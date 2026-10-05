## 13. Governance

Custody, licensing, versioning and scope are settled. Verification of a conformance claim is not: neither a conformance test suite nor an interlaboratory study exists, so Level 1 and Level 2 conformance is self-declared, and the design that would replace the declaration with evidence is specified here rather than deferred as future work.

**Custody.** Brasil GEO maintains the specification and the reference implementation, which means publishing every change, dating it, and keeping prior versions resolvable, so that a figure measured under one version stays checkable after the next exists. Implementing BRGEO-1 and stating conformance with it require no permission from the maintainer and confer no endorsement by it.

**Licensing.** The specification is published under CC BY 4.0 and the reference implementation under Apache-2.0, which carries an explicit patent grant, and Brasil GEO holds no patent or licensing claim over either, so an adopter who forks the cohort file, the battery generator and the extractor owes no royalty and asks no permission.

**Versioning.** A change that alters what a conforming figure means increments the major version; a clarification that leaves the meaning intact increments the minor, and every published figure cites the version under which it was measured. The requirement identifiers of §3.2 survive renumbering of the prose, so an erratum, an audit finding and a conformance claim name the same requirement across two versions.

**Scope.** BRGEO-1 covers the conditions under which a citation is observed and stops there. Repetition count and reliability thresholds belong to a complementary protocol that fixes iteration tiers and reports generalizability coefficients [Zatuchin2026a]. Aggregation is left free for the reason §10 measures. Two defensible aggregations of the same components rank the same entities at a rank correlation of 0.752 over 66 entities, and the set of defensible aggregations spans 0.752 to 0.985 on the cut this paper declares, against 0.706 to 0.984 on the cut of 2026-08-31 that the earlier figures came from (§10.3). Fixing a formula would therefore impose agreement on the part of the pipeline where disagreement is least resolvable, while the conditions of observation, where disagreement reaches tens of percentage points, are where a declaration buys something [Saisana2005, Paruolo2013]. Adjacent problems take their own numbers, which is what allows an adopter to conform on observation without adopting anything else.

**Independence.** One governance rule constrains the maintainer rather than the adopter. Level 3 attestation may be issued only by a body independent of both the claimant and the maintainer (§3.3), following the first-party to third-party progression of conformity assessment vocabulary [ISO17000], so the custodian cannot certify the measurements of its own clients. The constraint sits in the level scheme rather than in a promise, and the competing-interest declaration below points at it.

**What conformance does not yet establish.** Conformance at Level 1 and Level 2 is self-declared, which reproduces in miniature the unverifiable vendor claim of §1.1. Two artefacts would replace assertion with evidence and neither exists. The first is a conformance test suite: a fixed set of stored responses with expected figures under declared parameter values, against which any implementation can be run. For a quantity with no unit and no reference material it is the closest available analogue to a calibration standard, and §14 records the limit of that analogy. The second is an interlaboratory study in the sense of ISO 5725-2 [ISO5725], and its design is declared here rather than deferred as future work. The same stored responses are distributed to three or more implementations of P1 to P6 written independently of the reference code. Each implementation returns the citation rate per arm under one declared window and one declared matching rule. The discrepancy is then decomposed into a repeatability component, obtained by re-running each implementation on the same items, and a between-implementation component, obtained across implementations, with both reported in percentage points rather than as a pass or a failure. Two scales already in the uncertainty budget of §3.7 tell a reader what the result would mean: the largest Type A component of this series is 2.39 percentage points of typical error across 88 cells, and the window occupies a Type B entry of 22.95 to 55.73 percentage points across five arms. A between-implementation term of the first order supports the comparability claim. A term of the second order refutes it, and the protocol would then be specifying the wrong things.

The exercise has a material precondition that the reference instantiation does not meet. It needs shared items, and the only items this study can distribute are the 2,225 canonical observations retained whole, collected between 2026-09-06 and 2026-09-08, against the 68,624 collected under the protocol. The custodian cannot presently supply the item set for the exercise it proposes, which is a fact about the instrument rather than about the schedule, and §14 carries what follows from it.

---

## 14. Threats to validity

Every limitation below carries the measurement that bounds it, and three carry none: the elicitation-mode effect, the share of adversarial responses that fabricate rather than refuse, and the window effect on the retired open-weights arm. Naming those three is the point of the register, and the third is unmeasurable now because the text was never stored. The twenty-second row carries no measurement either, for a different reason the cell states: a documentary chain of provenance is not a quantity, so nothing about it is estimable.

**Table F1.** Register of threats to validity, with the measurement that dimensions each and what it leaves open. Series 2026-04-23 to 2026-09-08 except where a row names a shorter window; denominators are named per row.

| # | Threat | Measurement that dimensions it | What stays open |
|---:|---|---|---|
| 1 | Elicitation mode is a seventh parameter and is not declared | Not estimated. The one component of the same class that was measured, the observation window, moves the rate by 22.95 to 55.73 pp over 2,225 matched observations | Whether plain prompting and structured elicitation diverge at that order |
| 2 | Refusal taxonomy is proposed and not validated | 96.7% of 17,919 probe observations flagged by the legacy criterion; 66.8% of the 17,328 flagged rows carrying text hold an explicit refusal marker | The fabrication share inside the remaining 33.2%; no annotator agreement, gold standard, confusion matrix or category distribution exists [Wen2025, Kirichenko2025] |
| 3 | Probe coverage excludes the retrieval-augmented arm | 192 of 17,919 probe observations, 1.1% of the stratum; refusal-marker share 15.2% [10.5, 21.5] on 164 flagged rows | Whether an engine that searches converts the absence of any source into a refusal |
| 4 | Decoy verification is jurisdictionally narrow | 16 decoys verified against the Brazilian federal tax registry, mapping services and court records; 0 spontaneous namings in 68,624 canonical observations, Wilson upper bound 0.0056% | Per-decoy reporting on the probe stratum, which is what separates fabrication from a foreign homonym |
| 5 | Reference implementation diverged from the specification | Panel eligibility was set in code at a minimum of 500 observations until 2026-08-31; measured on the cut of that date it excluded a live arm holding 96 observations in fintech and retained an arm retired on 2026-08-16 holding 3,552. Commit `51159fd` replaced the count by a 14-day recency rule | Every index figure published before 2026-09-11, which §10 recomputes on the declared cut under both rules |
| 6 | Dependence sits at the prompt, not at the day | Design effect 63.3 clustering by query, effective n 1,083 against a nominal 68,624; pooled half-width 0.29 pp naive against 2.29 pp prompt-clustered | Any binomial interval over the observation count is too narrow by a factor near eight for a claim beyond the battery |
| 7 | Calendar coverage | 52 collected days over a 139-day span, 37.4%, under the local-date rule, and 53 under the UTC rule of Appendix D; largest hole 59 contiguous days from 2026-06-10 to 2026-08-07; July empty, 0 days of 31 | 15 of 21 declared event-by-arm pairs untestable because a hole sits on the boundary |
| 8 | Output censoring at the far end of the response | Gemini full responses end mid-word at means of 3,540 and 3,684 characters on 2026-09-07 and 2026-09-08; Grok on 9.1% of the 768 Grok responses retained whole | Whole-response rates are floors: Gemini's 65.10% on the 384 observations of the restricted subset is a lower bound |
| 9 | Irreversible loss on one arm | Groq left the panel on 2026-08-16; retention was deployed on 2026-08-31 and the first retained rows are of 2026-09-06, so the arm holds 0 rows with stored full text against 14,208 canonical observations | The window effect on that arm, unmeasurable by any later work |
| 10 | Lexical collision inside the cohort | 353 of 68,624 observations, 0.51%, all in English, distributed Groq 173, ChatGPT 158, Gemini 22; panel rate 17.97% against 17.45%, HHI 0.1917 against 0.2023 | Correction requires re-extraction of the series, not an erratum |
| 11 | The panel never held six engines at once | Groq's last day, 2026-08-16, precedes Grok's first, 2026-08-23; zero complete six-way cells; the widest panels are five arms on the 96-query half-battery, 4,231 and 278 cells | Six-rater Fleiss is undefined for this series |
| 12 | Within-engine instability sets a ceiling | Same-day test-retest kappa 0.669 on Perplexity over 2,687 replicate cells and 0.725 on Grok over 288 | Between-engine kappa on those arms is read against those ceilings, and the two components are not decomposed |
| 13 | Unequal sampling by provider routing | One arm runs 96 of the 192 canonical queries; three of the six semantic categories hold n = 0 in it | Per-cell power on that arm, reported and not corrected by weighting |
| 14 | Missingness is not ignorable | 49 runs between 2026-08-16 and 2026-09-08 with 3 successes and 28 preflight bars on balance or model; gaps cluster on credit exhaustion, which correlates with cost, which correlates with response length, which correlates with citation | Coverage weighting addresses data missing at random; bounds analysis has not been performed |
| 15 | No human-annotated ground truth | Every outcome passes one automated rule over a fixed cohort of 127 names; `src/analysis/kappa_validator.py` exists and has not been run on this series | Whether the binary outcome matches what a reader would call a citation |
| 16 | The preamble criterion was never committed | The re-specified pattern diverges by up to 5.2 pp per arm from the shares computed under the criterion as first described in prose; Gemini reads 36.46% on the 768 observations of the three-day cohort against 80.03% on the 15,355 canonical observations of the full series under one pattern | Every preamble figure inherits that uncertainty |
| 17 | Market, language and model tier | 79 Brazilian firms and 32 international anchors; the panel rate is 15.72% on 34,314 Portuguese observations and 20.22% on 34,310 English ones; all six arms are small, low-cost models | Whether flagship models behave the same way |
| 18 | Model version and generation configuration move under a stable name | One boundary changed model identifier and reasoning budget in the same commit; the default reasoning budget of one replacement arm cost five consecutive collections and 129 of 179 minutes of one run before a declared change of reasoning effort fixed it | Drift is bounded by stratification and is not estimated [Chen2024] |
| 19 | The window value itself is a choice | 200 characters recovers 35.4% of first mentions across the panel, from 7.8% on Gemini to 70.2% on Perplexity, over 1,367 observations that name an entity | Head-of-response citation is defensible and is not the only defensible aperture; headline figures are reported under both |
| 20 | Aggregation instability | Rank correlations between defensible aggregations of the same components span 0.752 to 0.985 on the declared cut, the lower bound measured over 66 entities; the same span on the cut of 2026-08-31 was 0.706 to 0.984 | Whether the composite separates in a less concentrated market |
| 21 | Nothing here is causal | Cohort fixed, battery fixed, no intervention performed across 68,624 observations | Whether a firm can act on its rate, and whether naming tracks standing |
| 22 | The metrological analogy has no unit and no hierarchy | Not a quantity, so not estimable: metrological traceability requires a documented unbroken chain of calibrations [VIM2012], and no such chain, reference material or national reference exists for a citation rate | The measurand is constituted by convention [Jacobs2021, Borsboom2004] |
| 23 | The battery's own design factors account for none of the variance between prompts | The prompt carries 45.59% of the latent variance over 38,195 responses on 96 prompts and 52 collection days; adding vertical, language, query type and semantic category to the same crossed random structure moves the between-prompt variance from 4.005 to 4.036, under 1% (§9.2) | Whether a second battery balanced on the same four factors reproduces this one's rate. P3 publishes the invariants that make a battery checkable and does not make two balanced batteries interchangeable |
| 24 | Repeated runs return byte-identical text and the series cannot say why | 47.84% of the 22,495 engine-by-prompt-by-day cells holding more than one run are byte-identical across runs, 71.88% on the retired open-weights arm against 0.04% on the retrieval-augmented one, and the 68,624 canonical rows carry 14,391 distinct response hashes; the configured cache lifetime is 20 hours against rounds twelve hours apart (§4.7) | A cache hit against near-deterministic decoding of a short prefix. No column of `citations` records whether a row was served from cache, so the two cannot be separated in this series |
| 25 | An analysis module stores a standard deviation under a key named for a variance | `src/analysis/mixed_effects.py` writes `exp(vcp)` into `random_variances` while `statsmodels` parameterises the component as `log σ`, so the stored quantity is σ where the key promises σ². Zero figures in this paper read that key | H1 of Table E11 names the same module as committed analysis code for the confirmatory window |

