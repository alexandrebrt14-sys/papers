# S5. The observation window as a curve: sensitivity, recovery, and the validity of the measure

Produced by `s5_window_validity.py` in this directory. Every figure below is written by that script to `./data/`; no number in this file was computed by hand. The database was opened read-only.

Snapshot: `MAX(citations.timestamp) = 2026-09-08T19:30:57Z`. Full-text cohort: 2,225 canonical observations (`COALESCE(is_probe,0)=0`, `response_full_text` non-null and non-empty), five engines, four verticals, 192 canonical queries, collected 2026-09-06 to 2026-09-08. Long series used in S5.6b: 68,624 canonical observations over 53 collection days, 2026-04-23 to 2026-09-08.

---

## 1. What this section adds to the manuscript

Manuscript v1.0 reports the observation window as a single contrast on a single arm: Perplexity at 75.7 per cent as collected against 51.9 per cent under a uniform 200-character window, a difference of 23.8 percentage points. That number carries a general claim about parameter P1 on the evidence of one engine, because five of six client adapters wrote `response_text = text[:200]` and the text past character 200 was never stored. Table 13 of `../tables/NUMBERS.md` extends the contrast to every active arm now that `response_full_text` is retained.

Six things remain unmeasured after Table 13, and this file measures them.

1. The window is a continuous parameter, and a two-point contrast cannot say where an adopter should set it. S5.1 reports the whole curve.
2. An adopter needs the inverse function: given a target recall of first mentions, which window delivers it. S5.2 reports that.
3. The manuscript restates the mechanism as hypothesis H6, that susceptibility follows response style rather than engine architecture. S5.3 tests it at three levels and reports a split verdict.
4. The N available for the symmetric test is 2,225, and the manuscript does not say what that N can and cannot support. S5.4 reports minimum detectable differences with an empirically measured design effect.
5. Parameter P6, the entity matching rule, is declared in the specification and never quantified. S5.5 quantifies it by re-running the same rows with the alias table off, the exclusion contexts off, both off, and the ambiguity guard off.
6. Nothing in the manuscript establishes that the measure is stable when the window is uniform. S5.6 splits the series by even and odd collection days and reports rate agreement, entity-ranking agreement and a typical error.

## 2. Method

**Matching rule.** The cohort comes from `src.config_v2.get_v2_cohort(vertical, include_anchors=True, include_decoys=True)` and the matching from `src.analysis.entity_extraction.EntityExtractor`, in the configuration `scripts/harmonize_citation_window.py` used to produce the manuscript's window table: the v2 cohort with international anchors and fictitious decoys (31 entities in fintech, 32 in each of retail, health and technology), and the project's `ENTITY_ALIASES`, `AMBIGUOUS_ENTITIES`, `CANONICAL_NAMES` and `ENTITY_STOP_CONTEXTS` dictionaries. The script imports those primitives, the Wilson interval and the preamble regular expression from `../tables/_common.py`, which is the module the published tables already use. Writing a second extractor would confound a change of rule with a change of window, which is the defect the paper reports.

**Identity checks.** Two checks run before anything is computed and both passed on all 2,225 rows.

| Check | Mismatches | Verdict |
|---|---:|---|
| `response_text` equals `response_full_text[:200]` | 0 | PASS |
| re-extraction of `response_full_text[:200]` equals stored `cited_v2` | 0 | PASS |

The first establishes that the two stored columns are two views of one response. The second establishes that this script's rule reproduces the rule that produced the series. Without both, no delta below is attributable to the window.

**Declared constants.** Coarse grid 50, 100, 150, 200, 300, 400, 600, 800, 1,200, 1,600 characters and the whole response. Fine grid for S5.2: 25 to 300 in steps of 25, 350 to 1,000 in steps of 50, 1,100 to 2,000 in steps of 100, then 2,250, 2,500, 3,000, 3,500, 4,000 and 5,000. Saturation criterion: the narrowest grid window whose rate is within 1.0 percentage point of the whole-response rate and stays within it at every wider grid window. Bootstrap: 10,000 replicates, clusters resampled by query text, seed 20260911. Power targets: alpha 0.05, power 0.80. Cells below n = 30 are descriptive only.

**Clustering.** Observations sharing a query are repeated measurements of the same prompt across collection days. Every interval and every standard error below resamples or clusters by query. ChatGPT and Claude contribute one observation per query, so the correction is inert on those arms by construction. Gemini and Grok contribute four, Perplexity three or four.

---

## 3. S5.1 The sensitivity curve

**Table S5.1.** Citation rate by observation window, recomputed over the identical observation set with the matching rule held fixed. Series 2026-09-06 to 2026-09-08, 2,225 canonical observations, denominator is all canonical observations of that engine retaining a full response.

| Engine | n | 50 | 100 | 150 | 200 | 300 | 400 | 600 | 800 | 1,200 | 1,600 | Full |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ChatGPT | 192 | 1.0 | 3.6 | 11.5 | 17.2 | 35.9 | 41.7 | 45.8 | 47.9 | 51.0 | 52.6 | 53.6 |
| Claude | 192 | 0.5 | 5.2 | 14.6 | 25.0 | 43.8 | 52.6 | 58.3 | 62.0 | 65.6 | 66.1 | 66.1 |
| Gemini | 768 | 0.3 | 1.6 | 2.3 | 2.6 | 4.8 | 10.4 | 17.1 | 18.5 | 21.6 | 26.0 | 33.3 |
| Grok | 768 | 17.7 | 21.4 | 24.5 | 28.4 | 39.6 | 50.1 | 61.3 | 67.6 | 75.4 | 79.0 | 84.1 |
| Perplexity | 305 | 14.1 | 29.5 | 43.6 | 54.1 | 64.6 | 72.1 | 75.4 | 76.7 | 77.0 | 77.0 | 77.0 |

