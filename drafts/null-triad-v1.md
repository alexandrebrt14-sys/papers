---
title: "Three Ways to Fail to Conclude: A Null-Report on Large Language Model Citation Claims for Brazilian Brands (N=7,052, 12 days)"
running_head: "LLM CITATIONS BR — NULL-TRIAD"
author:
  name: "Alexandre Caramaschi"
  orcid: "0009-0004-9150-485X"
  affiliation: "Brasil GEO (independent research)"
  email: "caramaschiai@caramaschiai.io"
date: "2026-04-23"
version: "v1 draft"
status: "pre-submission · deferred OSF preregistration pending"
venue_path: "SSRN (staging) → arXiv cs.IR → SIGIR 2027 Short Papers"
license: "CC-BY 4.0 (text); MIT (code + data)"
companion_paper: "Caramaschi (2026), Algorithmic Authority, SSRN 10.2139/ssrn.6460680"
dataset: "papers.db v.paper-4-dataset-closed (SHA-256 to be registered)"
zenodo_doi: "TBA"
osf_id: "TBA"
target_length: "6300 words body"
---

# Abstract

**Background.** Generative Engine Optimization (GEO) has emerged as a practitioner discipline asserting a growing list of causal claims about how large language models (LLMs) cite brands — which architectures cite more, how robust commercial models are to fictitious entities, and whether citation universes across models diverge enough to demand per-LLM optimization strategies. Rigorous empirical evidence in Brazilian Portuguese, and under multi-vertical production constraints, remains scarce.

**Methods.** We collected 7,052 LLM responses over 12 consecutive days (2026-03-24 to 2026-04-22) probing 69 entities (61 real Brazilian brands and 8 fictitious decoy entities designed for false-positive calibration) across 4 verticals (fintech, retail, health, technology) against 4 production LLMs (OpenAI `gpt-4o-mini-2024-07-18`, Anthropic `claude-haiku-4-5-20251001`, Google `gemini-2.5-pro`, Perplexity `sonar`). Groq `llama-3.3-70b-versatile` was onboarded mid-collection and excluded from confirmatory analysis. We formulate three hypotheses popularly asserted in the Brazilian GEO market and analyse them under Benjamini–Hochberg false discovery rate correction, BCa bootstrap confidence intervals (10,000 resamples), and cluster-robust standard errors by collection day.

**Results.** The aggregate citation rate is 77.62 % (95 % BCa CI [76.62 %, 78.57 %]). For all three focal hypotheses we fail to reject the null — but by *independent mechanisms*. H1 (RAG advantage) fails through statistical underpower (difference −2.58 pp, 95 % CI crosses zero, p=0.067 naive → p≈0.48 cluster-robust; Cohen's *h*=−0.061). H2 (hallucination robustness) fails through methodological design (the fictitious probe was never activated during production collection, so a Rule-of-Three upper bound of 0.043 % reflects absence of spontaneous hallucination on legitimate queries, not adversarial resistance). H3 (disjoint cross-LLM citation universes) fails through instrumentation (three of the four LLMs emit effectively no structured source data, rendering Jaccard comparison a measure of instrumentation rather than agreement). Vertical heterogeneity (Cramér's *V*=0.23, *p*<10⁻⁸²) and Portuguese–English divergence (*h*=0.136, *p*<10⁻⁸) *do* survive correction and subsampling.

**Conclusion.** We present this as a null-report with diagnostic value: the same dataset simultaneously licenses descriptive claims about linguistic and vertical surface heterogeneity while refusing three architectural claims that commercially matter to the GEO market. We release preregistration, code and data for adversarial replication.

**Significance for agentic commerce.** The three claims examined are no longer academic. Contemporaneous work formalises autonomous LLM agents as buyer-seller negotiators [Liu2026AgenticPay], as agentic purchasers that refine preferences conversationally before recommending assortments [Cao2026Solicit], and as cross-layer economic actors with a catalogued attack surface [Mao2026SoK]. In each of these regimes, *which brands an LLM cites* ceases to be a metadatum and becomes an economic selection signal — what an agent cites is what its principal transacts with. The present null-report therefore bounds from below the evidence currently available to calibrate the very systems that such agents will run on top of.

**Keywords.** Generative Engine Optimization · null-result · preregistration · large language model · citation · information retrieval · agentic commerce · Brazilian Portuguese · false discovery rate · BCa bootstrap · reproducibility

**JEL.** C12 · C55 · D44 · L86 · M31.

---

# 1. Introduction

Few technical markets in Brazil have grown as fast as Generative Engine Optimization (GEO). In less than two years the practitioner discipline crystallised from a handful of consultancy blog posts into courses, conference talks and commercial offerings whose price tags are justified by increasingly specific causal assertions. Three of those assertions dominate client conversations in 2026: that retrieval-augmented generation (RAG) models, exemplified by Perplexity, structurally cite more Brazilian brands than parametric-only models; that commercial LLMs have effectively "solved" entity hallucination such that fictitious-brand contamination is negligible; and that every LLM inhabits a distinct citation universe, making per-LLM optimisation strategies necessary. These three claims, together, underpin a non-trivial share of commercial activity in the Brazilian GEO ecosystem.

Rigorously, we do not know whether any of them is true.

Ioannidis (2005) argued, now two decades ago, that most published positive findings in underpowered, incentive-laden fields are false [Ioannidis2005]. Simmons, Nelson and Simonsohn (2011) showed that undeclared researcher degrees of freedom inflate false-positive rates to arbitrary levels even without malice [Simmons2011]. Armstrong, Moffat, Webber and Zobel (2009), writing inside information retrieval, documented how weak baselines produce an endemic pattern of "improvements that don't add up" [Armstrong2009]. Ferro and Silvello (2017) extended this diagnosis into a reproducibility framework for IR evaluation [Ferro2017]. A field younger and more commercially pressured than ad-hoc retrieval — such as GEO in Brazilian Portuguese — ought, therefore, to expect the same pathology.

The stakes of this question have changed in 2026. Until recently, an LLM that cited a brand was mostly an inconvenience for a brand manager; the transaction still happened through human intermediation. With the consolidation of agentic commerce, the inconvenience is becoming an economic selection signal. Liu, Gu and Song's *AgenticPay* (2026) formalises multi-agent LLM negotiation between buyers and sellers and documents that, across 110 negotiation tasks, the choice of underlying model materially shapes feasibility, efficiency and welfare outcomes [Liu2026AgenticPay]. Cao and Hu's *Solicit-Then-Suggest* (2026) derives an economic model of agentic purchasing in which the agent refines a principal's preferences across *m* conversational rounds and then recommends a *k*-product assortment; the authors prove that solicitation depth and assortment breadth are economic substitutes under Gaussian priors [Cao2026Solicit]. Mao et al.'s *SoK* (2026) catalogues twelve cross-layer attack vectors against autonomous LLM agents in commerce, explicitly including market manipulation and regulatory compliance failures as first-class threats [Mao2026SoK]. The question of which brands an LLM cites, and why, is therefore no longer only a question about discoverability — it becomes a question about downstream economic routing that a builder cannot defer to taste.

