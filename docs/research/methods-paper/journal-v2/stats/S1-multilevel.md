# S1 — Multilevel model of entity citation in generative engines

**Analysis date.** 2026-09-11. **Script.** `s1_multilevel.py` (this directory). **Machine-readable output.** `s1_results.json`. **Runtime.** 1,596.7 s. **Environment.** Python 3.12.10, numpy 2.4.3, pandas 3.0.1, statsmodels 0.14.6, scipy 1.17.1.

**Database.** `C:/Sandyboxclaude/papers/data/papers.db`, opened with `sqlite3.connect("file:...?mode=ro", uri=True)`. Nothing was written to it at any point, and no git operation that alters state was run.

Every number in this document is produced by the script. Where an analysis did not run, or ran and did not hold still, the text says so and gives the evidence. Cells with fewer than 30 observations are marked `SMALL_N` and read as descriptive only.

---

## 1. What is modelled, and the four decisions that precede the model

### 1.1 Canonical cut and the uniform observation window

The canonical cut is `COALESCE(is_probe,0) = 0`: **68,624 responses**, six engine arms, 192 distinct prompts, four verticals, two languages, two query types, six query categories.

The outcome is **citation of at least one cohort entity inside a uniform 200-character observation window**. The stored column `cited_v2` is not that outcome for every arm. Five arms stored `text[:200]`, so `cited_v2` is already a 200-character measurement for them; Perplexity stored the whole response, so its `cited_v2` scans a mean of 668 characters. Comparing arms on `cited_v2` compares two different apertures.

The repair does not need a re-extraction. `first_entity_offset_v2` is the character offset of the *earliest* cohort entity in the response, so "at least one cohort entity begins inside the first 200 characters" is exactly

```
cited200 = 1  iff  cited_v2 = 1  AND  first_entity_offset_v2 < 200
```

This leaves every row in the analysis and, by construction, changes nothing in the five truncated arms.

**Table 1. What the uniform window changes, arm by arm.** *Caption: `native` is the outcome as stored; `uniform 200 (start rule)` is the primary outcome defined above; `strict boundary` additionally requires `first_entity_offset_v2 + len(first_entity_v2) <= 200`. All rates over the canonical cut. Source: `s1_results.json:design.window_asymmetry`.*

| Engine | n | Mean chars scored | Rate, native | Rate, uniform 200 (start rule) | Shift (pp) | Rate, strict boundary |
|---|---:|---:|---:|---:|---:|---:|
| ChatGPT | 15,168 | 200.0 | 0.17168 | 0.17168 | 0.00 | 0.17168 |
| Claude | 15,034 | 200.0 | 0.25748 | 0.25748 | 0.00 | 0.25649 |
| Gemini | 15,355 | 195.7 | 0.01856 | 0.01856 | 0.00 | 0.01856 |
| Grok | 1,118 | 200.0 | 0.29606 | 0.29606 | 0.00 | 0.29606 |
| Groq | 14,208 | 200.0 | 0.08516 | 0.08516 | 0.00 | 0.08312 |
| **Perplexity** | 7,741 | 668.0 | 0.74874 | **0.53779** | **21.10** | 0.52861 |

The five zero shifts are the identity operation applied to a string already 200 characters long. They are a check on the rule, not independent evidence about those arms. The one shift that matters is 21.10 points on Perplexity, which is roughly the gap between "Perplexity cites three times as often as ChatGPT" and "Perplexity cites 2.7 times as often as ChatGPT" — a difference large enough to change a procurement conversation.

The strict variant is reported to bracket the boundary decision, not to replace the primary rule. It is an approximation of "fully contained", because a match can be made through an alias shorter than the canonical name stored in `first_entity_v2`; that is why it perturbs Claude and Groq, whose stored text is already exactly 200 characters and therefore cannot contain a straddling match. The start rule does not have that defect and is the primary outcome here. **S2 reports 0.52035 for Perplexity** by re-running the extractor over `response_text[:200]`; the gap of 1.74 points against the start rule is entities that begin inside the window and end outside it. Neither figure is wrong — they answer "does an entity appear" and "does an entity fit". S1 uses the first, S2 the second, and any sentence in the manuscript that quotes a Perplexity level has to say which.

### 1.2 The collection day

A collection day is the **Brazilian local date, UTC−3**. The evening cron starts at 21:00 UTC and 7,598 observations land at 00:00–01:59 UTC, so a UTC calendar splits one collection round across two day-clusters. Under UTC−3 the series has **52 collection days**; under UTC it has 53. Robustness cut H re-runs the main model clustering on the UTC date and moves nothing.

### 1.3 The panel is not what the protocol describes, in four specific ways

**Perplexity never ran half the battery.** It has zero observations in `confianca`, `experiencia` and `inovacao`. Engine and query category are therefore **not crossed**, and any six-engine model fitted on all 192 prompts extrapolates Perplexity into three categories it never saw. The analysis handles this by splitting the design rather than by ignoring it:

| Design | Prompts | Engines | n | What it identifies |
|---|---:|---:|---:|---|
| **Core-3 balanced** (`comparativo`, `descoberta`, `mercado`) | 96 | 6 | **38,195** | Engine contrasts, fully crossed |
| Five-arm full battery (Perplexity dropped) | 192 | 5 | 60,883 | Category contrasts across all six categories |
| Full canonical | 192 | 6 | 68,624 | Neither cleanly; reported for completeness only |

Every engine comparison in this supplement runs on the core-3 balanced design. Every category comparison runs on the five-arm design.

