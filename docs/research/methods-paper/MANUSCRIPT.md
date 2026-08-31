# BRGEO-1: An Open Protocol for Measuring Entity Citation in Generative Engines

**Alexandre Caramaschi**
Independent AI Researcher · ORCID [0009-0004-9150-485X](https://orcid.org/0009-0004-9150-485X)
Protocol custodian: Brasil GEO

**Working paper** · Version 1.0 · September 2026
**Target:** SSRN (Information Systems & eBusiness Network), Elsevier

---

## Abstract

Large language models now stand between consumers and the firms they might choose, and a market has formed around measuring which firms get named. That market reports citation rates that are not comparable with one another, because the conditions of measurement are left unstated. This paper specifies BRGEO-1, an open protocol for measuring entity citation in generative engines, and argues that a measurement standard — not a metric — is what the field is missing.

The protocol fixes five parameters that published figures normally leave implicit: the observation window, the entity cohort with fictitious calibration decoys, the query battery, the engine panel with pinned model versions, and a missingness ledger that records every collection gap rather than imputing it. Of the five, the window is the one we show empirically to matter most. In our own pipeline it had drifted apart between arms unnoticed — five parametric engines measured on the first 200 characters of each answer, one retrieval-augmented engine on the whole response. Across 64,191 observations the asymmetry inflated that engine's citation rate from 52.0% to 75.8%. Re-measuring the five truncated arms under the same window moves none of them by a tenth of a point, which is what separates a correction from a new number.

We also specify a derived index for reporting, and then report the result that argues against leaning on it: across 66 entities in four verticals the composite reorders almost nothing relative to simple coverage (Spearman rho = 0.980, and 0.945 restricted to the middle of the distribution). We take that seriously as a design conclusion. A standard should spend its authority on the conditions of measurement, where two defensible choices differ by 23.8 points, not on an aggregation formula where they differ by almost nothing.

BRGEO-1 is general in its rules and calibrated on Brazilian data — Portuguese and English in equal proportion, a cohort of Brazilian firms with international anchors for contrast. It is published with a reference implementation, a conformance definition, and a versioning policy, so that a third party can state that a figure was measured under it and a reader can check what that means.

**Keywords:** generative engine optimization; measurement standard; entity citation; large language models; measurement validity; retrieval-augmented generation

**JEL:** C81, C83, L86, M31

---

## 1. Introduction

A consumer who once typed a question into a search engine and read ten blue links now asks a model and reads one answer. The firms named in that answer inherit attention that used to be spread across a results page, and the firms left out have no equivalent of page two.

An industry has formed around this in under two years. Agencies sell visibility in generative answers, vendors sell dashboards that track it, and boards have begun asking for the number. The number is almost always the same one: the citation rate, the share of prompts in which a model names a given firm.

Two vendors measuring the same firm in the same week will report different citation rates, and neither is lying. They differ because they asked different questions, of different models, on different days, and — this is the part nobody reports — read different amounts of each answer before deciding whether the firm was named. There is no shared definition to appeal to. The figure travels into board decks and press releases with the precision of a measurement and the comparability of an opinion.

This is the ordinary situation of a young measurement field, and it has an ordinary solution: a protocol that fixes the conditions under which a number is produced, published openly so that anyone can meet it and any reader can check whether it was met. That is what BRGEO-1 is.

We make three claims.

**A standard is more useful here than a metric.** The field does not lack for metrics; it lacks agreement on what has to be held constant for two metrics to be compared. §2 argues this, and §3 specifies the five parameters that BRGEO-1 fixes.

**Among those parameters, the observation window is the one that moves the number.** §4 shows it on our own data, where the parameter had drifted apart between the study's own arms without any test, validator or health check detecting it. The effect is 23.8 percentage points on one engine, and its direction is predictable: it understates retrieval-augmented engines specifically, because they open with framing prose before naming anything.

**A composite index is not where the value is, and we show this against our own index.** §7 defines one, because reporting needs a headline figure, and then reports that it reorders almost nothing relative to simple coverage. We publish that result rather than the index alone, because a standard that asks the market to adopt a formula owes the market evidence about how much the formula changes.

The protocol is offered as a candidate standard for the Brazilian market, which is where it is calibrated and where the need is most acute, and its rules are written to be general. Custody, versioning and the conformance definition are in §9, because a specification without a governance model is a paper, not a standard.

## 2. Why a protocol rather than a metric

### 2.1 What a measurement standard does

A standard does not tell anyone what to measure. It tells them what to hold constant so that two measurements can be placed side by side, and it gives them a way to say which version they followed.

The comparison that matters here is rarely between two runs of the same pipeline. It is between a figure a firm produced about itself, a figure a vendor produced about the same firm, and a figure in a published study. Those three will never share code. They can share a specification.

This is why the deliverable is a protocol with a conformance statement rather than a tool or a score. A tool has users; a standard has adopters, and an adopter needs to be able to implement it independently and still land on a comparable number.

### 2.2 The three parameters that circulate unstated

Reviewing how citation rates are reported in practitioner material and early research, three parameters recur as unspecified:

**The window.** How much of the answer was read before deciding. §4.

**The matching rule.** Whether an entity counts when its name appears anywhere, only when presented as a recommendation, or only when accompanied by a source. Substring matching on short brand names is especially fragile in Portuguese, where *Inter* occurs inside ordinary words and *99* inside percentages.

**The refusal case.** What happens when a model declines. A model that says it has no information about a firm has produced a response containing that firm's name. Instruments counting name occurrences record this as a citation, and in the adversarial case as a hallucination. It is the opposite: a correct refusal. §5 gives the measured size of this error in our own probes — 67.4% of what we had been counting as hallucinations.

### 2.3 Why the Brazilian market first

The rules in §3 are market-neutral. The calibration is not, and the choice is deliberate.

Portuguese-language measurement is where the instrument breaks in ways English-first tooling does not anticipate: diacritics that models render inconsistently across languages, brand names that collide with ordinary words, and a market whose leading firms postdate the pre-training cutoff of several deployed models. A protocol that survives Portuguese has been tested against harder conditions than one calibrated on English alone.

The English half of the battery is not decoration. Every canonical query exists in both languages, and the cohort carries 32 international anchors, so that a Brazilian result can be checked against a non-Brazilian baseline within the same instrument rather than against someone else's study.

## 3. The BRGEO-1 specification

### 3.1 The five declared parameters

A figure is measured under BRGEO-1 when all five are fixed, published, and versioned with the figure.

**P1 — Observation window.** The number of characters of each response over which entity extraction runs, applied identically to every engine in the panel. BRGEO-1 sets a default of 200 characters and requires that whatever value is used be stated with the figure. Rationale and evidence in §4.

**P2 — Cohort.** The set of entities the instrument can detect, fixed before collection begins, with three requirements: tier stratification (head, torso, long tail), annotated legal status, and fictitious calibration decoys. Decoys are not optional; without them a false-positive rate cannot be estimated and a citation rate has no floor. §5.

**P3 — Query battery.** A factorial design over the dimensions that are known to move citation behaviour, balanced rather than convenience-sampled: language, query type (directive against exploratory), temporal frame, and semantic category. Balance is a conformance requirement because an unbalanced battery silently encodes the author's assumptions about what users ask.

**P4 — Engine panel with pinned versions.** Every engine identified by an explicit model version recorded on every observation. Providers update the model behind a stable product name without notice; a series that records only the product name cannot distinguish a change in the world from a change in the instrument.

**P5 — Missingness ledger.** Every collection gap recorded with date, extent and cause, and marked in the data rather than imputed or silently dropped. §8.

### 3.2 Conformance

Three levels, so that adoption does not require running a full longitudinal panel.

**BRGEO-1 Basic.** P1, P2 and P4 declared. Sufficient for a point-in-time measurement of one firm. A figure at this level may be compared with another Basic figure using the same window and panel.

**BRGEO-1 Full.** All five parameters, with a balanced battery (P3) and a published ledger (P5). Required for any longitudinal claim, any cross-vertical comparison, and any claim about change over time.

**BRGEO-1 Full + Calibrated.** Full, plus fictitious decoys active in the same collection, so that the reported rate carries an empirical false-positive floor from the same instrument that produced it.

A conformance statement names the level, the protocol version, and the five parameter values. It is one paragraph, and its absence is informative.

### 3.3 The reference instantiation

The values below are what our own longitudinal study uses. They are the calibration, not the specification: another adopter meets BRGEO-1 with different values, provided they are declared.

| Parameter | Reference value |
|---|---|
| P1 Window | 200 characters, uniform across the panel |
| P2 Cohort | 127 entities — 79 Brazilian firms, 32 international anchors, 16 fictitious decoys, across 4 verticals |
| P3 Battery | 192 canonical queries (4 verticals × 6 categories × 2 languages × 2 query types × 2 temporal frames) plus 64 adversarial probes |
| P4 Panel | 6 engines, versions pinned per observation; 5 parametric, 1 retrieval-augmented |
| P5 Ledger | every gap recorded; 49 days with data against 296 aborted runs, published |

Cohort construction follows P2: tiers stratified with at least three long-tail firms per vertical, seven Brazilian states represented, legal status annotated so that a model naming a firm in judicial recovery is not pooled with one naming an active firm, and firms founded after 2020 deliberately included to probe the awareness gap of models whose pre-training predates them. Each of the 16 decoys was verified as non-existent against the federal tax registry, mapping services and court records before inclusion.

The unit of observation is one (query, engine, run) triple, collected twice daily. Two runs per day give a within-day contrast that separates genuine temporal variance from sampling noise at a single hour.

## 4. P1: the observation window

### 4.1 The parameter

Entity extraction runs over a string. That string is not the model's answer; it is whatever the pipeline kept. The length of that string is the observation window, and BRGEO-1 requires it to be declared because two defensible values produce materially different numbers.

The parameter has a substantive reading, not merely a technical one. A narrow window measures *head-of-response citation*: whether the firm appears in the opening a reader sees before deciding whether to keep reading. A full window measures *whole-response citation*: whether it appears anywhere the reader could eventually reach. Either is defensible. Leaving the choice implicit is not, because then the figure cannot be compared with anyone else's.

### 4.2 How the asymmetry arose, and why nothing caught it

Our pipeline stored the extraction string in a single column. Five of the six provider adapters passed the answer through a helper that truncated it to the first 200 characters. The sixth returned earlier in the call path and stored the response whole, up to 2,502 characters.

No test caught this, because every test asserted on the column and the column was populated in both cases. No validator caught it, because both values are well-formed strings of plausible length. The daily health checks verified that all six engines produced rows, that the language split held at 50/50, and that probes were being marked — all true. Two hundred and twenty-three tests passed. The defect lived one level below every assertion the pipeline made about itself.

It surfaced from a distributional check rather than a functional one. Stored response length sat against a ceiling of exactly 200 characters in five arms and nowhere near it in the sixth:

| Arm | n | Mean length | Min | Max | Share at exactly 200 |
|---|---:|---:|---:|---:|---:|
| ChatGPT | 18,560 | 200.0 | 200 | 200 | 100.0% |
| Claude | 18,394 | 200.0 | 200 | 200 | 100.0% |
| Groq | 18,304 | 199.8 | 74 | 200 | 99.8% |
| Grok | 206 | 199.9 | 187 | 200 | 99.0% |
| Gemini | 18,026 | 198.5 | 87 | 200 | 97.3% |
| **Perplexity** | **7,148** | **691.8** | **198** | **2,502** | **0.0%** |

A variable whose maximum equals its minimum across 18,560 observations is not measuring anything; it is reporting a boundary. The arms that fall marginally short of 200 are those that sometimes answered in fewer characters than the ceiling, which is the signature of truncation rather than of a length distribution.

This is why P1 is a conformance requirement and not a recommendation. The window is normally a line of code inside a provider adapter, written for reasons of cost or log volume, and it therefore varies exactly where studies are least likely to look: between providers, which is where the comparison lives.

### 4.3 Magnitude

Re-running extraction over the 49-day series under a uniform 200-character window:

| Arm | n | As collected | Uniform window | Δ | Rows actually cut |
|---|---:|---:|---:|---:|---:|
| ChatGPT | 14,400 | 17.2% | 17.2% | +0.0 pp | 0 |
| Claude | 14,266 | 25.8% | 25.8% | +0.0 pp | 0 |
| Groq | 14,208 | 8.5% | 8.5% | +0.0 pp | 0 |
| Gemini | 14,011 | 1.8% | 1.8% | +0.0 pp | 0 |
| Grok | 158 | 39.2% | 39.2% | +0.0 pp | 0 |
| **Perplexity** | **7,148** | **75.8%** | **52.0%** | **−23.8 pp** | **7,147** |

Canonical queries only. The five zero-deltas are the verification: they confirm the re-extraction reproduces the original instrument exactly where the window did not change, which is what licenses reading the sixth row as a correction rather than as new code producing a new number.

The effect is large enough to reverse an interpretation. At 75.8% the retrieval-augmented engine looks categorically different from the parametric ones, roughly twice the rate of the closest competitor. At 52.0% it remains highest but sits within the same family — a difference of degree, and one that any account of *why* would have to explain differently.

### 4.4 The bias has a direction

The asymmetry is not an accident of which adapter happened to be written differently. A retrieval-augmented engine composes its answer after fetching sources, and its opening is typically framing: a restatement of the question, a scoping remark, a note on what the sources cover. Named entities arrive once that framing is done. A parametric model, generating from weights without a retrieval step, names candidates earlier.

A narrow window therefore does not penalise all engines equally. It penalises those whose rhetorical structure defers naming, and the direction is predictable: it understates retrieval-augmented engines. First-mention offsets show it:

| Arm | Cited observations | Mean first-mention offset | Max offset |
|---|---:|---:|---:|
| Perplexity | 5,418 | 157 chars | 1,994 |
| Claude | 3,674 | 124 chars | 194 |
| ChatGPT | 2,471 | 116 chars | 194 |
| Groq | 1,210 | 108 chars | 193 |
| Gemini | 252 | 97 chars | 187 |
| Grok | 62 | 25 chars | 182 |

The maxima for the parametric arms cluster just under 200 because that is where their stored text ended; the tail beyond was never observable. For the retrieval-augmented arm, 1,558 of 5,418 cited observations name the first entity past character 200, and 1,698 observations lose their citation entirely under the cut.

Any comparison of retrieval-augmented against parametric engines under an undeclared window is confounded with discourse structure. This is the strongest practical argument for the protocol: the confound is invisible, systematic, and points the same way every time.

### 4.5 What BRGEO-1 requires

- **Uniformity.** One window, applied identically to every engine. Per-provider windows are a conformance failure.
- **Declaration.** The value is published with the figure.
- **Retention of the full response.** The complete answer is stored alongside the window so that a third party can re-extract. Until August 2026 ours was discarded in the client, which meant none of 80,638 observations could be independently reproduced. This was the more serious of the two defects: an asymmetric window is correctable because the truncated string is still the string the extractor saw, but no amount of care recovers text that was never stored.
- **Sensitivity reporting.** Where the full response exists, the headline figure is reported under both windows, per engine.

## 5. P2: calibration decoys and the refusal taxonomy

### 5.1 Why decoys are mandatory

A citation rate without a false-positive floor is a number without a zero. Sixteen fictitious entities, verified as non-existent before collection, give the instrument that floor from within the same run that produced the rate.

Adversarial probes name a decoy and ask about it directly, forcing a decision: describe an entity that does not exist, or decline.

### 5.2 The refusal problem

Our original implementation flagged a hallucination whenever the decoy's name occurred in the response. This is wrong in a specific and consequential way: the probe puts the name in the prompt, so any response that engages with the question at all — including a refusal — contains it.

Of 15,993 responses flagged as hallucinations, **67.4% carried an explicit refusal marker**, and the sample includes a model stating plainly that the named institution is not a real or registered financial institution in Brazil. Counting that as a hallucination inverts the measurement. The regular expression used is conservative, so 67.4% is a floor rather than a ceiling.

BRGEO-1 therefore specifies a three-way outcome rather than a binary:

1. **Ontological refusal** — the model states the entity does not exist. The strongest correct response.
2. **Epistemic refusal** — the model states it lacks information, typically citing a training cutoff. Correct in effect, weaker in kind: it declines without asserting non-existence.
3. **Fabrication** — the model describes products, history or positioning for an entity that has none.

Only the third is a hallucination. A protocol that pools all three reports a false-positive rate near 97% where the defensible figure is roughly a third of that. The taxonomy is the reportable output; the collapsed rate is not.

### 5.3 Probe coverage is a conformance requirement

Our probe stratum previously excluded the retrieval-augmented engine entirely, because provider routing sent only a subset of query categories to it and the calibration category was not among them. The exclusion removed the most informative case from the design: an engine that searches before answering has evidence available that a parametric model does not, and whether it uses that evidence to refuse is the question worth asking. BRGEO-1 requires probes to cover every engine in the panel.

## 6. P4 and P5: instrument drift and honest missingness

### 6.1 Series events

An instrument that changes mid-series and reports a single pooled figure is reporting an average over several instruments. BRGEO-1 requires each change to be dated, recorded and carried into analysis as a stratification boundary. Four have occurred in ours:

**2026-06-17 — Gemini model and reasoning budget.** Moved from one model version to another with internal reasoning disabled. Pre- and post-boundary observations in this arm are not comparable.

**2026-08-19 — fifth arm replaced.** The provider retired the model; the arm was replaced with another vendor's. This is a change of engine, not of configuration, and the two are not a continuous series.

**2026-08-31 — window unified.** §4. Affects the retrieval-augmented arm only; the other five are unchanged by construction, which the zero-deltas demonstrate.

**2026-08-31 — reasoning effort reduced on one arm.** A generation parameter, so the 206 observations under the previous setting form a separate stratum. Because the boundary falls at 206 of roughly 18,000 per-arm observations, that day is discarded for that arm rather than stratified.

### 6.2 The ledger

Longitudinal collection against commercial APIs fails: providers return errors, credit runs out, payload validation changes without notice. A study that imputes those gaps, or reports only the days that worked, misrepresents its own series.

BRGEO-1 imputes nothing. Every gap is recorded with date, extent and cause. As of this writing the series holds 49 days with data against 296 aborted runs, and we publish that ratio because it is the honest denominator for any claim about temporal stability. Analysis weights days by coverage with a random intercept per collection date; partial days enter a sensitivity analysis reported with and without them; total gaps are excluded from the formal analytic window.

The failure modes are worth naming, because an adopter will meet them. Ours were: credit exhaustion at a provider, a job timeout caused by one engine's default reasoning consuming 72% of the run, and a restore path that had been silently inert for two months because it depended on configuration that was never created. All three produced green pipelines.

## 7. The derived index, and the evidence against leaning on it

### 7.1 Definition

Reporting needs a headline figure. BRGEO-1 defines one, from three components computable under the specification:

- **Coverage (C)** — the share of panel observations in which the entity is named.
- **Prominence (P)** — one minus the relative offset of the entity's first mention within the window, averaged over observations where it appears. An entity named in the opening clause scores higher than one named at the edge of the window.
- **Engine breadth (B)** — the share of panel engines that name the entity at all.

The index is their geometric mean:

> **GCI = (C × P × B)^(1/3)**

The geometric mean is chosen for a substantive reason rather than convenience: it is non-compensatory. Being invisible in one engine cannot be offset by strength in another, which matches how the quantity behaves in the world — a firm absent from an engine is absent for every user of that engine. An arithmetic mean would let a single strong arm mask absence elsewhere.

BRGEO-1 requires the three components to be published alongside the index. An index reported alone is a conformance failure.

### 7.2 The result we did not want

Having defined it, we tested whether it does anything. Across 66 entities in four verticals, the index ranks entities almost identically to raw coverage:

| Subset | Spearman rho | n |
|---|---:|---:|
| All entities | 0.980 | 66 |
| Excluding each vertical's leader | 0.977 | 62 |
| Middle of the distribution (0.1%–5% coverage) | 0.945 | 42 |
| Tail (below 1% coverage) | 0.957 | 44 |

The high correlation is not an artefact of market concentration. Removing the leader of each vertical — Nubank alone accounts for 66.4% of measured coverage in fintech — barely moves it, and restricting to entities of comparable coverage leaves it at 0.945.

Reordering happens, and it happens where the theory says it should: entities whose coverage is concentrated in a single engine fall, and entities named early in the response rise. But the movement is one or two positions, not a different picture of the market.

### 7.3 What follows from that

We report this rather than the index alone, and it changes the shape of the standard.

The temptation in a young measurement market is to make the index the product: name it, brand it, sell access to it. The evidence here says the index is the least consequential part of the specification. Two defensible aggregation choices produce nearly the same ranking. Two defensible window choices produce a 23.8-point difference on the same engine, and a qualitative reversal in how that engine compares with its peers.

A standard should spend its authority where the disagreement is. BRGEO-1 therefore treats the index as a reporting convenience, subordinate to the components and to the declared parameters, and its conformance rules constrain the conditions of measurement rather than the formula.

This also blunts the standard objection to composite indices, which is that the aggregation is arbitrary. It is somewhat arbitrary. We measured how much that matters and it is small, which is the sort of thing worth knowing before an industry builds contracts on it.

## 8. Validation and pre-registered analysis

The confirmatory window closes on 28 September 2026. This paper carries no confirmatory results, and the plan is recorded here for that reason.

**H1 — vertical asymmetry.** Citation rates differ across verticals. Likelihood-ratio test on the vertical fixed effect in a mixed-effects logistic model with random intercepts per query and per collection date. Minimum meaningful effect: Cramér's V ≥ 0.15.

**H2 — false-positive baseline.** Fabrication rate on fictitious entities, using the §5.2 taxonomy rather than name occurrence, differs across engines. Tested across all six arms. Directional expectation: the retrieval-augmented arm fabricates less, having retrieval evidence available.

**H3 — inter-engine agreement.** Agreement on cited entity sets across the panel, Fleiss kappa on the rectangular query × engine panel, per vertical.

**H4 — temporal stability.** At least one engine shows a non-stationary citation rate, as a significant slope on day index after false-discovery-rate correction.

**H5 — directive inflation.** Directive queries yield higher citation rates than exploratory ones, Cohen's h as effect size.

**H6 — window sensitivity.** The gap between head-of-response and whole-response citation is larger for retrieval-augmented than for parametric engines. Testable only because the full response is now retained, and it converts the defect of §4 into a measurable claim.

Multiplicity handled by Benjamini-Hochberg; cluster-robust standard errors for repeated queries; cells below 30 observations reported as descriptive without inferential claim. Anything not listed here is labelled exploratory and reported without p-values.

## 9. Governance

A specification without a governance model is a paper. Four commitments make BRGEO-1 adoptable.

**Custody.** Brasil GEO maintains the specification and the reference implementation. Custody means publishing changes, dating them, and keeping prior versions resolvable; it does not mean gatekeeping. No permission is required to implement BRGEO-1 or to state conformance with it.

**Openness.** The specification, the reference implementation, the query battery, the cohort definition and the harmonization script are public. An adopter can implement independently and check their implementation against ours on the same inputs.

**Versioning.** Semantic, and tied to comparability. A change that alters what a conforming figure means increments the major version; a clarification that does not increments the minor. A figure cites the version it was measured under. The four series events in §6.1 are the model for how instrument changes are published.

**Scope of the series.** BRGEO-1 covers entity citation measurement. Adjacent problems get their own numbers rather than being folded into this one — source and SERP divergence, and intervention measurement, are the obvious next two. Keeping them separate is what allows an adopter to conform to one without implementing all.

**How to adopt.** Fix the five parameters, publish them with the figure, state the conformance level. That is the whole obligation. A firm measuring only itself meets Basic with a paragraph; a vendor publishing comparative rankings should meet Full, and the absence of a ledger in a comparative ranking is worth a reader's attention.

## 10. Threats to validity

**Construct validity — elicitation mode.** We send plain natural-language prompts and extract entities post hoc, rather than instructing models to return structured lists. This is closer to what a user sees, but we have not yet measured how far the two modes diverge at scale. The dual collector exists and the comparison is the highest-priority open item; until it runs, results characterise natural-mode answers and should not be assumed to transfer.

**Construct validity — window choice.** Head-of-response citation is defensible but it is a choice. Every headline figure is reported under both windows for this reason.

**Construct validity — index.** §7.2 is a limitation reported as a finding. The composite adds little over coverage in this dataset; whether it separates more in a less concentrated market is untested.

**Internal validity — instrument changes.** Four series events in five months. Each is dated and stratified, but cross-boundary comparison within an affected arm is descriptive.

**Internal validity — unequal sampling.** Provider routing sends the retrieval-augmented arm roughly half the canonical battery, on cost grounds. Its per-cell power is lower, and this is reported rather than corrected by weighting.

**External validity — market and language.** The cohort is Brazilian and the battery is Portuguese and English. Vertical asymmetries may reflect the composition of Brazilian web corpora rather than a general property of the models. The international anchors are the internal check on this, not a substitute for replication elsewhere.

**External validity — model tier.** The panel uses small, low-cost models, which is what makes twice-daily collection over 90 days affordable. Flagship models may behave differently; the quarterly scaling observation exists to test that at low frequency rather than to claim it.

**Statistical conclusion validity — missingness.** 49 days with data against 296 aborted runs. The gaps are not missing at random: they cluster around provider credit exhaustion, which correlates with cost, which correlates with response length. We publish the ledger and weight by coverage; we do not claim the mechanism is ignorable.

## 11. Discussion

The finding we would ask a reader to carry away is not that our pipeline had a defect. It is that the defect was invisible to every check the pipeline ran on itself, and the checks were not weak ones. Six engines produced rows daily. The language split held at exactly 50/50. Probes were marked. Response hashes varied. Two hundred and twenty-three tests passed. None of it could detect that one arm was measured on a different amount of text than the others, because none of it asked what the extractor was reading.

Defects of this shape are likely common in citation measurement, for a structural reason: the window is usually not a design decision at all. It is the incidental consequence of how a provider adapter was written, and it varies between providers, which is where the comparison lives.

For the practitioner market, the implication is direct. A citation rate reported without a window is not comparable to another citation rate, and the error is not small: 23.8 points on our data, enough to move an engine from apparent outlier to member of the same family. A buyer evaluating vendor figures has one question that separates a measurement from an assertion, and it is what window was used.

For research, the implication is that the window belongs alongside model version and prompt text among the parameters reported by default.

We publish the protocol before our confirmatory results so that the analysis plan precedes the estimates, and so that the window is on record as a declared parameter rather than as something settled after seeing which value produced the more interesting finding.

## 12. Availability

Specification, reference implementation, dataset, query battery, cohort definition and harmonization script are public at `github.com/alexandrebrt14-sys/papers`. Collection logs and the missingness ledger are retained with the workflow runs. A versioned dataset snapshot is deposited with a persistent identifier at the close of the confirmatory window.

## 13. Declaration of competing interest

Alexandre Caramaschi is Chief Strategy Officer of Nuvini (Nasdaq: NVNI). This work is conducted and published in his capacity as Founder of Brasil GEO, and does not represent a position of Nuvini.

Brasil GEO sells generative engine optimization services commercially and is the custodian of the protocol proposed here. This is a competing interest of the most direct kind: a firm that sells GEO services benefits if its own measurement protocol becomes the market's reference, and the reader should weigh the paper accordingly.

Three features of the design limit what that interest can do to the results. The cohort was fixed before collection began and contains no client selected for that reason. The specification, the battery, the cohort and the analysis plan are public and were registered in the repository before the confirmatory window closed. And §7.2 reports a result that runs against the commercial interest — that the index this paper defines adds little over a simpler measure — because the alternative would have been to publish the index without testing it.

No external funding supported this work. API costs were borne by the author.
