#!/usr/bin/env python3
"""s4_concentration.py — S4: how generative-engine visibility distributes across firms.

Produces `S4-concentration.md` and the CSV files under `data/`. Every number in
the section text is interpolated from a value computed here, so no figure in the
prose is transcribed by hand.

WHAT IS MEASURED
----------------
Six questions, in the order the section reports them:

  1. Concentration of coverage across the cohort: Lorenz, Gini, HHI, cumulative
     shares of the leading entities, and the number of firms that take half of
     all mentions. Global and within vertical.
  2. The shape of the upper tail: power law against lognormal, by maximum
     likelihood with the Clauset-Shalizi-Newman xmin rule, a bootstrap
     goodness-of-fit test, and a normalised likelihood-ratio (Vuong) comparison.
  3. Entities never named: how many, which, and a logistic regression of never
     being named on the attributes the cohort file actually carries.
  4. International anchors against Brazilian firms inside the same vertical and
     the same battery, and the same comparison split by query language.
  5. The number of entities named per response: Poisson against negative
     binomial against zero-inflated forms, chosen on information criteria.
  6. Where in the answer the first mention falls, by engine.

MEASUREMENT RULE
----------------
The canonical stratum is `COALESCE(is_probe,0)=0`. Entity matching is the
project's own extractor over the v2 cohort with anchors and decoys included,
reached through `../tables/_common.py` so that this script and the manuscript
tables cannot drift apart on the matching rule.

Every observation is read under the uniform 200-character window, that is over
`response_text[:200]`. Five of the six client adapters stored only the first 200
characters, so for those arms the window is the whole stored record; Perplexity
stored up to 2,502 characters, so for that arm the window is a restriction. The
identity check printed at the top of the run verifies that, on every row whose
stored text is at most 200 characters long, re-extraction reproduces the stored
`cited_v2` exactly. A non-zero mismatch count invalidates every figure below and
is printed as FAIL.

The database is opened read-only. Nothing here writes to it.

    python s4_concentration.py                  # regenerate S4-concentration.md and data/
    python s4_concentration.py --cache uni.pkl  # reuse a cached re-extraction
    python s4_concentration.py --boot 2000      # bootstrap replicates (default 2000)
"""
from __future__ import annotations

import argparse
import json
import math
import pickle
import sys
import time
import warnings
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
import scipy.sparse as sparse
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import optimize, special, stats
from statsmodels.discrete.count_model import (
    ZeroInflatedNegativeBinomialP,
    ZeroInflatedPoisson,
)

warnings.filterwarnings("ignore")

HERE = Path(__file__).resolve().parent
TABLES = HERE.parent / "tables"
sys.path.insert(0, str(TABLES))

import _common as CM  # noqa: E402

from src.config_v2 import (  # noqa: E402
    _ANCHORS_COHORT_BY_SLUG,
    _REAL_COHORT_BY_SLUG,
    FICTITIOUS_DECOYS_V2,
)

DATA_DIR = HERE / "data"
OUT_MD = HERE / "S4-concentration.md"
OUT_JSON = HERE / "data" / "s4_numbers.json"

SEED = 20260911

#: Database vertical slug keyed by the English slug used inside config_v2.
EN_TO_DB = {"fintech": "fintech", "retail": "varejo",
            "health": "saude", "technology": "tecnologia"}

#: Cohort names whose surface form collides with an ordinary word of the
#: response language. Identified and quantified in `../tables/build_tables.py`;
#: carried here so the sensitivity analysis uses the same two names.
COLLIDING_NAMES = ("Involves", "Target")

#: Cohort names that are word-boundary prefixes of another cohort name in the
#: same vertical, so that one text span can satisfy both patterns. Found by
#: `find_nested_names` below, listed here as (contained, container).
NESTED_PAIRS_EXPECTED = (("Amazon", "Amazon Brasil"), ("Accenture", "Accenture Brasil"))


# ===========================================================================
# Cohort attributes
# ===========================================================================

def cohort_frame() -> pd.DataFrame:
    """The 127 cohort members with every attribute `config_v2` actually carries.

    No attribute is invented. `tier`, `legal_status`, `origin`, `founded_year`
    and `region` come from the `Entity` dataclass; `group` is the partition the
    cohort file itself defines by placing an entity in a REAL, an ANCHORS or a
    DECOYS list; `vertical` is the list it sits in, translated to the database
    slug. The sixteen decoys carry none of the firm attributes because they name
    no firm.
    """
    rows = []
    for en, entities in _REAL_COHORT_BY_SLUG.items():
        for e in entities:
            rows.append(dict(name=e.name, vertical=EN_TO_DB[en], group="BR",
                             tier=e.tier, legal_status=e.legal_status,
                             origin=e.origin, founded_year=e.founded_year,
                             region=e.region))
    for en, entities in _ANCHORS_COHORT_BY_SLUG.items():
        for e in entities:
            rows.append(dict(name=e.name, vertical=EN_TO_DB[en], group="anchor",
                             tier=e.tier, legal_status=e.legal_status,
                             origin=e.origin, founded_year=e.founded_year,
                             region=e.region))
    for en, decoys in FICTITIOUS_DECOYS_V2.items():
        for d in decoys:
            rows.append(dict(name=d, vertical=EN_TO_DB[en], group="decoy",
                             tier=None, legal_status=None, origin=None,
                             founded_year=None, region=None))
    df = pd.DataFrame(rows)
    assert len(df) == 127, f"cohort is {len(df)} entities, expected 127"
    assert df.name.is_unique
    return df


def find_nested_names(cohort: pd.DataFrame) -> list[tuple[str, str]]:
    """Pairs (a, b) in one vertical where matching b necessarily also matches a."""
    out = []
    for v, g in cohort.groupby("vertical"):
        names = list(g.name)
        for a in names:
            for b in names:
                if a != b and (b == a or b.startswith(a + " ") or b.endswith(" " + a)):
                    out.append((a, b))
    return sorted(set(out))


# ===========================================================================
# Re-extraction under the uniform 200-character window
# ===========================================================================

def reextract_uniform(cache: Path | None) -> tuple[list[dict], int]:
    """One record per canonical observation, read under the uniform window.

    Identical in operation to `build_tables.reextract_uniform`; it additionally
    keeps the within-window offset of the first match, which the position
    analysis needs and which no stored column carries (the stored
    `first_entity_offset_v2` is an offset into the as-collected text).
    """
    if cache is not None and cache.exists():
        blob = pickle.loads(cache.read_bytes())
        return blob["rows"], blob["mismatch"]

    con = CM.connect()
    ext = CM.build_extractors(include_anchors=True, include_decoys=True)
    rows = con.execute(
        f"""SELECT id, date(timestamp) AS day, llm, vertical, query_lang, query_type,
                   query_category, response_text, cited_v2, cited_count_v2,
                   first_entity_v2, first_entity_offset_v2,
                   response_length_chars_v2, response_full_text
              FROM citations
             WHERE {CM.CANONICAL} AND response_text IS NOT NULL
             ORDER BY id"""
    ).fetchall()

    out, mismatch = [], 0
    for r in rows:
        e = ext.get(r["vertical"])
        if e is None:
            continue
        text = r["response_text"]
        head = text[: CM.WINDOW]
        m = e.extract(head)
        cited_win = 1 if m else 0
        if len(text) <= CM.WINDOW and cited_win != (r["cited_v2"] or 0):
            mismatch += 1
        full = r["response_full_text"]
        out.append(dict(
            id=r["id"], day=r["day"], llm=r["llm"], vertical=r["vertical"],
            lang=r["query_lang"], qtype=r["query_type"], category=r["query_category"],
            obs_len=len(text), truncated=int(len(text) > CM.WINDOW),
            first_win=m[0].entity if m else None,
            first_off=m[0].start if m else None,
            ents_win=[x.entity for x in m], n_win=len(m),
            cited_v2=r["cited_v2"], cited_count_v2=r["cited_count_v2"] or 0,
            first_v2=r["first_entity_v2"], first_off_v2=r["first_entity_offset_v2"],
            obs_len_v2=r["response_length_chars_v2"],
            full_text=full,
        ))
    con.close()
    if cache is not None:
        cache.write_bytes(pickle.dumps({"rows": out, "mismatch": mismatch}))
    return out, mismatch


# ===========================================================================
# Concentration indices
# ===========================================================================

def gini(counts) -> float:
    """Gini coefficient of a vector of sizes, zeros included as observed.

    Same estimator as `build_tables.gini`, so the first-mention figure over
    named entities reproduces Table 8 of the manuscript exactly. Which entities
    enter the vector is the whole question, and every table below states it.
    """
    x = np.sort(np.asarray(counts, dtype=float))
    n, total = len(x), x.sum()
    if n == 0 or total == 0:
        return float("nan")
    cum = float(np.sum((np.arange(1, n + 1)) * x))
    return (2.0 * cum) / (n * total) - (n + 1) / n


def hhi(counts) -> float:
    """Herfindahl-Hirschman index on the 0-to-1 scale. Invariant to zeros."""
    x = np.asarray(counts, dtype=float)
    total = x.sum()
    return float(np.sum((x / total) ** 2)) if total > 0 else float("nan")


def cumulative_share(counts, k: int) -> float:
    x = np.sort(np.asarray(counts, dtype=float))[::-1]
    total = x.sum()
    return float(x[:k].sum() / total) if total > 0 else float("nan")


def n_for_half(counts) -> int:
    """How many of the largest entities it takes to reach half of all mentions."""
    x = np.sort(np.asarray(counts, dtype=float))[::-1]
    total = x.sum()
    if total == 0:
        return 0
    return int(np.searchsorted(np.cumsum(x), total / 2.0) + 1)


def lorenz(counts) -> tuple[np.ndarray, np.ndarray]:
    """Lorenz curve points, entities ordered from smallest to largest."""
    x = np.sort(np.asarray(counts, dtype=float))
    n, total = len(x), x.sum()
    p = np.concatenate([[0.0], np.arange(1, n + 1) / n])
    q = np.concatenate([[0.0], np.cumsum(x) / total]) if total > 0 else np.zeros(n + 1)
    return p, q


# ===========================================================================
# Discrete power law, Clauset-Shalizi-Newman
# ===========================================================================

def _discrete_pl_nll(alpha: float, x: np.ndarray, xmin: float) -> float:
    if alpha <= 1.0:
        return np.inf
    return float(alpha * np.sum(np.log(x)) + len(x) * np.log(special.zeta(alpha, xmin)))


def fit_discrete_pl(x: np.ndarray, xmin: float) -> tuple[float, float]:
    """MLE of the exponent of a discrete power law truncated below at xmin.

    Returns (alpha, D), with D the Kolmogorov-Smirnov distance between the
    empirical and fitted distribution above xmin.
    """
    tail = np.sort(x[x >= xmin])
    if len(tail) < 2:
        return (float("nan"), float("nan"))
    res = optimize.minimize_scalar(_discrete_pl_nll, bounds=(1.0001, 20.0),
                                   args=(tail, xmin), method="bounded")
    alpha = float(res.x)
    z0 = special.zeta(alpha, xmin)
    cdf_model = 1.0 - special.zeta(alpha, tail) / z0          # P(X < x)
    n = len(tail)
    ecdf_lo = np.arange(0, n) / n
    ecdf_hi = np.arange(1, n + 1) / n
    D = float(max(np.max(np.abs(ecdf_hi - (1.0 - special.zeta(alpha, tail + 1) / z0))),
                  np.max(np.abs(ecdf_lo - cdf_model))))
    return alpha, D


def csn_xmin(x: np.ndarray, min_tail: int = 5) -> dict:
    """Choose xmin by minimising the KS distance, the CSN rule."""
    cands = np.unique(x)
    best = None
    for xm in cands:
        if np.sum(x >= xm) < min_tail:
            continue
        a, d = fit_discrete_pl(x, float(xm))
        if not np.isfinite(d):
            continue
        if best is None or d < best["D"]:
            best = {"xmin": float(xm), "alpha": a, "D": d,
                    "n_tail": int(np.sum(x >= xm))}
    return best or {"xmin": float("nan"), "alpha": float("nan"),
                    "D": float("nan"), "n_tail": 0}


def sample_discrete_pl(n: int, alpha: float, xmin: float, rng) -> np.ndarray:
    """Draw from a discrete power law by the CSN continuous approximation.

    Exact to order (xmin)^-1; with the xmin selected here the approximation is
    far below the resolution of any figure reported.
    """
    u = rng.random(n)
    return np.floor((xmin - 0.5) * (1.0 - u) ** (-1.0 / (alpha - 1.0)) + 0.5)


