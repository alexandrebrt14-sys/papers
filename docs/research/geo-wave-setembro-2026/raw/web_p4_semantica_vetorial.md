# web_p4_semantica_vetorial (Perplexity WEB Pro, https://www.perplexity.ai/search/cbeb87bb-68c9-432b-aab3-ba1c064ed3bd)

Nota de método: resposta do Perplexity WEB (conta alexandre.brt14@gmail.com, plano gratuito no navegador logado por CDP), usada porque a API devolveu 401 insufficient_quota. Sidebar e sugestões da interface removidos; só resposta e links.

Concluído
4 etapas

Aqui está o estado da arte prático (maio–setembro de 2026) sobre recuperação, reranking e seleção de passagens em motores de resposta (GEO), com evidência sobre chunking, headings, densidade de entidade, dados estruturados, frescor e diversidade, além dos novos modelos de embedding e reranker lançados no período, com benchmarks e fontes datadas.
clickup
+5

Como motores de resposta recuperam, reordenam e selecionam passagens (GEO)

Motores de resposta baseados em RAG/GEO tipicamente operam em três estágios: (1) recuperação densa via embeddings em espaço vetorial (“nuvem semântica”), (2) reranking com cross-encoder/listwise, e (3) seleção final de passagens para citação e geração. A “nuvem semântica” refere-se ao índice vetorial onde cada chunk é um ponto; a similaridade de cosseno entre o vetor da pergunta e os vetores dos chunks define a proximidade semântica e, portanto, a probabilidade de seleção.
llms
+2

Recuperação: a consulta é embedada e o sistema puxa k candidatos (tipicamente 50–200) do índice vetorial.
llms
+1

Rerank: um cross-encoder reavalia pares (query, documento) e devolve um top-10/20 com maior precisão; o ganho típico é +5 a +15 pontos de nDCG@10.
llms
+1

Seleção: o gerador recebe as passagens rerankeadas e escolhe trechos para citação; passagens com embeddings próximos à consulta, boa estrutura (headings claros), entidades densas e dados estruturados tendem a ser priorizadas.
get-ryze
+1

Tamanho de chunk: o que a evidência diz (2026)

Não há “tamanho universal”, mas há consenso prático:

Faixa típica de produção: 256–1.024 tokens por chunk, com sobreposição de 10–20%.
atlan
+2

Conteúdo denso/técnico: chunks menores (200–500 tokens) favorecem precisão.
jobsbyculture
+1

Prosa narrativa/políticas: chunks maiores (500–1.000 tokens) preservam contexto.
jobsbyculture
+1

Default sensato em 2026: ~512–800 tokens com 50–100 tokens de sobreposição, respeitando limites de sentença e headings.
jobsbyculture
+2

Fontes: guias de chunking e benchmarks de RAG de maio–agosto de 2026.
atlan
+4

Headings-pergunta, densidade de entidade e dados estruturados

Headings: chunks que começam em headings e incluem o título da seção embedam melhor o “contexto de seção”, melhorando recuperação.
thepromptbench

Densidade de entidade: passagens com entidades bem definidas (nomes, locais, produtos) e relações explícitas tendem a ter embeddings mais discriminativos e maior chance de citação em GEO.
buzzmatic

Dados estruturados (Schema.org, JSON-LD, tabelas): facilitam extração de fatos atômicos e permitem chunking estruturado (por tabela/campo), o que aumenta precisão de recuperação em perguntas factuais.
jobsbyculture
+1

Frescor: em domínios dinâmicos (notícias, preços, políticas), sistemas priorizam documentos recentes; embeddings sozinhos não capturam frescor, logo metadados de data e sinais de atualização são usados no rerank/seleção.
get-ryze
+1

Diversidade de evidência: para reduzir alucinação e viés, pipelines selecionam passagens de fontes diversas (domínios, autores, datas) antes de gerar a resposta.
get-ryze
+1

Embeddings: novos modelos (maio–setembro 2026) e benchmarks
Modelos proprietários (API)

