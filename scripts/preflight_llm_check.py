#!/usr/bin/env python3
"""preflight_llm_check.py — valida que TODAS as 5 LLMs respondem antes da coleta.

Motivacao (incidente 2026-04-24): Anthropic credit balance esgotado fez 30min
de fintech rodar sem Claude antes do FAILED_VERTICALS abortar. Resultado: gap
seletivo no vertical fintech para Claude na janela confirmatoria v2.

Comportamento: faz 1 chamada minima (1 token) para cada provider em
mandatory_llms(). Se qualquer provider falhar com 4xx (auth, quota, credit),
exit 2 ANTES da coleta comecar. Se todas responderem, exit 0.

Custo: ~5 chamadas de ~1 token = praticamente zero (<US$0.0001/run).

Exit codes:
    0 = todas as 5 LLMs OK
    2 = pelo menos 1 LLM falhou (failure critico — bloqueia coleta)
"""
from __future__ import annotations

import json
import os
import sys
import time
from dataclasses import dataclass
from typing import Callable, Optional

import httpx


@dataclass
class ProviderCheck:
    name: str
    ok: bool
    latency_ms: int
    error: Optional[str] = None


def _post_with_retry(name: str, do_post: Callable[[], httpx.Response]) -> ProviderCheck:
    # 1 retry com backoff 3s para 5xx ou erros de rede (transientes do provider).
    # 4xx NUNCA retenta — sao bugs nossos (payload invalido, auth, quota) e
    # retry apenas atrasa diagnostico. Boundary com APIs externas justifica
    # essa tolerancia para preservar a janela do paper (julho/2026).
    attempts = 2
    last_err: Optional[str] = None
    last_latency = 0
    for i in range(attempts):
        try:
            r = do_post()
            last_latency = int(r.elapsed.total_seconds() * 1000)
            if r.status_code == 200:
                return ProviderCheck(name, True, last_latency)
            if 500 <= r.status_code < 600 and i < attempts - 1:
                last_err = f"HTTP {r.status_code} (retry)"
                time.sleep(3)
                continue
            return ProviderCheck(name, False, last_latency, f"HTTP {r.status_code}: {r.text[:200]}")
        except (httpx.ConnectError, httpx.ReadTimeout, httpx.RemoteProtocolError, httpx.ConnectTimeout) as e:
            last_err = f"{type(e).__name__}: {e}"
            if i < attempts - 1:
                time.sleep(3)
                continue
            return ProviderCheck(name, False, 0, last_err)
        except Exception as e:
            return ProviderCheck(name, False, 0, f"{type(e).__name__}: {e}")
    return ProviderCheck(name, False, last_latency, last_err or "unknown")


# Endpoints e payloads minimos por provider. Cada chamada usa max_tokens=1
# (Anthropic exige >=1) e prompt curto. O objetivo e exercitar o auth +
# billing path sem gerar payload significativo.
def check_openai(key: str) -> ProviderCheck:
    if not key:
        return ProviderCheck("chatgpt", False, 0, "OPENAI_API_KEY ausente")
    return _post_with_retry("chatgpt", lambda: httpx.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {key}"},
        json={
            "model": "gpt-4o-mini-2024-07-18",
            "messages": [{"role": "user", "content": "ok"}],
            "max_tokens": 1,
            "temperature": 0,
        },
        timeout=15,
    ))


def check_anthropic(key: str) -> ProviderCheck:
    if not key:
        return ProviderCheck("claude", False, 0, "ANTHROPIC_API_KEY ausente")
    return _post_with_retry("claude", lambda: httpx.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json={
            "model": "claude-haiku-4-5-20251001",
            "max_tokens": 1,
            "messages": [{"role": "user", "content": "ok"}],
        },
        timeout=15,
    ))


def check_google(key: str) -> ProviderCheck:
    if not key:
        return ProviderCheck("gemini", False, 0, "GOOGLE_AI_API_KEY ausente")
    # Gemini 2.5 Pro thinking consome 1000-3000 tokens internos. maxOutputTokens
    # baixo retorna candidates sem 'parts'. Pre-flight valida AUTH apenas, nao
    # qualidade de output — usar 32 tokens evita cobertura zero por max_tokens.
    return _post_with_retry("gemini", lambda: httpx.post(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent",
        params={"key": key},
        json={
            "contents": [{"role": "user", "parts": [{"text": "ok"}]}],
            "generationConfig": {"maxOutputTokens": 32, "temperature": 0},
        },
        timeout=20,
    ))


def check_perplexity(key: str) -> ProviderCheck:
    if not key:
        return ProviderCheck("perplexity", False, 0, "PERPLEXITY_API_KEY ausente")
    # Perplexity sonar exige max_tokens>=16 desde validação 2026-05-18
    # (incidente run #26033337487: HTTP 400 invalid_parameter com max_tokens=1).
    return _post_with_retry("perplexity", lambda: httpx.post(
        "https://api.perplexity.ai/chat/completions",
        headers={"Authorization": f"Bearer {key}"},
        json={
            "model": "sonar",
            "messages": [{"role": "user", "content": "ok"}],
            "max_tokens": 16,
        },
        timeout=20,
    ))


def check_groq(key: str) -> ProviderCheck:
    if not key:
        return ProviderCheck("groq", False, 0, "GROQ_API_KEY ausente")
    return _post_with_retry("groq", lambda: httpx.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {key}"},
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": "ok"}],
            "max_tokens": 1,
            "temperature": 0,
        },
        timeout=15,
    ))


def main() -> int:
    print("=== preflight LLM check ===")
    print()

    checks = [
        check_openai(os.environ.get("OPENAI_API_KEY", "")),
        check_anthropic(os.environ.get("ANTHROPIC_API_KEY", "")),
        check_google(os.environ.get("GOOGLE_AI_API_KEY", "")),
        check_perplexity(os.environ.get("PERPLEXITY_API_KEY", "")),
        check_groq(os.environ.get("GROQ_API_KEY", "")),
    ]

    failed = [c for c in checks if not c.ok]

    for c in checks:
        if c.ok:
            print(f"  [OK]      {c.name:<11} {c.latency_ms}ms")
        else:
            print(f"  [FAIL]    {c.name:<11} {c.error}")

    print()

    if failed:
        names = ", ".join(c.name for c in failed)
        print(f"CRITICO: {len(failed)}/5 LLMs falharam: {names}")
        print("Coleta abortada para evitar dataset enviesado na janela confirmatoria v2.")
        print("Acoes possiveis:")
        print("  1. Verificar credit balance em cada provider (especialmente Anthropic)")
        print("  2. Confirmar que API keys nao foram rotacionadas")
        print("  3. Checar status pages: status.openai.com, status.anthropic.com, etc.")
        print()
        # Telemetria estruturada para parsing por monitoring/alerting
        print(json.dumps({
            "preflight_failed": True,
            "failed_providers": [c.name for c in failed],
            "errors": {c.name: c.error for c in failed},
        }))
        return 2

    print("Todas as 5 LLMs OK — prosseguindo com coleta.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
