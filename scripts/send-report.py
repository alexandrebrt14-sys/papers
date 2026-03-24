"""
send-report.py — Envia relatório diário por email após coleta.

Gera um resumo HTML com métricas do dia e envia via Resend API.
Roda como step final do GitHub Actions após coleta + FinOps.

Uso:
  python scripts/send-report.py                    # Envia relatório do dia
  python scripts/send-report.py --dry-run          # Gera sem enviar
  RESEND_API_KEY=re_... python scripts/send-report.py
"""

import json
import os
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

import httpx

DB_PATH = os.getenv("PAPERS_DB_PATH", "data/papers.db")
RESEND_KEY = os.getenv("RESEND_API_KEY", "")
TO_EMAIL = os.getenv("FINOPS_ALERT_EMAIL", "caramaschiai@caramaschiai.io")
FROM_EMAIL = "Papers GEO <onboarding@resend.dev>"
DRY_RUN = "--dry-run" in sys.argv


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def build_report() -> dict:
    """Coleta métricas do banco e monta o relatório."""
    db = get_db()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Citações de hoje
    citations = db.execute("""
        SELECT llm, COUNT(*) as total,
               SUM(CASE WHEN cited THEN 1 ELSE 0 END) as cited_count
        FROM citations WHERE date(timestamp) = ?
        GROUP BY llm
    """, (today,)).fetchall()

    # FinOps de hoje
    finops = db.execute("""
        SELECT platform, SUM(total_cost_usd) as cost, SUM(total_queries) as queries,
               SUM(total_input_tokens + total_output_tokens) as tokens
        FROM finops_daily_rollup WHERE date = ?
        GROUP BY platform
    """, (today,)).fetchall()

    # Totais acumulados
    total_citations = db.execute("SELECT COUNT(*) as n FROM citations").fetchone()["n"]
    total_cited = db.execute("SELECT COUNT(*) as n FROM citations WHERE cited = 1").fetchone()["n"]

    # Alertas recentes
    alerts = db.execute("""
        SELECT * FROM finops_alerts WHERE date(timestamp) = ? ORDER BY timestamp DESC LIMIT 5
    """, (today,)).fetchall()

    # Runs de hoje
    runs = db.execute("""
        SELECT module, status, records, duration_ms
        FROM collection_runs WHERE date(timestamp) = ?
        ORDER BY timestamp DESC
    """, (today,)).fetchall()

    db.close()

    return {
        "date": today,
        "citations_today": [dict(r) for r in citations],
        "finops_today": [dict(r) for r in finops],
        "total_citations": total_citations,
        "total_cited": total_cited,
        "overall_rate": round(total_cited / max(total_citations, 1) * 100, 1),
        "alerts": [dict(r) for r in alerts],
        "runs": [dict(r) for r in runs],
    }


