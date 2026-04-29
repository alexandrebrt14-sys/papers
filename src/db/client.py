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
        """Apply SQL schema from file, with incremental migration for vertical column."""
        if not SCHEMA_PATH.exists():
            raise FileNotFoundError(f"Schema not found: {SCHEMA_PATH}")
        # First, migrate existing tables to add vertical column if missing
        self._migrate_add_vertical()
        schema = SCHEMA_PATH.read_text(encoding="utf-8")
        self._conn.executescript(schema)
        self._conn.commit()

    def _migrate_add_vertical(self) -> None:
        """Add vertical column to existing tables if not present."""
        tables_needing_vertical = [
            "citations", "competitor_citations", "serp_ai_overlap",
            "daily_snapshots", "collection_runs", "dual_responses",
            "finops_usage", "finops_daily_rollup",
        ]
        for table in tables_needing_vertical:
            try:
                cols = [r[1] for r in self._conn.execute(f"PRAGMA table_info({table})").fetchall()]
                if cols and "vertical" not in cols:
                    default = "'fintech'"
                    self._conn.execute(f"ALTER TABLE {table} ADD COLUMN vertical TEXT NOT NULL DEFAULT {default}")
                    logger.info(f"Migração: coluna 'vertical' adicionada a {table}")
            except sqlite3.OperationalError as exc:
                if "no such table" in str(exc) or "duplicate column" in str(exc):
                    pass  # Table doesn't exist yet (schema will create it) or column already exists
                else:
                    logger.warning(f"Migracao falhou para {table}: {exc}")
                    raise
        self._conn.commit()
        # Migracoes adicionais (ortogonais)
        self._migrate_add_model_version()
        self._migrate_add_query_type()
        self._migrate_add_fictional_columns()
        self._migrate_snapshot_composite_unique()

    def _migrate_add_query_type(self) -> None:
        """Adiciona citations.query_type (Migration 0003 inline).

        Permite que DBs criados em máquinas que não rodaram a migration
        standalone continuem funcionando. Idempotente.
        """
        try:
            cols = [r[1] for r in self._conn.execute("PRAGMA table_info(citations)").fetchall()]
            if cols and "query_type" not in cols:
                self._conn.execute(
                    "ALTER TABLE citations ADD COLUMN query_type TEXT DEFAULT 'exploratory'"
                )
                logger.info("Migracao: coluna 'query_type' adicionada a citations")
                self._conn.commit()
        except Exception as exc:
            logger.debug("query_type migration skipped: %s", exc)

    def _migrate_snapshot_composite_unique(self) -> None:
        """daily_snapshots: UNIQUE(date) → UNIQUE(date, module, vertical).

        Bug histórico (2026-04-29 health-check):
            schema antigo tinha `UNIQUE(date)`. Cada INSERT OR REPLACE com a
            mesma date sobrescrevia a anterior, deixando só 1 row/dia (a
            última vertical do loop). Snapshots por vertical não persistiam.
        Idempotente: detecta UNIQUE composto antes de aplicar.
        """
        try:
            sql = self._conn.execute(
                "SELECT sql FROM sqlite_master WHERE type='table' AND name='daily_snapshots'"
            ).fetchone()
            schema = (sql[0] if sql else "") or ""
            if (
                "UNIQUE(date, module, vertical)" in schema
                or "UNIQUE (date, module, vertical)" in schema
            ):
                return
            from src.db import migrate_0008_snapshot_composite_unique
            migrate_0008_snapshot_composite_unique.apply(self._conn)
            logger.info("Migracao 0008 aplicada: daily_snapshots UNIQUE composto")
        except Exception as exc:
            logger.debug("snapshot composite migration skipped: %s", exc)

    def _migrate_add_fictional_columns(self) -> None:
        """Adiciona citations.fictional_hit + fictional_names_json (Migration 0004 inline).

        Garante que DBs fora do fluxo standalone de migrations também tenham
        as colunas de calibração de false-positive. Idempotente.
        """
        try:
            cols = [r[1] for r in self._conn.execute("PRAGMA table_info(citations)").fetchall()]
            if cols and "fictional_hit" not in cols:
                self._conn.execute(
                    "ALTER TABLE citations ADD COLUMN fictional_hit INTEGER NOT NULL DEFAULT 0"
                )
                logger.info("Migracao: coluna 'fictional_hit' adicionada a citations")
            if cols and "fictional_names_json" not in cols:
                self._conn.execute(
                    "ALTER TABLE citations ADD COLUMN fictional_names_json TEXT NOT NULL DEFAULT '[]'"
                )
                logger.info("Migracao: coluna 'fictional_names_json' adicionada a citations")
            self._conn.commit()
        except Exception as exc:
            logger.debug("fictional_* migration skipped: %s", exc)

    def _migrate_add_model_version(self) -> None:
        """Add model_version column to citations for non-stationarity tracking.

        Modelos LLM mudam silenciosamente: 'gpt-4o-mini' em janeiro nao e o
        mesmo de junho. Para painel longitudinal valido, precisamos rastrear
        a versao exata do modelo no momento da coleta. NULL e aceitavel para
        registros legacy. Novos inserts devem popular esta coluna.
        """
        try:
            cols = [r[1] for r in self._conn.execute("PRAGMA table_info(citations)").fetchall()]
            if cols and "model_version" not in cols:
                self._conn.execute(
                    "ALTER TABLE citations ADD COLUMN model_version TEXT DEFAULT NULL"
                )
                logger.info("Migracao: coluna 'model_version' adicionada a citations")
                self._conn.commit()
        except Exception as exc:
            logger.debug("model_version migration skipped: %s", exc)

    def close(self) -> None:
        if self._conn:
            self._conn.close()
            self._conn = None

    # === Insert methods ===

    def insert_citations(self, records: list[dict[str, Any]], vertical: str = "fintech") -> int:
        """Insert citation tracker records.

        Populates columns added pelas migrations:
            - Migration 0003: query_type (directive/exploratory)
            - Migration 0004: fictional_hit + fictional_names_json (false-positive)
            - Migration 0005: cited_v2, cited_entities_v2_json, position_v2, ... (NER v2)
            - Migration 0006: response_hash (drift detection)
            - Migration 0007: is_probe, probe_type, adversarial_framing,
              fictitious_target, is_calibration (probe design)

        Registros que não tragam essas chaves recebem defaults seguros para
        preservar compat com coletores ainda não atualizados (v1 legacy).
        """
        sql = """
            INSERT INTO citations (
                timestamp, llm, model, query, query_category, query_lang,
                query_type,
                vertical, cited, cited_entity, cited_domain, cited_person,
                position, attribution, source_count, our_source_count,
                hedging_detected, response_length, response_text,
                sources_json, latency_ms, token_count, model_version,
                fictional_hit, fictional_names_json,
                -- Migration 0005 (NER v2)
                cited_v2, cited_count_v2, cited_entities_v2_json,
                first_entity_v2, first_entity_offset_v2, position_v2,
                via_alias_count_v2, via_fold_count_v2,
                response_length_chars_v2, extraction_version, extracted_at_v2,
                -- Migration 0006 (drift)
                response_hash,
                -- Migration 0007 (probe design)
                is_probe, probe_type, adversarial_framing,
                fictitious_target, is_calibration
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                      ?, ?,
                      ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                      ?,
                      ?, ?, ?, ?, ?)
        """
        rows = []
        for r in records:
            fict_names = r.get("fictional_names", []) or []
            rows.append((
                r["timestamp"], r["llm"], r["model"], r["query"],
                r["query_category"], r["query_lang"],
                r.get("query_type", "exploratory"),
                r.get("vertical", vertical),
                r["cited"], r.get("cited_entity"), r.get("cited_domain"),
                r.get("cited_person"), r.get("position"), r.get("attribution"),
                r.get("source_count"), r.get("our_source_count"),
                r.get("hedging_detected"), r.get("response_length"),
                r.get("response_text"), json.dumps(r.get("all_sources", [])),
                r.get("latency_ms"), r.get("token_count"),
                # model_version: rastreio de non-stationarity. Fallback = model.
                r.get("model_version") or r.get("model"),
                # Migration 0004: calibração de false-positive
                1 if r.get("fictional_hit") else 0,
                json.dumps(fict_names, ensure_ascii=False),
                # Migration 0005: NER v2 columns
                r.get("cited_v2"),
                r.get("cited_count_v2"),
                r.get("cited_entities_v2_json"),
                r.get("first_entity_v2"),
                r.get("first_entity_offset_v2"),
                r.get("position_v2"),
                r.get("via_alias_count_v2", 0),
                r.get("via_fold_count_v2", 0),
                r.get("response_length_chars_v2"),
                r.get("extraction_version", "v1"),
                r.get("extracted_at_v2"),
                # Migration 0006: drift detection
                r.get("response_hash"),
                # Migration 0007: probe design
                r.get("is_probe", 0) or 0,
                r.get("probe_type"),
                r.get("adversarial_framing", 0) or 0,
                r.get("fictitious_target"),
                r.get("is_calibration", 0) or 0,
            ))
        self._conn.executemany(sql, rows)
        self._conn.commit()
        return len(rows)

    def insert_competitor_citations(self, records: list[dict[str, Any]], vertical: str = "fintech") -> int:
        """Insert competitor benchmark records."""
        sql = """
            INSERT INTO competitor_citations (
                timestamp, llm, model, query, query_category, query_lang,
                vertical, entity, entity_type, cited, position, response_length
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        rows = []
        for r in records:
            rows.append((
                r["timestamp"], r["llm"], r["model"], r["query"],
                r["query_category"], r["query_lang"],
                r.get("vertical", vertical),
                r["entity"], r["entity_type"], r["cited"],
                r.get("position"), r.get("response_length"),
            ))
        self._conn.executemany(sql, rows)
        self._conn.commit()
        return len(rows)

    def insert_serp_overlap(self, records: list[dict[str, Any]], vertical: str = "fintech") -> int:
        """Insert SERP vs AI overlap records."""
        sql = """
            INSERT INTO serp_ai_overlap (
                timestamp, llm, model, query, query_category,
                vertical,
                serp_domain_count, ai_domain_count, overlap_count, overlap_pct,
                serp_only_count, ai_only_count,
                overlap_domains, serp_only_domains, ai_only_domains,
                primary_in_serp, primary_in_ai
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        rows = []
        for r in records:
            rows.append((
                r["timestamp"], r["llm"], r["model"], r["query"], r["query_category"],
                r.get("vertical", vertical),
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
        error_msg: str | None = None, vertical: str = "fintech",
    ) -> None:
        """Record a collection run in metadata."""
        self._conn.execute(
            """INSERT INTO collection_runs (timestamp, module, vertical, records, duration_ms, status, error_msg)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (datetime.now(timezone.utc).isoformat(), module, vertical, records, duration_ms, status, error_msg),
        )
        self._conn.commit()

    def save_daily_snapshot(self, module: str, data: dict[str, Any], vertical: str = "fintech") -> None:
        """Save or update a daily snapshot."""
        date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        self._conn.execute(
            """INSERT OR REPLACE INTO daily_snapshots (date, module, vertical, data_json)
               VALUES (?, ?, ?, ?)""",
            (date, module, vertical, json.dumps(data, ensure_ascii=False)),
        )
        self._conn.commit()

    def insert_citation_context(self, citation_id: int, result: dict[str, Any]) -> None:
        """Insert a citation context analysis result."""
        sql = """
            INSERT INTO citation_context (
                citation_id, entity, sentiment, attribution,
                factual_accuracy_json, position_tercile, hedging,
                hedging_phrases, context_window, sentiment_signals
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        self._conn.execute(sql, (
            citation_id,
            result["entity"],
            result.get("sentiment"),
            result.get("attribution"),
            json.dumps(result.get("factual_accuracy"), ensure_ascii=False) if result.get("factual_accuracy") else None,
            result.get("position_tercile"),
            result.get("hedging", False),
            json.dumps(result.get("hedging_phrases", []), ensure_ascii=False),
            result.get("context_window"),
            json.dumps(result.get("sentiment_signals", []), ensure_ascii=False),
        ))
        self._conn.commit()

    def insert_intervention(self, record: dict[str, Any]) -> int:
        """Insert a new intervention record. Returns rowid."""
        sql = """
            INSERT INTO interventions (
                slug, intervention_type, description, url,
                queries_json, baseline_json, registered_at, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor = self._conn.execute(sql, (
            record["slug"],
            record["intervention_type"],
            record["description"],
            record["url"],
            json.dumps(record.get("queries", []), ensure_ascii=False),
            json.dumps(record.get("baseline_citations", {}), ensure_ascii=False),
            record.get("registered_at", datetime.now(timezone.utc).isoformat()),
            record.get("status", "active"),
        ))
        self._conn.commit()
        return cursor.lastrowid

    def insert_intervention_measurement(self, record: dict[str, Any]) -> int:
        """Insert an intervention measurement. Returns rowid."""
        sql = """
            INSERT INTO intervention_measurements (
                intervention_slug, timestamp, days_since_intervention,
                citations_json, citation_rate, delta_from_baseline, details_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        cursor = self._conn.execute(sql, (
            record["intervention_slug"],
            record.get("timestamp", datetime.now(timezone.utc).isoformat()),
            record["days_since_intervention"],
            json.dumps(record.get("citations_by_llm", {}), ensure_ascii=False),
            record.get("citation_rate"),
            record.get("delta_from_baseline"),
            json.dumps(record.get("details", {}), ensure_ascii=False),
        ))
        self._conn.commit()
        return cursor.lastrowid

    def get_active_interventions(self) -> list[dict[str, Any]]:
        """Return all active interventions."""
        rows = self._conn.execute(
            "SELECT * FROM interventions WHERE status = 'active'"
        ).fetchall()
        return [dict(r) for r in rows]

    def get_intervention_measurements(self, slug: str) -> list[dict[str, Any]]:
        """Return all measurements for an intervention."""
        rows = self._conn.execute(
            "SELECT * FROM intervention_measurements WHERE intervention_slug = ? ORDER BY days_since_intervention",
            (slug,),
        ).fetchall()
        return [dict(r) for r in rows]

    # === Query methods ===

    def get_citation_rate(
        self, llm: str | None = None, days: int = 30, vertical: str | None = None,
    ) -> dict[str, float]:
        """Get citation rate by LLM for the last N days, optionally filtered by vertical."""
        where = "WHERE timestamp >= datetime('now', ?)"
        params: list[Any] = [f"-{days} days"]
        if llm:
            where += " AND llm = ?"
            params.append(llm)
        if vertical:
            where += " AND vertical = ?"
            params.append(vertical)

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

    def get_collection_history(self, module: str | None = None, limit: int = 20, vertical: str | None = None) -> list[dict]:
        """Get recent collection run history."""
        conditions = []
        params: list[Any] = []
        if module:
            conditions.append("module = ?")
            params.append(module)
        if vertical:
            conditions.append("vertical = ?")
            params.append(vertical)
        where = ("WHERE " + " AND ".join(conditions)) if conditions else ""
        rows = self._conn.execute(
            f"""SELECT * FROM collection_runs {where}
                ORDER BY timestamp DESC LIMIT ?""",
            params + [limit],
        ).fetchall()
        return [dict(r) for r in rows]

    def export_citations_csv(self, output_path: str, vertical: str | None = None) -> int:
        """Export citations to CSV, optionally filtered by vertical."""
        import csv
        where = "WHERE vertical = ?" if vertical else ""
        params = [vertical] if vertical else []
        rows = self._conn.execute(
            f"SELECT * FROM citations {where} ORDER BY timestamp", params
        ).fetchall()
        if not rows:
            return 0
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            for row in rows:
                writer.writerow(dict(row))
        return len(rows)
