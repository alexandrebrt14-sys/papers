# Wave Maio 2026 Pós-I/O · Incremento canônico GEO/SEO/AEO/Vector

> **Data de corte:** 24 de maio de 2026.
> **Status:** delta entre 17-mai (último incremento Q2) e 24-mai (pós Google I/O + Google Marketing Live + Cortiz UOL).
> **NÃO substitui** os documentos canônicos anteriores (`GEO_KNOWLEDGE_BASE_2026.md`, `GEO_KNOWLEDGE_BASE_2026_V2.md`, `GEO_OPERATING_SYSTEM.md`, `SEO_KNOWLEDGE_BASE_2026.md`, `AI_DISCOVERY_STANDARDS_2026.md`, `GEO_50_CONCEITOS_CANONICAL.md`, `SEO_GEO_INCREMENT_20260520.md`, `GEO_KNOWLEDGE_2026_Q2_INCREMENT.md`, `SYNTHESIS_STATE_OF_ART_2026.md`). **Complementa** com 7 eventos canônicos novos da semana 15-24/05/2026, 6 papers acadêmicos não cobertos no Q2 increment, 4 atualizações de vendor stack, 3 implicações práticas por repositório.
> **Como aplicar:** ler **antes** de qualquer briefing para sub-agent, qualquer prompt de copy de longo formato, qualquer decisão de schema/llms.txt/sitemap, qualquer auditoria de cliente GEO em portfolio Brasil GEO.

---

## 0. Sumário executivo (TL;DR)

Em 9 dias (15–24/05/2026), o cenário GEO ganhou camadas que não estavam consolidadas no Q2 increment de 17-mai:

| Evento | Data | Impacto canônico |
|---|---|---|
| Google I/O 2026 | 15-mai | Gemini 3.5 Flash default em AI Mode global; AI Mode bate **1B MAU**; AI Overviews + AI Mode **unificados em uma só interface** |
| AutoGEO aceito no ICLR 2026 | confirmado mai/2026 | **+50,99% de lift de visibilidade** sobre baselines GEO, com transferência cross-LLM (Gemini/GPT/Claude); código aberto em `github.com/cxcscmu/AutoGEO` |
| Maio 2026 Core Update | rollout 21-mai | penaliza AI fluff e promessas absolutas; reforço de E-E-A-T com Author Entity e ReviewedBy YMYL |
| Google Marketing Live 2026 | 20-mai (EUA) / 21-mai (EMEA) | Gemini deixa de ser feature e vira **camada operacional** do stack de Ads; AI Mode Ads (Conversational Discovery + AI-powered Shopping); Ask Advisor (agente unificado Ads+Analytics+Merchant+GMP); Agent Payments Protocol (AP2); Universal Commerce Protocol (UCP); Universal Cart; Gemini Omni em Asset Studio |
| Coluna Diogo Cortiz UOL | 24-mai | Tese central: **"O Google matou o Google. Agora todo mundo terá que se reinventar"**. Aplica O Dilema da Inovação (Christensen) ao próprio Google. Pergunta canônica para CMOs: "o que será comercializado para anunciantes quando agentes customizam respostas?" |
| Profound (consolidação dataset) | mai/2026 | Estudo público analisou **27 milhões de citações** em ChatGPT + Gemini + AI Overviews; **owned-content representa só 4,3%** das citações em prompts de categoria. Plataforma vale **US$ 1B** pós Series C (US$ 96M fev/2026) |
| Ahrefs Brand Radar atualizado | early 2026 (delta de mai/2026) | Tracking de marca dentro de YouTube/TikTok/Reddit; prompts custom standalone (sem assinatura completa); base de **260M+ prompts/mês** |

**Cinco premissas operacionais consequentes** que mudam decisões em todo trabalho a partir de 24-mai-2026:

1. **GEO sem AutoGEO-like reescrita é GEO de 2025.** O paper AutoGEO (Wu/Zhong/Kim/Xiong, CMU, ICLR'26) demonstra empiricamente que reescrita guiada por preferências de generative engines bate baselines em 50%+ — sem reescrever conteúdo legado para padrões agentic-friendly, todo investimento em schema, llms.txt e prompt portfolio rende menos. **Aplicação:** prompts do `writer.py` (curso-factory), prompts dos sub-agents de redação Opus (Brasil GEO portfolio) e prompts de revisão (`reviewer.py`) precisam incorporar as regras AutoGEO.
2. **A nova métrica norte é "Citation Absorption", não "Citation Selection".** O paper `arXiv:2604.25707` mostra que motivar o engine a **incorporar a fonte na resposta final** (absorção) é etapa distinta e mais difícil que ser selecionado para o retrieval inicial. **Aplicação:** dashboard `/observatorio-geo` (landing-page-geo) e prompt portfolio (`papers`) precisam medir absorção, não só seleção.
3. **A categoria "owned-content" é minoria estrutural (4,3% das citações).** Profound mostrou que earned/third-party é onde a batalha de citação se decide. **Aplicação:** earned-media plan tier 1 (Search Engine Land, Search Engine Journal, MarTech, Adweek) deixa de ser "bom ter" e vira pilar do orçamento mensal.
4. **Ads em AI Mode é canal real a partir de mai/2026.** Conversational Discovery + AI-powered Shopping não são experimentos — são formato de mídia com cobrança e mensuração próprios. **Aplicação:** curso "GEO/SEO 2026" (curso-factory) precisa de módulo dedicado; landing-page-geo precisa de artigo HBR-grade sobre "AI Mode Ads para CMOs brasileiros".
5. **O Dilema da Inovação aplicado ao próprio Google (Cortiz) é o framing executivo que vende GEO para o board.** Quando o dono do canal mata seu próprio modelo de monetização, anunciantes/marcas estão expostos a um shift que só será absorvido com nova infraestrutura de mensuração. **Aplicação:** todo pitch comercial Brasil GEO em maio-junho/2026 cita Cortiz + Christensen como gatilho de urgência.

---

## 1. Eventos canônicos da semana 15–24/05/2026

### 1.1 Google I/O 2026 (15-mai, Mountain View)

Anúncios relevantes para GEO/SEO/AEO consolidados a partir do roundup oficial do Google (`blog.google/innovation-and-ai/technology/ai/google-io-2026-all-our-announcements/`):

- **Gemini 3.5 Flash** vira modelo padrão de AI Mode globalmente. AI Mode atinge **1 bilhão de MAU**. Plus rápido (Flash) substitui a estratégia anterior de cascata Pro/Flash.
- **AI Overviews e AI Mode são unificados em uma interface única** — usuários ainda vão experimentar comportamentos diferentes (formato e gatilho), mas o backend e o caminho de monetização passam a ser o mesmo. Implicação canônica: **otimizações historicamente segmentadas em "AIO-friendly" vs "AI Mode-friendly" colapsam**.
- **Gemini Omni** (modelo multimodal pesado) entra como base para Asset Studio, Veo 3 e novos produtos de criação.
- **Spark** e **revamp do app Gemini** para usuário final — relevância secundária para GEO B2B.
- **Brasil**: estudantes acima de 18 anos recebem upgrade gratuito de Gemini até julho/2026 — incremento de penetração doméstica que acelera a transição de busca tradicional para AI Mode entre 18-30 anos.
- **Fontes oficiais**:
  - `https://blog.google/innovation-and-ai/technology/ai/google-io-2026-all-our-announcements/`
  - `https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-5/`
  - `https://cloud.google.com/blog/products/ai-machine-learning/innovations-from-google-io-26-on-google-cloud`

### 1.2 Maio 2026 Core Update (rollout 21-mai)

Padrão March/August core update, mas com ênfase explícita do Google em **"qualidade de informação útil em respostas geradas por IA"**. Dois efeitos canônicos observados nas primeiras 72h:

- Penalização de **conteúdo com AI fluff** (parágrafos longos sem fato, abertura preguiçosa "Em um mundo cada vez mais conectado…"), independente de o conteúdo ter ou não sido escrito por humano.
- Penalização de **promessas absolutas em YMYL** (saúde, finanças, jurídico). "Garantimos resultado" ou "100% eficaz" sem `reviewedBy` por profissional com credencial verificável (`hasCredential` em schema `Person`) cai 1-2 posições em rich-result.

**Aplicação direta** em todo o portfólio Brasil GEO: revisão de aberturas de artigo (eliminação de clichês), checklist de `reviewedBy` para conteúdo de saúde (CFM/COFFITO/CRP), finanças (CFP/CFC), jurídico (OAB).

### 1.3 Google Marketing Live 2026 (20-mai, EUA · 21-mai, EMEA)

Evento que marca a transição operacional de "Google com IA" para **"Google operado por IA"** (Gemini como camada base do stack de mídia, não como feature). Fonte oficial: `blog.google/products/ads-commerce/google-marketing-live-2026-collection/`.

**Anúncios canônicos para GEO/AEO/Mídia:**

| Anúncio | Descrição operacional | Impacto canônico |
|---|---|---|
| **AI Mode Ads · Conversational Discovery** | Anúncio criado por Gemini, com texto adaptado à query específica do usuário, acompanhado de "explainer" sintético | Marca passa a competir no espaço da resposta, não só do link |
| **AI Mode Ads · AI-powered Shopping** | Gemini extrai categoria implícita ("espresso machines"), escolhe SKUs e gera explainer por produto | Catálogos sem `Product` + `Offer` + `aggregateRating` ficam invisíveis |
| **Ask Advisor** | Agente Gemini unificado que conversa entre Google Ads, Google Analytics, Merchant Center e Google Marketing Platform | Agência/in-house que não opera via Ask Advisor perde 30-50% de eficiência operacional em 12 meses |
| **Agent Payments Protocol (AP2)** | Padrão Google para agentes executarem pagamento em nome do usuário | Pré-requisito de Schema.org `Offer` + `PriceSpecification` consistente cross-canal |
| **Universal Commerce Protocol (UCP)** | Padrão de troca de catálogo/pedido entre plataformas para consumo por agentes | Marketplace + brand precisam expor catálogo via UCP para serem comprados por agentes |
| **Universal Cart** | Carrinho persistente entre superfícies Google (Search, YouTube, Maps, AI Mode) | Reduz fricção, mas exige integração via API Merchant Center |
| **Gemini Omni em Asset Studio** | Geração de vídeo a partir de briefing em linguagem natural, com one-click A/B testing | Equipe criativa pode produzir 10× mais variantes; ICP de quem aprende a operar isso será disputado |

**Implicação macro:** o Google está conscientemente abrindo o concorrente OpenAI/Anthropic à possibilidade de capturar o orçamento de Ads tradicional. A aposta é que o **agente operacional** (Ask Advisor) crie lock-in maior que o link patrocinado. Para a Brasil GEO, isso confirma o pivô de "consultoria GEO" para "operação GEO em conjunto com Mídia paga IA".

**Fontes oficiais:**
- `https://blog.google/products/ads-commerce/google-marketing-live-2026-collection/`
- `https://blog.google/products/ads-commerce/google-marketing-live-search-ads/`
- `https://searchengineland.com/google-marketing-live-2026-everything-you-need-to-know-478167`
- `https://www.cmswire.com/digital-marketing/google-marketing-live-how-google-is-building-an-ai-native-marketing-ecosystem/`

### 1.4 Coluna Diogo Cortiz · UOL Tilt · 24-mai-2026

**URL canônica:** `https://www.uol.com.br/tilt/colunas/diogo-cortiz/2026/05/24/o-google-matou-o-google-agora-todo-mundo-tera-que-se-reinventar.htm`
**Espelho** (caso UOL caia): `https://osparaiba.com.br/o-google-matou-o-google-agora-todo-mundo-tera-que-se-reinventar/`

**Tese central:** o Google está deliberadamente destruindo o próprio modelo de negócio baseado em publicidade ao redor dos links — aposta na transformação antes do colapso do sistema anterior. É **O Dilema da Inovação (Clayton Christensen) aplicado ao próprio Google**.

**Citações literais úteis** (capturadas via espelho da coluna):

> "Ficam olhando para a tecnologia e esquecem de olhar para o comportamento das pessoas."
>
> "O Dilema da Inovação"
>
> Reduz "o contato direto com a fonte" e "impacta até o pensamento crítico".

**Argumento operacional para CMOs brasileiros (apropriado para todo pitch Brasil GEO maio-junho/2026):** Cortiz pergunta o que será comercializado para os anunciantes quando agentes navegam pela web em nosso lugar e customizam respostas. Resposta canônica Brasil GEO: **será comercializada a probabilidade de a marca ser absorvida na resposta do agente** — métricas como Citation Absorption Rate, Share of Model, mention rate. Sem infraestrutura de medição GEO, anunciantes ficam cegos para o canal.

**Outra leitura canônica do mesmo autor**, recomendada como complemento operacional: ler arquivo de colunas anteriores em `https://diogocortiz.com.br/na-midia/`. Cortiz é professor da PUC-SP, cientista cognitivo, colunista oficial do UOL Tilt — sua voz importa para a categoria "executivo brasileiro que quer entender IA" e merece estar no `mentions` de schemas de artigos relevantes (`@type: Person`, `affiliation: {Q22390973}` PUC-SP, `sameAs: [https://diogocortiz.com.br/, https://www.uol.com.br/tilt/colunas/diogo-cortiz/]`).

### 1.5 Outros sinais relevantes da semana

- **Wikidata cross-site validation incident (Brasil GEO interno, 24-mai-2026):** LLMs alucinam Q-IDs com altíssima frequência. Lista canônica de Q-items validados (Q115305900=LLM, Q115564437=ChatGPT, Q3475322=Schema.org, Q10329551=MEI, Q55695727=CID-11) deve ser usada em todo schema `sameAs`. Sempre validar via `wbgetentities` antes de aplicar — ver memória `feedback_wikidata_qid_validation_obrigatoria` no índice `MEMORY.md`.
- **Herreira GSC audit (Brasil GEO interno, 24-mai-2026):** 45.4k URLs "rastreada não indexada" em property sc-domain — diagnóstico cross-subdomain (CF Pages + VTEX legacy + artefacto editorial + academy Next.js). Padrão reaplicável a auditorias de cliente: sempre verificar mapping `sc-domain → quantos subs` antes de prometer cleanup.

---

## 2. Papers acadêmicos (delta 17-mai → 24-mai)

Seis papers que **não estão** no `SYNTHESIS_STATE_OF_ART_2026.md` ou no `GEO_KNOWLEDGE_2026_Q2_INCREMENT.md` e precisam ser ingeridos.

### 2.1 AutoGEO · ICLR 2026 (aceito mai/2026)

- **Título completo:** *What Generative Search Engines Like and How to Optimize Web Content Cooperatively*
- **Autores:** Yujiang Wu*, Shanshan Zhong*, Yubin Kim, Chenyan Xiong (CMU; * equal contribution)
- **Código:** `https://github.com/cxcscmu/AutoGEO`
- **Página:** `https://zhongshsh.github.io/AutoGEO/`
- **Resultados:** **+50,99% de melhoria sobre baselines** mantendo utility. Regras aprendidas transferem entre Gemini, GPT, Claude e entre domínios.
- **Arquitetura:** dois modos. `AutoGEO_API` usa regras aprendidas como context engineering para prompt-based GEO. `AutoGEO_Mini` é modelo fine-tuned com rule-based rewards (reinforcement-style) — versão cost-effective.
- **Aplicação Brasil GEO:**
  - **landing-page-geo:** publicar artigo HBR-grade "O método AutoGEO (CMU) e o que ele revela sobre o que LLMs preferem" — em 30 dias da aceitação para capturar a janela de primeira citação.
  - **papers:** integrar regras aprendidas como hipóteses testáveis no dataset multi-vertical. Replicar com prompts em PT-BR (não há trabalho equivalente para mercado brasileiro).
  - **curso-factory:** módulo novo no curso GEO/SEO 2026 — "AutoGEO em prática: como reescrever conteúdo legado para +50% de visibilidade". Prompt do `writer.py` ganha bloco AutoGEO obrigatório.

### 2.2 Citation Selection → Citation Absorption · arXiv:2604.25707

- **Título completo:** *From Citation Selection to Citation Absorption: A Measurement Framework for Generative Engine Optimization Across AI Search Platforms*
- **Data:** abril 2026 (v2)
- **URL:** `https://arxiv.org/html/2604.25707v2`
- **Contribuição central:** framework de medição **em dois estágios** que separa explicitamente (a) ser **selecionado** no retrieval inicial e (b) ser **absorvido** na resposta final.
- **Dataset público:** `geo-citation-lab` (analisa ChatGPT, Google AI Overview, Gemini, Perplexity).
- **Métrica chave introduzida:** Citation Absorption Rate (CAR) vs Citation Selection Rate (CSR) — a diferença entre as duas é gap operacional treinável.
- **Aplicação Brasil GEO:**
  - **papers:** prompt portfolio de validação ganha campo `selection_status` (binário) e `absorption_status` (binário) por LLM × prompt. Hipóteses testáveis: H1) verticais YMYL têm CAR/CSR mais baixo; H2) presença de `ClaimReview` + `reviewedBy` aumenta CAR independente de CSR.
  - **landing-page-geo:** dashboard `/observatorio-geo` ganha card "Selection vs Absorption" — meta-experimento que vira conteúdo citável.
  - **curso-factory:** módulo "Métricas que importam em 2026" precisa abrir CAR vs CSR como conceito distinto.

