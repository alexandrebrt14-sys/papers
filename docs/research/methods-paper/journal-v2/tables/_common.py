"""_common.py — shared primitives for the BRGEO-1 journal-v2 tables.

Read-only access to the study database, Wilson intervals, and the two
measurement rules that are not plain SQL (the entity extractor and the
preamble regex). Everything the table builders need that is not a query
lives here, so that `window_analysis.py` and `build_tables.py` cannot
drift apart on the matching rule — which is the whole point of the paper.

Nothing in this module writes to the database: the connection is opened with
`mode=ro`, so any write raises `sqlite3.OperationalError`.
"""
from __future__ import annotations

import math
import re
import sqlite3
import sys
from pathlib import Path

# The repository root, so that `src.*` imports resolve regardless of cwd.
REPO_ROOT = Path(__file__).resolve().parents[5]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

DB_PATH = REPO_ROOT / "data" / "papers.db"
DB_URI = f"file:{DB_PATH.as_posix()}?mode=ro"

#: Canonical observation window of the study, in characters (METHODOLOGY_V2 4.1-bis).
WINDOW = 200

#: Database vertical slugs (pt-BR), as stored in `citations.vertical`.
VERTICALS = ("fintech", "varejo", "saude", "tecnologia")

#: English labels for the verticals, for the published tables.
VERTICAL_LABEL = {
    "fintech": "Fintech",
    "varejo": "Retail",
    "saude": "Health",
    "tecnologia": "Technology",
}

#: Display order for engines.
ENGINES = ("ChatGPT", "Claude", "Gemini", "Groq", "Perplexity", "Grok")

#: Engine class, per MANUSCRIPT.md Table 3.
ENGINE_CLASS = {
    "ChatGPT": "parametric",
    "Claude": "parametric",
    "Gemini": "parametric",
    "Groq": "parametric, open weights",
    "Grok": "parametric",
    "Perplexity": "retrieval-augmented",
}

#: Cells below this n are reported as descriptive only.
SMALL_N = 30

#: The canonical stratum of the study.
CANONICAL = "COALESCE(is_probe,0)=0"


def connect() -> sqlite3.Connection:
    """Open the study database read-only. Writes are impossible on this handle."""
    con = sqlite3.connect(DB_URI, uri=True)
    con.row_factory = sqlite3.Row
    return con


# ---------------------------------------------------------------------------
# Wilson score interval
# ---------------------------------------------------------------------------

def wilson(successes: int, n: int, z: float = 1.959963984540054) -> tuple[float, float]:
    """95% Wilson score interval for a binomial proportion, returned as (lo, hi).

    Wilson rather than Wald because several cells in these tables sit at or
    near zero (Gemini at 1.9%, Claude preamble at 0.0%), where the Wald
    interval is degenerate or crosses zero.
    """
    if n == 0:
        return (float("nan"), float("nan"))
    p = successes / n
    denom = 1.0 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = (z / denom) * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (max(0.0, centre - half), min(1.0, centre + half))


def pct(successes: int, n: int, decimals: int = 1) -> str:
    if n == 0:
        return "—"
    return f"{100 * successes / n:.{decimals}f}"


def rate_cell(successes: int, n: int, decimals: int = 1) -> str:
    """Format a rate as `p.p [lo, hi]` in percentage points, or an em dash when n = 0."""
    if n == 0:
        return "—"
    lo, hi = wilson(successes, n)
    return (f"{100 * successes / n:.{decimals}f} "
            f"[{100 * lo:.{decimals}f}, {100 * hi:.{decimals}f}]")


def flag_small(n: int) -> str:
    """Dagger marker for cells below the descriptive-only threshold."""
    return "†" if 0 < n < SMALL_N else ""


# ---------------------------------------------------------------------------
# Entity extraction — the project's own rule, not a parallel implementation
# ---------------------------------------------------------------------------

