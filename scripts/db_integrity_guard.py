#!/usr/bin/env python3
"""db_integrity_guard.py — barra bancos degenerados antes de virarem verdade.

Incidente 2026-08-09: weekly-benchmark.yml e weekly-calibration.yml baixaram um
artifact chamado papers-db-latest, rodaram a analise sobre 864 citations em vez
de 63.940, publicaram o resultado e marcaram o run como success. Nenhum alarme
disparou porque nada no pipeline comparava o tamanho do dataset com o que ele
tinha na vespera.

Este guard mantem um high-water mark versionado em data/db_floor.json. Qualquer
banco que chegue abaixo do piso (menos a tolerancia) derruba o run em vez de
virar analise publicada ou sobrescrever o backup.

Uso:
    python scripts/db_integrity_guard.py check          # valida contra o piso
    python scripts/db_integrity_guard.py update         # eleva o piso apos run bom
    python scripts/db_integrity_guard.py check --json   # saida legivel por maquina

Exit codes:
    0 = banco integro
    2 = banco degenerado (abaixo do piso) ou ilegivel
"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys

FLOOR_PATH = "data/db_floor.json"

# Coleta pode legitimamente nao rodar (falha de LLM, fim de semana), mas o
# numero de citations JAMAIS cai — a tabela e append-only. A tolerancia de 2%
# cobre apenas VACUUM e limpeza pontual de linhas invalidas.
TOLERANCE = 0.02

TRACKED_TABLES = ("citations", "citation_context", "collection_runs", "finops_usage")


def table_counts(path: str) -> dict[str, int] | None:
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return None
    # sqlite3.connect() nao le o arquivo: um .db truncado ou corrompido so
    # estoura na primeira query. Por isso o except precisa envolver tambem a
    # leitura de sqlite_master, senao um upload interrompido vira traceback
    # com exit 1 em vez do exit 2 que o CI sabe interpretar.
    con = None
    try:
        con = sqlite3.connect(path)
        cur = con.cursor()
        existing = {
            r[0]
            for r in cur.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        }
        out: dict[str, int] = {}
        for t in TRACKED_TABLES:
            if t not in existing:
                out[t] = 0
                continue
            try:
                out[t] = cur.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0]
            except sqlite3.Error:
                out[t] = 0
        return out
    except sqlite3.Error:
        return None
    finally:
        if con is not None:
            con.close()


def load_floor() -> dict[str, int]:
    if not os.path.exists(FLOOR_PATH):
        return {}
    try:
        with open(FLOOR_PATH, encoding="utf-8") as f:
            return json.load(f).get("floor", {})
    except (OSError, json.JSONDecodeError):
        return {}


def save_floor(floor: dict[str, int]) -> None:
    os.makedirs(os.path.dirname(FLOOR_PATH), exist_ok=True)
    payload = {
        "_comment": (
            "High-water mark do dataset. Gerado por scripts/db_integrity_guard.py. "
            "Nunca editar a mao: se precisar baixar o piso, apague o arquivo e "
            "rode 'update' sobre um banco reconhecidamente integro."
        ),
        "floor": floor,
    }
    with open(FLOOR_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
        f.write("\n")


def cmd_check(args: argparse.Namespace) -> int:
    counts = table_counts(args.db)
    if counts is None:
        print(f"FALHA: {args.db} ausente, vazio ou ilegivel como SQLite.", file=sys.stderr)
        return 2

    floor = load_floor()
    if not floor:
        print("Piso ainda nao registrado — nada a comparar. Rode 'update'.")
        if args.json:
            print(json.dumps({"status": "no_floor", "counts": counts}))
        return 0

    violations = []
    for table, minimum in floor.items():
        actual = counts.get(table, 0)
        allowed = int(minimum * (1 - TOLERANCE))
        status = "OK" if actual >= allowed else "FALHA"
        print(f"  [{status}] {table:<20} atual={actual:<8} piso={minimum:<8} min={allowed}")
        if actual < allowed:
            violations.append((table, actual, minimum))

    if violations:
        # Sem o flush, o log do CI intercala stderr antes da tabela acima.
        sys.stdout.flush()
        print("", file=sys.stderr)
        print("BANCO DEGENERADO — o dataset encolheu:", file=sys.stderr)
        for table, actual, minimum in violations:
            pct = (actual / minimum * 100) if minimum else 0
            print(
                f"  {table}: {actual} linhas contra piso de {minimum} ({pct:.1f}%)",
                file=sys.stderr,
            )
        print("", file=sys.stderr)
        print(
            "Run abortado. Um banco menor que o piso significa restore da fonte "
            "errada, artifact truncado ou colisao de nome de artifact entre "
            "workflows. Investigar ANTES de re-executar.",
            file=sys.stderr,
        )
        if args.json:
            print(json.dumps({"status": "degraded", "counts": counts, "floor": floor}))
        return 2

    print("Banco integro — todas as tabelas rastreadas acima do piso.")
    if args.json:
        print(json.dumps({"status": "ok", "counts": counts, "floor": floor}))
    return 0


def cmd_update(args: argparse.Namespace) -> int:
    counts = table_counts(args.db)
    if counts is None:
        print(f"FALHA: {args.db} ausente, vazio ou ilegivel.", file=sys.stderr)
        return 2

    floor = load_floor()
    changed = False
    for table, actual in counts.items():
        previous = floor.get(table, 0)
        if actual > previous:
            floor[table] = actual
            changed = True
            print(f"  piso elevado: {table} {previous} -> {actual}")
        else:
            print(f"  piso mantido: {table} {previous} (atual {actual})")

    if changed:
        save_floor(floor)
        print(f"{FLOOR_PATH} atualizado.")
    else:
        print("Nenhum piso elevado nesta execucao.")
    return 0


def main() -> int:
    # As flags entram tambem em cada subparser para que tanto
    # "guard --db X check" quanto "guard check --db X" funcionem.
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--db", default=os.environ.get("PAPERS_DB_PATH", "data/papers.db"))
    common.add_argument("--json", action="store_true", help="emite resumo JSON")

    p = argparse.ArgumentParser(description=__doc__, parents=[common])
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check", parents=[common])
    sub.add_parser("update", parents=[common])
    args = p.parse_args()
    return {"check": cmd_check, "update": cmd_update}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