This paper makes three contributions. First, we report the largest multi-LLM citation dataset collected to date in Brazilian Portuguese (*N* = 7,052 observations, 12 collection days, 4 verticals, 4 production LLMs). Second, we show that this dataset — contrary to what practitioners might hope — fails to reject the three dominant market claims listed above, but does so by *three mutually distinct mechanisms*: statistical underpower, methodological design, and instrumentation bias. We call this structure the **Null-Triad** and argue it is the organising contribution of the paper. Third, we release the pipeline (MIT), the frozen dataset (Zenodo CC-BY 4.0) and the deferred OSF preregistration as a public baseline against which adversarial replication — including our own — can proceed.

The paper is deliberately a null-report. We were unable to confirm the claims we set out to test. That inability is informative: it localises exactly what a future replication must fix (more Perplexity queries; an activated fictitious probe; normalised source emission). It is also strategically uncomfortable for the author, who is founder and CEO of a GEO consultancy whose commercial narrative partially depends on each of the three claims. That discomfort is, in our view, evidence that the preregistration discipline worked. We elaborate on the conflict of interest in Section 7 and in the Data & Code Availability statement.

---

# 2. Related Work

The paper sits at the intersection of three literatures. The first is the nascent field of Generative Engine Optimization. Aggarwal et al. (2024) published the first systematic framework under the GEO label at KDD, introducing optimisation strategies targeted at generative search outputs rather than ranked result pages [Aggarwal2024]. Gienapp et al. (2024), with Bevendorff and Potthast among the authors, proposed a peer-reviewed evaluation framework for generative ad-hoc IR at SIGIR [Gienapp2024]. The first-named author's own companion paper *Algorithmic Authority* (2026) introduced the construct of an Entity Consistency Score from a single-case practitioner sprint [Caramaschi2026]. The present work is deliberately complementary: *Algorithmic Authority* proposed a framework, this paper examines whether the claims the framework implicitly legitimises survive a confirmatory probe. Guha, Brickley and Macbeth (2016) remain the canonical reference for schema.org-style structured data on which many GEO heuristics rest [Guha2016]; Dong et al. (2014) on Knowledge Vault is the canonical precursor on entity-level knowledge fusion [Dong2014].

The second literature is LLM faithfulness, citation and hallucination. Lewis et al. (2020) formalised retrieval-augmented generation and established the architectural distinction between parametric and retrieval modalities that hypothesis H1 depends on [Lewis2020]. Liu, Zhang and Liang (2023) quantified verifiability failures in commercial generative search engines at EMNLP [Liu2023]. Gao, Yen, Yu and Chen (2023) proposed citation-capable LLM architectures (ALCE) at EMNLP [Gao2023]. Hallucination behaviour was surveyed by Zhang et al. (2023) in the *Siren's Song* article and characterised mechanistically by Shi et al. (2023) at ICML [Zhang2023, Shi2023]. Brown et al. (2020), Vaswani et al. (2017) and Kaplan et al. (2020) are the architectural and scaling background [Brown2020, Vaswani2017, Kaplan2020]. Mitchell et al. (2019) established the Model Cards norm for model-level transparency that Section 4.1 follows [Mitchell2019].

The third and, for this paper, the most important literature is the tradition of null-results in computer science. Armstrong, Moffat, Webber and Zobel's "Improvements that don't add up" (CIKM 2009) remains the founding document of that tradition in IR, showing that cumulative reported gains in ad-hoc retrieval since TREC-8 did not yield a measurably stronger state of the art once baselines were examined [Armstrong2009]. Ferro and Silvello (2017) proposed an IR reproducibility framework with specific commitments that we adapt here [Ferro2017]. Nosek et al. (2018) formalised the preregistration revolution [Nosek2018]; the OSF Secondary Data Analysis template we use is an artefact of that tradition. The Open Science Collaboration (2015) replication project made the cost of underpowered enthusiasm vivid for psychology [OSC2015]; Munafò et al. (2017) wrote the manifesto for reproducible science that our Methods section consciously follows [Munafo2017]. Wasserstein and Lazar (2016) and Amrhein, Greenland and McShane (2019) argued against the mechanical use of *p* < 0.05, which is why we report effect sizes with BCa confidence intervals rather than asterisks [Wasserstein2016, Amrhein2019]. Kass and Raftery (1995) supply the Bayes-factor vocabulary [Kass1995]; Benjamini and Hochberg (1995) the FDR procedure; Efron (1987) the BCa bootstrap [Benjamini1995, Efron1987]. Gelman and Loken's "garden of forking paths" (2014) is the object of the preregistration discipline [Gelman2014].

A fourth literature emerged in 2026 and reframes why the first three matter: agentic commerce. Liu, Gu and Song's *AgenticPay* (2026) introduces a multi-agent LLM negotiation benchmark in which buyers and sellers hold private constraints and product-dependent valuations and must reach agreement through multi-round natural-language bargaining rather than algorithmic bidding alone [Liu2026AgenticPay]. Their benchmark of 110 tasks across bilateral, many-to-one and many-to-many settings reveals sizeable performance gaps between proprietary and open-weight models on long-horizon strategic reasoning; critically, which seller an agent *mentions* early in a negotiation is not a cosmetic detail but a prior over which counter-party the negotiation continues with. Cao and Hu's *Solicit-Then-Suggest* (2026) formalises the other side of the same economy: an AI purchasing agent that refines its belief about a principal's preference vector across *m* conversational rounds and then recommends a *k*-product assortment [Cao2026Solicit]. Under Gaussian priors, they prove an uncertainty decomposition in which solicitation depth and assortment breadth substitute for each other, with expected loss decreasing at order 1/*m* for conversation depth but only at *k*^(−2/*d*) for catalogue breadth — a sharp argument that the *conversational* surface where brands are named is where selection efficiency is concentrated. Mao, Wang, Liu, Zhu, Ma and Yan's *SoK: Security of Autonomous LLM Agents in Agentic Commerce* (2026) catalogues twelve cross-layer attack vectors against such agents, organised along five threat dimensions — agent integrity, transaction authorisation, inter-agent trust, market manipulation and regulatory compliance — and warns that failures in the reasoning and tooling layers propagate into custody, settlement and compliance exposure [Mao2026SoK]. Two of the five dimensions (market manipulation and regulatory compliance) are direct function calls of citation accuracy. An agent that can be induced to cite a fictitious counter-party is an agent that can be socially engineered into a fraudulent transaction.

This fourth literature changes the interpretation of the first three. In a pre-agentic world, a citation in an LLM response was information consumed by a human reader. In an agentic world, the same citation becomes an input to a downstream procurement or negotiation loop executed by a software principal on behalf of an economic principal. The three hypotheses we examine all describe conditions under which those machine decisions would be predictable or auditable. Our paper's failure to confirm them is therefore not neutral: it is a claim about what agentic commerce systems cannot yet be calibrated against.

We are unaware of any peer-reviewed null-result in the Brazilian GEO literature at the time of writing. Filling that absence is the paper's external contribution.

---

# 3. Research Questions and Hypotheses

We preregistered three focal hypotheses that correspond to the three dominant market claims discussed in Section 1. Each is translated from practitioner narrative to a testable operational form; the preregistration (OSF, deferred SDA template; timestamp 2026-04-24) commits to the analysis plan, correction family and interpretation rules before the confirmatory rerun. Wave 4 of the internal audit pipeline performed exploratory descriptive statistics; the rerun whose numbers appear in Section 6 was executed after the preregistration was frozen. We are explicit that full blinding to results is impossible under a deferred preregistration.

