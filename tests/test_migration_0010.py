"""Migration 0010 — a íntegra da resposta e a janela, gravadas por linha.

Antes de 31/08/2026 o banco guardava só a janela de extração e descartava o
resto da resposta. Nenhuma das 80.638 observações da série era auditável: um
revisor não tinha como reproduzir a extração, e o projeto não tinha como medir
o que a janela deixava de fora.

Estes testes cobrem também a armadilha que a própria 0010 caiu ao ser escrita:
chamada de dentro de `_migrate_add_vertical`, ela roda ANTES do executescript
que cria `citations`, morre em "no such table" e o except a transforma em log
DEBUG. O skip fica invisível e a coluna nunca aparece num banco novo — o mesmo
padrão do restore R2 que ficou dois meses inerte.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

from src.db import migrate_0010_full_response
from src.db.client import DatabaseClient


def test_banco_novo_ja_nasce_com_as_colunas(tmp_path: Path) -> None:
    """Regressão do skip silencioso: connect() precisa deixar as colunas prontas."""
    db = DatabaseClient(str(tmp_path / "novo.db"))
    db.connect()
    cols = {r[1] for r in db._conn.execute("PRAGMA table_info(citations)").fetchall()}
    assert "response_full_text" in cols
    assert "citation_window_chars" in cols


def test_apply_e_idempotente(tmp_path: Path) -> None:
    db = DatabaseClient(str(tmp_path / "idem.db"))
    db.connect()
    assert migrate_0010_full_response.apply(db._conn) == []


def test_insert_grava_integra_e_janela(tmp_path: Path) -> None:
    db = DatabaseClient(str(tmp_path / "rt.db"))
    db.connect()
    integra = "A" * 150 + " Nubank lidera. " + "B" * 1500
    db.insert_citations([{
        "timestamp": "2026-08-31T12:00:00Z",
        "llm": "Perplexity", "model": "sonar", "query": "melhor fintech",
        "query_category": "descoberta", "query_lang": "pt",
        "cited": True,
        "response_text": integra[:200],
        "response_full_text": integra,
        "citation_window_chars": 200,
        "all_sources": [],
    }], vertical="fintech")
    row = db._conn.execute(
        "SELECT response_text, response_full_text, citation_window_chars FROM citations"
    ).fetchone()
    assert len(row[0]) == 200, "response_text é a janela"
    assert row[1] == integra, "response_full_text é a resposta antes do corte"
    assert row[2] == 200, "a janela fica legível na própria linha"


def test_backfill_anota_a_janela_efetiva_das_linhas_historicas(tmp_path: Path) -> None:
    """Para linhas antigas a janela não é estimativa: é o que o extrator viu."""
    db = DatabaseClient(str(tmp_path / "bf.db"))
    db.connect()
    db.insert_citations([
        {"timestamp": "2026-06-01T00:00:00Z", "llm": "Claude", "model": "haiku",
         "query": "q", "query_category": "descoberta", "query_lang": "pt",
         "cited": False, "response_text": "X" * 200, "all_sources": []},
        {"timestamp": "2026-06-01T00:00:00Z", "llm": "Perplexity", "model": "sonar",
         "query": "q", "query_category": "descoberta", "query_lang": "pt",
         "cited": True, "response_text": "Y" * 1450, "all_sources": []},
    ], vertical="fintech")
    db._conn.execute("UPDATE citations SET citation_window_chars = NULL")
    db._conn.commit()

    n = migrate_0010_full_response.backfill_window(db._conn)
    assert n == 2
    janelas = dict(db._conn.execute(
        "SELECT llm, citation_window_chars FROM citations").fetchall())
    assert janelas["Claude"] == 200
    assert janelas["Perplexity"] == 1450, (
        "a assimetria histórica precisa ficar visível na coluna, não escondida"
    )
