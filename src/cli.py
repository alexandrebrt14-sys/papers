"""Papers CLI — Command-line interface for GEO research data collection."""

from __future__ import annotations

import json
import logging
import time
from datetime import datetime, timezone

import click
from rich.console import Console
from rich.table import Table

from src.config import config, list_verticals, get_queries, get_cohort, VERTICALS
from src.db.client import DatabaseClient
from src.collectors.citation_tracker import CitationTracker
from src.collectors.competitor import CompetitorBenchmark
from src.collectors.serp_overlap import SerpAIOverlap
from src.collectors.context_analyzer import CitationContextAnalyzer
from src.collectors.intervention import InterventionTracker
from src.persistence.timeseries import TimeSeriesManager

console = Console()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
)

VERTICAL_CHOICES = list_verticals() + ["all"]


def get_db() -> DatabaseClient:
    db = DatabaseClient()
    db.connect()
    return db


def resolve_verticals(ctx: click.Context) -> list[str]:
    """Resolve which verticals to process from click context."""
    vertical = ctx.obj.get("vertical", "fintech") if ctx.obj else "fintech"
    if vertical == "all":
        return list_verticals()
    return [vertical]


@click.group()
@click.option(
    "--vertical", "-v",
    type=click.Choice(VERTICAL_CHOICES, case_sensitive=False),
    default="fintech",
    envvar="VERTICAL",
    help="Vertical de estudo: fintech, varejo, saude, tecnologia, all.",
)
@click.pass_context
def main(ctx: click.Context, vertical: str) -> None:
    """Papers — Infraestrutura de pesquisa empírica em GEO."""
    ctx.ensure_object(dict)
    ctx.obj["vertical"] = vertical


# === Collect Commands ===

@main.group()
@click.pass_context
def collect(ctx: click.Context) -> None:
    """Executar módulos de coleta de dados."""
    pass


@collect.command("all")
@click.pass_context
def collect_all(ctx: click.Context) -> None:
    """Rodar todos os coletores disponíveis."""
    db = get_db()
    verticals = resolve_verticals(ctx)

    for vert in verticals:
        console.print(f"\n[bold magenta]--- Vertical: {VERTICALS[vert]['name']} ({vert}) ---[/bold magenta]")
        modules = [
            ("citation_tracker", CitationTracker, db.insert_citations),
            ("competitor_benchmark", CompetitorBenchmark, db.insert_competitor_citations),
            ("serp_ai_overlap", SerpAIOverlap, db.insert_serp_overlap),
        ]

        for name, cls, insert_fn in modules:
            console.print(f"\n[bold cyan]Coletando: {name}[/bold cyan]")
            start = time.time()
            try:
                collector = cls(vertical=vert)
                results = collector.collect()
                if results:
                    count = insert_fn(results, vertical=vert)
                    duration = int((time.time() - start) * 1000)
                    db.insert_collection_run(name, count, duration, vertical=vert)
                    console.print(f"  [green]{count} registros salvos ({duration}ms)[/green]")
                else:
                    console.print(f"  [yellow]Nenhum registro coletado[/yellow]")
                collector.close()
            except Exception as e:
                duration = int((time.time() - start) * 1000)
                db.insert_collection_run(name, 0, duration, status="error", error_msg=str(e), vertical=vert)
                console.print(f"  [red]Erro: {e}[/red]")

        # Run context analyzer on citations just collected
        console.print(f"\n[bold cyan]Analisando contexto das citações...[/bold cyan]")
        try:
            analyzer = CitationContextAnalyzer()
            ctx_rows = db._conn.execute(
                "SELECT id, query, response_text FROM citations "
                "WHERE vertical = ? AND response_text IS NOT NULL "
                "ORDER BY id DESC LIMIT 200",
                (vert,),
            ).fetchall()
            ctx_count = 0
            cohort = get_cohort(vert)
            for row in ctx_rows:
                # Skip if already analyzed
                existing = db._conn.execute(
                    "SELECT 1 FROM citation_context WHERE citation_id = ?", (row["id"],)
                ).fetchone()
                if existing:
                    continue
                for entity in cohort:
                    result = analyzer.analyze(entity, row["response_text"])
                    if result["cited"]:
                        db.insert_citation_context(row["id"], result)
                        ctx_count += 1
            console.print(f"  [green]{ctx_count} registros de contexto salvos[/green]")
        except Exception as e:
            console.print(f"  [yellow]Context analyzer: {e}[/yellow]")

        # Save daily snapshot per vertical
        ts = TimeSeriesManager(db)
        snapshot = ts.compute_daily_citation_aggregate(vertical=vert)
        ts.save_daily_aggregate("citation_tracker", snapshot, vertical=vert)

    db.close()

    # Auto-run FinOps monitor (rollup, budget check, exports, dashboard)
    console.print(f"\n[bold cyan]FinOps monitor...[/bold cyan]")
    from src.finops.hooks import post_collection_hook
    post_collection_hook("collect_all", sum(1 for _ in []), 0)
    console.print(f"[bold green]Coleta + FinOps concluídos.[/bold green]")


