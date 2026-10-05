## 9. Five months of descriptive evidence

### 9.1 Every figure here is descriptive, and the confirmatory window is still open

Every figure below is descriptive and pre-confirmatory, and the constraint that makes it so is arithmetic rather than editorial. The design is observational: the cohort of 127 entities, the battery of 192 queries and the engine panel were fixed before collection, nothing was manipulated, and no estimate here supports a causal reading. The confirmatory window declared in §8.3 has not closed. It counts 90 collected days rather than 90 calendar days, the calendar ninetieth day passed on 2026-07-21, and on 2026-09-11 the count stood at 56 with a projected close of 2026-10-15 (§8.3). The analysis plan of §11 is the instrument for that window; §9 is what the instrument saw on the way there.

The series analysed runs from 2026-04-23 to 2026-09-08 and holds 68,624 canonical observations, read under the uniform 200-character window that §6 requires and re-extracted with the project's own matching rule. Every rate in this section is a head-of-response rate. §6.5 puts the distance between that rate and the whole-response rate at 22.95 to 55.73 percentage points across five arms on 2,225 matched observations, so no figure here should be quoted as an engine's citation rate without the window attached to it.

The sample size that governs inference is not 68,624. The battery re-asks the same 192 prompts twice a day, so the prompts are the population a general claim would have to reach, and they are observed deeply rather than sampled.

**Table E1.** Design effect for the pooled citation rate under two candidate primary sampling units. Series 2026-04-23 to 2026-09-08, 68,624 canonical observations; denominator for each arm is its own canonical rows. The query-clustered columns cluster on the prompts the arm answers, 192 in each arm row and 96 in the retrieval-augmented one, and on the 1,056 engine-by-prompt cells in the panel row. Grok is omitted: with 5 collected days the estimator is not run (`stats/data/s2_dependence.csv`, status `NOT RUN`). Source `stats/data/s2_dependence.csv`.

| Arm | Naive SE (pp) | Day-clustered SE (pp) | Day deff | Query-clustered SE (pp) | Query deff | Effective n (query) |
|---|---:|---:|---:|---:|---:|---:|
| ChatGPT | 0.306 | 0.097 | 0.10 | 2.563 | 70.1 | 216 |
| Claude | 0.357 | 0.159 | 0.20 | 3.017 | 71.6 | 210 |
| Gemini | 0.109 | 0.132 | 1.46 | 0.574 | 27.8 | 553 |
| Perplexity | 0.568 | 0.816 | 2.07 | 3.743 | 43.5 | 178 |
| Groq | 0.234 | 0.133 | 0.32 | 1.883 | 64.7 | 220 |
| **Panel** | **0.147** | **0.193** | **1.74** | **1.166** | **63.3** | **1,083** |

Clustering on the collection day, which the methodology anticipated through a random intercept per date, inflates the pooled standard error by 1.32 and inflates nothing at all in three of five arms, whose day-level design effects sit below one because a day is close to a census of the prompt population. Clustering on the engine-by-prompt cell, 1,056 clusters over the panel, gives a pooled design effect of 63.3, an eightfold inflation, and an effective sample of 1,083 against a nominal 68,624; inside a single arm, where the cluster is the prompt itself, the design effect runs from 27.8 on Gemini to 71.6 on Claude. On the canonical cut the pooled rate of 17.97% carries a naive half-width of 0.29 points, a day-clustered half-width of 0.38 and a prompt-clustered half-width of 2.29.

The multilevel model of §9.2 measures the same dependence coefficient by coefficient and on the square-root scale, where its clustered standard errors run from 2.4 to 10.4 times the binomial ones: an inflation of 8.0 is a design effect of 64, so the 63.3 above and the inflation column of Table E12 are one quantity written two ways. The inflation is smallest on the engine contrasts, which vary inside a prompt, and largest on the covariates that are properties of the prompt, whose block tests carry design effects of 74 to 90 (`stats/S1-multilevel.md`, Tables 4 and 5). The Wilson intervals printed in the tables below are of the first kind, correct for a statement about these 192 prompts as answered by these arms and eight times too narrow for a statement about the population of prompts those 192 were drawn from. Where a claim generalises beyond the battery, the third figure is the one that applies, and the reliability vocabulary of generalizability theory is the natural frame for reporting it [Zatuchin2026a, Bailey2016].

Two stored fields, `selection_status` and `absorption_status`, are proxies derived from mention and from name matching in exposed URLs. Neither demonstrates semantic support by a source nor internal retrieval, and neither enters any figure in this section.

### 9.2 Citation belongs to the prompt and to the firm-engine pair, and almost none of it belongs to the day

Which prompt was asked carries more of the latent variance in citation than which engine answered it, and the collection day carries almost none of it. Two analyses of this series reach that ordering along routes that share no estimator: a multilevel model over 38,195 individual responses, which is the inferential result reported here, and a two-way decomposition of logit coverage over an entity-by-engine grid, which is the convergent one.

The model is a binomial mixed model with crossed random intercepts for prompt and for collection day, fitted on the core-3 balanced design (`stats/S1-multilevel.md`, Table 3): the 96 prompts of the three semantic categories every arm answered, 52 collection days, six engines and 38,195 responses under the uniform 200-character window. The restriction is forced by the panel. The retrieval-augmented arm never ran `confianca`, `experiencia` or `inovacao`, so engine and semantic category are not crossed over the full battery, and a six-engine model fitted on all 192 prompts would extrapolate that arm into three categories it never saw; the six-level category block is therefore tested separately on the five-arm battery of 60,883 responses. Engine enters as a fixed factor with ChatGPT as reference, because a handful of levels cannot identify a variance component; the supplement's stability ladder shows what the attempt returns at the entity level, where a five-level engine component converges at a standard deviation near 6.7 across three independent seeds while the marginal engine logits span 2.94 on the same scale.

Two estimators of the same fixed part are reported because they answer different questions. The variational Bayes fit of the mixed model gives odds ratios conditional on the prompt and the day; a pooled logistic with a two-way cluster-robust covariance on the 96 prompts and the 52 days, with inference on `t(51)`, gives population-averaged ones. The second governs every p-value quoted from this model, because a mean-field variational posterior is anti-conservative and its intervals here run about eight times narrower than the clustered ones. The two disagree by a factor near two on the same contrast, 14.49 against 6.79 for the retrieval-augmented arm against ChatGPT, so a claim about engines in general takes the population-averaged figure and a claim about the same prompt on the same day takes the conditional one.

**Table E12.** Fixed effects of the multilevel model under two estimators. Series 2026-04-23 to 2026-09-08, core-3 balanced design, 38,195 responses on 96 prompts, 52 collection days and 6 engines, uniform 200-character window; reference cell is ChatGPT, fintech, English, directive, `comparativo`. The conditional column is the variational Bayes mixed model with crossed random intercepts for prompt and day, with credible intervals from that posterior; the population-averaged column is the pooled logistic with two-way clustering on prompt and day, `t(51)` intervals and the p-value in the last column. Inflation is the clustered standard error divided by the binomial one. Source `stats/S1-multilevel.md` Tables 3 and 4, computed by `stats/s1_multilevel.py` into `stats/s1_results.json`.

| Term | Conditional OR [95% CrI] | Population-averaged OR [95% CI] | SE inflation | p |
|---|---|---|---:|---:|
| engine = Perplexity | 14.491 [13.666, 15.366] | 6.794 [4.189, 11.018] | 5.76 | 1.70e−10 |
| engine = Claude | 4.861 [4.575, 5.165] | 3.033 [1.519, 6.053] | 8.29 | 0.00222 |
| engine = Grok | 4.729 [3.791, 5.898] | 2.997 [1.834, 4.899] | 2.39 | 4.17e−05 |
| engine = Groq | 0.456 [0.415, 0.500] | 0.617 [0.354, 1.075] | 5.76 | 0.0869 |
| engine = Gemini | 0.016 [0.014, 0.019] | 0.089 [0.050, 0.157] | 3.60 | 2.47e−11 |
| vertical = saude | 0.086 [0.080, 0.093] | 0.220 [0.103, 0.470] | 9.25 | 0.000207 |
| vertical = tecnologia | 0.086 [0.080, 0.092] | 0.162 [0.079, 0.330] | 8.28 | 4.78e−06 |
| vertical = varejo | 0.874 [0.820, 0.931] | 0.801 [0.375, 1.710] | 10.38 | 0.560 |
| language = pt | 0.866 [0.827, 0.908] | 0.852 [0.497, 1.459] | 9.46 | 0.552 |
| query type = exploratory | 0.077 [0.073, 0.081] | 0.211 [0.125, 0.356] | 8.62 | 2.35e−07 |
| category = descoberta | 0.591 [0.560, 0.625] | 0.865 [0.437, 1.713] | 9.84 | 0.673 |
| category = mercado | 0.437 [0.411, 0.464] | 0.857 [0.437, 1.681] | 9.69 | 0.647 |

