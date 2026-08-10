#!/usr/bin/env python3
"""r2_sync.py — sincroniza data/papers.db com o Cloudflare R2 (source of truth).

Substitui a implementacao anterior baseada em boto3 + credenciais S3. O token
de API do Cloudflare disponivel para este projeto nao tem permissao para criar
tokens R2 filhos, entao usamos a REST API de objetos do R2, que autentica com
o mesmo Bearer token ja usado no resto da automacao Cloudflare.

Secrets necessarios (3, contra os 4 do modelo S3):
    CLOUDFLARE_API_TOKEN  — token com permissao de R2 na conta
    CF_ACCOUNT_ID         — id da conta Cloudflare
    R2_BUCKET             — nome do bucket (papers-research-db)

Subcomandos:
    pull    baixa papers/db/latest.db e adota a base MAIOR (forward-only)
    push    valida integridade e sobe latest.db + copia datada com sha256
    verify  confere que o latest.db remoto casa com o local por sha256

Politica forward-only: o banco NUNCA encolhe. Se a base remota tiver menos
linhas que a local, a local prevalece e vice-versa. Foi assim que o incidente
2026-08-09 (weeklies sobrescrevendo papers-db-latest com 864 de 63.940
citations) passou despercebido por dois ciclos semanais.

Exit codes:
    0 = ok
    1 = erro de configuracao ou transporte
    2 = guard de integridade barrou a operacao
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import os
import sqlite3
import sys
import tempfile

import httpx

API = "https://api.cloudflare.com/client/v4"
KEY_LATEST = "papers/db/latest.db"
PREFIX_HISTORY = "papers/db/history/"
TIMEOUT = httpx.Timeout(900.0, connect=30.0)

# Acima disso o upload single-part da REST API fica arriscado. O banco cresce
# ~1 MB/semana, entao o aviso da meses de antecedencia para migrar a multipart.
SIZE_WARN_BYTES = 250 * 1024 * 1024


def _cfg() -> tuple[str, str, str]:
    token = os.environ.get("CLOUDFLARE_API_TOKEN", "").strip()
    account = os.environ.get("CF_ACCOUNT_ID", "").strip()
    bucket = os.environ.get("R2_BUCKET", "").strip()
    missing = [
        n
        for n, v in (
            ("CLOUDFLARE_API_TOKEN", token),
            ("CF_ACCOUNT_ID", account),
            ("R2_BUCKET", bucket),
        )
        if not v
    ]
    if missing:
        required = os.environ.get("R2_REQUIRED", "").strip() == "1"
        msg = f"R2 nao configurado — secrets ausentes: {', '.join(missing)}"
        if required:
            print(f"ERRO: {msg}", file=sys.stderr)
            print("R2_REQUIRED=1 exige backup off-site. Abortando.", file=sys.stderr)
            raise SystemExit(1)
        print(f"AVISO: {msg} — seguindo apenas com artifact do Actions.")
        raise SystemExit(0)
    return token, account, bucket


def _url(account: str, bucket: str, key: str) -> str:
    return f"{API}/accounts/{account}/r2/buckets/{bucket}/objects/{key}"


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def total_rows(path: str) -> int:
    """Soma linhas de todas as tabelas. -1 se o arquivo nao abre como SQLite."""
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return -1
    try:
        con = sqlite3.connect(path)
        try:
            cur = con.cursor()
            total = 0
            for (name,) in cur.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall():
                try:
                    total += cur.execute(f'SELECT COUNT(*) FROM "{name}"').fetchone()[0]
                except sqlite3.Error:
                    continue
            return total
        finally:
            con.close()
    except sqlite3.Error:
        return -1


def citation_rows(path: str) -> int:
    if not os.path.exists(path):
        return -1
    try:
        con = sqlite3.connect(path)
        try:
            return con.execute("SELECT COUNT(*) FROM citations").fetchone()[0]
        except sqlite3.Error:
            return 0
        finally:
            con.close()
    except sqlite3.Error:
        return -1


def cmd_pull(args: argparse.Namespace) -> int:
    token, account, bucket = _cfg()
    local = args.db
    tmp_fd, tmp = tempfile.mkstemp(suffix=".db", dir=os.path.dirname(local) or ".")
    os.close(tmp_fd)
    try:
        with httpx.Client(timeout=TIMEOUT) as client:
            with client.stream(
                "GET",
                _url(account, bucket, KEY_LATEST),
                headers={"Authorization": f"Bearer {token}"},
            ) as r:
                if r.status_code == 404:
                    print("R2 latest.db ainda nao existe — mantendo base local.")
                    return 0
                if r.status_code != 200:
                    body = r.read()[:300].decode("utf-8", "replace")
                    print(f"AVISO: R2 GET HTTP {r.status_code}: {body}")
                    print("Mantendo base local (R2 indisponivel nao derruba o run).")
                    return 0
                with open(tmp, "wb") as f:
                    for chunk in r.iter_bytes(1 << 20):
                        f.write(chunk)

        r_remote, r_local = total_rows(tmp), total_rows(local)
        c_remote, c_local = citation_rows(tmp), citation_rows(local)
        print(f"linhas totais: local={r_local}  R2={r_remote}")
        print(f"citations:     local={c_local}  R2={c_remote}")

        if r_remote > r_local:
            os.replace(tmp, local)
            print(f"Base do R2 adotada ({r_remote} > {r_local} linhas) — forward-only.")
        else:
            print("Base local mantida (>= R2).")
        return 0
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def cmd_push(args: argparse.Namespace) -> int:
    token, account, bucket = _cfg()
    local = args.db
    if not os.path.exists(local):
        print(f"ERRO: {local} nao existe — nada a subir.", file=sys.stderr)
        return 1

    rows = total_rows(local)
    cites = citation_rows(local)
    if rows < 0:
        print(f"ERRO: {local} nao abre como SQLite valido.", file=sys.stderr)
        return 2

    # Guard de regressao: nunca sobrescreve o remoto com uma base menor.
    tmp_fd, tmp = tempfile.mkstemp(suffix=".db", dir=os.path.dirname(local) or ".")
    os.close(tmp_fd)
    try:
        with httpx.Client(timeout=TIMEOUT) as client:
            with client.stream(
                "GET",
                _url(account, bucket, KEY_LATEST),
                headers={"Authorization": f"Bearer {token}"},
            ) as r:
                if r.status_code == 200:
                    with open(tmp, "wb") as f:
                        for chunk in r.iter_bytes(1 << 20):
                            f.write(chunk)
                    r_remote = total_rows(tmp)
                    c_remote = citation_rows(tmp)
                    if rows < r_remote:
                        print(
                            f"BLOQUEADO: base local ({rows} linhas, {cites} citations) "
                            f"e MENOR que o R2 ({r_remote} linhas, {c_remote} citations).",
                            file=sys.stderr,
                        )
                        print(
                            "Upload recusado para nao destruir a serie longitudinal.",
                            file=sys.stderr,
                        )
                        return 2
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)

    size = os.path.getsize(local)
    if size > SIZE_WARN_BYTES:
        print(
            f"AVISO: papers.db esta em {size / 1048576:.0f} MB. Acima de ~300 MB o "
            "upload single-part da REST API falha — migrar para multipart."
        )

    digest = sha256_file(local)
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    # As copias datadas ficam sob history/ para que a lifecycle rule do bucket
    # possa expira-las sem tocar em latest.db, que precisa viver para sempre.
    # Sao ~105 MB por run e dois runs por dia; sem expiracao isso vira 6 GB/mes.
    keys = [KEY_LATEST, f"{PREFIX_HISTORY}{stamp}-{digest[:8]}.db"]

    with httpx.Client(timeout=TIMEOUT) as client:
        for key in keys:
            with open(local, "rb") as f:
                resp = client.put(
                    _url(account, bucket, key),
                    headers={
                        "Authorization": f"Bearer {token}",
                        "Content-Type": "application/octet-stream",
                    },
                    content=f,
                )
            if resp.status_code != 200:
                print(
                    f"ERRO: upload de {key} falhou HTTP {resp.status_code}: "
                    f"{resp.text[:300]}",
                    file=sys.stderr,
                )
                return 1
            print(f"R2 upload OK -> {key} ({size} bytes, {cites} citations)")

    print(f"sha256={digest}")
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    token, account, bucket = _cfg()
    local = args.db
    local_digest = sha256_file(local) if os.path.exists(local) else None

    tmp_fd, tmp = tempfile.mkstemp(suffix=".db", dir=os.path.dirname(local) or ".")
    os.close(tmp_fd)
    try:
        with httpx.Client(timeout=TIMEOUT) as client:
            with client.stream(
                "GET",
                _url(account, bucket, KEY_LATEST),
                headers={"Authorization": f"Bearer {token}"},
            ) as r:
                if r.status_code != 200:
                    print(f"ERRO: R2 GET HTTP {r.status_code}", file=sys.stderr)
                    return 1
                with open(tmp, "wb") as f:
                    for chunk in r.iter_bytes(1 << 20):
                        f.write(chunk)

        remote_digest = sha256_file(tmp)
        print(f"local  sha256={local_digest} rows={total_rows(local)}")
        print(f"R2     sha256={remote_digest} rows={total_rows(tmp)}")
        if local_digest == remote_digest:
            print("IDENTICOS — backup off-site confirmado.")
            return 0
        print("DIVERGENTES — local e R2 diferem (esperado apos coleta nova).")
        return 0
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def main() -> int:
    # Flag replicada nos subparsers para aceitar as duas ordens de chamada.
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--db", default=os.environ.get("PAPERS_DB_PATH", "data/papers.db"))

    p = argparse.ArgumentParser(description=__doc__, parents=[common])
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("pull", parents=[common])
    sub.add_parser("push", parents=[common])
    sub.add_parser("verify", parents=[common])
    args = p.parse_args()
    return {"pull": cmd_pull, "push": cmd_push, "verify": cmd_verify}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
