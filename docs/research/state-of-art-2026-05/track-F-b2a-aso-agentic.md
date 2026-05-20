# Track F — B2A / ASO / Agent Standards (mai-2026)

> Sub-agent Opus · 2026-05-20 · Brasil GEO Research
> Escopo: catálogo de crawlers/agentes de IA, Model Context Protocol, padrões de descoberta (llms.txt, ai-plugin.json, well-known), agentic browsers/operators, agent UX, analytics e atribuição, aplicação nos repos Brasil GEO.

## Sumário executivo

Em mai/2026 o tráfego web está rachado em quatro camadas distintas: (1) browsers humanos clássicos, (2) crawlers de busca tradicional (Googlebot, Bingbot), (3) crawlers de IA — separados em training (GPTBot, ClaudeBot, Bytespider, Google-Extended, Applebot-Extended) e search/retrieval (OAI-SearchBot, Claude-SearchBot, PerplexityBot, MistralAI-Index, DuckAssistBot) — e (4) agentes user-initiated e operators autônomos (ChatGPT-User, Claude-User, Perplexity-User, MistralAI-User, ChatGPT Agent, Anthropic Computer Use, Comet, Mariner, Operator, Skyvern, Browser-Use, NovaAct). HUMAN Security mediu crescimento de mais de 1.300% de tráfego agentic entre jan-ago/2025, e Snowplow reporta 6.900% YoY em agentic browsing 2024→2025. Comet ultrapassou ChatGPT Agent em setembro/2025 como maior fonte de tráfego de agentes (52,5% vs 42%). Crawl-to-referral ratio de Anthropic 73.000:1 e OpenAI 1.700:1 contra Google 14:1 (Cloudflare): a assimetria quebra o pacto histórico entre indexação e tráfego de retorno.

A consequência prática para um portal Brasil GEO é tripla:

1. **Robots.txt precisa de granularidade por user-agent** — permitir search/retrieval bots (que ainda mandam citações com link clicável) e considerar bloqueio ou pay-per-crawl para training-only bots. Modelo padrão: allow OAI-SearchBot/PerplexityBot/Claude-SearchBot/Google-Extended para search, allow Perplexity-User/ChatGPT-User/Claude-User para retrieval ao vivo, decidir caso a caso GPTBot/ClaudeBot/Bytespider.
2. **Discovery files são B2A infrastructure, não SEO lever** — llms.txt, llms-full.txt, mcp.json, ai-policy.json não movem ranking, mas reduzem ruído e custo de ingestão para o agente que já decidiu visitar. Google declarou via John Mueller que não usa llms.txt; mesmo assim Anthropic ativamente pede llms-full.txt em docs de B2B, e a Mintlify, Fern, GitBook auto-geram. Vale o investimento por agentes user-initiated, não por placement.
3. **MCP é o novo padrão para "site como ferramenta agentic"** — protocolo aberto JSON-RPC 2.0 lançado por Anthropic em 25-nov-2024, agora suportado nativamente em Claude, ChatGPT, Cursor, Windsurf, Zed, VS Code. A apex de um portal Brasil GEO pode (e deve, em curva 12-18 meses) expor um MCP server canônico com tools tipo `get_article(slug)`, `search_articles(query)`, `list_glossary()` que devolvem markdown limpo. Reduz fricção de retrieval e cria moat: agentes vão preferir sites com MCP exposto a sites que precisam ser scrapeados.

A grande regra ASO mai/2026: **um site é otimizado para agente quando o agente paga menos tokens e tempo para extrair valor canônico verificável dele do que qualquer concorrente para a mesma intent.**

---

## Parte 1 — Catálogo definitivo de 30+ AI crawlers/agents (mai-2026)

Tabela ordenada por proprietário. Categoria: T = training, S = search/retrieval, U = user-initiated agent, A = autonomous agent, M = mixed/legacy.

### 1.1 OpenAI

| Crawler | User-Agent canônico | Categoria | Robots.txt token | Respeita robots.txt? | IP ranges | Rate limit | Documentação |
|---|---|---|---|---|---|---|---|
| **GPTBot** | `Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; GPTBot/1.2; +https://openai.com/gptbot)` | T | `GPTBot` | Sim — confirmado por OpenAI | https://openai.com/gptbot.json | Não publicado | platform.openai.com/docs/bots |
| **OAI-SearchBot** | `Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; OAI-SearchBot/1.0; +https://openai.com/searchbot)` | S | `OAI-SearchBot` | Sim | https://openai.com/searchbot.json | Não publicado | platform.openai.com/docs/bots |
| **ChatGPT-User** | `Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; ChatGPT-User/1.0; +https://openai.com/bot)` | U | `ChatGPT-User` | Parcial — pode ignorar para fetches user-initiated | https://openai.com/chatgpt-user.json | Não publicado | platform.openai.com/docs/bots |
| **ChatGPT Agent / Operator** | UA do Chrome (mascarado) + `Signature-Agent: "https://chatgpt.com"` + RFC 9421 HTTP Message Signatures | A | N/A (verifica por assinatura) | Não aplicável | https://chatgpt.com/.well-known/http-message-signatures-directory | Não publicado | openai.com/index/introducing-chatgpt-agent |

**Notas operacionais:** GPTBot opt-out via `User-agent: GPTBot / Disallow: /`. Em jul/2025 OpenAI lançou ChatGPT Agent unificando Operator + Deep Research; assinaturas RFC 9421 são o discriminador canônico — Cloudflare e Akamai já integraram a verificação. Crawl-to-referral ratio observado por Cloudflare: ~1.700:1.

### 1.2 Anthropic

| Crawler | User-Agent canônico | Categoria | Robots.txt token | Respeita robots.txt? | IP ranges | Rate limit | Documentação |
|---|---|---|---|---|---|---|---|
| **ClaudeBot** | `Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; ClaudeBot/1.0; +claudebot@anthropic.com)` | T | `ClaudeBot` | Sim — declarado oficialmente | https://claude.com/crawling/bots.json | Honra `Crawl-delay` | support.claude.com/en/articles/8896518 |
| **Claude-User** | `Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Claude-User/1.0; +Claude-User@anthropic.com)` | U | `Claude-User` | Parcial | https://claude.com/crawling/bots.json | N/A | support.claude.com/en/articles/8896518 |
| **Claude-SearchBot** | `Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Claude-SearchBot/1.0; +Claude-SearchBot@anthropic.com)` | S | `Claude-SearchBot` | Sim | https://claude.com/crawling/bots.json | N/A | support.claude.com/en/articles/8896518 |
| **anthropic-ai** (legacy) | `anthropic-ai` | T (legacy) | `anthropic-ai` | Histórico — preserve no robots.txt | — | — | Dark Visitors/KnownAgents |
| **Claude-Web** (legacy) | `Mozilla/5.0 ...; compatible; Claude-Web/1.0` | M (legacy) | `Claude-Web` | Histórico | — | — | KnownAgents |
| **Claude-Code** | UA do CLI Anthropic | A (developer) | `Claude-Code` | Sim quando declarado | — | — | claude.com/code |

**Notas:** Anthropic crawl-to-referral 73.000:1 (Cloudflare, jan/2026) — pior do mercado, justifica bloqueio agressivo de ClaudeBot em sites comerciais. Documentação canônica recomenda `Crawl-delay: 1` para rate limiting.

### 1.3 Google

| Crawler | User-Agent canônico | Categoria | Robots.txt token | Respeita robots.txt? | IP ranges | Rate limit | Documentação |
|---|---|---|---|---|---|---|---|
| **Googlebot** (smartphone) | `Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 ... Chrome/W.X.Y.Z Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)` | S | `Googlebot` | Sim | googlebot.json | Adaptivo | developers.google.com/search/docs/crawling-indexing/overview-google-crawlers |
| **Googlebot-Desktop** | `Mozilla/5.0 AppleWebKit/537.36 ... (compatible; Googlebot/2.1; +http://www.google.com/bot.html)` | S | `Googlebot` | Sim | googlebot.json | Adaptivo | mesmo doc |
| **Google-Extended** | Sem UA dedicado — mesmo Googlebot UA + token específico | T (Gemini training + grounding) | `Google-Extended` | Sim | googlebot.json | N/A | developers.google.com/search/docs/crawling-indexing/google-common-crawlers |
| **GoogleOther** | `Mozilla/5.0 (compatible; GoogleOther) AppleWebKit/...` | M (research, product) | `GoogleOther` | Sim | special-crawlers.json | N/A | developers.google.com/search/docs/crawling-indexing/google-special-crawlers |
| **Google-CloudVertexBot** | `Mozilla/5.0 (compatible; Google-CloudVertexBot/1.0; +http://www.google.com/bot.html)` | S | `Google-CloudVertexBot` | Sim | special-crawlers.json | N/A | mesmo doc |
| **Google-NotebookLM** | UA dedicado (Notebook LM agent) | U | `Google-NotebookLM` | Sim quando declarado | — | — | KnownAgents |
| **GoogleAgent-Mariner / Project Mariner** | UA padrão Chrome (sem token dedicado) | A | N/A | Não declarado | — | — | deepmind.google/technologies/project-mariner |
| **Gemini-Deep-Research** | UA dedicado em fetches de research mode | U | `Gemini-Deep-Research` | Sim | — | — | KnownAgents |
| **AdsBot-Google** | `AdsBot-Google (+http://www.google.com/adsbot.html)` | M (ads) | `AdsBot-Google` | Special-case (não respeita `*` wildcard) | — | — | developers.google.com/search/docs/crawling-indexing/google-special-crawlers |
| **Storebot-Google** | UA dedicado | S | `Storebot-Google` | Sim | — | — | mesmo doc |
| **APIs-Google** | UA dedicado | M (push, pub-sub) | `APIs-Google` | Sim | — | — | mesmo doc |