Two of the engine coefficients describe something narrower than their column labels, and both qualifications are measured on the same specification. Gemini's odds ratio of 0.089 falls to 0.044 when the fit is restricted to the 39 days from 2026-04-23 to 2026-06-09, because the arm pools `gemini-2.5-pro` before the 59-day hole with `gemini-2.5-flash` after it, so the coefficient belongs to a mixture of two models and the version string has to travel with the number. The retrieval arm's 6.794 becomes 21.341 [12.52, 36.38] when the 200-character rule is lifted and that arm alone is scored on its whole stored response, a factor of 3.1 that measures the aperture and reproduces the window argument of §6 at coefficient level. Five further cuts leave the four principal coefficients inside one another's intervals: complete days only, a four-arm panel, byte-identical repeats collapsed, the strict boundary rule at the window edge, and the day index taken in UTC rather than local time. The widest movement among the five is the collapse of repeats, which takes the retrieval arm from 6.794 to 6.508 and Gemini from 0.089 to 0.078 over 31,975 responses; the UTC recoding moves nothing at all.

The size of the design correction is itself a result. Each block of fixed effects was tested by a likelihood-ratio test divided by the generalised design effect of the block it drops, which is the Rao-Scott first-order correction. Engine varies within prompt and within day, carries a design effect of 29.51, and survives at a corrected p of 1.38e−58. Vertical and query type carry design effects of 82.28 and 74.25 and survive at 4.41e−08 and 2.41e−10; the six-level category block on the five-arm battery carries 84.22 and survives at 3.99e−06. Language and the three-level category block do not survive, at 0.549 and 0.870 under design effects of 89.50 and 90.03, which puts the naive inflation of evidence for a prompt-level covariate in this series at a factor of 74 to 90. Thirteen of the seventeen tests in the declared confirmatory family survive Benjamini-Hochberg at a false discovery rate of 5%.

One interaction changes a market reading and two do not reach the threshold. Engine by vertical survives the design correction at a corrected p of 0.00305, and the spread between an engine's best and worst vertical runs from 58.46 points on Grok and 56.07 on Claude down to 17.93 on ChatGPT and 5.00 on Gemini, which is why the all-verticals column of Table E4 summarises the first two badly and the last two well. Its Wald p of 3.72e−35 on the clustered covariance is set aside in favour of the corrected likelihood ratio, because 15 parameters against 52 clusters produce a rank-deficient and anti-conservative sandwich. Query type by vertical fails at 0.645, and the marginal test of engine by language fails at 0.354 for a reason that belongs to the contrast rather than to the effect, which §9.4 measures inside the matched pair.

**Table E13.** Variance decomposition by level, on the latent logistic scale. Series 2026-04-23 to 2026-09-08. The response-level panel is the core-3 balanced design, 38,195 responses over 96 prompts, 52 days and 6 engines, outcome "at least one cohort entity inside the first 200 characters". The entity-level panel takes one response-by-candidate-entity pair as the unit over the five arms truncated at collection time, on a stratified subsample of 5,988 responses giving 166,164 entity-rows, with the intraclass correlation averaged over three seeds and the variance read on seed 11; the retrieval-augmented arm is excluded because its stored text is the whole response, so per-entity restriction to the window is impossible for any entity after the earliest. Engine is carried as a fixed factor in both panels and converted by the Nakagawa-Schielzeth rule. Intraclass correlation is the level's variance over the sum of the components plus the logistic residual of π²/3 ≈ 3.290. Source `stats/S1-multilevel.md` Tables 6a and 6b.

| Level | Response σ² | Response ICC | Entity σ² | Entity ICC |
|---|---:|---:|---:|---:|
| Entity identity | not in the model | — | 10.601 | 0.4641 |
| Prompt | 7.709 | 0.4559 | 5.994 | 0.2840 |
| Engine | 5.905 | 0.3492 | 2.144 | 0.0993 |
| Residual (logistic) | 3.290 | 0.1946 | 3.290 | 0.1491 |
| Collection day | 0.005 | 0.0003 | 0.042 | 0.0011 |

What dominates depends on which question the unit of analysis encodes. With the response as the unit and the outcome "was anybody named", the prompt takes 45.59% of the latent variance and the engine 34.92%, leaving the day at 0.03% (Table E13). With the response-by-entity pair as the unit and the outcome "was this company named", the entity's own identity takes 46.41%, the prompt 28.40% and the engine 9.93%, leaving the day at 0.11%. Whether a Brazilian entity is named at all is mostly a property of the question; which Brazilian entity is named is mostly a property of the entity. Both engine figures are transformations of a fixed factor and not random-effects variances, and they carry that qualifier because a variance component over five or six levels is weakly identified in this design: the entity-level engine share would have been published as 0.69 instead of 0.10 had the stability ladder of `stats/S1-multilevel.md` not been fitted.

The most consequential number in the model is the one that refused to move. Fitting the same crossed random structure with no covariates at all puts the variance between the 96 prompts at 4.005 on the logit scale; adding vertical, language, query type and semantic category, which are four of the five axes the battery was balanced on, puts it at 4.036, a change under 1% and in the direction of a slightly larger component. The four design factors account for none of the variation between prompts, while that variation is the largest component in the response-level decomposition. Whatever makes one prompt orders of magnitude more likely than another to surface a cohort entity is not captured by the axes used to build the battery, and the battery was built on the assumption that it would be.

That result bears directly on P3. Declaring the battery is not the same as characterising it. Two batteries balanced on the same four factors, with equal counts in every cell, can return citation rates far apart, because the factors carry no information about which prompts elicit names, and an adopter who publishes the factorial invariants of §3.1 has made the battery checkable without making it interchangeable with anyone else's. The query-clustered intervals of §9.1 measure the same limit from the sampling side, putting the retrieval arm's 53.78% on this battery at 46.35% to 61.21% on a newly drawn one; §14 carries the threat in its own row.

The second path to the same question starts from a different grid and holds different terms, which is why it is worth reading beside the model rather than in place of it. Citation is also a property of the firm-engine pair: over a balanced grid of 62 named entities by 6 engines, the firm takes 34.46% of the variance in logit coverage, the engine 26.21%, and the firm-by-engine interaction 39.33%, so the largest single term is the one saying that which firm gets named depends on which engine is asked.

**Table E2.** Two-way decomposition of logit coverage. Series 2026-04-23 to 2026-09-08, 62 entities by 6 engines, one observation per cell, rates offset by 1/(2 × 42,487) before the logit; denominator is the total sum of squares. The 62 are the cohort members named at least once in the replicate-reduced grid of 42,487 cells; the 66 of §9.6 counts entities named at least once over all 68,624 observations.

| Source | Sum of squares | Share of total |
|---|---:|---:|
| Entity (firm) | 1,880.12 | 34.46% |
| Engine | 1,429.96 | 26.21% |
| Entity × engine interaction | 2,145.56 | 39.33% |

Neither analysis nests inside the other and their terms do not map one to one. The grid carries no prompt term, since each of its 372 cells aggregates over every prompt that arm answered; the model carries no entity-by-engine interaction, since its entity-level fit holds engine as a fixed factor. Where the two can be compared they agree, and they agree on the two statements a buyer acts on. The collection day is negligible under both, at 0.28% of cell-level variance across 42,487 replicate-reduced cells and at intraclass correlations of 0.0003 and 0.0011, so instability over the five months is not what produces the disagreement between engines, and day-to-day movement in a citation dashboard built on this design is measurement noise unless it survives an interval built on the day cluster. The engine sits below the leading term under both, which is the arithmetic behind the finding that a single per-engine number summarises nothing on the three arms whose spread across verticals exceeds 40 points.

Agreement between engines is low and the low value is not a sampling artefact. On the panel that runs the full five months on the full battery, Fleiss' kappa on the harmonised binary outcome is 0.086 over 9,129 complete cells from 50 days; adding a fourth continuously observed arm raises it to 0.169 over 8,550 cells, which rewards a rater that shares the majority pattern rather than recording convergence. No six-engine figure exists: Groq's last collection day is 2026-08-16 and Grok's first is 2026-08-23, so the six-way panel has zero complete cells.

**Table E3.** Fleiss' kappa on the harmonised binary outcome, by nested panel. Series 2026-04-23 to 2026-09-08, percentile intervals from 2,000 day-cluster bootstrap replications; denominator is complete panel cells.

| Panel | Engines | k | Cells | Days | Base rate | Fleiss kappa | 95% CI |
|---|---|---:|---:|---:|---:|---:|---|
| P1 | ChatGPT, Claude, Gemini | 3 | 9,129 | 50 | 0.151 | 0.0861 | [0.0736, 0.0996] |
| P2 | P1 + Groq | 4 | 8,550 | 47 | 0.135 | 0.1692 | [0.1579, 0.1809] |
| P3 | P1 + Grok | 4 | 542 | 3 | 0.194 | 0.2263 | [0.2170, 0.2371] |
| P4 | P2 + Perplexity | 5 | 4,231 | 47 | 0.259 | 0.1464 | [0.1364, 0.1561] |
| P5 | P3 + Perplexity | 5 | 278 | 3 | 0.311 | 0.2359 | [0.2163, 0.2548] |

