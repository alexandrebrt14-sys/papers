# p4_semantica_vetorial_reports_pro (Perplexity sonar-pro)

# Estado da arte prático para GEO + SEO (janela: 22/jul/2026 a 27/ago/2026)

A janela pedida está **parcialmente coberta** pelos resultados disponíveis; para vários tópicos nucleares da prática GEO/SEO, o que encontrei foi **material secundário** ou **fontes fora da janela**. Onde não localizei evidência confiável dentro do período, marco como **não localizado**. Para uma consultoria no Brasil, a leitura operacional é: **retrieval + rerank + chunking semântico + entidades estruturadas + frescor verificável** continuam sendo os pilares, mas as evidências mais concretas na janela vieram sobretudo de **novos modelos de embedding/rerank** e de **guias práticos de agências/vendors**, não de papers acadêmicos.

## 1) O que há de mais útil para GEO na prática

| Tema | Evidência prática na janela | Leitura acionável para GEO |
|---|---|---|
| **Recuperação de passagens** | Motores de resposta privilegiam trechos curtos, autoexplicativos e próximos do foco semântico do prompt; isso aparece de forma reiterada em guias de mercado, mas não encontrei paper/bench oficial na janela que quantifique o mecanismo para GEO especificamente. | Estruture páginas para “citação de passagem”: resposta direta no início, H2/H3 específicos e blocos autocontidos. |
| **Tamanho de chunk** | Várias fontes de mercado convergem para blocos curtos; encontrei recomendações entre **60–120 palavras** e **75–225 palavras**. | Para conteúdo editorial, mire em blocos de **~100–250 tokens** como padrão prático; use blocos ainda menores para FAQs e definições. |
| **Headings em forma de pergunta** | Fontes práticas de auditoria GEO recomendam H2/H3 que reflitam a intenção da busca e a formulação conversacional. | Troque rótulos vagos por headings interrogativos e específicos. |
| **Densidade de entidades** | **Não localizado** na janela com evidência primária robusta. | Em vez de “densidade”, priorize **cobertura de entidades relevantes**, coocorrência natural e desambiguação explícita. |
| **Dados estruturados** | Fontes de prática GEO tratam schema como facilitador de extração e desambiguação; não localizei métrica experimental forte na janela. | Publique schema consistente com o conteúdo visível e mantenha `dateModified` atualizado. |
| **llms.txt** | Aparece em guias práticos como camada de “agent readiness”, mas sem evidência de impacto mensurável em citações. | Trate como arquivo de acessibilidade/descoberta, não como fator de ranking/citação comprovado. |
| **Frescor** | Recomendações de mercado destacam `dateModified` visível e atualização periódica; não localizei experimento primário na janela. | Atualize páginas “money pages” e conteúdos-fundação com cadência fixa e timestamps claros. |

## 2) Como motores de პასუხra recuperam e selecionam passagens

### Padrão operacional mais consistente
| Etapa | O que acontece na prática | Implicação para GEO |
|---|---|---|
| **1. Entendimento do prompt** | O sistema infere intenção, entidades e tipo de resposta necessário. | Páginas devem nomear entidades, tarefas e desfechos com precisão. |
| **2. Recuperação inicial** | Um buscador/recuperador traz candidatos por relevância semântica e lexical. | Conteúdo precisa ser indexável, específico e com termos que coincidam com a linguagem do usuário. |
| **3. Reordenação (rerank)** | Um reranker refina a ordem dos candidatos por adequação ao prompt. | Trechos curtos, coerentes e “prontos para uso” têm mais chance de subir. |
| **4. Seleção de passagens** | O motor privilegia trechos com alta densidade de resposta e pouca ambiguidade. | Resposta direta no topo da seção aumenta chance de extração. |
| **5. Síntese/citação** | O modelo sintetiza ou cita a passagem selecionada. | Consistência factual, data, fontes e estrutura limpa importam mais que estilo persuasivo. |

### Evidência prática disponível
| Afirmação | Status na janela | Fonte nomeada | URL |
|---|---:|---|---|
| Conteúdo deve ser “answer-first” e segmentado em blocos autocontidos para facilitar extração | **Parcial** | MaxIntel | https://maxintel.org/ai-seo-guide-2026.html |
| Headings devem refletir intenção e perguntas conversacionais | **Parcial** | Tisdigitech | https://www.tisdigitech.com/blog/ai-search-visibility-audit/ |
| A estrutura semântica ajuda agentes e crawlers a entender e isolar passagens | **Parcial** | MaxIntel | https://maxintel.org/ai-seo-guide-2026.html |

## 3) Chunking: o que a evidência de mercado sugere