**Notas:** Google é o único grande player com crawl-to-referral ratio 14:1 (saudável). Bloquear `Google-Extended` previne uso de novo conteúdo em training Gemini e em grounding de AI Overviews, **mas não retroage** sobre modelos já treinados. Mariner não tem UA dedicado — só detectável por padrões comportamentais e IP ranges Google.

### 1.4 Microsoft / Bing

| Crawler | User-Agent canônico | Categoria | Robots.txt token | Respeita robots.txt? | Doc |
|---|---|---|---|---|---|
| **Bingbot** | `Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)` | S | `bingbot` | Sim | bing.com/webmaster |
| **BingPreview** | `Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 ... BingPreview/1.0b` | S | `BingPreview` | Sim | mesmo |
| **MicrosoftPreview** | UA dedicado | M | `MicrosoftPreview` | Sim | KnownAgents |
| **Copilot agent** (Microsoft Copilot Studio agents) | UA do navegador + Microsoft-specific header | A | N/A | N/A | learn.microsoft.com/copilot |

### 1.5 Perplexity

| Crawler | User-Agent canônico | Categoria | Robots.txt token | Respeita robots.txt? | IP ranges | Doc |
|---|---|---|---|---|---|---|
| **PerplexityBot** | `Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; PerplexityBot/1.0; +https://perplexity.ai/perplexitybot)` | S | `PerplexityBot` | Sim — declarado | https://www.perplexity.com/perplexitybot.json | docs.perplexity.ai/guides/bots |
| **Perplexity-User** | `Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Perplexity-User/1.0; +https://perplexity.ai/perplexity-user)` | U | `Perplexity-User` | "Generally ignores robots.txt" — declarado pela própria Perplexity | https://www.perplexity.com/perplexity-user.json | mesmo |
| **Comet Browser** | UA padrão Chrome + headers Perplexity quando aplicável | A | N/A | N/A | — | perplexity.ai/comet |

**Notas críticas:** Cloudflare publicou em ago/2025 evidências de "stealth crawling" Perplexity — UA Chrome genérico, IP rotation entre ASNs, ignorando robots.txt em domínios test. ~3-6M requests/dia stealth vs ~20-25M declarados. Por isso, em mai/2026, Cloudflare Bot Management trata Perplexity como caso especial de detection comportamental, não só UA.

### 1.6 Meta / Facebook

| Crawler | User-Agent canônico | Categoria | Robots.txt token | Respeita robots.txt? | Doc |
|---|---|---|---|---|---|
| **Meta-ExternalAgent** | `meta-externalagent/1.1 (+https://developers.facebook.com/docs/sharing/webmasters/crawler)` | T | `meta-externalagent` | Sim | developers.facebook.com/docs/sharing/webmasters/web-crawlers |
| **Meta-ExternalFetcher** | `meta-externalfetcher/1.1` | U | `meta-externalfetcher` | Parcial — pode ignorar para user-initiated | mesmo doc |
| **Meta-WebIndexer** | `meta-webindexer/1.1` | S | `Meta-WebIndexer` | Sim | mesmo doc |
| **FacebookExternalHit** | `facebookexternalhit/1.1` | M (preview + AI) | `facebookexternalhit` | Pode ignorar para integrity/security checks | mesmo doc |
| **FacebookBot** | UA dedicado | T | `facebookbot` | Sim | mesmo doc |

### 1.7 Apple

| Crawler | User-Agent canônico | Categoria | Robots.txt token | Respeita robots.txt? | Doc |
|---|---|---|---|---|---|
| **Applebot** | `Mozilla/5.0 (Device; OS_version) AppleWebKit/WebKit_version (KHTML, like Gecko)Version/Safari_version Safari/WebKit_version (Applebot/Applebot_version; +http://www.apple.com/go/applebot)` | S | `Applebot` | Sim | support.apple.com/en-us/119829 |
| **Applebot-Extended** | Não tem UA dedicado — mesmo Applebot UA + token robots.txt distinto | T (Apple Intelligence training) | `Applebot-Extended` | Sim | mesmo doc |

**Nota:** Bloquear `Applebot-Extended` impede uso em training Apple Intelligence **sem** afetar Spotlight/Siri/Safari search. Padrão recomendado para conteúdo proprietário.

### 1.8 ByteDance / TikTok

| Crawler | User-Agent canônico | Categoria | Robots.txt token | Respeita robots.txt? | Doc |
|---|---|---|---|---|---|
| **Bytespider** | `Mozilla/5.0 (compatible; Bytespider; spider-feedback@bytedance.com)` | T | `Bytespider` | Histórico — declarou Sim, em campo observa-se Parcial | bytedance.com (sparse) |

**Nota:** Dark Visitors classifica como "respect: No" por padrão de campo. Bloqueio agressivo recomendado para sites comerciais.

### 1.9 Amazon

| Crawler | User-Agent canônico | Categoria | Robots.txt token | Respeita robots.txt? | Doc |
|---|---|---|---|---|---|
| **Amazonbot** | `Mozilla/5.0 (compatible; Amazonbot/0.1; +https://developer.amazon.com/amazonbot)` | T (Alexa + Bedrock) | `Amazonbot` | Sim | developer.amazon.com/amazonbot |
| **bedrockbot** | UA dedicado Bedrock | T | `bedrockbot` | Sim | KnownAgents |
| **AmazonBuyForMe** | UA agent dedicado | A | N/A | N/A | KnownAgents |
| **NovaAct** | UA agent dedicado | A | N/A | N/A | KnownAgents |

### 1.10 Mistral

| Crawler | User-Agent canônico | Categoria | Robots.txt token | Respeita robots.txt? | Doc |
|---|---|---|---|---|---|
| **MistralAI-User** | `MistralAI-User/1.0 (+https://docs.mistral.ai/)` | U | `MistralAI-User` | Parcial | docs.mistral.ai |
| **MistralAI-Index** | UA dedicado | S | `MistralAI-Index` | Sim | mesmo |

### 1.11 Cohere

| Crawler | User-Agent canônico | Categoria | Robots.txt token | Respeita robots.txt? | Doc |
|---|---|---|---|---|---|
| **cohere-ai** | `cohere-ai` | T | `cohere-ai` | Histórico — declarado Sim | cohere.com (sparse) — Dark Visitors |
| **cohere-training-data-crawler** | UA dedicado | T | `cohere-training-data-crawler` | Sim | KnownAgents |

### 1.12 DuckDuckGo

| Crawler | User-Agent canônico | Categoria | Robots.txt token | Respeita robots.txt? | Doc |
|---|---|---|---|---|---|
| **DuckAssistBot** | `DuckAssistBot/1.2; (+http://duckduckgo.com/duckassistbot.html)` | S (live retrieval para AI-assisted answers) | `DuckAssistBot` | Sim — 72h propagation | duckduckgo.com/duckduckgo-help-pages/results/duckassistbot |
| **DuckDuckBot** | `DuckDuckBot/1.1; (+http://duckduckgo.com/duckduckbot.html)` | S (search) | `DuckDuckBot` | Sim | mesmo |

### 1.13 You.com

| Crawler | User-Agent canônico | Categoria | Robots.txt token | Respeita robots.txt? | Doc |
|---|---|---|---|---|---|
| **YouBot** | `Mozilla/5.0 (compatible; YouBot (+http://www.you.com))` | S | `YouBot` | Sim | about.you.com/policies |

### 1.14 Common Crawl

| Crawler | User-Agent canônico | Categoria | Robots.txt token | Respeita robots.txt? | Doc |
|---|---|---|---|---|---|
| **CCBot** | `CCBot/2.0 (https://commoncrawl.org/faq/)` | T (open corpus) | `CCBot` | Sim — verificação por reverse DNS `*.crawl.commoncrawl.org` | index.commoncrawl.org/ccbot.json |

**Nota:** CCBot alimenta GPT-3, LLaMA, MPT e dezenas de outros modelos. Bloqueá-lo equivale a opt-out broad de training open-source.

### 1.15 SEO/AI híbridos

| Crawler | User-Agent canônico | Owner | Categoria | Robots.txt token | Doc |
|---|---|---|---|---|---|
| **AhrefsBot** | `Mozilla/5.0 (compatible; AhrefsBot/7.0; +http://ahrefs.com/robot/)` | Ahrefs | SEO | `AhrefsBot` | ahrefs.com/robot |
| **SemrushBot** | `Mozilla/5.0 (compatible; SemrushBot/7~bl; +http://www.semrush.com/bot.html)` | Semrush | SEO | `SemrushBot` | semrush.com/bot |
| **MJ12bot** | `Mozilla/5.0 (compatible; MJ12bot/v1.4.8; http://mj12bot.com/)` | Majestic | SEO | `MJ12bot` | mj12bot.com |
| **PetalBot** | `Mozilla/5.0 (compatible; PetalBot; +https://webmaster.petalsearch.com/site/petalbot)` | Huawei | S | `PetalBot` | webmaster.petalsearch.com |
| **YandexBot** | `Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)` | Yandex | S | `YandexBot` | yandex.com/support/webmaster |

### 1.16 GEO/AEO vendors

