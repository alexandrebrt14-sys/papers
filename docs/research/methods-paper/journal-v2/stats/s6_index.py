#!/usr/bin/env python3
"""s6_index.py — S6: the BRGEO-1 reporting index, recomputed on the declared cut.

WHY THIS SCRIPT EXISTS
----------------------
Every index figure published before 2026-09-11 came from `scripts/brgeo1_index.py`
run on a snapshot that closed on 2026-08-31 with 66,399 canonical observations,
and was reported under a caption naming the series that closes on 2026-09-08 with
68,624. The panel in force on that run was selected by an undeclared minimum
observation count of 500, which excluded a live arm and retained one retired on
2026-08-16; commit 51159fd of 2026-08-31 replaced the count by a 14-day recency
rule. This script recomputes the index on the declared cut, under both panel
rules, so that the caption, the cut and the panel agree with each other.

WHAT IS MEASURED
----------------
For every entity of the v2 cohort, inside its own vertical:

  C  coverage     share of panel observations naming the entity inside the window
  P  prominence   1 - offset/window at the first mention, averaged over the
                  observations in which the entity appears
  B  breadth      share of panel engines naming the entity at least once

  GCI = (C * P * B)^(1/3)

and then, over the entities cited at least once, pooled across the four verticals:

  1. Spearman rank correlation of the index against simple coverage, on the four
     subsets the published table carries.
  2. Spearman rank correlation between four aggregations of the same three
     components, and between each and simple coverage.
  3. Variance decomposition of log GCI, Cov(log X, log GCI) / (3 Var(log GCI)).
  4. Rank displacement between the index ordering and the coverage ordering.

MEASUREMENT RULE
----------------
The canonical stratum is `COALESCE(is_probe,0)=0`, which is the rule the tables
and the S-files use; `scripts/brgeo1_index.py` writes `is_probe = 0`, and the two
agree on this database because the column holds no NULL. Entity matching is the
project's own extractor over the v2 cohort with anchors and decoys included,
reached through `../tables/_common.py` so that this script cannot drift from the
manuscript tables on the matching rule. Every observation is read under the
uniform 200-character window, that is over `response_text[:200]`.

Two panel rules are computed and both are written out:

  series   every arm that contributed a canonical observation to the series.
           No undeclared parameter; the denominator is the 68,624 of §9.
  recency  the rule now in `scripts/brgeo1_index.py`: an arm is in the panel when
           it produced a row within DIAS_PARA_CONSIDERAR_ATIVO days of the last
           timestamp of its vertical. On this cut it drops the arm retired on
           2026-08-16 and admits the one that entered on 2026-08-23.

Under `recency` the numerator and the denominator are both restricted to panel
arms. The reference implementation divides a numerator summed over every arm by a
denominator summed over panel arms only; that asymmetry is reported by this
script as a separate row rather than reproduced.

The database is opened read-only. Nothing here writes to it.

A third rule, `--min-obs`, reproduces the undeclared observation count the
reference implementation applied before commit 51159fd. Together with `--until`
it recovers the exact configuration behind a superseded figure, which is how the
provenance statement in §10.2 was established rather than asserted.

    python s6_index.py                 # recompute, write data/s6_*.csv
    python s6_index.py --window 0      # whole stored response instead of 200 chars
    python s6_index.py --quiet         # CSV only, no report on stdout
    python s6_index.py --until 2026-08-31 --min-obs 500   # the superseded figures
"""
from __future__ import annotations

import argparse
import collections
import csv
import math
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TABLES = HERE.parent / "tables"
sys.path.insert(0, str(TABLES))

import _common as CM  # noqa: E402

from src.analysis.entity_extraction import EntityExtractor  # noqa: E402
from src.config import (  # noqa: E402
    AMBIGUOUS_ENTITIES,
    CANONICAL_NAMES,
    ENTITY_ALIASES,
    ENTITY_STOP_CONTEXTS,
)
from src.config_v2 import get_v2_cohort  # noqa: E402

DATA_DIR = HERE / "data"

#: Recency parameter of the reference implementation, `scripts/brgeo1_index.py`.
DIAS_PARA_CONSIDERAR_ATIVO = 14

#: Weights of the fourth aggregation, kept identical to the published table.
WEIGHTS = (0.60, 0.25, 0.15)

VERTICAL_LABEL = CM.VERTICAL_LABEL


# ---------------------------------------------------------------------------
# Rank statistics, written out rather than imported, so the tie rule is visible
# ---------------------------------------------------------------------------

