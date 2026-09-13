## 6. The observation window

### 6.1 One parameter, two measurands

Entity extraction runs over a string, and that string is whatever the pipeline retained rather than the model's answer. Its length is parameter P1, the observation window, and on the 2,225 responses this study stored whole it moves the citation rate by between 22.95 and 55.73 percentage points depending on the engine, with no other parameter touched.

Both values of the parameter answer a real question. A narrow window measures *head-of-response citation*, whether the entity appears in the opening a reader sees before deciding whether to keep reading, which is the quantity a click-through argument needs. A wide window measures *whole-response citation*, whether the entity appears anywhere in the text the engine produced, which is the quantity an attribution argument needs. Either is defensible. Leaving the choice unstated is what breaks comparison, because two figures produced under two windows are estimates of two different quantities and their difference carries no information about the engines.

Metrology has a name for this. A citation rate reported without its window skips the requirement of VIM 2.3 Note 1, and VIM 2.27 names the resulting component, definitional uncertainty [JCGM200]; §1.2 states the two notes to that clause and what they cost an interval derived from sample size alone. The window movement in Table D2 is an instance of Note 2 and it sits at the floor Note 1 describes. Calling it measurement error concedes the wrong thing, since error implies a correct value that better technique approaches, and no sample size, no better extractor and no additional collection day closes a gap between two questions. The uncertainty budget of §3 lists P1 as a Type B component [JCGM100]; this section supplies its measured value.

### 6.2 How the asymmetry arose, and why nothing detected it

In five of six client adapters the stored extraction string was cut at 200 characters by the line `response_text = text[:200]`. The sixth stored up to 2,502 characters. The cut was a property of the client rather than of the measurement design, written for log volume rather than for a reading of the construct, and it was therefore invisible to every check that operated on the stored field.

§5.3 gives the detection history: no functional control saw the asymmetry, and a distributional check found it.

**Table D1.** Length in characters of `citations.response_text`, the string entity extraction actually read. Series 2026-04-23 to 2026-09-08, 68,624 canonical observations, denominator is canonical rows with a non-null `response_text`, by engine.

| Engine | n | Mean chars | Min | Max | Share exactly 200 |
|---|---:|---:|---:|---:|---:|
| Gemini | 15,355 | 195.7 | 87 | 200 | 92.6% |
| ChatGPT | 15,168 | 200.0 | 200 | 200 | 100.0% |
| Claude | 15,034 | 200.0 | 200 | 200 | 100.0% |
| Groq | 14,208 | 200.0 | 200 | 200 | 100.0% |
| Perplexity | 7,741 | 668.0 | 198 | 2,502 | 3.9% |
| Grok | 1,118 | 200.0 | 179 | 200 | 99.9% |

A variable whose maximum equals its minimum across 15,168 observations is reporting a boundary rather than measuring a length. Gemini and Grok fall marginally short of the ceiling, which is what an arm that occasionally answers in fewer characters than the cap looks like once the cap is imposed. The 305 Perplexity rows now sitting at exactly 200 were collected after the uniform window was applied at collection time on 2026-08-31, which is why that arm's mean sits at 668.0 against the 687.2 of the series that closed on 2026-08-31.

P1 is a conformance requirement because of where its value gets set. Position effects in generated output are already measured: models are sensitive to the order of candidates they are given [Liu2024, Guo2024], position bias in generated recommendation and reranking is a venue-accepted phenomenon [Hou2024, Bito2026], and the effect is model-specific in ways that track neither provider nor capability [Menschikov2025, Wadi2026]. What this study adds is about the instrument, and it is the conversion P1 describes (§3.1): the cut-off that performs it differs between providers, which places the variation exactly where cross-engine comparison lives.

### 6.3 One arm moves 22.8 points on re-extraction

Re-extraction over the full series under a uniform 200-character window moves one arm. Perplexity falls from 74.9% [73.9, 75.8] as collected to 52.0% [50.9, 53.1] under the uniform window, a difference of 22.8 percentage points over the 7,435 rows whose stored text exceeded the window, and the panel falls from 20.5% to 18.0% on 68,624 canonical observations. On the series that closed on 2026-08-31, the same contrast runs 75.7% against 51.9% over 66,399 observations, a difference of 23.8 points; the gap between that figure and the one above is the 305 rows collected under the uniform window after 2026-08-31, which the earlier snapshot did not contain.

Under the same re-extraction the other five arms show deltas of exactly zero, and those zeros are identity by construction and not independent verification. Applying a 200-character window to a string that is already 200 characters long is the identity operation, so the zero is guaranteed before any data is read. What those rows do confirm is narrower and still worth having: re-extraction is deterministic and the cohort did not change between runs. Reading them as evidence that the window does not matter on the parametric arms is the misreading the comparison invites, and §6.4 shows what it would have cost.

### 6.4 Every arm gains and no arm loses

