# Wave Junho 2026 · Incremento canônico GEO/SEO/AEO/Vector

> **Data de corte:** 07 de junho de 2026.
> **Status:** delta entre 03-jun (último incremento — `GEO_KNOWLEDGE_BASE_2026_V3.md`, `GEO_REDACAO_CHECKLIST_2026.md`, `GEO_EARNED_MEDIA_2026.md`, `STATE_OF_ART_2026_06_INCREMENT.md`) e 07-jun.
> **NÃO substitui** nenhum documento canônico anterior. **Complementa** com: o framework operacional de 5 camadas de medição de GEO, a hierarquia de KPIs com metodologia formal de medição, o delta de vendor stack (Profound, Peec, Ahrefs, Semrush, Scrunch/Sitecore, Conductor, AthenaHQ, Microsoft Clarity), 5 papers acadêmicos novos de GEO/AEO, ~25 papers novos da camada semântica/vetorial (chunking, dense retrieval, reranking, semantic entropy, citation absorption), e a seção de aplicação por repositório.
> **Como aplicar:** ler **antes** de qualquer decisão sobre dashboard de medição, definição de KPI de cliente, escolha de ferramenta de AI visibility, briefing de sub-agent, prompt de coleta, design de schema/llms.txt, ou auditoria GEO em portfolio Brasil GEO.
> **Fonte:** orchestrator 5 LLMs (4 deep-research Perplexity `sonar-deep-research` + 1 board 5 LLMs) executado em 07-jun-2026, raw em [`raw/`](raw/). Dois arXiv IDs de 2026 verificados via WebFetch (EcoGEO `2605.12887`, What Gets Cited `2605.25517`).

---

## 0. Sumário executivo (TL;DR)

O delta de junho não traz um novo modelo ou um novo "Google I/O". Traz **maturação de disciplina**: GEO deixou de ser "será que aparecemos no ChatGPT?" e virou uma função operacional medível, com framework de camadas defensável diante de CFO, hierarquia de KPIs com metodologia formal, vendor stack em consolidação (com a primeira aquisição relevante e o primeiro artigo de imprensa de ceticismo) e uma base acadêmica que agora separa **seleção** de **absorção** de citação e trata o motor como **agente de navegação**, não como rankeador de páginas.

| Evento / achado | Data | Impacto canônico |
|---|---|---|
| Framework de 5 camadas de medição de GEO consolidado pela indústria | 2025-2026 | Roadmap de maturidade: Captura de canal → Logs/crawlers → SOV + Interrogação estruturada → Pipeline influenciado por IA → Difference-in-differences. É o esqueleto de dashboard defensável diante de CFO. |
| Sitecore adquire a Scrunch (GEO/AEO) por ~US$ 225M | jun/2026 | Primeira aquisição relevante de uma startup pure-play de GEO por um DXP enterprise. AXP (Agent Experience Platform) vira camada do Sitecore. Confirma que GEO é categoria de M&A, não feature. |
| Conductor lança AgentStack para AEO | abr/2026 | Suite enterprise: apps LLM-nativos (ChatGPT/Claude/Copilot) + servidor MCP + agentes AEO turnkey sem prompt engineering. |
| Profound Index (leaderboard público) + Ask Profound + Profound Agents | nov/2025→2026 | Benchmark público de AI Visibility sobre 400M+ conversas reais, 12 indústrias, semanal. "Workflows viram Agents". |
| Peec AI: Series A de US$ 21M; ARR dobrou para ~US$ 10M; lançamento de Actions | mai/2026 | Actions agrupa fontes em clusters semânticos e sugere onde criar conteúdo/ganhar mídia. Berlim virou polo de GEO tooling. |
| Microsoft Clarity adiciona painel **Citations** | 2026 | Métricas formais grátis: Share of Authority, Queries Cited, Query Volume e **Citation Rate** (Queries Cited / Query Volume). |
| Ahrefs Brand Radar: "Found in" vs "Cited in" + estudo de citações em AIO | abr/2026 | Só ~38% das URLs citadas em AI Overviews vêm do top-10 orgânico — evidência dura de **query fan-out**. |
| Semrush AI Visibility Toolkit a US$ 99/mês + módulo Perception (sentimento) | 2026 | Brand Performance soma 100% de SOV por categoria; ChatGPT ponderado por volume de busca do tópico. |
| Artigo Digiday: ceticismo do mercado com ferramentas caras de AI Visibility | 05-jun-2026 | Primeiro sinal de imprensa apontando resultados inconsistentes entre ferramentas. Maturidade traz cobrança por rigor. |
| Paper "What Gets Cited: Competitive GEO" (arXiv:2605.25517) | 25-mai-2026 | 252 mil experimentos de RAG pareado isolam fatores-gatekeeper de citação em 6 LLMs. |
| Paper "EcoGEO" (arXiv:2605.12887) | 13-mai-2026 | Otimizar páginas isoladas é insuficiente: o motor é agente de navegação. Otimiza-se a **trajetória de evidências**. |
| Paper "From Citation Selection to Citation Absorption" (arXiv:2604.25707) — dataset detalhado | abr/2026 | dataset `geo-citation-lab`: 602 prompts, 72 features. ChatGPT cita **menos** fontes porém com **influência maior** por página; Perplexity/Google citam mais com influência distribuída. |
| ~25 papers novos de chunking/dense retrieval/reranking/semantic entropy (arXiv 25xx-26xx) | 2025-2026 | A camada técnica que explica **por que** estrutura semântica gera citação. Ver §5. |