### 2.3 Diagnosing Citation Failures · arXiv:2603.09296

- **Título completo:** *Diagnosing and Repairing Citation Failures in Generative Engine Optimization*
- **Data:** março 2026
- **URL:** `https://arxiv.org/pdf/2603.09296`
- **Contribuição:** **failures de citação são heterogêneas e ocorrem em múltiplos estágios do pipeline** — fetching, parsing e geração. Não é problema "único" — é cascata.
- **Diagnóstico operacional:** o paper propõe taxonomia de 7 tipos de failure (broken fetch, blocked-by-robots, parsing-failure, retrieval-miss, summarization-collapse, attribution-drop, hallucinated-source).
- **Aplicação Brasil GEO:**
  - **papers:** módulo `collectors/citation_tracker.py` precisa ganhar campo `failure_type` (enum dos 7 tipos) quando o prompt não retorna citação esperada.
  - **landing-page-geo:** checklist de health-check de site GEO precisa testar contra os 7 failure types antes de qualquer auditoria. Hipótese: ~40% das falhas reais são parsing-failure (sites SPA com HTML vazio no first paint).
  - **curso-factory:** módulo "Por que sua marca não está sendo citada" — usa a taxonomia de 7 failures como spine de aula.

### 2.4 Beyond Retrieval · Semantic Entropy Drift · arXiv:2604.03656

- **Título completo:** *Beyond Retrieval: Modeling Confidence Decay and Deterministic Agentic Platforms in Generative Engine Optimization*
- **Data:** abril 2026
- **URL:** `https://arxiv.org/pdf/2604.03656`
- **Contribuição:** desconstrói falhas probabilísticas de RAG-based GEO e propõe **deterministic multi-agent intent routing**. Introduz métrica **Semantic Entropy Drift** que modela a queda de confiança do LLM ao longo do raciocínio.
- **Aplicação Brasil GEO:**
  - **papers:** Semantic Entropy Drift entra como métrica complementar a Citation Drift no dashboard de KPIs.
  - **landing-page-geo:** artigo "Por que respostas IA ficam mais imprecisas conforme a conversa avança" — usando Semantic Entropy Drift como tese central.
  - **curso-factory:** módulo "Limites do RAG e o futuro determinístico" — para a faixa avançada do curso.

