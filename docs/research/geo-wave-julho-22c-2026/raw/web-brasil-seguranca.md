# Pesquisa web — GEO no Brasil + segurança agêntica (22/07/2026)

Fonte: subagente de pesquisa web; rótulos [CONFIRMADO]/[SECUNDÁRIO]. Conteúdo integral do levantamento (blocos A e B) preservado como proveniência da Wave Julho-22C.

## BLOCO A — Brasil

### Google no Brasil
- Modo IA em pt-BR desde 08/09/2025 (Gemini 2.5 customizado; blog.google/intl/pt-br; CNN Brasil; Meio & Mensagem) [CONFIRMADO].
- I/O 2026: caixa de busca com IA agêntica, AI Mode com Gemini 3.5 Flash default; rollout inclui Brasil [CONFIRMADO].
- Universal Commerce Protocol (UCP): checkout direto no AI Mode/Gemini; rollout global desde 19/05/2026 nos mercados com AI Mode, incluindo Brasil (Mobile Time; NRF 2026) [CONFIRMADO].
- Evento SP 24/03/2026: estratégia B2A (business-to-agents), agentes em português para Ads/Analytics, anúncios contextuais em conversas de IA, agendamento de reservas no AI Mode; estruturar dados via Merchant Center e Ads Data Manager (Mobile Time) [CONFIRMADO]. "Google for Brasil 2026" nomeado: não encontrado.
- Agentic booking exclusivo de AI Pro/Ultra [SECUNDÁRIO].

### Penetração
- Brasil 3º maior usuário de ChatGPT do mundo (relatório da OpenAI, ago/2025): ~140M mensagens/dia de ~2B globais; 2º em devs usando API (Fast Company Brasil, Softex, Olhar Digital) [CONFIRMADO].
- Datafolha + Observatório Fundação Itaú (jul-ago/2025): 93% usam alguma ferramenta com IA, só 54% entendem o termo; classe A 69% vs D/E 16% em IA generativa [CONFIRMADO].
- "Mapa da Busca no Brasil 2026" (Optimiza/Adnews): 46,5% usam ChatGPT/Gemini/Copilot com frequência no processo de decisão de compra (23% diário, 23,5% semanal) [SECUNDÁRIO].
- Mobile Time/Opinion Box (12/06/2026): 15% deixariam agente comprar em seu nome; 67,3% delegariam busca de informação [SECUNDÁRIO].
- ~40% com smartphone usam só buscadores; 1 em 4 usa buscador e IA igualmente; 2,2% só chatbots [SECUNDÁRIO].

### Imprensa × IA
- Estadão × Google (10/12/2025): 1º licenciamento de notícias para IA no Brasil (feed factual p/ Gemini; exclui opinião/colunas/agências) [CONFIRMADO].
- Folha × Google: acervo + feed p/ Gemini, fixo + variável, News Pilot [CONFIRMADO].
- Folha + UOL × OpenAI (25/05/2026): 1º acordo com a OpenAI no Brasil; notícias em tempo real no ChatGPT; ENCERRA a ação da Folha (ago/2025) contra a OpenAI; inclui ChatGPT Enterprise/API/Codex [CONFIRMADO].
- ANJ + Abert + Aner + 9 entidades notificaram Google, Microsoft, Amazon, Meta, Apple e OpenAI em 22/12/2025 propondo remuneração [CONFIRMADO].
- CADE: inquérito sobre impacto da IA do Google no jornalismo virou processo administrativo em abr/2026 [CONFIRMADO].
- Não encontrado: acordo/processo da Globo; posição formal da Abraji.

### Regulatório
- PL 2338/2023: NÃO aprovado na Câmara até 22/07/2026 (aprovado no Senado 10/12/2024; adiamentos sucessivos; votação marcada 27/05/2026 não confirmada; indício de novo adiamento p/ dez/2026 via DIAP) [CONFIRMADO o não-aprovado]. Modelo de risco, SIA, multas até R$ 50M. PL 2688/2025 paralelo [SECUNDÁRIO].
- ANPD: sandbox regulatório de IA (piloto desde fev/2026, 3 empresas: Metatext, Synapse AI, IA Greenworld); Radar Tecnológico sobre IA generativa; Mapa de Temas Prioritários 2026-2027 [CONFIRMADO].
- CONAR: Guia de Influenciadores nova edição 12/05/2026 (efeitos 01/06/2026): responsabilidade solidária pela veracidade de conteúdo gerado/editado com IA; adequação ao ECA Digital (Lei 15.211/2025) [CONFIRMADO].