**Eight of 52 days are partial.** A day is complete when every engine in panel that day covered its full battery — 96 prompts for Perplexity, 192 for the others. Incomplete: 2026-04-23, 05-27, 06-04, 06-05, 08-13, 08-23, 09-06, 09-07. **44 days are complete.** Only two of these (09-06, 09-07) appear in `data/partial_days.json`; that file's three remaining entries (09-10 twice, 09-11) postdate the database snapshot of 2026-09-08 and cannot be checked here.

**Byte-identical responses repeat inside a day.** The protocol argues that caching cannot enter the series, an 8-hour TTL against a 12-hour interval. `response_hash` disagrees: the canonical cut holds 68,624 rows carrying only **14,391 distinct response hashes**, and of the 22,495 `(engine, prompt, day)` cells with more than one run, **47.84 % are byte-identical across runs**.

| Engine | Cells with a repeat run | Byte-identical (%) |
|---|---:|---:|
| Groq | 4,800 | 71.88 |
| Claude | 4,927 | 60.60 |
| ChatGPT | 4,992 | 58.25 |
| Gemini | 4,992 | 28.37 |
| Perplexity | 2,592 | 0.04 |
| Grok | 192 | 0.00 |

Two readings survive. Either the short greedy decode is close to deterministic at the top of the answer, in which case the repeat is genuine but carries no new information; or something is serving a cached answer, in which case the repeat is not an observation at all. Both readings imply the same correction, so the argument need not be settled to act: robustness cut E collapses byte-identical repeats and refits. The zero values for Perplexity and Grok are informative on their own — those two arms almost never return the same first 200 characters twice.

**The panel composition changes twice.** Gemini switches from `gemini-2.5-pro` (2026-04-23 to 06-09, 10,939 rows) to `gemini-2.5-flash` (2026-08-08 to 09-08, 4,416 rows) across a 59-day collection gap. Groq leaves after 2026-08-16; Grok joins on 2026-08-23 and is observed on **5 collection days**. Robustness cuts C and D address both.

---

## 2. Method

### 2.1 The model

Let `y_i ∈ {0,1}` be the uniform-window outcome for response *i*, collected from engine `e(i)` on prompt `q(i)` on day `d(i)`. The primary model is a binomial GLMM with **crossed** random intercepts for prompt and collection day:

```
y_i  ~  Bernoulli(p_i)

logit(p_i) = β0
           + β_engine[e(i)]      (5 contrasts, reference ChatGPT)
           + β_vertical          (3 contrasts, reference fintech)
           + β_language          (1 contrast,  reference en)
           + β_querytype         (1 contrast,  reference directive)
           + β_category          (2 contrasts, reference comparativo)
           + u_q(i) + v_d(i)

u_q ~ N(0, σ²_query)     q = 1 … 96
v_d ~ N(0, σ²_day)       d = 1 … 52
u ⟂ v
```

The two groupings are crossed, not nested: every prompt recurs on every day and every day carries every prompt. The engine is a fixed factor in this model because six levels cannot identify a variance component — §4 shows what happens when one tries.

For the variance decomposition the fixed part is dropped to an engine-only term and the intraclass correlation is read on the latent scale,

```
ICC_ℓ = σ²_ℓ / ( Σ_k σ²_k + π²/3 ),
```

with `π²/3 ≈ 3.290` the residual variance of the standard logistic. At the entity level the unit becomes one *(response, candidate entity)* pair and a fourth grouping enters:

```
logit(p_{i,j}) = β0 + β_engine[e(i)] + b_j + u_q(i) + v_d(i),        b_j ~ N(0, σ²_entity)
```

where *j* ranges over the vertical's own roster of 27 or 28 candidates (real Brazilian companies plus international anchors; the extractor only searches within the query's vertical).

### 2.2 Estimation, and why three statistics appear for every effect

**M1 — GLMM by variational Bayes.** `statsmodels.BinomialBayesMixedGLM.fit_vb`. It converged on every specification reported here at full N; no specification had to be reduced by sampling for the response-level models. Its objective is an evidence lower bound, not a log-likelihood, so the fit cannot supply a likelihood-ratio test, and its mean-field posterior is known to understate uncertainty. M1 is therefore read for the *variance components and the point estimates*, not for its p-values.

`statsmodels` parameterises each component as `log σ`, so this analysis converts as `σ = exp(vcp_mean)` and `σ² = exp(2·vcp_mean)`, with `exp(vcp_mean ± 1.96·vcp_sd)` as the interval. This is worth stating because the repo's own wrapper, `src/analysis/mixed_effects.py`, stores `exp(vcp)` under the key `random_variances` when that quantity is a standard *deviation*. Anything downstream that read `random_variances` as a variance read `σ` for `σ²`.

**M2 — pooled logistic with two-way cluster-robust covariance.** The same fixed part, with a Cameron–Gelbach–Miller sandwich clustered simultaneously on prompt (96) and day (52), inference on `t(51)`. This is the **primary inferential anchor** of the supplement. Its standard errors are between 2.4 and 10.4 times the naive ones.

**LRT.** A textbook likelihood-ratio test is computed on the pooled likelihood and reported beside a **Rao–Scott first-order correction**, `LRT / d̄`, where `d̄ = trace(V_cluster V_naive⁻¹)/q` is the generalised design effect of the dropped block. The corrected version is the one to read; the naive version is printed so the reader can see the size of the correction.

**Block Wald.** Also reported as `F = W/q` on `(q, 51)` rather than χ² on `q`, because a χ² read of a cluster-robust Wald over-rejects with 52 clusters. Blocks wide relative to the cluster count are flagged `ANTICONSERVATIVE`; for those, the design-corrected LRT governs.

