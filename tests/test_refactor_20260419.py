"""Testes de regressão do refactor 2026-04-19 (Ondas 1-4).

Cobertura:
- config.query_type_for() — classificação por categoria com override
- config.is_fictional() — detecção case-insensitive
- config.get_fictional_probe_queries() — probe para cada vertical
- config.mandatory_llms() — default + override via env
- migrate_0003 — idempotência + colunas + índices + backfill
"""

from __future__ import annotations

import os
import sqlite3
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.config import (  # noqa: E402
    FICTIONAL_ENTITIES,
    QUERY_TYPE_BY_CATEGORY,
    get_fictional_probe_queries,
    get_queries,
    is_fictional,
    list_verticals,
    mandatory_llms,
    query_type_for,
)
from src.db.migrate_0003_eficacia_consistencia import migrate  # noqa: E402


# ── query_type_for ────────────────────────────────────────────────────────


def test_query_type_for_directive_categories():
    for cat in ["descoberta", "comparativo", "b2b", "mercado", "reputacao"]:
        assert query_type_for({"category": cat}) == "directive", f"{cat} deve ser directive"


def test_query_type_for_exploratory_categories():
    for cat in ["confianca", "produto", "investimento", "alternativas"]:
        assert query_type_for({"category": cat}) == "exploratory", f"{cat} deve ser exploratory"


def test_query_type_for_explicit_override():
    """Chave 'type' explícita sobrescreve a heurística."""
    q = {"category": "descoberta", "type": "exploratory"}
    assert query_type_for(q) == "exploratory"


def test_query_type_for_unknown_category_defaults_exploratory():
    assert query_type_for({"category": "categoria_inventada"}) == "exploratory"
    assert query_type_for({}) == "exploratory"


def test_query_type_table_covers_all_real_categories():
    """Todas as categorias usadas no config.py devem estar mapeadas."""
    from src.config import VERTICALS, COMMON_QUERIES
    seen: set[str] = set()
    for q in COMMON_QUERIES:
        seen.add(q["category"])
    for v in VERTICALS.values():
        for q in v["queries"]:
            seen.add(q["category"])
    missing = seen - QUERY_TYPE_BY_CATEGORY.keys()
    assert not missing, (
        f"Categorias sem classificação directive/exploratory: {missing}. "
        f"Adicione em QUERY_TYPE_BY_CATEGORY."
    )


# ── Fictional entities ─────────────────────────────────────────────────────


def test_fictional_entities_all_verticals_present():
    assert set(FICTIONAL_ENTITIES.keys()) == set(list_verticals())
    for names in FICTIONAL_ENTITIES.values():
        assert len(names) >= 2, "Cada vertical precisa de ≥2 entidades fictícias"


def test_is_fictional_case_insensitive():
    assert is_fictional("Banco Floresta Digital")
    assert is_fictional("banco floresta digital")
    assert is_fictional("MEGASTORE BRASIL")
    assert not is_fictional("Nubank")
    assert not is_fictional("Magazine Luiza")
    assert not is_fictional("")


def test_get_fictional_probe_queries_has_pt_and_en():
    for v in list_verticals():
        probes = get_fictional_probe_queries(v)
        assert len(probes) >= 4, f"Vertical {v}: esperado ≥4 probes (2 fictícias × 2 langs)"
        langs = {p["lang"] for p in probes}
        assert langs == {"pt", "en"}, f"Vertical {v}: deve ter probe PT e EN"
        for p in probes:
            assert p["category"] == "calibracao_fp"
            assert p["type"] == "exploratory"
            assert "target_fictional" in p
            assert is_fictional(p["target_fictional"])


def test_get_queries_respects_include_fictional_flag():
    qs_without = get_queries("fintech", include_common=False, include_fictional=False)
    qs_with = get_queries("fintech", include_common=False, include_fictional=True)
    assert len(qs_with) == len(qs_without) + 4  # 2 fictícias × 2 langs


# ── Mandatory LLMs ─────────────────────────────────────────────────────────


def test_mandatory_llms_default_all_five(monkeypatch):
    monkeypatch.delenv("MANDATORY_LLMS", raising=False)
    assert mandatory_llms() == {"ChatGPT", "Claude", "Gemini", "Perplexity", "Groq"}


def test_mandatory_llms_override(monkeypatch):
    monkeypatch.setenv("MANDATORY_LLMS", "ChatGPT,Claude")
    assert mandatory_llms() == {"ChatGPT", "Claude"}


# ── Migration 0003 ─────────────────────────────────────────────────────────