### Sete premissas operacionais consequentes (mudam decisões a partir de 07-jun-2026)

1. **Medição de GEO sem o framework de 5 camadas é anedota.** "Perguntei ao ChatGPT e a marca apareceu" não é dado — a saída do LLM é estocástica. A medição séria exige conjuntos estáveis de prompts, N execuções por prompt e **séries temporais**, organizadas nas 5 camadas (§1.2). **Aplicação:** todo dashboard de cliente Brasil GEO, o `/roadmap` (landing-page-geo) e o prompt portfolio (papers) seguem a estrutura de 5 camadas.
2. **A métrica-rainha é relativa, não absoluta.** Share of Voice / Share of Model só faz sentido contra um conjunto de concorrentes e um benchmark de categoria. Contagem absoluta de menções é métrica de vaidade. **Aplicação:** todo relatório de cliente traz 3 linhas de base — marca, 3 concorrentes, benchmark de categoria.
3. **Por plataforma, não agregado.** AI Overviews e AI Mode citam as mesmas URLs em só ~13,7% dos casos; Perplexity/Copilot incluem links externos em >77% das respostas, ChatGPT em ~31%. Uma métrica agregada esconde a realidade. **Aplicação:** coleta e reporting segmentados por motor (ChatGPT, Gemini/AIO, AI Mode, Perplexity, Copilot).
4. **Ser citado ≠ ser absorvido.** O paper `2604.25707` prova que seleção (entrar na lista de fontes) e absorção (influenciar o texto final) são fenômenos distintos e mensuráveis. Otimizar só para "aparecer na lista" deixa valor na mesa. **Aplicação:** o KPI canônico passa a distinguir Citation Selection Rate de Citation Absorption Rate (já previsto no schema do repo papers).
5. **O motor é um agente de navegação, não um rankeador de páginas.** EcoGEO (`2605.12887`) mostra que a unidade de otimização migra da página para o **ecossistema de evidências** e a **trajetória** que o agente percorre. **Aplicação:** auditorias passam a mapear clusters de páginas interligadas e a presença em fontes de terceiros que o agente visita, não só a página-alvo.
6. **A estrutura semântica do documento é a alavanca técnica de citação.** Os ~25 papers de §5 convergem: chunking dependente de estrutura (headings/seções), densidade de evidência extraível (definições, números, passos, tabelas), self-containment e alinhamento semântico com o prompt determinam recuperabilidade e absorção. **Aplicação:** a rubrica de redação (curso-factory `GEO_REDACAO_CHECKLIST_2026.md`) e os prompts de redação ganham fundamento técnico verificável, não só empírico.
7. **O mercado de tooling entrou na fase de ceticismo.** O artigo Digiday (05-jun) e a alta variabilidade apontada pela SparkToro exigem cautela: nenhuma ferramenta mede o funil completo, resultados divergem entre fornecedores. **Aplicação:** todo pitch Brasil GEO posiciona medição como **triangulação** (GSC + analytics + logs + ≥2 ferramentas cross-engine + interrogação própria), nunca como número único de uma ferramenta.

---

## 1. Frameworks de execução operacional de GEO

### 1.1 O loop agêntico (OBSERVAR → DIAGNOSTICAR → AGIR → MEDIR)

A síntese do board de 5 LLMs converge num ponto: a consultoria de GEO competitiva em 2026 **não opera em pipeline linear trimestral**, mas num **loop agêntico** que itera semanalmente. A frequência de iteração é o diferencial competitivo — velocidade de feedback supera sofisticação de plano.

```
OBSERVAR     → o que os LLMs dizem da marca hoje (multi-modelo, multi-prompt, N execuções)
   ↓
DIAGNOSTICAR → por que dizem isso (qual fonte foi recuperada, qual gap de entidade/citação)
   ↓
AGIR         → publicar/editar/estruturar conteúdo, construir entidade, conquistar citação
   ↓
MEDIR        → mudou citação? sentimento? share of voice? absorção?
   ↓ (volta ao topo, cadência semanal)
```

Dois workstreams precisam ser separados explicitamente, porque são jogos técnicos diferentes:
- **GEO de entidade** — fazer o modelo *entender* quem é a marca (Knowledge Graph, Wikipedia/Wikidata, consistência de NAP, `sameAs`, páginas canônicas de entidade).
- **GEO de citação** — fazer o modelo *recuperar e citar* o conteúdo (estrutura semântica, densidade de evidência, earned media, chunkability).

Tendência emergente (LlamaIndex/board): **agentes sintéticos de teste**. Antes de publicar, rodar um RAG local com personas em IA ("CFO buscando software") contra o conteúdo do cliente para verificar se ele é recuperado frente aos concorrentes **no espaço vetorial** — teste de recuperabilidade contínuo como gate de publicação.

### 1.2 O framework de 5 camadas de medição (defensável diante de CFO)

O framework mais influente de 2025-2026 para **medir** GEO de forma defensável organiza a medição em camadas, das mais operacionais às mais estratégicas. Nenhuma camada isolada prova ROI; em conjunto, conectam visibilidade em IA a demanda e receita. É um **roadmap de maturidade**: comece pelas camadas 1-2, avance para 3a-3b, integre RevOps na 4 e só então tente a 5.

