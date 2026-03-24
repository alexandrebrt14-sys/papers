# Plano de Desenvolvimento — Papers

**Versão:** 1.0
**Data:** 2026-03-24
**Autor:** Alexandre Caramaschi — CEO da Brasil GEO
**Repositório:** github.com/alexandrebrt14-sys/papers

---

## 1. Visão Geral

### 1.1 Propósito do Documento

Este documento define o plano de desenvolvimento incremental da plataforma **Papers** — infraestrutura de coleta e análise de dados empíricos para pesquisa acadêmica em Generative Engine Optimization (GEO). O plano é estruturado em fases com critérios de aceitação mensuráveis.

### 1.2 Estado Atual

| Dimensão | Valor | Meta |
|----------|-------|------|
| Linhas de código | 4.609 | — |
| Módulos funcionais | 7/10 | 10/10 |
| Testes unitários | 19 | 80+ |
| Cobertura estimada | ~35% | >80% |
| LLMs coletando | 0/4 | 4/4 |
| Citações acumuladas | 0 | 10.000+ |
| Dias de coleta contínua | 0 | 180+ |
| Artigos submetidos | 0 | 2+ |

### 1.3 Bloqueadores Atuais (P0)

1. **API keys sem créditos** — OpenAI (billing inativo), Anthropic (sem créditos), Gemini (quota 0 no workspace)
2. **GitHub Secrets não configurados** — 5 secrets necessários para CI/CD
3. **Bug em `intervention add`** — passa objetos LLMConfig em vez de strings de query
4. **Path hardcoded** — `update-docs.py` referencia path Windows que falha no CI/CD (Ubuntu)

---

## 2. Arquitetura Alvo

