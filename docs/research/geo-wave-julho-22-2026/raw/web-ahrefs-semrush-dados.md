# Pesquisa web — Ahrefs, Semrush/Adobe, estudos de dados AI search (22/07/2026)

Fonte: subagente de pesquisa web (WebSearch/WebFetch). Fatos com URL e data; fontes secundárias sinalizadas.

## 1. Ahrefs

### Brand Radar (jul/2026)
- Mede: menções de marca, citações (links), posicionamento em respostas de IA; "AI Share of Voice" vs concorrentes; impressões estimadas (ahrefs.com/brand-radar; ahrefs.com/academy/how-to-use-brand-radar/intro).
- Cobertura: Google AI Overviews & AI Mode, ChatGPT, Perplexity, Microsoft Copilot, Gemini e Grok + YouTube, TikTok e Reddit.
- Base de prompts: 406M+ prompts mensais (Google AI 319M+; ChatGPT 16M+), "search-backed, not synthetic". Em 05/03/2026 Tim Soulo citava 243M+. Preços oficiais: US$ 398/mês (2.500 checks de prompts customizados) e US$ 699/mês; terceiros citam US$ 199–699 como add-on (tryanalyze.ai, 2026).
- Atualizações 2026: exportação de dados, demo searches, AI Content Grader no Content Explorer, detecção de AIO no Rank Tracker, cruzamento backlinks × citações de IA (arfadia.com; dageno.ai).

### Estudos CTR
- Abr/2025 — "AI Overviews Reduce Clicks by 34.5%" (ahrefs.com/blog/ai-overviews-reduce-clicks/): 300k keywords, GSC agregado, mar/2024 vs mar/2025; CTR da posição 1 −34,5% com AIO; 99,2% das keywords com AIO são informacionais. Autora: Xibeijia Guan.
- 04/02/2026 — "AI Overviews Reduce Clicks by 58%" (ahrefs.com/blog/ai-overviews-reduce-clicks-update/, Ryan Law + Xibeijia Guan): mesma base, dez/2023 vs dez/2025 (desktop). CTR pos. 1 −58% com AIO. CTRs absolutos: 0,076 (dez/2023 sem AIO) → 0,039 (dez/2025 sem AIO) → 0,016 (dez/2025 com AIO). Pos. 2 = −50,8% … pos. 10 = −19,4%. Parte da queda é secular; a AIO corta por cima.
- Metodologia: dados agregados de Search Console, não painel clickstream.

### Conversão de tráfego de IA
- "Does AI Search Traffic Convert Better…" (ahrefs.com/blog/ai-search-traffic-conversions-ahrefs/, 16/06/2025, Patrick Stox): AI search = 0,5% do tráfego, 12,1% dos signups — ~23x a conversão do orgânico. First-party (Ahrefs Web Analytics), 1 site, público atípico; usuários de AI search clicam ~75% menos.

### Posts-chave
- Tim Soulo — "GEO Tool Market Analysis: 47 Vendors, One Commodity, and The Data Problem" (blog.timsoulo.com, 05/03/2026): 47 ferramentas; mecanismo (prompts agendados + dashboard) é commodity; ~80% dos vendors devem sumir em 3–5 anos; diferencial = origem dos dados de prompts. Também: comparativo Profound vs Brand Radar (medium.com/@timsoulo); entrevista "From SEO to GEO in 2026" (searchpilot.com).
- Ryan Law — "Generative Engine Optimization: Growth Strategies and Metrics For the AI Era" (ahrefs.com/blog/geo-generative-engine-optimization/): maioria das menções vem de sites de terceiros. "Top Brand Visibility Factors… (75k Brands Studied)" (ahrefs.com/blog/ai-brand-visibility-correlations/): fator nº 1 = amplitude de sites mencionando; AI Mode correlaciona mais com sinais de marca tradicionais. "67% of ChatGPT's Top 1,000 Citations Are Off-Limits" (ahrefs.com/blog/chatgpts-most-cited-pages/): Wikipedia, homepages, app stores = citações não influenciáveis. Levantamento 900k páginas novas (abr/2025): 74,2% com conteúdo gerado por IA.
- Patrick Stox — estudo 23x + "How to Monitor Brand Mentions in ChatGPT" (ahrefs.com/blog/monitor-brand-mentions-chatgpt/).

