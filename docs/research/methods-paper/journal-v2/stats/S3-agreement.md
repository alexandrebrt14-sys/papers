# S3. Inter-engine agreement: do six generative engines measure the same object?

Analysis file: `stats/s3_agreement.py`. Database: `data/papers.db`, opened read-only
(`file:...?mode=ro`). Canonical stratum `COALESCE(is_probe,0)=0`. Series 2026-04-23 to
2026-09-08, 53 collection days, 192 canonical queries, six engines, 68,624 rows.
Random seed 20260911; 2,000 bootstrap replications; 2,000 null replications.
Every figure below is printed by the script.

The substantive question is whether "citation rate" names a property of the firm or a
property of the engine. Under the first reading the engines are interchangeable
instruments reading one underlying quantity, and their disagreement is sampling noise.
Under the second, each engine constitutes its own object, and a rate bought from one
vendor estimates nothing outside that vendor.

---

## 1. Panel, outcome and what constrains the answer

### 1.1 The outcome had to be re-derived

`citations.cited_v2` is not comparable across arms as stored. Five arms wrote
`response_text = text[:200]` at collection time; Perplexity wrote the whole response,
median 607 characters. The stored outcome was extracted from whatever text was stored,
so one arm was measured through a wider aperture than the other five. This section
therefore re-derives the outcome under a uniform 200-character window for every arm,
using the project's own extractor (`src.analysis.entity_extraction.EntityExtractor`
over the v2 cohort, via `tables/_common.build_extractors`):

| symbol | definition |
|---|---|
| `cited_win` | 1 if at least one cohort entity is matched in `response_text[:200]` |
| `entities_win` | the matched entities, ordered by first-mention offset |

**Table S3.0a.** Re-extraction at the 200-character window against the stored `cited_v2`.
Series 2026-04-23 to 2026-09-08, 68,624 canonical rows, denominator is rows per engine.

| Engine | n | Stored rate (%) | Window rate (%) | Rows identical (%) | Median stored chars |
|---|---:|---:|---:|---:|---:|
| ChatGPT | 15,168 | 17.17 | 17.17 | 100.00 | 200 |
| Claude | 15,034 | 25.75 | 25.75 | 100.00 | 200 |
| Gemini | 15,355 | 1.86 | 1.86 | 100.00 | 200 |
| Groq | 14,208 | 8.52 | 8.52 | 100.00 | 200 |
| Perplexity | 7,741 | 74.87 | 52.03 | 77.16 | 607 |
| Grok | 1,118 | 29.61 | 29.61 | 100.00 | 200 |

The re-derivation reproduces the stored value on every one of the 60,883 rows from the
five truncated arms, which is what licenses using it as the harmonised outcome, and it
moves Perplexity by 22.84 percentage points. Section 8 reports the whole analysis again
on the outcome as stored, so that a reader can see how much of the between-engine
spread is the instrument.

### 1.2 No six-engine panel exists

Groq's last collection day is 2026-08-16 and Grok's first is 2026-08-23. The two never
appear on the same day, so the six-way panel has zero complete cells and Fleiss' kappa
on six raters is undefined in this series. Perplexity ran a 96-query half-battery
against the other arms' 192. Agreement is reported on five nested balanced panels:

| Panel | Engines | Query set | Complete cells | Days |
|---|---|---|---:|---:|
| P1 | ChatGPT, Claude, Gemini | 192 | 9,129 | 50 |
| P2 | ChatGPT, Claude, Gemini, Groq | 192 | 8,550 | 47 |
| P3 | ChatGPT, Claude, Gemini, Grok | 192 | 542 | 3 |
| P4 | ChatGPT, Claude, Gemini, Groq, Perplexity | 96 | 4,231 | 47 |
| P5 | ChatGPT, Claude, Gemini, Grok, Perplexity | 96 | 278 | 3 |

The unit of observation is (collection day, canonical query, engine). Replicates within
a cell are reduced to the earliest run, leaving 42,487 cells: ChatGPT 9,359, Claude
9,323, Gemini 9,455, Groq 8,783, Perplexity 4,737, Grok 830.

### 1.3 Test-retest sets the ceiling

The collector re-ran parts of the battery inside the same day, which gives a within-engine
replication that no between-engine statistic can exceed by much.

**Table S3.0b.** Same engine, same query, same day, more than one run. Series 2026-04-23
to 2026-09-08, denominator is cells with at least two runs for that engine.

| Engine | Cells with replicates | Extra runs | Concordant | Chance concordance | Test-retest kappa |
|---|---:|---:|---:|---:|---:|
| ChatGPT | 5,158 | 5,809 | 0.966 | 0.716 | 0.881 |
| Claude | 5,059 | 5,711 | 0.964 | 0.618 | 0.906 |
| Gemini | 5,249 | 5,900 | 0.989 | 0.964 | 0.686 |
| Groq | 4,965 | 5,425 | 0.992 | 0.844 | 0.950 |
| Perplexity | 2,687 | 3,004 | 0.835 | 0.501 | 0.669 |
| Grok | 288 | 288 | 0.885 | 0.583 | 0.725 |

Perplexity repeats itself on 83.5% of same-day re-runs and Grok on 88.5%. Any
between-engine kappa involving those two arms is read against a ceiling near 0.67 and
0.73, not against 1.

### 1.4 Implementation

Fleiss' kappa is computed from the per-item count of raters assigning 1, and matches
`statsmodels.stats.inter_rater.fleiss_kappa` to machine precision on P1 (0.086089 both
ways, difference 0.0). Pairwise Cohen's kappa matches
`src.analysis.kappa_validator.cohen_kappa_binary` on ChatGPT against Claude (0.1882 both
ways, n = 9,322). The vectorised forms exist so that the cluster bootstrap can run
thousands of replications; they are not a second definition of the statistic. Intervals
resample collection days with replacement, which is the cluster the project already uses
in `src/analysis/cluster_robust.py`: every query in a day faces the same model snapshot.

---

## 2. Agreement on whether a citation happened

**Table S3.1a.** Fleiss' kappa on the harmonised binary outcome, by panel. Series
2026-04-23 to 2026-09-08, percentile interval from 2,000 day-cluster bootstrap
replications, denominator is complete panel cells.

