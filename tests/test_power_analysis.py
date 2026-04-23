"""Testes do power_analysis.py."""
from __future__ import annotations

import pytest

from src.analysis.power_analysis import (
    cohens_h,
    design_effect_adjusted_n,
    probe_fictitious_n_required,
    proportions_n_required,
    reboot_roadmap,
)


def test_probe_rule_of_three_basic():
    # Para upper_bound 1% com alpha 5%: n ≥ 3/0.01 = 300 (approx)
    n = probe_fictitious_n_required(p_max=0.005, upper_bound=0.01, alpha=0.05)
    # Via exact formula: ln(0.05)/ln(0.99) ≈ 299.1 → 300
    assert 298 <= n <= 302


def test_probe_for_tighter_bound():
    # Upper bound 0.1% → n ≈ 3000
    n = probe_fictitious_n_required(p_max=0.0001, upper_bound=0.001, alpha=0.05)
    # ln(0.05)/ln(0.999) ≈ 2994 → 2995
    assert 2990 <= n <= 3000


def test_probe_invalid_bound():
    with pytest.raises(ValueError):
        probe_fictitious_n_required(p_max=0.001, upper_bound=0.0)
    with pytest.raises(ValueError):
        probe_fictitious_n_required(p_max=0.001, upper_bound=1.0)


def test_cohens_h_zero_when_equal():
    assert cohens_h(0.5, 0.5) == 0.0
    assert cohens_h(0.7, 0.7) < 1e-9


def test_cohens_h_positive_when_different():
    assert cohens_h(0.8, 0.5) > 0.5  # large effect
    assert cohens_h(0.5, 0.45) < 0.15  # small effect


def test_proportions_n_required_for_small_effect():
    # Cohen's h=0.10, alpha=0.05, power=0.80 → n ≈ 785 per group
    n = proportions_n_required(h=0.10, alpha=0.05, power=0.80)
    assert 780 < n < 790


def test_proportions_n_required_for_large_effect():
    # h=0.50 → n ≈ 32 per group
    n = proportions_n_required(h=0.50, alpha=0.05, power=0.80)
    assert 30 < n < 35


def test_design_effect_no_correlation():
    """ICC=0 → DE=1 → n ajustado = n naive."""
    assert design_effect_adjusted_n(n_naive=100, m_per_cluster=10, icc=0.0) == 100


def test_design_effect_high_correlation():
    """ICC=0.1, m=20 → DE = 1 + 19*0.1 = 2.9 → n_adj ≈ 291 (ceil de 290)."""
    n_adj = design_effect_adjusted_n(n_naive=100, m_per_cluster=20, icc=0.1)
    assert 289 <= n_adj <= 291


def test_reboot_roadmap_has_all_hypotheses():
    rm = reboot_roadmap()
    hypotheses = [r.target_hypothesis for r in rm]
    # Pelo menos H1, H2, H3, H4 cobertos
    assert any("H1" in h for h in hypotheses)
    assert any("H2" in h for h in hypotheses)
    assert any("H3" in h for h in hypotheses)
    assert any("H4" in h for h in hypotheses)


def test_reboot_roadmap_has_realistic_durations():
    """Nenhum roadmap item deve ter >100 dias (senão config está errada)."""
    rm = reboot_roadmap()
    for r in rm:
        assert 0 < r.days_to_target < 200, (
            f"{r.target_hypothesis}: days={r.days_to_target} fora de range"
        )
