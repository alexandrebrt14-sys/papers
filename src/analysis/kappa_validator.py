"""Triple-LLM kappa validator — interim inter-annotator agreement proxy.

Gap Onda 6d (2026-04-23): Paper 4 flagged that NER v2 lacks human-annotated
ground truth. Pre-registration of Paper 5 targets 200 rows with Cohen's κ
against two human annotators, but that dataset will not be ready for weeks.

This module provides an **interim** proxy: ask 3 LLMs (GPT-4o-mini, Claude
Haiku, Gemini Pro) to independently label whether each cohort entity is
cited in a response, then compute pairwise Cohen's κ between:
  - regex NER v2 (the extractor under test)
  - each of the 3 LLM annotators

Interpretation:
  - κ > 0.75: near-perfect agreement (regex = LLM consensus)
  - κ 0.60 — 0.75: substantial agreement
  - κ 0.40 — 0.60: moderate agreement (investigate disagreements)
  - κ < 0.40: poor agreement — regex likely wrong, needs review

This is **not a replacement** for human annotation. It catches gross
implementation bugs and lets us ship without blocking on Ground Truth Lab.

Usage:
    from src.analysis.kappa_validator import run_triple_llm_kappa
    result = run_triple_llm_kappa(
        rows=[{"response_text": "...", "cited_true": ["Nubank", "Itaú"]}, ...],
        cohort=["Nubank", "Itaú", "Bradesco", ...],
        llm_extract_fn=extract_entities_llm,  # dependency-injected for testing
    )
    print(result.kappas)  # {"regex_vs_openai": 0.82, ...}
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from typing import Callable

# Binary entity-level label: 1 if entity cited in response, 0 otherwise
Labels = list[int]
LLMExtractFn = Callable[[str, list[str], str], list[str]]


@dataclass
class KappaResult:
    """Cohen's κ result for a pair of annotators."""
    annotator_a: str
    annotator_b: str
    kappa: float
    po: float  # observed agreement
    pe: float  # expected agreement by chance
    n_items: int
    agreement_count: int
    disagreement_count: int

    def interpretation(self) -> str:
        """Landis & Koch (1977) verbal labels."""
        if self.kappa < 0:
            return "poor (worse than chance)"
        if self.kappa < 0.20:
            return "slight"
        if self.kappa < 0.40:
            return "fair"
        if self.kappa < 0.60:
            return "moderate"
        if self.kappa < 0.75:
            return "substantial"
        return "near-perfect"


@dataclass
class TripleLLMKappaReport:
    """Aggregate report across N rows × M annotators."""
    n_rows: int
    n_entities: int
    annotators: list[str]
    pairwise_kappas: list[KappaResult] = field(default_factory=list)
    regex_consensus_kappa: float | None = None  # vs majority vote
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "n_rows": self.n_rows,
            "n_entities": self.n_entities,
            "annotators": self.annotators,
            "pairwise_kappas": [asdict(k) for k in self.pairwise_kappas],
            "regex_consensus_kappa": self.regex_consensus_kappa,
            "warnings": self.warnings,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


def cohen_kappa_binary(labels_a: Labels, labels_b: Labels) -> KappaResult:
    """Cohen's κ for two binary annotators.

    κ = (po - pe) / (1 - pe) where:
        po = observed agreement proportion
        pe = expected agreement by chance (from marginal distributions)
    """
    if len(labels_a) != len(labels_b):
        raise ValueError(f"length mismatch: {len(labels_a)} vs {len(labels_b)}")
    n = len(labels_a)
    if n == 0:
        return KappaResult("a", "b", float("nan"), 0.0, 0.0, 0, 0, 0)

    agree = sum(1 for x, y in zip(labels_a, labels_b) if x == y)
    po = agree / n

    # Marginal probabilities (P(label=1) for each annotator)
    p_a_1 = sum(labels_a) / n
    p_b_1 = sum(labels_b) / n
    p_a_0 = 1 - p_a_1
    p_b_0 = 1 - p_b_1

    # Expected agreement by chance
    pe = p_a_1 * p_b_1 + p_a_0 * p_b_0

    if pe >= 1.0:
        # All labels identical on both sides — perfect agreement trivially
        kappa = 1.0 if po == 1.0 else float("nan")
    else:
        kappa = (po - pe) / (1 - pe)

    return KappaResult(
        annotator_a="a", annotator_b="b",
        kappa=round(kappa, 4), po=round(po, 4), pe=round(pe, 4),
        n_items=n, agreement_count=agree, disagreement_count=n - agree,
    )


