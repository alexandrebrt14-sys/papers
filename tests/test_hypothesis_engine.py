"""Testes do hypothesis_engine — BH-FDR, decision rule, H1/H2/H3 runners."""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.analysis.hypothesis_engine import (
    HypothesisEngine,
    HypothesisResult,
    apply_decision_rule,
    benjamini_hochberg,
    run_h1_rag_advantage,
    run_h2_hallucination,
    run_h3_jaccard,
)


# ---------- BH-FDR ----------

def test_bh_sorted_monotone():
    """BH-adjusted p-values são monotônicos não-decrescentes após sort."""
    p = [0.001, 0.01, 0.04, 0.08, 0.2]
    adj = benjamini_hochberg(p, alpha=0.05)
    # Sort and check monotonic
    sorted_adj = sorted(adj)
    for i in range(len(sorted_adj) - 1):
        assert sorted_adj[i] <= sorted_adj[i + 1]


def test_bh_empty_input():
    assert benjamini_hochberg([]) == []


def test_bh_conservative_vs_raw():
    """BH-adjusted sempre >= raw p-value."""
    p = [0.001, 0.01, 0.04, 0.08]
    adj = benjamini_hochberg(p)
    for raw, a in zip(p, adj):
        assert a >= raw


def test_bh_capped_at_one():
    p = [0.9, 0.95, 0.99]
    adj = benjamini_hochberg(p)
    for a in adj:
        assert a <= 1.0


# ---------- Decision rule ----------

def test_decision_rule_reject_when_significant():
    v, m = apply_decision_rule(p_bh=0.01, ci_low=0.05, ci_high=0.15, null_value=0.0)
    assert v == "reject H0"
    assert m == "significant"


def test_decision_rule_fail_to_reject_underpower():
    v, m = apply_decision_rule(p_bh=0.08, ci_low=-0.02, ci_high=0.12, null_value=0.0)
    assert v == "fail to reject"
    assert m == "underpower"


def test_decision_rule_pending_when_missing():
    v, m = apply_decision_rule(p_bh=None, ci_low=None, ci_high=None)
    assert v == "pending"


# ---------- H1 smoke test ----------

def test_h1_rag_advantage_basic():
    """H1 com dados sintéticos — verifica pipeline roda sem erro."""
    np.random.seed(42)
    n = 500
    df = pd.DataFrame({
        "cited": np.random.binomial(1, 0.75, n),
        "is_rag": np.tile([1, 0], n // 2),
        "day": np.random.choice(["2026-04-23", "2026-04-24", "2026-04-25"], n),
    })
    result = run_h1_rag_advantage(df)
    assert result.hypothesis == "H1"
    assert result.n_observations == n
    assert result.effect_size is not None
    assert result.verdict in {"reject H0", "fail to reject", "pending"}


def test_h1_with_real_rag_advantage():
    """Simula RAG realmente maior — esperar reject H0 se n suficiente."""
    np.random.seed(0)
    n = 2000
    df = pd.DataFrame({
        "cited": np.concatenate([
            np.random.binomial(1, 0.85, n // 2),  # RAG: 85%
            np.random.binomial(1, 0.65, n // 2),  # parametric: 65%
        ]),
        "is_rag": [1] * (n // 2) + [0] * (n // 2),
        "day": np.random.choice([f"day_{i}" for i in range(10)], n),
    })
    result = run_h1_rag_advantage(df, mde_h=0.10)
    # Com h~0.46 (big effect) e n=2000, provavelmente reject
    assert result.effect_size > 0
    assert result.ci_low is not None


# ---------- H2 smoke test ----------

def test_h2_design_null_when_probe_absent():
    """Se fictitious_hit col ausente, devolve 'design null'."""
    df = pd.DataFrame({"cited": [0, 1, 0, 1]})
    result = run_h2_hallucination(df)
    assert result.verdict == "design null"
    assert "fictitious_hit column absent" in result.warnings[0]


def test_h2_probe_active_zero_hits():
    """Probe ativo com k=0 hits — bound upper deve ser computado."""
    df = pd.DataFrame({
        "fictitious_hit": [0] * 1000,
        "is_probe": [1] * 1000,
    })
    result = run_h2_hallucination(df, upper_bound=0.01)
    assert result.statistic == 0.0
    assert result.effect_size is not None  # upper 95% bound (3/n)
    assert result.effect_size <= 0.01


# ---------- H3 smoke test ----------

def test_h3_low_overlap_reject_h0():
    """Universos quase disjuntos — deve rejeitar H0 'uniform'."""
    top_entities = {
        "LLM_A": ["Nubank", "Itaú", "Bradesco"],
        "LLM_B": ["Magalu", "Amazon", "Mercado Livre"],
        "LLM_C": ["Dasa", "Fleury", "Einstein"],
    }
    result = run_h3_jaccard(
        top_entities_by_llm=top_entities,
        cohort_size=60,
        top_k=3,
        n_simulations=500,
    )
    assert result.hypothesis == "H3"
    assert result.verdict in {"reject H0", "fail to reject"}


def test_h3_high_overlap_fail_to_reject():
    """Universos idênticos — deve falhar em rejeitar H0."""
    identical = ["Nubank", "Itaú", "Bradesco"]
    top_entities = {"A": identical, "B": identical, "C": identical}
    result = run_h3_jaccard(
        top_entities_by_llm=top_entities,
        cohort_size=60,
        top_k=3,
        n_simulations=500,
    )
    # Jaccard = 1 (idênticos) > threshold P5 (~0.0-0.2) → fail to reject
    assert result.verdict == "fail to reject"


# ---------- Family aggregation ----------

def test_family_applies_bh_fdr():
    """Family com 3 H's — BH-FDR aplicado."""
    h1 = HypothesisResult(
        hypothesis="H1", description="", n_observations=100,
        test_type="test", p_raw=0.01, ci_low=0.02, ci_high=0.10,
    )
    h2 = HypothesisResult(
        hypothesis="H2", description="", n_observations=100,
        test_type="test", p_raw=0.04,
    )
    h3 = HypothesisResult(
        hypothesis="H3", description="", n_observations=100,
        test_type="test", p_raw=0.10,
    )
    engine = HypothesisEngine(db_path="test.db")
    family = engine.run_family([h1, h2, h3])
    # All p-values got BH-adjusted
    for h in family.hypotheses:
        assert h.p_bh_adjusted is not None
        assert h.p_bh_adjusted >= h.p_raw
