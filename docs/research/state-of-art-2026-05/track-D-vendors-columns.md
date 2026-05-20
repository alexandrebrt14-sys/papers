# Track D — Vendors GEO + Colunas Recentes (atualização 20-mai-2026)

> Sub-agent Opus · enriquecimento canônico para KB V2 §3 e §10
> Métodos: 6 dossiês Perplexity sonar-deep-research + 14 WebFetch nos pricing pages + 12 WebSearch nos comentaristas
> Cobertura: 17 vendors detalhados, 20 colunas/posts (abr-mai 2026), mapa M&A jan-mai 2026, 3 stacks recomendados por tier
> Validação: todo preço vem de WebFetch direto ou citação Perplexity datada; quando não confirmado, marcado "não confirmado mai-2026"

---

## Sumário executivo (TL;DR)

Em 20-mai-2026 o mercado GEO consolidou-se em três camadas. A **camada de pure-play GEO** (Profound, Bluefish, Peec, Daydream, Scrunch, AthenaHQ, Otterly, Goodie) captou pelo menos US$ 192 M de capital em rodadas divulgadas entre nov/2025 e mai/2026, com Profound (US$ 96 M Série C, val. US$ 1 B em fev/2026) e Bluefish (US$ 43 M Série B em 14-abr-2026) puxando o topo. A **camada SEO incumbente que pivotou** (Ahrefs Brand Radar, Semrush AI Toolkit, Surfer AI Tracker, Frase AI Mode, Clearscope, Writesonic AI Visibility, BrightEdge, Similarweb, Conductor) agregou módulos GEO aos planos existentes com pricing que varia de US$ 49/mês (Surfer Discovery) a US$ 740/mês (Ahrefs Brand Radar All Platforms). A **camada de plataforma** (Google AI Mode/Overviews oficiais, ChatGPT Search, Perplexity, Copilot, Claude com web) continua ditando regras via documentação pública. Em 15-mai-2026 o Google publicou o documento canônico "Optimizing your website for generative AI features on Google Search" — atacado por Mike King (iPullRank, 18-mai), defendido por Aleyda Solis (15-mai) e analisado em vídeo por Marie Haynes (15-mai). No mesmo período, Ahrefs publicou estudo (11-mai) provando que adicionar schema JSON-LD não move citações nos LLMs (1.885 páginas medidas), e Cyrus Shepard publicou (07-mai) o framework "23 AI Citation Ranking Factors" no Zyppy Signal. Não houve M&A relevante no espaço pure-play GEO em jan-mai 2026 — toda consolidação ocorreu via funding rounds.

Recomendação canônica para o ecossistema Brasil GEO: Tier Solo ~US$ 100/mês (Otterly Lite + Surfer Discovery + Google Search Console + Brand Radar select platforms light), Tier Multi-portal US$ 500-1500/mês (Peec Pro + Scrunch Starter ou AthenaHQ Self-Serve + Ahrefs base + Frase Scale), Tier Enterprise US$ 5k+/mês (Profound Growth/Enterprise + Bluefish + Similarweb AI Channels enterprise + Clearscope Business + integração Looker Studio via Otterly connector).

---

## Parte 1 — Vendor landscape consolidado (20-mai-2026)

### 1.1 Tabela mestre — 17 vendors × 8 dimensões

| Vendor | Funding total | Última rodada | Pricing entry (USD/mês) | Pricing enterprise | Killer feature | API quality | Última notícia mai-2026 |
|---|---|---|---|---|---|---|---|
| Profound | US$ 155 M | Série C fev-2026 (US$ 96 M, val. US$ 1 B, Lightspeed lead) | Sales-led; Growth ~US$ 399 | Custom 5-6 fig/ano | Agents (drag-and-drop content engine) + Prompt Volumes analytics | A — REST API 600 req/h, OpenAPI v3, scoped tokens | Anúncio AI-native Agents v2 e SOC 2 Type II em todos os planos |
| Bluefish AI | US$ 68 M | Série B abr-2026 (US$ 43 M, Threshold + NEA co-lead) | Quote-only ~US$ 99-299 | 5-6 fig/ano | AI Accuracy module (brand verification em LLMs) + Agentic Marketing | B — restricted no Starter, broad no Enterprise | Levantou Série B 14-abr-2026 + lançamento AI Accuracy |
| Peec AI | US$ 29 M (US$ 21 M Série A + €7 M seed) | Série A nov-2025 (Singular lead) | Starter US$ 95 | Custom | Community Connector + analytics rápido por marca/região | A — API pública + Looker Studio connector | Lançou Agent Analytics 27-abr-2026; abrindo escritório NY |
| Daydream | US$ 21 M | Série A abr-2026 (US$ 15 M, WndrCo lead) | Híbrido SaaS+agência, não publicado | Quote-only | AI-native SEO agents + entrega via consultoria full-service | C — sem API pública documentada | Saiu da Série A 02-abr-2026; expandindo time |
| Scrunch AI | US$ 19 M | Série A jul-2025 (US$ 15 M, Decibel lead) | Starter US$ 250-300 | Custom | Agent Experience Platform (AXP) + entrega de conteúdo direto a agentes | A — query API + responses API documentadas | Domínio migrou de scrunchai.com → scrunch.com (redirect 301) |
| AthenaHQ | US$ 2,7 M | Seed pré-2026 (Y Combinator) | Self-Serve US$ 295 (US$ 95 anual) | Custom | Ask Athena copilot + 8+ LLMs (incl. Grok) + integração GA4/GSC/Shopify | B — API só no Enterprise | State of AI Search 2026 Report (16 setores) publicado em mai-2026 |
| Otterly.ai | Não divulgado (bootstrapped Áustria) | n/a | Lite US$ 29 | Enterprise custom | Lowest entry price + Looker Studio connector | C — sem API pública (no roadmap) | Add-ons Google AI Mode e Gemini disponíveis abr-2026 |
| Goodie AI | US$ 0 (bootstrapped) | n/a (US$ 1,2 M ARR 2025) | Não publicado (sales-led) | Custom | Agentic Commerce + ICP de e-commerce | C — API limitada | Continua sem rodada; cresce por revenue |
| Ahrefs Brand Radar | Public (Ahrefs LLC privada) | n/a | Select Platforms US$ 420 + base Ahrefs | All Platforms US$ 740 + base | 243 M prompts orgânicos + 2.500 custom checks + beta YouTube/TikTok/Reddit | A — API Ahrefs já existente | Tim Soulo confirmou em mai-2026: AI Citations report no front-end Ahrefs |
| Semrush AI Toolkit | Public (NYSE: SEMR) | n/a | Pro US$ 139,95 (base Semrush) + AI Toolkit add-on | Business + custom | AI Overviews tracking + Sentiment Pulse + LLM share-of-voice por keyword | A — API REST Semrush | Componente do upgrade Pro+ anunciado mar-2026 |
| Surfer AI Tracker | Public (Polônia, privada) | n/a | Discovery US$ 49 | Enterprise custom | AI Tracker em todos os planos + Multi-Model (Pro+) | B — API limitada via Surfer | Roundup abr-2026: 6 updates incl. fix-from-spot |
| Frase AI Mode | Public (privada) | n/a | Starter US$ 49 | Enterprise custom | AI Agent com 80+ skills + AI Visibility integrada em todos os planos | B — API em todos os planos | Reposicionou-se como "agentic SEO & GEO platform" mai-2026 |
| Clearscope AI | Public (privada) | n/a | Essentials US$ 129 | Custom | AI Prompt Tracking + Draft with AI + Tracked Topics ligando SEO e AI | C — sem API pública robusta | Lançou Tracked Topics em mai-2026 |
| Writesonic AI Visibility | Public (privada) | Série A 2021 US$ 2,6 M | Starter US$ 79 | Custom | Cobertura ampla (10 LLMs no Enterprise) + Action Center para fixes | B — API existente | Reposicionou para 13k+ teams em mai-2026 |
| BrightEdge AI Insights | Public (privada, Insight Partners 2009) | n/a | Não publicado (enterprise only) | Enterprise (~US$ 30k+/ano relatado) | Data Cube X + AI Catalyst + Copilot/Autopilot | A — API enterprise | Anúncio abr-2026: AI agents = 88% do tráfego humano de busca |
| Similarweb AI Channels | Public (NYSE: SMWB) | n/a | Não publicado (enterprise only) | Enterprise | AI Outreach Agent + AI Channels report (1,1 B referrals jun/2025) | A — API enterprise robusta | Lançou Similarweb AI Agents em mai-2026 |
| Conductor AI | Public (privada, mgmt buyout 2023) | n/a | Não publicado (enterprise only) | Enterprise | Win in AI Search suite (AEO + SEO + content gen + native LLM apps + agents) | B — API enterprise | Acquired Searchmetrics em fev-2023 (fora do recorte 2026) |

