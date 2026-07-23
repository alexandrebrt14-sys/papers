# Digest arXiv — Generative Engine Optimization (GEO)
Data da coleta: 22/07/2026 · Fonte: export.arxiv.org (API Atom) · Todos os números citados constam dos abstracts originais. XMLs brutos: geo_q1.xml, geo_q2.xml, geo_q3.xml (mesmo diretório).

## Lista-mestre

| ID arXiv | Data | Título |
|---|---|---|
| 2607.14035 | 2026-07-15 | Optimizing Visibility in Generative Engines: A Critical Survey of GEO (2023-2026) |
| 2607.14197 | 2026-07-15 | How AI LLM Engines Shape the Global Conflict Information Environment |
| 2607.12056 | 2026-07-13 | Designing Agent-Ready Websites for AI Web Agents |
| 2606.27736 | 2026-06-26 | ToE: Hierarchical and Explainable Claim Verification (contra GEO poisoning) |
| 2606.20065 | 2026-06-18 | GEO at Scale: Measuring Brand Visibility Across AI Search Engines |
| 2606.17443 | 2026-06-16 | Incumbent Advantage: Brand Bias in LLM Recommendation Systems |
| 2606.16344 | 2026-06-15 | Whose hotel does the AI recommend? (auditoria de algoritmo) |
| 2606.28356 | 2026-06-08 | SafeGEO: GEO Risks in Recommendation Agents |
| 2606.12439 | 2026-05-18 | Position: GEO Creates Underexamined Risks (governança) |
| 2606.04362 | 2026-06-03 | Disentangling AEO from Platform Growth (experimento natural glasp.co) |
| 2605.29107 | 2026-05-27 | GEO-Bench: Benchmarking Ranking Manipulation in GEO |
| 2605.25517 | 2026-05-25 | What Gets Cited: Competitive GEO in AI Answer Engines |
| 2605.21948 | 2026-05-21 | SCI-Defense: Defending Manipulation Attacks from GEO |
| 2605.12887 | 2026-05-13 | EcoGEO: Trajectory-Aware Evidence Ecosystems for LLM Search Agents |
| 2605.09314 | 2026-05-10 | How LLMs Are Persuaded: A Few Attention Heads, Rerouted |
| 2604.27790 | 2026-04-30 | How Generative AI Disrupts Search (Google, Gemini, AI Overviews) |
| 2604.25707 | 2026-04-28 | From Citation Selection to Citation Absorption (framework de medição) |
| 2604.19516 | 2026-04-21 | From Experience to Skill: Multi-Agent GEO (MAGEO) |
| 2604.19113 | 2026-04-21 | Think Before Writing: Feature-Level Multi-Objective Optimization (FeatGEO) |
| 2604.07585 | 2026-04-08 | Don't Measure Once: Measuring Visibility in AI Search (GEO) |
| 2604.03656 | 2026-04-04 | Beyond Retrieval: Confidence Decay and Deterministic Agentic Platforms |
| 2603.29979 | 2026-03-31 | Structural Feature Engineering for GEO (GEO-SFE) |
| 2603.09296 | 2026-03-10 | Diagnosing and Repairing Citation Failures in GEO (AgentGEO) |
| 2603.12282 | 2026-03-05 | Algorithmic Trust and Compliance: UK iGaming em Generative Search |
| 2603.20213 | 2026-03-02 | AgenticGEO: A Self-Evolving Agentic System for GEO |
| 2602.12187 | 2026-02-12 | SAGEO Arena: Realistic Environment for Search-Augmented GEO |
| 2602.02961 | 2026-02-03 | GEO: A VLM and Agent Framework for Pinterest Acquisition Growth |
| 2601.13938 | 2026-01-20 | IF-GEO: Conflict-Aware Instruction Fusion for Multi-Query GEO |
| 2601.12263 | 2026-01-18 | Multimodal GEO: Rank Manipulation for VLM Rankers (MGEO) |
| 2601.00912 | 2026-01-01 | The Discovery Gap: Product Hunt Startups em LLM Discovery |
| 2601.00869 | 2025-12-30 | Cultural Encoding in LLMs: The Existence Gap |
| 2601.16858 | 2026-01-23 | Navigating the Shift: Web Search vs Generative AI Response Generation |

## (a) Medição e KPIs

