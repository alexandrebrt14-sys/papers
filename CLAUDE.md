# CLAUDE.md — Papers (refatorado 2026-04-19)

## REGRA #0 — IDIOMA
Todo conteúdo em PT-BR com acentuação completa. Exceção: código, commits, docstrings técnicas (inglês acadêmico).

## REGRA #1 — Contexto enriquecido GEO 2026 (mandatório)

Em **toda** decisão metodológica (escolha de dataset, framing de paper, definição de métrica estatística, escolha de conference de submissão, prompt portfolio de validação): ler primeiro [`docs/GEO_KNOWLEDGE_BASE_2026.md`](docs/GEO_KNOWLEDGE_BASE_2026.md) e [`docs/GEO_OPERATING_SYSTEM.md`](docs/GEO_OPERATING_SYSTEM.md).

- **KB (~21 KB)** consolida estado da arte 2025-2026 adaptado ao repo papers: papers fundadores GEO (Aggarwal SIGIR 2023 arXiv:2311.09735, Chen arXiv:2509.08919, Yao EMNLP 2025), datasets benchmark (GEO-bench, AI-citation-bench, MentionGen), metodologias estatísticas canônicas (n mínimo, IC, replicação inter-LLM), top conferences (SIGIR, ACL, EMNLP, KDD, WWW, ECIR), tooling open source (AthenaHQ public, Peec API). **§11 é a aplicação específica deste repo.**
- **OS (~24 KB)** é o playbook operacional alinhado a calendário de submissões: cadência diária (coleta + cache), semanal (review estatístico), mensal (preprint draft), trimestral (submission window). KPIs estatísticos (n por vertical, intervalo de confiança, pré-registro OSF). Prompt portfolio para validar replicabilidade do dataset.
- **Pesquisa bruta** em [`docs/research/geo-knowledge-2026/`](docs/research/geo-knowledge-2026/) (Perplexity sonar-pro com citações reais).

**Incremento Q2 2026 (17-05-2026)** — adiciona ao KB/OS sem substituir:
- [`docs/research/geo-q2-2026/GEO_KNOWLEDGE_2026_Q2_INCREMENT.md`](docs/research/geo-q2-2026/GEO_KNOWLEDGE_2026_Q2_INCREMENT.md) — doc canônico específico deste repo de pesquisa (sumário executivo, mudanças metodológicas Q1-Q2 2026, novos papers a integrar no pipeline arXiv, novos critérios de scoring, preregistration, 7 artefatos a produzir). Gerado por Claude Opus 4.7 sobre síntese Gemini 2.5 Pro de 5 Perplexity sonar-pro + 5 sonar-deep-research + 1 GPT-4o web_search.
- [`docs/research/geo-q2-2026/SYNTHESIS_STATE_OF_ART_2026.md`](docs/research/geo-q2-2026/SYNTHESIS_STATE_OF_ART_2026.md) — síntese geral (estado da arte, 8 seções, papers AgenticGEO/AdaptOrch/MoA/DAAO/CASTER, frameworks evaluation BiGGen-Bench/GEO-Bench/Arena-Hard, métricas GEO 2026).
- [`docs/research/geo-q2-2026/CITATIONS_POOL.md`](docs/research/geo-q2-2026/CITATIONS_POOL.md) — **325 URLs verificáveis** (arXiv IDs prioritários para ingestão).
- [`docs/research/geo-q2-2026/raw/`](docs/research/geo-q2-2026/raw/) — 10 JSONs originais das waves.

Citar `§X.Y` do KB/OS/INCREMENT ao tomar decisões. Atualizar trimestralmente (ciclo de submissão).

## REGRA #2 — Taxonomia canônica de 50 conceitos GEO/SEO 2026 (classificação obrigatória)

[`docs/GEO_50_CONCEITOS_CANONICAL.md`](docs/GEO_50_CONCEITOS_CANONICAL.md) é o **dicionário obrigatório de classificação** ao catalogar paper acadêmico, análise de fonte, ou produção de research neste repo. 14 eixos, 50 conceitos numerados, anti-padrões proibidos (pseudo-GEO, schema inflado, llms.txt como talismã).

**Mapeamento obrigatório:**

- **Ao resumir um paper** (entrada em `docs/research/` ou ingestão arXiv): tagueá-lo contra os Conceitos **11** (Answer capsules), **13** (Schema.org), **15** (Clareza de entidade), **21** (Referências externas), **22** (Autoria), **24** (Citabilidade GEO), **25** (Recuperabilidade generativa), **30** (llms.txt). Anotar quais o paper cobre, quais ignora, e quais ele desafia.
- **Em pesquisa nova com Perplexity sonar-deep-research**: usar os 50 conceitos como template de checklist da query — incorporar conceitos pertinentes ao tópico para evitar lacunas estruturais comuns em reviews ad hoc.
- **Em prompt portfolio de validação**: garantir que cobertura por vertical toca os 14 eixos (não só os de citação direta).
- **Em pré-registro OSF**: declarar quais conceitos a hipótese testa explicitamente.