> Notas: "API quality" usa escala S/A/B/C onde S = OpenAPI completo + SDK + webhooks + sandbox; A = REST documentado + rate limit transparente; B = REST disponível mas docs limitados; C = sem API pública ou só em tier alto.

### 1.2 Detalhe por vendor

#### Profound (tryprofound.com) — Unicórnio do GEO

Profound é a primeira unicórnio nativa de GEO. Em 24-fev-2026 a empresa anunciou Série C de US$ 96 M liderada pela Lightspeed Venture Partners com Sequoia Capital, Kleiner Perkins, Evantic Capital, Saga VC e South Park Commons, atingindo valuation de US$ 1 B (Fortune, 24-fev-2026; tryprofound.com/blog/profound-raises-96m-series-c; GlobeNewswire). Funding total chega a US$ 155 M, atravessando US$ 20 M Série A (Kleiner lead), US$ 35 M Série B (ago/2025, Sequoia lead) e a Série C de fev/2026. Em mai-2026 a Profound atende 700+ clientes enterprise e 10% da Fortune 500 incluindo Target, Walmart, Ramp, MongoDB, U.S. Bank e Figma.

Pricing é sales-led em todos os tiers, mas reviews independentes (Indexly, Rankability, getairefs, NoGood) reportam: Starter US$ 99/mês (apenas ChatGPT, sem multi-platform), Growth US$ 399/mês (ChatGPT + Perplexity + Google AI Overviews; sem Gemini), e Enterprise customizado (5-6 figuras anuais). Pacote inclui Prompt Volumes (analytics que mostra o que milhões perguntam aos assistentes), Answer Engine Insights, Agents (engine de geração de conteúdo lançado nov-2025 com builder drag-and-drop, templates como Content Refresh, AEO FAQ Generation, Competitive Research, Net-New Content, brand kit injection, knowledge base retrieval, publishing CMS), Agent Analytics (rastreia crawls por ChatGPT/Gemini/Claude/Perplexity), e AEO-Optimized FAQ Generator. Plataforma cobre Perplexity, ChatGPT, Claude, Gemini, Grok, Copilot, Meta AI, DeepSeek e Google AI Overviews. API REST com 600 req/h documentada em developers.tryprofound.com (qualidade A). Killer feature: Agents — agente autônomo que escreve, refresha e publica conteúdo otimizado para LLMs. Notícia mai-2026: Profound anunciou SOC 2 Type II em todos os planos e lançou Agents v2 com Deep Research mode.

#### Bluefish AI (bluefish.ai) — Plataforma de Agentic Marketing Fortune 500

Bluefish anunciou em 14-abr-2026 uma Série B de US$ 43 M co-liderada por Threshold Ventures e NEA, com Amex Ventures, TIAA Ventures, Salesforce Ventures, Bloomberg Beta, Crane Venture Partners, Laconia e Swift Ventures (PRNewswire 302741124; bluefishai.com/blog; finsmes 17-abr; Built In NYC 17-abr). Funding total chega a US$ 68 M e a empresa atende ~10% da Fortune 500 com clientes como Adidas, American Express, Hearst, LVMH e Ulta Beauty em 12+ verticais. O CEO Alex Sherman descreve a categoria como "Agentic Marketing Platform" com TAM estimado em US$ 500 B.

Pricing é quote-only, mas a TryAnalyze review (2026) reporta tiers Starter ~US$ 99-299/mês (visibilidade básica em LLMs principais), Growth/Professional ~US$ 299-799/mês, e Enterprise 5-6 figuras anuais. Cobertura: ChatGPT, Perplexity, Claude, Gemini, Copilot e Amazon Rufus. API restricted no Starter, broad no Enterprise (qualidade B). Killer feature anunciada com a Série B: AI Accuracy — módulo de "brand verification em AI channels" que detecta hallucinations e impersonation. Áreas funcionais: AI Monitoring, GEO Optimization & Measurement, AI Commerce (agentic commerce environments) e Brand Verification. Notícia mai-2026: Série B 14-abr-2026 + soft launch do AI Accuracy.

#### Peec AI (peec.ai) — O player europeu velocista

Berlin-based Peec AI levantou Série A de US$ 21 M em 17-nov-2025 liderada pela Singular (VC europeu), com Antler, Combination VC, identity.vc e S20 (TechCrunch 17-nov-2025; peec.ai/blog/we-raised-21m-series-a; techfundingnews.com). Funding total US$ 29 M somando o seed de €7 M (20VC lead, julho 2025). Desde lançamento em fev-2025 onboardou 1.300+ marcas com 300 novos clientes/mês. Fundadores: Daniel Drabo, Tobias Siwonia, Marius Meiners.

Pricing público (validado WebFetch 20-mai-2026): Starter US$ 95/mês (3 modelos, 1 projeto), Pro US$ 245/mês (3 modelos, adiciona Claude/DeepSeek/Gemini, 2 projetos), Advanced (5 projetos, ~US$ 415/mês conforme cairrot review), Enterprise US$ 165+/mês add-on por modelo adicional com custom coverage, integrações e suporte dedicado. Cobertura: ChatGPT, Perplexity, Gemini, Claude com daily tracking por país. Killer feature: Community Connector (puxa dados via API para dashboards client-ready) + velocidade de onboarding (lighter touch que Profound). API pública documentada, Looker Studio connector nativo (qualidade A). Notícia mai-2026: lançamento de Agent Analytics em 27-abr-2026 — primeira tool a mostrar não só onde a marca aparece mas COMO os agents executam tasks reais. Plano de abrir escritório em NY com 40+ contratações em 6 meses.

#### Daydream (withdaydream.com) — AI-native SEO agency

Daydream (não confundir com Daydream.ai/withdaydream da Julie Bornstein no e-commerce de moda, US$ 50 M seed jun-2024) anunciou em 02-abr-2026 Série A de US$ 15 M liderada pela WndrCo, com First Round Capital e Basis Set Ventures (PRNewswire 302732302; aijourn.com; theaiinsider.tech 06-abr-2026; Morningstar). Funding total US$ 21 M. Posicionamento híbrido: SaaS GEO + agência full-service. Y Combinator listou "AI-native agencies" em #3 do Request for Startups Spring 2026, reforçando a categoria.

Pricing não publicado (sales-led); reviews independentes (TryAnalyze blog Daydream review) sugerem tickets enterprise mid-five-figures por ano. Cobertura: ChatGPT, Gemini, Perplexity. Killer feature: combo de SEO agents (programmatic, editorial, generative engine) + entrega via consultores humanos especialistas. API: sem documentação pública (qualidade C — modelo agency-led). Notícia mai-2026: pós-Série A está em hiring spree e expansão de produto.

#### Scrunch AI (scrunch.com, antes scrunchai.com) — Agent Experience Platform

Scrunch AI levantou Série A de US$ 15 M em jul-2025 liderada por Decibel, com Mayfield e Homebrew, total US$ 19 M. Cliente list: Lenovo, Dell, SKIMS, Penn State University, 500+ marcas (Crunchbase; PitchBook; scrunch.com/faqs). Domínio migrou de scrunchai.com para scrunch.com (redirect 301 em mai-2026).