Reused from the existing analysis package rather than reimplemented: `benjamini_hochberg` (`hypothesis_engine.py`), `cluster_robust_mean` (`cluster_robust.py`), `cohens_h` (`power_analysis.py`), and the cohort definitions in `config_v2.py`.

### 2.3 Three intervals, three questions

Every descriptive rate carries three intervals because they answer different questions and disagree by nearly an order of magnitude.

*Wilson* treats the cell's rows as independent draws. They are not.

*Day-clustered* answers "if the same 96 prompts were run on new days". Because every collected day replicates the whole balanced battery, a day mean is a **stratified** mean and its interval is usually *narrower* than Wilson. A ratio below 1 is the expected result of the design, not a defect.

*Query-clustered* answers "if a new sample of prompts had been drawn". It runs 2 to 12 times wider than the binomial interval and is the one that governs any claim generalising beyond the 96 prompts actually used.

---

## 3. Results

### 3.1 Where the outcome sits

**Table 2. Citation rate by engine, core-3 balanced design (96 prompts, 52 days).** *Caption: `k` is the count of responses citing at least one cohort entity inside the first 200 characters. `day/iid` and `query/iid` are the ratios of the clustered standard error to the binomial one. Source: `s1_results.json:rates.overall_core3`.*

| Engine | n | k | Days | Rate | Wilson 95 % | Day-clustered 95 % | Query-clustered 95 % | day/iid | query/iid |
|---|---:|---:|---:|---:|---|---|---|---:|---:|
| Perplexity | 7,741 | 4,163 | 52 | 0.5378 | [0.5267, 0.5489] | [0.5226, 0.5530] | [0.4635, 0.6121] | 1.34 | 6.61 |
| Claude | 7,520 | 2,870 | 50 | 0.3816 | [0.3707, 0.3927] | [0.3767, 0.3866] | [0.2888, 0.4745] | 0.44 | 8.35 |
| Grok | 566 | 216 | **5** | 0.3816 | [0.3425, 0.4223] | [0.3446, 0.4186] | [0.2958, 0.4675] | 0.65 | 2.12 |
| ChatGPT | 7,584 | 1,511 | 50 | 0.1992 | [0.1904, 0.2084] | [0.1957, 0.2028] | [0.1235, 0.2750] | 0.38 | 8.32 |
| Groq | 7,104 | 1,002 | 47 | 0.1410 | [0.1331, 0.1493] | [0.1387, 0.1434] | [0.0742, 0.2079] | 0.29 | 8.15 |
| Gemini | 7,680 | 201 | 51 | 0.0262 | [0.0228, 0.0300] | [0.0193, 0.0330] | [0.0095, 0.0429] | 1.87 | 4.62 |

Grok's 566 observations clear the 30-row floor but rest on **five collection days** inside a two-and-a-half-week window. Its interval should be read as provisional regardless of its width; the cell-size rule does not flag it, and the day-cluster count is the reason it should be flagged anyway. Six query-clustered intervals in the full rate tables have negative lower bounds — ChatGPT/health, Gemini/fintech, Gemini/technology, Groq/health, Groq/technology and Gemini in Portuguese — because a Wald-type cluster-robust interval is unbounded on a rate near zero. Read those six as "indistinguishable from zero on a new sample of prompts"; do not truncate and quote the truncated bound.

The query-clustered columns carry the sharpest operational message in the table. Perplexity's citation rate is 53.8 % on this battery, but on a *newly drawn* battery from the same prompt population it is 46 % to 61 %. Any claim of the form "engine X cites Brazilian fintechs N % of the time" is a claim about a prompt sample, and the prompt sample dominates the sampling error.

### 3.2 The multilevel model

**Table 3. M1, primary GLMM on the core-3 balanced design (n = 38,195).** *Caption: binomial GLMM, crossed random intercepts for prompt and collection day, estimated by variational Bayes; converged. Reference cell is ChatGPT / fintech / English / directive / comparativo. Odds ratios with 95 % credible intervals from the variational posterior — see §2.2 on why these intervals are not the inferential anchor. Source: `s1_results.json:m1_glmm_core3`.*

| Term | β | SE | OR [95 % CrI] |
|---|---:|---:|---|
| Intercept | 0.5517 | 0.0169 | 1.736 [1.680, 1.795] |
| engine = Perplexity | 2.6735 | 0.0299 | 14.491 [13.666, 15.366] |
| engine = Claude | 1.5813 | 0.0309 | 4.861 [4.575, 5.165] |
| engine = Grok | 1.5536 | 0.1127 | 4.729 [3.791, 5.898] |
| engine = Groq | −0.7855 | 0.0475 | 0.456 [0.415, 0.500] |
| engine = Gemini | −4.1176 | 0.0847 | 0.016 [0.014, 0.019] |
| vertical = saude | −2.4520 | 0.0374 | 0.086 [0.080, 0.093] |
| vertical = tecnologia | −2.4537 | 0.0370 | 0.086 [0.080, 0.092] |
| vertical = varejo | −0.1349 | 0.0322 | 0.874 [0.820, 0.931] |
| language = pt | −0.1435 | 0.0239 | 0.866 [0.827, 0.908] |
| query type = exploratory | −2.5638 | 0.0264 | 0.077 [0.073, 0.081] |
| category = descoberta | −0.5253 | 0.0278 | 0.591 [0.560, 0.625] |
| category = mercado | −0.8288 | 0.0308 | 0.437 [0.411, 0.464] |

| Random intercept | Levels | σ [95 % CrI] | σ² |
|---|---:|---|---:|
| prompt | 96 | 2.009 [1.746, 2.312] | 4.036 |
| collection day | 52 | 0.074 [0.061, 0.090] | 0.005 |

