# Paper 3 — Industry-Specific Patterns in AI Citation: A Multi-Vertical Econometric Analysis

**Target venue:** *Information Sciences* (Elsevier, Q1; SJR 2.2, JCR IF ≈ 8.1).
**Status:** outline only; depends on 90-day coleta consolidada (fechamento 06/07/2026) e agregação econométrica posterior.
**Draft target:** outubro/2026 (submissão dezembro/2026). Cruza com Paper 1 (arXiv) como preprint de referência.
**Autor:** Alexandre Caramaschi (Brasil GEO).

---

## 1. Title

**Primary title (working):**
> Industry-Specific Patterns in AI Citation Behavior: A Multi-Vertical Econometric Analysis of Large Language Models

**Alternative (Q1-journal friendly, emphasizing contribution):**
> Why Do Large Language Models Cite Some Industries More Than Others? A Longitudinal Multi-Vertical Study With an Open Dataset

---

## 2. Abstract (target 200–250 words, structured per *Information Sciences* convention: Purpose / Methods / Findings / Value)

> **Purpose.** As large language models (LLMs) become the primary interface through which consumers discover commercial entities, the structural determinants of which entities are surfaced remain underdetermined. We ask why fintech entities are cited at systematically different rates than healthcare entities by the same LLMs answering the same class of questions, and we isolate the contribution of entity-level attributes (Wikidata knowledge graph richness, Wikipedia article presence, brand age, estimated revenue, regulatory exposure) from model-level effects.
>
> **Methods.** We analyze a longitudinal panel of approximately 25,000 query–model observations collected over 90 days from five commercial LLMs (OpenAI GPT-4o-mini, Anthropic Claude Haiku 4.5, Google Gemini 2.5, Perplexity Sonar, Groq Llama 3.3 70B) probed with a frozen battery of canonical queries spanning 69 entities in four industry verticals (fintech, retail, healthcare, technology). Our primary specification is a mixed-effects logistic regression of the binary citation event on entity-level covariates with random intercepts per query and per LLM. Multiple testing is controlled via Benjamini–Hochberg FDR; robustness is assessed via BCa bootstrap (B = 10,000), leave-one-LLM-out refits, and a pre-registered sensitivity analysis excluding fictitious-control entities.
>
> **Findings.** We report effect sizes in odds-ratio form for every entity-level covariate and identify which industry-level features mediate the vertical asymmetry. Findings are presented with explicit Bayesian posterior intervals alongside frequentist tests.
>
> **Value.** This study provides the first open, reproducible, multi-vertical empirical foundation for Generative Engine Optimization (GEO) research, releases the full dataset on Zenodo under CC-BY-4.0, and publishes a reusable Python pipeline (GitHub Actions + SQLite + Supabase) under MIT licensing. No human subjects were involved; all data derive from public LLM APIs.

**Word count target:** 200–250. Current ≈ 245.

---

## 3. Research questions

- **RQ1.** Does industry vertical remain a significant predictor of LLM citation rate *after* controlling for entity-level attributes (brand age, estimated revenue proxy, Wikidata QID richness, Wikipedia presence, academic reference density, presence in regulated financial registries)?
- **RQ2.** Which entity-level attribute carries the largest odds-ratio effect on citation probability, and is the ranking of attributes stable across the five LLMs?
- **RQ3.** Does regulatory discourse exposure (proxied by presence in Banco Central / ANS / ANVISA / Receita Federal public registries) differentially predict citation in regulated verticals (fintech, healthcare) vs. unregulated (retail, technology)?
- **RQ4.** Over the 90-day window, do entity-level effect sizes drift, and is any drift correlated with public events (product launches, regulatory actions, news coverage)?

---

## 4. Hypotheses (pre-registered, abril/2026)