Inside the arm, on identical observations, reading the whole response instead of the first 200 characters moves the rate by 22.95 to 55.73 points and loses no citation. Since migration 0010 the pipeline writes the whole response to `citations.response_full_text` while continuing to write the windowed string to `response_text`, which is what makes the comparison a within-observation one: extract over `response_full_text[:200]`, extract over `response_full_text`, hold the cohort, the battery and the matching rule fixed, and read the difference. Two identity checks run first and both pass on all 2,225 rows: `response_text` equals `response_full_text[:200]`, so the two columns are two views of one response, and re-extraction of the first 200 characters reproduces the stored `cited_v2` exactly, so the rule used here is the rule that produced the series.

**Table D2.** Citation rate at 200 characters against citation rate on the whole response, same observations, same matching rule. Series 2026-09-06 to 2026-09-08, 2,225 canonical observations, denominator is the engine's own observations retaining a full response. Intervals are 10,000-replicate bootstrap percentiles with query clusters resampled; McNemar is the exact two-sided binomial on the discordant pairs.

| Engine | n | Rate at 200 [95% CI] | Rate on full [95% CI] | Δ pp | Bootstrap 95% CI | Gains | Losses | Exact McNemar p | Design effect |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Perplexity | 305 | 54.10 [48.49, 59.61] | 77.05 [72.01, 81.41] | +22.95 | [16.8, 29.6] | 70 | 0 | 1.69e-21 | 1.83 |
| Gemini | 768 | 2.60 [1.69, 3.99] | 33.33 [30.09, 36.74] | +30.73 | [27.3, 34.0] | 236 | 0 | 1.81e-71 | 1.05 |
| ChatGPT | 192 | 17.19 [12.51, 23.15] | 53.65 [46.59, 60.56] | +36.46 | [29.7, 43.2] | 70 | 0 | 1.69e-21 | 0.99 |
| Claude | 192 | 25.00 [19.41, 31.57] | 66.15 [59.19, 72.46] | +41.15 | [34.4, 47.9] | 79 | 0 | 3.31e-24 | 0.99 |
| Grok | 768 | 28.39 [25.31, 31.68] | 84.11 [81.36, 86.53] | +55.73 | [50.1, 61.6] | 428 | 0 | 2.89e-129 | 2.71 |

Losses are zero on every arm. Not one observation classified as citing at 200 characters loses that classification when more text is read, which makes the 200-character rate a lower bound on the whole-response rate at the level of the individual observation and not only in aggregate. The smallest effect in the table, Perplexity at +22.95 points, stands against a paired minimum detectable difference of 12.5 points for that arm at alpha 0.05 and power 0.80, and the other four clear their own thresholds by factors of 2.9 to 5.3.

Two consequences follow for the argument the manuscript has been making. The 23.8 points of §6.3 are the smallest of the five effects, so a figure computed on the truncated series understates the parameter's influence on the panel it is drawn from rather than bounding it. The retrieval-augmented arm is the one the narrow window damages least, which closes the architectural account: an explanation that predicted retrieval-augmented composition as the source of late naming predicts the opposite of what the matched comparison shows.

The Gemini row needs stratifying before it is read. On 2026-09-06 the API returned responses that were themselves cut at the origin, 384 observations with a mean stored full length of 143 characters, of which 378 sit at or below 200 characters and the measured delta for that day is exactly 0.0 points. Restricted to the 390 Gemini observations longer than the window, the delta is +60.51 points on a median full length of 3,423 characters; restricted instead to the collection days 2026-09-07 and 2026-09-08, it is +61.5 points on 384 observations. The pooled row of Table D2 describes a mixture of two collection regimes.

The other end of the response is censored as well, and the censoring runs in the direction that makes the whole-response rate a floor.

**Table D3.** Stored responses ending without terminal punctuation, applied to `response_full_text` under the criterion published as `TERMINAL_RE` in `s5_window_validity.py`. Series 2026-09-06 to 2026-09-08, 2,225 canonical observations, denominator is the engine's own observations.

| Engine | n | Ends mid-sentence | Share | 95th percentile length | Max length |
|---|---:|---:|---:|---:|---:|
| ChatGPT | 192 | 0 | 0.0% | 3,688 | 4,088 |
| Claude | 192 | 2 | 1.0% | 1,728 | 3,072 |
| Gemini | 768 | 648 | 84.4% | 4,085 | 19,777 |
| Grok | 768 | 70 | 9.1% | 3,698 | 4,263 |
| Perplexity | 305 | 1 | 0.3% | 848 | 1,032 |

The criterion is crude and calls a response ending in a bare bullet item incomplete, so it is reported as a diagnostic and never used to filter a rate. At 84.4% of 768 observations the Gemini figure is too large to be an artifact of list formatting, and the tails end mid-word. Gemini's whole-response rate of 33.33% is therefore a floor on the quantity and not an estimate of it, its window delta sits at a floor for the same reason, and the recovery quantiles of Table D5 are longer than reported. Grok carries the same bias on 9.1% of its observations. The three remaining arms are effectively uncensored.

### 6.5 The curve, and what it does to a ranking

A two-point contrast cannot tell an adopter where to set the parameter, so the same rows were re-extracted at ten grid windows and on the whole response.

