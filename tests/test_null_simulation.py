"""Testes do null_simulation.py — distribuição de Jaccard sob H0."""
from __future__ import annotations

import numpy as np
import pytest

from src.analysis.null_simulation import (
    jaccard_null_threshold,
    jaccard_similarity,
    simulate_jaccard_null,
)


def test_jaccard_basic():
    assert jaccard_similarity({1, 2, 3}, {2, 3, 4}) == 2 / 4
    assert jaccard_similarity({1, 2}, {3, 4}) == 0.0
    assert jaccard_similarity({1, 2}, {1, 2}) == 1.0
    assert jaccard_similarity(set(), set()) == 1.0  # edge case


def test_simulate_smaller_than_cohort():
    r = simulate_jaccard_null(cohort_size=20, top_k=5, n_llms=3, n_simulations=500, seed=42)
    # Expected: com 20 entidades totais e 5 por LLM, intersect pairwise ~ 5*5/20 = 1.25
    # Jaccard ~ 1.25 / (5 + 5 - 1.25) = 0.14
    assert 0.10 < r.mean < 0.25
    assert r.n_simulations == 500
    assert r.cohort_size == 20


def test_top_k_equal_cohort_means_identical():
    """Se top_k == cohort_size, todos LLMs pegam mesmo conjunto → Jaccard=1."""
    r = simulate_jaccard_null(cohort_size=10, top_k=10, n_llms=3, n_simulations=100, seed=0)
    assert r.mean == 1.0


def test_threshold_reproducible():
    t1 = jaccard_null_threshold(cohort_size=61, top_k=30, n_llms=4, n_simulations=1000, seed=42)
    t2 = jaccard_null_threshold(cohort_size=61, top_k=30, n_llms=4, n_simulations=1000, seed=42)
    assert t1 == t2


def test_invalid_top_k():
    with pytest.raises(ValueError):
        simulate_jaccard_null(cohort_size=10, top_k=20, n_llms=2)


def test_invalid_n_llms():
    with pytest.raises(ValueError):
        simulate_jaccard_null(cohort_size=10, top_k=5, n_llms=1)


def test_threshold_for_paper4_params():
    """Para cohort=61, top_k=30, 4 LLMs: threshold P5 tipicamente 0.10-0.18."""
    t = jaccard_null_threshold(
        cohort_size=61, top_k=30, n_llms=4, n_simulations=2000, seed=42
    )
    assert 0.05 < t < 0.30
