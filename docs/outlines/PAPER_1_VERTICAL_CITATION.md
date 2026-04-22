# Paper 1 — How LLMs Cite Entities Across Industry Verticals: A 90-Day Empirical Study

**Target venue:** arXiv `cs.IR` (moderated preprint, no APC, cross-post permitido para futura submissão em periódico).
**Status:** draft-in-progress, dados em coleta longitudinal contínua (08/04/2026 → 06/07/2026).
**Draft target:** julho/2026 (pós-fechamento da janela de 90 dias).
**Autor:** Alexandre Caramaschi (Brasil GEO).

---

## 1. Title

**Primary title (working):**
> How Large Language Models Cite Entities Across Industry Verticals: A 90-Day Longitudinal Empirical Study of Five Commercial LLMs

**Alternative (if space constrained):**
> Vertical Asymmetries in LLM Citation Behavior: A Longitudinal Multi-Model Study

---

## 2. Abstract (target 180–230 words)

> Large Language Models (LLMs) increasingly mediate consumer discovery of commercial entities, yet the empirical properties of their citation behavior across industry verticals remain poorly characterized. We present results from a 90-day longitudinal observational study that probes five commercial LLMs (OpenAI GPT-4o-mini, Anthropic Claude Haiku 4.5, Google Gemini 2.5, Perplexity Sonar, Groq Llama 3.3 70B) with a fixed battery of queries covering 69 entities in four industry verticals (fintech, retail, healthcare, technology). Queries are stratified by type (directive vs. exploratory) and language (pt-BR vs. en-US) and are dispatched twice daily via a reproducible GitHub Actions pipeline. The observational unit is a single query–model pair; we record whether any cohort entity was cited, its rank among cited entities, the response length, and latency, along with context-level annotations (sentiment valence, factual hedging, self-described attribution). Eight fictitious control entities (two per vertical) anchor the false-positive rate and allow correction for hallucinated name recall. We plan a pre-registered confirmatory analysis using mixed-effects logistic regression with random intercepts per query, Bayesian posterior intervals for per-model citation rates, and Benjamini–Hochberg FDR control across the multi-vertical comparison family. We discuss implications for the emerging field of Generative Engine Optimization (GEO) and release the dataset on Zenodo. The target sample at close is ~25,920 query–model observations.

**Word count (target):** 180–230. Current draft ≈ 225.

---

## 3. Research Questions (RQs)

