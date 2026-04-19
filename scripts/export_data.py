"""export_data.py — consolidador de exports (Onda 4 — Refactor 2026-04-19).

Substitui os 3 scripts duplicados que existiam em `data/`:
    - data/extract_dashboard.py     (text dump)
    - data/extract_json_dashboard.py (JSON)
    - data/create_html_dashboard.py  (HTML)

Agora uma ferramenta única com --format, evitando divergência entre cópias.

Uso:
    python scripts/export_data.py --format text              # relatório no stdout
    python scripts/export_data.py --format json              # salva data/dashboard_data.json
    python scripts/export_data.py --format csv --vertical fintech
    python scripts/export_data.py --format html              # data/dashboard.html
    python scripts/export_data.py --format json --output custom.json

A lógica de extração é compartilhada entre todos os formats (função
`extract_dashboard_data`), garantindo que text/json/html/csv enxerguem
EXATAMENTE os mesmos números.

Não confundir com `scripts/generate_dashboard_json.py`, que tem propósito
distinto: gera um JSON específico para o frontend em alexandrecaramaschi.com/
research (com metadata de cores dos LLMs e verticais, schema fechado, consumido
via ISR). Este export_data.py é ferramenta genérica de análise — saída
paramétrica por --format. Use o export_data para análises ad-hoc e o
generate_dashboard_json para a publicação web.
"""

from __future__ import annotations

import argparse
import csv
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB = REPO_ROOT / "data" / "papers.db"
DEFAULT_OUT_DIR = REPO_ROOT / "data"


# ============================================================
# Core extraction (shared between all formats)
# ============================================================


