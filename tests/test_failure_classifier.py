"""Tests for citation selection/absorption derivation + failure taxonomy.

Cobre src/collectors/failure_classifier.py e o round-trip end-to-end das
colunas da Migration 0009 via DatabaseClient.insert_citations.
"""
from __future__ import annotations

from src.collectors.failure_classifier import (
    classify_failure,
    derive_citation_status,
    slug,
)
from src.db.client import DatabaseClient


def test_slug_normalizes() -> None:
    assert slug("Mercado Pago") == "mercadopago"
    assert slug("C6 Bank") == "c6bank"
    assert slug("Itaú") == "ita"  # acento removido pelo filtro a-z0-9


def test_absorbed_and_selected() -> None:
    sel, ab = derive_citation_status(
        cited=True,
        cited_entities=["Nubank"],
        cohort=["Nubank", "PicPay"],
        sources=["https://nubank.com.br/sobre"],
    )
    assert (sel, ab) == (1, 1)


def test_absorbed_not_selected_is_attribution_drop() -> None:
    sel, ab = derive_citation_status(
        cited=True,
        cited_entities=["Nubank"],
        cohort=["Nubank"],
        sources=["https://example.com/fintech-roundup"],
    )
    assert (sel, ab) == (0, 1)
    ft = classify_failure(cited=True, selection_status=sel, absorption_status=ab)
    assert ft == "attribution-drop"


def test_selected_not_absorbed() -> None:
    sel, ab = derive_citation_status(
        cited=False,
        cited_entities=[],
        cohort=["Stone"],
        sources=["https://stone.com.br/precos"],
    )
    assert (sel, ab) == (1, 0)


def test_neither() -> None:
    sel, ab = derive_citation_status(
        cited=False, cited_entities=[], cohort=["Neon"], sources=[]
    )
    assert (sel, ab) == (0, 0)


def test_failure_hallucinated_source() -> None:
    assert (
        classify_failure(
            cited=True, selection_status=0, absorption_status=1, fictional_hit=True
        )
        == "hallucinated-source"
    )


def test_failure_transport_and_robots() -> None:
    assert classify_failure(
        cited=False, selection_status=0, absorption_status=0,
        response_error="Network error after retries",
    ) == "broken-fetch"
    assert classify_failure(
        cited=False, selection_status=0, absorption_status=0,
        response_error="HTTP 403 Forbidden by robots",
    ) == "blocked-by-robots"


def test_failure_parsing_and_retrieval_miss_and_none() -> None:
    assert classify_failure(
        cited=False, selection_status=0, absorption_status=0, response_text="   "
    ) == "parsing-failure"
    assert classify_failure(
        cited=False, selection_status=0, absorption_status=0, expected=True
    ) == "retrieval-miss"
    # caso saudável: absorvido e selecionado, sem expectativa -> sem falha
    assert classify_failure(
        cited=True, selection_status=1, absorption_status=1
    ) is None


def test_insert_citations_round_trip_0009(tmp_path) -> None:
    db = DatabaseClient(str(tmp_path / "rt.db"))
    db.connect()
    # insert_citations referencia colunas de migrations standalone (0005/0006/0007)
    # que não estão no schema.sql; aplica-as para espelhar um DB de produção.
    from src.db import (
        migrate_0005_ner_v2,
        migrate_0006_response_hash,
        migrate_0007_probe_fictitious,
    )
    migrate_0005_ner_v2.apply(db._conn)
    migrate_0006_response_hash.apply(db._conn)
    migrate_0007_probe_fictitious.apply(db._conn)
    try:
        rec = {
            "timestamp": "2026-06-07T00:00:00Z",
            "llm": "Claude", "model": "claude-haiku-4-5", "query": "melhor fintech",
            "query_category": "brand", "query_lang": "pt",
            "cited": True,
            "selection_status": 0, "absorption_status": 1,
            "failure_type": "attribution-drop",
            "all_sources": ["https://example.com"],
        }
        n = db.insert_citations([rec], vertical="fintech")
        assert n == 1
        row = db._conn.execute(
            "SELECT selection_status, absorption_status, failure_type FROM citations LIMIT 1"
        ).fetchone()
        assert tuple(row) == (0, 1, "attribution-drop")
    finally:
        db.close()