Rates in percentage points. Wilson intervals for every cell are in `data/s5_window_curve_by_engine.csv`, together with the gap to the whole-response rate at each window.

The ordering of engines is not stable across the curve. At 50 characters Grok leads at 17.7 per cent and Perplexity follows at 14.1; at 200 characters Perplexity leads at 54.1 and Grok sits at 28.4; on the whole response Grok leads at 84.1 and Perplexity has fallen to fourth. A ranking of engines by citation rate is therefore a statement about the window, and a published ranking that does not declare its window is not interpretable.

**Table S5.2.** The 200-character contrast: rate at the canonical window against rate on the whole response, same rows, paired. Series 2026-09-06 to 2026-09-08, 2,225 canonical observations, denominator is the engine's own observations. Intervals are 10,000-replicate bootstrap percentiles with query clusters resampled; McNemar is the exact two-sided binomial on the discordant pairs.

| Engine | n | Rate at 200 [95% CI] | Rate on full [95% CI] | Δ pp | Bootstrap 95% CI | Gains | Losses | Exact McNemar p | Design effect | Saturation |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ChatGPT | 192 | 17.19 [12.51, 23.15] | 53.65 [46.59, 60.56] | +36.46 | [29.7, 43.2] | 70 | 0 | 1.69e-21 | 0.99 | full |
| Claude | 192 | 25.00 [19.41, 31.57] | 66.15 [59.19, 72.46] | +41.15 | [34.4, 47.9] | 79 | 0 | 3.31e-24 | 0.99 | 1,200 |
| Gemini | 768 | 2.60 [1.69, 3.99] | 33.33 [30.09, 36.74] | +30.73 | [27.3, 34.0] | 236 | 0 | 1.81e-71 | 1.05 | full |
| Grok | 768 | 28.39 [25.31, 31.68] | 84.11 [81.36, 86.53] | +55.73 | [50.1, 61.6] | 428 | 0 | 2.89e-129 | 2.71 | full |
| Perplexity | 305 | 54.10 [48.49, 59.61] | 77.05 [72.01, 81.41] | +22.95 | [16.8, 29.6] | 70 | 0 | 1.69e-21 | 1.83 | 800 |

The design effect is the squared ratio of the query-clustered bootstrap standard deviation of the paired difference to its independence-assuming standard error, `sqrt(b + c - (b - c)^2 / n) / n`. ChatGPT and Claude sit at 0.99 because each query is observed once. Grok at 2.71 and Perplexity at 1.83 repeat the same prompt across days and pay for it. Gemini repeats prompts as often as Grok and still sits at 1.05, because its two long-response days differ so sharply from 2026-09-06 that variation between repeats of one query is not much smaller than variation between queries.

Losses are zero on every arm: no observation classified as citing at 200 characters loses that classification on the whole response. The effect is one-directional, which is why the exact McNemar p-values are extreme, and it means the 200-character rate is a lower bound on the whole-response rate at the observation level and not only in aggregate.

The manuscript's single-arm figure of 23.8 percentage points is the smallest of the five deltas measured here. Perplexity is the arm least damaged by the narrow window, and the paper's headline number therefore understates the parameter's influence on the panel it was drawn from.

**Saturation.** Under the declared one-point criterion, only Perplexity saturates inside the grid at a window an adopter would call short (800 characters), and Claude at 1,200. ChatGPT, Gemini and Grok do not saturate below the whole response. Gemini's rate is still climbing between 1,600 characters and the whole response, by 7.3 points.

### 3.1 The subset the window can bind on

An observation whose stored response is 200 characters or shorter cannot move between the two windows: both see the same string. Such rows are real observations and they belong in the pooled rate, but they dilute the delta by an amount that depends on which day an arm happened to be collected. Gemini contributes 378 of them from 2026-09-06 alone, a day on which the API returned responses that were themselves cut mid-sentence at a mean of 143 characters.

**Table S5.3.** The same contrast restricted to observations longer than the canonical window, with the recovery quantiles of S5.2 recomputed on that subset. Series 2026-09-06 to 2026-09-08, 1,846 canonical observations longer than 200 characters, denominator is the engine's own observations in the subset.

| Engine | n > 200 | Dropped | Rate at 200 | Rate on full | Δ pp | Median full length | w50 | w80 | w90 | w95 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ChatGPT | 192 | 0 | 17.19 | 53.65 | +36.46 | 1,894 | 275 | 500 | 850 | 1,100 |
| Claude | 192 | 0 | 25.00 | 66.15 | +41.15 | 1,130 | 275 | 450 | 700 | 850 |
| Gemini | 390 | 378 | 3.59 | 64.10 | +60.51 | 3,423 | 600 | 1,700 | 2,250 | 2,500 |
| Grok | 767 | 1 | 28.29 | 84.09 | +55.80 | 1,993 | 350 | 800 | 1,300 | 1,800 |
| Perplexity | 305 | 0 | 54.10 | 77.05 | +22.95 | 528 | 150 | 275 | 400 | 450 |

Three arms are unaffected by the restriction. Gemini's delta nearly doubles, from 30.73 to 60.51 percentage points, and its median stored length rises from 452 to 3,423 characters. The pooled Gemini row of Table S5.2 describes a mixture of two collection regimes rather than an engine.

**Table S5.4.** The full-text cohort by collection day, which is where the restriction comes from. Series 2026-09-06 to 2026-09-08, 2,225 canonical observations, denominator is the engine-day cell.

