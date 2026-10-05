# BRGEO-1 — numerical tables, journal version

**Database snapshot.** `data/papers.db`, latest `citations.timestamp` = `2026-09-08T19:30:57.635649+00:00`; earliest = `2026-04-23T22:23:00.960050+00:00`. 86,543 rows in total: 68,624 canonical and 17,919 adversarial probes.

**Regenerate.** From this directory, `python build_tables.py` rewrites this file and `NUMBERS.md`; `python window_analysis.py` prints Table 13 alone. Both open the database read-only.

## Conventions

1. **Canonical stratum.** Unless a table says otherwise, the denominator is `COALESCE(is_probe,0)=0`: the 68,624 observations from the 192-query canonical battery. The 17,919 adversarial probes are a separate instrument and appear only in Table 10.
2. **Observation window.** The study's canonical window is 200 characters. Where a table reports a rate without qualification, entity extraction ran over the first 200 characters of the stored string. Tables 3 and 13 report both windows side by side.
3. **Intervals.** Every rate carries a 95% Wilson score interval in square brackets, in percentage points. Wilson rather than Wald because several cells sit at or near zero, where the Wald interval is degenerate.
4. **Small cells.** A dagger (†) marks any cell with fewer than 30 observations. Those cells are descriptive: they are printed so the table is complete, not so a comparison can be built on them.
5. **Matching rule.** Entity extraction uses the project's own extractor (`src/analysis/entity_extraction.EntityExtractor`) over the v2 cohort (`src/config_v2.get_v2_cohort`, anchors and decoys included), with the project's alias, ambiguity, canonical-name and stop-context dictionaries. The rule is held fixed across every table; only the window moves.

## Table 1. Engine panel

| Engine | Pinned model identifier | Class | Active period | Canonical n |
|---|---|---|---|---:|
| ChatGPT | `gpt-4o-mini-2024-07-18` (2026-04-23 to 2026-09-08) | parametric | 2026-04-23 to 2026-09-08 | 15,168 |
| Claude | `claude-haiku-4-5-20251001` (2026-04-23 to 2026-09-08) | parametric | 2026-04-23 to 2026-09-08 | 15,034 |
| Gemini | `gemini-2.5-pro` (2026-04-23 to 2026-06-09)<br>`gemini-2.5-flash` (2026-08-08 to 2026-09-08) | parametric | 2026-04-23 to 2026-09-08 | 15,355 |
| Groq | `llama-3.3-70b-versatile` (2026-04-23 to 2026-08-16) | parametric, open weights | 2026-04-23 to 2026-08-16 | 14,208 |
| Perplexity | `sonar` (2026-04-23 to 2026-09-08) | retrieval-augmented | 2026-04-23 to 2026-09-08 | 7,741 |
| Grok | `grok-4.6` (2026-08-23 to 2026-09-08) | parametric | 2026-08-23 to 2026-09-08 | 1,118 |
| **Panel** | — | — | 2026-04-23 to 2026-09-08 | **68,624** |

**Table 1.** Engine panel with pinned model identifiers, architectural class and active period. 2026-04-23 to 2026-09-08, n = 68,624 canonical observations; denominator: rows of `citations` with `COALESCE(is_probe,0)=0`.

*Notes.* The panel holds six engines across the series but never six at once. Groq leaves on 2026-08-16 and Grok enters on 2026-08-23, so the two occupy one slot in successive periods and any analysis crossing 2026-08-16 must stratify or truncate. Gemini changes pinned model inside the series (`gemini-2.5-pro` to `gemini-2.5-flash`), which is a stratum boundary of the same kind. Perplexity runs half the battery (96 of the 192 canonical queries), which is why its n is roughly half of the parametric arms; Table 7c shows that the half it runs is not a random half.

## Table 2. Length of the stored extraction string

| Engine | n | Mean chars | Min | Max | Share exactly 200 |
|---|---:|---:|---:|---:|---:|
| Gemini | 15,355 | 195.7 | 87 | 200 | 92.6% |
| ChatGPT | 15,168 | 200.0 | 200 | 200 | 100.0% |
| Claude | 15,034 | 200.0 | 200 | 200 | 100.0% |
| Groq | 14,208 | 200.0 | 200 | 200 | 100.0% |
| Perplexity | 7,741 | 668.0 | 198 | 2,502 | 3.9% |
| Grok | 1,118 | 200.0 | 179 | 200 | 99.9% |

**Table 2.** Length in characters of `citations.response_text`, the string entity extraction actually read. 2026-04-23 to 2026-09-08, n = 68,624 canonical observations; denominator: canonical rows with a non-null `response_text`, by engine.

*Notes.* A variable whose maximum equals its minimum across fifteen thousand observations is not measuring anything; it is reporting a boundary. ChatGPT, Claude, Groq are at exactly 200 on every single observation, because their client adapter stored `text[:200]`. Gemini and Grok fall marginally short of that ceiling, which is what an arm that occasionally answers in fewer characters than the ceiling looks like once the ceiling is imposed. Perplexity took a different path through the client and stored up to 2,502 characters, which is the asymmetry the paper is about. The 305 Perplexity rows now sitting at exactly 200 are the observations collected after the uniform window was applied at collection time on 2026-08-31.

## Table 3. Citation rate as collected and under a uniform window

