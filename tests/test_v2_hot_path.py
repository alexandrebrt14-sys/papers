"""Onda 7 — E2E test do hot path v2 (CitationTracker → DB).

Cobre o gap crítico identificado pela Onda E audit (2026-04-23):
- Zero cobertura do caminho CLI→collect()→insert()
- Zero teste que valida que colunas v2 são populadas no INSERT real

Estes testes constroem LLMResponse mocks, rodam _analyze em metodologia v2
e validam que `insert_citations()` grava corretamente as colunas de cada
migration (0005 NER v2, 0006 response_hash, 0007 probe design).

Sem rede. Usa tmp_path para DB isolado.
"""
from __future__ import annotations

import json
import shutil
import sqlite3
from pathlib import Path

import pytest

from src.collectors.base import LLMResponse
from src.db import (
    migrate_0005_ner_v2,
    migrate_0006_response_hash,
    migrate_0007_probe_fictitious,
)
from src.db.client import DatabaseClient


@pytest.fixture
def v2_db(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> str:
    """DB tmp com schema aplicado + todas migrations v2."""
    src_db = Path("data/papers.db")
    tmp_db = tmp_path / "papers_v2.db"
    if src_db.exists():
        shutil.copy(src_db, tmp_db)
    else:
        # fallback para CI: cria DB do zero
        tmp_db.touch()
    monkeypatch.setenv("PAPERS_DB_PATH", str(tmp_db))
    monkeypatch.setenv("PAPERS_METHODOLOGY_VERSION", "v2")

    # Garante migrations aplicadas
    conn = sqlite3.connect(tmp_db)
    migrate_0005_ner_v2.apply(conn)
    migrate_0006_response_hash.apply(conn)
    migrate_0007_probe_fictitious.apply(conn)
    conn.close()

    return str(tmp_db)


def _build_response(text: str, provider: str = "openai",
                    cited: list[str] | None = None) -> LLMResponse:
    return LLMResponse(
        model="gpt-4o-mini", provider=provider, query="test",
        response_text=text, sources=[], cited_entities=cited or [],
        timestamp="2026-04-24T09:00:00Z", latency_ms=250,
        input_tokens=50, output_tokens=80, cost_usd=0.0001,
    )


def _build_record(tracker, response: LLMResponse, query_entry: dict) -> dict:
    analysis = tracker._analyze(response, query_entry=query_entry)
    return {
        "module": "citation_tracker", "llm": response.provider,
        "model": response.model, "query": query_entry.get("query", "test"),
        "query_category": query_entry.get("category", "descoberta"),
        "query_lang": query_entry.get("lang", "pt"),
        "query_type": query_entry.get("query_type", "directive"),
        "timestamp": response.timestamp, "latency_ms": response.latency_ms,
        "token_count": (response.input_tokens + response.output_tokens),
        "input_tokens": response.input_tokens,
        "output_tokens": response.output_tokens, "from_cache": False,
        **analysis,
    }


# ---------- methodology flag + cohort/queries v2 ----------

def test_v2_tracker_loads_cohort_and_battery(v2_db: str, monkeypatch: pytest.MonkeyPatch) -> None:
    """CitationTracker v2 carrega 31-32 entidades + 48 queries canonical
    (+ 16 adversarial probes ativos por default, Onda 16/2026-04-29).

    Para isolar a battery canonical, opta-se por desligar probes via env.
    """
    monkeypatch.setenv("PAPERS_INCLUDE_ADVERSARIAL_PROBES", "0")
    from src.collectors.citation_tracker import CitationTracker
    for slug, expected_cohort, expected_queries in [
        ("fintech", 31, 48),
        ("varejo", 32, 48),
        ("saude", 32, 48),
        ("tecnologia", 32, 48),
    ]:
        ct = CitationTracker(vertical=slug)
        assert ct.methodology_version == "v2"
        assert len(ct.cohort) == expected_cohort, (
            f"{slug}: {len(ct.cohort)} != {expected_cohort}"
        )
        assert len(ct.queries) == expected_queries


def test_v2_tracker_includes_adversarial_probes_by_default(v2_db: str) -> None:
    """Default (PAPERS_INCLUDE_ADVERSARIAL_PROBES unset): 48 + 16 = 64 queries.

    Wire 2026-04-29 (Onda 16): adversarial probes essenciais para H2
    (false-positive baseline). Bug histórico: 100% das 8.571 rows na
    janela v2 inicial (23-29/abril) tinham is_probe=0 porque
    build_adversarial_queries() retornava []. Após fix, BaseCollector
    inclui as 16 probes/vertical em self.queries por default.
    """
    from src.collectors.citation_tracker import CitationTracker
    ct = CitationTracker(vertical="fintech")
    assert len(ct.queries) == 48 + 16
    probes = [q for q in ct.queries if q.get("is_probe")]
    assert len(probes) == 16
    assert all(p.get("target_fictional") for p in probes)
    assert all(p.get("adversarial_framing") == 1 for p in probes)


def test_v1_fallback_when_env_set(v2_db: str, monkeypatch: pytest.MonkeyPatch) -> None:
    """PAPERS_METHODOLOGY_VERSION=v1 cai no cohort/queries v1 legacy."""
    monkeypatch.setenv("PAPERS_METHODOLOGY_VERSION", "v1")
    from src.collectors.citation_tracker import CitationTracker
    ct = CitationTracker(vertical="fintech")
    assert ct.methodology_version == "v1"
    # v1 cohort tem diferente numero (inclui fictícias legacy)
    # e entity_extractor é None
    assert ct.entity_extractor is None


# ---------- NER v2 populates correct cols ----------

def test_v2_ner_extracts_via_fold(v2_db: str) -> None:
    """'Itau' (sem acento) → 'Itaú' com via_fold=1 (G1 do Null-Triad)."""
    from src.collectors.citation_tracker import CitationTracker
    ct = CitationTracker(vertical="fintech")
    response = _build_response("O Itau dominou o 1º trimestre de 2026.")
    analysis = ct._analyze(response, query_entry={"query": "x", "category": "descoberta", "lang": "pt"})
    assert analysis["extraction_version"] == "v2"
    assert "Itaú" in analysis["cited_entities_json"]
    assert analysis["via_fold_count_v2"] >= 1
    assert analysis["first_entity_v2"] == "Itaú"


def test_v2_ner_extracts_via_alias(v2_db: str) -> None:
    """'BTG' (alias) → 'BTG Pactual' com via_alias=1."""
    from src.collectors.citation_tracker import CitationTracker
    ct = CitationTracker(vertical="fintech")
    response = _build_response("BTG é forte em private banking.")
    analysis = ct._analyze(response, query_entry={"query": "x", "category": "mercado", "lang": "pt"})
    assert "BTG Pactual" in analysis["cited_entities_json"]
    assert analysis["via_alias_count_v2"] >= 1


# ---------- probe design cols ----------

def test_v2_probe_detected_when_target_fictional_set(v2_db: str) -> None:
    """query com target_fictional → is_probe=1, probe_type=decoy, is_calibration=1."""
    from src.collectors.citation_tracker import CitationTracker
    ct = CitationTracker(vertical="fintech")
    response = _build_response("Nubank lidera o setor.")
    query = {
        "query": "cite algum banco", "category": "descoberta", "lang": "pt",
        "target_fictional": "Banco Floresta Digital",
    }
    analysis = ct._analyze(response, query_entry=query)
    assert analysis["is_probe"] == 1
    assert analysis["probe_type"] == "decoy"
    assert analysis["is_calibration"] == 1
    assert analysis["fictitious_target"] == "Banco Floresta Digital"


def test_v2_fictitious_hit_on_decoy_in_text(v2_db: str) -> None:
    """Decoy v2 ('Banco Floresta Digital') no texto → fictional_hit=True."""
    from src.collectors.citation_tracker import CitationTracker
    ct = CitationTracker(vertical="fintech")
    response = _build_response("Banco Floresta Digital é inovador.")
    analysis = ct._analyze(response, query_entry={"query": "x", "category": "descoberta", "lang": "pt"})
    assert analysis["fictional_hit"] is True
    assert any("floresta" in n.lower() for n in analysis["fictional_names"])


# ---------- response_hash ----------

def test_v2_response_hash_populated(v2_db: str) -> None:
    """Toda citation tem SHA256 do response_text (primeiros 16 chars)."""
    from src.collectors.citation_tracker import CitationTracker
    ct = CitationTracker(vertical="fintech")
    response = _build_response("Texto qualquer de teste.")
    analysis = ct._analyze(response, query_entry={"query": "x", "category": "descoberta", "lang": "pt"})
    rh = analysis["response_hash"]
    assert rh is not None
    assert len(rh) == 16
    assert all(c in "0123456789abcdef" for c in rh)


# ---------- INSERT end-to-end ----------

def test_insert_citations_populates_all_v2_cols(v2_db: str) -> None:
    """INSERT real grava todas as colunas das migrations 0005/0006/0007."""
    from src.collectors.citation_tracker import CitationTracker
    ct = CitationTracker(vertical="fintech")
    response = _build_response(
        "Nubank e Itau dominam. BTG é forte. Banco Floresta Digital cresceu.",
        cited=["Nubank", "Itau"],
    )
    query = {
        "query": "test e2e", "category": "descoberta", "lang": "pt",
        "query_type": "directive",
        "target_fictional": "Banco Floresta Digital",
    }
    record = _build_record(ct, response, query)

    db = DatabaseClient()
    db.connect()
    n = db.insert_citations([record], vertical="fintech")
    assert n == 1

    conn = sqlite3.connect(v2_db)
    row = conn.execute(
        """SELECT extraction_version, cited_v2, cited_count_v2,
                  cited_entities_v2_json, first_entity_v2, position_v2,
                  via_fold_count_v2, via_alias_count_v2,
                  is_probe, probe_type, adversarial_framing,
                  fictitious_target, is_calibration, response_hash
           FROM citations WHERE query = ?""",
        ("test e2e",),
    ).fetchone()
    conn.close()
    db.close()

    (extraction_version, cited_v2, cited_count_v2, cited_entities_json,
     first_entity, position, via_fold, via_alias,
     is_probe, probe_type, adv_framing, fict_target, is_calib, rhash) = row

    assert extraction_version == "v2"
    assert cited_v2 == 1
    assert cited_count_v2 >= 3  # Nubank, Itaú, BTG Pactual, Floresta
    entities = json.loads(cited_entities_json)
    assert "Nubank" in entities and "Itaú" in entities and "BTG Pactual" in entities
    assert first_entity in entities
    assert position in (1, 2, 3)
    assert via_fold >= 1  # Itau→Itaú
    assert via_alias >= 1  # BTG→BTG Pactual
    assert is_probe == 1
    assert probe_type == "decoy"
    assert fict_target == "Banco Floresta Digital"
    assert is_calib == 1
    assert rhash is not None and len(rhash) == 16


# ---------- migrations idempotency ----------

def _fresh_schema_db(tmp_path: Path) -> sqlite3.Connection:
    """Load schema.sql into a fresh DB so migrations have the base cols they rely on."""
    db_path = tmp_path / "fresh.db"
    conn = sqlite3.connect(db_path)
    schema = Path("src/db/schema.sql").read_text(encoding="utf-8")
    conn.executescript(schema)
    return conn


def test_migration_0005_idempotent(tmp_path: Path) -> None:
    """migrate_0005 rodada 2x não duplica colunas."""
    conn = _fresh_schema_db(tmp_path)
    out1 = migrate_0005_ner_v2.apply(conn)
    out2 = migrate_0005_ner_v2.apply(conn)
    # 2a invocação não adiciona nada (todas as cols já existem)
    assert out2 == []
    conn.close()


def test_migration_0006_idempotent(tmp_path: Path) -> None:
    conn = _fresh_schema_db(tmp_path)
    out1 = migrate_0006_response_hash.apply(conn)
    out2 = migrate_0006_response_hash.apply(conn)
    assert out2 == []
    conn.close()


def test_migration_0007_idempotent(tmp_path: Path) -> None:
    conn = _fresh_schema_db(tmp_path)
    out1 = migrate_0007_probe_fictitious.apply(conn)
    out2 = migrate_0007_probe_fictitious.apply(conn)
    assert out2 == []
    conn.close()
