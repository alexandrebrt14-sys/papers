# Wave Junho 19 2026 · Incremento canônico GEO/SEO — pesquisa profunda multi-LLM (mai–19/jun 2026)

> **Data de corte:** 19 de junho de 2026.
> **Status:** **complementa — não substitui** o `GEO_WAVE_JUNHO_15B_2026_CANONICAL.md` (15-jun, 2ª passada) e todo o corpus anterior. Onde houver conflito de fato datado, **esta passada prevalece** apenas nos itens explicitamente marcados como correção (§7). Tudo o que a 15B já canonizou (papers `2605.25517`, `2606.12439`, `2605.29107`; SparkToro 68,01%; Seer +120%; RCT −38%; Profound Série C; Scrunch/Sitecore; Semrush×Perplexity MCP; Clarity AI Citations GA; Lily Ray spam; AIPREF vs llms.txt) **permanece válido e não é repetido aqui** — este documento é o **delta** mai–jun 2026.
> **Fontes e método (transparência):** pesquisa profunda em **três LLMs de ponta, em paralelo, com web ao vivo**, orquestrada pelo Claude e cruzada com doublecheck próprio:
> 1. **OpenAI `gpt-5.5`** (Responses API + ferramenta `web_search`) — espinha factual, com IDs arXiv e datas verificados na fonte.
> 2. **Google `gemini-3.1-pro-preview`** (com `google_search` grounding) — complemento e triangulação.
> 3. **Perplexity `sonar-deep-research`** (80 sub-buscas; 33 citações) — profundidade do Google I/O 2026 e papers de atribuição/alucinação.
> 4. **Doublecheck do Claude** (WebSearch + WebFetch página a página em arXiv/Search Central/Ahrefs/SparkToro) — toda afirmação datada abaixo foi conferida em fonte primária; conflitos entre LLMs estão isolados em §7.
> Raws preservados em [`raw/`](raw/) (`openai_gpt55.json`, `gemini_31_pro.json`, `perplexity_sonar_deep_research.json`).
> **Como aplicar:** leitura obrigatória **antes** de qualquer decisão sobre schema/llms.txt, briefing de redação GEO, escolha de KPI/ferramenta de AI visibility, ou copy pública que cite "boas práticas de GEO". Os itens de §7 **revogam clichês** que ainda circulam no mercado (e em conteúdo antigo).

---

## 0. Sumário executivo (TL;DR) — o que é NOVO em mai–19/jun 2026

O evento dominante do período é o **Google assumir oficialmente a narrativa de GEO**: em 15-mai e 15-jun o Search Central publicou o primeiro guia consolidado de otimização para experiências generativas, que (a) revela a mecânica real — **RAG + grounding + query fan-out** — e (b) **desmonta cinco "hacks" de GEO** que o mercado vendia. Em paralelo, dois estudos causais da Ahrefs derrubaram mitos caros (schema e llms.txt), a infraestrutura de medição começou a existir (GA4 e GSC), e a comunidade reagiu com ceticismo qualificado (Michael King, Aimee Jurenka, Aleyda Solís). A tese Brasil GEO não muda — **GEO é engenharia de relevância para recuperação e citação** —, mas o período **profissionaliza o discurso** e **encerra a era dos arquivos mágicos**.

