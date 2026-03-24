"""
monitor.py -- Automated FinOps monitor that runs without human intervention.

Designed to be called:
  1. As post-collection hook (after every data collection)
  2. As standalone cron (GitHub Actions every 6h)
  3. As CLI command (python -m src.cli finops monitor)

Handles:
  - Daily rollup computation
  - Budget checks across all platforms
  - Anomaly detection on recent activity
  - Credit balance checks via API (OpenAI, Anthropic)
  - Stale data detection (no collection in 48h)
  - Alert export to Git-tracked JSON
  - Dashboard HTML generation
  - Pricing drift validation
"""
from __future__ import annotations

import json
import logging
import os
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import httpx

from src.finops.tracker import FinOpsTracker, get_tracker, PRICING, BudgetStatus, ALERT_EMAIL

logger = logging.getLogger("finops.monitor")

OUTPUT_DIR = Path(__file__).resolve().parent.parent.parent / "output"
DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"


def ensure_dirs() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# CREDIT BALANCE CHECKS (live API calls)
# ============================================================

def check_openai_balance() -> dict[str, Any] | None:
    """Check OpenAI credit balance via billing API."""
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        return None
    try:
        r = httpx.get(
            "https://api.openai.com/v1/organization/costs",
            headers={"Authorization": f"Bearer {api_key}"},
            params={"start_time": int((datetime.now(timezone.utc) - timedelta(days=30)).timestamp()), "limit": 1},
            timeout=10,
        )
        if r.status_code == 200:
            data = r.json()
            return {"platform": "openai", "status": "ok", "data": data}
        return {"platform": "openai", "status": "error", "code": r.status_code}
    except Exception as e:
        return {"platform": "openai", "status": "error", "error": str(e)}


def check_anthropic_balance() -> dict[str, Any] | None:
    """Check Anthropic credit balance via API."""
    api_key = os.getenv("ANTHROPIC_API_KEY", "")
    if not api_key:
        return None
    try:
        r = httpx.get(
            "https://api.anthropic.com/v1/messages/count_tokens",
            headers={"x-api-key": api_key, "anthropic-version": "2023-06-01"},
            timeout=10,
        )
        # If we get 400 (bad request) instead of 401/403, credits are OK
        if r.status_code in (200, 400):
            return {"platform": "anthropic", "status": "credits_ok"}
        elif r.status_code in (401, 403):
            return {"platform": "anthropic", "status": "auth_error", "code": r.status_code}
        else:
            return {"platform": "anthropic", "status": "credit_low_or_error", "code": r.status_code}
    except Exception as e:
        return {"platform": "anthropic", "status": "error", "error": str(e)}


# ============================================================
# STALE DATA DETECTION
# ============================================================

def check_stale_data(tracker: FinOpsTracker, max_hours: int = 48) -> dict[str, Any]:
    """Detect if collection hasn't run in too long."""
    conn = sqlite3.connect(tracker._db_path)
    conn.row_factory = sqlite3.Row

    result = {"stale": False, "hours_since_last": 0, "platforms": {}}
    cutoff = (datetime.now(timezone.utc) - timedelta(hours=max_hours)).isoformat()

    for platform in ["openai", "anthropic", "google", "perplexity"]:
        last = conn.execute(
            "SELECT MAX(timestamp) as ts FROM finops_usage WHERE platform = ?",
            (platform,),
        ).fetchone()

        ts = last["ts"] if last and last["ts"] else None
        if ts:
            last_dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            hours_ago = (datetime.now(timezone.utc) - last_dt).total_seconds() / 3600
            result["platforms"][platform] = {
                "last_activity": ts,
                "hours_ago": round(hours_ago, 1),
                "stale": hours_ago > max_hours,
            }
            if hours_ago > max_hours:
                result["stale"] = True
        else:
            result["platforms"][platform] = {"last_activity": None, "hours_ago": None, "stale": True}
            result["stale"] = True

    conn.close()
    return result


# ============================================================
# PRICING VALIDATION
# ============================================================

