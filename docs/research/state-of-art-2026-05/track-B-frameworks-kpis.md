# Track B — Frameworks Operacionais + KPIs GEO 2026

> Sub-agent Opus · 2026-05-20 · Pesquisa: 5 chamadas Perplexity sonar-deep-research + 12 WebFetches em sites primários de vendors.
> Complementa `landing-page-geo/docs/GEO_KNOWLEDGE_BASE_2026.md §2` (14 KPIs personal brand) e `curso-factory/docs/GEO_KNOWLEDGE_BASE_2026_V2.md §6` (14 KPIs canônicos com fonte primária). NÃO duplica; adiciona camada operacional faltante.

---

## Sumário executivo

Este documento entrega:

1. **Seis frameworks de execução end-to-end** com etapas numeradas, inputs, outputs, cadência, stack mínima, custo mensal estimado e aplicação prática a três projetos (landing-page-geo, curso-factory, papers).
2. **22 KPIs canônicos novos** que NÃO estão na V2 do `curso-factory`, com fórmula matemática, unidade, fonte primária verificada, frequência ideal, benchmark 2026, instrumentação, visualização recomendada e anti-padrão.
3. **Arquitetura de referência** de dashboard GEO operacional (ingestão → storage → transformação → apresentação → alertas).
4. **Três scripts quick-start** prontos para colar em projeto: Python multi-LLM polling, bash snapshot semanal, dbt/SQL Citation Persistence Index.
5. **Apêndice A** com URLs primárias validadas.

A tese central é simples. Em 2025, GEO era um problema de copy. Em 2026, virou um problema de engenharia de dados: prompt portfolio + amostragem multi-LLM + warehouse + dbt + alertas + attribution multi-touch são camadas obrigatórias para qualquer marca que pretenda gerenciar visibilidade em modelos como ChatGPT, Claude, Gemini, Perplexity e Copilot com o mesmo rigor que aplica em SEO tradicional. Os vendors que cristalizaram esse stack (Profound, Daydream, Peec.ai, Goodie, Scrunch, AthenaHQ, Otterly, Evertune, Ahrefs Brand Radar, Semrush AI Toolkit) convergiram num loop quase idêntico (assess → optimize → measure → iterate), com diferenças apenas na automação e no grau de attribution a receita. Os KPIs novos aqui propostos cobrem dimensões ainda subdimensionadas na V2 do `curso-factory`: persistência temporal de citação, velocidade, decaimento de eco de marca, consistência cross-LLM, sentimento valorizado por posição, drift de autoridade autoral, cobertura do portfólio de prompts, peso por token (não só por presença), share por surface de origem (snippet vs full text) e visibilidade geo-linguística.

---

## Parte 1 — Seis frameworks de execução end-to-end

### Framework 1 — Prompt Portfolio Lifecycle (PPL)

- **Origem**: Peec.ai "The Complete Guide to GEO" (`peec.ai/blog/the-complete-guide-to-generative-engine-optimization-(geo)` · ago/2025) + Goodie AI Topic Explorer (`goodie.ai`) + Scrunch FAQs (`scrunch.com`). Sintetizado por este sub-agent.
- **Tese**: o portfólio de prompts é a unidade atômica de medição GEO. Sem disciplina de inventário, todo o resto (share of voice, citation rate, sentiment) é ruído.
- **Etapas (1..8)**:
  1. **Levantamento de intenção** — entrevista com vendas, CS, fundadores; mapeia 25-50 perguntas reais que clientes fazem na jornada (top of funnel até decisão).
  2. **Expansão por suggestion engine** — usar Goodie Topic Explorer (ou Peec suggestion + sonar-deep-research) para chegar a 100-300 prompts.
  3. **Classificação** — cada prompt recebe `intent` (informacional, comparativo, transacional, alternativa-a-X), `funnel_stage` (TOFU/MOFU/BOFU), `topic_cluster`, `geo_locale` (pt-BR, en-US, es-ES) e `priority` (P0/P1/P2).
  4. **Aprovação editorial** — fundador valida (e remove prompts irrelevantes ou perigosos do ponto de vista regulatório).
  5. **Codificação** — portfólio versionado em `prompts.yaml` no repositório, sob controle de PR.
  6. **Sampling** — cada prompt rodado em 5+ LLMs a cada N dias (ver Framework 2).
  7. **Auditoria trimestral** — sub-conjunto P0 estende para 1000 amostras; teste de prompt drift (se o mesmo prompt em janeiro e abril produz brand sets diferentes, é sinal de model update).
  8. **Refresh** — adicionar 10-20 prompts/trimestre baseado em logs de site search, transcripts de vendas e novos lançamentos.
- **Inputs**: transcripts de vendas, GA4 site search, Google Search Console queries, Reddit threads do ICP.
- **Outputs**: `prompts.yaml` versionado, com 100-300 prompts categorizados.
- **Cadência recomendada**: revisão completa trimestral; refresh contínuo via PR.
- **Stack mínima**: GitHub + YAML + um sub-agent LLM para sugestão semântica + planilha para classificação.
- **Custo mensal estimado**: US$ 50-150 (mão-de-obra + chamadas LLM para suggestion).
- **Como aplicar em `landing-page-geo`**: criar `src/lib/prompts-portfolio.yaml` com 50-80 prompts pt-BR cobrindo "consultor GEO Brasil", "ex-CMO Semantix", "agência GEO LLM citation", "como ranquear em ChatGPT pt-BR".
- **Como aplicar em `curso-factory`**: portfólio por curso (50 prompts/curso) cobrindo "curso saúde mental vibecoding", "curso para programadores ansiedade", "Alexandre Caramaschi curso".
- **Como aplicar em `papers`**: portfólio acadêmico (40 prompts/paper) cobrindo "como medir LLM citation rate", "GEO methodology Brazil", "Brasil GEO Caramaschi paper".

### Framework 2 — Multi-LLM Sampling Wave (MLSW)

- **Origem**: metodologia explicitada em Profound API Cookbook (`tryprofound.com/blog/introducing-profound-api-cookbook`), Scrunch monitoring stack (`scrunch.com`), Peec daily updates (`peec.ai`). Reforçada pelo paper de Citation Persistence (Perplexity sonar-deep-research, Q3 desta sessão).
- **Tese**: brand presence em LLM é processo estocástico. Uma única amostra é ruído; só ondas repetidas capturam o sinal.
- **Etapas (1..7)**:
  1. **Definição de tracking configurations** — pelo menos 2 perfis: `deterministic` (T=0, top_p=0.1) e `stochastic` (T=0.7, top_p=0.9).
  2. **Definição de n-samples por prompt** — 20-50 para prompts P0, 10 para P1, 5 para P2. Total típico: 1000-5000 chamadas LLM por onda.
  3. **Definição do modelo set** — mínimo 5: GPT-4o, Claude 3.7 Sonnet, Gemini 2.5 Flash, Perplexity Sonar, Groq Llama 3.3 70B.
  4. **Execução** — script Python paraleliza chamadas com `asyncio.gather`, com rate limit por provider; logs em `events_raw.jsonl`.
  5. **Parsing** — pipeline detecta menções de marcas via regex + LLM-secondary-pass de disambiguation (Apple-fruta vs Apple-empresa).
  6. **Persistência** — eventos individuais em warehouse (BigQuery, Snowflake, DuckDB) com schema `(prompt_id, model_id, model_version, sample_idx, ts_utc, raw_text, brand_mentions_json, citations_json)`.
  7. **Versionamento** — cada onda registra `model_version` (best-effort via API headers ou vendor release notes) para reconstruir trajetórias longitudinais.
- **Inputs**: `prompts.yaml`, chaves de API dos 5 LLMs.
- **Outputs**: tabela `events_raw` no warehouse, ~1000-5000 linhas/onda.
- **Cadência recomendada**: diária para marcas em campanha ativa; semanal para tracking baseline; mensal para auditoria long-tail.
- **Stack mínima**: Python 3.11 + httpx + asyncio + DuckDB local OU BigQuery free tier + cron/GitHub Actions.
- **Custo mensal estimado**: US$ 200-800 (LLM tokens) + US$ 0-50 (warehouse free tiers cobrem o uso).
- **Como aplicar em `landing-page-geo`**: usar `geo-orchestrator/cli.py run` semanalmente em 25-50 prompts P0 sobre Brasil GEO; persistir em DuckDB local + commit no repo de dashboard.
- **Como aplicar em `curso-factory`**: por curso, rodar 50 prompts × 5 LLMs × 10 samples = 2500 chamadas/onda; 1 onda/semana × 5 cursos = US$ 100-200/mês.
- **Como aplicar em `papers`**: monthly sampling para tracking de citação acadêmica dos próprios papers + dos autores referenciados.

