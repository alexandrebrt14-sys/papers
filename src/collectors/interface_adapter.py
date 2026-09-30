"""interface_adapter.py — optional "interface arm": answers as the PRODUCT shows them.

The papers cohort queries the engines through their APIs. What a person sees in
chatgpt.com, Copilot, Gemini or Google AI Mode is a different object: the web
product runs its own search, its own system prompt and exposes its own sources.
Cloro (https://cloro.dev, catalogued in the treg fork) scrapes those interfaces
and returns the answer text with the cited sources as structured fields.

This adapter is OFF by default and inert without configuration:

- enabled only with ``PAPERS_INTERFACE_ARM=cloro`` AND a present ``CLORO_API_KEY``;
  without both, :meth:`CloroInterfaceAdapter.is_enabled` is False and nothing
  else in the pipeline changes;
- the collection policy runs FIRST (``require_collection_open`` by default).
  The papers project closed its collections on 11/09/2026, so in this
  repository the adapter refuses every call before any network, cache or disk
  access. It exists so that a new study with its own protocol can pass its own
  policy (``policy_check=``) without writing a second collector;
- cost comes from the real ``X-Credits-Charged`` header times the per-credit
  price (``CLORO_USD_PER_CREDIT``), recorded in ``finops_usage`` through the
  existing tracker, which also feeds geo-finops (``unified_adapter``). Cloro
  charges only successful extractions, so a failed call records no cost;
- two spending ceilings: the FinOps budget for platform ``cloro``
  (``tracker.can_spend``) and a per-run cap (``CLORO_MAX_USD_PER_RUN``),
  checked against the worst-case price of the next call before it is made;
- every call writes one row to ``engine_call_outcomes`` (success, failure,
  timeout, skipped), the data needed to retire an engine the way treg retired
  Perplexity;
- fail-loud: a failure of an engine whose label (``Cloro-ChatGPT``...) is in
  ``MANDATORY_LLMS`` raises; any other engine failure is recorded and the run
  continues with the other engines.

Engine timeout is 75 s, as in treg. Perplexity is catalogued but not in the
default engine list: in treg it failed 51% of 1,395 calls over 14 days.
"""
from __future__ import annotations

import logging
import os
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from src.collection_policy import require_collection_open

logger = logging.getLogger(__name__)

CLORO_BASE_URL = "https://api.cloro.dev"
ENGINE_TIMEOUT_S = 75.0
DEFAULT_USD_PER_CREDIT = 0.0008   # Lite, cheapest listed plan; Hobby metered is 0.0004
DEFAULT_MAX_USD_PER_RUN = 0.50
DEFAULT_COUNTRY = "BR"
DEFAULT_ENGINES = ("chatgpt", "gemini", "copilot", "aimode")


@dataclass(frozen=True)
class InterfaceEngine:
    name: str
    label: str              # label used in MANDATORY_LLMS and engine_call_outcomes
    path: str
    geo_field: str          # "country" or "gl"
    credits: int            # documented price of a plain call (markdown only)
    refused: frozenset[str] = field(default_factory=frozenset)


ENGINES: dict[str, InterfaceEngine] = {
    "chatgpt": InterfaceEngine("chatgpt", "Cloro-ChatGPT", "/v1/monitor/chatgpt", "country", 7,
                               frozenset({"CN", "CZ", "HK", "IR", "MO", "RU", "VE"})),
    "gemini": InterfaceEngine("gemini", "Cloro-Gemini", "/v1/monitor/gemini", "country", 6,
                              frozenset({"BY", "CN", "RU"})),
    "copilot": InterfaceEngine("copilot", "Cloro-Copilot", "/v1/monitor/copilot", "country", 7,
                               frozenset({"BY", "CN", "RU", "SY", "VE"})),
    "aimode": InterfaceEngine("aimode", "Cloro-AIMode", "/v1/monitor/aimode", "gl", 6, frozenset()),
    "perplexity": InterfaceEngine("perplexity", "Cloro-Perplexity", "/v1/monitor/perplexity",
                                  "country", 6, frozenset({"CN"})),
}


class InterfaceArmError(RuntimeError):
    """A mandatory interface engine failed (fail-loud)."""


@dataclass
class InterfaceAnswer:
    """One engine, one prompt, as returned by the product interface."""
    engine: str
    label: str
    status: str                      # success | failure | timeout | skipped
    text: str = ""
    sources: list[str] = field(default_factory=list)
    model: str = ""
    credits_charged: float = 0.0
    cost_usd: float = 0.0
    cost_source: str = "none"        # header | estimated | none
    http_status: int | None = None
    latency_ms: int | None = None
    note: str = ""