def extract_dashboard_data(
    db_path: Path,
    vertical: str | None = None,
) -> dict[str, Any]:
    """Extrai o conjunto de métricas que alimenta todos os formats.

    Args:
        db_path: caminho para papers.db.
        vertical: filtra por vertical; None = todas.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    where_clause = ""
    params: tuple[Any, ...] = ()
    if vertical:
        where_clause = " WHERE vertical = ?"
        params = (vertical,)

    data: dict[str, Any] = {
        "extracted_at": datetime.now(timezone.utc).isoformat(),
        "db_path": str(db_path),
        "vertical_filter": vertical,
    }

    # Verticals registry
    cur.execute("SELECT slug, name, cohort_json, created_at FROM verticals ORDER BY slug")
    data["verticals"] = [dict(r) for r in cur.fetchall()]

    # Citations summary
    cur.execute(
        f"SELECT COUNT(*) AS total, "
        f"       SUM(CASE WHEN cited=1 THEN 1 ELSE 0 END) AS cited, "
        f"       SUM(CASE WHEN cited=0 THEN 1 ELSE 0 END) AS not_cited "
        f"FROM citations{where_clause}",
        params,
    )
    row = cur.fetchone()
    total = row["total"] or 0
    cited = row["cited"] or 0
    data["citations_summary"] = {
        "total": total,
        "cited": cited,
        "not_cited": row["not_cited"] or 0,
        "citation_rate": (cited / total) if total else 0.0,
    }

    # Breakdown por LLM x Vertical
    cur.execute(
        f"SELECT llm, vertical, "
        f"       COUNT(*) AS total, "
        f"       SUM(CASE WHEN cited=1 THEN 1 ELSE 0 END) AS cited "
        f"FROM citations{where_clause} "
        f"GROUP BY llm, vertical ORDER BY vertical, llm",
        params,
    )
    data["citations_by_llm_vertical"] = [
        {**dict(r), "rate": (r["cited"] or 0) / r["total"] if r["total"] else 0.0}
        for r in cur.fetchall()
    ]

    # Breakdown por Model (rastreio de non-stationarity)
    cur.execute(
        f"SELECT model, model_version, COUNT(*) AS total, "
        f"       SUM(CASE WHEN cited=1 THEN 1 ELSE 0 END) AS cited "
        f"FROM citations{where_clause} "
        f"GROUP BY model, model_version ORDER BY total DESC",
        params,
    )
    data["citations_by_model"] = [dict(r) for r in cur.fetchall()]

    # Breakdown por Query Type (directive vs exploratory) — Onda 3
    try:
        cur.execute(
            f"SELECT query_type, vertical, COUNT(*) AS total, "
            f"       SUM(CASE WHEN cited=1 THEN 1 ELSE 0 END) AS cited "
            f"FROM citations{where_clause} "
            f"GROUP BY query_type, vertical ORDER BY vertical, query_type",
            params,
        )
        data["citations_by_query_type"] = [dict(r) for r in cur.fetchall()]
    except sqlite3.OperationalError:
        # DB pré-Migration 0003 ainda não tem a coluna
        data["citations_by_query_type"] = []

    # Breakdown por categoria
    cur.execute(
        f"SELECT query_category, COUNT(*) AS total, "
        f"       SUM(CASE WHEN cited=1 THEN 1 ELSE 0 END) AS cited "
        f"FROM citations{where_clause} "
        f"GROUP BY query_category ORDER BY total DESC",
        params,
    )
    data["citations_by_category"] = [dict(r) for r in cur.fetchall()]

    # Breakdown por Lang (PT vs EN)
    cur.execute(
        f"SELECT query_lang, COUNT(*) AS total, "
        f"       SUM(CASE WHEN cited=1 THEN 1 ELSE 0 END) AS cited "
        f"FROM citations{where_clause} "
        f"GROUP BY query_lang ORDER BY query_lang",
        params,
    )
    data["citations_by_lang"] = [dict(r) for r in cur.fetchall()]

    # FinOps summary
    cur.execute(
        f"SELECT platform, COUNT(*) AS calls, "
        f"       SUM(cost_usd) AS total_cost, "
        f"       SUM(total_tokens) AS total_tokens "
        f"FROM finops_usage{where_clause} "
        f"GROUP BY platform ORDER BY total_cost DESC",
        params,
    )
    data["finops_by_platform"] = [dict(r) for r in cur.fetchall()]

    # Collection runs (últimos 10)
    cur.execute(
        "SELECT timestamp, module, vertical, records, duration_ms, status "
        "FROM collection_runs ORDER BY timestamp DESC LIMIT 10"
    )
    data["recent_runs"] = [dict(r) for r in cur.fetchall()]

    # Daily snapshots
    cur.execute(
        f"SELECT date, module, vertical, created_at "
        f"FROM daily_snapshots{where_clause} "
        f"ORDER BY date DESC LIMIT 14",
        params,
    )
    data["recent_snapshots"] = [dict(r) for r in cur.fetchall()]

    conn.close()
    return data


# ============================================================
# Format: text
# ============================================================


def render_text(data: dict[str, Any]) -> str:
    """Relatório denso no stdout (substitui extract_dashboard.py original)."""
    lines: list[str] = []
    bar = "=" * 96

    lines.append(bar)
    lines.append("DASHBOARD DE CITAÇÕES — PAPERS")
    lines.append(bar)
    lines.append(f"Extraído em: {data['extracted_at']}")
    if data.get("vertical_filter"):
        lines.append(f"Filtro:      vertical = {data['vertical_filter']}")
    lines.append("")

    s = data["citations_summary"]
    lines.append(f"[Total] {s['total']} citações | cited={s['cited']} "
                 f"(rate {s['citation_rate']*100:.1f}%) | not_cited={s['not_cited']}")
    lines.append("")

    lines.append("[Por LLM × Vertical]")
    for r in data["citations_by_llm_vertical"]:
        lines.append(
            f"  {r['vertical']:<12} {r['llm']:<12} "
            f"total={r['total']:>4}  cited={r['cited']:>4}  rate={r['rate']*100:.1f}%"
        )
    lines.append("")

    if data.get("citations_by_query_type"):
        lines.append("[Por Query Type] (directive vs exploratory)")
        for r in data["citations_by_query_type"]:
            rate = (r["cited"] / r["total"] * 100) if r["total"] else 0
            lines.append(
                f"  {r['vertical']:<12} {r.get('query_type', '?'):<12} "
                f"total={r['total']:>4}  cited={r['cited']:>4}  rate={rate:.1f}%"
            )
        lines.append("")

    lines.append("[Por Language]")
    for r in data["citations_by_lang"]:
        rate = (r["cited"] / r["total"] * 100) if r["total"] else 0
        lines.append(f"  {r['query_lang']:<4} total={r['total']}  cited={r['cited']}  rate={rate:.1f}%")
    lines.append("")

    lines.append("[FinOps por platform]")
    for r in data["finops_by_platform"]:
        cost = r["total_cost"] or 0
        lines.append(f"  {r['platform']:<12} calls={r['calls']:>4}  cost=${cost:.4f}  tokens={r['total_tokens']}")
    lines.append("")

    lines.append("[Últimos 10 runs]")
    for r in data["recent_runs"]:
        lines.append(f"  {r['timestamp']}  {r['module']:<20} {r['vertical']:<12} "
                     f"records={r['records']:>4}  status={r['status']}")

    return "\n".join(lines)


# ============================================================
# Format: json
# ============================================================


def render_json(data: dict[str, Any]) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2, default=str)


# ============================================================
# Format: csv
# ============================================================


def render_csv(data: dict[str, Any]) -> str:
    """CSV flat por LLM × vertical (principal breakdown do paper)."""
    import io
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["vertical", "llm", "total", "cited", "not_cited", "citation_rate"])
    for r in data["citations_by_llm_vertical"]:
        not_cited = r["total"] - r["cited"]
        writer.writerow([
            r["vertical"], r["llm"], r["total"], r["cited"], not_cited,
            f"{r['rate']:.4f}",
        ])
    return buf.getvalue()


# ============================================================
# Format: html
# ============================================================


def render_html(data: dict[str, Any]) -> str:
    """Dashboard HTML autocontido (versão simplificada do create_html_dashboard)."""
    s = data["citations_summary"]
    rate = s["citation_rate"] * 100

    rows_llm = "".join(
        f"<tr><td>{r['vertical']}</td><td>{r['llm']}</td>"
        f"<td class='num'>{r['total']}</td>"
        f"<td class='num'>{r['cited']}</td>"
        f"<td class='num'>{r['rate']*100:.1f}%</td></tr>"
        for r in data["citations_by_llm_vertical"]
    )
    rows_qt = "".join(
        f"<tr><td>{r['vertical']}</td><td>{r.get('query_type', '?')}</td>"
        f"<td class='num'>{r['total']}</td>"
        f"<td class='num'>{r['cited']}</td>"
        f"<td class='num'>{(r['cited']/r['total']*100 if r['total'] else 0):.1f}%</td></tr>"
        for r in data.get("citations_by_query_type", [])
    )
    rows_finops = "".join(
        f"<tr><td>{r['platform']}</td>"
        f"<td class='num'>{r['calls']}</td>"
        f"<td class='num'>${(r['total_cost'] or 0):.4f}</td>"
        f"<td class='num'>{r['total_tokens']}</td></tr>"
        for r in data["finops_by_platform"]
    )

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Papers — Brasil GEO</title>
    <style>
        * {{ box-sizing: border-box; }}
        body {{ font-family: -apple-system, system-ui, sans-serif; background: #0f1419; color: #e0e0e0; margin: 0; line-height: 1.5; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 32px 20px; }}
        h1 {{ font-size: 28px; margin: 0 0 4px; color: #fff; }}
        .meta {{ color: #9aa4ad; font-size: 13px; margin-bottom: 24px; }}
        .card {{ background: #1a2028; border: 1px solid #2a3139; border-radius: 8px; padding: 20px; margin-bottom: 16px; }}
        h2 {{ font-size: 18px; margin: 0 0 12px; color: #9cdcfe; }}
        .kpi {{ display: flex; gap: 24px; flex-wrap: wrap; }}
        .kpi div {{ flex: 1 1 150px; }}
        .kpi strong {{ display: block; font-size: 32px; color: #ffd580; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
        th, td {{ padding: 8px 10px; border-bottom: 1px solid #2a3139; text-align: left; }}
        th {{ font-weight: 600; color: #9aa4ad; text-transform: uppercase; font-size: 11px; letter-spacing: 0.05em; }}
        .num {{ text-align: right; font-variant-numeric: tabular-nums; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Dashboard Papers — Brasil GEO</h1>
        <div class="meta">
            Extraído em {data['extracted_at']}
            {f"· filtro: {data['vertical_filter']}" if data.get('vertical_filter') else ''}
        </div>

        <div class="card kpi">
            <div><strong>{s['total']}</strong>total de observações</div>
            <div><strong>{s['cited']}</strong>com citação</div>
            <div><strong>{rate:.1f}%</strong>taxa de citação</div>
            <div><strong>{len(data['verticals'])}</strong>verticais ativas</div>
        </div>

        <div class="card">
            <h2>Citações por LLM × Vertical</h2>
            <table>
                <tr><th>Vertical</th><th>LLM</th><th class="num">Total</th><th class="num">Citadas</th><th class="num">Taxa</th></tr>
                {rows_llm}
            </table>
        </div>

        {'<div class="card"><h2>Citações por Query Type (directive vs exploratory)</h2><table>'
         '<tr><th>Vertical</th><th>Tipo</th><th class="num">Total</th><th class="num">Citadas</th><th class="num">Taxa</th></tr>'
         + rows_qt + '</table></div>' if rows_qt else ''}

        <div class="card">
            <h2>FinOps por plataforma</h2>
            <table>
                <tr><th>Platform</th><th class="num">Calls</th><th class="num">Cost (USD)</th><th class="num">Tokens</th></tr>
                {rows_finops}
            </table>
        </div>
    </div>
</body>
</html>
"""


# ============================================================
# CLI
# ============================================================


FORMATS = {
    "text": (render_text,  "stdout",              None),
    "json": (render_json,  "dashboard_data.json", "application/json"),
    "csv":  (render_csv,   "dashboard.csv",       "text/csv"),
    "html": (render_html,  "dashboard.html",      "text/html"),
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Export consolidado do papers.db")
    parser.add_argument("--format", choices=sorted(FORMATS.keys()), default="text")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Caminho de saída (default: data/<nome-padrão>; para --format text usa stdout)",
    )
    parser.add_argument("--vertical", default=None, help="Filtra por vertical (default: todas)")
    args = parser.parse_args()

    if not args.db.exists():
        print(f"ERRO: DB não encontrado em {args.db}", file=sys.stderr)
        return 1

    data = extract_dashboard_data(args.db, vertical=args.vertical)
    renderer, default_name, _ = FORMATS[args.format]
    output = renderer(data)

    if args.format == "text":
        target = args.output
        if target is None:
            print(output)
            return 0
    else:
        target = args.output or (DEFAULT_OUT_DIR / default_name)

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(output, encoding="utf-8")
    print(f"OK — {args.format} salvo em {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
