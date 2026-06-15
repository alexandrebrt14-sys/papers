# Wave Junho 15 2026 · Incremento canônico GEO/SEO/AEO/Vector

> **Data de corte:** 15 de junho de 2026.
> **Status:** delta entre 07-jun (`GEO_WAVE_JUNHO_2026_CANONICAL.md` — framework de 5 camadas, CSR/CAR, EcoGEO, GEO-16, vendor stack jun) e 15-jun.
> **NÃO substitui** nenhum documento canônico anterior. **Complementa** com: dois papers acadêmicos de 2026 verificados (GEO-SFE e AgentGEO), a taxonomia de KPIs que separa Share of Voice de Share of Answer, benchmarks rigorosos de impacto de AI Overviews (RCT e Seer Interactive), o delta de vendor stack (Profound 10 motores + Personas, Ahrefs Brand Radar com 199M+ prompts, Semrush AI Visibility Index + MCP), as novidades de busca do Google I/O 2026, a disciplina de Relevance Engineering, e a transição de llms.txt para o padrão IETF AIPREF.
> **Como aplicar:** ler **antes** de qualquer decisão sobre dashboard de medição, definição de KPI de cliente, escolha de ferramenta de AI visibility, briefing de sub-agent, prompt de coleta, design de schema/llms.txt, rubrica de redação ou auditoria GEO em portfolio Brasil GEO.
> **Fonte e transparência metodológica:** esta wave foi ancorada na pesquisa web ao vivo do Claude Code (WebSearch + WebFetch, junho/2026), com verificação direta de fontes primárias (arXiv, blogs oficiais de fornecedores, blog do Google). O `geo-orchestrator` (5 LLMs) foi executado em 4 waves paralelas (15-jun-2026, raw em [`raw/`](raw/)) e contribuiu com o **fundamento técnico atemporal** da camada semântica/vetorial (§5). Importante: nesta execução, as tarefas Perplexity `sonar-deep-research` do orchestrator retornaram **sem resultados de busca live** (search results vazios) e, portanto, **não foram usadas como fonte de fatos datados** — todo dado de evento, data, número e URL abaixo vem de verificação ao vivo independente. Dois arXiv IDs confirmados via WebFetch (`2603.29979`, `2603.09296`).

---

## 0. Sumário executivo (TL;DR)

O delta de 07 a 15 de junho não traz um novo modelo fundador; traz **fechamento de lacunas de medição e de fundamentação técnica**. Três movimentos definem a semana: (a) a literatura passou a quantificar **como a estrutura do documento** (não só sua autoridade) determina citação, com framework reprodutível e lift medido; (b) o vocabulário de KPI amadureceu e separou formalmente **estar na lista de fontes** (Share of Voice) de **ser a resposta** (Share of Answer); e (c) saiu a primeira evidência experimental controlada (RCT) do impacto de AI Overviews sobre cliques, junto com a contraparte de valor: marcas citadas em AIO ganham mais cliques por impressão do que as não citadas.

