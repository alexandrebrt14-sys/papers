# 4. Results

All estimates below derive from the confirmatory window of `papers.db` (62,820 raw observations; analytic core n = 50,453 after excluding adversarial probes and calibration items, extraction version v2). This snapshot covers the complete collection record to date (April 23 - June 9, 2026); absolute rates and the anchor concentration figure should be read as upper bounds pending the integral re-collection described in §3 of the Methods. Where inference treats responses as independent, we flag the assumption explicitly and report the cluster-level test that supersedes it.

## 4.1 An apparent sectoral advantage

At face value, fintech is the most cited vertical. Across the analytic core, spontaneous citation rates rank fintech (28.15%) above retail (24.94%), technology (14.50%), and healthcare (13.35%); the global rate is 20.25% (Table 1). Treating each response as an independent trial, the fintech−healthcare contrast is large: a risk difference of +14.80 percentage points (pp) (95% CI +13.82 to +15.78) and an adjusted odds ratio of 4.13 (95% CI 3.81–4.47) under the fixed-effects logistic model (reference vertical = healthcare; LLM = ChatGPT; query category = comparative; McFadden pseudo-R² = 0.339). The fintech−retail contrast is smaller — RD +3.22 pp (95% CI +2.13 to +4.31), OR 1.18 (95% CI 1.115–1.247) — but still nominally positive. The weekly series (W16–W23) shows this ordering never inverts, which the draft read as temporal robustness [FIGURE 1 HERE].

That reading is the hypothesis this section dismantles. The aggregate ordering is genuine at the level of the marginal mean, but its attribution to the *vertical* does not survive decomposition.

**Table 1. Spontaneous citation rate by vertical (analytic core, Wilson 95% CI).**

| Vertical | n | Cited | Rate (%) | 95% CI (%) |
|---|---:|---:|---:|---|
| Fintech | 12,648 | 3,561 | 28.15 | 27.38 – 28.95 |
| Retail | 12,648 | 3,154 | 24.94 | 24.19 – 25.70 |
| Technology | 12,547 | 1,819 | 14.50 | 13.89 – 15.12 |
| Healthcare | 12,610 | 1,684 | 13.35 | 12.77 – 13.96 |
| **Total** | 50,453 | 10,218 | 20.25 | — |

## 4.2 Decomposition reveals anchor concentration

The fintech rate is concentrated in a single entity. Nubank accounts for 3,533 of the 7,112 entity mentions in fintech (49.68%), and 2,112 of the 3,561 cited responses (59.31%) name Nubank and no other roster entity. Citation concentration tracks citation rate across the four verticals: the Herfindahl index falls fintech (0.283) > retail (0.202) > healthcare (0.154) > technology (0.110), mirroring the rate ordering and consistent with a cumulative-advantage account rather than a diffuse sectoral property [FIGURE 4 HERE]. We caution that the 49.68% concentration is itself an upper bound: under 200-character truncation (§4.5), fintech's tail anchors are recorded late — Itaú at 402 chars, PicPay at 515, Banco Inter at 838, BTG at 906 — while Nubank's first mention sits at a mean offset of 118 chars, so truncation mechanically inflates the anchor's apparent dominance within the vertical.

Recoding as "not cited" every fintech response whose only named entity is Nubank (leave-one-out, LOO) drops the fintech rate from 28.15% to 11.46% (95% CI 10.91–12.02), moving it below all three other verticals — a complete reversal of the ranking (Table 3). In the logistic model the adjusted fintech-vs-healthcare odds ratio inverts from 4.13 to 0.77 (95% CI 0.70–0.84); the LOO outcome also fits the structural covariates marginally better (pseudo-R² rises from 0.339 to 0.352), suggesting the genuine vertical and engine signal lives in the anchor-free data [FIGURE 2 HERE].

## 4.3 Cluster-robust inference kills the raw gap but confirms the LOO reversal

The naive contrasts above treat ~293 repetitions per query as independent; the effective design has ~48 query-clusters per vertical. Aggregating the citation rate to the query-cluster level (48 clusters per vertical, ≥30 observations each) and applying a Welch test between cluster means, the raw fintech−retail gap does not survive. Fintech averages 26.51% per cluster and retail 23.30%, but the between-query standard deviation is ~24 pp, yielding Welch t = 0.65 (df ≈ 94) — not significant. The 3.2-pp surface gap is swallowed by between-query variance, so "fintech has the highest rate" must be reported as a descriptive observation, not a statistically detected effect.

