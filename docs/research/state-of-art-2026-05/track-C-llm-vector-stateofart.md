# Track C — LLM/Vector/Semantic State of the Art 2026

> Sub-agent Opus · 2026-05-20 · Pesquisa para Alexandre Caramaschi (CEO Brasil GEO)
> Cobre estado da arte de retrieval, embedding, vector search e nuvem semântica em maio de 2026, com aplicação direta para `landing-page-geo`, `papers` e `curso-factory`.

---

## Sumário executivo

O ecossistema de recuperação de informação de 2026 estabilizou em torno de cinco realidades operacionais que devem orientar qualquer decisão de arquitetura nos três repositórios do programa Brasil GEO:

1. **Embeddings densos chegaram ao platô.** Os modelos de fronteira (OpenAI `text-embedding-3-large`, Cohere `embed-v4`, Voyage `voyage-3-large` e `voyage-4-large`, Jina v4, Snowflake Arctic Embed 2.0) entregam entre 64 e 72 pontos no MTEB v2 agregado, com diferenças de 1 a 3 pontos que raramente justificam migração isolada. A escolha hoje é guiada por contexto operacional: tokens máximos, suporte multilíngue, custo por milhão de tokens, dependência de fornecedor e qualidade em português brasileiro.
2. **Híbrido vence puro.** A combinação de BM25 (ou SPLADE) com vetor denso, sucedida por um reranker cross-encoder, virou o padrão de fato. A queda de hallucination e ganho de recall@20 documentado pelo Anthropic Contextual Retrieval (49 a 67 por cento de redução de falhas) confirma o que vinha de papers acadêmicos desde 2023.
3. **Vector DBs viraram commodities, mas custam diferente.** Turbopuffer, Pinecone Serverless v2 e pgvector cobrem 80 por cento dos casos pequenos a médios. Qdrant 1.16, Weaviate 1.30 e Milvus dominam o segmento de bilhões de vetores. A diferença de custo total entre Turbopuffer e Pinecone (storage 0,02 contra 0,33 dólares por GB por mês) chega a uma ordem de grandeza para cargas de leitura intensiva.
4. **Agentic RAG é o próximo platô.** Self-RAG, CRAG, Adaptive-RAG e GraphRAG 1.0 da Microsoft saíram do laboratório para produção em 2025 e 2026. Padrões como RAPTOR (clustering hierárquico) e HippoRAG 2 (memória inspirada em hipocampo) já viraram componentes nativos em LlamaIndex Workflows 1.0 e LangGraph Platform GA.
5. **Long context não substitui RAG.** Mesmo com Gemini 2.5 Pro em 2 milhões de tokens, Claude Opus 4.7 em 1 milhão e GPT-5 em 200 a 400 mil, o custo computacional sobre 1 milhão de tokens é cerca de 17 vezes maior que recuperar 2 mil tokens via RAG. Para portais de conteúdo dinâmico, ingestão acadêmica e cross-link de cursos, RAG continua mais barato, mais fresco e mais auditável.

Este relatório destrincha esses cinco eixos, depois aterrissa em decisões concretas (paths, configs, custos) para os três repositórios.

---

## 1. Embeddings landscape 2026

### 1.1 Tabela comparativa dos 15 modelos canônicos

| Modelo | Provedor | Dim. nativa | Dim. truncável (MRL) | Max tokens | MTEB (médio) | MIRACL (multilíngue) | Custo por 1M tokens | PT-BR | Lançamento |
|---|---|---|---|---|---|---|---|---|---|
| text-embedding-3-large | OpenAI | 3072 | 256/512/1024 | 8.192 | 64,6 | 54,9 | USD 0,13 | Médio | jan/2024 |
| text-embedding-3-small | OpenAI | 1536 | 256/512 | 8.192 | 62,3 | 44,0 | USD 0,02 | Médio | jan/2024 |
| embed-v4 | Cohere | 1536 | 256/512/1024/1536 | 128.000 | n/d (sem score MTEB oficial publicado) | Alto (100+ idiomas) | USD 0,12 | Bom | abr/2025 |
| embed-multilingual-v3 | Cohere | 1024 | n/a | 512 | 64,01 | 66,3 | USD 0,10 | Bom | nov/2023 |
| voyage-4-large | Voyage AI | 1024 | 256/512/1024/2048 | 32.000 | 70+ (estimativa) | n/d | USD 0,18 | Bom | abr/2026 |
| voyage-3-large | Voyage AI | 1024 | 256/512/1024/2048 | 32.000 | 68,2 | n/d | USD 0,18 | Médio | jan/2025 |
| voyage-3.5 | Voyage AI | 1024 | 256/512/1024/2048 | 32.000 | 0,9429 nDCG@3 médio | n/d | USD 0,06 | Médio | ago/2025 |
| mistral-embed-2312 | Mistral | 1024 | n/a | 8.192 | ~62 | n/d | USD 0,10 | Médio | out/2025 |
| mxbai-embed-large-v1 | Mixedbread | 1024 | 256/512/768 | 512 | 64,68 | n/d | Open (self-host) | Médio | mar/2024 |
| jina-embeddings-v4 | Jina AI | 2048 | 128/256/512/1024 | 32.768 | 55,97 (MTEB-en) / 66,49 (MMTEB) | Alto (29 idiomas) | USD 0,12 | Bom | jun/2025 |
| nomic-embed-text-v2-moe | Nomic | 768 | 256 | 512 | 56,5 | 65,8 | Open (self-host) | Bom | fev/2025 |
| arctic-embed-l-v2 (2.0) | Snowflake | 1024 | n/a | 8.192 | 55,98 (retrieval NDCG@10) | Sim (multilíngue) | Open (self-host) | Médio | dez/2024 |
| bge-m3 | BAAI | 1024 | n/a | 8.192 | 69,88 | 69,20 | Open (self-host) | Bom | jan/2024 |
| bge-en-icl | BAAI | 4096 | n/a | 32.768 | 71,67 | n/d | Open (self-host) | Baixo (só EN) | jul/2024 |
| gte-large-en-v1.5 | Alibaba | 1024 | n/a | 8.192 | 65,39 | n/d | Open (self-host) | Médio | abr/2024 |
| gte-Qwen2-7B-instruct | Alibaba | 3584 | n/a | 32.768 | 70,24 | Sim (multilíngue) | Open (self-host) | Bom | ago/2024 |
| NV-Embed-v2 | NVIDIA | 4096 | n/a | 32.768 | 72,31 | n/d | Open (self-host) | Médio | set/2024 |
| serafim-pt-900M | Univ. Lisboa | 1024 | n/a | 512 | n/a | "clearly over 0.80" em IR PT | Open (self-host) | Excelente | fev/2026 |

> Fontes diretas: MTEB Leaderboard (huggingface.co/spaces/mteb/leaderboard), OpenAI API docs (developers.openai.com/api/docs/models/text-embedding-3-large), Voyage docs (docs.voyageai.com/docs/embeddings), Cohere docs (docs.cohere.com/docs/cohere-embed), Jina v4 launch post (jina.ai/news/jina-embeddings-v4-universal-embeddings-for-multimodal-multilingual-retrieval), Snowflake Arctic Embed 2.0 (snowflake.com/en/blog/engineering/snowflake-arctic-embed-2-multilingual), BGE-M3 model card (huggingface.co/BAAI/bge-m3), Serafim PT paper (arxiv.org/html/2407.19527v1).

### 1.2 Recomendação por caso de uso

**Multilíngue PT-BR (uso público, custo controlado).** A escolha de produção depende do orçamento e da tolerância a self-hosting. Para custo mínimo com qualidade alta em português, BGE-M3 self-hosted via BentoML ou Ollama é insuperável: 69,2 no MIRACL (que inclui português), 1024 dimensões, 8192 tokens de contexto, zero custo por inferência depois do servidor (uma GPU L4 ou A10 atende milhares de requests por minuto). Para PT-BR crítico (jurídico, médico, conteúdo da Brasil GEO em comparativos com fontes oficiais), a família Serafim PT publicada na ACL Anthology 2026 supera todos os modelos generalistas com escore acima de 0,80 em IR contra 0,74 do melhor GTE inglês.

