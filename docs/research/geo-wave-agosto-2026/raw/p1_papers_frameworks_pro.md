# p1_papers_frameworks_pro (Perplexity sonar-pro)

# Escopo e limite desta resposta

Com os dados já coletados, **há poucos papers diretamente sobre GEO/AEO/citação por LLMs publicados entre 22/jul/2026 e 27/ago/2026**; o que apareceu com força foi **RAG, recuperação, reranking e infraestrutura para motores de პასუხa**, além de **um paper explicitamente sobre GEO**. Onde não houve confirmação suficiente, marco como **“não localizado”**.

## 1) Papers acadêmicos relevantes no período

### 1.1 Lista executiva

| Data | Paper | Tipo | ArXiv ID real | Fonte nomeada | URL | Relevância GEO/AEO |
|---|---|---:|---|---|---|---|
| 17/08/2026 | **GEO-Flag: Detecting and Measuring GEO-Optimized Web Content** | Primária | **2608.16824** | arXiv | https://arxiv.org/abs/2608.16824v1?ref | **Diretamente GEO** |
| 14/08/2026 | **How retriever redundancy and diversity impact RAG effectiveness** | Primária | **2608.13956** | arXiv | https://arxiv.org/abs/2608.13956 | RAG/recuperação para resposta |
| 13/08/2026 | **GEM: A Generative Embedding Model Bridging Reasoning ...** | Primária | **2608.13200** | arXiv | não localizado | Recuperação semântica para motores de resposta |
| 12/08/2026 | **EnterpriseRAG: Benchmarking LLM Instruction Adherence ...** | Primária | **2608.11584** | arXiv | https://arxiv.org/html/2608.11584 | RAG empresarial / aderência a instruções |
| 11/08/2026 | **Self-Knowledge Retrieval Augmented Generation Framework for Patent Matching** | Primária | **2608.11030** | arXiv | https://arxiv.org/abs/2608.11030 | RAG especializado |
| 04/08/2026 | **RAG-Stack: Co-Optimizing RAG Serving Performance and Quality** | Primária | **2608.03487** | arXiv | https://arxiv.org/abs/2608.03487 | Execução/infra de RAG |
| 04/08/2026 | **Training Documents Reranker with Search Rubrics for Deep Research Agent** | Primária | **2608.03527** | arXiv | https://arxiv.org/abs/2608.03527 | Reranking para agentes de pesquisa |
| 04/08/2026 | **Lightweight Chunk Selection for Mobile Retrieval-Augmented Generation** | Primária | **2608.03148** | arXiv | https://arxiv.org/abs/2608.03148v1 | Recuperação leve/edge |
| 03/08/2026 | **Before Reasoning Can Fail: Pre-Evidence Procedural Failures in Agentic RAG** | Primária | **2608.02011** | arXiv | https://arxiv.org/abs/2608.02011 | Falhas em RAG agentic |
| 02/08/2026 | **From Cloud to Crowd: Democratizing LLM Service with Decentralized Edge Collaboration for RAG** | Primária | **2608.00922** | arXiv | https://arxiv.org/abs/2608.00922 | Arquitetura distribuída para RAG |
| 01/08/2026 | **A Triple-Robustness Analysis of Retrieval-Augmented Generation for Multi-Hop Requirements Traceability** | Primária | **2608.00705** | arXiv | https://arxiv.org/abs/2608.00705 | Robustez em RAG |
| 01/08/2026 | **Select-And-Extract: A Lightweight Plugin for Retrieval-Augmented Generation** | Primária | **2608.00658** | arXiv | https://arxiv.org/abs/2608.00658 | Plugin leve para RAG |

## 1.2 Papers com mais utilidade prática para GEO