| Panel | Engines | k | Cells | Days | Base rate | Fleiss kappa | 95% CI | Band |
|---|---|---:|---:|---:|---:|---:|---|---|
| P1 | ChatGPT+Claude+Gemini | 3 | 9,129 | 50 | 0.151 | 0.0861 | [0.0736, 0.0996] | slight |
| P2 | ChatGPT+Claude+Gemini+Groq | 4 | 8,550 | 47 | 0.135 | 0.1692 | [0.1579, 0.1809] | slight |
| P3 | ChatGPT+Claude+Gemini+Grok | 4 | 542 | 3 | 0.194 | 0.2263 | [0.2170, 0.2371] | fair |
| P4 | P2 + Perplexity | 5 | 4,231 | 47 | 0.259 | 0.1464 | [0.1364, 0.1561] | slight |
| P5 | P3 + Perplexity | 5 | 278 | 3 | 0.311 | 0.2359 | [0.2163, 0.2548] | fair |
| P6 | all six | 6 | 0 | 0 | — | undefined | — | — |

Bands follow Landis and Koch (1977), as coded in `src/analysis/kappa_validator.py`. The
panel that runs the whole five months on the full battery, P1, sits at 0.086. Adding a
fourth arm raises the figure because Fleiss rewards a rater that shares the majority
pattern, not because the engines converged.

**Table S3.1b.** Fleiss' kappa within vertical. Series 2026-04-23 to 2026-09-08,
denominator is complete panel cells in that vertical.

| Panel | Fintech | Retail | Health | Technology |
|---|---:|---:|---:|---:|
| P1 (n per cell 2,352 / 2,352 / 2,236 / 2,189) | 0.0581 | 0.1220 | 0.0508 | **-0.0983** |
| P2 (2,208 / 2,208 / 2,089 / 2,045) | 0.1375 | 0.2310 | 0.1383 | 0.0078 |
| P3 (144 / 144 / 144 / 110) | 0.1049 | 0.2907 | 0.1045 | 0.0463 |
| P4 (1,104 / 1,100 / 1,027 / 1,000) | 0.0756 | 0.1550 | 0.1062 | -0.0004 |
| P5 (72 / 72 / 72 / 62) | 0.1307 | 0.2800 | 0.1141 | 0.0275 |

Technology in P1 is negative, with a bootstrap interval of [-0.1081, -0.0868] that
excludes zero. Three engines asked the same technology query on the same day agree less
often than three raters drawing independently at their own observed rates. Retail is the
only vertical where any panel reaches the fair band.

**Table S3.1c.** Base rates on the harmonised outcome. Series 2026-04-23 to 2026-09-08,
denominator is cells run by that engine after replicate reduction.

| Engine | Class | Cells | Cited (%) |
|---|---|---:|---:|
| ChatGPT | parametric | 9,359 | 17.41 |
| Claude | parametric | 9,323 | 26.04 |
| Gemini | parametric | 9,455 | 1.91 |
| Groq | parametric, open weights | 8,783 | 8.52 |
| Perplexity | retrieval-augmented | 4,737 | 53.09 |
| Grok | parametric | 830 | 32.65 |

A 27.8-fold spread separates the lowest arm from the highest on identical queries in
identical windows. Kappa is prevalence-sensitive, and marginals this unequal cap the
statistic before any disagreement is observed: Table S3.2a reports that cap.

### What a low Fleiss means for a buyer of single-vendor measurement

A Fleiss of 0.086 on the three arms that ran the entire five months says that, for a
given firm and a given question on a given day, knowing that one engine named the firm
carries very little information about whether another engine named it. The number a
single vendor sells is therefore not an estimate of a quantity that exists outside that
vendor's pipeline. Three operational consequences follow. A rate quoted without naming
the engine and the observation window is uninterpretable, because the same cohort and
the same battery produce 1.9% on one arm and 53.1% on another. A change in a
single-vendor rate cannot be attributed to a change in the firm's standing unless the
engine's own behaviour has been held fixed and demonstrated stable, and Table S3.0b shows
that two of the six arms are not stable enough within a single day to support that. And
a vendor panel that averages engines is reporting a composite whose weights are the
vendor's engine mix, which makes two vendors' averages incomparable even when both are
honestly computed.

---

## 3. Which pairs agree, and which barely overlap

**Table S3.2a.** Pairwise agreement on the harmonised outcome, over the maximal set of
cells both engines ran. Series 2026-04-23 to 2026-09-08, percentile interval from 2,000
day-cluster bootstrap replications, denominator is shared cells.

| Pair | Shared cells | P_o | Rate A | Rate B | Cohen kappa | 95% CI | Phi | Kappa max | Band |
|---|---:|---:|---:|---:|---:|---|---:|---:|---|
| Perplexity–Grok | 391 | 0.719 | 0.537 | 0.394 | 0.4461 | [0.4121, 0.5129] | 0.465 | 0.718 | moderate |
| Claude–Grok | 542 | 0.758 | 0.266 | 0.304 | 0.4081 | [0.3605, 0.4324] | 0.410 | 0.905 | moderate |
| ChatGPT–Groq | 8,777 | 0.864 | 0.174 | 0.085 | 0.4071 | [0.3946, 0.4197] | 0.442 | 0.612 | moderate |
| ChatGPT–Grok | 542 | 0.736 | 0.170 | 0.304 | 0.2885 | [0.2700, 0.3176] | 0.310 | 0.637 | fair |
| ChatGPT–Perplexity | 4,623 | 0.608 | 0.205 | 0.529 | 0.2414 | [0.2218, 0.2620] | 0.310 | 0.374 | fair |
| Claude–Perplexity | 4,615 | 0.606 | 0.389 | 0.530 | 0.2228 | [0.2045, 0.2409] | 0.232 | 0.722 | fair |
| Claude–Groq | 8,743 | 0.765 | 0.261 | 0.085 | 0.2205 | [0.2125, 0.2291] | 0.271 | 0.418 | fair |
| ChatGPT–Claude | 9,322 | 0.721 | 0.174 | 0.261 | 0.1882 | [0.1793, 0.1974] | 0.194 | 0.749 | slight |
| Groq–Perplexity | 4,336 | 0.572 | 0.144 | 0.530 | 0.1786 | [0.1601, 0.1980] | 0.266 | 0.259 | slight |
| Gemini–Groq | 8,587 | 0.917 | 0.018 | 0.085 | 0.1700 | [0.1238, 0.2132] | 0.231 | 0.324 | slight |
| Gemini–Grok | 830 | 0.701 | 0.035 | 0.327 | 0.1176 | [0.0889, 0.1496] | 0.231 | 0.139 | slight |
| ChatGPT–Gemini | 9,165 | 0.832 | 0.174 | 0.019 | 0.0998 | [0.0715, 0.1296] | 0.181 | 0.165 | slight |
| Claude–Gemini | 9,130 | 0.744 | 0.261 | 0.019 | 0.0483 | [0.0358, 0.0622] | 0.109 | 0.103 | slight |
| Gemini–Perplexity | 4,640 | 0.484 | 0.027 | 0.533 | 0.0276 | [0.0197, 0.0369] | 0.091 | 0.047 | slight |
| Groq–Grok | 0 | — | — | — | undefined | — | — | — | — |

