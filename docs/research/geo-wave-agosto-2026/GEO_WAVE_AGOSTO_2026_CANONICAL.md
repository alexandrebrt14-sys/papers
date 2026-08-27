# Wave Agosto 2026 · GEO + SEO: estado da arte, frameworks de execução, KPIs e reports (27-ago-2026)

**Data:** 27-ago-2026 · **Janela:** delta 22-jul → 27-ago-2026 · **Método:** 10 rodadas em 5 provedores com web ao vivo — Perplexity `sonar-pro` ×6 (as 4 rodadas `sonar-deep-research` em paralelo penduraram sem resposta e foram substituídas pelo `sonar-pro` sequencial), Gemini 3.1 Pro grounding ×2, OpenAI `gpt-5.5` Responses + `web_search` ×1, xAI `grok-4.6` Responses + `x_search` ×1 (o endpoint `chat/completions` com `search_parameters` devolve `410 Gone`; a xAI migrou para a Agent Tools API) — mais doublecheck do Claude em fonte primária: 5 arXiv IDs de jul–ago conferidos na página do arXiv, 5 anteriores na API, e 30 URLs abertas com string-sentinela. Proveniência em `raw/`.

**Precedência:** cadeia vigente: **Agosto §8 > Julho-22C §7 > Julho-22B §7 > Julho-22 §7 > Julho §7 > Wave 19 §7 > 15B §8**. Esta wave fecha o ciclo de julho com três eixos que o corpus pedia: (a) frameworks de EXECUÇÃO e de REPORT com fonte de vendor datada; (b) mudanças de comportamento dos motores no período (ChatGPT `site:`, Preferred Sources, Cloudflare 15-set, Ads no Brasil); (c) a camada semântico-vetorial com paper controlado (diversidade > redundância) e o alerta de detecção de conteúdo sobre-otimizado (GEO-Flag).

---

## 0. TL;DR — o que muda para uma operação de GEO brasileira

1. **O motor decide QUEM pesquisar antes de pesquisar.** Desde 08-ago-2026, 16–17% das fan-out queries do ChatGPT Search levam operador `site:` (antes 0,3–0,5%; medição Promptwatch relatada por Simon Willison em 20-ago; primária do vendor de medição, não da OpenAI). Consequência: existe uma "lista de domínios candidatos" por tema; quem não está nela não é visto. Junto com a queda das citações ao Reddit no ChatGPT (≈12% em julho → 3% em meados de agosto; Similarweb 23-ago), o sinal é de preferência por domínios estabelecidos e temáticos (§2.2).
2. **Google publicou, em documento oficial, o que ignora:** `LLMS.txt` e "markup especial" ("Google Search ignores them"), chunking ("no requirement to break your content") e reescrita "para IA"; e disse que criar páginas por variação de fan-out para manipular respostas viola a política de scaled content abuse. John Mueller (24-ago): "there's nothing really special you need to do for generative AI responses in search". Para Google, **GEO = SEO + fundamentos** (§2.1). Isso REBAIXA o `llms.txt` (§8.b).
3. **Preferred Sources (20-ago) é alavanca nova e mensurável**: fonte escolhida pelo usuário ganha badge em Top Stories, AI Overviews e AI Mode onde disponível. Vira campanha de ativação de audiência para publishers e marcas com base própria (§2.1).
4. **Mídia paga entrou nas superfícies de IA no Brasil**: ChatGPT Ads lançado em UK, México, **Brasil**, Japão e Coreia em 11-ago-2026 (OpenAI, primária); Similarweb lançou AI Ads (13-ago) para ver anúncios em ChatGPT, AI Mode e AIO. Todo report passa a separar **orgânico citado × referral × pago em IA** (§5.3).
5. **Volume de prompt não existe como dado.** Ahrefs (17-ago) declarou não haver fonte confiável de volume real de prompts e passou a usar "AI adjusted volume" (proxy derivado do volume Google × razão IA/orgânico); a partir de 31-ago só o proxy. Rand Fishkin (12-ago) alerta que análise de citação engana porque o modelo "já sabe" que marcas vai recomendar. **Nunca vender volume de prompt como medida** (§5.2).
6. **Infra vira prazo:** Cloudflare muda os defaults em **15-set-2026** — para domínios novos, bots classificados como Training e Agent bloqueados em páginas com anúncios; Search continua liberado (doc oficial). Auditoria de "AI crawl readiness" antes de setembro é entregável urgente (§2.6).
7. **Camada vetorial com evidência controlada:** documentos DIVERSOS melhoram a resposta do gerador; duplicatas e paráfrases NÃO (`2608.13956`, 14-ago, experimento controlado com FictionalQA). Para GEO: cobertura de evidência variada (dados próprios, tabela, definição, caso) vale mais que repetir o mesmo parágrafo em 5 páginas (§6).
8. **Conteúdo sobre-otimizado é detectável — e vai ser filtrado.** GEO-Flag (`2608.16824`, 17-ago) cria benchmark de 3.200 instâncias e detector com F1 0,944; estima prevalência de conteúdo GEO-otimizado de 8,90% nas páginas recuperadas por Google/Gemini para 1.000 queries reais, 16,36% entre páginas modificadas em 2026. O anti-padrão "pseudo-GEO" dos 50 Conceitos ganha instrumento de medição do outro lado (§6.3).
9. **Não existe "core update de agosto de 2026".** O único evento registrado é um spam update (18–20-ago, ≈2,5 dias) [secundário: The First Ranker, SEJ, Storyboard18; o histórico do Search Status Dashboard devolveu 404 na verificação]. Quem chamar as quedas de agosto de "core" está errado (§8.d).
10. **Relatório por URL substitui score genérico**: Conductor Pages Report (23-jul) une AI visibility, ranking, tráfego, saúde técnica, changelog e conversão por página; Ahrefs Brand Radar 2.0 (ago) traz Cited Domains/Cited Pages com exportação. O "GEO URL Ledger" (§5.4) é o formato de report que este corpus adota.

---

## 1. Corpus científico — papers verificados (jul–ago 2026)

Todos os IDs abaixo foram abertos em `arxiv.org/abs/<id>` ou na API em 27-ago-2026; título e data conferem. PDFs NÃO lidos — ler antes de citar número em copy ou paper. Marcação: ✓ = abstract lido; ○ = só título/data.

