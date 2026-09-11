#!/usr/bin/env python3
"""build_tables.py — generates TABLES.md and NUMBERS.md for BRGEO-1 journal-v2.

Every figure that reaches TABLES.md is produced here and echoed into NUMBERS.md
next to the SQL statement or the function call that produced it, so no number in
the manuscript is transcribed by hand. Where a figure comes from plain SQL, the
statement printed in NUMBERS.md is the same string object that was executed —
they cannot drift.

The database is opened read-only. Nothing here writes to it.

    python build_tables.py            # regenerate TABLES.md and NUMBERS.md
    python build_tables.py --stdout   # print TABLES.md to the terminal instead
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import _common as C  # noqa: E402
import window_analysis as WA  # noqa: E402

CANON = "COALESCE(is_probe,0)=0"

# ---------------------------------------------------------------------------
# SQL statements, kept as named constants so NUMBERS.md can print what ran
# ---------------------------------------------------------------------------

SQL = {}

SQL["snapshot"] = """
SELECT MIN(timestamp) AS first_ts, MAX(timestamp) AS last_ts,
       COUNT(*) AS rows_all,
       SUM(CASE WHEN COALESCE(is_probe,0)=0 THEN 1 ELSE 0 END) AS rows_canonical,
       SUM(CASE WHEN COALESCE(is_probe,0)=1 THEN 1 ELSE 0 END) AS rows_probe
  FROM citations;
"""

SQL["t1_panel"] = """
SELECT llm, model_version,
       COUNT(*) AS n,
       MIN(date(timestamp)) AS first_day,
       MAX(date(timestamp)) AS last_day
  FROM citations
 WHERE COALESCE(is_probe,0)=0
 GROUP BY llm, model_version
 ORDER BY llm, first_day;
"""

SQL["t2_length"] = """
SELECT llm,
       COUNT(*) AS n,
       ROUND(AVG(length(response_text)),1) AS mean_chars,
       MIN(length(response_text)) AS min_chars,
       MAX(length(response_text)) AS max_chars,
       SUM(CASE WHEN length(response_text)=200 THEN 1 ELSE 0 END) AS exactly_200
  FROM citations
 WHERE COALESCE(is_probe,0)=0 AND response_text IS NOT NULL
 GROUP BY llm;
"""

SQL["t2_length_full_series"] = """
SELECT llm, COUNT(*) AS n, ROUND(AVG(length(response_text)),1) AS mean_chars,
       MIN(length(response_text)) AS min_chars, MAX(length(response_text)) AS max_chars,
       SUM(CASE WHEN length(response_text)=200 THEN 1 ELSE 0 END) AS exactly_200
  FROM citations WHERE response_text IS NOT NULL GROUP BY llm;
"""

SQL["t3_as_collected"] = """
SELECT llm,
       COUNT(*) AS n,
       SUM(CASE WHEN cited THEN 1 ELSE 0 END) AS cited_as_collected,
       SUM(COALESCE(cited_v2,0)) AS cited_v2,
       SUM(CASE WHEN length(response_text) > 200 THEN 1 ELSE 0 END) AS rows_truncated
  FROM citations
 WHERE COALESCE(is_probe,0)=0 AND response_text IS NOT NULL
 GROUP BY llm;
"""

SQL["t4_offset"] = """
SELECT llm,
       COUNT(*) AS n_cited,
       ROUND(AVG(first_entity_offset_v2),1) AS mean_offset,
       ROUND(AVG(response_length_chars_v2),1) AS mean_observed_length,
       ROUND(AVG(1.0*first_entity_offset_v2/response_length_chars_v2),4) AS mean_relative
  FROM citations
 WHERE COALESCE(is_probe,0)=0 AND cited_v2=1
   AND first_entity_offset_v2 IS NOT NULL
   AND response_length_chars_v2 > 0
 GROUP BY llm;
"""

SQL["t4_relative_values"] = """
SELECT llm, 1.0*first_entity_offset_v2/response_length_chars_v2 AS rel
  FROM citations
 WHERE COALESCE(is_probe,0)=0 AND cited_v2=1
   AND first_entity_offset_v2 IS NOT NULL
   AND response_length_chars_v2 > 0;
"""

SQL["t10_probe"] = """
SELECT llm,
       COUNT(*) AS n_probe,
       SUM(COALESCE(fictional_hit,0)) AS flagged_old_criterion
  FROM citations
 WHERE COALESCE(is_probe,0)=1
 GROUP BY llm;
"""

SQL["t10_refusal_rows"] = """
SELECT llm, response_text
  FROM citations
 WHERE COALESCE(is_probe,0)=1 AND fictional_hit=1
   AND response_text IS NOT NULL AND length(response_text) > 0;
"""

SQL["t11_days"] = """
SELECT date(timestamp) AS day, llm,
       COUNT(*) AS n,
       COUNT(DISTINCT query) AS distinct_queries
  FROM citations
 WHERE COALESCE(is_probe,0)=0
 GROUP BY day, llm
 ORDER BY day, llm;
