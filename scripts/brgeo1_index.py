"""BRGEO-1 — implementação de referência do índice de citação generativa.

Calcula o GCI (Generative Citation Index) e, obrigatoriamente, os três
componentes que o formam. A especificação trata o índice como conveniência de
reporte: publicá-lo sozinho é falha de conformidade, porque a evidência da §7.2
do paper mostra que a agregação reordena pouco (rho de Spearman 0,980 contra a
cobertura simples) enquanto a janela de observação move 23,8 pontos. Quem lê só
o índice está lendo a parte menos informativa da medição.

    GCI = (C x P x B)^(1/3)

    C  cobertura      fração das observações do painel em que a entidade aparece
    P  proeminência   1 menos o offset relativo da primeira menção, na média
    B  amplitude      fração dos motores do painel que citam a entidade

A média geométrica é escolha substantiva, não conveniência: ela é
não-compensatória. Ser invisível num motor não pode ser compensado por força em
outro, porque a entidade ausente de um motor está ausente para todo usuário
daquele motor. Média aritmética deixaria um braço forte mascarar ausência.

USO

    python scripts/brgeo1_index.py --vertical fintech
    python scripts/brgeo1_index.py --vertical all --window 0     # resposta inteira
    python scripts/brgeo1_index.py --vertical all --compare      # GCI x cobertura

A proeminência exige o offset de CADA entidade, não só da primeira, então o
script re-extrai a partir do texto em vez de ler as colunas agregadas. Rodar
sobre a série inteira leva alguns minutos.
"""
from __future__ import annotations

import argparse
import collections
import os
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.analysis.entity_extraction import EntityExtractor
from src.config import (
    AMBIGUOUS_ENTITIES, CANONICAL_NAMES, ENTITY_ALIASES, ENTITY_STOP_CONTEXTS,
)
from src.config_v2 import get_v2_cohort

VERTICAIS = ("fintech", "varejo", "saude", "tecnologia")
JANELA_PADRAO = 200
# Um motor entra no painel quando tem observações suficientes para que a
# amplitude signifique algo. Abaixo disso, um braço recém-incluído derrubaria o
# B de toda a coorte por ainda não ter coletado, não por não citar.
MIN_OBS_PARA_ENTRAR_NO_PAINEL = 500


def _extrator(vertical: str) -> EntityExtractor:
    return EntityExtractor(
        cohort=get_v2_cohort(vertical, include_anchors=True, include_decoys=True),
        aliases=ENTITY_ALIASES, ambiguous=AMBIGUOUS_ENTITIES,
        canonical_names=CANONICAL_NAMES, stop_contexts=ENTITY_STOP_CONTEXTS,
    )


def componentes(con: sqlite3.Connection, vertical: str, janela: int) -> tuple[list[dict], list[str], int]:
    """Devolve (linhas, motores do painel, n de observações)."""
    ext = _extrator(vertical)
    con.row_factory = sqlite3.Row
    rows = con.execute(
        "SELECT llm, response_text FROM citations "
        "WHERE is_probe = 0 AND vertical = ? AND response_text IS NOT NULL",
        (vertical,),
    ).fetchall()

    obs_por_motor: collections.Counter = collections.Counter()
    citacoes: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    proeminencias: dict[str, list[float]] = collections.defaultdict(list)

    for r in rows:
        obs_por_motor[r["llm"]] += 1
        texto = r["response_text"][:janela] if janela else r["response_text"]
        comprimento = max(len(texto), 1)
        # Primeira ocorrência de cada entidade, não só da primeira entidade:
        # sem isso a proeminência de quem nunca abre a resposta vira zero e o
        # índice a elimina por um motivo que não existe.
        primeira_ocorrencia: dict[str, int] = {}
        for m in ext.extract(texto):
            primeira_ocorrencia.setdefault(m.entity, m.start)
        for entidade, offset in primeira_ocorrencia.items():
            citacoes[entidade][r["llm"]] += 1
            proeminencias[entidade].append(1.0 - min(1.0, offset / comprimento))

    painel = [m for m, n in obs_por_motor.items() if n >= MIN_OBS_PARA_ENTRAR_NO_PAINEL]
    total = sum(obs_por_motor[m] for m in painel)

    saida = []
    for entidade, por_motor in citacoes.items():
        c = sum(por_motor.values()) / total if total else 0.0
        p = sum(proeminencias[entidade]) / len(proeminencias[entidade])
        b = len([m for m in painel if por_motor[m] > 0]) / len(painel) if painel else 0.0
        gci = (c * p * b) ** (1 / 3) if c > 0 and p > 0 and b > 0 else 0.0
        saida.append({
            "vertical": vertical, "entidade": entidade,
            "cobertura": c, "proeminencia": p, "amplitude": b, "gci": gci,
            "citacoes": sum(por_motor.values()),
        })
    return sorted(saida, key=lambda d: -d["gci"]), painel, total