Nine of those rows carry an argument the table cannot hold.

**Elicitation mode is the largest unmeasured quantity in the study.** The battery sends plain natural-language prompts and entities are extracted afterwards, which is closer to what a user reads than instructing a model to return a structured list of company names. No pilot has compared the two. The reason this sits at the top of the open items is the size of the one comparable quantity that was measured: a single undeclared difference in how much of the answer was read moved five arms by 22.95 to 55.73 percentage points on 2,225 matched observations. A protocol that fixes six parameters while a seventh of unknown magnitude varies freely has not finished the job, and the honest form of the claim in §3 is that BRGEO-1 declares the conditions it has identified.

**The interval this paper publishes depends on which claim it is making.** Table E1 puts the engine-by-prompt design effect on the panel at 63.3 and the day-clustered inflation of the pooled standard error at 1.32, with three of five arms showing no day-level inflation at all, because every round re-asks the same fixed battery and a day is close to a census of the prompt population. Any statement in this paper that generalises beyond these 192 prompts carries the second interval, and any statement about these 192 prompts carries the first. The distinction is the reason §9 reports strata descriptively and the reason a published rate whose interval came from the observation count is reporting a quantity below the floor that definitional uncertainty already sets [VIM2012].

**The calendar removes the events that matter most.** The coverage of row 7 of Table F1 would be a power problem on its own; the shape of the hole makes it a design problem, since 15 of 21 declared event-by-arm pairs cannot be confronted with blind change-point detection because a hole sits on the boundary. The events and the outages have common causes, since the late-August gap exists because the fifth arm consumed 129 of 179 minutes of a run under its provider's default reasoning budget and the fix for that consumption is itself a declared configuration event, which is why §3 requires the boundary to be declared in advance and stratified by rule.

**Censoring runs in both directions and both make the reported figures conservative.** The 200-character window censors the head of the answer, which §6 measures. The provider's own output cap censors the tail: Gemini's stored responses on 2026-09-07 and 2026-09-08 end mid-word at means of 3,540 and 3,684 characters, and Grok's do so on 9.1% of the 768 Grok responses retained whole. A response that was cut before the model finished can only lose citations, so every whole-response rate in this paper is a floor rather than an estimate, and Gemini's 65.10% over the 384 observations of the restricted subset is a lower bound with an unknown distance to the true value. The retired open-weights arm is the case with no floor at all, because its 14,208 canonical observations hold no text beyond character 200 and regeneration is not a substitute: hosted models do not reproduce their outputs exactly at temperature zero [Atil2025, Coqueret2026].

**Two of the paper's agreement statements are read against ceilings rather than against unity.** Rows 11 and 12 of Table F1 carry the two facts: the six-engine panel the design describes never existed, and the two affected arms disagree with themselves twelve hours apart. Part of what this paper counts as disagreement between engines on those arms is that self-disagreement, and no decomposition separates the two components. The Fleiss figures of §9 are therefore lower bounds on the agreement a stable instrument would report, in the same direction as the window correction and for a different reason.

**The battery's design factors do not characterise the battery.** The multilevel model of §9.2 puts 45.59% of the latent variance between the 96 prompts, then finds that the four factors the battery was balanced on account for none of that share: with no covariates the between-prompt variance is 4.005 on the logit scale, and with vertical, language, query type and semantic category all present it is 4.036. P3 requires the full battery and its factorial invariants to be published, which is what makes an instrument checkable by a second party. Row 23 records what the requirement does not deliver, which is comparability between two batteries balanced the same way, since balance on those four axes carries no information about which prompts elicit names. An adopter setting a figure beside this paper's is comparing prompt samples before comparing engines, and the width that claim has to carry is the query-clustered interval of §9.1: 46.35% to 61.21% around a measured 53.78% on the arm with the highest rate.

**Repeated runs return the same bytes often enough to matter, and the series cannot say why.** Of the 22,495 engine-by-prompt-by-day cells holding more than one run, 47.84% are byte-identical across runs, and the 68,624 canonical rows carry 14,391 distinct response hashes. The distribution across arms is the part that discriminates: 71.88% on the retired open-weights arm and 0.04% on the retrieval-augmented one, with ChatGPT at 58.25% and Claude at 60.60%. Two explanations survive the measurement. A cached answer served inside the configured 20-hour lifetime against rounds twelve hours apart is possible by construction (§4.7), and near-deterministic decoding of a short prefix at temperature zero would produce the same repetition with no cache involved. The pattern across arms favours the second reading, because the arm that searches the web almost never repeats itself while the parametric arms repeat constantly, which is the ordering a deterministic decode predicts and one a cache keyed on the query text has no reason to produce. The series cannot decide between the two, because no column of `citations` carries a cache flag and the information was never written.

That open question has a requirement attached to it and a passage of §3.1 on the other side of the same axis. An implementation that intends to measure run-to-run variation records, per observation, whether the response came from cache, and that record belongs in the declared generation configuration of P5 beside temperature, seed and output caps, because without it the run-to-run term of an uncertainty budget cannot be told apart from a replay of the previous round. P5 already concedes the converse half: it pins the request and not the response, since hosted models do not reproduce their outputs exactly at temperature zero [Atil2025, Coqueret2026]. One passage says repetition cannot be assumed; row 24 says repetition arrived anyway, on four arms of six, between 28.37% and 71.88% of their multi-run cells. Neither is evidence about the other until a cache flag separates them, and the coefficient-level cost of leaving it open is bounded: collapsing every byte-identical repeat and refitting the model of §9.2 over the surviving 31,975 responses takes the retrieval arm's odds ratio from 6.794 to 6.508 and Gemini's from 0.089 to 0.078, well inside the interval of either fit.

**One analysis module in the repository names a standard deviation a variance.** `src/analysis/mixed_effects.py` stores `exp(vcp)` under the key `random_variances`, and `statsmodels` parameterises each random component as `log σ`, so the value behind that key is σ where the name promises σ². Nothing in this paper reads it, because the S1 script performs its own conversion and publishes σ and σ² side by side, and `random_variances` is read by no other module in the repository. The reason it belongs in this register rather than in a changelog is Table E11: H1 of the confirmatory plan names that module as the committed code for the mixed-effects test, so the mislabelled key sits one run away from a published variance component that would be out by a square root.

**The metrological vocabulary is borrowed for its discipline and not for its guarantees.** A citation rate has no SI unit, no calibration hierarchy and no national institute holding a reference copy, so the chain that BRGEO-1 offers is documentary: a published figure resolves to a specification version, which resolves to six declared parameter values, which resolve to published artefacts and to stored responses a third party can re-extract. Metrological traceability in the strict sense requires a documented unbroken chain of calibrations, each of which contributes to the measurement uncertainty [VIM2012], and that chain does not exist here. The measurand is constituted by convention rather than discovered, which is the standing position for unobservable constructs [Jacobs2021, Borsboom2004], and what a documentary chain buys is set out in §1.2: a convention written down is one a second party can dispute clause by clause, which is a weaker property than correctness and the only one available here.

---

## 15. Discussion

Five results in this paper are measurements and five of its propositions are designs, and a reader who mixes the two will overreach in one direction or dismiss the work in the other. Table F2 sets each measurement beside the proposition it does not support.

**Table F2.** What the evidence establishes and what the paper proposes without evidence. Series 2026-04-23 to 2026-09-08, 68,624 canonical observations, except the window rows, which cover 2026-09-06 to 2026-09-08 and 2,225 matched observations, and the multilevel row, which covers the 38,195 responses of the core-3 balanced design.