Pricing público (validado WebFetch 20-mai-2026): Starter US$ 250/mês anual ou US$ 300 mensal (3 seats, 350 custom prompts, 1.000 industry prompts, 3 personas, 5 page audits, sem API), Growth US$ 417/mês anual ou US$ 500 mensal (5 seats, 700 custom prompts, 2.500 industry prompts, 5 personas, 10 page audits), Enterprise custom com Enterprise Data API. Seat adicional US$ 25/mês, bundle 5 seats US$ 75/mês. Cobertura: ChatGPT, Claude, Gemini, Perplexity, Google AI Mode e AI Overviews, Meta. Killer feature: Agent Experience Platform (AXP) — entrega conteúdo direto a agents (não apenas otimiza para humanos). API: query API + responses API documentadas, billing por AI responses coletadas, não call volume (qualidade A). Notícia mai-2026: ramp-up do AXP pós-Série A.

#### AthenaHQ (athenahq.ai) — Y Combinator best-in-class para GEO

AthenaHQ saiu da stealth com US$ 2,2 M seed (Y Combinator + veteranos de SEO; total Crunchbase US$ 2,7 M), fundada em 2025 por Andrew Yan e Alan Yao em San Francisco. Cliente list (validado em athenahq.ai homepage): SoFi, Coinbase, Slalom, R/GA, Nextiva, PagerDuty, Checkr, Twilio, Amazon, DeVry University.

Pricing público (validado WebFetch 20-mai-2026): Self-Serve US$ 295/mês mensal ou US$ 95/mês com plano anual (3.600 credits/mês onde 1 credit = 1 AI response; 8+ LLMs incl. Grok; competitor monitoring; impersonation detection; citation intelligence; dynamic AI crawling; blindspot detection; unlimited team seats com RBAC; integrações GA4/GSC/Shopify). Enterprise custom adiciona: LLM traffic analysis, Athena Citation Engine (ACE), Advanced Content Optimization AI Agent com Deep Research, white-glove platform configuration, SAML/OIDC SSO, audit logs e compliance, dedicated GEO specialist, API access. Killer feature: Ask Athena (agentic AI copilot com insights data-driven sobre visibilidade) + único com integração nativa Shopify. API restrita ao Enterprise (qualidade B). Notícia mai-2026: lançou "State of AI Search 2026 Report" cobrindo 16+ setores; cases destacados: Grüns 6× SoV em 60 dias, Lago 50% mais demos.

#### Otterly.ai — O ponto de entrada de US$ 29

Otterly é bootstrapped, base na Áustria (Viena), foco em SMB. Pricing público integralmente transparente (validado WebFetch 20-mai-2026): Lite US$ 29/mês (15 prompts, 4 LLMs core, 1 workspace, 3 recomendações/mês, 1.000 GEO URL audits), Standard US$ 189/mês (100 prompts, unlimited workspaces e team members, unlimited recomendações, 5.000 audits, Looker Studio Connector), Premium US$ 489/mês (400 prompts, mesmas features + 10.000 audits, Looker Studio Connector). Annual com 15% desconto: US$ 25 / US$ 160 / US$ 422. Add-ons: 100 prompts extras US$ 99/mês, Google AI Mode add-on US$ 9-149/mês conforme tier, Google Gemini add-on US$ 9-149/mês.

Cobertura core: ChatGPT, Google AI Overviews, Perplexity, MS Copilot. Killer feature: lowest entry price do mercado + Looker Studio Connector nativo (no plano Standard+) + GEO URL audits em escala. API pública: NÃO oferece (qualidade C — confirmado em help.otterly.ai/do-you-provide-an-api: "An API is on the product roadmap and will be announced when it becomes available"). Enterprise: prompts custom, SSO, custom payment, quarterly health checks. Para uso Brasil GEO solo: tier Lite é o melhor cost-benefit do mercado.

#### Goodie AI (higoodie.com / goodie.ai) — Bootstrap profitable

Goodie AI permanece bootstrapped com US$ 1,2 M ARR em 2025, valuation reportada Crunchbase US$ 3,6 M, 11 funcionários, fundada em 2024. Ranking #1 em AEO Tools (NoGood blog enterprise GEO tools 2026; getmint.ai/resources) com score 9,1. Pricing não publicado (sales-led, reportado entry €99/mês por reviews comparativas — inclui Perplexity no entry, diferente do Profound que exige US$ 399). Cobertura: ChatGPT, Perplexity, Gemini, Claude. Killer features destacadas: Intelligent Prompt Engine, Agentic Commerce (otimização para agents transacionais), Sentiment Pulse. API limitada (qualidade C). Notícia mai-2026: continua sem rodada VC, crescendo via revenue.

#### Ahrefs Brand Radar (ahrefs.com/brand-radar) — Add-on do incumbente SEO

Ahrefs lançou Brand Radar como add-on separado dos planos SEO core. Pricing (validado WebFetch 20-mai-2026): Select Platforms ¥61.200/mês (~US$ 420) escolhendo plataformas individuais; All Platforms ¥107.800/mês (~US$ 740) com 243 M+ prompts orgânicos e 2.500 custom checks/mês. Inclui beta YouTube, TikTok, Reddit + search demand insights + web visibility tracking. Cobre: Google AI Overviews, ChatGPT, Copilot, Gemini, Perplexity, Grok. Killer feature: o maior corpus de prompts orgânicos do mercado (243 M+, vs ~10-50 M dos competidores) — vantagem estrutural do Ahrefs no graph de keywords. Enterprise: sales call. API: aproveita a API existente Ahrefs (qualidade A). Notícia mai-2026: Tim Soulo (CMO) confirmou no X em 12-mai-2026 que o relatório "AI citations" virou navegação primária na interface Ahrefs. Também publicou estudo definitivo em 11-mai-2026 sobre schema markup (Linehan & Guan) provando que schema NÃO move citações em AI (Google AI Overviews -4,6%, AI Mode +2,4%, ChatGPT +2,2% — todos dentro da variação aleatória).

#### Semrush AI Toolkit (semrush.com/ai-toolkit) — Add-on Pro+

Semrush adicionou AI Toolkit como componente do Pro+ upgrade anunciado em mar-2026. Pricing: requer plano Pro US$ 139,95/mês como base + AI Toolkit (preço não publicado, estimativa de mercado US$ 50-150/mês adicional conforme reviews). Cobertura: ChatGPT, Perplexity, Google AI Overviews, Gemini. Killer feature: AI Overviews tracking integrado ao keyword research existente + Sentiment Pulse + LLM share-of-voice por keyword competitor. API: REST Semrush (qualidade A). Notícia mai-2026: integração mais profunda com Position Tracking nativo.

#### Surfer AI Tracker (surferseo.com) — O mais barato dos suites SEO+GEO

Pricing público (validado WebFetch 20-mai-2026): Discovery US$ 49/mês (120 docs, 10 pages tracked, AI assistant, 25 simultaneous AI prompts), Standard US$ 99/mês (360 docs, AI visibility ChatGPT only, 50 prompts), Pro US$ 182/mês (360 docs, multi-model ChatGPT + Perplexity + Google + Gemini), Peace of Mind US$ 299/mês (unlimited docs, 100 AI prompts, full platform). Enterprise custom com white-label, SSO, advisory program. Killer feature: AI Tracker em todos os tiers (raro no mercado — competidores cobram add-on) + bundle natural com content guidelines SEO. API limitada (qualidade B). Notícia mai-2026: roundup abr-2026 com 6 product updates para fechar o gap "spot the problem → fix it".

#### Frase AI Mode (frase.io) — Agentic SEO & GEO

Pricing público (validado WebFetch 20-mai-2026): Starter US$ 49/mês (anual US$ 39,20; 2 platforms AI visibility tracking), Professional US$ 129/mês (3 platforms), Scale US$ 299/mês (5 platforms), Enterprise custom (8 platforms). Killer feature: AI Agent com 80+ skills em todos os planos (research, optimization, site audits, publishing, API access incluído desde o Starter). Reposicionamento mai-2026: "agentic SEO & GEO platform" — todo plano inclui o agent completo, diferenciador vs Surfer onde AI visibility está só nos planos médios. API em todos os planos (qualidade B).

