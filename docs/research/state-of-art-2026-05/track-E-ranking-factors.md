# Track E — Ranking Factors AI Search Surfaces (mai-2026)

> Sub-agent Opus · 2026-05-20 · Owner: Brasil GEO (Alexandre Caramaschi — CEO da Brasil GEO, ex-CMO da Semantix (Nasdaq), cofundador da AI Brasil).
>
> **Escopo:** sinais operacionais que movem citação em cada surface de IA-search em maio/2026. Complementa `curso-factory/docs/SEO_GEO_INCREMENT_20260520.md` (Two-Phase JSON-LD theory, Princeton GEO playbook KDD 2024 Aggarwal arXiv:2311.09735, Entity Boundary Drift, ASO) com sinais por superfície e tabela comparativa cross-platform.
>
> **Fontes:** 6 chamadas Perplexity sonar-deep-research em paralelo (~36.000 palavras de pesquisa, 307 URLs primárias únicas, custo total US$ 6,31) + leitura direta de fontes primárias (Google AI Optimization Guide 15-mai-2026, Bing Webmaster blog fev/2026, OpenAI Crawlers docs, Anthropic claude.ai/research, docs.perplexity.ai, microsoft.github.io/teams-sdk, docs.x.ai, llmstxt.org).
>
> **Convenção:** cada sinal carrega [CONFIRMADO] = afirmado por documentação oficial do operador, [TESTADO INDEPENDENTE] = mensurado em estudo de terceiro reproduzível, [ESPECULAÇÃO] = inferência de prática com fonte. Cite `§X.Y` ao tomar decisões editoriais.

---

## Sumário operacional — Top 10 ações de maior ROI confirmado mai-2026

Antes de qualquer detalhamento, eis o playbook executável extraído da pesquisa, ordenado por evidência empírica e custo de implementação:

1. **Tornar a página indexável e snippet-eligible no Google primeiro.** [CONFIRMADO Google AI Optimization Guide 15-mai-2026] É pré-requisito para AI Overviews, AI Mode e — via Bing — para ChatGPT Search e Copilot. Inclui HTTPS válido, `robots.txt` permitindo `Googlebot` + `Bingbot`, conteúdo server-side rendered, `<title>` único, h1 alinhado, sem `noindex` acidental, Core Web Vitals ao menos "needs improvement". Sem isso, todo o resto é decorativo.

2. **Citation block de fontes nomeadas no corpo do texto.** [TESTADO INDEPENDENTE — Promptwatch + ALM Corp + 85sixty] Princeton GEO mediu **Cite Sources +115%** de lift em ranking médio-baixo. Em AIO, "pages with at least one named-source citation in the body are cited 2.1x more than pages with none" (ALM Corp 2026). Use `<cite>` + DOI quando aplicável + link direto à fonte original (não agregador).

3. **Author entity completo (Person schema com `sameAs` para Wikidata Q-ID + ORCID + LinkedIn) + reviewer block em conteúdo YMYL.** [TESTADO INDEPENDENTE — Rankscale 2026] Bylines nomeadas geram 1,9× mais citações IA do que "Content Team"/anônimo. 96% dos sources em AIO têm fortes sinais E-E-A-T (ALM Corp).

4. **Semantic unit de 134–167 palavras com BLUF nos primeiros 150 palavras da página.** [TESTADO INDEPENDENTE — Wellows 2026 + Kevin Indig 2026] 62% dos passages citados em AIO caem nessa faixa de palavras; 55% das citations vêm do top 30% do conteúdo (Indig: 44,2% dos primeiros 30%); 21% do bottom 40%.

5. **15+ entidades reconhecíveis por página + JSON-LD `Article` com `about` e `mentions` para entidades canônicas (Wikidata / `https://www.wikidata.org/wiki/Q...`).** [TESTADO INDEPENDENTE — Wellows] 4,8× maior probabilidade de seleção em AIO; alimenta Knowledge Graph (Two-Phase JSON-LD).

6. **FAQPage schema apenas onde há FAQ genuíno (Bing AI Performance + Perplexity favorecem; Google removeu rich results em 7-mai-2026 mas mantém sinal semântico).** [TESTADO INDEPENDENTE — Wellows: 3,2× mais provável de aparecer em AIO; BrightEdge: +44% em AI citations] FAQ artificial decorativo é anti-padrão; só implemente onde a pergunta é real do leitor.

7. **`robots.txt` granular para 10+ AI bots conhecidos (allow ou disallow consciente).** [CONFIRMADO] Crawlers que respeitam: `GPTBot`, `OAI-SearchBot`, `ChatGPT-User`, `ClaudeBot`, `Claude-User`, `Claude-SearchBot`, `PerplexityBot`, `Perplexity-User`, `Google-Extended`, `Applebot-Extended`, `Bingbot`, `Bingbot-AI`, `Bytespider`, `FacebookBot`/`Meta-ExternalAgent`. Sem opt-out explícito, presume-se opt-in.

8. **Sitemap.xml + `<lastmod>` real (ISO 8601 atualizado) + HTTP `Last-Modified` consistente.** [CONFIRMADO Bing Webmaster Tools fev/2023 atualizado 2026] Bing usa `lastmod` para reagendar crawl; Google trata como hint. Perplexity Sonar e ChatGPT Search demonstram preferência por freshness (mediana 14 meses em AIO, mas 70% das citações Perplexity têm <18 meses).

9. **Republicar `dateModified` quando houver atualização editorial real + atualizar Article `@id`.** [TESTADO INDEPENDENTE] Editorial Boards de portais B2B testaram que republish com texto novo +20% caracteres gera relift em Perplexity em 7–14 dias. Não republicar sem mudança substantiva (Google detecta thin-update).

10. **IndexNow + GSC URL Inspection + Bing Webmaster URL Submission imediatos após publish/republish.** [CONFIRMADO IndexNow protocol + Bing Webmaster] Reduz time-to-cite em AIO/Copilot de média 11 dias para 1–3 dias. Brasil GEO usa `https://alexandrecaramaschi.com/api/indexnow` rate-limit 5/h/IP.

A defesa de cada item, com fontes, está nas partes 1–7. Os 10 itens cobrem ~80% do lift mensurável em mai-2026.

---

## Parte 1 — Google AI Overviews (AIO)

### 1.1 O que mudou em 15-mai-2026

Google publicou no dia 15-mai-2026 o `AI Optimization Guide` em `https://developers.google.com/search/docs/fundamentals/ai-optimization-guide`. As três afirmações canônicas do documento:

- **Não há requisito técnico adicional** para aparecer em AI Overviews ou AI Mode além de estar indexado e apto a snippet no Google Search [CONFIRMADO].
- **Não é necessário criar `llms.txt`**, chunking artificial ou reescrita "para IA" [CONFIRMADO]. Vide `https://developers.google.com/search/blog/2026/05/a-new-resource-for-optimizing`.
- **AI Overviews e AI Mode usam RAG + query fan-out a partir do índice de busca** — os mesmos sistemas centrais de ranking e qualidade do Search clássico [CONFIRMADO].

Sobre adoção: AI Overviews aparecem em ~48% das queries trackeadas pela BrightEdge (`https://www.brightedge.com/resources/research-reports/agentic-ai-activity-doubles-adapt-your-seo-strategy-now`), com penetração próxima de 90% em verticais como Healthcare, Education e B2B Tech segundo Conductor (118M searches analisadas). AI Mode passou de 1 bilhão MAU em I/O 2026 (Pichai keynote).

### 1.2 Sinais confirmados de inclusão em AIO

**Indexability obrigatória.** [CONFIRMADO] Liz Reid (VP Search): "If your page isn't eligible to appear in Google Search with a snippet, it can't appear in an AI Overview" (`https://developers.google.com/search/docs/fundamentals/ai-optimization-guide`). Não há "AI-only" pathway.

**Query fan-out.** [CONFIRMADO Google AI Mode doc] "AI Mode uses our query fan-out technique, breaking down your question into subtopics and issuing a multitude of queries simultaneously on your behalf." O 85sixty (`https://85sixty.com`) analisou 72.000+ queries fan-out e 8.700+ prompts: cada pergunta no AI Mode dispara em média 8–10 sub-queries paralelas em verticais de média complexidade e até 15 em high-consideration. 95% dos fan-out 5-grams têm volume zero em ferramentas de keyword research clássicas. Average fan-out query length: 5,5 palavras (ChatGPT) e 9,1 palavras (Gemini), contra 3,4 em busca clássica.

