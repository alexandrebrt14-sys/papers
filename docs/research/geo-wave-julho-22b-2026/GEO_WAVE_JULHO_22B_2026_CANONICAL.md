# Wave Julho-22B 2026 · Infraestrutura técnica de GEO: crawlers, controle de acesso e atribuição (22-jul-2026)

**Data:** 22-jul-2026 · **Método:** 2 × Perplexity `sonar-deep-research` (crawlers; atribuição) + 1 subagente web com verificação em documentação oficial (OpenAI, Anthropic, Perplexity, Google, Cloudflare, Stripe). Proveniência em `raw/` (pplx-crawlers.md, pplx-atribuicao.md, web-crawlers-cloudflare-atribuicao.md).

**Precedência:** cadeia atualizada: **Julho-22C §7 > Julho-22B §7 > Julho-22 §7 > Julho §7 > Wave 19 §7 > 15B §8** (as waves 22B e 22C são publicadas no mesmo commit; a cadeia completa está disponível no corpus). Esta wave cobre a camada que faltava: o encanamento (quem rastreia, o que controlar, como atribuir). Para conflito entre fontes DENTRO desta wave, vale a escala de 7 níveis definida na Wave Julho-22 §7.4.

---

## 0. TL;DR — as cinco decisões técnicas que esta wave canoniza

1. **A matriz robots.txt por finalidade substitui o "permitir ou bloquear IA".** Cada provedor tem 2-3 bots com papéis distintos (treino / busca-citação / ação de usuário), documentados oficialmente. Ficar citável sem ceder treino é POSSÍVEL (§2.2), mas não é o default da Brasil GEO: para a tese de visibilidade, o default é liberar tudo, inclusive treino — a matriz restritiva é opção para cliente com conteúdo proprietário sensível (§2.2, condições).
2. **Bloquear Google-Extended NÃO tira o site dos AI Overviews.** AIO e AI Mode usam o Googlebot normal (doc oficial do Google); Google-Extended controla treino do Gemini E grounding (Gemini Apps/Vertex). Controles de exposição em AIO: `nosnippet`, `data-nosnippet`, `max-snippet`, `noindex` (§2.3).
3. **GA4 tem canal default "AI Assistants"** (doc oficial; lançamento reportado em 13-mai-2026): classifica sessões com medium `ai-assistant` (ChatGPT, Gemini, Copilot, Grok etc.) — mas EXCLUI AI Overviews/AI Mode (seguem como Organic Search) e, na doc acessada em 22-jul-2026, NÃO lista a Perplexity. Custom channel group com regex ancorada continua necessário como complemento (§4.1).
4. **O tráfego "dark" de IA é a maior parte do tráfego de IA.** Estudo de vendor (Loamly, 446 mil visitas): ~70,6% das visitas de IA chegam sem referrer e caem em Direct [vendor, ordem de grandeza]. Corolário: relatório de canal de IA baseado só em referrer SUBESTIMA o canal; declarar isso em todo report (§4.2).
5. **Crawl-to-referral é a métrica de troca justa** (crawls consumidos por visita devolvida): Cloudflare mediu Anthropic ~70.900:1 (jun/2025, blog primário) e o painel vivo Radar AI Insights é a fonte para números correntes. Usar na decisão de bloqueio/liberação por bot e nas conversas de licenciamento (§3).

## 1. Contexto: a camada de acesso virou campo de negociação

Entre jul/2025 e jul/2026 a Cloudflare (à frente de >20% dos domínios da web, afirmação própria) transformou o acesso de crawlers de IA em regime de opt-in com preço: bloqueio default para novos domínios (01-jul-2025), Content Signals Policy no robots.txt gerenciado de 3,8M+ domínios (24-set-2025), e — POLÍTICA ANUNCIADA, ainda não vigente — bloqueio default de Training e Agent em páginas com anúncios para novos domínios a partir de 15-set-2026, com crawlers multi-propósito (Googlebot, Applebot, BingBot nomeados) julgados "por todos os seus comportamentos" (anúncio de 01-jul-2026, sujeito a mudança). O Pay Per Crawl evoluiu para Pay Per Use (pagamento quando o conteúdo é usado na resposta; parceiros Ceramic.ai e You.com) [imprensa, post primário não localizado]. Escopo importante: esses defaults valem para domínios NA Cloudflare (novos, nos planos/configurações afetados) — não para a web inteira nem automaticamente para domínios antigos. Consequência para GEO: em sites atrás da Cloudflare, "não apareço no ChatGPT" ganha uma causa possível nova — o próprio CDN bloqueou; auditar o painel AI Crawl Control vira passo padrão de diagnóstico.

## 2. Matriz canônica de crawlers (docs oficiais, acessadas em 22-jul-2026)