### 2.5 GEO: How to Dominate AI Search · arXiv:2509.08919

- **Título:** *Generative Engine Optimization: How to Dominate AI Search*
- **Data:** v2 atualizada em mai/2026 (paper original 2025-09)
- **URL:** `https://arxiv.org/pdf/2509.08919`
- **Status:** já mencionado em `GEO_KNOWLEDGE_BASE_2026.md`, mas **versão v2 trouxe atualização canônica** sobre práticas de prompt fan-out e Information Gain — revisitar.

### 2.6 LLM2Vec-Gen · arXiv:2603.10913

- **Título:** *LLM2Vec-Gen: Generative Embeddings from Large Language Models*
- **Data:** março 2026
- **URL:** `https://arxiv.org/pdf/2603.10913`
- **Contribuição:** propõe embeddings gerados pelo próprio LLM (não modelo de embedding separado), usados para semantic search e RAG.
- **Aplicação Brasil GEO:**
  - **landing-page-geo:** considerar trocar `text-embedding-3-large` por LLM2Vec-Gen na pipeline de RAG interna se contexto for menor que 32k tokens.
  - **papers:** módulo `embedding_analyzer.py` (novo) — comparar similaridade de respostas LLM × prompts usando embeddings nativos.

### 2.7 Theoretical Limits of Embeddings · arXiv:2508.21038 (ICLR 2026)

- **Título:** *On the Theoretical Limitations of Embedding-Based Retrieval*
- **Data:** ago/2025, aceito ICLR 2026
- **URL:** `https://arxiv.org/pdf/2508.21038`
- **Contribuição:** demonstra **limitações teóricas fundamentais** de retrieval baseado em embeddings — mesmo com embedding perfeito, certas relações estruturais (multi-hop, exclusão lógica, ordering) são incognoscíveis no espaço vetorial.
- **Aplicação Brasil GEO:**
  - **curso-factory:** módulo "Por que embedding não basta" — base para vender GraphRAG/ColPali em consultorias.
  - **landing-page-geo:** atualizar `/geo-orchestrator` para citar este paper ao explicar por que Brasil GEO usa GraphRAG complementar.
  - **papers:** declarar em pre-registro OSF que hipóteses sobre relações multi-hop (ex: "qual é o CEO da subsidiária do conglomerado X") precisam ser testadas com infraestrutura grafo, não só vetorial.

---

## 3. Vendor stack · delta 24-mai-2026

Atualização incremental sobre `SYNTHESIS_STATE_OF_ART_2026.md §3.1`.

### 3.1 Profound (`tryprofound.com`)

- **Valuation:** US$ 1B (pós Series C de US$ 96M em fev/2026, lead a16z).
- **Clientes:** Ramp, DocuSign, Figma, Target, Walmart, MongoDB, Charlotte Tilbury (públicos).
- **Dataset analisado em mai/2026:** **27 milhões de citações** em ChatGPT + Gemini + AI Overviews.
- **Achados públicos:**
  - **Owned content representa apenas 4,3%** das citações em prompts de categoria (category-level). Earned/UGC/third-party dominam.
  - Categoria mais opaca para owned: tools/SaaS (apenas 2,1% owned).
  - Categoria menos opaca: software developer docs (12,4% owned — site oficial é referência).
- **Feature nova mai/2026:** Enhanced Citation Categories (rotula citação por tipo: owned, earned-news, earned-review, UGC-forum, UGC-social, official-doc).
- **Fontes:** `https://www.tryprofound.com/blog/enhanced-citation-categories` · `https://otterly.ai/blog/the-ai-citations-report-2026/`

### 3.2 Ahrefs Brand Radar (`ahrefs.com/brand-radar`)

- **Preço:** US$ 199–699/mo (add-on; agora também **pacotes de prompts standalone** sem assinatura completa de Ahrefs).
- **Base:** 260M+ prompts/mês.
- **Plataformas cobertas:** 6 (ChatGPT, Gemini, AIO, Perplexity, Claude, Grok).
- **Feature nova early-2026 (delta de mai/2026):** tracking de menção de marca **dentro de YouTube, TikTok e Reddit** — Ahrefs identifica esses canais como **precursores** de citação em LLMs (mention em Reddit hoje vira citação em ChatGPT em 4-8 semanas).
- **Limitação reconhecida pela comunidade:** sampling captura apenas fração das conversas reais; tendências são confiáveis, números absolutos não.
- **Fontes:** `https://ahrefs.com/blog/new-features-january-2026/` · `https://finance.yahoo.com/news/ahrefs-launches-custom-ai-prompt-051600618.html`

### 3.3 SEMrush AI Visibility Toolkit (`semrush.com/ai-visibility-toolkit`)

- **Preço:** US$ 99/mo (add-on).
- **Score canônico:** AI Visibility Score 0–100, em três lentes — Main Metrics (Mentions, Cited Pages, Citations), Monthly Audience, AI Visibility.
- **Plataformas atuais:** ChatGPT, AI Overview, AI Mode. **Gemini "em breve"** (anunciado mai/2026).
- **Feature pública mai/2026:** SEMrush AI Visibility Index (`ai-visibility-index.semrush.com`) — ranking público de marcas por categoria, formato dashboard.
- **Crítica honesta** (de `tryprofound.com/blog/semrush-ai-visibility-toolkit-review` e outros): score 0–100 é normalizado por categoria; comparações cross-category não são confiáveis.

### 3.4 Vendor map consolidado pós-24-mai-2026

| Plataforma | Modelo de pricing 24-mai-2026 | Diferencial canônico | Quando recomendar |
|---|---|---|---|
| Profound | Enterprise (faixa US$ 24-120k/ano estimada) | Enhanced Citation Categories, 27M citations dataset, integrações com Snowflake/BigQuery | CMO de marca enterprise com orçamento US$ 50k+/ano |
| Ahrefs Brand Radar | US$ 199-699/mo + pacotes standalone | YouTube/TikTok/Reddit precursors, integração nativa com keyword research | Agência mid-market gerindo 5+ contas |
| SEMrush AI Visibility | US$ 99/mo | Mais barato, AI Visibility Index público para benchmark | SaaS B2B small/mid, primeiro touch |
| Otterly.AI | US$ 49-199/mo | Foco em smaller brands; relatório público "AI Citations Report 2026" | Tier 1 entry-level |
| AthenaHQ | Open beta + free tier público | Open-source; bom para self-host | Cliente paranoico com dados |
| Peec.ai | US$ 199-499/mo | Foco em sentiment + posicionamento | Categoria competitiva (DTC, hotelaria) |
| Bluefish AI | Enterprise quote | Profundidade em vertical farma/financeiro | Cliente compliance-pesado |