Across the fourteen pairs that share any cell, mean kappa is 0.219, median 0.204,
mean phi 0.267, and mean observed agreement 0.716. High observed agreement is not
evidence of a shared object: Gemini and Groq agree on 91.7% of 8,587 cells while
reaching kappa 0.170, because both mostly say no.

Kappa max is the largest kappa these two marginals allow. Reading each pair against its
own ceiling changes the picture: the fourteen pairs reach on average 54.6% of the value
their base rates permit. Gemini–Perplexity attains 0.028 of a possible 0.047, so the pair
is close to the maximum compatible with marginals that far apart. The failure there is
not that the two disagree given what they could have agreed on; it is that a 1.9% arm
and a 53.1% arm cannot be describing the same object in the first place.

Three pairs sit at or below one tenth: Gemini–Perplexity (0.028), Claude–Gemini (0.048),
ChatGPT–Gemini (0.100). Gemini is a member of all three. The one pair above 0.44,
Perplexity–Grok, rests on 391 shared cells from three days, and its interval
[0.412, 0.513] is a three-cluster bootstrap that should not be read as a coverage
statement.

**Table S3.2b.** Cohen's kappa matrix. Series 2026-04-23 to 2026-09-08, cell denominators
in Table S3.2a.

| | ChatGPT | Claude | Gemini | Groq | Perplexity | Grok |
|---|---:|---:|---:|---:|---:|---:|
| **ChatGPT** | 1.000 | 0.188 | 0.100 | 0.407 | 0.241 | 0.289 |
| **Claude** | 0.188 | 1.000 | 0.048 | 0.221 | 0.223 | 0.408 |
| **Gemini** | 0.100 | 0.048 | 1.000 | 0.170 | 0.028 | 0.118 |
| **Groq** | 0.407 | 0.221 | 0.170 | 1.000 | 0.179 | n/a |
| **Perplexity** | 0.241 | 0.223 | 0.028 | 0.179 | 1.000 | 0.446 |
| **Grok** | 0.289 | 0.408 | 0.118 | n/a | 0.446 | 1.000 |

**Table S3.2c.** Observed agreement P_o. Same cells as Table S3.2b.

| | ChatGPT | Claude | Gemini | Groq | Perplexity | Grok |
|---|---:|---:|---:|---:|---:|---:|
| **ChatGPT** | 1.000 | 0.721 | 0.832 | 0.864 | 0.608 | 0.736 |
| **Claude** | 0.721 | 1.000 | 0.743 | 0.765 | 0.606 | 0.758 |
| **Gemini** | 0.832 | 0.743 | 1.000 | 0.917 | 0.484 | 0.701 |
| **Groq** | 0.864 | 0.765 | 0.917 | 1.000 | 0.571 | n/a |
| **Perplexity** | 0.608 | 0.606 | 0.484 | 0.571 | 1.000 | 0.719 |
| **Grok** | 0.736 | 0.758 | 0.701 | n/a | 0.719 | 1.000 |

---

## 4. Agreement on who is named

Binary agreement conflates two failures: engines can disagree about whether anyone was
named, and they can disagree about whom. Separating the two changes the reading of every
number above.

Entities named per cell: mean 0.284 over 42,487 cells; among the cells that name at
least one, mean 1.550, median 1, p90 3, maximum 9. Lists this short make rank-biased
overlap close to a weighted top-1 agreement, which is why RBO is reported next to the
first-name agreement rather than in place of it. RBO is the extrapolated form of Webber,
Moffat and Zobel (2010) with persistence p = 0.90.

**Table S3.3a.** Jaccard and RBO on the named-entity sets. Series 2026-04-23 to
2026-09-08. Columns 2 to 6 use cells where at least one of the two engines named an
entity; columns 7 to 9 use only cells where both named at least one.

| Pair | Scored cells | Only one named | Jaccard = 0 (%) | Mean Jaccard | Mean RBO | Both named | Mean Jaccard | Jaccard = 0 (%) | Mean RBO |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ChatGPT–Claude | 3,326 | 2,602 | 81.99 | 0.157 | 0.164 | 724 | 0.722 | 17.27 | 0.752 |
| ChatGPT–Gemini | 1,652 | 1,537 | 93.71 | 0.049 | 0.056 | 115 | 0.704 | 9.57 | 0.807 |
| ChatGPT–Groq | 1,737 | 1,196 | 74.73 | 0.228 | 0.245 | 541 | 0.732 | 18.85 | 0.787 |
| ChatGPT–Perplexity | 2,605 | 1,814 | 80.46 | 0.141 | 0.168 | 791 | 0.464 | 35.65 | 0.554 |
| ChatGPT–Grok | 200 | 143 | 73.00 | 0.209 | 0.242 | 57 | 0.732 | 5.26 | 0.849 |
| Claude–Gemini | 2,446 | 2,342 | 96.48 | 0.033 | 0.033 | 104 | 0.787 | 17.31 | 0.782 |
| Claude–Groq | 2,540 | 2,055 | 85.04 | 0.127 | 0.129 | 485 | 0.668 | 21.65 | 0.675 |
| Claude–Perplexity | 3,027 | 1,817 | 71.19 | 0.188 | 0.272 | 1,210 | 0.469 | 27.93 | 0.681 |
| Claude–Grok | 220 | 131 | 65.00 | 0.235 | 0.321 | 89 | 0.581 | 13.48 | 0.794 |
| Gemini–Groq | 799 | 713 | 89.74 | 0.085 | 0.097 | 86 | 0.789 | 4.65 | 0.903 |
| Gemini–Perplexity | 2,495 | 2,395 | 97.03 | 0.028 | 0.029 | 100 | 0.697 | 26.00 | 0.733 |
| Gemini–Grok | 274 | 248 | 91.24 | 0.049 | 0.062 | 26 | 0.519 | 7.69 | 0.658 |
| Groq–Perplexity | 2,391 | 1,858 | 86.58 | 0.094 | 0.120 | 533 | 0.421 | 39.78 | 0.537 |
| Perplexity–Grok | 237 | 110 | 49.37 | 0.366 | 0.474 | 127 | 0.684 | 5.51 | 0.885 |

