"""Database client with SQLite (local) and Supabase (production) support."""

from __future__ import annotations

import json
import logging
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.config import config, BASE_DIR

logger = logging.getLogger(__name__)

SCHEMA_PATH = BASE_DIR / "src" / "db" / "schema.sql"


class DatabaseClient:
    """Unified database client for persisting collection results."""

    def __init__(self, db_path: str | None = None) -> None:
        self.db_path = db_path or config.db_path
        self._conn: sqlite3.Connection | None = None

    def connect(self) -> None:
        """Initialize database connection and apply schema."""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(self.db_path)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute("PRAGMA foreign_keys=ON")
        self._apply_schema()
        logger.info(f"Conectado ao banco: {self.db_path}")

    def _apply_schema(self) -> None:
        """Apply SQL schema from file."""
        if not SCHEMA_PATH.exists():
            raise FileNotFoundError(f"Schema not found: {SCHEMA_PATH}")
        schema = SCHEMA_PATH.read_text(encoding="utf-8")
        self._conn.executescript(schema)
        self._conn.commit()

    def close(self) -> None:
        if self._conn:
            self._conn.close()
            self._conn = None

    # === Insert methods ===

    def insert_citations(self, records: list[dict[str, Any]]) -> int:
        """Insert citation tracker records."""
        sql = """
            INSERT INTO citations (
                timestamp, llm, model, query, query_category, query_lang,
                cited, cited_entity, cited_domain, cited_person,
                position, attribution, source_count, our_source_count,
                hedging_detected, response_length, response_text,
                sources_json, latency_ms, token_count
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        rows = []
        for r in records:
            rows.append((
                r["timestamp"], r["llm"], r["model"], r["query"],
                r["query_category"], r["query_lang"],
                r["cited"], r.get("cited_entity"), r.get("cited_domain"),
                r.get("cited_person"), r.get("position"), r.get("attribution"),
                r.get("source_count"), r.get("our_source_count"),
                r.get("hedging_detected"), r.get("response_length"),
                r.get("response_text"), json.dumps(r.get("all_sources", [])),
                r.get("latency_ms"), r.get("token_count"),
            ))
        self._conn.executemany(sql, rows)
        self._conn.commit()
        return len(rows)

    def insert_competitor_citations(self, records: list[dict[str, Any]]) -> int:
        """Insert competitor benchmark records."""
        sql = """
            INSERT INTO competitor_citations (
                timestamp, llm, model, query, query_category, query_lang,
                entity, entity_type, cited, position, response_length
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        rows = []
        for r in records:
            rows.append((
                r["timestamp"], r["llm"], r["model"], r["query"],
                r["query_category"], r["query_lang"],
                r["entity"], r["entity_type"], r["cited"],
                r.get("position"), r.get("response_length"),
            ))
        self._conn.executemany(sql, rows)
        self._conn.commit()
        return len(rows)

    def insert_serp_overlap(self, records: list[dict[str, Any]]) -> int:
        """Insert SERP vs AI overlap records."""
        sql = """
            INSERT INTO serp_ai_overlap (
                timestamp, llm, model, query, query_category,
                serp_domain_count, ai_domain_count, overlap_count, overlap_pct,
                serp_only_count, ai_only_count,
                overlap_domains, serp_only_domains, ai_only_domains,
                primary_in_serp, primary_in_ai
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        rows = []
        for r in records:
            rows.append((
                r["timestamp"], r["llm"], r["model"], r["query"], r["query_category"],
                r["serp_domain_count"], r["ai_domain_count"],
                r["overlap_count"], r["overlap_pct"],
                r["serp_only_count"], r["ai_only_count"],
                json.dumps(r["overlap_domains"]),
                json.dumps(r["serp_only_domains"]),
                json.dumps(r["ai_only_domains"]),
                r["primary_in_serp"], r["primary_in_ai"],
            ))
        self._conn.executemany(sql, rows)
        self._conn.commit()
        return len(rows)

    def insert_collection_run(
        self, module: str, records: int, duration_ms: int, status: str = "success",
        error_msg: str | None = None,
    ) -> None:
        """Record a collection run in metadata."""
        self._conn.execute(
            """INSERT INTO collection_runs (timestamp, module, records, duration_ms, status, error_msg)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (datetime.now(timezone.utc).isoformat(), module, records, duration_ms, status, error_msg),
        )
        self._conn.commit()

    def save_daily_snapshot(self, module: str, data: dict[str, Any]) -> None:
        """Save or update a daily snapshot."""
        date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        self._conn.execute(
            """INSERT OR REPLACE INTO daily_snapshots (date, module, data_json)
               VALUES (?, ?, ?)""",
            (date, module, json.dumps(data, ensure_ascii=False)),
        )
        self._conn.commit()

    # === Query methods ===

    def get_citation_rate(
        self, llm: str | None = None, days: int = 30
    ) -> dict[str, float]:
        """Get citation rate by LLM for the last N days."""
        where = "WHERE timestamp >= datetime('now', ?)"
        params: list[Any] = [f"-{days} days"]
        if llm:
            where += " AND llm = ?"
            params.append(llm)

        rows = self._conn.execute(
            f"""SELECT llm,
                       COUNT(*) as total,
                       SUM(CASE WHEN cited THEN 1 ELSE 0 END) as cited_count
                FROM citations {where}
                GROUP BY llm""",
            params,
        ).fetchall()

        return {
            row["llm"]: round(row["cited_count"] / max(row["total"], 1), 3)
            for row in rows
        }

    def get_collection_history(self, module: str | None = None, limit: int = 20) -> list[dict]:
        """Get recent collection run history."""
        where = "WHERE module = ?" if module else ""
        params = [module] if module else []
        rows = self._conn.execute(
            f"""SELECT * FROM collection_runs {where}
                ORDER BY timestamp DESC LIMIT ?""",
            params + [limit],
        ).fetchall()
        return [dict(r) for r in rows]

    def export_citations_csv(self, output_path: str) -> int:
        """Export all citations to CSV."""
        import csv
        rows = self._conn.execute("SELECT * FROM citations ORDER BY timestamp").fetchall()
        if not rows:
            return 0
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            for row in rows:
                writer.writerow(dict(row))
        return len(rows)
