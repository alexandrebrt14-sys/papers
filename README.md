# papers — Empirical Multi-Vertical Research on LLM Citations of Brazilian Companies

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Status: Collecting](https://img.shields.io/badge/Status-Collecting-yellow)

Platform for collection, persistence, and statistical analysis of **how LLMs cite Brazilian companies** across 4 economic sectors.

Longitudinal study (target: 90+ days, ~25,920 observations) focused on citation patterns, visibility, and source attribution by generative search engines (Generative Engine Optimization — GEO).

---

## Study Design

| Dimension | Value |
|---|---|
| Verticals | 4 (Fintech, Retail, Healthcare, Technology) |
| Entities | 69 (61 real + 8 fictional for calibration) |
| LLM Models | 4 (GPT-4o-mini, Claude Haiku 4.5, Gemini 2.5 Flash, Perplexity Sonar) |
| Queries per vertical | 12 specific + 6 cross-vertical = 18 |
| Daily observations | ~288 (18 queries x 4 models x 4 verticals) |
| Observations collected | 653 citations, 172 contexts, 11 runs |
| Code | 7,010 lines Python, 35 files, 91 commits |
| Schema | 21 tables (citations, contexts, finops, interventions, snapshots, model_versions) |
| Collection | Automated daily (GitHub Actions, 06:00 UTC) |
| Persistence | SQLite WAL (canonical ledger) + Supabase (read projection) |
| Publication target | 3 papers (ArXiv, SIGIR/WWW, Information Sciences Q1) |

---

## Verticals and Cohorts

### Fintech (21 entities)
**Real (14):** Nubank, PagBank, Cielo, Stone, Banco Inter, Mercado Pago, Itau, Bradesco, C6 Bank, PicPay, Neon, Safra, BTG Pactual, XP Investimentos
**Cross-market (5):** Revolut, Monzo, N26, Chime, Wise
**Fictional (2):** Banco Floresta Digital, FinPay Solutions

### Retail (16 entities)
**Real (14):** Magazine Luiza, Casas Bahia, Americanas, Amazon Brasil, Mercado Livre, Shopee Brasil, Renner, Riachuelo, C&A Brasil, Leroy Merlin, Centauro, Netshoes, Via Varejo, Grupo Pao de Acucar
**Fictional (2):** MegaStore Brasil, ShopNova Digital

### Healthcare (16 entities)
**Real (14):** Dasa, Hapvida, Unimed, Fleury, Rede D'Or, Einstein, Sirio-Libanes, Raia Drogasil, Eurofarma, Ache, EMS, Hypera Pharma, NotreDame Intermedica, SulAmerica Saude
**Fictional (2):** HealthTech Brasil, Clinica Horizonte Digital

### Technology (16 entities)
**Real (14):** Totvs, Stefanini, Tivit, CI&T, Locaweb, Linx, Movile, iFood, Vtex, RD Station, Conta Azul, Involves, Accenture Brasil, IBM Brasil
**Fictional (2):** TechNova Solutions, DataBridge Brasil

---

## Collection Status (March 2026)

| Criterion | Target | Current |
|---|---|---|
| Total observations | >= 25,920 (288/day x 90 days) | 397 (1.5%) |
| N per LLM | >= 1,000 | 30-136 |
| Collection days | >= 90 continuous | 2 |
| Pre-registered hypotheses | >= 3 | 0 |
| A/B experiments | >= 2 | 0 |
| Fictional entity validation | 8 (false positive rate) | 0 queries |

### Known Limitations

1. **Effective N < Gross N**: 54% of observations are cache hits (identical responses reused). N_eff ~181
2. **Sample imbalance**: Gemini Flash has N=3 in 3 of 4 verticals (API failures in early rounds)
3. **Directive queries**: Categories like "fintech_trust" produce 100% citation rate by design — do not represent spontaneous citation
4. **Non-stationarity**: LLMs update models without notice. `model_versions` table exists but is not being populated
5. **Non-independent observations**: Similar queries to the same model in the same session share internal state

---

## Statistical Methodology

### Test Framework

| Test | Use | Implementation |
|---|---|---|
| **Chi-squared** | Association between query category and citation | `scipy.stats.chi2_contingency` + Cramer's V |
| **Kruskal-Wallis** | Comparison of rates across 4+ LLM models (non-parametric) | `scipy.stats.kruskal` + eta-squared |
| **ANOVA one-way** | Group comparison (when Levene p > 0.05) | `scipy.stats.f_oneway` + eta-squared |
| **Mann-Whitney U** | Citation position (ordinal, non-normal) | `scipy.stats.mannwhitneyu` + rank-biserial r |
| **T-test** (ind/paired) | Mean comparison pre/post intervention | `scipy.stats.ttest_ind/rel` + Cohen's d |
| **Logistic regression** | Citation predictors (schema, word count, etc.) | `statsmodels.Logit` + pseudo R-squared, AIC, BIC, odds ratios |
| **Correlation** | Spearman (default) / Pearson | `scipy.stats.spearmanr/pearsonr` |

### Multiple Testing Correction

| Method | Application |
|---|---|
| **Bonferroni** | Family-wise comparisons (across verticals) |
| **Benjamini-Hochberg FDR** | Per-entity tests (controls false discovery rate) |

### Effect Sizes

| Metric | Associated Test | Classification |
|---|---|---|
| Cohen's d | t-test | 0.2 small, 0.5 medium, 0.8 large |
| Cramer's V | chi-squared | sqrt(chi2 / (n * (min_dim-1))) |
| Eta-squared | ANOVA/KW | SS_between / SS_total |
| Rank-biserial r | Mann-Whitney | 1 - (2U)/(n1*n2) |
| Pseudo R-squared | Logistic | McFadden |

### Context Analysis (Module 7)

Each detected citation undergoes analysis of:

| Field | Method |
|---|---|
| **Sentiment** | Regex against 16 positive + 12 negative signals (PT-BR + EN), 200-char window |
| **Attribution** | Hierarchy: linked (URL present) > named (entity in text) > paraphrased |
| **Factual accuracy** | Verification against canonical facts (founding year, CEO, HQ) for 5 key entities |
| **Hedging** | 16 regular patterns ("according to", "reportedly", "possivelmente") |
| **Position** | Tertile: 1 (first third), 2 (middle), 3 (last third) of response |

---

## Planned Papers

| # | Title | Venue | Main Methodology |
|---|---|---|---|
| 1 | How LLMs Cite Entities Across Industry Verticals | ArXiv | Multi-vertical tracking, ANOVA/KW across models, time series |
| 2 | GEO vs SEO: Source Divergence | SIGIR/WWW | Weekly Jaccard index (top-10 Google vs LLM sources), 12+ weeks |
| 3 | Industry-Specific Patterns in AI Citation | Information Sciences (Q1) | Fisher exact test, odds ratios, 95% CI, 2 A/B experiments |

---

## Architecture

```
src/
  config.py               # Central configuration, cohorts per vertical, LLM configs
  cli.py                  # Main CLI (click)
  collectors/
    base.py               # Multi-provider LLM client + cache + FinOps tracking
    citation_tracker.py   # Module 1: Citation Tracker (4 LLMs x 4 verticals)
    competitor.py         # Module 2: Multi-Vertical Benchmark
    serp_overlap.py       # Module 3: SERP vs AI Overlap
    intervention.py       # Module 4: A/B Testing
    context_analyzer.py   # Module 7: Sentiment, attribution, accuracy
  db/
    schema.sql            # Complete schema (21 tables)
    client.py             # SQLite/Supabase persistence
  persistence/
    timeseries.py         # Module 5: Daily snapshots
  analysis/
    statistical.py        # Module 6: 7 tests + corrections + effect sizes
    visualization.py      # Charts with 95% CI (matplotlib/seaborn)
  finops/
    tracker.py            # Cost per token, 4 providers, budget control
    monitor.py            # Dashboard, alerts, security audit
    secrets.py            # Key rotation, leak scanning, health checks
  api/
    main.py               # FastAPI (endpoints per vertical)
.github/workflows/
  daily-collect.yml       # Daily collection 06:00 UTC
  weekly-benchmark.yml    # Weekly benchmark (Sunday 08:00 UTC)
```

---

## FinOps

| Provider | Model | Cost/MTok (in/out) | Monthly Budget |
|---|---|---|---|
| OpenAI | gpt-4o-mini-2024-07-18 | $0.15 / $0.60 | $10 |
| Anthropic | claude-haiku-4-5 | $0.80 / $4.00 | $10 |
| Google | gemini-2.5-flash | $0.15 / $0.60 | $5 |
| Perplexity | sonar | $1.00 / $1.00 | $10 |
| **Global** | | | **$70** (hard stop 95%) |

---

## Setup

```bash
pip install -e ".[dev]"
cp .env.example .env  # Configure API keys
python -m src.cli db migrate
python -m src.cli collect all
```

## Commands

```bash
# Collection
python -m src.cli collect all                         # All verticals
python -m src.cli collect all --vertical fintech      # Fintech only
python -m src.cli collect citation                    # Citation Tracker only

# Analysis
python -m src.cli analyze --report                    # Full report
python -m src.cli analyze --report --vertical saude   # Healthcare only
python -m src.cli analyze --visualize                 # Charts per vertical

# Database
python -m src.cli db migrate                          # Apply schema
python -m src.cli db export --format csv              # Export data
python -m src.cli db health                           # Health per vertical

# Migrations (one-time)
python src/db/migrate_normalize_models.py             # Normalize GPT model strings
python src/db/migrate_cited_entity.py                 # Backfill cited_entity
```

---

## Documentation

| Document | Description |
|---|---|
| [docs/METHODOLOGY.md](docs/METHODOLOGY.md) | Complete statistical methodology with tests, assumptions, and limitations |
| [docs/REQUIREMENTS.md](docs/REQUIREMENTS.md) | Formal specification (functional/non-functional) |
| [docs/GOVERNANCE.md](docs/GOVERNANCE.md) | Spending policies, ADRs, roadmap |
| [docs/MANUAL.md](docs/MANUAL.md) | Operational manual |
| [docs/CHANGELOG.md](docs/CHANGELOG.md) | Change history |
| [output/critica_estatistica_panel.md](output/critica_estatistica_panel.md) | Critical review by panel of 7 specialists |

---

## License

MIT

---

**Author:** [Alexandre Caramaschi](https://alexandrecaramaschi.com) — CEO of Brasil GEO, former CMO at Semantix (Nasdaq), co-founder of AI Brasil.

---

## Ecosystem

| Property | Stack | Status |
|---|---|---|
| [alexandrecaramaschi.com](https://alexandrecaramaschi.com) | Next.js 16 + React 19 + Supabase | Production — 35 courses, 25 insights, 122K+ lines |
| [brasilgeo.ai](https://brasilgeo.ai) | Cloudflare Workers | Production — 14 articles |
| [geo-orchestrator](https://github.com/alexandrebrt14-sys/geo-orchestrator) | Python + 5 LLMs | Active — multi-LLM pipeline |
| [curso-factory](https://github.com/alexandrebrt14-sys/curso-factory) | Python + Jinja2 | Active — course generation pipeline |
| [geo-checklist](https://github.com/alexandrebrt14-sys/geo-checklist) | Markdown | Open-source — GEO audit checklist |
| [llms-txt-templates](https://github.com/alexandrebrt14-sys/llms-txt-templates) | Markdown + JSON | Open-source — llms.txt standard |
| [geo-taxonomy](https://github.com/alexandrebrt14-sys/geo-taxonomy) | JSON + CSV + Markdown | Open-source — 60+ GEO terms |
| [entity-consistency-playbook](https://github.com/alexandrebrt14-sys/entity-consistency-playbook) | Markdown | Open-source — entity consistency |
| [papers](https://github.com/alexandrebrt14-sys/papers) | Python + Supabase | Research — LLM citation study |