| Evento / achado | Data | Impacto canônico |
|---|---|---|
| Paper GEO-SFE (Structural Feature Engineering for GEO) — arXiv:2603.29979 | 31-mar-2026 | Decompõe a estrutura do conteúdo em três níveis (macro/meso/micro) e mede +17,3% de citation rate e +18,5% de qualidade subjetiva em 6 motores. Dá rubrica técnica reprodutível à redação para citação. |
| Paper AgentGEO (Diagnosing and Repairing Citation Failures) — arXiv:2603.09296 | 10-mar-2026 | Sistema agêntico que diagnostica por que uma página não é citada e a repara: +40% de citação relativa modificando só 5% do conteúdo (vs 25% de baselines). GEO vira loop de diagnóstico-reparo, não reescrita total. |
| Taxonomia de KPI separando Share of Voice de Share of Answer | 2026 | "SoV sozinho não basta": visibilidade, citação e recomendação são influências distintas. Novos KPIs: Answer Inclusion Rate, Recommendation Rate, Prompt Coverage, Assisted Click Yield. |
| RCT de AI Overviews (primeiro experimento de campo randomizado) | jan-fev/2026 | AIO reduz cliques orgânicos em queries acionadas em ~38%, com avaliação de experiência do usuário inalterada. Evidência dura de zero-clique causado, não correlacionado. |
| Seer Interactive 2026: valor da citação em AIO | 2026 | Marcas **citadas** em AIO ganham ~120% mais cliques orgânicos por impressão que as não citadas nas mesmas queries. CTR em queries com AIO se recuperou de ~1,3% (dez/25) para ~2,4% (fev/26). |
| Profound: 10 motores rastreados + Personas + Profound Agents | 2026 | Cobertura subiu para 10 engines (inclui Meta AI, DeepSeek, Grok); Personas vê a resposta pela ótica do público; Series C de US$ 96M a US$ 1B (Fortune, 24-fev-2026). |
| Ahrefs Brand Radar: 199M+ prompts, Agent A, Custom AI Prompt Tracking | jan-jun/2026 | Base de 199M+ prompts ancorados em busca real; 6 motores; estudo "50 domínios mais citados em AI Overviews" (jun/2026). |
| Semrush: SoV ponderado por volume de prompt + AI Visibility Index + acesso MCP | out/2025-2026 | SoV reflete volume de busca do prompt; AI Visibility Index público enterprise; toolkit com API, MCP e 200 prompts rastreados. |
| Google I/O 2026: AI Mode global, Personal Intelligence, Search Agents | mai-jun/2026 | Gemini 3.5 Flash default no AI Mode; Personal Intelligence em ~200 países / 98 idiomas sem assinatura; follow-up direto do AI Overview para conversa; agentes de informação 24/7 (verão/2026). |
| SparkToro: zero-clique em 68,01% no início de 2026 | 2026 | Apenas 276 cliques por 1.000 buscas chegam à web aberta (era 374 em 2024), queda de 26% em dois anos. Só 0,34% das buscas migraram para AI Mode (jan-abr). |
| OpenAI inicia anúncios no ChatGPT | 09-fev-2026 | Ads em tiers Free/Go; Plus/Pro/Business/Enterprise/Education sem anúncio. Pivô de Instant Checkout para descoberta de produto. Guerra de agentes de compra (ChatGPT, Rufus, Perplexity, Alexa+). |
| Relevance Engineering (Michael King / iPullRank) | 2026 | Disciplina que funde recuperação de informação, IA e estratégia de conteúdo; reposiciona "SEO" como engenharia de relevância para motores generativos. |
| llms.txt ~10% de adoção; IETF AIPREF como padrão emergente | 2026 | llms.txt segue convenção comunitária (não padrão formal); o futuro do controle de crawler de IA é moldado pelo IETF AIPREF (`draft-ietf-aipref-attach`) e pela indústria de CDN. |

### Sete premissas operacionais consequentes (mudam decisões a partir de 15-jun-2026)