**Table S3.3b.** Distribution of Jaccard, pooled over the fourteen pairs. Series
2026-04-23 to 2026-09-08, 23,949 scored cell-pairs, denominator is cell-pairs where at
least one engine named an entity.

| Decile | p10 | p20 | p30 | p40 | p50 | p60 | p70 | p80 | p90 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Jaccard | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.667 |

84.4% of scored cell-pairs have Jaccard exactly 0 and 9.8% exactly 1. The distribution
is bimodal at the endpoints with almost nothing in between, and the median of every pair
except Perplexity–Grok is zero. Reporting the mean alone (0.028 to 0.366 across pairs)
describes a shape that does not exist in the data.

The two right-hand blocks of Table S3.3a carry the finding. Of the 23,949 scored
cell-pairs, 18,961 have exactly one engine naming somebody; the Jaccard of those is zero
by construction. Restricted to the 4,988 cell-pairs where both engines named at least
one entity, mean Jaccard runs from 0.421 (Groq–Perplexity) to 0.789 (Gemini–Groq), and
mean RBO from 0.537 to 0.903.

**Table S3.9.** First-named entity agreement. Series 2026-04-23 to 2026-09-08,
denominator is cell-pairs where both engines named at least one entity.

| Pair | Both named | Same first name (%) |
|---|---:|---:|
| Perplexity–Grok | 127 | 91.34 |
| Gemini–Groq | 86 | 86.05 |
| ChatGPT–Groq | 541 | 81.15 |
| ChatGPT–Gemini | 115 | 80.00 |
| Claude–Grok | 89 | 77.53 |
| ChatGPT–Grok | 57 | 75.44 |
| Gemini–Perplexity | 100 | 73.00 |
| Claude–Perplexity | 1,210 | 69.50 |
| ChatGPT–Claude | 724 | 69.06 |
| Claude–Gemini | 104 | 61.54 |
| Claude–Groq | 485 | 58.97 |
| Gemini–Grok | 26 | 57.69 |
| Groq–Perplexity | 533 | 49.34 |
| ChatGPT–Perplexity | 791 | 48.04 |
| **Pooled** | **4,988** | **65.26** |

When two engines both name a company, they name the same company first 65.3% of the
time. The engines disagree about whether the question gets answered with a name far more
than they disagree about which name.

**Table S3.3c.** Kendall tau-b between engines on the ranking of cohort entities by
coverage rate, by vertical. Series 2026-04-23 to 2026-09-08, denominator is entities in
that vertical named at least once by any engine.

| Vertical | Entities | Median tau-b | Range | Undefined |
|---|---:|---:|---|---:|
| Fintech | 15 | 0.518 | 0.181 to 0.778 | 0 |
| Retail | 13 | 0.579 | 0.250 to 0.763 | 0 |
| Health | 16 | 0.269 | -0.033 to 0.621 | 5 |
| Technology | 18 | 0.181 | -0.246 to 0.553 | 0 |

Five combinations are undefined because Gemini never named a health cohort member inside
the window, so its column is constant. Over the 55 defined combinations, mean tau-b is
0.385, median 0.404, 38.2% exceed 0.5 and 14.5% are negative. Ranking agreement is
moderate and unevenly distributed: fintech and retail hold up, technology does not.

**Table S3.3d.** Kendall tau-b by pair, averaged across the verticals where it is
defined. Series 2026-04-23 to 2026-09-08.

| Pair | Verticals | Mean | Min | Max |
|---|---:|---:|---:|---:|
| ChatGPT–Gemini | 3 | 0.698 | 0.553 | 0.778 |
| Gemini–Groq | 3 | 0.668 | 0.485 | 0.778 |
| Perplexity–Grok | 4 | 0.528 | 0.285 | 0.742 |
| Gemini–Grok | 3 | 0.476 | 0.181 | 0.667 |
| ChatGPT–Groq | 4 | 0.470 | 0.221 | 0.763 |
| ChatGPT–Grok | 4 | 0.414 | 0.123 | 0.671 |
| Claude–Perplexity | 4 | 0.390 | 0.279 | 0.621 |
| Claude–Grok | 4 | 0.379 | 0.250 | 0.455 |
| Groq–Grok | 4 | 0.361 | -0.181 | 0.715 |
| Claude–Groq | 4 | 0.321 | -0.018 | 0.518 |
| Gemini–Perplexity | 3 | 0.309 | -0.155 | 0.686 |
| ChatGPT–Perplexity | 4 | 0.282 | -0.052 | 0.546 |
| Groq–Perplexity | 4 | 0.250 | -0.212 | 0.550 |
| Claude–Gemini | 3 | 0.162 | -0.246 | 0.404 |
| ChatGPT–Claude | 4 | 0.160 | -0.167 | 0.659 |

Groq and Grok never share a collection day, so their tau-b is computed on aggregate
coverage ranks from disjoint periods and is confounded with the era.

---

## 5. Latent structure of the engine panel

The matrix has one row per cohort entity named at least once inside the window and one
column per engine, holding the share of that engine's cells in the entity's vertical
that named it: 62 entities by 6 engines. Columns are standardised across entities before
decomposition, so the analysis is about the shape of an engine's coverage profile rather
than its level.

