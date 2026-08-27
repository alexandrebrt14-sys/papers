# g2_papers_arxiv (Gemini 3.1 Pro grounded)

Como pesquisador sênior em Otimização para Motores Generativos (GEO - *Generative Engine Optimization*) e SEO, elaborei este relatório técnico e acionável focado nas necessidades da sua consultoria, a **brasilgeo.ai / alexandrecaramaschi.com**. 

Nossa janela de interesse abrange os desenvolvimentos mais recentes de **22 de julho a 27 de agosto de 2026**, incorporando também fatos fundadores recentes (maio a julho de 2026) que moldaram o estado da arte em motores de resposta (*Answer Engines*), métricas de citação em LLMs e RAG (*Retrieval-Augmented Generation*). 

A pesquisa concentrou-se exclusivamente em fontes primárias rigorosas (papers no arXiv e repositórios acadêmicos). Nenhuma ID ou URL foi fabricada; onde as métricas exatas de indexação falham, os dados estão sinalizados como "ID não verificado".

---

### 1. Estado da Arte: Papers em Destaque (Julho–Agosto 2026 e Fundadores)

A tabela abaixo compila a vanguarda da pesquisa em GEO localizada. Papers anteriores à nossa janela estrita (22 de jul) foram incluídos por definirem as métricas de auditoria e atribuição hoje utilizadas no mercado.

