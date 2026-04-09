#!/usr/bin/env python3
"""generate_dashboard_json.py — gera papers/data/dashboard_data.json
a partir do papers.db.

Roda no GitHub Actions após cada coleta diária.
Output é consumido por alexandrecaramaschi.com/research via fetch
GitHub raw com ISR (revalidate 24h).
"""

import sqlite3
import json
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "papers.db"
OUT_PATH = Path(__file__).resolve().parent.parent / "data" / "dashboard_data.json"

LLM_META = {
    "Perplexity": {"provider": "Perplexity AI", "model": "sonar", "color": "#20b2aa"},
    "Claude": {"provider": "Anthropic", "model": "claude-haiku-4-5-20251001", "color": "#d4a574"},
    "ChatGPT": {"provider": "OpenAI", "model": "gpt-4o-mini-2024-07-18", "color": "#10a37f"},
    "Gemini": {"provider": "Google", "model": "gemini-2.5-flash", "color": "#4285f4"},
}

VERT_META = {
    "fintech": {"name": "Fintech", "color": "#0ea5e9"},
    "tecnologia": {"name": "Tecnologia", "color": "#f59e0b"},
    "varejo": {"name": "Varejo", "color": "#ec4899"},
    "saude": {"name": "Saúde", "color": "#0d9488"},
}