@collect.command("citation")
@click.pass_context
def collect_citation(ctx: click.Context) -> None:
    """Rodar apenas o Citation Tracker (Módulo 1).

    Fail-loud: se ZERO citacoes forem coletadas em todas as verticais,
    o comando sai com exit code 1 para que o GitHub Actions falhe.
    Isso previne o bug silencioso onde keys 401 fazem o run aparecer
    como "success" sem dados gravados (incidente 2026-04-07).
    """
    db = get_db()
    verticals = resolve_verticals(ctx)
    total_collected = 0
    total_attempted = 0
    run_start_ts = datetime.now(timezone.utc).isoformat()

    for vert in verticals:
        console.print(f"\n[bold magenta]Vertical: {vert}[/bold magenta]")
        start = time.time()
        collector = CitationTracker(vertical=vert)
        results = collector.collect()
        duration = int((time.time() - start) * 1000)
        count = 0
        if results:
            count = db.insert_citations(results, vertical=vert)
            console.print(f"[green]{count} citações coletadas ({duration}ms)[/green]")
        else:
            console.print(f"[yellow]Nenhuma resposta valida para {vert}[/yellow]")
        # Registra collection_run SEMPRE (inclusive com 0 resultados) para
        # diagnostico historico de quais verticais falharam em cada dia.
        db.insert_collection_run(
            "citation_tracker", count, duration,
            vertical=vert, status="success" if count > 0 else "empty",
        )
        total_collected += count
        # Tentamos ao menos a vertical (mesmo que retornem 0)
        total_attempted += 1
        collector.close()

    db.close()
    # Auto FinOps
    from src.finops.hooks import post_collection_hook
    post_collection_hook("citation_tracker", 0, 0)

    # FAIL-LOUD: se nenhuma vertical retornou dados, falha o comando
    if total_attempted > 0 and total_collected == 0:
        console.print(
            f"\n[bold red]FAIL-LOUD: 0 citacoes em {total_attempted} verticais. "
            f"Provavel causa: API keys invalidas/expiradas no GitHub Secrets, "
            f"rate limiting, ou erro de configuracao. Verifique os logs acima.[/bold red]"
        )
        raise SystemExit(1)

    # FAIL-LOUD per-LLM: garante que cada provider em MANDATORY_LLMS
    # produziu linhas nesta execução. Detecta bugs silenciosos (ex: Groq
    # sem roteamento no _dispatch, incidente 2026-04-07→2026-04-22) que
    # o fail-loud global não pega quando outros providers compensam.
    from src.config import mandatory_llms
    required = mandatory_llms()
    db2 = get_db()
    seen_rows = db2._conn.execute(
        "SELECT DISTINCT llm FROM citations WHERE timestamp >= ?",
        (run_start_ts,),
    ).fetchall()
    db2.close()
    seen = {r[0] for r in seen_rows}
    missing = required - seen
    if missing:
        console.print(
            f"\n[bold red]FAIL-LOUD LLM: providers obrigatorios sem dados neste run: "
            f"{sorted(missing)}. Verifique API keys, roteamento em llm_client._dispatch, "
            f"e circuit breaker. MANDATORY_LLMS={sorted(required)}.[/bold red]"
        )
        raise SystemExit(2)


@collect.command("competitor")
@click.pass_context
def collect_competitor(ctx: click.Context) -> None:
    """Rodar apenas o Competitor Benchmark (Módulo 2)."""
    db = get_db()
    verticals = resolve_verticals(ctx)

    for vert in verticals:
        console.print(f"\n[bold magenta]Vertical: {vert}[/bold magenta]")
        start = time.time()
        collector = CompetitorBenchmark(vertical=vert)
        results = collector.collect()
        count = 0
        if results:
            count = db.insert_competitor_citations(results, vertical=vert)
            duration = int((time.time() - start) * 1000)
            db.insert_collection_run("competitor_benchmark", count, duration, vertical=vert)
            console.print(f"[green]{count} registros de benchmark coletados ({duration}ms)[/green]")
        collector.close()

    db.close()
    from src.finops.hooks import post_collection_hook
    post_collection_hook("competitor_benchmark", 0, 0)