**Table S3.4a.** Principal components of the standardised entity-by-engine coverage
matrix. Series 2026-04-23 to 2026-09-08, 62 entities, 6 engines.

| Component | Explained variance | Cumulative |
|---|---:|---:|
| PC1 | 0.7805 | 0.7805 |
| PC2 | 0.0882 | 0.8688 |
| PC3 | 0.0529 | 0.9216 |
| PC4 | 0.0405 | 0.9622 |
| PC5 | 0.0289 | 0.9911 |
| PC6 | 0.0089 | 1.0000 |

**Table S3.4b.** Engine loadings on the first three components. Same matrix as Table
S3.4a.

| Engine | PC1 | PC2 | PC3 | Class |
|---|---:|---:|---:|---|
| ChatGPT | 0.374 | 0.683 | 0.389 | parametric |
| Claude | 0.413 | -0.304 | -0.427 | parametric |
| Gemini | 0.424 | -0.134 | -0.381 | parametric |
| Groq | 0.396 | 0.444 | -0.315 | parametric, open weights |
| Perplexity | 0.396 | -0.447 | 0.632 | retrieval-augmented |
| Grok | 0.443 | -0.163 | 0.151 | parametric |

PC1 carries 78.05% of the variance with six positive loadings of near-equal size, 0.374
to 0.443. The dominant structure is a general prominence axis on which all six engines
load alike: entities that one engine names often are entities the others name often. The
first two components carry 86.88% together, so the residual room for engine-specific
structure is 13.12% spread over four components.

PC2, at 8.82%, puts ChatGPT (0.683) and Groq (0.444) on one side and Perplexity (-0.447),
Claude (-0.304), Grok (-0.163) and Gemini (-0.134) on the other. That split does not
follow architecture: the one retrieval-augmented arm sits with three parametric arms.
It does not follow vendor either, since no two arms in this panel share a vendor.

**Table S3.4c.** Pearson correlation of engine coverage vectors. Same matrix as Table
S3.4a.

| | ChatGPT | Claude | Gemini | Groq | Perplexity | Grok |
|---|---:|---:|---:|---:|---:|---:|
| **ChatGPT** | 1.000 | 0.599 | 0.669 | 0.741 | 0.584 | 0.726 |
| **Claude** | 0.599 | 1.000 | 0.832 | 0.712 | 0.754 | 0.821 |
| **Gemini** | 0.669 | 0.832 | 1.000 | 0.726 | 0.710 | 0.896 |
| **Groq** | 0.741 | 0.712 | 0.726 | 1.000 | 0.623 | 0.756 |
| **Perplexity** | 0.584 | 0.754 | 0.710 | 0.623 | 1.000 | 0.862 |
| **Grok** | 0.726 | 0.821 | 0.896 | 0.756 | 0.862 | 1.000 |

Dendrogram, average linkage on 1 minus Pearson correlation, merges in order of height:

```
0.104   Gemini ........................ Grok
0.173   Claude ........................ (Gemini + Grok)
0.225   Perplexity .................... (Claude + Gemini + Grok)
0.259   ChatGPT ....................... Groq
0.326   (Perplexity + Claude + ......   (ChatGPT + Groq)
         Gemini + Grok)
```

The tree does not recover architecture. Perplexity, the only retrieval-augmented arm,
joins a cluster of three parametric arms at height 0.225, well before the final split at
0.326. The outer split separates ChatGPT and Groq from everything else. ChatGPT is a
hosted proprietary model and Groq is an open-weights Llama served on third-party
hardware, so the pairing is not a vendor or a licensing grouping either. With six objects
the tree is a description of one correlation matrix, not a test of any taxonomy, and the
honest reading of Table S3.4a plus this tree is that the engines differ along one shared
prominence axis and a small residue that matches no declared architectural label.

---

## 6. Firm effect against engine effect

**Table S3.4-bis.** Two-way decomposition of logit coverage. Series 2026-04-23 to
2026-09-08, 62 entities by 6 engines, balanced with one observation per cell, rates
offset by 1/(2 x 42,487) before the logit.

| Source | Sum of squares | Share of total |
|---|---:|---:|
| Entity (firm) | 1,880.12 | 34.46% |
| Engine | 1,429.96 | 26.21% |
| Residual (entity x engine interaction) | 2,145.56 | 39.33% |

**Table S3.4d.** Share of cell-level variance in the binary outcome explained by single
factors. Series 2026-04-23 to 2026-09-08, 42,487 cells, denominator is total sum of
squares of `cited_win`.

| Factor | Levels | R² |
|---|---:|---:|
| Engine | 6 | 0.1551 |
| Query | 192 | 0.3220 |
| Query type | 2 | 0.0436 |
| Vertical | 4 | 0.0350 |
| Query language | 2 | 0.0036 |
| Collection day | 53 | 0.0028 |
| Engine x query | 1,056 | 0.8252 |

The engine-by-query row fits one mean per cell of a 6 by 192 grid over 42,487
observations and is an in-sample upper bound, not an effect. It is reported because the
gap between it and the two main effects it contains (0.1551 and 0.3220) is the size of
the interaction.

The firm effect and the engine effect are of the same order, 34.5% against 26.2%, and
neither dominates. The largest single share, 39.3%, belongs to the interaction: which
firm an engine names is not the firm's general prominence shifted by an engine-specific
level. Day contributes 0.28% of cell-level variance, so instability across the five
months is not what is producing the disagreement.

---

## 7. Entities as the object

62 of the 127 cohort members (Fintech 31, Retail 32, Health 32, Technology 32) were named
by at least one engine inside the window on at least one day. 65 were never named by any
engine on any day.

**Table S3.5a.** Breadth distribution, where breadth is the number of engines that ever
named the entity. Series 2026-04-23 to 2026-09-08, 62 named entities, 12,050 entity
mentions, denominator for coverage is all cells of the entity's vertical across all
engines.

| Breadth | Entities | Median coverage | Mean coverage | Mentions | Share of all mentions |
|---:|---:|---:|---:|---:|---:|
| 1 | 20 | 0.00075 | 0.00188 | 400 | 3.32% |
| 2 | 15 | 0.00414 | 0.00567 | 893 | 7.41% |
| 3 | 13 | 0.01068 | 0.01235 | 1,694 | 14.06% |
| 4 | 7 | 0.01895 | 0.02413 | 1,766 | 14.66% |
| 5 | 3 | 0.03414 | 0.03447 | 1,109 | 9.20% |
| 6 | 4 | 0.12888 | 0.14097 | 6,188 | 51.35% |

