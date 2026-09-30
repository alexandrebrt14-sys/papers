"""Taxa de falha por motor e recomendação de retirada com base em dado."""
from __future__ import annotations

import sqlite3

import pytest

from src.db.client import DatabaseClient
from src.persistence.engine_health import (
    EngineOutcome,
    EngineRate,
    failure_rates,
    record_outcome,
    retirement_advice,
    wilson_interval,
)


def _fill(conn, engine, success, failure, timeout=0, skipped=0, arm="api"):
    for status, n in (("success", success), ("failure", failure), ("timeout", timeout), ("skipped", skipped)):
        for i in range(n):
            record_outcome(conn, EngineOutcome(engine=engine, status=status, arm=arm,
                                               latency_ms=1000 + i if status == "success" else None,
                                               timestamp="2026-10-01T00:00:00Z"))


def test_taxa_exclui_ignorados_do_denominador():
    conn = sqlite3.connect(":memory:")
    _fill(conn, "Gemini", success=8, failure=1, timeout=1, skipped=5)
    (r,) = failure_rates(conn)
    assert r.attempted == 10 and r.failure_rate == pytest.approx(0.2) and r.skipped == 5
    assert r.p50_latency_ms == 1004


def test_filtros_por_braco_e_data():
    conn = sqlite3.connect(":memory:")
    _fill(conn, "ChatGPT", 3, 0, arm="api")
    _fill(conn, "Cloro-ChatGPT", 1, 2, arm="interface")
    assert [r.engine for r in failure_rates(conn, arm="interface")] == ["Cloro-ChatGPT"]
    assert failure_rates(conn, since="2026-10-02") == []


def test_caso_perplexity_do_treg_recomenda_retirar():
    # 1.395 chamadas, 51% de falha: o caso que tirou a Perplexity do painel do treg.
    perplexity = EngineRate("Perplexity", "interface", success=684, failure=180, timeout=531,
                            skipped=0, p50_latency_ms=None)
    gemini = EngineRate("Gemini", "interface", success=1350, failure=45, timeout=0,
                        skipped=0, p50_latency_ms=None)
    advice = {a.engine: a for a in retirement_advice([perplexity, gemini])}
    assert advice["Perplexity"].verdict == "retire"
    assert advice["Gemini"].verdict == "keep"
    assert "1395 chamadas" in advice["Perplexity"].reason


def test_amostra_pequena_e_zona_de_observacao():
    small = EngineRate("X", "api", success=5, failure=5, timeout=0, skipped=0, p50_latency_ms=None)
    border = EngineRate("Y", "api", success=150, failure=45, timeout=5, skipped=0, p50_latency_ms=None)
    advice = {a.engine: a.verdict for a in retirement_advice([small, border])}
    assert advice == {"X": "insufficient_data", "Y": "watch"}


def test_wilson():
    assert wilson_interval(0, 0) == (0.0, 1.0)
    lo, hi = wilson_interval(51, 100)
    assert 0.41 < lo < 0.51 < hi < 0.61


def test_status_invalido_recusado():
    with pytest.raises(ValueError):
        EngineOutcome(engine="x", status="ok")
    with pytest.raises(ValueError):
        EngineOutcome(engine="x", status="success", arm="web")
    conn = sqlite3.connect(":memory:")
    record_outcome(conn, EngineOutcome(engine="x", status="success"))
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("INSERT INTO engine_call_outcomes (engine, status) VALUES ('x', 'ok')")


def test_database_client_cria_a_tabela(tmp_path):
    db = DatabaseClient(str(tmp_path / "p.db"))
    db.connect()
    try:
        names = {r[0] for r in db._conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        assert "engine_call_outcomes" in names
    finally:
        db.close()


def test_tracker_registra_custo_medido_pelo_provedor(tmp_path, monkeypatch):
    from src.finops import unified_adapter
    from src.finops.tracker import FinOpsTracker
    mirrored = []
    monkeypatch.setattr(unified_adapter, "record", lambda **kw: mirrored.append(kw))
    tracker = FinOpsTracker(db_path=str(tmp_path / "f.db"))
    rec = tracker.record(platform="cloro", model="cloro/chatgpt", operation="interface_arm",
                         input_tokens=0, output_tokens=0, cost_usd=0.0036)
    assert rec.cost_usd == pytest.approx(0.0036)
    assert tracker.can_spend("cloro")
    # O mesmo custo segue para o geo-finops pelo adapter existente.
    assert mirrored[0]["platform"] == "cloro" and mirrored[0]["cost_usd"] == pytest.approx(0.0036)
    # Sem override, o custo continua vindo dos tokens.
    rec2 = tracker.record(platform="openai", model="gpt-4o-mini-2024-07-18", operation="mention_judge",
                          input_tokens=1_000_000, output_tokens=0)
    assert rec2.cost_usd == pytest.approx(0.15)
