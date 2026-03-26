# Papers — Pesquisa Empirica Multi-Vertical sobre Citacoes de LLMs em Empresas Brasileiras

Plataforma de coleta, persistencia e analise estatistica para pesquisa academica sobre **como LLMs citam empresas brasileiras** em 4 setores da economia.

Estudo longitudinal (alvo: 90+ dias, ~25.920 observacoes) focado em padroes de citacao, visibilidade e atribuicao de fontes por motores de busca generativos (Generative Engine Optimization — GEO).

## Design do Estudo

| Dimensao | Valor |
|----------|-------|
| Verticais | 4 (Fintech, Varejo, Saude, Tecnologia) |
| Entidades | 69 (61 reais + 8 ficticias para calibracao) |
| Modelos LLM | 4 (GPT-4o-mini, Claude Haiku 4.5, Gemini 2.5 Flash, Perplexity Sonar) |
| Queries por vertical | 12 especificas + 6 cross-vertical = 18 |
| Observacoes diarias | ~288 (18 queries x 4 modelos x 4 verticais) |
| Coleta | Diaria automatizada (GitHub Actions, 06:00 UTC) |
| Persistencia | SQLite (local) + Supabase (producao) |
| Alvo de publicacao | 3 papers (ArXiv, SIGIR/WWW, Information Sciences Q1) |

## Verticais e Coortes

### Fintech (21 entidades)
**Reais (14):** Nubank, PagBank, Cielo, Stone, Banco Inter, Mercado Pago, Itau, Bradesco, C6 Bank, PicPay, Neon, Safra, BTG Pactual, XP Investimentos
**Cross-market (5):** Revolut, Monzo, N26, Chime, Wise
**Ficticias (2):** Banco Floresta Digital, FinPay Solutions

### Varejo (16 entidades)
**Reais (14):** Magazine Luiza, Casas Bahia, Americanas, Amazon Brasil, Mercado Livre, Shopee Brasil, Renner, Riachuelo, C&A Brasil, Leroy Merlin, Centauro, Netshoes, Via Varejo, Grupo Pao de Acucar
**Ficticias (2):** MegaStore Brasil, ShopNova Digital

### Saude (16 entidades)
**Reais (14):** Dasa, Hapvida, Unimed, Fleury, Rede D'Or, Einstein, Sirio-Libanes, Raia Drogasil, Eurofarma, Ache, EMS, Hypera Pharma, NotreDame Intermedica, SulAmerica Saude
**Ficticias (2):** HealthTech Brasil, Clinica Horizonte Digital

### Tecnologia (16 entidades)
**Reais (14):** Totvs, Stefanini, Tivit, CI&T, Locaweb, Linx, Movile, iFood, Vtex, RD Station, Conta Azul, Involves, Accenture Brasil, IBM Brasil
**Ficticias (2):** TechNova Solutions, DataBridge Brasil

## Metodologia Estatistica

### Framework de Testes

| Teste | Uso | Implementacao |
|-------|-----|---------------|
| **Chi-squared** | Associacao entre query category e citacao | `scipy.stats.chi2_contingency` + Cramer's V |
| **Kruskal-Wallis** | Comparacao de taxas entre 4+ modelos LLM (nao-parametrico) | `scipy.stats.kruskal` + eta-squared |
| **ANOVA one-way** | Comparacao entre grupos (quando Levene p > 0.05) | `scipy.stats.f_oneway` + eta-squared |
| **Mann-Whitney U** | Posicao de citacao (ordinal, nao-normal) | `scipy.stats.mannwhitneyu` + rank-biserial r |
| **T-test** (ind/paired) | Comparacao de medias pre/pos intervencao | `scipy.stats.ttest_ind/rel` + Cohen's d |
| **Regressao logistica** | Preditores de citacao (schema, word count, etc.) | `statsmodels.Logit` + pseudo R-squared, AIC, BIC, odds ratios |
| **Correlacao** | Spearman (default) / Pearson | `scipy.stats.spearmanr/pearsonr` |

### Correcao para Multiplicidade