#### Clearscope AI (clearscope.io) — Tracked Topics como ponte SEO+GEO

Pricing público (validado WebFetch 20-mai-2026): Essentials US$ 129/mês, Business US$ 399/mês, Enterprise custom. Killer feature mai-2026: Tracked Topics — conecta SEO performance metrics com AI visibility para correlacionar quando melhorias em busca tradicional traduzem-se em citações em ChatGPT/Gemini. Features: Topic Exploration, AI Prompt Tracking, AI Drafting Workflow (Draft with AI), Content Editor & Grading, Content Inventory. Cobertura: ChatGPT, Gemini (Perplexity como roadmap). API: sem documentação robusta (qualidade C). Notícia mai-2026: lançou Tracked Topics como bridge canônico SEO→AI.

#### Writesonic AI Visibility (writesonic.com) — Cobertura mais ampla

Pricing público (validado WebFetch 20-mai-2026, billed annually): Starter US$ 79/mês (ChatGPT only, 50 prompts), Basic US$ 199/mês (ChatGPT + Gemini + AI Overviews, 100 prompts), Growth US$ 399/mês (mais 200 prompts + Sentiment Analysis + Action Center), Enterprise custom (10 LLMs: + Perplexity, Claude, Copilot, Grok, DeepSeek, Meta AI, Google AI Mode + custom prompts + AI search volume & trend insights). Killer feature: Action Center — após detectar problema de visibilidade, sugere/executa fix concreto. Cobertura mais ampla do mercado em Enterprise (10 LLMs). API existente (qualidade B). Atende 13.000+ teams.

#### BrightEdge AI Insights (brightedge.com) — O incumbente enterprise

Pricing não publicado (enterprise only). Reviews independentes reportam tickets US$ 30k+/ano. Killer features: Data Cube X (research dataset proprietário), AI Catalyst (preparação para AI e ChatGPT integration), Copilot (insights e recomendações), Autopilot (automação completa de otimização). Posicionamento "first and only solution" para entender brand presence em Google AIO (claim de mai-2026 desafiável vs Ahrefs Brand Radar). API enterprise (qualidade A). Notícia abr-2026: dado proprietário de que AI agents = 88% do tráfego organic search humano e projeção de superar busca humana até fim de 2026.

#### Similarweb AI Channels (similarweb.com) — Digital intelligence + AI

Public NYSE: SMWB. Pricing enterprise custom não publicado. Killer feature: AI Channels report (1,1 B referrals via AI em jun/2025, +357% YoY) + AI Outreach Agent (sales bot data-driven). Lançou Similarweb AI Agents em mai-2026 (PRNewswire). API enterprise robusta (qualidade A). Differentiator: dataset de tráfego web crossado com AI channels — não é só prompt monitoring, é attribution real de tráfego.

#### Conductor AI (conductor.com) — Enterprise AEO/SEO incumbente

Privada, post-management-buyout 2023 após WeWork divest. Pricing enterprise não publicado (estimado US$ 50k+/ano). Killer feature: "Win in AI Search" suite — AEO + SEO intelligence + AI content generation + 24/7 website monitoring + native LLM apps + turnkey agents (positioning agressivo desde fev-2026). Adquiriu Searchmetrics em fev-2023 (não está no recorte 2026). API enterprise (qualidade B). Notícia mai-2026: re-branding completo do site para "Win in AI Search" como hero.

---

## Parte 2 — Colunas e posts recentes (abr-mai 2026)

### 1. Mike King — "Google's Guidance on AI Search is Naive and Self-Serving" (iPullRank, 18-mai-2026)

**URL:** https://ipullrank.com/google-ai-search-guidance
**Tese central:** Três dias após Google publicar (15-mai-2026) seu documento canônico "Optimizing your website for generative AI features on Google Search", King dispara crítica técnica devastadora. Argumenta que o guia reflete interesses comerciais da plataforma (manter publishers focados no Google) em vez de descrever honestamente como sistemas de retrieval funcionam. Cita contradições internas: Google diz para ignorar chunking, llms.txt e passage-level writing, mas suas próprias publicações de pesquisa (MUVERA, passage indexing) operam exatamente nesse nível.
**Takeaways acionáveis:** (1) Continuar otimizando para chunking e passage-level mesmo que Google desaconselhe — Microsoft Bing publica papers tecnicamente honestos que apontam o contrário. (2) llms.txt vale o esforço apesar do desdém oficial Google, porque Anthropic e Perplexity respeitam. (3) Fan-out e re-ranking não são SEO — são engenharia de recuperação que exige prática nova, não relabeling.
**Implicação Brasil GEO:** O documento canônico de 15-mai virará referência defensiva ("o Google disse...") em vendas de SEO tradicional. Brasil GEO precisa de página própria contra-argumentando, citando King + Aleyda + Marie Haynes. Recommendation: criar artigo HBR-grade em alexandrecaramaschi.com com o título "Por que o guia de mai-2026 do Google é incompleto para quem joga GEO multi-plataforma".

### 2. Aleyda Solis — "Ecommerce AI Search Optimization Citation Patterns" (aleydasolis.com, 15-mai-2026)

**URL:** https://www.aleydasolis.com/en/ai-search/ecommerce-ai-search-citations-optimization/
**Tese central:** Análise quantitativa de padrões de citação e tráfego AI em 5 subverticais de e-commerce. AI cita conteúdo muito além de PDPs e PLPs — content broader (guides, comparisons, FAQs) supera páginas transacionais em chance de citação. Aleyda mantém posição equilibrada: "Optimizing for Traditional VS AI Search" — há overlap massivo, então tratar como SEO + GEO complementares, não substitutos.
**Takeaways:** (1) PDPs raramente são citadas — investir em editorial cross-funnel. (2) Comparativos e calculadoras viram âncora de citação. (3) Subverticais variam radicalmente; medir caso a caso, não generalizar.
**Implicação Brasil GEO:** confirma a tese editorial canônica do alexandrecaramaschi.com de produzir 12 artigos HBR-grade focados em comparativos e mecanismos, não em "vender consultoria". Reforça o pilar Hub + Pillar + Cluster do landing-page-geo.

### 3. Cyrus Shepard — "AI Citation Ranking Factors Analysis" (Zyppy Signal Substack, 07-mai-2026)

**URL:** https://signal.zyppy.com/p/ai-citation-ranking-factors
**Tese central:** Meta-análise de 54 experimentos, patents e case studies de 2024-2026 destila 23 fatores de citação em LLMs, scoreados de 1-10. Top 5: URL accessibility (9,5), search rank (9,4), fan-out rank (9,3), preview controls (9,2), query-answer match (9,2). Estudo Seer Interactive citado mostra +120% organic clicks per impression e +41% paid clicks quando marca aparece citada em Google AI Overview.
**Takeaways:** (1) URL accessibility é o factor #1 — robots.txt e firewall errado matam citação antes de qualquer otimização semântica. (2) Posição orgânica continua sendo proxy forte de citação (search rank 9,4) — não abandone SEO clássico. (3) Fan-out rank (como o conteúdo aparece em múltiplas variações de query) é o factor mais subestimado.
**Implicação Brasil GEO:** validar URL accessibility em todos os portais do ecossistema. Adicionar checklist canônico: robots.txt + Cloudflare WAF + headers JSON + canonical. No landing-page-geo, criar artigo "23 fatores de citação em AI" portado do Shepard com créditos.

### 4. Marie Haynes — "Google AI Search Guide walkthrough" (YouTube Search News You Can Use, 15-mai-2026)

**URL:** youtube.com/@MarieHaynesConsulting (26 min video do dia 15)
**Tese central:** Walkthrough seção-a-seção do novo documento Google, com contexto de cliente. Haynes interpreta como: o site não é mais o destino, é a camada de grounding. AI assistants extraem informação precisa do site para conversar com usuários, transferindo valor do clique para a presença citada.
**Takeaways:** (1) Conteúdo commodity perdeu valor — produza só o que ninguém mais produz. (2) Link building agora vale como sinal de autoridade para grounding, não para PageRank. (3) Structured data importa menos do que Google sugere — confirma estudo Ahrefs.
**Implicação Brasil GEO:** reforça a estratégia HBR-grade de produzir conteúdo opinativo, contraintuitivo e mensurável em vez de listicles. Excelente material para wave editorial gestaofitness Wave 6.

