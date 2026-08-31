"""Guard distribucional da coleta — detecta defeito de instrumento, não de dado.

POR QUE ESTE SCRIPT EXISTE

Em 31/08/2026 descobrimos que a extração de entidades rodava sobre janelas
diferentes em braços diferentes do estudo: cinco motores eram medidos nos
primeiros 200 caracteres da resposta e um era medido na resposta inteira. O
efeito foi de 23,8 pontos percentuais na taxa de citação de um braço.

Nada detectou isso por meses. Os testes afirmavam sobre a coluna, e a coluna
estava preenchida nos dois casos. Os validadores viam strings bem-formadas de
tamanho plausível. Os health-checks diários conferiam que os seis braços
produziam linhas, que o split de idioma se mantinha em 50/50 e que os probes
estavam marcados — tudo verdade. Duzentos e vinte e três testes passavam.

O defeito apareceu numa checagem DISTRIBUCIONAL. O comprimento médio armazenado
batia em exatamente 200,0 em cinco braços e em 691,8 no sexto:

    ChatGPT     19.328 linhas   min 200   max 200   100,0% em exatamente 200
    Claude      19.162 linhas   min 200   max 200   100,0%
    Groq        18.304 linhas   min  74   max 200    99,8%
    Grok           462 linhas   min 187   max 200    99,6%
    Gemini      18.794 linhas   min  87   max 200    94,8%
    Perplexity   7.436 linhas   min 198   max 2502    0,0%

Uma variável cujo máximo é igual ao mínimo em 19.328 observações não está
medindo nada: está reportando um limite. E o zero isolado da Perplexity é a
assinatura de que aquele braço escapou do corte — em 7.436 respostas de
comprimento livre, nenhuma cai exatamente sobre o valor de truncamento dos
outros, porque acertá-lo seria coincidência.

A lição generalizável é que teste funcional verifica se o pipeline faz o que
foi escrito, e não se o que foi escrito mede o que se pretende. Um limite de
instrumento é invisível para asserção sobre presença de valor, e visível de
imediato numa distribuição.

O QUE ELE CHECA

    truncamento    massa empilhada num único comprimento, por braço
    assimetria     braços medidos sob janelas diferentes entre si
    degenerado     variável sem variância, ou quase
    integra        response_full_text sendo gravado após a migration 0010

USO

    python scripts/distribution_guard.py check              # sai 1 se reprovar
    python scripts/distribution_guard.py check --since-days 1
    python scripts/distribution_guard.py check --verbose

Feito para rodar no workflow depois da coleta, ao lado de validate_v2_collection.
"""
from __future__ import annotations

import argparse
import os
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# Um braço só entra na avaliação com observações suficientes para que a forma
# da distribuição signifique alguma coisa. Abaixo disso, um braço recém-incluído
# dispararia alarme por ainda não ter coletado, não por estar truncado.
MIN_OBS = 200

# Acima desta fração num único valor de comprimento, a distribuição deixou de
# ser de resposta e passou a ser de limite. Um modelo real não produz a mesma
# contagem exata de caracteres em 90% das respostas.
LIMIAR_TRUNCAMENTO = 0.90

# Quando dois braços diferem mais que isto no comprimento típico, ou eles estão
# sob janelas diferentes ou um deles mudou de comportamento. Os dois casos
# merecem olhar humano.
RAZAO_MAX_ENTRE_BRACOS = 2.0


class Reprovacao(Exception):
    """Falha que invalida a comparação entre braços."""


def _conectar(caminho: Path) -> sqlite3.Connection:
    con = sqlite3.connect(caminho)
    con.row_factory = sqlite3.Row
    return con


def _colunas(con: sqlite3.Connection) -> set[str]:
    return {r[1] for r in con.execute("PRAGMA table_info(citations)")}


def coletar_perfil(con: sqlite3.Connection, desde_dias: int | None) -> list[dict]:
    filtro = ""
    if desde_dias:
        filtro = f"AND timestamp >= datetime('now', '-{int(desde_dias)} days')"
    sql = f"""
        SELECT llm,
               COUNT(*) AS n,
               MIN(length(response_text)) AS minimo,
               MAX(length(response_text)) AS maximo,
               AVG(length(response_text)) AS media
        FROM citations
        WHERE response_text IS NOT NULL AND is_probe = 0 {filtro}
        GROUP BY llm
    """
    perfil = []
    for r in con.execute(sql):
        if r["n"] < MIN_OBS:
            continue
        moda = con.execute(f"""
            SELECT length(response_text) AS L, COUNT(*) AS c
            FROM citations
            WHERE llm = ? AND response_text IS NOT NULL AND is_probe = 0 {filtro}
            GROUP BY L ORDER BY c DESC LIMIT 1
        """, (r["llm"],)).fetchone()
        perfil.append({
            "llm": r["llm"], "n": r["n"],
            "minimo": r["minimo"], "maximo": r["maximo"], "media": r["media"],
            "moda": moda["L"], "fracao_na_moda": moda["c"] / r["n"],
        })
    return sorted(perfil, key=lambda d: -d["n"])


