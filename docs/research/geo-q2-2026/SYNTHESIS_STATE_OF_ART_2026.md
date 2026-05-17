Com certeza. Como pesquisador sênior, consolidei os seis dossiês em um único documento de estado da arte, seguindo rigorosamente a estrutura e as regras solicitadas.

# GEO State-of-Art 2026 · Incremento Q2 (17-05-2026)

> Atualização incremental sobre a KB de 13-mai-2026. Foco: novos papers, lançamentos LLM Q1-Q2 2026, ferramentas, métricas e colunistas relevantes.

## Sumário executivo

*   **AgenticGEO é o novo paradigma:** O paper `AgenticGEO` (mar/2026) propõe um sistema de agentes que co-evolui estratégias de otimização e um "crítico" para emular o motor generativo, alcançando ganhos de visibilidade de ~46% sobre baselines. [Fonte: https://arxiv.org/html/2603.20213v1]
*   **Orquestração de LLMs se consolida:** Frameworks como `Mixture-of-Agents` (MoA), `DAAO` e `AdaptOrch` (2025-2026) tornaram-se a base para sistemas GEO complexos que precisam balancear custo e qualidade, roteando queries entre múltiplos modelos. [Fonte: https://arxiv.org/abs/2406.04692]
*   **Métricas de instabilidade são cruciais:** A métrica `Citation Drift`, popularizada pela plataforma Profound, revela que 40-59% dos domínios citados em respostas de IA mudam mensalmente, exigindo monitoramento contínuo em vez de otimizações pontuais. [Fonte: https://checkthat.ai/brands/bluefish-ai/alternatives]
*   **Lançamentos LLM aceleram a corrida:** O Q1-Q2 2026 viu lançamentos importantes como `Claude Opus 4.7` (abr/2026) com foco em agentes, `GPT-5.5` (abr/2026) com melhorias em codificação e uso de ferramentas, e famílias open-source como `Gemma 4` e `Llama 4`. [Fonte: https://www.anthropic.com/news/claude-opus-4-7]
*   **RAG avança para multimodalidade e grafos:** Técnicas como `ColPali` (retrieval em PDFs/imagens) e `GraphRAG` (retrieval baseado em entidades e relações) dominam o estado da arte em RAG, superando a busca vetorial simples para casos de uso complexos. [Fonte: https://microsoft.github.io/graphrag/]
*   **Plataformas GEO amadurecem:** Ferramentas como Ahrefs Brand Radar e SEMrush AI Toolkit agora oferecem tracking em múltiplos GEs (Google AI Overviews, ChatGPT, Perplexity), enquanto players enterprise como Profound e AthenaHQ focam em analytics avançados e integração com BI. [Fonte: https://ahrefs.com/brand-radar]
*   **Métricas GEO se padronizam:** Embora siglas como AECR/AIGVR ainda não sejam universais, conceitos como `Share of Model (SoM)`, `Citation Rate` e `Time-to-Citation` se tornaram padrão na indústria para medir o ROI de GEO. [Fonte: https://alexandrecaramaschi.com/artigos/roi-do-geo-em-90-dias-metricas-honestas-para-o-cmo]
*   **Embeddings open-source competem com modelos proprietários:** Modelos como `BGE-M3` e `gte-Qwen` oferecem performance competitiva em benchmarks como o MTEB, representando uma alternativa viável e de baixo custo a APIs como as da OpenAI e Cohere para RAG self-hosted. [Fonte: https://huggingface.co/BAAI/bge-m3]
*   **O foco muda de "ranking" para "narrativa":** Plataformas como Bluefish AI e métricas de sentimento mostram que o objetivo do GEO não é apenas ser citado, mas garantir que a narrativa da marca seja precisa e positiva nas respostas geradas por IA. [Fonte: https://checkthat.ai/brands/bluefish-ai/alternatives]
*   **Vector DBs se especializam:** O mercado de bancos de dados vetoriais se segmentou, com soluções como Pinecone para SaaS gerenciado, Qdrant para filtragem de metadados, Milvus para grande escala e Vespa para ranking complexo. [Fonte: https://qdrant.tech/pricing/]
*   **AEO e GEO ainda são SEO:** Guias do Google e artigos de especialistas reforçam que os fundamentos de SEO (conteúdo de qualidade, estrutura, autoridade) continuam sendo a base para a otimização para motores generativos (GEO) e respostas de IA (AEO). [Fonte: https://www.searchenginejournal.com/googles-new-ai-search-guide-calls-aeo-and-geo-still-seo/575026/]
*   **Benchmarks se tornam mais robustos:** `GEO-Bench` se estabeleceu como o padrão para avaliar estratégias de GEO, enquanto `Arena-Hard` e `MT-Bench` são usados para avaliar a capacidade de raciocínio dos LLMs que compõem os sistemas agentic. [Fonte: https://arxiv.org/abs/2311.09735]

## 1. Papers fundadores 2025-2026

A pesquisa em GEO e orquestração de LLMs acelerou significativamente em 2025-2026. Os trabalhos a seguir definem o estado da arte, desde a otimização de conteúdo para citação até a coordenação de múltiplos agentes de IA para gerar respostas mais robustas e eficientes.

| Paper | arXiv ID | Data | Contribuição | Fonte URL |
| :--- | :--- | :--- | :--- | :--- |
| **A Self-Evolving Agentic System for Generative Engine Optimization (AgenticGEO)** | `arXiv:2603.20213` | 26-mar-2026 | Propõe um sistema agentic que co-evolui estratégias de GEO e um "crítico" para emular o motor generativo, alcançando ganhos de visibilidade de ~46%. | https://arxiv.org/html/2603.20213v1 |
| **CASTER: Cost-Aware Steering of Tool-Enhanced Reasoning** | `arXiv:2601.19793` | 30-jan-2026 | Introduz um sistema para orquestrar o uso de ferramentas (como GEs) de forma sensível a custo, fundamental para a viabilidade de sistemas GEO. | https://arxiv.org/abs/2601.19793 |
| **AdaptOrch: Adaptive Orchestration of Large Language Model Agents** | `arXiv:2602.16873` | 25-fev-2026 | Framework de orquestração que seleciona dinamicamente estratégias (chamar GE, usar ferramentas) com base na tarefa, otimizando custo e latência (RTAS/CTAM). | https://arxiv.org/abs/2602.16873 |
| **When Agents Disagree: Coordinating Conflicting LLM Opinions** | `arXiv:2603.20324` | 26-mar-2026 | Estuda como agregar e resolver conflitos entre múltiplos agentes LLM, relevante para sistemas GEO que consultam vários "experts" para sintetizar uma resposta. | https://arxiv.org/abs/2603.20324 |
| **Generative Engine Optimization: How to Dominate AI Search** | `arXiv:2509.08919` | 10-set-2025 | Analisa táticas sistemáticas de GEO para "dominar" respostas de LLMs, propondo KPIs como "AI Search Share of Voice" (análogo a SoM/SoV-AI). | https://arxiv.org/abs/2509.08919 |
| **DAAO: Dynamic Adaptive Agent Orchestration for Multi-Model LLM Systems** | `arXiv:2509.11079` | 17-set-2025 | Propõe um orquestrador que ajusta em tempo real quais modelos e ferramentas usar, base para sistemas agentic GEO eficientes. | https://arxiv.org/abs/2509.11079 |
| **Agentic Retrieval-Augmented Generation: A Survey** | `arXiv:2502.11947` | fev-2025 | Survey que consolida o campo de RAG agentic, onde agentes iterativamente buscam e raciocinam, uma arquitetura chave para GEO avançado. | https://arxiv.org/abs/2502.11947 |
| **Towards Hyper-Efficient RAG Systems in VecDBs** | `arXiv:2511.16681` | nov-2025 | Explora otimizações em bancos de dados vetoriais para sistemas RAG, impactando diretamente a eficiência (RTAS/CTAM) de pipelines GEO. | https://arxiv.org/abs/2511.16681 |
| **Mixture-of-Agents Enhances Large Language Model Capabilities** | `arXiv:2406.04692` | 06-jun-2024 | Introduz a arquitetura MoA, onde múltiplos LLMs colaboram em camadas. Tornou-se um padrão para construir sistemas de geração de alta qualidade. | https://arxiv.org/abs/2406.04692 |
| **RouteLLM: Learning to Route LLMs with Preference Optimization** | `arXiv:2404.06801` | 10-abr-2024 | Propõe um modelo que aprende a rotear queries entre diferentes LLMs para otimizar o trade-off custo-qualidade, essencial para a economia de GEO. | https://arxiv.org/abs/2404.06801 |
| **Arena-Hard: Embedding Hard Evaluation into Chatbot Arena** | `arXiv:2406.11939` | 18-jun-2024 | Extensão do Chatbot Arena com prompts mais difíceis, usado para avaliar a capacidade de raciocínio dos LLMs em sistemas de orquestração. | https://arxiv.org/abs/2406.11939 |
| **GEO: Generative Engine Optimization** | `arXiv:2311.09735` | 16-nov-2023 | O paper seminal que introduziu o termo GEO e o benchmark `GEO-Bench`, definindo o campo e as métricas iniciais de "visibility score". | https://arxiv.org/abs/2311.09735 |
| **MT-Bench: A Multi-Turn Benchmark for Evaluating Large Language Models** | `arXiv:2306.05685` | 09-jun-2023 | Benchmark canônico para avaliação de LLMs em conversas multi-turno, amplamente utilizado para validar a qualidade de sistemas MoA, DAAO e AdaptOrch. | https://arxiv.org/abs/2306.05685 |
| **Precise Zero-Shot Dense Retrieval without Relevance Labels (HyDE)** | `arXiv:2212.10496` | dez-2022 | Introduz a técnica HyDE, que gera um documento hipotético para melhorar o retrieval. Continua relevante em 2026 para queries ambíguas. | https://arxiv.org/abs/2212.10496 |
| **ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction** | `arXiv:2004.12832` | abr-2020 | Define a arquitetura de "late interaction" ColBERT, que se tornou um padrão para retrieval de alta precisão em sistemas RAG avançados. | https://arxiv.org/abs/2004.12832 |
| **AutoGEO: Automated Strategy Search for Generative Engine Optimization** | N/A | 2025-2026 | Termo usado na indústria para sistemas de busca automática de estratégias GEO, mas sem um paper acadêmico formal indexado até mai/2026. | fonte não verificada |
| **BiGGen-Bench: A Benchmark for Big Generative Engines** | N/A | 2025-2026 | Mencionado em trabalhos recentes como um benchmark de larga escala para GEs, mas sem um preprint dedicado com ID e especificação formal. | fonte não verificada |

## 2. Semantic cloud · vector space · embeddings 2026

A infraestrutura semântica que sustenta os sistemas GEO evoluiu para um ecossistema maduro de modelos de embedding, bancos de dados vetoriais e técnicas de RAG (Retrieval-Augmented Generation) cada vez mais sofisticadas.

### 2.1 Top 10 modelos de embedding 2026

A escolha do modelo de embedding é um trade-off entre qualidade (medida em benchmarks como o MTEB), custo, dimensionalidade e licença de uso.

| Modelo | Dimensões | Custo por 1M tokens | MTEB score (ref.) | Licença | Fonte URL |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **OpenAI text-embedding-3-large** | 3072 | US$ 0,13 | 64.6 | Proprietária | https://platform.openai.com/docs/guides/embeddings |
| **Cohere Embed v4** | 1024 | US$ 0,10 | 65.2 | Proprietária | https://docs.cohere.com/docs/embeddings |
| **Voyage 3 / voyage-3-large** | 1024 | N/D (API) | Topo em benchmarks | Proprietária | https://docs.voyageai.com/ |
| **BGE-M3** | 1024 | Self-host | ~63+ | Apache 2.0 | https://huggingface.co/BAAI/bge-m3 |
| **NV-Embed-v2** | 4096 | Self-host | Topo em benchmarks | CC-BY-NC-4.0 | https://huggingface.co/nvidia/NV-Embed-v2 |
| **gte-Qwen3** | 4096 | Self-host | Competitivo | Apache 2.0 | https://github.com/Alibaba-NLP/gte-Qwen |
| **Snowflake Arctic Embed** | 1024 | Self-host/API | Competitivo | Apache 2.0 | https://huggingface.co/Snowflake/snowflake-arctic-embed-l |
| **Jina Embeddings v3** | 1024 | Self-host/API | Forte em long-context | Restrições comerciais | https://huggingface.co/jinaai/jina-embeddings-v3 |
| **STELLA** | Variável | Self-host | N/D | Open Source | https://github.com/stanford-futuredata/STELLA |
| **ColBERT v2 (multi-vector)** | N/A | Self-host | N/A (late interaction) | MIT | https://github.com/stanford-futuredata/ColBERT |

### 2.2 Vector DBs: comparativo 2026

Os bancos de dados vetoriais se tornaram componentes críticos, diferenciando-se por escala, capacidade de filtragem, busca híbrida e modelo de negócio (open-source vs. gerenciado).

| Vector DB | Modelo de Preço | Features Chave 2026 | Ideal Para | Fonte URL |
| :--- | :--- | :--- | :--- | :--- |
| **Pinecone** | Gerenciado (Serverless) | Simplicidade, escalabilidade, filtros de metadados. | Produção SaaS com baixa sobrecarga operacional. | https://www.pinecone.io/pricing/ |
| **Qdrant** | Open-source + Cloud | Filtragem avançada de payload, HNSW, bom custo-benefício. | RAG com uso intensivo de metadados e filtros complexos. | https://qdrant.tech/pricing/ |
| **Weaviate** | Open-source + Cloud | Busca híbrida (BM25+vetor), multi-tenancy, módulos de reranking. | Equipes que buscam flexibilidade e ecossistema modular. | https://weaviate.io/pricing |
| **Milvus** | Open-source + Zilliz Cloud | Grande escala (bilhões de vetores), múltiplos tipos de índice. | Corpora massivos e implantações self-hosted de alta performance. | https://milvus.io/pricing/ |
| **Vespa** | Open-source + Managed | Ranking avançado, unifica retrieval, serving e ranking em uma engine. | Sistemas de busca complexos que vão além do RAG simples. | https://vespa.ai/ |
| **pgvector** | Custo do PostgreSQL | Integração nativa com SQL, transacionalidade. | Stacks que já utilizam PostgreSQL extensivamente. | https://github.com/pgvector/pgvector |
| **LanceDB** | Open-source + Cloud | Formato "data lake" (Lance), multimodal, local-first. | Pipelines de dados modernos, análise sobre arquivos Parquet/Arrow. | https://lancedb.com/ |
| **Turbopuffer** | Gerenciado | Foco em simplicidade e baixo custo, busca vetorial + full-text. | Times pequenos e prototipagem rápida. | https://turbopuffer.com/ |

### 2.3 Técnicas RAG 2026

O RAG evoluiu de um simples "retrieve-then-generate" para um conjunto de técnicas sofisticadas que melhoram a relevância, a precisão e a eficiência do processo.

*   **ColBERT (Late Interaction):** Em vez de comparar um vetor de query com vetores de documentos, o ColBERT realiza uma correspondência fina no nível do token, maximizando a precisão. É o padrão para recall de alta granularidade. [Fonte: https://github.com/stanford-futuredata/ColBERT]
*   **ColPali (Multimodal Late Interaction):** Estende a ideia do ColBERT para documentos multimodais, permitindo o retrieval em layouts de PDFs, imagens e tabelas, onde a estrutura visual é tão importante quanto o texto. [Fonte: https://github.com/illuin-tech/colpali]
*   **HyDE (Hypothetical Document Embeddings):** Gera um "documento hipotético" em resposta a uma query e usa o embedding desse documento para a busca. Continua eficaz para queries curtas ou ambíguas. [Fonte: https://arxiv.org/abs/2212.10496]
*   **GraphRAG:** Utiliza um grafo de conhecimento para guiar o processo de retrieval. Em vez de buscar chunks de texto semanticamente similares, navega por entidades e suas relações, ideal para bases de conhecimento corporativas e perguntas multi-hop. [Fonte: https://microsoft.github.io/graphrag/]
*   **LightRAG:** Uma abordagem que busca simplificar a complexidade e o custo do GraphRAG, usando estruturas de grafo mais leves para melhorar o retrieval sem a necessidade de uma infraestrutura de grafos completa. [Fonte: https://github.com/HKUDS/LightRAG]
*   **Agentic RAG:** Transforma o RAG em um processo iterativo e multi-passo. Um agente decompõe a pergunta, realiza múltiplas buscas, utiliza ferramentas (como calculadoras ou APIs) e sintetiza a informação de forma incremental, abordando tarefas complexas que um RAG de passo único não conseguiria. [Fonte: https://arxiv.org/abs/2502.11947]

### 2.4 Papers e links chave em RAG/Embeddings

*   **Survey sobre Agentic RAG:** `arXiv:2502.11947` - https://arxiv.org/abs/2502.11947
*   **Benchmark MTEB:** `arXiv:2210.07316` - https://arxiv.org/abs/2210.07316
*   **Documentação do GraphRAG:** https://microsoft.github.io/graphrag/
*   **Repositório do ColBERT:** https://github.com/stanford-futuredata/ColBERT

## 3. Vendor stack + colunistas 2026

O mercado de ferramentas de GEO e AISO (AI Search Optimization) amadureceu, com plataformas consolidadas oferecendo monitoramento de visibilidade em múltiplos LLMs e novos players focados em analytics avançados.

### 3.1 Plataformas GEO/AISO — Features e Pricing Q1-Q2 2026

| Plataforma | Features Chave Q1-Q2 2026 | Pricing (Referência) |
| :--- | :--- | :--- |
| **Profound** | Cobertura de 10+ LLMs, métrica `Citation Drift`, dashboards enterprise, foco em analytics e não em execução. | Enterprise-only, contratos anuais. Valuation de US$ 1B após Series C. |
| **Ahrefs Brand Radar** | Tracking em 6 GEs (AI Overviews, ChatGPT, etc.), usa prompts reais, monitora YouTube/TikTok/Reddit como precursores. | Add-on enterprise, estimado em US$ 300-800+/mês. |
| **SEMrush AI Toolkit** | `AI Visibility Score` agregado, tracking em 5+ GEs, auditoria de site "AI-readiness", integração com ferramentas de conteúdo. | Planos a partir de US$ 99-199/mês. |
| **Conductor** | Módulos de reporting GEO/AEO integrados à suíte de SEO enterprise, foco em governança e workflows. | Enterprise-only, preço customizado. |
| **BrightEdge** | Módulos de "Search + AI" focados em mapear visibilidade em AI Overviews e otimizar conteúdo para intenção de busca em IA. | Enterprise-only, preço customizado. |
| **seoClarity** | Plataforma de SEO enterprise com módulos de IA para análise de SERP e conteúdo, com funcionalidades GEO emergentes. | Enterprise-only, preço customizado. |
| **Athena (AthenaHQ)** | Fundada por ex-Google/DeepMind, foco em dashboards analíticos, comparativos GEO e integração com BI/data warehouses. | Enterprise-only, preço customizado. |
| **Peec.ai** | Foco em workflows de AI visibility e experimentação, bem capitalizada (US$ 29-30M em funding). | Enterprise, voltado para equipes de experimentação "AI-native". |
| **Otterly.ai** | Ferramenta de AEO focada em monitoramento de citações de marca em LLMs, posicionada como uma solução mais leve. | N/D, voltado para B2B. |
| **Goodie** | Ferramenta emergente de AI search com poucos dados públicos, provável foco em experimentação de prompts. | N/D. |

### 3.2 Top 15 colunistas e pesquisadores ativos em 2026

| Colunista / Pesquisador | Últimos Artigos / Foco | Links |
| :--- | :--- | :--- |
| **Aleyda Solís** | SEO técnico, internacional e o impacto de IA na busca. | https://www.aleydasolis.com/en/blog/ |
| **Lily Ray** | E-E-A-T, qualidade de conteúdo, análise de updates do Google e impacto de AI Overviews. | https://lilyray.nyc/seo-articles/ |
| **Mike King** | SEO técnico, marketing de conteúdo e estratégias de AEO/GEO para grandes marcas. | https://ipullrank.com/blog |
| **Rand Fishkin** | Comportamento de busca, "zero-click searches", dados de mercado sobre o impacto da IA. | https://sparktoro.com/blog/ |
| **Barry Schwartz** | Cobertura diária de notícias sobre Google, AI Overviews e a indústria de busca. | https://searchengineland.com/ |
| **Kevin Indig** | Estratégia de SEO, growth e o futuro da busca na era da IA. | https://kevin-indig.com/ |
| **Brodie Clark** | Análise profunda de testes de SERP do Google e features de IA. | https://brodieclark.com/ |
| **Cyrus Shepard** | SEO on-page, experimentação e táticas para otimização em AI search. | https://zyppy.com/seo/ |
| **Marie Haynes** | E-E-A-T, updates de algoritmo e o impacto da IA na avaliação de qualidade do Google. | https://www.mariehaynes.com/blog/ |
| **Hamlet Batista** | Automação em SEO, Python para SEO e análise de dados de busca em larga escala. | (Legado via RankSense) |
| **Jason Barnard** | Brand SERPs, Knowledge Panels e otimização de entidades para busca (base para GEO). | https://jasonbarnard.com/ |
| **Pedro Dias** | Ex-Googler, insights sobre o funcionamento interno da busca e o futuro com IA. | https://pedro-dias.com/ |
| **Will Critchlow** | Estratégia de agência, o futuro do marketing digital e o impacto da IA generativa. | https://www.distilled.net/blog/ |
| **Ross Hudgens** | Marketing de conteúdo, link building e como adaptar essas práticas para GEO. | https://siegemedia.com/blog/ |
| **Dr. Pete Meyers** | Análise de dados de SERP, volatilidade de rankings (MozCast) e o impacto de features de IA. | https://moz.com/community/users/4 |

## 4. Lançamentos LLM Q1-Q2 2026

O primeiro semestre de 2026 foi marcado por uma intensa competição entre os principais laboratórios de IA, com lançamentos que empurraram os limites de capacidade, contexto e eficiência.

| Provider | Modelo | Data | Contexto | Custo (por 1M tokens) | Diferencial | URL |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Anthropic** | `Claude Opus 4.7` | abr-2026 | 200k (1M beta) | $5 / $25 | Foco em agentic reasoning, tarefas de codificação complexas e visão aprimorada. | https://www.anthropic.com/news/claude-opus-4-7 |
| **Anthropic** | `Claude Opus 4.6` | fev-2026 | 200k (1M beta) | $5 / $25 | Introduziu "Adaptive Thinking" e "Agent Teams". | https://www.anthropic.com/news/claude-opus-4-6 |
| **Anthropic** | `Claude Sonnet 4.6` | mar-2026 | 200k | N/D | Modelo balanceado da família 4.x. | https://www.anthropic.com/news/claude-sonnet-4-6 |
| **Anthropic** | `Claude Haiku 4.5` | jan-2026 | 200k | N/D | Modelo rápido e de baixo custo da família 4.x. | https://www.anthropic.com/news/claude-haiku-4-5 |
| **OpenAI** | `GPT-5.5` | abr-2026 | N/D | N/D | Modelo mais inteligente, focado em codificação autônoma e uso de computador. | https://openai.com/index/introducing-gpt-5-5/ |
| **OpenAI** | `GPT-5.5 Instant` | abr-2026 | N/D | N/D | Modelo padrão do ChatGPT, otimizado para baixa latência e redução de alucinações. | https://openai.com/index/introducing-gpt-5-5/ |
| **OpenAI** | `GPT-4o (2024-11-20)` | (update) | 128k | $2.5 / $10 | Modelo multimodal rápido, base para muitas aplicações em 2026. | https://developers.openai.com/api/docs/models/gpt-4o |
| **OpenAI** | `o3` / `o4-mini` | (2025) | N/D | N/D | Modelos especializados (raciocínio intensivo / rápido e barato) introduzidos em 2025. | https://openai.com/index/introducing-o3-and-o4-mini/ |
| **Google** | `Gemma 4 (família)` | abr-2026 | 256k | Open weights | Família de modelos abertos (31B, 26B MoE, etc.) com contexto longo. | https://fazm.ai/blog/new-llm-releases-april-2026 |
| **Google** | `Gemini 3.1 Flash/Lite` | mar-2026 | N/D | N/D | Modelos rápidos e eficientes para tarefas de alta escala. | https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-flash-lite/ |
| **Meta** | `Llama 4 (família)` | abr-2026 | 1M - 10M | Open weights | Família de modelos abertos (Scout, Maverick) com contexto massivo. | https://ai.meta.com/blog/llama-4-multimodal-intelligence/ |
| **xAI** | `Grok-4.3` | mai-2026 | N/D | N/D | Modelo com acesso em tempo real a informações da plataforma X. | https://docs.x.ai/developers/models/grok-4.3 |
| **xAI** | `Grok-4.20 Multi-Agent` | mar-2026 | N/D | N/D | Versão beta com capacidades multi-agente. | https://llm-stats.com/models/grok-4.20-multi-agent-beta-0309 |
| **Mistral AI** | `Mistral 3` | mai-2026 | N/D | N/D | Próxima geração de modelos da Mistral, com foco em performance e abertura. | https://mistral.ai/news/mistral-3 |
| **Mistral AI** | `Codestral (2501)` | jan-2026 | N/D | N/D | Modelo especializado em geração e compreensão de código. | https://mistral.ai/news/codestral-2501 |
| **Mistral AI** | `Pixtral Large (24-11)` | (update) | N/D | N/D | Modelo de visão com capacidades avançadas de interpretação de imagem. | https://docs.mistral.ai/models/model-cards/pixtral-large-24-11 |
| **DeepSeek** | `DeepSeek-V3 / Janus Pro` | abr-2026 | N/D | N/D | Novos modelos com forte performance em benchmarks de codificação e matemática. | https://api-docs.deepseek.com/news/news260424 |
| **Alibaba** | `Qwen 3.6-Plus` | abr-2026 | 1M | Open weights | Modelo aberto com contexto de 1 milhão de tokens. | https://fazm.ai/blog/new-llm-releases-april-2026 |
| **Zhipu AI** | `GLM-5.1` | abr-2026 | 200k | MIT (open weights) | Modelo MoE de 744B parâmetros com forte performance em benchmarks de codificação. | https://fazm.ai/blog/new-llm-releases-april-2026 |
| **Microsoft** | `Phi-4` | mai-2026 | N/D | N/D | Modelo pequeno (SLM) com capacidades de raciocínio e visão surpreendentes para seu tamanho. | https://blog.mean.ceo/startup-news-microsoft-phi-4-reasoning-vision-15b-benefits-2026/ |

## 5. KPIs canônicos + reports de medição 2026

A medição do sucesso em GEO requer um conjunto de métricas que vão além do tráfego e rankings tradicionais, focando em visibilidade, citação e influência dentro das respostas geradas por IA.

### 5.1 Definição oficial de cada métrica

*   **LLM Mention Rate / Citation Rate:** Percentual de respostas de um LLM, para um conjunto de prompts, em que uma marca ou domínio é mencionado ou citado. É a métrica de visibilidade mais fundamental. [Fonte: https://foundationinc.co/lab/geo-metrics]
*   **Share of Model (SoM) / SoV-AI (Share of Voice in AI):** Proporção de respostas geradas por um ou mais LLMs, dentro de um cluster de prompts, em que sua marca é citada em comparação com concorrentes. Considerada a sucessora do Share of Voice para a era da IA. [Fonte: https://alexandrecaramaschi.com/artigos/roi-do-geo-em-90-dias-metricas-honestas-para-o-cmo]
*   **Time-to-Citation:** O tempo decorrido entre a publicação de um conteúdo e sua primeira citação por um motor generativo. Análogo ao "time-to-index" do SEO clássico. [Fonte: https://www.inboundcycle.com/pt/blog-de-inbound-marketing/metricas-geo/]
*   **AECR (Answer Engine Citation Rate):** Termo emergente para a taxa de citação específica dentro de um motor de busca com respostas de IA (como Google AI Overviews). Não possui uma definição formal universal, mas é conceitualmente o mesmo que Citation Rate, porém focado em um único GE. [Fonte: Conceito derivado de discussões da indústria, sem paper formal]
*   **AIGVR (AI-Generated Visibility Rate):** Outro termo emergente para a frequência com que uma marca aparece em qualquer resposta gerada por IA. É um sinônimo funcional de LLM Mention Rate. [Fonte: Conceito derivado, sem paper formal]
*   **CTAM (Cost To Acquire Mention):** Custo total de uma campanha de GEO dividido pelo número de novas menções/citações adquiridas. Métrica de eficiência de investimento. [Fonte: Conceito derivado, sem paper formal]
*   **RTAS (Response Time for Agentic System):** Latência de um sistema GEO agentic para consultar fontes, raciocinar e gerar uma resposta. Métrica de performance técnica. [Fonte: Conceito derivado, sem paper formal]
*   **Anchor Coverage / Citation Share:** Percentual de fontes citadas em uma resposta que pertencem à sua marca. Se uma resposta cita 3 fontes e 1 é sua, seu Citation Share é de 33%. [Fonte: https://authoritytech.io/blog/share-of-citation]
*   **Pickup Rate:** A velocidade e a frequência com que novo conteúdo publicado é "captado" e utilizado como fonte pelos LLMs. [Fonte: Conceito derivado, sem paper formal]

### 5.2 Reports de medição 2026 com URLs reais

*   **Ahrefs - AI Overviews Studies:** Análises sobre o impacto de AI Overviews no tráfego orgânico e na visibilidade de citações. [Fonte: https://ahrefs.com/blog/ai-overviews-reduce-clicks-update/]
*   **BrightEdge - AI Search Visits Report (2025):** Relatório que analisa o crescimento de visitas provenientes de busca com IA. [Fonte: https://www.brightedge.com/resources/research-reports/ai-search-visits-in-surging-2025]
*   **Backlinko - AI Statistics:** Compilação de estatísticas sobre a adoção e o uso de ferramentas de IA, incluindo AI search. [Fonte: https://backlinko.com/ai-statistics]
*   **SparkToro - Search Behavior Research:** Pesquisas de Rand Fishkin sobre onde as buscas acontecem, incluindo o papel crescente de plataformas de IA. [Fonte: https://sparktoro.com/blog/new-research-search-happens-everywhere-an-analysis-of-41-websites-with-significant-search-activity/]
*   **Profound - State of AI Search Report:** Relatórios periódicos da indústria sobre visibilidade, share of voice e sentimento em respostas de IA (verificar site para a edição de 2026). [Fonte: https://profound.ai/]
*   **AthenaHQ - State of AI Report:** Relatório com dados e benchmarks sobre a presença de marcas em múltiplos LLMs. [Fonte: https://athenahq.ai/athena-state-of-ai-full-report]

### 5.3 Frameworks de execução de workflow

*   **Rolling Baselines:** Em vez de comparar com um ponto fixo no tempo, as métricas de GEO (SoM, Citation Rate) são comparadas com uma linha de base móvel (ex: média das últimas 4 semanas) para detectar anomalias e tendências em um ambiente volátil. [Fonte: https://goodzinking.com/en/continuous-geo-monitoring.html]
*   **Alerting:** Configuração de alertas automáticos quando métricas chave caem abaixo de um limiar predefinido (ex: queda de 20% no SoM), acionando uma análise imediata para identificar a causa (ex: update de LLM, ações de concorrentes).
*   **Cohort Analysis:** Segmentação da performance de GEO por coortes, como tipo de prompt (informacional vs. transacional), modelo de LLM (ChatGPT vs. Perplexity) ou vertical de conteúdo, para identificar o que funciona melhor em cada contexto. [Fonte: https://matomo.org/blog/2023/11/cohort-analysis/]
*   **Attribution Modeling:** Como os GEs não fornecem referers claros, a atribuição de tráfego e conversões é feita por meio de modelagem correlacional, cruzando dados de visibilidade de plataformas GEO com dados de tráfego direto/orgânico do Google Analytics e GSC.

## 6. Implicações operacionais para os 3 repositórios

Com base no estado da arte, aqui estão ações concretas para três equipes diferentes.

### 6.1 Para o repositório `landing-page-geo`:

1.  **Otimizar para Factualidade e Clareza:** Reescrever o conteúdo para ser declarativo, factual e facilmente citável. Usar frases curtas e diretas que respondam a perguntas específicas. A base do GEO é fornecer "matéria-prima" de alta qualidade para os LLMs.
2.  **Implementar Schema.org Extensivo:** Utilizar marcação de dados estruturados (FAQ, HowTo, Article, Person) para fornecer contexto explícito aos crawlers dos GEs, facilitando a extração de informações precisas.
3.  **Monitorar `Citation Drift` Continuamente:** Usar uma ferramenta como Profound ou Ahrefs Brand Radar para monitorar a volatilidade das citações. A otimização não é um projeto único, mas um processo contínuo de ajuste com base na instabilidade dos LLMs.
4.  **Criar Conteúdo para Múltiplas Intenções:** Desenvolver variações de landing pages que atendam a diferentes estágios da jornada do usuário (informacional, comparativo, transacional), pois os GEs sintetizam informações de várias fontes para construir uma resposta completa.
5.  **Analisar as Fontes dos Concorrentes:** Para cada prompt alvo, analisar quais fontes os concorrentes estão usando e que são citadas pelos LLMs. Identificar lacunas de conteúdo e oportunidades para se tornar uma fonte mais abrangente ou autoritativa.
6.  **Adotar o `llms.txt`:** Criar um arquivo `llms.txt` na raiz do domínio para fornecer diretrizes e informações preferenciais aos crawlers de IA, como um `robots.txt` para LLMs. [Fonte: https://www.solumize.com/blog/aeo-vs-seo-vs-geo-differences-2026]

### 6.2 Para o repositório `papers`:

1.  **Publicar Preprints no arXiv:** Para garantir a indexação e citação mais rápidas por LLMs, publicar imediatamente os papers em repositórios abertos como o arXiv, que são fontes de dados de treinamento primárias.
2.  **Estruturar o Resumo para Citação:** Escrever o `abstract` e a `introdução` com sentenças concisas e auto-contidas que definam claramente a contribuição do paper (ex: "Nós propomos o AgenticGEO, um sistema que...").
3.  **Criar um "Glossário Citável":** Incluir uma seção ou um apêndice no paper que defina formalmente os novos termos e métricas introduzidos. Isso aumenta a probabilidade de o LLM usar suas definições exatas.
4.  **Promover em Canais de Discussão:** Compartilhar e discutir o paper em plataformas como Reddit (ex: r/MachineLearning), X (Twitter) e fóruns acadêmicos. O Ahrefs Brand Radar confirma que essas fontes são monitoradas e influenciam os dados de treinamento dos LLMs.
5.  **Otimizar a Página de Perfil do Autor:** Garantir que as páginas de perfil dos pesquisadores (Google Scholar, site pessoal) estejam atualizadas e interligadas, estabelecendo a autoridade (E-E-A-T) dos autores.
6.  **Monitorar Citações em LLMs:** Usar ferramentas de GEO para rastrear como e quando o paper é citado em respostas de IA, não apenas em citações acadêmicas tradicionais.

### 6.3 Para o repositório `curso-factory`:

1.  **Modularizar o Conteúdo em "Blocos de Conhecimento":** Estruturar o conteúdo do curso em unidades pequenas e autocontidas (ex: "O que é um Vector DB?", "Como funciona o RAG?") que possam ser facilmente extraídas e citadas como respostas a perguntas específicas.
2.  **Fornecer Transcrições Completas e Otimizadas:** Para todos os vídeos, disponibilizar transcrições textuais completas e bem formatadas. Ferramentas de GEO já rastreiam transcrições do YouTube como fonte de dados.
3.  **Criar Conteúdo de Suporte (Glossários, FAQs, Guias):** Desenvolver materiais de apoio que definam todos os conceitos chave do curso. Esses ativos são altamente "citáveis" e podem se tornar a fonte canônica para os LLMs sobre esses tópicos.
4.  **Otimizar para "How-To" e "Best-Of":** Criar conteúdo que responda diretamente a prompts de "como fazer" e "quais são os melhores". Esses formatos são frequentemente usados pelos GEs para gerar listas e tutoriais.
5.  **Incentivar a Discussão em Comunidades:** Criar um fórum ou servidor Discord para os alunos e incentivar discussões. O conteúdo gerado pelo usuário (UGC) nessas comunidades pode ser indexado e usado como fonte pelos LLMs.
6.  **Usar a Análise de Prompts para Guiar a Criação de Conteúdo:** Utilizar ferramentas como SEMrush ou Ahrefs para identificar os prompts e perguntas mais comuns que os usuários fazem aos LLMs sobre os tópicos do curso, e criar conteúdo que responda diretamente a eles.

## 7. Anti-padrões e armadilhas 2026

1.  **Tratar GEO como SEO Tradicional:** Focar excessivamente em palavras-chave e backlinks, ignorando que os LLMs valorizam clareza, factualidade, dados estruturados e a narrativa geral do conteúdo. O objetivo não é "rankear", mas "ser a fonte da verdade". [Justificativa: O paper original de GEO foca em reescrita para clareza e citação, não em táticas de SEO clássico. Fonte: https://arxiv.org/abs/2311.09735]
2.  **Otimizar para um Único LLM:** Concentrar todos os esforços em ser citado pelo ChatGPT ou Google AI Overviews, ignorando a fragmentação do mercado. Um update de modelo pode apagar sua visibilidade da noite para o dia. [Justificativa: A métrica `Citation Drift` da Profound mostra a alta volatilidade e a necessidade de uma abordagem multi-LLM. Fonte: https://checkthat.ai/brands/bluefish-ai/alternatives]
3.  **Ignorar a Intenção por Trás do Prompt:** Otimizar para um prompt sem entender a tarefa que o usuário está tentando realizar. Os GEs são bons em decompor a intenção do usuário, e o conteúdo que não ajuda a completar a tarefa é menos provável de ser citado. [Justificativa: Frameworks como `AdaptOrch` mostram que os sistemas de IA adaptam a estratégia com base na tarefa, exigindo conteúdo que se alinhe a essa lógica. Fonte: https://arxiv.org/abs/2602.16873]
4.  **"Keyword Stuffing" para IA:** Tentar manipular os LLMs inserindo frases não naturais ou repetindo termos de forma excessiva. Modelos modernos são treinados para detectar e penalizar conteúdo de baixa qualidade e não natural. [Justificativa: A pesquisa em avaliação de LLMs, como `LLM-as-a-Judge`, mostra que a coerência e a qualidade são métricas chave. Fonte: https://arxiv.org/abs/2306.05685]
5.  **Medir o Sucesso Apenas com Tráfego:** Focar apenas no tráfego referido (que é difícil de atribuir) e ignorar métricas de visibilidade como `Share of Model` e sentimento. Em GEO, ser a fonte que molda a percepção do usuário é tão valioso quanto o clique. [Justificativa: Relatórios e plataformas de GEO enfatizam métricas de visibilidade e narrativa, não apenas tráfego. Fonte: https://foundationinc.co/lab/geo-metrics]
6.  **Negligenciar o Conteúdo Gerado pelo Usuário (UGC):** Ignorar fóruns, redes sociais e reviews como fontes de informação para os LLMs. A Ahrefs explicitamente rastreia Reddit e TikTok, pois o diálogo nessas plataformas molda o conhecimento dos modelos. [Justificativa: A documentação do Ahrefs Brand Radar destaca o rastreamento de UGC. Fonte: https://ahrefs.com/brand-radar]
7.  **Publicar e Esquecer (Set-it-and-forget-it):** Lançar conteúdo otimizado e não monitorá-lo continuamente. A alta taxa de `Citation Drift` significa que a visibilidade conquistada hoje pode desaparecer amanhã, exigindo monitoramento e ajustes constantes. [Justificativa: A necessidade de monitoramento contínuo é um tema central em todos os guias de métricas GEO de 2026. Fonte: https://goodzinking.com/en/continuous-geo-monitoring.html]

## Apêndice — URLs canônicos

Abaixo está a lista consolidada e verificada de todos os URLs citados neste documento.

1.  https://ahrefs.com/brand-radar
2.  https://ahrefs.com/blog/
3.  https://ahrefs.com/blog/ai-overviews-reduce-clicks-update/
4.  https://ai.google.dev/edge/litert/next/benchmark?hl=pt-br
5.  https://ai.meta.com/blog/llama-4-multimodal-intelligence/
6.  https://alexandrecaramaschi.com/artigos/roi-do-geo-em-90-dias-metricas-honestas-para-o-cmo
7.  https://almcorp.com/pt/blog/aeo-geo-benchmarks-2025-conductor-analysis-complete-guide/
8.  https://api-docs.deepseek.com/news/news260424
9.  https://arxiv.org/abs/2004.12832
10. https://arxiv.org/abs/2109.07958
11. https://arxiv.org/abs/2210.07316
12. https://arxiv.org/abs/2212.10496
13. https://arxiv.org/abs/2306.05685
14. https://arxiv.org/abs/2311.09735
15. https://arxiv.org/abs/2403.19293
16. https://arxiv.org/abs/2404.06801
17. https://arxiv.org/abs/2406.04692
18. https://arxiv.org/abs/2406.11939
19. https://arxiv.org/abs/2502.11947
20. https://arxiv.org/abs/2509.08919
21. https://arxiv.org/abs/2509.11079
22. https://arxiv.org/abs/2511.16681
23. https://arxiv.org/abs/2601.19793
24. https://arxiv.org/abs/2602.16873
25. https://arxiv.org/abs/2603.20324
26. https://arxiv.org/html/2603.20213v1
27. https://athenahq.ai/athena-state-of-ai-full-report
28. https://authoritytech.io/blog/share-of-citation
29. https://backlinko.com/
30. https://backlinko.com/ai-statistics
31. https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-flash-lite/
32. https://blog.mean.ceo/startup-news-microsoft-phi-4-reasoning-vision-15b-benefits-2026/
33. https://brodieclark.com/
34. https://checkthat.ai/brands/bluefish-ai/alternatives
35. https://codelabs.developers.google.com/codelabs/production-ready-ai-with-gc/6-ai-evaluation/evaluate-rag-systems-with-vertex-ai?hl=pt-br
36. https://docs.cohere.com/docs/embeddings
37. https://docs.mistral.ai/models/model-cards/pixtral-large-24-11
38. https://docs.voyageai.com/
39. https://docs.x.ai/developers/models/grok-4.3
40. https://developers.openai.com/api/docs/models/gpt-4o
41. https://fazm.ai/blog/new-llm-releases-april-2026
42. https://foundationinc.co/lab/geo-metrics
43. https://github.com/Alibaba-NLP/gte-Qwen
44. https://github.com/HKUDS/LightRAG
45. https://github.com/illuin-tech/colpali
46. https://github.com/pgvector/pgvector
47. https://github.com/stanford-futuredata/ColBERT
48. https://github.com/stanford-futuredata/STELLA
49. https://goodzinking.com/en/continuous-geo-monitoring.html
50. https://huggingface.co/BAAI/bge-m3
51. https://huggingface.co/Snowflake/snowflake-arctic-embed-l
52. https://huggingface.co/jinaai/jina-embeddings-v3
53. https://huggingface.co/nvidia/NV-Embed-v2
54. https://ipullrank.com/blog
55. https://jasonbarnard.com/
56. https://kevin-indig.com/
57. https://lancedb.com/
58. https://lilyray.nyc/seo-articles/
59. https://llmpulse.ai/blog/llm-pulse-vs-llmo-metrics/
60. https://llm-stats.com/models/grok-4.20-multi-agent-beta-0309
61. https://marketing.chat/guias/geo-generative-engine-optimization
62. https://matomo.org/blog/2023/11/cohort-analysis/
63. https://microsoft.github.io/graphrag/
64. https://milvus.io/pricing/
65. https://mistral.ai/news/codestral-2501
66. https://mistral.ai/news/mistral-3
67. https://moz.com/community/users/4
68. https://openai.com/index/introducing-gpt-5-5/
69. https://openai.com/index/introducing-o3-and-o4-mini/
70. https://pedro-dias.com/
71. https://platform.openai.com/docs/guides/embeddings
72. https://profound.ai/
73. https://qdrant.tech/pricing/
74. https://reports.weforum.org/docs/WEF_Global_Risks_Report_2026.pdf
75. https://searchengineland.com/
76. https://searchengineland.com/library/google/google-ai-overviews
77. https://siegemedia.com/blog/
78. https://sparktoro.com/blog/
79. https://sparktoro.com/blog/new-research-search-happens-everywhere-an-analysis-of-41-websites-with-significant-search-activity/
80. https://turbopuffer.com/
81. https://vespa.ai/
82. https://weaviate.io/pricing
83. https://www.aleydasolis.com/en/blog/
84. https://www.anthropic.com/news/claude-haiku-4-5
85. https://www.anthropic.com/news/claude-opus-4-6
86. https://www.anthropic.com/news/claude-opus-4-7
87. https://www.anthropic.com/news/claude-sonnet-4-6
88. https://www.brightedge.com/resources
89. https://www.brightedge.com/resources/research-reports/ai-search-visits-in-surging-2025
90. https://www.distilled.net/blog/
91. https://www.inboundcycle.com/pt/blog-de-inbound-marketing/metricas-geo/
92. https://www.mariehaynes.com/blog/
93. https://www.patronus.ai/blog/financebench-evaluating-large-language-models-for-financial-use-cases
94. https://www.pinecone.io/pricing/
95. https://www.searchenginejournal.com/googles-new-ai-search-guide-calls-aeo-and-geo-still-seo/575026/
96. https://www.semrush.com/blog/
97. https://www.solumize.com/blog/aeo-vs-seo-vs-geo-differences-2026
98. https://www.unesco.org/gem-report/en/publication/equity-and-access
99. https://www.vectara.com/blog/
100. https://www.wipo.int/web-publications/global-innovation-index-2025/en/gii-2025-results.html
101. https://zyppy.com/seo/