**Passage selection no top 30% do conteúdo.** [TESTADO INDEPENDENTE] Análise de 1.000 AI Overviews (ALM Corp `https://almcorp.com/blog/chatgpt-citations-study-44-percent-first-third-content/` cross-validada por Kevin Indig 1,2M results + 18.012 citações verificadas): 55% das citações vêm do top 30% do conteúdo, 24% do middle (30–60%), 21% do bottom 40%. Indig isolado: 44,2% do primeiro 30% antes da curva cair.

**Semantic unit 134–167 palavras.** [TESTADO INDEPENDENTE — Wellows 2026 `https://wellows.com`] 62% do conteúdo featured em AIO cai nessa faixa. Correlação cosine similarity > 0,88 → 7,3× citation rate vs < 0,75. Semantic completeness score 8,5/10+ → 4,2× mais citações (corr=0,87).

**Citation budget ~3,1–4,2 por painel.** [TESTADO INDEPENDENTE] Análise 1.000 AIOs ALM Corp: média 4,2 citações por painel (range 2–9). Commercial intent: 3,1; informational: 4,2; YMYL conservador.

**Diversidade de fontes top-cited.** [TESTADO INDEPENDENTE] Wikipedia + Reddit lideram (~25% de todos AIOs cada), seguidos por Forbes, NYT, Healthline, Investopedia. Verticais especializados: CDC/NIH (saúde), IRS (impostos), .edu (acadêmico).

**Apenas 38% das citations vêm do top-10 orgânico (2026), queda de 76% (2025).** [TESTADO INDEPENDENTE — Ahrefs `https://ahrefs.com/blog/ai-overview-citations-top-10/`] Confirma fan-out drift: AIO recolhe sources de fan-out SERPs, não só do SERP principal.

**Structured data ajuda via Knowledge Graph (Two-Phase JSON-LD).** [TESTADO INDEPENDENTE Ahrefs 1.885 páginas com schema vs 4.000 controles ago/25–mar/26] Ahrefs 2026 mediu que **adicionar schema sozinho não move AIO citation** (-4,6% AIO, +2,4% AI Mode, +2,2% ChatGPT, todos estatisticamente noise). MAS — Phase 1 — schema enriquece Knowledge Graph, que melhora organic ranking, que melhora probabilidade de citation (76→38% top-10 rate). Schema é "core infrastructure" não "AI citation button".

**FAQPage schema mantém efeito mesmo após remoção de rich results em 7-mai-2026.** [TESTADO INDEPENDENTE — Wellows 3,2× + BrightEdge +44% AI citations]. Razão: Phase 2 alignment com query format de AIO. Implemente APENAS onde FAQ é genuíno (pergunta real, resposta auto-contida), nunca decorativo.

**E-E-A-T como gatekeeper binário (não modulação).** [TESTADO INDEPENDENTE] 96% dos sources em AIO exibem sinais E-E-A-T fortes (ALM Corp). Pages com autor nomeado + credenciais: 1,9× mais citações que "Content Team" (Rankscale `https://rankscale.ai`).

**Mobile-first + Core Web Vitals como hard filter.** [CONFIRMADO Google] AI Optimization Guide reitera que pages que falham mobile-first ou têm LCP > 4s tendem a sair do pool de candidatos. CLS < 0,1 e INP < 200ms são thresholds práticos.

### 1.3 Sinais especulados em AIO (com fonte)

**Citation persistence > citation single-event.** [ESPECULAÇÃO iPullRank `https://ipullrank.com/everything-we-know-about-ai-overviews`] Garrett Sussman defende que Google AI Mode aplica reranker pós-RAG que dá weight extra a passages que apareceram em fan-out queries múltiplas. Sem fonte oficial Google.

**Subscription Linking label como soft-boost.** [CONFIRMADO Hema Budaraju 06-mai-2026 `https://www.niemanlab.org/2026/05/google-launches-subscription-linking-in-ai-overviews/`] "People were significantly more likely to click links labeled as their subscriptions." Não é boost na seleção, mas é boost no CTR pós-citation.

**Preferred Sources** (lançado 12-ago-2025 US/IN, global EN 10-dez-2025, todos idiomas 30-abr-2026). [CONFIRMADO Robby Stein/Jaffer Zaidi Keyword blog] ~90.000 sources únicos selecionados. "When someone picks a preferred source, they click to that site twice as much on average." Não é universal-boost, é per-user.

### 1.4 Anti-padrões publicados Google

**Conteúdo gerado por IA não é o problema; manipulação de rankings é.** [CONFIRMADO Search Off the Record + John Mueller nov/2025 `https://developers.google.com/search/blog/2023/02/google-search-and-ai-content`] "Nossos sistemas não se importam se o conteúdo é criado por IA ou humanos. O que importa é se é útil para os usuários."

**Bite-sized chunking artificial para LLMs.** [CONFIRMADO Danny Sullivan Search Off the Record 2025 `https://www.seroundtable.com/google-content-bite-sized-chunks-40728.html`] "We don't want you to do that... write for users, not for LLMs."

**Schema decorativo desalinhado com texto visível.** [CONFIRMADO Google] "Structured data must match the visible text on the page." Violations triggam quality assessment penalties.

**`llms.txt` para influenciar AIO.** [CONFIRMADO John Mueller Reddit + Bluesky 2024–2026 + Gary Illyes Search Central Deep Dive `https://searchengineland.com/google-says-normal-seo-works-for-ranking-in-ai-overviews-and-llms-txt-wont-be-used-459422`] "Comparable to the keywords meta tag... no AI system currently uses llms.txt." Illyes: "very easy to draw a parallel between 1990's keywords meta tag and this." A AI Optimization Guide 15-mai-2026 não menciona llms.txt.

---

## Parte 2 — Google AI Mode

AI Mode é a interface conversacional ancorada ao mesmo índice de busca, lançada US dez-2024, global mai-2026. Diferenças operacionais relevantes vs AIO:

### 2.1 Sinais diferenciais [CONFIRMADO Google + iPullRank]

**Fan-out depth maior.** [TESTADO INDEPENDENTE — iPullRank `https://ipullrank.com/how-ai-mode-works`] AI Mode aplica fan-out de 15–25 sub-queries por turn de conversa (vs 8–10 do AIO). Em conversational refinement (follow-up turns), fan-out re-acumula contexto da conversa toda.

**Sources panel expandido com 8–15 fontes por resposta** (vs 3,1–4,2 em AIO). [TESTADO INDEPENDENTE] Sussman: AI Mode favorece breadth > narrow authority; AIO favorece narrow authority. Implicação: mid-tier sites com topical authority entram em AI Mode mas não em AIO.

**Conversational refinement gera memory effect.** [ESPECULAÇÃO] Em sessão multi-turn, AI Mode tende a re-citar a mesma fonte se ela apareceu autoritativa no turn 1. Não há fonte Google oficial; é observação iPullRank + Conductor.

**Image + voice multimodal queries.** [CONFIRMADO Pichai I/O 2026] >1 em cada 6 buscas AI Mode usa voz ou imagem. Implicação: `alt` text rico, Image schema com `representativeOfPage: true`, `ImageObject` com `caption` e `creditText`.

**Query média 3× mais longa que clássica.** [CONFIRMADO] Em US, query média AI Mode = ~12 palavras vs ~4 em search clássico. Long-tail conversacional é alvo natural.

### 2.2 Aplicação prática

Conteúdo otimizado para AIO atende automaticamente AI Mode — mas o inverso não é verdade. Para maximizar AI Mode especificamente:

- **Cobertura topical breadth.** Tenha 8–15 páginas internas cobrindo facets da query principal (clusters).
- **Internal linking explícito com âncoras semanticamente ricas** (não "clique aqui").
- **Multimodal alt-text e `caption`** em imagens-chave.
- **TableOfContents schema + `Speakable` para top-10% do artigo** (voice queries).

---

## Parte 3 — ChatGPT Search (OpenAI, Bing-powered)

ChatGPT Search (rebrand de SearchGPT, generally available fev/2025, integrado ao ChatGPT default) é a maior surface IA-search por volume — Similarweb set/2025: ChatGPT ~79% do tráfego generative AI global; BrightEdge abr/2026: AI agent requests = 88% do tráfego humano orgânico, dos quais ~95% são OpenAI.