| Engine | Day | n | Mean full length | Rows ≤ 200 chars | Rate at 200 | Rate on full | Δ pp |
|---|---|---:|---:|---:|---:|---:|---:|
| ChatGPT | 2026-09-08 | 192 | 1,895 | 0 | 17.2 | 53.6 | +36.5 |
| Claude | 2026-09-08 | 192 | 1,194 | 0 | 25.0 | 66.1 | +41.1 |
| Gemini | 2026-09-06 | 384 | 143 | 378 | 1.6 | 1.6 | +0.0 |
| Gemini | 2026-09-07 | 96 | 3,540 | 0 | 7.3 | 67.7 | +60.4 |
| Gemini | 2026-09-08 | 288 | 3,684 | 0 | 2.4 | 64.2 | +61.8 |
| Grok | 2026-09-06 | 384 | 2,013 | 1 | 27.9 | 83.9 | +56.0 |
| Grok | 2026-09-07 | 96 | 2,014 | 0 | 51.0 | 92.7 | +41.7 |
| Grok | 2026-09-08 | 288 | 2,017 | 0 | 21.5 | 81.6 | +60.1 |
| Perplexity | 2026-09-06 | 192 | 555 | 0 | 54.2 | 74.5 | +20.3 |
| Perplexity | 2026-09-07 | 17 | 536 | 0 | 82.4 | 94.1 | +11.8 |
| Perplexity | 2026-09-08 | 96 | 562 | 0 | 49.0 | 79.2 | +30.2 |

The Gemini row for 2026-09-06 shows a delta of exactly zero on 384 observations. That is the signature of a retention defect rather than of an engine that names entities early: a column called `response_full_text` held a string that was not the full response. Full-response retention became effective for Gemini on 2026-09-07.

### 3.2 The other end of the response is censored too

The window analysis assumes that the column named `response_full_text` holds a complete response. A response whose last non-space character is not terminal punctuation was cut somewhere, by the generation cap or by the storage path, and its whole-response rate is a lower bound.

**Table S5.5.** Censoring diagnostic: stored responses that end without terminal punctuation. Criterion `[.!?:;\)\]"”»’'*_]\s*$` applied to `response_full_text`, published in `s5_window_validity.py` as `TERMINAL_RE`. Series 2026-09-06 to 2026-09-08, 2,225 canonical observations, denominator is the engine's own observations.

| Engine | n | Ends mid-sentence | Share | 95th percentile length | Max length |
|---|---:|---:|---:|---:|---:|
| ChatGPT | 192 | 0 | 0.0% | 3,688 | 4,088 |
| Claude | 192 | 2 | 1.0% | 1,728 | 3,072 |
| Gemini | 768 | 648 | 84.4% | 4,085 | 19,777 |
| Grok | 768 | 70 | 9.1% | 3,698 | 4,263 |
| Perplexity | 305 | 1 | 0.3% | 848 | 1,032 |

The criterion is crude: it calls a response ending in a bare bullet item incomplete. It is reported as a diagnostic and is never used to filter a rate. Even allowing for that, the Gemini figure of 84.4 per cent is too large to be an artifact of list formatting, and it is consistent with the tails observed directly, which end mid-word. Gemini's whole-response rate is a lower bound, its window delta is a lower bound, and its recovery quantiles in Table S5.6 are longer than reported rather than shorter. Grok carries the same bias at one tenth the frequency. The three remaining arms are effectively uncensored.

---

## 4. S5.2 The mention recovery curve

The question an adopter asks is the inverse of Table S5.1. Given a tolerance for missed mentions, how wide must the window be. The quantity reported is the narrowest window from which an observation is classified as citing and stays so at every wider grid window, computed only on observations that are cited on the whole response.

The monotone envelope is used because the rule is not monotone in principle: an exclusion context reaches thirty characters past a match, so widening the window can in principle remove a match a narrower window kept. On these 2,225 observations that never happened; the script reports zero non-monotone observations and zero observations whose first mention lies beyond the 5,000-character grid.

**Table S5.6.** Window required to recover a given fraction of the first mentions. Series 2026-09-06 to 2026-09-08, 1,367 canonical observations cited on the whole response, denominator is the engine's own cited-on-full observations.

| Engine | Cited on full | w50 | w80 | w90 | w95 | Median first-mention offset |
|---|---:|---:|---:|---:|---:|---:|
| ChatGPT | 103 | 275 | 500 | 850 | 1,100 | 245 |
| Claude | 127 | 275 | 450 | 700 | 850 | 241 |
| Gemini | 256 | 600 | 1,700 | 2,250 | 2,500 | 550 |
| Grok | 646 | 350 | 800 | 1,300 | 1,800 | 312 |
| Perplexity | 235 | 150 | 275 | 400 | 450 | 114 |
| All | 1,367 | 300 | 750 | 1,400 | 1,900 | 284 |

**Table S5.7.** Cumulative recovery of first mentions by window, in per cent of the observations cited on the whole response. Series 2026-09-06 to 2026-09-08, 1,367 canonical observations, denominator is the engine's own cited-on-full observations. The complete 42-point curve is in `data/s5_mention_recovery_curve.csv`.

| Window | ChatGPT | Claude | Gemini | Grok | Perplexity | All |
|---:|---:|---:|---:|---:|---:|---:|
| 50 | 1.9 | 0.8 | 0.8 | 21.1 | 18.3 | 13.5 |
| 100 | 6.8 | 7.9 | 4.7 | 25.4 | 38.3 | 20.7 |
| 150 | 21.4 | 22.0 | 7.0 | 29.1 | 56.6 | 28.5 |
| 200 | 32.0 | 37.8 | 7.8 | 33.7 | 70.2 | 35.4 |
| 300 | 67.0 | 66.1 | 14.5 | 47.1 | 83.8 | 50.5 |
| 400 | 77.7 | 79.5 | 31.2 | 59.6 | 93.6 | 63.4 |
| 600 | 85.4 | 88.2 | 51.2 | 72.9 | 97.9 | 75.5 |
| 800 | 89.3 | 93.7 | 55.5 | 80.3 | 99.6 | 80.9 |
| 1,200 | 95.1 | 99.2 | 64.8 | 89.6 | 100.0 | 88.1 |
| 1,600 | 98.1 | 100.0 | 78.1 | 94.0 | 100.0 | 92.9 |
| 2,000 | 99.0 | 100.0 | 89.5 | 98.0 | 100.0 | 97.0 |

