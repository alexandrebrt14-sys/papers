# oai_p4_semantica_vetorial (OpenAI gpt-5.5 web_search)

# Estado da arte prático em GEO, RAG semântico, embeddings, chunking, rerankers e knowledge graphs  
**Janela analisada:** 01 de maio a 03 de setembro de 2026, com achados principais entre 27 de agosto e 03 de setembro quando localizados.  
**Escopo GEO:** aplicação prática para consultorias como alexandrecaramaschi.com e brasilgeo.ai, com foco em como motores de resposta e pipelines RAG recuperam, reordenam e escolhem passagens citáveis.

## 1. Resumo executivo para GEO

| Tema | O que mudou, evidência de maio a setembro de 2026 | Implicação prática para GEO | Fonte, data, tipo, URL |
|---|---|---|---|
| **Motores de resposta usam fan-out, não apenas uma busca** | Google documenta que AI Overviews e AI Mode podem usar **query fan-out**, emitindo múltiplas buscas relacionadas por subtópicos e fontes de dados, e que os modelos identificam páginas de suporte durante a geração. | Otimizar uma página para uma keyword única é insuficiente, cada cluster deve cobrir subperguntas, entidades, atributos, comparações, datas, locais e objeções. | Google Search Central, documentação rastreada em 31 ago. 2026, fonte primária. ([developers.google.com](https://developers.google.com/search/docs/appearance/ai-features?kgs=aa0bcc3d152ed142)) |
| **Elegibilidade em Google AI depende de indexação e snippet, não de “AI schema” especial** | Google afirma que, para aparecer como link de suporte em AI Overviews ou AI Mode, a página deve estar indexada e elegível a snippet, sem requisitos técnicos adicionais e sem schema.org especial para IA. | Prioridade, crawlability, indexabilidade, conteúdo textual visível, snippets bons, dados estruturados consistentes com o conteúdo visível. | Google Search Central, documentação rastreada em 31 ago. 2026, fonte primária. ([developers.google.com](https://developers.google.com/search/docs/appearance/ai-features?kgs=aa0bcc3d152ed142)) |
| **Embeddings multimodais entram no fluxo de recuperação** | Gemini Embedding 2 foi lançado GA em 22 abr. 2026 e, em 05 maio 2026, o File Search da Gemini API passou a suportar busca multimodal com `gemini-embedding-2`, incluindo metadados de grounding como `media_id` e `page_numbers`. | Para GEO, imagens, PDFs e vídeos precisam de legendas, contexto textual, títulos, páginas citáveis, transcrições e identificação de entidade. | Google AI for Developers, changelog, 22 abr. e 05 maio 2026, fonte primária. ([ai.google.dev](https://ai.google.dev/gemini-api/docs/changelog?authuser=6)) |
| **Chunking fixo perdeu status de “melhor prática universal”** | Estudo controlado em RAG para code completion, submetido em 06 maio 2026, encontrou que aumentar contexto cross-file de 2.048 para 8.192 tokens gerou até **4,2 p.p.** de melhoria, enquanto chunk size teve efeito mais fraco e não monotônico. | Testar chunk por intenção e tipo de documento, FAQ, artigo, tabela, código, lei, produto, em vez de fixar 512 ou 1.000 tokens para tudo. | Wu et al., arXiv:2605.04763, 06 maio 2026, fonte primária. ([arxiv.org](https://arxiv.org/abs/2605.04763)) |
| **Hierarquia e estrutura documental viraram sinal operacional** | HiChunk, ACL 2026, propõe estruturação hierárquica com LLMs ajustados e Auto-Merge Retrieval, visando preservar integridade semântica e granularidade de recuperação. | Headings, H2/H3, perguntas, listas, tabelas e blocos autocontidos não são decoração editorial, são unidades de recuperação e fusão. | Lu et al., ACL 2026, 02 a 07 jul. 2026, fonte primária. ([aclanthology.org](https://aclanthology.org/2026.acl-long.1372.pdf)) |
| **Entidades e KG ajudam quando a resposta exige relação e multi-hop** | EnSI-RAG, submetido em 21 ago. 2026, afirma que RAG por chunks brutos degrada quando limites de chunk separam entidades de evidências, e propõe índice centrado em entidade com registros `(e, t, k, v)` ligados às passagens originais. | Para GEO, criar páginas e seções que conectem entidade, tipo, atributo, relação e evidência, por exemplo “Brasil GEO AI, consultoria, oferece, auditoria de presença em AI Overviews”. | Meng et al., arXiv:2608.21252, 21 ago. 2026, fonte primária. ([arxiv.org](https://arxiv.org/abs/2608.21252)) |
| **Hybrid retrieval é o padrão robusto** | DocuSearch combina busca vetorial, BM25 e expansão por knowledge graph, funde via RRF, reranqueia com cross-encoder e aplica MMR para relevância e diversidade, reportando Precision@10 0,69, Recall@10 0,79 e grounding 89,6%. | Em GEO, não apostar só em embedding, combinar semântica, texto exato, entidades, links internos, marcações e diversidade de evidência. | Saragadam et al., arXiv:2609.01617, submissão em 30 jun. 2026, fonte primária. ([arxiv.org](https://arxiv.org/abs/2609.01617)) |

---

## 2. Como motores de resposta recuperam, reordenam e selecionam passagens

### 2.1 Arquitetura prática observável

| Etapa | O que acontece | Evidência, data, fonte, URL | O que fazer em GEO |
|---|---|---|---|
| **1, Interpretação da query** | O motor de resposta expande a intenção em subconsultas, entidades e facetas. O Google chama isso de **query fan-out** em AI Overviews e AI Mode. | Google Search Central, documentação rastreada em 31 ago. 2026, fonte primária. ([developers.google.com](https://developers.google.com/search/docs/appearance/ai-features?kgs=aa0bcc3d152ed142)) | Mapear cada página para 5 a 12 subperguntas, incluir variações transacionais, comparativas, locais e temporais. |
| **2, Recuperação inicial** | Recuperação mistura busca lexical, busca vetorial e, em sistemas avançados, vizinhança de grafo. DocuSearch usa Qdrant com BGE-Large, BM25 via SQLite FTS5 e expansão KG. | Saragadam et al., arXiv:2609.01617, submissão em 30 jun. 2026, fonte primária. ([arxiv.org](https://arxiv.org/abs/2609.01617)) | Manter correspondência lexical exata para termos de categoria, marca, preço, SKU, cidade, legislação, além de semântica. |
| **3, Fusão de rankings** | Rankings de fontes diferentes podem ser combinados por RRF, no DocuSearch os pesos reportados foram 0,50 vetorial, 0,35 BM25 e 0,15 KG, com constante 60. | Saragadam et al., arXiv:2609.01617, submissão em 30 jun. 2026, fonte primária. ([arxiv.org](https://arxiv.org/abs/2609.01617)) | Não otimizar só para similaridade, páginas devem ser boas em exato, semântico e relacional. |
| **4, Reranking** | Um cross-encoder ou reranker reordena candidatos pelo par query, documento. Cohere mostra fluxo em que resultados semânticos são reranqueados e apenas `top_n` segue para geração. | Cohere Docs, exemplo RAG com Embed e Rerank, rastreado em 03 set. 2026, fonte primária. ([docs.cohere.com](https://docs.cohere.com/docs/rag-complete-example?utm_source=openai)) | Passagens devem ser autocontidas, com resposta direta, entidade nomeada, unidade factual e contexto mínimo. |
| **5, Seleção diversa de evidência** | DocuSearch aplica MMR com fator 0,65 após o rerank para podar por relevância e diversidade. | Saragadam et al., arXiv:2609.01617, submissão em 30 jun. 2026, fonte primária. ([arxiv.org](https://arxiv.org/abs/2609.01617)) | Criar evidência não redundante, definição, estatística, caso, comparação, tabela, fonte primária, FAQ. |
| **6, Síntese e citação** | Gemini File Search adicionou metadados de grounding visual, `media_id` e `page_numbers`, em 05 maio 2026. | Google AI for Developers, changelog, 05 maio 2026, fonte primária. ([ai.google.dev](https://ai.google.dev/gemini-api/docs/changelog?authuser=6)) | PDFs precisam de páginas estáveis, títulos claros, texto extraível, tabelas legíveis e citações por página. |

---

## 3. Evidência prática sobre chunking

### 3.1 Tamanho de chunk

| Questão | Evidência localizada | Conclusão prática para GEO | Fonte, data, tipo, URL |
|---|---|---|---|
| Existe tamanho universal ótimo? | **Não localizado** em fonte primária de maio a setembro de 2026. A evidência localizada aponta efeitos dependentes do domínio. | Evitar regra fixa, testar por template e intenção. | Não localizado. |
| Chunks maiores sempre ajudam? | No estudo de code completion, o ganho dominante veio do contexto cross-file, 2.048 para 8.192 tokens, até 4,2 p.p., enquanto chunk size foi mais fraco e não monotônico. | Em conteúdo técnico, documentação e SaaS, preservar contexto de arquivo, seção e dependência pode valer mais que mexer em tamanho. | Wu et al., arXiv:2605.04763, 06 maio 2026, fonte primária. ([arxiv.org](https://arxiv.org/abs/2605.04763)) |
| Chunk semântico é sempre melhor? | HiChunk afirma que chunking semântico pode gerar granularidade variável, por isso aplica chunk fixo sobre o resultado hierárquico e usa Auto-Merge Retrieval para balancear riqueza semântica e completude. | Melhor padrão: chunk estrutural/hierárquico, depois ajuste de tamanho e fusão adaptativa. | Lu et al., ACL 2026, 02 a 07 jul. 2026, fonte primária. ([aclanthology.org](https://aclanthology.org/2026.acl-long.1372.pdf)) |
| Overlap ainda é obrigatório? | Hyper-RAG usou chunks fixos de 1.200 tokens com overlap de 100 tokens para preservar coerência entre fronteiras. Isso é evidência de uso em sistema, não prova universal. | Usar overlap quando há risco de separar definição, entidade e evidência, mas medir custo de índice e redundância. | Nature Communications, Hyper-RAG, 2026, fonte primária. ([nature.com](https://www.nature.com/articles/s41467-026-71411-1)) |
| Chunk por entidade melhora long-doc QA? | EnSI-RAG aponta degradação quando fronteiras de chunk separam entidades de evidências e propõe índice entidade, tipo, categoria semântica, valor, com links às passagens originais. | Para GEO, cada entidade importante deve aparecer próxima aos seus atributos, relações, números e fontes. | Meng et al., arXiv:2608.21252, 21 ago. 2026, fonte primária. ([arxiv.org](https://arxiv.org/abs/2608.21252)) |

### 3.2 Recomendação operacional de chunking para sites GEO

| Tipo de página | Chunk inicial recomendado | Estrutura recomendada | Motivo |
|---|---:|---|---|
| Artigo “o que é” | 250 a 600 palavras por bloco | H2 pergunta, resposta curta, bullets, exemplo, fonte | A recuperação tende a favorecer unidade autocontida e direta. |
| Página de serviço B2B | 200 a 500 palavras por bloco | Problema, solução, prova, processo, FAQ | Facilita rerank por intenção comercial e seleção de evidência. |
| Estudos, pesquisas, relatórios | 400 a 900 palavras por bloco | Sumário executivo, metodologia, achados numerados, limitações | Preserva estatística, contexto metodológico e citação. |
| PDFs | Por página ou seção lógica | Título por página, legenda de tabela, metadados, número de página | Gemini File Search passou a expor `page_numbers` em grounding. ([ai.google.dev](https://ai.google.dev/gemini-api/docs/changelog?authuser=6)) |
| FAQ | 1 pergunta por chunk | H3 em forma de pergunta, resposta direta, entidade e data | “Heading-pergunta” como prática é defensável por granularidade, mas estudo causal maio a setembro 2026 foi **não localizado**. |
| Conteúdo técnico/código | Função, classe, arquivo ou seção, testado por benchmark | Preservar imports, dependências e contexto cross-file | Em code RAG, contexto cross-file superou tamanho de chunk como fator dominante. ([arxiv.org](https://arxiv.org/abs/2605.04763)) |

---

## 4. Headings-pergunta, densidade de entidade, structured data, frescor e diversidade

| Fator GEO | O que a evidência diz | Grau de evidência | Ação recomendada | Fonte, data, tipo, URL |
|---|---|---|---|---|
| **Headings-pergunta** | Evidência causal específica, maio a setembro 2026, **não localizada**. HiChunk e Google sustentam indiretamente a importância de estrutura textual e hierárquica. | Médio como prática de engenharia, baixo como causal GEO isolado. | Usar H2/H3 como perguntas reais, responder nos primeiros 40 a 80 tokens, depois expandir. | HiChunk, ACL 2026, fonte primária. ([aclanthology.org](https://aclanthology.org/2026.acl-long.1372.pdf)) |
| **Densidade de entidade** | EnSI-RAG mostra que separar entidade e evidência por fronteira de chunk degrada RAG, e propõe índice centrado em entidade. | Alto para RAG long-doc e multi-hop. | Em cada bloco, manter entidade, tipo, atributo, relação, data e fonte no mesmo trecho. | Meng et al., 21 ago. 2026, fonte primária. ([arxiv.org](https://arxiv.org/abs/2608.21252)) |
| **Knowledge graph** | DocuSearch usa expansão por KG como terceiro sinal, junto com vetor e BM25, e reporta ganhos sobre dense-only. | Médio, corpus telecom específico. | Criar grafo editorial: marca, autores, serviços, clientes, setores, localidades, cases, fontes externas. | Saragadam et al., 30 jun. 2026, fonte primária. ([arxiv.org](https://arxiv.org/abs/2609.01617)) |
| **Dados estruturados** | Google diz que structured data deve corresponder ao texto visível e que não há schema.org especial para AI Overviews ou AI Mode. | Alto para Google Search, não prova boost isolado em AIO. | Usar Schema.org correto, Organization, Person, Article, FAQ quando elegível, Product, LocalBusiness, Breadcrumb, mas sem prometer “AI schema”. | Google Search Central, rastreado 31 ago. 2026, fonte primária. ([developers.google.com](https://developers.google.com/search/docs/appearance/ai-features?kgs=aa0bcc3d152ed142)) |
| **Frescor** | Survey de RAG publicado em 01 jun. 2026 aponta que benchmarks ainda falham em capturar atualização dinâmica e temporal freshness. Google recomenda manter Merchant Center e Business Profile atualizados. | Médio, mais forte para consultas temporais, locais, produto e preço. | Criar rotina `lastReviewed`, changelog editorial, atualização de preços, disponibilidade, legislação e dados de negócio. | Wu et al., Artificial Intelligence Review, 01 jun. 2026, fonte primária. ([link.springer.com](https://link.springer.com/article/10.1007/s10462-026-11605-7)) |
| **Diversidade de evidência** | Google afirma que fan-out permite links mais amplos e diversos, e DocuSearch usa MMR para balancear relevância e diversidade. | Alto como princípio de recuperação, médio como causal GEO. | Em uma peça, incluir definição, tabela, dado próprio, fonte primária, exemplo brasileiro, limitação e comparação. | Google Search Central, fonte primária, e Saragadam et al., fonte primária. ([developers.google.com](https://developers.google.com/search/docs/appearance/ai-features?kgs=aa0bcc3d152ed142)) |

---

## 5. Modelos de embedding e rerank, lançamentos e benchmarks

### 5.1 Lançamentos e modelos relevantes de maio a setembro de 2026

| Provedor | Modelo | Data | Tipo | Capacidades e números reportados | Fonte, tipo, URL |
|---|---|---:|---|---|---|
| **Google** | `gemini-embedding-2` | GA em 22 abr. 2026, suporte multimodal em File Search em 05 maio 2026 | Embedding multimodal API | Suporta embedding e busca de imagens no File Search, grounding com `media_id` e `page_numbers`. | Google AI for Developers changelog, fonte primária. ([ai.google.dev](https://ai.google.dev/gemini-api/docs/changelog?authuser=6)) |
| **Google DeepMind** | Gemini Embedding 2, paper | 26 maio 2026 | Paper, embedding multimodal | Paper reporta 62,9 R@1 em MSCOCO, 68,8 NDCG@10 em Vatex, 69,9 em MTEB Multilingual e 84,0 em MTEB Code. | arXiv:2605.27295, fonte primária. ([arxiv.org](https://arxiv.org/abs/2605.27295)) |
| **Google Developers** | Gemini Embedding 2 | 30 abr. 2026 | Blog técnico/vendor | Entrada por chamada: até 8.192 tokens de texto, 6 imagens, 120 s de vídeo, 180 s de áudio e 6 páginas de PDF, com espaço semântico unificado. | Google Developers Blog, fonte primária. ([developers.googleblog.com](https://developers.googleblog.com/en/building-with-gemini-embedding-2/?linkId=61665236)) |
| **Google Developers** | Gemini Embedding 2 com task prefixes | 30 abr. 2026 | Blog técnico/vendor | Prefixos de tarefa para QA, fact checking, code retrieval e search result podem melhorar recuperação quando aplicados em indexação e consulta. | Google Developers Blog, fonte primária. ([developers.googleblog.com](https://developers.googleblog.com/en/building-with-gemini-embedding-2/?linkId=61665236)) |
| **Voyage AI, MongoDB** | `voyage-context-4` | 30 jun. 2026 | Embedding/context retrieval | MongoDB anunciou `voyage-context-4`, Hybrid Search e Native Reranking, com Native Reranking melhorando qualidade de recuperação em até 30%. | MongoDB press release, fonte primária. ([mongodb.com](https://www.mongodb.com/company/newsroom/press-releases/mongodb-delivers-accurate-ai-retrieval-wherever-enterprise-data-lives?utm_source=openai)) |
| **Voyage AI, MongoDB** | `voyage-code-4` | 13 ago. 2026 | Embedding de código | Reportado como superando `voyage-code-3`, Cohere Embed v4, Gemini Embedding 2 e OpenAI v3 large por 13,98%, 19,21%, 16,01% e 40,06% nos 28 datasets de code retrieval usados na avaliação do `voyage-code-3`. | Voyage AI blog, fonte primária. ([blog.voyageai.com](https://blog.voyageai.com/2026/08/13/voyage-code-4/?utm_source=openai)) |
| **Voyage AI, MongoDB** | `voyage-code-4` | 13 ago. 2026 | Embedding de código | Em benchmark agentic code retrieval com 19 benchmarks de PRs de correção, `voyage-code-4` superou `voyage-code-3`, Cohere Embed v4, Gemini Embedding 2 e OpenAI v3 large por 27,54%, 28,25%, 31,03% e 48,58%. | Voyage AI blog, fonte primária. ([blog.voyageai.com](https://blog.voyageai.com/2026/08/13/voyage-code-4/?utm_source=openai)) |
| **Voyage AI, MongoDB** | Model lifecycle | 01 set. 2026 | Documentação | `voyage-4`, `voyage-4-lite`, `voyage-4-large`, `voyage-code-4`, `voyage-context-4`, `voyage-multimodal-3.5`, `rerank-3` e `rerank-3-lite` disponíveis em todos os endpoints, e `rerank-3`/`rerank-3-lite` em Preview. | MongoDB Docs, fonte primária. ([mongodb.com](https://www.mongodb.com/docs/voyageai/models/lifecycle/?utm_source=openai)) |
| **Jina AI** | `jina-embeddings-v5-omni-small` | 11 maio 2026 | Embedding multimodal | Blog reporta embeddings para texto, imagem, áudio e vídeo, com breakdown por modalidade, e score textual 67,0 em MMTEB para o modelo omni-small. | Jina AI blog, fonte primária. ([jina.ai](https://jina.ai/news/jina-embeddings-v5-omni-multimodal-embeddings-for-text-image-audio-and-video/?utm_source=openai)) |
| **Jina AI** | `jina-reranker-v3.5` | 03 ago. 2026 | Reranker listwise | Reportado com 0,6B parâmetros, BEIR 63,20, MIRACL 74,11, RTEB 70,95 e Struct-IR 48,3, reranqueando top-100 de `jina-embeddings-v5-text-small`. | Jina AI blog, fonte primária. ([jina.ai](https://jina.ai/news/jina-reranker-v3-5-faster-listwise-reranking-hybrid-attention-self-distillation/?utm_source=openai)) |
| **Cohere** | `rerank-v4.0-pro` e `rerank-v4.0-fast` | Changelog em 11 dez. 2025, disponibilidade OCI em 09 maio 2026 | Reranker | OCI informa contexto de 32.000 tokens, variantes Pro e Fast, suporte multilíngue, semiestruturado, JSON, tabelas e código. | Oracle OCI release notes, fonte primária. ([docs.oracle.com](https://docs.oracle.com/en-us/iaas/releasenotes/generative-ai/cohere-rerank-4.htm?utm_source=openai)) |
| **Cohere** | `embed-v4.0` | Modelo anterior à janela, documentação rastreada em 2026 | Embedding multimodal | Docs indicam output_dimension 256, 512, 1024 e 1536 para Embed v4+, embedding types float, int8, uint8, binary e ubinary, e inputs mistos texto/imagem. | Cohere Docs, fonte primária. ([docs.cohere.com](https://docs.cohere.com/v2/reference/embed?utm_source=openai)) |
| **OpenAI** | Novos embeddings maio a setembro 2026 | **Não localizado** | Embedding API | Não localizei lançamento oficial OpenAI de novo modelo de embedding no período. A fonte oficial mais recente localizada para embedding continua `text-embedding-3-small` e `text-embedding-3-large`, lançados em jan. 2024, com MTEB 62,3 e 64,6 no anúncio. | OpenAI, 25 jan. 2024, fonte primária. ([openai.com](https://openai.com/index/new-embedding-models-and-api-updates/?continueFlag=796b1e3784a5bf777d5be0285d64ad01&utm_source=openai)) |
| **Qwen, Alibaba** | Qwen3-Embedding e Qwen3-Reranker | Lançamento em 05 jun. 2025, fora da janela, ainda relevante em 2026 | Open-weight embedding/reranker | Série 0,6B, 4B e 8B, contexto 32K, MRL e instruction-aware, embedding dims 1024, 2560 e 4096, rerankers equivalentes. | Qwen GitHub e HF, fonte primária. ([github.com](https://github.com/QwenLM/Qwen3-Embedding)) |
| **Microsoft** | Harrier-OSS-v1 | 30 mar. a 06 abr. 2026, fora da janela principal mas relevante para 2026 | Open-source embedding | Bing blog afirma modelo open-source de embedding com ranking 1º no Multilingual MTEB-v2 em 06 abr. 2026 e versões 27B, 0,6B e 270M. | Microsoft Bing Blog, fonte primária. ([blogs.bing.com](https://blogs.bing.com/search/April-2026/Microsoft-Open-Sources-Industry-Leading-Embedding-Model?utm_source=openai)) |
| **ML-Embed** | ML-Embed | 14 maio 2026 | Paper/open framework | Paper propõe MRL, MLL e MEL para eficiência e relata avaliação em 430 tarefas, com novos recordes em 9 de 17 benchmarks MTEB avaliados. | arXiv:2605.15081, fonte primária. ([arxiv.org](https://arxiv.org/abs/2605.15081?utm_source=openai)) |

### 5.2 Benchmarks práticos, MTEB, BEIR, RTEB e limitações

| Modelo | Benchmark e número reportado | Observação de uso | Fonte, data, tipo, URL |
|---|---:|---|---|
| `gemini-embedding-2` | MTEB Multilingual 69,9, MTEB Code 84,0, MSCOCO R@1 62,9, Vatex NDCG@10 68,8 | Forte opção quando GEO envolve multimodalidade, PDFs, vídeo, imagem, áudio e busca cross-modal. | arXiv:2605.27295, 26 maio 2026, fonte primária. ([arxiv.org](https://arxiv.org/abs/2605.27295)) |
| `Qwen3-Embedding-8B` | MTEB Multilingual Mean(Task) 70,58, MTEB English Mean(Task) 75,22, C-MTEB Mean(Task) 73,84 | Excelente para self-hosting multilíngue, mas lançado em 2025, fora da janela. | Qwen GitHub/HF, fonte primária. ([github.com](https://github.com/QwenLM/Qwen3-Embedding)) |
| `Qwen3-Reranker-4B` | MTEB-R 69,76, CMTEB-R 75,94, MMTEB-R 72,74, MLDR 69,97, MTEB-Code 81,20 | Melhor ponto de equilíbrio entre qualidade e custo entre rerankers Qwen reportados, pois 8B tem MTEB-R 69,02 mas CMTEB-R 77,45. | Qwen GitHub, fonte primária. ([github.com](https://github.com/QwenLM/Qwen3-Embedding)) |
| `jina-reranker-v3.5` | BEIR 63,20, MIRACL 74,11, RTEB 70,95, Struct-IR 48,3 | Forte para semiestruturado e listwise reranking em top-100. | Jina AI, 03 ago. 2026, fonte primária. ([jina.ai](https://jina.ai/news/jina-reranker-v3-5-faster-listwise-reranking-hybrid-attention-self-distillation/?utm_source=openai)) |
| `voyage-code-4` | +48,58% versus OpenAI v3 large em agentic code retrieval, +40,06% versus OpenAI v3 large nos 28 datasets de code retrieval | Para GEO técnico, documentação de API, devtools e software, é candidato forte para busca semântica de código. | Voyage AI, 13 ago. 2026, fonte primária. ([blog.voyageai.com](https://blog.voyageai.com/2026/08/13/voyage-code-4/?utm_source=openai)) |
| `text-embedding-3-large` | MTEB 64,6 e MIRACL 54,9 no anúncio oficial de 2024 | Continua baseline seguro e amplamente suportado, mas sem lançamento novo localizado entre maio e setembro de 2026. | OpenAI, 25 jan. 2024, fonte primária. ([openai.com](https://openai.com/index/new-embedding-models-and-api-updates/?continueFlag=796b1e3784a5bf777d5be0285d64ad01&utm_source=openai)) |
| `text-embedding-3-small` | MTEB 62,3 e MIRACL 44,0 no anúncio oficial de 2024 | Bom baseline custo/benefício, especialmente quando reranker compensa recuperação inicial. | OpenAI, 25 jan. 2024, fonte primária. ([openai.com](https://openai.com/index/new-embedding-models-and-api-updates/?continueFlag=796b1e3784a5bf777d5be0285d64ad01&utm_source=openai)) |
| `Cohere rerank-v4.0-pro` | Benchmark público comparável MTEB/BEIR oficial na janela, **não localizado** | Usável como reranker enterprise multilíngue de 32K, mas números independentes devem ser validados em corpus próprio. | Cohere Docs e OCI, fontes primárias. ([docs.cohere.com](https://docs.cohere.com/v2/docs/models?utm_source=openai)) |

---

## 6. O que isso significa para “nuvem semântica” e “espaço vetorial” em GEO

### 6.1 Nuvem semântica prática

Uma nuvem semântica útil para GEO não é uma lista de palavras relacionadas, é uma matriz de **entidades, atributos, relações, intenções e evidências**. A evidência de EnSI-RAG favorece a modelagem entidade, tipo, categoria semântica e valor, enquanto DocuSearch mostra ganhos ao combinar KG, BM25 e vetores. ([arxiv.org](https://arxiv.org/abs/2608.21252))

| Camada | Exemplo para brasilgeo.ai | Como escrever no conteúdo |
|---|---|---|
| Entidade principal | Brasil GEO AI | Nome consistente, variações, `sameAs`, autores e organização. |
| Tipo | Consultoria de GEO, AEO e SEO para IA | Definição curta em H1/H2 e Schema.org Organization/ProfessionalService quando aplicável. |
| Atributos | Auditoria de AI Overviews, presença no ChatGPT, otimização de entidades | Cada atributo em seção própria com prova e método. |
| Relações | “Brasil GEO AI ajuda empresas brasileiras a serem citadas por motores de resposta” | Frases explícitas sujeito, verbo, objeto. |
| Evidências | Cases, benchmarks, prints, datas, metodologia, fontes | Tabelas, números, datas e URLs citáveis. |
| Temporalidade | “Atualizado em 03 set. 2026” | `dateModified`, changelog e bloco “o que mudou”. |

### 6.2 Espaço vetorial aplicado

O espaço vetorial transforma trechos, imagens, PDFs e vídeos em pontos comparáveis, mas a seleção final não depende apenas da distância vetorial. Google documenta fan-out, Cohere exemplifica rerank, DocuSearch usa RRF, cross-encoder e MMR, e Gemini Embedding 2 mostra que multimodalidade passa a viver no mesmo espaço semântico. ([developers.google.com](https://developers.google.com/search/docs/appearance/ai-features?kgs=aa0bcc3d152ed142))

**Implicação:** conteúdo GEO deve ser recuperável em três eixos:

1. **Lexical:** conter termos exatos, nomes, marcas, cidades, datas, preços, normas.
2. **Semântico:** responder ao significado da pergunta, mesmo sem repetir a keyword.
3. **Relacional:** deixar claro quem faz o quê, para quem, onde, quando, com qual evidência.

---

## 7. Playbook acionável para consultoria GEO no Brasil

| Prioridade | Ação | Por quê | Evidência |
|---:|---|---|---|
| 1 | Criar **blocos de resposta autocontidos** sob H2/H3 em formato de pergunta. | Facilita recuperação, rerank e citação por passagem. | Inferência prática apoiada por Google Search Central e HiChunk, causal específico não localizado. ([developers.google.com](https://developers.google.com/search/docs/appearance/ai-features?kgs=aa0bcc3d152ed142)) |
| 2 | Em cada bloco, incluir **entidade, atributo, relação, data e fonte**. | EnSI-RAG mostra que separar entidade e evidência em fronteiras de chunk prejudica recuperação. | Meng et al., 21 ago. 2026. ([arxiv.org](https://arxiv.org/abs/2608.21252)) |
| 3 | Usar **dados estruturados corretos**, não “AI schema”. | Google diz que não há schema especial para AI Overviews ou AI Mode e que structured data deve bater com texto visível. | Google Search Central, 2026. ([developers.google.com](https://developers.google.com/search/docs/appearance/ai-features?kgs=aa0bcc3d152ed142)) |
| 4 | Manter **frescor auditável** em páginas sensíveis a preço, ferramenta, modelo, lei, ranking e benchmark. | Survey RAG aponta temporal freshness como lacuna relevante, Google recomenda dados de negócio atualizados. | Wu et al., 01 jun. 2026, e Google Search Central. ([link.springer.com](https://link.springer.com/article/10.1007/s10462-026-11605-7)) |
| 5 | Construir **grafo editorial interno** com páginas de entidade, autor, serviço, setor, local e case. | KG expansion melhora pipeline híbrido em DocuSearch, em conjunto com vetores e BM25. | Saragadam et al., 30 jun. 2026. ([arxiv.org](https://arxiv.org/abs/2609.01617)) |
| 6 | Testar chunking por template, não por dogma. | Code RAG mostra efeito não monotônico de chunk size e importância maior de contexto. | Wu et al., 06 maio 2026. ([arxiv.org](https://arxiv.org/abs/2605.04763)) |
| 7 | Diversificar evidência dentro da página. | Google usa fan-out para links mais diversos, DocuSearch usa MMR para diversidade. | Google Search Central e Saragadam et al. ([developers.google.com](https://developers.google.com/search/docs/appearance/ai-features?kgs=aa0bcc3d152ed142)) |
| 8 | Para PDFs, imagens e vídeos, gerar **texto extraível e metadados por página/mídia**. | Gemini File Search passou a retornar `media_id` e `page_numbers` em grounding. | Google AI changelog, 05 maio 2026. ([ai.google.dev](https://ai.google.dev/gemini-api/docs/changelog?authuser=6)) |
| 9 | Medir presença por pergunta, não por keyword. | Google documenta query fan-out e diferentes links entre AI Mode e AI Overviews. | Google Search Central, 2026. ([developers.google.com](https://developers.google.com/search/docs/appearance/ai-features?kgs=aa0bcc3d152ed142)) |
| 10 | Avaliar embeddings e rerankers em corpus brasileiro próprio. | Benchmarks MTEB/BEIR/RTEB não capturam toda variação de dados empresariais e temporalidade. | Survey RAG, 01 jun. 2026. ([link.springer.com](https://link.springer.com/article/10.1007/s10462-026-11605-7)) |

---

## 8. Recomendações de stack em setembro de 2026

| Cenário | Recuperação inicial | Rerank | Observação |
|---|---|---|---|
| Site institucional e blog GEO em português | OpenAI `text-embedding-3-small` ou Qwen3-Embedding-0.6B self-hosted | Cohere Rerank v4 Fast, Jina v3.5 ou Qwen3-Reranker-0.6B | Melhor custo, validar em português brasileiro. |
| Consultoria B2B com relatórios, PDFs e mídia | Gemini Embedding 2 ou Jina v5 omni | Cohere Rerank v4 Pro ou Jina v3.5 | Priorizar multimodalidade e grounding por página. |
| Conteúdo técnico, API, SaaS, devtools | `voyage-code-4` para código, híbrido com BM25 | Qwen3-Reranker-4B ou Jina v3.5 | Voyage reporta ganhos fortes em agentic code retrieval. ([blog.voyageai.com](https://blog.voyageai.com/2026/08/13/voyage-code-4/?utm_source=openai)) |
| Corpus regulado, jurídico, saúde, financeiro | Híbrido, BM25, vetor, KG, filtros temporais | Cross-encoder com logging e avaliação humana | Não confiar apenas em embedding, exigir rastreabilidade e freshness. |
| GEO local no Brasil | Vetor multilíngue + BM25 + entidades locais | Rerank com campos cidade, serviço, prova, reviews | Google recomenda Business Profile atualizado. ([developers.google.com](https://developers.google.com/search/docs/appearance/ai-features?kgs=aa0bcc3d152ed142)) |

---

## 9. Lacunas, incertezas e “não localizado”

| Pergunta | Status |
|---|---|
| Novo modelo oficial de embedding da OpenAI entre 01 maio e 03 set. 2026 | **Não localizado**. |
| Benchmark oficial MTEB/BEIR da Cohere para `rerank-v4.0-pro` publicado entre 01 maio e 03 set. 2026 | **Não localizado**. |
| Estudo causal específico mostrando que H2/H3 em formato de pergunta aumenta citações em AI Overviews, maio a setembro 2026 | **Não localizado**. |
| Prova pública de pesos exatos usados por Google AI Overviews para entidades, freshness, structured data e autoridade | **Não localizado**. Google documenta princípios e elegibilidade, não pesos. |
| Benchmark brasileiro amplo, MTEB-BR oficial e recente para todos os modelos listados | **Não localizado** nas fontes primárias consultadas. |

---

# Conclusão prática

O estado da arte em setembro de 2026 favorece uma abordagem **híbrida, estruturada e orientada a evidência**: páginas não competem apenas por ranking, competem para virar passagens recuperáveis, reranqueáveis, diversas e citáveis. Para GEO no Brasil, a unidade de otimização deve deixar de ser “keyword + artigo” e passar a ser **entidade + pergunta + resposta autocontida + evidência + data + fonte + relação no grafo**. Embeddings melhores ajudam, mas os ganhos mais confiáveis vêm de arquitetura de informação, chunking mensurável, rerank, diversidade de evidência, frescor e consistência entre conteúdo visível, dados estruturados e entidades.

## Fontes
-  — https://aclanthology.org/2026.acl-long.1372.pdf
- AI Features and Your Website | Google Search Central  |  Documentation  |  Google for Developers — https://developers.google.com/search/docs/appearance/ai-features?kgs=aa0bcc3d152ed142
- An Overview of Cohere's Models | Cohere — https://docs.cohere.com/v2/docs/models?utm_source=openai
- Building with Gemini Embedding 2: Agentic multimodal RAG and beyond - Google Developers Blog — https://developers.googleblog.com/en/building-with-gemini-embedding-2/?linkId=61665236
- Embed API (v2) | Cohere — https://docs.cohere.com/v2/reference/embed?utm_source=openai
- EnSI-RAG: Entity-Structure-Indexed Retrieval-Augmented Generation for Long-Document Question Answering — https://arxiv.org/abs/2608.21252
- End-to-end example of RAG with Chat, Embed, and Rerank | Cohere — https://docs.cohere.com/docs/rag-complete-example?utm_source=openai
- GitHub - QwenLM/Qwen3-Embedding · GitHub — https://github.com/QwenLM/Qwen3-Embedding
- How Does Chunking Affect Retrieval-Augmented Code Completion? A Controlled Empirical Study — https://arxiv.org/abs/2605.04763
- Hybrid Retrieval-Augmented Generation with Knowledge Graph Expansion, RRF Fusion, and Per-Chunk Grounded Evaluation for Enterprise Document Search — https://arxiv.org/abs/2609.01617
- Hyper-RAG: combating LLM hallucinations using hypergraph-driven retrieval-augmented generation | Nature Communications — https://www.nature.com/articles/s41467-026-71411-1
- ML-Embed: Inclusive and Efficient Embeddings for a Multilingual World — https://arxiv.org/abs/2605.15081?utm_source=openai
- Microsoft Open-Sources Industry-Leading Embedding Model | Bing... — https://blogs.bing.com/search/April-2026/Microsoft-Open-Sources-Industry-Leading-Embedding-Model?utm_source=openai
- Model Deprecations, Lifecycle States, and Support - Voyage AI by MongoDB - MongoDB Docs — https://www.mongodb.com/docs/voyageai/models/lifecycle/?utm_source=openai
- MongoDB Delivers Accurate AI Retrieval Wherever Enterprise Data Lives | MongoDB — https://www.mongodb.com/company/newsroom/press-releases/mongodb-delivers-accurate-ai-retrieval-wherever-enterprise-data-lives?utm_source=openai
- New embedding models and API updates | OpenAI — https://openai.com/index/new-embedding-models-and-api-updates/?continueFlag=796b1e3784a5bf777d5be0285d64ad01&utm_source=openai
- Release notes  |  Gemini API  |  Google AI for Developers — https://ai.google.dev/gemini-api/docs/changelog?authuser=6
- Retrieval-augmented generation for natural language processing: a survey | Artificial Intelligence Review | Springer Nature Link — https://link.springer.com/article/10.1007/s10462-026-11605-7
- Use Cohere Rerank 4 in OCI Generative AI — https://docs.oracle.com/en-us/iaas/releasenotes/generative-ai/cohere-rerank-4.htm?utm_source=openai
- [2605.27295] Gemini Embedding 2: A Native Multimodal Embedding Model from Gemini — https://arxiv.org/abs/2605.27295
- jina-embeddings-v5-omni: Embeddings for Text, Image, Audio and Video — https://jina.ai/news/jina-embeddings-v5-omni-multimodal-embeddings-for-text-image-audio-and-video/?utm_source=openai
- jina-reranker-v3.5: Faster Listwise Reranking with Hybrid Attention and Self-Distillation — https://jina.ai/news/jina-reranker-v3-5-faster-listwise-reranking-hybrid-attention-self-distillation/?utm_source=openai
- voyage-code-4: code retrieval built for coding agents – Voyage AI — https://blog.voyageai.com/2026/08/13/voyage-code-4/?utm_source=openai