def main():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row

    # === KPIs gerais ===
    total_row = con.execute("SELECT COUNT(*) AS q, COALESCE(SUM(cited),0) AS c FROM citations").fetchone()
    total_queries = total_row["q"]
    total_cited = total_row["c"]

    # === By LLM ===
    by_llm = []
    for r in con.execute("SELECT llm, COUNT(*) AS q, COALESCE(SUM(cited),0) AS c, ROUND(AVG(latency_ms)) AS lat FROM citations WHERE latency_ms IS NOT NULL GROUP BY llm"):
        meta = LLM_META.get(r["llm"], {"provider": r["llm"], "model": "unknown", "color": "#666"})
        by_llm.append({
            "name": r["llm"],
            "model": meta["model"],
            "provider": meta["provider"],
            "queries": r["q"],
            "cited": r["c"],
            "rate": round((r["c"] / max(r["q"], 1)) * 100, 1),
            "avgLatencyMs": int(r["lat"] or 0),
            "color": meta["color"],
        })
    by_llm.sort(key=lambda x: -x["rate"])

    # === By Vertical ===
    by_vertical = []
    for r in con.execute("SELECT vertical, COUNT(*) AS q, COALESCE(SUM(cited),0) AS c FROM citations GROUP BY vertical"):
        meta = VERT_META.get(r["vertical"], {"name": r["vertical"].title(), "color": "#666"})
        by_vertical.append({
            "slug": r["vertical"],
            "name": meta["name"],
            "queries": r["q"],
            "cited": r["c"],
            "rate": round((r["c"] / max(r["q"], 1)) * 100, 1),
            "color": meta["color"],
        })
    by_vertical.sort(key=lambda x: -x["rate"])

    # === Cross matrix LLM × Vertical ===
    cross = []
    for v in ["fintech", "saude", "tecnologia", "varejo"]:
        for r in con.execute("SELECT llm, COUNT(*) AS q, COALESCE(SUM(cited),0) AS c FROM citations WHERE vertical=? GROUP BY llm", (v,)):
            cross.append({
                "vertical": v,
                "model": r["llm"],
                "queries": r["q"],
                "cited": r["c"],
                "rate": round((r["c"] / max(r["q"], 1)) * 100, 1),
            })

    # === Verticals full (rosters + cited entities) ===
    # Coleta primeiro os rosters
    roster_data = []
    for r in con.execute("SELECT slug, name, cohort_json FROM verticals"):
        roster_data.append((r["slug"], r["name"], json.loads(r["cohort_json"])))

    verticals_full = {}
    for slug, name, roster in roster_data:
        # Cita entities por vertical via JOIN
        cited_ents = []
        for r in con.execute("""
            SELECT ctx.entity AS entity, COUNT(*) AS cnt
            FROM citation_context ctx
            JOIN citations c ON c.id = ctx.citation_id
            WHERE c.vertical = ?
            GROUP BY ctx.entity
            ORDER BY cnt DESC
        """, (slug,)):
            cited_ents.append({"entity": r["entity"], "count": r["cnt"]})

        verticals_full[slug] = {
            "slug": slug,
            "name": name,
            "roster": roster,
            "rosterCount": len(roster),
            "citedEntities": cited_ents,
            "citedCount": len(cited_ents),
            "coverage": round(len(cited_ents) / max(len(roster), 1) * 100, 1),
        }

    # === Top entities globally ===
    top_ents = []
    for r in con.execute("""
        SELECT entity, COUNT(*) AS cnt
        FROM citation_context
        GROUP BY entity
        ORDER BY cnt DESC
        LIMIT 30
    """):
        top_ents.append({"name": r["entity"], "citations": r["cnt"]})

    # === Sentiment ===
    sentiment = {"neutral": 0, "positive": 0, "negative": 0}
    for r in con.execute("SELECT sentiment, COUNT(*) AS cnt FROM citation_context GROUP BY sentiment"):
        if r["sentiment"] in sentiment:
            sentiment[r["sentiment"]] = r["cnt"]

    # === Attribution ===
    attribution = {"named": 0, "linked": 0}
    for r in con.execute("SELECT attribution, COUNT(*) AS cnt FROM citation_context GROUP BY attribution"):
        if r["attribution"] == "named":
            attribution["named"] = r["cnt"]
        elif r["attribution"] == "linked":
            attribution["linked"] = r["cnt"]

    # === Position ===
    position = {"initial": 0, "middle": 0, "final": 0}
    for r in con.execute("SELECT position_tercile, COUNT(*) AS cnt FROM citation_context WHERE position_tercile IS NOT NULL GROUP BY position_tercile"):
        if r["position_tercile"] == 1:
            position["initial"] = r["cnt"]
        elif r["position_tercile"] == 2:
            position["middle"] = r["cnt"]
        elif r["position_tercile"] == 3:
            position["final"] = r["cnt"]

    # === Last collection + collection rounds ===
    last_coll = con.execute("SELECT MAX(created_at) AS last FROM citations").fetchone()["last"]
    rounds = con.execute("SELECT COUNT(*) AS n FROM collection_runs WHERE status='success'").fetchone()["n"]
    ctx_count = con.execute("SELECT COUNT(*) AS n FROM citation_context").fetchone()["n"]

    # === Days collecting ===
    days_collecting = con.execute("SELECT COUNT(DISTINCT date(timestamp)) AS n FROM citations").fetchone()["n"]

    entities_real = sum(v["rosterCount"] for v in verticals_full.values())

    # === Build final JSON ===
    from datetime import datetime, timezone
    data = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "lastCollection": last_coll,
        "dbVersion": f"papers.db ({total_queries} queries dataset)",
        "totalQueries": total_queries,
        "totalCited": total_cited,
        "overallRate": round((total_cited / max(total_queries, 1)) * 100, 1),
        "entitiesMonitored": entities_real + 8,  # 8 fictícias para validação
        "entitiesReal": entities_real,
        "entitiesFictitious": 8,
        "contextAnalyses": ctx_count,
        "collectionRounds": rounds,
        "daysCollecting": days_collecting,
        "byLLM": by_llm,
        "byVertical": by_vertical,
        "crossMatrix": cross,
        "verticalsFull": verticals_full,
        "topEntities": top_ents,
        "sentiment": sentiment,
        "attribution": attribution,
        "positionInResponse": position,
    }

    OUT_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"OK — {OUT_PATH.relative_to(DB_PATH.parent.parent)}")
    print(f"  {total_queries} queries, {total_cited} citadas, {data['overallRate']}% taxa global")
    print(f"  {entities_real} entidades reais + 8 fictícias")
    print(f"  {ctx_count} análises de contexto")
    print(f"  {rounds} rodadas de coleta")
    print(f"  Última coleta: {last_coll}")
    print()
    print("Por vertical:")
    for v in by_vertical:
        vf = verticals_full[v["slug"]]
        print(f"  {v['name']}: {v['queries']} queries, {v['cited']} citadas ({v['rate']}%) — {vf['rosterCount']} no roster, {vf['citedCount']} com citação detectada")


if __name__ == "__main__":
    main()