**Table D4.** Citation rate by observation window, recomputed over the identical observation set with the matching rule held fixed. Series 2026-09-06 to 2026-09-08, 2,225 canonical observations, denominator is all canonical observations of that engine retaining a full response. Rates in percentage points; Wilson intervals for every cell are in `stats/data/s5_window_curve_by_engine.csv`.

| Engine | n | 50 | 100 | 150 | 200 | 300 | 400 | 600 | 800 | 1,200 | 1,600 | Full | Saturation |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ChatGPT | 192 | 1.0 | 3.6 | 11.5 | 17.2 | 35.9 | 41.7 | 45.8 | 47.9 | 51.0 | 52.6 | 53.6 | full |
| Claude | 192 | 0.5 | 5.2 | 14.6 | 25.0 | 43.8 | 52.6 | 58.3 | 62.0 | 65.6 | 66.1 | 66.1 | 1,200 |
| Gemini | 768 | 0.3 | 1.6 | 2.3 | 2.6 | 4.8 | 10.4 | 17.1 | 18.5 | 21.6 | 26.0 | 33.3 | full |
| Grok | 768 | 17.7 | 21.4 | 24.5 | 28.4 | 39.6 | 50.1 | 61.3 | 67.6 | 75.4 | 79.0 | 84.1 | full |
| Perplexity | 305 | 14.1 | 29.5 | 43.6 | 54.1 | 64.6 | 72.1 | 75.4 | 76.7 | 77.0 | 77.0 | 77.0 | 800 |

Saturation is the narrowest grid window whose rate falls within 1.0 percentage point of the whole-response rate and stays within it at every wider grid window. Two arms of five saturate inside the grid, Perplexity at 800 characters and Claude at 1,200; ChatGPT, Gemini and Grok are still climbing at 1,600, and Gemini gains a further 7.3 points between 1,600 characters and the whole response.

The ordering of engines changes along the curve. At 50 characters Grok leads at 17.7% and Perplexity follows at 14.1%; from 100 through 1,200 characters Perplexity leads; from 1,600 characters onward Grok leads again and reaches 84.1% on the whole response, with Perplexity second at 77.0%. ChatGPT sits above Claude at 50 characters and below it at every wider window. A published ranking of engines by citation rate is therefore a statement about the window, and one that does not declare its window cannot be compared with any other.

The inverse function is what an adopter actually needs: given a tolerance for missed mentions, how wide must the window be.

**Table D5.** Window in characters required to recover a given fraction of first mentions, computed as the narrowest window from which an observation is classified as citing and stays so at every wider grid window. Series 2026-09-06 to 2026-09-08, 1,367 canonical observations cited on the whole response, denominator is the engine's own cited-on-full observations.

| Engine | Cited on full | w50 | w80 | w90 | w95 | Median first-mention offset |
|---|---:|---:|---:|---:|---:|---:|
| ChatGPT | 103 | 275 | 500 | 850 | 1,100 | 245 |
| Claude | 127 | 275 | 450 | 700 | 850 | 241 |
| Gemini | 256 | 600 | 1,700 | 2,250 | 2,500 | 550 |
| Grok | 646 | 350 | 800 | 1,300 | 1,800 | 312 |
| Perplexity | 235 | 150 | 275 | 400 | 450 | 114 |
| All | 1,367 | 300 | 750 | 1,400 | 1,900 | 284 |

The canonical 200-character window recovers 35.4% of the first mentions across the panel, and between 7.8% on Gemini and 70.2% on Perplexity by engine. No window below 2,500 characters reaches 95% recovery on every arm. At the 95% target the required count runs from 450 characters on Perplexity to 2,500 on Gemini, a factor of 5.6, and the spread is of the same order at the 80% and 90% targets. An adopter should therefore declare the window as a recall target together with the count that delivered it on the panel measured; a bare character count means a different thing on each arm.

**Figure D1.** Citation rate and recovery of first mentions as functions of the observation window. Panel (a) gives the citation rate of each arm when entity extraction runs over the first k characters of the stored response, k from 50 to 1,600 on a logarithmic scale, with the open marker at the right showing the rate on the whole response; the dashed vertical marks the 200-character window declared in the reference instantiation. Panel (b) gives the share of first mentions already recovered at k, with the 95% line marked. Both panels are computed on the same 2,225 canonical observations with a full response retained, collected 2026-09-06 to 2026-09-08 under the uniform matching rule of P6, so each arm is compared against itself rather than against another arm. The lead changes hands three times along the curve, which is the property that makes an undeclared window incomparable. Drawn from `stats/data/s5_window_curve_by_engine.csv` and `stats/data/s5_mention_recovery_curve.csv`.

### 6.6 What is left of the mechanism

The discourse-structure account, that retrieval-augmented engines compose after fetching sources and therefore defer naming, is refuted by Table D2, and the relative-position evidence that supported it does not survive the removal of the truncation either.

**Table D6.** Position of the first cohort mention on the rows that retained the whole response, where the denominator of the relative offset is the real length of the answer and a first mention past character 200 is counted instead of lost. Series 2026-09-06 to 2026-09-08, 1,367 canonical observations naming an entity, denominator is the engine's own naming observations.

