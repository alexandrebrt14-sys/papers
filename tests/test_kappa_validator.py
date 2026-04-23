"""Onda 6d — triple-LLM kappa validator tests (mocked LLMs, no network)."""
from __future__ import annotations

import math

import pytest

from src.analysis.kappa_validator import (
    cohen_kappa_binary,
    labels_from_cited_set,
    majority_vote,
    run_triple_llm_kappa,
)


# ---------- Cohen's κ ----------

def test_kappa_perfect_agreement() -> None:
    k = cohen_kappa_binary([1, 0, 1, 0, 1], [1, 0, 1, 0, 1])
    assert k.kappa == 1.0
    assert k.po == 1.0


def test_kappa_complete_disagreement() -> None:
    k = cohen_kappa_binary([1, 1, 0, 0], [0, 0, 1, 1])
    assert k.kappa < 0  # worse than chance
    assert k.po == 0.0


def test_kappa_chance_level() -> None:
    """50% agreement with balanced margins → κ ≈ 0."""
    a = [1] * 100 + [0] * 100
    b = [1] * 50 + [0] * 50 + [1] * 50 + [0] * 50
    k = cohen_kappa_binary(a, b)
    assert abs(k.kappa) < 0.05


def test_kappa_length_mismatch_raises() -> None:
    with pytest.raises(ValueError):
        cohen_kappa_binary([1, 0], [1])


def test_kappa_all_ones_identical() -> None:
    """If both annotators always say 1, agreement is perfect but pe=1 edge case."""
    k = cohen_kappa_binary([1, 1, 1, 1], [1, 1, 1, 1])
    assert k.kappa == 1.0


def test_kappa_empty_input() -> None:
    k = cohen_kappa_binary([], [])
    assert math.isnan(k.kappa)
    assert k.n_items == 0


def test_kappa_interpretation_bands() -> None:
    # Build known-kappa cases and check labels
    perfect = cohen_kappa_binary([1, 1, 0, 0] * 25, [1, 1, 0, 0] * 25)
    assert perfect.interpretation() == "near-perfect"


# ---------- labels_from_cited_set ----------

def test_labels_case_insensitive() -> None:
    cohort = ["Nubank", "Itaú", "Bradesco"]
    lbl = labels_from_cited_set(["nubank", "BRADESCO"], cohort)
    assert lbl == [1, 0, 1]


def test_labels_empty_cited() -> None:
    assert labels_from_cited_set([], ["A", "B"]) == [0, 0]


# ---------- majority_vote ----------

def test_majority_vote_strict() -> None:
    """2 de 3 → 1; 1 de 3 → 0; empate → 0."""
    ls = [[1, 0, 1], [1, 0, 0], [0, 0, 1]]
    # entity 0: 2 vs 1 → 1
    # entity 1: 0 → 0
    # entity 2: 2 vs 1 → 1
    assert majority_vote(ls) == [1, 0, 1]


def test_majority_vote_empty() -> None:
    assert majority_vote([]) == []


# ---------- run_triple_llm_kappa ----------

def test_triple_llm_kappa_perfect_agreement() -> None:
    """Mock regex + 3 LLMs que retornam a MESMA coisa → κ = 1."""
    cohort = ["Nubank", "Itaú", "Bradesco"]
    rows = [
        {"response_text": "Nubank e Itaú dominam o mercado."},
        {"response_text": "Bradesco lidera o varejo bancário."},
        {"response_text": "Nubank supera os concorrentes."},
    ] * 15  # 45 rows

    def regex_fn(text: str, coh: list[str]) -> list[str]:
        return [e for e in coh if e.lower() in text.lower()]

    def llm_fn(text: str, coh: list[str], llm: str) -> list[str]:
        return [e for e in coh if e.lower() in text.lower()]

    report = run_triple_llm_kappa(rows, cohort, regex_fn, llm_fn)
    assert report.n_rows == 45
    assert report.n_entities == 3
    # All κs should be ~1.0
    for k in report.pairwise_kappas:
        assert k.kappa == pytest.approx(1.0, abs=0.01)
    assert report.regex_consensus_kappa == pytest.approx(1.0, abs=0.01)


def test_triple_llm_kappa_flags_regex_disagreement() -> None:
    """Regex falha em detectar 'Itau' (sem acento) mas LLMs pegam."""
    cohort = ["Itaú"]
    rows = [
        {"response_text": "O Itau é o maior banco do país."},  # sem acento
        {"response_text": "Itau lidera hoje."},
        {"response_text": "Outro banco sem Itaú relevante."},
    ] * 10  # 30 rows

    # Regex naïve: só pega acento exato
    def bad_regex(text: str, coh: list[str]) -> list[str]:
        return [e for e in coh if e in text]

    # LLMs "inteligentes": pegam variantes
    def smart_llm(text: str, coh: list[str], llm: str) -> list[str]:
        out = []
        for e in coh:
            if e in text or e.replace("ú", "u") in text:
                out.append(e)
        return out

    report = run_triple_llm_kappa(rows, cohort, bad_regex, smart_llm)
    # regex vs llm should NOT be perfect (regex missed "Itau")
    regex_vs_llm = [k for k in report.pairwise_kappas if k.annotator_a == "regex_ner_v2" and k.annotator_b != "llm_consensus"]
    assert any(k.kappa < 1.0 for k in regex_vs_llm)


def test_triple_llm_kappa_warns_small_sample() -> None:
    cohort = ["Nubank"]
    rows = [{"response_text": "Nubank forte."}]  # n=1 (< 30)

    def fn(text: str, coh: list[str], *_) -> list[str]:
        return []

    def regex_fn(text: str, coh: list[str]) -> list[str]:
        return []

    report = run_triple_llm_kappa(rows, cohort, regex_fn, fn)
    assert any("small sample" in w for w in report.warnings)


def test_triple_llm_kappa_report_to_json() -> None:
    """Report serializes to JSON for governance audit trail."""
    cohort = ["A", "B"]
    rows = [{"response_text": "A e B"}, {"response_text": "Só A"}] * 20

    def fn(text: str, coh: list[str], *_) -> list[str]:
        return [e for e in coh if e in text]

    def regex_fn(text: str, coh: list[str]) -> list[str]:
        return fn(text, coh, "")

    report = run_triple_llm_kappa(rows, cohort, regex_fn, fn)
    out = report.to_json()
    import json
    parsed = json.loads(out)
    assert parsed["n_rows"] == 40
    assert "pairwise_kappas" in parsed