def ranks_average(values: list[float]) -> list[float]:
    """Ranks of `values`, ties receiving their average rank."""
    order = sorted(range(len(values)), key=lambda i: values[i])
    out = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            out[order[k]] = avg
        i = j + 1
    return out


def spearman(a: list[float], b: list[float]) -> float:
    """Spearman rank correlation, computed as Pearson on average ranks."""
    ra, rb = ranks_average(a), ranks_average(b)
    n = len(ra)
    ma, mb = sum(ra) / n, sum(rb) / n
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    da = math.sqrt(sum((x - ma) ** 2 for x in ra))
    db = math.sqrt(sum((y - mb) ** 2 for y in rb))
    return num / (da * db) if da and db else float("nan")


def descending_positions(values: list[float]) -> list[int]:
    """Position of each element when the list is sorted from largest to smallest.

    Ties are broken by the entity order already fixed by the caller, so the
    displacement statistics below are reproducible.
    """
    order = sorted(range(len(values)), key=lambda i: -values[i])
    pos = [0] * len(values)
    for place, idx in enumerate(order, 1):
        pos[idx] = place
    return pos


def quantile(values: list[float], q: float) -> float:
    """Linear-interpolation quantile, the numpy default, spelled out."""
    if not values:
        return float("nan")
    s = sorted(values)
    if len(s) == 1:
        return float(s[0])
    h = (len(s) - 1) * q
    lo = math.floor(h)
    hi = math.ceil(h)
    return float(s[lo] + (s[hi] - s[lo]) * (h - lo))


# ---------------------------------------------------------------------------
# Components
# ---------------------------------------------------------------------------

def extractor(vertical: str) -> EntityExtractor:
    return EntityExtractor(
        cohort=get_v2_cohort(vertical, include_anchors=True, include_decoys=True),
        aliases=ENTITY_ALIASES,
        ambiguous=AMBIGUOUS_ENTITIES,
        canonical_names=CANONICAL_NAMES,
        stop_contexts=ENTITY_STOP_CONTEXTS,
    )


def recency_panel(con: sqlite3.Connection, vertical: str,
                  days: int = DIAS_PARA_CONSIDERAR_ATIVO,
                  until: str | None = None) -> set[str]:
    """The panel rule of `scripts/brgeo1_index.py`, anchored on the data.

    Anchored on the last timestamp of the vertical rather than on the clock, so
    that the same database yields the same panel whenever the script is run.
    """
    clause = " AND date(timestamp) <= ?" if until else ""
    params = (vertical, until) if until else (vertical,)
    end = con.execute(
        "SELECT MAX(timestamp) FROM citations WHERE vertical = ?" + clause, params
    ).fetchone()[0]
    if not end:
        return set()
    rows = con.execute(
        "SELECT DISTINCT llm FROM citations WHERE vertical = ? "
        "AND timestamp >= datetime(?, ?)" + clause,
        ((vertical, end, f"-{int(days)} days", until) if until
         else (vertical, end, f"-{int(days)} days")),
    ).fetchall()
    return {r[0] for r in rows}


def scan_vertical(con: sqlite3.Connection, vertical: str, window: int,
                  until: str | None = None) -> dict:
    """One pass over the canonical rows of a vertical, read under the window.

    `until` closes the cut at an earlier date, so that a figure published on a
    previous snapshot can be checked rather than taken on trust.
    """
    ext = extractor(vertical)
    clause = " AND date(timestamp) <= ?" if until else ""
    params = (vertical, until) if until else (vertical,)
    rows = con.execute(
        f"SELECT llm, response_text, cited_v2 FROM citations "
        f"WHERE {CM.CANONICAL} AND vertical = ? AND response_text IS NOT NULL"
        f"{clause}",
        params,
    ).fetchall()

    obs = collections.Counter()
    mentions: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    prominence: dict[str, dict[str, list[float]]] = collections.defaultdict(
        lambda: collections.defaultdict(list))
    identity_checked = identity_failed = 0

    for r in rows:
        llm = r["llm"]
        stored = r["response_text"]
        obs[llm] += 1
        text = stored[:window] if window else stored
        denominator = window if window else max(len(text), 1)

        first: dict[str, int] = {}
        for m in ext.extract(text):
            first.setdefault(m.entity, m.start)

        # The identity check of NUMBERS.md V2, repeated here on the rows where
        # the stored record is itself inside the window: re-extraction has to
        # reproduce the stored `cited_v2` flag, or every figure below is void.
        if window and len(stored) <= window and r["cited_v2"] is not None:
            identity_checked += 1
            if bool(first) != bool(r["cited_v2"]):
                identity_failed += 1

        for entity, offset in first.items():
            mentions[entity][llm] += 1
            prominence[entity][llm].append(1.0 - min(1.0, offset / denominator))

    return {
        "vertical": vertical,
        "obs": obs,
        "mentions": mentions,
        "prominence": prominence,
        "identity_checked": identity_checked,
        "identity_failed": identity_failed,
    }


