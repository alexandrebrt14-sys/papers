# web_p1_papers_maio_set (Perplexity WEB Pro, https://www.perplexity.ai/search/70da8003-2132-4aae-9a50-f744bc836a94)

Nota de método: resposta do Perplexity WEB (conta alexandre.brt14@gmail.com, plano gratuito no navegador logado por CDP), usada porque a API devolveu 401 insufficient_quota. Sidebar e sugestões da interface removidos; só resposta e links.

Concluído
3 etapas

Encontrei sete preprints diretamente relevantes no intervalo de 1º de maio a 3 de setembro de 2026, todos com ID arXiv verificável na fonte primária (arXiv). Não localizei, nas fontes consultadas, trabalhos publicados nesses meses em SIGIR, KDD, ACL, EMNLP, CIKM, RecSys, WWW ou WSDM que fossem simultaneamente novos e diretamente focados em GEO/AEO.

Critério e status

Fonte primária: página oficial de resumo do arXiv, usada para verificar ID, autores, data e resultados declarados pelos autores.

Fonte secundária: não usada para confirmar metadados nesta lista; notícias e blogs foram tratados apenas como pistas, não como validação.

ID verificado na web: 7.

ID não verificado: não localizado.

Prioridade: 20 ago.–3 set.
Data	Paper e autores	Fonte e URL	Achado central com número	Método	Mudança prática para GEO
27 de agosto de 2026	“Beyond the Vacuum: Combinatorial Strategy Selection for Competitor-Aware Generative Engine Optimization” — Vaibhav Sourirajan, Yao Zhang, Himanshu Kumar, Sahil Wadhwa, Mann Patel e Amirfarrokh Iranitalab. arXiv:2608.27631	Primária: arXiv. https://arxiv.org/abs/2608.27631	O artigo declara desempenho de estado da arte em métricas de impressões no geo-bench, geo-bench_comp e transferências fora de distribuição; o resumo não informa um valor numérico específico de ganho. 
arxiv
	Formula GEO como seleção de combinações de estratégias sob concorrência; usa BOCS para buscar combinações e gera pares de preferência/raciocínios para ajustar um modelo que recomenda estratégias. 
arxiv
	Não trate cada página isoladamente: teste portfólios de intervenções e monitore adoção de táticas pelos concorrentes, pois a estratégia ótima muda quando o ambiente é saturado. 
arxiv

22 de agosto de 2026	“From Association to Causation: Improving Retrieval Precision of Retrieval-Augmented Generation via Causal Relations and an Attention Mechanism” — Jing Liu, Yongxing Qi, Muchen Jiang, Chengnan Hu, Qingqing Peng, Haoming Wang, Yuqing Wang, Yang Yu, Xu Zhang e Ting Wu. arXiv:2608.21702	Primária: arXiv. https://arxiv.org/abs/2608.21702	Em uma base empresarial de 471 documentos, uma diretriz relevante subiu da posição 6 para o top 3; no corpus diagnóstico, o ranking médio do alvo melhorou de 2,88 para 1,25, versus 2,63 do reranker cross-encoder. O gate de calibração escolheu o regime adequado com confiabilidade de pelo menos 95%, mas o método ficou abaixo da similaridade-base em três benchmarks BEIR. 
arxiv
	Reordenação sem treinamento baseada em estrutura causal do processo de recuperação: similaridade entre embedding da consulta e o centróide ponderado dos termos residuais do documento. 
arxiv
	Para conteúdo que disputa recuperação em RAG, evite inflar palavras-chave: produzir evidência específica e causalmente ligada à pergunta pode sobreviver melhor a filtros contra keyword stuffing. Operadores também devem testar reranking por tipo de corpus, não assumir benefício universal. 
arxiv

