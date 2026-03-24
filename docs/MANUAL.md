# Manual do Sistema — Papers

## 1. Visão Geral

O **Papers** é uma plataforma de coleta automatizada de dados para pesquisa empírica sobre **como LLMs citam bancos e fintechs brasileiras**. Projetado para gerar datasets longitudinais de 6 a 12 meses que suportem publicação acadêmica peer-reviewed.

**Coorte de estudo:** Nubank, PagBank, Cielo, Stone, Banco Inter, Mercado Pago, Itaú, Bradesco, C6 Bank, PicPay, Ame Digital, Neon, Original, BS2, Safra
**Licença:** MIT

---

## 2. Arquitetura

```
┌─────────────────────────────────────────────────┐
│             GitHub Actions (Cron)                │
│        daily-collect (06:00 BRT)                 │
│        weekly-benchmark (domingo 08:00 BRT)      │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│               CLI (click + rich)                 │
│          python -m src.cli <command>             │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│            7 Módulos de Coleta                   │
│  1. Citation Tracker    5. Time Series           │
│  2. Competitor Bench    6. Statistical Analysis   │
│  3. SERP vs AI Overlap  7. Context Analyzer      │
│  4. Intervention A/B                             │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│          Persistência (SQLite/Supabase)          │
│              + Logging (JSONL)                   │
└─────────────────────────────────────────────────┘
```

---

## 3. Módulos

### 3.1 Citation Tracker (Módulo 1)
**Arquivo:** `src/collectors/citation_tracker.py`
**Função:** Monitora se as entidades da coorte (15 fintechs brasileiras) são citadas em 5 LLMs.
**LLMs:** ChatGPT (OpenAI), Claude (Anthropic), Gemini (Google), Perplexity, Copilot (scraping).
**Dados capturados por query:**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| cited | bool | LLM citou a entidade? |
| cited_entity | bool | Citou o nome da fintech? |
| cited_domain | bool | Citou o domínio oficial? |
| position | int | 1=primeiro terço, 2=meio, 3=final |
| attribution | str | linked, named, paraphrased, none |
| hedging_detected | bool | Linguagem hesitante? |
| response_text | str | Resposta completa |
| sources | array | URLs citadas pelo LLM |

**Comando:** `python -m src.cli collect citation`

### 3.2 Competitor Benchmark (Módulo 2)
**Arquivo:** `src/collectors/competitor.py`
**Função:** Monitora as mesmas queries para todas as 15 entidades da coorte para comparação estatística cruzada.
**Entidades:** Nubank, PagBank, Cielo, Stone, Banco Inter, Mercado Pago, Itaú, Bradesco, C6 Bank, PicPay, Ame Digital, Neon, Original, BS2, Safra.
**Comando:** `python -m src.cli collect competitor`

### 3.3 SERP vs AI Overlap (Módulo 3)
**Arquivo:** `src/collectors/serp_overlap.py`
**Função:** Mede divergência entre Google SERP top 10 e fontes citadas por IA.
**Dependência:** SerpAPI key (opcional, $50/mês ou 100 buscas grátis).
**Comando:** `python -m src.cli collect serp`

### 3.4 Intervention Tracker (Módulo 4)
**Arquivo:** `src/collectors/intervention.py`
**Função:** Framework de A/B testing para otimizações de conteúdo.
**Tipos de intervenção:** schema_org, llms_txt, academic_citations, structured_data, statistics_addition, quotation_addition, entity_fix, combined.
**Comando:** `python -m src.cli intervention add <slug> --type <tipo> --desc "..." --url "..."`

### 3.5 Time Series Persistence (Módulo 5)
**Arquivo:** `src/persistence/timeseries.py`
**Função:** Snapshots diários agregados + health check de dados.
**Meta:** 6+ meses de dados contínuos para análise longitudinal.

### 3.6 Statistical Analysis (Módulo 6)
**Arquivo:** `src/analysis/statistical.py`
**Testes disponíveis:**

| Teste | Uso | Função |
|-------|-----|--------|
| Chi-squared | Comparar taxas de citação entre fintechs | `chi_squared_citation_rate()` |
| T-test | Comparar médias antes/depois | `t_test_means()` |
| ANOVA | Comparar citação entre LLMs | `anova_repeated_measures()` |
| Correlação | Market cap x Citation Rate | `correlation()` |
| Regressão logística | Preditores de citação | `logistic_regression_predictors()` |
| Bonferroni | Correção para comparações múltiplas | `bonferroni_correction()` |