1. **Estrutura é alavanca mensurável de citação, com lift quantificado.** GEO-SFE (`2603.29979`) prova que macro-estrutura (arquitetura do documento), meso-estrutura (chunking de informação) e micro-estrutura (ênfase visual) movem citation rate (+17,3%) independentemente de autoridade. **Aplicação:** a rubrica de redação ganha três eixos estruturais explícitos; auditoria on-page passa a pontuar os três níveis.
2. **GEO competitivo é diagnóstico-e-reparo, não reescrita.** AgentGEO (`2603.09296`) atinge +40% de citação mudando 5% do conteúdo. **Aplicação:** o fluxo de trabalho vira "diagnosticar a falha de citação específica → intervir cirurgicamente → remedir", e não "reescrever a página inteira".
3. **Share of Voice e Share of Answer são KPIs distintos.** Estar entre as fontes (SoV) não é ser a resposta recomendada (Share of Answer). **Aplicação:** todo relatório de cliente reporta os dois separadamente; o headline KPI é AI Share of Voice, mas Share of Answer e Recommendation Rate sobem ao board.
4. **A citação tem ROI mensurável mesmo no zero-clique.** Ser citado em AIO vale ~120% mais cliques por impressão (Seer 2026); o RCT mostra -38% de cliques agregados, mas o tráfego citado é mais qualificado. **Aplicação:** o pitch troca "vamos recuperar tráfego" por "vamos capturar a fração qualificada que ainda clica e a lembrança de marca que não clica".
5. **A superfície de descoberta é agêntica e paga.** Google Search Agents 24/7, ChatGPT com anúncios e agentes de compra mudam o jogo de "aparecer numa resposta" para "ser elegível na ação do agente". **Aplicação:** auditorias incluem elegibilidade em fluxos de compra/ação agêntica, não só citação textual.
6. **O controle de acesso de IA migra de llms.txt para AIPREF.** Com ~10% de adoção e status de convenção, llms.txt não é talismã; o padrão real emergente é o IETF AIPREF. **Aplicação:** preparar `/.well-known/ai-preferences` e acompanhar o `draft-ietf-aipref-attach`; manter llms.txt como defensivo, não como requisito.
7. **"Deep research" sem busca live é fabricação.** A própria operação desta wave flagrou um motor de "pesquisa profunda" sem resultados de busca prestes a inventar datas/URLs. **Aplicação:** todo fato datado exige verificação em fonte primária ao vivo; arXiv IDs verificados via WebFetch antes de canonizar (anti-GhostCite reforçado).

---

## 1. Frameworks de execução operacional de GEO (delta)

### 1.1 O loop refinado: OBSERVAR → DIAGNOSTICAR → REPARAR → MEDIR

O loop agêntico canônico (wave 07-jun, §1.1) ganha um vértice com base empírica. AgentGEO (`2603.09296`, Tian, Chen, Tang, Liu, Jia, 10-mar-2026) formaliza a etapa de **diagnóstico de falha de citação** seguida de **reparo cirúrgico**: o sistema identifica por que uma página não foi citada (taxonomia de modos de falha), aplica intervenção dirigida e remede. O resultado canônico é forte: **+40% de citação relativa modificando apenas 5% do conteúdo**, contra 25% de melhoria de baselines que reescrevem mais. A consequência operacional inverte a intuição: o trabalho de maior retorno não é produzir mais conteúdo, é diagnosticar a falha específica de uma página que já existe e corrigi-la com precisão.

### 1.2 GEO-SFE: a estrutura do documento em três níveis

GEO-SFE (`2603.29979`, Yu, Yang, Ding, Sato, 31-mar-2026) é o framework de execução mais acionável da semana porque transforma "escreva conteúdo estruturado" em três eixos mensuráveis e otimizáveis:

| Nível | Nome | O que governa | Alavancas práticas |
|---|---|---|---|
| **Macro** | Arquitetura do documento | Como o documento se organiza como um todo | Hierarquia de seções, ordem lógica, escopo por página, interligação |
| **Meso** | Chunking de informação | Como a informação se agrupa em unidades recuperáveis | Densidade de evidência por bloco, self-containment de seção, answer capsules, tabelas/listas |
| **Micro** | Ênfase visual | Como o texto sinaliza o que importa | Negrito em termos-chave, marcação semântica, destaque de números e definições |

Medição reportada: **+17,3% de citation rate** e **+18,5% de qualidade subjetiva** em 6 motores generativos. Isso dá fundamento reprodutível, com lift numérico, à rubrica de redação empírica que o ecossistema já adotava (Princeton/AutoGEO/GEO-16) — agora com um vocabulário de três níveis que mapeia diretamente para checklist e para auditoria.

### 1.3 Relevance Engineering como disciplina-guarda-chuva

Michael King (iPullRank) consolidou em 2026 o termo **Relevance Engineering (r17g)** — a fusão de recuperação de informação, IA e estratégia de conteúdo — e publicou o "AI Search Manual". A tese: o trabalho deixou de ser "otimizar para um rankeador" e passou a ser "engenheirar a relevância semântica que faz um modelo recuperar e usar o conteúdo". É o enquadramento profissional que une as camadas técnica (§5), de conteúdo (§1.2) e de medição (§2) sob uma única engenharia. Para a Brasil GEO, é o vocabulário que posiciona o serviço acima de "AI visibility tool reseller": entregamos engenharia de relevância, não leitura de dashboard.