def components(scan: dict, panel: list[str]) -> list[dict]:
    """C, P, B and the geometric mean, with numerator and denominator on the panel."""
    total = sum(scan["obs"][m] for m in panel)
    out = []
    for entity, per_engine in scan["mentions"].items():
        hits = sum(per_engine[m] for m in panel)
        if hits == 0:
            continue
        c = hits / total if total else 0.0
        vals = [v for m in panel for v in scan["prominence"][entity][m]]
        p = sum(vals) / len(vals) if vals else 0.0
        b = len([m for m in panel if per_engine[m] > 0]) / len(panel) if panel else 0.0
        gci = (c * p * b) ** (1 / 3) if c > 0 and p > 0 and b > 0 else 0.0
        out.append({
            "vertical": scan["vertical"],
            "entity": entity,
            "mentions": hits,
            "panel_observations": total,
            "coverage": c,
            "prominence": p,
            "breadth": b,
            "gci": gci,
        })
    return sorted(out, key=lambda d: -d["gci"])


# ---------------------------------------------------------------------------
# Aggregations
# ---------------------------------------------------------------------------

def aggregations(row: dict) -> dict[str, float]:
    c, p, b = row["coverage"], row["prominence"], row["breadth"]
    wc, wp, wb = WEIGHTS
    harmonic = 3.0 / (1 / c + 1 / p + 1 / b) if c > 0 and p > 0 and b > 0 else 0.0
    return {
        "geometric": (c * p * b) ** (1 / 3) if c > 0 and p > 0 and b > 0 else 0.0,
        "arithmetic": (c + p + b) / 3.0,
        "harmonic": harmonic,
        "weighted": wc * c + wp * p + wb * b,
    }


def variance_decomposition(rows: list[dict]) -> list[dict]:
    """Cov(log X, log GCI) / (3 Var(log GCI)), per component, summing to unity."""
    logs = {k: [math.log(r[k]) for r in rows] for k in ("coverage", "breadth", "prominence")}
    log_gci = [math.log(r["gci"]) for r in rows]
    n = len(rows)
    mg = sum(log_gci) / n
    var_g = sum((x - mg) ** 2 for x in log_gci) / (n - 1)
    out = []
    for name in ("coverage", "breadth", "prominence"):
        xs = logs[name]
        mx = sum(xs) / n
        var_x = sum((x - mx) ** 2 for x in xs) / (n - 1)
        cov = sum((x - mx) * (y - mg) for x, y in zip(xs, log_gci)) / (n - 1)
        out.append({
            "component": name,
            "var_log": var_x,
            "contribution": cov / (3.0 * var_g),
        })
    return out


def subset_correlations(rows: list[dict]) -> list[dict]:
    """The four subsets the published table carries, in its own order."""
    leaders = {}
    for r in rows:
        cur = leaders.get(r["vertical"])
        if cur is None or r["coverage"] > cur["coverage"]:
            leaders[r["vertical"]] = r
    leader_ids = {(r["vertical"], r["entity"]) for r in leaders.values()}

    subsets = [
        ("All entities", rows),
        ("Excluding each vertical's leader",
         [r for r in rows if (r["vertical"], r["entity"]) not in leader_ids]),
        ("Coverage between 0.1% and 5%",
         [r for r in rows if 0.001 <= r["coverage"] <= 0.05]),
        ("Coverage below 1%", [r for r in rows if r["coverage"] < 0.01]),
    ]
    out = []
    for label, sub in subsets:
        rho = (spearman([r["gci"] for r in sub], [r["coverage"] for r in sub])
               if len(sub) > 2 else float("nan"))
        out.append({"subset": label, "rho": rho, "n": len(sub)})
    return out