- **H1.** After controlling for entity-level attributes, vertical remains a significant fixed effect in the mixed-effects logit (ΔAIC > 10 vs. nested model without vertical).
- **H2.** Wikidata QID richness (number of statements) is the single largest odds-ratio predictor of citation (OR ≥ 1.4 per standard-deviation increase) across all five LLMs.
- **H3.** Regulatory registry presence interacts with vertical: the effect of regulatory presence is positive in fintech, positive in healthcare, and null or negative in retail and technology.
- **H4.** Brand age (years since founding) is positively associated with citation, but the effect is attenuated for models with more recent training cutoffs.
- **H5.** Fictitious control entities have a false-positive citation rate < 5% across all models; any deviation is concentrated in specific LLMs.
- **H6.** The dominant source of variance in citation probability is entity-level (> 50% of total variance component in the mixed-effects decomposition), not query-level or model-level.

---

## 5. Methods

### 5.1 Sample and design

Reuses the full Paper 1 longitudinal panel (see `PAPER_1_VERTICAL_CITATION.md` §5.1) — 69 entities, 5 LLMs, ~96 queries, 2×/day for 90 days, N ≈ 25,920 at close. Paper 3 adds the entity-level covariate layer described below.

### 5.2 Entity-level covariates

Collected once per entity at pre-registration and re-snapshotted at end of coleta. All covariates are stored in a new `entity_attributes` table (schema addition planned, non-breaking).

| Covariate | Source | Type | Rationale |
|-----------|--------|------|-----------|
| `brand_age_years` | Receita Federal / corporate filings | continuous | Older brands have more training-data exposure |
| `revenue_proxy_log` | Public filings / industry reports | continuous log-USD | Market weight correlates with coverage |
| `wikidata_statements` | Wikidata SPARQL endpoint | integer | Knowledge graph richness |
| `wikipedia_present` | Wikipedia API (pt and en) | binary per-language | Wikipedia is a high-weight LLM training source |
| `wikipedia_revisions_12mo` | Wikipedia API | integer | Active editing proxies salience |
| `academic_refs_count` | Google Scholar / OpenAlex | integer | Academic citations proxy authority |
| `regulatory_registered` | Banco Central, ANS, ANVISA, CVM public lists | binary | Regulatory discourse hypothesis |
| `news_mentions_90d` | GDELT / Google News API | integer | Recency proxy |
| `schema_org_density` | site crawl | integer | SEO / GEO optimization proxy |
| `language_dominance` | domain ccTLD + primary-language heuristic | categorical (pt/en/mixed) | Language asymmetry |

Missing data policy: covariates with > 20% missingness are excluded from primary specification and reported only in exploratory §7.4. Others imputed via median (continuous) or "unknown" level (categorical), with a sensitivity analysis refitting on complete cases only.

### 5.3 Statistical plan

**Primary specification — mixed-effects logistic regression:**

```
logit P(cited_ijk = 1) = β_vertical_i
                      + β_attributes_i · X_entity_i
                      + β_query_type_j + β_lang_j
                      + β_model_k
                      + u_entity_i + u_query_j + u_model_k
```

Fitted in `statsmodels.MixedLM` with lme4-compatible formula via `pymer4` for cross-validation. Variance decomposition reported via intraclass correlation coefficients (ICC) for entity, query, and model levels (addresses H6).

**Effect sizes:** odds ratios with 95% profile-likelihood CIs + Bayesian posterior intervals via `pymc` logit with weakly-informative priors (Normal(0, 2.5) for coefficients, Cauchy(0, 1) for variance components, per Gelman et al. 2008).

**Multiple testing:** Benjamini–Hochberg FDR across the 10+ covariate family, α = 0.05. Family-wise Bonferroni for the 4 hypothesis-level tests.

**Hedges's g** (Hedges, 1981) for small-sample standardized mean differences in sub-vertical comparisons.

**Robustness / sensitivity:**

- BCa bootstrap (B = 10,000) for every reported OR.
- Leave-one-LLM-out refit (5 refits).
- Complete-case sensitivity (exclude imputed rows).
- Fictitious-entity exclusion rerun (H5 robustness).
- Pre/post split: first 45 days vs. last 45 days to detect drift (addresses H4 of Paper 1 at Paper 3 granularity).
- Bootstrapped variance component decomposition to bound H6.

**Causal caveats.** We do not claim causation. Associations are interpreted as conditional on the observed covariate set; unmeasured confounders (e.g., training-data inclusion, undisclosed prompt-engineering) are discussed in §6.