---

## 2. KPIs, medição e reports (delta)

### 2.1 Share of Voice vs Share of Answer — a separação canônica

A maturação de 2026 estabelece que **estar entre as fontes** e **ser a resposta** são influências distintas e exigem KPIs separados:

- **AI Share of Voice (SoV)** — proporção de respostas (num conjunto estável de prompts e plataformas) em que a marca aparece, relativa a concorrentes. Fórmula canônica: citações da marca / total de citações de todas as marcas no conjunto de queries. Continua sendo o **headline KPI**.
- **Share of Answer** — proporção em que a marca é a base efetiva da resposta (recomendada, sintetizada no texto), não apenas listada. É o análogo de KPI da distinção Citation Selection Rate vs Citation Absorption Rate (wave maio/junho).
- **Recommendation Rate** — frequência com que a marca é explicitamente recomendada, não só mencionada.

### 2.2 A bateria de KPIs consolidada (2026)

Os programas de medição mais fortes combinam, além de SoV e Share of Answer:

- **Answer Inclusion Rate** — % de prompts em que a marca entra na resposta.
- **Citation Rate** e **Citation Prevalence** — frequência e disseminação de citação do domínio/URL como fonte.
- **Prompt Coverage** — de todo o universo de intenções relevantes, em quantas a marca aparece.
- **Brand Mention Prominence** — posição/proeminência da menção dentro da resposta.
- **Sentiment e Accuracy** — como a marca é descrita e se os fatos estão corretos.
- **AI Referral e Assisted Impact / Assisted Click Yield** — tráfego e pipeline assistidos por IA.

### 2.3 Cadência e estrutura de report

O report mensal canônico de AI visibility em 2026 se organiza em **oito seções**, com **AI Share of Voice como KPI de manchete**, descendo para Share of Answer, cobertura de prompts, sentimento e impacto assistido. Mantém-se a regra dos 9-11 KPIs no nível board (wave 07-jun, §1.3) e a triangulação obrigatória (nenhum número único de uma só ferramenta).

### 2.4 Benchmarks de impacto verificáveis (Seer Interactive / RCT)

- **RCT de AI Overviews** (primeiro experimento de campo randomizado, 2 semanas por participante, jan-fev/2026): AIO reduziu cliques orgânicos em queries acionadas em **~38%**, com avaliação de experiência do usuário **inalterada**. Zero-clique subiu de 54% para 72% nas queries com AIO. (searchenginejournal.com)
- **Seer Interactive 2026** (53 marcas): CTR orgânico em queries com AIO se recuperou de um piso de ~1,3% (dez/2025) para ~2,4% (fev/2026), alta de ~85% em dois meses. E o dado canônico de ROI: **marcas citadas em AIO ganham ~120% mais cliques orgânicos por impressão** que marcas não citadas nas mesmas queries.

Leitura canônica: o zero-clique é real e causal, mas a citação tem valor mensurável — tanto na fração qualificada que ainda clica quanto na lembrança de marca. Isto sustenta o KPI de Share of Answer como métrica de negócio, não de vaidade.

---

## 3. Ecossistema de ferramentas — delta jun/2026