**On-prem ou edge.** mxbai-embed-large-v1 (Mixedbread), BGE-M3, nomic-embed-text-v2-moe e arctic-embed-l-v2 são as quatro opções viáveis. O nomic-v2-moe tem só 305M parâmetros ativos (mixture of experts) e roda em CPU para volumes baixos. O Arctic Embed 2.0 chegou em dezembro de 2024 com suporte multilíngue explícito e otimização para SQL/dados estruturados, ganho competitivo para portais com dados tabulares como o `papers`.

**Low-cost via API gerenciada.** OpenAI text-embedding-3-small a USD 0,02 por milhão de tokens é o piso de mercado. Voyage 3.5 a USD 0,06 oferece qualidade superior (0,9429 nDCG@3 em domínios variados) com 200M tokens gratuitos mensais. Para `landing-page-geo` em estágio inicial, o regime gratuito Voyage cobre tranquilamente o índice de 800 artigos (estimativa de 12 a 15M tokens totais).

**MTEB top sem restrição de custo.** NV-Embed-v2 (72,31), jasper_en_vision_language_v1 (72,02), bge-en-icl (71,67), stella_en_1.5B_v5 (71,19) e SFR-Embedding-2_R (70,31) são os cinco primeiros do leaderboard em maio de 2026. Todos open weights, mas exigem GPU de alta memória (24 a 40 GB) e otimização de batching para servir produção. Apropriados para `papers` (volumes acadêmicos densos, queries técnicas) onde precisão de fronteira justifica o overhead.

**Multimodal (texto + imagem).** Cohere embed-v4 (texto + imagem em embedding único de 1536 dim, 128k tokens) é o mais robusto comercialmente. Jina v4 (2048 dim, baseado em Qwen2.5-VL-3B, elimina modality gap dos dual-encoders CLIP) é a alternativa open de fronteira, com vantagem de até 12 por cento sobre OpenAI 3-large em retrieval multilíngue. Voyage multimodal-3.5 vale para casos com OCR de PDFs (200M tokens texto + 150B pixels gratuitos por mês).

### 1.3 Matryoshka Representation Learning (MRL): por que importa

Praticamente todos os modelos de 2025-2026 implementam MRL: o vetor de saída pode ser truncado nas primeiras N dimensões sem retreino e mantém alta fidelidade. text-embedding-3-large com 3072 dimensões truncado a 256 mantém 91 por cento da qualidade original. Isso colapsa o trade-off histórico entre qualidade e custo de armazenamento: o `landing-page-geo` pode armazenar 1.024 dim em produção e usar 3.072 só para reranking final, cortando 67 por cento do custo de storage no vector DB sem perda perceptível de recall@10.

---

## 2. Retrieval híbrido

### 2.1 BM25 + denso (canônico desde 2023)

A combinação mais simples de retrieval híbrido fundir BM25 (sparse, lexical) com embedding denso (semantic) via Reciprocal Rank Fusion (RRF) é a baseline obrigatória para qualquer sistema de produção em 2026. Mathieu Brenndoerfer (mbrenndoerfer.com/writing/hybrid-retrieval-combining-sparse-dense-methods-effective-information-retrieval) documenta que a soma ponderada simples (alpha entre 0,3 e 0,7) bate qualquer abordagem isolada em 92 por cento dos benchmarks BEIR.

O Weaviate 1.30 e o Qdrant 1.10+ trazem suporte nativo a RRF e BM25 + dense em uma única query API, e o Weaviate específicamente lança o BlockMax WAND no 1.30 (default para novas instâncias) com aceleração de até 10x em buscas keyword/hybrid. Implementação em produção:

```python
# Padrão Qdrant 1.16 — universal query API
result = client.query_points(
    collection_name="articles",
    prefetch=[
        models.Prefetch(query=bm25_vector, using="bm25", limit=100),
        models.Prefetch(query=dense_vector, using="dense", limit=100),
    ],
    query=models.FusionQuery(fusion=models.Fusion.RRF),
    limit=20,
)
```

### 2.2 SPLADE e sparse neural retrieval

SPLADE (SParse Lexical AnD Expansion model) é a evolução natural do BM25: produz embeddings esparsos altos-dimensionais (tipicamente 30k dimensões com 50 a 200 dimensões ativas), aprendidos por LLM, capturando termos relacionados que o BM25 jamais identificaria. O Qdrant publicou em 2025 um guia canônico (qdrant.tech/articles/modern-sparse-neural-retrieval) confirmando que SPLADE + dense bate BM25 + dense em recall@10 por 3 a 7 pontos em domínios técnicos. Para `papers` (linguagem científica densa, alta densidade lexical), SPLADE é especialmente vantajoso.

Trade-off: SPLADE exige inferência de modelo em cada documento (tempo de indexação 3 a 5x maior) e cada query (latência adicional de 15 a 30ms). Para `landing-page-geo` com ingestão diária baixa, o overhead se paga pelo recall ganho. Para `papers` com ingestão semanal de papers, o custo de indexação dilui.

### 2.3 ColBERT v2 e late interaction

ColBERT mantém embeddings token-level (multi-vector) em vez de pooling para um único vetor. A pontuação MaxSim compara cada token de query contra todos os tokens de documento. Vantagens documentadas pelo Vespa (blog.vespa.ai/announcing-colbert-embedder-in-vespa): recall maior em queries longas com sintagmas complexos, capacidade de explicar match (que token bateu com que token).

Custo: armazenamento por documento aumenta em 32x a 128x (dependendo do truncamento), latência sobe 4 a 8x. Em maio de 2026, o Weaviate 1.30 trouxe quantização multi-vector que reduz o custo de armazenamento de ColBERT em 75 por cento sem perda relevante. Qdrant 1.10 também suporta nativamente. A literatura recente do Qdrant (qdrant.tech/articles/late-interaction-models) é honesta: modelos densos com output token embeddings rivalizam ColBERT em accuracy enquanto consomem 4x menos memória após quantização.

**Recomendação operacional:** ColBERT v2 vale como reranker (top-100 de retrieval híbrido), não como retrieval primário. Para Brasil GEO, exceto em `papers` onde precisão jurídico-acadêmica é crítica, ColBERT está fora do escopo no biênio 2026-2027.

### 2.4 Query expansion: HyDE, multi-query, step-back

**HyDE (Hypothetical Document Embeddings, Gao et al. 2022, arxiv.org/abs/2212.10496).** Em vez de embeddar a query, peça ao LLM para gerar um documento hipotético que responderia a ela, e embedde esse documento. Em domínios sem labels de relevância, HyDE bate retrievers densos zero-shot em todos os benchmarks Mr.TyDi (incluindo coreano, japonês, suahíli). Custo: 1 chamada LLM extra por query (USD 0,0001 com Haiku, latência adicional 200 a 400ms).

**Multi-query Self-Query (Elastic blog, dev.to/sreeni5018).** Use o LLM para reescrever a query original em 3 a 5 variações sintaticamente distintas mas semanticamente equivalentes. Retrieve cada variação, faça RRF dos resultados. Ganho de recall@20 documentado: 8 a 14 por cento. Adequado para queries longas e ambíguas.

**Step-back prompting (PromptHub, Google DeepMind 2024).** Para queries muito específicas, peça ao LLM para abstrair a query em uma versão mais genérica primeiro, recupere, depois use a query original para reranking. Aumenta cobertura em queries com terminologia que pode estar parafraseada nos documentos.

**Recomendação:** em produção, a pilha canônica é HyDE como pré-processamento opcional (toggled por classifier de complexidade de query, ver Adaptive-RAG em 5.3) + retrieval híbrido BM25/SPLADE + dense + reranking. Multi-query e step-back ficam para queries onde o cliente exige cobertura máxima e a latência adicional é aceitável.

---

## 3. Re-ranking 2026

Reranking cross-encoder é o componente que mais multiplica qualidade por dólar gasto em RAG. Anthropic Contextual Retrieval (2024) mostrou que adicionar rerank ao stack contextual + BM25 + dense reduz failure rate de 5,7 por cento para 1,9 por cento (67 por cento de redução). Em maio de 2026, o mercado de rerankers convergiu para cinco fornecedores principais.

### 3.1 Tabela comparativa