Google Gemini Embedding 2 (GA em 22 de abril de 2026; amplamente adotado a partir de maio): multimodal (texto, imagem, vídeo, áudio, PDF) em um único espaço vetorial; dimensões 3.072; preço ~US$ 0,15/1M tokens; MTEB Overall ~68,32 (líder em 2026).
clickup
+4

OpenAI text-embedding-3-large/small: mantidos como padrão em stacks OpenAI; dimensões 3.072/1.536 (Matryoshka); preço US$ 0,13/0,02 por 1M tokens; MTEB ~64,6 (sem atualização major no período).
app.ailog
+2

Cohere Embed v4: dimensões 1.536; preço ~US$ 0,10/1M tokens; MTEB Overall ~66,72; forte em multilingue e RAG misto texto+imagem.
app.ailog
+2

Voyage AI voyage-3-large / voyage-context-4: voyage-context-4 lançado em 29 de junho de 2026; dimensões até 2.048 (MRL); preço ~US$ 0,06–0,12/1M tokens; MTEB ~65,1–68; destacado em retrieval contextual.
fast
+1

Jina Embeddings v3/v5: open weights (v3) e API; dimensões 1.024; MTEB Overall ~65,52 (v3); bom custo-benefício.
app.ailog
+1

Modelos open-source / pesos abertos

Qwen3-Embedding-8B: novo líder open em 2026; MTEB Overall ~67,89; Retrieval ~63,8; dimensões 4.096; contexto 32k; livre para uso comercial (Apache 2.0 em alguns lançamentos Qwen).
app.ailog
+2

BGE-M3 / bge-multilingual-gemma2: BGE-M3 permanece forte em multilingue; bge-multilingual-gemma2 ~67,4 no MTEB-Retrieval; dimensões 3.584; Apache 2.0.
app.ailog
+2

Jina-Embeddings-v3: open weights; MTEB ~65,52; bom para self-host.
app.ailog

Fontes primárias/secundárias: leaderboard MTEB 2026 (secundária, compilação), blogs de provedores (primárias quando indicam GA/preço), e comparações técnicas independentes.
clickup
+6

Rerankers: novos modelos (maio–setembro 2026) e benchmarks

Qwen3-Reranker 0.6B / 4B / 8B: lançados em 2026; 8B atinge ~77,0 de nDCG@10 no BEIR (máxima qualidade); 0.6B/4B oferecem trade-offs; pesos abertos (Apache 2.0 em alguns).
llms
+1

Jina Reranker v3.5 (0.6B, listwise): lançado em 3 de agosto de 2026; BEIR nDCG@10 ~63,20, superando Qwen3-Reranker-4B com ~7× menos parâmetros; focado em velocidade e qualidade em dados empresariais.
x
+2

Querit-Reranker-A0.4B / 4B (arXiv:2606.19037, 17 de junho de 2026): família multilingue; A0.4B melhora BEIR de 54,11 para 59,28 e MIRACL de 59,87 para 67,70; 4B atinge SOTA público em reranking multilingue.
arxiv
+1

BGE-Reranker-v2-m3 / Gemma / MiniCPM: v2-m3 (568M, MIT) ~60,4 MTEB Rerank; v2-Gemma (9B) ~64,5; v2-MiniCPM (2,7B) ~62,3; defaults fortes para self-host.
localaimaster

Cohere Rerank 4 (Fast/Pro): API hospedada; preço por busca (Fast ~US$ 2,00/1K, Pro ~US$ 2,50/1K); padrão de mercado em produção.
techsy
+1

Voyage rerank-2.5 / -lite: API; preço por token (rerank-2.5 ~US$ 0,05/1M, lite ~US$ 0,02/1M); bom para candidatos curtos e instruções.
techsy
+1

Fontes: posts de lançamento (Jina, Google), artigos arXiv (Querit), e comparações técnicas de agosto de 2026.
arxiv
+7

Tabelas-resumo (modelos e números)
Embeddings (MTEB / BEIR / preço)
Modelo	Tipo	Dimensões	MTEB Overall	Retrieval	Preço (1M tokens)	Fonte (data)
Gemini Embedding 001/2	API (Google)	3.072	68,32	64,5	~US$ 0,15	
clickup
+2

