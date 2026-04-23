"""Testes do config_v2 — cohort + query battery v2."""
from __future__ import annotations

import pytest

from src.config_v2 import (
    COHORT_FINTECH_ANCHORS,
    COHORT_FINTECH_REAL,
    COHORT_HEALTH_ANCHORS,
    COHORT_HEALTH_REAL,
    COHORT_RETAIL_ANCHORS,
    COHORT_RETAIL_REAL,
    COHORT_TECHNOLOGY_ANCHORS,
    COHORT_TECHNOLOGY_REAL,
    FICTITIOUS_DECOYS_V2,
    QUERY_CATEGORIES_V2,
    QUERY_TYPES_V2,
    TEMPORAL_FRAMES_V2,
    build_canonical_battery,
    build_query,
    _validate_cohort_v2,
    _validate_query_battery,
)


def test_cohort_v2_counts():
    assert len(COHORT_FINTECH_REAL) == 19
    assert len(COHORT_FINTECH_ANCHORS) == 8
    assert len(COHORT_RETAIL_REAL) == 20
    assert len(COHORT_RETAIL_ANCHORS) == 8
    assert len(COHORT_HEALTH_REAL) == 20
    assert len(COHORT_HEALTH_ANCHORS) == 8
    assert len(COHORT_TECHNOLOGY_REAL) == 20
    assert len(COHORT_TECHNOLOGY_ANCHORS) == 8


def test_cohort_geographic_diversity():
    """Cohort deve ter representação fora de SP (gap D7 Agent D)."""
    regions_br = set()
    for cohort in [COHORT_FINTECH_REAL, COHORT_RETAIL_REAL,
                   COHORT_HEALTH_REAL, COHORT_TECHNOLOGY_REAL]:
        for e in cohort:
            if e.region:
                regions_br.add(e.region)
    # Deve ter pelo menos 5 regiões distintas
    assert len(regions_br) >= 5, f"Regiões BR: {regions_br}"


def test_cohort_has_long_tail():
    """Cada vertical deve ter >=3 entidades long_tail (gap D6)."""
    for name, cohort in [
        ("fintech", COHORT_FINTECH_REAL),
        ("retail", COHORT_RETAIL_REAL),
        ("health", COHORT_HEALTH_REAL),
        ("technology", COHORT_TECHNOLOGY_REAL),
    ]:
        long_tail = [e for e in cohort if e.tier == "long_tail"]
        assert len(long_tail) >= 3, f"{name}: only {len(long_tail)} long_tail"


def test_legal_status_tracked():
    """Americanas deve estar marcada como judicial_recovery (gap D5)."""
    americanas = next(e for e in COHORT_RETAIL_REAL if e.name == "Americanas")
    assert americanas.legal_status == "judicial_recovery"


def test_decoys_have_4_per_vertical():
    for v in ["fintech", "retail", "health", "technology"]:
        assert len(FICTITIOUS_DECOYS_V2[v]) == 4


def test_decoys_distinct_from_cohort():
    """Nenhuma fictícia v2 pode colidir com cohort real."""
    real_names = set()
    for cohort in [COHORT_FINTECH_REAL, COHORT_RETAIL_REAL,
                   COHORT_HEALTH_REAL, COHORT_TECHNOLOGY_REAL]:
        for e in cohort:
            real_names.add(e.name.lower())
    for v, decoys in FICTITIOUS_DECOYS_V2.items():
        for d in decoys:
            assert d.lower() not in real_names, f"Decoy '{d}' colide com real em {v}"


def test_cohort_no_duplicates_within_vertical():
    for cohort in [COHORT_FINTECH_REAL, COHORT_RETAIL_REAL,
                   COHORT_HEALTH_REAL, COHORT_TECHNOLOGY_REAL]:
        names = [e.name for e in cohort]
        assert len(names) == len(set(names))


def test_query_battery_192_total():
    qs = build_canonical_battery()
    assert len(qs) == 192


def test_query_battery_balanced_lang():
    qs = build_canonical_battery()
    pt = sum(1 for q in qs if q["lang"] == "pt")
    en = sum(1 for q in qs if q["lang"] == "en")
    assert pt == 96 and en == 96


def test_query_battery_balanced_type():
    qs = build_canonical_battery()
    d = sum(1 for q in qs if q["query_type"] == "directive")
    e = sum(1 for q in qs if q["query_type"] == "exploratory")
    assert d == 96 and e == 96


def test_query_battery_48_per_vertical():
    qs = build_canonical_battery()
    for v in ["fintech", "retail", "health", "technology"]:
        count = sum(1 for q in qs if q["vertical"] == v)
        assert count == 48


def test_query_battery_temporal_balance():
    qs = build_canonical_battery()
    atemporal = sum(1 for q in qs if q["temporal_frame"] == "atemporal")
    temporal = sum(1 for q in qs if q["temporal_frame"] == "em 2026")
    assert atemporal == temporal == 96


def test_en_queries_include_brazil_context():
    """Gap D9: EN queries SEMPRE explicitam 'Brazil' ou 'Brazilian'."""
    qs = build_canonical_battery()
    en_queries = [q for q in qs if q["lang"] == "en"]
    for q in en_queries:
        assert "Brazil" in q["query"] or "Brazilian" in q["query"], (
            f"EN query sem context BR: {q['query']}"
        )


def test_categories_match_expected():
    assert QUERY_CATEGORIES_V2 == ["descoberta", "comparativo", "confianca",
                                    "experiencia", "mercado", "inovacao"]


def test_build_query_determinism():
    """Mesmos args → mesma query string."""
    q1 = build_query("fintech", "descoberta", "directive", "pt", "atemporal")
    q2 = build_query("fintech", "descoberta", "directive", "pt", "atemporal")
    assert q1 == q2


def test_validate_helpers_pass():
    _validate_cohort_v2()
    _validate_query_battery()