"""

SQL["t11_months"] = """
SELECT strftime('%Y-%m', timestamp) AS month,
       COUNT(*) AS n_canonical,
       COUNT(DISTINCT date(timestamp)) AS days_with_data
  FROM citations
 WHERE COALESCE(is_probe,0)=0
 GROUP BY month ORDER BY month;
"""

SQL["t11_runs"] = """
SELECT status, COUNT(*) AS n, MIN(date(timestamp)) AS first_day,
       MAX(date(timestamp)) AS last_day
  FROM collection_runs GROUP BY status;
"""

SQL["t9_canonical_fictional_hit"] = """
SELECT COUNT(*) AS n_canonical,
       SUM(COALESCE(fictional_hit,0)) AS flagged_in_canonical
  FROM citations WHERE COALESCE(is_probe,0)=0;
"""

SQL["t3_perplexity_regime"] = """
SELECT CASE WHEN length(response_text) > 200
            THEN 'stored text longer than the window'
            ELSE 'stored text at or below the window' END AS regime,
       COUNT(*) AS n,
       SUM(CASE WHEN cited THEN 1 ELSE 0 END) AS cited,
       SUM(CASE WHEN response_full_text IS NOT NULL
                 AND length(response_full_text) > 0 THEN 1 ELSE 0 END)
         AS with_full_text_retained,
       MIN(date(timestamp)) AS first_day, MAX(date(timestamp)) AS last_day
  FROM citations
 WHERE COALESCE(is_probe,0)=0 AND llm='Perplexity'
 GROUP BY regime ORDER BY regime DESC;
"""

SQL["battery_coverage"] = """
SELECT llm, query_category, COUNT(*) AS n
  FROM citations WHERE COALESCE(is_probe,0)=0
 GROUP BY llm, query_category;
"""

SQL["t8_as_collected_distinct"] = """
SELECT COUNT(DISTINCT first_entity_v2) AS distinct_first_entities
  FROM citations
 WHERE COALESCE(is_probe,0)=0 AND first_entity_v2 IS NOT NULL;
"""

SQL["t11_aborted_detail"] = """
SELECT COUNT(*) AS n_rows, COUNT(DISTINCT date(timestamp)) AS distinct_days,
       substr(MIN(error_msg),1,60) AS reason_prefix
  FROM collection_runs WHERE status='aborted';
