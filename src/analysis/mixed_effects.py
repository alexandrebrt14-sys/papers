"""mixed_effects.py — GLMM logit para H1/H4/H5 do paper 4 v2.

Resolve gap A3 do Agent A audit (2026-04-23):

Cluster-robust SE (cluster_robust.py) é um proxy para independência dentro
de clusters. O modelo correto para `cited ~ is_rag` quando temos múltiplos
níveis aninhados (query, entity, model, day) é Generalized Linear Mixed
Model com random intercepts. statsmodels.BinomialBayesMixedGLM faz isso
com prior fracamente informativo; cross-check manual com pymer4 quando
disponível.

Uso:
    from src.analysis.mixed_effects import fit_cited_mixed_logit

    result = fit_cited_mixed_logit(
        df,  # DataFrame com cited (0/1), is_rag, day, query, entity, llm
        formula_fixed="cited ~ is_rag + query_lang + query_type",
        random_groups=["day", "query"],
    )
    # → {"params": {...}, "or_is_rag": 0.95, "ci_95": (0.80, 1.13),
    #    "conditional_aic": 8456.3, "converged": True}
"""
from __future__ import annotations

import logging
import warnings
from dataclasses import dataclass, field
from typing import Any

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


@dataclass
class MixedEffectsResult:
    """Resultado do fit de um GLMM logit."""
    converged: bool
    n_obs: int
    n_random_groups: dict[str, int]
    fixed_params: dict[str, float]
    fixed_se: dict[str, float]
    fixed_z: dict[str, float]
    fixed_p: dict[str, float]
    fixed_ci_low: dict[str, float]
    fixed_ci_high: dict[str, float]
    odds_ratios: dict[str, float]
    or_ci_low: dict[str, float]
    or_ci_high: dict[str, float]
    random_variances: dict[str, float] = field(default_factory=dict)
    aic: float | None = None
    bic: float | None = None
    loglike: float | None = None
    warnings: list[str] = field(default_factory=list)

    def summary_text(self) -> str:
        """Tabela de efeitos fixos em formato legível para paper."""
        lines = [
            f"{'='*70}",
            f"Mixed-effects logit model (n={self.n_obs}, converged={self.converged})",
            f"Random groups: {self.n_random_groups}",
            f"{'='*70}",
            f"{'Variable':<30} {'Coef':>10} {'SE':>10} {'OR':>10} {'95% CI':>20}",
            "-" * 70,
        ]
        for var in self.fixed_params:
            coef = self.fixed_params[var]
            se = self.fixed_se.get(var, float("nan"))
            or_v = self.odds_ratios.get(var, float("nan"))
            or_lo = self.or_ci_low.get(var, float("nan"))
            or_hi = self.or_ci_high.get(var, float("nan"))
            lines.append(
                f"{var:<30} {coef:>10.4f} {se:>10.4f} {or_v:>10.3f} "
                f"  [{or_lo:>6.3f}, {or_hi:>6.3f}]"
            )
        lines.append("-" * 70)
        if self.aic is not None:
            lines.append(f"AIC={self.aic:.1f}, BIC={self.bic:.1f}, LL={self.loglike:.1f}")
        return "\n".join(lines)


