#!/usr/bin/env python3
"""Sync aggregated Papers data from local SQLite to Supabase.

Reads the local papers.db, aggregates citation data per vertical,
and upserts JSON summaries to Supabase via REST API (httpx).
Designed to run as a GitHub Actions step after daily collection.

Usage:
    python scripts/sync_to_supabase.py

Env vars required:
    SUPABASE_URL  — Supabase project URL (e.g. https://xxx.supabase.co)
    SUPABASE_KEY  — Supabase service_role key (full write access)
    PAPERS_DB_PATH — path to SQLite DB (default: data/papers.db)
"""

from __future__ import annotations

import json
import os
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

import httpx

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SUPABASE_URL = os.getenv("SUPABASE_URL", "").rstrip("/")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
DB_PATH = os.getenv("PAPERS_DB_PATH", "data/papers.db")

VERTICALS = ["fintech", "varejo", "saude", "tecnologia"]

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "resolution=merge-duplicates",
}


# ---------------------------------------------------------------------------
# SQLite helpers
# ---------------------------------------------------------------------------

def get_conn() -> sqlite3.Connection:
    """Open SQLite connection with Row factory."""
    if not Path(DB_PATH).exists():
        print(f"[WARN] Banco não encontrado: {DB_PATH} — usando dados vazios")
        # Create in-memory placeholder so queries return empty
        conn = sqlite3.connect(":memory:")
        conn.row_factory = sqlite3.Row
        return conn
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def safe_fetchall(conn: sqlite3.Connection, sql: str, params: tuple = ()) -> list[dict]:
    """Execute query and return list of dicts, empty list on error."""
    try:
        rows = conn.execute(sql, params).fetchall()
        return [dict(r) for r in rows]
    except Exception as e:
        print(f"  [WARN] Query falhou: {e}")
        return []


# ---------------------------------------------------------------------------
# Aggregation queries (mirror main.py patterns)
# ---------------------------------------------------------------------------

def get_citation_rates(conn: sqlite3.Connection, vertical: str) -> list[dict]:
    """Citation rates by LLM for a vertical (last 30 days)."""
    rows = safe_fetchall(conn, """
        SELECT llm,
               COUNT(*) as total,
               SUM(CASE WHEN cited THEN 1 ELSE 0 END) as cited_count,
               AVG(CASE WHEN cited AND position IS NOT NULL THEN position ELSE NULL END) as avg_pos
        FROM citations
        WHERE timestamp >= datetime('now', '-30 days') AND vertical = ?
        GROUP BY llm
        ORDER BY cited_count DESC
    """, (vertical,))

    return [
        {
            "llm": r["llm"],
            "total_queries": r["total"],
            "cited_count": r["cited_count"],
            "citation_rate": round(r["cited_count"] / max(r["total"], 1), 4),
            "avg_position": round(r["avg_pos"], 2) if r["avg_pos"] else None,
        }
        for r in rows
    ]


def get_entity_rankings(conn: sqlite3.Connection, vertical: str, top: int = 15) -> list[dict]:
    """Top entities by citation count within a vertical, from citation_context joined with citations."""
    rows = safe_fetchall(conn, """
        SELECT cc.entity,
               COUNT(*) as citation_count,
               (SELECT COUNT(*) FROM citations c2 WHERE c2.vertical = ? AND c2.cited = 1) as total_cited,
               (SELECT c3.model FROM citations c3
                JOIN citation_context cc3 ON cc3.citation_id = c3.id
                WHERE cc3.entity = cc.entity AND c3.vertical = ?
                GROUP BY c3.model ORDER BY COUNT(*) DESC LIMIT 1) as top_llm
        FROM citation_context cc
        JOIN citations c ON cc.citation_id = c.id
        WHERE c.vertical = ?
        GROUP BY cc.entity
        ORDER BY citation_count DESC
        LIMIT ?
    """, (vertical, vertical, vertical, top))

    total_cited = rows[0]["total_cited"] if rows else 1
    return [
        {
            "entity": r["entity"],
            "citation_count": r["citation_count"],
            "citation_rate": round(r["citation_count"] / max(total_cited, 1), 4),
            "total": r["citation_count"],
            "top_llm": r["top_llm"] or "N/A",
        }
        for r in rows
    ]