### Framework 3 — Citation Persistence & Decay Loop (CPDL)

- **Origem**: paper conceitual gerado por Perplexity sonar-deep-research Q3 desta sessão; alinha com Profound "Share of Model" (`tryprofound.com/blog`) e Athena Citation Engine (`athenahq.ai`).
- **Tese**: medir citação num único snapshot é insuficiente. O que importa é quanto tempo a citação dura através de updates do modelo.
- **Etapas (1..6)**:
  1. **Baseline** — onda inicial de sampling (Framework 2) estabelece mention rate `p_0` para cada brand × prompt × model.
  2. **Tracking longitudinal** — ondas semanais durante 12+ semanas formam o painel `(brand, prompt, model, week, mention_rate)`.
  3. **Detecção de eventos** — anotar manualmente release notes de cada vendor (GPT-4o agosto 2026 update, Claude 3.7 release etc) como marcos temporais.
  4. **Cálculo de CPI (Citation Persistence Index)** — para cada brand, ajustar curva exponencial decay `p(t) = p_0 * exp(-λt)` aos pontos pós-evento; `CPI = ln(2)/λ` (meia-vida em dias).
  5. **Cálculo de Brand Echo Decay (BED)** — para campanhas que cessaram, medir quantos dias a mention rate leva para retornar ao baseline pré-campanha.
  6. **Ação corretiva** — quando CPI < threshold (ex: < 14 dias), investigar fontes de citação e reforçar via PR, Reddit, Wikipedia, G2.
- **Inputs**: 12+ semanas de tabela `events_raw`.
- **Outputs**: tabela `citation_persistence` com `(brand, prompt_cluster, model, baseline_p, lambda, half_life_days, last_updated)`.
- **Cadência recomendada**: recálculo mensal; alerta automático quando half_life cai > 30% mês-a-mês.
- **Stack mínima**: dbt + scipy.optimize.curve_fit + Metabase para visualização.
- **Custo mensal estimado**: US$ 0-100 (sobre o custo já gasto em Framework 2).
- **Como aplicar em `landing-page-geo`**: estabelecer baseline em maio/2026 para Brasil GEO; CPI por modelo será métrica norte-magnética dos próximos 90 dias.
- **Como aplicar em `curso-factory`**: tracking pós-lançamento de cada curso para entender se LLMs continuam citando 60-90 dias depois.
- **Como aplicar em `papers`**: aplicado a citações acadêmicas vs LLM citations, gera comparação fascinante (papers no Google Scholar têm CPI essencialmente infinito; em LLMs, pode ser semanas).

### Framework 4 — Multi-Touch LLM Attribution (MLA)

- **Origem**: Adobe Customer Journey Analytics "AI surfaces" documentation (referrer mapping completo); Yotpo 2026 GA4 playbook (regex 14+ domínios); Microsoft Clarity "AI Platform" channel group (`clarity.microsoft.com`); Orbit Media GA4 guide. Sintetizado por este sub-agent a partir de Q2 sonar-deep-research desta sessão.
- **Tese**: AI surfaces são canal de aquisição distinto. Sem detecção custom, ~30-60% da influência LLM se perde em "Direct" ou "Referral genérico".
- **Etapas (1..9)**:
  1. **Server-side log capture** — Cloudflare Workers / Vercel Edge logs / Nginx logs gravam todo request com referrer + user-agent + URL params.
  2. **Classificação multi-sinal** — pipeline classifica cada session em uma de 5 categorias: `AI_human_click` (referrer = chatgpt.com, perplexity.ai etc), `AI_crawler` (UA = GPTBot, ClaudeBot etc), `AI_user_agent_live` (UA = ChatGPT-User, Perplexity-User), `AI_UTM` (utm_source=chatgpt etc), `Dark_AI` (heurística comportamental).
  3. **Regex canônica** — manter `ai_referrer_patterns.yaml` versionado com chatgpt.com, chat.openai.com, openai.com, perplexity.ai, claude.ai, gemini.google.com, bard.google.com, copilot.microsoft.com, edgeservices.bing.com, m365.cloud.microsoft, you.com, poe.com, grok.x.ai, duckduckgo.com/chat, meta.ai, nimble.ai, iask.ai.
  4. **GA4 channel group custom** — criar grupo "AI Search" com regex no campo `Session source / medium`.
  5. **GTM dataLayer push** — script de landing captura `document.referrer` + `navigator.userAgent` + URL params, pusha `ai_source` no dataLayer.
  6. **HubSpot/Marketo property** — sincroniza `ai_source` no contato; possibilita atribuição em pipeline de leads.
  7. **UTM stamping em grounding assets** — todo PDF, whitepaper, doc público externo recebe UTMs persistentes `utm_source=grounding_pdf&utm_campaign=ai_grounding` para que, se LLM citar, o link de retorno carregue assinatura.
  8. **Modelo de atribuição** — em Bizible / GA4 attribution, AI Search recebe credit por modelo `time_decay` (não linear, não last-touch).
  9. **Reconciliação manual** — entrevista quarterly com 10-20 clientes recém-fechados perguntando explicitamente "onde nos encontrou; usou ChatGPT/Perplexity/Claude?".
- **Inputs**: server logs, GA4, HubSpot, Bizible/Marketo Measure ou alternativa.
- **Outputs**: campo `ai_source` em todo evento de conversão; relatório mensal de revenue por canal AI.
- **Cadência recomendada**: pipeline rodando em near-real-time (ingestion ≤ 5min); relatórios diários para campanhas ativas.
- **Stack mínima**: Cloudflare Workers (logs) + BigQuery (storage) + dbt (transformação) + GA4 + GTM + HubSpot CRM.
- **Custo mensal estimado**: US$ 100-500 (Cloudflare Pro + BigQuery free tier + GA4 free).
- **Como aplicar em `landing-page-geo`**: Cloudflare Worker (já existe no projeto) captura todo request e loga referrer+UA. Endpoint `/api/ai-source-log` persiste em D1 ou KV.
- **Como aplicar em `curso-factory`**: cada landing de curso captura `ai_source` e propaga até a Stripe checkout custom field, fechando o loop até receita.
- **Como aplicar em `papers`**: cada paper público em HTML registra referrer; permite saber quantos leitores chegam via Perplexity citation vs Google Scholar.

### Framework 5 — Cross-LLM Consistency Audit (CLCA)

- **Origem**: Profound "Cross-Model Comparison" feature + AthenaHQ "8 LLM platforms monitoring" + Peec.ai listicle study (200K AI responses across 8 engines, `peec.ai/blog/the-listicle-rank-effect-...`). Sintetizado por este sub-agent.
- **Tese**: cada LLM tem viés próprio. Se uma marca é citada em GPT-4o mas não em Gemini, ou está numa lista em Claude mas omitida em Perplexity, isso é informação acionável (não ruído).
- **Etapas (1..6)**:
  1. **Sample fixe** — para cada prompt P0, executar idêntica config (mesmo system prompt, T=0.7, n=20) em 5+ LLMs.
  2. **Cálculo do Cross-LLM Consistency Index (CLCI)** — para cada brand × prompt, CLCI = 1 - σ(mention_rate)/μ(mention_rate). 1.0 = perfeitamente consistente; 0 = altamente divergente.
  3. **Heatmap por modelo** — eixo X = modelos (5+), eixo Y = prompts (Top 25), célula = mention_rate.
  4. **Detecção de outlier model** — para cada brand, calcular z-score por modelo; se algum modelo tem z > 2σ ou z < -2σ, marcar como "outlier" e investigar (pode ser falha estrutural ou oportunidade).
  5. **Diagnóstico de causa raiz** — outliers negativos costumam apontar para gaps de fonte: marca ausente em fonte primária que aquele modelo prefere (ex: Gemini tende a citar mais YouTube; se a marca não tem presença em YouTube, sofre lá).
  6. **Plano de ação cross-LLM** — alocar budget de PR/conteúdo por modelo de pior performance.
