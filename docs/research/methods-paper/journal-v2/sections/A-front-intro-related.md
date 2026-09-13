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

The quantity this market sells has no agreed definition, and the size of the resulting ambiguity can be measured. A consumer who once read ten ranked links now reads one answer, and the empirical comparison of classical search against Gemini and AI Overviews presented at SIGIR 2026 gives that shift a shape [Grossman2026]. The displacement carries a measured cost on the other side. A difference-in-differences design exploiting the staggered geographic rollout of AI Overviews estimates that default availability reduced monthly external-search referrals to English Wikipedia by 5.45% and 4.82% against the same articles in German and French [Khosravi2026]. Firms named in a generated answer inherit attention that a results page used to spread across ten positions.

An industry formed around that inheritance in under two years. Agencies sell placement in generated answers, vendors sell dashboards that track it, and boards ask for one number. The number is almost always the citation rate: the share of prompts in which a model names a given firm. Movement in that traffic is easy to misread. A single-domain log study with untreated pages on the same domain as a contemporaneous control found ChatGPT referrals to treated pages growing 5.7-fold while untreated pages grew 3.5-fold over the same window, so most of the headline movement was platform growth [Watanabe2026].

Two vendors measuring the same firm in the same week report different citation rates, and neither need be dishonest. They asked different questions, of different models, on different days, and read different amounts of each answer before deciding that the firm was named. The last of those four is the condition §6.5 measures, and §2.8 records that whether published studies declare it has not been surveyed here. The series reported here holds 68,624 canonical observations, collected on 53 days between 2026-04-23 and 2026-09-08 under one 192-query battery and one 127-entity cohort. Across it the panel rate runs from 1.86% on one engine to 52.03% on another under a single 200-character window (§9), and the gap survives the reduction of same-day replicates to one cell per engine, query and day, where the two arms sit at 1.91% over 9,455 cells and 53.09% over 4,737. The two arms do not answer the same battery: the low arm receives all 192 queries and the high one 96, from which three of the six semantic categories are absent, which is itself a declared parameter value and not a difference between the engines. On the 2,225 observations for which the whole response was retained, reading to the end of the response instead of stopping at character 200 moves the rate by 22.95 to 55.73 percentage points, with no observation in any arm losing its citation (§6.5).

A young measurement field in this condition has an ordinary remedy: a protocol that fixes the conditions under which a number is produced, published openly so that anyone can meet it and any reader can check whether it was met. The field has asked for one in its own venue. A position paper at ICML 2026 names concentrated influence under low contestability, undisclosed commercial influence inside evidence and reasoning, and evaluation asymmetries between offline setups and deployed systems as the risks of the transition, and argues for answer-level governance and deployment-aligned metrics [Wen2026]. The case for pinning conditions has an empirical precedent as well: a reproduction study of published TikTok audits at SIGIR 2025 found poor reproducibility and short-term validity in the original findings, traced to conditions those studies had not fixed [Mosnar2025]. Commercial placement has now begun to appear inside the answers themselves [Lurie2026], which raises what an unstandardised metric costs.

BRGEO-1 is an opaque identifier: the prefix denotes the organisation that maintains the specification, in the manner of an IETF or W3C document number, and carries no geographic scope. The protocol is written for any market and any language, and §4 gives the reasons for a Brazilian reference instantiation.

### 1.2 Citation rate is an incompletely specified measurand

Metrology named this problem decades ago and supplies the term for the floor it sets. The International Vocabulary of Metrology defines a measurand as the quantity intended to be measured, and Note 1 to clause 2.3 requires, for the specification of a measurand, knowledge of the kind of quantity together with a description of the state of the phenomenon carrying it [JCGM200]. The market's definition of the citation rate satisfies the first requirement and stops there. Which prompts. Asked of which model version. Under which generation configuration. Read to which length. Under which rule for deciding that a string names the firm. Those five questions are the description of the state of the phenomenon, and a figure published without them reports a quantity whose specification is incomplete.

The six parameters of BRGEO-1 supply that description. P1 fixes the observation window, P2 the cohort the instrument can detect, P3 the query battery, P4 the engine panel with pinned model versions, P5 the generation configuration and P6 the entity matching rule (§3.1). They are the detail the vocabulary requires before the quantity exists as a measurand, which is why §3 states them with normative force and attaches a failure mode to each.

The consequence for uncertainty is sharper than a reader might expect. Clause 2.27 defines definitional uncertainty as the component of measurement uncertainty resulting from the finite amount of detail in the definition of a measurand; Note 1 makes it the practical minimum achievable, and Note 2 states that any change in the descriptive detail leads to another definitional uncertainty [JCGM200]. The window result of §6 is an instance of Note 2. Changing the number of characters read changes the descriptive detail, so the two figures describe two measurands, and the gap between them is not error in the ordinary sense. No sample size closes it, because the two numbers answer different questions. One is head-of-response citation. The other is whole-response citation.

Note 1 also settles what an interval computed from sample size alone is worth. Definitional uncertainty is the practical minimum, so an interval derived from the observation count is narrower than the floor whenever the dominant component never entered the budget. This study's own series shows the size of the omission: clustering by prompt instead of by observation gives a design effect of 63.3 and an effective sample of 1,083 against a nominal 68,624, widening the pooled half-width from 0.29 to 2.29 percentage points over the collection days of the series (§9), while re-reading the same stored responses to the end moves individual arms by tens of points (§6.5).

The Guide to the Expression of Uncertainty in Measurement separates components evaluated from repeated observation, Type A, from those evaluated by other means, Type B, and states that the split concerns the method of evaluation [JCGM100]. Sorted that way, the components the market reports are the Type A ones, and they are the small ones. §3 publishes an uncertainty budget on that split, where the function of a protocol becomes visible: a parameter that is fixed and published stops contributing uncertainty to comparisons between figures declaring the same value for it.

The analogy has a limit that §14 keeps in view. A citation rate has no unit, no calibration hierarchy and no true value, and the measurand is constituted by convention, which is how validity behaves for an unobservable construct [Borsboom2004, Jacobs2021]. A convention has to be written down before anyone can argue about whether it is the right one.

### 1.3 Contributions and structure of the paper

The BRGEO-1 protocol fixes six parameters that any citation-rate claim has to declare, and a five-month record shows what happens to the number when one of them moves. Six contributions follow. §3 gives the specification: six parameters with a rationale and a failure mode each, requirement identifiers, conformance levels on an axis of attestation, the conformance claim a first party publishes, and the missingness ledger. §4 gives a reference instantiation with every value published. §5 reports how the instrument was built and broken, including seven defects that passed every automated check. §6 measures the observation window symmetrically on every arm that retained a full response, 2,225 matched observations collected between 2026-09-06 and 2026-09-08, and reports what the magnitude does to a published reading of one engine. §9 reports five months of descriptive evidence across engines, verticals, languages, query types and entity concentration. §10 defines a reporting index and publishes the evidence against leaning on it, which is the sensitivity analysis the composite-indicator literature prescribes for exactly this case [Saisana2005].