## 2. Semrush

### AI Visibility Toolkit
- semrush.com/kb/1493-ai-visibility-toolkit: seções AI Visibility, Brand Performance, Monitoring; mede AI Visibility Score, Share of Voice, sentimento (Overall Sentiment Score), menções e prompts, em ChatGPT, AIO, AI Mode e Gemini. Complementos: Semrush Copilot, ContentShake AI.
- **AI Visibility Index 2026** (press release 26/06/2026: semrush.com/news/463141-…): 126 milhões de prompts dos EUA (jan–abr/2026), 22 indústrias, ChatGPT/Gemini/AI Mode/AIO. Achados: ChatGPT cita em média 15 fontes por resposta vs 3 do Gemini; 45% dos líderes de marketing não conseguem medir visibilidade em IA; só 36 marcas globais no top-100 das 4 plataformas; 81% das organizações com estratégia unificada SEO+IA reportaram aumento de tráfego vs 36% das que separam.

### Estudo de conversão
- AI Search SEO Traffic Study (semrush.com/blog/ai-search-seo-traffic-study/): visitante de AI search vale 4,4x o orgânico (taxa de conversão); 500+ tópicos → prompts; projeção: valor econômico similar ao da busca tradicional até fim de 2027. Cobertura: martech.org (13/06/2025 — MarTech é da Semrush); ppc.land.

### Adobe
- **Aquisição concluída em 28/04/2026**: US$ 1,9 bi all-cash, US$ 12,00/ação (anunciada nov/2025). Fontes: news.adobe.com/news/2026/04/adobe-completes-semrush-acquisition; semrush.com/news/455953-…; FAQ semrush.com/news/455963-….
- **Adobe LLM Optimizer**: GA out/2025 (news.adobe.com/news/2025/10/…): monitoramento de tráfego de IA, benchmark de visibilidade, motor de recomendações (conteúdo + técnicas/metadados), Visibility Score proprietário (menções + proeminência + acurácia + sentimento), automação de fixes. Docs: experienceleague.adobe.com/en/docs/llm-optimizer/using/home.
- Integração 2026: Semrush no pilar "brand visibility" do Adobe CX Enterprise (Adobe Summit 2026), com AEM, LLM Optimizer, Commerce e Brand Concierge; "Adobe Brand Visibility" combinando ~289M prompts da Semrush com o LLM Optimizer (pulse2.com; news.designrush.com). Dado Adobe: tráfego de IA para varejo +1.324% (out/2024→mai/2026).

## 3. Estudos de dados 2026

### Similarweb (painel clickstream)
- "Gen AI Stats 2026" (similarweb.com/blog/marketing/geo/gen-ai-stats/, 28/05/2026): visitas ao ChatGPT +84% (set/2024→mar/2026); Gemini ~9x (app +1.100%); Claude ~+770%; referral de IA para sites >3x (set/2024→set/2025). Referral específico da Perplexity: não encontrado.
- 07/05/2026 (similarweb.com/blog/insights/ai-news/chatgpt-referral-traffic-triples/): ChatGPT passou a mostrar links de marca clicáveis → referrals +157,7% WoW; homepage +354,7%; share de referrals na homepage 26–32% → ~60%. Conversão do referral do ChatGPT: 7,1% vs paid search 7,8% (à frente de direct/orgânico/social/e-mail/display).
- Vencedores por indústria: similarweb.com/blog/insights/ai-news/ai-referral-traffic-winners/.

### BrightEdge (telemetria própria)
- AIO: ~31% das queries (fev/2025) → ~48% (fev/2026), +58% YoY; educação 18%→83%, B2B tech 36%→82%, restaurantes 10%→78% (searchenginejournal.com/…/568448/; brightedge.com).
- 08/04/2026 (brightedge.com/news/press-releases/brightedge-data-ai-search-reaching-tipping-point-ai-agents-2026): requisições de agentes de IA = 88% da atividade de busca orgânica humana; agentes ~15% do tráfego dos sites, 95% disso da OpenAI; só 19% dos sites têm diretivas para bots do ChatGPT; previsão: agentes ultrapassam busca humana até fim de 2026. Metodologia não detalhada.
- Moz (40.000 queries, via digitalapplied.com): 88% das citações do Google AI Mode não vêm do top-10 orgânico.

