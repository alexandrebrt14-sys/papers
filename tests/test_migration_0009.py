"""Regression tests for Migration 0009 — Citation Selection vs Absorption columns.

Garante que:
  1. Um DB fresco criado pelo schema.sql já contém as 6 colunas novas.
  2. Um DB legacy (sem as colunas) é migrado via ALTER pela cadeia inline.
  3. A migration standalone é idempotente (2a aplicação adiciona 0 colunas).
  4. O enum FAILURE_TYPES tem os 7 tipos da taxonomia arXiv:2603.09296.
"""
from __future__ import annotations

import sqlite3

from src.db import migrate_0009_citation_absorption as m
from src.db.client import DatabaseClient

_CITATIONS_NEW = {"selection_status", "absorption_status", "failure_type"}
_SNAPSHOT_NEW = {"citation_selection_rate", "citation_absorption_rate", "semantic_entropy_drift"}


def _cols(conn: sqlite3.Connection, table: str) -> set[str]:
    return {r[1] for r in conn.execute(f"PRAGMA table_info({table})").fetchall()}


def test_fresh_db_has_0009_columns(tmp_path) -> None:
    db = DatabaseClient(str(tmp_path / "fresh.db"))
    db.connect()
    try:
        assert _CITATIONS_NEW <= _cols(db._conn, "citations")
        assert _SNAPSHOT_NEW <= _cols(db._conn, "daily_snapshots")
    finally:
        db.close()


def test_standalone_idempotent(tmp_path) -> None:
    db = DatabaseClient(str(tmp_path / "idem.db"))
    db.connect()
    try:
        # schema.sql já criou as colunas → standalone não deve adicionar nada
        assert m.apply(db._conn) == 0
    finally:
        db.close()


def test_legacy_table_is_altered(tmp_path) -> None:
    path = str(tmp_path / "legacy.db")
    # Tabela citations legacy mínima porém com as colunas que os índices do
    # schema referenciam, para o executescript não falhar.
    conn = sqlite3.connect(path)
    conn.executescript(
        """
        CREATE TABLE citations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT, llm TEXT, model TEXT, query TEXT,
            query_category TEXT, vertical TEXT DEFAULT 'fintech',
            cited BOOLEAN DEFAULT 0, model_version TEXT, query_type TEXT
        );
        """
    )
    conn.commit()
    conn.close()

    db = DatabaseClient(path)
    db.connect()
    try:
        assert _CITATIONS_NEW <= _cols(db._conn, "citations")
    finally:
        db.close()


def test_failure_type_enum_has_seven_types() -> None:
    assert len(m.FAILURE_TYPES) == 7
    assert "hallucinated-source" in m.FAILURE_TYPES
    assert "retrieval-miss" in m.FAILURE_TYPES