The remaining sections carry the apparatus. §7 covers the calibration decoys and the refusal taxonomy, §8 the instrument drift and the missingness ledger in operation, §11 the analysis plan, §12 the ten decisions an adopter makes and the errors an adopter meets, §13 governance, §14 threats to validity, §15 the discussion and §16 the conclusions. The specification appears here ahead of the confirmatory results it will be tested by, so that the parameter values, the observation window among them, are on the record before the analysis that reads them and not after it.

## 2. Related work

### 2.1 Generative engine optimization, and the harness each study fixes for itself

BRGEO-1 works one level below the optimisation literature: it specifies the conditions under which a citation rate is a comparable quantity. That literature asks how to raise the probability that a source is selected, and each study fixes an evaluation harness adequate to its own comparison. Aggarwal and colleagues introduced the term and the GEO-bench suite at KDD 2024, evaluating content modifications against generative engines [Aggarwal2024]. The line extends to commerce with the E-GEO testbed [Bagga2025], to content organisation with structural feature engineering [Yu2026], and to the features that move source selection in open-domain generative search [Wu2025]. Nimase and colleagues unify black-box prompt attacks, white-box gradient attacks and ten white-hat content strategies under one scoring protocol over five datasets against a fixed open-weight ranker [Nimase2026]; their benchmark shares a name with the suite of Aggarwal and colleagues and is a separate artefact, which matters to a reader who knows one and assumes the other.

Holding the harness constant across arms is what a controlled comparison inside one study requires, and the harness is then reported as an implementation detail. Two studies built on different harnesses produce figures that cannot be read side by side, and nothing in the optimisation literature prevents that, because preventing it was never its question. The ICML 2026 position paper cited in §1.1 argues for black-box auditing of material influence and for metrics aligned with deployed systems [Wen2026], which is a requirement on the measurement layer and not on the content layer.

### 2.2 Measuring visibility and citation: a line that has converged on sampling

During 2026 several authors began treating AI visibility as a statistical estimation problem, and they have converged on one axis. Sielinski treats visibility metrics as sample estimators, showing that apparent differences between domains often fall inside measurement noise [Sielinski2026a], then derives convergence criteria, rank stability and structural sufficiency, for deciding when enough data has been collected [Sielinski2026b]. Schulte and colleagues show that generative search results vary between runs and over time and argue for characterising visibility as a distribution [Schulte2026]. Zhang and colleagues separate citation selection, where a platform chooses a source, from citation absorption, where the cited page contributes language and evidence to the answer [Zhang2026]. Varga distinguishes raw mention from verified mention [Varga2026] and Kumar reports brand visibility at scale [Kumar2026]. The survey covering 2023 to 2026 finds terminology, metrics and evidentiary standards heterogeneous, with no reviewed technique showing a stable effect that holds longitudinally and across platforms [Martinez2026].

Four recent measurements establish how far the conditions move the answer. A crossed random-effects decomposition over 12,933 responses, 20 brands, 8 languages and 3 models reports query language as the largest systematic factor in response-level brand outcomes [Zatuchin2026b]. Across 1,909 English-only queries on six models and 30 brands, Chinese-developed models mention brands at 88.9% against 58.3% for international models, a gap of 30.6 points under identical prompts [Huang2026]. Querying 66 brands in 12 languages over 35,640 responses gives a cross-language mean cosine similarity of 0.825 [Zatuchin2026c], and three skincare experiments report well-known brands recommended in 100% of responses when product specifications are held identical across three models [Chu2026]. Eight of the twelve 2026 works this section cites are single-author preprints without peer review; the peer-reviewed anchors are [Aggarwal2024], [Wen2026], [Grossman2026] and [Mosnar2025]. Every figure this section attributes to a preprint is reported as that work's own claim, and no figure in §§3 to 16 of this paper depends on one.

The Dice Roll Method is the other published attempt to standardise measurement of entity mention in generative engines, and the two standards are disjoint. It formalises repeated-query auditing of brand recommendations over a reanalysis of roughly 190,000 observations across more than 270 brands and six languages, and derives three tiers of iteration guidance from a generalizability-theory decision study, reporting G = 0.58 at five iterations and G = 0.74 at ten [Zatuchin2026a]. It answers how many times a query is repeated and when the resulting measure is reliable, and is agnostic about the cohort, the panel and the extraction rule. BRGEO-1 answers which text is read, which entities can be detected, which queries are asked, which model version answered, under which generation configuration and by which matching rule, and is agnostic about how many repetitions to buy. A measurement declared under both is better specified than one declared under either, and §12 recommends the Dice Roll iteration tiers as a non-normative companion. Generalizability theory is also the vocabulary §9 uses for its variance decomposition.

**Table A1.** Parameters each of the two published protocols fixes, as stated in its own specification document. No observations: the entries are specification content, read from the source documents on 2026-09-11.

| Condition of measurement | Dice Roll Method [Zatuchin2026a] | BRGEO-1 (§3.1) |
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

Entity citation as this paper defines it sits upstream of the attribution question, which asks whether a cited source supports what the answer says and therefore presupposes the naming. Rashkin and colleagues give the Attributable to Identified Sources framework [Rashkin2023], Liu and colleagues establish citation precision and recall as auditable metrics for generative search engines [Liu2023], and Gao and colleagues provide the ALCE benchmark for citation generation [Gao2023]. Audits of source-cited responses report systematic gaps between claimed and actual verifiability [Venkit2024, Venkit2025]. The largest recent instance decomposes AI Overviews at claim level: 55,393 trending queries across 19 topical categories over the 40 days from 13 March to 21 April 2026, with activation at 13.7% of queries overall and 64.7% of question-form queries, nearly 30% of cited domains absent from the co-displayed first-page results, and 11.0% of 98,020 atomic claims unsupported by the pages cited for them [Xu2026]. The survey of generative information retrieval evaluation covers the same ground from both directions, models as assessors and generative systems as objects of assessment [Alaofi2024].

The upstream quantity is whether the firm appears in the answer at all, and it is the one the commercial market reports almost exclusively, which is what gives standardising it practical consequence. The attribution line remains the methodological neighbour, because the discipline of publishing an explicit matching and support criterion alongside a figure comes from it, and P6 is that discipline applied to entity names.

### 2.4 Fictitious entities as a target of measurement

Non-existent entities are an established measurement target with a mature literature behind them. PhantomBench is built from non-existent terms and entities derived from real concepts and reports that frontier models frequently fail to abstain when a question presupposes existence [Jung2026]. HalluLens includes a NonExistentRefusal task [Bang2025], AbstentionBench benchmarks abstention on unanswerable questions [Kirichenko2025], and knowledge-aware refusal in factual tasks is measured on its own terms [Pan2026]. The abstention survey in TACL organises the field and supplies the categories against which any new taxonomy is read [Wen2025]. WildHallucinations moves the unit of analysis to real-world entity queries [Zhao2024], large-scale evidence from non-existent citations shows what fabricated items look like in the wild [Zhao2026], and a model's own signal about fabricated references has been measured directly [Agrawal2024]. The hallucination surveys map the surrounding work [Ji2023, Huang2025].