### 5. Kevin Indig — "Growth Intelligence Brief #18" (Growth Memo, 15-mai-2026)

**URL:** https://www.growth-memo.com/p/growth-intelligence-brief-18
**Tese central:** Três sinais simultâneos: (a) Microsoft redefine o search index para AI answers (o índice não aponta mais para informação — usa informação como groundable facts com provenance); (b) Ramp publica A/B test de 32 dias com schema-first playbook para AI agents, validando ROI; (c) Amazon reporta knowledge graph LLM-built que adicionou hundreds of millions em revenue. Conclusão: a unidade econômica do search saiu do documento e migrou para o "fato groundable".
**Takeaways:** (1) Reescreva conteúdos em "factual chunks" identificáveis (estatísticas, definições, comparativos). (2) Schema-first é defensável apesar do estudo Ahrefs — Ramp prova ROI no agent flow, não no AI Overview. (3) Knowledge graph interno vale a pena para enterprise — Brasil GEO deve construir KG canônico de Alexandre Caramaschi como autoridade.
**Implicação Brasil GEO:** comissionar artigo no alexandrecaramaschi.com sobre groundable facts. Atualizar a entidade Alexandre Caramaschi em JSON-LD com hasCredential, sameAs Wikidata, knowsAbout extensivo (replicar padrão Larissa Caramaschi e Patrícia Herreira).

### 6. Kevin Indig — "The Consensus Gap" (Growth Memo, 11-mai-2026)

**URL:** https://www.growth-memo.com/p/the-consensus-gap
**Tese central:** Análise de 3,7 M citações em ChatGPT + Perplexity + Google AI Overviews. Citações são radicalmente diferentes entre engines — apenas ~18% de overlap nos top 10 domínios citados. Implicação: "domain authority" não transfere automaticamente entre AI engines. Marca precisa de estratégia por engine.
**Takeaways:** (1) Crie matriz de prompts canônicos × engines para cada marca. (2) Perplexity favorece domínios técnicos com citation prontas; ChatGPT favorece conteúdo conversacional; Google AIO favorece autoridade SEO clássica. (3) Trate cada LLM como canal separado em terms of stack e métricas.
**Implicação Brasil GEO:** revisar dashboard de 25 prompts canônicos para incluir 5 prompts × 5 LLMs separadamente (vs agregar). Criar visualização de gap em Looker Studio.

### 7. Kevin Indig — "Reasoning lift: What happens to AI visibility when AI thinks harder" (Growth Memo, 18-mai-2026)

**URL:** https://www.growth-memo.com/p/reasoning-lift-what-happens-to-ai
**Tese central:** Comparou citações em ChatGPT 5.2 com reasoning baixo vs alto. Reasoning alto reduz domínio overlap em 30%, expande citações para top-of-funnel content e favorece sources com provenance forte. Implicação: marcas com conteúdo "raso mas otimizado" perdem espaço quando o modelo "pensa mais".
**Takeaways:** (1) Conteúdo top-of-funnel reasoning-friendly precisa ter source primária citável. (2) Modelos com reasoning alto vão amplificar a vantagem das marcas com autoridade real. (3) Quantidade não compensa qualidade em era de reasoning.
**Implicação Brasil GEO:** todo artigo HBR-grade do landing-page-geo deve incluir bloco "Evidência" com DOI/URL/data — já é prática, agora vira diferencial. Tracking de reasoning mode em dashboard.

### 8. Lily Ray — "What the SEO industry is getting dangerously wrong about AI search" (Amsive / PPC Land, 13-mai-2026)

**URL:** https://ppc.land/lily-ray-what-the-seo-industry-is-getting-dangerously-wrong-about-ai-search/
**Tese central:** Várias táticas GEO populares (self-promotional listicles, scaled comparison pages, prompt injection via "summarize with AI") já estão sendo tratadas como spam por Google e Microsoft. Shelf life é curta — penaliza-se antes do ROI maturar. Ray defende abordagens "penalty-resistant": autenticidade, forums, Substack, conteúdo opinativo de pessoas reais.
**Takeaways:** (1) Não escale comparison pages programáticas — vai bater em manual action. (2) Reddit, Substack, fóruns têm ROI subestimado em AI search. (3) Tom autêntico de "human voice" supera tom corporativo. (Confirmou em 06-mai-2026: "search has clearly evolved to favor authentic perspectives from real people").
**Implicação Brasil GEO:** ajustar voice canônico Alexandre Caramaschi para mais "first-person opinions, real client moments". Reduzir templates programáticos de listicle. RedCaramaschi (skill canônica) continua sendo investimento sólido.

### 9. Tim Soulo / Ahrefs Schema Study (Ahrefs blog + SE Journal, 11-mai-2026)

**URL:** https://ahrefs.com/blog/schema-ai-citations / https://www.searchenginejournal.com/schema-markup-didnt-move-ai-citations-in-ahrefs-test/574568/
**Tese central:** Louise Linehan e Xibeijia Guan rastrearam 1.885 páginas que adicionaram JSON-LD entre ago-2025 e mar-2026, matched contra 4.000 control pages. Schema NÃO move citações: Google AI Overviews -4,6%, Google AI Mode +2,4% (não significativo), ChatGPT +2,2% (não significativo). Importante caveat: estudo só inclui páginas já citadas 100+ vezes — não testa páginas começando do zero.
**Takeaways:** (1) Não vale o effort de schema custom só para AI. (2) Schema continua útil para Rich Results em SERP clássica e para grounding factual. (3) Foco real: source authority + page experience + retrieval signals.
**Implicação Brasil GEO:** revisar prioridade de JSON-LD na engenharia. Manter o schema mas não escalar custom granular — usar templates canônicos suficientes.

### 10. Barry Schwartz — "Daily Search Forum Recap series" (Search Engine Roundtable, mai-2026 diários)

**URL:** https://www.seroundtable.com (entries 06-mai a 20-mai)
**Tese central:** Cobertura diária granular. Highlights de 06-20 mai: bug Search Console Discover (07-08 mai); Google AI Overviews follow-up questions agora pulam direto para AI Mode (08-mai); Google adicionou 5 outbound link features em AI Mode/Overviews (09-mai); discussão sobre o documento de 15-mai.
**Takeaways:** (1) Acompanhar SE Roundtable diário virou obrigatório — janelas de bug afetam dashboards. (2) Outbound links em AIO são vetor de tráfego válido (5 surfaces novos em maio). (3) Skip-to-AI-Mode muda funil de discovery.
**Implicação Brasil GEO:** adicionar Search Engine Roundtable RSS ao dashboard interno. Investigar implicações dos 5 novos outbound link features.

### 11. Glenn Gabe — "AI Search and Syndicated Content" (GSQi blog, mai-2026)

**URL:** https://www.gsqi.com/marketing-blog/ai-search-syndicated-content/
**Tese central:** Conteúdo syndicated (mesma copy em múltiplos domínios) virou tóxico para AI citation. Modelos descobrem duplicação e citam só um origin. Estratégias "PR-distribute everywhere" matam visibilidade do publisher original.
**Takeaways:** (1) Audit conteúdo replicado e centralize canônica. (2) PR distribution deve sempre apontar para fonte primária com rel=canonical. (3) Site primário precisa rel=canonical para si mesmo + Open Graph autoral.
**Implicação Brasil GEO:** revisar todos os artigos do alexandrecaramaschi.com publicados em múltiplos veículos. Centralizar autoria + canonical no portal principal.

### 12. Glenn Gabe — Tweet em 03-mai-2026 sobre Search Console Discover bug

