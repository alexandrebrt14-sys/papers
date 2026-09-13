#!/usr/bin/env python3
"""window_analysis.py — Table 13: the observation window measured on every arm.

WHAT THIS ANSWERS
-----------------
Manuscript v1.0 could put a number on the window effect for exactly one arm.
Five of the six client adapters stored `response_text = text[:200]`, so the
text beyond character 200 was never written to disk and no re-extraction can
recover it. Perplexity took a different path through the client and stored up
to 2,502 characters, which is why its rate could be measured twice — 75.7% as
collected, 51.9% under a uniform 200-character window — and why the paper's
headline is a single-arm result carrying a general claim.

Since 2026-08-31 the pipeline writes the entire response to
`citations.response_full_text` (migration 0010) while continuing to write the
windowed string to `response_text`. For those observations the comparison can
be run within the arm, on the same rows, with the same matching rule: extract
over `response_full_text[:200]`, extract over `response_full_text`, and read
off the difference. That is what this script does.

WHY IT REUSES THE PROJECT'S EXTRACTOR
-------------------------------------
The point of the paper is that the matching rule is held fixed and only the
window moves. A parallel extractor written for this analysis would confound
the two. So the cohort comes from `src/config_v2.get_v2_cohort` and the
matching from `src.analysis.entity_extraction.EntityExtractor`, in the same
configuration `scripts/harmonize_citation_window.py` used to produce the
manuscript's window table: the v2 cohort including international anchors and
fictitious decoys, with the project's alias, ambiguity, canonical-name and
stop-context dictionaries.

Two internal checks guard that claim and are printed with the result:

  1. `response_text` must equal `response_full_text[:200]` on every row used.
     If it does not, the two columns are not two views of one response and the
     paired comparison is meaningless.
  2. Extracting over `response_full_text[:200]` must reproduce the stored
     `cited_v2` on every row used. If it does not, this script's matching rule
     differs from the one that produced the series, and no delta it reports is
     attributable to the window.

Both checks are hard: a failure is printed as FAIL and the exit code is 1.

USAGE
-----
    python window_analysis.py                 # print the table
    python window_analysis.py --json out.json # also write the raw numbers

The database is opened read-only. Nothing here writes to it.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _common as C  # noqa: E402


def collect_rows(con) -> list:
    """Canonical observations that retained the full response.

    `COALESCE(is_probe,0)=0` is the canonical stratum of the study; the
    adversarial probes are excluded because their target is a fictitious
    entity and their citation rate is not the quantity in question.
    """
    return con.execute(
        """
        SELECT id, timestamp, llm, vertical, query_lang, query_type,
               response_text, response_full_text, cited_v2
          FROM citations
         WHERE COALESCE(is_probe,0)=0
           AND response_full_text IS NOT NULL
           AND length(response_full_text) > 0
         ORDER BY id
        """
    ).fetchall()


def analyse(rows, extractors) -> dict:
    """Per-engine paired comparison of the 200-character and full windows."""
    per: dict[str, dict] = {}
    checks = {"text_prefix_mismatch": 0, "cited_v2_mismatch": 0, "rows": 0}

    for r in rows:
        engine = r["llm"]
        ext = extractors.get(r["vertical"])
        if ext is None:  # unknown vertical slug; should not happen
            continue
        full = r["response_full_text"]
        head = full[: C.WINDOW]

        # Check 1 — the two stored columns are two views of the same response.
        if (r["response_text"] or "") != head:
            checks["text_prefix_mismatch"] += 1

        m_head = ext.extract(head)
        m_full = ext.extract(full)
        c_head = 1 if m_head else 0
        c_full = 1 if m_full else 0

        # Check 2 — this script's rule reproduces the series' own rule.
        if c_head != (r["cited_v2"] or 0):
            checks["cited_v2_mismatch"] += 1
        checks["rows"] += 1

        a = per.setdefault(engine, {
            "n": 0, "cited_head": 0, "cited_full": 0,
            "len_full_sum": 0, "len_full": [],
            "gain": 0, "loss": 0,            # discordant pairs
            "count_head_sum": 0, "count_full_sum": 0,
            "first_offset_full": [],
            "dates": set(),
        })
        a["n"] += 1
        a["cited_head"] += c_head
        a["cited_full"] += c_full
        a["len_full_sum"] += len(full)
        a["len_full"].append(len(full))
        a["count_head_sum"] += len(m_head)
        a["count_full_sum"] += len(m_full)
        if c_full and not c_head:
            a["gain"] += 1
        if c_head and not c_full:
            a["loss"] += 1
        if m_full:
            a["first_offset_full"].append(m_full[0].start)
        a["dates"].add(r["timestamp"][:10])

    out = {}
    for engine, a in per.items():
        n = a["n"]
        rh, rf = a["cited_head"] / n, a["cited_full"] / n
        out[engine] = {
            "n": n,
            "cited_head": a["cited_head"],
            "cited_full": a["cited_full"],
            "rate_head": 100 * rh,
            "rate_head_ci": [100 * x for x in C.wilson(a["cited_head"], n)],
            "rate_full": 100 * rf,
            "rate_full_ci": [100 * x for x in C.wilson(a["cited_full"], n)],
            "delta_pp": 100 * (rf - rh),
            "mean_len_full": a["len_full_sum"] / n,
            "median_len_full": C.median([float(x) for x in a["len_full"]]),
            "max_len_full": max(a["len_full"]),
            "rows_longer_than_window": sum(1 for x in a["len_full"] if x > C.WINDOW),
            "mean_entities_head": a["count_head_sum"] / n,
            "mean_entities_full": a["count_full_sum"] / n,
            "gain": a["gain"],
            "loss": a["loss"],
            "mcnemar_p": C.exact_binomial_two_sided(a["gain"], a["loss"]),
            "median_first_offset_full": C.median(
                [float(x) for x in a["first_offset_full"]]),
            "dates": sorted(a["dates"]),
        }
    return {"per_engine": out, "checks": checks}


def render_markdown(result: dict) -> str:
    per = result["per_engine"]
    order = [e for e in C.ENGINES if e in per]
    lines = [
        "| Engine | n | Rate at 200 chars [95% CI] | Rate on full text [95% CI] "
        "| Δ | Gains | Losses | Exact McNemar p | Mean full length |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for e in order:
        d = per[e]
        mark = C.flag_small(d["n"])
        p = d["mcnemar_p"]
        p_txt = "—" if p != p else ("<0.001" if p < 0.001 else f"{p:.3f}")
        lines.append(
            f"| {e}{mark} | {d['n']:,} | "
            f"{d['rate_head']:.1f} [{d['rate_head_ci'][0]:.1f}, {d['rate_head_ci'][1]:.1f}] | "
            f"{d['rate_full']:.1f} [{d['rate_full_ci'][0]:.1f}, {d['rate_full_ci'][1]:.1f}] | "
            f"{d['delta_pp']:+.1f} pp | {d['gain']:,} | {d['loss']:,} | {p_txt} | "
            f"{d['mean_len_full']:,.0f} |"
        )
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", default=None,
                    help="also write the raw numbers to this path")
    args = ap.parse_args()

    con = C.connect()
    snapshot = con.execute("SELECT MAX(timestamp) FROM citations").fetchone()[0]
    rows = collect_rows(con)
    if not rows:
        print("no canonical row retains response_full_text; nothing to compare")
        return 1

    extractors = C.build_extractors(include_anchors=True, include_decoys=True)
    result = analyse(rows, extractors)
    result["snapshot_max_timestamp"] = snapshot
    result["window"] = C.WINDOW
    result["cohort_sizes"] = {
        v: len(C.get_v2_cohort(v, True, True)) for v in C.VERTICALS}

    checks = result["checks"]
    ok = (checks["text_prefix_mismatch"] == 0 and checks["cited_v2_mismatch"] == 0)

    print(f"snapshot (max citations.timestamp): {snapshot}")
    print(f"rows compared                     : {checks['rows']:,}")
    print(f"check 1 response_text == full[:200] mismatches: "
          f"{checks['text_prefix_mismatch']}  "
          f"{'PASS' if checks['text_prefix_mismatch'] == 0 else 'FAIL'}")
    print(f"check 2 re-extraction == cited_v2   mismatches: "
          f"{checks['cited_v2_mismatch']}  "
          f"{'PASS' if checks['cited_v2_mismatch'] == 0 else 'FAIL'}")
    print()
    print(render_markdown(result))
    print()
    for e in [x for x in C.ENGINES if x in result["per_engine"]]:
        d = result["per_engine"][e]
        print(f"  {e:<12} dates={','.join(d['dates'])}  "
              f"rows>200 chars={d['rows_longer_than_window']:,}  "
              f"median full length={d['median_len_full']:,.0f}  "
              f"max={d['max_len_full']:,}  "
              f"mean entities 200/full={d['mean_entities_head']:.2f}/"
              f"{d['mean_entities_full']:.2f}  "
              f"median first offset in full={d['median_first_offset_full']:,.0f}")

    if args.json:
        Path(args.json).write_text(
            json.dumps(result, indent=2, ensure_ascii=False, default=list),
            encoding="utf-8")
        print(f"\nwrote {args.json}")

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
