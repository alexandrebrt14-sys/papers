"""Health-check 2026-08-31 — a janela de observação da citação.

A extração de entidades sempre rodou sobre `citations.response_text`, e
`response_text` nunca foi a resposta do modelo. Cinco dos seis braços gravavam
`text[:200]`; a Perplexity, por usar outro caminho no cliente, gravava a
resposta inteira (até 2.502 caracteres). A janela ficou assimétrica ENTRE OS
BRAÇOS — que é exatamente a comparação que o estudo faz. Recortada nos mesmos
200 caracteres, a taxa de citação da Perplexity cai de 75,8% para 52,0%: 23,8
pontos eram instrumento, não comportamento do modelo.

Estes testes fixam as três garantias que impedem a assimetria de voltar:
a janela é uma decisão única e uniforme, a íntegra é preservada para auditoria,
e a janela efetiva de cada linha fica gravada na própria linha.
"""
from __future__ import annotations

import pytest

from src.collectors.llm_client import apply_citation_window, citation_window_chars

LONGA = "A" * 150 + "Nubank lidera o mercado. " + "B" * 2000


def test_janela_padrao_e_200(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("PAPERS_CITATION_WINDOW_CHARS", raising=False)
    assert citation_window_chars() == 200
    assert len(apply_citation_window(LONGA)) == 200


def test_zero_desliga_o_corte(monkeypatch: pytest.MonkeyPatch) -> None:
    """0 = resposta inteira. É como a análise de sensibilidade do paper roda."""
    monkeypatch.setenv("PAPERS_CITATION_WINDOW_CHARS", "0")
    assert citation_window_chars() == 0
    assert apply_citation_window(LONGA) == LONGA


def test_valor_invalido_cai_no_padrao(monkeypatch: pytest.MonkeyPatch) -> None:
    """Um typo na repo var não pode virar janela silenciosamente diferente."""
    monkeypatch.setenv("PAPERS_CITATION_WINDOW_CHARS", "duzentos")
    assert citation_window_chars() == 200


def test_texto_menor_que_a_janela_passa_inteiro(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("PAPERS_CITATION_WINDOW_CHARS", raising=False)
    curto = "Nubank e Inter."
    assert apply_citation_window(curto) == curto


def test_perplexity_usa_a_mesma_janela_dos_demais(monkeypatch: pytest.MonkeyPatch) -> None:
    """A regressão que originou tudo: o braço RAG escapava do corte.

    Não basta a Perplexity chamar apply_citation_window — a garantia é que o
    resultado seja idêntico ao dos braços paramétricos para o mesmo texto.
    """
    monkeypatch.delenv("PAPERS_CITATION_WINDOW_CHARS", raising=False)
    import src.collectors.llm_client as mod
    import inspect
    fonte = inspect.getsource(mod.LLMClient._query_perplexity)
    assert "apply_citation_window" in fonte, (
        "_query_perplexity voltou a gravar o texto inteiro; a janela precisa "
        "valer para os seis braços ou a comparação entre modelos fica "
        "confundida com o tamanho da janela"
    )


def test_probes_adversariais_incluem_a_perplexity() -> None:
    """H2 media só os cinco braços paramétricos e excluía o único RAG."""
    from src.collectors.llm_client import LLMClient
    assert "calibracao_fp" in LLMClient.PERPLEXITY_CATEGORIES
