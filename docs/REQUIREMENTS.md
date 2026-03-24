# Especificação de Requisitos — Papers

**Versão:** 2.0
**Atualizado:** 2026-03-24

---

## 1. Objetivo do Sistema

Plataforma de coleta, persistência e análise de dados empíricos para pesquisa acadêmica sobre **como LLMs citam bancos e fintechs brasileiras**. Gera datasets longitudinais que suportam publicação peer-reviewed em conferências tier-1 e journals.

**Coorte de estudo:** Nubank, PagBank, Cielo, Stone, Banco Inter, Mercado Pago, Itaú, Bradesco, C6 Bank, PicPay, Ame Digital, Neon, Original, BS2, Safra

## 2. Requisitos Funcionais

### RF-01: Coleta Multi-LLM
- **Prioridade:** Crítica
- **Status:** Implementado
- **Descrição:** Monitorar citações das 15 entidades fintech em 5 LLMs: ChatGPT, Claude, Gemini, Perplexity, Copilot
- **Métricas capturadas:** cited (bool), position, attribution, hedging, sentiment, source_count, latency_ms, token_count
- **Frequência:** Diária (06:00 BRT via GitHub Actions)

### RF-02: Benchmark Competitivo (Coorte Completa)
- **Prioridade:** Crítica
- **Status:** Implementado
- **Descrição:** Monitorar as 15 entidades da coorte nas mesmas queries para comparação estatística cruzada
- **Entidades:** Nubank, PagBank, Cielo, Stone, Banco Inter, Mercado Pago, Itaú, Bradesco, C6 Bank, PicPay, Ame Digital, Neon, Original, BS2, Safra
- **Frequência:** Diária

### RF-03: Comparação SERP vs IA
- **Prioridade:** Alta
- **Status:** Implementado
- **Descrição:** Medir divergência entre resultados tradicionais do Google e fontes citadas por LLMs (Jaccard index)
- **Dependência:** SerpAPI key
- **Frequência:** Semanal (domingo 08:00 BRT)

### RF-04: Experimentos de Conteúdo (A/B)
- **Prioridade:** Alta
- **Status:** Implementado
- **Descrição:** Framework para registrar intervenções de conteúdo e medir impacto na citação
- **Tipos:** schema_org, llms_txt, academic_citations, structured_data, statistics_addition, quotation_addition, entity_fix, combined
- **Medições:** baseline (dia 0), +7, +14, +30 dias

### RF-05: Análise Estatística Publicável
- **Prioridade:** Crítica
- **Status:** Implementado
- **Descrição:** Testes de significância prontos para peer review
- **Testes:** Chi-squared, T-test (paired/independent), Pearson/Spearman, ANOVA, Regressão logística, Bonferroni
- **Effect sizes:** Cohen's d, Cramer's V, eta-squared
- **Output:** Gráficos 300 DPI publication-quality

### RF-06: Análise de Contexto de Citação
- **Prioridade:** Alta
- **Status:** Implementado
- **Descrição:** Análise qualitativa de COMO cada fintech é citada (sentimento, atribuição, precisão factual, hedging)
- **Detecção:** 30+ padrões regex em PT-BR + EN

### RF-07: Persistência de Série Temporal
- **Prioridade:** Crítica
- **Status:** Implementado
- **Descrição:** Snapshots diários para análise longitudinal (6-12 meses)
- **Storage:** SQLite local + Supabase (futuro)
- **Retenção:** Ilimitada (dados são o produto da pesquisa)

### RF-08: FinOps e Governança de Custos
- **Prioridade:** Alta
- **Status:** Implementado (scripts/python/)
- **Descrição:** Tracking de tokens/custos por plataforma, limites de gasto, alertas por email
- **Limites:** $10/plataforma/mês, $30 global, hard stop em 95%
- **Alertas:** Email em 70% (warning), 90% (critical), 100% (exceeded)
- **Dashboard:** HTML com painel por plataforma

### RF-09: Documentação Automatizada
- **Prioridade:** Alta
- **Status:** Implementado
- **Descrição:** Atualização automática de changelog, métricas, governança a cada coleta
- **Script:** scripts/update-docs.py
- **Trigger:** Post-collection no CI/CD

## 3. Requisitos Não-Funcionais

### RNF-01: Custo Operacional
- Budget máximo: $30/mês (todas as APIs)
- Hard stop automático em 95% do limite
- Alertas proativos em 70% e 90%

### RNF-02: Reprodutibilidade
- Todas as queries padronizadas e versionadas
- Seeds fixos onde aplicável
- Schema SQL versionado no repositório

### RNF-03: Observabilidade
- Logging estruturado (JSONL) com run_id
- Console output rico (rich)
- Rotação automática de logs (30/90 dias)

### RNF-04: Tolerância a Falhas
- Degradação graciosa quando API key ausente
- Retry com backoff (futuro)
- Fallback SQLite quando Supabase indisponível

### RNF-05: Conformidade Acadêmica
- Datasets exportáveis em CSV (R, SPSS, pandas)
- Gráficos em formato publicável (PNG 300 DPI)
- Relatórios com p-values e effect sizes

## 4. Queries Monitoradas

| Categoria | Quantidade | Idiomas |
|-----------|-----------|---------|
| Brand | 4 | PT-BR + EN |
| Entity | 4 | PT-BR + EN |
| Concept | 8 | PT-BR + EN |
| Technical | 6 | PT-BR + EN |
| B2A | 4 | PT-BR + EN |
| Market | 6 | PT-BR + EN |
| Academic | 8 | PT-BR + EN |
| Fintech | 15 | PT-BR |
| **Total** | **55** | — |

## 5. Stack Tecnológica

| Componente | Tecnologia | Versão |
|-----------|-----------|--------|
| Linguagem | Python | >= 3.11 |
| CLI | click + rich | >= 8.1, >= 13.7 |
| HTTP | httpx | >= 0.27 |
| LLM SDKs | openai, anthropic, google-genai | latest |
| Banco | SQLite + Supabase | — |
| Análise | scipy, statsmodels, pandas | >= 1.13, >= 0.14, >= 2.2 |
| Visualização | matplotlib, seaborn | >= 3.9, >= 0.13 |
| CI/CD | GitHub Actions | — |
| Testes | pytest | >= 8.0 |

## 6. Histórico de Versões

| Versão | Data | Mudanças |
|--------|------|----------|
| 1.0 | 2026-03-24 | Infraestrutura inicial: 7 módulos, schema, CLI, CI/CD |
| 1.1 | 2026-03-24 | 15 fintechs na coorte + 28 queries + setup scripts |
| 1.2 | 2026-03-24 | Sistema de logging estruturado + manual |
| 2.0 | 2026-03-24 | FinOps, governança automatizada, documentação evolutiva |