P3 and P5 rest on three collection days, so their intervals are printed for symmetry and carry no coverage claim. Against a permutation null that preserves every engine's base rate and destroys cell-level association, all five panels sit 15.5 to 50.2 null standard deviations above the null mean with zero of 2,000 permutations reaching the observed value. The engines are not independent instruments and they are not interchangeable ones either: on P1 the distance from the null is 0.125 kappa points and the distance from perfect agreement is 0.914.

What the engines disagree about is whether a name appears, not which name. Restricted to the 4,988 cell-pairs in which both engines named at least one cohort member, mean Jaccard runs from 0.421 (Groq against Perplexity) to 0.789 (Gemini against Groq) against a uniform-draw null of 0.050 to 0.066, and 65.26% of those pairs share the first-named firm. Pooled over the fourteen pairs that share any cell, 84.4% of 23,949 scored cell-pairs have Jaccard exactly zero, and 18,961 of them are pairs in which exactly one engine named anybody.

Part of the disagreement belongs to the instrument. On 2026-09-08, over the 192 cells the four fully truncated arms share, widening the aperture from 200 characters to the whole response moves four-arm Fleiss from 0.2371 to 0.4881 and Claude against Gemini from 0.126 to 0.633, with the base rate moving from 0.182 to 0.672. The gain does not extend to the pairs containing the retrieval-augmented arm, where kappa loses discriminating power as prevalence approaches the ceiling. Two arms also carry a ceiling of their own: same-day test-retest kappa is 0.669 for Perplexity over 2,687 replicated cells and 0.725 for Grok over 288, so part of what is counted as between-engine disagreement in those arms is within-engine instability, which this series does not decompose.

### 9.3 Vertical asymmetry, and the concentration that travels with it

Verticals differ more in how concentrated their coverage is than in how many firms they leave out. At panel level the citation rate runs from 26.80% in fintech (n = 17,225) to 10.53% in health (n = 17,146), and the within-vertical Herfindahl-Hirschman index runs from 0.4395 in fintech to 0.1470 in technology, a factor of three between cohorts of the same size.

**Table E4.** Citation rate under the uniform 200-character window by engine and vertical, with within-vertical concentration on the real cohort. Series 2026-04-23 to 2026-09-08, 68,624 canonical observations; denominator for each rate is the canonical rows of that cell, and for each index the mentions of that vertical. Bootstrap intervals on the indices are percentile over 2,000 observation-cluster replicates.

| Engine | Fintech | Retail | Health | Technology | All |
|---|---:|---:|---:|---:|---:|
| ChatGPT | 18.1 | 22.4 | 7.7 | 20.4 | 17.2 |
| Claude | 50.8 | 30.4 | 11.0 | 10.3 | 25.7 |
| Gemini | 4.4 | 2.5 | 0.0 | 0.5 | 1.9 |
| Groq | 9.4 | 12.8 | 6.0 | 5.9 | 8.5 |
| Perplexity | 67.8 | 68.4 | 44.5 | 26.9 | 52.0 |
| Grok | 59.0 | 40.6 | 10.4 | 5.5 | 29.6 |
| **Panel** | **26.8** | **23.2** | **10.5** | **11.2** | **18.0** |
| Panel n | 17,225 | 17,204 | 17,146 | 17,049 | 68,624 |
| HHI [95% CI] | 0.4395 [0.4221, 0.4583] | 0.2640 [0.2566, 0.2717] | 0.1819 [0.1741, 0.1909] | 0.1470 [0.1400, 0.1550] | 0.0970 [0.0945, 0.0999] |
| Equivalent firms (1/HHI) | 2.28 | 3.79 | 5.50 | 6.80 | 10.31 |
| Firms taking half the mentions | 1 | 2 | 2 | 3 | 4 |
| Never named, of the real cohort | 11 of 27 | 12 of 28 | 12 of 28 | 10 of 28 | 45 of 111 |

The panel ordering is a mixture over arms with very different levels and is not a property of the verticals. Retail leads three of the six arms and fintech the other three; technology trails four of six and health two. Gemini in health is a hard zero over 3,840 observations, with a Wilson upper bound of 0.100%, which under the reading of §6 is a statement about the first 200 characters of a Gemini answer rather than about what Gemini knows. The pooled index of 0.0970 answers a question the battery never asked, since no query ever placed a bank and a hospital in the same choice set. The exclusion rate, by contrast, barely moves: 35.7% to 42.9% of the real cohort is never named in any vertical, so the four markets differ in who dominates the visible part and agree on how much of the cohort stays invisible.

### 9.4 Language, and why measuring a Brazilian brand only in English inverts the answer

Ask the same question of the same engine on the same day in Portuguese rather than English and the chance of a Brazilian cohort entity appearing in the first 200 characters falls by 4.54 points. The battery was built as 96 matched Portuguese and English pairs, and the paired contrast is what identifies the language effect, because language varies only between prompts in the marginal model and the prompt carries 45.59% of the latent variance (§9.2). A pair is one prompt in both languages sharing vertical, semantic category, query type and temporal variant, matched inside the same engine on the same collection day, with one observation per engine, day and prompt taken as the first run by timestamp so that a repeated run cannot enter a pair twice. The design yields 21,862 complete pairs over 52 days.

**Table E14.** Paired Portuguese against English contrast, overall and by engine. Series 2026-04-23 to 2026-09-08, 21,862 matched pairs over 52 collection days under the uniform 200-character window. `Rate PT` and `Rate EN` are the two halves of the same pairs; the paired difference is the mean of the within-pair difference in percentage points, with a day-clustered interval; `PT-only` and `EN-only` are the discordant counts; `p` is the exact McNemar binomial test on those discordant pairs, and all seven survive Benjamini-Hochberg inside the confirmatory family of 17. Source `stats/S1-multilevel.md` Table 8.

| Stratum | Pairs | Days | Rate PT | Rate EN | Paired difference (pp) | 95% CI (pp) | PT-only | EN-only | p exact |
|---|---:|---:|---:|---:|---:|---|---:|---:|---:|
| All engines | 21,862 | 52 | 0.1595 | 0.2049 | −4.54 | [−4.90, −4.17] | 1,009 | 2,001 | 2.86e−74 |
| ChatGPT | 4,800 | 50 | 0.1110 | 0.2352 | −12.42 | [−12.95, −11.89] | 122 | 718 | 1.86e−103 |
| Groq | 4,512 | 47 | 0.0512 | 0.1166 | −6.54 | [−6.98, −6.10] | 13 | 308 | 2.36e−74 |
| Grok | 462 | 5 | 0.2727 | 0.3333 | −6.06 | [−9.81, −2.31] | 26 | 54 | 0.00232 |
| Gemini | 4,893 | 51 | 0.0092 | 0.0286 | −1.94 | [−2.23, −1.65] | 13 | 108 | 8.37e−20 |
| Claude | 4,765 | 50 | 0.2478 | 0.2667 | −1.89 | [−2.54, −1.24] | 417 | 507 | 0.00339 |
| Perplexity | 2,430 | 52 | 0.5642 | 0.5181 | +4.61 | [+2.54, +6.68] | 418 | 306 | 3.58e−05 |

The engines do not share a direction, and the pairing supplies the design-valid instrument for that heterogeneity. Five arms lose ground in Portuguese and the retrieval-augmented one gains 4.61 points; regressing the within-pair difference on the engine, with errors clustered on day and on pair, puts that arm 17.03 points above ChatGPT with an interval of [6.86, 27.20] and Gemini 10.47 above it at [3.02, 17.93], under a block test of F(5, 51) = 3.17 at p = 0.0145, which survives Benjamini-Hochberg. The same engine-by-language interaction fails at p = 0.354 on the marginal model, and the gap between the two answers is one of design: pairing removes the prompt effect that carries 45.59% of the variance, and nothing about the data changed between the two fits. A Brazilian firm optimising for Portuguese-language prompts works against ChatGPT's grain by roughly 12 points and with the retrieval arm's grain by roughly 5, which is why the language of the battery belongs beside the figure for every arm separately.

The marginal contrast is the same effect read through a comparison the design cannot support, and it is reported here as context for the paired figure. Over the full canonical cut, 20.22% of the 34,310 English observations carry a citation against 15.72% of the 34,314 Portuguese ones, with Perplexity again running the other way at 54.17% in Portuguese against 49.90% in English. Entered as a fixed effect, language returns an odds ratio of 0.852 [0.497, 1.459] at a two-way clustered p of 0.552 (Table E12) and a design-corrected likelihood-ratio p of 0.549 under a design effect of 89.50, which measures the power of a between-prompt contrast where the prompt carries 45.59% of the variance. Publishing only the marginal figure would report a null the pairing contradicts at p = 2.86e−74 over 21,862 pairs. The interaction with the firm's origin is where the remaining measurement decision lies.

