# S2 — Temporal stability of the BRGEO-1 citation series

**Analysis date.** 2026-09-11. **Script.** `s2_temporal.py` (this directory). **Machine-readable output.** `s2_results.json`. **Figure data.** `data/s2_*.csv`.

**Database.** `C:/Sandyboxclaude/papers/data/papers.db`, opened read-only, snapshot written 2026-09-08 19:34 UTC, 86,543 rows in `citations`. Nothing was written to the database at any point.

Every number below is produced by the script. Where an analysis could not be run, the table says so and the reason is given; nothing is reported as a result that did not execute.

---

## 1. Cut, outcome and the one preprocessing decision

**Canonical cut.** `COALESCE(is_probe,0) = 0`. That leaves 68,624 observations across six engine arms, 192 distinct prompts, four verticals, two languages and two query types, balanced to within 0.02 points on every design factor.

**Outcome.** Citation of a cohort entity inside a uniform 200-character observation window. The stored column `cited_v2` was not used directly, because it was computed over `citations.response_text`, and until 2026-08-31 that column held `text[:200]` in five arms and the whole response in Perplexity. The script therefore re-runs the project's own extractor (`src.analysis.entity_extraction.EntityExtractor`, same cohort, aliases, ambiguity list and stop contexts used by `scripts/harmonize_citation_window.py`) over `response_text[:200]` for every row. This reproduces the operation the project performs forward from 2026-08-31 and applies it backwards over the whole series, which is the only way to obtain a series measured through one aperture.

**Table 1. What the uniform window changes, arm by arm.** *Caption: `rate_stored` is the outcome as held in the database; `rate_win200` is the same extractor re-run over the first 200 characters. Source: `data/s2_window_reconciliation.csv`.*

| Arm | n | Stored rate (%) | Window-200 rate (%) | Δ (pp) | Mean stored length | Rows longer than the window |
|---|---:|---:|---:|---:|---:|---:|
| ChatGPT | 15,168 | 17.168 | 17.168 | 0.000 | 200.0 | 0 |
| Claude | 15,034 | 25.748 | 25.748 | 0.000 | 200.0 | 0 |
| Gemini | 15,355 | 1.856 | 1.856 | 0.000 | 195.7 | 0 |
| Grok | 1,118 | 29.606 | 29.606 | 0.000 | 200.0 | 0 |
| Groq | 14,208 | 8.516 | 8.516 | 0.000 | 200.0 | 0 |
| Perplexity | 7,741 | 74.874 | 52.035 | **−22.839** | 668.0 | 7,435 |

The 7,435 truncated rows match the count recorded in `governance/HEALTH-CHECK-COLETA-20260831.md:85-92` exactly, and the resulting Perplexity level of 52.03% sits on the documented 51.9% / 52.0%. The delta here is −22.84 pp rather than the documented −23.8 pp because the documented figure closes on 2026-08-31 over 66,399 observations and this one runs to 2026-09-08 over 68,624. The five zero deltas are the identity operation applied to a string already 200 characters long, which is a check on the harmonisation code and not independent evidence about those arms; the correction recorded at `MANUSCRIPT.md:243` applies here unchanged.

**Day definition.** A collection day is the local Brazilian date, UTC−3. Evening runs start at 21:00 UTC and finish after midnight UTC; assigning by UTC date would split a single run across two days. Under UTC−3 no run is split.

**Round definition.** Two crons: one at 06:00 BRT (09:00–19:00 UTC in practice) and one at 18:00 BRT (21:00–01:00 UTC). No observation falls between 17:00 and 18:00 BRT, so the split at 18:00 BRT separates the two rounds cleanly.

**Partial-day policy.** Nothing is imputed. Partial days stay in the primary cut, marked, and every headline quantity is recomputed on complete days only as a declared sensitivity (`data/s2_partial_day_sensitivity.csv`). The largest movement across the two cuts in any arm is 1.21 pp (Grok, whose complete-day cut has three days) and 0.30 pp in every other arm. A day is marked partial if it is declared partial in `docs/METHODOLOGY_V2.md:116-133` or `data/partial_days.json`, or if it empirically holds fewer than 20 engine-by-vertical cells or fewer than half the median daily volume.

---

## 2. The calendar, which governs everything that follows

**Table 2. Coverage of the analysed span.** *Caption: collected days against calendar days, and the five largest holes. Source: `data/s2_calendar_gaps.csv`, `s2_results.json:coverage`.*

| Quantity | Value |
|---|---:|
| First collected day | 2026-04-23 |
| Last collected day | 2026-09-08 |
| Calendar span | 139 days |
| Collected days | 52 |
| Calendar coverage | 37.4% |
| Largest hole | 59 days, 2026-06-10 to 2026-08-07 |
| Next four holes | 7 d (08-24 to 08-30), 6 d (08-17 to 08-22), 5 d (05-06 to 05-10), 5 d (09-01 to 09-05) |
| Days with both rounds | 24 of 52 |

Three consequences follow and none of them is optional.

The 59-day hole is recorded in `collection_runs` as 236 aborted runs with `records = 0` between 2026-06-10 and 2026-08-07 inclusive, which is the same 59-day gap recorded at commit `79b5021` and cited in the field log at T31. The itemised missingness ledger in `R3-fieldlog.md` §4.3 lists 2026-07-25, 2026-08-06 and 2026-08-09/10 as isolated one- and two-day balance gaps. Those entries describe a July in which collection otherwise ran. In the canonical database no observation exists on any day in July. The ledger and the data disagree, and the ledger's own §4.4 item 2 anticipates the problem by noting that no day-level cause is recorded for 2026-05-19 to 2026-07-24. The manuscript should either correct the July entries or state that they describe attempted runs rather than collected days.