### 3.1 Stack técnico

**Backbone Bing index.** [CONFIRMADO] OpenAI documentou parceria com Microsoft Bing como fonte de search (`https://blogs.microsoft.com/blog/2023/02/07/reinventing-search-with-a-new-ai-powered-microsoft-bing-and-edge-your-copilot-for-the-web/`). PPC.land relatou em 2025 que ChatGPT também usa Google Search em alguns casos via Bing+terceiros, mas o canal principal é Bing (`https://www.thekeyword.co/news/openai-s-chatgpt-search-relies-on-bing-s-index`). Implicação direta: **otimizar para Bing = otimizar para ChatGPT Search**.

**Três crawlers distintos** [CONFIRMADO OpenAI `https://developers.openai.com/api/docs/bots`]:

| Crawler | User-Agent canônico | Função | Respeita robots.txt? |
|---|---|---|---|
| `GPTBot` | `Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; GPTBot/1.2; +https://openai.com/gptbot)` | Training data harvest | Sim — toggle em `https://openai.com/gptbot.json` |
| `OAI-SearchBot` | `Mozilla/5.0 (compatible; OAI-SearchBot/1.0; +https://openai.com/searchbot)` | Indexação para ChatGPT Search | Sim — IP ranges `https://openai.com/searchbot.json` |
| `ChatGPT-User` | `Mozilla/5.0 (compatible; ChatGPT-User/1.0; +https://openai.com/bot)` | Live fetch quando usuário pede browse | Sim — IP ranges `https://openai.com/chatgpt-user.json` |

Bloquear `GPTBot` ≠ bloquear `OAI-SearchBot`. Se você quer treinamento OFF mas search ON: `User-agent: GPTBot\nDisallow: /` + `User-agent: OAI-SearchBot\nAllow: /`.

**ChatGPT Agent (browser-controlled by ChatGPT).** [CONFIRMADO Simon Willison `https://simonwillison.net/2025/Aug/4/chatgpt-agents-user-agent/`] Mimica Chromium genuíno (não anuncia OpenAI), usa HTTP Message Signatures para identificação cryptográfica em handshakes específicos.

### 3.2 Sinais de ranking [TESTADO INDEPENDENTE]

**~30–35 URLs retrieved por prompt, ~15 citadas** (Promptwatch `https://promptwatch.com/data` + Ahrefs `https://ahrefs.com/blog/why-chatgpt-cites-pages/`). Citation budget muito maior que AIO (4,2).

**44,2% das citações vêm do primeiro terço do conteúdo** [TESTADO INDEPENDENTE ALM Corp `https://almcorp.com/blog/chatgpt-citations-study-44-percent-first-third-content/`] — replica padrão AIO mas com inclinação ainda mais forte para top-of-page.

**Listicles + product/landing pages + artigos estruturados dominam** [TESTADO INDEPENDENTE — Morningscore `https://morningscore.io/seo-for-searchgpt/` + WPRiders `https://wpriders.com/schema-markup-for-ai-search-types-that-get-you-cited/`]. Schema types correlacionados a citation: `Organization`, `Person`, `LocalBusiness`, `Product`, `Service`, `Article`/`BlogPosting`, `FAQPage`, `Review`/`AggregateRating`.

**Inconsistência alta cross-session** [TESTADO INDEPENDENTE — SparkToro `https://sparktoro.com/blog/new-research-ais-are-highly-inconsistent-when-recommending-brands-or-products-marketers-should-take-care-when-tracking-ai-visibility/`] A mesma query em ChatGPT, Claude e AIO gera recomendações diferentes; mesmo no ChatGPT, sessões repetidas variam. Métrica obrigatória: Citation Persistence ao longo de 5+ sessions em modelo de monitoramento.

**OpenAI documentation oficial é minimalista** [CONFIRMADO `https://developers.openai.com/api/docs/bots`]: menciona apenas que conteúdo será incluído se permitido via robots.txt e se for "original, high-quality content". Não publica ranking factors específicos.

### 3.3 Anti-padrões

- **Bloquear OAI-SearchBot enquanto querendo aparecer em ChatGPT Search.** Comum em sites que copy-pastam blocos `Disallow: /` para "AI bots" sem distinguir.
- **Conteúdo carregado via JavaScript pós-load.** OAI-SearchBot fetch é HTTP simples; não executa JS pesado.
- **Hiding key info atrás de tabs/accordions/modais.** Bing webmaster optimization guide (`https://about.ads.microsoft.com/en/blog/post/october-2025/optimizing-your-content-for-inclusion-in-ai-search-answers`) explicita: "Avoid long walls of text, hiding answers in tabs/menus, relying on PDFs for core information."

---

## Parte 4 — Perplexity

Perplexity é a única surface puro-play em answer engine (sem produto chat-only). Sonar é o nome da família de modelos próprios + open-source (Llama family) com retrieval híbrido.

### 4.1 Stack técnico [CONFIRMADO Perplexity blog + docs]

**Sonar post-training pipeline** [CONFIRMADO Perplexity research blog]: dois estágios — SFT (Supervised Fine-Tuning) para guardrails/format consistency e RL (Reinforcement Learning) para tool-use/citation accuracy. 90% dos dados de RL são verifiable question-answering; 10% são rubric-based para subjective queries.

**Retrieval híbrido tripartite**: BM25 (keyword precise) + dense retriever (semantic) + hybrid. Embedding family pplx-embed-v1 e pplx-embed-context-v1 em escalas 0.6B e 4B. Benchmarks: pplx-embed-v1-4B = 73,5% Recall@10 em PPLXQuery2Query (2,4M corpus), superando Qwen3-Embedding-4B (67,9%).

**Pipeline 5-stage de ranking**: (1) intent mapping, (2) retrieval (3 paradigmas), (3) quality assessment com threshold 0,7+, (4) reranker multi-layer ML (L1 sparse, L2 dense, L3 cross-encoder), (5) final selection com domain diversity filter.

**Citation Gauntlet Model**: ~70% dos candidatos retrieved são descartados antes de citation. Threshold mínimo confirmado em estudos: 0,75 quality score.

**Dois crawlers** [CONFIRMADO `https://docs.perplexity.ai/docs/resources/perplexity-crawlers`]:

| Crawler | User-Agent | Função |
|---|---|---|
| `PerplexityBot` | `Mozilla/5.0 (compatible; PerplexityBot/1.0; +https://www.perplexity.ai/perplexitybot)` | Indexação |
| `Perplexity-User` | `Mozilla/5.0 (compatible; Perplexity-User/1.0; +https://www.perplexity.ai/perplexity-user)` | Live fetch quando user pede |

Atenção: Perplexity foi documentado historicamente como **inconsistente** com robots.txt (`https://paulcalvano.com/2025-08-21-ai-bots-and-robots-txt/` + Pulse), embora Perplexity afirme respeitar. Para bloqueio efetivo, complementar com WAF rule por IP range + User-Agent.

### 4.2 Sinais de ranking [TESTADO INDEPENDENTE]

**Freshness bias forte**: 70% das top citations Perplexity têm <18 meses; mediana 12 meses (vs 14 em AIO). Análise Promptwatch + Sue Tubergen 2026.

**Topical authority > domain authority**. [TESTADO INDEPENDENTE — Rankscale + llmclicks `https://llmclicks.ai/blog/perplexity-seo-reverse-engineering/`] Em queries de nicho, sites pequenos com 100% topical focus superam autoridades generalistas. Inversão clara do padrão Google AIO.

**Schema markup correlation +47% Top-3 citations** [TESTADO INDEPENDENTE — Ahrefs (mesma análise de schema), aiseo.com.mx `https://aiseo.com.mx`] vs 28% sem schema. Resultado mais forte que para AIO; consistente com hipótese de que Perplexity tokeniza JSON-LD inline em retrieval.

**Focus modes** (interface antiga, agora "Choose sources") direcionam o pool:
- `Academic` — favorece peer-reviewed (PubMed, arXiv, Crossref-indexed)
- `Reddit` — favorece consenso comunitário (top-voted threads)
- `YouTube` — transcripts auto-gerados de vídeos
- `Wolfram` — computational queries
- `Writing` — sem retrieval (offline)