**Table E5.** Per-slot naming rate by group and language, and the language interaction. Series 2026-04-23 to 2026-09-08, 68,624 canonical observations. Per-slot rate is mentions divided by (observations × entities in the group), which is the probability that a given cohort member is named in a given answer. Log rate ratio is Brazilian over anchor; intervals are percentile cluster bootstrap over observations, 2,000 replicates.

| Vertical | Brazilian rate, PT | Anchor rate, PT | Brazilian rate, EN | Anchor rate, EN | log RR, PT | log RR, EN | Difference (PT less EN) | 95% interval | Bootstrap p |
|---|---:|---:|---:|---:|---:|---:|---:|---|---:|
| Fintech | 1.921% | 0.001% | 2.416% | 0.001% | 7.188 | 7.417 | −0.229 | [−1.364, 0.898] | 0.5885 |
| Retail | 1.339% | 0.645% | 1.933% | 0.324% | 0.730 | 1.786 | −1.056 | [−1.211, −0.910] | < 0.0005 |
| Health | 0.833% | 0.289% | 0.615% | 0.124% | 1.059 | 1.602 | −0.543 | [−0.992, −0.191] | 0.0020 |
| Technology | 0.252% | 1.056% | 0.886% | 0.348% | −1.434 | 0.936 | −2.370 | [−2.590, −2.153] | < 0.0005 |
| All | 1.078% | 0.497% | 1.453% | 0.199% | 0.775 | 1.988 | −1.213 | [−1.339, −1.090] | < 0.0005 |

Asked in Portuguese about Brazilian technology and IT, the engines name an international anchor at 1.056% per slot against 0.252% for a Brazilian firm, a rate ratio of 0.24. Asked the same question in English, from the same battery translated, the ratio is 2.55 the other way. The difference of 2.370 on the log scale is a sign change rather than a change of magnitude, and its interval excludes zero by a wide margin. Retail and health favour Brazilian firms in both languages and favour them more strongly in English. Fintech records 2 anchor matches in 137,800 entity slots, so its rate ratio is numerically unstable and is tabulated without interpretation.

The consequence for anyone measuring a Brazilian brand is direct. A visibility figure taken only in English reports the language in which local firms do best against international anchors across the panel, at a pooled log rate ratio of 1.988 against 0.775 in Portuguese, and in technology it reports the only language in which the local firm leads at all. A brand whose customers ask in Portuguese and whose dashboard asks in English is reading a different measurand, and the gap is largest exactly where a Brazilian technology vendor competes with a global consultancy. Declaring the language of the battery is therefore not a courtesy to the reader; it is the condition under which the figure identifies a quantity, which is the same argument the window carries in §6 and which the cross-language literature reaches from the sampling side [Zatuchin2026c]. A parallel result holds for the provenance of the model rather than the language of the query. Over 1,909 English-only queries put to six models about 30 brands, Chinese-developed models mention a brand in 88.9% of answers against 58.3% for internationally developed ones, a gap of 30.6 points that survives identical wording, because a brand absent from a model's training corpus has no presence in its answers whatever its quality [Huang2026].

### 9.5 Directive queries buy names, and one arm runs half the categories

A question that asks for a named best is answered with a name two and a half times as often as one that asks for the landscape. Directive queries carry a citation in 25.93% of 34,319 observations against 10.00% of 34,305 exploratory ones, and the ordering holds in every one of the six arms.

**Table E6.** Citation rate under the uniform 200-character window by query type and by semantic category. Series 2026-04-23 to 2026-09-08, 68,624 canonical observations; denominator is the canonical rows of each cell. The five-arm rows are the panel rows of T7c with the Perplexity row subtracted, since that arm runs only three of the six categories; their intervals are Wilson on the resulting counts (`tables/NUMBERS.md` T7c). Per-arm counts by query type are in T7b of the same file.

| Stratum | Level | n | Rate [95% CI] |
|---|---|---:|---|
| Query type | directive | 34,319 | 25.93 [25.47, 26.40] |
| Query type | exploratory | 34,305 | 10.00 [9.69, 10.32] |
| Category, panel | comparativo | 12,742 | 27.00 [26.23, 27.78] |
| Category, panel | descoberta | 12,744 | 25.15 [24.40, 25.91] |
| Category, panel | mercado | 12,709 | 25.05 [24.30, 25.81] |
| Category, panel | confianca | 10,152 | 12.50 [11.87, 13.16] |
| Category, panel | inovacao | 10,131 | 9.07 [8.53, 9.65] |
| Category, panel | experiencia | 10,146 | 3.08 [2.77, 3.44] |
| Category, five arms | mercado | 10,136 | 20.81 [20.03, 21.61] |
| Category, five arms | comparativo | 10,158 | 19.97 [19.21, 20.76] |
| Category, five arms | descoberta | 10,160 | 16.36 [15.65, 17.09] |
| Category, five arms | experiencia | 10,146 | 3.08 [2.77, 3.44] |

The spread across categories is wider than the spread across verticals and narrower than the spread across engines, and it is the stratum most obviously confounded with the window, since an exploratory answer has more reason to open with framing prose before it reaches a name. Within-arm the type contrast runs from 2.73% of 7,679 directive observations against 0.98% of 7,676 exploratory ones on Gemini, to 74.03% of 3,873 against 30.02% of 3,868 on Perplexity, so its magnitude is engine-specific even where its sign is not.

The category panel row mixes compositions and should not be read as a category effect. Perplexity runs 96 of the 192 canonical queries, and the three categories it runs (`descoberta`, `comparativo`, `mercado`) are the discovery-shaped ones with the highest rates, so three of the six columns carry a six-arm mixture and three carry a five-arm one. Restricting to the five arms that run all six categories narrows the range from 27.00% to 3.08% down to 20.81% to 3.08% and removes the artefact. A comparison across categories is defensible within an engine row or on the restricted panel, and nowhere else in this table.

### 9.6 How few firms are ever named, and what the tail will not tell us

Four firms take half of every entity mention the six engines produced in five months, and 45 of the 111 real cohort members were never named at all. The Gini coefficient over the real cohort is 0.8499 with a bootstrap interval of [0.8471, 0.8533] on 19,057 mentions, and the reported HHI of 0.0970 corresponds to 10.31 equally sized participants against a cohort of 111.

**Table E7.** Concentration, exclusion and what predicts it. Series 2026-04-23 to 2026-09-08, 68,624 canonical observations under the uniform window. Coverage counts an entity once per observation in which it appears; first mentions count it only when it is the earliest cohort name. Odds ratios come from a logistic regression of never being named on the attributes the cohort file carries, fitted on the 111 real members with Brazilian, head tier and fintech as the reference cell.

| Quantity | Coverage (19,057 mentions) | First mentions (12,329) |
|---|---:|---:|
| Gini over the real cohort of 111 | 0.8499 [0.8471, 0.8533] | 0.9310 |
| Gini over named entities only | 0.7475 (66 named) | 0.8176 (42 named) |
| HHI, 0 to 1 | 0.0970 | 0.1917 |
| Top-1 share | 24.16% | 37.27% |
| Top-5 share | 56.04% | 76.98% |
| Entities taking half the total | 4 | 2 |

| Term in the exclusion model | Odds ratio | 95% interval | Block LR p |
|---|---:|---|---:|
| Long-tail tier (against head) | 11.401 | [2.921, 44.499] | 0.0007 |
| Torso tier (against head) | 3.887 | [1.063, 14.215] | (tier block) |
| International anchor (against Brazilian) | 5.418 | [1.636, 17.941] | 0.0033 |
| Vertical, three contrasts against fintech | 0.699 to 1.695 | — | 0.5899 |
| Founding year, per decade later | 1.109 | [0.945, 1.302] | 0.1931 |

Tier is the attribute that separates. A long-tail firm carries 11.4 times the odds of never being named that a head firm carries, the tier block returns a likelihood-ratio p of 0.0007 on 111 entities of which 45 are never named, and the model reaches a McFadden pseudo-R² of 0.1467. Vertical separates nothing, which agrees with the exclusion row of Table E4. The anchor coefficient needs the caveat printed with it: all 32 international anchors are head tier, so the adjusted odds ratio of 5.418 compares anchors with Brazilian head firms alone, 15 of 32 (46.9%) against 5 of 34 (14.7%), while unadjusted the two groups barely differ at 46.9% against 38.0%. The confounding between group and tier is total, and the adjustment produces the whole contrast.

The shape of the upper tail is not determined, and saying so is the result. Under the Clauset-Shalizi-Newman rule the estimated xmin sits at 246 mentions, which leaves 19 entities in the fitted tail out of 66 with any mention at all. The exponent is 2.225 with a 95% interval of [1.674, 2.776], the bootstrap goodness of fit does not reject the power law (p = 0.9570), and the likelihood-ratio comparison against a lognormal returns a normalised R of −0.0091 with p = 0.9927, which is the numerical statement that the two families fit the same 19 points equally well. The fitted lognormal is degenerate along a ridge. The constraint is structural rather than temporal: the cohort holds 111 real firms by design and 66 were ever named, so no amount of further collection puts more than a few dozen points into a tail fit. The sentence "citation follows a power law" is not available from this design, and an exponent quoted without the 19 would be a stronger claim than the data carry.