def get_timeseries(conn: sqlite3.Connection, vertical: str, days: int = 90) -> list[dict]:
    """Daily citation rate for the last N days."""
    rows = safe_fetchall(conn, """
        SELECT date(timestamp) as dt,
               AVG(CASE WHEN cited THEN 1.0 ELSE 0.0 END) as rate,
               COUNT(*) as n
        FROM citations
        WHERE vertical = ? AND timestamp >= datetime('now', ?)
        GROUP BY dt
        ORDER BY dt ASC
    """, (vertical, f"-{days} days"))

    return [
        {
            "date": r["dt"],
            "rate": round(r["rate"], 4),
            "observations": r["n"],
        }
        for r in rows
    ]


def get_collection_status(conn: sqlite3.Connection, vertical: str) -> dict:
    """Collection status for a vertical."""
    # Last successful run
    last = safe_fetchall(conn, """
        SELECT MAX(timestamp) as ts
        FROM collection_runs
        WHERE vertical = ? AND status = 'success'
    """, (vertical,))
    last_run = last[0]["ts"] if last and last[0].get("ts") else None

    # Runs in last 24h
    count_rows = safe_fetchall(conn, """
        SELECT COUNT(*) as n
        FROM collection_runs
        WHERE vertical = ? AND timestamp >= datetime('now', '-1 day')
    """, (vertical,))
    total_runs_24h = count_rows[0]["n"] if count_rows else 0

    # Module status (latest run per module)
    modules_rows = safe_fetchall(conn, """
        SELECT module, status
        FROM collection_runs
        WHERE vertical = ? AND id IN (
            SELECT MAX(id) FROM collection_runs WHERE vertical = ? GROUP BY module
        )
    """, (vertical, vertical))
    modules = {r["module"]: r["status"] for r in modules_rows}

    return {
        "last_run": last_run,
        "total_runs_24h": total_runs_24h,
        "modules": modules,
    }


def get_kpis(conn: sqlite3.Connection, vertical: str) -> dict:
    """Key performance indicators for a vertical."""
    # Total observations + overall rate
    stats = safe_fetchall(conn, """
        SELECT COUNT(*) as total,
               SUM(CASE WHEN cited THEN 1 ELSE 0 END) as cited_count
        FROM citations
        WHERE vertical = ?
    """, (vertical,))

    total_obs = stats[0]["total"] if stats else 0
    cited_count = stats[0]["cited_count"] if stats else 0

    # Distinct entities monitored (from citation_context joined with citations)
    entities = safe_fetchall(conn, """
        SELECT COUNT(DISTINCT cc.entity) as n
        FROM citation_context cc
        JOIN citations c ON cc.citation_id = c.id
        WHERE c.vertical = ?
    """, (vertical,))
    # Fallback: count from verticals config table
    if not entities or entities[0]["n"] == 0:
        entities = safe_fetchall(conn, """
            SELECT json_array_length(cohort_json) as n FROM verticals WHERE slug = ?
        """, (vertical,))
    entities_monitored = entities[0]["n"] if entities else 0

    # Days collecting
    days = safe_fetchall(conn, """
        SELECT COUNT(DISTINCT date(timestamp)) as n
        FROM collection_runs
        WHERE vertical = ? AND status = 'success'
    """, (vertical,))
    days_collecting = days[0]["n"] if days else 0

    return {
        "total_observations": total_obs,
        "overall_rate": round(cited_count / max(total_obs, 1), 4),
        "entities_monitored": entities_monitored,
        "days_collecting": days_collecting,
    }


