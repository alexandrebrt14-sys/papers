#!/usr/bin/env python3
"""preflight_llm_check.py — sonda os 5 provedores antes da coleta e decide
se o dia roda completo, parcial ou nao roda.

Motivacao (incidente 2026-04-24): Anthropic credit balance esgotado fez 30min
de fintech rodar sem Claude antes do FAILED_VERTICALS abortar. Resultado: gap
seletivo no vertical fintech para Claude na janela confirmatoria v2.

Degradacao graciosa (2026-09-09): entre 16/08 e 08/09 o preflight abortou 28
runs por saldo de UM provedor e a serie perdeu 17 dias inteiros — os outros
quatro bracos tinham credito e nao coletaram nada. Um dia com 4 de 5 bracos,
marcado como parcial, vale mais para a serie longitudinal do que um dia vazio.
Comportamento, controlado por variavel:

  PAPERS_PREFLIGHT_MODE=degrade (padrao)
      Provedor obrigatorio que falha por CREDITO/QUOTA/AUTH (HTTP 400 com
      "credit"/"quota", 401, 402, 403, 429, ou chave ausente) vira "degradado":
      sai de MANDATORY_LLMS para os passos seguintes (via GITHUB_ENV) e o dia e
      registrado em data/partial_days.json, que o dashboard publica como
      `partialDays`. A coleta so prossegue se sobrarem >= PAPERS_MIN_LLMS
      (padrao 2) provedores OK; abaixo disso, exit 2 como antes.
      Falha que NAO e de saldo (5xx persistente, rede, payload) continua
      bloqueando: e defeito de instrumento, nao decisao de billing.
  PAPERS_PREFLIGHT_MODE=strict
      Comportamento anterior: qualquer obrigatorio falhando = exit 2.

Custo: ~5 chamadas de ~1 token = praticamente zero (<US$0.0001/run).

Exit codes:
    0 = coleta pode prosseguir (completa, ou parcial em modo degrade)
    2 = coleta bloqueada
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
    # Mesma chave do coletor: com PAPERS_PPLX_AGENT_API=1 o preflight sonda a
    # rota que a coleta vai usar (POST /v1/agent, modelo perplexity/sonar).
    # A rota legada /chat/completions e retirada em 27/09/2026.
    if os.getenv("PAPERS_PPLX_AGENT_API", "0").strip() == "1":
        return _post_with_retry("perplexity", lambda: httpx.post(
            "https://api.perplexity.ai/v1/agent",
            headers={"Authorization": f"Bearer {key}"},
            json={
                "model": "perplexity/sonar",
                "input": "ok",
                "max_output_tokens": 16,
            },
            timeout=30,
        ))
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


def check_grok(key: str) -> ProviderCheck:
    # grok-4.6 raciocina por padrão: max_tokens baixo não corta o content,
    # mas 16 dá folga e o custo do probe segue desprezível.
    if not key:
        return ProviderCheck("grok", False, 0, "XAI_API_KEY ausente")
    return _post_with_retry("grok", lambda: httpx.post(
        "https://api.x.ai/v1/chat/completions",
        headers={"Authorization": f"Bearer {key}"},
        json={
            "model": "grok-4.6",
            "messages": [{"role": "user", "content": "ok"}],
            "max_tokens": 16,
            "temperature": 0,
        },
        timeout=30,
    ))


# Nomes como aparecem em MANDATORY_LLMS (src/config.mandatory_llms), indexados
# pelo nome minusculo que os checks usam.
CANONICAL_NAMES = {
    "chatgpt": "ChatGPT",
    "claude": "Claude",
    "gemini": "Gemini",
    "perplexity": "Perplexity",
    "grok": "Grok",
}

# Erros que significam "conta sem saldo/quota/permissao": degradaveis. O resto
# (5xx, rede, payload invalido) e defeito de instrumento e continua bloqueando.
_BILLING_STATUS = ("http 401", "http 402", "http 403", "http 429")
_BILLING_HINTS = ("credit", "quota", "billing", "prepayment", "insufficient")


def _canon(name: str) -> str:
    return CANONICAL_NAMES.get(name.lower(), name)


def is_billing_failure(error: Optional[str]) -> bool:
    """True quando o erro e de saldo/quota/permissao, nao de instrumento."""
    if not error:
        return False
    e = error.lower()
    if e.startswith(_BILLING_STATUS):
        return True
    if e.startswith("http 400") and any(h in e for h in _BILLING_HINTS):
        return True
    # Chave ausente no ambiente ("OPENAI_API_KEY ausente"): sem chave nao ha
    # como o braco responder — indisponibilidade do provedor, nao bug nosso.
    return e.endswith("ausente")


@dataclass
class Decision:
    exit_code: int
    degraded: list[str]          # nomes canonicos removidos de MANDATORY_LLMS
    remaining_mandatory: list[str]
    blocked_by: list[str]        # obrigatorios com falha nao degradavel
    reason: str


def decide(
    checks: list[ProviderCheck],
    mandatory: set[str],
    mode: str = "degrade",
    min_llms: int = 2,
) -> Decision:
    """Regra pura, sem rede, para o teste cobrir as saidas.

    `mandatory` e o conjunto em minusculas (ex.: {"chatgpt", "claude"}).
    """
    ok = [c for c in checks if c.ok]
    failed_mandatory = [c for c in checks if not c.ok and c.name.lower() in mandatory]
    failed_names = {c.name.lower() for c in failed_mandatory}
    remaining = sorted(_canon(n) for n in mandatory if n not in failed_names)
    if not failed_mandatory:
        return Decision(0, [], remaining, [], "todos os obrigatorios OK")

    if mode != "degrade":
        return Decision(2, [], remaining, [_canon(c.name) for c in failed_mandatory],
                        "modo strict: obrigatorio falhou")

    billing = [c for c in failed_mandatory if is_billing_failure(c.error)]
    hard = [c for c in failed_mandatory if not is_billing_failure(c.error)]
    if hard:
        return Decision(2, [], remaining, [_canon(c.name) for c in hard],
                        "falha nao e de saldo (defeito de instrumento)")
    if len(ok) < min_llms:
        return Decision(2, [], remaining, [_canon(c.name) for c in billing],
                        f"restaram {len(ok)} provedores OK, minimo {min_llms}")
    degraded = sorted(_canon(c.name) for c in billing)
    return Decision(0, degraded, remaining, [],
                    "coleta parcial: provedores sem saldo removidos")


def record_partial_day(path: str, day: str, degraded: list[str], reason: str,
                       source: str) -> None:
    """Acrescenta a entrada do dia em data/partial_days.json (lista JSON)."""
    entries: list[dict] = []
    if os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as fh:
                entries = json.load(fh) or []
        except (OSError, json.JSONDecodeError):
            entries = []
    entries.append({
        "date": day,
        "missingLLMs": degraded,
        "reason": reason,
        "source": source,
    })
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(entries, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def export_env(remaining_mandatory: list[str], degraded: list[str]) -> None:
    """Propaga a decisao aos passos seguintes do job via GITHUB_ENV.

    GITHUB_ENV sobrepoe o `env:` do workflow para os passos seguintes, entao
    `collect`, `validate-run` e `validate_v2_collection` passam a exigir so os
    bracos que responderam. Fora do Actions, so imprime.
    """
    lines = [
        f"MANDATORY_LLMS={','.join(remaining_mandatory)}",
        f"PAPERS_DEGRADED_LLMS={','.join(degraded)}",
    ]
    env_file = os.environ.get("GITHUB_ENV")
    if env_file:
        with open(env_file, "a", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")
    for ln in lines:
        print(f"  export {ln}")


def main() -> int:
    from datetime import datetime, timezone

    print("=== preflight LLM check ===")
    print()

    checks = [
        check_openai(os.environ.get("OPENAI_API_KEY", "")),
        check_anthropic(os.environ.get("ANTHROPIC_API_KEY", "")),
        check_google(os.environ.get("GOOGLE_AI_API_KEY", "")),
        check_perplexity(os.environ.get("PERPLEXITY_API_KEY", "")),
        check_grok(os.environ.get("XAI_API_KEY", "")),
    ]

    mandatory = {
        n.strip().lower()
        for n in os.getenv("MANDATORY_LLMS", "ChatGPT,Claude,Gemini,Perplexity,Grok").split(",")
        if n.strip()
    }
    mode = os.getenv("PAPERS_PREFLIGHT_MODE", "degrade").strip().lower()
    min_llms = int(os.getenv("PAPERS_MIN_LLMS", "2") or 2)

    decision = decide(checks, mandatory, mode, min_llms)
    failed = [c for c in checks if not c.ok]

    for c in checks:
        if c.ok:
            print(f"  [OK]      {c.name:<11} {c.latency_ms}ms")
        elif _canon(c.name) in decision.degraded:
            print(f"  [DEGRAD]  {c.name:<11} (sem saldo; removido deste dia) {c.error}")
        elif c.name.lower() in mandatory:
            print(f"  [FAIL]    {c.name:<11} {c.error}")
        else:
            print(f"  [WARN]    {c.name:<11} (opcional/degradado) {c.error}")

    print()

    if failed:
        # Telemetria estruturada para parsing por monitoring/alerting.
        print(json.dumps({
            "preflight_failed": decision.exit_code != 0,
            "preflight_mode": mode,
            "failed_providers": decision.blocked_by,
            "degraded_providers": decision.degraded,
            "remaining_mandatory": decision.remaining_mandatory,
            "optional_degraded": [
                c.name for c in failed if c.name.lower() not in mandatory
            ],
            "errors": {c.name: c.error for c in failed},
        }))
        print()

    if decision.exit_code != 0:
        print(f"CRITICO: coleta bloqueada — {decision.reason}: {', '.join(decision.blocked_by)}")
        print("Acoes possiveis:")
        print("  1. Verificar credit balance em cada provider (especialmente Anthropic)")
        print("  2. Confirmar que API keys nao foram rotacionadas")
        print("  3. Checar status pages: status.openai.com, status.anthropic.com, etc.")
        print("  4. Se a falha for de saldo e PAPERS_PREFLIGHT_MODE=strict, considere degrade.")
        return 2

    if decision.degraded:
        today = datetime.now(timezone.utc).date().isoformat()
        reasons = "; ".join(
            f"{_canon(c.name)}: {c.error}" for c in failed
            if _canon(c.name) in decision.degraded
        )
        run_url = ""
        if os.getenv("GITHUB_SERVER_URL"):
            run_url = (
                f"{os.getenv('GITHUB_SERVER_URL')}/{os.getenv('GITHUB_REPOSITORY')}"
                f"/actions/runs/{os.getenv('GITHUB_RUN_ID')}"
            )
        record_partial_day(
            os.getenv("PAPERS_PARTIAL_DAYS_PATH", "data/partial_days.json"),
            today, decision.degraded, reasons, run_url or "preflight local",
        )
        export_env(decision.remaining_mandatory, decision.degraded)
        print(f"AVISO: dia {today} marcado como PARCIAL sem {', '.join(decision.degraded)}.")
        print("  Coleta prossegue com os provedores restantes; reabasteca o saldo para")
        print("  restaurar a cobertura completa. O dashboard publica o dia em partialDays.")
        return 0

    optional_failed = [c for c in failed if c.name.lower() not in mandatory]
    if optional_failed:
        names = ", ".join(c.name for c in optional_failed)
        print(f"AVISO: provider(s) OPCIONAL(is) degradado(s): {names} — coleta prossegue.")
        return 0

    print("Todas as LLMs mandatory OK — prosseguindo com coleta.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