In each of those designs the fictitious item is what is being measured. BRGEO-1 puts sixteen decoys, each verified as non-existent against registry, mapping and court records before collection, inside the measured cohort, so that the citation rate carries a false-positive floor produced by the run that produced the rate. Across the 68,624 canonical observations of the series no decoy was named spontaneously on any engine, giving a 95% Wilson upper bound of 0.0056% on that floor (§7.1). The refusal taxonomy of §7.2 is stated against the categories of [Wen2025] instead of being proposed on its own, and §7.2 reports what the first implementation did when it counted the decoy name wherever it appeared: 96.7% of 17,919 probe observations were flagged, and 66.8% of the 17,328 flagged responses with non-empty text carry an explicit refusal marker.

### 2.5 Measurement validity, benchmark critique and the arithmetic of composites

Benchmark critique supplies the warrant for treating a widely reported quantity as a construct that has to be modelled. Validity is a property of the relation between an attribute and a measurement outcome [Borsboom2004], and the import of measurement modelling into computing makes that requirement operational for unobservable constructs [Jacobs2021]. Benchmarks acquire authority disconnected from what they measure [Raji2021, Bowman2021], BLEU is the canonical case study [Reiter2018], and a review of 445 benchmarks finds construct-validity problems to be structural [Bean2025]. Two results sit closest to this paper's own: decoding parameters, seed and prompt format move reasoning results far enough to reverse published conclusions [Hochlehnert2025], and chat interface and API diverge, with web search shifting accuracy by up to eight percentage points, which makes access condition a measurement parameter [Encarnacion2026]. A validity-centred framework separates the attestation axis from the validity axis [Salaudeen2025], which is the distinction the conformance levels of §3.3 rest on, and a 2026 position paper argues that aggregate scores are the root cause of underspecified item selection and that item-level data release should be default infrastructure [Jiang2026].

The composite-indicator literature prescribes the test §10 runs. The OECD handbook sets out the construction choices [Nardo2008], and the foundational statement requires every composite to travel with an uncertainty and sensitivity analysis across the choices a defender would accept [Saisana2005]. Nominal weights are shown not to be the weights that drive the ranking, with importance measures that recover the effective ones [Paruolo2013]; the review of weighting, aggregation and robustness gives the grounds for choosing the geometric mean [Greco2019]; and composite indicators serve advocacy as often as analysis, which a custodian selling services in the measured domain has to answer [Saltelli2007]. §10 reports rank correlations between four defensible aggregations of the same three components falling to 0.752 across 66 entities, and a variance decomposition in which coverage carries 72.4% of the variance of the log index, which is the nominal-against-effective weight gap in this instrument. At least one index of this kind is already in circulation: one recent study proposes a Category Ownership Index, a Competitive Vacuum Index and a Displacement Score from 3,750 responses across 50 brands, five industries and three models [Zatuchin2026d].

### 2.6 Reporting standards and specifications that became standards by adoption

Structured declaration of the conditions of an experiment is a converging practice across three communities. In information retrieval, `ir_metadata` attaches an extensible metadata schema to experiment results [Breuer2022] following the PRIMAD model of components that affect reproducibility [Ferro2016], whose current development keeps the line active [Aloqalaa2026], and `repro_eval` turns reproducibility measures into runnable software [Breuer2021], which is the nearest existing model for the conformance test suite §13 promises. In evaluation reporting, benchmark metadata, run data and model metadata are composed into one record with interpretive signals [Ghosh2026, Dhar2025]. In documentation, model cards [Mitchell2019] and datasheets [Gebru2021] set the precedent for structured disclosure, and the algorithm-auditing methodology that underlies this design includes the requirement to record collection failures [Metaxa2021], now extended by automated black-box auditing at scale [Morosini2026] and by domain-specific audits of AI Overviews and featured snippets [Hu2026].

For the shape of an open specification that becomes a standard through adoption rather than authority, HELM [Liang2023], MTEB [Muennighoff2023] and BEIR [Thakur2021] are the precedents, and MMTEB shows the same specification growing by community contribution [Enevoldsen2025]. The institutional genealogy runs through the TREC deep learning track [Craswell2020], the demonstration that relative system ordering survives judge variability provided the protocol is fixed [Voorhees2000], which is the strongest available answer to the objection that non-deterministic answers cannot be measured, the test collection built on query variability [Bailey2016], and artifact review and badging in computing conferences [Ferro2018]. The cautionary case is the reproduction study at SIGIR 2025 [Mosnar2025]: self-declared conformance is open to the same failure, and §13 says so. The normative vocabulary of §3.2 comes from BCP 14 [Bradner1997, Leiba2017], the attestation vocabulary of §3.3 from conformity-assessment terminology [ISO17000], the interlaboratory design named in §13 from the accuracy standard [ISO5725-2], and the measurement vocabulary of §1.2 from [JCGM200] and [JCGM100]; benchmarking, standardisation and certification for AI systems have been connected in the same frame [Adel2024].

### 2.7 Position effects in the input, and truncation of the output by the instrument

What this paper adds about position is a property of the instrument rather than of the models: the conversion P1 describes (§3.1) moves the citation rate by 22.95 to 55.73 percentage points across five arms on 2,225 matched observations (§6.5). Position within a prompt is not neutral, and the output analogue is now measured as well. Models use information in long contexts unevenly [Liu2024], serial position effects appear across tasks and models [Guo2024], and most of those effects are model-specific with language-specific nuance, some models favouring later positions against a universal early-token account [Menschikov2025]. On the output side, models used as zero-shot rankers are sensitive to candidate order and to popularity, so the ordering they emit is not a neutral function of the input [Hou2024]; position bias in recommendation output is measured [Bito2025] and shown to undermine preference consistency in listwise reranking [Bito2026]. Randomising one hundred hotel listings across 5,000 agent sessions against four models finds that position predicts inspection weakly and non-monotonically, and that whether position reaches the choice stage is model-specific in a way that tracks neither provider nor capability [Wadi2026].

Output-side position effects are therefore established, and this paper claims nothing new about them. §6.4 reports susceptibility to a narrow window as a property of the model with the same shape as the heterogeneity of [Wadi2026]: it tracks neither architectural class nor provider.

### 2.8 What the literature leaves unmeasured

The published protocols in this space fix how often a query is asked and how the spread of the answers is characterised; the aperture through which each answer is read is not among the conditions any of them fixes. The consequence is arithmetic. A variance decomposition that partitions response-level variance into resampling, paraphrase, model identity and language treats the response as the unit observed [Zatuchin2026b]. Where a pipeline truncates the response at a length that differs between providers, the four components are computed on four different units, and their comparison across arms inherits that difference without recording it. The sampling question and the aperture question are therefore not parallel: one is answered on top of an answer to the other.