def get_finops_data(conn: sqlite3.Connection) -> dict:
    """FinOps summary from finops tables."""
    try:
        # Try reading from finops_usage table
        rows = safe_fetchall(conn, """
            SELECT platform, monthly_spend, monthly_limit, daily_spend, daily_limit,
                   queries_today, tokens_today
            FROM finops_usage
        """)

        if not rows:
            return {"budget_monthly": 0, "spent_monthly": 0, "pct_used": 0, "by_platform": {}}

        total_budget = sum(r.get("monthly_limit", 0) or 0 for r in rows)
        total_spent = sum(r.get("monthly_spend", 0) or 0 for r in rows)

        by_platform = {}
        for r in rows:
            by_platform[r["platform"]] = {
                "monthly_spend": r.get("monthly_spend", 0),
                "monthly_limit": r.get("monthly_limit", 0),
                "daily_spend": r.get("daily_spend", 0),
                "daily_limit": r.get("daily_limit", 0),
                "queries_today": r.get("queries_today", 0),
                "tokens_today": r.get("tokens_today", 0),
            }

        return {
            "budget_monthly": round(total_budget, 2),
            "spent_monthly": round(total_spent, 4),
            "pct_used": round(total_spent / max(total_budget, 0.001) * 100, 1),
            "by_platform": by_platform,
        }
    except Exception as e:
        print(f"  [WARN] FinOps query falhou: {e}")
        return {"budget_monthly": 0, "spent_monthly": 0, "pct_used": 0, "by_platform": {}}


# ---------------------------------------------------------------------------
# Supabase REST upsert
# ---------------------------------------------------------------------------

def upsert(client: httpx.Client, table: str, payload: list[dict] | dict) -> bool:
    """Upsert data to a Supabase table via REST API."""
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    data = payload if isinstance(payload, list) else [payload]

    try:
        resp = client.post(url, json=data, headers=HEADERS)
        if resp.status_code in (200, 201):
            print(f"  [OK] {table}: {resp.status_code}")
            return True
        else:
            print(f"  [ERRO] {table}: {resp.status_code} — {resp.text[:200]}")
            return False
    except Exception as e:
        print(f"  [ERRO] {table}: {e}")
        return False


# ---------------------------------------------------------------------------
# Main sync
# ---------------------------------------------------------------------------

def main() -> int:
    """Run full sync from SQLite to Supabase."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("[SKIP] SUPABASE_URL ou SUPABASE_KEY não configuradas. Sync ignorado.")
        return 0

    print(f"=== Sync Papers -> Supabase ===")
    print(f"  DB: {DB_PATH}")
    print(f"  Supabase: {SUPABASE_URL}")
    print(f"  Verticais: {', '.join(VERTICALS)}")
    print()

    conn = get_conn()
    now = datetime.now(timezone.utc).isoformat()
    errors = 0

    with httpx.Client(timeout=30) as client:
        # ----- Dashboard data per vertical -----
        dashboard_rows = []
        for v in VERTICALS:
            print(f"[{v}] Agregando dados...")
            row = {
                "vertical": v,
                "citation_rates": get_citation_rates(conn, v),
                "entity_rankings": get_entity_rankings(conn, v),
                "timeseries": get_timeseries(conn, v),
                "collection_status": get_collection_status(conn, v),
                "kpis": get_kpis(conn, v),
                "updated_at": now,
            }
            cr_count = len(row["citation_rates"])
            er_count = len(row["entity_rankings"])
            ts_count = len(row["timeseries"])
            obs = row["kpis"].get("total_observations", 0)
            print(f"  LLMs: {cr_count} | Entidades: {er_count} | Timeseries: {ts_count} pts | Obs: {obs}")
            dashboard_rows.append(row)

        print()
        print("Enviando papers_dashboard_data...")
        if not upsert(client, "papers_dashboard_data", dashboard_rows):
            errors += 1

        # ----- FinOps -----
        print()
        print("Agregando FinOps...")
        finops = get_finops_data(conn)
        finops["id"] = "global"
        finops["updated_at"] = now
        print(f"  Orçamento: ${finops['budget_monthly']:.2f} | Gasto: ${finops['spent_monthly']:.4f} | Uso: {finops['pct_used']:.1f}%")

        print("Enviando papers_finops...")
        if not upsert(client, "papers_finops", finops):
            errors += 1

    conn.close()

    print()
    if errors:
        print(f"=== Sync concluído com {errors} erro(s) ===")
        return 1
    else:
        print("=== Sync concluído com sucesso ===")
        return 0


if __name__ == "__main__":
    sys.exit(main())