| Achado NOVO (não estava na 15B) | Número-chave / fonte primária | Impacto canônico |
|---|---|---|
| **Google oficializa "GEO para Search ainda é SEO"** — guia consolidado de AI optimization | Google Search Central, publicado 15-mai, atualizado 15-jun-2026 (`developers.google.com/search/docs/fundamentals/ai-optimization-guide`) | Revela RAG + **query fan-out**; define a unidade de competição como o **trecho que melhor responde a subconsultas geradas**. Indexação/rastreabilidade/elegibilidade a snippet continuam sendo a base. |
| **Google lista 5 táticas "não precisa fazer"** | Mesmo guia, 15-jun-2026 | `llms.txt`, markup especial p/ IA, chunking obrigatório, reescrita "para IA" e overfoco em structured data são declarados **desnecessários** para AI Overviews/AI Mode. |
| **Google: cuidado com ferramentas/conselhos AEO/GEO de terceiros** | Google Search Central `third-party-seo`, atualizado 5-jun-2026 | Terceiros têm **zero acesso** a dados internos de ranking; claims de "otimização aprovada pelo Google" devem ser tratados como marketing. |
| **Ahrefs derruba o mito do schema** | 1.885 páginas que adicionaram JSON-LD vs 4.000 controles (diff-in-diff): AIO **−4,6%**, AI Mode +2,4%, ChatGPT +2,2% · Ahrefs, 11-mai-2026 (`ahrefs.com/blog/schema-ai-citations`) | **Schema não é alavanca causal de citação em IA.** Contradiz o clichê "schema +67%". Útil para rich results e parsing — não como substituto de conteúdo único. |
| **Ahrefs: 97% dos `llms.txt` nunca recebem requisição** | 137 mil domínios; dos ~38 mil com `llms.txt` válido, **97% tiveram zero requisições em maio**; bots de IA nomeados = 19,5% dos fetches · Ahrefs, 15-jun-2026 (`ahrefs.com/blog/llmstxt-study`) | Evidência de servidor (complementa o "10,13% de adoção / correlação zero" da SE Ranking na 15B): llms.txt é estatisticamente ignorado pelos LLMs. |
| **Profound: tempo até a primeira citação** | Mediana **6,81 dias**; P75 18,68; P90 37,10 dias · Profound Research Hub, 20-mai-2026 | Conteúdo novo entra no pool de citações de IA em **dias**, não meses. |
| **Semrush: volatilidade de fontes UGC** | Estudo interno de **230 mil prompts**: citações do Reddit pelo ChatGPT caíram de ~60% → ~10% das respostas em poucas semanas · Semrush, 29-mai-2026 | Fontes UGC são **voláteis**; e **citação ≠ recomendação** (marca pode ser citada e ainda perder a recomendação comercial). |
| **AI Mode vira superfície de massa** | **1 bilhão+** de usuários ativos mensais globais; queries mais que dobraram a cada trimestre desde o lançamento · Google, 19-mai-2026 (`blog.google`) | AI Mode deixou de ser experimento marginal. |
| **Google I/O 2026: reconfiguração agentic do Search** | Gemini 3.5 Flash como modelo padrão do AI Mode; nova caixa de busca ("maior upgrade em 25 anos", multimodal); continuidade AI Overviews→conversa; Personal Intelligence em ~200 países · Google I/O, mai-2026 | A intenção desloca de keyword literal para descrição rica → mais peso semântico/contexto. |
| **Medição oficial começa a existir (sem cliques)** | GA4: canal padrão **"AI Assistant"** (medium `ai-assistant`), 15-mai · GSC: relatórios de AI Search em teste (UK), com impressões e granularidade horária, **sem click data**, + toggle de opt-out, 5-jun | Stack mínimo de medição = GSC/GA4 + amostragem de prompts; impressão/menção viram o KPI inicial, não CTR. |
| **Regulação separa AI Search de indexação** | Reino Unido: Google tem **9 meses** para cumprir exigência de opt-out de AI Overviews/AI Mode e treinamento · SEJ, 5-jun-2026 | Primeiro caso regulatório tratando AI Search como camada distinta. |
| **Novos papers de mecânica e segurança** | `EcoGEO` (`arXiv:2605.12887`, 13-mai) — ecossistemas de evidência; `SCI-Defense` (`arXiv:2605.21948`, 21-mai) — defesa contra manipulação GEO (Precision 1,000 / FPR 0,000) | GEO migra de "página isolada" para **trajetória/ecossistema**; spam semântico é detectável. |
| **AWR — arquitetura e mecânica de LLM (capítulo-base)** | Gianluca Fiorelli, 21-jan-2026 (`advancedwebranking.com/seo/llm-architecture-and-mechanics`) + AWR/Aimee Jurenka, 11-mai: "single-shot prompt não basta" | Fundamenta o vocabulário: tokenização, embeddings, atenção O(n²), perplexidade; medir AI visibility exige **múltiplas execuções e média de mention rate**. |

