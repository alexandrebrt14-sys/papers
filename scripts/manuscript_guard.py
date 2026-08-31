"""Confere os números do manuscrito contra o banco e contra si mesmos.

POR QUE ESTE SCRIPT EXISTE

Três defeitos distintos apareceram na revisão de 31/08/2026, e nenhum deles
seria pego por revisão de prosa:

1. O manuscrito afirmava um número que a medição não sustentava. A §7.2 dizia
   que "duas agregações defensáveis produzem quase o mesmo ranking" apoiada no
   rho de 0,982 entre o índice e a cobertura — que é o componente com 74,7% da
   variância do índice. Contra agregações alternativas o rho cai a 0,706.

2. A citação fundadora do campo estava errada em quatro documentos canônicos
   (venue, ano e DOI), e o DOI sequer resolvia. A origem foi um arquivo de
   pesquisa que confabulou os metadados.

3. O paper violava a própria conformidade que especificava: exigia versão de
   modelo pinada em toda observação e depois nomeava só produtos nas tabelas.

O que estes três têm em comum é serem verificáveis por máquina. Prosa não é, e
por isso este guard não tenta avaliar argumento: ele confere aritmética,
integridade de referência e coerência interna.

O QUE ELE CHECA

    referencias    toda citação [n] tem entrada, e toda entrada é citada
    identificadores  DOI e arXiv com forma válida; nenhum inventado por typo
    tabelas        numeração sequencial, sem salto nem repetição
    aritmetica     deltas de tabela batem com as colunas que os originam
    ancoras        toda seção citada como §n existe
    abstract       dentro do limite do periódico-alvo

USO

    python scripts/manuscript_guard.py check
    python scripts/manuscript_guard.py check --max-abstract 250
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
PADRAO = RAIZ / "docs" / "research" / "methods-paper" / "MANUSCRIPT.md"

# Information Sciences declara 200 palavras em "Article types" e 250 em
# "Abstract", na mesma página. 200 satisfaz os dois textos ao mesmo tempo.
LIMITE_ABSTRACT = 200


def _falha(msgs: list[str], texto: str) -> None:
    msgs.append(texto)


def checar_referencias(t: str, falhas: list[str]) -> None:
    corpo, _, refs = t.partition("## References")
    if not refs:
        _falha(falhas, "não encontrei a seção References")
        return
    citadas = {int(n) for grupo in re.findall(r"\[(\d+(?:,\s*\d+)*)\]", corpo)
               for n in grupo.split(",")}
    definidas = {int(m) for m in re.findall(r"^\[(\d+)\]", refs, re.M)}
    orfas = sorted(citadas - definidas)
    nunca = sorted(definidas - citadas)
    if orfas:
        _falha(falhas, f"citadas no corpo sem entrada na bibliografia: {orfas}")
    if nunca:
        _falha(falhas, f"na bibliografia e nunca citadas: {nunca}")
    if definidas and sorted(definidas) != list(range(1, max(definidas) + 1)):
        faltando = sorted(set(range(1, max(definidas) + 1)) - definidas)
        _falha(falhas, f"numeração da bibliografia tem buracos: {faltando}")


def checar_identificadores(t: str, falhas: list[str]) -> None:
    # DOI: prefixo 10.NNNN seguido de sufixo. Forma, não resolução — o guard
    # roda offline; resolver de fato é trabalho do VERIFICATION.md.
    for doi in re.findall(r"\b(10\.\d{4,9}/[^\s)\]]+)", t):
        if doi.endswith((".", ",")) or len(doi) < 10:
            _falha(falhas, f"DOI com forma suspeita: {doi}")
    for aid in re.findall(r"arXiv:(\S+)", t):
        aid = aid.rstrip(".,;)")
        if not re.fullmatch(r"\d{4}\.\d{4,5}(v\d+)?", aid):
            _falha(falhas, f"identificador arXiv com forma inválida: arXiv:{aid}")


def checar_tabelas(t: str, falhas: list[str]) -> None:
    nums = [int(n) for n in re.findall(r"\*\*Table (\d+)\.\*\*", t)]
    if not nums:
        return
    if nums != list(range(1, len(nums) + 1)):
        _falha(falhas, f"numeração de tabelas fora de sequência: {nums}")
    for n in set(re.findall(r"\bTable (\d+)\b", t)):
        if int(n) not in nums:
            _falha(falhas, f"texto cita Table {n}, que não existe")


def checar_ancoras(t: str, falhas: list[str]) -> None:
    secoes = {m for m in re.findall(r"^#{2,3} (\d+)(?:\.(\d+))?", t, re.M)}
    existentes = {s[0] for s in secoes} | {f"{s[0]}.{s[1]}" for s in secoes if s[1]}
    for ref in set(re.findall(r"§(\d+(?:\.\d+)?)", t)):
        if ref not in existentes:
            _falha(falhas, f"referência cruzada §{ref} aponta para seção inexistente")


def checar_aritmetica(t: str, falhas: list[str]) -> None:
    """Confere deltas declarados contra as colunas que os produzem.

    Só atua em linhas de tabela com o formato "| ... | a% | b% | delta pp | ...",
    que é onde um número copiado à mão diverge sem ninguém notar.
    """
    padrao = re.compile(
        r"\|\s*\**([\d.,]+)%\**\s*\|\s*\**([\d.,]+)%\**\s*\|\s*\**([+−-]?[\d.,]+)\s*pp\**\s*\|")
    for linha in t.splitlines():
        m = padrao.search(linha)
        if not m:
            continue
        try:
            a = float(m.group(1).replace(",", "."))
            b = float(m.group(2).replace(",", "."))
            d = float(m.group(3).replace("−", "-").replace(",", "."))
        except ValueError:
            continue
        if abs((b - a) - d) > 0.15:
            _falha(falhas,
                   f"delta não fecha: {a}% -> {b}% declarado como {d} pp "
                   f"(esperado {b - a:+.1f})")


def checar_abstract(t: str, limite: int, falhas: list[str]) -> None:
    m = re.search(r"## Abstract\s*(.*?)\*\*Keywords", t, re.S)
    if not m:
        _falha(falhas, "não encontrei o Abstract")
        return
    n = len(m.group(1).split())
    if n > limite:
        _falha(falhas, f"abstract com {n} palavras, acima do limite de {limite}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("comando", choices=["check"])
    ap.add_argument("--file", default=str(PADRAO))
    ap.add_argument("--max-abstract", type=int, default=LIMITE_ABSTRACT)
    a = ap.parse_args()

    caminho = Path(a.file)
    if not caminho.exists():
        print(f"manuscrito não encontrado: {caminho}", file=sys.stderr)
        return 1
    t = caminho.read_text(encoding="utf-8")

    falhas: list[str] = []
    checar_referencias(t, falhas)
    checar_identificadores(t, falhas)
    checar_tabelas(t, falhas)
    checar_ancoras(t, falhas)
    checar_aritmetica(t, falhas)
    checar_abstract(t, a.max_abstract, falhas)

    if falhas:
        print("  GUARD DO MANUSCRITO REPROVOU\n")
        for f in falhas:
            print(f"  - {f}")
        print("\n  Estas são falhas mecânicas. O guard não avalia argumento:")
        print("  número que sustenta afirmação continua sendo trabalho de revisão.")
        return 1

    print("  guard do manuscrito: aprovado")
    print("  (confere forma e coerência; não substitui VERIFICATION.md, que")
    print("   reproduz cada número a partir do banco)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