| Ferramenta | Delta / lançamento (2026) | Diferencial | Fonte |
|---|---|---|---|
| **Profound** | Rastreia agora **10 motores** (inclui Meta AI, DeepSeek, Grok, Copilot, AIO); **Personas** (ver a resposta pela ótica de cada público); **Profound Agents** (gera e distribui copy na voz da marca). Series C de **US$ 96M a US$ 1B** | Maior amplitude de motores + camada de agentes de marketing | fortune.com/2026/02/24/exclusive-as-ai-threatens-search-profound-raises-96-million; tryprofound.com |
| **Ahrefs Brand Radar** | Base de **199M+ prompts** ancorados em busca real; 6 motores (AIO, AI Mode, ChatGPT, Perplexity, Gemini, Copilot); **Agent A** (análise mensal automática); **Custom AI Prompt Tracking**; estudo "50 domínios mais citados em AI Overviews" | Volume de prompts e integração ao stack Ahrefs (Site/Keywords Explorer, GSC) | ahrefs.com/blog/most-cited-domains-ai-overviews/; businesswire 20-jan-2026 (Custom AI Prompt Tracking) |
| **Semrush AI Visibility Toolkit / Enterprise** | **SoV ponderado por volume de prompt** (desde out/2025); **AI Visibility Index** público enterprise; API + **acesso MCP** + 200 prompts rastreados | SoV calibrado por demanda real; leaderboard enterprise | semrush.com/blog/how-to-measure-ai-share-of-voice/; ai-visibility-index.semrush.com |
| **Peec AI / Otterly / AthenaHQ** | Consolidação da categoria de monitoramento contínuo (cf. wave 07-jun) | Monitoramento acessível multi-motor | (cf. wave 07-jun §3) |
| **Scrunch / Sitecore** | Aquisição (~US$ 225M, jun/2026) — AXP no DXP da Sitecore (cf. wave 07-jun) | GEO vira camada de DXP enterprise | (cf. wave 07-jun §3) |

**Sinal de mercado:** o ceticismo registrado em 07-jun (Digiday/SparkToro: resultados inconsistentes entre ferramentas) permanece válido. A contraparte construtiva é a profissionalização via Relevance Engineering (§1.3) e a separação de KPIs (§2.1), que tornam a triangulação defensável.

---

## 4. Papers acadêmicos novos — verificados via WebFetch (15-jun-2026)

### 4.1 GEO-SFE — arXiv:2603.29979 ✓ (Yu, Yang, Ding, Sato, 31-mar-2026)
"Structural Feature Engineering for Generative Engine Optimization: How Content Structure Shapes Citation Behavior". Decompõe estrutura em macro (arquitetura do documento), meso (chunking de informação) e micro (ênfase visual). Resultado: **+17,3% de citation rate** e **+18,5% de qualidade subjetiva** em 6 motores. Rubrica reprodutível — ver §1.2.

### 4.2 AgentGEO — arXiv:2603.09296 ✓ (Tian, Chen, Tang, Liu, Jia, 10-mar-2026)
"Diagnosing and Repairing Citation Failures in Generative Engine Optimization". Sistema agêntico de diagnóstico de modos de falha de citação + reparo dirigido. Resultado: **+40% de citação relativa modificando apenas 5% do conteúdo** (vs 25% de baselines). Reconcilia a referência anterior a `2603.09296` como "taxonomia de 7 tipos de falha": é exatamente uma taxonomia de falhas acoplada a reparo agêntico — ver §1.1.

> Os demais papers GEO/AEO permanecem como na wave 07-jun (§4): `2509.08919` (GEO/share of model), `2509.10762` (GEO-16), `2605.25517` (What Gets Cited ✓), `2605.12887` (EcoGEO ✓), `2604.25707` (Citation Selection→Absorption). Validar qualquer ID novo em `arxiv.org/abs/<ID>` antes de canonizar.

---

## 5. Camada semântica / espaço vetorial / embeddings / RAG (fundamento técnico)

Esta seção consolida o fundamento técnico atemporal — base de **recuperabilidade** e **citabilidade** — sintetizado pelo geo-orchestrator (wave1 t2) e cruzado com o cânone. Responde "por que estrutura semântica gera citação" na camada da máquina.

### 5.1 Da busca lexical à nuvem semântica
Sistemas clássicos (TF-IDF, BM25) operam por sobreposição de termos. A partir de embeddings densos e Transformers, texto vira vetor em espaço de alta dimensão, onde proximidade geométrica (similaridade de cosseno) corresponde a proximidade semântica. A **nuvem semântica** é o ecossistema de índices vetoriais, lexicais, grafos de conhecimento e caches sobre o qual ChatGPT, Gemini, Perplexity e Claude recuperam — estratificada por granularidade (token → sentença → parágrafo → documento) e multimodal.

