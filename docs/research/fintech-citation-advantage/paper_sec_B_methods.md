# Section B — Methods (Data, Measurement, Statistical Approach, Threats, Ethics)

## 3. Data and Measurement

We audit spontaneous brand citation in large language model outputs across five
engines and four verticals of the Brazilian market. Collection is automated. A
GitHub Actions workflow issues two scheduled runs per day, sending each prompt to
every engine and persisting the raw response, the engine identifier, the model
version string, the query metadata, and the named-entity extraction result into a
single SQLite store (`papers.db`). The workflow has run continuously since the
opening of the confirmatory window; the analysis reported here covers the complete
collection record, from the first run (April 23, 2026) through the most recent (June 9, 2026).

The five engines and their exact model versions, as recorded in the
`model_version` field of every row, are: ChatGPT (`gpt-4o-mini-2024-07-18`),
Claude (`claude-haiku-4-5`), Gemini (`gemini-2.5-pro`), Perplexity (`sonar`), and
Groq (`llama-3.3-70b`). Four of the five are economy-tier variants. We scope every
claim accordingly and do not extrapolate to flagship models; this restriction is a
validity boundary, not an aside (see Section on Threats to Validity).

### 3.1 Verticals, roster, and entity cohort

The four verticals are fintech, retail, technology, and healthcare, all in the
Brazilian market. Detection runs against a cohort of 127 entities: 79 real
Brazilian entities, 32 international anchors, and 16 fictitious decoys. The decoys
are invented names that should almost never be cited; they exist to probe detector
specificity. The roster effectively evaluated per vertical — the real Brazilian
brands whose mentions enter the rate — is unbalanced by design: fintech carries 19
entities, while retail, technology, and healthcare carry 15 each. We flag this
asymmetry rather than hide it. A larger roster mechanically raises the chance that
some brand appears, so per-entity normalization is reported alongside per-response
rates (Section on Statistical Approach), and on the per-roster-entity metric retail
(0.01662) already exceeds fintech (0.01482).

Entity-to-vertical allocation is a clean partition: zero entity strings appear in
more than one vertical. No string leaks across verticals. The partition is
nonetheless an analyst decision — Mercado Pago is coded only in fintech and Mercado
Livre only in retail, although both belong to the same economic group; iFood is
coded only in technology. We declare this allocation as a design degree of freedom.

### 3.2 Query design

Each vertical is probed by 48 distinct queries. The 48 are generated from a single
shared set of templates, with only the vertical-naming phrase swapped between them.
The design is balanced: 8 queries per `query_category` (comparative, trust,
discovery, experience, innovation, market) in every vertical, and 24 directive
against 24 exploratory in every vertical, split across Portuguese and English.
Paired examples illustrate the parallelism: "Como está estruturado o mercado de
fintechs e bancos digitais no Brasil?" against the structurally identical retail
and healthcare variants.

One property of the design we report as a verified strength, because it neutralizes
the most obvious objection. None of the 48 queries in any vertical contains the
name of a roster brand — 0 of 48 in all four verticals, confirmed by direct
inspection of the query table. There is no construct leakage through the prompt
wording: the questions do not induce the brands they are testing for. Reviewers
should weigh this against the looser practice common in the literature, where
vertical is operationalized as a prompt variation rather than as a fully paired,
brand-free template.

Each query is repeated roughly 293 times over the window (two daily runs across the
days, engines, and languages). This repetition structure defines the cluster
geometry that governs inference and is treated explicitly below.

### 3.3 Extraction (NER v2)

A named-entity recognition pass (NER v2, recorded as `cited_v2`) marks, per
response, whether any roster entity was cited. The detector supports alias matching
(`via_alias_count_v2`) and folding (`via_fold_count_v2`). Items outside the analysis
core — adversarial probes (`is_probe`) and calibration items (`is_calibration`) — are
excluded. The analysis core is defined as `is_probe=0 AND is_calibration=0 AND
extraction_version='v2'`.

### 3.4 Window and sample sizes

The confirmatory window (v2) runs from 2026-04-23 to 2026-07-21. This report is the
a full snapshot through June 9, 2026, with the collection program still active. The raw sample is
n=62,820. The analysis core is n=50,453, with `cited_v2`=10,218, a global citation
rate of 20.25%. Per-vertical core sizes are fintech 12,648, retail 12,648,
technology 12,547, and healthcare 12,610. Per cell of the vertical-by-engine matrix
the count is roughly 2,832, except Perplexity at roughly 1,416, which was collected
at half cadence.

### 3.5 Public dataset and provenance

The analysis is reproduced by scripts that read `papers.db` directly:
`_run_stats.py` and `_run_stats2.py` print every number in the results tables,
`extract_analysis.py` regenerates the quantitative summary, and `run_waves.sh`
orchestrates the external model board. Because collection is commit-driven, every
observation carries collection-day provenance, and the rate series can be
reconstructed week by week. The frozen dataset, the analysis code, and the public
dump are to be released with SHA-256 manifests; those manifests are not yet
materialized and are tracked as a submission blocker (see Ethics, Data
Availability and Reproducibility).

