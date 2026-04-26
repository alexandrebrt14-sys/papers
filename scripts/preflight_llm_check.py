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
from dataclasses import dataclass
from typing import Optional

import httpx


@dataclass
class ProviderCheck:
    name: str
    ok: bool
    latency_ms: int
    error: Optional[str] = None


# Endpoints e payloads minimos por provider. Cada chamada usa max_tokens=1
# (Anthropic exige >=1) e prompt curto. O objetivo e exercitar o auth +
# billing path sem gerar payload significativo.
def check_openai(key: str) -> ProviderCheck:
    if not key:
        return ProviderCheck("chatgpt", False, 0, "OPENAI_API_KEY ausente")
    try:
        r = httpx.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {key}"},
            json={
                "model": "gpt-4o-mini-2024-07-18",
                "messages": [{"role": "user", "content": "ok"}],
                "max_tokens": 1,
                "temperature": 0,
            },
            timeout=15,
        )
        if r.status_code == 200:
            return ProviderCheck("chatgpt", True, int(r.elapsed.total_seconds() * 1000))
        return ProviderCheck("chatgpt", False, int(r.elapsed.total_seconds() * 1000),
                             f"HTTP {r.status_code}: {r.text[:200]}")
    except Exception as e:
        return ProviderCheck("chatgpt", False, 0, f"{type(e).__name__}: {e}")


def check_anthropic(key: str) -> ProviderCheck:
    if not key:
        return ProviderCheck("claude", False, 0, "ANTHROPIC_API_KEY ausente")
    try:
        r = httpx.post(
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
        )
        if r.status_code == 200:
            return ProviderCheck("claude", True, int(r.elapsed.total_seconds() * 1000))
        return ProviderCheck("claude", False, int(r.elapsed.total_seconds() * 1000),
                             f"HTTP {r.status_code}: {r.text[:200]}")
    except Exception as e:
        return ProviderCheck("claude", False, 0, f"{type(e).__name__}: {e}")


def check_google(key: str) -> ProviderCheck:
    if not key:
        return ProviderCheck("gemini", False, 0, "GOOGLE_AI_API_KEY ausente")
    try:
        # Gemini 2.5 Pro thinking consome 1000-3000 tokens internos. maxOutputTokens
        # baixo retorna candidates sem 'parts'. Pre-flight valida AUTH apenas, nao
        # qualidade de output — usar 32 tokens evita cobertura zero por max_tokens.
        r = httpx.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent",
            params={"key": key},
            json={
                "contents": [{"role": "user", "parts": [{"text": "ok"}]}],
                "generationConfig": {"maxOutputTokens": 32, "temperature": 0},
            },
            timeout=20,
        )
        if r.status_code == 200:
            return ProviderCheck("gemini", True, int(r.elapsed.total_seconds() * 1000))
        return ProviderCheck("gemini", False, int(r.elapsed.total_seconds() * 1000),
                             f"HTTP {r.status_code}: {r.text[:200]}")
    except Exception as e:
        return ProviderCheck("gemini", False, 0, f"{type(e).__name__}: {e}")


def check_perplexity(key: str) -> ProviderCheck:
    if not key:
        return ProviderCheck("perplexity", False, 0, "PERPLEXITY_API_KEY ausente")
    try:
        r = httpx.post(
            "https://api.perplexity.ai/chat/completions",
            headers={"Authorization": f"Bearer {key}"},
            json={
                "model": "sonar",
                "messages": [{"role": "user", "content": "ok"}],
                "max_tokens": 1,
            },
            timeout=20,
        )
        if r.status_code == 200:
            return ProviderCheck("perplexity", True, int(r.elapsed.total_seconds() * 1000))
        return ProviderCheck("perplexity", False, int(r.elapsed.total_seconds() * 1000),
                             f"HTTP {r.status_code}: {r.text[:200]}")
    except Exception as e:
        return ProviderCheck("perplexity", False, 0, f"{type(e).__name__}: {e}")


def check_groq(key: str) -> ProviderCheck:
    if not key:
        return ProviderCheck("groq", False, 0, "GROQ_API_KEY ausente")
    try:
        r = httpx.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {key}"},
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": "ok"}],
                "max_tokens": 1,
                "temperature": 0,
            },
            timeout=15,
        )
        if r.status_code == 200:
            return ProviderCheck("groq", True, int(r.elapsed.total_seconds() * 1000))
        return ProviderCheck("groq", False, int(r.elapsed.total_seconds() * 1000),
                             f"HTTP {r.status_code}: {r.text[:200]}")
    except Exception as e:
        return ProviderCheck("groq", False, 0, f"{type(e).__name__}: {e}")


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