### 5.2 Embeddings, bi-encoders e cross-encoders
- **Embedding** = função que mapeia texto em vetor; treino contrastivo (InfoNCE, in-batch negatives) aproxima pares relevantes. Dimensionalidades típicas 256-4096 (768/1024 são bom equilíbrio).
- **Bi-encoder**: codifica consulta e documento separadamente; escalável (pré-computa vetores; busca por vizinhos aproximados). É o filtro de primeiro estágio.
- **Cross-encoder**: processa consulta+documento juntos; mais preciso, caro; usado como **reranker** de segundo estágio.
- O pipeline real dos motores combina os dois: bi-encoder recupera candidatos, cross-encoder/LLM reranqueia — o que explica como escala e qualidade coexistem.

### 5.3 Indexação ANN, índices lexicais e grafos
Busca aproximada de vizinhos (ANN) via **HNSW** (grafo hierárquico navegável) e **IVF + Product Quantization** torna a recuperação sublinear. Índices lexicais (posting lists/BM25) seguem essenciais para match exato e filtragem; grafos de conhecimento dão grounding factual e desambiguação de entidade; metadados (data, autoridade de domínio, idioma, frescor) governam elegibilidade e ordenação de citação.

### 5.4 Chunking: a ponte direta com GEO-SFE
Chunking por tamanho fixo é simples mas ignora estrutura, produzindo blocos que começam no meio de uma ideia. Chunking **estrutural/semântico** (por títulos, seções, fronteiras de sentido) é superior — e é exatamente o nível **meso** do GEO-SFE (§1.2). A implicação unificada: conteúdo que vence é chunkável por estrutura, denso em evidência extraível, terminologicamente consistente (acopla com embeddings de entidade), alinhado ao prompt e interligado em ecossistema (trajetória do agente, cf. EcoGEO).

---

## 6. Convergência SEO + GEO e tendências (delta jun/2026)

### 6.1 Google I/O 2026 e busca
- **Gemini 3.5 Flash** vira modelo default no AI Mode globalmente.
- **Personal Intelligence** no AI Mode expande para ~200 países e 98 idiomas, sem assinatura.
- "Maior upgrade da caixa de busca em 25 anos": expansão dinâmica, sugestões com IA, busca multimodal (texto, imagens, arquivos, vídeos, abas do Chrome).
- **Follow-up direto a partir de um AI Overview**, fluindo para conversa no AI Mode, com contexto preservado e links ficando mais relevantes (desktop e mobile, mundial).
- **Search Agents**: agentes de informação 24/7 (verão/2026, assinantes Pro/Ultra) que monitoram a web por critérios do usuário; reservas agênticas; Google liga para empresas em nome do usuário em categorias selecionadas.
- Fonte: blog.google/products-and-platforms/products/search/search-io-2026/ (verificado).

### 6.2 Zero-clique e valor da citação
- **SparkToro 2026**: **68,01%** de zero-clique no início de 2026 (era 60,45% em 2024); apenas **276 cliques por 1.000 buscas** chegam à web aberta (era 374), queda de 26% em dois anos; só **0,34%** das buscas migraram para AI Mode (jan-abr). Recomendação de Rand Fishkin: investir em marca e influência nas plataformas onde o público já está, independentemente de cliques diretos. (sparktoro.com)
- Contraponto: ser citado em AIO vale ~120% mais cliques/impressão (Seer, §2.4) — o valor migra de clique para presença na resposta.

### 6.3 Comércio agêntico e monetização
- OpenAI iniciou **anúncios no ChatGPT em 09-fev-2026** (tiers Free/Go; Plus/Pro/Business/Enterprise/Education sem anúncio), com pivô de Instant Checkout para descoberta de produto. Guerra de agentes de compra em 2026: ChatGPT, Amazon Rufus, Perplexity (Comet), Alexa+. **Implicação:** elegibilidade da marca em fluxos de compra agênticos vira frente de GEO, distinta da citação textual.

### 6.4 Padrões de acesso: de llms.txt a AIPREF
- **llms.txt** ~10% de adoção (SE Ranking, 300k domínios, início 2026; tech/blockchain 20-30%, media/legal/insurance <10%); segue **convenção comunitária**, não padrão formal. O futuro do controle de crawler de IA é moldado pelo **IETF AIPREF** (`draft-ietf-aipref-attach` — "Associating AI Usage Preferences with Content in HTTP") e pela indústria de CDN. **Implicação:** preparar `/.well-known/ai-preferences`; manter llms.txt como defensivo, nunca como requisito ou talismã.