@collect.command("context")
@click.option("--limit", type=int, default=500, show_default=True,
              help="Máx. citações sem contexto a processar por vertical")
@click.pass_context
def collect_context(ctx: click.Context, limit: int) -> None:
    """Rodar Context Analyzer (Módulo 7) em citations sem contexto.

    Bug fix 2026-04-23: antes só o comando `collect all` chamava o analyzer,
    mas o workflow diário usa `collect citation` + `collect competitor`. Isso
    deixou citation_context vazio em varejo/saude/tecnologia desde início de
    abril (bug reportado em PAPERS-DEEP-ANALYTICS-2026-04-16 §2.5).

    Este comando standalone processa TODAS as verticais, respeitando --limit.
    """
    db = get_db()
    verticals = resolve_verticals(ctx)
    analyzer = CitationContextAnalyzer()
    total = 0

    for vert in verticals:
        console.print(f"\n[bold magenta]Vertical: {vert}[/bold magenta]")
        rows = db._conn.execute(
            "SELECT c.id, c.query, c.response_text FROM citations c "
            "LEFT JOIN citation_context cc ON cc.citation_id = c.id "
            "WHERE c.vertical = ? AND c.response_text IS NOT NULL "
            "AND c.cited = 1 AND cc.citation_id IS NULL "
            "ORDER BY c.id DESC LIMIT ?",
            (vert, limit),
        ).fetchall()
        cohort = get_cohort(vert)
        vert_count = 0
        for row in rows:
            for entity in cohort:
                result = analyzer.analyze(entity, row["response_text"])
                if result["cited"]:
                    db.insert_citation_context(row["id"], result)
                    vert_count += 1
        total += vert_count
        console.print(f"  [green]{vert_count} contextos gravados (de {len(rows)} citations pendentes)[/green]")

    db.close()
    console.print(f"\n[bold green]Context Analyzer: {total} registros em {len(verticals)} verticais.[/bold green]")


@collect.command("serp")
@click.pass_context
def collect_serp(ctx: click.Context) -> None:
    """Rodar apenas o SERP vs AI Overlap (Módulo 3)."""
    db = get_db()
    verticals = resolve_verticals(ctx)

    for vert in verticals:
        console.print(f"\n[bold magenta]Vertical: {vert}[/bold magenta]")
        start = time.time()
        collector = SerpAIOverlap(vertical=vert)
        results = collector.collect()
        count = 0
        if results:
            count = db.insert_serp_overlap(results, vertical=vert)
            duration = int((time.time() - start) * 1000)
            db.insert_collection_run("serp_ai_overlap", count, duration, vertical=vert)
            console.print(f"[green]{count} registros de overlap coletados ({duration}ms)[/green]")
        collector.close()

    db.close()
    from src.finops.hooks import post_collection_hook
    post_collection_hook("serp_ai_overlap", 0, 0)


# === Analysis Commands ===

@main.group()
@click.pass_context
def analyze(ctx: click.Context) -> None:
    """Executar análises estatísticas."""
    pass


@analyze.command("report")
@click.pass_context
def analyze_report(ctx: click.Context) -> None:
    """Gerar relatório estatístico completo."""
    db = get_db()
    import pandas as pd
    from src.analysis.statistical import StatisticalAnalyzer

    verticals = resolve_verticals(ctx)

    for vert in verticals:
        console.print(f"\n[bold magenta]--- Relatório: {vert} ---[/bold magenta]")
        where = "WHERE vertical = ?" if vert != "all" else ""
        params = [vert] if vert != "all" else []
        rows = db._conn.execute(f"SELECT * FROM citations {where}", params).fetchall()
        if not rows:
            console.print("[yellow]Sem dados de citação para análise.[/yellow]")
            continue

        df = pd.DataFrame([dict(r) for r in rows])
        analyzer = StatisticalAnalyzer()
        report = analyzer.generate_summary_report(df)

        console.print(f"\n[bold]Relatório Estatístico — GEO Papers ({vert})[/bold]\n")
        console.print(f"Total de observações: {report['total_observations']}")
        console.print(f"Taxa de citação geral: {report['overall_citation_rate']:.1%}\n")

        table = Table(title=f"Taxa de Citação por LLM ({vert})")
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


