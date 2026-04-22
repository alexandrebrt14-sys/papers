# Paper 2 — GEO vs SEO: Source Divergence Between Generative and Traditional Search

**Target venue:** SIGIR Gen-IR workshop (2027) ou WWW Companion Posters (2027). Workshop-track como entrada comunitária de IR.
**Status:** outline; coleta SERP ainda não ativada em produção (toggle `ENABLE_SERP_OVERLAP=true` pronto, aguardando start de coleta).
**Draft target:** outubro–novembro/2026 (após 12+ semanas de SERP pareado).
**Autor:** Alexandre Caramaschi (Brasil GEO).

---

## 1. Title

**Primary title (working):**
> GEO vs. SEO: Measuring Source Divergence Between Generative LLM Citations and Traditional Search Engine Rankings

**Alternative (poster-compact):**
> How Far Do LLM Citations Drift From Google's Top-10? A Multi-Vertical Overlap Study

---

## 2. Abstract (target 150–200 words, workshop-length)

> As large language models increasingly act as consumer-facing answer engines, the set of entities they cite is quietly displacing the traditional Search Engine Results Page (SERP) as the first surface a user encounters. This short paper quantifies the gap. We run 96 canonical queries across four industry verticals (fintech, retail, healthcare, technology) against both (i) a standardized Brave Search SERP and (ii) five commercial LLMs (OpenAI GPT-4o-mini, Anthropic Claude Haiku 4.5, Google Gemini 2.5, Perplexity Sonar, Groq Llama 3.3), pairing every SERP response with the LLM answers produced within the same hour. For each query we compute (a) the Jaccard overlap of the SERP top-10 entity set with the LLM-cited entity set, (b) the Kendall tau rank correlation between SERP rank and LLM position, and (c) the displacement metric Δ = (entities cited by LLM but absent from top-10 SERP) / (|LLM citations|). Preliminary evidence suggests fintech and healthcare behave asymmetrically, motivating a pre-registered confirmatory analysis once 12 weeks of paired panels are available. We release paired data on Zenodo and discuss implications for IR practitioners, content strategists, and GEO research.

**Word count (target):** 150–200. Current ≈ 200.

---

## 3. Research questions

- **RQ1.** What is the average Jaccard overlap between the SERP top-10 entity set and the LLM-cited entity set across the four verticals? Does it differ significantly across verticals?
- **RQ2.** For queries where both the SERP and the LLM name at least one common entity, how strong is the rank correlation (Kendall tau) between SERP position and LLM citation position?
- **RQ3.** Which LLM shows the highest divergence from SERP (Δ), and is divergence explained by the presence of retrieval augmentation (Perplexity Sonar explicitly grounded vs. others)?
- **RQ4.** Do entities that are cited by LLMs but absent from SERP top-10 share measurable attributes (Wikidata QID presence, Wikipedia article, academic mentions)?

---

## 4. Hypotheses

- **H1.** Mean Jaccard(SERP top-10, LLM citations) ≤ 0.35, i.e., meaningful divergence.
- **H2.** Perplexity Sonar (explicitly retrieval-augmented) has higher Jaccard with SERP than the non-retrieval-augmented LLMs (one-sided contrast).
- **H3.** Kendall tau between SERP rank and LLM position, computed on the intersection set, is positive but weak (0.1 ≤ τ ≤ 0.4), indicating that LLMs preserve some SERP signal but not rank order.
- **H4.** Δ is higher in healthcare than in fintech, driven by SERP being dominated by regulatory portals while LLMs lean on brand-aware corpora.

---

## 5. Methods

### 5.1 Entity cohort and query battery

Reuse the 69-entity cohort and ~96-query battery from Paper 1 (`src/config.py`) unchanged. This keeps Paper 2 fully comparable with Paper 1 descriptors and reuses the same cohort-matching regex (canonical forms + word-boundary for ambiguous short names like "Neon", "Stone", "99").

### 5.2 SERP collection

Implemented in `src/collectors/brave_search.py` (`BraveSearchClient`) and `src/collectors/serp_overlap.py` (Module 3). Activation gate: `ENABLE_SERP_OVERLAP=true` + `BRAVE_API_KEY` in GitHub Actions environment. Free-tier quota: 2,000 req/month (sufficient for 96 queries × 2 dispatches/day × 12 weeks = 1,614 req/quarter for pt-BR only; en-US will be added when paid tier is budgeted).

For each query we record:

- Top-10 organic URLs and their extracted domains.
- Extracted entity per URL (normalized via the same cohort regex used in citation tracking).
- Request timestamp aligned within ±60 minutes of the LLM dispatch for that query.

Storage: `serp_ai_overlap` table in `data/papers.db` (schema already present, empty until toggle is flipped).

### 5.3 LLM collection

Unchanged from the Paper 1 pipeline — same 5 LLMs, same query battery, same `citations` table. For Paper 2, we pair every SERP run with all five LLM responses produced in the same six-hour collection window.

### 5.4 Divergence metrics

For each (query, model) pair let **S** = SERP top-10 entity set, **L** = LLM-cited entity set.

- **Jaccard overlap:** J = |S ∩ L| / |S ∪ L|.
- **Coverage:** C = |S ∩ L| / |L| (fraction of LLM citations that also appear in SERP top-10).
- **Displacement:** Δ = |L \\ S| / |L| (fraction of LLM citations absent from SERP top-10).
- **Rank correlation:** Kendall tau between `serp_rank` and `llm_position` on the intersection S ∩ L (tie-corrected, τ_b).
- **Normalized Discounted Cumulative Gain:** nDCG@10 of the LLM-cited ordering, treating SERP top-10 as the relevance graded list.

