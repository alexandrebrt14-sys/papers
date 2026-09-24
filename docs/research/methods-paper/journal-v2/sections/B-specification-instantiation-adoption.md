# Block B — §3 The BRGEO-1 specification · §4 Reference instantiation · §12 Adopting the protocol

Draft for the journal-length manuscript. Numbers are drawn from `../tables/TABLES.md`, `../tables/NUMBERS.md` and `../stats/S5-window-validity.md` on the database snapshot whose latest `citations.timestamp` is 2026-09-08T19:30:57Z. Citations are by key; the full entry for every key appears at the end of this file.

---

## 3. The BRGEO-1 specification

A citation rate reported without its conditions is a precise measurement of a quantity the reader cannot identify. Metrology names the gap: VIM 2.3 Note 1 requires that the specification of a measurand include a description of the state of the phenomenon carrying the quantity, and VIM 2.27 calls the residual from an incomplete specification definitional uncertainty [JCGM200]. §1.2 sets out the two notes to clause 2.27 and what they cost an interval computed from sample size alone, which estimates a term sitting below a floor the budget never entered.

That is the argument for making the six parameters normative rather than advisory. A recommendation that an implementer may decline leaves the descriptive detail free, and free descriptive detail means every implementation measures a different measurand while publishing the same word. The parameters below are the minimum detail under which two figures refer to the same quantity.

### 3.1 The six declared parameters

*This subsection is normative.*

A figure is measured under BRGEO-1 when all six parameters are fixed before collection, published with the figure, and versioned `[BRGEO1-M-012]`.

**Table B1.** The six declared parameters: what each fixes, what goes wrong when it is left implicit, and what a conforming implementation publishes.

| | Parameter | Failure mode when implicit | Published with the figure |
|---|---|---|---|
| P1 | Observation window | The instrument silently measures head-of-response citation and reports it as whole-response citation, at a cut-off that differs between providers | Window in characters, applied identically to every arm; the recall target it meets |
| P2 | Cohort | The rate has no false-positive floor and no stated detection set, so absence of a name is unreadable | Entity list with tier, legal status and decoys, dated before first collection |
| P3 | Query battery | The battery encodes the author's assumptions about what users ask, and stratum effects load onto engine effects | The full battery with its factorial invariants |
| P4 | Engine panel with pinned versions | A change in the world cannot be separated from a change in the instrument | Model version string recorded on every observation, with the dates of every boundary |
| P5 | Generation configuration | A parameter that moves latency, cost and output length varies without changing the model identifier | Temperature, sampling parameters, seed where available, output caps, reasoning effort, system prompt |
| P6 | Entity matching rule | Two implementations produce different figures from identical responses while both claiming conformance | Matching form, alias table, ambiguity policy, exclusion contexts, boundary policy, and the rate with each dictionary removed |

**P1, the observation window.** Entity extraction runs over a string, and that string is whatever the pipeline retained rather than the model's answer. Its length is the observation window `[BRGEO1-M-001]`, and it MUST be identical across every arm of the panel `[BRGEO1-M-002]`. The parameter carries a substantive reading in either setting: a narrow window measures whether the entity appears in the opening a reader sees before deciding to continue, and a full window measures whether it appears at all. Leaving the choice implicit is the failure, because the window is usually not a design decision. It is an incidental consequence of how a provider adapter was written, for reasons of cost or log volume, and it therefore varies between providers, which is where the comparison lives. The measured magnitude is in §6; the short statement is that on 2,225 canonical observations collected from 2026-09-06 to 2026-09-08, moving from 200 characters to the whole response changed the citation rate by between 22.95 and 55.73 percentage points on five arms, with zero reversals. Position within model output is a measured phenomenon in the recommendation literature [Hou2024; Bito2026; Wadi2026]; what P1 adds is that the instrument's truncation of that output is an unreported measurement parameter, which is a narrower claim and a checkable one.

**P2, the cohort.** The cohort is the set of entities the instrument can detect, fixed before collection with tier stratification, annotated legal status, and fictitious calibration decoys `[BRGEO1-M-003]`. Decoys are required `[BRGEO1-M-004]`: without them the rate has no empirical floor from the run that produced it, and a matcher that fires on ordinary prose is indistinguishable from a model that names firms. An unfixed cohort fails in a second way that the literature has now measured. Brands absent from training corpora have no presence in model answers regardless of quality [Huang2026], and a well-known brand is recommended in every response when product specifications are held identical, with that dominance collapsing under a rating advantage of less than a tenth of a star for a competitor [Chu2026], so a cohort assembled after seeing the answers reports an artefact of its own assembly. Publishing the cohort with a date before first collection is what makes that objection answerable.

**P3, the query battery.** The battery is a factorial design over dimensions known to move citation behaviour, balanced rather than convenience-sampled, and published in full `[BRGEO1-M-005]`. Query language is reported as the largest systematic factor in a crossed variance decomposition of brand answers over 12,933 responses [Zatuchin2026b], and query variability has been treated as a first-class property of a test collection since UQV100 [Bailey2016]. An unbalanced battery does not announce itself: it produces a rate that is a weighted average over strata the reader cannot see, and it makes an engine that was routed a discovery-heavy subset look more generous than one that was not. Publishing the invariants makes a battery checkable by a second party without making two balanced batteries interchangeable, since the four factors this battery balances account for none of the variance between its own prompts, which §9.2 measures and row 23 of Table F1 records.

**P4, the engine panel with pinned versions.** Every engine MUST be identified by an explicit model version string recorded on every observation, with the date of every panel change `[BRGEO1-M-006]`. Providers alter the model behind a stable product name, and the behaviour of a commercial model under one name has been shown to move materially over a few months [Chen2024]. A series recording only the product name cannot separate a change in the world from a change in the instrument, and it also cannot be repaired later, because the row does not carry the evidence. Naming the product is exactly what P4 declares insufficient, which is why every table in this manuscript carries the pinned identifier rather than the brand.

**P5, the generation configuration.** Temperature, nucleus sampling parameter, seed where available, output limits, reasoning effort where the provider exposes it, and the system prompt are published with the figure `[BRGEO1-M-007]`. The requirement earns its place from the field record: two of the four series events in the reference instantiation were caused by changing generation configuration without changing the model identifier. The limit of the requirement has to be conceded in the same breath. Pinning temperature at zero does not buy determinism in a hosted model, because silent updates, numerical rounding and expert routing keep the output variable [Atil2025; Coqueret2026; Ouyang2025]. P5 pins the request and not the response. The consequence is procedural: regeneration cannot serve as the reproduction path, and the stored response becomes the only artefact a third party can re-measure. That argument is the reason retention of the full response is a requirement in its own right `[BRGEO1-S-001]` rather than a convenience.

