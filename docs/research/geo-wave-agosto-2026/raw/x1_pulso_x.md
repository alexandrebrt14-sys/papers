# x1_pulso_x (xAI grok-4.6 responses+x_search)

**Pulso da comunidade SEO/GEO (22 jul – 27 ago 2026)**

O período foi marcado pela expansão acelerada de AI Overviews/AI Mode (especialmente França em 22 jul), spam updates do Google, queda contínua de CTR orgânico, debate intenso sobre medição de visibilidade em IA (citações vs. tráfego/referrals), ceticismo oficial do Google sobre “GEO hacks” e atualizações pesadas de ferramentas de vendors. A comunidade oscila entre “GEO é o novo santo graal” e “é só SEO de sempre, com métricas diferentes”. Tráfego de referral de IA cresce rápido (ChatGPT ainda dominante), mas permanece fatia pequena do total; conversão às vezes supera orgânico tradicional. Zero-click e “good SEO is good GEO” dominam o discurso oficial.[[1]](https://www.lumar.io/blog/industry-news/ai-search-seo-industry-news-july-2026/)

Fontes primárias (docs Google, press/blog vendor, papers) vs. secundárias (imprensa, blogs, X) estão distinguídas abaixo. Dados anteriores a 22 jul só entram se fundadores (ex.: guia Google de maio/jun).

### Eventos e atualizações principais do Google
| Data | Fato | Fonte (tipo) | URL |
|------|------|--------------|-----|
| 22 jul 2026 | Google liga AI Overviews e AI Mode na França; em 3–4 dias, ~66% dos SERPs rastreados (informacionais) passaram a exibir AI Overview (de 0%). | Secundária (estudo próprio + Semrush) | https://hacktheseo.com/geo-vs-seo-2/ |
| ~final jul 2026 | Spam update de julho concluiu rollout em ~2 dias; sem novas políticas de spam anunciadas. Recuperação de penalidades leva meses. | Secundária (Lumar roundup, dashboard Google) | https://www.lumar.io/blog/industry-news/ai-search-seo-industry-news-july-2026/ |
| 18–21 ago 2026 | Spam update de agosto (3º do ano) rolou em ~2,5 dias; classificadores de spam em AI Overviews/AI Mode reaplicados. Impacto estimado 10–20% em tráfego para alguns publishers. | Secundária (SEJ, Storyboard18, dashboard) | https://searchengineland.com/library/google-seo ; https://www.storyboard18.com/advertising/googles-ai-overviews-spam-updates-devalue-traffic-ws-lo-108927.htm |
| 24 ago 2026 | John Mueller: “from our POV there’s nothing really special you need to do for generative AI responses in search.” AI search puxa do índice regular + query fan-out. | Primária (Mueller) via secundária SEJ | https://www.searchenginejournal.com/google-answers-if-some-sites-can-ignore-geo-and-just-focus-on-seo/586737/ |
| 26 ago 2026 | Google confirma rollout de parâmetros goto URL (redirects server-side) para combater scrapers/abuse; “long history of deploying technical measures”. Afeta ferramentas de SERP tracking. | Primária (declaração Google a Barry Schwartz) | https://www.seroundtable.com/google-search-goto-tracking-41957.html |
| Período | Google reforça “good SEO is good GEO”: fundamentos técnicos, conteúdo único/não-commodity, sinais de ranking existentes. Só links visíveis (não menções de marca) contam como impressões em AI Overviews/AI Mode. | Primária (guia Search Central + Think with Google) | https://developers.google.com/search/docs/fundamentals/ai-optimization-guide |

Guia oficial Google (maio/jun, ainda vigente): RAG + query fan-out; ignore llms.txt, chunking, reescrita “para IA”, schema especial. Foco em conteúdo people-first, estrutura técnica clara, Merchant Center/GBP para local/ecom. Medição via Search Console (filtros de AI features em rollout).[[2]](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)

AI Mode superou 1B MAUs (I/O 2026); queries ~3x mais longas, mais conversacionais/multimodais. Link carousels para tópicos em desenvolvimento chegaram a AI Mode (já em Overviews). Gemini 3.7 Flash em rollout para subscribers.[[3]](https://www.searchenginejournal.com/ai-mode-queries-are-3x-longer-the-case-for-leading-with-the-answer/585990/)

### Polêmicas e debates quentes
**Ceticismo sobre GEO como disciplina separada**: Google (Mueller + guia) trata AEO/GEO como extensão de SEO. Paper crítico (arXiv 2607.14035, jul) revisou 45 estudos: táticas GEO não demonstram efeito estável cross-platform em retrieval orgânico ou tráfego downstream; o famoso “+40% visibilidade” é máximo relativo em contexto fixo, não geral. Rewrites body-only podem até reduzir presença top-10 em 16%. Vendors continuam vendendo ganhos não confirmados por engine.[[4]](https://ppc.land/survey-of-45-studies-finds-geo-rewrites-can-cut-a-pages-ai-retrieval-16/)

**llms.txt**: Adotado em massa (~28% de domínios em amostras Ahrefs), mas 97% dos arquivos válidos receberam zero requests em maio 2026. Tráfego restante majoritariamente de ferramentas SEO/auditores, não LLMs de busca/citação (GPTBot/Claude Code minoria). Google ignora explicitamente (guia + Illyes 2025). V2 da spec (Jeremy Howard, 10 ago) adiciona linking Markdown e header HTTP; Chrome Lighthouse checa, mas Search não usa. Comunidade dividida: “barato, faça como seguro” vs. “desperdício vs. conteúdo/entidade”. Tim Soulo (Ahrefs) e Dan Petrovic: “mostly pointless”.[[5]](https://crklr.com/news/llms-txt/)

**Dados de referral de IA e CTR**: Ahrefs: CTR do #1 orgânico cai ~58% quando AI Overview aparece (atualização fev 2026 com dados dez 2025; inicial 34,5%). Só 38% das URLs citadas em AI Overviews também rankeiam top 10 tradicional (caiu de ~76% um ano antes). Tráfego AI (ChatGPT ~60-90% share conforme painel, Gemini/Claude crescendo) explode em volume relativo (+centenas % YoY em alguns), mas ainda 2-11% das sessões por indústria; conversão frequentemente 1,5–4x+ vs. orgânico em estudos (Adobe, Semrush, First Page Sage, Brainlabs). Painéis mostram ChatGPT caindo em share relativo, Claude/Gemini subindo. 80%+ do crawl AI é treinamento, não referral. Zero-click sobe. Analytics web tradicionais falham para “onde alcançar clientes” (Rand Fishkin).[[6]](https://naturaily.com/blog/query-fan-out-seo-and-ai-citations)

**Outras**: Reddit share em citações ChatGPT despencou ~86% mid-ago (causa não confirmada). AI slop backlash (Spotify removeu 75M tracks, LinkedIn apertou). IRS perdeu visibilidade Google mas ChatGPT/Bing ok (possível bug Google). Prompt “search volume” é ilusão (Tim Soulo: parágrafos, rambling, personalização).

### Threads e discussões mais citadas no X (22 jul–27 ago)
- **Rand Fishkin (@randfish, 12 ago)**: “I'm worried that citation analysis research is misleading us... badly. AI tools often already know which brands they're going to search for and recommend...” Relatório: suganthan.com. ~33k views, alta discussão. https://x.com/randfish/status/2087612290610970640
- **Rand (26 ago)**: Analytics web não serve mais para A) alcançar clientes, B) fontes valiosas, C) onde investir. Lily Ray quoteou. https://x.com/randfish/status/2092684976051704299
- **Barry Schwartz (@rustybrick, 26 ago)**: Goto URLs rolling out (anti-scraper); Google confirmou. Lily Ray: “very big deal”. Glenn Gabe comentou impacto em ferramentas. Thread com ~36k views. https://x.com/rustybrick/status/2092763164219683112
- **Aleyda Solis (@aleyda)**: Survey SEOFOMO State of AI Search Optimization (fecha 27 ago); maior desafio = medir visibilidade de forma confiável (60/111 respostas iniciais). Framework 3 camadas atualizado. Fan-out ChatGPT branded (MJ Cachon). https://x.com/aleyda/status/2091819497384472659 e https://x.com/aleyda/status/2092540731726430718
- **Lily Ray (@lilyraynyc, 26–27 ago)**: Authentic/organic content vai ser mais desejado por slop. Goto URLs grande. Quoteou Tim Soulo/Ahrefs podcast (llms.txt pointless, sem prompt volume, biases primários/secundários, Trojan horse para citações). https://x.com/lilyraynyc/status/2092682455211713003
- **iPullRank/Mike King**: Zero-click Q3 2026, 89% respostas AI unbranded de terceiros, 44% shoppers começam em AI, omnimedia strategy, readiness quiz. Conteúdo resonance vs. volume.
- Outros: Kevin Indig (@Kevin_Indig) elogiou link carousels AI Mode (“better for publishers”). Discussões slop antibodies, IRS drop, Claude vs. Claude Code (Profound).

### O que os principais nomes disseram (seleção do período)
| Nome / Handle | Data aprox. | Posição / Fato-chave | Link X ou fonte |
|---------------|-------------|----------------------|-----------------|
| Rand Fishkin (@randfish) | 12 ago, 26 ago | Citações/URLs enganam (modelos já “conhecem” marcas); analytics web obsoletos para decisão de investimento. Livro Zero Click Marketing em audiobook. | https://x.com/randfish/status/2087612290610970640 |
| Lily Ray (@lilyraynyc) | 26–27 ago | Slop vai aumentar demanda por autêntico. Goto URLs “very big deal”. Apoio a Tim Soulo (sem volumes de prompt, llms.txt inútil). | https://x.com/lilyraynyc/status/2092779392057450935 |
| Kevin Indig (@Kevin_Indig) | 25 ago + SEJ 24 ago | Link carousels AI Mode positivos. “Slop antibodies”: empresas precisam filtrar output AI interno. | https://x.com/Kevin_Indig/status/2092305523588685936 ; SEJ artigo |
| Aleyda Solis (@aleyda) | 24–27 ago | Medir visibilidade IA é o #1 desafio. Framework 3 camadas (presence, readiness, business impact). Fan-out branded importa (indexabilidade, reputação, consistência). Survey comunitária. | https://x.com/aleyda/status/2091819497384472659 |
| Mike King / iPullRank (@ipullrank, @VeryWellVersed) | Ago | SEO não está morto; mais superfícies. 89% AI answers unbranded de 3os. Omnimedia + resonance. Zero-click sobe, paid segura. AI readiness assessment. | Vários posts @ipullrank ago |
| Glenn Gabe (@glenngabe) | 26 ago | Goto links ~100% rollout (anti-bot). IRS drop pode ser Google-side (ChatGPT/Bing ok). | https://x.com/glenngabe/status/2092715951154241926 |
| Barry Schwartz (@rustybrick) | 26 ago | Reportou/confirmou goto URLs + AI Overviews chegando em Workspace. Cobertura diária SERoundtable. | https://x.com/rustybrick/status/2092763164219683112 |
| Profound (@profound) | 19–21 ago | AEO Guide (6 caps, 16 líderes). Index Report Summer 2026 (visibilidade local vs. global, movers Q2). Preferem AEO. Claude vs. Claude Code distintos. Community para Marketing Engineers. | https://x.com/profound/status/2090876636547670045 ; tryprofound.com |
| Ahrefs (@ahrefs) | Jul–ago | Brand Radar: 14M→30M prompts, Claude support (28 jul), Adaptive traffic (AI Overviews), AI counts em Site Explorer, novos APIs. Tim Soulo: sem prompt volume, llms.txt pointless. | Vários @ahrefs ; podcast com Dan Petrovic |
| Semrush (@semrush) | Ago | Posts gerais advanced SEO 2026; agora Adobe. Menos anúncios específicos GEO no período vs. Ahrefs. | Poucos posts relevantes |

### Anúncios de vendors (destaques)
- **Ahrefs**: Expansão agressiva Brand Radar (prompts, Claude, volume AI-adjusted), Adaptive traffic model (15 SERP features incl. AI Overviews), AI visibility em Top pages/Site Explorer, APIs. Foco em dados realistas vs. volume tradicional.
- **Profound**: AEO Guide 21 ago; Index Report 19 ago (1,9B+ conversas); glossário 300+ termos; estudo Claude vs. Claude Code. Plataforma AEO/GEO enterprise (quote-based).
- **Outros**: Lumar GEO Toolkit; Microsoft Clarity/Bing Webmaster (bot tracking, citation share, intents); iPullRank quizzes/relatórios zero-click; Semrush menos visível em GEO específico.

**Não localizado no período**: Declarações específicas de Semrush sobre GEO/llms.txt/AI Mode além de posts genéricos; dados Brazil-only de AI Mode rollout (França destacada); Profound handle confirmado @profound / tryprofound.com.

### Implicações acionáveis para consultoria GEO no Brasil (alexandrecaramaschi.com / brasilgeo.ai)
Priorize **fundamentos Google** (conteúdo único/expert, técnico limpo, entidades, GBP/Merchant) — Mueller e guia oficial dizem que isso alimenta AI Overviews/AI Mode via índice + fan-out. Ignore hacks caros (llms.txt como prioridade, chunking, “GEO rewrite”). Meça **citações/share of voice + referral AI + conversão**, não só rankings/tráfego (GSC filtros AI, Brand Radar/Profound-like, UTM). Tráfego AI cresce e converte bem em B2B/SaaS/serviços, mas zero-click sobe — construa autoridade off-site (PR, menções, original research) para ser a fonte citada, não só o site. Conteúdo PT-BR autêntico + consistência de entidade (marca, founder, localização) ajuda em fan-out branded. Teste multi-engine (ChatGPT ainda líder, Gemini/Claude subindo), mas Google continua o maior. Spam updates e goto URLs afetam tools/scraping. Slop backlash favorece qualidade humana. Survey Aleyda e Rand mostram: o gap agora é **medição confiável e decisão de investimento**, não mais “fazer GEO”.

Fonte primária Google continua o norte; vendors vendem dashboards. Foque ROI em visibilidade citável + tráfego de alta intenção. Dados mudam rápido — reavalie mensalmente.

## Fontes
- https://crklr.com/news/llms-txt/
- https://developers.google.com/search/docs/fundamentals/ai-optimization-guide
- https://naturaily.com/blog/query-fan-out-seo-and-ai-citations
- https://ppc.land/survey-of-45-studies-finds-geo-rewrites-can-cut-a-pages-ai-retrieval-16/
- https://www.lumar.io/blog/industry-news/ai-search-seo-industry-news-july-2026/
- https://www.searchenginejournal.com/ai-mode-queries-are-3x-longer-the-case-for-leading-with-the-answer/585990/