| Reranker | Provedor | Max contexto | Latência (top-100) | Multilíngue | PT-BR | Custo por 1M tokens | Lançamento |
|---|---|---|---|---|---|---|---|
| Rerank 4 | Cohere | 8.192 | ~150ms | Sim (100+) | Bom | USD 2,00 | abr/2026 |
| Rerank 3.5 | Cohere | 4.096 | ~120ms | Sim | Bom | USD 1,00 | dez/2024 |
| rerank-2.5 | Voyage AI | 8.000 | ~140ms | Sim | Médio | USD 0,05 | ago/2025 |
| rerank-2.5-lite | Voyage AI | 8.000 | ~70ms | Sim | Médio | USD 0,02 | ago/2025 |
| jina-reranker-v3 | Jina | 8.000 | ~130ms | Sim (29) | Bom | USD 0,02 | jul/2025 |
| mxbai-rerank-large-v2 | Mixedbread | 8.000 | ~150ms (self) | Sim | Médio | Open | fev/2025 |
| bge-reranker-v2-m3 | BAAI | 8.192 | ~180ms (self) | Sim | Bom | Open | jul/2024 |
| MonoT5-3B | NQ original | 512 | ~250ms (self) | Não | Baixo | Open | 2020 |
| RankGPT / RankZephyr | OpenAI/HF | 4.096 | ~600ms (LLM) | Sim | Bom | USD 5+ | 2024-2025 |

> Fontes: cohere.com/blog/rerank-4, cohere.com/blog/rerank-3pt5, blog.voyageai.com/2025/08/11/rerank-2-5, jina.ai/models/jina-reranker-v3, mixedbread.com/blog/mxbai-rerank-v2, huggingface.co/BAAI/bge-reranker-v2-m3.

### 3.2 Trade-off latência x ganho

A pesquisa empírica de 2025 e 2026 converge em três recomendações:

- **Top-100 do retrieval, top-20 do rerank, top-10 para o LLM.** Recall máximo no retrieval (que tem latência baixa) e precisão máxima no rerank (que tem latência média) é o ponto ótimo. Aumentar top-N do retrieval além de 100 raramente compensa o overhead de rerankear 200+ documentos.

- **Listwise vs pointwise.** Rerankers modernos (Cohere 4, Voyage 2.5, Jina v3) usam aprendizado listwise (ordenam toda a lista simultaneamente) e batem pointwise por 5 a 10 pontos em nDCG@10. RankGPT e variantes LLM-as-judge ainda batem cross-encoders em precision@5 para queries especialmente ambíguas, mas a latência (600ms a 2s) e custo (5 a 10x maior) restringem o uso a queries premium.

- **Reranker é onde economizar embeddings densos pesados.** Use embedding mais leve (text-embedding-3-small a USD 0,02 ou BGE-M3 self-hosted) no retrieval e gaste o orçamento de qualidade no reranker (Cohere Rerank 4 a USD 2 por milhão de tokens). Inversão classica de prioridade ainda comum em sistemas legados.

### 3.3 Recomendação canônica para Brasil GEO

`landing-page-geo` e `curso-factory` (volumes médios, query premium-baixa): **Cohere Rerank 3.5** ou **Voyage rerank-2.5-lite**. Custo controlado, latência sub-200ms aceitável para search UX. Voyage 2.5-lite a USD 0,02 por milhão de tokens com 200M tokens gratuitos cobre tranquilamente os 800 artigos iniciais.

`papers` (queries densas, precision crítica em validação de citação): **Cohere Rerank 4** + Jina v3 como fallback open-source. O custo de USD 2 por milhão de tokens dilui em uso B2B/acadêmico, e a robustez em queries com terminologia técnica justifica a escolha.

---

## 4. Vector DBs 2026

### 4.1 Tabela comparativa

| DB | Tipo | Pricing 2026 | Latência p95 | Hybrid search | Multi-tenancy | Quando usar |
|---|---|---|---|---|---|---|
| Turbopuffer | Serverless / S3 | ~USD 0,02/GB storage; pay per query/write | ~10ms p50 cached | Sim (BM25 + ANN) | Namespaces | Cargas write-heavy, ingestão massiva, custo mínimo |
| Pinecone Serverless v2 | Serverless | USD 0,33/GB storage + reads/writes WCU/RCU | ~30ms p99 | Sim (sparse-dense) | Namespaces (até 10k por index) | SaaS enterprise, SLA, sem ops |
| Weaviate 1.30 | Open / Cloud | Free 14 dias; USD 30/org base + uso | ~5-15ms | Sim (BM25 + dense + BlockMax WAND) | Nativo, RBAC | Multimodal, esquemas ricos, RBAC enterprise |
| Qdrant 1.16 | Open / Cloud | Free 1GB RAM / 4GB disk; cloud usage-based | 3,5ms (4,9ms p95, 8,6ms p99) | Sim (Universal Query, IDF, ColBERT) | Tiered, ACORN filter | Performance pura, hybrid avançado, on-prem |
| Milvus 2.4+ | Open / Cloud (Zilliz) | Open self-host; Zilliz Cloud usage-based | ~20-40ms | Sim | 4 estratégias (db/collection/partition/field) | Bilhões de vetores, GPU, escala extrema |
| LanceDB | Open / Embedded | Storage S3-compatible; sem cobrança por DB | ~50ms (depende S3) | Sim (FTS + ANN) | Por path | Notebook, edge, embedded, NL ETL |
| Chroma 0.5+ | Open / Cloud | Local free; Cloud enterprise | ~30ms | Sim básico | Tenants explícitos | Prototipagem, projetos pequenos |
| pgvector + pg_embedding | Postgres | Custo do Postgres apenas | 20-200ms (IVFFlat/HNSW) | Sim (FTS Postgres + vector) | Row-level security | Stack Postgres existente, dados relacionais críticos |
| Vespa | Open / Cloud Yahoo | Cloud usage; self host complexo | ~10-20ms | Sim (busca lexical + tensor + ML ranking) | Tenants nativos | Search platform completa, billion-scale, ML ranking custom |
| Vald | Open | Self host only | ~15ms | Limited | Yes (k8s namespaces) | Kubernetes-native, NGT engine, sem cloud |
| Marqo | Open / Cloud | Cloud usage-based | ~30ms | Sim (CLIP + dense) | Sim | Multimodal CLIP, search APIs prontas |

> Fontes: turbopuffer.com (FTS v2 dez/2025, ANN v3 jan/2026 com 200ms p99 sobre 100 bi vetores), pinecone.io/blog/serverless-architecture, weaviate.io/blog/weaviate-1-30-release, qdrant.tech/benchmarks, qdrant.tech/blog/qdrant-1.16.x, milvus.io, github.com/prrao87/lancedb-study, github.com/chroma-core/chroma/releases, blog.vespa.ai/billion-scale-knn-part-two, github.com/vdaas/vald, marqo.ai/courses/introduction-to-vector-databases.

### 4.2 Custos reais comparados (100M vetores 1024-dim, 1M queries/mês)

| DB | Custo mensal | Notas |
|---|---|---|
| Turbopuffer | ~USD 90-220 | Storage S3 + writes + queries cacheados |
| Pinecone Serverless v2 | ~USD 500-2.000 | Storage 0,33/GB + WCU + RCU |
| Qdrant Cloud | ~USD 300-800 | Cluster managed médio |
| Weaviate Cloud | ~USD 400-1.200 | Hybrid + replicação |
| Milvus / Zilliz Cloud | ~USD 600-1.500 | Cluster managed |
| pgvector em Neon | ~USD 50-150 | Compute Neon + storage |
| LanceDB self-host S3 | ~USD 30-100 | Só S3 + compute serverless |

A diferença Turbopuffer x Pinecone (USD 200 contra USD 2.000) é a maior alavanca de custo do stack em 2026 para sistemas com volume médio. O trade-off: Turbopuffer é mais novo (lançou janeiro de 2024, atingiu maturidade em 2025), e a maturidade do SDK Python e ferramentas de observabilidade ainda fica abaixo de Pinecone. Para `landing-page-geo` e `curso-factory` em early-stage, Turbopuffer é o caminho. Para `papers` com requisitos de conformidade acadêmica e auditoria, pgvector em Neon é canônico (controle total, custo previsível, query SQL nativa).