The design is nominally twice daily. It was realised twice daily on 24 of 52 collected days, so "two rounds per day" describes 46% of the series.

The declared window of 90 days is a window of 90 *collected* days. At 52 collected days over 139 calendar days, a naive reading of the series as a four-and-a-half-month daily panel overstates its temporal density by a factor of 2.7.

**Table 3. The eight partial days.** *Caption: `cells` is the number of engine-by-vertical cells filled, out of 20. Source: `data/s2_daily_pooled.csv`.*

| Day | n | Rate (%) | Arms | Cells | Rounds | Declared | Empirical | Recorded cause |
|---|---:|---:|---:|---:|---:|:--:|:--:|---|
| 2026-04-23 | 795 | 18.87 | 5 | 19 | 1 | yes | yes | collection interrupted (`METHODOLOGY_V2.md:121`) |
| 2026-04-24 | 864 | 17.94 | 5 | 20 | 1 | yes | no | Anthropic balance mid-run, ~15 rows as `api_failure` |
| 2026-05-04 | 864 | 17.82 | 5 | 20 | 1 | yes | no | partial recovery (`METHODOLOGY_V2.md:125`) |
| 2026-05-18 | 864 | 17.71 | 5 | 20 | 1 | yes | no | Perplexity `max_tokens<16` rejected on `sonar` |
| **2026-06-05** | 1,344 | 20.91 | **4** | **16** | 1 | **no** | **yes** | not in any ledger |
| **2026-08-13** | 812 | 17.00 | 5 | **18** | 1 | **no** | **yes** | not in any ledger |
| 2026-09-06 | 960 | 22.60 | 3 | 12 | 1 | yes | yes | ChatGPT 429, Claude 400 (`partial_days.json`) |
| 2026-09-07 | 401 | 19.45 | 3 | 9 | 1 | yes | yes | idem |

Two days are empirically incomplete and appear in no ledger. 2026-06-05 is the day Gemini was removed from `MANDATORY_LLMS`, so the arm is simply absent; that absence is a declared *event* but not a declared *partial day*, and the two registers do not talk to each other. 2026-08-13 has 18 of 20 cells and no recorded cause at all. Conversely, three days the documentation calls partial (2026-04-24, 2026-05-04, 2026-05-18) are complete in cell terms, because the failures they describe consumed rows rather than cells. The ledger and the data are measuring two different things under one word.

---

## 3. Trend

**Method.** Three estimators per arm, on two cuts (all days, complete days only) and, for Gemini and Grok, on instrument-homogeneous segments. Theil-Sen regresses the daily rate on the calendar day index and reports the median pairwise slope with its distribution-free interval. Mann-Kendall is tie-corrected, and is reported twice: under the standard variance, and under the Hamed-Rao variance inflated by the autocorrelation of the de-trended ranks. The logistic model is fitted at observation level with the day index as the sole predictor and standard errors clustered on the collection day; the effect is converted to percentage points per 30 days by a 2,000-draw parametric bootstrap over the cluster-robust covariance. Benjamini-Hochberg runs over each family of p-values across the fifteen rows of the table.

**Table 4. Trend per arm.** *Caption: effect sizes in percentage points per 30 calendar days. `q` values are Benjamini-Hochberg. Source: `data/s2_trend.csv`.*

| Arm | Cut | Days | Rate (%) | Theil-Sen pp/30 d [95% CI] | MK τ | MK p | MK p (Hamed-Rao) | Logistic pp/30 d [95% CI] | Logistic p | Logistic q |
|---|---|---:|---:|---|---:|---:|---:|---|---:|---:|
| ChatGPT | all days | 50 | 17.17 | 0.00 [−0.07, +0.18] | 0.057 | 0.559 | 0.580 | −0.01 [−0.16, +0.13] | 0.858 | 0.858 |
| ChatGPT | complete | 44 | 17.17 | 0.00 [−0.09, +0.22] | 0.061 | 0.560 | 0.444 | −0.02 [−0.18, +0.13] | 0.777 | 0.848 |
| Claude | all days | 50 | 25.75 | 0.00 [−0.22, +0.12] | −0.037 | 0.710 | 0.564 | −0.12 [−0.34, +0.08] | 0.244 | 0.366 |
| Claude | complete | 44 | 25.68 | 0.00 [−0.17, +0.20] | 0.004 | 0.976 | 0.962 | −0.06 [−0.24, +0.12] | 0.482 | 0.579 |
| Gemini | all days | 51 | 1.86 | +0.49 [+0.31, +0.60] | 0.435 | 6.0e−6 | 0.010 | +0.41 [+0.30, +0.53] | 8.8e−14 | 2.6e−13 |
| Gemini | complete | 44 | 1.83 | +0.52 [+0.36, +0.65] | 0.457 | 1.1e−5 | 0.011 | +0.45 [+0.36, +0.54] | 5.4e−21 | 2.2e−20 |
| Gemini | pre 2026-06-17 (`2.5-pro`) | 38 | 1.41 | +0.03 [0.00, +0.58] | 0.135 | 0.231 | 0.349 | +0.33 [+0.03, +0.69] | 0.046 | 0.079 |
| Gemini | post 2026-06-17 (`2.5-flash`) | 13 | 2.97 | 0.00 [−1.74, +1.12] | 0.026 | 0.950 | 0.938 | −0.81 [−2.15, +0.76] | 0.296 | 0.395 |
| Perplexity | all days | 52 | 52.03 | −1.81 [−3.91, −0.44] | −0.249 | 0.009 | 0.113 | −0.89 [−1.68, −0.10] | 0.026 | 0.051 |
| Perplexity | complete | 44 | 51.74 | −2.37 [−4.69, −0.76] | −0.319 | 0.002 | 0.039 | −1.21 [−2.04, −0.37] | 0.005 | 0.012 |
| Groq | all days | 47 | 8.52 | +0.38 [0.00, +0.52] | 0.320 | 0.001 | 0.106 | +0.50 [+0.41, +0.59] | 2.6e−26 | 3.2e−25 |
| Groq | complete | 41 | 8.55 | +0.37 [0.00, +0.52] | 0.317 | 0.003 | 0.110 | +0.50 [+0.40, +0.60] | 1.3e−22 | 7.9e−22 |
| Grok | any cut | 5 | 29.61 | NOT RUN — fewer than 8 collected days | | | | | | |