The canonical 200-character window recovers 35.4 per cent of the first mentions across the panel and between 7.8 and 70.2 per cent depending on the engine. No single window achieves 95 per cent recovery on every arm below 2,500 characters. An adopter who wants 90 per cent recovery on the worst arm in this panel needs 2,250 characters; one who wants 90 per cent on the panel as a whole needs 1,400.

The practical recommendation that follows from Table S5.7 is that the window should be reported as a recall target rather than as a character count, because the character count that meets a given target differs by an order of magnitude across engines.

### 4.1 Figure

**Figure S5.1.** Two panels, one row.

*Panel A, the sensitivity curve.* x: observation window in characters, log scale, ticks at 50, 100, 200, 400, 800, 1,600 and a separate right-hand category for the whole response. y: citation rate in per cent, 0 to 90. Five lines, one per engine, from `data/s5_window_curve_by_engine.csv` columns `window_chars` and `rate_pct`, with a shaded band from `ci_lo_pct` to `ci_hi_pct`. A vertical rule at x = 200 marks the canonical window. Line colours must be distinguishable in greyscale; label each line at its right-hand end rather than in a legend box.

*Panel B, the recovery curve.* x: window in characters, linear, 0 to 2,500. y: cumulative per cent of first mentions recovered, 0 to 100. Five lines from `data/s5_mention_recovery_curve.csv` columns `window_chars` and `recovery_pct`. Horizontal rules at 80 and 95 per cent. Drop lines from each curve's crossing of 95 per cent to the x-axis, annotated with the value from Table S5.6.

Both panels are generated from the CSVs alone and carry no number that is not in them.

---

## 5. S5.3 Preamble as a predictor, and the test of H6

H6 states that the gap between head-of-response and whole-response citation varies across engines and is predicted by preamble share rather than by engine class.

**Criterion.** A response opens with a preamble when `_common.PREAMBLE_RE` matches at its start. The pattern is anchored at `^\W*` and covers three families: praise or greeting directed at the question, a hedge on whether the question can be answered, and explicit model self-reference. It is published in full in `../tables/_common.py` and reproduced in `../tables/NUMBERS.md` T5, where it is also compared against the figures of manuscript v1.0 over the identical row set. It is a re-specification: the regular expression used for Table 7 of v1.0 was never committed and cannot be re-run.

**Table S5.8.** Preamble share and window damage by engine, with the two competing predictors. Series 2026-09-06 to 2026-09-08, 2,225 canonical observations, denominator is the engine's own observations. Median first-mention offset is computed on observations cited on the whole response.

| Engine | n | Preamble | Share [95% CI] | Δ 200→full pp | Median full length | Median first offset | Engine class |
|---|---:|---:|---:|---:|---:|---:|---|
| ChatGPT | 192 | 0 | 0.00 [0.00, 1.96] | +36.46 | 1,894 | 245 | parametric |
| Claude | 192 | 0 | 0.00 [0.00, 1.96] | +41.15 | 1,130 | 241 | parametric |
| Gemini | 768 | 280 | 36.46 [33.13, 39.92] | +30.73 | 452 | 550 | parametric |
| Grok | 768 | 74 | 9.64 [7.74, 11.93] | +55.73 | 1,991 | 312 | parametric |
| Perplexity | 305 | 14 | 4.59 [2.75, 7.56] | +22.95 | 528 | 114 | retrieval-augmented |

Across the five engines, Spearman correlation of preamble share with the delta is −0.154 (p = 0.805); of median response length with the delta, +0.800 (p = 0.104); of median first-mention offset with the delta, +0.300 (p = 0.624).

**Table S5.9.** The same, restricted to observations longer than the window, which removes the Gemini retention defect of 2026-09-06. Series 2026-09-06 to 2026-09-08, 1,846 canonical observations longer than 200 characters, denominator is the engine's own observations in the subset.

| Engine | n | Preamble share | Δ pp | Median full length | Median first offset |
|---|---:|---:|---:|---:|---:|
| ChatGPT | 192 | 0.00 | +36.46 | 1,894 | 245 |
| Claude | 192 | 0.00 | +41.15 | 1,130 | 241 |
| Gemini | 390 | 39.49 | +60.51 | 3,423 | 582 |
| Grok | 767 | 9.65 | +55.80 | 1,993 | 312 |
| Perplexity | 305 | 4.59 | +22.95 | 528 | 114 |

On the restricted set the Spearman correlation of preamble share with the delta rises to +0.667 (p = 0.219); median length reaches +0.900 (p = 0.037) and median first-mention offset also +0.900 (p = 0.037). With five engines these are five-point rank correlations and any of them is compatible with chance at conventional thresholds except the two at 0.900, which reach p = 0.037 only because a perfect five-point rank correlation is the extreme of a small discrete distribution.

**Table S5.10.** Cell-level regressions of the window delta on preamble share. Unit is the engine-by-vertical cell; 20 cells, each with n between 48 and 192, all at or above the descriptive-only threshold. Series 2026-09-06 to 2026-09-08, 2,225 canonical observations in 20 cells. Standard errors clustered by engine in the first two models and heteroskedasticity-robust in the two fixed-effect models, which already condition on engine.

| Model | Coefficient on preamble share (pp of delta per pp of share) | 95% CI | p |
|---|---:|---:|---:|
| Δ ~ preamble share | −0.048 | [−0.459, +0.363] | 0.819 |
| Δ ~ preamble share + mean log₁₀ length | +0.232 | [−0.164, +0.628] | 0.250 |
| Δ ~ preamble share + engine fixed effects | +1.018 | [+0.054, +1.981] | 0.038 |
| Δ ~ preamble share + mean log₁₀ length + engine fixed effects | +0.969 | [−0.212, +2.149] | 0.108 |

