"""
FinOps Tracker v2 — Production-grade cost tracking for GEO research.

Integrated directly into LLMClient via hooks. Uses real token counts
from API responses (never estimates). Implements circuit breaker,
anomaly detection, and multi-level alerting.
"""
from __future__ import annotations

import json
import logging
import os
import sqlite3
import statistics
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Optional

import httpx

logger = logging.getLogger("finops")

ALERT_EMAIL = os.getenv("FINOPS_ALERT_EMAIL", "")

# ============================================================
# PRICING — per 1M tokens, updated Mar 2026
# ============================================================

PRICING: dict[str, dict[str, dict[str, float]]] = {
    "openai": {
        "gpt-4o":         {"input": 2.50,  "output": 10.00},
        "gpt-4o-mini":    {"input": 0.15,  "output": 0.60},
        "gpt-4.1-nano":   {"input": 0.10,  "output": 0.40},
        "gpt-4.1-mini":   {"input": 0.40,  "output": 1.60},
        "gpt-4.1":        {"input": 2.00,  "output": 8.00},
        "_default":       {"input": 0.15,  "output": 0.60},
    },
    "anthropic": {
        "claude-haiku-4-5-20251001":  {"input": 0.80,  "output": 4.00},
        "claude-sonnet-4-20250514":   {"input": 3.00,  "output": 15.00},
        "claude-opus-4-20250514":     {"input": 15.00, "output": 75.00},
        "_default":                   {"input": 3.00,  "output": 15.00},
    },
    "google": {
        "gemini-2.5-flash":      {"input": 0.15,  "output": 0.60},  # Billing ativo (R$500 credito)
        "gemini-2.0-flash":      {"input": 0.10,  "output": 0.40},
        "gemini-2.0-flash-lite": {"input": 0.0,   "output": 0.0},
        "gemini-2.5-pro":        {"input": 1.25,  "output": 10.00},
        "_default":              {"input": 0.15,  "output": 0.60},
    },
    "perplexity": {
        "sonar":                                  {"input": 1.00,  "output": 1.00},
        "sonar-pro":                              {"input": 3.00,  "output": 15.00},
        "llama-3.1-sonar-small-128k-online":      {"input": 0.20,  "output": 0.20},
        "_default":                               {"input": 1.00,  "output": 1.00},
    },
    "groq": {
        "llama-3.3-70b-versatile":                {"input": 0.59,  "output": 0.79},
        "llama-3.1-8b-instant":                   {"input": 0.05,  "output": 0.08},
        "_default":                               {"input": 0.59,  "output": 0.79},
    },
}

DEFAULT_BUDGETS: dict[str, dict[str, float]] = {
    "openai":     {"monthly": 10.0, "daily": 1.0,  "alert_pct": 0.70, "hard_stop_pct": 0.95},
    "anthropic":  {"monthly": 10.0, "daily": 1.0,  "alert_pct": 0.70, "hard_stop_pct": 0.95},
    "google":     {"monthly": 5.0,  "daily": 0.50, "alert_pct": 0.80, "hard_stop_pct": 1.00},
    "perplexity": {"monthly": 10.0, "daily": 1.0,  "alert_pct": 0.70, "hard_stop_pct": 0.95},
    "groq":       {"monthly": 5.0,  "daily": 1.0,  "alert_pct": 0.80, "hard_stop_pct": 1.00},
    "global":     {"monthly": 35.0, "daily": 4.0,  "alert_pct": 0.70, "hard_stop_pct": 0.95},
}

# Anomaly: flag if single query costs more than this
ANOMALY_SINGLE_QUERY_USD = 0.50
# Anomaly: flag if hourly spend exceeds this
ANOMALY_HOURLY_SPIKE_USD = 2.00


# ============================================================
# DATA CLASSES
# ============================================================

@dataclass
class UsageRecord:
    """Immutable record of a single API call's cost."""
    platform: str
    model: str
    operation: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    cost_usd: float
    query: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    run_id: str = ""


@dataclass
class BudgetStatus:
    """Current budget status for a platform."""
    platform: str
    monthly_spend: float
    monthly_limit: float
    monthly_pct: float
    daily_spend: float
    daily_limit: float
    daily_pct: float
    is_blocked: bool
    queries_today: int
    tokens_today: int


# ============================================================
# SCHEMA
# ============================================================