All metrics computed per (vertical, LLM, query_type) stratum.

### 5.5 Statistical plan

- **Primary inference:** mixed-effects Beta regression of J on fixed effects `vertical`, `llm`, `query_type`, with random intercept per query. Reported as effect sizes + 95% profile-likelihood CIs. Beta regression chosen because J ∈ (0, 1) and skewed.
- **Pairwise LLM contrasts:** Wilcoxon signed-rank on within-query J differences, Bonferroni-corrected across the 10 LLM pairs.
- **Per-vertical BCa bootstrap** (B = 10,000) of mean J, mean Δ, mean τ.
- **Multiple testing:** Benjamini–Hochberg FDR across the per-query family (96 queries × 5 LLMs = 480 tests).
- **Sensitivity:** refit primary Beta regression excluding Perplexity Sonar (explicit retrieval-augmented) to confirm that overall divergence is not driven by a single outlier model.

### 5.6 Threats to validity

- **SERP provider bias.** Brave Search ≠ Google. We explicitly frame Brave as a proxy and plan a smaller paired validation against Google Programmable Search (250 req/day free tier) on a subsample. Reported as a robustness check, not a primary finding.
- **Temporal non-alignment.** SERP and LLM dispatches are aligned within ±60 minutes; we will report a sensitivity analysis using ±15 minute alignment.
- **Language drift.** pt-BR SERP results for Brazilian entities may differ substantially from en-US. We report per-language strata and plan to cover both in v2.

---

## 6. Expected results structure

- **Table 1.** Sample: 96 queries × 5 LLMs × ~12 weeks × ~84 runs paired with SERP, with realized N.
- **Table 2.** Mean Jaccard, coverage, and Δ per vertical × LLM with BCa 95% CIs.
- **Figure 1.** Heatmap of mean Jaccard: y = vertical, x = LLM.
- **Table 3.** Beta regression coefficients (fixed effects + random variance component).
- **Figure 2.** Rank displacement scatter: SERP rank (x) vs. LLM position (y), one panel per LLM, with Kendall τ reported in each panel.
- **Table 4.** Attributes of "LLM-only" entities (cited by LLM, absent from SERP top-10): Wikidata QID richness, Wikipedia article present, academic reference density.
- **Figure 3.** Temporal stability of J across the 12-week window (addresses whether divergence is constant or drifting).

---

## 7. Contribution statement

We contribute (i) the first IR-community workshop study quantifying Jaccard and rank-level divergence between SERP top-10 and LLM citations, using a paired panel across four industry verticals and five LLMs; (ii) open, pairable datasets (SERP snapshots + LLM responses per query, same-hour) published on Zenodo; (iii) a reusable codebase (`src/collectors/serp_overlap.py`) that other teams can adapt for other markets. We explicitly frame the contribution as workshop-appropriate — descriptive-to-early-inferential — and use the feedback loop of the workshop community to refine the analysis before a full-journal submission.

---

## 8. Why a workshop and not a journal?

Workshops at SIGIR and WWW serve as IR community entry points for work still in methodological development. We choose workshop rather than journal because:

- **Early feedback matters.** Divergence metrics (Jaccard vs. Kendall vs. nDCG) have not been canonized for GEO-vs-SEO comparisons; workshop review will surface methodological objections faster than a 6-month journal loop.
- **Data in flight.** At workshop submission (abril/2027 for SIGIR 2027, janeiro/2027 for WWW 2027 Companion), we will have only 12–20 weeks of paired data. A workshop paper can report that sample honestly as "early evidence"; a journal referee typically rejects samples short of 12 months.
- **Lightweight format fits the scope.** Workshop short-paper (4–6 pages IR tracks) is the natural length for a focused overlap study. The full multi-vertical analysis with econometric controls lives in Paper 3 (Information Sciences).
- **Community cross-pollination.** Gen-IR in particular brings together researchers working on retrieval-augmented generation, citation fidelity, and LLM evaluation — the exact audience we want for feedback.

**Specific target venues, in order of preference:**

1. **SIGIR 2027 — Gen-IR (Generative Information Retrieval) Workshop** — short paper (4–6 pp) or position paper (2 pp). Co-located with main conference. Direct community fit.
2. **SIGIR 2027 — Industry Track** — if Gen-IR calendar slips; practitioner-oriented, accepts observational studies.
3. **The Web Conference 2027 (WWW) — Companion / Posters Track** — 2-page poster with mandatory demo or dataset artifact. Good match for the Zenodo-backed release.
4. **ACL 2027 — NewSumm or similar NLP workshop** — fallback if IR venues saturate.
5. **CIKM 2027 — short paper track** — broader venue, less GEO-specific but accepts IR empirical work.

---

## 9. References (selected)

- Aggarwal, P. et al. (2024). GEO: Generative Engine Optimization. arXiv:2311.09735.
- Ferrari Dacrema, M. et al. (2019). Are we really making much progress? (recsys reproducibility). *RecSys*.
- Bevendorff, J. et al. (2025). Measuring citation accuracy in generative search. arXiv.
- Kendall, M. G. (1938). A new measure of rank correlation. *Biometrika*, 30.
- Järvelin, K., & Kekäläinen, J. (2002). Cumulated gain-based evaluation of IR techniques. *ACM TOIS*, 20(4).
- Cribari-Neto, F., & Zeileis, A. (2010). Beta regression in R. *Journal of Statistical Software*, 34(2).

---

*Última revisão deste outline: 2026-04-21.*
*Autor responsável: Alexandre Caramaschi.*
*Dependências abertas: ativar `ENABLE_SERP_OVERLAP=true` em produção (abril/maio 2026), acumular 12 semanas de SERP pareado, validação amostral contra Google Programmable Search.*