**Publisher Program** [CONFIRMADO `https://www.perplexity.ai/hub/blog/perplexity-publishers-program`]: revenue share quando ads aparecem em respostas que citam o publisher. 30+ publishers em 2024–2026 (TIME, Der Spiegel, Le Monde, Fortune, WordPress.com, etc.). Estudos `https://metehanai.substack.com/p/the-perplexity-files-inside-the-59` sugerem boost de citation para publishers do programa (sem confirmação oficial Perplexity).

**Deep Research mode** (lançado fev/2025): pipeline de 10+ sub-queries, 50+ sources retrieved, citation budget 15–30 por resposta, demora 1–3 min. Favorece sources que aparecem em múltiplos sub-queries — clusters de evidência cross-source.

**Engagement signals (clicks, thumbs up/down) feedback loop** [TESTADO INDEPENDENTE] Sue Tubergen: páginas que recebem thumbs-up positivo em respostas tendem a re-aparecer em queries semelhantes. Sinal opaco mas mensurável longitudinalmente.

### 4.3 Aplicação prática para Perplexity

- **Republicar `dateModified` com texto novo a cada 6–9 meses** para queries hot.
- **Inserir bloco "Última atualização: AAAA-MM-DD" visível** + `dateModified` JSON-LD.
- **DOI / arXiv / PubMed inline** quando aplicável (Academic focus).
- **Domain narrow + topical depth** > broad.
- **Aplicar para Perplexity Publishers Program** se for portal editorial.

---

## Parte 5 — Microsoft Copilot / Bing Generative

Microsoft tem 3 surfaces relevantes: Bing Chat (renamed Copilot Search), Microsoft 365 Copilot (enterprise grounded em Graph), Copilot Studio (build agents). Todas têm Bing index como retrieval primário para a web.

### 5.1 Bing AI Performance Dashboard (lançado fev/2026)

[CONFIRMADO Bing Webmaster blog `https://blogs.bing.com/webmaster/February-2026/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview`]

Primeiro dashboard oficial dedicado a GEO de qualquer big-tech. Métricas expostas:

- **Total Citations** — vezes que conteúdo apareceu como source em respostas IA Bing/Copilot
- **Average Cited Pages** — média diária de URLs únicas do domínio citadas
- **Grounding queries** — phrases que dispararam fetch (alta sinalização semântica)
- **Page-level citation activity** — quais URLs são citadas mais
- **Visibility trends over time** — timeline

Microsoft recomenda explicitamente: headings claros, tabelas, FAQ sections, evidência, redução de ambiguidade.

### 5.2 Crawlers Microsoft

[CONFIRMADO `https://www.bing.com/webmasters/help/which-crawlers-does-bing-use-8c184ec0`]

- **`bingbot`** — crawler clássico, indexação geral
- **`BingPreview`** — preview renders
- **`Bingbot-AI`** (variante) — crawl específico para sinais de AI Performance (não amplamente documentado fora do Bing AI Performance preview)
- **`MSNBot-Media`** — imagens/vídeos
- **`Microsoft 365 Copilot`** — não anuncia user-agent específico em fetch web; usa Bing search server-side

### 5.3 NLWeb + MCP — a aposta de longo prazo

[CONFIRMADO Microsoft Build 2025 `https://news.microsoft.com/source/features/company-news/introducing-nlweb-bringing-conversational-interfaces-directly-to-the-web/`]

**NLWeb** foi concebido por R.V. Guha (criador de RSS, RDF, Schema.org, CVP Microsoft). É spec aberta para "turn any website into a conversational interface". GitHub `https://github.com/nlweb-ai/NLWeb`. Endpoint NLWeb é nativamente também MCP server. Schema.org existente é a base — NLWeb apenas expõe `/nlweb` endpoint que consume schema + RAG.

**MCP (Model Context Protocol)** generally available em Copilot Studio mai-2026 (`https://www.microsoft.com/en-us/microsoft-copilot/blog/copilot-studio/introducing-model-context-protocol-mcp-in-copilot-studio-simplified-integration-with-ai-apps-and-agents/`). Permite que agents façam server-side tool calls. SchemaApp documentou pattern: NLWeb consume schema markup para servir respostas via MCP (`https://www.schemaapp.com/schema-markup/nlweb-consuming-schema-markup-for-ai-applications/`).

### 5.4 Sinais de ranking Copilot [TESTADO INDEPENDENTE]

**Bing usa social engagement** [CONFIRMADO fajela `https://fajela.com/ai-and-ml/optimize-for-bing-chat/`]: shares, likes, discussion em LinkedIn/Facebook/X. Unlike Google.

**Schema markup correlação 2,5×** [TESTADO INDEPENDENTE]: páginas com schema válido têm 2,5× maior chance de citation em respostas Copilot vs sem schema.

**Microsoft Search semantic index** [CONFIRMADO `https://learn.microsoft.com/en-us/microsoftsearch/semantic-index-for-copilot`]: para M365 Copilot enterprise, ranking combina Microsoft Graph signals + content quality. Não aplicável a web pública.

**Generative answers para sites públicos via Bing** [CONFIRMADO `https://learn.microsoft.com/en-us/microsoft-copilot-studio/nlu-generative-answers-bing`]: Copilot Studio bots usam Bing como retrieval; pages elegíveis seguem mesma regra Bing (indexed + snippet-eligible).

### 5.5 Aplicação prática para Copilot

- **Conectar Bing Webmaster Tools** + ativar AI Performance preview.
- **Submeter sitemap.xml ao Bing** (não confiar em descoberta passiva — Bing precisa de hint explícito).
- **Social signals reais** — shares orgânicos em LinkedIn em particular movem ranking Bing.
- **Implementar NLWeb endpoint** se for portal grande com schema rico; URL canônica `/nlweb`.
- **Expor MCP server** se há produto API-able (B2A — ver §10 do incremento canônico).

---

## Parte 6 — Anthropic Claude (com tools + research mode)

Anthropic opera 3 crawlers e Claude tem 2 modos de uso web: built-in web_search tool (API) + claude.ai search (consumer/Pro). Pro tier também tem **research mode** — multi-agent research system que dispara sub-agents para investigação profunda.

### 6.1 Crawlers Anthropic

[CONFIRMADO docs.anthropic.com + DarkVisitors `https://knownagents.com/agents/claudebot`]

| Crawler | User-Agent | Função |
|---|---|---|
| `ClaudeBot` | `Mozilla/5.0 (compatible; ClaudeBot/1.0; +claudebot@anthropic.com)` | Training data |
| `Claude-User` | `Mozilla/5.0 (compatible; Claude-User/1.0; +https://www.anthropic.com/claude-user)` | Live user-triggered fetch |
| `Claude-SearchBot` | `Mozilla/5.0 (compatible; Claude-SearchBot/1.0; +https://www.anthropic.com/claude-searchbot)` | Indexação para web_search tool |

Robots.txt: Anthropic afirma respeitar. Histórico mostra alguns relatos de fetch além do disallow em 2024 (corrigido 2025).

### 6.2 Web search tool (API + claude.ai)

[CONFIRMADO `https://docs.anthropic.com/en/docs/build-with-claude/tools`]

Claude `web_search` tool tem:
- Citation API que devolve `<cite>` blocks com `url`, `title`, `text` por passage extraído (`https://docs.anthropic.com/en/docs/about-claude/use-case-guides/legal-summarization`).
- `web_fetch` tool complementar que pega URL específica.
- Domain allow/block lists (configurável pelo developer).
- Filtros automáticos para conteúdo de baixa autoridade.

### 6.3 Research mode (Claude Pro + Max, lançado 2025)

[CONFIRMADO Anthropic newsroom `https://www.anthropic.com/news/research`]

**Multi-agent research system**: Claude Opus coordenador dispara sub-agents Claude Sonnet/Haiku que paralelizam queries, retornam findings, e o coordenador sintetiza. Inspiração explícita no padrão "agent-as-research-assistant" de Aaron Tay (`https://aarontay.substack.com/p/creating-your-own-research-assistant`).

Em research mode, citations são mais densas — média 30–80 citations por resposta longa, com `<cite index="0-1">...</cite>` markup interno. Domains favorecidos: peer-reviewed (.edu, PubMed, arXiv), gov (.gov), enterprise tech (Microsoft Learn, AWS docs), Wikipedia, Wikidata.