Four readings.

ChatGPT and Claude show no trend by any estimator, and the Theil-Sen slope is exactly zero because the daily rate repeats the same value so often that the median pairwise slope is zero. On a 192-prompt battery re-asked twice a day, ChatGPT's daily rate sits between 16.7% and 17.9% for four and a half months. That stability is itself the most reportable property of those two arms.

Gemini's headline trend is a step, not a trend. The full-span slope of +0.49 pp per 30 days has p below 1e−5 and survives every correction, and it disappears entirely inside each segment (pre-boundary p = 0.23, post-boundary p = 0.95). What the full-span estimator is fitting is the level difference between `gemini-2.5-pro` at 1.41% and `gemini-2.5-flash` at 2.97%, spread across the calendar as though it were gradual. Any trend statement about Gemini that does not stratify on 2026-06-17 is a statement about the instrument.

Groq's trend has the same shape for the same reason. The full-span estimate is +0.50 pp per 30 days with p = 2.6e−26 under day-clustered logistic, and the change-point analysis below places the entire movement at the 59-day hole. Mann-Kendall corrected for autocorrelation puts it at p = 0.106. The gap between p = 0.001 and p = 0.106 for the same series is the whole argument of Section 5.

Perplexity is the only arm with a trend that survives the autocorrelation correction, and only on the complete-day cut: −2.37 pp per 30 days, Hamed-Rao p = 0.039, logistic q = 0.012. The direction is downward. It is not attributable to the window, because the window has been harmonised out of the series by construction.

---

## 4. Change points, detected blind, then confronted

**Method.** Detection never sees the event table. The primary detector is binary segmentation on the binomial likelihood: the split maximising the likelihood ratio between two binomial segments, with significance from a 999-permutation test that shuffles the order of the daily (successes, trials) pairs and so destroys temporal structure while preserving every day's size and rate. Minimum segment length three days, recursion to depth four, α = 0.05. `ruptures` 1.1.10 (PELT, `l2` cost on the logit of the daily rate, BIC-style penalty) runs afterwards as corroboration only.

**Table 5. Detected change points.** *Caption: a boundary is located between the last day of the earlier regime and the first day of the later one. Where those two days straddle a hole, the change point is located only to the width of the hole. Source: `data/s2_changepoints.csv`.*

| Arm | Detector | Boundary | Interval width | Rate before (%) | Rate after (%) | Δ (pp) | p (permutation) |
|---|---|---|---:|---:|---:|---:|---:|
| ChatGPT | binomial binseg | none at α = 0.05 | | | | | |
| Claude | binomial binseg | none at α = 0.05 | | | | | |
| Gemini | binomial binseg | 2026-06-04 → 2026-06-06 | 2 d | 1.29 | 2.80 | +1.50 | 0.001 |
| Perplexity | binomial binseg | 2026-05-24 → 2026-05-25 | 1 d | 56.49 | 48.62 | −7.87 | 0.001 |
| Perplexity | binomial binseg | 2026-05-27 → 2026-05-28 | 1 d | 41.41 | 47.17 | +5.77 | 0.008 |
| Perplexity | binomial binseg | 2026-08-08 → 2026-08-10 | 2 d | 46.25 | 51.49 | +5.24 | 0.001 |
| Groq | binomial binseg | 2026-06-09 → 2026-08-08 | **59 d** | 8.17 | 9.86 | +1.69 | 0.001 |
| Gemini | ruptures PELT | 2026-06-06 → 2026-06-07 | 1 d | 1.33 | 2.83 | | |
| Perplexity | ruptures PELT | 2026-05-20 → 2026-05-21 | 1 d | 57.11 | 49.34 | | |
| Groq | ruptures PELT | 2026-08-08 → 2026-08-10 | 2 d | 8.20 | 9.86 | | |

The two detectors agree on Gemini to within one day and on Groq's late-series level shift to within two. They disagree on where Perplexity's late-May decline begins, PELT placing it on 2026-05-20 and the binomial segmentation on 2026-05-24. That disagreement is informative: the Perplexity decline is a slope over four or five days rather than a step, and a step detector will locate it wherever its cost function prefers.

**Table 6. Confrontation with the declared event table.** *Caption: the twenty-one declared event-by-arm pairs from `R3-fieldlog.md` §3, matched against Table 5 with a tolerance of three calendar days. Minimum detectable difference is the shift a two-proportion test at 80% power would have found on the fourteen days either side of the boundary. Source: `data/s2_event_confrontation.csv`.*