| arXiv | Data | Título (autores) | Achado com número | Uso |
|---|---|---|---|---|
| `2608.16824` ✓ | 17-ago-2026 | GEO-Flag: Detecting and Measuring GEO-Optimized Web Content (Chu, Leng, Li, Shen, Shen, Zhang) | GEOFlagBench: 3.200 instâncias, 400 queries, 4 domínios, 8 famílias de otimizador. Melhor baseline F1 0,880 com atalhos de autoria; Intervention-Paired Training sobe F1 de 0,862 → 0,944 e worst-group accuracy 0,725 → 0,883 (ModernBERT). Prevalência de GEO em 10.095 páginas de Google + Gemini-grounded para 1.000 queries reais: **8,90%; 16,36% entre páginas modificadas em 2026**. Agente "GEO-gated" audita tier da fonte e verificabilidade das URLs citadas. | Anti-padrão 1 (pseudo-GEO) agora tem detector; auditoria de risco de sobre-otimização (§6.3). |
| `2608.13956` ✓ | 14-ago-2026 | How retriever redundancy and diversity impact RAG effectiveness | Experimento controlado (FictionalQA, o modelo não sabe a resposta de cor): duplicatas e paráfrases por LLM NÃO melhoram correção; documentos DIVERSOS (gêneros diferentes com a informação em formas diferentes) melhoram significativamente. | Base da regra "diversidade de evidência > repetição" (§6.1). |
| `2608.03527` ○ | 04-ago-2026 | Training Documents Reranker with Search Rubrics for Deep Research Agent | Reranker treinado com rubricas de busca: +2,6 pontos sobre o baseline mais forte em 4 benchmarks de deep research; generaliza a 5 benchmarks RAG [via resumo do Perplexity; conferir no PDF]. | Rubrica editorial vira sinal de rerank: o que o brief exige é o que o motor pontua (§6.2). |
| `2608.03487` ○ | 04-ago-2026 | RAG-Stack: Co-Optimizing RAG Serving Performance and Quality | Fronteira de Pareto qualidade×desempenho cobre 52,5%–153,2% mais espaço que SOTA com o mesmo número de iterações [via resumo; conferir]. | Custo/latência/qualidade são co-otimizados; não existe "só precisão" (§6.2). |
| `2608.02011` ○ | 03-ago-2026 | Before Reasoning Can Fail: Pre-Evidence Procedural Failures in Agentic RAG | Falhas de procedimento ANTES de a evidência chegar ao raciocínio. | Reforça a Wave Julho-22: muitos problemas de citação são de pipeline, não de texto (§6.2). |
| `2606.00898` ✓ (v2 08-ago) | 30-mai-2026, rev. 08-ago | Citation Grounding Measures the Oracle: Graph Coverage Determines Reported LLM Hallucination Rates in Law (Ovcharov) | 400 respostas × 2 snapshots do MESMO grafo de citações: snapshot esparso (4,7e5 registros) dá grounding 0,791–0,855 ("15–21% alucinado"); snapshot denso (3,3e8) dá 0,989–0,999 nas MESMAS respostas. A métrica mede a cobertura do grafo, não o modelo. | Toda "taxa de alucinação/citação fabricada" que publicarmos precisa declarar a cobertura do índice usado para verificar (§5.2). |
| `2607.14035` ✓ | 15-jul-2026 | Optimizing Visibility in Generative Engines: A Critical Survey of GEO (2023–2026) | 45 estudos. "Already-retrieved content can causally alter its citation or use, but no reviewed technique shows a stable, longitudinal, cross-platform causal effect on organic discoverability or downstream behavior." Reescritas voltadas a citação podem PREJUDICAR recuperação (ppc.land: até −16% na presença top-10 em body-only rewrites). | Já é a espinha da Wave Julho-22; aqui só confirma que o mercado a absorveu (Mueller, Google guide). |
| `2606.20065` ○ | 18-jun-2026 | Generative Engine Optimization at Scale: Measuring Brand Visibility Across AI Search Engines (Ranqo) | Marcas globais 73% / mid 44% / nicho 11%; listicles ≈21% das citações. | Julho-22 §3; base do argumento earned media para PME (§4). |
| `2606.04362` ○ | 03-jun-2026 | Disentangling AEO from Platform Growth: Log-Based Natural Experiment on ChatGPT | glasp.co: 5,7× bruto vira 1,63× na razão e 1,82× no modelo; placebo p=0,16. | Julho-22 §2; controle on-domain obrigatório em todo "case" (§5.2). |
| `2605.06635` ○ | 07-mai-2026 | Cited but Not Verified: Source Attribution in LLM Deep Research Agents (Onweller et al.) | Validade de link >94%, mas precisão factual 39–77% [via Gemini; conferir]. | "Link válido ≠ afirmação correta": rubrica de absorção (Julho-22 §2.4). |

**Não localizado na janela** (afirmar ausência, não inventar): paper primário sobre tamanho ideal de chunk para GEO; estudo controlado headings-pergunta × neutros; medida primária de "densidade de entidade"; paper de citação por LLM com números novos além dos acima. O Gemini citou "Dino et al., auditoria censitária local (4.776 negócios × 2.208 respostas)" e "Martinez et al., survey crítico" **sem ID verificável** — o segundo é provavelmente `2607.14035` (autoria a confirmar); o primeiro fica como PENDENTE.

---

## 2. Motores de resposta — o que mudou (22-jul → 27-ago)

### 2.1. Google (fontes primárias abertas em 27-ago)

