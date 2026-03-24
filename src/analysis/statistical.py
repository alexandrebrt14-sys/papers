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

        # Cohen's d
        pooled_std = np.sqrt((np.std(group_a) ** 2 + np.std(group_b) ** 2) / 2)
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

    def anova_repeated_measures(
        self, data: dict[str, list[float]],
    ) -> SignificanceResult:
        """One-way ANOVA for comparing citation rates across LLMs.

        Use case: do different LLMs cite at significantly different rates?
        """
        groups = list(data.values())
        stat, p = stats.f_oneway(*groups)

        # Eta-squared
        grand_mean = np.mean([v for group in groups for v in group])
        ss_between = sum(len(g) * (np.mean(g) - grand_mean) ** 2 for g in groups)
        ss_total = sum((v - grand_mean) ** 2 for g in groups for v in g)
        eta_sq = ss_between / max(ss_total, 1e-10)

        return SignificanceResult(
            test_name="ANOVA (one-way)",
            statistic=round(stat, 4),
            p_value=round(p, 6),
            significant=p < 0.05,
            effect_size=round(eta_sq, 4),
            interpretation=(
                f"Comparação entre {len(data)} grupos (LLMs). "
                f"{'Diferença significativa' if p < 0.05 else 'Sem diferença significativa'} "
                f"(F={stat:.2f}, p={p:.4f}, η²={eta_sq:.3f})."
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
            report["anova_llms"] = self.anova_repeated_measures(llm_groups).__dict__

        return report