| Camada | Nome | O que mede | Como instrumentar |
|---|---|---|---|
| **1** | Captura de canal e atribuição | Sessões, conversões e receita vindas explicitamente de ferramentas de IA | Reagrupar canais no GA4 para `chatgpt.com`, `chat.openai.com`, `perplexity.ai`, `gemini.google.com`, `copilot.microsoft.com`, `claude.ai` + dimensões de user agent |
| **2** | Logs de servidor e sinais de rastreamento | Se/como o conteúdo está sendo coletado para indexação/treino | Análise semanal de fetchers, indexers e training crawlers de IA nos URLs comerciais |
| **3a** | Share of Voice em respostas generativas | Proporção de respostas em que a marca aparece, em conjuntos estáveis de prompts, ao longo do tempo | Ferramentas de mercado ou amostragem via API; série temporal por motor |
| **3b** | Interrogação estruturada | Acurácia factual, alinhamento com ICP, atribuição de fontes | Conjunto-padrão de prompts (ICP, proposta de valor, forças/fraquezas, casos de uso, comparações) aplicado regularmente a 4-5 modelos |
| **4** | Geração de demanda e pipeline | Pipeline e receita influenciados por IA | Campos em formulários/scripts comerciais: "como descobriu a empresa?" (ChatGPT/Perplexity/Gemini/Claude/Copilot) + prompt/tópico associado |
| **5** | Análise de portfólio | Impacto causal aproximado | Difference-in-differences entre clientes com níveis distintos de investimento em GEO, controlando vertical, tráfego inicial, busca de marca |

Métricas que sobem ao dashboard executivo consolidado: SOV e presença ao longo do tempo; acurácia de interrogação; sessões/conversões de canais de IA; relação ajustada entre SOV e busca de marca; % de pipeline influenciado por IA; resultado dos benchmarks de portfólio.

### 1.3 Disciplina de performance management (evitar o pântano de métricas)

GEO se apoia em frameworks de gestão já maduros — não reinventar a roda:
- **Regra dos 9 KPIs.** Pesquisa sobre 20 mil+ planos estratégicos: scorecards com **9 a 11 medidas** no nível executivo superam em **8,5×** dashboards inflados com 60+ indicadores. Aplicar a GEO: o board do cliente vê ≤11 métricas; o resto é drill-down operacional.
- **O problema não é KPI vs OKR, é dono.** ~75% dos responsáveis por KPIs nunca registram um único update. Toda métrica de GEO precisa de dono e cadência.
- **Camadas de dashboard:** operacional (muda diariamente, investiga causa-raiz) ≠ tático ≠ estratégico (board).
- **Integração RevOps:** GEO é subconjunto especializado de marketing/conteúdo cujo sucesso precisa falar a língua do RevOps — pipeline influenciado por IA, CAC de canais de IA, LTV de clientes originados em IA, impacto em NRR. Single source of truth, definições comuns.

### 1.4 Cadência de reporting canônica

- **Diária:** interrogação estruturada automatizada nos principais LLMs (acurácia de entidade, tempo até primeira menção, contenção de alucinação de marca < 5%).
- **Semanal:** painel operacional — Share of Model, taxa de citação por plataforma, SOV vs concorrentes, monitoramento da meta de alucinação.
- **Mensal:** auditoria de qualidade on-page (GEO-16), análise do ecossistema de evidências (trajetória), conciliação de pipeline/receita influenciados (RevOps).
- **Semestral:** análise de impacto econômico (camada 5, difference-in-differences).

---

## 2. Camadas de KPI e metodologia formal de medição

### 2.1 Os quatro eixos canônicos

A convergência de fornecedores (LLM Pulse, Semrush, Microsoft Clarity, Moz, BrightEdge, Spotlight, Peec) estabelece quatro eixos:

1. **Citation share / Citation frequency** — quantas vezes um domínio/URL é citado como fonte, em recorte temporal, por plataforma e por tag de prompt. Proxy de autoridade e "extraibilidade". Tipicamente **ponderado por posição** (citações nos slots 1-3 pesam mais).
2. **Cobertura de prompts (prompt coverage)** — de todo o universo de perguntas/intenções relevantes, em quantas a marca aparece. Exige construir universos de prompts sintéticos organizados por tag (descoberta, comparação, implementação, problemas).
3. **Share of Voice (AI SOV)** — % de menções da marca vs concorrentes, num universo de prompts e plataformas. **Sempre relativa.** Métrica-rainha porque é estatística e comparativa.
4. **Sentimento / framing** — *como* o modelo descreve a marca (favorável/neutro/crítico), com identificação de drivers (suporte, preço, onboarding). Camada qualitativa sobre a quantitativa.

### 2.2 Definições formais (o que cada vendor padronizou)

- **Microsoft Clarity — painel Citations** (gratuito, novo em 2026):
  - **Queries Cited** = nº de consultas em que o domínio recebeu ≥1 citação em respostas de IA.
  - **Query Volume** = nº total de consultas em que o domínio era elegível para o grounding.
  - **Citation Rate** = Queries Cited / Query Volume — métrica formal de cobertura/conversão de elegibilidade em citação.
  - **Share of Authority** = citações do domínio / citações de todos os domínios no subconjunto de consultas de grounding.
- **LLM Pulse** — citation frequency com ponderação de posição; tags de prompt para cobertura por tema; granularidade dupla domínio vs URL. Dado canônico: **AIO e AI Mode citam as mesmas URLs em só ~13,7% dos casos**; correlatos de citação: estrutura, clareza, autoridade (backlinks → 5× mais provável), frescor (< 12 meses).
- **Semrush AI Visibility Toolkit / Enterprise AIO** — AI Share of Voice combina nº de menções + posição na resposta; em Brand Performance, todas as marcas da categoria somam 100%; para ChatGPT, pondera pelo volume de busca do tópico. Módulo **Perception** para sentimento + **Key Sentiment Drivers**.
- **Citation Selection Rate (CSR) vs Citation Absorption Rate (CAR)** — do paper `2604.25707`: seleção = entrar na lista de fontes; absorção = influenciar o texto final. São métricas-alvo distintas (ver §4.3 e §5).
- **Taxa de links externos por plataforma** (calibra pesos): Perplexity e Copilot > 77% das respostas com links externos; ChatGPT ~31%.

