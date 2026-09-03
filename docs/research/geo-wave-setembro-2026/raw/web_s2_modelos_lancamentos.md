# web_s2_modelos_lancamentos (Perplexity WEB Pro, https://www.perplexity.ai/search/c82029ac-2914-4b33-94c1-9ad755f260df)

Nota de método: resposta do Perplexity WEB (conta alexandre.brt14@gmail.com, plano gratuito no navegador logado por CDP), usada porque a API devolveu 401 insufficient_quota. Sidebar e sugestões da interface removidos; só resposta e links.

Concluído
3 etapas

Aqui está o panorama dos lançamentos de modelos e mudanças de API entre 20 de agosto e 3 de setembro de 2026, com datas, fontes nomeadas e URLs, distinguindo fonte primária (anúncio oficial / docs do provedor) de secundária (imprensa, agregadores, blogs de terceiros). Quando não localizei informação oficial para um item específico, indico “não localizado”.

OpenAI (GPT‑5.x)

GPT‑5.6 Sol / Terra / Luna (atualizações de agosto)

Data: 6 de agosto de 2026 (atualizações Sol e Luna para ChatGPT).

O que mudou (busca web / citação / browsing agêntico / memória / comércio):

Busca web: habilitada por sessão; “Deep Research” executa pesquisa autônoma multi‑etapa com relatório citado.

Citação de fontes: redução de citações a Reddit a partir de ~14 de agosto (mudança de comportamento de citação, não novo recurso de API).

Browsing agêntico: “Deep Research” é um agente de pesquisa autônomo (multi‑step).

Memória/comércio: não localizado mudança específica de API neste período.

Fonte primária: OpenAI (implantação/segurança e docs de preços) — URL: página de preços da OpenAI e anúncio de deployment‑safety (não localizado URL exata nos resultados; informação reportada por Tech Insider e MFate7).

Fonte secundária: [MFate7], [Tech Insider – citações Reddit], [AI News 22/ago].
mfate7
+2

Observação: Não encontrei, nos resultados consultados, URL direta de changelog da OpenAI com detalhes de “GPT‑5.6 Sol/Luna” neste intervalo; as informações vêm de reportagens e trackers.

WebMCP (agente interagindo com apps/sites)

Data: 31 de agosto de 2026 (anúncio no X da conta @OpenAIDevs).

O que mudou: nova forma de agentes interagirem com apps e websites (padrão MCP via web). Impacta browsing agêntico e potencialmente comércio (ações em sites).

Fonte primária: Post oficial no X da OpenAI Developers — URL: https://x.com/OpenAIDevs/status/2094529078863024174.
x

Fonte secundária: não localizado.

Google (Gemini 3.x)

Gemini 3.8 Flash (e variante “3.8 Flash Cyber”)

Data: 2 de setembro de 2026.

O que mudou:

Busca web / browsing agêntico: modelo posicionado para “long‑horizon software engineering, autonomous agents, and multi‑step enterprise reasoning”; disponível no Gemini Enterprise Agent Platform com agentes stateful (já em 3.7 Flash, mantido).

Citação de fontes: não localizado mudança específica de citação neste lançamento.

Memória/comércio: não localizado mudança específica.

Preço (relevante para medição de custo): US$ 0,75 / US$ 3,75 por 1M tokens (entrada/saída) até 31/12/2026; cache a US$ 0,075/1M no Enterprise Agent Platform.

Fonte primária: Blog oficial do Google / docs do Gemini API (preços e disponibilidade) — URL do anúncio reportado: post no blog do Google (não localizado URL exata nos resultados; detalhes em docs de preço do Gemini).

Fonte secundária: Tech Insider (lançamento, preços, distribuição); 9to5Google (citado pelo Tech Insider); VUVE (contexto de agentes stateful).
36kr
+2

Gemini 3.7 Flash (para contexto imediato anterior)

Data: ~13 de agosto de 2026 (lançamento).

O que mudou: agentes stateful hospedados que planejam e executam em ambientes isolados gerenciados pelo Google.

Fonte primária: docs do Gemini / Google Cloud (não localizado URL exata nos resultados).

Fonte secundária: VUVE, Tech Insider.
vuve
+1

Anthropic (Claude 5 / Fable / Mythos)

Claude Fable 5.1 e Claude Mythos 5.1

Data: 1 de setembro de 2026.

O que mudou:

Busca web / browsing agêntico: não localizado mudança específica de browsing neste update.

Citação de fontes: não localizado mudança específica.

Memória/comércio: não localizado mudança específica.

Observação relevante para agentes: mesmo modelo com dois níveis de salvaguarda; Fable 5.1 tem salvaguardas mais precisas (ex.: permite identificar vulnerabilidades em código; intervenções em biologia benigna 85% menores).

Preço: US$ 10 / US$ 50 por 1M tokens (entrada/saída); leitura de cache a US$ 0,25/1M (redução de 75% vs Fable 5).

Fonte primária: Página oficial Anthropic “Claude Mythos” (anúncio 1/9/2026) — URL: https://www.anthropic.com/claude/mythos.
anthropic