| Metodo | Aplicacao |
|--------|-----------|
| **Bonferroni** | Comparacoes family-wise (entre verticais) |
| **Benjamini-Hochberg FDR** | Testes per-entity (controla false discovery rate) |

### Effect Sizes Reportados

| Metrica | Teste associado | Classificacao |
|---------|----------------|---------------|
| Cohen's d | t-test | 0.2 small, 0.5 medium, 0.8 large |
| Cramer's V | chi-squared | sqrt(chi2 / (n * (min_dim-1))) |
| Eta-squared | ANOVA/KW | SS_between / SS_total |
| Rank-biserial r | Mann-Whitney | 1 - (2U)/(n1*n2) |
| Pseudo R-squared | Logistica | McFadden |

### Verificacao de Pressupostos

```
Query -> Levene test (homogeneidade de variancias)
           |
           ├── p > 0.05 -> ANOVA parametrica
           └── p <= 0.05 -> Kruskal-Wallis (nao-parametrico)
```

### Analise de Contexto (Modulo 7)

Cada citacao detectada passa por analise de:

| Campo | Metodo |
|-------|--------|
| **Sentimento** | Regex contra 16 sinais positivos + 12 negativos (PT-BR + EN), janela de 200 chars |
| **Atribuicao** | Hierarquia: linked (URL presente) > named (entidade no texto) > paraphrased |
| **Precisao factual** | Verificacao contra fatos canonicos (ano fundacao, CEO, sede) para 5 entidades-chave |
| **Hedging** | 16 padroes regulares ("according to", "reportedly", "possivelmente") |
| **Posicao** | Tercil: 1 (primeiro terco), 2 (meio), 3 (ultimo terco) da resposta |

### Pre-registro de Hipoteses

Schema `hypotheses` preparado para pre-registro formal:
- `null_hypothesis` / `alt_hypothesis`
- `test_method`, `expected_effect_size`, `min_sample_size`
- `alpha` (default 0.05), `power` (default 0.80)
- Status lifecycle: `registered` -> `collecting` -> `analyzing` -> `confirmed` | `rejected` | `inconclusive`

### Criterios de Publicacao

| Criterio | Alvo | Status atual |
|----------|------|-------------|
| Observacoes totais | >= 25.920 (288/dia x 90 dias) | 397 (1.5%) |
| N por LLM | >= 1.000 | 30-136 |
| Dias de coleta | >= 90 continuos | 2 |
| Hipoteses pre-registradas | >= 3 | 0 |
| A/B experiments | >= 2 | 0 |
| Entidades ficticias validadas | 8 (false positive rate) | 0 queries |

### Limitacoes Conhecidas (26/03/2026)

1. **N efetivo < N bruto:** 54% das observacoes sao cache hits (respostas identicas reutilizadas). N_eff ~ 181
2. **Desbalanceamento amostral:** Gemini Flash tem N=3 em 3 de 4 verticais (falhas de API nas primeiras rodadas)
3. **Queries diretivas:** Categorias como "fintech_trust" produzem taxa de citacao de 100% por design — nao representam citacao espontanea
4. **Non-stationarity:** LLMs atualizam modelos sem aviso. Tabela `model_versions` existe mas nao esta sendo populada
5. **Observacoes nao-independentes:** Queries similares ao mesmo modelo na mesma sessao compartilham estado interno

## Arquitetura

