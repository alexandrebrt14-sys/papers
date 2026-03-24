# Papers — Pesquisa Empírica Multi-Vertical sobre Citações de LLMs em Empresas Brasileiras

Plataforma de coleta, persistência e análise de dados para pesquisa acadêmica sobre **como LLMs citam empresas brasileiras** em 4 setores da economia — Fintech, Varejo, Saúde e Tecnologia.

Estudo longitudinal focado em padrões de citação, visibilidade e atribuição de fontes por motores de busca generativos (Generative Engine Optimization — GEO) com framework multi-vertical.

## Verticais e Coortes de Estudo

### Fintech (16 entidades)
Nubank, PagBank, Cielo, Stone, Banco Inter, Mercado Pago, Itaú, Bradesco, C6 Bank, PicPay, Ame Digital, Neon, Original, BS2, Safra, Banco Carrefour

### Varejo (15 entidades)
Magazine Luiza, Casas Bahia, Mercado Livre, Amazon Brasil, Shopee Brasil, Americanas, Carrefour, Pão de Açúcar, Renner, Riachuelo, C&A Brasil, Havan, Leroy Merlin, Netshoes, Dafiti

### Saúde (15 entidades)
Dasa, Hapvida, Unimed, Fleury, Rede D'Or, Einstein, Sírio-Libanês, Mater Dei, Hermes Pardini, Sabin, Amil, SulAmérica Saúde, Prevent Senior, HCor, A.C. Camargo

### Tecnologia (15 entidades)
Tivit, Totvs, Stefanini, Accenture, CI&T, Globant, Softplan, Linx, Locaweb, Movile, iFood Tech, Vtex, RD Station, Involves, Tempest Security

**Total: 61 entidades monitoradas em 4 LLMs**

## Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Actions (Cron)                     │
│         daily-collect (06:00 BRT) · weekly-benchmark         │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                  CLI (click + rich)                           │
│        python -m src.cli <command> [--vertical <v>]          │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                  7 Módulos de Coleta                          │
│                                                              │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────────┐ │
│  │ 1. Citation   │ │ 2. Multi-    │ │ 3. SERP vs AI        │ │
│  │    Tracker    │ │    Vertical  │ │    Overlap           │ │
│  │ (4 LLMs API) │ │  Benchmark   │ │ (divergência)        │ │
│  └──────────────┘ └──────────────┘ └──────────────────────┘ │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────────┐ │
│  │ 4. Content   │ │ 6. Statistical│ │ 7. Citation          │ │
│  │  Intervention│ │    Analysis  │ │    Context           │ │
│  │  (A/B test)  │ │ (scipy)      │ │    Analyzer          │ │
│  └──────────────┘ └──────────────┘ └──────────────────────┘ │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│           5. Persistência + Logging                          │
│     SQLite/Supabase · JSONL structured · Rich console        │
│     Rotação diária · 30d texto · 90d erros                   │
│     Coluna `vertical` em todas as tabelas de citação         │
└─────────────────────────────────────────────────────────────┘
```

## Status

| # | Módulo | Função | Status |
|---|--------|--------|--------|
| 1 | Multi-LLM Citation Tracker | Citações em ChatGPT, Claude, Gemini, Perplexity (4 verticais) | Pronto |
| 2 | Multi-Vertical Benchmark | Coorte: 61 entidades em 4 verticais | Pronto |
| 3 | SERP vs AI Overlap | Divergência Google SERP vs respostas IA por vertical | Pronto |
| 4 | Intervention Tracker | A/B testing de otimizações (schema, llms.txt, citações) | Pronto |
| 5 | Time Series Persistence | SQLite + Supabase, snapshots diários, 6-12 meses | Pronto |
| 6 | Statistical Analysis | Chi-squared, t-test, ANOVA, regressão logística, viz | Pronto |
| 7 | Citation Context Analyzer | Sentimento, atribuição, precisão factual, hedging | Pronto |

## API Keys Configuradas

| Provedor | Modelo | Status | Custo |
|----------|--------|--------|-------|
| OpenAI | gpt-4o | GitHub Secret | ~$3/mês |
| Anthropic | claude-sonnet-4 | GitHub Secret | ~$2/mês |
| Google AI | gemini-2.5-flash | GitHub Secret | Grátis |
| Perplexity | sonar | Pendente | ~$5/mês |

## Queries: 55 padronizadas por vertical

8 categorias: brand, entity, concept, technical, b2a, market, academic, vertical-specific (product/trust/b2b)

Com 4 verticais: ~880 queries/dia (55 x 4 LLMs x 4 verticais, execução sequencial)

## Observabilidade

| Destino | Formato | Retenção |
|---------|---------|----------|
| Console | Rich (colorido) | Sessão |
| `logs/papers.log` | Texto, rotação diária | 30 dias |
| `logs/papers.jsonl` | JSON Lines estruturado | Ilimitado |
| `logs/errors.log` | Erros, rotação diária | 90 dias |
| `logs/run_*.jsonl` | Log completo por execução | Ilimitado |

Cada execução gera um `run_id` para rastreabilidade. Eventos estruturados: started, query_cited, query_not_cited, query_error, completed.

## FinOps — Governança de Custos

Sistema integrado de controle financeiro para APIs de LLM:

- **Dashboard HTML** com painel por plataforma (gasto, tokens, queries)
- **Limites automáticos**: $10/plataforma/mês, $30 global, hard stop em 95%
- **Alertas por email**: 70% warning, 90% critical, 100% exceeded
- **Tracking por token**: custo calculado por modelo com tabela de preços atualizada
- **Execução sequencial por vertical**: mantém o orçamento dentro do limite global de $30/mês

## Documentação Evolutiva

| Documento | Descrição |
|-----------|-----------|
| [docs/REQUIREMENTS.md](docs/REQUIREMENTS.md) | Especificação formal de requisitos (RF/RNF) |
| [docs/CHANGELOG.md](docs/CHANGELOG.md) | Histórico de mudanças com métricas auto-atualizadas |
| [docs/GOVERNANCE.md](docs/GOVERNANCE.md) | Políticas de gasto, ADRs, roadmap de publicação |
| [docs/STATUS.md](docs/STATUS.md) | Snapshot de saúde do projeto (auto-gerado) |
| [docs/MANUAL.md](docs/MANUAL.md) | Manual operacional completo |
| [docs/DEVELOPMENT_PLAN.md](docs/DEVELOPMENT_PLAN.md) | Plano de desenvolvimento em 4 fases com critérios de aceitação |

Documentação atualizada automaticamente após cada coleta via `scripts/update-docs.py`.

## Setup

```bash
pip install -e ".[dev]"
python -m src.cli db migrate
python -m src.cli collect all
```

## Comandos

```bash
# Coleta (todas as verticais)
python -m src.cli collect all                        # Todos os módulos, todas as verticais
python -m src.cli collect all --vertical fintech     # Todos os módulos, só fintech
python -m src.cli collect all --vertical varejo      # Todos os módulos, só varejo
python -m src.cli collect all --vertical saude       # Todos os módulos, só saúde
python -m src.cli collect all --vertical tecnologia  # Todos os módulos, só tecnologia

# Coleta (módulo específico)
python -m src.cli collect citation                   # Só Citation Tracker (todas as verticais)
python -m src.cli collect citation --vertical fintech  # Citation Tracker só fintech
python -m src.cli collect competitor                 # Só Multi-Vertical Benchmark
python -m src.cli collect serp                       # Só SERP Overlap

# Análise
python -m src.cli analyze report                     # Relatório estatístico (todas as verticais)
python -m src.cli analyze report --vertical saude    # Relatório só saúde

# Intervenções
python -m src.cli intervention add <slug> --type schema_org --desc "..." --url "..."

# Banco de dados
python -m src.cli db migrate           # Aplicar schema (inclui coluna vertical)
python -m src.cli db export --format csv
python -m src.cli db export --format csv --vertical fintech  # Exportar só fintech
python -m src.cli db health            # Verificar completude por vertical
```

## Documentação

- **[Manual do Sistema](docs/MANUAL.md)** — Referência completa com todos os módulos, schema, queries, custos e roadmap de 12 meses

## Licença

MIT