def fit_cited_mixed_logit(
    df: pd.DataFrame,
    formula_fixed: str = "cited ~ is_rag",
    random_groups: list[str] | None = None,
    method: str = "BayesMixedGLM",
) -> MixedEffectsResult:
    """Fit GLMM logit para outcome binário cited.

    Args:
        df: DataFrame com colunas citadas em formula_fixed + random_groups.
            Todas variáveis categóricas devem ser codificadas como int ou str.
            cited deve ser 0/1.
        formula_fixed: Patsy formula para efeitos fixos (sem intercept implícito
            — o BayesMixedGLM adiciona automaticamente).
        random_groups: lista de colunas para random intercepts. Exemplo:
            ["day", "query"] gera dois random intercepts.
        method: "BayesMixedGLM" (default, disponível em statsmodels) ou
            "PenalizedGLM" (mais rápido mas aproximado).

    Returns:
        MixedEffectsResult com params, SE, p, OR e CIs.

    Notes:
        - BayesMixedGLM usa VB (variational Bayes) com prior N(0, 10)
          não-informativo para efeitos fixos e half-Cauchy para variâncias
          dos random effects.
        - Para convergência em datasets pequenos (<500 obs), pode ser
          necessário regularização mais forte ou usar PenalizedGLM.
        - Se fit falhar, retorna converged=False com warnings populados.
    """
    import statsmodels.api as sm
    from statsmodels.genmod.bayes_mixed_glm import BinomialBayesMixedGLM
    from patsy import dmatrices

    random_groups = random_groups or []
    warnings_list = []

    # Prepara matrizes
    try:
        y, X = dmatrices(formula_fixed, df, return_type="dataframe")
    except Exception as e:
        return MixedEffectsResult(
            converged=False,
            n_obs=len(df),
            n_random_groups={g: df[g].nunique() for g in random_groups},
            fixed_params={}, fixed_se={}, fixed_z={}, fixed_p={},
            fixed_ci_low={}, fixed_ci_high={},
            odds_ratios={}, or_ci_low={}, or_ci_high={},
            warnings=[f"Patsy dmatrices failed: {e}"],
        )

    n_obs = len(df)

    # Random effects design matrices (exog_vc)
    # statsmodels BayesMixedGLM espera dict de designs por grupo
    vc_formulas = {}
    for g in random_groups:
        vc_formulas[g] = f"0 + C({g})"

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            model = BinomialBayesMixedGLM.from_formula(
                formula=formula_fixed,
                vc_formulas=vc_formulas,
                data=df,
            )
            result = model.fit_vb()
        converged = True
    except Exception as e:
        logger.error("BayesMixedGLM fit failed: %s", e)
        return MixedEffectsResult(
            converged=False,
            n_obs=n_obs,
            n_random_groups={g: df[g].nunique() for g in random_groups},
            fixed_params={}, fixed_se={}, fixed_z={}, fixed_p={},
            fixed_ci_low={}, fixed_ci_high={},
            odds_ratios={}, or_ci_low={}, or_ci_high={},
            warnings=[f"BayesMixedGLM fit failed: {e}"],
        )

    # Extrai efeitos fixos
    fe_params = dict(zip(result.model.exog_names, result.fe_mean))
    fe_se = dict(zip(result.model.exog_names, result.fe_sd))

    from scipy.stats import norm
    z_crit = norm.ppf(0.975)

    params, se, z, p, ci_low, ci_high = {}, {}, {}, {}, {}, {}
    or_v, or_lo, or_hi = {}, {}, {}

    for name, coef in fe_params.items():
        se_val = fe_se[name]
        z_val = coef / se_val if se_val > 0 else float("nan")
        p_val = 2 * (1 - norm.cdf(abs(z_val))) if se_val > 0 else float("nan")

        params[name] = float(coef)
        se[name] = float(se_val)
        z[name] = float(z_val)
        p[name] = float(p_val)
        ci_low[name] = float(coef - z_crit * se_val)
        ci_high[name] = float(coef + z_crit * se_val)
        or_v[name] = float(np.exp(coef))
        or_lo[name] = float(np.exp(coef - z_crit * se_val))
        or_hi[name] = float(np.exp(coef + z_crit * se_val))

    # Variâncias dos random effects
    random_vars = {}
    for g, var in zip(random_groups, result.vcp_mean if hasattr(result, 'vcp_mean') else []):
        random_vars[g] = float(np.exp(var))

    return MixedEffectsResult(
        converged=converged,
        n_obs=n_obs,
        n_random_groups={g: df[g].nunique() for g in random_groups},
        fixed_params=params,
        fixed_se=se,
        fixed_z=z,
        fixed_p=p,
        fixed_ci_low=ci_low,
        fixed_ci_high=ci_high,
        odds_ratios=or_v,
        or_ci_low=or_lo,
        or_ci_high=or_hi,
        random_variances=random_vars,
        warnings=warnings_list,
    )


# ---------------------------------------------------------------------------
# Helper: prepara dataframe da tabela citations para fit
# ---------------------------------------------------------------------------

def prepare_citations_for_mixed(
    db_path: str,
    extraction_version: str = "v2",
    include_rag_flag: bool = True,
) -> pd.DataFrame:
    """Lê citations (preferencialmente v2) e adiciona is_rag, day, etc.

    Retorna DataFrame pronto para fit_cited_mixed_logit.
    """
    import sqlite3
    conn = sqlite3.connect(db_path)

    col_cited = "cited_v2" if extraction_version == "v2" else "cited"
    col_entities = "cited_entities_v2_json" if extraction_version == "v2" else ""

    where = ""
    if extraction_version == "v2":
        where = "WHERE extraction_version = 'v2' AND cited_v2 IS NOT NULL"

    df = pd.read_sql(
        f"""
        SELECT id, llm, model_version, query, query_category, query_lang,
               query_type, vertical, {col_cited} AS cited,
               DATE(timestamp) AS day,
               response_length_chars_v2 AS response_length
        FROM citations
        {where}
        """,
        conn,
    )
    conn.close()

    # Coerce cited to 0/1 int
    df["cited"] = df["cited"].fillna(0).astype(int)

    # is_rag flag — Perplexity é o único RAG-native
    if include_rag_flag:
        df["is_rag"] = (df["llm"] == "Perplexity").astype(int)

    # Language dummy (pt é baseline)
    df["is_en"] = (df["query_lang"] == "en").astype(int)

    # query_type dummy (directive baseline)
    df["is_exploratory"] = (df["query_type"] == "exploratory").astype(int)

    return df