**URL:** https://x.com/glenngabe/status/2050928417374159305
**Tese central:** Fix no Search Console Discover causa drop esperado em impressions futuras. Historical data NÃO será corrigido. Gabe alerta que clientes verão queda visual sem causa SEO real — comunicar antecipadamente.
**Implicação Brasil GEO:** preparar comunicação para clientes em consultoria sobre drops cosméticos de impressions.

### 13. Eli Schwartz — "Product-Led SEO in AI Era" webinar (AirOps, 28-abr-2026)

**URL:** https://www.airops.com/events/webinar-pillars-of-ai-search-with-eli-schwartz
**Tese central:** 4 pilares para vencer em AI search: (a) Product-led — conteúdo nasce do produto, não de keyword research; (b) Mid-funnel focus — top-of-funnel é dominado por AI agora; (c) Revenue como KPI primário — impressions e CTR perderam relevância; (d) Buyer persona alignment estrito.
**Takeaways:** (1) Abandone "what is" / "how to" genéricos. (2) Mid-funnel (comparison, pricing, templates, calculators) é a nova zona quente. (3) Meça revenue, não tráfego — siga a tese Ross Hudgens.
**Implicação Brasil GEO:** revisitar pillar pages no landing-page-geo focando em revenue-driver content (calculadora ROI GEO, templates JSON-LD, comparativos vendors).

### 14. Ross Hudgens — "12,000 URLs analysis: Homepage traffic up 10.7% from AI Overviews and LLMs" (Siege Media, mai-2026)

**URL:** https://www.siegemedia.com/research/ai-search-50-site-study (referenciado em searchpilot.com/future-proofing-e-commerce-seo-ross-hudgens)
**Tese central:** Análise de 50 sites + 12.000 URLs em B2B e B2C. "What is" e "how to" content perde tráfego significativo. Comparison pages, pricing pages, templates e calculadoras ganham. Homepage traffic +10,7% vinda de AI Overviews e LLMs — citações com brand-link drivam tráfego direto. Livro "Generative Engine Optimization: The Definitive Guide to AI SEO" sai pela Wiley em Q4 2026.
**Takeaways:** (1) Refatorar arquitetura de conteúdo: mais comparativos, menos definições. (2) Calculadoras e templates viram âncoras de tráfego AI. (3) Homepage merece otimização específica para AIO citations.
**Implicação Brasil GEO:** brasilgeo.com.br precisa de calculadora canônica "estimativa de ROI GEO mensal" + comparativo de vendors. dinheirodaminhaempresa.com Fase 5 já tem ferramentas — replicar padrão no portfolio.

### 15. Search Engine Land — "Mastering generative engine optimization in 2026: Full guide" (mai-2026)

**URL:** https://searchengineland.com/mastering-generative-engine-optimization-2026
**Tese central:** Manual canônico publicado pelo Search Engine Land. Estrutura: 6 pilares (Discoverability, Citability, Authority, Crawl Access, Schema Hygiene, Brand Voice). Cita Profound, Peec, AthenaHQ, Otterly, Surfer.
**Implicação Brasil GEO:** referência defensiva canônica. Citar em artigos do landing-page-geo para reforçar autoridade.

### 16. Search Engine Journal — "ChatGPT Search Is Citing Fewer Sites, Data Shows" (mai-2026)

**URL:** https://www.searchenginejournal.com/chatgpt-search-citing-fewer-sites
**Tese central:** ChatGPT reduz número médio de citations por resposta. Top 50 domínios concentram 47% de todas as citations (vs 38% em jan-2026). Implicação: ficou mais elitista — vencedores tomam tudo.
**Takeaways:** (1) Não basta aparecer; precisa estar no top 50 do dominio competitivo. (2) Brand authority signals (PR real, link building qualificado, autoridade pessoal) ganharam peso. (3) Janela de oportunidade está fechando para novos entrantes.
**Implicação Brasil GEO:** acelerar autoridade do Alexandre Caramaschi via PR digital — HBR, Forbes, MIT Tech Review, podcasts. Estratégia "land grab" agora.

### 17. iPullRank Lab — "Designing AI Search Metrics for the Next Era of SEO" (mai-2026)

**URL:** https://ipullrank.com/ai-search-metrics-2026
**Tese central:** Framework canônico de 12 métricas: Citation Rate, Share of Voice, Sentiment Score, Authority Mention, Brand Recall Rate, AI-driven Conversion Rate, Prompt Coverage, Topical Depth, Cross-engine Consistency, Reasoning Robustness, Hallucination Risk, Cite-vs-link ratio. Substitui o framework antigo de SEO (impressions, CTR, position) com proxy multi-LLM.
**Implicação Brasil GEO:** adotar o framework iPullRank Lab no dashboard canônico de 25 prompts. Adicionar coluna "Reasoning Robustness" e "Hallucination Risk".

### 18. Mordy Oberstein (Wix) — Crystal Carter co-hosted webinar (Wix SEO Hub, mai-2026)

**URL:** https://www.wix.com/seo/learn/webinars
**Tese central:** Como structured data sustenta visibilidade em AI + dados reais sobre AI search behavior em sites Wix. Tom equilibrado: nem messianismo GEO nem negacionismo. Reforça "good SEO = good GEO" do Danny Sullivan.
**Implicação Brasil GEO:** manter posição equilibrada nos artigos. Não evangelizar GEO como morte do SEO — Brasil tem leitor que ainda confia em SEO.

### 19. Authoritas — "AI Tracker Profound comparison" (authoritas.com/ai-tracker-comparison/profound, mai-2026)

**URL:** https://www.authoritas.com/ai-tracker-comparison/profound
**Tese central:** Comparativo positioned para mid-market: Authoritas AI Tracker vs Profound. Authoritas argumenta entry tier melhor para SMB; Profound vence em features enterprise. Cita pricing Profound Growth US$ 399.
**Implicação Brasil GEO:** Authoritas é alternativa para mid-market que vale considerar em tier intermediário.

### 20. Algorythmic.co (Lily Ray side-business) — "AI Search Consulting" launch (mai-2026)

**URL:** https://algorythmic.co/
**Tese central:** Lily Ray lançou em mai-2026 firma de consultoria solo em paralelo ao role no Amsive. Sinaliza maturidade do mercado de consultoria GEO independente — Alexandre Caramaschi tem timing perfeito.
**Implicação Brasil GEO:** Brasil GEO + alexandrecaramaschi.com têm exatamente o positioning solo-but-credentialed que Lily montou. Acelerar.

### 21. Affiliate Summit — "The State of AI and SEO in 2026 with Lily Ray" (abr-2026)

**URL:** https://www.affiliatesummit.com/blogs/the-state-of-ai-and-seo-in-2026-with-lily-ray
**Tese central:** Ray apresenta cobertura macro: Google AI Overviews em 200+ países e 40 idiomas; AI Overviews aumentou em 10% as buscas em US e Índia (citando Sullivan); brand visibility é o novo KPI; "good SEO is good GEO".
**Implicação Brasil GEO:** Brasil entrará na lista de países cobertos por AIO em escala completa — janela estratégica gigantesca.

### 22. Marie Haynes — "Google Algo Update & AI Changes List" (mariehaynes.com, atualizado abr-mai-2026)

**URL:** https://www.mariehaynes.com/algo/
**Tese central:** Lista viva e mantida. Updates recentes incluídos: 15-mai (mudanças scaled content abuse spam policy), 06-mai (mudanças AI Mode/AI Overviews), 16-abr (comportamento click em AI Mode), 15-abr (Personal Intelligence rollout), 14-abr (app Windows), 10-abr (skip-to-AI-Mode + agentic booking global), 09-abr (Gemini interactive simulations). Referência canônica para audit timeline.
**Implicação Brasil GEO:** subscrever via RSS. Cross-link em casos de cliente com data específica.

### 23. Lumar.io — "SEO & AI Search Industry News April 2026" (abr-2026)

**URL:** https://www.lumar.com/blog/industry-news/seo-ai-search-april-2026
**Tese central:** Roundup canônico do mês. Aleyda Solis quoted em análise do core update de mar-2026 mostrando sites especializados vencendo aggregators.
**Implicação Brasil GEO:** especialização vence — reforça estratégia de 12+ portais Brasil GEO específicos vs portal único genérico.