Four entities are named by all six engines and account for 51.4% of every mention in the
series: Nubank (2,955 mentions, coverage 0.269), Mercado Livre (1,522, 0.139), Magazine
Luiza (1,304, 0.119) and Americanas (407, 0.037). Twenty entities are named by exactly
one engine and account for 3.3%.

**Table S3.5b.** Entities named by exactly one engine. Series 2026-04-23 to 2026-09-08,
denominator is all cells of that entity's vertical across all engines.

| Entity | Vertical | Only engine | Mentions | Trials | Coverage |
|---|---|---|---:|---:|---:|
| Walmart | Retail | Claude | 165 | 10,964 | 0.01505 |
| SAP | Technology | Perplexity | 47 | 10,143 | 0.00463 |
| CI&T | Technology | Perplexity | 39 | 10,143 | 0.00385 |
| Agibank | Fintech | Perplexity | 34 | 10,985 | 0.00310 |
| BTG Pactual | Fintech | Perplexity | 21 | 10,985 | 0.00191 |
| IBM Brasil | Technology | Perplexity | 15 | 10,143 | 0.00148 |
| Roche | Health | Perplexity | 13 | 10,395 | 0.00125 |
| Vtex | Technology | Perplexity | 11 | 10,143 | 0.00108 |
| eBay | Retail | Claude | 10 | 10,964 | 0.00091 |
| CloudWalk | Fintech | Perplexity | 9 | 10,985 | 0.00082 |
| SulAmérica Saúde | Health | Perplexity | 7 | 10,395 | 0.00067 |
| Target | Retail | Gemini | 6 | 10,964 | 0.00055 |
| NotreDame Intermédica | Health | Perplexity | 5 | 10,395 | 0.00048 |
| TCS | Technology | Perplexity | 5 | 10,143 | 0.00049 |
| Tivit | Technology | Perplexity | 4 | 10,143 | 0.00039 |
| Dock | Fintech | Perplexity | 2 | 10,985 | 0.00018 |
| Grupo Boticário | Retail | Perplexity | 2 | 10,964 | 0.00018 |
| Sinqia | Technology | Perplexity | 2 | 10,143 | 0.00020 |
| Wise | Fintech | Perplexity | 2 | 10,985 | 0.00018 |
| Salesforce | Technology | Perplexity | 1 | 10,143 | 0.00010 |

Seventeen of the twenty belong to Perplexity, the one retrieval-augmented arm, and they are
mid-cap and long-tail names (Agibank, CloudWalk, Dock, Sinqia, Tivit, Vtex). A firm whose
only route into a generative answer runs through one engine is measurable on that engine
and invisible everywhere else, which is the single-vendor problem stated at the level of
the firm rather than the buyer.

### Model S3.5

Declared before estimation: mentions of entity *e* are modelled as Binomial with the
entity's trial count, logit link, breadth as the only predictor.

```
hits_e ~ Binomial(trials_e, pi_e),   logit(pi_e) = b0 + b1 * breadth_e
```

Estimated on 62 entities, 656,201 trials and 12,050 mentions. b1 = 0.8574. The iid
standard error (0.0064) is not usable: the Pearson overdispersion scale is 111.5, because
the same firm is named in bursts within a query and within a day. The quasi-binomial
standard error is 0.0671. Odds ratio per additional engine 2.357, 95% interval
[2.067, 2.688]. Residual deviance 6,040.9 on 60 degrees of freedom against a null
deviance of 28,600.5, deviance pseudo-R² 0.789. Spearman rho between breadth and coverage
0.826 (p = 1.4e-16).

Breadth and coverage are computed from the same mention counts, so the odds ratio
describes the shape of a concentration rather than predicting anything. What it
establishes is that the shape is steep and monotone: each additional engine that has ever
named a firm corresponds to roughly a 2.4-fold increase in the odds of that firm being
named in any given cell, with no breadth level breaking the ordering.

---

## 8. How much of the observed agreement is above chance

### 8.1 Permutation null for Fleiss

Each engine's column is permuted independently across cells, which destroys cell-level
association and preserves every engine's base rate. This is the null that "beyond
chance" in kappa refers to; sampling error puts its realised centre slightly below zero.

**Table S3.6a.** Observed Fleiss against a marginal-preserving permutation null. Series
2026-04-23 to 2026-09-08, 2,000 replications per panel, denominator is complete panel
cells.

| Panel | k | Cells | Observed | Null mean | Null SD | Null p95 | z | p |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| P1 | 3 | 9,129 | 0.0861 | -0.0390 | 0.0052 | -0.0306 | 24.02 | < 0.0005 |
| P2 | 4 | 8,550 | 0.1692 | -0.0240 | 0.0038 | -0.0175 | 50.18 | < 0.0005 |
| P3 | 4 | 542 | 0.2263 | -0.0228 | 0.0156 | 0.0038 | 15.92 | < 0.0005 |
| P4 | 5 | 4,231 | 0.1464 | -0.0424 | 0.0039 | -0.0358 | 47.89 | < 0.0005 |
| P5 | 5 | 278 | 0.2359 | -0.0282 | 0.0170 | 0.0008 | 15.53 | < 0.0005 |

No panel is compatible with independence. The observed agreement sits 15.5 to 50.2 null
standard deviations above the null mean, and zero of 2,000 permutations reached the
observed value in any panel. The engines are not independent instruments. They are also
not interchangeable ones: on P1 the distance from the null is 0.125 kappa points while
the distance from perfect agreement is 0.914.

### 8.2 Uniform-draw null for the entity sets

Using `src/analysis/null_simulation.simulate_jaccard_null` with two raters, each drawing
top_k cohort members uniformly at random. Both simulated raters name something by
construction, so the comparator is the both-named observed Jaccard, not the pooled one.

**Table S3.6b.** Mean Jaccard of two independent uniform draws. 2,000 simulations per
row, seed 20260911.