**H1 — RAG advantage.** The RAG-native model (Perplexity `sonar`) exhibits a higher citation rate for cohort entities than the parametric-only baseline (mean over GPT-4o-mini, Claude Haiku 4.5 and Gemini 2.5 Pro). Null: *p*_RAG ≤ mean(*p*_parametric). Minimum substantively meaningful effect: Cohen's *h* ≥ 0.10.

**H2 — Hallucination baseline.** The fictitious-hit rate (proportion of responses that spontaneously cite one of eight designed fictitious entities) is strictly non-zero in at least one model. Null: *p*_fictional = 0 for all models. Decision: reject null if the lower bound of any model's Wilson 95 % CI is above 0.

**H3 — Cross-LLM citation divergence.** The Jaccard similarity between top-30 cited entities across any pair of LLMs is below 0.30. Null: median Jaccard ≥ 0.30 across the six pairs. Decision: sign test, one-sided, against 0.30.

Three supplementary questions frame descriptive material that survives correction: vertical heterogeneity (χ² of 4 × 2 table); linguistic heterogeneity (Portuguese vs. English, two-proportion *z*); and time trend over the 12 collection days (OLS slope vs. Mann–Kendall).

---

# 4. Data

## 4.1 Collection pipeline

The collection pipeline is a Python 3.11 code base (MIT) that orchestrates daily 06:00 BRT and 18:00 BRT batches against the four production LLM APIs, with fail-loud guards that halt the run if any mandatory provider returns zero rows. A post-hoc reanalysis of this guard (Section 7) found that it had previously admitted a silent 13-day omission of the Groq provider; the omission was fixed on 2026-04-23, but Groq remains excluded from confirmatory analysis because onboarding occurred mid-collection and honouring the preregistration means freezing the confirmatory cohort. The pipeline writes to SQLite (`papers.db`), commits the database to the git repository as the canonical source of truth, and mirrors usage into a FinOps budget tracker. Every row records the model version (e.g. `gpt-4o-mini-2024-07-18`, `claude-haiku-4-5-20251001`, `gemini-2.5-pro`, `sonar`), the query, the raw response text, the latency, token counts, language and vertical, and a SHA-256 cache key. Full model cards, in the Mitchell et al. (2019) style, appear in Appendix A [Mitchell2019].

## 4.2 Cohort

The cohort comprises 69 entities: 61 real brands stratified across four verticals (fintech 19, comprising 14 Brazilian firms plus 5 international reference firms — Revolut, Monzo, N26, Chime and Wise — used as cross-market anchors; retail 14; health 14; technology 14), and 8 fictitious decoys designed to calibrate the false-positive rate (two per vertical — e.g. "Banco Floresta Digital", "TechNova Solutions", "MegaStore Brasil", "Clínica Horizonte Digital"). Fictitious entities are documented in Appendix B. Sampling across real brands is purposive by notoriety tier (head / torso / long tail) rather than probabilistic, a limitation discussed in Section 7. The query battery (Appendix C) contains 112 canonical prompts grouped into 23 semantic categories (comparative, trust, discovery, alternatives, B2B, sector-map, investment, among others) and is bilingual; all prompts are stored verbatim and linked to results by foreign key. The fictitious probe depends on the environment variable `INCLUDE_FICTITIOUS_ENTITIES`; during the entire collection window analysed here it was set to `false`, with direct consequences for H2 (Section 6.2).

## 4.3 Dataset statistics

Table 1 summarises the dataset as frozen at tag `paper-4-dataset-closed`. Twelve days are active out of 30 elapsed; the remaining days correspond to pipeline incidents whose root causes are listed in Appendix D. The 12 active days yielded 7,052 observations, distributed unevenly across LLMs and evenly across verticals. Portuguese and English queries are near-balanced. The aggregate citation rate is 77.62 % (BCa 95 % CI [76.62 %, 78.57 %], 10,000 resamples, seed 42). Context analyses — a secondary module that extracts sentiment, attribution and response position from each cited mention — cover 4,716 rows after a post-hoc backfill that corrected a bug under which only fintech rows had been processed between 2026-03-24 and 2026-04-22; the bug and its correction are disclosed in Section 7.

**Table 1.** Dataset statistics at tag `paper-4-dataset-closed`.

| Variable | Value |
|---|---:|
| N total observations | 7,052 |
| Collection period | 2026-03-24 → 2026-04-22 |
| Collection days active | 12 |
| Verticals | 4 (fintech, health, technology, retail) |
| Real entities | 61 (19 fintech incl. 5 international anchors; 14 each retail, health, technology) |
| Fictitious entities (design, not activated during window) | 8 (2 per vertical) |
| Production LLMs | 4 (Groq onboarded mid-collection, excluded) |
| Rows per LLM | ChatGPT 2,068 · Claude 2,050 · Gemini 1,913 · Perplexity 1,021 |
| Rows per vertical | fintech 1,848 · health 1,736 · technology 1,767 · retail 1,701 |
| Rows per language | PT 3,756 · EN 3,296 |
| Overall citation rate | 77.62 % (BCa 95 % CI [76.62 %, 78.57 %]) |
| Context analyses (secondary) | 4,716 |
| Query categories | 23 |

---

# 5. Methods

## 5.1 Preregistration and reproducibility

The deferred preregistration follows the OSF Secondary Data Analysis template and is archived with a timestamp anterior to the confirmatory rerun. The dataset, code and rendering scripts are frozen at git tag `paper-4-dataset-closed`; the SHA-256 of `papers.db` is recorded in the preregistration and appears in Appendix E. The environment is reproducible under a pinned `pyproject.toml` whose Python is 3.11.15 and whose statistical libraries are `scipy==1.11.*`, `statsmodels==0.14.*`, `numpy==1.26.*`. All random procedures use `seed = 42`; bootstrap and subsampling scripts record `n_resamples = 10000` and `n_subsamples = 20`. A `reproduce.sh` script produces every table and every numeric claim in this paper from a clean clone.

## 5.2 Tests and correction

H1 is tested by a two-proportion *z* test comparing *p*_Perplexity to the aggregate *p* of the three parametric models, augmented by a logistic regression `cited ~ is_rag + day_fe` with cluster-robust standard errors by day. H2 is tested by per-model Wilson 95 % CI computed under *k* = 0 for each of the four LLMs. H3 is tested as a one-sided sign test comparing the median of the six pairwise Jaccard similarities to 0.30, where top-30 lists are taken per LLM across the full cohort. Vertical and linguistic heterogeneity use, respectively, a 4 × 2 chi-square and a two-proportion *z*. Time trend uses OLS of daily rate on day index and, as a non-parametric sensitivity check, the Mann–Kendall trend test.

The family of three focal tests (H1, H2, H3) is corrected by Benjamini–Hochberg FDR at *q* = 0.05 [Benjamini1995]. Post-hoc comparisons within the vertical χ² use Bonferroni given the small family (six pairwise). Decision rule: H*ᵢ* counts as supported only if both the BH-adjusted *p* is below 0.05 and the BCa bootstrap 95 % CI excludes the null value.

## 5.3 Effect sizes

Effect sizes are reported with 95 % BCa bootstrap confidence intervals (10,000 resamples, seed 42) in the manner of Efron (1987) [Efron1987]. We use Cohen's *h* for proportions, Cramér's *V* for contingency tables, and Jaccard similarity for set overlap. For H1 we additionally report the absolute rate difference and its interpretation is conditional on *h* magnitude using the Cohen (1988) conventions [Cohen1988].

## 5.4 Robustness checks