| Established, with its measurement | Proposed, with what would test it |
|---|---|
| Reading the whole response instead of the first 200 characters raises the rate on every arm that retained text, by 22.95 to 55.73 pp, with 0 reversals in 2,225 matched observations and exact McNemar p from 1.69e-21 to 2.89e-129 | That declaring the six parameters produces comparability between independent measurements. Tested by the interlaboratory study of §13, not yet run |
| Three engines running the full 192-query battery agree at Fleiss 0.086 on whether a citation happened, over 9,129 complete cells on 50 collection days; mean pairwise Cohen's kappa is 0.219 over 14 defined pairs | The three-way refusal taxonomy of §7.2. Tested by a human-labelled sample with annotator agreement and a confusion matrix, not yet built |
| The firm-by-engine interaction carries 39.33% of the variance in logit coverage, against 34.46% for the firm and 26.21% for the engine, over 62 entities by 6 engines | That the window delta is driven by how far into the response the first mention falls. Tested by manipulating response style and observing the delta move, not attempted |
| The matching rule names no fictitious entity spontaneously: 0 in 68,624 canonical observations, Wilson upper bound 0.0056% | That conformance levels on an attestation axis are the right axis. Tested by adoption, which has not happened |
| Which prompt was asked carries more of the latent variance than which engine answered it, at intraclass correlations of 0.4559 against 0.3492 over 38,195 responses on 96 prompts and 52 collection days, with the collection day at 0.0003 | That a battery published with its factorial invariants is a characterised battery. Tested by fitting the same model on a second battery balanced on the same four factors, which does not exist; those four factors move the between-prompt variance from 4.005 to 4.036 |

The defect this paper reports about itself was invisible to every control the pipeline ran, and §5.3 lists the controls that were green on the day the asymmetry was found. What no assertion asked was whether the string being read was the model's answer. Audits of commercial systems fail to reproduce for the same species of reason, traced to conditions the original studies had not fixed [Mosnar2025], and validity has to be argued rather than inherited from a passing suite [Salaudeen2025, Bean2025]. The transferable part is cheap: a variable whose maximum equals its minimum across 15,168 observations reports a boundary rather than a measurement, and that query costs seconds.

The window turned out to be the dominant parameter across the whole panel rather than a quirk of retrieval. Four parametric arms move by at least 30.73 percentage points and the single retrieval-augmented arm moves least, at 22.95, which inverts the architectural expectation that retrieval-augmented composition would suffer most, and §6.6 reports the test that rejects it. It also reverses a published reading: the 1.86% attributed to Gemini over 15,355 observations is a property of the aperture, since on the 768 observations that retained a whole response the same window gives 2.60% while the whole response gives 33.3%, rising to 65.10% over the 384 observations from the two of three days on which that arm returned full-length answers rather than answers capped at 216 characters. The gap between the two figures is definitional uncertainty in the sense of VIM 2.27 [VIM2012], so no sample size closes it and no better extractor reduces it. A vendor who reports a confidence interval derived from the observation count is reporting a term below the floor, and the dominant term never entered the budget.

Agreement between engines is partly an artefact of the instrument that measures it. On identical cells on 2026-09-08 across the four fully truncated arms, Fleiss on the binary outcome rises from 0.2371 at 200 characters to 0.4881 on the whole response over 192 cells, and the Claude to Gemini pair moves from 0.126 to 0.633. Doubling is the size of the correction on those cells, and the direction matters more than the magnitude: part of what reads as models disagreeing about a firm is one aperture applied to answers of very different lengths. The correction does not extend to every pair, since the four pairs containing the retrieval arm move the other way as prevalence approaches the ceiling where kappa loses discriminating power, so the harmonised figure is not uniformly higher and should not be presented as if it were.

Citation is a property of the firm-engine pair, and §9.2 puts the interaction above either main effect on the entity-by-engine grid, while the multilevel model on the same series puts the prompt above the engine on the response, at intraclass correlations of 0.4559 against 0.3492 over 38,195 responses. A measurement bought from one engine therefore estimates a quantity that does not transfer, and the effect is visible at the level of individual firms: of the twenty entities named by exactly one engine in five months, seventeen are named only by the retrieval-augmented arm, and they are the mid-cap and long-tail names. A firm in that position does not have a low rate on the other engines. It has no rate there, and a dashboard that pools the panel into one number will report the two cases identically. The query side behaves the same way: asked in Portuguese rather than English, five arms name fewer Brazilian entities and the retrieval arm names more, a within-pair spread of 17.03 points between the two extremes over 21,862 matched pairs (§9.4).

For anyone buying measurement, the consequences are specific and none of them requires adopting this protocol. A rate arrives with the window that produced it and the recall target that window meets, because 200 characters recovers 35.4% of first mentions across the panel, and between 7.8% and 70.2% by arm, over the 1,367 observations that name an entity (row 19 of Table F1). It arrives per engine, because the same cohort on the same days gives 1.91% over 9,455 replicate-reduced cells on one arm and 53.09% over 4,737 on another (`stats/S3-agreement.md`, Table S3.1c), and the two arms do not even answer the same battery: one receives all 192 queries and the other 96, as §9.5 and Appendix B record. The effective sample travels with it rather than the observation count, because the 68,624 observations of 192 prompts carry the statistical weight of 1,083 (Table E1). It arrives with the matching rule and its ablation, because removing the alias table alone moves the panel by 0.94 percentage points and one arm by 5.25 over the 2,225 observations of the ablation in §3.1. And it arrives with a note on what survives a change of vendor, which is the ranking inside a vertical rather than the level, at a median Kendall tau-b between engines of 0.52 in fintech and 0.58 in retail against 0.27 in health and 0.18 in technology, so even that property holds in two of the four markets measured (`stats/S3-agreement.md`, Table S3.3c).

One control in that list costs almost nothing. The decoy construction of §7.1 puts sixteen fictitious firms inside the same battery, on the same days, through the same adapters as the 111 real entities, and across 68,624 canonical observations no engine named one of them spontaneously at either window, which puts a 95% upper bound of 0.0056% on the rate at which the matching rule manufactures a cohort name out of ordinary prose. The floor is estimated from the run that produced the rate rather than from a separate calibration an adopter would have to trust transfers, and the bound is honest about where it is loose: the newest arm's 1,118 observations admit an upper bound of 0.342%, sixty times the panel figure. What the floor does not bound is a model's willingness to describe an invented firm when the name is handed to it, which is a different instrument and a different number.

What changes in reporting practice is the shape of the published object. A headline figure becomes a figure plus six declared values, an uncertainty budget that separates components estimated from repetition from components estimated from knowledge of the instrument, and a missingness ledger stating what was not collected. The cost of publishing that object is a page. The cost of not publishing it is the situation this paper documents inside its own instrument for four months, in which two figures that differ by tens of percentage points are both correct and no reader can tell why.

---

## 16. Conclusion

BRGEO-1 fixes six parameters, three conformance levels on an axis of attestation, a missingness ledger and an uncertainty budget, and states each requirement with a stable identifier and a failure mode. The parameters are the observation window, the cohort, the query battery, the engine panel with pinned model versions, the generation configuration and the entity matching rule. They are the description of the state of the phenomenon that the vocabulary of metrology requires before a quantity can be called a measurand [VIM2012], and a rate published without them names no measurand a second party can reproduce.

The empirical contribution is a five-month record of what happens when one of the six moves without being declared. On 2,225 observations matched within the response, reading to the end instead of stopping at character 200 raises the citation rate by 22.95 to 55.73 percentage points across five engines, with no observation losing its citation in any arm. The effect is not predictable from architectural class, the four parametric arms spanning the full range while the single retrieval-augmented arm moves least. It reverses one published reading, since an engine reported at 1.86% over 15,355 observations cites at 33.3% on the 768 of those observations whose whole response was retained. Beside that number sit the conditions under which it was produced: 37.4% calendar coverage over 139 days, a design effect of 63.3 at the prompt that cuts the effective sample to 1,083, a false-positive floor of zero spontaneous fictitious namings in 68,624 observations with a Wilson upper bound of 0.0056%, and a firm-by-engine interaction carrying 39.33% of the variance in coverage.

The specification's principal gap is that conformance remains self-declared. Two artefacts would close it and neither exists: a conformance test suite of reference responses with expected figures under declared parameters, and an interlaboratory study in the sense of ISO 5725-2 in which independent implementations process the same stored responses and the discrepancy is decomposed into repeatability and between-implementation components [ISO5725]. Until the second runs, the central proposition of this paper, that declaring the six parameters produces comparability, is a design argument with no measured evidence in its favour.

The gap has a precondition that this instrument does not yet meet. An interlaboratory exercise needs shared items, and full-response retention was deployed on 2026-08-31 with the first retained rows falling on 2026-09-06, which leaves the 2,225 canonical observations of 2026-09-06 to 2026-09-08 available to distribute against 68,624 collected. The confirmatory window is defined in collected days rather than calendar days and stood at 56 of 90 on 2026-09-11, with a projected close on 2026-10-15. Retention from the first observation is therefore the requirement an adopter should implement before any other, because it is the only one in the specification that cannot be satisfied retroactively [Jiang2026]. Everything else in this record was repaired after it was found. The four months of responses that were never stored were not.

---

## CRediT authorship contribution statement

**Alexandre Caramaschi:** Conceptualization, Methodology, Software, Formal analysis, Investigation, Data curation, Writing – original draft, Writing – review and editing, Visualization, Project administration.

The taxonomy is applied to a single-author paper by listing the roles that the author performed, not all fourteen. No role in the taxonomy was performed by a party not named here.

## Declaration of competing interest

The author takes a deliberately expansive view of competing interests, and declares the following.

Alexandre Caramaschi is the founder of Brasil GEO, the organisation that is the custodian and maintainer of the BRGEO-1 specification described in this paper. Brasil GEO provides commercial advisory and audit services in the domain that the specification measures, and would benefit from the adoption of BRGEO-1. He is also Chief Strategy Officer of Nuvini (Nasdaq: NVNI); this work is conducted in his capacity at Brasil GEO and does not represent a position of Nuvini.

Brasil GEO holds no patent or licensing claim over the specification, which is released under CC BY 4.0 with a reference implementation under Apache-2.0 and is free to implement by any party without royalty. Use of the BRGEO-1 identifier to describe a conforming measurement requires no permission from the maintainer and confers no endorsement by it.

Four features constrain this interest structurally rather than by declaration alone. Level 3 attestation (§3.3) may be issued only by a body independent of both the claimant and the maintainer, so the custodian cannot certify its own clients. The reference implementation, the cohort file and the query battery are published under an open licence, so no party controls the instrument. The cohort was fixed before collection began and contains no entity selected for a commercial relationship, and its composition is enumerated in Appendix A. And §5, §8 and §14 report defects in the custodian's own instrument, including a reference implementation that did not implement the specification at the panel threshold, which is the class of finding a custodian with an undeclared interest would suppress.

No external party had any role in the design of the specification, the selection of the cohort, the analysis of results, or the decision to submit this article.

## Declaration of generative AI and AI-assisted technologies in the manuscript preparation process

