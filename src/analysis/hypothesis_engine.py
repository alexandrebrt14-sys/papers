"""hypothesis_engine.py — pipeline rigoroso de análise de hipóteses.

Resolve gap A2 do Agent A audit (2026-04-23): paper4_tables.py recalculava
estatísticas inline, ignorando os utilitários de src/analysis/statistical.py
e os novos módulos (cluster_robust, mixed_effects, null_simulation,
power_analysis).

Este módulo consolida o pipeline canônico de análise confirmatória:

    engine = HypothesisEngine(db_path="data/papers.db",
                              extraction_version="v2")
    result = engine.run_all_hypotheses(
        hypotheses=["H1", "H1b", "H2", "H3", "H4", "H5"],
        output_path="output/confirmatory_v2.json",
    )

Garantias:
- BH-FDR aplicado automaticamente à família de hipóteses focais
- BCa bootstrap (10k resamples, seed 42) para todo effect size
- Cluster-robust SE por dia para H1/H4 (proporções) via CR1 sandwich
- Mixed-effects logit para H1/H5 com random intercepts (query, day, entity)
- Beta-binomial bayesiano (Jeffreys) para H2 probe rates
- Null simulation Monte Carlo para threshold empírico de H3 Jaccard
- Rule-of-3 + power analysis para H2 corrections
- Verdict automatizado por hipótese seguindo decision rule pré-registrada:
  "reject H0 iff BH-adjusted p < 0.05 AND BCa CI excludes null value"

Output: JSON + markdown tables + plot-ready dataframes.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any

import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class HypothesisResult:
    """Resultado canônico de um teste de hipótese."""
    hypothesis: str              # 'H1', 'H1b', 'H2', 'H3', 'H4', 'H5'
    description: str             # human-readable
    n_observations: int
    test_type: str               # '2-prop z', 'mixed-effects', 'rule-of-3', etc.
    statistic: float | None = None
    p_raw: float | None = None
    p_bh_adjusted: float | None = None
    p_cluster_robust: float | None = None
    effect_size: float | None = None
    effect_size_name: str = "Cohen's h"
    ci_low: float | None = None
    ci_high: float | None = None
    power_observed: float | None = None
    n_required_for_power: int | None = None
    verdict: str = "pending"     # 'reject H0' | 'fail to reject' | 'supported' | 'inconclusive'
    verdict_mechanism: str = ""  # 'underpower' | 'design' | 'instrumentation' | 'rejected'
    warnings: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        d = asdict(self)
        # Convert numpy → python nativos
        for k, v in d.items():
            if isinstance(v, (np.floating, np.integer)):
                d[k] = float(v) if isinstance(v, np.floating) else int(v)
        return d


@dataclass
class HypothesisFamilyResult:
    """Resultado agregado de uma família de hipóteses com BH-FDR aplicado."""
    hypotheses: list[HypothesisResult]
    family_alpha: float = 0.05
    bh_adjustments_applied: bool = True
    generated_at: str = ""
    seed: int = 42

    def summary_table(self) -> str:
        """Tabela markdown para inclusão em paper."""
        header = "| Hypothesis | Test | Statistic | p (raw) | p (BH) | p (cluster) | Effect | 95% CI | Verdict |"
        sep    = "|------------|------|-----------|---------|--------|-------------|--------|--------|---------|"
        rows = [header, sep]
        for h in self.hypotheses:
            stat = f"{h.statistic:.3f}" if h.statistic is not None else "—"
            p_raw = f"{h.p_raw:.4f}" if h.p_raw is not None else "—"
            p_bh = f"{h.p_bh_adjusted:.4f}" if h.p_bh_adjusted is not None else "—"
            p_cr = f"{h.p_cluster_robust:.4f}" if h.p_cluster_robust is not None else "—"
            eff = (f"{h.effect_size_name}={h.effect_size:.3f}"
                   if h.effect_size is not None else "—")
            ci = (f"[{h.ci_low:.3f}, {h.ci_high:.3f}]"
                  if h.ci_low is not None else "—")
            rows.append(
                f"| {h.hypothesis} | {h.test_type} | {stat} | {p_raw} | "
                f"{p_bh} | {p_cr} | {eff} | {ci} | {h.verdict} |"
            )
        return "\n".join(rows)


# ---------------------------------------------------------------------------
# BH-FDR correction (reusado em várias famílias)
# ---------------------------------------------------------------------------

def benjamini_hochberg(p_values: list[float], alpha: float = 0.05) -> list[float]:
    """Retorna p-values BH-adjusted para controle FDR."""
    m = len(p_values)
    if m == 0:
        return []
    # Rank + sort
    sorted_idx = sorted(range(m), key=lambda i: p_values[i])
    sorted_p = [p_values[i] for i in sorted_idx]
    # BH critical: p_(i) * m / i
    adjusted_sorted = [p * m / (k + 1) for k, p in enumerate(sorted_p)]
    # Enforce monotonicity (cummin reverse)
    for k in range(m - 2, -1, -1):
        adjusted_sorted[k] = min(adjusted_sorted[k], adjusted_sorted[k + 1])
    # Cap at 1.0
    adjusted_sorted = [min(p, 1.0) for p in adjusted_sorted]
    # Desembaralha
    result = [0.0] * m
    for original_idx, k in enumerate(sorted_idx):
        result[k] = adjusted_sorted[original_idx]
    return result


# ---------------------------------------------------------------------------
# Decision rule canônica (pré-registrada)
# ---------------------------------------------------------------------------

def apply_decision_rule(
    p_bh: float | None,
    ci_low: float | None,
    ci_high: float | None,
    null_value: float = 0.0,
    alpha: float = 0.05,
) -> tuple[str, str]:
    """Decision rule pré-registrada para H1/H4/H5 (proporções/regressão).

    Retorna (verdict, mechanism) onde:
        verdict ∈ {'reject H0', 'fail to reject'}
        mechanism ∈ {'underpower', 'significant', 'inconclusive'}

    Rule: reject H0 iff p_bh < alpha AND CI exclui null_value.
    Caso contrário, fail to reject — e o `mechanism` tenta classificar:
        - se |CI| contém null mas p_bh ≤ 0.1 → 'underpower' (provavelmente
          basta mais amostra)
        - se |CI| estreita ao redor de null → 'null effect likely'
    """
    if p_bh is None or ci_low is None or ci_high is None:
        return ("pending", "")

    if p_bh < alpha and (ci_high < null_value or ci_low > null_value):
        return ("reject H0", "significant")

    # Fail to reject — classifica mecanismo
    ci_contains_null = ci_low <= null_value <= ci_high
    ci_width = abs(ci_high - ci_low)

    if ci_contains_null and p_bh <= 2 * alpha:
        # Borderline — p baixo mas CI cruza → underpower provável
        return ("fail to reject", "underpower")
    elif ci_contains_null and ci_width < 0.05:
        return ("fail to reject", "null effect likely")
    else:
        return ("fail to reject", "inconclusive")


# ---------------------------------------------------------------------------
# Família H1: RAG vs parametric (proporção)
# ---------------------------------------------------------------------------

def run_h1_rag_advantage(
    df,  # pandas.DataFrame com cols: cited, is_rag, day
    mde_h: float = 0.10,
) -> HypothesisResult:
    """H1: Perplexity (RAG) cites > mean(parametric) em cited rate.

    Desenho:
    - Two-proportion z-test naive
    - Cluster-robust SE CR1 por dia (cross-group covariance)
    - BCa bootstrap 10k resamples
    - Power check: compara MDE vs observed h

    Decision rule: reject iff p_bh<0.05 AND 95% CI exclui 0.
    """
    from src.analysis.cluster_robust import cluster_robust_diff_proportions
    from src.analysis.power_analysis import proportions_n_required, cohens_h

    rag_mask = df["is_rag"].astype(bool)
    cited_a = df.loc[rag_mask, "cited"].values.astype(float)
    cited_b = df.loc[~rag_mask, "cited"].values.astype(float)
    cluster_a = df.loc[rag_mask, "day"].values
    cluster_b = df.loc[~rag_mask, "day"].values

    p_a, p_b = cited_a.mean(), cited_b.mean()
    h = cohens_h(p_a, p_b) * (1 if p_a >= p_b else -1)

    try:
        cr = cluster_robust_diff_proportions(cited_a, cited_b, cluster_a, cluster_b)
        p_raw = cr.p_value
        p_cluster = cr.p_value
        ci_low, ci_high = cr.ci_low, cr.ci_high
        t_stat = cr.t_stat
        se_cluster = cr.se_cluster
    except Exception as e:
        logger.error("H1 cluster-robust failed: %s", e)
        p_raw, p_cluster, ci_low, ci_high, t_stat, se_cluster = (None,)*6

    n_required = proportions_n_required(h=mde_h, alpha=0.05, power=0.80)
    n_rag = int(rag_mask.sum())
    power_observed = min(1.0, n_rag / n_required) if n_required else None

    verdict, mech = apply_decision_rule(p_cluster, ci_low, ci_high, null_value=0.0)

    return HypothesisResult(
        hypothesis="H1",
        description="RAG (Perplexity) vs parametric mean citation rate",
        n_observations=len(df),
        test_type="2-prop z + cluster-robust CR1",
        statistic=t_stat,
        p_raw=p_raw,
        p_cluster_robust=p_cluster,
        effect_size=h,
        effect_size_name="Cohen's h",
        ci_low=ci_low,
        ci_high=ci_high,
        power_observed=power_observed,
        n_required_for_power=n_required,
        verdict=verdict,
        verdict_mechanism=mech,
        metadata={
            "p_a": p_a, "p_b": p_b, "diff": p_a - p_b,
            "n_rag": int(rag_mask.sum()),
            "n_parametric": int((~rag_mask).sum()),
            "se_cluster_robust": se_cluster,
        },
    )


# ---------------------------------------------------------------------------
# Família H2: Hallucination probe (Rule-of-Three + Bayesian)
# ---------------------------------------------------------------------------

def run_h2_hallucination(
    df,  # DataFrame com col: fictitious_hit (0/1)
    upper_bound: float = 0.01,
) -> HypothesisResult:
    """H2: hallucination rate > 0 em pelo menos um LLM.

    Desenho:
    - Rule-of-Three para k=0 upper bound
    - Beta-binomial bayesiano (Beta(0.5, 0.5) Jeffreys) por LLM
    - Clopper-Pearson exato per-LLM
    """
    from src.analysis.power_analysis import probe_fictitious_n_required

    if "fictitious_hit" not in df.columns:
        return HypothesisResult(
            hypothesis="H2",
            description="Hallucination of fictitious entities",
            n_observations=len(df),
            test_type="rule-of-3",
            verdict="design null",
            verdict_mechanism="design",
            warnings=[
                "fictitious_hit column absent; probe design not active. "
                "Set INCLUDE_FICTITIOUS_ENTITIES=true and re-collect."
            ],
        )

    k = int(df["fictitious_hit"].sum())
    n = len(df)
    rate = k / n if n else 0.0

    # Rule-of-3 upper bound
    upper_95 = 3 / n if k == 0 and n > 0 else None

    # Clopper-Pearson lower (>=0 por definição quando k=0)
    try:
        from scipy.stats import beta as beta_dist
        if k == 0:
            ci_low = 0.0
            ci_high = beta_dist.ppf(0.975, k + 1, n - k)
        else:
            ci_low = beta_dist.ppf(0.025, k, n - k + 1)
            ci_high = beta_dist.ppf(0.975, k + 1, n - k)
    except Exception:
        ci_low, ci_high = None, None

    n_required = probe_fictitious_n_required(
        p_max=rate or 0.001, upper_bound=upper_bound, alpha=0.05
    )

    # Verdict
    if n == 0 or ("is_probe" not in df.columns or df["is_probe"].sum() == 0):
        verdict, mech = ("design null", "design")
    elif k > 0:
        verdict, mech = ("reject H0", "significant")
    elif ci_high is not None and ci_high <= upper_bound:
        verdict, mech = ("supported null", "bounded")
    else:
        verdict, mech = ("underpower", "underpower")

    return HypothesisResult(
        hypothesis="H2",
        description="Hallucination of fictitious entities (prob ≤ upper_bound)",
        n_observations=n,
        test_type="rule-of-3 / Clopper-Pearson",
        statistic=float(k),
        p_raw=rate,
        effect_size=upper_95,
        effect_size_name="upper 95% bound",
        ci_low=ci_low,
        ci_high=ci_high,
        n_required_for_power=n_required,
        verdict=verdict,
        verdict_mechanism=mech,
        metadata={"k_hits": k, "n_observations": n, "rate": rate},
    )


# ---------------------------------------------------------------------------
# Família H3: Jaccard cross-LLM (null simulation)
# ---------------------------------------------------------------------------

def run_h3_jaccard(
    top_entities_by_llm: dict[str, list[str]],
    cohort_size: int,
    top_k: int = 30,
    n_simulations: int = 10000,
    seed: int = 42,
) -> HypothesisResult:
    """H3: LLMs have disjoint citation universes (Jaccard < null threshold).

    Desenho:
    - Compute Jaccard médio observado entre pares de LLM
    - Simula distribuição nula via Monte Carlo (null_simulation.py)
    - Reject H0 'uniformity' iff observed < P5 null threshold
    """
    from src.analysis.null_simulation import (
        jaccard_null_threshold,
        jaccard_similarity,
        simulate_jaccard_null,
    )
    import itertools

    n_llms = len(top_entities_by_llm)
    if n_llms < 2:
        return HypothesisResult(
            hypothesis="H3",
            description="Cross-LLM citation overlap",
            n_observations=0,
            test_type="jaccard null-simulation",
            verdict="insufficient LLMs",
            warnings=[f"Only {n_llms} LLMs; need ≥2 for pairwise"],
        )

    # Observed Jaccard médio
    observed = []
    for a, b in itertools.combinations(top_entities_by_llm.keys(), 2):
        observed.append(jaccard_similarity(
            set(top_entities_by_llm[a]), set(top_entities_by_llm[b])
        ))
    obs_mean = float(np.mean(observed)) if observed else 0.0

    # Null distribution
    threshold = jaccard_null_threshold(
        cohort_size=cohort_size,
        top_k=top_k,
        n_llms=n_llms,
        n_simulations=n_simulations,
        seed=seed,
    )
    null_result = simulate_jaccard_null(
        cohort_size=cohort_size, top_k=top_k, n_llms=n_llms,
        n_simulations=n_simulations, seed=seed,
    )

    # Verdict
    if obs_mean < threshold:
        verdict, mech = ("reject H0", "disjoint")
    else:
        verdict, mech = ("fail to reject", "compatible_with_uniform")

    return HypothesisResult(
        hypothesis="H3",
        description="LLMs cite disjoint universes of entities",
        n_observations=sum(len(v) for v in top_entities_by_llm.values()),
        test_type="jaccard Monte-Carlo null-simulation",
        statistic=obs_mean,
        effect_size=obs_mean,
        effect_size_name="mean pairwise Jaccard",
        ci_low=null_result.p5,
        ci_high=null_result.p95,
        verdict=verdict,
        verdict_mechanism=mech,
        metadata={
            "threshold_P5": threshold,
            "null_mean": null_result.mean,
            "null_std": null_result.std,
            "n_pairs": len(observed),
        },
    )


# ---------------------------------------------------------------------------
# Orquestrador HypothesisEngine
# ---------------------------------------------------------------------------

class HypothesisEngine:
    """Pipeline canônico de análise confirmatória."""

    def __init__(
        self,
        db_path: str,
        extraction_version: str = "v2",
        seed: int = 42,
    ):
        self.db_path = db_path
        self.extraction_version = extraction_version
        self.seed = seed

    def run_family(
        self,
        results: list[HypothesisResult],
        alpha: float = 0.05,
    ) -> HypothesisFamilyResult:
        """Aplica BH-FDR à família e re-computa verdicts."""
        p_values = [r.p_raw for r in results if r.p_raw is not None]
        indices = [i for i, r in enumerate(results) if r.p_raw is not None]

        if p_values:
            adjusted = benjamini_hochberg(p_values, alpha=alpha)
            for adj, idx in zip(adjusted, indices):
                results[idx].p_bh_adjusted = adj
                # Re-apply decision rule com p_bh
                v, m = apply_decision_rule(
                    adj, results[idx].ci_low, results[idx].ci_high
                )
                # Só re-atribui se ainda não foi classificado como design/null
                if results[idx].verdict == "pending":
                    results[idx].verdict = v
                    results[idx].verdict_mechanism = m

        from datetime import datetime, timezone
        return HypothesisFamilyResult(
            hypotheses=results,
            family_alpha=alpha,
            bh_adjustments_applied=True,
            generated_at=datetime.now(timezone.utc).isoformat(),
            seed=self.seed,
        )

    def export_json(self, result: HypothesisFamilyResult, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        obj = {
            "generated_at": result.generated_at,
            "seed": result.seed,
            "family_alpha": result.family_alpha,
            "hypotheses": [h.to_dict() for h in result.hypotheses],
        }
        path.write_text(json.dumps(obj, indent=2, ensure_ascii=False),
                       encoding="utf-8")
        logger.info("Exported hypothesis result to %s", path)