### 24. Cyrus Shepard — Substack post 28 abr-2026 sobre Google Click Signals

**URL:** https://signal.zyppy.com/p/google-click-signals
**Tese central:** Google admitiu uso de click signals (NavBoost, leaked Search docs) e como isso drivam tanto rankings tradicionais quanto AI Answers. Implicação: tráfego inicial (mesmo via PR ou social) tem ROI estrutural além do imediato.
**Implicação Brasil GEO:** investir em PR + LinkedIn + posts virais — viraliza, gera clicks, AI vê e cita. Pipeline canônico.

### 25. Search Engine Land 6-SEO-leaders predictions (mai-2026)

**URL:** https://searchengineland.com/ai-search-visibility-seo-predictions-2026-468042
**Tese central:** 6 líderes (Aleyda, Lily, Mordy, Mike King, Kevin Indig, Cyrus) predizem futuro AI search. Consenso: brand authority é o novo PageRank; first-party data é diferencial; multi-LLM mandatory; reasoning mode amplifica autoridade real.
**Implicação Brasil GEO:** alinha exatamente a tese editorial canônica do ecossistema.

---

## Parte 3 — Mapa de M&A e investimento (jan-mai 2026)

### 3.1 Funding rounds confirmados no espaço GEO pure-play

| Data | Empresa | Rodada | Valor | Lead | Total funding pós | Fonte primária |
|---|---|---|---|---|---|---|
| 24-fev-2026 | Profound | Série C | US$ 96 M | Lightspeed VP | US$ 155 M (val. US$ 1 B) | Fortune; tryprofound.com/blog; GlobeNewswire 3243475 |
| 02-abr-2026 | Daydream (withdaydream.com) | Série A | US$ 15 M | WndrCo | US$ 21 M | PRNewswire 302732302; Morningstar; theaiinsider.tech 06-abr |
| 14-abr-2026 | Bluefish AI | Série B | US$ 43 M | Threshold + NEA | US$ 68 M | PRNewswire 302741124; bluefishai.com; finsmes 17-abr; Built In NYC 17-abr |
| (referência) 17-nov-2025 | Peec AI | Série A | US$ 21 M | Singular | US$ 29 M | TechCrunch 17-nov-2025; peec.ai/blog |
| (referência) jul-2025 | Scrunch AI | Série A | US$ 15 M | Decibel | US$ 19 M | Crunchbase; PitchBook 708134-32 |
| (referência) ano-2025 | AthenaHQ | Seed | US$ 2,2 M | Y Combinator | US$ 2,7 M | Crunchbase athenahq |

### 3.2 Rodadas adjacentes confirmadas

- **05-mai-2026 (relatado em PRNewswire):** Searchable secured US$ 14 M growth funding, lead Headline, val. US$ 85 M. Não pure-play GEO mas ferramenta de discovery interna que toca AI search.
- **OpenAI 6 aquisições em jan-mar-2026:** Astral (19-mar), Promptfoo (mar), Convogo (jan), Torch Health (jan), Crixet (jan), OpenClaw (fev) — nenhuma é pure-play GEO, mas Promptfoo é adjacente (testing AI apps, útil para GEO operators).

### 3.3 M&A confirmados no espaço

**Nenhuma aquisição pure-play GEO foi reportada entre 01-jan-2026 e 20-mai-2026.** A consolidação ocorre via VC rounds, não M&A. Aquisições históricas relevantes que ainda figuram no contexto:
- Conductor adquiriu Searchmetrics em fev-2023 (fora do recorte).
- BrightEdge adquiriu Oncrawl em fev-2022 (fora do recorte).
- Daydream (Bornstein, e-commerce, diferente do Daydream/SEO): exits ainda em formação.

### 3.4 Tendências macro

- **Gartner forecast 2026:** AI spending global US$ 2,52 trilhões (+44% YoY).
- **2025 M&A global record:** US$ 4,8 trilhões em valor (segundo maior ano da história).
- **BrightEdge data 08-abr-2026:** AI agent requests = 88% do volume de tráfego organic search humano; projeção: ultrapassar até fim 2026.
- **Similarweb data:** AI platforms geraram 1,1 bilhão de referrals em jun/2025 (+357% YoY).
- **OpenAI acquisition cadence:** 6 em jan-mai-2026 vs ~6 em todo 2025 — escala dramática.

---

## Parte 4 — Recomendação de stack por tier

### 4.1 Tier Solo Consultant (~US$ 100/mês) — alexandrecaramaschi.com

**Stack canônico:**
- **Otterly Lite — US$ 29/mês** (15 prompts custom, ChatGPT + AIO + Perplexity + Copilot, 1.000 URL audits)
- **Surfer Discovery — US$ 49/mês** (AI Tracker básico em ChatGPT + content guidelines SEO+GEO + AI assistant)
- **Google Search Console + Bing Webmaster + IndexNow** — gratuito; pipeline canônico do landing-page-geo
- **Looker Studio com Otterly connector** — gratuito; dashboards client-ready
- **Manual cron Perplexity sonar API (~US$ 5-10/mês)** para 25 prompts canônicos × 4 LLMs semanal (já documentado em larissa-geo/docs/geo/llm-mention-rate-canonical-25-prompts.md)

**Total: ~US$ 88/mês.** Cobre: visibilidade em 4 LLMs, content optimization base SEO+GEO, audit técnico, dashboard semanal, geração editorial via sub-agents Opus do Claude Code (já no .env Brasil GEO).

**Quando upgradar:** se número de prompts canônicos passar de 25 ou se cliente exigir Gemini/Claude tracking robusto, mover para tier SMB.

### 4.2 Tier SMB Multi-portal (US$ 500-1.500/mês) — ecossistema Brasil GEO completo

**Stack canônico para 12+ portais:**
- **Peec Pro — US$ 245/mês** (3 modelos + Claude/DeepSeek/Gemini adicionais, 2 projetos; usa API + Looker Studio connector para alimentar dashboards centralizados)
- **AthenaHQ Self-Serve anual — US$ 95/mês** (8 LLMs incl. Grok, 3.600 credits, integração nativa GA4 + GSC + Shopify para portais e-commerce do ecossistema)
- **Surfer Pro — US$ 182/mês** (multi-model AI tracking + content guidelines completos para os 12 portais)
- **Frase Scale — US$ 299/mês** (AI Agent 80+ skills + AI visibility tracking 5 platforms + 80+ skills para automação editorial)
- **Ahrefs base plan + Brand Radar Select Platforms — base US$ 129 + add-on US$ 420 = US$ 549/mês** (243 M prompts orgânicos + 2.500 custom checks; única ferramenta com escala de keyword universe)

**Subtotal:** ~US$ 1.370/mês. Tier de produção. Equivalente a 1/3 do custo de SEM tier alto. Recomendação de prioridade se budget começa em US$ 500: Peec Pro + Surfer Pro + Otterly Standard (US$ 189) = US$ 616/mês com cobertura sólida.

**Diferencial Brasil GEO:** o ecossistema já tem stack proprietária (geo-orchestrator 5 LLMs + scripts Perplexity GSC IndexNow) que reduz dependência de vendor. Brasil GEO pode operar tier SMB com US$ 500/mês comprando só Peec Pro + Otterly Standard + IndexNow.

### 4.3 Tier Enterprise (US$ 5k+/mês) — clientes de consultoria

**Stack canônico para Fortune 500 BR ou clientes grandes:**
- **Profound Growth ou Enterprise — US$ 399-2.000+/mês** (Agents v2 + Prompt Volumes + SOC 2 + Deep Research; mandatório para entrar em discussões C-level em Fortune 500 BR)
- **Bluefish AI Enterprise — US$ 1.500-5.000/mês** (AI Accuracy module + Agentic Marketing + RBAC + SSO; obrigatório se cliente faz commerce ou pharma compliance)
- **Similarweb AI Channels Enterprise — US$ 2.000-5.000/mês** (digital intelligence + AI referrals attribution real)
- **Clearscope Business — US$ 399/mês** (Tracked Topics + AI Drafting + Content Inventory para times editoriais grandes)
- **Conductor — US$ 4.000+/mês** (se cliente já tem stack Conductor existente)
- **Ahrefs Brand Radar All Platforms — US$ 740/mês**