The null model M0, same random structure and no covariates, gives σ_prompt = 2.001 [1.739, 2.303] and σ_day = 0.087 [0.071, 0.106]. Adding the entire fixed part moves σ²_prompt from 4.005 to 4.036, under 1 %. Vertical, language, query type and category are *properties of the prompt*, and those four factors together account for essentially none of the variance between prompts. Whatever makes one prompt orders of magnitude more likely to surface a cohort entity than another is not captured by the design factors used to build the battery — which is worth saying, because the battery was built on the assumption that they would be.

**Table 4. M2, the inferential anchor: pooled logistic with two-way cluster-robust covariance (n = 38,195; 96 prompt × 52 day clusters, df = 51).** *Caption: same fixed part as M1. Odds ratios with `t(51)` intervals. `Inflation` is the cluster-robust standard error divided by the naive one. Source: `s1_results.json:m2_cluster_robust_core3`.*

| Term | β | OR [95 % CI] | SE naive | SE two-way | Inflation | p |
|---|---:|---|---:|---:|---:|---:|
| Intercept | 0.1170 | 1.124 [0.465, 2.719] | 0.0459 | 0.4400 | 9.59 | 0.791 |
| engine = Perplexity | 1.9160 | **6.794 [4.189, 11.018]** | 0.0418 | 0.2408 | 5.76 | 1.70e−10 |
| engine = Claude | 1.1094 | 3.033 [1.519, 6.053] | 0.0415 | 0.3443 | 8.29 | 0.00222 |
| engine = Grok | 1.0977 | 2.997 [1.834, 4.899] | 0.1022 | 0.2448 | 2.39 | 4.17e−05 |
| engine = Groq | −0.4831 | 0.617 [0.354, 1.075] | 0.0480 | 0.2767 | 5.76 | 0.0869 |
| engine = Gemini | −2.4232 | **0.089 [0.050, 0.157]** | 0.0791 | 0.2853 | 3.60 | 2.47e−11 |
| vertical = saude | −1.5156 | 0.220 [0.103, 0.470] | 0.0410 | 0.3792 | 9.25 | 0.000207 |
| vertical = tecnologia | −1.8229 | 0.162 [0.079, 0.330] | 0.0430 | 0.3563 | 8.28 | 4.78e−06 |
| vertical = varejo | −0.2219 | 0.801 [0.375, 1.710] | 0.0364 | 0.3779 | 10.38 | 0.560 |
| language = pt | −0.1604 | 0.852 [0.497, 1.459] | 0.0283 | 0.2681 | 9.46 | 0.552 |
| query type = exploratory | −1.5562 | 0.211 [0.125, 0.356] | 0.0303 | 0.2610 | 8.62 | 2.35e−07 |
| category = descoberta | −0.1446 | 0.865 [0.437, 1.713] | 0.0346 | 0.3403 | 9.84 | 0.673 |
| category = mercado | −0.1547 | 0.857 [0.437, 1.681] | 0.0346 | 0.3357 | 9.69 | 0.647 |

Two things deserve attention. The inflation column runs from 2.4 to 10.4: an analysis of this series that treats its 38,195 rows as 38,195 independent observations understates the width of a prompt-level interval by roughly one order of magnitude. And the M1 and M2 odds ratios for the same contrast differ by a factor of about two — 14.49 against 6.79 for Perplexity — because M1 is a subject-specific estimate conditional on prompt and day while M2 is population-averaged. Both are correct answers to different questions. The manuscript should quote **M2** wherever the sentence is about engines in general and **M1** wherever it is about the same prompt on the same day.

**Table 5. Likelihood-ratio tests, one per fixed-effect block.** *Caption: `d̄` is the generalised design effect of the dropped block; `LRT corrected` is the Rao–Scott statistic `LRT/d̄`, compared to χ²(df). The last row is fitted on the five-arm full battery (n = 60,883), the only design in which all six categories are crossed with the engines present. Source: `s1_results.json:lrt_core3`, `lrt_5arm_categories`.*

| Block | df | LRT naive | p naive | d̄ | LRT corrected | **p corrected** | Wald F p |
|---|---:|---:|---:|---:|---:|---:|---:|
| engine | 5 | 8,284.1 | <1e−300 | 29.51 | 280.74 | **1.38e−58** | 3.38e−19 |
| vertical | 3 | 3,051.6 | <1e−300 | 82.28 | 37.09 | **4.41e−08** | 2.95e−06 |
| query type | 1 | 2,977.8 | <1e−300 | 74.25 | 40.10 | **2.41e−10** | 2.35e−07 |
| language | 1 | 32.1 | 1.49e−08 | 89.50 | 0.36 | 0.549 | 0.552 |
| category (core-3) | 2 | 25.1 | 3.54e−06 | 90.03 | 0.28 | 0.870 | 0.883 |
| category (five-arm, 6 levels) | 5 | 2,768.6 | <1e−300 | 84.22 | 32.87 | **3.99e−06** | 0.000149 |

The design effects are the result. A naive analysis of this series inflates its evidence for a prompt-level covariate by a factor of 74 to 90. Engine, which varies *within* prompt and *within* day, carries a design effect of 29.5 and survives the correction with room to spare. Language and the three-level category contrast do not survive at all once the correction is applied — and §3.5 shows that for language this is a statement about the *between-prompt* comparison, not about the effect itself.

### 3.3 Variance decomposition

**Table 6a. Response level, core-3 balanced design, six engines.** *Caption: intercept-only GLMM with crossed random intercepts for prompt and day; the engine is carried as a fixed factor and converted to a variance component by the Nakagawa–Schielzeth rule (variance of the engine contribution to the linear predictor, equal weight per engine). Six levels are too few to identify a random-intercept variance — see Table 6d. ICC on the latent scale. Source: `s1_results.json:vd_response.primary`.*

