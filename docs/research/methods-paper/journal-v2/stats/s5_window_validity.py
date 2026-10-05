#!/usr/bin/env python3
"""s5_window_validity.py — S5: the observation window as a curve, not a number.

WHAT THIS SCRIPT ANSWERS
------------------------
Manuscript v1.0 reports the observation window (BRGEO-1 parameter P1) as a
single contrast: 200 characters against the whole response, measurable on one
arm because five of six client adapters stored `response_text = text[:200]`
and only Perplexity took a path through the client that stored more. Since
2026-08-31 the pipeline writes the response to `citations.response_full_text`
as well, so the contrast can be run inside every active arm, on the same rows,
with the matching rule held fixed.

This script turns that contrast into six measurements:

  S5.1  Sensitivity curve. Citation rate recomputed at 50, 100, 150, 200, 300,
        400, 600, 800, 1,200 and 1,600 characters and on the whole response,
        over the identical observation set, per engine. Reports the saturation
        window under a declared criterion and the 200-to-full difference with
        an exact McNemar p-value and a query-clustered paired bootstrap
        interval.

  S5.2  Mention recovery curve. For every observation that is cited on the
        whole response, the narrowest window that recovers the first mention.
        The quantiles of that distribution answer the adopter's question:
        which window recovers 50, 80, 90 and 95 per cent of the mentions.

  S5.3  Preamble as a predictor (H6). The manuscript proposes that
        susceptibility to a narrow window follows response style rather than
        engine architecture. Tested at three levels — observation, cell and
        engine — against the competing explanation that the window effect is
        simply a function of response length.

  S5.4  Power. Minimum detectable difference per engine and per vertical at the
        N now available, for the paired within-observation comparison and for
        an unpaired comparison, inflated by an empirically measured design
        effect from query clustering.

  S5.5  Matching-rule sensitivity (P6). The same rows re-extracted with the
        alias table on and off and the exclusion contexts on and off, plus a
        variant with the ambiguity guard removed. This quantifies a protocol
        parameter that is declared in the specification but never measured.

  S5.6  Reliability. Even-numbered against odd-numbered collection days, on
        the full-text cohort and on the whole five-month series under a uniform
        200-character window: rates, entity ranking, and the typical error.

WHAT IT REUSES AND WHY
----------------------
The result of the paper is that the matching rule is held fixed while the
window moves. A second extractor written for this analysis would confound the
two, so the cohort comes from `src.config_v2.get_v2_cohort` and the matching
from `src.analysis.entity_extraction.EntityExtractor`, in the configuration
`scripts/harmonize_citation_window.py` used to produce the manuscript's window
table: the v2 cohort with international anchors and fictitious decoys, and the
project's alias, ambiguity, canonical-name and stop-context dictionaries. Those
primitives, the preamble regular expression and the Wilson interval are taken
from `../tables/_common.py`, which is the module the published tables already
use. This script imports that module; it does not copy it and does not modify
it.

Two identity checks run first and are printed with the result. They are the
same two that guard Table 13, restated here because every number below
inherits them:

  1. `response_text` must equal `response_full_text[:200]` on every row used.
  2. Re-extracting `response_full_text[:200]` must reproduce the stored
     `cited_v2` on every row used.

A failure in either means the deltas below are not attributable to the window.

USAGE
-----
    python s5_window_validity.py                # full run, writes CSVs
    python s5_window_validity.py --quick        # smaller bootstrap, skips S5.6b
    python s5_window_validity.py --bootstrap 10000

The database is opened read-only (`mode=ro`). Nothing here writes to it.
Outputs go to `./data/` beside this script and nowhere else.

Author: S5 analyst, journal-v2 statistics pack.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import math
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

# --- stdout as UTF-8: the tables carry accented entity names ---------------
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
else:  # pragma: no cover
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HERE = Path(__file__).resolve().parent
TABLES_DIR = HERE.parent / "tables"
DATA_DIR = HERE / "data"
if str(TABLES_DIR) not in sys.path:
    sys.path.insert(0, str(TABLES_DIR))

import _common as C  # noqa: E402  (path set above)

from src.analysis.entity_extraction import EntityExtractor  # noqa: E402
from src.config import (  # noqa: E402
    AMBIGUOUS_ENTITIES,
    CANONICAL_NAMES,
    ENTITY_ALIASES,
    ENTITY_STOP_CONTEXTS,
)

# ---------------------------------------------------------------------------
# Declared analysis constants. Every threshold used anywhere below is here.
# ---------------------------------------------------------------------------

#: S5.1 grid, in characters. `None` denotes the whole response.
WINDOW_GRID: list[int | None] = [50, 100, 150, 200, 300, 400, 600, 800,
                                 1200, 1600, None]

#: S5.2 grid, finer, for the recovery curve.
RECOVERY_GRID: list[int] = (
    list(range(25, 301, 25))            # 25 … 300 in steps of 25
    + list(range(350, 1001, 50))        # 350 … 1,000 in steps of 50
    + list(range(1100, 2001, 100))      # 1,100 … 2,000 in steps of 100
    + [2250, 2500, 3000, 3500, 4000, 5000]
)

#: S5.1 saturation criterion. A window w is the saturation point when the rate
#: at w is within SATURATION_TOL_PP of the whole-response rate and every wider
#: grid window is too. One percentage point is the resolution at which the
#: manuscript reports rates; the criterion is arbitrary and is stated so that a
#: reader can substitute another from the published CSV.
SATURATION_TOL_PP = 1.0

#: S5.2 recovery levels reported for the adopter.
RECOVERY_LEVELS = (0.50, 0.80, 0.90, 0.95)

#: Bootstrap replicates for the query-clustered paired interval.
BOOTSTRAP_B = 10_000

#: Power targets.
ALPHA = 0.05
POWER = 0.80

#: Cells below this n are descriptive only (matches `_common.SMALL_N`).
SMALL_N = C.SMALL_N

Z_ALPHA_2 = 1.959963984540054
Z_BETA = 0.8416212335729143

#: A stored response is treated as complete when its last non-space character
#: is terminal punctuation or a closing mark. A response that ends anywhere
#: else was cut, either by the generation cap or by the storage path, and its
#: whole-response citation flag is a lower bound rather than a measurement.
#: The criterion is crude and is published so a reader can substitute another:
#: it will call a response ending in a bare list item incomplete, which is why
#: it is reported as a diagnostic and never used to filter a rate.
TERMINAL_RE = __import__("re").compile(
    r"[.!?:;\)\]\"”»’'*_]\s*$")

RNG_SEED = 20260911

ENGINE_ORDER = ("ChatGPT", "Claude", "Gemini", "Grok", "Perplexity")


# ---------------------------------------------------------------------------
# Matching-rule variants for S5.5. `base` is the canonical configuration.
# ---------------------------------------------------------------------------

RULE_VARIANTS: dict[str, dict] = {
    "base": dict(aliases=ENTITY_ALIASES, ambiguous=AMBIGUOUS_ENTITIES,
                 canonical_names=CANONICAL_NAMES,
                 stop_contexts=ENTITY_STOP_CONTEXTS),
    "no_aliases": dict(aliases={}, ambiguous=AMBIGUOUS_ENTITIES,
                       canonical_names=CANONICAL_NAMES,
                       stop_contexts=ENTITY_STOP_CONTEXTS),
    "no_stop_contexts": dict(aliases=ENTITY_ALIASES,
                             ambiguous=AMBIGUOUS_ENTITIES,
                             canonical_names=CANONICAL_NAMES,
                             stop_contexts={}),
    "no_aliases_no_stop": dict(aliases={}, ambiguous=AMBIGUOUS_ENTITIES,
                               canonical_names=CANONICAL_NAMES,
                               stop_contexts={}),
    "no_ambiguity_guard": dict(aliases=ENTITY_ALIASES, ambiguous=set(),
                               canonical_names={},
                               stop_contexts=ENTITY_STOP_CONTEXTS),
}


def build_variant_extractors(variant: str) -> dict[str, EntityExtractor]:
    """One extractor per vertical under a named matching-rule variant."""
    cfg = RULE_VARIANTS[variant]
    return {
        v: EntityExtractor(
            cohort=C.get_v2_cohort(v, include_anchors=True,
                                   include_decoys=True),
            aliases=cfg["aliases"],
            ambiguous=cfg["ambiguous"],
            canonical_names=cfg["canonical_names"],
            stop_contexts=cfg["stop_contexts"],
        )
        for v in C.VERTICALS
    }


# ---------------------------------------------------------------------------
# Small statistics not already in _common
# ---------------------------------------------------------------------------

def wilson_pp(successes: int, n: int) -> tuple[float, float]:
    lo, hi = C.wilson(successes, n)
    return (100 * lo, 100 * hi)


def quantile_of_sorted(values: list[float], q: float) -> float:
    """Smallest value v such that at least q of the sample is <= v.

    The inverse empirical CDF, not an interpolating quantile: the quantity
    asked for is "the window that recovers q of the mentions", and an
    interpolated window is not a window anyone can adopt.
    """
    if not values:
        return float("nan")
    s = sorted(values)
    idx = math.ceil(q * len(s)) - 1
    idx = max(0, min(len(s) - 1, idx))
    return s[idx]


def spearman(a: list[float], b: list[float]) -> tuple[float, float]:
    from scipy import stats
    if len(a) < 3:
        return (float("nan"), float("nan"))
    r = stats.spearmanr(a, b)
    return (float(r.statistic), float(r.pvalue))


def pearson(a: list[float], b: list[float]) -> tuple[float, float]:
    from scipy import stats
    if len(a) < 3:
        return (float("nan"), float("nan"))
    r = stats.pearsonr(a, b)
    return (float(r.statistic), float(r.pvalue))


def fisher_exact_rd(a: int, n_a: int, b: int, n_b: int) -> tuple[float, float]:
    """Risk difference (a/n_a - b/n_b, in pp) and a two-sided Fisher p."""
    from scipy import stats
    if n_a == 0 or n_b == 0:
        return (float("nan"), float("nan"))
    table = [[a, n_a - a], [b, n_b - b]]
    _, p = stats.fisher_exact(table)
    return (100 * (a / n_a - b / n_b), float(p))


def mde_two_proportions(p0: float, n_per_group: int,
                        alpha: float = ALPHA, power: float = POWER) -> float:
    """Minimum detectable difference in pp, two independent proportions.

    Solves the standard normal-approximation sample-size relation for delta
    given n per group. Returns NaN when no delta in (0, 1 - p0] reaches the
    target power, which happens when the arm is too small for any effect the
    scale can contain.
    """
    if n_per_group < 2:
        return float("nan")

    def power_at(delta: float) -> float:
        p1 = min(1.0, p0 + delta)
        pbar = (p0 + p1) / 2
        se0 = math.sqrt(2 * pbar * (1 - pbar) / n_per_group)
        se1 = math.sqrt((p0 * (1 - p0) + p1 * (1 - p1)) / n_per_group)
        if se1 <= 0:
            return 1.0
        from scipy import stats
        z = (delta - Z_ALPHA_2 * se0) / se1
        return float(stats.norm.cdf(z))

    lo, hi = 1e-6, max(1e-6, 1.0 - p0)
    if power_at(hi) < power:
        return float("nan")
    for _ in range(200):
        mid = (lo + hi) / 2
        if power_at(mid) < power:
            lo = mid
        else:
            hi = mid
    return 100 * hi


def mde_mcnemar(n: int, psi: float,
                alpha: float = ALPHA, power: float = POWER) -> float:
    """Minimum detectable paired difference in pp (McNemar, normal form).

    `psi` is the proportion of discordant pairs. Uses the relation
    n = [z_{a/2} sqrt(psi) + z_b sqrt(psi - d^2)]^2 / d^2 and solves for d.
    Returns NaN when psi is zero (no discordance, nothing to detect) or when
    no admissible d reaches the target power.
    """
    if n < 2 or psi <= 0:
        return float("nan")

    def n_needed(d: float) -> float:
        inner = psi - d * d
        if inner <= 0:
            return float("inf")
        return ((Z_ALPHA_2 * math.sqrt(psi) + Z_BETA * math.sqrt(inner)) ** 2
                / (d * d))

    lo, hi = 1e-6, math.sqrt(psi) * 0.999999
    if n_needed(hi) > n:
        return float("nan")
    for _ in range(200):
        mid = (lo + hi) / 2
        if n_needed(mid) > n:
            lo = mid
        else:
            hi = mid
    return 100 * hi


def _cluster_aggregates(clusters: np.ndarray,
                        *series: np.ndarray) -> tuple[int, np.ndarray, list]:
    """Per-cluster sizes and per-cluster sums of each series.

    The cluster bootstrap only ever needs those aggregates, so resampling can
    be a matrix of cluster indices rather than a rebuilt observation vector.
    """
    uniq, inverse = np.unique(clusters, return_inverse=True)
    k = len(uniq)
    sizes = np.bincount(inverse, minlength=k).astype(float)
    sums = [np.bincount(inverse, weights=s.astype(float), minlength=k)
            for s in series]
    return k, sizes, sums


def cluster_bootstrap_paired(y_head: np.ndarray, y_full: np.ndarray,
                             clusters: np.ndarray, b: int,
                             rng: np.random.Generator) -> tuple[float, float, float]:
    """Percentile interval for the paired rate difference, clustering by query.

    Observations that share a query are repeated measurements of the same
    prompt across collection days and are not independent. The interval
    resamples query clusters with replacement; the point estimate reported
    elsewhere is the observed difference, not the bootstrap mean.
    """
    k, sizes, (sh, sf) = _cluster_aggregates(clusters, y_head, y_full)
    idx = rng.integers(0, k, size=(b, k))
    n_b = sizes[idx].sum(axis=1)
    diffs = (sf[idx].sum(axis=1) - sh[idx].sum(axis=1)) / n_b
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    return (100 * float(lo), 100 * float(hi), float(np.std(diffs, ddof=1)))


def cluster_bootstrap_rate_se(y: np.ndarray, clusters: np.ndarray, b: int,
                              rng: np.random.Generator) -> float:
    """Bootstrap standard error of a rate under query clustering."""
    k, sizes, (sy,) = _cluster_aggregates(clusters, y)
    idx = rng.integers(0, k, size=(b, k))
    rates = sy[idx].sum(axis=1) / sizes[idx].sum(axis=1)
    return float(np.std(rates, ddof=1))


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def fmt(x: float, d: int = 1) -> str:
    if x != x:
        return "—"
    return f"{x:.{d}f}"


def fmt_p(p: float) -> str:
    if p != p:
        return "—"
    if p < 1e-300:
        return "<1e-300"
    if p < 0.001:
        return f"{p:.2e}"
    return f"{p:.3f}"


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

FULLTEXT_SQL = """
    SELECT id, timestamp, llm, vertical, query, query_lang, query_type,
           response_text, response_full_text, cited_v2
      FROM citations
     WHERE COALESCE(is_probe,0)=0
       AND response_full_text IS NOT NULL
       AND length(response_full_text) > 0
     ORDER BY id