In the second model the length term carries +55.19 percentage points of delta per log₁₀ character (95 per cent CI [+25.63, +84.75], p = 2.53e-04). In the fourth model the length term is +36.55 with an interval spanning zero by a wide margin ([−306.05, +379.16], p = 0.834), because within an engine the verticals differ hardly at all in mean response length.

**Table S5.11.** Observation-level contrast. Among observations cited on the whole response, the 200-character window misses the citation at these rates. Series 2026-09-06 to 2026-09-08, 1,367 canonical observations cited on the whole response, denominator is the engine's own cited-on-full observations.

| Engine | Cited on full | With preamble | Without | Miss rate with preamble | Miss rate without | Risk difference pp | Fisher p |
|---|---:|---:|---:|---:|---:|---:|---:|
| ChatGPT | 103 | 0 | 103 | — | 68.0 | — | — |
| Claude | 127 | 0 | 127 | — | 62.2 | — | — |
| Gemini | 256 | 121 | 135 | 98.3 | 86.7 | +11.7 | 3.48e-04 |
| Grok | 646 | 74 | 572 | 91.9 | 62.9 | +29.0 | 8.20e-08 |
| Perplexity | 235 | 13 | 222 | 46.2 | 28.8 | +17.3 | 0.215 |

Logistic models on the same 1,367 observations, clustered by query:

| Model | Odds ratio for preamble | 95% CI | p | n |
|---|---:|---:|---:|---:|
| miss ~ preamble | 8.75 | [4.66, 16.41] | 1.45e-11 | 1,367 |
| miss ~ preamble + log₁₀ length | 6.91 | [3.74, 12.78] | 6.73e-10 | 1,367 |
| miss ~ preamble + log₁₀ length + engine fixed effects | 7.72 | [3.99, 14.94] | 1.29e-09 | 1,137 |

The length term in the second model carries an odds ratio of 32.24 per log₁₀ character ([18.40, 56.52], p = 7.27e-34). The third model is fitted on the three engines with within-engine variation in preamble, Gemini, Grok and Perplexity, because ChatGPT and Claude emit no preamble at all on this cohort and contribute no identifying variation.

**Mechanism.** Regressing log₁₀ of the first-mention offset on preamble, log₁₀ response length and engine fixed effects, clustered by query, over the 1,367 cited-on-full observations: the preamble coefficient is +0.424 ([+0.322, +0.526], p = 3.12e-16), meaning a response that opens with a preamble places its first cohort mention 2.66 times further into the text (95 per cent CI 2.10 to 3.36) than a response of the same length from the same engine. The length coefficient is +1.289 ([+0.998, +1.581], p = 4.27e-18).

### 5.1 Verdict on H6

The hypothesis has two halves and they do not survive together.

The half that survives is the negative one. Engine class does not order the damage. All four parametric arms sit between +30.7 and +55.7 percentage points, spanning the whole range, and the single retrieval-augmented arm sits at the bottom of that range at +23.0. A taxonomy with one engine in one of its classes cannot be tested, and on the evidence available the architectural account explains nothing the style account does not explain better.

The half that fails as stated is the positive one. Preamble share does not order the engines. It is uncorrelated with the delta on the pooled cohort (ρ = −0.154) and reaches only ρ = +0.667 with p = 0.219 once the Gemini retention defect is removed, while response length and first-mention offset both reach ρ = +0.900 on the same five points. In the cell-level model, preamble carries no coefficient distinguishable from zero until engine fixed effects absorb the between-engine variation, and the length term is the one that survives.

What preamble does predict, and predicts strongly, is damage within an engine. Holding engine and response length fixed, a response that opens with a preamble is roughly eight times more likely to have its first mention hidden past character 200, and it places that mention 2.66 times further into the text. Grok shows the pattern most clearly across verticals: its preamble share runs from 2.6 per cent in fintech to 16.7 per cent in technology, and its window delta runs from +35.4 to +72.9 percentage points over the same cells.

The proposition that should replace H6 is narrower and testable: the window delta is a function of how far into the response the first cohort mention falls, and preamble is one of at least two things that push it there, the other being sheer response length. Preamble is a within-engine predictor of individual susceptibility, and it is not the property that ranks engines.

---

## 6. S5.4 Power, and the limit of this N

**Table S5.12.** Minimum detectable difference at alpha 0.05 and power 0.80, by engine and by vertical. Series 2026-09-06 to 2026-09-08, 2,225 canonical observations, denominator is the stratum. The paired column is McNemar in its normal form at the observed discordance; the unpaired column is two independent proportions at the observed whole-response rate with n per group. Both are inflated by the square root of a design effect measured as the squared ratio of a query-clustered bootstrap standard error of the rate to the binomial standard error.

| Stratum | n | Queries | Rate on full | Discordant | Design effect | Effective n | MDE paired pp | MDE unpaired pp |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ChatGPT | 192 | 192 | 53.6 | 36.5 | 1.06 | 181 | 12.5 | 14.3 |
| Claude | 192 | 192 | 66.1 | 41.1 | 1.01 | 189 | 13.0 | 12.8 |
| Gemini | 768 | 192 | 33.3 | 30.7 | 1.06 | 726 | 5.8 | 7.1 |
| Grok | 768 | 192 | 84.1 | 55.7 | 3.01 | 255 | 13.1 | 8.5 |
| Perplexity | 305 | 96 | 77.0 | 23.0 | 2.66 | 115 | 12.5 | 14.4 |
| Fintech | 569 | 48 | 68.9 | 31.5 | 2.71 | 210 | 10.8 | 12.2 |
| Retail | 552 | 48 | 66.8 | 38.6 | 2.54 | 218 | 11.8 | 12.2 |
| Health | 552 | 48 | 53.1 | 41.7 | 4.35 | 127 | 16.0 | 17.4 |
| Technology | 552 | 48 | 56.7 | 47.3 | 3.39 | 163 | 15.1 | 15.1 |
| All engines | 2,225 | 192 | 61.4 | 39.7 | 3.49 | 638 | 7.0 | 7.6 |