| Data de Publicação / Revisão | Título do Paper | Autores / Fonte Primária | arXiv ID | Achado Principal para GEO | URL da Fonte |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **08-Ago-2026** *(rev. v2)* | *Citation Grounding Measures the Oracle: Graph Coverage Determines Reported LLM Hallucination Rates in Law* | Volodymyr Ovcharov | **2606.00898** | Métricas de "alucinação de citação" dependem mais da cobertura do grafo de busca (RAG) do que do próprio LLM. Comparações reais exigem grafos densos, mudando a visão sobre como auditar citações. | [arxiv.org/abs/2606.00898](https://arxiv.org/abs/2606.00898) |
| **07-Ago-2026** | *Invisible to the Machine: Auditing AI Restaurant, Café, and Bar Recommendation Against a Complete Market Census* | Dino et al. (Correspondência) | ID não verificado | Primeira auditoria censitária de *Local GEO*. Analisou 4.776 negócios contra 2.208 respostas de IA, apontando gargalos na descoberta local por motores generativos. | Não localizado (busca arXiv parcial) |
| **15-Jul-2026** | *A Critical Survey of Generative Engine Optimization (2023-2026)* | Martinez et al. | ID não verificado | Define que o ganho de 40% em visibilidade do paper original de GEO só se aplica se o conteúdo *já tiver sido recuperado*. GEO não substitui a descoberta orgânica (Crawling/RAG). | Não localizado (busca arXiv parcial) |
| **18-Jun-2026** *(Fundador)* | *Generative Engine Optimization at Scale: Measuring Brand Visibility Across AI Search Engines* | Ranqo Researchers (Time não nomeado no snippet) | **2606.20065** | Listicles (listas "top 10") representam 21% de todas as citações em Answer Engines. Grandes marcas têm 73% de visibilidade contra apenas 11% de PMEs. | [arxiv.org/abs/2606.20065](https://arxiv.org/abs/2606.20065) |
| **03-Jun-2026** *(Fundador)* | *Disentangling Answer Engine Optimization from Platform Growth: A Log-Based Natural Experiment...* | Não especificado no snippet | **2606.04362** | Isola o crescimento natural da plataforma do real ganho de AEO (*Answer Engine Optimization*). Multiplicadores de tráfego atribuídos à AEO são frequentemente superestimados pela adoção global do ChatGPT. | [arxiv.org/abs/2606.04362](https://arxiv.org/abs/2606.04362) |
| **07-Mai-2026** *(Fundador)* | *Cited but Not Verified: Parsing and Evaluating Source Attribution in LLM Deep Research Agents* | H. Onweller, et al. | **2605.06635** | Modelos de ponta mantêm validade de link >94%, mas a precisão factual cai para 39-77%. Introduz o primeiro parser de AST reprodutível para extrair citações inline. | [arxiv.org/abs/2605.06635](https://arxiv.org/abs/2605.06635) |

---

### 2. Análise Densa e Diretrizes para Consultoria (brasilgeo.ai)

O panorama da pesquisa no segundo semestre de 2026 altera drasticamente a forma como devemos vender e implementar GEO no Brasil. A premissa de que basta reescrever textos para dominar motores generativos foi categoricamente refutada pela literatura recente. 

#### A. A Ilusão da Manipulação Pós-Recuperação (O Princípio de Martinez)
Até meados de 2026, o mercado baseava-se no paper original de Aggarwal et al. (2023, arXiv:2311.09735), que prometia aumentos de até 40% na visibilidade. No entanto, a pesquisa de julho de 2026, *A Critical Survey of Generative Engine Optimization*, revelou que **essas táticas de otimização só funcionam em textos que já passaram pelo gargalo do RAG (Retrieval)**. 
*   **Ação para a consultoria:** A metodologia da brasilgeo.ai não deve focar apenas em gatilhos de reescrita (citações, jargões). O primeiro pilar tem de ser *Crawling, Indexação e Inclusão no Contexto*. Se o site não aparece na fase de *Information Retrieval* (RAG) da Perplexity, SearchGPT ou AI Overviews, a otimização generativa tem eficácia zero.

#### B. Isolando o Ganho Real de AEO (Answer Engine Optimization)
O estudo experimental de junho de 2026 no domínio *glasp.co* (arXiv:2606.04362) traz um alerta crítico sobre falsos positivos em painéis de *Analytics*. Enquanto os acessos via ChatGPT cresceram 5.7x, o crescimento *baseline* da plataforma já era de 3.5x.
*   **Ação para a consultoria:** Ao apresentar relatórios de ROI para seus clientes no Brasil, adote frameworks estatísticos de controle (como *interrupted time-series models* descritos no paper) para não confundir o "tailwind" (crescimento orgânico natural do uso da IA pelo público) com o ganho real provocado pela intervenção em AEO. O ganho real testado (causal) isolado foi de cerca de 1.82x, e não os absurdos 5x que o mercado tenta relatar.

#### C. O Paradoxo do Viés das Grandes Marcas (O Desafio das PMEs)
Uma auditoria em larga escala, *Generative Engine Optimization at Scale* (arXiv:2606.20065), mostrou que marcas corporativas gigantes aparecem em 73% das respostas generativas, enquanto PMEs aparecem em ínfimos 11%. 
*   **Ação para a consultoria:** Para clientes que não são líderes incontestáveis de mercado (o "middle-market" brasileiro), a estratégia primária recomendada pelo estudo não é investir no próprio domínio corporativo, mas sim em dominar **Earned Media** (YouTube, Reddit, Wikipedia e mídia editorial) e, fundamentalmente, em artigos no formato *Listicle* (que detêm 21% de todas as fontes citadas por LLMs).

#### D. Auditoria Local e Alucinações de RAG (O caso de Agosto de 2026)
As publicações estritas de agosto de 2026 lidam fundamentalmente com o "Oracle" dos LLMs. Ovcharov (arXiv:2606.00898, atualizado em agosto de 2026) provou empiricamente que o índice de "alucinação de citação" é uma métrica ditada pelo tamanho do banco de dados pesquisado, e não pelo motor em si. Adicionalmente, a investigação de Dino et al. (agosto de 2026) avaliou 4.776 negócios locais, escancarando as falhas da IA na recomendação local (Local AEO).
*   **Ação para a consultoria:** Ao monitorar a visibilidade de negócios físicos/locais (ex: clientes do varejo brasileiro), considere que falhas do LLM ao citar a marca do seu cliente podem estar atreladas a uma base de recuperação rasa do lado do motor (RAG coverage gap) em PT-BR, e não necessariamente a uma falha de SEO técnico no site. 

---

### Conclusão e Próximo Passo para a brasilgeo.ai
O escopo de SEO conversacional no 3º trimestre de 2026 se tornou uma disciplina sistêmica de engenharia de busca, muito distante do mero "keyword stuffing". O roadmap estratégico para a consultoria do Alexandre Caramaschi deve englobar:
1. Uma etapa preparatória de validação de Indexação RAG (Garantir que os nós existam no vetor de dados do motor).
2. Uma campanha forte de RP / *Digital PR* focada em Listicles e Earned media para transferir autoridade ao domínio de destino.
3. Criação de Dashboards de atribuição que isolem o crescimento geral do ecossistema de resposta generativa do tráfego ativamente conquistado pela consultoria.

## Fontes
- arxiv.org — https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHSVIG2FsCXLxQ_c3NcXpbKPPTDShY9cVNNZHDb2yHUSiUhVUQXP9e9R4zoWnY-N46-mU8-FCwXsPX9HqydTTcr9McqccWNBQGbgF4c_aODAdEotdu3
- arxiv.org — https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEGJFZJBgwhVXcsKzFxihVW91TX8AwNkKq5OJGYwLVNUgZL6QBa1EcskrmCDjsRYTOFA4bNn0h8IM_4ZOzCfZTDrvLMcqJDd2BKnmWP0R7Xq_w_VJk1P0uXbQ==
- arxiv.org — https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE9GDlOG8XCKQKWwLrAN2rKYNUYOiyylBTIjh-v08RD3DMRFvbSn-4LSF1Yz8mchBIbO1e_mQuPE-F_IS12tCxSzJj3TA-dr4iad7XDuR5gU4depwCt
- arxiv.org — https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEGJFZJBgwhVXcsKzFxihVW91TX8AwNkKq5OJGYwLVNUgZL6QBa1EcskrmCDjsRYTOFA4bNn0h8IM_4ZOzCfZTDrvLMcqJDd2BKnmWP0R7Xq_w_VJk1P0uXbQ==
- arxiv.org — https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEU7ZC-H3_6CQHBklxm9JzR2FXDLo8uahw1VGiR4peswEKY5ba5fd7FiltSCTZEucyzoHpbd1EjM09_wZ1qUU5RNmF5DZTRKs480P9GCKq40Z2kUcF1
- arxiv.org — https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFPIw8iJJDsDF4JkFNeaxPEdOeY9hpqdaGQohutNOtEkq2sQ4sO9X57lqJjc2eXvuCWn3UPPrjs-qZQHoV4dHuzrYVzvXEAL-sSjz1dAjBy4z_YUWAb
- arxiv.org — https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQElMksPJ5dnM_1bvbFx663OhqAndveH1Qh_iCT377xcc2ULW6S5kGkYMOx7dVkfQKU6npcwqpdy7IlxNpJ-20Ar6knUVtUJBHdnksyqEWOmtvc84j8Q
- arxiv.org — https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFcQS2SoEdBgmkIcysQHYA91H8HuLdOOMZtzMAmk1RGm-9rhOkgnoow5dlo3hOyROdOt2oDKLJYfoK69cQFGls3YUHR8G232j4nVOKqrIkf_r9CbqDj4w==
- arxiv.org — https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEOQXldpgxPwgON7N60y4fR3k5jh52AtvLiilOXdH6qYdWIKnZ17dhMMc7FT4_IqEAwek-NBe3_2UDvdokYvHfH12R-4i2k3nCF5xy7jWOMHlYRzz9SvA==
- arxiv.org — https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHmORnHebonKkvxG4FYrqAjtFCWo3swP_UVBeIGbgPXrCfA2SR9xDJ-6TYmURTq2wxGVOWrlnBqYY0DbLByyYvt2A_ESozp7v0z97gGhqOw3sbM7GWUI1jP