**Subtotal piso:** US$ 5.500/mês. Teto enterprise pode passar US$ 30k/mês.

**Para consultoria Brasil GEO entregar projetos Fortune 500 BR (Itaú, Stone, Magalu, Natura, Vale, Bradesco):** stack pivot canônico = Profound Growth + Bluefish AI + Similarweb AI Channels + Clearscope Business + Ahrefs Brand Radar = ~US$ 4.000-8.000/mês repassado ao cliente. Brasil GEO entra como integrador estratégico + operador local com voice em PT-BR + JSON-LD canônico.

### 4.4 Decisões pendentes Brasil GEO

1. **Adoção Peec vs AthenaHQ no tier solo:** Peec tem velocidade europeia + Looker connector; AthenaHQ tem 8 LLMs incl. Grok + Shopify nativo. Para alexandrecaramaschi.com, Peec é melhor; para herreirasemijoias.com.br (Shopify), AthenaHQ é mais natural.
2. **Profound Growth vs Sales-pivot direto:** Profound Growth a US$ 399/mês é elegível para o tier solo se cliente é Fortune 500 BR específico. Mas a cobertura limitada (sem Gemini) frustra. Aguardar Profound publicar plano público com Gemini para reconsiderar.
3. **Frase Scale vs Surfer Pro como suite SEO+GEO:** Frase tem AI Agent completo desde Starter; Surfer tem AI Tracker em todos. Para Brasil GEO produzindo 100+ artigos/mês, Surfer Pro (US$ 182) tem melhor cost-per-document. Para uma única consultoria boutique, Frase Scale.
4. **Investimento em Ahrefs Brand Radar:** custo total US$ 549/mês (base + Select Platforms). Justifica-se se mais de 5 clientes Brasil GEO usam Ahrefs como hub canônico de keyword research. Caso contrário, ficar com Peec + Otterly.

---

## Apêndice A — URLs validadas via WebFetch (20-mai-2026)

| URL | Status WebFetch | Achado canônico |
|---|---|---|
| https://www.tryprofound.com | 200 OK | Confirmou Profound = AI search visibility platform, customer Ramp testimonial, AEO category |
| https://www.tryprofound.com/pricing | 200 OK navigation only | Pricing oculto, requer sales call — confirmado sales-led |
| https://peec.ai/pricing | 200 OK | Confirmou Starter/Pro/Advanced/Enterprise estrutura; pricing tier names sem USD value visível na página (USD obtido via cairrot review cross-check) |
| https://otterly.ai/pricing | 200 OK | Pricing transparente: Lite US$ 29, Standard US$ 189, Premium US$ 489. Annual 15% off |
| https://athenahq.ai/pricing | 200 OK | Self-Serve US$ 295/mês (US$ 95 anual com 17% off), Enterprise custom |
| https://www.athenahq.ai | 200 OK | Confirmou clientes SoFi/Coinbase/Amazon/DeVry; "State of AI Search 2026 Report" lançado em mai-2026 |
| https://ahrefs.com/brand-radar | 200 OK | Select Platforms ¥61.200 (~US$ 420); All Platforms ¥107.800 (~US$ 740); beta YouTube/TikTok/Reddit |
| https://daydream.run/pricing | ECONNREFUSED | Domínio inexistente — Daydream usa withdaydream.com (confirmado via Web Search) |
| https://www.daydream.ai/pricing | 404 Not Found | Confirmado: Daydream/SEO usa withdaydream.com, não daydream.ai (que pertence a Bornstein/e-commerce) |
| https://www.scrunchai.com/pricing | 301 redirect | Confirmado: scrunchai.com → scrunch.com migração 2026 |
| https://scrunch.com/pricing | 200 OK | Starter US$ 250 anual/US$ 300 mensal, Growth US$ 417/US$ 500, Enterprise custom + Enterprise Data API |
| https://www.bluefishai.com | 200 OK | Confirmou Série B 14-abr-2026, total US$ 68 M, CEO Alex Sherman, customers Adidas/Amex/LVMH |
| https://bluefish.ai | empty body | Domínio principal é bluefishai.com, não bluefish.ai |
| https://www.semrush.com/ai-toolkit/ | 404 (URL pública limitada) | AI Toolkit é módulo do upgrade Pro+, não tem página standalone com pricing |
| https://surferseo.com/pricing/ | 200 OK | Discovery US$ 49, Standard US$ 99, Pro US$ 182, Peace of Mind US$ 299; AI Tracker em todos os planos |
| https://www.frase.io/pricing/ | 200 OK | Starter US$ 49 (anual US$ 39,20), Professional US$ 129, Scale US$ 299, Enterprise; AI Agent 80+ skills |
| https://writesonic.com/pricing | 200 OK | Starter US$ 79, Basic US$ 199, Growth US$ 399, Enterprise; cobertura 10 LLMs no Enterprise |
| https://www.clearscope.io/pricing | 200 OK | Essentials US$ 129, Business US$ 399, Enterprise custom; Tracked Topics novo em mai-2026 |
| https://www.brightedge.com | 200 OK | Sem pricing público; AI Catalyst + Data Cube X + Copilot/Autopilot; foco enterprise |
| https://goodieai.com | 404 (próprio) / higoodie.com 200 OK | Domínio canônico é higoodie.com |

## Apêndice B — Citações canônicas mai-2026 para reuso em copy

1. "Profound atingiu US$ 1 bilhão de valuation em 24-fev-2026 com Série C de US$ 96 milhões liderada pela Lightspeed, sinalizando a maturidade comercial do GEO como categoria." (Fortune 24-fev-2026)
2. "Mike King, em 18-mai-2026, classificou a documentação Google sobre AI search como 'naive and self-serving', apontando contradições com o próprio paper MUVERA." (iPullRank)
3. "O estudo Ahrefs de 11-mai-2026 (1.885 páginas) provou que adicionar JSON-LD não move citations em AI: Google AI Overviews -4,6%, AI Mode +2,4%, ChatGPT +2,2%." (Search Engine Journal)
4. "Cyrus Shepard, em 07-mai-2026, publicou framework de 23 AI Citation Ranking Factors; URL accessibility (9,5) ficou em primeiro." (Zyppy Signal)
5. "BrightEdge documentou em 08-abr-2026 que AI agent requests alcançaram 88% do volume de busca humana orgânica, com projeção de ultrapassagem ainda em 2026." (BrightEdge)
6. "Similarweb registrou 1,1 bilhão de referrals via AI em jun/2025 (+357% YoY), evidenciando AI como canal de aquisição maduro." (Similarweb Generative AI Report 2025)
7. "Kevin Indig, em 11-mai-2026 ('The Consensus Gap'), mediu apenas 18% de overlap nos top 10 domínios citados entre ChatGPT, Perplexity e Google AIO — exigindo estratégia por engine." (Growth Memo)
8. "Bluefish AI raised US$ 43 M Série B em 14-abr-2026 co-liderada por Threshold + NEA, atendendo ~10% da Fortune 500." (PRNewswire 302741124)
9. "Peec AI cresceu de 0 para 1.300 marcas em 9 meses (fev-2025 a nov-2025), com 300 novos clientes/mês — ritmo possível para o ecossistema Brasil GEO replicar." (TechCrunch 17-nov-2025)
10. "Lily Ray, em 13-mai-2026, alertou que listicles auto-promocionais escalonados são tratados como spam por Google e Microsoft em AI search — shelf life de táticas GEO populares está se esgotando." (PPC Land)

---

> Fim do Track D. Próxima leitura recomendada: cruzar com Track A (panorama macro) e Track B (research técnico em retrieval/citation) para reconciliar narrative editorial canônica do landing-page-geo.
