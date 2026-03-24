"""GEO Research API — FastAPI application for multi-vertical LLM citation tracking.

Production-ready REST API exposing citation data, collection status,
statistical analysis, and FinOps monitoring for the Papers research platform.
"""

from __future__ import annotations

import csv
import io
import logging
import os
import time
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse

from src.api.models import (
    CitationMetrics,
    CitationRateByLLM,
    CitationRecord,
    CollectionRun,
    CollectionStatus,
    CollectionTriggerRequest,
    EntityRanking,
    FinOpsStatus,
    HealthStatus,
    ReportRequest,
    ReportSummary,
    TaskStatus,
    TimeSeriesPoint,
    VerticalInfo,
    VerticalListResponse,
)
from src.config import VERTICALS, get_cohort, get_queries, list_verticals
from src.db.client import DatabaseClient

logger = logging.getLogger("api")

# ============================================================
# Global state
# ============================================================

_db: DatabaseClient | None = None
_start_time: float = 0.0
_tasks: dict[str, TaskStatus] = {}


def get_db() -> DatabaseClient:
    """Dependency that returns the shared DatabaseClient."""
    if _db is None or _db._conn is None:
        raise HTTPException(status_code=503, detail="Banco de dados não inicializado.")
    return _db


# ============================================================
# Auth dependency (optional API key)
# ============================================================

API_KEY = os.getenv("API_KEY", "")


def verify_api_key(request: Request) -> None:
    """Verify API key if API_KEY env var is set. No-op if unset."""
    if not API_KEY:
        return
    header = request.headers.get("X-API-Key", "")
    query_key = request.query_params.get("api_key", "")
    if header != API_KEY and query_key != API_KEY:
        raise HTTPException(status_code=401, detail="Chave de API inválida.")


# ============================================================
# Lifespan (startup / shutdown)
# ============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize DB on startup, close on shutdown."""
    global _db, _start_time
    _start_time = time.time()
    _db = DatabaseClient()
    _db.connect()
    logger.info("API iniciada — banco de dados conectado.")
    yield
    if _db:
        _db.close()
        logger.info("API encerrada — banco de dados fechado.")


# ============================================================
# App creation
# ============================================================