**Comando:** `python -m src.cli analyze report`

### 3.7 Citation Context Analyzer (Módulo 7)
**Arquivo:** `src/collectors/context_analyzer.py`
**Função:** Analisa COMO cada fintech é citada (sentimento, atribuição, precisão factual, hedging).
**Verificações de precisão:** Nome oficial, segmento, posição de mercado.

---

## 4. Queries Padrão

O sistema usa 55 queries padronizadas em 8 categorias:

| Categoria | Queries | Idiomas | Objetivo |
|-----------|---------|---------|----------|
| brand | 4 | EN/PT | Visibilidade da marca |
| entity | 2 | EN/PT | Reconhecimento da entidade |
| concept | 5 | EN/PT | GEO como conceito |
| technical | 5 | EN/PT | Implementação técnica |
| b2a | 2 | EN/PT | Business-to-Agent |
| market | 5 | EN/PT | Mercado e ferramentas |
| academic | 3 | EN | Pesquisa acadêmica |
| fintech | 8 | EN/PT | Ecossistema financeiro |
| fintech_product | 8 | EN/PT | Produtos e serviços |
| fintech_trust | 6 | PT | Reputação e confiança |
| fintech_b2b | 6 | EN/PT | Enterprise e BaaS |

---

## 5. Banco de Dados

### Schema (SQLite / Supabase)
**Arquivo:** `src/db/schema.sql`

| Tabela | Módulo | Registros/dia estimados |
|--------|--------|------------------------|
| citations | 1 | ~220 (55 queries x 4 LLMs) |
| competitor_citations | 2 | ~1.200 (20 queries x 4 LLMs x 15 entidades) |
| serp_ai_overlap | 3 | ~52/semana (13 queries x 4 LLMs) |
| interventions | 4 | Por evento |
| intervention_measurements | 4 | Por evento |
| daily_snapshots | 5 | 1/dia por módulo |
| citation_context | 7 | ~220 (acompanha citations) |
| collection_runs | Meta | 1 por módulo por execução |

### Backup
- GitHub Actions faz upload de artifact (retenção 90 dias para diário, 365 para semanal)
- CSV exportado e commitado diariamente para rastreabilidade em git

---

## 6. Sistema de Logs

### Arquitetura de Logging
**Arquivo:** `src/logging/logger.py`

| Destino | Formato | Nível | Retenção |
|---------|---------|-------|----------|
| Console (Rich) | Human-readable, colorido | INFO+ | Sessão |
| `logs/papers.log` | Texto plain, rotação diária | DEBUG+ | 30 dias |
| `logs/papers.jsonl` | JSON Lines (estruturado) | DEBUG+ | Ilimitado |
| `logs/errors.log` | Texto plain, rotação diária | ERROR+ | 90 dias |
| `logs/run_*.jsonl` | JSONL por execução | ALL | Ilimitado |

### CollectionLogger
Cada execução de coleta gera um `CollectionLogger` com:
- **run_id:** Identificador único (8 chars UUID)
- **Eventos estruturados:** started, query_sent, query_cited, query_not_cited, query_error, completed, fatal
- **Métricas agregadas:** total_queries, total_cited, citation_rate, total_tokens, total_cost_usd, errors, duration_ms
- **Arquivo de run:** `logs/run_{module}_{timestamp}_{run_id}.jsonl`

### Exemplo de log JSONL
```json
{"ts":"2026-03-24T09:00:01Z","level":"INFO","logger":"papers.citation_tracker","message":"Coleta iniciada: citation_tracker","event":{"run_id":"a1b2c3d4","module":"citation_tracker","event":"started"}}
{"ts":"2026-03-24T09:00:03Z","level":"INFO","logger":"papers.citation_tracker","message":"[ChatGPT] What is Nubank?... → CITOU","event":{"run_id":"a1b2c3d4","module":"citation_tracker","event":"query_cited","llm":"ChatGPT","cited":true,"duration_ms":1234,"tokens":450}}
```

---

## 7. GitHub Actions

