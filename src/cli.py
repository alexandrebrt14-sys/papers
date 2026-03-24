"""Papers CLI — Command-line interface for GEO research data collection."""

from __future__ import annotations

import json
import logging
import time
from datetime import datetime, timezone

import click
from rich.console import Console
from rich.table import Table

from src.config import config
from src.db.client import DatabaseClient
from src.collectors.citation_tracker import CitationTracker
from src.collectors.competitor import CompetitorBenchmark
from src.collectors.serp_overlap import SerpAIOverlap
from src.collectors.intervention import InterventionTracker
from src.persistence.timeseries import TimeSeriesManager

console = Console()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
)


def get_db() -> DatabaseClient:
    db = DatabaseClient()
    db.connect()
    return db


@click.group()
def main() -> None:
    """Papers — Infraestrutura de pesquisa empírica em GEO."""
    pass


# === Collect Commands ===

@main.group()
def collect() -> None:
    """Executar módulos de coleta de dados."""
    pass


@collect.command("all")
def collect_all() -> None:
    """Rodar todos os coletores disponíveis."""
    db = get_db()
    modules = [
        ("citation_tracker", CitationTracker, db.insert_citations),
        ("competitor_benchmark", CompetitorBenchmark, db.insert_competitor_citations),
        ("serp_ai_overlap", SerpAIOverlap, db.insert_serp_overlap),
    ]

    for name, cls, insert_fn in modules:
        console.print(f"\n[bold cyan]Coletando: {name}[/bold cyan]")
        start = time.time()
        try:
            collector = cls()
            results = collector.collect()
            if results:
                count = insert_fn(results)
                duration = int((time.time() - start) * 1000)
                db.insert_collection_run(name, count, duration)
                console.print(f"  [green]{count} registros salvos ({duration}ms)[/green]")
            else:
                console.print(f"  [yellow]Nenhum registro coletado[/yellow]")
            collector.close()
        except Exception as e:
            duration = int((time.time() - start) * 1000)
            db.insert_collection_run(name, 0, duration, "error", str(e))
            console.print(f"  [red]Erro: {e}[/red]")

    # Save daily snapshot
    ts = TimeSeriesManager(db)
    snapshot = ts.compute_daily_citation_aggregate()
    ts.save_daily_aggregate("citation_tracker", snapshot)
    console.print(f"\n[bold green]Coleta concluída. Snapshot diário salvo.[/bold green]")
    db.close()


@collect.command("citation")
def collect_citation() -> None:
    """Rodar apenas o Citation Tracker (Módulo 1)."""
    db = get_db()
    start = time.time()
    collector = CitationTracker()
    results = collector.collect()
    if results:
        count = db.insert_citations(results)
        duration = int((time.time() - start) * 1000)
        db.insert_collection_run("citation_tracker", count, duration)
        console.print(f"[green]{count} citações coletadas ({duration}ms)[/green]")
    collector.close()
    db.close()


@collect.command("competitor")
def collect_competitor() -> None:
    """Rodar apenas o Competitor Benchmark (Módulo 2)."""
    db = get_db()
    start = time.time()
    collector = CompetitorBenchmark()
    results = collector.collect()
    if results:
        count = db.insert_competitor_citations(results)
        duration = int((time.time() - start) * 1000)
        db.insert_collection_run("competitor_benchmark", count, duration)
        console.print(f"[green]{count} registros de benchmark coletados ({duration}ms)[/green]")
    collector.close()
    db.close()


@collect.command("serp")
def collect_serp() -> None:
    """Rodar apenas o SERP vs AI Overlap (Módulo 3)."""
    db = get_db()
    start = time.time()
    collector = SerpAIOverlap()
    results = collector.collect()
    if results:
        count = db.insert_serp_overlap(results)
        duration = int((time.time() - start) * 1000)
        db.insert_collection_run("serp_ai_overlap", count, duration)
        console.print(f"[green]{count} registros de overlap coletados ({duration}ms)[/green]")
    collector.close()
    db.close()


# === Analysis Commands ===

@main.group()
def analyze() -> None:
    """Executar análises estatísticas."""
    pass


@analyze.command("report")
def analyze_report() -> None:
    """Gerar relatório estatístico completo."""
    db = get_db()
    import pandas as pd
    from src.analysis.statistical import StatisticalAnalyzer

    rows = db._conn.execute("SELECT * FROM citations").fetchall()
    if not rows:
        console.print("[yellow]Sem dados de citação para análise.[/yellow]")
        return

    df = pd.DataFrame([dict(r) for r in rows])
    analyzer = StatisticalAnalyzer()
    report = analyzer.generate_summary_report(df)

    console.print("\n[bold]Relatório Estatístico — GEO Papers[/bold]\n")
    console.print(f"Total de observações: {report['total_observations']}")
    console.print(f"Taxa de citação geral: {report['overall_citation_rate']:.1%}\n")

    table = Table(title="Taxa de Citação por LLM")
    table.add_column("LLM", style="cyan")
    table.add_column("Taxa", justify="right")
    table.add_column("Citações", justify="right")
    table.add_column("N", justify="right")
    for llm, data in report["by_llm"].items():
        table.add_row(llm, f"{data['rate']:.1%}", str(data["cited"]), str(data["n"]))
    console.print(table)

    if "anova_llms" in report:
        anova = report["anova_llms"]
        console.print(f"\n[bold]ANOVA entre LLMs:[/bold] {anova['interpretation']}")

    db.close()


# === Database Commands ===

@main.group()
def db_cmd() -> None:
    """Gerenciar banco de dados."""
    pass


