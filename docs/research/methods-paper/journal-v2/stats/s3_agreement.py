#!/usr/bin/env python
"""s3_agreement.py — inter-engine agreement for the BRGEO-1 field record (S3).

Question this script answers
----------------------------
When six generative engines are asked the same query on the same day, do they
measure the same object? If "citation rate" were a property of the firm, the
engines would be interchangeable instruments reading one underlying quantity and
their disagreement would be sampling noise. If it is a property of the engine,
each engine defines its own object and a single-vendor measurement is not an
estimate of anything outside that vendor.

Everything below is computed from `citations` under the canonical stratum
(`COALESCE(is_probe,0)=0`), read-only.

The outcome
-----------
`citations.cited_v2` is NOT comparable across engines as stored. Five of the six
arms wrote `response_text = text[:200]` at collection time; Perplexity wrote the
whole response (median 607 characters, max 2,502). The stored `cited_v2` was
extracted from whichever text was stored, so Perplexity was measured through a
wider aperture than the others. This script therefore re-derives the outcome
under a uniform 200-character window for every arm, using the project's own
extractor (`src.analysis.entity_extraction.EntityExtractor` over the v2 cohort,
via `tables/_common.build_extractors`):

    cited_win        1 iff >= 1 cohort entity is matched in response_text[:200]
    entities_win     the matched entities, ordered by first-mention offset

Section 0 verifies that this re-derivation reproduces the stored `cited_v2`
exactly on the five truncated arms, which is what licenses using it as the
harmonised outcome. Agreement on the as-stored outcome is reported as a
sensitivity so that a reader can see how much of the between-engine spread is
the instrument rather than the engines.

Panel
-----
Unit of observation: (collection day, canonical query, engine). Replicates of
the same cell (the collector re-ran some batteries within a day) are reduced to
the earliest timestamp; their concordance is reported separately as a
test-retest ceiling on any between-engine agreement.

No day carries all six engines: Groq's last day is 2026-08-16 and Grok's first
is 2026-08-23, and they never co-occur. Perplexity ran a 96-query half-battery
against the other arms' 192. Agreement is therefore reported on nested balanced
panels rather than on one impossible six-way panel.

Usage
-----
    python s3_agreement.py                    # full run, markdown to stdout
    python s3_agreement.py --boot 2000        # bootstrap replications
    python s3_agreement.py --cache <path.pkl> # cache the extraction pass

Nothing here writes to the database: the handle comes from `_common.connect()`,
opened with `mode=ro`.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import pickle
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats as sps
from scipy.cluster.hierarchy import linkage
from scipy.spatial.distance import squareform
from sklearn.decomposition import PCA

# ---------------------------------------------------------------------------
# Project primitives. `_common` lives one directory over, in tables/.
# ---------------------------------------------------------------------------
HERE = Path(__file__).resolve().parent
TABLES = HERE.parent / "tables"
if str(TABLES) not in sys.path:
    sys.path.insert(0, str(TABLES))

import _common as C  # noqa: E402

REPO_ROOT = C.REPO_ROOT
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.analysis.kappa_validator import cohen_kappa_binary  # noqa: E402
from src.analysis.null_simulation import simulate_jaccard_null  # noqa: E402

WINDOW = C.WINDOW                       # 200 characters, METHODOLOGY_V2 4.1-bis
ENGINES = C.ENGINES                     # display order
VERTICALS = C.VERTICALS
VLABEL = C.VERTICAL_LABEL
ENGINE_CLASS = C.ENGINE_CLASS
SEED = 20260911
RBO_P = 0.90                            # top-weighting of the rank overlap

#: Size of the v2 extractor cohort per vertical (real + anchors + decoys).
from src.config_v2 import get_v2_cohort  # noqa: E402
COHORT_SIZE = {v: len(get_v2_cohort(v, True, True)) for v in VERTICALS}


# ---------------------------------------------------------------------------
# 0. Extraction pass
# ---------------------------------------------------------------------------

def load_panel(cache: Path | None = None) -> pd.DataFrame:
    """One row per (day, query, engine, replicate) with the harmonised outcome.

    Columns: day, query, llm, vertical, query_lang, query_type, ts, row_id,
    cited_v2 (as stored), cited_win (200-char window), ents_win (tuple, ordered
    by first-mention offset), n_full (length of the stored response_text).
    """
    if cache is not None and cache.exists():
        with cache.open("rb") as fh:
            return pickle.load(fh)

    ex = C.build_extractors(include_anchors=True, include_decoys=True)
    con = C.connect()
    cur = con.cursor()
    cur.execute(
        f"""SELECT id, timestamp, date(timestamp) AS day, llm, vertical, query,
                   query_lang, query_type, cited_v2, response_text
              FROM citations
             WHERE {C.CANONICAL}
             ORDER BY timestamp, id"""
    )
    recs = []
    for r in cur:
        text = r["response_text"] or ""
        mentions = ex[r["vertical"]].extract(text[:WINDOW])
        seen: dict[str, int] = {}
        for m in mentions:
            if m.entity not in seen or m.start < seen[m.entity]:
                seen[m.entity] = m.start
        ents = tuple(e for e, _ in sorted(seen.items(), key=lambda kv: kv[1]))
        recs.append(
            (r["id"], r["timestamp"], r["day"], r["llm"], r["vertical"],
             r["query"], r["query_lang"], r["query_type"],
             r["cited_v2"], 1 if ents else 0, ents, len(text))
        )
    con.close()
    df = pd.DataFrame.from_records(
        recs,
        columns=["row_id", "ts", "day", "llm", "vertical", "query",
                 "query_lang", "query_type", "cited_v2", "cited_win",
                 "ents_win", "n_full"],
    )
    if cache is not None:
        with cache.open("wb") as fh:
            pickle.dump(df, fh)
    return df


def harmonisation_check(df: pd.DataFrame) -> pd.DataFrame:
    """Does re-extracting at 200 characters reproduce the stored cited_v2?"""
    g = df.groupby("llm")
    out = pd.DataFrame({
        "n": g.size(),
        "stored_mean_pct": 100 * g["cited_v2"].mean(),
        "window_mean_pct": 100 * g["cited_win"].mean(),
        "identical_pct": 100 * g.apply(
            lambda d: float((d["cited_v2"] == d["cited_win"]).mean()),
            include_groups=False),
        "median_stored_chars": g["n_full"].median(),
    })
    return out.reindex([e for e in ENGINES if e in out.index])


def replicate_concordance(df: pd.DataFrame) -> pd.DataFrame:
    """Same engine, same query, same day, run more than once: does it agree?

    This is the test-retest ceiling. Between-engine agreement cannot exceed
    within-engine stability by much, and any kappa has to be read against it.
    """
    rows = []
    for llm, d in df.groupby("llm"):
        g = d.groupby(["day", "query"])["cited_win"]
        sizes = g.size()
        rep = sizes[sizes >= 2].index
        if len(rep) == 0:
            rows.append((llm, 0, 0, float("nan"), float("nan")))
            continue
        sub = g.agg(["min", "max", "mean", "size"]).loc[rep]
        concord = float((sub["min"] == sub["max"]).mean())
        # Expected concordance of two independent draws at the engine's own rate
        p = float(d["cited_win"].mean())
        chance = p * p + (1 - p) * (1 - p)
        rows.append((llm, int(len(rep)), int(sizes.sum() - len(sizes)),
                     concord, chance))
    out = pd.DataFrame(rows, columns=["llm", "cells_with_replicates",
                                      "extra_runs", "concordant",
                                      "chance_concordance"]).set_index("llm")
    out["kappa_retest"] = ((out["concordant"] - out["chance_concordance"])
                           / (1 - out["chance_concordance"]))
    return out.reindex([e for e in ENGINES if e in out.index])


def first_run(df: pd.DataFrame) -> pd.DataFrame:
    """Reduce replicates to the earliest run of the cell."""
    return (df.sort_values(["ts", "row_id"])
              .drop_duplicates(subset=["day", "query", "llm"], keep="first")
              .reset_index(drop=True))


# ---------------------------------------------------------------------------
# 1. Fleiss' kappa
# ---------------------------------------------------------------------------

def fleiss_from_counts(n1: np.ndarray, k: int) -> float:
    """Fleiss' kappa for a binary rating with a fixed number of raters k.

    n1[i] is the number of raters assigning category 1 to item i.

        P_i    = (n_i1^2 + n_i0^2 - k) / (k(k-1))
        Pbar   = mean_i P_i
        p_1    = sum_i n_i1 / (N k);  Pe = p_1^2 + (1-p_1)^2
        kappa  = (Pbar - Pe) / (1 - Pe)

    Vectorised so the cluster bootstrap can run it thousands of times.
    """
    n1 = np.asarray(n1, dtype=np.float64)
    N = n1.size
    if N == 0 or k < 2:
        return float("nan")
    n0 = k - n1
    P = (n1 * n1 + n0 * n0 - k) / (k * (k - 1))
    Pbar = P.mean()
    p1 = n1.sum() / (N * k)
    Pe = p1 * p1 + (1 - p1) ** 2
    if Pe >= 1.0:
        return float("nan")
    return float((Pbar - Pe) / (1 - Pe))


def lk_label(k: float) -> str:
    """Landis & Koch (1977) verbal band, as coded in src/analysis/kappa_validator."""
    if not np.isfinite(k):
        return "undefined"
    if k < 0:
        return "worse than chance"
    if k < 0.20:
        return "slight"
    if k < 0.40:
        return "fair"
    if k < 0.60:
        return "moderate"
    if k < 0.75:
        return "substantial"
    return "near-perfect"


def implementation_checks(one: pd.DataFrame) -> None:
    """The two kappa implementations here are checked against the references.

    Fleiss against statsmodels.stats.inter_rater.fleiss_kappa, and the pairwise
    2x2 against src.analysis.kappa_validator.cohen_kappa_binary, which is the
    module the project already uses for annotator agreement. The vectorised
    forms exist only so the cluster bootstrap can run thousands of replications;
    they are not a second definition of the statistic.
    """
    from statsmodels.stats.inter_rater import aggregate_raters, fleiss_kappa
    engs = ("ChatGPT", "Claude", "Gemini")
    w = build_panel(one, engs)
    mat = w[list(engs)].to_numpy().astype(int)
    table, _ = aggregate_raters(mat)
    sm_k = float(fleiss_kappa(table, method="fleiss"))
    own_k = fleiss_from_counts(mat.sum(axis=1), len(engs))
    a = one[one["llm"] == "ChatGPT"].set_index(["day", "query"])["cited_win"]
    b = one[one["llm"] == "Claude"].set_index(["day", "query"])["cited_win"]
    j = pd.concat([a.rename("a"), b.rename("b")], axis=1).dropna()
    ref = cohen_kappa_binary(j["a"].astype(int).tolist(),
                            j["b"].astype(int).tolist())
    own_c = kappa_phi(j["a"].to_numpy().astype(int),
                      j["b"].to_numpy().astype(int))["kappa"]
    print("\nimplementation checks")
    print(f"  Fleiss, ChatGPT+Claude+Gemini: statsmodels {sm_k:.6f} | "
          f"this script {own_k:.6f} | delta {abs(sm_k - own_k):.2e}")
    print(f"  Cohen, ChatGPT vs Claude: kappa_validator {ref.kappa:.4f} | "
          f"this script {own_c:.6f} | n = {ref.n_items}")


def cluster_bootstrap(values: np.ndarray, days: np.ndarray, stat,
                      n_boot: int, rng: np.random.Generator) -> tuple:
    """Percentile CI resampling collection days with replacement.

    Days are the project's cluster (cluster_robust.py): every query in a day
    faces the same model snapshot, so cells within a day are not independent.
    """
    uniq = np.unique(days)
    idx_by_day = {d: np.flatnonzero(days == d) for d in uniq}
    reps = np.empty(n_boot)
    for b in range(n_boot):
        pick = rng.choice(uniq, size=uniq.size, replace=True)
        sel = np.concatenate([idx_by_day[d] for d in pick])
        reps[b] = stat(values[sel])
    reps = reps[np.isfinite(reps)]
    if reps.size == 0:
        return (float("nan"), float("nan"), float("nan"))
    return (float(np.percentile(reps, 2.5)), float(np.percentile(reps, 97.5)),
            float(reps.std(ddof=1)))


# ---------------------------------------------------------------------------
# Panels
# ---------------------------------------------------------------------------

PANELS = [
    ("P1", ("ChatGPT", "Claude", "Gemini"), "three arms present end to end"),
    ("P2", ("ChatGPT", "Claude", "Gemini", "Groq"),
     "full 192-query battery, Groq era"),
    ("P3", ("ChatGPT", "Claude", "Gemini", "Grok"),
     "full 192-query battery, Grok era"),
    ("P4", ("ChatGPT", "Claude", "Gemini", "Groq", "Perplexity"),
     "96-query half-battery, Groq era"),
    ("P5", ("ChatGPT", "Claude", "Gemini", "Grok", "Perplexity"),
     "96-query half-battery, Grok era"),
    ("P6", ("ChatGPT", "Claude", "Gemini", "Groq", "Grok", "Perplexity"),
     "all six arms"),
]


def build_panel(one: pd.DataFrame, engines: tuple[str, ...],
                outcome: str = "cited_win") -> pd.DataFrame:
    """Wide (day, query) x engine frame keeping only complete cells."""
    sub = one[one["llm"].isin(engines)]
    wide = sub.pivot_table(index=["day", "query", "vertical"], columns="llm",
                           values=outcome, aggfunc="first")
    missing = [e for e in engines if e not in wide.columns]
    for e in missing:
        wide[e] = np.nan
    wide = wide[list(engines)].dropna()
    return wide.reset_index()


# ---------------------------------------------------------------------------
# 2. Pairwise agreement
# ---------------------------------------------------------------------------

def pair_tables(one: pd.DataFrame, outcome: str = "cited_win") -> dict:
    """2x2 count tables per (pair, day) so the bootstrap only resums tables."""
    wide = one.pivot_table(index=["day", "query", "vertical"], columns="llm",
                           values=outcome, aggfunc="first")
    out = {}
    for a, b in itertools.combinations(ENGINES, 2):
        if a not in wide.columns or b not in wide.columns:
            out[(a, b)] = None
            continue
        sub = wide[[a, b]].dropna()
        if sub.empty:
            out[(a, b)] = None
            continue
        days = np.array([ix[0] for ix in sub.index])
        A = sub[a].to_numpy().astype(int)
        B = sub[b].to_numpy().astype(int)
        out[(a, b)] = (days, A, B)
    return out


def kappa_phi(A: np.ndarray, B: np.ndarray) -> dict:
    """Cohen's kappa, phi, observed agreement and the marginals that bound them."""
    n = A.size
    n11 = int(np.sum((A == 1) & (B == 1)))
    n10 = int(np.sum((A == 1) & (B == 0)))
    n01 = int(np.sum((A == 0) & (B == 1)))
    n00 = int(np.sum((A == 0) & (B == 0)))
    po = (n11 + n00) / n
    pa = (n11 + n10) / n
    pb = (n11 + n01) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    kappa = (po - pe) / (1 - pe) if pe < 1 else float("nan")
    denom = math.sqrt((n11 + n10) * (n01 + n00) * (n11 + n01) * (n10 + n00))
    phi = (n11 * n00 - n10 * n01) / denom if denom > 0 else float("nan")
    # Maximum kappa attainable with these marginals held fixed (Cohen 1960).
    po_max = 1 - abs(pa - pb)
    kmax = (po_max - pe) / (1 - pe) if pe < 1 else float("nan")
    return dict(n=n, n11=n11, n10=n10, n01=n01, n00=n00, po=po, pa=pa, pb=pb,
                pe=pe, kappa=kappa, phi=phi, kappa_max=kmax)