| Level | σ | σ² | **ICC** |
|---|---:|---:|---:|
| prompt | 2.777 | 7.709 | **0.4559** |
| engine | 2.430 | 5.905 | **0.3492** |
| residual (logistic) | — | 3.290 | 0.1946 |
| collection day | 0.074 | 0.005 | **0.0003** |

**One sentence: which prompt was asked explains more of whether a Brazilian entity gets cited (ICC 0.46) than which engine answered it (0.35), and the day it was asked explains essentially nothing (0.0003).**

The engine-as-random alternative gives σ_engine = 2.260 and ICC 0.317, and the unadjusted plug-in variance of the six marginal engine logits is 1.812 (σ = 1.35). The three estimates bracket the engine level between roughly a quarter and a third of the latent variance; the prompt level is above it on every specification.

σ_prompt here (2.777) is larger than in M1 (2.009), and the reason is non-collapsibility rather than a discrepancy. M1 conditions on vertical, language, query type and category; the decomposition model conditions only on the engine, so the prompt random effect has to carry the prompt attributes as well. Because the residual variance of a logistic model is pinned at π²/3 and cannot absorb heterogeneity, unmodelled variation is pushed into the random effects rather than shrinking them. The decomposition is the quantity of interest precisely because it does not partial out prompt attributes: the question is how much of the outcome lives at the prompt level, not how much survives after the prompt's own design factors are removed.

**Table 6b. Entity level, five truncated arms.** *Caption: the unit is one candidate entity inside one response; the candidate set is the query's own vertical roster (27 candidates for fintech, 28 for the others). Perplexity is excluded because its stored text is the whole response, so `cited_entities_v2_json` cannot be restricted to the first 200 characters for any entity but the earliest; the other five arms were truncated at collection time, so their entity lists ARE the uniform window. The full long frame is 1,689,460 rows, which the variational fit cannot take, so each run uses a stratified subsample of responses (strata: engine × vertical × category), 5,988 responses → 166,164 entity-rows, across three independent seeds. All six fits converged. Source: `s1_results.json:vd_entity`.*

| Level | ICC, mean across seeds | min | max | σ (seed 11) | σ² |
|---|---:|---:|---:|---:|---:|
| **entity** | **0.4641** | 0.4556 | 0.4803 | 3.256 | 10.601 |
| prompt | 0.2840 | 0.2716 | 0.2956 | 2.448 | 5.994 |
| engine | 0.0993 | 0.0949 | 0.1059 | 1.464 | 2.144 |
| residual (logistic) | 0.1491 | — | — | — | 3.290 |
| collection day | 0.0011 | 0.0005 | 0.0019 | 0.206 | 0.042 |

**One sentence: once the question is "which company gets named" rather than "does anyone get named", the entity's own identity dominates (ICC 0.46), the prompt comes second (0.28), the engine is a distant third (0.10), and the day is noise (0.001).**

The model-free benchmark agrees on the engine level: the five marginal entity-slot logits are ChatGPT −4.80, Claude −4.35, Gemini −6.76, Grok −3.82, Groq −5.68, variance 1.344 against the model's 2.144. Slot counts and hit counts are in `s1_results.json:vd_entity.entity_slots_per_engine` and `entity_hits_per_engine`.

**Tables 6a and 6b together are the citable result.** Whether a Brazilian entity is mentioned at all is mostly a property of the question; which Brazilian entity is mentioned is mostly a property of the entity. Neither is mostly a property of the engine, and neither is meaningfully a property of the day. That last point is worth stating plainly for an operator: day-to-day movement in a citation dashboard built on this design is measurement noise unless it survives an interval built on the day cluster, and the day cluster carries between 0.03 % and 0.11 % of the latent variance.

**Table 6d. Engine-as-random at the entity level: the specification that does not hold still.** *Caption: the same four-way model with the engine as a random intercept, refitted at three subsample sizes and three seeds. This is reported as a negative result, not as an estimate. Source: `s1_results.json:vd_entity.engine_random_stability_ladder`.*

| Responses sampled | Entity-rows | σ engine | σ entity | σ prompt | σ day |
|---:|---:|---:|---:|---:|---:|
| 1,527 | 42,372 | 2.386 | 2.445 | 1.800 | 0.451 |
| 2,991 | 82,998 | 2.186 | 2.725 | 2.062 | 0.331 |
| 5,988 (seed 11) | 166,164 | **6.743** | 3.396 | 2.487 | 0.208 |
| 5,988 (seed 23) | 166,164 | **6.439** | 3.258 | 2.519 | 0.102 |
| 5,988 (seed 47) | 166,164 | **6.942** | 3.268 | 2.566 | 0.138 |

Every one of these fits reported convergence. The engine standard deviation nevertheless triples between 2,991 and 5,988 sampled responses and then sits, stably and wrongly, near 6.7 across three independent seeds — while the marginal engine logits span only 2.94 on the logit scale (σ ≈ 1.16). A variance component over five levels is weakly identified, the variational objective is flat in that direction, and a reproducible optimum is not the same thing as a trustworthy one. This is why Tables 6a and 6b carry the engine as a fixed factor. Had the ladder not been fitted, the engine ICC at the entity level would have been reported as roughly 0.69 instead of 0.10 — a seven-fold error, stable across seeds, with a convergence flag reading `True`.

### 3.4 Interactions

**Table 7. Interaction tests, core-3 balanced design.** *Caption: each interaction is tested against the identical model without it. `d̄` and the corrected LRT as in Table 5. `ΔAIC` is from the naive likelihood and is shown only for magnitude. Source: `s1_results.json:interactions`.*

