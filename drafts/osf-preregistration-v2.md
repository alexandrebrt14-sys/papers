# OSF Preregistration — Paper 5 (v2 Confirmatory Window)

**Working title**: *"How LLMs cite Brazilian companies: a 90-day confirmatory longitudinal study across five generative engines"*

**Principal investigator**: Alexandre Caramaschi (CEO Brasil GEO; ex-CMO Semantix; co-founder AI Brasil)
**Affiliation**: Brasil GEO — independent research
**Contact**: alexandre@caramaschiai.io
**ORCID**: 0009-0004-9150-485X
**Date of preregistration**: 2026-04-23 (before any v2 data was collected)
**Companion paper**: "Null-Triad — Three Ways to Fail to Conclude", Zenodo DOI 10.5281/zenodo.19712217
**Repository**: https://github.com/alexandrebrt14-sys/papers (MIT, commits `deea1bb`, `680240f`, `93cea8b`, `addf3b8`, `a032560`, `e4df151`, `dd84f06`)
**Data collection window**: 2026-04-23 00:00 UTC to 2026-07-21 23:59 UTC (90 days)

---

## 1. Study type

Confirmatory, observational, longitudinal. The hypotheses, variables, analysis plan, decision rules, and stopping criterion are declared here before any v2 data has been analysed. The authors commit to reporting outcomes regardless of direction (positive, negative, null-supported, or underpowered).

## 2. Background

The companion Paper 4 (Null-Triad, Zenodo DOI 10.5281/zenodo.19712217) documents that the v1 methodology failed to conclude on any of its three hypotheses due to three simultaneous failure modes: underpowered design on H1, null design on H2, and asymmetric instrumentation on H3. The v1 dataset (7,052 queries, 2026-03 to 2026-04) is archived in git tag `paper-4-dataset-frozen-20260423` and is not used in this study.