### Mercado GEO BR
- Agências: Wyse, Bloomin, Geostack (R$ 1.497–4.491/mês); <5% das agências oferecem GEO estruturado; ~1,2% das empresas otimizam p/ IA (números autorreferidos do setor) [SECUNDÁRIO].
- Ferramentas locais: Tropk, Promptado [SECUNDÁRIO].
- Eventos: Web Summit Rio 8-11/06/2026 (IA eixo central); SEO Summit 13-14/11/2026 SP ("SEO na era das IAs") [CONFIRMADO]. Painel rotulado "GEO": não encontrado.
- Mercado IA generativa BR: US$ 371,2M (2025) → US$ 1,48B (2034) [SECUNDÁRIO].

## BLOCO B — Segurança agêntica

### Prompt injection em browser-agents
- Brave × Comet (ago/2025): indirect prompt injection via página (texto branco, comentários HTML, post de Reddit) → agente acessa e-mail logado, captura OTP, exfiltra (brave.com/blog/comet-prompt-injection) [CONFIRMADO]. Out/2025: injeções invisíveis em screenshots/imagens (unseeable-prompt-injections; Simon Willison 21/10/2025) [CONFIRMADO].
- CometJacking: comandos em parâmetros de URL → lê memória, base64, exfiltra (PPC Land, Medianama, out/2025) [CONFIRMADO].
- ChatGPT Atlas (out/2025, macOS): hijack via Google Docs demonstrado em horas; OpenAI (dez/2025): prompt injection "dificilmente será totalmente resolvido"; programa de hardening com red teaming por RL (openai.com/index/hardening-atlas-against-prompt-injection) [CONFIRMADO].
- In the wild: Unit 42 documentou IPI web; arXiv 2604.27202 mapeia prevalência; categorias observadas (via Google, abr/2026): manipulação de SEO, dissuasão de agentes, exfiltração, pegadinhas destrutivas [CONFIRMADO].

### OWASP e defesa
- Versão vigente em 2026 = OWASP Top 10 for LLM Applications 2025 (genai.owasp.org); NÃO existe edição "2026"; LLM01 = Prompt Injection incl. indireta [CONFIRMADO].
- Microsoft (mar/2026): defesa contra IPI — privilégios mínimos/curta duração, separação de privilégios (learn.microsoft.com) [CONFIRMADO]. Google (abr/2026): defesas determinísticas, sanitização de URLs/HTML/Markdown, confirmação de usuário [SECUNDÁRIO na data].
- Guia canônico "agent-friendly sem virar vetor" para publishers: NÃO EXISTE como padrão único; práticas derivadas: sanitizar UGC exibido, não hospedar instruções invisíveis (Google trata como spam), usar identidade de agentes (B3).

### Identidade de agentes
- Web Bot Auth (IETF): assinatura por requisição via HTTP Message Signatures (RFC 9421), Ed25519, header Signature-Agent, diretório JWKS; WG formal criado no início de 2026; apoio Cloudflare, Amazon, Akamai, OpenAI [CONFIRMADO; marcos exatos SECUNDÁRIO].
- Cloudflare Signed Agents (ago/2025): 1ª coorte ChatGPT, Blocks, Anchor Browser, Browserbase [CONFIRMADO]. Registry aberto de agentes com Amazon Bedrock AgentCore (fev/2026) [CONFIRMADO].

### Fraude em comércio agêntico
- Akamai "Securing the Agentic Storefront" (15/07/2026): 47,9% do tráfego de commerce na rede Akamai é de bots de IA (dez/2025); treino >70% dos gatilhos; OpenAI/ByteDance/Anthropic top-3; agent hijacking de credenciais salvas; identidade sintética; >90% da atividade só em modo monitorar [CONFIRMADO].
- Stripe/OpenAI ACP: Shared Payment Tokens de uso único e escopo restrito; sinais de risco compartilhados; Radar; opt-in do merchant [CONFIRMADO].
- 65% do bad bot traffic mira e-commerce; login attacks +216% em 2025; US$ 48B/ano em fraude [SECUNDÁRIO].

## Lacunas declaradas
Votação do PL 2338 na Câmara (não ocorrida/não confirmada); Globo × IA; posição Abraji; pesquisa Ilumeo; "Google for Brasil 2026" nomeado; painel "GEO" em evento BR.

## Fontes (seleção)
blog.google/intl/pt-br · cnnbrasil.com.br · mobiletime.com.br · conversion.com.br · fastcompanybrasil.com · adnews.com.br · tecmundo.com.br · meioemensagem.com.br · poder360.com.br · teletime.com.br · pt.globalvoices.org · gov.br/anpd · conar.org.br · migalhas.com.br · seosummit.com.br · exame.com · brave.com/blog · openai.com/index/hardening-atlas-against-prompt-injection · genai.owasp.org · learn.microsoft.com · datatracker.ietf.org (draft-meunier-web-bot-auth-architecture) · blog.cloudflare.com/signed-agents · stripe.com/newsroom · globenewswire.com (Akamai 15/07/2026)