### 3.X Measurement caveat — response truncation

One measurement fact constrains every absolute rate in this paper and we state it
plainly. The `response_text` field was persisted truncated at exactly 200
characters for four of the five collectors. Direct inspection of
`LENGTH(response_text)` confirms it: ChatGPT, Claude, and Gemini show 100% of rows
at exactly 200 characters (11,328 / 11,194 / 10,939 rows respectively); Perplexity
is the exception, ranging from 198 to 2,502 characters with a mean of 722 and 0% of
rows at exactly 200.

The consequence for the construct is precise. NER v2 ran over the opening snippet,
not the full response. What `cited_v2` measures, for four of five engines, is
whether a brand appears in the first roughly 200 characters — citation in the
response opening, or front-loading — not full citation propensity. Engines that
open with rhetorical preamble are penalized: a real Gemini retail response cuts mid-
word at "volume de v[endas]" before any brand appears. The destroyed text cannot be
recovered from storage, so the bias is not correctable in the current data; a dual-
track re-collection that persists the full text and re-runs the NER is running until
window close (2026-07-21), with about six weeks of integral collection before the
window ends.

The Perplexity full-text subset bounds the bias rather than removing it. Measured on
the untruncated engine, the fraction of citations whose first entity name appears
after character 200 — exactly the citations truncation would destroy — is 20.5% for
fintech, 20.9% for retail, 30.7% for healthcare, and 51.6% for technology. The
direction matters and corrects an earlier reading. Truncation does not reward
fintech by front-loading; it penalizes the rivals, erasing over half of
technology's citations and nearly a third of healthcare's against about a fifth of
fintech's and retail's. The fintech-versus-technology and fintech-versus-healthcare
gaps are therefore partly an artifact of the cut, while the fintech-versus-retail
gap (both near 20%) is not. Truncation also inflates within-fintech anchor dominance,
because tail brands surface late (PicPay at 515, Banco Inter at 838 characters) and
are cut before they register; the 49.68% Nubank share must accordingly be read as an
upper bound until integral re-collection lands.

## Statistical Approach

The observation unit is the binary outcome `cited`. The naive specification treats
all 50,453 responses as independent, which is false. Each of the 48 queries per
vertical is repeated roughly 293 times across two daily runs, days, engines, and
languages, so the effective sample is on the order of 48 queries × 5 engines ≈ 240
clusters, not 50,453 trials. A chi-square that ignores this overstates precision
grossly: the fintech-versus-retail contrast reads χ²=33.6, p=6.8×10⁻⁹ under i.i.d.,
but aggregating to the 48 query-clusters per vertical and running a Welch test on
the per-cluster means gives t=0.645 (df≈94), not significant — the between-query
standard deviation (about 24 percentage points) swallows the 3.2-point gap. We
therefore report the surface fintech advantage as a descriptive observation, not as
an inference.

The principal model is a logistic generalized linear mixed model (GLMM) with random
intercepts for query and for collection day (ideally also for engine), estimating

  logit P(cited=1) = β₀ + β₁·vertical + β₂·llm + β₃·query_category + β₄·query_lang
                     + (1 | query) + (1 | collection_day),

with references vertical=healthcare, llm=ChatGPT, category=comparative. Odds ratios
are reported as exp(β) with profile 95% intervals. Cluster-robust standard errors
(by query and by engine) and a query-cluster bootstrap serve as robustness checks.
The model is run with a dual outcome: `cited_v2` and `cited_loo`, the latter
recoding as not-cited every fintech response whose only entity is the anchor. The
odds-ratio inversion for fintech (adjusted OR 4.13 to 0.77) belongs in the body, not
an appendix, because that inversion — unlike the surface gap — survives clustering
(Welch t=−3.353 on per-cluster LOO means) and is stable across all eight weeks (LOO
gap −7.6 to −8.2 percentage points).

Wilson intervals are reported for description only, never as the basis for the
inferential claim. A jackknife / leave-one-out protocol is run per vertical, not only
for Nubank: Mercado Livre and Magazine Luiza for retail, Totvs for technology, and
Hypera and EMS for healthcare, with confidence intervals on the drops themselves so
that the asymmetry of fragility (fintech falls 16.70 points; the others 2.55–5.67)
is itself tested rather than asserted. Engine heterogeneity is handled with
Mantel-Haenszel common odds ratios stratified by category (fintech vs retail,
M-H OR=1.205) and a Breslow-Day test of homogeneity, which rejects (χ²=25.42, 5 df,
p=0.0001), justifying the vertical-by-category interaction term. Multiple-comparison
correction (Holm/FDR) is applied over the 4×5×6=108 tested cells and the pairwise
contrasts. Power is assessed at the cluster level (~240), not the observation level,
because that is where the near-vertical reversals under LOO can still shift before
the window closes at day 90.

## Threats to Validity

We organize threats by type and state the mitigation status of each.