Per-engine-by-vertical minimum detectable differences are in `data/s5_power_mde.csv`.

**What this N supports.** Every window effect in Table S5.2 is between two and nine times the minimum detectable difference for its arm, and the smallest of them, Perplexity at +23.0 points against a paired MDE of 12.5, clears the threshold with room. The claim that the window moves the citation rate on every active arm is established at this N, and it is established within the observation, which is the strongest form the comparison can take: the discordance is one-directional on all five arms with not a single reversal in 2,225 observations.

**What this N does not support.** Differences between engines in the size of the window effect are, with one exception, below what this N can resolve. The gap between ChatGPT at +36.5 and Claude at +41.1 is 4.7 points against paired MDEs of 12.5 and 13.0; the gap between Gemini and Grok on the restricted subset is 4.7 points against a similar threshold. Only the separation of Perplexity from Grok, 32.8 points, exceeds both arms' thresholds. Statements of the form "engine A is more window-sensitive than engine B" are not supported here except for that one pair.

Vertical strata are worse. Every vertical pools all five engines, so a vertical contrast is a comparison of mixtures whose composition differs, and the design effect in health reaches 4.35, cutting 552 observations to an effective 127 and pushing the minimum detectable difference to 16 points. No difference between verticals reported anywhere in this file should be read as a finding.

The binding constraint is not the number of observations but the number of independent prompts and days. The cohort rests on 192 canonical queries collected over three days, with ChatGPT and Claude contributing a single day each. Adding observations by repeating the same battery on more days raises n quickly and effective n slowly, and the design effects of 2.7 to 3.5 on the repeated arms are the measured price of that.

---

## 7. S5.5 Sensitivity to the matching rule: P6 quantified

BRGEO-1 parameter P6 declares the entity matching rule. The specification states what the rule is and never states how much the number depends on it. The same 2,225 rows were re-extracted under four variants of the rule alongside the canonical configuration, at both windows.

**Table S5.13.** Citation rate under variants of the matching rule, same rows, both windows. Series 2026-09-06 to 2026-09-08, 2,225 canonical observations, denominator is the engine's own observations. Deltas are against the canonical configuration; flips are observations whose binary classification changes.

| Variant | Scope | Rate at 200 | Rate on full | Δ at 200 pp | Δ on full pp | Flips at 200 | Flips on full |
|---|---|---:|---:|---:|---:|---:|---:|
| canonical | All | 21.75 | 61.44 | — | — | — | — |
| no aliases | All | 20.81 | 60.67 | −0.94 | −0.76 | 21 | 17 |
| no exclusion contexts | All | 21.75 | 61.44 | 0.00 | 0.00 | 0 | 0 |
| neither | All | 20.81 | 60.67 | −0.94 | −0.76 | 21 | 17 |
| no ambiguity guard | All | 21.80 | 61.48 | +0.04 | +0.04 | 1 | 1 |
| no aliases | ChatGPT | 17.19 | 53.65 | 0.00 | 0.00 | 0 | 0 |
| no aliases | Claude | 25.00 | 66.15 | 0.00 | 0.00 | 0 | 0 |
| no aliases | Gemini | 2.60 | 33.33 | 0.00 | 0.00 | 0 | 0 |
| no aliases | Grok | 27.73 | 83.72 | −0.65 | −0.39 | 5 | 3 |
| no aliases | Perplexity | 48.85 | 72.46 | −5.25 | −4.59 | 16 | 14 |
| no ambiguity guard | Claude | 25.52 | 66.67 | +0.52 | +0.52 | 1 | 1 |

Rows not shown are zero-delta. The complete matrix of five variants by six scopes at both windows is in `data/s5_matching_rule_sensitivity.csv`.

**Table S5.14.** How much of the rule binds on the v2 cohort. Counted as cohort entities reached by each dictionary, by vertical.

| Vertical | Cohort size | Entities with an alias | Alias surfaces | Ambiguous entities | Entities with an exclusion context |
|---|---:|---:|---:|---:|---:|
| Fintech | 31 | 5 | 9 | 0 | 0 |
| Retail | 32 | 3 | 7 | 1 | 1 |
| Health | 32 | 6 | 9 | 0 | 0 |
| Technology | 32 | 2 | 4 | 0 | 0 |

Three results follow.

The alias table is the only component of the rule that moves the number, and it moves it by less than one percentage point on the panel. Removing it costs 0.94 points at 200 characters and 0.76 on the whole response, flipping 21 and 17 observations out of 2,225.

The effect is concentrated on one arm. Perplexity loses 5.25 points at 200 characters and 4.59 on the whole response; Grok loses under one point; ChatGPT, Claude and Gemini lose nothing at all. The reason is visible in the data: aliases such as BTG, XP, C6, Magalu, EMS and Hypera are short forms that a retrieval-augmented answer reproduces from its sources, and the parametric arms in this cohort write the canonical long names.

The exclusion contexts move nothing. Zero flips, zero delta, on every arm at both windows. Table S5.14 explains why: exactly one cohort entity in the entire v2 cohort carries an exclusion context, the retail anchor Amazon, and its three patterns (`floresta amaz[oô]nica`, `rio amazonas`, `amazon rainforest`) never fired on these 2,225 responses. The ambiguity guard is nearly as inert, moving a single observation, because the v2 cohort was rebuilt with canonical long names (Stone Co, Banco Inter, Banco Neon, Amazon Brasil) and the guard has almost nothing left to protect.

The reading for the specification is that P6's declared components are not equally consequential and that their consequence is a property of the cohort, not of the rule. A cohort of canonical long names makes the ambiguity machinery inert and leaves the alias table as the only lever. An adopter whose cohort contains short or colliding names should expect the opposite distribution and should publish this same sensitivity rather than assume it transfers. The number to publish alongside a conformance claim is the one in Table S5.13: the rate under the rule and the rate with each dictionary removed.

