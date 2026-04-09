"""Tests para scripts/sync_to_supabase.py — B-017.

Achado B-017 da auditoria de ecossistema 2026-04-08. O script
sync_to_supabase.py existia mas nunca havia sido testado. Estes
testes cobrem:

- Agregacoes SQL com banco em-memoria + fixtures
- Cliente Supabase mockado (sem rede real)
- Dry-run produz preview sem upload
- Skip quando credenciais ausentes (exit code 2)
- Erro de upsert eh propagado corretamente (exit code 1)
- Sentinela: PII nao vaza no payload agregado
"""

from __future__ import annotations

import os
import sqlite3
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

# Path setup
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))


@pytest.fixture(autouse=True)
def reset_modules():
    """Limpa imports cached entre testes."""
    yield
    # Garantir que o modulo eh recarregado em cada teste para pegar
    # mudancas de monkeypatch nas variaveis globais
    if "sync_to_supabase" in sys.modules:
        del sys.modules["sync_to_supabase"]


@pytest.fixture
def memory_db():
    """SQLite em memoria com schema minimo + dados sinteticos."""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript("""
        CREATE TABLE citations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            vertical TEXT NOT NULL,
            llm TEXT NOT NULL,
            model TEXT,
            cited INTEGER NOT NULL DEFAULT 0,
            position INTEGER,
            cited_entity TEXT
        );
        CREATE TABLE citation_context (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            citation_id INTEGER NOT NULL,
            entity TEXT NOT NULL,
            FOREIGN KEY (citation_id) REFERENCES citations(id)
        );
        CREATE TABLE collection_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            vertical TEXT NOT NULL,
            module TEXT NOT NULL,
            status TEXT NOT NULL
        );
        CREATE TABLE verticals (
            slug TEXT PRIMARY KEY,
            cohort_json TEXT
        );
        CREATE TABLE finops_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            platform TEXT NOT NULL,
            cost_usd REAL NOT NULL DEFAULT 0,
            total_tokens INTEGER NOT NULL DEFAULT 0
        );
        CREATE TABLE finops_budgets (
            platform TEXT PRIMARY KEY,
            monthly_limit_usd REAL,
            daily_limit_usd REAL
        );
    """)

    # Dados sinteticos
    conn.execute(
        "INSERT INTO verticals (slug, cohort_json) VALUES (?, ?)",
        ("fintech", '["Nubank","Itau","Bradesco"]'),
    )
    # 10 citacoes na vertical fintech (5 cited)
    for i in range(10):
        conn.execute(
            "INSERT INTO citations (timestamp, vertical, llm, model, cited, position, cited_entity) "
            "VALUES (datetime('now'), 'fintech', 'gpt-4o', 'openai', ?, ?, ?)",
            (1 if i < 5 else 0, i + 1 if i < 5 else None, "Nubank" if i < 5 else None),
        )
    conn.execute(
        "INSERT INTO collection_runs (timestamp, vertical, module, status) "
        "VALUES (datetime('now'), 'fintech', 'citation_tracker', 'success')"
    )
    conn.execute(
        "INSERT INTO finops_budgets (platform, monthly_limit_usd, daily_limit_usd) "
        "VALUES ('openai', 50.0, 5.0)"
    )
    conn.execute(
        "INSERT INTO finops_usage (timestamp, platform, cost_usd, total_tokens) "
        "VALUES (strftime('%Y-%m-01T12:00:00Z', 'now'), 'openai', 2.50, 50000)"
    )
    conn.commit()
    yield conn
    conn.close()


# ─── Smoke imports ─────────────────────────────────────────────────────────


def test_module_imports():
    import sync_to_supabase
    assert hasattr(sync_to_supabase, "run_sync")
    assert hasattr(sync_to_supabase, "VERTICALS")
    assert "fintech" in sync_to_supabase.VERTICALS


def test_constants_defined():
    import sync_to_supabase
    assert sync_to_supabase.TABLE_DASHBOARD == "papers_dashboard_data"
    assert sync_to_supabase.TABLE_FINOPS == "papers_finops"


# ─── Aggregations ──────────────────────────────────────────────────────────


def test_citation_rates_aggregation(memory_db):
    import sync_to_supabase as sync
    rows = sync._citation_rates(memory_db, "fintech")
    assert len(rows) >= 1
    row = rows[0]
    assert row["llm"] == "gpt-4o"
    assert row["total_queries"] == 10
    assert row["cited_count"] == 5
    assert row["citation_rate"] == 0.5


def test_citation_rates_empty_vertical(memory_db):
    import sync_to_supabase as sync
    rows = sync._citation_rates(memory_db, "saude")
    assert rows == []


def test_kpis_basic(memory_db):
    import sync_to_supabase as sync
    kpis = sync._kpis(memory_db, "fintech")
    assert kpis["total_observations"] == 10
    assert kpis["overall_rate"] == 0.5
    assert kpis["entities_monitored"] == 3  # ["Nubank","Itau","Bradesco"]
    assert kpis["days_collecting"] >= 1


def test_collection_status_includes_modules(memory_db):
    import sync_to_supabase as sync
    status = sync._collection_status(memory_db, "fintech")
    assert "citation_tracker" in status["modules"]
    assert status["modules"]["citation_tracker"] == "success"
    assert status["last_run"] is not None