**Construct validity.** The dominant threat is the 200-character truncation: for
four of five engines `cited_v2` measures front-loading, not full citation.
Mitigation is the integral re-collection running to window close; until it lands,
every absolute rate is read as a potential truncation artifact (status: unresolved,
re-collection in progress). The decoy false-positive rate is catastrophic — fictitious
brands are "found" in 96.94%–98.61% of probe cases across verticals — so detector
specificity is near zero on that test. The mitigation is to determine and document
whether the high false-positive rate is by design (a decoy planted in the prompt to
test obedience, hence not comparable to spontaneous citation) or a detector bug
requiring correction (status: unresolved, audit pending; the board briefing's claim
of "low decoy FPR" is overruled by the verified database). Alias matching applies
unequal leniency across verticals (healthcare 991 alias hits, technology 4), so the
construct partly reflects annotator alias curation; mitigation is to report strict-
match rates beside alias-inclusive rates (status: planned). Self-report validation
from the `dual_responses` table is available but unused in the main analysis
(status: planned as cross-validation).

**Internal validity.** The unbalanced roster (19 vs 15) mechanically favors fintech;
mitigation is per-entity normalization, already showing retail above fintech, plus
fixed-size roster resampling (status: partially addressed). Brand selection is
neither blind nor preregistered, risking circularity — choosing citable brands and
concluding the vertical is citable; mitigation is to document, ideally preregister,
the selection criterion (status: to document). Single-entity dependence is the
central internal threat and the paper's pivot: removing Nubank drops fintech from
28.15% to 11.46%, from first to last place. This is reframed as the contribution —
anchor-entity concentration — rather than treated as a defect to be corrected
(status: prototyped via LOO, generalized to all verticals).

**External validity.** Four of five engines are economy-tier; results do not
generalize to flagships. Mitigation is to scope the claim explicitly to economy-tier
models and declare exact `model_version` strings (status: scoped). Each engine is a
single frozen version with no cross-version replication, so temporal validity is
limited (status: declared as limitation; an optional cross-version probe is proposed
if budget allows). The causal narrative — corpus density, category brands — is
post-hoc: no corpus-size, news-share, or search-volume measure was crossed with the
rate. Mitigation is to present the mechanisms as hypotheses with discriminating
tests, not established causality (status: reframed).

**Statistical conclusion validity.** Non-independence inflates intervals and
p-values: the effective n is ~240 clusters, and p<10⁻¹⁵⁰ denotes "highly significant"
under a false i.i.d. assumption, not literal precision. Mitigation is the clustered
GLMM and multiple-comparison correction described above (status: designed). Engine
heterogeneity is itself a threat to the aggregate claim: only two of five engines
(Claude, Gemini) place fintech above retail, the aggregate gap is largely a Claude-
Haiku idiosyncrasy (+574 cited responses) plus a Gemini truncation artifact (+134),
and Gemini's zeros are themselves measurement artifacts (preamble cut before the
brand). Mitigation is to elevate engine heterogeneity to a first-order finding, to
report direction per engine, and to remove or re-collect Gemini (status: reframed;
Gemini decision pending). The anchor-entity share, the central metric, is also
threatened by truncation, which cuts late-appearing tail brands and exaggerates
Nubank's dominance; the 49.68% share is therefore an upper bound pending integral
re-collection (status: declared).

## Ethics, Data Availability, and Reproducibility

This is an observational measurement study. It measures the frequency of spontaneous
brand mention in public LLM output; it does not recommend brands, audit product
quality, or confer endorsement. We state explicitly that high citation does not imply
product superiority and that low citation does not imply deficiency. The measured
bias is a property of the models and their training corpora, not conduct by the named
companies: the manuscript reads "model X cites Nubank," never "Nubank is more citable
because it is better." No proprietary data and no material non-public information are
used; every entity is named solely because it appears in public LLM output. Subjects
are legal persons, not natural persons, and the mentions derive from public output,
so no personal data is processed and LGPD does not apply — we declare this rather than
leave it implicit. Anonymization would be counterproductive: it would destroy the
contribution (the Nubank case is the paper) without reducing real risk, since the
thesis concerns a mechanism favorable to all brands. We therefore name entities, with
the ethics framing above, and we declare no competing interests.

The dataset and protocol are released publicly so that any named brand can reproduce
and contest the result, which serves as a factual right of reply. The dataset is
deposited at Zenodo (DOI 10.5281/zenodo.19687866) and the analysis software at Zenodo
(DOI 10.5281/zenodo.19687958); the open repository is at
github.com/alexandrebrt14-sys/papers, and the corresponding author's ORCID is
0009-0004-9150-485X. The reproducibility package is incomplete at this stage,
and we list the gaps as binding: SHA-256 manifests for the frozen `papers.db`, the
scripts, and the public dump; a versioned dataset with a data dictionary; the NER
codebook (per-vertical alias table, folding rules, disambiguation criterion), without
which the alias asymmetry is not auditable; the roster selection protocol; and an
environment lock for the analysis scripts. These are scheduled before submission and
the dataset continues to accrue in the ongoing collection program; subsequent snapshots will extend this record.