### 2.3 Os três pilares de qualquer pipeline de medição

1. Coleta sistemática multi-plataforma (texto completo + lista de citações + ordem + plataforma + prompt), respeitando que o comportamento de citação varia por motor.
2. Extração estruturada de citações, menções e sinais de grounding (domínio vs URL).
3. Modelos de NLP/LLM para classificar, agrupar e ponderar (sentimento via DeBERTa/RoBERTa/FinBERT-class; NLI para coerência/contradição como camada de veracidade).

---

## 3. Ecossistema de ferramentas — delta jun/2026

Segmentação funcional: de um lado, pure-plays nascidos para **monitorar** AI Visibility e orientar GEO (Profound, Peec, Otterly, AthenaHQ, Scrunch); de outro, extensões de suites de SEO/marketing que incorporam AI Visibility a um sistema de registro mais amplo (Ahrefs Brand Radar, Semrush AI Visibility Toolkit, Conductor AgentStack). Convergência geral: rastrear prompts em ChatGPT/AIO/AI Mode/Perplexity/Gemini, medir frequência de menção, citação de domínio/URL e posição.

| Ferramenta | Delta / lançamento (2026) | Diferencial | Fonte |
|---|---|---|---|
| **Profound** | Profound Index (leaderboard público, 400M+ conversas, 12 indústrias, semanal); **Ask Profound** (consulta dados em linguagem natural); **Profound Agents** ("Workflows viram Agents", Agent Assistant por voz/texto) | Maior dataset público de AI Visibility por conversas reais; camada de automação por agentes | tryprofound.com/blog/introducing-profound-index, /profound-2026, /workflows-are-now-agents-january-release-roundup |
| **Peec AI** | **Series A US$ 21M**; ARR dobrou para ~US$ 10M (TechCrunch 23-mai); recurso **Actions** | Actions agrupa fontes em clusters semânticos e sugere onde criar conteúdo / ganhar mídia; ~US$ 100/mês; blog de KPIs canônico | peec.ai/blog/introducing-actions, /how-to-measure-ai-search-visibility-and-revenue-the-kpis-that-actually-matter; techcrunch.com/2026/05/23/peec-... |
| **Ahrefs Brand Radar** | Decomposição **"Found in"** (páginas lidas) vs **"Cited in"** (páginas citadas); posição média de citação por página; API; update abr/2026 | Integra citações de IA ao Site Explorer/Keywords Explorer/GSC. Estudo: só ~38% das citações em AIO vêm do top-10 orgânico (query fan-out) | ahrefs.com/blog/ai-overview-citations-top-10/, /new-features/ |
| **Semrush AI Visibility Toolkit** | US$ 99/mês (sem trial), análise global/regional, módulo **Perception** (sentimento + Key Sentiment Drivers) | AI SOV ponderado por posição e volume de busca; Brand Performance soma 100% por categoria | semrush.com/kb/1493-ai-visibility-toolkit, /blog/ai-visibility/, /blog/how-to-measure-ai-share-of-voice/ |
| **Scrunch AI** | **Adquirida pela Sitecore por ~US$ 225M (jun/2026)** | Agent Experience Platform (AXP): "versão paralela do site" otimizada para agentes, integrada ao DXP da Sitecore | prnewswire.com/.../sitecore-acquires-scrunch-...302790214.html; adweek.com/media/sitecore-snaps-up-geo-startup-scrunch-for-225m/; cmswire.com/.../sitecore-acquires-scrunch... |
| **Conductor** | **AgentStack** (abr/2026) para AEO | Apps LLM-nativos (ChatGPT/Claude/Copilot) + infra dev (APIs + servidor MCP) + agentes AEO turnkey sem prompt engineering | cmswire.com/digital-experience/conductor-launches-agentstack-for-aeo/ |
| **AthenaHQ** | Relatório **State of AI Search 2026** | Aponta quedas de 30-50% de tráfego orgânico desde respostas diretas; preço por créditos (caro para PME) | athenahq.ai/athena-state-of-ai-full-report; radarkit.ai/blog/athenahq-ai-review/ |
| **Otterly.AI** | Fluxo 3 passos (add prompts → gerar relatório → acompanhar semanal) Google/ChatGPT/Perplexity; estudo de citação no YouTube; Gartner Cool Vendor 2025; G2 #10 2026 | Acessível, rápido, foco em monitoramento contínuo | otterly.ai/case-studies, /blog/youtube-ai-citation-study-2026/ |
| **Microsoft Clarity** | Painel **Citations** (grátis) | Share of Authority, Queries Cited, Query Volume, Citation Rate | clarity.microsoft.com/blog/understanding-your-influence-ai-citations/ |
| **BrightEdge / Moz** | BrightEdge AI Catalyst (estudo AIO 1 ano); Moz AI Mode citations | Benchmarks de presença/citação em AIO e AI Mode | brightedge.com/resources/weekly-ai-search-insights/...; moz.com/blog/ai-mode-citations |

