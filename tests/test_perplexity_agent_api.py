"""Gate da Agent API da Perplexity (POST /v1/agent).

A Sonar Chat Completions e retirada em 27/09/2026, dentro da janela de 90
dias. O braco Perplexity precisa continuar sendo o MESMO modelo (sonar) e
devolver a MESMA forma de LLMResponse — texto na janela, integra em raw_text,
fontes em `sources` — para que a serie nao mude de instrumento no meio.

Fixture da resposta copiada da sondagem ao vivo de 08/09/2026 (modelo
perplexity/sonar + tool web_search): fontes no item `search_results`, texto no
item `message`, annotations vazias.
"""
from __future__ import annotations

from datetime import datetime, timezone

import pytest

from src.collectors.llm_client import LLMClient, pplx_agent_api_enabled
from src.config import LLMConfig

AGENT_PAYLOAD = {
    "id": "resp_x",
    "object": "response",
    "status": "completed",
    "model": "perplexity/sonar",
    "output": [
        {
            "type": "search_results",
            "queries": ["melhores contas digitais PJ"],
            "results": [
                {"url": "https://a.example/1", "title": "A"},
                {"url": "https://b.example/2", "title": "B"},
                {"url": "https://a.example/1", "title": "A duplicada"},
            ],
        },
        {
            "type": "message",
            "role": "assistant",
            "status": "completed",
            "content": [
                {
                    "type": "output_text",
                    "text": "As mais citadas são Nubank PJ e Cora. " * 12,
                    "annotations": [
                        {"type": "url_citation", "url": "https://c.example/3"},
                    ],
                }
            ],
        },
    ],
    "usage": {
        "input_tokens": 3042,
        "output_tokens": 300,
        "cost": {"total_cost": 0.00401, "currency": "USD"},
    },
}


class _Resp:
    def __init__(self, payload: dict) -> None:
        self._payload = payload

    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict:
        return self._payload


class _Http:
    def __init__(self, payload: dict) -> None:
        self.payload = payload
        self.calls: list[dict] = []

    def post(self, url: str, headers: dict, json: dict) -> _Resp:
        self.calls.append({"url": url, "headers": headers, "json": json})
        return _Resp(self.payload)


def _llm() -> LLMConfig:
    return LLMConfig(
        name="Perplexity", provider="perplexity", model="sonar",
        api_key="pplx-test", input_cost_per_mtok=1.0, output_cost_per_mtok=1.0,
        max_output_tokens=300,
    )