### Seis premissas operacionais consequentes (a partir de 19-jun-2026)

1. **Pare de vender "arquivos mágicos".** O próprio Google declarou `llms.txt`, markup-p/-IA, chunking e reescrita-p/-IA como desnecessários para Search; a Ahrefs mostrou que `llms.txt` é ignorado (97% sem requisição) e que schema não move citação. **Aplicação:** copy e auditoria Brasil GEO nunca apresentam esses itens como alavanca causal — schema fica como higiene de rich results; llms.txt como defensivo B2A de baixo custo.
2. **Otimize para subconsultas (fan-out) e passagens, não para a keyword única.** **Aplicação:** cada artigo cobre o leque de reformulações de um tópico com seções claras, respostas diretas e evidência verificável; chunks autocontidos com números/nomes vencem o reranking.
3. **GEO para Google Search = SEO sólido aplicado a experiências generativas.** Indexabilidade, rastreabilidade e elegibilidade a snippet continuam sendo a base. **Aplicação:** o pitch separa "SEO técnico (base)" de "engenharia de evidência e entidade (camada GEO)" — sem prometer atalho técnico.
4. **Conteúdo não comoditizado é o diferencial estrutural.** Google distingue explicitamente commodity de conteúdo com experiência/ponto de vista; AWR confirma que "skyscraper genérico" e AI slop perderam força. **Aplicação:** rubrica de redação prioriza nicho, autoridade declarada e evidência datada.
5. **Meça por superfície e por estágio: impressão → menção → citação → recomendação.** GA4/GSC só capturam o que chega ao site; citação sem clique exige amostragem de prompts; AIO ≠ AI Mode ≠ ChatGPT ≠ Perplexity. **Aplicação:** todo report nomeia metodologia e fonte de cada número; nunca comparar SoV de fornecedores diferentes lado a lado.
6. **Earned media offsite tem ROI, mas menção artificial é risco.** Profound estima 10+ horas/placement; Google reforça que menções inautênticas caem nos sistemas de spam. **Aplicação:** distribuição legítima (PR, comunidade, journals) — nunca prompt injection ou texto manipulativo.

---

## 1. Google oficializa a mecânica (o evento do período)

### 1.1. O guia de AI optimization do Search Central
Em **15-mai-2026** o Google publicou o primeiro guia consolidado para otimizar sites para recursos generativos da Busca (AI Overviews e AI Mode), atualizado em **15-jun**. Pontos canônicos:
- A mecânica é **RAG/grounding sobre o índice da Busca + query fan-out**: o modelo gera consultas relacionadas concorrentes para cobrir subtópicos. Exemplo oficial: "how to fix a lawn that's full of weeds" gera subconsultas sobre herbicidas, remoção sem químicos e prevenção.
- **Cinco táticas declaradas desnecessárias** ("you don't need to"): `llms.txt`, markup especial para IA, chunking obrigatório, reescrita de conteúdo "para IA", e overfoco em structured data.
- Blocos do guia: conteúdo único (não-commodity), conteúdo local/shopping/imagem/vídeo, mythbusting AEO/GEO, agentes, e "SEO continua sendo a base".
- Fonte: `developers.google.com/search/docs/fundamentals/ai-optimization-guide` (15-mai/15-jun-2026); blog `developers.google.com/search/blog/2026/05/a-new-resource-for-optimizing`.

### 1.2. Guia sobre conselhos/ferramentas de terceiros
Em **5-jun-2026** (versões localizadas 9–10/jun), o Search Central publicou orientação `third-party-seo`: ferramentas de SEO/AEO/GEO de terceiros **não têm acesso** aos dados internos de ranking do Google e não podem garantir performance; conselhos devem ser verificados contra documentação oficial. **Implicação:** trate "otimização aprovada pelo Google" como marketing.