**Sinal de mercado (Digiday, 05-jun-2026):** executivos de agência citam Profound, Peec AI e Ahrefs Brand Radar como as mais úteis na prática, mas o artigo registra **ceticismo** com preços altos e **resultados inconsistentes** entre ferramentas. A única coisa consensualmente útil é "ver com que frequência a marca aparece em diferentes tipos de consulta". Leitura canônica: medição de GEO ainda é **triangulação**, não número único. (digiday.com/marketing/marketers-question-expensive-ai-visibility-tools-as-inconsistent-results-fuel-skepticism/)

---

## 4. Papers acadêmicos novos — GEO / AEO (2025-2026)

> IDs marcados com ✓ foram verificados via WebFetch em 07-jun-2026. Os demais vêm do pool de citações Perplexity e devem ser confirmados na ingestão.

### 4.1 Generative Engine Optimization: How to Dominate AI Search — arXiv:2509.08919 (Chen et al., cs.IR, 2025)
Marco fundador (associado à "pesquisa de Princeton em GEO"). Compara AI Search vs Google em experimentos controlados. Achados canônicos: **viés a favor de earned media** sobre brand media; **big brand bias** (concentração de citações em domínios de altíssima autoridade, mais intensa que no Google); formaliza **taxa de citação** e **share of model**; recomenda "machine scannability" e justificabilidade. Já citado no cânone; aqui reforçado como base do share of model.

### 4.2 AI Answer Engine Citation Behavior: An Empirical Analysis of the GEO-16 Framework — arXiv:2509.10762 (cs.AI, 2025)
Introduz o **GEO-16**: 16 pilares de auditoria de página → escore por pilar → **GEO score G** contínuo (0-1). Método: 70 prompts industriais → 3 motores (Brave, Google AIO, Perplexity) → 1.702 citações → 1.100 URLs únicas auditadas. Achado: qualidade on-page é forte preditor de citação **independente da autoridade de domínio**. Pilares destacados: **Metadata & Freshness**, **Semantic HTML**, **Structured Data** (JSON-LD Article/TechArticle/FAQPage com `datePublished`/`dateModified`/`author`/`breadcrumb`). Framework **aberto e reprodutível** — ideal como rubrica de auditoria.

### 4.3 What Gets Cited: Competitive GEO in AI Answer Engines — arXiv:2605.25517 ✓ (Vishwakarma, Kumar, Jamidar, 25-mai-2026)
**252 mil experimentos de RAG pareado** sobre 6 LLMs para isolar, em condição quase laboratorial, que características fazem um modelo citar uma fonte em vez de outra. Identifica **fatores-gatekeeper** (recência, presença de preço, match estrito de tópico) que praticamente anulam a chance de citação quando violados. É a evidência mais forte de que GEO competitivo se decide por fatores editoriais objetivos.

### 4.4 EcoGEO: Trajectory-Aware Evidence Ecosystems for Web-Enabled LLM Search Agents — arXiv:2605.12887 ✓ (Ye, Mao, Guan, Tian, 13-mai-2026)
Otimizar páginas isoladas é insuficiente quando o motor é um **agente de navegação** que executa múltiplas consultas e constrói a resposta a partir de um **ecossistema de evidências**. Propõe otimização de **trajetória**: coordenar múltiplas páginas interligadas para moldar quais o agente visita e em que ordem. Muda a unidade de análise de página → ecossistema.

### 4.5 GEO-Bench: Benchmarking Ranking Manipulation in Generative Engines (2026 — arXiv ID a confirmar na ingestão)
Sistematiza ataques de manipulação de ranking (caixa-preta e gradiente) e estratégias *white-hat*, num protocolo unificado sobre rankeador aberto baseado em Llama-3.1-8B-Instruct. Relevante para o eixo "anti-padrão / detecção" e para distinguir otimização legítima de manipulação.

### 4.6 GEO–GEU (formulação de utilidade)
"What Generative Search Engines Like and How to Optimize Web Content for Them" (família AutoGEO) introduz o **GEU score** (Generative Engine Utility) como contrapeso ao GEO score: maximizar visibilidade **sem degradar** a utilidade da resposta. Princípio de tensão já canônico (V3); aqui reforçado como par GEO/GEU formal.

> Guia de mercado (GEO Guide 2026): citar fontes autoritativas + estatísticas + citações de especialistas → +30-40% de visibilidade em respostas de IA. SparkToro alerta para **alta variabilidade** das recomendações de marca por sistemas de IA — interpretar qualquer métrica de visibilidade como instável.

---

## 5. Camada semântica / espaço vetorial / embeddings / retrieval

A pergunta "por que estrutura semântica gera citação?" agora tem base técnica. ~25 papers de 2025-2026 mapeiam o pipeline RAG (Indexador/chunking → Recuperação densa → Reranking/seleção → Geração → Avaliação/incerteza). É a fundação de **recuperabilidade** e **citabilidade**.

> IDs abaixo vêm do pool de citações Perplexity (tabela explícita título→ID). Confirmar na ingestão (arXiv `abs/<ID>`).

### 5.1 Chunking e segmentação (como o documento é fatiado determina o que é recuperado)
- **Hierarchical Text Segmentation Chunking** (2507.09935) — árvore de segmentos (parágrafo/seção/subseção) + clustering semântico; recuperação em múltiplos níveis. Ganhos em NarrativeQA/QuALITY/QASPER.
- **SemRAG** (2507.21110) — chunking semântico por similaridade de cosseno entre sentenças + knowledge graph; recuperação em 2 camadas (vetor → entidades/relações no KG).
- **A Systematic Investigation of Document Chunking Strategies** (2603.06976) — avalia **36 estratégias**; achado: chunking **dependente da estrutura** (títulos/seções) dá o melhor trade-off cobertura×redundância; não há método dominante único.
- **Optimizing Chunking-Method Selection for RAG** (2603.25333); **Query-Adaptive Semantic Chunking / QASC** (2605.22834); **MultiDocFusion** (2604.12352, hierárquico multimodal).