### 2.1. Tabela por finalidade

| Provedor | TREINO | BUSCA/CITAÇÃO | AÇÃO DE USUÁRIO | Respeito a robots.txt |
|---|---|---|---|---|
| OpenAI | GPTBot | OAI-SearchBot | ChatGPT-User | GPTBot/OAI-SearchBot sim; ChatGPT-User: regras "podem não se aplicar" (doc oficial) |
| Anthropic | ClaudeBot | Claude-SearchBot | Claude-User | Todos sim (Claude-User inclusive — diferencial); IPs verificáveis em claude.com/crawling/bots.json |
| Perplexity | (doc afirma não treinar) | PerplexityBot | Perplexity-User | PerplexityBot sim; Perplexity-User "generally ignores robots.txt" (texto oficial) |
| Google | Google-Extended (token de controle, sem UA próprio; controla treino Gemini + grounding) | Googlebot (AIO e AI Mode usam o Googlebot NORMAL) | — | Googlebot sim; bloquear Googlebot remove da busca inteira |

### 2.2. Postura canônica Brasil GEO ("citável sem ceder treino")

```
# OPÇÃO RESTRITIVA (cliente com conteúdo proprietário sensível) — NÃO é o default Brasil GEO
User-agent: GPTBot
Disallow: /
User-agent: ClaudeBot
Disallow: /
# Google-Extended: registrar decisão EXPLÍCITA por cliente (não deixar implícito):
User-agent: Google-Extended
Allow: /
# (trocar por Disallow: / apenas se o cliente aceitar reduzir presença no ecossistema Gemini)
```
Condições de aplicação: (a) **default Brasil GEO = liberar tudo, inclusive treino** — presença no corpus paramétrico é ativo (Existence Gap, wave julho-22); a opção restritiva acima é para cliente com conteúdo proprietário sensível; (b) o snippet pressupõe que NÃO há regras globais conflitantes no robots.txt existente (`User-agent: *` com Disallow, paths sensíveis) — sempre auditar o arquivo inteiro antes de colar, ou o efeito real pode ser o oposto do pretendido; (c) Google-Extended: registrar a decisão em linha explícita (acima) para ficar auditável; segundo a doc oficial do Google, o token controla uso em treino de futuras gerações Gemini e em grounding (Gemini Apps / Grounding with Google Search no Vertex) [citação da doc; verificar redação vigente antes de aconselhar, pois o escopo do token já mudou historicamente]; (d) fetchers de usuário: a doc da OpenAI diz que para ChatGPT-User as regras de robots "podem não se aplicar" e a da Perplexity diz que Perplexity-User "generally ignores robots.txt" (textos oficiais) — robots.txt continua sendo o sinal correto a publicar; bloqueio efetivo desses fetchers, quando necessário, é via WAF/CDN.

### 2.3. Regra AIO que desfaz um erro comum de mercado
"Bloquear Google-Extended para não aparecer em AI Overviews" é tecnicamente errado: AIO/AI Mode operam com o Googlebot comum (doc oficial "AI features and your website"). A exposição em AIO se gerencia com nosnippet/data-nosnippet/max-snippet/noindex, com custo direto de visibilidade; para clientes GEO o default é NÃO restringir. Nota sobre o achado acadêmico correlato: o estudo arXiv:2604.27790 (wave julho-22) reporta que sites que bloqueiam "o crawler de IA do Google" são menos recuperados em AIO — evidência OBSERVACIONAL e com termo ambíguo no abstract (não especifica se mediu Google-Extended ou outra diretiva), em aparente tensão com a doc oficial; ler o PDF antes de usar esse achado em aconselhamento, e em conflito prevalece a doc oficial do Google (escala §7.4 da Wave Julho-22).

## 3. Estatísticas de crawl (para calibrar expectativa e negociação)