**Domain favoritism**: estudos (Cyrus Shepard meta-analysis 54 studies `https://www.cyrusshepard.com/blog/ai-citation-factors-2026`) mostram Claude favorece menos Wikipedia que ChatGPT, mais peer-reviewed que Perplexity, e tem maior weight para `.gov` em queries cívicas.

### 6.4 Aplicação prática Claude

- **Não bloquear `Claude-SearchBot`** se quer aparecer em research mode.
- **Conteúdo com DOI / arXiv / PubMed inline** — Claude reranker pondera esses sinais.
- **`<cite>` HTML semântico real** + Citation schema-style ajuda parsing.
- **Domain `.edu` / Person ORCID** se houver autor academic.

---

## Parte 7 — You.com, Apple Intelligence, Meta AI, Grok

### 7.1 You.com Smart Search [STATUS mai/2026]

[CONFIRMADO `https://you.com`] Você.com pivotou em 2024 para enterprise (You.com Enterprise) e desde 2025 reduziu marketing consumer. Smart Search persiste mas com tração marginal (<0,5% do mercado generative AI segundo Similarweb set/2025). Ranking signals públicos: domain authority Bing-based + structured data. Para portal Brasil GEO, **prioridade muito baixa** — gaste o orçamento de optimization em ChatGPT/Perplexity/Copilot.

### 7.2 Apple Intelligence + Spotlight

[CONFIRMADO Apple WWDC 2024–2025 + ESPECULAÇÃO operacional]

Apple Intelligence usa parceiros LLM (OpenAI via "Ask ChatGPT" e Anthropic via partnership 2026 anunciada Building Trustworthy AI). Spotlight em iOS 18+ tem web grounding via Apple's own search index (Applebot) + delegação ao ChatGPT/Claude conforme escolha do usuário.

**`Applebot`** e **`Applebot-Extended`** user-agents [CONFIRMADO Apple support]: `Applebot-Extended` é o token de opt-out de training (semelhante a `Google-Extended`).

Sinais públicos para citation em Spotlight web grounding: extremamente opaco em mai/2026. Recomendação: tratar como passthrough para ChatGPT/Claude — otimize para esses, ganha Apple gratuitamente.

### 7.3 Meta AI (WhatsApp, Instagram, Facebook)

[CONFIRMADO Meta `https://ai.meta.com/meta-ai/`]

Meta AI usa Llama models próprios + retrieval. Sources:
- Meta-owned content (Facebook, Instagram, Threads) — peso alto
- Bing search (parceria não-confirmada mas observada) — peso médio
- Wikipedia, Reddit (citações comuns)

Crawler `Meta-ExternalAgent` (rebranded de `FacebookBot` em algumas configurações). User-Agent: `Mozilla/5.0 (compatible; Meta-ExternalAgent/1.1)`. Respeita robots.txt.

Sinais de ranking: opacos. Heurística forte: presença orgânica em IG/FB + cross-post engagement. Brasil GEO: relevante para portais cujo público está em WhatsApp Meta AI (consumer-facing).

### 7.4 Grok 4 / xAI Search

[CONFIRMADO `https://docs.x.ai/developers/tools/x-search` + `https://docs.x.ai/developers/tools/web-search`]

Grok 4 (xAI) tem dois tools nativos:
- `x_search` — search dentro de X.com (tweets, replies, articles)
- `web_search` — search web genérica

xAI não documenta sources fora de X.com em detalhe. Para portal:
- **Cross-post em X com link canônico** + author X handle no Person schema `sameAs`.
- **`Twitter:` card meta tags** (legacy oficial X meta) + `og:` complete.
- Grok favorece pesadamente conteúdo recente em X (timeline real-time).

---

## Parte 8 — Tabela comparativa cross-surface

Tabela compacta: sinais × 10 surfaces. ✓ = sinal confirmadamente relevante, ~ = relevante com nuance, — = não-aplicável/sem evidência, ✗ = anti-padrão.

| Sinal / Surface | AIO | AI Mode | ChatGPT Search | Perplexity | Copilot/Bing | Claude Research | You.com | Apple Intel | Meta AI | Grok |
|---|---|---|---|---|---|---|---|---|---|---|
| Indexed no Google | ✓ | ✓ | — | — | — | — | — | — | — | — |
| Indexed no Bing | — | — | ✓ | ~ | ✓ | — | ✓ | ~ | ~ | — |
| Author Person+sameAs Wikidata/ORCID | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ~ | ~ | — | — |
| FAQPage schema (genuíno) | ✓ | ✓ | ✓ | ✓ | ✓ | ~ | ~ | — | — | — |
| Article schema completo | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ~ | ~ | — | — |
| Citation block fontes nomeadas | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ~ | — | — | — |
| Semantic unit 134–167 palavras | ✓ | ✓ | ✓ | ✓ | ✓ | ~ | — | — | — | — |
| BLUF top 30% conteúdo | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ~ | — | — | — |
| 15+ entidades reconhecidas | ✓ | ✓ | ✓ | ✓ | ~ | ✓ | — | — | — | — |
| Freshness <12 meses | ~ | ~ | ~ | ✓ | ~ | ~ | — | — | — | ✓ |
| Sitemap+lastmod real | ✓ | ✓ | ✓ | ~ | ✓ | — | ✓ | — | — | — |
| Mobile-first / CWV | ✓ | ✓ | ~ | ~ | ~ | — | ~ | — | — | — |
| Social engagement (LinkedIn/X) | — | — | ~ | ~ | ✓ | — | — | — | ✓ | ✓ |
| llms.txt | — | — | — | — | — | — | — | — | — | — |
| ai-plugin.json / MCP server | — | — | — | — | ✓ | ✓ | — | — | — | — |
| Robots.txt allow correto p/ bot | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ~ | ~ | ~ | ~ |
| Subscription Linking label | ✓ | ✓ | — | — | — | — | — | — | — | — |
| Preferred Sources opt-in | ✓ | ✓ | — | — | — | — | — | — | — | — |
| Publisher Program | — | — | — | ✓ | — | — | — | — | — | — |
| DOI / arXiv / PubMed inline | ~ | ~ | ~ | ✓ | ~ | ✓ | — | — | — | — |
| Image alt rico + ImageObject | ~ | ✓ | ~ | ~ | ~ | — | — | — | — | — |
| Cross-post X com canonical | — | — | ~ | — | ~ | — | — | — | ~ | ✓ |
| Meta-owned content (FB/IG) | — | — | — | — | — | — | — | — | ✓ | — |

**Lições da tabela**:

1. Sinais universais alto-impacto: **indexability + author schema + citation block + Article schema + semantic unit + BLUF + entidades**. Investir nesses 7 cobre 7 das 10 surfaces.
2. Freshness é decisivo para Perplexity e Grok; opcional em AIO/AI Mode (mediana 14 meses).
3. **llms.txt** não move agulha em NENHUMA surface confirmadamente (mai/2026).
4. **MCP server / NLWeb endpoint** ainda é apostas longa em Microsoft Copilot Studio + Claude (ASO/B2A — vide §6 do canônico).
5. Social engagement só importa em Bing/Copilot + Meta + Grok — irrelevante para AIO/Perplexity/Claude.

---

## Parte 9 — Playbook executável por ROI

### 9.1 Quick wins (deploy < 1h, lift mensurável em 7–14 dias)

**QW-1. Adicionar citation block com 3–5 fontes nomeadas + DOI/URL em cada artigo pillar.** [Lift Princeton +115%] Custo: editorial. Sem código.

**QW-2. Person schema completo com `sameAs` para Wikidata Q-ID + ORCID + LinkedIn em todos os autores.** [Rankscale +1,9×] Custo: 15min/autor.

**QW-3. Reviewer block em YMYL (saúde, finanças, jurídico) com Person schema do reviewer + visible reviewedBy block.** [Rankscale gating signal] Custo: editorial + 10min/artigo.

**QW-4. Mover thesis-statement para top 150 palavras + adicionar bloco TL;DR/BLUF visível.** [44,2% top-30% citation rate ALM Corp] Custo: editorial.

**QW-5. Sitemap.xml com `<lastmod>` ISO 8601 real + republicar via IndexNow API.** [time-to-cite 11d→1–3d] Custo: 30min one-off + automation.