### 1.3. Google I/O 2026 — Search como ambiente agentic
- **Gemini 3.5 Flash** vira o modelo padrão global do AI Mode (otimizado para uso sustentado em agentes e código, baixa latência).
- Nova **caixa de busca inteligente** (descrita como o maior upgrade em 25 anos): multimodal, expansão dinâmica, entrada de imagens/arquivos/vídeos/abas do Chrome → desloca a mediação de keyword literal para descrição rica.
- **Continuidade AI Overviews → conversa** (follow-up direto do Overview), com refinamento progressivo de links de suporte.
- **Personal Intelligence** expandida para ~200 países (Gmail, Fotos, em breve Agenda); mini-apps gerados on-the-fly (plataforma Antigravity).
- Fonte: cobertura do Google I/O 2026 (mai-2026) + `blog.google/products-and-platforms/products/search/`.

### 1.4. Outras mudanças de plataforma datadas
- **6-mai:** Google anuncia 5 novas formas de explorar a web com IA generativa na Busca (mais links diretos, sugestões de artigos).
- **29-mai:** Preferred Sources expandido para AI Overviews e AI Mode.
- **21-mai a 2-jun:** **May 2026 Core Update** (2ª core update do ano; rollout de 11 dias). Profissionais reportaram recuperação em ranking tradicional com perda em AI answer placements; Aleyda Solís resumiu que "fit do tipo de fonte importou mais que autoridade isolada".
- **15-mai:** FAQ rich results — filtro/relatório removidos; suporte de API encerra em agosto.
- **1-jun:** ChatGPT passa a buscar vagas ao vivo (Indeed, Upwork, Appcast).
- **20-mai:** Chrome Lighthouse adiciona auditoria experimental de `llms.txt` na categoria "Agentic Browsing" (uso para **agentes**, não para Search) — contradição prática sinalizada por Danny Goodwin (Search Engine Land).

---

## 2. Estudos causais que derrubam mitos (Ahrefs)

### 2.1. Schema NÃO é alavanca causal de citação em IA
- **"We Tracked 1,885 Pages Adding Schema. AI Citations Barely Moved"** — Ahrefs (Louise Linehan, Xibeijia Guan; revisão Ryan Law), **11-mai-2026**.
- Método: análise inicial de 6 milhões de URLs; depois diff-in-diff com **1.885 páginas** que adicionaram JSON-LD entre ago/2025 e mar/2026, pareadas contra **4.000 controles**.
- Resultado: Google AIO **−4,6%** (única variação pequena e estatisticamente significativa, e negativa), AI Mode **+2,4%**, ChatGPT **+2,2%**. Conclusão: schema é útil para rich results e compreensão estruturada, **não** para mover citação em IA.
- Fonte: `ahrefs.com/blog/schema-ai-citations`.

### 2.2. llms.txt é ignorado na prática
- **"We Analyzed 137K Sites: 97% of llms.txt Files Never Get Read"** — Ahrefs, **15-jun-2026**.
- Dos ~38 mil domínios com `llms.txt` válido, **97% tiveram zero requisições em maio**; entre os fetches que ocorreram, **19,5%** vieram de ferramentas de IA nomeadas (lideradas por GPTBot e Claude-Code) e ~12% de scanners/auditores.
- Complementa a 15B (SE Ranking: 10,13% de adoção, correlação zero com citação) com evidência de **log de servidor**.
- Fonte: `ahrefs.com/blog/llmstxt-study`; cobertura `searchenginejournal.com/97-of-llms-txt-files-got-no-requests-ahrefs-data-shows`.

---

## 3. Papers acadêmicos novos (mai-2026, verificados em arXiv)

> A 15B já canonizou `2605.25517` (What Gets Cited), `2606.12439` (governança ICML) e `2605.29107` (GEO-Bench). Abaixo, os **adicionais** deste delta.