The reversal behaves in exactly the opposite way. Running the same cluster-level Welch test on fintech's LOO rate (10.50% per cluster) against raw retail (23.30%) gives t = −3.35 — significant and negative. The fragile finding (sectoral advantage) collapses where it should; the robust finding (anchor dominance, now expressed as a reversal) holds at the cluster level. The reversal is also temporally stable: the fintech−retail gap under LOO (both verticals' anchors removed) is negative in all eight weeks, ranging narrowly from −7.6 to −8.2 pp, which rules out the objection that the reversal is driven by particular weeks.

## 4.4 Anchors exist in every vertical (top-k generalization)

Applying the single-top-entity jackknife to each vertical shows that all four are anchor-driven, with the drop scaling with concentration (Table 3). Removing the top entity costs fintech 16.70 pp (Nubank), but only 5.67 pp for retail (Mercado Livre), 2.89 pp for technology (Totvs), and 2.55 pp for healthcare (Hypera). Read this way, fintech looks uniquely fragile. The asymmetry is real but not yet formally tested with a confidence interval on the *difference* of drops, which we flag as required confirmatory work.

The single-entity comparison is, however, the wrong unit for retail, which has a dual-anchor structure: Mercado Livre and Magazine Luiza together account for 58% of mentions. Removing both top-2 anchors drops retail from 24.94% to 10.59% — a fall of 14.35 pp, comparable in magnitude to fintech's. The top-3 share already signalled this and was under-exploited: fintech 70.9% versus retail 69.4%. The defensible contribution therefore generalizes not as "a single superstar" but as *top-k anchor concentration that varies by vertical*, with fintech the extreme k = 1 case and retail the k = 2 case [FIGURE 1 HERE].

**Table 3. Leave-one-out and per-vertical jackknife (analytic core).**

| Vertical | Anchor(s) removed | Anchor share | Original rate (%) | Rate after removal (%) | Drop (pp) |
|---|---|---:|---:|---:|---:|
| Fintech | Nubank | 49.7% | 28.15 | 11.46 | −16.70 |
| Retail | Mercado Livre | 29.5% | 24.94 | 19.27 | −5.67 |
| Retail | Mercado Livre + Magazine Luiza | 58% | 24.94 | 10.59 | −14.35 |
| Technology | Totvs | 24.8% | 14.50 | 11.60 | −2.89 |
| Healthcare | Hypera | 24.7% | 13.35 | 10.80 | −2.55 |

*Fintech LOO rate carries a Wilson 95% CI of 10.91–12.02%. Confidence intervals on the per-vertical drops are not yet computed and are required for confirmatory comparison of the asymmetry.*

## 4.5 Engine heterogeneity

The "sectoral" effect is not consistent across engines; it is largely one engine's idiosyncrasy plus one artifact. Only two of five engines place fintech above retail in raw rate: Claude Haiku (51.0% vs 30.7%) and Gemini (4.9% vs 0.0%, in a near-floor regime contaminated by truncation). ChatGPT (18.1% vs 22.2%), Groq (8.7% vs 12.0%), and Perplexity (86.5% vs 92.9%) all run the other way (Table 2). Decomposing the aggregate fintech−retail gap into excess cited responses per engine, Claude contributes +574 and Gemini +134 (truncation artifact), against ChatGPT −117, Perplexity −91, and Groq −93 [FIGURE 3 HERE; FIGURE 5 HERE]. The engine effect dominates the marginal model: Perplexity carries an OR of 12.12 (95% CI 11.12–13.21) versus ChatGPT, while Gemini sits at 0.061 (95% CI 0.052–0.072). Because Perplexity is a retrieval-augmented (RAG) engine that saturates near the ceiling (up to 92.9%) and Gemini near the floor, reporting the RAG and parametric engines as a single headline rate conflates two construct regimes; excluding Perplexity, the fintech rate is 20.80%. The cleanest parametric signal is the 40-pp Claude gap (fintech 51.0% vs technology 10.4%), which localizes the effect in the model weights rather than in live retrieval.

A sanity check in the integral (untruncated) Perplexity subset confirms the anchor effect is not a truncation artifact: fintech LOO falls to 67.9%, still below retail's 92.9%, whereas retail, technology, and healthcare have LOO rates equal to their originals (the RAG engine rarely cites the anchor alone). This validation rests on only ~24 query-clusters per vertical — half the prompt diversity of the truncated engines — and so is under-powered; we report it as supporting rather than confirmatory.