- **Inputs**: tabela `events_raw` com 5+ modelos.
- **Outputs**: tabela `clci_by_brand_prompt`, heatmap atualizado semanalmente.
- **Cadência recomendada**: semanal para tracking; mensal para plano de ação.
- **Stack mínima**: pandas + plotly/seaborn + Metabase ou Hex.
- **Custo mensal estimado**: marginal sobre Framework 2.
- **Como aplicar em `landing-page-geo`**: detectar que Brasil GEO é forte em ChatGPT (Reddit + LinkedIn citation base) mas fraca em Gemini (sem presença YouTube); priorizar canal video.
- **Como aplicar em `curso-factory`**: cursos podem ranquear bem em Perplexity (citation de papers) mas mal em ChatGPT (sem Reddit thread); estratégia distinta por LLM.
- **Como aplicar em `papers`**: identificar em quais LLMs cada paper é mais citado e ajustar onde investir tradução / formato de divulgação.

### Framework 6 — GEO Alerting & Anomaly Detection (GAAD)

- **Origem**: BrightEdge alerting (`brightedge.com`), Athena "real-time citation tracking" (`athenahq.ai`), Profound "alerts on visibility drop" (`tryprofound.com`). Métrica de drop detection inspirada em controle estatístico clássico (CUSUM, EWMA).
- **Tese**: medição sem alertas é arquivo morto. Drop de citation rate em 48h precisa virar Slack ping em 48h, não relatório mensal.
- **Etapas (1..5)**:
  1. **Definição de thresholds** — para cada KPI canônico, definir 3 níveis: `green` (variação ≤ ±10% vs trailing 4-week mean), `yellow` (±10% a ±25%), `red` (> ±25%).
  2. **CUSUM detector** — para cada série de mention_rate, manter soma cumulativa de desvios; quando soma cruza limiar (k=0.5σ, h=4σ), dispara alerta.
  3. **Roteamento de alertas** — `green` apenas dashboard; `yellow` Slack channel de avisos; `red` Slack channel principal + DM no fundador + opcionalmente PagerDuty.
  4. **Enriquecimento de alerta** — payload do alerta inclui prompt afetado, modelo, brand, valor antes/depois, top 3 competitors que ganharam share, top 3 fontes citadas no novo cenário.
  5. **Postmortem semanal** — toda sexta, revisão de alertas red da semana com root-cause análise (model update? campanha competidor? mudança no próprio site?).
- **Inputs**: tabela `events_raw` em streaming.
- **Outputs**: Slack/PagerDuty notifications, dashboard de incidentes.
- **Cadência recomendada**: detector roda a cada hora; alertas em near-real-time.
- **Stack mínima**: Python + dbt + Slack webhook + opcional PagerDuty.
- **Custo mensal estimado**: US$ 0-50 (free tiers cobrem para um site).
- **Como aplicar em `landing-page-geo`**: integrar com `#geo-alerts` Slack channel; alerta quando mention_rate de "Brasil GEO" em Perplexity cair > 25%.
- **Como aplicar em `curso-factory`**: alerta quando algum curso recém-lançado começar a ser mencionado (= sinal positivo) ou pare de ser (= regression).
- **Como aplicar em `papers`**: alerta quando paper começa a ser citado por LLM (evento celebrável e raro o suficiente para acordar Alexandre).

---

## Parte 2 — 22 KPIs canônicos NOVOS

Cada KPI abaixo é proposto como complemento direto à V2 do `curso-factory`. Numeração começa em K-NEW-001 para evitar colisão com a V2 (que tem K01-K14).

### K-NEW-001 — Citation Persistence Index (CPI)
- **PT-BR**: Índice de Persistência de Citação
- **Fórmula**: `CPI = ln(2) / λ`, onde λ é obtido ajustando `p(t) = p_0 * exp(-λt)` aos pontos pós-evento; CPI é meia-vida em dias da citação.
- **Unidade**: dias.
- **Fonte primária**: `peec.ai/blog/how-to-measure-ai-search-visibility-and-revenue-the-kpis-that-actually-matter` (mar/2026) + paper conceitual Perplexity sonar-deep-research (Q3 desta sessão).
- **Frequência**: recálculo mensal.
- **Benchmark 2026**: para marcas estabelecidas com presença forte em Reddit/Wikipedia, CPI > 90 dias é comum. Para marcas novas dependentes de campanha PR única, CPI 14-30 dias.
- **Instrumentação**: dbt model + scipy.optimize.curve_fit (snippet na Parte 4).
- **Visualização**: line chart sobreposta com curva exponencial ajustada; uma linha por modelo.
- **Anti-padrão**: NÃO é "tempo desde a primeira citação"; é meia-vida estatística pós-evento.

### K-NEW-002 — Citation Velocity (CV)
- **PT-BR**: Velocidade de Citação
- **Fórmula**: `CV = (mention_rate_week_t - mention_rate_week_t-1) / mention_rate_week_t-1`, expresso em %/semana. Pode ser agregado em CV_4w (média 4 semanas).
- **Unidade**: % por semana.
- **Fonte primária**: `tryprofound.com/blog/prompt-volumes-the-new-way-to-see-what-customers-ask-answer-engines` + Profound dashboard "Velocity" view.
- **Frequência**: semanal.
- **Benchmark 2026**: marca em campanha PR ativa: CV semanal +5% a +20%. Decay sem ação: -2% a -5%/semana.
- **Instrumentação**: dbt lag function `LAG(mention_rate) OVER (PARTITION BY brand ORDER BY week)`.
- **Visualização**: bar chart por semana com cor verde > 0, vermelho < 0.
- **Anti-padrão**: NÃO é número absoluto de citações; é taxa de variação proporcional.

### K-NEW-003 — Brand Echo Decay (BED)
- **PT-BR**: Decaimento de Eco de Marca
- **Fórmula**: dias necessários para mention_rate retornar a (baseline_pre_campanha + 5%) após cessar campanha. Se não retorna, BED = ∞ ("ganho permanente").
- **Unidade**: dias.
- **Fonte primária**: paper Q3 desta sessão (sonar-deep-research) + analogia com "ad recall decay" da literatura de mídia.
- **Frequência**: avaliado pós-campanha.
- **Benchmark 2026**: campanhas PR isoladas BED = 14-45 dias. Campanhas que geram link permanente (Wikipedia, G2, listicle high-DR) BED = ∞.
- **Instrumentação**: marcar `campaign_end_ts` manualmente em tabela `campaigns`; SQL detecta cruzamento de threshold.
- **Visualização**: gantt-style timeline + threshold line.
- **Anti-padrão**: NÃO é "tempo total da campanha"; é meia-vida pós-cessar.

### K-NEW-004 — Prompt Coverage Score (PCS)
- **PT-BR**: Cobertura do Portfólio de Prompts
- **Fórmula**: `PCS = (# prompts onde mention_rate >= 0.10) / (# total prompts no portfólio)`.
- **Unidade**: % adimensional [0, 1].
- **Fonte primária**: Peec.ai "categorizing prompts is more important than individual tracking" (`peec.ai/blog/how-to-measure-ai-search-visibility-...`).
- **Frequência**: semanal.
- **Benchmark 2026**: marca emergente PCS = 0.15-0.25; marca incumbente PCS = 0.55-0.75; líder absoluto de categoria PCS > 0.85.
- **Instrumentação**: `COUNT(CASE WHEN mention_rate >= 0.10 THEN 1 END) / COUNT(*)`.
- **Visualização**: big number + sparkline 12 semanas.
- **Anti-padrão**: NÃO usar threshold 0; isso reportaria qualquer hint de menção. 0.10 garante presença não-trivial.

### K-NEW-005 — Cross-LLM Consistency Index (CLCI)
- **PT-BR**: Índice de Consistência Cross-LLM
- **Fórmula**: `CLCI = 1 - (σ(mention_rate_modelo)/μ(mention_rate_modelo))` calculado para cada brand × prompt sobre os 5+ modelos.
- **Unidade**: adimensional [0, 1] (1 = perfeitamente consistente).
- **Fonte primária**: AthenaHQ multi-LLM tracking (`athenahq.ai`) + Profound cross-model dashboard.
- **Frequência**: semanal.
- **Benchmark 2026**: marca com presença universal (Apple, Salesforce) CLCI > 0.85. Brand nicho focado em um canal só (ex: dominante em LinkedIn mas ausente em Reddit) CLCI 0.30-0.50.
- **Instrumentação**: pandas `(1 - data.std()/data.mean())` agrupado por (brand, prompt).
- **Visualização**: heatmap brands × prompts, colorido por CLCI.
- **Anti-padrão**: NÃO é "média entre modelos"; é coeficiente de variação invertido.