| Declared event | Arm | Class | Verdict | Hole at the boundary | MDD at 80% power |
|---|---|---|---|---:|---:|
| 2026-04-30 | ChatGPT | battery | **no rupture** | 1 d | 3.7 pp |
| 2026-04-30 | Claude | battery | **no rupture** | 1 d | 4.3 pp |
| 2026-04-30 | Gemini | battery | **no rupture** | 1 d | 1.2 pp |
| 2026-04-30 | Perplexity | battery | **no rupture** | 1 d | 6.5 pp |
| 2026-04-30 | Groq | battery | **no rupture** | 1 d | 2.8 pp |
| 2026-06-05 | Gemini | generation configuration | **coincides** (distance 0 d, +1.50 pp, p = 0.001) | 2 d | 1.2 pp |
| 2026-06-17 | Gemini | model version + generation config | not testable | **59 d** | |
| 2026-08-17 | Groq | provider outage | not testable | arm ends 2026-08-16 | |
| 2026-08-19 | Groq / Grok | engine replacement | not testable | arms never overlap | |
| 2026-08-19 | four continuous arms | transport (declared non-event) | not testable | 7 d | |
| 2026-08-31 | Perplexity | window unified | not testable | 8 d | |
| 2026-08-31 | Perplexity | probe stratum added | not testable | 8 d | |
| 2026-08-31 | Grok | `reasoning_effort=low` | not testable | 8 d | |
| 2026-09-06 | ChatGPT, Claude | panel composition | not testable | 8 d | |

| Detected, not declared | Arm | Verdict |
|---|---|---|
| 2026-05-24 → 2026-05-25 | Perplexity | rupture of −7.87 pp with no declared event; nearest declared event 24 days away |
| 2026-05-27 → 2026-05-28 | Perplexity | rupture of +5.77 pp with no declared event; nearest declared event 27 days away |
| 2026-08-08 → 2026-08-10 | Perplexity | rupture of +5.24 pp with no declared event; nearest declared event 9 days away |
| 2026-06-09 → 2026-08-08 | Groq | rupture of +1.69 pp localised only to the 59-day hole; not attributable |

This is the result the analysis was commissioned to produce, and it reads as follows.

**One declared event produced a detectable rupture, and it is the one the manuscript does not declare.** 2026-06-05, when `GEMINI_THINKING_BUDGET` was set to 1024 and Gemini was dropped from `MANDATORY_LLMS`, is listed in `R3-fieldlog.md` §3 as a *candidate* for Table 8, sourced to `ROADMAP_2026Q2-Q4.md:26-36` rather than to the methodology. The detector finds a boundary there at zero distance, with the arm's rate moving from 1.29% to 2.80%. The mechanism is the one proposed and never confirmed in the 2026-04-26 Gemini investigation (I6): capping the thinking budget leaves output tokens for text, and text is what the extractor reads. The confirmation is indirect and it rests on four post-boundary days, since the 59-day hole opens on 2026-06-10. It is nonetheless the first quantitative support the project has for that hypothesis, and it argues that 2026-06-05 belongs in Table 8.

**Five declared events produced no rupture, and the instrument was sensitive enough to have seen one.** The 2026-04-30 battery changes (probe activation, `query_type` re-annotation) move nothing in any arm, and the minimum detectable difference at that boundary ranges from 1.2 pp in Gemini to 6.5 pp in Perplexity. Both changes are outside the canonical outcome by construction: probe rows are excluded by the cut, and `query_type` re-annotation relabels a factor without touching a response. The absence of a rupture is therefore the expected result and it is worth reporting as a positive control, since it shows the detector is not manufacturing boundaries wherever the documentation mentions a date.

**Fifteen of the twenty-one declared event-by-arm pairs are not testable, and the reason is always the same.** Every remaining declared event sits inside or adjacent to a hole: 59 days for the Gemini model change, seven days for the arm swap and the TLS change, eight days for the three 2026-08-31 events and for the September panel reduction. The collection stopped, for reasons of credit or provider behaviour, at almost exactly the moments the instrument was being changed. That is not a coincidence. The 2026-08-24 to 2026-08-30 hole exists because the new fifth arm consumed 72% of the run (I13), and the fix for that consumption is the 2026-08-31 `reasoning_effort` event; the September holes exist because of the credit exhaustion that also forced the panel reduction. The instrument changes and the missing data have common causes, which means no design that waits for the events to happen can measure them.

**Perplexity carries three ruptures nobody declared.** Two fall in late May and one in early August, each localised to one or two days, each larger in magnitude than the Gemini event that is declared. The late-May pair is a decline and a partial recovery inside four days. The early-August rupture of +5.24 pp sits nine days from the arm-swap boundary and coincides with the resumption of collection after the 59-day hole. No commit, changelog entry or governance note in the repository dates an instrument change to any of these boundaries. Either the retrieval-augmented arm moves on its own at a scale the parametric arms never show, or something changed in it that the project did not record.

---

## 5. Autocorrelation and what it costs the standard errors

**Method.** Autocorrelation is computed on the daily rate twice per arm: on the raw series, and after removing the mean of each segment defined by the ruptures of Table 5. The second version answers whether consecutive days are dependent; the first version, if read without the second, mostly reports that the series contains a step. Lags are reported both in collected-day index and in true calendar days, the latter using only pairs that are genuinely adjacent on the calendar so that a hole contributes nothing. Ljung-Box, a Wald-Wolfowitz runs test and Spearman correlation on calendar-adjacent day pairs complete the picture.

**Table 7. Lag-1 to lag-3 autocorrelation of the daily rate.** *Caption: the raw column is dominated by the level shift across the 59-day hole in the two arms that have one. Source: `data/s2_acf.csv`.*