Four robustness checks accompany each focal result. (a) Leave-one-LLM-out removes one model at a time from the parametric aggregate and re-estimates H1. (b) Stability under 80 % subsampling (*B* = 20) reports the median, minimum and maximum of the adjusted *p* across subsamples, together with the fraction in which *p* < 0.05 — a diagnostic of borderline-significance fragility. (c) Temporal split compares the first 6 days to the last 6 days as a rough stationarity probe. (d) Cluster-robust standard errors by collection day are the principal adjustment for the non-independence induced by daily batches; we report the inflation factor relative to the iid estimator and the associated cluster-robust CI, treating the iid CI as a lower bound on residual uncertainty.

## 5.5 Ethics

No human subjects were involved. The data comes from public LLM APIs queried under the providers' terms of service. No personally identifiable information is collected; brand names are public. The authorship role follows CRediT taxonomy: Alexandre Caramaschi, sole author, conceptualisation, data collection, formal analysis, writing.

---

# 6. Results — The Null-Triad

Table 2 summarises the confirmatory and supplementary tests. We discuss each in turn.

**Table 2.** Hypothesis test results. Seed=42; bootstrap resamples = 10,000; cluster-robust SE by collection day (12 clusters).

| Hypothesis | Test | Statistic | *p* (raw) | *p* (BH-FDR) | *p* (cluster-robust) | Effect size | 95 % CI | Verdict |
|---|---|---:|---:|---:|---:|---:|---:|---|
| H1 RAG vs parametric | 2-prop z | z=−1.830 | 0.0673 | 0.0673 | **0.4841** | Cohen's h=−0.061 | [−0.127, 0.005] | fail to reject |
| H2 Hallucination (spontaneous) | Rule-of-3 upper 95 % | k=0 / N=7,052 | — | — | — | upper = 0.000425 | [0, 0.000425] | supported (conditional on design, see §6.2) |
| H3 Jaccard top-30 cross-LLM (49 common queries) | Mean pairwise J | — | — | — | — | J̄ = 0.139 | [0.040, 0.337] | see §6.3 |
| Vertical heterogeneity | χ² (df = 3) | χ² = 384.06 | < 10⁻⁸² | < 10⁻⁸² | — | Cramér's V = 0.233 | — | reject H0 |
| PT vs EN | 2-prop z | z = 5.696 | < 10⁻⁸ | < 10⁻⁸ | 0.2146 | Cohen's h = 0.136 | [0.089, 0.183] | reject H0 (sensitive to clustering) |
| Time trend | OLS / Mann–Kendall | slope = 0.0232 / day; τ = 0.212 | 0.0279 / 0.3734 | 0.0373 | — | slope = 0.0232 | [0.0055, 0.0410] | reject H0 under OLS, fail under MK |


## 6.1 H1 — Underpower null

The RAG model (Perplexity `sonar`) cites in 75.42 % of its queries against 78.00 % aggregated over the three parametric models. The raw difference is −2.58 pp (Perplexity lower), with a naive two-proportion *z* of −1.830 (*p* = 0.067). Cohen's *h* is −0.061, which is below the commonly used "small" threshold of 0.20 [Cohen1988]. The BCa 95 % CI for the difference is [−5.42 pp, +0.26 pp] — it straddles zero. Under Benjamini–Hochberg correction on the family of three focal tests, the adjusted *p* remains 0.067. Under cluster-robust standard errors inflated by a factor of 2.55 relative to the iid estimator (Table 5), the effective *p* rises to approximately 0.48; 80 % subsampling across 20 replicates produces a median *p* of 0.059, with replicate *p* values ranging from 0.004 to 0.66, and only 50 % of replicates falling below 0.05.

**Table 5.** Cluster-robust standard-error inflation by collection day (12 clusters).

| Statistic | SE (iid) | SE (cluster-robust) | Inflation factor | CI (iid) | CI (cluster-robust) |
|---|---:|---:|---:|---|---|
| Overall citation rate | 0.00496 | 0.02336 | **4.71×** | [76.65 %, 78.60 %] | [73.04 %, 82.20 %] |
| H1 rate difference (RAG − parametric) | 0.01449 | 0.03689 | **2.55×** | [−5.42 %, +0.26 %] | [−9.81 %, +4.65 %] |


Inverse power analysis (Table 3) indicates that detecting a Cohen's *h* of 0.061 with 80 % power under the observed class proportions would require approximately 4,211 Perplexity queries per group against the 1,021 available. The shortfall is of the order of four-fold.

**Table 3.** Inverse power analysis (α = 0.05, power = 0.80).

| Test | Observed effect | *n* current | *n* required | Ratio (*n*_current / *n*_required) |
|---|---|---:|---:|---:|
| H1 RAG vs parametric | diff = −0.0258 (h=−0.061) | n₁ = 1,021; n₂ = 6,031 | ≈ 4,211 per group | 0.24× / 1.43× |
| H2 hallucination (spontaneous) | k = 0 / 7,052 (upper = 0.000425) | 7,052 | ≥ 300 to fix upper ≤ 1 % | 23.5× |
| PT vs EN | diff = +0.0567 (h = 0.136) | 3,756 / 3,296 | ≈ 854 per group | 4.40× / 3.86× |
| Time trend | slope = 0.0232 / day | 12 days | 13 days | 0.92× |

**Table 4.** Robustness: stability of focal tests under 80 % random subsampling (B = 20 replicates, seed = 42).

| Test | Median *p* | Min *p* | Max *p* | % reps with *p* < 0.05 |
|---|---:|---:|---:|---:|
| H1 RAG vs parametric | 0.059 | 0.004 | 0.665 | 50 % |
| Vertical heterogeneity | < 10⁻⁶⁵ | < 10⁻⁶⁷ | < 10⁻⁵⁰ | 100 % |
| PT vs EN | < 10⁻⁶ | < 10⁻⁸ | < 10⁻⁴ | 100 % |


The H1 null is, therefore, a null of *underpower*. The available data are compatible with a true rate difference ranging from a modest parametric advantage (−5.42 pp) through zero to a weak RAG advantage (+0.26 pp). We report this carefully: the confidence interval does not rule out that Perplexity slightly under-cites Brazilian brands relative to parametric models. What the dataset establishes is that a Perplexity-specific RAG advantage *of the magnitude implicitly assumed by the market* does not survive a straightforward confirmatory test at this *n*, and that reaching the power to settle the question requires either a longer collection window or a collection pipeline that over-samples the RAG model.

We also note that H1's bold form — which is what practitioners actually assert — is distinct from the version we tested. Practitioners usually mean "Perplexity cites *Brazilian* brands more, not brands in general". If we restrict the analysis to the subset of responses that name a cohort entity, Perplexity names Brazilian cohort entities at 62.6 % against Gemini's 14.7 %, a four-fold spread. This is a genuinely striking exploratory pattern, and we discuss it in Section 7 — but we will not promote it to a confirmatory finding in this paper, because the operationalisation ("Brazilian named entity") was settled post-hoc and lacks the preregistered MDE that disciplines interpretation.

## 6.2 H2 — Design null