### Conductor e seoClarity
- Conductor: Creator + Intelligence + Monitoring; rastreia Google, ChatGPT, Perplexity etc.; Data API; **AgentStack** (apps LLM nativos para ChatGPT, Claude e Copilot + servidor MCP); parceria Optimizely (cmswire.com); "2026 AEO/GEO Benchmarks Report" (conductor.com/academy/aeo-geo-benchmarks-report/).
- seoClarity: ArcAI + Content Fusion; jul/2026 lançou **LiveWire™** (seoclarity.net/resources/news/…). Achado: desde mar/2026 o **ChatGPT reduziu fortemente citações externas** (share de respostas com citação e nº por resposta) — seoclarity.net/chatgpt-citation-decline-analysis.

### Amsive e Kevin Indig
- Amsive (abr/2025, ~700k keywords, 5 indústrias): CTR com AIO −15,49% média; non-branded −19,98%; branded com AIO +18,68% (só 4,79% das branded disparam AIO); AIO + featured snippet −37,04% (amsive.com/insights/seo/google-ai-overviews-new-research-…).
- Kevin Indig: primeiro estudo de UX de AIO (mai/2025, com Eric Van Buskirk; growth-memo.com/p/the-first-ever-ux-study-of-googles): 70 usuários, 8 tarefas, 29h think-aloud, 400+ encontros com AIO. AIOs em 42% das queries analisadas (704/1.675). Sumário 2026: growth-memo.com/p/2026-growth-memo-research-summary.

### Pew Research (painel com consentimento)
- 22/07/2025 (pewresearch.org/short-reads/2025/07/22/…): ~900 adultos EUA, mar/2025; 68.879 queries, 12.593 com AI summary. Clique em resultado tradicional: 8% com resumo vs 15% sem; cliques em links do resumo: 1%; abandono da sessão: 26% vs 16%.

## 4. Benchmarks de conversão (não comparáveis entre si)

| Fonte | Número | Metodologia | Data |
|---|---|---|---|
| Ahrefs (site próprio) | AI = 0,5% do tráfego, 12,1% dos signups → ~23x | First-party, 1 site | 16/06/2025 |
| Semrush | Visitante AI vale 4,4x | Multi-site, 500+ tópicos | jun/2025 |
| Similarweb | Referral ChatGPT converte 7,1% vs 7,8% paid | Painel clickstream | mai/2026 |
| Microsoft Clarity (via agregadores) | signup 1,66% vs 0,15% (~11x), 1.200+ sites | Telemetria Clarity — fonte primária NÃO localizada | 2025/2026 |
| "Claude 16,8%/ChatGPT 14,2%/Perplexity 12,4% vs Google 2,8%" | agregadores (coseom.com) | NÃO verificado — cautela | 2025/2026 |

Consenso honesto: conversão 4x–23x melhor, sobre volumes pequenos (fração de 1% a poucos % do tráfego); cada estudo mede conversão diferente.

## 5. WordPress/CMS
- Yoast SEO: geração automática de llms.txt (yoast.com/features/llms-txt/); guia LLM SEO.
- Rank Math: módulo llms.txt granular (post types, páginas, produtos, URLs manuais); ambos em 2025.
- Caveat (jun/2026): Google atualizou docs — llms.txt não ajuda nem prejudica rankings e não é usado pelos recursos de IA do Google Search (searchenginejournal.com/googles-says-its-fine-to-use-llms-txt-for-ai-seo/579608/).

## Nota de metodologias
- Painel clickstream (Similarweb, Pew): tendências de mercado, impreciso por site.
- First-party (Ahrefs WA, Clarity): preciso no site medido, não generalizável; referral de LLM subcontado (chega como "direct").
- GSC agregado (Ahrefs CTR, Amsive): CTR real, só ecossistema Google.
- Telemetria de plataforma (BrightEdge, Semrush, seoClarity): grandes volumes, amostragem proprietária não auditável.

## Não encontrado
- Referral específico da Perplexity no post 2026 da Similarweb; fonte primária do estudo Microsoft Clarity; dado "Claude 16,8%/12,3M visitas".