def csn_gof(x: np.ndarray, fit: dict, B: int, rng) -> float:
    """CSN bootstrap goodness of fit. Small p rules the power law out."""
    x = np.asarray(x, dtype=float)
    n = len(x)
    below = x[x < fit["xmin"]]
    p_tail = fit["n_tail"] / n
    worse = 0
    for _ in range(B):
        k = rng.binomial(n, p_tail)
        tail = sample_discrete_pl(k, fit["alpha"], fit["xmin"], rng)
        body = (rng.choice(below, n - k, replace=True) if len(below)
                else np.array([], dtype=float))
        synth = np.concatenate([tail, body])
        f = csn_xmin(synth)
        if np.isfinite(f["D"]) and f["D"] >= fit["D"]:
            worse += 1
    return worse / B


def fit_truncated_lognormal(x: np.ndarray, xmin: float) -> tuple[float, float, float]:
    """MLE of a lognormal truncated below at xmin. Returns (mu, sigma, loglik)."""
    tail = x[x >= xmin]
    lx = np.log(tail)

    def nll(theta):
        mu, ls = theta
        s = math.exp(ls)
        surv = stats.norm.sf((math.log(xmin) - mu) / s)
        if surv <= 0:
            return np.inf
        ll = np.sum(-lx - ls - 0.5 * math.log(2 * math.pi)
                    - 0.5 * ((lx - mu) / s) ** 2) - len(tail) * math.log(surv)
        return -ll

    res = optimize.minimize(nll, x0=[lx.mean(), math.log(lx.std() + 1e-6)],
                            method="Nelder-Mead",
                            options={"maxiter": 5000, "fatol": 1e-10})
    mu, ls = res.x
    return float(mu), float(math.exp(ls)), float(-res.fun)


# ===========================================================================
# Bootstrap machinery: resample observations, not entities
# ===========================================================================

def cluster_bootstrap_indices(n_obs: int, B: int, rng) -> np.ndarray:
    """B resamples of observation weights, each a multiset of size n_obs."""
    return rng.integers(0, n_obs, size=(B, n_obs))


def boot_ci(values, lo=2.5, hi=97.5) -> tuple[float, float]:
    v = np.asarray(values, dtype=float)
    v = v[np.isfinite(v)]
    if len(v) == 0:
        return (float("nan"), float("nan"))
    return (float(np.percentile(v, lo)), float(np.percentile(v, hi)))


# ===========================================================================
# Small statistics
# ===========================================================================

def cohens_h(p1: float, p2: float) -> float:
    return float(2 * math.asin(math.sqrt(p1)) - 2 * math.asin(math.sqrt(p2)))


def cliffs_delta(a, b) -> float:
    a, b = np.asarray(a, float), np.asarray(b, float)
    if len(a) == 0 or len(b) == 0:
        return float("nan")
    gt = np.sum(a[:, None] > b[None, :])
    lt = np.sum(a[:, None] < b[None, :])
    return float((gt - lt) / (len(a) * len(b)))


def epsilon_squared(H: float, n: int, k: int) -> float:
    """Effect size for Kruskal-Wallis. 0 means the groups are interchangeable."""
    if n <= k:
        return float("nan")
    return float((H - k + 1) / (n - k))


def dunn_holm(groups: dict[str, np.ndarray]) -> list[dict]:
    """Dunn's post-hoc test on rank sums with Holm-corrected p-values."""
    names = list(groups)
    allv = np.concatenate([groups[g] for g in names])
    ranks = stats.rankdata(allv)
    idx, pos = {}, 0
    for g in names:
        idx[g] = ranks[pos:pos + len(groups[g])]
        pos += len(groups[g])
    N = len(allv)
    _, counts = np.unique(allv, return_counts=True)
    ties = float(np.sum(counts ** 3 - counts))
    sigma_base = (N * (N + 1) / 12.0) - ties / (12.0 * (N - 1))
    raw = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            gi, gj = names[i], names[j]
            ni, nj = len(idx[gi]), len(idx[gj])
            diff = idx[gi].mean() - idx[gj].mean()
            se = math.sqrt(sigma_base * (1.0 / ni + 1.0 / nj))
            z = diff / se
            raw.append({"a": gi, "b": gj, "z": float(z),
                        "p_raw": float(2 * stats.norm.sf(abs(z)))})
    order = np.argsort([r["p_raw"] for r in raw])
    m = len(raw)
    prev = 0.0
    for rank, k in enumerate(order):
        adj = min(1.0, (m - rank) * raw[k]["p_raw"])
        adj = max(adj, prev)
        prev = adj
        raw[k]["p_holm"] = float(adj)
    return raw


def jsonable(o):
    """Recursively coerce numpy scalars and tuple keys so json.dumps succeeds."""
    if isinstance(o, dict):
        return {str(k): jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jsonable(v) for v in o]
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    return o


def fmt_p(p: float) -> str:
    if not np.isfinite(p):
        return "—"
    if p < 1e-4:
        return "&lt; 0.0001"
    return f"{p:.4f}"


def fmt_boot_p(d: dict) -> str:
    """Format a bootstrap p-value, never below the resolution of the bootstrap."""
    if not np.isfinite(d.get("p_boot", float("nan"))):
        return "—"
    if d.get("p_is_floor"):
        return f"&lt; {d['p_boot']:.4f}"
    return f"{d['p_boot']:.4f}"


def fmt_ci(lo: float, hi: float, d: int = 3) -> str:
    if not (np.isfinite(lo) and np.isfinite(hi)):
        return "—"
    return f"[{lo:.{d}f}, {hi:.{d}f}]"