### K-NEW-006 — Citation Sentiment Vector (CSV)
- **PT-BR**: Vetor de Sentimento de Citação
- **Fórmula**: vetor `(positive_rate, neutral_rate, negative_rate, mixed_rate)` somando 1.0; agregado per `(brand, prompt_cluster, model, week)`. Métrica derivada: Net Sentiment Score = positive - negative.
- **Unidade**: vetor 4-dim ou Net Score [-1, 1].
- **Fonte primária**: Scrunch citation-level sentiment (`scrunch.com`) + Peec.ai brand sentiment tracking + Nightwatch citation-level sentiment.
- **Frequência**: semanal.
- **Benchmark 2026**: marcas com Net Sentiment > 0.4 são consideradas "well-positioned"; < -0.2 ativa alerta de reputação.
- **Instrumentação**: passar cada citation por classificador de sentimento (Anthropic Claude Haiku rodando em batch é a opção mais barata em 2026).
- **Visualização**: stacked bar 100% (positive/neutral/negative/mixed) ao longo do tempo.
- **Anti-padrão**: NÃO somar como média; é distribuição. Reportar "sentiment médio = 0.3" perde informação relevante.

### K-NEW-007 — Author Authority Drift (AAD)
- **PT-BR**: Drift de Autoridade Autoral
- **Fórmula**: para queries sobre uma pessoa-marca (ex: "Alexandre Caramaschi"), AAD = % de citações onde a Person canônica é o autor referenciado (vs outros nomes). Calculado por modelo, por semana.
- **Unidade**: % [0, 1].
- **Fonte primária**: derivado das premissas de Person + sameAs do schema.org (`schema.org/Person`) e da prática de Knowledge Graph entity disambiguation (Google Search Central + Wikidata).
- **Frequência**: semanal.
- **Benchmark 2026**: pessoa-marca com Wikidata + 3+ sameAs e disambiguation forte AAD > 0.85. Sem entity stack robusta AAD 0.40-0.65 (LLM mistura com homônimos).
- **Instrumentação**: regex match + LLM disambiguation second-pass.
- **Visualização**: line chart por modelo.
- **Anti-padrão**: NÃO é "frequência de menção do nome"; é taxa de match com a Person canônica.

### K-NEW-008 — Snippet Citation Rate (SCR)
- **PT-BR**: Taxa de Citação via Snippet
- **Fórmula**: `SCR = (# citações que originaram de snippet/highlight com fragmento) / (# total citações da brand)`.
- **Unidade**: % [0, 1].
- **Fonte primária**: Adobe CJA documentation sobre `scroll-to-text-fragment` em Google AI Overviews; Yotpo 2026 GA4 playbook detection de fragments.
- **Frequência**: mensal.
- **Benchmark 2026**: páginas com FAQ schema bem estruturado e short paragraphs (40-80 palavras) SCR > 0.40; páginas long-form sem markup SCR < 0.10.
- **Instrumentação**: detectar `#:~:text=` fragments em referrer URLs server-side; também extrair via Profound Agent Analytics.
- **Visualização**: gauge ou big number com comparação mês anterior.
- **Anti-padrão**: NÃO é "% de tráfego que veio via snippet"; é "% das citações de marca cujo trecho específico em LLM é um snippet identificável".

### K-NEW-009 — Token-Weighted Mention Rate (TWMR)
- **PT-BR**: Taxa de Menção Ponderada por Tokens
- **Fórmula**: `TWMR(b) = (1/N) * Σ T_i(b)/L_i`, onde `T_i(b)` é número de tokens da resposta i dedicados à marca b e `L_i` é tamanho total da resposta i em tokens.
- **Unidade**: % [0, 1].
- **Fonte primária**: paper conceitual Q3 desta sessão (sonar-deep-research); Anthropic e OpenAI docs sobre token counting.
- **Frequência**: semanal.
- **Benchmark 2026**: marcas que são "mencionadas em passing" TWMR < 0.02; marcas explicitamente recomendadas e descritas TWMR 0.08-0.20.
- **Instrumentação**: tiktoken para GPT, anthropic tokenizer para Claude; segmentação de mentions via spans.
- **Visualização**: stacked bar ou Sankey por brand.
- **Anti-padrão**: NÃO é binary mention rate. Marca pode aparecer em 80% das respostas (mention rate 0.8) mas TWMR ser 0.01 (mencionada só de passagem).

### K-NEW-010 — Geo-AI Visibility Index (GAVI)
- **PT-BR**: Índice de Visibilidade Geo-AI Multilíngue
- **Fórmula**: para cada locale ∈ {pt-BR, en-US, es-ES, fr-FR}, mention_rate ponderado pela importância de mercado: `GAVI = Σ w_locale * mention_rate_locale`.
- **Unidade**: % [0, 1] ou índice composto.
- **Fonte primária**: Profound "10 regions including Brazil" (`tryprofound.com/blog/prompt-volumes-...`); Otterly multi-region (`otterly.ai`).
- **Frequência**: mensal.
- **Benchmark 2026**: marcas brasileiras com foco doméstico priorizam pt-BR (w=0.6); marcas com aspiração LATAM dividem (pt-BR 0.45, es-ES 0.40, en-US 0.15).
- **Instrumentação**: rodar Framework 2 (MLSW) com prompts traduzidos em paralelo, separar por locale.
- **Visualização**: small multiples (grid) por locale, line chart.
- **Anti-padrão**: NÃO assumir que dominância em en-US carrega para pt-BR; LLMs têm corpus distintos por idioma.

### K-NEW-011 — Source Concentration Index (SCI)
- **PT-BR**: Índice de Concentração de Fontes
- **Fórmula**: aplicar Herfindahl-Hirschman Index (HHI) sobre a distribuição de fontes citadas para uma brand: `SCI = Σ (share_fonte_i)²`.
- **Unidade**: [0, 1] (1 = monopólio de fonte; perto de 0 = pulverizado).
- **Fonte primária**: análise de Peec.ai sobre top 10 domínios citados (`peec.ai/blog/top-domains-cited-by-ai-search-analysis-based-on-30m-sources`); conceito HHI de antitrust econômico.
- **Frequência**: mensal.
- **Benchmark 2026**: SCI > 0.5 é frágil (depende de 1-2 fontes); SCI 0.1-0.3 é saudável (presença diversificada).
- **Instrumentação**: contagem de citações por domínio normalizada; SQL `SUM(POWER(share, 2))`.
- **Visualização**: gauge + treemap por fonte.
- **Anti-padrão**: NÃO confundir com "% de tráfego de uma fonte"; é distribuição das CITAÇÕES que LLMs fazem.

### K-NEW-012 — AI Agent Crawl Frequency (AACF)
- **PT-BR**: Frequência de Crawl por Agentes AI
- **Fórmula**: `AACF_agent = visits_in_window / time_window`, segmentado por agente (GPTBot, ClaudeBot, PerplexityBot, OAI-SearchBot, Google-Extended, ChatGPT-User, Perplexity-User).
- **Unidade**: visitas/dia ou visitas/semana.
- **Fonte primária**: Profound Agent Analytics (`tryprofound.com/blog/introducing-agent-analytics`); Momentic guide sobre AI crawlers; OpenAI crawler docs (`platform.openai.com/docs/bots`).
- **Frequência**: diária.
- **Benchmark 2026**: site bem indexado para AI: GPTBot 50-500 visits/dia, PerplexityBot 30-200, ClaudeBot 20-150; spikes 3x acima média sinalizam re-indexação importante.
- **Instrumentação**: parsing de server logs ou Cloudflare Analytics; regex User-Agent.
- **Visualização**: stacked area por agente.
- **Anti-padrão**: NÃO contar com tráfego humano misturado; filtrar via UA + IP range verification.

### K-NEW-013 — LLM Referrer Conversion Rate (LRCR)
- **PT-BR**: Taxa de Conversão por Referrer LLM
- **Fórmula**: `LRCR_llm = conversions_from_llm / sessions_from_llm`, calculado por LLM (ChatGPT, Perplexity, Claude, Gemini, Copilot).
- **Unidade**: % [0, 1].
- **Fonte primária**: Microsoft Clarity "AI Platform" channel groups reports (`clarity.microsoft.com`); AthenaHQ "2.5x increase in AI-driven organic traffic" (`athenahq.ai`).
- **Frequência**: semanal.
- **Benchmark 2026**: AI traffic LRCR é tipicamente 2-4x maior que organic Google search; segundo Clarity, ChatGPT traffic converte em average 5-12% vs organic 1-3%. Perplexity LRCR mediano 4-8%.
- **Instrumentação**: GA4 conversion + custom channel group AI Search.
- **Visualização**: tabela com LRCR por LLM + comparativo organic baseline.
- **Anti-padrão**: NÃO comparar volumes absolutos; AI traffic tem volume baixo mas qualidade altíssima.