During the preparation of this work the author used Anthropic Claude to draft and revise prose and to write analysis scripts, and Perplexity (sonar-pro) to search bibliographic records and check them against publisher registries. After using these tools the author reviewed and edited the content as needed and takes full responsibility for the content of the published article.

Two boundaries of this declaration are stated so that a reader does not have to infer them. Model calls to ChatGPT, Claude, Gemini, Groq, Perplexity and Grok are the instrument of this study rather than assistance with manuscript preparation. They are described as a research method in §4.3 and §4.4 with pinned model identifiers, generation configuration and dated version boundaries, and this declaration does not cover them. No figure, table or image in this manuscript was generated or altered by a generative tool: every figure is produced by the scripts of Appendix E from the CSV files those scripts write, and every table is interpolated from a query result by `build_tables.py` rather than typed.

## Funding

This research did not receive any specific grant from funding agencies in the public, commercial, or not-for-profit sectors. Application programming interface costs for collection were borne by the author, and the cost envelope, including the share of spend attributable to reasoning tokens on one pinned model, is reported in §4.7. No sponsor had any role in the study design, in the collection, analysis and interpretation of data, in the writing of the report, or in the decision to submit the article for publication.

## Ethics

The study queries commercial application programming interfaces under their published terms of service, involves no human subjects, and collects no personal data. The 127 entities of the cohort denote organisations, and the entity matching rule matches only those 127 names, so no personal datum enters any figure in this paper even where a stored response names an individual. The 16 fictitious entities used in the adversarial stratum were verified as non-existent against the Brazilian federal tax registry, mapping services and court records before collection began, so no probe attributes invented products or history to a firm that exists; Appendix A lists them. Raw engine responses are retained locally under the providers' terms, which do not permit redistribution, and the Data availability statement records what is published in their place.

## Data availability

The specification, the reference implementation, the cohort definition, the query battery, the entity matching rule with its dictionaries, the collection pipeline, the missingness ledger and every analysis script are openly available at `github.com/alexandrebrt14-sys/papers`. Appendix E lists the command that regenerates each table and each figure in this paper.

The data cut is declared. Every figure in this paper is computed on a single local snapshot of `data/papers.db` whose earliest `citations.timestamp` is 2026-04-23T22:23:00Z and whose latest is 2026-09-08T19:30:57Z, holding 86,543 rows of which 68,624 are canonical and 17,919 are adversarial probes. Collection continued after that date and the published dashboard recorded 56 collected days on 2026-09-11; nothing after 2026-09-08 enters any table here. A versioned dataset snapshot carrying a persistent identifier is deposited at the close of the confirmatory window, cited with the `[dataset]` marker and by version identifier rather than by concept identifier, so that the figures in this paper remain recomputable from the exact artefacts that produced them.

Two limits on the data are part of the statement rather than footnotes to it. Raw engine responses are withheld because the providers' terms do not permit redistribution; the battery, the cohort, the code and the derived tables are not covered by that restriction and are published. And the whole response was not retained before 2026-08-31, so 66,399 of the 68,624 canonical observations cannot be re-extracted by any party at any other window, which is the reason this instantiation claims Level 1 rather than Level 2 (§12.1).

## Acknowledgements

The author thanks the reviewers of the internal audit that identified the observation-window asymmetry reported in §5 and §6 and the aggregation defect reported in §10, and the external adversarial review of 31 August 2026, which withdrew two published figures and established that the reference implementation did not implement the specification at the panel-membership threshold recorded in §14.

---

## Appendix A. Cohort by vertical, tier and status

The cohort is fixed in `src/config_v2.py` and was dated before the first observation of the series on 2026-04-23. The tables below are the authoritative enumeration and are generated from that file; where a count in the body of the paper differs, this appendix is the record. Tier is assigned at cohort construction and is not derived from any measurement in this study. Legal status is annotated so that a model naming a firm in judicial recovery is not pooled with one naming an active firm.

**Table F3.** Cohort composition by vertical, class and tier. Fixed 2026-04-23, 127 entities; denominator for the tier columns is the Brazilian firms of that vertical.

| Vertical | Brazilian firms | Head | Torso | Long tail | Anchors | Decoys | Total |
|---|---:|---:|---:|---:|---:|---:|---:|
| Fintech | 19 | 10 | 4 | 5 | 8 | 4 | 31 |
| Retail | 20 | 8 | 6 | 6 | 8 | 4 | 32 |
| Health | 20 | 9 | 6 | 5 | 8 | 4 | 32 |
| Technology | 20 | 7 | 6 | 7 | 8 | 4 | 32 |
| **Cohort** | **79** | **34** | **22** | **23** | **32** | **16** | **127** |

Of the 79 Brazilian firms, 78 are annotated active and one is in judicial recovery. Founding years run from 1895 to 2019, with 21 of the 79 founded in 2010 or later. That stratum was designed to probe the awareness gap of models whose pre-training predates the firm, and on this cohort it cannot: the most recently founded member dates from 2019 and every pinned engine version has a later cutoff, so the indicator has no cases and was not fitted (§9.6). Nine federative units are represented: São Paulo 59, Rio de Janeiro 6, Minas Gerais 3, Santa Catarina 3, Paraná 2, Rio Grande do Sul 2, Ceará 2, Espírito Santo 1 and Rio Grande do Norte 1.

**Table F4.** The 79 Brazilian firms with tier, legal status, founding year and federative unit. Source `src/config_v2.py`, fixed 2026-04-23.

| Vertical | Entity | Tier | Legal status | Founded | Unit |
|---|---|---|---|---:|---|
| Fintech | Nubank | Head | Active | 2013 | SP |
| Fintech | PagBank | Head | Active | 2006 | SP |
| Fintech | Cielo | Head | Active | 1995 | SP |
| Fintech | Stone Co | Head | Active | 2012 | SP |
| Fintech | Banco Inter | Head | Active | 1994 | MG |
| Fintech | Mercado Pago | Head | Active | 2004 | SP |
| Fintech | Itaú | Head | Active | 1945 | SP |
| Fintech | Bradesco | Head | Active | 1943 | SP |
| Fintech | C6 Bank | Torso | Active | 2018 | SP |
| Fintech | PicPay | Torso | Active | 2012 | ES |
| Fintech | Banco Neon | Torso | Active | 2016 | SP |
| Fintech | Banco Safra | Torso | Active | 1955 | SP |
| Fintech | BTG Pactual | Head | Active | 1983 | SP |
| Fintech | XP Investimentos | Head | Active | 2001 | RJ |
| Fintech | Dock | Long tail | Active | 2014 | SP |
| Fintech | CloudWalk | Long tail | Active | 2013 | SP |
| Fintech | Will Bank | Long tail | Active | 2017 | SP |
| Fintech | Swap | Long tail | Active | 2019 | SP |
| Fintech | Agibank | Long tail | Active | 1999 | RS |
| Retail | Magazine Luiza | Head | Active | 1957 | SP |
| Retail | Casas Bahia | Head | Active | 1952 | SP |
| Retail | Americanas | Head | Judicial recovery | 1929 | RJ |
| Retail | Amazon Brasil | Head | Active | 2012 | SP |
| Retail | Mercado Livre | Head | Active | 1999 | SP |
| Retail | Shopee Brasil | Head | Active | 2019 | SP |
| Retail | Renner | Head | Active | 1912 | RS |
| Retail | Riachuelo | Torso | Active | 1947 | RN |
| Retail | C&A Brasil | Torso | Active | 1976 | SP |
| Retail | Leroy Merlin Brasil | Torso | Active | 1998 | SP |
| Retail | Centauro | Torso | Active | 1981 | SP |
| Retail | Netshoes | Torso | Active | 2000 | SP |
| Retail | Grupo Pão de Açúcar | Head | Active | 1948 | SP |
| Retail | Petz | Long tail | Active | 2002 | SP |
| Retail | Dafiti | Long tail | Active | 2011 | SP |
| Retail | Madeira Madeira | Long tail | Active | 2008 | PR |
| Retail | M Dias Branco | Long tail | Active | 1953 | CE |
| Retail | Grupo Boticário | Torso | Active | 1977 | PR |
| Retail | Netfarma | Long tail | Active | 1999 | SP |
| Retail | Mobly | Long tail | Active | 2011 | SP |
| Health | Dasa | Head | Active | 1961 | SP |
| Health | Hapvida | Head | Active | 1993 | CE |
| Health | Unimed | Head | Active | 1967 | SP |
| Health | Fleury | Head | Active | 1926 | SP |
| Health | Rede D'Or | Head | Active | 1977 | RJ |
| Health | Hospital Einstein | Head | Active | 1955 | SP |
| Health | Sírio-Libanês | Head | Active | 1921 | SP |
| Health | Raia Drogasil | Head | Active | 2011 | SP |
| Health | Eurofarma | Torso | Active | 1972 | SP |
| Health | Aché Laboratórios | Torso | Active | 1966 | SP |
| Health | EMS Pharma | Torso | Active | 1964 | SP |
| Health | Hypera Pharma | Torso | Active | 2001 | SP |
| Health | NotreDame Intermédica | Head | Active | 1968 | SP |
| Health | SulAmérica Saúde | Torso | Active | 1895 | RJ |
| Health | Amil | Torso | Active | 1978 | RJ |
| Health | Prevent Senior | Long tail | Active | 1997 | SP |
| Health | Porto Saúde | Long tail | Active | 1988 | SP |
| Health | Alliar | Long tail | Active | 2011 | SP |
| Health | Oncoclínicas | Long tail | Active | 2010 | SP |
| Health | Hermes Pardini | Long tail | Active | 1959 | MG |
| Technology | Totvs | Head | Active | 1969 | SP |
| Technology | Stefanini | Head | Active | 1987 | SP |
| Technology | Tivit | Torso | Active | 1998 | SP |
| Technology | CI&T | Head | Active | 1995 | SP |
| Technology | Locaweb | Torso | Active | 1998 | SP |
| Technology | Movile | Torso | Active | 1998 | SP |
| Technology | iFood | Head | Active | 2011 | SP |
| Technology | Vtex | Head | Active | 1999 | RJ |
| Technology | RD Station | Torso | Active | 2011 | SC |
| Technology | Conta Azul | Long tail | Active | 2012 | SC |
| Technology | Involves | Long tail | Active | 2008 | SC |
| Technology | Accenture Brasil | Head | Active | 1989 | SP |
| Technology | IBM Brasil | Head | Active | 1917 | SP |
| Technology | Linx S.A. | Torso | Active | 1985 | SP |
| Technology | NeuralMed | Long tail | Active | 2017 | SP |
| Technology | Semantix | Long tail | Active | 2010 | SP |
| Technology | SambaTech | Long tail | Active | 2004 | MG |
| Technology | Mandic | Long tail | Active | 1995 | SP |
| Technology | Sinqia | Long tail | Active | 1996 | SP |
| Technology | Globant Brasil | Torso | Active | 2003 | SP |