- **Guia oficial "AI features and your website"** (Search Central, vigente): "You don't need to create new machine readable files, AI text files, markup, or Markdown to appear in Google Search (including its generative AI capabilities), as Google Search itself doesn't use them. […] Doing so will neither harm nor help your site's visibility or rankings in Google Search, as Google Search ignores them." Idem para chunking. Define **query fan-out** (consultas concorrentes geradas pelo modelo) e avisa que criar conteúdo por variação de fan-out "primarily to manipulate rankings or generative AI responses" viola a política de scaled content abuse.
- **John Mueller, 24-ago (via SEJ):** "from our POV there's nothing really special you need to do for generative AI responses in search". AIO/AI Mode puxam do índice regular + fan-out.
- **Preferred Sources, 20-ago (doc oficial + blog):** botão interativo; fontes preferidas podem aparecer com badge em Top Stories, AI Overviews e AI Mode onde o recurso existir. Alavanca de audiência própria: newsletter, app, comunidade → "adicione como fonte preferida" → medir brand/direct.
- **Goto URLs, 26-ago (declaração do Google a Barry Schwartz, SERoundtable):** redirecionamentos server-side nos links do resultado, "long history of deploying technical measures" contra scrapers. Afeta rank trackers e qualquer medição própria por scraping de SERP — declarar em report quando a série quebrar.
- **Spam update de agosto** (18–20-ago, ≈2,5 dias) [secundário; dashboard 404 na verificação]. **Nenhum core update em agosto** (§8.d).
- **AI Overviews: 2,5 bilhões de usuários/mês** (Pichai, earnings; via Motley Fool 21/25-ago) [primária citada em secundária]. **AI Mode: 1 bilhão de MAU** (I/O 2026) — mas painel de tráfego terceiro estima **0,13% das visitas relacionadas a busca nos EUA** (AnythingEngineOptimization, 03-ago) [secundário; universos diferentes, ver §8.c].
- **Search Console "Search Generative AI Performance"**: rollout acelerado em jul–ago para mais países (EUA, Índia, Suíça, França 22-jul), ainda **só impressões**, sem cliques nem queries [secundário]; toggle de opt-out de AIO/AI Mode/Discover AI sem afetar ranking tradicional [secundário]. Generative UI começou a chegar em AI Overviews (anúncio 19-ago) [secundário]; imagens geradas por IA dentro de AIO (14-ago, SERoundtable) [secundário].
- **AI Max no Google Ads (20-ago, blog oficial):** novas ferramentas de teste/planejamento; em setembro, testes A/B de orçamento e ROI multi-campanha.
- **Gemini Spark** (agente pessoal 24/7) disponível no Brasil para Ultra/Pro desde 31-jul (blog Google Brasil, primária); **Auto Browse no Chrome Android** para Pro/Ultra nos EUA (18-ago, blog Google, primária): o agente opera o Chrome real do usuário, com sessão autenticada.

### 2.2. ChatGPT / OpenAI

- **`site:` em escala (08-ago):** fan-out queries com operador `site:` saltaram de 0,3–0,5% para 16–17% ao dia, alinhado ao rollout do GPT-5.6 (Promptwatch; Simon Willison 20-ago; o campo `search_queries`, antes `search_model_queries`, é visível na resposta do navegador — Suganthan). Leitura de GEO: existe uma etapa de **seleção de domínio candidato** antes da busca. Sinais para entrar na lista: entidade consistente, tema focado, autoridade de terceiros.
- **GPT-5.6 Sol melhorado; GPT-5.6 Luna default para Free/Go (06-ago, blog OpenAI, primária).** Release notes de 07–08-ago: "further improvements to search in ChatGPT" (help center, primária).
- **Citações ao Reddit: ≈12% (jul) → 3% (meados de ago) no ChatGPT Search** (Similarweb, 23-ago, primária do vendor). Um analista reporta quedas de 88% Reddit / 84% arXiv / 78% YouTube após o GPT-5.6 [secundário, não verificado]. Regra: nunca depender de uma comunidade como fonte.
- **ChatGPT Ads no Brasil (11-ago, OpenAI, primária):** "ChatGPT Ads has now launched in the United Kingdom, Mexico, Brazil, Japan, and South Korea"; a OpenAI afirma que anúncios não alteram respostas.
- **Referral do ChatGPT "quase triplicou" após mudança de UX de 07-mai** (Similarweb, 20-ago) — **URL devolvida pelo OpenAI deu 404**; tratar como [secundário; localizar a peça antes de citar].
- **Comércio:** Shipt lançou compra dentro de ChatGPT e Claude (18-ago) [secundário]; reservas via OpenTable/Resy/Yelp (10–14-ago) [secundário]. **Atlas descontinuado (09-ago) e browsing agêntico integrado ao app/extensão** [secundário, sem primária localizada].

### 2.3. Perplexity

- Comet em todas as plataformas (iOS para todos em 24-ago; release notes via agregador) e Comet Plus US$ 5/mês com conteúdo de publishers [secundário].
- **9º Circuito (04-ago) revogou a liminar da Amazon contra o agente de compras Comet** — quem acessa o servidor é o usuário, não a Perplexity (CFAA). Reuters citada; a página exigiu login (401) na verificação [primária judicial não aberta; secundárias concordantes].
- Deck de ads: 230 M usuários/mês, "charter partners" para lançamento de ads no Q4 [primária do vendor via deck.gallery]. Bloqueou anúncios em markdown do Time.com por "deceptive" para agentes (Digiday, 11-ago).
- Comportamento: 3–10 fontes por resposta, peso em primárias. Em painel de 12 sites/90 dias, Perplexity = 2,7% do tráfego de IA vs ChatGPT 91,2% [secundário, amostra pequena].

### 2.4. Microsoft / Bing / Copilot

- **Playbook "Prepare for the Age of AI Shopping" (blog Microsoft Advertising, 21-ago, primária):** descoberto por agentes → escolhido (AI-native ads, Copilot Checkout, Brand Agents) → medido (AI referrals). **Copilot Checkout limitado a merchants em inglês vendendo em USD nos EUA** [secundário concordante]. Configuração no Microsoft Merchant Center (política de devolução, suporte, atributos de feed UCP) [secundário].
- **AI Max no Bing Ads em rollout global (20–21-ago)**; Max CPC deixa de existir para campanhas novas com lances automáticos a partir de 01-out-2026 [secundário].
- Bing Webmaster Tools tem relatório próprio de citações em IA (help doc) — camada 2 de medição sem custo.

### 2.5. Claude, Grok, DeepSeek, Apple

- **Marca d'água de texto do Claude (14-ago, Anthropic, primária):** modelos lançados na UE em ou após 02-ago-2026 suportam marcação legível por máquina, imperceptível, sem caracteres extras, sem identificar usuário/organização. Contratos de conteúdo precisam prever disclosure e o risco de o cliente entender errado o que a marca faz (Ahrefs comentou em 14-ago).
- Conversas compartilhadas do Claude apareciam na busca do Google; Anthropic bloqueou indexação (29-jul → ago) [secundário]. Busca em conversas passadas para Max/Team/Enterprise (12-ago) [secundário].
- **Grok 4.6 (12-ago)** com live-search como tool [secundário]; a API xAI descontinuou `search_parameters` — Agent Tools API (`/v1/responses` + `x_search`/`web_search`) é o caminho (verificado nesta sessão: `410 Gone` no antigo).
- **DeepSeek V4 Pro-0813** (12–13-ago; 1 M tokens; Harness v0.1 MIT) [secundário: Reuters, Unite.ai]. **Nenhum Llama na janela** [secundário]. Claude 5 / Fable / Mythos: sem lançamento localizado na janela pelas rodadas.
- Apple testa assistente de compras no app Apple Store (24-ago) [secundário].

