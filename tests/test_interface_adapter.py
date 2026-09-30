"""Braço de interface (Cloro): desligado por padrão, custo pelo header, tetos e falha ruidosa. Sem rede."""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import httpx
import pytest

from src.collection_policy import CollectionClosedError
from src.collectors.interface_adapter import (
    ENGINES,
    CloroInterfaceAdapter,
    InterfaceArmError,
    sqlite_outcome_sink,
)
from src.persistence.engine_health import failure_rates

FIXTURE = json.loads(
    (Path(__file__).parent / "fixtures" / "interface" / "cloro_chatgpt_br.json").read_text(encoding="utf-8")
)


def OPEN() -> None:
    """Política de um estudo com protocolo próprio (coleta aberta)."""


@pytest.fixture(autouse=True)
def sem_rede(monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("o teste tentou acessar a rede")
    monkeypatch.setattr(httpx.HTTPTransport, "handle_request", forbidden)
    for name in ["PAPERS_INTERFACE_ARM", "CLORO_API_KEY", "CLORO_ENGINES", "CLORO_COUNTRY",
                 "CLORO_USD_PER_CREDIT", "CLORO_MAX_USD_PER_RUN"]:
        monkeypatch.delenv(name, raising=False)


class FakeTracker:
    def __init__(self, allow=True):
        self.allow = allow
        self.records = []

    def can_spend(self, platform):
        assert platform == "cloro"
        return self.allow

    def record(self, **kwargs):
        self.records.append(kwargs)


def mock_client(handler_map):
    seen = []

    def handler(request):
        seen.append((request.url.path, json.loads(request.content), request.headers.get("authorization")))
        action = handler_map.get(request.url.path, handler_map.get("*"))
        if isinstance(action, Exception):
            raise action
        return action
    return httpx.Client(transport=httpx.MockTransport(handler)), seen


def ok(credits="7"):
    headers = {"X-Credits-Charged": credits} if credits is not None else {}
    return httpx.Response(200, json=FIXTURE, headers=headers)


def adapter(**kw):
    base = {"api_key": "test-key", "enabled": True, "policy_check": OPEN, "mandatory": set(),
            "usd_per_credit": 0.0004, "max_usd_per_run": 1.0}
    base.update(kw)
    return CloroInterfaceAdapter(**base)


def test_desligado_por_padrao_sem_chave_nao_faz_nada(monkeypatch):
    a = CloroInterfaceAdapter(policy_check=OPEN)
    assert not a.is_enabled()
    assert a.query("chatgpt", "melhor banco digital") is None
    assert a.query_all("melhor banco digital") == []
    monkeypatch.setenv("PAPERS_INTERFACE_ARM", "cloro")
    assert not CloroInterfaceAdapter(policy_check=OPEN).is_enabled()   # flag sem chave
    monkeypatch.delenv("PAPERS_INTERFACE_ARM")
    monkeypatch.setenv("CLORO_API_KEY", "test-key")
    assert not CloroInterfaceAdapter(policy_check=OPEN).is_enabled()   # chave sem flag
    monkeypatch.setenv("PAPERS_INTERFACE_ARM", "cloro")
    assert CloroInterfaceAdapter(policy_check=OPEN).is_enabled()


def test_no_papers_encerrado_recusa_antes_de_tudo_mesmo_com_chave(monkeypatch):
    monkeypatch.setenv("PAPERS_INTERFACE_ARM", "cloro")
    monkeypatch.setenv("CLORO_API_KEY", "test-key")
    a = CloroInterfaceAdapter(tracker=FakeTracker())
    with pytest.raises(CollectionClosedError, match="11/09/2026"):
        a.query("chatgpt", "x")
    with pytest.raises(CollectionClosedError):
        a.query_all("x")


def test_sucesso_com_custo_pelo_header_real():
    client, seen = mock_client({"*": ok("9")})
    tracker, outcomes = FakeTracker(), []
    a = adapter(http=client, tracker=tracker, outcome_sink=outcomes.append, run_id="r1")
    ans = a.query("chatgpt", "Qual o melhor banco digital?")
    assert ans.status == "success" and "Nubank" in ans.text and ans.model == "gpt-5-6"
    assert ans.credits_charged == 9 and ans.cost_source == "header"
    assert ans.cost_usd == pytest.approx(0.0036)
    assert "https://c6bank.com.br/conta-global" in ans.sources and len(ans.sources) == 4
    path, body, auth = seen[0]
    assert path == "/v1/monitor/chatgpt" and body["country"] == "BR" and auth == "Bearer test-key"
    rec = tracker.records[0]
    assert rec["platform"] == "cloro" and rec["cost_usd"] == pytest.approx(0.0036)
    assert outcomes[0].status == "success" and outcomes[0].arm == "interface"
    assert outcomes[0].engine == "Cloro-ChatGPT"


def test_ai_mode_usa_gl():
    client, seen = mock_client({"*": ok("6")})
    adapter(http=client).query("aimode", "x")
    assert seen[0][1]["gl"] == "BR" and "country" not in seen[0][1]


def test_sem_header_estima_pela_tabela():
    client, _ = mock_client({"*": ok(None)})
    ans = adapter(http=client).query("gemini", "x")
    assert ans.cost_source == "estimated" and ans.credits_charged == ENGINES["gemini"].credits


def test_falha_nao_registra_custo_e_segue_para_os_outros_motores():
    client, _ = mock_client({
        "/v1/monitor/chatgpt": httpx.ReadTimeout("lento"),
        "/v1/monitor/gemini": httpx.Response(502, json={"success": False}),
        "/v1/monitor/copilot": httpx.ConnectError("sem rota"),
        "*": ok("6"),
    })
    tracker, outcomes = FakeTracker(), []
    a = adapter(http=client, tracker=tracker, outcome_sink=outcomes.append)
    answers = a.query_all("x")
    assert [x.status for x in answers] == ["timeout", "failure", "failure", "success"]
    assert len(tracker.records) == 1 and tracker.records[0]["model"] == "cloro/aimode"
    assert [o.status for o in outcomes] == ["timeout", "failure", "failure", "success"]


def test_falha_ruidosa_quando_motor_e_obrigatorio():
    client, _ = mock_client({"*": httpx.Response(500, json={})})
    a = adapter(http=client, mandatory={"Cloro-Gemini"})
    assert a.query("chatgpt", "x").status == "failure"
    with pytest.raises(InterfaceArmError, match="Cloro-Gemini"):
        a.query("gemini", "x")


def test_pais_recusado_e_ignorado_sem_chamada():
    client, seen = mock_client({"*": ok()})
    ans = adapter(http=client, country="RU").query("chatgpt", "x")
    assert ans.status == "skipped" and seen == []


def test_tetos_de_gasto():
    client, seen = mock_client({"*": ok("7")})
    a = adapter(http=client, max_usd_per_run=0.005)       # cabe uma chamada de 7 créditos
    assert a.query("chatgpt", "x").status == "success"
    assert a.query("copilot", "x").status == "skipped"
    assert len(seen) == 1
    b = adapter(http=client, tracker=FakeTracker(allow=False))
    assert b.query("chatgpt", "x").status == "skipped" and len(seen) == 1


def test_perplexity_fora_da_lista_padrao_e_motor_desconhecido_recusado():
    assert "perplexity" not in adapter().engines
    with pytest.raises(ValueError):
        adapter(engines=("grok",))


def test_sink_sqlite_alimenta_taxa_de_falha(tmp_path):
    db = tmp_path / "t.db"
    client, _ = mock_client({"/v1/monitor/chatgpt": httpx.Response(500, json={}), "*": ok("6")})
    a = adapter(http=client, outcome_sink=sqlite_outcome_sink(str(db)))
    a.query_all("x")
    conn = sqlite3.connect(db)
    try:
        rates = {r.engine: r for r in failure_rates(conn)}
    finally:
        conn.close()
    assert rates["Cloro-ChatGPT"].failure == 1 and rates["Cloro-Gemini"].success == 1