### daily-collect.yml
- **Cron:** 09:00 UTC (06:00 BRT)
- **Módulos:** Citation Tracker + Competitor Benchmark (4 LLMs)
- **FinOps:** Rollup + budget check + dashboard
- **Relatório:** Enviado automaticamente por email para caramaschiai@caramaschiai.io
- **Artifact:** `papers-db-{run}` (90 dias)
- **Commit:** CSV + docs + FinOps commitados automaticamente

### weekly-benchmark.yml
- **Cron:** Domingo 11:00 UTC (08:00 BRT)
- **Módulos:** Todos (SERP Overlap + coleta completa + análise estatística)
- **Relatório:** Enviado por email com métricas semanais acumuladas
- **Artifact:** `weekly-report-{run}` (365 dias)

### Relatório por Email
Após cada coleta (diária e semanal), um relatório HTML é enviado automaticamente via Resend API com:
- Taxa de citação do dia e acumulada
- Custo e tokens por plataforma (FinOps)
- Status de cada execução (módulo, registros, duração)
- Alertas de orçamento ativos
- Script: `scripts/send-report.py`

---

## 8. Configuração

### Variáveis de Ambiente

| Variável | Obrigatória | Descrição |
|----------|-------------|-----------|
| OPENAI_API_KEY | Sim | ChatGPT gpt-4o-mini ($0,15/$0,60 MTok) |
| ANTHROPIC_API_KEY | Sim | Claude haiku-4.5 ($1/$5 MTok, $55 crédito) |
| GOOGLE_AI_API_KEY | Sim | Gemini 2.5 Flash ($0,15/$0,60 MTok, billing Cloud ativo) |
| PERPLEXITY_API_KEY | Sim | Perplexity sonar ($1/$1 MTok + $0,005/busca, $89 crédito) |
| RESEND_API_KEY | Sim | Envio de relatórios diários por email |
| FINOPS_ALERT_EMAIL | Sim | Destino dos relatórios (caramaschiai@caramaschiai.io) |
| SERPAPI_KEY | Opcional | Google SERP data (substituído por Brave Search grátis) |
| SUPABASE_URL | Opcional | Persistência cloud |
| SUPABASE_KEY | Opcional | Persistência cloud |
| PAPERS_DB_PATH | Opcional | Caminho SQLite (default: data/papers.db) |
| PAPERS_LOG_DIR | Opcional | Diretório de logs (default: logs/) |

### GitHub Secrets (configurados)
- OPENAI_API_KEY
- ANTHROPIC_API_KEY
- GOOGLE_AI_API_KEY

---

## 9. Comandos CLI

```bash
# === Setup ===
pip install -e ".[dev]"          # Instalar dependências
python -m src.cli db migrate     # Aplicar schema

# === Coleta ===
python -m src.cli collect all        # Todos os módulos
python -m src.cli collect citation   # Só Citation Tracker
python -m src.cli collect competitor # Só Competitor Benchmark
python -m src.cli collect serp       # Só SERP vs AI Overlap

# === Análise ===
python -m src.cli analyze report     # Relatório estatístico

# === Intervenções ===
python -m src.cli intervention add teste-nubank --type schema_org --desc "Teste Schema.org em página Nubank" --url "https://nubank.com.br/sobre"

# === Banco de Dados ===
python -m src.cli db migrate         # Aplicar/atualizar schema
python -m src.cli db export --format csv  # Exportar dados
python -m src.cli db health          # Verificar saúde dos dados

# === Testes ===
pytest tests/ -v                     # Rodar todos os testes
```

---

## 10. Custo Operacional

| Provedor | Custo/mês | Queries/dia |
|----------|-----------|-------------|
| OpenAI (gpt-4o) | ~$3 | 55 |
| Anthropic (Claude Sonnet) | ~$2 | 55 |
| Google AI (Gemini Flash) | $0 | 55 |
| Perplexity (Sonar) | ~$5 | 55 |
| **Total estimado** | **~$10/mês** | **220** |

---

## 11. Roadmap (12 meses)

| Mês | Marco | Dados acumulados |
|-----|-------|------------------|
| 1 | Setup + primeiras coletas diárias | ~6.600 citações |
| 2 | Baseline estável, primeiras intervenções | ~13.200 |
| 3 | Relatório trimestral, first draft do paper | ~19.800 |
| 6 | Dataset longitudinal robusto, submissão ArXiv | ~39.600 |
| 9 | Peer review, dados cross-platform completos | ~59.400 |
| 12 | Publicação, dataset público, replicabilidade | ~79.200 |