### 2.6. Infraestrutura e acesso

- **Cloudflare, 15-set-2026 (doc oficial, "Last updated Jul 1, 2026"):** "bots classified as Training or as Agent will be blocked on pages that display ads, and Search will remain allowed" para domínios novos; crawlers mistos podem ser bloqueados quando Training está bloqueado. Complementa a matriz de crawlers da Julho-22B §2.1: o cliente com ads e domínio novo precisa decidir explicitamente Agent (ChatGPT-User, Claude-User, Perplexity-User).
- Similarweb (23-ago): AI search caminha para RAG em tempo real, feeds estruturados, clareza de entidade e controles de bot — feeds (Merchant Center Google/Microsoft) entram no checklist técnico.

---

## 3. Vendors e colunas — lançamentos e estudos datados

| Data | Quem | O quê | Número/feature | Fonte |
|---|---|---|---|---|
| 23-jul | Conductor | **Pages Report** | AI visibility + ranking + tráfego + engajamento + saúde técnica + changelog + conversões **por URL** | primária ✓ |
| 24-jul | Ahrefs | 5 AI Search Trends | demanda de medição: "ai search tracking" +184%, "ai rank tracking" +175%; retorno do programmatic SEO | primária ✓ |
| 27-jul | Ahrefs | Google Doesn't Punish AI Content | 5,3% das páginas top-ranking 100% IA; 9% com ≥80% IA | primária ✓ |
| 27-jul | Semrush | Find AI visibility gaps | gaps por prompt, tópico, fonte e narrativa; ChatGPT, Gemini, AIO, AI Mode (+Perplexity em Brand Performance) | primária ✓ |
| 27-jul | Semrush | AI visibility ROI | ROI direto, assistido, **autodeclarado** ("como nos conheceu") e modelado; janelas 30/60/90 dias | primária ✓ |
| 29-jul | Conductor | Content API | outline, draft, meta, scoring AEO/SEO dentro do CMS | primária ✓ |
| 29-jul | Victorious/SEJ | AI Recognizes 96% of Brands But Mentions Almost None | correlação mais forte com referring domains e menções de terceiros | secundário ✓ |
| 30-jul | Semrush | Digital PR for AI visibility | métricas: citation lift, AI share of voice, competitive citation displacement | primária ✓ |
| 05-ago | Semrush/SEL | Does topical focus make your brand more visible | dataset EUA jan–jun/2026: foco temático correlaciona com visibilidade | secundário (SEL 403 na verificação) |
| 08-ago | SEJ | AI's Impact Is Outrunning Measurement | um rank tracker não cobre a superfície de IA; painel multiassistente | secundário |
| 10-ago | Semrush | Traffic Is Down — Now What? | SEO como visibilidade + demanda + conversão | primária |
| 13-ago | Similarweb | **AI Ads** no Ad Intelligence | anúncios em ChatGPT, AI Mode, AIO; 10.000 maiores anunciantes dos EUA no lançamento | primária ✓ |
| 14-ago | Ahrefs | Claude Now Watermarks Everything It Writes | leitura para marketing da marca d'água | primária |
| 17-ago | Ahrefs | **AI adjusted volume** | sem fonte confiável de volume real de prompt; proxy = volume Google × razão IA/orgânico; só o proxy após 31-ago | primária ✓ |
| 18-ago | Ahrefs/SEJ | 9 AI Search Myths, 15 M data points | 863 mil SERPs, 4 M citações; **38% das URLs citadas em AIO no top-10 (era 76%)**; **CTR da posição 1 −58% com AIO**; wording muda 70%, marcas 46%, fontes 45,5% entre execuções | secundário ✓ (SEJ) |
| 18-ago | Conductor | 10 Best AEO Tools 2026 | critérios: engine coverage, citation tracking, content optimization, enterprise readiness | primária |
| 19-ago | Profound | **Index Report Summer 2026** | 1,9 bi+ conversas, 50+ indústrias; em **24 de 30** indústrias multirregionais, líder europeu fora do top-5 dos EUA | primária ✓ |
| 21-ago | Profound | AEO Guide (6 capítulos, 16 líderes); glossário 300+ termos; comunidade "Marketing Engineers" | prefere o termo AEO | secundário (X) |
| 08–22-ago | Ahrefs | Brand Radar 2.0 | Overview, AI Responses, Cited Domains, Cited Pages, Topics; índice de AI Mode (EUA, UK, Índia); export Sheets/CSV; suporte a Claude (28-jul); 14 M → 30 M prompts | primária (changelog) |
| 23-ago | Similarweb | AI Search News August | Reddit 12% → 3% no ChatGPT Search; RAG em tempo real, feeds, entidade, bot control | primária ✓ |
| 20-ago | Google Ads | AI Max testing & planning | testes A/B de orçamento/ROI em setembro | primária ✓ |
| jul–ago | Semrush/Adobe | — | **nenhum lançamento Adobe novo na janela**; fundacional 17-jun: Adobe Brand Visibility = LLM Optimizer + Semrush AI Optimization | primária (newsroom) |

**Preços (secundário, comparativos de terceiros em ago/2026 — conferir na página do vendor antes de citar):** Profound Growth US$ 99/mês e tier US$ 399/mês anual; Semrush AI Visibility Toolkit US$ 99/mês por domínio; Ahrefs Brand Radar a partir de ≈US$ 398/mês; Otterly Lite €29/mês (15 prompts); Peec Starter €85/mês (50 prompts); AthenaHQ free 300 créditos. Ceticismo do período: Tim Soulo (Ahrefs) e Dan Petrovic — llms.txt "mostly pointless", "prompt volume" é ilusão; Lily Ray e Kevin Indig — slop backlash favorece conteúdo autêntico; Aleyda Solis — medir visibilidade de forma confiável é o desafio nº 1 (survey SEOFOMO, 60/111 respostas iniciais) e framework em 3 camadas (presence, readiness, business impact).

---

## 4. Framework de EXECUÇÃO de um trabalho de GEO (síntese das 5 rodadas + corpus)

