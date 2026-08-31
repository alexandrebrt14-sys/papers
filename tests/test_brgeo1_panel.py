"""Definição do painel do índice BRGEO-1.

A amplitude B é um terço do índice e é calculada contra o painel de motores.
Enquanto o painel foi definido por contagem de observações, ele favorecia o
braço aposentado contra o braço novo: em 31/08/2026 o índice de referência
rodava com o Groq, encerrado em 16/08 com meses de volume acumulado, e sem o
Grok, que o substituiu em 23/08 e ainda tinha poucas observações.

Nenhum limiar de contagem corrige isso, porque o problema é temporal e não de
volume. Estes testes fixam o critério de atividade.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from scripts.brgeo1_index import DIAS_PARA_CONSIDERAR_ATIVO, motores_ativos


def _banco(tmp_path: Path, linhas: list[tuple[str, str, int]]) -> sqlite3.Connection:
    """linhas: (llm, data ISO, quantas observações)."""
    con = sqlite3.connect(tmp_path / "p.db")
    con.execute("CREATE TABLE citations (llm TEXT, vertical TEXT, timestamp TEXT)")
    for llm, data, n in linhas:
        for _ in range(n):
            con.execute("INSERT INTO citations VALUES (?,?,?)",
                        (llm, "fintech", f"{data}T12:00:00"))
    con.commit()
    return con


def test_braco_aposentado_sai_do_painel(tmp_path: Path) -> None:
    """O caso real: Groq encerrado em 16/08 com volume alto, Grok vivo desde 23/08."""
    con = _banco(tmp_path, [
        ("ChatGPT", "2026-08-31", 3744),
        ("Groq", "2026-08-16", 3552),   # aposentado, muito volume
        ("Grok", "2026-08-29", 96),     # vivo, pouco volume
    ])
    painel = motores_ativos(con, "fintech")
    assert "Grok" in painel, "braço vivo precisa entrar mesmo com poucas observações"
    assert "Groq" not in painel, "braço aposentado não pode ocupar vaga no painel"
    assert "ChatGPT" in painel


def test_ancorado_no_dado_e_nao_no_relogio(tmp_path: Path) -> None:
    """Rodar o mesmo banco hoje ou daqui a um ano precisa dar o mesmo painel.

    Se a janela fosse medida contra `now`, um banco arquivado devolveria painel
    vazio e a amplitude viraria zero para toda a coorte.
    """
    con = _banco(tmp_path, [
        ("ChatGPT", "2024-01-15", 500),
        ("Claude", "2024-01-14", 500),
        ("Antigo", "2023-06-01", 500),
    ])
    painel = motores_ativos(con, "fintech")
    assert painel == {"ChatGPT", "Claude"}


def test_janela_de_atividade_e_configuravel(tmp_path: Path) -> None:
    con = _banco(tmp_path, [
        ("ChatGPT", "2026-08-31", 100),
        ("Antigo", "2026-08-01", 100),
    ])
    assert motores_ativos(con, "fintech", dias=14) == {"ChatGPT"}
    assert motores_ativos(con, "fintech", dias=60) == {"ChatGPT", "Antigo"}


def test_vertical_sem_dado_devolve_painel_vazio(tmp_path: Path) -> None:
    con = _banco(tmp_path, [("ChatGPT", "2026-08-31", 10)])
    assert motores_ativos(con, "saude") == set()


def test_default_documentado_bate_com_o_usado(tmp_path: Path) -> None:
    """O default é parâmetro declarado da especificação, não número solto."""
    assert DIAS_PARA_CONSIDERAR_ATIVO == 14