---

## 7. Aplicação por repositório

### 7.1 landing-page-geo (alexandrecaramaschi.com / Brasil GEO)

1. **Dashboard / `/roadmap`:** adicionar **Share of Answer** e **Recommendation Rate** ao lado de AI Share of Voice (headline). Estruturar o report mensal nas 8 seções canônicas (§2.3); manter ≤11 KPIs no board.
2. **Artigo HBR-grade novo:** "Ser citado vale 120% mais cliques: o ROI do zero-clique" — traduz o RCT de AIO e o dado da Seer (§2.4) para CMO brasileiro.
3. **Artigo HBR-grade novo:** "Relevance Engineering: por que SEO virou engenharia de relevância" — enquadra o serviço Brasil GEO acima de leitura de dashboard (§1.3).
4. **Rubrica de auditoria on-page:** adotar os três níveis do GEO-SFE (macro/meso/micro, §1.2) como pontuação de auditoria, somando ao GEO-16. Documentar o lift (+17,3%) como referência.
5. **Schema / discovery files:** preparar `/.well-known/ai-preferences` (AIPREF) e acompanhar `draft-ietf-aipref-attach`; revisar llms.txt como defensivo (§6.4).
6. **Fluxo de trabalho de cliente:** adotar o ciclo diagnosticar-reparar do AgentGEO (§1.1) — intervir cirurgicamente em páginas que falham citação, não reescrever tudo.

### 7.2 papers (pesquisa empírica multi-vertical)

1. **Ingestão de papers (Related Work / Paper 5):** adicionar `2603.29979` (GEO-SFE) e `2603.09296` (AgentGEO), ambos verificados. Tagueá-los contra os Conceitos 11/13/15/24/25 e contra CSR/CAR.
2. **Variáveis de controle estruturais:** operacionalizar os três níveis do GEO-SFE (macro/meso/micro) como features mensuráveis na coleta, correlacionando com taxa de citação observada por vertical — ponte direta §5↔desenho estatístico.
3. **Novo KPI no schema:** adicionar **Share of Answer / Recommendation Rate** ao lado de citation_selection_rate/citation_absorption_rate; alinhar o prompt portfolio para distinguir "listado" de "recomendado".
4. **Hipóteses falsificáveis:** o lift de AgentGEO (+40% com 5% de mudança) e os fatores estruturais de GEO-SFE viram hipóteses pré-registradas no dataset longitudinal brasileiro — não há replicação PT-BR. O dado do RCT de AIO (-38% cliques, +120% para citados) é hipótese de impacto de negócio a testar.
5. **Cautela metodológica canônica:** registrar no METHODOLOGY que "deep research" sem busca live fabrica citações (§0, premissa 7); toda fonte datada exige verificação primária.

### 7.3 curso-factory (fábrica de cursos EAD GEO-first)

1. **Módulo novo "Share of Voice vs Share of Answer":** ensina a distinção canônica (§2.1) e a bateria de KPIs (§2.2) + estrutura de report de 8 seções. Conceitos GEO-core 24/25.
2. **Módulo novo "Relevance Engineering":** a disciplina de Michael King (§1.3) como enquadramento profissional; aula de "engenharia de relevância, não leitura de dashboard".
3. **Rubrica de redação (`GEO_REDACAO_CHECKLIST_2026.md`) + prompts:** incorporar os três níveis do GEO-SFE (macro/meso/micro) ao `draft.md` e ao `content_checker.py` (validar arquitetura de seções, self-containment de chunk, ênfase de termos/números). O `reviewer.py` (Claude) adota o checklist de diagnóstico-reparo do AgentGEO.
4. **Tags do `classify.md`:** adicionar `share-of-answer`, `relevance-engineering`, `structural-features`, `agentic-commerce`.
5. **Módulo novo "Comércio agêntico e a nova superfície de descoberta":** ChatGPT com ads, guerra de agentes de compra, elegibilidade em fluxos de ação (§6.3); aula de AIPREF vs llms.txt (§6.4).