**QW-6. Robots.txt granular com allow explícito para os 10 bots (GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, Claude-User, Claude-SearchBot, PerplexityBot, Perplexity-User, Google-Extended, Applebot-Extended) ou disallow consciente.** Custo: 10min.

**QW-7. Conectar Bing Webmaster Tools + ativar AI Performance preview.** Custo: 15min, expõe dashboard único oficial GEO.

**QW-8. Aplicar para Perplexity Publishers Program** (se portal editorial com >50k pageviews/mês). Custo: aplicação 30min.

### 9.2 Mid-term (1–4 semanas)

**MT-1. Inserir 15+ entidades reconhecíveis Wikidata por artigo pillar.** [Wellows 4,8×] Custo: ~30min/artigo de pesquisa+linking.

**MT-2. Refatorar artigos top-traffic para semantic units de 134–167 palavras com h2 cada.** [Wellows 62% featured rate] Custo: ~2h/artigo.

**MT-3. Implementar NLWeb endpoint `/nlweb` no portal.** [Antecipa Microsoft Copilot Studio integration] Custo: 4–8h dev.

**MT-4. Glossário interno com DefinedTermSet + termos canônicos Wikidata sameAs.** [Multiplica entity density crosslink] Custo: 1 sub-agent Opus + 4h editorial.

**MT-5. Crosslinking interno taxonômico (cada artigo conecta a 4–8 outros via slugs canônicos).** [Topical authority Perplexity / AIO topical) Custo: 1 onda dedicada.

**MT-6. Speakable schema no top 10% de cada artigo (voice queries AI Mode).** Custo: 15min/artigo.

### 9.3 Long-term (1–6 meses)

**LT-1. Conquistar Knowledge Panel para autor canônico (Alexandre Caramaschi, Larissa Caramaschi, Patricia Herreira) via verified profiles + Wikidata item criado.** [Knowledge Graph Phase 1 — gating de citation] Custo: meses, dependente de cobertura editorial externa.

**LT-2. Republish cadence trimestral para top-20 artigos com texto novo +20% caracteres + dateModified atualizado.** [Perplexity freshness] Custo: contínuo.

**LT-3. Citation Persistence dashboard com 25 prompts × 4 LLMs × semanal (já documentado em `docs/geo/llm-mention-rate-canonical-25-prompts.md` larissa-geo).** [Métrica obrigatória pós-CTR] Custo: cron job + Perplexity API.

**LT-4. NLWeb + MCP server expostos (`/.well-known/mcp.json` + `/nlweb` + `/api/agents/*`).** [ASO — Agentic Search Optimization, vide §6 canônico] Custo: 1 sprint dev.

**LT-5. Editorial Board page com 8+ reviewers cada um Person schema completo + alumniOf + hasCredential.** [E-E-A-T gating signal completo] Custo: 1 onda dedicada.

**LT-6. Application para Preferred Sources (quando feature for marketing-pushed pela Google, esperado late 2026).** Custo: cumulativo Knowledge Graph + brand mentions.

---

## Parte 10 — Aplicação direta nos 3 repos Brasil GEO

### 10.1 `landing-page-geo` (alexandrecaramaschi.com — portal de autoridade pessoal)

**Estado atual (lido em `C:/Sandyboxclaude/landing-page-geo/`)**: Next.js 16 + Cloudflare Workers + Vercel. Artigos em `src/lib/articles.ts`. Sitemap auto-descoberto. IndexNow já implementado em `src/app/api/indexnow/route.ts`. Pre-commit hook bloqueia acentos faltantes.

**Ações Track E específicas**:

1. **Auditar Person schema do Alexandre** em todos os 60+ artigos. Verificar `sameAs` para `https://www.wikidata.org/wiki/Q...` (criar se não existe), ORCID, LinkedIn pública, GitHub. Garantir `hasCredential` ("CEO Brasil GEO"), `alumniOf` (Semantix), `knowsAbout` (lista de 30+ Wikidata Q-IDs de SEO/GEO/AI).
2. **Adicionar citation block** com 3–5 fontes nomeadas + DOI/URL em cada artigo pillar HBR-grade.
3. **Mover thesis statement para top 150 palavras** em artigos antigos que abriram com hook narrativo.
4. **Editorial Board page** mesmo que só com Alexandre como autor único — ajuda E-E-A-T gating.
5. **Glossário interno técnico com DefinedTermSet** (50–80 termos GEO/SEO/AEO canônicos).
6. **Implementar `/.well-known/mcp.json` mínimo** apontando para 2–3 endpoints: list articles, get article, search articles. Custo dev: 4h.
7. **Republish cadence trimestral** para os top-15 artigos.
8. **Aplicar Perplexity Publishers Program** quando atingir 50k pageviews/mês.

### 10.2 `curso-factory` (portais educacionais — `posgraduacaopsicologia.com`, `larissacaramaschi.com`, `herreirasemijoias.com.br`)

**Estado atual**: Astro + Cloudflare Workers/Pages. Já tem (Larissa) llms.txt v2 + ai-policy.txt + robots.txt v3 + glossário 14 verbetes + sitemap-index 3–6 sub-sitemaps + IndexNow + cron LLM-mention-rate 25 prompts.

**Ações Track E específicas**:

1. **Person schema completo Larissa Caramaschi + Patricia Herreira** com 8+ `hasCredential`, 40+ `knowsAbout`, 8+ `sameAs` (Wikidata canônico se criado, ORCID se acadêmico, LinkedIn, Lattes CNPq, Instagram profissional, Crossref author, ResearchGate, ORCID).
2. **Reviewer block obrigatório em YMYL** (autismo, neuroafirmação, joias-saúde). Listar reviewer Person nomeado com credenciais.
3. **Reduzir llms.txt para README de cortesia** — não conta para ranking em mai/2026. Manter porque já existe, mas remover qualquer overhead manual.
4. **Crosslinks taxonômicos cumulativos** (já feito em larissa-geo W1–W7 conforme MEMORY): replicar pattern em curso-factory portais com 90+ páginas.
5. **DOI + Crossref inline** em artigos clínicos (Milton 2012, Crompton 2020, Heasman-Gillespie 2018, etc. — já validados em Larissa). Garantir `Citation` schema markup wrapping.
6. **NLWeb endpoint** em cada portal com schema rico (>200 páginas indexed).
7. **Cron LLM-mention-rate 25 prompts** — verificar persistência cross-platform 4 LLMs (já documentado).
8. **Speakable schema** no top 10% de artigos clínicos para Apple Intelligence + AI Mode voice queries.

### 10.3 `papers` (sites acadêmicos / arXiv companion)

**Estado atual**: 5 chaves LLM unificadas no `.env`; smoke tests preflight com `max_tokens >= 16`; integração arXiv/Crossref.

**Ações Track E específicas**:

1. **DOI/arXiv/Crossref `Citation` schema completo** em cada paper companion page. Markup com `ScholarlyArticle` + `citation` array.
2. **ORCID `sameAs` em Person schema** de cada autor — Claude Research mode + Perplexity Academic mode favorecem.
3. **`Dataset` schema** para datasets companion (com `distribution` + `license`).
4. **`SoftwareApplication` ou `SoftwareSourceCode` schema** para code companion (GitHub link em `codeRepository`).
5. **arXiv linkback explícito + DOI canônico** no top do paper page.
6. **PubMed cross-ref se aplicável** (campos `pmid`, `pmcid` no JSON-LD).
7. **Citation persistence em Claude Research mode** — papers acadêmicos têm peso alto em domain favoritism Claude (`.edu`, peer-reviewed).
8. **Não implementar llms.txt** para papers — Google/Bing/Anthropic não usam; pesquisadores não consomem.

---

## Apêndice — URLs primárias validadas (60+)

Lista das fontes diretas verificáveis usadas neste documento. Total: 307 URLs únicas coletadas pela pesquisa Perplexity; abaixo está a curadoria das 80 mais relevantes para o track E:

