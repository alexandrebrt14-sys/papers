"""Guard do manuscrito — falhas mecânicas que revisão de prosa não pega.

Os três defeitos que a revisão externa de 31/08/2026 encontrou no paper eram
verificáveis por máquina: referência com venue e DOI errados, delta de tabela
que não fechava com as colunas, e citação cruzada para seção inexistente.
Nenhum deles sobrevive a este guard; nenhum deles seria pego relendo o texto.

O guard não avalia argumento. Sustentar uma afirmação com o número certo
continua sendo trabalho humano, e o teste final registra essa fronteira.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from scripts.manuscript_guard import (
    checar_abstract, checar_ancoras, checar_aritmetica,
    checar_identificadores, checar_referencias, checar_tabelas,
)


def test_pega_citacao_sem_entrada() -> None:
    falhas: list[str] = []
    checar_referencias("Como mostra [1] e também [7].\n## References\n[1] Um.\n", falhas)
    assert any("sem entrada" in f and "7" in f for f in falhas)


def test_pega_entrada_nunca_citada() -> None:
    falhas: list[str] = []
    checar_referencias("Vide [1].\n## References\n[1] Um.\n[2] Dois.\n", falhas)
    assert any("nunca citadas" in f for f in falhas)


def test_pega_buraco_na_numeracao_da_bibliografia() -> None:
    falhas: list[str] = []
    checar_referencias("Vide [1] e [3].\n## References\n[1] Um.\n[3] Tres.\n", falhas)
    assert any("buracos" in f for f in falhas)


def test_pega_arxiv_malformado() -> None:
    """O erro real que originou o guard veio de metadados confabulados."""
    falhas: list[str] = []
    checar_identificadores("Preprint arXiv:23110.9735 e arXiv:2311.09735.", falhas)
    assert len(falhas) == 1
    assert "23110.9735" in falhas[0]


def test_aceita_arxiv_valido_com_versao() -> None:
    falhas: list[str] = []
    checar_identificadores("arXiv:2311.09735v3 e arXiv:2104.08663.", falhas)
    assert not falhas


def test_pega_tabela_citada_que_nao_existe() -> None:
    falhas: list[str] = []
    checar_tabelas("**Table 1.** Uma.\n\nComo mostra a Table 4.", falhas)
    assert any("Table 4" in f for f in falhas)


def test_pega_numeracao_de_tabela_fora_de_sequencia() -> None:
    falhas: list[str] = []
    checar_tabelas("**Table 1.** A.\n**Table 3.** B.", falhas)
    assert any("fora de sequência" in f for f in falhas)


def test_pega_ancora_para_secao_inexistente() -> None:
    falhas: list[str] = []
    checar_ancoras("## 1. Intro\n\nComo diz a §9.", falhas)
    assert any("§9" in f for f in falhas)


def test_aceita_ancora_para_subsecao_existente() -> None:
    falhas: list[str] = []
    checar_ancoras("## 5. Janela\n### 5.4 Mecanismo\n\nVer §5.4 e §5.", falhas)
    assert not falhas


def test_pega_delta_que_nao_fecha() -> None:
    """Número copiado à mão para a coluna de delta é erro silencioso."""
    falhas: list[str] = []
    checar_aritmetica("| Perplexity | 75.7% | 51.9% | −12.0 pp | 7,435 |", falhas)
    assert any("delta não fecha" in f for f in falhas)


def test_aceita_delta_correto_com_sinal_unicode() -> None:
    falhas: list[str] = []
    checar_aritmetica("| **Perplexity** | **75.7%** | **51.9%** | **−23.8 pp** | 7,435 |", falhas)
    assert not falhas


def test_aceita_delta_zero() -> None:
    falhas: list[str] = []
    checar_aritmetica("| ChatGPT | 17.2% | 17.2% | +0.0 pp | 0 |", falhas)
    assert not falhas


def test_pega_abstract_acima_do_limite() -> None:
    falhas: list[str] = []
    texto = "## Abstract\n\n" + " ".join(["palavra"] * 210) + "\n\n**Keywords:** a"
    checar_abstract(texto, 200, falhas)
    assert any("210 palavras" in f for f in falhas)


def test_manuscrito_real_passa() -> None:
    """O manuscrito versionado precisa estar sempre aprovado no repositório."""
    caminho = Path(__file__).resolve().parents[1] / "docs" / "research" / "methods-paper" / "MANUSCRIPT.md"
    if not caminho.exists():
        pytest.skip("manuscrito ausente neste clone")
    t = caminho.read_text(encoding="utf-8")
    falhas: list[str] = []
    for f in (checar_referencias, checar_identificadores, checar_tabelas, checar_ancoras):
        f(t, falhas)
    checar_aritmetica(t, falhas)
    checar_abstract(t, 200, falhas)
    assert not falhas, f"manuscrito versionado reprovado: {falhas}"


def test_o_guard_nao_avalia_argumento() -> None:
    """Fronteira declarada: forma correta e afirmação falsa passam pelo guard.

    Registrado como teste para que ninguém trate o verde do guard como
    verificação de conteúdo. Foi exatamente esse tipo de afirmação — bem
    formada e sem apoio na medição — que a revisão externa derrubou na §8.
    """
    falso = ("Duas agregações produzem o mesmo ranking [1].\n"
             "## References\n[1] Fonte real.\n")
    falhas: list[str] = []
    checar_referencias(falso, falhas)
    checar_identificadores(falso, falhas)
    assert not falhas
