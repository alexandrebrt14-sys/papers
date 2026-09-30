"""engine_health.py — failure rate per engine, to retire an engine on data.

The treg fork dropped Perplexity from its AI-visibility panel because, over
1,395 production calls in 14 days, it failed 51% of the time (the other four
engines failed 0.3-8%). This module gives the papers pipeline the same basis:
every call to an engine is recorded with its outcome (``success``, ``failure``,
``timeout``, ``skipped``) in ``engine_call_outcomes`` (Migration 0011), and
:func:`failure_rates` / :func:`retirement_advice` turn those rows into a
recommendation with a confidence interval, so one bad afternoon does not retire
an engine and a chronic failure is not excused by a lucky day.

``skipped`` (engine does not serve the requested country) is not a failure and
is left out of the denominator.
"""
from __future__ import annotations

import math
import sqlite3
import time
from collections.abc import Iterable
from dataclasses import dataclass

from src.db import migrate_0011_engine_call_outcomes as mig

OUTCOME_STATUSES = mig.OUTCOME_STATUSES
DEFAULT_MAX_FAILURE_RATE = 0.20
DEFAULT_MIN_CALLS = 100


@dataclass(frozen=True)
class EngineOutcome:
    """One call to one engine."""
    engine: str
    status: str               # success | failure | timeout | skipped
    arm: str = "api"          # api | interface
    provider: str = ""
    latency_ms: int | None = None
    http_status: int | None = None
    error_class: str | None = None
    vertical: str = ""
    run_id: str = ""
    timestamp: str | None = None

    def __post_init__(self) -> None:
        if self.status not in OUTCOME_STATUSES:
            raise ValueError(f"status inválido: {self.status!r}")
        if self.arm not in ("api", "interface"):
            raise ValueError(f"arm inválido: {self.arm!r}")


def ensure_table(conn: sqlite3.Connection) -> None:
    """Idempotent: create ``engine_call_outcomes`` if missing."""
    mig.apply(conn)


def record_outcome(conn: sqlite3.Connection, outcome: EngineOutcome) -> None:
    """Persist one outcome (creates the table on first use)."""
    ensure_table(conn)
    ts = outcome.timestamp or time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    conn.execute(
        "INSERT INTO engine_call_outcomes (timestamp, engine, arm, provider, status, latency_ms, "
        "http_status, error_class, vertical, run_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (ts, outcome.engine, outcome.arm, outcome.provider, outcome.status, outcome.latency_ms,
         outcome.http_status, (outcome.error_class or None) and outcome.error_class[:120],
         outcome.vertical, outcome.run_id),
    )
    conn.commit()


def wilson_interval(successes: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """Wilson score interval for a proportion. ``(0, 1)`` when ``n == 0``."""
    if n <= 0:
        return 0.0, 1.0
    p = successes / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return max(0.0, centre - half), min(1.0, centre + half)


@dataclass(frozen=True)
class EngineRate:
    """Aggregated outcomes for one (engine, arm)."""
    engine: str
    arm: str
    success: int
    failure: int
    timeout: int
    skipped: int
    p50_latency_ms: int | None

    @property
    def attempted(self) -> int:
        """Calls that count in the denominator (skipped excluded)."""
        return self.success + self.failure + self.timeout

    @property
    def failure_rate(self) -> float:
        """Share of attempted calls that failed or timed out."""
        return (self.failure + self.timeout) / self.attempted if self.attempted else 0.0

    @property
    def failure_ci(self) -> tuple[float, float]:
        return wilson_interval(self.failure + self.timeout, self.attempted)


def failure_rates(
    conn: sqlite3.Connection,
    since: str | None = None,
    arm: str | None = None,
) -> list[EngineRate]:
    """Aggregate outcomes per (engine, arm), optionally since an ISO timestamp."""
    ensure_table(conn)
    where, params = [], []
    if since:
        where.append("timestamp >= ?")
        params.append(since)
    if arm:
        where.append("arm = ?")
        params.append(arm)
    clause = ("WHERE " + " AND ".join(where)) if where else ""
    rows = conn.execute(
        f"SELECT engine, arm, status, latency_ms FROM engine_call_outcomes {clause}",
        params,
    ).fetchall()
    buckets: dict[tuple[str, str], dict[str, list]] = {}
    for engine, arm_value, status, latency in rows:
        b = buckets.setdefault((engine, arm_value), {s: [] for s in OUTCOME_STATUSES})
        b[status].append(latency)
    out: list[EngineRate] = []
    for (engine, arm_value), b in sorted(buckets.items()):
        lat = sorted(v for v in b["success"] if v is not None)
        out.append(EngineRate(
            engine=engine, arm=arm_value,
            success=len(b["success"]), failure=len(b["failure"]),
            timeout=len(b["timeout"]), skipped=len(b["skipped"]),
            p50_latency_ms=lat[len(lat) // 2] if lat else None,
        ))
    return out


@dataclass(frozen=True)
class RetirementAdvice:
    engine: str
    arm: str
    verdict: str   # keep | watch | retire | insufficient_data
    reason: str


def retirement_advice(
    rates: Iterable[EngineRate],
    max_failure_rate: float = DEFAULT_MAX_FAILURE_RATE,
    min_calls: int = DEFAULT_MIN_CALLS,
) -> list[RetirementAdvice]:
    """Recommend per engine, from data only.

    - ``insufficient_data``: fewer than ``min_calls`` attempted calls.
    - ``retire``: the LOWER bound of the 95% Wilson interval of the failure rate
      is above ``max_failure_rate`` (the failure is chronic, not noise).
    - ``watch``: the point estimate is above the limit, the lower bound is not.
    - ``keep``: otherwise.
    The decision to actually drop an engine stays with the study owner.
    """
    advice: list[RetirementAdvice] = []
    for r in rates:
        lo, hi = r.failure_ci
        pct = f"{r.failure_rate:.1%} (IC95% {lo:.1%} a {hi:.1%}) em {r.attempted} chamadas"
        if r.attempted < min_calls:
            verdict, reason = "insufficient_data", f"amostra abaixo de {min_calls}: {pct}"
        elif lo > max_failure_rate:
            verdict, reason = "retire", f"falha crônica acima de {max_failure_rate:.0%}: {pct}"
        elif r.failure_rate > max_failure_rate:
            verdict, reason = "watch", f"falha acima de {max_failure_rate:.0%} sem margem: {pct}"
        else:
            verdict, reason = "keep", f"falha dentro do limite: {pct}"
        advice.append(RetirementAdvice(r.engine, r.arm, verdict, reason))
    return advice