Tese: GEO é a camada de otimização da presença em motores generativos, dependente de SEO técnico, conteúdo útil, autoridade externa, dados estruturados coerentes, PR digital, medição por URL e atribuição de receita. Sustentam: Google (guia + Mueller), Semrush (gaps, ROI, PR), Ahrefs (volume, mitos), Conductor (por página), Similarweb (ads, referral), Profound (liderança é local), Bing (relatório próprio), Cloudflare (bot rules).

| Etapa | Duração | Objetivo | Entregáveis | KPIs da etapa |
|---|---:|---|---|---|
| 1. Kickoff e baseline | Sem. 1 | Produto × ICP × jornada, concorrentes SEO/GEO, vocabulário de marca, riscos regulatórios | matriz, lista, glossário | baseline de leads/receita orgânica/brand search |
| 2. Instrumentação | Sem. 1–2 | Separar orgânico clássico, AI visibility, AI referral, AI paid, conversões | GA4 canal "AI Assistants" + grupo custom (Julho-22B §4.1); GSC AI report (impressões); Bing WMT AI Performance; ferramenta de prompts | AI sessions; AI-assisted conversions; branded lift; URLs citadas |
| 3. Universo de prompts e mapa de tópicos | Sem. 2–3 | Trocar keyword-only por clusters de prompts por intenção | biblioteca (informacional, comparativo, alternativa, best, local, preço, problema, compra) por ICP e por mercado/idioma | nº de prompts por etapa; cobertura por ICP; AI adjusted volume como proxy |
| 4. Auditoria de visibilidade generativa | Sem. 3–4 | Onde aparece, não aparece, aparece errado | SOV por engine, mention rate, citation rate, sentimento/narrativa, gaps vs concorrente, **N execuções por prompt** (Julho-22 §2: N≥5 monitoramento, N≥30 pré/pós) | AI SoV; citation frequency; resposta correta × incorreta |
| 5. Auditoria de fontes citáveis | Sem. 4–5 | Quais domínios alimentam as respostas do tema | mapa owned/earned/comunidade/reviews/mídia/YouTube/marketplaces; lista de "domínios candidatos" do `site:` | nº de fontes influenciadoras; source gap |
| 6. Auditoria técnica para IA | Sem. 4–6 | Crawl, render, estrutura, schema, feeds, bot rules | robots.txt + matriz de crawlers (Julho-22B §2.1), Cloudflare/WAF antes de 15-set, sitemaps, IndexNow, schema, feeds Merchant Center, logs, canonical | % indexável; schema coverage; bloqueios por CDN; freshness |
| 7. Conteúdo e entidades | Sem. 5–8 | Recuperabilidade, clareza de entidade, resposta direta | briefs por cluster; pilar; FAQ útil; tabelas comparativas; about/entity page; autoria; **evidência diversa** (§6.1) | cited pages; information gain; AI citation lift; conversão |
| 8. PR digital e autoridade externa | Sem. 6–12 | Fazer a web corroborar os claims | fontes-alvo, pitches, listicles best-of, reviews, dados proprietários, estudos setoriais | menções qualificadas; inclusão em comparativos; citation lift em prompts não-branded |
| 9. Correção de representação | contínua | Corrigir descrições erradas e atributos ausentes | dossiê "como a IA descreve a marca"; correções em site, perfis, terceiros | % respostas corretas; queda de menções negativas falsas |
| 10. Operação mensal de experimentos | mensal | hipótese → implementação → medição → aprendizado | backlog, changelog por URL, cohort de páginas, **controle on-domain** (`2606.04362`), report executivo | tempo até indexação/citação; AI referrals; ROI direto/modelado |

**Cadência:** semanal (war room GEO/SEO: SEO, conteúdo, dev, PR, BI) · quinzenal (revisão de prompts e engines; ajuste de conteúdo) · mensal (comitê executivo: report, pipeline, investimento) · trimestral (rebase de ICP, prompts, concorrentes, stack, budget).

**Papéis mínimos:** estrategista GEO (dono do universo de prompts), SEO técnico (crawl/schema/bot rules), redator + SME (evidência), PR digital (fontes), analista/BI (N execuções, controle, report).

---

## 5. Medição, KPIs e report

### 5.1. Hierarquia de KPIs (com status de fonte)

| Camada | KPI | Definição operacional | Fonte primária localizada? |
|---|---|---|---|
| Visibilidade | **Citation rate** | respostas com link para o domínio ÷ prompts × N execuções | Peec (15-ago), Microsoft Clarity (Wave Junho §2.2) |
| Visibilidade | **Mention rate** | respostas que nomeiam a marca ÷ prompts | Semrush (22-jul), Peec |
| Visibilidade | **AI Share of Voice / Share of Answer** | citações ou menções da marca ÷ total do set | Semrush; Profound (fórmula proprietária) |
| Visibilidade | Position in answer | posição ordinal da citação na resposta | Dageno/Peec [secundário] |
| Visibilidade | Sentimento/narrativa | LLM-as-a-judge sobre o contexto da menção | Semrush (proprietária) |
| Infra | Impressões em AIO/AI Mode | GSC "Search Generative AI Performance" (só impressões) | Google (primária, secundárias descrevem) |
| Infra | Citações em IA no Bing | Bing WMT AI Performance | Microsoft (help doc) |
| Infra | Crawl-to-referral; bloqueios | logs + radar.cloudflare.com/ai-insights | Julho-22B §5 |
| Negócio | **AI referrals identificáveis** | sessões com referrer/UTM de assistentes (piso: ≈70% chegam sem referrer — Julho-22B §4) | Similarweb; Conductor |
| Negócio | Branded search lift | busca de marca pós-exposição | Semrush (assistido) |
| Negócio | ROI direto/assistido/**autodeclarado**/modelado | GA4 + formulário "como nos conheceu" + CRM; 30/60/90 dias | Semrush 27-jul ✓ |
| Negócio | Paid AI visibility | share de anúncios em ChatGPT/AIO/AI Mode | Similarweb AI Ads 13-ago ✓ |

**Regra dos 9 KPIs** (Wave Junho) segue: ≤11 no board. A Camada 2 (infra) continua a menos explorada cientificamente — é onde este corpus tem vantagem.

### 5.2. O que foi desmentido ou perdeu força no período

