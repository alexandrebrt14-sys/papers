# BRGEO-1: An Open Protocol for Measuring Entity Citation in Generative Engines

**Alexandre Caramaschi**

Brasil GEO, São Paulo, Brazil · ORCID [0009-0004-9150-485X](https://orcid.org/0009-0004-9150-485X)

**Working paper** · Version 1.0 · September 2026

---

## Highlights

- Citation rates from generative engines are reported without the conditions under which they were measured.
- BRGEO-1 fixes six parameters and defines three conformance levels on an attestation axis.
- The observation window moved one engine's citation rate by 23.8 percentage points.
- Susceptibility to the window tracks per-model response style, not engine architecture.
- Two defensible aggregations of the same components rank entities at rho 0.706.

## Abstract

Large language models increasingly mediate how consumers discover firms, and a market has formed around measuring which firms get named. Figures from that market are not comparable with one another, because the conditions under which a citation is counted are left unstated. We specify BRGEO-1, an open protocol for measuring entity citation in generative engines, fixing six parameters that published figures normally leave implicit and defining three conformance levels on an attestation axis. We show that one parameter, the observation window, is first-order: across 66,399 canonical observations from a six-engine panel, measuring one engine on its full response rather than on the first 200 characters moved its citation rate from 51.9% to 75.8%. We report the mechanism as unresolved. Measured relative to the text observed, the retrieval-augmented arm names entities earlier than every parametric arm, contradicting the discourse-structure account we initially advanced; susceptibility instead tracks per-model response style, and the engine most affected is parametric, opening 79.6% of its answers with preamble. We also define a reporting index and report evidence against leaning on it: two defensible aggregations of the same components correlate at 0.706. A measurement standard should constrain the conditions of observation, where disagreement is large and resolvable, rather than the aggregation formula.

**Keywords:** generative engine optimization; measurement standard; entity citation; large language models; construct validity; retrieval-augmented generation

**JEL classification:** C81; C83; L86; M31

---

## 1. Introduction

A consumer who once typed a question into a search engine and read ten ranked links now asks a model and reads one answer. Firms named in that answer inherit attention formerly spread across a results page; firms omitted have no equivalent of page two.

An industry formed around this in under two years. Agencies sell visibility in generative answers, vendors sell dashboards tracking it, and boards ask for the number. The number is almost always the citation rate: the share of prompts in which a model names a given firm.

Two vendors measuring the same firm in the same week will report different citation rates, and neither need be dishonest. They differ because they asked different questions, of different models, on different days, and — the part that is never reported — read different amounts of each answer before deciding whether the firm was named. There is no shared definition to appeal to. The figure travels into board decks with the precision of a measurement and the comparability of an opinion.

This is the ordinary condition of a young measurement field, and it has an ordinary remedy: a protocol that fixes the conditions under which a number is produced, published openly so anyone can meet it and any reader can check whether it was met. That is what BRGEO-1 is.

**On the identifier.** BRGEO-1 is an opaque identifier. The prefix denotes the organisation that maintains the specification, in the manner of an IETF or W3C document number, and carries no geographic scope. The protocol is written for any market and any language; §4 explains why its reference instantiation is Brazilian, and why that is a stress test rather than a restriction.

We make three claims.

**A standard is more useful here than a metric.** The field does not lack metrics; it lacks agreement on what must be held constant for two metrics to be compared. §2 positions this against recent work, and §3 specifies the six parameters BRGEO-1 fixes.

**Among those parameters, the observation window is first-order and its effect is not predictable from architecture.** §5 shows a 23.8 percentage point movement on one engine, and then shows that our initial mechanistic account of that movement was wrong. Susceptibility tracks per-model response style, which cannot be inferred from whether an engine is retrieval-augmented.

**A composite index is not where the value is, and we show this against our own index.** §8 defines one, because reporting needs a headline figure, and then reports that aggregation choice is unstable across defensible alternatives while adding little over the dominant component. We publish that rather than the index alone.

## 2. Related work

### 2.1 Generative engine optimization

The term originates with Aggarwal et al. [1], who introduced GEO and the GEO-bench suite for evaluating content modifications against generative engines. Subsequent work has extended the testbed [2] and studied structural features of content that correlate with citation [3].

Measurement of citation itself became an active area during 2026. Sielinski [4] treats visibility metrics as sample estimators and shows with bootstrap intervals that apparent differences between domains often fall within measurement noise. Schulte et al. [5] show that generative search results vary between runs and over time, and argue for characterising visibility as a distribution rather than a point result. Zhang et al. [6] separate citation *selection*, where a platform chooses a source, from citation *absorption*, where the cited page contributes language and evidence to the answer. Varga [7] distinguishes raw mention from verified mention and reports entity-specific calibration effects. Kumar [8] reports brand visibility at scale across engines. Martinez [9] surveys the field between 2023 and 2026 and concludes that terminology, metrics and evidentiary standards remain heterogeneous, and that no reviewed technique demonstrates a stable causal effect that holds longitudinally and across platforms.

BRGEO-1 is complementary to these. Sielinski addresses sample size, Schulte addresses temporal sampling, Zhang addresses what a citation *is* semantically, and Varga addresses per-entity bias. None isolates how much of the answer the instrument reads. That parameter is the subject of §5, and to our knowledge it has not previously been manipulated as a controlled variable.

### 2.2 Attribution and verifiability

Rashkin et al. [10] give the formal Attributable to Identified Sources framework. Liu et al. [11] establish citation precision and recall as auditable metrics for generative search engines, and Gao et al. [12] provide the ALCE benchmark for citation generation. Venkit et al. [13, 14] audit source-cited responses and report systematic gaps between claimed and actual verifiability. This literature measures whether a cited source supports a claim. BRGEO-1 measures whether an entity is named at all, which is upstream of attribution and is the quantity the commercial market reports.

### 2.3 Fictitious entities, refusal and abstention

Jung and Gonen [15] introduce PhantomBench, built from non-existent terms and entities derived from real concepts, and report that frontier models frequently fail to abstain when a question presupposes existence. Bang et al. [16] include a NonExistentRefusal task within HalluLens. Kirichenko et al. [17] benchmark abstention on unanswerable questions, and Pan et al. [18] propose a refusal index relating refusal probability to error probability. Surveys by Ji et al. [19] and Huang et al. [20] map the broader hallucination literature.

These works use non-existent entities as a *target* of measurement. BRGEO-1 uses them as an *instrument*: decoys embedded in the same collection provide an empirical false-positive floor for the citation rate itself. We have not located prior work using fictitious entities as a negative control on a visibility measurement, and §6 reports what happened when we implemented that badly.

### 2.4 Measurement validity and benchmark critique

The concern that a widely reported quantity may lack construct validity is not specific to this field. Jacobs and Wallach [21] give the framework for treating an unobservable construct as requiring an explicit measurement model. Raji et al. [22] and Bowman and Dahl [23] document how benchmarks acquire authority disconnected from what they measure, and Reiter [24] provides the canonical case study in BLEU. Bean et al. [25] review 445 benchmarks and find construct validity problems to be systemic. Hochlehnert et al. [26] show that decoding parameters, seed and prompt format move reasoning results enough to reverse conclusions — the closest structural analogue to our window finding. Encarnación et al. [27] reach a convergent conclusion by an independent route, measuring that chat interface and API diverge and that enabling web search shifts accuracy by up to eight percentage points, and argue that access condition is a measurement parameter rather than an implementation detail.

### 2.5 Reporting standards and open specifications

Breuer et al. [28] propose `ir_metadata`, an extensible metadata schema attached to IR experiment results, following the PRIMAD model of components that affect reproducibility [29]. Ghosh et al. [30] compose benchmark metadata, run data and model metadata into a single record with interpretive signals for reproducibility and score comparability. Documentation conventions established by Mitchell et al. [31] and Gebru et al. [32] provide precedent for structured disclosure. Metaxa et al. [33] give the algorithm auditing methodology that underlies our design, including the requirement to record collection failures.

For the shape of an open specification that becomes a standard by adoption rather than authority, HELM [34], MTEB [35] and BEIR [36] are the relevant precedents; MMTEB [37] shows the same specification growing by community contribution. The TREC deep learning track [38] provides the institutional genealogy, and Voorhees [39] the classic demonstration that relative system ordering survives judge variability provided the protocol is fixed — which is the strongest available answer to the objection that non-deterministic answers cannot be measured. Bailey et al. [40] provide precedent for a test collection built explicitly on query variability.

### 2.6 Position effects

Liu et al. [41] establish that models use information in long contexts unevenly, with position mattering. Guo and Vosoughi [42] document serial position effects across tasks and models. Menschikov et al. [43] show that position effects are primarily model-specific with language-specific nuance, and that some models favour later positions, contradicting a universal early-token account. This literature concerns position within the *input*; §5 concerns position within the *output*, and §5.4 reports that the analogous effect there is likewise model-specific rather than architectural.

## 3. The BRGEO-1 specification

### 3.1 The six declared parameters

*This subsection is normative.*

A figure is measured under BRGEO-1 when all six parameters are fixed, published with the figure, and versioned.

**P1 — Observation window.** The number of characters of each response over which entity extraction runs, applied identically to every engine in the panel. Per-engine windows are a conformance failure. Rationale and evidence in §5.

**P2 — Cohort.** The set of entities the instrument can detect, fixed before collection begins, with tier stratification, annotated legal status, and fictitious calibration decoys. Decoys are required: without them a citation rate has no empirical floor.

**P3 — Query battery.** A factorial design over dimensions known to move citation behaviour — language, query type, temporal frame, semantic category — balanced rather than convenience-sampled. Balance is a conformance requirement because an unbalanced battery silently encodes the author's assumptions about what users ask.

**P4 — Engine panel with pinned versions.** Every engine identified by an explicit model version string recorded on every observation. Providers update the model behind a stable product name without notice; a series recording only the product name cannot distinguish a change in the world from a change in the instrument.

**P5 — Generation configuration.** Temperature, nucleus sampling parameter, seed where available, output limits, reasoning effort where applicable, and the system prompt, published with the figure. §7.1 documents a series event in our own data caused by a change to reasoning effort alone; a specification that pins the model and leaves generation configuration free has a gap the size of that event.

**P6 — Entity matching rule.** The procedure mapping a response to the set of entities it names: matching form, alias table, disambiguation policy, exclusion contexts, and boundary policy for a mention that straddles the window edge. Two implementations with different matching rules produce different figures under identical values of P1 to P5, which would defeat the purpose of the specification.

BRGEO-1 additionally requires a **missingness ledger**: every collection gap recorded with date, extent and cause, marked in the data rather than imputed or silently dropped (§7.2).

### 3.2 Normative language

*This subsection is normative.* The key words "MUST", "MUST NOT", "REQUIRED",
"SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED",
"MAY", and "OPTIONAL" in this document are to be interpreted as described in
BCP 14 [45, 46] when, and only when, they appear in all capitals, as shown here.

Sections are marked as normative or informative. Only normative content states
requirements for conformance; examples and explanatory passages impose none.
Requirements carry stable identifiers of the form `[BRGEO1-M-nnn]` for MUST,
`[BRGEO1-S-nnn]` for SHOULD and `[BRGEO1-O-nnn]` for OPTIONAL, so that errata
and audit findings have a fixed referent.

### 3.3 Conformance levels

Levels sit on an axis of attestation rather than of completeness, following the
vocabulary of ISO/IEC 17000 for first-party declaration through third-party
certification, and the practice of artifact badging in computing conferences
[47]. Each level answers a different question about who verified the figure.
Conformance is cumulative.

**Table 1.** Conformance levels.

| | Level 1 — Declared | Level 2 — Verified | Level 3 — Attested |
|---|---|---|---|
| Requirements | all MUST | all MUST and SHOULD | all MUST and SHOULD |
| Evidence | public claim with the components of §3.4 | complete evidence package, recomputable by a third party | evidence package plus external attestation |
| Verified by | first party | first party, reproducibly | body independent of the claimant and of the maintainer |

An implementation is BRGEO-1 Level 1 (Declared) conformant if it satisfies all
MUST level requirements and publishes a conformance claim containing the
components listed in §3.4. It is Level 2 (Verified) conformant if it further
satisfies all SHOULD level requirements and publishes an evidence package from
which an independent party can recompute the reported values. It is Level 3
(Attested) conformant if it meets Level 2 and holds a valid attestation issued
by a body independent of both the claimant and the maintainer of this
specification.

It is NOT RECOMMENDED that Level 3 be required as a general procurement policy,
since third-party attestation is not attainable at reasonable cost for every
class of measurement subject. A level scheme whose top rung is affordable only
to large firms becomes a barrier to entry, which is the opposite of what an
open measurement standard is for.

### 3.4 Divisions

Orthogonal to level, and adapted from the divisions used in machine learning
performance benchmarking, every measurement declares a division.

**Closed.** Window, cohort, battery, panel, generation configuration and
matching rule take the values fixed by the specification or by a published
profile. Closed figures are comparable across claimants.

**Open.** Any parameter varies from the profile, with the deviation documented.
Open figures are comparable neither with each other nor with Closed figures,
and MUST NOT be presented as though they were.

A conformance claim names the level, the division, the protocol version, and
the six parameter values.

## 4. Reference instantiation

The values below are what our own longitudinal study uses. They are calibration, not specification: another adopter conforms with different values, provided they are declared.

**Table 2.** Reference instantiation of the six parameters.

| Parameter | Reference value |
|---|---|
| P1 Window | 200 characters, uniform across the panel |
| P2 Cohort | 127 entities: 79 Brazilian firms, 32 international anchors, 16 fictitious decoys, across four verticals |
| P3 Battery | 192 canonical queries (4 verticals × 6 categories × 2 languages × 2 query types × 2 temporal frames) plus 64 adversarial probes |
| P4 Panel | 6 engines, versions pinned per observation (Table 3) |
| P5 Generation | temperature 0.0; output cap 500–800 tokens by provider; reasoning disabled or minimised where the provider exposes the control; system prompt published |
| P6 Matching | word-boundary matching with NFKD dual-pass normalisation, alias table, ambiguity guards requiring canonical form, and exclusion contexts |

**Table 3.** Engine panel with pinned model versions.

| Engine | Model version | Class | Active |
|---|---|---|---|
| ChatGPT | `gpt-4o-mini-2024-07-18` | parametric | full series |
| Claude | `claude-haiku-4-5-20251001` | parametric | full series |
| Gemini | `gemini-2.5-pro`, then `gemini-2.5-flash` | parametric | boundary 2026-06-17 |
| Groq | `llama-3.3-70b-versatile` | parametric, open weights | to 2026-08-16 |
| Grok | `grok-4.6` | parametric | from 2026-08-23 |
| Perplexity | `sonar` | retrieval-augmented | full series |

The panel holds six engines across the series but never six simultaneously: Groq and Grok occupy one slot in successive periods (§7.1). Analyses spanning that boundary must stratify or truncate.

Cohort construction follows P2: tiers stratified with at least three long-tail firms per vertical, seven Brazilian states represented, legal status annotated so a model naming a firm in judicial recovery is not pooled with one naming an active firm, and firms founded after 2020 deliberately included to probe the awareness gap of models whose pre-training predates them. Each decoy was verified as non-existent against the Brazilian federal tax registry, mapping services and court records before inclusion. §11 notes the limitation of that verification.

Collection runs twice daily. The unit of observation is one (query, engine, run) triple. Responses are cached by content hash with an eight-hour time-to-live, shorter than the twelve-hour interval between runs, so no observation in the series is served from cache.

**Why a Brazilian instantiation.** Portuguese-language measurement exercises the instrument against three conditions that English-first tooling does not anticipate: brand names colliding with ordinary words, diacritics rendered inconsistently across languages, and market leaders postdating the pre-training cutoff of deployed models. None of these is peculiar to Brazil. Lexical collision between a brand and a function word occurs in any language — *Orange*, *Free*, *Next*, *Three*, *Ideal*, *Post*, *Meta* — and is the failure mode most likely to inflate a naive citation count. A protocol validated where all three conditions hold simultaneously has been tested under harder conditions than one calibrated on English alone. The battery is half English precisely so that a Brazilian result can be checked against a non-Brazilian baseline within the same instrument.

## 5. The observation window

### 5.1 The parameter

Entity extraction runs over a string. That string is not the model's answer; it is whatever the pipeline retained. Its length is the observation window.

The parameter has a substantive reading. A narrow window measures *head-of-response citation*: whether the entity appears in the opening a reader sees before deciding whether to continue. A full window measures *whole-response citation*. Either is defensible; leaving the choice implicit is not, because the resulting figure cannot be compared with any other.

### 5.2 How the asymmetry arose, and why nothing detected it

In five of six client adapters the stored extraction string was truncated at 200 characters. In the sixth the full response was stored, up to 2,502 characters. The truncation was a property of the client rather than of the measurement design, and was therefore invisible to any check operating on the stored field.

No test detected this, because every test asserted on the field and the field was populated in both cases. No validator detected it, because both values are well-formed strings of plausible length. Daily health checks confirmed that all six engines produced rows, that the language split held at 50/50, and that probes were marked — all true. A functional test suite covering the collection path passed in full.

Detection came from a distributional check rather than a functional one.

**Table 4.** Stored response length by engine, full series.

| Engine | n | Mean | Min | Max | Share at exactly 200 |
|---|---:|---:|---:|---:|---:|
| ChatGPT | 19,328 | 200.0 | 200 | 200 | 100.0% |
| Claude | 19,162 | 200.0 | 200 | 200 | 100.0% |
| Groq | 18,304 | 199.8 | 74 | 200 | 99.8% |
| Grok | 462 | 200.0 | 187 | 200 | 99.6% |
| Gemini | 18,794 | 197.0 | 87 | 200 | 94.8% |
| Perplexity | 7,436 | 687.2 | 198 | 2,502 | 0.0% |

A variable whose maximum equals its minimum across 19,328 observations is not measuring anything; it is reporting a boundary. Arms falling marginally short of 200 are those that sometimes answered in fewer characters than the ceiling, which is the signature of truncation rather than of a length distribution.

This is why P1 is a conformance requirement rather than a recommendation. The window is normally not a design decision at all: it is an incidental consequence of how a provider adapter was written, often for reasons of cost or log volume, and it therefore varies exactly where studies are least likely to look — between providers, which is where the comparison lives.

### 5.3 Magnitude

Re-running extraction over the series under a uniform 200-character window gives Table 5. Counts are canonical queries only; the adversarial stratum is excluded.

**Table 5.** Citation rate as collected and under a uniform window. Series 2026-04-23 to 2026-08-31, 50 days, 66,399 canonical observations.

| Engine | n | As collected | Uniform window | Δ | Rows truncated |
|---|---:|---:|---:|---:|---:|
| ChatGPT | 14,976 | 17.2% | 17.2% | +0.0 pp | 0 |
| Claude | 14,842 | 25.8% | 25.8% | +0.0 pp | 0 |
| Gemini | 14,587 | 1.8% | 1.8% | +0.0 pp | 0 |
| Groq | 14,208 | 8.5% | 8.5% | +0.0 pp | 0 |
| Grok | 350 | 32.3% | 32.3% | +0.0 pp | 0 |
| **Perplexity** | **7,436** | **75.7%** | **51.9%** | **−23.8 pp** | **7,435** |

The five zero deltas are a sanity check rather than an independent verification, and we state this because we initially claimed otherwise. For an arm whose stored text is already 200 characters, applying a 200-character window is the identity operation, so the zero is guaranteed by construction. Its residual value is confirming that re-extraction is deterministic and that the cohort did not change between runs.

The effect is large enough to reverse an interpretation. At 75.7% the retrieval-augmented engine appears categorically different from the parametric arms, roughly three times the rate of the closest competitor. At 51.9% it remains highest but sits within the same family.

### 5.4 The mechanism is unresolved, and the architectural account is wrong

We initially advanced a discourse-structure account: retrieval-augmented engines compose after fetching sources, open with framing prose, and therefore defer naming, so a narrow window understates them specifically. Two analyses contradict this.

**Relative position.** Normalising the first-mention offset by the length of the text actually observed reverses the ordering.

**Table 6.** First-mention offset, absolute and relative to observed text. Canonical observations with a citation.

| Engine | n | Absolute offset | Observed length | Relative, mean | Relative, median |
|---|---:|---:|---:|---:|---:|
| Grok | 113 | 33 | 200 | 0.164 | 0.000 |
| Perplexity | 5,631 | 158 | 662 | 0.228 | 0.169 |
| Gemini | 265 | 97 | 197 | 0.493 | 0.375 |
| Groq | 1,210 | 108 | 200 | 0.539 | 0.530 |
| ChatGPT | 2,571 | 116 | 200 | 0.582 | 0.600 |
| Claude | 3,823 | 124 | 200 | 0.621 | 0.645 |

If mentions were uniformly distributed along a Perplexity response, the fraction beyond character 200 would be 1 − 200/662 = 69.8%. The observed fraction is 28.8%. The retrieval-augmented arm concentrates first mentions in the opening of its own response.

The parametric denominators are censored at 200, so the relative values of 0.49 to 0.62 are upper bounds and the reversal cannot be asserted as established. That is the point: **the direction of the window bias is not identified by data collected under an asymmetric window.** The simpler mechanism, and the one consistent with the evidence, is quantity of text read rather than discourse structure — reading 662 characters instead of 200 finds more mentions, and would find more in any engine whose full response had been retained. That reading makes the finding more general, not less.

**Susceptibility tracks response style, not architecture.** The engine most affected by a narrow window is parametric.

**Table 7.** Share of responses opening with preamble, against citation rate. Preamble is matched at the start of the response against greetings, hedges and question restatements ("Excellent question", "It is difficult to predict", "As a large language model"); the criterion is published with the figure because it is itself a measurement rule.

| Engine | n | Opens with preamble | Citation rate |
|---|---:|---:|---:|
| Gemini | 14,587 | 79.6% | 1.8% |
| Perplexity | 7,436 | 9.2% | 75.7% |
| Grok | 350 | 4.0% | 32.3% |
| ChatGPT | 14,976 | 2.1% | 17.2% |
| Groq | 14,208 | 1.1% | 8.5% |
| Claude | 14,842 | 0.0% | 25.8% |

Gemini spends the window on preamble, so entities rarely appear within the observed text. Its 1.8% is not "Gemini cites little"; it is "Gemini cites little within the first 200 characters", and what it would cite over a full response is unknown because that text was never retained. A control supports this reading: among Gemini observations that do contain a citation, 23.0% of first mentions fall beyond character 150, comparable to ChatGPT at 24.5% and below Claude at 36.1%. When Gemini reaches a name inside the window, its distribution is unremarkable; what is remarkable is how rarely it gets there.

The engine with the longest preamble is parametric and the retrieval-augmented engine has little. Susceptibility to the window is therefore a property of the model, not of its architecture, and is not predictable from the class. That is the strongest argument for declaring the parameter: no rule of thumb allows a reader to estimate the effect without measuring it.

### 5.5 What BRGEO-1 requires

- **Uniformity.** One window, applied identically to every engine.
- **Declaration.** The value published with the figure.
- **Retention of the full response**, so a third party can re-extract. Until August 2026 the full response was not retained in our pipeline, which meant none of 83,486 observations could be independently reproduced. This was the more serious of the two window defects: an asymmetric window is correctable because the truncated string is still the string the extractor saw, but no amount of care recovers text that was never stored.
- **Sensitivity reporting.** Where the full response exists, the headline figure reported under both windows, per engine.

## 6. Calibration decoys and the refusal taxonomy

### 6.1 Decoys as instrument

Sixteen fictitious entities, verified as non-existent before collection, give the instrument an empirical false-positive floor from within the run that produced the rate. Adversarial probes name a decoy and ask about it directly, forcing a decision: describe an entity that does not exist, or decline.

### 6.2 The refusal problem

Our original implementation flagged a hallucination whenever the decoy name occurred in the response. This is wrong in a specific way: the probe places the name in the prompt, so any response engaging with the question at all — including a refusal — contains it. That 97% of probe responses were flagged is itself evidence that the marker was detecting the prompt rather than the answer.

Of 16,579 responses flagged as hallucinations, 11,195 (67.5%) carry an explicit refusal marker, including responses stating that the named institution is not a real or registered financial institution in Brazil. A stricter criterion, removing alternants capable of matching attribute negation inside a fabricated description, yields 11,100 (67.0%); only 95 cases (0.6%) matched on the weak alternant alone, and inspection showed those to be genuine refusals. The estimate is stable to that variation. We do not claim it is a lower bound, because that would require human annotation we have not performed.

BRGEO-1 therefore specifies a three-way outcome:

1. **Ontological refusal** — the model states the entity does not exist.
2. **Epistemic refusal** — the model states it lacks information, typically citing a training cutoff. Correct in effect, weaker in kind.
3. **Fabrication** — the model describes products, history or positioning for an entity that has none.

Only the third is a hallucination. A protocol pooling all three reports a false-positive rate near 97% where the defensible figure is a fraction of that.

**This taxonomy is proposed, not validated.** We report no inter-annotator agreement, no human-labelled sample, and no confusion matrix of the automatic classifier against a gold standard, and the distribution across the three categories is not yet measured. Estimating fabrication as the complement of a refusal detector is inference of the same kind this paper criticises elsewhere: the residual contains refusals phrased outside the detector's vocabulary, empty responses, clarifying questions, and responses about real homonyms. Fabrication requires positive detection of invented verifiable attributes. §11 lists this as the principal open item in the specification.

### 6.3 Probe coverage

Our probe stratum excluded the retrieval-augmented engine entirely, because provider routing sent it a subset of query categories that did not include the calibration category. The exclusion removed the most informative case: an engine that searches before answering has evidence a parametric model does not, and whether it uses that evidence to refuse is the question worth asking. BRGEO-1 requires probes to cover every engine in the panel. Figures in §6.2 therefore describe five parametric arms.

## 7. Instrument drift and honest missingness

### 7.1 Series events

An instrument that changes mid-series and reports a single pooled figure reports an average over several instruments. BRGEO-1 requires each change to be dated, recorded and carried into analysis as a stratification boundary.

**Table 8.** Series events, reference instantiation.

| Date | Arm | Change class | Analytic consequence |
|---|---|---|---|
| 2026-06-17 | Gemini | model version and reasoning budget | pre and post not comparable within arm |
| 2026-08-19 | slot 5 | engine replaced (Groq to Grok) | not a continuous series |
| 2026-08-31 | Perplexity | window unified | affects this arm only |
| 2026-08-31 | Grok | reasoning effort reduced | separate stratum |

A boundary affecting fewer observations than a declared threshold is dropped for that arm rather than stratified; in the last case 206 of roughly 18,000 per-arm observations made discarding the cheaper option.

### 7.2 The missingness ledger

Longitudinal collection against commercial APIs fails: providers return errors, credit is exhausted, payload validation changes without notice. A study imputing those gaps, or reporting only the days that worked, misrepresents its own series.

BRGEO-1 imputes nothing. As of this writing the series holds 50 days with data against 324 aborted runs, and we publish that ratio because it is the honest denominator for any claim about temporal stability. Analysis weights days by coverage with a random intercept per collection date; partial days enter a sensitivity analysis reported with and without them.

Three failure modes are worth naming because an adopter will meet them, and all three produced green pipelines: provider credit exhaustion, a job timeout caused by one engine's default reasoning consuming 72% of the run, and a restore path that had been silently inert for two months because it depended on configuration never created. The generalisable lesson is that a degradation path which does not announce itself is indistinguishable from one that does not exist.

## 8. The reporting index, and evidence against leaning on it

### 8.1 Definition

Reporting needs a headline figure. Let $E$ be the cohort, $M$ the engine panel, $w$ the declared window, and $\mu$ the matching rule of P6, returning the offset of the first mention of entity $e$ in a response or $\infty$ if absent. For entity $e$:

- **Coverage** $C_w(e)$: the share of panel observations in which $e$ is named within the window.
- **Prominence** $P_w(e)$: one minus the offset of the first mention divided by $w$, averaged over observations where $e$ appears. Normalisation is by the declared window, not by response length, so the component remains comparable across engines.
- **Breadth** $B_w(e)$: the share of panel engines naming $e$ at least once.

The index is their geometric mean:

$$\mathrm{GCI}_w(e) = \left( C_w(e) \cdot P_w(e) \cdot B_w(e) \right)^{1/3}$$

The geometric mean is invariant to rescaling of the components and penalises imbalance between them more than the arithmetic mean. It is sometimes described as non-compensatory; that is accurate only in the limit, since it vanishes solely when a component is exactly zero, and an entity absent from one engine of six retains $B = 5/6$. The penalty is gradual, not absolute.

Panel membership requires a minimum observation count, declared as a parameter rather than left in the implementation. §11 records that our reference implementation currently applies a threshold that excludes a live arm and retains a retired one, which is a defect of the implementation against this specification.

BRGEO-1 requires the three components to be published alongside the index.

### 8.2 What the index does

Across 66 entities in four verticals, rank correlation between the composite and simple coverage is high, and stable under subsetting.

**Table 9.** Spearman rank correlation, composite against simple coverage.

| Subset | ρ | n |
|---|---:|---:|
| All entities | 0.982 | 66 |
| Excluding each vertical's leader | 0.978 | 62 |
| Coverage between 0.1% and 5% | 0.945 | 42 |
| Coverage below 1% | 0.960 | 44 |

Entities are those cited at least once; the 61 never-cited entities are excluded because Spearman is undefined over a mass of ties at zero, and this is selection on the outcome.

That correlation is not evidence that aggregation is inconsequential. It reflects the composite's variance being dominated by one component.

**Table 10.** Variance decomposition of log GCI. Contribution is $\mathrm{Cov}(\log X, \log \mathrm{GCI}) / (3 \cdot \mathrm{Var}(\log \mathrm{GCI}))$, summing to unity.

| Component | Var(log) | Contribution |
|---|---:|---:|
| Coverage | 4.490 | 74.7% |
| Breadth | 0.306 | 16.9% |
| Prominence | 0.198 | 8.4% |

Coverage varies by orders of magnitude while prominence and breadth are confined to narrow ranges. The geometric mean inherits that dominance by construction.

### 8.3 Aggregation is unstable across defensible choices

Comparing the composite against one of its own components does not test whether aggregation matters. The test is against alternative aggregations of the same components.

**Table 11.** Spearman rank correlation between aggregations, n = 66. Weighted uses 0.6·C + 0.25·P + 0.15·B, an arbitrary choice included to show that a plausible weighting diverges.

| | Geometric | Arithmetic | Harmonic | Weighted |
|---|---:|---:|---:|---:|
| Geometric (GCI) | 1.000 | 0.816 | 0.983 | 0.787 |
| Arithmetic | 0.816 | 1.000 | 0.734 | 0.984 |
| Harmonic | 0.983 | 0.734 | 1.000 | 0.706 |
| Weighted | 0.787 | 0.984 | 0.706 | 1.000 |

Against simple coverage the four give 0.982, 0.728, 1.000 and 0.700 respectively. The harmonic mean reproduces the coverage ordering exactly, because it is dominated by the smallest component and coverage is smallest by orders of magnitude. Aggregations not dominated by the minimum diverge substantially — from coverage and from each other, with correlation falling to 0.706.

Rank displacement between the composite and coverage has median 2, ninetieth percentile 6, and maximum 10 positions out of 66; only 7 entities retain their exact rank.

### 8.4 What follows

The aggregation formula is unstable across reasonable choices, and the data offer no principled basis for preferring one: the alternatives differ mainly in how much weight they give to components that barely vary. The observation window, by contrast, moves one engine by 23.8 points through a mechanism that can be investigated and, as §5.4 shows, corrected when the initial account proves wrong.

A standard should spend its authority where disagreement is both large and resolvable. BRGEO-1 therefore constrains the conditions of observation, requires the components to be published alongside any index, and treats the index as a reporting convenience subordinate to them.

This also addresses the standard objection to composite indicators, that aggregation is arbitrary [44]. It is arbitrary here. We measured how arbitrary, and report it, which is the sort of thing worth establishing before an industry writes contracts against a number.

## 9. Analysis plan

The confirmatory window closes on 28 September 2026. This paper reports no confirmatory results; the plan is recorded here in advance of them. It is published in the project repository and is not registered with an independent third party, which we state plainly rather than describe as pre-registration.

**H1 — vertical asymmetry.** Citation rates differ across verticals. Likelihood-ratio test on the vertical fixed effect in a mixed-effects logistic model with random intercepts per query and per collection date. Minimum meaningful effect: Cramér's V ≥ 0.15.

**H2 — false-positive baseline.** Fabrication rate on fictitious entities, using the §6.2 taxonomy with human-validated labels, differs across engines. Requires probe coverage of all arms and the annotation study of §11.

**H3 — inter-engine agreement.** Fleiss kappa on the rectangular query × engine panel, per vertical.

**H4 — temporal stability.** At least one engine shows a non-stationary citation rate, as a significant slope on day index after false-discovery-rate correction.

**H5 — directive inflation.** Directive queries yield higher citation rates than exploratory ones, with Cohen's h as effect size.

**H6 — window sensitivity.** The gap between head-of-response and whole-response citation varies across engines and is predicted by preamble share rather than by engine class. This is testable only because full responses are now retained, and it restates §5.4 as a proposition rather than a finding.

Multiplicity is handled by Benjamini-Hochberg; standard errors are cluster-robust for repeated queries; cells below 30 observations are reported descriptively. Anything not listed here is labelled exploratory and reported without inferential claims.

## 10. Governance

**Custody.** Brasil GEO maintains the specification and the reference implementation. Custody means publishing changes, dating them, and keeping prior versions resolvable. No permission is required to implement BRGEO-1 or to state conformance with it.

**Licensing.** The specification is published under CC BY 4.0 and the reference implementation under Apache-2.0, which carries an explicit patent grant. Use of the identifier to describe a conforming measurement requires no permission and confers no endorsement.

**Versioning.** A change altering what a conforming figure means increments the major version; a clarification that does not increments the minor. A figure cites the version under which it was measured.

**Scope.** BRGEO-1 covers entity citation measurement. Adjacent problems take their own numbers rather than being folded into this one, so that an adopter may conform to one without implementing all.

**What conformance does not yet establish.** Conformance is self-declared, and a self-declared statement reproduces the unverifiable claim this paper opens by criticising. Two mechanisms would replace assertion with evidence, and neither exists yet: a conformance test suite of reference responses with expected figures under declared parameters, against which any implementation can be run; and an inter-implementation reproducibility exercise in the sense of ISO 5725, in which two independent implementations process the same stored responses and the discrepancy is reported. Until the second exists, the central proposition of this paper — that the protocol produces comparability — has no direct evidence in its favour. We state this as the specification's principal limitation rather than as future work.

## 11. Threats to validity

**Elicitation mode, unmeasured.** We send plain natural-language prompts and extract entities post hoc, which is closer to what a user sees than instructing models to return structured lists. We have not measured how far the two modes diverge. If that difference approaches the magnitude of the window effect, the specification fixes six parameters while a seventh of unknown size varies freely. A pilot comparison is the highest-priority open item.

**Refusal taxonomy, unvalidated.** No inter-annotator agreement, no gold standard, no measured distribution across the three categories (§6.2).

**Decoy verification, jurisdictionally narrow.** Decoys were verified against Brazilian registries. Several are generic constructions with plausible international homonyms; a model correctly describing a real firm of the same name in another country would be counted as fabricating. Per-decoy reporting would separate fabrication from homonymy and has not been done.

**Reference implementation diverges from the specification.** The panel membership threshold sits in code rather than in the declared parameters, and at current values excludes a live arm while retaining a retired one. The figures in this paper are computed on a panel that includes Groq and excludes Grok.

**Window choice.** Head-of-response citation is defensible but is a choice; figures are reported under both windows for that reason.

**Index.** §8.3 is a limitation reported as a finding. Whether the composite separates more in a less concentrated market is untested.

**Unequal sampling.** Provider routing sends the retrieval-augmented arm roughly half the canonical battery on cost grounds. Per-cell power is correspondingly lower, reported rather than corrected by weighting.

**Missingness is not ignorable.** Gaps cluster around provider credit exhaustion, which correlates with cost, which correlates with response length, which §5 establishes correlates with citation. Coverage weighting corrects data missing at random and does not address this mechanism; bounds analysis is required and has not been performed.

**Market, language and model tier.** The cohort is Brazilian and the battery bilingual; vertical asymmetries may reflect corpus composition rather than model properties, with the international anchors as an internal check rather than a substitute for replication. The panel uses small, low-cost models, which is what makes twice-daily collection affordable; flagship models may behave differently.

**An unexplained arm.** Gemini's 1.8% citation rate is explained by preamble (§5.4) but the explanation is post hoc, and whether preamble share is stable for that model over time has not been tested.

## 12. Discussion

The finding we would ask a reader to carry away is not that our pipeline had a defect. It is that the defect was invisible to every check the pipeline ran on itself, and the checks were not weak. Six engines produced rows daily. The language split held at 50/50. Probes were marked. Response hashes varied. A full functional suite passed. None of it could detect that one arm was measured on a different amount of text than the others, because none of it asked what the extractor was reading.

Defects of this shape are likely common in citation measurement, for a structural reason: the window is usually not a design decision at all, and it varies between providers, which is where the comparison lives.

The second lesson concerns our own explanation. We advanced a plausible mechanism — retrieval-augmented engines defer naming — and the data refuted it once the offset was normalised. The engine most damaged by a narrow window turned out to be parametric, and the property that predicts damage is response style, which no architectural taxonomy exposes. A field this young will generate many such accounts, and the discipline worth adopting is to state them as propositions and test them, which is why §9 restates the claim as H6 rather than reporting it as a result.

For practice, the implication is that a citation rate reported without a declared window is not comparable to another, and the magnitude of that incomparability here is 23.8 percentage points on one engine. Reporting practice should treat the window as it treats the model version.

We publish the protocol ahead of confirmatory results so the analysis plan precedes the estimates, and so the window is on record as a declared parameter rather than as something settled after observing which value produced the more interesting finding.

## 13. Conclusion

BRGEO-1 specifies six parameters, three conformance levels and a missingness ledger for measuring entity citation in generative engines. Its empirical contribution is the demonstration that one of those parameters, the observation window, moves a headline figure by 23.8 percentage points, that its effect is not predictable from engine architecture, and that our own initial account of the mechanism did not survive normalisation.

The specification's principal gap is that conformance remains self-declared. A conformance test suite and an inter-implementation reproducibility exercise are the next two pieces of work, and until they exist the claim that the protocol produces comparability is a design argument rather than a measured result.

## CRediT authorship contribution statement

**Alexandre Caramaschi:** Conceptualization, Methodology, Software, Formal
analysis, Investigation, Data curation, Writing – original draft, Writing –
review and editing, Visualization, Project administration.

## Declaration of competing interest

The author takes a deliberately expansive view of competing interests.

Alexandre Caramaschi is the founder of Brasil GEO, the organisation that acts
as custodian and maintainer of the BRGEO-1 specification described in this
paper. Brasil GEO provides commercial advisory and audit services in the domain
that the specification measures, and would therefore benefit from the adoption
of BRGEO-1. He is also Chief Strategy Officer of Nuvini (Nasdaq: NVNI); this
work is conducted in his capacity at Brasil GEO and does not represent a
position of Nuvini.

Brasil GEO holds no patent or licensing claim over the specification, which is
released under CC BY 4.0 with a reference implementation under Apache-2.0 and
is free to implement by any party without royalty.

Three features constrain this interest structurally rather than by declaration
alone. Level 3 attestation (§3.3) may be issued only by a body independent of
both the claimant and the maintainer, so the custodian cannot certify its own
clients. The reference implementation, cohort and query battery are published
under an open licence, so no party controls the measurement instrument. And the
cohort was fixed before collection began and contains no entity selected for a
commercial relationship.

No external party had any role in the design of the specification, the
selection of the cohort, the analysis of results, or the decision to submit
this article.

## Acknowledgements

The author thanks the reviewers of the internal audit that identified the
window asymmetry reported in §5 and the aggregation defect reported in §8.

## Declaration of generative AI and AI-assisted technologies in the manuscript preparation process

During the preparation of this work the author used large language model
assistance to draft and revise prose, to write analysis scripts, and to search
and verify bibliographic records. Every quantitative result reported here was
computed from the primary data by scripts published in the project repository,
and every reference was checked against its publisher record. After using these
tools the author reviewed and edited the content and takes full responsibility
for the content of the published article.

## Funding

This research did not receive any specific grant from funding agencies in the
public, commercial, or not-for-profit sectors. Application programming
interface costs were borne by the author.

## Ethics

The study queries commercial application programming interfaces under their
published terms of service, collects no personal data, and involves no human
subjects.

## Data availability

The specification, reference implementation, cohort definition, query battery
and analysis scripts are openly available at
`github.com/alexandrebrt14-sys/papers`. A versioned dataset snapshot carrying a
persistent identifier is deposited at the close of the confirmatory window; the
version identifier rather than the concept identifier is cited, so that figures
in this paper remain recomputable from the exact artefacts that produced them.

## References

[1] Aggarwal, P., Murahari, V., Rajpurohit, T., Kalyan, A., Narasimhan, K., Deshpande, A., 2024. GEO: Generative Engine Optimization, in: Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining, pp. 5–16. https://doi.org/10.1145/3637528.3671900

[2] Bagga, P.S., Farias, V.F., Korkotashvili, T., Peng, T., Wu, Y., 2025. E-GEO: A Testbed for Generative Engine Optimization in E-Commerce. arXiv:2511.20867.

[3] Yu, J., Yang, M., Ding, Y., Sato, H., 2026. Structural Feature Engineering for Generative Engine Optimization: How Content Structure Shapes Citation Behavior. arXiv:2603.29979.

[4] Sielinski, R., 2026. Quantifying Uncertainty in AI Visibility: A Statistical Framework for Generative Search Measurement. arXiv:2603.08924.

[5] Schulte, J., Bleeker, M., Kaufmann, P., 2026. Don't Measure Once: Measuring Visibility in AI Search (GEO). arXiv:2604.07585.

[6] Zhang, K., He, X., Yao, J., 2026. From Citation Selection to Citation Absorption: A Measurement Framework for Generative Engine Optimization Across AI Search Platforms. arXiv:2604.25707.

[7] Varga, Z., 2026. Per-Entity Bias Mapping for AI Visibility: Why Brand Mentions Require Entity-Specific Calibration. arXiv:2606.21595.

[8] Kumar, P., 2026. Generative Engine Optimization at Scale: Measuring Brand Visibility Across AI Search Engines. arXiv:2606.20065.

[9] Martinez, O., 2026. Optimizing Visibility in Generative Engines: A Critical Survey of Generative Engine Optimization (2023–2026). arXiv:2607.14035.

[10] Rashkin, H., Nikolaev, V., Lamm, M., Aroyo, L., Collins, M., Das, D., Petrov, S., Tomar, G.S., Turc, I., Reitter, D., 2023. Measuring Attribution in Natural Language Generation Models. Computational Linguistics 49 (4), 777–840. https://doi.org/10.1162/coli_a_00486

[11] Liu, N.F., Zhang, T., Liang, P., 2023. Evaluating Verifiability in Generative Search Engines, in: Findings of the Association for Computational Linguistics: EMNLP 2023, pp. 7001–7025. https://doi.org/10.18653/v1/2023.findings-emnlp.467

[12] Gao, T., Yen, H., Yu, J., Chen, D., 2023. Enabling Large Language Models to Generate Text with Citations, in: Proceedings of EMNLP 2023, pp. 6465–6488. https://doi.org/10.18653/v1/2023.emnlp-main.398

[13] Venkit, P.N., Laban, P., Zhou, Y., Mao, Y., Wu, C.-S., 2024. Search Engines in an AI Era: The False Promise of Factual and Verifiable Source-Cited Responses. arXiv:2410.22349.

[14] Venkit, P.N., Laban, P., Zhou, Y., Huang, K.-H., Mao, Y., Wu, C.-S., 2025. DeepTRACE: Auditing Deep Research AI Systems for Tracking Reliability Across Citations and Evidence. arXiv:2509.04499.

[15] Jung, H., Gonen, H., 2026. PhantomBench: Benchmarking the Non-existential Threat of Language Models. arXiv:2606.11105.

[16] Bang, Y., Ji, Z., Schelten, A., Hartshorn, A., Fowler, T., Zhang, C., Cancedda, N., Fung, P., 2025. HalluLens: LLM Hallucination Benchmark, in: Proceedings of ACL 2025 (Volume 1: Long Papers), pp. 24128–24156. https://doi.org/10.18653/v1/2025.acl-long.1176

[17] Kirichenko, P., Ibrahim, M., Chaudhuri, K., Bell, S.J., 2025. AbstentionBench: Reasoning LLMs Fail on Unanswerable Questions. arXiv:2506.09038.

[18] Pan, W., Xu, J., Chen, Q., Dong, J., Qin, L., Li, X., Yu, H., Jia, X., 2026. Can LLMs Refuse Questions They Do Not Know? Measuring Knowledge-Aware Refusal in Factual Tasks. arXiv:2510.01782.

[19] Ji, Z., Lee, N., Frieske, R., Yu, T., Su, D., Xu, Y., Ishii, E., Bang, Y., Madotto, A., Fung, P., 2023. Survey of Hallucination in Natural Language Generation. ACM Computing Surveys 55 (12), 1–38. https://doi.org/10.1145/3571730

[20] Huang, L., Yu, W., Ma, W., Zhong, W., Feng, Z., Wang, H., Chen, Q., Peng, W., Feng, X., Qin, B., Liu, T., 2025. A Survey on Hallucination in Large Language Models: Principles, Taxonomy, Challenges, and Open Questions. ACM Transactions on Information Systems. https://doi.org/10.1145/3703155

[21] Jacobs, A.Z., Wallach, H., 2021. Measurement and Fairness, in: Proceedings of the 2021 ACM Conference on Fairness, Accountability, and Transparency, pp. 375–385. https://doi.org/10.1145/3442188.3445901

[22] Raji, I.D., Denton, E., Bender, E.M., Hanna, A., Paullada, A., 2021. AI and the Everything in the Whole Wide World Benchmark, in: Proceedings of the NeurIPS Track on Datasets and Benchmarks 1.

[23] Bowman, S.R., Dahl, G., 2021. What Will it Take to Fix Benchmarking in Natural Language Understanding?, in: Proceedings of NAACL-HLT 2021, pp. 4843–4855. https://doi.org/10.18653/v1/2021.naacl-main.385

[24] Reiter, E., 2018. A Structured Review of the Validity of BLEU. Computational Linguistics 44 (3), 393–401. https://doi.org/10.1162/coli_a_00322

[25] Bean, A.M., Kearns, R.O., Romanou, A., Hafner, F.S., Mayne, H., et al., 2025. Measuring what Matters: Construct Validity in Large Language Model Benchmarks, in: Proceedings of the NeurIPS 2025 Track on Datasets and Benchmarks. arXiv:2511.04703.

[26] Hochlehnert, A., Bhatnagar, H., Udandarao, V., Albanie, S., Prabhu, A., Bethge, M., 2025. A Sober Look at Progress in Language Model Reasoning: Pitfalls and Paths to Reproducibility, in: Proceedings of COLM 2025. arXiv:2504.07086.

[27] Encarnación, R., Behzad, T., Lurie, E., Metaxa, D., 2026. What Current AI Benchmarks Leave Unmeasured: Modality, Search, Citations, and Implications (for Safety Evaluations). arXiv:2608.06202.

[28] Breuer, T., Keller, J., Schaer, P., 2022. ir_metadata: An Extensible Metadata Schema for IR Experiments, in: Proceedings of SIGIR 2022, pp. 3078–3089. https://doi.org/10.1145/3477495.3531738

[29] Ferro, N., Fuhr, N., Järvelin, K., Kando, N., Lippold, M., Zobel, J., 2016. Increasing Reproducibility in IR: Findings from the Dagstuhl Seminar on Reproducibility of Data-Oriented Experiments in e-Science. ACM SIGIR Forum 50 (1), 68–82. https://doi.org/10.1145/2964797.2964808

[30] Ghosh, A., Reuel, A., Chim, J., Kennedy, W.M., Yadav, S., Mickel, J., et al., 2026. Evaluation Cards: An Interpretive Layer for AI Evaluation Reporting. arXiv:2606.09809.

[31] Mitchell, M., Wu, S., Zaldivar, A., Barnes, P., Vasserman, L., Hutchinson, B., Spitzer, E., Raji, I.D., Gebru, T., 2019. Model Cards for Model Reporting, in: Proceedings of the Conference on Fairness, Accountability, and Transparency, pp. 220–229. https://doi.org/10.1145/3287560.3287596

[32] Gebru, T., Morgenstern, J., Vecchione, B., Vaughan, J.W., Wallach, H., Daumé III, H., Crawford, K., 2021. Datasheets for Datasets. Communications of the ACM 64 (12), 86–92. https://doi.org/10.1145/3458723

[33] Metaxa, D., Park, J.S., Robertson, R.E., Karahalios, K., Wilson, C., Hancock, J.T., Sandvig, C., 2021. Auditing Algorithms: Understanding Algorithmic Systems from the Outside In. Foundations and Trends in Human-Computer Interaction 14 (4), 272–344. https://doi.org/10.1561/1100000083

[34] Liang, P., Bommasani, R., Lee, T., Tsipras, D., Soylu, D., Yasunaga, M., et al., 2023. Holistic Evaluation of Language Models. Transactions on Machine Learning Research. arXiv:2211.09110.

[35] Muennighoff, N., Tazi, N., Magne, L., Reimers, N., 2023. MTEB: Massive Text Embedding Benchmark, in: Proceedings of EACL 2023, pp. 2014–2037. https://doi.org/10.18653/v1/2023.eacl-main.148

[36] Thakur, N., Reimers, N., Rücklé, A., Srivastava, A., Gurevych, I., 2021. BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models, in: Proceedings of the NeurIPS Track on Datasets and Benchmarks 1. arXiv:2104.08663.

[37] Enevoldsen, K., Chung, I., Kerboua, I., Kardos, M., Mathur, A., Stap, D., et al., 2025. MMTEB: Massive Multilingual Text Embedding Benchmark, in: Proceedings of ICLR 2025. arXiv:2502.13595.

[38] Craswell, N., Mitra, B., Yilmaz, E., Campos, D., Voorhees, E.M., 2020. Overview of the TREC 2019 Deep Learning Track. arXiv:2003.07820.

[39] Voorhees, E.M., 2000. Variations in relevance judgments and the measurement of retrieval effectiveness. Information Processing & Management 36 (5), 697–716. https://doi.org/10.1016/S0306-4573(00)00010-8

[40] Bailey, P., Moffat, A., Scholer, F., Thomas, P., 2016. UQV100: A Test Collection with Query Variability, in: Proceedings of SIGIR 2016, pp. 725–728. https://doi.org/10.1145/2911451.2914671

[41] Liu, N.F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F., Liang, P., 2024. Lost in the Middle: How Language Models Use Long Contexts. Transactions of the Association for Computational Linguistics 12, 157–173. https://doi.org/10.1162/tacl_a_00638

[42] Guo, X., Vosoughi, S., 2024. Serial Position Effects of Large Language Models. arXiv:2406.15981.

[43] Menschikov, M., Kharitonov, A., Kotyga, M., Porvatov, V., Zhukovskaya, A., Kagramanyan, D., Shvetsov, E., Burnaev, E., 2025. Beyond Early-Token Bias: Model-Specific and Language-Specific Position Effects in Multilingual LLMs. arXiv:2505.16134.

[44] Nardo, M., Saisana, M., Saltelli, A., Tarantola, S., Hoffmann, A., Giovannini, E., 2008. Handbook on Constructing Composite Indicators: Methodology and User Guide. OECD Publishing, Paris. https://doi.org/10.1787/9789264043466-en

[45] Bradner, S., 1997. Key words for use in RFCs to Indicate Requirement Levels. RFC 2119, BCP 14, Internet Engineering Task Force. https://doi.org/10.17487/RFC2119

[46] Leiba, B., 2017. Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words. RFC 8174, BCP 14, Internet Engineering Task Force. https://doi.org/10.17487/RFC8174

[47] Ferro, N., Kelly, D., 2018. SIGIR Initiative to Implement ACM Artifact Review and Badging. ACM SIGIR Forum 52 (1), 4–10. https://doi.org/10.1145/3274784.3274786