```
src/
  config.py                  # Configuracao central, cohorts por vertical, LLM configs
  cli.py                     # CLI principal (click)
  collectors/
    base.py                  # Cliente LLM multi-provider + cache + FinOps tracking
    citation_tracker.py      # Modulo 1: Citation Tracker (4 LLMs x 4 verticais)
    competitor.py             # Modulo 2: Multi-Vertical Benchmark
    serp_overlap.py           # Modulo 3: SERP vs AI Overlap
    intervention.py           # Modulo 4: A/B Testing
    context_analyzer.py       # Modulo 7: Sentimento, atribuicao, precisao
  db/
    schema.sql               # Schema completo (21 tabelas)
    client.py                # Persistencia SQLite/Supabase
    migrate_cited_entity.py  # Migracao: backfill cited_entity
    migrate_normalize_models.py  # Migracao: normalizar model strings
  persistence/
    timeseries.py            # Modulo 5: Snapshots diarios
  analysis/
    statistical.py           # Modulo 6: 7 testes + correcoes + effect sizes
    visualization.py         # Graficos com IC 95% (matplotlib/seaborn)
  finops/
    tracker.py               # Custo por token, 4 provedores, budget control
    monitor.py               # Dashboard, alertas, security audit
    secrets.py               # Key rotation, leak scanning, health checks
  api/
    main.py                  # FastAPI (endpoints por vertical)
data/
  papers.db                  # SQLite local (gitignored)
  dashboard_data.json        # Dados extraidos para dashboard
output/
  critica_estatistica_panel.md  # Revisao por painel de 7 especialistas
.github/workflows/
  daily-collect.yml          # Coleta diaria 06:00 UTC
  weekly-benchmark.yml       # Benchmark semanal (domingo 08:00 UTC)
```

## Papers Planejados

| # | Titulo | Venue | Metodologia principal |
|---|--------|-------|----------------------|
| 1 | How LLMs Cite Entities Across Industry Verticals | ArXiv | Multi-vertical tracking, ANOVA/KW entre modelos, series temporais |
| 2 | GEO vs SEO: Source Divergence | SIGIR/WWW | Jaccard index semanal (top-10 Google vs fontes LLM), 12+ semanas |
| 3 | Industry-Specific Patterns in AI Citation | Information Sciences (Q1) | Fisher exact test, odds ratios, IC 95%, 2 A/B experiments |

## FinOps

| Provedor | Modelo | Custo/MTok (in/out) | Budget mensal |
|----------|--------|---------------------|---------------|
| OpenAI | gpt-4o-mini-2024-07-18 | $0.15 / $0.60 | $10 |
| Anthropic | claude-haiku-4-5 | $0.80 / $4.00 | $10 |
| Google | gemini-2.5-flash | $0.15 / $0.60 | $5 |
| Perplexity | sonar | $1.00 / $1.00 | $10 |
| **Global** | | | **$70** (hard stop 95%) |

## Setup

```bash
pip install -e ".[dev]"
cp .env.example .env  # Configurar API keys
python -m src.cli db migrate
python -m src.cli collect all
```

## Comandos

```bash
# Coleta
python -m src.cli collect all                          # Todas as verticais
python -m src.cli collect all --vertical fintech       # So fintech
python -m src.cli collect citation                     # So Citation Tracker

# Analise
python -m src.cli analyze --report                     # Relatorio completo
python -m src.cli analyze --report --vertical saude    # So saude
python -m src.cli analyze --visualize                  # Graficos por vertical

# Banco de dados
python -m src.cli db migrate                           # Aplicar schema
python -m src.cli db export --format csv               # Exportar dados
python -m src.cli db health                            # Saude por vertical

# Migracoes (one-time)
python src/db/migrate_normalize_models.py              # Normalizar GPT model strings
python src/db/migrate_cited_entity.py                  # Backfill cited_entity
```

## Documentacao

| Documento | Descricao |
|-----------|-----------|
| [docs/METHODOLOGY.md](docs/METHODOLOGY.md) | Metodologia estatistica completa com testes, pressupostos e limitacoes |
| [docs/REQUIREMENTS.md](docs/REQUIREMENTS.md) | Especificacao formal (RF/RNF) |
| [docs/GOVERNANCE.md](docs/GOVERNANCE.md) | Politicas de gasto, ADRs, roadmap |
| [docs/MANUAL.md](docs/MANUAL.md) | Manual operacional |
| [docs/CHANGELOG.md](docs/CHANGELOG.md) | Historico de mudancas |
| [output/critica_estatistica_panel.md](output/critica_estatistica_panel.md) | Revisao critica por painel de 7 especialistas |

## Licenca

MIT
