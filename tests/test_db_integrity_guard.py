"""Testes do guard que impede o dataset de encolher.

Cobre o cenario real do incidente 2026-08-09: um banco com 864 citations
substituindo um de 63.940 sem que nada no pipeline reclamasse.
"""
from __future__ import annotations

import json
import os
import sqlite3
import subprocess
import sys

import pytest

GUARD = os.path.join("scripts", "db_integrity_guard.py")
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def make_db(path: str, citations: int, context: int = 0, runs: int = 0) -> str:
    con = sqlite3.connect(path)
    con.execute("CREATE TABLE citations (id INTEGER PRIMARY KEY, llm TEXT)")
    con.execute("CREATE TABLE citation_context (id INTEGER PRIMARY KEY)")
    con.execute("CREATE TABLE collection_runs (id INTEGER PRIMARY KEY)")
    con.execute("CREATE TABLE finops_usage (id INTEGER PRIMARY KEY)")
    con.executemany(
        "INSERT INTO citations (llm) VALUES (?)", [("chatgpt",)] * citations
    )
    con.executemany("INSERT INTO citation_context DEFAULT VALUES", [()] * context)
    con.executemany("INSERT INTO collection_runs DEFAULT VALUES", [()] * runs)
    con.commit()
    con.close()
    return path


def run_guard(cmd: str, db: str, cwd: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, os.path.join(REPO, GUARD), cmd, "--db", db],
        capture_output=True,
        text=True,
        cwd=cwd,
    )


@pytest.fixture()
def workdir(tmp_path):
    (tmp_path / "data").mkdir()
    return str(tmp_path)


def test_update_cria_piso(workdir):
    db = make_db(os.path.join(workdir, "papers.db"), citations=1000, context=500)
    r = run_guard("update", db, workdir)
    assert r.returncode == 0, r.stderr

    floor_file = os.path.join(workdir, "data", "db_floor.json")
    assert os.path.exists(floor_file)
    with open(floor_file, encoding="utf-8") as f:
        floor = json.load(f)["floor"]
    assert floor["citations"] == 1000
    assert floor["citation_context"] == 500


def test_check_passa_quando_banco_cresce(workdir):
    db = os.path.join(workdir, "papers.db")
    make_db(db, citations=1000)
    run_guard("update", db, workdir)

    os.remove(db)
    make_db(db, citations=1200)
    r = run_guard("check", db, workdir)
    assert r.returncode == 0, r.stderr


def test_check_barra_banco_degenerado(workdir):
    """O caso do incidente: 63.940 citations viram 864."""
    db = os.path.join(workdir, "papers.db")
    make_db(db, citations=63940, context=25128)
    run_guard("update", db, workdir)

    os.remove(db)
    make_db(db, citations=864)
    r = run_guard("check", db, workdir)
    assert r.returncode == 2
    assert "DEGENERADO" in r.stderr
    assert "864" in r.stderr


def test_tolerancia_absorve_vacuum(workdir):
    """Queda de 1% nao derruba o run; 10% derruba."""
    db = os.path.join(workdir, "papers.db")
    make_db(db, citations=10000)
    run_guard("update", db, workdir)

    os.remove(db)
    make_db(db, citations=9900)  # -1%, dentro da tolerancia de 2%
    assert run_guard("check", db, workdir).returncode == 0

    os.remove(db)
    make_db(db, citations=9000)  # -10%, fora
    assert run_guard("check", db, workdir).returncode == 2


def test_banco_ausente_ou_corrompido_falha(workdir):
    ausente = os.path.join(workdir, "nao_existe.db")
    assert run_guard("check", ausente, workdir).returncode == 2

    corrompido = os.path.join(workdir, "lixo.db")
    with open(corrompido, "wb") as f:
        f.write(b"isto nao e um banco sqlite")
    assert run_guard("check", corrompido, workdir).returncode == 2


def test_piso_nunca_baixa(workdir):
    """Rodar update sobre um banco menor nao rebaixa o piso."""
    db = os.path.join(workdir, "papers.db")
    make_db(db, citations=5000)
    run_guard("update", db, workdir)

    os.remove(db)
    make_db(db, citations=100)
    run_guard("update", db, workdir)

    with open(os.path.join(workdir, "data", "db_floor.json"), encoding="utf-8") as f:
        assert json.load(f)["floor"]["citations"] == 5000