| Interaction | df | LRT naive | d̄ | LRT corrected | **p corrected** | Wald F p | ΔAIC | Flags |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| engine × vertical | 15 | 992.3 | 28.90 | 34.34 | **0.00305** | 3.72e−35 | −962.3 | rank-deficient, anticonservative |
| engine × language | 5 | 174.5 | 31.52 | 5.54 | 0.354 | 0.395 | −164.5 | — |
| query type × vertical | 3 | 125.2 | 75.32 | 1.66 | 0.645 | 0.490 | −119.2 | — |

**Engine × vertical is the one interaction that changes a market reading.** It survives the design correction and it is large where it matters: the spread between an engine's best and worst vertical, in points of citation rate, is

| Engine | Spread across verticals (pp) |
|---|---:|
| Grok | 58.46 |
| Claude | 56.07 |
| Perplexity | 41.35 |
| Groq | 20.61 |
| ChatGPT | 17.93 |
| Gemini | 5.00 |

Claude cites a cohort fintech in 72.4 % of responses (1,373 / 1,896) and a cohort health company in 18.8 % (354 / 1,880). Perplexity runs 68.6 % on fintech against 29.2 % on technology. ChatGPT moves 18 points across the same four verticals and Gemini 5. A single "engine X cites Brazilian companies Y % of the time" number is therefore not a summary of anything for Claude, Grok or Perplexity, and roughly is one for ChatGPT and Gemini. The most striking cell is **Gemini on health: 0 citations in 1,920 responses**, an exact zero rather than a small rate.

The Wald test on this block is flagged: 15 parameters against 52 clusters produces a rank-deficient and anti-conservative cluster-robust covariance, which is why its p-value of 3.7e−35 must be discarded in favour of the corrected LRT's 0.00305.

**Engine × language and query type × vertical do not survive the design correction on the marginal model.** For query type × vertical the reading is straightforward: the interaction is not separable from prompt-level variance in this design, and it should not be claimed. For engine × language the reading is not straightforward at all, and §3.5 resolves it.

### 3.5 The language effect, paired

Language varies only *between* prompts in the marginal model, so the whole between-prompt variance lands on the language contrast and the design effect of 89.5 destroys the power (Table 5: p = 0.549). The battery was built as 96 matched PT/EN pairs precisely so this would not be necessary. A pair is identified by *(vertical, category, query type, temporal variant)* and matched inside the same engine on the same collection day. One binary observation per `(engine, day, prompt)` is taken as the first run by timestamp, so a repeated run inside a day cannot enter a pair twice. **21,862 complete pairs** result.

**Table 8. McNemar on matched PT/EN pairs.** *Caption: `PT-only` and `EN-only` are the discordant counts; the paired difference is `mean(y_pt − y_en)` with a day-clustered CR1 interval; `p` is the exact McNemar binomial test on the discordant pairs; `h` is Cohen's h. Source: `s1_results.json:paired_language`.*

| Stratum | Pairs | Days | Rate PT | Rate EN | Paired diff (pp) | 95 % CI (pp) | PT-only | EN-only | Disc. OR | p exact | h |
|---|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|
| **All engines** | 21,862 | 52 | 0.1595 | 0.2049 | **−4.54** | [−4.90, −4.17] | 1,009 | 2,001 | 0.504 | 2.86e−74 | 0.118 |
| ChatGPT | 4,800 | 50 | 0.1110 | 0.2352 | **−12.42** | [−12.95, −11.89] | 122 | 718 | 0.170 | 1.86e−103 | 0.333 |
| Groq | 4,512 | 47 | 0.0512 | 0.1166 | −6.54 | [−6.98, −6.10] | 13 | 308 | 0.042 | 2.36e−74 | 0.240 |
| Grok | 462 | 5 | 0.2727 | 0.3333 | −6.06 | [−9.81, −2.31] | 26 | 54 | 0.481 | 0.00232 | 0.132 |
| Gemini | 4,893 | 51 | 0.0092 | 0.0286 | −1.94 | [−2.23, −1.65] | 13 | 108 | 0.120 | 8.37e−20 | 0.148 |
| Claude | 4,765 | 50 | 0.2478 | 0.2667 | −1.89 | [−2.54, −1.24] | 417 | 507 | 0.822 | 0.00339 | 0.043 |
| **Perplexity** | 2,430 | 52 | 0.5642 | 0.5181 | **+4.61** | [+2.54, +6.68] | 418 | 306 | 1.366 | 3.58e−05 | 0.093 |

Ask the *same question* of the *same engine* on the *same day* in Portuguese rather than English and the chance of a Brazilian cohort entity appearing in the first 200 characters falls by 4.54 points overall — and every one of the six engine-level tests survives Benjamini–Hochberg. The marginal model said nothing (OR 0.852, p = 0.552); the paired design says the effect is real, is large on ChatGPT, and **reverses on Perplexity**.

That reversal is an engine × language interaction, and the pairing gives the design-valid instrument for it that the marginal model could not. Regressing the paired difference `d = y_pt − y_en` on the engine — a linear model, because `d` is already a difference of two probabilities and its coefficients read directly in points — with two-way cluster-robust errors on (day, pair):

**Table 9. Engine × language tested inside the pair.** *Caption: reference engine ChatGPT; 21,862 pairs; 52 day × 96 pair clusters; df = 51. The intercept is ChatGPT's own paired difference; every other row is the difference between that engine's paired difference and ChatGPT's. Block test F(5, 51) = 3.17, p = 0.0145. Source: `s1_results.json:paired_language.engine_by_language_within_pair`.*

