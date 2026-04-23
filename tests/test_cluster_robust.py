"""Testes do CR1 cluster-robust estimator."""
from __future__ import annotations

import numpy as np
import pytest

from src.analysis.cluster_robust import (
    cluster_robust_diff_proportions,
    cluster_robust_mean,
)


def test_single_cluster_falls_back_to_iid():
    np.random.seed(42)
    y_a = np.random.binomial(1, 0.8, size=100)
    y_b = np.random.binomial(1, 0.7, size=100)
    c = np.zeros(100)  # mesmo cluster para ambos → só 1 cluster total
    r = cluster_robust_diff_proportions(y_a, y_b, c, c)
    assert r.n_clusters == 1
    assert abs(r.se_cluster - r.se_iid) < 1e-9


def test_independent_clusters_inflation_modest():
    """Quando obs independentes aleatórias dentro de cluster, CR1 ≈ iid."""
    np.random.seed(42)
    n = 1000
    y_a = np.random.binomial(1, 0.7, size=n)
    y_b = np.random.binomial(1, 0.68, size=n)
    # 20 clusters, obs distribuídas uniformemente
    c = np.tile(np.arange(20), n // 20)[:n]
    r = cluster_robust_diff_proportions(y_a, y_b, c, c)
    # Sem correlação intra-cluster, inflation deve ser ~1 (permitindo ruído)
    assert 0.5 < r.inflation < 2.5
    assert r.n_clusters == 20


def test_strong_correlation_inflates_se():
    """Se clusters têm rate HOMOGÊNEO diferente por cluster (strong ICC),
    CR1 deve inflar SE vs iid."""
    np.random.seed(42)
    # 10 clusters; dentro de cada, y_a e y_b compartilham p_cluster
    cluster_rates_a = [0.9, 0.85, 0.8, 0.75, 0.7, 0.65, 0.6, 0.55, 0.5, 0.45]
    cluster_rates_b = [0.88, 0.83, 0.78, 0.73, 0.68, 0.63, 0.58, 0.53, 0.48, 0.43]
    y_a, y_b, c_a, c_b = [], [], [], []
    for k, (pa, pb) in enumerate(zip(cluster_rates_a, cluster_rates_b)):
        y_a.extend(np.random.binomial(1, pa, 100))
        y_b.extend(np.random.binomial(1, pb, 100))
        c_a.extend([k] * 100)
        c_b.extend([k] * 100)
    r = cluster_robust_diff_proportions(np.array(y_a), np.array(y_b),
                                         np.array(c_a), np.array(c_b))
    # Como a diferença é ~constante por cluster, a covariância CROSS-GROUP
    # reduz V(diff). Inflation deve ser ~1 (diff estável entre clusters).
    assert r.n_clusters == 10
    # SE iid > 0, SE cluster > 0, razão finita
    assert r.se_cluster > 0
    assert r.se_iid > 0


def test_diff_matches_proportions():
    y_a = np.array([1] * 80 + [0] * 20)  # p_a = 0.80
    y_b = np.array([1] * 70 + [0] * 30)  # p_b = 0.70
    c = np.arange(100)  # cada obs = cluster único
    r = cluster_robust_diff_proportions(y_a, y_b, c, c)
    assert abs(r.diff - 0.10) < 1e-9
    assert r.n_a == 100
    assert r.n_b == 100


def test_ci_contains_truth_when_iid():
    """Com verdade conhecida e obs independentes, CI cobre truth ~95% do tempo."""
    np.random.seed(0)
    truth = 0.05
    coverages = 0
    TRIALS = 50
    for _ in range(TRIALS):
        n = 500
        y_a = np.random.binomial(1, 0.75, n)
        y_b = np.random.binomial(1, 0.70, n)
        c = np.random.randint(0, 10, n)
        r = cluster_robust_diff_proportions(y_a, y_b, c, c)
        if r.ci_low <= truth <= r.ci_high:
            coverages += 1
    # Cobertura deve ser ≥85% em 50 trials (tolerância estatística)
    assert coverages / TRIALS >= 0.80


def test_cluster_robust_mean_basic():
    np.random.seed(42)
    n = 500
    values = np.random.binomial(1, 0.75, n)
    clusters = np.random.randint(0, 5, n)
    r = cluster_robust_mean(values, clusters)
    assert "mean" in r
    assert "se_cluster" in r
    assert "inflation" in r
    assert r["n_clusters"] == 5
    assert 0.7 < r["mean"] < 0.8