- **RQ1.** Do commercial LLMs cite Brazilian commercial entities at rates that differ significantly across the four industry verticals (fintech, retail, healthcare, technology), after controlling for query type, query language, and model?
- **RQ2.** Given a fixed query, how consistent is a single LLM with itself across 90 days? (intra-model temporal stability)
- **RQ3.** Given a fixed query, how much do the five LLMs agree with each other on the set of cited entities? (inter-model agreement, measured by Fleiss' kappa)
- **RQ4.** Does the false-positive rate for fictitious cohort entities differ across verticals and across models, and does hallucinated-name recall correlate with the model's reported confidence (hedging density)?
- **RQ5.** Do directive queries ("best digital bank in Brazil") produce systematically higher citation rates than exploratory queries ("how should I pick a digital bank"), and does this effect interact with vertical?

---

## 4. Hypotheses (pre-registration target: abril/2026)

Each hypothesis states a direction, an operational test, and the minimum effect size we treat as substantively meaningful.

- **H1 (vertical asymmetry).** Citation rates differ across verticals with fintech highest and healthcare lowest. Operationalized as a likelihood-ratio test of the `vertical` fixed effect in the mixed-effects logit model. Minimum substantively meaningful effect: Cramér's V ≥ 0.15 on the aggregated 4×2 contingency table.
- **H2 (intra-model drift).** At least one of the five LLMs exhibits a non-stationary citation rate across the 90-day window, detected as a significant slope of `cited ~ day_index` per model after FDR correction (α' = 0.05/5).
- **H3 (inter-model agreement).** Fleiss' kappa across the five LLMs, computed on the rectangular panel of (query × model) decisions, is > 0.40 (Landis–Koch "moderate") for fintech and retail, and ≤ 0.40 for healthcare. Rationale: regulatory discourse homogenizes fintech reporting corpora.
- **H4 (fictitious calibration).** False-positive rate on fictitious entities is strictly below 5% for every model, and differs significantly across models (Kruskal–Wallis on per-model FPR).
- **H5 (directive inflation).** Directive queries yield ≥ 15 percentage points higher citation rates than exploratory queries, averaged across verticals (Cohen's h as effect size).
- **H6 (hedging × accuracy).** Within a single LLM, responses containing hedging markers ("reportedly", "segundo", "may be") have lower factual accuracy than non-hedged responses on the five manually verifiable entities (Nubank, PagBank, Banco Inter, Stone, C6 Bank). One-sided t-test on accuracy scores.

**Stopping rule:** we freeze the cohort, query battery, and statistical plan at pre-registration (abril/2026); any post-hoc analysis is labeled exploratory in §7 (Results) and reported without inferential claims.

---

## 5. Methods

### 5.1 Sample

- **Entities:** 69 total — 61 real commercial entities plus 8 fictitious controls (2 per vertical) — distributed across four verticals (fintech n=21, retail n=16, healthcare n=16, technology n=16). Five international fintechs (Revolut, Monzo, N26, Chime, Wise) are included as cross-market anchors.
- **LLMs:** 5 commercial providers — GPT-4o-mini (`gpt-4o-mini-2024-07-18`), Claude Haiku 4.5 (`claude-haiku-4-5-20251001`), Gemini 2.5 Pro (`gemini-2.5-pro`), Perplexity Sonar (`sonar`), Groq Llama 3.3 70B (`llama-3.3-70b-versatile`).
- **Query battery:** ~24 canonical queries per vertical, stratified across 8+ categories (discovery, comparative, trust, product, b2b, reputation, directive, exploratory) and two languages (pt-BR, en-US). Queries are frozen at pre-registration.
- **Collection cadence:** 2× per day (06:00 and 18:00 BRT) via `.github/workflows/daily-collect.yml` for 90 calendar days.
- **Target observations at close:** 4 verticals × ~24 queries × 5 LLMs × 2 runs/day × 90 days ≈ 25,920 unit observations. Realized sample will be reported in §7 net of cache deduplication (SHA-256 response cache with 20h TTL; identical responses are not counted as independent observations for inferential purposes).
- **Preliminary snapshot (2026-04-19, N=4,148, 75.8% aggregate citation rate):** reported as descriptive preliminary, explicitly flagged as non-confirmatory in §7.1.

### 5.2 Data collection pipeline

Reproducible pipeline documented in `docs/ARCHITECTURE.md`. Key components:

- **Source of truth.** SQLite database `data/papers.db` versioned in git (protection against artifact loss; see incident 2026-03-29 in `docs/INCIDENT_PIPELINE_2026-03-29.md`).
- **Orchestration.** `src/cli.py` (Click) drives `citation_tracker` (Module 1), `competitor` (Module 2), `context_analyzer` (Module 7), `timeseries` (Module 5).
- **LLM client.** `src/collectors/llm_client.py` dispatches to each provider with shared `ResponseCache` (SHA-256, TTL 20h) and per-call FinOps tracking (`src/finops/tracker.py`).
- **Schema.** 22 tables; primary analytical table is `citations` with columns `vertical`, `llm`, `model`, `model_version`, `query_type`, `query_lang`, `cited`, `cited_entity`, `cited_entities_json`, `position`, `attribution`, `response_text`, `hedging_detected`, `fictional_hit`. Migrations 0003 (query_type + 5 composite indexes + backfills) and 0004 (fictional_hit + retroactive backfill) are idempotent.
- **Health gating.** `scripts/health_check.py` fails the pipeline on under-collection; `MANDATORY_LLMS` env var forces a fail-loud on missing providers to protect N-balance.
- **Publication artifacts.** Dataset exported via `scripts/export_data.py` to JSON, CSV, HTML; synced read-only to Supabase; Zenodo DOI at submission.

### 5.3 Statistical plan

Layered from primary confirmatory (H1–H6) to sensitivity analyses.

**Primary inference — mixed-effects logistic regression** (per RQ1, RQ5):

```
logit P(cited = 1) = β0 + β_vertical + β_model + β_query_type + β_lang
                   + β_vertical × query_type
                   + u_query + u_entity
```

Fitted in `statsmodels.MixedLM` (or `pymer4` for comparison) with random intercepts for `query_id` and `entity_id` to respect repeated measures. Effect sizes reported as odds ratios with profile-likelihood 95% CIs. Model comparison via AIC and likelihood-ratio tests against the null (intercept + model only).

**Per-model citation rate — Bayesian Beta-binomial** (per RQ4):

`StatisticalAnalyzer.beta_binomial_ci` (already implemented, `docs/METHODOLOGY.md` §10.2) with uniform prior Beta(1,1), reporting posterior mean and 95% credible interval. Preferred over Wald for small cells (e.g., Gemini N=30 at snapshot).

**Inter-model agreement — Fleiss' kappa** (per RQ3):

`StatisticalAnalyzer.fleiss_kappa` over the rectangular panel of binary `cited` decisions per query, interpreted via Landis & Koch (1977). Cohen's kappa reported for every pairwise model combination.

**Multi-group vertical comparison** (per RQ1):

ANOVA if Levene's test supports homogeneity of variances (`p > 0.05`), otherwise Kruskal–Wallis. Effect size η² classified per Cohen. Fisher's exact fallback triggered automatically when any expected cell count < 5 (implemented, METHODOLOGY §10.4).

**Multiple-comparison control:**

- **Family 1 (four-vertical pairwise).** 6 comparisons → Bonferroni (conservative, FWER-controlling).
- **Family 2 (per-entity, 69 entities).** Benjamini–Hochberg FDR at α = 0.05 (Benjamini & Hochberg, 1995).
- **Family 3 (per-model drift slopes, 5 models).** Bonferroni.

**Bayes factors:** BF₁₀ via Savage–Dickey ratio for the fixed effect of vertical; reported alongside frequentist tests (per Gelman panel review, METHODOLOGY §8). Interpretation thresholds follow Kass & Raftery (1995).

**Robustness and sensitivity:**

- **BCa bootstrap** (Efron, 1987) with B = 10,000 resamples for every reported point estimate (`StatisticalAnalyzer.bootstrap_ci_bca`, already implemented).
- **Cache-deduplicated sensitivity run:** re-run primary analysis with `N_eff` (excluding identical SHA-256 cache hits) to bound the impact of dependent observations.
- **Leave-one-model-out:** refit the mixed-effects model five times, each dropping one LLM, to gauge single-model leverage.
- **Directive/exploratory split:** H5 is tested as an interaction; results reported separately for each stratum.

**Effect size vocabulary.** Cohen's d for continuous, Cramér's V for nominal, Cohen's h for proportions, η² for ANOVA, Hedges's g for small-sample mean comparisons (Hedges, 1981). No dichotomization of p-values (per Gelman panel review).

### 5.4 Threats to validity and mitigations

Documented in full in `docs/METHODOLOGY.md` §7. Paper body will include a condensed Limitations section mirroring that table and flagging: query selection bias, LLM non-stationarity (mitigated by `model_version` column and H2 drift test), dependence across within-session queries (mitigated by cache-deduplicated sensitivity run), rule-based sentiment ceiling (§4.1 of METHODOLOGY).

---

## 6. Expected results structure (paper skeleton)

### §7.1 Descriptive landscape (preliminary / descriptive only)

- **Table 1.** Sample composition: entities × verticals × LLMs × queries × days, with realized vs. target N and cache-dedup ratio.
- **Table 2.** Aggregate citation rate by vertical × LLM (Beta-binomial posterior mean + 95% credible interval).
- **Figure 1.** Heatmap of citation rate: y = vertical, x = LLM, cell = posterior mean with CI bars.
- **Figure 2.** Temporal series: daily citation rate per LLM, 90 days, with LOESS smoothing.

### §7.2 Confirmatory inference (H1–H6)

- **Table 3.** Mixed-effects logit coefficients with ORs, 95% CIs, p-values, and Bayes factors — one row per fixed effect.
- **Table 4.** Multiple comparison results — pairwise vertical contrasts, Bonferroni-adjusted.
- **Figure 3.** Forest plot of per-model citation ORs vs. the grand mean, with Bayesian posterior intervals.
- **Table 5.** Fleiss' kappa global + Cohen's kappa pairwise matrix (5×5).
- **Figure 4.** Calibration plot: fictitious-entity FPR per model, with binomial 95% CIs (anchors RQ4 and H4).

### §7.3 Mechanism / exploratory

- **Table 6.** Hedging × accuracy contingency (H6) for five manually verifiable entities.
- **Figure 5.** Directive vs. exploratory citation-rate gap per vertical (H5 interaction).
- **Figure 6.** Drift detection: per-model slope of daily citation rate with confidence bands (H2).

### §7.4 Sensitivity and robustness

- **Table 7.** Leave-one-model-out refit summary.
- **Table 8.** Cache-deduplicated N_eff rerun summary.

---

## 7. Contribution statement

We contribute (i) the first published 90-day longitudinal dataset of commercial LLM citations spanning four industry verticals and five commercial providers, with open release on Zenodo; (ii) a methodologically defensible analytical pipeline combining mixed-effects regression, Bayesian posteriors, BCa bootstrap, and FDR control for a domain (Generative Engine Optimization / GEO) currently dominated by ad-hoc practitioner claims; (iii) an explicit false-positive calibration protocol via fictitious cohort entities, enabling correction for hallucinated-name recall; (iv) a reproducible open-source pipeline (Python, GitHub Actions, SQLite, Supabase) that other researchers can fork for their own verticals or markets. We position the paper as an IR-community empirical foundation for the emerging GEO literature and make explicit the boundary between descriptive (abril/2026 snapshot) and confirmatory (julho/2026 close) claims.

---

## 8. Target venue rationale

**arXiv `cs.IR`** chosen because:

- Moderated preprint, no APC, cross-post permitted for future journal submission (compatible with the downstream *Information Sciences* plan, Paper 3).
- IR community actively discusses retrieval-augmented generation and LLM citation fidelity (SIGIR Gen-IR workshops, 2024–2026).
- Immediate DOI via arXiv timestamp, plus Zenodo DOI for the dataset, satisfies open-science credit without blocking on a 6–12 month peer-review loop.
- Existing GEO / LLM-citation literature (Aggarwal et al., 2024; Bevendorff et al., 2025) already lives on arXiv cs.IR, so venue fit is native.

**Submission artifacts:**

- LaTeX source (ACM or arXiv standard template).
- Zenodo-hosted CSV dump of `citations` + `collection_runs` + `finops_usage`.
- GitHub tag `paper-1-submission` on this repository with pinned commit hash of `data/papers.db`.
- Pre-registration at OSF (planned abril/2026, per METHODOLOGY §11 roadmap).

---

## 9. References (selected, working list)

- Benjamini, Y., & Hochberg, Y. (1995). Controlling the false discovery rate. *JRSS-B*, 57(1).
- Efron, B. (1987). Better bootstrap confidence intervals. *JASA*, 82(397).
- Fleiss, J. L. (1971). Measuring nominal scale agreement among many raters. *Psychological Bulletin*, 76(5).
- Hedges, L. V. (1981). Distribution theory for Glass's estimator of effect size. *Journal of Educational Statistics*, 6(2).
- Kass, R. E., & Raftery, A. E. (1995). Bayes factors. *JASA*, 90(430).
- Landis, J. R., & Koch, G. G. (1977). The measurement of observer agreement for categorical data. *Biometrics*, 33(1).
- Aggarwal, P. et al. (2024). GEO: Generative Engine Optimization. arXiv:2311.09735.
- Bevendorff, J. et al. (2025). The LLM leaderboard for citation accuracy. arXiv preprint.

---

*Última revisão deste outline: 2026-04-21.*
*Autor responsável: Alexandre Caramaschi.*
*Dependências abertas: pré-registro OSF (abril/2026), fechamento de janela de coleta (06/07/2026), Zenodo DOI, voice review editorial.*
