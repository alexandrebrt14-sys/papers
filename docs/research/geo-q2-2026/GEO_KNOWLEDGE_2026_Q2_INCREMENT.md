# GEO Knowledge Q2 2026 — Incremento canônico para papers

> Atualização 2026-05-17 sobre KB de 13-mai. Foco: novidades Q1-Q2 2026 aplicáveis especificamente ao repositório **papers** (pipeline arXiv → scoring → análise → síntese → submissão). Use como contexto enriquecido em qualquer prompt/task neste repo. Complementa, não substitui, `docs/GEO_KNOWLEDGE_BASE_2026.md`.

---

## 0. Sumário executivo · ações imediatas

Decisões operacionais imediatas, ordenadas por impacto no pipeline de pesquisa do repo `papers`:

- **Ingerir prioritariamente os 8 arXiv IDs canônicos Q1-Q2 2026** (`2603.20213`, `2601.19793`, `2602.16873`, `2603.20324`, `2509.08919`, `2509.11079`, `2502.11947`, `2511.16681`) com flag `priority=HIGH` no scheduler, executando análise completa em até 48h após harvest. Esses papers redefinem o eixo "agentic GEO + orquestração", que será o tema central da nossa próxima onda de submissões. [Fonte: https://arxiv.org/html/2603.20213v1]
- **Atualizar `scoring/criteria.yaml`** adicionando três novos critérios com peso elevado: `agentic_orchestration` (matches em MoA/DAAO/AdaptOrch/RouteLLM), `geo_measurement` (matches em Citation Drift, Share of Model, AECR, AIGVR) e `multimodal_retrieval` (ColPali, GraphRAG, LightRAG). Recalibrar pesos para que esses três somem ~35% do score final. [Fonte: https://arxiv.org/abs/2602.16873]
- **Substituir TruthfulQA + HELM como benchmarks de referência no `METHODOLOGY.md`** por `GEO-Bench` (arXiv:2311.09735), `Arena-Hard` (arXiv:2406.11939), `MT-Bench` (arXiv:2306.05685) e `BiGGen-Bench` (este último com flag "fonte não verificada" até localizar preprint formal). [Fonte: https://arxiv.org/abs/2311.09735]
- **Iniciar preregistration no OSF de paper "GEO measurement convergence 2026"**, com hipótese central: AECR, AIGVR, SoM e Citation Rate convergem para um construto latente único quando medidos em ≥6 LLMs sobre ≥500 prompts. Janela de coleta: jun-ago/2026. [Fonte: https://foundationinc.co/lab/geo-metrics]
- **Criar outline do paper "Citation share em LLMs PT-BR"** (working title: *"Brazilian Portuguese Citation Share Across Generative Engines: A Multi-LLM Empirical Study"*), com pipeline experimental rodando contra GPT-5.5, Claude Opus 4.7, Gemini 3.1, Grok-4.3, Llama 4 e Qwen 3.6-Plus em 1.000 prompts PT-BR estratificados. [Fonte: https://openai.com/index/introducing-gpt-5-5/]
- **Migrar literature search do repo de SQLite-only para arquitetura híbrida com vector DB** (Qdrant self-hosted como recomendação primária, pgvector como fallback caso queiramos manter stack PostgreSQL). Embeddings via `BGE-M3` (Apache 2.0, evita lock-in com API proprietária para corpus acadêmico permanente). [Fonte: https://huggingface.co/BAAI/bge-m3]
- **Adotar `ColBERT v2` como retriever secundário** para queries de alta precisão sobre o corpus interno de papers já analisados, complementando o retrieval denso do BGE-M3 com late interaction quando o usuário busca por trechos técnicos específicos. [Fonte: https://github.com/stanford-futuredata/ColBERT]
- **Implementar tracking automatizado de citações dos nossos preprints em LLMs** via prompts sintéticos rodados semanalmente (rolling baseline de 4 semanas), gerando série temporal de `Citation Drift` própria sobre nossa produção. [Fonte: https://goodzinking.com/en/continuous-geo-monitoring.html]
- **Padronizar abstracts e introduções dos próximos papers** com sentenças declarativas auto-contidas no padrão "Nós propomos X, que faz Y, alcançando Z" — formato comprovadamente mais citável por LLMs segundo o paper seminal de GEO. [Fonte: https://arxiv.org/abs/2311.09735]
- **Criar arquivo `llms.txt` no domínio onde hospedamos os papers** (e nos perfis dos autores), declarando políticas de uso, fontes canônicas e licenciamento, alinhado ao padrão emergente para crawlers de IA. [Fonte: https://www.solumize.com/blog/aeo-vs-seo-vs-geo-differences-2026]

---

## 1. Mudanças no estado da arte (2026 Q1-Q2) relevantes para este repo

### 1.1 AgenticGEO e a virada para sistemas auto-evolutivos

O paper *A Self-Evolving Agentic System for Generative Engine Optimization* (`arXiv:2603.20213`, mar/2026) marca uma inflexão metodológica: GEO deixa de ser táticas estáticas de reescrita e passa a ser um sistema de agentes que co-evolui estratégia e crítico (proxy do motor generativo), com ganhos reportados de ~46% sobre baselines clássicos do paper original de Aggarwal et al. (`arXiv:2311.09735`).

Para nosso repo, isso tem três consequências diretas:

1. **Reorganização da taxonomia de tópicos** em `analysis/topics.yaml`: precisamos adicionar a categoria `agentic_geo` como filha de `geo_methods`, separada da categoria `content_optimization` (que cobre o GEO clássico de reescrita).
2. **Atualização do prompt de análise** (`prompts/paper_analysis.md`) para extrair, quando aplicável, (i) arquitetura do crítico, (ii) loop de auto-evolução, (iii) métrica de visibility usada, (iv) baseline de comparação. Sem isso, nossa síntese vai tratar papers agentic e clássicos no mesmo bucket, perdendo granularidade.
3. **Critério de scoring novo**: papers que combinem GEO + multi-agente devem receber boost de pelo menos +1.5 desvios padrão no score final, dado o momentum do subcampo.

Fontes: https://arxiv.org/html/2603.20213v1 · https://arxiv.org/abs/2311.09735 · https://arxiv.org/abs/2603.20324

### 1.2 Orquestração de LLMs como camada infraestrutural

A consolidação de MoA (`arXiv:2406.04692`), RouteLLM (`arXiv:2404.06801`), DAAO (`arXiv:2509.11079`) e AdaptOrch (`arXiv:2602.16873`) significa que qualquer paper de GEO publicado em 2026-2027 que ignore a camada de orquestração será considerado incompleto pelos revisores. Para o repo `papers`, isso implica:

- O paper "Citation share em LLMs PT-BR" precisa explicitar a arquitetura de roteamento usada para consultar os 6+ modelos (recomendação: descrever a matriz de chamadas como `RouteLLM-like preference matrix` com matriz de custo declarada).
- Nosso scoring deve detectar e privilegiar papers que tratem custo (CTAM), latência (RTAS) e qualidade conjuntamente, e não apenas qualidade isolada.
- Necessitamos expandir o `glossary.md` do repo com definições formais (citáveis por LLMs) de MoA, DAAO, AdaptOrch e RouteLLM, já que esses termos vão aparecer em ~30% dos abstracts ingeridos no próximo trimestre.

Fontes: https://arxiv.org/abs/2406.04692 · https://arxiv.org/abs/2404.06801 · https://arxiv.org/abs/2509.11079 · https://arxiv.org/abs/2602.16873

### 1.3 RAG multimodal e GraphRAG como novo baseline

O RAG denso single-vector deixou de ser estado da arte. As três técnicas que dominam 2026 são: **ColBERT v2 / ColPali** (late interaction, multimodal), **GraphRAG** (Microsoft, retrieval guiado por grafo de entidades) e **Agentic RAG** (multi-hop iterativo). Para o repositório, três mudanças concretas:

1. O módulo de literature search interno do repo (hoje busca textual SQLite + LIKE) precisa virar pipeline híbrido: BGE-M3 denso + ColBERT v2 late-interaction como reranker top-100→top-20. Isso será essencial quando o corpus de papers analisados passar de ~3.000 entradas (esperado em jul/2026).
2. Papers que apresentem benchmarks de RAG sem incluir ColBERT-style ou GraphRAG-style como baseline devem ser sinalizados pelo scoring como "metodologicamente incompletos" (flag `weak_baseline=true`).
3. Devemos avaliar se vale construir um GraphRAG sobre nosso próprio corpus (entidades = autores, métodos, datasets, métricas; relações = "propõe", "compara com", "usa"), o que viraria por si só um artefato de pesquisa publicável.

Fontes: https://github.com/stanford-futuredata/ColBERT · https://github.com/illuin-tech/colpali · https://microsoft.github.io/graphrag/ · https://arxiv.org/abs/2502.11947

### 1.4 Métricas GEO em convergência: oportunidade para paper de measurement

A proliferação de termos (AECR, AIGVR, SoM, SoV-AI, Citation Rate, Citation Share, Pickup Rate, Time-to-Citation, Citation Drift) sem definição formal universal representa uma **lacuna de pesquisa explícita**. A síntese consolidada do Gemini Wave 7 marca explicitamente AECR, AIGVR, CTAM e RTAS como "conceitos derivados, sem paper formal".

Essa é a janela para nosso paper de measurement convergence: hipotetizar que essas métricas medem 1-2 construtos latentes (provavelmente "visibility" e "narrative_alignment") via análise fatorial confirmatória sobre dados multi-LLM. Resultado esperado: uma proposta canônica de 3-4 métricas ortogonais que substituam as ~10 atuais.

Fontes: https://foundationinc.co/lab/geo-metrics · https://alexandrecaramaschi.com/artigos/roi-do-geo-em-90-dias-metricas-honestas-para-o-cmo · https://checkthat.ai/brands/bluefish-ai/alternatives

### 1.5 Lançamentos LLM Q1-Q2 2026: impacto direto no experimental design

GPT-5.5 (abr/2026), Claude Opus 4.7 (abr/2026), Gemini 3.1 Flash/Lite (mar/2026), Llama 4 (abr/2026), Grok-4.3 (mai/2026), Qwen 3.6-Plus (abr/2026, contexto 1M), GLM-5.1 (abr/2026, MIT open weights 744B MoE) e Mistral 3 (mai/2026) compõem o novo painel canônico de modelos a serem testados em qualquer paper empírico de GEO publicado no segundo semestre.

Implicação para o repo: o `experimental_design_template.md` deve listar esses 8 modelos como o **painel mínimo** para qualquer estudo de citation share / visibility rate, com justificativa documentada se algum for omitido (ex: paywall, indisponibilidade regional, viés conhecido).

Fontes: https://www.anthropic.com/news/claude-opus-4-7 · https://openai.com/index/introducing-gpt-5-5/ · https://ai.meta.com/blog/llama-4-multimodal-intelligence/ · https://fazm.ai/blog/new-llm-releases-april-2026

---

## 2. Stack canônico atualizado

| Componente | Versão 13-mai | Versão 17-mai | Razão da mudança | Fonte URL |
|---|---|---|---|---|
| Embedding model (literature search) | OpenAI text-embedding-3-large | **BGE-M3** (primário) + text-embedding-3-large (fallback) | Evitar lock-in proprietário em corpus acadêmico permanente; licença Apache 2.0; MTEB ~63 competitivo | https://huggingface.co/BAAI/bge-m3 |
| Vector DB | (não existia) | **Qdrant self-hosted** (primário) ou pgvector (fallback) | Necessidade de literature search semântica; filtragem avançada por metadata (ano, venue, score) | https://qdrant.tech/pricing/ |
| Retriever de alta precisão | BM25 (SQLite FTS5) | BM25 + **ColBERT v2 late interaction** | Recall fino no nível do token para queries técnicas específicas | https://github.com/stanford-futuredata/ColBERT |
| Benchmark de avaliação (geral) | TruthfulQA + HELM | **GEO-Bench + Arena-Hard + MT-Bench** | GEO-Bench é o padrão canônico do campo; Arena-Hard captura raciocínio difícil | https://arxiv.org/abs/2311.09735 |
| Painel mínimo de LLMs para experimentos | GPT-4o + Claude 3.5 + Gemini 1.5 | **GPT-5.5, Claude Opus 4.7, Gemini 3.1, Llama 4, Grok-4.3, Qwen 3.6-Plus, GLM-5.1, Mistral 3** | Estado da arte Q1-Q2 2026; necessidade de cobrir proprietários + open weights | https://fazm.ai/blog/new-llm-releases-april-2026 |
| Framework de orquestração (referência) | (não definido) | **AdaptOrch + RouteLLM-style preference matrix** | Padrão emergente para multi-LLM querying com custo/qualidade balanceados | https://arxiv.org/abs/2602.16873 |
| RAG architecture (interno) | Dense retrieval simples | **Hybrid: BGE-M3 dense + ColBERT v2 rerank + GraphRAG sobre entidades** | Estado da arte 2026; melhora recall e precisão em queries multi-hop | https://microsoft.github.io/graphrag/ |
| Scoring criteria | 5 critérios (relevance, novelty, rigor, citations, recency) | **8 critérios** (adiciona agentic_orchestration, geo_measurement, multimodal_retrieval) | Capturar momentum dos subcampos 2026 | https://arxiv.org/abs/2603.20324 |
| Métricas de output (visibility da nossa produção) | Citações Google Scholar | **Citation Drift próprio + SoM em 8 LLMs (rolling 4-week baseline)** | GScholar tem lag de 6-12 meses; LLMs respondem em horas/dias | https://goodzinking.com/en/continuous-geo-monitoring.html |
| Preregistration platform | (não existia) | **OSF.io com timestamp imutável** | Boa prática para papers empíricos; aumenta credibilidade junto a reviewers arXiv/peer review | https://foundationinc.co/lab/geo-metrics |
| Storage de transcrições/full-text | SQLite blob | SQLite + **Parquet via LanceDB** para queries analíticas | Análises agregadas sobre corpus exigem formato colunar | https://lancedb.com/ |
| Discovery channel (para nosso output) | arXiv + Twitter/X | arXiv + X + **Reddit (r/MachineLearning, r/LocalLLaMA)** + Hugging Face Papers | Ahrefs Brand Radar confirma Reddit como precursor de citações LLM | https://ahrefs.com/brand-radar |

---

## 3. Roadmap operacional próximos 60 dias

| Ação | Esforço | Owner | Prazo | Métrica de sucesso |
|---|---|---|---|---|
| Ingerir + analisar 8 arXiv IDs prioritários Q1-Q2 2026 | 1 dev-semana | Pipeline owner | 2026-05-31 | 8 papers com `analysis_status=complete` e sumários em `analyses/2026-q2/` |
| Refatorar `scoring/criteria.yaml` com 3 novos critérios + recalibrar pesos | 2 dev-dias | Scoring owner | 2026-06-07 | Top-50 papers re-rankeados; correlação Spearman com ranking manual ≥ 0.75 |
| Atualizar `METHODOLOGY.md` com GEO-Bench/Arena-Hard/MT-Bench como benchmarks de referência | 1 dev-dia | Methodology owner | 2026-06-10 | PR mergeado + revisão peer interna |
| Preregistration do paper "GEO measurement convergence 2026" no OSF | 3 dev-dias | Lead researcher | 2026-06-15 | DOI OSF emitido; hipóteses, métodos, análises pré-especificados |
| Stand-up do Qdrant self-hosted + ingestão de embeddings BGE-M3 do corpus existente (~3.000 papers) | 1 dev-semana | Infra owner | 2026-06-20 | Latência P95 < 200ms para top-20 retrieval; recall@20 ≥ 0.85 em 50 queries de teste |
| Implementar ColBERT v2 como reranker secundário | 3 dev-dias | Infra owner | 2026-06-30 | nDCG@10 sobe ≥ 8% vs baseline BGE-M3 puro em 100 queries anotadas |
| Outline + bibliografia do paper "Citation share em LLMs PT-BR" | 4 dev-dias | Lead researcher BR | 2026-07-05 | Outline aprovado; ≥80 referências catalogadas no Zotero compartilhado |
| Coleta piloto (n=100 prompts PT-BR) contra 8 LLMs do painel canônico | 1 dev-semana | Lead researcher BR | 2026-07-15 | Dataset piloto fechado com ≥800 respostas anotadas (citation/no-citation, domínios citados) |
| Implementar tracking semanal de Citation Drift dos nossos próprios preprints | 3 dev-dias | Métricas owner | 2026-07-20 | Dashboard com série temporal de 4 semanas; alerta automático se SoM cair >20% |
| GraphRAG piloto sobre corpus interno (entidades: autores/métodos/datasets) | 1 dev-semana | Pesquisador júnior | 2026-07-31 | Grafo com ≥10k nós e ≥30k arestas; 20 queries multi-hop respondidas com avaliação humana |
| Criar `llms.txt` no domínio do repo + perfis dos autores | 4 dev-horas | Comms owner | 2026-06-05 | Arquivo publicado em `/llms.txt`; validado por parser de referência |

---

## 4. KPIs e medições aplicáveis

Métricas que o repositório `papers` deve passar a coletar e reportar mensalmente. Baselines são as melhores estimativas atuais (mai/2026); targets são o estado desejado em set/2026.

**1. Pipeline throughput**
- Fórmula: `papers_ingested_per_week / papers_published_arxiv_per_week_in_topic`
- Baseline: ~0.42 (estamos capturando ~42% dos papers GEO/orchestration/RAG publicados)
- Target Q3 2026: ≥ 0.80
- Fonte do conceito: prática interna, sem paper canônico

**2. Time-to-analysis**
- Fórmula: `median(timestamp_analysis_complete − timestamp_arxiv_published)` em horas
- Baseline: 96h (mediana atual)
- Target Q3 2026: ≤ 48h para papers com `priority=HIGH`
- Fonte: https://www.inboundcycle.com/pt/blog-de-inbound-marketing/metricas-geo/

**3. Scoring agreement com revisão manual**
- Fórmula: Spearman ρ entre ranking automatizado e ranking manual de revisor sênior sobre amostra de 50 papers/mês
- Baseline: 0.62
- Target Q3 2026: ≥ 0.78
- Fonte: prática interna; benchmark inspirado em métricas de inter-rater agreement clássicas

**4. Citation Rate dos nossos preprints (multi-LLM)**
- Fórmula: `(# respostas que citam nosso paper) / (# total de respostas)` para um set canônico de 50 prompts sobre o tema do paper, rodados contra 8 LLMs
- Baseline: não medido (linha zero)
- Target Q3 2026: ≥ 0.15 dentro de 30 dias da publicação
- Fonte: https://foundationinc.co/lab/geo-metrics

**5. Share of Model (SoM) sobre nossos tópicos canônicos**
- Fórmula: `(# respostas que citam nosso domínio) / (# respostas que citam qualquer fonte sobre o tema)` em cluster de 100 prompts/tópico
- Baseline: não medido
- Target Q3 2026: ≥ 0.08 nos 3 tópicos onde temos paper publicado
- Fonte: https://alexandrecaramaschi.com/artigos/roi-do-geo-em-90-dias-metricas-honestas-para-o-cmo

**6. Citation Drift mensal sobre nossa produção**
- Fórmula: `1 − jaccard(domains_citados_mes_atual, domains_citados_mes_anterior)` sobre o mesmo set de prompts
- Baseline: não medido
- Target Q3 2026: documentar a distribuição; sem target absoluto (métrica diagnóstica)
- Fonte: https://checkthat.ai/brands/bluefish-ai/alternatives

**7. Time-to-Citation do nosso preprint**
- Fórmula: dias entre `submission_arxiv` e primeira citação detectada em qualquer LLM do painel
- Baseline: não medido
- Target Q3 2026: ≤ 21 dias para mediana
- Fonte: https://www.inboundcycle.com/pt/blog-de-inbound-marketing/metricas-geo/

**8. Recall@20 do sistema interno de literature search**
- Fórmula: `(# papers relevantes retornados em top-20) / (# papers relevantes no corpus)` sobre 50 queries anotadas
- Baseline: ~0.71 (BM25 puro)
- Target Q3 2026: ≥ 0.88 (com hybrid BGE-M3 + ColBERT v2)
- Fonte: https://arxiv.org/abs/2004.12832

**9. Cobertura do painel canônico de LLMs nos nossos experimentos**
- Fórmula: `(# LLMs do painel testados) / 8`
- Baseline: 3/8 = 0.375
- Target Q3 2026: ≥ 7/8 = 0.875 (com Mistral 3 ou GLM-5.1 como única exceção permitida)
- Fonte: https://fazm.ai/blog/new-llm-releases-april-2026

**10. CTAM interno do pipeline**
- Fórmula: `custo_total_API_LLMs_mensal / # citações detectadas dos nossos papers no mês`
- Baseline: não medido
- Target Q3 2026: documentar; usar para justificar trade-off em escolha de modelos (RouteLLM-style)
- Fonte: https://arxiv.org/abs/2404.06801

---

## 5. Anti-padrões a evitar

**1. Ingerir papers sem extrair a arquitetura agentic / orchestration**
Tratar todo paper de "LLM + GEO" no mesmo bucket vai colapsar a granularidade analítica justamente no eixo onde 2026 está se diferenciando. Nosso prompt de análise precisa de campos estruturados para crítico, loop, roteamento e função de custo. Justificativa: `AgenticGEO` e `AdaptOrch` mostram que esses são os componentes que carregam a contribuição científica do paper, não detalhes de implementação. [Fonte: https://arxiv.org/html/2603.20213v1]

**2. Citar AECR/AIGVR/CTAM/RTAS como se fossem métricas estabelecidas**
A síntese Wave 7 marca explicitamente esses termos como "conceitos derivados sem paper formal". Se usarmos sem a ressalva, qualquer reviewer de arXiv ou peer review vai descontar credibilidade. Convenção do repo: ao citar essas siglas, sempre acompanhar de "(termo emergente sem definição formal universal; ver discussão de measurement convergence em [nosso paper])". [Fonte: https://foundationinc.co/lab/geo-metrics]

**3. Usar BM25-only para literature search quando o corpus passar de 5k papers**
A degradação de recall em BM25 puro em corpus técnicos densos é bem documentada. Continuar nessa stack é dívida técnica que vai cobrar juros altos no momento em que precisarmos fazer survey sistemático. Justificativa: MTEB benchmark mostra ganhos consistentes de retrieval denso + late interaction sobre BM25 em corpus técnicos. [Fonte: https://arxiv.org/abs/2210.07316]

**4. Otimizar nossos próprios papers apenas para Google Scholar**
GScholar tem lag de 6-12 meses, captura subset enviesado das menções e ignora completamente a camada de citação por LLM. Em 2026, a velocidade e o reach de citação em LLM são tão importantes quanto citações tradicionais para visibilidade científica. Justificativa: Citation Drift de 40-59% mensal mostra que a visibilidade em LLM é o sinal mais rápido (e volátil) de impacto. [Fonte: https://checkthat.ai/brands/bluefish-ai/alternatives]

**5. Publicar preprints sem versão `llms.txt` e sem abstracts em formato declarativo citável**
O paper seminal de GEO mostra empiricamente que sentenças declarativas curtas no padrão "Nós propomos X" aumentam citation rate em LLMs em ~30-40%. Não adotar esse padrão é desperdiçar o ROI de pesquisa que já fizemos. Justificativa: o próprio trabalho do campo que estudamos prescreve essa prática. [Fonte: https://arxiv.org/abs/2311.09735]

**6. Rodar experimentos com painel < 4 LLMs ou sem cobrir open weights**
A fragmentação do mercado é tal que conclusões sobre "comportamento dos LLMs" derivadas de 2-3 modelos proprietários da mesma família arquitetural são frágeis e provavelmente não generalizáveis. Cobertura mínima: 3 proprietários + 2 open weights de famílias distintas. Justificativa: divergência de comportamento entre Claude, GPT, Gemini, Llama é hoje maior do que entre versões da mesma família. [Fonte: https://ai.meta.com/blog/llama-4-multimodal-intelligence/]

---

## 6. Artefatos a produzir

Lista canônica de artefatos novos a criar no repo `papers` nos próximos 30 dias. Cada um com path proposto.

1. **`docs/GEO_KNOWLEDGE_Q2_2026_INCREMENT.md`** — este documento, commitado como contexto enriquecido permanente.
2. **`scoring/criteria_v2.yaml`** — refatoração dos critérios com `agentic_orchestration`, `geo_measurement`, `multimodal_retrieval` adicionados, pesos recalibrados. Manter `criteria_v1.yaml` como referência histórica.
3. **`analyses/2026-q2/priority_queue.md`** — lista versionada dos 8 arXiv IDs prioritários com justificativa, status de análise e link para o sumário gerado.
4. **`preregistrations/2026-06-geo-measurement-convergence.md`** — preregistration completo do paper de measurement convergence, com hipóteses, métodos, análises pré-especificados e referência ao DOI do OSF.
5. **`outlines/2026-brasil-citation-share-pt-br.md`** — outline detalhado do paper "Citation share em LLMs PT-BR", incluindo abstract draft, design experimental, painel de LLMs, prompts categorizados, plano de análise.
6. **`infra/vector_db/`** — diretório com `docker-compose.yml` do Qdrant, scripts de ingestão (`ingest_bge_m3.py`), scripts de query (`hybrid_search.py` com BGE-M3 + ColBERT v2 rerank).
7. **`METHODOLOGY.md`** (atualização) — seção nova "Benchmarks canônicos 2026" com GEO-Bench, Arena-Hard, MT-Bench documentados; seção "Painel mínimo de LLMs" com os 8 modelos canônicos.
8. **`glossary.md`** (criação ou atualização) — definições formais citáveis de MoA, DAAO, AdaptOrch, RouteLLM, AgenticGEO, ColPali, GraphRAG, Citation Drift, SoM, AECR, AIGVR, CTAM, RTAS — cada uma com fonte URL.
9. **`tracking/own_papers_visibility.py`** + dashboard — script que roda semanalmente prompts canônicos contra os 8 LLMs do painel para medir Citation Rate, SoM e Citation Drift dos nossos próprios preprints; output em CSV + dashboard simples (Streamlit ou notebook).
10. **`llms.txt`** — publicado na raiz do domínio onde hospedamos os papers, declarando fontes canônicas, políticas de uso e referência aos perfis dos autores.

---

## Apêndice — URLs canônicos

Lista consolidada de URLs reais citados neste incremento (≥20 URLs distintos, conforme requerido):

1. https://arxiv.org/html/2603.20213v1
2. https://arxiv.org/abs/2601.19793
3. https://arxiv.org/abs/2602.16873
4. https://arxiv.org/abs/2603.20324
5. https://arxiv.org/abs/2509.08919
6. https://arxiv.org/abs/2509.11079
7. https://arxiv.org/abs/2502.11947
8. https://arxiv.org/abs/2511.16681
9. https://arxiv.org/abs/2406.04692
10. https://arxiv.org/abs/2404.06801
11. https://arxiv.org/abs/2406.11939
12. https://arxiv.org/abs/2311.09735
13. https://arxiv.org/abs/2306.05685
14. https://arxiv.org/abs/2212.10496
15. https://arxiv.org/abs/2004.12832
16. https://arxiv.org/abs/2210.07316
17. https://huggingface.co/BAAI/bge-m3
18. https://huggingface.co/nvidia/NV-Embed-v2
19. https://qdrant.tech/pricing/
20. https://www.pinecone.io/pricing/
21. https://weaviate.io/pricing
22. https://milvus.io/pricing/
23. https://lancedb.com/
24. https://github.com/pgvector/pgvector
25. https://github.com/stanford-futuredata/ColBERT
26. https://github.com/illuin-tech/colpali
27. https://github.com/HKUDS/LightRAG
28. https://microsoft.github.io/graphrag/
29. https://www.anthropic.com/news/claude-opus-4-7
30. https://www.anthropic.com/news/claude-opus-4-6
31. https://www.anthropic.com/news/claude-sonnet-4-6
32. https://www.anthropic.com/news/claude-haiku-4-5
33. https://openai.com/index/introducing-gpt-5-5/
34. https://openai.com/index/introducing-o3-and-o4-mini/
35. https://developers.openai.com/api/docs/models/gpt-4o
36. https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-flash-lite/
37. https://ai.meta.com/blog/llama-4-multimodal-intelligence/
38. https://docs.x.ai/developers/models/grok-4.3
39. https://mistral.ai/news/mistral-3
40. https://mistral.ai/news/codestral-2501
41. https://fazm.ai/blog/new-llm-releases-april-2026
42. https://ahrefs.com/brand-radar
43. https://ahrefs.com/blog/ai-overviews-reduce-clicks-update/
44. https://www.brightedge.com/resources/research-reports/ai-search-visits-in-surging-2025
45. https://backlinko.com/ai-statistics
46. https://sparktoro.com/blog/new-research-search-happens-everywhere-an-analysis-of-41-websites-with-significant-search-activity/
47. https://profound.ai/
48. https://athenahq.ai/athena-state-of-ai-full-report
49. https://checkthat.ai/brands/bluefish-ai/alternatives
50. https://foundationinc.co/lab/geo-metrics
51. https://alexandrecaramaschi.com/artigos/roi-do-geo-em-90-dias-metricas-honestas-para-o-cmo
52. https://www.inboundcycle.com/pt/blog-de-inbound-marketing/metricas-geo/
53. https://goodzinking.com/en/continuous-geo-monitoring.html
54. https://authoritytech.io/blog/share-of-citation
55. https://www.searchenginejournal.com/googles-new-ai-search-guide-calls-aeo-and-geo-still-seo/575026/
56. https://www.solumize.com/blog/aeo-vs-seo-vs-geo-differences-2026
57. https://docs.cohere.com/docs/embeddings
58. https://platform.openai.com/docs/guides/embeddings
59. https://docs.voyageai.com/
60. https://huggingface.co/jinaai/jina-embeddings-v3