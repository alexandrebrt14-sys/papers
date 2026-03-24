# Papers — Infraestrutura de Pesquisa Empírica em GEO

Plataforma de coleta, persistência e análise de dados para pesquisa acadêmica em **Generative Engine Optimization (GEO)**.

Desenvolvido pela [Brasil GEO](https://brasilgeo.ai) como infraestrutura de suporte para publicação de artigos científicos peer-reviewed sobre visibilidade em motores de busca generativos.

## Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Actions (Cron)                     │
│              daily-collect · weekly-benchmark                │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                     7 Módulos de Coleta                      │
│                                                              │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────────┐ │
│  │ 1. Citation   │ │ 2. Competitor│ │ 3. SERP vs AI        │ │
│  │    Tracker    │ │    Benchmark │ │    Overlap           │ │
│  │ (5 LLMs)     │ │ (controle)   │ │ (divergência)        │ │
│  └──────────────┘ └──────────────┘ └──────────────────────┘ │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────────┐ │
│  │ 4. Content   │ │ 6. Statistical│ │ 7. Citation          │ │
│  │  Intervention│ │    Analysis  │ │    Context           │ │
│  │  (A/B test)  │ │ (scipy)      │ │    Analyzer          │ │
│  └──────────────┘ └──────────────┘ └──────────────────────┘ │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│              5. Persistência de Série Temporal                │
│              Supabase + SQLite fallback                       │
│              Granularidade: diária / por-evento / semanal     │
└─────────────────────────────────────────────────────────────┘
```

## Módulos

| # | Módulo | Função | Status |
|---|--------|--------|--------|
| 1 | Multi-LLM Citation Tracker | Monitora citações em 5 LLMs (ChatGPT, Claude, Gemini, Perplexity, Copilot) | Em desenvolvimento |
| 2 | Competitor Benchmark Dataset | Grupo de controle com 5-10 entidades comparáveis | Em desenvolvimento |
| 3 | SERP vs AI Overlap Tracker | Divergência entre Google SERP e respostas de IA | Em desenvolvimento |
| 4 | Content Intervention Tracker | A/B testing de otimizações com medição before/after | Em desenvolvimento |
| 5 | Persistência de Série Temporal | Supabase + SQLite, dados longitudinais 6-12 meses | Em desenvolvimento |
| 6 | Statistical Analysis Module | Testes de significância, correlação, regressão, visualização | Em desenvolvimento |
| 7 | Citation Context Analyzer | Sentimento, atribuição, precisão factual, posição | Em desenvolvimento |

## Objetivo Científico

Gerar datasets longitudinais de 6-12 meses que permitam:
- Publicação em conferências tier-1 (KDD, SIGIR, WWW, WSDM)
- Submissão a journals peer-reviewed (IJDSML, IJRASET, Infonomy)
- Preprints no ArXiv com dados reprodutíveis

### Métricas-alvo por query

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `cited` | bool | LLM citou a entidade? |
| `position` | int | Posição na resposta (1=primeiro terço) |
| `context` | text | Resposta completa do LLM |
| `sentiment` | enum | positivo / neutro / negativo |
| `sources` | array | Fontes listadas pelo LLM |
| `attribution` | enum | nomeou / linkou / parafraseou |
| `factual_accuracy` | bool | Reproduziu corretamente? |
| `confidence_language` | text | Hedging ("segundo...", "possivelmente...") |
| `timestamp` | datetime | UTC |
| `model` | string | Modelo e versão exatos |

## Setup

```bash
pip install -e ".[dev]"
cp .env.example .env  # Preencher API keys
python -m src.cli db migrate
python -m src.cli collect --all
```

## Licença

MIT

---

**Brasil GEO** — [brasilgeo.ai](https://brasilgeo.ai) · [alexandrecaramaschi.com](https://alexandrecaramaschi.com)