| Engine | n | As collected [95% CI] | Uniform 200-char window [95% CI] | Δ | Rows truncated |
|---|---:|---:|---:|---:|---:|
| Gemini | 15,355 | 1.9 [1.7, 2.1] | 1.9 [1.7, 2.1] | +0.0 pp | 0 |
| ChatGPT | 15,168 | 17.2 [16.6, 17.8] | 17.2 [16.6, 17.8] | +0.0 pp | 0 |
| Claude | 15,034 | 25.7 [25.1, 26.5] | 25.7 [25.1, 26.5] | +0.0 pp | 0 |
| Groq | 14,208 | 8.5 [8.1, 9.0] | 8.5 [8.1, 9.0] | +0.0 pp | 0 |
| Perplexity | 7,741 | 74.9 [73.9, 75.8] | 52.0 [50.9, 53.1] | -22.8 pp | 7,435 |
| Grok | 1,118 | 29.6 [27.0, 32.3] | 29.6 [27.0, 32.3] | +0.0 pp | 0 |
| **Panel** | **68,624** | 20.5 [20.2, 20.8] | 18.0 [17.7, 18.3] | -2.6 pp | **7,435** |

**Table 3.** Citation rate by engine, as collected and after re-extraction under a uniform 200-character window, with the difference in percentage points and the number of rows whose stored text exceeded the window. 2026-04-23 to 2026-09-08, n = 68,624 canonical observations; denominator: canonical rows with a non-null `response_text`, by engine.

*Notes.* Five deltas of exactly zero are a sanity check and not an independent verification: applying a 200-character window to a string that is already 200 characters is the identity operation, so the zero is guaranteed by construction. What it confirms is that re-extraction is deterministic and that the cohort did not change between runs. The one non-zero delta belongs to the retrieval-augmented arm: Perplexity moves from 74.9% to 52.0%, -22.8 pp over 7,435 truncated rows.

The 'as collected' column for Perplexity now mixes two collection regimes, and the mixture is disclosed rather than smoothed:

| Perplexity, by stored length | n | Cited | Rate [95% CI] | Full response also retained | Period |
|---|---:|---:|---:|---:|---|
| stored text longer than the window | 7,435 | 5,630 | 75.7 [74.7, 76.7] | 0 | 2026-04-23 to 2026-08-31 |
| stored text at or below the window | 306 | 166 | 54.2 [48.6, 59.7] | 305 | 2026-04-28 to 2026-09-08 |

The group at or below the window is the set of observations collected after the uniform window was applied at collection time on 2026-08-31, plus a single early response that happened to be shorter than the window, which is why its period starts in April. For those rows 'as collected' and 'uniform window' are the same measurement. This is why the panel figure for Perplexity as collected (74.9%) is slightly below the 75.7% reported in manuscript v1.0, which closed before those rows existed.

## Table 4. First-mention offset

| Engine | n cited | Absolute offset, mean | Observed length, mean | Relative, mean | Relative, median |
|---|---:|---:|---:|---:|---:|
| Grok | 331 | 40 | 200 | 0.198 | 0.000 |
| Perplexity | 5,796 | 155 | 649 | 0.233 | 0.171 |
| Gemini | 285 | 96 | 196 | 0.493 | 0.375 |
| Groq | 1,210 | 108 | 200 | 0.539 | 0.530 |
| ChatGPT | 2,604 | 116 | 200 | 0.582 | 0.600 |
| Claude | 3,871 | 124 | 200 | 0.621 | 0.645 |

**Table 4.** Offset of the first cohort entity named, absolute and relative to the length of the text actually observed. 2026-04-23 to 2026-09-08, n = 14,097 canonical observations carrying a citation; denominator: canonical rows with `cited_v2 = 1`, a non-null `first_entity_offset_v2` and `response_length_chars_v2 > 0`, by engine.

*Notes.* This table is computed on the text as stored, not under the uniform window, because its subject is the position of the first mention inside whatever text the extractor saw. That makes the denominators censored at 200 characters for every arm except Perplexity, so the relative values of the parametric arms are upper bounds on their true relative position. The apparent reversal, in which the retrieval-augmented arm names entities earlier in relative terms than every parametric arm except Grok, therefore cannot be asserted as established. The defensible reading is non-identification: data collected under an asymmetric window does not identify the direction of the window bias. Table 13 is the analysis that removes the censoring.

## Table 5. Opening style against citation rate

| Engine | n | Opens with preamble [95% CI] | Citation rate, as collected [95% CI] |
|---|---:|---:|---:|
| Gemini | 15,355 | 80.0 [79.4, 80.7] | 1.9 [1.7, 2.1] |
| Grok | 1,118 | 9.5 [7.9, 11.3] | 29.6 [27.0, 32.3] |
| Perplexity | 7,741 | 4.0 [3.6, 4.4] | 74.9 [73.9, 75.8] |
| ChatGPT | 15,168 | 0.0 [0.0, 0.0] | 17.2 [16.6, 17.8] |
| Claude | 15,034 | 0.0 [0.0, 0.0] | 25.7 [25.1, 26.5] |
| Groq | 14,208 | 0.0 [0.0, 0.0] | 8.5 [8.1, 9.0] |

**Table 5.** Share of responses opening with preamble, against the citation rate as collected. 2026-04-23 to 2026-09-08, n = 68,624 canonical observations; denominator: canonical rows with a non-null `response_text`, by engine.

*Criterion applied.* Preamble is a case-insensitive regular expression anchored at the start of the stored string, after skipping leading non-word characters (`^\W*`), matching any of three families: a greeting or praise of the question; a hedge on whether the question can be answered; an explicit model self-reference. The pattern is printed in full in NUMBERS.md T5, because the criterion is part of the result and not an implementation detail.

*Provenance of the criterion.* The regular expression behind Table 7 of manuscript v1.0 is described in prose in three documents but was never committed to the repository, so it cannot be re-run. The pattern used here is a re-specification in the same spirit, and NUMBERS.md T5 reports it against the v1.0 figures over the identical row set so a reviewer can see where the two agree and where they do not. The two largest divergences are Perplexity and Grok; the ordering claim the paper rests on survives both criteria.