20 de agosto de 2026 — revisão v2; submetido em 17 de agosto	“GEO-Flag: Detecting and Measuring GEO-Optimized Web Content” — Junjie Chu, Ye Leng, Mingjie Li, Yun Shen, Xinyue Shen e Yang Zhang. arXiv:2608.16824v2	Primária: arXiv. https://arxiv.org/abs/2608.16824	No GEOFlagBench, a melhor baseline teve F1 agregado de 0,880; o treinamento IPT elevou o F1 do ModernBERT de 0,862 para 0,944 e a acurácia do pior grupo de 0,725 para 0,883. Em 10.095 páginas disponíveis, a prevalência estimada de GEO foi 8,90%, chegando a 16,36% nas páginas modificadas em 2026. 
arxiv
	Cria benchmark de 3.200 instâncias, 400 consultas, quatro domínios e oito famílias de otimizadores; propõe Intervention-Paired Training e auditoria de tier/verificabilidade de URLs citadas. 
arxiv
	GEO precisa ser defensável e verificável, não apenas agressivo: mantenha registro editorial, fontes rastreáveis e separação entre melhoria legítima por IA e intervenções desenhadas para manipular seleção/citação. Isso reduz risco de classificação como conteúdo GEO suspeito. 
arxiv
Fundadores de maio a agosto
Data	Paper e autores	Fonte e URL	Achado central com número	Método	Mudança prática para GEO
4 de agosto de 2026	“Training Documents Reranker with Search Rubrics for Deep Research Agent” — Wenhan Liu, Yu Lu, Qiaolin Xia, Hui Xu, Tong Zhao, Jian Xi, Yutao Zhu, Haijin Liang, Haibo Shi, Hao Wang e Zhicheng Dou. arXiv:2608.03527	Primária: arXiv. https://arxiv.org/abs/2608.03527	O RubricRanker superou a baseline mais forte em 2,6 pontos em quatro benchmarks de deep research e generalizou para cinco benchmarks de RAG. 
arxiv
	Rubricas hierárquicas produzidas por LLM especificam diversidade, concisão e autoridade do conjunto documental; o reranker é treinado em duas etapas, com ajuste supervisionado e reinforcement learning guiados pelas rubricas. 
arxiv
	Otimize páginas para contribuição complementar em um conjunto de fontes: uma página GEO deve ser concisa, específica, autoritativa e adicionar cobertura, em vez de apenas maximizar similaridade lexical com a consulta. 
arxiv

15 de julho de 2026	“Optimizing Visibility in Generative Engines: A Critical Survey of Generative Engine Optimization (2023–2026)” — Olivier Martinez. arXiv:2607.14035	Primária: arXiv. https://arxiv.org/abs/2607.14035	Revisão crítica de 45 estudos conclui que existe evidência causal estreita para alterar citação/uso quando a fonte já está no contexto, mas não há técnica que tenha demonstrado efeito causal estável, longitudinal e multiplataforma sobre descoberta orgânica ou comportamento posterior. 
arxiv
	Propõe modelo em múltiplas etapas — ativação de busca, crawling/indexação, recuperação, reranking/contexto, citação, absorção e comportamento — além de vetor de visibilidade e protocolo com repetições, paráfrases, controles e validação humana. 
arxiv
	Troque a métrica única “fui citado?” por um funil: indexabilidade, recuperação, posição/contexto, citação, fidelidade da menção e resultado econômico. Faça testes repetidos entre motores e paráfrases; promessas de “hack de GEO” não são evidência suficiente. 
arxiv

18 de junho de 2026	“Generative Engine Optimization at Scale: Measuring Brand Visibility Across AI Search Engines” — Pratyush Kumar (Ranqo). arXiv:2606.20065	Primária: arXiv. https://arxiv.org/abs/2606.20065	Em mais de 100 mil respostas e mais de 100 marcas, marcas globais apareceram em 73% das respostas relevantes na primeira medição, marcas estabelecidas em 44% e marcas nichadas em 11%. Cerca de 78% das citações foram para sites corporativos; listicles “best-of” representaram cerca de 21% das citações, e o sentimento variou 6,7 vezes mais que a simples menção. 
arxiv
	Estudo observacional de respostas rastreadas entre março e maio de 2026 em múltiplos motores; propõe sete protocolos para testar causalidade de recomendações. 