| Narrativa | Evidência | Regra editorial |
|---|---|---|
| "Volume de prompt é dado" | Ahrefs 17-ago: não existe fonte confiável; AI adjusted volume é proxy | rotular como estimativa direcional; nunca "X buscas por mês no ChatGPT" |
| "Análise de citação diz onde investir" | Rand Fishkin 12-ago: o modelo já sabe que marcas vai recomendar; citação é consequência, não causa | citação como sintoma; investir em ser conhecido (earned) |
| "Google pune conteúdo de IA" | Ahrefs 27-jul: 5,3% do top é 100% IA | vender qualidade verificável, não "humano" como diferencial |
| "Basta um prompt principal" | Semrush 27-jul e 20-jul: jogo de tópico | portfólio de prompts por cluster |
| "SEO morreu / GEO é camada separada" | Google guia + Mueller 24-ago; Conductor e Semrush unificam | GEO = SEO + medição nova (Wave 19 §1 confirmada) |
| "Reddit é fonte estável do ChatGPT" | Similarweb 23-ago: 12% → 3% | diversificar fontes |
| "IA não gera clique" | Similarweb 20-ago (referral ≈3×) [URL 404]; Ahrefs: CTR −58% com AIO | medir AI referral E zero-click; os dois coexistem |
| "Core update de agosto" | só spam update 18–20-ago | não atribuir queda a core inexistente |
| "Taxa de alucinação do modelo X é Y%" | `2606.00898`: mede a cobertura do grafo | declarar cobertura do índice verificador |
| "llms.txt ajuda no Google" | guia oficial: "Google Search ignores them"; 97% dos arquivos com zero requests em mai/2026 [secundário, Ahrefs] | ver §8.b |

### 5.3. Separação obrigatória em todo report a partir desta wave

`orgânico clássico` | `citação orgânica em IA` | `AI referral (piso)` | `AI paid (ChatGPT Ads BR, AI Mode Ads, AIO)` | `conversão assistida/autodeclarada`. Misturar as cinco é o erro que o comitê vai apontar primeiro.

### 5.4. Template de report mensal ("GEO URL Ledger")

1. Sumário executivo (5 bullets: ganhos, perdas, riscos, decisões, próximos testes). 2. Visibilidade por engine (ChatGPT, Perplexity, Gemini, AIO, AI Mode, Copilot) com N execuções e faixa. 3. Performance por etapa da jornada (prompt win rate, topic ownership). 4. **Páginas vencedoras/perdedoras por URL** (citações, tráfego, conversão, mudanças datadas). 5. Concorrentes (SoV, source gaps, citation displacement). 6. Fontes externas (menções, listicles, reviews). 7. Técnico (crawl, schema, feeds, bot rules, goto URLs/quebras de série). 8. Conteúdo publicado e hipótese de cada peça. 9. ROI nas quatro trilhas. 10. Plano de 30 dias (ICE/RICE, owner, prazo).

**Como apresentar incerteza (bastidor, nunca no corpo publicado — DIRETRIZ §12):** faixa e amostra de prompts; mediana e dispersão; "observado" ≠ "inferido"; controle on-domain declarado; cobertura do índice quando o KPI é "citação verificada".

---

## 6. Camada semântico-vetorial — o que a evidência de agosto acrescenta

### 6.1. Diversidade > redundância (primária)
`2608.13956`: com o modelo impedido de saber a resposta, duplicar ou parafrasear o mesmo documento não melhora a resposta; documentos de gêneros diferentes que carregam a informação em formas diferentes melhoram significativamente. Aplicação: para um mesmo fato-chave, publicar **formas distintas de evidência** (parágrafo definitório, tabela com número e data, caso/exemplo, figura com legenda, FAQ) em vez de clonar o parágrafo em várias páginas. Junta-se ao funil da Wave Julho §5 (`similarity → hit rate@k → rerank survival → citation share`) como regra de composição do conjunto recuperado.

### 6.2. Rerank, custo e falhas de pipeline
- Reranker treinado com rubricas de busca (`2608.03527`) e jina-reranker-v3.5 (03-ago; 0,6B parâmetros; 63,20 nDCG@10 no BEIR, acima do Qwen3-Reranker-4B com ~7× menos parâmetros [post do fundador no X; secundário]); Voyage `voyage-code-4` (13-ago, blog oficial ✓) e `rerank-2.5` [secundário]. Leitura: a etapa de rerank fica mais barata e mais exigente com relevância semântica — o brief editorial (pergunta, entidade, evidência) vira o critério de pontuação.
- RAG-Stack (`2608.03487`) e "pre-evidence procedural failures" (`2608.02011`): custo, latência e ordem de operações decidem antes do texto. Confirma Julho-22B: crawl/render/bot rules primeiro.
- Chunking: **nenhuma primária na janela** sobre tamanho ideal; guias de mercado convergem em 60–225 palavras por bloco autocontido [secundário]. O Google diz que não há requisito de chunking. Regra da casa mantida (Wave Julho §5): chunks autocontidos de 2–4 frases, heading-pergunta, entidade nomeada — como técnica de clareza para o leitor e para o recuperador, **não** como promessa de citação.

### 6.3. GEO-Flag: o outro lado do espelho
Detector com F1 0,944 e prevalência estimada de 8,90% (16,36% em páginas de 2026) significa que motores e auditores passam a ter instrumento para descontar conteúdo sobre-otimizado ("citações plantadas, estatística decorativa, autoridade fabricada"), e o próprio paper entrega um agente que audita tier da fonte e verificabilidade das URLs citadas. Para este corpus: (a) **anti-padrão 1 (pseudo-GEO) e 5 (pseudo-autoridade) dos 50 Conceitos viram risco mensurável de rebaixamento**, não só de reputação; (b) toda URL citada em página nossa precisa resolver (regra 0.2 do landing-page-geo, agora com motivo externo); (c) "AI polishing" sem intervenção GEO é explicitamente separado por IPT — polir prosa não é o problema; plantar evidência é.

---

## 7. Brasil (22-jul → 27-ago)

| Fato | Data | Fonte | Rótulo |
|---|---|---|---|
| ChatGPT Ads lançado no Brasil | 11-ago | OpenAI ✓ | PRIMÁRIA |
| Gemini Spark disponível no Brasil (Ultra/Pro) | 31-jul | blog Google Brasil ✓ | PRIMÁRIA |
| AI Overviews "em quase metade das buscas" | 04-ago | iMasters (429 na verificação), agências | SECUNDÁRIO; universo não declarado |
| Imagens geradas por IA na busca (Nano Banana) | 18-ago | EducaSEO | SECUNDÁRIO |
| Conversion atualiza guias com AIO/Modo IA | 22–24-ago | blog Conversion | SECUNDÁRIO |
| CADE, PL 2338, ANPD, RD Summit, Web Summit Rio, Folha/Estadão/UOL sobre IA e busca | — | **não localizado** na janela | manter Julho-22C §4 como estado vigente |