### 5.4 Open dataset

Final dataset released on **Zenodo** under CC-BY-4.0:

- `citations.csv` — full longitudinal panel, ~25K rows.
- `citation_context.csv` — sentiment, hedging, attribution.
- `entity_attributes.csv` — the 10-column covariate table described above.
- `collection_runs.csv` — pipeline metadata with commit hashes.
- `finops_usage.csv` — per-call cost tracking (reproducibility for cost estimates).
- `data_dictionary.md` — column-by-column definitions.
- `zenodo_metadata.json` — DOI, license, ORCID.

Alexandre Caramaschi's Zenodo account was created in abril/2026 specifically for this release. A Zenodo DOI will be minted at preprint posting (Paper 1 on arXiv) and re-used across all three papers, guaranteeing cross-referential integrity.

### 5.5 Code and pipeline

Full source code on GitHub (`alexandrebrt14-sys/papers`) under MIT. Every figure in the paper is regenerable from the Zenodo dataset via `scripts/export_data.py` + `src/analysis/visualization.py`. A `DOCKERFILE` and a `reproduce.sh` entry point will ship with the preprint; Binder notebook planned if reviewer asks.

### 5.6 Ethics

**No IRB approval required.** The study relies exclusively on:

- Public APIs of commercial LLM providers, accessed under their commercial terms of service.
- Public knowledge graphs (Wikidata), encyclopedias (Wikipedia), and government registries (Banco Central, ANS, ANVISA, CVM).
- No human subjects, no survey responses, no user-generated content beyond publicly indexed corporate entities.

The commercial-entity corpus is public business information. Fictitious control entities are explicitly labeled; we do not publish under those names. A data-use statement in the paper will reaffirm the no-human-subjects posture.

### 5.7 Threats to validity

- **Unmeasured confounders** (training-data composition, LLM update cadence) — acknowledged, partially mitigated by `model_version` column and longitudinal drift tests.
- **Ceiling / floor effects** on entities with universal citation (Nubank ~100%) or near-zero citation (small healthcare players) — addressed via Bayesian Beta-binomial intervals that handle k=0, k=n cases correctly (METHODOLOGY §10.2).
- **Generalization to non-Brazilian markets** — explicitly out of scope; five international fintechs are included as anchors but not as inferential sample.
- **LLM non-stationarity** — flagged as Paper 1 H2 and carried over as a sensitivity split in §5.3 above.

---

## 6. Expected results structure

### §7.1 Sample and descriptive covariate landscape

- **Table 1.** Entity-level covariate summary (mean/median/IQR per vertical).
- **Figure 1.** Correlation matrix of entity covariates (Spearman).

### §7.2 Primary inference (H1–H6)

- **Table 2.** Full mixed-effects coefficient table with ORs, 95% profile CIs, Bayesian 95% credible intervals, BH-adjusted p-values.
- **Figure 2.** Forest plot of covariate ORs by LLM.
- **Table 3.** ICC decomposition: entity-level / query-level / model-level variance.

### §7.3 Interactions and mechanism

- **Figure 3.** Interaction plot: regulatory registry × vertical (H3).
- **Table 4.** Brand-age OR by LLM training-cutoff year (H4).
- **Table 5.** Fictitious-entity FPR per LLM with binomial 95% CI (H5).

### §7.4 Robustness

- **Table 6.** Leave-one-LLM-out coefficient stability.
- **Table 7.** Pre/post-45-day drift in effect sizes.
- **Figure 4.** BCa bootstrap density of the top-three ORs.

---

## 7. Contribution statement

Paper 3 is positioned as the **confirmatory, mechanism-oriented** companion to Paper 1 (descriptive arXiv preprint) and Paper 2 (workshop overlap study). Its novel contributions are:

1. **Econometric decomposition** of LLM citation behavior, isolating entity-level from model-level effects via mixed-effects logit with ICC variance decomposition. No prior published study has done this on a multi-vertical panel of this size.
2. **Regulatory-discourse hypothesis** (H3) — testable, operationalized, and falsifiable via the Banco Central/ANS/ANVISA/CVM registry merge.
3. **Open, fully reproducible dataset** on Zenodo under CC-BY-4.0, enabling secondary analysis by other IR and marketing-science researchers. Dataset DOI + code commit hash in the paper body.
4. **Methodological contribution**: the fictitious-entity calibration protocol (as operationalized in the Paper 1 pipeline and extended here to verify the non-inflation of odds ratios) is a reusable primitive for GEO-adjacent research.
5. **Practitioner relevance**: we explicitly discuss actionable implications for content strategy, knowledge-graph optimization, and the "Wikidata investment" question that GEO practitioners currently address with ad-hoc heuristics.

---

## 8. Target venue rationale — Why *Information Sciences* (Elsevier, Q1)

- **SJR 2.2, JCR IF ≈ 8.1** (2024 metrics). Comfortably Q1 in Information Systems.
- **Scope match.** *Information Sciences* explicitly publishes on AI evaluation, knowledge representation, and information behavior empirical studies. Our econometric panel fits the "empirical contribution with open dataset" profile the journal favors.
- **Open-access option** (gold OA, APC ≈ USD 2,700). Alexandre has budgeted the APC; gold OA eliminates any paywall concern for the dataset-backed companion.
- **Review timeline:** typical 3–6 months to first decision, 9–14 months to acceptance. Compatible with submission dezembro/2026 and acceptance by end of 2027.
- **Cross-post compatibility.** *Information Sciences* explicitly allows arXiv preprint co-existence — Paper 1 on arXiv does not block Paper 3 submission.

**Why Q1 and not Q2:**

- The study contributes an **original** empirical foundation (no prior multi-vertical longitudinal LLM-citation panel exists in the open literature).
- The **dataset is public** (CC-BY-4.0, Zenodo DOI), satisfying open-science priorities that Q1 venues increasingly demand.
- **Effect sizes are substantive** (we target ORs and ICCs with substantive, not merely statistical, significance; see Gelman panel review in METHODOLOGY §8).
- **Methodological rigor** — mixed-effects with ICC decomposition, BCa bootstrap, Bayesian posteriors, FDR control — meets the bar of Q1 reviewers in the Information Systems subfield.

**Backup venues (if Information Sciences rejects):**

1. *Journal of Information Science* (Sage, Q1 IS, IF ≈ 3.2) — tighter IR focus.
2. *Expert Systems with Applications* (Elsevier, Q1, IF ≈ 8.5) — AI-forward audience.
3. *International Journal of Information Management* (Elsevier, Q1, IF ≈ 21.0) — management-oriented but accepts empirical IS work.
4. *Information Processing & Management* (Elsevier, Q1, IF ≈ 8.6) — classical IR venue, also a strong fit.

---

## 9. References (selected)

- Benjamini, Y., & Hochberg, Y. (1995). Controlling the false discovery rate. *JRSS-B*, 57(1).
- Efron, B. (1987). Better bootstrap confidence intervals. *JASA*, 82(397).
- Gelman, A., Jakulin, A., Pittau, M. G., & Su, Y.-S. (2008). A weakly informative default prior distribution for logistic and other regression models. *Annals of Applied Statistics*, 2(4).
- Hedges, L. V. (1981). Distribution theory for Glass's estimator of effect size. *Journal of Educational Statistics*, 6(2).
- Snijders, T. A. B., & Bosker, R. J. (2012). *Multilevel Analysis* (2nd ed.). Sage.
- Vrandečić, D., & Krötzsch, M. (2014). Wikidata: a free collaborative knowledgebase. *CACM*, 57(10).
- Aggarwal, P. et al. (2024). GEO: Generative Engine Optimization. arXiv:2311.09735.
- Mollick, E. (2024). On LLM evaluation reproducibility. *Harvard Business Review / Oneusefulthing*.

---

*Última revisão deste outline: 2026-04-21.*
*Autor responsável: Alexandre Caramaschi.*
*Dependências abertas: fechamento de janela 06/07/2026 (Paper 1), consolidação `entity_attributes` table (mai–jun/2026), Zenodo DOI, APC orçado (USD 2,700), review editorial final.*