- **EcoGEO: Trajectory-Aware Evidence Ecosystems for Web-Enabled LLM Search Agents** — `arXiv:2605.12887` (13-mai-2026; Ye, Mao, Guan, Tian). GEO deixa de ser "otimizar uma página" e passa a **otimizar um ecossistema de evidências**: páginas de entrada, de suporte, terminologia compartilhada e links internos moldam a trajetória de navegação do agente. Benchmark: OPR-Bench. (Percentual de uplift não publicado no abstract.)
- **SCI-Defense: Defending Manipulation Attacks from Generative Engine Optimization** — `arXiv:2605.21948` (21-mai-2026; Yu, Jin, Zeng, Wang; submissão NeurIPS 2026). Combina Perplexity detection + Semantic Integrity Scoring + Inter-Candidate Detection. Avaliação: 600 descrições Amazon (6 categorias) + 600 passagens MS MARCO. **Precision 1,000 / FPR 0,000**; Recall 1,000 / 0,952 / 0,830 contra ataques String/Reasoning/Review; defesas ingênuas (PPL-only, SafetyClf, paraphrasing) tiveram **recall zero** contra ataque semântico.
- **Telematics and Informatics — "A search changer: auditing Google's AI overviews interface in political and news search"** — Shir Weinbrand, edição jun-2026 (DOI 10.1016/j.tele.2026.102417). AI Overviews têm padrões estruturais distintos em política vs notícias.
- **Tema transversal (Perplexity):** trabalhos de 2026 sobre **atribuição e alucinação** documentam taxas substanciais de citações inexistentes/misatribuídas em LLMs públicos — reforçando que verificação humana de fonte continua obrigatória em qualquer pipeline GEO.

---

## 4. Mecânica de citação e arquitetura (série canônica AWR — Fiorelli)

> **Referência indicada (2×) pelo cliente.** O "Comprehensive Guide to Generative AI" de Gianluca Fiorelli (Advanced Web Ranking, base publicada 21-jan-2026, índice em `advancedwebranking.com/seo/generative-ai-guide`) é o tratado de referência sobre a mecânica que sustenta GEO. **7 capítulos** — fundamento técnico atemporal que ancora os achados datados deste período:

| # | Capítulo | URL (`/seo/...`) | Núcleo para GEO |
|---|---|---|---|
| 1 | **The Model: LLM Architecture and Mechanics** | `llm-architecture-and-mechanics` | LLM = máquina probabilística que minimiza perplexidade (não banco de dados); tokenização (~100 tokens ≈ 75 palavras), embeddings densos (1.536/3.072 dim), atenção **O(n²)** como gargalo, positional encoding, monosemanticidade/interpretabilidade, speculative decoding (latência 2–3×), context caching (KV). |
| 2 | **The Agent: Reasoning, Planning, and Action** | `ai-agent-reasoning-and-action` | Agente = perfil + memória (curta/longa) + planejamento + ferramentas; **tool/function calling** (JSON estruturado, com risco de prompt injection); frameworks de raciocínio **CoT / Tree-of-Thoughts / ReAct** (Thought→Action→Observation). |
| 3 | **The Library: Neural Search and Retrieval Architectures** | `neural-search-and-retrieval-architectures` | **RAG** (open-book), Agentic RAG (multi-passo, autocorreção), **GraphRAG**; algoritmos: Dense Retrieval (semântica), **BM25** (sparse/técnico — "nunca descartar"), **Hybrid (fusão RRF)**, HyDE, query expansion. "O algoritmo escolhido determina o que é encontrado e o que é perdido." |
| 4 | **The Strategy: SEO for AI Search** | `build-strategy-for-ai-search` | **Framework de 4 pilares** (abaixo) + **estratégia em 4 camadas**; otimizar para **inclusão na janela de contexto**, não só posição no SERP. |
| 5 | **The Technical Foundation** | `technical-seo-for-ai-search` | Acessibilidade total a crawlers/retrievers/agentes (camada 1). |
| 6 | **Content and AI Search** | `content-ai-search` | Design semântico: entidades, hubs, **chunks coerentes** (camada 2). |
| 7 | **Amplification** | `amplification-ai-search-seo` | Distribuição: evidência off-site, salience de marca (camada 3). |

**Os 4 pilares (Cap. 4) — vocabulário canônico de auditoria GEO:**
1. **Retrieval** — "o sistema consegue te *encontrar*?" (neural search + RAG).
2. **Reasoning** — "consegue *usar* seu conteúdo para pensar?" (clareza/estrutura para CoT).
3. **Agency** — "consegue *agir* através de você?" (APIs, tool calling, prontidão B2A).
4. **Authority & Memory** — "*confia* em você?" (knowledge graphs, entidades, salience de marca).