# ---------------------------------------------------------------------------
# 3. Entity-set agreement
# ---------------------------------------------------------------------------

def jaccard(a: frozenset, b: frozenset) -> float:
    u = a | b
    return len(a & b) / len(u) if u else float("nan")


def rbo_ext(S: list, T: list, p: float = RBO_P) -> float:
    """Rank-biased overlap, extrapolated (Webber, Moffat & Zobel 2010, eq. 32).

    Top-weighted with persistence p: at p = 0.90 the first three ranks carry
    roughly 27% of the weight. Lists here are short (median 1-3 entities), so
    RBO is close to a weighted top-1 agreement; the median list length is
    reported next to it so the reader can calibrate that.
    """
    if not S and not T:
        return 1.0
    if not S or not T:
        return 0.0
    L, Sh = (S, T) if len(S) >= len(T) else (T, S)
    l, s = len(L), len(Sh)
    setL: set = set()
    setS: set = set()
    X = np.zeros(l + 1)
    for d in range(1, l + 1):
        setL.add(L[d - 1])
        if d <= s:
            setS.add(Sh[d - 1])
        X[d] = len(setL & setS)
    sum1 = sum((X[d] / d) * (p ** d) for d in range(1, l + 1))
    sum2 = sum((X[s] * (d - s) / (s * d)) * (p ** d) for d in range(s + 1, l + 1))
    return float(((1 - p) / p) * (sum1 + sum2)
                 + ((X[l] - X[s]) / l + X[s] / s) * (p ** l))