from src.analysis.entity_extraction import EntityExtractor  # noqa: E402
from src.config import (  # noqa: E402
    AMBIGUOUS_ENTITIES,
    CANONICAL_NAMES,
    ENTITY_ALIASES,
    ENTITY_STOP_CONTEXTS,
)
from src.config_v2 import (  # noqa: E402
    FICTITIOUS_DECOYS_V2,
    get_v2_anchors,
    get_v2_cohort,
    get_v2_decoys,
    get_v2_real_entities,
)


def build_extractors(include_anchors: bool = True,
                     include_decoys: bool = True) -> dict[str, EntityExtractor]:
    """One extractor per vertical, over the v2 cohort.

    `include_anchors=True, include_decoys=True` is the configuration used by
    `scripts/harmonize_citation_window.py`, i.e. the one that produced the
    window table of manuscript v1.0. NUMBERS.md V2 verifies that re-extracting
    `response_text[:200]` under this configuration reproduces the stored
    `cited_v2` exactly for every arm whose text was truncated at collection
    time; that identity is what licenses using it here.
    """
    return {
        v: EntityExtractor(
            cohort=get_v2_cohort(v, include_anchors, include_decoys),
            aliases=ENTITY_ALIASES,
            ambiguous=AMBIGUOUS_ENTITIES,
            canonical_names=CANONICAL_NAMES,
            stop_contexts=ENTITY_STOP_CONTEXTS,
        )
        for v in VERTICALS
    }


def build_decoy_extractors() -> dict[str, EntityExtractor]:
    """Extractors restricted to the sixteen fictitious decoys."""
    return {
        v: EntityExtractor(
            cohort=get_v2_decoys(v),
            aliases={}, ambiguous=set(), canonical_names={}, stop_contexts={},
        )
        for v in VERTICALS
    }


ALL_DECOYS = {d for ds in FICTITIOUS_DECOYS_V2.values() for d in ds}
ALL_ANCHORS = {a for v in VERTICALS for a in get_v2_anchors(v)}
ALL_REAL_BR = {e for v in VERTICALS for e in get_v2_real_entities(v)}


# ---------------------------------------------------------------------------
# Preamble criterion (Table 5)
# ---------------------------------------------------------------------------
# The regular expression used for Table 7 of manuscript v1.0 is described in
# prose in MANUSCRIPT.md, METHODOLOGY_V2.md and
# governance/REVISAO-EXTERNA-PAPER-20260831.md ("anchored at the start of the
# response, matching greeting, hedge, question restatement and model
# self-reference") but was never committed to the repository, so it cannot be
# re-run. What follows is a re-specification in the same spirit, published in
# full because the criterion is itself part of the result. NUMBERS.md T5
# reports it side by side with the v1.0 figures over the identical row set, so
# a reviewer sees exactly where the two criteria agree and where they do not.

_PREAMBLE_GREETING = (
    r"(?:excelente|[óo]tima|boa|grande)\s+pergunta"
    r"|excellent\s+question|great\s+question|good\s+question"
    r"|that'?s\s+(?:an?\s+)?(?:excellent|great|good|interesting|very\s+good"
    r"|tricky|complex|challenging)"
    r"|com\s+certeza|claro(?:\!|,|\s+que)|of\s+course|certainly[,!]|sure[,!]"
)
_PREAMBLE_HEDGE = (
    r"[ée]\s+(?:muito\s+|bastante\s+)?"
    r"(?:dif[íi]cil|complexo|complicado|imposs[íi]vel)"
    r"|n[ãa]o\s+(?:h[áa]|existe|d[áa])\s+(?:uma\s+)?"
    r"(?:resposta|empresa|consenso|forma|[úu]nica)"
    r"|n[ãa]o\s+d[áa]\s+para"
    r"|it'?s?\s+(?:a\s+)?(?:tricky|difficult|hard|complex|impossible|challenging|not\s+easy)"
    r"|it\s+is\s+(?:tricky|difficult|hard|complex|impossible|challenging)"
    r"|predicting|prever|there\s+is\s+no\s+single|there'?s\s+no\s+single"
    r"|no\s+single\s+company"
    r"|[ée]\s+importante\s+(?:notar|destacar|ressaltar|considerar)"
    r"|it'?s\s+important\s+to\s+note"
)
_PREAMBLE_SELFREF = (
    r"as\s+an?\s+(?:large\s+)?(?:language\s+model|ai\b|artificial\s+intelligence)"
    r"|como\s+(?:um|uma)\s+(?:modelo\s+de\s+linguagem|ia\b"
    r"|intelig[êe]ncia\s+artificial)"
)

