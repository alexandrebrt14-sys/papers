"""Degradação graciosa do preflight (2026-09-09).

Entre 16/08 e 08/09 o preflight abortou 28 runs por saldo de um provedor e a
série perdeu 17 dias inteiros. A regra `decide` é pura (sem rede) e estes
testes cobrem as saídas: completo, parcial, bloqueado por mínimo, bloqueado por
defeito de instrumento, e modo strict.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

_SPEC = importlib.util.spec_from_file_location(
    "preflight_llm_check",
    Path(__file__).resolve().parent.parent / "scripts" / "preflight_llm_check.py",
)
pf = importlib.util.module_from_spec(_SPEC)
sys.modules["preflight_llm_check"] = pf
_SPEC.loader.exec_module(pf)

ALL = {"chatgpt", "claude", "gemini", "perplexity", "grok"}


def _ok(name):
    return pf.ProviderCheck(name, True, 100)


def _fail(name, err):
    return pf.ProviderCheck(name, False, 0, err)


@pytest.mark.parametrize("err,esperado", [
    ("HTTP 400: {\"error\":{\"message\":\"Your credit balance is too low\"}}", True),
    ("HTTP 429: no credits remaining", True),
    ("HTTP 401: insufficient_quota", True),
    ("HTTP 402: payment required", True),
    ("HTTP 429: prepayment credits depleted", True),
    ("OPENAI_API_KEY ausente", True),
    ("HTTP 400: invalid_parameter max_tokens", False),
    ("HTTP 500: internal", False),
    ("ConnectTimeout: timed out", False),
    (None, False),
])
def test_classificacao_de_falha_de_saldo(err, esperado):
    assert pf.is_billing_failure(err) is esperado


def test_todos_ok_prossegue_completo():
    d = pf.decide([_ok(n) for n in ALL], ALL)
    assert d.exit_code == 0 and d.degraded == [] and len(d.remaining_mandatory) == 5


def test_um_provedor_sem_saldo_vira_dia_parcial():
    checks = [_ok("chatgpt"), _fail("claude", "HTTP 400: credit balance is too low"),
              _ok("gemini"), _ok("perplexity"), _ok("grok")]
    d = pf.decide(checks, ALL, mode="degrade", min_llms=2)
    assert d.exit_code == 0
    assert d.degraded == ["Claude"]
    assert d.remaining_mandatory == ["ChatGPT", "Gemini", "Grok", "Perplexity"]


def test_dois_sem_saldo_ainda_parcial_com_tres_ok():
    checks = [_fail("chatgpt", "HTTP 429: no credits remaining"),
              _fail("claude", "HTTP 400: credit balance is too low"),
              _ok("gemini"), _ok("perplexity"), _ok("grok")]
    d = pf.decide(checks, ALL)
    assert d.exit_code == 0 and d.degraded == ["ChatGPT", "Claude"]


def test_abaixo_do_minimo_bloqueia():
    checks = [_fail("chatgpt", "HTTP 429: x"), _fail("claude", "HTTP 400: credit"),
              _fail("gemini", "HTTP 429: prepayment credits depleted"),
              _fail("perplexity", "HTTP 401: insufficient_quota"), _ok("grok")]
    d = pf.decide(checks, ALL, min_llms=2)
    assert d.exit_code == 2 and d.degraded == []
    assert "minimo 2" in d.reason


def test_defeito_de_instrumento_bloqueia_mesmo_em_degrade():
    checks = [_ok("chatgpt"), _ok("claude"), _ok("gemini"),
              _fail("perplexity", "HTTP 400: invalid_parameter"), _ok("grok")]
    d = pf.decide(checks, ALL)
    assert d.exit_code == 2 and d.blocked_by == ["Perplexity"]
    assert "instrumento" in d.reason


def test_modo_strict_mantem_comportamento_anterior():
    checks = [_ok("chatgpt"), _fail("claude", "HTTP 400: credit balance is too low"),
              _ok("gemini"), _ok("perplexity"), _ok("grok")]
    d = pf.decide(checks, ALL, mode="strict")
    assert d.exit_code == 2 and d.blocked_by == ["Claude"] and d.degraded == []


def test_opcional_falhando_nao_conta():
    checks = [_ok("chatgpt"), _ok("claude"), _fail("gemini", "HTTP 429: depleted"),
              _ok("perplexity"), _ok("grok")]
    d = pf.decide(checks, ALL - {"gemini"})
    assert d.exit_code == 0 and d.degraded == []


def test_record_partial_day_acrescenta_sem_apagar(tmp_path):
    p = tmp_path / "partial_days.json"
    pf.record_partial_day(str(p), "2026-09-10", ["Claude"], "HTTP 400 credit", "run 1")
    pf.record_partial_day(str(p), "2026-09-10", ["ChatGPT"], "HTTP 429", "run 2")
    entries = json.loads(p.read_text(encoding="utf-8"))
    assert [e["missingLLMs"] for e in entries] == [["Claude"], ["ChatGPT"]]
    assert entries[0]["date"] == "2026-09-10"


def test_export_env_escreve_github_env(tmp_path, monkeypatch, capsys):
    env_file = tmp_path / "env"
    monkeypatch.setenv("GITHUB_ENV", str(env_file))
    pf.export_env(["ChatGPT", "Gemini"], ["Claude"])
    txt = env_file.read_text(encoding="utf-8")
    assert "MANDATORY_LLMS=ChatGPT,Gemini\n" in txt
    assert "PAPERS_DEGRADED_LLMS=Claude\n" in txt


def test_main_em_degrade_grava_dia_parcial_sem_rede(tmp_path, monkeypatch):
    """Fim a fim com os checks substituídos: nenhuma chamada HTTP."""
    def fake(name, ok, err=None):
        return lambda key: pf.ProviderCheck(name, ok, 10, err)
    monkeypatch.setattr(pf, "check_openai", fake("chatgpt", True))
    monkeypatch.setattr(pf, "check_anthropic", fake("claude", False, "HTTP 400: credit balance is too low"))
    monkeypatch.setattr(pf, "check_google", fake("gemini", True))
    monkeypatch.setattr(pf, "check_perplexity", fake("perplexity", True))
    monkeypatch.setattr(pf, "check_grok", fake("grok", True))
    partial = tmp_path / "partial_days.json"
    monkeypatch.setenv("PAPERS_PARTIAL_DAYS_PATH", str(partial))
    monkeypatch.setenv("PAPERS_PREFLIGHT_MODE", "degrade")
    monkeypatch.delenv("GITHUB_ENV", raising=False)
    monkeypatch.delenv("MANDATORY_LLMS", raising=False)
    assert pf.main() == 0
    entries = json.loads(partial.read_text(encoding="utf-8"))
    assert entries[0]["missingLLMs"] == ["Claude"]
    assert "credit" in entries[0]["reason"]

    monkeypatch.setenv("PAPERS_PREFLIGHT_MODE", "strict")
    assert pf.main() == 2