def test_gate_default_desligado(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("PAPERS_PPLX_AGENT_API", raising=False)
    assert pplx_agent_api_enabled() is False
    monkeypatch.setenv("PAPERS_PPLX_AGENT_API", "1")
    assert pplx_agent_api_enabled() is True
    monkeypatch.setenv("PAPERS_PPLX_AGENT_API", "0")
    assert pplx_agent_api_enabled() is False


def test_parse_output_separa_texto_citacoes_e_hits() -> None:
    text, cited, hits = LLMClient._parse_pplx_agent_output(AGENT_PAYLOAD["output"])
    assert text.startswith("As mais citadas são Nubank PJ e Cora.")
    assert cited == ["https://c.example/3"]
    assert hits == ["https://a.example/1", "https://b.example/2", "https://a.example/1"]


def test_gate_ligado_usa_v1_agent_com_o_mesmo_modelo(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PAPERS_PPLX_AGENT_API", "1")
    monkeypatch.delenv("PAPERS_CITATION_WINDOW_CHARS", raising=False)
    client = LLMClient(cohort=["Nubank", "Cora"])
    http = _Http(AGENT_PAYLOAD)
    client._http = http  # type: ignore[assignment]
    # Transporte falso instalado: preserva o teste do contrato histórico.
    monkeypatch.setattr("src.collectors.llm_client.require_collection_open", lambda: None)

    start = datetime.now(timezone.utc)
    resp = client._query_perplexity(_llm(), "Quais fintechs PJ?", start)

    call = http.calls[0]
    assert call["url"] == "https://api.perplexity.ai/v1/agent"
    assert call["json"]["model"] == "perplexity/sonar"
    assert "preset" not in call["json"], "preset roteia para modelo de terceiros"
    assert call["json"]["tools"] == [{"type": "web_search"}]
    assert call["json"]["input"] == "Quais fintechs PJ?"
    assert call["json"]["instructions"]
    assert call["headers"]["Authorization"] == "Bearer pplx-test"

    # Mesma forma que a rota legada devolve.
    assert resp.model == "sonar"
    assert resp.provider == "perplexity"
    assert resp.engine_type == "rag"
    assert len(resp.response_text) == 200, "janela de citacao aplicada"
    assert resp.raw_text.startswith("As mais citadas são")
    assert len(resp.raw_text) > 200, "integra preservada em raw_text"
    # Citadas primeiro, hits depois, sem duplicata.
    assert resp.sources == [
        "https://c.example/3", "https://a.example/1", "https://b.example/2",
    ]
    assert resp.input_tokens == 3042 and resp.output_tokens == 300
    assert "Nubank" in resp.cited_entities and "Cora" in resp.cited_entities
    assert resp.raw is AGENT_PAYLOAD


def test_gate_desligado_mantem_rota_legada(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PAPERS_PPLX_AGENT_API", "0")
    legacy = {
        "choices": [{"message": {"content": "Nubank lidera."}}],
        "citations": ["https://d.example/4"],
        "usage": {"prompt_tokens": 10, "completion_tokens": 5},
    }
    client = LLMClient(cohort=["Nubank"])
    http = _Http(legacy)
    client._http = http  # type: ignore[assignment]
    # Transporte falso instalado: preserva o teste do contrato histórico.
    monkeypatch.setattr("src.collectors.llm_client.require_collection_open", lambda: None)
    resp = client._query_perplexity(_llm(), "q", datetime.now(timezone.utc))
    assert http.calls[0]["url"] == "https://api.perplexity.ai/chat/completions"
    assert resp.sources == ["https://d.example/4"]


def test_resposta_sem_message_falha_alto(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PAPERS_PPLX_AGENT_API", "1")
    client = LLMClient(cohort=["Nubank"])
    client._http = _Http({"status": "completed", "output": [], "usage": {}})  # type: ignore[assignment]
    # Transporte falso instalado: preserva o teste do contrato histórico.
    monkeypatch.setattr("src.collectors.llm_client.require_collection_open", lambda: None)
    with pytest.raises(RuntimeError, match="sem item message"):
        client._query_perplexity(_llm(), "q", datetime.now(timezone.utc))


class _HttpErro(_Http):
    class _RespErro(_Resp):
        def raise_for_status(self) -> None:
            raise RuntimeError("HTTP 401 insufficient_quota")

    def post(self, url: str, headers: dict, json: dict) -> _Resp:
        self.calls.append({"url": url, "headers": headers, "json": json})
        return self._RespErro(self.payload)


def test_erro_http_do_v1_agent_propaga_para_o_circuit_breaker(monkeypatch: pytest.MonkeyPatch) -> None:
    """Sem saldo, a nova rota falha alto como a legada: quem trata e o chamador."""
    monkeypatch.setenv("PAPERS_PPLX_AGENT_API", "1")
    client = LLMClient(cohort=["Nubank"])
    client._http = _HttpErro({})  # type: ignore[assignment]
    # Transporte falso instalado: preserva o teste do contrato histórico.
    monkeypatch.setattr("src.collectors.llm_client.require_collection_open", lambda: None)
    with pytest.raises(RuntimeError, match="insufficient_quota"):
        client._query_perplexity(_llm(), "q", datetime.now(timezone.utc))


def test_preflight_sonda_a_rota_que_a_coleta_vai_usar(monkeypatch: pytest.MonkeyPatch) -> None:
    import importlib.util
    import sys
    from pathlib import Path

    import httpx

    spec = importlib.util.spec_from_file_location(
        "preflight_llm_check_pplx",
        Path(__file__).resolve().parent.parent / "scripts" / "preflight_llm_check.py",
    )
    pf = importlib.util.module_from_spec(spec)
    sys.modules["preflight_llm_check_pplx"] = pf
    spec.loader.exec_module(pf)

    calls: list[str] = []

    def fake_post(url, **kwargs):
        calls.append(url)
        r = httpx.Response(200, request=httpx.Request("POST", url))
        r.elapsed = __import__("datetime").timedelta(milliseconds=5)
        return r

    monkeypatch.setattr(pf.httpx, "post", fake_post)
    monkeypatch.setattr(pf, "require_collection_open", lambda: None)
    monkeypatch.setenv("PAPERS_PPLX_AGENT_API", "1")
    assert pf.check_perplexity("pplx-test").ok
    monkeypatch.setenv("PAPERS_PPLX_AGENT_API", "0")
    assert pf.check_perplexity("pplx-test").ok
    assert calls == [
        "https://api.perplexity.ai/v1/agent",
        "https://api.perplexity.ai/chat/completions",
    ]