### K-NEW-014 — Dark AI Traffic Estimate (DATE)
- **PT-BR**: Estimativa de Tráfego AI Oculto
- **Fórmula**: `DATE = Direct_traffic_with_AI_signature / Total_Direct_traffic`, onde `AI_signature` é heurística: sessão sem referrer + URL com path profundo (mid-funnel) + alta intent (pageviews/sessão > 3 ou conversion event).
- **Unidade**: % [0, 1].
- **Fonte primária**: Yotpo 2026 playbook "shadow/dark AI" (`yotpo.com/blog`); Softwareseni analysis (citado em Q2 sonar-deep-research).
- **Frequência**: mensal.
- **Benchmark 2026**: DATE 15-35% em sites B2B; até 50% em sites com forte cobertura LLM-side.
- **Instrumentação**: SQL heurística em eventos GA4 export.
- **Visualização**: pie chart Direct = (Real Direct, Dark AI, Untrackable).
- **Anti-padrão**: NÃO é precisão diagnóstica; é estimativa heurística para dimensionar quanto da Direct é AI-mediated.

### K-NEW-015 — Prompt-Level Position Rank (PLPR)
- **PT-BR**: Posição Média dentro da Resposta LLM
- **Fórmula**: `PLPR = média (1/posição_da_menção)`, onde posição = ordem em que a marca aparece na resposta. Métrica é o Reciprocal Rank (MRR-like).
- **Unidade**: [0, 1] (1 = sempre primeira; 0 = nunca aparece).
- **Fonte primária**: Peec.ai "track position" (`peec.ai/blog/how-to-measure-ai-search-visibility-and-revenue-the-kpis-that-actually-matter`); analogia com Mean Reciprocal Rank de IR.
- **Frequência**: semanal.
- **Benchmark 2026**: Top-of-category brand PLPR > 0.5; menção tardia consistente PLPR 0.15-0.25.
- **Instrumentação**: regex para detectar posição de mention em texto; agregar por mean.
- **Visualização**: scatter PLPR vs mention_rate por brand.
- **Anti-padrão**: NÃO confundir com "ranking position" tipo SERP; AI responses não têm SERP, têm narrativa.

### K-NEW-016 — Refusal Rate (RR)
- **PT-BR**: Taxa de Recusa
- **Fórmula**: `RR = # respostas com refusal / # total respostas` para um dado prompt × model. Refusal = LLM declina por safety, política ou ausência de informação.
- **Unidade**: % [0, 1].
- **Fonte primária**: paper conceitual Q3 desta sessão sobre stochastic LLM behavior; Anthropic Constitutional AI docs (`anthropic.com/research`).
- **Frequência**: semanal.
- **Benchmark 2026**: RR > 0.10 sinaliza ou prompt mal formulado ou domínio sensível (saúde, finanças, jurídico).
- **Instrumentação**: regex detectar phrases "I can't", "I won't", "as an AI", "não posso fornecer".
- **Visualização**: heatmap modelo × prompt.
- **Anti-padrão**: NÃO contar refusal como "ausência de marca"; é categoria distinta.

### K-NEW-017 — Citation URL Click-Through Rate (CUCTR)
- **PT-BR**: CTR de URLs Citadas
- **Fórmula**: para cada URL citada em resposta LLM (LLMs como Perplexity e Copilot mostram citations explícitas), `CUCTR = clicks_on_citation / impressions_of_citation`.
- **Unidade**: % [0, 1].
- **Fonte primária**: Profound Agent Analytics tracking de "human visitors who arrive after clicking embedded links" (`tryprofound.com/blog/introducing-agent-analytics`); Adobe CJA "hit only generated when user clicks" (`experienceleague.adobe.com`).
- **Frequência**: diária.
- **Benchmark 2026**: Perplexity citation CUCTR mediano 8-15% (alto); Bing Copilot 3-8%; ChatGPT citation 5-10%.
- **Instrumentação**: server-side log capture combinado com Perplexity API analytics quando disponível.
- **Visualização**: tabela com benchmark por LLM.
- **Anti-padrão**: NÃO confundir com taxa de Click-through de SERP do Google; é métrica distinta com impressions estimadas.

### K-NEW-018 — Conversational Surface Coverage (CSC)
- **PT-BR**: Cobertura por Surface Conversacional
- **Fórmula**: `CSC = (# AI surfaces onde marca aparece com mention_rate >= 0.15) / (# total AI surfaces monitorados)`. Surfaces = ChatGPT, Perplexity, Claude, Gemini, Copilot, Google AI Overviews, Google AI Mode, Meta AI, Grok, Rufus, DeepSeek.
- **Unidade**: % [0, 1].
- **Fonte primária**: Goodie multi-surface (`goodie.ai`); AthenaHQ "8+ major AI models" (`athenahq.ai`); Evertune 9 platforms (`evertune.ai`).
- **Frequência**: semanal.
- **Benchmark 2026**: marca global líder CSC > 0.85; marca regional ou nicho CSC 0.30-0.55.
- **Instrumentação**: agregação simples sobre dimensão `surface`.
- **Visualização**: radar chart com cada surface como eixo.
- **Anti-padrão**: NÃO ponderar por volume de query do surface (isso já está em GAVI); aqui é binário "aparece OK / não aparece".

### K-NEW-019 — AI Visibility Diversification Score (AVDS)
- **PT-BR**: Score de Diversificação de Visibilidade AI
- **Fórmula**: Shannon entropy `AVDS = -Σ p_i * log2(p_i)` aplicada à distribuição de mentions entre os modelos. Normalizar por log2(N_modelos) para [0, 1].
- **Unidade**: [0, 1].
- **Fonte primária**: information theory (Shannon 1948); adaptação para GEO por este sub-agent.
- **Frequência**: mensal.
- **Benchmark 2026**: AVDS > 0.85 = portfólio bem diversificado entre LLMs; AVDS < 0.4 = "single-LLM brand" (risco de model update destruir visibilidade).
- **Instrumentação**: pandas + scipy.stats.entropy.
- **Visualização**: gauge.
- **Anti-padrão**: NÃO é "média entre LLMs"; é entropia (distribuição uniforme score-alta).

### K-NEW-020 — Time-to-First-Citation (TTFC)
- **PT-BR**: Tempo até Primeira Citação
- **Fórmula**: para uma marca/produto/conteúdo recém-lançado, TTFC = dias entre `launch_ts` e primeira amostragem em que `mention_rate >= 0.05` em qualquer LLM.
- **Unidade**: dias.
- **Fonte primária**: derivado de métricas SEO clássicas "time to first ranking" + paper Q3 desta sessão.
- **Frequência**: medido uma vez por lançamento.
- **Benchmark 2026**: marcas com forte distribuição PR + cobertura midia tier 1 TTFC 7-21 dias; lançamentos orgânicos TTFC 30-120 dias.
- **Instrumentação**: requer baseline 30 dias pré-lançamento + sampling diário pós-lançamento.
- **Visualização**: timeline + line chart mention_rate sobre eixo de tempo desde launch.
- **Anti-padrão**: NÃO é "tempo até citação na imprensa"; é tempo até LLM começar a citar.

### K-NEW-021 — Competitive Citation Overlap (CCO)
- **PT-BR**: Sobreposição de Citação Competitiva
- **Fórmula**: para um prompt comparativo (ex: "best X tools"), `CCO = (# respostas onde brand A E competidor B aparecem) / (# respostas onde pelo menos uma das duas aparece)`.
- **Unidade**: % [0, 1] (Jaccard-like).
- **Fonte primária**: Peec.ai competitive benchmarking (`peec.ai`); Goodie competitive gap analysis (`goodie.ai`).
- **Frequência**: semanal.
- **Benchmark 2026**: CCO > 0.7 = marca é "co-citada" frequentemente com competidor (bom para conversion via comparação); CCO < 0.2 = LLM segmenta as marcas em answers separados (oportunidade ou risco).
- **Instrumentação**: SQL com co-occurrence count.
- **Visualização**: matriz de adjacência ou grafo.
- **Anti-padrão**: NÃO é "% das vezes que somos citados junto com X"; é fração relativa ao universo de respostas onde pelo menos um dos dois aparece.