**P6, the entity matching rule.** The rule maps a response to the set of entities it names, and it is declared in full: matching form, alias table, disambiguation policy, exclusion contexts, and the boundary policy for a mention straddling the window edge `[BRGEO1-M-008]`. Two implementations with different rules produce different figures under identical values of P1 to P5, which would defeat the specification. Until now that was an argument rather than a measurement. An ablation over 2,225 canonical observations collected from 2026-09-06 to 2026-09-08 gives it a magnitude: removing the alias table moved the panel rate by 0.94 percentage points at 200 characters and 0.76 on the whole response, flipping 21 and 17 observations; removing the exclusion contexts moved nothing at all, with zero flips at both windows; removing the ambiguity guard moved one observation. The effect of the alias table is concentrated on one arm, the retrieval-augmented one, which lost 5.25 points at 200 characters because short forms reproduced from sources are what aliases catch, while the parametric arms in this cohort write canonical long names. The exclusion contexts are inert for a reason a reader can check: exactly one entity in the 127-member cohort carries one, and its three patterns never fired. The magnitude, including when it is zero, is what turns a declared parameter into a checkable one, which is why the ablation is published here with its flip counts. The distribution does not transfer: an implementation whose cohort contains short or colliding surfaces should expect the opposite ordering, which is why a conforming claim publishes its own ablation `[BRGEO1-S-003]` rather than citing this one.

### 3.2 Normative language and requirement identifiers

*This subsection is normative.*

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY" and "OPTIONAL" are to be interpreted as described in BCP 14 [Bradner1997; Leiba2017] when, and only when, they appear in all capitals.

Sections are marked normative or informative. Only normative content states requirements for conformance; examples and explanatory passages impose none. Requirements carry stable identifiers of the form `[BRGEO1-M-nnn]` for MUST, `[BRGEO1-S-nnn]` for SHOULD and `[BRGEO1-O-nnn]` for OPTIONAL, so that errata, audit findings and conformance claims have a fixed referent that survives renumbering of the prose.

### 3.3 Conformance levels on an attestation axis

*This subsection is normative.*

The three levels differ in who verified the figure, and in nothing else. They borrow the first-party to third-party progression of conformity assessment vocabulary [ISO17000] and the artifact badging practice of computing conferences [Ferro2018]; the framework separating what an evaluation licenses from who vouches for it is the reason the axis is attestation rather than completeness [Salaudeen2025], and the connection between benchmarking, standardisation and certification is developed for AI systems in [Adel2024].

**Table B2.** Conformance levels. Requirements are cumulative; the axis is who attests, not how complete the measurement is.

| | Level 1, Declared | Level 2, Verified | Level 3, Attested |
|---|---|---|---|
| Requirements | all MUST | all MUST and SHOULD | all MUST and SHOULD |
| Evidence | public claim with the components of §3.5 | complete evidence package, recomputable by a third party from stored responses | evidence package plus external attestation |
| Verified by | first party | first party, reproducibly | body independent of the claimant and of the maintainer |

Level 2 is unreachable without retention of the full response `[BRGEO1-S-001]`, since recomputation requires the input. The reference instantiation of §4 was therefore Level 1 for the first four months of its series and could not have claimed otherwise. It is NOT RECOMMENDED that Level 3 be required as a general procurement policy `[BRGEO1-O-001]`, because third-party attestation is not attainable at reasonable cost for every class of measurement subject, and a level scheme whose top rung is affordable only to large firms is a barrier to entry rather than an open standard.

### 3.4 Divisions, closed and open

*This subsection is normative.*

Orthogonal to level, every measurement declares a division. In the **Closed** division, window, cohort, battery, panel, generation configuration and matching rule take the values fixed by the specification or by a published profile, and figures are comparable across claimants. In the **Open** division any parameter varies from the profile, with the deviation documented; Open figures are comparable neither with each other nor with Closed figures and MUST NOT be presented as though they were `[BRGEO1-M-011]`. The division system is what keeps the specification usable by an adopter whose market or budget rules out a profile value, and it follows the practice of benchmark suites that survive by adoption rather than by authority [Liang2023; Thakur2021; Muennighoff2023].

### 3.5 The conformance claim

*This subsection is normative.*

A claimant publishes one page `[BRGEO1-M-010]`. The page carries the level, the division, the specification version, the six parameter values, and the evidence locations. Structured declaration of this kind is converging practice in evaluation reporting [Mitchell2019; Gebru2021; Breuer2022; Ghosh2026; Dhar2025], and the argument for publishing the components rather than only the headline is made independently in the item-level release literature [Jiang2026].

**Table B3.** Components of a BRGEO-1 conformance claim. Every row is required at Level 1; the evidence rows acquire a resolvable identifier at Level 2.

| Component | Content |
|---|---|
| Identification | Specification version, claimed level, claimed division, measurement period with start and end dates |
| P1 | Window in characters, uniform across arms, with the recall target it meets and the arm on which recovery is worst |
| P2 | Cohort file identifier, entity count by class, decoy count, date fixed |
| P3 | Battery file identifier, query count, the factorial invariants and any routing that sends an arm a subset |
| P4 | Model version string per arm, with the dates of every panel or version boundary |
| P5 | Temperature, sampling parameters, seed, output caps, reasoning effort, system prompt |
| P6 | Matching rule with its dictionaries, plus the rate recomputed with each dictionary removed |
| Missingness | Days with data against days on the calendar, partial days, aborted runs, and the policy statement that nothing is imputed |
| Uncertainty | The budget of §3.7, with the state of each component |
| Evidence | Locations of stored responses, extraction code and the script that regenerates every published figure |

### 3.6 The missingness ledger

*This subsection is normative.*

BRGEO-1 imputes nothing `[BRGEO1-M-009]`. Longitudinal collection against commercial interfaces fails: providers return errors, credit is exhausted, payload validation changes without notice. Every gap is recorded with its date, its extent and its cause, and it is marked in the data rather than filled or dropped. The requirement to record collection failures comes from the algorithm-auditing methodology the design follows [Metaxa2021], and the reason it is normative rather than good practice is that a study which reports only the days that worked has quietly selected on the instrument's own health.

Two rules make the ledger enforceable rather than decorative. First, a claim of absence requires a measurement: an entity that was never named is reported with the observation count over which it was never named, and with the ledger entry accounting for the queries that returned an error and were therefore not evaluable. Second, the analysis weights days by coverage and carries partial days into a sensitivity analysis reported with and without them, so that a reader can see the effect of the decision rather than inherit it.

The ledger also has to record its own limits. Missingness in the reference instantiation is not ignorable: gaps cluster around provider credit exhaustion, which correlates with cost, which correlates with response length, which §6 establishes correlates with citation. Coverage weighting corrects data missing at random and does not address that mechanism. Publishing the ratio is what allows a reader to discount the series; it does not repair it.

### 3.7 The uncertainty budget

*This subsection is normative.*