@pytest.fixture
def fresh_db(tmp_path: Path) -> Path:
    """DB minimal com esquema compatível pré-Migration 0003."""
    db = tmp_path / "test.db"
    con = sqlite3.connect(db)
    con.executescript("""
        CREATE TABLE citations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT, llm TEXT, model TEXT, model_version TEXT,
            query TEXT, query_category TEXT, query_lang TEXT,
            vertical TEXT, cited INTEGER
        );
        CREATE TABLE finops_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT, platform TEXT, model TEXT, operation TEXT,
            vertical TEXT, input_tokens INTEGER, output_tokens INTEGER,
            total_tokens INTEGER, cost_usd REAL
        );
    """)
    # seed 2 registros sem model_version e 1 finops sem vertical
    con.execute(
        "INSERT INTO citations (timestamp, llm, model, query, query_category, "
        "query_lang, vertical, cited) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        ("2026-04-01T00:00:00Z", "ChatGPT", "gpt-4o-mini", "test", "descoberta", "pt", "fintech", 1),
    )
    con.execute(
        "INSERT INTO citations (timestamp, llm, model, model_version, query, "
        "query_category, query_lang, vertical, cited) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        ("2026-04-02T00:00:00Z", "Claude", "haiku", "haiku-4-5-20251001", "test2",
         "confianca", "en", "varejo", 0),
    )
    con.execute(
        "INSERT INTO finops_usage (timestamp, platform, model, operation) VALUES (?, ?, ?, ?)",
        ("2026-04-01T00:00:00Z", "openai", "gpt-4o-mini", "test"),
    )
    con.commit()
    con.close()
    return db


def test_migration_0003_adds_query_type_column(fresh_db: Path):
    migrate(fresh_db, dry_run=False)
    con = sqlite3.connect(fresh_db)
    cols = [r[1] for r in con.execute("PRAGMA table_info(citations)").fetchall()]
    assert "query_type" in cols
    con.close()


def test_migration_0003_creates_indexes(fresh_db: Path):
    migrate(fresh_db, dry_run=False)
    con = sqlite3.connect(fresh_db)
    indexes = {r[0] for r in con.execute(
        "SELECT name FROM sqlite_master WHERE type='index'"
    ).fetchall()}
    expected = {
        "idx_citations_vertical_cited",
        "idx_citations_vertical_llm",
        "idx_citations_timestamp_vert",
        "idx_citations_llm_modelver",
        "idx_citations_query_type",
    }
    assert expected.issubset(indexes), f"Faltam índices: {expected - indexes}"
    con.close()


def test_migration_0003_backfill_model_version(fresh_db: Path):
    migrate(fresh_db, dry_run=False)
    con = sqlite3.connect(fresh_db)
    nulls = con.execute(
        "SELECT COUNT(*) FROM citations WHERE model_version IS NULL OR model_version = ''"
    ).fetchone()[0]
    assert nulls == 0
    # O registro que tinha NULL deve ter herdado model (gpt-4o-mini)
    val = con.execute(
        "SELECT model_version FROM citations WHERE llm='ChatGPT'"
    ).fetchone()[0]
    assert val == "gpt-4o-mini"
    # O registro que já tinha deve ter sido preservado
    val2 = con.execute(
        "SELECT model_version FROM citations WHERE llm='Claude'"
    ).fetchone()[0]
    assert val2 == "haiku-4-5-20251001"
    con.close()


def test_migration_0003_backfill_finops_vertical(fresh_db: Path):
    migrate(fresh_db, dry_run=False)
    con = sqlite3.connect(fresh_db)
    val = con.execute("SELECT vertical FROM finops_usage").fetchone()[0]
    assert val == "unknown"
    con.close()


def test_migration_0003_idempotent(fresh_db: Path):
    """Rodar 2x não deve causar erro nem duplicar índices."""
    s1 = migrate(fresh_db, dry_run=False)
    s2 = migrate(fresh_db, dry_run=False)
    assert s1["added_column_query_type"] is True
    assert s2["added_column_query_type"] is False  # já existia
    assert len(s2["added_indexes"]) == 0  # todos já criados
    assert s2["backfilled_model_version"] == 0  # já preenchido


def test_migration_0003_dry_run_does_not_modify(fresh_db: Path):
    s = migrate(fresh_db, dry_run=True)
    assert s["added_column_query_type"] is True  # reportaria o que faria
    assert s["dry_run"] is True
    # Confirma que NADA foi persistido
    con = sqlite3.connect(fresh_db)
    cols = [r[1] for r in con.execute("PRAGMA table_info(citations)").fetchall()]
    assert "query_type" not in cols
    indexes = {r[0] for r in con.execute(
        "SELECT name FROM sqlite_master WHERE type='index'"
    ).fetchall()}
    assert "idx_citations_query_type" not in indexes
    con.close()