| Term | Estimate (pp) | SE (pp) | 95 % CI (pp) | p |
|---|---:|---:|---|---:|
| Intercept (ChatGPT paired difference) | −12.417 | 3.605 | [−19.653, −5.180] | 0.00115 |
| Perplexity − ChatGPT | **+17.026** | 5.066 | [+6.856, +27.196] | 0.00148 |
| Claude − ChatGPT | +10.528 | 5.622 | [−0.759, +21.815] | 0.0669 |
| Gemini − ChatGPT | +10.475 | 3.712 | [+3.023, +17.927] | 0.00679 |
| Grok − ChatGPT | +6.356 | 3.687 | [−1.046, +13.758] | 0.0908 |
| Groq − ChatGPT | +5.879 | 3.581 | [−1.311, +13.068] | 0.107 |

**The same interaction that failed at p = 0.354 on the marginal model reaches p = 0.0145 within the pair, and survives BH.** The difference is entirely one of design, not of data: the pairing removes the prompt effect that carries 46 % of the latent variance. This is the practical argument for building a paired battery, and it is worth making explicitly in the manuscript. The operational content is that a Brazilian company optimising for Portuguese-language prompts is optimising against ChatGPT's grain by roughly 12 points and with Perplexity's grain by roughly 5.

### 3.6 Robustness

**Table 10. The principal coefficients under eight cuts.** *Caption: every row is the M2 specification (two-way cluster-robust logistic, reference ChatGPT / fintech / English / directive / comparativo) refitted on the stated subset. Odds ratios with `t` intervals. Cut F is not a robustness check of the model but a measurement of how much the window rule matters. Source: `s1_results.json:robustness`.*

| Cut | n | Perplexity vs ChatGPT | Gemini vs ChatGPT | PT vs EN | Exploratory vs directive |
|---|---:|---|---|---|---|
| **A. reference** (core-3, uniform window) | 38,195 | 6.794 [4.19, 11.02] | 0.089 [0.050, 0.157] | 0.852 [0.497, 1.459] | 0.211 [0.125, 0.356] |
| B. complete days only (44 days) | 33,568 | 6.738 [4.16, 10.90] | 0.083 [0.046, 0.149] | 0.846 [0.491, 1.458] | 0.216 [0.127, 0.368] |
| C. four-arm panel (no Groq, no Grok) | 30,525 | 6.873 [4.17, 11.32] | 0.088 [0.049, 0.157] | 0.961 [0.585, 1.578] | 0.204 [0.125, 0.331] |
| D. stable-panel era 04-23 → 06-09 (39 d) | 28,064 | 6.874 [4.19, 11.29] | 0.044 [0.018, 0.110] | 0.879 [0.504, 1.534] | 0.221 [0.129, 0.381] |
| E. byte-identical repeats collapsed | 31,975 | 6.508 [4.04, 10.47] | 0.078 [0.044, 0.138] | 0.884 [0.527, 1.481] | 0.200 [0.121, 0.330] |
| **F. native window** (no 200-char rule) | 38,195 | **21.341 [12.52, 36.38]** | 0.089 [0.050, 0.159] | 0.826 [0.474, 1.440] | 0.242 [0.139, 0.419] |
| G. strict boundary rule | 38,195 | 6.501 [4.00, 10.57] | 0.088 [0.050, 0.157] | 0.837 [0.491, 1.428] | 0.213 [0.126, 0.361] |
| H. day index in UTC, not UTC−3 | 38,195 | 6.794 [4.19, 11.01] | 0.089 [0.050, 0.157] | 0.852 [0.497, 1.459] | 0.211 [0.125, 0.356] |

The engine contrasts, the language contrast and the query-type contrast are all stable across B, C, E, G and H. Two cells move and both are informative.

Cut D moves Gemini from 0.089 to 0.044. That is the model-version switch: the stable-panel era contains only `gemini-2.5-pro`, and the pooled estimate blends it with `gemini-2.5-flash`. **Gemini's engine coefficient is not a property of "Gemini"; it is a property of a mixture of two models across a 59-day collection gap**, and the manuscript should name the version wherever it names the number.

Cut F is the headline of §1.1 in coefficient form: scoring Perplexity on its whole response while scoring everyone else on 200 characters inflates its odds ratio against ChatGPT from 6.79 to **21.34**, a factor of 3.1. Any published comparison of engines on this series that predates the harmonisation is reporting an artefact of unequal apertures at roughly triple its true size.

### 3.7 Multiplicity

Three families are declared in advance and corrected separately. Mixing them would be dishonest in both directions: the robustness family is deliberately redundant (the same coefficient under eight cuts) and would dilute the confirmatory tests, while the confirmatory family is the one the paper's claims rest on.

**Table 11. Benjamini–Hochberg, family `S1-confirmatory` (m = 17, FDR = 0.05, 13 survive).** *Caption: the confirmatory family is the five block LRTs from Table 5, the category LRT on the five-arm design, the three marginal interaction tests, the within-pair interaction test, and the seven McNemar tests. `p` for the LRTs is the design-corrected value; for the interactions the cluster-robust F; for McNemar the exact binomial. Source: `s1_results.json:multiplicity`.*