A conforming figure SHOULD be published with an uncertainty budget `[BRGEO1-S-004]`. The GUM classifies the evaluation of uncertainty components into Type A, estimated from a series of repeated observations, and Type B, estimated by any other means, from prior knowledge, specifications or judgement; clause 3.3.4 is explicit that the classification concerns the method of evaluation and implies no difference in the nature of the components [JCGM100]. Applied to a citation rate, the division separates the components a sample count can estimate from the components only a declared parameter removes, which is what Table B4 carries.

**Table B4.** Uncertainty budget for a citation rate under BRGEO-1, with the state of each component in the reference instantiation of §4. Type A follows GUM 3.3.5 and 4.2; Type B follows GUM 4.3. Series 2026-04-23 to 2026-09-08 except where the entry names a shorter window; day counts are the table-build count of §8.2.

| Component | Type | Source of the estimate | State in this study |
|---|---|---|---|
| Query sampling | A | Variance across the 192-query battery | Estimable from the series |
| Day-to-day variation | A | Even-odd split of 53 collected days over 88 cells | Estimated: typical error 2.39 pp |
| Run-to-run variation of the model | A | Two runs per day at temperature 0 | Measured: same-day test-retest concordance 0.835 to 0.992 by arm, kappa 0.669 on the retrieval-augmented arm (S3) |
| Observation window, P1 | B | Re-extraction under two declared windows | Measured: +22.95 to +55.73 pp across five arms, n = 2,225 |
| Entity matching rule, P6 | B | Ablation of alias table, exclusion contexts and ambiguity guard | Measured: 0.94 pp on the panel, 5.25 pp on one arm, n = 2,225 |
| Lexical collision in the cohort | B | Removal of two colliding surface forms | Measured: 0.51 pp on the panel, n = 68,624 |
| Model version drift, P4 | B | Dated series events | Bounded by stratification, not estimated |
| Generation configuration, P5 | B | One series event caused by reasoning effort alone | Bounded, not estimated |
| Provider routing and unequal sampling | B | One arm receives 96 of the 192 canonical queries | Reported, not corrected |
| Elicitation mode | B | Plain prompt against structured request | Not estimated; the highest-priority open item |
| Cohort and battery composition | B | Design fixed before collection | Fixed by declaration, which is what a Closed division means |

Two readings follow, and the second is the point of publishing the table. The components the market reports are the Type A ones, and they are the small ones: the largest Type A entry here is 2.39 percentage points of typical error, against a Type B entry of 22.95 to 55.73 percentage points for the window. The protocol's function is to convert Type B components into declared constants, since a parameter that is fixed and published stops contributing to comparisons between figures that declare the same value. That is the precise sense in which BRGEO-1 produces comparability, and it is also the sense in which the claim remains untested: two components are bounded rather than estimated and one is not estimated at all. The exercise that would close the gap is an interlaboratory study in the sense of ISO 5725-2, with the discrepancy between independent implementations of the same stored responses decomposed into repeatability and between-implementation terms [ISO5725-2]. The variance vocabulary of generalizability theory, already used in this market to decide how many times to repeat a query [Zatuchin2026a], is the natural companion for that decomposition. The measurand itself remains constituted by convention rather than discovered, which is the standing position for unobservable constructs [Jacobs2021; Borsboom2004], and §14 keeps that limit in view.

---

## 4. Reference instantiation

The values below are what the longitudinal study of this paper uses. They are calibration rather than specification: another adopter conforms with different values, provided the values are declared. This section is informative; the requirements it instantiates are stated in §3.

**Table B5.** Reference instantiation of the six parameters. Series 2026-04-23 to 2026-09-08, 68,624 canonical observations and 17,919 adversarial probes, 86,543 rows in total.

| Parameter | Reference value |
|---|---|
| P1 Window | 200 characters, uniform across the panel, configurable by `PAPERS_CITATION_WINDOW_CHARS`; the whole response retained since migration 0010 |
| P2 Cohort | 127 entities: 79 Brazilian firms, 32 international anchors, 16 fictitious decoys, across four verticals |
| P3 Battery | 192 canonical queries: 4 verticals × 6 semantic categories × 2 languages × 2 query types × 2 temporal frames, plus 16 adversarial probes |
| P4 Panel | 6 engines across the series and never 6 at once, versions pinned per observation (Table B6) |
| P5 Generation | Temperature 0.0; output caps by provider; reasoning disabled or reduced where the provider exposes the control; system prompt published |
| P6 Matching | Word-boundary matching with NFKD dual-pass normalisation, markup stripping, alias table, ambiguity guard requiring canonical form, and exclusion contexts |

### 4.1 Cohort construction and tier stratification

The cohort is fixed in `src/config_v2.py` and dated before the first observation of the series. Tiers are balanced with at least five long-tail firms per vertical, seven Brazilian states are represented, and `legal_status` is annotated so that a model naming a firm in judicial recovery is not pooled with one naming an active firm. In this cohort the field has almost no variance, with 110 of the 111 real members active and one, Americanas, in judicial recovery, which is why §9 does not model it. The cohort was designed to probe the awareness gap of models whose pre-training predates a firm, and it does not reach it: the most recently founded member dates from 2019, earlier than every plausible cut-off for the pinned versions, so the indicator for a firm founded after the cut-off has no cases and §9 does not fit it. The mechanism benchmark-contamination work describes from the other direction [Xu2024] therefore remains untested here, and its measured form in brand discovery is the existence gap [Huang2026]. Each of the 16 decoys was verified as non-existent against the Brazilian federal tax registry, mapping services and court records before inclusion, and §14 records the jurisdictional limit of that verification.

### 4.2 Query battery and factorial balance

The 192 canonical queries are generated from five declared axes, so the balance is a property of the construction and not of an editorial pass. The cells run 96 Portuguese and 96 English, 96 directive and 96 exploratory, 48 per vertical, with half of each cell carrying the temporal frame "em 2026" and half atemporal. English queries always name Brazil, which prevents drift toward North American and European brands. Balance is what makes the stratum contrasts readable: the largest of them, directive against exploratory, runs 25.9% against 10.0% at panel level over 34,319 and 34,305 canonical observations respectively, and it holds in every arm. Provider routing breaks the balance in one place, which is declared rather than smoothed: the retrieval-augmented arm runs 96 of the 192 queries on cost grounds, and the half it runs is the discovery-shaped half, so its category column is not comparable with the parametric arms.

### 4.3 Engine panel with pinned versions

**Table B6.** Engine panel with pinned model identifiers, architectural class and active period. Series 2026-04-23 to 2026-09-08, 68,624 canonical observations; denominator is rows of `citations` with `COALESCE(is_probe,0)=0`.