One artifact of the cohort deserves recording. The retail cohort contains both the real entity `Amazon Brasil` and the international anchor `Amazon`, and the ambiguity guard maps the anchor's surface to `Amazon Brasil`, so a single occurrence of the string satisfies two cohort entries. This inflates `cited_count` in retail without affecting the binary `cited`, which is the quantity every rate in this file reports.

---

## 8. S5.6 Reliability of the measure

### 8.1 The full-text cohort cannot answer the question

**Table S5.15.** Even-numbered against odd-numbered collection days on the full-text cohort. Series 2026-09-06 to 2026-09-08, 2,225 canonical observations, denominator is the engine-half cell.

| Engine | n even | Rate 200, even | Rate full, even | n odd | Rate 200, odd | Rate full, odd | Splittable |
|---|---:|---:|---:|---:|---:|---:|---|
| ChatGPT | 192 | 17.2 | 53.6 | 0 | — | — | no |
| Claude | 192 | 25.0 | 66.1 | 0 | — | — | no |
| Gemini | 672 | 1.9 | 28.4 | 96 | 7.3 | 67.7 | yes |
| Grok | 672 | 25.1 | 82.9 | 96 | 51.0 | 92.7 | yes |
| Perplexity | 288 | 52.4 | 76.0 | 17 | 82.4 | 94.1 | yes |

This table is reported because it was asked for, and it should not be read as a reliability estimate. The full-text cohort spans three days. The odd half is a single day, 2026-09-07, holding 96, 96 and 17 observations for three arms and none for the other two. The even half pools 2026-09-06, on which Gemini's stored responses were cut at 143 characters, with 2026-09-08, on which they ran to 3,684. The even-odd contrast on this cohort measures the change in collection regime, and it has no reading as instrument stability.

### 8.2 The five-month series can

The long series answers the question, under a window that is the same on every arm. `response_text` was re-cut at 200 characters and re-extracted for all 68,624 canonical observations rather than read from `cited_v2`, because for Perplexity before 2026-08-31 the stored string runs past the window and the stored flag is not a uniform-window measurement.

**Table S5.16.** Citation rate on even-numbered against odd-numbered collection days, uniform 200-character window. Series 2026-04-23 to 2026-09-08, 68,624 canonical observations over 53 collection days, denominator is the engine-half cell. Fisher exact, two-sided.

| Engine | n even | Days | Rate even | n odd | Days | Rate odd | Difference pp | Fisher p |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ChatGPT | 7,759 | 25 | 16.99 | 7,409 | 26 | 17.36 | −0.37 | 0.547 |
| Claude | 7,709 | 25 | 25.42 | 7,325 | 26 | 26.09 | −0.66 | 0.361 |
| Gemini | 8,236 | 26 | 1.77 | 7,119 | 26 | 1.95 | −0.18 | 0.436 |
| Groq | 7,564 | 24 | 8.67 | 6,644 | 24 | 8.34 | +0.33 | 0.489 |
| Perplexity | 4,062 | 26 | 51.94 | 3,679 | 27 | 52.13 | −0.19 | 0.873 |
| Grok† | 672 | 2 | 25.15 | 446 | 3 | 36.32 | −11.17 | 7.70e-05 |

† Grok entered the panel on 2026-08-23 and contributes five collection days. Its halves are two days against three, and the difference is a between-day difference rather than an instability of the instrument. The daily Grok rates in Table S5.4 vary from 21.5 to 51.0 per cent at the 200-character window within a single week.

Five of the six arms agree between halves to within 0.7 percentage points, none of them significantly.

**Table S5.17.** Agreement of cell rates between halves. Unit is the engine-by-vertical-by-language-by-query-type cell with at least 30 observations in each half; 88 cells. Series 2026-04-23 to 2026-09-08, 68,624 canonical observations, denominator is the cell-half.

| Quantity | Value |
|---|---:|
| Pearson r, even against odd | 0.9923 |
| Spearman ρ | 0.9933 |
| Spearman-Brown stepped-up reliability | 0.9961 |
| Typical error, SD of the difference divided by √2 | 2.39 pp |

**Table S5.18.** Agreement of the entity ranking between halves. Rank correlation over the union of entities appearing as a first mention in either half, and overlap of the two top-ten lists. Series 2026-04-23 to 2026-09-08, 68,624 canonical observations, denominator is the engine.

| Engine | Entities in union | Spearman ρ | p | Top-ten overlap |
|---|---:|---:|---:|---:|
| ChatGPT | 11 | 0.961 | 2.47e-06 | 100% |
| Claude | 17 | 0.978 | 1.33e-11 | 100% |
| Gemini | 6 | 0.943 | 0.005 | 100% |
| Grok | 13 | 0.935 | 2.73e-06 | 100% |
| Groq | 9 | 0.996 | 1.54e-08 | 100% |
| Perplexity | 37 | 0.855 | 1.69e-11 | 100% |

Under a uniform window the measure is stable. Rates reproduce across independent halves of the series to a typical error of 2.39 percentage points, and the entity ranking reproduces with rank correlations from 0.855 to 0.996 and complete overlap of the top ten on every arm. That stability is what makes the window result interpretable: a 23 to 56 point movement produced by changing the window is ten to twenty-three times the measurement noise of the instrument at a fixed window.

---

## 9. What this establishes