| Vertical | Named universe (size) | top_k = 1 | top_k = 2 | top_k = 3 | Extractor cohort (size) | top_k = 1 | top_k = 2 | top_k = 3 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Fintech | 15 | 0.0625 | 0.0895 | 0.1362 | 31 | 0.0280 | 0.0412 | 0.0604 |
| Retail | 13 | 0.0655 | 0.1003 | 0.1555 | 32 | 0.0290 | 0.0375 | 0.0597 |
| Health | 16 | 0.0590 | 0.0813 | 0.1215 | 32 | 0.0290 | 0.0375 | 0.0597 |
| Technology | 18 | 0.0500 | 0.0738 | 0.1092 | 32 | 0.0290 | 0.0375 | 0.0597 |

**Table S3.6c.** Observed pairwise Jaccard by vertical. Series 2026-04-23 to 2026-09-08,
denominator in columns 2 and 3 is cell-pairs where at least one engine named an entity;
in columns 4 and 5, cell-pairs where both did.

| Vertical | Scored cell-pairs | Mean Jaccard | Both named | Mean Jaccard, both named |
|---|---:|---:|---:|---:|
| Fintech | 8,800 | 0.2128 | 2,185 | 0.8569 |
| Retail | 7,613 | 0.0970 | 2,001 | 0.3692 |
| Health | 3,749 | 0.0345 | 510 | 0.2535 |
| Technology | 3,787 | 0.0411 | 292 | 0.5332 |

Against a null that draws one name from the named universe (0.050 to 0.066), the
both-named observed values are 4.3 to 13.7 times the null: fintech 0.857 against 0.063,
technology 0.533 against 0.050, retail 0.369 against 0.066, health 0.254 against 0.059.
Raising the draw to two names, which is closer to the observed mean of 1.55 entities per
named cell, the multiples run 3.1 to 9.6. Against the pooled observed values, which
include cells where only one engine named anyone, the multiple falls to 0.58 (health) and
0.82 (technology), both below the null, with retail at 1.48 and fintech at 3.40. The gap between the two rows is the same gap Table S3.3a reports, seen
against a simulated floor.

---

## 9. The observation window

The five truncated arms make "the engine did not name the firm" indistinguishable from
"the recorded text ended before it did". Three days near the end of the series retained
the complete response, which permits the comparison on identical cells.

**Table S3.7a.** The same rows under two apertures. Series 2026-09-06 to 2026-09-08,
1,553 rows with the full response retained, denominator is rows per engine.

| Engine | Rows | Cited, 200-char window (%) | Cited, full text (%) | Delta (pp) | Median full length | Mean entities, window | Mean entities, full |
|---|---:|---:|---:|---:|---:|---:|---:|
| ChatGPT | 192 | 17.19 | 53.65 | +36.46 | 1,894 | 0.23 | 1.86 |
| Claude | 192 | 25.00 | 66.15 | +41.15 | 1,130 | 0.35 | 2.34 |
| Gemini | 480 | 3.54 | 39.79 | +36.25 | 3,152 | 0.06 | 2.12 |
| Perplexity | 209 | 55.02 | 78.47 | +23.44 | 523 | 1.09 | 2.56 |
| Grok | 480 | 32.92 | 86.67 | +53.75 | 2,028 | 0.70 | 4.48 |

**Table S3.7b.** Fleiss on identical cells under both apertures. Series 2026-09-08,
denominator is complete cells on that day.

| Aperture | Engines | k | Cells | Base rate | Fleiss kappa |
|---|---|---:|---:|---:|---:|
| 200-char window | ChatGPT+Claude+Gemini+Grok | 4 | 192 | 0.182 | 0.2371 |
| Full text | ChatGPT+Claude+Gemini+Grok | 4 | 192 | 0.672 | **0.4881** |
| 200-char window | the four plus Perplexity | 5 | 96 | 0.302 | 0.2342 |
| Full text | the four plus Perplexity | 5 | 96 | 0.798 | 0.2248 |

**Table S3.7c.** Pairwise agreement on identical cells, both apertures. Series
2026-09-08, denominator is shared cells that day.

| Pair | n | Kappa, window | Kappa, full | Mean Jaccard, window | Mean Jaccard, full |
|---|---:|---:|---:|---:|---:|
| Claude–Gemini | 192 | 0.1262 | 0.6334 | 0.0433 | 0.2967 |
| ChatGPT–Gemini | 192 | 0.2552 | 0.5746 | 0.0711 | 0.2772 |
| ChatGPT–Claude | 192 | 0.2093 | 0.5306 | 0.1490 | 0.2665 |
| Claude–Grok | 192 | 0.4324 | 0.5159 | 0.2380 | 0.3223 |
| Gemini–Grok | 192 | 0.1487 | 0.4297 | 0.0566 | 0.3916 |
| Gemini–Perplexity | 96 | 0.0667 | 0.3117 | 0.0204 | 0.2320 |
| ChatGPT–Grok | 192 | 0.2700 | 0.2976 | 0.2065 | 0.2764 |
| ChatGPT–Perplexity | 96 | 0.2619 | 0.1464 | 0.1477 | 0.2238 |
| Perplexity–Grok | 96 | 0.4134 | 0.1264 | 0.3433 | 0.3216 |
| Claude–Perplexity | 96 | 0.2251 | 0.0975 | 0.1810 | 0.2316 |

Among the four fully truncated arms, widening the aperture roughly doubles Fleiss, from
0.2371 to 0.4881, and raises every pairwise kappa, with Claude–Gemini moving from 0.126
to 0.633. Mean Jaccard rises for all ten pairs except Perplexity–Grok. A substantial part
of what Section 2 measures as engine disagreement is the window.

The four pairs containing Perplexity move the other way. Perplexity is at 78.5% under
full text and Grok at 86.7%, and kappa loses discriminating power as prevalence
approaches the ceiling: Perplexity–Grok falls from 0.413 to 0.126 while its observed agreement rises
from 0.708 to 0.802 and its mean Jaccard is flat (0.343 to 0.322). The drop is a property
of the coefficient at extreme marginals, not a loss of agreement. This is why the
five-arm Fleiss under full text (0.2248) should not be compared with the four-arm figure
(0.4881): the two panels sit at different base rates.