*Reading.* The arm that spends the window on preamble is parametric: Gemini opens 80.0% of its responses that way and cites within the window 1.9% of the time. The retrieval-augmented arm has little preamble (4.0%) and the highest citation rate. Susceptibility to a narrow window therefore tracks response style, which is a property of the model, and is not deducible from the architectural class.

## Table 6. Citation rate by vertical and engine

| Engine | Fintech | Retail | Health | Technology | All |
|---|---:|---:|---:|---:|---:|
| ChatGPT | 18.1 [16.9, 19.4]<br><sub>n = 3,792</sub> | 22.4 [21.1, 23.7]<br><sub>n = 3,792</sub> | 7.7 [6.9, 8.6]<br><sub>n = 3,792</sub> | 20.4 [19.2, 21.8]<br><sub>n = 3,792</sub> | 17.2 [16.6, 17.8]<br><sub>n = 15,168</sub> |
| Claude | 50.8 [49.2, 52.4]<br><sub>n = 3,792</sub> | 30.4 [28.9, 31.9]<br><sub>n = 3,792</sub> | 11.0 [10.1, 12.1]<br><sub>n = 3,754</sub> | 10.3 [9.3, 11.3]<br><sub>n = 3,696</sub> | 25.7 [25.1, 26.5]<br><sub>n = 15,034</sub> |
| Gemini | 4.4 [3.8, 5.1]<br><sub>n = 3,840</sub> | 2.5 [2.1, 3.0]<br><sub>n = 3,840</sub> | 0.0 [0.0, 0.1]<br><sub>n = 3,840</sub> | 0.5 [0.3, 0.8]<br><sub>n = 3,835</sub> | 1.9 [1.7, 2.1]<br><sub>n = 15,355</sub> |
| Groq | 9.4 [8.5, 10.4]<br><sub>n = 3,552</sub> | 12.8 [11.7, 13.9]<br><sub>n = 3,552</sub> | 6.0 [5.3, 6.8]<br><sub>n = 3,552</sub> | 5.9 [5.2, 6.7]<br><sub>n = 3,552</sub> | 8.5 [8.1, 9.0]<br><sub>n = 14,208</sub> |
| Perplexity | 67.8 [65.7, 69.9]<br><sub>n = 1,961</sub> | 68.4 [66.2, 70.4]<br><sub>n = 1,940</sub> | 44.5 [42.3, 46.8]<br><sub>n = 1,920</sub> | 26.9 [25.0, 29.0]<br><sub>n = 1,920</sub> | 52.0 [50.9, 53.1]<br><sub>n = 7,741</sub> |
| Grok | 59.0 [53.3, 64.6]<br><sub>n = 288</sub> | 40.6 [35.1, 46.4]<br><sub>n = 288</sub> | 10.4 [7.4, 14.5]<br><sub>n = 288</sub> | 5.5 [3.3, 9.0]<br><sub>n = 254</sub> | 29.6 [27.0, 32.3]<br><sub>n = 1,118</sub> |
| **Panel** | 26.8 [26.1, 27.5]<br><sub>n = 17,225</sub> | 23.2 [22.6, 23.9]<br><sub>n = 17,204</sub> | 10.5 [10.1, 11.0]<br><sub>n = 17,146</sub> | 11.2 [10.8, 11.7]<br><sub>n = 17,049</sub> | 18.0 [17.7, 18.3]<br><sub>n = 68,624</sub> |

**Table 6.** Citation rate under the uniform 200-character window, by engine and vertical, as percentage points with a 95% Wilson interval. 2026-04-23 to 2026-09-08, n = 68,624 canonical observations; denominator: canonical rows with a non-null `response_text`, by cell.

*Notes.* Every cell is large, so the intervals are narrow and the between-cell differences are not interval artefacts. Gemini in health is a hard zero over 3,840 observations, with a Wilson upper bound of 0.100%; read together with Table 5 that is a statement about the first 200 characters of a Gemini answer, not about whether Gemini knows Brazilian health providers.

The vertical ordering is not uniform across arms and should not be summarised as one. Counting which vertical leads each of the six arms: Retail in 3 of 6; Fintech in 3 of 6. Counting which trails: Technology in 4 of 6; Health in 2 of 6. At panel level Fintech is highest at 26.8% and Health lowest at 10.5%, but that ordering is a mixture over arms with very different overall rates and is not a property of the verticals.

## Table 7. Citation rate by query stratum

### Table 7a. By language

| Engine | pt | en |
|---|---:|---:|
| ChatGPT | 11.1 [10.4, 11.8]<br><sub>n = 7,584</sub> | 23.2 [22.3, 24.2]<br><sub>n = 7,584</sub> |
| Claude | 24.8 [23.8, 25.8]<br><sub>n = 7,518</sub> | 26.7 [25.7, 27.7]<br><sub>n = 7,516</sub> |
| Gemini | 0.9 [0.7, 1.1]<br><sub>n = 7,677</sub> | 2.9 [2.5, 3.2]<br><sub>n = 7,678</sub> |
| Groq | 5.3 [4.8, 5.8]<br><sub>n = 7,104</sub> | 11.8 [11.0, 12.5]<br><sub>n = 7,104</sub> |
| Perplexity | 54.2 [52.6, 55.7]<br><sub>n = 3,871</sub> | 49.9 [48.3, 51.5]<br><sub>n = 3,870</sub> |
| Grok | 26.4 [22.9, 30.2]<br><sub>n = 560</sub> | 32.8 [29.0, 36.8]<br><sub>n = 558</sub> |
| **Panel** | 15.7 [15.3, 16.1]<br><sub>n = 34,314</sub> | 20.2 [19.8, 20.6]<br><sub>n = 34,310</sub> |