| Recomendação | Faixa observada | Fonte nomeada | URL | Tipo |
|---|---:|---|---|---|
| Blocos por ideia, autocontidos | 75–225 palavras / ~100–300 tokens | MaxIntel | https://maxintel.org/ai-seo-guide-2026.html | Secundária |
| Parágrafos curtos e respostas diretas no início | 40–60 palavras iniciais para responder | Tisdigitech | https://www.tisdigitech.com/blog/ai-search-visibility-audit/ | Secundária |
| Blocos compactos para extração em respostas de IA | 60–120 palavras | Tisdigitech | https://www.tisdigitech.com/blog/ai-search-visibility-audit/ | Secundária |

### Leitura crítica
| Ponto | Interpretação prática |
|---|---|
| Há convergência para “curto” | Sim: o intervalo mais repetido fica abaixo de um parágrafo tradicional de blog longo. |
| Existe consenso científico na janela | **Não localizado**. O que há são guias e auditorias operacionais. |
| Melhor prática para consultoria | Projetar conteúdo em **módulos de resposta**, não em textos longos monolíticos. |

## 4) Headings, entidades e schema: como organizar páginas para GEO

### Headings-pergunta
| Regra prática | Justificativa | Fonte nomeada | URL |
|---|---|---|---|
| Usar H2/H3 que pareçam prompts reais | Facilita correspondência entre intenção e seção | Tisdigitech | https://www.tisdigitech.com/blog/ai-search-visibility-audit/ |
| Evitar rótulos genéricos como “Visão geral” | Reduz ambiguidade na recuperação | MaxIntel | https://maxintel.org/ai-seo-guide-2026.html |

### Entidades
| Regra prática | Situação na janela | Observação |
|---|---|---|
| Nomear pessoas, produtos, lugares, datas, métricas e relações explicitamente | **Não localizado** como benchmark quantitativo | É uma inferência operacional razoável para recuperação semântica, mas não vi medida primária na janela. |
| Manter consistência de nomes e aliases | **Não localizado** | Recomenda-se especialmente para marcas e páginas com múltiplas variações de termo. |

### Dados estruturados
| Prática | Evidência na janela | Fonte nomeada | URL |
|---|---|---|---|
| Schema ajuda a leitura por sistemas e agentes | Parcial | MaxIntel | https://maxintel.org/ai-seo-guide-2026.html |
| `dateModified` visível e no schema | Parcial | MaxIntel | https://maxintel.org/ai-seo-guide-2026.html |
| FAQ/schema de artigos para trechos citáveis | Parcial | Tisdigitech | https://www.tisdigitech.com/blog/ai-search-visibility-audit/ |

## 5) Frescor: o que fazer e o que não prometer

| Item | Evidência na janela | Fonte nomeada | URL | Tipo |
|---|---|---|---|---|
| Exibir “última atualização” nas páginas importantes | Recomendado | MaxIntel | https://maxintel.org/ai-seo-guide-2026.html | Secundária |
| Atualizar `dateModified` com revisões relevantes | Recomendado | MaxIntel | https://maxintel.org/ai-seo-guide-2026.html | Secundária |
| Revisar conteúdo-fundação a cada 3 meses | Recomendado | MaxIntel | https://maxintel.org/ai-seo-guide-2026.html | Secundária |
| Provar que isso aumenta citações de IA em X% | **Não localizado** com fonte primária na janela | — | — | — |

## 6) Modelos de embedding e rerank lançados no período

> Observação importante: como você pediu **fontes primárias vs. secundárias**, abaixo priorizo **blog do vendor** e páginas oficiais; quando o único dado disponível veio de imprensa/terceiros, eu marco como **secundária**. Onde eu não consegui localizar um anúncio oficial no período, marco **não localizado**.

### 6.1 Voyage AI
| Data | Modelo | Números publicados | Fonte nomeada | URL | Tipo |
|---|---|---|---|---|---|
| 29/jul/2026 | **Voyage 4 embeddings / rerank-2.5 / rerank-2.5-lite** | `rerank-2.5` e `rerank-2.5-lite` foram descritos como novos rerankers; em material agregado apareceu ganho de **7,16%–7,94%** sobre Cohere Rerank v3.5 em 93 datasets | OpenRouter / VoyageAI | https://openrouter.ai/voyageai | Secundária |
| 13/ago/2026 | **voyage-code-4** | Primeiro **200 milhões de tokens gratuitos** | Voyage AI | https://blog.voyageai.com/2026/08/13/voyage-code-4/ | Primária |