Leitura: o fato brasileiro relevante do mês é **mídia paga dentro do ChatGPT** — o pitch "sua marca ao lado de um anúncio do concorrente na resposta" é concreto e datado. Cobertura de imprensa nacional sobre GEO segue rala: janela de autoridade aberta (Julho-22C §5 confirmada).

---

## 8. Correções e conflitos (precedência sobre o corpus anterior)

- **a) Survey `2607.14035` é agora a régua do mercado, não só nossa.** Google (guia, Mueller) e as colunas céticas convergem: não prometer descobribilidade por reescrita. Julho-22 §3 mantido; copy comercial deve usar o vetor de 4 camadas.
- **b) `llms.txt` REBAIXADO.** Fonte primária do Google: ignora. Sinais de uso por outros motores: 97% dos arquivos válidos sem nenhuma requisição em mai/2026 e tráfego restante de ferramentas de SEO [secundário, Ahrefs]; spec v2 (Jeremy Howard, 10-ago) [secundário]. Status a partir desta wave: **opcional, custo zero, nunca entregável cobrado, nunca KPI**; Wave 19 §7 já dizia "não é alavenca causal" — agora vira "sem consumidor comprovado". Manter o arquivo onde existe; não criar módulo de curso ou serviço em torno dele.
- **c) AI Mode: 1 bi MAU (Google) × 0,13% das visitas (painel terceiro).** Não são a mesma medida (usuários mensais do produto × visitas referentes a busca num painel clickstream). Citar cada um com sua fonte; **não** compor. Prioridade operacional: AIO (2,5 bi/mês) > AI Mode.
- **d) "Core update de agosto de 2026" NÃO existe.** Só spam update 18–20-ago. Toda análise de queda em agosto que cite core update está errada na premissa.
- **e) Reddit deixa de ser exemplo de "fonte que o ChatGPT ama"** em copy, aulas e prompts: 12% → 3%.
- **f) "IA converte 4–5×" segue PROIBIDO como constante** (Julho §7.3); os 1,5–4× citados na janela vêm de painéis de vendor sem denominador comum.
- **g) Volume de prompt**: qualquer número "de buscas em IA" em copy, aula ou paper deve dizer "estimativa (AI adjusted volume, Ahrefs)" ou não entrar.
- **h) xAI**: `chat/completions` + `search_parameters` está morto (410). O `geo-orchestrator` precisa migrar o alias `grok` para `/v1/responses` com `x_search`/`web_search` (verificado funcionando em 27-ago).
- **i) Perplexity `sonar-deep-research` em paralelo (4 chamadas) pendura sem erro**; padrão da casa: `sonar-pro` sequencial como plano B automático (a memória de 27-ago já registrava o 429).

---

## 9. Aplicação por repositório

### 9.1. `landing-page-geo` (alexandrecaramaschi.com)
1. **Painel `/roadmap`**: adicionar as 5 trilhas do §5.3 e a coluna "URL" do §5.4; marcar quebra de série em 26-ago (goto URLs) e 31-ago (AI adjusted volume).
2. **Antes de 15-set**: revisar bot rules do Cloudflare do próprio site e dos clientes com ads; oferta "AI Crawl Readiness" com matriz Training/Search/Agent.
3. **Preferred Sources**: CTA na newsletter/portal "adicione alexandrecaramaschi.com como fonte preferida"; medir brand/direct.
4. **Artigos HBR novos (2):** "Por que o ChatGPT escolhe onde buscar antes de buscar" (`site:` 16–17%) e "O que o Google disse que ignora" (guia oficial + Mueller) — ambos com evidência diversa (§6.1) e zero rótulo de confiança no corpo (DIRETRIZ §12).
5. **Regra 0.2 ganha motivo externo**: GEO-Flag audita URLs citadas; toda citação do site precisa resolver.
6. Copy comercial: separar "citação orgânica" de "ChatGPT Ads" — o anúncio já existe no Brasil.

### 9.2. `papers` (pipeline arXiv e coleta)
1. **Ingestão tagueada**: `2608.16824` (GEO-Flag; Conceitos 11/24 + anti-padrões 1/5), `2608.13956` (diversidade; Conceito 25 e funil vetorial), `2608.03527`, `2608.03487`, `2608.02011` (pipeline), `2606.00898` v2 (metrologia de citação).
2. **Metodologia**: toda métrica de "citação verificada/alucinada" declara a **cobertura do índice verificador** (`2606.00898`); coletar `search_queries` do ChatGPT quando disponível para medir share de `site:` por tema em pt-BR — hipótese pré-registrável: "domínios candidatos em pt-BR concentram-se em X% dos temas".
3. **Variável nova de controle**: score GEO-Flag da página (replicar IPT em pt-BR é candidato a preprint; o benchmark é em inglês).
4. **Cohort de mídia** (Julho-22C): adicionar Reddit como caso de queda abrupta de fonte para testar sensibilidade do CSR a mudanças de plataforma.
5. Registrar no METHODOLOGY que `sonar-deep-research` em paralelo pendura e que a xAI mudou de API (reprodutibilidade).

### 9.3. `curso-factory` (EAD)
1. **Aula nova "O motor escolhe antes de buscar"** (`site:`, domínios candidatos, Preferred Sources) e **aula "O que o Google disse que ignora"** (guia oficial; retirar de qualquer módulo a promessa de `llms.txt`).
2. **Módulo de medição**: template §5.4 como exercício; separar as 5 trilhas do §5.3; exercício de "AI adjusted volume" como proxy.
3. **Aula "Conteúdo sobre-otimizado é detectável"** com GEO-Flag: os 5 anti-padrões dos 50 Conceitos como itens de auditoria.
4. **Reviewer** ganha 4 vetos: "core update de agosto", "volume de prompt" sem rótulo, "Reddit como fonte estável", "llms.txt como entregável".
5. `writer.py`: bloco "evidência diversa" — cada fato-chave em pelo menos duas formas (prosa + tabela/figura), nunca clonado entre aulas.

### 9.4. `Escrita-Empresarial` (gate e fichas)
1. **Fichas de fato** em `pesquisa/geo-wave-agosto-2026.md` (formato do modo pesquisar: fato/fonte/verificacao/limite/atribuicao/validade) para os 12 fatos primários desta wave — são os únicos números de GEO de agosto autorizados a entrar em texto.
2. **Léxico vetado** (candidatos ao gate, não regra ainda): "core update de agosto de 2026", "volume de buscas no ChatGPT" sem "estimativa", "converte 4 vezes mais" sem fonte e vertical.
3. **Regra de diversidade de evidência** como orientação de escrita (não cota): o mesmo número não aparece em duas frases com a mesma forma no mesmo texto.

