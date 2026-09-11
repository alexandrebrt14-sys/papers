#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S2 - Temporal stability of the BRGEO-1 citation series.

Reproducible script behind `S2-temporal.md`. Read-only against the database.

WHAT IT DOES
    1. Rebuilds the daily per-engine citation series under a uniform 200-character
       observation window, re-running the project's own entity extractor over
       `citations.response_text[:200]`. Emits Wilson intervals, n per day, and a
       partial-day flag.
    2. Trend per engine: Theil-Sen slope, Mann-Kendall (tie-corrected, plus the
       Hamed-Rao variance correction for serial dependence) and a day-index
       logistic regression with day-clustered standard errors. Benjamini-Hochberg
       across the family. Effect size in percentage points per 30 days.
    3. Change points detected blind to the event table (binomial binary
       segmentation with a permutation test; `ruptures` as corroboration), then
       confronted with the declared instrument events.
    4. Autocorrelation of the daily series and the design effect this implies for
       the standard error of any aggregate of the study.
    5. Round (06:00 BRT vs 18:00 BRT) and weekday/weekend effects.
    6. Weekly ranking stability for entities and for engines (Kendall tau-b).
    7. Difference-in-differences for the 2026-06-17 Gemini event and an
       instrument-stability check around the 2026-08-19 arm swap.

HARD RULES OBSERVED
    * The database is opened read-only (`mode=ro`). Nothing is written to it.
    * Partial days are never imputed. They stay in the primary cut, marked, and
      every headline number is recomputed on complete days only as a sensitivity.
    * Every number in `S2-temporal.md` comes from `s2_results.json` or from the
      CSVs this script writes.

USAGE
    python s2_temporal.py
    python s2_temporal.py --db <path> --out <dir> --repo <papers repo root>

DEPENDENCIES
    numpy, pandas, scipy, statsmodels, and the `papers` repository on sys.path
    (for `src.analysis.entity_extraction`). `ruptures` is optional; when it is
    absent the script reports the corroboration step as NOT RUN and the primary
    binomial segmentation still runs.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sqlite3
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests
import statsmodels.api as sm

RNG = np.random.default_rng(20260911)

# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------

WINDOW_CHARS = 200
BRT_OFFSET_HOURS = -3          # collection day is the local Brazilian date
ROUND_SPLIT_HOUR_BRT = 18      # < 18h BRT -> morning run; >= 18h BRT -> evening run
MIN_SEG_DAYS = 3               # minimum days per segment in change-point search
N_PERM = 999                   # permutations for the change-point test
N_BOOT = 2000                  # parametric bootstrap draws for marginal effects
ALPHA = 0.05

VERTICALS = ("fintech", "varejo", "saude", "tecnologia")

# Engines. Groq and Grok occupy the same panel slot at different times and are
# treated as two distinct series, never as one.
ENGINES = ["ChatGPT", "Claude", "Gemini", "Perplexity", "Groq", "Grok"]
CONTINUOUS_ENGINES = ["ChatGPT", "Claude", "Gemini", "Perplexity"]

# Declared instrument events, transcribed from
# docs/research/methods-paper/journal-v2/research/R3-fieldlog.md section 3
# ("Series events, in manuscript table format"). Dates are the declared dates,
# not dates inferred from the data. `arms` lists the series each event can move.
DECLARED_EVENTS = [
    dict(date="2026-04-30", arms=["ChatGPT", "Claude", "Gemini", "Perplexity", "Groq"],
         change="adversarial probes activated; query_type re-annotated on 4,284 rows",
         klass="battery / battery annotation",
         status="declared (CHANGELOG.md:254-255) + candidate"),
    dict(date="2026-06-05", arms=["Gemini"],
         change="GEMINI_THINKING_BUDGET set to 1024; Gemini dropped from MANDATORY_LLMS",
         klass="generation configuration",
         status="candidate (ROADMAP_2026Q2-Q4.md:26-36)"),
    dict(date="2026-06-17", arms=["Gemini"],
         change="gemini-2.5-pro -> gemini-2.5-flash; thinking budget 1024 -> 0",
         klass="model version + generation configuration",
         status="declared (METHODOLOGY_V2.md:91-92; MANUSCRIPT.md:331)"),
    dict(date="2026-08-17", arms=["Groq"],
         change="Groq retires llama-3.3-70b-versatile; five collections abort at preflight",
         klass="provider-imposed outage",
         status="declared (CHANGELOG.md:180-186)"),
    dict(date="2026-08-19", arms=["Groq", "Grok"],
         change="panel slot 5 replaced: Groq llama-3.3-70b -> xAI grok-4.6",
         klass="engine replacement",
         status="declared (METHODOLOGY_V2.md:72-77; MANUSCRIPT.md:332)"),
    dict(date="2026-08-19", arms=["ChatGPT", "Claude", "Gemini", "Perplexity", "Groq", "Grok"],
         change="TLS delegated to the OS certificate store (truststore)",
         klass="transport; declared to have no effect on data",
         status="declared non-event (CHANGELOG.md:172-176)"),
    dict(date="2026-08-31", arms=["Perplexity"],
         change="observation window unified at 200 characters across all arms",
         klass="window unified",
         status="declared (CHANGELOG.md:81-93; MANUSCRIPT.md:333)"),
    dict(date="2026-08-31", arms=["Grok"],
         change="XAI_REASONING_EFFORT reduced to low",
         klass="generation configuration",
         status="declared (CHANGELOG.md:136-148; MANUSCRIPT.md:334)"),
    dict(date="2026-08-31", arms=["Perplexity"],
         change="Perplexity added to the probe stratum (calibracao_fp routing)",
         klass="battery coverage",
         status="candidate (CHANGELOG.md:99-104)"),
    dict(date="2026-09-06", arms=["ChatGPT", "Claude"],
         change="arms absent; MANDATORY_LLMS downgraded as repository variable",
         klass="panel composition",
         status="declared (HEALTH-CHECK-APIS-20260908.md:44)"),
]

# Partial days declared in the documentation. Two sources, both transcribed:
#   (a) docs/METHODOLOGY_V2.md:116-133 missingness ledger (cells filled out of 20)
#   (b) data/partial_days.json (machine-written from 2026-09-09 onward, plus two
#       hand-seeded rows for 2026-09-06 and 2026-09-07)
DECLARED_PARTIAL_LEDGER = {
    "2026-04-23": "15 of 20 cells; collection interrupted (METHODOLOGY_V2.md:121)",
    "2026-04-24": "~15 Claude fintech rows as api_failure; Anthropic balance mid-run",
    "2026-05-01": "9 of 20 cells; health check failure (METHODOLOGY_V2.md:123)",
    "2026-05-04": "15 of 20 cells; partial recovery (METHODOLOGY_V2.md:125)",
    "2026-05-18": "5 of 20 cells; Perplexity max_tokens<16 rejected on sonar",
}


# --------------------------------------------------------------------------
# Small statistical helpers
# --------------------------------------------------------------------------

def wilson_ci(k: int, n: int, alpha: float = ALPHA) -> tuple[float, float]:
    """Wilson score interval for a binomial proportion."""
    if n == 0:
        return (float("nan"), float("nan"))
    z = stats.norm.ppf(1 - alpha / 2)
    p = k / n
    den = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / den
    half = (z / den) * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (max(0.0, centre - half), min(1.0, centre + half))


def mann_kendall(x: np.ndarray) -> dict:
    """Mann-Kendall trend test with tie correction and the Hamed-Rao variance
    correction for serially correlated data.

    Returns S, tau, the normal deviate and two-sided p under both the original
    variance and the Hamed-Rao corrected variance.
    """
    x = np.asarray(x, dtype=float)
    n = x.size
    if n < 4:
        return dict(n=n, S=np.nan, tau=np.nan, var_s=np.nan, z=np.nan, p=np.nan,
                    var_s_hr=np.nan, z_hr=np.nan, p_hr=np.nan, note="n<4, not run")
    s = 0.0
    for i in range(n - 1):
        s += np.sum(np.sign(x[i + 1:] - x[i]))
    # tie-corrected variance
    _, counts = np.unique(x, return_counts=True)
    tie_term = np.sum(counts * (counts - 1) * (2 * counts + 5))
    var_s = (n * (n - 1) * (2 * n + 5) - tie_term) / 18.0
    denom = 0.5 * n * (n - 1)
    tau = s / denom if denom else np.nan

    def _z(s_val, var_val):
        if var_val <= 0:
            return np.nan
        if s_val > 0:
            return (s_val - 1) / math.sqrt(var_val)
        if s_val < 0:
            return (s_val + 1) / math.sqrt(var_val)
        return 0.0

    z = _z(s, var_s)
    p = 2 * (1 - stats.norm.cdf(abs(z))) if np.isfinite(z) else np.nan

    # Hamed & Rao (1998): inflate the variance by the autocorrelation of the
    # de-trended ranks. Only significant lags contribute.
    ranks = stats.rankdata(x)
    slope = stats.theilslopes(x, np.arange(n))[0]
    detr = x - slope * np.arange(n)
    detr_ranks = stats.rankdata(detr)
    rho = []
    max_lag = max(1, n - 1)
    for lag in range(1, max_lag):
        a = detr_ranks[:-lag] - detr_ranks.mean()
        b = detr_ranks[lag:] - detr_ranks.mean()
        den = np.sum((detr_ranks - detr_ranks.mean()) ** 2)
        rho.append(np.sum(a * b) / den if den else 0.0)
    rho = np.asarray(rho)
    crit = stats.norm.ppf(1 - ALPHA / 2)
    sig = np.abs(rho) > crit / math.sqrt(n)
    corr = 1.0
    for lag in range(1, max_lag):
        if sig[lag - 1]:
            corr += (2.0 / (n * (n - 1) * (n - 2))) * (n - lag) * (n - lag - 1) * (n - lag - 2) * rho[lag - 1]
    corr = max(corr, 1e-6)
    var_hr = var_s * corr
    z_hr = _z(s, var_hr)
    p_hr = 2 * (1 - stats.norm.cdf(abs(z_hr))) if np.isfinite(z_hr) else np.nan
    return dict(n=n, S=float(s), tau=float(tau), var_s=float(var_s), z=float(z), p=float(p),
                var_s_hr=float(var_hr), z_hr=float(z_hr), p_hr=float(p_hr),
                hr_factor=float(corr), note="")


