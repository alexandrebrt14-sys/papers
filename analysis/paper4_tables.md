## Table 1 — Dataset statistics

| Variable | Value |
|---|---:|
| N total observations | 7,052 |
| Collection period | 2026-03-24 → 2026-04-22 |
| Collection days active | 12 |
| Number of verticals | 4 (fintech, saude, tecnologia, varejo) |
| Real entities (cohort_json) | 61 |
| Fictitious entities (design) | 8 (per CLAUDE.md: 2 per vertical — Banco Floresta Digital, FinPay Solutions, MegaStore Brasil, ShopNova Digital, HealthTech Brasil, Clínica Horizonte Digital, TechNova Solutions, DataBridge Brasil) |
| Fictitious-entity hits observed | 0 / 7,052 (fictional_hit column) |
| Number of LLMs | 4 (ChatGPT, Claude, Gemini in full run; Perplexity onboarded mid-period) |
| Queries — ChatGPT | 2,068 |
| Queries — Claude | 2,050 |
| Queries — Gemini | 1,913 |
| Queries — Perplexity | 1,021 |
| Queries — vertical fintech | 1,848 |
| Queries — vertical saude | 1,736 |
| Queries — vertical tecnologia | 1,767 |
| Queries — vertical varejo | 1,701 |
| Queries — lang en | 3,296 |
| Queries — lang pt | 3,756 |
| Overall citation rate | 77.62% (95% BCa CI: 76.62% — 78.57%) |
| Context analyses (citation_context rows) | 4,716 |
| Query categories (distinct) | 23 |

_Note — BCa CI via bootstrap (10.000 iterações, seed=42). The design specifies 8 fictitious entities (2 per vertical) as a hallucination probe; the `fictional_hit` column recorded zero hits across all 7,052 rows, which drives H2's Rule-of-3 upper bound._

## Table 2 — Hypothesis test results (Null-Triad core)

| Hypothesis | Test | Statistic | p (raw) | p (BH-FDR) | p (cluster-robust) | Effect size | 95% CI | Verdict |
|---|---|---:|---:|---:|---:|---:|---:|---|
| H1 RAG vs parametric | 2-prop z | z=-1.830 | 0.0673 | 0.0673 | 0.4841 | Cohen's h=-0.061 | [-0.127, 0.005] | FAIL TO REJECT |
| H2 Hallucination probe | Clopper-Pearson upper | k=0/N=7052 | — | — | — | upper bound=0.000425 | [0, 0.000425] (Rule of 3) | SUPPORTED (upper<0.5%) |
| H3 Jaccard top-30 | Mean pairwise Jaccard | shared queries=49 | — | — | — | mean J=0.1386 | range [0.0397, 0.3371] | SUPPORTED (low divergence) |
| Vertical heterogeneity | χ²(df=3) | χ²=384.064 | 0.0000 | 0.0000 | — | Cramér's V=0.233 | — | REJECT H0 |
| PT vs EN | 2-prop z | z=5.696 | 0.0000 | 0.0000 | 0.2146 | Cohen's h=0.136 | [0.089, 0.183] | REJECT H0 |
| Time trend | OLS slope / MK τ | slope=0.02323/day, τ=0.212 | 0.0279 | 0.0373 | — | slope=0.02323 | [0.00551, 0.04095] | REJECT H0 |

_Note — BH-FDR adjustment applied over the 4 frequentist rows (H2 and H3 excluded: H2 is a one-sided upper bound with k=0; H3 is a descriptive similarity). Cluster-robust p-values use day-of-collection as the cluster variable with the Liang-Zeger finite-sample correction._

## Table 3 — Inverse power analysis (n required for 80% power, α=0.05)

| Test | Observed effect | n (current) | n required for 80% power | Ratio (n_current / n_required) |
|---|---:|---:|---:|---:|
| H1 RAG vs parametric | diff=-0.0258 (h=-0.061) | n1=1,021, n2=6,031 | 4,211/group | 0.2× / 1.4× |
| H2 Hallucination probe | k=0/N=7,052 (upper=0.000425) | N=7,052 | n≥300 to upper-bound rate ≤1% | 23.51× |
| PT vs EN | diff=0.0567 (h=0.136) | n_pt=3,756, n_en=3,296 | 854/group | 4.40× / 3.86× |
| Time trend (daily rate, OLS) | slope=0.02323/day (SD resid=0.1031) | 12 days | 13 days | 0.92× |

_Note — H1 and PT-vs-EN use the 2-proportion z-test sample formula; H2 uses the Rule-of-3 inversion (n ≥ 3/upper) targeting a 1% upper bound; time trend solves n^3 ≈ 12·σ²·(z_α+z_β)²/slope²._

## Table 4 — Robustness: stability under 80% subsampling (B=20)

| Test | Median p | Min p | Max p | % reps with p<0.05 |
|---|---:|---:|---:|---:|
| H1 RAG vs parametric | 0.0586 | 0.0043 | 0.6646 | 50.0% |
| Vertical heterogeneity | 0.0000 | 0.0000 | 0.0000 | 100.0% |
| PT vs EN | 0.0000 | 0.0000 | 0.0000 | 100.0% |

_Note — Each of 20 replicates draws 80% of rows without replacement (seed=42) and re-runs the test. Stability interpreted as % replicates retaining significance at α=0.05._

## Table 5 — Cluster-robust SE inflation by day-of-collection

| Statistic | SE naive (iid) | SE cluster-robust | Inflation factor | CI naive | CI cluster-robust |
|---|---:|---:|---:|---:|---:|
| Overall citation rate | 0.00496 | 0.02336 | 4.71× | [76.65%, 78.60%] | [73.04%, 82.20%] |
| H1 difference (RAG − parametric) | 0.01449 | 0.03689 | 2.55× | [-5.42%, 0.26%] | [-9.81%, 4.65%] |

_Note — Cluster-robust SE groups observations by UTC collection day (n_days=12) with Liang-Zeger correction g/(g−1). Inflation factor >1 indicates intra-day autocorrelation tightens vs iid assumption._

## Table 6 — sources_json token distribution (instrumentation evidence for H3)

| LLM | Rows | Rows with sources | % non-empty | Mean tokens | Median tokens | P95 tokens |
|---|---:|---:|---:|---:|---:|---:|
| ChatGPT | 2,068 | 1 | 0.05% | 36.0 | 36.0 | 36.0 |
| Claude | 2,050 | 61 | 2.98% | 26.2 | 28.0 | 51.0 |
| Gemini | 1,913 | 58 | 3.03% | 49.2 | 51.0 | 103.3 |
| Perplexity | 1,021 | 1,021 | 100.00% | 132.3 | 137.2 | 181.2 |

_Note — Tokens are approximated as len(sources_json)/4 (OpenAI BPE heuristic). Row counts and non-empty fractions are exact from SQLite. Perplexity's 100% coverage with heavy tails is the instrumentation signal that Jaccard overlap is low (H3): different retrieval substrates, not divergent knowledge._