| Engine | Pinned model identifier | Class | Active period | Canonical n |
|---|---|---|---|---:|
| ChatGPT | `gpt-4o-mini-2024-07-18` | parametric | 2026-04-23 to 2026-09-08 | 15,168 |
| Claude | `claude-haiku-4-5-20251001` | parametric | 2026-04-23 to 2026-09-08 | 15,034 |
| Gemini | `gemini-2.5-pro` to 2026-06-09, then `gemini-2.5-flash` from 2026-08-08 | parametric | 2026-04-23 to 2026-09-08 | 15,355 |
| Groq | `llama-3.3-70b-versatile` | parametric, open weights | 2026-04-23 to 2026-08-16 | 14,208 |
| Perplexity | `sonar` | retrieval-augmented | 2026-04-23 to 2026-09-08 | 7,741 |
| Grok | `grok-4.6` | parametric | 2026-08-23 to 2026-09-08 | 1,118 |
| **Panel** | — | — | 2026-04-23 to 2026-09-08 | **68,624** |

The panel holds six engines across the series and never six at once. Groq leaves on 2026-08-16 and Grok enters on 2026-08-23, so the two occupy one slot in successive periods and any analysis crossing that boundary stratifies or truncates. The Gemini row is a second boundary of the same kind, and it is the one that shows why P4 is written as it is: the commit of 2026-06-17 changed the model identifier and the reasoning budget together, so the pre-boundary and post-boundary observations of that arm differ in two parameters at once and are not comparable within the arm.

### 4.4 Generation configuration

Temperature is 0.0 on every arm, output caps are set per provider, and the system prompt is published. Reasoning effort is the control that turned out to matter. Measured against the collection query on 2026-08-31, the Grok arm returned in 73.7 seconds with 2,746 reasoning tokens under provider defaults, against 19.7 seconds and 419 tokens at `reasoning_effort=low`. Under defaults the arm alone consumed 129 of 179 minutes of wall-clock time and lost five consecutive collections to a 180-minute timeout between 24 and 30 August without persisting a single day. The model identifier did not change across that boundary, which is the whole argument for P5: a parameter that moves latency by a factor of nearly four, and with it whether a day enters the series at all, is invisible to any record that logs only the model name. The 206 rows collected on 2026-08-23 fall on the earlier side of that boundary. The declared decision was to discard them in that arm rather than stratify; the tables of this manuscript do not implement it, and the 158 canonical rows of that day remain inside the arm's 1,118 observations. The discrepancy is 14% of the arm and it is declared here rather than silently reconciled, because reconciling it would change every Grok figure in §9.

### 4.5 Entity matching rule, and a collision it did not catch

The rule is the project's own extractor over the v2 cohort, with anchors and decoys included. It matches on word boundaries under `\b`, runs a dual pass preserving NFC and folding NFKD so that a Portuguese name written without diacritics in an English response still matches, strips markup so that bold formatting and bracketed reference markers do not break the boundary, and applies an alias table, an ambiguity guard requiring the canonical form, and exclusion contexts. Position is the real offset from `text.find`, not an artefact of cohort iteration order.

Collision between a brand and an ordinary word is the failure mode most likely to inflate a naive count, and this instantiation demonstrates it on itself. Two names in this cohort are ordinary English words and neither carried a guard: `Involves`, a Brazilian technology firm founded in 2008, matches the English verb in 345 observations, and `Target`, an international retail anchor, matches the noun in eight.

**Table B7.** Sensitivity of the published panel figures to two colliding cohort surfaces. Series 2026-04-23 to 2026-09-08, 68,624 canonical observations under the uniform 200-character window; denominator for the rate is all canonical observations, and for the concentration statistics the 12,329 first mentions.

| Quantity | With the two surfaces | Without |
|---|---:|---:|
| Panel citations under the uniform window | 12,329 | 11,976 |
| Panel citation rate | 17.97% | 17.45% |
| Distinct entities ever named first | 42 | 40 |
| Herfindahl-Hirschman index of first mentions | 0.1917 | 0.2023 |
| Share of first mentions held by the leader | 37.3% | 38.4% |

The affected set is 353 observations, 0.51% of the canonical panel, and in every one of them the collision is the only match, so the whole set is counted as cited for no other reason. All 353 fall in English responses, distributed as Groq 173, ChatGPT 158 and Gemini 22. The tables of this manuscript are published with the collisions left in, because those figures are what the instrument as specified produces, and because correcting the cohort here would break the correspondence with the stored series that the verification file establishes. The correction belongs to the configuration: `Involves` needs a canonical name and `Target` needs a stop context, and both require re-extraction of the series rather than a note in the text. Until that runs, this paragraph is the declared error term on every rate in §9, two orders of magnitude below the window effect of §6, which is why it changes no conclusion drawn from them. A protocol paper that asks others to declare their matching rule has to declare where its own leaks.

### 4.6 Why a Brazilian instantiation is a stress test

Portuguese-language measurement exercises the instrument against three conditions that English-first tooling does not anticipate: brand names colliding with ordinary words, diacritics rendered inconsistently across languages, and market leaders postdating the pre-training cut-off of deployed models. None is peculiar to Brazil. Lexical collision between a brand and a common word occurs in any language, as Orange, Free, Next, Three, Ideal, Post, Meta and Target attest, and §4.5 shows the failure occurring inside this instrument rather than in a hypothetical one. The linguistic case is no longer only an argument from first principles: cross-language responses about the same brands diverge in similarity and in sentiment across twelve European languages [Zatuchin2026c], query language is the largest systematic factor in a crossed variance decomposition [Zatuchin2026b], and evaluation instruments themselves degrade outside English [Hada2024]. Brazilian-Portuguese evaluation is an active research area rather than a convenience choice [Santos2026]. An instrument validated where all three conditions hold at once has been tested under harder conditions than one calibrated on English alone, and the battery is half English precisely so that a Brazilian result can be checked against a non-Brazilian baseline inside the same instrument.

### 4.7 Collection pipeline, caching and cost

Collection runs twice daily at 06:00 and 18:00 in Brasília time. The unit of observation is one triple of query, engine and run. Responses are cached by SHA-256 content hash, and what keeps a cached answer out of the series is not the time-to-live. The implementation's default is 20 hours, longer than the twelve-hour interval between rounds, so on that parameter alone the evening round could be served the morning's answer. The protection that operates instead is that the cache directory is excluded from version control and every collection, scheduled or manually dispatched, runs on an ephemeral hosted runner whose cache directory is created empty. A run started from a local working copy that keeps its cache between invocations carries no such protection, and no column of `citations` records whether a row was served from cache, so such a run would not be identifiable after the fact. The Type A run-to-run component of Table B4 is the entry that depends on this: a cached second round would return concordance of exactly 1.0, and the measured same-day concordance runs from 0.835 to 0.992, which is the only evidence in the series that the two rounds are two calls.

The response hash is stored per row, which turns a silent provider change into a visible shift in the distribution of hashes. Since migration 0010 the pipeline writes the whole response to `response_full_text` while continuing to write the windowed string to `response_text`, which is what makes the two-window comparison of §6 a within-observation comparison rather than a between-period one.

