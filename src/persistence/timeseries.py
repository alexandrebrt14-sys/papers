"""Module 5: Time Series Persistence.

Manages longitudinal data storage with daily, per-event, and weekly granularity.
Target: 6+ months of continuous data for statistical analysis.
Supports SQLite (local) with Supabase sync for durability.
Multi-vertical aware: snapshots and aggregates are scoped per vertical.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone, timedelta
from typing import Any

from src.db.client import DatabaseClient

logger = logging.getLogger(__name__)


class TimeSeriesManager:
    """Manage time series data across collection modules."""

    def __init__(self, db: DatabaseClient) -> None:
        self.db = db

    def save_daily_aggregate(self, module: str, data: dict[str, Any], vertical: str = "fintech") -> None:
        """Save a daily aggregate snapshot for a module and vertical."""
        self.db.save_daily_snapshot(module, {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "vertical": vertical,
            "data": data,
        }, vertical=vertical)
        logger.info(f"Snapshot diário salvo: {module} ({vertical})")

    def get_time_series(
        self, module: str, days: int = 90, vertical: str | None = None,
    ) -> list[dict[str, Any]]:
        """Retrieve time series data for analysis, optionally filtered by vertical."""
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d")
        if vertical:
            rows = self.db._conn.execute(
                """SELECT date, data_json FROM daily_snapshots
                   WHERE module = ? AND date >= ? AND vertical = ?
                   ORDER BY date ASC""",
                (module, cutoff, vertical),
            ).fetchall()
        else:
            rows = self.db._conn.execute(
                """SELECT date, data_json FROM daily_snapshots
                   WHERE module = ? AND date >= ?
                   ORDER BY date ASC""",
                (module, cutoff),
            ).fetchall()
        return [{"date": r["date"], **json.loads(r["data_json"])} for r in rows]

    def compute_daily_citation_aggregate(self, vertical: str | None = None) -> dict[str, Any]:
        """Compute today's citation aggregate from raw data, optionally filtered by vertical."""
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        where = "WHERE date(timestamp) = ?"
        params: list[Any] = [today]
        if vertical:
            where += " AND vertical = ?"
            params.append(vertical)

        rows = self.db._conn.execute(
            f"""SELECT llm,
                      COUNT(*) as queries,
                      SUM(CASE WHEN cited THEN 1 ELSE 0 END) as cited,
                      AVG(CASE WHEN cited THEN 1.0 ELSE 0.0 END) as rate,
                      AVG(response_length) as avg_response_length,
                      AVG(latency_ms) as avg_latency
               FROM citations
               {where}
               GROUP BY llm""",
            params,
        ).fetchall()

        by_llm = {}
        total_queries = 0
        total_cited = 0
        for r in rows:
            by_llm[r["llm"]] = {
                "queries": r["queries"],
                "cited": r["cited"],
                "rate": round(r["rate"], 3),
                "avg_response_length": round(r["avg_response_length"] or 0),
                "avg_latency_ms": round(r["avg_latency"] or 0),
            }
            total_queries += r["queries"]
            total_cited += r["cited"]

        return {
            "date": today,
            "vertical": vertical or "all",
            "total_queries": total_queries,
            "total_cited": total_cited,
            "overall_rate": round(total_cited / max(total_queries, 1), 3),
            "by_llm": by_llm,
        }

    def get_data_health(self) -> dict[str, Any]:
        """Check data completeness and health, including vertical breakdown."""
        runs = self.db._conn.execute(
            """SELECT module, vertical, COUNT(*) as runs, MIN(timestamp) as first, MAX(timestamp) as last
               FROM collection_runs WHERE status = 'success'
               GROUP BY module, vertical"""
        ).fetchall()

        snapshots = self.db._conn.execute(
            """SELECT module, vertical, COUNT(*) as days, MIN(date) as first, MAX(date) as last
               FROM daily_snapshots GROUP BY module, vertical"""
        ).fetchall()

        total_citations = self.db._conn.execute(
            "SELECT COUNT(*) as n FROM citations"
        ).fetchone()

        citations_by_vertical = self.db._conn.execute(
            "SELECT vertical, COUNT(*) as n FROM citations GROUP BY vertical"
        ).fetchall()

        return {
            "collection_runs": [dict(r) for r in runs],
            "daily_snapshots": [dict(r) for r in snapshots],
            "total_citation_records": total_citations["n"],
            "citations_by_vertical": {r["vertical"]: r["n"] for r in citations_by_vertical},
            "checked_at": datetime.now(timezone.utc).isoformat(),
        }