### Table 7b. By query type

| Engine | directive | exploratory |
|---|---:|---:|
| ChatGPT | 32.0 [30.9, 33.0]<br><sub>n = 7,584</sub> | 2.4 [2.1, 2.7]<br><sub>n = 7,584</sub> |
| Claude | 31.1 [30.0, 32.1]<br><sub>n = 7,519</sub> | 20.4 [19.5, 21.3]<br><sub>n = 7,515</sub> |
| Gemini | 2.7 [2.4, 3.1]<br><sub>n = 7,679</sub> | 1.0 [0.8, 1.2]<br><sub>n = 7,676</sub> |
| Groq | 11.3 [10.6, 12.1]<br><sub>n = 7,104</sub> | 5.7 [5.2, 6.3]<br><sub>n = 7,104</sub> |
| Perplexity | 74.0 [72.6, 75.4]<br><sub>n = 3,873</sub> | 30.0 [28.6, 31.5]<br><sub>n = 3,868</sub> |
| Grok | 45.7 [41.6, 49.9]<br><sub>n = 560</sub> | 13.4 [10.9, 16.5]<br><sub>n = 558</sub> |
| **Panel** | 25.9 [25.5, 26.4]<br><sub>n = 34,319</sub> | 10.0 [9.7, 10.3]<br><sub>n = 34,305</sub> |

### Table 7c. By semantic category

| Engine | descoberta | comparativo | mercado | confianca | experiencia | inovacao |
|---|---:|---:|---:|---:|---:|---:|
| ChatGPT | 1.5 [1.1, 2.0]<br><sub>n = 2,528</sub> | 28.5 [26.8, 30.3]<br><sub>n = 2,528</sub> | 29.8 [28.1, 31.6]<br><sub>n = 2,528</sub> | 23.5 [21.9, 25.2]<br><sub>n = 2,528</sub> | 0.0 [0.0, 0.2]<br><sub>n = 2,528</sub> | 19.7 [18.2, 21.3]<br><sub>n = 2,528</sub> |
| Claude | 51.9 [49.9, 53.8]<br><sub>n = 2,512</sub> | 28.1 [26.4, 29.9]<br><sub>n = 2,512</sub> | 34.5 [32.7, 36.4]<br><sub>n = 2,496</sub> | 19.7 [18.2, 21.3]<br><sub>n = 2,512</sub> | 6.3 [5.4, 7.3]<br><sub>n = 2,506</sub> | 13.9 [12.6, 15.3]<br><sub>n = 2,496</sub> |
| Gemini | 0.3 [0.2, 0.6]<br><sub>n = 2,560</sub> | 4.3 [3.6, 5.2]<br><sub>n = 2,560</sub> | 3.2 [2.6, 4.0]<br><sub>n = 2,560</sub> | 0.2 [0.1, 0.4]<br><sub>n = 2,560</sub> | 3.1 [2.5, 3.9]<br><sub>n = 2,560</sub> | 0.0 [0.0, 0.2]<br><sub>n = 2,555</sub> |
| Groq | 9.6 [8.5, 10.9]<br><sub>n = 2,368</sub> | 17.7 [16.3, 19.3]<br><sub>n = 2,368</sub> | 14.9 [13.6, 16.4]<br><sub>n = 2,368</sub> | 6.4 [5.5, 7.4]<br><sub>n = 2,368</sub> | 1.0 [0.6, 1.5]<br><sub>n = 2,368</sub> | 1.4 [1.0, 2.0]<br><sub>n = 2,368</sub> |
| Perplexity | 59.7 [57.8, 61.6]<br><sub>n = 2,584</sub> | 54.6 [52.7, 56.5]<br><sub>n = 2,584</sub> | 41.7 [39.8, 43.7]<br><sub>n = 2,573</sub> | — | — | — |
| Grok | 44.8 [37.9, 51.9]<br><sub>n = 192</sub> | 38.4 [31.8, 45.5]<br><sub>n = 190</sub> | 31.0 [24.7, 38.0]<br><sub>n = 184</sub> | 13.0 [8.9, 18.7]<br><sub>n = 184</sub> | 28.3 [22.3, 35.2]<br><sub>n = 184</sub> | 21.2 [15.9, 27.7]<br><sub>n = 184</sub> |
| **Panel** | 25.1 [24.4, 25.9]<br><sub>n = 12,744</sub> | 27.0 [26.2, 27.8]<br><sub>n = 12,742</sub> | 25.0 [24.3, 25.8]<br><sub>n = 12,709</sub> | 12.5 [11.9, 13.2]<br><sub>n = 10,152</sub> | 3.1 [2.8, 3.4]<br><sub>n = 10,146</sub> | 9.1 [8.5, 9.6]<br><sub>n = 10,131</sub> |

**Table 7.** Citation rate under the uniform 200-character window by query language (a), query type (b) and semantic category (c), by engine. 2026-04-23 to 2026-09-08, n = 68,624 canonical observations; denominator: canonical rows with a non-null `response_text`, by cell.

*Notes.* The language and type splits are balanced by construction, so the panel comparison in 7a and 7b is between equal denominators. The category split is not: Perplexity runs only three of the six categories (`descoberta`, `comparativo`, `mercado`) because it runs half the battery, and those three are exactly the discovery-shaped categories where citation rates are highest. The panel row of Table 7c is therefore composed of different engine mixtures from column to column and should not be read as a category effect. Compare within an engine row, or restrict to the five arms that run all six.