| Engine | Rows naming an entity | First mention beyond the window | Median response length | Median absolute offset | Median relative offset |
|---|---:|---:|---:|---:|---:|
| ChatGPT | 103 | 70 | 1,123 | 245 | 0.216 |
| Claude | 127 | 79 | 1,094 | 241 | 0.225 |
| Gemini | 256 | 236 | 3,407 | 550 | 0.191 |
| Grok | 646 | 428 | 1,778 | 312 | 0.223 |
| Perplexity | 235 | 70 | 491 | 114 | 0.227 |

Measured on the whole text, relative position does not separate the engines: Kruskal-Wallis returns H = 7.7 on 4 degrees of freedom, p = 0.104, epsilon-squared 0.0027, and the five medians fall in a band from 0.191 to 0.227. On the same rows the absolute offsets separate them decisively, H = 277.7, p < 0.0001, epsilon-squared 0.2010. The difference in position dissolves when the offset is divided by the length of the response, which means the engine ranking on absolute offset is a joint statement about where an engine starts naming and how long it writes. Any relative-position claim built on the truncated series would have been an artefact of the truncation, because for five of six arms the denominator was the constant 200 whenever the answer reached that length, which inflates the relative offset by an amount that grows with the text discarded.

Hypothesis H6 stated that susceptibility to a narrow window varies across engines and is predicted by preamble share rather than by engine class. It splits.

**Table D7.** Preamble share and window damage by engine, with the two competing predictors. Series 2026-09-06 to 2026-09-08, 2,225 canonical observations, denominator is the engine's own observations; median first-mention offset is computed on observations cited on the whole response.

| Engine | n | Preamble | Share [95% CI] | Δ 200→full pp | Median full length | Median first offset | Engine class |
|---|---:|---:|---:|---:|---:|---:|---|
| ChatGPT | 192 | 0 | 0.00 [0.00, 1.96] | +36.46 | 1,894 | 245 | parametric |
| Claude | 192 | 0 | 0.00 [0.00, 1.96] | +41.15 | 1,130 | 241 | parametric |
| Gemini | 768 | 280 | 36.46 [33.13, 39.92] | +30.73 | 452 | 550 | parametric |
| Grok | 768 | 74 | 9.64 [7.74, 11.93] | +55.73 | 1,991 | 312 | parametric |
| Perplexity | 305 | 14 | 4.59 [2.75, 7.56] | +22.95 | 528 | 114 | retrieval-augmented |

The negative half survives. Engine class does not order the damage: the four parametric arms span the whole range from +30.73 to +55.73 points and the single retrieval-augmented arm sits at the bottom at +22.95. One engine in one class cannot test a taxonomy, and on the evidence available the architectural account explains nothing the style account explains better.

The positive half fails as stated. Preamble share does not order the engines. Across the five arms its Spearman correlation with the delta is −0.154 (p = 0.805) on the pooled cohort and +0.667 (p = 0.219) once the Gemini retention defect of 2026-09-06 is removed, while median response length and median first-mention offset both reach +0.900 (p = 0.037) on the same five points. In cell-level regressions over 20 engine-by-vertical cells, preamble carries no coefficient distinguishable from zero (−0.048, 95% CI [−0.459, +0.363]) until engine fixed effects absorb the between-engine variation, and the length term is the one that survives at +55.19 points of delta per log₁₀ character (95% CI [+25.63, +84.75], p = 2.53e-04).

Inside an engine, preamble predicts strongly. Among the 1,367 observations cited on the whole response, a logistic model of whether the 200-character window misses the citation gives preamble an odds ratio of 7.72 (95% CI [3.99, 14.94], p = 1.29e-09) holding log₁₀ response length and engine fixed, fitted on the 1,137 observations from the three arms with within-engine variation in preamble. A response that opens with a preamble places its first cohort mention 2.66 times further into the text (95% CI 2.10 to 3.36) than a response of the same length from the same engine. Grok shows the same pattern across verticals, with preamble share running from 2.6% in fintech to 16.7% in technology over cells of 192 observations each, and the window delta from +35.4 to +72.9 points over those same cells.

What replaces H6 is narrower and testable: the window delta is a function of how far into the response the first cohort mention falls, and preamble is one of at least two things that push it there, the other being sheer response length. Two cautions travel with every preamble figure above. The regular expression is a re-specification of a criterion described in prose and never committed, and it diverges from the shares computed under that prose criterion by up to 5.2 points on individual arms. Gemini's preamble share is 36.46% on the 768 observations of this three-day cohort against 80.03% on the 15,355 canonical observations of the full series under the same pattern, a difference between periods that leaves a five-point engine-level test weak evidence in either direction.

### 6.7 What BRGEO-1 requires, and what uniformity buys

Four requirements follow, and each carries the cost of skipping it.

**Uniformity.** One window, applied identically to every engine. The alternative is what this instrument did for four months: a comparison in which one arm was read through a different aperture than the other five, which is neither a repeatability nor a reproducibility condition in the sense of VIM 2.20 and 2.24 [JCGM200].

**Declaration.** The value published with the figure, for the reason §6.5 closes on.