### 5.2 Dense retrieval e representações
- **LREM — Large Reasoning Embedding Models** (2510.14321) — dense retrieval com raciocínio explícito.
- **Multi-layer Representations for Dense Passage Retrieval** (2509.23861); **ReinPool** (2601.07125, pooling RL multi-vector); **HiRAG** (2503.10150); **RAG vs GraphRAG** (2502.11371); **T-RAG** sobre tabelas (2504.01346); **S-Path-RAG** (2603.23512, KG-RAG multi-hop).
- **On the Theoretical Limitations of Embedding-Based Retrieval** (2508.21038) — limites teóricos do que um único vetor representa (já sinalizado na wave de maio; reforçado).
- **Pooling and Semantic Shift** (2603.21437) — geometria de embeddings em textos longos.

### 5.3 Reranking e seleção de evidências
- **BAR-RAG** (2602.03689, reranking boundary-aware); **SetR** (2507.06838, seleção set-wise em vez de ranquear); **Scaling Laws for Cross-Encoder Reranking** (2603.04816); **jina-reranker-v3** (2509.25085, multilíngue); **Comparative Analysis of Neural Retriever–Reranker Pipelines** (2602.22219).

### 5.4 Incerteza, semantic entropy e avaliação
- **Semantic Energy** (2508.14496) — detecção de alucinação via energia semântica.
- **Redefining Retrieval Evaluation in the Era of LLMs** (2510.21440, métrica UDCG focada em RAG); **VB-Score** (2604.19281); **RIKER** (2601.08847); **PosIR** (2601.08363, viés de posição em IR).

### 5.5 Embeddings de marca/entidade e a ponte com GEO
- **Semantic Structure in Large Language Model Embeddings** (2508.10003) — marcas/entidades são representadas em espaços vetoriais estruturados; consistência de nomenclatura e densidade de menções reduzem ambiguidade e aumentam recuperabilidade.
- **NER Retriever: Zero-Shot Named Entity Retrieval with Type-Aware Embeddings** (2509.04011) — recuperação de entidade nomeada com embeddings cientes de tipo.
- **Characterizing Web Search in the Age of Generative AI** (2510.11560) — motores generativos e busca orgânica selecionam fontes diferentes; generativos recorrem mais a domínios de menor popularidade SEO.
- **The Rise of AI Search** (2602.13415) — implicações de mercado; Google ~90%+ do tráfego de busca de IA em 2025.
- **Citation Selection → Citation Absorption** (2604.25707) — dataset `geo-citation-lab` (602 prompts, 72 features). Páginas longas, bem estruturadas, semanticamente alinhadas e densas em evidência extraível (definições, fatos, comparações, passos) têm influência muito maior. ChatGPT: menos fontes, maior influência por página; Perplexity/Google: mais fontes, influência distribuída. Ambiente de teste: **SAGEO Arena** (isola efeito de otimização de documento do efeito do modelo).
- **DED — Discovery with Exact Definition** (fórum OpenAI): ser citado não garante definição correta absorvida; o gap entre descoberta, citação e definição exata gera "Dark Revenue" — e é mensurável/intervencionável.

**Implicação prática unificada (a "física" da citabilidade):** conteúdo que vence é **chunkável por estrutura** (headings/seções autossuficientes), **denso em evidência extraível**, **terminologicamente consistente** (acopla com embeddings de entidade), **alinhado semanticamente ao prompt** e **interligado em ecossistema** (trajetória do agente). Isto fundamenta tecnicamente a rubrica de redação empírica já no cânone.

---

## 6. Convergência SEO + GEO (estado em jun/2026)

- **Google Search Console — Gen AI performance reports** (anúncio 03-jun-2026): primeiras impressões oficiais do Google em recursos generativos (AI Overviews/AI Mode/Discover) — impressões, NÃO cliques (institucionaliza zero-clique). Rollout gradual, Reino Unido primeiro. Acompanha controles de opt-out de conteúdo em respostas de IA. (developers.google.com/search/blog/2026/06/gen-ai-performance-reports) — ver doc dedicado `landing-page-geo/docs/research/geo-2026-06-medicao-ai-visibility.md`. **Cautela:** o relatório cobre só o ecossistema Google e nem sempre separa por tipo de recurso; combinar com ferramentas cross-engine e interrogação própria.
- **GEO estende o SEO, não o substitui.** A base técnica do SEO (rastreabilidade, indexação, performance, dados estruturados, relevância temática) permanece pré-requisito; GEO adiciona a disputa por **ser fonte** na resposta. Não bloquear snippets se a meta é aparecer em IA (`nosnippet`/`data-nosnippet`/`max-snippet` limitam o uso).
- **De palavras-chave para entidades.** Entity SEO vira centro: nome consistente, domínio canônico, `sameAs` confiáveis, página "Sobre" clara, autoria identificável, presença em grafos (Wikipedia/Wikidata). "Authority Flywheel" = pesquisa original + PR digital + menções independentes.
- **Zero-clique consolidado:** AI Overviews chegam a ~83% de zero-clique; AI Mode, estudos apontam até ~93%. ChatGPT Search ~250-500M consultas/semana; Perplexity ~50M/semana. Market share de chatbots migrando para multipolar (ChatGPT de ~87% em 2025 para ~64,5-68% em jan/2026; Gemini ~18-21,5%). CTR do ChatGPT Search ~0,84-1,3% vs ~29% do Google — tráfego direto de IA é baixo; o valor é **citação/lembrança**, não clique.