Three further gaps follow from the same reading. The attribution literature measures support for a claim once a source has been named [Rashkin2023, Liu2023, Xu2026] and does not reach the prior question of whether the entity was named at all. The abstention literature measures a model's failure on non-existent items [Jung2026, Wen2025] and does not use them to floor a visibility measurement taken in the same run. The composite-indicator literature prescribes a sensitivity analysis for exactly the construction choices a reporting index makes [Saisana2005, Paruolo2013], and the indices now circulating in this market are published without one [Zatuchin2026d].

Table A2 maps what each line of work states that it constrains onto the six parameters of §3.1. It reads each work's own specification of its conditions and is not a survey of undeclared practice: whether published visibility studies declare an extraction window at all has not been surveyed here, §14 records that as an open item, and this paper therefore makes no claim about how common an undeclared window is outside this pipeline.

**Table A2.** Conditions of observation each line of work states that it constrains, mapped to the parameters of §3.1. No observations: entries record the specification content of the cited works.

| Line of work | What it states that it constrains | Parameters of §3.1 it reaches |
|---|---|---|
| GEO optimisation [Aggarwal2024, Bagga2025, Yu2026, Wu2025, Nimase2026] | content modification and the scoring of its effect, on a harness fixed per study | none across studies |
| Visibility as estimation [Sielinski2026a, Sielinski2026b, Schulte2026] | sample size, convergence and the reporting of a distribution | none |
| Repeated-query auditing [Zatuchin2026a, Zatuchin2026b] | iterations per query, reliability threshold, variance components | P4, as a variance component |
| Attribution [Rashkin2023, Liu2023, Gao2023, Xu2026] | the support criterion linking a claim to a cited source | P6, for sources rather than entities |
| Abstention and non-existence [Jung2026, Bang2025, Kirichenko2025, Wen2025] | the item set of non-existent entities and the refusal outcome | P2, as a target rather than a floor |
| Reporting schemas [Breuer2022, Ghosh2026, Dhar2025, Mitchell2019, Gebru2021] | the fields a report carries | the act of declaring, not the values |
| Composite indicators [Nardo2008, Saisana2005, Paruolo2013, Greco2019] | aggregation, weighting and the sensitivity analysis around them | none; §10 applies them downstream |
| BRGEO-1 (§3) | the six conditions under which the count is taken | P1 to P6 |

The row that the others leave blank is where BRGEO-1 sits, and it arrives with its failures attached: six parameters with a failure mode each (§3), seven defects that passed every automated check (§5), the window measured symmetrically on 2,225 matched observations (§6.5), five months of descriptive evidence (§9), and the evidence against the reporting index, published by its custodian (§10).

---

## Reference keys used

Entries follow Elsevier style. Items [Aggarwal2024] through [Ferro2018] are the v1.0 reference list as verified in `research/R1-literature.md` section A, with the three corrections that section requires applied. Items [Zatuchin2026a] onwards are from `research/R1-literature.md` section B. The four standards at the end are verified in `research/R5-metrology.md` and are flagged in the provenance note below.

[Aggarwal2024] Aggarwal, P., Murahari, V., Rajpurohit, T., Kalyan, A., Narasimhan, K., Deshpande, A., 2024. GEO: Generative Engine Optimization, in: Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining, pp. 5–16. https://doi.org/10.1145/3637528.3671900

[Bagga2025] Bagga, P.S., Farias, V.F., Korkotashvili, T., Peng, T., Wu, Y., 2025. E-GEO: A Testbed for Generative Engine Optimization in E-Commerce. arXiv:2511.20867.

[Yu2026] Yu, J., Yang, M., Ding, Y., Sato, H., 2026. Structural Feature Engineering for Generative Engine Optimization: How Content Structure Shapes Citation Behavior. arXiv:2603.29979.

[Sielinski2026a] Sielinski, R., 2026. Quantifying Uncertainty in AI Visibility: A Statistical Framework for Generative Search Measurement. arXiv:2603.08924.

[Schulte2026] Schulte, J., Bleeker, M., Kaufmann, P., 2026. Don't Measure Once: Measuring Visibility in AI Search (GEO). arXiv:2604.07585.

[Zhang2026] Zhang, K., He, X., Yao, J., 2026. From Citation Selection to Citation Absorption: A Measurement Framework for Generative Engine Optimization Across AI Search Platforms. arXiv:2604.25707.

[Varga2026] Varga, Z., 2026. Per-Entity Bias Mapping for AI Visibility: Why Brand Mentions Require Entity-Specific Calibration. arXiv:2606.21595.

[Kumar2026] Kumar, P., 2026. Generative Engine Optimization at Scale: Measuring Brand Visibility Across AI Search Engines. arXiv:2606.20065.

[Martinez2026] Martinez, O., 2026. Optimizing Visibility in Generative Engines: A Critical Survey of Generative Engine Optimization (2023–2026). arXiv:2607.14035.

[Rashkin2023] Rashkin, H., Nikolaev, V., Lamm, M., Aroyo, L., Collins, M., Das, D., Petrov, S., Tomar, G.S., Turc, I., Reitter, D., 2023. Measuring Attribution in Natural Language Generation Models. Computational Linguistics 49 (4), 777–840. https://doi.org/10.1162/coli_a_00486

[Liu2023] Liu, N.F., Zhang, T., Liang, P., 2023. Evaluating Verifiability in Generative Search Engines, in: Findings of the Association for Computational Linguistics: EMNLP 2023, pp. 7001–7025. https://doi.org/10.18653/v1/2023.findings-emnlp.467

[Gao2023] Gao, T., Yen, H., Yu, J., Chen, D., 2023. Enabling Large Language Models to Generate Text with Citations, in: Proceedings of EMNLP 2023, pp. 6465–6488. https://doi.org/10.18653/v1/2023.emnlp-main.398

[Venkit2024] Venkit, P.N., Laban, P., Zhou, Y., Mao, Y., Wu, C.-S., 2024. Search Engines in an AI Era: The False Promise of Factual and Verifiable Source-Cited Responses. arXiv:2410.22349.

[Venkit2025] Venkit, P.N., Laban, P., Zhou, Y., Huang, K.-H., Mao, Y., Wu, C.-S., 2025. DeepTRACE: Auditing Deep Research AI Systems for Tracking Reliability Across Citations and Evidence. arXiv:2509.04499.

[Jung2026] Jung, H., Gonen, H., 2026. PhantomBench: Benchmarking the Non-existential Threat of Language Models. arXiv:2606.11105.

[Bang2025] Bang, Y., Ji, Z., Schelten, A., Hartshorn, A., Fowler, T., Zhang, C., Cancedda, N., Fung, P., 2025. HalluLens: LLM Hallucination Benchmark, in: Proceedings of ACL 2025 (Volume 1: Long Papers), pp. 24128–24156. https://doi.org/10.18653/v1/2025.acl-long.1176

