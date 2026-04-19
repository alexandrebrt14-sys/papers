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
    "Gemini": {"provider": "Google", "model": "gemini-2.5-pro", "color": "#4285f4"},
    "Groq": {"provider": "Groq", "model": "llama-3.3-70b-versatile", "color": "#f55036"},
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

    # === ENRIQUECIMENTO ANALITICO (2026-04-16) ================================

    # --- Serie temporal diaria ---
    daily_series = []
    for r in con.execute("""
        SELECT date(timestamp) AS d, COUNT(*) AS q, SUM(cited) AS c
        FROM citations GROUP BY d ORDER BY d
    """):
        daily_series.append({
            "date": r["d"],
            "queries": r["q"],
            "cited": r["c"],
            "rate": round((r["c"] / max(r["q"], 1)) * 100, 1),
        })

    # --- Bootstrap CI 95% da taxa global via Wilson score (sem deps externas) ---
    def wilson_ci(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
        if n == 0: return (0.0, 0.0)
        p = k / n
        z2 = z * z
        denom = 1 + z2 / n
        center = (p + z2 / (2 * n)) / denom
        margin = z * ((p * (1 - p) / n + z2 / (4 * n * n)) ** 0.5) / denom
        return (round((center - margin) * 100, 1), round((center + margin) * 100, 1))

    overall_lo, overall_hi = wilson_ci(total_cited, total_queries)
    llm_ci = {}
    for r in con.execute("SELECT llm, COUNT(*) q, SUM(cited) c FROM citations GROUP BY llm"):
        lo, hi = wilson_ci(r["c"], r["q"])
        llm_ci[r["llm"]] = {"ci95_low": lo, "ci95_high": hi}

    # --- Entity coverage gap: marcas do roster NUNCA citadas ---
    uncited_by_vertical = {}
    for slug, name, roster in roster_data:
        cited_entities_set = set()
        for r in con.execute("""
            SELECT DISTINCT ctx.entity
            FROM citation_context ctx
            JOIN citations c ON c.id = ctx.citation_id
            WHERE c.vertical = ?
        """, (slug,)):
            cited_entities_set.add(r["entity"])
        # Match por substring para lidar com "Banco Inter" vs "Inter"
        uncited = []
        for brand in roster:
            # Ficticias nao devem aparecer — filtrar
            is_fake = brand in {
                "Banco Floresta Digital", "FinPay Solutions",
                "MegaStore Brasil", "ShopNova Digital",
                "HealthTech Brasil", "Clínica Horizonte Digital",
                "TechNova Solutions", "DataBridge Brasil",
            }
            if is_fake:
                continue
            matched = any(
                brand.lower() in c.lower() or c.lower() in brand.lower()
                for c in cited_entities_set
            )
            if not matched:
                uncited.append(brand)
        uncited_by_vertical[slug] = uncited

    # --- Cross-vertical mentions: marcas que aparecem em >1 vertical ---
    cross_vertical_ents = []
    for r in con.execute("""
        SELECT ctx.entity, COUNT(DISTINCT c.vertical) AS verts, COUNT(*) AS total
        FROM citation_context ctx JOIN citations c ON c.id = ctx.citation_id
        GROUP BY ctx.entity HAVING verts > 1
        ORDER BY verts DESC, total DESC LIMIT 15
    """):
        cross_vertical_ents.append({
            "entity": r["entity"],
            "verticals": r["verts"],
            "totalMentions": r["total"],
        })

    # --- Sentiment por LLM ---
    sentiment_by_llm = {}
    for r in con.execute("""
        SELECT c.llm, ctx.sentiment, COUNT(*) AS n
        FROM citation_context ctx JOIN citations c ON c.id = ctx.citation_id
        WHERE ctx.sentiment IS NOT NULL GROUP BY c.llm, ctx.sentiment
    """):
        sentiment_by_llm.setdefault(r["llm"], {"neutral": 0, "positive": 0, "negative": 0})
        if r["sentiment"] in sentiment_by_llm[r["llm"]]:
            sentiment_by_llm[r["llm"]][r["sentiment"]] = r["n"]

    # --- Categoria x taxa de citacao (qual tipo de query mais dispara citacao?) ---
    by_category = []
    for r in con.execute("""
        SELECT query_category, COUNT(*) q, SUM(cited) c
        FROM citations GROUP BY query_category ORDER BY c * 1.0 / q DESC
    """):
        by_category.append({
            "category": r["query_category"],
            "queries": r["q"],
            "cited": r["c"],
            "rate": round((r["c"] / max(r["q"], 1)) * 100, 1),
        })

    # --- Idioma: PT vs EN (LLMs citam mais em qual?) ---
    by_lang = []
    for r in con.execute("SELECT query_lang, COUNT(*) q, SUM(cited) c FROM citations GROUP BY query_lang"):
        by_lang.append({
            "lang": r["query_lang"],
            "queries": r["q"],
            "cited": r["c"],
            "rate": round((r["c"] / max(r["q"], 1)) * 100, 1),
        })

    # --- Query Type: directive vs exploratory (Onda 3 — 2026-04-19) ---
    # Directive = query já força listagem ("quais os melhores X"). Exploratory
    # = descoberta genuína ("é seguro?"). Permite isolar bias de framing nos
    # testes estatísticos do Paper 1.
    by_query_type = []
    try:
        for r in con.execute(
            "SELECT query_type, COUNT(*) q, SUM(cited) c FROM citations "
            "WHERE query_type IS NOT NULL GROUP BY query_type"
        ):
            by_query_type.append({
                "type": r["query_type"],
                "queries": r["q"],
                "cited": r["c"],
                "rate": round((r["c"] / max(r["q"], 1)) * 100, 1),
            })
    except sqlite3.OperationalError:
        # DB pré-Migration 0003 ainda sem a coluna query_type
        pass

    # --- Latencia media por LLM (performance signal) ---
    latency_stats = []
    for r in con.execute("""
        SELECT llm, ROUND(AVG(latency_ms)) avg_ms, ROUND(MIN(latency_ms)) min_ms, ROUND(MAX(latency_ms)) max_ms
        FROM citations WHERE latency_ms IS NOT NULL GROUP BY llm
    """):
        latency_stats.append({
            "llm": r["llm"],
            "avgMs": int(r["avg_ms"] or 0),
            "minMs": int(r["min_ms"] or 0),
            "maxMs": int(r["max_ms"] or 0),
        })

    # --- False-positive calibration result ---
    fictitious_entities = [
        "Banco Floresta Digital", "FinPay Solutions",
        "MegaStore Brasil", "ShopNova Digital",
        "HealthTech Brasil", "Clínica Horizonte Digital",
        "TechNova Solutions", "DataBridge Brasil",
    ]
    total_responses = con.execute("SELECT COUNT(*) n FROM citations WHERE response_text IS NOT NULL").fetchone()["n"]
    fp_count = 0
    for e in fictitious_entities:
        r = con.execute("SELECT COUNT(*) n FROM citations WHERE response_text LIKE ?", (f"%{e}%",)).fetchone()
        fp_count += r["n"]
    false_positive_rate = round((fp_count / max(total_responses, 1)) * 100, 3)
    specificity = round(100 - false_positive_rate, 3)

    # === Build final JSON ===
    from datetime import datetime, timezone
    data = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "lastCollection": last_coll,
        "dbVersion": f"papers.db ({total_queries} queries dataset)",
        "totalQueries": total_queries,
        "totalCited": total_cited,
        "overallRate": round((total_cited / max(total_queries, 1)) * 100, 1),
        "overallCI95": {"low": overall_lo, "high": overall_hi},
        "entitiesMonitored": entities_real + 8,  # 8 fictícias para validação
        "entitiesReal": entities_real,
        "entitiesFictitious": 8,
        "contextAnalyses": ctx_count,
        "collectionRounds": rounds,
        "daysCollecting": days_collecting,
        "byLLM": [{**llm, **llm_ci.get(llm["name"], {})} for llm in by_llm],
        "byVertical": by_vertical,
        "crossMatrix": cross,
        "verticalsFull": verticals_full,
        "topEntities": top_ents,
        "sentiment": sentiment,
        "attribution": attribution,
        "positionInResponse": position,
        # Analytics enriquecidos (2026-04-16)
        "dailySeries": daily_series,
        "uncitedByVertical": uncited_by_vertical,
        "crossVerticalEntities": cross_vertical_ents,
        "sentimentByLLM": sentiment_by_llm,
        "byCategory": by_category,
        "byLanguage": by_lang,
        "byQueryType": by_query_type,
        "latencyStats": latency_stats,
        "calibration": {
            "fictitiousEntities": fictitious_entities,
            "fictitiousMentions": fp_count,
            "totalResponses": total_responses,
            "falsePositiveRate": false_positive_rate,
            "specificity": specificity,
        },
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