| Arm | Raw ρ₁ | Raw ρ₂ | Raw ρ₃ | Demeaned ρ₁ | Demeaned ρ₂ | Demeaned ρ₃ | Calendar-adjacent ρ₁ |
|---|---:|---:|---:|---:|---:|---:|---:|
| ChatGPT | 0.248 | −0.025 | −0.099 | 0.248 | −0.025 | −0.099 | 0.238 |
| Claude | −0.107 | 0.051 | −0.152 | −0.107 | 0.051 | −0.152 | −0.193 |
| Gemini | **0.673** | 0.690 | 0.613 | 0.120 | 0.270 | 0.050 | 0.157 |
| Perplexity | 0.375 | 0.351 | 0.259 | 0.016 | 0.098 | −0.013 | 0.006 |
| Groq | **0.724** | 0.573 | 0.545 | 0.266 | −0.117 | −0.053 | 0.250 |
| Grok | NOT RUN — 5 collected days | | | | | | |

Gemini and Groq look strongly autocorrelated and are not. Their raw lag-1 correlations of 0.67 and 0.72 collapse to 0.12 and 0.27 once the step at the 59-day hole is removed, and stay near zero at longer lags. An analyst who fits an autoregressive model to the raw series will estimate persistence that is an undeclared regime change in disguise.

What remains after demeaning is weak and inconsistent in sign. Ljung-Box at lag 1 clears 0.05 in every arm (smallest p = 0.062, Groq). The Spearman correlation between calendar-adjacent days is significant in exactly one arm, and it is negative: Claude, ρ = −0.374, p = 0.016, which on five arms tested is one rejection where 0.25 is expected by chance. The runs test flags the same arm (z = 2.15, p = 0.031) and no other. The honest summary is that consecutive days are close to independent once regime shifts are accounted for, with a single unreplicated negative lag-1 signal in Claude.

**Table 8. Design effect for the study's aggregate rate.** *Caption: the same pooled rate, with two candidate primary sampling units. `deff` above 1 means a naive binomial interval is too narrow by its square root. Source: `data/s2_dependence.csv`.*

| Arm | Naive SE (pp) | Day-clustered SE (pp) | Day deff | SE inflation | Query-clustered SE (pp) | Query deff | SE inflation | Effective n (query) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ChatGPT | 0.306 | 0.097 | 0.10 | 0.32 | 2.563 | 70.1 | 8.37 | 216 |
| Claude | 0.357 | 0.159 | 0.20 | 0.45 | 3.017 | 71.6 | 8.46 | 210 |
| Gemini | 0.109 | 0.132 | 1.46 | 1.21 | 0.574 | 27.8 | 5.27 | 553 |
| Perplexity | 0.568 | 0.816 | 2.07 | 1.44 | 3.743 | 43.5 | 6.59 | 178 |
| Groq | 0.234 | 0.133 | 0.32 | 0.57 | 1.883 | 64.7 | 8.04 | 220 |
| **All arms pooled** | **0.147** | **0.193** | **1.74** | **1.32** | **1.166** | **63.3** | **7.96** | **1,083** |

The implication for the study is direct, and it is not the implication the methodology anticipated.

Clustering on the collection day, which is what `METHODOLOGY_V2.md:114` specifies through a random intercept per date, inflates the pooled standard error by a factor of 1.32 and inflates nothing at all in three of five arms. ChatGPT, Claude and Groq have day-level design effects *below* one, with Pearson overdispersion of 0.09, 0.26 and 0.25 against a binomial expectation of 1. Days in those arms vary less than independent sampling would predict. The reason is structural: every round re-asks the same fixed battery of 192 prompts, so a day is close to a census of the prompt population rather than a sample from it, and the prompt effects that would dominate a random sample are held constant across days by design.

The dependence that matters is at the prompt. Clustering on the query gives a pooled design effect of 63.3, an eightfold inflation of the standard error, and an effective sample size of 1,083 against a nominal 68,624. Within-prompt intraclass correlation is 0.97 pooled and between 0.34 and 0.91 by arm. That is the arithmetic consequence of asking the same 192 questions a hundred times each: the study observes 192 prompts deeply, not 68,624 independent trials.

Any interval in the manuscript computed as binomial over the observation count is too narrow by roughly a factor of eight for any statement about the population of prompts, and roughly correct for a statement about these 192 prompts. The distinction is not cosmetic. On the canonical cut used here, the pooled rate carries a naive half-width of 0.29 points, a day-clustered half-width of 0.38, and a prompt-clustered half-width of 2.29. The published dashboard interval of 36.3% [36.0, 36.6] is of the first kind. Which kind is right depends entirely on whether the claim generalises beyond the battery, and the manuscript should say which claim it is making.

---

## 6. Round and weekday

**Method.** The round comparison is paired within the day, so no day-level shock can produce it, and it uses the 24 days on which both rounds ran; the test is Wilcoxon signed-rank on the within-day difference with a 2,000-draw bootstrap interval. The weekday comparison is at day level, Mann-Whitney with a bootstrap interval on the difference of means. Benjamini-Hochberg runs over all fourteen tests.

Composition is balanced across rounds and cannot confound the comparison: both rounds carry all 192 prompts, all six arms, 50.00% Portuguese and 50.00% directive (`data/s2_round_composition.csv`).

**Table 9. Round and weekday effects.** *Caption: positive means morning above evening, or weekend above weekday. Source: `data/s2_round_weekday.csv`.*