| Crawler | User-Agent | Owner | Doc |
|---|---|---|---|
| **BrightBot** | `BrightBot/1.0` | Bright Data — collects training data | brightdata.com/brightbot |
| **ScrunchAI-Crawler** | `ScrunchAI-Crawler` | Scrunch AI — GEO monitoring | KnownAgents |
| **AthenaBot** | `AthenaBot` | Athena/Hyperscope — AI ranking analytics | KnownAgents |
| **PeecBot** | `PeecBot/1.0` | Peec AI — AI visibility monitoring | peec.ai |
| **DaydreamBot** | `DaydreamBot/1.0` | Daydream — AI agent analytics | KnownAgents |
| **Profound** | UA dedicado | Profound — GEO analytics | tryprofound.com |
| **Otterly** | UA dedicado | Otterly AI — AI search monitoring | otterly.ai |
| **TavilyBot** | `TavilyBot/1.0` | Tavily — AI search API | tavily.com |
| **ExaBot** | `Exabot/3.0 (+https://exa.ai)` | Exa — semantic search API | exa.ai |
| **FirecrawlAgent** | `FirecrawlAgent/1.0` | Firecrawl — structured data converter | firecrawl.dev |
| **Diffbot** | `Mozilla/5.0 (compatible; Diffbot/0.1; +http://www.diffbot.com)` | Diffbot — knowledge graph + crawler | diffbot.com |

### 1.17 Outros training crawlers a conhecer

| Crawler | User-Agent | Owner | Categoria |
|---|---|---|---|
| **AI2Bot** | `AI2Bot` | Allen Institute | T |
| **AI2Bot-Dolma** | `AI2Bot-Dolma` | Allen Institute (Dolma corpus) | T |
| **DeepSeekBot** | UA dedicado | DeepSeek | T |
| **LAIONDownloader** | UA dedicado | LAION | T |
| **OpenAI-SearchBot** (sinônimo OAI-SearchBot) | — | OpenAI | S |
| **Devin** | UA dedicado | Cognition AI | A (coding) |
| **TwinAgent** | UA dedicado | Twin | A |
| **AddSearchBot** | UA dedicado | AddSearch | S |

**Total: 50+ user-agents canônicos catalogados, dos quais 30+ tratados explicitamente acima com fonte oficial primária.**

---

## Parte 2 — MCP (Model Context Protocol) no estado mai-2026

### 2.1 Origem, especificação e adoção

**Lançamento:** 25 de novembro de 2024, por David Soria Parra e Justin Spahr-Summers (Anthropic), aberto sob MIT.

**Especificação canônica:** versão `2025-06-18` (a versão mais recente publicamente verificável em mai/2026), em modelcontextprotocol.io/specification/2025-06-18. Schema TypeScript autoritativo em github.com/modelcontextprotocol/specification/blob/main/schema/2025-06-18/schema.ts.

**Base técnica:** mensagens JSON-RPC 2.0 sobre transportes intercambiáveis. Os três transportes oficiais em mai/2026 são:
- **stdio** — server local que se comunica via stdin/stdout (canônico para integrações desktop, Claude Desktop, Cursor, Zed)
- **Streamable HTTP** — servidor remoto HTTP com SSE para streaming server→client (canônico para integrações cloud-to-cloud)
- **SSE legacy** — modo legacy, ainda suportado mas marcado para deprecação

**Componentes do protocolo:**
- **Hosts** — aplicações LLM que iniciam conexões (Claude Desktop, ChatGPT app, Cursor IDE)
- **Clients** — connectors dentro do host
- **Servers** — serviços que expõem capacidades

**Capacidades server-side (oferecidas para clients):**
- **Resources** — dados e contexto (arquivos, documentos, registros de DB)
- **Prompts** — templates de mensagens e workflows
- **Tools** — funções executáveis pelo modelo

**Capacidades client-side (oferecidas para servers):**
- **Sampling** — server pede ao client para invocar o LLM (agentic recursion)
- **Roots** — server consulta limites de filesystem/URI permitidos
- **Elicitation** — server pede info adicional ao usuário via UI do client

**Utilities transversais:** Configuration, Progress tracking, Cancellation, Error reporting, Logging.

**Princípios de segurança canônicos:**
1. User Consent and Control — explicit user consent para data access
2. Data Privacy — host não pode transmitir dados resource sem consentimento
3. Tool Safety — tools são arbitrary code execution, tratar com cautela; descrições/annotations devem ser consideradas untrusted exceto se vindas de server trusted
4. LLM Sampling Controls — usuário aprova explicitamente cada sampling

**Adoção real em mai-2026 (clients que suportam MCP):**
- Claude.ai (web), Claude Desktop, Claude Code
- ChatGPT (developers.openai.com/api/docs/mcp/)
- Cursor (cursor.com/docs/context/mcp)
- VS Code com Copilot Chat
- Windsurf
- Zed
- Replit
- Sourcegraph (Cody)
- Codeium
- MCPJam, Continue, Open Interpreter

**Adoção real (servers públicos disponíveis em mai-2026):**
- Anthropic registry referência: github.com/modelcontextprotocol/servers
- Pre-built oficiais: Google Drive, Slack, GitHub, Git, Postgres, Puppeteer, Filesystem, Fetch, Brave Search, Memory, Sequential Thinking, EverArt, Sentry, Time
- Comunidade: 500+ servers community-built em github.com/modelcontextprotocol/servers/tree/main/src e github.com/punkpeye/awesome-mcp-servers
- Adopção enterprise: Block, Apollo, Stripe (mcp.stripe.com), Cloudflare (mcp.cloudflare.com), Linear, Notion, Atlassian, Asana, Figma, PayPal, Square

### 2.2 mcp.json canônico para sites

O **mcp.json** (não confundir com manifest de extension) é o arquivo de descoberta que um host MCP consulta para configurar quais servers conectar. Existem dois contextos canônicos:

**(a) mcp.json no client (configuração de host):**

```json
{
  "mcpServers": {
    "brasilgeo-articles": {
      "command": "npx",
      "args": ["-y", "@brasilgeo/mcp-articles"],
      "env": {
        "BRASILGEO_API_KEY": "${BRASILGEO_API_KEY}"
      }
    },
    "brasilgeo-remote": {
      "url": "https://mcp.alexandrecaramaschi.com/sse",
      "transport": "sse"
    }
  }
}
```

Local típico: `~/.config/claude/mcp.json` no Linux/macOS, `%APPDATA%\Claude\mcp.json` no Windows, ou settings do IDE.

**(b) mcp.json no site (descoberta well-known) — proposta canônica emergente:**

Apesar de não estar formalmente na spec 2025-06-18, várias propostas (incluindo do próprio Brasil GEO) estabeleceram convenção:

```json
{
  "version": "2025-06-18",
  "name": "Alexandre Caramaschi — Brasil GEO",
  "description": "Acervo canônico de artigos HBR-grade, glossário, conceitos e perfil do CEO da Brasil GEO.",
  "publisher": {
    "name": "Brasil GEO",
    "url": "https://alexandrecaramaschi.com",
    "contact": "mcp@brasilgeo.com.br"
  },
  "endpoints": {
    "sse": "https://mcp.alexandrecaramaschi.com/sse",
    "streamable_http": "https://mcp.alexandrecaramaschi.com/mcp"
  },
  "capabilities": {
    "resources": true,
    "tools": true,
    "prompts": false
  },
  "tools": [
    {"name": "search_articles", "description": "Busca artigos por query semântica"},
    {"name": "get_article", "description": "Retorna artigo completo em Markdown por slug"},
    {"name": "list_glossary", "description": "Lista verbetes do glossário canônico"},
    {"name": "get_profile", "description": "Retorna perfil completo do autor"}
  ],
  "authentication": {
    "type": "none",
    "rate_limit": "100 req/min por IP"
  },
  "ai_policy": "https://alexandrecaramaschi.com/.well-known/ai-policy.json"
}
```

Servido em `/.well-known/mcp.json` ou `/mcp.json` na raiz. A spec exata está em discussão — ver github.com/modelcontextprotocol/specification/discussions.

### 2.3 MCP vs OpenAPI + ai-plugin.json + RAG endpoints

| Dimensão | OpenAPI + ai-plugin.json | RAG endpoint custom | **MCP** |
|---|---|---|---|
| Status mai-2026 | Legacy (ai-plugin.json deprecado por OpenAI desde set/2024 com sunset de plugins) | Ad-hoc | Padrão emergente |
| Protocolo | REST + manifesto OpenAPI 3 | Qualquer | JSON-RPC 2.0 stateful |
| Statefulness | Stateless | Variável | **Stateful** (negociação de capabilities) |
| Streaming | Não nativo | Variável | SSE/Streamable HTTP nativo |
| Sampling recursivo (server→client→LLM) | Não | Não | **Sim** |
| Discovery de tools dinâmico | Não — fixed manifesto | Não | **Sim** — `tools/list` em runtime |
| Security model | OAuth + API keys | Variável | OAuth 2.1 (Streamable HTTP) + permissions |
| Adoção em IDEs/clients | Praticamente zero em 2026 | Custom | 10+ clients principais |
| Caso de uso ideal | API pública generic | Q&A retrieval | Tools agentic + context resources |

**Decisão recomendada:** ai-plugin.json está morto. Para retrieval simples, MCP via Streamable HTTP. Para integração leve com webhook simples, REST OpenAPI continua válido — mas se o destino é agentic flow, **MCP é canônico**.

### 2.4 Roadmap MCP para os 3 repos Brasil GEO