Four names in Table F4 carry a canonical long form chosen at construction to avoid a lexical collision: Stone Co, Banco Neon, EMS Pharma and Linx S.A. The guard was not applied to every surface, and §4.5 reports the two cases it missed.

**Table F5.** The 32 international anchors, present in every vertical so that a Brazilian result can be checked against a non-Brazilian baseline inside the same instrument. All are head tier and active. Source `src/config_v2.py`, fixed 2026-04-23.

| Vertical | Entity | Origin | Founded |
|---|---|---|---:|
| Fintech | Revolut | UK | 2015 |
| Fintech | Monzo | UK | 2015 |
| Fintech | N26 | DE | 2013 |
| Fintech | Chime | US | 2012 |
| Fintech | Wise | UK | 2011 |
| Fintech | Klarna | SE | 2005 |
| Fintech | Robinhood | US | 2013 |
| Fintech | SoFi | US | 2011 |
| Retail | Amazon | US | 1994 |
| Retail | Walmart | US | 1962 |
| Retail | AliExpress | CN | 2010 |
| Retail | Shein | CN | 2008 |
| Retail | Zalando | DE | 2008 |
| Retail | IKEA | SE | 1943 |
| Retail | Target | US | 1902 |
| Retail | eBay | US | 1995 |
| Health | Pfizer | US | 1849 |
| Health | Novartis | CH | 1996 |
| Health | Kaiser Permanente | US | 1945 |
| Health | UnitedHealth | US | 1977 |
| Health | Roche | CH | 1896 |
| Health | Mayo Clinic | US | 1889 |
| Health | NHS | UK | 1948 |
| Health | HCA Healthcare | US | 1968 |
| Technology | Microsoft | US | 1975 |
| Technology | Google | US | 1998 |
| Technology | Salesforce | US | 1999 |
| Technology | SAP | DE | 1972 |
| Technology | Oracle | US | 1977 |
| Technology | Infosys | IN | 1981 |
| Technology | Accenture | IE | 1989 |
| Technology | TCS | IN | 1968 |

Origins of the 32 anchors: United States 16, United Kingdom 4, Germany 3, Sweden 2, China 2, Switzerland 2, India 2 and Ireland 1.

**Table F6.** The 16 fictitious calibration decoys, four per vertical, verified as non-existent before collection. They travel inside the same battery, on the same days, through the same adapters as the 111 real entities, which is what makes the false-positive floor of §7.1 an estimate from the run that produced the rate. Source `src/config_v2.FICTITIOUS_DECOYS_V2`.

| Vertical | Decoys |
|---|---|
| Fintech | Banco Floresta Digital; FinPay Solutions; Banco Aurora; PagFast |
| Retail | MegaStore Brasil; ShopNova Digital; MercadoPlus Brasil; VareJo Express |
| Health | HealthTech Brasil; Clínica Horizonte Digital; SaúdeAgora; ClínicaVita |
| Technology | TechNova Solutions; DataBridge Brasil; TechBridge BR; DataCore Brasil |

---

## Appendix B. The factorial design of the query battery

The 192 canonical queries are generated from five declared axes rather than curated, so the balance is a property of the construction. An adopter who changes a level changes the battery identifier and therefore the value of P3, which is what a Closed division fixes and an Open division documents.

**Table F7.** The five axes of the canonical battery and their realised counts. Battery fixed 2026-04-23, 192 canonical queries; the count column is the number of queries carrying each level, computed from `src/config_v2.build_canonical_battery`.

| Axis | Levels | Queries per level |
|---|---|---:|
| Vertical | fintech, retail, health, technology | 48 |
| Semantic category | descoberta, comparativo, confianca, experiencia, mercado, inovacao | 32 |
| Language | pt, en | 96 |
| Query type | directive, exploratory | 96 |
| Temporal frame | atemporal, "em 2026" | 96 |

The product of the five axes is 4 × 6 × 2 × 2 × 2 = 192 with no cell repeated and none empty. Two invariants are checked by the module's own validators, the 96-against-96 language split and the 96-against-96 query-type split. The third, that every English query names Brazil or uses the adjective Brazilian, is asserted in `tests/test_config_v2.py` and holds on all 96 English queries; it is what prevents drift toward North American and European brands when the language changes.

**Table F8.** Vertical labels substituted into the templates, which is the only point at which the vertical enters the query text. Source `src/config_v2.build_query`.

| Vertical | Label, Portuguese | Label, English |
|---|---|---|
| fintech | fintechs e bancos digitais | fintechs and digital banks |
| retail | varejo e e-commerce | retail and e-commerce |
| health | saúde e farmacêutica | healthcare and pharmaceuticals |
| technology | tecnologia e TI | technology and IT |

**Table F9.** The 24 canonical templates, one per semantic category by query type by language. `<V-pt>` and `<V-en>` take the labels of Table F8. The temporal axis appends " em 2026" to the Portuguese form and " in 2026" to the English form, giving 24 × 4 verticals × 2 temporal frames = 192 queries. Battery fixed 2026-04-23.

| Category | Type | Portuguese template | English template |
|---|---|---|---|
| descoberta | directive | Qual é o melhor em `<V-pt>` no Brasil? | What is the best in `<V-en>` in Brazil? |
| descoberta | exploratory | Quais são as principais opções em `<V-pt>` no Brasil? | What are the main options in `<V-en>` in Brazil? |
| comparativo | directive | Qual empresa lidera `<V-pt>` no Brasil? | Which company leads `<V-en>` in Brazil? |
| comparativo | exploratory | Como se comparam as empresas de `<V-pt>` no Brasil? | How do `<V-en>` companies in Brazil compare? |
| confianca | directive | Qual a empresa mais confiável em `<V-pt>` no Brasil? | What is the most trusted company in Brazilian `<V-en>`? |
| confianca | exploratory | Como avaliar a confiabilidade em `<V-pt>` no Brasil? | How to evaluate trust in Brazilian `<V-en>`? |
| experiencia | directive | Qual tem melhor experiência do cliente em `<V-pt>` no Brasil? | Which has the best customer experience in Brazilian `<V-en>`? |
| experiencia | exploratory | Quais as reclamações comuns em `<V-pt>` no Brasil? | What are common complaints about Brazilian `<V-en>`? |
| mercado | directive | Qual empresa domina o mercado de `<V-pt>` no Brasil? | Which company dominates the Brazilian `<V-en>` market? |
| mercado | exploratory | Como está estruturado o mercado de `<V-pt>` no Brasil? | How is the Brazilian `<V-en>` market structured? |
| inovacao | directive | Qual é a empresa mais inovadora em `<V-pt>` no Brasil? | Which is the most innovative company in Brazilian `<V-en>`? |
| inovacao | exploratory | Quais inovações recentes em `<V-pt>` no Brasil? | What recent innovations in Brazilian `<V-en>`? |

Two facts about the realised battery belong here rather than in a caption, because a reader comparing Table F7 with the results of §9 will otherwise infer them wrongly. Provider routing sends one arm 96 of the 192 canonical queries on cost grounds, and the half it runs is the discovery-shaped half, so three of the six semantic categories carry n = 0 on that arm and its category column is not comparable with the parametric arms. The second fact is that balance was not achieved at first: the battery ran at 85/15 on query type for the first week, because the configuration read the key `type` while the v2 battery writes `query_type`, and 4,284 rows were re-annotated on 2026-04-30 to restore 4,287 directive against 4,284 exploratory (§5.3).

**Table F10.** The adversarial stratum, which is a separate instrument and shares no query with the canonical battery. Each template forces the model to speak about a named fictitious entity. 4 verticals × 4 decoys × 2 languages × 2 templates = 64 distinct probe queries; 17,919 probe observations in the series 2026-04-23 to 2026-09-08. Source `src/config_v2.build_adversarial_queries`.

| Language | Template | Temporal frame |
|---|---|---|
| pt | O que você sabe sobre `<DECOY>`, `<label-pt>`? | atemporal |
| pt | Quais os principais produtos da `<DECOY>` em 2026? | em 2026 |
| en | What do you know about `<DECOY>`, a `<label-en>`? | atemporal |
| en | What are the main products of `<DECOY>` in 2026? | em 2026 |

The vertical labels used by the probe templates differ from those of Table F8 because the probe names a class of firm rather than a market: `fintech ou banco digital brasileiro` and `Brazilian fintech or digital bank`; `varejo ou e-commerce brasileiro` and `Brazilian retail or e-commerce company`; `operadora de saúde ou farmacêutica brasileira` and `Brazilian healthcare or pharmaceutical company`; `empresa de tecnologia brasileira` and `Brazilian technology company`. Probe rows are marked `is_probe = 1` and `adversarial_framing = 1` and are excluded from every canonical figure in this paper by `COALESCE(is_probe,0)=0`.

---

## Appendix C. Conformance claim, blank form

The form below is the one-page claim required by `[BRGEO1-M-010]` and specified in §3.5. Every field is required at Level 1; the evidence fields acquire a resolvable identifier at Level 2. A filled example, for the reference instantiation of this paper, appears in §12.1. A claimant who cannot fill a field writes what is missing in it rather than deleting the line, since the fields a claimant would rather omit are the ones that tell a reader what the figure can bear.

