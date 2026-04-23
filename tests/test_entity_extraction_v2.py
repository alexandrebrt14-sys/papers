"""Testes do NER v2 — garante que os gaps do Agent C audit (2026-04-23)
estão todos cobertos.
"""
from __future__ import annotations

import pytest

from src.analysis.entity_extraction import (
    EntityExtractor,
    EntityMention,
    fold_diacritics,
    normalize_nfc,
    position_tercile,
    strip_markup,
)


# ---------- Normalização ----------

def test_fold_diacritics_basic():
    assert fold_diacritics("Itaú") == "Itau"
    assert fold_diacritics("São Paulo") == "Sao Paulo"
    assert fold_diacritics("Sírio-Libanês") == "Sirio-Libanes"
    assert fold_diacritics("Aché") == "Ache"
    assert fold_diacritics("Pão de Açúcar") == "Pao de Acucar"


def test_normalize_nfc_idempotent():
    # 'á' composto vs decomposto: mesmo char após NFC
    decomposed = "á"   # a + combining acute
    composed = "á"            # á
    assert normalize_nfc(decomposed) == composed
    assert normalize_nfc(composed) == composed


def test_strip_markup_refs():
    assert strip_markup("Segundo o Nubank[1], taxa é 0%.") == "Segundo o Nubank, taxa é 0%."
    assert strip_markup("Stone[1][2][3] lidera.") == "Stone lidera."


def test_strip_markup_bold_italic():
    assert strip_markup("**Nubank** e *Itaú*") == "Nubank e Itaú"


def test_strip_markup_link():
    assert strip_markup("Veja [Banco Inter](https://inter.co)") == "Veja Banco Inter"


def test_strip_markup_html():
    assert strip_markup("<em>Stone</em> cresceu.") == "Stone cresceu."


def test_strip_markup_url():
    assert strip_markup("Saiba mais em https://nubank.com.br/taxas") == "Saiba mais em "


# ---------- Word-boundary rigoroso (G3) ----------

def test_no_substring_match():
    """'Inter' no cohort (ambiguous) NÃO deve match em 'international'."""
    ext = EntityExtractor(
        cohort=["Inter"],
        ambiguous={"Inter"},
        canonical_names={"Inter": "Banco Inter"},
    )
    m = ext.extract("This is an international bank.")
    assert m == []


def test_ambiguous_canonical_requires_full():
    ext = EntityExtractor(
        cohort=["Inter"],
        ambiguous={"Inter"},
        canonical_names={"Inter": "Banco Inter"},
    )
    # Nome canônico presente: casa
    m = ext.extract("Banco Inter cresce.")
    assert len(m) == 1
    assert m[0].entity == "Inter"
    # Nome só "Inter" sozinho: não casa (ambiguous)
    m2 = ext.extract("Inter foi elogiado.")
    assert m2 == []


def test_nonambiguous_matches_standalone():
    ext = EntityExtractor(cohort=["Nubank"])
    m = ext.extract("Nubank lançou novo produto.")
    assert len(m) == 1
    assert m[0].entity == "Nubank"


# ---------- Acento-insensitive dual-pass (G1) ----------

def test_fold_match_in_english_response():
    """Resposta EN sem acento deve match cohort PT acentuado."""
    ext = EntityExtractor(cohort=["Itaú"])
    m = ext.extract("Itau is the largest Brazilian bank.")
    assert len(m) == 1
    assert m[0].entity == "Itaú"
    assert m[0].via_fold is True


def test_accent_sensitive_preferred_over_fold():
    """Se texto tem acento, match PASS 1 vence (via_fold=False)."""
    ext = EntityExtractor(cohort=["Itaú"])
    m = ext.extract("Itaú é o maior banco.")
    assert len(m) == 1
    assert m[0].via_fold is False


# ---------- Aliases (G6) ----------

def test_aliases_map_to_canonical():
    ext = EntityExtractor(
        cohort=["BTG Pactual"],
        aliases={"BTG Pactual": ["BTG"]},
    )
    m = ext.extract("A BTG tem posição forte em M&A.")
    assert len(m) == 1
    assert m[0].entity == "BTG Pactual"
    assert m[0].matched_form == "BTG"
    assert m[0].via_alias is True


def test_canonical_preferred_over_alias():
    ext = EntityExtractor(
        cohort=["BTG Pactual"],
        aliases={"BTG Pactual": ["BTG"]},
    )
    # Canonical aparece antes: via_alias=False
    m = ext.extract("BTG Pactual cresceu. Hoje BTG domina.")
    assert len(m) == 1
    assert m[0].entity == "BTG Pactual"
    assert m[0].via_alias is False


# ---------- Stop-contexts (G7) ----------

def test_stop_context_removes_false_positive():
    # stop_contexts usa regex literal (não precisa de \b — word boundaries
    # não funcionam com % e outros non-word chars).
    ext = EntityExtractor(
        cohort=["99"],
        stop_contexts={"99": [r"99%"]},
    )
    m = ext.extract("Crescimento de 99% no ano.")
    assert m == []


def test_stop_context_still_matches_when_absent():
    ext = EntityExtractor(
        cohort=["99"],
        stop_contexts={"99": [r"99%"]},
    )
    m = ext.extract("99 lançou app de mobilidade.")
    assert len(m) == 1


# ---------- Position via offset (G4) ----------

def test_position_tercile_first_third():
    # Texto de 90 chars; start=20 → ratio ~0.22 → tercile 1
    assert position_tercile(start=20, text_length=90) == 1


def test_position_tercile_middle():
    assert position_tercile(start=45, text_length=90) == 2


def test_position_tercile_final():
    assert position_tercile(start=75, text_length=90) == 3


def test_position_tercile_edge_cases():
    assert position_tercile(start=0, text_length=0) == 2    # texto vazio: meio
    assert position_tercile(start=0, text_length=1) == 1    # primeiro char


# ---------- Ordem + dedup ----------

def test_multiple_entities_ordered_by_position():
    ext = EntityExtractor(cohort=["Itaú", "Bradesco", "Nubank"])
    text = "Nubank é o líder, seguido de Itaú e depois Bradesco."
    m = ext.extract(text)
    assert [x.entity for x in m] == ["Nubank", "Itaú", "Bradesco"]


def test_entity_reported_once_even_multiple_mentions():
    ext = EntityExtractor(cohort=["Nubank"])
    m = ext.extract("Nubank. Mais sobre Nubank. E Nubank.")
    assert len(m) == 1
    assert m[0].start == 0


# ---------- Integração com strip_markup ----------

def test_match_after_stripping_md():
    ext = EntityExtractor(cohort=["Itaú"])
    m = ext.extract("**Itaú** é referência[1].")
    assert len(m) == 1
    assert m[0].entity == "Itaú"


def test_match_in_link_text():
    ext = EntityExtractor(cohort=["Banco Inter"], ambiguous={"Banco Inter"},
                         canonical_names={"Banco Inter": "Banco Inter"})
    m = ext.extract("Veja [Banco Inter](https://inter.co) para detalhes.")
    assert len(m) == 1