**Retention of the whole response.** Full-response retention began with migration 0010, and it reaches 2,225 of the 68,624 canonical observations in this series, so every earlier observation is a string no third party can widen. The retired Groq arm is the irreversible case: it left the panel on 2026-08-16, contributes zero rows to Table D2, and the window effect on its 14,208 canonical observations is now unmeasurable because the text past character 200 was never written to disk. Retention is also the only reproducible artefact available, since hosted models do not reproduce their outputs exactly even at temperature zero [Atil2025, Coqueret2026].

**Sensitivity reporting.** The headline figure published under both windows, per engine, in the form of Table D2. Publishing one window only leaves a reader unable to tell a 22.95-point arm from a 55.73-point arm, which is the spread Table D2 measures.

Uniformity buys something the specification did not previously claim. Measured on identical cells on 2026-09-08 across the four fully truncated arms, Fleiss' kappa on the binary outcome rises from 0.2371 at the 200-character window to 0.4881 on the whole response, on 192 cells, with the base rate moving from 0.182 to 0.672; the Claude-Gemini pair moves from 0.126 to 0.633. Part of what the market reads as disagreement between models is the instrument. The gain does not extend to every pair: the four pairs containing the retrieval-augmented arm move the other way as prevalence approaches the ceiling, where kappa loses discriminating power, so Perplexity-Grok falls from 0.413 to 0.126 while its observed agreement rises from 0.708 to 0.802. Across the whole series the effect is smaller and runs in one direction: analysing the outcome as stored rather than harmonised understates agreement by 0.086 on the five-arm panel of 4,231 complete cells.

## 7. Calibration decoys and the refusal taxonomy

### 7.1 The decoys give the instrument an empirical false-positive floor

Sixteen fictitious entities, verified as non-existent before collection, sit inside the cohort that produced every rate in this paper. They cost nothing to carry and they answer a question the rate cannot answer about itself: how often the matching rule declares a cohort entity present in prose that contains no such entity.

**Table D8.** Spontaneous naming of a fictitious entity in answers to canonical queries, none of which contains a decoy name. Series 2026-04-23 to 2026-09-08, 68,624 canonical observations, denominator is canonical rows with a non-null `response_text`, by engine. Sixteen decoys, verified as non-existent before collection.

| Engine | Canonical n | Decoy in the 200-character window [95% CI] | Decoy in the text as stored [95% CI] |
|---|---:|---:|---:|
| ChatGPT | 15,168 | 0.000 [0.000, 0.025] | 0.000 [0.000, 0.025] |
| Claude | 15,034 | 0.000 [0.000, 0.026] | 0.000 [0.000, 0.026] |
| Gemini | 15,355 | 0.000 [0.000, 0.025] | 0.000 [0.000, 0.025] |
| Groq | 14,208 | 0.000 [0.000, 0.027] | 0.000 [0.000, 0.027] |
| Perplexity | 7,741 | 0.000 [0.000, 0.050] | 0.000 [0.000, 0.050] |
| Grok | 1,118 | 0.000 [0.000, 0.342] | 0.000 [0.000, 0.342] |
| **Panel** | **68,624** | 0.000 [0.000, 0.006] | 0.000 [0.000, 0.006] |

Zero occurrences in 68,624 observations and six engines, inside the window and in the stored text alike. The 95% Wilson upper bound on the panel is 0.0056%, which corresponds to 3.84 expected occurrences over the series. The bound is loose on the arm with the least data: Grok's 1,118 observations admit an upper bound of 0.342%, sixty times the panel figure, which is the price of an arm that entered on 2026-08-23 and contributed five collection days inside a seventeen-day calendar span.

The result bounds one failure mode and no other. It says that the extractor is not manufacturing cohort matches out of ordinary prose, which is the failure a word-boundary matcher on surfaces such as `Inter` or `Stone` would be expected to show. It says nothing about a model's willingness to describe an entity that does not exist when asked about it directly, which is the adversarial stratum of §7.2, and it cannot bound false positives on real names used in an unintended sense, because a decoy carries no such sense. The stored `fictional_hit` column is 0 on every canonical row, consistent with the table and not independent evidence for it, since that column was only ever populated on the probe stratum.

Two design choices make the floor readable. The decoy extractors are restricted to the sixteen fictitious names and run with no alias table and no exclusion contexts, so the count is the raw behaviour of the matcher on names that cannot be right, with none of the machinery that protects the real cohort. The decoys also travel inside the same battery, on the same days, through the same adapters as the 111 real entities, so the floor is estimated from the run that produced the rate instead of from a separate calibration exercise that an adopter would have to trust transfers. An adopter who publishes a conformance claim can carry the same construction at a cost of sixteen cohort slots out of 127, and the claim then arrives with the false-positive bound attached to it.

### 7.2 The refusal problem, and a taxonomy that is proposed rather than validated

The original criterion flagged a hallucination whenever the decoy name occurred in the response. The probe places that name in the prompt, so any response engaging with the question at all contains it, including a flat refusal.