---

## 7. Aplicação por repositório

### 7.1 landing-page-geo (alexandrecaramaschi.com / Brasil GEO)

1. **`/roadmap` e dashboard de métricas:** estruturar o painel ao redor das **5 camadas** (§1.2). Hoje o repo já coleta de 11 fontes (GA4/GSC/etc.); adicionar explicitamente (a) reagrupamento de canais de IA no GA4 (camada 1), (b) leitura semanal de crawlers de IA nos logs (camada 2), (c) série temporal de SOV por plataforma (camada 3a) e (d) interrogação estruturada agendada (camada 3b). Expor ≤11 KPIs no nível board (regra dos 9 KPIs).
2. **Artigo HBR-grade novo:** "O framework de 5 camadas para medir GEO sem enganar o CFO" — captura a janela de primeira citação do tema. Conceitos 24/25/49/50.
3. **Artigo HBR-grade novo:** "Por que ser citado não é ser absorvido (e como medir os dois)" — traduz `2604.25707` (CSR vs CAR) e DED/Dark Revenue para CMO brasileiro.
4. **Auditoria de cliente:** adotar GEO-16 (`2509.10762`) como rubrica aberta de auditoria on-page; mapear ecossistema/trajetória (EcoGEO) e não só a página-alvo.
5. **Schema/JSON-LD:** reforçar `datePublished`/`dateModified`/`author`/`breadcrumb` (pilares GEO-16). Frescor < 12 meses como sinal de citação.
6. **Medição honesta no pitch:** posicionar como triangulação (GSC Gen AI report + GA4 + logs + ≥2 ferramentas cross-engine + interrogação própria) — não número único (Digiday/SparkToro).

### 7.2 papers (pesquisa empírica multi-vertical)

1. **Schema SQLite:** confirmar/popular os campos `citation_selection_rate` e `citation_absorption_rate` (já previstos na wave de maio) com o detalhamento metodológico do dataset `geo-citation-lab` (602 prompts, 72 features) como referência de desenho. Considerar campo de **influência por página** (ChatGPT concentra, Perplexity/Google distribui).
2. **Prompt portfolio (camada 3b):** alinhar o conjunto-padrão de interrogação estruturada do framework de 5 camadas (ICP, proposta de valor, forças/fraquezas, casos de uso, comparações) ao roster v2 de 127 entidades. Medir por plataforma, não agregado (AIO×AI Mode = 13,7% de overlap de URL).
3. **Novos papers para ingestão (Related Work / Discussion do Paper 5):** `2605.25517` (What Gets Cited, 252k experimentos, fatores-gatekeeper), `2605.12887` (EcoGEO, trajetória), `2509.10762` (GEO-16/GEO score G), GEO-Bench (ID a confirmar). Tagueá-los contra os Conceitos 11/13/15/21/24/25/30 e contra CSR/CAR.
4. **Hipóteses testáveis:** os fatores-gatekeeper de `2605.25517` (recência, preço, match de tópico) viram hipóteses falsificáveis no dataset longitudinal brasileiro — não há replicação PT-BR. Pré-registro OSF deve declarar quais conceitos/fatores testa.
5. **Camada semântica:** o módulo de coleta pode incorporar, como variável de controle, métricas de estrutura on-page (GEO-16) para correlacionar com taxa de citação observada — ponte direta entre §5 e o desenho estatístico.

### 7.3 curso-factory (fábrica de cursos EAD GEO-first)

1. **Módulo novo "Como medir GEO":** o framework de 5 camadas vira a espinha de uma trilha (1 aula por camada) + aula de "Regra dos 9 KPIs e a língua do RevOps". Conceitos GEO-core 11/12/24/25.
2. **Módulo novo "O ecossistema de ferramentas de AI Visibility 2026":** Profound/Peec/Ahrefs/Semrush/Scrunch-Sitecore/Conductor/Clarity — o que cada uma habilita em qual camada; aula de "medição é triangulação, não número único" (caso Digiday).
3. **Fundamento técnico da rubrica de redação:** `GEO_REDACAO_CHECKLIST_2026.md` ganha base verificável de §5 — chunkability (chunking por estrutura, `2603.06976`), densidade de evidência extraível e citation absorption (`2604.25707`), self-containment e alinhamento semântico. O `content_checker.py` já conta Cite Sources/Statistics/Quotation/answer capsule; documentar que isto otimiza **absorção**, não só seleção.
4. **Prompts do pipeline:** `writer.py` (GPT) e `reviewer.py` (Claude) podem citar os fatores-gatekeeper de `2605.25517` (recência, número específico, match estrito de tópico) como checklist; `classify.md` mantém tags `geo-2026`/`citation-ready`/`aeo`/`aso`/`b2a` e adiciona `citation-absorption`/`entity-embedding`.
5. **Aula avançada "O motor é um agente, não um rankeador":** EcoGEO + agentes sintéticos de teste (RAG local com personas) como prática — aula de laboratório.

---

## 8. Anti-padrões e cautelas reforçados (jun/2026)

