# Preregistration — Paper 4 (OSF Secondary Data Analysis Template)

**Title:** Three Ways to Fail to Conclude: A Null-Report on LLM Citation Claims for Brazilian Brands (N=7,052, 12 days)

**Authors:** Alexandre Caramaschi (ORCID: 0009-0005-7856-7029)

**Affiliation:** Brasil GEO (independent research, self-funded)

**Template:** OSF Secondary Data Analysis (AsPredicted-style, extended)

**Version:** v1 — submitted 2026-04-24

**Status note (honesty clause):** Wave 4 of the audit pipeline performed exploratory descriptive statistics on this dataset. The analyses proposed in this preregistration are confirmatory rerruns of those same tests with stricter protocols (family-wise FDR, BCa bootstrap, cluster-robust SE) and formally committed interpretations. This is a *deferred preregistration* / *post-hoc preregistration* for secondary data analysis — following the OSF SDA template — with explicit acknowledgment that full blinding to results is impossible. The value of this document is constraining the degrees of freedom in the final analysis and committing to null-result interpretation rules *before* the confirmatory rerun.

---

## 1. Data Origin

Secondary analysis of a pre-existing dataset collected by the author between **2026-03-24 and 2026-04-22** (12 active days). Collection was automated via scheduled cron jobs in the `papers/` pipeline, querying four commercial LLM APIs with a fixed set of Brazilian brand prompts. The dataset is **frozen** at the time of this registration.

## 2. Existing Data — Prior Access

- The author has accessed the data.
- Wave 4 (exploratory) statistics have been computed and reviewed.
- Confirmatory reruns under the protocols below have **not** been executed.
- Snapshot tag `paper-4-dataset-closed` to be created on `papers.db` before analysis; SHA-256 of the SQLite file to be recorded in the final paper.

## 3. Data Access

- Repository: `github.com/[author]/papers` (public at publication).
- Dataset: `C:/Sandyboxclaude/papers/data/papers.db` (SQLite, tables `citations`, `runs`, `prompts`).
- Zenodo DOI: to be minted on paper submission.
- License: CC-BY 4.0 for data; MIT for code.

## 4. Hypotheses

All hypotheses are **directional** and stated with Null (H0) and Alternative (H1) explicitly.

**H1 — RAG advantage.** Perplexity (`sonar`, retrieval-augmented) cites target Brazilian brands at a higher rate than the mean of parametric-only models (OpenAI `gpt-4o-mini-2024-07-18`, Anthropic `claude-haiku-4-5-20251001`, Google `gemini-2.5-pro`).
- H0: p_perplexity ≤ mean(p_parametric)
- H1: p_perplexity > mean(p_parametric)

**H2 — Hallucination baseline.** The rate of `fictional_hit = 1` (citation of a fabricated brand from the control set) is non-zero across all four models.
- H0: p_fictional = 0 for each model
- H1: p_fictional > 0 for at least one model

**H3 — Cross-LLM citation overlap.** Jaccard similarity of the top-30 cited entities between any two models is low (< 0.30), indicating fragmented citation ecosystems.
- H0: median pairwise Jaccard(top-30) ≥ 0.30
- H1: median pairwise Jaccard(top-30) < 0.30

## 5. Dependent Variables

- **Primary:** `cited` (binary 0/1, table `citations`) — whether the target brand appeared in the model response for a given prompt-day.
- **Secondary a:** `fictional_hit` (binary 0/1) — whether a fabricated control brand was cited.
- **Secondary b:** `sources_json` token count (integer) — structural proxy for answer verbosity; used only as covariate, not as outcome.

## 6. Conditions / Groups

- **Model** (4 levels): `gpt-4o-mini-2024-07-18`, `claude-haiku-4-5-20251001`, `gemini-2.5-pro`, `sonar`.
- **Retrieval class** (2 levels): RAG {sonar} vs parametric {the other three}.
- **Day** (12 levels, cluster variable).
- **Groq excluded** due to instability in the collection window (documented in `INCIDENT_PIPELINE_2026-03-29.md`).

## 7. Analysis Plan

**Software:** Python 3.11; `statsmodels` 0.14, `scipy` 1.11, `numpy` 1.26, `arch` 6.2 (bootstrap). Seed `20260424` for all stochastic procedures.

**Models:**
- H1: logistic regression `cited ~ is_rag + prompt_fe + day_fe`, cluster-robust SE by `day`. Effect = marginal probability difference.
- H2: per-model Wilson 95% CI on `fictional_hit`. Reject H0 if lower bound > 0.
- H3: Jaccard top-30 for all 6 model pairs; report median and IQR; one-sided sign test against 0.30.

**Multiple comparisons:** Benjamini–Hochberg FDR at q = 0.05, applied to the family of 3 primary tests.

**Effect sizes:** reported with **95% BCa bootstrap CI, 10,000 resamples**, clustered at the day level.

**Decision rule:** A hypothesis is declared "supported" only if (a) BH-adjusted p < 0.05 **and** (b) the BCa 95% CI excludes the null. Any other outcome is reported as a **null result** with the full CI; we commit in advance not to reinterpret narrow misses as "trends".

## 8. Outliers and Exclusions

- Pre-registered exclusions: Groq model rows; prompts with `status != 'ok'`; days with fewer than 80% of scheduled API calls completed (pipeline health).
- No outlier trimming on the primary binary outcome.
- For token-count covariate: winsorize at the 99th percentile.
- Final N after exclusions expected near 7,052 rows (exact N to be reported in the paper with exclusion CONSORT-style flow).

## 9. Sample Size

N was **fixed before this preregistration** — the dataset is frozen and no further collection will occur for Paper 4. No power analysis is used to justify N *post hoc*. Instead, achieved precision (CI half-width) will be reported for each estimate, and underpowered comparisons will be explicitly labeled as such. This is consistent with the null-report framing of the paper.

## 10. Other — Disclosures

- **COI:** Alexandre Caramaschi is founder/CEO of Brasil GEO, a consultancy whose commercial narrative could benefit from findings about LLM citation gaps. This paper reports a null/mixed result that *does not* directly support commercial claims; the preregistration is specifically designed to discipline the interpretation against motivated reasoning.
- **Funding:** Self-funded. No external grants, no sponsor review.
- **Ethics:** No human subjects. Only public commercial LLM APIs queried under their terms of service. No PII collected.
- **Incentives:** None beyond academic publication and personal portfolio.

## 11. Changelog

- **v1 (2026-04-24):** Initial submission. Any subsequent modifications will be versioned (v2, v3, …) with a dated diff and written justification appended to this document. Changes made *after* seeing confirmatory results will be flagged as exploratory.

---

## Checklist — What to Submit to OSF

- [ ] Create OSF project "Paper 4 — Null-Report LLM Citations BR"
- [ ] Upload this file as **Preregistration** component
- [ ] Choose template: **Secondary Data Analysis Registration** (not Registered Report — analysis is post-access)
- [ ] Mark registration as **deferred / post-hoc** in the optional narrative field
- [ ] Attach `papers.db` SHA-256 and git tag `paper-4-dataset-closed`
- [ ] Link GitHub repo (public) and reserve Zenodo DOI
- [ ] Set embargo: none (open from day 1)
- [ ] Confirm COI, funding, ethics fields on the OSF form match Section 10
- [ ] Freeze registration (immutable) **before** running the confirmatory analysis script
- [ ] Record OSF registration DOI in the paper's Methods section

**Decision: Deferred Preregistration (SDA), not Registered Report.** A full Registered Report requires pre-data-access commitment and Stage-1 peer review, which is not feasible here. The SDA deferred path is the honest, template-appropriate choice.