def _tabela(linhas: list[dict], painel: list[str], total: int, vertical: str,
            janela: int, comparar: bool, limite: int) -> None:
    print(f"\n  BRGEO-1 · {vertical} · janela {janela or 'resposta inteira'} · "
          f"painel de {len(painel)} motores · n = {total:,}".replace(",", "."))
    print(f"  motores: {', '.join(sorted(painel))}\n")

    ordem_cobertura = [d["entidade"] for d in sorted(linhas, key=lambda d: -d["cobertura"])]
    cab = f"  {'entidade':<24}{'C':>9}{'P':>8}{'B':>8}{'GCI':>8}"
    if comparar:
        cab += "   posição GCI vs cobertura"
    print(cab)
    print("  " + "-" * (len(cab) - 2))

    for i, d in enumerate(linhas[:limite], 1):
        linha = (f"  {d['entidade']:<24}{100*d['cobertura']:>8.1f}%"
                 f"{d['proeminencia']:>8.2f}{d['amplitude']:>8.2f}{100*d['gci']:>8.1f}")
        if comparar:
            pos = ordem_cobertura.index(d["entidade"]) + 1
            delta = pos - i
            marca = "=" if delta == 0 else (f"sobe {delta}" if delta > 0 else f"desce {-delta}")
            linha += f"   #{i} vs #{pos}  {marca}"
        print(linha)

    if comparar:
        try:
            from scipy.stats import spearmanr
        except ImportError:
            print("\n  (scipy ausente: rho de Spearman não calculado)")
            return
        ordem_gci = [d["entidade"] for d in linhas]
        rho = spearmanr(
            [ordem_cobertura.index(d["entidade"]) for d in linhas],
            [ordem_gci.index(d["entidade"]) for d in linhas],
        ).statistic
        print(f"\n  rho de Spearman entre GCI e cobertura simples: {rho:.3f}  (n = {len(linhas)})")
        print("  A §7.2 do paper reporta 0,980 na coorte completa. Correlação alta é o")
        print("  resultado esperado e é por isso que a especificação exige publicar C, P e B")
        print("  junto do índice: quem lê só o GCI está lendo a parte que menos separa.")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--db", default=os.getenv("PAPERS_DB_PATH", "data/papers.db"))
    ap.add_argument("--vertical", default="all",
                    help="fintech | varejo | saude | tecnologia | all")
    ap.add_argument("--window", type=int, default=JANELA_PADRAO,
                    help="janela de observação em caracteres; 0 = resposta inteira")
    ap.add_argument("--compare", action="store_true",
                    help="mostra o deslocamento de posição contra a cobertura simples")
    ap.add_argument("--top", type=int, default=15, help="quantas entidades listar")
    a = ap.parse_args()

    db = Path(a.db)
    if not db.exists():
        print(f"banco não encontrado: {db}", file=sys.stderr)
        return 1

    alvos = VERTICAIS if a.vertical == "all" else (a.vertical,)
    con = sqlite3.connect(db)
    for v in alvos:
        linhas, painel, total = componentes(con, v, a.window)
        if not linhas:
            print(f"\n  {v}: sem observações")
            continue
        _tabela(linhas, painel, total, v, a.window, a.compare, a.top)
    con.close()
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
