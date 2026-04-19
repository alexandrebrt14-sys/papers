# Arquitetura — Papers (atualizado 2026-04-19)

Documento vivo da arquitetura de coleta acadêmica de dados de GEO no projeto Papers.

## Visão

Pipeline longitudinal que observa como 5 LLMs citam empresas brasileiras em 4 verticais, gerando evidência para 3 papers peer-reviewed. Fluxo operado 2x/dia via GitHub Actions com persistência em SQLite (source of truth no git) + Supabase (projeção somente-leitura).

## Diagrama do pipeline

```
                  cron (06:00 BRT + 18:00 BRT)
                          │
                          ▼
              .github/workflows/daily-collect.yml
                          │
      ┌───────────────────┼──────────────────────┐
      │                   │                      │
      ▼                   ▼                      ▼
  checkout           setup-python           download-artifact
  data/papers.db     pip install -e .       (safety net)
      │                   │                      │
      └──────────┬────────┴──────────┬───────────┘
                 ▼                   ▼
             src/cli.py        src/config.py
                 │                (queries + LLMs +
                 │                 entidades fictícias +
                 │                 mandatory_llms)
                 │
                 ▼
         for V in [fintech, varejo, saude, tecnologia]:
                 │
      ┌──────────┼──────────┐──────────────┐
      ▼          ▼          ▼              ▼
  Module 1   Module 2   Module 7        Module 5
  citation   competitor context_         timeseries
  tracker    benchmark  analyzer        (daily snapshot)
      │          │          │              │
      └──────────┴──────────┴──────────────┘
                        │
                        ▼
                 src/db/client.py
                 INSERT citations, collection_runs,
                        finops_usage, citation_context
                        │
                        ▼
                  data/papers.db  ← source of truth
                        │
                        ▼
         scripts/export_data.py --format json
                        │
                        ▼
                 data/dashboard_data.json
                        │
                        ▼
              scripts/sync_to_supabase.py
                        │
                        ▼
                    Supabase (projeção)
                        │
                        ▼
              scripts/send-report.py (Resend)
                        │
                        ▼
              scripts/health_check.py
                 (exit 1 trava o workflow)
                        │
                        ▼
               git commit + push
```

## Arquivos críticos

| Arquivo | Papel |
|---------|-------|
| `src/config.py` | 4 verticais, 5 LLMs, queries com `query_type`, `FICTIONAL_ENTITIES`, `mandatory_llms()` |
| `src/collectors/base.py` | Fachada enxuta (~85 linhas) + re-exports — split aplicado em Onda 7 |
| `src/collectors/llm_client.py` | **Onda 7** — `LLMClient` + `LLMResponse` (dispatch providers, cache, finops, circuit breaker) |
| `src/collectors/response_cache.py` | **Onda 7** — `ResponseCache` SHA-256 TTL 20h |
| `src/collectors/brave_search.py` | **Onda 7** — `BraveSearchClient` (SERP via Brave, free tier 2k/mo) |
| `src/collectors/citation_tracker.py` | Módulo 1 — principal. Gera linhas em `citations`. Marca `fictional_hit`; emite eventos para `structured_logger` (Onda 8) |
| `src/collectors/competitor.py` | Módulo 2 — benchmark cross-vertical |
| `src/collectors/serp_overlap.py` | Módulo 3 — **ativo via `ENABLE_SERP_OVERLAP=true`** (Onda 9). Sem toggle ou sem `BRAVE_API_KEY`, pula silently |
| `src/collectors/context_analyzer.py` | Módulo 7 — sentimento, atribuição, hedging |
| `src/logging/logger.py` | `CollectionLogger` estruturado (JSONL rotativo). Aceita `vertical`; exposto via `BaseCollector.structured_logger` lazy (Onda 8) |
| `src/db/schema.sql` | Schema SQLite + Supabase. Índices compostos pós-Migration 0003; `fictional_hit` pós-Migration 0004 |
| `src/db/client.py` | Persistência; ALTER TABLE idempotente inline (0003 + 0004) |
| `src/db/migrate_0003_eficacia_consistencia.py` | Onda 2: `query_type`, 5 índices compostos, backfills |
| `src/db/migrate_0004_fictional_persistence.py` | Double-check #2: `fictional_hit` + índice + backfill retroativo |
| `scripts/export_data.py` | Consolidador — substitui 3 scripts duplicados |
| `scripts/health_check.py` | Gate do pipeline — exit 1 se observações insuficientes |

## Schema em camadas (após Onda 2)