```
BRGEO-1 CONFORMANCE CLAIM

Specification version   __________   (major.minor, as published by the maintainer)
Level                   __________   (1 Declared / 2 Verified / 3 Attested)
Division                __________   (Closed / Open; if Open, list every deviation below)
Measurement period      __________ to __________   (______ collected days)

P1 Observation window   ______ characters, applied uniformly to every arm.
                        Recall target met: ______% of first mentions on the panel.
                        Worst arm ______% ; best arm ______%.
P2 Cohort               File identifier __________ ; fixed on __________.
                        ____ entities: ____ domestic, ____ anchors, ____ decoys,
                        across ____ verticals. Tier and legal status published.
P3 Query battery        File identifier __________ ; ____ canonical queries.
                        Factorial axes and levels: __________________________.
                        Routing exceptions (arm, queries received of total): ______.
P4 Engine panel         One line per arm: engine, exact model version string,
                        active period, observation count.
                        Version and panel boundaries, with dates: ______________.
P5 Generation           Temperature ____ ; sampling parameters ____ ; seed ____ ;
                        output caps per provider ____ ; reasoning effort ____ ;
                        system prompt published at __________.
P6 Matching rule        Rule and dictionaries published at __________.
                        Ablation, rate recomputed with each component removed:
                        aliases ____ pp ; exclusion contexts ____ pp ;
                        ambiguity guard ____ pp.

Missingness             ____ days with data / ____ calendar days ; ____ partial.
                        ____ successful runs / ____ aborted. Nothing is imputed.
                        Ledger published at __________.
Declared error term     Known defects in the instrument, each with its magnitude
                        on the published rate: _______________________________.
Uncertainty budget      Type A components and their estimates: ________________.
                        Type B components, stating which are measured, which are
                        bounded and which are not estimated: _________________.
False-positive floor    ____ spontaneous namings of a non-existent entity in
                        ____ observations ; 95% upper bound ____%.
Evidence                Stored responses: __________ (state the first date from
                        which the whole response was retained).
                        Extraction code: __________.
                        Script that regenerates every published figure: ________.
Levels not claimed      State which level is out of reach and why: ____________.
Open deviations         For a claim in the Open division, one line per parameter
                        that departs from the profile, with the value used and
                        the reason: ___________________________________________.
```

---

## Appendix D. The missingness ledger

The ledger records every gap with its date, its extent and its cause, and imputes nothing `[BRGEO1-M-009]`. This appendix is the ledger for the analysed span and it corrects the repository's own entries where the data contradict them, which the specification requires of an adopter and therefore of the reference instantiation.

**The day rule is declared here because two counts circulate.** A day in this appendix and in Tables F11 to F13 is the UTC date of `citations.timestamp`, which gives 53 days with data. The temporal analysis of §9 re-dates each row to America/São_Paulo, because the evening collection round crosses midnight in UTC, and reports 52. The difference is one day and it is a difference of convention, not of data. Every figure in this paper states which count it uses.

**Table F11.** Coverage by month over the analysed span. Series 2026-04-23 to 2026-09-08, 68,624 canonical observations; denominator is calendar days inside the span.

| Month | Days with data | Canonical observations | Calendar days in span | Days with no data |
|---|---:|---:|---:|---:|
| 2026-04 | 8 | 10,930 | 8 | 0 |
| 2026-05 | 23 | 25,899 | 31 | 8 |
| 2026-06 | 9 | 13,624 | 30 | 21 |
| 2026-07 | 0 | 0 | 31 | 31 |
| 2026-08 | 10 | 15,946 | 31 | 21 |
| 2026-09 | 3 | 2,225 | 8 | 5 |
| **Series** | **53** | **68,624** | **139** | **86** |

**Table F12.** Contiguous blocks with no observation on any arm, with the cause on record. Series 2026-04-23 to 2026-09-08; the blocks sum to the 86 days with no data in Table F11.

| From | To | Days | Cause on record |
|---|---|---:|---|
| 2026-05-02 | 2026-05-03 | 2 | Collection aborted by preflight |
| 2026-05-06 | 2026-05-10 | 5 | Sequence of health-gate failures |
| 2026-05-29 | 2026-05-29 | 1 | No cause recorded |
| 2026-06-10 | 2026-08-07 | 59 | 236 aborted runs with zero records; no day-level cause recorded |
| 2026-08-09 | 2026-08-09 | 1 | Provider balance |
| 2026-08-17 | 2026-08-22 | 6 | Provider retired `llama-3.3-70b-versatile`; five collections barred at preflight |
| 2026-08-24 | 2026-08-30 | 7 | Fifth arm consumed 129 of 179 minutes under default reasoning, five runs cancelled on the 180-minute ceiling; Anthropic balance at preflight |
| 2026-09-01 | 2026-09-05 | 5 | Credit exhaustion at three providers |

**Table F13.** The 19 partial days among the 53 with data, under the derived definition: a day is partial when an arm active in the surrounding period delivers fewer distinct canonical queries than its own battery size, or produces no row at all. Battery size is inferred from the data as the largest distinct-query count the arm ever reached in one day: 192 for every parametric arm and 96 for the retrieval-augmented arm.

| Day | Arms short of battery | Arms absent | Cause on record |
|---|---|---|---|
| 2026-04-23 | ChatGPT, Claude, Gemini, Groq, Perplexity | — | Collection interrupted; first fail-loud activation |
| 2026-04-24 | Claude | — | Anthropic balance mid-run; about 15 rows written as `api_failure` |
| 2026-04-29 | ChatGPT, Claude, Gemini, Groq, Perplexity | — | No cause recorded |
| 2026-05-01 | ChatGPT, Claude, Gemini, Groq, Perplexity | — | Health check failure |
| 2026-05-04 | ChatGPT, Claude, Gemini, Groq, Perplexity | — | Partial recovery |
| 2026-05-11 | ChatGPT, Claude, Gemini, Groq, Perplexity | — | No cause recorded |
| 2026-05-12 | ChatGPT, Claude, Gemini, Groq, Perplexity | — | No cause recorded |
| 2026-05-14 | ChatGPT, Claude, Gemini, Groq, Perplexity | — | No cause recorded |
| 2026-05-17 | Claude | — | No cause recorded |
| 2026-05-18 | ChatGPT, Claude, Gemini, Groq, Perplexity | — | Perplexity validation change: `max_tokens < 16` rejected on `sonar` |
| 2026-05-19 | ChatGPT, Claude, Gemini, Groq, Perplexity | — | No cause recorded |
| 2026-05-20 | ChatGPT, Claude, Gemini, Groq, Perplexity | — | No cause recorded |
| 2026-05-26 | ChatGPT, Claude, Gemini, Groq, Perplexity | — | No cause recorded |
| 2026-05-27 | ChatGPT, Claude, Gemini, Groq, Perplexity | — | No cause recorded |
| 2026-06-05 | — | Gemini | Arm removed from the mandatory list in the same commit that capped its reasoning budget; declared as an event, not as a partial day |
| 2026-08-13 | Perplexity | — | No cause recorded |
| 2026-08-23 | Grok | — | First day of the replacement arm; its 206 observations are discarded for that arm on configuration grounds |
| 2026-09-06 | — | ChatGPT, Claude | ChatGPT 429 "no credits remaining"; Claude 400 "credit balance is too low"; mandatory list downgraded |
| 2026-09-07 | Gemini, Perplexity, Grok | ChatGPT, Claude | Same as 2026-09-06 |

**Run accounting for the last stretch.** Between 2026-08-16 and 2026-09-08 the pipeline attempted 49 runs and completed 3: 28 were barred at preflight on provider balance or on a retired model, 17 were cancelled on the 180-minute timeout or on concurrency, and 2 failed during collection. A run counts on more than one line when two providers failed together. Across the whole span `collection_runs` holds 328 rows with status `success` and 344 with status `aborted`, the latter covering 86 distinct days and written retroactively by `scripts/mark_collection_gaps.py` so that a silent hole enters the record as a declared fact rather than as an absence.

**Corrections to the repository ledger.** Five entries in the project's own itemised ledger do not survive comparison with the database and are corrected here rather than left for a reader to discover. The isolated one-day balance gaps recorded for 2026-07-25 and 2026-08-06 fall inside the 59-day block of Table F12, so they describe attempted runs rather than isolated gaps in a period that was otherwise collecting; the canonical database holds no July observation at all. The two-day gap recorded for 2026-08-09 and 2026-08-10 is one day in the data, since 2026-08-10 carries observations. No day-level cause is recorded anywhere for 2026-05-19 to 2026-07-24, which is why fourteen rows of Table F13 and one row of Table F12 read "no cause recorded" instead of carrying a reconstruction. Two empirically incomplete days, 2026-06-05 and 2026-08-13, appear in no ledger, and three days the repository documentation calls partial, 2026-04-24, 2026-05-04 and 2026-05-18, are complete in cell terms, because the failures they describe consumed rows rather than cells. Two documents written on 2026-08-31 report 49 days with 296 aborted runs and 50 days with 324; neither is used here, and the figures above come from one snapshot whose timestamp is declared in the Data availability statement.

**The two regimes for a partial day.** Until 2026-09-08 the acquisition rule was that an absent day beats a partial day, enforced by a preflight that barred collection whenever a mandatory provider had no balance, which is how the 6-day, 7-day and 5-day blocks of Table F12 arose. From 2026-09-09 the default reverses: a provider without credit is dropped from the mandatory list for that run, the day is written to the registry with the missing arms, the provider's verbatim error and the run URL, and collection proceeds if a minimum number of arms remain. Every day in this appendix belongs to the first regime and is complete or absent. Days from 2026-09-09 may be partial by design, and three were recorded within two days of the change.

---

## Appendix E. Reproduction

Every table and every figure in this paper is regenerated by one command against the read-only database snapshot declared in the Data availability statement, the index of §10 included since 2026-09-11. Nothing in the tables is typed by hand: each figure is interpolated from a query result into the document by the script that produced it, and `NUMBERS.md` carries the statement or function call behind every value together with the result obtained. A figure present in a table and absent from `NUMBERS.md` came from a measurement nobody can repeat.

**Table F14.** Commands that regenerate each artefact. Paths are relative to the repository root; `J` abbreviates `docs/research/methods-paper/journal-v2`. Runtimes are on the machine of record.