"""


def q(con, key, params=()):
    return con.execute(SQL[key], params).fetchall()


# ---------------------------------------------------------------------------
# Re-extraction under the uniform window (used by T3, T6, T7, T8, T9, T12)
# ---------------------------------------------------------------------------

def reextract_uniform(con):
    """Apply the uniform 200-character window to every canonical row.

    Returns a list of dicts, one per observation, carrying the harmonised
    citation flag and the first entity named inside the window. This is the
    identical operation performed by `scripts/harmonize_citation_window.py`,
    reimplemented here only so that the connection stays read-only.
    """
    ext = C.build_extractors(include_anchors=True, include_decoys=True)
    decoy_ext = C.build_decoy_extractors()
    rows = con.execute(
        f"""SELECT id, date(timestamp) AS day, llm, vertical, query_lang, query_type,
                   query_category, response_text, cited, cited_v2
              FROM citations
             WHERE {CANON} AND response_text IS NOT NULL
             ORDER BY id"""
    ).fetchall()
    out = []
    identity_mismatch = 0
    for r in rows:
        e = ext.get(r["vertical"])
        if e is None:
            continue
        text = r["response_text"]
        head = text[: C.WINDOW]
        m = e.extract(head)
        cited_win = 1 if m else 0
        if len(text) <= C.WINDOW and cited_win != (r["cited_v2"] or 0):
            identity_mismatch += 1
        dm = decoy_ext[r["vertical"]].extract(head)
        dm_full = decoy_ext[r["vertical"]].extract(text)
        out.append({
            "id": r["id"], "day": r["day"], "llm": r["llm"],
            "vertical": r["vertical"], "lang": r["query_lang"],
            "qtype": r["query_type"], "category": r["query_category"],
            "cited_collected": int(bool(r["cited"])),
            "cited_win": cited_win,
            "first_win": m[0].entity if m else None,
            "ents_win": [x.entity for x in m],
            "truncated": 1 if len(text) > C.WINDOW else 0,
            "decoy_win": dm[0].entity if dm else None,
            "decoy_collected": dm_full[0].entity if dm_full else None,
        })
    return out, identity_mismatch


#: Cohort names whose surface form collides with an ordinary word of the
#: response language, verified by inspecting the matched contexts. Neither is
#: listed in `src/config.AMBIGUOUS_ENTITIES` or `ENTITY_STOP_CONTEXTS`, so the
#: extractor matches the ordinary word. Quantified, not silently removed.
COLLIDING_NAMES = ("Involves", "Target")


# ---------------------------------------------------------------------------
# Concentration indices
# ---------------------------------------------------------------------------

def hhi(counts: list[int]) -> float:
    total = sum(counts)
    if total == 0:
        return float("nan")
    return sum((c / total) ** 2 for c in counts)


def gini(counts: list[int]) -> float:
    """Gini over the observed first-mention counts of the named entities."""
    xs = sorted(counts)
    n = len(xs)
    total = sum(xs)
    if n == 0 or total == 0:
        return float("nan")
    cum = sum((i + 1) * x for i, x in enumerate(xs))
    return (2 * cum) / (n * total) - (n + 1) / n


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------

def build():
    con = C.connect()
    ctx = {}

    snap = q(con, "snapshot")[0]
    ctx["snapshot"] = dict(snap)
    first_day = snap["first_ts"][:10]
    last_day = snap["last_ts"][:10]
    ctx["first_day"], ctx["last_day"] = first_day, last_day
    period = f"{first_day} to {last_day}"
    ctx["period"] = period

    n_canonical = snap["rows_canonical"]
    n_probe = snap["rows_probe"]

    # --- uniform-window re-extraction -------------------------------------
    uni, identity_mismatch = reextract_uniform(con)
    ctx["identity_mismatch"] = identity_mismatch
    ctx["n_reextracted"] = len(uni)

    by_engine = defaultdict(list)
    for r in uni:
        by_engine[r["llm"]].append(r)

    engines_present = [e for e in C.ENGINES if e in by_engine]
    ctx["engines_present"] = engines_present

    # ================= T1 =================
    t1_rows = q(con, "t1_panel")
    panel = defaultdict(list)
    for r in t1_rows:
        panel[r["llm"]].append(dict(r))
    ctx["t1"] = {k: v for k, v in panel.items()}

    t1_md = ["| Engine | Pinned model identifier | Class | Active period | Canonical n |",
             "|---|---|---|---|---:|"]
    for e in engines_present:
        parts = panel[e]
        ids = "<br>".join(
            f"`{p['model_version']}` ({p['first_day']} to {p['last_day']})"
            for p in parts)
        n = sum(p["n"] for p in parts)
        first = min(p["first_day"] for p in parts)
        last = max(p["last_day"] for p in parts)
        t1_md.append(f"| {e} | {ids} | {C.ENGINE_CLASS[e]} | {first} to {last} | {n:,} |")
    t1_md.append(f"| **Panel** | — | — | {first_day} to {last_day} | **{n_canonical:,}** |")

    # ================= T2 =================
    t2_rows = {r["llm"]: dict(r) for r in q(con, "t2_length")}
    ctx["t2"] = t2_rows
    ctx["t2_full_series"] = {r["llm"]: dict(r) for r in q(con, "t2_length_full_series")}
    t2_md = ["| Engine | n | Mean chars | Min | Max | Share exactly 200 |",
             "|---|---:|---:|---:|---:|---:|"]
    for e in sorted(engines_present, key=lambda x: -t2_rows[x]["n"]):
        d = t2_rows[e]
        share = 100 * d["exactly_200"] / d["n"]
        t2_md.append(f"| {e} | {d['n']:,} | {d['mean_chars']:,.1f} | {d['min_chars']:,} "
                     f"| {d['max_chars']:,} | {share:.1f}% |")

    # ================= T3 =================
    t3_sql = {r["llm"]: dict(r) for r in q(con, "t3_as_collected")}
    ctx["t3_sql"] = t3_sql
    t3 = {}
    for e in engines_present:
        rows = by_engine[e]
        n = len(rows)
        coll = sum(r["cited_collected"] for r in rows)
        win = sum(r["cited_win"] for r in rows)
        trunc = sum(r["truncated"] for r in rows)
        t3[e] = {"n": n, "collected": coll, "window": win, "truncated": trunc,
                 "rate_collected": 100 * coll / n, "rate_window": 100 * win / n,
                 "delta": 100 * (win - coll) / n}
    ctx["t3"] = t3
    t3_md = ["| Engine | n | As collected [95% CI] | Uniform 200-char window [95% CI] "
             "| Δ | Rows truncated |", "|---|---:|---:|---:|---:|---:|"]
    for e in sorted(engines_present, key=lambda x: -t3[x]["n"]):
        d = t3[e]
        t3_md.append(
            f"| {e}{C.flag_small(d['n'])} | {d['n']:,} | {C.rate_cell(d['collected'], d['n'])} "
            f"| {C.rate_cell(d['window'], d['n'])} | {d['delta']:+.1f} pp | {d['truncated']:,} |")
    tot_n = sum(d["n"] for d in t3.values())
    tot_c = sum(d["collected"] for d in t3.values())
    tot_w = sum(d["window"] for d in t3.values())
    tot_t = sum(d["truncated"] for d in t3.values())
    t3_md.append(f"| **Panel** | **{tot_n:,}** | {C.rate_cell(tot_c, tot_n)} "
                 f"| {C.rate_cell(tot_w, tot_n)} | {100*(tot_w-tot_c)/tot_n:+.1f} pp "
                 f"| **{tot_t:,}** |")
    ctx["t3_panel"] = {"n": tot_n, "collected": tot_c, "window": tot_w, "truncated": tot_t}

    # ================= T4 =================
    t4_sql = {r["llm"]: dict(r) for r in q(con, "t4_offset")}
    rel_by_engine = defaultdict(list)
    for r in con.execute(SQL["t4_relative_values"]):
        rel_by_engine[r["llm"]].append(r["rel"])
    t4 = {}
    for e in engines_present:
        if e not in t4_sql:
            continue
        d = t4_sql[e]
        t4[e] = {**d, "median_relative": C.median(rel_by_engine[e])}
    ctx["t4"] = t4
    t4_md = ["| Engine | n cited | Absolute offset, mean | Observed length, mean "
             "| Relative, mean | Relative, median |", "|---|---:|---:|---:|---:|---:|"]
    for e in sorted(t4, key=lambda x: t4[x]["mean_relative"]):
        d = t4[e]
        t4_md.append(f"| {e}{C.flag_small(d['n_cited'])} | {d['n_cited']:,} "
                     f"| {d['mean_offset']:,.0f} | {d['mean_observed_length']:,.0f} "
                     f"| {d['mean_relative']:.3f} | {d['median_relative']:.3f} |")

    # ================= T5 =================
    pre_rows = con.execute(
        f"""SELECT llm, response_text, COALESCE(cited_v2,0) AS c
              FROM citations WHERE {CANON} AND response_text IS NOT NULL"""
    ).fetchall()
    t5 = {}
    for r in pre_rows:
        a = t5.setdefault(r["llm"], {"n": 0, "pre": 0, "cited": 0})
        a["n"] += 1
        a["pre"] += 1 if C.opens_with_preamble(r["response_text"]) else 0
        a["cited"] += r["c"]
    ctx["t5"] = t5
    t5_md = ["| Engine | n | Opens with preamble [95% CI] | Citation rate, as collected [95% CI] |",
             "|---|---:|---:|---:|"]
    for e in sorted(t5, key=lambda x: -t5[x]["pre"] / t5[x]["n"]):
        d = t5[e]
        t5_md.append(f"| {e}{C.flag_small(d['n'])} | {d['n']:,} "
                     f"| {C.rate_cell(d['pre'], d['n'])} | {C.rate_cell(d['cited'], d['n'])} |")

    # T5 cross-check against manuscript v1.0 (same row set, to 2026-08-31)
    v10_rows = con.execute(
        f"""SELECT llm, response_text FROM citations
             WHERE {CANON} AND response_text IS NOT NULL
               AND date(timestamp) <= '2026-08-31'"""
    ).fetchall()
    t5_v10 = {}
    for r in v10_rows:
        a = t5_v10.setdefault(r["llm"], [0, 0])
        a[0] += 1
        a[1] += 1 if C.opens_with_preamble(r["response_text"]) else 0
    ctx["t5_v10_window"] = t5_v10
    ctx["t5_v10_published"] = {"Gemini": 79.6, "Perplexity": 9.2, "Grok": 4.0,
                               "ChatGPT": 2.1, "Groq": 1.1, "Claude": 0.0}

    # ================= T6 =================
    t6 = defaultdict(lambda: defaultdict(lambda: [0, 0]))
    for r in uni:
        cell = t6[r["llm"]][r["vertical"]]
        cell[0] += 1
        cell[1] += r["cited_win"]
    ctx["t6"] = {e: {v: list(t6[e][v]) for v in t6[e]} for e in t6}
    t6_md = ["| Engine | " + " | ".join(C.VERTICAL_LABEL[v] for v in C.VERTICALS) + " | All |",
             "|---|" + "---:|" * (len(C.VERTICALS) + 1)]
    for e in engines_present:
        cells = []
        tn = tc = 0
        for v in C.VERTICALS:
            n, c = t6[e][v]
            tn += n
            tc += c
            cells.append(f"{C.rate_cell(c, n)}{C.flag_small(n)}<br><sub>n = {n:,}</sub>"
                         if n else "—")
        cells.append(f"{C.rate_cell(tc, tn)}<br><sub>n = {tn:,}</sub>")
        t6_md.append(f"| {e} | " + " | ".join(cells) + " |")
    vt = {v: [0, 0] for v in C.VERTICALS}
    for e in engines_present:
        for v in C.VERTICALS:
            vt[v][0] += t6[e][v][0]
            vt[v][1] += t6[e][v][1]
    cells = [f"{C.rate_cell(vt[v][1], vt[v][0])}<br><sub>n = {vt[v][0]:,}</sub>" for v in C.VERTICALS]
    cells.append(f"{C.rate_cell(tot_w, tot_n)}<br><sub>n = {tot_n:,}</sub>")
    t6_md.append("| **Panel** | " + " | ".join(cells) + " |")
    ctx["t6_panel"] = {v: vt[v] for v in C.VERTICALS}

    # ================= T7 =================
    def stratum_matrix(key, levels):
        acc = defaultdict(lambda: defaultdict(lambda: [0, 0]))
        for r in uni:
            cell = acc[r["llm"]][r[key]]
            cell[0] += 1
            cell[1] += r["cited_win"]
        md = ["| Engine | " + " | ".join(levels) + " |",
              "|---|" + "---:|" * len(levels)]
        for e in engines_present:
            cells = []
            for lv in levels:
                n, c = acc[e][lv]
                cells.append(f"{C.rate_cell(c, n)}{C.flag_small(n)}<br><sub>n = {n:,}</sub>"
                             if n else "—")
            md.append(f"| {e} | " + " | ".join(cells) + " |")
        tots = {lv: [0, 0] for lv in levels}
        for e in engines_present:
            for lv in levels:
                tots[lv][0] += acc[e][lv][0]
                tots[lv][1] += acc[e][lv][1]
        md.append("| **Panel** | " + " | ".join(
            f"{C.rate_cell(tots[lv][1], tots[lv][0])}<br><sub>n = {tots[lv][0]:,}</sub>"
            for lv in levels) + " |")
        raw = {e: {lv: list(acc[e][lv]) for lv in levels} for e in engines_present}
        raw["Panel"] = {lv: list(tots[lv]) for lv in levels}
        return md, raw

    t7a_md, t7a_raw = stratum_matrix("lang", ["pt", "en"])
    t7b_md, t7b_raw = stratum_matrix("qtype", ["directive", "exploratory"])
    cats = [r[0] for r in con.execute(
        f"SELECT query_category, COUNT(*) c FROM citations WHERE {CANON} "
        "GROUP BY 1 ORDER BY c DESC")]
    t7c_md, t7c_raw = stratum_matrix("category", cats)
    ctx["t7a"], ctx["t7b"], ctx["t7c"] = t7a_raw, t7b_raw, t7c_raw
    ctx["categories"] = cats

    # ================= T8 =================
    firsts = Counter(r["first_win"] for r in uni if r["first_win"])
    total_first = sum(firsts.values())
    distinct = len(firsts)
    ranked = firsts.most_common()
    top10 = ranked[:10]
    cum = {}
    running = 0
    for i, (_, c) in enumerate(ranked, start=1):
        running += c
        if i in (1, 3, 5, 10):
            cum[i] = 100 * running / total_first
    counts = [c for _, c in ranked]
    ctx["t8"] = {
        "distinct": distinct, "total_first": total_first,
        "cohort_total": sum(len(C.get_v2_cohort(v, True, True)) for v in C.VERTICALS),
        "cohort_unique": len(C.ALL_REAL_BR | C.ALL_ANCHORS | C.ALL_DECOYS),
        "real_br": len(C.ALL_REAL_BR), "anchors": len(C.ALL_ANCHORS),
        "decoys": len(C.ALL_DECOYS),
        "named_real_br": len([e for e in firsts if e in C.ALL_REAL_BR]),
        "named_anchors": len([e for e in firsts if e in C.ALL_ANCHORS]),
        "named_decoys": len([e for e in firsts if e in C.ALL_DECOYS]),
        "top10": top10, "cumulative": cum,
        "hhi": hhi(counts), "gini": gini(counts),
    }
    t8_md = ["| Rank | Entity | First mentions | Share of first mentions | Cumulative share |",
             "|---:|---|---:|---:|---:|"]
    run = 0
    for i, (ent, c) in enumerate(top10, start=1):
        run += c
        t8_md.append(f"| {i} | {ent} | {c:,} | {100*c/total_first:.1f}% | {100*run/total_first:.1f}% |")

    # ================= T9 =================
    n_can = len(uni)
    decoy_win = sum(1 for r in uni if r["decoy_win"])
    decoy_coll = sum(1 for r in uni if r["decoy_collected"])
    decoy_names_win = Counter(r["decoy_win"] for r in uni if r["decoy_win"])
    decoy_names_coll = Counter(r["decoy_collected"] for r in uni if r["decoy_collected"])
    fh = q(con, "t9_canonical_fictional_hit")[0]
    ctx["t9"] = {
        "n_canonical": n_can,
        "decoy_window": decoy_win, "decoy_collected": decoy_coll,
        "names_window": dict(decoy_names_win), "names_collected": dict(decoy_names_coll),
        "stored_fictional_hit_in_canonical": fh["flagged_in_canonical"],
        "n_decoys": len(C.ALL_DECOYS),
    }
    per_engine_decoy = defaultdict(lambda: [0, 0, 0])
    for r in uni:
        a = per_engine_decoy[r["llm"]]
        a[0] += 1
        a[1] += 1 if r["decoy_win"] else 0
        a[2] += 1 if r["decoy_collected"] else 0
    ctx["t9_per_engine"] = {e: list(per_engine_decoy[e]) for e in engines_present}
    t9_md = ["| Engine | Canonical n | Spontaneous decoy, 200-char window [95% CI] "
             "| Spontaneous decoy, text as stored [95% CI] |",
             "|---|---:|---:|---:|"]
    for e in engines_present:
        n, w, cc = per_engine_decoy[e]
        t9_md.append(f"| {e} | {n:,} | {C.rate_cell(w, n, 3)} | {C.rate_cell(cc, n, 3)} |")
    t9_md.append(f"| **Panel** | **{n_can:,}** | {C.rate_cell(decoy_win, n_can, 3)} "
                 f"| {C.rate_cell(decoy_coll, n_can, 3)} |")

    # ================= T10 =================
    t10_sql = {r["llm"]: dict(r) for r in q(con, "t10_probe")}
    refusal = defaultdict(lambda: [0, 0])
    for r in con.execute(SQL["t10_refusal_rows"]):
        a = refusal[r["llm"]]
        a[0] += 1
        a[1] += 1 if C.has_refusal_marker(r["response_text"]) else 0
    ctx["t10"] = {e: {**t10_sql[e], "refusal_den": refusal[e][0],
                      "refusal_num": refusal[e][1]} for e in t10_sql}
    t10_md = ["| Engine | Probe n | Flagged by the legacy criterion [95% CI] "
              "| Of those, carrying an explicit refusal marker [95% CI] |",
              "|---|---:|---:|---:|"]
    tp = tf = trd = trn = 0
    for e in sorted(t10_sql, key=lambda x: -t10_sql[x]["n_probe"]):
        d = t10_sql[e]
        rd, rn = refusal[e]
        tp += d["n_probe"]; tf += d["flagged_old_criterion"]; trd += rd; trn += rn
        t10_md.append(f"| {e}{C.flag_small(d['n_probe'])} | {d['n_probe']:,} "
                      f"| {C.rate_cell(d['flagged_old_criterion'], d['n_probe'])} "
                      f"| {C.rate_cell(rn, rd)} |")
    t10_md.append(f"| **Panel** | **{tp:,}** | {C.rate_cell(tf, tp)} | {C.rate_cell(trn, trd)} |")
    ctx["t10_panel"] = {"n_probe": tp, "flagged": tf, "refusal_den": trd, "refusal_num": trn}

    # ================= T11 =================
    day_rows = q(con, "t11_days")
    per_day = defaultdict(dict)
    for r in day_rows:
        per_day[r["day"]][r["llm"]] = {"n": r["n"], "uq": r["distinct_queries"]}
    days = sorted(per_day)
    # Battery size actually attempted by each engine, taken as the maximum
    # distinct-query count the engine ever reached in one day.
    battery = {}
    for e in engines_present:
        battery[e] = max((per_day[d][e]["uq"] for d in days if e in per_day[d]),
                         default=0)
    active_span = {}
    for e in engines_present:
        ds = [d for d in days if e in per_day[d]]
        active_span[e] = (min(ds), max(ds))
    partial_days = []
    for d in days:
        short = [e for e in engines_present if e in per_day[d]
                 and per_day[d][e]["uq"] < battery[e]]
        absent = [e for e in engines_present
                  if e not in per_day[d] and active_span[e][0] <= d <= active_span[e][1]]
        if short or absent:
            partial_days.append({"day": d, "short": short, "absent": absent})
    # The registry of partial days, if the repository carries one. It records
    # engine absence only, and only from the date it was first seeded, so it is
    # read as an authority on the days it covers and not as a complete list.
    pd_path = C.REPO_ROOT / "data" / "partial_days.json"
    registered = []
    if pd_path.exists():
        try:
            registered = json.loads(pd_path.read_text(encoding="utf-8"))
        except Exception as exc:  # malformed file is a fact worth printing
            registered = [{"error": f"{type(exc).__name__}: {exc}"}]

    months = [dict(r) for r in q(con, "t11_months")]
    runs = {r["status"]: dict(r) for r in q(con, "t11_runs")}
    cal_first = days[0]
    cal_last = days[-1]
    from datetime import date, timedelta
    d0, d1 = date.fromisoformat(cal_first), date.fromisoformat(cal_last)
    calendar_days = (d1 - d0).days + 1
    dayset = {date.fromisoformat(d) for d in days}
    missing = [(d0 + timedelta(days=i)).isoformat()
               for i in range(calendar_days)
               if (d0 + timedelta(days=i)) not in dayset]
    # contiguous gap blocks
    gaps = []
    run_start = None
    prev = None
    for iso in missing:
        cur = date.fromisoformat(iso)
        if run_start is None:
            run_start = cur
        elif (cur - prev).days > 1:
            gaps.append((run_start.isoformat(), prev.isoformat(), (prev - run_start).days + 1))
            run_start = cur
        prev = cur
    if run_start is not None:
        gaps.append((run_start.isoformat(), prev.isoformat(), (prev - run_start).days + 1))
    ctx["t11"] = {
        "days_with_data": len(days), "calendar_days": calendar_days,
        "days_missing": len(missing), "gaps": gaps,
        "partial_days": [p["day"] for p in partial_days],
        "partial_detail": partial_days,
        "battery": battery, "months": months, "runs": runs,
        "first_day": cal_first, "last_day": cal_last,
        "partial_days_json_present": pd_path.exists(),
        "partial_days_json_path": str(pd_path),
        "registered": registered,
        "registered_in_span": [e for e in registered
                               if isinstance(e, dict) and "date" in e
                               and cal_first <= e["date"] <= cal_last],
        "registered_outside_span": [e for e in registered
                                    if isinstance(e, dict) and "date" in e
                                    and not (cal_first <= e["date"] <= cal_last)],
    }
    # Agreement between the registry and the derived definition, on the days
    # the registry covers.
    derived_absent = {p["day"]: set(p["absent"]) for p in partial_days}
    agree = []
    for e in [x for x in registered if isinstance(x, dict) and "date" in x
              and cal_first <= x["date"] <= cal_last]:
        agree.append({
            "date": e["date"],
            "registered_missing": sorted(e.get("missingLLMs", [])),
            "derived_absent": sorted(derived_absent.get(e["date"], set())),
            "match": sorted(e.get("missingLLMs", [])) == sorted(
                derived_absent.get(e["date"], set())),
        })
    ctx["t11"]["registry_agreement"] = agree
    t11_md = ["| Month | Days with data | Canonical n | Days on the calendar | Days with no data |",
              "|---|---:|---:|---:|---:|"]
    from calendar import monthrange
    have = {m["month"]: m for m in months}
    # Walk every month in the span so that a month with no data at all still
    # gets a row; 2026-07 is entirely absent from the GROUP BY result.
    all_months = []
    y, mo = d0.year, d0.month
    while (y, mo) <= (d1.year, d1.month):
        all_months.append(f"{y:04d}-{mo:02d}")
        mo += 1
        if mo == 13:
            y, mo = y + 1, 1
    months_full = []
    for key in all_months:
        yy, mm = (int(x) for x in key.split("-"))
        dim = monthrange(yy, mm)[1]
        lo = max(d0, date(yy, mm, 1))
        hi = min(d1, date(yy, mm, dim))
        span = (hi - lo).days + 1
        m = have.get(key, {"month": key, "days_with_data": 0, "n_canonical": 0})
        months_full.append({**m, "calendar_days": span,
                            "days_missing": span - m["days_with_data"]})
        t11_md.append(f"| {key} | {m['days_with_data']} | {m['n_canonical']:,} "
                      f"| {span} | {span - m['days_with_data']} |")
    ctx["t11_months_full"] = months_full
    t11_md.append(f"| **Series** | **{len(days)}** | **{n_canonical:,}** "
                  f"| **{calendar_days}** | **{len(missing)}** |")

    # ================= T12 =================
    t12 = {}
    daily = defaultdict(lambda: defaultdict(lambda: [0, 0]))
    for r in uni:
        cell = daily[r["llm"]][r["day"]]
        cell[0] += 1
        cell[1] += r["cited_win"]
    for e in engines_present:
        pts = [(d, n, c) for d, (n, c) in sorted(daily[e].items()) if n >= C.SMALL_N]
        if len(pts) < 3:
            t12[e] = {"days": len(pts), "slope": float("nan"),
                      "lo": float("nan"), "hi": float("nan"),
                      "first": None, "last": None, "min": None, "max": None}
            continue
        xs = [(date.fromisoformat(d) - d0).days for d, _, _ in pts]
        ys = [100 * c / n for _, n, c in pts]
        slope, lo, hi = C.ols_slope([float(x) for x in xs], ys)
        t12[e] = {"days": len(pts), "slope": slope, "lo": lo, "hi": hi,
                  "first": (pts[0][0], ys[0]), "last": (pts[-1][0], ys[-1]),
                  "min": min(ys), "max": max(ys),
                  "n_total": sum(p[1] for p in pts)}
    ctx["t12"] = t12
    ctx["t12_daily"] = {e: {d: list(v) for d, v in sorted(daily[e].items())}
                        for e in engines_present}
    t12_md = ["| Engine | Days with n ≥ 30 | First day rate | Last day rate | Min | Max "
              "| Slope, pp per day [95% interval] |",
              "|---|---:|---:|---:|---:|---:|---:|"]
    for e in engines_present:
        d = t12[e]
        if d["days"] < 3:
            t12_md.append(f"| {e}† | {d['days']} | — | — | — | — | not estimated |")
            continue
        # Fewer than ten daily points is too thin for even a descriptive slope.
        thin = "†" if d["days"] < 10 else ""
        t12_md.append(
            f"| {e}{thin} | {d['days']} | {d['first'][1]:.1f}% ({d['first'][0]}) "
            f"| {d['last'][1]:.1f}% ({d['last'][0]}) | {d['min']:.1f}% | {d['max']:.1f}% "
            f"| {d['slope']:+.4f} [{d['lo']:+.4f}, {d['hi']:+.4f}] |")

    # ================= T13 =================
    wa_rows = WA.collect_rows(con)
    wa = WA.analyse(wa_rows, C.build_extractors(True, True))
    ctx["t13"] = wa
    t13_md = WA.render_markdown(wa).split("\n")
    t13_dates = {e: wa["per_engine"][e]["dates"] for e in wa["per_engine"]}
    ctx["t13_dates"] = t13_dates

    # Gemini stratified by day (the 2026-09-06 anomaly)
    gem = defaultdict(lambda: {"n": 0, "head": 0, "full": 0, "len": 0})
    ext_all = C.build_extractors(True, True)
    for r in wa_rows:
        if r["llm"] != "Gemini":
            continue
        a = gem[r["timestamp"][:10]]
        full = r["response_full_text"]
        a["n"] += 1
        a["head"] += 1 if ext_all[r["vertical"]].extract(full[:C.WINDOW]) else 0
        a["full"] += 1 if ext_all[r["vertical"]].extract(full) else 0
        a["len"] += len(full)
    ctx["t13_gemini_by_day"] = {d: dict(v) for d, v in sorted(gem.items())}

    # --- lexical collision sensitivity (instrument note under Table 8) -----
    coll = set(COLLIDING_NAMES)
    coll_rows = sum(1 for r in uni if coll & set(r["ents_win"]))
    coll_only = sum(1 for r in uni
                    if r["ents_win"] and not (set(r["ents_win"]) - coll))
    coll_first = sum(1 for r in uni if r["first_win"] in coll)
    coll_by_name = Counter(
        e for r in uni for e in r["ents_win"] if e in coll)
    coll_by_engine = Counter(r["llm"] for r in uni if coll & set(r["ents_win"]))
    coll_by_lang = Counter(r["lang"] for r in uni if coll & set(r["ents_win"]))
    clean_cited = sum(1 for r in uni if set(r["ents_win"]) - coll)
    clean_firsts = Counter()
    for r in uni:
        rest = [e for e in r["ents_win"] if e not in coll]
        if rest:
            clean_firsts[rest[0]] += 1
    clean_total = sum(clean_firsts.values())
    clean_counts = [c for _, c in clean_firsts.most_common()]
    ctx["collision"] = {
        "names": list(COLLIDING_NAMES),
        "rows_touched": coll_rows,
        "rows_cited_only_by_collision": coll_only,
        "rows_first_mention_is_collision": coll_first,
        "by_name": dict(coll_by_name),
        "by_engine": dict(coll_by_engine),
        "by_lang": dict(coll_by_lang),
        "panel_n": len(uni),
        "panel_cited_with": sum(r["cited_win"] for r in uni),
        "panel_cited_without": clean_cited,
        "distinct_first_with": len(set(
            r["first_win"] for r in uni if r["first_win"])),
        "distinct_first_without": len(clean_firsts),
        "hhi_without": hhi(clean_counts),
        "top1_share_without": 100 * clean_counts[0] / clean_total,
    }

    # Gemini restricted to the two days on which its responses were not
    # themselves short: 2026-09-06 returned a maximum of 216 characters.
    g = ctx["t13_gemini_by_day"]
    sel = [v for d, v in g.items() if d >= "2026-09-07"]
    gn = sum(v["n"] for v in sel)
    gh = sum(v["head"] for v in sel)
    gf = sum(v["full"] for v in sel)
    ctx["t13_gemini_0708"] = {
        "n": gn, "head": gh, "full": gf,
        "rate_head": 100 * gh / gn, "rate_full": 100 * gf / gn,
        "delta_pp": 100 * (gf - gh) / gn,
        "head_ci": [100 * x for x in C.wilson(gh, gn)],
        "full_ci": [100 * x for x in C.wilson(gf, gn)],
        "mean_len": sum(v["len"] for v in sel) / gn,
    }

    ctx["t3_perplexity_regime"] = [dict(r) for r in q(con, "t3_perplexity_regime")]
    ctx["t8_as_collected_distinct"] = q(con, "t8_as_collected_distinct")[0][
        "distinct_first_entities"]
    ctx["t11_aborted_detail"] = dict(q(con, "t11_aborted_detail")[0])
    cov = defaultdict(dict)
    for r in q(con, "battery_coverage"):
        cov[r["llm"]][r["query_category"]] = r["n"]
    ctx["battery_coverage"] = {e: cov[e] for e in engines_present}

    ctx["md"] = {
        "t1": t1_md, "t2": t2_md, "t3": t3_md, "t4": t4_md, "t5": t5_md,
        "t6": t6_md, "t7a": t7a_md, "t7b": t7b_md, "t7c": t7c_md,
        "t8": t8_md, "t9": t9_md, "t10": t10_md, "t11": t11_md,
        "t12": t12_md, "t13": t13_md,
    }
    ctx["n_canonical"] = n_canonical
    ctx["n_probe"] = n_probe
    ctx["n_all"] = snap["rows_all"]
    return ctx


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stdout", action="store_true")
    ap.add_argument("--dump", default=None, help="write the raw context as JSON")
    args = ap.parse_args()

    ctx = build()

    import render  # local module holding the prose of the two documents
    tables_md = render.tables_md(ctx)
    numbers_md = render.numbers_md(ctx, SQL)

    if args.stdout:
        print(tables_md)
    else:
        (HERE / "TABLES.md").write_text(tables_md, encoding="utf-8")
        (HERE / "NUMBERS.md").write_text(numbers_md, encoding="utf-8")
        print(f"wrote {HERE / 'TABLES.md'}")
        print(f"wrote {HERE / 'NUMBERS.md'}")
    if args.dump:
        Path(args.dump).write_text(
            json.dumps(ctx, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
        print(f"wrote {args.dump}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