FINOPS_SCHEMA = """
CREATE TABLE IF NOT EXISTS finops_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    platform TEXT NOT NULL,
    model TEXT NOT NULL,
    operation TEXT NOT NULL,
    input_tokens INTEGER NOT NULL DEFAULT 0,
    output_tokens INTEGER NOT NULL DEFAULT 0,
    total_tokens INTEGER NOT NULL DEFAULT 0,
    cost_usd REAL NOT NULL DEFAULT 0.0,
    query TEXT DEFAULT '',
    run_id TEXT DEFAULT '',
    CHECK (input_tokens >= 0),
    CHECK (output_tokens >= 0),
    CHECK (cost_usd >= 0)
);

CREATE INDEX IF NOT EXISTS idx_finops_usage_ts ON finops_usage(timestamp);
CREATE INDEX IF NOT EXISTS idx_finops_usage_platform ON finops_usage(platform);
CREATE INDEX IF NOT EXISTS idx_finops_usage_platform_ts ON finops_usage(platform, timestamp);
CREATE INDEX IF NOT EXISTS idx_finops_usage_run ON finops_usage(run_id);

CREATE TABLE IF NOT EXISTS finops_budgets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    platform TEXT UNIQUE NOT NULL,
    monthly_limit_usd REAL NOT NULL DEFAULT 10.0,
    daily_limit_usd REAL NOT NULL DEFAULT 1.0,
    alert_threshold_pct REAL NOT NULL DEFAULT 0.70,
    hard_stop_pct REAL NOT NULL DEFAULT 0.95,
    updated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    CHECK (monthly_limit_usd >= 0),
    CHECK (daily_limit_usd >= 0),
    CHECK (alert_threshold_pct > 0 AND alert_threshold_pct <= 1),
    CHECK (hard_stop_pct > 0 AND hard_stop_pct <= 1)
);

CREATE TABLE IF NOT EXISTS finops_alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    platform TEXT NOT NULL,
    alert_type TEXT NOT NULL,
    severity TEXT NOT NULL DEFAULT 'warning',
    message TEXT NOT NULL,
    current_spend_usd REAL NOT NULL,
    limit_usd REAL NOT NULL,
    pct_used REAL NOT NULL,
    sent_email INTEGER NOT NULL DEFAULT 0,
    email_to TEXT DEFAULT '',
    run_id TEXT DEFAULT '',
    acknowledged INTEGER NOT NULL DEFAULT 0,
    CHECK (alert_type IN (
        'budget_warning', 'budget_critical', 'budget_exceeded',
        'daily_warning', 'daily_critical', 'daily_exceeded',
        'anomaly_single_query', 'anomaly_hourly_spike',
        'credit_low', 'circuit_open'
    )),
    CHECK (severity IN ('info', 'warning', 'critical', 'emergency'))
);

CREATE INDEX IF NOT EXISTS idx_finops_alerts_ts ON finops_alerts(timestamp);
CREATE INDEX IF NOT EXISTS idx_finops_alerts_type ON finops_alerts(alert_type, platform);

CREATE TABLE IF NOT EXISTS finops_daily_rollup (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    platform TEXT NOT NULL,
    total_queries INTEGER NOT NULL DEFAULT 0,
    total_input_tokens INTEGER NOT NULL DEFAULT 0,
    total_output_tokens INTEGER NOT NULL DEFAULT 0,
    total_cost_usd REAL NOT NULL DEFAULT 0.0,
    avg_cost_per_query REAL NOT NULL DEFAULT 0.0,
    max_single_query_cost REAL NOT NULL DEFAULT 0.0,
    models_used TEXT DEFAULT '[]',
    UNIQUE(date, platform)
);

CREATE INDEX IF NOT EXISTS idx_finops_rollup_date ON finops_daily_rollup(date);
"""


# ============================================================
# TRACKER
# ============================================================