The directive/exploratory contrast in 7b is the largest stratum effect in these tables and it holds in every arm: a question that asks for a named best is answered with a name far more often than a question that asks for the landscape. It is also the contrast most obviously confounded with the window, since an exploratory answer has more reason to open with framing prose.

## Table 8. Concentration of first mentions

| Rank | Entity | First mentions | Share of first mentions | Cumulative share |
|---:|---|---:|---:|---:|
| 1 | Nubank | 4,595 | 37.3% | 37.3% |
| 2 | Mercado Livre | 2,090 | 17.0% | 54.2% |
| 3 | Magazine Luiza | 1,406 | 11.4% | 65.6% |
| 4 | Totvs | 813 | 6.6% | 72.2% |
| 5 | EMS Pharma | 587 | 4.8% | 77.0% |
| 6 | Hypera Pharma | 540 | 4.4% | 81.4% |
| 7 | Involves | 345 | 2.8% | 84.2% |
| 8 | Accenture | 212 | 1.7% | 85.9% |
| 9 | Americanas | 209 | 1.7% | 87.6% |
| 10 | Walmart | 208 | 1.7% | 89.3% |

**Table 8.** The ten entities most often named first, with count and share of all first mentions. 2026-04-23 to 2026-09-08, n = 12,329 canonical observations carrying a citation under the uniform 200-character window; denominator: those 12,329 first mentions.

| Quantity | Value |
|---|---:|
| Cohort, distinct entities | 127 |
| of which Brazilian real firms | 79 |
| of which international anchors | 32 |
| of which fictitious decoys | 16 |
| Distinct entities ever named first | **42** |
| of which Brazilian real firms | 31 of 79 |
| of which international anchors | 11 of 32 |
| of which fictitious decoys | 0 of 16 |
| Cumulative share, top 1 | 37.3% |
| Cumulative share, top 3 | 65.6% |
| Cumulative share, top 5 | 77.0% |
| Cumulative share, top 10 | 89.3% |
| Herfindahl-Hirschman index (reported index) | **0.1917** |
| Gini coefficient over named entities | 0.8176 |

*Notes.* The concentration index reported here is the Herfindahl-Hirschman index, computed as the sum of squared shares of first mentions across the 42 entities that were ever named first, on the 0 to 1 scale. At 0.1917 it is equivalent to a market with about 5.2 equally sized participants, against a cohort of 127. The Gini coefficient is given as a secondary statistic and is computed only over entities that were named at least once, so it understates inequality relative to a version that counted the 85 never-named members as zeros.

The denominator matters for the headline reading. 42 of 127 cohort members were ever the first name in an answer, and one firm takes 37.3% of all first mentions. Under the as-collected window the distinct count is 53 rather than 42, the difference being entities that Perplexity named beyond character 200. That gap is itself a window effect: how concentrated the market looks depends on how much of each answer you read.

### Instrument note: two cohort names collide with ordinary words

Inspecting the ranked list above turned up a defect in the matcher that had not been recorded anywhere. Two cohort names are also ordinary words of the response language, and neither is listed in `src/config.AMBIGUOUS_ENTITIES` nor given a stop context, so the extractor matches the ordinary word:

| Colliding name | Matches under the uniform window | What it is matching |
|---|---:|---|
| `Involves` | 345 | the English verb, as in "Evaluating trust in Brazilian technology and IT **involves** several factors" |
| `Target` | 8 | the English noun and verb, as in "B2B platforms like Mercado Shops **target** SMEs" |

Magnitude. 353 of 68,624 canonical observations contain at least one such match, 0.51% of the panel. In every one of them the collision is the only match, so the whole set is counted as cited for no other reason. Removing both names from the cohort moves the panel citation rate from 17.97% to 17.45%, the distinct first-mention count from 42 to 40, the HHI from 0.1917 to 0.2023, and the top-1 share from 37.3% to 38.4%.

The collisions sit where the ordinary word lives. By language: en 353. By engine: Groq 173, ChatGPT 158, Gemini 22.

The tables are published with the collisions left in, because the figures above are what the instrument as specified produces, and correcting the cohort here would break the correspondence with the stored series that V1 of NUMBERS.md establishes. The correction belongs in `src/config.py`, where `Involves` needs a canonical name and `Target` a stop context, followed by re-extraction. Until then this paragraph is the declared error term on every rate in these tables. It is two orders of magnitude smaller than the window effect of Table 13, which is why it changes no conclusion drawn here, and it is worth stating anyway: a protocol paper that asks others to declare their matching rule has to declare where its own leaks.

## Table 9. Calibration decoys in the canonical stratum

| Engine | Canonical n | Spontaneous decoy, 200-char window [95% CI] | Spontaneous decoy, text as stored [95% CI] |
|---|---:|---:|---:|
| ChatGPT | 15,168 | 0.000 [0.000, 0.025] | 0.000 [0.000, 0.025] |
| Claude | 15,034 | 0.000 [0.000, 0.026] | 0.000 [0.000, 0.026] |
| Gemini | 15,355 | 0.000 [0.000, 0.025] | 0.000 [0.000, 0.025] |
| Groq | 14,208 | 0.000 [0.000, 0.027] | 0.000 [0.000, 0.027] |
| Perplexity | 7,741 | 0.000 [0.000, 0.050] | 0.000 [0.000, 0.050] |
| Grok | 1,118 | 0.000 [0.000, 0.342] | 0.000 [0.000, 0.342] |
| **Panel** | **68,624** | 0.000 [0.000, 0.006] | 0.000 [0.000, 0.006] |

**Table 9.** Spontaneous naming of a fictitious entity in answers to canonical queries, which no decoy name appears in. 2026-04-23 to 2026-09-08, n = 68,624 canonical observations; denominator: canonical rows with a non-null `response_text`, by engine. Sixteen decoys, verified as non-existent before collection.