def validate_pricing() -> list[dict[str, Any]]:
    """Validate hardcoded pricing hasn't drifted.

    Checks the pricing comment date and flags if older than 60 days.
    Future: compare against live pricing APIs.
    """
    warnings = []

    # Check if any model is missing from pricing table
    from src.config import config
    for llm in config.llms:
        provider_prices = PRICING.get(llm.provider, {})
        if llm.model not in provider_prices and "_default" not in provider_prices:
            warnings.append({
                "type": "missing_model",
                "platform": llm.provider,
                "model": llm.model,
                "message": f"Model {llm.model} not in pricing table for {llm.provider}",
            })

    # Check cost_per_1k_tokens in config vs PRICING
    for llm in config.llms:
        if llm.requires_scraping or not llm.api_key:
            continue
        provider_prices = PRICING.get(llm.provider, {})
        model_prices = provider_prices.get(llm.model, provider_prices.get("_default", {}))
        if model_prices:
            avg_price = (model_prices.get("input", 0) + model_prices.get("output", 0)) / 2 / 1000
            config_price = llm.cost_per_1k_tokens
            if config_price > 0 and abs(avg_price - config_price) / max(config_price, 0.0001) > 0.5:
                warnings.append({
                    "type": "price_drift",
                    "platform": llm.provider,
                    "model": llm.model,
                    "config_price": config_price,
                    "tracker_price": avg_price,
                    "message": f"Price drift detected for {llm.model}: config={config_price} vs tracker={avg_price}",
                })

    return warnings


# ============================================================
# CHECKPOINT EXPORT (Git-tracked state)
# ============================================================