@analyze.command("visualize")
@click.option("--output-dir", "-o", default="output", help="Diretório de saída para gráficos.")
@click.pass_context
def analyze_visualize(ctx: click.Context, output_dir: str) -> None:
    """Gerar gráficos de publicação (5 visualizações)."""
    from pathlib import Path
    from src.analysis.visualization import (
        plot_citation_rate_by_llm,
        plot_citation_trend,
        plot_serp_ai_overlap,
        plot_competitor_comparison,
        plot_intervention_impact,
        OUTPUT_DIR,
    )
    import pandas as pd

    # Override output dir if specified
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    import src.analysis.visualization as viz
    viz.OUTPUT_DIR = out

    db = get_db()
    verticals = resolve_verticals(ctx)
    generated = []

    for vert in verticals:
        console.print(f"\n[bold magenta]--- Visualizações: {vert} ---[/bold magenta]")

        where = "WHERE vertical = ?"
        params = [vert]

        # 1. Citation rate by LLM
        rows = db._conn.execute(f"SELECT * FROM citations {where}", params).fetchall()
        if rows:
            df = pd.DataFrame([dict(r) for r in rows])
            path = plot_citation_rate_by_llm(df, output=f"citation_rate_by_llm_{vert}.png")
            generated.append(path)
            console.print(f"  [green]1/5 Taxa de citação por LLM: {path}[/green]")

            # 2. Citation trend
            path = plot_citation_trend(df, output=f"citation_trend_{vert}.png")
            generated.append(path)
            console.print(f"  [green]2/5 Tendência de citação: {path}[/green]")
        else:
            console.print(f"  [yellow]1-2/5 Sem dados de citação para {vert}[/yellow]")

        # 3. SERP vs AI overlap
        serp_rows = db._conn.execute(
            f"SELECT * FROM serp_ai_overlap {where}", params
        ).fetchall()
        if serp_rows:
            df_serp = pd.DataFrame([dict(r) for r in serp_rows])
            path = plot_serp_ai_overlap(df_serp, output=f"serp_ai_overlap_{vert}.png")
            generated.append(path)
            console.print(f"  [green]3/5 Sobreposição SERP-IA: {path}[/green]")
        else:
            console.print(f"  [yellow]3/5 Sem dados de overlap SERP para {vert}[/yellow]")

        # 4. Competitor comparison
        comp_rows = db._conn.execute(
            f"SELECT * FROM competitor_citations {where}", params
        ).fetchall()
        if comp_rows:
            df_comp = pd.DataFrame([dict(r) for r in comp_rows])
            path = plot_competitor_comparison(df_comp, output=f"competitor_comparison_{vert}.png")
            generated.append(path)
            console.print(f"  [green]4/5 Comparativo de competidores: {path}[/green]")
        else:
            console.print(f"  [yellow]4/5 Sem dados de benchmark para {vert}[/yellow]")

        # 5. Intervention impact
        interventions = db._conn.execute(
            "SELECT * FROM interventions WHERE status IN ('active', 'completed')"
        ).fetchall()
        if interventions:
            for intv in interventions:
                measurements = db.get_intervention_measurements(intv["slug"])
                if measurements:
                    baseline = json.loads(intv["baseline_json"]) if intv["baseline_json"] else {}
                    baseline_rate = sum(baseline.values()) / max(len(baseline), 1) if baseline else 0.0
                    path = plot_intervention_impact(
                        measurements, baseline_rate,
                        output=f"intervention_impact_{intv['slug']}.png",
                    )
                    generated.append(path)
                    console.print(f"  [green]5/5 Impacto intervenção '{intv['slug']}': {path}[/green]")
        else:
            console.print(f"  [yellow]5/5 Sem intervenções registradas[/yellow]")

    db.close()
    console.print(f"\n[bold green]{len(generated)} gráficos gerados em {out}[/bold green]")


# === Database Commands ===

@main.group()
@click.pass_context
def db_cmd(ctx: click.Context) -> None:
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
@click.pass_context
def db_export(ctx: click.Context, fmt: str, output: str) -> None:
    """Exportar dados de citação."""
    db = get_db()
    verticals = resolve_verticals(ctx)
    for vert in verticals:
        if fmt == "csv":
            path = f"{output}_{vert}_citations.csv"
            count = db.export_citations_csv(path, vertical=vert)
            console.print(f"[green]{count} registros exportados para {path} ({vert})[/green]")
    db.close()


@db_cmd.command("health")
@click.pass_context
def db_health(ctx: click.Context) -> None:
    """Verificar saúde e completude dos dados."""
    db = get_db()
    ts = TimeSeriesManager(db)
    health = ts.get_data_health()
    console.print(json.dumps(health, indent=2, ensure_ascii=False))
    db.close()


# === Intervention Commands ===

@main.group()
@click.pass_context
def intervention(ctx: click.Context) -> None:
    """Gerenciar intervenções de conteúdo (A/B)."""
    pass