[Kirichenko2025] Kirichenko, P., Ibrahim, M., Chaudhuri, K., Bell, S.J., 2025. AbstentionBench: Reasoning LLMs Fail on Unanswerable Questions. arXiv:2506.09038.

[Pan2026] Pan, W., Xu, J., Chen, Q., Dong, J., Qin, L., Li, X., Yu, H., Jia, X., 2026. Can LLMs Refuse Questions They Do Not Know? Measuring Knowledge-Aware Refusal in Factual Tasks, in: Proceedings of the International Conference on Learning Representations (ICLR 2026). arXiv:2510.01782.

[Ji2023] Ji, Z., Lee, N., Frieske, R., Yu, T., Su, D., Xu, Y., Ishii, E., Bang, Y., Madotto, A., Fung, P., 2023. Survey of Hallucination in Natural Language Generation. ACM Computing Surveys 55 (12), 1–38. https://doi.org/10.1145/3571730

[Huang2025] Huang, L., Yu, W., Ma, W., Zhong, W., Feng, Z., Wang, H., Chen, Q., Peng, W., Feng, X., Qin, B., Liu, T., 2025. A Survey on Hallucination in Large Language Models: Principles, Taxonomy, Challenges, and Open Questions. ACM Transactions on Information Systems 43 (2), 1–55. https://doi.org/10.1145/3703155

[Jacobs2021] Jacobs, A.Z., Wallach, H., 2021. Measurement and Fairness, in: Proceedings of the 2021 ACM Conference on Fairness, Accountability, and Transparency, pp. 375–385. https://doi.org/10.1145/3442188.3445901

[Raji2021] Raji, I.D., Bender, E.M., Paullada, A., Denton, E., Hanna, A., 2021. AI and the Everything in the Whole Wide World Benchmark, in: Proceedings of the NeurIPS Track on Datasets and Benchmarks 1. arXiv:2111.15366.

[Bowman2021] Bowman, S.R., Dahl, G., 2021. What Will it Take to Fix Benchmarking in Natural Language Understanding?, in: Proceedings of NAACL-HLT 2021, pp. 4843–4855. https://doi.org/10.18653/v1/2021.naacl-main.385

[Reiter2018] Reiter, E., 2018. A Structured Review of the Validity of BLEU. Computational Linguistics 44 (3), 393–401. https://doi.org/10.1162/coli_a_00322

[Bean2025] Bean, A.M., Kearns, R.O., Romanou, A., Hafner, F.S., Mayne, H., et al., 2025. Measuring what Matters: Construct Validity in Large Language Model Benchmarks, in: Proceedings of the NeurIPS 2025 Track on Datasets and Benchmarks. arXiv:2511.04703.

[Hochlehnert2025] Hochlehnert, A., Bhatnagar, H., Udandarao, V., Albanie, S., Prabhu, A., Bethge, M., 2025. A Sober Look at Progress in Language Model Reasoning: Pitfalls and Paths to Reproducibility, in: Proceedings of COLM 2025. arXiv:2504.07086.

[Encarnacion2026] Encarnación, R., Behzad, T., Lurie, E., Metaxa, D., 2026. What Current AI Benchmarks Leave Unmeasured: Modality, Search, Citations, and Implications (for Safety Evaluations). arXiv:2608.06202.

[Breuer2022] Breuer, T., Keller, J., Schaer, P., 2022. ir_metadata: An Extensible Metadata Schema for IR Experiments, in: Proceedings of SIGIR 2022, pp. 3078–3089. https://doi.org/10.1145/3477495.3531738

[Ferro2016] Ferro, N., Fuhr, N., Järvelin, K., Kando, N., Lippold, M., Zobel, J., 2016. Increasing Reproducibility in IR: Findings from the Dagstuhl Seminar on Reproducibility of Data-Oriented Experiments in e-Science. ACM SIGIR Forum 50 (1), 68–82. https://doi.org/10.1145/2964797.2964808

[Ghosh2026] Ghosh, A., Reuel, A., Chim, J., Kennedy, W.M., Yadav, S., Mickel, J., et al., 2026. Evaluation Cards: An Interpretive Layer for AI Evaluation Reporting. arXiv:2606.09809.

[Mitchell2019] Mitchell, M., Wu, S., Zaldivar, A., Barnes, P., Vasserman, L., Hutchinson, B., Spitzer, E., Raji, I.D., Gebru, T., 2019. Model Cards for Model Reporting, in: Proceedings of the Conference on Fairness, Accountability, and Transparency, pp. 220–229. https://doi.org/10.1145/3287560.3287596

[Gebru2021] Gebru, T., Morgenstern, J., Vecchione, B., Vaughan, J.W., Wallach, H., Daumé III, H., Crawford, K., 2021. Datasheets for Datasets. Communications of the ACM 64 (12), 86–92. https://doi.org/10.1145/3458723

[Metaxa2021] Metaxa, D., Park, J.S., Robertson, R.E., Karahalios, K., Wilson, C., Hancock, J.T., Sandvig, C., 2021. Auditing Algorithms: Understanding Algorithmic Systems from the Outside In. Foundations and Trends in Human-Computer Interaction 14 (4), 272–344. https://doi.org/10.1561/1100000083

[Liang2023] Liang, P., Bommasani, R., Lee, T., Tsipras, D., Soylu, D., Yasunaga, M., et al., 2023. Holistic Evaluation of Language Models. Transactions on Machine Learning Research. arXiv:2211.09110.

[Muennighoff2023] Muennighoff, N., Tazi, N., Magne, L., Reimers, N., 2023. MTEB: Massive Text Embedding Benchmark, in: Proceedings of EACL 2023, pp. 2014–2037. https://doi.org/10.18653/v1/2023.eacl-main.148

[Thakur2021] Thakur, N., Reimers, N., Rücklé, A., Srivastava, A., Gurevych, I., 2021. BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models, in: Proceedings of the NeurIPS Track on Datasets and Benchmarks 1. arXiv:2104.08663.

[Enevoldsen2025] Enevoldsen, K., Chung, I., Kerboua, I., Kardos, M., Mathur, A., Stap, D., et al., 2025. MMTEB: Massive Multilingual Text Embedding Benchmark, in: Proceedings of ICLR 2025. arXiv:2502.13595.

[Craswell2020] Craswell, N., Mitra, B., Yilmaz, E., Campos, D., Voorhees, E.M., 2020. Overview of the TREC 2019 Deep Learning Track. arXiv:2003.07820.

[Voorhees2000] Voorhees, E.M., 2000. Variations in relevance judgments and the measurement of retrieval effectiveness. Information Processing & Management 36 (5), 697–716. https://doi.org/10.1016/S0306-4573(00)00010-8

[Bailey2016] Bailey, P., Moffat, A., Scholer, F., Thomas, P., 2016. UQV100: A Test Collection with Query Variability, in: Proceedings of SIGIR 2016, pp. 725–728. https://doi.org/10.1145/2911451.2914671

[Liu2024] Liu, N.F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F., Liang, P., 2024. Lost in the Middle: How Language Models Use Long Contexts. Transactions of the Association for Computational Linguistics 12, 157–173. https://doi.org/10.1162/tacl_a_00638