Cost shapes the design in three places, and each is declared because each biases something. Reasoning tokens on the first Gemini pinned model were about 91% of the study's inference spend, roughly R$2,100 per month, which is the stated motive for the 2026-06-17 change of model and reasoning budget, and therefore the reason that arm has a stratum boundary. The retrieval arm runs 96 of the 192 canonical queries on cost grounds, which halves its per-cell power and removes three of the six semantic categories from its coverage. The same arm bills US$0.0025 per search on the agent route against US$0.005 per request on the legacy route, a difference that matters because the legacy transport is scheduled for retirement on 2026-09-27, inside the projected collection window. Coverage over the span is 53 days with data against 139 calendar days under the table-build date rule of §8.2, with 19 of those 53 partial, 328 collection runs recorded as successful and 344 as aborted; §8 carries the ledger and §14 carries the consequence, which is that the missingness mechanism correlates with the quantity being measured.

---

## 12. Adopting the protocol

An adopter needs three things the specification does not supply on its own: a form to fill in, a list of the decisions that cannot be deferred, and a warning about the failures that will not announce themselves. This section supplies all three from the record of this study. Reproduction failures in audits of commercial systems are documented rather than hypothetical [Mosnar2025], and the conditions that failed there are the conditions BRGEO-1 pins.

### 12.1 A conformance claim in one page

This subsection is informative; the requirements it illustrates are stated in §3.5.

The claim below is the form as it would be filled for the reference instantiation, at the level and division that instantiation can honestly claim.

```
BRGEO-1 CONFORMANCE CLAIM
Specification version   BRGEO-1, v1.0
Level                   Level 1 (Declared)
Division                Closed
Measurement period      2026-04-23 to 2026-09-08 (53 collected days
                        under the table-build date rule; 52 under the
                        local-date rule of §8.2)

P1 Observation window   200 characters, uniform across all arms.
                        On the 1,367 mentions retained whole,
                        2026-09-06 to 09-08: recovers 35.4% on the
                        panel; worst arm 7.8%, best arm 70.2%.
P2 Cohort               127 entities (79 Brazilian firms, 32 international
                        anchors, 16 fictitious decoys), 4 verticals,
                        fixed 2026-04-23, file src/config_v2.py.
P3 Query battery        192 canonical queries, 4x6x2x2x2 factorial;
                        96 pt / 96 en; 96 directive / 96 exploratory.
                        Routing: 1 arm receives 96 of 192.
P4 Engine panel         gpt-4o-mini-2024-07-18; claude-haiku-4-5-20251001;
                        gemini-2.5-pro then gemini-2.5-flash (boundary
                        2026-06-17); llama-3.3-70b-versatile (to
                        2026-08-16); sonar; grok-4.6 (from 2026-08-23).
P5 Generation           temperature 0.0; per-provider output caps;
                        reasoning reduced or disabled where exposed
                        (boundary 2026-08-31); system prompt published.
P6 Matching rule        word-boundary, NFKD dual pass, markup stripped,
                        alias table, ambiguity guard, exclusion contexts.
                        Ablation on 2,225 observations, 2026-09-06 to
                        09-08: -0.94 pp without aliases, 0.00 pp
                        without exclusion contexts, +0.04 pp without
                        the ambiguity guard.
Missingness             53 days with data / 139 calendar days; 19 partial;
                        328 successful runs, 344 aborted. No imputation.
Declared error term     Two cohort surfaces collide with ordinary words:
                        +0.51 pp on the panel rate.
Uncertainty budget      Table B4.
Evidence                Stored responses: response_full_text from
                        2026-08-31 forward only. Extraction code and
                        table-regeneration scripts: public repository.
Level 2 not claimed     Responses before 2026-08-31 were never retained,
                        so 66,399 canonical observations cannot be
                        re-extracted by a third party.
```

The Level 2 line is the one a claimant would omit, and it is the line that tells a reader that 66,399 of the 68,624 observations behind every rate in §9 cannot be re-extracted by anyone.

### 12.2 Ten decisions an adopter must make

**Table B8.** The ten decisions, the recommendation, and the evidence that produces it. Series and denominators are named per row; where a row cites the three-day full-text cohort it covers 2026-09-06 to 2026-09-08, and where it cites the long series it covers 2026-04-23 to 2026-09-08.

| | Decision | Recommendation | Evidence |
|---|---|---|---|
| 1 | Window value | Set it from a recall target, not from a round number, and publish both | 200 characters recovers 35.4% of first mentions across the panel and between 7.8% and 70.2% by arm, over 1,367 observations cited on the whole response |
| 2 | Window uniformity | One value for every arm, applied at collection and re-checked at analysis | An asymmetric window moved one published rate from 74.9% to 52.0% over 7,435 truncated rows of 7,741 |
| 3 | Retention | Store the whole response from the first observation | 66,399 canonical observations collected before retention began cannot be re-extracted, and one retired arm's window effect is now unmeasurable |
| 4 | Cohort surfaces | Use canonical long names, and run the collision test before collection | Two colliding surfaces added 0.51 pp to the panel rate over 68,624 observations and changed the concentration index from 0.1917 to 0.2023 |
| 5 | Calibration decoys | Include them, and cover every arm with the probes | Spontaneous decoy naming was 0 over 68,624 canonical observations, Wilson upper bound 0.0056%; the probe stratum excluded one arm entirely, which removed the most informative case |
| 6 | Battery balance | Generate the battery from declared axes rather than curating it | Directive against exploratory is 25.9% against 10.0% at panel level over 34,319 and 34,305 observations, and it holds in every arm |
| 7 | Engine identification | Record the version string per row and date every boundary | One boundary changed model identifier and reasoning budget in the same commit, making the arm's two periods non-comparable [Chen2024] |
| 8 | Generation configuration | Publish it, reasoning effort included, and treat a change as a stratum boundary | One change to reasoning effort alone cost five consecutive collections and 129 of 179 minutes of one run's wall-clock time |
| 9 | Matching rule | Publish the rule and its ablation, never the rule alone | Aliases moved the panel by 0.94 pp and one arm by 5.25 pp; exclusion contexts moved nothing, on 2,225 observations |
| 10 | Missingness | Record every gap; impute nothing; publish the ratio | 53 days with data against 139 calendar days, 19 partial, 344 aborted runs; gaps cluster on credit exhaustion, which correlates with the measured quantity |

Two decisions sit outside the table because BRGEO-1 does not take them. Repetition count is the province of a complementary protocol that fixes iteration tiers and reports reliability as a generalizability coefficient, G = 0.58 at five iterations and G = 0.74 at ten [Zatuchin2026a]; an adopter who declares both protocols is better specified than one who declares either, and BRGEO-1 recommends the pairing without requiring it `[BRGEO1-O-002]`. Sufficiency of the collected sample has its own convergence criteria in this market [Sielinski2026b], and an adopter should state which one stopped collection. Aggregation is deliberately unconstrained: §10 reports that two defensible aggregations of the same components rank entities at rho 0.752 over 66 entities, so the specification constrains the conditions of observation, where disagreement is large and resolvable, and leaves the formula to the reporter who must then publish the components alongside it [Saisana2005; Paruolo2013; Jiang2026].

