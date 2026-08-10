#!/usr/bin/env python3
"""window_progress.py — quanto falta para fechar a janela de 90 dias.

Decisao do operador em 10/08/2026: a janela e ACUMULADA. Os 41 dias ja
coletados contam, o bloco de 10/06 a 07/08 fica registrado como gap e sai da
janela analitica formal (METHODOLOGY_V2, "Politica de imputacao"), e a coleta
segue ate somar 90 dias-com-dado.

Progresso e medido em dias que produziram linha, nunca em dias de calendario.
Foi exatamente essa confusao que fez o dashboard publicar "dia 90 de 90"
enquanto o banco tinha 41 dias reais e um buraco de 59.

Uso:
    python scripts/window_progress.py
    python scripts/window_progress.py --json
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import sqlite3
import sys

ALVO_DIAS = 90
# Duas coletas por dia (cron 09:00 e 21:00 UTC). Uma falhar nao perde o dia,
# entao a projecao assume 1 dia-com-dado por dia corrido.
DIAS_POR_DIA_CORRIDO = 1.0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--db", default=os.environ.get("PAPERS_DB_PATH", "data/papers.db"))
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    if not os.path.exists(args.db):
        print(f"ERRO: {args.db} nao existe.", file=sys.stderr)
        return 1

    con = sqlite3.connect(args.db)
    try:
        dias = con.execute(
            "SELECT COUNT(DISTINCT date(timestamp)) FROM citations"
        ).fetchone()[0]
        obs = con.execute("SELECT COUNT(*) FROM citations").fetchone()[0]
        primeiro, ultimo = con.execute(
            "SELECT MIN(date(timestamp)), MAX(date(timestamp)) FROM citations"
        ).fetchone()
        try:
            gaps = con.execute(
                "SELECT COUNT(DISTINCT date(timestamp)) FROM collection_runs "
                "WHERE status = 'aborted'"
            ).fetchone()[0]
        except sqlite3.Error:
            gaps = 0
    finally:
        con.close()

    faltam = max(0, ALVO_DIAS - dias)
    hoje = datetime.date.today()
    previsao = hoje + datetime.timedelta(days=int(faltam / DIAS_POR_DIA_CORRIDO))
    media = round(obs / dias) if dias else 0
    pct = round(dias / ALVO_DIAS * 100, 1)

    if args.json:
        print(
            json.dumps(
                {
                    "diasColetados": dias,
                    "alvoDias": ALVO_DIAS,
                    "faltam": faltam,
                    "percentual": pct,
                    "observacoes": obs,
                    "mediaPorDia": media,
                    "primeiroDia": primeiro,
                    "ultimoDia": ultimo,
                    "diasComGapRegistrado": gaps,
                    "previsaoConclusao": previsao.isoformat(),
                },
                ensure_ascii=False,
            )
        )
        return 0

    barra = "#" * int(pct / 2.5) + "." * (40 - int(pct / 2.5))
    print()
    print("  JANELA DE 90 DIAS — paper GEO multi-vertical")
    print("  ORCID 0009-0004-9150-485X")
    print()
    print(f"  [{barra}] {pct}%")
    print()
    print(f"  dias coletados      {dias} de {ALVO_DIAS}")
    print(f"  faltam              {faltam} dias")
    print(f"  previsao            {previsao.strftime('%d/%m/%Y')}")
    print()
    print(f"  observacoes         {obs:,}".replace(",", "."))
    print(f"  media por dia       {media:,}".replace(",", "."))
    print(f"  serie               {primeiro} -> {ultimo}")
    if gaps:
        print(f"  gaps registrados    {gaps} dias (fora da janela analitica)")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