| Test | p raw | p BH | Survives |
|---|---:|---:|---|
| paired language — ChatGPT | 1.86e−103 | 3.16e−102 | yes |
| paired language — Groq | 2.36e−74 | 1.62e−73 | yes |
| paired language — overall | 2.86e−74 | 1.62e−73 | yes |
| LRT engine | 1.38e−58 | 5.87e−58 | yes |
| interaction engine × vertical | 3.72e−35 | 1.27e−34 | yes |
| paired language — Gemini | 8.37e−20 | 2.37e−19 | yes |
| LRT query type | 2.41e−10 | 5.85e−10 | yes |
| LRT vertical | 4.41e−08 | 9.37e−08 | yes |
| LRT category (five-arm) | 3.99e−06 | 7.53e−06 | yes |
| paired language — Perplexity | 3.58e−05 | 6.09e−05 | yes |
| paired language — Grok | 0.00232 | 0.00359 | yes |
| paired language — Claude | 0.00339 | 0.00480 | yes |
| **interaction engine × language (within pair)** | 0.0145 | 0.0189 | **yes** |
| interaction engine × language (marginal) | 0.395 | 0.480 | no |
| interaction query type × vertical | 0.490 | 0.555 | no |
| LRT language (marginal) | 0.549 | 0.584 | no |
| LRT category (core-3) | 0.870 | 0.870 | no |

Family `S1-contrasts` (the 12 individual coefficient tests of Table 4): m = 12, **7 survive**. The five engine contrasts survive except Groq (p_BH = 0.13); `query type = exploratory`, `vertical = tecnologia` and `vertical = saude` survive; language and the two category contrasts do not.

Family `S1-robustness` (the coefficient tests across the eight cuts of Table 10): m = 93, 54 survive. This family is reported for completeness and carries no confirmatory weight, because its members are by construction near-duplicates.

**Declared false discovery rate: 5 %.** At m = 17 in the confirmatory family, 13 rejections at FDR 0.05 means fewer than one of the thirteen is expected to be false.

---

## 4. What this does not establish

**It does not establish that Perplexity, or any engine, "cites Brazilian companies N % of the time."** Every rate here is conditional on a specific 96- or 192-prompt battery, and the query-clustered intervals of Table 2 are 2 to 12 times wider than the binomial ones. On a newly drawn battery from the same prompt population, Perplexity's 53.8 % is 46.4 % to 61.2 %. The prompt sample, not the response count, is the binding constraint on precision — and no amount of additional daily collection narrows it.

**It does not establish a causal effect of anything.** The engine, the vertical, the language and the query type are observed attributes of an observational panel, not assignments. The engine coefficients absorb every difference between vendors — model family, decoding parameters, retrieval, safety layer, system prompt, index freshness — and no design here separates them.

**It does not establish that the engine matters less than the prompt in a form a vendor can act on.** The variance decomposition is a statement about this cohort, this battery and this window. A different cohort, a longer window, or a battery with less between-prompt spread would move the ICCs. The one component that is robust across every specification tried is the smallest: the collection day carries between 0.03 % and 0.11 % of the latent variance.

**It does not establish an entity-level engine variance.** Table 6d shows a variance component over five levels producing a stable, reproducible, converged and wrong estimate. Table 6b's engine ICC of 0.099 is a Nakagawa–Schielzeth transformation of a fixed factor, not a random-effects variance, and it should be quoted with that qualifier. The marginal benchmark (variance 1.344 against the model's 2.144) supports the order of magnitude, not the second digit.

**It does not establish that Perplexity is excluded from the entity-level result for a substantive reason.** It is excluded for a measurement reason — its stored text is the whole response, so per-entity restriction to the first 200 characters is impossible for any entity but the earliest. A future collection storing the truncated text for all six arms would remove the exclusion; nothing in the data says what Perplexity's entity-level behaviour would look like under that window.

**It does not establish anything about Grok.** 1,118 observations on **five collection days** inside a two-week window, all on `grok-4.6`. Its coefficients are reported because withholding them would be worse, but they carry no temporal replication at all, and the day-clustered interval on five clusters is not a meaningful interval.

**It does not establish that Gemini's coefficient describes Gemini.** The arm is a mixture of `gemini-2.5-pro` (before the 59-day gap) and `gemini-2.5-flash` (after it). Cut D shows the two are not interchangeable: the engine odds ratio halves, from 0.089 to 0.044, when the estimate is restricted to the `2.5-pro` era.

**It does not establish that the repeated responses are cached.** Section 1.3 documents that 47.84 % of multi-run cells return byte-identical text and that the protocol's TTL argument predicts none. It does not distinguish caching from near-deterministic decoding of a short prefix, and the data here cannot. What cut E establishes is only that the coefficients do not depend on which reading is right.

**It does not establish that the marginal language effect is null.** Table 5 reports a design-corrected p of 0.549 for language, and Table 8 reports a paired difference of −4.54 points at p = 2.9e−74. Those are not in conflict: the first is a between-prompt comparison in a design where prompt carries 46 % of the variance, and the second is a within-pair comparison where it carries none. Reporting only the first would be a false negative produced by the wrong contrast, not by the data.

**It does not establish the three interactions that failed.** Query type × vertical and the marginal engine × language test did not survive the design correction. That is a statement about the power of this design against those contrasts, not evidence of absence. The naive LRTs for both are enormous (125.2 and 174.5) and the corrected ones are not (1.66 and 5.54) — which is exactly what an underpowered contrast in a clustered design looks like, and exactly what a null effect looks like too. The design cannot tell them apart.

**It does not establish the number of days the protocol claims.** The canonical cut holds 52 collection days over a 139-day calendar span with a 59-day hole. Any description of this series as a continuous twice-daily panel over eight weeks is not supported by the timestamps. S2 treats the calendar in detail.

**It does not license the M1 credible intervals as confidence intervals.** They come from a mean-field variational posterior, which is known to be anti-conservative, and they are systematically narrower than the cluster-robust intervals of Table 4 by a factor of roughly eight. Where a p-value is quoted from this supplement it should be the cluster-robust or the design-corrected one.