Fonte secundária: 9to5Mac, MacRumors, VentureBeat, SaaSCity, ExplainX, GlobalTechCouncil, Pasquale Pillitteri, JLS42.
9to5mac
+7

xAI (Grok)

Grok 4.6

Data: 12 de agosto de 2026.

O que mudou:

Busca web: “Image Search in Web Search” já estava disponível desde maio/2026; Grok 4.6 mantém ferramentas de agent (web_search, x_search, code_execution).

Browsing agêntico: modelo frontier para coding e tarefas agênticas; disponível em GitHub Copilot, Cursor, Grok Build, Perplexity Computer, etc.

Citação de fontes: não localizado mudança específica.

Memória/comércio: não localizado mudança específica neste lançamento.

Preço: US$ 2 / US$ 6 por 1M tokens (entrada/saída) abaixo de 200k tokens de prompt; acima disso US$ 4 / US$ 12.

Fonte primária: xAI Docs – Release Notes (12/ago: Grok 4.6) — URL: https://docs.x.ai/developers/release-notes.
x

Fonte secundária: Tech Insider (Grok 4.6 vs Grok 3), Lunquora, BigHatGroup.
tech-insider
+2

Grok Bot (agente durável em nuvem)

Data: 11 de agosto de 2026 (disponibilidade); 31 de agosto (saída do beta).

O que mudou: agentes “duráveis” com mensagens, aprovações, conectores e rotinas; impacta diretamente browsing agêntico e automação (potencialmente comércio via conectores).

Fonte primária: xAI Docs – Release Notes (11/ago: Grok Bot) — URL: https://docs.x.ai/developers/release-notes.
x

Fonte secundária: Basenor (Grok Bot expande capacidades), BigHatGroup.
bighatgroup
+1

Agent Tools / Collections Search / Remote MCP

Data: várias (maio–nov/2025), mas relevantes para medição de uso de ferramentas em agosto/2026.

O que mudou: ferramentas de agente (web_search, x_search, code_execution) e “Collections Search Tool” para buscar em bases de conhecimento enviadas; Remote MCP Tools.

Fonte primária: xAI Docs – Release Notes.
x

Fonte secundária: Trend Undefined Labs (resumo de Agent Tools API).
trend.undefined-labs

Meta (Llama)

Llama 4 / Llama 3.3 / embedding / rerank (20–ago a 03–set/2026): não localizado lançamento oficial neste intervalo nas fontes consultadas.

Fonte primária: não localizado.

Fonte secundária: não localizado.

Mistral

Novos modelos Mistral (20–ago a 03–set/2026): não localizado lançamento oficial neste intervalo nas fontes consultadas.

Fonte primária: não localizado.

Fonte secundária: não localizado.

DeepSeek

DeepSeek‑V4‑Flash‑Vision‑Exp (multimodal)

Data: 21 de agosto de 2026 (API); pesos abertos em 31 de agosto de 2026.

O que mudou: primeiro modelo V4 com visão (imagem + texto); mantém capacidades de agente e raciocínio do V4‑Flash; API suporta Chat Completions, Messages (Anthropic‑compatible) e Responses (OpenAI‑compatible).

Preço: taxas padrão V4‑Flash; imagens tokenizadas até 384 tokens cada.

Fonte primária: DeepSeek API Changelog / post oficial no X — URL do changelog reportado: https://deepseek.ai/blog/deepseek-v4-rollout-flash-vision-pricing-harness-2026-guide; post X: https://x.com/deepseek_ai/status/2090730032574631962.
deepseek
+1

Fonte secundária: Pandaily, ExplainX, Cellcog, Julian Goldie.
pandaily
+3

DeepSeek V4‑Pro (GA)

Data: 13 de agosto de 2026 (GA).

O que mudou: variante “Pro” da família V4 para tarefas mais pesadas; não localizado detalhe específico de browsing/citação neste intervalo.

Fonte primária: DeepSeek API Changelog (reportado em ).
deepseek
+1

Fonte secundária: Coursiv (V5 inexistente, confirma V4).
coursiv

Qwen (Alibaba)

Qwen3.8‑Flash‑Next (open weights, preview da arquitetura Qwen4)

Data: 26–27 de agosto de 2026 (anúncio/open‑source).

O que mudou: MoE 125B (6B ativos) com camada “N‑gram Embedding” (51B); preview da arquitetura Qwen4; API no QwenCloud com preço ~US$ 0,16 / US$ 0,47 por 1M tokens.

Embedding/rerank: introduz “N‑gram Embedding” como mecanismo de representação de vocabulário; não é um modelo de embedding separado, mas uma camada que amplia representação de tokens.

Fonte primária: Anúncio Qwen / QwenCloud (reportado por GPTS24 e Gigazine); URL do post Gigazine (JP): https://gigazine.net/gsc_news/en/20260827-qwen3-8-flash-next/.
gigazine
+1

Fonte secundária: GPTS24, Pasquale Pillitteri, Local AI Zone, Winzheng, Orcarouter.
gpts24
+4