| Arm | Contrast | Units | Estimate (pp) | 95% bootstrap CI | p | q (BH) |
|---|---|---:|---:|---|---:|---:|
| ChatGPT | morning − evening | 24 d | +0.35 | [−0.24, +0.93] | 0.312 | 0.868 |
| Claude | morning − evening | 24 d | +0.41 | [−0.37, +1.46] | 0.703 | 0.868 |
| Gemini | morning − evening | 24 d | −0.03 | [−0.27, +0.22] | 0.808 | 0.868 |
| Perplexity | morning − evening | 24 d | −0.30 | [−1.48, +0.91] | 0.732 | 0.868 |
| Groq | morning − evening | 24 d | −0.29 | [−0.49, −0.09] | **0.019** | 0.232 |
| Pooled | morning − evening | 24 d | +0.01 | [−0.21, +0.22] | 0.548 | 0.868 |
| ChatGPT | weekend − weekday | 50 d | −0.16 | [−0.51, +0.21] | 0.358 | 0.868 |
| Claude | weekend − weekday | 50 d | +0.20 | [−0.73, +1.15] | 0.355 | 0.868 |
| Gemini | weekend − weekday | 51 d | −0.02 | [−0.50, +0.49] | 0.868 | 0.868 |
| Perplexity | weekend − weekday | 52 d | −0.07 | [−3.66, +3.40] | 0.701 | 0.868 |
| Groq | weekend − weekday | 47 d | +0.09 | [−0.35, +0.56] | 0.846 | 0.868 |
| Pooled | weekend − weekday | 52 d | +0.39 | [−0.42, +1.38] | 0.436 | 0.868 |
| Grok | both contrasts | — | NOT RUN — 0 days with both rounds; 2 weekend and 3 weekday days | | | |

Nothing survives correction. The Groq morning-minus-evening difference of −0.29 pp has a nominal p of 0.019 and a BH q of 0.232 on a family of fourteen, and the arm it belongs to no longer exists. The pooled round effect is +0.01 pp with an interval a fifth of a point wide either side, which is as close to a demonstrated null as a design of this size can produce.

The practical reading is that the second daily round buys precision and nothing else. Collapsing the two rounds into a single daily observation loses no systematic signal, and the 24-of-52 realisation rate means the panel has in effect been running once a day for most of its life without any consequence visible in the outcome.

---

## 7. Ranking stability

**Method.** Weekly entity coverage is the share of the week's responses in the entity's vertical that mention it inside the 200-character window. The ranking spans the full cohort of 111 real entities, with coverage zero for an entity absent from a week; restricting the correlation to entities cited in both weeks would drop precisely the entities that moved. Kendall tau-b is computed between consecutive ISO weeks, alongside a second tau restricted to entities with non-zero coverage in at least one of the two weeks, the top-10 overlap, and the rank displacement among active entities. Engine rankings are treated the same way.

**Table 10. Week-to-week ranking stability.** *Caption: `days` gives collected days per week, since a week with one collected day is a thin base. Source: `data/s2_rank_tau.csv`.*

| Week pair | Days | τ-b (full cohort) | τ-b (active only) | Top-10 overlap | Median rank shift | Share moving ≥3 ranks |
|---|---|---:|---:|---:|---:|---:|
| W17 → W18 | 4, 4 | 0.927 | 0.852 | 0.9 | 2 | 18/50 |
| W18 → W19 | 4, 2 | 0.918 | 0.872 | 0.8 | 3 | 26/48 |
| W19 → W20 | 2, 7 | 0.866 | 0.826 | 1.0 | 3 | 29/52 |
| W20 → W21 | 7, 7 | 0.868 | 0.823 | 0.9 | 3 | 34/57 |
| W21 → W22 | 7, 6 | 0.886 | 0.837 | 0.9 | 3 | 33/56 |
| W22 → W23 | 6, 7 | 0.937 | 0.863 | 0.9 | 2 | 17/53 |
| W23 → W24 | 7, 2 | 0.866 | 0.868 | 0.8 | 3 | 31/52 |
| W24 → W32 (across the hole) | 2, 1 | 0.818 | 0.606 | 0.7 | 6 | 32/45 |
| W32 → W33 | 1, 7 | 0.846 | 0.809 | 1.0 | 5 | 36/56 |
| W33 → W34 | 7, 1 | 0.866 | 0.813 | 0.9 | 3 | 34/57 |
| W34 → W36 | 1, 2 | 0.877 | 0.731 | 0.9 | 5 | 35/52 |
| W36 → W37 | 2, 2 | 0.777 | 0.694 | 1.0 | 4 | 39/55 |
| **Mean** | | **0.871** | **0.800** | **0.892** | **3.5** | **57.5%** |

Engine rankings are a different story. Kendall tau-b between consecutive weeks is **1.000 in all twelve pairs**: Perplexity, Claude, ChatGPT, Groq, Gemini never change places. That stability is partly an artefact of measuring only the arms common to both weeks. When Groq left and Grok entered, the new arm landed at 39.2% in its first week, second in the panel, demoting Claude and ChatGPT one place each. Tau computed on common arms reports 1.000 for that transition because it never sees the substitution. A rank-stability statistic that conditions on common membership is blind to exactly the change that reorders a market.

The practical conclusion the paper can carry is quantitative. Entity ordering is stable in bulk and unstable in detail: the correlation is high, the top of the table barely moves (top-10 overlap 0.89), and yet 57.5% of active entities change rank by three or more positions from one week to the next and 35.5% by five or more, with a median displacement of 3.5 ranks. Of 111 real cohort entities, 66 are ever cited inside the window and 45 never are, so the churn is concentrated in a middle band of roughly fifty entities with coverage between about 0.5% and 10%.

That pattern sets the measurement frequency directly. A brand in the top ten can be measured monthly and will not be misread. A brand in the middle band measured in any single week has a better-than-even chance of being reported three or more ranks from where the next week would place it, so a claim about its position needs either a multi-week average or an explicit interval, never a weekly snapshot. Zero decoy entities were cited in any canonical row, so the churn is movement among real entities and not contamination.

---

## 8. Intervention analysis

### 8.1 The 2026-06-17 Gemini event