The v2 reboot (src/analysis/*, src/config_v2.py, Dockerfile, scripts/reproduce.sh) addresses each failure mode with twelve methodological pillars documented in `docs/METHODOLOGY_V2.md` and `CHANGELOG.md`.

## 3. Research questions and hypotheses

### H1 — RAG vs parametric advantage (primary)

**RQ1**: Does the citation rate of Brazilian real-company entities differ between RAG models (Perplexity `sonar`) and parametric models (ChatGPT `gpt-4o-mini`, Claude `claude-haiku-4-5`, Gemini `gemini-2.5-pro`, Groq `llama-3.3-70b-versatile`)?

- **H1₀**: p(cited | RAG) = p(cited | parametric)
- **H1₁**: p(cited | RAG) > p(cited | parametric)

**Effect size of interest**: Cohen's *h* ≥ 0.20 (small-to-medium).
**Direction**: one-sided (RAG expected higher).

### H2 — Hallucination of non-existent entities (primary)

**RQ2**: When probed with adversarial queries that force mention of a fictitious (decoy) entity, what fraction of responses actually mention it? For control queries (no fictitious target), what fraction spontaneously mentions any of the 16 decoys?

- **H2₀ (bounded-null)**: p(mention | adversarial probe) ≤ 0.01 for each LLM.
- **H2₁**: p(mention | adversarial probe) > 0.01 for at least one LLM (evidence of meaningful hallucination rate).

**Decision**: if observed count k=0 after n=1,585 probes per LLM, Rule-of-Three inverse yields upper-bound < 0.19% with α=0.05 → null is supported.

### H3 — Inter-LLM asymmetry (primary)

**RQ3**: Do different LLMs converge on the same set of canonically cited entities per vertical, or do their citation universes diverge?

- **H3₀**: Jaccard similarity between LLM top-K entity sets ≥ P₅ of the null Monte Carlo distribution under uniform sampling (compatibility with uniform).
- **H3₁**: Jaccard < P₅ (significant divergence / inter-LLM asymmetry).

**Null distribution**: 2,000 Monte Carlo simulations of uniform random sampling of K entities per LLM from cohort of size 127.
**K**: K=10 for primary test; sensitivity analyses at K=5 and K=20.

### H4 — Query formulation sensitivity (secondary, exploratory-confirmatory)

**RQ4**: For semantically equivalent queries in directive vs exploratory form (e.g., "Which company leads fintechs in Brazil?" vs "What are the main options in fintechs in Brazil?"), does the cited-entity distribution differ?

- **H4₀**: cited-entity distributions are equal between directive and exploratory forms.
- **H4₁**: they differ (chi-square or Jaccard shift > threshold).

### H5 — Temporal stability (secondary, exploratory-confirmatory)

**RQ5**: Is citation behaviour stationary across the 90-day window, or is there drift attributable to silent model updates?

- **H5₀**: no significant drift in p(cited) or response_hash distribution across 90 days.
- **H5₁**: drift detected (change-point in `model_versions` table or Mann-Kendall trend on p(cited) daily series with p < 0.05).

## 4. Design

### 4.1 Cohort

127 entities total:
- **79 Brazilian real companies** across 4 verticals (fintech 19, retail 20, health 20, technology 20) — source: `src/config_v2.py` `COHORT_{VERTICAL}_REAL`
- **32 international anchors** (8 per vertical: e.g., Revolut, Monzo, Klarna, Amazon, Walmart, Pfizer, etc.) — for cross-vertical comparison
- **16 fictitious decoys** (4 per vertical: e.g., Banco Floresta Digital, MegaStore Brasil) — for false-positive calibration

### 4.2 Query battery

192 canonical queries = 4 verticals × 6 categories (descoberta, comparativo, confiança, experiência, mercado, inovação) × 2 languages (pt, en) × 2 types (directive, exploratory) × 2 temporal frames (atemporal, "em 2026"). Source: `src/config_v2.build_canonical_battery()`. English queries always include "in Brazil" / "Brazilian".

### 4.3 LLM cohort

Five engines, declared canonical (env var `MANDATORY_LLMS` pins all 5):
- ChatGPT (`gpt-4o-mini-2024-07-18`, OpenAI) — parametric
- Claude (`claude-haiku-4-5-20251001`, Anthropic) — parametric
- Gemini (`gemini-2.5-pro`, Google) — parametric
- Perplexity (`sonar`, Perplexity AI) — RAG
- Groq (`llama-3.3-70b-versatile`) — parametric (open-weight)

Temperature fixed at 0.0 for all. Max output tokens per config. Failures counted as missing; if any mandatory LLM produces 0 rows in a run, `collect validate-run` aborts the run (fail-loud).

### 4.4 Collection cadence

Two collections per day at 06:00 and 18:00 BRT (09:00 and 21:00 UTC). GitHub Actions workflow `daily-collect.yml`, concurrency group `papers-daily-collect`, `cancel-in-progress: false`. Target sample size: ~172,800 observations (4 verticals × 48 queries × 5 LLMs × 2 runs/day × 90 days = 172,800).

### 4.5 Fictitious probes (H2 design)

10% of queries per vertical per run are adversarial probes that force inclusion of a decoy. The `query_entry` carries `target_fictional` field, which is detected by `citation_tracker._analyze` and sets `is_probe=1`, `probe_type="decoy"`, `is_calibration=1`, `adversarial_framing=1`. Expected: n_probe ≈ 0.10 × 172,800 = 17,280; per LLM n_probe ≈ 3,456.

## 5. Variables

### 5.1 Primary outcomes

- `cited_v2` (binary, v2 NER extractor): 1 iff any real-cohort entity is mentioned in the response text.
- `fictional_hit` (binary): 1 iff any decoy entity is mentioned in the response text.
- `cited_entities_v2_json` (list of strings): canonical names of real entities mentioned.
- `response_hash` (SHA256 truncated 16): for drift detection (H5).

### 5.2 Covariates

- `llm` (5 levels), `vertical` (4 levels), `query_category` (6 levels), `query_lang` (pt/en), `query_type` (directive/exploratory), `temporal_frame` (atemporal / "em 2026"), `day` (clustering variable), `model_version` (from API response).

## 6. Analysis plan

### 6.1 Statistical framework

- **Multiple testing correction**: Benjamini-Hochberg FDR, α = 0.05, applied within the family of primary hypotheses (H1, H2, H3).
- **Decision rule (pre-registered, canonical)**: reject H₀ **if and only if** BH-adjusted p < 0.05 **AND** the 95% CI excludes the null value. Otherwise: "fail to reject", with explicit verdict "underpower" if CI width > 1.5× Cohen's *h* threshold.
- **Verdicts** (enum): `reject H0 (significant)` · `fail to reject` · `supported null (bounded)` · `pending` · `design null`.

### 6.2 H1 test

- Cluster-robust CR1 sandwich estimator on diff-of-proportions, with clusters = `day`.
- Cohen's *h* with 95% CI.
- Bootstrap BCa confidence interval on *h* (B=10,000) as secondary robustness.
- **Pre-registered sample size**: n ≥ 1,920 per arm for 80% power at *h* = 0.20, α = 0.05 one-sided. Reached within 3 collection days.

### 6.3 H2 test

- For each LLM, binomial rule-of-three inverse test: if k=0 in n probes, upper 95% bound is 3/n.
- **Pre-registered sample size**: n ≥ 1,499 per LLM to achieve upper bound < 0.20%. Reached within 38 collection days.

### 6.4 H3 test

- Monte Carlo null: 2,000 simulations of uniform random top-K entity sets per LLM from cohort size 127.
- Compute observed Jaccard across all LLM pairs; compare vs P₅ of null distribution.
- Decision: observed Jaccard < P₅ → reject H3₀.

### 6.5 H4 test

- Chi-square test of independence on (cited_entity, query_type) within each LLM × vertical cell.
- BH correction within family H4.

### 6.6 H5 test

- Daily series of p(cited) per LLM: Mann-Kendall trend test, 2-sided α = 0.05.
- Change-point detection via `model_versions` table: any row with `detected_change=1` flags a potential drift event.
- Both tests must pass for H5₁ rejection.

### 6.7 Mixed-effects sensitivity

All primary inferences also reported with GLMM (`statsmodels.BinomialBayesMixedGLM`) including random intercepts for query, day, and entity. If fixed-effect coefficients differ by > 20% vs the marginal test, the GLMM estimate is the reported primary.

## 7. Sampling plan & stopping

### 7.1 Data collection stopping rule

Collection runs from 2026-04-23 00:00 UTC to 2026-07-21 23:59 UTC. No early stopping for efficacy. No peeking at the primary outcomes before day 90. Descriptive dashboard updates at alexandrecaramaschi.com/research are permitted because they show aggregate rates, not inferential statistics.

### 7.2 Minimum detectable effect sizes (reached at)

| Hypothesis | Target n | Day reached |
|---|---|---|
| H1 (h = 0.20) | 1,920 per arm | 3 |
| H2 (bound < 0.2%) | 1,499 per LLM | 38 |
| H3 (Jaccard vs P₅) | K=10, n≥60 per LLM | 5 |
| H4 | n ≥ 240 per cell | 30 |
| H5 | daily n ≥ 30 for Mann-Kendall | 2 |

### 7.3 Exclusion criteria

Pre-registered, applied during analysis:
- Rows with `latency_ms` > 120,000 (indicative of timeout retries).
- Rows where `llm.provider` circuit-broken during the run (flagged in `collection_runs.errors_jsonl`).
- Duplicates on `(llm, model, query, day, response_hash)` (keep first, treating others as cache hits).

## 8. Specific null findings we commit to reporting

Per the Null-Triad precedent, we commit to publishing the following even when statistically uninteresting:

1. If H1 fails to reject with CI crossing zero: report as "underpower" with the final n and the smallest effect size that would have been detectable.
2. If H2 k > 0 for any LLM: report per-LLM hallucination rates even if BH-adjusted p > 0.05 — practitioners need the point estimate.
3. If H3 Jaccard ≥ P₅: report which LLM-pair Jaccards were highest as descriptive evidence of partial convergence.
4. If H5 detects a drift event: report the day, the model affected, the magnitude of the shift. Continue collection after drift events; do not re-anchor.

## 9. Analysts and blinding

The principal investigator conducts all analyses. No data analyst blinding is feasible given single-author setup. However:
- All analysis code is committed before day 90 (already in `src/analysis/hypothesis_engine.py`, `src/analysis/cluster_robust.py`, `src/analysis/null_simulation.py`, `src/analysis/power_analysis.py`, `src/analysis/mixed_effects.py`).
- Code is reviewed by external agents in Null-Triad audit (five-parallel-agent review documented 2026-04-23).
- Any post-hoc analysis not pre-registered here will be explicitly flagged as "exploratory" in the Paper 5 manuscript and will not inform the primary decision rules.

## 10. Reproducibility

- Docker: `Dockerfile` pins python 3.11.15-slim, `PYTHONHASHSEED=20260424`, `requirements-lock.txt` pins 12 dependencies including scipy 1.17.1 and statsmodels.
- `scripts/reproduce.sh`: regenerates all paper tables from a git tag with SHA-256 manifest.
- Raw dataset (papers.db) is committed at every run; frozen at day 90 under tag `paper-5-dataset-closed-20260721`.
- Zenodo deposit at submission: separate DOI for dataset (distinct from preprint DOI).

## 11. Amendments

Any amendments to this preregistration after 2026-04-23 will be registered as an **addendum** at OSF, linked from the original preregistration, and reported transparently in the Paper 5 discussion section.

## 12. Deviations

If any protocol deviation occurs during the 90 days (e.g., an LLM API becomes unavailable, a provider deprecates a model, a rate limit forces reduction of the query battery), it will be logged in `.logs/structured/protocol_deviations.jsonl`, reported in Paper 5 Methods, and its impact on inferences quantified via sensitivity analysis.

## 13. Target publication

**Journal**: *Information Sciences* (Elsevier) — open call for empirical studies on generative AI and information retrieval.
**Target submission date**: October 2026.
**Arxiv/SSRN preprint**: concurrent with submission, with OSF DOI of this registration cited in the manuscript.

---

**End of preregistration. Version 1.0. Signed by Alexandre Caramaschi on 2026-04-23, before the v2 dataset contained any records.**
