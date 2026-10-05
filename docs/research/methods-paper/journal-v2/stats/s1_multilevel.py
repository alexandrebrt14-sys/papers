#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S1 — Multilevel analysis of entity citation in generative engines.

Reproduces every number reported in `S1-multilevel.md`.

WHAT THIS SCRIPT DOES
---------------------
  0. Design audit .................. panel structure, partial days, window asymmetry,
                                     byte-identical response repeats, balanced sub-design.
  1. Multilevel binomial model ..... crossed random intercepts for query and collection
                                     date; fixed effects for engine, vertical, language,
                                     query type and query category. Odds ratios with 95%
                                     intervals, likelihood-ratio tests, and a two-way
                                     cluster-robust logistic model as the inferential
                                     anchor.
  2. Variance decomposition ........ response level (engine / query / day) and entity
                                     level (engine / entity / query / day), latent-scale
                                     ICC.
  3. Interactions .................. engine x vertical, engine x language,
                                     query type x vertical.
  4. Paired language effect ........ McNemar on PT/EN query pairs matched within the same
                                     engine and the same collection day.
  5. Robustness .................... complete days only; four-arm panel; stable-panel era;
                                     de-duplicated responses; native (non-uniform) window.
  6. Multiplicity .................. Benjamini-Hochberg over the declared family.

HARD RULES HONOURED HERE
------------------------
  * The database is opened read-only (`mode=ro`). Nothing is ever written to it.
  * Every number that reaches the .md comes out of this file. Nothing is typed by hand.
  * Cells with fewer than 30 observations are flagged `SMALL_N` and treated as descriptive.

USAGE
-----
    python s1_multilevel.py               # full run; measured 1,596.7 s on the
                                          # reference machine, of which ~1,200 s is
                                          # the entity-level decomposition
    python s1_multilevel.py --fast        # smaller entity subsample, one seed
    python s1_multilevel.py --skip-entity # everything except the entity-level GLMM

Results are printed to stdout and written to `s1_results.json` next to this file.

