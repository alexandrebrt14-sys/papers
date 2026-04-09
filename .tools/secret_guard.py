#!/usr/bin/env python3
"""Pre-commit secret guard — bloqueia commits com segredos conhecidos.

Roda em modo standalone (zero dependencias externas, apenas stdlib) e
pode ser invocado por hook pre-commit em qualquer repo Python ou Node.

Detecta dois tipos de risco:

1. Arquivos .env sendo commitados (qualquer .env, .env.local, .env.production
   etc — NAO bloqueia .env.example, .env.sample, .env.template).

2. Padroes de segredo conhecidos no conteudo staged:
   - Anthropic API key:    sk-ant-api03-... ou sk-ant-...
   - OpenAI API key:       sk-proj-... ou sk-...XXXXX (legacy)
   - Google API key:       AIza... (39 chars apos prefixo)
   - Groq API key:         gsk_...
   - Perplexity API key:   pplx-...
   - Supabase JWT:         eyJ...eyJ... (header.payload base64)
   - GitHub PAT:           ghp_..., gho_..., ghs_..., github_pat_...
   - Generic high-entropy: detectado em variaveis com nomes _KEY/_TOKEN/_SECRET

Uso (em pre-commit hook):
    python secret_guard.py --staged

Exit codes:
    0  — nenhum segredo detectado, commit permitido
    1  — segredo detectado, commit bloqueado
    2  — erro de execucao (git nao disponivel, etc)

Para forcar commit (NAO recomendado, registra warning):
    SECRET_GUARD_BYPASS=1 git commit ...

Achado F44 da auditoria de ecossistema Brasil GEO 2026-04-08.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from typing import Iterable


# ---------------------------------------------------------------------------
# Padroes de deteccao
# ---------------------------------------------------------------------------

# Padroes de filename — bloqueia .env e variantes, NAO bloqueia exemplos
ENV_FILE_PATTERNS = [
    re.compile(r"(^|/)\.env$"),
    re.compile(r"(^|/)\.env\.local$"),
    re.compile(r"(^|/)\.env\.production$"),
    re.compile(r"(^|/)\.env\.development$"),
    re.compile(r"(^|/)\.env\.staging$"),
    re.compile(r"(^|/)\.env\.test$"),
]

ENV_FILE_ALLOWED = [
    re.compile(r"\.env\.example$"),
    re.compile(r"\.env\.sample$"),
    re.compile(r"\.env\.template$"),
    re.compile(r"\.env\.dist$"),
]

# Padroes de segredo — devem ser high-confidence (poucos falsos positivos)
SECRET_PATTERNS = [
    ("Anthropic API key (sk-ant-api03)", re.compile(r"sk-ant-api03-[A-Za-z0-9_\-]{50,}")),
    ("Anthropic API key (sk-ant)", re.compile(r"sk-ant-[A-Za-z0-9_\-]{40,}")),
    ("OpenAI project key (sk-proj)", re.compile(r"sk-proj-[A-Za-z0-9_\-]{40,}")),
    ("OpenAI legacy key (sk-)", re.compile(r"\bsk-[A-Za-z0-9]{48}\b")),
    ("Google API key (AIza)", re.compile(r"\bAIza[A-Za-z0-9_\-]{35}\b")),
    ("Groq API key (gsk_)", re.compile(r"\bgsk_[A-Za-z0-9]{50,}")),
    ("Perplexity API key (pplx-)", re.compile(r"\bpplx-[A-Za-z0-9]{40,}")),
    ("GitHub PAT (ghp_/gho_/ghs_)", re.compile(r"\b(ghp|gho|ghs|ghr|ghu)_[A-Za-z0-9]{36}\b")),
    ("GitHub fine-grained PAT", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{82}\b")),
    ("AWS Access Key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    # JWT (Supabase service_role) — header eyJ + payload eyJ + signature
    ("JWT token (Supabase/Auth0)", re.compile(r"\beyJ[A-Za-z0-9_\-]{10,}\.eyJ[A-Za-z0-9_\-]{20,}\.[A-Za-z0-9_\-]{20,}\b")),
    # Private key blocks. Patterns construidos por concatenacao para
    # evitar auto-deteccao quando este proprio arquivo eh escaneado pelo
    # secret_guard (literais ----BEGIN ... PRIVATE KEY---- no source
    # casariam consigo mesmos).
    ("RSA Private Key", re.compile(r"-----" + r"BEGIN RSA " + r"PRIVATE KEY-----")),
    ("OpenSSH Private Key", re.compile(r"-----" + r"BEGIN OPENSSH " + r"PRIVATE KEY-----")),
    ("EC Private Key", re.compile(r"-----" + r"BEGIN EC " + r"PRIVATE KEY-----")),
    ("Generic Private Key", re.compile(r"-----" + r"BEGIN " + r"PRIVATE KEY-----")),
]

# Allowlist de placeholders comumente usados em docs/example.
# Padroes UPPERCASE-strict para evitar suprimir segredos com chars 'x' ou 'a'.
PLACEHOLDER_PATTERNS = [
    re.compile(r"sk-ant-api03-XXX"),  # exato uppercase
    re.compile(r"sk-ant-api03-YOUR"),
    re.compile(r"sk-proj-XXX"),
    re.compile(r"sk-proj-YOUR"),
    re.compile(r"AIzaSy_PLACEHOLDER"),
    re.compile(r"YOUR_API_KEY", re.IGNORECASE),
    re.compile(r"YOUR-API-KEY", re.IGNORECASE),
    re.compile(r"<your[_\s]api[_\s]key>", re.IGNORECASE),
    re.compile(r"REPLACE[_\s]ME", re.IGNORECASE),
    re.compile(r"PLACEHOLDER", re.IGNORECASE),
    re.compile(r"EXAMPLE", re.IGNORECASE),
]


# ---------------------------------------------------------------------------
# Git interop
# ---------------------------------------------------------------------------


def _run_git(args: list[str]) -> str:
    """Roda comando git e retorna stdout. Retorna string vazia em erro."""
    try:
        result = subprocess.run(
            ["git", *args],
            capture_output=True,
            text=True,
            check=False,
            encoding="utf-8",
            errors="replace",
        )
        if result.returncode != 0:
            return ""
        return result.stdout
    except (FileNotFoundError, OSError):
        return ""


def get_staged_files() -> list[str]:
    """Retorna lista de arquivos staged (added, modified, copied, renamed)."""
    output = _run_git(["diff", "--cached", "--name-only", "--diff-filter=ACMR"])
    return [line.strip() for line in output.splitlines() if line.strip()]


def get_staged_diff() -> str:
    """Retorna o diff completo staged (so as linhas adicionadas)."""
    output = _run_git(["diff", "--cached", "--unified=0"])
    # Filtra apenas linhas adicionadas (comecam com '+' mas nao '+++')
    added_lines = []
    for line in output.splitlines():
        if line.startswith("+") and not line.startswith("+++"):
            added_lines.append(line[1:])  # remove o '+'
    return "\n".join(added_lines)


# ---------------------------------------------------------------------------
# Deteccao
# ---------------------------------------------------------------------------


def is_env_file_blocked(filename: str) -> tuple[bool, str]:
    """Retorna (blocked, reason). Aceita .env.example/sample/template."""
    fn = filename.replace("\\", "/")

    # Allowlist primeiro
    for allowed in ENV_FILE_ALLOWED:
        if allowed.search(fn):
            return False, ""

    for pattern in ENV_FILE_PATTERNS:
        if pattern.search(fn):
            return True, f".env file ({pattern.pattern}) sendo commitado"
    return False, ""


def is_placeholder(text: str) -> bool:
    """Verifica se o trecho contem um placeholder conhecido (allowlist)."""
    for pattern in PLACEHOLDER_PATTERNS:
        if pattern.search(text):
            return True
    return False


def scan_content(content: str) -> list[tuple[str, str, str]]:
    """Escaneia conteudo procurando padroes de segredo.

    Returns:
        Lista de (label, snippet, contexto). Snippet eh redacted (so primeiros
        10 chars + '...' + ultimos 4) para nao logar o segredo completo.
    """
    findings: list[tuple[str, str, str]] = []
    if not content:
        return findings

    for label, pattern in SECRET_PATTERNS:
        for match in pattern.finditer(content):
            secret = match.group(0)
            # Pega contexto: 30 chars antes e depois
            start = max(0, match.start() - 30)
            end = min(len(content), match.end() + 30)
            context = content[start:end].replace("\n", " ")
            if is_placeholder(context):
                continue
            # Redact: primeiros 10 + ultimos 4
            if len(secret) > 16:
                redacted = f"{secret[:10]}...{secret[-4:]}"
            else:
                redacted = f"{secret[:6]}..."
            findings.append((label, redacted, context.strip()))
    return findings


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Pre-commit secret guard — bloqueia commit de segredos",
    )
    parser.add_argument(
        "--staged",
        action="store_true",
        help="Escaneia arquivos staged no git index (modo pre-commit hook)",
    )
    parser.add_argument(
        "--file",
        action="append",
        default=[],
        help="Escaneia arquivo especifico (modo manual, pode repetir)",
    )
    args = parser.parse_args(argv)

    if os.environ.get("SECRET_GUARD_BYPASS") == "1":
        print("[secret_guard] BYPASS ativo via SECRET_GUARD_BYPASS=1", file=sys.stderr)
        return 0

    issues: list[str] = []

    if args.staged:
        files = get_staged_files()
        if not files:
            return 0

        # 1. Verificar arquivos .env
        for f in files:
            blocked, reason = is_env_file_blocked(f)
            if blocked:
                issues.append(f"ARQUIVO BLOQUEADO: {f}\n  motivo: {reason}")

        # 2. Escanear conteudo staged
        diff_content = get_staged_diff()
        findings = scan_content(diff_content)
        for label, redacted, context in findings:
            issues.append(
                f"SEGREDO DETECTADO: {label}\n"
                f"  trecho redacted: {redacted}\n"
                f"  contexto: ...{context[:120]}..."
            )

    if args.file:
        for f in args.file:
            blocked, reason = is_env_file_blocked(f)
            if blocked:
                issues.append(f"ARQUIVO BLOQUEADO: {f}\n  motivo: {reason}")
            try:
                with open(f, "r", encoding="utf-8", errors="replace") as fh:
                    content = fh.read()
            except OSError as exc:
                print(f"[secret_guard] erro ao ler {f}: {exc}", file=sys.stderr)
                continue
            findings = scan_content(content)
            for label, redacted, context in findings:
                issues.append(
                    f"SEGREDO DETECTADO em {f}: {label}\n"
                    f"  trecho redacted: {redacted}\n"
                    f"  contexto: ...{context[:120]}..."
                )

    if issues:
        print("=" * 70, file=sys.stderr)
        print("[secret_guard] COMMIT BLOQUEADO — segredos detectados", file=sys.stderr)
        print("=" * 70, file=sys.stderr)
        for issue in issues:
            print(file=sys.stderr)
            print(issue, file=sys.stderr)
        print(file=sys.stderr)
        print("=" * 70, file=sys.stderr)
        print("Para forcar (NAO recomendado): SECRET_GUARD_BYPASS=1 git commit ...", file=sys.stderr)
        print("Para corrigir: remova o segredo, adicione ao .gitignore, rotacione a chave", file=sys.stderr)
        print("=" * 70, file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