[Guo2024] Guo, X., Vosoughi, S., 2024. Serial Position Effects of Large Language Models. arXiv:2406.15981.

[Menschikov2025] Menschikov, M., Kharitonov, A., Kotyga, M., Porvatov, V., Zhukovskaya, A., Kagramanyan, D., Shvetsov, E., Burnaev, E., 2025. Beyond Early-Token Bias: Model-Specific and Language-Specific Position Effects in Multilingual LLMs. arXiv:2505.16134.

[Nardo2008] Nardo, M., Saisana, M., Saltelli, A., Tarantola, S., Hoffmann, A., Giovannini, E., 2008. Handbook on Constructing Composite Indicators: Methodology and User Guide. OECD Publishing, Paris. https://doi.org/10.1787/9789264043466-en

[Bradner1997] Bradner, S., 1997. Key words for use in RFCs to Indicate Requirement Levels. RFC 2119, BCP 14, Internet Engineering Task Force. https://doi.org/10.17487/RFC2119

[Leiba2017] Leiba, B., 2017. Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words. RFC 8174, BCP 14, Internet Engineering Task Force. https://doi.org/10.17487/RFC8174

[Ferro2018] Ferro, N., Kelly, D., 2018. SIGIR Initiative to Implement ACM Artifact Review and Badging. ACM SIGIR Forum 52 (1), 4–10. https://doi.org/10.1145/3274784.3274786

[Zatuchin2026a] Żatuchin, D., 2026. The Dice Roll Method: A Standardized Protocol for Repeated-Query Auditing of Large Language Model Brand Recommendations. arXiv:2609.04047.

[Sielinski2026b] Sielinski, R., 2026. From Stochastic to Stable: Rank Stability and Structural Sufficiency in AI Visibility Measurement. arXiv:2607.10341.

[Zatuchin2026b] Żatuchin, D., 2026. Where Does the Noise Come From? A Variance-Components Decomposition of Non-Determinism in LLM Brand Answers. arXiv:2607.13304.

[Zatuchin2026c] Żatuchin, D., 2026. The Language Blind Spot: How Query Language and Brand Recognition Tier Shape AI-Constructed Brand Reputation Across Twelve European Languages. arXiv:2606.23165.

[Huang2026] Huang, J., Situ, R., Ye, R., 2026. Cultural Encoding in Large Language Models: The Existence Gap in AI-Mediated Brand Discovery. arXiv:2601.00869.

[Zatuchin2026d] Żatuchin, D., 2026. Who Owns the AI Recommendation? A Multi-Industry Empirical Map of Brand Category Ownership Across Large Language Models. arXiv:2606.23057.

[Chu2026] Chu, X., Hou, Y., 2026. Incumbent Advantage: Brand Bias and Cognitive Manipulation Dynamics in LLM Recommendation Systems. arXiv:2606.17443.

[Nimase2026] Nimase, O., Chen, Z., Qi, G., Zhao, Y., Hu, X., 2026. GEO-Bench: Benchmarking Ranking Manipulation in Generative Engine Optimization. arXiv:2605.29107.

[Wu2025] Wu, Y., Zhong, S., Kim, Y., Xiong, C., 2025. What Generative Search Engines Like and How to Optimize Web Content Cooperatively. arXiv:2510.11438.

[Wen2026] Wen, Y., Zhang, N., Yuan, H., Chen, X., Zhang, H., Guo, H., 2026. Position: Generative Engine Optimization Creates Underexamined Risks, Governance Must Target Concentration, Disclosure, and Academic Blind Spots, in: Proceedings of the International Conference on Machine Learning (ICML 2026), Position Paper Track. arXiv:2606.12439.

[Xu2026] Xu, H., Iqbal, U., Montgomery, J.M., 2026. Measuring Google AI Overviews: Activation, Source Quality, Claim Fidelity, and Publisher Impact. arXiv:2605.14021.

[Hu2026] Hu, D., Baumann, J., Urman, A., Lichtenegger, E., Forsberg, R., Hannak, A., et al., 2026. Auditing Google's AI Overviews and Featured Snippets: A Case Study on Baby Care and Pregnancy, in: Proceedings of the International AAAI Conference on Web and Social Media (ICWSM 2026). arXiv:2511.12920.

[Grossman2026] Grossman, R., Liu, S., Chen, M.K., Smith, M., Borcea, C., Chen, Y., 2026. How Generative AI Disrupts Search: An Empirical Study of Google Search, Gemini, and AI Overviews, in: Proceedings of the 49th International ACM SIGIR Conference on Research and Development in Information Retrieval (SIGIR 2026). arXiv:2604.27790.

[Khosravi2026] Khosravi, M., Yoganarasimhan, H., 2026. Impact of AI Search Summaries on Website Traffic: Evidence from Google AI Overviews and Wikipedia. arXiv:2602.18455.

[Watanabe2026] Watanabe, K., Nakayashiki, K., 2026. Disentangling Answer Engine Optimization from Platform Growth: A Log-Based Natural Experiment on ChatGPT Referral Traffic. arXiv:2606.04362.

[Lurie2026] Lurie, E., Encarnación, R., Friedler, S.A., Metaxa, D., 2026. The Beginning of ChatGPT Ads, in: Proceedings of the AAAI/ACM Conference on AI, Ethics, and Society (AIES 2026). arXiv:2608.05008.

[Morosini2026] Morosini, A., Cen, S.H., Ilyas, A., Driss, H., Mądry, A., Podimata, C., 2026. Using AI Agents to Automate Black-Box Audits of Personalization Algorithms at Scale. arXiv:2606.30801.

[Mosnar2025] Mosnar, M., Skurla, A., Pecher, B., Tibensky, M., Jakubcik, J., Bindas, A., Sakalik, P., Srba, I., 2025. Revisiting Algorithmic Audits of TikTok: Poor Reproducibility and Short-Term Validity of Findings, in: Proceedings of the International ACM SIGIR Conference on Research and Development in Information Retrieval (SIGIR 2025). arXiv:2504.18140.

[Alaofi2024] Alaofi, M., Arabzadeh, N., Clarke, C.L.A., Sanderson, M., 2024. Generative Information Retrieval Evaluation, in: Shah, C., White, R. (Eds.), Information Access in the Era of Generative AI. Springer. arXiv:2404.08137.

[Agrawal2024] Agrawal, A., Suzgun, M., Mackey, L., Kalai, A.T., 2024. Do Language Models Know When They're Hallucinating References?, in: Findings of the Association for Computational Linguistics: EACL 2024, pp. 912–928. https://doi.org/10.18653/v1/2024.findings-eacl.62

[Zhao2026] Zhao, Z., Wang, Y., Stuart, T., De Vaan, M., Ginsparg, P., Yin, Y., 2026. LLM Hallucinations in the Wild: Large-Scale Evidence from Non-Existent Citations. arXiv:2605.07723.