Author: statistical analysis track, journal-v2.
"""
from __future__ import annotations

import argparse
import json
import re
import math
import os
import sqlite3
import sys
import time
import warnings
from collections import OrderedDict
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from patsy import dmatrices
from scipy import stats
from statsmodels.genmod.bayes_mixed_glm import BinomialBayesMixedGLM
from statsmodels.stats.contingency_tables import mcnemar
from statsmodels.stats.proportion import proportion_confint

warnings.simplefilter("ignore")

# --------------------------------------------------------------------------------------
# Paths and repo modules that are reused rather than reimplemented
# --------------------------------------------------------------------------------------
REPO = Path("C:/Sandyboxclaude/papers")
DB_URI = "file:C:/Sandyboxclaude/papers/data/papers.db?mode=ro"
PARTIAL_DAYS_JSON = REPO / "data" / "partial_days.json"
HERE = Path(__file__).resolve().parent

sys.path.insert(0, str(REPO))

# Reused from the existing analysis package (do not reimplement):
#   benjamini_hochberg  -> src/analysis/hypothesis_engine.py
#   cluster_robust_mean -> src/analysis/cluster_robust.py
#   cohens_h            -> src/analysis/power_analysis.py
from src.analysis.cluster_robust import cluster_robust_mean  # noqa: E402
from src.analysis.hypothesis_engine import benjamini_hochberg  # noqa: E402
from src.analysis.power_analysis import cohens_h  # noqa: E402
from src.config_v2 import (  # noqa: E402
    COHORT_FINTECH_ANCHORS,
    COHORT_FINTECH_REAL,
    COHORT_HEALTH_ANCHORS,
    COHORT_HEALTH_REAL,
    COHORT_RETAIL_ANCHORS,
    COHORT_RETAIL_REAL,
    COHORT_TECHNOLOGY_ANCHORS,
    COHORT_TECHNOLOGY_REAL,
    FICTITIOUS_DECOYS_V2,
)

# NOTE on src/analysis/mixed_effects.py: `fit_cited_mixed_logit` wraps the same
# BinomialBayesMixedGLM used below, but it (a) stores exp(vcp) under the name
# "random_variances" when exp(vcp) is a standard DEVIATION, not a variance, and
# (b) discards `vcp_sd`, which we need for intervals on the variance components.
# We therefore call BinomialBayesMixedGLM directly and convert correctly:
#       sigma   = exp(vcp_mean)          (posterior median of the RE std. dev.)
#       sigma^2 = exp(2 * vcp_mean)
#       95% CrI = exp(vcp_mean +/- 1.96 * vcp_sd)   (lognormal VB posterior)

# --------------------------------------------------------------------------------------
# Study constants
# --------------------------------------------------------------------------------------
UNIFORM_WINDOW_CHARS = 200
CORE3_CATEGORIES = ["comparativo", "descoberta", "mercado"]  # the 96-query balanced battery
ALL_ENGINES = ["ChatGPT", "Claude", "Gemini", "Grok", "Groq", "Perplexity"]
SMALL_N = 30

# Explicit reference levels, so every contrast in the paper has a fixed meaning.
REF = {
    "llm": "ChatGPT",
    "vertical": "fintech",
    "query_lang": "en",
    "query_type": "directive",
    "query_category": "comparativo",
}

CANDIDATE_ENTITIES = {
    "fintech": [e.name for e in COHORT_FINTECH_REAL + COHORT_FINTECH_ANCHORS],
    "varejo": [e.name for e in COHORT_RETAIL_REAL + COHORT_RETAIL_ANCHORS],
    "saude": [e.name for e in COHORT_HEALTH_REAL + COHORT_HEALTH_ANCHORS],
    "tecnologia": [e.name for e in COHORT_TECHNOLOGY_REAL + COHORT_TECHNOLOGY_ANCHORS],
}

RESULTS: dict = OrderedDict()
PVALUE_REGISTRY: list[dict] = []  # declared family for BH-FDR


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def register_p(test_id: str, family: str, p: float, note: str = "") -> None:
    """Add a p-value to the declared multiplicity family (section 6)."""
    if p is None or (isinstance(p, float) and not np.isfinite(p)):
        return
    PVALUE_REGISTRY.append({"test_id": test_id, "family": family, "p_raw": float(p), "note": note})


# ======================================================================================
# 0. DATA
# ======================================================================================
def load_frame() -> pd.DataFrame:
    """Canonical study frame: COALESCE(is_probe,0)=0. Read-only connection."""
    con = sqlite3.connect(DB_URI, uri=True)
    try:
        df = pd.read_sql(
            """
            SELECT id,
                   timestamp,
                   llm,
                   model_version,
                   query,
                   query_category,
                   query_lang,
                   query_type,
                   vertical,
                   cited_v2,
                   cited_count_v2,
                   cited_entities_v2_json,
                   first_entity_v2,
                   first_entity_offset_v2,
                   response_length_chars_v2,
                   response_hash,
                   DATE(timestamp, '-3 hours') AS day,
                   DATE(timestamp)             AS day_utc
              FROM citations
             WHERE COALESCE(is_probe, 0) = 0
            """,
            con,
        )
    finally:
        con.close()
    return df


def add_derived(df: pd.DataFrame) -> pd.DataFrame:
    """Uniform-window outcome, pairing keys, era flags."""
    # --- The uniform 200-character outcome ------------------------------------------
    # Five arms stored only the first 200 characters, so `cited_v2` is already a
    # 200-character measurement for them. One arm (Perplexity) stored the whole
    # response, so `cited_v2` there is a whole-response measurement. Because
    # `first_entity_offset_v2` is the offset of the EARLIEST cohort entity in the
    # response, "at least one cohort entity inside the first 200 characters" is
    # exactly `cited_v2 = 1 AND first_entity_offset_v2 < 200`. This restores a
    # common observation window across all six arms without discarding any row.
    df["cited200"] = (
        (df["cited_v2"] == 1) & (df["first_entity_offset_v2"] < UNIFORM_WINDOW_CHARS)
    ).astype(int)
    df["cited_native"] = df["cited_v2"].fillna(0).astype(int)

    # Boundary sensitivity: require the canonical entity name to END before character
    # 200 as well. This is only an approximation of "fully contained", because a match
    # can be made through an alias shorter than the canonical name, which is why it
    # perturbs arms whose stored text is already exactly 200 characters. It is reported
    # to bracket the boundary decision, never used as the primary outcome.
    _name_len = df["first_entity_v2"].fillna("").str.len()
    df["cited200_strict"] = (
        (df["cited_v2"] == 1)
        & ((df["first_entity_offset_v2"] + _name_len) <= UNIFORM_WINDOW_CHARS)
    ).astype(int)

    # Collection day = Brazilian local date (UTC-3). The evening cron starts at 21:00
    # UTC and runs past midnight UTC, so a UTC calendar would split one collection round
    # across two "days". Under UTC-3 no round is split. `day_utc` is kept for the
    # sensitivity cut that re-clusters on the raw UTC date.

    # --- PT/EN pairing key -----------------------------------------------------------
    # The battery is 4 verticals x 6 categories x 2 query types x 2 temporal variants
    # ("... in 2026" vs. no year) x 2 languages = 192 queries, i.e. 96 PT/EN pairs.
    df["year_variant"] = df["query"].str.contains("2026", regex=False).astype(int)
    df["pair_id"] = (
        df["vertical"] + "|" + df["query_category"] + "|" + df["query_type"] + "|"
        + df["year_variant"].astype(str)
    )
    df["day"] = df["day"].astype(str)
    df["day_utc"] = df["day_utc"].astype(str)
    return df


def compute_partial_days(df: pd.DataFrame) -> dict:
    """A day is complete when every engine that is in-panel that day covered its full
    battery. Perplexity's battery is 96 queries (it never ran the confianca /
    experiencia / inovacao categories); every other arm's battery is 192.
    The empirical rule is unioned with the hand-curated data/partial_days.json.
    """
    expected = {e: (96 if e == "Perplexity" else 192) for e in ALL_ENGINES}
    span = df.groupby("llm")["day"].agg(["min", "max"])
    cov = df.groupby(["day", "llm"])["query"].nunique().unstack().fillna(0).astype(int)
    all_days = sorted(df["day"].unique())

    incomplete = {}
    for d in all_days:
        misses = []
        for e in ALL_ENGINES:
            if not (span.loc[e, "min"] <= d <= span.loc[e, "max"]):
                continue  # arm not in panel on that date
            got = int(cov.loc[d, e]) if e in cov.columns else 0
            if got < expected[e]:
                misses.append({"llm": e, "covered": got, "expected": expected[e]})
        if misses:
            incomplete[d] = misses

    curated = []
    if PARTIAL_DAYS_JSON.exists():
        curated = sorted({r["date"] for r in json.loads(PARTIAL_DAYS_JSON.read_text(encoding="utf-8"))})

    partial = sorted(set(incomplete) | (set(curated) & set(all_days)))
    return {
        "n_days_total": len(all_days),
        "day_min": all_days[0],
        "day_max": all_days[-1],
        "calendar_span_days": (pd.Timestamp(all_days[-1]) - pd.Timestamp(all_days[0])).days + 1,
        "partial_days": partial,
        "n_partial": len(partial),
        "n_complete": len(all_days) - len(partial),
        "detail": incomplete,
        "curated_json_dates": curated,
        "curated_json_dates_in_db": sorted(set(curated) & set(all_days)),
    }


def design_audit(df: pd.DataFrame) -> dict:
    """Everything a reader needs to judge whether the estimates are identified."""
    out: dict = OrderedDict()
    out["n_rows_canonical"] = int(len(df))
    out["n_queries"] = int(df["query"].nunique())
    out["n_pairs"] = int(df["pair_id"].nunique())
    out["n_days"] = int(df["day"].nunique())
    out["n_engines"] = int(df["llm"].nunique())

    # --- window asymmetry ------------------------------------------------------------
    win = (
        df.groupby("llm")
        .agg(
            n=("cited200", "size"),
            mean_chars_scored=("response_length_chars_v2", "mean"),
            max_chars_scored=("response_length_chars_v2", "max"),
            rate_native=("cited_native", "mean"),
            rate_uniform200=("cited200", "mean"),
        )
        .reset_index()
    )
    win["window_shift_pp"] = 100 * (win["rate_native"] - win["rate_uniform200"])
    win["rate_uniform200_strict"] = (
        df.groupby("llm")["cited200_strict"].mean().reindex(win["llm"]).to_numpy()
    )
    out["window_asymmetry"] = win.round(6).to_dict("records")
    out["day_coding"] = {
        "primary": "DATE(timestamp, '-3 hours')  (Brazilian local date, UTC-3)",
        "n_days_brt": int(df["day"].nunique()),
        "n_days_utc": int(df["day_utc"].nunique()),
        "rows_after_midnight_utc": int((df["timestamp"].str[11:13].isin(["00", "01"])).sum()),
    }

    # --- engine x category crossing --------------------------------------------------
    ct = pd.crosstab(df["llm"], df["query_category"])
    out["engine_by_category_counts"] = ct.to_dict()
    out["categories_missing_by_engine"] = {
        e: sorted(ct.columns[ct.loc[e] == 0].tolist()) for e in ct.index
    }

    # --- model version drift ---------------------------------------------------------
    mv = (
        df.groupby(["llm", "model_version"])["day"]
        .agg(n_rows="size", first="min", last="max")
        .reset_index()
    )
    out["model_versions"] = mv.to_dict("records")

    # --- byte-identical repeated responses -------------------------------------------
    # The protocol assumes cached answers never enter the series (8 h TTL against a
    # 12 h interval). We test that assumption directly against response_hash.
    cells = df.groupby(["llm", "query", "day"])["response_hash"].agg(["size", "nunique"]).reset_index()
    multi = cells[cells["size"] > 1]
    dup = (
        multi.assign(identical=(multi["nunique"] == 1).astype(int))
        .groupby("llm")
        .agg(cells_with_repeat=("identical", "size"), pct_byte_identical=("identical", "mean"))
        .reset_index()
    )
    dup["pct_byte_identical"] = 100 * dup["pct_byte_identical"]
    out["repeat_runs"] = {
        "n_cells_llm_query_day": int(len(cells)),
        "n_cells_with_more_than_one_run": int(len(multi)),
        "pct_multi_run_cells_byte_identical": float(100 * (multi["nunique"] == 1).mean()),
        "n_distinct_response_hashes": int(df["response_hash"].nunique()),
        "by_engine": dup.round(4).to_dict("records"),
    }

    # --- cohort ----------------------------------------------------------------------
    n_decoys = sum(len(v) for v in FICTITIOUS_DECOYS_V2.values())
    out["cohort"] = {
        "n_real_plus_anchors": sum(len(v) for v in CANDIDATE_ENTITIES.values()),
        "n_decoys": int(n_decoys),
        "n_total": int(sum(len(v) for v in CANDIDATE_ENTITIES.values()) + n_decoys),
        "candidates_per_vertical": {k: len(v) for k, v in CANDIDATE_ENTITIES.items()},
    }
    return out


# ======================================================================================
# Descriptive rates with intervals and N (small cells flagged)
# ======================================================================================
def rate_table(df: pd.DataFrame, by: list[str], outcome: str = "cited200") -> pd.DataFrame:
    """Cell rate with three intervals, because they answer three different questions.

    Wilson       treats the cell's rows as independent draws. They are not, and the
                 design is stratified rather than simple random, so this interval is
                 reported only as the conventional benchmark.
    Day-clustered (CR1, reused from src/analysis/cluster_robust.py) answers "if the same
                 96-query battery were run on new days". Because every collected day
                 replicates the full balanced battery, a day mean is a stratified mean
                 and its interval is usually NARROWER than Wilson. A ratio below one is
                 therefore the expected result here, not a defect.
    Query-clustered answers "if a new sample of queries had been drawn from the same
                 population of prompts". This is the interval that governs any claim
                 generalising beyond the 96 prompts actually used, and it is much wider.
    """
    rows = []
    for key, g in df.groupby(by):
        key = key if isinstance(key, tuple) else (key,)
        n = len(g)
        k = int(g[outcome].sum())
        lo, hi = proportion_confint(k, n, alpha=0.05, method="wilson")
        cr_d = cluster_robust_mean(g[outcome].to_numpy(), g["day"].to_numpy())
        cr_q = cluster_robust_mean(g[outcome].to_numpy(), g["query"].to_numpy())
        rows.append(
            dict(
                zip(by, key),
                n=n,
                k=k,
                rate=k / n,
                wilson_low=lo,
                wilson_high=hi,
                n_days=cr_d["n_clusters"],
                n_queries=cr_q["n_clusters"],
                se_iid=cr_d["se_iid"],
                se_day_cluster=cr_d["se_cluster"],
                se_query_cluster=cr_q["se_cluster"],
                ratio_day_over_iid=cr_d["inflation"],
                ratio_query_over_iid=cr_q["inflation"],
                cl_low=cr_d.get("ci_low_cluster", np.nan),
                cl_high=cr_d.get("ci_high_cluster", np.nan),
                q_low=cr_q.get("ci_low_cluster", np.nan),
                q_high=cr_q.get("ci_high_cluster", np.nan),
                flag="SMALL_N" if n < SMALL_N else "",
            )
        )
    return pd.DataFrame(rows)


# ======================================================================================
# 1. MODELS
# ======================================================================================
def _ref(var: str, data: pd.DataFrame | None) -> str:
    """Reference level for `var`. Falls back to the most frequent level when the
    canonical reference is absent from a subset (can happen in a robustness cut)."""
    r = REF[var]
    if data is None or r in set(data[var].unique()):
        return r
    return str(data[var].value_counts().index[0])


def build_formula(include: list[str], interaction: str | None = None,
                  data: pd.DataFrame | None = None) -> str:
    """Fixed part with explicit reference levels."""
    terms = [f"C({v}, Treatment('{_ref(v, data)}'))" for v in include]
    f = "cited200 ~ " + " + ".join(terms)
    if interaction:
        a, b = interaction.split("*")
        f += (f" + C({a}, Treatment('{_ref(a, data)}'))"
              f":C({b}, Treatment('{_ref(b, data)}'))")
    return f


_TERM_RE = re.compile(r"C\((\w+), Treatment\('[^']*'\)\)")


def pretty(name: str) -> str:
    """Turn a patsy term name into something a table can carry."""
    out = _TERM_RE.sub(r"\1", name)
    return out.replace("[T.", "=").replace("]", "").replace(":", " x ")


def fit_glmm(data: pd.DataFrame, formula: str, vc: dict, label: str,
             fixed_block: str | None = None) -> dict:
    """Crossed-random-intercept binomial GLMM by variational Bayes.

    statsmodels' BinomialBayesMixedGLM parameterises each variance component as
    log(sigma). `fit_vb` maximises an evidence lower bound, so its objective is NOT a
    log-likelihood and cannot be used for a likelihood-ratio test; see `lrt_block`.
    """
    t0 = time.time()
    try:
        model = BinomialBayesMixedGLM.from_formula(formula, vc, data)
        res = model.fit_vb(verbose=False)
        converged = True
        err = None
    except Exception as exc:  # pragma: no cover - documented, never silenced
        log(f"    GLMM '{label}' FAILED: {exc}")
        return {
            "label": label,
            "formula": formula,
            "vc": vc,
            "n_obs": int(len(data)),
            "converged": False,
            "error": str(exc),
        }

    zc = stats.norm.ppf(0.975)
    fixed = []
    for nm, mu, sd in zip(res.model.exog_names, res.fe_mean, res.fe_sd):
        z = mu / sd if sd > 0 else np.nan
        fixed.append(
            {
                "term": pretty(nm),
                "raw_term": nm,
                "beta": float(mu),
                "se": float(sd),
                "z": float(z),
                "p": float(2 * stats.norm.sf(abs(z))) if np.isfinite(z) else np.nan,
                "OR": float(np.exp(mu)),
                "OR_low": float(np.exp(mu - zc * sd)),
                "OR_high": float(np.exp(mu + zc * sd)),
            }
        )

    comps = []
    for nm, mu, sd in zip(res.model.vcp_names, res.vcp_mean, res.vcp_sd):
        comps.append(
            {
                "component": nm,
                "n_levels": int(data[nm].nunique()) if nm in data.columns else None,
                "sigma": float(np.exp(mu)),
                "sigma_low": float(np.exp(mu - zc * sd)),
                "sigma_high": float(np.exp(mu + zc * sd)),
                "sigma2": float(np.exp(2 * mu)),
                "sigma2_low": float(np.exp(2 * (mu - zc * sd))),
                "sigma2_high": float(np.exp(2 * (mu + zc * sd))),
            }
        )

    # Nakagawa-Schielzeth variance of a fixed-effect block. Used for the ENGINE level,
    # which has only five or six levels: a random intercept over so few levels is not
    # identified (see the stability ladder in the results), so the engine is carried as
    # a fixed factor and its contribution to the linear predictor is turned into a
    # variance component the same way Nakagawa and Schielzeth do for marginal R^2.
    ns = None
    if fixed_block is not None:
        X = np.asarray(res.model.exog, dtype=float)
        names = list(res.model.exog_names)
        idx = [i for i, nm in enumerate(names) if nm.startswith(f"C({fixed_block}")]
        if idx:
            beta = np.asarray(res.fe_mean)[idx]
            contrib = X[:, idx] @ beta
            # level means of the contribution, for the equal-weight variant
            lv = pd.DataFrame({"lvl": data[fixed_block].to_numpy(), "c": contrib})
            per_level = lv.groupby("lvl")["c"].mean()
            ns = {
                "block": fixed_block,
                "n_levels": int(len(per_level)),
                "sigma2_observation_weighted": float(np.var(contrib)),
                "sigma2_equal_weight_across_levels": float(np.var(per_level.to_numpy(), ddof=1)),
                "level_contributions": {k: float(v) for k, v in per_level.items()},
            }

    log(f"    GLMM '{label}' done in {time.time() - t0:.0f}s (n={len(data)})")
    return {
        "label": label,
        "formula": formula,
        "vc": vc,
        "n_obs": int(len(data)),
        "converged": converged,
        "error": err,
        "fixed": fixed,
        "variance_components": comps,
        "ns_fixed_block": ns,
        "elbo": float(getattr(res, "elbo", np.nan)) if hasattr(res, "elbo") else None,
        "fit_seconds": round(time.time() - t0, 1),
    }


def fit_glm_cluster(data: pd.DataFrame, formula: str, label: str) -> dict:
    """Pooled logistic model with two-way cluster-robust covariance (query, day).

    Two-way clustering (Cameron-Gelbach-Miller) is the right correction here: the same
    query recurs on every day and the same day carries every query, so neither margin
    nests inside the other. Degrees of freedom use min(G_query, G_day) - 1.
    """
    y, X = dmatrices(formula, data, return_type="dataframe")
    groups = np.column_stack(
        [pd.factorize(data["query"])[0], pd.factorize(data["day"])[0]]
    )
    mod = sm.GLM(y, X, family=sm.families.Binomial())
    naive = mod.fit()
    robust = mod.fit(
        cov_type="cluster",
        cov_kwds={"groups": groups, "use_correction": True, "df_correction": True},
    )
    g_min = min(data["query"].nunique(), data["day"].nunique())
    dfree = g_min - 1
    tcrit = stats.t.ppf(0.975, dfree)

    rows = []
    for nm in X.columns:
        b = float(naive.params[nm])
        se_n = float(naive.bse[nm])
        se_c = float(robust.bse[nm])
        t_stat = b / se_c if se_c > 0 else np.nan
        rows.append(
            {
                "term": pretty(nm),
                "raw_term": nm,
                "beta": b,
                "se_naive": se_n,
                "se_cluster2way": se_c,
                "se_inflation": se_c / se_n if se_n > 0 else np.nan,
                "OR": float(np.exp(b)),
                "OR_low": float(np.exp(b - tcrit * se_c)),
                "OR_high": float(np.exp(b + tcrit * se_c)),
                "t": float(t_stat),
                "df": int(dfree),
                "p": float(2 * stats.t.sf(abs(t_stat), dfree)) if np.isfinite(t_stat) else np.nan,
            }
        )
    return {
        "label": label,
        "formula": formula,
        "n_obs": int(len(data)),
        "n_query_clusters": int(data["query"].nunique()),
        "n_day_clusters": int(data["day"].nunique()),
        "df": int(dfree),
        "llf": float(naive.llf),
        "aic": float(naive.aic),
        "terms": rows,
        "_naive": naive,
        "_robust": robust,
        "_X": X,
    }



def block_wald(beta: np.ndarray, V: np.ndarray, dfree: int) -> dict:
    """Cluster-robust Wald test for a block of q coefficients.

    A two-way cluster-robust covariance has rank at most min(G_query, G_day) - 1, and
    it can be ill-conditioned when the block is wide. We therefore invert with a
    pseudo-inverse under an explicit tolerance, report the effective rank, and read the
    statistic as F = W / q on (q, df) rather than chi-square on q, because the
    chi-square version is anti-conservative with a few dozen clusters.
    """
    q = int(len(beta))
    eig = np.linalg.eigvalsh((V + V.T) / 2.0)
    tol = max(eig) * q * np.finfo(float).eps if len(eig) else 0.0
    rank = int((eig > tol).sum())
    Vinv = np.linalg.pinv(V, hermitian=True)
    W = float(beta @ Vinv @ beta)
    F = W / q
    return {
        "q": q,
        "wald_chi2": W,
        "p_wald_chi2": float(stats.chi2.sf(W, q)),
        "wald_F": float(F),
        "df_num": q,
        "df_den": int(dfree),
        "p_wald_F": float(stats.f.sf(F, q, dfree)) if dfree > 0 else float("nan"),
        "cov_rank": rank,
        "cov_full_rank": bool(rank == q),
        "cov_condition": float(max(eig) / min(eig)) if len(eig) and min(eig) > 0 else float("inf"),
        # A cluster-robust Wald test over-rejects once the block is wide relative to the
        # number of clusters. We flag it rather than hide it; for flagged blocks the
        # design-corrected LRT is the statistic to read.
        "q_over_clusters": float(q / (dfree + 1)) if dfree > 0 else float("nan"),
        "anticonservative_flag": bool(dfree > 0 and q / (dfree + 1) > 0.10),
    }


def lrt_block(full: dict, data: pd.DataFrame, block_var: str) -> dict:
    """Likelihood-ratio test for one fixed-effect block, in two versions.

    naive          : the textbook LRT from the pooled binomial likelihood. It assumes
                     independent observations, which this design violates, so it is
                     reported only as the uncorrected benchmark.
    design-corrected: Rao-Scott first-order correction, LRT / dbar, where dbar is the
                     generalised design effect of the dropped block,
                     dbar = trace(V_cluster[block] V_naive[block]^-1) / q.
                     This is the version that should be read.
    """
    keep = [v for v in full["_block_vars"] if v != block_var]
    f_red = build_formula(keep, data=data) if keep else "cited200 ~ 1"
    y, Xr = dmatrices(f_red, data, return_type="dataframe")
    red = sm.GLM(y, Xr, family=sm.families.Binomial()).fit()

    stat = 2 * (full["llf"] - red.llf)
    q = full["_X"].shape[1] - Xr.shape[1]
    idx = [i for i, nm in enumerate(full["_X"].columns) if nm not in set(Xr.columns)]
    Vc = np.asarray(full["_robust"].cov_params())[np.ix_(idx, idx)]
    Vn = np.asarray(full["_naive"].cov_params())[np.ix_(idx, idx)]
    dbar = float(np.trace(Vc @ np.linalg.inv(Vn)) / q)
    stat_rs = stat / dbar

    # Cluster-robust Wald for the same block (primary inference).
    beta = np.asarray(full["_naive"].params)[idx]
    w = block_wald(beta, Vc, full["df"])
    return {
        "block": block_var,
        "df": int(q),
        "lrt_naive": float(stat),
        "p_lrt_naive": float(stats.chi2.sf(stat, q)),
        "design_effect_dbar": dbar,
        "lrt_design_corrected": float(stat_rs),
        "p_lrt_design_corrected": float(stats.chi2.sf(stat_rs, q)),
        "wald_cluster2way": w["wald_chi2"],
        "p_wald_cluster2way": w["p_wald_F"],
        "wald_detail": w,
    }


# ======================================================================================
# 2. VARIANCE DECOMPOSITION
# ======================================================================================
def icc_from_components(comps: list[dict], extra: dict | None = None) -> dict:
    """Latent-scale ICC: sigma2_level / (sum sigma2 + pi^2/3).

    `extra` carries variance components that did not come from a random intercept —
    in practice the engine block, which is fitted as a fixed factor and converted to a
    variance by the Nakagawa-Schielzeth rule.
    """
    parts = {c["component"]: c["sigma2"] for c in comps}
    sds = {c["component"]: c["sigma"] for c in comps}
    if extra:
        for k, v in extra.items():
            parts[k] = float(v)
            sds[k] = float(math.sqrt(v))
    total = sum(parts.values()) + (math.pi ** 2) / 3
    return {
        "total_latent_variance": float(total),
        "residual_logistic": float((math.pi ** 2) / 3),
        "icc": {k: float(v / total) for k, v in parts.items()},
        "sigma": sds,
        "sigma2": parts,
    }


def vd_response_level(d3: pd.DataFrame) -> dict:
    """Three-way decomposition at the response level, on the balanced core-3 design.

    The primary specification carries the engine as a FIXED factor and converts its
    contribution to a variance by the Nakagawa-Schielzeth rule, because six levels are
    too few to identify a random-intercept variance (the stability ladder inside
    `vd_entity_level` shows what happens when one tries). The engine-as-random
    specification is fitted anyway and reported beside it, so the reader can see the
    size of the disagreement instead of taking our word for it.
    """
    log("  [2a] response-level variance decomposition (engine / query / day)")
    f_eng_fixed = "cited200 ~ C(llm, Treatment('{}'))".format(REF["llm"])
    m_fix = fit_glmm(d3, f_eng_fixed, {"query": "0 + C(query)", "day": "0 + C(day)"},
                     "VD-response, engine fixed", fixed_block="llm")
    m_ran = fit_glmm(d3, "cited200 ~ 1",
                     {"llm": "0 + C(llm)", "query": "0 + C(query)", "day": "0 + C(day)"},
                     "VD-response, engine random")

    out = {"model_engine_fixed": m_fix, "model_engine_random": m_ran}
    if m_fix["converged"] and m_fix["ns_fixed_block"]:
        ns = m_fix["ns_fixed_block"]
        out["primary"] = icc_from_components(
            m_fix["variance_components"], extra={"llm": ns["sigma2_equal_weight_across_levels"]}
        )
        out["primary"]["engine_variance_rule"] = (
            "Nakagawa-Schielzeth variance of the engine fixed-effect contribution, "
            "equal weight per engine level"
        )
        out["primary"]["engine_variance_observation_weighted"] = ns["sigma2_observation_weighted"]
        out["primary"]["engine_level_contributions"] = ns["level_contributions"]
    if m_ran["converged"]:
        out["engine_random_alternative"] = icc_from_components(m_ran["variance_components"])

    # Plug-in between-engine variance from six marginal logits, with no adjustment.
    rates = d3.groupby("llm")["cited200"].agg(["sum", "size"])
    logits = np.log((rates["sum"] + 0.5) / (rates["size"] - rates["sum"] + 0.5))
    out["plugin_between_engine"] = {
        "engine_logits": {k: float(v) for k, v in logits.items()},
        "variance_of_engine_logits": float(np.var(logits, ddof=1)),
        "note": "Haldane-Anscombe corrected marginal logits; unadjusted for composition.",
    }
    return out


def _entity_long(df5: pd.DataFrame, n_resp: int, seed: int):
    """Stratified subsample of responses (engine x vertical x category), expanded to one
    row per (response, candidate entity of that response's vertical)."""
    frac = min(1.0, n_resp / len(df5))
    rng = np.random.default_rng(seed)
    take = []
    for _, idx in df5.groupby(["llm", "vertical", "query_category"], sort=True).indices.items():
        k = max(1, int(round(len(idx) * frac)))
        take.append(rng.choice(idx, size=min(k, len(idx)), replace=False))
    sub = df5.iloc[np.concatenate(take)].reset_index(drop=True)
    rows = []
    for r in sub.itertuples():
        got = set(json.loads(r.cited_entities_v2_json or "[]"))
        for ent in CANDIDATE_ENTITIES[r.vertical]:
            rows.append((r.llm, ent, r.query, r.day, int(ent in got)))
    return pd.DataFrame(rows, columns=["llm", "entity", "query", "day", "y"]), len(sub)


def vd_entity_level(df5: pd.DataFrame, n_resp: int, seeds: list, ladder: list) -> dict:
    """Four-way decomposition at the (response x candidate entity) level.

    The unit is one cohort entity inside one response. The candidate set is the
    vertical's own roster (real companies plus international anchors), because the
    extractor only looks for entities belonging to the query's vertical.

    Perplexity is excluded: its stored text is the whole response, so
    `cited_entities_v2_json` cannot be restricted to the first 200 characters for any
    entity except the earliest one. The remaining five arms were truncated at 200
    characters at collection time, so their entity lists ARE the uniform window.

    The full long frame is about 1.7 M rows, which the variational fit cannot take, so
    the model runs on a stratified subsample of responses, repeated across independent
    seeds. A stability ladder over subsample sizes is fitted as well, because the
    engine-as-random specification does not hold still and the paper has to say so.
    """
    log("  [2b] entity-level variance decomposition (n_resp={}, seeds={})".format(n_resp, seeds))
    runs = []
    for seed in seeds:
        long, n_sub = _entity_long(df5, n_resp, seed)
        m_fix = fit_glmm(
            long, "y ~ C(llm, Treatment('{}'))".format(REF["llm"]),
            {"entity": "0 + C(entity)", "query": "0 + C(query)", "day": "0 + C(day)"},
            "VD-entity engine-fixed seed={}".format(seed), fixed_block="llm",
        )
        m_ran = fit_glmm(
            long, "y ~ 1",
            {"llm": "0 + C(llm)", "entity": "0 + C(entity)",
             "query": "0 + C(query)", "day": "0 + C(day)"},
            "VD-entity engine-random seed={}".format(seed),
        )
        rec = {"seed": seed, "n_responses": int(n_sub), "n_rows": int(len(long)),
               "mean_y": float(long["y"].mean()),
               "model_engine_fixed": m_fix, "model_engine_random": m_ran}
        if m_fix["converged"] and m_fix["ns_fixed_block"]:
            ns = m_fix["ns_fixed_block"]
            rec["primary"] = icc_from_components(
                m_fix["variance_components"],
                extra={"llm": ns["sigma2_equal_weight_across_levels"]},
            )
            rec["primary"]["engine_variance_observation_weighted"] = ns["sigma2_observation_weighted"]
            rec["primary"]["engine_level_contributions"] = ns["level_contributions"]
        if m_ran["converged"]:
            rec["engine_random_alternative"] = icc_from_components(m_ran["variance_components"])
        runs.append(rec)

    ok = [r for r in runs if "primary" in r]
    pooled = {}
    if ok:
        for comp in ["llm", "entity", "query", "day"]:
            vals = [r["primary"]["icc"][comp] for r in ok if comp in r["primary"]["icc"]]
            if vals:
                pooled[comp] = {"icc_mean": float(np.mean(vals)),
                                "icc_min": float(np.min(vals)),
                                "icc_max": float(np.max(vals))}

    # Stability ladder for the engine-as-random specification: the number the paper must
    # NOT report, published together with the evidence that it must not be reported.
    lad = []
    for n in ladder:
        long, n_sub = _entity_long(df5, n, seeds[0])
        m = fit_glmm(long, "y ~ 1",
                     {"llm": "0 + C(llm)", "entity": "0 + C(entity)",
                      "query": "0 + C(query)", "day": "0 + C(day)"},
                     "ladder engine-random n_resp={}".format(n))
        row = {"n_responses": int(n_sub), "n_rows": int(len(long)),
               "converged": m["converged"]}
        if m["converged"]:
            row["sigma"] = {c["component"]: c["sigma"] for c in m["variance_components"]}
        lad.append(row)

    # Marginal per-engine entity-slot logits: the model-free benchmark for the engine
    # variance component.
    slots, hits = {}, {}
    for e, g in df5.groupby("llm"):
        slots[e] = int(sum(len(CANDIDATE_ENTITIES[v]) for v in g["vertical"]))
        hits[e] = int(g["cited_count_v2"].where(g["cited200"] == 1, 0).sum())
    marg = {e: float(np.log((hits[e] + 0.5) / (slots[e] - hits[e] + 0.5))) for e in slots}

    return {
        "runs": runs,
        "pooled_icc_across_seeds": pooled,
        "engine_random_stability_ladder": lad,
        "marginal_engine_entity_logits": marg,
        "variance_of_marginal_engine_logits": float(np.var(list(marg.values()), ddof=1)),
        "entity_slots_per_engine": slots,
        "entity_hits_per_engine": hits,
        "n_responses_available": int(len(df5)),
        "long_rows_if_full": int(sum(len(CANDIDATE_ENTITIES[v]) for v in df5["vertical"])),
    }


# ======================================================================================
# 3. INTERACTIONS
# ======================================================================================
def interaction_tests(d3: pd.DataFrame, base_vars: list[str]) -> list[dict]:
    """Each interaction is tested against the same model without it."""
    y, X0 = dmatrices(build_formula(base_vars, data=d3), d3, return_type="dataframe")
    base = sm.GLM(y, X0, family=sm.families.Binomial())
    base_n = base.fit()
    groups = np.column_stack([pd.factorize(d3["query"])[0], pd.factorize(d3["day"])[0]])
    g_min = min(d3["query"].nunique(), d3["day"].nunique())

    specs = [
        ("llm*vertical", "engine x vertical"),
        ("llm*query_lang", "engine x language"),
        ("query_type*vertical", "query type x vertical"),
    ]
    out = []
    for spec, name in specs:
        log(f"  [3] interaction {name}")
        f = build_formula(base_vars, interaction=spec, data=d3)
        y1, X1 = dmatrices(f, d3, return_type="dataframe")
        m1 = sm.GLM(y1, X1, family=sm.families.Binomial())
        fit_n = m1.fit()
        fit_c = m1.fit(cov_type="cluster",
                       cov_kwds={"groups": groups, "use_correction": True, "df_correction": True})

        stat = 2 * (fit_n.llf - base_n.llf)
        q = X1.shape[1] - X0.shape[1]
        idx = [i for i, nm in enumerate(X1.columns) if nm not in set(X0.columns)]
        Vc = np.asarray(fit_c.cov_params())[np.ix_(idx, idx)]
        Vn = np.asarray(fit_n.cov_params())[np.ix_(idx, idx)]
        dbar = float(np.trace(Vc @ np.linalg.inv(Vn)) / q)
        beta = np.asarray(fit_n.params)[idx]
        w = block_wald(beta, Vc, g_min - 1)

        # Practical magnitude: observed cell rates on the interacting margins.
        a, b = spec.split("*")
        cell = rate_table(d3, [a, b])
        spread = (
            cell.assign(lo=cell["rate"])
            .groupby(a)["rate"]
            .agg(lambda s: float(s.max() - s.min()))
        )

        rec = {
            "interaction": name,
            "spec": spec,
            "df": int(q),
            "lrt_naive": float(stat),
            "p_lrt_naive": float(stats.chi2.sf(stat, q)),
            "design_effect_dbar": dbar,
            "lrt_design_corrected": float(stat / dbar),
            "p_lrt_design_corrected": float(stats.chi2.sf(stat / dbar, q)),
            "wald_cluster2way": w["wald_chi2"],
            "p_wald_cluster2way": w["p_wald_F"],
            "wald_detail": w,
            "delta_aic_vs_base": float(fit_n.aic - base_n.aic),
            "pseudo_r2_gain": float((fit_n.llf - base_n.llf) / abs(base_n.llf)),
            "n_obs": int(len(d3)),
            "n_clusters_min": int(g_min),
            "cell_rates": cell.round(6).to_dict("records"),
            "within_level_rate_spread_pp": {k: round(100 * v, 2) for k, v in spread.items()},
        }
        register_p(f"interaction::{name}", "S1-confirmatory", rec["p_wald_cluster2way"],
                   "cluster-robust Wald, interaction block test")
        out.append(rec)
    return out


# ======================================================================================
# 4. PAIRED LANGUAGE EFFECT
# ======================================================================================
def paired_language(df: pd.DataFrame) -> dict:
    """McNemar on PT/EN pairs matched inside the same engine and the same day.

    One binary observation per (engine, day, query) is taken as the FIRST run of that
    cell by timestamp, so that repeated runs inside a day cannot enter the pair twice.
    A pair contributes only when both languages of the same query template were
    collected on that engine on that day.
    """
    log("  [4] paired PT/EN McNemar")
    first = (
        df.sort_values("timestamp")
        .drop_duplicates(subset=["llm", "day", "query"], keep="first")
    )
    wide = first.pivot_table(
        index=["llm", "day", "pair_id"], columns="query_lang", values="cited200", aggfunc="first"
    ).dropna()
    wide = wide.reset_index()
    wide["d"] = wide["pt"] - wide["en"]

    def one(g: pd.DataFrame, label: str) -> dict:
        n = len(g)
        n11 = int(((g["pt"] == 1) & (g["en"] == 1)).sum())
        n10 = int(((g["pt"] == 1) & (g["en"] == 0)).sum())  # PT only
        n01 = int(((g["pt"] == 0) & (g["en"] == 1)).sum())  # EN only
        n00 = int(((g["pt"] == 0) & (g["en"] == 0)).sum())
        tbl = np.array([[n11, n10], [n01, n00]])
        disc = n10 + n01
        if disc == 0:
            return {"stratum": label, "n_pairs": n, "n_discordant": 0, "flag": "NO_DISCORDANT_PAIRS"}
        mc_chi = mcnemar(tbl, exact=False, correction=True)
        mc_ex = mcnemar(tbl, exact=True)
        # Paired difference with a day-clustered interval (CR1). cluster_robust_mean's
        # own se_iid assumes a 0/1 variable, so for the signed difference d in {-1,0,1}
        # the iid benchmark is recomputed here as sd(d)/sqrt(n).
        cr = cluster_robust_mean(g["d"].to_numpy(), g["day"].to_numpy())
        tcrit = stats.t.ppf(0.975, max(1, cr["n_clusters"] - 1))
        diff = float(g["d"].mean())
        se_iid = float(g["d"].std(ddof=1) / math.sqrt(n)) if n > 1 else float("nan")
        # Exact interval for the conditional odds of a PT-only over an EN-only discordance.
        lo_p, hi_p = proportion_confint(n10, disc, alpha=0.05, method="beta")
        rec = {
            "stratum": label,
            "n_pairs": int(n),
            "n_days": int(cr["n_clusters"]),
            "rate_pt": float(g["pt"].mean()),
            "rate_en": float(g["en"].mean()),
            "n11": n11, "n10_pt_only": n10, "n01_en_only": n01, "n00": n00,
            "n_discordant": int(disc),
            "paired_diff_pt_minus_en": diff,
            "se_day_cluster": float(cr["se_cluster"]),
            "se_iid": se_iid,
            "se_inflation": float(cr["se_cluster"] / se_iid) if se_iid > 0 else float("nan"),
            "ci_low": diff - tcrit * float(cr["se_cluster"]),
            "ci_high": diff + tcrit * float(cr["se_cluster"]),
            "mcnemar_chi2_cc": float(mc_chi.statistic),
            "p_mcnemar_chi2_cc": float(mc_chi.pvalue),
            "p_mcnemar_exact": float(mc_ex.pvalue),
            "discordance_or_pt_over_en": float(n10 / n01) if n01 else np.inf,
            "discordance_share_pt": float(n10 / disc),
            "discordance_share_pt_ci": [float(lo_p), float(hi_p)],
            "cohens_h": float(cohens_h(g["pt"].mean(), g["en"].mean())),
            "flag": "SMALL_N" if n < SMALL_N or disc < SMALL_N else "",
        }
        return rec

    overall = one(wide, "ALL ENGINES")
    register_p("paired_language::overall", "S1-confirmatory", overall.get("p_mcnemar_exact"),
               "McNemar exact, PT vs EN")
    by_engine = []
    for e, g in wide.groupby("llm"):
        rec = one(g, e)
        register_p(f"paired_language::{e}", "S1-confirmatory", rec.get("p_mcnemar_exact"),
                   "McNemar exact, PT vs EN within engine")
        by_engine.append(rec)

    # ---------------------------------------------------------------------------------
    # Engine x language, tested INSIDE the pairing.
    #
    # The marginal model cannot see this interaction: language varies only between
    # queries there, so the whole between-query variance lands on the language contrast
    # and the design correction eats the power. Inside a pair the query template is
    # held fixed, so the paired difference d = y_pt - y_en is free of it. Regressing d
    # on the engine and testing that block is therefore the design-valid test of
    # engine x language, and a linear model is the right one because d is already a
    # difference of two probabilities and its coefficients read in percentage points.
    # Standard errors are two-way cluster-robust on (collection day, query pair).
    # ---------------------------------------------------------------------------------
    inter = {"available": False}
    if wide["llm"].nunique() > 1:
        ref_llm = _ref("llm", wide)
        yv, Xv = dmatrices(f"d ~ C(llm, Treatment('{ref_llm}'))", wide, return_type="dataframe")
        groups = np.column_stack(
            [pd.factorize(wide["day"])[0], pd.factorize(wide["pair_id"])[0]]
        )
        ols = sm.OLS(yv, Xv)
        fit_n = ols.fit()
        fit_c = ols.fit(cov_type="cluster",
                        cov_kwds={"groups": groups, "use_correction": True,
                                  "df_correction": True})
        g_min = min(wide["day"].nunique(), wide["pair_id"].nunique())
        idx = [i for i, nm in enumerate(Xv.columns) if nm != "Intercept"]
        Vc = np.asarray(fit_c.cov_params())[np.ix_(idx, idx)]
        beta = np.asarray(fit_n.params)[idx]
        w = block_wald(beta, Vc, g_min - 1)
        tcrit = stats.t.ppf(0.975, g_min - 1)
        terms = []
        for nm in Xv.columns:
            b = float(fit_n.params[nm])
            se = float(fit_c.bse[nm])
            t_ = b / se if se > 0 else np.nan
            terms.append({
                "term": pretty(nm) if nm != "Intercept" else f"Intercept (= {ref_llm} paired diff)",
                "estimate_pp": 100 * b,
                "se_pp": 100 * se,
                "ci_low_pp": 100 * (b - tcrit * se),
                "ci_high_pp": 100 * (b + tcrit * se),
                "t": float(t_),
                "p": float(2 * stats.t.sf(abs(t_), g_min - 1)) if np.isfinite(t_) else np.nan,
            })
        inter = {
            "available": True,
            "reference_engine": ref_llm,
            "n_pairs": int(len(wide)),
            "n_day_clusters": int(wide["day"].nunique()),
            "n_pair_clusters": int(wide["pair_id"].nunique()),
            "df": int(g_min - 1),
            "terms": terms,
            "block_test": w,
        }
        register_p("interaction::engine x language (within-pair)", "S1-confirmatory",
                   w["p_wald_F"], "paired difference regressed on engine, two-way cluster-robust")

    return {
        "n_complete_pairs": int(len(wide)),
        "pairing_key": "vertical | category | query_type | year_variant, matched on (engine, day)",
        "overall": overall,
        "by_engine": by_engine,
        "engine_by_language_within_pair": inter,
    }


# ======================================================================================
# 5. ROBUSTNESS
# ======================================================================================
PRINCIPAL_TERMS = [
    ("llm=Perplexity", "engine: Perplexity vs ChatGPT"),
    ("llm=Gemini", "engine: Gemini vs ChatGPT"),
    ("query_lang=pt", "language: PT vs EN"),
    ("query_type=exploratory", "query type: exploratory vs directive"),
]


def principal_row(model: dict, cut: str, n: int, note: str) -> list[dict]:
    rows = []
    lookup = {t["term"]: t for t in model["terms"]}
    for term, label in PRINCIPAL_TERMS:
        t = lookup.get(term)
        if t is None:
            rows.append({"cut": cut, "coefficient": label, "n_obs": n, "flag": "NOT_IDENTIFIED",
                         "note": note})
            continue
        rows.append({
            "cut": cut, "coefficient": label, "n_obs": n,
            "beta": t["beta"], "OR": t["OR"], "OR_low": t["OR_low"], "OR_high": t["OR_high"],
            "se_cluster2way": t["se_cluster2way"], "p": t["p"], "note": note,
            "flag": "SMALL_N" if n < SMALL_N else "",
        })
    return rows


def robustness(df: pd.DataFrame, partial: dict, base_vars: list[str]) -> dict:
    """The principal coefficients re-estimated under five alternative cuts."""
    log("  [5] robustness cuts")
    d3 = df[df["query_category"].isin(CORE3_CATEGORIES)].copy()
    cuts = []

    def add(sub: pd.DataFrame, cut: str, note: str, outcome: str = "cited200"):
        sub = sub.copy()
        if outcome != "cited200":
            sub["cited200"] = sub[outcome]
        keep = [v for v in base_vars if sub[v].nunique() > 1]
        f = build_formula(keep, data=sub)
        try:
            m = fit_glm_cluster(sub, f, cut)
        except Exception as exc:
            cuts.append({"cut": cut, "n_obs": int(len(sub)), "flag": "FAILED",
                         "error": str(exc), "note": note})
            return
        for r in principal_row(m, cut, len(sub), note):
            cuts.append(r)
        for t in m["terms"]:
            if t["raw_term"] != "Intercept":
                register_p(f"robust::{cut}::{t['term']}", "S1-robustness", t["p"], note)

    add(d3, "A. reference (core-3 balanced, uniform 200-char window)",
        "all six arms, 96 matched queries")
    add(d3[~d3["day"].isin(partial["partial_days"])], "B. complete days only",
        f"{partial['n_partial']} partial days dropped")
    add(d3[~d3["llm"].isin(["Groq", "Grok"])], "C. four-arm panel (no Groq, no Grok)",
        "arm that left and arm that joined both removed")
    stable = d3[(d3["day"] >= "2026-04-23") & (d3["day"] <= "2026-06-09")]
    add(stable, "D. stable-panel era 2026-04-23..2026-06-09",
        "constant five-arm panel, Gemini still on 2.5-pro")
    dedup = d3.drop_duplicates(subset=["llm", "query", "day", "response_hash"])
    add(dedup, "E. byte-identical repeats collapsed",
        "one row per (engine, query, day, response_hash)")
    add(d3, "F. native window (no uniform 200-char rule)",
        "shown only to quantify how much the window rule moves the engine contrast",
        outcome="cited_native")
    add(d3, "G. strict boundary (entity name must end before char 200)",
        "brackets the boundary decision; approximate because a match can come via an alias",
        outcome="cited200_strict")
    d3_utc = d3.copy()
    d3_utc["day"] = d3_utc["day_utc"]
    add(d3_utc, "H. day index in UTC instead of Brazilian local time",
        "re-clusters on the raw UTC date, which splits the evening round across two days")

    return {"rows": cuts,
            "n_stable_era_days": int(stable["day"].nunique()),
            "n_dedup_rows": int(len(dedup)),
            "n_reference_rows": int(len(d3))}


# ======================================================================================
# 6. MULTIPLICITY
# ======================================================================================
def multiplicity(alpha: float = 0.05) -> dict:
    fams = {}
    for fam in sorted({r["family"] for r in PVALUE_REGISTRY}):
        rows = [r for r in PVALUE_REGISTRY if r["family"] == fam]
        adj = benjamini_hochberg([r["p_raw"] for r in rows], alpha=alpha)
        for r, a in zip(rows, adj):
            r["p_bh"] = float(a)
            r["survives_bh"] = bool(a < alpha)
        fams[fam] = {
            "m_tests": len(rows),
            "alpha_fdr": alpha,
            "n_survive": int(sum(r["survives_bh"] for r in rows)),
            "tests": sorted(rows, key=lambda r: r["p_raw"]),
        }
    return fams


# ======================================================================================
# MAIN
# ======================================================================================
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fast", action="store_true", help="smaller entity subsample, one seed")
    ap.add_argument("--skip-entity", action="store_true")
    ap.add_argument("--out", default=str(HERE / "s1_results.json"))
    args = ap.parse_args()

    t_start = time.time()
    log("[0] loading canonical frame (read-only)")
    df = add_derived(load_frame())
    partial = compute_partial_days(df)
    RESULTS["design"] = design_audit(df)
    RESULTS["partial_days"] = partial
    log(f"    N={len(df)}  queries={df['query'].nunique()}  days={df['day'].nunique()} "
        f"  partial_days={partial['n_partial']}")

    base_vars = ["llm", "vertical", "query_lang", "query_type", "query_category"]
    d3 = df[df["query_category"].isin(CORE3_CATEGORIES)].copy()
    d_noppl = df[df["llm"] != "Perplexity"].copy()
    RESULTS["subsets"] = {
        "core3_balanced_n": int(len(d3)),
        "core3_queries": int(d3["query"].nunique()),
        "full_n": int(len(df)),
        "five_arm_full_battery_n": int(len(d_noppl)),
    }

    # --- descriptives -----------------------------------------------------------------
    log("[0b] descriptive rates")
    RESULTS["rates"] = {
        "overall_core3": rate_table(d3, ["llm"]).round(6).to_dict("records"),
        "overall_full": rate_table(df, ["llm"]).round(6).to_dict("records"),
        "by_vertical": rate_table(d3, ["vertical"]).round(6).to_dict("records"),
        "by_language": rate_table(d3, ["query_lang"]).round(6).to_dict("records"),
        "by_query_type": rate_table(d3, ["query_type"]).round(6).to_dict("records"),
        "by_category_five_arm": rate_table(d_noppl, ["query_category"]).round(6).to_dict("records"),
        "engine_by_vertical": rate_table(d3, ["llm", "vertical"]).round(6).to_dict("records"),
        "engine_by_language": rate_table(d3, ["llm", "query_lang"]).round(6).to_dict("records"),
    }

    # --- 1. models ---------------------------------------------------------------------
    log("[1] multilevel models")
    vc = {"query": "0 + C(query)", "day": "0 + C(day)"}
    f_main = build_formula(base_vars)

    RESULTS["m0_null_glmm"] = fit_glmm(d3, "cited200 ~ 1", vc, "M0 null (core-3)")
    RESULTS["m1_glmm_core3"] = fit_glmm(d3, f_main, vc, "M1 primary (core-3 balanced)")
    RESULTS["m1full_glmm_all"] = fit_glmm(df, f_main, vc, "M1-full (all 192 queries)")
    RESULTS["m1cat_glmm_5arm"] = fit_glmm(
        d_noppl, f_main, vc, "M1-cat (five arms, all six categories)"
    )

    log("  [1b] cluster-robust logistic (primary inference)")
    glm_core3 = fit_glm_cluster(d3, f_main, "M2 cluster-robust (core-3)")
    glm_core3["_block_vars"] = base_vars
    RESULTS["m2_cluster_robust_core3"] = {
        k: v for k, v in glm_core3.items() if not k.startswith("_")
    }
    for t in glm_core3["terms"]:
        if t["raw_term"] != "Intercept":
            register_p(f"contrast::{t['term']}", "S1-contrasts", t["p"],
                       "two-way cluster-robust t test, core-3 model")

    glm_5arm = fit_glm_cluster(d_noppl, f_main, "M2-cat cluster-robust (five arms)")
    glm_5arm["_block_vars"] = base_vars
    RESULTS["m2cat_cluster_robust_5arm"] = {
        k: v for k, v in glm_5arm.items() if not k.startswith("_")
    }

    log("  [1c] likelihood-ratio tests per fixed-effect block")
    RESULTS["lrt_core3"] = [lrt_block(glm_core3, d3, v) for v in base_vars]
    for r in RESULTS["lrt_core3"]:
        register_p(f"lrt::{r['block']}", "S1-confirmatory", r["p_lrt_design_corrected"],
                   "Rao-Scott design-corrected LRT, core-3 model")
    RESULTS["lrt_5arm_categories"] = [lrt_block(glm_5arm, d_noppl, "query_category")]
    for r in RESULTS["lrt_5arm_categories"]:
        register_p(f"lrt::{r['block']}@5arm", "S1-confirmatory", r["p_lrt_design_corrected"],
                   "Rao-Scott design-corrected LRT, five-arm six-category model")

    # --- 2. variance decomposition ------------------------------------------------------
    log("[2] variance decomposition")
    RESULTS["vd_response"] = vd_response_level(d3)
    if args.skip_entity:
        RESULTS["vd_entity"] = {"skipped": True}
    else:
        n_resp = 2000 if args.fast else 6000
        seeds = [11] if args.fast else [11, 23, 47]
        ladder = [1000] if args.fast else [1500, 3000]
        RESULTS["vd_entity"] = vd_entity_level(d_noppl, n_resp, seeds, ladder)

    # --- 3. interactions -----------------------------------------------------------------
    log("[3] interactions")
    RESULTS["interactions"] = interaction_tests(d3, base_vars)

    # --- 4. paired language ---------------------------------------------------------------
    RESULTS["paired_language"] = paired_language(df)

    # --- 5. robustness ---------------------------------------------------------------------
    RESULTS["robustness"] = robustness(df, partial, base_vars)

    # --- 6. multiplicity -------------------------------------------------------------------
    log("[6] Benjamini-Hochberg")
    RESULTS["multiplicity"] = multiplicity(alpha=0.05)

    RESULTS["_meta"] = {
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "runtime_seconds": round(time.time() - t_start, 1),
        "python": sys.version.split()[0],
        "numpy": np.__version__,
        "pandas": pd.__version__,
        "statsmodels": sm.__version__,
        "scipy": __import__("scipy").__version__,
        "db": DB_URI,
        "uniform_window_chars": UNIFORM_WINDOW_CHARS,
        "outcome_definition": "cited200 = (cited_v2 == 1) AND (first_entity_offset_v2 < 200)",
        "fast_mode": bool(args.fast),
    }

    Path(args.out).write_text(json.dumps(RESULTS, indent=2, default=str), encoding="utf-8")
    log(f"[done] {args.out}  ({RESULTS['_meta']['runtime_seconds']}s)")
    print_report()


# ======================================================================================
# Console report (the tables that go into the .md)
# ======================================================================================
def fmt_or(t: dict) -> str:
    return f"{t['OR']:.3f} [{t['OR_low']:.3f}, {t['OR_high']:.3f}]"


def print_report() -> None:
    R = RESULTS
    p = print
    p("\n" + "=" * 96)
    p("S1 MULTILEVEL — CONSOLE REPORT")
    p("=" * 96)

    p("\n--- Table S1.0 window asymmetry (native vs uniform 200-char outcome) ---")
    p(f"{'engine':<12}{'n':>8}{'mean chars':>12}{'rate native':>13}{'rate 200':>11}{'shift pp':>10}")
    for r in R["design"]["window_asymmetry"]:
        p(f"{r['llm']:<12}{r['n']:>8}{r['mean_chars_scored']:>12.1f}"
          f"{r['rate_native']:>13.4f}{r['rate_uniform200']:>11.4f}{r['window_shift_pp']:>10.2f}")

    p("\n--- Table S1.1 citation rate by engine, core-3 balanced design ---")
    p(f"{'engine':<12}{'n':>7}{'k':>7}{'rate':>8}{'Wilson 95%':>20}{'day-clustered 95%':>22}"
      f"{'query-clustered 95%':>24}{'flag':>9}")
    for r in R["rates"]["overall_core3"]:
        p(f"{r['llm']:<12}{r['n']:>7}{r['k']:>7}{r['rate']:>8.4f}"
          f"   [{r['wilson_low']:.4f}, {r['wilson_high']:.4f}]"
          f"   [{r['cl_low']:.4f}, {r['cl_high']:.4f}]"
          f"   [{r['q_low']:.4f}, {r['q_high']:.4f}]{r['flag']:>9}")

    for key, title in [("m1_glmm_core3", "Table S1.2 GLMM M1 (core-3 balanced)"),
                       ("m1full_glmm_all", "Table S1.2b GLMM M1-full (all 192 queries)"),
                       ("m1cat_glmm_5arm", "Table S1.2c GLMM M1-cat (five arms, six categories)")]:
        m = R.get(key, {})
        p(f"\n--- {title} | converged={m.get('converged')} n={m.get('n_obs')} ---")
        if not m.get("converged"):
            p(f"    NOT ESTIMATED: {m.get('error')}")
            continue
        for t in m["fixed"]:
            p(f"  {t['term']:<34} beta={t['beta']:>8.4f}  OR={fmt_or(t):<28} p={t['p']:.3g}")
        for c in m["variance_components"]:
            p(f"  [RE] {c['component']:<10} levels={c['n_levels']}  sigma={c['sigma']:.3f} "
              f"[{c['sigma_low']:.3f}, {c['sigma_high']:.3f}]  sigma2={c['sigma2']:.3f}")

    p("\n--- Table S1.3 cluster-robust logistic (core-3), primary inference ---")
    m2 = R["m2_cluster_robust_core3"]
    p(f"    clusters: {m2['n_query_clusters']} queries x {m2['n_day_clusters']} days, df={m2['df']}")
    p(f"{'term':<34}{'OR [95% CI]':>30}{'SE naive':>11}{'SE 2-way':>10}{'infl':>7}{'p':>11}")
    for t in m2["terms"]:
        p(f"{t['term']:<34}{fmt_or(t):>30}{t['se_naive']:>11.4f}"
          f"{t['se_cluster2way']:>10.4f}{t['se_inflation']:>7.2f}{t['p']:>11.3g}")

    p("\n--- Table S1.4 likelihood-ratio tests per block (core-3) ---")
    p(f"{'block':<18}{'df':>4}{'LRT naive':>12}{'p naive':>11}{'dbar':>8}{'LRT corr':>11}{'p corr':>11}{'p Wald CR':>12}")
    for r in R["lrt_core3"]:
        p(f"{r['block']:<18}{r['df']:>4}{r['lrt_naive']:>12.1f}{r['p_lrt_naive']:>11.2g}"
          f"{r['design_effect_dbar']:>8.2f}{r['lrt_design_corrected']:>11.2f}"
          f"{r['p_lrt_design_corrected']:>11.3g}{r['p_wald_cluster2way']:>12.3g}"
          f"{'' if r['wald_detail']['cov_full_rank'] else '  RANK_DEFICIENT'}")
    for r in R["lrt_5arm_categories"]:
        p(f"{r['block']+' (5-arm)':<18}{r['df']:>4}{r['lrt_naive']:>12.1f}{r['p_lrt_naive']:>11.2g}"
          f"{r['design_effect_dbar']:>8.2f}{r['lrt_design_corrected']:>11.2f}"
          f"{r['p_lrt_design_corrected']:>11.3g}{r['p_wald_cluster2way']:>12.3g}")

    p("\n--- Table S1.5 variance decomposition ---")
    vr = R["vd_response"]
    if "primary" in vr:
        p("  response level, PRIMARY (engine as fixed factor, NS variance):")
        for k, v in vr["primary"]["icc"].items():
            p(f"    {k:<10} sigma={vr['primary']['sigma'][k]:.3f}  "
              f"sigma2={vr['primary']['sigma2'][k]:.3f}  ICC={v:.4f}")
        p(f"    total latent variance = {vr['primary']['total_latent_variance']:.3f}")
    if "engine_random_alternative" in vr:
        a = vr["engine_random_alternative"]
        p("  response level, engine-as-random alternative (shown for contrast):")
        for k, v in a["icc"].items():
            p(f"    {k:<10} sigma={a['sigma'][k]:.3f}  ICC={v:.4f}")
    p(f"  plug-in variance of marginal engine logits = "
      f"{vr['plugin_between_engine']['variance_of_engine_logits']:.3f}")
    ve = R.get("vd_entity", {})
    if ve.get("pooled_icc_across_seeds"):
        p("  entity level, PRIMARY (engine fixed), across seeds:")
        for k, v in ve["pooled_icc_across_seeds"].items():
            p(f"    {k:<10} ICC mean={v['icc_mean']:.4f}  range=[{v['icc_min']:.4f}, {v['icc_max']:.4f}]")
        p(f"  variance of marginal engine entity-slot logits = "
          f"{ve['variance_of_marginal_engine_logits']:.3f}")
        p("  engine-as-random stability ladder (why the random version is not reported):")
        for row in ve["engine_random_stability_ladder"]:
            sg = row.get("sigma", {})
            p(f"    n_resp={row['n_responses']:<6} rows={row['n_rows']:<8} "
              f"sigma_llm={sg.get('llm', float('nan')):.3f} "
              f"sigma_entity={sg.get('entity', float('nan')):.3f} "
              f"sigma_query={sg.get('query', float('nan')):.3f} "
              f"sigma_day={sg.get('day', float('nan')):.3f}")
        for r in ve["runs"]:
            a = r.get("engine_random_alternative")
            if a:
                p(f"    seed={r['seed']} engine-random at n_resp={r['n_responses']}: "
                  f"sigma_llm={a['sigma']['llm']:.3f}")

    p("\n--- Table S1.6 interactions ---")
    p(f"{'interaction':<26}{'df':>4}{'LRT naive':>12}{'dbar':>8}{'LRT corr':>11}{'p corr':>11}{'p Wald CR':>12}{'dAIC':>10}")
    for r in R["interactions"]:
        p(f"{r['interaction']:<26}{r['df']:>4}{r['lrt_naive']:>12.1f}{r['design_effect_dbar']:>8.2f}"
          f"{r['lrt_design_corrected']:>11.2f}{r['p_lrt_design_corrected']:>11.3g}"
          f"{r['p_wald_cluster2way']:>12.3g}{r['delta_aic_vs_base']:>10.1f}"
          f"{'  WALD_ANTICONSERVATIVE' if r['wald_detail']['anticonservative_flag'] else ''}")

    p("\n--- Table S1.7 paired PT/EN (McNemar) ---")
    pl = R["paired_language"]
    p(f"    complete pairs: {pl['n_complete_pairs']}  key: {pl['pairing_key']}")
    hdr = f"{'stratum':<14}{'pairs':>7}{'PT':>8}{'EN':>8}{'diff':>9}{'95% CI':>20}{'PT-only':>9}{'EN-only':>9}{'p exact':>11}{'flag':>10}"
    p(hdr)
    for r in [pl["overall"]] + pl["by_engine"]:
        if r.get("flag") == "NO_DISCORDANT_PAIRS":
            p(f"{r['stratum']:<14}{r['n_pairs']:>7}{'-':>8}{'-':>8}{'-':>9}{'-':>20}{'-':>9}{'-':>9}{'-':>11}{r['flag']:>10}")
            continue
        p(f"{r['stratum']:<14}{r['n_pairs']:>7}{r['rate_pt']:>8.4f}{r['rate_en']:>8.4f}"
          f"{r['paired_diff_pt_minus_en']:>9.4f}"
          f"  [{r['ci_low']:>6.4f},{r['ci_high']:>7.4f}]"
          f"{r['n10_pt_only']:>9}{r['n01_en_only']:>9}{r['p_mcnemar_exact']:>11.3g}{r.get('flag',''):>10}")

    pi = R["paired_language"].get("engine_by_language_within_pair", {})
    if pi.get("available"):
        bt = pi["block_test"]
        p(f"\n--- Table S1.7b engine x language tested within the pair (reference {pi['reference_engine']}) ---")
        p(f"    {pi['n_pairs']} pairs, {pi['n_day_clusters']} day x {pi['n_pair_clusters']} pair clusters, df={pi['df']}")
        p(f"    block F({bt['df_num']}, {bt['df_den']}) = {bt['wald_F']:.2f}, p = {bt['p_wald_F']:.3g}"
          f"{'  WALD_ANTICONSERVATIVE' if bt['anticonservative_flag'] else ''}")
        p(f"{'term':<44}{'est (pp)':>10}{'95% CI (pp)':>24}{'p':>11}")
        for t in pi["terms"]:
            p(f"{t['term']:<44}{t['estimate_pp']:>10.3f}"
              f"   [{t['ci_low_pp']:>7.3f}, {t['ci_high_pp']:>7.3f}]{t['p']:>11.3g}")

    p("\n--- Table S1.8 robustness ---")
    p(f"{'cut':<56}{'coefficient':<40}{'n':>8}{'OR [95% CI]':>28}{'p':>11}")
    for r in R["robustness"]["rows"]:
        if r.get("flag") in ("NOT_IDENTIFIED", "FAILED"):
            p(f"{r['cut']:<56}{r.get('coefficient','-'):<40}{r.get('n_obs',0):>8}{r['flag']:>28}{'-':>11}")
            continue
        p(f"{r['cut']:<56}{r['coefficient']:<40}{r['n_obs']:>8}{fmt_or(r):>28}{r['p']:>11.3g}")

    p("\n--- Table S1.9 Benjamini-Hochberg ---")
    for fam, d in R["multiplicity"].items():
        p(f"  family '{fam}': m={d['m_tests']} tests, FDR alpha={d['alpha_fdr']}, "
          f"{d['n_survive']} survive")
        for t in d["tests"][:40]:
            p(f"    {t['test_id']:<52} p={t['p_raw']:.3g}  p_BH={t['p_bh']:.3g}  "
              f"{'SURVIVES' if t['survives_bh'] else 'no'}")
    p("=" * 96)


if __name__ == "__main__":
    main()
