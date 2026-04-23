"""power_analysis.py — power calculations para todas as hipóteses do paper.

Resolve gap A4 do Agent A audit (2026-04-23):

Paper 4 declarou "H2 fails by design" mas não calculou qual seria o n
necessário para detectar hallucination rates realistas (0.1%, 0.5%, 1%).
Este módulo preenche essa lacuna — e serve de planning tool para o
reboot da coleta com nova cohort/queries v2.

Fórmulas:
- Probe fictício (k=0 rare events): inverse Rule-of-Three
    n ≈ ln(alpha) / ln(1 - p)
    Para alpha=0.05, Wilson lower=0.
- Proporções (H1, H4): Cohen's h → n via arcsin transformation
    n_per_group = (z_α/2 + z_β)² / h²
- Mixed-effects (H5): aproximação via design effect DE = 1 + (m-1)·ICC
    onde m = obs por cluster. n_effective = n_total / DE.

Uso:
    from src.analysis.power_analysis import (
        probe_fictitious_n_required,
        proportions_n_required,
        design_effect_adjusted_n,
    )

    # H2: quantas decoy queries para bound 0.1% com upper CI ≤ 1%?
    n = probe_fictitious_n_required(p_max=0.001, upper_bound=0.01, alpha=0.05)

    # H1: quantas Perplexity queries para detectar Cohen's h=0.10 com power 0.80?
    n_per_group = proportions_n_required(h=0.10, alpha=0.05, power=0.80)
"""
from __future__ import annotations

import math
from dataclasses import dataclass


# ---------------------------------------------------------------------------
# Probe fictício (H2) — Rule-of-Three inverse
# ---------------------------------------------------------------------------

def probe_fictitious_n_required(
    p_max: float,
    upper_bound: float = 0.01,
    alpha: float = 0.05,
) -> int:
    """Calcula n mínimo para bound superior k=0 Wilson CI ao upper_bound.

    Scenario: queremos um probe fictício com k=0 hits. Com k=0, Wilson 95%
    CI lower=0; upper=3/n (Rule-of-Three) aproximadamente. Para afirmar
    "hallucination rate ≤ upper_bound" com 95% confiança, precisa:
        n ≥ 3 / upper_bound    (Rule-of-Three)
    Mais precisamente via exact binomial: n ≥ ln(alpha) / ln(1 - upper_bound).

    Args:
        p_max: rate máximo que ainda se considera "raro"
        upper_bound: upper bound desejado para Wilson CI quando k=0
        alpha: nível de confiança (default 0.05 → 95%)

    Returns:
        n mínimo (inteiro, arredondado para cima)

    Exemplo:
        Para bound ≤0.1% (0.001) com 95% confiança:
            n ≥ 3/0.001 = 3000
        Para 0.5% (0.005):
            n ≥ 600
        Para 1% (0.01):
            n ≥ 300
    """
    if upper_bound <= 0 or upper_bound >= 1:
        raise ValueError(f"upper_bound must be in (0, 1), got {upper_bound}")
    # Rule-of-Three: n = 3/upper_bound
    # Exact (Clopper-Pearson): n = ln(alpha) / ln(1 - upper_bound)
    n_exact = math.log(alpha) / math.log(1 - upper_bound)
    return int(math.ceil(n_exact))


# ---------------------------------------------------------------------------
# Proporções (H1, H4) — Cohen's h
# ---------------------------------------------------------------------------

def proportions_n_required(
    h: float,
    alpha: float = 0.05,
    power: float = 0.80,
    two_sided: bool = True,
) -> int:
    """Calcula n por grupo para detectar Cohen's h com power dado.

    Cohen's h = |2·arcsin(√p1) - 2·arcsin(√p2)|.
    Convenções: h=0.20 "small", h=0.50 "medium", h=0.80 "large".

    Fórmula: n_per_group = (z_{α/2} + z_β)² / h²

    Args:
        h: Cohen's h (effect size)
        alpha: significância
        power: 1 - β
        two_sided: two-sided test (default True)

    Returns:
        n mínimo por grupo
    """
    from scipy.stats import norm

    z_alpha = norm.ppf(1 - alpha / (2 if two_sided else 1))
    z_beta = norm.ppf(power)
    n = ((z_alpha + z_beta) ** 2) / (h ** 2)
    return int(math.ceil(n))


def cohens_h(p1: float, p2: float) -> float:
    """Cohen's h para diff entre duas proporções."""
    phi1 = 2 * math.asin(math.sqrt(p1))
    phi2 = 2 * math.asin(math.sqrt(p2))
    return abs(phi1 - phi2)


# ---------------------------------------------------------------------------
# Design effect (clustered data — H5 mixed-effects)
# ---------------------------------------------------------------------------

def design_effect_adjusted_n(
    n_naive: int,
    m_per_cluster: float,
    icc: float,
) -> int:
    """Ajusta n naive para inflation factor DE = 1 + (m-1)·ICC.

    Em dados clusterizados (e.g. múltiplas queries no mesmo dia), o n
    efetivo para potência é n_naive / DE.

    Args:
        n_naive: n calculado assumindo iid
        m_per_cluster: tamanho médio do cluster (obs/day)
        icc: intraclass correlation (0 = iid; 1 = obs idênticas por cluster)

    Returns:
        n ajustado (ceil)
    """
    de = 1 + (m_per_cluster - 1) * icc
    return int(math.ceil(n_naive * de))


# ---------------------------------------------------------------------------
# Roadmap para paper 4 v2 — quanto tempo de coleta é preciso?
# ---------------------------------------------------------------------------