### 12.3 Errors an adopter will meet

Every failure below produced a green pipeline in this study, which is the property they share and the reason a functional test suite will not find them.

**The window is set in the adapter, not in the design.** Five of six client adapters wrote `text[:200]` and the sixth did not. §5.3 gives the detection history; the transferable part is the check that found it, a variable whose maximum equals its minimum across 15,168 observations is reporting a boundary rather than measuring a length. Run that check on day one.

**A protection can be written, called, and swallowed.** The migration that added full-response retention was invoked from inside a function that ran before the table it altered existed. It failed on "no such table", an `except` turned the failure into a debug log, and on an existing database the column appeared anyway. A new database would have been born without it and nobody would have known. Every exception handler that degrades to a low-level log inside an initialisation path needs a test that exercises the path from zero.

**An undeclared constant in the reference implementation is an undeclared parameter.** The index script in this project carried a minimum observation count of 500 for panel eligibility, set in code and named nowhere in the specification. In the fintech panel it excluded a live arm holding 96 observations and retained an arm retired weeks earlier holding 3,552. The reference implementation of a measurement standard is part of the standard, and an eligibility rule that lives only in code reproduces, inside the artefact meant to demonstrate the specification, the failure the specification exists to prevent.

**The dashboard and the paper will disagree.** The field log of this project records a divergence between the per-arm rates published on the public dashboard and the per-arm rates in the manuscript, traced by code inspection to a different extractor version and a denominator that includes the adversarial probe stratum; the log marks the divergence as not yet reconciled in any repository document and as requiring independent verification before it is asserted as a finding. The adopter lesson does not wait on that verification. Decide once which extractor and which denominator a published number uses, and make every surface read from the same computation, because the alternative is the defect this protocol describes in the market occurring between two artefacts of the same project.

**The provider will move without asking.** Presets on one interface routed to a third-party model under a name that did not change, which would have swapped an arm silently; the study now names the model explicitly on every call. The same provider scheduled retirement of the transport in use for a date inside the collection window. Pin the model by string, probe what the string actually returns, and read the provider's deprecation notices as instrument risk rather than as engineering news.

**Credit exhaustion is a measurement problem.** Seventeen days of series were lost between 2026-08-16 and 2026-09-08, with 49 runs of which three succeeded, 28 barred at preflight on balance or model, 17 cancelled on timeout or concurrency and two failed in collection, a run counting on more than one line when two providers failed together. A preflight that bars a partial day protects the series from a day that looks complete and is not, and it costs statistical power; a policy that admits partial days costs the opposite. Both are defensible, and the requirement is that the choice, the date it changed, and its effect on the ledger are published rather than inferred.

---

## Reference keys used

Entries are reproduced from `../research/R1-literature.md`, which records the primary record against which each identifier was resolved on 2026-09-11, with the three corrections listed in `../DECISIONS.md` §8 applied. Two entries, marked below, come from `../research/R5-metrology.md` §7, where the clause numbers were confirmed by extracting the text of the official documents; the two paywalled standards are cited at document level because their clause numbers were not opened.

**[Adel2024]** Adel, T., Bilson, S., Levene, M., Thompson, A., 2024. Trustworthy Artificial Intelligence in the Context of Metrology, in: Ferreira, M.I.A. (Ed.), Producing Artificial Intelligent Systems: The Roles of Benchmarking, Standardisation and Certification, Studies in Computational Intelligence. Springer. arXiv:2406.10117.

**[Atil2025]** Atıl, B., Aykent, S., Chittams, A., Fu, L., Passonneau, R.J., Radcliffe, E., et al., 2025. Non-Determinism of "Deterministic" LLM System Settings in Hosted Environments, in: Proceedings of the 5th Workshop on Evaluation and Comparison of NLP Systems (Eval4NLP), pp. 135–148. https://doi.org/10.18653/v1/2025.eval4nlp-1.12

**[Bailey2016]** Bailey, P., Moffat, A., Scholer, F., Thomas, P., 2016. UQV100: A Test Collection with Query Variability, in: Proceedings of SIGIR 2016, pp. 725–728. https://doi.org/10.1145/2911451.2914671

**[Bito2026]** Bito, E., Ren, Y., He, E., 2026. Position Bias Undermines Preference Consistency in Listwise LLM-Based Reranking, in: Proceedings of the ACM Conference on Recommender Systems (RecSys 2026). arXiv:2608.03091.

**[Borsboom2004]** Borsboom, D., Mellenbergh, G.J., van Heerden, J., 2004. The Concept of Validity. Psychological Review 111 (4), 1061–1071. https://doi.org/10.1037/0033-295X.111.4.1061

**[Bradner1997]** Bradner, S., 1997. Key words for use in RFCs to Indicate Requirement Levels. RFC 2119, BCP 14, Internet Engineering Task Force. https://doi.org/10.17487/RFC2119

**[Breuer2022]** Breuer, T., Keller, J., Schaer, P., 2022. ir_metadata: An Extensible Metadata Schema for IR Experiments, in: Proceedings of SIGIR 2022, pp. 3078–3089. https://doi.org/10.1145/3477495.3531738

**[Chen2024]** Chen, L., Zaharia, M., Zou, J., 2024. How Is ChatGPT's Behavior Changing Over Time? Harvard Data Science Review 6 (2). https://doi.org/10.1162/99608f92.5317da47

**[Chu2026]** Chu, X., Hou, Y., 2026. Incumbent Advantage: Brand Bias and Cognitive Manipulation Dynamics in LLM Recommendation Systems. arXiv:2606.17443.

**[Coqueret2026]** Coqueret, G., Llull, J., Oswald, F., Pérignon, C., Scheuch, C., Vilhuber, L., 2026. Randomness in Large Language Models: What Researchers Need to Know (and Report). arXiv:2607.24372.

**[Dhar2025]** Dhar, R., Sanchez Villegas, D., Karamolegkou, A., Schiavone, A., Yuan, Y., Chen, X., et al., 2025. EvalCards: A Framework for Standardized Evaluation Reporting. arXiv:2511.21695.

**[Ferro2018]** Ferro, N., Kelly, D., 2018. SIGIR Initiative to Implement ACM Artifact Review and Badging. ACM SIGIR Forum 52 (1), 4–10. https://doi.org/10.1145/3274784.3274786

**[Gebru2021]** Gebru, T., Morgenstern, J., Vecchione, B., Vaughan, J.W., Wallach, H., Daumé III, H., Crawford, K., 2021. Datasheets for Datasets. Communications of the ACM 64 (12), 86–92. https://doi.org/10.1145/3458723

