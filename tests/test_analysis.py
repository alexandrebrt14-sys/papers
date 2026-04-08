"""Tests for statistical analysis module."""

import math
import random

import numpy as np

from src.analysis.statistical import StatisticalAnalyzer


class TestStatisticalAnalyzer:
    def setup_method(self):
        self.analyzer = StatisticalAnalyzer()

    # ------------------------------------------------------------------
    # Existing tests (originals)
    # ------------------------------------------------------------------

    def test_chi_squared_significant(self):
        # Group A: 80% citation rate, Group B: 20%
        group_a = [True] * 80 + [False] * 20
        group_b = [True] * 20 + [False] * 80
        result = self.analyzer.chi_squared_citation_rate(group_a, group_b)
        assert result.significant == True
        assert result.p_value < 0.001
        assert "chi-squared" in result.test_name  # Nao deve cair em Fisher

    def test_chi_squared_not_significant(self):
        group_a = [True] * 50 + [False] * 50
        group_b = [True] * 48 + [False] * 52
        result = self.analyzer.chi_squared_citation_rate(group_a, group_b)
        assert result.significant == False

    def test_chi_squared_falls_back_to_fisher_when_expected_low(self):
        # 2x2 com expected counts < 5: precisa cair em Fisher exact
        group_a = [True] * 2 + [False] * 3
        group_b = [True] * 0 + [False] * 4
        result = self.analyzer.chi_squared_citation_rate(group_a, group_b)
        assert result.test_name.startswith("fisher-exact")
        assert 0.0 <= result.p_value <= 1.0

    def test_t_test(self):
        group_a = [1.0, 1.5, 2.0, 1.8, 1.2]
        group_b = [3.0, 3.5, 4.0, 3.8, 3.2]
        result = self.analyzer.t_test_means(group_a, group_b)
        assert result.significant == True

    def test_correlation_strong(self):
        x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        y = [2, 4, 5, 8, 10, 12, 14, 15, 18, 20]
        result = self.analyzer.correlation(x, y)
        assert result.strength == "strong"
        assert result.significant == True

    def test_anova_between_groups(self):
        data = {
            "ChatGPT": [0.8, 0.7, 0.9, 0.85, 0.75],
            "Claude": [0.3, 0.2, 0.4, 0.35, 0.25],
            "Gemini": [0.5, 0.6, 0.4, 0.55, 0.45],
        }
        result = self.analyzer.anova_between_groups(data)
        assert result.significant == True

    def test_bonferroni(self):
        p_values = [0.01, 0.03, 0.04, 0.10]
        corrected = self.analyzer.bonferroni_correction(p_values)
        assert corrected[0]["significant"] is True  # 0.01 * 4 = 0.04 < 0.05
        assert corrected[3]["significant"] is False  # 0.10 * 4 = 0.40 > 0.05

    def test_fdr_correction_less_conservative(self):
        # BH deve ser mais permissivo que Bonferroni para uma serie crescente
        p_values = [0.001, 0.01, 0.03, 0.04, 0.05]
        bh = self.analyzer.fdr_correction(p_values, alpha=0.05)
        bonf = self.analyzer.bonferroni_correction(p_values)
        # BH rejeita pelo menos tantos quanto Bonferroni
        assert sum(b["significant"] for b in bh) >= sum(b["significant"] for b in bonf)

    # ------------------------------------------------------------------
    # New: Bootstrap BCa
    # ------------------------------------------------------------------

    def test_bootstrap_bca_proportion_recovers_truth(self):
        rng = np.random.default_rng(7)
        true_p = 0.30
        sample = rng.binomial(1, true_p, 500).tolist()
        ci = self.analyzer.bootstrap_ci_bca(sample, "mean", n_resamples=2000)
        assert ci.method == "bootstrap_bca"
        assert ci.ci_lower < ci.point_estimate < ci.ci_upper
        assert ci.ci_lower < true_p < ci.ci_upper  # CI cobre a verdade
        assert 0.0 <= ci.ci_lower <= 1.0
        assert 0.0 <= ci.ci_upper <= 1.0
        assert "bias_z0" in ci.extras
        assert "acceleration" in ci.extras

    def test_bootstrap_bca_mean_close_to_normal_ci(self):
        rng = np.random.default_rng(11)
        sample = rng.normal(10.0, 2.0, 200).tolist()
        ci = self.analyzer.bootstrap_ci_bca(sample, "mean", n_resamples=2000)
        # Para normal grande, BCa deve estar perto do CI normal
        sem = 2.0 / math.sqrt(200)
        normal_lo = 10.0 - 1.96 * sem
        normal_hi = 10.0 + 1.96 * sem
        # Toleramos diferenca de 0.5 SEM
        assert abs(ci.ci_lower - normal_lo) < 0.5
        assert abs(ci.ci_upper - normal_hi) < 0.5

    def test_bootstrap_bca_rejects_too_small(self):
        try:
            self.analyzer.bootstrap_ci_bca([1.0])
            raised = False
        except ValueError:
            raised = True
        assert raised

    # ------------------------------------------------------------------
    # New: Beta-binomial bayesiano
    # ------------------------------------------------------------------

    def test_beta_binomial_basic(self):
        ci = self.analyzer.beta_binomial_ci(60, 200)
        assert ci.method == "beta_binomial"
        # Posterior mean = (1+60)/(1+1+200) = 61/202 ~ 0.302
        assert abs(ci.point_estimate - 61 / 202) < 1e-9
        assert ci.ci_lower < 0.30 < ci.ci_upper

    def test_beta_binomial_handles_zero_successes(self):
        # k=0/n=10: posterior Beta(1, 11), mean = 1/12 ~ 0.083
        ci = self.analyzer.beta_binomial_ci(0, 10)
        assert ci.ci_lower >= 0.0
        assert ci.ci_upper > 0.0
        assert ci.point_estimate > 0.0  # Bayesiano nao colapsa em 0

    def test_beta_binomial_handles_full(self):
        ci = self.analyzer.beta_binomial_ci(10, 10)
        assert ci.ci_upper <= 1.0
        assert ci.point_estimate < 1.0  # Bayesiano nao colapsa em 1

    def test_beta_binomial_rejects_invalid(self):
        try:
            self.analyzer.beta_binomial_ci(11, 10)
            raised = False
        except ValueError:
            raised = True
        assert raised

    # ------------------------------------------------------------------
    # New: Cohen's kappa
    # ------------------------------------------------------------------

    def test_cohen_kappa_perfect(self):
        a = ["yes"] * 50 + ["no"] * 50
        b = list(a)
        k = self.analyzer.cohen_kappa(a, b)
        assert k.kappa == 1.0
        assert k.interpretation == "quase perfeito"

    def test_cohen_kappa_chance_level(self):
        random.seed(7)
        a = [random.choice(["yes", "no"]) for _ in range(500)]
        b = [random.choice(["yes", "no"]) for _ in range(500)]
        k = self.analyzer.cohen_kappa(a, b)
        # Kappa deve estar perto de zero (acordo so por chance)
        assert abs(k.kappa) < 0.15

    def test_cohen_kappa_substantial(self):
        random.seed(11)
        a = [random.choice(["yes", "no"]) for _ in range(200)]
        # 85% concordancia
        b = [x if random.random() < 0.85 else ("no" if x == "yes" else "yes") for x in a]
        k = self.analyzer.cohen_kappa(a, b)
        assert 0.55 < k.kappa < 0.85
        assert k.interpretation in ("moderado", "substancial")

    # ------------------------------------------------------------------
    # New: Fleiss' kappa
    # ------------------------------------------------------------------

    def test_fleiss_kappa_perfect(self):
        # Todos os raters concordam em todos os sujeitos
        ratings = [["yes"] * 4 for _ in range(30)]
        ratings += [["no"] * 4 for _ in range(30)]
        fk = self.analyzer.fleiss_kappa(ratings)
        assert fk.kappa == 1.0
        assert fk.n_raters == 4
        assert fk.n_subjects == 60

    def test_fleiss_kappa_chance(self):
        random.seed(13)
        ratings = [[random.choice(["yes", "no"]) for _ in range(4)] for _ in range(200)]
        fk = self.analyzer.fleiss_kappa(ratings)
        assert abs(fk.kappa) < 0.15

    def test_fleiss_kappa_rejects_inconsistent(self):
        try:
            self.analyzer.fleiss_kappa([["a", "b"], ["a", "b", "c"]])
            raised = False
        except ValueError:
            raised = True
        assert raised

    # ------------------------------------------------------------------
    # New: Brier score
    # ------------------------------------------------------------------

    def test_brier_perfect_predictor(self):
        outcomes = [1, 0, 1, 0, 1, 0]
        # Predicoes perfeitas
        probs = [1.0, 0.0, 1.0, 0.0, 1.0, 0.0]
        b = self.analyzer.brier_score(probs, outcomes)
        assert b["brier_score"] == 0.0

    def test_brier_random_predictor(self):
        # Predicao constante 0.5 contra base rate 0.5: BS = 0.25
        outcomes = [1, 0] * 100
        probs = [0.5] * 200
        b = self.analyzer.brier_score(probs, outcomes)
        assert abs(b["brier_score"] - 0.25) < 0.01

    def test_brier_decomposition_sums(self):
        rng = np.random.default_rng(7)
        outcomes = rng.binomial(1, 0.4, 500)
        probs = np.clip(rng.beta(2, 3, 500), 0, 1)
        b = self.analyzer.brier_score(probs.tolist(), outcomes.tolist())
        # rel - res + unc deve ser proximo de bs (Murphy decomposition)
        approx = b["reliability"] - b["resolution"] + b["uncertainty"]
        assert abs(approx - b["brier_score"]) < 0.05

    def test_reliability_diagram_bins(self):
        rng = np.random.default_rng(7)
        probs = rng.uniform(0, 1, 200)
        outcomes = rng.binomial(1, probs)
        diag = self.analyzer.reliability_diagram(probs.tolist(), outcomes.tolist(), n_bins=10)
        # Pelo menos alguns bins ocupados
        assert len(diag) >= 5
        # Todos com chaves esperadas
        for d in diag:
            assert "predicted_mean" in d and "observed_mean" in d and "n" in d
