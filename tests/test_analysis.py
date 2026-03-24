"""Tests for statistical analysis module."""

from src.analysis.statistical import StatisticalAnalyzer


class TestStatisticalAnalyzer:
    def setup_method(self):
        self.analyzer = StatisticalAnalyzer()

    def test_chi_squared_significant(self):
        # Group A: 80% citation rate, Group B: 20%
        group_a = [True] * 80 + [False] * 20
        group_b = [True] * 20 + [False] * 80
        result = self.analyzer.chi_squared_citation_rate(group_a, group_b)
        assert result.significant is True
        assert result.p_value < 0.001

    def test_chi_squared_not_significant(self):
        # Both groups similar
        group_a = [True] * 50 + [False] * 50
        group_b = [True] * 48 + [False] * 52
        result = self.analyzer.chi_squared_citation_rate(group_a, group_b)
        assert result.significant is False

    def test_t_test(self):
        group_a = [1.0, 1.5, 2.0, 1.8, 1.2]
        group_b = [3.0, 3.5, 4.0, 3.8, 3.2]
        result = self.analyzer.t_test_means(group_a, group_b)
        assert result.significant is True

    def test_correlation_strong(self):
        x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        y = [2, 4, 5, 8, 10, 12, 14, 15, 18, 20]
        result = self.analyzer.correlation(x, y)
        assert result.strength == "strong"
        assert result.significant is True

    def test_anova(self):
        data = {
            "ChatGPT": [0.8, 0.7, 0.9, 0.85, 0.75],
            "Claude": [0.3, 0.2, 0.4, 0.35, 0.25],
            "Gemini": [0.5, 0.6, 0.4, 0.55, 0.45],
        }
        result = self.analyzer.anova_repeated_measures(data)
        assert result.significant is True

    def test_bonferroni(self):
        p_values = [0.01, 0.03, 0.04, 0.10]
        corrected = self.analyzer.bonferroni_correction(p_values)
        assert corrected[0]["significant"] is True  # 0.01 * 4 = 0.04 < 0.05
        assert corrected[3]["significant"] is False  # 0.10 * 4 = 0.40 > 0.05
