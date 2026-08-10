#!/usr/bin/env python3
"""mark_collection_gaps.py — registra em collection_runs os dias sem coleta.

docs/METHODOLOGY_V2.md, secao "Politica de imputacao" (linha 111):

    Gaps totais sao marcados em collection_runs como status='aborted' e o
    intervalo e excluido da janela analitica formal — preserva honestidade
    estatistica sobre serie temporal incompleta.

O protocolo esta escrito, mas nunca foi executado. Em 10/08/2026 a tabela tinha
240 linhas, todas com status='success', cobrindo 41 dias distintos. Os 67 dias
sem coleta — entre eles o bloco de 59 dias de 10/06 a 07/08 — simplesmente nao
existiam na tabela. Um revisor que consultasse collection_runs veria um pipeline
impecavel; a verdade e que 108 runs executaram nesse periodo e nao persistiram
uma linha (causa em .github/workflows/daily-collect.yml, correcao no PR #48).

Ausencia nao e registro. Este script transforma o buraco silencioso em fato
declarado, que e o que a analise longitudinal precisa para excluir o intervalo
da janela formal em vez de tratar dias faltantes como se nunca tivessem sido
tentados.

O script NAO inventa observacao: nao escreve nada em `citations`. Ele apenas
grava, por dia-vertical ausente, uma linha de tentativa fracassada com
records=0 e o motivo no error_msg.

Uso:
    python scripts/mark_collection_gaps.py --dry-run          # mostra o plano
    python scripts/mark_collection_gaps.py --apply            # grava
    python scripts/mark_collection_gaps.py --apply --from 2026-06-10 --to 2026-08-07
"""
from __future__ import annotations

import argparse
import datetime
import os
import sqlite3
import sys

VERTICAIS = ("fintech", "varejo", "saude", "tecnologia")
MODULE = "citation_tracker"
STATUS = "aborted"

MOTIVO = (
    "gap sem coleta persistida — restore do artifact nunca trouxe a base viva "
    "(workflow_conclusion vazio casava a run em curso consigo mesma) e o "
    "restore do R2 estava inerte por falta de secrets. Runs verdes, zero "
    "linhas. Diagnostico: PR #48 e commit bba851f. Intervalo excluido da "
    "janela analitica formal conforme METHODOLOGY_V2 secao Politica de "
    "imputacao."
)


def dias_com_coleta(con: sqlite3.Connection) -> set[str]:
    return {
        r[0]
        for r in con.execute("SELECT DISTINCT date(timestamp) FROM citations").fetchall()
    }


def dias_ja_marcados(con: sqlite3.Connection) -> set[tuple[str, str]]:
    return {
        (r[0], r[1])
        for r in con.execute(
            "SELECT date(timestamp), vertical FROM collection_runs WHERE status = ?",
            (STATUS,),
        ).fetchall()
    }


def janela(con: sqlite3.Connection) -> tuple[datetime.date, datetime.date]:
    lo, hi = con.execute(
        "SELECT MIN(date(timestamp)), MAX(date(timestamp)) FROM citations"
    ).fetchone()
    return (
        datetime.date.fromisoformat(lo),
        datetime.date.fromisoformat(hi),
    )


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--db", default=os.environ.get("PAPERS_DB_PATH", "data/papers.db"))
    p.add_argument("--from", dest="ini", help="data inicial YYYY-MM-DD")
    p.add_argument("--to", dest="fim", help="data final YYYY-MM-DD")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--dry-run", action="store_true")
    g.add_argument("--apply", action="store_true")
    args = p.parse_args()

    if not os.path.exists(args.db):
        print(f"ERRO: {args.db} nao existe.", file=sys.stderr)
        return 1

    con = sqlite3.connect(args.db)
    try:
        tem = dias_com_coleta(con)
        marcados = dias_ja_marcados(con)
        auto_ini, auto_fim = janela(con)
        ini = datetime.date.fromisoformat(args.ini) if args.ini else auto_ini
        fim = datetime.date.fromisoformat(args.fim) if args.fim else auto_fim

        print(f"banco:   {args.db}")
        print(f"janela:  {ini} -> {fim}")
        print(f"dias com coleta: {len(tem)}")
        print(f"dias-vertical ja marcados como {STATUS}: {len(marcados)}")
        print()

        faltantes = []
        cur = ini
        while cur <= fim:
            dia = cur.isoformat()
            if dia not in tem:
                for v in VERTICAIS:
                    if (dia, v) not in marcados:
                        faltantes.append((dia, v))
            cur += datetime.timedelta(days=1)

        dias_unicos = sorted({d for d, _ in faltantes})
        print(f"dias sem coleta a registrar: {len(dias_unicos)}")
        print(f"linhas a inserir ({len(VERTICAIS)} verticais por dia): {len(faltantes)}")
        if dias_unicos:
            print(f"primeiro: {dias_unicos[0]}   ultimo: {dias_unicos[-1]}")

        if not faltantes:
            print("\nNada a fazer — todos os gaps ja estao registrados.")
            return 0

        if args.dry_run:
            print("\n--dry-run: nada foi gravado. Use --apply para registrar.")
            return 0

        # timestamp = meio-dia UTC do dia ausente, para cair inequivocamente
        # dentro do dia em date(timestamp) sem sugerir hora real de execucao.
        agora = datetime.datetime.now(datetime.timezone.utc).isoformat()
        linhas = [
            (f"{dia}T12:00:00+00:00", MODULE, 0, 0, STATUS, MOTIVO, agora, v)
            for dia, v in faltantes
        ]
        con.executemany(
            "INSERT INTO collection_runs "
            "(timestamp, module, records, duration_ms, status, error_msg, created_at, vertical) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            linhas,
        )
        con.commit()
        print(f"\n{len(linhas)} linhas gravadas com status='{STATUS}'.")

        total = con.execute("SELECT COUNT(*) FROM collection_runs").fetchone()[0]
        por_status = con.execute(
            "SELECT status, COUNT(*) FROM collection_runs GROUP BY status"
        ).fetchall()
        print(f"collection_runs agora: {total} linhas -> {dict(por_status)}")
        print("citations NAO foi tocada — nenhuma observacao foi criada.")
        return 0
    finally:
        con.close()


if __name__ == "__main__":
    sys.exit(main())