---

## 10. Claims machine-readable

```yaml
wave: agosto-2026
data: 2026-08-27
precedencia: [agosto, julho-22c, julho-22b, julho-22, julho, wave19, 15b]
claims:
  - id: chatgpt-site-operator
    valor: "16-17% das fan-out queries com site: desde 08-ago-2026 (antes 0,3-0,5%)"
    fonte: {tipo: secundaria-vendor-medicao, nome: Promptwatch via Simon Willison, data: 2026-08-20, url: https://simonwillison.net/2026/Aug/20/chatgpt-search-now-uses-the-siteoperator-at-scale/}
  - id: google-ignora-llms-txt
    valor: "Google Search ignores them (LLMS.txt, markup especial); sem requisito de chunking"
    fonte: {tipo: primaria, nome: Google Search Central, url: https://developers.google.com/search/docs/fundamentals/ai-optimization-guide}
  - id: google-preferred-sources
    valor: "badge em Top Stories, AI Overviews e AI Mode onde disponivel"
    fonte: {tipo: primaria, nome: Google Search Central, data: 2026-08-20, url: https://developers.google.com/search/docs/appearance/preferred-sources}
  - id: chatgpt-ads-brasil
    valor: "ChatGPT Ads lancado em UK, Mexico, Brasil, Japao e Coreia do Sul"
    fonte: {tipo: primaria, nome: OpenAI, data: 2026-08-11, url: https://openai.com/index/testing-ads-in-chatgpt/}
  - id: ahrefs-ai-adjusted-volume
    valor: "sem fonte confiavel de volume real de prompt; proxy unico apos 31-ago-2026"
    fonte: {tipo: primaria, nome: Ahrefs, data: 2026-08-17, url: https://ahrefs.com/blog/how-ahrefs-estimates-ai-search-demand/}
  - id: cloudflare-defaults-15-set
    valor: "dominios novos: Training e Agent bloqueados em paginas com anuncios; Search liberado"
    fonte: {tipo: primaria, nome: Cloudflare Docs, data: 2026-09-15, url: https://developers.cloudflare.com/bots/additional-configurations/block-ai-bots/}
  - id: similarweb-reddit-chatgpt
    valor: "citacoes ao Reddit no ChatGPT Search: ~12% (jul) -> 3% (meados de ago)"
    fonte: {tipo: primaria-vendor, nome: Similarweb, data: 2026-08-23, url: https://www.similarweb.com/blog/insights/ai-news/ai-search-news-update/}
  - id: profound-index-summer-2026
    valor: "1,9 bi+ conversas; em 24 de 30 industrias multirregionais o lider europeu nao esta no top-5 dos EUA"
    fonte: {tipo: primaria-vendor, nome: Profound, data: 2026-08-19, url: https://www.tryprofound.com/reports-guides/profound-index-report-summer-2026}
  - id: ahrefs-aio-overlap-ctr
    valor: "38% das URLs citadas em AIO no top-10 (era 76%); CTR posicao 1 -58% com AIO"
    fonte: {tipo: secundaria, nome: Search Engine Journal sobre Ahrefs, data: 2026-08-18, url: https://www.searchenginejournal.com/ai-search-myths-debunked-ahrefs-spa/584393/}
  - id: geo-flag-prevalencia
    valor: "8,90% das paginas recuperadas sao GEO-otimizadas; 16,36% entre modificadas em 2026; detector F1 0,944"
    fonte: {tipo: primaria, nome: arXiv 2608.16824, data: 2026-08-17, url: https://arxiv.org/abs/2608.16824}
  - id: rag-diversidade
    valor: "duplicatas e parafrases nao melhoram a resposta; documentos diversos melhoram significativamente"
    fonte: {tipo: primaria, nome: arXiv 2608.13956, data: 2026-08-14, url: https://arxiv.org/abs/2608.13956}
  - id: claude-watermark
    valor: "modelos lancados na UE em ou apos 02-ago-2026 suportam marca d'agua de texto legivel por maquina"
    fonte: {tipo: primaria, nome: Anthropic, data: 2026-08-14, url: https://www.anthropic.com/news/claude-text-watermark}
vetos:
  - "core update de agosto de 2026 (nao existe; so spam update 18-20-ago)"
  - "volume de prompt sem rotulo de estimativa"
  - "llms.txt como entregavel, KPI ou fator"
  - "Reddit como fonte estavel do ChatGPT"
  - "IA converte 4-5x como constante"
  - "taxa de alucinacao sem declarar cobertura do indice verificador"
```

---

## 11. Fontes verificadas nesta sessão (27-ago-2026)

Abertas com string-sentinela (✓) ou só status HTTP: Google ai-optimization-guide ✓ · Google preferred-sources ✓ · SEJ Mueller 24-ago ✓ · SERoundtable goto URLs ✓ · OpenAI testing-ads (EN) ✓ (pt-BR 403 anti-bot) · OpenAI GPT-5.6 Sol/Luna ✓ · Anthropic watermark ✓ · Cloudflare block-ai-bots ✓ · Ahrefs AI adjusted volume ✓ · Ahrefs AI content ✓ · Ahrefs trends ✓ · Semrush ROI ✓ · Semrush Digital PR ✓ · Conductor Pages ✓ · Similarweb AI Ads ✓ · Similarweb news 23-ago ✓ · Profound Index Summer ✓ · Profound webinars ✓ · SEJ Ahrefs myths ✓ · SEJ Victorious ✓ · ppc.land survey ✓ · Simon Willison 20-ago ✓ · Suganthan ✓ · Google blog Gemini Spark BR ✓ · Google blog Auto Browse Android ✓ · Voyage code-4 ✓ · Microsoft Advertising playbook (200; "Brand Agents" não achado no texto) · X @randfish 12-ago (200) · arXiv: 2608.16824, 2608.13956, 2608.03527, 2608.03487, 2608.02011 (página abs ✓), 2607.14035, 2606.00898, 2606.20065, 2606.04362, 2605.06635 (API ✓). **Falhas:** Similarweb "referral triples" 404; Reuters Amazon×Perplexity 401; Search Status Dashboard 404; iMasters 429; SEL 403.