def render_html(report: dict) -> str:
    """Renderiza o relatório como HTML para email."""
    date = report["date"]
    citations = report["citations_today"]
    finops = report["finops_today"]
    runs = report["runs"]
    alerts = report["alerts"]

    # Citações por LLM
    citation_rows = ""
    total_queries = 0
    total_cited_today = 0
    for c in citations:
        rate = round(c["cited_count"] / max(c["total"], 1) * 100, 1)
        total_queries += c["total"]
        total_cited_today += c["cited_count"]
        color = "#2e844a" if rate > 10 else "#f4b400" if rate > 0 else "#c23934"
        citation_rows += f'<tr><td>{c["llm"]}</td><td>{c["cited_count"]}/{c["total"]}</td><td style="color:{color};font-weight:bold">{rate}%</td></tr>'

    overall_rate = round(total_cited_today / max(total_queries, 1) * 100, 1) if total_queries else 0

    # FinOps
    finops_rows = ""
    total_cost = 0
    total_tokens = 0
    for f in finops:
        total_cost += f["cost"] or 0
        total_tokens += f["tokens"] or 0
        finops_rows += f'<tr><td>{f["platform"]}</td><td>${f["cost"]:.4f}</td><td>{f["queries"] or 0}</td><td>{f["tokens"] or 0:,}</td></tr>'

    # Runs
    run_rows = ""
    for r in runs:
        status_color = "#2e844a" if r["status"] == "success" else "#c23934"
        run_rows += f'<tr><td>{r["module"]}</td><td style="color:{status_color}">{r["status"]}</td><td>{r["records"]}</td><td>{r["duration_ms"] or 0}ms</td></tr>'

    # Alertas
    alert_section = ""
    if alerts:
        alert_rows = ""
        for a in alerts:
            sev_color = "#c23934" if a["severity"] in ("critical", "emergency") else "#f4b400"
            alert_rows += f'<tr><td style="color:{sev_color}">{a["severity"]}</td><td>{a["platform"]}</td><td>{a["message"][:60]}</td></tr>'
        alert_section = f"""
        <h3 style="color:#f4b400;margin-top:20px">Alertas FinOps</h3>
        <table width="100%" cellpadding="6" style="border-collapse:collapse;font-size:13px">
            <tr style="background:#1a1a1a"><th>Severidade</th><th>Plataforma</th><th>Mensagem</th></tr>
            {alert_rows}
        </table>"""

    return f"""
    <div style="font-family:'Segoe UI',Arial,sans-serif;max-width:600px;margin:0 auto;background:#0a0a0a;color:#e0e0e0;padding:24px;border-radius:8px">
        <h2 style="color:#0176d3;margin:0 0 4px">Papers GEO — Relatório Diário</h2>
        <p style="color:#888;font-size:13px;margin:0 0 20px">{date} | Coleta automatizada | 4 LLMs</p>

        <div style="display:flex;gap:12px;margin-bottom:20px">
            <div style="flex:1;background:#141414;border-radius:8px;padding:16px;text-align:center">
                <div style="font-size:28px;font-weight:700;color:#fff">{overall_rate}%</div>
                <div style="font-size:11px;color:#888;text-transform:uppercase">Taxa de Citação</div>
                <div style="font-size:12px;color:#666">{total_cited_today}/{total_queries} hoje</div>
            </div>
            <div style="flex:1;background:#141414;border-radius:8px;padding:16px;text-align:center">
                <div style="font-size:28px;font-weight:700;color:#fff">${total_cost:.4f}</div>
                <div style="font-size:11px;color:#888;text-transform:uppercase">Custo do Dia</div>
                <div style="font-size:12px;color:#666">{total_tokens:,} tokens</div>
            </div>
            <div style="flex:1;background:#141414;border-radius:8px;padding:16px;text-align:center">
                <div style="font-size:28px;font-weight:700;color:#fff">{report['overall_rate']}%</div>
                <div style="font-size:11px;color:#888;text-transform:uppercase">Taxa Acumulada</div>
                <div style="font-size:12px;color:#666">{report['total_cited']}/{report['total_citations']} total</div>
            </div>
        </div>

        <h3 style="color:#0176d3;margin-top:20px">Citações por LLM</h3>
        <table width="100%" cellpadding="6" style="border-collapse:collapse;font-size:13px">
            <tr style="background:#1a1a1a"><th style="text-align:left">LLM</th><th>Citações</th><th>Taxa</th></tr>
            {citation_rows}
        </table>

        <h3 style="color:#0176d3;margin-top:20px">FinOps — Custo por Plataforma</h3>
        <table width="100%" cellpadding="6" style="border-collapse:collapse;font-size:13px">
            <tr style="background:#1a1a1a"><th style="text-align:left">Plataforma</th><th>Custo</th><th>Queries</th><th>Tokens</th></tr>
            {finops_rows}
        </table>

        <h3 style="color:#0176d3;margin-top:20px">Execuções</h3>
        <table width="100%" cellpadding="6" style="border-collapse:collapse;font-size:13px">
            <tr style="background:#1a1a1a"><th style="text-align:left">Módulo</th><th>Status</th><th>Registros</th><th>Duração</th></tr>
            {run_rows}
        </table>

        {alert_section}

        <hr style="border:1px solid #222;margin:20px 0">
        <p style="color:#666;font-size:11px;text-align:center">
            <a href="https://github.com/alexandrebrt14-sys/papers" style="color:#0176d3">GitHub</a> ·
            <a href="https://brasilgeo.ai" style="color:#0176d3">brasilgeo.ai</a> ·
            Papers v0.1.0 — Coleta automática diária
        </p>
    </div>
    """


def send_email(subject: str, html: str) -> bool:
    """Envia email via Resend API."""
    if not RESEND_KEY:
        print("[WARN] RESEND_API_KEY não configurada — email não enviado")
        return False

    resp = httpx.post(
        "https://api.resend.com/emails",
        headers={"Authorization": f"Bearer {RESEND_KEY}"},
        json={
            "from": FROM_EMAIL,
            "to": [TO_EMAIL],
            "subject": subject,
            "html": html,
        },
        timeout=15,
    )
    if resp.status_code in (200, 201):
        print(f"[OK] Email enviado para {TO_EMAIL}")
        return True
    else:
        print(f"[ERRO] Resend {resp.status_code}: {resp.text[:200]}")
        return False


def main():
    print(f"Gerando relatório diário ({datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')})...")

    if not Path(DB_PATH).exists():
        print(f"[WARN] Banco não encontrado: {DB_PATH} — pulando relatório")
        return

    report = build_report()
    html = render_html(report)
    subject = f"Papers GEO — Relatório {report['date']} | {report['overall_rate']}% citação acumulada"

    if DRY_RUN:
        output = Path("output/reports") / f"email-report-{report['date']}.html"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(html, encoding="utf-8")
        print(f"[DRY-RUN] Relatório salvo em {output}")
    else:
        send_email(subject, html)

    # Sempre salvar cópia local
    output = Path("output/reports") / f"email-report-{report['date']}.html"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html, encoding="utf-8")
    print(f"Cópia local: {output}")


if __name__ == "__main__":
    main()
