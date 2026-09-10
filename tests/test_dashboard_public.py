"""Integridade do dashboard_data.json público (2026-09-09).

Prova por mutação: injeta um decoy fictício nos rankings e confere que o
pós-processamento o remove; confere que o arquivo publicado no repo obedece
às mesmas regras (fictícia em topEntities reprova o commit).
"""
from __future__ import annotations

import copy
import json
from datetime import date
from pathlib import Path

import pytest

from src.analysis.dashboard_public import (
    apply_partial_days,
    compute_window_fields,
    load_partial_days,
    postprocess,
    roster_coverage,
    sanitize_public_rankings,
)
from src.config_v2 import FICTITIOUS_DECOYS_V2

REPO = Path(__file__).resolve().parent.parent
DASHBOARD = REPO / "data" / "dashboard_data.json"
PARTIAL = REPO / "data" / "partial_days.json"
FICT = sorted({e for lst in FICTITIOUS_DECOYS_V2.values() for e in lst})


def _sample() -> dict:
    return {
        "windowStart": "2026-04-23",
        "windowTotalDays": 90,
        "lastCollection": "2026-09-09 11:22:29",
        "collectedDays": 54,
        "calibration": {"fictitiousEntities": FICT, "fictitiousMentions": 0},
        "topEntities": [
            {"name": "Nubank", "citations": 5137},
            {"name": "Banco Floresta Digital", "citations": 1146},
            {"name": "FinPay Solutions", "citations": 1137},
            {"name": "PicPay", "citations": 1112},
        ],
        "crossVerticalEntities": [
            {"entity": "Nubank", "verticals": 3, "totalMentions": 5000},
            {"entity": "DataBridge Brasil", "verticals": 2, "totalMentions": 900},
        ],
        "weeklyDeltas": {
            "fintech": {
                "risers": [
                    {"entity": "Banco Floresta Digital", "deltaPct": 468.8},
                    {"entity": "Nubank", "deltaPct": 359.6},
                ],
                "fallers": [{"entity": "FinPay Solutions", "deltaPct": -50}],
                "newEntrants": [{"entity": "ShopNova Digital", "currentWeek": 4}],
            }
        },
        "verticalsFull": {
            "fintech": {
                "roster": ["Nubank", "PagBank", "Cielo", "Stone", "Banco Inter",
                           "Mercado Pago", "Itaú", "Bradesco", "C6 Bank", "PicPay",
                           "Ame Digital", "Neon", "Original", "BS2", "Safra",
                           "Banco Carrefour"],
                "rosterCount": 16,
                "citedEntities": [
                    {"entity": "Nubank", "count": 5137},
                    {"entity": "Banco Floresta Digital", "count": 1146},
                    {"entity": "FinPay Solutions", "count": 1137},
                    {"entity": "Inter", "count": 812},
                    {"entity": "Revolut", "count": 148},
                    {"entity": "BTG Pactual", "count": 78},
                ],
                "citedCount": 6,
                "coverage": 118.8,
            }
        },
        "dailySeries": [
            {"date": "2026-09-06", "queries": 100, "cited": 40, "rate": 40.0},
            {"date": "2026-09-08", "queries": 100, "cited": 40, "rate": 40.0},
        ],
    }


def _names(rows, key):
    return [r[key] for r in rows]


def test_mutacao_ficticia_injetada_sai_de_todos_os_rankings():
    data = sanitize_public_rankings(_sample())
    assert _names(data["topEntities"], "name") == ["Nubank", "PicPay"]
    assert _names(data["crossVerticalEntities"], "entity") == ["Nubank"]
    wd = data["weeklyDeltas"]["fintech"]
    assert _names(wd["risers"], "entity") == ["Nubank"]
    assert wd["fallers"] == [] and wd["newEntrants"] == []
    vf = data["verticalsFull"]["fintech"]
    assert "Banco Floresta Digital" not in _names(vf["citedEntities"], "entity")
    assert vf["citedCount"] == 4
    # Fictícias continuam no bloco de calibração: é o lugar delas.
    assert data["calibration"]["fictitiousEntities"] == FICT


def test_comparacao_ignora_caixa_e_espacamento():
    data = _sample()
    data["topEntities"].append({"name": "varejo  express", "citations": 1})
    sanitize_public_rankings(data)
    assert "varejo  express" not in _names(data["topEntities"], "name")