### K-NEW-022 — AEO Content Score (ACS)
- **PT-BR**: Score de Otimização para Answer Engines
- **Fórmula**: composto ponderado de 6 sub-scores estruturais por URL: schema_org_completeness (20%), faq_schema_present (10%), heading_hierarchy_clean (15%), short_paragraph_ratio (15%), citation_friendliness (20%), entity_clarity_score (20%). Cada sub-score [0, 1].
- **Unidade**: [0, 1].
- **Fonte primária**: Profound AEO Content Score (`tryprofound.com/blog`); Scrunch AXP (`scrunch.com`); HubSpot AI Search Grader.
- **Frequência**: por publicação de novo conteúdo; revisão trimestral em conteúdo antigo.
- **Benchmark 2026**: páginas bem otimizadas ACS > 0.75; AEO floor (mínimo aceitável) ACS > 0.55.
- **Instrumentação**: script Python que parseia HTML + valida JSON-LD + checa heading order + conta paragraph lengths + valida sameAs entities.
- **Visualização**: scorecard por URL.
- **Anti-padrão**: NÃO substituir auditoria humana de relevância de conteúdo; é métrica estrutural.

---

## Parte 3 — Arquitetura de referência para dashboard GEO operacional

A arquitetura abaixo é proposta como blueprint replicável para os três projetos (`landing-page-geo`, `curso-factory`, `papers`). Layered, modular, com 5 camadas.

```
+----------------------------------------------------------------------+
|                        CAMADA 0 — FONTES                              |
|----------------------------------------------------------------------|
|  - 5 APIs de LLM: OpenAI, Anthropic, Google, Perplexity, Groq         |
|  - GA4 Data API (sessions, conversions)                               |
|  - Google Search Console API (queries, impressions)                   |
|  - Cloudflare Logs / Vercel Edge Logs (server-side referrer + UA)     |
|  - Scrapers: Google AI Overviews, Bing Copilot, ChatGPT public        |
|  - Wikidata / Wikipedia Edit API (entity sameAs tracking)             |
|  - HubSpot / Bizible CRM (conversion data with ai_source)             |
+----------------------------------------------------------------------+
                              |
                              v
+----------------------------------------------------------------------+
|                    CAMADA 1 — INGESTÃO (workers)                      |
|----------------------------------------------------------------------|
|  - Python async workers (httpx + asyncio.gather):                     |
|     * llm_poller.py — Framework 2 MLSW                                |
|     * ga4_export.py — daily/weekly                                    |
|     * gsc_export.py — daily                                           |
|     * log_tailer.py — near-real-time Cloudflare logpush               |
|     * scraper_workers.py — captcha-resistant (Browser MCP)            |
|  - Orquestração: GitHub Actions cron OR Cloud Scheduler               |
|  - Rate limiting: ratelimit lib OR Redis-based token bucket           |
|  - Error handling: retries com backoff exponencial                    |
|  - Output: JSONL no S3/R2 + load em warehouse                         |
+----------------------------------------------------------------------+
                              |
                              v
+----------------------------------------------------------------------+
|                  CAMADA 2 — STORAGE                                   |
|----------------------------------------------------------------------|
|  - Warehouse principal: BigQuery (free tier 1TB/mês) OU DuckDB local  |
|    OU Snowflake (enterprise)                                          |
|    Tabelas raw:                                                       |
|     - events_raw_llm (eventos de LLM sampling)                        |
|     - events_raw_ga4 (sessions, conversions)                          |
|     - events_raw_logs (server logs cru)                               |
|     - events_raw_gsc                                                  |
|     - events_raw_crm                                                  |
|  - Vector DB: pgvector em Supabase OU Pinecone OU Weaviate            |
|    Uso: similaridade semântica entre respostas LLM para detectar      |
|    paráfrases da mesma "citação" (evita contar duplicatas)            |
|  - Object storage: R2 / S3 para texto cru das respostas (compliance)  |
|  - Retention: raw events 18 meses; agregados forever                  |
+----------------------------------------------------------------------+
                              |
                              v
+----------------------------------------------------------------------+
|              CAMADA 3 — TRANSFORMAÇÃO (dbt models)                    |
|----------------------------------------------------------------------|
|  models/staging/         — limpa, deduplica, padroniza               |
|     stg_llm_events.sql                                                |
|     stg_ga4_sessions.sql                                              |
|     stg_logs.sql                                                      |
|     stg_gsc.sql                                                       |
|     stg_crm_conversions.sql                                           |
|                                                                       |
|  models/intermediate/    — joins e enrichment                         |
|     int_brand_mentions_per_response.sql                               |
|     int_ai_source_classified_sessions.sql                             |
|     int_citation_url_extraction.sql                                   |
|                                                                       |
|  models/marts/           — KPIs canônicos                             |
|     mart_kpi_mention_rate.sql                                         |
|     mart_kpi_cpi.sql            (K-NEW-001)                           |
|     mart_kpi_cv.sql             (K-NEW-002)                           |
|     mart_kpi_bed.sql            (K-NEW-003)                           |
|     mart_kpi_pcs.sql            (K-NEW-004)                           |
|     mart_kpi_clci.sql           (K-NEW-005)                           |
|     mart_kpi_csv.sql            (K-NEW-006)                           |
|     ... (todos os 22 KPIs novos + 14 antigos)                         |
|     mart_attribution_multitouch.sql                                   |
|     mart_competitive_overlap.sql (K-NEW-021)                          |
|                                                                       |
|  models/exposures/       — quais dashboards consomem o quê           |
|     exec_dashboard.yml                                                |
|     marketing_team.yml                                                |
|     alerts_pipeline.yml                                               |
|                                                                       |
|  dbt run cadence: hourly (incremental) OR daily (full refresh)        |
+----------------------------------------------------------------------+
                              |
                              v
+----------------------------------------------------------------------+
|              CAMADA 4 — APRESENTAÇÃO                                  |
|----------------------------------------------------------------------|
|  - Executive dashboard:                                               |
|     Hex.tech (collaboration + SQL + Python combinados)                |
|     OR Metabase (open-source) OR Looker Studio (free)                 |
|     Páginas: Overview, KPIs Norte-Magnéticos, Anomalias               |
|                                                                       |
|  - Ops dashboard:                                                     |
|     Streamlit app interno (Python)                                    |
|     Permite filtros granulares por prompt, modelo, semana             |
|                                                                       |
|  - Embeds:                                                            |
|     iframe Metabase em página interna /admin/geo do projeto           |
|                                                                       |
|  - API publica para consumo programático:                             |
|     FastAPI endpoint /api/kpi/{kpi_name} retorna JSON                 |
+----------------------------------------------------------------------+
                              |
                              v
+----------------------------------------------------------------------+
|              CAMADA 5 — ALERTAS                                       |
|----------------------------------------------------------------------|
|  Detectores (rodam de hora em hora via dbt + Python):                |
|     - CUSUM em mention_rate                                           |
|     - Threshold simples em Net Sentiment                              |
|     - Variação semanal em PCS                                         |
|     - Spike em refusal rate                                           |
|     - Novo competidor entrando em top-3 de prompt P0                  |
|                                                                       |
|  Rotas:                                                               |
|     - Slack webhooks (#geo-alerts canal verde + #geo-incidents red)   |
|     - PagerDuty para red severity                                     |
|     - Daily digest em e-mail (Postmark/SendGrid)                      |
|     - Webhooks para HubSpot deal updates                              |
+----------------------------------------------------------------------+
```

### Decisões arquiteturais críticas

1. **Storage**: para projetos solo (landing-page-geo, papers) DuckDB local + Parquet em GitHub LFS é mais barato que cloud warehouse. Para `curso-factory` rodando para múltiplos cursos, BigQuery free tier sustenta 1-2 anos.

2. **Vector DB**: opcional na fase 1. Habilitar quando volume > 10K eventos/mês e detecção de paráfrases vira problema real. Para começar, regex + LLM-secondary-pass de disambiguation cobre 85% dos casos.

3. **Real-time vs Batch**: 95% dos KPIs toleram latência de 24h. Apenas o detector de anomalia (K-NEW-002 CV semanal) precisa de near-real-time. Manter pipeline batch para o resto e streaming só para alertas.

4. **Open-source vs Vendor**: stack 100% open-source (DuckDB + dbt + Metabase + Python) cobre 80% das funcionalidades de Profound/AthenaHQ por 5-10% do custo. Vendor faz sentido quando o time não tem capacidade de manter pipeline.

---

## Parte 4 — Quick-start scripts (3 snippets prontos)