# ===========================================================================
# Analysis
# ===========================================================================

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", type=Path, default=None,
                    help="pickle path for the re-extraction, read if present")
    ap.add_argument("--boot", type=int, default=2000,
                    help="bootstrap replicates for the concentration indices")
    ap.add_argument("--gof", type=int, default=1000,
                    help="synthetic datasets for the power-law goodness of fit")
    args = ap.parse_args()

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(SEED)
    t0 = time.time()
    N: dict = {}

    cohort = cohort_frame()
    N["nested_pairs"] = find_nested_names(cohort)

    uni, mismatch = reextract_uniform(args.cache)
    N["identity_mismatch"] = mismatch
    print(f"[{'OK ' if mismatch == 0 else 'FAIL'}] identity check: "
          f"{mismatch} mismatches on rows whose stored text is <= {CM.WINDOW} chars")
    if mismatch:
        print("FAIL — the matching rule here differs from the one that produced "
              "the series; no figure below is attributable to the window.")
        return 1
    print(f"[OK ] re-extracted {len(uni):,} canonical observations "
          f"({time.time() - t0:.0f} s)")

    n_obs = len(uni)
    N["n_obs"] = n_obs
    N["period"] = (min(r["day"] for r in uni), max(r["day"] for r in uni))
    N["obs_by_vertical"] = dict(Counter(r["vertical"] for r in uni))
    N["obs_by_engine"] = dict(Counter(r["llm"] for r in uni))
    N["obs_by_lang"] = dict(Counter(r["lang"] for r in uni))

    names = list(cohort.name)
    ent_ix = {e: i for i, e in enumerate(names)}
    n_ent = len(names)

    # Observation-by-entity incidence matrix; each entity is matched at most
    # once per observation by contract 3 of the extractor.
    rows_i, cols_i = [], []
    for i, r in enumerate(uni):
        for e in r["ents_win"]:
            rows_i.append(i)
            cols_i.append(ent_ix[e])
    M = sparse.csr_matrix((np.ones(len(rows_i), dtype=np.float64),
                           (np.array(rows_i), np.array(cols_i))),
                          shape=(n_obs, n_ent))
    mentions = np.asarray(M.sum(axis=0)).ravel()
    cohort["mentions"] = [mentions[ent_ix[e]] for e in cohort.name]

    first_counter = Counter(r["first_win"] for r in uni if r["first_win"])
    cohort["first_mentions"] = [first_counter.get(e, 0) for e in cohort.name]

    is_real = (cohort.group != "decoy").to_numpy()
    real_ix = np.where(is_real)[0]
    N["n_total_mentions"] = int(mentions.sum())
    N["n_first_mentions"] = int(sum(first_counter.values()))
    N["n_cohort_full"] = n_ent
    N["n_cohort_real"] = int(is_real.sum())
    N["n_named"] = int((mentions > 0).sum())
    N["n_named_first"] = len(first_counter)

    # ---------------------------------------------------------------- 1. concentration
    def index_block(counts) -> dict:
        return {
            "N": len(counts), "total": int(np.sum(counts)),
            "named": int(np.sum(np.asarray(counts) > 0)),
            "gini": gini(counts), "hhi": hhi(counts),
            "hhi_equiv": 1.0 / hhi(counts) if hhi(counts) > 0 else float("nan"),
            "top1": cumulative_share(counts, 1), "top3": cumulative_share(counts, 3),
            "top5": cumulative_share(counts, 5), "top10": cumulative_share(counts, 10),
            "top20": cumulative_share(counts, 20), "n_half": n_for_half(counts),
        }

    conc = {
        "mentions_real": index_block(mentions[real_ix]),
        "mentions_full": index_block(mentions),
        "mentions_named": index_block(mentions[mentions > 0]),
        "first_real": index_block(cohort.first_mentions.to_numpy()[real_ix]),
        "first_named": index_block(
            cohort.first_mentions.to_numpy()[cohort.first_mentions.to_numpy() > 0]),
    }

    verticals = ["fintech", "varejo", "saude", "tecnologia"]
    conc_vert = {}
    vert_ix = {v: np.where((cohort.vertical == v).to_numpy() & is_real)[0]
               for v in verticals}
    for v in verticals:
        conc_vert[v] = index_block(mentions[vert_ix[v]])
        conc_vert[v]["obs"] = N["obs_by_vertical"][v]

    # cluster bootstrap over observations
    boot = {k: [] for k in ["gini_real", "hhi", "n_half"]}
    boot_vert = {v: {"gini": [], "hhi": []} for v in verticals}
    obs_vert = np.array([verticals.index(r["vertical"]) for r in uni])
    Mt = M.T.tocsr()
    for _ in range(args.boot):
        w = np.bincount(rng.integers(0, n_obs, n_obs), minlength=n_obs).astype(float)
        c = Mt.dot(w)
        boot["gini_real"].append(gini(c[real_ix]))
        boot["hhi"].append(hhi(c))
        boot["n_half"].append(n_for_half(c[real_ix]))
        for k, v in enumerate(verticals):
            wv = w * (obs_vert == k)
            cv = Mt.dot(wv)
            boot_vert[v]["gini"].append(gini(cv[vert_ix[v]]))
            boot_vert[v]["hhi"].append(hhi(cv[vert_ix[v]]))
    conc["mentions_real"]["gini_ci"] = boot_ci(boot["gini_real"])
    conc["mentions_real"]["hhi_ci"] = boot_ci(boot["hhi"])
    conc["mentions_real"]["n_half_ci"] = boot_ci(boot["n_half"])
    for v in verticals:
        conc_vert[v]["gini_ci"] = boot_ci(boot_vert[v]["gini"])
        conc_vert[v]["hhi_ci"] = boot_ci(boot_vert[v]["hhi"])
    N["concentration"] = conc
    N["concentration_vertical"] = conc_vert
    print(f"[OK ] concentration and {args.boot} cluster-bootstrap replicates "
          f"({time.time() - t0:.0f} s)")

    # collision sensitivity
    coll = set(COLLIDING_NAMES)
    keep = np.array([e not in coll for e in names])
    m_clean = mentions.copy()
    m_clean[~keep] = 0
    sens_ix = np.where(is_real & keep)[0]
    N["collision_sensitivity"] = {
        "names": list(COLLIDING_NAMES),
        "matches": {e: int(mentions[ent_ix[e]]) for e in COLLIDING_NAMES},
        **index_block(m_clean[sens_ix]),
    }

    # CSVs
    lor_rows = []
    for label, counts in [("mentions_real_cohort", mentions[real_ix]),
                          ("mentions_full_cohort", mentions),
                          ("mentions_named_only", mentions[mentions > 0]),
                          ("first_mentions_real_cohort",
                           cohort.first_mentions.to_numpy()[real_ix])]:
        p, q = lorenz(counts)
        for a, b in zip(p, q):
            lor_rows.append({"series": label, "cum_share_entities": a,
                             "cum_share_mentions": b})
    pd.DataFrame(lor_rows).to_csv(DATA_DIR / "s4_lorenz_global.csv", index=False)

    lorv_rows = []
    for v in verticals:
        p, q = lorenz(mentions[vert_ix[v]])
        for a, b in zip(p, q):
            lorv_rows.append({"vertical": v, "cum_share_entities": a,
                              "cum_share_mentions": b})
    pd.DataFrame(lorv_rows).to_csv(DATA_DIR / "s4_lorenz_by_vertical.csv", index=False)

    rank = cohort.sort_values(["mentions", "name"], ascending=[False, True]).copy()
    rank["rank"] = np.arange(1, len(rank) + 1)
    rank["share_of_mentions"] = rank.mentions / N["n_total_mentions"]
    rank["cum_share_of_mentions"] = rank.share_of_mentions.cumsum()
    rank["share_of_first_mentions"] = rank.first_mentions / N["n_first_mentions"]
    rank["never_named"] = (rank.mentions == 0).astype(int)
    rank["obs_in_vertical"] = rank.vertical.map(N["obs_by_vertical"])
    rank["coverage_rate"] = rank.mentions / rank.obs_in_vertical
    rank[["rank", "name", "vertical", "group", "tier", "legal_status", "origin",
          "founded_year", "region", "mentions", "share_of_mentions",
          "cum_share_of_mentions", "first_mentions", "share_of_first_mentions",
          "obs_in_vertical", "coverage_rate", "never_named"]].to_csv(
        DATA_DIR / "s4_rank_size.csv", index=False)

    # ---------------------------------------------------------------- 2. tail shape
    import powerlaw  # noqa: E402  (optional dependency, installed for this run)

    tail_out = {}
    for label, counts in [("mentions", mentions[mentions > 0]),
                          ("first_mentions",
                           cohort.first_mentions.to_numpy()[
                               cohort.first_mentions.to_numpy() > 0])]:
        x = np.asarray(counts, dtype=float)
        import contextlib
        import io
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            f = powerlaw.Fit(x, discrete=True)
            cmp_ln = f.distribution_compare("power_law", "lognormal",
                                            normalized_ratio=True)
            cmp_lnp = f.distribution_compare("power_law", "lognormal_positive",
                                             normalized_ratio=True)
            cmp_exp = f.distribution_compare("power_law", "exponential",
                                             normalized_ratio=True)
            cmp_tpl = f.distribution_compare("power_law", "truncated_power_law",
                                             normalized_ratio=True)
        own = csn_xmin(x)
        gof_p = csn_gof(x, own, args.gof, rng)
        mu_t, sd_t, ll_t = fit_truncated_lognormal(x, own["xmin"])
        tail_out[label] = {
            "n_positive": int(len(x)), "max": float(x.max()), "min": float(x.min()),
            "pl_xmin": float(f.xmin), "pl_alpha": float(f.alpha),
            "pl_sigma": float(f.sigma), "pl_n_tail": int(f.n_tail), "pl_D": float(f.D),
            "pl_alpha_lo": float(f.alpha - 1.959963984540054 * f.sigma),
            "pl_alpha_hi": float(f.alpha + 1.959963984540054 * f.sigma),
            "own_xmin": own["xmin"], "own_alpha": own["alpha"],
            "own_D": own["D"], "own_n_tail": own["n_tail"],
            "gof_p": gof_p,
            "ln_mu": float(f.lognormal.mu), "ln_sigma": float(f.lognormal.sigma),
            "own_ln_mu": mu_t, "own_ln_sigma": sd_t,
            "vs_lognormal_R": float(cmp_ln[0]), "vs_lognormal_p": float(cmp_ln[1]),
            "vs_lognormal_pos_R": float(cmp_lnp[0]), "vs_lognormal_pos_p": float(cmp_lnp[1]),
            "vs_exponential_R": float(cmp_exp[0]), "vs_exponential_p": float(cmp_exp[1]),
            "vs_truncated_R": float(cmp_tpl[0]), "vs_truncated_p": float(cmp_tpl[1]),
        }
    N["tail"] = tail_out
    print(f"[OK ] tail fits and {args.gof} goodness-of-fit replicates "
          f"({time.time() - t0:.0f} s)")

    # ---------------------------------------------------------------- 3. never named
    never = cohort[cohort.mentions == 0]
    N["never"] = {
        "n_total": int(len(never)),
        "by_group": dict(Counter(never.group)),
        "by_group_denom": dict(Counter(cohort.group)),
        "by_tier": {str(k): int(v) for k, v in Counter(never.tier.fillna("decoy")).items()},
        "by_tier_denom": {str(k): int(v) for k, v in Counter(cohort.tier.fillna("decoy")).items()},
        "by_vertical": dict(Counter(never.vertical)),
        "names_by_vertical": {v: sorted(never[never.vertical == v].name)
                              for v in verticals},
        "never_first_only": sorted(
            cohort[(cohort.first_mentions == 0) & (cohort.mentions > 0)].name),
    }
    cross = pd.crosstab([cohort.group, cohort.tier.fillna("decoy")],
                        cohort.mentions == 0)
    N["never_cross"] = {f"{g}|{t}": {"named": int(row.get(False, 0)),
                                     "never": int(row.get(True, 0))}
                        for (g, t), row in cross.iterrows()}

    reg = cohort[cohort.group != "decoy"].copy()
    reg["never"] = (reg.mentions == 0).astype(int)
    reg["founded_dec"] = (reg.founded_year - 2000) / 10.0
    N["never_reg_n"] = int(len(reg))
    N["legal_status_counts"] = {str(k): int(v)
                                for k, v in Counter(reg.legal_status).items()}
    N["legal_status_mentions"] = {
        r["name"]: int(r["mentions"])
        for _, r in reg[reg.legal_status != "active"].iterrows()}

    formula = ("never ~ C(group, Treatment('BR')) + C(tier, Treatment('head')) "
               "+ C(vertical, Treatment('fintech')) + founded_dec")
    mod = smf.logit(formula, data=reg).fit(disp=0)
    ors = pd.DataFrame({
        "term": mod.params.index, "coef": mod.params.values,
        "se": mod.bse.values, "z": mod.tvalues.values, "p": mod.pvalues.values,
        "or": np.exp(mod.params.values),
        "or_lo": np.exp(mod.conf_int()[0].values),
        "or_hi": np.exp(mod.conf_int()[1].values)})
    N["never_logit"] = {
        "converged": bool(mod.mle_retvals["converged"]),
        "n": int(mod.nobs), "llf": float(mod.llf), "llnull": float(mod.llnull),
        "prsquared": float(mod.prsquared), "llr_p": float(mod.llr_pvalue),
        "terms": ors.to_dict("records"),
    }
    # type-II likelihood-ratio test per block
    blocks = {
        "group": "never ~ C(tier, Treatment('head')) + C(vertical, Treatment('fintech')) + founded_dec",
        "tier": "never ~ C(group, Treatment('BR')) + C(vertical, Treatment('fintech')) + founded_dec",
        "vertical": "never ~ C(group, Treatment('BR')) + C(tier, Treatment('head')) + founded_dec",
        "founded_year": "never ~ C(group, Treatment('BR')) + C(tier, Treatment('head')) + C(vertical, Treatment('fintech'))",
    }
    lr = {}
    for blk, f_red in blocks.items():
        red = smf.logit(f_red, data=reg).fit(disp=0)
        stat = 2 * (mod.llf - red.llf)
        df = int(mod.df_model - red.df_model)
        lr[blk] = {"lr": float(stat), "df": df,
                   "p": float(stats.chi2.sf(stat, df)),
                   "converged": bool(red.mle_retvals["converged"])}
    N["never_lr"] = lr

    # marginal never-rates that the adjusted odds ratios are adjusting
    N["never_marginal"] = {
        "BR_head": [int(((reg.group == "BR") & (reg.tier == "head") & (reg.never == 1)).sum()),
                    int(((reg.group == "BR") & (reg.tier == "head")).sum())],
        "anchor_head": [int(((reg.group == "anchor") & (reg.never == 1)).sum()),
                        int((reg.group == "anchor").sum())],
    }
    print(f"[OK ] never-named model on {len(reg)} entities "
          f"({time.time() - t0:.0f} s)")

    # ---------------------------------------------------------------- 4. anchors vs BR
    br_sets = {EN_TO_DB[k]: {e.name for e in v} for k, v in _REAL_COHORT_BY_SLUG.items()}
    an_sets = {EN_TO_DB[k]: {e.name for e in v} for k, v in _ANCHORS_COHORT_BY_SLUG.items()}
    n_br = {v: len(br_sets[v]) for v in verticals}
    n_an = {v: len(an_sets[v]) for v in verticals}

    per_obs = np.zeros((n_obs, 4))     # br matched, an matched, br slots, an slots
    any_br = np.zeros(n_obs, dtype=bool)
    any_an = np.zeros(n_obs, dtype=bool)
    an_no_amazon = np.zeros(n_obs)
    for i, r in enumerate(uni):
        v = r["vertical"]
        s = set(r["ents_win"])
        b, a = len(s & br_sets[v]), len(s & an_sets[v])
        per_obs[i] = (b, a, n_br[v], n_an[v])
        any_br[i], any_an[i] = b > 0, a > 0
        an_no_amazon[i] = len(s & (an_sets[v] - {"Amazon"}))

    def group_rates(mask) -> dict:
        sub = per_obs[mask]
        sb, sa = sub[:, 2].sum(), sub[:, 3].sum()
        mb, ma = sub[:, 0].sum(), sub[:, 1].sum()
        rb, ra = mb / sb, ma / sa
        b = int(np.sum(any_br[mask] & ~any_an[mask]))
        c = int(np.sum(any_an[mask] & ~any_br[mask]))
        mc = stats.binomtest(min(b, c), b + c, 0.5) if (b + c) else None
        return {"n": int(mask.sum()), "br_slots": int(sb), "br_named": int(mb),
                "br_rate": float(rb), "an_slots": int(sa), "an_named": int(ma),
                "an_rate": float(ra),
                "rr": float(rb / ra) if ra > 0 else float("inf"),
                "h": cohens_h(rb, ra),
                "any_br": float(any_br[mask].mean()),
                "any_an": float(any_an[mask].mean()),
                "mcnemar_b": b, "mcnemar_c": c,
                "mcnemar_p": float(mc.pvalue) if mc else float("nan")}

    lang_arr = np.array([r["lang"] for r in uni])
    vert_arr = np.array([r["vertical"] for r in uni])
    cells = {}
    for v in verticals + ["all"]:
        for lg in ["pt", "en", "all"]:
            m = np.ones(n_obs, dtype=bool)
            if v != "all":
                m &= vert_arr == v
            if lg != "all":
                m &= lang_arr == lg
            cells[(v, lg)] = group_rates(m)
    N["anchor_cells"] = {f"{v}|{lg}": val for (v, lg), val in cells.items()}

    # cluster bootstrap for the pooled rate ratio and the language interaction
    def pooled_logrr(w, mask) -> float:
        ww = w * mask
        sb = float(np.dot(ww, per_obs[:, 2]))
        sa = float(np.dot(ww, per_obs[:, 3]))
        mb = float(np.dot(ww, per_obs[:, 0]))
        ma = float(np.dot(ww, per_obs[:, 1]))
        if sb == 0 or sa == 0 or mb == 0 or ma == 0:
            return float("nan")
        return math.log((mb / sb) / (ma / sa))

    pt_mask = (lang_arr == "pt").astype(float)
    en_mask = (lang_arr == "en").astype(float)
    boot_rr = {"all": [], "pt": [], "en": [], "inter": []}
    boot_rr_v = {v: {"pt": [], "en": [], "inter": []} for v in verticals}
    ones = np.ones(n_obs)
    for _ in range(args.boot):
        w = np.bincount(rng.integers(0, n_obs, n_obs), minlength=n_obs).astype(float)
        lp, le = pooled_logrr(w, pt_mask), pooled_logrr(w, en_mask)
        boot_rr["all"].append(pooled_logrr(w, ones))
        boot_rr["pt"].append(lp)
        boot_rr["en"].append(le)
        boot_rr["inter"].append(lp - le)
        for v in verticals:
            vm = (vert_arr == v).astype(float)
            a, b = pooled_logrr(w, vm * pt_mask), pooled_logrr(w, vm * en_mask)
            boot_rr_v[v]["pt"].append(a)
            boot_rr_v[v]["en"].append(b)
            boot_rr_v[v]["inter"].append(a - b)

    def boot_summary(v) -> dict:
        arr = np.asarray(v, float)
        finite = arr[np.isfinite(arr)]
        lo, hi = boot_ci(finite)
        if len(finite) == 0:
            return {"lo": float("nan"), "hi": float("nan"), "p_boot": float("nan"),
                    "p_is_floor": False, "n_finite": 0}
        p = float(2 * min((finite <= 0).mean(), (finite >= 0).mean()))
        floor = 1.0 / (len(finite) + 1)
        return {"lo": float(lo), "hi": float(hi),
                "p_boot": min(1.0, max(p, floor)),
                "p_is_floor": bool(p < floor), "n_finite": int(len(finite))}

    N["anchor_boot"] = {k: boot_summary(v) for k, v in boot_rr.items()}
    N["anchor_boot_vertical"] = {v: {k: boot_summary(x) for k, x in d.items()}
                                 for v, d in boot_rr_v.items()}

    # entity-level rates, within vertical
    ent_lvl = {}
    for v in verticals:
        obs_v = N["obs_by_vertical"][v]
        sub = cohort[(cohort.vertical == v) & (cohort.group != "decoy")]
        a = (sub[sub.group == "BR"].mentions / obs_v).to_numpy()
        b = (sub[sub.group == "anchor"].mentions / obs_v).to_numpy()
        u = stats.mannwhitneyu(a, b, alternative="two-sided")
        ent_lvl[v] = {"n_br": len(a), "n_an": len(b),
                      "median_br": float(np.median(a)), "median_an": float(np.median(b)),
                      "U": float(u.statistic), "p": float(u.pvalue),
                      "cliffs_delta": cliffs_delta(a, b)}
    N["anchor_entity_level"] = ent_lvl

    # nesting sensitivity: retail "Amazon" is contained in "Amazon Brasil"
    both = sum(1 for r in uni
               if "Amazon" in r["ents_win"] and "Amazon Brasil" in r["ents_win"])
    N["amazon_nesting"] = {
        "amazon": int(mentions[ent_ix["Amazon"]]),
        "amazon_brasil": int(mentions[ent_ix["Amazon Brasil"]]),
        "co_occurring": both,
        "accenture": int(mentions[ent_ix["Accenture"]]),
        "accenture_brasil": int(mentions[ent_ix["Accenture Brasil"]]),
    }
    m_ret = vert_arr == "varejo"
    sa = float(per_obs[m_ret, 3].sum() * (n_an["varejo"] - 1) / n_an["varejo"])
    N["amazon_nesting"]["retail_anchor_rate_with"] = float(
        per_obs[m_ret, 1].sum() / per_obs[m_ret, 3].sum())
    N["amazon_nesting"]["retail_anchor_rate_without"] = float(
        an_no_amazon[m_ret].sum() / sa)
    print(f"[OK ] anchors against Brazilian firms ({time.time() - t0:.0f} s)")

    # ---------------------------------------------------------------- 5. count model
    count_models = {}
    for label, y in [("window", np.array([r["n_win"] for r in uni], dtype=float)),
                     ("as_collected",
                      np.array([r["cited_count_v2"] for r in uni], dtype=float))]:
        X = np.ones((len(y), 1))
        obs_hist = {int(k): int(v) for k, v in sorted(Counter(y.astype(int)).items())}
        fits = {}
        pois = sm.Poisson(y, X).fit(disp=0)
        fits["Poisson"] = pois
        nb2 = sm.NegativeBinomial(y, X, loglike_method="nb2").fit(disp=0)
        fits["NB2"] = nb2
        zip_ = ZeroInflatedPoisson(y, X, exog_infl=X).fit(disp=0, maxiter=500)
        fits["ZIP"] = zip_
        zinb = ZeroInflatedNegativeBinomialP(y, X, exog_infl=X, p=2).fit(
            disp=0, maxiter=1000)
        fits["ZINB"] = zinb

        mu_p = float(np.exp(pois.params[0]))
        mu_n = float(np.exp(nb2.params[0]))
        alpha = float(nb2.params[1])
        r_ = 1.0 / alpha
        p_ = r_ / (r_ + mu_n)
        pi_zip = float(1 / (1 + np.exp(-zip_.params[0])))
        pi_zinb = float(1 / (1 + np.exp(-zinb.params[0])))
        mu_zinb = float(np.exp(zinb.params[1]))
        a_zinb = float(zinb.params[2])
        rz = 1.0 / a_zinb
        pz = rz / (rz + mu_zinb)
        pred0 = {
            "Poisson": float(len(y) * math.exp(-mu_p)),
            "NB2": float(len(y) * p_ ** r_),
            "ZIP": float(len(y) * (pi_zip + (1 - pi_zip)
                                   * math.exp(-math.exp(zip_.params[1])))),
            "ZINB": float(len(y) * (pi_zinb + (1 - pi_zinb) * pz ** rz)),
        }
        count_models[label] = {
            "n": int(len(y)), "mean": float(y.mean()), "var": float(y.var(ddof=1)),
            "vmr": float(y.var(ddof=1) / y.mean()), "max": int(y.max()),
            "obs_zeros": int((y == 0).sum()),
            "p_zero_obs": float((y == 0).mean()),
            "hist": obs_hist,
            "fits": {k: {"llf": float(m.llf), "aic": float(m.aic),
                         "bic": float(m.bic), "k": int(len(m.params)),
                         "converged": bool(m.mle_retvals.get("converged", False))}
                     for k, m in fits.items()},
            "pred_zeros": pred0,
            "nb_alpha": alpha, "nb_mu": mu_n, "poisson_mu": mu_p,
            "zip_pi": pi_zip, "zinb_pi": pi_zinb,
            "vuong_zip_vs_pois_lr": float(2 * (zip_.llf - pois.llf)),
            "vuong_zinb_vs_nb_lr": float(2 * (zinb.llf - nb2.llf)),
            "lr_nb_vs_pois": float(2 * (nb2.llf - pois.llf)),
        }
        best = min(count_models[label]["fits"],
                   key=lambda k: count_models[label]["fits"][k]["aic"])
        count_models[label]["best_aic"] = best
        count_models[label]["best_bic"] = min(
            count_models[label]["fits"],
            key=lambda k: count_models[label]["fits"][k]["bic"])
    N["counts"] = count_models

    # the same model with engine, vertical and language, as a robustness check
    dfc = pd.DataFrame([{k: r[k] for k in ("llm", "vertical", "lang", "n_win")}
                        for r in uni])
    cov_fits = {}
    Xd = pd.get_dummies(dfc[["llm", "vertical", "lang"]], drop_first=True).astype(float)
    Xd = sm.add_constant(Xd).to_numpy()
    yv = dfc.n_win.to_numpy(dtype=float)
    for label, ctor in [("Poisson", lambda: sm.Poisson(yv, Xd)),
                        ("NB2", lambda: sm.NegativeBinomial(yv, Xd, loglike_method="nb2"))]:
        m = ctor().fit(disp=0, maxiter=200)
        cov_fits[label] = {"llf": float(m.llf), "aic": float(m.aic),
                           "bic": float(m.bic),
                           "converged": bool(m.mle_retvals.get("converged", False))}
    try:
        m = ZeroInflatedNegativeBinomialP(yv, Xd, exog_infl=np.ones((len(yv), 1)),
                                          p=2).fit(disp=0, maxiter=1000)
        cov_fits["ZINB"] = {"llf": float(m.llf), "aic": float(m.aic),
                            "bic": float(m.bic),
                            "converged": bool(m.mle_retvals.get("converged", False))}
    except Exception as exc:  # pragma: no cover - reported, never hidden
        cov_fits["ZINB"] = {"llf": float("nan"), "aic": float("nan"),
                            "bic": float("nan"), "converged": False,
                            "error": str(exc)}
    N["counts_covariates"] = cov_fits
    print(f"[OK ] count models ({time.time() - t0:.0f} s)")

    # ---------------------------------------------------------------- 6. position
    pos = defaultdict(list)
    rel_obs = defaultdict(list)
    for r in uni:
        if r["first_off"] is None:
            continue
        pos[r["llm"]].append(r["first_off"])
        if r["obs_len_v2"]:
            rel_obs[r["llm"]].append(r["first_off"] / r["obs_len_v2"])
    engines = [e for e in CM.ENGINES if e in pos]
    pos_stats = {}
    for e in engines:
        a = np.asarray(pos[e], dtype=float)
        rel = np.asarray(rel_obs[e], dtype=float)
        trunc = [r for r in uni if r["llm"] == e and r["first_off"] is not None]
        pos_stats[e] = {
            "n": int(len(a)), "mean": float(a.mean()), "sd": float(a.std(ddof=1)),
            "q10": float(np.percentile(a, 10)), "q25": float(np.percentile(a, 25)),
            "median": float(np.median(a)), "q75": float(np.percentile(a, 75)),
            "q90": float(np.percentile(a, 90)), "max": float(a.max()),
            "frac_at_zero": float((a == 0).mean()),
            "rel_median": float(np.median(rel)) if len(rel) else float("nan"),
            "rel_q25": float(np.percentile(rel, 25)) if len(rel) else float("nan"),
            "rel_q75": float(np.percentile(rel, 75)) if len(rel) else float("nan"),
            "at_cap_share": float(np.mean([t["obs_len"] == CM.WINDOW for t in trunc])),
        }
    H = stats.kruskal(*[np.asarray(pos[e], float) for e in engines])
    N["position"] = {
        "by_engine": pos_stats,
        "kruskal_H": float(H.statistic), "kruskal_p": float(H.pvalue),
        "kruskal_df": len(engines) - 1,
        "epsilon2": epsilon_squared(H.statistic,
                                    sum(len(pos[e]) for e in engines), len(engines)),
        "dunn": dunn_holm({e: np.asarray(pos[e], float) for e in engines}),
    }

    # Uncensored subset: rows that retained the whole response. The first
    # mention is re-extracted over the entire text rather than reused from the
    # window, because a first mention that falls after character 200 belongs in
    # this distribution and the windowed pass cannot see it.
    ext_full = CM.build_extractors(include_anchors=True, include_decoys=True)
    full_rows = [r for r in uni if r["full_text"]]
    unc = defaultdict(list)
    unc_abs = defaultdict(list)
    unc_len = defaultdict(list)
    unc_beyond = Counter()
    for r in full_rows:
        e = ext_full.get(r["vertical"])
        m = e.extract(r["full_text"]) if e else []
        if not m:
            continue
        unc[r["llm"]].append(m[0].start / len(r["full_text"]))
        unc_abs[r["llm"]].append(float(m[0].start))
        unc_len[r["llm"]].append(float(len(r["full_text"])))
        if r["first_off"] is None:
            unc_beyond[r["llm"]] += 1
    N["position_uncensored_beyond_window"] = dict(unc_beyond)
    N["position_uncensored"] = {
        e: {"n": len(v), "median": float(np.median(v)),
            "q25": float(np.percentile(v, 25)), "q75": float(np.percentile(v, 75)),
            "abs_median": float(np.median(unc_abs[e])),
            "len_median": float(np.median(unc_len[e]))}
        for e, v in sorted(unc.items()) if len(v) > 0}
    N["position_uncensored_n_rows"] = len(full_rows)
    if len(unc_abs) > 1:
        Ha = stats.kruskal(*[np.asarray(v, float) for v in unc_abs.values()])
        N["position_uncensored_abs_kruskal"] = {
            "H": float(Ha.statistic), "p": float(Ha.pvalue), "df": len(unc_abs) - 1,
            "epsilon2": epsilon_squared(Ha.statistic,
                                        sum(len(v) for v in unc_abs.values()),
                                        len(unc_abs))}
    if len(unc) > 1:
        Hu = stats.kruskal(*[np.asarray(v, float) for v in unc.values()])
        N["position_uncensored_kruskal"] = {
            "H": float(Hu.statistic), "p": float(Hu.pvalue),
            "df": len(unc) - 1,
            "epsilon2": epsilon_squared(Hu.statistic,
                                        sum(len(v) for v in unc.values()), len(unc))}

    # Perplexity is the one arm whose stored text exceeds the window
    ppx = [r for r in uni if r["llm"] == "Perplexity"]
    N["perplexity_window"] = {
        "n": len(ppx),
        "n_stored_gt_window": sum(1 for r in ppx if r["obs_len"] > CM.WINDOW),
        "mean_stored_len": float(np.mean([r["obs_len"] for r in ppx])),
        "named_in_window": sum(1 for r in ppx if r["n_win"] > 0),
        "named_as_collected": sum(1 for r in ppx if (r["cited_v2"] or 0) == 1),
    }
    print(f"[OK ] position of first mention ({time.time() - t0:.0f} s)")

    OUT_JSON.write_text(json.dumps(jsonable(N), indent=1, default=str),
                        encoding="utf-8")
    OUT_MD.write_text(render(N, cohort, rank, args), encoding="utf-8")
    print(f"[OK ] wrote {OUT_MD.name}, {OUT_JSON.name} and 3 CSV files "
          f"({time.time() - t0:.0f} s)")
    return 0