Citar `Conceito N — Nome` ao referenciar (ex.: "Conceito 24 — Citabilidade GEO"). Documento revisado trimestralmente em sincronia com KB/OS.

## Propósito

Pesquisa empírica multi-vertical sobre como LLMs citam empresas brasileiras em respostas generativas. Framework de 4 verticais com coortes independentes monitoradas em 5 LLMs. Dataset longitudinal alvo: 6-12 meses para sustentar 3 papers peer-reviewed.

## Arquitetura (2026-04-19)

```
papers/
├── data/
│   ├── papers.db                  # SQLite — source of truth no git (protege pós-incidente 08/04)
│   ├── dashboard_data.json        # artefato para UIs externas
│   └── cache/                     # cache SHA-256 de respostas (não versionado)
├── src/
│   ├── config.py                  # 4 verticais, 5 LLMs, queries, pricing, entidades fictícias
│   ├── cli.py                     # Click CLI — --vertical, --module, --all
│   ├── collectors/                # Módulos de coleta (Onda 7: split aplicado)
│   │   ├── base.py                # Fachada enxuta + re-exports (85 linhas após split)
│   │   ├── llm_client.py          # LLMClient + LLMResponse (extraído Onda 7)
│   │   ├── response_cache.py      # ResponseCache SHA-256 TTL (extraído Onda 7)
│   │   ├── brave_search.py        # BraveSearchClient (extraído Onda 7)
│   │   ├── citation_tracker.py    # Módulo 1: principal, gera linha em citations
│   │   ├── competitor.py          # Módulo 2: benchmark entre verticais
│   │   ├── serp_overlap.py        # Módulo 3: SERP vs IA (Onda 9: toggle ENABLE_SERP_OVERLAP)
│   │   ├── intervention.py        # Módulo 4: A/B testing (estrutura pronta)
│   │   ├── context_analyzer.py    # Módulo 7: sentimento, atribuição, hedging
│   │   ├── drift_detector.py      # Detector de non-stationarity
│   │   └── prompt_sensitivity.py  # Variância por prompt
│   ├── db/
│   │   ├── schema.sql             # Schema SQLite + Supabase
│   │   ├── client.py              # DBClient (INSERTs, migrations)
│   │   └── migrate_*.py           # Migrations versionadas
│   ├── persistence/
│   │   └── timeseries.py          # Módulo 5: daily_snapshots
│   ├── analysis/
│   │   ├── statistical.py         # Módulo 6: 8 testes + effect sizes + corrections
│   │   └── visualization.py       # Charts publicação-ready
│   ├── finops/
│   │   ├── tracker.py             # record_usage → finops_usage
│   │   ├── monitor.py             # dashboards, rollups, alertas
│   │   ├── hooks.py               # integration post-coleta
│   │   └── secrets.py             # rotação de API keys (exploratório)
│   ├── api/
│   │   ├── main.py                # FastAPI endpoints por vertical
│   │   └── models.py              # Pydantic schemas
│   └── logging/
│       └── logger.py              # CollectionLogger (não integrado — TODO)
├── scripts/
│   ├── export_data.py             # CONSOLIDADO (Onda 4) — substitui 3 scripts duplicados
│   ├── generate_report.py         # Markdown diário
│   ├── sync_to_supabase.py        # Replica SQLite → Supabase
│   ├── health_check.py            # Valida coleta; exit 1 trava pipeline (anti-silent-fail)
│   ├── send-report.py             # Email via Resend
│   ├── update-docs.py             # Atualiza docs/STATUS.md
│   └── calibrate_score.py         # Fine-tune de detecção (exploratório)
├── tests/
├── .github/workflows/
│   ├── daily-collect.yml          # 06:00 e 18:00 BRT, job único sequencial
│   ├── weekly-benchmark.yml       # Domingo 05:00 BRT, análise agregada
│   ├── finops-monitor.yml         # Budget check
│   └── security-scan.yml          # Bandit + gitleaks
└── docs/
    ├── ARCHITECTURE.md            # Fluxograma completo (Onda 5)
    ├── METHODOLOGY.md             # Desenho estatístico (auditado)
    ├── REQUIREMENTS.md            # Especificação funcional
    ├── GOVERNANCE.md              # ADRs, roadmap
    ├── STATUS.md                  # Auto-gerado a cada coleta
    ├── MANUAL.md                  # Procedimentos operacionais
    └── audits/                    # Auditorias arquivadas por data
        └── 2026-03-26/            # Primeira auditoria (N=397, histórica)
```

## Verticais e Coortes

**Total: 69 entidades (61 reais + 8 fictícias), 4 verticais, 5 LLMs.**