Answers name firms in clumps. Across the 68,624 observations, 82.03% name nobody, 12.42% name exactly one entity and 5.54% name two or more, with a mean of 0.2777 and a variance-to-mean ratio of 1.993. A negative binomial fitted with an intercept alone beats the Poisson on both information criteria (AIC 89,146 against 99,876) and beats the zero-inflated Poisson (90,882), reproducing the observed zero count to within 55 answers; the zero-inflated negative binomial estimates its inflation probability at 1.01 × 10⁻⁵ and BIC prefers the simpler model by 11.14. Abstention was measured directly on the probe stratum and §7.2 reports it; position inside the answer is reported in §6.6, where the relative offset stops separating the engines once the truncation is removed. The zeros carry no manufactured names either, since no decoy was named spontaneously in any of the 68,624 canonical observations, which holds the 95% Wilson upper bound on the instrument's spontaneous false-positive rate at 0.0056% on the panel and at 0.342% on the 1,118 observations of the seventeen-day Grok arm (§7.1). One overdispersed process generates the zeros and the multiple mentions alike, so nothing in the count distribution requires a separate abstention mechanism, and a reader who sees a zero in Table E4 is looking at silence inside the window rather than at a refusal the instrument classified.

**Figure E1.** Lorenz curves of entity coverage, one line per denominator, drawn from `stats/data/s4_lorenz_global.csv` (four series: mentions over the real cohort of 111, over the full cohort of 127, over the 66 named entities, and first mentions over the real cohort) with the by-vertical panel from `stats/data/s4_lorenz_by_vertical.csv`. Horizontal axis, cumulative share of entities from 0 to 1; vertical axis, cumulative share of mentions. The diagonal is drawn for reference and each curve is labelled at its right-hand end with its Gini. The spread between the named-only curve at 0.7475 and the real-cohort curve at 0.8499 is the whole content of the denominator choice.

### 9.7 What the series does over time, and what that implies for reporting frequency

Ranking is the part of this measurement that survives a week; the level of an individual mid-tier entity is not. Before any of that reads as a time series, the calendar has to be declared. The span of 139 days holds observations on 52 of them under the local-date rule of §8.2, 37.4% coverage, or on 53 under the UTC rule of Appendix D. One hole runs 59 consecutive days, from 2026-06-10 to 2026-08-07, and July is empty in full. A reader who treats the series as a four-and-a-half-month daily panel overstates its temporal density by a factor of 2.7, and any line fitted across it interpolates over two months of no observation (§8.2).

**Table E8.** Trend per arm in percentage points per 30 calendar days, on the daily rate under the uniform window. Series 2026-04-23 to 2026-09-08; denominator for each arm is its collected days. Theil-Sen carries a distribution-free interval; Mann-Kendall is reported under the standard variance and under the Hamed-Rao variance inflated by the autocorrelation of the de-trended ranks; the logistic model is fitted at observation level with day-clustered errors and q is Benjamini-Hochberg over the twelve rows that were run, the three Grok rows carrying no p-value. Source `stats/data/s2_trend.csv`.

| Arm | Cut | Days | Rate (%) | Theil-Sen pp/30 d | MK p | MK p (Hamed-Rao) | Logistic pp/30 d | Logistic q |
|---|---|---:|---:|---|---:|---:|---|---:|
| ChatGPT | all days | 50 | 17.17 | 0.00 [−0.07, +0.18] | 0.559 | 0.580 | −0.01 [−0.16, +0.13] | 0.858 |
| Claude | all days | 50 | 25.75 | 0.00 [−0.22, +0.12] | 0.710 | 0.564 | −0.12 [−0.34, +0.08] | 0.366 |
| Gemini | all days | 51 | 1.86 | +0.49 [+0.31, +0.60] | 6.0e−6 | 0.010 | +0.41 [+0.30, +0.53] | 2.6e−13 |
| Gemini | pre 2026-06-17 | 38 | 1.41 | +0.03 [0.00, +0.58] | 0.231 | 0.349 | +0.33 [+0.03, +0.69] | 0.079 |
| Gemini | post 2026-06-17 | 13 | 2.97 | 0.00 [−1.74, +1.12] | 0.950 | 0.938 | −0.81 [−2.15, +0.76] | 0.395 |
| Groq | all days | 47 | 8.52 | +0.38 [0.00, +0.52] | 0.001 | 0.106 | +0.50 [+0.41, +0.59] | 3.2e−25 |
| Perplexity | all days | 52 | 52.03 | −1.81 [−3.91, −0.44] | 0.009 | 0.113 | −0.89 [−1.68, −0.10] | 0.051 |
| Perplexity | complete days | 44 | 51.74 | −2.37 [−4.69, −0.76] | 0.002 | 0.039 | −1.21 [−2.04, −0.37] | 0.012 |
| Grok† | any cut | 5 | 29.61 | not run, fewer than 8 collected days | | | | |

† Fewer than 30 daily points; the arm entered on 2026-08-23 and the row is descriptive.

Four arms of six show no trend once the series is read correctly. ChatGPT and Claude are flat under all three estimators, with ChatGPT's daily rate confined between 15.62% and 19.43% on every day meeting the 30-observation threshold. Gemini's headline slope of +0.49 points per 30 days is a level difference between `gemini-2.5-pro` at 1.41% and `gemini-2.5-flash` at 2.97%, spread across the calendar as though it were gradual, and it vanishes inside each segment (p = 0.231 before the boundary, p = 0.950 after). Groq's slope survives the naive test at p = 0.001 and falls to p = 0.106 once the autocorrelation correction is applied, with the change-point analysis placing the whole movement inside the 59-day hole. Perplexity is the one arm whose slope survives the autocorrelation correction, at −2.37 points per 30 days on the complete-day cut, with a Hamed-Rao Mann-Kendall p of 0.039 and a day-clustered logistic Benjamini-Hochberg q of 0.012. Under Benjamini-Hochberg applied to the Hamed-Rao family itself, that arm reaches q = 0.157 and no arm clears 0.05. The window is harmonised out of the series by construction, so the decline is not a window artefact, and §8.4 records that the same arm carries three undeclared ruptures of 5 to 8 points.

Rank stability splits by unit. Between consecutive weeks the ordering of engines is identical in all twelve week pairs, Kendall tau-b 1.000, and that figure is blind to the only change that reordered the panel. Grok entered at 39.2% over the 158 canonical observations of its first week, second in the panel, demoting Claude and ChatGPT one place each, and a tau computed on arms common to both weeks never sees the substitution. Entity ordering behaves the opposite way. Mean tau-b across consecutive weeks is 0.871 over the full cohort of 111 and 0.800 over active entities, with a top-10 overlap of 0.892, while 57.5% of active entities move three or more ranks from one week to the next, 35.5% move five or more, and the mean of the twelve weekly median displacements is 3.5 ranks against a median of 3. The churn sits in a middle band of roughly fifty entities with coverage between about 0.5% and 10%, since 66 of the 111 are ever cited and 45 never are.

That pattern sets a reporting rule with a number attached. A brand in the top ten can be measured monthly and will not be misread. The second daily round buys precision and nothing else: paired within the day over the 24 days on which both rounds ran, the pooled morning-minus-evening difference is +0.01 points with an interval of [−0.21, +0.22], and no arm-level contrast survives correction over the family of fourteen tests. Findings of this kind also carry a shelf life, which is the reproduction problem algorithm audits have already met [Mosnar2025]. A brand in the middle band, measured in any single week, has a better than even chance of being placed three or more ranks from where the next week would place it, which is why a claim about its position needs a multi-week average or an explicit interval rather than a weekly snapshot, and why P4 pins a model snapshot against silent provider updates [Chen2024].

## 10. The reporting index, and evidence against leaning on it

### 10.1 The index, and the three components it is made of

BRGEO-1 defines a reporting index and then constrains everything except the index. Let *E* be the cohort, *M* the engine panel, *w* the declared window and *μ* the matching rule of P6, returning the offset of the first mention of entity *e* in a response or infinity if absent. Coverage *C<sub>w</sub>(e)* is the share of panel observations naming *e* within the window; prominence *P<sub>w</sub>(e)* is one minus the offset of the first mention divided by *w*, averaged over the observations in which *e* appears, normalised by the declared window rather than by response length so that it stays comparable across engines; breadth *B<sub>w</sub>(e)* is the share of panel engines naming *e* at least once. The index is their geometric mean:

$$\mathrm{GCI}_w(e) = \left( C_w(e) \cdot P_w(e) \cdot B_w(e) \right)^{1/3}$$