| Paper | Achado central com número | Método | O que muda na prática |
|---|---|---|---|
| **GEO-Flag: Detecting and Measuring GEO-Optimized Web Content** | **Não localizado** no snippet um número principal confiável; o paper é explicitamente sobre detecção e mensuração de conteúdo otimizado para GEO. | **Não localizado** no snippet. | É o paper mais diretamente acionável para **auditoria de conteúdo GEO**; vale como base para classificar páginas, padrões de escrita e risco de otimização excessiva. |
| **How retriever redundancy and diversity impact RAG effectiveness** | **Não localizado** no snippet um número principal confiável. | Estudo do efeito de **redundância e diversidade do retriever** sobre a eficácia de RAG. | Em consultoria, isso reforça que **ganhar cobertura de fontes e variedade de evidência** tende a importar mais do que “mais resultados” do mesmo tipo. |
| **RAG-Stack: Co-Optimizing RAG Serving Performance and Quality** | O snippet informa que, com o mesmo número de iterações, o Pareto frontier cobriu **52,5% a 153,2% mais** do espaço qualidade-desempenho que métodos SOTA. | **Busca de configuração/Pareto frontier** em espaço de design RAG. | Para operação de GEO/RAG, isso sugere um framework de **otimização sistemática** de custo, latência e qualidade em vez de ajustes ad hoc. |
| **Training Documents Reranker with Search Rubrics for Deep Research Agent** | O snippet informa ganho de **2,6 pontos** sobre o baseline mais forte em quatro benchmarks de deep research e boa generalização a cinco benchmarks RAG. | Treinamento de reranker com **rubricas de busca**. | É útil para desenhar pipelines onde **critérios editoriais de busca** viram sinais de treinamento/avaliação. |
| **Lightweight Chunk Selection for Mobile Retrieval-Augmented Generation** | **Não localizado** número principal confiável no snippet. | Seleção leve de chunks para RAG mobile. | Reforça a necessidade de **chunking e seleção de contexto** para ambientes com restrições fortes de memória/latência. |
| **EnterpriseRAG: Benchmarking LLM Instruction Adherence ...** | **Não localizado** número principal confiável no snippet. | Benchmark de aderência a instruções em contexto enterprise. | Importante para GEO corporativo: **responder corretamente ao briefing** é tão crítico quanto a recuperação. |

## 1.3 O que é verdadeiramente “GEO” vs. só “RAG”

| Categoria | Status no período | Interpretação para a consultoria |
|---|---|---|
| **GEO/AEO explícito** | **Pouquíssimo localizado**; o destaque foi **GEO-Flag** | O campo ainda está em consolidação acadêmica. |
| **Citação por LLMs** | **Não localizado** em paper com evidência forte no snippet deste recorte | Faltou, nesta amostra, paper específico sobre “LLM citation” com números diretamente citáveis. |
| **RAG / recuperação para answer engines** | **Muito forte** | É aqui que estão os métodos acionáveis hoje para GEO prático no Brasil. |

---

# 2) Frameworks de **execução** de trabalhos de GEO

## 2.1 Frameworks localizados no período

| Framework / origem | Data | Fonte nomeada | URL | Tipo de fonte | Estrutura / cadência |
|---|---|---|---|---|---|
| **RAG-Stack** | 04/08/2026 | arXiv | https://arxiv.org/abs/2608.03487 | Primária | Co-otimização de **qualidade + desempenho** por busca de configurações e fronteira de Pareto. |
| **RubricRanker / search rubrics** | 04/08/2026 | arXiv | https://arxiv.org/abs/2608.03527 | Primária | Usa **rubricas de busca** para treinar e avaliar reranker. |
| **GEO monitoring dashboard** | 05/08/2026 | HG Insights / TrustRadius / Conductor | não localizado | Secundária | Views de monitoramento por produto, categoria e crawler analytics. |
| **AEO playbook mensal com query rotation** | 03/08/2026 | CMO Magazine | não localizado | Secundária | Rodar **20 a 30 queries por mês** em ChatGPT, Perplexity e AI Overviews e registrar presença/citação. |
| **AEO tracker com prompts agendados** | 07/08/2026 | AirankLab | não localizado | Secundária | Executar prompts em agenda e reportar share ao longo do tempo. |
| **Relatório mensal de GEO com cinco métricas** | 20/08/2026 | Allegiant Digital | não localizado | Secundária | Uma página, leitura mensal, com sinais vitais de AI referral, citation rate, share of citation, pipeline e custo por oportunidade. |

## 2.2 Framework operacional recomendado para GEO no Brasil, derivado do material encontrado