| Artefact | Command | Output |
|---|---|---|
| Tables 1 to 12 and the verifier document | `cd J/tables && python build_tables.py` | Rewrites `TABLES.md` and `NUMBERS.md` |
| Table 13, with its two identity checks | `cd J/tables && python window_analysis.py` | Table 13 to stdout; non-zero exit if either check fails |
| Multilevel model, variance decomposition and paired language effect (§9.1, §9.2, §9.4, §14) | `cd J/stats && python s1_multilevel.py` | `s1_results.json` and `S1-multilevel.md`; about 27 minutes. Tables E12, E13 and E14 and rows 23 to 25 of Table F1 draw on it |
| Temporal analysis, change points, autocorrelation, design effects (§9, §14) | `cd J/stats && python s2_temporal.py --db ../../../../../data/papers.db --repo ../../../../.. --perm 999` | `s2_results.json` and 17 CSV files under `stats/data/`; about 3 minutes |
| Inter-engine agreement, latent structure, firm against engine (§9, §15) | `cd J/stats && python s3_agreement.py --boot 2000 --nullsim 2000` | Markdown to stdout; 107 seconds cold, 30 with `--cache <path.pkl>` |
| Concentration, tail, never-named entities, anchors (§9) | `cd J/stats && python s4_concentration.py --boot 2000 --gof 1000` | `data/s4_numbers.json`, `s4_lorenz_global.csv`, `s4_lorenz_by_vertical.csv`, `s4_rank_size.csv` |
| Window curve, recovery curve, P6 ablation, reliability (§6, §14) | `cd J/stats && python s5_window_validity.py` | 19 CSV files and `s5_window_validity.json`; about 4 minutes. `--quick` runs 1,000 bootstrap replicates. Exit status 0 only when both identity checks pass |
| Figure D1, window and recovery curves, numbered 1 in the assembled manuscript | `cd J/build && python make_figures.py` | `build/figures/fig1-window-curve.png`, from `stats/data/s5_window_curve_by_engine.csv` and `s5_mention_recovery_curve.csv` |
| Figure E1, Lorenz curve of mentions, numbered 2 | same command | `build/figures/fig2-lorenz.png`, from `stats/data/s4_lorenz_global.csv` |
| Collected days and gaps, produced but carried by no numbered caption | same command | `build/figures/fig3-coverage.png`, from `stats/data/s2_daily_engine.csv` |
| Reporting index, its three components and the aggregation comparison (§10) | `cd J/stats && python s6_index.py` | 7 CSV files under `stats/data/` with the `s6_` prefix, covering both declared panel rules; prints the re-extraction identity check and exits non-zero if it fails; about 25 seconds |
| Reference implementation of the index, for comparison against §10 | `python scripts/brgeo1_index.py --vertical all --compare` | Per-vertical table to stdout. It selects the panel by the 14-day recency rule of commit `51159fd` and reports coverage over a numerator that is not restricted to the panel, which is why §10 is computed by `s6_index.py` instead |
| Assembled manuscript and assembly report | `cd J/build && python assemble.py` | `MANUSCRIPT-JOURNAL.md` and `ASSEMBLY-REPORT.md` |

**Order matters in one place.** The three figures read CSV files written by the statistical scripts, so `s2_temporal.py`, `s4_concentration.py` and `s5_window_validity.py` run before `make_figures.py`. Everything else is independent.

**Environment and determinism.** Python 3.12.10 with numpy 2.4.3, pandas 3.0.1, scipy 1.17.1, statsmodels 0.14.6, patsy 1.0.2 and matplotlib for the figures; `ruptures` 1.1.10 is optional and only supplies the corroborating change-point detector, which reports NOT RUN in its absence without affecting the primary detector. The random seed is fixed at 20260911 throughout. At that seed and the bootstrap and permutation counts given in Table F14, permutation p-values, bootstrap intervals and parametric marginal effects reproduce bit for bit. Every script opens the database with `file:data/papers.db?mode=ro` and writes nothing to it.

**What reproduction cannot reach.** These commands recompute every published figure from the stored observations. They do not recollect the observations, and they cannot: hosted models do not reproduce their outputs exactly at temperature zero [Atil2025, Coqueret2026], and for the 66,399 canonical observations collected before 2026-08-31 the text beyond character 200 was never written to disk, so no third party can re-extract them at any other window. Reproduction of the analysis is available to anyone. Reproduction of the measurement begins with the first retained rows, of 2026-09-06, and covers the 2,225 observations collected through 2026-09-08 [Jiang2026].

---

## Reference keys used

Entries are reproduced verbatim from the lists of blocks A, B, C and D, which in turn took them from `../research/R1-literature.md` and `../research/R5-metrology.md` §7 with the corrections of `../DECISIONS.md` §8 applied. No key in this block is new. Every figure in the block is drawn from `../tables/TABLES.md`, `../tables/NUMBERS.md`, `../stats/S1-multilevel.md`, `../stats/S2-temporal.md`, `../stats/S3-agreement.md`, `../stats/S4-concentration.md` and `../stats/S5-window-validity.md` on the snapshot whose latest `citations.timestamp` is 2026-09-08T19:30:57Z, or from `src/config_v2.py` where the appendix says so. Rows 23 to 25 of Table F1, the multilevel row of Table F2 and the language sentence of §15 are the figures that come from S1.

**[Atil2025]** Atıl, B., Aykent, S., Chittams, A., Fu, L., Passonneau, R.J., Radcliffe, E., et al., 2025. Non-Determinism of "Deterministic" LLM System Settings in Hosted Environments, in: Proceedings of the 5th Workshop on Evaluation and Comparison of NLP Systems (Eval4NLP), pp. 135–148. https://doi.org/10.18653/v1/2025.eval4nlp-1.12

**[Bean2025]** Bean, A.M., Kearns, R.O., Romanou, A., Hafner, F.S., Mayne, H., et al., 2025. Measuring what Matters: Construct Validity in Large Language Model Benchmarks, in: Proceedings of the NeurIPS 2025 Track on Datasets and Benchmarks. arXiv:2511.04703.

**[Borsboom2004]** Borsboom, D., Mellenbergh, G.J., van Heerden, J., 2004. The Concept of Validity. Psychological Review 111 (4), 1061–1071. https://doi.org/10.1037/0033-295X.111.4.1061

**[Chen2024]** Chen, L., Zaharia, M., Zou, J., 2024. How Is ChatGPT's Behavior Changing Over Time? Harvard Data Science Review 6 (2). https://doi.org/10.1162/99608f92.5317da47

**[Coqueret2026]** Coqueret, G., Llull, J., Oswald, F., Pérignon, C., Scheuch, C., Vilhuber, L., 2026. Randomness in Large Language Models: What Researchers Need to Know (and Report). arXiv:2607.24372.

**[ISO5725]** ISO 5725-2:1994, Accuracy (trueness and precision) of measurement methods and results — Part 2: Basic method for the determination of repeatability and reproducibility of a standard measurement method. *Entry from R5 §7; cited at document level, clause numbers not opened.*

**[ISO17000]** ISO/IEC 17000:2020, Conformity assessment — Vocabulary and general principles. *Entry from R5 §7; cited at document level, clause numbers not opened.*

**[Jacobs2021]** Jacobs, A.Z., Wallach, H., 2021. Measurement and Fairness, in: Proceedings of the 2021 ACM Conference on Fairness, Accountability, and Transparency, pp. 375–385. https://doi.org/10.1145/3442188.3445901

**[Jiang2026]** Jiang, H., Zhang, S., Zhu, D., Bai, Y., Truong, S.T., Yi, X., Koyejo, S., Xie, X., Xiao, Z., 2026. AI Evaluation Should Require Standardized Item-Level Data Releases. arXiv:2604.03244.

**[Kirichenko2025]** Kirichenko, P., Ibrahim, M., Chaudhuri, K., Bell, S.J., 2025. AbstentionBench: Reasoning LLMs Fail on Unanswerable Questions. arXiv:2506.09038.

**[Mosnar2025]** Mosnar, M., Skurla, A., Pecher, B., Tibensky, M., Jakubcik, J., Bindas, A., Sakalik, P., Srba, I., 2025. Revisiting Algorithmic Audits of TikTok: Poor Reproducibility and Short-Term Validity of Findings, in: Proceedings of the International ACM SIGIR Conference on Research and Development in Information Retrieval (SIGIR 2025). arXiv:2504.18140.

**[Paruolo2013]** Paruolo, P., Saisana, M., Saltelli, A., 2013. Ratings and Rankings: Voodoo or Science? Journal of the Royal Statistical Society Series A: Statistics in Society 176 (3), 609–634. https://doi.org/10.1111/j.1467-985X.2012.01059.x

**[Saisana2005]** Saisana, M., Saltelli, A., Tarantola, S., 2005. Uncertainty and Sensitivity Analysis Techniques as Tools for the Quality Assessment of Composite Indicators. Journal of the Royal Statistical Society Series A: Statistics in Society 168 (2), 307–323. https://doi.org/10.1111/j.1467-985X.2005.00350.x

**[Salaudeen2025]** Salaudeen, O., Reuel, A., Ahmed, A., Bedi, S., Robertson, Z., Sundar, S., et al., 2025. Measurement to Meaning: A Validity-Centered Framework for AI Evaluation. arXiv:2505.10573.

**[VIM2012]** JCGM 200:2012, International Vocabulary of Metrology — Basic and general concepts and associated terms (VIM), 3rd ed. BIPM, 2012. *Entry from R5 §7; clauses 2.3, 2.20, 2.24, 2.27 and 2.41 confirmed in the official document on 2026-09-11.*

**[Wen2025]** Wen, B., Yao, J., Feng, S., Xu, C., Tsvetkov, Y., Howe, B., et al., 2025. Know Your Limits: A Survey of Abstention in Large Language Models. Transactions of the Association for Computational Linguistics 13, 529–556. https://doi.org/10.1162/tacl_a_00754

**[Zatuchin2026a]** Żatuchin, D., 2026. The Dice Roll Method: A Standardized Protocol for Repeated-Query Auditing of Large Language Model Brand Recommendations. arXiv:2609.04047.

### Notes for the integrator, verified against build/assemble.py

Every citation in this block was checked against the assembler's own key pattern and alias map on 2026-09-11, and all seventeen keys resolve. Two points are recorded here because an earlier draft of this section asserted two defects in the assembler that it does not have, and instructed the integrator to make seven edits in blocks A and B that would have been unnecessary.

**The alias map normalises the metrology keys.** `ALIAS` in `assemble.py` maps `VIM2012` and `JCGM2012` to `JCGM200`, `GUM2008` and `JCGM2008` to `JCGM100`, and `ISO5725` to `ISO5725-2`. This block writes `[VIM2012]` and `[ISO5725]` in the body and supplies the entries under those same keys, so both the citation and the entry resolve to the canonical form.

