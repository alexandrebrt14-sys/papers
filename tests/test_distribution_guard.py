"""Guard distribucional — detecta limite de instrumento, não ausência de dado.

O defeito de 31/08/2026 (janela de observação assimétrica entre braços) passou
por 223 testes funcionais sem ser notado, porque todo teste afirmava sobre a
presença de valor na coluna e a coluna estava preenchida nos dois casos. O que
o denunciou foi a forma da distribuição: comprimento médio armazenado batendo
em exatamente 200,0 em cinco braços e em 691,8 no sexto.

Estes testes fixam as duas metades do contrato do guard, e a segunda importa
tanto quanto a primeira: ele precisa reprovar o defeito e precisa APROVAR a
configuração corrigida, na qual a janela de 200 é deliberada e a íntegra fica
guardada. Um guard que reprova sempre é indistinguível de um guard desligado.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from scripts.distribution_guard import avaliar, coletar_perfil


def _banco(tmp_path: Path, linhas: list[dict], com_integra: bool = False) -> sqlite3.Connection:
    """Monta um banco mínimo com o formato que o guard inspeciona."""
    con = sqlite3.connect(tmp_path / "t.db")
    con.row_factory = sqlite3.Row
    cols = ["llm TEXT", "response_text TEXT", "is_probe INTEGER DEFAULT 0",
            "timestamp TEXT"]
    if com_integra:
        cols += ["response_full_text TEXT", "citation_window_chars INTEGER"]
    con.execute(f"CREATE TABLE citations ({', '.join(cols)})")
    for r in linhas:
        if com_integra:
            con.execute(
                "INSERT INTO citations (llm, response_text, timestamp, "
                "response_full_text, citation_window_chars) VALUES (?,?,?,?,?)",
                (r["llm"], r["texto"], "2026-08-31T12:00:00Z",
                 r.get("integra"), r.get("janela")))
        else:
            con.execute(
                "INSERT INTO citations (llm, response_text, timestamp) VALUES (?,?,?)",
                (r["llm"], r["texto"], "2026-08-31T12:00:00Z"))
    con.commit()
    return con


def _truncado(llm: str, n: int, janela: int = 200) -> list[dict]:
    return [{"llm": llm, "texto": "A" * janela} for _ in range(n)]


def _livre(llm: str, n: int) -> list[dict]:
    # comprimentos espalhados, como uma resposta real não recortada
    return [{"llm": llm, "texto": "A" * (250 + (i * 37) % 900)} for i in range(n)]


def test_reprova_o_defeito_de_31_08(tmp_path: Path) -> None:
    """Cinco braços cortados em 200 e um livre: exatamente o que aconteceu."""
    linhas = (_truncado("ChatGPT", 300) + _truncado("Claude", 300)
              + _truncado("Groq", 300) + _truncado("Gemini", 300)
              + _livre("Perplexity", 300))
    con = _banco(tmp_path, linhas)
    falhas = avaliar(coletar_perfil(con, None), con)
    assert falhas, "o guard não pode passar sobre a configuração que causou o incidente"
    assert any("assimetria entre braços" in f for f in falhas)
    assert any("não é recuperável" in f for f in falhas)


def test_aprova_a_configuracao_corrigida(tmp_path: Path) -> None:
    """Janela deliberada de 200 com a íntegra guardada precisa passar.

    Este é o teste que impede o alarme permanente: depois da correção todos os
    braços ficam empilhados em 200 caracteres em `response_text`, que é a mesma
    forma distribucional do defeito. O que os separa é `response_full_text`.
    """
    linhas = []
    for motor in ("ChatGPT", "Claude", "Groq", "Gemini", "Grok", "Perplexity"):
        for i in range(300):
            integra = "A" * (250 + (i * 37) % 900)
            linhas.append({"llm": motor, "texto": integra[:200],
                           "integra": integra, "janela": 200})
    con = _banco(tmp_path, linhas, com_integra=True)
    falhas = avaliar(coletar_perfil(con, None), con)
    assert not falhas, f"guard reprovou a configuração correta: {falhas}"


def test_reprova_janela_divergente_entre_bracos(tmp_path: Path) -> None:
    """Mesmo com a íntegra guardada, janelas diferentes quebram a comparação."""
    linhas = []
    for motor, janela in (("ChatGPT", 200), ("Claude", 200), ("Perplexity", 800)):
        for i in range(300):
            integra = "A" * (900 + i)
            linhas.append({"llm": motor, "texto": integra[:janela],
                           "integra": integra, "janela": janela})
    con = _banco(tmp_path, linhas, com_integra=True)
    falhas = avaliar(coletar_perfil(con, None), con)
    assert any("janela declarada difere entre braços" in f for f in falhas)


def test_reprova_integra_declarada_e_nao_gravada(tmp_path: Path) -> None:
    """Coluna existente e sempre nula é proteção inerte, o padrão do restore R2."""
    linhas = [{"llm": m, "texto": "A" * 200, "integra": None, "janela": 200}
              for m in ("ChatGPT", "Claude") for _ in range(300)]
    con = _banco(tmp_path, linhas, com_integra=True)
    falhas = avaliar(coletar_perfil(con, None), con)
    assert any("response_full_text" in f for f in falhas)


def test_ignora_braco_com_poucas_observacoes(tmp_path: Path) -> None:
    """Braço recém-incluído não pode disparar alarme por ainda não ter coletado."""
    linhas = _livre("ChatGPT", 300) + _truncado("Grok", 5)
    con = _banco(tmp_path, linhas)
    perfil = coletar_perfil(con, None)
    assert [p["llm"] for p in perfil] == ["ChatGPT"]


def test_resposta_naturalmente_curta_nao_e_truncamento(tmp_path: Path) -> None:
    """Comprimento pequeno com variância é resposta curta, não corte."""
    linhas = [{"llm": "ChatGPT", "texto": "A" * (40 + i % 25)} for i in range(300)]
    linhas += [{"llm": "Claude", "texto": "A" * (45 + i % 20)} for i in range(300)]
    con = _banco(tmp_path, linhas)
    falhas = avaliar(coletar_perfil(con, None), con)
    assert not falhas, f"falso positivo em resposta curta legítima: {falhas}"