### Fintech (21 entidades)
Nubank, PagBank, Cielo, Stone, Banco Inter, Mercado Pago, Itaú, Bradesco, C6 Bank, PicPay, Neon, Safra, BTG Pactual, XP Investimentos
— Internacional: Revolut, Monzo, N26, Chime, Wise
— Fictícias: **Banco Floresta Digital**, **FinPay Solutions**

### Varejo (16 entidades)
Magazine Luiza, Casas Bahia, Americanas, Amazon Brasil, Mercado Livre, Shopee Brasil, Renner, Riachuelo, C&A Brasil, Leroy Merlin, Centauro, Netshoes, Via Varejo, Grupo Pão de Açúcar
— Fictícias: **MegaStore Brasil**, **ShopNova Digital**

### Saúde (16 entidades)
Dasa, Hapvida, Unimed, Fleury, Rede D'Or, Einstein, Sírio-Libanês, Raia Drogasil, Eurofarma, Aché, EMS, Hypera Pharma, NotreDame Intermédica, SulAmérica Saúde
— Fictícias: **HealthTech Brasil**, **Clínica Horizonte Digital**

### Tecnologia (16 entidades)
Totvs, Stefanini, Tivit, CI&T, Locaweb, Linx, Movile, iFood, Vtex, RD Station, Conta Azul, Involves, Accenture Brasil, IBM Brasil
— Fictícias: **TechNova Solutions**, **DataBridge Brasil**

As **entidades fictícias** calibram o false-positive rate: se um LLM "cita" Banco Floresta Digital (que não existe), sabemos o quanto ele alucina nomes plausíveis. Crítico para a metodologia do Paper 1.

## LLM cohort (5 providers, todos obrigatórios)

| LLM | Provider | Modelo | Pricing in/out (USD/MTok) |
|-----|----------|--------|----------------------------|
| ChatGPT | OpenAI | `gpt-4o-mini-2024-07-18` | 0.15 / 0.60 |
| Claude | Anthropic | `claude-haiku-4-5-20251001` | 0.80 / 4.00 |
| Gemini | Google | `gemini-2.5-pro` | 1.25 / 5.00 |
| Perplexity | Perplexity | `sonar` | 1.00 / 1.00 + search |
| Groq | Groq | `llama-3.3-70b-versatile` | 0.59 / 0.79 |

Env var `MANDATORY_LLMS` (defaults a todos os 5) — falha de provider obrigatório dispara fail-loud.

## Pipeline (simplificado)

```
cron (06:00/18:00 BRT)
  → daily-collect.yml
    → for V in [fintech, varejo, saude, tecnologia]:
        citation_tracker   ← 5 LLMs × N queries
        competitor         ← benchmark
        context_analyzer   ← post-processing
        timeseries         ← daily_snapshots
    → sync_to_supabase
    → export_data --format json
    → send-report
    → health_check (exit 1 se validação falhar)
    → git commit data/papers.db + push
```

## Comandos

```bash
# Coleta
python -m src.cli collect --all                              # Tudo
python -m src.cli collect --module citation --vertical fintech

# Análise
python -m src.cli analyze --report
python -m src.cli analyze --visualize

# DB
python -m src.cli db migrate
python -m src.cli db health

# Export (Onda 4 — consolidado)
python scripts/export_data.py --format json
python scripts/export_data.py --format csv --vertical fintech
python scripts/export_data.py --format html
```

## Env vars obrigatórias

Ver `.env.example`. Resumo:
- 5 chaves LLM (OPENAI, ANTHROPIC, GOOGLE_AI, PERPLEXITY, GROQ)
- 2 chaves SERP (BRAVE, SERPAPI — opcional fallback)
- 2 chaves persistência (SUPABASE_URL, SUPABASE_KEY)
- 1 chave notificação (RESEND_API_KEY)

## Convenções de código

- Type hints em todas as funções públicas
- Docstrings em inglês (padrão acadêmico)
- Nomes de variáveis em inglês
- Logs e output CLI em PT-BR com acentuação
- Testes com pytest (parametrizados por vertical quando aplicável)
- Coluna `vertical` obrigatória em todas as tabelas de citação
- Schema migrations em `src/db/migrate_NNNN_*.py` versionadas
- Sem emojis em qualquer conteúdo

## Regras anti-retrabalho

- `papers.db` é **source of truth no git**. Artifact é safety-net apenas.
- Pipeline é **fail-loud**: qualquer vertical falha → exit 1 (protege desbalanceamento de N).
- Entidades fictícias são **parte da metodologia**. Nunca desativar em produção sem publicar os resultados já coletados.
- Auditorias antigas vão para `docs/audits/<data>/` — nunca deletar, nunca usar como source of truth atual.
- `AUDIT_*.txt` na raiz = red flag: deve ser movido para `docs/audits/<data>/` no próximo refactor.