```
┌──────────────────────────────────────────────────────────────────┐
│                    GitHub Actions (3 workflows)                    │
│   daily-collect (06:00) · weekly-benchmark (dom 08:00)           │
│   finops-monitor (cada 6h)                                        │
└─────────────────────┬────────────────────────────────────────────┘
                      │
┌─────────────────────▼────────────────────────────────────────────┐
│                      CLI (click + rich)                            │
│   collect · analyze · db · intervention · finops                  │
└─────────────────────┬────────────────────────────────────────────┘
                      │
┌─────────────────────▼────────────────────────────────────────────┐
│                   Camada de Coleta                                 │
│  ┌─────────────┐ ┌──────────────┐ ┌────────────┐ ┌────────────┐ │
│  │ Citation     │ │ Competitor   │ │ SERP vs AI │ │ Context    │ │
│  │ Tracker      │ │ Benchmark    │ │ Overlap    │ │ Analyzer   │ │
│  └──────┬──────┘ └──────┬───────┘ └─────┬──────┘ └─────┬──────┘ │
│         └────────────────┼───────────────┼──────────────┘        │
│                    ┌─────▼─────┐                                  │
│                    │ LLMClient │ ← FinOps pre/post hooks          │
│                    │ (httpx)   │                                   │
│                    └───────────┘                                   │
└─────────────────────┬────────────────────────────────────────────┘
                      │
┌─────────────────────▼────────────────────────────────────────────┐
│                   Camada de Persistência                          │
│  ┌───────────┐ ┌──────────────┐ ┌──────────────┐                │
│  │ SQLite    │ │ Time Series  │ │ FinOps DB    │                │
│  │ (11 tab)  │ │ Manager      │ │ (4 tabelas)  │                │
│  └───────────┘ └──────────────┘ └──────────────┘                │
└─────────────────────┬────────────────────────────────────────────┘
                      │
┌─────────────────────▼────────────────────────────────────────────┐
│                   Camada de Análise                               │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────────────┐ │
│  │ Statistical  │ │ Visualization│ │ Intervention Tracker     │ │
│  │ (scipy/sm)   │ │ (mpl/sns)    │ │ (A/B framework)          │ │
│  └──────────────┘ └──────────────┘ └──────────────────────────┘ │
└─────────────────────┬────────────────────────────────────────────┘
                      │
┌─────────────────────▼────────────────────────────────────────────┐
│                   Observabilidade                                 │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────────────┐ │
│  │ FinOps       │ │ Security     │ │ Collection Logger        │ │
│  │ Monitor      │ │ Audit        │ │ (JSONL + Rich)           │ │
│  └──────────────┘ └──────────────┘ └──────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

---

## 3. Fases de Desenvolvimento

### Fase 0 — Desbloqueio (Semana 1)

**Objetivo:** Tornar o sistema operacional com coleta real de dados.

| ID | Tarefa | Tipo | Critério de Aceitação |
|----|--------|------|----------------------|
| P0-01 | Adicionar créditos OpenAI ($5) | Infra | `collect citation` retorna dados reais |
| P0-02 | Adicionar créditos Anthropic ($5) | Infra | Claude responde queries via API |
| P0-03 | Gerar Gemini API key em conta Gmail pessoal | Infra | Gemini responde queries (free tier) |
| P0-04 | Configurar 5 GitHub Secrets | Infra | `daily-collect.yml` roda sem erro |
| P0-05 | Corrigir bug `intervention add` (cli.py:255) | Bug fix | `config.llms[:5]` → `STANDARD_QUERIES[:5]` |
| P0-06 | Remover hardcoded path Windows em update-docs.py | Bug fix | Script funciona no Ubuntu (CI/CD) |
| P0-07 | Primeira coleta completa (manual) | Validação | `python -m src.cli collect all` retorna >0 citações |
| P0-08 | Confirmar CI/CD funcionando | Validação | `daily-collect.yml` dispara e commita dados |

**Entrega:** Sistema coletando dados diariamente em 4 LLMs.
**Estimativa:** 2-4 horas de trabalho + tempo de ativação de billing.

---

### Fase 1 — Completude Funcional (Semanas 2-3)

**Objetivo:** Todos os módulos integrados e funcionais.

| ID | Tarefa | Tipo | Critério de Aceitação | Dependência |
|----|--------|------|-----------------------|-------------|
| F1-01 | Integrar CitationContextAnalyzer no pipeline `collect_all` | Feature | `citation_context` table populada após coleta | P0-07 |
| F1-02 | Implementar `insert_interventions()` e `insert_intervention_measurements()` no DatabaseClient | Feature | `intervention add` persiste no banco | P0-05 |
| F1-03 | Implementar `check_interventions()` no InterventionTracker | Feature | Intervenções ativas medidas automaticamente na coleta diária | F1-02 |
| F1-04 | Adicionar comando CLI `analyze visualize` | Feature | Gera 5 gráficos PNG em `output/` | — |
| F1-05 | Integrar CollectionLogger nos coletores | Feature | Cada coleta gera `logs/run_*.jsonl` com run_id e custo | — |
| F1-06 | Corrigir `check_anthropic_balance()` | Bug fix | Usa endpoint `/v1/models` (gratuito, sem consumo) | — |
| F1-07 | Adicionar `concurrency:` nos 3 workflows | Bug fix | Race condition de git push eliminada | — |
| F1-08 | Remover dependências mortas do pyproject.toml | Cleanup | `openai`, `anthropic`, `google-genai`, `supabase` removidas | — |
| F1-09 | Alinhar `cost_per_1k_tokens` em config.py com pricing real | Bug fix | `price_drift` warning desaparece do checkpoint | — |

**Entrega:** 10/10 módulos funcionais, zero warnings no monitor.
**Estimativa:** 8-12 horas.

---

### Fase 1.5 — Rigor Metodológico (Semana 3) — RECOMENDADA POR PAINEL DE ESPECIALISTAS

**Objetivo:** Corrigir falhas metodológicas identificadas por revisão de nível SIGIR/TOIS.
**Contexto:** Simulação de revisão por Bengio, Hinton, LeCun, Karpathy, Gomez e Kaplan.

| ID | Tarefa | Inspirado por | Status | Critério de Aceitação |
|----|--------|---------------|--------|-----------------------|
| M-01 | Coleta dual (JSON + linguagem natural) | Hinton | Implementado | `dual_collector.py` coleta ambas as respostas, mede Jaccard de self-report vs orgânico |
| M-02 | Separar análise RAG vs paramétrico | Gomez | Implementado | `citation_type` campo em dual_responses (parametric/retrieval/none) |
| M-03 | Verificação de URLs (alucinação de fontes) | Gomez | Implementado | `url_verifier.py` faz HTTP HEAD em cada URL retornada, calcula hallucination_rate |
| M-04 | Detecção de drift de modelos | Hinton, Karpathy | Implementado | `drift_detector.py` registra version strings + hashes de resposta, alerta em mudanças |
| M-05 | Análise de sensibilidade ao prompt | Bengio | Implementado | `prompt_sensitivity.py` testa 11 variantes parafraseadas, mede agreement rate |
| M-06 | Corrigir ANOVA para between-groups + Mann-Whitney para dados ordinais | Karpathy | Implementado | `anova_between_groups()` com Levene test + fallback Kruskal-Wallis; `mann_whitney_position()` para posição ordinal |
| M-07 | Schema v2 para dados metodológicos | Todos | Implementado | 6 tabelas novas: dual_responses, model_versions, url_verifications, prompt_variants, scaling_observations, hypotheses |
| M-08 | Pré-registrar hipóteses no OSF | Todos | Planejado | Tabela `hypotheses` no banco + registro externo em osf.io |
| M-09 | Análise de poder a priori | Todos | Planejado | Cálculo de n mínimo por efeito esperado antes de cada experimento |
| M-10 | DAG causal + Difference-in-Differences | Bengio | Planejado | Formalizar mecanismo causal, usar DiD com URLs controle do mesmo domínio |
| M-11 | Scaling analysis (modelos maiores) | Kaplan | Planejado | Adicionar gpt-4o + sonnet semanal, plotar citation rate vs model size |
| M-12 | Validar sentiment com anotação humana + Cohen's kappa | LeCun | Planejado | Anotar 200 respostas manualmente, calcular inter-rater reliability |

**Entrega:** 7 módulos implementados (M-01 a M-07), 5 planejados para execução durante Fase 3.

---

### Fase 2 — Qualidade e Resiliência (Semanas 3-4)

**Objetivo:** Cobertura de testes >80%, resiliência em produção.

| ID | Tarefa | Tipo | Critério de Aceitação | Dependência |
|----|--------|------|-----------------------|-------------|
| F2-01 | Testes para `db/client.py` (insert + query) | Testes | 10+ testes, DB in-memory | F1-02 |
| F2-02 | Testes para `finops/tracker.py` (record, budget, circuit breaker) | Testes | 12+ testes com mocks | — |
| F2-03 | Testes para `finops/monitor.py` (rollup, stale, pricing) | Testes | 8+ testes | F2-02 |
| F2-04 | Testes para `finops/secrets.py` (mask, fingerprint, scan) | Testes | 6+ testes | — |
| F2-05 | Testes para `persistence/timeseries.py` | Testes | 5+ testes | F2-01 |
| F2-06 | Testes para `collectors/base.py` (LLMClient com mocks httpx) | Testes | 8+ testes com resptest | — |
| F2-07 | Implementar retry com backoff exponencial no LLMClient | Feature | 3 retries com jitter, log de cada tentativa | — |
| F2-08 | Adicionar workflow de testes (`pytest.yml`) | CI/CD | Testes rodam em cada push/PR | F2-01..F2-06 |
| F2-09 | Adicionar GitHub Action para `ruff` lint | CI/CD | Lint automático em cada push | — |
| F2-10 | Adicionar type checking (`mypy` ou `pyright`) | CI/CD | Zero erros de tipo | — |

**Entrega:** >80 testes, cobertura >80%, CI com lint + type check + tests.
**Estimativa:** 16-24 horas.

---

### Fase 3 — Dados e Análise (Semanas 4-12)

**Objetivo:** Acumular dados suficientes para publicação.

| ID | Tarefa | Tipo | Critério de Aceitação | Dependência |
|----|--------|------|-----------------------|-------------|
| F3-01 | Acumular 30 dias de coleta contínua | Operacional | 30 snapshots diários no banco | P0-08 |
| F3-02 | Primeiro experimento A/B (adicionar Schema.org) | Pesquisa | Baseline + treatment com >50 medições cada | F1-03, F3-01 |
| F3-03 | Acumular 1.000 citações | Operacional | `citations` table com 1.000+ rows | F3-01 |
| F3-04 | Primeiro relatório estatístico com significância | Pesquisa | p < 0.05 em pelo menos 1 teste | F3-03 |
| F3-05 | Gerar dataset CSV reprodutível | Pesquisa | `data/exports/` com CSV + metadados | F3-03 |
| F3-06 | Acumular 90 dias de coleta contínua | Operacional | Série temporal robusta | F3-01 |
| F3-07 | Segundo experimento A/B (llms.txt vs sem llms.txt) | Pesquisa | Baseline + treatment completos | F3-06 |
| F3-08 | Análise de divergência SERP vs IA (com dados) | Pesquisa | >12 semanas de dados de overlap | F3-06 |

**Entrega:** 90+ dias de dados, 2 experimentos A/B, dataset reprodutível.
**Estimativa:** 12 semanas (execução contínua automatizada).

---

### Fase 4 — Publicação (Semanas 12-20)

**Objetivo:** Submeter 2 artigos acadêmicos.

| ID | Tarefa | Tipo | Critério de Aceitação | Dependência |
|----|--------|------|-----------------------|-------------|
| F4-01 | Redigir preprint: "How LLMs Cite Entities" | Publicação | Preprint completo com abstract, metodologia, resultados | F3-06 |
| F4-02 | Submeter ao ArXiv | Publicação | ArXiv ID atribuído | F4-01 |
| F4-03 | Redigir paper: "GEO vs SEO: Source Divergence" | Publicação | Paper completo com gráficos publication-quality | F3-08 |
| F4-04 | Submeter a conferência (SIGIR/WWW/WSDM) | Publicação | Submissão confirmada | F4-03 |
| F4-05 | Redigir paper: "Content Interventions for AI Visibility" | Publicação | Paper com resultados dos experimentos A/B | F3-07 |
| F4-06 | Submeter a journal (Information Sciences / JASIST) | Publicação | Submissão confirmada | F4-05 |

**Entrega:** 1 preprint no ArXiv + 2 submissões a venues peer-reviewed.
**Estimativa:** 8 semanas de redação.

---

## 4. Backlog Técnico (sem fase atribuída)

| ID | Tarefa | Prioridade | Justificativa |
|----|--------|-----------|---------------|
| BL-01 | Implementar Supabase sync como backup | Baixa | Redundância; SQLite é suficiente para volume atual |
| BL-02 | Implementar Copilot scraping (Playwright) | Baixa | Copilot não tem API pública; scraping é frágil |
| BL-03 | Pricing validation ao vivo via APIs de billing | Baixa | Pricing muda ~2x/ano; validação manual é suficiente |
| BL-04 | Dashboard web interativo (Streamlit ou FastAPI) | Média | Atualmente HTML estático; útil quando houver stakeholders |
| BL-05 | Export para formato LaTeX (tabelas e gráficos) | Média | Acelera redação de papers; pode ser feito manualmente |
| BL-06 | API REST para consulta de dados (FastAPI) | Baixa | Útil se outros pesquisadores quiserem acessar dados |
| BL-07 | Integração com Zotero/Mendeley para gestão de referências | Baixa | Facilita citações nos papers |

---

## 5. Métricas de Progresso

### 5.1 Métricas Técnicas (auto-atualizadas pelo sistema)

| Métrica | Fonte | Frequência |
|---------|-------|-----------|
| Linhas de código | `update-docs.py` → CHANGELOG.md | Diária |
| Testes passando | `pytest.yml` (futuro) → badge | Push |
| Cobertura de testes | `pytest-cov` (futuro) → badge | Push |
| Citações acumuladas | `finops_checkpoint.json` → STATUS.md | Diária |
| Gasto mensal | `finops_checkpoint.json` → GOVERNANCE.md | 6h |
| Dias de coleta contínua | `collection_runs` table | Diária |
| Alertas disparados | `finops_alerts.jsonl` | 6h |

### 5.2 Métricas de Pesquisa (manuais)

| Métrica | Meta | Tracking |
|---------|------|----------|
| Citações com p < 0.05 | 1+ testes | Relatório semanal |
| Experimentos A/B completos | 2+ | docs/GOVERNANCE.md |
| Papers submetidos | 2+ | docs/GOVERNANCE.md |
| Papers aceitos | 1+ | — |

---

## 6. Riscos e Mitigações

| Risco | Probabilidade | Impacto | Mitigação |
|-------|-------------|---------|-----------|
| APIs mudam formato de resposta | Média | Alto | Testes de integração semanais; extract_tokens() com fallback |
| Créditos API acabam | Alta | Crítico | FinOps com hard stop a 95%; alertas em 70% |
| GitHub Actions falha silenciosamente | Média | Alto | finops-monitor.yml independente a cada 6h; stale data detection |
| Preços de API aumentam | Baixa | Médio | Budget limits configuraveis; pricing validation no monitor |
| Paper rejeitado | Alta | Médio | Submeter a 2+ venues; dataset aberto para reprodutibilidade |
| Key vazada | Baixa | Crítico | secrets.py scan a cada 6h; keys em GitHub Secrets, nunca em código |

---

## 7. Definição de Pronto (DoD)

Uma tarefa é considerada **pronta** quando:

1. Código commitado e pushed para `main`
2. Testes existentes passam (zero regressão)
3. Novos testes escritos para código novo (quando aplicável)
4. Documentação atualizada via `update-docs.py`
5. FinOps checkpoint reflete mudança (se aplicável)
6. Nenhum warning novo no `finops monitor`

---

## 8. Calendário Resumido

```
Semana 1    ████████░░  Fase 0: Desbloqueio (keys, secrets, bugs)
Semana 2-3  ████████░░  Fase 1: Completude funcional (10/10 módulos)
Semana 3-4  ████████░░  Fase 2: Qualidade (80+ testes, CI/CD completo)
Semana 4-12 ████████████████████████  Fase 3: Acumulação de dados (90 dias)
Semana 12-20 ████████████████  Fase 4: Publicação (2 papers)
```

**Marco crítico:** Semana 1 — primeira coleta real com 4 LLMs.
**Marco de pesquisa:** Semana 12 — 90 dias de dados, primeiro preprint.
**Marco final:** Semana 20 — 2 submissões a venues peer-reviewed.

---

## 9. Dependências Externas

| Dependência | Responsável | Status | Bloqueio |
|-------------|-----------|--------|----------|
| OpenAI billing ($5+) | Alexandre | Pendente | Fase 0 |
| Anthropic credits ($5+) | Alexandre | Pendente | Fase 0 |
| Gemini API (conta Gmail) | Alexandre | Pendente | Fase 0 |
| Perplexity credits ($5+) | Alexandre | Pendente | Fase 0 |
| SerpAPI key | Alexandre | Pendente | Fase 3 |
| RESEND_API_KEY | Já existe (Vercel) | Copiar para Secrets | Fase 0 |
| ArXiv account | Alexandre | Pendente | Fase 4 |
| ORCID | Já existe (0009-0004-9150-485X) | OK | — |

---

*Documento gerado automaticamente e mantido em docs/DEVELOPMENT_PLAN.md.*
*Atualizações são commitadas via `scripts/update-docs.py`.*

**Brasil GEO** — [brasilgeo.ai](https://brasilgeo.ai) · [alexandrecaramaschi.com](https://alexandrecaramaschi.com)
