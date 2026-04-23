"""Onda 6b — CollectionLogger auto-persists JSONL on run exit."""
from __future__ import annotations

import json
import os
from pathlib import Path

import pytest


@pytest.fixture
def tmp_structured_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Redirect STRUCTURED_DIR to a tmp path per test (re-imports module)."""
    target = tmp_path / "structured"
    target.mkdir(parents=True, exist_ok=True)
    monkeypatch.setenv("PAPERS_STRUCTURED_LOG_DIR", str(target))
    monkeypatch.setenv("PAPERS_STRUCTURED_LOG_PERSIST", "1")
    # Force re-import to pick up the new env var
    import importlib
    import src.logging.logger as logger_module
    importlib.reload(logger_module)
    yield target
    # Restore module to default
    importlib.reload(logger_module)


def _get_logger_class():
    from src.logging.logger import CollectionLogger
    return CollectionLogger


def test_run_completes_and_persists_jsonl(tmp_structured_dir: Path) -> None:
    """Happy path: context manager sai com sucesso, arquivo JSONL existe."""
    CollectionLogger = _get_logger_class()
    logger = CollectionLogger(module="citation_test", vertical="fintech")
    with logger.run() as lg:
        lg.log_info("running some work")
        lg.log_query(llm="openai", query="q1", category="mercado", duration_ms=100, tokens=50, cost=0.001, cited=True)

    files = list(tmp_structured_dir.glob("citation_test_fintech_*.jsonl"))
    assert len(files) == 1, f"Expected 1 jsonl, found {[f.name for f in tmp_structured_dir.iterdir()]}"

    lines = files[0].read_text(encoding="utf-8").strip().splitlines()
    # First line is summary
    summary = json.loads(lines[0])
    assert summary["_type"] == "summary"
    assert summary["module"] == "citation_test"
    assert summary["vertical"] == "fintech"
    assert summary["total_queries"] == 1
    assert summary["total_cited"] == 1


def test_run_fails_still_persists_jsonl(tmp_structured_dir: Path) -> None:
    """Sad path: exception raised — finally block ainda persiste o log."""
    CollectionLogger = _get_logger_class()
    logger = CollectionLogger(module="citation_fail", vertical="saude")
    with pytest.raises(ValueError):
        with logger.run() as lg:
            lg.log_info("partial work")
            raise ValueError("simulated failure")

    files = list(tmp_structured_dir.glob("citation_fail_saude_*.jsonl"))
    assert len(files) == 1


def test_persist_disabled_via_env(tmp_structured_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Opt-out via PAPERS_STRUCTURED_LOG_PERSIST=0 suppresses save."""
    monkeypatch.setenv("PAPERS_STRUCTURED_LOG_PERSIST", "0")
    CollectionLogger = _get_logger_class()
    logger = CollectionLogger(module="no_persist", vertical="varejo")
    with logger.run() as lg:
        lg.log_info("work")

    files = list(tmp_structured_dir.glob("no_persist_*.jsonl"))
    assert files == []


def test_filename_encodes_module_vertical_runid(tmp_structured_dir: Path) -> None:
    """Filename pattern: {module}_{vertical}_{ts}_{run_id}.jsonl."""
    CollectionLogger = _get_logger_class()
    logger = CollectionLogger(module="context_analyzer", vertical="tecnologia")
    expected_run_id = logger.run_id
    with logger.run():
        pass

    files = list(tmp_structured_dir.glob("context_analyzer_tecnologia_*.jsonl"))
    assert len(files) == 1
    assert expected_run_id in files[0].name