class FinOpsTracker:
    """Production-grade cost tracker with circuit breaker and anomaly detection."""

    def __init__(self, db_path: str | None = None) -> None:
        self._db_path = db_path or os.getenv(
            "PAPERS_DB_PATH",
            str(Path(__file__).resolve().parent.parent.parent / "data" / "papers.db"),
        )
        self._circuit_open: dict[str, datetime] = {}  # platform -> open_until
        self._ensure_schema()
        self._ensure_budgets()

    # --- DB helpers ---

    def _conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        conn.row_factory = sqlite3.Row
        return conn

    def _ensure_schema(self) -> None:
        with self._conn() as conn:
            conn.executescript(FINOPS_SCHEMA)

    def _ensure_budgets(self) -> None:
        with self._conn() as conn:
            for platform, b in DEFAULT_BUDGETS.items():
                exists = conn.execute(
                    "SELECT 1 FROM finops_budgets WHERE platform = ?", (platform,)
                ).fetchone()
                if not exists:
                    conn.execute(
                        "INSERT INTO finops_budgets (platform, monthly_limit_usd, daily_limit_usd, alert_threshold_pct, hard_stop_pct) VALUES (?, ?, ?, ?, ?)",
                        (platform, b["monthly"], b["daily"], b["alert_pct"], b["hard_stop_pct"]),
                    )

    # --- Cost calculation ---

    @staticmethod
    def calculate_cost(platform: str, model: str, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost in USD from real token counts."""
        provider_prices = PRICING.get(platform, {})
        prices = provider_prices.get(model, provider_prices.get("_default", {"input": 0, "output": 0}))
        cost = (input_tokens * prices["input"] + output_tokens * prices["output"]) / 1_000_000
        return round(cost, 8)

    @staticmethod
    def extract_tokens(platform: str, raw_response: dict[str, Any] | None) -> tuple[int, int]:
        """Extract real input/output token counts from API response.

        Each provider returns usage data differently. This handles all formats
        and returns (input_tokens, output_tokens). Never estimates.
        """
        if not raw_response:
            return 0, 0

        usage = raw_response.get("usage") or raw_response.get("usageMetadata") or {}

        if platform == "openai" or platform == "perplexity":
            return (
                usage.get("prompt_tokens", 0),
                usage.get("completion_tokens", 0),
            )
        elif platform == "anthropic":
            return (
                usage.get("input_tokens", 0),
                usage.get("output_tokens", 0),
            )
        elif platform == "google":
            return (
                usage.get("promptTokenCount", 0),
                usage.get("candidatesTokenCount", 0),
            )
        return 0, 0

    # --- Pre-flight check ---

    def can_spend(self, platform: str) -> bool:
        """Check if platform is within budget AND circuit is closed.

        Call this BEFORE making an API request.
        Returns False if budget exceeded or circuit is open.
        """
        # Circuit breaker check
        if platform in self._circuit_open:
            if datetime.now(timezone.utc) < self._circuit_open[platform]:
                logger.warning(f"[finops] Circuit OPEN for {platform} — skipping")
                return False
            else:
                del self._circuit_open[platform]
                logger.info(f"[finops] Circuit CLOSED for {platform} — resuming")

        with self._conn() as conn:
            budget = conn.execute(
                "SELECT monthly_limit_usd, daily_limit_usd, hard_stop_pct FROM finops_budgets WHERE platform = ?",
                (platform,),
            ).fetchone()
            if not budget:
                return True

            now = datetime.now(timezone.utc)
            month_start = now.strftime("%Y-%m-01T00:00:00Z")
            day_start = now.strftime("%Y-%m-%dT00:00:00Z")

            monthly = conn.execute(
                "SELECT COALESCE(SUM(cost_usd), 0) FROM finops_usage WHERE platform = ? AND timestamp >= ?",
                (platform, month_start),
            ).fetchone()[0]

            daily = conn.execute(
                "SELECT COALESCE(SUM(cost_usd), 0) FROM finops_usage WHERE platform = ? AND timestamp >= ?",
                (platform, day_start),
            ).fetchone()[0]

            hard_stop = budget["hard_stop_pct"]
            if budget["daily_limit_usd"] > 0 and daily / budget["daily_limit_usd"] >= hard_stop:
                return False
            if budget["monthly_limit_usd"] > 0 and monthly / budget["monthly_limit_usd"] >= hard_stop:
                return False

            # Global check
            global_budget = conn.execute(
                "SELECT monthly_limit_usd, hard_stop_pct FROM finops_budgets WHERE platform = 'global'"
            ).fetchone()
            if global_budget:
                global_monthly = conn.execute(
                    "SELECT COALESCE(SUM(cost_usd), 0) FROM finops_usage WHERE timestamp >= ?",
                    (month_start,),
                ).fetchone()[0]
                if global_monthly / max(global_budget["monthly_limit_usd"], 0.001) >= global_budget["hard_stop_pct"]:
                    return False

        return True

    # --- Record usage ---

    def record(
        self,
        platform: str,
        model: str,
        operation: str,
        input_tokens: int,
        output_tokens: int,
        query: str = "",
        run_id: str = "",
        raw_response: dict[str, Any] | None = None,
    ) -> UsageRecord:
        """Record a single API call. Runs all checks post-hoc.

        If raw_response is provided, extracts real token counts
        (overriding any passed values).
        """
        # Prefer real token counts from API response
        if raw_response:
            real_in, real_out = self.extract_tokens(platform, raw_response)
            if real_in > 0 or real_out > 0:
                input_tokens, output_tokens = real_in, real_out

        cost = self.calculate_cost(platform, model, input_tokens, output_tokens)
        total = input_tokens + output_tokens
        ts = datetime.now(timezone.utc).isoformat()

        record = UsageRecord(
            platform=platform, model=model, operation=operation,
            input_tokens=input_tokens, output_tokens=output_tokens,
            total_tokens=total, cost_usd=cost, query=query[:200],
            timestamp=ts, run_id=run_id,
        )

        with self._conn() as conn:
            conn.execute(
                "INSERT INTO finops_usage (timestamp, platform, model, operation, input_tokens, output_tokens, total_tokens, cost_usd, query, run_id) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (ts, platform, model, operation, input_tokens, output_tokens, total, cost, query[:200], run_id),
            )

        # Post-hoc checks (non-blocking)
        self._check_anomaly(platform, cost, query)
        self._check_budgets(platform)

        logger.debug(f"[finops] {platform}/{model}: {input_tokens}+{output_tokens} tokens = ${cost:.6f}")
        return record

    # --- Budget checks ---

    def _check_budgets(self, platform: str) -> None:
        """Check monthly and daily budgets, trigger alerts."""
        with self._conn() as conn:
            budget = conn.execute(
                "SELECT * FROM finops_budgets WHERE platform = ?", (platform,)
            ).fetchone()
            if not budget:
                return

            now = datetime.now(timezone.utc)
            month_start = now.strftime("%Y-%m-01T00:00:00Z")
            day_start = now.strftime("%Y-%m-%dT00:00:00Z")

            monthly_spend = conn.execute(
                "SELECT COALESCE(SUM(cost_usd), 0) FROM finops_usage WHERE platform = ? AND timestamp >= ?",
                (platform, month_start),
            ).fetchone()[0]

            daily_spend = conn.execute(
                "SELECT COALESCE(SUM(cost_usd), 0) FROM finops_usage WHERE platform = ? AND timestamp >= ?",
                (platform, day_start),
            ).fetchone()[0]

            # Monthly budget
            if budget["monthly_limit_usd"] > 0:
                pct = monthly_spend / budget["monthly_limit_usd"]
                self._evaluate_threshold(
                    conn, platform, "monthly", pct, monthly_spend,
                    budget["monthly_limit_usd"], budget["alert_threshold_pct"],
                )

            # Daily budget
            if budget["daily_limit_usd"] > 0:
                pct = daily_spend / budget["daily_limit_usd"]
                self._evaluate_threshold(
                    conn, platform, "daily", pct, daily_spend,
                    budget["daily_limit_usd"], budget["alert_threshold_pct"],
                )

    def _evaluate_threshold(
        self, conn: sqlite3.Connection, platform: str, period: str,
        pct: float, current: float, limit: float, alert_pct: float,
    ) -> None:
        """Evaluate spend against thresholds and emit alerts."""
        if pct >= 1.0:
            self._emit_alert(conn, platform, f"{period}_exceeded", "emergency", current, limit, pct)
        elif pct >= 0.90:
            self._emit_alert(conn, platform, f"{period}_critical", "critical", current, limit, pct)
        elif pct >= alert_pct:
            self._emit_alert(conn, platform, f"{period}_warning", "warning", current, limit, pct)

    # --- Anomaly detection ---

    def _check_anomaly(self, platform: str, cost: float, query: str) -> None:
        """Detect anomalous spending patterns."""
        # Single query cost anomaly
        if cost > ANOMALY_SINGLE_QUERY_USD:
            with self._conn() as conn:
                self._emit_alert(
                    conn, platform, "anomaly_single_query", "warning",
                    cost, ANOMALY_SINGLE_QUERY_USD, cost / ANOMALY_SINGLE_QUERY_USD,
                    extra=f"Query custou ${cost:.4f}: {query[:80]}",
                )

        # Hourly spike detection
        with self._conn() as conn:
            hour_ago = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
            hourly = conn.execute(
                "SELECT COALESCE(SUM(cost_usd), 0) FROM finops_usage WHERE platform = ? AND timestamp >= ?",
                (platform, hour_ago),
            ).fetchone()[0]
            if hourly > ANOMALY_HOURLY_SPIKE_USD:
                self._emit_alert(
                    conn, platform, "anomaly_hourly_spike", "critical",
                    hourly, ANOMALY_HOURLY_SPIKE_USD, hourly / ANOMALY_HOURLY_SPIKE_USD,
                    extra=f"${hourly:.4f} na última hora",
                )
                # Open circuit breaker for 30 min
                self._circuit_open[platform] = datetime.now(timezone.utc) + timedelta(minutes=30)
                logger.warning(f"[finops] Circuit OPEN for {platform} — hourly spike ${hourly:.4f}")

    # --- Alert emission ---

    def _emit_alert(
        self, conn: sqlite3.Connection, platform: str, alert_type: str,
        severity: str, current: float, limit: float, pct: float,
        extra: str = "",
    ) -> None:
        """Emit alert with dedup (max 1 per type/platform/6h)."""
        six_hours_ago = (datetime.now(timezone.utc) - timedelta(hours=6)).isoformat()
        recent = conn.execute(
            "SELECT COUNT(*) FROM finops_alerts WHERE platform = ? AND alert_type = ? AND timestamp >= ?",
            (platform, alert_type, six_hours_ago),
        ).fetchone()[0]
        if recent > 0:
            return

        msg = f"{platform} {alert_type}: ${current:.4f}/${limit:.2f} ({pct*100:.1f}%)"
        if extra:
            msg += f" — {extra}"

        sent = self._send_email(severity, alert_type, platform, msg, current, limit, pct)

        conn.execute(
            "INSERT INTO finops_alerts (timestamp, platform, alert_type, severity, message, current_spend_usd, limit_usd, pct_used, sent_email, email_to) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (datetime.now(timezone.utc).isoformat(), platform, alert_type, severity, msg, current, limit, round(pct * 100, 1), int(sent), ALERT_EMAIL),
        )

        level = {"info": logging.INFO, "warning": logging.WARNING, "critical": logging.ERROR, "emergency": logging.CRITICAL}.get(severity, logging.WARNING)
        logger.log(level, f"[ALERT] {msg}")

    def _send_email(self, severity: str, alert_type: str, platform: str, message: str, current: float, limit: float, pct: float) -> bool:
        """Send alert via Resend API."""
        api_key = os.getenv("RESEND_API_KEY", "")
        if not api_key:
            return False

        colors = {"info": "#3b82f6", "warning": "#d97706", "critical": "#dc2626", "emergency": "#7f1d1d"}
        color = colors.get(severity, "#d97706")

        html = f"""
        <div style="font-family:system-ui;max-width:600px;margin:0 auto;">
            <div style="background:{color};color:white;padding:16px 24px;border-radius:8px 8px 0 0;">
                <h2 style="margin:0;">FinOps {severity.upper()}: {platform}</h2>
                <p style="margin:4px 0 0;opacity:0.9;">{alert_type}</p>
            </div>
            <div style="background:#1a1a2e;color:#e0e0e0;padding:24px;border-radius:0 0 8px 8px;">
                <p>{message}</p>
                <table style="width:100%;border-collapse:collapse;margin:16px 0;">
                    <tr><td style="padding:6px;border-bottom:1px solid #333;">Plataforma</td><td style="text-align:right;padding:6px;border-bottom:1px solid #333;font-weight:700;">{platform}</td></tr>
                    <tr><td style="padding:6px;border-bottom:1px solid #333;">Gasto</td><td style="text-align:right;padding:6px;border-bottom:1px solid #333;color:#f87171;font-weight:700;">${current:.4f}</td></tr>
                    <tr><td style="padding:6px;border-bottom:1px solid #333;">Limite</td><td style="text-align:right;padding:6px;border-bottom:1px solid #333;">${limit:.2f}</td></tr>
                    <tr><td style="padding:6px;">Uso</td><td style="text-align:right;padding:6px;font-weight:700;">{pct*100:.1f}%</td></tr>
                </table>
                <p style="font-size:12px;color:#6b7280;">GEO Research FinOps — {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}</p>
            </div>
        </div>"""

        try:
            r = httpx.post(
                "https://api.resend.com/emails",
                headers={"Authorization": f"Bearer {api_key}"},
                json={
                    "from": "GEO FinOps <onboarding@resend.dev>",
                    "to": [ALERT_EMAIL],
                    "subject": f"[FinOps {severity.upper()}] {platform}: {alert_type} ({pct*100:.0f}%)",
                    "html": html,
                },
                timeout=10,
            )
            return r.status_code == 200
        except Exception as e:
            logger.warning(f"[finops] Email failed: {e}")
            return False

    # --- Reporting ---

    def get_status(self, platform: str | None = None) -> list[BudgetStatus]:
        """Get budget status for one or all platforms."""
        platforms = [platform] if platform else ["openai", "anthropic", "google", "perplexity"]
        now = datetime.now(timezone.utc)
        month_start = now.strftime("%Y-%m-01T00:00:00Z")
        day_start = now.strftime("%Y-%m-%dT00:00:00Z")
        results = []

        with self._conn() as conn:
            for p in platforms:
                budget = conn.execute(
                    "SELECT monthly_limit_usd, daily_limit_usd, hard_stop_pct FROM finops_budgets WHERE platform = ?",
                    (p,),
                ).fetchone()
                if not budget:
                    continue

                row_m = conn.execute(
                    "SELECT COALESCE(SUM(cost_usd), 0), COALESCE(SUM(total_tokens), 0), COUNT(*) FROM finops_usage WHERE platform = ? AND timestamp >= ?",
                    (p, month_start),
                ).fetchone()

                row_d = conn.execute(
                    "SELECT COALESCE(SUM(cost_usd), 0), COALESCE(SUM(total_tokens), 0), COUNT(*) FROM finops_usage WHERE platform = ? AND timestamp >= ?",
                    (p, day_start),
                ).fetchone()

                m_limit = budget["monthly_limit_usd"]
                d_limit = budget["daily_limit_usd"]

                results.append(BudgetStatus(
                    platform=p,
                    monthly_spend=round(row_m[0], 4),
                    monthly_limit=m_limit,
                    monthly_pct=round(row_m[0] / max(m_limit, 0.001) * 100, 1),
                    daily_spend=round(row_d[0], 4),
                    daily_limit=d_limit,
                    daily_pct=round(row_d[0] / max(d_limit, 0.001) * 100, 1),
                    is_blocked=not self.can_spend(p),
                    queries_today=row_d[2],
                    tokens_today=row_d[1],
                ))

        return results

    def rollup_daily(self) -> None:
        """Compute daily rollup for historical analysis. Run at end of day."""
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        day_start = f"{today}T00:00:00Z"
        day_end = f"{today}T23:59:59Z"

        with self._conn() as conn:
            platforms = conn.execute(
                "SELECT DISTINCT platform FROM finops_usage WHERE timestamp >= ? AND timestamp <= ?",
                (day_start, day_end),
            ).fetchall()

            for (platform,) in platforms:
                row = conn.execute(
                    "SELECT COUNT(*), SUM(input_tokens), SUM(output_tokens), SUM(cost_usd), AVG(cost_usd), MAX(cost_usd), "
                    "GROUP_CONCAT(DISTINCT model) FROM finops_usage WHERE platform = ? AND timestamp >= ? AND timestamp <= ?",
                    (platform, day_start, day_end),
                ).fetchone()

                conn.execute(
                    "INSERT OR REPLACE INTO finops_daily_rollup (date, platform, total_queries, total_input_tokens, total_output_tokens, total_cost_usd, avg_cost_per_query, max_single_query_cost, models_used) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (today, platform, row[0], row[1] or 0, row[2] or 0, round(row[3] or 0, 6), round(row[4] or 0, 8), round(row[5] or 0, 6), json.dumps((row[6] or "").split(","))),
                )

    def set_budget(self, platform: str, monthly: float | None = None, daily: float | None = None) -> None:
        """Update budget limits for a platform."""
        with self._conn() as conn:
            if monthly is not None:
                conn.execute(
                    "UPDATE finops_budgets SET monthly_limit_usd = ?, updated_at = ? WHERE platform = ?",
                    (monthly, datetime.now(timezone.utc).isoformat(), platform),
                )
            if daily is not None:
                conn.execute(
                    "UPDATE finops_budgets SET daily_limit_usd = ?, updated_at = ? WHERE platform = ?",
                    (daily, datetime.now(timezone.utc).isoformat(), platform),
                )
        logger.info(f"[finops] Budget updated: {platform} monthly=${monthly} daily=${daily}")


# Singleton for use across the application
_tracker: FinOpsTracker | None = None


def get_tracker() -> FinOpsTracker:
    """Get or create the global FinOpsTracker instance."""
    global _tracker
    if _tracker is None:
        _tracker = FinOpsTracker()
    return _tracker
