# Measuring Entity Citation in Generative Engines: The BRGEO-1 Protocol and a Five-Month Field Record

**Alexandre Caramaschi**

Brasil GEO, São Paulo, Brazil · ORCID [0009-0004-9150-485X](https://orcid.org/0009-0004-9150-485X)

Custodian of the specification: Brasil GEO · Version 2.0 · September 2026

---

## Highlights

- Six declared parameters decide whether two citation rates can be compared.
- Whole-response reading raises citation rates by 22.95 to 55.73 points.
- None of 2,225 paired observations lost a citation under a wider window.
- Three engines on one battery agree at Fleiss kappa 0.086 over 9,129 cells.
- Prompt clustering cuts 68,624 observations to an effective 1,083.

## Abstract

Citation rates from generative engines travel as comparable figures while the conditions producing them stay unstated, so two honest measurements of the same firm disagree with no way to adjudicate. BRGEO-1 declares six: observation window, cohort, query battery, engine panel with pinned versions, generation configuration and entity matching rule. On 2,225 matched observations, reading the whole response instead of the first 200 characters raised the citation rate by 22.95 to 55.73 points on five engines, with no observation losing its citation. Three engines running the full battery agree at a Fleiss kappa of 0.086. A multilevel model over 38,195 responses puts 45.6% of the variance at the prompt, 34.9% at the engine and 0.03% at the collection day, and the four factors the battery was balanced on explain under 1% of the variance between prompts, so declaring a battery is not the same as characterising it. Clustering by prompt gives a design effect of 63.3, cutting the effective sample to 1,083. A composite index of the same components ranks entities at correlations from 0.752 to 0.985 across defensible aggregations, so the specification constrains observation and leaves aggregation free. No inter-implementation exercise has been run, so comparability remains a design argument.

**Keywords:** generative engine optimization; measurement standard; entity citation; large language models; construct validity; retrieval-augmented generation

**JEL classification:** C81; C83; L86; M31

---

## 1. Introduction

### 1.1 The number everyone reports and nobody defines

The quantity this market sells has no agreed definition, and the size of the resulting ambiguity can be measured. A consumer who once read ten ranked links now reads one answer, and the empirical comparison of classical search against Gemini and AI Overviews presented at SIGIR 2026 gives that shift a shape [1]. The displacement carries a measured cost on the other side. A difference-in-differences design exploiting the staggered geographic rollout of AI Overviews estimates that default availability reduced monthly external-search referrals to English Wikipedia by 5.45% and 4.82% against the same articles in German and French [2]. Firms named in a generated answer inherit attention that a results page used to spread across ten positions.

An industry formed around that inheritance in under two years. Agencies sell placement in generated answers, vendors sell dashboards that track it, and boards ask for one number. The number is almost always the citation rate: the share of prompts in which a model names a given firm. Movement in that traffic is easy to misread. A single-domain log study with untreated pages on the same domain as a contemporaneous control found ChatGPT referrals to treated pages growing 5.7-fold while untreated pages grew 3.5-fold over the same window, so most of the headline movement was platform growth [3].

Two vendors measuring the same firm in the same week report different citation rates, and neither need be dishonest. They asked different questions, of different models, on different days, and read different amounts of each answer before deciding that the firm was named. The last of those four is the condition §6.5 measures, and §2.8 records that whether published studies declare it has not been surveyed here. The series reported here holds 68,624 canonical observations, collected on 53 days between 2026-04-23 and 2026-09-08 under one 192-query battery and one 127-entity cohort. Across it the panel rate runs from 1.86% on one engine to 52.03% on another under a single 200-character window (§9), and the gap survives the reduction of same-day replicates to one cell per engine, query and day, where the two arms sit at 1.91% over 9,455 cells and 53.09% over 4,737. The two arms do not answer the same battery: the low arm receives all 192 queries and the high one 96, from which three of the six semantic categories are absent, which is itself a declared parameter value and not a difference between the engines. On the 2,225 observations for which the whole response was retained, reading to the end of the response instead of stopping at character 200 moves the rate by 22.95 to 55.73 percentage points, with no observation in any arm losing its citation (§6.5).

A young measurement field in this condition has an ordinary remedy: a protocol that fixes the conditions under which a number is produced, published openly so that anyone can meet it and any reader can check whether it was met. The field has asked for one in its own venue. A position paper at ICML 2026 names concentrated influence under low contestability, undisclosed commercial influence inside evidence and reasoning, and evaluation asymmetries between offline setups and deployed systems as the risks of the transition, and argues for answer-level governance and deployment-aligned metrics [4]. The case for pinning conditions has an empirical precedent as well: a reproduction study of published TikTok audits at SIGIR 2025 found poor reproducibility and short-term validity in the original findings, traced to conditions those studies had not fixed [5]. Commercial placement has now begun to appear inside the answers themselves [6], which raises what an unstandardised metric costs.

BRGEO-1 is an opaque identifier: the prefix denotes the organisation that maintains the specification, in the manner of an IETF or W3C document number, and carries no geographic scope. The protocol is written for any market and any language, and §4 gives the reasons for a Brazilian reference instantiation.

### 1.2 Citation rate is an incompletely specified measurand

Metrology named this problem decades ago and supplies the term for the floor it sets. The International Vocabulary of Metrology defines a measurand as the quantity intended to be measured, and Note 1 to clause 2.3 requires, for the specification of a measurand, knowledge of the kind of quantity together with a description of the state of the phenomenon carrying it [7]. The market's definition of the citation rate satisfies the first requirement and stops there. Which prompts. Asked of which model version. Under which generation configuration. Read to which length. Under which rule for deciding that a string names the firm. Those five questions are the description of the state of the phenomenon, and a figure published without them reports a quantity whose specification is incomplete.

The six parameters of BRGEO-1 supply that description. P1 fixes the observation window, P2 the cohort the instrument can detect, P3 the query battery, P4 the engine panel with pinned model versions, P5 the generation configuration and P6 the entity matching rule (§3.1). They are the detail the vocabulary requires before the quantity exists as a measurand, which is why §3 states them with normative force and attaches a failure mode to each.

The consequence for uncertainty is sharper than a reader might expect. Clause 2.27 defines definitional uncertainty as the component of measurement uncertainty resulting from the finite amount of detail in the definition of a measurand; Note 1 makes it the practical minimum achievable, and Note 2 states that any change in the descriptive detail leads to another definitional uncertainty [7]. The window result of §6 is an instance of Note 2. Changing the number of characters read changes the descriptive detail, so the two figures describe two measurands, and the gap between them is not error in the ordinary sense. No sample size closes it, because the two numbers answer different questions. One is head-of-response citation. The other is whole-response citation.

Note 1 also settles what an interval computed from sample size alone is worth. Definitional uncertainty is the practical minimum, so an interval derived from the observation count is narrower than the floor whenever the dominant component never entered the budget. This study's own series shows the size of the omission: clustering by prompt instead of by observation gives a design effect of 63.3 and an effective sample of 1,083 against a nominal 68,624, widening the pooled half-width from 0.29 to 2.29 percentage points over the collection days of the series (§9), while re-reading the same stored responses to the end moves individual arms by tens of points (§6.5).

The Guide to the Expression of Uncertainty in Measurement separates components evaluated from repeated observation, Type A, from those evaluated by other means, Type B, and states that the split concerns the method of evaluation [8]. Sorted that way, the components the market reports are the Type A ones, and they are the small ones. §3 publishes an uncertainty budget on that split, where the function of a protocol becomes visible: a parameter that is fixed and published stops contributing uncertainty to comparisons between figures declaring the same value for it.

The analogy has a limit that §14 keeps in view. A citation rate has no unit, no calibration hierarchy and no true value, and the measurand is constituted by convention, which is how validity behaves for an unobservable construct [9, 10]. A convention has to be written down before anyone can argue about whether it is the right one.

### 1.3 Contributions and structure of the paper

The BRGEO-1 protocol fixes six parameters that any citation-rate claim has to declare, and a five-month record shows what happens to the number when one of them moves. Six contributions follow. §3 gives the specification: six parameters with a rationale and a failure mode each, requirement identifiers, conformance levels on an axis of attestation, the conformance claim a first party publishes, and the missingness ledger. §4 gives a reference instantiation with every value published. §5 reports how the instrument was built and broken, including seven defects that passed every automated check. §6 measures the observation window symmetrically on every arm that retained a full response, 2,225 matched observations collected between 2026-09-06 and 2026-09-08, and reports what the magnitude does to a published reading of one engine. §9 reports five months of descriptive evidence across engines, verticals, languages, query types and entity concentration. §10 defines a reporting index and publishes the evidence against leaning on it, which is the sensitivity analysis the composite-indicator literature prescribes for exactly this case [11].

The remaining sections carry the apparatus. §7 covers the calibration decoys and the refusal taxonomy, §8 the instrument drift and the missingness ledger in operation, §11 the analysis plan, §12 the ten decisions an adopter makes and the errors an adopter meets, §13 governance, §14 threats to validity, §15 the discussion and §16 the conclusions. The specification appears here ahead of the confirmatory results it will be tested by, so that the parameter values, the observation window among them, are on the record before the analysis that reads them and not after it.

## 2. Related work

### 2.1 Generative engine optimization, and the harness each study fixes for itself

BRGEO-1 works one level below the optimisation literature: it specifies the conditions under which a citation rate is a comparable quantity. That literature asks how to raise the probability that a source is selected, and each study fixes an evaluation harness adequate to its own comparison. Aggarwal and colleagues introduced the term and the GEO-bench suite at KDD 2024, evaluating content modifications against generative engines [12]. The line extends to commerce with the E-GEO testbed [13], to content organisation with structural feature engineering [14], and to the features that move source selection in open-domain generative search [15]. Nimase and colleagues unify black-box prompt attacks, white-box gradient attacks and ten white-hat content strategies under one scoring protocol over five datasets against a fixed open-weight ranker [16]; their benchmark shares a name with the suite of Aggarwal and colleagues and is a separate artefact, which matters to a reader who knows one and assumes the other.

Holding the harness constant across arms is what a controlled comparison inside one study requires, and the harness is then reported as an implementation detail. Two studies built on different harnesses produce figures that cannot be read side by side, and nothing in the optimisation literature prevents that, because preventing it was never its question. The ICML 2026 position paper cited in §1.1 argues for black-box auditing of material influence and for metrics aligned with deployed systems [4], which is a requirement on the measurement layer and not on the content layer.

### 2.2 Measuring visibility and citation: a line that has converged on sampling

During 2026 several authors began treating AI visibility as a statistical estimation problem, and they have converged on one axis. Sielinski treats visibility metrics as sample estimators, showing that apparent differences between domains often fall inside measurement noise [17], then derives convergence criteria, rank stability and structural sufficiency, for deciding when enough data has been collected [18]. Schulte and colleagues show that generative search results vary between runs and over time and argue for characterising visibility as a distribution [19]. Zhang and colleagues separate citation selection, where a platform chooses a source, from citation absorption, where the cited page contributes language and evidence to the answer [20]. Varga distinguishes raw mention from verified mention [21] and Kumar reports brand visibility at scale [22]. The survey covering 2023 to 2026 finds terminology, metrics and evidentiary standards heterogeneous, with no reviewed technique showing a stable effect that holds longitudinally and across platforms [23].

Four recent measurements establish how far the conditions move the answer. A crossed random-effects decomposition over 12,933 responses, 20 brands, 8 languages and 3 models reports query language as the largest systematic factor in response-level brand outcomes [24]. Across 1,909 English-only queries on six models and 30 brands, Chinese-developed models mention brands at 88.9% against 58.3% for international models, a gap of 30.6 points under identical prompts [25]. Querying 66 brands in 12 languages over 35,640 responses gives a cross-language mean cosine similarity of 0.825 [26], and three skincare experiments report well-known brands recommended in 100% of responses when product specifications are held identical across three models [27]. Eight of the twelve 2026 works this section cites are single-author preprints without peer review; the peer-reviewed anchors are [12], [4], [1] and [5]. Every figure this section attributes to a preprint is reported as that work's own claim, and no figure in §§3 to 16 of this paper depends on one.

The Dice Roll Method is the other published attempt to standardise measurement of entity mention in generative engines, and the two standards are disjoint. It formalises repeated-query auditing of brand recommendations over a reanalysis of roughly 190,000 observations across more than 270 brands and six languages, and derives three tiers of iteration guidance from a generalizability-theory decision study, reporting G = 0.58 at five iterations and G = 0.74 at ten [28]. It answers how many times a query is repeated and when the resulting measure is reliable, and is agnostic about the cohort, the panel and the extraction rule. BRGEO-1 answers which text is read, which entities can be detected, which queries are asked, which model version answered, under which generation configuration and by which matching rule, and is agnostic about how many repetitions to buy. A measurement declared under both is better specified than one declared under either, and §12 recommends the Dice Roll iteration tiers as a non-normative companion. Generalizability theory is also the vocabulary §9 uses for its variance decomposition.

**Table 1.** Parameters each of the two published protocols fixes, as stated in its own specification document. No observations: the entries are specification content, read from the source documents on 2026-09-11.

| Condition of measurement | Dice Roll Method [28] | BRGEO-1 (§3.1) |
|---|---|---|
| Number of repetitions per query | fixed, in three tiers by brand recognition | not constrained |
| Reliability threshold for the resulting measure | fixed, as a generalizability coefficient | not constrained |
| Variance decomposition of the outcome | prescribed, four components | recommended, §9 |
| Observation window over the response | not constrained | P1, uniform across the panel |
| Cohort of detectable entities, with decoys | not constrained | P2, fixed before collection |
| Query battery and its factorial balance | not constrained | P3 |
| Engine panel and pinned model versions | model version enters as a variance component | P4, recorded per observation |
| Generation configuration | not constrained | P5, published with the figure |
| Entity matching rule | not constrained | P6 |

### 2.3 Attribution and verifiability measure a different object

Entity citation as this paper defines it sits upstream of the attribution question, which asks whether a cited source supports what the answer says and therefore presupposes the naming. Rashkin and colleagues give the Attributable to Identified Sources framework [29], Liu and colleagues establish citation precision and recall as auditable metrics for generative search engines [30], and Gao and colleagues provide the ALCE benchmark for citation generation [31]. Audits of source-cited responses report systematic gaps between claimed and actual verifiability [32, 33]. The largest recent instance decomposes AI Overviews at claim level: 55,393 trending queries across 19 topical categories over the 40 days from 13 March to 21 April 2026, with activation at 13.7% of queries overall and 64.7% of question-form queries, nearly 30% of cited domains absent from the co-displayed first-page results, and 11.0% of 98,020 atomic claims unsupported by the pages cited for them [34]. The survey of generative information retrieval evaluation covers the same ground from both directions, models as assessors and generative systems as objects of assessment [35].

The upstream quantity is whether the firm appears in the answer at all, and it is the one the commercial market reports almost exclusively, which is what gives standardising it practical consequence. The attribution line remains the methodological neighbour, because the discipline of publishing an explicit matching and support criterion alongside a figure comes from it, and P6 is that discipline applied to entity names.

### 2.4 Fictitious entities as a target of measurement

Non-existent entities are an established measurement target with a mature literature behind them. PhantomBench is built from non-existent terms and entities derived from real concepts and reports that frontier models frequently fail to abstain when a question presupposes existence [36]. HalluLens includes a NonExistentRefusal task [37], AbstentionBench benchmarks abstention on unanswerable questions [38], and knowledge-aware refusal in factual tasks is measured on its own terms [39]. The abstention survey in TACL organises the field and supplies the categories against which any new taxonomy is read [40]. WildHallucinations moves the unit of analysis to real-world entity queries [41], large-scale evidence from non-existent citations shows what fabricated items look like in the wild [42], and a model's own signal about fabricated references has been measured directly [43]. The hallucination surveys map the surrounding work [44, 45].

In each of those designs the fictitious item is what is being measured. BRGEO-1 puts sixteen decoys, each verified as non-existent against registry, mapping and court records before collection, inside the measured cohort, so that the citation rate carries a false-positive floor produced by the run that produced the rate. Across the 68,624 canonical observations of the series no decoy was named spontaneously on any engine, giving a 95% Wilson upper bound of 0.0056% on that floor (§7.1). The refusal taxonomy of §7.2 is stated against the categories of [40] instead of being proposed on its own, and §7.2 reports what the first implementation did when it counted the decoy name wherever it appeared: 96.7% of 17,919 probe observations were flagged, and 66.8% of the 17,328 flagged responses with non-empty text carry an explicit refusal marker.

### 2.5 Measurement validity, benchmark critique and the arithmetic of composites

Benchmark critique supplies the warrant for treating a widely reported quantity as a construct that has to be modelled. Validity is a property of the relation between an attribute and a measurement outcome [9], and the import of measurement modelling into computing makes that requirement operational for unobservable constructs [10]. Benchmarks acquire authority disconnected from what they measure [46, 47], BLEU is the canonical case study [48], and a review of 445 benchmarks finds construct-validity problems to be structural [49]. Two results sit closest to this paper's own: decoding parameters, seed and prompt format move reasoning results far enough to reverse published conclusions [50], and chat interface and API diverge, with web search shifting accuracy by up to eight percentage points, which makes access condition a measurement parameter [51]. A validity-centred framework separates the attestation axis from the validity axis [52], which is the distinction the conformance levels of §3.3 rest on, and a 2026 position paper argues that aggregate scores are the root cause of underspecified item selection and that item-level data release should be default infrastructure [53].

The composite-indicator literature prescribes the test §10 runs. The OECD handbook sets out the construction choices [54], and the foundational statement requires every composite to travel with an uncertainty and sensitivity analysis across the choices a defender would accept [11]. Nominal weights are shown not to be the weights that drive the ranking, with importance measures that recover the effective ones [55]; the review of weighting, aggregation and robustness gives the grounds for choosing the geometric mean [56]; and composite indicators serve advocacy as often as analysis, which a custodian selling services in the measured domain has to answer [57]. §10 reports rank correlations between four defensible aggregations of the same three components falling to 0.752 across 66 entities, and a variance decomposition in which coverage carries 72.4% of the variance of the log index, which is the nominal-against-effective weight gap in this instrument. At least one index of this kind is already in circulation: one recent study proposes a Category Ownership Index, a Competitive Vacuum Index and a Displacement Score from 3,750 responses across 50 brands, five industries and three models [58].

### 2.6 Reporting standards and specifications that became standards by adoption

Structured declaration of the conditions of an experiment is a converging practice across three communities. In information retrieval, `ir_metadata` attaches an extensible metadata schema to experiment results [59] following the PRIMAD model of components that affect reproducibility [60], whose current development keeps the line active [61], and `repro_eval` turns reproducibility measures into runnable software [62], which is the nearest existing model for the conformance test suite §13 promises. In evaluation reporting, benchmark metadata, run data and model metadata are composed into one record with interpretive signals [63, 64]. In documentation, model cards [65] and datasheets [66] set the precedent for structured disclosure, and the algorithm-auditing methodology that underlies this design includes the requirement to record collection failures [67], now extended by automated black-box auditing at scale [68] and by domain-specific audits of AI Overviews and featured snippets [69].

For the shape of an open specification that becomes a standard through adoption rather than authority, HELM [70], MTEB [71] and BEIR [72] are the precedents, and MMTEB shows the same specification growing by community contribution [73]. The institutional genealogy runs through the TREC deep learning track [74], the demonstration that relative system ordering survives judge variability provided the protocol is fixed [75], which is the strongest available answer to the objection that non-deterministic answers cannot be measured, the test collection built on query variability [76], and artifact review and badging in computing conferences [77]. The cautionary case is the reproduction study at SIGIR 2025 [5]: self-declared conformance is open to the same failure, and §13 says so. The normative vocabulary of §3.2 comes from BCP 14 [78, 79], the attestation vocabulary of §3.3 from conformity-assessment terminology [80], the interlaboratory design named in §13 from the accuracy standard [81], and the measurement vocabulary of §1.2 from [7] and [8]; benchmarking, standardisation and certification for AI systems have been connected in the same frame [82].

### 2.7 Position effects in the input, and truncation of the output by the instrument

What this paper adds about position is a property of the instrument rather than of the models: the conversion P1 describes (§3.1) moves the citation rate by 22.95 to 55.73 percentage points across five arms on 2,225 matched observations (§6.5). Position within a prompt is not neutral, and the output analogue is now measured as well. Models use information in long contexts unevenly [83], serial position effects appear across tasks and models [84], and most of those effects are model-specific with language-specific nuance, some models favouring later positions against a universal early-token account [85]. On the output side, models used as zero-shot rankers are sensitive to candidate order and to popularity, so the ordering they emit is not a neutral function of the input [86]; position bias in recommendation output is measured [87] and shown to undermine preference consistency in listwise reranking [88]. Randomising one hundred hotel listings across 5,000 agent sessions against four models finds that position predicts inspection weakly and non-monotonically, and that whether position reaches the choice stage is model-specific in a way that tracks neither provider nor capability [89].

Output-side position effects are therefore established, and this paper claims nothing new about them. §6.4 reports susceptibility to a narrow window as a property of the model with the same shape as the heterogeneity of [89]: it tracks neither architectural class nor provider.

### 2.8 What the literature leaves unmeasured

The published protocols in this space fix how often a query is asked and how the spread of the answers is characterised; the aperture through which each answer is read is not among the conditions any of them fixes. The consequence is arithmetic. A variance decomposition that partitions response-level variance into resampling, paraphrase, model identity and language treats the response as the unit observed [24]. Where a pipeline truncates the response at a length that differs between providers, the four components are computed on four different units, and their comparison across arms inherits that difference without recording it. The sampling question and the aperture question are therefore not parallel: one is answered on top of an answer to the other.

Three further gaps follow from the same reading. The attribution literature measures support for a claim once a source has been named [29, 30, 34] and does not reach the prior question of whether the entity was named at all. The abstention literature measures a model's failure on non-existent items [36, 40] and does not use them to floor a visibility measurement taken in the same run. The composite-indicator literature prescribes a sensitivity analysis for exactly the construction choices a reporting index makes [11, 55], and the indices now circulating in this market are published without one [58].

Table 2 maps what each line of work states that it constrains onto the six parameters of §3.1. It reads each work's own specification of its conditions and is not a survey of undeclared practice: whether published visibility studies declare an extraction window at all has not been surveyed here, §14 records that as an open item, and this paper therefore makes no claim about how common an undeclared window is outside this pipeline.

**Table 2.** Conditions of observation each line of work states that it constrains, mapped to the parameters of §3.1. No observations: entries record the specification content of the cited works.

| Line of work | What it states that it constrains | Parameters of §3.1 it reaches |
|---|---|---|
| GEO optimisation [12, 13, 14, 15, 16] | content modification and the scoring of its effect, on a harness fixed per study | none across studies |
| Visibility as estimation [17, 18, 19] | sample size, convergence and the reporting of a distribution | none |
| Repeated-query auditing [28, 24] | iterations per query, reliability threshold, variance components | P4, as a variance component |
| Attribution [29, 30, 31, 34] | the support criterion linking a claim to a cited source | P6, for sources rather than entities |
| Abstention and non-existence [36, 37, 38, 40] | the item set of non-existent entities and the refusal outcome | P2, as a target rather than a floor |
| Reporting schemas [59, 63, 64, 65, 66] | the fields a report carries | the act of declaring, not the values |
| Composite indicators [54, 11, 55, 56] | aggregation, weighting and the sensitivity analysis around them | none; §10 applies them downstream |
| BRGEO-1 (§3) | the six conditions under which the count is taken | P1 to P6 |

The row that the others leave blank is where BRGEO-1 sits, and it arrives with its failures attached: six parameters with a failure mode each (§3), seven defects that passed every automated check (§5), the window measured symmetrically on 2,225 matched observations (§6.5), five months of descriptive evidence (§9), and the evidence against the reporting index, published by its custodian (§10).

---


# Block B — §3 The BRGEO-1 specification · §4 Reference instantiation · §12 Adopting the protocol

Draft for the journal-length manuscript. Numbers are drawn from `../tables/TABLES.md`, `../tables/NUMBERS.md` and `../stats/S5-window-validity.md` on the database snapshot whose latest `citations.timestamp` is 2026-09-08T19:30:57Z. Citations are by key; the full entry for every key appears at the end of this file.

---

## 3. The BRGEO-1 specification

A citation rate reported without its conditions is a precise measurement of a quantity the reader cannot identify. Metrology names the gap: VIM 2.3 Note 1 requires that the specification of a measurand include a description of the state of the phenomenon carrying the quantity, and VIM 2.27 calls the residual from an incomplete specification definitional uncertainty [7]. §1.2 sets out the two notes to clause 2.27 and what they cost an interval computed from sample size alone, which estimates a term sitting below a floor the budget never entered.

That is the argument for making the six parameters normative rather than advisory. A recommendation that an implementer may decline leaves the descriptive detail free, and free descriptive detail means every implementation measures a different measurand while publishing the same word. The parameters below are the minimum detail under which two figures refer to the same quantity.

### 3.1 The six declared parameters

*This subsection is normative.*

A figure is measured under BRGEO-1 when all six parameters are fixed before collection, published with the figure, and versioned `[BRGEO1-M-012]`.

**Table 3.** The six declared parameters: what each fixes, what goes wrong when it is left implicit, and what a conforming implementation publishes.

| | Parameter | Failure mode when implicit | Published with the figure |
|---|---|---|---|
| P1 | Observation window | The instrument silently measures head-of-response citation and reports it as whole-response citation, at a cut-off that differs between providers | Window in characters, applied identically to every arm; the recall target it meets |
| P2 | Cohort | The rate has no false-positive floor and no stated detection set, so absence of a name is unreadable | Entity list with tier, legal status and decoys, dated before first collection |
| P3 | Query battery | The battery encodes the author's assumptions about what users ask, and stratum effects load onto engine effects | The full battery with its factorial invariants |
| P4 | Engine panel with pinned versions | A change in the world cannot be separated from a change in the instrument | Model version string recorded on every observation, with the dates of every boundary |
| P5 | Generation configuration | A parameter that moves latency, cost and output length varies without changing the model identifier | Temperature, sampling parameters, seed where available, output caps, reasoning effort, system prompt |
| P6 | Entity matching rule | Two implementations produce different figures from identical responses while both claiming conformance | Matching form, alias table, ambiguity policy, exclusion contexts, boundary policy, and the rate with each dictionary removed |

**P1, the observation window.** Entity extraction runs over a string, and that string is whatever the pipeline retained rather than the model's answer. Its length is the observation window `[BRGEO1-M-001]`, and it MUST be identical across every arm of the panel `[BRGEO1-M-002]`. The parameter carries a substantive reading in either setting: a narrow window measures whether the entity appears in the opening a reader sees before deciding to continue, and a full window measures whether it appears at all. Leaving the choice implicit is the failure, because the window is usually not a design decision. It is an incidental consequence of how a provider adapter was written, for reasons of cost or log volume, and it therefore varies between providers, which is where the comparison lives. The measured magnitude is in §6; the short statement is that on 2,225 canonical observations collected from 2026-09-06 to 2026-09-08, moving from 200 characters to the whole response changed the citation rate by between 22.95 and 55.73 percentage points on five arms, with zero reversals. Position within model output is a measured phenomenon in the recommendation literature [86, 88, 89]; what P1 adds is that the instrument's truncation of that output is an unreported measurement parameter, which is a narrower claim and a checkable one.

**P2, the cohort.** The cohort is the set of entities the instrument can detect, fixed before collection with tier stratification, annotated legal status, and fictitious calibration decoys `[BRGEO1-M-003]`. Decoys are required `[BRGEO1-M-004]`: without them the rate has no empirical floor from the run that produced it, and a matcher that fires on ordinary prose is indistinguishable from a model that names firms. An unfixed cohort fails in a second way that the literature has now measured. Brands absent from training corpora have no presence in model answers regardless of quality [25], and a well-known brand is recommended in every response when product specifications are held identical, with that dominance collapsing under a rating advantage of less than a tenth of a star for a competitor [27], so a cohort assembled after seeing the answers reports an artefact of its own assembly. Publishing the cohort with a date before first collection is what makes that objection answerable.

**P3, the query battery.** The battery is a factorial design over dimensions known to move citation behaviour, balanced rather than convenience-sampled, and published in full `[BRGEO1-M-005]`. Query language is reported as the largest systematic factor in a crossed variance decomposition of brand answers over 12,933 responses [24], and query variability has been treated as a first-class property of a test collection since UQV100 [76]. An unbalanced battery does not announce itself: it produces a rate that is a weighted average over strata the reader cannot see, and it makes an engine that was routed a discovery-heavy subset look more generous than one that was not. Publishing the invariants makes a battery checkable by a second party without making two balanced batteries interchangeable, since the four factors this battery balances account for none of the variance between its own prompts, which §9.2 measures and row 23 of Table 37 records.

**P4, the engine panel with pinned versions.** Every engine MUST be identified by an explicit model version string recorded on every observation, with the date of every panel change `[BRGEO1-M-006]`. Providers alter the model behind a stable product name, and the behaviour of a commercial model under one name has been shown to move materially over a few months [90]. A series recording only the product name cannot separate a change in the world from a change in the instrument, and it also cannot be repaired later, because the row does not carry the evidence. Naming the product is exactly what P4 declares insufficient, which is why every table in this manuscript carries the pinned identifier rather than the brand.

**P5, the generation configuration.** Temperature, nucleus sampling parameter, seed where available, output limits, reasoning effort where the provider exposes it, and the system prompt are published with the figure `[BRGEO1-M-007]`. The requirement earns its place from the field record: two of the four series events in the reference instantiation were caused by changing generation configuration without changing the model identifier. The limit of the requirement has to be conceded in the same breath. Pinning temperature at zero does not buy determinism in a hosted model, because silent updates, numerical rounding and expert routing keep the output variable [91, 92, 93]. P5 pins the request and not the response. The consequence is procedural: regeneration cannot serve as the reproduction path, and the stored response becomes the only artefact a third party can re-measure. That argument is the reason retention of the full response is a requirement in its own right `[BRGEO1-S-001]` rather than a convenience.

**P6, the entity matching rule.** The rule maps a response to the set of entities it names, and it is declared in full: matching form, alias table, disambiguation policy, exclusion contexts, and the boundary policy for a mention straddling the window edge `[BRGEO1-M-008]`. Two implementations with different rules produce different figures under identical values of P1 to P5, which would defeat the specification. Until now that was an argument rather than a measurement. An ablation over 2,225 canonical observations collected from 2026-09-06 to 2026-09-08 gives it a magnitude: removing the alias table moved the panel rate by 0.94 percentage points at 200 characters and 0.76 on the whole response, flipping 21 and 17 observations; removing the exclusion contexts moved nothing at all, with zero flips at both windows; removing the ambiguity guard moved one observation. The effect of the alias table is concentrated on one arm, the retrieval-augmented one, which lost 5.25 points at 200 characters because short forms reproduced from sources are what aliases catch, while the parametric arms in this cohort write canonical long names. The exclusion contexts are inert for a reason a reader can check: exactly one entity in the 127-member cohort carries one, and its three patterns never fired. The magnitude, including when it is zero, is what turns a declared parameter into a checkable one, which is why the ablation is published here with its flip counts. The distribution does not transfer: an implementation whose cohort contains short or colliding surfaces should expect the opposite ordering, which is why a conforming claim publishes its own ablation `[BRGEO1-S-003]` rather than citing this one.

### 3.2 Normative language and requirement identifiers

*This subsection is normative.*

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY" and "OPTIONAL" are to be interpreted as described in BCP 14 [78, 79] when, and only when, they appear in all capitals.

Sections are marked normative or informative. Only normative content states requirements for conformance; examples and explanatory passages impose none. Requirements carry stable identifiers of the form `[BRGEO1-M-nnn]` for MUST, `[BRGEO1-S-nnn]` for SHOULD and `[BRGEO1-O-nnn]` for OPTIONAL, so that errata, audit findings and conformance claims have a fixed referent that survives renumbering of the prose.

### 3.3 Conformance levels on an attestation axis

*This subsection is normative.*

The three levels differ in who verified the figure, and in nothing else. They borrow the first-party to third-party progression of conformity assessment vocabulary [80] and the artifact badging practice of computing conferences [77]; the framework separating what an evaluation licenses from who vouches for it is the reason the axis is attestation rather than completeness [52], and the connection between benchmarking, standardisation and certification is developed for AI systems in [82].

**Table 4.** Conformance levels. Requirements are cumulative; the axis is who attests, not how complete the measurement is.

| | Level 1, Declared | Level 2, Verified | Level 3, Attested |
|---|---|---|---|
| Requirements | all MUST | all MUST and SHOULD | all MUST and SHOULD |
| Evidence | public claim with the components of §3.5 | complete evidence package, recomputable by a third party from stored responses | evidence package plus external attestation |
| Verified by | first party | first party, reproducibly | body independent of the claimant and of the maintainer |

Level 2 is unreachable without retention of the full response `[BRGEO1-S-001]`, since recomputation requires the input. The reference instantiation of §4 was therefore Level 1 for the first four months of its series and could not have claimed otherwise. It is NOT RECOMMENDED that Level 3 be required as a general procurement policy `[BRGEO1-O-001]`, because third-party attestation is not attainable at reasonable cost for every class of measurement subject, and a level scheme whose top rung is affordable only to large firms is a barrier to entry rather than an open standard.

### 3.4 Divisions, closed and open

*This subsection is normative.*

Orthogonal to level, every measurement declares a division. In the **Closed** division, window, cohort, battery, panel, generation configuration and matching rule take the values fixed by the specification or by a published profile, and figures are comparable across claimants. In the **Open** division any parameter varies from the profile, with the deviation documented; Open figures are comparable neither with each other nor with Closed figures and MUST NOT be presented as though they were `[BRGEO1-M-011]`. The division system is what keeps the specification usable by an adopter whose market or budget rules out a profile value, and it follows the practice of benchmark suites that survive by adoption rather than by authority [70, 72, 71].

### 3.5 The conformance claim

*This subsection is normative.*

A claimant publishes one page `[BRGEO1-M-010]`. The page carries the level, the division, the specification version, the six parameter values, and the evidence locations. Structured declaration of this kind is converging practice in evaluation reporting [65, 66, 59, 63, 64], and the argument for publishing the components rather than only the headline is made independently in the item-level release literature [53].

**Table 5.** Components of a BRGEO-1 conformance claim. Every row is required at Level 1; the evidence rows acquire a resolvable identifier at Level 2.

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

BRGEO-1 imputes nothing `[BRGEO1-M-009]`. Longitudinal collection against commercial interfaces fails: providers return errors, credit is exhausted, payload validation changes without notice. Every gap is recorded with its date, its extent and its cause, and it is marked in the data rather than filled or dropped. The requirement to record collection failures comes from the algorithm-auditing methodology the design follows [67], and the reason it is normative rather than good practice is that a study which reports only the days that worked has quietly selected on the instrument's own health.

Two rules make the ledger enforceable rather than decorative. First, a claim of absence requires a measurement: an entity that was never named is reported with the observation count over which it was never named, and with the ledger entry accounting for the queries that returned an error and were therefore not evaluable. Second, the analysis weights days by coverage and carries partial days into a sensitivity analysis reported with and without them, so that a reader can see the effect of the decision rather than inherit it.

The ledger also has to record its own limits. Missingness in the reference instantiation is not ignorable: gaps cluster around provider credit exhaustion, which correlates with cost, which correlates with response length, which §6 establishes correlates with citation. Coverage weighting corrects data missing at random and does not address that mechanism. Publishing the ratio is what allows a reader to discount the series; it does not repair it.

### 3.7 The uncertainty budget

*This subsection is normative.*

A conforming figure SHOULD be published with an uncertainty budget `[BRGEO1-S-004]`. The GUM classifies the evaluation of uncertainty components into Type A, estimated from a series of repeated observations, and Type B, estimated by any other means, from prior knowledge, specifications or judgement; clause 3.3.4 is explicit that the classification concerns the method of evaluation and implies no difference in the nature of the components [8]. Applied to a citation rate, the division separates the components a sample count can estimate from the components only a declared parameter removes, which is what Table 6 carries.

**Table 6.** Uncertainty budget for a citation rate under BRGEO-1, with the state of each component in the reference instantiation of §4. Type A follows GUM 3.3.5 and 4.2; Type B follows GUM 4.3. Series 2026-04-23 to 2026-09-08 except where the entry names a shorter window; day counts are the table-build count of §8.2.

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

Two readings follow, and the second is the point of publishing the table. The components the market reports are the Type A ones, and they are the small ones: the largest Type A entry here is 2.39 percentage points of typical error, against a Type B entry of 22.95 to 55.73 percentage points for the window. The protocol's function is to convert Type B components into declared constants, since a parameter that is fixed and published stops contributing to comparisons between figures that declare the same value. That is the precise sense in which BRGEO-1 produces comparability, and it is also the sense in which the claim remains untested: two components are bounded rather than estimated and one is not estimated at all. The exercise that would close the gap is an interlaboratory study in the sense of ISO 5725-2, with the discrepancy between independent implementations of the same stored responses decomposed into repeatability and between-implementation terms [81]. The variance vocabulary of generalizability theory, already used in this market to decide how many times to repeat a query [28], is the natural companion for that decomposition. The measurand itself remains constituted by convention rather than discovered, which is the standing position for unobservable constructs [10, 9], and §14 keeps that limit in view.

---

## 4. Reference instantiation

The values below are what the longitudinal study of this paper uses. They are calibration rather than specification: another adopter conforms with different values, provided the values are declared. This section is informative; the requirements it instantiates are stated in §3.

**Table 7.** Reference instantiation of the six parameters. Series 2026-04-23 to 2026-09-08, 68,624 canonical observations and 17,919 adversarial probes, 86,543 rows in total.

| Parameter | Reference value |
|---|---|
| P1 Window | 200 characters, uniform across the panel, configurable by `PAPERS_CITATION_WINDOW_CHARS`; the whole response retained since migration 0010 |
| P2 Cohort | 127 entities: 79 Brazilian firms, 32 international anchors, 16 fictitious decoys, across four verticals |
| P3 Battery | 192 canonical queries: 4 verticals × 6 semantic categories × 2 languages × 2 query types × 2 temporal frames, plus 16 adversarial probes |
| P4 Panel | 6 engines across the series and never 6 at once, versions pinned per observation (Table 8) |
| P5 Generation | Temperature 0.0; output caps by provider; reasoning disabled or reduced where the provider exposes the control; system prompt published |
| P6 Matching | Word-boundary matching with NFKD dual-pass normalisation, markup stripping, alias table, ambiguity guard requiring canonical form, and exclusion contexts |

### 4.1 Cohort construction and tier stratification

The cohort is fixed in `src/config_v2.py` and dated before the first observation of the series. Tiers are balanced with at least five long-tail firms per vertical, seven Brazilian states are represented, and `legal_status` is annotated so that a model naming a firm in judicial recovery is not pooled with one naming an active firm. In this cohort the field has almost no variance, with 110 of the 111 real members active and one, Americanas, in judicial recovery, which is why §9 does not model it. The cohort was designed to probe the awareness gap of models whose pre-training predates a firm, and it does not reach it: the most recently founded member dates from 2019, earlier than every plausible cut-off for the pinned versions, so the indicator for a firm founded after the cut-off has no cases and §9 does not fit it. The mechanism benchmark-contamination work describes from the other direction [94] therefore remains untested here, and its measured form in brand discovery is the existence gap [25]. Each of the 16 decoys was verified as non-existent against the Brazilian federal tax registry, mapping services and court records before inclusion, and §14 records the jurisdictional limit of that verification.

### 4.2 Query battery and factorial balance

The 192 canonical queries are generated from five declared axes, so the balance is a property of the construction and not of an editorial pass. The cells run 96 Portuguese and 96 English, 96 directive and 96 exploratory, 48 per vertical, with half of each cell carrying the temporal frame "em 2026" and half atemporal. English queries always name Brazil, which prevents drift toward North American and European brands. Balance is what makes the stratum contrasts readable: the largest of them, directive against exploratory, runs 25.9% against 10.0% at panel level over 34,319 and 34,305 canonical observations respectively, and it holds in every arm. Provider routing breaks the balance in one place, which is declared rather than smoothed: the retrieval-augmented arm runs 96 of the 192 queries on cost grounds, and the half it runs is the discovery-shaped half, so its category column is not comparable with the parametric arms.

### 4.3 Engine panel with pinned versions

**Table 8.** Engine panel with pinned model identifiers, architectural class and active period. Series 2026-04-23 to 2026-09-08, 68,624 canonical observations; denominator is rows of `citations` with `COALESCE(is_probe,0)=0`.

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

**Table 9.** Sensitivity of the published panel figures to two colliding cohort surfaces. Series 2026-04-23 to 2026-09-08, 68,624 canonical observations under the uniform 200-character window; denominator for the rate is all canonical observations, and for the concentration statistics the 12,329 first mentions.

| Quantity | With the two surfaces | Without |
|---|---:|---:|
| Panel citations under the uniform window | 12,329 | 11,976 |
| Panel citation rate | 17.97% | 17.45% |
| Distinct entities ever named first | 42 | 40 |
| Herfindahl-Hirschman index of first mentions | 0.1917 | 0.2023 |
| Share of first mentions held by the leader | 37.3% | 38.4% |

The affected set is 353 observations, 0.51% of the canonical panel, and in every one of them the collision is the only match, so the whole set is counted as cited for no other reason. All 353 fall in English responses, distributed as Groq 173, ChatGPT 158 and Gemini 22. The tables of this manuscript are published with the collisions left in, because those figures are what the instrument as specified produces, and because correcting the cohort here would break the correspondence with the stored series that the verification file establishes. The correction belongs to the configuration: `Involves` needs a canonical name and `Target` needs a stop context, and both require re-extraction of the series rather than a note in the text. Until that runs, this paragraph is the declared error term on every rate in §9, two orders of magnitude below the window effect of §6, which is why it changes no conclusion drawn from them. A protocol paper that asks others to declare their matching rule has to declare where its own leaks.

### 4.6 Why a Brazilian instantiation is a stress test

Portuguese-language measurement exercises the instrument against three conditions that English-first tooling does not anticipate: brand names colliding with ordinary words, diacritics rendered inconsistently across languages, and market leaders postdating the pre-training cut-off of deployed models. None is peculiar to Brazil. Lexical collision between a brand and a common word occurs in any language, as Orange, Free, Next, Three, Ideal, Post, Meta and Target attest, and §4.5 shows the failure occurring inside this instrument rather than in a hypothetical one. The linguistic case is no longer only an argument from first principles: cross-language responses about the same brands diverge in similarity and in sentiment across twelve European languages [26], query language is the largest systematic factor in a crossed variance decomposition [24], and evaluation instruments themselves degrade outside English [95]. Brazilian-Portuguese evaluation is an active research area rather than a convenience choice [96]. An instrument validated where all three conditions hold at once has been tested under harder conditions than one calibrated on English alone, and the battery is half English precisely so that a Brazilian result can be checked against a non-Brazilian baseline inside the same instrument.

### 4.7 Collection pipeline, caching and cost

Collection runs twice daily at 06:00 and 18:00 in Brasília time. The unit of observation is one triple of query, engine and run. Responses are cached by SHA-256 content hash, and what keeps a cached answer out of the series is not the time-to-live. The implementation's default is 20 hours, longer than the twelve-hour interval between rounds, so on that parameter alone the evening round could be served the morning's answer. The protection that operates instead is that the cache directory is excluded from version control and every collection, scheduled or manually dispatched, runs on an ephemeral hosted runner whose cache directory is created empty. A run started from a local working copy that keeps its cache between invocations carries no such protection, and no column of `citations` records whether a row was served from cache, so such a run would not be identifiable after the fact. The Type A run-to-run component of Table 6 is the entry that depends on this: a cached second round would return concordance of exactly 1.0, and the measured same-day concordance runs from 0.835 to 0.992, which is the only evidence in the series that the two rounds are two calls.

The response hash is stored per row, which turns a silent provider change into a visible shift in the distribution of hashes. Since migration 0010 the pipeline writes the whole response to `response_full_text` while continuing to write the windowed string to `response_text`, which is what makes the two-window comparison of §6 a within-observation comparison rather than a between-period one.

Cost shapes the design in three places, and each is declared because each biases something. Reasoning tokens on the first Gemini pinned model were about 91% of the study's inference spend, roughly R$2,100 per month, which is the stated motive for the 2026-06-17 change of model and reasoning budget, and therefore the reason that arm has a stratum boundary. The retrieval arm runs 96 of the 192 canonical queries on cost grounds, which halves its per-cell power and removes three of the six semantic categories from its coverage. The same arm bills US$0.0025 per search on the agent route against US$0.005 per request on the legacy route, a difference that matters because the legacy transport is scheduled for retirement on 2026-09-27, inside the projected collection window. Coverage over the span is 53 days with data against 139 calendar days under the table-build date rule of §8.2, with 19 of those 53 partial, 328 collection runs recorded as successful and 344 as aborted; §8 carries the ledger and §14 carries the consequence, which is that the missingness mechanism correlates with the quantity being measured.

---

## 12. Adopting the protocol

An adopter needs three things the specification does not supply on its own: a form to fill in, a list of the decisions that cannot be deferred, and a warning about the failures that will not announce themselves. This section supplies all three from the record of this study. Reproduction failures in audits of commercial systems are documented rather than hypothetical [5], and the conditions that failed there are the conditions BRGEO-1 pins.

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
Uncertainty budget      Table 6.
Evidence                Stored responses: response_full_text from
                        2026-08-31 forward only. Extraction code and
                        table-regeneration scripts: public repository.
Level 2 not claimed     Responses before 2026-08-31 were never retained,
                        so 66,399 canonical observations cannot be
                        re-extracted by a third party.
```

The Level 2 line is the one a claimant would omit, and it is the line that tells a reader that 66,399 of the 68,624 observations behind every rate in §9 cannot be re-extracted by anyone.

### 12.2 Ten decisions an adopter must make

**Table 10.** The ten decisions, the recommendation, and the evidence that produces it. Series and denominators are named per row; where a row cites the three-day full-text cohort it covers 2026-09-06 to 2026-09-08, and where it cites the long series it covers 2026-04-23 to 2026-09-08.

| | Decision | Recommendation | Evidence |
|---|---|---|---|
| 1 | Window value | Set it from a recall target, not from a round number, and publish both | 200 characters recovers 35.4% of first mentions across the panel and between 7.8% and 70.2% by arm, over 1,367 observations cited on the whole response |
| 2 | Window uniformity | One value for every arm, applied at collection and re-checked at analysis | An asymmetric window moved one published rate from 74.9% to 52.0% over 7,435 truncated rows of 7,741 |
| 3 | Retention | Store the whole response from the first observation | 66,399 canonical observations collected before retention began cannot be re-extracted, and one retired arm's window effect is now unmeasurable |
| 4 | Cohort surfaces | Use canonical long names, and run the collision test before collection | Two colliding surfaces added 0.51 pp to the panel rate over 68,624 observations and changed the concentration index from 0.1917 to 0.2023 |
| 5 | Calibration decoys | Include them, and cover every arm with the probes | Spontaneous decoy naming was 0 over 68,624 canonical observations, Wilson upper bound 0.0056%; the probe stratum excluded one arm entirely, which removed the most informative case |
| 6 | Battery balance | Generate the battery from declared axes rather than curating it | Directive against exploratory is 25.9% against 10.0% at panel level over 34,319 and 34,305 observations, and it holds in every arm |
| 7 | Engine identification | Record the version string per row and date every boundary | One boundary changed model identifier and reasoning budget in the same commit, making the arm's two periods non-comparable [90] |
| 8 | Generation configuration | Publish it, reasoning effort included, and treat a change as a stratum boundary | One change to reasoning effort alone cost five consecutive collections and 129 of 179 minutes of one run's wall-clock time |
| 9 | Matching rule | Publish the rule and its ablation, never the rule alone | Aliases moved the panel by 0.94 pp and one arm by 5.25 pp; exclusion contexts moved nothing, on 2,225 observations |
| 10 | Missingness | Record every gap; impute nothing; publish the ratio | 53 days with data against 139 calendar days, 19 partial, 344 aborted runs; gaps cluster on credit exhaustion, which correlates with the measured quantity |

Two decisions sit outside the table because BRGEO-1 does not take them. Repetition count is the province of a complementary protocol that fixes iteration tiers and reports reliability as a generalizability coefficient, G = 0.58 at five iterations and G = 0.74 at ten [28]; an adopter who declares both protocols is better specified than one who declares either, and BRGEO-1 recommends the pairing without requiring it `[BRGEO1-O-002]`. Sufficiency of the collected sample has its own convergence criteria in this market [18], and an adopter should state which one stopped collection. Aggregation is deliberately unconstrained: §10 reports that two defensible aggregations of the same components rank entities at rho 0.752 over 66 entities, so the specification constrains the conditions of observation, where disagreement is large and resolvable, and leaves the formula to the reporter who must then publish the components alongside it [11, 55, 53].

### 12.3 Errors an adopter will meet

Every failure below produced a green pipeline in this study, which is the property they share and the reason a functional test suite will not find them.

**The window is set in the adapter, not in the design.** Five of six client adapters wrote `text[:200]` and the sixth did not. §5.3 gives the detection history; the transferable part is the check that found it, a variable whose maximum equals its minimum across 15,168 observations is reporting a boundary rather than measuring a length. Run that check on day one.

**A protection can be written, called, and swallowed.** The migration that added full-response retention was invoked from inside a function that ran before the table it altered existed. It failed on "no such table", an `except` turned the failure into a debug log, and on an existing database the column appeared anyway. A new database would have been born without it and nobody would have known. Every exception handler that degrades to a low-level log inside an initialisation path needs a test that exercises the path from zero.

**An undeclared constant in the reference implementation is an undeclared parameter.** The index script in this project carried a minimum observation count of 500 for panel eligibility, set in code and named nowhere in the specification. In the fintech panel it excluded a live arm holding 96 observations and retained an arm retired weeks earlier holding 3,552. The reference implementation of a measurement standard is part of the standard, and an eligibility rule that lives only in code reproduces, inside the artefact meant to demonstrate the specification, the failure the specification exists to prevent.

**The dashboard and the paper will disagree.** The field log of this project records a divergence between the per-arm rates published on the public dashboard and the per-arm rates in the manuscript, traced by code inspection to a different extractor version and a denominator that includes the adversarial probe stratum; the log marks the divergence as not yet reconciled in any repository document and as requiring independent verification before it is asserted as a finding. The adopter lesson does not wait on that verification. Decide once which extractor and which denominator a published number uses, and make every surface read from the same computation, because the alternative is the defect this protocol describes in the market occurring between two artefacts of the same project.

**The provider will move without asking.** Presets on one interface routed to a third-party model under a name that did not change, which would have swapped an arm silently; the study now names the model explicitly on every call. The same provider scheduled retirement of the transport in use for a date inside the collection window. Pin the model by string, probe what the string actually returns, and read the provider's deprecation notices as instrument risk rather than as engineering news.

**Credit exhaustion is a measurement problem.** Seventeen days of series were lost between 2026-08-16 and 2026-09-08, with 49 runs of which three succeeded, 28 barred at preflight on balance or model, 17 cancelled on timeout or concurrency and two failed in collection, a run counting on more than one line when two providers failed together. A preflight that bars a partial day protects the series from a day that looks complete and is not, and it costs statistical power; a policy that admits partial days costs the opposite. Both are defensible, and the requirement is that the choice, the date it changed, and its effect on the ledger are published rather than inferred.

---


## 5. Building and breaking the instrument: a field record

Every defect described below passed a green test suite, and each one that moved a published number was found by inspecting a distribution rather than by running a check. The instrument specified in §3 and instantiated in §4 is the second the project built. The first was abandoned in April 2026, after a null report established that two of its three hypotheses could not have produced a positive result whatever the engines did.

The record is drawn from the repository's own artefacts, each cited in place: the changelog, dated incident and health-check notes, and commit messages.

### 5.1 What the first instrument could not conclude

Three dominant market claims survived testing at N = 7,052 observations over 12 days, and only one of the three survived for a statistical reason. The null report, deposited on Zenodo on 2026-04-22 (10.5281/zenodo.19712217) and submitted to SSRN the same day, separates the mechanisms.

The retrieval-advantage hypothesis was underpowered: about 1,000 observations in the retrieval-augmented arm against the roughly 4,200 the corrective design specifies, so the null reports the sample rather than the engines. The hallucination hypothesis was null by construction, because the adversarial probe was switched off and the corrective action recorded against it is the activation of the flag that generates fictitious entities. A hypothesis about whether models name entities that do not exist was tested on a battery that never asked about one. The disjoint-universes hypothesis was defeated by asymmetric instrumentation: citation universes were compared through `sources_json`, a field each provider populates by its own convention, and the corrective action is to read the named entities from the response body and ignore the field.

The second and third failures share a property that matters more than their subject: neither is visible in the output of the analysis. A null on fictitious-entity citation has the same shape whether the models abstain reliably or the probe never executed, and a cross-provider comparison of a provider-defined field returns a number whether or not the field denotes the same thing in each arm. Measurement modelling names this gap between the construct and the thing the code operationalises [10], and benchmark critique has shown how completely an aggregate hides the item selection that produced it [46]. The project published that diagnosis about itself in April and met the same species of defect again in August.

### 5.2 The reboot of 23 April 2026 and what it fixed

The reboot replaced the matching rule, the cohort, the battery and the analysis stack in a single release, and it deleted every observation the old instrument had produced. A five-agent audit listed more than 95 gaps; the P0 and P1 items were implemented as v2.0.0 on 2026-04-23 (`CHANGELOG.md:285-340`).

Four changes carry the weight. Entity matching moved to NFC and NFKD dual-pass normalisation, markup stripping, strict word boundaries, an alias table and stop contexts, closing seven of the defects the null report had named, among them diacritic insensitivity and substring matching. The cohort was rebuilt at 127 entities and the battery at 192 queries balanced 50/50 on language and on query type. The inference stack gained cluster-robust standard errors, a mixed-effects logit, and a Monte Carlo null in place of an arbitrary Jaccard threshold of 0.30. The adversarial stratum became part of the design rather than an option.

The matching change was measured before it was adopted. Re-extracting 2,000 historical rows under the new rule moved the positive count from 1,409 to 776, a fall of 633, because 45% of the old positives were substring matches (`CHANGELOG.md:342-347`). A factor of roughly 1.8 on the headline rate separates two rules that both answer to the description "the engine cited the entity", which is the observation that later becomes parameter P6. At 16:40 the same day the old series was truncated, 18,537 rows deleted and the pre-reboot state tagged and backed up; the first v2 collection was dispatched at 20:21 against an empty `citations` table. No analysis in this paper crosses that line.

### 5.3 Seven defects that passed every control

**Table 11.** Eight defects that reached production behind passing checks, grouped into the seven episodes §5.3 narrates, with the route that actually exposed each. Series 2026-03-25 to 2026-09-09; sources are repository artefacts, not references.

| Dates | Defect | What exposed it | Cost to the series |
|---|---|---|---|
| 2026-03-25 to 03-29 | Import error masked by `\|\| true`; four days of successful runs with no rows | A weekly benchmark failure, after three days in which the FinOps monitor failed correctly and went unread | 4 days, about 768 observations, unrecoverable |
| 2026-03-30 to 04-07 | Externally rotated keys; HTTP 401 on all four providers under `continue-on-error` | Manual inspection of the published dashboard, nine days in | 9 days; dashboard aggregates overwritten daily with zeros |
| 2026-04-29 | Adversarial probes never executed (`is_probe = 0` on all 8,571 rows); `query_type` at 7,299 directive against 1,272 exploratory | A deep health check that counted rows by design cell | Days 1 to 7 redeclared as warm-up without probes; 4,284 rows re-annotated |
| 2026-08-24 to 08-31 | Default reasoning in the fifth arm consumed 129 of 179 wall-clock minutes | Reading the job logs after five consecutive cancellations | 8 days; about 900 Actions minutes; no day persisted |
| 2026-08-31 | Observation window asymmetric: five adapters stored `text[:200]`, one stored up to 2,502 characters | A distributional check prompted by a review question about a column reading 0.0% | Perplexity falls 23.8 pp on re-extraction over 66,399 observations |
| 2026-08-31 | The full response was never retained, so no observation was reproducible by a third party | The same review, on the same column | Every observation from 2026-04-23 to 2026-08-30 is unauditable at any other window |
| 2026-08-16 to 09-08 | Credit exhaustion at three providers barring whole days at preflight | Run accounting: 49 runs, of which 3 succeeded | 17 days of series |
| 2026-09-09 | The public panel ranked 8 fictitious calibration decoys among 30 entities | Recorded in the commit that changed the preflight policy | No internal table affected; the published ranking was wrong for an undetermined period |

**Two episodes of green continuous integration with zero data.** An f-string valid on Python 3.12 and invalid on the 3.11 that CI ran killed every collection command at import, and the workflow reported success because the collection step ended in `|| true`. Five days after the fix, a key rotation performed outside the repository returned HTTP 401 on all four providers, and `continue-on-error` again produced exit 0 for nine days. The control installed after the first episode validated imports, which is why it did not see the second: it had learned one shape of silence and met another. The fix that generalised was a fail-loud exit when zero citations are collected across all verticals, an aggregate that cannot legitimately be zero. The incident report states the transferable rule: the success criterion of a collection pipeline has to be a property of the data, such as a new row in `collection_runs` (`docs/INCIDENT_PIPELINE_2026-03-29.md:119-120`).

**The audit that found the design was not the design being executed.** The adversarial query builder returned an empty list, a placeholder nobody had replaced, so all 8,571 rows carried `is_probe = 0`. The factorial balance ran at 85/15 rather than 50/50, because the configuration read the key `type` while the v2 battery writes `query_type`, and the fallback map resolved five of six categories to `directive` (`docs/audits/2026-04-29/HEALTH-CHECK-DEEP.md:15-59`). Neither defect stopped collection, and the 204-test suite asserted behaviour rather than distribution. Re-annotating 4,284 rows restored 4,287 directive against 4,284 exploratory, and a regression test was written against the empty probe list. Both lessons transfer to anyone building a battery: a placeholder returning an empty list is indistinguishable downstream from a design with no probes, and a factorial design is balanced only if the balancing key is the key the code reads.

**The arm that consumed 72% of the run.** The fifth arm's replacement model reasons by default and bills the reasoning as output. In one run it took 129 of 179 wall-clock minutes against 17 for Gemini, 15 for Claude, 12 for ChatGPT and 5 for Perplexity, and the job hit the 180-minute ceiling with the fourth vertical half-collected. Nothing surfaced above job-log level, because the run panel alternated between cancelled and failed without saying where collection stopped. The fix was measured against the API with the collection's own query: 73.7 s and 2,746 reasoning tokens at the default, 19.7 s and 419 tokens at the lowest permitted effort, model identifier untouched (`governance/HEALTH-CHECK-COLETA-20260831.md:27-47`). A provider default for reasoning changes latency and cost by a factor of three or four while leaving the model version unchanged, so a panel's affordability turns on a parameter no model identifier records. Two of the four registered series events came from generation configuration, which is why it became parameter P5.

**The asymmetric window, found by a distributional check.** Entity extraction ran over a column that was never the model's answer: five of six client adapters stored the first 200 characters, and the sixth, taking a different path inside its client, stored the whole response up to 2,502 characters. The asymmetry fell on the axis the study compares, retrieval-augmented against parametric. Every control looked in the right place for the wrong question. Tests asserted on the column, and the column was populated in both cases; validators checked that the string was well formed, and both were; the daily health check confirmed six arms producing rows, probes marked and response hashes varying, all true, and none of it asking how much text the extractor was reading (`governance/ASSINATURA-DISTRIBUCIONAL-20260831.md:58-66`). The distribution answered in one query: a mean stored length of exactly 200.0 in five arms against 691.8 in the sixth, whose lengths run continuously from a first percentile of 289 to a maximum of 2,502. The magnitude appears in §6. On the day the asymmetry was found, 223 tests passed.

**The response that was never retained.** Text beyond the window was discarded inside the client and never reached the database, so for the whole series to 2026-08-30 the input to the extraction does not exist and no third party can reproduce a single observation. The repository reports the affected count twice in the same week, as 80,638 in two documents and 83,486 in two others, and reconciles them nowhere; §4 declares which snapshot the manuscript uses. Retention was added forward-only by migration on 2026-08-31, with a backfill that annotates each historical row's effective window from the stored length and makes no attempt to reconstruct what was discarded. The asymmetry was correctable, because a truncated string is still the string the extractor read; discarded text is not. Regeneration is no substitute, since hosted models are not deterministic at temperature zero [91] and silent updates, numerical rounding and expert routing keep exact reproduction out of reach through a commercial API [92]. Retention of the raw observation is a requirement separate from correctness of the measurement, and the only one that cannot be repaired retroactively [53].

**Credit exhaustion barring whole days.** Between 2026-08-16 and 2026-09-08 the pipeline attempted 49 runs and completed 3: 28 were barred at preflight by balance or by a retired model, 17 cancelled on timeout or concurrency and 2 failed during collection, with a run counting on more than one line when two providers failed together (`governance/HEALTH-CHECK-APIS-20260908.md:21-44`). The control behaved exactly as designed. A preflight that spends about US$0.0001 on one token per provider and aborts on any 4xx was installed in April so that a provider without balance would produce a declared gap instead of a silently partial day. The structural cause was documented in September: the six API keys in the study's environment are the same keys two other systems use, so three measurements presented as independent stopped at the same time for the same reason, and the 49 runs of which 3 succeeded are that stoppage in the ledger. An adopter who shares credentials across instruments buys correlated outages and loses cost attribution, exactly where independence is being claimed.

**Fictitious entities in the public brand ranking.** The published panel listed 8 calibration decoys among the 30 entries of its entity ranking, so a reader who copied the top ten would have named at least one company that does not exist. The same commit corrected a coverage figure reading 118.8% and a published window end of 2026-07-21 when the last collection had run on 2026-09-09 (commit `427ab00`). The internal tables were unaffected: across 68,624 canonical observations no decoy is named spontaneously in any arm, at either window (Table 21). The defect lived in the aggregation layer of the published artefact, where the filter separating the adversarial stratum from the canonical one was applied to some blocks and not to the ranking. An instrument that leaks into a public number stops being a control, so the stratum filter needs a test at every aggregation rather than at the one where it was first written.

### 5.4 What the defects have in common

The seven share a detection profile, and it is the reason a passing suite is not evidence of correct measurement. In every case the tests asserted something about a field, and the field was populated. The column held a well-formed string of plausible length; `is_probe` held a valid zero; `query_type` held a legal value; `sources_json` held a parseable object. The project's own health check puts it precisely: the defect lived one level below every claim the pipeline made about itself, and no assertion was false, the set of them simply did not cover the question "is this string the model's answer?" (`governance/HEALTH-CHECK-COLETA-20260831.md:77`).

What did detect them was distributional, and cheap. A mean equal to a maximum across tens of thousands of rows reports a boundary rather than a measurement (`:79`). A zero on a binary column across 8,571 of 8,571 rows describes a feature that does not exist. A 7,299 against 1,272 split on a factor designed at 50/50 is one count. None of these is expressible as a functional assertion, because a functional test asks whether the pipeline does what was written and never whether what was written measures the intended quantity (`governance/ASSINATURA-DISTRIBUCIONAL-20260831.md:52-55`). The same asymmetry allows reported progress on a benchmark to be an artefact of the evaluation harness rather than of the systems evaluated [50], and it is why construct validity has to be argued rather than inherited from a passing suite [49].

Two corollaries follow and both are operational. A degradation path that does not announce itself is indistinguishable from one that does not exist, which a restore step gated on four secrets that were never created demonstrated over two months of weekly analyses run on 1.4% of the dataset. The inverse holds with equal force: a guard that always fails is indistinguishable from a guard that is switched off, which a time-relative condition tested against time-fixed fixtures produced across six days of red pipelines with nothing wrong in the instrument. BRGEO-1 therefore asks for distributional attestation alongside the functional kind, and structured reporting of evaluation metadata is the existing vehicle for carrying it [59].

## 8. Instrument drift and honest missingness

A pooled figure over this series averages across a panel that changed composition or configuration at four declared boundaries, and across 86 calendar days holding no observation. The event register as it stood at the first analysis carried four of the seventeen boundaries the record supports.

### 8.1 Seventeen boundaries, of which four were declared

An instrument that changes mid-series and publishes one number publishes an average over several instruments. The requirement in §3 is that every change be dated, recorded and carried into analysis as a stratification boundary, which presumes the register is complete. The four registered events were the ones that forced an analytic decision at the time; thirteen further boundaries were documented elsewhere in the repository, declared in prose without reaching the table, or never classed as events at all.

**Table 12.** Series events and candidates, 2026-04-23 to 2026-09-27. Status distinguishes the four events in the register as first published from boundaries documented elsewhere and from candidates never declared. The final row is scheduled and has not occurred.

| Date | Arm | Change | Class | Analytic consequence | Status |
|---|---|---|---|---|---|
| 2026-04-23 | all | v1 dataset truncated, 18,537 rows deleted; NER v2 replaces v1 matching | dataset reset, matching rule | Hard discontinuity; v1 positives ran 1.8× v2 on 2,000 rows | Documented, not in the event table |
| 2026-04-30 | all | adversarial probes activated | battery | Days 1 to 7 are a warm-up without probes; the calibrated sub-window starts here | Documented, not in the event table |
| 2026-04-30 | all | `query_type` re-annotated on 4,284 rows, 85/15 to 50.02/49.98 | battery annotation | Any query-type result on the earlier window used a mislabelled factor | Candidate, not declared |
| 2026-06-05 | Gemini | thinking budget set to 1024; arm made optional in the mandatory list | generation configuration | Second of two adjacent configuration events in the same arm | Candidate, not declared |
| 2026-06-17 | Gemini | `gemini-2.5-pro` to `gemini-2.5-flash`; thinking budget 1024 to 0 | model version and generation configuration | Pre and post not comparable; the two effects are not separable | **Declared** |
| 2026-08-17 to 08-19 | slot 5 | Groq retires `llama-3.3-70b-versatile`; five collections abort at preflight | provider-imposed outage | Gap in the fifth arm; last Groq observation 2026-08-16 | Documented, not in the event table |
| 2026-08-19 | slot 5 | engine replaced, Groq to xAI `grok-4.6` | engine replacement | Not a continuous series; stratify or truncate | **Declared** |
| 2026-08-19 | all | TLS delegated to the OS certificate store | transport | Declared to have no effect on collected data | Documented as a non-event |
| 2026-08-31 | Perplexity | observation window unified at 200 characters | window | 75.7% to 51.9%, −23.8 pp over 66,399 canonical observations | **Declared** |
| 2026-08-31 | all | full response retained (migration 0010) | retention | Forward-only; no window sensitivity before this date | Declared in prose, not in the event table |
| 2026-08-31 | Perplexity | arm added to the probe stratum | battery coverage | Earlier decoy figures describe five parametric arms only | Candidate, not declared |
| 2026-08-31 | Grok | reasoning effort reduced to the lowest permitted level | generation configuration | Separate stratum; 206 observations of 2026-08-23 discarded in that arm | **Declared** |
| 2026-08-31 | all | panel membership redefined from observation count to recent activity | index computation | The fintech panel loses Groq and gains Grok; breadth is a third of the index | Candidate, not declared |
| 2026-08-31 | all | hallucination marker separated from refusal marker | outcome definition | The probe outcome changes meaning; on the snapshot of that day 11,195 of 16,579 flagged rows, 67.5%, carry an explicit refusal | Candidate, not declared |
| 2026-09-06 to 09-07 | ChatGPT, Claude | arms absent; mandatory list downgraded as a repository variable | panel composition | Two days with three of five arms | Documented, not in the event table |
| 2026-09-09 | all | preflight default changes from abort to degrade | missingness policy | Later days may hold unequal panels by design | Documented, not in the event table |
| 2026-09-27 | Perplexity | legacy chat transport retired; Agent API behind a flag | transport | Same model, window and retention; auditable per row | Scheduled, prepared, not switched |

Two of these are boundaries an adopter cannot avoid. Providers change the behaviour behind a stable product name [90], which is the rationale for pinning a snapshot in P4, and a provider retiring a model or a transport sets a boundary on a schedule the study does not control. Variance decomposition that treats model version as a component alongside sampling and prompt phrasing [28] is the natural companion to a register of this kind.

### 8.2 What the calendar actually covers

The series spans 139 calendar days and holds data on 52 of them, a coverage of 37.4%. Two day rules are in use and they differ by one. The temporal analysis counts 52, assigning each row to the local Brazilian date because evening runs cross midnight in UTC; the table build counts 53, assigning each row to its UTC date. Every figure in this paper that depends on a day count states which of the two it uses, and a figure that names neither is the table-build count of 53.

One hole dominates. Between 2026-06-10 and 2026-08-07 the database holds no observation on any day, 59 days recorded in `collection_runs` as 236 aborted runs with zero records. July is empty in full, 0 days with data out of 31, and the next four holes run 7, 6, 5 and 5 days. Across the span `collection_runs` carries 344 aborted rows against 328 successful ones, covering 86 distinct days, written retroactively by a script so that a silent hole would enter the record as a declared fact. Any line fitted across the series interpolates over two months in which nothing was observed, which is why §9 reports daily behaviour as description and tests nothing on it. The nearest methodological peer in the literature declares a 40-day window and reports 55,393 queries inside it [34]; read as a four-and-a-half-month daily panel, this series would have its temporal density overstated by a factor of 2.7.

<img src="figures/fig3-coverage.svg" alt="Figure 1">

**Figure 1.** Collected days by arm across the calendar span of the series, 2026-04-23 to 2026-09-08. Each mark is one arm on one day; lighter marks are days recorded as partial in the missingness ledger. The shaded band is the 59-day interruption from 2026-06-10 to 2026-08-07, in which no arm produced an observation. Drawn from `stats/data/s2_daily_engine.csv` and `stats/data/s2_calendar_gaps.csv`.


The ledger itself has a hole, and it is the more uncomfortable of the two. The itemised table of gaps and causes runs to 2026-05-18 and resumes at 2026-07-25, leaving no day-level cause for 2026-05-19 to 2026-07-24, and the entry for 2026-07-25 records an isolated one-day balance gap, which presumes a July in which collection otherwise ran. The canonical database holds no July observation at all. A protocol that requires a missingness ledger from its adopters has, for two months of its own reference series, a ledger recording attempted runs as though they were collected days. The entries are corrected in Appendix D and the aggregate counts stand, since they come from `collection_runs` rather than from the ledger. Datasheets were proposed against this shape of failure [66]: the record of how a dataset came to be is written by the process that produced it and degrades in the same places.

Partial days are counted twice for the same reason, and the two rules do not agree on the count. The repository's registry begins on 2026-09-06 and holds two entries inside the span. The rule of the table build, marking a day partial when an active engine delivers fewer distinct canonical queries than its own battery or produces nothing, finds 19 partial days among the 53 with data. The rule of the temporal analysis, which marks a day partial when the documentation declares it so, or when it holds fewer than 20 of the 20 engine-by-vertical cells, or when its volume falls below half the daily median, finds 8. Both agree exactly with the registry on the two days it covers, which licenses either for the four months the registry does not reach. Under the second rule, two empirically incomplete days, 2026-06-05 and 2026-08-13, appear in no ledger, and three the documentation calls partial are complete in cell terms, because the failures they describe consumed rows rather than cells.

### 8.3 Two regimes for a partial day, and the date that separates them

Until 2026-09-09 the acquisition rule was that an absent day beats a partial day, on the stated ground that a gap enters the missingness ledger while a partial day enters the series looking like a complete observation. The preflight enforced it by barring collection whenever a mandatory provider had no balance, which is how the 8-day and 17-day gaps of §5.3 arose. From 2026-09-09 the default reverses: a provider without credit is dropped from the mandatory list for that run, the day is written to the registry with the missing arms, the provider's verbatim error and the run URL, and collection proceeds if a minimum number of arms remain (commit `427ab00`). Within two days the new path recorded three further partial days, on 2026-09-10 and 2026-09-11, from credit exhaustion at three different providers.

Both rules are defensible and they trade the same quantity in opposite directions. The strict rule protects the comparability of every day that enters the series and pays in statistical power; the degrading rule preserves days and pays in unequal panels, moving the problem from the day dimension to the arm dimension. Every day up to 2026-09-08 belongs to the first regime and is complete or absent; every day from 2026-09-09 belongs to the second and may be partial by design. The analysed snapshot ends on 2026-09-08 and lies entirely in the first regime.

One further declaration belongs here, because a reader would otherwise infer it wrongly. The confirmatory window is 90 **collected** days rather than 90 calendar days. The calendar ninetieth day passed on 2026-07-21; on 2026-09-11 the count stood at 56 of 90, with a projected close of 2026-10-15. Defining the window in collected days turns an outage into a schedule extension instead of missing data, so the published close date moves whenever a provider stops answering.

### 8.4 What a change-point detector can and cannot reach

Confronting the declared events with ruptures detected blind states what the calendar costs. Of 21 declared event-by-arm pairs, one coincides with a detected rupture, five produced no rupture where the instrument was sensitive enough to have seen one, and fifteen are not testable because a hole sits on the boundary.

The one that coincides is not among the four registered events. On 2026-06-05, when the Gemini thinking budget was capped and the arm was made optional, the detector places a boundary at zero distance, with the arm moving from 1.29% to 2.80%, a rise of 1.50 points at a permutation p of 0.001. The mechanism is the one proposed and never confirmed in the April investigation of that arm: capping the reasoning budget leaves output tokens for text, and text is what the extractor reads. It rests on four post-boundary days, since the 59-day hole opens on 2026-06-10, and it belongs in the event table as a candidate with a hypothesis attached. The five non-ruptures are a positive control: the battery changes of 2026-04-30 move nothing in any of the five arms then active, at a minimum detectable difference running from 1.2 points in Gemini to 6.5 points in Perplexity, and both changes sit outside the canonical outcome by construction.

The fifteen untestable pairs fail for one reason, and the reason is not accidental. The declared model change of 2026-06-17 sits inside the 59-day hole; the arm swap and the transport change sit against a 7-day hole, the three events of 2026-08-31 against an 8-day hole, and the September panel reduction against another. Collection stopped at almost exactly the moments the instrument was being changed, because the changes and the outages have common causes: the late-August hole exists because the new fifth arm consumed 72% of the run, and the fix for that consumption is the 2026-08-31 configuration event; the September holes come from the credit exhaustion that also forced the panel reduction. No design that waits for its own events to happen can measure them. An adopter declares the boundary in advance, stratifies on it by rule rather than by detection, and retains the full response so that the arms on either side are re-extractable under one aperture.

Four ruptures were detected that nobody declared, and each is larger than the one declared event the detector reproduces.

**Table 13.** Ruptures detected blind that no repository artefact dates. Binomial binary segmentation on the daily rate, permutation p; magnitudes are the change in the arm's daily citation rate across the boundary. Source `stats/data/s2_changepoints.csv`.

| Last day before | First day after | Arm | Δ pp | Permutation p | How far the boundary is localised | Artefact dating it |
|---|---|---|---:|---:|---|---|
| 2026-05-24 | 2026-05-25 | Perplexity | −7.87 | 0.001 | one day | none |
| 2026-05-27 | 2026-05-28 | Perplexity | +5.77 | 0.008 | one day | none |
| 2026-08-08 | 2026-08-10 | Perplexity | +5.24 | 0.001 | two days, on the resumption after the long hole | none |
| 2026-06-09 | 2026-08-08 | Groq | +1.69 | 0.001 | anywhere inside the hole | none |

Either the retrieval-augmented arm moves on its own at a scale the parametric arms never show, or something changed in it that the project did not record. Both readings cost the same thing: a pooled rate for that arm over the whole series, reported without the confrontation, would be an average across regimes nobody can date.


## 6. The observation window

### 6.1 One parameter, two measurands

Entity extraction runs over a string, and that string is whatever the pipeline retained rather than the model's answer. Its length is parameter P1, the observation window, and on the 2,225 responses this study stored whole it moves the citation rate by between 22.95 and 55.73 percentage points depending on the engine, with no other parameter touched.

Both values of the parameter answer a real question. A narrow window measures *head-of-response citation*, whether the entity appears in the opening a reader sees before deciding whether to keep reading, which is the quantity a click-through argument needs. A wide window measures *whole-response citation*, whether the entity appears anywhere in the text the engine produced, which is the quantity an attribution argument needs. Either is defensible. Leaving the choice unstated is what breaks comparison, because two figures produced under two windows are estimates of two different quantities and their difference carries no information about the engines.

Metrology has a name for this. A citation rate reported without its window skips the requirement of VIM 2.3 Note 1, and VIM 2.27 names the resulting component, definitional uncertainty [7]; §1.2 states the two notes to that clause and what they cost an interval derived from sample size alone. The window movement in Table 15 is an instance of Note 2 and it sits at the floor Note 1 describes. Calling it measurement error concedes the wrong thing, since error implies a correct value that better technique approaches, and no sample size, no better extractor and no additional collection day closes a gap between two questions. The uncertainty budget of §3 lists P1 as a Type B component [8]; this section supplies its measured value.

### 6.2 How the asymmetry arose, and why nothing detected it

In five of six client adapters the stored extraction string was cut at 200 characters by the line `response_text = text[:200]`. The sixth stored up to 2,502 characters. The cut was a property of the client rather than of the measurement design, written for log volume rather than for a reading of the construct, and it was therefore invisible to every check that operated on the stored field.

§5.3 gives the detection history: no functional control saw the asymmetry, and a distributional check found it.

**Table 14.** Length in characters of `citations.response_text`, the string entity extraction actually read. Series 2026-04-23 to 2026-09-08, 68,624 canonical observations, denominator is canonical rows with a non-null `response_text`, by engine.

| Engine | n | Mean chars | Min | Max | Share exactly 200 |
|---|---:|---:|---:|---:|---:|
| Gemini | 15,355 | 195.7 | 87 | 200 | 92.6% |
| ChatGPT | 15,168 | 200.0 | 200 | 200 | 100.0% |
| Claude | 15,034 | 200.0 | 200 | 200 | 100.0% |
| Groq | 14,208 | 200.0 | 200 | 200 | 100.0% |
| Perplexity | 7,741 | 668.0 | 198 | 2,502 | 3.9% |
| Grok | 1,118 | 200.0 | 179 | 200 | 99.9% |

A variable whose maximum equals its minimum across 15,168 observations is reporting a boundary rather than measuring a length. Gemini and Grok fall marginally short of the ceiling, which is what an arm that occasionally answers in fewer characters than the cap looks like once the cap is imposed. The 305 Perplexity rows now sitting at exactly 200 were collected after the uniform window was applied at collection time on 2026-08-31, which is why that arm's mean sits at 668.0 against the 687.2 of the series that closed on 2026-08-31.

P1 is a conformance requirement because of where its value gets set. Position effects in generated output are already measured: models are sensitive to the order of candidates they are given [83, 84], position bias in generated recommendation and reranking is a venue-accepted phenomenon [86, 88], and the effect is model-specific in ways that track neither provider nor capability [85, 89]. What this study adds is about the instrument, and it is the conversion P1 describes (§3.1): the cut-off that performs it differs between providers, which places the variation exactly where cross-engine comparison lives.

### 6.3 One arm moves 22.8 points on re-extraction

Re-extraction over the full series under a uniform 200-character window moves one arm. Perplexity falls from 74.9% [73.9, 75.8] as collected to 52.0% [50.9, 53.1] under the uniform window, a difference of 22.8 percentage points over the 7,435 rows whose stored text exceeded the window, and the panel falls from 20.5% to 18.0% on 68,624 canonical observations. On the series that closed on 2026-08-31, the same contrast runs 75.7% against 51.9% over 66,399 observations, a difference of 23.8 points; the gap between that figure and the one above is the 305 rows collected under the uniform window after 2026-08-31, which the earlier snapshot did not contain.

Under the same re-extraction the other five arms show deltas of exactly zero, and those zeros are identity by construction and not independent verification. Applying a 200-character window to a string that is already 200 characters long is the identity operation, so the zero is guaranteed before any data is read. What those rows do confirm is narrower and still worth having: re-extraction is deterministic and the cohort did not change between runs. Reading them as evidence that the window does not matter on the parametric arms is the misreading the comparison invites, and §6.4 shows what it would have cost.

### 6.4 Every arm gains and no arm loses

Inside the arm, on identical observations, reading the whole response instead of the first 200 characters moves the rate by 22.95 to 55.73 points and loses no citation. Since migration 0010 the pipeline writes the whole response to `citations.response_full_text` while continuing to write the windowed string to `response_text`, which is what makes the comparison a within-observation one: extract over `response_full_text[:200]`, extract over `response_full_text`, hold the cohort, the battery and the matching rule fixed, and read the difference. Two identity checks run first and both pass on all 2,225 rows: `response_text` equals `response_full_text[:200]`, so the two columns are two views of one response, and re-extraction of the first 200 characters reproduces the stored `cited_v2` exactly, so the rule used here is the rule that produced the series.

**Table 15.** Citation rate at 200 characters against citation rate on the whole response, same observations, same matching rule. Series 2026-09-06 to 2026-09-08, 2,225 canonical observations, denominator is the engine's own observations retaining a full response. Intervals are 10,000-replicate bootstrap percentiles with query clusters resampled; McNemar is the exact two-sided binomial on the discordant pairs.

| Engine | n | Rate at 200 [95% CI] | Rate on full [95% CI] | Δ pp | Bootstrap 95% CI | Gains | Losses | Exact McNemar p | Design effect |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Perplexity | 305 | 54.10 [48.49, 59.61] | 77.05 [72.01, 81.41] | +22.95 | [16.8, 29.6] | 70 | 0 | 1.69e-21 | 1.83 |
| Gemini | 768 | 2.60 [1.69, 3.99] | 33.33 [30.09, 36.74] | +30.73 | [27.3, 34.0] | 236 | 0 | 1.81e-71 | 1.05 |
| ChatGPT | 192 | 17.19 [12.51, 23.15] | 53.65 [46.59, 60.56] | +36.46 | [29.7, 43.2] | 70 | 0 | 1.69e-21 | 0.99 |
| Claude | 192 | 25.00 [19.41, 31.57] | 66.15 [59.19, 72.46] | +41.15 | [34.4, 47.9] | 79 | 0 | 3.31e-24 | 0.99 |
| Grok | 768 | 28.39 [25.31, 31.68] | 84.11 [81.36, 86.53] | +55.73 | [50.1, 61.6] | 428 | 0 | 2.89e-129 | 2.71 |

Losses are zero on every arm. Not one observation classified as citing at 200 characters loses that classification when more text is read, which makes the 200-character rate a lower bound on the whole-response rate at the level of the individual observation and not only in aggregate. The smallest effect in the table, Perplexity at +22.95 points, stands against a paired minimum detectable difference of 12.5 points for that arm at alpha 0.05 and power 0.80, and the other four clear their own thresholds by factors of 2.9 to 5.3.

Two consequences follow for the argument the manuscript has been making. The 23.8 points of §6.3 are the smallest of the five effects, so a figure computed on the truncated series understates the parameter's influence on the panel it is drawn from rather than bounding it. The retrieval-augmented arm is the one the narrow window damages least, which closes the architectural account: an explanation that predicted retrieval-augmented composition as the source of late naming predicts the opposite of what the matched comparison shows.

The Gemini row needs stratifying before it is read. On 2026-09-06 the API returned responses that were themselves cut at the origin, 384 observations with a mean stored full length of 143 characters, of which 378 sit at or below 200 characters and the measured delta for that day is exactly 0.0 points. Restricted to the 390 Gemini observations longer than the window, the delta is +60.51 points on a median full length of 3,423 characters; restricted instead to the collection days 2026-09-07 and 2026-09-08, it is +61.5 points on 384 observations. The pooled row of Table 15 describes a mixture of two collection regimes.

The other end of the response is censored as well, and the censoring runs in the direction that makes the whole-response rate a floor.

**Table 16.** Stored responses ending without terminal punctuation, applied to `response_full_text` under the criterion published as `TERMINAL_RE` in `s5_window_validity.py`. Series 2026-09-06 to 2026-09-08, 2,225 canonical observations, denominator is the engine's own observations.

| Engine | n | Ends mid-sentence | Share | 95th percentile length | Max length |
|---|---:|---:|---:|---:|---:|
| ChatGPT | 192 | 0 | 0.0% | 3,688 | 4,088 |
| Claude | 192 | 2 | 1.0% | 1,728 | 3,072 |
| Gemini | 768 | 648 | 84.4% | 4,085 | 19,777 |
| Grok | 768 | 70 | 9.1% | 3,698 | 4,263 |
| Perplexity | 305 | 1 | 0.3% | 848 | 1,032 |

The criterion is crude and calls a response ending in a bare bullet item incomplete, so it is reported as a diagnostic and never used to filter a rate. At 84.4% of 768 observations the Gemini figure is too large to be an artifact of list formatting, and the tails end mid-word. Gemini's whole-response rate of 33.33% is therefore a floor on the quantity and not an estimate of it, its window delta sits at a floor for the same reason, and the recovery quantiles of Table 18 are longer than reported. Grok carries the same bias on 9.1% of its observations. The three remaining arms are effectively uncensored.

### 6.5 The curve, and what it does to a ranking

A two-point contrast cannot tell an adopter where to set the parameter, so the same rows were re-extracted at ten grid windows and on the whole response.

**Table 17.** Citation rate by observation window, recomputed over the identical observation set with the matching rule held fixed. Series 2026-09-06 to 2026-09-08, 2,225 canonical observations, denominator is all canonical observations of that engine retaining a full response. Rates in percentage points; Wilson intervals for every cell are in `stats/data/s5_window_curve_by_engine.csv`.

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

**Table 18.** Window in characters required to recover a given fraction of first mentions, computed as the narrowest window from which an observation is classified as citing and stays so at every wider grid window. Series 2026-09-06 to 2026-09-08, 1,367 canonical observations cited on the whole response, denominator is the engine's own cited-on-full observations.

| Engine | Cited on full | w50 | w80 | w90 | w95 | Median first-mention offset |
|---|---:|---:|---:|---:|---:|---:|
| ChatGPT | 103 | 275 | 500 | 850 | 1,100 | 245 |
| Claude | 127 | 275 | 450 | 700 | 850 | 241 |
| Gemini | 256 | 600 | 1,700 | 2,250 | 2,500 | 550 |
| Grok | 646 | 350 | 800 | 1,300 | 1,800 | 312 |
| Perplexity | 235 | 150 | 275 | 400 | 450 | 114 |
| All | 1,367 | 300 | 750 | 1,400 | 1,900 | 284 |

The canonical 200-character window recovers 35.4% of the first mentions across the panel, and between 7.8% on Gemini and 70.2% on Perplexity by engine. No window below 2,500 characters reaches 95% recovery on every arm. At the 95% target the required count runs from 450 characters on Perplexity to 2,500 on Gemini, a factor of 5.6, and the spread is of the same order at the 80% and 90% targets. An adopter should therefore declare the window as a recall target together with the count that delivered it on the panel measured; a bare character count means a different thing on each arm.

<img src="figures/fig1-window-curve.svg" alt="Figure 2">

**Figure 2.** Citation rate and recovery of first mentions as functions of the observation window. Panel (a) gives the citation rate of each arm when entity extraction runs over the first k characters of the stored response, k from 50 to 1,600 on a logarithmic scale, with the open marker at the right showing the rate on the whole response; the dashed vertical marks the 200-character window declared in the reference instantiation. Panel (b) gives the share of first mentions already recovered at k, with the 95% line marked. Both panels are computed on the same 2,225 canonical observations with a full response retained, collected 2026-09-06 to 2026-09-08 under the uniform matching rule of P6, so each arm is compared against itself rather than against another arm. The lead changes hands three times along the curve, which is the property that makes an undeclared window incomparable. Drawn from `stats/data/s5_window_curve_by_engine.csv` and `stats/data/s5_mention_recovery_curve.csv`.

### 6.6 What is left of the mechanism

The discourse-structure account, that retrieval-augmented engines compose after fetching sources and therefore defer naming, is refuted by Table 15, and the relative-position evidence that supported it does not survive the removal of the truncation either.

**Table 19.** Position of the first cohort mention on the rows that retained the whole response, where the denominator of the relative offset is the real length of the answer and a first mention past character 200 is counted instead of lost. Series 2026-09-06 to 2026-09-08, 1,367 canonical observations naming an entity, denominator is the engine's own naming observations.

| Engine | Rows naming an entity | First mention beyond the window | Median response length | Median absolute offset | Median relative offset |
|---|---:|---:|---:|---:|---:|
| ChatGPT | 103 | 70 | 1,123 | 245 | 0.216 |
| Claude | 127 | 79 | 1,094 | 241 | 0.225 |
| Gemini | 256 | 236 | 3,407 | 550 | 0.191 |
| Grok | 646 | 428 | 1,778 | 312 | 0.223 |
| Perplexity | 235 | 70 | 491 | 114 | 0.227 |

Measured on the whole text, relative position does not separate the engines: Kruskal-Wallis returns H = 7.7 on 4 degrees of freedom, p = 0.104, epsilon-squared 0.0027, and the five medians fall in a band from 0.191 to 0.227. On the same rows the absolute offsets separate them decisively, H = 277.7, p < 0.0001, epsilon-squared 0.2010. The difference in position dissolves when the offset is divided by the length of the response, which means the engine ranking on absolute offset is a joint statement about where an engine starts naming and how long it writes. Any relative-position claim built on the truncated series would have been an artefact of the truncation, because for five of six arms the denominator was the constant 200 whenever the answer reached that length, which inflates the relative offset by an amount that grows with the text discarded.

Hypothesis H6 stated that susceptibility to a narrow window varies across engines and is predicted by preamble share rather than by engine class. It splits.

**Table 20.** Preamble share and window damage by engine, with the two competing predictors. Series 2026-09-06 to 2026-09-08, 2,225 canonical observations, denominator is the engine's own observations; median first-mention offset is computed on observations cited on the whole response.

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

**Uniformity.** One window, applied identically to every engine. The alternative is what this instrument did for four months: a comparison in which one arm was read through a different aperture than the other five, which is neither a repeatability nor a reproducibility condition in the sense of VIM 2.20 and 2.24 [7].

**Declaration.** The value published with the figure, for the reason §6.5 closes on.

**Retention of the whole response.** Full-response retention began with migration 0010, and it reaches 2,225 of the 68,624 canonical observations in this series, so every earlier observation is a string no third party can widen. The retired Groq arm is the irreversible case: it left the panel on 2026-08-16, contributes zero rows to Table 15, and the window effect on its 14,208 canonical observations is now unmeasurable because the text past character 200 was never written to disk. Retention is also the only reproducible artefact available, since hosted models do not reproduce their outputs exactly even at temperature zero [91, 92].

**Sensitivity reporting.** The headline figure published under both windows, per engine, in the form of Table 15. Publishing one window only leaves a reader unable to tell a 22.95-point arm from a 55.73-point arm, which is the spread Table 15 measures.

Uniformity buys something the specification did not previously claim. Measured on identical cells on 2026-09-08 across the four fully truncated arms, Fleiss' kappa on the binary outcome rises from 0.2371 at the 200-character window to 0.4881 on the whole response, on 192 cells, with the base rate moving from 0.182 to 0.672; the Claude-Gemini pair moves from 0.126 to 0.633. Part of what the market reads as disagreement between models is the instrument. The gain does not extend to every pair: the four pairs containing the retrieval-augmented arm move the other way as prevalence approaches the ceiling, where kappa loses discriminating power, so Perplexity-Grok falls from 0.413 to 0.126 while its observed agreement rises from 0.708 to 0.802. Across the whole series the effect is smaller and runs in one direction: analysing the outcome as stored rather than harmonised understates agreement by 0.086 on the five-arm panel of 4,231 complete cells.

## 7. Calibration decoys and the refusal taxonomy

### 7.1 The decoys give the instrument an empirical false-positive floor

Sixteen fictitious entities, verified as non-existent before collection, sit inside the cohort that produced every rate in this paper. They cost nothing to carry and they answer a question the rate cannot answer about itself: how often the matching rule declares a cohort entity present in prose that contains no such entity.

**Table 21.** Spontaneous naming of a fictitious entity in answers to canonical queries, none of which contains a decoy name. Series 2026-04-23 to 2026-09-08, 68,624 canonical observations, denominator is canonical rows with a non-null `response_text`, by engine. Sixteen decoys, verified as non-existent before collection.

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

**Table 22.** Adversarial probes: share flagged by the legacy hallucination criterion, and share of those flagged answers carrying an explicit refusal marker. Series 2026-04-23 to 2026-09-08, 17,919 probe observations; denominators are all probe rows for the first rate and the 17,328 flagged rows with non-empty text for the second.

| Engine | Probe n | Flagged by the legacy criterion [95% CI] | Of those, carrying an explicit refusal marker [95% CI] |
|---|---:|---:|---:|
| Gemini | 4,463 | 90.3 [89.4, 91.2] | 46.9 [45.3, 48.4] |
| ChatGPT | 4,416 | 97.3 [96.8, 97.8] | 67.4 [66.0, 68.8] |
| Claude | 4,384 | 100.0 [99.9, 100.0] | 92.4 [91.6, 93.2] |
| Groq | 4,096 | 99.7 [99.5, 99.8] | 61.7 [60.2, 63.2] |
| Grok | 368 | 99.5 [98.0, 99.9] | 50.3 [45.2, 55.4] |
| Perplexity | 192 | 85.4 [79.7, 89.7] | 15.2 [10.5, 21.5] |
| **Panel** | **17,919** | 96.7 [96.4, 97.0] | 66.8 [66.1, 67.5] |

That 96.7% of 17,919 probe responses were flagged is evidence that the marker was detecting the prompt. Of the 17,328 flagged responses carrying text, 11,569 (66.8%) contain an explicit refusal marker, among them a Gemini response of 2026-04-29 which states of the decoy named in its prompt, verbatim, that *o "Banco Floresta Digital" não é uma instituição financeira real ou registrada no Brasil*. The refusal regular expression counts only explicit markers, which puts 66.8% at the floor of the refusal share. Two counts of the 2026-08-31 snapshot circulate in the repository, 11,195 of 16,579 at 67.5% and 10,775 of 15,993 at 67.4%, neither recording which extraction produced its base; Table 12 carries the first. That three bases of 15,993, 16,579 and 17,328 return 67.4%, 67.5% and 66.8% is the only stability this figure has been given, and it is stability of the proportion rather than agreement on the count.

The engine spread is the operational result. Claude carries a refusal marker in 92.4% of its flagged answers and the retrieval-augmented arm in 15.2%, so a headline hallucination rate computed under the legacy criterion ranks engines mostly by how explicitly they decline. BRGEO-1 therefore specifies a three-way outcome: ontological refusal, where the model states the entity does not exist; epistemic refusal, where it states that it lacks information, typically citing a training cutoff, which is correct in effect and weaker in kind; and fabrication, where it describes products, history or positioning for an entity that has none. Only the third is a hallucination, and a protocol that pools all three reports a false-positive rate of 96.7% on 17,919 probe observations, of which 66.8% of the 17,328 flagged responses carrying text already show an explicit refusal marker, so the pooled figure counts refusals as hallucinations.

The taxonomy is proposed and not validated. There is no inter-annotator agreement, no human-labelled sample, no confusion matrix of the automatic classifier against a gold standard, and no measured distribution across the three categories. Estimating fabrication as the complement of a refusal detector is inference of the kind this paper criticises elsewhere: the residual contains refusals phrased outside the detector's vocabulary, empty responses, clarifying questions and answers about real homonyms. Fabrication requires positive detection of invented verifiable attributes, and §14 carries this as the principal open item in the specification. Validation also owes the abstention literature an explicit mapping. The survey of abstention in large language models sets out the field's own categories [40], unanswerable-question benchmarks measure the behaviour at question level [38, 39], and the entity-query surface these probes use has its own instruments [36, 41]. A three-way taxonomy that neither aligns with those categories nor says where it departs from them will be read as parallel invention.

### 7.3 Probe coverage excludes the arm worth probing

The probe stratum reaches the retrieval-augmented arm in 192 of 17,919 observations, 1.1% of the stratum. Each of the four parametric arms that ran the whole series carries 4,096 to 4,463 probe observations and the arm that entered in August carries 368, because provider routing sent the retrieval arm a subset of query categories that largely excluded the calibration category. The exclusion removes the most informative case. An engine that searches before answering holds evidence a parametric model does not, namely the absence of any source for a firm that was invented for the purpose, and whether it converts that absence into a refusal is the question the instrument exists to ask. The 192 observations available are consistent with something worth measuring properly, 85.4% flagged and the lowest refusal-marker share in the panel at 15.2% [10.5, 21.5] on 164 flagged rows, and 164 rows on one arm settle nothing. BRGEO-1 requires probes to cover every engine in the panel at the battery's declared size, and every figure in §7.2 describes five parametric arms plus a token presence of the sixth.

---


## 9. Five months of descriptive evidence

### 9.1 Every figure here is descriptive, and the confirmatory window is still open

Every figure below is descriptive and pre-confirmatory, and the constraint that makes it so is arithmetic rather than editorial. The design is observational: the cohort of 127 entities, the battery of 192 queries and the engine panel were fixed before collection, nothing was manipulated, and no estimate here supports a causal reading. The confirmatory window declared in §8.3 has not closed. It counts 90 collected days rather than 90 calendar days, the calendar ninetieth day passed on 2026-07-21, and on 2026-09-11 the count stood at 56 with a projected close of 2026-10-15 (§8.3). The analysis plan of §11 is the instrument for that window; §9 is what the instrument saw on the way there.

The series analysed runs from 2026-04-23 to 2026-09-08 and holds 68,624 canonical observations, read under the uniform 200-character window that §6 requires and re-extracted with the project's own matching rule. Every rate in this section is a head-of-response rate. §6.5 puts the distance between that rate and the whole-response rate at 22.95 to 55.73 percentage points across five arms on 2,225 matched observations, so no figure here should be quoted as an engine's citation rate without the window attached to it.

The sample size that governs inference is not 68,624. The battery re-asks the same 192 prompts twice a day, so the prompts are the population a general claim would have to reach, and they are observed deeply rather than sampled.

**Table 23.** Design effect for the pooled citation rate under two candidate primary sampling units. Series 2026-04-23 to 2026-09-08, 68,624 canonical observations; denominator for each arm is its own canonical rows. The query-clustered columns cluster on the prompts the arm answers, 192 in each arm row and 96 in the retrieval-augmented one, and on the 1,056 engine-by-prompt cells in the panel row. Grok is omitted: with 5 collected days the estimator is not run (`stats/data/s2_dependence.csv`, status `NOT RUN`). Source `stats/data/s2_dependence.csv`.

| Arm | Naive SE (pp) | Day-clustered SE (pp) | Day deff | Query-clustered SE (pp) | Query deff | Effective n (query) |
|---|---:|---:|---:|---:|---:|---:|
| ChatGPT | 0.306 | 0.097 | 0.10 | 2.563 | 70.1 | 216 |
| Claude | 0.357 | 0.159 | 0.20 | 3.017 | 71.6 | 210 |
| Gemini | 0.109 | 0.132 | 1.46 | 0.574 | 27.8 | 553 |
| Perplexity | 0.568 | 0.816 | 2.07 | 3.743 | 43.5 | 178 |
| Groq | 0.234 | 0.133 | 0.32 | 1.883 | 64.7 | 220 |
| **Panel** | **0.147** | **0.193** | **1.74** | **1.166** | **63.3** | **1,083** |

Clustering on the collection day, which the methodology anticipated through a random intercept per date, inflates the pooled standard error by 1.32 and inflates nothing at all in three of five arms, whose day-level design effects sit below one because a day is close to a census of the prompt population. Clustering on the engine-by-prompt cell, 1,056 clusters over the panel, gives a pooled design effect of 63.3, an eightfold inflation, and an effective sample of 1,083 against a nominal 68,624; inside a single arm, where the cluster is the prompt itself, the design effect runs from 27.8 on Gemini to 71.6 on Claude. On the canonical cut the pooled rate of 17.97% carries a naive half-width of 0.29 points, a day-clustered half-width of 0.38 and a prompt-clustered half-width of 2.29.

The multilevel model of §9.2 measures the same dependence coefficient by coefficient and on the square-root scale, where its clustered standard errors run from 2.4 to 10.4 times the binomial ones: an inflation of 8.0 is a design effect of 64, so the 63.3 above and the inflation column of Table 24 are one quantity written two ways. The inflation is smallest on the engine contrasts, which vary inside a prompt, and largest on the covariates that are properties of the prompt, whose block tests carry design effects of 74 to 90 (`stats/S1-multilevel.md`, Tables 4 and 5). The Wilson intervals printed in the tables below are of the first kind, correct for a statement about these 192 prompts as answered by these arms and eight times too narrow for a statement about the population of prompts those 192 were drawn from. Where a claim generalises beyond the battery, the third figure is the one that applies, and the reliability vocabulary of generalizability theory is the natural frame for reporting it [28, 76].

Two stored fields, `selection_status` and `absorption_status`, are proxies derived from mention and from name matching in exposed URLs. Neither demonstrates semantic support by a source nor internal retrieval, and neither enters any figure in this section.

### 9.2 Citation belongs to the prompt and to the firm-engine pair, and almost none of it belongs to the day

Which prompt was asked carries more of the latent variance in citation than which engine answered it, and the collection day carries almost none of it. Two analyses of this series reach that ordering along routes that share no estimator: a multilevel model over 38,195 individual responses, which is the inferential result reported here, and a two-way decomposition of logit coverage over an entity-by-engine grid, which is the convergent one.

The model is a binomial mixed model with crossed random intercepts for prompt and for collection day, fitted on the core-3 balanced design (`stats/S1-multilevel.md`, Table 3): the 96 prompts of the three semantic categories every arm answered, 52 collection days, six engines and 38,195 responses under the uniform 200-character window. The restriction is forced by the panel. The retrieval-augmented arm never ran `confianca`, `experiencia` or `inovacao`, so engine and semantic category are not crossed over the full battery, and a six-engine model fitted on all 192 prompts would extrapolate that arm into three categories it never saw; the six-level category block is therefore tested separately on the five-arm battery of 60,883 responses. Engine enters as a fixed factor with ChatGPT as reference, because a handful of levels cannot identify a variance component; the supplement's stability ladder shows what the attempt returns at the entity level, where a five-level engine component converges at a standard deviation near 6.7 across three independent seeds while the marginal engine logits span 2.94 on the same scale.

Two estimators of the same fixed part are reported because they answer different questions. The variational Bayes fit of the mixed model gives odds ratios conditional on the prompt and the day; a pooled logistic with a two-way cluster-robust covariance on the 96 prompts and the 52 days, with inference on `t(51)`, gives population-averaged ones. The second governs every p-value quoted from this model, because a mean-field variational posterior is anti-conservative and its intervals here run about eight times narrower than the clustered ones. The two disagree by a factor near two on the same contrast, 14.49 against 6.79 for the retrieval-augmented arm against ChatGPT, so a claim about engines in general takes the population-averaged figure and a claim about the same prompt on the same day takes the conditional one.

**Table 24.** Fixed effects of the multilevel model under two estimators. Series 2026-04-23 to 2026-09-08, core-3 balanced design, 38,195 responses on 96 prompts, 52 collection days and 6 engines, uniform 200-character window; reference cell is ChatGPT, fintech, English, directive, `comparativo`. The conditional column is the variational Bayes mixed model with crossed random intercepts for prompt and day, with credible intervals from that posterior; the population-averaged column is the pooled logistic with two-way clustering on prompt and day, `t(51)` intervals and the p-value in the last column. Inflation is the clustered standard error divided by the binomial one. Source `stats/S1-multilevel.md` Tables 3 and 4, computed by `stats/s1_multilevel.py` into `stats/s1_results.json`.

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

One interaction changes a market reading and two do not reach the threshold. Engine by vertical survives the design correction at a corrected p of 0.00305, and the spread between an engine's best and worst vertical runs from 58.46 points on Grok and 56.07 on Claude down to 17.93 on ChatGPT and 5.00 on Gemini, which is why the all-verticals column of Table 28 summarises the first two badly and the last two well. Its Wald p of 3.72e−35 on the clustered covariance is set aside in favour of the corrected likelihood ratio, because 15 parameters against 52 clusters produce a rank-deficient and anti-conservative sandwich. Query type by vertical fails at 0.645, and the marginal test of engine by language fails at 0.354 for a reason that belongs to the contrast rather than to the effect, which §9.4 measures inside the matched pair.

**Table 25.** Variance decomposition by level, on the latent logistic scale. Series 2026-04-23 to 2026-09-08. The response-level panel is the core-3 balanced design, 38,195 responses over 96 prompts, 52 days and 6 engines, outcome "at least one cohort entity inside the first 200 characters". The entity-level panel takes one response-by-candidate-entity pair as the unit over the five arms truncated at collection time, on a stratified subsample of 5,988 responses giving 166,164 entity-rows, with the intraclass correlation averaged over three seeds and the variance read on seed 11; the retrieval-augmented arm is excluded because its stored text is the whole response, so per-entity restriction to the window is impossible for any entity after the earliest. Engine is carried as a fixed factor in both panels and converted by the Nakagawa-Schielzeth rule. Intraclass correlation is the level's variance over the sum of the components plus the logistic residual of π²/3 ≈ 3.290. Source `stats/S1-multilevel.md` Tables 6a and 6b.

| Level | Response σ² | Response ICC | Entity σ² | Entity ICC |
|---|---:|---:|---:|---:|
| Entity identity | not in the model | — | 10.601 | 0.4641 |
| Prompt | 7.709 | 0.4559 | 5.994 | 0.2840 |
| Engine | 5.905 | 0.3492 | 2.144 | 0.0993 |
| Residual (logistic) | 3.290 | 0.1946 | 3.290 | 0.1491 |
| Collection day | 0.005 | 0.0003 | 0.042 | 0.0011 |

What dominates depends on which question the unit of analysis encodes. With the response as the unit and the outcome "was anybody named", the prompt takes 45.59% of the latent variance and the engine 34.92%, leaving the day at 0.03% (Table 25). With the response-by-entity pair as the unit and the outcome "was this company named", the entity's own identity takes 46.41%, the prompt 28.40% and the engine 9.93%, leaving the day at 0.11%. Whether a Brazilian entity is named at all is mostly a property of the question; which Brazilian entity is named is mostly a property of the entity. Both engine figures are transformations of a fixed factor and not random-effects variances, and they carry that qualifier because a variance component over five or six levels is weakly identified in this design: the entity-level engine share would have been published as 0.69 instead of 0.10 had the stability ladder of `stats/S1-multilevel.md` not been fitted.

The most consequential number in the model is the one that refused to move. Fitting the same crossed random structure with no covariates at all puts the variance between the 96 prompts at 4.005 on the logit scale; adding vertical, language, query type and semantic category, which are four of the five axes the battery was balanced on, puts it at 4.036, a change under 1% and in the direction of a slightly larger component. The four design factors account for none of the variation between prompts, while that variation is the largest component in the response-level decomposition. Whatever makes one prompt orders of magnitude more likely than another to surface a cohort entity is not captured by the axes used to build the battery, and the battery was built on the assumption that it would be.

That result bears directly on P3. Declaring the battery is not the same as characterising it. Two batteries balanced on the same four factors, with equal counts in every cell, can return citation rates far apart, because the factors carry no information about which prompts elicit names, and an adopter who publishes the factorial invariants of §3.1 has made the battery checkable without making it interchangeable with anyone else's. The query-clustered intervals of §9.1 measure the same limit from the sampling side, putting the retrieval arm's 53.78% on this battery at 46.35% to 61.21% on a newly drawn one; §14 carries the threat in its own row.

The second path to the same question starts from a different grid and holds different terms, which is why it is worth reading beside the model rather than in place of it. Citation is also a property of the firm-engine pair: over a balanced grid of 62 named entities by 6 engines, the firm takes 34.46% of the variance in logit coverage, the engine 26.21%, and the firm-by-engine interaction 39.33%, so the largest single term is the one saying that which firm gets named depends on which engine is asked.

**Table 26.** Two-way decomposition of logit coverage. Series 2026-04-23 to 2026-09-08, 62 entities by 6 engines, one observation per cell, rates offset by 1/(2 × 42,487) before the logit; denominator is the total sum of squares. The 62 are the cohort members named at least once in the replicate-reduced grid of 42,487 cells; the 66 of §9.6 counts entities named at least once over all 68,624 observations.

| Source | Sum of squares | Share of total |
|---|---:|---:|
| Entity (firm) | 1,880.12 | 34.46% |
| Engine | 1,429.96 | 26.21% |
| Entity × engine interaction | 2,145.56 | 39.33% |

Neither analysis nests inside the other and their terms do not map one to one. The grid carries no prompt term, since each of its 372 cells aggregates over every prompt that arm answered; the model carries no entity-by-engine interaction, since its entity-level fit holds engine as a fixed factor. Where the two can be compared they agree, and they agree on the two statements a buyer acts on. The collection day is negligible under both, at 0.28% of cell-level variance across 42,487 replicate-reduced cells and at intraclass correlations of 0.0003 and 0.0011, so instability over the five months is not what produces the disagreement between engines, and day-to-day movement in a citation dashboard built on this design is measurement noise unless it survives an interval built on the day cluster. The engine sits below the leading term under both, which is the arithmetic behind the finding that a single per-engine number summarises nothing on the three arms whose spread across verticals exceeds 40 points.

Agreement between engines is low and the low value is not a sampling artefact. On the panel that runs the full five months on the full battery, Fleiss' kappa on the harmonised binary outcome is 0.086 over 9,129 complete cells from 50 days; adding a fourth continuously observed arm raises it to 0.169 over 8,550 cells, which rewards a rater that shares the majority pattern rather than recording convergence. No six-engine figure exists: Groq's last collection day is 2026-08-16 and Grok's first is 2026-08-23, so the six-way panel has zero complete cells.

**Table 27.** Fleiss' kappa on the harmonised binary outcome, by nested panel. Series 2026-04-23 to 2026-09-08, percentile intervals from 2,000 day-cluster bootstrap replications; denominator is complete panel cells.

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

**Table 28.** Citation rate under the uniform 200-character window by engine and vertical, with within-vertical concentration on the real cohort. Series 2026-04-23 to 2026-09-08, 68,624 canonical observations; denominator for each rate is the canonical rows of that cell, and for each index the mentions of that vertical. Bootstrap intervals on the indices are percentile over 2,000 observation-cluster replicates.

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

**Table 29.** Paired Portuguese against English contrast, overall and by engine. Series 2026-04-23 to 2026-09-08, 21,862 matched pairs over 52 collection days under the uniform 200-character window. `Rate PT` and `Rate EN` are the two halves of the same pairs; the paired difference is the mean of the within-pair difference in percentage points, with a day-clustered interval; `PT-only` and `EN-only` are the discordant counts; `p` is the exact McNemar binomial test on those discordant pairs, and all seven survive Benjamini-Hochberg inside the confirmatory family of 17. Source `stats/S1-multilevel.md` Table 8.

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

The marginal contrast is the same effect read through a comparison the design cannot support, and it is reported here as context for the paired figure. Over the full canonical cut, 20.22% of the 34,310 English observations carry a citation against 15.72% of the 34,314 Portuguese ones, with Perplexity again running the other way at 54.17% in Portuguese against 49.90% in English. Entered as a fixed effect, language returns an odds ratio of 0.852 [0.497, 1.459] at a two-way clustered p of 0.552 (Table 24) and a design-corrected likelihood-ratio p of 0.549 under a design effect of 89.50, which measures the power of a between-prompt contrast where the prompt carries 45.59% of the variance. Publishing only the marginal figure would report a null the pairing contradicts at p = 2.86e−74 over 21,862 pairs. The interaction with the firm's origin is where the remaining measurement decision lies.

**Table 30.** Per-slot naming rate by group and language, and the language interaction. Series 2026-04-23 to 2026-09-08, 68,624 canonical observations. Per-slot rate is mentions divided by (observations × entities in the group), which is the probability that a given cohort member is named in a given answer. Log rate ratio is Brazilian over anchor; intervals are percentile cluster bootstrap over observations, 2,000 replicates.

| Vertical | Brazilian rate, PT | Anchor rate, PT | Brazilian rate, EN | Anchor rate, EN | log RR, PT | log RR, EN | Difference (PT less EN) | 95% interval | Bootstrap p |
|---|---:|---:|---:|---:|---:|---:|---:|---|---:|
| Fintech | 1.921% | 0.001% | 2.416% | 0.001% | 7.188 | 7.417 | −0.229 | [−1.364, 0.898] | 0.5885 |
| Retail | 1.339% | 0.645% | 1.933% | 0.324% | 0.730 | 1.786 | −1.056 | [−1.211, −0.910] | < 0.0005 |
| Health | 0.833% | 0.289% | 0.615% | 0.124% | 1.059 | 1.602 | −0.543 | [−0.992, −0.191] | 0.0020 |
| Technology | 0.252% | 1.056% | 0.886% | 0.348% | −1.434 | 0.936 | −2.370 | [−2.590, −2.153] | < 0.0005 |
| All | 1.078% | 0.497% | 1.453% | 0.199% | 0.775 | 1.988 | −1.213 | [−1.339, −1.090] | < 0.0005 |

Asked in Portuguese about Brazilian technology and IT, the engines name an international anchor at 1.056% per slot against 0.252% for a Brazilian firm, a rate ratio of 0.24. Asked the same question in English, from the same battery translated, the ratio is 2.55 the other way. The difference of 2.370 on the log scale is a sign change rather than a change of magnitude, and its interval excludes zero by a wide margin. Retail and health favour Brazilian firms in both languages and favour them more strongly in English. Fintech records 2 anchor matches in 137,800 entity slots, so its rate ratio is numerically unstable and is tabulated without interpretation.

The consequence for anyone measuring a Brazilian brand is direct. A visibility figure taken only in English reports the language in which local firms do best against international anchors across the panel, at a pooled log rate ratio of 1.988 against 0.775 in Portuguese, and in technology it reports the only language in which the local firm leads at all. A brand whose customers ask in Portuguese and whose dashboard asks in English is reading a different measurand, and the gap is largest exactly where a Brazilian technology vendor competes with a global consultancy. Declaring the language of the battery is therefore not a courtesy to the reader; it is the condition under which the figure identifies a quantity, which is the same argument the window carries in §6 and which the cross-language literature reaches from the sampling side [26]. A parallel result holds for the provenance of the model rather than the language of the query. Over 1,909 English-only queries put to six models about 30 brands, Chinese-developed models mention a brand in 88.9% of answers against 58.3% for internationally developed ones, a gap of 30.6 points that survives identical wording, because a brand absent from a model's training corpus has no presence in its answers whatever its quality [25].

### 9.5 Directive queries buy names, and one arm runs half the categories

A question that asks for a named best is answered with a name two and a half times as often as one that asks for the landscape. Directive queries carry a citation in 25.93% of 34,319 observations against 10.00% of 34,305 exploratory ones, and the ordering holds in every one of the six arms.

**Table 31.** Citation rate under the uniform 200-character window by query type and by semantic category. Series 2026-04-23 to 2026-09-08, 68,624 canonical observations; denominator is the canonical rows of each cell. The five-arm rows are the panel rows of T7c with the Perplexity row subtracted, since that arm runs only three of the six categories; their intervals are Wilson on the resulting counts (`tables/NUMBERS.md` T7c). Per-arm counts by query type are in T7b of the same file.

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

**Table 32.** Concentration, exclusion and what predicts it. Series 2026-04-23 to 2026-09-08, 68,624 canonical observations under the uniform window. Coverage counts an entity once per observation in which it appears; first mentions count it only when it is the earliest cohort name. Odds ratios come from a logistic regression of never being named on the attributes the cohort file carries, fitted on the 111 real members with Brazilian, head tier and fintech as the reference cell.

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

Tier is the attribute that separates. A long-tail firm carries 11.4 times the odds of never being named that a head firm carries, the tier block returns a likelihood-ratio p of 0.0007 on 111 entities of which 45 are never named, and the model reaches a McFadden pseudo-R² of 0.1467. Vertical separates nothing, which agrees with the exclusion row of Table 28. The anchor coefficient needs the caveat printed with it: all 32 international anchors are head tier, so the adjusted odds ratio of 5.418 compares anchors with Brazilian head firms alone, 15 of 32 (46.9%) against 5 of 34 (14.7%), while unadjusted the two groups barely differ at 46.9% against 38.0%. The confounding between group and tier is total, and the adjustment produces the whole contrast.

The shape of the upper tail is not determined, and saying so is the result. Under the Clauset-Shalizi-Newman rule the estimated xmin sits at 246 mentions, which leaves 19 entities in the fitted tail out of 66 with any mention at all. The exponent is 2.225 with a 95% interval of [1.674, 2.776], the bootstrap goodness of fit does not reject the power law (p = 0.9570), and the likelihood-ratio comparison against a lognormal returns a normalised R of −0.0091 with p = 0.9927, which is the numerical statement that the two families fit the same 19 points equally well. The fitted lognormal is degenerate along a ridge. The constraint is structural rather than temporal: the cohort holds 111 real firms by design and 66 were ever named, so no amount of further collection puts more than a few dozen points into a tail fit. The sentence "citation follows a power law" is not available from this design, and an exponent quoted without the 19 would be a stronger claim than the data carry.

Answers name firms in clumps. Across the 68,624 observations, 82.03% name nobody, 12.42% name exactly one entity and 5.54% name two or more, with a mean of 0.2777 and a variance-to-mean ratio of 1.993. A negative binomial fitted with an intercept alone beats the Poisson on both information criteria (AIC 89,146 against 99,876) and beats the zero-inflated Poisson (90,882), reproducing the observed zero count to within 55 answers; the zero-inflated negative binomial estimates its inflation probability at 1.01 × 10⁻⁵ and BIC prefers the simpler model by 11.14. Abstention was measured directly on the probe stratum and §7.2 reports it; position inside the answer is reported in §6.6, where the relative offset stops separating the engines once the truncation is removed. The zeros carry no manufactured names either, since no decoy was named spontaneously in any of the 68,624 canonical observations, which holds the 95% Wilson upper bound on the instrument's spontaneous false-positive rate at 0.0056% on the panel and at 0.342% on the 1,118 observations of the seventeen-day Grok arm (§7.1). One overdispersed process generates the zeros and the multiple mentions alike, so nothing in the count distribution requires a separate abstention mechanism, and a reader who sees a zero in Table 28 is looking at silence inside the window rather than at a refusal the instrument classified.

<img src="figures/fig2-lorenz.svg" alt="Figure 3">

**Figure 3.** Lorenz curves of entity coverage, one line per denominator, drawn from `stats/data/s4_lorenz_global.csv` (four series: mentions over the real cohort of 111, over the full cohort of 127, over the 66 named entities, and first mentions over the real cohort) with the by-vertical panel from `stats/data/s4_lorenz_by_vertical.csv`. Horizontal axis, cumulative share of entities from 0 to 1; vertical axis, cumulative share of mentions. The diagonal is drawn for reference and each curve is labelled at its right-hand end with its Gini. The spread between the named-only curve at 0.7475 and the real-cohort curve at 0.8499 is the whole content of the denominator choice.

### 9.7 What the series does over time, and what that implies for reporting frequency

Ranking is the part of this measurement that survives a week; the level of an individual mid-tier entity is not. Before any of that reads as a time series, the calendar has to be declared. The span of 139 days holds observations on 52 of them under the local-date rule of §8.2, 37.4% coverage, or on 53 under the UTC rule of Appendix D. One hole runs 59 consecutive days, from 2026-06-10 to 2026-08-07, and July is empty in full. A reader who treats the series as a four-and-a-half-month daily panel overstates its temporal density by a factor of 2.7, and any line fitted across it interpolates over two months of no observation (§8.2).

**Table 33.** Trend per arm in percentage points per 30 calendar days, on the daily rate under the uniform window. Series 2026-04-23 to 2026-09-08; denominator for each arm is its collected days. Theil-Sen carries a distribution-free interval; Mann-Kendall is reported under the standard variance and under the Hamed-Rao variance inflated by the autocorrelation of the de-trended ranks; the logistic model is fitted at observation level with day-clustered errors and q is Benjamini-Hochberg over the twelve rows that were run, the three Grok rows carrying no p-value. Source `stats/data/s2_trend.csv`.

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

That pattern sets a reporting rule with a number attached. A brand in the top ten can be measured monthly and will not be misread. The second daily round buys precision and nothing else: paired within the day over the 24 days on which both rounds ran, the pooled morning-minus-evening difference is +0.01 points with an interval of [−0.21, +0.22], and no arm-level contrast survives correction over the family of fourteen tests. Findings of this kind also carry a shelf life, which is the reproduction problem algorithm audits have already met [5]. A brand in the middle band, measured in any single week, has a better than even chance of being placed three or more ranks from where the next week would place it, which is why a claim about its position needs a multi-week average or an explicit interval rather than a weekly snapshot, and why P4 pins a model snapshot against silent provider updates [90].

## 10. The reporting index, and evidence against leaning on it

### 10.1 The index, and the three components it is made of

BRGEO-1 defines a reporting index and then constrains everything except the index. Let *E* be the cohort, *M* the engine panel, *w* the declared window and *μ* the matching rule of P6, returning the offset of the first mention of entity *e* in a response or infinity if absent. Coverage *C<sub>w</sub>(e)* is the share of panel observations naming *e* within the window; prominence *P<sub>w</sub>(e)* is one minus the offset of the first mention divided by *w*, averaged over the observations in which *e* appears, normalised by the declared window rather than by response length so that it stays comparable across engines; breadth *B<sub>w</sub>(e)* is the share of panel engines naming *e* at least once. The index is their geometric mean:

$$\mathrm{GCI}_w(e) = \left( C_w(e) \cdot P_w(e) \cdot B_w(e) \right)^{1/3}$$

The geometric mean is invariant to rescaling of the components and penalises imbalance more heavily than the arithmetic mean, which is the ground on which the composite-indicator review recommends it [56]. The geometric mean is called non-compensatory, and that holds only in the limit: it vanishes when a component is exactly zero, and an entity absent from one engine of six retains *B* = 5/6, so the penalty is gradual. Panel membership is the one decision in this definition that the specification does not yet fix, and §14 records what that cost: the reference implementation resolved it in code twice, first by an undeclared minimum observation count and then by a recency rule, and neither value appears in BRGEO-1. What the specification does require is that the three components be published alongside the index, and §10.2 is the reason.

### 10.2 One component carries three quarters of the index

The composite tracks simple coverage almost exactly, and that agreement is a symptom rather than a reassurance. Across the 66 entities cited at least once, Spearman rank correlation between the composite and coverage is 0.982, holding at 0.979 with each vertical's leader removed, 0.949 over the 42 entities with coverage between 0.1% and 5%, and 0.956 over the 42 below 1%. The 61 never-cited entities are excluded because Spearman is undefined over a mass of ties at zero, which is selection on the outcome and is declared as such.

Every index figure in §10.2 and §10.3 was recomputed on 2026-09-11 over the cut this paper declares, by `stats/s6_index.py`, and the earlier figures are superseded. They were produced by the reference implementation on a snapshot that closed on 2026-08-31 with 66,399 canonical observations, under a panel selected by the undeclared observation count §14 records, and were reported under a caption naming the series that closes on 2026-09-08. The subset correlations barely move: 0.978 becomes 0.979, 0.945 over 42 entities becomes 0.949 over the same 42, and 0.960 over 44 becomes 0.956 over 42, since two entities that sat below 1% coverage on the shorter cut sit above it on the longer one. The variance shares and the aggregation matrix move enough to be worth naming, and each is named where it appears.

Re-running the same script on the superseded cut, under the panel rule in force when those figures were produced, establishes something the earlier table did not declare. With the cut closed at 2026-08-31 and the panel restricted to arms holding at least 500 observations, the variance shares come back at 74.7%, 16.9% and 8.4%, identical to the figures published, and the aggregation matrix comes back within 0.007 of every published cell. Two published values do not come from that configuration: Var(log) of coverage at 4.490 and the count of seven entities holding their exact rank both reproduce on the six-arm panel over the same cut, which returns shares of 72.9%, 19.1% and 8.1% instead. The earlier table was therefore assembled from more than one run, which is a second reason to read the recomputation here rather than it.

**Table 34.** Variance decomposition of the log index over the 66 entities cited at least once. Series 2026-04-23 to 2026-09-08, 68,624 canonical observations under the uniform 200-character window, over the panel of six arms that contributed to the series; contribution is Cov(log X, log GCI) / (3 · Var(log GCI)) and the three contributions sum to unity. Computed by `stats/s6_index.py`, source `stats/data/s6_variance_decomposition.csv`. The figures published on the 2026-08-31 cut were 4.490 and 74.7%, 0.306 and 16.9%, 0.198 and 8.4%.

| Component | Var(log) | Contribution |
|---|---:|---:|
| Coverage | 4.360 | 72.4% |
| Breadth | 0.369 | 18.8% |
| Prominence | 0.188 | 8.7% |

Coverage varies by orders of magnitude across the cohort while prominence and breadth are confined to narrow ranges, so the geometric mean inherits coverage's dominance by construction. Nominal weights of one third each produce effective weights of 72.4%, 18.8% and 8.7%, which is the gap between nominal and effective importance that the ratings literature formalises [55]. A buyer told that an index balances three signals is holding a coverage figure with two decorations. The panel rule moves the shares by about a point and moves nothing else: recomputed over the five arms the recency rule of the reference implementation selects on this cut, the same three shares read 73.6%, 17.5% and 9.0% over the same 66 entities.

### 10.3 Aggregation is unstable, and the specification declines to settle it

Comparing a composite against one of its own components tests nothing about aggregation. The test is against alternative aggregations of the same three components, and the OECD handbook and the sensitivity-analysis literature prescribe exactly that [54, 11].

**Table 35.** Spearman rank correlation between four aggregations of the same three components, and between each and simple coverage. Series 2026-04-23 to 2026-09-08, 68,624 canonical observations under the uniform 200-character window, over the panel of six arms that contributed to the series; n = 66 entities cited at least once. The weighted form is 0.6·C + 0.25·P + 0.15·B, an arbitrary but defensible choice included to show that a plausible weighting diverges. Computed by `stats/s6_index.py`, source `stats/data/s6_aggregation_matrix.csv`. On the 2026-08-31 cut the six off-diagonal values read 0.816, 0.983, 0.787, 0.734, 0.984 and 0.706, and the coverage column read 0.982, 0.728, 1.000 and 0.700.

| | Geometric | Arithmetic | Harmonic | Weighted | Against coverage |
|---|---:|---:|---:|---:|---:|
| Geometric (GCI) | 1.000 | 0.870 | 0.983 | 0.836 | 0.982 |
| Arithmetic | 0.870 | 1.000 | 0.788 | 0.985 | 0.784 |
| Harmonic | 0.983 | 0.788 | 1.000 | 0.752 | 0.9997 |
| Weighted | 0.836 | 0.985 | 0.752 | 1.000 | 0.748 |

The harmonic mean all but reproduces the coverage ordering, because it is dominated by the smallest component and coverage is smallest by orders of magnitude: ten of the 66 entities exchange places with an immediate neighbour and none moves further, which the earlier cut rounded to a correlation of 1.000. The aggregations not dominated by the minimum diverge from coverage and from each other, with the correlation between two defensible choices falling to 0.752 across 66 entities, against 0.706 on the earlier cut. Rank displacement between the composite and coverage has a median of 2 positions, a ninetieth percentile of 6 and a maximum of 14 out of 66, and only 9 of the 66 entities keep their exact rank; the earlier cut gave the same median and ninetieth percentile, a maximum of 10 and 7 entities holding rank. Under the five-arm recency panel the median and the ninetieth percentile hold again, the maximum falls to 12 and 13 entities keep rank, so the conclusion does not turn on which panel rule is in force. An entity's published position therefore depends on a formula choice that no property of the data adjudicates.

A standard should spend its authority where disagreement is large and resolvable. The observation window moves a single arm by 22.95 to 55.73 points and moves it for a reason that can be investigated and corrected (§6.5); the aggregation formula moves ranks by a median of 2 positions for reasons that reduce to taste. BRGEO-1 therefore fixes the conditions of observation, requires the three components to be published beside any index, and leaves the aggregation free, which is the opposite of the practice one recent multi-industry map records, a single branded score published with the components withheld [58]. Composite indicators are used for advocacy as well as for analysis [57], and a custodian that sells services in the measured domain answers that objection by measuring how arbitrary its own index is and publishing the measurement.

The reference implementation carried a defect against this specification, and it belongs in the record rather than in a footnote. Panel membership was filtered by a minimum observation count that the implementation did not declare, and on the cut of 2026-08-31 that threshold excluded an arm holding 96 observations that was live and retained an arm retired on 2026-08-16, which moved breadth, the component carrying 18.8% of the index variance, for one vertical. Commit `51159fd` of 2026-08-31 replaced the count by a 14-day recency rule anchored on the last timestamp of the data. Every index figure published before 2026-09-11 was computed on the earlier panel and is superseded by the recomputation above; §14 records the finding, and the code no longer carries it.

## 11. Pre-specified analysis plan

The confirmatory window closes at 90 collected days, projected for 2026-10-15, with 56 of the 90 reached on 2026-09-11. Nothing below is confirmatory. The plan is recorded in advance of one, and the close date has moved: a forecast made on 2026-08-10 put it at 2026-09-28 under an assumed collection rate that the credit outages of August and September broke, costing seventeen days of series (§8.3). A window defined in collected days converts an outage into a schedule extension, which is a design choice a reader should see declared rather than infer from a moving date.

The plan is published in the project repository with a verifiable commit date, and it is not registered with any independent third party. A repository under the author's control offers no guarantee that the plan was not edited after the data were seen, since the same party holds the history and the authority to rewrite it. What publication in the repository does buy is a dated artefact a reviewer can diff against the analysis code; what it does not buy is the property that makes a pre-registration worth citing. §13 lists independent registration of the next window as a governance commitment.

**Table 36.** Hypotheses for the confirmatory window, with the test, the minimum effect the design can detect and the multiplicity treatment. Minimum detectable differences are computed at 80% power on the 2,225-observation full-text cohort of 2026-09-06 to 2026-09-08 (Table S5.12), which is the only stratum in which both windows exist, and account for the design effect measured there; source `stats/data/s5_power_mde.csv` and Table 23. The confirmatory window will carry more power than these figures imply, because it runs over 90 collected days rather than three.

| # | Hypothesis | Test | Minimum meaningful or detectable effect | Multiplicity |
|---|---|---|---|---|
| H1 | Citation rates differ across verticals | Likelihood-ratio test on the vertical fixed effect in a mixed-effects logistic model with random intercepts per query and per collection day | Cramér's V ≥ 0.15; per-vertical paired MDE 6.6 to 8.2 pp unclustered, 10.8 to 16.0 pp under the estimated design effect | BH within the family of six |
| H2 | Fabrication on fictitious entities differs across engines | Three-way outcome of §7.2 on human-validated labels, tested across arms | Requires probe coverage of all six arms at declared battery size and the annotation study of §14; not estimable until both exist | BH within the family of six |
| H3 | Inter-engine agreement differs by vertical | Fleiss' kappa on the rectangular query-by-engine panel, per vertical, with day-cluster bootstrap intervals | A vertical whose interval excludes the panel figure of 0.086 (P1, 9,129 cells) | BH within the family of six |
| H4 | At least one engine has a non-stationary citation rate | Slope on day index, Mann-Kendall under the Hamed-Rao variance and day-clustered logistic, on collected days only, stratified at every declared boundary of §8.1 | 2.37 pp per 30 days is what the current series detects on the arm with the largest movement | BH across arms and within the family of six |
| H5 | Directive queries yield higher citation rates than exploratory ones | Two-proportion contrast within engine, cluster-robust on query | Cohen's h ≥ 0.2; the observed panel contrast is 25.93% against 10.00% on 34,319 and 34,305 observations | BH within the family of six |
| H6 | Window damage varies across engines and is predicted by preamble share rather than engine class | Logistic model of whether the 200-character window misses a citation, with preamble, log response length and engine, on rows retaining the whole response | Between-engine: paired MDE 5.6 to 12.9 pp by arm, 5.8 to 13.1 pp once the arm's design effect is applied; within-engine: the fitted odds ratio of 7.72 is the effect the design already resolves | BH within the family of six |

H6 has already been run in a descriptive register on the 2,225 observations that retained the whole response, and it splits down the middle (§6.6). The negative half survives: engine class does not order the damage, since four parametric arms span +30.73 to +55.73 points and the single retrieval-augmented arm sits at the bottom at +22.95. The positive half fails as stated: preamble share does not order the engines. On the pooled five-arm cohort its Spearman correlation against the delta is −0.154 (p = 0.805), against +0.800 (p = 0.104) for median response length and +0.300 (p = 0.624) for median first-mention offset; on the restricted set that removes the Gemini retention defect of 2026-09-06, preamble reaches only +0.667 (p = 0.219) while length and offset both reach +0.900 (p = 0.037). Inside an engine, preamble predicts strongly, with an odds ratio of 7.72 [3.99, 14.94] on 1,137 observations holding engine and log response length fixed. The confirmatory test therefore runs a restated H6, in which the window delta is a function of how far into the response the first cohort mention falls and preamble is one of at least two things that push it there. Running a hypothesis descriptively and then confirming it on the same data would test nothing, so the restated form is fixed now and estimated only on observations collected after 2026-09-11.

Three rules govern the whole plan. Standard errors are cluster-robust on the query within each arm, because Table 23 puts the per-arm query design effect between 27.8 and 71.6 and the engine-by-query design effect on the panel at 63.3, and any claim generalising beyond the 192 prompts inherits that inflation. Multiplicity is handled by Benjamini-Hochberg within each declared family, with the families fixed here and not after inspection. Cells below 30 observations are reported descriptively and marked, and anything not listed in Table 36 is labelled exploratory and reported without an inferential claim.

---


## 13. Governance

Custody, licensing, versioning and scope are settled. Verification of a conformance claim is not: neither a conformance test suite nor an interlaboratory study exists, so Level 1 and Level 2 conformance is self-declared, and the design that would replace the declaration with evidence is specified here rather than deferred as future work.

**Custody.** Brasil GEO maintains the specification and the reference implementation, which means publishing every change, dating it, and keeping prior versions resolvable, so that a figure measured under one version stays checkable after the next exists. Implementing BRGEO-1 and stating conformance with it require no permission from the maintainer and confer no endorsement by it.

**Licensing.** The specification is published under CC BY 4.0 and the reference implementation under Apache-2.0, which carries an explicit patent grant, and Brasil GEO holds no patent or licensing claim over either, so an adopter who forks the cohort file, the battery generator and the extractor owes no royalty and asks no permission.

**Versioning.** A change that alters what a conforming figure means increments the major version; a clarification that leaves the meaning intact increments the minor, and every published figure cites the version under which it was measured. The requirement identifiers of §3.2 survive renumbering of the prose, so an erratum, an audit finding and a conformance claim name the same requirement across two versions.

**Scope.** BRGEO-1 covers the conditions under which a citation is observed and stops there. Repetition count and reliability thresholds belong to a complementary protocol that fixes iteration tiers and reports generalizability coefficients [28]. Aggregation is left free for the reason §10 measures. Two defensible aggregations of the same components rank the same entities at a rank correlation of 0.752 over 66 entities, and the set of defensible aggregations spans 0.752 to 0.985 on the cut this paper declares, against 0.706 to 0.984 on the cut of 2026-08-31 that the earlier figures came from (§10.3). Fixing a formula would therefore impose agreement on the part of the pipeline where disagreement is least resolvable, while the conditions of observation, where disagreement reaches tens of percentage points, are where a declaration buys something [11, 55]. Adjacent problems take their own numbers, which is what allows an adopter to conform on observation without adopting anything else.

**Independence.** One governance rule constrains the maintainer rather than the adopter. Level 3 attestation may be issued only by a body independent of both the claimant and the maintainer (§3.3), following the first-party to third-party progression of conformity assessment vocabulary [80], so the custodian cannot certify the measurements of its own clients. The constraint sits in the level scheme rather than in a promise, and the competing-interest declaration below points at it.

**What conformance does not yet establish.** Conformance at Level 1 and Level 2 is self-declared, which reproduces in miniature the unverifiable vendor claim of §1.1. Two artefacts would replace assertion with evidence and neither exists. The first is a conformance test suite: a fixed set of stored responses with expected figures under declared parameter values, against which any implementation can be run. For a quantity with no unit and no reference material it is the closest available analogue to a calibration standard, and §14 records the limit of that analogy. The second is an interlaboratory study in the sense of ISO 5725-2 [81], and its design is declared here rather than deferred as future work. The same stored responses are distributed to three or more implementations of P1 to P6 written independently of the reference code. Each implementation returns the citation rate per arm under one declared window and one declared matching rule. The discrepancy is then decomposed into a repeatability component, obtained by re-running each implementation on the same items, and a between-implementation component, obtained across implementations, with both reported in percentage points rather than as a pass or a failure. Two scales already in the uncertainty budget of §3.7 tell a reader what the result would mean: the largest Type A component of this series is 2.39 percentage points of typical error across 88 cells, and the window occupies a Type B entry of 22.95 to 55.73 percentage points across five arms. A between-implementation term of the first order supports the comparability claim. A term of the second order refutes it, and the protocol would then be specifying the wrong things.

The exercise has a material precondition that the reference instantiation does not meet. It needs shared items, and the only items this study can distribute are the 2,225 canonical observations retained whole, collected between 2026-09-06 and 2026-09-08, against the 68,624 collected under the protocol. The custodian cannot presently supply the item set for the exercise it proposes, which is a fact about the instrument rather than about the schedule, and §14 carries what follows from it.

---

## 14. Threats to validity

Every limitation below carries the measurement that bounds it, and three carry none: the elicitation-mode effect, the share of adversarial responses that fabricate rather than refuse, and the window effect on the retired open-weights arm. Naming those three is the point of the register, and the third is unmeasurable now because the text was never stored. The twenty-second row carries no measurement either, for a different reason the cell states: a documentary chain of provenance is not a quantity, so nothing about it is estimable.

**Table 37.** Register of threats to validity, with the measurement that dimensions each and what it leaves open. Series 2026-04-23 to 2026-09-08 except where a row names a shorter window; denominators are named per row.

| # | Threat | Measurement that dimensions it | What stays open |
|---:|---|---|---|
| 1 | Elicitation mode is a seventh parameter and is not declared | Not estimated. The one component of the same class that was measured, the observation window, moves the rate by 22.95 to 55.73 pp over 2,225 matched observations | Whether plain prompting and structured elicitation diverge at that order |
| 2 | Refusal taxonomy is proposed and not validated | 96.7% of 17,919 probe observations flagged by the legacy criterion; 66.8% of the 17,328 flagged rows carrying text hold an explicit refusal marker | The fabrication share inside the remaining 33.2%; no annotator agreement, gold standard, confusion matrix or category distribution exists [40, 38] |
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
| 18 | Model version and generation configuration move under a stable name | One boundary changed model identifier and reasoning budget in the same commit; the default reasoning budget of one replacement arm cost five consecutive collections and 129 of 179 minutes of one run before a declared change of reasoning effort fixed it | Drift is bounded by stratification and is not estimated [90] |
| 19 | The window value itself is a choice | 200 characters recovers 35.4% of first mentions across the panel, from 7.8% on Gemini to 70.2% on Perplexity, over 1,367 observations that name an entity | Head-of-response citation is defensible and is not the only defensible aperture; headline figures are reported under both |
| 20 | Aggregation instability | Rank correlations between defensible aggregations of the same components span 0.752 to 0.985 on the declared cut, the lower bound measured over 66 entities; the same span on the cut of 2026-08-31 was 0.706 to 0.984 | Whether the composite separates in a less concentrated market |
| 21 | Nothing here is causal | Cohort fixed, battery fixed, no intervention performed across 68,624 observations | Whether a firm can act on its rate, and whether naming tracks standing |
| 22 | The metrological analogy has no unit and no hierarchy | Not a quantity, so not estimable: metrological traceability requires a documented unbroken chain of calibrations [7], and no such chain, reference material or national reference exists for a citation rate | The measurand is constituted by convention [10, 9] |
| 23 | The battery's own design factors account for none of the variance between prompts | The prompt carries 45.59% of the latent variance over 38,195 responses on 96 prompts and 52 collection days; adding vertical, language, query type and semantic category to the same crossed random structure moves the between-prompt variance from 4.005 to 4.036, under 1% (§9.2) | Whether a second battery balanced on the same four factors reproduces this one's rate. P3 publishes the invariants that make a battery checkable and does not make two balanced batteries interchangeable |
| 24 | Repeated runs return byte-identical text and the series cannot say why | 47.84% of the 22,495 engine-by-prompt-by-day cells holding more than one run are byte-identical across runs, 71.88% on the retired open-weights arm against 0.04% on the retrieval-augmented one, and the 68,624 canonical rows carry 14,391 distinct response hashes; the configured cache lifetime is 20 hours against rounds twelve hours apart (§4.7) | A cache hit against near-deterministic decoding of a short prefix. No column of `citations` records whether a row was served from cache, so the two cannot be separated in this series |
| 25 | An analysis module stores a standard deviation under a key named for a variance | `src/analysis/mixed_effects.py` writes `exp(vcp)` into `random_variances` while `statsmodels` parameterises the component as `log σ`, so the stored quantity is σ where the key promises σ². Zero figures in this paper read that key | H1 of Table 36 names the same module as committed analysis code for the confirmatory window |

Nine of those rows carry an argument the table cannot hold.

**Elicitation mode is the largest unmeasured quantity in the study.** The battery sends plain natural-language prompts and entities are extracted afterwards, which is closer to what a user reads than instructing a model to return a structured list of company names. No pilot has compared the two. The reason this sits at the top of the open items is the size of the one comparable quantity that was measured: a single undeclared difference in how much of the answer was read moved five arms by 22.95 to 55.73 percentage points on 2,225 matched observations. A protocol that fixes six parameters while a seventh of unknown magnitude varies freely has not finished the job, and the honest form of the claim in §3 is that BRGEO-1 declares the conditions it has identified.

**The interval this paper publishes depends on which claim it is making.** Table 23 puts the engine-by-prompt design effect on the panel at 63.3 and the day-clustered inflation of the pooled standard error at 1.32, with three of five arms showing no day-level inflation at all, because every round re-asks the same fixed battery and a day is close to a census of the prompt population. Any statement in this paper that generalises beyond these 192 prompts carries the second interval, and any statement about these 192 prompts carries the first. The distinction is the reason §9 reports strata descriptively and the reason a published rate whose interval came from the observation count is reporting a quantity below the floor that definitional uncertainty already sets [7].

**The calendar removes the events that matter most.** The coverage of row 7 of Table 37 would be a power problem on its own; the shape of the hole makes it a design problem, since 15 of 21 declared event-by-arm pairs cannot be confronted with blind change-point detection because a hole sits on the boundary. The events and the outages have common causes, since the late-August gap exists because the fifth arm consumed 129 of 179 minutes of a run under its provider's default reasoning budget and the fix for that consumption is itself a declared configuration event, which is why §3 requires the boundary to be declared in advance and stratified by rule.

**Censoring runs in both directions and both make the reported figures conservative.** The 200-character window censors the head of the answer, which §6 measures. The provider's own output cap censors the tail: Gemini's stored responses on 2026-09-07 and 2026-09-08 end mid-word at means of 3,540 and 3,684 characters, and Grok's do so on 9.1% of the 768 Grok responses retained whole. A response that was cut before the model finished can only lose citations, so every whole-response rate in this paper is a floor rather than an estimate, and Gemini's 65.10% over the 384 observations of the restricted subset is a lower bound with an unknown distance to the true value. The retired open-weights arm is the case with no floor at all, because its 14,208 canonical observations hold no text beyond character 200 and regeneration is not a substitute: hosted models do not reproduce their outputs exactly at temperature zero [91, 92].

**Two of the paper's agreement statements are read against ceilings rather than against unity.** Rows 11 and 12 of Table 37 carry the two facts: the six-engine panel the design describes never existed, and the two affected arms disagree with themselves twelve hours apart. Part of what this paper counts as disagreement between engines on those arms is that self-disagreement, and no decomposition separates the two components. The Fleiss figures of §9 are therefore lower bounds on the agreement a stable instrument would report, in the same direction as the window correction and for a different reason.

**The battery's design factors do not characterise the battery.** The multilevel model of §9.2 puts 45.59% of the latent variance between the 96 prompts, then finds that the four factors the battery was balanced on account for none of that share: with no covariates the between-prompt variance is 4.005 on the logit scale, and with vertical, language, query type and semantic category all present it is 4.036. P3 requires the full battery and its factorial invariants to be published, which is what makes an instrument checkable by a second party. Row 23 records what the requirement does not deliver, which is comparability between two batteries balanced the same way, since balance on those four axes carries no information about which prompts elicit names. An adopter setting a figure beside this paper's is comparing prompt samples before comparing engines, and the width that claim has to carry is the query-clustered interval of §9.1: 46.35% to 61.21% around a measured 53.78% on the arm with the highest rate.

**Repeated runs return the same bytes often enough to matter, and the series cannot say why.** Of the 22,495 engine-by-prompt-by-day cells holding more than one run, 47.84% are byte-identical across runs, and the 68,624 canonical rows carry 14,391 distinct response hashes. The distribution across arms is the part that discriminates: 71.88% on the retired open-weights arm and 0.04% on the retrieval-augmented one, with ChatGPT at 58.25% and Claude at 60.60%. Two explanations survive the measurement. A cached answer served inside the configured 20-hour lifetime against rounds twelve hours apart is possible by construction (§4.7), and near-deterministic decoding of a short prefix at temperature zero would produce the same repetition with no cache involved. The pattern across arms favours the second reading, because the arm that searches the web almost never repeats itself while the parametric arms repeat constantly, which is the ordering a deterministic decode predicts and one a cache keyed on the query text has no reason to produce. The series cannot decide between the two, because no column of `citations` carries a cache flag and the information was never written.

That open question has a requirement attached to it and a passage of §3.1 on the other side of the same axis. An implementation that intends to measure run-to-run variation records, per observation, whether the response came from cache, and that record belongs in the declared generation configuration of P5 beside temperature, seed and output caps, because without it the run-to-run term of an uncertainty budget cannot be told apart from a replay of the previous round. P5 already concedes the converse half: it pins the request and not the response, since hosted models do not reproduce their outputs exactly at temperature zero [91, 92]. One passage says repetition cannot be assumed; row 24 says repetition arrived anyway, on four arms of six, between 28.37% and 71.88% of their multi-run cells. Neither is evidence about the other until a cache flag separates them, and the coefficient-level cost of leaving it open is bounded: collapsing every byte-identical repeat and refitting the model of §9.2 over the surviving 31,975 responses takes the retrieval arm's odds ratio from 6.794 to 6.508 and Gemini's from 0.089 to 0.078, well inside the interval of either fit.

**One analysis module in the repository names a standard deviation a variance.** `src/analysis/mixed_effects.py` stores `exp(vcp)` under the key `random_variances`, and `statsmodels` parameterises each random component as `log σ`, so the value behind that key is σ where the name promises σ². Nothing in this paper reads it, because the S1 script performs its own conversion and publishes σ and σ² side by side, and `random_variances` is read by no other module in the repository. The reason it belongs in this register rather than in a changelog is Table 36: H1 of the confirmatory plan names that module as the committed code for the mixed-effects test, so the mislabelled key sits one run away from a published variance component that would be out by a square root.

**The metrological vocabulary is borrowed for its discipline and not for its guarantees.** A citation rate has no SI unit, no calibration hierarchy and no national institute holding a reference copy, so the chain that BRGEO-1 offers is documentary: a published figure resolves to a specification version, which resolves to six declared parameter values, which resolve to published artefacts and to stored responses a third party can re-extract. Metrological traceability in the strict sense requires a documented unbroken chain of calibrations, each of which contributes to the measurement uncertainty [7], and that chain does not exist here. The measurand is constituted by convention rather than discovered, which is the standing position for unobservable constructs [10, 9], and what a documentary chain buys is set out in §1.2: a convention written down is one a second party can dispute clause by clause, which is a weaker property than correctness and the only one available here.

---

## 15. Discussion

Five results in this paper are measurements and five of its propositions are designs, and a reader who mixes the two will overreach in one direction or dismiss the work in the other. Table 38 sets each measurement beside the proposition it does not support.

**Table 38.** What the evidence establishes and what the paper proposes without evidence. Series 2026-04-23 to 2026-09-08, 68,624 canonical observations, except the window rows, which cover 2026-09-06 to 2026-09-08 and 2,225 matched observations, and the multilevel row, which covers the 38,195 responses of the core-3 balanced design.

| Established, with its measurement | Proposed, with what would test it |
|---|---|
| Reading the whole response instead of the first 200 characters raises the rate on every arm that retained text, by 22.95 to 55.73 pp, with 0 reversals in 2,225 matched observations and exact McNemar p from 1.69e-21 to 2.89e-129 | That declaring the six parameters produces comparability between independent measurements. Tested by the interlaboratory study of §13, not yet run |
| Three engines running the full 192-query battery agree at Fleiss 0.086 on whether a citation happened, over 9,129 complete cells on 50 collection days; mean pairwise Cohen's kappa is 0.219 over 14 defined pairs | The three-way refusal taxonomy of §7.2. Tested by a human-labelled sample with annotator agreement and a confusion matrix, not yet built |
| The firm-by-engine interaction carries 39.33% of the variance in logit coverage, against 34.46% for the firm and 26.21% for the engine, over 62 entities by 6 engines | That the window delta is driven by how far into the response the first mention falls. Tested by manipulating response style and observing the delta move, not attempted |
| The matching rule names no fictitious entity spontaneously: 0 in 68,624 canonical observations, Wilson upper bound 0.0056% | That conformance levels on an attestation axis are the right axis. Tested by adoption, which has not happened |
| Which prompt was asked carries more of the latent variance than which engine answered it, at intraclass correlations of 0.4559 against 0.3492 over 38,195 responses on 96 prompts and 52 collection days, with the collection day at 0.0003 | That a battery published with its factorial invariants is a characterised battery. Tested by fitting the same model on a second battery balanced on the same four factors, which does not exist; those four factors move the between-prompt variance from 4.005 to 4.036 |

The defect this paper reports about itself was invisible to every control the pipeline ran, and §5.3 lists the controls that were green on the day the asymmetry was found. What no assertion asked was whether the string being read was the model's answer. Audits of commercial systems fail to reproduce for the same species of reason, traced to conditions the original studies had not fixed [5], and validity has to be argued rather than inherited from a passing suite [52, 49]. The transferable part is cheap: a variable whose maximum equals its minimum across 15,168 observations reports a boundary rather than a measurement, and that query costs seconds.

The window turned out to be the dominant parameter across the whole panel rather than a quirk of retrieval. Four parametric arms move by at least 30.73 percentage points and the single retrieval-augmented arm moves least, at 22.95, which inverts the architectural expectation that retrieval-augmented composition would suffer most, and §6.6 reports the test that rejects it. It also reverses a published reading: the 1.86% attributed to Gemini over 15,355 observations is a property of the aperture, since on the 768 observations that retained a whole response the same window gives 2.60% while the whole response gives 33.3%, rising to 65.10% over the 384 observations from the two of three days on which that arm returned full-length answers rather than answers capped at 216 characters. The gap between the two figures is definitional uncertainty in the sense of VIM 2.27 [7], so no sample size closes it and no better extractor reduces it. A vendor who reports a confidence interval derived from the observation count is reporting a term below the floor, and the dominant term never entered the budget.

Agreement between engines is partly an artefact of the instrument that measures it. On identical cells on 2026-09-08 across the four fully truncated arms, Fleiss on the binary outcome rises from 0.2371 at 200 characters to 0.4881 on the whole response over 192 cells, and the Claude to Gemini pair moves from 0.126 to 0.633. Doubling is the size of the correction on those cells, and the direction matters more than the magnitude: part of what reads as models disagreeing about a firm is one aperture applied to answers of very different lengths. The correction does not extend to every pair, since the four pairs containing the retrieval arm move the other way as prevalence approaches the ceiling where kappa loses discriminating power, so the harmonised figure is not uniformly higher and should not be presented as if it were.

Citation is a property of the firm-engine pair, and §9.2 puts the interaction above either main effect on the entity-by-engine grid, while the multilevel model on the same series puts the prompt above the engine on the response, at intraclass correlations of 0.4559 against 0.3492 over 38,195 responses. A measurement bought from one engine therefore estimates a quantity that does not transfer, and the effect is visible at the level of individual firms: of the twenty entities named by exactly one engine in five months, seventeen are named only by the retrieval-augmented arm, and they are the mid-cap and long-tail names. A firm in that position does not have a low rate on the other engines. It has no rate there, and a dashboard that pools the panel into one number will report the two cases identically. The query side behaves the same way: asked in Portuguese rather than English, five arms name fewer Brazilian entities and the retrieval arm names more, a within-pair spread of 17.03 points between the two extremes over 21,862 matched pairs (§9.4).

For anyone buying measurement, the consequences are specific and none of them requires adopting this protocol. A rate arrives with the window that produced it and the recall target that window meets, because 200 characters recovers 35.4% of first mentions across the panel, and between 7.8% and 70.2% by arm, over the 1,367 observations that name an entity (row 19 of Table 37). It arrives per engine, because the same cohort on the same days gives 1.91% over 9,455 replicate-reduced cells on one arm and 53.09% over 4,737 on another (`stats/S3-agreement.md`, Table S3.1c), and the two arms do not even answer the same battery: one receives all 192 queries and the other 96, as §9.5 and Appendix B record. The effective sample travels with it rather than the observation count, because the 68,624 observations of 192 prompts carry the statistical weight of 1,083 (Table 23). It arrives with the matching rule and its ablation, because removing the alias table alone moves the panel by 0.94 percentage points and one arm by 5.25 over the 2,225 observations of the ablation in §3.1. And it arrives with a note on what survives a change of vendor, which is the ranking inside a vertical rather than the level, at a median Kendall tau-b between engines of 0.52 in fintech and 0.58 in retail against 0.27 in health and 0.18 in technology, so even that property holds in two of the four markets measured (`stats/S3-agreement.md`, Table S3.3c).

One control in that list costs almost nothing. The decoy construction of §7.1 puts sixteen fictitious firms inside the same battery, on the same days, through the same adapters as the 111 real entities, and across 68,624 canonical observations no engine named one of them spontaneously at either window, which puts a 95% upper bound of 0.0056% on the rate at which the matching rule manufactures a cohort name out of ordinary prose. The floor is estimated from the run that produced the rate rather than from a separate calibration an adopter would have to trust transfers, and the bound is honest about where it is loose: the newest arm's 1,118 observations admit an upper bound of 0.342%, sixty times the panel figure. What the floor does not bound is a model's willingness to describe an invented firm when the name is handed to it, which is a different instrument and a different number.

What changes in reporting practice is the shape of the published object. A headline figure becomes a figure plus six declared values, an uncertainty budget that separates components estimated from repetition from components estimated from knowledge of the instrument, and a missingness ledger stating what was not collected. The cost of publishing that object is a page. The cost of not publishing it is the situation this paper documents inside its own instrument for four months, in which two figures that differ by tens of percentage points are both correct and no reader can tell why.

---

## 16. Conclusion

BRGEO-1 fixes six parameters, three conformance levels on an axis of attestation, a missingness ledger and an uncertainty budget, and states each requirement with a stable identifier and a failure mode. The parameters are the observation window, the cohort, the query battery, the engine panel with pinned model versions, the generation configuration and the entity matching rule. They are the description of the state of the phenomenon that the vocabulary of metrology requires before a quantity can be called a measurand [7], and a rate published without them names no measurand a second party can reproduce.

The empirical contribution is a five-month record of what happens when one of the six moves without being declared. On 2,225 observations matched within the response, reading to the end instead of stopping at character 200 raises the citation rate by 22.95 to 55.73 percentage points across five engines, with no observation losing its citation in any arm. The effect is not predictable from architectural class, the four parametric arms spanning the full range while the single retrieval-augmented arm moves least. It reverses one published reading, since an engine reported at 1.86% over 15,355 observations cites at 33.3% on the 768 of those observations whose whole response was retained. Beside that number sit the conditions under which it was produced: 37.4% calendar coverage over 139 days, a design effect of 63.3 at the prompt that cuts the effective sample to 1,083, a false-positive floor of zero spontaneous fictitious namings in 68,624 observations with a Wilson upper bound of 0.0056%, and a firm-by-engine interaction carrying 39.33% of the variance in coverage.

The specification's principal gap is that conformance remains self-declared. Two artefacts would close it and neither exists: a conformance test suite of reference responses with expected figures under declared parameters, and an interlaboratory study in the sense of ISO 5725-2 in which independent implementations process the same stored responses and the discrepancy is decomposed into repeatability and between-implementation components [81]. Until the second runs, the central proposition of this paper, that declaring the six parameters produces comparability, is a design argument with no measured evidence in its favour.

The gap has a precondition that this instrument does not yet meet. An interlaboratory exercise needs shared items, and full-response retention was deployed on 2026-08-31 with the first retained rows falling on 2026-09-06, which leaves the 2,225 canonical observations of 2026-09-06 to 2026-09-08 available to distribute against 68,624 collected. The confirmatory window is defined in collected days rather than calendar days and stood at 56 of 90 on 2026-09-11, with a projected close on 2026-10-15. Retention from the first observation is therefore the requirement an adopter should implement before any other, because it is the only one in the specification that cannot be satisfied retroactively [53]. Everything else in this record was repaired after it was found. The four months of responses that were never stored were not.

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

**Table 39.** Cohort composition by vertical, class and tier. Fixed 2026-04-23, 127 entities; denominator for the tier columns is the Brazilian firms of that vertical.

| Vertical | Brazilian firms | Head | Torso | Long tail | Anchors | Decoys | Total |
|---|---:|---:|---:|---:|---:|---:|---:|
| Fintech | 19 | 10 | 4 | 5 | 8 | 4 | 31 |
| Retail | 20 | 8 | 6 | 6 | 8 | 4 | 32 |
| Health | 20 | 9 | 6 | 5 | 8 | 4 | 32 |
| Technology | 20 | 7 | 6 | 7 | 8 | 4 | 32 |
| **Cohort** | **79** | **34** | **22** | **23** | **32** | **16** | **127** |

Of the 79 Brazilian firms, 78 are annotated active and one is in judicial recovery. Founding years run from 1895 to 2019, with 21 of the 79 founded in 2010 or later. That stratum was designed to probe the awareness gap of models whose pre-training predates the firm, and on this cohort it cannot: the most recently founded member dates from 2019 and every pinned engine version has a later cutoff, so the indicator has no cases and was not fitted (§9.6). Nine federative units are represented: São Paulo 59, Rio de Janeiro 6, Minas Gerais 3, Santa Catarina 3, Paraná 2, Rio Grande do Sul 2, Ceará 2, Espírito Santo 1 and Rio Grande do Norte 1.

**Table 40.** The 79 Brazilian firms with tier, legal status, founding year and federative unit. Source `src/config_v2.py`, fixed 2026-04-23.

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

Four names in Table 40 carry a canonical long form chosen at construction to avoid a lexical collision: Stone Co, Banco Neon, EMS Pharma and Linx S.A. The guard was not applied to every surface, and §4.5 reports the two cases it missed.

**Table 41.** The 32 international anchors, present in every vertical so that a Brazilian result can be checked against a non-Brazilian baseline inside the same instrument. All are head tier and active. Source `src/config_v2.py`, fixed 2026-04-23.

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

**Table 42.** The 16 fictitious calibration decoys, four per vertical, verified as non-existent before collection. They travel inside the same battery, on the same days, through the same adapters as the 111 real entities, which is what makes the false-positive floor of §7.1 an estimate from the run that produced the rate. Source `src/config_v2.FICTITIOUS_DECOYS_V2`.

| Vertical | Decoys |
|---|---|
| Fintech | Banco Floresta Digital; FinPay Solutions; Banco Aurora; PagFast |
| Retail | MegaStore Brasil; ShopNova Digital; MercadoPlus Brasil; VareJo Express |
| Health | HealthTech Brasil; Clínica Horizonte Digital; SaúdeAgora; ClínicaVita |
| Technology | TechNova Solutions; DataBridge Brasil; TechBridge BR; DataCore Brasil |

---

## Appendix B. The factorial design of the query battery

The 192 canonical queries are generated from five declared axes rather than curated, so the balance is a property of the construction. An adopter who changes a level changes the battery identifier and therefore the value of P3, which is what a Closed division fixes and an Open division documents.

**Table 43.** The five axes of the canonical battery and their realised counts. Battery fixed 2026-04-23, 192 canonical queries; the count column is the number of queries carrying each level, computed from `src/config_v2.build_canonical_battery`.

| Axis | Levels | Queries per level |
|---|---|---:|
| Vertical | fintech, retail, health, technology | 48 |
| Semantic category | descoberta, comparativo, confianca, experiencia, mercado, inovacao | 32 |
| Language | pt, en | 96 |
| Query type | directive, exploratory | 96 |
| Temporal frame | atemporal, "em 2026" | 96 |

The product of the five axes is 4 × 6 × 2 × 2 × 2 = 192 with no cell repeated and none empty. Two invariants are checked by the module's own validators, the 96-against-96 language split and the 96-against-96 query-type split. The third, that every English query names Brazil or uses the adjective Brazilian, is asserted in `tests/test_config_v2.py` and holds on all 96 English queries; it is what prevents drift toward North American and European brands when the language changes.

**Table 44.** Vertical labels substituted into the templates, which is the only point at which the vertical enters the query text. Source `src/config_v2.build_query`.

| Vertical | Label, Portuguese | Label, English |
|---|---|---|
| fintech | fintechs e bancos digitais | fintechs and digital banks |
| retail | varejo e e-commerce | retail and e-commerce |
| health | saúde e farmacêutica | healthcare and pharmaceuticals |
| technology | tecnologia e TI | technology and IT |

**Table 45.** The 24 canonical templates, one per semantic category by query type by language. `<V-pt>` and `<V-en>` take the labels of Table 44. The temporal axis appends " em 2026" to the Portuguese form and " in 2026" to the English form, giving 24 × 4 verticals × 2 temporal frames = 192 queries. Battery fixed 2026-04-23.

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

Two facts about the realised battery belong here rather than in a caption, because a reader comparing Table 43 with the results of §9 will otherwise infer them wrongly. Provider routing sends one arm 96 of the 192 canonical queries on cost grounds, and the half it runs is the discovery-shaped half, so three of the six semantic categories carry n = 0 on that arm and its category column is not comparable with the parametric arms. The second fact is that balance was not achieved at first: the battery ran at 85/15 on query type for the first week, because the configuration read the key `type` while the v2 battery writes `query_type`, and 4,284 rows were re-annotated on 2026-04-30 to restore 4,287 directive against 4,284 exploratory (§5.3).

**Table 46.** The adversarial stratum, which is a separate instrument and shares no query with the canonical battery. Each template forces the model to speak about a named fictitious entity. 4 verticals × 4 decoys × 2 languages × 2 templates = 64 distinct probe queries; 17,919 probe observations in the series 2026-04-23 to 2026-09-08. Source `src/config_v2.build_adversarial_queries`.

| Language | Template | Temporal frame |
|---|---|---|
| pt | O que você sabe sobre `<DECOY>`, `<label-pt>`? | atemporal |
| pt | Quais os principais produtos da `<DECOY>` em 2026? | em 2026 |
| en | What do you know about `<DECOY>`, a `<label-en>`? | atemporal |
| en | What are the main products of `<DECOY>` in 2026? | em 2026 |

The vertical labels used by the probe templates differ from those of Table 44 because the probe names a class of firm rather than a market: `fintech ou banco digital brasileiro` and `Brazilian fintech or digital bank`; `varejo ou e-commerce brasileiro` and `Brazilian retail or e-commerce company`; `operadora de saúde ou farmacêutica brasileira` and `Brazilian healthcare or pharmaceutical company`; `empresa de tecnologia brasileira` and `Brazilian technology company`. Probe rows are marked `is_probe = 1` and `adversarial_framing = 1` and are excluded from every canonical figure in this paper by `COALESCE(is_probe,0)=0`.

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

**The day rule is declared here because two counts circulate.** A day in this appendix and in Tables 47 to F13 is the UTC date of `citations.timestamp`, which gives 53 days with data. The temporal analysis of §9 re-dates each row to America/São_Paulo, because the evening collection round crosses midnight in UTC, and reports 52. The difference is one day and it is a difference of convention, not of data. Every figure in this paper states which count it uses.

**Table 47.** Coverage by month over the analysed span. Series 2026-04-23 to 2026-09-08, 68,624 canonical observations; denominator is calendar days inside the span.

| Month | Days with data | Canonical observations | Calendar days in span | Days with no data |
|---|---:|---:|---:|---:|
| 2026-04 | 8 | 10,930 | 8 | 0 |
| 2026-05 | 23 | 25,899 | 31 | 8 |
| 2026-06 | 9 | 13,624 | 30 | 21 |
| 2026-07 | 0 | 0 | 31 | 31 |
| 2026-08 | 10 | 15,946 | 31 | 21 |
| 2026-09 | 3 | 2,225 | 8 | 5 |
| **Series** | **53** | **68,624** | **139** | **86** |

**Table 48.** Contiguous blocks with no observation on any arm, with the cause on record. Series 2026-04-23 to 2026-09-08; the blocks sum to the 86 days with no data in Table 47.

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

**Table 49.** The 19 partial days among the 53 with data, under the derived definition: a day is partial when an arm active in the surrounding period delivers fewer distinct canonical queries than its own battery size, or produces no row at all. Battery size is inferred from the data as the largest distinct-query count the arm ever reached in one day: 192 for every parametric arm and 96 for the retrieval-augmented arm.

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

**Corrections to the repository ledger.** Five entries in the project's own itemised ledger do not survive comparison with the database and are corrected here rather than left for a reader to discover. The isolated one-day balance gaps recorded for 2026-07-25 and 2026-08-06 fall inside the 59-day block of Table 48, so they describe attempted runs rather than isolated gaps in a period that was otherwise collecting; the canonical database holds no July observation at all. The two-day gap recorded for 2026-08-09 and 2026-08-10 is one day in the data, since 2026-08-10 carries observations. No day-level cause is recorded anywhere for 2026-05-19 to 2026-07-24, which is why fourteen rows of Table 49 and one row of Table 48 read "no cause recorded" instead of carrying a reconstruction. Two empirically incomplete days, 2026-06-05 and 2026-08-13, appear in no ledger, and three days the repository documentation calls partial, 2026-04-24, 2026-05-04 and 2026-05-18, are complete in cell terms, because the failures they describe consumed rows rather than cells. Two documents written on 2026-08-31 report 49 days with 296 aborted runs and 50 days with 324; neither is used here, and the figures above come from one snapshot whose timestamp is declared in the Data availability statement.

**The two regimes for a partial day.** Until 2026-09-08 the acquisition rule was that an absent day beats a partial day, enforced by a preflight that barred collection whenever a mandatory provider had no balance, which is how the 6-day, 7-day and 5-day blocks of Table 48 arose. From 2026-09-09 the default reverses: a provider without credit is dropped from the mandatory list for that run, the day is written to the registry with the missing arms, the provider's verbatim error and the run URL, and collection proceeds if a minimum number of arms remain. Every day in this appendix belongs to the first regime and is complete or absent. Days from 2026-09-09 may be partial by design, and three were recorded within two days of the change.

---

## Appendix E. Reproduction

Every table and every figure in this paper is regenerated by one command against the read-only database snapshot declared in the Data availability statement, the index of §10 included since 2026-09-11. Nothing in the tables is typed by hand: each figure is interpolated from a query result into the document by the script that produced it, and `NUMBERS.md` carries the statement or function call behind every value together with the result obtained. A figure present in a table and absent from `NUMBERS.md` came from a measurement nobody can repeat.

**Table 50.** Commands that regenerate each artefact. Paths are relative to the repository root; `J` abbreviates `docs/research/methods-paper/journal-v2`. Runtimes are on the machine of record.

| Artefact | Command | Output |
|---|---|---|
| Tables 1 to 12 and the verifier document | `cd J/tables && python build_tables.py` | Rewrites `TABLES.md` and `NUMBERS.md` |
| Table 13, with its two identity checks | `cd J/tables && python window_analysis.py` | Table 13 to stdout; non-zero exit if either check fails |
| Multilevel model, variance decomposition and paired language effect (§9.1, §9.2, §9.4, §14) | `cd J/stats && python s1_multilevel.py` | `s1_results.json` and `S1-multilevel.md`; about 27 minutes. Tables 24, E13 and E14 and rows 23 to 25 of Table 37 draw on it |
| Temporal analysis, change points, autocorrelation, design effects (§9, §14) | `cd J/stats && python s2_temporal.py --db ../../../../../data/papers.db --repo ../../../../.. --perm 999` | `s2_results.json` and 17 CSV files under `stats/data/`; about 3 minutes |
| Inter-engine agreement, latent structure, firm against engine (§9, §15) | `cd J/stats && python s3_agreement.py --boot 2000 --nullsim 2000` | Markdown to stdout; 107 seconds cold, 30 with `--cache <path.pkl>` |
| Concentration, tail, never-named entities, anchors (§9) | `cd J/stats && python s4_concentration.py --boot 2000 --gof 1000` | `data/s4_numbers.json`, `s4_lorenz_global.csv`, `s4_lorenz_by_vertical.csv`, `s4_rank_size.csv` |
| Window curve, recovery curve, P6 ablation, reliability (§6, §14) | `cd J/stats && python s5_window_validity.py` | 19 CSV files and `s5_window_validity.json`; about 4 minutes. `--quick` runs 1,000 bootstrap replicates. Exit status 0 only when both identity checks pass |
| Figure 2, window and recovery curves, numbered 1 in the assembled manuscript | `cd J/build && python make_figures.py` | `build/figures/fig1-window-curve.png`, from `stats/data/s5_window_curve_by_engine.csv` and `s5_mention_recovery_curve.csv` |
| Figure 3, Lorenz curve of mentions, numbered 2 | same command | `build/figures/fig2-lorenz.png`, from `stats/data/s4_lorenz_global.csv` |
| Collected days and gaps, produced but carried by no numbered caption | same command | `build/figures/fig3-coverage.png`, from `stats/data/s2_daily_engine.csv` |
| Reporting index, its three components and the aggregation comparison (§10) | `cd J/stats && python s6_index.py` | 7 CSV files under `stats/data/` with the `s6_` prefix, covering both declared panel rules; prints the re-extraction identity check and exits non-zero if it fails; about 25 seconds |
| Reference implementation of the index, for comparison against §10 | `python scripts/brgeo1_index.py --vertical all --compare` | Per-vertical table to stdout. It selects the panel by the 14-day recency rule of commit `51159fd` and reports coverage over a numerator that is not restricted to the panel, which is why §10 is computed by `s6_index.py` instead |
| Assembled manuscript and assembly report | `cd J/build && python assemble.py` | `MANUSCRIPT-JOURNAL.md` and `ASSEMBLY-REPORT.md` |

**Order matters in one place.** The three figures read CSV files written by the statistical scripts, so `s2_temporal.py`, `s4_concentration.py` and `s5_window_validity.py` run before `make_figures.py`. Everything else is independent.

**Environment and determinism.** Python 3.12.10 with numpy 2.4.3, pandas 3.0.1, scipy 1.17.1, statsmodels 0.14.6, patsy 1.0.2 and matplotlib for the figures; `ruptures` 1.1.10 is optional and only supplies the corroborating change-point detector, which reports NOT RUN in its absence without affecting the primary detector. The random seed is fixed at 20260911 throughout. At that seed and the bootstrap and permutation counts given in Table 50, permutation p-values, bootstrap intervals and parametric marginal effects reproduce bit for bit. Every script opens the database with `file:data/papers.db?mode=ro` and writes nothing to it.

**What reproduction cannot reach.** These commands recompute every published figure from the stored observations. They do not recollect the observations, and they cannot: hosted models do not reproduce their outputs exactly at temperature zero [91, 92], and for the 66,399 canonical observations collected before 2026-08-31 the text beyond character 200 was never written to disk, so no third party can re-extract them at any other window. Reproduction of the analysis is available to anyone. Reproduction of the measurement begins with the first retained rows, of 2026-09-06, and covers the 2,225 observations collected through 2026-09-08 [53].

---

## References

[1] Grossman, R., Liu, S., Chen, M.K., Smith, M., Borcea, C., Chen, Y., 2026. How Generative AI Disrupts Search: An Empirical Study of Google Search, Gemini, and AI Overviews, in: Proceedings of the 49th International ACM SIGIR Conference on Research and Development in Information Retrieval (SIGIR 2026). arXiv:2604.27790.

[2] Khosravi, M., Yoganarasimhan, H., 2026. Impact of AI Search Summaries on Website Traffic: Evidence from Google AI Overviews and Wikipedia. arXiv:2602.18455.

[3] Watanabe, K., Nakayashiki, K., 2026. Disentangling Answer Engine Optimization from Platform Growth: A Log-Based Natural Experiment on ChatGPT Referral Traffic. arXiv:2606.04362.

[4] Wen, Y., Zhang, N., Yuan, H., Chen, X., Zhang, H., Guo, H., 2026. Position: Generative Engine Optimization Creates Underexamined Risks, Governance Must Target Concentration, Disclosure, and Academic Blind Spots, in: Proceedings of the International Conference on Machine Learning (ICML 2026), Position Paper Track. arXiv:2606.12439.

[5] Mosnar, M., Skurla, A., Pecher, B., Tibensky, M., Jakubcik, J., Bindas, A., Sakalik, P., Srba, I., 2025. Revisiting Algorithmic Audits of TikTok: Poor Reproducibility and Short-Term Validity of Findings, in: Proceedings of the International ACM SIGIR Conference on Research and Development in Information Retrieval (SIGIR 2025). arXiv:2504.18140.

[6] Lurie, E., Encarnación, R., Friedler, S.A., Metaxa, D., 2026. The Beginning of ChatGPT Ads, in: Proceedings of the AAAI/ACM Conference on AI, Ethics, and Society (AIES 2026). arXiv:2608.05008.

[7] JCGM 200:2012, International Vocabulary of Metrology — Basic and general concepts and associated terms (VIM), 3rd ed. BIPM, 2012. *Entry from R5 §7; clauses 2.3, 2.20, 2.24, 2.27 and 2.41 confirmed in the official document on 2026-09-11.*

[8] JCGM 100:2008. Evaluation of Measurement Data: Guide to the Expression of Uncertainty in Measurement (GUM). Joint Committee for Guides in Metrology, Bureau International des Poids et Mesures, Sevres.

[9] Borsboom, D., Mellenbergh, G.J., van Heerden, J., 2004. The Concept of Validity. Psychological Review 111 (4), 1061–1071. https://doi.org/10.1037/0033-295X.111.4.1061

[10] Jacobs, A.Z., Wallach, H., 2021. Measurement and Fairness, in: Proceedings of the 2021 ACM Conference on Fairness, Accountability, and Transparency, pp. 375–385. https://doi.org/10.1145/3442188.3445901

[11] Saisana, M., Saltelli, A., Tarantola, S., 2005. Uncertainty and Sensitivity Analysis Techniques as Tools for the Quality Assessment of Composite Indicators. Journal of the Royal Statistical Society Series A: Statistics in Society 168 (2), 307–323. https://doi.org/10.1111/j.1467-985X.2005.00350.x

[12] Aggarwal, P., Murahari, V., Rajpurohit, T., Kalyan, A., Narasimhan, K., Deshpande, A., 2024. GEO: Generative Engine Optimization, in: Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining, pp. 5–16. https://doi.org/10.1145/3637528.3671900

[13] Bagga, P.S., Farias, V.F., Korkotashvili, T., Peng, T., Wu, Y., 2025. E-GEO: A Testbed for Generative Engine Optimization in E-Commerce. arXiv:2511.20867.

[14] Yu, J., Yang, M., Ding, Y., Sato, H., 2026. Structural Feature Engineering for Generative Engine Optimization: How Content Structure Shapes Citation Behavior. arXiv:2603.29979.

[15] Wu, Y., Zhong, S., Kim, Y., Xiong, C., 2025. What Generative Search Engines Like and How to Optimize Web Content Cooperatively. arXiv:2510.11438.

[16] Nimase, O., Chen, Z., Qi, G., Zhao, Y., Hu, X., 2026. GEO-Bench: Benchmarking Ranking Manipulation in Generative Engine Optimization. arXiv:2605.29107.

[17] Sielinski, R., 2026. Quantifying Uncertainty in AI Visibility: A Statistical Framework for Generative Search Measurement. arXiv:2603.08924.

[18] Sielinski, R., 2026. From Stochastic to Stable: Rank Stability and Structural Sufficiency in AI Visibility Measurement. arXiv:2607.10341.

[19] Schulte, J., Bleeker, M., Kaufmann, P., 2026. Don't Measure Once: Measuring Visibility in AI Search (GEO). arXiv:2604.07585.

[20] Zhang, K., He, X., Yao, J., 2026. From Citation Selection to Citation Absorption: A Measurement Framework for Generative Engine Optimization Across AI Search Platforms. arXiv:2604.25707.

[21] Varga, Z., 2026. Per-Entity Bias Mapping for AI Visibility: Why Brand Mentions Require Entity-Specific Calibration. arXiv:2606.21595.

[22] Kumar, P., 2026. Generative Engine Optimization at Scale: Measuring Brand Visibility Across AI Search Engines. arXiv:2606.20065.

[23] Martinez, O., 2026. Optimizing Visibility in Generative Engines: A Critical Survey of Generative Engine Optimization (2023–2026). arXiv:2607.14035.

[24] Żatuchin, D., 2026. Where Does the Noise Come From? A Variance-Components Decomposition of Non-Determinism in LLM Brand Answers. arXiv:2607.13304.

[25] Huang, J., Situ, R., Ye, R., 2026. Cultural Encoding in Large Language Models: The Existence Gap in AI-Mediated Brand Discovery. arXiv:2601.00869.

[26] Żatuchin, D., 2026. The Language Blind Spot: How Query Language and Brand Recognition Tier Shape AI-Constructed Brand Reputation Across Twelve European Languages. arXiv:2606.23165.

[27] Chu, X., Hou, Y., 2026. Incumbent Advantage: Brand Bias and Cognitive Manipulation Dynamics in LLM Recommendation Systems. arXiv:2606.17443.

[28] Żatuchin, D., 2026. The Dice Roll Method: A Standardized Protocol for Repeated-Query Auditing of Large Language Model Brand Recommendations. arXiv:2609.04047.

[29] Rashkin, H., Nikolaev, V., Lamm, M., Aroyo, L., Collins, M., Das, D., Petrov, S., Tomar, G.S., Turc, I., Reitter, D., 2023. Measuring Attribution in Natural Language Generation Models. Computational Linguistics 49 (4), 777–840. https://doi.org/10.1162/coli_a_00486

[30] Liu, N.F., Zhang, T., Liang, P., 2023. Evaluating Verifiability in Generative Search Engines, in: Findings of the Association for Computational Linguistics: EMNLP 2023, pp. 7001–7025. https://doi.org/10.18653/v1/2023.findings-emnlp.467

[31] Gao, T., Yen, H., Yu, J., Chen, D., 2023. Enabling Large Language Models to Generate Text with Citations, in: Proceedings of EMNLP 2023, pp. 6465–6488. https://doi.org/10.18653/v1/2023.emnlp-main.398

[32] Venkit, P.N., Laban, P., Zhou, Y., Mao, Y., Wu, C.-S., 2024. Search Engines in an AI Era: The False Promise of Factual and Verifiable Source-Cited Responses. arXiv:2410.22349.

[33] Venkit, P.N., Laban, P., Zhou, Y., Huang, K.-H., Mao, Y., Wu, C.-S., 2025. DeepTRACE: Auditing Deep Research AI Systems for Tracking Reliability Across Citations and Evidence. arXiv:2509.04499.

[34] Xu, H., Iqbal, U., Montgomery, J.M., 2026. Measuring Google AI Overviews: Activation, Source Quality, Claim Fidelity, and Publisher Impact. arXiv:2605.14021.

[35] Alaofi, M., Arabzadeh, N., Clarke, C.L.A., Sanderson, M., 2024. Generative Information Retrieval Evaluation, in: Shah, C., White, R. (Eds.), Information Access in the Era of Generative AI. Springer. arXiv:2404.08137.

[36] Jung, H., Gonen, H., 2026. PhantomBench: Benchmarking the Non-existential Threat of Language Models. arXiv:2606.11105.

[37] Bang, Y., Ji, Z., Schelten, A., Hartshorn, A., Fowler, T., Zhang, C., Cancedda, N., Fung, P., 2025. HalluLens: LLM Hallucination Benchmark, in: Proceedings of ACL 2025 (Volume 1: Long Papers), pp. 24128–24156. https://doi.org/10.18653/v1/2025.acl-long.1176

[38] Kirichenko, P., Ibrahim, M., Chaudhuri, K., Bell, S.J., 2025. AbstentionBench: Reasoning LLMs Fail on Unanswerable Questions. arXiv:2506.09038.

[39] Pan, W., Xu, J., Chen, Q., Dong, J., Qin, L., Li, X., Yu, H., Jia, X., 2026. Can LLMs Refuse Questions They Do Not Know? Measuring Knowledge-Aware Refusal in Factual Tasks, in: Proceedings of the International Conference on Learning Representations (ICLR 2026). arXiv:2510.01782.

[40] Wen, B., Yao, J., Feng, S., Xu, C., Tsvetkov, Y., Howe, B., et al., 2025. Know Your Limits: A Survey of Abstention in Large Language Models. Transactions of the Association for Computational Linguistics 13, 529–556. https://doi.org/10.1162/tacl_a_00754

[41] Zhao, W., Goyal, T., Chiu, Y.Y., Jiang, L., Newman, B., Ravichander, A., et al., 2024. WildHallucinations: Evaluating Long-Form Factuality in LLMs with Real-World Entity Queries. arXiv:2407.17468.

[42] Zhao, Z., Wang, Y., Stuart, T., De Vaan, M., Ginsparg, P., Yin, Y., 2026. LLM Hallucinations in the Wild: Large-Scale Evidence from Non-Existent Citations. arXiv:2605.07723.

[43] Agrawal, A., Suzgun, M., Mackey, L., Kalai, A.T., 2024. Do Language Models Know When They're Hallucinating References?, in: Findings of the Association for Computational Linguistics: EACL 2024, pp. 912–928. https://doi.org/10.18653/v1/2024.findings-eacl.62

[44] Ji, Z., Lee, N., Frieske, R., Yu, T., Su, D., Xu, Y., Ishii, E., Bang, Y., Madotto, A., Fung, P., 2023. Survey of Hallucination in Natural Language Generation. ACM Computing Surveys 55 (12), 1–38. https://doi.org/10.1145/3571730

[45] Huang, L., Yu, W., Ma, W., Zhong, W., Feng, Z., Wang, H., Chen, Q., Peng, W., Feng, X., Qin, B., Liu, T., 2025. A Survey on Hallucination in Large Language Models: Principles, Taxonomy, Challenges, and Open Questions. ACM Transactions on Information Systems 43 (2), 1–55. https://doi.org/10.1145/3703155

[46] Raji, I.D., Bender, E.M., Paullada, A., Denton, E., Hanna, A., 2021. AI and the Everything in the Whole Wide World Benchmark, in: Proceedings of the NeurIPS Track on Datasets and Benchmarks 1. arXiv:2111.15366.

[47] Bowman, S.R., Dahl, G., 2021. What Will it Take to Fix Benchmarking in Natural Language Understanding?, in: Proceedings of NAACL-HLT 2021, pp. 4843–4855. https://doi.org/10.18653/v1/2021.naacl-main.385

[48] Reiter, E., 2018. A Structured Review of the Validity of BLEU. Computational Linguistics 44 (3), 393–401. https://doi.org/10.1162/coli_a_00322

[49] Bean, A.M., Kearns, R.O., Romanou, A., Hafner, F.S., Mayne, H., et al., 2025. Measuring what Matters: Construct Validity in Large Language Model Benchmarks, in: Proceedings of the NeurIPS 2025 Track on Datasets and Benchmarks. arXiv:2511.04703.

[50] Hochlehnert, A., Bhatnagar, H., Udandarao, V., Albanie, S., Prabhu, A., Bethge, M., 2025. A Sober Look at Progress in Language Model Reasoning: Pitfalls and Paths to Reproducibility, in: Proceedings of COLM 2025. arXiv:2504.07086.

[51] Encarnación, R., Behzad, T., Lurie, E., Metaxa, D., 2026. What Current AI Benchmarks Leave Unmeasured: Modality, Search, Citations, and Implications (for Safety Evaluations). arXiv:2608.06202.

[52] Salaudeen, O., Reuel, A., Ahmed, A., Bedi, S., Robertson, Z., Sundar, S., et al., 2025. Measurement to Meaning: A Validity-Centered Framework for AI Evaluation. arXiv:2505.10573.

[53] Jiang, H., Zhang, S., Zhu, D., Bai, Y., Truong, S.T., Yi, X., Koyejo, S., Xie, X., Xiao, Z., 2026. AI Evaluation Should Require Standardized Item-Level Data Releases. arXiv:2604.03244.

[54] Nardo, M., Saisana, M., Saltelli, A., Tarantola, S., Hoffmann, A., Giovannini, E., 2008. Handbook on Constructing Composite Indicators: Methodology and User Guide. OECD Publishing, Paris. https://doi.org/10.1787/9789264043466-en

[55] Paruolo, P., Saisana, M., Saltelli, A., 2013. Ratings and Rankings: Voodoo or Science? Journal of the Royal Statistical Society Series A: Statistics in Society 176 (3), 609–634. https://doi.org/10.1111/j.1467-985X.2012.01059.x

[56] Greco, S., Ishizaka, A., Tasiou, M., Torrisi, G., 2019. On the Methodological Framework of Composite Indices: A Review of the Issues of Weighting, Aggregation and Robustness. Social Indicators Research 141 (1), 61–94. https://doi.org/10.1007/s11205-017-1832-9

[57] Saltelli, A., 2007. Composite Indicators between Analysis and Advocacy. Social Indicators Research 81 (1), 65–77. https://doi.org/10.1007/s11205-006-0024-9

[58] Żatuchin, D., 2026. Who Owns the AI Recommendation? A Multi-Industry Empirical Map of Brand Category Ownership Across Large Language Models. arXiv:2606.23057.

[59] Breuer, T., Keller, J., Schaer, P., 2022. ir_metadata: An Extensible Metadata Schema for IR Experiments, in: Proceedings of SIGIR 2022, pp. 3078–3089. https://doi.org/10.1145/3477495.3531738

[60] Ferro, N., Fuhr, N., Järvelin, K., Kando, N., Lippold, M., Zobel, J., 2016. Increasing Reproducibility in IR: Findings from the Dagstuhl Seminar on Reproducibility of Data-Oriented Experiments in e-Science. ACM SIGIR Forum 50 (1), 68–82. https://doi.org/10.1145/2964797.2964808

[61] Aloqalaa, M., Soiland-Reyes, S., Goble, C., 2026. PRIMAD-LID: A Developed Framework for Computational Reproducibility. arXiv:2601.02349.

[62] Breuer, T., Ferro, N., Maistro, M., Schaer, P., 2021. repro_eval: A Python Interface to Reproducibility Measures of System-Oriented IR Experiments, in: Advances in Information Retrieval (ECIR 2021), Lecture Notes in Computer Science, pp. 481–486. https://doi.org/10.1007/978-3-030-72240-1_51

[63] Ghosh, A., Reuel, A., Chim, J., Kennedy, W.M., Yadav, S., Mickel, J., et al., 2026. Evaluation Cards: An Interpretive Layer for AI Evaluation Reporting. arXiv:2606.09809.

[64] Dhar, R., Sanchez Villegas, D., Karamolegkou, A., Schiavone, A., Yuan, Y., Chen, X., et al., 2025. EvalCards: A Framework for Standardized Evaluation Reporting. arXiv:2511.21695.

[65] Mitchell, M., Wu, S., Zaldivar, A., Barnes, P., Vasserman, L., Hutchinson, B., Spitzer, E., Raji, I.D., Gebru, T., 2019. Model Cards for Model Reporting, in: Proceedings of the Conference on Fairness, Accountability, and Transparency, pp. 220–229. https://doi.org/10.1145/3287560.3287596

[66] Gebru, T., Morgenstern, J., Vecchione, B., Vaughan, J.W., Wallach, H., Daumé III, H., Crawford, K., 2021. Datasheets for Datasets. Communications of the ACM 64 (12), 86–92. https://doi.org/10.1145/3458723

[67] Metaxa, D., Park, J.S., Robertson, R.E., Karahalios, K., Wilson, C., Hancock, J.T., Sandvig, C., 2021. Auditing Algorithms: Understanding Algorithmic Systems from the Outside In. Foundations and Trends in Human-Computer Interaction 14 (4), 272–344. https://doi.org/10.1561/1100000083

[68] Morosini, A., Cen, S.H., Ilyas, A., Driss, H., Mądry, A., Podimata, C., 2026. Using AI Agents to Automate Black-Box Audits of Personalization Algorithms at Scale. arXiv:2606.30801.

[69] Hu, D., Baumann, J., Urman, A., Lichtenegger, E., Forsberg, R., Hannak, A., et al., 2026. Auditing Google's AI Overviews and Featured Snippets: A Case Study on Baby Care and Pregnancy, in: Proceedings of the International AAAI Conference on Web and Social Media (ICWSM 2026). arXiv:2511.12920.

[70] Liang, P., Bommasani, R., Lee, T., Tsipras, D., Soylu, D., Yasunaga, M., et al., 2023. Holistic Evaluation of Language Models. Transactions on Machine Learning Research. arXiv:2211.09110.

[71] Muennighoff, N., Tazi, N., Magne, L., Reimers, N., 2023. MTEB: Massive Text Embedding Benchmark, in: Proceedings of EACL 2023, pp. 2014–2037. https://doi.org/10.18653/v1/2023.eacl-main.148

[72] Thakur, N., Reimers, N., Rücklé, A., Srivastava, A., Gurevych, I., 2021. BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models, in: Proceedings of the NeurIPS Track on Datasets and Benchmarks 1. arXiv:2104.08663.

[73] Enevoldsen, K., Chung, I., Kerboua, I., Kardos, M., Mathur, A., Stap, D., et al., 2025. MMTEB: Massive Multilingual Text Embedding Benchmark, in: Proceedings of ICLR 2025. arXiv:2502.13595.

[74] Craswell, N., Mitra, B., Yilmaz, E., Campos, D., Voorhees, E.M., 2020. Overview of the TREC 2019 Deep Learning Track. arXiv:2003.07820.

[75] Voorhees, E.M., 2000. Variations in relevance judgments and the measurement of retrieval effectiveness. Information Processing & Management 36 (5), 697–716. https://doi.org/10.1016/S0306-4573(00)00010-8

[76] Bailey, P., Moffat, A., Scholer, F., Thomas, P., 2016. UQV100: A Test Collection with Query Variability, in: Proceedings of SIGIR 2016, pp. 725–728. https://doi.org/10.1145/2911451.2914671

[77] Ferro, N., Kelly, D., 2018. SIGIR Initiative to Implement ACM Artifact Review and Badging. ACM SIGIR Forum 52 (1), 4–10. https://doi.org/10.1145/3274784.3274786

[78] Bradner, S., 1997. Key words for use in RFCs to Indicate Requirement Levels. RFC 2119, BCP 14, Internet Engineering Task Force. https://doi.org/10.17487/RFC2119

[79] Leiba, B., 2017. Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words. RFC 8174, BCP 14, Internet Engineering Task Force. https://doi.org/10.17487/RFC8174

[80] ISO/IEC 17000:2020. Conformity Assessment: Vocabulary and General Principles. International Organization for Standardization, Geneva.

[81] ISO 5725-2:1994, Accuracy (trueness and precision) of measurement methods and results — Part 2: Basic method for the determination of repeatability and reproducibility of a standard measurement method. *Entry from R5 §7; cited at document level, clause numbers not opened.*

[82] Adel, T., Bilson, S., Levene, M., Thompson, A., 2024. Trustworthy Artificial Intelligence in the Context of Metrology, in: Ferreira, M.I.A. (Ed.), Producing Artificial Intelligent Systems: The Roles of Benchmarking, Standardisation and Certification, Studies in Computational Intelligence. Springer. arXiv:2406.10117.

[83] Liu, N.F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F., Liang, P., 2024. Lost in the Middle: How Language Models Use Long Contexts. Transactions of the Association for Computational Linguistics 12, 157–173. https://doi.org/10.1162/tacl_a_00638

[84] Guo, X., Vosoughi, S., 2024. Serial Position Effects of Large Language Models. arXiv:2406.15981.

[85] Menschikov, M., Kharitonov, A., Kotyga, M., Porvatov, V., Zhukovskaya, A., Kagramanyan, D., Shvetsov, E., Burnaev, E., 2025. Beyond Early-Token Bias: Model-Specific and Language-Specific Position Effects in Multilingual LLMs. arXiv:2505.16134.

[86] Hou, Y., Zhang, J., Lin, Z., Lu, H., Xie, R., McAuley, J., Zhao, W.X., 2024. Large Language Models Are Zero-Shot Rankers for Recommender Systems, in: Advances in Information Retrieval (ECIR 2024), Lecture Notes in Computer Science, pp. 364–381. https://doi.org/10.1007/978-3-031-56060-6_24

[87] Bito, E., Ren, Y., He, E., 2025. Evaluating Position Bias in Large Language Model Recommendations. arXiv:2508.02020.

[88] Bito, E., Ren, Y., He, E., 2026. Position Bias Undermines Preference Consistency in Listwise LLM-Based Reranking, in: Proceedings of the ACM Conference on Recommender Systems (RecSys 2026). arXiv:2608.03091.

[89] Wadi, D., Ma, Y., 2026. Does Rank Still Matter? Position Bias When AI Agents Shop on Our Behalf. arXiv:2608.22697.

[90] Chen, L., Zaharia, M., Zou, J., 2024. How Is ChatGPT's Behavior Changing Over Time? Harvard Data Science Review 6 (2). https://doi.org/10.1162/99608f92.5317da47

[91] Atıl, B., Aykent, S., Chittams, A., Fu, L., Passonneau, R.J., Radcliffe, E., et al., 2025. Non-Determinism of "Deterministic" LLM System Settings in Hosted Environments, in: Proceedings of the 5th Workshop on Evaluation and Comparison of NLP Systems (Eval4NLP), pp. 135–148. https://doi.org/10.18653/v1/2025.eval4nlp-1.12

[92] Coqueret, G., Llull, J., Oswald, F., Pérignon, C., Scheuch, C., Vilhuber, L., 2026. Randomness in Large Language Models: What Researchers Need to Know (and Report). arXiv:2607.24372.

[93] Ouyang, S., Zhang, J.M., Harman, M., Wang, M., 2025. An Empirical Study of the Non-Determinism of ChatGPT in Code Generation. ACM Transactions on Software Engineering and Methodology 34 (2), 1–28. https://doi.org/10.1145/3697010

[94] Xu, C., Guan, S., Greene, D., Kechadi, M-T., 2024. Benchmark Data Contamination of Large Language Models: A Survey. arXiv:2406.04244.

[95] Hada, R., Gumma, V., de Wynter, A., Diddee, H., Ahmed, M., Choudhury, M., Bali, K., Sitaram, S., 2024. Are Large Language Model-Based Evaluators the Solution to Scaling Up Multilingual Evaluation?, in: Findings of the Association for Computational Linguistics: EACL 2024. arXiv:2309.07462.

[96] Santos, J.G.A., Bonás, G.K., Laitz, T., Almeida, T.S., Pedrini, H., 2026. BLUEX v2: Benchmarking LLMs on Open-Ended Questions from Brazilian University Entrance Exams. arXiv:2606.22723.
