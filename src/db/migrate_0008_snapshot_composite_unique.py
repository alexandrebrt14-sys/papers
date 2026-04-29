"""migrate_0008 — daily_snapshots UNIQUE composto (date, module, vertical).

Bug histórico (2026-04-29 health-check):
    schema antigo tinha `date TEXT NOT NULL UNIQUE`. Cada INSERT OR REPLACE
    com a mesma date sobrescrevia a anterior, então só sobrevivia 1 row por
    dia (a última vertical processada no loop). Resultado: snapshots
    longitudinais por vertical impossíveis. Backfill confirmou: 4 verticais
    × 7 dias = 28 snapshots intentados → apenas 7 rows persistiram.

Esta migration:
  1. Cria daily_snapshots_v2 com UNIQUE (date, module, vertical)
  2. Migra dados existentes (preserva vertical='fintech' default e os 7 já
     gravados). NÃO tenta reconstruir os 21 snapshots perdidos — backfill
     deve ser rerodado depois.
  3. DROP antiga, RENAME nova.
  4. Idempotente: detecta se schema já tem composite unique.
"""
from __future__ import annotations

import sqlite3


def _has_composite_unique(conn: sqlite3.Connection) -> bool:
    sql = conn.execute(
        "SELECT sql FROM sqlite_master WHERE type='table' AND name='daily_snapshots'"
    ).fetchone()
    if not sql:
        return False
    schema = sql[0] or ""
    # heurística: a versão nova define UNIQUE(date, module, vertical) explícito
    return "UNIQUE(date, module, vertical)" in schema or "UNIQUE (date, module, vertical)" in schema


def apply(conn: sqlite3.Connection) -> None:
    if _has_composite_unique(conn):
        return
    cur = conn.cursor()
    cur.executescript(
        """
        BEGIN;

        CREATE TABLE IF NOT EXISTS daily_snapshots_v2 (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            date        TEXT NOT NULL,
            module      TEXT NOT NULL,
            vertical    TEXT NOT NULL DEFAULT 'fintech',
            data_json   TEXT NOT NULL,
            created_at  TEXT DEFAULT (datetime('now')),
            UNIQUE(date, module, vertical)
        );

        INSERT OR IGNORE INTO daily_snapshots_v2
              (id, date, module, vertical, data_json, created_at)
        SELECT id, date, module, COALESCE(vertical, 'fintech'), data_json, created_at
          FROM daily_snapshots;

        DROP TABLE daily_snapshots;
        ALTER TABLE daily_snapshots_v2 RENAME TO daily_snapshots;

        COMMIT;
        """
    )