### 2607.14035 — Critical Survey of GEO (2023-2026) ⭐
Revisa 45 estudos (nov/2023–jul/2026). GEO não é tarefa única de ranking: é pipeline estocástico e parcialmente observável — ativação de busca, crawling/indexação, retrieval, reranking e alocação de contexto, citação, proeminência, absorção factual, fidelidade e comportamento do usuário. Os ganhos do paper fundacional de GEO são condicionais à fonte já estar no contexto — não provam descobribilidade orgânica nem efeito durável. Mais reprodutíveis: relevância temática e posição no contexto; heurísticas genéricas transferem mal; competição erode ganhos; reescritas voltadas a citação podem prejudicar retrieval. Auditorias comerciais: baixa sobreposição de fontes, alta variabilidade run-a-run, lacunas de fidelidade. Contribui modelo formal multiestágio, vetor de visibilidade (descobribilidade / citação / absorção / resultado econômico), hierarquia de evidência e protocolo reprodutível (medições repetidas, paráfrases, controles, validação humana, interferência multi-ator). Nenhuma técnica revisada demonstra efeito causal estável, longitudinal e cross-plataforma sobre descobribilidade orgânica.

### 2606.20065 — GEO at Scale (Ranqo) ⭐
100K+ respostas, 100+ marcas, mar–mai/2026. Escada de estatura de marca: globais 73% de presença nas respostas relevantes; mid-market 44%; nicho 11% (~30 pp por degrau). ~78% das citações vão a sites corporativos; entre não corporativos, YouTube > Reddit > mídia editorial > Wikipedia. Formato com mais alavancagem: listicle "best-of" ranqueado (~21% das citações). Sentimento flipa ~6,7x mais que a menção. Propõe 7 protocolos v1.1 para causalidade.

### 2604.25707 — Citation Selection → Citation Absorption ⭐
Dois estágios: seleção de citação e absorção (a página contribui com linguagem/evidência/estrutura para a resposta). Dataset geo-citation-lab: 602 prompts em ChatGPT, AIO/Gemini e Perplexity; 21.143 citações válidas; 72 features. Perplexity e Google citam mais fontes; ChatGPT cita menos mas com influência por citação maior. Páginas de alta influência: mais longas, estruturadas, semanticamente alinhadas, ricas em evidência extraível (definições, fatos numéricos, comparações, passos). Contar citações é KPI insuficiente — medir absorção.

### 2604.07585 — Don't Measure Once ⭐
A natureza probabilística da busca por IA quebra o paradigma da medição pontual. Respostas variam entre execuções, prompts e tempo. Medições repetidas; visibilidade como distribuição com variância reportada. Screenshot único não é evidência.

### 2606.04362 — Disentangling AEO from Platform Growth
Experimento natural em glasp.co (jan/2026): páginas tratadas com AEO cresceram 5,7x em referrals do ChatGPT, mas o controle on-domain cresceu 3,5x — o crescimento bruto é dominado pelo crescimento da plataforma. Efeito estimado 1,82x (IC 95% 1,31–2,54, p=0,001 HAC; 2,27x filtrado por engajamento), mas placebo permutacional p=0,16 — sugestivo, não conclusivo. Cases de mercado superestimam efeito causal; sempre descontar tailwind com controle on-domain.

### 2602.12187 — SAGEO Arena ⭐
Ambiente realista cobrindo retrieval, reranking e geração com informação estrutural (schema). Abordagens GEO existentes largamente impraticáveis em condições realistas; frequentemente degradam retrieval/reranking. Informação estrutural mitiga; otimização deve ser por estágio do pipeline.

## (b) Técnicas de otimização

### 2605.25517 — What Gets Cited ⭐
252.000 trials, 6 LLMs, 18 fatores, pareado e contrabalanceado. Maiores drivers de primeira citação: relevância temática e posição na lista; preço explícito e timestamp recente ajudam consistentemente; completude e sinais de confiança dão ganhos menores; formatação pura tem pouco impacto. Protocolo e checklist públicos; piloto na Sprinklr.

### 2603.29979 — GEO-SFE ⭐
Estrutura em 3 níveis: macro (arquitetura do documento), meso (chunking), micro (ênfase visual). Modelos por arquitetura de motor. Em 6 motores: +17,3% taxa de citação, +18,5% qualidade subjetiva.