def test_finops_data_aggregation(memory_db):
    import sync_to_supabase as sync
    finops = sync._finops_data(memory_db)
    assert finops["budget_monthly"] == 50.0
    assert finops["spent_monthly"] >= 0
    assert "openai" in finops["by_platform"]
    assert finops["by_platform"]["openai"]["monthly_limit"] == 50.0


def test_finops_data_no_budgets():
    import sync_to_supabase as sync
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript("""
        CREATE TABLE finops_budgets (platform TEXT PRIMARY KEY,
                                      monthly_limit_usd REAL, daily_limit_usd REAL);
        CREATE TABLE finops_usage (id INTEGER PRIMARY KEY,
                                    timestamp TEXT, platform TEXT,
                                    cost_usd REAL, total_tokens INTEGER);
    """)
    finops = sync._finops_data(conn)
    assert finops["budget_monthly"] == 0
    assert finops["spent_monthly"] == 0
    assert finops["by_platform"] == {}
    conn.close()


# ─── Skip behavior ─────────────────────────────────────────────────────────


def test_run_sync_skips_without_credentials(monkeypatch, tmp_path):
    """Sem SUPABASE_URL/SUPABASE_KEY, run_sync retorna 2 (skip)."""
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.delenv("SUPABASE_KEY", raising=False)
    db_file = tmp_path / "ghost.db"
    import sync_to_supabase as sync
    monkeypatch.setattr(sync, "SUPABASE_URL", "")
    monkeypatch.setattr(sync, "SUPABASE_KEY", "")
    rc = sync.run_sync(db_path=str(db_file), dry_run=False, verbose=False)
    assert rc == 2


def test_run_sync_dry_run_succeeds_without_credentials(tmp_path):
    """Dry-run nao precisa de credenciais."""
    db = tmp_path / "fake.db"
    conn = sqlite3.connect(str(db))
    conn.executescript("""
        CREATE TABLE citations (id INTEGER PRIMARY KEY, timestamp TEXT,
                                 vertical TEXT, llm TEXT, model TEXT,
                                 cited INTEGER, position INTEGER, cited_entity TEXT);
        CREATE TABLE citation_context (id INTEGER PRIMARY KEY,
                                        citation_id INTEGER, entity TEXT);
        CREATE TABLE collection_runs (id INTEGER PRIMARY KEY, timestamp TEXT,
                                       vertical TEXT, module TEXT, status TEXT);
        CREATE TABLE verticals (slug TEXT, cohort_json TEXT);
        CREATE TABLE finops_usage (id INTEGER PRIMARY KEY, timestamp TEXT,
                                    platform TEXT, cost_usd REAL, total_tokens INTEGER);
        CREATE TABLE finops_budgets (platform TEXT PRIMARY KEY,
                                      monthly_limit_usd REAL, daily_limit_usd REAL);
    """)
    conn.commit()
    conn.close()
    import sync_to_supabase as sync
    rc = sync.run_sync(
        db_path=str(db),
        verticals=["fintech"],
        dry_run=True,
        verbose=False,
    )
    assert rc == 0


# ─── Mock Supabase upload ─────────────────────────────────────────────────


def test_upsert_mock_success(tmp_path):
    import sync_to_supabase as sync
    mock_client = MagicMock()
    mock_table = MagicMock()
    mock_client.table.return_value = mock_table
    mock_table.upsert.return_value = mock_table
    mock_table.execute.return_value = MagicMock(data=[{"id": 1}])

    rows = [{"vertical": "fintech", "key": "value"}]
    ok = sync._upsert(mock_client, sync.TABLE_DASHBOARD, rows, dry_run=False)
    assert ok is True
    mock_client.table.assert_called_with(sync.TABLE_DASHBOARD)


def test_upsert_mock_error_propagates():
    import sync_to_supabase as sync
    mock_client = MagicMock()
    mock_client.table.return_value.upsert.return_value.execute.side_effect = (
        Exception("HTTP 500: server error")
    )
    rows = [{"vertical": "fintech", "key": "value"}]
    ok = sync._upsert(mock_client, sync.TABLE_DASHBOARD, rows, dry_run=False)
    assert ok is False


def test_upsert_empty_rows_is_noop():
    import sync_to_supabase as sync
    ok = sync._upsert(MagicMock(), sync.TABLE_DASHBOARD, [], dry_run=False)
    assert ok is True


# ─── Sentinelas ────────────────────────────────────────────────────────────


def test_sync_does_not_leak_pii_in_aggregations(memory_db):
    """Agregacoes JAMAIS devem incluir PII (emails, telefones).

    A pesquisa cientifica eh sobre marcas/empresas, nao individuos.
    Mesmo assim, sentinela contra leak de campos sensiveis.
    """
    import sync_to_supabase as sync
    cr = sync._citation_rates(memory_db, "fintech")
    er = sync._entity_rankings(memory_db, "fintech")
    serialized = str(cr) + str(er)
    # Sentinelas contra padroes de email/telefone
    assert "@" not in serialized or serialized.count("@") == 0
    assert not any(c.isdigit() and len(c) == 11 for c in serialized.split())


def test_aggregations_handle_missing_tables_gracefully():
    """Banco vazio nao deve crashar — _query retorna []."""
    import sync_to_supabase as sync
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    # Sem nenhuma tabela criada
    rows = sync._query(conn, "SELECT * FROM nonexistent")
    assert rows == []
    conn.close()