PREAMBLE_PATTERN = (
    r"^\W*(?:" + _PREAMBLE_GREETING + "|" + _PREAMBLE_HEDGE + "|"
    + _PREAMBLE_SELFREF + ")"
)
PREAMBLE_RE = re.compile(PREAMBLE_PATTERN, re.IGNORECASE)


def opens_with_preamble(text: str) -> bool:
    return bool(PREAMBLE_RE.search(text or ""))


# ---------------------------------------------------------------------------
# Refusal marker (Table 10) — reproduced verbatim from VERIFICATION.md 5.3
# ---------------------------------------------------------------------------

REFUSAL_PT = re.compile(
    r"n[ãa]o (tenho|encontrei|há|ha|existe|consigo|possuo|disponho|localizei)"
    r"|desconhe|sem informa|n[ãa]o (é|e) (uma|um) (empresa|institui)"
    r"|fict[íi]cia|n[ãa]o consta|nenhuma informa|n[ãa]o reconhe", re.I)
REFUSAL_EN = re.compile(
    r"i (don't|do not|couldn't|could not|cannot|can't) (have|find|know|locate)"
    r"|no (information|record|data|publicly)|not aware"
    r"|does not (appear|seem) to exist|fictional|unable to find"
    r"|i'm not familiar|no verifiable", re.I)


def has_refusal_marker(text: str) -> bool:
    return bool(REFUSAL_PT.search(text) or REFUSAL_EN.search(text))


# ---------------------------------------------------------------------------
# Small statistics used in more than one table
# ---------------------------------------------------------------------------

def median(values: list[float]) -> float:
    if not values:
        return float("nan")
    s = sorted(values)
    mid = len(s) // 2
    return s[mid] if len(s) % 2 else (s[mid - 1] + s[mid]) / 2.0


def ols_slope(xs: list[float], ys: list[float]) -> tuple[float, float, float]:
    """Ordinary least squares slope of y on x, with a 95% interval.

    Returns (slope, lo, hi). The interval uses the residual standard error and
    a normal quantile; with fewer than three points it is undefined and NaN is
    returned. This is a description of the observed daily series, not a test:
    the daily rates are neither independent nor identically distributed across
    the collection gaps, so the interval has no confirmatory reading.
    """
    n = len(xs)
    if n < 3:
        return (float("nan"), float("nan"), float("nan"))
    mx = sum(xs) / n
    my = sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    if sxx == 0:
        return (float("nan"), float("nan"), float("nan"))
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx
    a = my - b * mx
    resid = [y - (a + b * x) for x, y in zip(xs, ys)]
    dof = n - 2
    s2 = sum(r * r for r in resid) / dof
    se = math.sqrt(s2 / sxx)
    z = 1.959963984540054
    return (b, b - z * se, b + z * se)


def exact_binomial_two_sided(b: int, c: int) -> float:
    """Two-sided exact binomial p-value for b successes out of b+c at p = 0.5.

    This is the exact form of McNemar's test, used for the paired window
    comparison in Table 13 where the discordant counts are small.
    """
    n = b + c
    if n == 0:
        return float("nan")
    k = min(b, c)
    tail = sum(math.comb(n, i) for i in range(0, k + 1)) / (2 ** n)
    return min(1.0, 2 * tail)