### 6.2 Jina AI
| Data | Modelo | Números publicados | Fonte nomeada | URL | Tipo |
|---|---|---|---|---|---|
| 03/ago/2026 | **jina-reranker-v3.5** | **63.20 nDCG@10** em BEIR; **1,22× a 1,56×** mais rápido que v3; ganho de **9,6 pontos nDCG@10** em retrieval semi-estruturado | Post do fundador / anúncio do vendor | https://x.com/hxiao/status/2084290170484900268 | Secundária/primária híbrida, porém não é blog oficial |
| 05/ago/2026 | **Jina Reranker v3.5** | Resumo de desempenho e posicionamento como upgrade do v3 | MenuAgentic | https://menuagentic.com/blogs/cohere-vs-voyage-vs-jina-vs-qwen3-rerankers/ | Secundária |

### 6.3 Cohere
| Data | Modelo | Números publicados | Fonte nomeada | URL | Tipo |
|---|---|---|---|---|---|
| Jul/ago de 2026 | **Rerank 4 / Rerank 4 Pro / Rerank 4 Fast** | Não localizado anúncio oficial dentro da janela com números verificáveis | não localizado | não localizado | — |
| Jul/ago de 2026 | **Embed v4** | Não localizado anúncio oficial dentro da janela com números verificáveis | não localizado | não localizado | — |

### 6.4 OpenAI
| Data | Modelo | Números publicados | Fonte nomeada | URL | Tipo |
|---|---|---|---|---|---|
| Jul/ago de 2026 | **text-embedding-3-small / text-embedding-3-large** | Página comparativa de terceiros cita dimensões máximas e preço, mas não localizei lançamento novo na janela | TheRouter.ai | https://therouter.ai/blog/llm-api-embeddings-reranking-cross-provider-comparison/ | Secundária |
| Jul/ago de 2026 | **reranker nativo** | **Não localizado**; a fonte comparativa afirma que a OpenAI não oferece endpoint nativo de rerank | TheRouter.ai | https://therouter.ai/blog/llm-api-embeddings-reranking-cross-provider-comparison/ | Secundária |

### 6.5 Google
| Data | Modelo | Números publicados | Fonte nomeada | URL | Tipo |
|---|---|---|---|---|---|
| Jul/ago de 2026 | Embeddings / rerank Google | **Não localizado** anúncio específico na janela com números verificáveis | não localizado | não localizado | — |

### 6.6 Open-source
| Data | Modelo | Números publicados | Fonte nomeada | URL | Tipo |
|---|---|---|---|---|---|
| Jul/ago de 2026 | **Qwen3-Reranker** | Fontes secundárias citam versões **0.6B, 4B, 8B** e cobertura de **100+ idiomas** | MenuAgentic / TheRouter.ai | https://menuagentic.com/blogs/cohere-vs-voyage-vs-jina-vs-qwen3-rerankers/ | Secundária |
| Jul/ago de 2026 | **bge / mixedbread / outros open weights** | Citados em comparativos de mercado, mas sem lançamento novo confirmado na janela | Redis | https://redis.io/blog/top-reranking-models-rag-accuracy/ | Secundária |

## 7) Tabela comparativa prática: qual stack escolher para GEO

| Cenário | Melhor aposta prática | Motivo |
|---|---|---|
| **Site editorial em escala** | Blocos curtos + headings-pergunta + schema + frescor | Maximiza “passage lift” em motores de resposta. |
| **E-commerce / catálogo** | Entidades fortes + schema robusto + páginas de categoria com respostas diretas | Ajuda desambiguação de produto, marca, atributos e comparações. |
| **B2B / SaaS** | Glossário de entidades, FAQs, páginas de solução e prova social com datas | Facilita seleção de passagens para perguntas de intenção comercial. |
| **Conteúdo técnico** | Chunking mais rigoroso, tabelas e definição de termos | Reduz ambiguidade e melhora citação de trechos exatos. |

## 8) Relatórios e dashboards de GEO + SEO usados por agências e vendors

### 8.1 Estruturas de relatório encontradas
| Estrutura | O que mede | Fonte nomeada | URL | Tipo |
|---|---|---|---|---|
| **Share of Voice, citation rate, recommendation rank** | Visibilidade e presença em respostas | SubscribePR | https://subscribepr.com/blog/geo-reporting-for-clients/ | Secundária |
| **Auditoria de visibilidade em IA** | Checklist de estrutura, resposta, entidades e freshness | Tisdigitech | https://www.tisdigitech.com/blog/ai-search-visibility-audit/ | Secundária |
| **Cobertura de embedding/rerank como camada de infraestrutura** | Escolha de modelo e custo/latência | TheRouter.ai / OpenRouter | https://therouter.ai/blog/llm-api-embeddings-reranking-cross-provider-comparison/ | Secundária |

