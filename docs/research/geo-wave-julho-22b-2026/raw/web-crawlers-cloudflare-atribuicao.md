# Pesquisa web — Crawlers de IA, Cloudflare e atribuição (22/07/2026)

Fonte: subagente de pesquisa web com fontes primárias; rótulos [CONFIRMADO]/[SECUNDÁRIO].

## 1. Crawlers oficiais (treino × busca/citação × ação de usuário)

### OpenAI [CONFIRMADO — developers.openai.com/api/docs/bots, acess. 22/07/2026]
| Bot | Propósito | robots.txt |
|---|---|---|
| GPTBot (GPTBot/1.4) | TREINO | Respeita; desautorizar = fora do treino |
| OAI-SearchBot (OAI-SearchBot/1.4) | BUSCA/CITAÇÃO (ChatGPT Search) | Respeita; bloquear = fora das respostas de busca |
| ChatGPT-User (ChatGPT-User/1.0) | AÇÃO DE USUÁRIO (fetch em tempo real) | Doc oficial: regras "podem não se aplicar" |

### Anthropic [CONFIRMADO — support.claude.com art. 8896518]
| Bot | Propósito | robots.txt |
|---|---|---|
| ClaudeBot | TREINO | Respeita |
| Claude-SearchBot | BUSCA/CITAÇÃO | Respeita |
| Claude-User | AÇÃO DE USUÁRIO | RESPEITA (diferencial vs OpenAI/Perplexity) |
Verificação de IP: claude.com/crawling/bots.json

### Perplexity [CONFIRMADO — docs.perplexity.ai/guides/bots]
| Bot | Propósito | robots.txt |
|---|---|---|
| PerplexityBot | BUSCA/CITAÇÃO (doc afirma que não treina) | Respeita |
| Perplexity-User | AÇÃO DE USUÁRIO | Texto oficial: "generally ignores robots.txt rules" |

### Google [CONFIRMADO — developers.google.com/search/docs/crawling-indexing/google-common-crawlers e /appearance/ai-features]
- Google-Extended: NÃO tem user-agent próprio; é token de controle no robots.txt. Controla TREINO de futuras gerações Gemini + GROUNDING (Gemini Apps e Vertex Grounding).
- **AI Overviews e AI Mode usam o Googlebot normal** ("AI is built into Search... robots.txt directives for Googlebot is the control"). Bloquear Google-Extended NÃO remove de AIO; limitar exposição em AIO = nosnippet/data-nosnippet/max-snippet/noindex (bloquear Googlebot sacrifica a busca inteira).
- Google-CloudVertexBot: crawls a pedido do dono do site (Vertex AI Agents).

### Matriz robots.txt "citação sem ceder treino" (derivada das docs)
```
User-agent: GPTBot
Disallow: /
User-agent: ClaudeBot
Disallow: /
User-agent: Google-Extended
Disallow: /
# Allow: OAI-SearchBot, ChatGPT-User, Claude-SearchBot, Claude-User,
#        PerplexityBot, Perplexity-User, Googlebot
```
Ressalvas: ChatGPT-User e Perplexity-User podem ignorar robots.txt (doc oficial); Google-Extended bloqueado também corta grounding do Gemini, não só treino.

## 2. Cloudflare 2025-2026
- 01/07/2025: bloqueio default de AI crawlers p/ novos domínios + Pay Per Crawl beta [CONFIRMADO — changelog developers.cloudflare.com/changelog/2025-07-01-pay-per-crawl/].
- AI Crawl Control (ex-AI Audit): allow/block por crawler, conformidade robots.txt, todos os planos [CONFIRMADO].
- Content Signals Policy (24/09/2025): robots.txt estendido com `search` (exclui resumos de IA), `ai-input` (RAG/grounding), `ai-train`; sintaxe `Content-Signal: search=yes, ai-train=no`; aplicado a 3,8M+ domínios; reserva de direitos Art. 4 Diretiva UE 2019/790 [CONFIRMADO — blog.cloudflare.com/content-signals-policy/].
- 01/07/2026: a partir de 15/09/2026, novos domínios bloqueiam Training e Agent em páginas com anúncios (Search permitido); crawlers multi-propósito (Googlebot, Applebot, BingBot nomeados) tratados "por todos os seus comportamentos". Cloudflare à frente de >20% dos domínios [CONFIRMADO — blog.cloudflare.com/content-independence-day-ai-options/].
- Pay Per Crawl → Pay Per Use (jul/2026): publisher pago quando o conteúdo É USADO na resposta; parceiros Ceramic.ai e You.com [SECUNDÁRIO — TechCrunch/Forbes 01/07/2026].
- Cloudflare vs Perplexity (04/08/2025) [CONFIRMADO — blog oficial]: crawling furtivo (UA imitando Chrome/macOS, rotação de IP/ASN, robots ignorado; 20-25M req/dia declaradas + 3-6M furtivas); delistagem como bot verificado. Resposta Perplexity [SECUNDÁRIO]: atribuição errada de tráfego da BrowserBase; fetches são agente de usuário, sem storage/treino.