**Table S3.8.** Fleiss on the outcome as stored against the harmonised outcome. Series
2026-04-23 to 2026-09-08, denominator is complete panel cells.

| Panel | Engines | k | Cells | Kappa, stored | Kappa, harmonised | Difference |
|---|---|---:|---:|---:|---:|---:|
| P1 | ChatGPT+Claude+Gemini | 3 | 9,129 | 0.0861 | 0.0861 | 0.0000 |
| P2 | P1 + Groq | 4 | 8,550 | 0.1692 | 0.1692 | 0.0000 |
| P3 | P1 + Grok | 4 | 542 | 0.2263 | 0.2263 | 0.0000 |
| P4 | P2 + Perplexity | 5 | 4,231 | 0.0604 | 0.1464 | +0.0860 |
| P5 | P3 + Perplexity | 5 | 278 | 0.1717 | 0.2359 | +0.0642 |

Analysing the series on the outcome as stored understates agreement by 0.086 on P4 and
0.064 on P5, in both cases because one arm was read through a different aperture. A study
that compared engines on this database without harmonising the window would have reported
Perplexity as further from the other engines than it is.

---

## 10. Interpretation

**Citation rate is a property of the pair, not of the firm and not of the engine.** The
two-way decomposition of logit coverage gives the firm 34.5% of the variance, the engine
26.2%, and the firm-by-engine interaction 39.3%. No single-engine measurement recovers a
firm-level quantity, because the largest term is the one that says which firm gets named
depends on which engine is asked.

**The engines disagree far more about whether than about whom.** Binary Fleiss on the
panel that spans the full five months is 0.086, and mean pairwise Cohen's kappa across
the fourteen defined pairs is 0.219. Restricted to the 4,988 cell-pairs where both
engines named at least one company, mean Jaccard is 0.42 to 0.79 by pair against a
uniform-draw null of 0.05 to 0.07, and 65.3% of those cell-pairs share the first-named
company. The prominence ordering inside a vertical also travels: PC1 of the
entity-by-engine coverage matrix carries 78.1% of the variance with six positive loadings
of near-equal size, and median Kendall tau-b is 0.52 in fintech and 0.58 in retail.

**Part of the "whether" disagreement is the instrument.** On the three days that retained
full responses, widening the aperture from 200 characters to the whole response doubles
four-arm Fleiss from 0.237 to 0.488 and raises Claude–Gemini from 0.126 to 0.633. The
window is not a nuisance parameter here; it is the largest single lever on the headline
agreement number.

**The panel does not cluster by architecture or by vendor.** The one retrieval-augmented
arm joins three parametric arms at height 0.225, before the final split at 0.326, and the
outer division separates ChatGPT and Groq from the rest. PC2, the first component with
any room for architectural structure, carries 8.8% and groups a hosted proprietary model
with an open-weights model served on third-party hardware. Whatever distinguishes these
engines from one another in their naming behaviour is not the label the manuscript
assigns them in Table 3.

**For a buyer.** A rate quoted without its engine, its query battery and its observation
window is uninterpretable: the same cohort and the same battery, on the same days,
produce 1.91% on Gemini and 53.09% on Perplexity. Ranking within a vertical is the part
of the measurement that survives a change of vendor; the level is not. And a firm named
by only one engine is not a firm with a low rate, it is a firm with no rate outside that
engine: seventeen of the twenty single-engine entities in this series are visible
only through Perplexity.

---

## What this does not establish

1. **Silence against truncation.** The harmonised outcome cannot distinguish an engine
   that did not name a cohort member from an engine whose recorded text stopped before it
   did. Section 9 bounds the effect on three days and finds it large (23.4 to 53.8
   percentage points per arm), but those three days are not the series, and no
   window-corrected agreement figure exists for 2026-04-23 to 2026-09-05.

2. **Engine identity against model version.** Gemini was collected under two model
   identifiers (`gemini-2.5-pro`, 10,939 rows; `gemini-2.5-flash`, 4,416 rows) and is
   treated as one rater. Every kappa involving Gemini therefore mixes two configurations.

3. **The six-engine question is not answered.** Groq's last day precedes Grok's first, so
   the six-way panel has zero cells. Every Groq-to-Grok comparison in this section is
   between disjoint periods and is confounded with time, model release and collection
   regime. The largest panels are five arms wide, and only on the 96-query half-battery.

4. **Agreement between engines against agreement as read by one extractor.** All outcomes
   pass through a single regex extractor over a fixed cohort, with no human-annotated
   ground truth. Two engines that name the same firm in forms the extractor treats
   differently are recorded as disagreeing. The project's own
   `src/analysis/kappa_validator.py` exists precisely because that validation is
   outstanding; it has not been run on this series.

5. **The ceiling.** Between-engine kappa is compared against 1 throughout, but same-day
   test-retest kappa is 0.669 for Perplexity and 0.725 for Grok. Part of what is counted
   as between-engine disagreement for those two arms is within-engine instability, and
   this section does not decompose the two.

6. **Interval coverage on the Grok panels.** P3 and P5 rest on three collection days, so
   a day-cluster bootstrap has three clusters. Their intervals are reported for symmetry
   and should not be read as coverage statements.

7. **The latent structure is description.** PCA and hierarchical clustering run on six
   columns. With six objects, no dendrogram height is a test, and the statement that the
   panel does not cluster by architecture is a failure to find structure in six points,
   not evidence that no such structure exists.

8. **The breadth model is mechanically dependent.** Breadth and coverage derive from the
   same mention counts, so Model S3.5 cannot predict coverage from breadth in any useful
   sense. It characterises the steepness of an observed concentration.

9. **Nothing causal.** This section says nothing about what makes a firm citable, whether
   a firm can act to change its rate, or whether any engine's naming behaviour tracks a
   firm's real-world standing. The cohort is fixed, the battery is fixed, and no
   intervention was performed.

---

## Reproduction

```
cd docs/research/methods-paper/journal-v2/stats
python s3_agreement.py --boot 2000 --nullsim 2000
```

Runtime 107 seconds without a cache and 30 with, on the machine of record.
`--cache <path.pkl>` stores the extraction pass. The script opens the database read-only and writes nothing; all output
goes to stdout as markdown.