- Share de AI crawlers (Cloudflare, mai/2025, blog primário): GPTBot 30%, ClaudeBot 21%, Meta-ExternalAgent 19%, Amazonbot 11%, Bytespider 7,2%. Só 14% dos top-10k domínios tinham diretivas de IA no robots.txt.
- Crawl-to-referral (crawls por 1 visita referida): Anthropic ~70.900:1, Mistral ~0,1:1 (Cloudflare, semana 19-26/jun/2025, blog primário de vendor). Nota metodológica: razão menor que 1 (caso Mistral) é possível — a plataforma refere mais visitas do que crawleia na janela medida (cache, corpus prévio, janela curta); não é erro de unidade. Números 2026 citados via agregadores do painel Radar AI Insights [conferir no painel primário antes de publicar]: Anthropic ~4.580:1, OpenAI ~848:1, Perplexity ~186:1, Google ~5:1.
- Panorama 2026 [secundário]: bots ≈ 57,5% do tráfego HTML; ClaudeBot ~20% do AI crawl em jun/2026; treino ≈ metade das requisições de AI crawlers.
- Caso Cloudflare × Perplexity (04-ago-2025, blog primário): crawling furtivo (UA de Chrome/macOS, rotação de ASN, robots ignorado; 3-6M req/dia não declaradas) → delistagem como bot verificado. Perplexity contesta (atribuição a BrowserBase; fetches de usuário) [secundário]. Lição: verificação de bot por IP oficial importa; spoofing de UA é comum nos dois sentidos.
- Leitura operacional: o site deve medir a PRÓPRIA razão crawl-to-referral (requisições de bots de IA nos logs ÷ sessões referidas por plataforma no analytics) antes de decidir bloqueios — é o número que transforma "os bots estão comendo meu conteúdo" em decisão quantificada.

## 4. Atribuição: o protocolo de três camadas

### 4.1. Camada GA4 (o que o analytics vê)
- Canal default **AI Assistants** no Default Channel Group (doc oficial support.google.com/analytics/answer/9756891): a condição documentada é medium = `ai-assistant`, atribuído pelo GA4 quando o referrer bate na lista interna do Google (a doc cita "sources like ChatGPT, Gemini, Deepseek, Copilot, or Grok"); EXCLUI AIO/AI Mode (ficam em Organic Search — indistinguíveis do orgânico clássico no GA4; a separação de impressões só existe no Search Console, sem cliques). A ausência da Perplexity foi observada na doc em 22-jul-2026 [claim volátil — verificar a lista oficial na data de configurar]. Nada a "criar" para esse canal: ele é nativo; verificar na própria propriedade como o tráfego está sendo classificado antes de qualquer regra.
- Complemento: **custom channel group** (não confundir com o canal nativo) cobrindo o que a lista do Google não cobre (Perplexity à frente), com regex ANCORADA por domínio na sintaxe do GA4 — ex.: `^(www\.)?(chatgpt\.com|chat\.openai\.com|claude\.ai|perplexity\.ai|gemini\.google\.com|copilot\.microsoft\.com|grok\.com|meta\.ai|you\.com|poe\.com)$` sobre a dimensão de source (nunca `chatgpt.com` sem escape: casa substring e domínio malicioso). Precisão sobre retroatividade: custom channel groups do GA4 aplicam-se retroativamente aos RELATÓRIOS; o que não retroage é dado não coletado (sessões antigas sem referrer/UTM continuam Direct para sempre) — por isso instrumentar cedo continua valendo.
- UTMs em botões "copiar link" de conteúdo compartilhável, com convenção alinhada ao canal nativo: `utm_source=<plataforma>&utm_medium=ai-assistant` (usar o mesmo medium que o GA4 usa evita fragmentar o canal) [prática nossa, derivada da doc].

### 4.2. Camada logs/CDN (o que o servidor vê)
- Crawl de IA não aparece no GA4; só em logs. Pipeline mínimo: filtrar user-agents da matriz §2.1, validar IP contra listas oficiais (anti-spoofing), computar série semanal de requisições por bot e a razão crawl-to-referral própria.
- Dark traffic: ~70,6% das visitas de IA sem referrer [Loamly, vendor]; conversão do dark AI 10,21% vs 2,46% não-IA no mesmo estudo [vendor]. Implicação de report: o canal de IA visível no GA4 é o PISO, não o teto; nunca reportar "IA = X% do tráfego" sem a nota do dark traffic.

### 4.3. Camada declarada/experimental (o que o cliente diz e o que o experimento prova)
- Campo "como nos conheceu?" com opção explícita de IA/ChatGPT em todo formulário de lead (autoatribuição recupera o que referrer perde).
- Brand search lift em janela de 7 dias pós-menção relevante; e, para intervenção de conteúdo, o controle on-domain da wave julho-22 (§2.3 de lá) como desenho padrão.
- Benchmarks de conversão de referral de IA para contexto (todos com metodologia distinta, nunca somar): Similarweb 7,1% (clickstream); Seer B2B: ChatGPT 15,9%, Perplexity 10,5% vs 1,76% orgânico [secundário]; faixa canônica por vertical da Wave Julho §7.3 permanece a regra de citação.

## 5. Aplicação por repositório

### 5.1. `landing-page-geo`
- Auditar o robots.txt do site e dos clientes contra a matriz §2.2 e registrar a decisão por bot (inclusive linha explícita de Google-Extended) num bloco comentado do próprio robots.txt.
- Verificar como o canal nativo AI Assistants está classificando o tráfego na propriedade GA4 e criar o custom channel group com a regex ancorada do §4.1 (dado não coletado não volta — quanto antes, mais série histórica); adicionar a nota de dark traffic no template de report do painel /admin.
- Incluir a razão crawl-to-referral própria no roadmap de medição (fonte: logs Vercel/Cloudflare, quando disponíveis).

