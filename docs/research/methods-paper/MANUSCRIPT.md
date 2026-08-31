# Measuring Entity Citation in Generative Engines: A Longitudinal Protocol and the Observation-Window Problem

**Alexandre Caramaschi**
Independent AI Researcher · ORCID [0009-0004-9150-485X](https://orcid.org/0009-0004-9150-485X)

**Working paper** · Version 1.0 · September 2026
**Target:** SSRN (Information Systems & eBusiness Network), Elsevier

---

## Abstract

Large language models increasingly stand between consumers and the firms they might choose, yet the field that has grown around this shift — generative engine optimization (GEO) — reports citation rates without stating the conditions under which a citation was counted. This paper documents the protocol of an ongoing 90-day longitudinal study of six commercial engines across four Brazilian industry verticals, and isolates one design parameter that the literature leaves implicit: the observation window, meaning how much of a model's answer the instrument actually reads before deciding whether an entity was cited.

The parameter is not innocuous. In our own pipeline the window was set once per provider and drifted apart unnoticed: five parametric arms were measured on the first 200 characters of each answer while the single retrieval-augmented arm was measured on the entire response. Across 64,191 canonical observations the asymmetry inflated that arm's citation rate from 52.0% to 75.8% — 23.8 percentage points produced by the instrument rather than by the model. Re-measuring the five truncated arms under the same window moves none of them by a tenth of a point, which is what separates a correction from a new number.

We report the full design (a 127-entity cohort including fictitious decoys, a 192-query factorial battery plus 64 adversarial probes, twice-daily collection), the extraction instrument, the missingness ledger that records every collection gap instead of imputing it, and the pre-registered analysis plan. We argue that a citation rate is not interpretable as a cross-engine comparison unless the window is declared, and that retrieval-augmented engines are the most affected, because they open with framing prose before naming anything. Dataset, code and collection logs are public.

**Keywords:** generative engine optimization; large language models; entity citation; measurement validity; longitudinal design; retrieval-augmented generation

**JEL:** C81, C83, L86, M31

---

## 1. Introduction

A consumer who once typed a question into a search engine and read ten blue links now asks a model and reads one answer. The firms named in that answer inherit attention that used to be spread across a results page, and the firms left out have no equivalent of page two. A practitioner literature has formed around this — generative engine optimization — alongside an early research literature measuring which entities models name and how often.

Both share a quantity: the citation rate, the share of prompts in which a model names a given entity. It is reported per model, per industry, per prompt type. It anchors claims that one engine favors incumbents, that another invents competitors, that a vertical is harder to enter than another.

What almost none of this work states is where in the answer the measurement stopped. A model asked to recommend a digital bank in Brazil may spend its opening sentences explaining what a digital bank is, name three institutions in the middle, and close with a caveat. An instrument that reads the whole response finds those three. An instrument that reads only the opening finds none. Both report a citation rate. Neither is wrong; they measure different things, and nothing in the published number distinguishes them.

This paper documents the protocol of a longitudinal study now in its fifth month, and treats that omission as its central methodological contribution. The occasion was not theoretical. A routine health check of our own pipeline found the parameter set inconsistently across the study's own arms — which is the failure mode the field should expect, since the window is typically a line of code inside a provider adapter rather than a documented design decision. It produces no error, no warning, and no visible anomaly in the results; it simply makes one arm easier to satisfy than the others.

Our contribution is threefold. First, we specify a longitudinal protocol for entity citation measurement that is auditable end to end: every collection gap is recorded rather than imputed, every instrument change is dated as a series event, and every observation carries the model version and the window under which it was produced. Second, we isolate and quantify the observation window as a design parameter, showing on our own data that it moves a headline number by 23.8 points and that it moves retrieval-augmented and parametric engines asymmetrically. Third, we release the protocol ahead of the confirmatory results, so the analysis plan is on record before the estimates it will produce.

## 2. Background

### 2.1 From ranked lists to single answers

Information retrieval evaluation assumes a ranked list and a user who scans it. Precision at k, NDCG and reciprocal rank all treat position in a list as the unit of exposure. A generative answer has no list. It has a sequence of prose in which entities appear at some offset, sometimes with sources attached, sometimes not, and the user's exposure decays along that sequence in a way no established metric captures.

The practitioner literature responded by borrowing the vocabulary of search — visibility, share of voice, ranking — and applying it to text. The borrowing is loose. "Ranking" in an answer usually means the order in which entities happen to be mentioned, which conflates the model's preference with the grammar of the sentence it chose. We record first-mention offset rather than rank for this reason, and treat position as a tercile of the observed window rather than as an ordinal.

### 2.2 What existing measurements leave unspecified

Three parameters recur as unstated in reported citation rates:

**The window.** How much of the answer was read. This is the subject of §4.

**The matching rule.** Whether an entity counts when its name appears anywhere in the text, only when presented as a recommendation, or only when accompanied by a source. Substring matching on short brand names is especially fragile in Portuguese, where "Inter" occurs inside ordinary words and "99" inside percentages.

**The refusal case.** What happens when a model declines to answer. A model that says "I have no information about that institution" has produced a response containing the institution's name. Instruments that count name occurrences record this as a citation and — in the adversarial case, where the entity is fictitious by construction — as a hallucination. It is the opposite: a correct refusal.

The third point is not hypothetical. In our own probe data, 67.4% of the responses flagged as hallucinating a fictitious entity contained an explicit refusal, several stating outright that the entity does not exist. §5.3 describes how the two are now separated.

## 3. Study design

### 3.1 Cohort

The cohort holds 127 entities: 111 real firms, of which 79 are Brazilian and 32 are international anchors included to test whether a model's Brazilian coverage is a local gap or a general one, plus 16 fictitious decoys used for calibration.

Entities span four verticals — fintech, retail, healthcare and technology — and are stratified by market tier (head, torso, long tail), with at least three long-tail firms per vertical. Geographic diversification covers seven Brazilian states. Each entity carries an annotated `legal_status` (active, judicial recovery, merged, deprecated), because a model naming a firm that no longer exists is a different phenomenon from a model naming one that does, and the two must not be pooled. Firms founded after 2020 are deliberately included to probe the awareness gap of models whose pre-training predates them.

The 16 decoys were each verified as non-existent against the Brazilian federal tax registry, mapping services and court records before inclusion. None collides with an active real entity.

### 3.2 Query battery

The canonical battery is a full factorial: 4 verticals × 6 semantic categories × 2 languages × 2 query types × 2 temporal frames = 192 queries.

Categories are discovery, comparative, trust, experience, market structure and innovation. Query type contrasts directive prompts ("what is the best digital bank in Brazil") with exploratory ones ("how should I choose a digital bank"), a distinction that matters because the first invites a ranked list and the second invites criteria. The temporal frame contrasts an atemporal prompt with one anchored to the current year, isolating whether a model treats recency as relevant. English queries always name Brazil explicitly; without that, answers drift to US and European brands and the vertical comparison collapses.

A further 64 adversarial probes form a separate stratum. Each names one decoy and asks about it directly, forcing a decision: describe an entity that does not exist, or decline. These carry `is_probe=1`, are excluded from the longitudinal series, and serve only the false-positive baseline.

### 3.3 Panel of engines

Six commercial engines, each pinned to an explicit model identifier recorded on every observation:

| Engine | Model identifier | Class |
|---|---|---|
| ChatGPT | `gpt-4o-mini-2024-07-18` | parametric |
| Claude | `claude-haiku-4-5-20251001` | parametric |
| Gemini | `gemini-2.5-flash` | parametric |
| Groq | `llama-3.3-70b-versatile` | parametric, open weights |
| Grok | `grok-4.6` | parametric |
| Perplexity | `sonar` | retrieval-augmented |

Pinning is not a formality. Providers update the model behind a stable name without notice, and a longitudinal series that records only "GPT-4o-mini" cannot distinguish a change in the world from a change in the instrument. Every row stores `model_version`, and a drift detector hashes each response so that a silent backend update surfaces as a shift in the hash distribution before it surfaces in the estimates.

The panel is not static. §7 records each change as a dated series event rather than smoothing it away.

### 3.4 Cadence and unit of observation

Collection runs twice daily, at 09:00 and 21:00 UTC, through a scheduled pipeline. Two runs per day give a within-day contrast that separates genuine temporal variance from sampling noise at a single hour.

The unit of observation is one (query, engine, run) triple. For each we record whether any cohort entity was cited, which entity appeared first and at what character offset, how many were named, the number of sources attached, latency, token counts, the model version, and — since August 2026 — the full response text alongside the window under which extraction ran.

## 4. The observation window

### 4.1 The parameter

Entity extraction runs over a string. That string is not the model's answer; it is whatever the pipeline chose to keep. We call the length of that string the **observation window**, and we argue it belongs in the reported design of any citation study.

The window has a substantive reading, not merely a technical one. A narrow window measures *head-of-response citation*: whether the entity appears in the opening that a reader sees before deciding whether to keep reading. A full window measures *whole-response citation*: whether the entity appears anywhere the reader could eventually reach. These are different constructs, and either is defensible. What is not defensible is leaving the choice implicit, because then the number cannot be compared with anyone else's — including one's own, across arms.

### 4.2 How the asymmetry arose

Our pipeline stored the extraction string in a single column. Five of the six provider adapters passed the answer through a helper that truncated it to the first 200 characters. The sixth, Perplexity, returned earlier in the call path and stored the response whole, up to 2,502 characters.

No test caught this, because every test asserted on the column, and the column was populated in both cases. No validator caught it, because both values are well-formed strings of plausible length. The health checks that ran daily verified that all six arms produced rows, that the language split held at 50/50, and that probes were being marked — all of which were true. The defect lived one level below every assertion the pipeline made about itself.

The discovery came from a distributional check rather than a functional one. Stored response length sat against a ceiling of exactly 200 characters in five arms and nowhere near it in the sixth:

| Arm | n | Mean length | Min | Max | Share at exactly 200 |
|---|---:|---:|---:|---:|---:|
| ChatGPT | 18,560 | 200.0 | 200 | 200 | 100.0% |
| Claude | 18,394 | 200.0 | 200 | 200 | 100.0% |
| Groq | 18,304 | 199.8 | 74 | 200 | 99.8% |
| Grok | 206 | 199.9 | 187 | 200 | 99.0% |
| Gemini | 18,026 | 198.5 | 87 | 200 | 97.3% |
| **Perplexity** | **7,148** | **691.8** | **198** | **2,502** | **0.0%** |

A variable whose maximum equals its minimum across 18,560 observations is not measuring anything; it is reporting a boundary. The arms that fall marginally short of 200 are the ones that sometimes answered in fewer characters than the ceiling — which is the signature of truncation, not of a length distribution.

### 4.3 Magnitude

Re-running the extraction over the 49-day series under a uniform 200-character window gives:

| Arm | n | As collected | Uniform window | Δ | Rows actually cut |
|---|---:|---:|---:|---:|---:|
| ChatGPT | 14,400 | 17.2% | 17.2% | +0.0 pp | 0 |
| Claude | 14,266 | 25.8% | 25.8% | +0.0 pp | 0 |
| Groq | 14,208 | 8.5% | 8.5% | +0.0 pp | 0 |
| Gemini | 14,011 | 1.8% | 1.8% | +0.0 pp | 0 |
| Grok | 158 | 39.2% | 39.2% | +0.0 pp | 0 |
| **Perplexity** | **7,148** | **75.8%** | **52.0%** | **−23.8 pp** | **7,147** |

Counts are canonical queries only; the adversarial stratum is excluded, which is why the retrieval-augmented arm shows the same n in both views — it received no probes until August 2026 (§5.3).

The five zero-deltas are the verification. They confirm the re-extraction reproduces the original instrument exactly where the window did not change, which is what licenses reading the sixth row as a correction rather than as an artifact of new code.

The effect is large enough to reverse an interpretation. At 75.8% the retrieval-augmented engine looks categorically different from the parametric ones, roughly twice the rate of the closest competitor. At 52.0% it remains the highest but sits within the same family — a difference of degree, and one that any account of *why* would need to explain differently.

### 4.4 Why retrieval-augmented engines are most exposed

The asymmetry is not an accident of which adapter we happened to write differently. A retrieval-augmented engine composes its answer after fetching sources, and its opening is typically framing: a restatement of the question, a scoping remark, a note about what the sources cover. Named entities arrive once that framing is done. A parametric model, generating from weights without a retrieval step, tends to name candidates earlier.

This means a narrow window does not penalize all engines equally; it penalizes the ones whose rhetorical structure defers naming. Any comparison of RAG against parametric engines under an undeclared window is therefore confounded by discourse structure, and the direction of the bias is predictable: it will understate the retrieval-augmented arm.

We observe this directly in first-mention offsets. Among canonical observations where a cohort entity is named, the retrieval-augmented arm names it later than every parametric arm, and its distribution has a right tail the others do not have:

| Arm | Cited observations | Mean first-mention offset | Max offset |
|---|---:|---:|---:|
| Perplexity | 5,418 | 157 chars | 1,994 |
| Claude | 3,674 | 124 chars | 194 |
| ChatGPT | 2,471 | 116 chars | 194 |
| Groq | 1,210 | 108 chars | 193 |
| Gemini | 252 | 97 chars | 187 |
| Grok | 62 | 25 chars | 182 |

The maxima for the parametric arms cluster just under 200 because that is where their stored text ended; the tail beyond it was never observable. For the retrieval-augmented arm, 1,558 of its 5,418 cited observations name the first entity past character 200, and 1,698 observations lose their citation entirely under the cut. Its mean response ran 692 characters against a hard 200 for the others.

### 4.5 What we now do

The window is a single, explicit decision applied to all six arms, configurable and recorded per row.

- **Primary measure.** A 200-character window across all arms. This preserves comparability with the 49 days already collected and is the only definition under which the entire series is homogeneous. It is reported as head-of-response citation, with that construct named.
- **Sensitivity analysis.** The whole response, where it exists. The gap between the two measures is reported per arm rather than buried in a footnote.
- **Auditability.** The full response is now persisted alongside the window. Until August 2026 it was discarded in the client, meaning none of the 80,638 observations could be re-extracted by a third party. This was the more serious of the two defects: the asymmetry was correctable because the truncated string was still the string the extractor saw, but no amount of care recovers text that was never stored.

Historical rows keep their original columns untouched and gain harmonized ones alongside. Nothing is overwritten, and the transformation is a script that anyone can re-run.

## 5. Instrumentation

### 5.1 Entity extraction

Extraction uses word-boundary matching against the cohort, with four refinements that a naive implementation lacks:

**Normalization.** A dual pass over both the composed and decomposed Unicode forms, so that "Itaú" in a Portuguese answer and "Itau" in an English one resolve to the same entity.

**Aliases.** A single-source alias dictionary maps surface forms to canonical entities, so "BTG" and "BTG Pactual" do not count as different firms.

**Ambiguity guards.** Entities whose names are ordinary words require their canonical full form. "Inter" alone does not match; "Banco Inter" does. Without this, Portuguese text produces false positives at a rate that swamps the signal.

**Stop contexts.** A dictionary of contexts in which a matching string is not the entity, the clearest case being "99" the ride-hailing firm against "99" the number.

Markup is stripped before matching, since bold markers and bracketed reference numerals otherwise break boundary detection.

### 5.2 Elicitation mode

Queries are sent as plain natural-language prompts, with no system prompt instructing the model to produce structured output, and entity extraction happens post hoc over the returned text.

This is a deliberate choice against the alternative of asking models to return a JSON list of the entities they cited. Structured elicitation is more convenient and far easier to parse, but it changes the task: the model is no longer answering a consumer question, it is completing an annotation exercise, and the entities it lists are a self-report rather than an observation. Our instrument supports both modes, and the codebase retains a dual collector that runs the same query both ways to measure their divergence. That validation has not yet been run at scale, and §9 lists it as the principal open threat to construct validity.

### 5.3 Fictitious-entity calibration and the refusal problem

Adversarial probes name a decoy and ask the model about it. The intended measurement is whether the model fabricates a description of an entity that does not exist.

Our original implementation flagged a hallucination whenever the decoy's name occurred in the response text. This is wrong in a specific and consequential way: the probe puts the name in the prompt, so any response that engages with the question at all — including a refusal — contains it. Of 15,993 responses flagged as hallucinations, 67.4% carried an explicit refusal marker, and the sample includes a model stating plainly that the named institution is not a real or registered financial institution in Brazil. Counting that as a hallucination inverts the measurement.

The corrected instrument distinguishes three outcomes, which we treat as a taxonomy rather than a binary:

1. **Ontological refusal** — the model states the entity does not exist. The strongest correct response.
2. **Epistemic refusal** — the model states it lacks information, typically citing a training cutoff. Correct in effect, weaker in kind: it declines without asserting non-existence.
3. **Fabrication** — the model describes products, history or positioning for an entity that has none.

Only the third is a hallucination. Reporting a false-positive rate that pools all three, as our earlier pipeline did, produces a figure near 97% where the defensible figure is closer to a third of that. We report the taxonomy rather than the collapsed rate.

The probe stratum previously excluded the retrieval-augmented arm entirely, because provider routing sent only a subset of query categories to it and the calibration category was not among them. This has been corrected. The exclusion had removed the most informative case from the hypothesis: an engine that searches the web before answering has evidence available that a purely parametric model does not, and whether it uses that evidence to refuse is precisely the question worth asking.

## 6. Pipeline and reproducibility

Collection runs as a scheduled workflow whose steps are public and whose logs are retained. Six properties are load-bearing for reproducibility:

**Fail-loud preflight.** Before any collection, every mandatory engine is probed. If one fails authentication or has exhausted its credit, the run aborts rather than recording a day with five of six arms. Partial days are more damaging than missing days: they enter the series looking complete.

**Per-vertical fail-loud.** If any vertical fails, the run exits non-zero. Partial coverage produces small-cell warnings in the affected vertical that are easy to misread as a finding.

**Post-run validation.** A standalone validator confirms that every mandatory engine produced rows in the run, distinguishing a design-driven skip from an API failure.

**Response hashing.** Every response is hashed. Identical hashes for the same query and model version indicate caching or determinism rather than independent observation, and the hash distribution is the drift signal described in §3.3.

**Redundant persistence.** The database is mirrored off-site with an integrity guard holding a high-water mark, so a restore cannot silently shrink the dataset. This guard exists because an earlier failure did exactly that.

**Cost ceiling.** Per-provider budgets with a circuit breaker. This is a methodological control as much as a financial one: an unbounded run that exhausts a provider mid-collection produces a truncated day that looks like a complete one.

The dataset, the collection code, the query battery and the cohort definition are public, and every reported figure in this paper is reproducible from the released artifacts.

## 7. Missingness and series events

### 7.1 The ledger

Longitudinal collection against commercial APIs fails: providers return errors, credit runs out, payload validation changes without notice. A study that imputes those gaps, or quietly reports only the days that worked, misrepresents its own series.

We impute nothing. Every gap is recorded in a ledger with its date, extent and root cause, and marked in the run table with status `aborted`. As of this writing the series holds 49 days with data against 296 aborted runs — a ratio we report rather than hide, because it is the honest denominator for any claim about temporal stability.

Analysis weights days by coverage, with a random intercept per collection date. Days with partial coverage enter a sensitivity analysis reported with and without them. Total gaps are excluded from the formal analytic window.

### 7.2 Series events

Four changes to the instrument have occurred during collection. Each is dated, recorded, and carried into the analysis as a stratification boundary rather than averaged over:

**2026-06-17 — Gemini model and reasoning budget.** The arm moved from `gemini-2.5-pro` to `gemini-2.5-flash` with internal reasoning disabled. Pre- and post-boundary observations in this arm are not comparable.

**2026-08-19 — fifth arm replaced.** The provider retired `llama-3.3-70b-versatile`; the arm was replaced by `grok-4.6`. This is a change of engine, not of configuration, and the two are not a continuous series.

**2026-08-31 — observation window unified.** Described in §4. Affects the retrieval-augmented arm only; the other five are unchanged by construction, which the zero-deltas in §4.3 demonstrate.

**2026-08-31 — Grok reasoning effort.** The arm now runs with reduced reasoning effort. Reasoning effort is a generation parameter, so the 206 observations collected under the previous setting are a separate stratum. Because the boundary falls at 206 of roughly 18,000 per-arm observations, we discard that day for this arm rather than stratify.

Publishing these boundaries is the point. An instrument that changed four times in five months and reported a single pooled series would be reporting an average over four different instruments.

## 8. Analysis plan

The plan is fixed before the confirmatory window closes and is recorded here for that reason.

**H1 — vertical asymmetry.** Citation rates differ across verticals. Tested as a likelihood-ratio test on the vertical fixed effect in a mixed-effects logistic model with random intercepts per query and per collection date. Minimum substantively meaningful effect: Cramér's V ≥ 0.15.

**H2 — false-positive baseline.** The fabrication rate on fictitious entities, using the §5.3 taxonomy rather than name occurrence, differs across engines. Tested across all six arms including the retrieval-augmented one. Pre-registered directional expectation: the RAG arm fabricates less, having retrieval evidence available.

**H3 — inter-engine agreement.** Agreement on cited entity sets across the panel, by Fleiss kappa on the rectangular query × engine panel, computed separately per vertical.

**H4 — intra-engine temporal stability.** At least one engine shows a non-stationary citation rate across the window, as a significant slope on day index per engine after false-discovery-rate correction.

**H5 — directive inflation.** Directive queries yield higher citation rates than exploratory ones, with Cohen's h as effect size.

**H6 — window sensitivity.** New, and following directly from §4: the difference between head-of-response and whole-response citation rates is larger for retrieval-augmented than for parametric engines. This is testable only because the full response is now persisted, and it converts the defect described in this paper into a measurable claim.

Multiplicity across the comparison family is handled by Benjamini-Hochberg. Cluster-robust standard errors account for repeated queries. Where cell counts fall below 30, estimates are reported as descriptive with no inferential claim.

Any analysis not listed here is labeled exploratory and reported without p-values.

## 9. Threats to validity

**Construct validity — elicitation mode.** Post-hoc extraction over natural text is closer to what a user sees than structured elicitation, but we have not yet measured how far the two diverge at scale. The dual collector exists and the comparison is the highest-priority open item. Until it runs, our results characterize natural-mode answers and should not be assumed to transfer to structured-output settings.

**Construct validity — window choice.** Head-of-response citation is a defensible construct but it is a choice. Every headline figure is reported under both windows for this reason.

**Internal validity — instrument changes.** Four series events in five months. Each is dated and stratified, but a reader should treat cross-boundary comparisons within an affected arm as descriptive.

**Internal validity — unequal sampling.** Provider routing sends the retrieval-augmented arm roughly half the canonical battery, on cost grounds. Its per-cell power is correspondingly lower, and this is reported rather than corrected by weighting.

**External validity — market and language.** The cohort is Brazilian and the battery is Portuguese and English. Vertical asymmetries may reflect the composition of Brazilian web corpora rather than a general property of the models.

**External validity — model tier.** The panel uses small, low-cost models, which is what makes twice-daily collection over 90 days affordable. Flagship models may behave differently, and the quarterly scaling observation exists to test that at low frequency rather than to claim it.

**Statistical conclusion validity — missingness.** 49 days with data against 296 aborted runs. The gaps are not missing at random: they cluster around provider credit exhaustion, which correlates with cost, which correlates with response length. We report the ledger and weight by coverage; we do not claim the mechanism is ignorable.

## 10. Discussion

The finding we would ask a reader to carry away is not that our pipeline had a defect. It is that the defect was invisible to every check the pipeline ran on itself, and that the checks were not weak ones. Six arms produced rows every day. The language split held at exactly 50/50. Probes were marked. Response hashes varied. Two hundred and twenty-three tests passed. None of this could detect that one arm was being measured on a different amount of text than the others, because none of it asked what the extractor was reading.

Measurement defects of this shape are likely to be common in citation studies, for a structural reason: the window is usually not a design decision at all. It is the incidental consequence of how a particular provider adapter was written, often for reasons of cost or log volume, and it therefore varies exactly where studies are least likely to look — between providers, which is where the comparison lives.

For the practitioner literature, the implication is direct. A citation rate reported without a window is not comparable to another citation rate, and the error is not small: 23.8 points on our data, enough to move an engine from an apparent outlier to a member of the same family. For the research literature, the implication is that window should join model version and prompt text as a parameter reported by default.

We publish this protocol before our confirmatory results so that the analysis plan precedes the estimates, and so that the window is on record as a declared parameter rather than as something we settled after seeing which value produced the more interesting finding.

## 11. Data and code availability

Dataset, collection code, query battery, cohort definition and the harmonization script are public at `github.com/alexandrebrt14-sys/papers`. Collection logs and the missingness ledger are retained with the workflow runs. A versioned dataset snapshot is deposited with a persistent identifier at the close of the confirmatory window.

## 12. Declaration of competing interest

Alexandre Caramaschi is Chief Strategy Officer of Nuvini (Nasdaq: NVNI). This work is conducted and published in his capacity as Founder of Brasil GEO and does not represent a position of Nuvini. Brasil GEO provides generative engine optimization services commercially, which is a competing interest with respect to research on generative engine citation behavior. The cohort was fixed before collection began and contains no Brasil GEO client selected for that reason; the query battery, the analysis plan and the series events are public and were registered in the repository before the confirmatory window closed.

No external funding supported this work. API costs were borne by the author.