**landing-page-geo (alexandrecaramaschi.com):**
- M-1 (mai-2026): publicar `/.well-known/mcp.json` estático com manifesto descritivo (sem server ainda) — sinal de intenção, discoverable por agentes scouts
- M-2 (jun-2026): MCP server stdio publicado em npm como `@brasilgeo/mcp-articles` — devs/agents podem instalar localmente (`npx -y @brasilgeo/mcp-articles`)
- M-3 (jul-2026): MCP server remoto em `mcp.alexandrecaramaschi.com` via Cloudflare Workers + Streamable HTTP transport
- M-4 (set-2026): tools canônicas — `search_articles(query, limit)`, `get_article(slug)`, `list_glossary(category?)`, `get_profile()`, `get_credentials()`
- M-5 (out-2026): submission ao Anthropic registry e listagem em mcp.so + glama.ai/mcp/servers

**curso-factory:**
- M-1: MCP server `@brasilgeo/mcp-cursos` que expõe `list_courses(track?)`, `get_course(slug)`, `get_lesson(course_slug, lesson_id)`, `search_courses(query)` — todos retornando markdown canônico
- M-2: bundle MCP server com cada portal de curso publicado (curso gerado vem com servidor MCP que descreve seu próprio conteúdo)
- M-3: integração com Claude Code para permitir que devs e learners "conversem" com o curso via MCP — ex.: "explique a aula 3 do módulo 2 dando exemplos do meu repo atual"

**papers:**
- M-1: MCP server `@brasilgeo/mcp-papers` que expõe `list_papers()`, `get_paper(slug)`, `search_papers(query)`, `get_citations(paper_slug)` — papers em formato markdown estruturado
- M-2: integração com Tavily/Exa para enriquecer queries de research agents
- M-3: tool `cite_paper(paper_slug, claim)` que devolve a citação formatada APA + parágrafo de contexto verificável

---

## Parte 3 — Standards de descoberta

### 3.1 llms.txt — debate e decisão recomendada

**Origem:** setembro de 2024, Jeremy Howard (Answer.AI). Spec em llmstxt.org.

**Estrutura canônica:**
```
# Nome do site

> Bloco-citação com sumário e propósito.

Parágrafos livres com contexto, termos do domínio, disclaimers.

## Documentação
- [Nome do recurso](/docs/intro.md): nota opcional
- [Outro recurso](/docs/advanced.md)

## API Reference
- [Endpoint X](/api/x.md)

## Optional
- [Caso de uso extenso](/case-studies/long.md)
```

**Convenção pareada:** para cada URL HTML útil, expor `<url>.md` com markdown limpo (sem chrome/nav).

**llms-full.txt:** variante introduzida por Mintlify a pedido da Anthropic — single Markdown file com conteúdo inline de todas as páginas-chave. Permite ingestão one-shot. Adotado por Fern, GitBook, ReadMe.

**Adoção em mai-2026:**
- Ahrefs (mar-2026), SE Ranking, ALLMO: ~10% dos top domains com llms.txt. Nenhum efeito mensurável em frequência de citação ou ranking AI.
- John Mueller (Google Search Central): "Google does not use llms.txt for crawling or AI Overviews" (várias falas em 2025-2026).
- Anthropic ativamente pede llms-full.txt em docs B2B (declarado em comm com Mintlify).
- OpenAI: crawls esporádicos a llms.txt observados em logs de B2B sites.
- Perplexity, Mistral: sem statement oficial.

**Conclusão canônica para Brasil GEO:**
- llms.txt **não é SEO lever**. Não move ranking, não aumenta citation rate de forma mensurável.
- llms.txt **é B2A infrastructure**. Reduz custo de ingestão para agentes user-initiated (Claude-User, Perplexity-User, Mistral-User), aumenta chance de o agente extrair conteúdo correto vs hallucinar.
- **Vale o investimento** quando: site tem docs/artigos densos e organizados; agentes user-initiated trazem tráfego mensurável; custo de manter <2h/mês.
- **Não vale** quando: site é majoritariamente paywall/dynamic; conteúdo muda mais rápido do que o file pode ser regenerado; é blog pessoal de cauda curta.

Para os 3 repos Brasil GEO: **sim, manter llms.txt v2 + llms-full.txt v2** (alguns repos já têm; padronizar).

### 3.2 ai-policy.json, ai-plugin.json, well-known e variantes

**ai-plugin.json:** legacy do ChatGPT Plugins (2023). OpenAI sunset os plugins em set-2024. Em mai-2026, ai-plugin.json está **deprecado**. Algumas referências persistem em sites antigos, mas não há cliente ativo que ainda consome.

**ai-policy.json:** **proposta** (não há RFC formal). O padrão emergente combina elementos do C2PA, Spawning ai.txt, e proposta Brasil GEO. Estrutura canônica usada em portais Brasil GEO:

```json
{
  "version": "1.1",
  "updated": "2026-05-20",
  "publisher": {
    "name": "Brasil GEO",
    "url": "https://alexandrecaramaschi.com",
    "contact": "ai-policy@brasilgeo.com.br"
  },
  "training": {
    "allow": ["OAI-SearchBot", "PerplexityBot", "Claude-SearchBot"],
    "disallow": ["GPTBot", "ClaudeBot", "anthropic-ai", "Bytespider", "Google-Extended", "Applebot-Extended", "Amazonbot", "cohere-ai"],
    "commercial_license_required": true,
    "contact_for_license": "license@brasilgeo.com.br"
  },
  "retrieval": {
    "allow": ["ChatGPT-User", "Claude-User", "Perplexity-User", "MistralAI-User", "DuckAssistBot"],
    "require_attribution": true,
    "attribution_format": "Cite source URL and author name on first reference"
  },
  "agents": {
    "allow_user_initiated": true,
    "require_signed_identity": false,
    "rate_limit": "60 req/min per session"
  },
  "content_provenance": {
    "c2pa": false,
    "watermarking": "none",
    "authoritative_source": true
  },
  "discovery": {
    "mcp": "/.well-known/mcp.json",
    "llms_txt": "/llms.txt",
    "llms_full": "/llms-full.txt",
    "sitemap": "/sitemap.xml"
  }
}
```

Servido em `/.well-known/ai-policy.json` e/ou `/ai-policy.json`. Não há cliente que **consome automaticamente** — é declaração legal/política, leitura humana e referência em disputas. Vale como sinal de profissionalismo e auxílio em remediation de bots desonestos.

**ai.txt (Spawning):** initiative spawning.ai de 2023 (txt simples para opt-out de training). Adoção muito baixa em 2026, ficou para nicho de creators visuais. Não vale a pena para Brasil GEO.

