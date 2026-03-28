"""Module 6: Statistical Analysis Module.

Significance tests, correlation, regression, and publishable visualizations
for GEO research data.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd
from scipy import stats

logger = logging.getLogger(__name__)


@dataclass
class SignificanceResult:
    """Result of a significance test."""
    test_name: str
    statistic: float
    p_value: float
    significant: bool  # p < 0.05
    effect_size: float | None = None
    interpretation: str = ""


@dataclass
class CorrelationResult:
    """Result of a correlation analysis."""
    method: str  # pearson or spearman
    variables: tuple[str, str]
    coefficient: float
    p_value: float
    significant: bool
    strength: str  # strong, moderate, weak, negligible


@dataclass
class RegressionResult:
    """Result of a regression analysis."""
    dependent_var: str
    independent_vars: list[str]
    coefficients: dict[str, float]
    r_squared: float
    adj_r_squared: float
    f_statistic: float
    f_p_value: float
    significant_predictors: list[str]


class StatisticalAnalyzer:
    """Statistical analysis toolkit for GEO research."""

    def chi_squared_citation_rate(
        self, group_a: list[bool], group_b: list[bool],
        label_a: str = "experimental", label_b: str = "control",
    ) -> SignificanceResult:
        """Chi-squared test comparing citation rates between two groups.

        Use case: is the citation rate significantly different between
        our optimized content and non-optimized content?
        """
        table = np.array([
            [sum(group_a), len(group_a) - sum(group_a)],
            [sum(group_b), len(group_b) - sum(group_b)],
        ])
        chi2, p, dof, expected = stats.chi2_contingency(table)

        # Effect size (Cramér's V)
        n = table.sum()
        v = np.sqrt(chi2 / (n * (min(table.shape) - 1)))

        rate_a = sum(group_a) / max(len(group_a), 1)
        rate_b = sum(group_b) / max(len(group_b), 1)

        return SignificanceResult(
            test_name="chi-squared",
            statistic=round(chi2, 4),
            p_value=round(p, 6),
            significant=p < 0.05,
            effect_size=round(v, 4),
            interpretation=(
                f"Taxa de citação {label_a}: {rate_a:.1%} vs {label_b}: {rate_b:.1%}. "
                f"{'Diferença significativa' if p < 0.05 else 'Sem diferença significativa'} "
                f"(χ²={chi2:.2f}, p={p:.4f}, V de Cramér={v:.3f})."
            ),
        )

    def t_test_means(
        self, group_a: list[float], group_b: list[float],
        label_a: str = "pre", label_b: str = "post", paired: bool = False,
    ) -> SignificanceResult:
        """T-test comparing means between two groups.

        Use case: did the citation position improve after intervention?
        """
        if paired:
            stat, p = stats.ttest_rel(group_a, group_b)
        else:
            stat, p = stats.ttest_ind(group_a, group_b)

        # Cohen's d with Bessel's correction (ddof=1) for unbiased sample std
        pooled_std = np.sqrt((np.std(group_a, ddof=1) ** 2 + np.std(group_b, ddof=1) ** 2) / 2)
        d = (np.mean(group_a) - np.mean(group_b)) / max(pooled_std, 1e-10)

        return SignificanceResult(
            test_name="t-test (paired)" if paired else "t-test (independent)",
            statistic=round(stat, 4),
            p_value=round(p, 6),
            significant=p < 0.05,
            effect_size=round(d, 4),
            interpretation=(
                f"Média {label_a}: {np.mean(group_a):.3f} vs {label_b}: {np.mean(group_b):.3f}. "
                f"{'Diferença significativa' if p < 0.05 else 'Sem diferença significativa'} "
                f"(t={stat:.2f}, p={p:.4f}, d de Cohen={d:.3f})."
            ),
        )

    def correlation(
        self, x: list[float], y: list[float],
        x_name: str = "x", y_name: str = "y",
        method: str = "spearman",
    ) -> CorrelationResult:
        """Correlation analysis between two variables.

        Use case: is Entity Consistency Score correlated with Citation Rate?
        """
        if method == "pearson":
            r, p = stats.pearsonr(x, y)
        else:
            r, p = stats.spearmanr(x, y)

        abs_r = abs(r)
        if abs_r >= 0.7:
            strength = "strong"
        elif abs_r >= 0.4:
            strength = "moderate"
        elif abs_r >= 0.2:
            strength = "weak"
        else:
            strength = "negligible"

        return CorrelationResult(
            method=method,
            variables=(x_name, y_name),
            coefficient=round(r, 4),
            p_value=round(p, 6),
            significant=p < 0.05,
            strength=strength,
        )

    def logistic_regression_predictors(
        self, df: pd.DataFrame, target: str, predictors: list[str],
    ) -> dict[str, Any]:
        """Logistic regression to identify citation predictors.

        Use case: which factors (schema types, word count, academic references,
        Wikidata statements) predict whether an entity is cited?
        """
        try:
            from statsmodels.discrete.discrete_model import Logit
            import statsmodels.api as sm

            X = sm.add_constant(df[predictors].astype(float))
            y = df[target].astype(float)

            model = Logit(y, X).fit(disp=0)

            significant = [
                pred for pred, p in zip(predictors, model.pvalues[1:])
                if p < 0.05
            ]

            return {
                "converged": True,
                "pseudo_r_squared": round(model.prsquared, 4),
                "llr_p_value": round(model.llr_pvalue, 6),
                "coefficients": {
                    pred: {
                        "coef": round(model.params[i + 1], 4),
                        "p_value": round(model.pvalues[i + 1], 6),
                        "odds_ratio": round(np.exp(model.params[i + 1]), 4),
                        "significant": model.pvalues[i + 1] < 0.05,
                    }
                    for i, pred in enumerate(predictors)
                },
                "significant_predictors": significant,
                "n_observations": len(df),
                "aic": round(model.aic, 2),
                "bic": round(model.bic, 2),
            }
        except Exception as e:
            logger.error(f"Logistic regression failed: {e}")
            return {"converged": False, "error": str(e)}

    def anova_between_groups(
        self, data: dict[str, list[float]],
    ) -> SignificanceResult:
        """One-way ANOVA for independent groups.

        Use case: compare citation rates between different entity categories
        (e.g., fintech vs GEO vs SaaS competitors).

        Automatically checks homogeneity of variance (Levene's test).
        Falls back to Kruskal-Wallis if assumptions violated.
        """
        groups = list(data.values())
        group_names = list(data.keys())

        # Check homogeneity of variance (Levene's test)
        levene_stat, levene_p = stats.levene(*groups)
        homogeneous = levene_p > 0.05

        if homogeneous:
            stat, p = stats.f_oneway(*groups)
            test_used = "ANOVA (one-way)"
        else:
            # Use non-parametric alternative when variance is not homogeneous
            stat, p = stats.kruskal(*groups)
            test_used = "Kruskal-Wallis (non-parametric, Levene p={:.4f})".format(levene_p)
            logger.warning(f"Variance not homogeneous (Levene p={levene_p:.4f}), using Kruskal-Wallis")

        # Eta-squared
        grand_mean = np.mean([v for group in groups for v in group])
        ss_between = sum(len(g) * (np.mean(g) - grand_mean) ** 2 for g in groups)
        ss_total = sum((v - grand_mean) ** 2 for g in groups for v in g)
        eta_sq = ss_between / max(ss_total, 1e-10)

        return SignificanceResult(
            test_name=test_used,
            statistic=round(stat, 4),
            p_value=round(p, 6),
            significant=p < 0.05,
            effect_size=round(eta_sq, 4),
            interpretation=(
                f"Comparação entre {len(data)} grupos ({', '.join(group_names)}). "
                f"{'Diferença significativa' if p < 0.05 else 'Sem diferença significativa'} "
                f"({test_used}: stat={stat:.2f}, p={p:.4f}, eta2={eta_sq:.3f})."
            ),
        )

    def mann_whitney_position(
        self, group_a: list[float], group_b: list[float],
        label_a: str = "pre", label_b: str = "post",
    ) -> SignificanceResult:
        """Mann-Whitney U test for ordinal/non-normal data.

        Use case: compare citation POSITION (ordinal: 1, 2, 3) between groups.
        Position data is ordinal and non-normal — t-test assumptions are violated.
        Mann-Whitney is the correct non-parametric alternative.
        """
        stat, p = stats.mannwhitneyu(group_a, group_b, alternative='two-sided')

        # Effect size: rank-biserial correlation
        n1, n2 = len(group_a), len(group_b)
        r = 1 - (2 * stat) / (n1 * n2)

        return SignificanceResult(
            test_name="Mann-Whitney U",
            statistic=round(stat, 4),
            p_value=round(p, 6),
            significant=p < 0.05,
            effect_size=round(r, 4),
            interpretation=(
                f"Mediana {label_a}: {np.median(group_a):.1f} vs {label_b}: {np.median(group_b):.1f}. "
                f"{'Diferença significativa' if p < 0.05 else 'Sem diferença significativa'} "
                f"(U={stat:.0f}, p={p:.4f}, r={r:.3f})."
            ),
        )

    def bonferroni_correction(self, p_values: list[float]) -> list[dict[str, Any]]:
        """Apply Bonferroni correction for multiple comparisons."""
        n = len(p_values)
        return [
            {
                "original_p": round(p, 6),
                "corrected_p": round(min(p * n, 1.0), 6),
                "significant": min(p * n, 1.0) < 0.05,
            }
            for p in p_values
        ]

    def fdr_correction(self, p_values: list[float], alpha: float = 0.05) -> list[dict[str, Any]]:
        """Apply Benjamini-Hochberg FDR correction for multiple comparisons.

        Less conservative than Bonferroni — controls false discovery rate
        rather than family-wise error rate. Preferred when testing many
        hypotheses simultaneously (e.g., per-entity citation significance).
        """
        n = len(p_values)
        sorted_indices = sorted(range(n), key=lambda i: p_values[i])
        results: list[dict[str, Any] | None] = [None] * n
        for rank, idx in enumerate(sorted_indices, 1):
            threshold = (rank / n) * alpha
            results[idx] = {
                "original_p": round(p_values[idx], 6),
                "rank": rank,
                "bh_threshold": round(threshold, 6),
                "significant": p_values[idx] <= threshold,
            }
        return results  # type: ignore[return-value]

    def generate_summary_report(
        self, citation_data: pd.DataFrame,
    ) -> dict[str, Any]:
        """Generate a comprehensive statistical summary for publication.

        Args:
            citation_data: DataFrame with columns: llm, query_category, cited, position, etc.
        """
        report: dict[str, Any] = {}

        # Overall citation rate
        overall_rate = citation_data["cited"].mean()
        report["overall_citation_rate"] = round(overall_rate, 3)
        report["total_observations"] = len(citation_data)

        # By LLM
        by_llm = citation_data.groupby("llm")["cited"].agg(["mean", "count", "sum"])
        report["by_llm"] = {
            llm: {"rate": round(row["mean"], 3), "n": int(row["count"]), "cited": int(row["sum"])}
            for llm, row in by_llm.iterrows()
        }

        # By query category
        by_cat = citation_data.groupby("query_category")["cited"].agg(["mean", "count"])
        report["by_category"] = {
            cat: {"rate": round(row["mean"], 3), "n": int(row["count"])}
            for cat, row in by_cat.iterrows()
        }

        # ANOVA across LLMs
        llm_groups = {
            llm: group["cited"].astype(float).tolist()
            for llm, group in citation_data.groupby("llm")
        }
        if len(llm_groups) >= 2:
            report["anova_llms"] = self.anova_between_groups(llm_groups).__dict__

        return report
