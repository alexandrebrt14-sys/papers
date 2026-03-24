"""Pydantic v2 models for the GEO Research API."""

from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field


# === Verticals ===

class VerticalInfo(BaseModel):
    """Detail of a single research vertical."""
    slug: str
    name: str
    entity_count: int
    entities: list[str]
    query_count: int
    last_collection: datetime | None = None


class VerticalListResponse(BaseModel):
    """List of all verticals with aggregate stats."""
    verticals: list[VerticalInfo]
    total_entities: int


# === Citations ===

class CitationRecord(BaseModel):
    """Single citation observation from the database."""
    timestamp: str
    llm: str
    query: str
    entity: str | None = None
    cited: bool
    position: int | None = None
    attribution: str | None = None
    sentiment: str | None = None
    vertical: str


class CitationRateByLLM(BaseModel):
    """Citation rate aggregated per LLM."""
    llm: str
    total_queries: int
    cited_count: int
    citation_rate: float
    avg_position: float | None = None


class CitationMetrics(BaseModel):
    """Citation metrics for a vertical over a period."""
    vertical: str
    period_days: int
    rates_by_llm: list[CitationRateByLLM]
    overall_rate: float
    total_observations: int


class EntityRanking(BaseModel):
    """Entity ranked by citation frequency."""
    entity: str
    citation_count: int
    citation_rate: float
    top_llm: str


# === Collections ===

class CollectionRun(BaseModel):
    """A single collection run record."""
    id: int
    module: str
    vertical: str
    status: str
    records_count: int
    duration_ms: int | None = None
    timestamp: str


class CollectionStatus(BaseModel):
    """Status of collections for a vertical."""
    vertical: str
    last_run: datetime | None = None
    modules_status: dict[str, str]
    total_runs_24h: int


# === Time Series ===

class TimeSeriesPoint(BaseModel):
    """Single data point in a time series."""
    date: str
    value: float
    label: str | None = None


# === Health ===

class HealthStatus(BaseModel):
    """API and database health status."""
    status: str = "ok"
    db_ok: bool
    tables: dict[str, int]
    verticals_active: list[str]
    last_collection: dict[str, str | None]
    uptime_seconds: float


# === FinOps ===

class FinOpsStatus(BaseModel):
    """FinOps budget and spending status."""
    budget_monthly: float
    spent_monthly: float
    pct_used: float
    by_platform: dict[str, dict]
    alerts: list[dict]


# === Analysis ===

class ReportRequest(BaseModel):
    """Request body for report generation."""
    vertical: str = "fintech"
    days: int = 30


class ReportSummary(BaseModel):
    """Summary of a statistical analysis report."""
    vertical: str
    generated_at: str
    period_days: int
    total_observations: int
    key_findings: list[str]
    statistical_tests: list[dict]


# === Tasks ===

class TaskStatus(BaseModel):
    """Status of a background task."""
    task_id: str
    status: str = "queued"  # queued | running | completed | failed
    vertical: str = ""
    started_at: str | None = None
    completed_at: str | None = None
    progress_pct: float | None = None
    result: dict | None = None
    error: str | None = None


# === Collection Trigger ===

class CollectionTriggerRequest(BaseModel):
    """Request body for triggering a collection."""
    vertical: str = "fintech"
    modules: list[str] = Field(default_factory=lambda: ["citation_tracker"])