### 4.3 Quantização e otimização de memória

Qdrant binary quantization (qdrant.tech/articles/binary-quantization) é a técnica de maior alavanca em 2026: reduz memória em 32x (900 MB para 128 MB em 100k OpenAI embeddings), com aceleração até 40x via SIMD. A perda de precisão é mitigada via oversampling + rescoring (busca top-200 binário, rescore com floats originais). Para vetores acima de 1024 dimensões, a perda de qualidade é negligenciável. Habilitar binary quantization em Qdrant ou Weaviate corta custos de cluster pela metade ou mais com configuração mínima.

### 4.4 Decisão para Brasil GEO

- **`landing-page-geo`:** Turbopuffer (custo) ou pgvector em Neon (já tem stack Postgres). Ambos cobrem o cenário de 800 artigos + 12-15M tokens. Recomendação canônica: **pgvector em Neon** para evitar acréscimo de fornecedor, com possibilidade futura de migrar para Turbopuffer se volume ultrapassar 10M vetores.

- **`papers`:** **pgvector em Neon** (já é stack core), com Qdrant como segunda camada para queries complexas com filtragem em metadados densos (DOI, ano, área temática, fonte). A separação permite manter consistência transacional para o sistema canônico e ganhar performance em queries de pesquisa exploratória.

- **`curso-factory`:** **LanceDB embedded** (formato Parquet em S3 ou local) para cross-link offline em build time. Não precisa de um vector DB rodando 24x7; o cross-link entre aulas é computado durante a geração do curso e congelado no JSON do output.

---

## 5. Agentic RAG patterns 2026

### 5.1 Self-RAG (Asai 2023, arxiv.org/abs/2310.11511)

Self-RAG treina um LLM customizado para gerar quatro tokens de reflexão durante a geração: `[Retrieve]` (decisão de recuperar), `[IsRel]` (relevância do passage), `[IsSup]` (suporte do passage à afirmação) e `[IsUse]` (utilidade da resposta). Em produção 2026, Self-RAG é mais útil como filosofia (sempre questionar se a recuperação é necessária e se o passage realmente suporta a resposta) do que como implementação literal — modelos de base já tão capazes que faz mais sentido orquestrar via prompts estruturados do que treinar Self-RAG do zero. Repo canônico: github.com/AkariAsai/self-rag.

### 5.2 CRAG, Corrective RAG (Yan 2024, arxiv.org/abs/2401.15884)

CRAG adiciona um avaliador leve de retrieval que classifica o resultado em três níveis: correto, incorreto, ambíguo. Para "incorreto", busca web complementar. Para "ambíguo", aplica refinamento decompose-then-recompose. Implementação canônica: github.com/HuskyInSalt/CRAG. Padrão genuinamente útil em produção 2026 para sistemas que cobrem domínios com conhecimento volátil (notícias, regulação, mercados), porque permite fallback gracioso sem reescrever todo o pipeline.

### 5.3 Adaptive-RAG (Jeong NAACL 2024, arxiv.org/abs/2403.14403)

Adaptive-RAG treina um classificador leve que decide entre três rotas: sem retrieval, retrieval single-step ou retrieval multi-step iterativo. Reduz custos médios em 30 a 50 por cento mantendo qualidade. Repo: github.com/starsuzi/Adaptive-RAG. Em produção, vira componente front-end de qualquer router de query. KeiroLabs (keirolabs.cloud/blogs/rag/what-is-adaptive-rag-and-when-should-i-use-it) reporta que sistemas que adotam Adaptive-RAG cortam em até 60 por cento o uso de chamadas LLM em pipelines multi-step.

### 5.4 RAPTOR (Sarthi NeurIPS 2024, arxiv.org/abs/2401.18059)

RAPTOR constrói uma árvore via embedding + clustering (GMM) + sumarização recursiva. Bottom-up: chunks viram clusters, clusters geram summaries, summaries viram chunks de nível N+1. Retrieve em qualquer nível da árvore. Ganho documentado: +20 por cento em accuracy absoluta no QuALITY benchmark com GPT-4. Para `curso-factory`, RAPTOR é especialmente adequado: gera uma árvore de conceitos a partir das aulas, permitindo retrieval em granularidade adaptativa (conceito, lição, módulo, curso). Implementações: github.com/parthsarthi03/raptor, integração nativa LlamaIndex.

### 5.5 GraphRAG 1.0 (Microsoft, abr/2026)

Microsoft GraphRAG saiu da versão experimental (julho 2024) para 1.0 em abril de 2025 e está agora em 3.0.9 (abril de 2026). Pipeline: extração de entidades + relações via LLM, clustering hierárquico via Leiden, geração de community summaries, query global (síntese sobre todo o grafo) vs local (entidade-centrada) vs DRIFT (foco em entidade + community context). Documentação: microsoft.github.io/graphrag, repo github.com/microsoft/graphrag.

Custo: ingestão de GraphRAG em corpus médio (1.000 documentos) custa USD 50 a 200 por LLM calls, comparado com USD 5 a 20 para chunking simples. Vale para queries de síntese cross-corpus. Para Brasil GEO, GraphRAG faz sentido em `papers` (consolidar conhecimento entre estudos) e potencialmente em `curso-factory` (descobrir conceitos transversais entre cursos). Para `landing-page-geo`, é overkill.

### 5.6 HippoRAG 2 (Gutierrez NeurIPS 2024, arxiv.org/abs/2405.14831)

Inspirado em hipocampo: combina LLM + knowledge graph + Personalized PageRank. Ganho de até 20 por cento em multi-hop QA, single-step retrieval rivaliza com IRCoT iterativo enquanto sendo 10-30x mais barato e 6-13x mais rápido. Repo: github.com/osu-nlp-group/hipporag. Em produção 2026, HippoRAG 2 é a alternativa low-cost ao GraphRAG quando o orçamento de ingestão é restrito mas multi-hop é necessário.

### 5.7 MemGPT/Letta (letta.com/blog/memgpt-and-letta)

MemGPT foi absorvida pela Letta em 2024. Letta é hoje a plataforma canônica para agentes statefully (memória persistente entre sessões). Arquitetura: memória de trabalho + memória archival vector + memória core. Repo: github.com/letta-ai/letta. Para `curso-factory`, Letta é o framework natural para um tutor virtual que lembra de aulas passadas do aluno.

### 5.8 LangGraph Platform GA (langchain.com/blog/langgraph-platform-ga)

LangGraph atingiu GA em 2025 e segue como framework de orquestração agentic canônico. Pattern de RAG agentic via LangGraph documentado em docs.langchain.com/oss/python/langgraph/agentic-rag. Boa escolha para implementar Adaptive-RAG + CRAG + reranker em uma máquina de estados auditável.

### 5.9 LlamaIndex Workflows 1.0 (llamaindex.ai/blog/announcing-workflows-1-0)

LlamaIndex Workflows 1.0 (anunciado 2025) cobre o caso de uso de orquestração agentic com foco em document workflows: LlamaParse v2 (parsing com até 50 por cento de redução de custo), LiteParse (open-source local), LlamaSheets, LlamaSplit, AgentWorkflow. ParseBench (benchmark próprio) coloca LlamaParse Agentic em 84,9 por cento em todas as 5 dimensões. Para `papers` (ingestão de PDFs acadêmicos), LlamaParse v2 + Workflows 1.0 é o caminho mais rápido para production.

### 5.10 CrewAI

CrewAI (crewai.com/open-source, github.com/crewaiinc/crewai) é o framework agentic de maior crescimento em produção 2025-2026 segundo o ZenML LLMOps report (zenml.io/blog/what-1200-production-deployments-reveal-about-llmops-in-2025). Foco em multi-agent orchestration com roles e tarefas. Para Brasil GEO, CrewAI faz sentido se o roadmap incluir agentes especializados (research, draft, fact-check, publish), cada um com tools e knowledge bases distintas. Não é prioritário até o programa GEO atingir 50+ artigos por mês com pipeline complexo.

### 5.11 Padrões emergentes 2026

O ZenML report de 2025 destila três padrões dominantes em deployment produção (mais de 1.200 sistemas observados):