| Etapa | Cadência | Papéis | Entregável |
|---|---|---|---|
| **1. Definição de universo de prompts** | Semanal no início; mensal depois | Estrategista GEO + SEO lead + especialista de mercado | Lista canônica de perguntas por cluster, persona e intenção. |
| **2. Coleta multi-engine** | Semanal para tracking; mensal para client report | Analista GEO | Capturas em ChatGPT, Perplexity, AI Overviews e outros motores observados. |
| **3. Auditoria de citação e menção** | Semanal | Analista de conteúdo + PR digital | Mapa de presença, ausência, citações e concorrentes. |
| **4. Ajuste de conteúdo e entidades** | Quinzenal | SEO técnico + redator + SME | Páginas revisadas para resposta direta, entidade, evidência e estrutura citável. |
| **5. Teste de fonte e recuperação** | Quinzenal | Técnico de dados / engenharia de busca | Validação de chunking, snippetability, schema, crawlability e acesso das fontes. |
| **6. Revisão executiva** | Mensal | Consultor sênior + cliente | Relatório com tendência, mudanças e ações priorizadas. |

## 2.3 Cadência prática recomendada para consultoria

| Frequência | Ação | Objetivo |
|---|---|---|
| Diária ou contínua | Monitoramento de anomalias em citações/menções | Detectar quedas ou picos bruscos. |
| Semanal | Rodada fixa de prompts e comparação com concorrentes | Manter série temporal confiável. |
| Quinzenal | Ajustes de conteúdo e páginas-fonte | Capturar ganhos rápidos. |
| Mensal | Report executivo e atribuição | Mostrar progresso comercial. |
| Trimestral | Rebase de prompts, concorrentes e clusters | Evitar métricas obsoletas. |

---

# 3) Frameworks de **medição** e **report**

## 3.1 KPIs localizados

| KPI | Status | Fonte nomeada | URL | Tipo de fonte | Observação prática |
|---|---|---|---|---|---|
| **Citation rate** | **Consenso emergente** | CMO Magazine; AEO.how; Subscribe PR | não localizado | Secundária | Métrica mais repetida: percentual de prompts em que a marca é citada. |
| **Share of AI citations / share of citation** | **Consenso emergente** | AEO.how; Allegiant Digital | não localizado | Secundária | Mede participação relativa entre concorrentes. |
| **AI referral traffic** | **Consenso emergente** | Allegiant Digital; NisonCo | não localizado | Secundária | Útil, mas incompleto sem contexto de assistência. |
| **Branded search lift** | **Consenso emergente** | NisonCo; AEO.how | não localizado | Secundária | Indicador indireto de efeito de exposição em AI. |
| **Assisted pipeline contribution** | **Consenso emergente para B2B** | NisonCo; Allegiant Digital | não localizado | Secundária | Bom para reporting executivo, fraco para causalidade pura. |
| **Mention rate** | **Usado, mas menos robusto** | Refine AI; Citlyze | não localizado | Secundária | Ajuda em visibilidade, mas não equivale a citação. |
| **Sentiment** | **Uso crescente, mas não consenso** | Refine AI; HG Insights | não localizado | Secundária | Pode ser enganoso em low-sample e em respostas híbridas. |
| **Answer accuracy** | **Uso crescente, mas não consenso** | Refine AI | não localizado | Secundária | Bom para qualidade, difícil de padronizar entre motores. |
| **Position in answer** | **Uso crescente, mas não consenso** | Citlyze | não localizado | Secundária | Relevante, mas varia muito por engine e contexto. |

## 3.2 KPIs que viraram consenso

| KPI | Status | Por quê |
|---|---|---|
| **Citation rate** | **Consenso** | É o indicador mais replicado e mais alinhado ao objetivo de GEO: ser citado pela resposta. |
| **Share of citation / share of AI citations** | **Consenso** | Permite benchmark competitivo e leitura de mercado. |
| **AI referral traffic** | **Consenso parcial** | Importante, mas insuficiente sozinho. |
| **Branded search lift** | **Consenso parcial** | Bom como efeito colateral, não como KPI único. |
| **Assisted pipeline** | **Consenso parcial em B2B** | Útil para negócio, mas depende muito de atribuição. |

## 3.3 KPIs desmentidos ou enfraquecidos no período

| KPI / hipótese | Situação | Leitura prática |
|---|---|---|
| **CTR tradicional como métrica principal de GEO/AEO** | **Enfraquecido** | Vários materiais do período tratam cliques de AI answers como subcontados ou incompletos. |
| **Ranking orgânico como proxy suficiente para citação em LLM** | **Enfraquecido** | Estar bem posicionado não garante ser citado no answer engine. |
| **Uma única métrica de visibilidade** | **Desmentido na prática** | Os materiais convergem para um conjunto de sinais, não para um único score. |
| **Sentiment isolado como prova de impacto** | **Enfraquecido** | Sentimento sem base amostral e sem contexto de citação é frágil. |