Qwen3.8‑Flash (produção no QwenCloud)

Data: ~28 de agosto de 2026 (disponibilidade API).

O que mudou: versão de produção da família Flash; preço ~US$ 0,15 / US$ 0,47 por 1M tokens; cache hits a ~US$ 0,016/1M.

Fonte primária: QwenCloud (reportado em ).
orcarouter

Fonte secundária: Orcarouter.
orcarouter

Kimi (Moonshot AI)

Novos modelos Kimi (20–ago a 03–set/2026): não localizado lançamento oficial neste intervalo nas fontes consultadas.

Fonte primária: não localizado.

Fonte secundária: não localizado.

Novos modelos de embedding e rerank (geral)

Embedding / rerank específicos (Cohere, Voyage, Nomic, etc.) neste intervalo: não localizado lançamento oficial entre 20‑ago e 03‑set/2026 nas fontes consultadas.

Observação: Qwen3.8‑Flash‑Next introduz “N‑gram Embedding” como camada interna, mas não é um modelo de embedding standalone.

Fonte primária: não localizado.

Fonte secundária: não localizado.

Mudanças de API relevantes para medição (Perplexity, OpenAI Responses, xAI Agent Tools)

Perplexity Agent API (mudanças 20‑ago a 03‑set/2026): não localizado changelog oficial ou anúncio neste intervalo nas fontes consultadas.

Fonte primária: não localizado.

Fonte secundária: não localizado.

OpenAI Responses API (mudanças 20‑ago a 03‑set/2026): não localizado mudança específica neste intervalo; o que aparece é WebMCP (31/ago) como novo padrão para agentes interagirem com apps/sites, o que afeta como medir ações de browsing/comércio.

Fonte primária: post @OpenAIDevs (WebMCP).
x

Fonte secundária: não localizado.

xAI Agent Tools / Responses API (mudanças 20‑ago a 03‑set/2026):

Data: 28 de agosto de 2026 (Imagine image API updates: qualidade “auto”, 5 imagens de referência, novos aspect ratios).

O que mudou: parâmetro quality: auto em grok-imagine-image-2.0; edição de imagem aceita até 5 imagens de referência; novos aspect ratios 21:9 e 5:2. Isso impacta medição de custos de geração/edição de imagem e throughput de agentes que usam Imagine.

Fonte primária: xAI Docs – Release Notes (28/ago) — URL: https://docs.x.ai/developers/release-notes.
x

Fonte secundária: não localizado.

Resumo por categoria (o que cada um mudou em busca web, citação, browsing agêntico, memória e comércio)

Busca web / browsing agêntico:

OpenAI: WebMCP (31/ago) para agentes interagirem com apps/sites; GPT‑5.6 com “Deep Research” (multi‑step, relatório citado).
trackerly
+2

Google: Gemini 3.8 Flash focado em agentes e raciocínio multi‑etapa; Enterprise Agent Platform com agentes stateful.
tech-insider
+1

xAI: Grok 4.6 + Grok Bot (11–12/ago) para agentes duráveis e tarefas de coding/agênticas; ferramentas de agente (web_search, x_search, code_execution) já disponíveis.
x
+2

DeepSeek: V4‑Flash‑Vision‑Exp (21/ago) adiciona visão a um modelo já forte em agentes.
deepseek
+2

Citação de fontes:

OpenAI: mudança observada de comportamento de citação (menos Reddit a partir de ~14/ago) e “Deep Research” com relatório citado.
trackerly
+1

Outros: não localizado mudança explícita de política/formato de citação nos lançamentos deste intervalo.

Memória:

Não localizado anúncio de novo recurso de “memória” (long‑term memory, user memory) neste intervalo para os provedores listados.

Comércio (ações em sites, pagamentos, integrações):

OpenAI: WebMCP habilita interação com apps/sites, o que abre caminho para ações de comércio via agente.
x

xAI: Grok Bot com conectores e rotinas; potencial para automação de fluxos que envolvem comércio, mas sem detalhe público de gateways de pagamento neste intervalo.
x
+1

Se quiser, posso montar uma tabela CSV com: modelo, provedor, data, tipo de fonte (primária/secundária), URL da fonte primária, URL da fonte secundária, e colunas para “busca web”, “citação”, “browsing agêntico”, “memória”, “comércio”, “embedding/rerank”, “mudança de API”.

55 fontes
Quais foram os preços anunciados para o Claude Fable 5 1
Qual o impacto da atualização do Gemini 3 8 Flash na API
Quais ferramentas de IA sofreram instabilidade recente
Quais as restrições de acesso ao modelo Mythos 5 1
Como funciona o recurso WebMCP anunciado pela OpenAI
Fontes
55





## Links na página
- https://x.com/OpenAIDevs/status/2094529078863024174
- https://www.anthropic.com/claude/mythos?refid=ft_appflow
- https://docs.x.ai/developers/release-notes
- https://trend.undefined-labs.dev/wiki/entities/xai
- https://coursiv.io/blog/deepseek-v5-release-date
- https://www.orcarouter.ai/blog/qwen-3-8-flash-release