def binomial_loglik(k: np.ndarray, n: np.ndarray) -> float:
    """Log-likelihood of a single binomial rate fitted to the pooled counts."""
    K, N = float(np.sum(k)), float(np.sum(n))
    if N == 0:
        return 0.0
    p = K / N
    if p <= 0 or p >= 1:
        return 0.0
    return K * math.log(p) + (N - K) * math.log(1 - p)


def best_split(k: np.ndarray, n: np.ndarray, min_size: int) -> tuple[int, float]:
    """Single best binomial split. Returns (index of first day of the second
    segment, likelihood-ratio statistic)."""
    m = k.size
    if m < 2 * min_size:
        return -1, 0.0
    base = binomial_loglik(k, n)
    best_i, best_lr = -1, 0.0
    for i in range(min_size, m - min_size + 1):
        lr = 2 * (binomial_loglik(k[:i], n[:i]) + binomial_loglik(k[i:], n[i:]) - base)
        if lr > best_lr:
            best_i, best_lr = i, lr
    return best_i, best_lr


def perm_pvalue(k: np.ndarray, n: np.ndarray, lr_obs: float, min_size: int,
                n_perm: int = N_PERM) -> float:
    """Permutation p-value for a change point: the day order is shuffled, which
    destroys any temporal structure while preserving the daily (k, n) pairs."""
    if lr_obs <= 0:
        return 1.0
    idx = np.arange(k.size)
    count = 0
    for _ in range(n_perm):
        perm = RNG.permutation(idx)
        _, lr = best_split(k[perm], n[perm], min_size)
        if lr >= lr_obs:
            count += 1
    return (count + 1) / (n_perm + 1)


def binseg_binomial(k: np.ndarray, n: np.ndarray, min_size: int = MIN_SEG_DAYS,
                    alpha: float = ALPHA, n_perm: int = N_PERM, depth: int = 0,
                    offset: int = 0, out: list | None = None) -> list:
    """Binary segmentation on a binomial series with a permutation stopping rule.
    Detects change points without ever seeing the event table."""
    if out is None:
        out = []
    if depth > 4 or k.size < 2 * min_size:
        return out
    i, lr = best_split(k, n, min_size)
    if i < 0:
        return out
    p = perm_pvalue(k, n, lr, min_size, n_perm)
    if p > alpha:
        return out
    left_rate = float(np.sum(k[:i]) / max(1, np.sum(n[:i])))
    right_rate = float(np.sum(k[i:]) / max(1, np.sum(n[i:])))
    out.append(dict(index=offset + i, lr=float(lr), p_perm=float(p),
                    rate_before=left_rate, rate_after=right_rate,
                    delta_pp=100 * (right_rate - left_rate),
                    n_before=int(np.sum(n[:i])), n_after=int(np.sum(n[i:]))))
    binseg_binomial(k[:i], n[:i], min_size, alpha, n_perm, depth + 1, offset, out)
    binseg_binomial(k[i:], n[i:], min_size, alpha, n_perm, depth + 1, offset + i, out)
    return out


def kendall_tau_b(a: np.ndarray, b: np.ndarray) -> tuple[float, float]:
    if a.size < 3:
        return (float("nan"), float("nan"))
    res = stats.kendalltau(a, b, variant="b", nan_policy="omit")
    return (float(res.statistic), float(res.pvalue))


def runs_test(x: np.ndarray) -> dict:
    """Wald-Wolfowitz runs test on the signs of deviations from the median."""
    x = np.asarray(x, dtype=float)
    med = np.median(x)
    s = np.sign(x - med)
    s = s[s != 0]
    if s.size < 8:
        return dict(runs=np.nan, z=np.nan, p=np.nan, note="n<8, not run")
    n1 = int(np.sum(s > 0))
    n2 = int(np.sum(s < 0))
    runs = 1 + int(np.sum(s[1:] != s[:-1]))
    mu = 2 * n1 * n2 / (n1 + n2) + 1
    var = (2 * n1 * n2 * (2 * n1 * n2 - n1 - n2)) / (((n1 + n2) ** 2) * (n1 + n2 - 1))
    if var <= 0:
        return dict(runs=runs, z=np.nan, p=np.nan, note="degenerate variance")
    z = (runs - mu) / math.sqrt(var)
    return dict(runs=runs, z=float(z), p=float(2 * (1 - stats.norm.cdf(abs(z)))), note="")


def design_effect(cl_k: np.ndarray, cl_n: np.ndarray, prefix: str = "") -> dict:
    """Design effect for the overall rate under a given clustering.

    Compares the naive binomial variance of the pooled rate against the
    Taylor-linearised variance of the same ratio estimator with the given units
    as primary sampling units. deff > 1 means every naive interval computed on
    this outcome is too narrow by sqrt(deff); deff < 1 means the clusters are
    *less* variable than independent sampling would be, which happens when the
    same fixed battery is re-run in every cluster.

    Also returns the Pearson overdispersion of the cluster counts against the
    binomial expectation, which reads the same fact without the ratio algebra.
    """
    cl_k = np.asarray(cl_k, dtype=float)
    cl_n = np.asarray(cl_n, dtype=float)
    keep = cl_n > 0
    cl_k, cl_n = cl_k[keep], cl_n[keep]
    m = cl_k.size
    N = float(cl_n.sum())
    K = float(cl_k.sum())
    if m < 2 or N == 0:
        return {f"{prefix}note": "not run"}
    p = K / N
    naive_var = p * (1 - p) / N
    resid = cl_k - p * cl_n
    cluster_var = (m / (m - 1)) * np.sum(resid ** 2) / (N ** 2)
    deff = cluster_var / naive_var if naive_var > 0 else np.nan
    mbar = N / m
    icc = (deff - 1) / (mbar - 1) if mbar > 1 else np.nan
    exp_var = cl_n * p * (1 - p)
    phi = float(np.sum(resid ** 2 / np.where(exp_var > 0, exp_var, np.nan)) / (m - 1))
    out = dict(rate=p, n_obs=int(N), n_clusters=m, mean_cluster_size=mbar,
               naive_se_pp=100 * math.sqrt(naive_var),
               cluster_se_pp=100 * math.sqrt(max(cluster_var, 0)),
               deff=float(deff),
               se_inflation=float(math.sqrt(deff)) if deff == deff and deff > 0 else np.nan,
               icc=float(icc), overdispersion_phi=phi,
               n_eff=float(N / deff) if deff and deff == deff and deff > 0 else np.nan, note="")
    return {f"{prefix}{k}": v for k, v in out.items()} if prefix else out


def mdd_two_proportion(n1: int, n2: int, p_base: float, power: float = 0.80,
                       alpha: float = ALPHA) -> float:
    """Minimum detectable difference, in percentage points, for a two-sample
    proportion comparison with the given cell sizes. Answers 'a rupture of what
    size would this boundary have shown, had one occurred?'."""
    if n1 < 2 or n2 < 2 or not (0 < p_base < 1):
        return float("nan")
    za = stats.norm.ppf(1 - alpha / 2)
    zb = stats.norm.ppf(power)
    # solve for h (Cohen's arcsine effect size), then translate back at p_base
    h = (za + zb) * math.sqrt(1 / n1 + 1 / n2)
    phi1 = 2 * math.asin(math.sqrt(p_base))
    p2 = math.sin((phi1 + h) / 2) ** 2
    return 100 * (p2 - p_base)


def acf_with_gaps(dates: list[date], values: np.ndarray, weights: np.ndarray,
                  max_lag: int = 10, calendar: bool = False) -> list[dict]:
    """Autocorrelation of the daily series.

    calendar=False: lag is measured in collected-day index, which is what a
    series with holes actually offers.
    calendar=True: lag is measured in calendar days, so pairs separated by a gap
    simply do not contribute.
    """
    v = np.asarray(values, dtype=float)
    w = np.asarray(weights, dtype=float)
    mean = float(np.sum(w * v) / np.sum(w)) if np.sum(w) else float(np.mean(v))
    dev = v - mean
    denom = float(np.sum(dev ** 2))
    out = []
    if calendar:
        pos = {d: i for i, d in enumerate(dates)}
        for lag in range(1, max_lag + 1):
            pairs = [(pos[d], pos[d + timedelta(days=lag)])
                     for d in dates if (d + timedelta(days=lag)) in pos]
            if len(pairs) < 5:
                out.append(dict(lag=lag, acf=np.nan, n_pairs=len(pairs)))
                continue
            a = np.array([dev[i] for i, _ in pairs])
            b = np.array([dev[j] for _, j in pairs])
            # product-moment correlation over the matched pairs: pairs separated
            # by a hole in the calendar simply do not exist and contribute nothing
            r = float(np.corrcoef(a, b)[0, 1])
            out.append(dict(lag=lag, acf=r, n_pairs=len(pairs)))
    else:
        n = dev.size
        for lag in range(1, max_lag + 1):
            if n - lag < 5 or denom == 0:
                out.append(dict(lag=lag, acf=np.nan, n_pairs=max(0, n - lag)))
                continue
            r = float(np.sum(dev[:-lag] * dev[lag:]) / denom)
            out.append(dict(lag=lag, acf=r, n_pairs=n - lag))
    return out