arxiv
	Para marcas pequenas, priorize construção de autoridade antes de esperar paridade de visibilidade. Fortaleça o site corporativo e acompanhe páginas de comparação/listas confiáveis, mas meça separadamente presença, citação, recomendação e sentimento por motor. 
arxiv

18 de maio de 2026	“Position: Generative Engine Optimization Creates Underexamined Risks, Governance Must Target Concentration, Disclosure, and Academic Blind Spots” — autores: não localizado na página primária recuperada. arXiv:2606.12439	Primária: arXiv. https://arxiv.org/abs/2606.12439	O artigo identifica três riscos: influência concentrada por baixa contestabilidade e sensibilidade do sistema; influência comercial não divulgada na evidência/raciocínio; e lacunas entre avaliação acadêmica e sistemas implantados. O resumo não traz métrica numérica. 
arxiv
	Trabalho de posição: formaliza o pipeline de GEO e defende governança no nível da resposta, auditoria de influência material e métricas alinhadas à implantação. 
arxiv
	Institua transparência editorial e auditoria: documente patrocínio, critérios de recomendação e mudanças de conteúdo. Para operações de marca, “ser citado” deve ser compatível com confiança, divulgação e qualidade de evidência. 
arxiv

3 de maio de 2026	“A Hybrid Retrieval and Reranking Framework for Evidence-Grounded Retrieval-Augmented Generation” — autores: não localizado na fonte primária recuperada. arXiv:2605.01664	Primária: arXiv. https://arxiv.org/abs/2605.01664	Em piloto de 25 consultas biomédicas, recuperou/reranqueou 500 trechos e avaliou 200 alegações; todas foram julgadas suportadas pela evidência recuperada, relatando 100,0% de grounding. É um resultado de pequena escala e domínio específico. 
arxiv
	Pipeline híbrido com ingestão, chunking e embeddings Titan Text Embeddings V2, índice OpenSearch Serverless, recuperação híbrida, reranking Cohere e avaliação de alegações por modelo juiz. 
arxiv
	Para GEO voltado a motores com RAG, torne cada afirmação importante fácil de extrair e sustentar por um trecho autocontido. Porém, não extrapole os 100%: o próprio desenho é piloto biomédico, com amostra limitada. 
arxiv
O que é verificável

Todos os seguintes identificadores foram verificados diretamente no arXiv: 2608.27631, 2608.21702, 2608.16824, 2608.03527, 2607.14035, 2606.20065, 2606.12439 e 2605.01664. As entradas de 2606.12439 e 2605.01664 têm o ID e a página arXiv identificados, mas os nomes completos de autores não foram localizados nos dados primários recuperados; por isso não os completei por inferência.
arxiv
+7

Não localizei, no material verificado, papers entre 20 de agosto e 3 de setembro de 2026 especificamente sobre embeddings novos para AI search ou citação por LLMs com foco direto em GEO, além dos trabalhos de recuperação, reranking, detecção e visibilidade listados acima.

16 fontes
Quais são os detalhes do paper arXiv 2608 16824 sobre detecção de GEO
Como o arXiv 2606 20065 mede a visibilidade de marcas em buscas por IA
Quais foram os achados centrais do levantamento crítico arXiv 2607 14035
Qual é o foco do paper de reranking e recuperação arXiv 2605 01664
Como o modelo BOCS é aplicado no paper arXiv 2608 27631
Fontes
16

## Links na página
- https://arxiv.org/abs/2608.27631
- https://arxiv.org/abs/2608.21702
- https://arxiv.org/abs/2608.16824
- https://arxiv.org/abs/2608.03527
- https://arxiv.org/abs/2607.14035
- https://arxiv.org/abs/2606.20065
- https://arxiv.org/abs/2606.12439
- https://arxiv.org/abs/2605.01664