*Result.* Zero. Across 68,624 canonical observations and six engines, no decoy was named spontaneously, either inside the 200-character window or anywhere in the text as stored. The point estimate of the spontaneous false-positive rate is 0, with a 95% Wilson upper bound of 0.00560% (3.8 expected occurrences per 68,624 observations).

*What this licenses and what it does not.* It bounds one failure mode of the instrument: the extractor is not inventing cohort matches out of ordinary prose, which is the failure a word-boundary matcher on names like `Inter` or `Stone` would be expected to show. It says nothing about the models' willingness to describe an entity that does not exist when asked about it directly, which is a different quantity and is Table 10. It also cannot bound false positives on real names used in an unintended sense, since a decoy carries no such sense. The stored `fictional_hit` column is 0 on every canonical row, which is consistent with this result but is not independent evidence for it: that column was only ever populated on the probe stratum.

## Table 10. Adversarial stratum

| Engine | Probe n | Flagged by the legacy criterion [95% CI] | Of those, carrying an explicit refusal marker [95% CI] |
|---|---:|---:|---:|
| Gemini | 4,463 | 90.3 [89.4, 91.2] | 46.9 [45.3, 48.4] |
| ChatGPT | 4,416 | 97.3 [96.8, 97.8] | 67.4 [66.0, 68.8] |
| Claude | 4,384 | 100.0 [99.9, 100.0] | 92.4 [91.6, 93.2] |
| Groq | 4,096 | 99.7 [99.5, 99.8] | 61.7 [60.2, 63.2] |
| Grok | 368 | 99.5 [98.0, 99.9] | 50.3 [45.2, 55.4] |
| Perplexity | 192 | 85.4 [79.7, 89.7] | 15.2 [10.5, 21.5] |
| **Panel** | **17,919** | 96.7 [96.4, 97.0] | 66.8 [66.1, 67.5] |

**Table 10.** Adversarial probes, the share flagged by the legacy hallucination criterion, and the share of those flagged answers that carry an explicit refusal marker. 2026-04-23 to 2026-09-08, n = 17,919 probe observations; denominators: all probe rows for the first rate, and the 17,328 flagged rows with non-empty text for the second.

*Notes.* The refusal regex is reproduced verbatim from `docs/research/methods-paper/VERIFICATION.md` section 5.3 and is deliberately conservative: it counts only answers carrying an explicit marker, so 66.8% is a floor on the refusal share, not a ceiling. What the table shows is that the legacy criterion, which flagged an answer whenever the decoy name appeared in it, was counting refusals as hallucinations: two thirds of the flagged answers say in so many words that the entity could not be found. A criterion that cannot separate 'here is what that company does' from 'I cannot find any company by that name' is not measuring hallucination.

The engine-level spread is the operational finding. Claude carries a refusal marker in 92.4% of its flagged answers and Perplexity in 15.2%, so any headline hallucination rate computed under the legacy criterion ranks the engines mostly by how explicitly they decline.

## Table 11. Temporal coverage

| Month | Days with data | Canonical n | Days on the calendar | Days with no data |
|---|---:|---:|---:|---:|
| 2026-04 | 8 | 10,930 | 8 | 0 |
| 2026-05 | 23 | 25,899 | 31 | 8 |
| 2026-06 | 9 | 13,624 | 30 | 21 |
| 2026-07 | 0 | 0 | 31 | 31 |
| 2026-08 | 10 | 15,946 | 31 | 21 |
| 2026-09 | 3 | 2,225 | 8 | 5 |
| **Series** | **53** | **68,624** | **139** | **86** |

**Table 11.** Days with data against days on the calendar, by month. 2026-04-23 to 2026-09-08, n = 68,624 canonical observations; denominator: calendar days in the span 2026-04-23 to 2026-09-08.

| Coverage quantity | Value |
|---|---:|
| Calendar days spanned | 139 |
| Days with at least one observation | **53** |
| Days with no observation | 86 |
| Partial days, derived definition below | **19** |
| Partial days registered in `data/partial_days.json`, inside the span | 2 |
| `collection_runs` rows with status `success` | 328 |
| `collection_runs` rows with status `aborted` | 344 |

Contiguous blocks with no data:

| From | To | Days |
|---|---|---:|
| 2026-05-02 | 2026-05-03 | 2 |
| 2026-05-06 | 2026-05-10 | 5 |
| 2026-05-29 | 2026-05-29 | 1 |
| 2026-06-10 | 2026-08-07 | 59 |
| 2026-08-09 | 2026-08-09 | 1 |
| 2026-08-17 | 2026-08-22 | 6 |
| 2026-08-24 | 2026-08-30 | 7 |
| 2026-09-01 | 2026-09-05 | 5 |

*Two sources for partial days, and why both are given.* The repository carries a registry at `data/partial_days.json`. It records, per day, the engines that produced nothing and why, with a link to the run or the governance note. It is authoritative on what it covers and it does not cover the whole series: its earliest entry is 2026-09-06, it was seeded by hand, and it records only engine absence, not an engine that ran a short battery.

Registry entries falling inside the snapshot span:

| Day | Engines missing | Reason, as recorded |
|---|---|---|
| 2026-09-06 | ChatGPT, Claude | Coleta local com MANDATORY_LLMS rebaixada para Gemini,Perplexity,Grok; ChatGPT 429 'no credits remaining' e Claude 400 'credit balance is too low'. |
| 2026-09-07 | ChatGPT, Claude | Coleta local com MANDATORY_LLMS rebaixada para Gemini,Perplexity,Grok; ChatGPT 429 'no credits remaining' e Claude 400 'credit balance is too low'. |