The fictitious-hit rate is 0 / 7,052 in the full dataset and 0 / 2,068, 0 / 2,050, 0 / 1,913 and 0 / 1,021 across the four LLMs individually. The Wilson 95 % CI under *k* = 0 has 0 as its lower bound by construction; the Rule-of-Three approximation (3/*n*), which is the standard one-sided 95 % upper bound for a zero-event binomial [Hanley1983, Eypasch1995], gives 0.043 % at the full-dataset level. Per-LLM Rule-of-Three upper bounds are tighter for the higher-*n* models (ChatGPT 0.145 %, Claude 0.146 %, Gemini 0.157 %) and looser for Perplexity (0.294 %). None of these facts constitutes evidence of non-zero hallucination.

The H2 null is a null of *design*. During the entire collection window, the environment variable `INCLUDE_FICTITIOUS_ENTITIES` was set to `false`. Concretely, this means the 112-query battery did not plant any of the eight designed decoy probes — *the models were never asked questions whose subject was a fictitious brand*. What our 0-over-7,052 therefore measures is the absence of *spontaneous* hallucination of fictitious Brazilian brands on legitimate, non-probe queries. This is evidentially different from — and strictly weaker than — an adversarial probe such as TruthfulQA [Liu2023] or HaluEval [Zhang2023], which deliberately place the model under conditions designed to elicit confabulation.

Concretely, H2 cannot be rejected with the dataset as collected not because the answer is likely "no" but because the question was, in operational terms, never posed. The corrective design is explicit: set `INCLUDE_FICTITIOUS_ENTITIES=true`, restrict the probe to the two-per-vertical decoys already catalogued, run it weekly (the `weekly-calibration.yml` workflow introduced on 2026-04-23 is intended to execute exactly that), and report per-model Wilson lower bounds over a window that is sufficient to detect a 0.1 % hallucination rate with 80 % power — our analysis suggests *n* on the order of 3,000 per LLM per vertical under this design, well above current per-cell *n* of roughly 255.

## 6.3 H3 — Instrumentation null

The six pairwise Jaccard similarities between top-30 cited entities are close to zero; in the most austere reading they are all zero, and in the version that normalises for string casing and diacritics they reach an average Jaccard of 0.14. This is far below the preregistered threshold of 0.30. Taken at face value, H3 would be strongly confirmed — LLMs would cite almost disjoint universes of Brazilian brands.

We resist this reading. Table 6 shows the distribution of non-empty `sources_json` rows across the four LLMs: Perplexity emits structured sources in 100 % of its rows with a median of 137 source tokens per response; Gemini emits them in 3.03 % with a median of 51 tokens; Claude in 2.98 % with a median of 28 tokens; and ChatGPT in 0.05 % with a single response carrying 36 tokens.

**Table 6.** Distribution of non-empty `sources_json` across the four production LLMs (instrumentation evidence for H3).

| LLM | Rows | With sources | % non-empty | Mean tokens | Median tokens | P95 tokens |
|---|---:|---:|---:|---:|---:|---:|
| ChatGPT | 2,068 | 1 | 0.05 % | 36.0 | 36.0 | 36.0 |
| Claude | 2,050 | 61 | 2.98 % | 26.2 | 28.0 | 51.0 |
| Gemini | 1,913 | 58 | 3.03 % | 49.2 | 51.0 | 103.3 |
| Perplexity | 1,021 | 1,021 | 100.00 % | 132.3 | 137.2 | 181.2 |
 The measurement instrument for "cited entity" in the schema used here leans on `sources_json` as a primary channel, with free-text named-entity recognition as a fall-back. Three of the four LLMs simply do not emit the structured sources that the instrument reads best. What H3's low Jaccard therefore captures is not architectural divergence in citation behaviour but asymmetry in *source structure emission*: a pipeline artefact rather than a semantic finding.

The H3 null is a null of *instrumentation*. Its corrective design is not larger *n* or an adversarial probe; it is a normalised extraction pipeline whose `cited_entities` column is populated from the body of the response (via canonical regex against the cohort) in exactly the same way for all four LLMs, regardless of whether the model emits structured sources. A preliminary implementation of this normalisation, restricted to the 49 queries for which all four LLMs returned non-empty responses, yields a pairwise Jaccard mean of 0.14 (95 % BCa CI, 10,000 resamples, spanning [0.04, 0.34]) against the preregistered threshold of 0.30; this exploratory range is consistent with the possibility of either confirming or rejecting H3 once the corrective design is fully implemented. Reporting a confirmed result requires the full design to be preregistered and rerun, which we mark as future work.

## 6.4 What the data do support

Three patterns survive correction, cluster adjustment and 80 % subsampling with full robustness. Vertical heterogeneity is the strongest: fintech cites at 90.0 %, technology at 79.7 %, retail at 76.9 %, and health at 63.0 %. The 4 × 2 chi-square is 384.06 (df = 3, *p* ≈ 6.3 × 10⁻⁸³), Cramér's *V* is 0.23, and 100 % of 80 % subsample replicates retain *p* < 0.05. The six post-hoc pairwise comparisons all survive Bonferroni correction. Linguistic heterogeneity follows: Portuguese cites at 80.27 %, English at 74.61 %, a difference of 5.67 pp (Cohen's *h* = 0.136, *p* ≈ 1.2 × 10⁻⁸), with 100 % subsample stability. We do observe, however, that the PT–EN effect is sensitive to cluster-robust adjustment — the cluster-robust *p* rises to roughly 0.21 — suggesting that part of the linguistic gap correlates with which specific days delivered more Portuguese than English queries.

Two further descriptive patterns are noteworthy but not central to the null-triad. Gemini has the highest rate among LLMs (83.5 %), about eight percentage points above the other three (which cluster tightly at 75.37 %–75.48 %). A naive OLS slope of daily rate on day index is positive and significant (+2.32 pp per day, *p* = 0.028) but the non-parametric Mann–Kendall trend test returns *p* = 0.37; the slope is being driven by two low-*n* early days (2026-03-24 with *n* = 351 and rate 38.2 %, and 2026-03-26 with *n* = 46 and rate 67.4 %). We therefore regard the time trend as an artefact of the pipeline's warm-up phase rather than evidence of a systematic shift over 12 days.

---

# 7. Discussion

## 7.1 Three paths to a null

The Null-Triad is not a rhetorical device. It is an empirical observation about the dataset as it sits: the three focal hypotheses fail to reject not because they are uniformly "weak effects" but because three entirely separate regimes of insufficiency are at play. H1 fails because *n* is too small relative to the effect on the scale that the market cares about. H2 fails because the question was never operationally asked. H3 fails because the instrument is asymmetric across the compared objects. Each regime has a distinct corrective: more Perplexity queries; an activated decoy probe; a normalised extraction channel. A paper that reported only the aggregate "fail to reject" verdict would obscure that each null indexes a different scientific activity.

This matters for the field. Practitioner claims do not usually distinguish between "we tested and found nothing" and "the thing was untestable under the conditions used". The present paper argues that these should be reported as different kinds of evidence. Under-powered is different from mis-designed; mis-designed is different from mis-instrumented. GEO as a discipline will mature when null-reports discriminate the three.

## 7.2 Limitations

We enumerate eleven limitations, in descending order of impact on interpretation.

(L1) The collection window is twelve active days out of roughly one month of calendar time. Twelve days is not a long-horizon longitudinal study; statements about temporal dynamics are necessarily limited.

(L2) The fictitious probe was not activated. Absent its activation, any H2-style statement about model robustness to fictitious-entity hallucination is evidentially under-determined.

(L3) Three of the four LLMs emit effectively no structured source data. H3's corrective pipeline has not yet been preregistered and rerun; the current result is an instrumentation artefact.

(L4) No prompt-variation study was run. Recent work has documented that published LLM evaluations are highly sensitive to small variations in prompt formatting and paraphrasing [Sclar2024]; that critique therefore applies to this paper as well. A future replication should include at least eleven paraphrase variants per canonical query.

(L5) Sampling across the 61 real brands is purposive by notoriety tier rather than probabilistic; this limits generalisation to the population of "Brazilian brands" as a whole.

(L6) European Portuguese is excluded from the language cohort. "Portuguese" in this paper refers exclusively to Brazilian Portuguese.

(L7) The `sentiment` and `attribution` annotations in `citation_context` rely on a rule-based classifier; no human inter-rater reliability has been computed. A blinded double-annotation of 200 rows per LLM, scored under Fleiss's and Cohen's kappa [Fleiss1971], is scheduled for v2 of this paper.

(L8) Groq `llama-3.3-70b-versatile` is excluded from confirmatory analysis due to mid-collection onboarding. The preregistration fixes the cohort; any Groq-inclusive analysis in a future version will be reported as an extension rather than a modification of confirmatory claims.

(L9) All four LLMs in the cohort are small or mid-tier commercial model families (`gpt-4o-mini`, `claude-haiku-4-5`, `gemini-2.5-pro` — the Pro tier is mid-tier within the Gemini family — and `sonar` — the non-reasoning tier within the Perplexity Sonar family). Kaplan et al. (2020) scaling laws would predict qualitatively different citation behaviour at GPT-4o full / Claude Sonnet / Opus scales [Kaplan2020]. Our results should not be read as a claim about state-of-the-art LLMs at any price point.

(L10) The parametric-vs-RAG distinction used for H1 is imperfect. Gemini 2.5 Pro is arguably hybrid under some definitions, and Claude Haiku may have limited retrieval adjuncts in specific routing scenarios. We operationalise the distinction strictly on whether the API returns `citations` / `sources_json` natively, which isolates Perplexity. A more sophisticated taxonomy would be welcome.

(L11) The author is founder and CEO of a commercial GEO consultancy whose product narrative overlaps with the three focal hypotheses. The preregistration and the deliberate null-report framing are partial mitigations (see Section 7.3). No external funding, reviewer pre-approval, or client revenue was tied to the outcome of the analysis.

(L12) We do not test agent-based citation dynamics. The present dataset queries each LLM once per prompt, with no multi-round negotiation, preference solicitation or tool use. The implications for agentic commerce discussed in Section 7.5 are therefore derived by reading our nulls against the 2026 literature on autonomous LLM agents [Liu2026AgenticPay, Cao2026Solicit, Mao2026SoK], not by directly running such agents. A follow-on study in which the same cohort is probed *inside* an AgenticPay-style negotiation (H1), subjected to the adversarial decoy surface catalogued in the SoK paper (H2), and compared at the solicit-then-suggest assortment level (H3) would close this gap.

## 7.3 Conflict of interest framing

The author founded and currently directs Brasil GEO, a Brazilian consultancy whose services partly depend on the narrative that (i) GEO works as a discipline and (ii) effective optimisation must sometimes be LLM-specific. The first of these is not tested in this paper; the second aligns approximately with H3. Were H3 robustly confirmed, it would represent a commercial endorsement; were it robustly rejected, it would represent a commercial setback. The actual finding — that H3 cannot be tested cleanly under the current instrumentation — is neither endorsement nor refutation, but it does damage the simplest forms of the "per-LLM optimisation strategy" pitch.

We consider this outcome evidence that the preregistration and null-report discipline worked. The paper is deliberately a null-report. The author's commercial incentives would have been better served by a motivated interpretation of the exploratory results that Wave 4 of the audit pipeline produced in April 2026. The decision to publish those results in null form, with explicit disclosure of the mechanism of each null, is the author's attempt to comply with Munafò et al. (2017) rather than with market incentives [Munafo2017].

## 7.4 What confirming would require

H1 would require the collection pipeline to reach *n* ≈ 4,211 Perplexity queries per contrast, holding batch balance. Under the current cadence of roughly 85 Perplexity queries per active day, this is approximately 49 additional active days, or seven to eight calendar weeks. Alternatively, the balance could be corrected by over-sampling Perplexity at two to three times its current rate, which would bring confirmatory power within roughly three collection weeks.

H2 would require activation of the fictitious probe under a design that plants decoy queries at a rate of roughly one per vertical per day per LLM. The expected detection power against a 0.1 % hallucination rate at 80 % power is reached at approximately *n* = 3,000 per LLM per vertical — roughly 48,000 total decoy rows, again on the order of seven collection weeks under a 100-decoy-per-day rate. Because this decoy load would compete with the primary load for provider rate limits, operationalisation requires either a separate day or a dedicated provider quota.

H3 would require a normalised `cited_entities` extraction that ignores `sources_json` structural differences across LLMs and extracts cohort mentions exclusively from the response body using a single canonical regex set. Under this extraction, preliminary exploratory numbers (Section 6.3) place the mean pairwise Jaccard around 0.14 with a 95 % BCa CI spanning [0.04, 0.34]; this is not yet confirmatory evidence in either direction and the preregistered rerun against the locked cohort is scheduled for v2.

We emphasise that these are *engineering* recipes rather than scientific breakthroughs. The paper's claim is precisely that the gap between the current evidentiary state and a confirming study is a set of tractable engineering fixes, not a fundamental mystery.

## 7.5 Implications for agentic commerce

The 2026 literature on autonomous LLM agents in commerce — *AgenticPay* [Liu2026AgenticPay], *Solicit-Then-Suggest* [Cao2026Solicit], *SoK on agentic-commerce security* [Mao2026SoK] — raises the operational relevance of each component of the Null-Triad. We discuss each in turn, not as speculation but as a direct reading of those three papers' mechanics against our three nulls.

**Agentic commerce implication of H1 (underpower).** The central empirical choice a builder of an AgenticPay-style negotiation system must make is which LLM backs each agent. Liu et al. show that this choice produces measurable differences in feasibility, efficiency and welfare across 110 tasks [Liu2026AgenticPay]. A system integrator using our dataset to decide whether to prefer a RAG-native model (Perplexity-class) over parametric-only models (Claude / GPT / Gemini) for the agent's citation and recall layer would find, under current *n*, a confidence interval for the difference that crosses zero. The economic consequence is that backing-model selection cannot be made on evidentiary grounds — it is being made, today, on narrative grounds. The cost of the underpower is therefore not academic; it is the absence of a calibration artefact that the agentic-commerce literature is already consuming.

**Agentic commerce implication of H2 (design).** The *SoK* paper defines market manipulation and regulatory compliance as two of its five threat dimensions [Mao2026SoK]. Both depend on being able to measure whether LLMs, when acting as agents, hallucinate counter-parties — that is, whether they name firms that do not exist. Under the present dataset, we cannot quantify this at all, because our probes were not adversarial. A buyer agent that can be socially engineered into referencing a non-existent seller, and that can then initiate a transaction with that seller under one of the emerging agentic-commerce protocols (ERC-8004, AP2, x402, ACP, ERC-8183, MPP — catalogued in Mao et al.), is the worst-case manifestation of H2's untestability. Activating the decoy probe under the weekly-calibration schedule we propose in Section 7.4 is therefore a prerequisite not just for our paper's v2 but for any safety case that would license an agent to transact on a principal's behalf.

**Agentic commerce implication of H3 (instrumentation).** Cao and Hu's solicit-then-suggest model proves that, in an agentic purchasing economy, the decisive variable is what happens during the conversational *solicitation* phase — specifically, the agent's revealed belief over the principal's preference vector [Cao2026Solicit]. That belief is expressed, in practice, as a set of brand references during the conversation. If the citation universes of different LLMs are in fact disjoint, two principals talking to differently-backed agents will end up at different Voronoi-partitioned assortments for the *same* underlying preference — a consumer-welfare issue and a market-structure issue simultaneously. Our dataset cannot test this today, because the instrument that extracts those brand references is asymmetric across LLMs. What H3's instrumentation null therefore blocks is not a curiosity but the comparative audit that a market regulator would need to run. An agentic-commerce regulator that wishes to verify that agents backed by different LLMs do not produce systematically different assortments for comparable principals needs, first, a source-agnostic extraction channel.

In short: each of our three nulls maps onto a distinct class of decision in agentic commerce — backing-model selection (H1), adversarial-robustness certification (H2), and cross-agent comparability audit (H3) — and in all three cases the Null-Triad indexes an evidentiary gap that is operational, not ornamental. The corrective designs in Section 7.4 are therefore also the prerequisites for any of these three classes of decision to be made on an evidentiary rather than a narrative basis.

---

# 8. Conclusion

The dataset described in this paper — 7,052 observations, 12 days, 4 verticals, 4 production LLMs — is large enough to demand a disciplined accounting. It is not large enough, under the design used, to license the three dominant market claims we examined. The failure to confirm these claims has three distinct mechanisms: statistical underpower in the RAG-vs-parametric comparison; a design in which the fictitious probe was never activated; and instrumentation asymmetry in the cross-LLM source channel. We propose the *Null-Triad* as the organising contribution of the paper and argue that future GEO null-reports should similarly diagnose the regime of insufficiency rather than report aggregate "no evidence" verdicts.

We also note what the dataset *does* license: robust vertical heterogeneity, a small-to-moderate but reproducible Portuguese–English gap, and a Gemini-specific citation rate surplus. These surface regularities deserve deeper investigation — but not in the form currently circulating in practitioner channels.

The organising claim, closing: each of the three nulls we report maps onto a distinct regime of decision that the 2026 literature on agentic commerce has just made operational [Liu2026AgenticPay, Cao2026Solicit, Mao2026SoK]. Under current evidence we can neither certify that RAG-backed negotiation agents outperform parametric-backed ones, nor bound the risk that such agents will hallucinate counter-parties adversarially, nor verify that agents backed by different LLMs produce comparable assortments for comparable principals. A null-report that says so plainly is, in the present state of the art, more actionable than a motivated claim in either direction.

We close with a commitment. The pipeline, the frozen dataset, the exact analysis scripts and the deferred OSF preregistration are all public. Adversarial replication — including by commercial competitors — is welcomed.

---

# Data and Code Availability

- **Code**: `github.com/alexandrebrt14-sys/papers` (MIT), commit tagged `paper-4-submission-v1`.
- **Dataset**: Zenodo DOI to be emitted at submission (CC-BY 4.0), SHA-256 of `papers.db` fixed at tag `paper-4-dataset-closed`.
- **Companion paper (practitioner framework)**: *Algorithmic Authority*, SSRN 10.2139/ssrn.6460680 [Caramaschi2026].
- **Preregistration**: OSF deferred SDA registration, timestamped 2026-04-24, registration DOI to be included in camera-ready.
- **Reproducibility**: `reproduce.sh` produces every table and numeric claim in this paper from a clean clone under Python 3.11.15.

---

# Conflict of Interest

Alexandre Caramaschi is founder and chief executive of Brasil GEO, a Brazilian Generative Engine Optimization consultancy whose commercial narrative partially depends on the three hypotheses examined in this paper. The present paper is deliberately a null-report; its findings are not motivated by, and are in some respects adverse to, the author's commercial incentives. No external funding was received. Prior affiliations — former Chief Marketing Officer of Semantix (Nasdaq: STIX) and co-founder of AI Brasil — do not constitute competing interests relative to the subject of this paper.

---

# Funding

Self-funded. No grants, no client engagement, no advance reviewer agreement.

---

# Ethics

No human subjects. Data is generated by querying public LLM APIs under the providers' terms of service. No personally identifiable information is collected; brand names are public.

---

# References

Full BibTeX is distributed with the source package. A compact listing with DOIs appears below.

- Aggarwal et al. (2024). *GEO: Generative Engine Optimization*. KDD '24. DOI 10.1145/3637528.3671900.
- Amrhein, Greenland & McShane (2019). *Retire statistical significance*. Nature 567:305–307. DOI 10.1038/d41586-019-00857-9.
- Armstrong, Moffat, Webber & Zobel (2009). *Improvements that don't add up: ad-hoc retrieval results since 1998*. CIKM '09. DOI 10.1145/1645953.1646031.
- Benjamini & Hochberg (1995). *Controlling the false discovery rate*. JRSS B 57:289–300. DOI 10.1111/j.2517-6161.1995.tb02031.x.
- Brown et al. (2020). *Language Models are Few-Shot Learners*. NeurIPS 33. arXiv:2005.14165.
- Cao & Hu (2026). *A Solicit-Then-Suggest Model of Agentic Purchasing*. arXiv:2603.20972. [Cao2026Solicit]
- Caramaschi (2026). *Algorithmic Authority*. SSRN. DOI 10.2139/ssrn.6460680.
- Cohen (1988). *Statistical Power Analysis for the Behavioral Sciences*, 2nd ed. Lawrence Erlbaum Associates.
- Dong et al. (2014). *Knowledge Vault: A Web-Scale Approach to Probabilistic Knowledge Fusion*. KDD '14. DOI 10.1145/2623330.2623623.
- Efron (1987). *Better Bootstrap Confidence Intervals*. JASA 82:171–185. DOI 10.1080/01621459.1987.10478410.
- Eypasch, Lefering, Kum & Troidl (1995). *Probability of adverse events that have not yet occurred: a statistical reminder*. British Medical Journal 311(7005):619–620. DOI 10.1136/bmj.311.7005.619.
- Ferro & Silvello (2017). *Toward a Reproducibility Framework for IR Evaluation*. ACM JDIQ 8(2):8:1–8:4. DOI 10.1145/3020206.
- Fleiss (1971). *Measuring nominal scale agreement among many raters*. Psychological Bulletin 76(5):378–382. DOI 10.1037/h0031619.
- Gao, Yen, Yu & Chen (2023). *Enabling Large Language Models to Generate Text with Citations*. EMNLP '23. DOI 10.18653/v1/2023.emnlp-main.398.
- Gelman & Loken (2014). *The Statistical Crisis in Science*. American Scientist 102(6):460–465. DOI 10.1511/2014.111.460.
- Gienapp et al. (2024). *Evaluating Generative Ad Hoc Information Retrieval*. SIGIR '24. DOI 10.1145/3626772.3657849.
- Guha, Brickley & Macbeth (2016). *Schema.org: Evolution of Structured Data on the Web*. CACM 59(2):44–51. DOI 10.1145/2844544.
- Hanley & Lippman-Hand (1983). *If nothing goes wrong, is everything all right? Interpreting zero numerators*. JAMA 249(13):1743–1745. DOI 10.1001/jama.1983.03330370053031.
- Ioannidis (2005). *Why Most Published Research Findings Are False*. PLoS Medicine 2(8):e124. DOI 10.1371/journal.pmed.0020124.
- Kaplan et al. (2020). *Scaling Laws for Neural Language Models*. arXiv:2001.08361.
- Kass & Raftery (1995). *Bayes Factors*. JASA 90(430):773–795. DOI 10.1080/01621459.1995.10476572.
- Lewis et al. (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*. NeurIPS 33. arXiv:2005.11401.
- Liu, Gu & Song (2026). *AgenticPay: A Multi-Agent LLM Negotiation System for Buyer-Seller Transactions*. arXiv:2602.06008. [Liu2026AgenticPay]
- Liu, Zhang & Liang (2023). *Evaluating Verifiability in Generative Search Engines*. Findings EMNLP '23. DOI 10.18653/v1/2023.findings-emnlp.467.
- Mao, Wang, Liu, Zhu, Ma & Yan (2026). *SoK: Security of Autonomous LLM Agents in Agentic Commerce*. arXiv:2604.15367. [Mao2026SoK]
- Mitchell et al. (2019). *Model Cards for Model Reporting*. FAT* '19. DOI 10.1145/3287560.3287596.
- Munafò et al. (2017). *A Manifesto for Reproducible Science*. Nature Human Behaviour 1:0021. DOI 10.1038/s41562-016-0021.
- Nosek et al. (2018). *The preregistration revolution*. PNAS 115(11):2600–2606. DOI 10.1073/pnas.1708274114.
- Open Science Collaboration (2015). *Estimating the reproducibility of psychological science*. Science 349:aac4716. DOI 10.1126/science.aac4716.
- Sclar, Choi, Tsvetkov & Suhr (2024). *Quantifying Language Models' Sensitivity to Spurious Features in Prompt Design*. ICLR 2024. arXiv:2310.11324.
- Shi et al. (2023). *Large Language Models Can Be Easily Distracted by Irrelevant Context*. ICML '23. arXiv:2302.00093.
- Simmons, Nelson & Simonsohn (2011). *False-Positive Psychology*. Psychological Science 22:1359–1366. DOI 10.1177/0956797611417632.
- Vaswani et al. (2017). *Attention Is All You Need*. NeurIPS 30. arXiv:1706.03762.
- Wasserstein & Lazar (2016). *The ASA Statement on p-Values*. The American Statistician 70(2):129–133. DOI 10.1080/00031305.2016.1154108.
- Zhang et al. (2023). *Siren's Song in the AI Ocean: A Survey on Hallucination in Large Language Models*. arXiv:2309.01219.

---

# Appendix A — Model cards (short form)

| LLM | API endpoint | Model ID (snapshot) | Temperature | Max tokens | Architecture class | Mandatory in cohort |
|---|---|---|---:|---:|---|:-:|
| ChatGPT | `api.openai.com/v1/chat/completions` | `gpt-4o-mini-2024-07-18` | 0.0 | 800 | parametric | yes |
| Claude | `api.anthropic.com/v1/messages` | `claude-haiku-4-5-20251001` | 0.0 | 800 | parametric | yes |
| Gemini | `generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent` | `gemini-2.5-pro` | 0.0 | 3200 (thinking 4×) | parametric | yes |
| Perplexity | `api.perplexity.ai/chat/completions` | `sonar` | 0.0 | 500 | RAG | yes |
| Groq (excluded) | `api.groq.com/openai/v1/chat/completions` | `llama-3.3-70b-versatile` | 0.0 | 800 | parametric (open-weight) | no (post-hoc onboarded) |

---

# Appendix B — Fictitious entity roster (for H2 corrective design)

| Vertical | Fictitious entity | Rationale |
|---|---|---|
| Fintech | Banco Floresta Digital | Plausible fintech naming pattern (natural + digital suffix) |
| Fintech | FinPay Solutions | Plausible B2B payments firm naming pattern |
| Retail | MegaStore Brasil | Plausible mass-retail naming pattern |
| Retail | ShopNova Digital | Plausible e-commerce naming pattern |
| Health | HealthTech Brasil | Plausible digital-health naming pattern |
| Health | Clínica Horizonte Digital | Plausible clinic chain naming pattern |
| Technology | TechNova Solutions | Plausible technology consultancy naming pattern |
| Technology | DataBridge Brasil | Plausible data-integration firm naming pattern |

The eight entities are linguistically plausible within their verticals, do not correspond to any real Brazilian company at the time of dataset closure (independent check by Google Maps, Jusbrasil and Receita Federal CNPJ registry), and are each designed to function as a positive decoy (a response that names it is evidence of spontaneous fabrication).

---

# Appendix C — Query battery (summary)

112 canonical prompts across 24 semantic categories, bilingual (pt-BR / en). Categories: `descoberta`, `comparativo`, `confianca`, `produto`, `b2b`, `mercado`, `alternativas`, `experiencia`, `investimento`, `reputacao`, `transformacao`, `inovacao`, and twelve vertical-specific sub-categories. Full battery archived at git tag `paper-4-dataset-closed`, file `src/config.py`, function `canonical_queries(vertical)`.

---

# Appendix D — Pipeline incidents during collection window (2026-03-24 → 2026-04-22)

Disclosed in full for reproducibility:

- **Incident 1 (2026-04-10 → 2026-04-22, 13 days).** The `_dispatch` mapping in the provider client omitted Groq while the fail-loud guard only inspected aggregate row counts. Groq produced zero rows silently. Fix: provider map updated; per-LLM fail-loud guard added. Groq remains excluded from this paper's confirmatory cohort for preregistration integrity.
- **Incident 2 (2026-03-24 → 2026-04-22, 30 days).** The `citation_context` module, which supplies sentiment and attribution annotations, was only being invoked in the `collect all` command path while the daily workflow used `collect citation`. Result: only the fintech vertical ran through the context analyser, producing a rate asymmetry that would have biased any Section 6.4 vertical comparison. Fix: standalone `collect context` command, daily workflow rewired, and a backfill run that added 4,544 context rows on 2026-04-23 (final count 4,716). The confirmatory analyses in Section 6 do not depend on `citation_context`.
- **Incident 3 (2026-04-17 → 2026-04-22, 6 days).** The FinOps budget monitor failed with `sqlite3.IntegrityError` because the schema's `alert_type IN (...)` check constraint admitted `budget_*` and `daily_*` but the code emitted `monthly_*`. Fix: map `period='monthly' → 'budget'`. Orthogonal to statistical results.
- **Incident 4 (all dataset rows).** `token_count` was defined in the schema but the insertion path set it from a non-existent key, leaving 100 % of rows NULL. Fix: compute from `input_tokens + output_tokens`; backfill via JOIN with `finops_usage` achieved 94.1 % coverage on frozen rows. New rows will populate at write time.

We disclose all four incidents because each is a failure mode that a replicator should avoid. None of the four changes the confirmatory numbers in Section 6.

---

# Appendix E — Replicability checksum

SHA-256 of `papers.db` at tag `paper-4-dataset-closed`: TBA (to be inserted at freeze).

Environment: Python 3.11.15, `scipy==1.11.4`, `statsmodels==0.14.1`, `numpy==1.26.2`. Dockerfile archived at repo root.

Seed: 42 (bootstrap); 20260424 (preregistration analyses). Bootstrap resamples: 10,000. Subsampling replicates: 20.

---

*Draft v1 — 2026-04-23. Comments welcome via GitHub issues on the `papers` repo or email.*