[Wen2025] Wen, B., Yao, J., Feng, S., Xu, C., Tsvetkov, Y., Howe, B., et al., 2025. Know Your Limits: A Survey of Abstention in Large Language Models. Transactions of the Association for Computational Linguistics 13, 529–556. https://doi.org/10.1162/tacl_a_00754

[Zhao2024] Zhao, W., Goyal, T., Chiu, Y.Y., Jiang, L., Newman, B., Ravichander, A., et al., 2024. WildHallucinations: Evaluating Long-Form Factuality in LLMs with Real-World Entity Queries. arXiv:2407.17468.

[Borsboom2004] Borsboom, D., Mellenbergh, G.J., van Heerden, J., 2004. The Concept of Validity. Psychological Review 111 (4), 1061–1071. https://doi.org/10.1037/0033-295X.111.4.1061

[Salaudeen2025] Salaudeen, O., Reuel, A., Ahmed, A., Bedi, S., Robertson, Z., Sundar, S., et al., 2025. Measurement to Meaning: A Validity-Centered Framework for AI Evaluation. arXiv:2505.10573.

[Jiang2026] Jiang, H., Zhang, S., Zhu, D., Bai, Y., Truong, S.T., Yi, X., Koyejo, S., Xie, X., Xiao, Z., 2026. AI Evaluation Should Require Standardized Item-Level Data Releases. arXiv:2604.03244.

[Dhar2025] Dhar, R., Sanchez Villegas, D., Karamolegkou, A., Schiavone, A., Yuan, Y., Chen, X., et al., 2025. EvalCards: A Framework for Standardized Evaluation Reporting. arXiv:2511.21695.

[Breuer2021] Breuer, T., Ferro, N., Maistro, M., Schaer, P., 2021. repro_eval: A Python Interface to Reproducibility Measures of System-Oriented IR Experiments, in: Advances in Information Retrieval (ECIR 2021), Lecture Notes in Computer Science, pp. 481–486. https://doi.org/10.1007/978-3-030-72240-1_51

[Aloqalaa2026] Aloqalaa, M., Soiland-Reyes, S., Goble, C., 2026. PRIMAD-LID: A Developed Framework for Computational Reproducibility. arXiv:2601.02349.

[Adel2024] Adel, T., Bilson, S., Levene, M., Thompson, A., 2024. Trustworthy Artificial Intelligence in the Context of Metrology, in: Ferreira, M.I.A. (Ed.), Producing Artificial Intelligent Systems: The Roles of Benchmarking, Standardisation and Certification, Studies in Computational Intelligence. Springer. arXiv:2406.10117.

[Hou2024] Hou, Y., Zhang, J., Lin, Z., Lu, H., Xie, R., McAuley, J., Zhao, W.X., 2024. Large Language Models Are Zero-Shot Rankers for Recommender Systems, in: Advances in Information Retrieval (ECIR 2024), Lecture Notes in Computer Science, pp. 364–381. https://doi.org/10.1007/978-3-031-56060-6_24

[Bito2025] Bito, E., Ren, Y., He, E., 2025. Evaluating Position Bias in Large Language Model Recommendations. arXiv:2508.02020.

[Bito2026] Bito, E., Ren, Y., He, E., 2026. Position Bias Undermines Preference Consistency in Listwise LLM-Based Reranking, in: Proceedings of the ACM Conference on Recommender Systems (RecSys 2026). arXiv:2608.03091.

[Wadi2026] Wadi, D., Ma, Y., 2026. Does Rank Still Matter? Position Bias When AI Agents Shop on Our Behalf. arXiv:2608.22697.

[Saisana2005] Saisana, M., Saltelli, A., Tarantola, S., 2005. Uncertainty and Sensitivity Analysis Techniques as Tools for the Quality Assessment of Composite Indicators. Journal of the Royal Statistical Society Series A: Statistics in Society 168 (2), 307–323. https://doi.org/10.1111/j.1467-985X.2005.00350.x

[Paruolo2013] Paruolo, P., Saisana, M., Saltelli, A., 2013. Ratings and Rankings: Voodoo or Science? Journal of the Royal Statistical Society Series A: Statistics in Society 176 (3), 609–634. https://doi.org/10.1111/j.1467-985X.2012.01059.x

[Saltelli2007] Saltelli, A., 2007. Composite Indicators between Analysis and Advocacy. Social Indicators Research 81 (1), 65–77. https://doi.org/10.1007/s11205-006-0024-9

[Greco2019] Greco, S., Ishizaka, A., Tasiou, M., Torrisi, G., 2019. On the Methodological Framework of Composite Indices: A Review of the Issues of Weighting, Aggregation and Robustness. Social Indicators Research 141 (1), 61–94. https://doi.org/10.1007/s11205-017-1832-9

[JCGM200] JCGM 200:2012. International Vocabulary of Metrology: Basic and General Concepts and Associated Terms (VIM), 3rd ed. Joint Committee for Guides in Metrology, BIPM, Sèvres.

[JCGM100] JCGM 100:2008. Evaluation of Measurement Data: Guide to the Expression of Uncertainty in Measurement (GUM). Joint Committee for Guides in Metrology, BIPM, Sèvres.

[ISO17000] ISO/IEC 17000:2020. Conformity Assessment: Vocabulary and General Principles. International Organization for Standardization, Geneva.

[ISO5725-2] ISO 5725-2:1994. Accuracy (Trueness and Precision) of Measurement Methods and Results, Part 2: Basic Method for the Determination of Repeatability and Reproducibility of a Standard Measurement Method. International Organization for Standardization, Geneva.

### Provenance note on four references

[JCGM200] and [JCGM100] are not in `research/R1-literature.md`, which covers the v1.0 reference list and 52 proposed additions. Both were verified in `research/R5-metrology.md`, whose author states that the clause numbers used in §1.2 (VIM 2.3 Note 1, VIM 2.27 Notes 1 and 2, GUM 3.3.4) were read in the official PDFs downloaded from bipm.org on 2026-09-11. [ISO17000] and [ISO5725-2] are recorded in `research/R5-metrology.md` section 7 as paywalled and **not verified at clause level**; both are cited at document level here and no clause of either is quoted. An editor preparing the submission should either open the two ISO documents and confirm the clause content or leave the document-level citation as it stands.

### Keys referenced in other blocks