## 3. Estatísticas de bots
[CONFIRMADO — Cloudflare "From Googlebot to GPTBot" 01/07/2025, dados mai/2025]: share AI crawlers: GPTBot 30%, ClaudeBot 21%, Meta-ExternalAgent 19%, Amazonbot 11%, Bytespider 7,2%. Top-20 geral: Googlebot 50%, Bingbot 8,7%, GPTBot 7,7%. Crescimento a/a: GPTBot +305%, ClaudeBot −46%, Bytespider −85%. Só 14% dos top-10k domínios tinham diretivas de IA.
Crawl-to-referral: [CONFIRMADO — blog "The crawl before the fall", semana 19-26/jun/2025] Anthropic ~70.900:1; Mistral ~0,1:1. [SECUNDÁRIO — via Radar AI Insights 2026]: Anthropic ~4.580:1, OpenAI ~848:1, Perplexity ~186:1, Google ~5:1 (conferir em radar.cloudflare.com/ai-insights antes de publicar).
Panorama 2026 [SECUNDÁRIO]: bots 57,5% do tráfego HTML (Prince/Radar 03/06/2026); jun/2026 ClaudeBot ~20% do AI crawl (+66%); treino ~47-52% das requisições; Imperva 2026: bots 53% do tráfego web 2025. Vercel [CONFIRMADO, dados 2024/25]: GPTBot 569M req/mês, Claude 370M (~20% do Googlebot 4,5B).

## 4. Atribuição
- **GA4 canal nativo "AI Assistants"** [CONFIRMADO — support.google.com/analytics/answer/9756891]: sources tipo ChatGPT, Gemini, Deepseek, Copilot, Grok; medium `ai-assistant` automático; **EXCLUI AI Overviews e AI Mode** (continuam como Organic Search); **Perplexity fora da lista** → canal customizado com regex segue necessário. Lançamento reportado 13/05/2026 [SECUNDÁRIO].
- Regex de mercado [SECUNDÁRIO]: `chatgpt.com|claude.ai|perplexity.ai|gemini.google.com|copilot.microsoft.com|grok.com|meta.ai|you.com|poe.com`; regra no topo; não retroage.
- **Dark traffic**: Loamly (446.405 visitas): **70,6% do tráfego de IA chega sem referrer** (Direct); conversão do dark AI 10,21% vs 2,46% não-IA [SECUNDÁRIO — vendor]. Seer Interactive: conversão Perplexity 10,5%, ChatGPT 15,9% vs 1,76% Google Organic em B2B [SECUNDÁRIO].
- Logs de servidor: GA4 só vê humanos que clicam; crawl de IA só em logs/CDN; validar IP contra listas oficiais (ex.: claude.com/crawling/bots.json); razão crawl-to-referral própria = req de bots nos logs ÷ sessões referidas.

## Não encontrado
Relatório primário Fastly 2026; post primário Cloudflare com termos do Pay Per Use.

## Fontes primárias
developers.openai.com/api/docs/bots · support.claude.com art. 8896518 · docs.perplexity.ai/guides/bots · developers.google.com/search/docs/crawling-indexing/google-common-crawlers · developers.google.com/search/docs/appearance/ai-features · support.google.com/analytics/answer/9756891 · blog.cloudflare.com/ai-search-crawl-refer-ratio-on-radar/ · blog.cloudflare.com/from-googlebot-to-gptbot-whos-crawling-your-site-in-2025/ · developers.cloudflare.com/changelog/2025-07-01-pay-per-crawl/ · blog.cloudflare.com/content-signals-policy/ · blog.cloudflare.com/perplexity-is-using-stealth-undeclared-crawlers-to-evade-website-no-crawl-directives/ · blog.cloudflare.com/content-independence-day-ai-options/ · developers.cloudflare.com/ai-crawl-control/ · radar.cloudflare.com/ai-insights · vercel.com/blog/the-rise-of-the-ai-crawler

## Fontes secundárias
techcrunch.com/2026/07/01/... · forbes.com/sites/sandycarter/2026/07/01/... · sdxcentral.com (resposta Perplexity) · research.contrary.com (dossiê) · seomator.com (ratios 2026) · digitalapplied.com (stats 2026) · loamly.ai (dark traffic) · scaleandprosper.com (regex GA4) · discoveredlabs.com (tracking) · searchenginejournal.com (docs Anthropic/Google-Extended)