The geometric mean is invariant to rescaling of the components and penalises imbalance more heavily than the arithmetic mean, which is the ground on which the composite-indicator review recommends it [Greco2019]. The geometric mean is called non-compensatory, and that holds only in the limit: it vanishes when a component is exactly zero, and an entity absent from one engine of six retains *B* = 5/6, so the penalty is gradual. Panel membership is the one decision in this definition that the specification does not yet fix, and §14 records what that cost: the reference implementation resolved it in code twice, first by an undeclared minimum observation count and then by a recency rule, and neither value appears in BRGEO-1. What the specification does require is that the three components be published alongside the index, and §10.2 is the reason.

### 10.2 One component carries three quarters of the index

The composite tracks simple coverage almost exactly, and that agreement is a symptom rather than a reassurance. Across the 66 entities cited at least once, Spearman rank correlation between the composite and coverage is 0.982, holding at 0.979 with each vertical's leader removed, 0.949 over the 42 entities with coverage between 0.1% and 5%, and 0.956 over the 42 below 1%. The 61 never-cited entities are excluded because Spearman is undefined over a mass of ties at zero, which is selection on the outcome and is declared as such.

Every index figure in §10.2 and §10.3 was recomputed on 2026-09-11 over the cut this paper declares, by `stats/s6_index.py`, and the earlier figures are superseded. They were produced by the reference implementation on a snapshot that closed on 2026-08-31 with 66,399 canonical observations, under a panel selected by the undeclared observation count §14 records, and were reported under a caption naming the series that closes on 2026-09-08. The subset correlations barely move: 0.978 becomes 0.979, 0.945 over 42 entities becomes 0.949 over the same 42, and 0.960 over 44 becomes 0.956 over 42, since two entities that sat below 1% coverage on the shorter cut sit above it on the longer one. The variance shares and the aggregation matrix move enough to be worth naming, and each is named where it appears.

Re-running the same script on the superseded cut, under the panel rule in force when those figures were produced, establishes something the earlier table did not declare. With the cut closed at 2026-08-31 and the panel restricted to arms holding at least 500 observations, the variance shares come back at 74.7%, 16.9% and 8.4%, identical to the figures published, and the aggregation matrix comes back within 0.007 of every published cell. Two published values do not come from that configuration: Var(log) of coverage at 4.490 and the count of seven entities holding their exact rank both reproduce on the six-arm panel over the same cut, which returns shares of 72.9%, 19.1% and 8.1% instead. The earlier table was therefore assembled from more than one run, which is a second reason to read the recomputation here rather than it.

**Table E9.** Variance decomposition of the log index over the 66 entities cited at least once. Series 2026-04-23 to 2026-09-08, 68,624 canonical observations under the uniform 200-character window, over the panel of six arms that contributed to the series; contribution is Cov(log X, log GCI) / (3 · Var(log GCI)) and the three contributions sum to unity. Computed by `stats/s6_index.py`, source `stats/data/s6_variance_decomposition.csv`. The figures published on the 2026-08-31 cut were 4.490 and 74.7%, 0.306 and 16.9%, 0.198 and 8.4%.

| Component | Var(log) | Contribution |
|---|---:|---:|
| Coverage | 4.360 | 72.4% |
| Breadth | 0.369 | 18.8% |
| Prominence | 0.188 | 8.7% |

Coverage varies by orders of magnitude across the cohort while prominence and breadth are confined to narrow ranges, so the geometric mean inherits coverage's dominance by construction. Nominal weights of one third each produce effective weights of 72.4%, 18.8% and 8.7%, which is the gap between nominal and effective importance that the ratings literature formalises [Paruolo2013]. A buyer told that an index balances three signals is holding a coverage figure with two decorations. The panel rule moves the shares by about a point and moves nothing else: recomputed over the five arms the recency rule of the reference implementation selects on this cut, the same three shares read 73.6%, 17.5% and 9.0% over the same 66 entities.

### 10.3 Aggregation is unstable, and the specification declines to settle it

Comparing a composite against one of its own components tests nothing about aggregation. The test is against alternative aggregations of the same three components, and the OECD handbook and the sensitivity-analysis literature prescribe exactly that [Nardo2008, Saisana2005].

**Table E10.** Spearman rank correlation between four aggregations of the same three components, and between each and simple coverage. Series 2026-04-23 to 2026-09-08, 68,624 canonical observations under the uniform 200-character window, over the panel of six arms that contributed to the series; n = 66 entities cited at least once. The weighted form is 0.6·C + 0.25·P + 0.15·B, an arbitrary but defensible choice included to show that a plausible weighting diverges. Computed by `stats/s6_index.py`, source `stats/data/s6_aggregation_matrix.csv`. On the 2026-08-31 cut the six off-diagonal values read 0.816, 0.983, 0.787, 0.734, 0.984 and 0.706, and the coverage column read 0.982, 0.728, 1.000 and 0.700.

| | Geometric | Arithmetic | Harmonic | Weighted | Against coverage |
|---|---:|---:|---:|---:|---:|
| Geometric (GCI) | 1.000 | 0.870 | 0.983 | 0.836 | 0.982 |
| Arithmetic | 0.870 | 1.000 | 0.788 | 0.985 | 0.784 |
| Harmonic | 0.983 | 0.788 | 1.000 | 0.752 | 0.9997 |
| Weighted | 0.836 | 0.985 | 0.752 | 1.000 | 0.748 |

The harmonic mean all but reproduces the coverage ordering, because it is dominated by the smallest component and coverage is smallest by orders of magnitude: ten of the 66 entities exchange places with an immediate neighbour and none moves further, which the earlier cut rounded to a correlation of 1.000. The aggregations not dominated by the minimum diverge from coverage and from each other, with the correlation between two defensible choices falling to 0.752 across 66 entities, against 0.706 on the earlier cut. Rank displacement between the composite and coverage has a median of 2 positions, a ninetieth percentile of 6 and a maximum of 14 out of 66, and only 9 of the 66 entities keep their exact rank; the earlier cut gave the same median and ninetieth percentile, a maximum of 10 and 7 entities holding rank. Under the five-arm recency panel the median and the ninetieth percentile hold again, the maximum falls to 12 and 13 entities keep rank, so the conclusion does not turn on which panel rule is in force. An entity's published position therefore depends on a formula choice that no property of the data adjudicates.

A standard should spend its authority where disagreement is large and resolvable. The observation window moves a single arm by 22.95 to 55.73 points and moves it for a reason that can be investigated and corrected (§6.5); the aggregation formula moves ranks by a median of 2 positions for reasons that reduce to taste. BRGEO-1 therefore fixes the conditions of observation, requires the three components to be published beside any index, and leaves the aggregation free, which is the opposite of the practice one recent multi-industry map records, a single branded score published with the components withheld [Zatuchin2026d]. Composite indicators are used for advocacy as well as for analysis [Saltelli2007], and a custodian that sells services in the measured domain answers that objection by measuring how arbitrary its own index is and publishing the measurement.

The reference implementation carried a defect against this specification, and it belongs in the record rather than in a footnote. Panel membership was filtered by a minimum observation count that the implementation did not declare, and on the cut of 2026-08-31 that threshold excluded an arm holding 96 observations that was live and retained an arm retired on 2026-08-16, which moved breadth, the component carrying 18.8% of the index variance, for one vertical. Commit `51159fd` of 2026-08-31 replaced the count by a 14-day recency rule anchored on the last timestamp of the data. Every index figure published before 2026-09-11 was computed on the earlier panel and is superseded by the recomputation above; §14 records the finding, and the code no longer carries it.

## 11. Pre-specified analysis plan

The confirmatory window closes at 90 collected days, projected for 2026-10-15, with 56 of the 90 reached on 2026-09-11. Nothing below is confirmatory. The plan is recorded in advance of one, and the close date has moved: a forecast made on 2026-08-10 put it at 2026-09-28 under an assumed collection rate that the credit outages of August and September broke, costing seventeen days of series (§8.3). A window defined in collected days converts an outage into a schedule extension, which is a design choice a reader should see declared rather than infer from a moving date.

The plan is published in the project repository with a verifiable commit date, and it is not registered with any independent third party. A repository under the author's control offers no guarantee that the plan was not edited after the data were seen, since the same party holds the history and the authority to rewrite it. What publication in the repository does buy is a dated artefact a reviewer can diff against the analysis code; what it does not buy is the property that makes a pre-registration worth citing. §13 lists independent registration of the next window as a governance commitment.

**Table E11.** Hypotheses for the confirmatory window, with the test, the minimum effect the design can detect and the multiplicity treatment. Minimum detectable differences are computed at 80% power on the 2,225-observation full-text cohort of 2026-09-06 to 2026-09-08 (Table S5.12), which is the only stratum in which both windows exist, and account for the design effect measured there; source `stats/data/s5_power_mde.csv` and Table E1. The confirmatory window will carry more power than these figures imply, because it runs over 90 collected days rather than three.