---

## 8. Anti-padrões e cautelas reforçados (jun-15/2026)

- **Confiar em "deep research" sem busca live** — proibido. Verificar resultado de busca não-vazio e validar fonte primária; arXiv via WebFetch (esta wave flagrou fabricação iminente em motor de pesquisa sem busca).
- **Reportar só Share of Voice** — insuficiente. Reportar também Share of Answer e Recommendation Rate (§2.1).
- **Reescrever a página inteira para ganhar citação** — ineficiente. Diagnosticar a falha e reparar 5% (AgentGEO, §1.1).
- **Tratar llms.txt como requisito/talismã** — falso. O padrão real é AIPREF (§6.4).
- **Métrica única de uma ferramenta / métrica absoluta / métrica agregada cross-plataforma** — permanecem proibidos (wave 07-jun §8).
- **Alucinação de arXiv ID e GhostCite (14-95% de citações fabricadas)** — fonte verificável é diferencial competitivo, não só higiene.

---

## 9. Pool de URLs verificáveis (consolidado, 15-jun-2026)

**Papers (arXiv):**
- https://arxiv.org/abs/2603.29979 — GEO-SFE (✓ verificado, 31-mar-2026)
- https://arxiv.org/abs/2603.09296 — AgentGEO (✓ verificado, 10-mar-2026)
- https://arxiv.org/abs/2605.25517 · https://arxiv.org/abs/2605.12887 · https://arxiv.org/abs/2604.25707 · https://arxiv.org/abs/2509.08919 · https://arxiv.org/abs/2509.10762 (cf. wave 07-jun)

**Vendors / mercado:**
- https://fortune.com/2026/02/24/exclusive-as-ai-threatens-search-profound-raises-96-million-to-help-brands-stay-visible/
- https://www.tryprofound.com/
- https://ahrefs.com/blog/most-cited-domains-ai-overviews/
- https://www.businesswire.com/news/home/20260120714417/en/Ahrefs-Launches-Custom-AI-Prompt-Tracking-for-Brand-Visibility
- https://www.semrush.com/blog/how-to-measure-ai-share-of-voice/ · https://ai-visibility-index.semrush.com/ · https://www.semrush.com/blog/measure-ai-visibility/

**KPIs / medição:**
- https://lseo.com/answer-engine-optimization-services/share-of-answer-vs-share-of-voice-a-2026-measurement-guide/
- https://citedme.co/blog/ai-search-visibility-metrics-kpis · https://www.omnibound.ai/blog/ai-search-visibility-metrics
- https://www.searchenginejournal.com/ai-overviews-cut-organic-clicks-38-field-study-finds/573145/
- https://www.seerinteractive.com/insights/aio-impact-on-google-ctr-september-2025-update

**SEO / Google / tendências:**
- https://blog.google/products-and-platforms/products/search/search-io-2026/
- https://sparktoro.com/blog/in-2026-less-than-one-third-of-google-searches-still-send-a-click/
- https://searchengineland.com/google-zero-click-searches-2026-study-479717
- https://almcorp.com/blog/chatgpt-ads-aggressive-placement-pricing-analysis/ (ChatGPT ads, 09-fev-2026)
- https://www.modernretail.co/technology/why-the-ai-shopping-agent-wars-will-heat-up-in-2026/

**Padrões / discovery:**
- https://www.ietf.org/blog/aipref-wg/ · https://ietf-wg-aipref.github.io/drafts/draft-ietf-aipref-attach.html
- https://presenc.ai/research/state-of-llms-txt-2026

**Thought leadership:**
- https://ipullrank.com/ai-search-manual (Relevance Engineering, Michael King)
- https://www.advancedwebranking.com/blog/optimizing-new-search-how-relevance-engineering-is-reshaping-seo

> **Próxima atualização:** trimestral (~set/2026) ou ao primeiro evento estrutural (novo core update, novo modelo default, nova aquisição relevante). Citar `§X.Y` desta wave ao tomar decisões.