@intervention.command("add")
@click.argument("slug")
@click.option("--type", "itype", required=True, help="Tipo: schema_org, llms_txt, etc.")
@click.option("--desc", required=True, help="Descrição da intervenção")
@click.option("--url", required=True, help="URL do conteúdo modificado")
def intervention_add(slug: str, itype: str, desc: str, url: str) -> None:
    """Registrar nova intervenção de conteúdo."""
    db = get_db()
    record = InterventionTracker.create_intervention(
        slug=slug,
        intervention_type=itype,
        description=desc,
        url=url,
        queries=[q["query"] for q in get_queries("fintech")[:5]],
    )
    db.insert_intervention(record)
    db.close()
    console.print(f"[green]Intervenção registrada e salva: {slug} ({itype})[/green]")
    console.print(json.dumps(record, indent=2, ensure_ascii=False))


@intervention.command("check")
def intervention_check() -> None:
    """Verificar intervenções ativas e registrar medições (dia +7, +14, +30)."""
    db = get_db()
    results = InterventionTracker.check_active_interventions(db)
    if results:
        console.print(f"[green]{len(results)} medições registradas.[/green]")
        for m in results:
            console.print(
                f"  {m['intervention_slug']} dia +{m['days_since_intervention']}: "
                f"taxa={m['citation_rate']:.1%}"
            )
    else:
        console.print("[yellow]Nenhuma medição pendente (ou sem intervenções ativas).[/yellow]")
    db.close()


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


@finops_cmd.command("monitor")
def finops_monitor_cmd() -> None:
    """Executa ciclo completo de monitoramento FinOps.

    Roda automaticamente após cada coleta, mas pode ser chamado manualmente.
    Inclui: rollup, budget checks, anomaly detection, exports, dashboard.
    """
    from src.finops.monitor import run_monitor
    run_monitor(verbose=True)


@finops_cmd.command("security")
def finops_security_cmd() -> None:
    """Auditoria de segurança: valida chaves, scan de vazamentos, rotação."""
    from src.finops.secrets import run_security_audit
    run_security_audit()


@finops_cmd.command("dashboard")
def finops_dashboard_cmd() -> None:
    """Gera dashboard HTML com estado atual."""
    from src.finops.tracker import get_tracker
    from src.finops.monitor import generate_dashboard
    path = generate_dashboard(get_tracker())
    console.print(f"[green]Dashboard gerado: {path}[/green]")


# ============================================================
# Sync Supabase
# ============================================================

@main.command("sync")
@click.option(
    "--dry-run",
    is_flag=True,
    help="Agrega e exibe dados sem enviar ao Supabase.",
)
@click.option(
    "--db",
    "db_path",
    default=None,
    metavar="PATH",
    help="Caminho para o banco SQLite (padrão: PAPERS_DB_PATH ou data/papers.db).",
)
@click.option(
    "--quiet", "-q",
    is_flag=True,
    help="Suprime output informativo (apenas erros).",
)
@click.pass_context
def sync_cmd(ctx: click.Context, dry_run: bool, db_path: str | None, quiet: bool) -> None:
    """Sincroniza dados agregados do SQLite para o Supabase.

    Faz upsert das tabelas papers_dashboard_data e papers_finops
    com dados agregados dos últimos 30/90 dias por vertical.

    Exemplo:
        python -m src.cli sync --dry-run
        python -m src.cli --vertical fintech sync
    """
    from scripts.sync_to_supabase import run_sync

    vertical = ctx.obj.get("vertical", "fintech") if ctx.obj else "fintech"
    verticals_to_sync = list_verticals() if vertical == "all" else [vertical]

    exit_code = run_sync(
        db_path=db_path,
        verticals=verticals_to_sync,
        dry_run=dry_run,
        verbose=not quiet,
    )

    if exit_code == 1:
        raise SystemExit(1)
    # exit_code == 2 significa credenciais ausentes (skip silencioso no CI)


# ============================================================
# API Server
# ============================================================

@main.command("serve")
@click.option("--host", default="0.0.0.0", help="Host para bind do servidor.")
@click.option("--port", default=8000, type=int, help="Porta do servidor.")
@click.option("--reload", "do_reload", is_flag=True, help="Hot-reload para desenvolvimento.")
def serve(host: str, port: int, do_reload: bool) -> None:
    """Inicia o servidor API REST."""
    import uvicorn
    console.print(f"[bold green]Iniciando API em {host}:{port}...[/bold green]")
    uvicorn.run("src.api.main:app", host=host, port=port, reload=do_reload)


if __name__ == "__main__":
    main()