| # | Hypothesis | Test | Minimum meaningful or detectable effect | Multiplicity |
|---|---|---|---|---|
| H1 | Citation rates differ across verticals | Likelihood-ratio test on the vertical fixed effect in a mixed-effects logistic model with random intercepts per query and per collection day | Cramér's V ≥ 0.15; per-vertical paired MDE 6.6 to 8.2 pp unclustered, 10.8 to 16.0 pp under the estimated design effect | BH within the family of six |
| H2 | Fabrication on fictitious entities differs across engines | Three-way outcome of §7.2 on human-validated labels, tested across arms | Requires probe coverage of all six arms at declared battery size and the annotation study of §14; not estimable until both exist | BH within the family of six |
| H3 | Inter-engine agreement differs by vertical | Fleiss' kappa on the rectangular query-by-engine panel, per vertical, with day-cluster bootstrap intervals | A vertical whose interval excludes the panel figure of 0.086 (P1, 9,129 cells) | BH within the family of six |
| H4 | At least one engine has a non-stationary citation rate | Slope on day index, Mann-Kendall under the Hamed-Rao variance and day-clustered logistic, on collected days only, stratified at every declared boundary of §8.1 | 2.37 pp per 30 days is what the current series detects on the arm with the largest movement | BH across arms and within the family of six |
| H5 | Directive queries yield higher citation rates than exploratory ones | Two-proportion contrast within engine, cluster-robust on query | Cohen's h ≥ 0.2; the observed panel contrast is 25.93% against 10.00% on 34,319 and 34,305 observations | BH within the family of six |
| H6 | Window damage varies across engines and is predicted by preamble share rather than engine class | Logistic model of whether the 200-character window misses a citation, with preamble, log response length and engine, on rows retaining the whole response | Between-engine: paired MDE 5.6 to 12.9 pp by arm, 5.8 to 13.1 pp once the arm's design effect is applied; within-engine: the fitted odds ratio of 7.72 is the effect the design already resolves | BH within the family of six |

H6 has already been run in a descriptive register on the 2,225 observations that retained the whole response, and it splits down the middle (§6.6). The negative half survives: engine class does not order the damage, since four parametric arms span +30.73 to +55.73 points and the single retrieval-augmented arm sits at the bottom at +22.95. The positive half fails as stated: preamble share does not order the engines. On the pooled five-arm cohort its Spearman correlation against the delta is −0.154 (p = 0.805), against +0.800 (p = 0.104) for median response length and +0.300 (p = 0.624) for median first-mention offset; on the restricted set that removes the Gemini retention defect of 2026-09-06, preamble reaches only +0.667 (p = 0.219) while length and offset both reach +0.900 (p = 0.037). Inside an engine, preamble predicts strongly, with an odds ratio of 7.72 [3.99, 14.94] on 1,137 observations holding engine and log response length fixed. The confirmatory test therefore runs a restated H6, in which the window delta is a function of how far into the response the first cohort mention falls and preamble is one of at least two things that push it there. Running a hypothesis descriptively and then confirming it on the same data would test nothing, so the restated form is fixed now and estimated only on observations collected after 2026-09-11.

Three rules govern the whole plan. Standard errors are cluster-robust on the query within each arm, because Table E1 puts the per-arm query design effect between 27.8 and 71.6 and the engine-by-query design effect on the panel at 63.3, and any claim generalising beyond the 192 prompts inherits that inflation. Multiplicity is handled by Benjamini-Hochberg within each declared family, with the families fixed here and not after inspection. Cells below 30 observations are reported descriptively and marked, and anything not listed in Table E11 is labelled exploratory and reported without an inferential claim.

---

## Reference keys used

Entries are copied from `research/R1-literature.md` as reproduced in the key list of `sections/A-front-intro-related.md`, which records the primary record against which each identifier was resolved on 2026-09-11 and applies the three corrections of `DECISIONS.md` §8. Keys match those used in blocks A, B and D for the same works.

[Bailey2016] Bailey, P., Moffat, A., Scholer, F., Thomas, P., 2016. UQV100: A Test Collection with Query Variability, in: Proceedings of SIGIR 2016, pp. 725–728. https://doi.org/10.1145/2911451.2914671

[Chen2024] Chen, L., Zaharia, M., Zou, J., 2024. How Is ChatGPT's Behavior Changing Over Time? Harvard Data Science Review 6 (2). https://doi.org/10.1162/99608f92.5317da47

[Greco2019] Greco, S., Ishizaka, A., Tasiou, M., Torrisi, G., 2019. On the Methodological Framework of Composite Indices: A Review of the Issues of Weighting, Aggregation and Robustness. Social Indicators Research 141 (1), 61–94. https://doi.org/10.1007/s11205-017-1832-9

[Huang2026] Huang, J., Situ, R., Ye, R., 2026. Cultural Encoding in Large Language Models: The Existence Gap in AI-Mediated Brand Discovery. arXiv:2601.00869.

[Mosnar2025] Mosnar, M., Skurla, A., Pecher, B., Tibensky, M., Jakubcik, J., Bindas, A., Sakalik, P., Srba, I., 2025. Revisiting Algorithmic Audits of TikTok: Poor Reproducibility and Short-Term Validity of Findings, in: Proceedings of the International ACM SIGIR Conference on Research and Development in Information Retrieval (SIGIR 2025). arXiv:2504.18140.

[Nardo2008] Nardo, M., Saisana, M., Saltelli, A., Tarantola, S., Hoffmann, A., Giovannini, E., 2008. Handbook on Constructing Composite Indicators: Methodology and User Guide. OECD Publishing, Paris. https://doi.org/10.1787/9789264043466-en

[Paruolo2013] Paruolo, P., Saisana, M., Saltelli, A., 2013. Ratings and Rankings: Voodoo or Science? Journal of the Royal Statistical Society Series A: Statistics in Society 176 (3), 609–634. https://doi.org/10.1111/j.1467-985X.2012.01059.x

[Saisana2005] Saisana, M., Saltelli, A., Tarantola, S., 2005. Uncertainty and Sensitivity Analysis Techniques as Tools for the Quality Assessment of Composite Indicators. Journal of the Royal Statistical Society Series A: Statistics in Society 168 (2), 307–323. https://doi.org/10.1111/j.1467-985X.2005.00350.x

[Saltelli2007] Saltelli, A., 2007. Composite Indicators between Analysis and Advocacy. Social Indicators Research 81 (1), 65–77. https://doi.org/10.1007/s11205-006-0024-9

[Zatuchin2026a] Żatuchin, D., 2026. The Dice Roll Method: A Standardized Protocol for Repeated-Query Auditing of Large Language Model Brand Recommendations. arXiv:2609.04047.

[Zatuchin2026c] Żatuchin, D., 2026. The Language Blind Spot: How Query Language and Brand Recognition Tier Shape AI-Constructed Brand Reputation Across Twelve European Languages. arXiv:2606.23165.

[Zatuchin2026d] Żatuchin, D., 2026. Who Owns the AI Recommendation? A Multi-Industry Empirical Map of Brand Category Ownership Across Large Language Models. arXiv:2606.23057.

---

## Open marks and number provenance

One item is flagged rather than resolved; three that the previous draft flagged are closed. The rule is that no figure enters the text without a source in `tables/NUMBERS.md`, `tables/TABLES.md` or a `stats/S*.md` file, and §10 was the passage that broke it.

1. **Closed: the index now has a source in this repository.** Every figure of §10.2, §10.3, Table E9 and Table E10 was produced by the reference implementation on a snapshot that closed on 2026-08-31 with 66,399 canonical observations, was reported under a caption naming the series that closes on 2026-09-08, and had no regeneration command in Appendix E. `stats/s6_index.py` now recomputes all of it on the declared cut, writes `stats/data/s6_components.csv`, `s6_spearman_subsets.csv`, `s6_aggregation_matrix.csv`, `s6_variance_decomposition.csv`, `s6_rank_displacement.csv`, `s6_panel.csv` and `s6_run.csv`, and appears in Table F14. The script reports 0 mismatches on the re-extraction identity over the 61,189 canonical rows whose stored text is itself inside the window, which is the same check `NUMBERS.md` V2 applies. Superseded values are named in the two captions and in the prose beside the values that replace them; nothing was changed in silence. The script also carries the panel rule as a declared parameter and publishes both readings, six arms over the series and the five the recency rule selects, because §10.1 concedes that the specification does not fix the panel.

2. **Closed: the multilevel model of S1, which now exists and is in the text.** An earlier state of this block recorded that `stats/S1-multilevel.md` was absent and that `stats/s1_results.json` had been removed during the rewrite of `s1_multilevel.py`, so §9.2 stated in one sentence what a mixed-effects model would add and rested on Table E2 alone. Both files were produced on 2026-09-11 by a run of 1,596.7 seconds over the read-only snapshot, and §9.2 now carries the model as its inferential result in Tables E12 and E13, §9.4 carries the paired language effect in Table E14, and §9.1 carries the tie between the standard-error inflation and the design effect. Table E2 stays where it was, recast as the convergent result. The caption of Table E6 still does not point at `s1_results.json`: its four five-arm rows are obtained by subtracting the Perplexity row from the panel rows of T7c, a stable source, and the subtraction is stated in the caption. Row 3 of Table F14 in block F, which declared that no table of this paper drew on `s1_multilevel.py`, is updated in the same pass.