@dataclass
class CollectionRoadmap:
    """Sumário de quantos dias para atingir power alvo nas 5 H's do paper v2."""
    target_hypothesis: str
    mde: str                    # descrição da MDE
    n_required: int             # obs mínimas
    current_rate_per_day: float # rows/dia do pipeline atual
    days_to_target: int         # int(n_required / current_rate_per_day)
    assumptions: list[str]


def reboot_roadmap(
    queries_per_day: int = 192,
    llms: int = 5,
    runs_per_day: int = 2,
) -> list[CollectionRoadmap]:
    """Gera cronograma de coleta para atingir power em todas as H's.

    Assume pipeline v2: 192 canonical queries × 5 LLMs × 2 runs/dia = 1920 rows/dia.
    Com verticals paralelas (4), queries são divididas: 48/vertical × 5 LLMs × 2 = 480/vertical/dia.
    """
    rows_per_day = queries_per_day * llms * runs_per_day

    # Perplexity específicamente: 1/5 das queries, 1/5 de rows (se PERPLEXITY_CATEGORIES off)
    perplexity_per_day = rows_per_day // llms

    roadmap = []

    # H1: RAG advantage (Perplexity vs parametric média)
    n_per_group_h1 = proportions_n_required(h=0.10, alpha=0.05, power=0.80)
    days_h1 = math.ceil(n_per_group_h1 / perplexity_per_day)
    roadmap.append(CollectionRoadmap(
        target_hypothesis="H1 RAG advantage (Perplexity > parametric mean)",
        mde="Cohen's h = 0.10 (small effect)",
        n_required=n_per_group_h1 * 2,  # total (2 grupos)
        current_rate_per_day=perplexity_per_day,
        days_to_target=days_h1,
        assumptions=["PERPLEXITY_CATEGORIES desligado (coleta em TODAS)",
                     f"{perplexity_per_day}/dia Perplexity"],
    ))

    # H1b: Brazilian brand rate (post-cohort-name-detection filter)
    # Com effect h=0.98 já observado exploratoriamente, MDE=0.20 conservador
    n_h1b = proportions_n_required(h=0.20, alpha=0.05, power=0.80)
    days_h1b = math.ceil(n_h1b / perplexity_per_day)
    roadmap.append(CollectionRoadmap(
        target_hypothesis="H1b Brazilian brand citation rate",
        mde="Cohen's h = 0.20 (medium-small)",
        n_required=n_h1b * 2,
        current_rate_per_day=perplexity_per_day,
        days_to_target=days_h1b,
        assumptions=["Filtra apenas BR brand matches"],
    ))

    # H2: probe fictício — bound 0.5%
    n_h2_per_cell = probe_fictitious_n_required(p_max=0.005, upper_bound=0.01)
    total_cells = llms * 4  # 5 LLMs × 4 verticais
    probe_rate_per_day = 16 * llms * runs_per_day  # 16 decoys (4/vert) × 5 LLMs × 2 runs
    days_h2 = math.ceil(n_h2_per_cell * total_cells / probe_rate_per_day)
    roadmap.append(CollectionRoadmap(
        target_hypothesis="H2 hallucination baseline (per LLM × vertical)",
        mde="Upper bound ≤ 1% com alpha=0.05",
        n_required=n_h2_per_cell * total_cells,
        current_rate_per_day=probe_rate_per_day,
        days_to_target=days_h2,
        assumptions=["16 decoys/run (4/vertical)", "INCLUDE_FICTITIOUS_ENTITIES=true"],
    ))

    # H3: Jaccard cross-LLM — requer top-100 entities com overlap estável
    # Empiricamente: 3 semanas para top-100 convergir com 1920/dia
    roadmap.append(CollectionRoadmap(
        target_hypothesis="H3 cross-LLM citation overlap (Jaccard top-100)",
        mde="Threshold empírico via null-simulation (~0.15-0.20)",
        n_required=500 * llms,  # 500 shared queries × 5 LLMs
        current_rate_per_day=rows_per_day,
        days_to_target=math.ceil(500 * llms / rows_per_day),
        assumptions=["Extração NER v2 uniforme (não sources_json)"],
    ))

    # H4: PT > EN post-vertical control
    n_h4 = proportions_n_required(h=0.10, alpha=0.05, power=0.80)
    # PT × EN 50/50 após split
    pt_rate_per_day = rows_per_day // 2
    days_h4 = math.ceil(n_h4 / pt_rate_per_day)
    roadmap.append(CollectionRoadmap(
        target_hypothesis="H4 PT > EN after vertical stratification (CMH)",
        mde="Cohen's h = 0.10 com 4 strata",
        n_required=n_h4 * 2 * 4,  # * 2 groups * 4 strata
        current_rate_per_day=pt_rate_per_day,
        days_to_target=days_h4,
        assumptions=["Query battery v2 50/50 PT/EN", "CMH test"],
    ))

    return roadmap


def print_roadmap_report() -> None:
    """Imprime roadmap formatado para inclusão em governance."""
    roadmap = reboot_roadmap()
    print(f"{'='*80}")
    print(f"PAPER 4 v2 — POWER ROADMAP")
    print(f"{'='*80}")
    print(f"Assume: 192 queries × 5 LLMs × 2 runs/day = 1920 rows/day")
    print(f"Budget: $50/month (Groq grátis + paid quotas)")
    print(f"{'='*80}")
    for r in roadmap:
        print(f"\n{r.target_hypothesis}")
        print(f"  MDE: {r.mde}")
        print(f"  N required: {r.n_required:,}")
        print(f"  Current rate: {r.current_rate_per_day:,.0f}/day")
        print(f"  Days to target: {r.days_to_target}")
        print(f"  Assumptions:")
        for a in r.assumptions:
            print(f"    - {a}")


if __name__ == "__main__":
    print_roadmap_report()