def labels_from_cited_set(cited: list[str], cohort: list[str]) -> Labels:
    """Convert a list of cited-entity names into binary labels aligned to cohort order.

    Output[i] = 1 iff cohort[i] ∈ cited (case-insensitive exact match).
    """
    cited_lower = {c.lower() for c in cited}
    return [1 if c.lower() in cited_lower else 0 for c in cohort]


def majority_vote(label_sets: list[Labels]) -> Labels:
    """For each position, return 1 iff strict majority of annotators labeled 1."""
    if not label_sets:
        return []
    n = len(label_sets[0])
    threshold = len(label_sets) / 2
    return [
        1 if sum(ls[i] for ls in label_sets) > threshold else 0
        for i in range(n)
    ]


def run_triple_llm_kappa(
    rows: list[dict],
    cohort: list[str],
    regex_extract_fn: Callable[[str, list[str]], list[str]],
    llm_extract_fn: LLMExtractFn,
    llm_names: tuple[str, ...] = ("openai", "anthropic", "google"),
) -> TripleLLMKappaReport:
    """Compute pairwise Cohen's κ between regex NER v2 and 3 LLM annotators.

    Parameters:
        rows: list of dicts with key "response_text"
        cohort: ordered list of entity names
        regex_extract_fn: (text, cohort) → list[str] cited entities (NER v2)
        llm_extract_fn: (text, cohort, llm_name) → list[str] cited entities
        llm_names: which LLMs to ask

    Returns KappaReport with pairwise κ values and consensus comparison.

    Dependency injection of extract functions makes this testable without
    network calls — unit tests pass mock fns; production wires real clients.
    """
    warnings: list[str] = []
    if len(rows) < 30:
        warnings.append(
            f"small sample (n={len(rows)}): κ CI will be wide. Minimum 30 rows recommended, 200 for publication."
        )

    # Build label matrix: [annotator][row][entity]
    regex_labels: list[Labels] = []
    llm_labels: dict[str, list[Labels]] = {name: [] for name in llm_names}

    for row in rows:
        text = row.get("response_text", "")
        # Regex extractor (ground-truth-candidate)
        regex_cited = regex_extract_fn(text, cohort)
        regex_labels.append(labels_from_cited_set(regex_cited, cohort))
        # Each LLM
        for name in llm_names:
            llm_cited = llm_extract_fn(text, cohort, name)
            llm_labels[name].append(labels_from_cited_set(llm_cited, cohort))

    # Flatten row×entity grid for κ computation
    regex_flat = [lbl for row_labels in regex_labels for lbl in row_labels]
    llm_flat = {
        name: [lbl for row_labels in llm_labels[name] for lbl in row_labels]
        for name in llm_names
    }

    pairwise: list[KappaResult] = []

    # regex vs each LLM
    for name in llm_names:
        k = cohen_kappa_binary(regex_flat, llm_flat[name])
        k.annotator_a = "regex_ner_v2"
        k.annotator_b = name
        pairwise.append(k)

    # LLM vs LLM (cross-check annotator stability)
    for i, a in enumerate(llm_names):
        for b in llm_names[i + 1:]:
            k = cohen_kappa_binary(llm_flat[a], llm_flat[b])
            k.annotator_a = a
            k.annotator_b = b
            pairwise.append(k)

    # regex vs majority vote of LLMs (consensus)
    consensus_flat: Labels = []
    for row_idx in range(len(rows)):
        row_label_sets = [llm_labels[name][row_idx] for name in llm_names]
        consensus_flat.extend(majority_vote(row_label_sets))

    consensus_k = cohen_kappa_binary(regex_flat, consensus_flat)
    consensus_k.annotator_a = "regex_ner_v2"
    consensus_k.annotator_b = "llm_consensus"

    return TripleLLMKappaReport(
        n_rows=len(rows),
        n_entities=len(cohort),
        annotators=["regex_ner_v2", *llm_names, "llm_consensus"],
        pairwise_kappas=[*pairwise, consensus_k],
        regex_consensus_kappa=consensus_k.kappa,
        warnings=warnings,
    )