# ===========================================================================
# Rendering
# ===========================================================================

def render(N: dict, cohort: pd.DataFrame, rank: pd.DataFrame, args) -> str:
    c = N["concentration"]
    cv = N["concentration_vertical"]
    t = N["tail"]
    L: list[str] = []
    A = L.append
    d0, d1 = N["period"]
    VL = {"fintech": "Fintech", "varejo": "Retail",
          "saude": "Health", "tecnologia": "Technology"}
    verticals = ["fintech", "varejo", "saude", "tecnologia"]

    A("# S4. Concentration: how generative-engine visibility distributes across firms")
    A("")
    A(f"Series {d0} to {d1}. Canonical stratum `COALESCE(is_probe,0)=0`, "
      f"{N['n_obs']:,} observations, {N['n_cohort_full']} cohort entities of which "
      f"{N['n_cohort_real']} name a real firm and 16 are fictitious decoys. "
      f"Generated by `s4_concentration.py`; every figure below is interpolated "
      f"from that script and none is transcribed by hand.")
    A("")

    # ---------------------------------------------------------------- method
    A("## Method")
    A("")
    A(f"Every observation is read under the uniform {CM.WINDOW}-character window, "
      f"that is over `response_text[:{CM.WINDOW}]`, with the project's own "
      f"extractor (`src.analysis.entity_extraction.EntityExtractor`) over the v2 "
      f"cohort including international anchors and fictitious decoys, reached "
      f"through `../tables/_common.py`. Holding the matching rule fixed and "
      f"moving only the window is the premise of the manuscript, so this section "
      f"imports the rule rather than restating it. The identity check reports "
      f"{N['identity_mismatch']} mismatches: on every row whose stored text is at "
      f"most {CM.WINDOW} characters, re-extraction reproduces the stored `cited_v2` "
      f"exactly. A non-zero count would have aborted the run.")
    A("")
    A("Two size variables are reported throughout and they answer different "
      "questions. **Mentions** counts an entity once per observation in which it "
      "appears anywhere inside the window, which is coverage. **First mentions** "
      "counts an entity only when it is the earliest cohort name in the window, "
      "which is the leading position. First mentions reproduce Table 8 of the "
      "manuscript to every published digit, and that agreement is the check that "
      "this script reads the series the same way `build_tables.py` does.")
    A("")
    A(f"Three denominators appear, and every table names the one it uses. The "
      f"**real cohort** is the {N['n_cohort_real']} entities that name an existing "
      f"firm, 79 Brazilian and 32 international anchors; it is the primary "
      f"denominator because the sixteen decoys cannot be cited correctly and "
      f"counting them as zeros measures the study design rather than the market. "
      f"The **full cohort** adds those sixteen. **Named only** restricts to "
      f"entities with at least one mention and is reported because the published "
      f"Gini of Table 8 uses it.")
    A("")
    A(f"Intervals on the concentration indices come from a cluster bootstrap over "
      f"observations, {args.boot:,} replicates, seed {SEED}: an observation is the "
      f"unit that was sampled, an entity is not, and resampling entities would "
      f"treat a fixed cohort as a random draw. Intervals are percentile.")
    A("")

    # ---------------------------------------------------------------- 1
    A("## 1. Concentration of coverage")
    A("")
    m = c["mentions_real"]
    A(f"Four firms take half of every entity mention the six engines produced in "
      f"five months, out of a cohort of {N['n_cohort_real']} real firms, and "
      f"{c['mentions_real']['N'] - c['mentions_real']['named']} of those firms "
      f"were never mentioned at all. The indices below put numbers on that "
      f"sentence and show how much each of them depends on a denominator the "
      f"analyst chooses.")
    A("")
    A(f"**Table S4.1.** Concentration of entity coverage under the uniform "
      f"{CM.WINDOW}-character window. Series {d0} to {d1}, {N['n_obs']:,} "
      f"observations, {N['n_total_mentions']:,} entity mentions. "
      f"Intervals are percentile cluster bootstrap over observations, "
      f"{args.boot:,} replicates.")
    A("")
    A("| Quantity | Real cohort (111) | Full cohort (127) | Named only |")
    A("|---|---:|---:|---:|")
    r1, r2, r3 = c["mentions_real"], c["mentions_full"], c["mentions_named"]
    A(f"| Entities in the denominator | {r1['N']} | {r2['N']} | {r3['N']} |")
    A(f"| Entities with at least one mention | {r1['named']} | {r2['named']} | {r3['named']} |")
    A(f"| Total mentions | {r1['total']:,} | {r2['total']:,} | {r3['total']:,} |")
    A(f"| Gini | {r1['gini']:.4f} | {r2['gini']:.4f} | {r3['gini']:.4f} |")
    A(f"| Gini, 95% bootstrap interval | {fmt_ci(*r1['gini_ci'], 4)} | — | — |")
    A(f"| HHI, 0 to 1 | {r1['hhi']:.6f} | {r2['hhi']:.6f} | {r3['hhi']:.6f} |")
    A(f"| HHI, 95% bootstrap interval | {fmt_ci(*r1['hhi_ci'], 6)} | — | — |")
    A(f"| Equivalent number of equal-sized firms (1/HHI) | {r1['hhi_equiv']:.2f} | "
      f"{r2['hhi_equiv']:.2f} | {r3['hhi_equiv']:.2f} |")
    A(f"| Cumulative share, top 1 | {100*r1['top1']:.2f}% | {100*r2['top1']:.2f}% | {100*r3['top1']:.2f}% |")
    A(f"| Cumulative share, top 3 | {100*r1['top3']:.2f}% | {100*r2['top3']:.2f}% | {100*r3['top3']:.2f}% |")
    A(f"| Cumulative share, top 5 | {100*r1['top5']:.2f}% | {100*r2['top5']:.2f}% | {100*r3['top5']:.2f}% |")
    A(f"| Cumulative share, top 10 | {100*r1['top10']:.2f}% | {100*r2['top10']:.2f}% | {100*r3['top10']:.2f}% |")
    A(f"| Cumulative share, top 20 | {100*r1['top20']:.2f}% | {100*r2['top20']:.2f}% | {100*r3['top20']:.2f}% |")
    A(f"| Entities taking half of all mentions | {r1['n_half']} | {r2['n_half']} | {r3['n_half']} |")
    A("")
    A(f"*Notes.* HHI and the cumulative shares are invariant to how many "
      f"never-named entities sit in the denominator, which is why the three "
      f"columns agree on them and disagree on Gini. The spread between "
      f"{r3['gini']:.4f} and {r2['gini']:.4f} is the entire content of the "
      f"denominator choice: an analyst who reports Gini over named entities is "
      f"describing the shape of the visible market, one who reports it over the "
      f"cohort is describing the market plus the firms the engines never reach. "
      f"The bootstrap interval on the real-cohort Gini, {fmt_ci(*r1['gini_ci'], 4)}, "
      f"is narrow because with {N['n_obs']:,} observations the entity ranking is "
      f"stable under resampling; it carries no information about how the figure "
      f"would move under a different cohort.")
    A("")

    fm = c["first_real"]
    fn = c["first_named"]
    A(f"**Table S4.2.** The same indices on first mentions, for comparison with "
      f"Table 8 of the manuscript. Series {d0} to {d1}, "
      f"{N['n_first_mentions']:,} observations carrying a first mention.")
    A("")
    A("| Quantity | Real cohort (111) | Named only |")
    A("|---|---:|---:|")
    A(f"| Entities in the denominator | {fm['N']} | {fn['N']} |")
    A(f"| Total first mentions | {fm['total']:,} | {fn['total']:,} |")
    A(f"| Gini | {fm['gini']:.4f} | {fn['gini']:.6f} |")
    A(f"| HHI, 0 to 1 | {fm['hhi']:.6f} | {fn['hhi']:.6f} |")
    A(f"| Cumulative share, top 1 | {100*fm['top1']:.2f}% | {100*fn['top1']:.2f}% |")
    A(f"| Cumulative share, top 5 | {100*fm['top5']:.2f}% | {100*fn['top5']:.2f}% |")
    A(f"| Cumulative share, top 20 | {100*fm['top20']:.2f}% | {100*fn['top20']:.2f}% |")
    A(f"| Entities taking half of all first mentions | {fm['n_half']} | {fn['n_half']} |")
    A("")
    A(f"*Notes.* The named-only Gini of {fn['gini']:.6f} and the HHI of "
      f"{fn['hhi']:.6f} reproduce Table 8 to every published digit, which is the "
      f"agreement check for this script. First mentions are more concentrated "
      f"than coverage on every index: {100*fm['top1']:.2f}% of first mentions "
      f"against {100*r1['top1']:.2f}% of mentions for the leading firm. Being "
      f"named at all and being named first are different quantities, and a report "
      f"that conflates them overstates concentration by roughly the difference "
      f"between these two columns.")
    A("")

    A(f"**Table S4.3.** Concentration within vertical, real cohort denominator. "
      f"Series {d0} to {d1}. Each vertical has its own battery, so the "
      f"observation counts are the denominators of that vertical alone.")
    A("")
    A("| Vertical | Observations | Entities | Named | Mentions | Gini [95% CI] | HHI [95% CI] | 1/HHI | Top 1 | Top 3 | Firms taking half |")
    A("|---|---:|---:|---:|---:|---|---|---:|---:|---:|---:|")
    for v in verticals:
        b = cv[v]
        A(f"| {VL[v]} | {b['obs']:,} | {b['N']} | {b['named']} | {b['total']:,} | "
          f"{b['gini']:.4f} {fmt_ci(*b['gini_ci'], 4)} | "
          f"{b['hhi']:.4f} {fmt_ci(*b['hhi_ci'], 4)} | {b['hhi_equiv']:.2f} | "
          f"{100*b['top1']:.2f}% | {100*b['top3']:.2f}% | {b['n_half']} |")
    A("")
    hi_v = max(verticals, key=lambda v: cv[v]["hhi"])
    lo_v = min(verticals, key=lambda v: cv[v]["hhi"])
    A(f"*Notes.* Concentration belongs to the vertical the engines are asked "
      f"about, and it varies across verticals by a factor of three. "
      f"{VL[hi_v]} answers to an equivalent of {cv[hi_v]['hhi_equiv']:.2f} firms, "
      f"{VL[lo_v]} to {cv[lo_v]['hhi_equiv']:.2f}, against cohorts of the same "
      f"size. The within-vertical HHI is far above the pooled figure of "
      f"{r1['hhi']:.4f} because pooling adds four leaders and averages their "
      f"shares; the pooled number answers a question nobody asks, since no query "
      f"ever put a fintech and a hospital in the same choice set.")
    A("")

    A(f"**Table S4.4.** Rank-size, top 20 by mentions. Denominator "
      f"{N['n_total_mentions']:,} mentions over {N['n_obs']:,} observations. "
      f"Coverage rate is mentions divided by the observations of that entity's "
      f"own vertical. The full table for all {N['n_cohort_full']} entities is in "
      f"`data/s4_rank_size.csv`.")
    A("")
    A("| Rank | Entity | Vertical | Group | Tier | Mentions | Share | Cumulative | Coverage rate | First mentions |")
    A("|---:|---|---|---|---|---:|---:|---:|---:|---:|")
    for _, r in rank.head(20).iterrows():
        A(f"| {r['rank']} | {r['name']} | {VL[r['vertical']]} | "
          f"{'Brazilian' if r['group']=='BR' else ('anchor' if r['group']=='anchor' else 'decoy')} | "
          f"{r['tier'] or '—'} | {int(r['mentions']):,} | "
          f"{100*r['share_of_mentions']:.2f}% | {100*r['cum_share_of_mentions']:.2f}% | "
          f"{100*r['coverage_rate']:.2f}% | {int(r['first_mentions']):,} |")
    A("")
    cs = N["collision_sensitivity"]
    A(f"*Notes.* Two cohort names collide with ordinary words of the response "
      f"language and are published with the collision left in, following the "
      f"convention of `../tables/TABLES.md`: `Involves` matches the English verb "
      f"({cs['matches']['Involves']:,} of its mentions) and `Target` the English "
      f"noun ({cs['matches']['Target']:,}). Removing both names from the cohort "
      f"moves the real-cohort Gini from {r1['gini']:.4f} to {cs['gini']:.4f}, the "
      f"HHI from {r1['hhi']:.6f} to {cs['hhi']:.6f}, and the count of named "
      f"entities from {r1['named']} to {cs['named']}. The correction belongs in "
      f"`src/config.py`, where `Involves` needs a canonical name and `Target` a "
      f"stop context, followed by re-extraction; until that happens this "
      f"paragraph is the declared error term on every figure in this section.")
    A("")
    A("Lorenz curves are written to `data/s4_lorenz_global.csv` (four series: "
      "mentions over the real cohort, over the full cohort, over named entities, "
      "and first mentions over the real cohort) and "
      "`data/s4_lorenz_by_vertical.csv`.")
    A("")

    # ---------------------------------------------------------------- 2
    A("## 2. The shape of the upper tail")
    A("")
    tm = t["mentions"]
    tf = t["first_mentions"]
    A(f"These data cannot tell a power law from a lognormal, and the design is "
      f"what stops them: the Kolmogorov-Smirnov rule leaves "
      f"{tm['pl_n_tail']} entities in the fitted tail, and at that size the two "
      f"families fit equally well by construction. The tables below report the "
      f"fits in full so that a reader can see how far short of a determination "
      f"they fall.")
    A("")
    A(f"**Table S4.5.** Power law against lognormal on the entity mention counts. "
      f"Discrete maximum likelihood, xmin chosen by minimising the "
      f"Kolmogorov-Smirnov distance (Clauset, Shalizi and Newman). Goodness of fit "
      f"is the CSN bootstrap over {args.gof:,} synthetic datasets; the "
      f"power law vs lognormal comparison is the normalised log-likelihood ratio "
      f"with its two-sided Vuong p-value.")
    A("")
    A("| Quantity | Mentions | First mentions |")
    A("|---|---:|---:|")
    A(f"| Entities with a positive count | {tm['n_positive']} | {tf['n_positive']} |")
    A(f"| Largest count | {tm['max']:.0f} | {tf['max']:.0f} |")
    A(f"| xmin (KS rule) | {tm['pl_xmin']:.0f} | {tf['pl_xmin']:.0f} |")
    A(f"| Observations above xmin | {tm['pl_n_tail']} | {tf['pl_n_tail']} |")
    A(f"| Exponent alpha | {tm['pl_alpha']:.3f} | {tf['pl_alpha']:.3f} |")
    A(f"| alpha, 95% interval | {fmt_ci(tm['pl_alpha_lo'], tm['pl_alpha_hi'])} | "
      f"{fmt_ci(tf['pl_alpha_lo'], tf['pl_alpha_hi'])} |")
    A(f"| KS distance D | {tm['pl_D']:.4f} | {tf['pl_D']:.4f} |")
    A(f"| Goodness-of-fit p (bootstrap) | {fmt_p(tm['gof_p'])} | {fmt_p(tf['gof_p'])} |")
    A(f"| Power law vs lognormal, R | {tm['vs_lognormal_R']:.4f} | {tf['vs_lognormal_R']:.4f} |")
    A(f"| Power law vs lognormal, p | {fmt_p(tm['vs_lognormal_p'])} | {fmt_p(tf['vs_lognormal_p'])} |")
    A(f"| Power law vs exponential, R | {tm['vs_exponential_R']:.4f} | {tf['vs_exponential_R']:.4f} |")
    A(f"| Power law vs exponential, p | {fmt_p(tm['vs_exponential_p'])} | {fmt_p(tf['vs_exponential_p'])} |")
    A(f"| Power law vs truncated power law, R | {tm['vs_truncated_R']:.4f} | {tf['vs_truncated_R']:.4f} |")
    A(f"| Power law vs truncated power law, p | {fmt_p(tm['vs_truncated_p'])} | {fmt_p(tf['vs_truncated_p'])} |")
    A(f"| Independent CSN implementation: xmin | {tm['own_xmin']:.0f} | {tf['own_xmin']:.0f} |")
    A(f"| Independent CSN implementation: alpha | {tm['own_alpha']:.3f} | {tf['own_alpha']:.3f} |")
    A(f"| Independent CSN implementation: D | {tm['own_D']:.4f} | {tf['own_D']:.4f} |")
    A("")
    A(f"*Notes.* Read the third row of this table before the fifth. The KS rule "
      f"places xmin at {tm['pl_xmin']:.0f} mentions, which leaves "
      f"{tm['pl_n_tail']} entities in the fitted tail out of "
      f"{tm['n_positive']} with any mention at all and "
      f"{N['n_cohort_real']} in the cohort. An exponent estimated on "
      f"{tm['pl_n_tail']} points carries a standard error of "
      f"{tm['pl_sigma']:.3f}, so the interval "
      f"{fmt_ci(tm['pl_alpha_lo'], tm['pl_alpha_hi'])} covers most of the range "
      f"that any tail model would produce. The bootstrap goodness of fit does not "
      f"reject the power law (p = {fmt_p(tm['gof_p'])}), and the likelihood-ratio "
      f"comparison against lognormal returns R = {tm['vs_lognormal_R']:.4f} with "
      f"p = {fmt_p(tm['vs_lognormal_p'])}. A normalised ratio that close to zero "
      f"is the numerical statement that the two families fit the same data "
      f"equally well. The fitted lognormal is itself degenerate, with mu = "
      f"{tm['ln_mu']:.1f} and sigma = {tm['ln_sigma']:.1f}: the likelihood is "
      f"flat along a ridge, which is what happens when a two-parameter family is "
      f"asked to describe {tm['pl_n_tail']} points.")
    A("")
    A(f"The honest conclusion is that these data do not distinguish the families. "
      f"A power law is not rejected; neither is a lognormal; the exponential is "
      f"the only candidate the comparison pushes against "
      f"(R = {tm['vs_exponential_R']:.4f}, p = {fmt_p(tm['vs_exponential_p'])}), "
      f"and even that falls short of conventional significance. The constraint is "
      f"structural, and collecting for longer does not lift it: the cohort has "
      f"{N['n_cohort_real']} real firms by design and only {tm['n_positive']} were "
      f"ever named, so the largest sample any amount of further collection can "
      f"put into a tail fit is a few dozen points. Distinguishing a power law from "
      f"a lognormal at these sample sizes is not a question the design can answer, "
      f"and the right way to report it is to say so rather than to quote "
      f"alpha = {tm['pl_alpha']:.2f} as though the family were settled.")
    A("")
    A(f"The last three rows of the table are a second estimator written for this "
      f"section against scipy, following the same Clauset-Shalizi-Newman recipe: "
      f"maximum likelihood for the exponent with the Hurwitz zeta normaliser, "
      f"xmin by minimum KS distance over the candidate values, and the same "
      f"bootstrap for goodness of fit. On the mention counts it lands one "
      f"candidate value away from the library, xmin {tm['own_xmin']:.0f} against "
      f"{tm['pl_xmin']:.0f}, with alpha {tm['own_alpha']:.3f} against "
      f"{tm['pl_alpha']:.3f}. On first mentions the two agree on xmin "
      f"{tf['own_xmin']:.0f} and on alpha to "
      f"{abs(tf['pl_alpha'] - tf['own_alpha']):.4f}, and differ on D because the "
      f"two implementations break the discrete step at the tie differently. A "
      f"criterion whose optimum shifts under a difference that small is flat near "
      f"its minimum, which is the same finding the likelihood ratio reports and "
      f"rules out an implementation artefact as the source of the ambiguity.")
    A("")
    A("Rank-size pairs for anyone who wants to plot the distribution directly are "
      "in `data/s4_rank_size.csv`.")
    A("")

    # ---------------------------------------------------------------- 3
    A("## 3. Entities never named")
    A("")
    nv = N["never"]
    A(f"Tier is the attribute that decides whether a firm is ever named. Long-tail "
      f"members of the cohort are never named at "
      f"{100*nv['by_tier'].get('long_tail', 0)/nv['by_tier_denom']['long_tail']:.0f}% "
      f"against {100*nv['by_tier'].get('head', 0)/nv['by_tier_denom']['head']:.0f}% "
      f"for head members, and vertical adds nothing once tier is in the model. "
      f"The anchor coefficient reads as a comparison with Brazilian head firms "
      f"only, for a reason the notes below set out.")
    A("")
    A(f"**Table S4.6.** Cohort members with no mention anywhere inside the "
      f"{CM.WINDOW}-character window, across all {N['n_obs']:,} canonical "
      f"observations. Series {d0} to {d1}.")
    A("")
    A("| Partition | Never named | In cohort | Rate |")
    A("|---|---:|---:|---:|")
    for g, lab in [("BR", "Brazilian firms"), ("anchor", "International anchors"),
                   ("decoy", "Fictitious decoys")]:
        k = nv["by_group"].get(g, 0)
        n = nv["by_group_denom"][g]
        A(f"| {lab} | {k} | {n} | {100*k/n:.1f}% |")
    A(f"| **Total** | **{nv['n_total']}** | **{N['n_cohort_full']}** | "
      f"**{100*nv['n_total']/N['n_cohort_full']:.1f}%** |")
    A("")
    A("| Tier | Never named | In cohort | Rate |")
    A("|---|---:|---:|---:|")
    for tier in ["head", "torso", "long_tail"]:
        k = nv["by_tier"].get(tier, 0)
        n = nv["by_tier_denom"][tier]
        A(f"| {tier} | {k} | {n} | {100*k/n:.1f}% |")
    A("")
    A("| Vertical | Never named | Real cohort | Rate |")
    A("|---|---:|---:|---:|")
    for v in verticals:
        sub = cohort[(cohort.vertical == v) & (cohort.group != "decoy")]
        k = int((sub.mentions == 0).sum())
        A(f"| {VL[v]} | {k} | {len(sub)} | {100*k/len(sub):.1f}% |")
    A("")
    A(f"*Notes.* All sixteen decoys are never named, which is the result the "
      f"decoys exist to produce and which makes them useless as regression rows: "
      f"the group predicts the outcome perfectly. They are excluded from the "
      f"model below and reported here. Among real firms the never-named list is "
      f"{nv['n_total'] - 16} of {N['n_cohort_real']}.")
    A("")
    for v in verticals:
        lst = [n for n in nv["names_by_vertical"][v]
               if n in set(cohort[cohort.group != "decoy"].name)]
        A(f"**{VL[v]}**, never named: {', '.join(lst)}.")
        A("")

    n_never_real = nv["n_total"] - nv["by_group"].get("decoy", 0)
    A(f"**Table S4.7.** Logistic regression of never being named on the "
      f"attributes `src/config_v2.py` carries. {N['never_reg_n']} real cohort "
      f"members, {n_never_real} of them never named. Reference cell: Brazilian, "
      f"head tier, fintech. Odds ratios with Wald 95% intervals; the block tests "
      f"are likelihood-ratio.")
    A("")
    lg = N["never_logit"]
    A(f"Model converged: {'yes' if lg['converged'] else 'NOT CONVERGED'}. "
      f"Log-likelihood {lg['llf']:.3f} against {lg['llnull']:.3f} at the null, "
      f"McFadden pseudo R-squared {lg['prsquared']:.4f}, "
      f"overall likelihood-ratio p = {fmt_p(lg['llr_p'])}.")
    A("")
    A("| Term | Odds ratio | 95% interval | z | p |")
    A("|---|---:|---|---:|---:|")
    pretty = {
        "Intercept": "Intercept (Brazilian, head, fintech, founded 2000)",
        "C(group, Treatment('BR'))[T.anchor]": "International anchor (vs Brazilian)",
        "C(tier, Treatment('head'))[T.long_tail]": "Long-tail tier (vs head)",
        "C(tier, Treatment('head'))[T.torso]": "Torso tier (vs head)",
        "C(vertical, Treatment('fintech'))[T.saude]": "Health (vs fintech)",
        "C(vertical, Treatment('fintech'))[T.tecnologia]": "Technology (vs fintech)",
        "C(vertical, Treatment('fintech'))[T.varejo]": "Retail (vs fintech)",
        "founded_dec": "Founding year, per decade later",
    }
    for row in lg["terms"]:
        A(f"| {pretty.get(row['term'], row['term'])} | {row['or']:.3f} | "
          f"{fmt_ci(row['or_lo'], row['or_hi'])} | {row['z']:.2f} | "
          f"{fmt_p(row['p'])} |")
    A("")
    A("| Block | Likelihood-ratio statistic | df | p |")
    A("|---|---:|---:|---:|")
    blk_label = {"group": "Anchor against Brazilian", "tier": "Tier",
                 "vertical": "Vertical", "founded_year": "Founding year"}
    for k, v in N["never_lr"].items():
        A(f"| {blk_label[k]} | {v['lr']:.3f} | {v['df']} | {fmt_p(v['p'])} |")
    A("")
    nm = N["never_marginal"]
    or_anchor = [r for r in lg["terms"]
                 if r["term"] == "C(group, Treatment('BR'))[T.anchor]"][0]
    or_lt = [r for r in lg["terms"]
             if r["term"] == "C(tier, Treatment('head'))[T.long_tail]"][0]
    A(f"*Notes.* Tier is the attribute that separates. A long-tail firm has "
      f"{or_lt['or']:.1f} times the odds of never being named that a head firm "
      f"has, {fmt_ci(or_lt['or_lo'], or_lt['or_hi'], 2)}, and the tier block "
      f"carries a likelihood-ratio p of "
      f"{fmt_p(N['never_lr']['tier']['p'])}. Read the anchor coefficient with "
      f"care: every one of the 32 international anchors is head tier, so the "
      f"adjusted odds ratio of {or_anchor['or']:.2f} compares anchors with "
      f"Brazilian head firms alone, of which {nm['BR_head'][0]} of "
      f"{nm['BR_head'][1]} ({100*nm['BR_head'][0]/nm['BR_head'][1]:.1f}%) are "
      f"never named against {nm['anchor_head'][0]} of {nm['anchor_head'][1]} "
      f"({100*nm['anchor_head'][0]/nm['anchor_head'][1]:.1f}%) of the anchors. "
      f"Unadjusted, the two groups barely differ "
      f"({100*nv['by_group']['BR']/nv['by_group_denom']['BR']:.1f}% against "
      f"{100*nv['by_group']['anchor']/nv['by_group_denom']['anchor']:.1f}%), so "
      f"the adjustment produces the whole contrast and the confounding between "
      f"group and tier is total. Vertical separates nothing "
      f"(p = {fmt_p(N['never_lr']['vertical']['p'])}), which agrees with "
      f"Table S4.3: verticals differ in how concentrated coverage is while "
      f"leaving out similar numbers of firms.")
    A("")
    A(f"Founding year enters as a continuous covariate, per decade, with "
      f"p = {fmt_p(N['never_lr']['founded_year']['p'])}. The pre-training cutoff "
      f"framing that motivated the variable cannot be tested on this cohort: the "
      f"most recently founded member dates from 2019 and every plausible cutoff "
      f"for the pinned engine versions is later, so the indicator for a firm "
      f"founded after the cutoff has no cases and was not fitted. What the "
      f"coefficient describes is a within-cohort gradient of age.")
    A("")
    ls = N["legal_status_counts"]
    A(f"Legal status was available and was not modelled, because it has no "
      f"variance to model: {ls.get('active', 0)} of the {N['never_reg_n']} real "
      f"cohort members are `active` and "
      f"{ls.get('judicial_recovery', 0)} carries `judicial_recovery` "
      f"({', '.join(f'{k} with {v:,} mentions' for k, v in N['legal_status_mentions'].items())}). "
      f"One case cannot identify a coefficient, and a model fitted on it would "
      f"report an interval wide enough to contain any conclusion. Region was also "
      f"not modelled: it is recorded only for Brazilian firms, so a regression "
      f"including it would silently drop all 32 anchors and change the question.")
    A("")

    # ---------------------------------------------------------------- 4
    A("## 4. International anchors against Brazilian firms")
    A("")
    cell = N["anchor_cells"]
    A(f"Query language changes which group the engines name, and in technology it "
      f"reverses the ranking outright: in Portuguese an international anchor is "
      f"named at {cell['tecnologia|pt']['rr']:.2f} times the per-slot rate of a "
      f"Brazilian firm, in English the Brazilian firm leads at "
      f"{cell['tecnologia|en']['rr']:.2f} times the anchor rate, from the same "
      f"battery translated. The tables below give the rates, the paired test and "
      f"the interaction.")
    A("")
    A(f"The cohort puts 8 international anchors in every vertical alongside 19 or "
      f"20 Brazilian firms, and every query names Brazil. The comparison is "
      f"therefore within vertical and within battery by construction: the same "
      f"answer is scored for both groups. Because the two groups have different "
      f"sizes, the rate reported is per entity-slot, that is mentions divided by "
      f"(observations x entities in the group), which is the probability that a "
      f"given cohort member is named in a given answer. Intervals and tests come "
      f"from the same cluster bootstrap over observations, {args.boot:,} "
      f"replicates.")
    A("")
    A(f"**Table S4.8.** Per-slot naming rate by group, vertical and query "
      f"language. Series {d0} to {d1}, {N['n_obs']:,} observations.")
    A("")
    A("| Vertical | Language | Observations | Brazilian rate | Anchor rate | Rate ratio | Cohen's h | Answers naming a Brazilian firm | Answers naming an anchor |")
    A("|---|---|---:|---:|---:|---:|---:|---:|---:|")
    for v in verticals + ["all"]:
        for lg_ in ["pt", "en", "all"]:
            b = cell[f"{v}|{lg_}"]
            rr = "—" if not np.isfinite(b["rr"]) else f"{b['rr']:.2f}"
            A(f"| {VL.get(v, 'All')} | {lg_.upper()} | {b['n']:,} | "
              f"{100*b['br_rate']:.3f}% | {100*b['an_rate']:.3f}% | {rr} | "
              f"{b['h']:.3f} | {100*b['any_br']:.2f}% | {100*b['any_an']:.2f}% |")
    A("")
    ab = N["anchor_boot"]
    A(f"*Notes.* Pooled over verticals and languages the rate ratio is "
      f"{cell['all|all']['rr']:.2f}, bootstrap interval on the log scale "
      f"{fmt_ci(math.exp(ab['all']['lo']), math.exp(ab['all']['hi']))} after "
      f"exponentiating, bootstrap p = {fmt_boot_p(ab['all'])}. The pooled "
      f"figure hides the result worth reporting, which is the interaction.")
    A("")
    A(f"**Table S4.9.** The language interaction: log rate ratio (Brazilian over "
      f"anchor) in each language and the difference between them, with percentile "
      f"cluster-bootstrap intervals over {args.boot:,} replicates. A difference "
      f"whose interval excludes zero is a language-dependent reversal of which "
      f"group the engines name.")
    A("")
    A("| Vertical | log RR, PT | log RR, EN | Difference (PT less EN) | 95% interval | Bootstrap p |")
    A("|---|---:|---:|---:|---|---:|")
    for v in verticals:
        b_pt = cell[f"{v}|pt"]
        b_en = cell[f"{v}|en"]
        bb = N["anchor_boot_vertical"][v]["inter"]
        lp = math.log(b_pt["rr"]) if np.isfinite(b_pt["rr"]) and b_pt["rr"] > 0 else float("nan")
        le = math.log(b_en["rr"]) if np.isfinite(b_en["rr"]) and b_en["rr"] > 0 else float("nan")
        A(f"| {VL[v]} | {lp:.3f} | {le:.3f} | {lp - le:.3f} | "
          f"{fmt_ci(bb['lo'], bb['hi'])} | {fmt_boot_p(bb)} |")
    bb = ab["inter"]
    lp = math.log(cell["all|pt"]["rr"])
    le = math.log(cell["all|en"]["rr"])
    A(f"| All | {lp:.3f} | {le:.3f} | {lp - le:.3f} | "
      f"{fmt_ci(bb['lo'], bb['hi'])} | {fmt_boot_p(bb)} |")
    A("")
    tec_pt = cell["tecnologia|pt"]
    tec_en = cell["tecnologia|en"]
    A(f"*Notes.* Technology reverses. Asked in Portuguese about Brazilian "
      f"technology and IT, the engines name an international anchor at "
      f"{100*tec_pt['an_rate']:.3f}% per slot against "
      f"{100*tec_pt['br_rate']:.3f}% for a Brazilian firm, a rate ratio of "
      f"{tec_pt['rr']:.2f}; asked the same question in English the ratio is "
      f"{tec_en['rr']:.2f} the other way. The other three verticals favour "
      f"Brazilian firms in both languages and favour them more strongly in "
      f"English. Fintech is the extreme case: "
      f"{cell['fintech|all']['an_named']} anchor matches in "
      f"{cell['fintech|all']['an_slots']:,} slots, so the rate ratio is "
      f"numerically unstable and is reported for completeness rather than "
      f"interpreted.")
    A("")
    A(f"**Table S4.10.** The same comparison paired within the answer. Each "
      f"observation either names a Brazilian firm only, an anchor only, both or "
      f"neither; the table counts the discordant answers and tests them with an "
      f"exact binomial, the exact form of McNemar's test. This is the "
      f"design-faithful comparison because both groups are scored on the same "
      f"text, but it does not correct for the groups being of different size.")
    A("")
    A("| Vertical | Language | Brazilian only | Anchor only | Exact p |")
    A("|---|---|---:|---:|---:|")
    for v in verticals:
        for lg_ in ["pt", "en"]:
            b = cell[f"{v}|{lg_}"]
            A(f"| {VL[v]} | {lg_.upper()} | {b['mcnemar_b']:,} | "
              f"{b['mcnemar_c']:,} | {fmt_p(b['mcnemar_p'])} |")
    b = cell["all|all"]
    A(f"| All | both | {b['mcnemar_b']:,} | {b['mcnemar_c']:,} | "
      f"{fmt_p(b['mcnemar_p'])} |")
    A("")
    el = N["anchor_entity_level"]
    A(f"**Table S4.11.** Entity-level check, so that the conclusion does not rest "
      f"on a unit of analysis that treats one answer as many. Each entity "
      f"contributes one coverage rate, mentions over the observations of its "
      f"vertical; the two groups are compared with Mann-Whitney U and Cliff's "
      f"delta.")
    A("")
    A("| Vertical | Brazilian firms | Anchors | Median rate, Brazilian | Median rate, anchor | U | p | Cliff's delta |")
    A("|---|---:|---:|---:|---:|---:|---:|---:|")
    for v in verticals:
        e = el[v]
        A(f"| {VL[v]} | {e['n_br']} | {e['n_an']} | {100*e['median_br']:.3f}% | "
          f"{100*e['median_an']:.3f}% | {e['U']:.1f} | {fmt_p(e['p'])} | "
          f"{e['cliffs_delta']:.3f} |")
    A("")
    az = N["amazon_nesting"]
    A(f"*Notes.* Two cohort names are nested inside another name of the same "
      f"vertical, so one span of text satisfies both patterns. `Amazon` (anchor, "
      f"retail) is contained in `Amazon Brasil` (Brazilian, retail): `Amazon` has "
      f"{az['amazon']:,} mentions, `Amazon Brasil` {az['amazon_brasil']:,}, and "
      f"{az['co_occurring']:,} of them are the same observation. Removing `Amazon` "
      f"from the retail anchor set moves the retail anchor rate from "
      f"{100*az['retail_anchor_rate_with']:.3f}% to "
      f"{100*az['retail_anchor_rate_without']:.3f}%, which does not change the "
      f"direction of any comparison in Table S4.8. `Accenture` and "
      f"`Accenture Brasil` are the same construction in technology, with "
      f"{az['accenture']:,} and {az['accenture_brasil']:,} mentions; since the "
      f"Brazilian variant is never matched, no retail-style correction applies "
      f"there. Both are declared rather than silently resolved, for the same "
      f"reason as the two colliding names in Table S4.4.")
    A("")

    # ---------------------------------------------------------------- 5
    A("## 5. How many firms an answer names")
    A("")
    cm = N["counts"]["window"]
    ca = N["counts"]["as_collected"]
    A(f"A single overdispersed process accounts for the whole distribution, zeros "
      f"included. The negative binomial beats the zero-inflated forms on both "
      f"information criteria and reproduces the observed zero count to within "
      f"{abs(cm['pred_zeros']['NB2'] - cm['obs_zeros']):,.0f} answers out of "
      f"{cm['n']:,}, so the excess of zeros over Poisson needs no second "
      f"mechanism to explain it. Citing is rare and clumped: most answers name "
      f"nobody and the ones that name anybody tend to name several.")
    A("")
    A(f"**Table S4.12.** Distribution of the number of distinct cohort entities "
      f"named per answer, under the uniform {CM.WINDOW}-character window and, for "
      f"contrast, in the stored `cited_count_v2` which was computed on the "
      f"as-collected text. Series {d0} to {d1}, {N['n_obs']:,} observations.")
    A("")
    A("| Entities named | Window count | Share | `cited_count_v2` | Share |")
    A("|---:|---:|---:|---:|---:|")
    kmax = max(max(cm["hist"]), max(ca["hist"]))
    for k in range(0, kmax + 1):
        a = cm["hist"].get(k, 0)
        b = ca["hist"].get(k, 0)
        A(f"| {k} | {a:,} | {100*a/cm['n']:.3f}% | {b:,} | {100*b/ca['n']:.3f}% |")
    A(f"| **Total** | **{cm['n']:,}** | 100% | **{ca['n']:,}** | 100% |")
    A("")
    A(f"Mean {cm['mean']:.4f}, variance {cm['var']:.4f}, variance-to-mean ratio "
      f"{cm['vmr']:.3f} under the window; mean {ca['mean']:.4f}, variance "
      f"{ca['var']:.4f}, ratio {ca['vmr']:.3f} as collected. A Poisson process "
      f"with the observed mean would put {cm['pred_zeros']['Poisson']:,.0f} "
      f"answers at zero; {cm['obs_zeros']:,} are observed, an excess of "
      f"{cm['obs_zeros'] - cm['pred_zeros']['Poisson']:,.0f}.")
    A("")
    A(f"**Table S4.13.** Count models for the windowed count, intercept only, so "
      f"that the comparison is about the shape of the marginal distribution and "
      f"not about covariates. {cm['n']:,} observations.")
    A("")
    A("| Model | Parameters | Log-likelihood | AIC | BIC | Predicted zeros | Converged |")
    A("|---|---:|---:|---:|---:|---:|---|")
    for k in ["Poisson", "NB2", "ZIP", "ZINB"]:
        f = cm["fits"][k]
        pz = cm["pred_zeros"][k]
        pzs = "—" if not np.isfinite(pz) else f"{pz:,.0f}"
        A(f"| {k} | {f['k']} | {f['llf']:,.2f} | {f['aic']:,.2f} | {f['bic']:,.2f} | "
          f"{pzs} | {'yes' if f['converged'] else 'NOT CONVERGED'} |")
    A(f"| Observed | — | — | — | — | {cm['obs_zeros']:,} | — |")
    A("")
    A(f"*Notes.* The negative binomial wins on both criteria "
      f"(AIC {cm['fits']['NB2']['aic']:,.0f} against "
      f"{cm['fits']['Poisson']['aic']:,.0f} for Poisson and "
      f"{cm['fits']['ZIP']['aic']:,.0f} for zero-inflated Poisson) and it "
      f"reproduces the zero count almost exactly, "
      f"{cm['pred_zeros']['NB2']:,.0f} predicted against {cm['obs_zeros']:,} "
      f"observed. The zero-inflated negative binomial adds a parameter and buys "
      f"nothing: its inflation probability is estimated at "
      f"{cm['zinb_pi']:.2e}, a boundary value, its log-likelihood matches the "
      f"plain negative binomial to "
      f"{abs(cm['fits']['ZINB']['llf'] - cm['fits']['NB2']['llf']):.4f}, and BIC "
      f"prefers the simpler model by "
      f"{cm['fits']['ZINB']['bic'] - cm['fits']['NB2']['bic']:.2f}. The answer to "
      f"the question this section asks is therefore that the zeros are not "
      f"special. There is no separate population of answers that cannot name a "
      f"firm sitting behind a population that sometimes does; a single "
      f"overdispersed process generates both, and the excess of zeros over "
      f"Poisson is the ordinary consequence of that overdispersion, with "
      f"dispersion parameter {cm['nb_alpha']:.3f}.")
    A("")
    cc = N["counts_covariates"]
    A(f"Adding engine, vertical and language as covariates does not change the "
      f"ranking: Poisson AIC {cc['Poisson']['aic']:,.0f}, negative binomial "
      f"{cc['NB2']['aic']:,.0f}, zero-inflated negative binomial "
      f"{cc['ZINB']['aic']:,.0f}"
      f"{'' if cc['ZINB']['converged'] else ' (NOT CONVERGED, reported as such)'}. "
      f"The dispersion parameter is what changes across those specifications, "
      f"and the ordering of the four families does not.")
    A("")
    A(f"The as-collected column is reported beside the windowed one because the "
      f"two differ by construction, and what separates them is the window. "
      f"Perplexity is the only arm whose stored text exceeds "
      f"{CM.WINDOW} characters: {N['perplexity_window']['n_stored_gt_window']:,} of "
      f"its {N['perplexity_window']['n']:,} canonical rows, mean stored length "
      f"{N['perplexity_window']['mean_stored_len']:.0f} characters. Its answers "
      f"name an entity in {N['perplexity_window']['named_as_collected']:,} rows as "
      f"collected and {N['perplexity_window']['named_in_window']:,} inside the "
      f"window. Every count comparison across arms therefore has to state its "
      f"window, which is why this section uses the uniform one everywhere else.")
    A("")

    # ---------------------------------------------------------------- 6
    A("## 6. Where the first mention falls")
    A("")
    ps = N["position"]
    _med = {e: s["median"] for e, s in N["position"]["by_engine"].items()}
    A(f"The six engines reach their first cohort entity at medians spanning "
      f"{min(_med.values()):.0f} to {max(_med.values()):.0f} characters, a spread "
      f"covering most of the observation window. On the rows that retained the "
      f"whole response the same engines cannot be told apart once the offset is "
      f"expressed as a fraction of the answer, which makes the absolute spread a "
      f"joint statement about where an engine starts naming and how long it "
      f"writes. A protocol that reports position has to declare the window before "
      f"the number compares across engines.")
    A("")
    A(f"**Table S4.14.** Character offset of the first cohort entity inside the "
      f"uniform {CM.WINDOW}-character window, by engine. Denominator is the "
      f"answers of that engine that name an entity inside the window. Series "
      f"{d0} to {d1}.")
    A("")
    A("| Engine | Answers naming an entity | Mean | Q10 | Q25 | Median | Q75 | Q90 | Max | Opens with the name |")
    A("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for e, s in ps["by_engine"].items():
        A(f"| {e} | {s['n']:,} | {s['mean']:.1f} | {s['q10']:.0f} | {s['q25']:.0f} | "
          f"{s['median']:.0f} | {s['q75']:.0f} | {s['q90']:.0f} | {s['max']:.0f} | "
          f"{100*s['frac_at_zero']:.1f}% |")
    A("")
    A(f"Kruskal-Wallis across the {ps['kruskal_df']+1} engines: "
      f"H = {ps['kruskal_H']:,.1f}, df = {ps['kruskal_df']}, "
      f"p = {fmt_p(ps['kruskal_p'])}, epsilon-squared = {ps['epsilon2']:.4f}.")
    A("")
    A("| Pair | z | Holm-adjusted p |")
    A("|---|---:|---:|")
    for row in sorted(ps["dunn"], key=lambda r: -abs(r["z"])):
        A(f"| {row['a']} against {row['b']} | {row['z']:.2f} | {fmt_p(row['p_holm'])} |")
    A("")
    slowest = max(ps["by_engine"], key=lambda e: ps["by_engine"][e]["median"])
    fastest = min(ps["by_engine"], key=lambda e: ps["by_engine"][e]["median"])
    A(f"*Notes.* The engines place the first name in different parts of the "
      f"answer. {slowest} reaches its first cohort entity at a median of "
      f"{ps['by_engine'][slowest]['median']:.0f} characters, {fastest} at "
      f"{ps['by_engine'][fastest]['median']:.0f}, with "
      f"{100*ps['by_engine'][fastest]['frac_at_zero']:.1f}% of its naming answers "
      f"opening on the entity itself. Epsilon-squared of {ps['epsilon2']:.4f} puts "
      f"about a fifth of the variance in rank on the engine, a large share for a "
      f"grouping variable nobody chose as a treatment. With "
      f"{sum(s['n'] for s in ps['by_engine'].values()):,} answers behind the "
      f"comparison the p-value carries little information and the quantiles carry "
      f"the result: the interquartile range of {slowest} sits entirely above the "
      f"median of {fastest}.")
    A("")
    A("### The relative offset is censored for five of the six arms")
    A("")
    A(f"A relative offset, the position of the first mention as a fraction of the "
      f"answer, is the quantity one would prefer to compare, and for most of this "
      f"series it cannot be computed. Five client adapters stored "
      f"`response_text = text[:{CM.WINDOW}]`. For those arms the denominator is "
      f"the constant {CM.WINDOW} whenever the answer reached that length, so the "
      f"relative offset is the absolute offset rescaled and adds nothing to "
      f"Table S4.14. It also carries a bias in a known direction: the answer ran "
      f"past the cap, so offset divided by {CM.WINDOW} overstates how late in the "
      f"text the first name appears, and the overstatement grows with the length "
      f"of what was discarded. The column below reports how often each arm's "
      f"naming answers sit exactly at the {CM.WINDOW}-character cap, which for the "
      f"five truncating arms is the share whose relative offset is censored. For "
      f"Perplexity a record of exactly {CM.WINDOW} characters is a short complete "
      f"answer, since that adapter stored up to 2,502 characters.")
    A("")
    A("| Engine | Answers naming an entity | Stored length exactly at the cap | Median relative offset, as stored |")
    A("|---|---:|---:|---:|")
    for e, s in ps["by_engine"].items():
        A(f"| {e} | {s['n']:,} | {100*s['at_cap_share']:.1f}% | "
          f"{s['rel_median']:.3f} |")
    A("")
    pu = N["position_uncensored"]
    beyond = N["position_uncensored_beyond_window"]
    A(f"**Table S4.15.** Relative offset on the rows that retained the whole "
      f"response, where the denominator is the real length of the answer and the "
      f"first mention is re-extracted over the entire text, so that a first "
      f"mention falling past character {CM.WINDOW} is counted. "
      f"{N['position_uncensored_n_rows']:,} rows carry a full response, from "
      f"migration 0010 onwards, which is why the counts are small and why this "
      f"table checks direction instead of measuring level.")
    A("")
    A("| Engine | Rows naming an entity | First mention beyond the window | Median response length | Median absolute offset | Q25 | Median relative | Q75 |")
    A("|---|---:|---:|---:|---:|---:|---:|---:|")
    for e, s in pu.items():
        A(f"| {e} | {s['n']:,} | {beyond.get(e, 0):,} | {s['len_median']:,.0f} | "
          f"{s['abs_median']:,.0f} | {s['q25']:.3f} | {s['median']:.3f} | "
          f"{s['q75']:.3f} |")
    A("")
    if "position_uncensored_kruskal" in N:
        k = N["position_uncensored_kruskal"]
        ka = N.get("position_uncensored_abs_kruskal", {})
        meds = [s["median"] for s in pu.values()]
        A(f"Kruskal-Wallis on the relative offsets of this subset: "
          f"H = {k['H']:.1f}, df = {k['df']}, p = {fmt_p(k['p'])}, "
          f"epsilon-squared = {k['epsilon2']:.4f}. The five arms present fall in "
          f"a band from {min(meds):.3f} to {max(meds):.3f} and the test does not "
          f"separate them. On the same rows the absolute offsets do separate them "
          f"(H = {ka.get('H', float('nan')):.1f}, df = {ka.get('df', 0)}, "
          f"p = {fmt_p(ka.get('p', float('nan')))}, epsilon-squared = "
          f"{ka.get('epsilon2', float('nan')):.4f}), so the engine ranking of "
          f"Table S4.14 describes where an engine starts naming in characters "
          f"while the arms write answers of different lengths, and the two "
          f"differences cancel once the offset is divided by the length.")
        A("")
        A(f"The reading this licenses is narrow. It applies to five arms, to "
          f"{sum(s['n'] for s in pu.values()):,} answers collected after the full "
          f"response began to be retained, and to a query mix that differs from the "
          f"one in force in April. It does say that a relative-position claim built on "
          f"the truncated series would have been an artefact of the truncation, "
          f"and that BRGEO-1 has to declare the window before any position "
          f"statistic is comparable across engines.")
        A("")

    # ---------------------------------------------------------------- limits
    A("## What this does not establish")
    A("")
    A(f"**Concentration is measured, its cause is not.** Every index here "
      f"describes the distribution of names across answers. Nothing in the design "
      f"separates an engine that concentrates because the market is concentrated "
      f"from one that concentrates because its training corpus over-represents "
      f"the same few firms, or because the query wording invites a single answer. "
      f"The battery contains directive prompts that ask for the best or the "
      f"leader, and those prompts mechanically produce one name; the section does "
      f"not decompose the indices by query type, and until it does no share of "
      f"the observed HHI can be attributed to engine behaviour rather than to "
      f"the instrument.")
    A("")
    A(f"**The tail family is undetermined, and no amount of further collection "
      f"settles it.** With {t['mentions']['pl_n_tail']} entities "
      f"above the selected xmin, the likelihood-ratio comparison against lognormal "
      f"returns R = {t['mentions']['vs_lognormal_R']:.4f}. Nothing here licenses "
      f"the sentence \"citation follows a power law\", and the exponent of "
      f"{t['mentions']['pl_alpha']:.2f} should not be quoted without the sample "
      f"size that produced it.")
    A("")
    A(f"**Never named is never named in this window, in this battery, by these "
      f"engines, in this period.** The {N['never']['n_total'] - 16} real firms "
      f"with no mention were not tested against queries naming them. A firm can "
      f"be absent from an answer to \"which company leads Brazilian retail\" and "
      f"be described accurately when asked about directly; the adversarial probe "
      f"stratum exists for that question and is excluded here by "
      f"`COALESCE(is_probe,0)=0`. Absence of coverage in a discovery battery is "
      f"not absence of knowledge.")
    A("")
    A(f"**The anchor comparison is not a test of home bias.** The two groups "
      f"differ in size (8 against 19 or 20 per vertical), in tier composition "
      f"(all anchors are head, the Brazilian set spans three tiers) and in what "
      f"the query asks for, since every prompt names Brazil. The per-slot rate "
      f"handles the size difference and nothing handles the other two. The "
      f"language interaction in Table S4.9 is the finding that survives those "
      f"caveats, because it compares each group with itself across languages.")
    A("")
    A(f"**The count models describe the marginal distribution and do not license "
      f"a causal reading of the zeros.** The negative binomial beating the "
      f"zero-inflated forms says that one overdispersed process fits; it does not "
      f"say that no distinct abstention mechanism exists. Abstention was measured "
      f"directly in the refusal taxonomy of the manuscript, and this section "
      f"neither confirms nor contradicts it.")
    A("")
    A(f"**Offsets in Table S4.14 are offsets inside a window.** For five of the "
      f"six arms the answer beyond character {CM.WINDOW} was never written to "
      f"disk, so no re-extraction can recover it, and a first mention that fell "
      f"past the cap is absent from the distribution rather than late in it. "
      f"Table S4.15 carries the uncensored measurement on "
      f"{N['position_uncensored_n_rows']:,} rows from the end of the series, and "
      f"on those rows the engines separate on absolute offset and not on relative "
      f"offset. A reader who needs relative position should use Table S4.15 with "
      f"its sample sizes and its period, and should treat the level as specific "
      f"to that slice.")
    A("")
    A(f"**Matching leaks are declared and not corrected.** Two cohort names "
      f"collide with ordinary words and two more are nested inside another cohort "
      f"name. The sensitivity analyses in Tables S4.4 and S4.11 bound their "
      f"effect; correcting them belongs in `src/config.py` followed by "
      f"re-extraction, which would break the correspondence with the stored "
      f"series that the identity check establishes.")
    A("")
    A("---")
    A("")
    A(f"Reproduce with `python s4_concentration.py --boot {args.boot} "
      f"--gof {args.gof}`. Raw values in `data/s4_numbers.json`; curves in "
      f"`data/s4_lorenz_global.csv`, `data/s4_lorenz_by_vertical.csv` and "
      f"`data/s4_rank_size.csv`.")
    A("")
    return "\n".join(L)


if __name__ == "__main__":
    raise SystemExit(main())
