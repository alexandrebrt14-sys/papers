"""Centralized logging with structured output, file rotation, and observability.

Provides:
- Structured JSON logs for machine parsing
- Human-readable console output with Rich
- File-based log rotation (daily, 30-day retention)
- Collection run tracing with correlation IDs
- Performance metrics (latency, token usage, cost)
- Error tracking with context
"""

from __future__ import annotations

import json
import logging
import logging.handlers
import os
import time
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Generator

from rich.console import Console
from rich.logging import RichHandler

# === Paths ===
LOG_DIR = Path(os.getenv("PAPERS_LOG_DIR", "logs"))
LOG_DIR.mkdir(exist_ok=True)

# Structured JSONL runs are persisted to .logs/structured/ for artifact upload
# by the daily-collect workflow (gap Onda 6b — observability handoff to CI).
STRUCTURED_DIR = Path(os.getenv("PAPERS_STRUCTURED_LOG_DIR", ".logs/structured"))
STRUCTURED_DIR.mkdir(parents=True, exist_ok=True)


# === Structured Log Record ===

@dataclass
class CollectionEvent:
    """A single collection event for structured logging."""
    timestamp: str = ""
    run_id: str = ""
    module: str = ""
    event: str = ""  # started, query_sent, query_received, error, completed
    llm: str = ""
    query: str = ""
    query_category: str = ""
    duration_ms: int = 0
    tokens: int = 0
    cost_usd: float = 0.0
    cited: bool | None = None
    error: str = ""
    details: dict[str, Any] = field(default_factory=dict)

    def to_json(self) -> str:
        d = {k: v for k, v in asdict(self).items() if v or v == 0 or v is False}
        return json.dumps(d, ensure_ascii=False)


# === JSON File Handler ===