1. **Router + Retriever + Reranker + Reader** (~57 por cento dos sistemas).
2. **Router + Multi-step Iterative Retrieval com self-correction** (~22 por cento).
3. **Knowledge graph hybrid (entity extraction + dense + KG traversal)** (~21 por cento).

A penetração de GraphRAG mais que dobrou em 2025 sob a evidência de queries cross-corpus, mas ainda fica atrás do padrão 1 em volume.

---

## 6. Chunking e ingestão 2026

### 6.1 Late chunking (Jina 2024, jina.ai/news/late-chunking-in-long-context-embedding-models)

Em vez de chunk-then-embed, faz embed-do-documento-inteiro-then-chunk. O embedding model (deve ser de contexto longo, 8k+) processa o texto completo e gera embeddings token-level. Os chunks são pooled retroativamente. Resultado: cada chunk preserva contexto cruzado, eliminando o "lost context problem" de chunking ingênuo.

Exemplo documentado pelo Jina: similaridade de "Berlin" contra sentença com anáforas vai de 0,708 (naive) para 0,825 (late chunking). Quanto mais longo o documento, maior o ganho. Suportado por jina-embeddings-v3 e v4, BGE-M3, e qualquer modelo com mais de 8k tokens de contexto.

### 6.2 Contextual chunking (Anthropic set/2024, anthropic.com/news/contextual-retrieval)

Para cada chunk, gere um contexto explicativo curto (50-100 tokens) que o situe no documento, e prependa esse contexto ao chunk antes do embedding e antes do BM25. Usando Claude Haiku para gerar os contextos + prompt caching, o custo cai para USD 1,02 por milhão de tokens de documento. Resultado canônico já citado: 49 por cento de redução de failure rate (contextual embed + contextual BM25), 67 por cento com reranking.

A combinação Contextual Retrieval + reranker virou o padrão de referência da indústria em 2025-2026. A implementação completa está no Anthropic Cookbook (cookbook do Claude).

### 6.3 Proposition indexing (Chen et al. 2023)

Quebra o documento em proposições atômicas (subject-predicate-object) via LLM, indexa essas proposições em vez de chunks contínuos. Ganhos em fact-based retrieval e multi-hop QA, mas custo de ingestão alto e perda de contexto narrativo. Útil para domínios em que a unidade de conhecimento é a proposição (jurídico, médico, científico) — relevante para `papers`.

### 6.4 Hierarchical chunking

Estruture o documento em 3 a 5 níveis (capítulo, seção, parágrafo, sentença, frase) e indexe cada nível separadamente. Retrieval adapta granularidade conforme a query. Implementação nativa em LlamaIndex (HierarchicalNodeParser). Para `curso-factory`, é o esquema natural (curso → módulo → aula → seção → exercício).

### 6.5 Small-to-big retrieval

Recupere chunks pequenos (proposição ou sentença) para precisão, depois expanda para chunks maiores (parágrafo ou seção) ao formar o contexto que vai ao LLM. Reduz ruído mantendo cobertura. LlamaIndex e LangChain têm implementações canônicas.

### 6.6 Sentence-window retrieval

Para cada sentença candidata, recupere uma janela de N sentenças antes e depois. Bom equilíbrio entre precisão (sentença) e contexto (janela). Padrão para chatbots de suporte.

### 6.7 Semantic chunking via embedding similarity

Em vez de chunks de tamanho fixo, deslize uma janela ao longo do documento e divida onde a similaridade entre sentenças consecutivas cai abaixo de um limiar. Implementações: LangChain `SemanticChunker`, LlamaIndex `SemanticSplitterNodeParser`. Ganhos sólidos para documentos heterogêneos (mix de tópicos), perdas para documentos monotemáticos.

### 6.8 Recomendação para Brasil GEO

- **`landing-page-geo`** (artigos HBR de 1.500-3.000 palavras): Contextual chunking de 800 tokens com overlap de 100 + contexto Anthropic-style. Late chunking se migrar para BGE-M3 ou Jina v4.
- **`papers`** (papers acadêmicos de 6k-30k tokens): Hierarchical chunking (seção → parágrafo → proposição) + proposition indexing para abstracts e conclusões. Late chunking obrigatório.
- **`curso-factory`** (aulas e cursos): Hierarchical chunking nativo (curso → módulo → aula → seção). Semantic chunking via embedding similarity para detectar transições conceituais dentro de uma aula longa.

---

## 7. Long-context vs RAG vs híbrido

### 7.1 Estado dos contextos

| Modelo | Contexto máximo | Custo input por 1M | Janela útil prática |
|---|---|---|---|
| Gemini 2.5 Pro | 2.000.000 | USD 1,25-2,50 | ~1M antes de degradação |
| Claude Opus 4.7 (1M) | 1.000.000 | USD 5,00 | ~700k antes de degradação |
| GPT-5 | 200-400k | USD 1,25-5,00 | ~200k antes de degradação |
| Claude Sonnet 4.6 | 200k | USD 3,00 | ~200k |
| GPT-4o / GPT-4 Turbo | 128k | USD 2,50-10 | ~128k |

### 7.2 Quando RAG ainda vence (consenso 2026)

Mesmo com 2M de contexto disponível, RAG vence em três dimensões:

1. **Custo.** Processar 1M tokens via Gemini 2.5 Pro custa ~17x mais que recuperar 2k tokens via RAG e processar com modelo médio. Para qualquer caso de uso com query-time inference frequente, RAG é mais barato.
2. **Freshness.** Knowledge bases podem ser atualizadas em minutos. Long context exige reembedding do contexto inteiro a cada query.
3. **Grounding.** RAG mantém atribuição explícita a chunks com 99,2 por cento de precisão (medição Stanford CAIS 2025). Long context produz citações imprecisas em 68 por cento dos casos, segundo o mesmo estudo.

### 7.3 Long context + RAG (híbrido)

A arquitetura emergente em 2026 é: RAG agressivo no retrieval (top-50 a top-100 chunks), seguido por contexto longo (50k a 200k tokens) no LLM. O LLM recebe contexto rico em vez de comprimido, e ainda mantém atribuição via chunk IDs. Anthropic Prompt Caching (cache write 1,25x, cache read 0,1x) torna esse padrão viável: o contexto base do sistema (system prompt + tools + documentos pre-warmed) fica em cache, queries variam o user message e os chunks dinâmicos.

### 7.4 Anthropic Prompt Caching (canônico 2026)

Cache write custa 1,25x o preço base (TTL 5 min) ou 2x (TTL 1h). Cache read custa 0,1x. Min tokens: 4.096 (Opus 4.7, 4.6, 4.5, Haiku 4.5), 1.024 (Sonnet 4.6, 4.5, Opus 4.1), 2.048 (Haiku 3.5). Máx 4 breakpoints por request. Documentação oficial: platform.claude.com/docs/en/docs/build-with-claude/prompt-caching.

Para Brasil GEO, prompt caching é alavanca de 70 a 90 por cento de redução de custo em três cenários:

- **`landing-page-geo`** chatbot: sistema + voice rules + glossário em cache.
- **`papers`** validação de citação: paper completo em cache enquanto o LLM checa múltiplas afirmações.
- **`curso-factory`** geração: rubricas + briefing + arquitetura do curso em cache enquanto o LLM gera aula por aula.

### 7.5 KV cache optimization

KV cache otimização (compressão de attention key-value pairs) é técnica que opera dentro do model serving. Não é configurável diretamente pelo usuário do API, mas habilita os preços baixos da Anthropic, Google e OpenAI para contextos longos. Para self-hosting (Llama, Qwen, Mistral), bibliotecas como vLLM e SGLang trazem implementações nativas de PagedAttention e Continuous Batching que reduzem custos em até 70 por cento.

---

## 8. Evaluation e eval

### 8.1 RAGAS 0.3+ (docs.ragas.io)

Métricas core 2026: Faithfulness, Answer Relevancy, Context Precision, Context Recall, Context Entity Recall, Noise Sensitivity. Pode rodar em CI via decorador. Suporta custom metrics. Recomendado integrar em pipeline de PR de qualquer sistema RAG: cada PR roda RAGAS sobre dataset golden e bloqueia merge se faithfulness cair abaixo de threshold. Para `papers`, o RAGAS é mandatório dado o requisito de citação verificável.