def test_coverage_limitada_ao_roster_e_nunca_passa_de_100():
    matched, cov = roster_coverage(["Nubank", "Banco Inter", "Cielo"], ["Nubank", "Inter", "Revolut", "Wise"])
    assert (matched, cov) == (2, 66.7)
    data = sanitize_public_rankings(_sample())
    vf = data["verticalsFull"]["fintech"]
    assert vf["rosterCited"] == 2  # Nubank e Inter -> Banco Inter; Revolut e BTG estao fora do roster
    assert vf["coverage"] <= 100.0
    assert vf["coverage"] == round(vf["rosterCited"] / 16 * 100, 1)


def test_sanitize_e_idempotente():
    once = sanitize_public_rankings(_sample())
    twice = sanitize_public_rankings(copy.deepcopy(once))
    assert once == twice


def test_window_end_projetado_e_coerente_com_o_health_check():
    # 09/09 com 54 de 90 dias coletados -> 36 restantes -> 15/10/2026
    w = compute_window_fields(date(2026, 4, 23), date(2026, 9, 9), 54)
    assert w["windowEnd"] == "2026-10-15"
    assert w["windowEndProjected"] == "2026-10-15"
    assert w["windowEndCalendar"] == "2026-07-21"
    assert w["windowRemainingDays"] == 36
    assert "COLETADOS" in w["windowEndSemantics"]


def test_window_fechada_termina_na_ultima_coleta():
    w = compute_window_fields(date(2026, 4, 23), date(2026, 10, 20), 90)
    assert w["windowEnd"] == "2026-10-20"
    assert w["windowRemainingDays"] == 0


def test_window_sem_coleta_cai_no_calendario():
    w = compute_window_fields(date(2026, 4, 23), None, 0)
    assert w["windowEnd"] == "2026-07-21"


def test_partial_days_marca_daily_series(tmp_path):
    p = tmp_path / "partial_days.json"
    p.write_text(json.dumps([
        {"date": "2026-09-06", "missingLLMs": ["ChatGPT"], "reason": "429"},
        {"date": "2026-09-06", "missingLLMs": ["Claude"], "reason": "400 credit"},
    ]), encoding="utf-8")
    partial = load_partial_days(p)
    assert partial == [{"date": "2026-09-06", "missingLLMs": ["ChatGPT", "Claude"],
                        "reason": "429; 400 credit", "source": ""}]
    data = apply_partial_days(_sample(), partial)
    by_date = {d["date"]: d for d in data["dailySeries"]}
    assert by_date["2026-09-06"]["partial"] is True
    assert by_date["2026-09-06"]["missingLLMs"] == ["ChatGPT", "Claude"]
    assert "partial" not in by_date["2026-09-08"]
    assert data["partialDays"] == partial


def test_partial_days_ausente_e_lista_vazia(tmp_path):
    assert load_partial_days(tmp_path / "nao-existe.json") == []


def test_postprocess_completo(tmp_path):
    data = postprocess(_sample(), tmp_path / "x.json")
    assert data["windowEnd"] == "2026-10-15"
    assert data["partialDays"] == []
    assert all(not any(n == f for f in FICT) for n in _names(data["topEntities"], "name"))


# --- O arquivo publicado obedece às regras ----------------------------------

@pytest.fixture(scope="module")
def published() -> dict:
    return json.loads(DASHBOARD.read_text(encoding="utf-8"))


def test_arquivo_publicado_sem_ficticia_nos_rankings(published):
    fict = {f.casefold() for f in published["calibration"]["fictitiousEntities"]}
    assert fict, "bloco de calibração precisa listar os decoys"
    assert not [e["name"] for e in published["topEntities"] if e["name"].casefold() in fict]
    for v, block in published["weeklyDeltas"].items():
        for group in ("risers", "fallers", "newEntrants"):
            assert not [r["entity"] for r in block[group] if r["entity"].casefold() in fict], (v, group)
    for v, vf in published["verticalsFull"].items():
        assert not [c["entity"] for c in vf["citedEntities"] if c["entity"].casefold() in fict], v
        assert vf["coverage"] <= 100.0, (v, vf["coverage"])
    assert not [e["entity"] for e in published["crossVerticalEntities"]
                if e["entity"].casefold() in fict]


def test_arquivo_publicado_window_end_nao_anterior_a_ultima_coleta(published):
    last = str(published["lastCollection"])[:10]
    assert published["windowEnd"] >= last, (published["windowEnd"], last)
    assert "windowEndCalendar" in published and "partialDays" in published


def test_partial_days_semeado_cobre_06_e_07_de_setembro():
    partial = load_partial_days(PARTIAL)
    dates = {p["date"] for p in partial}
    assert {"2026-09-06", "2026-09-07"} <= dates