# --------------------------------------------------------------------------
# Data loading and the 200-character window
# --------------------------------------------------------------------------

def load_observations(db_path: str, repo_root: str) -> pd.DataFrame:
    """Loads the canonical cut and rebuilds the outcome under a uniform
    200-character observation window, by re-running the project's own
    EntityExtractor over response_text[:200].

    The stored `cited_v2` is kept alongside as `cited_stored` so the window
    correction can be audited arm by arm.
    """
    sys.path.insert(0, repo_root)
    from src.analysis.entity_extraction import EntityExtractor          # noqa: E402
    from src.config import (AMBIGUOUS_ENTITIES, CANONICAL_NAMES,        # noqa: E402
                            ENTITY_ALIASES, ENTITY_STOP_CONTEXTS)
    from src.config_v2 import get_v2_cohort                             # noqa: E402

    extractors = {
        v: EntityExtractor(
            cohort=get_v2_cohort(v, include_anchors=True, include_decoys=True),
            aliases=ENTITY_ALIASES, ambiguous=AMBIGUOUS_ENTITIES,
            canonical_names=CANONICAL_NAMES, stop_contexts=ENTITY_STOP_CONTEXTS,
        ) for v in VERTICALS
    }
    decoys = set()
    for v in VERTICALS:
        decoys |= (set(get_v2_cohort(v, include_anchors=True, include_decoys=True))
                   - set(get_v2_cohort(v, include_anchors=True, include_decoys=False)))

    con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    sql = """
        SELECT id, timestamp, llm, model, vertical, query, query_type, query_lang,
               cited_v2, response_text, response_length
        FROM citations
        WHERE COALESCE(is_probe, 0) = 0
        ORDER BY timestamp
    """
    rows = con.execute(sql).fetchall()
    con.close()

    recs = []
    for r in rows:
        txt = (r["response_text"] or "")
        mentions = extractors[r["vertical"]].extract(txt[:WINDOW_CHARS])
        ents = []
        seen = set()
        for m in mentions:
            if m.entity not in seen:
                seen.add(m.entity)
                ents.append(m.entity)
        ts = datetime.fromisoformat(r["timestamp"])
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        ts_utc = ts.astimezone(timezone.utc)
        ts_brt = ts_utc + timedelta(hours=BRT_OFFSET_HOURS)
        recs.append(dict(
            id=r["id"],
            ts_utc=ts_utc,
            day=ts_brt.date(),
            hour_brt=ts_brt.hour,
            engine=r["llm"],
            model_version=r["model"],
            vertical=r["vertical"],
            query=r["query"],
            query_type=r["query_type"],
            query_lang=r["query_lang"],
            cited_stored=int(r["cited_v2"] or 0),
            cited=1 if ents else 0,
            n_entities=len(ents),
            entities=[e for e in ents if e not in decoys],
            decoy_hit=int(any(e in decoys for e in ents)),
            stored_len=len(txt),
        ))
    df = pd.DataFrame.from_records(recs)
    df["round"] = np.where(df["hour_brt"] < ROUND_SPLIT_HOUR_BRT, "morning", "evening")
    df["weekday"] = pd.to_datetime(df["day"]).dt.dayofweek
    df["is_weekend"] = (df["weekday"] >= 5).astype(int)
    df["iso_week"] = pd.to_datetime(df["day"]).dt.strftime("%G-W%V")
    return df


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default="C:/Sandyboxclaude/papers/data/papers.db")
    ap.add_argument("--repo", default="C:/Sandyboxclaude/papers")
    ap.add_argument("--out", default=str(Path(__file__).resolve().parent))
    ap.add_argument("--perm", type=int, default=N_PERM)
    args = ap.parse_args()

    out_dir = Path(args.out)
    data_dir = out_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    R: dict = {"meta": {}, "notes": []}

    def log(msg: str) -> None:
        print(msg, flush=True)

    log("[1/9] loading observations and applying the 200-character window ...")
    df = load_observations(args.db, args.repo)
    R["meta"] = dict(
        generated_at=datetime.now(timezone.utc).isoformat(),
        db=os.path.abspath(args.db),
        db_mtime=datetime.fromtimestamp(os.path.getmtime(args.db), timezone.utc).isoformat(),
        window_chars=WINDOW_CHARS,
        day_definition=f"local Brazilian date (UTC{BRT_OFFSET_HOURS:+d})",
        round_split_hour_brt=ROUND_SPLIT_HOUR_BRT,
        n_observations=int(len(df)),
        n_days=int(df["day"].nunique()),
        first_day=str(df["day"].min()),
        last_day=str(df["day"].max()),
        engines={e: int((df["engine"] == e).sum()) for e in sorted(df["engine"].unique())},
        seed=20260911,
        n_perm=args.perm,
    )

    # ---- window reconciliation -------------------------------------------
    rec = (df.groupby("engine")
             .agg(n=("cited", "size"),
                  rate_stored=("cited_stored", "mean"),
                  rate_win200=("cited", "mean"),
                  mean_stored_len=("stored_len", "mean"),
                  rows_longer_than_window=("stored_len", lambda s: int((s > WINDOW_CHARS).sum())))
             .reset_index())
    rec["delta_pp"] = 100 * (rec["rate_win200"] - rec["rate_stored"])
    rec["rate_stored"] *= 100
    rec["rate_win200"] *= 100
    rec.to_csv(data_dir / "s2_window_reconciliation.csv", index=False)
    R["window_reconciliation"] = rec.to_dict("records")
    log(rec.to_string(index=False))

    # ---- calendar coverage ------------------------------------------------
    all_days = sorted(df["day"].unique())
    span = (all_days[-1] - all_days[0]).days + 1
    missing = [str(all_days[0] + timedelta(days=i)) for i in range(span)
               if (all_days[0] + timedelta(days=i)) not in set(all_days)]
    # longest run of consecutive missing calendar days
    runs, cur = [], []
    for i in range(span):
        d = all_days[0] + timedelta(days=i)
        if d not in set(all_days):
            cur.append(d)
        elif cur:
            runs.append((cur[0], cur[-1], len(cur)))
            cur = []
    if cur:
        runs.append((cur[0], cur[-1], len(cur)))
    runs.sort(key=lambda t: -t[2])
    R["coverage"] = dict(
        calendar_span_days=span,
        collected_days=len(all_days),
        missing_calendar_days=len(missing),
        coverage_pct=100 * len(all_days) / span,
        largest_gaps=[dict(start=str(a), end=str(b), days=c) for a, b, c in runs[:5]],
    )
    pd.DataFrame([dict(start=str(a), end=str(b), days=c) for a, b, c in runs]).to_csv(
        data_dir / "s2_calendar_gaps.csv", index=False)
    log(f"    collected days={len(all_days)} over a {span}-day calendar span; "
        f"largest gap {runs[0][2]} days ({runs[0][0]} to {runs[0][1]})" if runs else "    no gaps")

    # ---- partial-day flags -------------------------------------------------
    partial_json = Path(args.repo) / "data" / "partial_days.json"
    declared_json = {}
    if partial_json.exists():
        for row in json.loads(partial_json.read_text(encoding="utf-8")):
            declared_json.setdefault(row["date"], []).append(",".join(row.get("missingLLMs", [])))

    day_tab = (df.groupby("day")
                 .agg(n=("cited", "size"), cited=("cited", "sum"),
                      arms=("engine", "nunique"),
                      cells=("engine", lambda s: 0),
                      rounds=("round", "nunique"))
                 .reset_index())
    cells = df.groupby("day").apply(
        lambda g: g.groupby(["engine", "vertical"]).ngroups, include_groups=False)
    day_tab["cells"] = day_tab["day"].map(cells)
    median_n = float(day_tab["n"].median())
    day_tab["partial_empirical"] = ((day_tab["cells"] < 20) | (day_tab["n"] < 0.5 * median_n)).astype(int)
    day_tab["partial_declared"] = day_tab["day"].map(
        lambda d: 1 if (str(d) in DECLARED_PARTIAL_LEDGER or str(d) in declared_json) else 0)
    day_tab["partial_reason"] = day_tab["day"].map(
        lambda d: DECLARED_PARTIAL_LEDGER.get(str(d))
        or ("partial_days.json: missing " + "; ".join(declared_json[str(d)]) if str(d) in declared_json else ""))
    day_tab["partial_any"] = ((day_tab["partial_empirical"] == 1) | (day_tab["partial_declared"] == 1)).astype(int)
    day_tab["rate_pct"] = 100 * day_tab["cited"] / day_tab["n"]
    day_tab.to_csv(data_dir / "s2_daily_pooled.csv", index=False)
    complete_days = set(day_tab.loc[day_tab["partial_any"] == 0, "day"])
    R["partial_days"] = dict(
        median_day_n=median_n,
        n_partial_any=int(day_tab["partial_any"].sum()),
        n_partial_declared=int(day_tab["partial_declared"].sum()),
        n_partial_empirical=int(day_tab["partial_empirical"].sum()),
        declared_but_not_empirical=[str(d) for d in day_tab.loc[
            (day_tab["partial_declared"] == 1) & (day_tab["partial_empirical"] == 0), "day"]],
        empirical_but_not_declared=[str(d) for d in day_tab.loc[
            (day_tab["partial_empirical"] == 1) & (day_tab["partial_declared"] == 0), "day"]],
        n_complete_days=len(complete_days),
    )
    log(f"    partial days: declared={int(day_tab['partial_declared'].sum())}, "
        f"empirical={int(day_tab['partial_empirical'].sum())}, union={int(day_tab['partial_any'].sum())}")

    # ---- daily series per engine ------------------------------------------
    log("[2/9] daily series per engine ...")
    g = (df.groupby(["engine", "day"])
           .agg(n=("cited", "size"), cited=("cited", "sum"),
                model_version=("model_version", lambda s: "|".join(sorted(set(s)))),
                rounds=("round", "nunique"),
                verticals=("vertical", "nunique"))
           .reset_index())
    ci = g.apply(lambda r: wilson_ci(int(r["cited"]), int(r["n"])), axis=1)
    g["rate_pct"] = 100 * g["cited"] / g["n"]
    g["wilson_lo_pct"] = [100 * c[0] for c in ci]
    g["wilson_hi_pct"] = [100 * c[1] for c in ci]
    g["partial_any"] = g["day"].map(lambda d: int(d not in complete_days))
    g["partial_reason"] = g["day"].map(dict(zip(day_tab["day"], day_tab["partial_reason"])))
    g["weekday"] = pd.to_datetime(g["day"]).dt.day_name()
    g["is_weekend"] = (pd.to_datetime(g["day"]).dt.dayofweek >= 5).astype(int)
    g["iso_week"] = pd.to_datetime(g["day"]).dt.strftime("%G-W%V")
    g["day_index"] = (pd.to_datetime(g["day"]) - pd.Timestamp(all_days[0])).dt.days
    gap_before = {}
    for eng, sub in g.groupby("engine"):
        ds = sorted(sub["day"])
        for i, d in enumerate(ds):
            gap_before[(eng, d)] = 0 if i == 0 else (d - ds[i - 1]).days
    g["gap_before_days"] = [gap_before[(e, d)] for e, d in zip(g["engine"], g["day"])]
    g = g.sort_values(["engine", "day"])
    g.to_csv(data_dir / "s2_daily_engine.csv", index=False)

    # per-round daily series (feeds item 5 and the figure)
    gr = (df.groupby(["engine", "day", "round"])
            .agg(n=("cited", "size"), cited=("cited", "sum")).reset_index())
    gr["rate_pct"] = 100 * gr["cited"] / gr["n"]
    gr.to_csv(data_dir / "s2_daily_engine_round.csv", index=False)

    # ---- trend -------------------------------------------------------------
    log("[3/9] trend: Theil-Sen, Mann-Kendall, logistic ...")

    def trend_for(sub_obs: pd.DataFrame, sub_day: pd.DataFrame, label: str, engine: str) -> dict:
        d = sub_day.sort_values("day")
        if len(d) < 8:
            return dict(engine=engine, cut=label, n_days=len(d),
                        first_day=str(d["day"].min()) if len(d) else "",
                        last_day=str(d["day"].max()) if len(d) else "",
                        n_obs=int(len(sub_obs)),
                        rate_pct=float(100 * sub_obs["cited"].mean()) if len(sub_obs) else np.nan,
                        status="NOT RUN (fewer than 8 collected days)")
        x = d["day_index"].to_numpy(dtype=float)
        y = d["rate_pct"].to_numpy(dtype=float)
        ts_slope, ts_int, ts_lo, ts_hi = stats.theilslopes(y, x, alpha=1 - ALPHA)
        mk = mann_kendall(y)
        # logistic with day index, day-clustered SE
        Xo = sm.add_constant(sub_obs["day_index"].to_numpy(dtype=float))
        yo = sub_obs["cited"].to_numpy(dtype=float)
        try:
            mod = sm.GLM(yo, Xo, family=sm.families.Binomial()).fit(
                cov_type="cluster", cov_kwds={"groups": sub_obs["day"].astype(str).to_numpy()})
            beta = float(mod.params[1]); se = float(mod.bse[1]); pv = float(mod.pvalues[1])
            cov = np.asarray(mod.cov_params(), dtype=float)
            draws = RNG.multivariate_normal(np.asarray(mod.params, dtype=float), cov, size=N_BOOT)
            xbar = float(np.average(sub_obs["day_index"], weights=np.ones(len(sub_obs))))
            lo_x, hi_x = xbar - 15, xbar + 15
            eff = 100 * (1 / (1 + np.exp(-(draws[:, 0] + draws[:, 1] * hi_x)))
                         - 1 / (1 + np.exp(-(draws[:, 0] + draws[:, 1] * lo_x))))
            eff_pt = 100 * (1 / (1 + math.exp(-(mod.params[0] + mod.params[1] * hi_x)))
                            - 1 / (1 + math.exp(-(mod.params[0] + mod.params[1] * lo_x))))
            eff_lo, eff_hi = np.percentile(eff, [2.5, 97.5])
            logit_status = "ok"
        except Exception as exc:                                    # pragma: no cover
            beta = se = pv = eff_pt = eff_lo = eff_hi = float("nan")
            logit_status = f"failed: {exc}"
        return dict(
            engine=engine, cut=label, n_days=int(len(d)), n_obs=int(len(sub_obs)),
            first_day=str(d["day"].min()), last_day=str(d["day"].max()),
            rate_pct=float(100 * sub_obs["cited"].mean()),
            theilsen_pp_per_day=float(ts_slope), theilsen_lo=float(ts_lo), theilsen_hi=float(ts_hi),
            theilsen_pp_per_30d=float(30 * ts_slope),
            theilsen_pp_per_30d_lo=float(30 * ts_lo), theilsen_pp_per_30d_hi=float(30 * ts_hi),
            mk_S=mk["S"], mk_tau=mk["tau"], mk_z=mk["z"], mk_p=mk["p"],
            mk_z_hamedrao=mk["z_hr"], mk_p_hamedrao=mk["p_hr"], mk_hr_factor=mk.get("hr_factor"),
            logit_beta_per_day=beta, logit_se=se, logit_p=pv,
            logit_pp_per_30d=eff_pt, logit_pp_per_30d_lo=float(eff_lo), logit_pp_per_30d_hi=float(eff_hi),
            logit_status=logit_status, status="run")

    # segments per engine: instrument-homogeneous stretches
    SEGMENTS = {
        "Gemini": [("pre 2026-06-17 (gemini-2.5-pro)", date(2026, 4, 23), date(2026, 6, 16)),
                   ("post 2026-06-17 (gemini-2.5-flash)", date(2026, 6, 17), date(2026, 9, 30))],
        "Grok":   [("post 2026-08-31 (reasoning_effort=low)", date(2026, 8, 31), date(2026, 9, 30))],
    }

    trend_rows = []
    for eng in ENGINES:
        obs = df[df["engine"] == eng].copy()
        if obs.empty:
            continue
        obs["day_index"] = (pd.to_datetime(obs["day"]) - pd.Timestamp(all_days[0])).dt.days
        dd = g[g["engine"] == eng]
        trend_rows.append(trend_for(obs, dd, "full span (all days)", eng))
        obs_c = obs[obs["day"].isin(complete_days)]
        dd_c = dd[dd["day"].isin(complete_days)]
        trend_rows.append(trend_for(obs_c, dd_c, "full span (complete days only)", eng))
        for lab, a, b in SEGMENTS.get(eng, []):
            o = obs[(obs["day"] >= a) & (obs["day"] <= b)]
            d2 = dd[(dd["day"] >= a) & (dd["day"] <= b)]
            trend_rows.append(trend_for(o, d2, lab, eng))
    trend = pd.DataFrame(trend_rows)
    fam = trend["status"] == "run"
    for col, qcol in (("mk_p", "mk_q_bh"), ("mk_p_hamedrao", "mk_hr_q_bh"), ("logit_p", "logit_q_bh")):
        trend[qcol] = np.nan
        mask = fam & trend[col].notna()
        if mask.sum() > 0:
            trend.loc[mask, qcol] = multipletests(trend.loc[mask, col], method="fdr_bh")[1]
    trend.to_csv(data_dir / "s2_trend.csv", index=False)
    R["trend"] = trend.to_dict("records")
    log(trend.loc[fam, ["engine", "cut", "n_days", "rate_pct", "theilsen_pp_per_30d",
                        "mk_p", "mk_p_hamedrao", "logit_pp_per_30d", "logit_p"]].to_string(index=False))

    # ---- change points -----------------------------------------------------
    log("[4/9] change points (blind to the event table) ...")
    cp_rows = []
    for eng in ENGINES:
        dd = g[g["engine"] == eng].sort_values("day").reset_index(drop=True)
        if len(dd) < 2 * MIN_SEG_DAYS:
            cp_rows.append(dict(engine=eng, method="binomial-binseg", status=f"NOT RUN ({len(dd)} days)"))
            continue
        k = dd["cited"].to_numpy(dtype=float)
        n = dd["n"].to_numpy(dtype=float)
        found = binseg_binomial(k, n, MIN_SEG_DAYS, ALPHA, args.perm)
        for f in sorted(found, key=lambda z: z["index"]):
            i = f["index"]
            d_prev, d_next = dd.loc[i - 1, "day"], dd.loc[i, "day"]
            span = (d_next - d_prev).days
            cp_rows.append(dict(engine=eng, method="binomial-binseg", status="run",
                                index=i, last_day_before=str(d_prev), first_day_after=str(d_next),
                                gap_across_days=span,
                                located=("day boundary" if span <= 3 else
                                         f"anywhere inside a {span}-day hole"),
                                rate_before_pct=100 * f["rate_before"],
                                rate_after_pct=100 * f["rate_after"],
                                delta_pp=f["delta_pp"], lr=f["lr"], p_perm=f["p_perm"],
                                n_before=f["n_before"], n_after=f["n_after"]))
        if not found:
            cp_rows.append(dict(engine=eng, method="binomial-binseg", status="run; no change point at alpha=0.05"))

    # corroboration with ruptures
    ruptures_status = "NOT RUN (ruptures unavailable)"
    try:
        import ruptures as rpt
        ruptures_status = f"run (ruptures {getattr(rpt, '__version__', '?')})"
        for eng in ENGINES:
            dd = g[g["engine"] == eng].sort_values("day").reset_index(drop=True)
            if len(dd) < 2 * MIN_SEG_DAYS:
                continue
            p = np.clip(dd["cited"].to_numpy(float) / dd["n"].to_numpy(float), 1e-4, 1 - 1e-4)
            sig = np.log(p / (1 - p)).reshape(-1, 1)
            sd = float(np.std(np.diff(sig[:, 0]))) / math.sqrt(2) or 1.0
            pen = 3 * (sd ** 2) * math.log(len(sig))
            bkps = rpt.Pelt(model="l2", min_size=MIN_SEG_DAYS).fit(sig).predict(pen=pen)
            for b in bkps[:-1]:
                d_prev, d_next = dd.loc[b - 1, "day"], dd.loc[b, "day"]
                cp_rows.append(dict(engine=eng, method="ruptures-pelt-l2-logit", status="run",
                                    index=int(b), last_day_before=str(d_prev), first_day_after=str(d_next),
                                    gap_across_days=(d_next - d_prev).days,
                                    rate_before_pct=100 * float(dd.loc[:b - 1, "cited"].sum() / dd.loc[:b - 1, "n"].sum()),
                                    rate_after_pct=100 * float(dd.loc[b:, "cited"].sum() / dd.loc[b:, "n"].sum()),
                                    delta_pp=np.nan, lr=np.nan, p_perm=np.nan,
                                    n_before=int(dd.loc[:b - 1, "n"].sum()), n_after=int(dd.loc[b:, "n"].sum())))
    except ImportError:
        pass
    R["ruptures_status"] = ruptures_status
    cp = pd.DataFrame(cp_rows)
    cp.to_csv(data_dir / "s2_changepoints.csv", index=False)
    log(f"    {ruptures_status}")
    if "first_day_after" in cp.columns:
        log(cp[cp["status"] == "run"][["engine", "method", "last_day_before", "first_day_after",
                                       "gap_across_days", "delta_pp", "p_perm"]].to_string(index=False))

    # ---- confrontation with the declared event table ----------------------
    log("[5/9] confronting detections with the declared event table ...")
    conf_rows = []
    detected = cp[(cp.get("status") == "run") & cp.get("first_day_after").notna()] if "first_day_after" in cp.columns else pd.DataFrame()
    primary = detected[detected["method"] == "binomial-binseg"] if not detected.empty else pd.DataFrame()

    def _match(ev_date: date, arm: str, table: pd.DataFrame, tol: int = 3):
        hits = []
        if table.empty:
            return hits
        sub = table[table["engine"] == arm]
        for _, row in sub.iterrows():
            a = date.fromisoformat(row["last_day_before"])
            b = date.fromisoformat(row["first_day_after"])
            # distance from the event date to the detected boundary interval [a, b]
            if a <= ev_date <= b:
                dist = 0
            else:
                dist = min(abs((ev_date - a).days), abs((ev_date - b).days))
            if dist <= tol:
                hits.append((dist, row))
        return sorted(hits, key=lambda t: t[0])

    matched_ids = set()
    for ev in DECLARED_EVENTS:
        ev_date = date.fromisoformat(ev["date"])
        for arm in ev["arms"]:
            dd = g[g["engine"] == arm]
            base = dict(event_date=ev["date"], arm=arm, change=ev["change"],
                        klass=ev["klass"], status_doc=ev["status"])
            if dd.empty:
                conf_rows.append(dict(**base, detected="n/a",
                                      verdict="arm absent from the analysed cut"))
                continue
            days = sorted(dd["day"])
            # An event dated D takes effect during D, so the boundary the data can
            # see sits between the last day strictly before D and the first day on
            # or after D.
            before = [d for d in days if d < ev_date]
            after = [d for d in days if d >= ev_date]
            if not before or not after:
                conf_rows.append(dict(
                    **base, detected="not testable",
                    verdict=(f"event lies outside the arm's observed span "
                             f"({days[0]} to {days[-1]}): not testable"),
                    days_of_data_within_3=0))
                continue
            local_gap = (after[0] - before[-1]).days
            n_close = sum(1 for d in days if abs((d - ev_date).days) <= 3)
            # what size of rupture could this boundary have revealed?
            win_pre = dd[(dd["day"] > before[-1] - timedelta(days=14)) & (dd["day"] <= before[-1])]
            win_post = dd[(dd["day"] >= after[0]) & (dd["day"] < after[0] + timedelta(days=14))]
            n1, n2 = int(win_pre["n"].sum()), int(win_post["n"].sum())
            p_base = float(win_pre["cited"].sum() / n1) if n1 else float("nan")
            mdd = mdd_two_proportion(n1, n2, p_base) if n1 and n2 else float("nan")
            hits = _match(ev_date, arm, primary)
            if hits:
                dist, row = hits[0]
                matched_ids.add((row["engine"], row["first_day_after"], row["method"]))
                verdict = (f"COINCIDES: detected boundary {row['last_day_before']} -> "
                           f"{row['first_day_after']}, distance {dist} d, "
                           f"delta {row['delta_pp']:+.1f} pp, p_perm={row['p_perm']:.3f}")
                det = "coincides"
            elif local_gap > 3:
                verdict = (f"NOT TESTABLE: the arm's nearest observations straddle a "
                           f"{local_gap}-day hole ({before[-1]} -> {after[0]}); no detector "
                           f"can separate the event from the hole")
                det = "not testable"
            else:
                verdict = ("declared event with NO detectable rupture at alpha=0.05 "
                           f"(binomial binary segmentation); {n_close} observed days within "
                           f"+/-3 d; a shift of {mdd:+.1f} pp would have been detected with "
                           f"80% power on the 14 days either side (n={n1} vs {n2})")
                det = "no rupture"
            conf_rows.append(dict(**base, detected=det, verdict=verdict,
                                  local_gap_days=local_gap, days_of_data_within_3=n_close,
                                  n_pre_14d=n1, n_post_14d=n2,
                                  rate_pre_14d_pct=100 * p_base if n1 else np.nan,
                                  mdd_80pct_pp=mdd))

    # detections that match no declared event
    for _, row in primary.iterrows():
        key = (row["engine"], row["first_day_after"], row["method"])
        if key in matched_ids:
            continue
        a = date.fromisoformat(row["last_day_before"])
        b = date.fromisoformat(row["first_day_after"])
        nearest, nd = None, 10 ** 6
        for ev in DECLARED_EVENTS:
            if row["engine"] not in ev["arms"]:
                continue
            e = date.fromisoformat(ev["date"])
            dist = 0 if a <= e <= b else min(abs((e - a).days), abs((e - b).days))
            if dist < nd:
                nearest, nd = ev, dist
        span = int(row["gap_across_days"])
        det = ("rupture across a data hole (not attributable)" if span > 3
               else "rupture without declared event")
        conf_rows.append(dict(
            event_date="(none)", arm=row["engine"],
            change=f"UNDECLARED RUPTURE {row['last_day_before']} -> {row['first_day_after']}",
            klass="detected, not declared", status_doc="",
            detected=det,
            verdict=(f"delta {row['delta_pp']:+.1f} pp (p_perm={row['p_perm']:.3f}); "
                     f"boundary localised to a {span}-day interval; "
                     f"nearest declared event for this arm: "
                     f"{nearest['date'] if nearest else 'none'} at {nd if nearest else 'n/a'} d"),
            local_gap_days=span))
    confront = pd.DataFrame(conf_rows)
    confront.to_csv(data_dir / "s2_event_confrontation.csv", index=False)
    R["confrontation"] = confront.to_dict("records")
    log(confront[["event_date", "arm", "detected"]].to_string(index=False))

    # ---- autocorrelation and dependence ------------------------------------
    log("[6/9] autocorrelation and dependence ...")
    acf_rows, dep_rows = [], []
    for eng in ENGINES:
        dd = g[g["engine"] == eng].sort_values("day").reset_index(drop=True)
        if len(dd) < 8:
            dep_rows.append(dict(engine=eng, status=f"NOT RUN ({len(dd)} days)"))
            continue
        days = list(dd["day"])
        vals = dd["rate_pct"].to_numpy(float)
        wts = dd["n"].to_numpy(float)
        # segment-demeaned version: removes the level shift each detected rupture
        # introduces, so the autocorrelation is not just the rupture showing up again
        seg_id = np.zeros(len(dd), dtype=int)
        bnds = sorted(int(r["index"]) for _, r in primary[primary["engine"] == eng].iterrows()) \
            if not primary.empty else []
        for b in bnds:
            seg_id[b:] += 1
        demeaned = vals.copy()
        for s in np.unique(seg_id):
            m = seg_id == s
            demeaned[m] = vals[m] - vals[m].mean()
        for kind, series in (("raw", vals), ("segment-demeaned", demeaned)):
            for row in acf_with_gaps(days, series, wts, 10, calendar=False):
                acf_rows.append(dict(engine=eng, series=kind, lag_unit="collected-day index",
                                     **row, bartlett_ci=1.96 / math.sqrt(len(dd))))
            for row in acf_with_gaps(days, series, wts, 10, calendar=True):
                acf_rows.append(dict(engine=eng, series=kind, lag_unit="calendar day",
                                     **row, bartlett_ci=np.nan))
        lb = sm.stats.acorr_ljungbox(demeaned, lags=[1, 3, 5], return_df=True)
        # consecutive-calendar-day pairs only
        pos = {d: i for i, d in enumerate(days)}
        pairs = [(pos[d], pos[d + timedelta(days=1)]) for d in days if (d + timedelta(days=1)) in pos]
        if len(pairs) >= 5:
            a = np.array([demeaned[i] for i, _ in pairs]); b = np.array([demeaned[j] for _, j in pairs])
            sp = stats.spearmanr(a, b)
            pear = stats.pearsonr(a, b)
            adj = dict(n_adjacent_pairs=len(pairs), spearman_rho=float(sp.statistic),
                       spearman_p=float(sp.pvalue), pearson_r=float(pear.statistic),
                       pearson_p=float(pear.pvalue))
        else:
            adj = dict(n_adjacent_pairs=len(pairs), spearman_rho=np.nan, spearman_p=np.nan,
                       pearson_r=np.nan, pearson_p=np.nan)
        de = design_effect(dd["cited"].to_numpy(float), dd["n"].to_numpy(float), prefix="day_")
        # The battery is fixed: the same 192 prompts are re-asked every round, so
        # the query is the other candidate primary sampling unit and the two
        # clusterings answer different questions.
        qq = (df[df["engine"] == eng].groupby("query")
                .agg(n=("cited", "size"), cited=("cited", "sum")))
        dq = design_effect(qq["cited"].to_numpy(float), qq["n"].to_numpy(float), prefix="query_")
        rt = runs_test(demeaned)
        dep_rows.append(dict(engine=eng, status="run",
                             lb_stat_lag1=float(lb.loc[1, "lb_stat"]), lb_p_lag1=float(lb.loc[1, "lb_pvalue"]),
                             lb_stat_lag5=float(lb.loc[5, "lb_stat"]), lb_p_lag5=float(lb.loc[5, "lb_pvalue"]),
                             runs=rt["runs"], runs_z=rt["z"], runs_p=rt["p"], **adj, **de, **dq))
    pd.DataFrame(acf_rows).to_csv(data_dir / "s2_acf.csv", index=False)
    dep = pd.DataFrame(dep_rows)
    pooled_de = design_effect(day_tab["cited"].to_numpy(float), day_tab["n"].to_numpy(float), prefix="day_")
    qall = df.groupby(["engine", "query"]).agg(n=("cited", "size"), cited=("cited", "sum"))
    pooled_dq = design_effect(qall["cited"].to_numpy(float), qall["n"].to_numpy(float), prefix="query_")
    dep = pd.concat([dep, pd.DataFrame([dict(engine="ALL (pooled)", status="run",
                                             **pooled_de, **pooled_dq)])], ignore_index=True)
    dep.to_csv(data_dir / "s2_dependence.csv", index=False)
    R["dependence"] = dep.to_dict("records")
    R["pooled_design_effect"] = dict(**pooled_de, **pooled_dq)
    log(dep[["engine", "day_deff", "day_se_inflation", "day_overdispersion_phi",
             "query_deff", "query_se_inflation", "day_naive_se_pp", "day_cluster_se_pp",
             "query_cluster_se_pp", "spearman_rho", "spearman_p"]].to_string(index=False))

    # ---- round and weekday -------------------------------------------------
    log("[7/9] round and weekday effects ...")
    rw_rows = []
    both = gr.groupby(["engine", "day"])["round"].nunique()
    both_days = {(e, d) for (e, d), v in both.items() if v == 2}
    for eng in ENGINES + ["ALL (pooled)"]:
        sub = df if eng == "ALL (pooled)" else df[df["engine"] == eng]
        if sub.empty:
            continue
        # --- round: paired within-day, so day effects cannot drive it
        sr = gr if eng == "ALL (pooled)" else gr[gr["engine"] == eng]
        if eng == "ALL (pooled)":
            sr = (df.groupby(["day", "round"]).agg(n=("cited", "size"), cited=("cited", "sum")).reset_index())
            sr["engine"] = "ALL (pooled)"
            pairs_days = [d for d, v in sr.groupby("day")["round"].nunique().items() if v == 2]
        else:
            pairs_days = [d for (e, d) in both_days if e == eng]
        piv = sr[sr["day"].isin(pairs_days)].pivot_table(
            index="day", columns="round", values=["n", "cited"], aggfunc="sum")
        if len(piv) >= 5 and ("morning" in piv["n"].columns) and ("evening" in piv["n"].columns):
            mrate = 100 * piv["cited"]["morning"] / piv["n"]["morning"]
            erate = 100 * piv["cited"]["evening"] / piv["n"]["evening"]
            diff = (mrate - erate).to_numpy(float)
            w = stats.wilcoxon(diff, zero_method="wilcox", alternative="two-sided")
            boot = np.array([np.mean(RNG.choice(diff, diff.size, replace=True)) for _ in range(N_BOOT)])
            rw_rows.append(dict(engine=eng, term="round: morning minus evening (paired by day)",
                                n_units=int(len(diff)),
                                estimate_pp=float(np.mean(diff)),
                                ci_lo=float(np.percentile(boot, 2.5)), ci_hi=float(np.percentile(boot, 97.5)),
                                test="Wilcoxon signed-rank", stat=float(w.statistic), p=float(w.pvalue),
                                status="run"))
        else:
            rw_rows.append(dict(engine=eng, term="round: morning minus evening (paired by day)",
                                status=f"NOT RUN (only {len(piv)} days with both rounds)"))
        # --- weekday vs weekend: day-level, unpaired
        dl = (sub.groupby(["day", "is_weekend"]).agg(n=("cited", "size"), cited=("cited", "sum"))
                 .reset_index())
        dl["rate"] = 100 * dl["cited"] / dl["n"]
        we = dl.loc[dl["is_weekend"] == 1, "rate"].to_numpy(float)
        wd = dl.loc[dl["is_weekend"] == 0, "rate"].to_numpy(float)
        if we.size >= 4 and wd.size >= 4:
            mw = stats.mannwhitneyu(we, wd, alternative="two-sided")
            boot = np.array([np.mean(RNG.choice(we, we.size, replace=True))
                             - np.mean(RNG.choice(wd, wd.size, replace=True)) for _ in range(N_BOOT)])
            rw_rows.append(dict(engine=eng, term="weekend minus weekday (day-level)",
                                n_units=int(we.size + wd.size),
                                estimate_pp=float(we.mean() - wd.mean()),
                                ci_lo=float(np.percentile(boot, 2.5)), ci_hi=float(np.percentile(boot, 97.5)),
                                test="Mann-Whitney U", stat=float(mw.statistic), p=float(mw.pvalue),
                                n_weekend_days=int(we.size), n_weekday_days=int(wd.size), status="run"))
        else:
            rw_rows.append(dict(engine=eng, term="weekend minus weekday (day-level)",
                                status=f"NOT RUN (weekend days={we.size}, weekday days={wd.size})"))
    rw = pd.DataFrame(rw_rows)
    mask = (rw["status"] == "run") & rw["p"].notna() if "p" in rw.columns else pd.Series(False, index=rw.index)
    rw["q_bh"] = np.nan
    if mask.sum() > 0:
        rw.loc[mask, "q_bh"] = multipletests(rw.loc[mask, "p"], method="fdr_bh")[1]
    # composition check: is the query mix identical across rounds?
    comp = (df.groupby(["round"])
              .agg(n=("cited", "size"),
                   pct_pt=("query_lang", lambda s: 100 * float((s == "pt").mean())),
                   pct_directive=("query_type", lambda s: 100 * float((s == "directive").mean())),
                   n_queries=("query", "nunique"), n_engines=("engine", "nunique"))
              .reset_index())
    comp.to_csv(data_dir / "s2_round_composition.csv", index=False)
    rw.to_csv(data_dir / "s2_round_weekday.csv", index=False)
    R["round_weekday"] = rw.to_dict("records")
    R["round_composition"] = comp.to_dict("records")
    log(rw.to_string(index=False))

    # ---- ranking stability -------------------------------------------------
    log("[8/9] weekly ranking stability ...")
    # entity coverage per week: share of the week's responses in the entity's
    # vertical in which the entity appears inside the 200-character window
    exploded = df[["iso_week", "vertical", "entities"]].explode("entities").dropna(subset=["entities"])
    hits = exploded.groupby(["iso_week", "vertical", "entities"]).size().rename("hits").reset_index()
    denom = df.groupby(["iso_week", "vertical"]).size().rename("responses").reset_index()
    ent = hits.merge(denom, on=["iso_week", "vertical"])
    ent = ent.rename(columns={"entities": "entity"})
    # Absence is information, not missingness: an entity observed anywhere in the
    # series but absent from a given week has coverage 0 that week, not a missing
    # value. Restricting the rank correlation to entities cited in both weeks
    # would silently drop exactly the entities that moved.
    sys.path.insert(0, args.repo)
    from src.config_v2 import get_v2_cohort as _cohort                  # noqa: E402
    ent_vert = {}
    for v in VERTICALS:
        for e in _cohort(v, include_anchors=True, include_decoys=False):
            ent_vert.setdefault(e, v)
    weeks = sorted(df["iso_week"].unique())
    full = pd.MultiIndex.from_product([weeks, sorted(ent_vert)], names=["iso_week", "entity"]).to_frame(index=False)
    full["vertical"] = full["entity"].map(ent_vert)
    ent = full.merge(ent[["iso_week", "entity", "hits"]], on=["iso_week", "entity"], how="left")
    ent["hits"] = ent["hits"].fillna(0.0)
    ent = ent.merge(denom, on=["iso_week", "vertical"], how="left")
    ent = ent[ent["responses"].notna() & (ent["responses"] > 0)]
    ent["coverage_pct"] = 100 * ent["hits"] / ent["responses"]
    wk_days = df.groupby("iso_week")["day"].nunique().rename("week_days")
    ent = ent.merge(wk_days, on="iso_week", how="left")
    ent["rank"] = ent.groupby("iso_week")["coverage_pct"].rank(ascending=False, method="min")
    ent = ent.sort_values(["iso_week", "rank"])
    ent.to_csv(data_dir / "s2_weekly_entity_rank.csv", index=False)

    wk_days_map = dict(df.groupby("iso_week")["day"].nunique())

    def tau_series(pivot: pd.DataFrame, label: str, min_common: int = 3) -> list[dict]:
        wks = list(pivot.index)
        rows = []
        for i in range(len(wks) - 1):
            a, b = pivot.loc[wks[i]], pivot.loc[wks[i + 1]]
            common = a.notna() & b.notna()
            base = dict(level=label, week_a=wks[i], week_b=wks[i + 1],
                        days_a=wk_days_map.get(wks[i]), days_b=wk_days_map.get(wks[i + 1]),
                        consecutive_calendar=int(wks[i + 1] == _next_week(wks[i])))
            if common.sum() < min_common:
                rows.append(dict(**base, n_common=int(common.sum()), tau_b=np.nan, p=np.nan,
                                 status="NOT RUN (<%d common items)" % min_common))
                continue
            t, p = kendall_tau_b(a[common].to_numpy(float), b[common].to_numpy(float))
            ta = a[common].rank(ascending=False, method="min")
            tb = b[common].rank(ascending=False, method="min")
            top = min(10, int(common.sum()))
            ov = len(set(ta.nsmallest(top).index) & set(tb.nsmallest(top).index)) / top
            # Rank movement is read only among items with some coverage in at
            # least one of the two weeks. Items tied at zero in both weeks carry
            # no ordering information and their nominal rank moves whenever the
            # number of non-zero items changes.
            active = common & ((a.fillna(0) > 0) | (b.fillna(0) > 0))
            if active.sum() >= 3:
                ra = a[active].rank(ascending=False, method="min")
                rb = b[active].rank(ascending=False, method="min")
                moved3 = int(np.sum(np.abs(ra - rb) >= 3))
                moved5 = int(np.sum(np.abs(ra - rb) >= 5))
                med_shift = float(np.median(np.abs(ra - rb)))
                t_act, p_act = kendall_tau_b(a[active].to_numpy(float), b[active].to_numpy(float))
            else:
                moved3 = moved5 = 0
                med_shift = t_act = p_act = np.nan
            rows.append(dict(**base, n_common=int(common.sum()), tau_b=t, p=p,
                             n_active=int(active.sum()), tau_b_active=t_act, p_active=p_act,
                             top_overlap_k=top, top_overlap=ov,
                             median_abs_rank_shift=med_shift,
                             n_moved_3plus_ranks=moved3, n_moved_5plus_ranks=moved5,
                             status="run"))
        return rows

    def _next_week(w: str) -> str:
        y, n = int(w[:4]), int(w[-2:])
        d = date.fromisocalendar(y, n, 1) + timedelta(days=7)
        return d.strftime("%G-W%V")

    ent_piv = ent.pivot_table(index="iso_week", columns="entity", values="coverage_pct")
    ent_piv = ent_piv.sort_index()
    tau_rows = tau_series(ent_piv, "entity coverage", min_common=5)
    eng_week = (df.groupby(["iso_week", "engine"]).agg(n=("cited", "size"), cited=("cited", "sum"))
                  .reset_index())
    eng_week["rate_pct"] = 100 * eng_week["cited"] / eng_week["n"]
    eng_week["rank"] = eng_week.groupby("iso_week")["rate_pct"].rank(ascending=False, method="min")
    eng_week.to_csv(data_dir / "s2_weekly_engine_rank.csv", index=False)
    eng_piv = eng_week.pivot_table(index="iso_week", columns="engine", values="rate_pct").sort_index()
    tau_rows += tau_series(eng_piv, "engine rate", min_common=3)
    tau = pd.DataFrame(tau_rows)
    tau.to_csv(data_dir / "s2_rank_tau.csv", index=False)
    cohort_real = set(ent_vert)
    ever_cited = set(ent.loc[ent["hits"] > 0, "entity"])
    R["entity_universe"] = dict(
        cohort_real_entities=len(cohort_real),
        ever_cited_in_window=len(ever_cited),
        never_cited_in_window=len(cohort_real - ever_cited),
        decoy_hits_in_canonical_rows=int(df["decoy_hit"].sum()),
        note="entities never cited inside the 200-character window in any week; "
             "they enter every weekly ranking at coverage 0 and are never dropped",
    )
    R["rank_stability"] = dict(
        entity=dict(
            n_pairs=int(((tau["level"] == "entity coverage") & (tau["status"] == "run")).sum()),
            mean_tau=float(tau.loc[(tau["level"] == "entity coverage") & (tau["status"] == "run"), "tau_b"].mean()),
            mean_tau_consecutive=float(tau.loc[(tau["level"] == "entity coverage") & (tau["status"] == "run")
                                               & (tau["consecutive_calendar"] == 1), "tau_b"].mean()),
            mean_top10_overlap=float(tau.loc[(tau["level"] == "entity coverage") & (tau["status"] == "run"),
                                             "top_overlap"].mean()),
            min_tau=float(tau.loc[(tau["level"] == "entity coverage") & (tau["status"] == "run"), "tau_b"].min()),
            max_tau=float(tau.loc[(tau["level"] == "entity coverage") & (tau["status"] == "run"), "tau_b"].max()),
            mean_tau_active=float(tau.loc[(tau["level"] == "entity coverage") & (tau["status"] == "run"),
                                          "tau_b_active"].mean()),
            mean_median_abs_rank_shift=float(tau.loc[(tau["level"] == "entity coverage")
                                                     & (tau["status"] == "run"), "median_abs_rank_shift"].mean()),
            mean_share_moved_3plus=float((tau.loc[(tau["level"] == "entity coverage") & (tau["status"] == "run"),
                                                  "n_moved_3plus_ranks"]
                                          / tau.loc[(tau["level"] == "entity coverage") & (tau["status"] == "run"),
                                                    "n_active"]).mean()),
            mean_share_moved_5plus=float((tau.loc[(tau["level"] == "entity coverage") & (tau["status"] == "run"),
                                                  "n_moved_5plus_ranks"]
                                          / tau.loc[(tau["level"] == "entity coverage") & (tau["status"] == "run"),
                                                    "n_active"]).mean()),
        ),
        engine=dict(
            n_pairs=int(((tau["level"] == "engine rate") & (tau["status"] == "run")).sum()),
            mean_tau=float(tau.loc[(tau["level"] == "engine rate") & (tau["status"] == "run"), "tau_b"].mean()),
            mean_tau_consecutive=float(tau.loc[(tau["level"] == "engine rate") & (tau["status"] == "run")
                                               & (tau["consecutive_calendar"] == 1), "tau_b"].mean()),
        ),
    )
    log(tau.to_string(index=False))

    # ---- intervention analysis --------------------------------------------
    log("[9/9] intervention analysis (difference in differences) ...")
    did_rows = []

    def did(treated: str, controls: list[str], pre: tuple[date, date], post: tuple[date, date],
            label: str, with_controls: bool = True) -> dict:
        arms = [treated] + controls
        s = df[df["engine"].isin(arms)].copy()
        s = s[((s["day"] >= pre[0]) & (s["day"] <= pre[1])) | ((s["day"] >= post[0]) & (s["day"] <= post[1]))]
        if s.empty:
            return dict(label=label, status="NOT RUN (no rows)")
        s["treat"] = (s["engine"] == treated).astype(int)
        s["post"] = (s["day"] >= post[0]).astype(int)
        s["did"] = s["treat"] * s["post"]
        cells = s.groupby(["treat", "post"]).agg(n=("cited", "size"), cited=("cited", "sum"))
        if len(cells) < 4:
            return dict(label=label, status="NOT RUN (a 2x2 cell is empty)")
        design = ["treat", "post", "did"]
        X = s[design].copy()
        if with_controls:
            for c in ("vertical", "query_type", "query_lang"):
                d = pd.get_dummies(s[c], prefix=c, drop_first=True, dtype=float)
                X = pd.concat([X, d], axis=1)
        X = sm.add_constant(X.astype(float))
        y = s["cited"].to_numpy(float)
        # Clustering on the collection day: a day is the unit at which an outage,
        # a provider hiccup or a battery irregularity hits every arm at once.
        groups = s["day"].astype(str).to_numpy()
        lpm = sm.OLS(y, X).fit(cov_type="cluster", cov_kwds={"groups": groups})
        logit = sm.GLM(y, X, family=sm.families.Binomial()).fit(
            cov_type="cluster", cov_kwds={"groups": groups})
        # average marginal effect of the interaction, from the logit
        X1 = X.copy(); X1["did"] = 1.0; X1["treat"] = 1.0; X1["post"] = 1.0
        X0 = X.copy(); X0["did"] = 0.0; X0["treat"] = 1.0; X0["post"] = 1.0
        ame = float(np.mean(logit.predict(X1) - logit.predict(X0))) * 100
        raw = {f"t{t}_p{p}": 100 * float(row["cited"] / row["n"]) for (t, p), row in cells.iterrows()}
        # Day-level cluster bootstrap on the raw 2x2 contrast. With about fifty
        # clusters the asymptotic cluster-robust interval is known to be too
        # narrow; this one makes no asymptotic claim.
        day_cells = (s.groupby(["day", "treat", "post"])
                       .agg(n=("cited", "size"), cited=("cited", "sum")).reset_index())
        udays = day_cells["day"].unique()
        boots = []
        for _ in range(600):
            pick = RNG.choice(udays, udays.size, replace=True)
            bs = pd.concat([day_cells[day_cells["day"] == d] for d in pick], ignore_index=True)
            agg = bs.groupby(["treat", "post"]).agg(n=("n", "sum"), cited=("cited", "sum"))
            if len(agg) < 4:
                continue
            r = {f"t{t}_p{p}": 100 * row["cited"] / row["n"] for (t, p), row in agg.iterrows()}
            boots.append((r["t1_p1"] - r["t1_p0"]) - (r["t0_p1"] - r["t0_p0"]))
        boot_lo, boot_hi = (np.percentile(boots, [2.5, 97.5]) if len(boots) > 50 else (np.nan, np.nan))
        return dict(label=label, status="run", treated=treated, controls=",".join(controls),
                    boot_ci_lo_pp=float(boot_lo), boot_ci_hi_pp=float(boot_hi),
                    n_boot=len(boots),
                    pre=f"{pre[0]}..{pre[1]}", post=f"{post[0]}..{post[1]}",
                    n_obs=int(len(s)), n_days=int(s["day"].nunique()),
                    treated_pre_pct=raw.get("t1_p0"), treated_post_pct=raw.get("t1_p1"),
                    control_pre_pct=raw.get("t0_p0"), control_post_pct=raw.get("t0_p1"),
                    raw_did_pp=(raw.get("t1_p1", np.nan) - raw.get("t1_p0", np.nan))
                               - (raw.get("t0_p1", np.nan) - raw.get("t0_p0", np.nan)),
                    lpm_did_pp=100 * float(lpm.params["did"]),
                    lpm_se_pp=100 * float(lpm.bse["did"]),
                    lpm_ci_lo_pp=100 * float(lpm.conf_int().loc["did", 0]),
                    lpm_ci_hi_pp=100 * float(lpm.conf_int().loc["did", 1]),
                    lpm_p=float(lpm.pvalues["did"]),
                    logit_did_logodds=float(logit.params["did"]), logit_p=float(logit.pvalues["did"]),
                    logit_ame_pp=ame, controls_in_model=with_controls,
                    n_clusters=int(len(set(groups))))

    gem_pre = (date(2026, 4, 23), date(2026, 6, 16))
    gem_post = (date(2026, 6, 17), date(2026, 9, 8))
    did_rows.append(did("Gemini", ["ChatGPT", "Claude"], gem_pre, gem_post,
                        "2026-06-17 Gemini model+reasoning change (controls: ChatGPT, Claude)"))
    did_rows.append(did("Gemini", ["ChatGPT", "Claude", "Perplexity"], gem_pre, gem_post,
                        "2026-06-17 Gemini (controls: three continuous arms, Perplexity included)"))
    did_rows.append(did("Gemini", ["ChatGPT", "Claude", "Perplexity", "Groq"], gem_pre, gem_post,
                        "2026-06-17 Gemini (controls include Groq, which exits 2026-08-16)"))
    did_rows.append(did("Gemini", ["ChatGPT", "Claude", "Perplexity"],
                        (date(2026, 4, 23), date(2026, 6, 16)), (date(2026, 8, 8), date(2026, 8, 18)),
                        "2026-06-17 Gemini, post truncated at 2026-08-18 (before the arm swap)"))
    # pre-trend placebo: split the pre-window in half, no real event
    did_rows.append(did("Gemini", ["ChatGPT", "Claude"],
                        (date(2026, 4, 23), date(2026, 5, 16)), (date(2026, 5, 17), date(2026, 6, 9)),
                        "PLACEBO pre-trend: false boundary at 2026-05-17 (controls: ChatGPT, Claude)"))
    did_rows.append(did("Gemini", ["ChatGPT", "Claude", "Perplexity"],
                        (date(2026, 4, 23), date(2026, 5, 16)), (date(2026, 5, 17), date(2026, 6, 9)),
                        "PLACEBO pre-trend: false boundary at 2026-05-17 (three controls)"))
    # arm swap: the treated unit changes identity, so what is testable is whether
    # the four continuous arms moved across the boundary
    for eng in CONTINUOUS_ENGINES:
        did_rows.append(did(eng, [e for e in CONTINUOUS_ENGINES if e != eng],
                            (date(2026, 8, 8), date(2026, 8, 18)), (date(2026, 8, 23), date(2026, 9, 8)),
                            f"2026-08-19 arm swap, instrument-stability check on {eng} "
                            f"(treated vs the other continuous arms)"))
    didt = pd.DataFrame(did_rows)
    m = didt["status"] == "run"
    didt["lpm_q_bh"] = np.nan
    if m.sum() > 0:
        didt.loc[m, "lpm_q_bh"] = multipletests(didt.loc[m, "lpm_p"], method="fdr_bh")[1]
    didt.to_csv(data_dir / "s2_did.csv", index=False)
    R["did"] = didt.to_dict("records")
    log(didt[["label", "status", "raw_did_pp", "lpm_did_pp", "lpm_ci_lo_pp", "lpm_ci_hi_pp",
              "lpm_p", "boot_ci_lo_pp", "boot_ci_hi_pp", "n_clusters"]].to_string(index=False))

    # Groq vs Grok level contrast, reported as non-identified
    gq = df[(df["engine"] == "Groq")]
    gk = df[(df["engine"] == "Grok")]
    gk_post = gk[gk["day"] >= date(2026, 8, 31)]
    R["arm_swap_levels"] = dict(
        groq_rate_pct=float(100 * gq["cited"].mean()), groq_n=int(len(gq)),
        groq_last_day=str(gq["day"].max()),
        grok_all_rate_pct=float(100 * gk["cited"].mean()), grok_all_n=int(len(gk)),
        grok_post_effort_rate_pct=float(100 * gk_post["cited"].mean()) if len(gk_post) else None,
        grok_post_effort_n=int(len(gk_post)),
        grok_first_day=str(gk["day"].min()), grok_days=int(gk["day"].nunique()),
        identification="NOT IDENTIFIED: engine identity, provider, model and generation "
                       "configuration all change at the same boundary, and the arms never overlap in time.",
    )

    # ---- sensitivity: complete days only, headline rates -------------------
    sens = []
    for eng in ENGINES:
        a = df[df["engine"] == eng]
        b = a[a["day"].isin(complete_days)]
        if a.empty:
            continue
        lo_a, hi_a = wilson_ci(int(a["cited"].sum()), len(a))
        lo_b, hi_b = (wilson_ci(int(b["cited"].sum()), len(b)) if len(b) else (np.nan, np.nan))
        sens.append(dict(engine=eng, n_all=len(a), rate_all_pct=100 * a["cited"].mean(),
                         ci_lo_all=100 * lo_a, ci_hi_all=100 * hi_a,
                         n_complete=len(b),
                         rate_complete_pct=100 * b["cited"].mean() if len(b) else np.nan,
                         ci_lo_complete=100 * lo_b, ci_hi_complete=100 * hi_b,
                         delta_pp=(100 * b["cited"].mean() - 100 * a["cited"].mean()) if len(b) else np.nan))
    sensd = pd.DataFrame(sens)
    sensd.to_csv(data_dir / "s2_partial_day_sensitivity.csv", index=False)
    R["partial_day_sensitivity"] = sensd.to_dict("records")
    log(sensd.to_string(index=False))

    def _clean(o):
        if isinstance(o, dict):
            return {k: _clean(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)):
            return [_clean(v) for v in o]
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.floating,)):
            v = float(o)
            return None if math.isnan(v) else v
        if isinstance(o, float):
            return None if math.isnan(o) else o
        if isinstance(o, (np.bool_, bool)):
            return bool(o)
        if isinstance(o, (date, datetime)):
            return str(o)
        if o is None or isinstance(o, (str, int)):
            return o
        return str(o)

    (out_dir / "s2_results.json").write_text(
        json.dumps(_clean(R), indent=2, ensure_ascii=False), encoding="utf-8")
    log(f"\nWrote {out_dir/'s2_results.json'} and {len(list(data_dir.glob('*.csv')))} CSVs in {data_dir}")


if __name__ == "__main__":
    main()