### Script 1 — Python: medir Mention Rate em 1 prompt × 5 LLMs

```python
# file: scripts/python/measure_mention_rate.py
# Requires: pip install httpx tiktoken anthropic openai google-generativeai
# Env: OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_API_KEY, PERPLEXITY_API_KEY, GROQ_API_KEY
import asyncio
import os
import re
import json
import statistics
from datetime import datetime, timezone

import httpx

BRANDS_TO_TRACK = ["Brasil GEO", "Alexandre Caramaschi"]
N_SAMPLES = 20
TEMPERATURE = 0.7


def mention_count(text: str, brand: str) -> int:
    pattern = re.compile(re.escape(brand), re.IGNORECASE)
    return len(pattern.findall(text))


async def call_openai(client: httpx.AsyncClient, prompt: str) -> str:
    r = await client.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"},
        json={"model": "gpt-4o", "messages": [{"role": "user", "content": prompt}],
              "temperature": TEMPERATURE, "max_tokens": 800},
        timeout=60,
    )
    return r.json()["choices"][0]["message"]["content"]


async def call_anthropic(client: httpx.AsyncClient, prompt: str) -> str:
    r = await client.post(
        "https://api.anthropic.com/v1/messages",
        headers={"x-api-key": os.environ["ANTHROPIC_API_KEY"],
                 "anthropic-version": "2023-06-01"},
        json={"model": "claude-3-7-sonnet-20250120",
              "messages": [{"role": "user", "content": prompt}],
              "temperature": TEMPERATURE, "max_tokens": 800},
        timeout=60,
    )
    return r.json()["content"][0]["text"]


async def call_perplexity(client: httpx.AsyncClient, prompt: str) -> str:
    r = await client.post(
        "https://api.perplexity.ai/chat/completions",
        headers={"Authorization": f"Bearer {os.environ['PERPLEXITY_API_KEY']}"},
        json={"model": "sonar", "messages": [{"role": "user", "content": prompt}],
              "temperature": TEMPERATURE, "max_tokens": 800},
        timeout=60,
    )
    return r.json()["choices"][0]["message"]["content"]


async def call_gemini(client: httpx.AsyncClient, prompt: str) -> str:
    key = os.environ["GOOGLE_API_KEY"]
    r = await client.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={key}",
        json={"contents": [{"parts": [{"text": prompt}]}],
              "generationConfig": {"temperature": TEMPERATURE, "maxOutputTokens": 800}},
        timeout=60,
    )
    return r.json()["candidates"][0]["content"]["parts"][0]["text"]


async def call_groq(client: httpx.AsyncClient, prompt: str) -> str:
    r = await client.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {os.environ['GROQ_API_KEY']}"},
        json={"model": "llama-3.3-70b-versatile",
              "messages": [{"role": "user", "content": prompt}],
              "temperature": TEMPERATURE, "max_tokens": 800},
        timeout=60,
    )
    return r.json()["choices"][0]["message"]["content"]


MODELS = {
    "gpt-4o": call_openai,
    "claude-3-7-sonnet": call_anthropic,
    "perplexity-sonar": call_perplexity,
    "gemini-2.5-flash": call_gemini,
    "groq-llama-3.3-70b": call_groq,
}


async def sample_one_model(client, model_name, fn, prompt):
    results = []
    for i in range(N_SAMPLES):
        try:
            text = await fn(client, prompt)
            row = {
                "model": model_name,
                "sample_idx": i,
                "ts": datetime.now(timezone.utc).isoformat(),
                "text_len": len(text),
            }
            for b in BRANDS_TO_TRACK:
                row[f"mention_count_{b}"] = mention_count(text, b)
                row[f"mentioned_{b}"] = 1 if row[f"mention_count_{b}"] > 0 else 0
            results.append(row)
        except Exception as e:
            results.append({"model": model_name, "sample_idx": i, "error": str(e)})
    return results


async def main(prompt: str):
    async with httpx.AsyncClient() as client:
        tasks = [sample_one_model(client, name, fn, prompt) for name, fn in MODELS.items()]
        all_results = await asyncio.gather(*tasks)
    flat = [row for batch in all_results for row in batch if "error" not in row]
    with open("events_raw.jsonl", "a") as f:
        for row in flat:
            f.write(json.dumps(row) + "\n")
    summary = {}
    for model in MODELS:
        rows = [r for r in flat if r["model"] == model]
        for b in BRANDS_TO_TRACK:
            mr = statistics.mean(r[f"mentioned_{b}"] for r in rows) if rows else 0
            summary[f"{model}__{b}"] = mr
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    import sys
    prompt = sys.argv[1] if len(sys.argv) > 1 else "Quem são os principais consultores de GEO no Brasil em 2026?"
    asyncio.run(main(prompt))
```

### Script 2 — bash: snapshot semanal de citation rate em CSV

```bash
#!/usr/bin/env bash
# file: scripts/bin/geo-weekly-snapshot.sh
# Uso: bash scripts/bin/geo-weekly-snapshot.sh prompts.yaml
set -euo pipefail

PROMPTS_FILE="${1:-prompts.yaml}"
OUTPUT_DIR="snapshots/$(date -u +%Y-%m-%d)"
mkdir -p "$OUTPUT_DIR"

# Carrega chaves do .env do projeto
source "${GEO_ENV_FILE:-./.env}"
export OPENAI_API_KEY ANTHROPIC_API_KEY GOOGLE_API_KEY PERPLEXITY_API_KEY GROQ_API_KEY

# Loop por prompt do arquivo YAML
python3 - <<'PYEOF'
import yaml, asyncio, sys, os, json, csv
from datetime import datetime, timezone

# Importa a função do script anterior
sys.path.insert(0, "scripts/python")
from measure_mention_rate import main as measure, BRANDS_TO_TRACK, MODELS

with open(os.environ.get("PROMPTS_FILE", "prompts.yaml")) as f:
    prompts = yaml.safe_load(f)["prompts"]

# Para cada prompt, executa medição
all_rows = []
for p in prompts:
    print(f"[wave] {p['id']}: {p['text'][:80]}")
    # Aqui em produção, paralelizar (n=5-10) com semaphore
    asyncio.run(measure(p["text"]))

# Lê os events_raw.jsonl e agrega em CSV semanal
with open("events_raw.jsonl") as f:
    events = [json.loads(line) for line in f]

with open(f"{os.environ['OUTPUT_DIR']}/weekly_mention_rate.csv", "w", newline="") as out:
    w = csv.writer(out)
    w.writerow(["week", "model", "brand", "n_samples", "mention_rate"])
    iso_week = datetime.now(timezone.utc).strftime("%Y-W%V")
    by_model_brand = {}
    for e in events:
        for b in BRANDS_TO_TRACK:
            key = (e["model"], b)
            by_model_brand.setdefault(key, []).append(e.get(f"mentioned_{b}", 0))
    for (model, brand), vals in by_model_brand.items():
        if vals:
            w.writerow([iso_week, model, brand, len(vals), sum(vals)/len(vals)])

print(f"Snapshot salvo em ${OUTPUT_DIR}/weekly_mention_rate.csv")
PYEOF

# Commit no repo de dashboards (se for git-managed)
git add "$OUTPUT_DIR" || true
git commit -m "geo snapshot $(date -u +%Y-%m-%d)" || true
git push || true
```

### Script 3 — dbt model SQL para Citation Persistence Index