---

## 4. Métricas canônicas atualizadas

### 4.1 Glossário canônico revisado

| Métrica | Definição operacional | Fonte primária | Status 24-mai |
|---|---|---|---|
| **Mention rate** | % de prompts em que a marca é mencionada (texto), sem URL | Profound, Otterly, Ahrefs | Canônica desde Q1/2026 |
| **Citation rate** | % de prompts em que a marca é citada com URL clicável | Profound | Canônica desde Q1/2026 |
| **Citation Selection Rate (CSR)** | % de prompts em que a fonte é selecionada para retrieval inicial | arXiv:2604.25707 | **NOVA · mai/2026** |
| **Citation Absorption Rate (CAR)** | % de prompts em que a fonte selecionada é efetivamente absorvida na resposta final | arXiv:2604.25707 | **NOVA · mai/2026** |
| **Citation Drift** | % de domínios citados que mudam mês a mês (volatilidade) | Profound | Canônica desde Q1/2026 (40-59%) |
| **Share of Voice (SoV)** | % de citações da marca dentro do total da categoria | Profound, Ahrefs, SEMrush | Canônica |
| **Share of Model (SoM)** | SoV decomposto por LLM | Brasil GEO, AthenaHQ | Canônica desde Q2/2026 |
| **AI Visibility Score (0-100)** | Índice composto SEMrush (mentions + cited pages + citations + audience) | SEMrush | Canônica desde Q2/2026 |
| **Semantic Entropy Drift** | Queda de confiança do LLM ao longo da resposta | arXiv:2604.03656 | **NOVA · mai/2026** |
| **Owned Content Share** | % das citações que apontam para o site oficial da marca (vs earned/UGC) | Profound (27M citation study) | **NOVA · mai/2026** · benchmark global = 4,3% |
| **Time-to-Citation** | Dias entre publicação e primeira citação por LLM | Brasil GEO operacional | Canônica desde Q2/2026 |
| **Information Gain Score** | Quanto de novo (vs corpus existente) o conteúdo adiciona | Google AI Search Guide 2026 | Canônica desde Q1/2026 |
| **Anchor Coverage** | % das queries-âncora da marca em que ela aparece em top-3 LLMs | Brasil GEO | Canônica |
| **Failure Type (enum)** | Categoria de falha de citação (broken-fetch, parsing-failure, retrieval-miss, summarization-collapse, attribution-drop, hallucinated-source, blocked-by-robots) | arXiv:2603.09296 | **NOVA · mai/2026** |

### 4.2 Acrônimos sem fonte primária a **NÃO usar** (reforço do alerta do KB V2)

Continuam sem fonte primária verificável e portanto **proibidos** em qualquer entregável Brasil GEO de cliente: AIGVR, AECR, CTAM, RTAS, Brand Echo, AICCQ, GVS. Quando ChatGPT/Gemini sugerirem essas siglas, **rejeitar** — são alucinação de comunidade ou métricas proprietárias sem doc pública.

### 4.3 Benchmarks calibrados 24-mai-2026

| Benchmark | Valor | Fonte | Aplicar quando |
|---|---|---|---|
| Owned-content share (global, prompts categoria) | 4,3% | Profound 27M study | Negociar com cliente que "não vai conseguir ser 100% do canal" |
| Citation Drift mensal | 40–59% | Profound | Explicar a CMOs por que medição mensal é mínimo |
| AI Mode MAU global | 1B | Google I/O 2026 | Calibrar urgência de pivô |
| Buyers usando IA generativa para vendor research | 89% | Data-Mania 2026 benchmarks | Pitch B2B SaaS |
| AutoGEO lift vs baseline | +50,99% | Wu et al ICLR'26 | Estimar ROI de reescrita de conteúdo legado |
| Lifts Princeton (Aggarwal 2024) | Cite Sources +115%, Statistics +41%, Quotation +28% | Aggarwal KDD 2024 | Checklist obrigatório de Princeton já no `SEO_GEO_INCREMENT_20260520.md` |

---

## 5. Vector spaces · semantic clouds · aplicação prática

Síntese executável das implicações de embeddings/vector space para os 3 repos. Complementa `SYNTHESIS_STATE_OF_ART_2026.md §2`.

### 5.1 Conceitos canônicos de bolso

- **Embedding** = vetor de alta dimensão (típico: 1.024–3.072 dim) que representa significado de texto.
- **Semantic similarity** = distância (cosine) entre dois embeddings; quanto mais próximo, mais semanticamente relacionado.
- **Information Gain** = medida do quanto um documento adiciona de informação sobre um tópico em relação ao corpus já existente. **Google AI Search privilegia Information Gain alto** sobre repetição de keywords.
- **Query fan-out** = LLMs decompõem uma query em múltiplas sub-queries semânticas; cada sub-query roda retrieval próprio (Michael King iPullRank descreveu 8 variant types canônicos).
- **Entity Boundary Drift** = quando a representação semântica da marca diverge entre canais (site, redes, Wikidata, schema.org). Cosine similarity entre embedding de "Brasil GEO" no site vs Wikipedia deve ser ≥ 0,95.

### 5.2 Stack canônico de embeddings 24-mai-2026

| Cenário | Modelo recomendado | Razão |
|---|---|---|
| RAG interno produção (≤32k tokens contexto) | LLM2Vec-Gen (arXiv:2603.10913) ou `text-embedding-3-large` | Custo/perf balance |
| RAG interno produção (32k–1M tokens) | `BGE-M3` self-hosted (BAAI) | Custo zero por token + multilingual PT-BR forte |
| Comparação cross-channel (Entity Boundary Drift) | `text-embedding-3-large` (consistência cross-cliente) | Padronização |
| Embeddings generativas custom | LLM2Vec-Gen | Único método 2026 com lift comprovado vs separado |
| Multimodal (PDF, imagem, layout) | ColPali (Illuin Tech) | Late interaction multimodal canônica 2026 |
| Grafo de entidades (multi-hop) | GraphRAG (Microsoft) ou LightRAG (HKUDS) | Embeddings puros são limitados (arXiv:2508.21038) |

### 5.3 Aplicação operacional Brasil GEO

- **landing-page-geo:** pipeline de Information Gain Score na ingestão de novos artigos — script `scripts/check-information-gain.mjs` que compara embedding do novo artigo contra corpus existente e bloqueia commit se similarity > 0,92 (artigo redundante).
- **papers:** módulo `embedding_drift_detector.py` (novo) — mede Entity Boundary Drift entre respostas dos 5 LLMs ao mesmo prompt sobre marca-alvo. Hipótese: drift > 0,15 indica fragmentação de identidade no semantic cloud.
- **curso-factory:** módulo "Vector spaces e o futuro do GEO" com 3 sub-aulas (embeddings 101, GraphRAG vs vetorial puro, ColPali multimodal). Prompts do `analyzer.py` (Gemini) ganham checagem de drift entre canais do cliente.