def displacement(rows: list[dict]) -> dict:
    """Rank displacement between the index ordering and the coverage ordering."""
    gci_pos = descending_positions([r["gci"] for r in rows])
    cov_pos = descending_positions([r["coverage"] for r in rows])
    shifts = [abs(a - b) for a, b in zip(gci_pos, cov_pos)]
    return {
        "n": len(rows),
        "median": CM.median([float(s) for s in shifts]),
        "p90": quantile([float(s) for s in shifts], 0.90),
        "max": max(shifts) if shifts else float("nan"),
        "exact_rank_kept": sum(1 for s in shifts if s == 0),
        "shifts": shifts,
        "gci_pos": gci_pos,
        "cov_pos": cov_pos,
    }


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--window", type=int, default=CM.WINDOW,
                    help="observation window in characters; 0 reads the stored response")
    ap.add_argument("--days-active", type=int, default=DIAS_PARA_CONSIDERAR_ATIVO,
                    help="recency parameter of the reference implementation")
    ap.add_argument("--until", default=None,
                    help="close the cut at this date (YYYY-MM-DD) instead of the "
                         "last day of the series, to check a published figure")
    ap.add_argument("--min-obs", type=int, default=0,
                    help="third panel rule: minimum observations per arm, the "
                         "undeclared threshold the reference implementation used "
                         "before commit 51159fd; 0 disables it")
    ap.add_argument("--quiet", action="store_true", help="write the CSV files and stop")
    args = ap.parse_args()

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    con = CM.connect()

    cut = " AND date(timestamp) <= ?" if args.until else ""
    lo, hi, n_canonical = con.execute(
        f"SELECT MIN(date(timestamp)), MAX(date(timestamp)), COUNT(*) "
        f"FROM citations WHERE {CM.CANONICAL}{cut}",
        (args.until,) if args.until else ()).fetchone()

    scans = {v: scan_vertical(con, v, args.window, args.until) for v in CM.VERTICALS}
    recency = {v: recency_panel(con, v, args.days_active, args.until)
               for v in CM.VERTICALS}

    identity_checked = sum(s["identity_checked"] for s in scans.values())
    identity_failed = sum(s["identity_failed"] for s in scans.values())

    panels = {
        "series": {v: sorted(scans[v]["obs"]) for v in CM.VERTICALS},
        "recency": {v: sorted(recency[v] & set(scans[v]["obs"])) for v in CM.VERTICALS},
    }
    if args.min_obs:
        panels["min_obs"] = {
            v: sorted(m for m in scans[v]["obs"] if scans[v]["obs"][m] >= args.min_obs)
            for v in CM.VERTICALS}

    panel_rows = []
    for rule, by_vertical in panels.items():
        for v, arms in by_vertical.items():
            panel_rows.append({
                "panel_rule": rule,
                "vertical": v,
                "vertical_label": VERTICAL_LABEL[v],
                "arms": ";".join(arms),
                "n_arms": len(arms),
                "panel_observations": sum(scans[v]["obs"][m] for m in arms),
                "vertical_observations": sum(scans[v]["obs"].values()),
            })

    results = {}
    for rule, by_vertical in panels.items():
        rows = []
        for v in CM.VERTICALS:
            rows.extend(components(scans[v], by_vertical[v]))
        cited = [r for r in rows if r["gci"] > 0]
        cited.sort(key=lambda r: (-r["gci"], r["vertical"], r["entity"]))
        for r in cited:
            r.update(aggregations(r))
        results[rule] = cited

    # --- per-entity components ------------------------------------------------
    comp_rows = []
    for rule, rows in results.items():
        disp = displacement(rows)
        for r, g, c, s in zip(rows, disp["gci_pos"], disp["cov_pos"], disp["shifts"]):
            comp_rows.append({
                "panel_rule": rule, **r,
                "rank_gci": g, "rank_coverage": c, "abs_rank_shift": s,
            })
    write_csv(DATA_DIR / "s6_components.csv",
              ["panel_rule", "vertical", "entity", "mentions", "panel_observations",
               "coverage", "prominence", "breadth", "gci",
               "geometric", "arithmetic", "harmonic", "weighted",
               "rank_gci", "rank_coverage", "abs_rank_shift"], comp_rows)

    # --- Spearman against simple coverage, on the published subsets ------------
    sub_rows = []
    for rule, rows in results.items():
        for r in subset_correlations(rows):
            sub_rows.append({"panel_rule": rule, **r})
    write_csv(DATA_DIR / "s6_spearman_subsets.csv",
              ["panel_rule", "subset", "rho", "n"], sub_rows)

    # --- correlation matrix between the four aggregations ---------------------
    names = ("geometric", "arithmetic", "harmonic", "weighted")
    matrix_rows = []
    for rule, rows in results.items():
        for a in names:
            row = {"panel_rule": rule, "aggregation": a, "n": len(rows)}
            for b in names:
                row[b] = spearman([r[a] for r in rows], [r[b] for r in rows])
            row["against_coverage"] = spearman([r[a] for r in rows],
                                               [r["coverage"] for r in rows])
            matrix_rows.append(row)
    write_csv(DATA_DIR / "s6_aggregation_matrix.csv",
              ["panel_rule", "aggregation", *names, "against_coverage", "n"], matrix_rows)

    # --- variance decomposition of the log index ------------------------------
    var_rows = []
    for rule, rows in results.items():
        for r in variance_decomposition(rows):
            var_rows.append({"panel_rule": rule, "n": len(rows), **r})
    write_csv(DATA_DIR / "s6_variance_decomposition.csv",
              ["panel_rule", "component", "var_log", "contribution", "n"], var_rows)

    # --- rank displacement ----------------------------------------------------
    disp_rows = []
    for rule, rows in results.items():
        d = displacement(rows)
        disp_rows.append({
            "panel_rule": rule, "n": d["n"], "median_abs_shift": d["median"],
            "p90_abs_shift": d["p90"], "max_abs_shift": d["max"],
            "exact_rank_kept": d["exact_rank_kept"],
        })
    write_csv(DATA_DIR / "s6_rank_displacement.csv",
              ["panel_rule", "n", "median_abs_shift", "p90_abs_shift",
               "max_abs_shift", "exact_rank_kept"], disp_rows)

    # --- panel composition ----------------------------------------------------
    write_csv(DATA_DIR / "s6_panel.csv",
              ["panel_rule", "vertical", "vertical_label", "arms", "n_arms",
               "panel_observations", "vertical_observations"], panel_rows)

    # --- provenance -----------------------------------------------------------
    write_csv(DATA_DIR / "s6_run.csv",
              ["key", "value"],
              [{"key": "series_first_day", "value": lo},
               {"key": "series_last_day", "value": hi},
               {"key": "canonical_observations", "value": n_canonical},
               {"key": "window_chars", "value": args.window},
               {"key": "days_active", "value": args.days_active},
               {"key": "min_obs_rule", "value": args.min_obs or "not applied"},
               {"key": "identity_rows_checked", "value": identity_checked},
               {"key": "identity_rows_failed", "value": identity_failed},
               {"key": "cohort", "value": "v2, anchors and decoys included"},
               {"key": "stratum", "value": CM.CANONICAL}])

    if args.quiet:
        con.close()
        return 0 if identity_failed == 0 else 2

    # --- report ---------------------------------------------------------------
    status = "OK  " if identity_failed == 0 else "FAIL"
    print(f"[{status}] re-extraction identity: {identity_failed} mismatches "
          f"in {identity_checked:,} rows stored inside the window")
    print(f"       series {lo} to {hi}, {n_canonical:,} canonical observations, "
          f"window {args.window or 'stored response'} characters")

    for rule in panels:
        rows = results[rule]
        arms = sorted({a for v in CM.VERTICALS for a in panels[rule][v]})
        print(f"\n=== panel rule: {rule} ({len(arms)} arms: {', '.join(arms)}) ===")
        print(f"    entities cited at least once: {len(rows)}")
        print("    Spearman, index against simple coverage")
        for r in subset_correlations(rows):
            print(f"      {r['subset']:<34} rho = {r['rho']:.3f}   n = {r['n']}")
        print("    Variance decomposition of log index")
        for r in variance_decomposition(rows):
            print(f"      {r['component']:<12} Var(log) = {r['var_log']:.3f}   "
                  f"contribution = {100 * r['contribution']:.1f}%")
        print("    Spearman between aggregations")
        print(f"      {'':<12}" + "".join(f"{b:>12}" for b in names) + f"{'coverage':>12}")
        for a in names:
            cells = "".join(
                f"{spearman([r[a] for r in rows], [r[b] for r in rows]):>12.3f}"
                for b in names)
            cells += f"{spearman([r[a] for r in rows], [r['coverage'] for r in rows]):>12.3f}"
            print(f"      {a:<12}{cells}")
        d = displacement(rows)
        print(f"    Rank displacement against coverage: median {d['median']:.0f}, "
              f"p90 {d['p90']:.0f}, max {d['max']}, exact rank kept "
              f"{d['exact_rank_kept']} of {d['n']}")

    con.close()
    print()
    return 0 if identity_failed == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
