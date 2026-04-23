"""Testes do DriftDetector — record_version, detected_change flag, history."""
from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from src.collectors.drift_detector import DriftDetector
from src.collectors.llm_client import LLMResponse


@pytest.fixture
def drift_db(tmp_path: Path) -> str:
    """Minimal DB with just the model_versions table."""
    db_path = str(tmp_path / "drift.db")
    conn = sqlite3.connect(db_path)
    conn.execute(
        """
        CREATE TABLE model_versions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
            provider TEXT NOT NULL,
            model_alias TEXT NOT NULL,
            model_version TEXT DEFAULT '',
            response_hash TEXT DEFAULT '',
            knowledge_cutoff TEXT DEFAULT '',
            detected_change INTEGER DEFAULT 0,
            UNIQUE(provider, model_alias, model_version)
        )
        """
    )
    conn.commit()
    conn.close()
    return db_path


def _resp(provider: str, model: str, text: str, version: str | None = None) -> LLMResponse:
    raw = {"model": version} if version and provider in ("openai", "anthropic") else {}
    if version and provider == "google":
        raw = {"modelVersion": version}
    return LLMResponse(
        model=model, provider=provider, query="probe",
        response_text=text, sources=[], cited_entities=[],
        timestamp="2026-04-23T15:00:00Z", latency_ms=100, raw=raw,
    )


def test_first_record_no_drift(drift_db: str) -> None:
    """Primeira gravação nunca é drift."""
    det = DriftDetector(drift_db)
    out = det.record_version(_resp("openai", "gpt-4o-mini", "paris", "gpt-4o-mini-2024-07-18"))
    assert out["detected_change"] is False
    assert out["actual_version"] == "gpt-4o-mini-2024-07-18"


def test_version_change_detects_drift(drift_db: str) -> None:
    """Mesma alias, version diferente → drift=True."""
    det = DriftDetector(drift_db)
    det.record_version(_resp("openai", "gpt-4o-mini", "paris", "gpt-4o-mini-2024-07-18"))
    out = det.record_version(_resp("openai", "gpt-4o-mini", "paris", "gpt-4o-mini-2025-01-15"))
    assert out["detected_change"] is True


def test_response_hash_change_detects_drift(drift_db: str) -> None:
    """Mesma version, response diferente → drift=True."""
    det = DriftDetector(drift_db)
    det.record_version(_resp("openai", "gpt-4o-mini", "paris", "gpt-4o-mini-2024-07-18"))
    out = det.record_version(_resp("openai", "gpt-4o-mini", "paris, france", "gpt-4o-mini-2024-07-18"))
    assert out["detected_change"] is True


def test_drift_event_persisted_with_flag(drift_db: str) -> None:
    """Drift=1 é gravado na row (bug fix Onda 6a)."""
    det = DriftDetector(drift_db)
    det.record_version(_resp("openai", "gpt-4o-mini", "paris", "v1"))
    det.record_version(_resp("openai", "gpt-4o-mini", "paris", "v2"))
    events = det.get_drift_events()
    # Pelo menos o v2 deve ter detected_change=1
    assert any(e["model_version"] == "v2" and e["detected_change"] == 1 for e in events)


def test_version_history_returns_chronological(drift_db: str) -> None:
    det = DriftDetector(drift_db)
    det.record_version(_resp("anthropic", "claude-haiku", "resposta a", "v1"))
    det.record_version(_resp("anthropic", "claude-haiku", "resposta b", "v2"))
    hist = det.get_version_history("anthropic", "claude-haiku")
    assert len(hist) >= 2
    versions = [h["model_version"] for h in hist]
    assert "v1" in versions and "v2" in versions
