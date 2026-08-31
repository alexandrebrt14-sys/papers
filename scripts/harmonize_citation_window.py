"""Harmoniza a janela de observação da citação em toda a série.

CONTEXTO (health-check 2026-08-31)

A extração de entidades sempre rodou sobre `citations.response_text`. Até
31/08/2026 esse campo não era a resposta do modelo: cinco dos seis braços
gravavam `text[:200]`, e a Perplexity — por usar outro caminho no cliente —
gravava a resposta inteira, até 2.502 caracteres. A janela de observação ficou
assimétrica ENTRE OS BRAÇOS, que é precisamente a comparação que o estudo faz.
Medida na mesma janela dos demais, a taxa de citação da Perplexity cai de 75,8%
para 52,0%.

O QUE ESTE SCRIPT FAZ

Nada é destruído. As colunas originais ficam como estão, porque elas são o
registro do que foi observado; o que muda é passar a existir, ao lado delas,
a mesma medida sob janela uniforme:

    cited_win        — houve citação dentro da janela canônica
    cited_count_win  — quantas entidades da coorte dentro da janela
    first_entity_win — primeira entidade dentro da janela
    window_applied   — tamanho da janela efetivamente usada nesta linha

Para os braços que já eram truncados o resultado é idêntico ao original, e é
justamente por isso que a coluna é confiável: ela reproduz o dado existente
onde nada mudou e só diverge onde a janela era de fato maior.

USO

    python scripts/harmonize_citation_window.py --check      # so relata
    python scripts/harmonize_citation_window.py --apply      # grava as colunas
    python scripts/harmonize_citation_window.py --apply --window 200

O backup SHA-256 com manifest é obrigatório antes de --apply e o script o faz
sozinho em data/backups/harmonize-window/.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.analysis.entity_extraction import EntityExtractor
from src.config import (
    AMBIGUOUS_ENTITIES, CANONICAL_NAMES, ENTITY_ALIASES, ENTITY_STOP_CONTEXTS,
)
from src.config_v2 import get_v2_cohort

DEFAULT_WINDOW = 200
VERTICAIS = ("fintech", "varejo", "saude", "tecnologia")
NOVAS_COLUNAS = {
    "cited_win": "INTEGER",
    "cited_count_win": "INTEGER",
    "first_entity_win": "TEXT",
    "window_applied": "INTEGER",
}


def _extratores() -> dict[str, EntityExtractor]:
    return {
        v: EntityExtractor(
            cohort=get_v2_cohort(v, include_anchors=True, include_decoys=True),
            aliases=ENTITY_ALIASES, ambiguous=AMBIGUOUS_ENTITIES,
            canonical_names=CANONICAL_NAMES, stop_contexts=ENTITY_STOP_CONTEXTS,
        )
        for v in VERTICAIS
    }


def _backup(db_path: Path) -> Path:
    destino = Path("data/backups/harmonize-window")
    destino.mkdir(parents=True, exist_ok=True)
    carimbo = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    copia = destino / f"papers-{carimbo}.db"
    shutil.copy2(db_path, copia)
    h = hashlib.sha256(copia.read_bytes()).hexdigest()
    (destino / f"papers-{carimbo}.manifest.json").write_text(
        json.dumps({
            "origem": str(db_path), "copia": str(copia),
            "sha256": h, "bytes": copia.stat().st_size,
            "gerado_em": carimbo, "motivo": "harmonize_citation_window",
        }, indent=2), encoding="utf-8")
    print(f"  backup   {copia}  sha256={h[:16]}...")
    return copia


def _garantir_colunas(con: sqlite3.Connection) -> None:
    existentes = {r[1] for r in con.execute("PRAGMA table_info(citations)").fetchall()}
    for nome, tipo in NOVAS_COLUNAS.items():
        if nome not in existentes:
            con.execute(f"ALTER TABLE citations ADD COLUMN {nome} {tipo}")
    con.commit()


def rodar(db_path: Path, janela: int, aplicar: bool) -> int:
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
    ext = _extratores()

    if aplicar:
        _backup(db_path)
        _garantir_colunas(con)

    linhas = con.execute(
        "SELECT id, vertical, llm, response_text, cited FROM citations "
        "WHERE response_text IS NOT NULL"
    ).fetchall()

    por_llm: dict[str, dict[str, int]] = {}
    updates: list[tuple] = []
    for r in linhas:
        e = ext.get(r["vertical"])
        if e is None:
            continue
        texto = r["response_text"]
        recortado = texto[:janela] if janela else texto
        mentions = e.extract(recortado)
        cit = 1 if mentions else 0
        primeiro = mentions[0].entity if mentions else None

        acc = por_llm.setdefault(r["llm"], {"n": 0, "orig": 0, "harm": 0, "mudou": 0, "cortadas": 0})
        acc["n"] += 1
        acc["orig"] += int(bool(r["cited"]))
        acc["harm"] += cit
        if len(texto) > janela > 0:
            acc["cortadas"] += 1
        if cit != int(bool(r["cited"])):
            acc["mudou"] += 1
        updates.append((cit, len(mentions), primeiro, min(len(texto), janela) if janela else len(texto), r["id"]))

    print(f"\n  janela canonica: {janela or 'resposta inteira'} caracteres\n")
    print(f"  {'braco':<12}{'n':>8}{'original':>11}{'harmonizado':>13}{'delta':>9}{'linhas cortadas':>18}")
    for llm, a in sorted(por_llm.items(), key=lambda kv: -kv[1]["n"]):
        o = 100 * a["orig"] / a["n"]
        h = 100 * a["harm"] / a["n"]
        print(f"  {llm:<12}{a['n']:>8}{o:>10.1f}%{h:>12.1f}%{h - o:>+8.1f}p{a['cortadas']:>18}")

    if aplicar:
        con.executemany(
            "UPDATE citations SET cited_win=?, cited_count_win=?, "
            "first_entity_win=?, window_applied=? WHERE id=?", updates)
        con.commit()
        print(f"\n  gravadas {len(updates)} linhas em cited_win/cited_count_win/"
              f"first_entity_win/window_applied")
    else:
        print("\n  (--check: nada foi gravado)")
    con.close()
    return len(updates)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--db", default=os.getenv("PAPERS_DB_PATH", "data/papers.db"))
    ap.add_argument("--window", type=int, default=DEFAULT_WINDOW,
                    help="janela em caracteres; 0 = resposta inteira")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true", help="so relata, nao grava")
    g.add_argument("--apply", action="store_true", help="grava as colunas harmonizadas")
    a = ap.parse_args()

    db = Path(a.db)
    if not db.exists():
        print(f"banco nao encontrado: {db}", file=sys.stderr)
        return 1
    rodar(db, a.window, aplicar=a.apply)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