**Table 2. Vertical × LLM citation rate (%, analytic core).**

| Vertical | ChatGPT (gpt-4o-mini) | Claude (haiku-4.5) | Gemini (2.5-pro) | Groq (llama-3.3-70b) | Perplexity (sonar) |
|---|---:|---:|---:|---:|---:|
| Fintech | 18.1 | 51.0 | 4.9 | 8.7 | 86.5 |
| Retail | 22.2 | 30.7 | 0.0 | 12.0 | 92.9 |
| Technology | 20.4 | 10.4 | 0.7 | 6.0 | 54.3 |
| Healthcare | 8.0 | 10.7 | 0.0 | 6.1 | 69.8 |

*Cell n ≈ 2,832, except Perplexity ≈ 1,416 (collected at half cadence, with 24 distinct queries per vertical against 48 in the other engines).*

A related measurement threat concerns truncation direction. Response text was persisted at exactly 200 characters in four of five engines; only Perplexity is integral. Measured on the integral engine, retail front-loads *more* than fintech (mean first-entity offset 111.1 vs 123.1 chars), with healthcare (159.9) and technology (173.3) latest — so the draft's claim that truncation "rewards fintech for front-loading" is empirically false. Truncation instead penalizes the rivals: it would erase 51.6% of technology citations and 30.7% of healthcare citations whose first entity appears after char 200, against ~20% for fintech and retail. Truncation therefore inflates the fintech-vs-technology and fintech-vs-healthcare gaps (the +14.80-pp and +13.66-pp contrasts of Table 4 are partly an artifact of the cut) but not the fintech-vs-retail gap [FIGURE 6 HERE].

## 4.6 Temporal intensification

The anchor is not stable within the measurement window — it is intensifying. Nubank's share of fintech mentions rises from ~41% (W16–W18) to ~53–59% (W19–W23), an interim peak of 59.2% in W20, and the sole-Nubank fraction of cited responses climbs in parallel from 53.5% to 66.7% [FIGURE 7 HERE]. The aggregate fintech rate stays flat (~27–29% across the eight weeks) precisely because the tail (PicPay, C6, Inter) contracts while the anchor grows, so the marginal is held fixed by compensation rather than by stability. The draft measured the stable quantity (the vertical's rate) and missed the moving one (anchor concentration). We therefore read the within-window growth as a service-drift threat to temporal validity for the anchor construct, to be tracked in subsequent snapshots, and treat the aggregate's apparent stability as a compensating artifact rather than evidence of robustness.

A Mantel–Haenszel summary stratifying the fintech-vs-retail contrast by the six query categories gives a common OR of 1.205, but the Breslow–Day homogeneity test rejects (χ² = 25.42, 5 df, p = 0.0001): stratum ORs range from 1.04 (discovery) to 2.29 (experience), so the common OR carries a vertical × category interaction and still embeds the Nubank effect on the original outcome. Under LOO the sign inverts, consistent with §4.3. We report the M–H estimate with this caveat rather than as a pooled effect.

**Table 4. Effect sizes, naive (response-level) vs cluster-level inference.**

| Quantity | Estimate | 95% CI / test |
|---|---:|---|
| RD fintech − healthcare (original) | +14.80 pp | +13.82 to +15.78 pp |
| RD fintech − retail (original) | +3.22 pp | +2.13 to +4.31 pp |
| OR fintech vs healthcare, adjusted (original) | 4.13 | 3.81 – 4.47 |
| OR fintech vs healthcare, adjusted (LOO) | 0.77 | 0.70 – 0.84 |
| OR Perplexity vs ChatGPT | 12.12 | 11.12 – 13.21 |
| OR Gemini vs ChatGPT | 0.061 | 0.052 – 0.072 |
| Welch t, fintech − retail gap (cluster-level) | 0.65 | df ≈ 94; not significant |
| Welch t, fintech-LOO − retail (cluster-level) | −3.35 | significant, negative |
| Nubank share of fintech mentions | 49.68% | upper bound (truncation) |
| Sole-Nubank fraction of fintech citations | 59.31% | — |

*Response-level CIs are Wald/Wilson and are optimistically narrow because they treat 50,453 responses as independent; the cluster-level Welch tests are the inferential statements of record for the two gap contrasts. A confirmatory GLMM with random intercepts for query, day, and engine, dual outcome (cited_v2 and cited_loo), and cluster bootstrap is specified for the final window.*