### Core (populado ativamente)
- `citations` (1.244+ linhas) — tabela principal. Colunas relevantes: `vertical`, `llm`, `model`, `model_version`, `query_type` (directive/exploratory), `query_lang`, `cited`, `cited_entity`, `position`, `attribution`, `response_text`
- `finops_usage` (848+) — custo por chamada LLM
- `finops_daily_rollup` — agregado diário por plataforma
- `citation_context` (172+) — análise pós-coleta (sentimento, hedging)
- `collection_runs` — metadata de cada run
- `verticals` — registry de 4 verticais com cohorts

### Schema de futuro (vazio, código parcialmente presente)
- `dual_responses` — comparação JSON vs texto livre (Módulo experimental)
- `model_versions` — rastreio explícito de drift
- `url_verifications` — validação de URLs citadas
- `prompt_variants` — sensibilidade a paráfrase
- `scaling_observations` — comparação entre tamanhos de modelo
- `hypotheses` — pré-registro estatístico
- `interventions` + `intervention_measurements` — Módulo 4 A/B test
- `serp_ai_overlap` — Módulo 3 (aguarda integração Brave Search)
- `competitor_citations` — Módulo 2 grava aqui (populava 0 no audit; revisar)
- `score_calibration_inputs` — ponte com GEO Score Checker

Essas tabelas ficam no schema documentadas como "intencionalmente vazias" até que o Módulo correspondente seja ativado. Não devem ser removidas sem revisão do roadmap.

## Índices (após Onda 2)

Simples:
- `idx_citations_timestamp`, `_llm`, `_query_category`, `_cited`, `_vertical`, `_model_version`, `_query_type`

Compostos (Migration 0003 — preventivo para N > 10K):
- `idx_citations_vertical_cited` — agregação por vertical+cited
- `idx_citations_vertical_llm` — breakdown principal do Paper 1
- `idx_citations_timestamp_vert` — série temporal por vertical
- `idx_citations_llm_modelver` — análise de drift

## Consistência de dados (guardas após Onda 2 e 3)

1. `model_version` sempre preenchido (fallback `= model` se None)
2. `vertical` sempre preenchido em `citations` e `finops_usage` (backfill aplicou)
3. `query_type` preenchido desde Migration 0003 (default 'exploratory' em legado)
4. `mandatory_llms` env var lista os LLMs obrigatórios — falha de provider obrigatório quebra o pipeline (fail-loud)
5. `FICTIONAL_ENTITIES` separadas do cohort principal; `is_fictional()` e `fictional_hit` permitem calcular false-positive rate sem contaminar a série longitudinal principal

## Comandos operacionais

```bash
# Coleta
python -m src.cli collect --all
python -m src.cli collect --module citation --vertical fintech

# Migration (idempotente)
python -m src.db.migrate_0003_eficacia_consistencia --dry-run
python -m src.db.migrate_0003_eficacia_consistencia

# Export consolidado
python scripts/export_data.py --format text
python scripts/export_data.py --format json --output data/dashboard.json
python scripts/export_data.py --format csv --vertical fintech
python scripts/export_data.py --format html

# Health & Sync
python scripts/health_check.py
python scripts/sync_to_supabase.py
```

## Estado das ondas de refactor (atualizado 2026-04-19)

| Onda | Escopo | Status |
|------|--------|--------|
| 1 | Limpeza (audits arquivados + gitignore + CLAUDE.md) | ✓ `b5d63a2` |
| 2 | Migration 0003: `query_type` + 5 índices compostos + backfills | ✓ `726f087` |
| 3 | `FICTIONAL_ENTITIES` + `mandatory_llms` + `query_type` no pipeline | ✓ `fd4d303` |
| 4 | `export_data` consolidado + `test_collectors` reescrito | ✓ `d15b337` |
| 5 | Double-check #1 — merge + sentinelas | ✓ `a777003` |
| 6 | Double-check #2 — `fictional_hit` persistido (Migration 0004) + stratified analysis + auto-migration | ✓ `02a9e78` |
| **7** | **Split `base.py`** em `llm_client` / `response_cache` / `brave_search` / `base` (fachada 85 linhas) | ✓ |
| **8** | **`CollectionLogger` em `BaseCollector.structured_logger` lazy** + aceita vertical | ✓ |
| **9** | **SERP overlap ativável** via `ENABLE_SERP_OVERLAP=true` + `BRAVE_API_KEY` no workflow | ✓ |

## Próximas ondas previsíveis (scope out desta sessão)

1. **Commit shared cache** ou migrar para Redis para economizar 50% API em runners paralelos
2. **Batch API** para queries non-urgent (economiza 50% em OpenAI + Anthropic)
3. **Ativar Brave API em produção** (hoje toggle off por default para proteger cota 2k/mo; basta setar `ENABLE_SERP_OVERLAP=true` como GitHub Actions variable quando quiser ligar)
4. **CollectionLogger global run-level** — hoje integrado por collector; um único run_id atravessando todos os módulos do daily-collect facilitaria correlação de logs
