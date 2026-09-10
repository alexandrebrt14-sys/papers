# Base de conhecimento de SEO e busca com IA para pesquisa empírica

**Revisão:** 10/09/2026. **Escopo:** definições e decisões científicas do `papers`. **Fonte do instrumento:** [metodologia v2](METHODOLOGY_V2.md). O protocolo executado e seus estratos prevalecem sobre recomendações gerais deste documento.

A base agora distingue o que o código mede, o que a documentação dos motores afirma e o que novos estudos poderiam testar. Afirmações antigas sobre ganhos universais, amostras mágicas e resultados esperados foram retiradas da orientação ativa. O [estado anterior em 249f548](https://github.com/alexandrebrt14-sys/papers/blob/249f548/docs/GEO_KNOWLEDGE_BASE_2026.md) conserva o histórico; esta revisão não declara que todas as referências antigas são falsas.

## 0. Qual pergunta governa o trabalho?

O `papers` estuda como entidades brasileiras aparecem em respostas de modelos sob condições controladas de consulta e observação. Seu objetivo científico é produzir estimativas interpretáveis, inclusive efeitos nulos e resultados inconclusivos. Melhorar a taxa de citação por reformulação de prompts seria mudar o instrumento, não melhorar sua qualidade.

A atualização de setembro conecta os [63 conceitos canônicos](GEO_50_CONCEITOS_CANONICAL.md) ao [guia de operacionalização](research/geo-wave-setembro-10-2026/GUIA_CONCEITOS_SEO_IA_PESQUISA.md). Os IDs classificam literatura e hipóteses; não são pesos de um algoritmo nem campos já implementados.

## 1. Como usar a literatura fundadora e o survey recente?

A referência fundadora confirmada é [Aggarwal et al., GEO: Generative Engine Optimization](https://arxiv.org/abs/2311.09735), aceito no KDD 2024, com versão v3 de 28/06/2024. Seu desenho deve ser examinado antes de transferir métricas ou intervenções para outro sistema. A KB anterior mantinha um DOI incompatível com essa referência; esta versão usa o identificador primário aberto.

O [survey da Zyppy, de 09/09/2026](https://signal.zyppy.com/p/google-ranking-factors-expert-survey), reúne 131 especialistas e 103 fatores. É evidência sobre julgamento profissional em ranking do Google. Os percentuais da pergunta “três fatores principais” contam participantes que escolheram uma categoria; não medem contribuição causal ao ranking. A pesquisa inspira variáveis e hipóteses, sem definir o desfecho da coleta de APIs.

A ficha de leitura de qualquer artigo deve registrar título, autores, versão, população, superfície, unidade, intervenção ou exposição, método, desfecho e limites. Links de agregadores e sínteses de LLM são caminhos de descoberta; afirmações acadêmicas remetem à publicação primária verificada.

## 2. Quais métricas o projeto pode interpretar?

| Objeto | Unidade e denominador necessários | Limite atual |
|---|---|---|
| Menção de entidade | Respostas elegíveis, por provedor, consulta e janela | O NER v2 detecta ocorrência; a janela principal é a da metodologia |
| Proeminência | Posição da menção na parte observada da resposta | Não equivale à posição em SERP nem à relevância da recomendação |
| Seleção de fonte | Correspondência em URLs expostas | Proxy local; não observa o conjunto interno recuperado |
| Absorção local | Indicador derivado de `cited` | Não valida sustentação semântica de uma afirmação |
| Overlap | Interseção e união de conjuntos explicitamente definidos | O módulo opcional usa domínios de Brave e fontes de API |
| Persistência | Presença por oportunidade repetida e comparável | Precisa distinguir execução nova, cache e falha de captura |
| Fidelidade | Pares afirmação/fonte avaliáveis | Proposta de anotação; não inferir da coluna de absorção |
| Resultado comercial | Eventos de visita ou ação com regra de atribuição | Não medido pela simples contagem de menções do painel |

O [guia científico](research/geo-wave-setembro-10-2026/GUIA_CONCEITOS_SEO_IA_PESQUISA.md) detalha falsos positivos de URL, candidatos restritos às entidades mencionadas e zeros ambíguos. A existência de colunas CSR/CAR agregadas e `semantic_entropy_drift` não comprova valores calculados ou validados.

## 3. Qual stack sustenta essas observações?

O inventário é o dos arquivos do repositório, não uma lista de ferramentas para contratar. [pyproject.toml](../pyproject.toml) e [requirements-lock.txt](../requirements-lock.txt) governam dependências; [config.py](../src/config.py) e [config_v2.py](../src/config_v2.py) definem braços, coortes e estímulos.

A extração de entidades está em [entity_extraction.py](../src/analysis/entity_extraction.py), as observações em [citation_tracker.py](../src/collectors/citation_tracker.py), as heurísticas de seleção/absorção em [failure_classifier.py](../src/collectors/failure_classifier.py), a análise de hipóteses em [hypothesis_engine.py](../src/analysis/hypothesis_engine.py) e a persistência em [client.py](../src/db/client.py). Bibliotecas instaladas não demonstram que todo método de uma publicação esteja implementado.

Conforme o [incidente de 08/09](../governance/HEALTH-CHECK-APIS-20260908.md), a base canônica fica no R2; o banco do clone é uma cópia de trabalho. Esta integração não consultou o banco remoto nem atualizou números da série.

## 4. Como comparar modelos e produtos?

Registrar provedor, produto, endpoint, modelo solicitado e devolvido, ferramentas de busca, parâmetros disponíveis, idioma, data e versão do protocolo. Um nome de interface de consumidor não identifica a configuração de uma API.

Nem todo provedor aceita os mesmos parâmetros. Fixar seed e temperatura quando disponíveis pode ajudar a controlar variação, mas não garante determinismo ou equivalência entre produtos. Não alterar parâmetros da série para satisfazer uma receita genérica.

RAG e geração paramétrica são dimensões do desenho, não sinônimos permanentes de marcas. Quando um único provedor representa uma arquitetura, a comparação também carrega diferenças desse provedor; não identifica isoladamente o efeito de RAG. Mudança de rota, modelo, raciocínio ou ferramenta exige avaliar um novo estrato, como documentado na metodologia e em [PERPLEXITY_AGENT_API.md](PERPLEXITY_AGENT_API.md).

## 5. O que RAG e fan-out permitem observar?

RAG combina recuperação e geração, mas a visibilidade de seus passos depende do sistema. Fontes expostas, documentos recuperados, trechos usados e afirmações sustentadas são conjuntos diferentes. Sem logs, não estimar “presença da marca no índice vetorial público” como se esse índice estivesse disponível.

Uma revisão de literatura pode executar fan-out investigativo com consultas registradas. Um experimento com motor comercial só chama de fan-out observado as subconsultas efetivamente expostas. Subtarefas propostas pelo pesquisador continuam um referencial externo.

Em RAG controlado, o pesquisador pode registrar corpus, consultas, recuperação e saída. A validade interna desse desenho não transforma o sistema experimental em réplica do Google. O tamanho dos blocos pertence ao sistema e à tarefa estudados, sem cota universal de palavras.

## 6. Como relacionar SEO, fontes e resultado?

Os fundamentos de busca continuam relevantes ao Google generativo segundo seu [guia oficial](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide). Isso não implica que a SERP original contenha todas as fontes possíveis de uma resposta, nem que uma citação leve a clique.

A [Ahrefs, em março de 2026](https://ahrefs.com/blog/ai-overview-citations-top-10/), comparou URLs citadas em AIO com resultados do Google; o `papers` possui um módulo de Jaccard entre domínios do Brave e fontes de APIs. São perguntas diferentes. Não transportar o número de um como baseline do outro.

CTR, citação, impressão e conversão exigem denominadores próprios. O [relatório de pesquisa](research/geo-wave-setembro-10-2026/relatorio-seo-ia-query-fan-out.md) compara Ahrefs, Seer e Pew sem tratar populações e períodos diferentes como um único efeito de IA sobre tráfego.

## 7. Arquivos de descoberta são variáveis ou requisitos?

Depende da superfície. Separar acesso por crawler, indexação, elegibilidade de snippet, inclusão em recurso generativo e treinamento. Uma configuração não responde automaticamente às outras perguntas.

Para Google Search, o guia oficial diz que `llms.txt` não ajuda nem prejudica visibilidade e ranking, pois é ignorado para esse fim. Um estudo sobre outro consumidor pode avaliar o arquivo se houver mecanismo ou uso verificável. Não presumir ganho universal nem reprovar um site pela ausência.

Robots e sitemap ajudam a investigar acesso e descoberta, mas nenhuma lista de arquivos garante que a página seja exibida. Métricas técnicas não podem ser substituídas por contagem de arquivos presentes.

## 8. Como estudar schema e E-E-A-T?

Schema pode ser uma variável de presença, validade ou coerência factual. Essas dimensões não são intercambiáveis. Uma intervenção precisa isolar a alteração de markup das mudanças em conteúdo, autoria, links e distribuição.

E-E-A-T é uma estrutura de avaliação de experiência e confiança; o Google explica que não é um fator específico de ranking em [Creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content). Um escore construído pelo pesquisador exige definição e validação; não deve receber um peso universal ou uma proporção de variância pré-fixada.

O conceito 61, Schema Authority Stack, é nome interno para organização coerente de entidades e relações. Não é markup especial exigido por Google Search. Hipóteses sobre seu efeito devem poder produzir resultado nulo.

## 9. Como proteger a pesquisa longitudinal?

A série exige versão de estímulo, janela, extrator e configuração. O texto integral preservado a partir da migração 0010 permite análises futuras, mas não recompõe o que se perdeu antes. Uma análise principal em 200 caracteres e uma sensibilidade em texto integral usam populações observáveis distintas.

Registrar dias coletados, dias parciais, braços ausentes, cache e mudanças de modelo. Não converter um dia sem coleta em taxa zero, nem somar réplicas idênticas como independentes. Relatórios de progresso precisam de banco canônico e extração datada.

A regra confirmatória segue a metodologia v2. Recomendações de convergência para monitoramento não autorizam parada opcional ou substituição retrospectiva da regra de análise.

## 10. Qual hierarquia de evidência adotar?

| Classe | Uso adequado | Limite |
|---|---|---|
| Documentação oficial | Requisitos, funcionamento público e disponibilidade de recursos | Não publica todos os pesos nem prova resultado de um site |
| Estudo com intervenção | Estimar efeito no desenho e população estudados | Tratamento composto não identifica cada componente |
| Painel observacional | Associações, distribuição, evolução e hipóteses | Seleção, sazonalidade, versão e confundimento restringem causalidade |
| Survey de especialistas | Prioridades percebidas e divergências profissionais | Opinião não é mecanismo demonstrado |
| Patente, hipótese ou teoria interna | Formular mecanismos e previsões | Existência do texto não comprova implantação |
| Material bruto de pesquisa | Rastrear descoberta e síntese | Não substitui a fonte que sustenta a afirmação |

A escolha da evidência depende da pergunta. Um documento oficial é a origem apropriada para um requisito do produto; um experimento adequado é mais informativo sobre uma intervenção específica. “Mais recente” não significa desenho melhor ou dados mais atuais.

## 11. O que muda especificamente no papers?

Os 63 conceitos passam a orientar classificação e desenho, preservando a coorte e a bateria v2. A [onda de setembro-10](research/geo-wave-setembro-10-2026/GEO_WAVE_SETEMBRO_10_2026_CANONICAL.md) apresenta cinco propostas novas, P-SEO-01 a P-SEO-05, fora das hipóteses H1 a H5. P-SEO-05 valida as proxies antes que sustentem alegações semânticas.

O [Paper 2](outlines/PAPER_2_GEO_VS_SEO.md) foi reconciliado com Brave, domínios e os campos realmente disponíveis. Seu planejamento deixa de anunciar resultados preliminares não demonstrados ou capacidades de ranking ausentes.

A contribuição brasileira deve ser expressa pelo recorte efetivamente estudado. Uma busca limitada sem resultados semelhantes não demonstra que o trabalho é o primeiro do mundo. Calendários, venues e pré-registros precisam de confirmação específica antes de serem apresentados como compromissos concluídos.

## 12. Quais erros científicos a base deixa de recomendar?

Não existe N mínimo que assegure significância, validade ou publicação. Dimensionar pelo estimando, efeito relevante, variabilidade e dependência; não usar p-valor como KPI de sucesso.

Ausência de significância não comprova equivalência. A classificação heurística de efeito provavelmente nulo da regra atual permanece com seu nome e seus limites. Estudos de equivalência precisam de margens e procedimento próprios.

Concordância entre fontes pode refletir republicação. Popularidade e citações podem compartilhar causas. Comparações entre produtos misturam arquitetura, dados, interface e políticas. “Controlar todas as variáveis” não resolve automaticamente esses problemas.

Nenhuma atualização editorial muda prompts medidos. Nenhuma correção de interpretação sobrescreve dados históricos. Exemplos de tabelas devem conter campos a preencher e definições, nunca coeficientes desejados apresentados como resultados.

## 13. Como revisar esta base?

Revisar quando uma fonte primária mudar um contrato, uma nova evidência alterar uma conclusão ou a instrumentação ganhar versão. Registrar data da publicação e janela dos dados separadamente.

A cada revisão, conferir se um conceito tem definição operacional, se a métrica citada existe e é preenchida, se o resultado corresponde ao método, se as fontes foram abertas e se limitações viajam com os números. Fazer os ajustes em KB, OS, dicionário e instruções dos agentes quando houver conflito ativo; preservar documentos históricos com nota de precedência.

A decisão desta revisão e suas pendências ficam em [APRENDIZADOS-SEO-IA-20260910.md](../governance/APRENDIZADOS-SEO-IA-20260910.md). O [sistema operacional](GEO_OPERATING_SYSTEM.md) transforma essas exigências em sequência de trabalho.