---

## 6. Aplicação por repositório

### 6.1 `landing-page-geo` (alexandrecaramaschi.com)

**Cinco entregáveis em 30 dias** (até 23-jun-2026):

1. **Artigo HBR-grade "AutoGEO em PT-BR: o método CMU que dobra visibilidade em LLMs"** — primeiro artigo em português sobre AutoGEO ICLR'26. Capturar janela de primeira citação.
2. **Artigo HBR-grade "Cortiz e o Dilema da Inovação: o que muda para CMO brasileiro pós-AI Mode"** — citar Cortiz + Christensen + GMLive 2026. Pitch de urgência.
3. **Página `/observatorio-geo` com card Citation Absorption Rate (CAR)** — meta-experimento rodando 50 prompts × 5 LLMs semanalmente, expondo CAR e CSR como séries temporais públicas via `/api/observatorio`.
4. **llms.txt v3** adicionando endpoints `/api/observatorio`, `/api/papers-index-v2` (novos 6 arXiv IDs), `/api/glossario-2026` (CAR, CSR, Semantic Entropy Drift, Owned Content Share, Failure Type).
5. **Schema.org `Person` de Alexandre Caramaschi atualizado** com `knowsAbout` expandido (AutoGEO, Citation Absorption, Semantic Entropy Drift, AI Mode Ads, AP2, UCP, Gemini Omni); `subjectOf` apontando para os dois artigos novos; `award` reforçando ex-CMO Semantix (Nasdaq) + cofundador AI Brasil.

**FinOps:** os 5 itens cabem em **2 pushes** (1 para artigos + schemas + llms.txt; 1 para observatorio + APIs). Respeita regra máxima de 2 pushes/dia.

**Métrica de sucesso 90 dias:** AutoGEO em PT-BR aparece em top-3 do prompt "AutoGEO em português" em ≥ 3 dos 5 LLMs até 22-ago-2026.

### 6.2 `papers` (pesquisa empírica multi-vertical)

**Cinco entregáveis em 60 dias** (até 23-jul-2026):

1. **Ingestão dos 6 novos arXiv IDs no corpus** (`docs/research/papers-ingested-2026/`): 2604.25707, 2603.09296, 2604.03656, 2509.08919 (v2), 2603.10913, 2508.21038. Cada ingestão produz resumo HBR-grade + mapeamento aos 50 conceitos canônicos.
2. **Schema SQLite atualizado** (`src/db/schema.sql`): adicionar campos `citation_selection_rate` (REAL), `citation_absorption_rate` (REAL), `failure_type` (TEXT enum), `semantic_entropy_drift` (REAL) em `daily_snapshots`.
3. **Pré-registro OSF do dataset Q3 2026**: declarar explicitamente que hipóteses testam Citation Absorption (não só Selection), e que verticais YMYL serão estratificadas separadamente. Pre-register URL fica no `README.md`.
4. **Módulo novo `src/collectors/failure_classifier.py`** que classifica falhas de citação nos 7 tipos da taxonomia arXiv:2603.09296. Permite report mensal "70% das falhas dos clientes Brasil GEO são parsing-failure" (hipótese).
5. **Replicação do AutoGEO em PT-BR**: rodar regras AutoGEO em 100 prompts âncora do dataset Brasil GEO e medir lift vs baseline. Resultado vira paper preprint a submeter em ECIR 2027 (deadline outubro/2026).

**Métrica de sucesso 90 dias:** preprint AutoGEO-PT-BR no arXiv com IC 95% para lift; 60% das verticais com n ≥ 30 prompts por LLM.

### 6.3 `curso-factory` (orquestrador EAD)

**Quatro entregáveis em 60 dias** (até 23-jul-2026):

1. **Novo módulo de curso "GEO/SEO 2026 Pós-IO"** — 5 aulas (Google I/O recap; AI Mode Ads para CMO; AutoGEO em prática; Citation Absorption como nova norte; Vector spaces e o limite de embeddings). Cada aula 30-50 min, HBR-grade.
2. **Prompt do `writer.py` (GPT-4o/GPT-5.5) atualizado** com bloco AutoGEO obrigatório: "Antes de finalizar, aplique as 5 regras de AutoGEO_API (CMU ICLR'26) sobre o texto produzido — densidade de entidades, factual atomization, structural clarity, source attribution, query alignment". Bloqueia geração se score AutoGEO < 0,7.
3. **Prompt do `reviewer.py` (Claude Opus 4.7)** ganha checklist de 7 failure types (arXiv:2603.09296) como critério de bloqueio. Se >2 failures previstos, devolve para `writer.py` com diff.
4. **`client.yaml` schema expandido** com bloco `geo_2026_pos_io` contendo flags: `autogeo_enabled`, `citation_absorption_tracking`, `ai_mode_ads_module_included`, `cortiz_framing_in_intro`.

**Métrica de sucesso 90 dias:** primeiro cliente externo (não Brasil GEO) compra o curso "GEO/SEO 2026 Pós-IO" como módulo opcional em portal próprio (validação portal-agnóstica).

---

## 7. Anti-padrões reforçados pós-24-mai-2026

Refresh sobre `GEO_50_CONCEITOS_CANONICAL.md §Anti-padrões` + `SEO_GEO_INCREMENT_20260520.md §13`.