**Design.** Difference in differences with Gemini as the treated arm, the other continuously observed arms as controls, a pre-window of 2026-04-23 to 2026-06-16 and a post-window of 2026-06-17 to 2026-09-08. Estimated as a linear probability model and as a logit, both with vertical, query type and language controls, and standard errors clustered on the collection day. Because the design has 52 day-clusters, where asymptotic cluster-robust intervals are known to be too narrow, a 600-draw day-level cluster bootstrap of the raw two-by-two contrast accompanies every specification.

**Table 11. Difference-in-differences estimates.** *Caption: all effects in percentage points on the citation rate. Source: `data/s2_did.csv`.*

| Specification | Raw DiD (pp) | LPM DiD (pp) | Cluster-robust 95% CI | p | Bootstrap 95% CI | Clusters |
|---|---:|---:|---|---:|---|---:|
| Controls: ChatGPT, Claude | +1.76 | +1.73 | [+1.26, +2.20] | 5.4e−13 | [+1.28, +2.27] | 52 |
| Controls: + Perplexity | +1.57 | +1.60 | [+0.12, +3.07] | 0.034 | [−0.66, +2.78] | 52 |
| Controls: + Perplexity, Groq | +0.04 | +0.06 | [−1.84, +1.95] | 0.953 | [−2.69, +1.66] | 52 |
| Post truncated at 2026-08-18 | +2.47 | +2.49 | [+1.76, +3.23] | 3.5e−11 | [+1.82, +3.21] | 47 |
| **Placebo, false boundary 2026-05-17, controls ChatGPT + Claude** | −0.18 | −0.21 | [−0.69, +0.27] | 0.395 | [−0.74, +0.29] | 39 |
| **Placebo, false boundary 2026-05-17, three controls** | +1.56 | +1.53 | [+0.72, +2.34] | 2.2e−4 | [+0.69, +2.40] | 39 |

**Premises the design requires, and how each one fails here.**

*Parallel trends.* The control arms must have followed the path Gemini would have followed without the intervention. The placebo row tests this and the design fails it in one of its two forms. With Perplexity among the controls, a boundary placed at 2026-05-17, where nothing happened, yields +1.53 pp with p = 2.2e−4, which is the same magnitude and the same sign as the estimate at the real boundary. The reason is visible in Section 3: Perplexity has a downward trend of its own, so any Gemini-versus-Perplexity contrast drifts upward whatever date is chosen. With ChatGPT and Claude alone, the placebo returns −0.21 pp with p = 0.395 and the real boundary returns +1.73 pp, which is the pattern a valid design produces. The estimate is therefore conditional on a control set justified by its own flatness rather than by any prior argument, and the four specifications span +0.06 to +2.49 pp.

*No composition change at the boundary.* The battery is identical on both sides. The panel is not: Groq leaves the fifth slot on 2026-08-16 and Grok enters it on 2026-08-23, both inside the post-window. The specification that includes Groq among the controls returns +0.06 pp because Groq's own level shift at the 59-day hole cancels Gemini's. Truncating the post-window at 2026-08-18 removes the swap and returns +2.49 pp. There is no specification that both uses a five-arm control set and avoids the swap.

*No other shock at the boundary.* This is where the design fails irreparably. The pre- and post-windows are separated by a 59-day hole, so the estimate compares Gemini in April to early June with Gemini in August to early September. Between the two lie the 100 MB database crisis, the R2 restoration that had been inert for two months, an integrity gate that blocked every run for four days, a FinOps ceiling that blocked a refilled provider, and a fifty-nine-day cessation of collection. Any of those could have moved a rate. The 2026-06-17 model change is one of a large set of things that changed between the last pre-observation and the first post-observation, and nothing in the data distinguishes it from the others.

*Separability of the treatment.* Even granting every premise above, commit `f43a42b` changed the model identity and the reasoning budget together, so the estimate attaches to their combination and to nothing narrower. The field log records this at I9 and the point stands unchanged.

**Conclusion for this event.** The best-supported estimate is +1.7 pp on a base of 1.4%, meaning the arm's citation rate roughly doubled, and the estimate is not identified as an effect of the model change. It is the difference between two regimes separated by two months of instrument history. The paper should report the magnitude and the non-identification together, in the same sentence.

### 8.2 The August arm replacement

There is no difference-in-differences estimate to be had for Groq to Grok, and the script reports none. The treated unit changes identity at the boundary: provider, model, generation configuration and engine all move at once, and the two arms never overlap in time. Groq's last observation is 2026-08-16 and Grok's first persisted day is 2026-08-23. The observed level difference is Groq 8.52% over 14,208 observations against Grok 29.61% over 1,118, or 28.02% over the 960 observations collected after the 2026-08-31 reasoning-effort change. That difference is between two engines, not before and after an intervention, and it is recorded in `s2_results.json:arm_swap_levels` with the non-identification stated in the field.

What is testable is whether the shared instrument moved when the fifth slot was replaced. Running each continuous arm as treated against the other three, across 2026-08-08 to 2026-08-18 versus 2026-08-23 to 2026-09-08, returns +1.06 pp (ChatGPT, p = 0.389), +1.00 pp (Claude, p = 0.273), −3.16 pp (Gemini, p = 0.226) and +3.22 pp (Perplexity, p = 0.328). None is significant. Each rests on 13 day-clusters, and the bootstrap intervals are correspondingly wide, reaching [−29.2, −0.1] for Gemini. The check is consistent with the CHANGELOG's declaration that the TLS change accompanying the swap had no effect on collected data, and it is far too weak to be evidence for that declaration.

---

## 9. What this does not establish

1. **Nothing here measures engine behaviour separately from instrument behaviour.** The series spans six arms, four of them carrying at least one declared configuration change, in a database whose calendar is 37.4% populated. Every trend, rupture and intervention estimate is a joint statement about the engine and the collector.