## 3.4 Estrutura de relatório mensal recomendada para cliente

| Bloco | Conteúdo |
|---|---|
| **1. Resumo executivo** | O que melhorou, o que piorou, quais motores mudaram. |
| **2. Cobertura de prompts** | Universo monitorado, engines, frequência e comparabilidade. |
| **3. Citação e share of voice** | Citation rate, share of citation, concorrentes. |
| **4. Tráfego e negócio** | AI referral, branded lift, leads assistidos, pipeline assistido. |
| **5. Diagnóstico de causa** | Conteúdo, entidades, schema, cobertura, crawlability, recuperação. |
| **6. Plano de ação** | Prioridades do próximo ciclo, com owner e prazo. |

---

# 4) Leitura crítica para GEO no Brasil

## 4.1 O que os papers sugerem de forma acionável

| Insight | Implicação prática |
|---|---|
| Diversidade e redundância de recuperador afetam eficácia do RAG | Não basta indexar mais; é preciso **melhorar variedade de fontes e cobertura de evidência**. |
| Co-otimização qualidade-desempenho é central | GEO precisa equilibrar **latência, custo e qualidade**, não só “precisão”. |
| Reranking por rubricas melhora deep research | Transforme briefings editoriais em **critérios de ranking e avaliação**. |
| Falhas podem ocorrer antes do raciocínio | Muitos problemas de GEO são de **pipeline**, não de geração final. |

## 4.2 O que eu recomendaria para alexandrecaramaschi.com / brasilgeo.ai

| Prioridade | Ação |
|---|---|
| **Alta** | Criar um framework próprio de **citation rate + share of citation + AI referral + branded lift**. |
| **Alta** | Montar um **prompt universe brasileiro** por segmento e intenção de compra. |
| **Alta** | Publicar páginas com **resposta direta, dados, autoria, datas e fontes** para aumentar citabilidade. |
| **Média** | Implementar **dashboards de monitoramento por engine** e por concorrente. |
| **Média** | Padronizar **relatório mensal de GEO** para clientes com foco executivo. |
| **Média** | Tratar **rankings clássicos** como sinal auxiliar, não como KPI principal. |

Se você quiser, eu posso converter isso em um **deliverable de consultoria pronto para cliente** com:
- matriz de priorização por setor,
- template de dashboard,
- modelo de relatório mensal em português,
- e checklist de execução GEO para 30/60/90 dias.

## Fontes
- https://arxiv.org/abs/2608.11030
- https://arxiv.org/abs/2608.03148v1
- https://arxiv.org/abs/2608.13956
- https://arxiv.org/abs/2608.03487
- https://arxiv.org/abs/2608.00922
- https://arxiv.org/abs/2608.14886
- https://arxiv.org/abs/2608.01311
- https://arxiv.org/abs/2608.16824v1?ref
- https://arxiv.org/abs/2608.03527
- https://arxiv.org/abs/2608.02011
- https://arxiv.org/abs/2608.00705
- https://arxiv.org/abs/2608.00658
- https://redmonk.com/kholterhoff/2026/08/24/ax-v-geo/
- https://papers.cool/arxiv/2608.13200
- https://arxiv.org/html/2608.11584
- https://cmomag.com/ai-in-marketing/answer-engine-optimization-playbook-2026
- https://nisonco.com/how-to-measure-generative-engine-optimization-success/
- https://www.citlyze.com/blog/best-geo-tools
- https://aeo.how/blog/aeo-roi-tracking-a-new-model-for-ai-search-pipeline-attribution
- https://aeo.how/blog/measuring-ai-search-roi-with-4-kpis-that-move-revenue
- https://getrefine.ai/blog
- https://subscribepr.com/blog/how-to-measure-an-aeo-agency/
- https://hginsights.com/blog/hg-insights-launches-geo-monitoring-dashboard/
- https://mustacheaeo.com/aeo-case-studies-proving-the-roi-of-answer-engine-optimization-in-2026/
- https://www.gtm8020.com/blog/answer-engine-optimization-companies
- https://www.mtsoln.com/en/services/geo-audit/transparency/
- https://allegiantdigital.com/ai-seo-agency/ai-seo-investment-roi-framework/
- https://pagelens.ai/blog
- https://www.airanklab.com/blog/aeo-tracker-complete-guide
- https://nicklafferty.com/blog/best-aeo-geo-tools-for-marketers-2026/