**[Ghosh2026]** Ghosh, A., Reuel, A., Chim, J., Kennedy, W.M., Yadav, S., Mickel, J., et al., 2026. Evaluation Cards: An Interpretive Layer for AI Evaluation Reporting. arXiv:2606.09809.

**[Hada2024]** Hada, R., Gumma, V., de Wynter, A., Diddee, H., Ahmed, M., Choudhury, M., Bali, K., Sitaram, S., 2024. Are Large Language Model-Based Evaluators the Solution to Scaling Up Multilingual Evaluation?, in: Findings of the Association for Computational Linguistics: EACL 2024. arXiv:2309.07462.

**[Hou2024]** Hou, Y., Zhang, J., Lin, Z., Lu, H., Xie, R., McAuley, J., Zhao, W.X., 2024. Large Language Models Are Zero-Shot Rankers for Recommender Systems, in: Advances in Information Retrieval (ECIR 2024), Lecture Notes in Computer Science, pp. 364–381. https://doi.org/10.1007/978-3-031-56060-6_24

**[Huang2026]** Huang, J., Situ, R., Ye, R., 2026. Cultural Encoding in Large Language Models: The Existence Gap in AI-Mediated Brand Discovery. arXiv:2601.00869.

**[ISO5725-2]** ISO 5725-2:1994, Accuracy (trueness and precision) of measurement methods and results — Part 2: Basic method for the determination of repeatability and reproducibility of a standard measurement method. *Entry from R5 §7; cited at document level, clause numbers not opened.*

**[ISO17000]** ISO/IEC 17000:2020, Conformity assessment — Vocabulary and general principles. *Entry from R5 §7; cited at document level, clause numbers not opened.*

**[Jacobs2021]** Jacobs, A.Z., Wallach, H., 2021. Measurement and Fairness, in: Proceedings of the 2021 ACM Conference on Fairness, Accountability, and Transparency, pp. 375–385. https://doi.org/10.1145/3442188.3445901

**[JCGM100]** JCGM 100:2008, Evaluation of measurement data — Guide to the expression of uncertainty in measurement (GUM). BIPM, 2008. *Entry from R5 §7; clauses 3.3.4, 3.3.5, 4.2 and 4.3 confirmed in the official document on 2026-09-11.*

**[JCGM200]** JCGM 200:2012, International Vocabulary of Metrology — Basic and general concepts and associated terms (VIM), 3rd ed. BIPM, 2012. *Entry from R5 §7; clauses 2.3, 2.20, 2.24, 2.27 and 2.41 confirmed in the official document on 2026-09-11.*

**[Jiang2026]** Jiang, H., Zhang, S., Zhu, D., Bai, Y., Truong, S.T., Yi, X., Koyejo, S., Xie, X., Xiao, Z., 2026. AI Evaluation Should Require Standardized Item-Level Data Releases. arXiv:2604.03244.

**[Leiba2017]** Leiba, B., 2017. Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words. RFC 8174, BCP 14, Internet Engineering Task Force. https://doi.org/10.17487/RFC8174

**[Liang2023]** Liang, P., Bommasani, R., Lee, T., Tsipras, D., Soylu, D., Yasunaga, M., et al., 2023. Holistic Evaluation of Language Models. Transactions on Machine Learning Research. arXiv:2211.09110.

**[Metaxa2021]** Metaxa, D., Park, J.S., Robertson, R.E., Karahalios, K., Wilson, C., Hancock, J.T., Sandvig, C., 2021. Auditing Algorithms: Understanding Algorithmic Systems from the Outside In. Foundations and Trends in Human-Computer Interaction 14 (4), 272–344. https://doi.org/10.1561/1100000083

**[Mitchell2019]** Mitchell, M., Wu, S., Zaldivar, A., Barnes, P., Vasserman, L., Hutchinson, B., Spitzer, E., Raji, I.D., Gebru, T., 2019. Model Cards for Model Reporting, in: Proceedings of the Conference on Fairness, Accountability, and Transparency, pp. 220–229. https://doi.org/10.1145/3287560.3287596

**[Mosnar2025]** Mosnar, M., Skurla, A., Pecher, B., Tibensky, M., Jakubcik, J., Bindas, A., Sakalik, P., Srba, I., 2025. Revisiting Algorithmic Audits of TikTok: Poor Reproducibility and Short-Term Validity of Findings, in: Proceedings of the International ACM SIGIR Conference on Research and Development in Information Retrieval (SIGIR 2025). arXiv:2504.18140.

**[Muennighoff2023]** Muennighoff, N., Tazi, N., Magne, L., Reimers, N., 2023. MTEB: Massive Text Embedding Benchmark, in: Proceedings of EACL 2023, pp. 2014–2037. https://doi.org/10.18653/v1/2023.eacl-main.148

**[Ouyang2025]** Ouyang, S., Zhang, J.M., Harman, M., Wang, M., 2025. An Empirical Study of the Non-Determinism of ChatGPT in Code Generation. ACM Transactions on Software Engineering and Methodology 34 (2), 1–28. https://doi.org/10.1145/3697010

**[Paruolo2013]** Paruolo, P., Saisana, M., Saltelli, A., 2013. Ratings and Rankings: Voodoo or Science? Journal of the Royal Statistical Society Series A: Statistics in Society 176 (3), 609–634. https://doi.org/10.1111/j.1467-985X.2012.01059.x

**[Saisana2005]** Saisana, M., Saltelli, A., Tarantola, S., 2005. Uncertainty and Sensitivity Analysis Techniques as Tools for the Quality Assessment of Composite Indicators. Journal of the Royal Statistical Society Series A: Statistics in Society 168 (2), 307–323. https://doi.org/10.1111/j.1467-985X.2005.00350.x

**[Salaudeen2025]** Salaudeen, O., Reuel, A., Ahmed, A., Bedi, S., Robertson, Z., Sundar, S., et al., 2025. Measurement to Meaning: A Validity-Centered Framework for AI Evaluation. arXiv:2505.10573.

**[Santos2026]** Santos, J.G.A., Bonás, G.K., Laitz, T., Almeida, T.S., Pedrini, H., 2026. BLUEX v2: Benchmarking LLMs on Open-Ended Questions from Brazilian University Entrance Exams. arXiv:2606.22723.

**[Sielinski2026b]** Sielinski, R., 2026. From Stochastic to Stable: Rank Stability and Structural Sufficiency in AI Visibility Measurement. arXiv:2607.10341.

**[Thakur2021]** Thakur, N., Reimers, N., Rücklé, A., Srivastava, A., Gurevych, I., 2021. BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models, in: Proceedings of the NeurIPS Track on Datasets and Benchmarks 1. arXiv:2104.08663.

**[Wadi2026]** Wadi, D., Ma, Y., 2026. Does Rank Still Matter? Position Bias When AI Agents Shop on Our Behalf. arXiv:2608.22697.