### 5.2. `papers`
- O caso Cloudflare×Perplexity e as razões crawl-to-referral são material direto para a discussão de "custo do ecossistema" nos papers (economia da atribuição); citar os posts primários da Cloudflare com data.
- A distinção treino/busca/ação-de-usuário (§2.1) deve entrar no desenho de qualquer experimento futuro que manipule acesso de bots (variável de confusão: bloquear treino ≠ bloquear citação).

### 5.3. `curso-factory`
- Aula candidata: "O encanamento do GEO: crawlers, robots.txt e atribuição" (matriz §2.1, erro comum do Google-Extended §2.3, protocolo de 3 camadas §4) — altamente prática e sem concorrência em pt-BR.
- O template `docs/templates/seo-geo-2026/robots.txt` do repo deve ser atualizado para a matriz por finalidade com comentários das condições (a).

## 6. Claims machine-readable (novo padrão, pedido da crítica GPT da wave julho-22)

```yaml
claims:
  - id: b1
    claim: "AIO e AI Mode usam o Googlebot normal; Google-Extended nao controla AIO"
    fonte: "developers.google.com/search/docs/appearance/ai-features"
    tipo_fonte: doc_oficial
    confianca: alta
    valido_em: 2026-07-22
    revisar_ate: 2026-10-31
  - id: b2
    claim: "GA4 tem canal default AI Assistants (condicao medium=ai-assistant); exclui AIO/AI Mode; Perplexity ausente da lista na doc em 22-jul-2026 (volatil)"
    fonte: "support.google.com/analytics/answer/9756891 (acesso 2026-07-22)"
    tipo_fonte: doc_oficial
    confianca: alta_exceto_lista_de_sources_media
    valido_em: 2026-07-22
    revisar_ate: 2026-10-31
  - id: b3
    claim: "ChatGPT-User e Perplexity-User podem ignorar robots.txt (texto das docs oficiais)"
    fonte: "developers.openai.com/api/docs/bots; docs.perplexity.ai/guides/bots"
    tipo_fonte: doc_oficial
    confianca: alta
    valido_em: 2026-07-22
    revisar_ate: 2026-12-31
  - id: b4
    claim: "~70,6% das visitas de IA chegam sem referrer (dark traffic)"
    fonte: "loamly.ai/blog/state-of-ai-traffic-2026-benchmark-report (446k visitas)"
    tipo_fonte: vendor
    confianca: media
    valido_em: 2026-07-22
    revisar_ate: 2026-09-30
  - id: b5
    claim: "POLITICA ANUNCIADA (nao vigente): Cloudflare bloqueara Training/Agent por default em paginas com anuncios para novos dominios a partir de 15-set-2026"
    fonte: "blog.cloudflare.com/content-independence-day-ai-options/ (01-jul-2026)"
    tipo_fonte: blog_primario_vendor
    confianca: alta_como_anuncio
    valido_em: 2026-07-22
    revisar_ate: 2026-09-15
  - id: b6
    claim: "Crawl-to-referral Anthropic ~70.900:1 (snapshot jun/2025); numeros correntes conferir no painel primario Radar AI Insights"
    fonte: "blog.cloudflare.com/ai-search-crawl-refer-ratio-on-radar/"
    tipo_fonte: blog_primario_vendor
    confianca: alta_para_2025_media_para_2026
    valido_em: 2026-07-22
    revisar_ate: 2026-08-31
```

## 7. Correções e conflitos
- Revogação PARCIAL e específica: fica revogado do corpus qualquer claim que afirme ou sugira que (a) "bloquear Google-Extended remove o site de AI Overviews" ou (b) que AI Overviews dependem de crawler distinto do Googlebot. Nada mais das waves anteriores é alterado.
- NOVO fato que refina a Wave Julho §2.4 (Search Console): a separação de impressões de AIO/AI Mode existe no GSC, mas no GA4 esse tráfego segue indistinguível dentro de Organic Search — os dois sistemas não se conciliam hoje; reports devem tratar GSC e GA4 como visões complementares não somáveis.
- Padronização de proveniência desta wave: blogs e changelogs da Cloudflare = fonte primária de vendor (snapshots datados); o painel Radar AI Insights = fonte primária viva que prevalece sobre qualquer snapshot; agregadores que citam o Radar = secundários. Números de crawl share e ratios mudam mês a mês; nenhum número do §3 deve ser citado sem data.