def set_agreement(one: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Jaccard and RBO per shared cell, per engine pair."""
    wide = one.pivot_table(index=["day", "query", "vertical"], columns="llm",
                           values="ents_win", aggfunc="first")
    rows = []
    dists: dict = {}
    for a, b in itertools.combinations(ENGINES, 2):
        if a not in wide.columns or b not in wide.columns:
            continue
        sub = wide[[a, b]].dropna()
        if sub.empty:
            continue
        ja, rb, jboth, rboth = [], [], [], []
        n_both_empty = n_one_empty = 0
        for ea, eb in zip(sub[a], sub[b]):
            sa, sb = frozenset(ea), frozenset(eb)
            if not sa and not sb:
                n_both_empty += 1
                continue
            if not sa or not sb:
                n_one_empty += 1
            else:
                jboth.append(jaccard(sa, sb))
                rboth.append(rbo_ext(list(ea), list(eb)))
            ja.append(jaccard(sa, sb))
            rb.append(rbo_ext(list(ea), list(eb)))
        ja = np.array(ja)
        rb = np.array(rb)
        jboth = np.array(jboth)
        rboth = np.array(rboth)
        if ja.size == 0:
            continue
        dists[(a, b)] = (ja, rb)
        rows.append(dict(
            pair=f"{a}-{b}", n_cells=len(sub), n_both_empty=n_both_empty,
            n_scored=ja.size, n_one_empty=n_one_empty,
            pct_j0=100 * float(np.mean(ja == 0)),
            pct_j1=100 * float(np.mean(ja == 1)),
            j_p25=float(np.percentile(ja, 25)),
            j_median=float(np.median(ja)),
            j_p75=float(np.percentile(ja, 75)),
            j_mean=float(ja.mean()),
            rbo_median=float(np.median(rb)), rbo_mean=float(rb.mean()),
            n_both_named=int(jboth.size),
            j_mean_both=float(jboth.mean()) if jboth.size else float("nan"),
            pct_j0_both=(100 * float(np.mean(jboth == 0))
                         if jboth.size else float("nan")),
            rbo_mean_both=float(rboth.mean()) if rboth.size else float("nan"),
        ))
    return pd.DataFrame(rows), dists


# ---------------------------------------------------------------------------
# 4. Latent structure
# ---------------------------------------------------------------------------

def coverage_matrix(one: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Entity x engine coverage: share of the engine's cells naming the entity.

    Denominator is engine- and vertical-specific: an entity belongs to one
    vertical, and only the cells of that vertical could have named it.
    """
    denom = one.groupby(["llm", "vertical"]).size()
    hits: dict = defaultdict(Counter)
    ent_vert: dict = {}
    for llm, vert, ents in zip(one["llm"], one["vertical"], one["ents_win"]):
        for e in ents:
            hits[llm][e] += 1
            ent_vert[e] = vert
    entities = sorted(ent_vert)
    engines = [e for e in ENGINES if e in set(one["llm"])]
    rate = pd.DataFrame(index=entities, columns=engines, dtype=float)
    count = pd.DataFrame(index=entities, columns=engines, dtype=float)
    for e in entities:
        v = ent_vert[e]
        for g in engines:
            n = denom.get((g, v), 0)
            c = hits[g][e]
            count.loc[e, g] = c
            rate.loc[e, g] = c / n if n else np.nan
    rate["vertical"] = [ent_vert[e] for e in entities]
    count["vertical"] = [ent_vert[e] for e in entities]
    return rate, count


def dendrogram_text(dist: pd.DataFrame, method: str = "average") -> list[str]:
    """Average-linkage tree over 1 - Pearson r between engine coverage vectors."""
    labels = list(dist.index)
    Z = linkage(squareform(dist.to_numpy(), checks=False), method=method)
    members = {i: [labels[i]] for i in range(len(labels))}
    lines = []
    for i, (a, b, h, _) in enumerate(Z):
        a, b = int(a), int(b)
        node = len(labels) + i
        members[node] = members[a] + members[b]
        lines.append(f"  height {h:.3f}  {'+'.join(members[a])}"
                     f"  |  {'+'.join(members[b])}")
    return lines


# ---------------------------------------------------------------------------
# 6. Null simulation
# ---------------------------------------------------------------------------

def permutation_null_fleiss(mat: np.ndarray, n_boot: int,
                            rng: np.random.Generator) -> np.ndarray:
    """Fleiss under independence with each engine's marginal held fixed.

    Permuting each column independently destroys any cell-level association
    while preserving every engine's base rate, which is exactly the null the
    "beyond chance" in kappa is supposed to refer to. Sampling error makes the
    realised null sit slightly below zero rather than exactly at it.
    """
    N, k = mat.shape
    out = np.empty(n_boot)
    work = mat.copy()
    for b in range(n_boot):
        for j in range(k):
            work[:, j] = rng.permutation(mat[:, j])
        out[b] = fleiss_from_counts(work.sum(axis=1), k)
    return out


# ---------------------------------------------------------------------------
# Reporting helpers
# ---------------------------------------------------------------------------

def md_table(df: pd.DataFrame, floatfmt: str = "{:.3f}") -> str:
    def fmt(x):
        if isinstance(x, float):
            return "—" if not np.isfinite(x) else floatfmt.format(x)
        return str(x)
    cols = list(df.columns)
    head = "| " + " | ".join(cols) + " |"
    rule = "|" + "|".join(["---"] * len(cols)) + "|"
    body = ["| " + " | ".join(fmt(v) for v in row) + " |"
            for row in df.itertuples(index=False)]
    return "\n".join([head, rule] + body)


def h(title: str) -> None:
    print(f"\n\n{'=' * 78}\n{title}\n{'=' * 78}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--boot", type=int, default=2000)
    ap.add_argument("--nullsim", type=int, default=2000)
    ap.add_argument("--cache", type=Path, default=None)
    args = ap.parse_args()
    rng = np.random.default_rng(SEED)
    t0 = time.time()

    # -- 0. extraction ------------------------------------------------------
    raw = load_panel(args.cache)
    h("S3.0  PANEL, HARMONISED OUTCOME AND TEST-RETEST CEILING")
    print(f"canonical rows (COALESCE(is_probe,0)=0): {len(raw)}")
    print(f"collection days: {raw['day'].nunique()}   "
          f"canonical queries: {raw['query'].nunique()}   "
          f"engines: {raw['llm'].nunique()}")
    print(f"series: {raw['day'].min()} to {raw['day'].max()}")
    print(f"\nTable S3.0a — window harmonisation check "
          f"(re-extraction at {WINDOW} chars vs stored cited_v2)")
    chk = harmonisation_check(raw).round(2).reset_index()
    print(md_table(chk, "{:.2f}"))

    rep = replicate_concordance(raw).round(4).reset_index()
    print("\nTable S3.0b — same engine, same query, same day: test-retest")
    print(md_table(rep, "{:.4f}"))

    one = first_run(raw)
    print(f"\ncells after reducing replicates to the earliest run: {len(one)}")
    print("cells per engine:")
    print(one.groupby("llm").size().reindex(
        [e for e in ENGINES if e in set(one['llm'])]).to_string())
    implementation_checks(one)

    # -- 1. Fleiss ----------------------------------------------------------
    h("S3.1  FLEISS' KAPPA ON THE BINARY OUTCOME")
    fleiss_rows = []
    panels_built = {}
    for name, engs, note in PANELS:
        w = build_panel(one, engs)
        panels_built[name] = (engs, w, note)
        if w.empty:
            fleiss_rows.append(dict(panel=name, engines="+".join(engs),
                                    k=len(engs), n_cells=0, days=0,
                                    base_rate=float("nan"),
                                    kappa=float("nan"), lo=float("nan"),
                                    hi=float("nan"), note="no complete cell"))
            continue
        mat = w[list(engs)].to_numpy().astype(int)
        n1 = mat.sum(axis=1)
        days = w["day"].to_numpy()
        kap = fleiss_from_counts(n1, len(engs))
        lo, hi, _ = cluster_bootstrap(
            n1, days, lambda v, k=len(engs): fleiss_from_counts(v, k),
            args.boot, rng)
        fleiss_rows.append(dict(
            panel=name, engines="+".join(engs), k=len(engs), n_cells=len(w),
            days=int(w["day"].nunique()), base_rate=float(mat.mean()),
            kappa=kap, lo=lo, hi=hi, note=note))
    fl = pd.DataFrame(fleiss_rows)
    fl.insert(fl.columns.get_loc("note"), "band",
              [lk_label(k) for k in fl["kappa"]])
    print("Table S3.1a — Fleiss' kappa by panel "
          f"(cluster bootstrap over collection days, B={args.boot})")
    print(md_table(fl, "{:.4f}"))

    print("\nTable S3.1b — Fleiss' kappa by vertical, within panel")
    rows = []
    for name, (engs, w, _) in panels_built.items():
        if w.empty:
            continue
        for v in VERTICALS:
            wv = w[w["vertical"] == v]
            if wv.empty:
                continue
            mat = wv[list(engs)].to_numpy().astype(int)
            n1 = mat.sum(axis=1)
            lo, hi, _ = cluster_bootstrap(
                n1, wv["day"].to_numpy(),
                lambda x, k=len(engs): fleiss_from_counts(x, k),
                max(500, args.boot // 4), rng)
            rows.append(dict(panel=name, vertical=VLABEL[v], k=len(engs),
                             n_cells=len(wv), base_rate=float(mat.mean()),
                             kappa=fleiss_from_counts(n1, len(engs)),
                             lo=lo, hi=hi))
    print(md_table(pd.DataFrame(rows), "{:.4f}"))

    # engine base rates, which bound kappa
    print("\nTable S3.1c — engine base rates on the harmonised outcome")
    br = (one.groupby("llm")["cited_win"].agg(["size", "mean"])
            .reindex([e for e in ENGINES if e in set(one["llm"])]))
    br["pct"] = 100 * br["mean"]
    br["class"] = [ENGINE_CLASS[i] for i in br.index]
    print(md_table(br.reset_index()[["llm", "class", "size", "pct"]], "{:.2f}"))

    # -- 2. pairwise --------------------------------------------------------
    h("S3.2  PAIRWISE AGREEMENT (COHEN'S KAPPA, PHI, OBSERVED AGREEMENT)")
    pt = pair_tables(one)
    rows = []
    for (a, b), val in pt.items():
        if val is None:
            rows.append(dict(pair=f"{a}-{b}", n=0, po=float("nan"),
                             pa=float("nan"), pb=float("nan"),
                             kappa=float("nan"), lo=float("nan"),
                             hi=float("nan"), phi=float("nan"),
                             kappa_max=float("nan")))
            continue
        days, A, B = val
        st = kappa_phi(A, B)
        # resample days on the paired cells, keeping A and B aligned
        uniq = np.unique(days)
        idx_by_day = {d: np.flatnonzero(days == d) for d in uniq}
        reps = np.empty(args.boot)
        for i in range(args.boot):
            pick = rng.choice(uniq, size=uniq.size, replace=True)
            sel = np.concatenate([idx_by_day[d] for d in pick])
            reps[i] = kappa_phi(A[sel], B[sel])["kappa"]
        reps = reps[np.isfinite(reps)]
        rows.append(dict(pair=f"{a}-{b}", n=st["n"], po=st["po"], pa=st["pa"],
                         pb=st["pb"], kappa=st["kappa"],
                         lo=float(np.percentile(reps, 2.5)),
                         hi=float(np.percentile(reps, 97.5)),
                         phi=st["phi"], kappa_max=st["kappa_max"]))
    pw = pd.DataFrame(rows)
    pw["band"] = [lk_label(k) for k in pw["kappa"]]
    print("Table S3.2a — all engine pairs, maximal shared-cell overlap")
    print(md_table(pw, "{:.4f}"))

    print("\nTable S3.2b — Cohen's kappa matrix (lower triangle)")
    km = pd.DataFrame(index=list(ENGINES), columns=list(ENGINES), dtype=float)
    pom = pd.DataFrame(index=list(ENGINES), columns=list(ENGINES), dtype=float)
    for (a, b), val in pt.items():
        if val is None:
            continue
        _, A, B = val
        st = kappa_phi(A, B)
        km.loc[a, b] = km.loc[b, a] = st["kappa"]
        pom.loc[a, b] = pom.loc[b, a] = st["po"]
    for e in ENGINES:
        km.loc[e, e] = 1.0
        pom.loc[e, e] = 1.0
    print(md_table(km.reset_index().rename(columns={"index": "engine"}),
                   "{:.3f}"))
    print("\nTable S3.2c — observed agreement P_o matrix")
    print(md_table(pom.reset_index().rename(columns={"index": "engine"}),
                   "{:.3f}"))

    # -- 3. entity sets -----------------------------------------------------
    h("S3.3  AGREEMENT ON WHICH ENTITIES ARE NAMED")
    setdf, dists = set_agreement(one)
    nent = one["ents_win"].map(len)
    named = nent[nent > 0]
    print(f"entities named per cell: mean {nent.mean():.3f}, "
          f"median {nent.median():.0f}; among cells with >=1 entity: "
          f"mean {named.mean():.3f}, median {named.median():.0f}, "
          f"p90 {np.percentile(named, 90):.0f}, max {named.max()}")
    print("\nTable S3.3a — Jaccard and RBO over cells where at least one "
          "engine named an entity")
    print(md_table(setdf, "{:.3f}"))

    print("\nTable S3.3b — Jaccard distribution, deciles, pooled over pairs")
    allj = np.concatenate([v[0] for v in dists.values()])
    dec = pd.DataFrame({
        "decile": [f"p{p}" for p in range(10, 100, 10)],
        "jaccard": [float(np.percentile(allj, p)) for p in range(10, 100, 10)],
    })
    print(md_table(dec, "{:.3f}"))
    print(f"pooled scored cell-pairs: {allj.size}; "
          f"share exactly 0: {100 * np.mean(allj == 0):.1f}%; "
          f"share exactly 1: {100 * np.mean(allj == 1):.1f}%")

    print("\nTable S3.3c — Kendall tau-b between engines on the entity "
          "coverage ranking, by vertical")
    rate, count = coverage_matrix(one)
    rows = []
    for v in VERTICALS:
        sub = rate[rate["vertical"] == v].drop(columns="vertical")
        for a, b in itertools.combinations(sub.columns, 2):
            x, y = sub[a], sub[b]
            m = x.notna() & y.notna()
            if m.sum() < 4:
                continue
            tau, p = sps.kendalltau(x[m], y[m], variant="b")
            rows.append(dict(vertical=VLABEL[v], pair=f"{a}-{b}",
                             n_entities=int(m.sum()), tau_b=tau, p=p))
    tk = pd.DataFrame(rows)
    print(md_table(tk, "{:.3f}"))
    print("\nTable S3.3d — Kendall tau-b summary by pair, across verticals")
    print(md_table(tk.groupby("pair")["tau_b"].agg(
        ["count", "mean", "min", "max"]).round(3).reset_index(), "{:.3f}"))

    # -- 4. latent structure ------------------------------------------------
    h("S3.4  LATENT STRUCTURE OF THE ENGINE PANEL")
    M = rate.drop(columns="vertical")
    M = M.dropna(axis=0, how="any")
    print(f"entity x engine coverage matrix: {M.shape[0]} entities "
          f"x {M.shape[1]} engines. Rows are the cohort members named at least "
          "once by at least one engine in the window; a zero row would carry no "
          "information about engine similarity and none of the dropped members "
          "was ever named.")
    Z = (M - M.mean()) / M.std(ddof=1)
    pca = PCA(n_components=min(M.shape[1], M.shape[0]))
    scores = pca.fit_transform(Z.to_numpy())
    evr = pca.explained_variance_ratio_
    print("\nTable S3.4a — PCA of the standardised entity x engine matrix")
    print(md_table(pd.DataFrame({
        "component": [f"PC{i+1}" for i in range(len(evr))],
        "explained_variance": evr,
        "cumulative": np.cumsum(evr),
    }), "{:.4f}"))
    load = pd.DataFrame(pca.components_[:3].T, index=M.columns,
                        columns=["PC1", "PC2", "PC3"])
    load["class"] = [ENGINE_CLASS[i] for i in load.index]
    print("\nTable S3.4b — engine loadings on the first three components")
    print(md_table(load.reset_index().rename(columns={"index": "engine"}),
                   "{:.3f}"))

    corr = M.corr(method="pearson")
    print("\nTable S3.4c — Pearson correlation of engine coverage vectors")
    print(md_table(corr.reset_index().rename(columns={"index": "engine"}),
                   "{:.3f}"))
    dist = (1 - corr).copy()
    dv = dist.to_numpy(copy=True)
    np.fill_diagonal(dv, 0.0)
    dist = pd.DataFrame(dv, index=corr.index, columns=corr.columns)
    print("\nDendrogram (average linkage on 1 - Pearson r), merges in order:")
    for line in dendrogram_text(dist):
        print(line)

    # variance decomposition: is coverage an entity property or an engine one?
    h("S3.4-bis  VARIANCE DECOMPOSITION: FIRM EFFECT VS ENGINE EFFECT")
    long = M.stack().rename("rate").reset_index()
    long.columns = ["entity", "engine", "rate"]
    cnt = count.drop(columns="vertical").stack().rename("hits").reset_index()
    cnt.columns = ["entity", "engine", "hits"]
    long = long.merge(cnt, on=["entity", "engine"])
    eps = 1.0 / (2 * len(one))
    long["logit"] = np.log((long["rate"] + eps) / (1 - long["rate"] + eps))
    gm = long["logit"].mean()
    ss_tot = float(((long["logit"] - gm) ** 2).sum())
    ent_m = long.groupby("entity")["logit"].transform("mean")
    eng_m = long.groupby("engine")["logit"].transform("mean")
    ss_ent = float(((ent_m - gm) ** 2).sum())
    ss_eng = float(((eng_m - gm) ** 2).sum())
    ss_res = float(((long["logit"] - ent_m - eng_m + gm) ** 2).sum())
    print("Two-way decomposition of logit coverage over "
          f"{long['entity'].nunique()} entities x {long['engine'].nunique()} "
          "engines (balanced, no replication)")
    print(md_table(pd.DataFrame({
        "source": ["entity (firm)", "engine", "residual (interaction)"],
        "sum_of_squares": [ss_ent, ss_eng, ss_res],
        "share_of_total": [ss_ent / ss_tot, ss_eng / ss_tot, ss_res / ss_tot],
    }), "{:.4f}"))

    # cell-level counterpart
    cell = one.copy()
    y = cell["cited_win"].to_numpy(dtype=float)
    tot = float(((y - y.mean()) ** 2).sum())
    def fac_r2(col):
        m = cell.groupby(col)["cited_win"].transform("mean").to_numpy()
        return float(((m - y.mean()) ** 2).sum() / tot)
    print("\nTable S3.4d — share of cell-level variance in the binary outcome "
          f"explained by single factors (N = {len(cell)} cells)")
    print("The engine x query row fits one mean per cell of a 6 x 192 grid "
          "and is an upper bound, not an effect: with "
          f"{one.groupby(['llm', 'query']).ngroups} group means over "
          f"{len(cell)} observations it is close to saturated.")
    print(md_table(pd.DataFrame({
        "factor": ["engine", "query (192 levels)", "vertical",
                   "query language", "query type", "collection day",
                   "engine x query"],
        "r2": [fac_r2("llm"), fac_r2("query"), fac_r2("vertical"),
               fac_r2("query_lang"), fac_r2("query_type"), fac_r2("day"),
               float(((cell.groupby(["llm", "query"])["cited_win"]
                       .transform("mean").to_numpy() - y.mean()) ** 2).sum()
                     / tot)],
    }), "{:.4f}"))

    # -- 5. entity breadth --------------------------------------------------
    h("S3.5  ENTITIES AS THE OBJECT: BREADTH AND COVERAGE")
    cm = count.drop(columns="vertical")
    breadth = (cm > 0).sum(axis=1)
    denom_tot = {}
    dn = one.groupby(["llm", "vertical"]).size()
    for e in cm.index:
        v = count.loc[e, "vertical"]
        denom_tot[e] = sum(dn.get((g, v), 0) for g in cm.columns)
    ent = pd.DataFrame({
        "entity": cm.index,
        "vertical": [VLABEL[count.loc[e, "vertical"]] for e in cm.index],
        "breadth": breadth.values,
        "hits": cm.sum(axis=1).values,
        "trials": [denom_tot[e] for e in cm.index],
    })
    ent["coverage"] = ent["hits"] / ent["trials"]
    print(f"entities ever named in the {WINDOW}-character window: {len(ent)}; "
          f"extractor cohort {sum(COHORT_SIZE.values())} "
          f"({', '.join(f'{VLABEL[v]} {COHORT_SIZE[v]}' for v in VERTICALS)}), "
          f"so {sum(COHORT_SIZE.values()) - len(ent)} cohort members were never "
          "named by any engine on any day inside the window")
    print("\nTable S3.5a — breadth distribution "
          "(number of engines that ever named the entity)")
    bd = (ent.groupby("breadth")
             .agg(n_entities=("entity", "size"),
                  median_coverage=("coverage", "median"),
                  mean_coverage=("coverage", "mean"),
                  total_hits=("hits", "sum"))
             .reset_index())
    bd["pct_of_all_citations"] = 100 * bd["total_hits"] / bd["total_hits"].sum()
    print(md_table(bd, "{:.5f}"))

    print("\nTable S3.5b — entities named by exactly one engine")
    solo = ent[ent["breadth"] == 1].copy()
    which = []
    for e in solo["entity"]:
        which.append(",".join(cm.columns[np.asarray(cm.loc[e] > 0)]))
    solo["only_engine"] = which
    print(md_table(solo[["entity", "vertical", "only_engine", "hits",
                         "trials", "coverage"]]
                   .sort_values("hits", ascending=False), "{:.5f}"))

    print("\nTable S3.5c — the twelve most widely named entities")
    top = ent.sort_values(["breadth", "hits"], ascending=False).head(12)
    print(md_table(top[["entity", "vertical", "breadth", "hits", "trials",
                        "coverage"]], "{:.4f}"))

    # declared model: binomial GLM, logit link, breadth as the predictor
    import statsmodels.api as sm
    X = sm.add_constant(ent["breadth"].astype(float).to_numpy())
    endog = np.column_stack([ent["hits"].to_numpy(),
                             (ent["trials"] - ent["hits"]).to_numpy()])
    glm = sm.GLM(endog, X, family=sm.families.Binomial()).fit()
    # Quasi-binomial: entity counts are heavily overdispersed relative to a
    # binomial (the same firm is named in bursts within a query and a day), so
    # the iid interval is meaningless. Scale computed by hand as Pearson
    # chi-square over residual degrees of freedom; statsmodels' scale="X2"
    # rescales by the binomial denominator on a two-column endog.
    phi_scale = float(glm.pearson_chi2 / glm.df_resid)
    se_quasi = float(glm.bse[1] * math.sqrt(phi_scale))
    rho, prho = sps.spearmanr(ent["breadth"], ent["coverage"])
    print("\nModel S3.5 — Binomial GLM with logit link:")
    print("    hits_e ~ Binomial(trials_e, pi_e),  "
          "logit(pi_e) = b0 + b1 * breadth_e")
    print(f"    entities N = {len(ent)}; trials = {int(ent['trials'].sum())}; "
          f"hits = {int(ent['hits'].sum())}")
    print(f"    b1 = {glm.params[1]:.4f}  (SE iid {glm.bse[1]:.4f}, "
          f"SE quasi-binomial {se_quasi:.4f}, "
          f"overdispersion scale {phi_scale:.1f})")
    print(f"    odds ratio per additional engine = "
          f"{math.exp(glm.params[1]):.3f} "
          f"[{math.exp(glm.params[1] - 1.96 * se_quasi):.3f}, "
          f"{math.exp(glm.params[1] + 1.96 * se_quasi):.3f}] "
          "(quasi-binomial interval)")
    print(f"    deviance {glm.deviance:.1f} on {glm.df_resid} df; "
          f"null deviance {glm.null_deviance:.1f}; "
          f"pseudo-R2 (deviance) {1 - glm.deviance / glm.null_deviance:.4f}")
    print(f"    Spearman rho(breadth, coverage) = {rho:.3f} (p = {prho:.3g})")

    # -- 6. null simulation -------------------------------------------------
    h("S3.6  NULL SIMULATION: HOW MUCH AGREEMENT IS THE FLOOR?")
    rows = []
    for name, (engs, w, note) in panels_built.items():
        if w.empty:
            continue
        mat = w[list(engs)].to_numpy().astype(int)
        obs = fleiss_from_counts(mat.sum(axis=1), len(engs))
        null = permutation_null_fleiss(mat, args.nullsim, rng)
        rows.append(dict(panel=name, k=len(engs), n_cells=len(w),
                         observed=obs, null_mean=float(null.mean()),
                         null_sd=float(null.std(ddof=1)),
                         null_p95=float(np.percentile(null, 95)),
                         z=(obs - null.mean()) / null.std(ddof=1),
                         p_ge=float((null >= obs).mean())))
    print("Table S3.6a — Fleiss against a marginal-preserving permutation null "
          f"(B = {args.nullsim})")
    print(md_table(pd.DataFrame(rows), "{:.4f}"))

    print("\nTable S3.6b — observed Jaccard against the uniform-draw null of "
          "src/analysis/null_simulation.py")
    named_universe = {v: int((rate["vertical"] == v).sum()) for v in VERTICALS}
    rows = []
    for v in VERTICALS:
        for label, size in (("named universe", named_universe[v]),
                            ("extractor cohort", COHORT_SIZE[v])):
            for topk in (1, 2, 3):
                res = simulate_jaccard_null(cohort_size=size, top_k=topk,
                                            n_llms=2, n_simulations=2000,
                                            seed=SEED)
                rows.append(dict(vertical=VLABEL[v], universe=label,
                                 size=size, top_k=topk,
                                 null_mean=res.mean, null_p50=res.p50,
                                 null_p95=res.p95))
    print(md_table(pd.DataFrame(rows), "{:.4f}"))
    print("Two universes are simulated. The named universe is the set of cohort "
          "members any engine ever named inside the window, which is the widest "
          "set the observed Jaccard could have drawn from; the extractor cohort "
          "is the set the instrument was actually looking for. The null is the "
          "mean Jaccard of two independent uniform draws of top_k members, "
          "which is the comparator for the both-named observed value, since "
          "both simulated raters name something by construction. At top_k = 1 "
          "the simulated Jaccard is 0 or 1, so its p95 is uninformative.")
    obs_by_v = []
    wideE = one.pivot_table(index=["day", "query", "vertical"], columns="llm",
                            values="ents_win", aggfunc="first")
    for v in VERTICALS:
        sel = wideE[[ix[2] == v for ix in wideE.index]]
        vals, both = [], []
        for a, b in itertools.combinations(ENGINES, 2):
            if a not in sel.columns or b not in sel.columns:
                continue
            ss = sel[[a, b]].dropna()
            for ea, eb in zip(ss[a], ss[b]):
                sa, sb = frozenset(ea), frozenset(eb)
                if sa or sb:
                    vals.append(jaccard(sa, sb))
                if sa and sb:
                    both.append(jaccard(sa, sb))
        obs_by_v.append(dict(vertical=VLABEL[v], n_pairs_cells=len(vals),
                             observed_mean_jaccard=float(np.mean(vals)),
                             observed_median=float(np.median(vals)),
                             n_both_named=len(both),
                             mean_jaccard_both_named=float(np.mean(both))))
    print("\nTable S3.6c — observed pairwise Jaccard by vertical")
    print(md_table(pd.DataFrame(obs_by_v), "{:.4f}"))

    # -- 7. the window: what the outcome cannot separate --------------------
    h("S3.7  THE OBSERVATION WINDOW: AGREEMENT UNDER TWO APERTURES")
    con = C.connect()
    cur = con.cursor()
    cur.execute(
        f"""SELECT id, timestamp, date(timestamp) AS day, llm, vertical, query,
                   response_text, response_full_text
              FROM citations
             WHERE {C.CANONICAL}
               AND response_full_text IS NOT NULL
               AND length(response_full_text) > 0
             ORDER BY timestamp, id"""
    )
    ex = C.build_extractors()
    frecs = []
    for r in cur:
        full = r["response_full_text"] or ""
        w_ents = tuple(sorted({m.entity for m in
                               ex[r["vertical"]].extract(full[:WINDOW])}))
        f_ents = tuple(sorted({m.entity for m in
                               ex[r["vertical"]].extract(full)}))
        frecs.append((r["id"], r["timestamp"], r["day"], r["llm"],
                      r["vertical"], r["query"], 1 if w_ents else 0,
                      1 if f_ents else 0, w_ents, f_ents, len(full)))
    con.close()
    fdf = pd.DataFrame.from_records(
        frecs, columns=["row_id", "ts", "day", "llm", "vertical", "query",
                        "cited_win", "cited_full", "ents_win", "ents_full",
                        "len_full"])
    fdf = (fdf.sort_values(["ts", "row_id"])
              .drop_duplicates(subset=["day", "query", "llm"], keep="first"))
    print(f"rows with the full response retained: {len(fdf)} "
          f"on {fdf['day'].nunique()} days "
          f"({fdf['day'].min()} to {fdf['day'].max()})")
    print("\nTable S3.7a — same rows, two apertures, by engine")
    g = fdf.groupby("llm")
    ap = pd.DataFrame({
        "n": g.size(),
        "pct_cited_window200": 100 * g["cited_win"].mean(),
        "pct_cited_full": 100 * g["cited_full"].mean(),
        "median_len_full": g["len_full"].median(),
        "mean_entities_window": g["ents_win"].apply(lambda s: s.map(len).mean()),
        "mean_entities_full": g["ents_full"].apply(lambda s: s.map(len).mean()),
    }).reindex([e for e in ENGINES if e in set(fdf["llm"])])
    ap["delta_pp"] = ap["pct_cited_full"] - ap["pct_cited_window200"]
    print(md_table(ap.reset_index(), "{:.2f}"))

    day_all = (fdf.groupby("day")["llm"].nunique().idxmax())
    sub = fdf[fdf["day"] == day_all]
    engs_here = tuple(e for e in ENGINES if e in set(sub["llm"]))
    print(f"\nrichest day for this comparison: {day_all}, "
          f"engines {engs_here}")
    rows = []
    for outcome, ecol in (("window 200", "cited_win"), ("full text", "cited_full")):
        wide = sub.pivot_table(index=["query", "vertical"], columns="llm",
                               values=ecol, aggfunc="first")
        for engs in (engs_here, tuple(e for e in engs_here if e != "Perplexity")):
            ww = wide[list(engs)].dropna()
            if ww.empty:
                continue
            mat = ww.to_numpy().astype(int)
            rows.append(dict(aperture=outcome, engines="+".join(engs),
                             k=len(engs), n_cells=len(ww),
                             base_rate=float(mat.mean()),
                             fleiss=fleiss_from_counts(mat.sum(axis=1), len(engs))))
    print("\nTable S3.7b — Fleiss on identical cells under both apertures")
    print(md_table(pd.DataFrame(rows), "{:.4f}"))

    rows = []
    for outcome, ecol, scol in (("window 200", "cited_win", "ents_win"),
                                ("full text", "cited_full", "ents_full")):
        wide = sub.pivot_table(index=["query", "vertical"], columns="llm",
                               values=ecol, aggfunc="first")
        wideS = sub.pivot_table(index=["query", "vertical"], columns="llm",
                                values=scol, aggfunc="first")
        for a, b in itertools.combinations(engs_here, 2):
            s = wide[[a, b]].dropna()
            if s.empty:
                continue
            st = kappa_phi(s[a].to_numpy().astype(int),
                           s[b].to_numpy().astype(int))
            ss = wideS[[a, b]].dropna()
            js = [jaccard(frozenset(x), frozenset(y))
                  for x, y in zip(ss[a], ss[b])
                  if frozenset(x) or frozenset(y)]
            rows.append(dict(aperture=outcome, pair=f"{a}-{b}", n=st["n"],
                             po=st["po"], kappa=st["kappa"],
                             mean_jaccard=float(np.mean(js)) if js else float("nan")))
    print("\nTable S3.7c — pairwise agreement on identical cells, both apertures")
    print(md_table(pd.DataFrame(rows), "{:.4f}"))

    # -- sensitivity: agreement on the outcome as stored --------------------
    h("S3.8  SENSITIVITY: AGREEMENT ON THE OUTCOME AS STORED (cited_v2)")
    rows = []
    for name, engs, note in PANELS:
        w = build_panel(one, engs, outcome="cited_v2")
        if w.empty:
            continue
        mat = w[list(engs)].to_numpy().astype(int)
        rows.append(dict(panel=name, engines="+".join(engs), k=len(engs),
                         n_cells=len(w), base_rate=float(mat.mean()),
                         kappa_stored=fleiss_from_counts(mat.sum(axis=1), len(engs))))
    st_df = pd.DataFrame(rows).merge(
        fl[["panel", "kappa"]].rename(columns={"kappa": "kappa_harmonised"}),
        on="panel", how="left")
    print("Table S3.8 — Fleiss on the stored outcome vs the harmonised outcome")
    print(md_table(st_df, "{:.4f}"))

    # -- 9. headline summary ------------------------------------------------
    h("S3.9  HEADLINE SUMMARY")
    defined = pw[np.isfinite(pw["kappa"])]
    print(f"pairs with any shared cell: {len(defined)} of "
          f"{len(pw)} ({len(ENGINES)} engines); "
          f"Cohen kappa mean {defined['kappa'].mean():.4f}, "
          f"median {defined['kappa'].median():.4f}, "
          f"range {defined['kappa'].min():.4f} to {defined['kappa'].max():.4f}")
    print(f"observed agreement P_o mean {defined['po'].mean():.4f}, "
          f"range {defined['po'].min():.4f} to {defined['po'].max():.4f}")
    print(f"phi mean {defined['phi'].mean():.4f}, "
          f"range {defined['phi'].min():.4f} to {defined['phi'].max():.4f}")
    print(f"kappa as a fraction of the marginal-constrained maximum: mean "
          f"{(defined['kappa'] / defined['kappa_max']).mean():.4f}")
    tkd = tk[np.isfinite(tk["tau_b"])]
    print(f"\nKendall tau-b on entity coverage ranks: {len(tkd)} defined "
          f"vertical x pair combinations of {len(tk)}; mean "
          f"{tkd['tau_b'].mean():.4f}, median {tkd['tau_b'].median():.4f}, "
          f"share above 0.5: {100 * float((tkd['tau_b'] > 0.5).mean()):.1f}%, "
          f"share below 0: {100 * float((tkd['tau_b'] < 0).mean()):.1f}%")

    # First-named entity: when both engines name someone, is it the same one?
    wideE2 = one.pivot_table(index=["day", "query", "vertical"], columns="llm",
                             values="ents_win", aggfunc="first")
    rows = []
    for a, b in itertools.combinations(ENGINES, 2):
        if a not in wideE2.columns or b not in wideE2.columns:
            continue
        ss = wideE2[[a, b]].dropna()
        hit = tot = 0
        for ea, eb in zip(ss[a], ss[b]):
            if ea and eb:
                tot += 1
                hit += int(ea[0] == eb[0])
        if tot:
            rows.append(dict(pair=f"{a}-{b}", n_both_named=tot,
                             pct_same_first=100 * hit / tot))
    fn = pd.DataFrame(rows)
    print("\nTable S3.9 — when both engines name someone, is the first name "
          "the same?")
    print(md_table(fn, "{:.2f}"))
    print(f"pooled: {int(fn['n_both_named'].sum())} cell-pairs, "
          f"{(fn['pct_same_first'] * fn['n_both_named']).sum() / fn['n_both_named'].sum():.2f}% "
          "share the first-named entity")

    print(f"\n\n[done in {time.time() - t0:.1f}s; seed {SEED}; "
          f"bootstrap B={args.boot}; null B={args.nullsim}]")


if __name__ == "__main__":
    main()