1. The observation window moves the citation rate on every active arm, by +22.95 to +55.73 percentage points between 200 characters and the whole response, with zero reversals in 2,225 observations and exact McNemar p-values from 1.69e-21 to 2.89e-129. The manuscript's single-arm figure of 23.8 points is the smallest effect in the panel.
2. The relationship is a curve with no common saturation point. Perplexity saturates at 800 characters and Claude at 1,200; ChatGPT, Gemini and Grok are still rising at 1,600.
3. The ranking of engines by citation rate changes with the window. A published rate without a declared window is not comparable to any other published rate.
4. The 200-character window recovers 35.4 per cent of first mentions across the panel, from 7.8 per cent on Gemini to 70.2 per cent on Perplexity. Ninety-five per cent recovery requires 450 characters on Perplexity and 2,500 on Gemini.
5. H6 splits. Engine class does not order the damage. Preamble share does not order it either; response length and first-mention offset do. Preamble predicts susceptibility within an engine, at an odds ratio near eight with engine and length held fixed.
6. Of the matching rule's declared components, only the alias table moves the number on this cohort, by 0.94 points overall and 5.25 points on Perplexity. The exclusion contexts move nothing, and the ambiguity guard moves one observation, because the v2 cohort was rebuilt with canonical long names.
7. Under a uniform window the instrument is stable: 2.39 percentage points of typical error across 88 cells and two independent halves of a 53-day series, with entity rankings reproducing at ρ = 0.855 to 0.996.

## 10. What this does not establish

**It does not establish a mechanism.** Preamble, length and offset are three descriptions of the same text measured after the fact. Nothing here manipulates an engine's response style and observes the window effect change, and the observational association is compatible with a third property, such as the prompt's difficulty, producing longer answers, more hedging and later naming at once.

**It does not establish that engines differ in window sensitivity.** With one exception (Perplexity against Grok) every between-engine difference in the delta is smaller than the minimum detectable difference of the arms being compared, which runs from 5.8 to 13.1 percentage points. The apparent ordering in Table S5.2 is not resolvable at this N.

**It does not establish anything about verticals.** Every vertical stratum pools five engines in a composition that differs by vertical, and the design effect reaches 4.35 in health. The vertical columns of `data/s5_window_curve_by_engine_vertical.csv` are published for reproduction and should not be read as a vertical result.

**It does not establish the whole-response rate for Gemini.** Gemini's stored responses on 2026-09-07 and 2026-09-08 end mid-word at a mean of 3,540 and 3,684 characters, which is a generation cap rather than a completed answer. The Gemini whole-response rate of 64.10 per cent on the restricted subset is a lower bound, and its recovery quantiles in Table S5.6 are a lower bound in the same direction. The same applies to Grok at one tenth the frequency, 9.1 per cent of responses (Table S5.5).

**It does not generalise across time.** The full-text cohort is three consecutive days in September 2026 on pinned model versions. Table S5.4 shows Grok's 200-character rate moving from 27.9 to 51.0 to 21.5 per cent across those three days, which is larger than several of the between-engine differences the paper might be tempted to draw from Table S5.2.

**It does not transfer the P6 result to another cohort.** Table S5.14 shows that the exclusion contexts are inert here because one cohort entity carries one, and that the ambiguity guard is inert because the cohort was rebuilt with long names. A cohort containing Stone, Inter, Neon or 99 as bare surfaces would produce entirely different numbers in Table S5.13, in the opposite direction.

**It does not validate the preamble criterion.** The regular expression is a re-specification of a criterion described in prose in manuscript v1.0 and never committed, and `../tables/NUMBERS.md` T5 documents where the two disagree by up to 5.2 percentage points on individual arms. Every preamble figure in S5.3 inherits that uncertainty. Gemini's preamble share on this three-day cohort is 36.46 per cent against 80.03 per cent on the full series under the same pattern, which is a difference between periods and not a difference between criteria, and it is another reason the engine-level H6 test on five points should not be treated as decisive.

**It does not measure agreement against human judgment.** Every number here is one automated rule compared with itself under different settings. Whether the rule's binary `cited` corresponds to what a reader would call a citation is the question `src/analysis/kappa_validator.py` addresses and this file does not.

---

## 11. Reproduction

```bash
cd docs/research/methods-paper/journal-v2/stats
python s5_window_validity.py                 # full run, about 4 minutes
python s5_window_validity.py --quick         # 1,000 bootstrap replicates, skips S5.6b
```

Exit status is 0 when both identity checks pass and 1 otherwise. Outputs, all written to `./data/`:

| File | Contents |
|---|---|
| `s5_window_curve_by_engine.csv` | Table S5.1 with Wilson intervals at every grid point; Figure S5.1 panel A |
| `s5_window_contrast_200_vs_full.csv` | Table S5.2 |
| `s5_window_curve_by_engine_vertical.csv` | The curve by engine and vertical, descriptive only |
| `s5_window_contrast_restricted.csv` | Table S5.3 |
| `s5_window_by_day.csv` | Table S5.4 |
| `s5_response_censoring.csv` | Table S5.5 |
| `s5_mention_recovery_curve.csv` | Table S5.7 at 42 grid points; Figure S5.1 panel B |
| `s5_mention_recovery_quantiles.csv` | Table S5.6 |
| `s5_preamble_by_engine.csv`, `s5_preamble_by_engine_restricted.csv` | Tables S5.8 and S5.9 |
| `s5_preamble_by_cell.csv`, `s5_preamble_model_cells.csv` | Inputs to Table S5.10 |
| `s5_preamble_observation_contrast.csv` | Table S5.11 |
| `s5_power_mde.csv` | Table S5.12, including engine-by-vertical cells |
| `s5_matching_rule_sensitivity.csv` | Table S5.13, complete matrix |
| `s5_reliability_fulltext_split.csv` | Table S5.15 |
| `s5_reliability_series_split.csv`, `s5_reliability_series_cells.csv` | Tables S5.16 and S5.17 |
| `s5_reliability_entity_rank.csv` | Table S5.18 |
| `s5_window_validity.json` | Every quantity above, including model coefficients not tabulated here |

Dependencies: numpy 2.4.3, pandas 3.0.1, scipy 1.17.1, statsmodels 0.14.6, patsy 1.0.2, Python 3.12.10.