"""

SERIES_SQL = """
    SELECT id, timestamp, llm, vertical, query, query_lang, query_type,
           response_text
      FROM citations
     WHERE COALESCE(is_probe,0)=0
       AND response_text IS NOT NULL
     ORDER BY id
"""


def load_fulltext_rows(con) -> list:
    return con.execute(FULLTEXT_SQL).fetchall()


# ---------------------------------------------------------------------------
# S5.0 — identity checks
# ---------------------------------------------------------------------------

def identity_checks(rows, extractors) -> dict:
    checks = {"rows": 0, "text_prefix_mismatch": 0, "cited_v2_mismatch": 0}
    for r in rows:
        ext = extractors.get(r["vertical"])
        if ext is None:
            continue
        head = r["response_full_text"][: C.WINDOW]
        if (r["response_text"] or "") != head:
            checks["text_prefix_mismatch"] += 1
        c_head = 1 if ext.extract(head) else 0
        if c_head != (r["cited_v2"] or 0):
            checks["cited_v2_mismatch"] += 1
        checks["rows"] += 1
    checks["pass"] = (checks["text_prefix_mismatch"] == 0
                      and checks["cited_v2_mismatch"] == 0)
    return checks


# ---------------------------------------------------------------------------
# S5.1 + S5.2 — the extraction pass over the window grid
# ---------------------------------------------------------------------------

def _cache_load(cache_dir: Path | None, tag: str, n: int):
    if not cache_dir:
        return None
    f = cache_dir / f"s5_{tag}_{n}.npz"
    if not f.exists():
        return None
    z = np.load(f, allow_pickle=True)
    return {k: z[k] for k in z.files}


def _cache_save(cache_dir: Path | None, tag: str, n: int, pack: dict) -> None:
    if not cache_dir:
        return
    cache_dir.mkdir(parents=True, exist_ok=True)
    np.savez(cache_dir / f"s5_{tag}_{n}.npz",
             **{k: np.asarray(v) for k, v in pack.items()})


def extract_over_grid(rows, extractors, grid: list[int]) -> dict:
    """Extract once per row per grid window, plus once over the whole response.

    Returns per-row arrays. A window wider than the stored response reproduces
    the whole-response extraction by construction, so it is not recomputed:
    the saving is what makes the fine grid of S5.2 affordable.
    """
    n = len(rows)
    grid_sorted = sorted(set(grid))
    cited_grid = np.zeros((n, len(grid_sorted)), dtype=np.int8)
    cited_full = np.zeros(n, dtype=np.int8)
    count_full = np.zeros(n, dtype=np.int16)
    first_offset_full = np.full(n, -1, dtype=np.int32)
    len_full = np.zeros(n, dtype=np.int32)

    for i, r in enumerate(rows):
        ext = extractors[r["vertical"]]
        full = r["response_full_text"]
        len_full[i] = len(full)
        m_full = ext.extract(full)
        cited_full[i] = 1 if m_full else 0
        count_full[i] = len(m_full)
        if m_full:
            first_offset_full[i] = m_full[0].start
        for j, w in enumerate(grid_sorted):
            if w >= len(full):
                cited_grid[i, j] = cited_full[i]
            else:
                cited_grid[i, j] = 1 if ext.extract(full[:w]) else 0

    return {
        "grid": grid_sorted,
        "cited_grid": cited_grid,
        "cited_full": cited_full,
        "count_full": count_full,
        "first_offset_full": first_offset_full,
        "len_full": len_full,
    }


def saturation_window(rates: dict[int, float], rate_full: float,
                      grid: list[int], tol: float = SATURATION_TOL_PP):
    """Smallest grid window at which the rate is within `tol` of the full rate
    and stays there for every wider grid window."""
    for i, w in enumerate(grid):
        if all(rate_full - rates[g] <= tol for g in grid[i:]):
            return w
    return None


def analyse_window_curve(rows, pack, bootstrap_b: int, rng) -> dict:
    engines = sorted({r["llm"] for r in rows}, key=lambda e: (
        ENGINE_ORDER.index(e) if e in ENGINE_ORDER else 99, e))
    grid = pack["grid"]
    cited_grid = pack["cited_grid"]
    cited_full = pack["cited_full"]
    len_full = pack["len_full"]
    queries = np.array([r["query"] for r in rows])
    llms = np.array([r["llm"] for r in rows])
    verts = np.array([r["vertical"] for r in rows])

    idx200 = grid.index(C.WINDOW)

    per_engine: dict[str, dict] = {}
    for e in engines:
        m = llms == e
        n = int(m.sum())
        y_full = cited_full[m]
        rates = {w: 100 * cited_grid[m, j].mean() for j, w in enumerate(grid)}
        ci = {w: wilson_pp(int(cited_grid[m, j].sum()), n)
              for j, w in enumerate(grid)}
        rate_full = 100 * y_full.mean()
        ci_full = wilson_pp(int(y_full.sum()), n)

        y200 = cited_grid[m, idx200]
        gain = int(((y_full == 1) & (y200 == 0)).sum())
        loss = int(((y_full == 0) & (y200 == 1)).sum())
        mcnemar_p = C.exact_binomial_two_sided(gain, loss)
        bs_lo, bs_hi, bs_sd = cluster_bootstrap_paired(
            y200.astype(float), y_full.astype(float), queries[m],
            bootstrap_b, rng)
        # Independence-assuming standard error of the paired difference:
        # Var(p_full - p_head) = [b + c - (b - c)^2 / n] / n^2. The cruder
        # sqrt(b + c)/n overstates it whenever the discordance is one-sided,
        # which it is on every arm here, and would leave an apparent design
        # effect below one where there is no clustering at all.
        var_naive = max(gain + loss - (gain - loss) ** 2 / n, 0.0) / (n * n)
        naive_se = 100 * math.sqrt(var_naive)
        sat = saturation_window(rates, rate_full, grid)
        w95 = next((w for w in grid
                    if rate_full > 0 and rates[w] >= 0.95 * rate_full), None)

        per_engine[e] = {
            "n": n,
            "n_queries": int(len(set(queries[m].tolist()))),
            "dates": sorted({r["timestamp"][:10] for r in rows
                             if r["llm"] == e}),
            "rates": rates,
            "rate_ci": ci,
            "cited_counts": {w: int(cited_grid[m, j].sum())
                             for j, w in enumerate(grid)},
            "rate_full": rate_full,
            "rate_full_ci": ci_full,
            "cited_full": int(y_full.sum()),
            "delta_200_full_pp": rate_full - rates[C.WINDOW],
            "mcnemar_gain": gain,
            "mcnemar_loss": loss,
            "mcnemar_p": mcnemar_p,
            "boot_ci_pp": [bs_lo, bs_hi],
            "boot_sd_pp": 100 * bs_sd,
            "mcnemar_se_pp": naive_se,
            "design_effect": ((100 * bs_sd) / naive_se) ** 2
                             if naive_se > 0 else float("nan"),
            "saturation_window": sat,
            "window_95pct_of_full": w95,
            "median_len_full": float(np.median(len_full[m])),
            "mean_len_full": float(len_full[m].mean()),
            "rows_longer_than_200": int((len_full[m] > C.WINDOW).sum()),
        }

    # Pooled across engines, and per engine x vertical.
    per_cell: list[dict] = []
    for e in engines:
        for v in C.VERTICALS:
            m = (llms == e) & (verts == v)
            n = int(m.sum())
            if n == 0:
                continue
            row = {"engine": e, "vertical": v, "vertical_label":
                   C.VERTICAL_LABEL[v], "n": n}
            for j, w in enumerate(grid):
                key = "full" if w is None else str(w)
                row[f"rate_{key}"] = 100 * cited_grid[m, j].mean()
            row["rate_full"] = 100 * cited_full[m].mean()
            row["delta_200_full_pp"] = row["rate_full"] - row[f"rate_{C.WINDOW}"]
            per_cell.append(row)

    return {"per_engine": per_engine, "per_cell": per_cell, "grid": grid,
            "engines": engines}


# ---------------------------------------------------------------------------
# S5.2 — mention recovery
# ---------------------------------------------------------------------------

def analyse_recovery(rows, pack_fine) -> dict:
    """Narrowest window that recovers the first mention, per observation.

    Defined on the monotone envelope: the smallest grid window from which the
    observation is cited at that window and at every wider one. The envelope
    matters because the rule is not monotone in principle — an exclusion
    context reaches thirty characters past a match, so widening the window can
    in rare cases remove a match that a narrower window kept. The count of
    such non-monotone observations is reported rather than hidden.
    """
    grid = pack_fine["grid"]
    cited_grid = pack_fine["cited_grid"]
    cited_full = pack_fine["cited_full"]
    llms = np.array([r["llm"] for r in rows])
    n = len(rows)

    needed = np.full(n, -1, dtype=np.int32)   # -1 = only the whole response
    non_monotone = 0
    for i in range(n):
        if not cited_full[i]:
            continue
        row = cited_grid[i]
        # monotone envelope from the right
        ok_from = len(grid)
        for j in range(len(grid) - 1, -1, -1):
            if row[j] == 1:
                ok_from = j
            else:
                break
        if ok_from < len(grid):
            needed[i] = grid[ok_from]
        if row.sum() > 0 and ok_from == len(grid):
            non_monotone += 1
        elif ok_from < len(grid) and row[:ok_from].sum() > 0:
            non_monotone += 1

    engines = sorted(set(llms.tolist()), key=lambda e: (
        ENGINE_ORDER.index(e) if e in ENGINE_ORDER else 99, e))

    curves: list[dict] = []
    quantiles: dict[str, dict] = {}
    for e in engines:
        m = (llms == e) & (cited_full == 1)
        base = int(m.sum())
        if base == 0:
            continue
        for j, w in enumerate(grid):
            rec = cited_grid[m, j].mean()
            curves.append({"engine": e, "window_chars": w,
                           "cited_at_window": int(cited_grid[m, j].sum()),
                           "cited_on_full": base,
                           "recovery_fraction": float(rec),
                           "recovery_pct": 100 * float(rec)})
        curves.append({"engine": e, "window_chars": "full",
                       "cited_at_window": base, "cited_on_full": base,
                       "recovery_fraction": 1.0, "recovery_pct": 100.0})
        vals = [float(x) if x > 0 else float(grid[-1] + 1)
                for x in needed[m]]
        quantiles[e] = {
            "n_cited_on_full": base,
            "beyond_grid": int((needed[m] <= 0).sum()),
            **{f"w{int(100*q)}": quantile_of_sorted(vals, q)
               for q in RECOVERY_LEVELS},
            "median_first_offset_full":
                float(np.median(pack_fine["first_offset_full"][m])),
        }

    # pooled
    m = cited_full == 1
    base = int(m.sum())
    for j, w in enumerate(grid):
        curves.append({"engine": "ALL", "window_chars": w,
                       "cited_at_window": int(cited_grid[m, j].sum()),
                       "cited_on_full": base,
                       "recovery_fraction": float(cited_grid[m, j].mean()),
                       "recovery_pct": 100 * float(cited_grid[m, j].mean())})
    curves.append({"engine": "ALL", "window_chars": "full",
                   "cited_at_window": base, "cited_on_full": base,
                   "recovery_fraction": 1.0, "recovery_pct": 100.0})
    vals = [float(x) if x > 0 else float(grid[-1] + 1) for x in needed[m]]
    quantiles["ALL"] = {
        "n_cited_on_full": base,
        "beyond_grid": int((needed[m] <= 0).sum()),
        **{f"w{int(100*q)}": quantile_of_sorted(vals, q)
           for q in RECOVERY_LEVELS},
        "median_first_offset_full":
            float(np.median(pack_fine["first_offset_full"][m])),
    }

    return {"curves": curves, "quantiles": quantiles,
            "non_monotone_rows": non_monotone, "needed": needed}


# ---------------------------------------------------------------------------
# S5.1b — the same contrast on observations the window can actually bind on,
#          and the per-day breakdown that explains why the restriction matters
# ---------------------------------------------------------------------------

def analyse_restricted_and_daily(rows, pack, pack_fine, needed) -> dict:
    """Two views that keep the pooled curve from being read as more than it is.

    An observation whose stored response is 200 characters or shorter cannot
    move between the 200-character window and the whole response: the two
    windows see the same string. Such rows are not noise, they are real
    observations, but they dilute the pooled delta by an amount that depends on
    how many of them an arm happens to contribute on a given day. Gemini
    contributes 378 of them from 2026-09-06 alone, where the responses the API
    returned were themselves cut mid-sentence at a mean of 143 characters.

    The restricted view drops those rows. The daily view shows where they came
    from, so a reader can see that the restriction is a property of one
    collection day and not a filter chosen to flatter the result.
    """
    grid = pack["grid"]
    idx200 = grid.index(C.WINDOW)
    llms = np.array([r["llm"] for r in rows])
    days = np.array([r["timestamp"][:10] for r in rows])
    len_full = pack["len_full"]
    y200 = pack["cited_grid"][:, idx200].astype(int)
    yfull = pack["cited_full"].astype(int)
    fine_grid = pack_fine["grid"]

    engines = sorted(set(llms.tolist()), key=lambda e: (
        ENGINE_ORDER.index(e) if e in ENGINE_ORDER else 99, e))

    restricted = []
    for e in engines:
        m = (llms == e) & (len_full > C.WINDOW)
        n = int(m.sum())
        if n == 0:
            continue
        gain = int(((yfull[m] == 1) & (y200[m] == 0)).sum())
        loss = int(((yfull[m] == 0) & (y200[m] == 1)).sum())
        cited_full_m = m & (pack["cited_full"] == 1)
        vals = [float(x) if x > 0 else float(fine_grid[-1] + 1)
                for x in needed[cited_full_m]]
        row = {
            "engine": e,
            "n_all": int((llms == e).sum()),
            "n_longer_than_window": n,
            "dropped_short_rows": int((llms == e).sum()) - n,
            "rate_200_pct": 100 * float(y200[m].mean()),
            "rate_full_pct": 100 * float(yfull[m].mean()),
            "delta_pp": 100 * float(yfull[m].mean() - y200[m].mean()),
            "mcnemar_gain": gain, "mcnemar_loss": loss,
            "mcnemar_p": C.exact_binomial_two_sided(gain, loss),
            "median_len_full": float(np.median(len_full[m])),
            "n_cited_on_full": int(cited_full_m.sum()),
        }
        for q in RECOVERY_LEVELS:
            row[f"w{int(100*q)}"] = quantile_of_sorted(vals, q)
        restricted.append(row)

    complete = np.array([1 if TERMINAL_RE.search(r["response_full_text"]) else 0
                         for r in rows], dtype=np.int8)

    daily = []
    for e in engines:
        for d in sorted(set(days[llms == e].tolist())):
            m = (llms == e) & (days == d)
            n = int(m.sum())
            daily.append({
                "engine": e, "day": d, "n": n,
                "mean_len_full": float(len_full[m].mean()),
                "median_len_full": float(np.median(len_full[m])),
                "rows_at_or_below_window": int((len_full[m] <= C.WINDOW).sum()),
                "rate_200_pct": 100 * float(y200[m].mean()),
                "rate_full_pct": 100 * float(yfull[m].mean()),
                "delta_pp": 100 * float(yfull[m].mean() - y200[m].mean()),
                "ends_without_terminal_punctuation_pct":
                    100 * float(1 - complete[m].mean()),
            })

    # Censoring diagnostic: a stored response that ends mid-sentence is not the
    # whole response, so the whole-response rate computed on it is a lower
    # bound. This is reported, never used to filter.
    censoring = []
    for e in engines:
        m = llms == e
        censoring.append({
            "engine": e, "n": int(m.sum()),
            "ends_without_terminal_punctuation": int((1 - complete[m]).sum()),
            "ends_without_terminal_punctuation_pct":
                100 * float(1 - complete[m].mean()),
            "max_len_full": int(len_full[m].max()),
            "p95_len_full": float(np.percentile(len_full[m], 95)),
        })
    return {"restricted": restricted, "daily": daily, "censoring": censoring}


# ---------------------------------------------------------------------------
# S5.3 — preamble as a predictor (H6)
# ---------------------------------------------------------------------------

def analyse_preamble(rows, pack, curve) -> dict:
    import pandas as pd
    import statsmodels.api as sm
    import statsmodels.formula.api as smf

    grid = pack["grid"]
    idx200 = grid.index(C.WINDOW)
    df = pd.DataFrame({
        "engine": [r["llm"] for r in rows],
        "vertical": [r["vertical"] for r in rows],
        "lang": [r["query_lang"] for r in rows],
        "qtype": [r["query_type"] for r in rows],
        "query": [r["query"] for r in rows],
        "day": [r["timestamp"][:10] for r in rows],
        "preamble": [int(C.opens_with_preamble(r["response_full_text"]))
                     for r in rows],
        "len_full": pack["len_full"],
        "cited_200": pack["cited_grid"][:, idx200].astype(int),
        "cited_full": pack["cited_full"].astype(int),
        "first_offset": pack["first_offset_full"].astype(float),
    })
    df["log_len"] = np.log10(df["len_full"].clip(lower=1))
    df["recovered_only_by_width"] = (
        (df["cited_full"] == 1) & (df["cited_200"] == 0)).astype(int)
    df["log_offset"] = np.log10(df["first_offset"].clip(lower=1))

    out: dict = {}

    # --- engine-level -----------------------------------------------------
    eng_rows = []
    for e, d in df.groupby("engine"):
        pe = curve["per_engine"][e]
        eng_rows.append({
            "engine": e, "n": len(d),
            "preamble_n": int(d["preamble"].sum()),
            "preamble_share_pct": 100 * float(d["preamble"].mean()),
            "preamble_ci_lo": wilson_pp(int(d["preamble"].sum()), len(d))[0],
            "preamble_ci_hi": wilson_pp(int(d["preamble"].sum()), len(d))[1],
            "delta_200_full_pp": pe["delta_200_full_pp"],
            "mean_len_full": float(d["len_full"].mean()),
            "median_len_full": float(d["len_full"].median()),
            "median_first_offset": float(
                d.loc[d["cited_full"] == 1, "first_offset"].median()),
            "engine_class": C.ENGINE_CLASS.get(e, "?"),
        })
    eng_rows.sort(key=lambda r: (ENGINE_ORDER.index(r["engine"])
                                 if r["engine"] in ENGINE_ORDER else 99))
    out["engine_level"] = eng_rows
    sh = [r["preamble_share_pct"] for r in eng_rows]
    dl = [r["delta_200_full_pp"] for r in eng_rows]
    ln = [r["median_len_full"] for r in eng_rows]
    of = [r["median_first_offset"] for r in eng_rows]
    out["engine_level_tests"] = {
        "n_engines": len(eng_rows),
        "spearman_preamble_vs_delta": spearman(sh, dl),
        "spearman_medianlen_vs_delta": spearman(ln, dl),
        "spearman_offset_vs_delta": spearman(of, dl),
        "pearson_preamble_vs_delta": pearson(sh, dl),
    }

    # The same engine-level test on observations the window can bind on. The
    # pooled Gemini row mixes a day whose stored responses were themselves cut
    # at 143 characters with two days of three-thousand-character responses, so
    # its pooled preamble share and its pooled delta both describe a mixture
    # rather than an engine. H6 is a claim about engines, so it gets the
    # restricted test as well as the pooled one.
    rdf = df[df["len_full"] > C.WINDOW]
    r_rows = []
    for e, d in rdf.groupby("engine"):
        r_rows.append({
            "engine": e, "n": len(d),
            "preamble_share_pct": 100 * float(d["preamble"].mean()),
            "delta_pp": 100 * float(d["cited_full"].mean()
                                    - d["cited_200"].mean()),
            "median_len_full": float(d["len_full"].median()),
            "median_first_offset": float(
                d.loc[d["cited_full"] == 1, "first_offset"].median()),
        })
    r_rows.sort(key=lambda r: (ENGINE_ORDER.index(r["engine"])
                               if r["engine"] in ENGINE_ORDER else 99))
    out["engine_level_restricted"] = r_rows
    out["engine_level_restricted_tests"] = {
        "n_engines": len(r_rows),
        "spearman_preamble_vs_delta": spearman(
            [r["preamble_share_pct"] for r in r_rows],
            [r["delta_pp"] for r in r_rows]),
        "spearman_medianlen_vs_delta": spearman(
            [r["median_len_full"] for r in r_rows],
            [r["delta_pp"] for r in r_rows]),
        "spearman_offset_vs_delta": spearman(
            [r["median_first_offset"] for r in r_rows],
            [r["delta_pp"] for r in r_rows]),
    }

    # --- cell level (engine x vertical x language) -------------------------
    cell_rows = []
    for (e, v, lg), d in df.groupby(["engine", "vertical", "lang"]):
        n = len(d)
        cell_rows.append({
            "engine": e, "vertical": v, "lang": lg, "n": n,
            "preamble_share_pct": 100 * float(d["preamble"].mean()),
            "rate_200_pct": 100 * float(d["cited_200"].mean()),
            "rate_full_pct": 100 * float(d["cited_full"].mean()),
            "delta_pp": 100 * float(d["cited_full"].mean()
                                    - d["cited_200"].mean()),
            "mean_log_len": float(d["log_len"].mean()),
            "small_n": int(n < SMALL_N),
        })
    out["cell_level"] = cell_rows

    # Model frame at engine x vertical. The finer engine x vertical x language
    # cell has n = 24 for ChatGPT and Claude, below the descriptive-only
    # threshold, so fitting on it would silently drop both parametric arms with
    # no preamble — the two observations the hypothesis most needs.
    model_cells = []
    for (e, v), d in df.groupby(["engine", "vertical"]):
        n = len(d)
        model_cells.append({
            "engine": e, "vertical": v, "n": n,
            "preamble_share_pct": 100 * float(d["preamble"].mean()),
            "delta_pp": 100 * float(d["cited_full"].mean()
                                    - d["cited_200"].mean()),
            "mean_log_len": float(d["log_len"].mean()),
        })
    out["model_cells"] = model_cells
    cdf = pd.DataFrame(model_cells)
    cdf = cdf[cdf["n"] >= SMALL_N]
    models: dict = {}
    if len(cdf) >= 6:
        m1 = smf.ols("delta_pp ~ preamble_share_pct", data=cdf).fit(
            cov_type="cluster", cov_kwds={"groups": cdf["engine"]})
        models["cell_preamble_only"] = _model_summary(m1, "preamble_share_pct")
        m2 = smf.ols("delta_pp ~ preamble_share_pct + mean_log_len",
                     data=cdf).fit(cov_type="cluster",
                                   cov_kwds={"groups": cdf["engine"]})
        models["cell_preamble_plus_length"] = _model_summary(
            m2, "preamble_share_pct")
        models["cell_length_in_joint"] = _model_summary(m2, "mean_log_len")
        cfe, fe_names = _engine_dummies(cdf)
        if fe_names:
            m3 = smf.ols("delta_pp ~ preamble_share_pct + "
                         + " + ".join(fe_names), data=cfe).fit(cov_type="HC1")
            models["cell_preamble_engine_fe"] = _model_summary(
                m3, "preamble_share_pct")
            m4 = smf.ols("delta_pp ~ preamble_share_pct + mean_log_len + "
                         + " + ".join(fe_names), data=cfe).fit(cov_type="HC1")
            models["cell_preamble_engine_fe_plus_length"] = _model_summary(
                m4, "preamble_share_pct")
            models["cell_length_engine_fe"] = _model_summary(
                m4, "mean_log_len")
        models["cell_n"] = int(len(cdf))
        models["cell_reference_engine"] = sorted(cdf["engine"].unique())[0]
    out["cell_models"] = models

    # --- observation level -------------------------------------------------
    # Among observations cited on the whole response, is the narrow window's
    # miss predicted by the preamble, once length is controlled?
    sub = df[df["cited_full"] == 1].copy()
    obs: dict = {"n": int(len(sub)),
                 "engines_with_preamble_variation": []}
    for e, d in sub.groupby("engine"):
        if 0 < d["preamble"].mean() < 1:
            obs["engines_with_preamble_variation"].append(e)

    try:
        mA = smf.glm("recovered_only_by_width ~ preamble",
                     data=sub, family=sm.families.Binomial()).fit(
            cov_type="cluster", cov_kwds={"groups": sub["query"]})
        obs["pooled_preamble_only"] = _model_summary(mA, "preamble", odds=True)
    except Exception as exc:                       # pragma: no cover
        obs["pooled_preamble_only"] = {"error": str(exc)}
    try:
        mB = smf.glm("recovered_only_by_width ~ preamble + log_len",
                     data=sub, family=sm.families.Binomial()).fit(
            cov_type="cluster", cov_kwds={"groups": sub["query"]})
        obs["pooled_preamble_plus_length"] = _model_summary(
            mB, "preamble", odds=True)
        obs["pooled_length_in_joint"] = _model_summary(mB, "log_len", odds=True)
    except Exception as exc:                       # pragma: no cover
        obs["pooled_preamble_plus_length"] = {"error": str(exc)}

    sub_var = sub[sub["engine"].isin(obs["engines_with_preamble_variation"])]
    if len(sub_var) > 30 and sub_var["engine"].nunique() >= 2:
        try:
            svfe, fe_names = _engine_dummies(sub_var)
            formula = ("recovered_only_by_width ~ preamble + log_len"
                       + ("" if not fe_names else " + " + " + ".join(fe_names)))
            mC = smf.glm(formula, data=svfe,
                         family=sm.families.Binomial()).fit(
                cov_type="cluster", cov_kwds={"groups": svfe["query"]})
            obs["within_engine_fe"] = _model_summary(mC, "preamble", odds=True)
            obs["within_engine_fe_n"] = int(len(sub_var))
            obs["within_engine_fe_engines"] = sorted(
                sub_var["engine"].unique())
        except Exception as exc:                   # pragma: no cover
            obs["within_engine_fe"] = {"error": str(exc)}

    # per-engine contrast, model-free
    per_engine_contrast = []
    for e, d in sub.groupby("engine"):
        a = d[d["preamble"] == 1]
        b = d[d["preamble"] == 0]
        rd, p = fisher_exact_rd(int(a["recovered_only_by_width"].sum()), len(a),
                                int(b["recovered_only_by_width"].sum()), len(b))
        per_engine_contrast.append({
            "engine": e,
            "n_cited_full": len(d),
            "n_preamble": len(a), "n_no_preamble": len(b),
            "miss_rate_preamble_pct": 100 * float(a["recovered_only_by_width"].mean())
                if len(a) else float("nan"),
            "miss_rate_no_preamble_pct": 100 * float(b["recovered_only_by_width"].mean())
                if len(b) else float("nan"),
            "risk_difference_pp": rd, "fisher_p": p,
        })
    per_engine_contrast.sort(key=lambda r: (ENGINE_ORDER.index(r["engine"])
                                            if r["engine"] in ENGINE_ORDER else 99))
    obs["per_engine_contrast"] = per_engine_contrast

    # --- mechanism: does the preamble push the first mention later? --------
    mech = {}
    cited = df[(df["cited_full"] == 1) & (df["first_offset"] >= 0)].copy()
    try:
        cfe2, fe2 = _engine_dummies(cited)
        mD = smf.ols("log_offset ~ preamble + log_len"
                     + ("" if not fe2 else " + " + " + ".join(fe2)),
                     data=cfe2).fit(cov_type="cluster",
                                    cov_kwds={"groups": cfe2["query"]})
        mech["offset_model"] = _model_summary(mD, "preamble")
        mech["offset_model_length"] = _model_summary(mD, "log_len")
        mech["offset_model_n"] = int(len(cited))
        # The coefficient is on log10 of the offset, so exponentiating gives
        # the multiplicative shift in the position of the first mention.
        mech["offset_multiplier_preamble"] = float(
            10 ** mech["offset_model"]["coef"])
        mech["offset_multiplier_preamble_ci"] = [
            float(10 ** mech["offset_model"]["ci_lo"]),
            float(10 ** mech["offset_model"]["ci_hi"])]
    except Exception as exc:                       # pragma: no cover
        mech["offset_model"] = {"error": str(exc)}
    from scipy import stats as sps
    per_engine_offset = []
    for e, d in cited.groupby("engine"):
        a = d[d["preamble"] == 1]["first_offset"]
        b = d[d["preamble"] == 0]["first_offset"]
        if len(a) >= 5 and len(b) >= 5:
            u = sps.mannwhitneyu(a, b, alternative="two-sided")
            per_engine_offset.append({
                "engine": e, "n_preamble": len(a), "n_no_preamble": len(b),
                "median_offset_preamble": float(a.median()),
                "median_offset_no_preamble": float(b.median()),
                "mannwhitney_u": float(u.statistic), "p": float(u.pvalue)})
        else:
            per_engine_offset.append({
                "engine": e, "n_preamble": len(a), "n_no_preamble": len(b),
                "median_offset_preamble": float(a.median()) if len(a) else float("nan"),
                "median_offset_no_preamble": float(b.median()) if len(b) else float("nan"),
                "mannwhitney_u": float("nan"), "p": float("nan")})
    mech["per_engine_offset"] = per_engine_offset
    out["mechanism"] = mech
    out["observation_level"] = obs
    out["_frame"] = df
    return out


def _engine_dummies(df, column: str = "engine") -> tuple[object, list[str]]:
    """Explicit engine fixed effects as named columns.

    Written out rather than expressed with patsy's `C()` because this module
    binds the name `C` to `_common`, and patsy evaluates formula factors in the
    calling module's namespace. Dropping the first level in sorted order fixes
    the reference engine deterministically across runs.
    """
    levels = sorted(df[column].unique())
    names = []
    out = df.copy()
    for lv in levels[1:]:
        col = "fe_" + "".join(ch if ch.isalnum() else "_" for ch in lv)
        out[col] = (out[column] == lv).astype(float)
        names.append(col)
    return out, names


def _model_summary(fit, term: str, odds: bool = False) -> dict:
    """Coefficient, robust SE, interval and p for one term of a fitted model."""
    if term not in fit.params.index:
        matches = [t for t in fit.params.index if t.startswith(term)]
        if not matches:
            return {"error": f"term {term} not in model"}
        term = matches[0]
    ci = fit.conf_int().loc[term]
    d = {
        "term": term,
        "coef": float(fit.params[term]),
        "se": float(fit.bse[term]),
        "ci_lo": float(ci[0]), "ci_hi": float(ci[1]),
        "p": float(fit.pvalues[term]),
        "n": int(fit.nobs),
    }
    if odds:
        d["odds_ratio"] = float(np.exp(d["coef"]))
        d["or_ci_lo"] = float(np.exp(d["ci_lo"]))
        d["or_ci_hi"] = float(np.exp(d["ci_hi"]))
    if hasattr(fit, "rsquared"):
        d["r2"] = float(fit.rsquared)
    return d


# ---------------------------------------------------------------------------
# S5.4 — power
# ---------------------------------------------------------------------------

def analyse_power(rows, pack, curve, bootstrap_b: int, rng) -> dict:
    grid = pack["grid"]
    idx200 = grid.index(C.WINDOW)
    llms = np.array([r["llm"] for r in rows])
    verts = np.array([r["vertical"] for r in rows])
    queries = np.array([r["query"] for r in rows])
    y200 = pack["cited_grid"][:, idx200].astype(float)
    yfull = pack["cited_full"].astype(float)

    def block(mask, label_fields: dict) -> dict:
        n = int(mask.sum())
        if n == 0:
            return {}
        p200 = float(y200[mask].mean())
        pfull = float(yfull[mask].mean())
        disc = float(((y200[mask] != yfull[mask])).mean())
        se_cluster = cluster_bootstrap_rate_se(
            yfull[mask], queries[mask], min(bootstrap_b, 4000), rng)
        se_naive = math.sqrt(max(pfull * (1 - pfull), 1e-12) / n)
        deff = (se_cluster / se_naive) ** 2 if se_naive > 0 else float("nan")
        mde_paired = mde_mcnemar(n, disc)
        mde_unpaired = mde_two_proportions(pfull, n)
        return {
            **label_fields,
            "n": n,
            "n_queries": int(len(set(queries[mask].tolist()))),
            "rate_200_pct": 100 * p200,
            "rate_full_pct": 100 * pfull,
            "discordant_share_pct": 100 * disc,
            "design_effect": deff,
            "effective_n": n / deff if deff == deff and deff > 0 else float("nan"),
            "mde_paired_pp": mde_paired,
            "mde_paired_pp_clustered": (mde_paired * math.sqrt(deff)
                                        if deff == deff else float("nan")),
            "mde_unpaired_pp": mde_unpaired,
            "mde_unpaired_pp_clustered": (mde_unpaired * math.sqrt(deff)
                                          if deff == deff else float("nan")),
            "small_n": int(n < SMALL_N),
        }

    per_engine = [block(llms == e, {"stratum": "engine", "label": e})
                  for e in curve["engines"]]
    per_vertical = [block(verts == v,
                          {"stratum": "vertical",
                           "label": C.VERTICAL_LABEL[v]})
                    for v in C.VERTICALS]
    per_engine_vertical = []
    for e in curve["engines"]:
        for v in C.VERTICALS:
            b = block((llms == e) & (verts == v),
                      {"stratum": "engine x vertical",
                       "label": f"{e} / {C.VERTICAL_LABEL[v]}"})
            if b:
                per_engine_vertical.append(b)
    overall = block(np.ones(len(rows), dtype=bool),
                    {"stratum": "all", "label": "all engines"})
    return {"per_engine": [b for b in per_engine if b],
            "per_vertical": [b for b in per_vertical if b],
            "per_engine_vertical": per_engine_vertical,
            "overall": overall}


# ---------------------------------------------------------------------------
# S5.5 — matching-rule sensitivity (P6)
# ---------------------------------------------------------------------------

def analyse_matching_rule(rows) -> dict:
    llms = np.array([r["llm"] for r in rows])
    engines = sorted(set(llms.tolist()), key=lambda e: (
        ENGINE_ORDER.index(e) if e in ENGINE_ORDER else 99, e))

    results: dict[str, dict] = {}
    per_row: dict[str, dict[str, np.ndarray]] = {}
    for variant in RULE_VARIANTS:
        ext = build_variant_extractors(variant)
        c200 = np.zeros(len(rows), dtype=np.int8)
        cfull = np.zeros(len(rows), dtype=np.int8)
        n200 = np.zeros(len(rows), dtype=np.int16)
        nfull = np.zeros(len(rows), dtype=np.int16)
        for i, r in enumerate(rows):
            e = ext[r["vertical"]]
            full = r["response_full_text"]
            m_h = e.extract(full[: C.WINDOW])
            m_f = e.extract(full)
            c200[i] = 1 if m_h else 0
            cfull[i] = 1 if m_f else 0
            n200[i] = len(m_h)
            nfull[i] = len(m_f)
        per_row[variant] = {"c200": c200, "cfull": cfull,
                            "n200": n200, "nfull": nfull}

    base = per_row["base"]
    table: list[dict] = []
    for variant in RULE_VARIANTS:
        d = per_row[variant]
        for scope, mask in ([("ALL", np.ones(len(rows), dtype=bool))]
                            + [(e, llms == e) for e in engines]):
            n = int(mask.sum())
            table.append({
                "variant": variant,
                "engine": scope,
                "n": n,
                "rate_200_pct": 100 * float(d["c200"][mask].mean()),
                "rate_full_pct": 100 * float(d["cfull"][mask].mean()),
                "delta_vs_base_200_pp": 100 * float(
                    d["c200"][mask].mean() - base["c200"][mask].mean()),
                "delta_vs_base_full_pp": 100 * float(
                    d["cfull"][mask].mean() - base["cfull"][mask].mean()),
                "flipped_rows_200": int((d["c200"][mask]
                                         != base["c200"][mask]).sum()),
                "flipped_rows_full": int((d["cfull"][mask]
                                          != base["cfull"][mask]).sum()),
                "mean_entities_full": float(d["nfull"][mask].mean()),
                "mean_entities_full_delta_vs_base": float(
                    d["nfull"][mask].mean() - base["nfull"][mask].mean()),
                "window_effect_200_to_full_pp": 100 * float(
                    d["cfull"][mask].mean() - d["c200"][mask].mean()),
            })
    results["table"] = table

    # How much of the rule actually binds on this cohort: the count of cohort
    # entities each dictionary reaches. A parameter that touches no entity
    # cannot move a rate, and saying so is part of the measurement.
    binding = []
    for v in C.VERTICALS:
        coh = C.get_v2_cohort(v, True, True)
        binding.append({
            "vertical": v,
            "cohort_size": len(coh),
            "entities_with_alias": sum(1 for e in coh if e in ENTITY_ALIASES),
            "alias_surfaces": sum(len(ENTITY_ALIASES[e]) for e in coh
                                  if e in ENTITY_ALIASES),
            "entities_ambiguous": sum(1 for e in coh
                                      if e in AMBIGUOUS_ENTITIES),
            "entities_with_stop_context": sum(
                1 for e in coh if e in ENTITY_STOP_CONTEXTS),
        })
    results["binding"] = binding
    return results


# ---------------------------------------------------------------------------
# S5.6 — reliability
# ---------------------------------------------------------------------------

def analyse_reliability_fulltext(rows, pack) -> dict:
    grid = pack["grid"]
    idx200 = grid.index(C.WINDOW)
    llms = np.array([r["llm"] for r in rows])
    days = np.array([int(r["timestamp"][8:10]) for r in rows])
    parity = np.where(days % 2 == 0, "even", "odd")
    y200 = pack["cited_grid"][:, idx200].astype(float)
    yfull = pack["cited_full"].astype(float)

    out = []
    for e in sorted(set(llms.tolist()), key=lambda x: (
            ENGINE_ORDER.index(x) if x in ENGINE_ORDER else 99, x)):
        row = {"engine": e}
        for half in ("even", "odd"):
            m = (llms == e) & (parity == half)
            n = int(m.sum())
            row[f"n_{half}"] = n
            row[f"rate200_{half}_pct"] = (100 * float(y200[m].mean())
                                          if n else float("nan"))
            row[f"ratefull_{half}_pct"] = (100 * float(yfull[m].mean())
                                           if n else float("nan"))
            row[f"days_{half}"] = ",".join(sorted(
                {r["timestamp"][:10] for i, r in enumerate(rows) if m[i]}))
        row["abs_diff_rate200_pp"] = abs(row["rate200_even_pct"]
                                         - row["rate200_odd_pct"]) \
            if row["n_even"] and row["n_odd"] else float("nan")
        row["abs_diff_ratefull_pp"] = abs(row["ratefull_even_pct"]
                                          - row["ratefull_odd_pct"]) \
            if row["n_even"] and row["n_odd"] else float("nan")
        row["splittable"] = int(bool(row["n_even"] and row["n_odd"]))
        out.append(row)
    return {"per_engine": out}


def analyse_reliability_series(con, extractors, sample_limit: int | None) -> dict:
    """Split-half over the five-month series under a uniform 200-char window.

    The full-text cohort spans three days, which is too short to say whether
    the measure is stable. The long series can answer that, but only under a
    window that is the same on every arm, which is why `response_text` is
    re-cut at 200 characters here rather than read from `cited_v2`: for
    Perplexity before 2026-08-31 the stored string is longer than the window
    and the stored flag is therefore not a uniform-window measurement.
    """
    rows = con.execute(SERIES_SQL).fetchall()
    if sample_limit and len(rows) > sample_limit:
        step = len(rows) / sample_limit
        rows = [rows[int(i * step)] for i in range(sample_limit)]
        sampled = True
    else:
        sampled = False

    recs = []
    for r in rows:
        ext = extractors.get(r["vertical"])
        if ext is None:
            continue
        m = ext.extract((r["response_text"] or "")[: C.WINDOW])
        recs.append({
            "engine": r["llm"], "vertical": r["vertical"],
            "lang": r["query_lang"], "qtype": r["query_type"],
            "day": r["timestamp"][:10],
            "parity": "even" if int(r["timestamp"][8:10]) % 2 == 0 else "odd",
            "cited": 1 if m else 0,
            "first_entity": m[0].entity if m else None,
        })

    import pandas as pd
    df = pd.DataFrame(recs)

    per_engine = []
    for e, d in df.groupby("engine"):
        ev, od = d[d["parity"] == "even"], d[d["parity"] == "odd"]
        rd, p = fisher_exact_rd(int(ev["cited"].sum()), len(ev),
                                int(od["cited"].sum()), len(od))
        per_engine.append({
            "engine": e,
            "n_even": len(ev), "n_odd": len(od),
            "days_even": int(ev["day"].nunique()),
            "days_odd": int(od["day"].nunique()),
            "rate_even_pct": 100 * float(ev["cited"].mean()) if len(ev) else float("nan"),
            "rate_odd_pct": 100 * float(od["cited"].mean()) if len(od) else float("nan"),
            "diff_pp": rd, "fisher_p": p,
        })
    per_engine.sort(key=lambda r: (ENGINE_ORDER.index(r["engine"])
                                   if r["engine"] in ENGINE_ORDER else 99))

    # cell-level agreement: engine x vertical x language x query type
    cells = []
    for (e, v, lg, qt), d in df.groupby(["engine", "vertical", "lang", "qtype"]):
        ev, od = d[d["parity"] == "even"], d[d["parity"] == "odd"]
        if len(ev) < SMALL_N or len(od) < SMALL_N:
            continue
        cells.append({"engine": e, "vertical": v, "lang": lg, "qtype": qt,
                      "n_even": len(ev), "n_odd": len(od),
                      "rate_even_pct": 100 * float(ev["cited"].mean()),
                      "rate_odd_pct": 100 * float(od["cited"].mean())})
    a = [c["rate_even_pct"] for c in cells]
    b = [c["rate_odd_pct"] for c in cells]
    diffs = [x - y for x, y in zip(a, b)]
    r_p, p_p = pearson(a, b)
    r_s, p_s = spearman(a, b)
    typical_error = (float(np.std(diffs, ddof=1)) / math.sqrt(2)
                     if len(diffs) > 1 else float("nan"))
    sb = (2 * r_p / (1 + r_p)) if r_p == r_p and r_p > -1 else float("nan")

    # entity ranking agreement per engine
    rank_rows = []
    for e, d in df.groupby("engine"):
        ce = Counter(d.loc[(d["parity"] == "even") & d["first_entity"].notna(),
                           "first_entity"])
        co = Counter(d.loc[(d["parity"] == "odd") & d["first_entity"].notna(),
                           "first_entity"])
        union = sorted(set(ce) | set(co))
        if len(union) < 3:
            rank_rows.append({"engine": e, "n_entities_union": len(union),
                              "spearman_rho": float("nan"), "p": float("nan"),
                              "top10_overlap": float("nan"),
                              "top5_even": "", "top5_odd": ""})
            continue
        rho, p = spearman([ce.get(x, 0) for x in union],
                          [co.get(x, 0) for x in union])
        t10e = [x for x, _ in ce.most_common(10)]
        t10o = [x for x, _ in co.most_common(10)]
        overlap = (len(set(t10e) & set(t10o)) / max(1, min(len(t10e), len(t10o)))
                   if t10e and t10o else float("nan"))
        rank_rows.append({
            "engine": e, "n_entities_union": len(union),
            "spearman_rho": rho, "p": p, "top10_overlap": overlap,
            "top5_even": " > ".join(x for x, _ in ce.most_common(5)),
            "top5_odd": " > ".join(x for x, _ in co.most_common(5)),
        })
    rank_rows.sort(key=lambda r: (ENGINE_ORDER.index(r["engine"])
                                  if r["engine"] in ENGINE_ORDER else 99))

    return {
        "sampled": sampled, "n_rows": len(df),
        "n_days": int(df["day"].nunique()),
        "date_min": str(df["day"].min()), "date_max": str(df["day"].max()),
        "per_engine": per_engine,
        "cells": cells,
        "cell_pearson": r_p, "cell_pearson_p": p_p,
        "cell_spearman": r_s, "cell_spearman_p": p_s,
        "spearman_brown": sb,
        "typical_error_pp": typical_error,
        "n_cells": len(cells),
        "entity_rank": rank_rows,
    }


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def print_report(res: dict) -> None:
    P = print
    P("=" * 78)
    P("S5 — WINDOW VALIDITY")
    P("=" * 78)
    P(f"snapshot (max citations.timestamp): {res['snapshot']}")
    ck = res["checks"]
    P(f"rows compared: {ck['rows']:,}")
    P(f"check 1 response_text == full[:200]      mismatches {ck['text_prefix_mismatch']}"
      f"  {'PASS' if ck['text_prefix_mismatch'] == 0 else 'FAIL'}")
    P(f"check 2 re-extraction == stored cited_v2 mismatches {ck['cited_v2_mismatch']}"
      f"  {'PASS' if ck['cited_v2_mismatch'] == 0 else 'FAIL'}")
    P("")

    curve = res["curve"]
    grid = curve["grid"]
    P("-- S5.1 window sensitivity curve (citation rate %, same rows) --")
    hdr = "engine        n   " + "".join(f"{(w or 'full'):>8}" for w in grid)
    P(hdr)
    for e in curve["engines"]:
        d = curve["per_engine"][e]
        line = f"{e:<12}{d['n']:>5}  "
        for w in grid:
            line += f"{d['rates'][w]:>8.1f}"
        P(line)
    P("")
    P("-- S5.1 the 200-to-full contrast --")
    P(f"{'engine':<12}{'n':>6}{'200':>8}{'full':>8}{'delta':>9}"
      f"{'boot 95% CI':>20}{'gain':>7}{'loss':>6}{'McNemar p':>12}"
      f"{'sat.':>7}{'deff':>7}")
    for e in curve["engines"]:
        d = curve["per_engine"][e]
        sat = d["saturation_window"] or "full"
        P(f"{e:<12}{d['n']:>6}{d['rates'][C.WINDOW]:>8.1f}{d['rate_full']:>8.1f}"
          f"{d['delta_200_full_pp']:>+9.1f}"
          f"{'[' + fmt(d['boot_ci_pp'][0]) + ', ' + fmt(d['boot_ci_pp'][1]) + ']':>20}"
          f"{d['mcnemar_gain']:>7}{d['mcnemar_loss']:>6}"
          f"{fmt_p(d['mcnemar_p']):>12}{str(sat):>7}{d['design_effect']:>7.2f}")
    P("")

    P("-- S5.1b restricted to observations longer than the window --")
    P(f"{'engine':<12}{'n>200':>7}{'dropped':>9}{'200':>8}{'full':>8}{'delta':>9}"
      f"{'w50':>7}{'w80':>7}{'w90':>7}{'w95':>7}{'median len':>12}")
    for r in res["restricted"]["restricted"]:
        P(f"{r['engine']:<12}{r['n_longer_than_window']:>7}"
          f"{r['dropped_short_rows']:>9}{r['rate_200_pct']:>8.1f}"
          f"{r['rate_full_pct']:>8.1f}{r['delta_pp']:>+9.1f}"
          f"{int(r['w50']):>7}{int(r['w80']):>7}{int(r['w90']):>7}"
          f"{int(r['w95']):>7}{r['median_len_full']:>12.0f}")
    P("")
    P("-- S5.1b by collection day --")
    P(f"{'engine':<12}{'day':<12}{'n':>6}{'mean len':>10}{'<=200':>7}"
      f"{'200':>8}{'full':>8}{'delta':>9}")
    for r in res["restricted"]["daily"]:
        P(f"{r['engine']:<12}{r['day']:<12}{r['n']:>6}{r['mean_len_full']:>10.0f}"
          f"{r['rows_at_or_below_window']:>7}{r['rate_200_pct']:>8.1f}"
          f"{r['rate_full_pct']:>8.1f}{r['delta_pp']:>+9.1f}")
    P("")

    rec = res["recovery"]
    P("-- S5.2 window that recovers q of the first mentions --")
    P(f"{'engine':<12}{'cited full':>11}{'w50':>7}{'w80':>7}{'w90':>7}{'w95':>7}"
      f"{'median offset':>15}{'beyond grid':>13}")
    for e in list(curve["engines"]) + ["ALL"]:
        q = rec["quantiles"].get(e)
        if not q:
            continue
        P(f"{e:<12}{q['n_cited_on_full']:>11}"
          f"{int(q['w50']):>7}{int(q['w80']):>7}{int(q['w90']):>7}{int(q['w95']):>7}"
          f"{q['median_first_offset_full']:>15.0f}{q['beyond_grid']:>13}")
    P(f"   non-monotone observations: {rec['non_monotone_rows']}")
    P("")

    pre = res["preamble"]
    P("-- S5.3 preamble by engine --")
    P(f"{'engine':<12}{'n':>6}{'preamble %':>12}{'delta pp':>10}"
      f"{'median len':>12}{'median offset':>15}  class")
    for r in pre["engine_level"]:
        P(f"{r['engine']:<12}{r['n']:>6}{r['preamble_share_pct']:>12.1f}"
          f"{r['delta_200_full_pp']:>+10.1f}{r['median_len_full']:>12.0f}"
          f"{r['median_first_offset']:>15.0f}  {r['engine_class']}")
    t = pre["engine_level_tests"]
    P(f"   engine-level Spearman, preamble share vs delta : "
      f"rho={fmt(t['spearman_preamble_vs_delta'][0], 3)} "
      f"p={fmt_p(t['spearman_preamble_vs_delta'][1])} (n={t['n_engines']})")
    P(f"   engine-level Spearman, median length vs delta  : "
      f"rho={fmt(t['spearman_medianlen_vs_delta'][0], 3)} "
      f"p={fmt_p(t['spearman_medianlen_vs_delta'][1])}")
    P(f"   engine-level Spearman, median offset vs delta  : "
      f"rho={fmt(t['spearman_offset_vs_delta'][0], 3)} "
      f"p={fmt_p(t['spearman_offset_vs_delta'][1])}")
    P("")
    P("-- S5.3 the same, restricted to responses longer than the window --")
    P(f"{'engine':<12}{'n':>6}{'preamble %':>12}{'delta pp':>10}"
      f"{'median len':>12}{'median offset':>15}")
    for r in pre["engine_level_restricted"]:
        P(f"{r['engine']:<12}{r['n']:>6}{r['preamble_share_pct']:>12.1f}"
          f"{r['delta_pp']:>+10.1f}{r['median_len_full']:>12.0f}"
          f"{r['median_first_offset']:>15.0f}")
    tr = pre["engine_level_restricted_tests"]
    P(f"   restricted Spearman, preamble share vs delta : "
      f"rho={fmt(tr['spearman_preamble_vs_delta'][0], 3)} "
      f"p={fmt_p(tr['spearman_preamble_vs_delta'][1])} (n={tr['n_engines']})")
    P(f"   restricted Spearman, median length vs delta  : "
      f"rho={fmt(tr['spearman_medianlen_vs_delta'][0], 3)} "
      f"p={fmt_p(tr['spearman_medianlen_vs_delta'][1])}")
    P(f"   restricted Spearman, median offset vs delta  : "
      f"rho={fmt(tr['spearman_offset_vs_delta'][0], 3)} "
      f"p={fmt_p(tr['spearman_offset_vs_delta'][1])}")
    P("")
    P("-- S5.3 cell-level models (engine x vertical x language, n>=30) --")
    for k, v in pre["cell_models"].items():
        if not isinstance(v, dict):
            P(f"   {k}: {v}")
            continue
        if "error" in v:
            P(f"   {k}: {v['error']}")
            continue
        P(f"   {k:<28} b={v['coef']:+.4f} [{v['ci_lo']:+.4f}, {v['ci_hi']:+.4f}] "
          f"p={fmt_p(v['p'])}")
    P("")
    P("-- S5.3 observation level: miss by the 200-char window, among cited-on-full --")
    obs = pre["observation_level"]
    P(f"{'engine':<12}{'cited full':>11}{'n pre':>7}{'n no-pre':>10}"
      f"{'miss% pre':>11}{'miss% no':>10}{'RD pp':>9}{'Fisher p':>12}")
    for r in obs["per_engine_contrast"]:
        P(f"{r['engine']:<12}{r['n_cited_full']:>11}{r['n_preamble']:>7}"
          f"{r['n_no_preamble']:>10}{fmt(r['miss_rate_preamble_pct']):>11}"
          f"{fmt(r['miss_rate_no_preamble_pct']):>10}{fmt(r['risk_difference_pp']):>9}"
          f"{fmt_p(r['fisher_p']):>12}")
    for key in ("pooled_preamble_only", "pooled_preamble_plus_length",
                "pooled_length_in_joint", "within_engine_fe"):
        v = obs.get(key)
        if not v:
            continue
        if "error" in v:
            P(f"   {key}: {v['error']}")
            continue
        P(f"   {key:<30} OR={v.get('odds_ratio', float('nan')):.3f} "
          f"[{v.get('or_ci_lo', float('nan')):.3f}, {v.get('or_ci_hi', float('nan')):.3f}] "
          f"p={fmt_p(v['p'])}  n={v['n']}")
    P("")
    mech = pre["mechanism"]
    if "error" not in mech.get("offset_model", {}):
        v = mech["offset_model"]
        P(f"   offset model (log10 first offset ~ preamble + log10 len + engine FE): "
          f"b={v['coef']:+.4f} [{v['ci_lo']:+.4f}, {v['ci_hi']:+.4f}] p={fmt_p(v['p'])} "
          f"n={mech['offset_model_n']}")
        v2 = mech["offset_model_length"]
        P(f"   same model, length term: b={v2['coef']:+.4f} "
          f"[{v2['ci_lo']:+.4f}, {v2['ci_hi']:+.4f}] p={fmt_p(v2['p'])}")
        mul = mech["offset_multiplier_preamble"]
        mci = mech["offset_multiplier_preamble_ci"]
        P(f"   preamble shifts the first mention by a factor of {mul:.2f}x "
          f"[{mci[0]:.2f}, {mci[1]:.2f}]")
    P("")
    P("-- censoring diagnostic: stored responses that end mid-sentence --")
    P(f"{'engine':<12}{'n':>6}{'cut':>7}{'cut %':>8}{'p95 len':>10}{'max len':>10}")
    for r in res["restricted"]["censoring"]:
        P(f"{r['engine']:<12}{r['n']:>6}"
          f"{r['ends_without_terminal_punctuation']:>7}"
          f"{r['ends_without_terminal_punctuation_pct']:>8.1f}"
          f"{r['p95_len_full']:>10.0f}{r['max_len_full']:>10}")
    P("")

    P("-- S5.4 minimum detectable difference (alpha=0.05, power=0.80) --")
    P(f"{'stratum':<26}{'n':>7}{'rate full':>11}{'disc.%':>8}{'deff':>7}"
      f"{'eff. n':>9}{'MDE paired':>12}{'MDE unpaired':>14}")
    for block in (res["power"]["per_engine"] + res["power"]["per_vertical"]
                  + [res["power"]["overall"]]):
        P(f"{block['label']:<26}{block['n']:>7}{block['rate_full_pct']:>11.1f}"
          f"{block['discordant_share_pct']:>8.1f}{block['design_effect']:>7.2f}"
          f"{block['effective_n']:>9.0f}"
          f"{fmt(block['mde_paired_pp_clustered']):>12}"
          f"{fmt(block['mde_unpaired_pp_clustered']):>14}")
    P("")

    P("-- S5.5 matching-rule sensitivity (P6) --")
    P(f"{'variant':<22}{'engine':<12}{'200%':>8}{'full%':>8}"
      f"{'d200':>8}{'dfull':>8}{'flips200':>10}{'flipsfull':>11}")
    for r in res["matching"]["table"]:
        if r["engine"] != "ALL" and r["variant"] == "base":
            pass
        P(f"{r['variant']:<22}{r['engine']:<12}{r['rate_200_pct']:>8.2f}"
          f"{r['rate_full_pct']:>8.2f}{r['delta_vs_base_200_pp']:>+8.2f}"
          f"{r['delta_vs_base_full_pp']:>+8.2f}{r['flipped_rows_200']:>10}"
          f"{r['flipped_rows_full']:>11}")
    P("   how much of the rule binds on the v2 cohort:")
    for b in res["matching"]["binding"]:
        P(f"     {b['vertical']:<12} cohort={b['cohort_size']:>3} "
          f"alias-entities={b['entities_with_alias']:>2} "
          f"alias-surfaces={b['alias_surfaces']:>2} "
          f"ambiguous={b['entities_ambiguous']:>2} "
          f"stop-contexts={b['entities_with_stop_context']:>2}")
    P("")

    P("-- S5.6a reliability on the full-text cohort (even vs odd days) --")
    for r in res["reliability_fulltext"]["per_engine"]:
        P(f"   {r['engine']:<12} even n={r['n_even']:>4} "
          f"rate200={fmt(r['rate200_even_pct']):>6} full={fmt(r['ratefull_even_pct']):>6} | "
          f"odd n={r['n_odd']:>4} rate200={fmt(r['rate200_odd_pct']):>6} "
          f"full={fmt(r['ratefull_odd_pct']):>6} | "
          f"splittable={'yes' if r['splittable'] else 'NO'}")
    P("")
    rs = res.get("reliability_series")
    if rs:
        P("-- S5.6b reliability on the five-month series, uniform 200-char window --")
        P(f"   rows={rs['n_rows']:,} days={rs['n_days']} "
          f"{rs['date_min']} to {rs['date_max']}"
          f"{'  [SAMPLED]' if rs['sampled'] else ''}")
        for r in rs["per_engine"]:
            P(f"   {r['engine']:<12} even {r['rate_even_pct']:>6.2f}% "
              f"(n={r['n_even']:,}, {r['days_even']}d) | "
              f"odd {r['rate_odd_pct']:>6.2f}% (n={r['n_odd']:,}, {r['days_odd']}d) | "
              f"diff {r['diff_pp']:+.2f} pp  p={fmt_p(r['fisher_p'])}")
        P(f"   cell-level agreement over {rs['n_cells']} cells: "
          f"Pearson r={fmt(rs['cell_pearson'], 4)}, "
          f"Spearman rho={fmt(rs['cell_spearman'], 4)}, "
          f"Spearman-Brown={fmt(rs['spearman_brown'], 4)}, "
          f"typical error={fmt(rs['typical_error_pp'], 2)} pp")
        for r in rs["entity_rank"]:
            P(f"   {r['engine']:<12} entity-rank rho={fmt(r['spearman_rho'], 3):>6} "
              f"p={fmt_p(r['p']):>10} top10 overlap={fmt(100*r['top10_overlap'], 0):>5}% "
              f"union={r['n_entities_union']}")
    P("")


# ---------------------------------------------------------------------------
# CSV emission
# ---------------------------------------------------------------------------

def write_outputs(res: dict) -> list[Path]:
    written: list[Path] = []
    curve, grid = res["curve"], res["curve"]["grid"]

    rows = []
    for e in curve["engines"]:
        d = curve["per_engine"][e]
        for w in grid:
            lo, hi = d["rate_ci"][w]
            rows.append({
                "engine": e, "n": d["n"], "n_queries": d["n_queries"],
                "window_chars": "full" if w is None else w,
                "cited": d["cited_counts"][w],
                "rate_pct": d["rates"][w],
                "ci_lo_pct": lo, "ci_hi_pct": hi,
                "rate_full_pct": d["rate_full"],
                "gap_to_full_pp": d["rate_full"] - d["rates"][w],
                "saturation_window": d["saturation_window"] or "full",
                "window_95pct_of_full": d["window_95pct_of_full"] or "full",
                "median_len_full": d["median_len_full"],
                "dates": ",".join(d["dates"]),
            })
    p = DATA_DIR / "s5_window_curve_by_engine.csv"
    write_csv(p, rows, list(rows[0].keys()))
    written.append(p)

    rows = []
    for e in curve["engines"]:
        d = curve["per_engine"][e]
        rows.append({
            "engine": e, "n": d["n"], "n_queries": d["n_queries"],
            "rate_200_pct": d["rates"][C.WINDOW],
            "rate_200_ci_lo": d["rate_ci"][C.WINDOW][0],
            "rate_200_ci_hi": d["rate_ci"][C.WINDOW][1],
            "rate_full_pct": d["rate_full"],
            "rate_full_ci_lo": d["rate_full_ci"][0],
            "rate_full_ci_hi": d["rate_full_ci"][1],
            "delta_pp": d["delta_200_full_pp"],
            "delta_boot_ci_lo_pp": d["boot_ci_pp"][0],
            "delta_boot_ci_hi_pp": d["boot_ci_pp"][1],
            "mcnemar_gain": d["mcnemar_gain"], "mcnemar_loss": d["mcnemar_loss"],
            "mcnemar_p": d["mcnemar_p"],
            "design_effect": d["design_effect"],
            "saturation_window": d["saturation_window"] or "full",
            "window_95pct_of_full": d["window_95pct_of_full"] or "full",
            "rows_longer_than_200": d["rows_longer_than_200"],
            "median_len_full": d["median_len_full"],
            "mean_len_full": d["mean_len_full"],
            "dates": ",".join(d["dates"]),
        })
    p = DATA_DIR / "s5_window_contrast_200_vs_full.csv"
    write_csv(p, rows, list(rows[0].keys()))
    written.append(p)

    cells = curve["per_cell"]
    p = DATA_DIR / "s5_window_curve_by_engine_vertical.csv"
    write_csv(p, cells, list(cells[0].keys()))
    written.append(p)

    rr = res["restricted"]["restricted"]
    p = DATA_DIR / "s5_window_contrast_restricted.csv"
    write_csv(p, rr, list(rr[0].keys()))
    written.append(p)
    dd = res["restricted"]["daily"]
    p = DATA_DIR / "s5_window_by_day.csv"
    write_csv(p, dd, list(dd[0].keys()))
    written.append(p)
    cz = res["restricted"]["censoring"]
    p = DATA_DIR / "s5_response_censoring.csv"
    write_csv(p, cz, list(cz[0].keys()))
    written.append(p)

    rec = res["recovery"]
    p = DATA_DIR / "s5_mention_recovery_curve.csv"
    write_csv(p, rec["curves"], list(rec["curves"][0].keys()))
    written.append(p)

    rows = []
    for e, q in rec["quantiles"].items():
        rows.append({"engine": e, **{k: v for k, v in q.items()}})
    p = DATA_DIR / "s5_mention_recovery_quantiles.csv"
    write_csv(p, rows, list(rows[0].keys()))
    written.append(p)

    pre = res["preamble"]
    p = DATA_DIR / "s5_preamble_by_engine.csv"
    write_csv(p, pre["engine_level"], list(pre["engine_level"][0].keys()))
    written.append(p)
    p = DATA_DIR / "s5_preamble_by_engine_restricted.csv"
    write_csv(p, pre["engine_level_restricted"],
              list(pre["engine_level_restricted"][0].keys()))
    written.append(p)
    p = DATA_DIR / "s5_preamble_by_cell.csv"
    write_csv(p, pre["cell_level"], list(pre["cell_level"][0].keys()))
    written.append(p)
    p = DATA_DIR / "s5_preamble_model_cells.csv"
    write_csv(p, pre["model_cells"], list(pre["model_cells"][0].keys()))
    written.append(p)
    p = DATA_DIR / "s5_preamble_observation_contrast.csv"
    oc = pre["observation_level"]["per_engine_contrast"]
    write_csv(p, oc, list(oc[0].keys()))
    written.append(p)

    pw = (res["power"]["per_engine"] + res["power"]["per_vertical"]
          + res["power"]["per_engine_vertical"] + [res["power"]["overall"]])
    p = DATA_DIR / "s5_power_mde.csv"
    write_csv(p, pw, list(pw[0].keys()))
    written.append(p)

    p = DATA_DIR / "s5_matching_rule_sensitivity.csv"
    write_csv(p, res["matching"]["table"],
              list(res["matching"]["table"][0].keys()))
    written.append(p)

    p = DATA_DIR / "s5_reliability_fulltext_split.csv"
    rf = res["reliability_fulltext"]["per_engine"]
    write_csv(p, rf, list(rf[0].keys()))
    written.append(p)

    rs = res.get("reliability_series")
    if rs:
        p = DATA_DIR / "s5_reliability_series_split.csv"
        write_csv(p, rs["per_engine"], list(rs["per_engine"][0].keys()))
        written.append(p)
        p = DATA_DIR / "s5_reliability_series_cells.csv"
        write_csv(p, rs["cells"], list(rs["cells"][0].keys()))
        written.append(p)
        p = DATA_DIR / "s5_reliability_entity_rank.csv"
        write_csv(p, rs["entity_rank"], list(rs["entity_rank"][0].keys()))
        written.append(p)

    # everything, for the prose to quote without re-running
    payload = {k: v for k, v in res.items() if k != "preamble"}
    payload["preamble"] = {k: v for k, v in res["preamble"].items()
                           if k != "_frame"}
    p = DATA_DIR / "s5_window_validity.json"
    p.write_text(json.dumps(payload, indent=2, ensure_ascii=False,
                            default=_json_default), encoding="utf-8")
    written.append(p)
    return written


def _json_default(o):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, set):
        return sorted(o)
    return str(o)


# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--bootstrap", type=int, default=BOOTSTRAP_B)
    ap.add_argument("--quick", action="store_true",
                    help="1,000 bootstrap replicates and no S5.6b")
    ap.add_argument("--series-sample", type=int, default=None,
                    help="cap S5.6b at N rows, sampled on a regular stride")
    ap.add_argument("--cache-dir", default=None,
                    help="reuse the extraction passes from this scratch "
                         "directory; leave unset for a clean run")
    args = ap.parse_args()

    b = 1000 if args.quick else args.bootstrap
    rng = np.random.default_rng(RNG_SEED)
    t0 = time.time()

    con = C.connect()
    snapshot = con.execute("SELECT MAX(timestamp) FROM citations").fetchone()[0]
    rows = load_fulltext_rows(con)
    if not rows:
        print("no canonical row retains response_full_text; nothing to compare")
        return 1
    print(f"loaded {len(rows):,} canonical observations with a stored full response")

    extractors = C.build_extractors(include_anchors=True, include_decoys=True)

    checks = identity_checks(rows, extractors)
    print(f"identity checks: {'PASS' if checks['pass'] else 'FAIL'} "
          f"({time.time() - t0:.0f}s)")

    cache_dir = Path(args.cache_dir) if args.cache_dir else None

    grid_ints = [w for w in WINDOW_GRID if w is not None]
    print("extracting over the coarse grid ...", flush=True)
    pack = _cache_load(cache_dir, "coarse", len(rows))
    if pack is None:
        pack = extract_over_grid(rows, extractors, grid_ints)
        _cache_save(cache_dir, "coarse", len(rows), pack)
    pack["grid"] = [int(w) for w in pack["grid"]] + [None]
    pack["cited_grid"] = np.column_stack([pack["cited_grid"],
                                          pack["cited_full"]])
    curve = analyse_window_curve(rows, pack, b, rng)
    print(f"  coarse grid done ({time.time() - t0:.0f}s)")

    print("extracting over the fine recovery grid ...", flush=True)
    pack_fine = _cache_load(cache_dir, "fine", len(rows))
    if pack_fine is None:
        pack_fine = extract_over_grid(rows, extractors, RECOVERY_GRID)
        _cache_save(cache_dir, "fine", len(rows), pack_fine)
    pack_fine["grid"] = [int(w) for w in pack_fine["grid"]]
    recovery = analyse_recovery(rows, pack_fine)
    print(f"  fine grid done ({time.time() - t0:.0f}s)")

    restricted = analyse_restricted_and_daily(rows, pack, pack_fine,
                                              recovery["needed"])
    preamble = analyse_preamble(rows, pack, curve)
    power = analyse_power(rows, pack, curve, b, rng)
    print(f"  preamble and power done ({time.time() - t0:.0f}s)")

    print("re-extracting under matching-rule variants ...", flush=True)
    matching = analyse_matching_rule(rows)
    print(f"  variants done ({time.time() - t0:.0f}s)")

    rel_full = analyse_reliability_fulltext(rows, pack)
    rel_series = None
    if not args.quick:
        print("re-extracting the five-month series under a uniform window ...",
              flush=True)
        rel_series = analyse_reliability_series(con, extractors,
                                                args.series_sample)
        print(f"  series done ({time.time() - t0:.0f}s)")

    res = {
        "snapshot": snapshot,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "n_rows": len(rows),
        "window_grid": [("full" if w is None else w) for w in WINDOW_GRID],
        "recovery_grid": RECOVERY_GRID,
        "saturation_tol_pp": SATURATION_TOL_PP,
        "bootstrap_replicates": b,
        "rng_seed": RNG_SEED,
        "cohort_sizes": {v: len(C.get_v2_cohort(v, True, True))
                         for v in C.VERTICALS},
        "checks": checks,
        "curve": curve,
        "restricted": restricted,
        "recovery": {k: v for k, v in recovery.items() if k != "needed"},
        "preamble": preamble,
        "power": power,
        "matching": matching,
        "reliability_fulltext": rel_full,
        "reliability_series": rel_series,
    }

    print_report(res)
    written = write_outputs(res)
    print("wrote:")
    for p in written:
        print(f"  {p}")
    print(f"total {time.time() - t0:.0f}s")
    return 0 if checks["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