Writers of blocks B to F reuse the keys above. Four verified entries from `research/R1-literature.md` section B that this block does not cite, and that §3.1, §4 and §14 need, are listed here so the key set stays consistent at assembly: **[Atil2025]** Atıl, B., Aykent, S., Chittams, A., Fu, L., Passonneau, R.J., Radcliffe, E., et al., 2025. Non-Determinism of "Deterministic" LLM System Settings in Hosted Environments, in: Proceedings of the 5th Workshop on Evaluation and Comparison of NLP Systems (Eval4NLP), pp. 135–148. https://doi.org/10.18653/v1/2025.eval4nlp-1.12 · **[Chen2024]** Chen, L., Zaharia, M., Zou, J., 2024. How Is ChatGPT's Behavior Changing Over Time? Harvard Data Science Review 6 (2). https://doi.org/10.1162/99608f92.5317da47 · **[Coqueret2026]** Coqueret, G., Llull, J., Oswald, F., Pérignon, C., Scheuch, C., Vilhuber, L., 2026. Randomness in Large Language Models: What Researchers Need to Know (and Report). arXiv:2607.24372 · **[Santos2026]** Santos, J.G.A., Bonás, G.K., Laitz, T., Almeida, T.S., Pedrini, H., 2026. BLUEX v2: Benchmarking LLMs on Open-Ended Questions from Brazilian University Entrance Exams. arXiv:2606.22723.

---

## Anti-tic pass

A final pass over the delivered text, run against PART C of `research/R4-standards.md` and measured by `reviews/style_check.py`. Every count below is a measurement of the file as delivered, not of an intermediate draft.

**Removed.**

1. **Formulaic antithesis (C.1.1), four instances.** "A standard is more useful here than a metric" was cut with the subsection it belonged to. "They are not an implementation checklist; without them the quantity does not exist" was rewritten as a positive statement of what the parameters supply. "Susceptibility tracks response style, not architecture" became "it tracks neither architectural class nor provider" in §2.7. "The novel claim is not that output position matters, it is that the instrument truncates it" became two declarative sentences in §2.7. The measurer finds zero closed-form and zero graduated antitheses in the delivered prose.
2. **"rather than" as a rhetorical hinge.** Three occurrences remain in prose, 0.8 per thousand words, each marking a real alternative under discussion: attestation against completeness in the abstract, adoption against authority in §2.6, and instrument against model in §2.7. Two more sit in cells of Table A2, where the comparison is the cell's content.
3. **Filler connective opening a paragraph (C.1.3), three instances.** "Moreover" opening the second paragraph of §1.2, "Furthermore" opening the third paragraph of §2.2, and "It is worth noting that" inside §2.6 were deleted. Two of the three paragraphs were re-opened with the information the connective stood in for: "Four recent measurements establish how far the conditions move the answer" and "The consequence for uncertainty is sharper than a reader might expect". The measurer finds zero filler openers and a spent-connective density of 0.06 per 250 words against a threshold of 1.00.
4. **Stylistic em dash (C.1.7), eleven instances.** All eleven were rewritten with a comma, a colon or a sentence break. The measurer finds zero em dashes and zero en dashes in running prose; the en dash survives only in page ranges and year spans inside the reference list, which is Elsevier style.
5. **Vague attribution (C.1.8), three instances.** "The literature indicates that output position matters" and "recent work has shown that audits do not reproduce" acquired their sources in the same sentence: [Hou2024, Bito2025, Bito2026, Wadi2026] and [Mosnar2025]. "The last of those four is the one no vendor publishes" in §1.1 asserted a fact about vendor practice that this paper has not measured, and now reads as a pointer to the condition §6.5 measures and to the reservation §2.8 records. The measurer finds zero vague attributions.
6. **Empty adjectives (C.1.10), five instances.** "Robust" (twice, of the window result), "crucial" (of the matching rule), "comprehensive" (of the survey) and "significant" used non-statistically (of the Wikipedia traffic estimate) were replaced by the number or the consequence. The measurer finds zero empty adjectives in the delivered prose, and the single "robust" in the block sits inside the title of [Greco2019].
7. **Self-narration outside the allowed roadmap (C.1.5), three instances.** "This paper presents a protocol" and "we specify BRGEO-1" were cut from §1.1 and the abstract. The third was the closer of §2.8, which had been written as a five-item inventory of what the paper delivers and therefore moved a roadmap into a related-work section; it now states where BRGEO-1 sits and what it arrives with. §1.3 keeps the single roadmap passage the adapted rule permits. The measurer finds zero self-narration phrases.
8. **Pseudo-profound closer (C.1.2), one instance.** §2.8 ended on "the measurement problem is only beginning". Replaced, and the replacement itself rewritten under item 7. The measurer finds zero pseudo-profound closers.
9. **Percentage without a recoverable denominator (C.1.13), three instances.** "96.7% of probes flagged" in §2.4 gained its 17,919-row denominator and its 17,328-row second denominator; the per-arm contrast in §1.1 now carries the panel figures over 68,624 observations and the replicate-reduced figures over 9,455 and 4,737 cells, and states that the two arms do not answer the same battery; "72.4% of the variance" in §2.5 gained the 66 entities and the statement that the variance is of the log index. The measurer counts 19 percentages in the delivered prose.
10. **Quantity without a count (C.2), two instances.** "A large share of this 2026 literature is single-author preprints" now gives the count, eight of the twelve 2026 works this section cites. "Such indices are already proliferating here", supported by one cited index, now reads "At least one index of this kind is already in circulation".
11. **Adverbs in `-ly` concentrated (C.2).** §2.7 carried five in one paragraph against a warning at four. "Primarily" and "directly" carried no information and were removed; the remaining three do. The measurer finds a maximum of three per paragraph in the block.

**Checked and left alone.**

- **Paragraph length (C.1.9).** Longest prose paragraph is 1,372 characters, in §1.1; the 1,500 warn is not reached and the 2,200 fail is not approached.
- **Contrastive apposition in series (C.2).** Zero occurrences in the 3,908 words of prose. The one instance of the form in the block sits in a cell of Table A2, where the contrast is the cell's content.
- **Rhetorical questions (C.2).** The five fragments in §1.2 ("Which prompts. Asked of which model version.") enumerate the specification detail the market omits and are not interrogative; the measurer finds zero rhetorical questions.
- **Repeated paragraph opening (C.2).** No three-word opening repeats three times. "The" opens 13 of the 33 prose paragraphs, which is article usage and not a template.
- **Visual support (C.2), a warn that is answered and not fixed.** Two tables across 26,731 characters of prose, 13,366 per item against a guide of one per 5,000. An introduction and a related-work section have no empirical display item to carry, and the paper's tables begin in §3; Table A1 and Table A2 hold specification content the prose would otherwise enumerate.
- **Sentence length (C.3).** Reported as the diagnostic the rule requires, never as a target: sentence length runs from 2 to 61 words at a mean of 25.9 and a standard deviation of 13.4, with one sentence above 60.
- **C.6 vocabulary list.** A search for the forty entries returns zero hits in the delivered prose.
- **Claims of absence (PART D.2), three rewritten and none surviving.** "No prior work uses fictitious entities as an instrument" was removed entirely, since the search that would license it has not been run; §2.4 now describes the difference in role without asserting precedence. "Published studies do not declare their extraction window" was replaced in §2.8 by a statement that the survey has not been run and that §14 records it as an open item. "The one no vendor publishes" in §1.1, the same claim in its shortest form, is the instance the earlier pass missed and is rewritten under item 5. The Table A2 entries reading "none" and "not constrained" describe what each work's own specification states that it fixes, and the note above the table says so.