**Table D9.** Adversarial probes: share flagged by the legacy hallucination criterion, and share of those flagged answers carrying an explicit refusal marker. Series 2026-04-23 to 2026-09-08, 17,919 probe observations; denominators are all probe rows for the first rate and the 17,328 flagged rows with non-empty text for the second.

| Engine | Probe n | Flagged by the legacy criterion [95% CI] | Of those, carrying an explicit refusal marker [95% CI] |
|---|---:|---:|---:|
| Gemini | 4,463 | 90.3 [89.4, 91.2] | 46.9 [45.3, 48.4] |
| ChatGPT | 4,416 | 97.3 [96.8, 97.8] | 67.4 [66.0, 68.8] |
| Claude | 4,384 | 100.0 [99.9, 100.0] | 92.4 [91.6, 93.2] |
| Groq | 4,096 | 99.7 [99.5, 99.8] | 61.7 [60.2, 63.2] |
| Grok | 368 | 99.5 [98.0, 99.9] | 50.3 [45.2, 55.4] |
| Perplexity | 192 | 85.4 [79.7, 89.7] | 15.2 [10.5, 21.5] |
| **Panel** | **17,919** | 96.7 [96.4, 97.0] | 66.8 [66.1, 67.5] |

That 96.7% of 17,919 probe responses were flagged is evidence that the marker was detecting the prompt. Of the 17,328 flagged responses carrying text, 11,569 (66.8%) contain an explicit refusal marker, among them a Gemini response of 2026-04-29 which states of the decoy named in its prompt, verbatim, that *o "Banco Floresta Digital" não é uma instituição financeira real ou registrada no Brasil*. The refusal regular expression counts only explicit markers, which puts 66.8% at the floor of the refusal share. Two counts of the 2026-08-31 snapshot circulate in the repository, 11,195 of 16,579 at 67.5% and 10,775 of 15,993 at 67.4%, neither recording which extraction produced its base; Table C2 carries the first. That three bases of 15,993, 16,579 and 17,328 return 67.4%, 67.5% and 66.8% is the only stability this figure has been given, and it is stability of the proportion rather than agreement on the count.

The engine spread is the operational result. Claude carries a refusal marker in 92.4% of its flagged answers and the retrieval-augmented arm in 15.2%, so a headline hallucination rate computed under the legacy criterion ranks engines mostly by how explicitly they decline. BRGEO-1 therefore specifies a three-way outcome: ontological refusal, where the model states the entity does not exist; epistemic refusal, where it states that it lacks information, typically citing a training cutoff, which is correct in effect and weaker in kind; and fabrication, where it describes products, history or positioning for an entity that has none. Only the third is a hallucination, and a protocol that pools all three reports a false-positive rate of 96.7% on 17,919 probe observations, of which 66.8% of the 17,328 flagged responses carrying text already show an explicit refusal marker, so the pooled figure counts refusals as hallucinations.

The taxonomy is proposed and not validated. There is no inter-annotator agreement, no human-labelled sample, no confusion matrix of the automatic classifier against a gold standard, and no measured distribution across the three categories. Estimating fabrication as the complement of a refusal detector is inference of the kind this paper criticises elsewhere: the residual contains refusals phrased outside the detector's vocabulary, empty responses, clarifying questions and answers about real homonyms. Fabrication requires positive detection of invented verifiable attributes, and §14 carries this as the principal open item in the specification. Validation also owes the abstention literature an explicit mapping. The survey of abstention in large language models sets out the field's own categories [Wen2025], unanswerable-question benchmarks measure the behaviour at question level [Kirichenko2025, Pan2026], and the entity-query surface these probes use has its own instruments [Jung2026, Zhao2024]. A three-way taxonomy that neither aligns with those categories nor says where it departs from them will be read as parallel invention.

### 7.3 Probe coverage excludes the arm worth probing

The probe stratum reaches the retrieval-augmented arm in 192 of 17,919 observations, 1.1% of the stratum. Each of the four parametric arms that ran the whole series carries 4,096 to 4,463 probe observations and the arm that entered in August carries 368, because provider routing sent the retrieval arm a subset of query categories that largely excluded the calibration category. The exclusion removes the most informative case. An engine that searches before answering holds evidence a parametric model does not, namely the absence of any source for a firm that was invented for the purpose, and whether it converts that absence into a refusal is the question the instrument exists to ask. The 192 observations available are consistent with something worth measuring properly, 85.4% flagged and the lowest refusal-marker share in the panel at 15.2% [10.5, 21.5] on 164 flagged rows, and 164 rows on one arm settle nothing. BRGEO-1 requires probes to cover every engine in the panel at the battery's declared size, and every figure in §7.2 describes five parametric arms plus a token presence of the sixth.

---

## Reference keys used

Entries below are copied from `research/R1-literature.md`, section A for works already in v1.0 and section B for proposed additions, with the corrections that file records applied. The two metrology entries carry no R1 record and are copied from `research/R5-metrology.md` §7, where the clause numbers were verified against the primary PDFs on 2026-09-11.