The registry also carries 3 entries for 2026-09-10, 2026-09-11, after the last observation in this snapshot. They are listed here so a reader who takes a fresher snapshot knows the outage continued, and they contribute nothing to the tables above.

The second source is derived from the observations themselves, because the registry says nothing about the first four months of the series. A day is partial when at least one engine active in the surrounding period either delivered fewer distinct canonical queries than its own battery size or produced no row at all. Battery size is inferred from the data as the largest number of distinct canonical queries the engine ever reached in a single day, which is 192 for every parametric arm and 96 for Perplexity.

The two sources can be checked against each other on the days both cover. They agree exactly: on 2026-09-06 the registry names ChatGPT and Claude and the derived rule finds ChatGPT and Claude; on 2026-09-07 the registry names ChatGPT and Claude and the derived rule finds ChatGPT and Claude. The derived rule therefore recovers the registered outages without being told about them, which is the reason it is trusted for the months the registry does not reach.

Under the derived definition 19 of the 53 days with data are partial:

| Day | Engines short of battery | Engines absent |
|---|---|---|
| 2026-04-23 | ChatGPT, Claude, Gemini, Groq, Perplexity | — |
| 2026-04-24 | Claude | — |
| 2026-04-29 | ChatGPT, Claude, Gemini, Groq, Perplexity | — |
| 2026-05-01 | ChatGPT, Claude, Gemini, Groq, Perplexity | — |
| 2026-05-04 | ChatGPT, Claude, Gemini, Groq, Perplexity | — |
| 2026-05-11 | ChatGPT, Claude, Gemini, Groq, Perplexity | — |
| 2026-05-12 | ChatGPT, Claude, Gemini, Groq, Perplexity | — |
| 2026-05-14 | ChatGPT, Claude, Gemini, Groq, Perplexity | — |
| 2026-05-17 | Claude | — |
| 2026-05-18 | ChatGPT, Claude, Gemini, Groq, Perplexity | — |
| 2026-05-19 | ChatGPT, Claude, Gemini, Groq, Perplexity | — |
| 2026-05-20 | ChatGPT, Claude, Gemini, Groq, Perplexity | — |
| 2026-05-26 | ChatGPT, Claude, Gemini, Groq, Perplexity | — |
| 2026-05-27 | ChatGPT, Claude, Gemini, Groq, Perplexity | — |
| 2026-06-05 | — | Gemini |
| 2026-08-13 | Perplexity | — |
| 2026-08-23 | Grok | — |
| 2026-09-06 | — | ChatGPT, Claude |
| 2026-09-07 | Gemini, Perplexity, Grok | ChatGPT, Claude |

*Notes on the aborted runs.* The 344 rows with status `aborted` are not failed attempts observed as they happened. They cover 86 distinct days and were written retroactively by `scripts/mark_collection_gaps.py` so that a silent hole in the series would appear in `collection_runs` as a declared fact rather than as an absence. The largest single block, 59 days from 2026-06-10 to 2026-08-07, is the period in which the workflow ran green and persisted nothing. Any longitudinal reading of Table 12 has to carry that block, because a straight line fitted across it is interpolating over two months of no observation.

## Table 12. Descriptive temporal stability

| Engine | Days with n ≥ 30 | First day rate | Last day rate | Min | Max | Slope, pp per day [95% interval] |
|---|---:|---:|---:|---:|---:|---:|
| ChatGPT | 51 | 16.3% (2026-04-23) | 17.2% (2026-09-08) | 15.6% | 19.4% | +0.0011 [-0.0053, +0.0074] |
| Claude | 51 | 35.0% (2026-04-23) | 25.0% (2026-09-08) | 9.6% | 35.0% | -0.0061 [-0.0298, +0.0177] |
| Gemini | 52 | 1.4% (2026-04-23) | 2.4% (2026-09-08) | 0.3% | 7.3% | +0.0183 [+0.0131, +0.0235] |
| Groq | 48 | 8.6% (2026-04-23) | 9.8% (2026-08-16) | 5.7% | 10.4% | +0.0171 [+0.0109, +0.0233] |
| Perplexity | 51 | 66.7% (2026-04-23) | 49.0% (2026-09-08) | 38.9% | 70.1% | -0.0433 [-0.0906, +0.0040] |
| Grok† | 5 | 39.2% (2026-08-23) | 21.5% (2026-09-08) | 21.5% | 51.0% | -0.2759 [-2.2582, +1.7064] |

**Table 12.** Daily citation rate under the uniform 200-character window, summarised by engine, with an ordinary least squares slope in percentage points per calendar day. 2026-04-23 to 2026-09-08, n = 68,583 canonical observations on days meeting the threshold; denominator: for each engine, its days with at least 30 canonical observations. A dagger marks an engine with fewer than ten daily points.

*This is a description, not a test.* The slope is fitted on daily rates treated as equally weighted points on a calendar axis. Those points are not independent: they share a fixed query battery, they are clustered by collection run, their denominators vary by a factor of four, and the axis contains an 86-day hole of which 59 days are contiguous. The interval in the last column is a residual-based interval around the fitted slope and is printed so the reader can see how badly the slope is determined. No hypothesis about drift is tested here, and none should be read off the sign.

What the column is useful for is the opposite of a trend claim: it shows that no arm's daily rate wanders far enough to make the series-level figures in Table 3 an artefact of which days happened to be collected. The widest day-to-day spread belongs to Perplexity, whose daily rate ranges from 38.9% to 70.1%, a span of 31.2 pp across 51 days. The steepest fitted slope belongs to Grok at -0.2759 pp per day, which over the 139 calendar days of the series would amount to 38.3 pp, and its interval [-2.2582, +1.7064] shows how little the daily points constrain it.

