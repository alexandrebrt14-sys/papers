"""Migration 0006 — response_hash column.

Adiciona `response_hash` (SHA-256 do response_text) em `citations`.
Motivação (gap E3 Agent E audit 2026-04-23):

1. Detecção de cache hits — respostas idênticas bit-a-bit para
   (query, llm, model_version) sugerem cache/determinism vs geração real.
2. Drift detection — quando provider silenciosamente atualiza o modelo
   backend, respostas começam a divergir para mesmo input; hash permite
   comparar distributions temporais.
3. Replicabilidade — inclui hash no manifest do dataset Zenodo para
   verificação externa ("este é o mesmo dataset que o paper v2 usou").

Forward-only. Backfill opcional via scripts/backfill_response_hash.py.
"""
from __future__ import annotations

import hashlib
import logging
import sqlite3

logger = logging.getLogger(__name__)


def apply(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()
    existing = {r[1] for r in cur.execute("PRAGMA table_info(citations)").fetchall()}

    added = []
    if "response_hash" not in existing:
        cur.execute(
            "ALTER TABLE citations ADD COLUMN response_hash TEXT"
        )
        added.append("response_hash")

    cur.execute(
        "CREATE INDEX IF NOT EXISTS idx_citations_response_hash "
        "ON citations(response_hash)"
    )
    cur.execute(
        "CREATE INDEX IF NOT EXISTS idx_citations_llm_model_hash "
        "ON citations(llm, model_version, response_hash)"
    )

    conn.commit()
    logger.info("migrate_0006_response_hash: added %d cols: %s", len(added), added)
    return added


def compute_hash(text: str) -> str:
    """Retorna SHA-256 hex dos primeiros 16 chars para armazenamento compacto."""
    if not text:
        return ""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def backfill(conn: sqlite3.Connection, limit: int | None = None) -> int:
    """Popula response_hash para rows existentes onde está NULL."""
    conn.row_factory = sqlite3.Row
    where = "WHERE response_hash IS NULL AND response_text IS NOT NULL"
    sql = f"SELECT id, response_text FROM citations {where}"
    if limit:
        sql += f" LIMIT {limit}"

    rows = conn.execute(sql).fetchall()
    count = 0
    for row in rows:
        h = compute_hash(row["response_text"])
        conn.execute(
            "UPDATE citations SET response_hash = ? WHERE id = ?",
            (h, row["id"]),
        )
        count += 1
    conn.commit()
    logger.info("backfill response_hash: %d rows updated", count)
    return count