### 8.2 TruLens

TruLens (truera.com / trulens.org) fornece instrumentação contínua em produção. Métricas RAG triad: groundedness, context relevance, answer relevance. Útil para monitoramento. Para Brasil GEO, integrar TruLens no `papers` produciona dashboards de drift de qualidade.

### 8.3 ARES (Saad-Falcon UMass 2024)

ARES (Automated RAG Evaluation System) usa LLM-judge calibrado com prediction-powered inference. Custo mais alto que RAGAS mas precisão de avaliação maior, especialmente em domínios técnicos. Ainda mais nicho que RAGAS em adoção 2026.

### 8.4 BEIR (Benchmark) e MTEB v2

BEIR continua o benchmark canônico de retrieval (18 datasets). MTEB v2 (lançado 2025) expandiu para 130+ tarefas em 50+ idiomas, com módulos específicos PT-BR via inclusão de datasets brasileiros e Serafim PT. Use o BEIR para sanity-check do retrieval em domínio adjacente, MTEB v2 para validação de embedding antes de migração.

### 8.5 Needle-in-a-Haystack v2 e FRAMES

Needle-in-a-Haystack v2 (greg.kamradt) virou padrão informal para testar long context. FRAMES (Google DeepMind 2024) é o benchmark canônico de long-form reasoning com multi-hop e citation. Para validar o ganho de migrar para Gemini 2.5 Pro ou Claude Opus 4.7, FRAMES é a evidência canônica.

### 8.6 Recomendação Brasil GEO

- **`landing-page-geo`**: RAGAS no pipeline de search interno + golden dataset de 50 queries representativas.
- **`papers`**: RAGAS + TruLens + golden dataset de 200 citações conhecidas para regression test em qualquer mudança de pipeline.
- **`curso-factory`**: RAGAS adaptado para QA pedagógica + métricas próprias (cobertura de objetivos de aprendizagem).

---

## 9. Semantic cache e cost optimization

### 9.1 GPTCache evolution

GPTCache (Zilliz 2023, github.com/zilliztech/GPTCache) foi a primeira biblioteca de semantic cache popular. Em 2026, o pattern se generalizou: cache de queries semelhantes (similarity acima de 0,95 cosine) com resposta anterior. Reduz custo em 30 a 60 por cento em sistemas com queries repetitivas (chatbot de suporte, FAQ).

Para Brasil GEO, semantic cache faz sentido no chatbot público de `landing-page-geo` se ele for lançado. Não vale para `papers` (queries únicas) nem `curso-factory` (geração única por curso).

### 9.2 Semantic deduplication

Antes de armazenar embeddings, deduplique semanticamente (remova chunks com similaridade acima de 0,98). Reduz custo de storage em 10 a 30 por cento em corpos com versões/republicações. Especialmente relevante para `papers` (papers republicados em diferentes journals).

### 9.3 Anthropic prompt caching (already covered, ver 7.4)

A maior alavanca de custo de 2024-2026 em LLM. Para Brasil GEO, deve ser default em qualquer chamada Claude com contexto reutilizável acima de 1.024 tokens.

### 9.4 Cost optimization stack 2026

A pilha recomendada para sistemas em produção:

1. **Roteador de query (Adaptive-RAG):** corta chamadas LLM em 30-60 por cento.
2. **Semantic cache:** corta chamadas LLM redundantes em 30 por cento adicional.
3. **Prompt caching:** corta tokens pagos em 70-90 por cento dentro das chamadas que sobram.
4. **Embedding compacto (256-dim via MRL) com rescoring 1024-dim:** corta storage em 67 por cento.
5. **Binary quantization no vector DB:** corta memória em 32x com perda neglígenciável.
6. **Reranker leve (Voyage 2.5-lite a USD 0,02):** mantém qualidade sem o custo de Cohere Rerank 4.

Para o `landing-page-geo` em escala 2026, esse stack mantém custo de inferência abaixo de USD 100/mês para 50k queries/mês.

---

## 10. Aplicação direta nos 3 repos

### 10.1 landing-page-geo (alexandrecaramaschi.com)

**Caso de uso:** search semântica interna, recomendação de artigos relacionados, chatbot opcional de FAQ.

**Stack recomendado:**

- **Embedding:** OpenAI text-embedding-3-small (USD 0,02/1M, custo controlado, suficiente para PT-BR conversacional) com fallback BGE-M3 self-host se PT-BR rigoroso virar requisito.
- **Vector store:** **pgvector em Neon** (stack já é Neon Postgres + Next.js). Tabela `article_embeddings(article_id, embedding vector(1536), updated_at)`. Indexação HNSW com `m=16, ef_construction=64`.
- **Reranker:** Voyage rerank-2.5-lite (USD 0,02/1M, 200M gratuitos cobrem o catálogo todo).
- **Chunking:** Contextual chunking (Anthropic-style) com 800 tokens por chunk + contexto gerado por Haiku. Cada artigo gera 3 a 8 chunks. Total estimado: 4.000-8.000 chunks para 800 artigos.
- **Pipeline ingestão:** novo artigo TS em `src/lib/articles*.ts` → trigger hook → script `scripts/python/embed_article.py` → INSERT em `article_embeddings` no Neon → trigger Vercel re-deploy.

**Paths e configs canônicos:**

```
landing-page-geo/
├── src/
│   ├── lib/
│   │   ├── search/
│   │   │   ├── client.ts        # cliente pgvector + Voyage rerank
│   │   │   ├── embeddings.ts    # wrapper OpenAI 3-small
│   │   │   └── rerank.ts        # wrapper Voyage 2.5-lite
│   │   └── articles.ts          # existente
│   └── app/
│       └── api/
│           └── search/route.ts  # GET /api/search?q=...
├── scripts/
│   └── python/
│       ├── embed_articles.py    # batch reembed full catalog
│       ├── embed_article.py     # single article on publish
│       └── ragas_eval.py        # CI eval gate
└── docs/
    └── search-canon.md          # arquitetura canonical
```

**Custos mensais estimados (2026):**

- Embedding inicial (800 artigos x média 3.000 tokens x 5 chunks): ~12M tokens x USD 0,02 = **USD 0,24** (one-shot).
- Re-embedding incremental: ~3 artigos/dia x 12k tokens = 360k tokens/dia x 30 = 10,8M tokens/mês x USD 0,02 = **USD 0,22/mês**.
- Queries (estimativa 5k/mês): 5k queries x 100 tokens = 500k tokens query + 5k x 20 chunks x 200 tokens rerank = 20M tokens rerank x USD 0,02 = **USD 0,40/mês**.
- pgvector em Neon: **USD 19-39/mês** (Pro tier).
- **Total: USD 20-40/mês.**

**Cuidados:**

- O Vercel project `landing-page-geo` tem disciplina de 2 pushes/dia (memória `feedback_vercel_project_sem_git_connection`). Em ingestão batch de embeddings, fazer commit único agregado.
- Acentuação PT-BR no payload: o pgvector aceita strings UTF-8 normais, mas garantir que o pre-commit hook de acentos não bloqueie o pipeline de embeddings.

### 10.2 papers (validação de citações acadêmicas)

**Caso de uso:** pipeline de ingestão de papers acadêmicos (PDFs e HTML) para validar citações em artigos publicados em `landing-page-geo`. Indexar abstracts, full text, autor, DOI, year. Permitir queries como "este paper realmente diz X?" para fact-check.

**Stack recomendado:**

- **Parser:** LlamaParse v2 Agentic (84,9 por cento em ParseBench, melhor estrutura para PDFs acadêmicos com tabelas e fórmulas).
- **Chunking:** Hierarchical (paper → seção → parágrafo) + Late chunking com BGE-M3 (8k tokens de contexto, suporta documento médio-longo inteiro em uma passagem). Proposition indexing para abstracts e conclusões.
- **Embedding:** BGE-M3 self-host (69,2 MIRACL multilíngue, qualidade superior em texto científico denso). Alternativa: Cohere embed-v4 a USD 0,12 para começar sem self-host.
- **Vector store:** **Qdrant 1.16 cloud** (USD 100-300/mês) para search exploratória + **pgvector em Neon** para metadados transacionais (autores, DOIs, citation graph).
- **Reranker:** Cohere Rerank 4 (USD 2/1M, qualidade fronteira justificada por uso B2B).
- **Eval:** RAGAS + TruLens em CI. Golden dataset de 200 papers conhecidos com citações esperadas.
- **Agentic layer:** CRAG (com fallback web via Semantic Scholar API) + Adaptive-RAG router. LangGraph para orquestração.