@db_cmd.command("migrate")
@click.pass_context
def db_migrate(ctx: click.Context) -> None:
    """Aplicar schema ao banco de dados."""
    db = get_db()
    console.print(f"[green]Schema aplicado: {db.db_path}[/green]")
    db.close()


@db_cmd.command("export")
@click.option("--format", "fmt", type=click.Choice(["csv", "json"]), default="csv")
@click.option("--output", "-o", default="data/export")
def db_export(fmt: str, output: str) -> None:
    """Exportar dados de citação."""
    db = get_db()
    if fmt == "csv":
        path = f"{output}_citations.csv"
        count = db.export_citations_csv(path)
        console.print(f"[green]{count} registros exportados para {path}[/green]")
    db.close()


@db_cmd.command("health")
def db_health() -> None:
    """Verificar saúde e completude dos dados."""
    db = get_db()
    ts = TimeSeriesManager(db)
    health = ts.get_data_health()
    console.print(json.dumps(health, indent=2, ensure_ascii=False))
    db.close()


# === Intervention Commands ===

@main.group()
def intervention() -> None:
    """Gerenciar intervenções de conteúdo (A/B)."""
    pass


@intervention.command("add")
@click.argument("slug")
@click.option("--type", "itype", required=True, help="Tipo: schema_org, llms_txt, etc.")
@click.option("--desc", required=True, help="Descrição da intervenção")
@click.option("--url", required=True, help="URL do conteúdo modificado")
def intervention_add(slug: str, itype: str, desc: str, url: str) -> None:
    """Registrar nova intervenção de conteúdo."""
    record = InterventionTracker.create_intervention(
        slug=slug,
        intervention_type=itype,
        description=desc,
        url=url,
        queries=[q["query"] for q in config.llms[:5]],  # Default queries
    )
    console.print(f"[green]Intervenção registrada: {slug} ({itype})[/green]")
    console.print(json.dumps(record, indent=2, ensure_ascii=False))


# Alias 'db' to 'db_cmd'
main.add_command(db_cmd, "db")


# ============================================================
# FinOps commands
# ============================================================

@main.group("finops")
def finops_cmd() -> None:
    """FinOps — governança de custos de APIs."""
    pass


@finops_cmd.command("status")
def finops_status() -> None:
    """Mostra status de gastos e budgets por plataforma."""
    from src.finops.tracker import get_tracker

    tracker = get_tracker()
    statuses = tracker.get_status()

    table = Table(title="FinOps — Status de Gastos")
    table.add_column("Plataforma", style="bold")
    table.add_column("Mensal", justify="right")
    table.add_column("Limite", justify="right")
    table.add_column("% Mensal", justify="right")
    table.add_column("Diário", justify="right")
    table.add_column("% Diário", justify="right")
    table.add_column("Status")
    table.add_column("Queries Hoje", justify="right")

    for s in statuses:
        pct_color = "red" if s.monthly_pct > 90 else "yellow" if s.monthly_pct > 70 else "green"
        status_str = "[red]BLOQUEADO[/red]" if s.is_blocked else "[green]OK[/green]"
        table.add_row(
            s.platform,
            f"${s.monthly_spend:.4f}",
            f"${s.monthly_limit:.2f}",
            f"[{pct_color}]{s.monthly_pct:.1f}%[/{pct_color}]",
            f"${s.daily_spend:.4f}",
            f"{s.daily_pct:.1f}%",
            status_str,
            str(s.queries_today),
        )

    console.print(table)


@finops_cmd.command("set-budget")
@click.argument("platform")
@click.option("--monthly", type=float, help="Limite mensal em USD")
@click.option("--daily", type=float, help="Limite diário em USD")
def finops_set_budget(platform: str, monthly: float | None, daily: float | None) -> None:
    """Atualiza limites de budget para uma plataforma."""
    from src.finops.tracker import get_tracker

    tracker = get_tracker()
    tracker.set_budget(platform, monthly=monthly, daily=daily)
    console.print(f"[green]Budget atualizado: {platform}[/green]")
    if monthly:
        console.print(f"  Mensal: ${monthly:.2f}")
    if daily:
        console.print(f"  Diário: ${daily:.2f}")


@finops_cmd.command("alerts")
@click.option("--limit", default=20, help="Número de alertas")
def finops_alerts(limit: int) -> None:
    """Lista alertas recentes."""
    from src.finops.tracker import get_tracker
    import sqlite3

    tracker = get_tracker()
    conn = sqlite3.connect(tracker._db_path)
    conn.row_factory = sqlite3.Row
    alerts = conn.execute(
        "SELECT * FROM finops_alerts ORDER BY timestamp DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()

    if not alerts:
        console.print("[dim]Nenhum alerta registrado.[/dim]")
        return

    table = Table(title="FinOps — Alertas Recentes")
    table.add_column("Data")
    table.add_column("Plataforma")
    table.add_column("Tipo")
    table.add_column("Severidade")
    table.add_column("Mensagem", max_width=50)
    table.add_column("Email")

    for a in alerts:
        sev_color = {"emergency": "red", "critical": "red", "warning": "yellow", "info": "blue"}.get(a["severity"], "white")
        table.add_row(
            a["timestamp"][:16],
            a["platform"],
            a["alert_type"],
            f"[{sev_color}]{a['severity']}[/{sev_color}]",
            a["message"][:50],
            "Sim" if a["sent_email"] else "Nao",
        )

    console.print(table)


@finops_cmd.command("rollup")
def finops_rollup() -> None:
    """Computa rollup diário para análise histórica."""
    from src.finops.tracker import get_tracker

    tracker = get_tracker()
    tracker.rollup_daily()
    console.print("[green]Rollup diário computado.[/green]")


if __name__ == "__main__":
    main()