| Key | Entry |
|---|---|
| [Atil2025] | Atıl, B., Aykent, S., Chittams, A., Fu, L., Passonneau, R.J., Radcliffe, E., et al., 2025. Non-Determinism of "Deterministic" LLM System Settings in Hosted Environments, in: Proceedings of the 5th Workshop on Evaluation and Comparison of NLP Systems (Eval4NLP), pp. 135–148. https://doi.org/10.18653/v1/2025.eval4nlp-1.12 |
| [Bito2026] | Bito, E., Ren, Y., He, E., 2026. Position Bias Undermines Preference Consistency in Listwise LLM-Based Reranking, in: Proceedings of the ACM Conference on Recommender Systems (RecSys 2026). arXiv:2608.03091. |
| [Coqueret2026] | Coqueret, G., Llull, J., Oswald, F., Pérignon, C., Scheuch, C., Vilhuber, L., 2026. Randomness in Large Language Models: What Researchers Need to Know (and Report). arXiv:2607.24372. |
| [Guo2024] | Guo, X., Vosoughi, S., 2024. Serial Position Effects of Large Language Models. arXiv:2406.15981. |
| [Hou2024] | Hou, Y., Zhang, J., Lin, Z., Lu, H., Xie, R., McAuley, J., Zhao, W.X., 2024. Large Language Models Are Zero-Shot Rankers for Recommender Systems, in: Advances in Information Retrieval (ECIR 2024), Lecture Notes in Computer Science, pp. 364–381. https://doi.org/10.1007/978-3-031-56060-6_24 |
| [JCGM100] | JCGM 100:2008, Evaluation of measurement data — Guide to the expression of uncertainty in measurement (GUM). BIPM, 2008. |
| [JCGM200] | JCGM 200:2012, International Vocabulary of Metrology — Basic and general concepts and associated terms (VIM), 3rd ed. BIPM, 2012. |
| [Jung2026] | Jung, H., Gonen, H., 2026. PhantomBench: Benchmarking the Non-existential Threat of Language Models. arXiv:2606.11105. |
| [Kirichenko2025] | Kirichenko, P., Ibrahim, M., Chaudhuri, K., Bell, S.J., 2025. AbstentionBench: Reasoning LLMs Fail on Unanswerable Questions. arXiv:2506.09038. |
| [Liu2024] | Liu, N.F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F., Liang, P., 2024. Lost in the Middle: How Language Models Use Long Contexts. Transactions of the Association for Computational Linguistics 12, 157–173. https://doi.org/10.1162/tacl_a_00638 |
| [Menschikov2025] | Menschikov, M., Kharitonov, A., Kotyga, M., Porvatov, V., Zhukovskaya, A., Kagramanyan, D., Shvetsov, E., Burnaev, E., 2025. Beyond Early-Token Bias: Model-Specific and Language-Specific Position Effects in Multilingual LLMs. arXiv:2505.16134. |
| [Pan2026] | Pan, W., Xu, J., Chen, Q., Dong, J., Qin, L., Li, X., Yu, H., Jia, X., 2026. Can LLMs Refuse Questions They Do Not Know? Measuring Knowledge-Aware Refusal in Factual Tasks, in: Proceedings of the International Conference on Learning Representations (ICLR 2026). arXiv:2510.01782. |
| [Wadi2026] | Wadi, D., Ma, Y., 2026. Does Rank Still Matter? Position Bias When AI Agents Shop on Our Behalf. arXiv:2608.22697. |
| [Wen2025] | Wen, B., Yao, J., Feng, S., Xu, C., Tsvetkov, Y., Howe, B., et al., 2025. Know Your Limits: A Survey of Abstention in Large Language Models. Transactions of the Association for Computational Linguistics 13, 529–556. https://doi.org/10.1162/tacl_a_00754 |
| [Zhao2024] | Zhao, W., Goyal, T., Chiu, Y.Y., Jiang, L., Newman, B., Ravichander, A., et al., 2024. WildHallucinations: Evaluating Long-Form Factuality in LLMs with Real-World Entity Queries. arXiv:2407.17468. |

---

## Anti-tic pass

Run on the finished draft against `research/R4-standards.md` PART C, on §6 and §7 only, and measured by `reviews/style_check.py` on the delivered file. The earlier pass over this block did not run C.1.2, C.1.4, C.1.8, C.1.12, C.1.14 or PART D.2, and five of its seven failures were in those rules.