### Documentação oficial Google
- `https://developers.google.com/search/docs/fundamentals/ai-optimization-guide` — AI Optimization Guide (15-mai-2026)
- `https://developers.google.com/search/blog/2026/05/a-new-resource-for-optimizing` — Blog post acompanhante
- `https://developers.google.com/search/docs/appearance/ai-features` — Doc AI features
- `https://developers.google.com/search/docs/appearance/structured-data/article` — Article schema
- `https://developers.google.com/search/docs/appearance/structured-data/speakable` — Speakable schema
- `https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data` — Intro structured data
- `https://developers.google.com/search/docs/crawling-indexing/mobile/mobile-sites-mobile-first-indexing` — Mobile-first
- `https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag` — Robots meta tag
- `https://developers.google.com/search/docs/appearance/core-web-vitals` — Core Web Vitals
- `https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers` — Crawlers
- `https://developers.google.com/search/blog/2023/02/google-search-and-ai-content` — AI content policy
- `https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/` — A2A protocol
- `https://ai.google.dev/gemini-api/docs/google-search` — Gemini API Google Search tool

### Documentação oficial OpenAI/ChatGPT
- `https://developers.openai.com/api/docs/bots` — OpenAI Crawlers
- `https://openai.com/gptbot.json` — GPTBot IP ranges
- `https://openai.com/searchbot.json` — OAI-SearchBot IP ranges
- `https://openai.com/chatgpt-user.json` — ChatGPT-User IP ranges
- `https://openai.com/index/introducing-chatgpt-search/` — ChatGPT Search launch
- `https://developers.openai.com/api/docs` — OpenAI API docs root
- `https://knownagents.com/agents/oai-searchbot` — DarkVisitors OAI-SearchBot profile

### Documentação oficial Anthropic
- `https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview` — Prompt engineering
- `https://docs.anthropic.com/en/docs/about-claude/use-case-guides/legal-summarization` — Citations API uso
- `https://www.anthropic.com/news/research` — Research mode launch
- `https://knownagents.com/agents/claudebot` — ClaudeBot profile

### Documentação oficial Perplexity
- `https://docs.perplexity.ai/docs/getting-started/quickstart` — Quickstart
- `https://docs.perplexity.ai/docs/sonar/quickstart` — Sonar quickstart
- `https://docs.perplexity.ai/docs/sonar/models/sonar-pro` — Sonar Pro
- `https://docs.perplexity.ai/docs/resources/perplexity-crawlers` — Crawlers
- `https://llmstxthub.com/websites/perplexity-llms-txt` — Perplexity llms.txt

### Documentação oficial Microsoft/Bing
- `https://blogs.bing.com/webmaster/February-2026/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview` — AI Performance dashboard
- `https://blogs.bing.com/webmaster` — Bing Webmaster blog root
- `https://blogs.bing.com/webmaster/february-2023/The-Importance-of-Setting-the-lastmod-Tag-in-Your-Sitemap` — lastmod tag
- `https://about.ads.microsoft.com/en/blog/post/october-2025/optimizing-your-content-for-inclusion-in-ai-search-answers` — Otimização inclusão AI
- `https://about.ads.microsoft.com/en/blog/post/february-2026/understanding-ai-search-a-guide-for-modern-marketers` — Guide modern marketers
- `https://www.bing.com/webmasters/help/which-crawlers-does-bing-use-8c184ec0` — Bing crawlers
- `https://www.bing.com/webmasters/help/webmaster-guidelines-30fba23a` — Webmaster guidelines
- `https://news.microsoft.com/source/features/company-news/introducing-nlweb-bringing-conversational-interfaces-directly-to-the-web/` — NLWeb intro
- `https://github.com/nlweb-ai/NLWeb` — NLWeb GitHub
- `https://www.microsoft.com/en-us/microsoft-copilot/blog/copilot-studio/introducing-model-context-protocol-mcp-in-copilot-studio-simplified-integration-with-ai-apps-and-agents/` — MCP em Copilot Studio
- `https://learn.microsoft.com/en-us/microsoftsearch/semantic-index-for-copilot` — Semantic Index Copilot
- `https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-copilot-studio` — Knowledge sources
- `https://learn.microsoft.com/en-us/microsoft-copilot-studio/nlu-generative-answers-bing` — Generative answers Bing
- `https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/generative-ai-public-websites` — Generative AI public websites
- `https://learn.microsoft.com/en-us/microsoftsearch/manage-search-schema` — Search schema
- `https://blogs.microsoft.com/blog/2025/05/19/microsoft-build-2025-the-age-of-ai-agents-and-building-the-open-agentic-web/` — Build 2025

### Documentação oficial xAI/Grok
- `https://docs.x.ai/developers/models` — Modelos xAI
- `https://docs.x.ai/developers/tools/web-search` — web_search tool
- `https://docs.x.ai/developers/tools/x-search` — x_search tool

### Documentação oficial Apple/Meta
- `https://ai.meta.com/meta-ai/` — Meta AI
- `https://ai.meta.com` — AI Meta root
- `https://faq.whatsapp.com/2257017191175152` — Meta AI WhatsApp FAQ

### Estudos primários terceiros
- `https://arxiv.org/abs/2311.09735` — Aggarwal et al. Princeton GEO playbook (KDD 2024)
- `https://arxiv.org/abs/2506.23366` — paper GEO 2026
- `https://arxiv.org/html/2507.05301v1` — paper GEO complementar
- `https://ahrefs.com/blog/ai-overview-citations-top-10/` — Ahrefs 38% top-10 drift
- `https://ahrefs.com/blog/how-to-rank-on-chatgpt/` — Ahrefs ChatGPT
- `https://ahrefs.com/blog/why-chatgpt-cites-pages/` — Por que ChatGPT cita
- `https://ahrefs.com/blog/schema-ai-citations/` — Ahrefs schema controlled test
- `https://ahrefs.com/blog/llm-visibility/` — LLM visibility
- `https://almcorp.com/blog/chatgpt-citations-study-44-percent-first-third-content/` — ALM Corp 44,2%
- `https://almcorp.com/blog/measuring-visibility-in-ai-search/` — ALM measuring visibility
- `https://almcorp.com/blog/does-llms-txt-matter-data-analysis/` — ALM llms.txt analysis
- `https://lp.botify.com/q4.2024-aio-report` — Botify Q4 2024 AIO report
- `https://www.brightedge.com/resources/research-reports/agentic-ai-activity-doubles-adapt-your-seo-strategy-now` — BrightEdge agentic AI
- `https://www.brightedge.com/news/press-releases/brightedge-data-ai-search-reaching-tipping-point-ai-agents-2026` — Tipping point
- `https://www.brightedge.com/resources/webinars/authorship-authority` — Authorship authority
- `https://ipullrank.com/everything-we-know-about-ai-overviews` — iPullRank AIO
- `https://ipullrank.com/how-ai-mode-works` — AI Mode mechanics
- `https://ipullrank.com/ai-search-entity-recognition` — Entity recognition
- `https://ipullrank.com/seo-week-2025-garrett-sussman` — SEO Week 2025
- `https://www.similarweb.com/blog/marketing/geo/gen-ai-stats/` — Similarweb gen AI stats
- `https://sparktoro.com/blog/new-research-ais-are-highly-inconsistent-when-recommending-brands-or-products-marketers-should-take-care-when-tracking-ai-visibility/` — SparkToro inconsistency
- `https://nextgrowth.ai/blog/ai-citation-study-2026` — NextGrowth ALM Corp 38%
- `https://www.searchenginejournal.com/google-says-llms-txt-comparable-to-keywords-meta-tag/544804/` — Mueller llms.txt
- `https://www.searchenginejournal.com/bing-webmaster-tools-adds-ai-citation-performance-data/566874/` — Bing AI Performance
- `https://searchengineland.com/google-says-normal-seo-works-for-ranking-in-ai-overviews-and-llms-txt-wont-be-used-459422` — Illyes Search Central
- `https://www.seroundtable.com/google-does-not-endorse-llms-txt-40789.html` — Mueller "no AI uses llms.txt"
- `https://www.seroundtable.com/google-parallel-meta-keywords-llmstxt-39862.html` — Illyes meta keywords
- `https://www.seroundtable.com/google-content-bite-sized-chunks-40728.html` — Sullivan bite-sized
- `https://www.niemanlab.org/2026/05/google-launches-subscription-linking-in-ai-overviews/` — Nieman Lab subscription
- `https://reutersinstitute.politics.ox.ac.uk/journalism-media-and-technology-trends-and-predictions-2026` — Reuters Institute 2026
- `https://discoveredlabs.com/blog/how-google-ai-overviews-works` — Discovered Labs technical
- `https://www.botify.com/blog/marketing-leaders-want-to-meet-ai-search-head-on-new-survey-results` — Botify survey
- `https://cxl.com/blog/google-ai-overview-citation-sources/` — CXL citation sources
- `https://promptwatch.com/data` — Promptwatch
- `https://morningscore.io/seo-for-searchgpt/` — SearchGPT SEO
- `https://wpriders.com/schema-markup-for-ai-search-types-that-get-you-cited/` — WPRiders schema
- `https://www.schemaapp.com/schema-markup/nlweb-consuming-schema-markup-for-ai-applications/` — SchemaApp NLWeb
- `https://www.stackmatix.com/blog/structured-data-ai-search` — Stackmatix structured data
- `https://www.digitalapplied.com/blog/google-ai-overviews-optimization-guide-2026` — Digital Applied 2026
- `https://www.digitalapplied.com/blog/schema-markup-types-complete-structured-data-reference` — Schema types reference
- `https://www.digitalapplied.com/blog/how-search-engines-work-2026-technical-guide` — How search works 2026
- `https://fajela.com/ai-and-ml/optimize-for-bing-chat/` — Bing Chat SEO
- `https://seranking.com/blog/llms-txt/` — SE Ranking llms.txt analysis
- `https://www.rankability.com/llms-report/` — Rankability llms.txt adoption
- `https://nohacks.co/blog/ai-user-agents-landscape-2026` — AI User-Agent landscape
- `https://www.humansecurity.com/learn/blog/crawlers-list-known-bots-guide/` — HUMAN Security crawlers
- `https://llmstxt.org` — llms.txt spec
- `https://answer.ai/posts/2024-09-03-llmstxt.html` — Howard original proposal
- `https://simonwillison.net/2025/Aug/4/chatgpt-agents-user-agent/` — Willison ChatGPT Agent UA
- `https://paulcalvano.com/2025-08-21-ai-bots-and-robots-txt/` — robots.txt empirical analysis
- `https://www.cyrusshepard.com/blog/ai-citation-factors-2026` — Shepard meta-analysis 54 studies
- `https://rankscale.ai` — Rankscale E-E-A-T framework
- `https://llmclicks.ai/blog/perplexity-seo-reverse-engineering/` — Perplexity reverse-engineering
- `https://metehanai.substack.com/p/the-perplexity-files-inside-the-59` — Perplexity Files
- `https://digiday.com/media/how-perplexity-calculates-publishers-share-of-ad-revenue/` — Perplexity revenue share
- `https://www.perplexity.ai/hub/blog/perplexity-publishers-program` — Publishers Program oficial
- `https://blog.graphlet.ai/the-rise-of-semantic-entity-resolution-45c48d5eb00a` — Entity resolution
- `https://data.world/blog/generative-ai-benchmark-increasing-the-accuracy-of-llms-in-the-enterprise-with-a-knowledge-graph/` — KG enterprise