Qwen3-Embedding-8B	Open weights	4.096	67,89	63,8	Free (self-host)	
app.ailog
+1

Cohere Embed v4	API	1.536	66,72	62,1	~US$ 0,10	
app.ailog
+1

Voyage voyage-3-large / context-4	API	até 2.048	~65,1–68	—	~US$ 0,06–0,12	
fast
+1

OpenAI text-embedding-3-large	API	3.072	64,6	—	US$ 0,13	
app.ailog
+1

Jina-Embeddings-v3	Open/API	1.024	65,52	60,8	Free (open)	
app.ailog

BGE-M3 / bge-multilingual-gemma2	Open	3.584	~67,4 (Retrieval)	—	Free	
aipromptshub
+1
Rerankers (BEIR nDCG@10 / MTEB Rerank)
Modelo	Parâmetros	BEIR nDCG@10	MTEB Rerank	Licença	Fonte (data)
Qwen3-Reranker-8B	~8B	~77,0	—	Tongyi/Apache (varia)	
llms
+1

Querit-Reranker-4B	4B	—	SOTA público (MTEB Multilingual v2)	—	
arxiv
+1

Querit-Reranker-A0.4B	0,4B (MoE)	59,28 (BEIR)	—	—	
arxiv
+1

Jina Reranker v3.5	0,6B	63,20	—	Apache 2.0	
x
+2

BGE-Reranker-v2-Gemma	9B	—	64,5	Apache 2.0	
localaimaster

BGE-Reranker-v2-m3	568M	—	60,4	MIT	
localaimaster

Cohere Rerank 4 (Pro/Fast)	API	—	—	Hosted	
menuagentic
+1

Voyage rerank-2.5	API	—	—	Hosted	
menuagentic
+1
Prática recomendada (GEO, maio–setembro 2026)

Chunking: comece com 512–800 tokens, 10–20% de sobreposição, respeitando headings e sem quebrar sentenças; ajuste com avaliação de recall@K em um conjunto pequeno de consultas representativas.
jobsbyculture
+2

Estrutura: use chunking ciente de documento (headings, seções, JSON/Markdown) e enriqueça com metadados (data, autor, domínio) para frescor e diversidade.
jobsbyculture
+1

Recuperação + rerank: combine um embedding forte (Gemini 2, Qwen3-8B, Cohere v4, Voyage) com um reranker listwise/cross-encoder (Qwen3-Reranker, Jina v3.5, BGE-v2, Cohere Rerank 4) para ganhos de +5–15 nDCG@10.
llms
+2

Entidades e dados estruturados: extraia entidades e use schemas para fatos atômicos; isso melhora a precisão em perguntas factuais e a seleção de passagens citáveis.
buzzmatic
+1

Fontes primárias vs secundárias (exemplos)

Primárias: anúncios de GA e posts oficiais (Google: Gemini Embedding 2 GA em 22/04/2026; Jina: v3.5 em 03/08/2026; arXiv: Querit-Reranker em 17/06/2026).
clickup
+5

Secundárias: leaderboards e comparações (MTEB 2026, blogs de benchmark, tabelas de preços compiladas).
app.ailog
+4

Se quiser, posso transformar isso em um checklist operacional (com valores-alvo de chunk, overlap, k de retrieval, e thresholds de rerank) para seu pipeline GEO.

45 fontes
Sim, por favor, crie um checklist operacional completo
Quais são os thresholds ideais de rerank para o pipeline
Prefiro detalhes sobre os modelos de embedding e custo
Sim, inclua os valores-alvo de chunk e overlap
Não preciso do checklist, mas quero saber mais sobre chunking
Fontes
45





## Links na página
- https://thepromptbench.com/rag-and-retrieval/chunking-strategies-explained/
- https://buzzmatic.com/en/knowledge/geo-wissen/embeddings-und-vektorrelevanz-fuer-geo
- https://app.ailog.fr/en/blog/news/embedding-models-leaderboard-2026
- https://localaimaster.com/blog/reranking-cross-encoders-guide