**As 4 camadas de execução:** (1) fundação técnica → (2) conteúdo & arquitetura semântica → (3) amplificação/sinais off-site → (4) medição & iteração (dados clássicos + análise de respostas de IA).

**Convergência com o resto desta wave:** os 4 pilares casam 1:1 com (a) o pipeline de 4 estágios da Wave 15B §2 (retrieval = recall híbrido BM25+vetor; reasoning/authority = reranking + atribuição com viés a domínios confiáveis), (b) os preditores de citação de `2605.25517` (relevância tópica + posição alimentam Retrieval; recência/preço explícito alimentam Reasoning), e (c) a tese EcoGEO `2605.12887` (Agency/Authority = ecossistema de evidência e trajetória do agente, não página isolada). **Aplicação:** usar os 4 pilares como eixos do relatório de auditoria de cliente (uma nota por pilar) e a sequência de 4 camadas como ordem de execução do projeto.
- **AWR / Aimee Jurenka** (11-mai-2026, "engineering SEO ecosystem for AI search era"): respostas de IA variam entre execuções → **single-shot prompt tracking não basta**; medir AI visibility exige múltiplas execuções e média de mention rate. Caso citado: 4–5 posts por categoria, 87 links/visitas via PR, marca recuperada em 2–3 semanas.
- **Consenso de pipeline (corrobora 15B):** indexação híbrida (lexical BM25 + vetorial + grafo de entidades) → recall híbrido + query fan-out → reranking neural (cross-encoder) + seleção de chunks citáveis → geração + atribuição com viés a domínios confiáveis.

---

## 5. Medição e ferramentas (a infra começa a existir)

- **GA4** (15-mai): tráfego de assistentes de IA atribuído a canal padrão **"AI Assistant"** (medium `ai-assistant`, campaign `(ai-assistant)`); exemplos: ChatGPT, Gemini, Claude. Mede só visitas que chegam ao site — não a resposta sem clique.
- **Google Search Console** (5-jun): relatórios de AI Search em teste num subconjunto de sites do Reino Unido — impressões, páginas, países, dispositivos, granularidade **horária**, **sem click data** + toggle de opt-out. Glenn Gabe comemorou a chegada mas criticou a ausência de cliques.
- **Profound** (20-mai): tempo até citação (mediana 6,81 dias); (26-mai) Noble Nodes para Profound Agents — estima 10+ horas de trabalho manual por placement offsite; (9-jun) "World Cup 2026: Who Wins AI Search" — benchmark em **9 motores** (ChatGPT, Perplexity, Google AI Mode, AI Overviews, Gemini, Copilot, Grok, Meta AI, Claude).
- **Semrush** (29-mai): "How we're driving AI visibility at Semrush" — separa citação de recomendação/posicionamento; estudo interno de 230 mil prompts; volatilidade do Reddit no ChatGPT (60%→10%).

---

## 6. Comentários impactantes (figuras-chave e comunidade)

- **Michael King (iPullRank)** — "Google's AI search guidance is naive and self-serving" (Search Engine Land, 22-mai): o guia do Google deve ser lido com ceticismo; critica a recepção binária ("é só SEO" vs "Google está mentindo").
- **Aimee Jurenka (AWR)** — "single-shot prompts don't work"; medir por amostragem e mention rate.
- **Aleyda Solís** — no May Core Update, "fit do tipo de fonte > autoridade isolada".
- **Glenn Gabe** — AI reporting no GSC é avanço, mas sem click data está incompleto.
- **Roger Lynch (Condé Nast)** — orientou times a **planejar como se o tráfego de busca fosse zero** (espera estabilização em 1 dígito % do tráfego total); assinaturas digitais +29% de receita no ano; Chartbeat: −60% de referrals de busca para pequenos publishers em 2 anos; Reuters Institute: expectativa de −40%+ em 3 anos (SEJ, 15-mai).
- **Comunidade (r/AISearchOptimizers, 15-jun):** post alegando que "42% das citações de IA vieram de páginas que não eram #1 no Google" — **sem metodologia auditável** (isolado como anedótico, não canonizado).