- **Número único de uma ferramenta** como verdade de visibilidade — proibido. Triangular (Digiday/SparkToro: resultados inconsistentes, alta variabilidade).
- **Métrica absoluta de menções** sem benchmark competitivo — vaidade. SOV/Share of Model são relativos por definição.
- **Métrica agregada cross-plataforma** — esconde a realidade (AIO×AI Mode 13,7% de overlap). Sempre por motor.
- **Otimizar só "aparecer na lista de fontes"** — seleção sem absorção deixa valor na mesa (`2604.25707`).
- **Otimizar só a página-alvo** — insuficiente para agentes de navegação (EcoGEO). Pensar ecossistema/trajetória.
- **Alucinação de arXiv ID** — LLMs inventam IDs com alta frequência. Nesta wave, EcoGEO e What Gets Cited foram verificados via WebFetch; GEO-Bench e os IDs de §5 ficam marcados "confirmar na ingestão". Validar `arxiv.org/abs/<ID>` antes de canonizar.
- **GhostCite** (já no V3): 14-95% de citações fabricadas em LLM — fonte verificável virou diferencial competitivo de GEO, não só higiene.
- **llms.txt como talismã / schema como silver bullet** — permanecem anti-padrões (cânone anterior).

---

## 9. Pool de URLs verificáveis (consolidado)

**Papers GEO/AEO (arXiv):**
- https://arxiv.org/abs/2509.08919 — GEO: How to Dominate AI Search
- https://arxiv.org/abs/2509.10762 — GEO-16 / GEO score G
- https://arxiv.org/abs/2605.25517 — What Gets Cited (✓ verificado)
- https://arxiv.org/abs/2605.12887 — EcoGEO (✓ verificado)
- https://arxiv.org/abs/2604.25707 — Citation Selection → Absorption

**Papers semântica/vetorial/RAG (arXiv — confirmar na ingestão):**
- https://arxiv.org/abs/2507.09935 · 2507.21110 · 2603.06976 · 2603.25333 · 2605.22834 · 2604.12352 (chunking)
- https://arxiv.org/abs/2510.14321 · 2509.23861 · 2601.07125 · 2503.10150 · 2502.11371 · 2504.01346 · 2603.23512 · 2508.21038 · 2603.21437 (dense retrieval/representações)
- https://arxiv.org/abs/2602.03689 · 2507.06838 · 2603.04816 · 2509.25085 · 2602.22219 (reranking/seleção)
- https://arxiv.org/abs/2508.14496 · 2510.21440 · 2604.19281 · 2601.08847 · 2601.08363 (incerteza/avaliação)
- https://arxiv.org/abs/2508.10003 · 2509.04011 · 2510.11560 · 2602.13415 (embeddings de entidade / ecossistema)

**Vendor / indústria:**
- https://www.tryprofound.com/blog/introducing-profound-index · /profound-2026 · /workflows-are-now-agents-january-release-roundup · /ahrefs-brand-radar-review
- https://peec.ai/blog/introducing-actions · /how-to-measure-ai-search-visibility-and-revenue-the-kpis-that-actually-matter · https://techcrunch.com/2026/05/23/peec-one-of-berlins-rising-startups-more-than-doubled-annualized-revenue-in-months-to-10m-sources-say/
- https://ahrefs.com/blog/ai-overview-citations-top-10/ · https://ahrefs.com/blog/new-features/
- https://www.semrush.com/kb/1493-ai-visibility-toolkit · https://www.semrush.com/blog/ai-visibility/ · https://www.semrush.com/blog/how-to-measure-ai-share-of-voice/ · https://www.semrush.com/blog/best-ai-visibility-tools/
- https://www.prnewswire.com/news-releases/sitecore-acquires-scrunch-to-help-brands-influence-discovery-and-buying-decisions-in-the-ai-search-era-302790214.html · https://www.adweek.com/media/sitecore-snaps-up-geo-startup-scrunch-for-225m/ · https://www.cmswire.com/digital-experience/sitecore-acquires-scrunch-to-boost-ai-search-visibility/
- https://www.cmswire.com/digital-experience/conductor-launches-agentstack-for-aeo/
- https://athenahq.ai/athena-state-of-ai-full-report · https://athenahq.ai/resources/generative-search-optimization-next-era-of-seo
- https://otterly.ai/case-studies · https://otterly.ai/blog/youtube-ai-citation-study-2026/
- https://clarity.microsoft.com/blog/understanding-your-influence-ai-citations/
- https://moz.com/blog/ai-mode-citations · https://www.brightedge.com/resources/weekly-ai-search-insights/ai-overviews-one-year-presence-size-citing
- https://llmpulse.ai/blog/glossary/citation-frequency/ · https://llmpulse.ai/blog/glossary/share-of-voice/ · https://www.get-spotlight.com/features/citation-tracking/ · https://www.wordstream.com/blog/llm-tracking
- https://digiday.com/marketing/marketers-question-expensive-ai-visibility-tools-as-inconsistent-results-fuel-skepticism/
- https://discoveredlabs.com/blog/peec-ai-review-best-for-ai-visibility-monitoring-use-cases-limits-alternatives · https://radarkit.ai/blog/athenahq-ai-review/

**SEO/Google:**
- https://developers.google.com/search/blog/2026/06/gen-ai-performance-reports
- https://blog.google/products-and-platforms/products/search/search-io-2026/
- https://blog.google/innovation-and-ai/technology/ai/google-io-2026-all-our-announcements/

> **Próxima atualização:** trimestral (próxima janela ~set/2026) ou ao primeiro evento estrutural (novo core update, novo modelo default, nova aquisição relevante). Citar `§X.Y` desta wave ao tomar decisões.
