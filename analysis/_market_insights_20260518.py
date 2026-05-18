"""Analise GEO para mercado — 2026-05-18

Computa:
1. Citation rate por entidade (real BR + anchor intl + fict), com IC 95% bootstrap
2. Cross-LLM consistency: em quantos dos 5 LLMs a entidade aparece >= 1×
3. Vertical breakdown (fintech / varejo / saude / tecnologia)
4. Directive (com nome) vs Exploratory (sem nome) — discrimina "share of mind organico"
5. Hallucination rate (fict citadas) por LLM — sinal de overconfidence
6. Top GEO performers e gaps

Fontes:
- citations.cited_entities_v2_json (extraction v2, normalizada)
- analysis/_cohort_canonical_v2.json (cohort canonico)
"""
from __future__ import annotations
import json
import sqlite3
import math
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "papers.db"

with open(ROOT / "analysis" / "_cohort_canonical_v2.json", "r", encoding="utf-8") as f:
    COHORT = json.load(f)

# Build reverse map: entity -> (vertical, type)
ENTITY_META: dict[str, tuple[str, str]] = {}
for v, names in COHORT["real"].items():
    for n in names:
        ENTITY_META[n] = (v, "real_br")
for v, names in COHORT["fict"].items():
    for n in names:
        ENTITY_META[n] = (v, "fictitious")
for v, names in COHORT["anchors"].items():
    for n in names:
        ENTITY_META[n] = (v, "anchor_intl")


def bca_bootstrap_ci(successes: int, n: int, n_boot: int = 2000, alpha: float = 0.05) -> tuple[float, float, float]:
    """IC 95% para proporção via percentile bootstrap (rápido, robusto para n>=30).
    Retorna (ponto, lower, upper)."""
    if n == 0:
        return (0.0, 0.0, 0.0)
    p = successes / n
    if n < 5:
        return (p, max(0, p - 0.3), min(1, p + 0.3))
    rng = np.random.default_rng(42)
    draws = rng.binomial(n, p, size=n_boot) / n
    lo, hi = np.quantile(draws, [alpha / 2, 1 - alpha / 2])
    return (p, float(lo), float(hi))


