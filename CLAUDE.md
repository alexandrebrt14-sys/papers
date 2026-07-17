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

**Wave Maio 2026 Pós-IO (24-05-2026)** — adiciona aos anteriores sem substituir:
- [`docs/research/geo-wave-maio-posio-2026/WAVE_MAIO_2026_POSIO_CANONICAL.md`](docs/research/geo-wave-maio-posio-2026/WAVE_MAIO_2026_POSIO_CANONICAL.md) — **doc canônico de 511 linhas** cobrindo delta 17-mai → 24-mai-2026 com foco metodológico-acadêmico: (a) 6 novos arXiv IDs prioritários para ingestão (2604.25707 Citation Selection→Absorption framework dual-stage, 2603.09296 7-type failure taxonomy, 2604.03656 Semantic Entropy Drift, 2509.08919 v2, 2603.10913 LLM2Vec-Gen, 2508.21038 ICLR'26 limites teóricos embeddings); (b) **AutoGEO ICLR'26** (Wu/Zhong/Kim/Xiong CMU, +50,99% lift, github.com/cxcscmu/AutoGEO) — replicar em PT-BR como preprint ECIR 2027; (c) novos campos de schema SQLite (`citation_selection_rate`, `citation_absorption_rate`, `failure_type` enum, `semantic_entropy_drift`); (d) novo módulo `src/collectors/failure_classifier.py` (taxonomia 7 tipos); (e) glossário CAR vs CSR como métricas distintas com fonte primária; (f) **Profound 27M citation dataset** (owned-content só 4,3% global); (g) convergência cross-disciplina (GEO + RAG + citation patterns + vector retrieval) — pre-registro Q3/2026 deve declarar hipóteses cross-camada; (h) 3 camadas de KPI (Visibilidade → Infraestrutura → Negócio) — Camada 2 é a menos explorada cientificamente; (i) **24 URLs verificáveis** adicionais. Inclui apêndice §10 com achados complementares do orchestrator 5 LLMs (raw em [`raw/orchestrator_5llm_20260524_213700.json`](docs/research/geo-wave-maio-posio-2026/raw/orchestrator_5llm_20260524_213700.json)). **§6.2 é a aplicação específica deste repo** (5 entregáveis 60 dias, métrica de sucesso preprint AutoGEO-PT-BR no arXiv com IC 95% para lift até 23-jul-2026).

**Wave Junho 2026 (07-06-2026)** — adiciona aos anteriores sem substituir:
- [`docs/research/geo-wave-junho-2026/GEO_WAVE_JUNHO_2026_CANONICAL.md`](docs/research/geo-wave-junho-2026/GEO_WAVE_JUNHO_2026_CANONICAL.md) — **doc canônico (300 linhas)** cobrindo o delta 03-jun → 07-jun, gerado pelo orchestrator 5 LLMs (4 deep-research Perplexity + 1 board). Foco metodológico-acadêmico: (a) **framework de 5 camadas de medição de GEO** (captura de canal → logs/crawlers → SOV + interrogação estruturada → pipeline influenciado por IA → difference-in-differences) — esqueleto do prompt portfolio camada 3b; (b) **5 papers novos GEO/AEO** para ingestão: `2509.10762` (GEO-16/GEO score G, 70 prompts→1.702 citações→1.100 URLs), `2605.25517` (What Gets Cited, 252k experimentos RAG pareado, fatores-gatekeeper — **verificado via WebFetch**), `2605.12887` (EcoGEO, trajetória de evidências — **verificado**), GEO-Bench (ID a confirmar), GEO–GEU; (c) **~25 papers da camada semântica/vetorial** (chunking `2603.06976`/SemRAG, dense retrieval LREM, reranking, semantic entropy `2508.14496`, embeddings de entidade `2508.10003`/`2509.04011`) — base técnica de recuperabilidade; (d) detalhamento do dataset `geo-citation-lab` (602 prompts, 72 features) de `2604.25707` para desenho de CSR×CAR; (e) hierarquia de KPIs com metodologia formal (Microsoft Clarity Citation Rate, AIO×AI Mode 13,7% overlap). **§7.2 é a aplicação específica deste repo** (5 entregáveis: campos CSR/CAR + influência por página, prompt portfolio camada 3b por plataforma, ingestão dos 4 papers tagueados, fatores-gatekeeper como hipóteses PT-BR falsificáveis, GEO-16 como variável de controle). Raw em [`raw/`](docs/research/geo-wave-junho-2026/raw/).

**Wave Junho 15 2026 (15-06-2026)** — adiciona aos anteriores sem substituir:
- [`docs/research/geo-wave-junho-15-2026/GEO_WAVE_JUNHO_15_2026_CANONICAL.md`](docs/research/geo-wave-junho-15-2026/GEO_WAVE_JUNHO_15_2026_CANONICAL.md) — **doc canônico**, delta 07-jun → 15-jun, ancorado em pesquisa web verificada ao vivo (WebSearch/WebFetch jun/2026) + orchestrator 5 LLMs no fundamento técnico atemporal (§5). Foco metodológico-acadêmico: (a) **2 papers verificados via WebFetch para ingestão** — `2603.29979` (GEO-SFE, Yu/Yang/Ding/Sato 31-mar-2026; estrutura em macro/meso/micro; +17,3% citation rate, +18,5% qualidade em 6 motores) e `2603.09296` (AgentGEO, Tian et al. 10-mar-2026; diagnóstico-reparo de falha de citação; +40% citação modificando 5% do conteúdo vs 25% baseline — reconcilia a antiga referência "taxonomia de 7 tipos de falha"); (b) **novo KPI Share of Answer vs Share of Voice** (estar na lista de fontes ≠ ser a resposta) + bateria consolidada (Answer Inclusion Rate, Recommendation Rate, Prompt Coverage, Assisted Click Yield); (c) **benchmarks de impacto** — RCT de AIO (-38% cliques, UX inalterada, jan-fev/26) e Seer 2026 (citado em AIO = +120% cliques/impressão) como hipóteses de negócio falsificáveis; (d) os 3 níveis estruturais de GEO-SFE como **variáveis de controle** mensuráveis na coleta, correlacionadas com taxa de citação por vertical. **§7.2 é a aplicação específica deste repo** (ingestão de `2603.29979`/`2603.09296` tagueados contra Conceitos 11/13/15/24/25 e CSR/CAR; features macro/meso/micro no schema; campo Share of Answer/Recommendation Rate; hipóteses pré-registradas do lift AgentGEO e do RCT de AIO; nota no METHODOLOGY de que "deep research" sem busca live fabrica citações). Raw do orchestrator em [`raw/`](docs/research/geo-wave-junho-15-2026/raw/).

**Wave Junho 15B 2026 (15-06-2026, 2ª passada)** — adiciona aos anteriores; foco de ingestão acadêmica:
- [`docs/research/geo-wave-junho-15b-2026/GEO_WAVE_JUNHO_15B_2026_CANONICAL.md`](docs/research/geo-wave-junho-15b-2026/GEO_WAVE_JUNHO_15B_2026_CANONICAL.md) — **doc canônico**, pesquisa viva cruzada (Perplexity `sonar-pro` com `citations`/`search_results` reais — raws `P1..P7.json` — + WebSearch/WebFetch do Claude verificando `arxiv.org/abs/<id>` página a página). **Papers novos para ingestão prioritária (§1, todos verificados via abs):** `2606.12439` (Wen et al., ICML 2026 Position Track, 18-mai — formaliza GEO como otimização conjunta de **retrievability** × **ranking impact**, via *retrieval booster* e *ranking shifter messages*); `2605.25517` (What Gets Cited, 252k trials, 6 LLMs — relevância tópica + posição na lista + preço/timestamp explícitos = preditores; formatação cosmética rende pouco); `2605.29107` (GEO-Bench, cs.CR — reescrita black-box iguala/supera ataques gradient-based e evade detecção por perplexidade); RAG/chunking: `2603.06976` (Paragraph Group Chunking lidera, nDCG@5≈0,459; fixo-por-caractere é fraco), `2601.15457` (rerank → faithfulness 0,797 vs 0,621), `2605.01664` (híbrido+rerank Cohere, 100% grounding), `2604.04936` (W-RAC, custo de chunking −1 ordem de magnitude). Marcar `2602.02961` (Pinterest GEO/VLM) como caso de produto, não benchmark. **Anti-GhostCite reforçado:** o `sonar-deep-research` chegou a **inventar IDs** (`2603.04567`/`2605.11203` — NÃO verificados); regra: nunca canonizar ID sem abrir o `abs` via WebFetch. **§7.2 = aplicação deste repo** (ingestão dos IDs por eixo: frameworks de execução / medição / recuperação-chunking / riscos-manipulação; cada paper entra com link abs + status de verificação). **CORREÇÕES (§8):** GEO-16 `2509.10762` e "How to Dominate" `2509.08919` são de **set/2025** (não 2026); "Share of Answer" não é KPI normalizado; Profound Index existe (5-nov-2025) e os 400M são do Conversation Explorer. Raws + proveniência em [`raw/`](docs/research/geo-wave-junho-15b-2026/raw/).

**Wave Junho 19 2026 (19-06-2026)** — adiciona aos anteriores sem substituir (sincronizada dos repos irmãos em 14-07):
- [`docs/research/geo-wave-junho-19-2026/GEO_WAVE_JUNHO_19_2026_CANONICAL.md`](docs/research/geo-wave-junho-19-2026/GEO_WAVE_JUNHO_19_2026_CANONICAL.md) — **doc canônico delta** mai–19/jun: (a) **Google oficializa "GEO para Search é SEO"** — guia de AI optimization do Search Central (15-mai/15-jun) revela **RAG + query fan-out** e lista **5 táticas "não precisa fazer"** (llms.txt, markup-p/-IA, chunking, reescrita-p/-IA, overfoco em structured data); (b) **estudos causais Ahrefs** — schema não move citação em IA (1.885 páginas diff-in-diff: AIO −4,6%) e **97% dos llms.txt nunca recebem requisição** (137k domínios); (c) infra de medição — GA4 canal "AI Assistant", GSC AI reports (impressão, sem CTR); (d) papers `2605.12887` EcoGEO e `2605.21948` SCI-Defense; (e) série AWR/Fiorelli (4 pilares Retrieval/Reasoning/Agency/Authority + 4 camadas de execução). **§7 = desmistificações que revogam clichês** ("schema +67%", "llms.txt aumenta citação", "Reddit nº 1 fixo", "um prompt = um ranking"). Para este repo: os estudos causais são o padrão-ouro metodológico a replicar em PT-BR; medição exige múltiplas execuções e média de mention rate.

**Wave Julho 2026 (14-07-2026)** — adiciona aos anteriores sem substituir; **inclui uma revogação de correção da 15B**:
- [`docs/research/geo-wave-julho-2026/GEO_WAVE_JULHO_2026_CANONICAL.md`](docs/research/geo-wave-julho-2026/GEO_WAVE_JULHO_2026_CANONICAL.md) — **doc canônico delta** 19-jun → 14-jul, 6 rodadas em 4 provedores cloud (Perplexity ×2, OpenAI, Anthropic, xAI) + doublecheck Claude em fonte primária. Núcleo: (a) **§7.1 REVOGA a correção §8.5 da 15B** — a Adobe **concluiu** a compra da Semrush (anúncio 19-nov-2025, US$ 1,9 bi; fechamento final de abr/2026; press release + 8-K verificados); (b) **Semrush AI Visibility Index 2026 expandido** (26-jun; 126 mi prompts EUA jan–abr; ChatGPT ~15 fontes/resposta vs Gemini ~3; só 36 marcas no top-100 das 4 plataformas); **81% vs 36%** (integração SEO+GEO vs separado); (c) **Ahrefs Brand Radar abre metodologia** (PAA + fan-out semântico, 5 engines, limitações declaradas — baseline de transparência para os 3 papers-alvo) + correlatos em 75k marcas (menções↔AIO r=0,664; YouTube = correlato nº 1 cross-engine); (d) **Profound 6,8 mi citações**: padrões por engine (Gemini 52,15% owned; ChatGPT 48,73% terceiros; Perplexity reviews); (e) **concentração de referral** (Previsible/SEL jul-26: ChatGPT 92,4%; Claude cresceu 64x e ultrapassou Perplexity em mar-26); conversão por vertical (faixa 1,3x–23x — §7.3 proíbe "4–5x" como constante); (f) **§5 funil vetorial mensurável** (`similarity → hit rate@k → rerank survival → citation share`, 7 métricas operacionais) — operacionaliza a Camada 2 (Infraestrutura), a menos explorada cientificamente; (g) §4 framework de execução consolidado (workflow 7 etapas, 10 papéis, cadência, 5 gates, report de 8 perguntas). **§8.1 = aplicação deste repo** (hipóteses H-a/H-b/H-c pré-registráveis; campo `citation_style` por engine no schema; ponderação do painel por share de referral). §7.2 refuta 2 alucinações do Grok (rodada xAI = sinal qualitativo apenas). Raws em [`raw/`](docs/research/geo-wave-julho-2026/raw/).

Citar `§X.Y` do KB/OS/INCREMENT/WAVE ao tomar decisões. **Em conflito de fato datado, prevalece a wave mais recente nos itens explicitamente marcados como correção (Julho §7 > Junho-19 §7 > 15B §8); fora desses itens, o corpus anterior permanece válido.** Atualizar trimestralmente (ciclo de submissão).

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

**Total: 127 entidades (79 reais BR + 32 âncoras internacionais + 16 fictícias), 4 verticais, 5 LLMs.** Fonte canônica: `src/config_v2.py`. As listas detalhadas abaixo são do cohort v1 (legado) e estão sendo migradas — ver README §Verticals para o roster v2 atual.

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


## Plugin Resend Claude Code (instalado 2026-05-28)

`resend@claude-plugins-official` v1.0.0 ativo (escopo user + project). Expõe 5 skills carregadas automaticamente quando o trabalho toca email, templates, deliverability ou inbound:

- `resend:resend` — SDK + gotchas (idempotência, webhook signing, template vars)
- `resend:react-email` — templates HTML via React Email
- `resend:email-best-practices` — SPF/DKIM/DMARC, CAN-SPAM/GDPR/CASL, retry, bounces, complaints
- `resend:agent-email-inbox` — patterns seguros para processar email inbound (sender allowlist, sandbox, content filtering)
- `resend:resend-cli` — flags non-interativas para shell/CI/CD (`--react-email` envia .tsx direto)

MCP server `resend-mcp` lê `RESEND_API_KEY` do env (configurado em `~/.claude/.env`). Para fixes em código que envia email, deixar essas skills acionarem por palavra-chave em vez de reimplementar lógica de retry/auth/headers.

Helper Python canônico para precheck sandbox: `C:/Sandyboxclaude/scripts/python/resend_precheck.py` (porta `landing-page-geo/src/lib/resend-precheck.ts`).

## Padrão editorial — escrita humanizada (17/07/2026)

Todo conteúdo de leitura humana produzido neste repo (artigo, curso, página, post,
e-mail, relatório, parecer, resposta ao usuário) segue o padrão editorial global do
Alexandre. Qualidade vence velocidade; profundidade proporcional ao problema;
escrever como especialista sênior conversando com outro profissional experiente.
Fonte de verdade completa: `docs/ESTILO_EDITORIAL.md` do repo GEO-Pesquisador
(clone local em `C:/Sandyboxclaude/GEO-Pesquisador`).

Proibidos como padrão recorrente (uso pontual e consciente é tolerado):

- Antítese em série: "não se trata de X, trata-se de Y", "não é apenas X, é Y",
  "não basta X, é preciso Y", "mais do que X, Y". Afirmar direto o que a evidência
  sustenta.
- Conectivos batidos repetidos: "além disso", "por outro lado", "nesse contexto",
  "vale destacar", "é importante ressaltar", "nesse sentido", "por fim".
- Parágrafos vizinhos abrindo com a mesma construção sintática; blocos com ritmo
  idêntico; excesso de paralelismo; perguntas retóricas em série; conclusões
  idênticas fechando tópicos sucessivos.
- Travessão e hífen como recurso estilístico no conteúdo final: preferir vírgula,
  dois-pontos ou ponto.
- Clichês, frases genéricas que serviriam para qualquer assunto, tom promocional,
  superlativo sem número ao lado, adjetivo decorativo, negrito por hábito.

Obrigatório: linha de raciocínio lógica; cada parágrafo acrescenta uma ideia nova;
alternar períodos curtos, médios e longos; recomendação sempre acompanhada do
porquê; conceito técnico coberto com contexto, motivação, funcionamento,
limitações e critérios de decisão quando relevantes; material educacional abre
pelo problema e fecha com síntese prática. Antes de entregar, reler procurando
esses padrões e reescrever o que soar texto de máquina. Sub-agentes que geram
copy recebem o bloco de `C:/Sandyboxclaude/scripts/prompts/COPY_PROMPT_PREFIX.md`
carimbado no prompt.