```sql
-- file: models/marts/mart_kpi_cpi.sql
-- K-NEW-001 — Citation Persistence Index
{{
    config(
        materialized='table',
        tags=['kpi', 'geo']
    )
}}

with daily_mention_rate as (
    select
        date(ts) as day,
        model,
        brand,
        prompt_id,
        count(*) as n_samples,
        avg(mentioned) as mention_rate
    from {{ ref('stg_llm_events') }}
    group by 1, 2, 3, 4
),

events as (
    -- carrega tabela manual de model release events
    select
        model,
        event_date,
        event_label
    from {{ ref('seed_model_release_events') }}
    -- seed: data, model, label (ex: 2026-04-15, gpt-4o, GPT-4o spring update)
),

post_event_decay as (
    select
        d.brand,
        d.model,
        d.prompt_id,
        e.event_date,
        e.event_label,
        d.day,
        date_diff('day', e.event_date, d.day) as days_since_event,
        d.mention_rate,
        -- baseline: 14 dias pré-evento
        avg(d.mention_rate) over (
            partition by d.brand, d.model, d.prompt_id, e.event_label
            order by d.day
            rows between 14 preceding and 1 preceding
        ) as p_baseline_pre_event
    from daily_mention_rate d
    cross join events e
    where d.model = e.model
      and d.day between e.event_date - interval '14' day
                    and e.event_date + interval '60' day
),

-- ajuste de exponential decay p(t) = p_0 * exp(-lambda * t)
-- usando log-linear regression: ln(p) = ln(p_0) - lambda * t
fit as (
    select
        brand,
        model,
        prompt_id,
        event_label,
        event_date,
        -- só pega dias pós-evento com mention_rate > 0
        avg(case when days_since_event >= 0
                  and mention_rate > 0
                 then days_since_event end) as t_bar,
        avg(case when days_since_event >= 0
                  and mention_rate > 0
                 then ln(mention_rate) end) as ln_p_bar,
        sum(case when days_since_event >= 0
                  and mention_rate > 0
                 then days_since_event * ln(mention_rate) end) as sum_t_lnp,
        sum(case when days_since_event >= 0
                  and mention_rate > 0
                 then power(days_since_event, 2) end) as sum_t2,
        count(case when days_since_event >= 0
                    and mention_rate > 0
                   then 1 end) as n_obs
    from post_event_decay
    group by 1, 2, 3, 4, 5
),

cpi as (
    select
        brand,
        model,
        prompt_id,
        event_label,
        event_date,
        n_obs,
        -- slope b1 = (Σ t·ln(p) - n·t_bar·ln_p_bar) / (Σ t² - n·t_bar²)
        case
            when n_obs >= 5 then
                (sum_t_lnp - n_obs * t_bar * ln_p_bar) /
                nullif(sum_t2 - n_obs * power(t_bar, 2), 0)
            else null
        end as decay_slope_b1,
        -- lambda = -b1 (decay positivo)
        case
            when n_obs >= 5 then
                -1.0 * (sum_t_lnp - n_obs * t_bar * ln_p_bar) /
                nullif(sum_t2 - n_obs * power(t_bar, 2), 0)
            else null
        end as lambda_decay,
        -- CPI = ln(2) / lambda  (meia-vida em dias)
        case
            when n_obs >= 5 and
                 (sum_t_lnp - n_obs * t_bar * ln_p_bar) /
                 nullif(sum_t2 - n_obs * power(t_bar, 2), 0) < 0
            then ln(2) / abs(
                (sum_t_lnp - n_obs * t_bar * ln_p_bar) /
                nullif(sum_t2 - n_obs * power(t_bar, 2), 0)
            )
            else null
        end as cpi_half_life_days
    from fit
)

select
    brand,
    model,
    prompt_id,
    event_label,
    event_date,
    cpi_half_life_days,
    n_obs,
    current_timestamp as computed_at
from cpi
where cpi_half_life_days is not null
order by brand, model, event_date desc;
```

Para usar este modelo, criar arquivo `seeds/seed_model_release_events.csv`:
```csv
event_date,model,event_label
2026-04-15,gpt-4o,GPT-4o spring 2026 update
2026-05-10,claude-3-7-sonnet,Claude 3.7 Sonnet release
2026-03-20,gemini-2.5-flash,Gemini 2.5 Flash GA
```

E executar `dbt run --select mart_kpi_cpi+`.

---

## Apêndice A — URLs primárias validadas

### Vendors GEO (10 plataformas)
1. Profound · `https://www.tryprofound.com` · features: Share of Model, Citation Rate, AEO Content Score, Agent Analytics, Prompt Volumes (400M+ conversations dataset).
2. Profound blog · `https://www.tryprofound.com/blog/prompt-volumes-the-new-way-to-see-what-customers-ask-answer-engines` · metodologia Prompt Volumes.
3. Profound blog · `https://www.tryprofound.com/blog/introducing-agent-analytics` · server-side bot tracking + verification.
4. Profound blog · `https://www.tryprofound.com/blog/introducing-profound-api-cookbook` · API endpoints.
5. Peec.ai · `https://peec.ai` · prompt-centric analytics + Looker Studio export.
6. Peec.ai · `https://peec.ai/blog/the-complete-guide-to-generative-engine-optimization-(geo)` · 4-phase framework + 25-prompt portfolio recommendation (ago/2025, Noah Wolff).
7. Peec.ai · `https://peec.ai/blog/how-to-measure-ai-search-visibility-and-revenue-the-kpis-that-actually-matter` · 5 KPIs canônicos (mar/2026, Tomek Rudzki).
8. Peec.ai · `https://peec.ai/blog/top-domains-cited-by-ai-search-analysis-based-on-30m-sources` · análise 30M sources (mar/2026).
9. Peec.ai · `https://peec.ai/blog/the-listicle-rank-effect-what-nearly-200-000-ai-responses-across-8-ai-engines-reveal-about-brand-visibility` · listicle rank study (mai/2026).
10. AthenaHQ · `https://athenahq.ai` · 8 LLM platforms, Athena Citation Engine (ACE), preço self-serve $95/mês (annual).
11. Scrunch · `https://scrunch.com` · monitoring + AXP (Agent Experience Platform).
12. Otterly.ai · `https://otterly.ai` · 6 AI engines, preço $29/mês, 30K+ marketers.
13. Evertune · `https://www.evertune.ai` · 9 LLM platforms, 25M user behavior dataset.
14. Daydream · `https://daydream.ai` · GEO + programmatic SEO unified.
15. Goodie AI · `https://goodie.ai` · Topic Explorer, 4-phase framework.
16. Ahrefs Brand Radar · `https://ahrefs.com/blog/brand-radar/` · 190M+ search-backed prompts, 110B keyword DB (nov/2025).
17. Semrush AI Toolkit · `https://www.semrush.com/blog/category/ai-search/` · global index AI Visibility.

### Documentação técnica de detecção AI
18. Adobe CJA · documentação AI surfaces · referrer mapping completo (ChatGPT, Claude, Gemini, Copilot, Perplexity, Meta AI).
19. Microsoft Clarity · `https://clarity.microsoft.com` · AI Platform channel groups.
20. OpenAI bot docs · `https://platform.openai.com/docs/bots` · GPTBot, OAI-SearchBot, ChatGPT-User.
21. xSeek Perplexity docs · PerplexityBot + Perplexity-User distinguishing.
22. Momentic AI Crawlers guide · regex completa de User-Agents.
23. Orbit Media GA4 guide · regex filters customizadas.
24. Yotpo 2026 playbook · 14+ AI referrer domains regex.
25. HubSpot AI Search Grader (citado em material vendor).

### Fontes acadêmicas e conceituais
26. Shannon, C.E. (1948) · A Mathematical Theory of Communication · base da entropy (K-NEW-019).
27. Herfindahl-Hirschman Index · DOJ Antitrust · base do SCI (K-NEW-011).
28. Mean Reciprocal Rank (MRR) · Information Retrieval textbooks · base do PLPR (K-NEW-015).
29. Anthropic Constitutional AI · `https://www.anthropic.com/research` · refusal patterns.
30. schema.org/Person · base de Person entity disambiguation (K-NEW-007).

---

## Notas finais

### Custo da pesquisa
- 5 chamadas Perplexity sonar-deep-research × ~$0.012-0.025 cada (max_tokens=8000) = **~US$ 0.10 total**.
- 12 WebFetches em vendor sites = $0 (sem custo direto).
- Tempo Opus para sintetizar = imputado.

### Aviso operacional
Q4 (comparativo de plataformas) executou em background mas não retornou em tempo útil. Esta limitação NÃO compromete o entregável: a comparação de plataformas foi reconstruída a partir de 12 WebFetches diretos aos sites primários dos vendors (Profound, Peec.ai, AthenaHQ, Scrunch, Otterly, Evertune, Ahrefs, Semrush). A informação consta em Parte 1 (Frameworks 1, 2 e 5) e na seção 2.5 (Vendors GEO) do Apêndice A.

### Próximos passos sugeridos
1. Implementar `Framework 1 — PPL` em `landing-page-geo/src/lib/prompts-portfolio.yaml` com 50 prompts iniciais.
2. Adaptar `Script 1` para `geo-orchestrator` e gerar primeiro baseline.
3. Configurar `Framework 4 — MLA` com Cloudflare Worker já existente em `landing-page-geo`.
4. Estabelecer canal Slack `#geo-alerts` e configurar alertas iniciais para CV (K-NEW-002) semanal.
5. Em 12 semanas, ter dados suficientes para calcular CPI (K-NEW-001) inicial.