class JsonFileHandler(logging.Handler):
    """Writes structured JSON logs, one per line (JSONL format)."""

    def __init__(self, filepath: Path) -> None:
        super().__init__()
        self.filepath = filepath

    def emit(self, record: logging.LogRecord) -> None:
        try:
            entry = {
                "ts": datetime.now(timezone.utc).isoformat(),
                "level": record.levelname,
                "logger": record.name,
                "message": record.getMessage(),
            }
            if hasattr(record, "event_data"):
                entry["event"] = record.event_data
            with open(self.filepath, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except Exception:
            self.handleError(record)


# === Setup ===

_configured = False

def setup_logging(level: str = "INFO", json_logs: bool = True) -> None:
    """Configure logging for the entire application."""
    global _configured
    if _configured:
        return
    _configured = True

    root = logging.getLogger()
    root.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Console handler (Rich, human-readable)
    console = Console(stderr=True)
    rich_handler = RichHandler(
        console=console,
        show_time=True,
        show_path=False,
        markup=True,
        rich_tracebacks=True,
    )
    rich_handler.setLevel(logging.INFO)
    root.addHandler(rich_handler)

    # Rotating file handler (plain text)
    file_handler = logging.handlers.TimedRotatingFileHandler(
        LOG_DIR / "papers.log",
        when="midnight",
        backupCount=30,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s [%(name)s] %(levelname)s: %(message)s"
    ))
    root.addHandler(file_handler)

    # JSON structured log (JSONL)
    if json_logs:
        json_handler = JsonFileHandler(LOG_DIR / "papers.jsonl")
        json_handler.setLevel(logging.DEBUG)
        root.addHandler(json_handler)

    # Error-only file
    error_handler = logging.handlers.TimedRotatingFileHandler(
        LOG_DIR / "errors.log",
        when="midnight",
        backupCount=90,
        encoding="utf-8",
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(logging.Formatter(
        "%(asctime)s [%(name)s] %(levelname)s: %(message)s\n%(exc_info)s"
    ))
    root.addHandler(error_handler)

    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Get a named logger."""
    return logging.getLogger(name)


# === Collection Logger (high-level tracing) ===

class CollectionLogger:
    """High-level logger for collection runs with tracing and metrics.

    Integrado em BaseCollector em 2026-04-19 (Onda 8) via `structured_logger`
    lazy. Aceita `vertical` opcional para prefixar logs quando rodando em
    contexto multi-vertical.
    """

    def __init__(self, module: str, vertical: str = "") -> None:
        self.module = module
        self.vertical = vertical
        self.run_id = str(uuid.uuid4())[:8]
        suffix = f".{vertical}" if vertical else ""
        self.logger = get_logger(f"papers.{module}{suffix}")
        self.start_time: float = 0
        self.events: list[CollectionEvent] = []
        self.total_tokens: int = 0
        self.total_cost: float = 0.0
        self.total_queries: int = 0
        self.total_cited: int = 0
        self.errors: int = 0

    @contextmanager
    def run(self) -> Generator[CollectionLogger, None, None]:
        """Context manager for a complete collection run.

        On exit (success or failure), persists the full event stream as a JSONL
        file under STRUCTURED_DIR. Disable via PAPERS_STRUCTURED_LOG_PERSIST=0.
        """
        self.start_time = time.time()
        self._log_event("started", f"Coleta iniciada: {self.module}")
        try:
            yield self
            duration = int((time.time() - self.start_time) * 1000)
            self._log_event(
                "completed",
                f"Coleta concluída: {self.total_queries} queries, "
                f"{self.total_cited} citações, {self.errors} erros, "
                f"{duration}ms, {self.total_tokens} tokens, ${self.total_cost:.4f}",
                duration_ms=duration,
            )
        except Exception as e:
            duration = int((time.time() - self.start_time) * 1000)
            self._log_event("fatal", f"Coleta falhou: {e}", error=str(e), duration_ms=duration)
            raise
        finally:
            if os.getenv("PAPERS_STRUCTURED_LOG_PERSIST", "1") == "1":
                try:
                    self.save_run_log()
                except Exception as exc:
                    self.logger.debug(f"save_run_log failed: {exc}")

    def log_query(
        self, llm: str, query: str, category: str,
        duration_ms: int = 0, tokens: int = 0, cost: float = 0.0,
        cited: bool | None = None, error: str = "",
    ) -> None:
        """Log a single LLM query."""
        self.total_queries += 1
        self.total_tokens += tokens
        self.total_cost += cost
        if cited:
            self.total_cited += 1
        if error:
            self.errors += 1

        event = "query_error" if error else ("query_cited" if cited else "query_not_cited")
        msg = f"[{llm}] {query[:50]}... → {'CITOU' if cited else 'NÃO CITOU' if cited is not None else 'ERRO'}"
        if error:
            msg = f"[{llm}] {query[:50]}... → ERRO: {error}"

        self._log_event(
            event, msg,
            llm=llm, query=query, query_category=category,
            duration_ms=duration_ms, tokens=tokens, cost_usd=cost,
            cited=cited, error=error,
        )

    def log_info(self, message: str, **kwargs: Any) -> None:
        """Log an informational message."""
        self._log_event("info", message, **kwargs)

    def log_error(self, message: str, error: str = "", **kwargs: Any) -> None:
        """Log an error."""
        self.errors += 1
        self._log_event("error", message, error=error, **kwargs)

    def _log_event(self, event: str, message: str, **kwargs: Any) -> None:
        """Internal: create and log a structured event."""
        evt = CollectionEvent(
            timestamp=datetime.now(timezone.utc).isoformat(),
            run_id=self.run_id,
            module=self.module,
            event=event,
            **kwargs,
        )
        self.events.append(evt)

        # Log to Python logger with structured data attached
        level = logging.ERROR if "error" in event or "fatal" in event else logging.INFO
        record = self.logger.makeRecord(
            self.logger.name, level, "", 0, message, (), None,
        )
        record.event_data = evt.to_json()  # type: ignore
        self.logger.handle(record)

    def get_summary(self) -> dict[str, Any]:
        """Return run summary for persistence."""
        return {
            "run_id": self.run_id,
            "module": self.module,
            "vertical": self.vertical,
            "total_queries": self.total_queries,
            "total_cited": self.total_cited,
            "citation_rate": round(self.total_cited / max(self.total_queries, 1), 3),
            "total_tokens": self.total_tokens,
            "total_cost_usd": round(self.total_cost, 4),
            "errors": self.errors,
            "duration_ms": int((time.time() - self.start_time) * 1000) if self.start_time else 0,
            "event_count": len(self.events),
        }

    def save_run_log(self, path: Path | None = None) -> str:
        """Save the complete run log as JSONL file.

        Default target: STRUCTURED_DIR/{module}_{vertical}_{ts}_{run_id}.jsonl.
        This path is what the GitHub Actions workflow uploads as artifact.
        """
        if path is None:
            ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
            vert_suffix = f"_{self.vertical}" if self.vertical else ""
            path = STRUCTURED_DIR / f"{self.module}{vert_suffix}_{ts}_{self.run_id}.jsonl"

        with open(path, "w", encoding="utf-8") as f:
            # Header: summary
            f.write(json.dumps({"_type": "summary", **self.get_summary()}, ensure_ascii=False) + "\n")
            # Events
            for evt in self.events:
                f.write(evt.to_json() + "\n")

        self.logger.info(f"Log de execução salvo: {path}")
        return str(path)