**[Xu2024]** Xu, C., Guan, S., Greene, D., Kechadi, M-T., 2024. Benchmark Data Contamination of Large Language Models: A Survey. arXiv:2406.04244.

**[Zatuchin2026a]** Żatuchin, D., 2026. The Dice Roll Method: A Standardized Protocol for Repeated-Query Auditing of Large Language Model Brand Recommendations. arXiv:2609.04047.

**[Zatuchin2026b]** Żatuchin, D., 2026. Where Does the Noise Come From? A Variance-Components Decomposition of Non-Determinism in LLM Brand Answers. arXiv:2607.13304.

**[Zatuchin2026c]** Żatuchin, D., 2026. The Language Blind Spot: How Query Language and Brand Recognition Tier Shape AI-Constructed Brand Reputation Across Twelve European Languages. arXiv:2606.23165.

---

## Anti-tic pass

Run over the full block after drafting, against `../research/R4-standards.md` Part C, and measured by `../reviews/style_check.py` on the delivered file.

| Check | Result |
|---|---|
| C.1.1 Formulaic antithesis | Two constructions removed. "The parameters below are not recommendations, they are the minimum detail" became a positive statement of what the parameters are. "The consequence is not that the parameter is worthless; it is that regeneration cannot serve as the reproduction path" became a positive clause in §3.1 under P5. The measurer finds zero closed-form and zero graduated instances |
| C.1.2 Pseudo-profound closers | Zero. Each subsection closes on a number, a requirement identifier or a consequence |
| C.1.3 Filler connective opening a paragraph | Zero occurrences of Moreover, Furthermore, Additionally, It is worth noting, It is important to note, In this context, In this regard, That said, Notably, Importantly, and a spent-connective density of 0.00 per 250 words |
| C.1.4 First sentence of a section over 45 words | Two instances, both fixed. §4.2 opened on a 48-word inventory and now opens on the 26-word claim that the balance is a property of the construction; §4.5 opened on a 70-word enumeration of the matching rule and now opens on a 17-word statement of what the rule is, with the enumeration in the sentence that follows. The measurer finds zero sections opening above 45 words |
| C.1.5 Self-narration | Zero. No "this paper presents" or "this study aims to". §4 opening states what the values are, not what the section does |
| C.1.6 Verification meta-discourse | Zero. Procedure narration is confined to §4, which is the methods section for this block |
| C.1.7 Em dash in prose | Zero in running prose. Present only as a null marker inside Table B6, in the reference list, and in the working header that disappears at assembly |
| C.1.8 Vague attribution | Zero. Every appeal to prior work carries a key in the same sentence |
| C.1.9 Paragraph over 2,200 characters | Zero. The longest prose paragraph is the P6 entry in §3.1 at 1,685 characters, the only one above the 1,500 warn, retained because splitting it would separate the ablation result from the transfer caveat that qualifies it. The cache declaration in §4.7 reached 1,542 characters and was split at the point where the subject changes from the cache to the stored hash |
| C.1.10 Repeated empty adjective | Zero. "robust", "crucial", "strategic", "comprehensive", "seamless" and "pivotal" absent; "significant" used nowhere in a non-statistical sense |
| C.1.11 Confidence label with no measurement | Every limitation carries its number: the retention gap carries 66,399 observations, the collision carries 0.51 pp, the P6 transfer caveat carries the one-entity count, the cohort's `legal_status` carries 110 of 111, and the post-cut-off indicator carries its zero cases. The run-to-run row of Table B4 read "small at temperature 0 and not zero" with no quantity and now carries the measured test-retest range, 0.835 to 0.992 |
| C.1.12 Labelled alert | Zero |
| C.1.13 Percentage without a denominator | Each of the five percentages in the prose names its n in the sentence, the preceding sentence or the table caption it sits under. The conformance claim of §12.1 gave three recall figures and one ablation under a period line covering the whole series; both now name the three-day cohort and its n |
| C.1.14 Errata inside the text | Zero. The 23.8 pp figure is discussed as a measurement on a defined row set, never as a correction notice, and the block carries no reference to an internal manuscript version outside the specification-version field of the conformance claim, where it is the field's content |
| C.2 Contrastive apposition "X, not Y" | Two occurrences across 4,617 words, 0.43 per thousand, below the 3-per-1,000 warning density. The word count rose by 42 when the P3 entry took its one-sentence cross-reference to §9.2 |
| C.2 Repeated paragraph opening | Zero three-word openings repeating three times |
| C.2 Nominalization and copula evasion | "serves as", "acts as", "functions as", "plays the role of" absent |
| C.2 Vague gerund closing a sentence | "enabling", "facilitating", "paving the way for" absent. "contributing to" appears once in §3.7, as a full verb with an object |
| C.2 Wordy locutions | "due to the fact that", "in order to", "in the realm of" absent |
| C.2 Rhetorical questions in series | Zero |
| C.2 Visual support density | Eight tables plus one form block over 29,382 characters of prose, one item per 3,673 characters, inside the one-per-5,000 floor |
| C.6 Machine-drafted lexicon | Zero hits against the 40-entry list |
| C.4.1 Chained reasoning, across blocks | Three passages were written in more than one block and this one is the owner of two of them. P1 in §3.1 is the single statement of the conversion of whole-response measurement into head-of-response measurement; §2.7 and §6.2 now point here. The detection history of the window asymmetry belongs to §5.3, and §12.3 now points there instead of restating it. The two notes to VIM 2.27 belong to §1.2, and §3 now cites the clause without re-enunciating them |
| C.4.3 Justified recommendation | Every row of Table B8 carries its evidence column; every MUST in §3 carries its failure mode in Table B1 |
| C.4.4 Answer before argument | First sentence of §3, §4 and §12 states the section's conclusion, and after the C.1.4 fixes so do §4.2 and §4.5 |
| C.4.6 Voice | Three paragraphs closed on a generalizing maxim. The one at the close of §4.5 is kept, because the section earns it. The one at the close of §12.1 was converted into its own evidence and now names the 66,399 observations the omitted line reports |
| Part D, four checks | Sample, period, method and denominator verified for every percentage against `../tables/NUMBERS.md` and `../stats/S5-window-validity.md` |
| Part D.2, claims of absence | Two removed. "A parameter that nobody has measured stops being a rhetorical declaration when somebody publishes its magnitude" asserted a state of the literature this paper has not surveyed, and now states what a published magnitude does. "The division does work that no existing reporting format in this market does" asserted the same about every reporting format, and now states what the division separates |
| Diagnostic, reported and not fixed | Sentence length runs from 3 to 68 words at a mean of 25.6 and a standard deviation of 13.9, with two sentences above 60. `rather than` appears 29 times in the prose of this block, 6.3 per thousand words, far above the other three; Part C does not list the construction, and the count is recorded here so that the next revision of the rule can decide whether it should |