### 8.2 Modelo de dashboard recomendado para consultoria
| Bloco do dashboard | Métrica | Frequência | Como apresentar incerteza |
|---|---|---|---|
| **Visibilidade GEO** | share of voice por prompt-cluster | semanal | Mostrar faixa e amostra de prompts usada |
| **Citação** | taxa de citação por domínio/página | semanal ou quinzenal | Informar cobertura de queries e variação por cluster |
| **Rank de recomendação** | posição média do cliente na resposta | semanal | Exibir mediana e dispersão |
| **Cobertura de entidades** | entidades críticas presentes nas páginas | mensal | Marcar “coberto / parcial / ausente” |
| **Frescor** | páginas com `dateModified` recente | mensal | Separar conteúdo evergreen de páginas sensíveis a tempo |
| **RAG readiness** | chunks, headings, schema, canonicalização | mensal | Usar checklist com status e prioridade |

### 8.3 Como apresentar incerteza ao cliente
| Recomendação | Formulação prática |
|---|---|
| Evitar prometer causalidade direta | “Observamos correlação entre a nova estrutura e aumento de citação, mas a amostra ainda é limitada.” |
| Sempre declarar o conjunto de prompts | “Resultados derivados de X prompts, Y clusters e Z marcas concorrentes.” |
| Exibir variação temporal | “A métrica oscilou entre A e B nas últimas 4 semanas.” |
| Separar dado observado de inferência | “A página foi citada; inferimos que o chunking contribuiu, mas não isolamos o efeito.” |

## 9) O que eu recomendaria para a sua consultoria no Brasil

| Prioridade | Ação | Impacto esperado |
|---|---|---|
| **Alta** | Reescrever páginas críticas em blocos de resposta de 60–180 palavras, com resposta direta no topo | Aumenta extração por motores de resposta |
| **Alta** | Transformar H2/H3 em perguntas e intenções reais | Melhora alinhamento com prompts |
| **Alta** | Fortalecer schema e `dateModified` | Ajuda desambiguação e frescor |
| **Alta** | Criar dashboard com share of voice, citation rate e recommendation rank | Mostra valor executivo para cliente |
| **Média** | Construir taxonomia de entidades do cliente | Melhora cobertura semântica |
| **Média** | Publicar llms.txt apenas como sinal de organização | Útil como higiene de ecossistema, não como milagre |
| **Baixa** | Buscar “densidade ideal” de entidades como número fixo | Não há evidência robusta suficiente na janela |

## 10) Lacunas importantes da janela

| Tema solicitado | Status |
|---|---|
| Paper primário de julho-agosto/2026 sobre chunk size ideal para GEO | **não localizado** |
| Estudo primário na janela sobre headings-pergunta vs. headings neutros | **não localizado** |
| Evidência quantitativa primária sobre densidade de entidades | **não localizado** |
| Bench oficial de Google/OpenAI/Cohere com números novos na janela | **não localizado** para Google e OpenAI; **parcial** para Cohere |
| Exemplos públicos de dashboard GEO de grandes vendors com URL e métricas completas | **parcial**; material mais claro veio de agências e posts de mercado |

Se você quiser, no próximo passo eu posso transformar isso em um **playbook operacional para alexandrecaramaschi.com / brasilgeo.ai**, com:

- arquitetura de páginas,
- checklist de publicação,
- template de relatório mensal,
- e modelo de dashboard em tabela pronto para cliente.

## Fontes
- https://menuagentic.com/blogs/cohere-vs-voyage-vs-jina-vs-qwen3-rerankers/
- https://x.com/OpenRouter/status/2082592473306800199
- https://blog.voyageai.com/2026/08/13/voyage-code-4/
- https://x.com/OpenRouter/status/2082592437923610988
- https://devtoollab.com/blog/best-embedding-models-apis
- https://github.com/garrytan/gbrain/blob/master/docs/integrations/embedding-providers.md
- https://openrouter.ai/voyageai
- https://www.linkedin.com/posts/lopezarmando_production-ai-succeeds-or-fails-on-retrieval-activity-7487859267744452608-tzty
- https://subscribepr.com/blog/geo-reporting-for-clients/
- https://maxintel.org/ai-seo-guide-2026.html
- https://x.com/hxiao/status/2084290170484900268
- https://explainx.ai/blog/top-10-open-closed-source-embedding-models-2026
- https://www.tisdigitech.com/blog/ai-search-visibility-audit/
- https://redis.io/blog/top-reranking-models-rag-accuracy/
- https://therouter.ai/blog/llm-api-embeddings-reranking-cross-provider-comparison/