---

## 7. Correções / desmistificações (revogam clichês em circulação)

> Estes itens **revogam** afirmações que ainda aparecem em conteúdo de GEO (inclusive material antigo). Em conflito, prevalece o estudo causal/fonte primária.

| Clichê em circulação | Correção verificada (mai–jun 2026) | Fonte |
|---|---|---|
| "Schema markup melhora descoberta por LLM em ~67%" | Estudo causal (diff-in-diff, 1.885 páginas): AIO **−4,6%**, AI Mode +2,4%, ChatGPT +2,2% — **sem uplift relevante**. | Ahrefs, 11-mai-2026 |
| "llms.txt aumenta citação em IA" | 97% dos arquivos sem requisição (137k domínios); Google diz que não usa; serve a agentes (B2A), não a ranking. | Ahrefs 15-jun; Google Search Central 15-jun |
| "Reddit é fonte nº 1 fixa (~40%) das citações de IA" | Fontes UGC são **voláteis**: Reddit no ChatGPT caiu de ~60% → ~10% das respostas em semanas (230k prompts). Tratar como série temporal, não constante. | Semrush, 29-mai-2026 |
| "GEO é uma camada técnica separada do SEO" | Para Google Search, GEO/AEO **é SEO** aplicado a experiências generativas; sem arquivos mágicos. | Google Search Central, 15-jun-2026 |
| "Um prompt = um ranking de visibilidade em IA" | Respostas variam por execução; medir exige múltiplas rodadas e média de mention rate. | AWR/Aimee Jurenka, 11-mai-2026 |
| "Ferramentas AEO/GEO têm dados do ranking do Google" | Terceiros têm **zero acesso** a dados internos de ranking. | Google Search Central, 5-jun-2026 |

---

## 8. Aplicação direta nos ativos Brasil GEO

- **Rubrica de redação (`GEO_REDACAO_CHECKLIST_2026.md`):** manter Cite Sources ≥3 / Stats ≥5 / Quotes ≥1 / answer capsule; **adicionar** ênfase em (a) casamento tópico forte + dados datados (preditor de citação per `2605.25517`), (b) cobertura do leque de subconsultas (fan-out), (c) conteúdo não-commodity. **Remover** qualquer promessa de "schema/llms.txt = mais citação".
- **Auditoria/dashboard de cliente:** medir nos dois eixos (recuperável × citado) e por superfície (AIO/AI Mode/ChatGPT/Perplexity); nomear metodologia e fonte de cada número; impressão/menção como KPI inicial (GSC/GA4 não dão CTR de IA).
- **Copy pública e cursos:** atualizar para o enquadramento "GEO = SEO sólido + engenharia de evidência/entidade + distribuição legítima"; usar os estudos causais da Ahrefs como prova de rigor (anti-clichê); citar o guia oficial do Google como validação de que indexabilidade segue sendo base.
- **B2A:** llms.txt e Lighthouse "Agentic Browsing" entram na trilha de **prontidão para agentes** (acessibilidade, DOM limpo, formulários rotulados, CLS), separada da trilha de citação em Search.

---

### Apêndice · método de orquestração (reaplicável)
Runner `deep_research_geo_20260619.py`: dispara 3 provedores em threads paralelas, cada um com web/grounding nativo (Perplexity `chat/completions` + `return_citations`; OpenAI `responses` + tool `web_search`; Gemini `generateContent` + `google_search`), `truststore.inject_into_ssl()` para o proxy corporativo. **Aprendizado operacional:** `sonar-deep-research` consome orçamento enorme de `reasoning_tokens` (1ª rodada: 80 buscas, 167k tokens de raciocínio, saída vazia) — forçar saída final com `reasoning_effort: low` e prompt "produza a resposta agora". OpenAI `gpt-5.5` via Responses API + `web_search` foi a fonte mais densa e verificável (IDs arXiv corretos).