### 2604.19113 — FeatGEO (Think Before Writing) ⭐
Otimização multiobjetivo no nível de features (estruturais, de conteúdo, linguísticas), LLM materializa a configuração. Supera baselines token-level no GEO-Bench em 3 motores. Citação é mais influenciada por propriedades documento-nível que por edições lexicais; configurações generalizam entre modelos.

### 2601.13938 — IF-GEO
Otimizar um documento para múltiplas queries conflitantes: mineração de preferências de queries latentes + Blueprint Global de Revisão via fusão de instruções consciente de conflitos; métricas de estabilidade sensíveis a risco. Otimizar para o portfólio de intenções, não para um prompt.

### 2607.12056 — Agent-Ready Websites
3 dimensões: interpretabilidade, executabilidade, confiabilidade de decisão. Experimento: mesmo site baseline vs agent-ready, 5 tarefas, 3 browser-agents (GPT-4.1, Gemini-2.5 Flash, Grok-4 Fast), 300 execuções: 134/150 PASS vs 74/150 (89,3% vs 49,3%); PARTIAL 43→3; passos médios 9,31→6,49. GEO expande de "ser citado" para "ser operável por agente".

### 2603.12282 — Algorithmic Trust (UK iGaming)
Viés esmagador por earned media sobre conteúdo próprio em vertical regulado; visibilidade depende de "Algorithmic Trust", não densidade de keyword. Em verticais regulados, GEO é majoritariamente earned media estruturado.

## (c) Sistemas agênticos

### 2603.20213 — AgenticGEO ⭐
GEO como problema de controle condicionado ao conteúdo. MAP-Elites para evoluir estratégias + Co-Evolving Critic (surrogate barato do motor). SOTA e transferibilidade sobre 14 baselines em 3 datasets. Código: github.com/AIcling/agentic_geo.

### 2604.19516 — MAGEO ⭐
Multiagente: planejamento, edição, avaliação consciente de fidelidade; padrões validados destilados em skills reutilizáveis por motor. Twin Branch Evaluation Protocol (atribuição causal), métrica DSV-CF, benchmark MSME-GEO-Bench. Modelagem de preferência por motor e reuso de estratégia são centrais.

### 2603.09296 — AgentGEO (diagnóstico) ⭐
Taxonomia de modos de falha de citação por estágio do pipeline; agente diagnostica e aplica reparos direcionados; +40% relativo na taxa de citação modificando só 5% do conteúdo (vs 25% dos baselines). Otimização genérica pode prejudicar long-tail; alguns documentos não são salváveis por otimização.

### 2604.03656 — Beyond Retrieval (DAH) ⭐
Semantic Entropy Drift (decaimento de confiança), Isomorphic Attribution Regression (valor de otimização em black-box com penalidade de alucinação), Deterministic Agent Handoff — LLM só roteia intenção, agente proprietário responde. Validação com EasyNote (Yishu Technology): alucinação próxima de zero em tarefa vertical. Futuro pós-citação: "ser o agente roteado", não "ser citado".

### 2602.02961 — Pinterest (produção)
VLMs fine-tunados para prever queries reais + agentes minerando tendências; Collection Pages semanticamente coerentes via embeddings multimodais; interlinking consciente de autoridade (VLM + two-tower ANN, bilhões de imagens). +20% tráfego orgânico; contribuiu para crescimento de MAU de vários milhões.

### 2605.12887 — EcoGEO / TRACE
Da página ao ecossistema: página de entrada voltada ao agente + páginas de suporte com terminologia compartilhada, links internos e atributos consistentes. Supera baselines page-level no OPR-Bench; mais crawls iniciais e navegação interna. Usa produto fictício — também é alerta de manipulação.

## (d) Riscos, manipulação e governança

### 2606.12439 — Position: riscos e governança
Três riscos: influência concentrada; influência comercial não divulgada; pontos cegos academia-indústria. Pede contestabilidade, disclosure de alta precisão, auditoria black-box, métricas de persistência de exposição. Antecipar disclosure é vantagem.

### 2605.29107 — GEO-Bench (manipulação)
Unifica ataques black-box de prompt, white-box de gradiente e 10 estratégias C-SEO em 5 datasets (ranker Llama-3.1-8B). Eficácia × furtividade trocam entre si; reescrita black-box iguala/supera gradiente com texto mais fluente; modelo de acesso não prediz força.

### 2606.28356 — SafeGEO
22 variantes de ataque em 600 casos: ataques GEO aumentam em até 83,2% a promoção de produtos defeituosos; defesas simples reduzem em até 39,2% mas não restauram.