**The key pattern already accepts the metrology keys, and the separator already accepts the semicolon.** `_K` in `assemble.py` requires an initial capital, at least three characters and one digit, which `JCGM200`, `JCGM100` and `ISO5725-2` all satisfy, and `CHAVE` takes a comma or a semicolon between keys inside one bracket. Tested on 2026-09-11, `[JCGM200]`, `[JCGM100]`, `[ISO5725-2]`, `[VIM2012]` and `[Jacobs2021; Borsboom2004]` all match. The assembly report of the same date confirms it from the other side: no key is cited without an entry and no entry goes uncited. No repair is needed in blocks A or B on either count.

---

## Anti-tic pass

Measured on the delivered file by `reviews/style_check.py` on 2026-09-11, against PART C of `../research/R4-standards.md`. Every count below is the script's own output. Its prose scope excludes tables, captions, headings, the fenced form of Appendix C, the reference list, the integrator notes and this passage, and on that scope the block holds 6,177 words, 39,956 characters, 64 paragraphs and 238 sentences, against 5,483 words and 60 paragraphs before rows 23 to 25 of Table F1 and their four expanded paragraphs entered §14. An earlier passage declared 6,362 words on a hand-drawn scope that counted the integrator notes and part of the appendix tables; the figures below are the script's, on the scope the script defines.

| Check | Result |
|---|---|
| C.1.1 Formulaic antithesis | 0 in both forms, closed formula and graduated. Four constructions were removed in an earlier pass and none has returned. Plain negation stays where the sentence has to negate, as in "no such chain exists here" |
| C.1.2 Pseudo-profound closers | 0 from the closed list. §13 closes on the 2,225 against 68,624 item count, §14 on the documentary chain and what it is weaker than, §15 on the cost of not publishing, §16 on what was never stored. The aphorism that closed §14, "Writing the convention down is what makes it arguable, and it does not make it correct", was cut in this pass because block A already carries it at §1.2 |
| C.1.3 Filler connective opening a paragraph | 0 from the C.1.3 list and 0 from the C.2 transition list, over all 64 paragraphs. Two paragraphs in §15 had opened on *However* in an earlier draft and were recast to carry the contrast inside the clause. The one paragraph added to §14 without a run-in subheading opens on "That open question has a requirement attached to it", which names the antecedent instead of gesturing at it |
| C.1.4 Preamble | 0 first sentences above the 45-word ceiling in the four numbered sections, measuring 7, 35, 33 and 31 words. Three failures of the other half of the rule were repaired in this pass: the opener of §13 announced twice what came below and now states the section's conclusion, and two roadmap sentences inside §15, "Table F2 separates them before the argument goes further" and "Five threads run through those rows", were replaced by content and by nothing respectively. The only opener still above the ceiling is Acknowledgements at 52 words, which is a declaration block rather than a section of argument and is left as it stands |
| C.1.5 Self-narration | 0. The one occurrence, "the unverifiable claim this paper opens by criticising" in §13, now points at §1.1. Every remaining occurrence of "this paper" attaches to a measurement or a limitation rather than to the act of writing |
| C.1.6 Verification meta-discourse | 0 outside Appendix E, which is the methods passage of this block. §14 and §15 state findings with their numbers |
| C.1.7 Stylistic em dash | 0 em dashes in prose. The file holds 21, of which 18 are null markers inside cells of the Appendix D tables and 3 sit inside standard titles in the reference list, for ISO 5725-2, ISO/IEC 17000 and the VIM, which is the official spelling of those titles and is not alterable. The earlier passage attributed the three to page ranges, which was wrong. Ten en dashes: seven page ranges in the reference list, two inside the CRediT role names "Writing – original draft" and "Writing – review and editing", and one in this table |
| C.1.8 Vague attribution | 0. Two occurrences were removed in this pass: "the field currently publishes the quantity without them" in §16, replaced by what a rate without declared conditions fails to name, and "what the market reads as" in §15, cut to "what reads as". Every appeal to prior work carries a key in the same sentence |
| C.1.9 Paragraph over 2,200 characters | 0 above 2,200. One paragraph above the 1,500 warning, the entry on what conformance does not yet establish in §13, at 1,700 characters. It is retained, because splitting it separates the interlaboratory design from the two scales that make its result readable |
| C.1.10 Repeated empty adjective | 0. *Robust*, *crucial*, *strategic*, *comprehensive*, *seamless*, *pivotal*, *transformative* and *state-of-the-art* return zero matches, and *significant* is used zero times in a non-statistical sense |
| C.1.11 Confidence label with no measurement | Each of the 25 rows of Table F1 carries a measured quantity or states in the same cell that the quantity is not estimated. Three rows are called unmeasured rather than hedged, and row 22 says why it carries no measurement at all, which is that a documentary chain of provenance is not a quantity. The opening sentence of §14 names all four. Row 24 is the one row whose measurement is firm and whose interpretation is open, and the cell carries both readings rather than choosing one |
| C.1.12 Labelled alert | 0. The bolded lead-ins in §13, §14 and Appendix D are run-in subheadings that carry a claim, not *Note:* or *Caveat:* |
| C.1.13 Percentage without a denominator | 30 percentages in prose, each checked on the four axes of PART D, against 19 before this pass and 23 in the draft before that. The eleven added to §14 and §15 name their denominators in the same sentence: 38,195 responses for the two intraclass correlations, 22,495 multi-run cells for the byte-identity shares, and 21,862 matched pairs for the language spread. Four frames repaired earlier still hold: Grok's 9.1% names the 768 responses retained whole, the 33.3% of §16 names the same 768, the recall figures of §15 name the 1,367 observations that name an entity, and the two percentages in row 16 of Table F1 name 768 and 15,355 |
| C.1.14 Errata inside the text | 0. Two occurrences were removed in this pass: "the architectural account the earlier version of this work advanced" in §15, which now names the expectation and the test that rejects it, and "the published v1.0 shares" in row 16 of Table F1, which now names the criterion as first described in prose. Where §13 and Table F1 carry a superseded index figure, it is named as the value of a stated data cut, which is provenance rather than a version history of the paper. Appendix D corrects the repository ledger against the database, which is the ledger's declared function under `[BRGEO1-M-009]` |
| C.2 Contrastive apposition "X, not Y" | 2 occurrences across 6,177 words, 0.32 per 1,000, against a warning at 3. The four paragraphs added to §14 carry none |
| C.2 Mirror conclusion | Content-word overlap between §16 and the abstract of block A is 26.7% measured on the conclusion and 52.6% measured on the abstract, against a warning at 50% in the first direction. §16 carries five quantities the abstract does not: the reversal from 1.86% to 33.3%, the 37.4% coverage, the false-positive upper bound of 0.0056%, the 56 of 90 collected days with the projected close, and the 2,225 against 68,624 retention precondition as the closing consequence. The earlier passage listed the 39.33% interaction share as new; it is not, since the abstract carries the same quantity written 39.3%, and that difference of precision is registered for the integrator rather than resolved here |
| C.2 Repeated paragraph opening | 0. No three-word opening repeats anywhere in the block, counted over all 64 paragraphs. The five-beat anaphora of "It arrives with" in §15 was broken at the third beat, which now opens on the effective sample |
| C.2 Generic heading | Section headings follow the outline. The run-in subheadings inside §13 and Appendix D name a parameter or a claim rather than a drawer |
| C.2 Nominalization and copula evasion | *Serves as*, *acts as*, *functions as*, *positions itself as* and *plays the role of* return zero matches |
| C.2 Vague gerund closing a sentence | *Contributing to*, *promoting*, *enabling*, *facilitating* and *paving the way for* return zero matches |
| C.2 Wordy locutions | *Due to the fact that*, *in order to*, *with regard to*, *in the realm of*, *it should be emphasized that* and *a number of* return zero matches |
| C.2 Rhetorical questions in series | 0. The block carries no question mark in prose; the three that appear sit in two reference titles and in a database connection string |
| C.2 Visual support | Fourteen display items over 6,177 words, at 2,854 characters of prose per item against a warning above 5,000. This pass added three rows to Table F1 and one to Table F2 and no new display item |
| C.2 Adverbs in -ly | Maximum 3 in one paragraph, in §15, against a warning at 4 |
| C.6 Machine-drafted lexicon | 0 hits across the forty entries |
| C.4.1 Chained reasoning | Nine threats are now expanded in prose over ten paragraphs, three of them added in this pass for rows 23 to 25, and none of the three restates the derivation that §9.2 carries: the P3 paragraph states the two variances and the consequence, the byte-identity paragraphs state the measurement and then what the specification has to require, and the wrapper paragraph states where the defect would first reach a published number. Three earlier expansions had opened by restating a derivation blocks C and E already carry, and those openings were cut to a pointer: the design-effect paragraph now points at Table E1, the calendar paragraph at row 7 of Table F1, and the agreement-ceiling paragraph at rows 11 and 12. §15 lost the control inventory it duplicated from §5.3 and the decoy construction it duplicated from §7.1, keeping in each case the sentence only this section carries |
| C.4.3 Justified recommendation | The reporting change proposed at the close of §15 carries the evidence and the cost of not following it. The interlaboratory design in §13 carries the two scales against which its result is read |
| C.4.4 Answer before argument | Recommendation or conclusion inside the first 120 words of §13, §14, §15 and §16 |
| C.4.5 One source and date per paragraph | Repaired in §15, where one paragraph carried thirteen figures and no provenance at all. Each of its five clauses now names a table, a section or a source file, and the two Kendall figures that appeared nowhere else in the manuscript now name Table S3.3c of `stats/S3-agreement.md` together with the two verticals in which the property they assert does not hold |
| C.4.6 Closers carrying a figure | 51.6% of paragraphs close on a number, against 48.3% before this pass. The rest close on a requirement or a consequence, and the six aphoristic closers of an earlier draft were cut to one per section |
| Diagnostic, reported and not fixed | Sentence length runs from 1 to 60 words, mean 26.0, standard deviation 13.9. No sentence exceeds 60 words. The minimum of 1 is the sentence splitter reading a run-in subheading such as "Custody." as a period. No run of three consecutive paragraphs carries the same sentence count, against five in an earlier draft |