1. **Formulaic antithesis (C.1.1), five occurrences removed.** The opening of §6.1 had read "the window is not an implementation detail, it is the parameter"; the sentence that replaced it reintroduced the same shape, "that string is not the model's answer: it is whatever the pipeline retained", and now carries the form §3.1 already uses for the same fact. §6.2 read "a variable whose maximum equals its minimum is not measuring anything; it is reporting a boundary", and now carries the form §12.3 and §5.4 use. §6.4 carried "this is not error, it is definitional uncertainty"; the passage moved to §6.1 and the negation now attaches to a named consequence, that error implies a correct value better technique approaches. §7.2 carried "only the third is a hallucination, not the first two", trimmed to the assertion alone. One structural antithesis survives in §6.6, "The negative half survives" against "The positive half fails as stated", which is content: the two halves of H6 are separately tested and separately reported. The measurer finds zero closed-form and zero graduated instances.
2. **Filler connective opening a paragraph (C.1.3).** Four removed by deletion, not substitution: "Moreover" in §6.2, "Furthermore" in §6.5, "It is important to note that" in §6.4 and "In this context" in §7.1. The delivered text has zero paragraph openings from the C.1.3 list, zero from the C.2 transition list, and a spent-connective density of 0.00 per 250 words.
3. **First sentence of a section over 45 words (C.1.4).** One instance. §6.4 opened on 47 words of procedure before any result; the conclusion now comes first in 26 words and the procedure follows intact. The measurer finds zero sections opening above the ceiling.
4. **Stylistic em dash (C.1.7).** Zero em dashes and zero en dashes in running prose. Both appear only inside the reference table, in page ranges and standard titles, where PART C tolerates them. Hyphens in prose are compound modifiers only.
5. **Contrastive apposition in series (C.2).** Zero occurrences of the ", not X" form across 3,415 words of prose. The near neighbour "rather than" was counted separately at eight occurrences, 2.3 per 1,000 words.
6. **Percentage without a denominator (C.1.13, PART D), four rewritten.** "84.4%" in §6.4 reads "84.4% of 768 observations" and the probe-coverage figure in §7.3 reads "192 of 17,919 observations, 1.1% of the stratum". The earlier pass declared every percentage checked and had missed the preamble paragraph of §6.6, where two more carried no recoverable base: the Grok share by vertical now names the 192 observations in each vertical cell, and the Gemini contrast now names the 768 observations of the three-day cohort against the 15,355 of the full series. The measurer counts 46 percentages in the delivered prose, the densest of the four blocks.
7. **Empty adjective (C.1.10).** "Robust", "crucial", "comprehensive", "pivotal" and "state-of-the-art" do not appear. "Significant" appears zero times in the non-statistical sense; statistical claims carry the test and the p-value.
8. **Confidence label without a measurement (C.1.11), one instance.** §7.2 read that a pooled protocol "reports a false-positive rate near 97% where the defensible figure is a fraction of it", which sizes a quantity the next paragraph declares unmeasured. It now reports the two proportions that are measured, 96.7% of 17,919 probe observations flagged and 66.8% of the 17,328 flagged responses already carrying an explicit refusal marker, and states what the pooling does. Every other limitation carries its number: the Gemini censoring share with its n, the Grok decoy bound with its 1,118 observations, the taxonomy's missing validation with the four artefacts that are missing, and the probe-coverage gap with the 164 flagged rows it rests on.
9. **Self-narration and verification meta-discourse (C.1.5, C.1.6).** The two identity checks are narrated once, in §6.4, which is the methods passage of this block. The measurer finds zero instances.
10. **Version history in prose (C.1.14), seven occurrences removed.** Every reference to an internal manuscript version was replaced by the dated series it denotes, with all four numbers of the §6.3 comparison kept: the 75.7%, 51.9%, 66,399 and 23.8 points are now stated as measurements on the series that closed on 2026-08-31, which is what they are, instead of as the difference between two published versions. The preamble criterion in §6.6 is now described as a prose criterion that was never committed, without naming the document that described it. The measurer finds zero.
11. **Paragraph length (C.1.9).** Longest prose paragraph is 1,095 characters, the shortest maximum of the four blocks, under the 1,500 warn and well under the 2,200 fail.
12. **Repeated paragraph opening (C.2).** Zero three-word openings repeat anywhere in the block.
13. **Visual support (C.2).** Nine tables, one figure specification and two new display items across 22,319 characters of prose, one item per 1,860 characters, the densest of the four blocks and well inside the one-per-5,000 floor.
14. **Claims of absence (PART D.2), one removed.** §6.3 read that a misreading of the zero deltas was "the reading v1.0 avoided and the market did not", which asserts what published practice does without any survey of it. It now says that the misreading is the one the comparison invites.
15. **Chained reasoning across blocks (C.4.1).** Two passages that this block had written in full belong elsewhere and now point there. The detection history of the window asymmetry is §5.3's, and §6.2 carries a one-line remission. The conversion of whole-response measurement into head-of-response measurement is P1's, and §6.2 cites §3.1 instead of restating it. The two notes to VIM 2.27 are §1.2's, and §6.1 cites the clause and keeps only what it adds, that calling the gap measurement error concedes the wrong thing. The "Declaration." requirement of §6.7 restated the conclusion of §6.5 and now points at it.
16. **Justified recommendation (C.4.3).** §6.7 promised that each of four requirements carries the cost of skipping it, and three did. Sensitivity reporting gave the form and not the cost, and now names the 22.95-to-55.73 spread a single-window publication hides.
17. **Diagnostic, reported and not fixed.** Sentence length runs from 1 to 55 words at a mean of 24.9 and a standard deviation of 13.4, with no sentence above 60. The paired contrast in §7.1, "It says that the extractor is not manufacturing cohort matches" followed by "It says nothing about a model's willingness", is a contrast distributed across two sentences; it sits under the C.2 threshold in isolation and is now the only residue of the habit in the block.
