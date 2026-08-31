"""Incidente 2026-08-31 — o Grok estourava o timeout da coleta diária.

grok-4.6 raciocina por padrão e o reasoning é cobrado como output. Medido
contra a API com a mesma query de citação da coleta: 73,7s e 2.746 reasoning
tokens sem o parâmetro, contra 19,7s e 419 com `reasoning_effort=low`. Na run
33303260035 o Grok consumiu 129 dos 179 minutos de wall-clock e o job morreu no
timeout de 180min — cinco runs seguidas canceladas entre 24 e 30/08 sem
persistir um único dia da série.

Estes testes fixam o contrato do body enviado ao endpoint xAI. Sem rede: o
cliente HTTP é substituído por um duplo que apenas captura o payload.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import pytest

from src.collectors.llm_client import LLMClient
from src.config import LLMConfig


class _FakeResponse:
    status_code = 200

    def __init__(self) -> None:
        self.captured: dict[str, Any] = {}

    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict[str, Any]:
        return {
            "choices": [{"message": {"content": "Nubank e Inter lideram."}}],
            "usage": {"prompt_tokens": 10, "completion_tokens": 20},
        }


class _FakeHTTP:
    def __init__(self) -> None:
        self.body: dict[str, Any] | None = None

    def post(self, url: str, headers: dict[str, str], json: dict[str, Any]) -> _FakeResponse:
        self.body = json
        return _FakeResponse()


def _grok() -> LLMConfig:
    return LLMConfig(
        name="Grok", provider="xai", model="grok-4.6",
        api_key="test-key", input_cost_per_mtok=2.00, output_cost_per_mtok=6.00,
        max_output_tokens=800, supports_json_mode=True,
    )


def _capture_body(monkeypatch: pytest.MonkeyPatch, env: str | None) -> dict[str, Any]:
    if env is None:
        monkeypatch.delenv("XAI_REASONING_EFFORT", raising=False)
    else:
        monkeypatch.setenv("XAI_REASONING_EFFORT", env)
    client = LLMClient()
    fake = _FakeHTTP()
    client._http = fake  # type: ignore[assignment]
    client._query_xai(_grok(), "Melhores fintechs do Brasil?", datetime.now(timezone.utc))
    assert fake.body is not None
    return fake.body


def test_reasoning_effort_low_por_padrao(monkeypatch: pytest.MonkeyPatch) -> None:
    """Sem a env, o body precisa sair com "low" — é o default que cabe no timeout."""
    body = _capture_body(monkeypatch, None)
    assert body["reasoning_effort"] == "low"


def test_repo_var_sobrescreve_o_default(monkeypatch: pytest.MonkeyPatch) -> None:
    """Operador consegue subir o esforço sem tocar em código."""
    body = _capture_body(monkeypatch, "high")
    assert body["reasoning_effort"] == "high"


def test_env_vazia_restaura_comportamento_anterior(monkeypatch: pytest.MonkeyPatch) -> None:
    """Escape hatch: string vazia omite o parâmetro em vez de mandar "" à API."""
    body = _capture_body(monkeypatch, "")
    assert "reasoning_effort" not in body


def test_model_pinning_preservado(monkeypatch: pytest.MonkeyPatch) -> None:
    """O fix limita o raciocínio; não pode trocar o modelo pinado da série."""
    body = _capture_body(monkeypatch, None)
    assert body["model"] == "grok-4.6"
    assert body["temperature"] == 0.0
    assert body["max_tokens"] == 800