def avaliar(perfil: list[dict], con: sqlite3.Connection,
            verbose: bool = False) -> list[str]:
    falhas: list[str] = []
    cols = _colunas(con)

    # Corte DELIBERADO e corte DESTRUTIVO produzem a mesma distribuição em
    # response_text: massa empilhada no valor da janela. O que os separa é se a
    # íntegra sobreviveu. Com response_full_text populado, o recorte é o
    # parâmetro P1 funcionando e a distribuição empilhada é o resultado
    # esperado; sem ela, o texto foi perdido no cliente e não volta.
    # Sem essa distinção o guard ficaria vermelho em toda coleta futura, e um
    # guard que sempre reprova é indistinguível de um guard desligado.
    integra_retida = False
    if "response_full_text" in cols:
        r = con.execute("""
            SELECT COUNT(*) n,
                   SUM(CASE WHEN response_full_text IS NOT NULL
                             AND length(response_full_text) >= length(response_text)
                        THEN 1 ELSE 0 END) c
            FROM citations
            WHERE timestamp >= datetime('now', '-2 days') AND is_probe = 0
        """).fetchone()
        integra_retida = bool(r["n"]) and r["c"] / r["n"] > 0.5

    if verbose:
        estado = "íntegra retida" if integra_retida else "íntegra AUSENTE"
        print(f"  modo: {estado}\n")

    if not integra_retida:
        # 1. Truncamento destrutivo: massa empilhada e nada guardado além dela.
        for p in perfil:
            if p["fracao_na_moda"] >= LIMIAR_TRUNCAMENTO:
                falhas.append(
                    f"{p['llm']}: {100*p['fracao_na_moda']:.1f}% das respostas têm "
                    f"exatamente {p['moda']} caracteres e a íntegra não está "
                    f"guardada. Distribuição de limite, não de resposta — o texto "
                    f"é cortado antes de chegar ao banco e não é recuperável."
                )

        # 2. Variável degenerada: máximo igual ao mínimo.
        for p in perfil:
            if p["minimo"] == p["maximo"] and p["n"] >= MIN_OBS:
                falhas.append(
                    f"{p['llm']}: comprimento constante em {p['minimo']} caracteres "
                    f"nas {p['n']} observações. Variável sem variância não mede nada."
                )

        # 3. Assimetria entre braços — o defeito de 31/08. Só é diagnosticável
        #    por aqui enquanto citation_window_chars não existir; com a coluna,
        #    a checagem 4 é direta e esta vira redundante.
        if len(perfil) >= 2 and "citation_window_chars" not in cols:
            medias = [p["media"] for p in perfil]
            razao = max(medias) / max(min(medias), 1)
            if razao > RAZAO_MAX_ENTRE_BRACOS:
                maior = max(perfil, key=lambda d: d["media"])
                menor = min(perfil, key=lambda d: d["media"])
                falhas.append(
                    f"assimetria entre braços: {maior['llm']} tem média de "
                    f"{maior['media']:.0f} caracteres e {menor['llm']} tem "
                    f"{menor['media']:.0f} (razão {razao:.1f}x). Se a janela de "
                    f"observação difere entre braços, a comparação entre motores "
                    f"fica confundida com o tamanho da janela."
                )

    # 4. A janela declarada precisa ser a mesma em todos os braços.
    if "citation_window_chars" in cols:
        janelas = con.execute("""
            SELECT llm, MIN(citation_window_chars) mn, MAX(citation_window_chars) mx
            FROM citations WHERE citation_window_chars IS NOT NULL AND is_probe = 0
            GROUP BY llm
        """).fetchall()
        limites = {r["mx"] for r in janelas}
        if len(limites) > 1:
            detalhe = ", ".join(f"{r['llm']}={r['mx']}" for r in janelas)
            falhas.append(
                f"janela declarada difere entre braços ({detalhe}). P1 exige "
                f"uma janela única aplicada a todos."
            )

    # 5. A íntegra precisa estar sendo gravada. Sem ela nenhuma observação é
    #    auditável, e essa perda é irreversível: texto não gravado não volta.
    if "response_full_text" in cols:
        recente = con.execute("""
            SELECT COUNT(*) n,
                   SUM(CASE WHEN response_full_text IS NOT NULL THEN 1 ELSE 0 END) c
            FROM citations
            WHERE timestamp >= datetime('now', '-2 days')
        """).fetchone()
        if recente["n"] > 0 and recente["c"] == 0:
            falhas.append(
                f"nenhuma das {recente['n']} observações dos últimos 2 dias tem "
                f"response_full_text. A coluna existe e não está sendo populada; "
                f"essas observações não serão auditáveis e o texto não é recuperável."
            )

    return falhas


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("comando", choices=["check"])
    ap.add_argument("--db", default=os.getenv("PAPERS_DB_PATH", "data/papers.db"))
    ap.add_argument("--since-days", type=int, default=None,
                    help="restringe a janela temporal analisada")
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args()

    db = Path(a.db)
    if not db.exists():
        print(f"banco não encontrado: {db}", file=sys.stderr)
        return 1

    con = _conectar(db)
    perfil = coletar_perfil(con, a.since_days)
    if not perfil:
        print("  nenhum braço com observações suficientes para avaliar.")
        return 0

    falhas = avaliar(perfil, con, a.verbose)
    con.close()

    if falhas:
        print("  GUARD DISTRIBUCIONAL REPROVOU\n")
        for f in falhas:
            print(f"  - {f}\n")
        print("  Estas são falhas de INSTRUMENTO. O pipeline pode estar verde e")
        print("  os dados ainda assim não serem comparáveis entre braços.")
        return 1

    print("  guard distribucional: aprovado")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
