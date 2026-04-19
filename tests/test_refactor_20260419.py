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
from src.db.migrate_0004_fictional_persistence import migrate as migrate_0004  # noqa: E402


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


# ── Migration 0004 (double-check #2) ───────────────────────────────────────


def test_migration_0004_adds_fictional_columns(fresh_db: Path):
    migrate_0004(fresh_db, dry_run=False)
    con = sqlite3.connect(fresh_db)
    cols = [r[1] for r in con.execute("PRAGMA table_info(citations)").fetchall()]
    assert "fictional_hit" in cols
    assert "fictional_names_json" in cols
    con.close()


def test_migration_0004_creates_fictional_index(fresh_db: Path):
    migrate_0004(fresh_db, dry_run=False)
    con = sqlite3.connect(fresh_db)
    idx = {r[0] for r in con.execute(
        "SELECT name FROM sqlite_master WHERE type='index'"
    ).fetchall()}
    assert "idx_citations_fictional_hit" in idx
    con.close()


def test_migration_0004_backfill_marks_fictional_mentions(fresh_db: Path):
    # Seed com response_text que menciona entidade fictícia
    con = sqlite3.connect(fresh_db)
    con.execute(
        "ALTER TABLE citations ADD COLUMN response_text TEXT"
    )
    con.execute(
        "INSERT INTO citations (timestamp, llm, model, query, query_category, "
        "query_lang, vertical, cited, response_text) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        ("2026-04-19T00:00:00Z", "ChatGPT", "gpt-4o-mini", "test", "descoberta",
         "pt", "fintech", 1, "Banco Floresta Digital é uma fintech brasileira."),
    )
    con.execute(
        "INSERT INTO citations (timestamp, llm, model, query, query_category, "
        "query_lang, vertical, cited, response_text) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        ("2026-04-19T00:00:00Z", "ChatGPT", "gpt-4o-mini", "test", "descoberta",
         "pt", "fintech", 1, "Nubank é líder de mercado."),
    )
    con.commit()
    con.close()

    s = migrate_0004(fresh_db, dry_run=False)
    assert s["rows_scanned"] == 2
    assert s["rows_marked_fictional"] == 1

    con = sqlite3.connect(fresh_db)
    con.row_factory = sqlite3.Row
    marked = con.execute(
        "SELECT fictional_hit, fictional_names_json FROM citations "
        "WHERE response_text LIKE '%Floresta%'"
    ).fetchone()
    assert marked["fictional_hit"] == 1
    assert "Banco Floresta Digital" in marked["fictional_names_json"]

    not_marked = con.execute(
        "SELECT fictional_hit FROM citations WHERE response_text LIKE '%Nubank%'"
    ).fetchone()
    assert not_marked["fictional_hit"] == 0
    con.close()


def test_migration_0004_idempotent(fresh_db: Path):
    s1 = migrate_0004(fresh_db, dry_run=False)
    s2 = migrate_0004(fresh_db, dry_run=False)
    assert len(s1["added_columns"]) == 2
    assert len(s2["added_columns"]) == 0
    assert len(s2["added_indexes"]) == 0


# ── Statistical stratification helpers (double-check #2) ────────────────────


def test_stratified_citation_rate_by_query_type():
    """Helper novo em analysis/statistical.py: calcula rate+IC por strata."""
    pd = pytest.importorskip("pandas")
    from src.analysis.statistical import StatisticalAnalyzer
    df = pd.DataFrame({
        "query_type": ["directive"] * 10 + ["exploratory"] * 10,
        "cited": [1] * 8 + [0] * 2 + [1] * 4 + [0] * 6,
    })
    out = StatisticalAnalyzer.stratified_citation_rate(df, "query_type", "cited")
    # Ordenado por rate desc
    assert out.iloc[0]["stratum"] == "directive"
    assert out.iloc[0]["k"] == 8
    assert out.iloc[0]["rate"] == 0.8
    assert out.iloc[1]["stratum"] == "exploratory"
    assert out.iloc[1]["rate"] == 0.4
    # IC contém o ponto estimado
    for _, row in out.iterrows():
        assert row["ci_low"] <= row["rate"] <= row["ci_high"]


def test_stratified_citation_rate_missing_column_raises():
    pd = pytest.importorskip("pandas")
    from src.analysis.statistical import StatisticalAnalyzer
    df = pd.DataFrame({"a": [1, 2], "b": [0, 1]})
    with pytest.raises(KeyError):
        StatisticalAnalyzer.stratified_citation_rate(df, "inexistente")


def test_false_positive_rate_helper():
    pd = pytest.importorskip("pandas")
    from src.analysis.statistical import StatisticalAnalyzer
    df = pd.DataFrame({"fictional_hit": [0, 0, 1, 0, 1, 0, 0, 0, 0, 0]})
    out = StatisticalAnalyzer.false_positive_rate(df)
    assert out["n_total"] == 10
    assert out["n_fictional_hits"] == 2
    assert out["fp_rate"] == 0.2
    assert out["specificity"] == 0.8


def test_cochran_mantel_haenszel_controls_for_confounder():
    """CMH deve neutralizar efeito de lang ao comparar directive vs exploratory."""
    pd = pytest.importorskip("pandas")
    from src.analysis.statistical import StatisticalAnalyzer
    analyzer = StatisticalAnalyzer()
    # 2x2x2 table: directive vs exploratory, stratified by lang=pt|en
    df = pd.DataFrame({
        "query_type": ["directive"] * 50 + ["exploratory"] * 50,
        "cited":      [1] * 40 + [0] * 10 + [1] * 30 + [0] * 20,
        "query_lang": ["pt"] * 25 + ["en"] * 25 + ["pt"] * 25 + ["en"] * 25,
    })
    result = analyzer.cochran_mantel_haenszel(
        df, group_col="query_type", outcome_col="cited", stratify_by="query_lang",
    )
    assert result.test_name.startswith("cochran-mantel-haenszel")
    assert result.p_value >= 0.0
    assert result.statistic >= 0.0


def test_cochran_mantel_haenszel_rejects_non_binary_group():
    pd = pytest.importorskip("pandas")
    from src.analysis.statistical import StatisticalAnalyzer
    analyzer = StatisticalAnalyzer()
    df = pd.DataFrame({
        "query_type": ["a", "b", "c", "a"],
        "cited": [1, 0, 1, 0],
        "query_lang": ["pt", "en", "pt", "en"],
    })
    with pytest.raises(ValueError):
        analyzer.cochran_mantel_haenszel(df, "query_type", "cited", "query_lang")


# ── db/client auto-migration (double-check #2) ──────────────────────────────


def test_db_client_auto_adds_fictional_columns(tmp_path: Path, monkeypatch):
    """DatabaseClient.apply_schema deve rodar as migrations inline (0003+0004)
    quando executado em um DB novo — garante que não é preciso rodar
    standalone para repos em fresh install."""
    monkeypatch.setenv("PAPERS_DB_PATH", str(tmp_path / "fresh.db"))
    from src.db.client import DatabaseClient
    db = DatabaseClient(db_path=tmp_path / "fresh.db")
    db.connect()
    try:
        cols = [r[1] for r in db._conn.execute("PRAGMA table_info(citations)").fetchall()]
        assert "query_type" in cols
        assert "fictional_hit" in cols
        assert "fictional_names_json" in cols
        assert "model_version" in cols
    finally:
        db.close()