## Table 13. The observation window measured on every arm

| Engine | n | Rate at 200 chars [95% CI] | Rate on full text [95% CI] | Δ | Gains | Losses | Exact McNemar p | Mean full length |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ChatGPT | 192 | 17.2 [12.5, 23.2] | 53.6 [46.6, 60.6] | +36.5 pp | 70 | 0 | <0.001 | 1,895 |
| Claude | 192 | 25.0 [19.4, 31.6] | 66.1 [59.2, 72.5] | +41.1 pp | 79 | 0 | <0.001 | 1,194 |
| Gemini | 768 | 2.6 [1.7, 4.0] | 33.3 [30.1, 36.7] | +30.7 pp | 236 | 0 | <0.001 | 1,895 |
| Perplexity | 305 | 54.1 [48.5, 59.6] | 77.0 [72.0, 81.4] | +23.0 pp | 70 | 0 | <0.001 | 556 |
| Grok | 768 | 28.4 [25.3, 31.7] | 84.1 [81.4, 86.5] | +55.7 pp | 428 | 0 | <0.001 | 2,015 |

**Table 13.** Citation rate at 200 characters against citation rate on the full response, for the same observations, under the same matching rule. 2026-09-06 to 2026-09-08, n = 2,225 canonical observations; denominator: canonical rows whose `response_full_text` is non-empty, by engine. Gains are rows uncited at 200 characters and cited on the full text; losses are the reverse; the p-value is the exact two-sided McNemar test on those discordant pairs.

*Method.* `scripts/harmonize_citation_window.py` could only ever move one arm, because five of six adapters stored `text[:200]` and the text beyond the window was never written to disk. Since migration 0010 the pipeline writes the whole response to `citations.response_full_text` while continuing to write the windowed string to `response_text`. For those rows the comparison runs within the arm: extract over `response_full_text[:200]`, extract over `response_full_text`, hold the cohort and the matching rule fixed, and read off the difference. Two checks are run on every row and both pass on all 2,225: `response_text` equals `response_full_text[:200]`, so the two columns are two views of one response; and re-extracting the first 200 characters reproduces the stored `cited_v2` exactly, so the rule used here is the rule that produced the series. Without the second check, a delta reported below could be an artefact of this script's matching rather than of the window.

*Result.* The window effect is present in every arm that retained full text. Grok +55.7 pp, Claude +41.1 pp, ChatGPT +36.5 pp, Gemini +30.7 pp, Perplexity +23.0 pp. Not one row in any arm loses its citation when more text is read, which is what a monotone window ought to produce and is therefore a further check rather than a finding.

Two readings of that row of numbers are available and only one of them is supported. The supported one is that the effect is not confined to the retrieval-augmented arm: four parametric arms move at least 30.7 percentage points, which is the point the protocol rests on. The unsupported one is a ranking of engines by susceptibility; see the limits below. What can be said about Perplexity is narrower and still useful: its delta here, +23.0 pp on 305 rows, sits close to the 23.8 pp that manuscript v1.0 measured on 7,435 truncated rows of the same arm, so the one figure the earlier paper could produce appears to be stable across two disjoint row sets.

*The Gemini rows need stratifying.* On 2026-09-06 Gemini returned unusually short responses: 384 rows with a maximum full length of 216 characters, of which only six contain a cohort entity at all, so for those rows the two windows are nearly the same text and the delta is mechanically near zero. Restricted to 2026-09-07 and 2026-09-08, Gemini has n = 384, 3.6% [2.2, 6.0] at 200 characters against 65.1% [60.2, 69.7] on the full text, a difference of +61.5 pp on a mean full length of 3,648 characters. The pooled Gemini row in the table above understates the effect for that reason, and both figures are given rather than only the convenient one.

### What this n permits, and what it does not

**It permits** a within-arm, within-observation statement: on these rows, for these engines, reading the whole response instead of the first 200 characters changes the citation rate by the amounts tabulated, and the change is not attributable to the matching rule, the cohort, the query set or the engine, because all four are held fixed across the paired comparison. The discordant counts are heavily one-sided and the exact McNemar p-values are far below any conventional threshold, so the direction is not in question for the rows observed.

**It permits** the protocol conclusion the paper needs: the window is a first-order parameter for every engine tested, not a quirk of one retrieval-augmented arm, and its magnitude is not predictable from architectural class. A reader who is handed a citation rate without a declared window has been handed a number that could move by tens of percentage points.

**It does not permit** treating the full-text rates as the engines' series-level citation rates. These 2,225 observations come from three days at the very end of the series, ChatGPT and Claude contribute one day each, and every engine's rows sit inside a single stratum of model version and generation settings. The series-level figures remain those of Table 3, measured under the declared 200-character window.

**It does not permit** comparing the deltas between engines as if they were estimates of a stable engine property. The arms differ in which days they contributed, in how long their responses are, and in whether their day-level behaviour was typical; the Gemini stratification above is a concrete case where the pooled delta and the stratified delta differ by more than 30 percentage points. Ranking engines by delta on this table would be reading sampling structure as substance.

**It does not permit** any statement about Groq. Groq left the panel on 2026-08-16, before full-text retention began, so it contributes zero rows here and the window effect on its 14,208 canonical observations is unmeasured and now unmeasurable. That is the irreversible half of the defect the paper documents: an asymmetric window can be corrected because the truncated string is still the string the extractor saw, but no amount of care recovers text that was never stored.

## Reproduction

`NUMBERS.md` in this directory lists every figure above with the SQL statement or the function call that produced it and the value obtained. Nothing in these tables was typed by hand: `build_tables.py` interpolates each figure from the query result into both documents.