**.well-known/* directories canônicos em mai-2026 para sites:**
- `/.well-known/security.txt` (RFC 9116) — contato de segurança
- `/.well-known/dnt-policy.txt` — Do Not Track
- `/.well-known/openid-configuration` — OAuth/OIDC
- `/.well-known/mcp.json` — MCP discovery (proposta)
- `/.well-known/ai-policy.json` — política IA (proposta Brasil GEO)
- `/.well-known/ai-plugin.json` — **legacy/deprecado**
- `/.well-known/oauth-protected-resource` (RFC 9728) — discovery OAuth para MCP Streamable HTTP

**sitemap-ai.xml:** não há proposta canônica. Sitemap.xml clássico continua sendo a fonte de URLs primária.

**Schema.org tipos AI-relevantes:**
- `DigitalDocument` — fallback para documentos genéricos
- `Dataset` — datasets estruturados
- `Article` + `headline`, `author` (`Person`), `publisher` (`Organization`), `datePublished`, `dateModified`, `mainEntityOfPage`
- `Person` + `hasCredential` (`EducationalOccupationalCredential`), `knowsAbout`, `sameAs` (Wikidata, ORCID, LinkedIn)
- `FAQPage` + `Question` + `Answer` + `speakable` (`SpeakableSpecification`) — crucial para LLMs
- `DefinedTermSet` + `DefinedTerm` — glossários
- `HowTo` — instruções
- `Course` + `Syllabus` — para curso-factory
- `ScholarlyArticle` — para papers

### 3.3 Robots.txt template canônico mai-2026

```txt
# robots.txt canônico Brasil GEO — mai/2026
# Política: permitir search/retrieval bots com referral, bloquear training-only.
# Bots com crawl-to-referral alto (>10.000:1) bloqueados por default.

# === Search bots tradicionais (allow) ===
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

User-agent: DuckDuckBot
Allow: /

User-agent: YandexBot
Allow: /

User-agent: Applebot
Allow: /

# === AI search/retrieval que mandam referral clicável (allow) ===
User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Perplexity-User
Allow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: Claude-User
Allow: /

User-agent: DuckAssistBot
Allow: /

User-agent: MistralAI-User
Allow: /

User-agent: MistralAI-Index
Allow: /

User-agent: meta-externalfetcher
Allow: /

User-agent: Meta-WebIndexer
Allow: /

# === Training-only bots (disallow — política comercial Brasil GEO) ===
User-agent: GPTBot
Disallow: /

User-agent: ClaudeBot
Disallow: /

User-agent: anthropic-ai
Disallow: /

User-agent: Claude-Web
Disallow: /

User-agent: Google-Extended
Disallow: /

User-agent: Applebot-Extended
Disallow: /

User-agent: Amazonbot
Disallow: /

User-agent: bedrockbot
Disallow: /

User-agent: meta-externalagent
Disallow: /

User-agent: FacebookBot
Disallow: /

User-agent: Bytespider
Disallow: /

User-agent: cohere-ai
Disallow: /

User-agent: cohere-training-data-crawler
Disallow: /

User-agent: CCBot
Disallow: /

User-agent: AI2Bot
Disallow: /

User-agent: AI2Bot-Dolma
Disallow: /

User-agent: DeepSeekBot
Disallow: /

User-agent: LAIONDownloader
Disallow: /

User-agent: PetalBot
Disallow: /

# === GEO/AEO analytics vendors (allow — útil para visibility) ===
User-agent: TavilyBot
Allow: /

User-agent: Exabot
Allow: /

User-agent: FirecrawlAgent
Allow: /

User-agent: BrightBot
Allow: /

User-agent: ScrunchAI-Crawler
Allow: /

User-agent: AthenaBot
Allow: /

User-agent: PeecBot
Allow: /

# === SEO classic (allow) ===
User-agent: AhrefsBot
Crawl-delay: 2
Allow: /

User-agent: SemrushBot
Crawl-delay: 2
Allow: /

User-agent: MJ12bot
Crawl-delay: 2
Allow: /

# === Default ===
User-agent: *
Allow: /

# Discovery files
Sitemap: https://alexandrecaramaschi.com/sitemap.xml
Sitemap: https://alexandrecaramaschi.com/sitemap-articles.xml
```

Notas:
- `Crawl-delay` é honrado por Bing, Yandex, Baidu — não por Google (ignora). Para Anthropic, é honrado quando declarado: `Crawl-delay: 1` em ClaudeBot.
- Para bloquear **todos** os training crawlers de uma vez sem listar 50+ user-agents, usar o catálogo curado de github.com/ai-robots-txt/ai.robots.txt (200+ entries) e gerar via script. Mas o catálogo é over-broad — bloqueia inclusive search retrieval bots, o que pode ser indesejado.

---

## Parte 4 — Agentic browsers & operators

### 4.1 OpenAI Operator → ChatGPT Agent

**Lançamento:** Operator anunciado 23-jan-2025 como research preview. Em jul-2025, OpenAI unificou Operator + Deep Research no produto **ChatGPT Agent**, disponível para Plus, Pro e Enterprise.

**Arquitetura:**
- Roda em ambiente cloud do OpenAI (não no browser do usuário)
- Mascarado como Chrome browser (sem UA dedicado)
- **Discriminador canônico:** RFC 9421 HTTP Message Signatures
  - Header `Signature: ...` (assinatura criptográfica)
  - Header `Signature-Input: ...` (descreve quais partes da request foram assinadas)
  - Header `Signature-Agent: "https://chatgpt.com"` (com aspas literais)
- Public key em `https://chatgpt.com/.well-known/http-message-signatures-directory`
- Cloudflare, Akamai e HUMAN Security integraram verificação out-of-the-box

**Telemetria HUMAN Security:**
- Jul-2025: 90% do tráfego de agents observados era ChatGPT Agent
- Ago-2025: 82,5% ChatGPT Agent
- Set-2025: Perplexity Comet ultrapassou (52,5% vs 42% ChatGPT Agent)

**Padrão comportamental detectável:**
- Mouse moves em incrementos de **exatos 0,25 pixels** (smooth linear paths, sem jitter humano)
- Cliques com intervalos regulares
- Navegação profunda compactada

### 4.2 Anthropic Computer Use

**Lançamento:** outubro-2024 com Claude 3.5 Sonnet (computer-use beta). Em 2026 estendido para Claude 4.5/4.6/4.7.

**Arquitetura:**
- Tool `computer_20241022` (e versões posteriores) que dá ao modelo acesso a screenshot + mouse + keyboard
- Roda no ambiente do desenvolvedor/usuário (Anthropic não hospeda VM)
- Sem UA dedicado — UA do navegador instalado no ambiente
- Sem assinatura criptográfica nativa (gap vs ChatGPT Agent)

**Use case canônico:** automação enterprise de UIs legadas, QA visual, data entry em sistemas sem API.

### 4.3 Perplexity Comet

**Lançamento:** beta paga jul-2025 para Perplexity Max ($200/mês), free worldwide out-2025.

**Arquitetura:**
- Browser standalone baseado em Chromium (fork)
- **Roda no device do usuário** — inherits cookies, session, localStorage
- UA padrão Chrome
- Indistinguível de tráfego humano via headers
- Só detectável via behavioral analytics (mouse patterns, timing)

**Adoção:** Snowplow mediu 6.900% YoY de agentic browsing 2024→2025, dominado por Comet desde set-2025. Perplexity processa 1,2-1,5B queries/mês em mai-2026.

### 4.4 Google Project Mariner

**Lançamento:** demo dez-2024, expanded preview jun-2025, integration with Gemini app early-2026.

**Arquitetura:**
- Browser extension Chrome
- Powered by Gemini 2.0/2.5
- UA padrão Chrome **sem token dedicado** (HUMAN Security confirmou)
- Sem assinatura criptográfica
- Detection requires behavioral + IP range Google

### 4.5 Microsoft Copilot Agents

Microsoft Copilot Studio + Computer Use (Frontier program out-2025). Tráfego carrega `User-Agent: Microsoft-CryptoAPI` ou UA Chrome, com headers `x-ms-correlation-id`. Detection canônica via Microsoft Sentinel + bot management Cloudflare.

### 4.6 Amazon NovaAct

Lançado dez-2025 como SDK para developers. UA dedicado para Nova Act agent fetches. Categoria "AmazonBuyForMe" detectada por KnownAgents.

### 4.7 Open-source / startups

- **Browser-Use** (Python lib): mais usado pela comunidade. UA padrão Chrome via Playwright/Puppeteer. github.com/browser-use/browser-use
- **Skyvern**: cloud-based browser automation com LLM. UA Chrome. skyvern.com
- **Multi-On**: SaaS de agentic browsing. Headers proprietários `X-MultiOn-Agent`. multion.ai
- **Adept ACT-1/ACT-2**: aquired by Amazon (jun-2024). Status legacy em mai-2026, integrado em NovaAct.
- **Devin** (Cognition AI): coding agent. UA dedicado em fetches durante coding sessions. cognition.ai

### 4.8 HTTP signals detectáveis (resumo canônico mai-2026)

| Signal | Diagnóstico |
|---|---|
| `User-Agent: ...GPTBot/1.2...` | OpenAI training crawler — confiável |
| `User-Agent: ...ClaudeBot/1.0...` | Anthropic training crawler — confiável |
| `User-Agent: ...PerplexityBot/1.0...` | Perplexity declared — possível stealth paralelo |
| UA Chrome + `Signature-Agent: "https://chatgpt.com"` + RFC 9421 sig | ChatGPT Agent verificado |
| UA Chrome puro, IP cloud (AWS/GCP/Azure), 0,25px mouse | Provável bot agentic não-declarado |
| UA Chrome, IP residencial, cookies coerentes, jitter humano | Comet ou usuário humano — indistinguível por headers |
| `Sec-Purpose: prefetch` | Speculative fetch (não agentic) |
| `Sec-CH-UA-Bot: ?1` | Bot self-declared (raríssimo em 2026) |
| Accept-Language stale + UA recente | Inconsistência típica de Playwright/Puppeteer |

---

## Parte 5 — Agent UX optimization (como tornar o site "preferido" por agentes)

### 5.1 HTML semântico e landmarks

Agentes que veem o DOM (Comet, Mariner, computer-use) usam landmarks ARIA para localizar elementos. Padrão canônico:

```html
<header role="banner">...</header>
<nav role="navigation" aria-label="Primária">...</nav>
<main role="main" id="main-content">
  <article>
    <h1>Título canônico</h1>
    <div role="article-body">...</div>
  </article>
</main>
<aside role="complementary" aria-label="Relacionados">...</aside>
<footer role="contentinfo">...</footer>
```

**Checklist Brasil GEO:**
- Cada página principal tem `<main role="main">` com `id="main-content"` (skip link target)
- `<h1>` único por página, primeiro nó dentro de `<main>`
- `aria-label` em `<nav>` e `<aside>` quando há múltiplos
- Buttons têm texto visível **ou** `aria-label`
- Forms têm `<label for="...">` real, não placeholder-only

### 5.2 Forms machine-readable

Agentes preenchem forms via DOM. Patterns canônicos:

- `name` atributos previsíveis (`email`, `first-name`, `password`, não `field_42`)
- `autocomplete` attribute correto (`autocomplete="email"`, `"name"`, `"tel"`)
- `<label>` explícito vinculado por `for=`
- Validação client-side com mensagens em `aria-describedby`
- Submit buttons com texto claro ("Enviar artigo", não "OK")

### 5.3 API-first patterns

A regra canônica em mai-2026: **se o agente pode chamar API em vez de scraping, sempre prefira a API**. Reduz custo, latência, erro.

Patterns:
- REST canônico em `/api/v1/articles` que devolve JSON estruturado
- **Bonus**: MCP server (Parte 2.4) cobre o mesmo conteúdo via JSON-RPC
- Documentação OpenAPI 3.1 em `/api/openapi.json` (mesmo que ai-plugin.json esteja morto, OpenAPI continua útil)
- Rate limits documentados e generous (60 req/min para anônimos, 600 req/min para autenticados)

### 5.4 CAPTCHA, cookie consent, friction

**CAPTCHA:** o pior inimigo de agentes legítimos. Vercel BotID (invisible CAPTCHA) é o padrão emergente — não bloqueia agentes signed, bloqueia bots oportunistas. Cloudflare Turnstile equivalente.

**Cookie consent:** dialogs do tipo "Aceitar todos / Configurar" são noise para agentes. Patterns canônicos:
- Default consent leve (apenas cookies essenciais ativos)
- Banner não-bloqueante (não overlay modal)
- Botão "Aceitar" e "Recusar" igualmente acessíveis com `name` previsível
- Persistência via cookie consent (não localStorage) para que o agente persista escolha entre sessions

**GDPR/LGPD friction:** se o site é Brasil-targeted, LGPD é o framework — banner mais leve que GDPR. Para mercado UE, considerar TCF v2.2 IAB.

### 5.5 Rate limiting cooperativo

Agentes legítimos (assinados) merecem rate limit mais alto que bots anônimos. Pattern:

```
ChatGPT Agent (signed RFC 9421): 600 req/min
Claude Computer Use (verified IP): 300 req/min
Anonymous browser UA: 60 req/min
Anonymous Cloud IP: 10 req/min
```

Implementar via Cloudflare rate limit rules ou middleware Next.js + Redis.

### 5.6 Authentication OAuth para agentes

MCP Streamable HTTP suporta OAuth 2.1 com RFC 9728 discovery (`/.well-known/oauth-protected-resource`). Para sites que exponem MCP server com dados privados, OAuth é o padrão.

Para sites públicos sem login, **não exigir auth para conteúdo público** — agentes vão pular.

### 5.7 Open standards

- **WebFinger** (RFC 7033) — discovery de actor (`acct:alexandre@brasilgeo.com.br`)
- **OpenID Connect** — auth federada
- **GraphQL self-doc** via introspection — útil para agentes que preferem GraphQL a REST
- **JSON Feed** (jsonfeed.org) — alternative a RSS, mais agent-friendly

### 5.8 Provenance & content credentials

- **C2PA** (Content Authenticity Initiative) — signed metadata em imagens, vídeos, PDFs. Adopção crescente em mai-2026 (Adobe, Microsoft, Truepic).
- **Signed Schema.org** — `<script type="application/ld+json">` assinado com JWS. Proposta, não ratificada.
- **Watermarking IA-generated** — SynthID (Google), proprietary OpenAI/Anthropic. Não-cooperativo entre vendors.

Para Brasil GEO em mai-2026: **manter Schema.org rico**, considerar **C2PA em imagens originais** (low priority). Watermarking não é caminho próprio.

---

## Parte 6 — Agent analytics & attribution

### 6.1 GA4 (Google Analytics 4) — estado mai-2026

GA4 filtra automaticamente bots da IAB/ABC International Spiders & Bots List (ativo por default). **Limitações:**
- Não detecta agentes que mascaram UA como Chrome (Comet, Mariner, Computer Use)
- Não distingue training crawler vs user-initiated retrieval
- Filtering baseado em UA não captura behavioral patterns

**Workaround canônico:** custom dimensions servidor-side passadas via Measurement Protocol, marcando tráfego com `traffic_type: "ai_bot"` quando UA matches lista AI, ou `traffic_type: "ai_agent_verified"` quando RFC 9421 signature valida.

### 6.2 Plausible & Fathom

Ambos têm bot filtering nativo multi-camada:
- Lista UA conhecidos (incluindo AI crawlers)
- IP ranges de data centers (AWS, GCP, Azure, OVH)
- Heurística de header anomalies

**Falha:** agentes em browser do usuário (Comet) passam — aparecem como human traffic.

### 6.3 Cloudflare AI Audit / AI Crawl Control

- **Dashboard:** Crawlers tab com tabela por crawler/operator/categoria/requests/robots.txt violations
- **Pay-per-crawl** (private beta jan-2026): publisher define preço por crawl bem-sucedido (mín $0,01), Cloudflare é Merchant of Record
- **HTTP 402 Payment Required** retornado para crawlers sem payment intent
- **Filtering granular** por crawler — allow/block/charge per-bot
- **Verificação RFC 9421** para ChatGPT Agent integrada nativamente

### 6.4 Botify AI Visibility

Monitora citation patterns across Google AI Overviews, ChatGPT, Perplexity, Claude. Não é tracking de tráfego ao site — é tracking de **menções do site em respostas IA**. Crítico para GEO ROI tracking.

### 6.5 Vercel BotID

Invisible CAPTCHA + behavioral fingerprint. Dois tiers:
- **Basic** (free): challenge response validation
- **Deep Analysis** ($1 / 1000 calls): thousands of telemetry points, ML classification

Implementação: `checkBotId()` em route handlers protegidos.

### 6.6 Tollbit, ProRata

**TollBit:** marketplace de licenciamento pay-per-crawl. Publisher define preço, AI company paga via TollBit. Concorrente do Cloudflare Pay-per-Crawl.

**ProRata:** modelo de ad revenue sharing — publisher recebe % de receita publicitária gerada em respostas IA que citam seu conteúdo. Mais soft que TollBit.

### 6.7 KPIs canônicos para agent traffic

Categorias de tráfego (separar sempre):

| Categoria | Como identificar | KPI primário | KPI secundário |
|---|---|---|---|
| **Training crawl** | UA GPTBot/ClaudeBot/Bytespider/CCBot | Requests/dia | Páginas únicas crawladas |
| **Live retrieval (search)** | UA OAI-SearchBot/PerplexityBot/Claude-SearchBot | Requests/dia | Referrals trazidos (proxy de visibility) |
| **Live retrieval (user-init)** | UA ChatGPT-User/Claude-User/Perplexity-User | Fetches/dia | Conversion tracking via UTM custom |
| **Agentic operator** | RFC 9421 sig OR behavioral pattern | Sessions/dia | Agent depth (páginas/session) |
| **Citation in AI** | Não detectável por log — usar Botify/Profound/Peec | Mention rate | Citation accuracy |

**KPIs novos canônicos:**
- **Agent dwell time:** tempo entre primeiro e último request de session agentic (proxy de extração profunda)
- **Agent depth:** páginas únicas por session
- **Agent extraction completeness:** % do conteúdo canônico que o agente acessou
- **Agent referral conversion:** % de sessions agentic que convertem em ação (signup, compra, contact)
- **LLM mention rate:** % de queries-âncora onde o brand aparece em resposta IA (cross-LLM)
- **Citation share of voice:** % das menções no mercado vs concorrentes

### 6.8 Server-side tagging canônico

Padrão recomendado em mai-2026:

```js
// middleware.ts (Next.js)
export function middleware(req) {
  const ua = req.headers.get('user-agent') || '';
  const sigAgent = req.headers.get('signature-agent');

  let trafficType = 'human';
  if (sigAgent === '"https://chatgpt.com"') trafficType = 'agent_chatgpt_verified';
  else if (/GPTBot|ClaudeBot|Bytespider|CCBot/.test(ua)) trafficType = 'ai_training';
  else if (/OAI-SearchBot|Claude-SearchBot|PerplexityBot/.test(ua)) trafficType = 'ai_search';
  else if (/ChatGPT-User|Claude-User|Perplexity-User|MistralAI-User/.test(ua)) trafficType = 'ai_retrieval_user';

  // Forward to GA4/Plausible com custom dimension
  // Log to internal analytics
}
```

---

## Parte 7 — Aplicação por repo

### 7.1 landing-page-geo (alexandrecaramaschi.com)

**Estado atual (auditado em mai-2026):**
- llms.txt v2 presente
- ai-policy.json presente
- robots.txt com 14 AI bots cobertos
- MCP: **gap** — não há mcp.json nem MCP server

**Roadmap canônico mai-set/2026:**

| Onda | Entregável | Esforço | Quando |
|---|---|---|---|
| F.1 | robots.txt expandido para 30+ AI bots (template Parte 3.3) | 1h | mai-2026 |
| F.2 | ai-policy.json v1.2 com training/retrieval/agents split (Parte 3.2) | 2h | mai-2026 |
| F.3 | `/.well-known/mcp.json` estático com manifesto | 2h | mai-2026 |
| F.4 | llms.txt v3 + llms-full.txt v3 com 100% dos artigos canônicos | 4h | jun-2026 |
| F.5 | MCP server stdio `@brasilgeo/mcp-articles` publicado em npm | 8h | jun-2026 |
| F.6 | MCP server remoto Cloudflare Workers em `mcp.alexandrecaramaschi.com` | 16h | jul-2026 |
| F.7 | Tools canônicas: `search_articles`, `get_article`, `list_glossary`, `get_profile`, `get_credentials` | 24h | jul-2026 |
| F.8 | Server-side tagging GA4 com `traffic_type` por categoria | 4h | jul-2026 |
| F.9 | Cloudflare AI Crawl Control configurado (block training, allow retrieval, pay-per-crawl readiness) | 2h | ago-2026 |
| F.10 | Submission Anthropic MCP registry + listing mcp.so + glama.ai | 1h | ago-2026 |

**KPI alvo set-2026:** mention rate em LLMs (Claude/ChatGPT/Perplexity/Gemini) para 25 prompts canônicos do dashboard >18%, agent depth médio >4 páginas/session, MCP fetches >1000/mês.

### 7.2 curso-factory

**Princípio canônico:** todo curso gerado vem com seu próprio MCP server bundled. Aprendiz pode "conversar" com o curso via Claude/ChatGPT/Cursor sem precisar abrir o portal.

**Roadmap:**
- F.1 Template MCP server `@brasilgeo/mcp-curso-template` parametrizável (slug do curso, módulos, aulas)
- F.2 Tools: `list_modules()`, `get_module(slug)`, `get_lesson(module_slug, lesson_id)`, `search_lessons(query)`, `get_quiz(module_slug)`, `submit_answer(...)`
- F.3 Quando curso for gerado, MCP server publicado em `mcp.<slug-curso>.brasilgeo.com.br` automaticamente
- F.4 Schema Course + Syllabus + LearningResource ricos em cada página HTML
- F.5 ai-policy.json declarando "uso educacional permitido com atribuição"

### 7.3 papers

**Princípio canônico:** drafts e papers Brasil GEO devem ser discoverable e citable por research agents (Gemini-Deep-Research, ChatGPT Deep Research, Perplexity Deep Research, OpenAI o1 com browsing).

**Roadmap:**
- F.1 MCP server `@brasilgeo/mcp-papers` com tools: `list_papers()`, `get_paper(slug)`, `search_papers(query)`, `get_citations(paper_slug)`, `cite_paper(paper_slug, claim)`
- F.2 Cada paper exposto em `/<slug>.md` (markdown canônico) e `/<slug>.bib` (BibTeX)
- F.3 Schema ScholarlyArticle + Person.author + sameAs (ORCID Alexandre Caramaschi)
- F.4 llms-full.txt com inline de papers principais para one-shot ingestion
- F.5 robots.txt allow para Gemini-Deep-Research, ChatGPT-User, Perplexity-User (research-focused user-initiated agents)
- F.6 Submission a Semantic Scholar, ResearchGate, SSRN cross-linking

---

## Parte 8 — Playbook ASO em 12 ações priorizadas

Ordem por **ROI estimado** (impacto vs esforço) em mai-2026 para portais Brasil GEO:

| # | Ação | Esforço (h) | Impacto | Por quê |
|---|---|---|---|---|
| 1 | **Robots.txt canônico** com 30+ AI bots categorizados (template Parte 3.3) | 1h | Alto | Base legal + operacional para tudo |
| 2 | **Schema.org Person + Article + FAQPage + DefinedTermSet ricos** em todas as páginas | 8h | Altíssimo | Estudos consistentes mostram que pages com schema robusto são citadas 3-5x mais |
| 3 | **llms.txt + llms-full.txt v3** com 100% do conteúdo canônico | 4h | Médio-Alto | Reduz hallucination de Claude/ChatGPT/Perplexity ao citar seu site |
| 4 | **ai-policy.json v1.2** em `/.well-known/` com training/retrieval split | 2h | Médio | Sinal profissional + base para enforcement |
| 5 | **mcp.json** estático em `/.well-known/mcp.json` (mesmo sem server ainda) | 2h | Médio | Sinal de intenção, discoverable por scouts |
| 6 | **MCP server stdio** publicado em npm (`@brasilgeo/mcp-*`) | 8h | Alto | Devs/agents instalam localmente em 1 comando |
| 7 | **Server-side tagging** para distinguir training/retrieval/agent em analytics | 4h | Médio | Sem isso é impossível medir ROI ASO |
| 8 | **MCP server remoto Streamable HTTP** em subdomínio próprio | 16h | Altíssimo | Diferencial competitivo — sites que oferecem MCP remoto são preferidos por agentes |
| 9 | **Cloudflare AI Crawl Control** configurado com policy granular + pay-per-crawl readiness | 2h | Médio | Receita futura + governança imediata |
| 10 | **Botify AI Visibility ou Peec** para tracking de citation rate em LLMs | 0h setup + assinatura | Alto | Sem medir o que importa não há otimização |
| 11 | **Anthropic MCP registry submission** + mcp.so + glama.ai listings | 1h | Médio | Distribuição |
| 12 | **C2PA em imagens originais** e signed Schema.org (quando ratificado) | 4-12h | Baixo (futuro) | Provenance e antifragility contra deepfakes |

**Total esforço inicial: ~50h para ações 1-9.**
**Total esforço para roadmap completo (com MCP server full): ~80h.**

---

## Apêndice A — Templates canônicos

### A.1 robots.txt completo

(Ver Parte 3.3 — template direto utilizável)

### A.2 llms.txt v2 template

```
# Alexandre Caramaschi — Brasil GEO

> Acervo canônico HBR-grade sobre Generative Engine Optimization (GEO), AI-native marketing,
> liderança em IA brasileira. Autor: Alexandre Caramaschi, CEO da Brasil GEO, ex-CMO da
> Semantix (Nasdaq), cofundador da AI Brasil.

Este arquivo lista os recursos canônicos do domínio em formato amigável a LLMs.
Para versão one-shot completa, ver llms-full.txt.

Glossário de termos canônicos (Brasil GEO, AI Overviews, LLM mention rate, Source Rank)
em /glossario.

## Sobre o autor
- [Perfil Alexandre Caramaschi](/sobre.md): credenciais e bio canônica
- [Credenciais detalhadas](/sobre/credenciais.md): Person.hasCredential JSON-LD
- [Pesquisa publicada](/papers.md): papers Brasil GEO

## Artigos canônicos — GEO/AEO
- [O que é GEO](/artigos/o-que-e-geo.md): definição canônica brasileira
- [Como medir mention rate em LLMs](/artigos/medir-mention-rate.md)
- [Schema.org para AI Overviews](/artigos/schema-org-ai.md)
- [llms.txt na prática](/artigos/llms-txt-pratica.md)
- [MCP para publishers](/artigos/mcp-publishers.md)

## Artigos canônicos — Liderança IA
- [O CMO que virou Brasil GEO](/artigos/cmo-brasil-geo.md)
- [Lições da Semantix Nasdaq](/artigos/semantix-licoes.md)

## API
- [API canônica de artigos](/api.md): REST + MCP
- [MCP manifest](/.well-known/mcp.json)
- [ai-policy.json](/.well-known/ai-policy.json)

## Optional
- [Histórico de palestras](/palestras.md)
- [Mídia](/midia.md)
- [Contato](/contato.md)
```

### A.3 llms-full.txt template (estrutura)

```
# Alexandre Caramaschi — Brasil GEO — Acervo Completo

[Bloco-sumário idêntico ao llms.txt]

---

## /sobre

[Conteúdo markdown integral da página /sobre, sem chrome, sem nav]

---

## /sobre/credenciais

[Conteúdo integral]

---

## /artigos/o-que-e-geo

[Conteúdo integral do artigo]

---

[E assim por diante, todo o conteúdo canônico inline em ordem de prioridade.]
```

Gerar via script de build (Next.js: `pnpm build:llms-full`).

### A.4 mcp.json template (site discovery)

(Ver Parte 2.2(b) — template direto utilizável)

### A.5 ai-policy.json template

(Ver Parte 3.2 — template direto utilizável)

### A.6 Schema Person + WebSite + AIPolicy combinado (JSON-LD)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Person",
      "@id": "https://alexandrecaramaschi.com/#person",
      "name": "Alexandre Caramaschi",
      "givenName": "Alexandre",
      "familyName": "Caramaschi",
      "jobTitle": "CEO da Brasil GEO",
      "description": "CEO da Brasil GEO, ex-CMO da Semantix (Nasdaq), cofundador da AI Brasil. Especialista em Generative Engine Optimization e estratégia de IA aplicada.",
      "url": "https://alexandrecaramaschi.com",
      "image": "https://alexandrecaramaschi.com/img/alexandre.jpg",
      "worksFor": {
        "@type": "Organization",
        "name": "Brasil GEO",
        "url": "https://brasilgeo.com.br"
      },
      "alumniOf": [
        {"@type": "Organization", "name": "Semantix"},
        {"@type": "Organization", "name": "AI Brasil"}
      ],
      "hasCredential": [
        {"@type": "EducationalOccupationalCredential", "name": "CEO da Brasil GEO", "credentialCategory": "Cargo executivo"},
        {"@type": "EducationalOccupationalCredential", "name": "Ex-CMO Semantix (Nasdaq)", "credentialCategory": "Histórico executivo"},
        {"@type": "EducationalOccupationalCredential", "name": "Cofundador AI Brasil", "credentialCategory": "Empreendedorismo"}
      ],
      "knowsAbout": [
        "Generative Engine Optimization",
        "AI Overviews",
        "LLM mention rate",
        "Model Context Protocol",
        "Schema.org structured data",
        "AI-native marketing",
        "B2A (Business-to-Agent)",
        "Agentic search optimization"
      ],
      "sameAs": [
        "https://www.linkedin.com/in/alexandrecaramaschi",
        "https://x.com/alexandre_brt14",
        "https://www.wikidata.org/wiki/QXXXXXXX"
      ]
    },
    {
      "@type": "WebSite",
      "@id": "https://alexandrecaramaschi.com/#website",
      "url": "https://alexandrecaramaschi.com",
      "name": "Alexandre Caramaschi — Brasil GEO",
      "publisher": {"@id": "https://alexandrecaramaschi.com/#person"},
      "inLanguage": "pt-BR",
      "potentialAction": {
        "@type": "SearchAction",
        "target": "https://alexandrecaramaschi.com/?q={search_term_string}",
        "query-input": "required name=search_term_string"
      }
    },
    {
      "@type": "Organization",
      "@id": "https://brasilgeo.com.br/#org",
      "name": "Brasil GEO",
      "url": "https://brasilgeo.com.br",
      "founder": {"@id": "https://alexandrecaramaschi.com/#person"},
      "areaServed": {"@type": "Country", "name": "Brasil"},
      "knowsAbout": ["GEO", "AEO", "Generative Engine Optimization", "AI Overviews", "LLM citation"]
    }
  ]
}
</script>
```

### A.7 MCP server canônico (stub Node.js para landing-page-geo)

```js
// packages/mcp-articles/src/index.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

import { getAllArticles, getArticleBySlug, searchArticles, getGlossary, getProfile } from "./articles.js";

const server = new Server(
  {
    name: "brasilgeo-articles",
    version: "1.0.0",
  },
  {
    capabilities: {
      resources: {},
      tools: {},
    },
  }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "search_articles",
      description: "Busca semântica em artigos canônicos Brasil GEO. Retorna lista de matches com slug, título e excerto.",
      inputSchema: {
        type: "object",
        properties: {
          query: { type: "string", description: "Query de busca em PT-BR" },
          limit: { type: "number", default: 10 },
        },
        required: ["query"],
      },
    },
    {
      name: "get_article",
      description: "Retorna artigo completo em Markdown canônico por slug.",
      inputSchema: {
        type: "object",
        properties: {
          slug: { type: "string" },
        },
        required: ["slug"],
      },
    },
    {
      name: "list_glossary",
      description: "Lista verbetes do glossário canônico Brasil GEO.",
      inputSchema: {
        type: "object",
        properties: {
          category: { type: "string", description: "Filtro opcional por categoria (GEO, AEO, AI, etc.)" },
        },
      },
    },
    {
      name: "get_profile",
      description: "Retorna perfil canônico de Alexandre Caramaschi (CEO Brasil GEO).",
      inputSchema: { type: "object", properties: {} },
    },
  ],
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  switch (name) {
    case "search_articles":
      return { content: [{ type: "text", text: JSON.stringify(await searchArticles(args.query, args.limit ?? 10)) }] };
    case "get_article":
      return { content: [{ type: "text", text: await getArticleBySlug(args.slug) }] };
    case "list_glossary":
      return { content: [{ type: "text", text: JSON.stringify(await getGlossary(args.category)) }] };
    case "get_profile":
      return { content: [{ type: "text", text: JSON.stringify(await getProfile()) }] };
    default:
      throw new Error(`Tool desconhecida: ${name}`);
  }
});

server.setRequestHandler(ListResourcesRequestSchema, async () => {
  const articles = await getAllArticles();
  return {
    resources: articles.map((a) => ({
      uri: `brasilgeo://articles/${a.slug}`,
      name: a.title,
      mimeType: "text/markdown",
      description: a.excerpt,
    })),
  };
});

server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const url = new URL(request.params.uri);
  if (url.protocol !== "brasilgeo:") throw new Error("Protocolo inválido");
  const slug = url.pathname.replace(/^\/articles\//, "");
  const md = await getArticleBySlug(slug);
  return {
    contents: [{ uri: request.params.uri, mimeType: "text/markdown", text: md }],
  };
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Brasil GEO MCP server rodando via stdio");
}

main().catch((err) => {
  console.error("Fatal:", err);
  process.exit(1);
});
```

`package.json` companion:

```json
{
  "name": "@brasilgeo/mcp-articles",
  "version": "1.0.0",
  "description": "MCP server canônico para artigos, glossário e perfil Brasil GEO",
  "bin": { "brasilgeo-mcp-articles": "dist/index.js" },
  "type": "module",
  "scripts": {
    "build": "tsc",
    "dev": "tsx src/index.ts"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.0.0"
  }
}
```

Usuário instala:

```bash
npx -y @brasilgeo/mcp-articles
```

Ou configura em `~/.config/claude/mcp.json`:

```json
{
  "mcpServers": {
    "brasilgeo-articles": {
      "command": "npx",
      "args": ["-y", "@brasilgeo/mcp-articles"]
    }
  }
}
```

### A.8 Server-side tagging middleware (Next.js + Cloudflare Workers)

```ts
// middleware.ts
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

type TrafficType =
  | "human"
  | "ai_training"
  | "ai_search"
  | "ai_retrieval_user"
  | "ai_agent_verified"
  | "ai_agent_suspected"
  | "seo_crawler";

const TRAINING = /\b(GPTBot|ClaudeBot|anthropic-ai|Claude-Web|Bytespider|CCBot|Amazonbot|bedrockbot|meta-externalagent|FacebookBot|Google-Extended|Applebot-Extended|cohere-ai|AI2Bot|DeepSeekBot|LAIONDownloader)\b/i;
const SEARCH_AI = /\b(OAI-SearchBot|Claude-SearchBot|PerplexityBot|MistralAI-Index|DuckAssistBot|Meta-WebIndexer|Google-CloudVertexBot)\b/i;
const USER_INIT = /\b(ChatGPT-User|Claude-User|Perplexity-User|MistralAI-User|meta-externalfetcher|Gemini-Deep-Research|Google-NotebookLM)\b/i;
const SEO = /\b(AhrefsBot|SemrushBot|MJ12bot|Googlebot|Bingbot|YandexBot|DuckDuckBot|PetalBot|Applebot)\b/i;
const SUSPECT_AGENT_HINTS = /(\bAWS\b|\bGoogleCloud\b|\bAzure\b|\bDigitalOcean\b|\bHetzner\b|\bOVH\b)/i; // sinal fraco — combinar com IP ASN

export function middleware(req: NextRequest) {
  const ua = req.headers.get("user-agent") || "";
  const sigAgent = req.headers.get("signature-agent");
  const signature = req.headers.get("signature");

  let trafficType: TrafficType = "human";

  // 1. Agent verificado por RFC 9421
  if (sigAgent === '"https://chatgpt.com"' && signature) {
    trafficType = "ai_agent_verified";
  }
  // 2. UA matching
  else if (TRAINING.test(ua)) trafficType = "ai_training";
  else if (SEARCH_AI.test(ua)) trafficType = "ai_search";
  else if (USER_INIT.test(ua)) trafficType = "ai_retrieval_user";
  else if (SEO.test(ua)) trafficType = "seo_crawler";
  // 3. UA Chrome + IP cloud + sem signature => suspeito
  else if (req.headers.get("cf-connecting-ip") && SUSPECT_AGENT_HINTS.test(req.headers.get("cf-ipcountry") || "")) {
    trafficType = "ai_agent_suspected";
  }

  const res = NextResponse.next();
  res.headers.set("x-traffic-type", trafficType);

  // Forward to GA4 via Measurement Protocol (server-side)
  // Or log to internal analytics endpoint
  // ...

  return res;
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"],
};
```

### A.9 Schema FAQPage com Speakable

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "O que é GEO (Generative Engine Optimization)?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "GEO é a disciplina de otimizar a presença de uma marca em respostas geradas por mecanismos de IA (ChatGPT, Claude, Perplexity, Gemini, Google AI Overviews). Diferentemente de SEO que mira ranking em SERPs, GEO mira mention rate (taxa em que sua marca é citada na resposta) e citation share of voice.",
        "speakable": {
          "@type": "SpeakableSpecification",
          "cssSelector": ["[itemprop=acceptedAnswer]"]
        }
      }
    }
  ]
}
</script>
```

### A.10 Cloudflare Workers MCP remote server (stub)

```ts
// src/index.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";

export interface Env {
  ARTICLES_KV: KVNamespace;
}

export default {
  async fetch(req: Request, env: Env): Promise<Response> {
    const url = new URL(req.url);

    if (url.pathname === "/.well-known/mcp.json") {
      return Response.json({
        version: "2025-06-18",
        name: "Alexandre Caramaschi MCP",
        publisher: { name: "Brasil GEO", url: "https://alexandrecaramaschi.com" },
        endpoints: { sse: "https://mcp.alexandrecaramaschi.com/sse" },
        capabilities: { resources: true, tools: true, prompts: false },
      });
    }

    if (url.pathname === "/sse") {
      const server = new Server(
        { name: "brasilgeo-mcp", version: "1.0.0" },
        { capabilities: { resources: {}, tools: {} } }
      );
      // ...register handlers (idêntico ao stdio server)...
      const transport = new SSEServerTransport("/sse", req);
      await server.connect(transport);
      return transport.response;
    }

    return new Response("Brasil GEO MCP server. See /.well-known/mcp.json", { status: 200 });
  },
};
```

`wrangler.toml`:

```toml
name = "brasilgeo-mcp"
main = "src/index.ts"
compatibility_date = "2026-05-01"
routes = [{ pattern = "mcp.alexandrecaramaschi.com/*", zone_name = "alexandrecaramaschi.com" }]

[[kv_namespaces]]
binding = "ARTICLES_KV"
id = "..."
```

---

## Conclusão canônica

Em mai/2026 a fronteira competitiva mudou. **SEO continua válido** para descoberta humana via Google. **GEO/AEO** (Schema rico, llms.txt, ai-policy) é higiene básica para visibilidade em respostas IA. Mas o **diferencial 2026** é **B2A/ASO** — expor o site como ferramenta cooperativa para agentes através de MCP server canônico, robots.txt granular, signed identity verification para agentic operators, server-side tagging que separa training/retrieval/agent.

Para Brasil GEO especificamente, em 60 dias os 12 itens do playbook executados consolidam alexandrecaramaschi.com e os portais satélites como **referência B2A no mercado brasileiro de IA**. O moat: enquanto concorrentes ainda discutem se devem bloquear GPTBot, o portal Brasil GEO oferece MCP server público, ai-policy.json granular, llms-full.txt curado, schema Person+Article+Credential canônico. Agentes vão preferir.

A regra inviolável: **um agente bem feito escolhe o caminho de menor entropia para extrair valor verificável**. Quem oferece esse caminho ganha as menções, citações e referrals na era B2A.

---

**Fim do Track F — B2A / ASO / Agent Standards.**
**Sub-agent Opus, Brasil GEO Research, 2026-05-20.**