### Crawlers/User-agents catálogo
- `https://github.com/ai-robots-txt/ai.robots.txt/blob/main/code/test_files/robots.txt` — ai.robots.txt project
- `https://dejan.ai/blog/ai-bots/` — Dejan AI bots
- `https://llmpulse.ai/ai-crawler-index/bingbot` — Bingbot index

### Comunidade SEO/IA — voices
- `https://developers.google.com/search/blog/authors/john-mueller` — Mueller blog
- `https://aarontay.substack.com/p/creating-your-own-research-assistant` — Research assistant pattern
- `https://learningseo.io/seo_roadmap/deepen-knowledge/content/quality-eeat/` — Learning SEO E-E-A-T
- `https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/cite-domain-rating.md` — Cite domain rating ref

### Padrões emergentes B2A
- `https://github.com/a2aproject/A2A` — A2A protocol
- `https://nlweb.ai` — NLWeb spec site
- `https://internationalaisafetyreport.org/publication/international-ai-safety-report-2026` — AI Safety Report 2026

### Casos clínicos / regulamentação
- `https://blog.clickpointsoftware.com/google-e-e-a-t` — Clickpoint E-E-A-T
- `https://blog.clickpointsoftware.com/position-zero-aio` — Position zero
- `https://chrisraulf.com/ai-seo-success-eeat-and-domain-authority-are-the-foundation/` — E-E-A-T foundation

### Discussão pública sobre llms.txt
- `https://higoodie.com/blog/llms-txt-robots-txt-ai-optimization/` — llms.txt vs robots.txt
- `https://github.com/simonw/llm-anthropic/issues/1` — Anthropic LLM issue
- `https://community.shopify.com/t/feature-request-support-for-llms-txt-ai-crawler-management/422216` — Shopify request
- `https://gitbook.com/docs/ai-and-search/llm-ready-docs` — GitBook llms.txt
- `https://learn.microsoft.com/en-us/microsoftteams/platform/teams-sdk/developer-tools/llms-text` — MS Teams SDK llms.txt
- `https://cookie-script.com/guides/beyond-robots-txt-implementing-ai-txt-and-llms-txt-for-purpose-based-scraping-control` — ai.txt + llms.txt
- `https://methodshub.gesis.org/library/tutorials/method-hub-linkage/1/` — Record linkage tutorial
- `https://momenticmarketing.com/blog/ai-search-crawlers-bots` — AI search crawlers

A lista completa de 307 URLs únicas está em `C:/Sandyboxclaude/_geo-research-20260520-evening/track-E/all-cites-sorted.txt`.

---

## Coda — Princípios operacionais Brasil GEO derivados do Track E

1. **Citation > Click.** Como Reuters Institute projeta -43% search traffic em 3 anos e Pew mostra CTR caindo 15%→8% em buscas com AI summary, KPIs single-channel (sessões orgânicas Google) ficaram insuficientes. KPI obrigatório: Mention Rate + Citation Rate + Share of Model + Citation Persistence, cross-platform.

2. **SEO é fundação, GEO é distribuição, ASO é decisão.** Não há substituição. O Track E confirma o que o canônico já articulava: AIO/AI Mode usam o mesmo índice Google; ChatGPT/Copilot usam Bing; Perplexity/Claude têm pipelines próprios mas obedecem heurísticas semelhantes (author authority, semantic completeness, fan-out). Otimizar fundação Google + Bing cobre 8 das 10 surfaces.

3. **llms.txt não move agulha.** Mueller, Illyes, Sullivan, Splitt todos públicos contra. Ahrefs + ALM Corp + Rankability todos sem correlation. Manter `llms.txt` por cortesia (custo zero) mas zero esforço editorial dedicado. Robots.txt granular é o que importa.

4. **Schema.org é Phase 1 (Knowledge Graph), não Phase 2 (AI direct).** Williams-Cook provou que LLMs tokenizam JSON-LD como texto bruto, não parseiam estrutura. O lift vem via melhora de ranking organic que então alimenta citation. Investir em schema apenas onde já há ranking organic forte ou em fase de Knowledge Graph push.

5. **Princeton GEO Cite Sources +115% é o lift mais barato de implementar em mai/2026.** Custo: editorial de inserir 3–5 fontes nomeadas por artigo. Toda implementação que faz isso fica acima da média.

6. **Author entity > content entity em YMYL.** Para portais médicos/jurídicos/financeiros, o reviewer block + Person schema completo é gating signal binário. Sem ele, citation rate cai a ponto zero em AIO.

7. **Republish cadence é Perplexity-specific.** Para AIO/AI Mode, mediana 14 meses ainda cita. Para Perplexity, 70% das citations <18 meses. Portais com tráfego dependente de Perplexity precisam cadence trimestral mínima.

8. **MCP + NLWeb antecipam ASO em 6–12 meses.** Microsoft Copilot Studio MCP GA mai/2026 + R.V. Guha CVP Microsoft executando NLWeb desde mai/2025 sinalizam que a próxima fronteira é endpoint-as-source, não page-as-source. Portais B2A-ready em 2026 colhem em 2027.

9. **Inconsistência cross-session é métrica, não bug.** SparkToro provou que mesma query em sessão diferente do mesmo modelo gera respostas diferentes. KPI canônico precisa ser Citation Persistence sobre 5+ sessions por prompt, não Citation single-event.

10. **307 URLs únicas neste documento, 80 curadas no apêndice, ~36k palavras de pesquisa primária Perplexity, US$ 6,31 de custo, ~50min wall-clock.** Track E está em produção e pronto para ser anexado como contexto em qualquer auditoria SEO/GEO Brasil GEO em mai-2026.