### 2605.21948 — SCI-Defense
Defesa PPL + Semantic Integrity Scoring (autoridade, propositividade, comparativos, alegações temporais) + inter-candidatos. Precision=1,000, FPR=0,000; Recall 1,000/0,952/0,830 (String/Reasoning/Review). Sinais punidos = exatamente o que parte do mercado GEO usa.

### 2605.09314 — How LLMs Are Persuaded
Poucas attention heads intermediárias decidem; persuasão = salto latente discreto; feature rank-one de roteamento de evidência controla a rota. Circuito estreito e monitorável — GEO de "keywords persuasivas" tem prazo de validade.

### Outros
- 2606.27736 (ToE): verificação de claims em árvore de evidência; +4 a 24 pp sobre baselines, maiores em inputs envenenados.
- 2601.12263 (MGEO): ataque multimodal (imagem + sufixos) a rankers VLM; manipulação maior que unimodal.
- 2607.14197 (conflitos): 5.460 respostas, 28 conflitos, 5 engines; quanto mais fino o registro, mais invenção/desatribuição; captura estado-partidária incipiente — "GEO information warfare".

## (e) Estudos empíricos de mercado

### 2604.27790 — How Generative AI Disrupts Search ⭐
11.500 queries reais: AIO em 51,5% das queries; fontes divergem fortemente entre Google/AIO/Gemini (Jaccard <0,2); busca tradicional favorece sites institucionais, motores generativos favorecem conteúdo de propriedade do Google; sites que bloqueiam o crawler de IA do Google são significativamente menos recuperados em AIO; AIOs menos consistentes entre execuções e menos robustos a edições mínimas.

### 2606.17443 — Incumbent Advantage
Skincare, 3 LLMs: monopólio condicional de marcas conhecidas (100% com specs idênticas) desaparece com +0,1 estrela do concorrente; tom de autoridade (incl. alegações clínicas fabricadas) vale +0,17 de rating; dilema social — todas usando a mesma estratégia, payoff cai de +0,802 para +0,007; não participantes recebem zero.

### 2606.16344 — Auditoria de hotéis
12 modelos, conjoint randomizado: rating máximo +31,6 pp na seleção; preço alto −30,0; sobrepeso de eco-certificação; posição na lista desloca causalmente (~US$ 12/diária); explicações dos modelos não refletem os pesos reais.

### 2601.00912 — The Discovery Gap
112 startups Product Hunt, 2.240 queries (gpt-4o-mini, sonar): reconhecimento por nome 99,4%/94,3%; descoberta 3,32%/8,29% (gap 30:1 no ChatGPT). Scores GEO não correlacionam com descoberta; no Perplexity o que prediz é SEO tradicional — referring domains (r=+0,319), ranking PH (r=−0,286), Reddit/comunidade (r=+0,395). Fundação SEO primeiro.

### 2601.00869 — Existence Gap
1.909 queries, 6 LLMs, 30 marcas: LLMs chineses mencionam marcas +30,6 pp vs internacionais (88,9% vs 58,3%); geografia dos dados de treino dirige o efeito. "Existence Gap", Data Moat Framework, "Algorithmic Omnipresence".

### 2601.16858 — Navigating the Shift
Divergências Google vs IA generativa: domínios, tipologia (earned/owned/social), intenção, frescor. Dois ecossistemas com mecânicas distintas — planejar fontes separadamente.

## Síntese executiva

1. **Medição antes de otimização**: medições repetidas, visibilidade como distribuição, controle on-domain, separação descobribilidade/citação/absorção/resultado (2607.14035, 2604.07585, 2606.04362).
2. **Alavancas com melhor evidência**: relevância temática e posição no contexto; estrutura em 3 níveis (+17,3%); densidade de evidência extraível; listicles de terceiros e YouTube; preço explícito e data recente.
3. **O que a evidência NÃO sustenta**: efeito causal estável sobre descobribilidade orgânica; correlação de scores GEO com descoberta real; formatação pura.
4. **Fronteira agêntica**: diagnóstico antes de reescrita (+40% mudando 5%); estratégias por motor com validação causal; crítico surrogate; roteamento de intenção para agentes (DAH).
5. **Risco e detecção**: motores filtram autoridade fabricada e comparativos/temporais (SCI-Defense); persuasão é circuito monitorável; agenda de disclosure chegando.