2. **Fifteen of twenty-one declared event-by-arm pairs were not tested.** They were not tested because there is no data on one side of the boundary within three days, and the tables say so in every row. Their absence from the results is a property of the calendar, not evidence that they moved nothing.

3. **The 2026-06-05 Gemini finding is one boundary with four post-boundary days and daily counts in single digits.** The rupture is significant at p = 0.001 under a permutation test that respects the daily sample sizes, and the mechanism is plausible and pre-registered in an April audit. It is not a replication, no second Gemini arm exists to compare against, and the same commit set also removed the arm from the mandatory list, which is why 2026-06-05 is a partial day in the first place. Treat it as a strong candidate for Table 8 and as a hypothesis for the next window, not as a confirmed mechanism.

4. **The three Perplexity ruptures have no established cause.** The analysis establishes that the arm's rate shifts by 5 to 8 points at three dated boundaries with no corresponding entry in the repository. Whether the cause is the engine, the retrieval index, the provider's routing or an undocumented change in the collector is not determined by anything measured here.

5. **The design effect calculation assumes days and prompts as the only candidate clusters.** Verticals, entity cohorts and languages are crossed with both and are not modelled here. The eightfold inflation under prompt clustering is a lower bound on what a fully crossed random-effects treatment would report, not a final figure.

6. **The autocorrelation results are conditional on the segment demeaning.** Segments come from the change points of Table 5, which were detected on the same data. Demeaning by detected segments removes some genuine autocorrelation along with the regime shifts; the demeaned values are therefore conservative estimates of day-to-day dependence, and the raw values are inflated ones. The truth for each arm lies between the two columns of Table 7.

7. **The round comparison uses 24 days and speaks only to those days.** Days with a single round were, by construction, days on which something went wrong. The null on round is a null on the days when the pipeline worked twice.

8. **The ranking analysis measures coverage, not prominence, share of voice or sentiment.** An entity's coverage is the share of responses naming it inside 200 characters. Two entities with equal coverage may occupy very different positions in the response, and first-mention offset is censored at 200 characters for five of six arms, so that comparison cannot be made on this series at all.

9. **The window harmonisation is not the same as window-independent measurement.** Re-extracting at 200 characters makes the six arms comparable to each other. It does not make the 200-character window the right aperture, and for rows collected before 2026-08-31 the text beyond 200 characters was never stored, so no sensitivity analysis at a wider window is possible for the historical series.

10. **This analysis does not reconcile with the published dashboard and should not be read as if it did.** `data/dashboard_data.json` reports an overall rate of 36.3%. On this snapshot, the same query, `SELECT COUNT(*), SUM(cited) FROM citations` with no filter, returns 35.97%, which is the dashboard's definition: all rows, probes included, no uniform window. The probe stratum is 17,919 rows at a 95.04% citation rate, and `scripts/generate_dashboard_json.py:191` computes the headline over it. The canonical cut used here gives 20.54% on the stored outcome and **17.97%** under the uniform 200-character window. The script's own comment at line 468 states that probe rows must be excluded because the citation is induced by the prompt, and the exclusion is applied to one later block and not to the headline. The published figure and the analytic figure differ by a factor of two, for reasons that are entirely mechanical and currently undocumented, which is finding I19C of the field log stated numerically.

11. **The snapshot is not the live series.** It ends 2026-09-08 with 52 collected days. The dashboard of 2026-09-11 reports 56. Three further collected days, and the four September partial days that the degrade-mode preflight has since recorded, are outside everything above.

---

## 10. Reproduction

```
cd docs/research/methods-paper/journal-v2/stats
python s2_temporal.py --db ../../../../../data/papers.db --repo ../../../../.. --perm 999
```

Runtime is about three minutes, dominated by the re-extraction of 68,624 responses and by the permutation tests. The random seed is fixed at 20260911; permutation p-values, bootstrap intervals and the parametric marginal effects are reproducible bit for bit at the same seed and `--perm` value. `ruptures` 1.1.10 is optional and was installed for this run; without it the corroboration column of Table 5 is reported as NOT RUN and the primary detector is unaffected.

**Files written.**

| File | Contents |
|---|---|
| `s2_results.json` | every headline number in this document |
| `data/s2_daily_engine.csv` | the daily series per arm: n, cited, rate, Wilson interval, model version, rounds, partial flag and reason, weekday, ISO week, day index, gap before |
| `data/s2_daily_engine_round.csv` | the same split by collection round |
| `data/s2_daily_pooled.csv` | pooled daily series with cells filled and partial-day classification |
| `data/s2_calendar_gaps.csv` | every hole in the calendar with start, end and length |
| `data/s2_window_reconciliation.csv` | Table 1 |
| `data/s2_trend.csv` | Table 4 with all intermediate statistics |
| `data/s2_changepoints.csv` | Table 5, both detectors |
| `data/s2_event_confrontation.csv` | Table 6 with verdicts and minimum detectable differences |
| `data/s2_acf.csv` | Table 7, both series and both lag units, lags 1 to 10 |
| `data/s2_dependence.csv` | Table 8 plus Ljung-Box, runs test and adjacent-day correlations |
| `data/s2_round_weekday.csv`, `data/s2_round_composition.csv` | Table 9 and its composition check |
| `data/s2_weekly_entity_rank.csv`, `data/s2_weekly_engine_rank.csv`, `data/s2_rank_tau.csv` | Table 10 and the underlying weekly rankings |
| `data/s2_did.csv` | Table 11 |
| `data/s2_partial_day_sensitivity.csv` | every arm's rate with and without partial days |