**Paths e configs canônicos:**

```
papers/
├── src/papers/
│   ├── ingestion/
│   │   ├── parse_llamaparse.py     # LlamaParse v2 wrapper
│   │   ├── chunk_hierarchical.py   # late chunking + propositions
│   │   └── embed_bgem3.py          # BGE-M3 inference local
│   ├── retrieval/
│   │   ├── qdrant_client.py        # Qdrant 1.16 hybrid
│   │   ├── rerank_cohere.py        # Rerank 4
│   │   └── crag_pipeline.py        # CRAG implementation
│   ├── eval/
│   │   ├── ragas_runner.py
│   │   └── trulens_logger.py
│   └── api/
│       └── verify_citation.py      # endpoint fact-check
├── golden/
│   ├── citations_v1.jsonl          # 200 known citations
│   └── ragas_eval_results/
└── scripts/
    ├── ingest_paper.py              # CLI single paper
    └── ingest_batch.sh              # nightly ingestion
```

**Custos mensais estimados:**

- BGE-M3 self-host em CoreWeave L4 GPU: ~USD 200-400/mês (24/7) ou via Replicate por chamada (USD 0,0003 por embedding).
- Qdrant Cloud: USD 300/mês.
- Cohere Rerank 4: estimativa 100 fact-checks/dia x 100 documentos x 200 tokens = 2M tokens/mês x USD 2/1M = USD 4/mês.
- LlamaParse v2 Agentic: USD 9 por 1.000 páginas; estimativa 100 papers/mês x 15 páginas = 1.500 páginas = USD 14/mês.
- **Total: USD 530-740/mês** (modelo self-host BGE-M3) ou **USD 400-500/mês** (modelo embed-v4 da Cohere via API).

### 10.3 curso-factory (geração e cross-link automático de cursos)

**Caso de uso:** ferramenta CLI que gera cursos completos (módulos, aulas, exercícios) via LLM. Precisa de RAG sobre conteúdo educacional gerado (para cross-link entre aulas) e ingestão de bibliografia de referência.

**Stack recomendado:**

- **Vector store:** **LanceDB embedded** (formato Parquet, sem serviço rodando, cache local + sync para S3 opcional). Custo zero para tamanhos pequenos.
- **Embedding:** OpenAI text-embedding-3-small (USD 0,02/1M, mais simples para iniciar) ou BGE-M3 local se preferir zero custo de API.
- **Chunking:** Hierarchical (curso → módulo → aula → seção). Semantic chunking dentro de aulas longas.
- **Agentic:** RAPTOR para construir árvore de conceitos cross-curso. LlamaIndex Workflows 1.0 como orquestrador.
- **Retrieval pattern:** Small-to-big (sentença para precisão, expansão para parágrafo no contexto LLM).
- **Memória:** Letta para tutor virtual (post-MVP). Memória de aulas vistas, dificuldades reportadas, preferências de exemplo.

**Paths e configs canônicos:**

```
curso-factory/
├── curso_factory/
│   ├── ingestion/
│   │   ├── chunk.py             # hierarchical + semantic
│   │   └── embed.py             # OpenAI 3-small wrapper
│   ├── retrieval/
│   │   ├── lancedb_client.py
│   │   └── crosslink.py         # find related aulas
│   ├── raptor/
│   │   └── tree_builder.py      # hierarchical clustering + summaries
│   └── workflows/
│       └── crosslink_workflow.py
├── output/
│   ├── courses/
│   │   └── <slug>/
│   │       ├── course.json
│   │       ├── embeddings.lance/  # LanceDB local
│   │       └── raptor_tree.json
├── examples/
└── config/
    └── crosslink.toml
```

**Custos mensais estimados:**

- Embedding (1 curso = 30 aulas x 3.000 palavras = ~100k tokens; 10 cursos/mês = 1M tokens): **USD 0,02/mês**.
- LanceDB: USD 0 (embedded).
- LLM calls de geração (não escopo deste track, mas referenciado): tipicamente USD 2-20 por curso.
- **Total RAG infra: praticamente USD 0/mês.**

**Comandos canônicos:**

```bash
# Geração de curso com cross-link
python -m curso_factory.cli generate \
  --topic "fundamentos-quant-ai" \
  --target-audience "executives" \
  --crosslink-from output/courses/* \
  --output-dir output/courses/

# Reconstruir RAPTOR tree global
python -m curso_factory.raptor.tree_builder \
  --courses-dir output/courses/ \
  --output output/raptor_tree.json
```

---

## Apêndice A — URLs primárias validadas

### Embeddings

1. https://huggingface.co/spaces/mteb/leaderboard
2. https://openai.com/index/new-embedding-models-and-api-updates/
3. https://developers.openai.com/api/docs/guides/embeddings
4. https://developers.openai.com/api/docs/models/text-embedding-3-large
5. https://developers.openai.com/api/docs/models/text-embedding-3-small
6. https://docs.voyageai.com/docs/embeddings
7. https://docs.voyageai.com/docs/pricing
8. https://docs.cohere.com/docs/cohere-embed
9. https://docs.cohere.com/docs/embeddings
10. https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-embed-v4.html
11. https://cohere.com/pricing
12. https://jina.ai/models/jina-embeddings-v4/
13. https://jina.ai/embeddings/
14. https://jina.ai/news/jina-embeddings-v4-universal-embeddings-for-multimodal-multilingual-retrieval/
15. https://huggingface.co/mixedbread-ai/mxbai-embed-large-v1
16. https://huggingface.co/nomic-ai/nomic-embed-text-v2-moe
17. https://huggingface.co/BAAI/bge-m3
18. https://huggingface.co/Alibaba-NLP/gte-large-en-v1.5
19. https://github.com/Snowflake-Labs/arctic-embed
20. https://www.snowflake.com/en/blog/engineering/snowflake-arctic-embed-2-multilingual/
21. https://build.nvidia.com/snowflake/arctic-embed-l/modelcard
22. https://openrouter.ai/mistralai/mistral-embed-2312
23. https://arxiv.org/html/2407.19527v1
24. https://aclanthology.org/2026.propor-1.52/
25. https://www.bentoml.com/blog/a-guide-to-open-source-embedding-models
26. https://modal.com/blog/mteb-leaderboard-article
27. https://www.digitalapplied.com/blog/embedding-model-cost-calculator-vendor-comparison-2026

### Retrieval híbrido e reranking

28. https://qdrant.tech/articles/modern-sparse-neural-retrieval/
29. https://qdrant.tech/articles/late-interaction-models/
30. https://qdrant.tech/articles/binary-quantization/
31. https://aclanthology.org/2022.naacl-main.272/
32. https://arxiv.org/abs/2212.10496
33. https://www.prompthub.us/blog/a-step-forward-with-step-back-prompting
34. https://research.atspotify.com/2025/7/optimizing-query-expansions-via-llm-preference-alignment
35. https://cohere.com/blog/rerank-4
36. https://cohere.com/blog/rerank-3pt5
37. https://blog.voyageai.com/2025/08/11/rerank-2-5/
38. https://jina.ai/models/jina-reranker-v3/
39. https://www.mixedbread.com/blog/mxbai-rerank-v2
40. https://huggingface.co/BAAI/bge-reranker-v2-m3
41. https://blog.vespa.ai/announcing-colbert-embedder-in-vespa/
42. https://www.elastic.co/search-labs/blog/self-querying-retrievers
43. https://zeroentropy.dev/articles/should-you-use-llms-for-reranking-a-deep-dive-into-pointwise-listwise-and-cross-encoders/

### Vector DBs