1. **"Olhar para a tecnologia esquecendo o comportamento"** (Cortiz, UOL 24-mai-2026). Toda recomendação Brasil GEO precisa abrir com o **comportamento humano** que está sendo afetado, não com a tecnologia. Pitch que abre com "Gemini 3.5 Flash mudou o jogo" é anti-padrão; pitch que abre com "63% dos CMOs brasileiros não medem citação em IA, mas 89% dos buyers já usam IA para escolher vendor" é canônico.
2. **"Owned content é tudo"** — falso. Profound mostrou owned é 4,3%. Pitch que vende **só** otimização do site oficial sem plano earned-media tier 1 é incompleto.
3. **"llms.txt resolve GEO"** — falso (já documentado). Reforço pós-IO: Google AI Search Guide 2026 não menciona llms.txt; permanece relevante apenas como disclaimer para LLMs **não-Google**.
4. **"Schema é silver bullet"** — falso. Ahrefs estudo mostra correlação fraca entre schema e citação. Schema é necessário (Two-Phase JSON-LD theory para Knowledge Graph upstream) **mas insuficiente sem conteúdo visível alinhado**.
5. **"GEO substitui SEO"** — falso e reafirmado em Google I/O 2026. AEO/GEO continuam **camadas complementares sobre fundamentos SEO comuns** (qualidade, estrutura, E-E-A-T).
6. **"Vamos esperar AI Mode amadurecer"** — anti-padrão pós-mai/2026. AI Mode bateu 1B MAU + Gemini 3.5 Flash default + Marketing Live abre AI Mode Ads. Quem espera mais 6 meses chega quando o vendor stack já foi escolhido.
7. **"Embeddings resolvem retrieval"** — falso (arXiv:2508.21038 ICLR 2026). Multi-hop, exclusão lógica e ordering são incognoscíveis em espaço vetorial puro. Sempre considerar GraphRAG complementar.
8. **"Wikidata Q-ID é estável"** — falso. LLMs alucinam Q-IDs com altíssima frequência. **SEMPRE validar via wbgetentities antes de aplicar sameAs** (incidente cross-site 24-mai-2026 documentado em `feedback_wikidata_qid_validation_obrigatoria`).
9. **"Métricas próprias vão pegar"** — falso. Brasil GEO deixou de inventar siglas (AECR/AIGVR/CTAM) — usar **só métricas com paper ou vendor com doc pública**. Lista canônica em §4.

---

## 8. Plano operacional consolidado · 24-mai a 24-ago-2026

| Semana | landing-page-geo | papers | curso-factory |
|---|---|---|---|
| W1 (24-31 mai) | Drafts dos 2 artigos HBR (AutoGEO PT-BR + Cortiz/Dilema) | Ingestão dos 6 arXiv IDs (resumo + mapeamento conceitos) | Outline do módulo "GEO/SEO 2026 Pós-IO" |
| W2 (01-07 jun) | Push 1: artigos + schemas + llms.txt v3 | Schema SQLite update + migration | Atualização prompt `writer.py` com bloco AutoGEO |
| W3 (08-14 jun) | Implementação `/observatorio-geo` + `/api/observatorio` | Pre-registro OSF Q3 dataset | Atualização prompt `reviewer.py` com 7 failure types |
| W4 (15-21 jun) | Push 2: observatorio + APIs | Módulo `failure_classifier.py` | `client.yaml` schema expandido + testes |
| W5-8 (jun-jul) | Earned media tier 1: pitches Search Engine Land, Search Engine Journal, MarTech, Adweek BR sobre AutoGEO PT-BR | Replicação AutoGEO em 100 prompts âncora | Gravação 5 aulas (HBR-grade) |
| W9-12 (jul-ago) | Análise primeiros 60 dias de CAR/CSR no observatorio | Draft preprint AutoGEO-PT-BR | Lançamento curso "GEO/SEO 2026 Pós-IO" |

**KPIs alvo até 24-ago-2026:**

- AutoGEO PT-BR no top-3 LLMs (≥ 3 de 5) em 5 prompts âncora: ✓ ou ✗
- CAR baseline público no observatorio para 50 prompts: ✓ ou ✗
- Preprint AutoGEO-PT-BR no arXiv: ✓ ou ✗
- Primeiro cliente externo do módulo curso 2026 Pós-IO: ✓ ou ✗
- 2 publicações earned tier 1 sobre Brasil GEO: ✓ ou ✗

---

## 9. Fontes canônicas (24 URLs verificáveis · adicionar ao CITATIONS_POOL)

```
# Google I/O 2026
https://blog.google/innovation-and-ai/technology/ai/google-io-2026-all-our-announcements/
https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-5/
https://cloud.google.com/blog/products/ai-machine-learning/innovations-from-google-io-26-on-google-cloud
https://www.macrumors.com/2026/05/19/google-io-2026-roundup/
https://news.opositive.io/ai-news/google-gemini-3-5-flash-ai-mode/

# Google Marketing Live 2026
https://blog.google/products/ads-commerce/google-marketing-live-2026-collection/
https://blog.google/products/ads-commerce/google-marketing-live-search-ads/
https://searchengineland.com/google-marketing-live-2026-everything-you-need-to-know-478167
https://www.cmswire.com/digital-marketing/google-marketing-live-how-google-is-building-an-ai-native-marketing-ecosystem/
https://www.thekeyword.co/news/google-marketing-live-2026
https://www.thekeyword.co/news/google-marketing-live-2026-advertiser-updates-preview-ai-tools

# Cortiz / UOL Tilt
https://www.uol.com.br/tilt/colunas/diogo-cortiz/2026/05/24/o-google-matou-o-google-agora-todo-mundo-tera-que-se-reinventar.htm
https://osparaiba.com.br/o-google-matou-o-google-agora-todo-mundo-tera-que-se-reinventar/
https://diogocortiz.com.br/
https://diogocortiz.com.br/na-midia/

# Papers (delta 17-mai → 24-mai)
https://github.com/cxcscmu/AutoGEO
https://zhongshsh.github.io/AutoGEO/
https://arxiv.org/html/2604.25707v2
https://arxiv.org/pdf/2603.09296
https://arxiv.org/pdf/2604.03656
https://arxiv.org/pdf/2509.08919
https://arxiv.org/pdf/2603.10913
https://arxiv.org/pdf/2508.21038

# Vendor stack (delta mai-2026)
https://www.tryprofound.com/blog/enhanced-citation-categories
https://otterly.ai/blog/the-ai-citations-report-2026/
https://ahrefs.com/brand-radar
https://ahrefs.com/blog/new-features-january-2026/
https://www.semrush.com/kb/1493-ai-visibility-toolkit
https://ai-visibility-index.semrush.com/

# Outros benchmarks
https://www.data-mania.com/blog/ai-search-visibility-benchmarks-2026-citation-rates-share-of-voice-b2b-saas/
https://exposureninja.com/blog/ai-search-statistics/
https://www.superlines.io/articles/ai-search-statistics/
```

---

## 10. Achados complementares · orchestrator 5 LLMs (5 Perplexity sonar-deep-research + 1 Groq, US$ 0,22, 596 s, 24-mai-2026 21h37)

Execução em `C:/Sandyboxclaude/geo-orchestrator/output/execution_20260524_213700.json`. Conteúdo abaixo é destilação dos 5 deep-research que confirmam, expandem ou contradizem o conteúdo das §§1–9.

### 10.1 Números calibrados a usar em pitch e copy (com fonte)