app = FastAPI(
    title="GEO Research API",
    description="Multi-vertical LLM citation tracking for Brazilian companies",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# Request logging middleware
# ============================================================

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log every request with timing."""
    start = time.time()
    response = await call_next(request)
    elapsed = (time.time() - start) * 1000
    logger.info(f"{request.method} {request.url.path} — {response.status_code} ({elapsed:.0f}ms)")
    return response


# ============================================================
# Health & Info
# ============================================================

@app.get("/api/health", response_model=HealthStatus, dependencies=[Depends(verify_api_key)])
def health():
    """Health check — DB connection, table counts, vertical status, uptime."""
    db = get_db()
    try:
        tables_to_check = [
            "citations", "competitor_citations", "serp_ai_overlap",
            "collection_runs", "daily_snapshots", "interventions",
            "finops_usage", "finops_alerts",
        ]
        table_counts: dict[str, int] = {}
        for t in tables_to_check:
            try:
                row = db._conn.execute(f"SELECT COUNT(*) as n FROM {t}").fetchone()
                table_counts[t] = row["n"] if row else 0
            except Exception:
                table_counts[t] = -1

        # Last collection per vertical
        last_coll: dict[str, str | None] = {}
        for slug in list_verticals():
            row = db._conn.execute(
                "SELECT MAX(timestamp) as ts FROM collection_runs WHERE vertical = ? AND status = 'success'",
                (slug,),
            ).fetchone()
            last_coll[slug] = row["ts"] if row and row["ts"] else None

        return HealthStatus(
            status="ok",
            db_ok=True,
            tables=table_counts,
            verticals_active=list_verticals(),
            last_collection=last_coll,
            uptime_seconds=round(time.time() - _start_time, 1),
        )
    except Exception as e:
        return HealthStatus(
            status="degraded",
            db_ok=False,
            tables={},
            verticals_active=[],
            last_collection={},
            uptime_seconds=round(time.time() - _start_time, 1),
        )


@app.get("/api/verticals", response_model=VerticalListResponse, dependencies=[Depends(verify_api_key)])
def get_verticals_list():
    """List all 4 research verticals with entity counts and last collection."""
    db = get_db()
    verticals_out: list[VerticalInfo] = []
    total_entities = 0

    for slug, v in VERTICALS.items():
        cohort = v["cohort"]
        queries = get_queries(slug, include_common=True)
        total_entities += len(cohort)

        # Last collection time
        row = db._conn.execute(
            "SELECT MAX(timestamp) as ts FROM collection_runs WHERE vertical = ? AND status = 'success'",
            (slug,),
        ).fetchone()
        last_ts = None
        if row and row["ts"]:
            try:
                last_ts = datetime.fromisoformat(row["ts"].replace("Z", "+00:00"))
            except Exception:
                last_ts = None

        verticals_out.append(VerticalInfo(
            slug=slug,
            name=v["name"],
            entity_count=len(cohort),
            entities=cohort,
            query_count=len(queries),
            last_collection=last_ts,
        ))

    return VerticalListResponse(verticals=verticals_out, total_entities=total_entities)


@app.get("/api/verticals/{slug}", response_model=VerticalInfo, dependencies=[Depends(verify_api_key)])
def get_vertical_detail(slug: str):
    """Detail of a single vertical."""
    if slug not in VERTICALS:
        raise HTTPException(status_code=404, detail=f"Vertical '{slug}' não encontrada.")

    db = get_db()
    v = VERTICALS[slug]
    cohort = v["cohort"]
    queries = get_queries(slug, include_common=True)

    row = db._conn.execute(
        "SELECT MAX(timestamp) as ts FROM collection_runs WHERE vertical = ? AND status = 'success'",
        (slug,),
    ).fetchone()
    last_ts = None
    if row and row["ts"]:
        try:
            last_ts = datetime.fromisoformat(row["ts"].replace("Z", "+00:00"))
        except Exception:
            last_ts = None

    return VerticalInfo(
        slug=slug,
        name=v["name"],
        entity_count=len(cohort),
        entities=cohort,
        query_count=len(queries),
        last_collection=last_ts,
    )


# ============================================================
# Citations Data
# ============================================================

@app.get("/api/citations", response_model=list[CitationRecord], dependencies=[Depends(verify_api_key)])
def get_citations(
    vertical: str | None = Query(None, description="Filtrar por vertical"),
    days: int = Query(30, ge=1, le=365, description="Período em dias"),
    llm: str | None = Query(None, description="Filtrar por LLM"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
):
    """Paginated citation records with optional filters."""
    db = get_db()
    conditions = ["timestamp >= datetime('now', ?)"]
    params: list[Any] = [f"-{days} days"]

    if vertical:
        conditions.append("vertical = ?")
        params.append(vertical)
    if llm:
        conditions.append("llm = ?")
        params.append(llm)

    where = "WHERE " + " AND ".join(conditions)
    params.extend([limit, offset])

    rows = db._conn.execute(
        f"""SELECT timestamp, llm, query, cited_entity as entity, cited, position,
                   attribution, vertical
            FROM citations {where}
            ORDER BY timestamp DESC
            LIMIT ? OFFSET ?""",
        params,
    ).fetchall()

    return [
        CitationRecord(
            timestamp=r["timestamp"],
            llm=r["llm"],
            query=r["query"],
            entity=r["entity"] if r["entity"] else None,
            cited=bool(r["cited"]),
            position=r["position"],
            attribution=r["attribution"],
            sentiment=None,
            vertical=r["vertical"],
        )
        for r in rows
    ]


@app.get("/api/citations/rates", response_model=CitationMetrics, dependencies=[Depends(verify_api_key)])
def get_citation_rates(
    vertical: str = Query("fintech", description="Vertical de estudo"),
    days: int = Query(30, ge=1, le=365),
):
    """Citation rates aggregated by LLM for a vertical."""
    db = get_db()
    where = "WHERE timestamp >= datetime('now', ?) AND vertical = ?"
    params: list[Any] = [f"-{days} days", vertical]

    rows = db._conn.execute(
        f"""SELECT llm,
                   COUNT(*) as total,
                   SUM(CASE WHEN cited THEN 1 ELSE 0 END) as cited_count,
                   AVG(CASE WHEN cited AND position IS NOT NULL THEN position ELSE NULL END) as avg_pos
            FROM citations {where}
            GROUP BY llm
            ORDER BY cited_count DESC""",
        params,
    ).fetchall()

    rates: list[CitationRateByLLM] = []
    total_obs = 0
    total_cited = 0
    for r in rows:
        total_obs += r["total"]
        total_cited += r["cited_count"]
        rates.append(CitationRateByLLM(
            llm=r["llm"],
            total_queries=r["total"],
            cited_count=r["cited_count"],
            citation_rate=round(r["cited_count"] / max(r["total"], 1), 4),
            avg_position=round(r["avg_pos"], 2) if r["avg_pos"] else None,
        ))

    return CitationMetrics(
        vertical=vertical,
        period_days=days,
        rates_by_llm=rates,
        overall_rate=round(total_cited / max(total_obs, 1), 4),
        total_observations=total_obs,
    )


@app.get("/api/citations/entities", response_model=list[EntityRanking], dependencies=[Depends(verify_api_key)])
def get_entity_rankings(
    vertical: str = Query("fintech"),
    days: int = Query(30, ge=1, le=365),
    top: int = Query(10, ge=1, le=100),
):
    """Rank entities by citation frequency within a vertical."""
    db = get_db()

    rows = db._conn.execute(
        """SELECT cc.entity,
                  SUM(CASE WHEN cc.cited THEN 1 ELSE 0 END) as citation_count,
                  COUNT(*) as total,
                  (SELECT cc2.llm FROM competitor_citations cc2
                   WHERE cc2.entity = cc.entity AND cc2.vertical = ? AND cc2.cited
                   GROUP BY cc2.llm ORDER BY COUNT(*) DESC LIMIT 1) as top_llm
           FROM competitor_citations cc
           WHERE cc.vertical = ? AND cc.timestamp >= datetime('now', ?)
           GROUP BY cc.entity
           ORDER BY citation_count DESC
           LIMIT ?""",
        (vertical, vertical, f"-{days} days", top),
    ).fetchall()

    return [
        EntityRanking(
            entity=r["entity"],
            citation_count=r["citation_count"],
            citation_rate=round(r["citation_count"] / max(r["total"], 1), 4),
            top_llm=r["top_llm"] or "N/A",
        )
        for r in rows
    ]


@app.get("/api/citations/timeseries", response_model=list[TimeSeriesPoint], dependencies=[Depends(verify_api_key)])
def get_citation_timeseries(
    vertical: str = Query("fintech"),
    days: int = Query(90, ge=1, le=365),
):
    """Daily citation rate as time series for charting."""
    db = get_db()

    rows = db._conn.execute(
        """SELECT date(timestamp) as dt,
                  AVG(CASE WHEN cited THEN 1.0 ELSE 0.0 END) as rate,
                  COUNT(*) as n
           FROM citations
           WHERE vertical = ? AND timestamp >= datetime('now', ?)
           GROUP BY dt
           ORDER BY dt ASC""",
        (vertical, f"-{days} days"),
    ).fetchall()

    return [
        TimeSeriesPoint(
            date=r["dt"],
            value=round(r["rate"], 4),
            label=f"n={r['n']}",
        )
        for r in rows
    ]


# ============================================================
# Collections
# ============================================================

@app.get("/api/collections", response_model=list[CollectionRun], dependencies=[Depends(verify_api_key)])
def get_collections(
    vertical: str | None = Query(None),
    limit: int = Query(20, ge=1, le=200),
):
    """Recent collection run history."""
    db = get_db()
    history = db.get_collection_history(module=None, limit=limit, vertical=vertical)
    return [
        CollectionRun(
            id=r.get("id", 0),
            module=r["module"],
            vertical=r.get("vertical", "fintech"),
            status=r.get("status", "success"),
            records_count=r.get("records", 0),
            duration_ms=r.get("duration_ms"),
            timestamp=r["timestamp"],
        )
        for r in history
    ]


@app.get("/api/collections/status", response_model=dict[str, CollectionStatus], dependencies=[Depends(verify_api_key)])
def get_collections_status():
    """Current collection status for all verticals."""
    db = get_db()
    result: dict[str, CollectionStatus] = {}

    for slug in list_verticals():
        # Last run
        last = db._conn.execute(
            "SELECT MAX(timestamp) as ts FROM collection_runs WHERE vertical = ? AND status = 'success'",
            (slug,),
        ).fetchone()
        last_run = None
        if last and last["ts"]:
            try:
                last_run = datetime.fromisoformat(last["ts"].replace("Z", "+00:00"))
            except Exception:
                pass

        # Module status
        modules = db._conn.execute(
            """SELECT module, status FROM collection_runs
               WHERE vertical = ? AND id IN (
                   SELECT MAX(id) FROM collection_runs WHERE vertical = ? GROUP BY module
               )""",
            (slug, slug),
        ).fetchall()
        mod_status = {r["module"]: r["status"] for r in modules}

        # Runs in last 24h
        count_24h = db._conn.execute(
            "SELECT COUNT(*) as n FROM collection_runs WHERE vertical = ? AND timestamp >= datetime('now', '-1 day')",
            (slug,),
        ).fetchone()

        result[slug] = CollectionStatus(
            vertical=slug,
            last_run=last_run,
            modules_status=mod_status,
            total_runs_24h=count_24h["n"] if count_24h else 0,
        )

    return result


@app.post("/api/collections/trigger", response_model=TaskStatus, dependencies=[Depends(verify_api_key)])
def trigger_collection(body: CollectionTriggerRequest, background_tasks: BackgroundTasks):
    """Trigger a background collection for a vertical."""
    if body.vertical not in VERTICALS and body.vertical != "all":
        raise HTTPException(status_code=400, detail=f"Vertical '{body.vertical}' inválida.")

    task_id = str(uuid.uuid4())[:8]
    task = TaskStatus(
        task_id=task_id,
        status="queued",
        vertical=body.vertical,
        started_at=datetime.now(timezone.utc).isoformat(),
    )
    _tasks[task_id] = task

    background_tasks.add_task(_run_collection, task_id, body.vertical, body.modules)
    return task


def _run_collection(task_id: str, vertical: str, modules: list[str]) -> None:
    """Execute collection in background."""
    task = _tasks.get(task_id)
    if not task:
        return
    task.status = "running"
    task.progress_pct = 0.0

    try:
        from src.collectors.citation_tracker import CitationTracker
        from src.collectors.competitor import CompetitorBenchmark
        from src.collectors.serp_overlap import SerpAIOverlap

        db = DatabaseClient()
        db.connect()

        verticals_to_run = list_verticals() if vertical == "all" else [vertical]
        module_map = {
            "citation_tracker": (CitationTracker, db.insert_citations),
            "competitor_benchmark": (CompetitorBenchmark, db.insert_competitor_citations),
            "serp_ai_overlap": (SerpAIOverlap, db.insert_serp_overlap),
        }

        total_steps = len(verticals_to_run) * len(modules)
        completed = 0
        total_records = 0

        for vert in verticals_to_run:
            for mod_name in modules:
                if mod_name not in module_map:
                    continue
                cls, insert_fn = module_map[mod_name]
                start = time.time()
                try:
                    collector = cls(vertical=vert)
                    results = collector.collect()
                    if results:
                        count = insert_fn(results, vertical=vert)
                        duration = int((time.time() - start) * 1000)
                        db.insert_collection_run(mod_name, count, duration, vertical=vert)
                        total_records += count
                    collector.close()
                except Exception as e:
                    duration = int((time.time() - start) * 1000)
                    db.insert_collection_run(mod_name, 0, duration, status="error", error_msg=str(e), vertical=vert)
                    logger.error(f"Coleta falhou: {mod_name}/{vert}: {e}")

                completed += 1
                task.progress_pct = round(completed / max(total_steps, 1) * 100, 1)

        db.close()
        task.status = "completed"
        task.progress_pct = 100.0
        task.completed_at = datetime.now(timezone.utc).isoformat()
        task.result = {"total_records": total_records}
    except Exception as e:
        task.status = "failed"
        task.error = str(e)
        task.completed_at = datetime.now(timezone.utc).isoformat()
        logger.error(f"Task {task_id} falhou: {e}")


@app.get("/api/tasks/{task_id}", response_model=TaskStatus, dependencies=[Depends(verify_api_key)])
def get_task_status(task_id: str):
    """Check the status of a background task."""
    task = _tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task '{task_id}' não encontrada.")
    return task


# ============================================================
# Analysis
# ============================================================

@app.post("/api/analysis/report", response_model=TaskStatus, dependencies=[Depends(verify_api_key)])
def generate_report(body: ReportRequest, background_tasks: BackgroundTasks):
    """Generate a statistical analysis report as a background task."""
    if body.vertical not in VERTICALS:
        raise HTTPException(status_code=400, detail=f"Vertical '{body.vertical}' inválida.")

    task_id = str(uuid.uuid4())[:8]
    task = TaskStatus(
        task_id=task_id,
        status="queued",
        vertical=body.vertical,
        started_at=datetime.now(timezone.utc).isoformat(),
    )
    _tasks[task_id] = task

    background_tasks.add_task(_run_report, task_id, body.vertical, body.days)
    return task


def _run_report(task_id: str, vertical: str, days: int) -> None:
    """Execute statistical report in background."""
    task = _tasks.get(task_id)
    if not task:
        return
    task.status = "running"

    try:
        from src.analysis.statistical import StatisticalAnalyzer

        db = DatabaseClient()
        db.connect()

        rows = db._conn.execute(
            "SELECT * FROM citations WHERE vertical = ? AND timestamp >= datetime('now', ?)",
            (vertical, f"-{days} days"),
        ).fetchall()

        if not rows:
            task.status = "completed"
            task.completed_at = datetime.now(timezone.utc).isoformat()
            task.result = {
                "vertical": vertical,
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "period_days": days,
                "total_observations": 0,
                "key_findings": ["Sem dados de citação para o período selecionado."],
                "statistical_tests": [],
            }
            db.close()
            return

        df = pd.DataFrame([dict(r) for r in rows])
        analyzer = StatisticalAnalyzer()
        report = analyzer.generate_summary_report(df)

        findings: list[str] = []
        findings.append(f"Taxa de citação geral: {report['overall_citation_rate']:.1%}")
        findings.append(f"Total de observações: {report['total_observations']}")

        for llm, data in report.get("by_llm", {}).items():
            findings.append(f"{llm}: {data['rate']:.1%} ({data['cited']}/{data['n']})")

        tests: list[dict] = []
        if "anova_llms" in report:
            tests.append(report["anova_llms"])

        task.status = "completed"
        task.completed_at = datetime.now(timezone.utc).isoformat()
        task.result = {
            "vertical": vertical,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "period_days": days,
            "total_observations": report["total_observations"],
            "key_findings": findings,
            "statistical_tests": tests,
            "by_llm": report.get("by_llm", {}),
            "by_category": report.get("by_category", {}),
        }
        db.close()
    except Exception as e:
        task.status = "failed"
        task.error = str(e)
        task.completed_at = datetime.now(timezone.utc).isoformat()
        logger.error(f"Report task {task_id} falhou: {e}")


@app.get("/api/analysis/compare", dependencies=[Depends(verify_api_key)])
def compare_verticals(
    verticals: str = Query("fintech,varejo", description="Slugs separados por vírgula"),
    days: int = Query(30, ge=1, le=365),
):
    """Cross-vertical comparison of citation rates."""
    db = get_db()
    slugs = [s.strip() for s in verticals.split(",") if s.strip()]

    for s in slugs:
        if s not in VERTICALS:
            raise HTTPException(status_code=400, detail=f"Vertical '{s}' inválida.")

    comparison: dict[str, Any] = {}
    for slug in slugs:
        rows = db._conn.execute(
            """SELECT llm,
                      COUNT(*) as total,
                      SUM(CASE WHEN cited THEN 1 ELSE 0 END) as cited_count
               FROM citations
               WHERE vertical = ? AND timestamp >= datetime('now', ?)
               GROUP BY llm""",
            (slug, f"-{days} days"),
        ).fetchall()

        total = sum(r["total"] for r in rows)
        cited = sum(r["cited_count"] for r in rows)
        comparison[slug] = {
            "name": VERTICALS[slug]["name"],
            "total_observations": total,
            "overall_rate": round(cited / max(total, 1), 4),
            "by_llm": {
                r["llm"]: {
                    "total": r["total"],
                    "cited": r["cited_count"],
                    "rate": round(r["cited_count"] / max(r["total"], 1), 4),
                }
                for r in rows
            },
        }

    return {
        "period_days": days,
        "verticals_compared": slugs,
        "comparison": comparison,
    }


# ============================================================
# FinOps
# ============================================================

@app.get("/api/finops/status", response_model=FinOpsStatus, dependencies=[Depends(verify_api_key)])
def get_finops_status():
    """FinOps budget and spending overview."""
    try:
        from src.finops.tracker import get_tracker

        tracker = get_tracker()
        statuses = tracker.get_status()

        total_monthly = sum(s.monthly_limit for s in statuses)
        total_spent = sum(s.monthly_spend for s in statuses)

        by_platform: dict[str, dict] = {}
        for s in statuses:
            by_platform[s.platform] = {
                "monthly_spend": s.monthly_spend,
                "monthly_limit": s.monthly_limit,
                "monthly_pct": s.monthly_pct,
                "daily_spend": s.daily_spend,
                "daily_limit": s.daily_limit,
                "is_blocked": s.is_blocked,
                "queries_today": s.queries_today,
                "tokens_today": s.tokens_today,
            }

        # Recent alerts
        import sqlite3
        conn = sqlite3.connect(tracker._db_path)
        conn.row_factory = sqlite3.Row
        alerts_rows = conn.execute(
            "SELECT * FROM finops_alerts ORDER BY timestamp DESC LIMIT 10"
        ).fetchall()
        conn.close()

        alerts = [dict(a) for a in alerts_rows]

        return FinOpsStatus(
            budget_monthly=total_monthly,
            spent_monthly=total_spent,
            pct_used=round(total_spent / max(total_monthly, 0.001) * 100, 1),
            by_platform=by_platform,
            alerts=alerts,
        )
    except Exception as e:
        logger.error(f"FinOps status falhou: {e}")
        return FinOpsStatus(
            budget_monthly=0,
            spent_monthly=0,
            pct_used=0,
            by_platform={},
            alerts=[{"error": str(e)}],
        )


@app.get("/api/finops/dashboard", response_class=HTMLResponse, dependencies=[Depends(verify_api_key)])
def get_finops_dashboard():
    """Serve the FinOps HTML dashboard."""
    dashboard_path = Path(__file__).resolve().parent.parent.parent / "output" / "finops_dashboard.html"
    if not dashboard_path.exists():
        # Try to generate it
        try:
            from src.finops.monitor import generate_dashboard
            from src.finops.tracker import get_tracker
            dashboard_path = generate_dashboard(get_tracker())
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Dashboard não encontrado e falhou ao gerar: {e}")

    return HTMLResponse(content=dashboard_path.read_text(encoding="utf-8"))


# ============================================================
# Export
# ============================================================

@app.get("/api/export/csv", dependencies=[Depends(verify_api_key)])
def export_csv(
    vertical: str = Query("fintech"),
):
    """Export citation data as CSV download."""
    db = get_db()
    if vertical not in VERTICALS:
        raise HTTPException(status_code=400, detail=f"Vertical '{vertical}' inválida.")

    rows = db._conn.execute(
        "SELECT * FROM citations WHERE vertical = ? ORDER BY timestamp",
        (vertical,),
    ).fetchall()

    if not rows:
        raise HTTPException(status_code=404, detail=f"Sem dados de citação para '{vertical}'.")

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=rows[0].keys())
    writer.writeheader()
    for row in rows:
        writer.writerow(dict(row))

    output.seek(0)
    filename = f"citations_{vertical}_{datetime.now(timezone.utc).strftime('%Y%m%d')}.csv"

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


# ============================================================
# Root
# ============================================================

@app.get("/")
def root():
    """API root — redirect to docs."""
    return {
        "name": "GEO Research API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health",
    }
