"""Module 6: Statistical Analysis Module.

Significance tests, correlation, regression, bootstrap, bayesian intervals,
inter-rater reliability and publishable visualizations for GEO research data.

Reference: docs/METHODOLOGY.md (sections 5, 6 and 10).
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Sequence

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
class IntervalResult:
    """Result of an interval estimation (bootstrap or bayesian credible interval)."""
    method: str               # "bootstrap_bca", "beta_binomial", ...
    point_estimate: float
    ci_lower: float
    ci_upper: float
    confidence: float         # e.g. 0.95
    n: int
    extras: dict[str, Any] = field(default_factory=dict)


@dataclass
class AgreementResult:
    """Inter-rater reliability result (Cohen / Fleiss kappa)."""
    method: str               # "cohen_kappa", "fleiss_kappa"
    kappa: float
    n_raters: int
    n_subjects: int
    interpretation: str       # Landis-Koch label
    extras: dict[str, Any] = field(default_factory=dict)


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
        """Chi-squared (or Fisher exact) test comparing two citation rates.

        Use case: is the citation rate significantly different between
        our optimized content and non-optimized content?

        Pressuposto do qui-quadrado: todas as frequencias esperadas E_ij >= 5.
        Quando esse pressuposto e violado, a aproximacao chi2 fica invalida e o
        teste cai automaticamente para o teste exato de Fisher (scipy.stats.fisher_exact),
        que enumera a distribuicao hipergeometrica e nao depende de aproximacoes
        assintoticas.
        """
        table = np.array([
            [sum(group_a), len(group_a) - sum(group_a)],
            [sum(group_b), len(group_b) - sum(group_b)],
        ])

        # Pre-checagem: expected counts via marginais
        chi2, p, dof, expected = stats.chi2_contingency(table)
        min_expected = float(np.min(expected))

        used_test = "chi-squared"
        if min_expected < 5.0:
            # Fallback Fisher exact: valido para qualquer N, sem pressuposto assintotico.
            try:
                _, p_fisher = stats.fisher_exact(table, alternative="two-sided")
                p = p_fisher
                used_test = f"fisher-exact (E_min={min_expected:.2f} < 5)"
                logger.info(
                    "Chi-squared assumption violated (min_expected=%.2f<5), "
                    "fell back to Fisher exact test.", min_expected,
                )
            except Exception as exc:
                logger.warning("Fisher exact fallback failed: %s", exc)

        # Effect size (Cramér's V) — vale para ambos os testes em 2x2
        n = table.sum()
        v = float(np.sqrt(chi2 / (n * (min(table.shape) - 1))))

        rate_a = sum(group_a) / max(len(group_a), 1)
        rate_b = sum(group_b) / max(len(group_b), 1)

        return SignificanceResult(
            test_name=used_test,
            statistic=round(float(chi2), 4),
            p_value=round(float(p), 6),
            significant=p < 0.05,
            effect_size=round(v, 4),
            interpretation=(
                f"Taxa de citação {label_a}: {rate_a:.1%} vs {label_b}: {rate_b:.1%}. "
                f"{'Diferença significativa' if p < 0.05 else 'Sem diferença significativa'} "
                f"({used_test}: χ²={chi2:.2f}, p={p:.4f}, V de Cramér={v:.3f})."
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

    # ------------------------------------------------------------------
    # Interval estimation
    # ------------------------------------------------------------------

    def bootstrap_ci_bca(
        self,
        sample: Sequence[float],
        statistic: str | callable = "mean",
        n_resamples: int = 10_000,
        confidence: float = 0.95,
        seed: int | None = 42,
    ) -> IntervalResult:
        """Bias-Corrected and accelerated (BCa) bootstrap CI (Efron, 1987).

        BCa corrige duas patologias do percentile bootstrap:
          1. vies (bias correction term z0): a mediana da distribuicao bootstrap
             pode nao coincidir com o ponto observado;
          2. assimetria (acceleration term a): variabilidade da estatistica varia
             ao longo da distribuicao subjacente, estimada via jackknife.

        Formulacao:
            z0 = Phi^-1( P(theta_b < theta_obs) )
            a  = sum( (theta_bar - theta_(i))^3 ) / ( 6 * (sum(...^2))^(3/2) )
            alpha1 = Phi( z0 + (z0 + z_{a/2}) / (1 - a*(z0 + z_{a/2})) )
            alpha2 = Phi( z0 + (z0 + z_{1-a/2}) / (1 - a*(z0 + z_{1-a/2})) )
            CI = [F^-1_boot(alpha1), F^-1_boot(alpha2)]

        Args:
            sample: amostra unidimensional.
            statistic: "mean", "median", "proportion" ou callable arbitraria.
            n_resamples: B (default 10_000 para 95% CI estavel).
            confidence: nivel de confianca (default 0.95).
            seed: para reprodutibilidade.

        Returns:
            IntervalResult com extras["bias_z0"] e extras["acceleration"].
        """
        arr = np.asarray(list(sample), dtype=float)
        n = arr.size
        if n < 2:
            raise ValueError("BCa exige n >= 2")

        if isinstance(statistic, str):
            stat_funcs = {
                "mean": np.mean,
                "median": np.median,
                "proportion": np.mean,  # binario {0,1}
            }
            if statistic not in stat_funcs:
                raise ValueError(f"statistic '{statistic}' nao suportada")
            stat_fn = stat_funcs[statistic]
            stat_name = statistic
        else:
            stat_fn = statistic
            stat_name = getattr(statistic, "__name__", "callable")

        observed = float(stat_fn(arr))

        rng = np.random.default_rng(seed)
        boot = np.empty(n_resamples, dtype=float)
        # vetorizado: amostra n_resamples x n indices
        idx = rng.integers(0, n, size=(n_resamples, n))
        for b in range(n_resamples):
            boot[b] = stat_fn(arr[idx[b]])

        # Bias correction
        prop_below = float(np.mean(boot < observed))
        # Clipping para evitar -inf/inf em ppf
        prop_below = float(np.clip(prop_below, 1e-9, 1 - 1e-9))
        z0 = stats.norm.ppf(prop_below)

        # Acceleration via jackknife
        jack = np.empty(n, dtype=float)
        mask_full = np.ones(n, dtype=bool)
        for i in range(n):
            mask_full[i] = False
            jack[i] = stat_fn(arr[mask_full])
            mask_full[i] = True
        jack_mean = float(np.mean(jack))
        diffs = jack_mean - jack
        denom = 6.0 * float(np.sum(diffs ** 2)) ** 1.5
        accel = float(np.sum(diffs ** 3) / denom) if denom > 1e-15 else 0.0

        alpha = 1.0 - confidence
        z_lo = stats.norm.ppf(alpha / 2)
        z_hi = stats.norm.ppf(1 - alpha / 2)

        def adjust(z):
            num = z0 + (z0 + z)
            den = 1.0 - accel * (z0 + z)
            if abs(den) < 1e-12:
                den = 1e-12 if den >= 0 else -1e-12
            return float(stats.norm.cdf(z0 + num / den))

        a1 = adjust(z_lo)
        a2 = adjust(z_hi)
        a1 = float(np.clip(a1, 0.0, 1.0))
        a2 = float(np.clip(a2, 0.0, 1.0))

        ci_lower = float(np.quantile(boot, a1))
        ci_upper = float(np.quantile(boot, a2))

        return IntervalResult(
            method="bootstrap_bca",
            point_estimate=observed,
            ci_lower=ci_lower,
            ci_upper=ci_upper,
            confidence=confidence,
            n=int(n),
            extras={
                "statistic": stat_name,
                "n_resamples": int(n_resamples),
                "bias_z0": round(float(z0), 6),
                "acceleration": round(accel, 6),
                "alpha_lower": round(a1, 6),
                "alpha_upper": round(a2, 6),
            },
        )

    def beta_binomial_ci(
        self,
        cited: int,
        n: int,
        prior_alpha: float = 1.0,
        prior_beta: float = 1.0,
        confidence: float = 0.95,
    ) -> IntervalResult:
        """Bayesian credible interval for a citation rate via Beta conjugacy.

        Modelo:
            theta ~ Beta(prior_alpha, prior_beta)
            k | theta ~ Binomial(n, theta)
            theta | k ~ Beta(prior_alpha + k, prior_beta + n - k)

        Defaults Beta(1, 1) (uniforme, equivalente a Laplace's rule of succession).
        Beta(0.5, 0.5) (Jeffreys) tambem e razoavel e mais conservador para
        amostras pequenas.

        Vantagens versus Wald (1.96 * SE):
          - sempre dentro de [0, 1]
          - bem comportado para k=0 e k=n
          - direto e interpretavel ("ha 95% de probabilidade de theta estar em ...").
        """
        if n < 0 or cited < 0 or cited > n:
            raise ValueError(f"argumentos invalidos: cited={cited}, n={n}")
        if prior_alpha <= 0 or prior_beta <= 0:
            raise ValueError("priors devem ser > 0")

        a_post = prior_alpha + cited
        b_post = prior_beta + (n - cited)
        alpha = 1.0 - confidence
        ci_lower = float(stats.beta.ppf(alpha / 2, a_post, b_post))
        ci_upper = float(stats.beta.ppf(1 - alpha / 2, a_post, b_post))
        # Posterior mean (estimador bayesiano natural; difere da MLE k/n)
        post_mean = float(a_post / (a_post + b_post))

        return IntervalResult(
            method="beta_binomial",
            point_estimate=post_mean,
            ci_lower=ci_lower,
            ci_upper=ci_upper,
            confidence=confidence,
            n=int(n),
            extras={
                "prior_alpha": prior_alpha,
                "prior_beta": prior_beta,
                "posterior_alpha": float(a_post),
                "posterior_beta": float(b_post),
                "mle": float(cited / n) if n > 0 else 0.0,
                "cited": int(cited),
            },
        )

    # ------------------------------------------------------------------
    # Inter-rater reliability
    # ------------------------------------------------------------------

    @staticmethod
    def _kappa_label(k: float) -> str:
        """Landis & Koch (1977) labels."""
        if k < 0:
            return "pior que acaso"
        if k < 0.20:
            return "leve"
        if k < 0.40:
            return "razoavel"
        if k < 0.60:
            return "moderado"
        if k < 0.80:
            return "substancial"
        return "quase perfeito"

    def cohen_kappa(
        self,
        rater_a: Sequence[Any],
        rater_b: Sequence[Any],
    ) -> AgreementResult:
        """Cohen's kappa for two raters and nominal categories.

            kappa = (p_o - p_e) / (1 - p_e)

        onde p_o e a concordancia observada e p_e e a esperada por sorteio
        independente das marginais. Corrige o "agreement bruto" para o que e
        esperado por chance — diferenca crucial em classes desbalanceadas.
        """
        a = np.asarray(list(rater_a))
        b = np.asarray(list(rater_b))
        if a.shape != b.shape or a.size == 0:
            raise ValueError("rater_a e rater_b devem ter mesmo tamanho > 0")
        n = a.size
        labels = sorted(set(a.tolist()) | set(b.tolist()))
        p_o = float(np.mean(a == b))
        p_e = 0.0
        for lbl in labels:
            p_e += (np.mean(a == lbl) * np.mean(b == lbl))
        denom = 1.0 - p_e
        kappa = float((p_o - p_e) / denom) if denom > 1e-12 else 1.0

        return AgreementResult(
            method="cohen_kappa",
            kappa=round(kappa, 4),
            n_raters=2,
            n_subjects=int(n),
            interpretation=self._kappa_label(kappa),
            extras={
                "p_observed": round(p_o, 4),
                "p_expected": round(p_e, 4),
                "categories": list(map(str, labels)),
            },
        )

    def fleiss_kappa(
        self,
        ratings: Sequence[Sequence[Any]],
    ) -> AgreementResult:
        """Fleiss' kappa for multiple raters and nominal categories.

        Input: matriz N x R (N sujeitos, R raters por sujeito), entradas
        sao rotulos categoricos (ex.: True/False ou strings). Os raters NAO
        precisam ser os mesmos por linha (so o numero de avaliacoes por sujeito).

        Formulacao:
            P_i  = (1/(R(R-1))) * (sum_j n_ij^2 - R)        # acordo no sujeito i
            P_bar = mean(P_i)                                # acordo medio
            p_j  = sum_i n_ij / (N R)                        # marginal categoria j
            P_e  = sum_j p_j^2                               # acordo esperado
            kappa = (P_bar - P_e) / (1 - P_e)
        """
        rows = [list(r) for r in ratings]
        if not rows:
            raise ValueError("ratings vazio")
        n = len(rows)
        r = len(rows[0])
        if r < 2:
            raise ValueError("Fleiss exige >= 2 raters por sujeito")
        if any(len(row) != r for row in rows):
            raise ValueError("Numero de avaliacoes por sujeito deve ser constante")

        labels = sorted({lbl for row in rows for lbl in row})
        # Matriz de contagem N x K
        K = len(labels)
        idx = {lbl: i for i, lbl in enumerate(labels)}
        counts = np.zeros((n, K), dtype=float)
        for i, row in enumerate(rows):
            for lbl in row:
                counts[i, idx[lbl]] += 1

        # P_i por sujeito
        P_i = (counts ** 2).sum(axis=1) - r
        P_i = P_i / (r * (r - 1))
        P_bar = float(P_i.mean())
        # Marginais por categoria
        p_j = counts.sum(axis=0) / (n * r)
        P_e = float((p_j ** 2).sum())
        denom = 1.0 - P_e
        kappa = float((P_bar - P_e) / denom) if denom > 1e-12 else 1.0

        return AgreementResult(
            method="fleiss_kappa",
            kappa=round(kappa, 4),
            n_raters=int(r),
            n_subjects=int(n),
            interpretation=self._kappa_label(kappa),
            extras={
                "P_observed": round(P_bar, 4),
                "P_expected": round(P_e, 4),
                "marginals": {lbl: round(float(p_j[idx[lbl]]), 4) for lbl in labels},
            },
        )

    # ------------------------------------------------------------------
    # Calibration metrics for predictive scores
    # ------------------------------------------------------------------

    def brier_score(
        self,
        probabilities: Sequence[float],
        outcomes: Sequence[int],
    ) -> dict[str, Any]:
        """Brier score and decomposition for binary probabilistic predictions.

        BS = (1/N) sum (p_i - y_i)^2  in [0, 1]; menor e melhor.

        Decomposicao Murphy (1973):
            BS = reliability - resolution + uncertainty
              reliability  = E[(p - P(y=1|p))^2]   # quanto p mente
              resolution   = E[(P(y=1|p) - p_bar)^2]  # quanto p discrimina
              uncertainty  = p_bar * (1 - p_bar)   # variancia base

        Util para calibracao do GEO Score Checker (probabilidade de citacao
        prevista vs observada).
        """
        p = np.asarray(list(probabilities), dtype=float)
        y = np.asarray(list(outcomes), dtype=float)
        if p.shape != y.shape or p.size == 0:
            raise ValueError("p e y devem ter mesmo tamanho > 0")
        bs = float(np.mean((p - y) ** 2))
        p_bar = float(np.mean(y))
        # Reliability/Resolution via 10 bins
        bins = np.linspace(0, 1, 11)
        rel = 0.0
        res = 0.0
        n = p.size
        for k in range(10):
            mask = (p >= bins[k]) & (p < bins[k + 1] if k < 9 else p <= bins[k + 1])
            n_k = int(mask.sum())
            if n_k == 0:
                continue
            p_mean_k = float(p[mask].mean())
            y_mean_k = float(y[mask].mean())
            rel += (n_k / n) * (p_mean_k - y_mean_k) ** 2
            res += (n_k / n) * (y_mean_k - p_bar) ** 2
        unc = p_bar * (1 - p_bar)
        return {
            "brier_score": round(bs, 6),
            "reliability": round(rel, 6),
            "resolution": round(res, 6),
            "uncertainty": round(unc, 6),
            "n": int(n),
        }

    def reliability_diagram(
        self,
        probabilities: Sequence[float],
        outcomes: Sequence[int],
        n_bins: int = 10,
    ) -> list[dict[str, float]]:
        """Reliability diagram bins (Murphy & Winkler, 1977).

        Para cada bin de probabilidade prevista, retorna a frequencia observada.
        Modelo perfeitamente calibrado: linha diagonal (predicted == observed).
        """
        p = np.asarray(list(probabilities), dtype=float)
        y = np.asarray(list(outcomes), dtype=float)
        bins = np.linspace(0, 1, n_bins + 1)
        out: list[dict[str, float]] = []
        for k in range(n_bins):
            lo, hi = bins[k], bins[k + 1]
            mask = (p >= lo) & (p < hi if k < n_bins - 1 else p <= hi)
            n_k = int(mask.sum())
            if n_k == 0:
                continue
            out.append({
                "bin_lo": float(lo),
                "bin_hi": float(hi),
                "predicted_mean": round(float(p[mask].mean()), 4),
                "observed_mean": round(float(y[mask].mean()), 4),
                "n": n_k,
            })
        return out

    # ------------------------------------------------------------------
    # Comprehensive summary report
    # ------------------------------------------------------------------

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

        # Bayesian Beta-binomial credible interval por LLM (mais robusto a N pequeno)
        bayes_by_llm: dict[str, dict[str, Any]] = {}
        for llm, row in by_llm.iterrows():
            ci = self.beta_binomial_ci(int(row["sum"]), int(row["count"]))
            bayes_by_llm[str(llm)] = {
                "rate_posterior_mean": round(ci.point_estimate, 4),
                "ci_95": [round(ci.ci_lower, 4), round(ci.ci_upper, 4)],
                "n": ci.n,
                "cited": int(row["sum"]),
            }
        report["bayesian_by_llm"] = bayes_by_llm

        # Inter-LLM agreement via Fleiss kappa, quando o painel for retangular
        # (mesma query respondida por todos os LLMs).
        try:
            if "query" in citation_data.columns:
                pivot = (
                    citation_data
                    .pivot_table(index="query", columns="llm", values="cited", aggfunc="max")
                    .dropna()
                )
                if pivot.shape[0] >= 2 and pivot.shape[1] >= 2:
                    ratings = pivot.astype(int).values.tolist()
                    fk = self.fleiss_kappa(ratings)
                    report["inter_llm_fleiss_kappa"] = {
                        "kappa": fk.kappa,
                        "interpretation": fk.interpretation,
                        "n_subjects": fk.n_subjects,
                        "n_raters": fk.n_raters,
                    }
        except Exception as exc:
            logger.debug("Fleiss kappa skipped: %s", exc)

        return report