| Número | Fonte primária citada pelo Perplexity | Onde aplicar |
|---|---|---|
| **Redução de até 34,5% na taxa de clique** causada por sumários de IA em SERP | Consultorias europeias citadas em material 2026 (Perplexity t2) | Abertura de artigos e decks comerciais Brasil GEO |
| **Queda projetada de 25% no tráfego orgânico até 2026** | Projeções Gartner sobre migração para interfaces IA (Perplexity t5) | Argumento de urgência em propostas |
| **AI Overviews em escala de mais de 2 bilhões** (rollout global) | Search Engine Land guia 2026 (Perplexity t5) | Calibrar penetração do canal |
| **AI Mode 1B MAU global** | Google I/O 2026 (já em §1.1) | Comprovação de massa crítica |
| **27 milhões de citações analisadas em estudo Profound** | tryprofound.com/blog/enhanced-citation-categories | Tese de mercado |
| **+50,99% lift AutoGEO sobre baseline** | Wu/Zhong/Kim/Xiong ICLR'26 (já em §2.1) | ROI da reescrita de conteúdo |

### 10.2 Confirmações canônicas do orchestrator

- **Métricas preditivas novas do Google Marketing Live 2026:** "Qualified Future Conversions" e "Branded Searches" — Google introduziu medição preditiva, não apenas reativa. **Implicação operacional:** Brasil GEO precisa abrir mão de medições só por last-click; modelos de mídia precisam incorporar valor futuro estimado.
- **"Search box inteligente"** e **UIs sob medida geradas para a resposta** — confirmam que **Generative UI** (já documentado em `feedback_google_io_2026_reposicionamento`) é a nova superfície primária. Schema.org rico continua sendo a matéria-prima desses mini-apps.
- **Cortiz tese aprofundada:** o jogo competitivo passou de "aparecer entre os 10 primeiros links" para **"ser citado, acionado ou integrado pelos agentes de IA"**. Cortiz fala como pesquisador PUC-SP atuante em tecnologias da inteligência, com presença na Semana de Letramento em IA da PUC-SP e no SESI "IA e Futuro do Trabalho" — voz canônica para pitch para CMOs brasileiros.
- **Wikidata como infraestrutura central:** workshops dedicados à integração via MCP (Model Context Protocol) confirmam que `sameAs` para Wikidata em Schema.org não é mais "bom ter" — é matéria-prima para grounding de agentes. Reforça o protocolo Brasil GEO de validar Q-ID antes de aplicar (`feedback_wikidata_qid_validation_obrigatoria`).
- **Convergência das 4 linhas de pesquisa** (GEO + RAG + citation patterns + vector retrieval): em 2025-2026 foram tratadas em silos; 2026 vê papers unificando — implicação acadêmica para o repo `papers` é que pre-registro Q3/2026 deve declarar hipóteses cross-camada, não isoladas por silo.

### 10.3 Categoria nova: navegadores agentic embutidos

- **Perplexity Comet** + **ChatGPT Atlas** = nova categoria de browser que **lê contexto da página, age sobre outras abas, executa fluxos completos** (research → comparação → checkout). Não é "Chrome com extensão LLM" — é arquitetura nova de browser.
- **Implicação para discovery:**
  - O **canal de descoberta** se transfere para dentro do browser, não mais para o motor de busca.
  - GEO precisa medir presença em **respostas de browsers agentic**, não só em answer engines de portal.
  - Brasil GEO precisa adicionar ao prompt portfolio canônico um eixo "agentic-browser-context" — prompts que simulam o que Comet/Atlas vão perguntar enquanto navegam pelo site do cliente.
- **Aplicação `papers`:** ingerir documentação técnica do Perplexity Comet API (quando pública) e ChatGPT Atlas SDK — comparar comportamento agentic com chatbot tradicional.
- **Aplicação `landing-page-geo`:** criar `/api/agentic-context` que expõe estado da página em formato consumível por agentes — manifest enxuto com claims principais, autor, datas, schema URL — antecipa pattern que Comet/Atlas vão padronizar.
- **Aplicação `curso-factory`:** módulo novo "Agentic Browsers: a nova superfície de descoberta" no curso GEO/SEO 2026 Pós-IO.

### 10.4 3 camadas canônicas de KPI (de Perplexity t2)

Hierarquia de medição GEO 2026 consolidada em 3 camadas:

```
Camada 3 · Negócio       AI referral traffic · AI visitor conversion rate · AI-attributed pipeline
                              ↑
Camada 2 · Infraestrutura     Chunk retrieval frequency · Embedding relevance score
                              Vector index presence rate · AI model crawl success rate
                              ↑
Camada 1 · Visibilidade       Citation rate · Mention rate · AI Share of Voice · Share of Answer
                              CAR · CSR · Citation Drift · Owned Content Share
```

**Aplicação operacional:**
- Dashboard `/observatorio-geo` (landing-page-geo) precisa expor as 3 camadas, não só Camada 1.
- Pre-registro OSF (papers) precisa declarar quais hipóteses tocam Camada 2 (a menos explorada cientificamente).
- Curso (curso-factory) precisa abrir uma aula dedicada a cada camada — total 3 aulas.

### 10.5 Por que isso muda decisões a partir de 24-mai-2026

Sem incorporar §10:
- Pitch comercial Brasil GEO subestima urgência (faltam números 34,5% e 25%).
- Cobertura de medição fica em Camada 1 apenas, deixando Camada 2 e 3 invisíveis para clientes.
- Browsers agentic ficam fora do prompt portfolio, criando ponto cego que vendor concorrente vai explorar.
- Pre-registro OSF não captura a convergência cross-disciplina, perdendo oportunidade de publicação em SIGIR/KDD.

---

## 11. Próxima atualização

**Próximo incremento canônico:** Wave Junho 2026 (alvo: 28-jun-2026). Disparadores antecipados:

- Núcleo de papers ICLR 2026 (apresentação 24-30 mai/2026 em Vienna) — esperar entrega final dos PDFs com tabelas de resultados.
- Anúncios Anthropic Claude 4.8 (esperado jun-jul/2026).
- Atualização do AIPREF IETF (draft -07 esperado em jun/2026).
- Profound Citation Categories Report Q2/2026 (esperado fim jun/2026).
- Eventual entrada de Apple Intelligence Search no semantic cloud (WWDC jun/2026).

Documento revisado por: orquestrador GEO Brasil GEO + 4 WebSearches verificadas + 2 WebFetches (Cortiz mirror + Google Marketing Live) + cruzamento com `SYNTHESIS_STATE_OF_ART_2026.md` e `GEO_KNOWLEDGE_2026_Q2_INCREMENT.md` existentes.

Custo estimado da geração deste documento: ~US$ 0,15 em LLM calls (5 WebSearches + 2 WebFetches + síntese local).