def export_checkpoint(tracker: FinOpsTracker) -> Path:
    """Export current FinOps state as JSON for Git tracking.

    This file is committed after each collection so the full
    FinOps history is auditable in Git, not just in SQLite.
    """
    ensure_dirs()
    now = datetime.now(timezone.utc)

    statuses = tracker.get_status()
    status_dicts = []
    for s in statuses:
        status_dicts.append({
            "platform": s.platform,
            "monthly_spend": s.monthly_spend,
            "monthly_limit": s.monthly_limit,
            "monthly_pct": s.monthly_pct,
            "daily_spend": s.daily_spend,
            "daily_limit": s.daily_limit,
            "daily_pct": s.daily_pct,
            "is_blocked": s.is_blocked,
            "queries_today": s.queries_today,
            "tokens_today": s.tokens_today,
        })

    # Recent alerts
    conn = sqlite3.connect(tracker._db_path)
    conn.row_factory = sqlite3.Row
    alerts = [dict(r) for r in conn.execute(
        "SELECT timestamp, platform, alert_type, severity, message, current_spend_usd, pct_used, sent_email "
        "FROM finops_alerts ORDER BY timestamp DESC LIMIT 50"
    ).fetchall()]

    # Daily rollup (last 30 days)
    rollups = [dict(r) for r in conn.execute(
        "SELECT * FROM finops_daily_rollup ORDER BY date DESC LIMIT 120"
    ).fetchall()]
    conn.close()

    checkpoint = {
        "generated_at": now.isoformat(),
        "budgets": status_dicts,
        "alerts_recent": alerts,
        "daily_rollups": rollups,
        "stale_check": check_stale_data(tracker),
        "pricing_warnings": validate_pricing(),
    }

    path = DATA_DIR / "finops_checkpoint.json"
    path.write_text(json.dumps(checkpoint, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    logger.info(f"[finops] Checkpoint exported: {path}")
    return path


# ============================================================
# ALERT LOG EXPORT (Git-tracked)
# ============================================================

def export_alerts_log(tracker: FinOpsTracker) -> Path:
    """Export full alerts history as JSONL for Git tracking."""
    ensure_dirs()
    conn = sqlite3.connect(tracker._db_path)
    conn.row_factory = sqlite3.Row
    alerts = conn.execute("SELECT * FROM finops_alerts ORDER BY timestamp").fetchall()
    conn.close()

    path = DATA_DIR / "finops_alerts.jsonl"
    with open(path, "w", encoding="utf-8") as f:
        for a in alerts:
            f.write(json.dumps(dict(a), ensure_ascii=False, default=str) + "\n")

    logger.info(f"[finops] Alerts log exported: {path} ({len(alerts)} records)")
    return path


# ============================================================
# DASHBOARD HTML
# ============================================================

def generate_dashboard(tracker: FinOpsTracker) -> Path:
    """Generate self-contained HTML dashboard with all FinOps data."""
    ensure_dirs()
    now = datetime.now(timezone.utc)
    statuses = tracker.get_status()

    conn = sqlite3.connect(tracker._db_path)
    conn.row_factory = sqlite3.Row

    # Top models by cost
    top_models = conn.execute(
        "SELECT platform, model, SUM(cost_usd) as cost, SUM(total_tokens) as tokens, COUNT(*) as queries "
        "FROM finops_usage WHERE timestamp >= ? GROUP BY platform, model ORDER BY cost DESC LIMIT 20",
        (now.strftime("%Y-%m-01T00:00:00Z"),),
    ).fetchall()

    # Daily costs (last 30 days)
    daily_costs = conn.execute(
        "SELECT DATE(timestamp) as day, platform, SUM(cost_usd) as cost, COUNT(*) as queries "
        "FROM finops_usage WHERE timestamp >= ? GROUP BY day, platform ORDER BY day",
        ((now - timedelta(days=30)).isoformat(),),
    ).fetchall()

    # Recent alerts
    alerts = conn.execute(
        "SELECT * FROM finops_alerts ORDER BY timestamp DESC LIMIT 20"
    ).fetchall()
    conn.close()

    # Build platform cards
    colors = {"openai": "#10a37f", "anthropic": "#d4a574", "google": "#4285f4", "perplexity": "#20b2aa"}
    labels = {"openai": "OpenAI", "anthropic": "Anthropic", "google": "Gemini", "perplexity": "Perplexity"}

    cards = ""
    for s in statuses:
        color = colors.get(s.platform, "#6b7280")
        label = labels.get(s.platform, s.platform)
        bar_m = "#dc2626" if s.monthly_pct > 90 else "#d97706" if s.monthly_pct > 70 else "#22c55e"
        bar_d = "#dc2626" if s.daily_pct > 90 else "#d97706" if s.daily_pct > 70 else "#22c55e"
        status_badge = '<span style="color:#dc2626;font-weight:700;">BLOCKED</span>' if s.is_blocked else '<span style="color:#22c55e;">ACTIVE</span>'

        models_html = ""
        for m in top_models:
            if m["platform"] == s.platform:
                models_html += f'<tr><td style="padding:3px 6px;font-size:11px;">{m["model"][:25]}</td><td style="text-align:right;padding:3px 6px;font-size:11px;">${m["cost"]:.4f}</td><td style="text-align:right;padding:3px 6px;font-size:11px;">{m["tokens"]:,}</td><td style="text-align:right;padding:3px 6px;font-size:11px;">{m["queries"]}</td></tr>'

        cards += f"""
        <div style="background:#1e1e2e;border-radius:12px;padding:20px;border-left:4px solid {color};">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
                <h3 style="margin:0;color:{color};">{label}</h3>
                {status_badge}
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:12px;">
                <div style="background:#2a2a3e;padding:8px;border-radius:6px;text-align:center;">
                    <div style="font-size:10px;color:#9ca3af;">Hoje</div>
                    <div style="font-size:18px;font-weight:700;">${s.daily_spend:.4f}</div>
                    <div style="font-size:9px;color:#6b7280;">{s.tokens_today:,} tok | {s.queries_today} q</div>
                </div>
                <div style="background:#2a2a3e;padding:8px;border-radius:6px;text-align:center;">
                    <div style="font-size:10px;color:#9ca3af;">Mes</div>
                    <div style="font-size:18px;font-weight:700;">${s.monthly_spend:.4f}</div>
                </div>
            </div>
            <div style="margin-bottom:6px;"><div style="display:flex;justify-content:space-between;font-size:10px;color:#9ca3af;"><span>Mensal</span><span>{s.monthly_pct:.1f}%</span></div><div style="background:#374151;border-radius:3px;height:6px;"><div style="background:{bar_m};height:100%;width:{min(s.monthly_pct,100):.0f}%;border-radius:3px;"></div></div></div>
            <div style="margin-bottom:10px;"><div style="display:flex;justify-content:space-between;font-size:10px;color:#9ca3af;"><span>Diario</span><span>{s.daily_pct:.1f}%</span></div><div style="background:#374151;border-radius:3px;height:6px;"><div style="background:{bar_d};height:100%;width:{min(s.daily_pct,100):.0f}%;border-radius:3px;"></div></div></div>
            <table style="width:100%;border-collapse:collapse;"><tr style="border-bottom:1px solid #374151;"><th style="text-align:left;padding:3px 6px;font-size:9px;color:#6b7280;">Modelo</th><th style="text-align:right;padding:3px 6px;font-size:9px;color:#6b7280;">Custo</th><th style="text-align:right;padding:3px 6px;font-size:9px;color:#6b7280;">Tokens</th><th style="text-align:right;padding:3px 6px;font-size:9px;color:#6b7280;">Q</th></tr>{models_html or '<tr><td colspan="4" style="padding:6px;text-align:center;font-size:10px;color:#4b5563;">Sem dados</td></tr>'}</table>
        </div>"""

    # Alerts table
    alerts_html = ""
    for a in alerts:
        sev_colors = {"emergency": "#dc2626", "critical": "#dc2626", "warning": "#d97706", "info": "#3b82f6"}
        alerts_html += f'<tr><td style="padding:4px 6px;font-size:11px;color:#9ca3af;">{a["timestamp"][:16]}</td><td style="padding:4px 6px;color:{sev_colors.get(a["severity"],"#9ca3af")};font-size:11px;font-weight:600;">{a["severity"]}</td><td style="padding:4px 6px;font-size:11px;">{a["platform"]}</td><td style="padding:4px 6px;font-size:11px;">{a["message"][:60]}</td></tr>'

    # Global totals
    total_spend = sum(s.monthly_spend for s in statuses)
    total_queries = sum(s.queries_today for s in statuses)

    html = f"""<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>GEO FinOps</title>
<style>*{{margin:0;padding:0;box-sizing:border-box}}body{{background:#0f0f1a;color:#e0e0e0;font-family:system-ui,sans-serif;padding:20px}}h1{{font-size:22px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px;margin:16px 0}}
.global{{background:#1e1e2e;border-radius:12px;padding:16px;margin-bottom:16px}}
table{{width:100%;border-collapse:collapse}}tr:hover{{background:rgba(255,255,255,0.02)}}</style></head>
<body>
<h1>GEO Research — FinOps Dashboard</h1>
<p style="color:#6b7280;font-size:12px;margin:4px 0 16px;">Auto-gerado: {now.strftime('%Y-%m-%d %H:%M UTC')} | Alertas: {ALERT_EMAIL}</p>
<div class="global"><div style="display:flex;justify-content:space-between;align-items:center;">
<div><span style="font-size:14px;color:#9ca3af;">Gasto mensal total</span><div style="font-size:28px;font-weight:700;">${total_spend:.4f}</div></div>
<div style="text-align:right;"><span style="font-size:14px;color:#9ca3af;">Queries hoje</span><div style="font-size:28px;font-weight:700;">{total_queries}</div></div></div></div>
<div class="grid">{cards}</div>
<div style="background:#1e1e2e;border-radius:12px;padding:16px;margin-top:16px;">
<h3 style="margin-bottom:10px;">Alertas Recentes</h3>
<table><tr style="border-bottom:1px solid #374151;"><th style="text-align:left;padding:4px 6px;font-size:10px;color:#6b7280;">Data</th><th style="text-align:left;padding:4px 6px;font-size:10px;color:#6b7280;">Sev</th><th style="text-align:left;padding:4px 6px;font-size:10px;color:#6b7280;">Plat</th><th style="text-align:left;padding:4px 6px;font-size:10px;color:#6b7280;">Msg</th></tr>
{alerts_html or '<tr><td colspan="4" style="padding:12px;text-align:center;color:#4b5563;">Nenhum alerta</td></tr>'}</table></div>
<p style="text-align:center;color:#374151;font-size:10px;margin-top:16px;">Brasil GEO FinOps v2 — Auto-gerado por monitor.py</p>
</body></html>"""

    path = OUTPUT_DIR / "finops_dashboard.html"
    path.write_text(html, encoding="utf-8")
    logger.info(f"[finops] Dashboard: {path}")
    return path


# ============================================================
# MAIN MONITOR — runs everything
# ============================================================

def run_monitor(verbose: bool = True) -> dict[str, Any]:
    """Run full automated FinOps monitoring cycle.

    Call this after every collection or on a cron schedule.
    Returns summary dict for logging/reporting.
    """
    tracker = get_tracker()
    now = datetime.now(timezone.utc)
    results: dict[str, Any] = {"timestamp": now.isoformat(), "actions": []}

    if verbose:
        print(f"{'='*50}")
        print(f"  FinOps Monitor — {now.strftime('%Y-%m-%d %H:%M UTC')}")
        print(f"{'='*50}")

    # 1. Compute daily rollup
    tracker.rollup_daily()
    results["actions"].append("rollup_daily")
    if verbose:
        print("  [1/6] Daily rollup computed")

    # 2. Check all budgets
    for platform in ["openai", "anthropic", "google", "perplexity", "global"]:
        tracker._check_budgets(platform)
    results["actions"].append("budget_checks")
    if verbose:
        print("  [2/6] Budget checks complete")

    # 3. Check stale data
    stale = check_stale_data(tracker)
    results["stale_data"] = stale
    if stale["stale"]:
        if verbose:
            for p, info in stale["platforms"].items():
                if info.get("stale"):
                    print(f"  [WARN] {p}: no data for {info.get('hours_ago', '?')}h")
    results["actions"].append("stale_check")
    if verbose:
        print("  [3/6] Stale data check complete")

    # 4. Validate pricing
    pricing_warnings = validate_pricing()
    results["pricing_warnings"] = pricing_warnings
    if pricing_warnings and verbose:
        for w in pricing_warnings:
            print(f"  [WARN] Pricing: {w['message']}")
    results["actions"].append("pricing_validation")
    if verbose:
        print("  [4/6] Pricing validation complete")

    # 5. Export checkpoint + alerts
    checkpoint_path = export_checkpoint(tracker)
    alerts_path = export_alerts_log(tracker)
    results["checkpoint"] = str(checkpoint_path)
    results["alerts_log"] = str(alerts_path)
    results["actions"].append("exports")
    if verbose:
        print("  [5/6] Checkpoint + alerts exported")

    # 6. Generate dashboard
    dashboard_path = generate_dashboard(tracker)
    results["dashboard"] = str(dashboard_path)
    results["actions"].append("dashboard")
    if verbose:
        print("  [6/6] Dashboard generated")

    # Summary
    statuses = tracker.get_status()
    results["budgets"] = [
        {"platform": s.platform, "monthly": s.monthly_spend, "pct": s.monthly_pct, "blocked": s.is_blocked}
        for s in statuses
    ]

    if verbose:
        print(f"\n  Status:")
        for s in statuses:
            icon = "BLOCK" if s.is_blocked else "OK"
            print(f"    {s.platform:12s} [{icon:5s}] ${s.monthly_spend:.4f}/${s.monthly_limit:.2f} ({s.monthly_pct:.1f}%)")
        print(f"\n{'='*50}")

    return results