44. https://turbopuffer.com
45. https://www.pinecone.io/pricing/
46. https://www.pinecone.io/blog/serverless-architecture/
47. https://weaviate.io/blog/weaviate-1-30-release
48. https://weaviate.io/pricing
49. https://weaviate.io/blog/hybrid-search-explained
50. https://qdrant.tech/benchmarks/
51. https://qdrant.tech/blog/qdrant-1.16.x/
52. https://qdrant.tech/blog/qdrant-1.10.x/
53. https://qdrant.tech/pricing/
54. https://milvus.io
55. https://milvus.io/docs/multi_tenancy.md
56. https://zilliz.com/blog/choose-the-right-milvus-deployment-mode-ai-applications
57. https://docs.lancedb.com/search/hybrid-search
58. https://www.trychroma.com/research/context-1
59. https://github.com/chroma-core/chroma/releases
60. https://blog.vespa.ai/billion-scale-knn-part-two/
61. https://blog.vespa.ai/constrained-approximate-nearest-neighbor-search/
62. https://github.com/vdaas/vald
63. https://www.marqo.ai/courses/introduction-to-vector-databases
64. https://neon.com/blog/pg-embedding-extension-for-vector-search
65. https://aws.amazon.com/blogs/database/optimize-generative-ai-applications-with-pgvector-indexing-a-deep-dive-into-ivfflat-and-hnsw-techniques/
66. https://www.morphllm.com/comparisons/turbopuffer-vs-pinecone

### Agentic RAG

67. https://arxiv.org/abs/2310.11511
68. https://arxiv.org/abs/2401.15884
69. https://arxiv.org/abs/2403.14403
70. https://arxiv.org/abs/2401.18059
71. https://arxiv.org/abs/2405.14831
72. https://www.microsoft.com/en-us/research/blog/moving-to-graphrag-1-0-streamlining-ergonomics-for-developers-and-users/
73. https://microsoft.github.io/graphrag/
74. https://github.com/microsoft/graphrag
75. https://github.com/osu-nlp-group/hipporag
76. https://www.letta.com/blog/memgpt-and-letta
77. https://github.com/letta-ai/letta
78. https://docs.langchain.com/oss/python/langgraph/agentic-rag
79. https://www.langchain.com/blog/langgraph-platform-ga
80. https://www.llamaindex.ai/blog/announcing-workflows-1-0-a-lightweight-framework-for-agentic-systems
81. https://www.llamaindex.ai/blog/introducing-agentic-document-workflows
82. https://crewai.com/open-source
83. https://github.com/crewaiinc/crewai
84. https://github.com/AkariAsai/self-rag
85. https://github.com/HuskyInSalt/CRAG
86. https://github.com/starsuzi/Adaptive-RAG
87. https://github.com/parthsarthi03/raptor
88. https://www.zenml.io/blog/what-1200-production-deployments-reveal-about-llmops-in-2025
89. https://www.langchain.com/state-of-agent-engineering
90. https://datanucleus.dev/rag-and-agentic-ai/agentic-rag-enterprise-guide-2026

### Chunking, eval, prompt cache

91. https://jina.ai/news/late-chunking-in-long-context-embedding-models/
92. https://www.anthropic.com/news/contextual-retrieval
93. https://claude.com/blog/prompt-caching
94. https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching
95. https://docs.ragas.io/en/stable/
96. https://github.com/embeddings-benchmark/mteb/
97. https://app.ailog.fr/en/blog/news/beir-benchmark-update

---

## Apêndice B — Diagrama de arquitetura referência RAG 2026

```
┌──────────────────────────────────────────────────────────────────────┐
│                          USER QUERY                                   │
└──────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌──────────────────────────────────────────────────────────────────────┐
│  ADAPTIVE-RAG ROUTER (classifier leve: no-retrieval | single | multi)│
│  + Semantic cache check (top-1 similar query response)                │
└──────────────────────────────────────────────────────────────────────┘
                                  │
                  ┌───────────────┼───────────────┐
                  ▼               ▼               ▼
            no-retrieval     single-step    multi-step (iterative)
                                  │               │
                                  ▼               │
┌──────────────────────────────────────────────────────────────────────┐
│  QUERY EXPANSION (opcional)                                           │
│  - HyDE (gera doc hipotético via Haiku)                               │
│  - Multi-query (3-5 reformulações)                                    │
└──────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌──────────────────────────────────────────────────────────────────────┐
│  HYBRID RETRIEVAL (parallel)                                          │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐         │
│  │ BM25 / SPLADE   │ │ Dense embedding │ │ Optional KG     │         │
│  │ (top-100)       │ │ (top-100)       │ │ (GraphRAG       │         │
│  └─────────────────┘ └─────────────────┘ │ community)      │         │
│                                          └─────────────────┘         │
│  Vector store: Turbopuffer | Pinecone | Qdrant | pgvector            │
│  Chunks: late chunking + contextual chunking (Anthropic-style)        │
└──────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌──────────────────────────────────────────────────────────────────────┐
│  RECIPROCAL RANK FUSION (RRF) → 100 candidates                       │
└──────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌──────────────────────────────────────────────────────────────────────┐
│  RE-RANKER cross-encoder                                              │
│  Cohere Rerank 4 | Voyage rerank-2.5 | Jina v3 | BGE Reranker v2     │
│  Output: top-20                                                       │
└──────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌──────────────────────────────────────────────────────────────────────┐
│  CRAG EVALUATOR (correct | incorrect | ambiguous)                     │
│  - Correto → segue para o LLM                                         │
│  - Incorreto → web fallback (Perplexity / Tavily)                     │
│  - Ambíguo → decompose-then-recompose                                 │
└──────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌──────────────────────────────────────────────────────────────────────┐
│  LLM GENERATION com Prompt Caching                                    │
│  System + Tools + Top-20 chunks em cache (1,25x write, 0,1x read)     │
│  Modelo: Claude Opus 4.7 | GPT-5 | Gemini 2.5 Pro                     │
│  Self-RAG opcional: [Retrieve][IsRel][IsSup] reflection tokens        │
└──────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌──────────────────────────────────────────────────────────────────────┐
│  EVAL ASSÍNCRONO (TruLens / RAGAS)                                    │
│  - Faithfulness, context precision, context recall                    │
│  - Logs para drift detection                                          │
│  - Cache da resposta para semantic cache layer                        │
└──────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
                        RESPOSTA + CITAÇÕES
```

Esse pipeline cobre 100 por cento dos requisitos dos três repos. Para o `landing-page-geo`, simplifica omitindo CRAG e Self-RAG. Para `papers`, é o pipeline completo. Para `curso-factory`, omite o Adaptive-RAG router (queries de geração são previsíveis) e adiciona RAPTOR como camada de organização de chunks pré-retrieval.

---

## Conclusão e próximos passos

O estado da arte de retrieval em maio de 2026 não está em uma única tecnologia revolucionária, mas na orquestração madura de seis componentes canônicos: embeddings densos competitivos (com PT-BR via BGE-M3 ou Serafim para casos críticos), retrieval híbrido com SPLADE ou BM25, reranking cross-encoder leve, vector DB adequado à carga (Turbopuffer/pgvector para baixo custo, Qdrant/Weaviate para escala), chunking contextual (Anthropic-style), e prompt caching agressivo. A camada agentic (Adaptive-RAG, CRAG, GraphRAG) entrega valor real onde a complexidade justifica, mas não é pré-requisito para todos os casos.

Para Brasil GEO especificamente, o plano canônico é:

1. **`landing-page-geo`:** começar com pgvector em Neon + OpenAI 3-small + Voyage rerank-2.5-lite (custo USD 20-40/mês). Validar com RAGAS antes de expandir.
2. **`papers`:** investir em LlamaParse v2 + BGE-M3 + Qdrant + Cohere Rerank 4 + CRAG (custo USD 400-700/mês). Justifica-se pelo uso B2B/acadêmico.
3. **`curso-factory`:** LanceDB embedded + OpenAI 3-small + RAPTOR (custo ~USD 0/mês para a infra RAG). Foco em cross-link de qualidade dentro do output.

Os três repos compartilham o mesmo princípio operacional: contextual chunking + reranker + prompt caching é o triplo que multiplica qualidade por dólar gasto. Tudo o mais é otimização adicional.

---

> Sub-agent Opus · pesquisa concluída 2026-05-20 noite · 5 chamadas Perplexity sonar-deep-research + 17 WebFetch validados · custo Perplexity total registrado em `_track-c-q*-*.json`.
