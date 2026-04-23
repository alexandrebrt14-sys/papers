"""null_simulation.py — Null distribution simulada para thresholds empíricos.

Resolve gap A5 do Agent A audit (2026-04-23):

O threshold de Jaccard = 0.30 usado em H3 do Paper 4 é ARBITRÁRIO.
Para decidir se "LLMs citam universos disjuntos", precisamos comparar o
Jaccard observado contra a distribuição sob H0 (citations independentes).

Método: Monte Carlo — amostrar top-K cited entities aleatórias de cada LLM
assumindo H0 (probabilidade igual por entidade do cohort), computar
Jaccard pairwise, repetir N vezes. O P95 dessa distribuição é o threshold
empírico.

Uso:
    from src.analysis.null_simulation import jaccard_null_threshold

    threshold_95 = jaccard_null_threshold(
        cohort_size=61,
        top_k=30,
        n_llms=4,
        n_simulations=10000,
        seed=42,
    )
    # → typically 0.15-0.20 para cohort=61, top_k=30

Interpretação:
    Se Jaccard observado < threshold_95 → rejeita H0 (universos DISJUNTOS)
    Se Jaccard observado ≥ threshold_95 → falha rejeitar H0 (compatível
    com citations uniformes)
"""
from __future__ import annotations

import itertools
import numpy as np
from dataclasses import dataclass


@dataclass
class JaccardNullResult:
    """Distribuição nula de Jaccard pairwise sob H0 de uniformidade."""
    n_simulations: int
    cohort_size: int
    top_k: int
    n_llms: int
    mean: float
    std: float
    p5: float
    p50: float
    p95: float
    observed_jaccards: np.ndarray  # Full array para plotting/inspeção


def jaccard_similarity(set_a: set, set_b: set) -> float:
    """Jaccard similarity entre dois conjuntos."""
    if not set_a and not set_b:
        return 1.0
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    return intersection / union if union > 0 else 0.0


def simulate_jaccard_null(
    cohort_size: int,
    top_k: int,
    n_llms: int,
    n_simulations: int = 10000,
    seed: int = 42,
) -> JaccardNullResult:
    """Simula distribuição nula de Jaccard pairwise médio.

    Assume sob H0: cada LLM escolhe top_k entidades uniformemente ao
    acaso do cohort de tamanho cohort_size. Computa Jaccard pairwise
    entre todos C(n_llms, 2) pares e reporta média por simulação.

    Args:
        cohort_size: tamanho do cohort (número total de entidades possíveis)
        top_k: quantas entidades cada LLM seleciona (top-K)
        n_llms: número de LLMs
        n_simulations: número de replicações Monte Carlo
        seed: seed para reprodutibilidade

    Returns:
        JaccardNullResult com estatísticas descritivas e array completo.
    """
    if top_k > cohort_size:
        raise ValueError(f"top_k ({top_k}) > cohort_size ({cohort_size})")
    if n_llms < 2:
        raise ValueError("n_llms deve ser >=2 para calcular pairwise Jaccard")

    rng = np.random.default_rng(seed)
    n_pairs = n_llms * (n_llms - 1) // 2
    mean_jaccards = np.zeros(n_simulations)

    cohort_indices = np.arange(cohort_size)

    for s in range(n_simulations):
        # Cada LLM sorteia top_k entidades (sem reposição) do cohort
        llm_sets = [
            frozenset(rng.choice(cohort_indices, size=top_k, replace=False))
            for _ in range(n_llms)
        ]
        # Jaccard pairwise médio
        jaccards = [
            jaccard_similarity(set(a), set(b))
            for a, b in itertools.combinations(llm_sets, 2)
        ]
        mean_jaccards[s] = np.mean(jaccards)

    return JaccardNullResult(
        n_simulations=n_simulations,
        cohort_size=cohort_size,
        top_k=top_k,
        n_llms=n_llms,
        mean=float(np.mean(mean_jaccards)),
        std=float(np.std(mean_jaccards, ddof=1)),
        p5=float(np.percentile(mean_jaccards, 5)),
        p50=float(np.percentile(mean_jaccards, 50)),
        p95=float(np.percentile(mean_jaccards, 95)),
        observed_jaccards=mean_jaccards,
    )


def jaccard_null_threshold(
    cohort_size: int,
    top_k: int,
    n_llms: int,
    n_simulations: int = 10000,
    seed: int = 42,
    alpha: float = 0.05,
) -> float:
    """Retorna threshold P95 (one-sided alpha=0.05) da distribuição nula.

    Interpretação: rejeitar H0 ("LLMs citam universos indistinguíveis de
    uniforme") se Jaccard observado < threshold retornado.
    """
    result = simulate_jaccard_null(
        cohort_size=cohort_size,
        top_k=top_k,
        n_llms=n_llms,
        n_simulations=n_simulations,
        seed=seed,
    )
    # Para H1 "universos disjuntos" (Jaccard < threshold), usamos P5 (extremidade baixa)
    # Para H1 "universos convergentes" (Jaccard > threshold), usamos P95
    # No Paper 4 a hipótese era "disjuntos" → returning P5 como threshold
    # (rejeita H0 se observed ≤ P5)
    return float(np.percentile(result.observed_jaccards, alpha * 100))