def main():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # 1) Extrai todas citations com entidades
    rows = c.execute("""
        SELECT id, llm, vertical, query_type, query_lang, query_category,
               cited_v2, cited_entities_v2_json, fictitious_target, is_calibration
        FROM citations
        WHERE cited_entities_v2_json IS NOT NULL
          AND cited_entities_v2_json NOT IN ('', '[]')
          AND COALESCE(is_calibration, 0) = 0
    """).fetchall()

    print(f"Citations com entidades extraidas: {len(rows):,}")

    # 2) Long form: (citation_id, llm, vertical, query_type, entity)
    long_form: list[dict] = []
    for r in rows:
        try:
            ents = json.loads(r["cited_entities_v2_json"])
        except Exception:
            continue
        if not isinstance(ents, list):
            continue
        for e in ents:
            long_form.append({
                "cid": r["id"],
                "llm": r["llm"],
                "vertical": r["vertical"],
                "query_type": r["query_type"],
                "query_lang": r["query_lang"],
                "query_category": r["query_category"],
                "entity": e,
                "fictitious_target": r["fictitious_target"],
            })
    print(f"Long-form rows (citation × entity): {len(long_form):,}")

    # 3) Total queries por (llm, vertical) — denominador
    denom = c.execute("""
        SELECT llm, vertical, COUNT(*) n
        FROM citations
        WHERE COALESCE(is_calibration,0)=0
        GROUP BY llm, vertical
    """).fetchall()
    denom_map = {(r["llm"], r["vertical"]): r["n"] for r in denom}

    # 4) Citation count por (entity, llm, vertical)
    counts: dict[tuple[str, str, str], int] = defaultdict(int)
    for r in long_form:
        counts[(r["entity"], r["llm"], r["vertical"])] += 1

    # 5) Agregação por entidade (sobre todos LLMs / verticais)
    agg_total: dict[str, dict] = defaultdict(lambda: {
        "mentions": 0, "llms": set(), "verticals": set(),
        "by_llm": defaultdict(int), "by_qtype": defaultdict(int),
    })
    for r in long_form:
        agg_total[r["entity"]]["mentions"] += 1
        agg_total[r["entity"]]["llms"].add(r["llm"])
        agg_total[r["entity"]]["verticals"].add(r["vertical"])
        agg_total[r["entity"]]["by_llm"][r["llm"]] += 1
        agg_total[r["entity"]]["by_qtype"][r["query_type"]] += 1

    # 6) Citation rate (proporcao de queries com a entidade citada)
    # Denominador: total de queries onde a entidade É CANDIDATA (mesma vertical)
    queries_per_vert = c.execute("""
        SELECT vertical, COUNT(*) n
        FROM citations
        WHERE COALESCE(is_calibration,0)=0
        GROUP BY vertical
    """).fetchall()
    qpv = {r["vertical"]: r["n"] for r in queries_per_vert}

    # 7) Build ranking — entidade × (cohort_type, vertical, total_mentions, n_llms, rate_em_propria_vertical)
    entity_rows = []
    for ent, data in agg_total.items():
        meta = ENTITY_META.get(ent)
        if meta:
            vert_cohort, kind = meta
            denom_q = qpv.get(vert_cohort, 0)
            in_vert = sum(v for (e, llm, v), n in counts.items() if e == ent and v == vert_cohort for v in [v] for n in [n])
            # Mentions in own vertical only
            in_vert = sum(n for (e, llm, v), n in counts.items() if e == ent and v == vert_cohort)
            rate, lo, hi = bca_bootstrap_ci(in_vert, denom_q)
        else:
            vert_cohort, kind = (data["verticals"].pop() if data["verticals"] else "?"), "unknown"
            data["verticals"].add(vert_cohort)
            denom_q = qpv.get(vert_cohort, 0)
            in_vert = data["mentions"]
            rate, lo, hi = bca_bootstrap_ci(in_vert, denom_q)
        entity_rows.append({
            "entity": ent,
            "kind": kind,
            "vertical": vert_cohort,
            "mentions": data["mentions"],
            "n_llms": len(data["llms"]),
            "in_vertical_mentions": in_vert,
            "vertical_queries": denom_q,
            "rate_pct": rate * 100,
            "ci95_lo_pct": lo * 100,
            "ci95_hi_pct": hi * 100,
            "by_llm_json": dict(data["by_llm"]),
            "by_qtype_json": dict(data["by_qtype"]),
        })

    # 8) Salva resultado completo + ranking
    entity_rows.sort(key=lambda r: r["mentions"], reverse=True)
    Path(ROOT / "analysis").mkdir(exist_ok=True)
    out_path = ROOT / "analysis" / "geo_insights_20260518.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({
            "generated_at": "2026-05-18",
            "n_citations": len(rows),
            "n_long_form": len(long_form),
            "by_llm_vertical": [dict(r) for r in denom],
            "entities": entity_rows,
        }, f, ensure_ascii=False, indent=2)
    print(f"\nSaved {out_path}")

    # 9) PRINT relatório
    print("\n" + "=" * 80)
    print("TOP 25 ENTIDADES REAIS BR — citation rate na própria vertical, IC 95%")
    print("=" * 80)
    real_only = [r for r in entity_rows if r["kind"] == "real_br"]
    real_only.sort(key=lambda r: r["rate_pct"], reverse=True)
    print(f"{'entity':<28} {'vert':<11} {'rate':>7} {'CI95':>16} {'n_llms':>7} {'mentions':>9}")
    for r in real_only[:25]:
        ci = f"[{r['ci95_lo_pct']:.1f}-{r['ci95_hi_pct']:.1f}]"
        print(f"{r['entity']:<28} {r['vertical']:<11} {r['rate_pct']:>6.2f}% {ci:>16} {r['n_llms']:>7} {r['mentions']:>9}")

    print("\n" + "=" * 80)
    print("HALLUCINATION RATE — FICTÍCIAS citadas (deveria ser 0%)")
    print("=" * 80)
    fict_only = [r for r in entity_rows if r["kind"] == "fictitious"]
    fict_only.sort(key=lambda r: r["mentions"], reverse=True)
    print(f"{'fict_entity':<28} {'vert':<11} {'mentions':>9} {'by_llm':<40}")
    for r in fict_only:
        by_llm = ", ".join(f"{k}={v}" for k, v in sorted(r["by_llm_json"].items(), key=lambda x: -x[1]))
        print(f"{r['entity']:<28} {r['vertical']:<11} {r['mentions']:>9}  {by_llm}")

    print("\n" + "=" * 80)
    print("HALLUCINATION RATE por LLM (queries fact-probe direcionadas)")
    print("=" * 80)
    fact_probe = c.execute("""
        SELECT llm, COUNT(*) n_probes, SUM(fictional_hit) n_halluc
        FROM citations
        WHERE fictitious_target IS NOT NULL
        GROUP BY llm
    """).fetchall()
    print(f"{'llm':<11} {'probes':>7} {'halluc':>7} {'rate':>7}")
    for r in fact_probe:
        rate = (r['n_halluc'] or 0) / r['n_probes'] if r['n_probes'] else 0
        print(f"{r['llm']:<11} {r['n_probes']:>7} {r['n_halluc'] or 0:>7} {rate*100:>6.2f}%")


if __name__ == "__main__":
    main()