3. **Closed: the 0.706 attribution.** The commissioning brief attributed that value to the geometric against weighted pair. Table 11 of `MANUSCRIPT.md` §8.3 placed it on the harmonic against weighted pair, and the recomputation on the declared cut puts that pair at 0.752. Table E10 carries the full matrix with both readings, and §10.3 states the minimum as the correlation between two defensible aggregations rather than naming a pair.

4. **Open: brief figures that the source files do not carry.** The commissioning brief named three figures that no table reproduces, and the documented values are used instead. Language marginals: the brief gave 22.9% English against 18.2% Portuguese; `tables/NUMBERS.md` T7a gives 20.22% [19.79, 20.64] on 34,310 English observations and 15.72% [15.34, 16.11] on 34,314 Portuguese ones under the uniform window, and those are the figures in §9.4. Query type: the brief gave 27.7% directive against 13.4% exploratory; T7b gives 25.93% on 34,319 and 10.00% on 34,305, used in §9.5. Category range: the brief gave 33.3% to 3.1%; the panel row of T7c runs 27.00% (comparativo) to 3.08% (experiencia), and the five-arm restriction runs 20.81% to 3.08%, both used in Table E6. If the brief's figures come from a cut this block did not see, the three sentences need re-sourcing before assembly.

5. **For the integrator.** The span 0.706 to 0.984 for the set of defensible aggregations appears in the abstract of block A, in block B and in row 20 of Table F1. Block F is updated here to 0.752 to 0.985; blocks A and B are outside the scope of this edit and carry the superseded span until someone updates them, which has to happen before assembly or the assembled manuscript contradicts itself.

---

## Anti-tic pass

Measured on the delivered file by `reviews/style_check.py` on 2026-09-11, against PART C of `research/R4-standards.md`. Every count below is the script's own output, not an estimate. Its prose scope excludes tables, captions, headings, code blocks, the reference list, this passage and the "Open marks" passage, and on that scope the block holds 6,228 words, 40,141 characters, 55 paragraphs and 217 sentences, against 4,491 words and 43 paragraphs before the multilevel model entered §9.1, §9.2 and §9.4. Where a check needs judgement the script supplies the candidates and the judgement is recorded here with its reason.

| Check | Result |
|---|---|
| C.1.1 Formulaic antithesis | Closed-formula count 0. Graduated count 1, the fixed-window verdict being a warning at the first occurrence and a failure at the second. The one occurrence is the close of §9.4, "is therefore not a courtesy to the reader; it is the condition under which the figure identifies a quantity", kept deliberately as the only structural antithesis in the block. Three earlier constructions were removed in a previous pass and have not returned: the script's regex, extended in the V5 audit to catch the variant with an intervening adverb, finds no other |
| C.1.2 Pseudo-profound closers | 0 from the closed list. Each subsection closes on a number, a requirement or a consequence: §9.6 on the count distribution and what a zero in Table E4 means, §9.7 on the reporting rule with the rank displacement attached, §10.3 on the superseded index figures, §11 on the three governing rules. The close of §9.7 was reordered in this pass, because it had ended on "Findings of this kind carry a shelf life" with the reporting rule two sentences earlier |
| C.1.3 Filler connective opening a paragraph | 0 from the C.1.3 list and 0 from the C.2 transition list, over all 55 paragraphs. Density of worn connectives 0.00 per 250 words. Three paragraph-initial transitions survive at low dose, "Part of the disagreement belongs to the instrument", "That pattern sets a reporting rule" and "That result bears directly on P3", each carrying information rather than glue |
| C.1.4 Preamble | 0 first sentences above the 45-word ceiling. Measured first sentences, in section order: 19, 26, 17, 33, 27, 26, 20, 12, 17, 13 and 14 words. The two that moved in this pass are §9.2, from 9 words to 26 because the opener now states which level dominates, and §9.4, from 17 to 33 because the opener now states the paired effect and its size. No opener announces the document |
| C.1.5 Self-narration | 0. The two occurrences the V5 audit found are gone: "This paper reports no confirmatory result" is now "Nothing below is confirmatory", and the sentence in §11 declaring that the paper does not present a repository commit as a registration was cut outright, since the two sentences after it make the argument |
| C.1.6 Verification meta-discourse | 0. No "we verified", "we checked" or "our analysis shows". Findings arrive with n, interval and source; identity checks, re-extraction and bootstrap construction stay in §4 and in the S-files, referenced by name and not narrated |
| C.1.7 Em dash in prose | 0. The file holds two em dashes in total, both null markers inside table cells, in Table E7 and in the response-level column of Table E13, which the rule tolerates. Five en dashes, all of them page ranges in the reference list. The minus signs in Tables E8, E12 and E14 are U+2212 and are counted separately |
| C.1.8 Vague attribution | 0. The one occurrence the V5 audit found, "It is described in the market as non-compensatory" in §10.1, now reads "The geometric mean is called non-compensatory". Every remaining appeal to prior work carries a key in the same sentence |
| C.1.9 Paragraph over 2,200 characters | 0 above 2,200 and 0 above the 1,500 warning. Longest prose paragraph is 1,386 characters, the count-distribution paragraph of §9.6, which grew in this pass by absorbing the decoy floor from the subsection that was dissolved |
| C.1.10 Repeated empty adjective | Total 2, verdict ok against a threshold of five occurrences or one root above two. Both hits are "robust" inside "cluster-robust", the standard-error term, in §9.2 and §11, and "crucial", "pivotal", "comprehensive", "seamless", "strategic" and "transformative" return zero. The estimator is named "two-way clustered" everywhere else in §9.2 and §9.4 to keep the root from crossing the threshold. "significant" appears nowhere in a non-statistical sense |
| C.1.11 Confidence label with no measurement | 0. Every limitation carries its number: the pre-confirmatory status carries 56 of 90 collected days, the interval caveat carries the design effect of 63.3 and the 1,056 clusters behind it, the tail caveat carries the 19 entities above xmin, the anchor caveat carries 32 of 32 anchors at head tier, and the index defect carries the 18.8% breadth share on the recomputed cut |
| C.1.12 Labelled alert | 0. The caveats are sentences of the argument with their conditions inside |
| C.1.13 Percentage without a denominator | 83 percentages in prose, each checked on the four axes of PART D, against 68 before the model entered. The fifteen new ones are variance shares and intraclass correlations, and each names the fit it comes from: 38,195 responses on 96 prompts and 52 days at the response level, 166,164 entity-rows from 5,988 sampled responses at the entity level, and 42,487 replicate-reduced cells for the grid decomposition it is set beside. Two frames repaired in the previous draft still hold: the within-arm type contrast of §9.5 names 7,679, 7,676, 3,873 and 3,868, and the 39.2% of Grok's first week in §9.7 names its 158 observations |
| C.1.14 Errata inside the text | 0. The one occurrence, "the v1.0 manuscript named 2026-09-28" in §11, was replaced by the dated forecast it refers to, with all four numbers and both dates preserved. Superseded index figures are named in §10 as superseded values of a stated cut, which is a data provenance statement and not a version history of the paper |
| C.2 Contrastive apposition "X, not Y" | 1 occurrence across 6,228 words, 0.16 per 1,000, against a warning at 3. The passages added in this pass carry none |
| C.2 Repeated paragraph opening | 0. No three consecutive paragraphs share their first three words and no pair does either, counted over all 55 paragraphs |
| C.2 Generic heading | Every subsection heading carries a claim. §9.2 was "Citation differs by engine more than by anything else", which the model contradicts at an intraclass correlation of 0.4559 for the prompt against 0.3492 for the engine, and the heading now names both levels and the day |
| C.2 Visual support density | Fifteen display items, fourteen tables and one figure, at 2,675 characters of prose per item against a warning above 5,000. Tables E12, E13 and E14 are the three added with the multilevel model |
| C.2 Adverbs in -ly | Maximum 3 in one paragraph, in §9.4, against a warning at 4 |
| C.6 Machine-drafted vocabulary | 0 hits across the forty entries. The script's single levy, "robust", is the technical term above |
| C.4.6 Closers carrying a figure | 76.4% of paragraphs close on a number, the highest in the manuscript, against 69.8% before this pass. The remaining 23.6% close on a requirement or a consequence |
| Diagnostic, reported and not fixed | Sentence length runs from 4 to 77 words, mean 28.7, standard deviation 13.7. Two sentences exceed 60 words as the script counts them and are retained: the reporting-rule sentence of §9.7 and the three-component definition of §10.1, which is a definition and reads as a list. Four runs of three consecutive paragraphs carry the same sentence count, against five before this pass, which the table-then-caveat structure of §9 produces and which the rule forbids turning into meta |