def _env_float(name: str, default: float) -> float:
    raw = os.getenv(name, "").strip()
    if not raw:
        return default
    try:
        value = float(raw.replace(",", "."))
        return value if value >= 0 else default
    except ValueError:
        logger.warning("%s inválido; usando %s", name, default)
        return default


def _parse_sources(result: dict[str, Any]) -> list[str]:
    from src.analysis.citation_match import source_urls
    urls = source_urls(result.get("sources") or [])
    for u in source_urls(result.get("citationPills") or []):
        if u not in urls:
            urls.append(u)
    return urls


class CloroInterfaceAdapter:
    """Cloro client for the interface arm. See the module docstring for the contract."""

    def __init__(
        self,
        api_key: str | None = None,
        enabled: bool | None = None,
        engines: tuple[str, ...] | None = None,
        country: str | None = None,
        usd_per_credit: float | None = None,
        max_usd_per_run: float | None = None,
        tracker: Any | None = None,
        outcome_sink: Callable[[Any], None] | None = None,
        http: Any | None = None,
        policy_check: Callable[[], None] = require_collection_open,
        mandatory: set[str] | None = None,
        run_id: str = "",
        vertical: str = "",
    ) -> None:
        self._api_key = (api_key if api_key is not None else os.getenv("CLORO_API_KEY", "")).strip()
        self._enabled_flag = (
            enabled if enabled is not None
            else os.getenv("PAPERS_INTERFACE_ARM", "").strip().lower() == "cloro"
        )
        raw_engines = engines or tuple(
            e.strip().lower() for e in os.getenv("CLORO_ENGINES", ",".join(DEFAULT_ENGINES)).split(",")
            if e.strip()
        )
        unknown = [e for e in raw_engines if e not in ENGINES]
        if unknown:
            raise ValueError(f"motor de interface desconhecido: {unknown}")
        self.engines = raw_engines
        self.country = (country or os.getenv("CLORO_COUNTRY", DEFAULT_COUNTRY)).strip().upper()
        self.usd_per_credit = (usd_per_credit if usd_per_credit is not None
                               else _env_float("CLORO_USD_PER_CREDIT", DEFAULT_USD_PER_CREDIT))
        self.max_usd_per_run = (max_usd_per_run if max_usd_per_run is not None
                                else _env_float("CLORO_MAX_USD_PER_RUN", DEFAULT_MAX_USD_PER_RUN))
        self._tracker = tracker
        self._sink = outcome_sink
        self._http = http
        self._policy_check = policy_check
        self._mandatory = mandatory
        self._run_id = run_id
        self._vertical = vertical
        self.spent_usd = 0.0

    # --- configuration ---------------------------------------------------

    def is_enabled(self) -> bool:
        """Pure check: flag set AND key present. Never touches network or disk."""
        return bool(self._enabled_flag and self._api_key)

    def worst_case_usd(self, engine: str) -> float:
        """Documented price of one plain call, used for the per-run ceiling before calling."""
        return ENGINES[engine].credits * self.usd_per_credit

    def _mandatory_labels(self) -> set[str]:
        if self._mandatory is not None:
            return self._mandatory
        from src.config import mandatory_llms
        return mandatory_llms()

    # --- side effects ----------------------------------------------------

    def _emit(self, ans: InterfaceAnswer) -> None:
        if self._sink is None:
            return
        from src.persistence.engine_health import EngineOutcome
        try:
            self._sink(EngineOutcome(
                engine=ans.label, status=ans.status, arm="interface", provider="cloro",
                latency_ms=ans.latency_ms, http_status=ans.http_status,
                error_class=ans.note or None, vertical=self._vertical, run_id=self._run_id,
            ))
        except Exception as exc:  # noqa: BLE001 — health log never breaks collection
            logger.warning("registro de desfecho do motor falhou: %s", exc)

    def _record_cost(self, ans: InterfaceAnswer, prompt: str) -> None:
        self.spent_usd += ans.cost_usd
        if self._tracker is None or ans.cost_usd <= 0:
            return
        self._tracker.record(
            platform="cloro", model=f"cloro/{ans.engine}", operation="interface_arm",
            input_tokens=0, output_tokens=0, query=prompt[:200], run_id=self._run_id,
            cost_usd=ans.cost_usd,
        )

    def _finish(self, ans: InterfaceAnswer, prompt: str) -> InterfaceAnswer:
        self._emit(ans)
        if ans.status == "success":
            self._record_cost(ans, prompt)
        elif ans.status in ("failure", "timeout") and ans.label in self._mandatory_labels():
            raise InterfaceArmError(
                f"FAIL-LOUD: motor obrigatório {ans.label} terminou em {ans.status} ({ans.note})"
            )
        return ans

    # --- the call --------------------------------------------------------

    def query(self, engine: str, prompt: str) -> InterfaceAnswer | None:
        """Ask one engine through its interface.

        Returns None when the arm is disabled (nothing happens). Raises the
        policy error first when collection is closed, and ``InterfaceArmError``
        when a mandatory engine fails.
        """
        self._policy_check()
        if not self.is_enabled():
            return None
        spec = ENGINES[engine]
        if self.country in spec.refused:
            return self._finish(InterfaceAnswer(engine, spec.label, "skipped",
                                                note=f"{engine} não atende {self.country}"), prompt)
        if self.spent_usd + self.worst_case_usd(engine) > self.max_usd_per_run:
            return self._finish(InterfaceAnswer(engine, spec.label, "skipped",
                                                note="teto por execução atingido"), prompt)
        if self._tracker is not None and not self._tracker.can_spend("cloro"):
            return self._finish(InterfaceAnswer(engine, spec.label, "skipped",
                                                note="teto FinOps da cloro atingido"), prompt)

        import httpx
        client = self._http or httpx.Client(timeout=ENGINE_TIMEOUT_S)
        body = {"prompt": prompt, spec.geo_field: self.country, "include": {"markdown": True}}
        started = time.monotonic()
        try:
            resp = client.post(
                CLORO_BASE_URL + spec.path,
                headers={"Authorization": f"Bearer {self._api_key}"},
                json=body,
                timeout=ENGINE_TIMEOUT_S,
            )
        except httpx.TimeoutException:
            return self._finish(InterfaceAnswer(
                engine, spec.label, "timeout", latency_ms=int((time.monotonic() - started) * 1000),
                note=f"sem resposta em {int(ENGINE_TIMEOUT_S)} s"), prompt)
        except httpx.HTTPError as exc:
            return self._finish(InterfaceAnswer(
                engine, spec.label, "failure", latency_ms=int((time.monotonic() - started) * 1000),
                note=type(exc).__name__), prompt)
        finally:
            if self._http is None:
                client.close()
        latency = int((time.monotonic() - started) * 1000)

        try:
            data = resp.json()
        except ValueError:
            data = {}
        result = data.get("result") if isinstance(data, dict) else None
        text = ""
        if resp.status_code == 200 and isinstance(result, dict):
            text = str(result.get("text") or result.get("markdown") or "")
        if not text:
            return self._finish(InterfaceAnswer(
                engine, spec.label, "failure", http_status=resp.status_code, latency_ms=latency,
                note=f"HTTP {resp.status_code} sem texto"), prompt)

        header = resp.headers.get("X-Credits-Charged")
        try:
            credits = float(header) if header is not None else None
        except ValueError:
            credits = None
        cost_source = "header"
        if credits is None:
            credits, cost_source = float(spec.credits), "estimated"
            logger.warning("%s: resposta sem X-Credits-Charged; custo estimado pela tabela", spec.label)
        return self._finish(InterfaceAnswer(
            engine=engine, label=spec.label, status="success", text=text,
            sources=_parse_sources(result), model=str(result.get("model") or ""),
            credits_charged=credits, cost_usd=round(credits * self.usd_per_credit, 8),
            cost_source=cost_source, http_status=resp.status_code, latency_ms=latency,
        ), prompt)

    def query_all(self, prompt: str) -> list[InterfaceAnswer]:
        """Ask every configured engine in sequence; one failure never stops the others
        (unless the engine is mandatory, which raises)."""
        self._policy_check()
        if not self.is_enabled():
            return []
        answers = []
        for engine in self.engines:
            ans = self.query(engine, prompt)
            if ans is not None:
                answers.append(ans)
        return answers


def sqlite_outcome_sink(db_path: str | None = None) -> Callable[[Any], None]:
    """Sink that writes outcomes to ``engine_call_outcomes`` in papers.db (or ``db_path``)."""
    import sqlite3
    from pathlib import Path

    from src.persistence.engine_health import record_outcome

    path = db_path or os.getenv(
        "PAPERS_DB_PATH", str(Path(__file__).resolve().parents[2] / "data" / "papers.db")
    )

    def _sink(outcome: Any) -> None:
        conn = sqlite3.connect(path)
        try:
            record_outcome(conn, outcome)
        finally:
            conn.close()

    return _sink
