# SEO e busca com IA: integração científica de 10 de setembro de 2026

**Recorte:** 10/09/2026. **Estado:** conhecimento integrado; propostas de pesquisa ainda não executadas. **Destino:** `papers`, estudo empírico de menções e fontes de empresas brasileiras.

Uma resposta pode mencionar uma empresa sem oferecer um link que sustente a afirmação. No `papers`, essa diferença aparece dentro do próprio instrumento: `absorption_status` acompanha a menção detectada, enquanto `selection_status` procura o nome normalizado em URLs. Ensinar conceitos novos exige começar por esse limite. Acrescentar treze nomes ao glossário sem esclarecer o que o coletor observa faria o vocabulário avançar mais que a validade da medição.

A integração usa a pesquisa sobre o [survey de Cyrus e Dawn Shepard, publicado em 09/09/2026](https://signal.zyppy.com/p/google-ranking-factors-expert-survey), reconciliada com documentação dos motores, estudos empíricos e o código deste repositório. A transferência parte do [PR #514 do landing-page-geo](https://github.com/alexandrebrt14-sys/landing-page-geo/pull/514). Recomendações comerciais foram convertidas em definições, limites de interpretação e propostas falsificáveis.

## Qual é a ordem de leitura?

O [guia científico](GUIA_CONCEITOS_SEO_IA_PESQUISA.md) ensina a passagem de conceito a variável e desenho de pesquisa. A [base de conhecimento](../../GEO_KNOWLEDGE_BASE_2026.md) concentra as decisões vigentes; o [sistema operacional](../../GEO_OPERATING_SYSTEM.md) organiza o trabalho verificável. O [dicionário](../../GEO_50_CONCEITOS_CANONICAL.md) preserva os IDs de 1 a 50 e acrescenta de 51 a 63, com a mesma identidade conceitual do repositório de origem.

O [relatório completo](relatorio-seo-ia-query-fan-out.md) contém 30 referências e o [registro do fan-out](registro-query-fan-out.md) preserva as 24 buscas executadas na investigação original. A confirmação bibliográfica de Aggarwal, o material de equivalência e a referência de regressão beta são leituras complementares desta adaptação, identificadas no guia; não aumentam artificialmente a contagem do fan-out original.

A [metodologia v2](../../METHODOLOGY_V2.md), incluindo os estratos e a janela de observação da seção 4.1bis, continua regendo a série. Seu novo adendo, seção 13, esclarece os construtos sem mudar prompts, extração, hipóteses H1 a H5, dados ou regra de decisão executada. Esta onda prevalece sobre recomendações conceituais anteriores que conflitem com ela; não substitui retroativamente o protocolo de uma coleta.

## O que as fontes recentes permitem concluir?

| Evidência | O que foi observado ou declarado | Consequência para o desenho científico |
|---|---|---|
| Zyppy, 09/09/2026 | 131 especialistas avaliaram 103 fatores; o artigo declara 13.665 avaliações | Opinião profissional orienta perguntas. Não estima pesos do Google, efeitos causais nem fatores de citação de IA |
| Google, guia consultado em 10/09/2026 | Fundamentos de SEO continuam relevantes; dispensa schema especial, `llms.txt` e fragmentação obrigatória para sua busca generativa | Separar requisitos documentados de hipóteses sobre efeitos; não impor esses recursos aos prompts de medição |
| Ahrefs, 02/03/2026 | Em 863 mil SERPs e cerca de quatro milhões de URLs citadas em AIO, 37,1% estavam nos dez links orgânicos principais; 37,9% considerando blocos da SERP | Declarar qual universo, unidade e parser produziram o overlap; o denominador são URLs citadas, não consultas nem marcas |
| Ahrefs, 04/02/2026 | Modelo sobre 300 mil consultas estimou CTR da primeira posição 58% menor com AIO, usando dados de dezembro de 2023 e dezembro de 2025 | Estimativa observacional contextual, não perda de tráfego universal nem resultado do `papers` |
| Seer, 24/04/2026 | Painel de 53 marcas, 5,47 milhões de consultas e 2,43 bilhões de impressões; CTR com AIO passou de 1,3% em dezembro de 2025 a 2,4% em fevereiro de 2026 | Recuperação parcial dentro de outro painel. Março é projeção; status de AIO retrospectivo e sazonalidade limitam atribuição |
| Google, anúncio de 03/06 com atualização em 31/08/2026 | Relatórios de impressões generativas disponibilizados globalmente | Nova fonte de observação externa; disponibilidade anunciada não significa ingestão implementada neste repo |

Fontes primárias da tabela: [Zyppy](https://signal.zyppy.com/p/google-ranking-factors-expert-survey), [Google: otimização](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide), [Ahrefs: overlap](https://ahrefs.com/blog/ai-overview-citations-top-10/), [Ahrefs: CTR](https://ahrefs.com/blog/ai-overviews-reduce-clicks-update/), [Seer: painel](https://www.seerinteractive.com/insights/aio-impact-on-google-ctr-2026-update) e [Google: relatório](https://developers.google.com/search/blog/2026/06/gen-ai-performance-reports). As limitações e os métodos estão desenvolvidos no relatório completo; nenhum painel comercial foi incorporado ao banco do `papers`.

## Como o conhecimento anterior foi compatibilizado?

| Orientação anterior | Decisão de 10/09 | Onde a decisão fica operável |
|---|---|---|
| Cobrir todos os 14 eixos nos prompts de validação | Classificar apenas os conceitos pertinentes; preservar o estímulo longitudinal | Dicionário, AGENTS, CLAUDE, GEMINI |
| Blocos de tamanho fixo, schema e arquivos de descoberta como motores de ganho garantido | Requisitos, escolhas editoriais e hipóteses passam a ter estados distintos | KB, conceitos 11, 13, 30, 52, 61 |
| Amostra mínima universal, coeficiente desejado e significância como meta | Dimensionar pelo estimando e dependência; aceitar efeito nulo e incerteza | KB, OS e guia |
| Convergência recente como nova regra geral de parada | Útil ao monitoramento exploratório; série confirmatória mantém regra declarada | Metodologia v2, seção 13 |
| CSR/CAR como prova das etapas internas de um motor | Proxies locais com perdas, zeros ambíguos e limites de matching | Guia e adendo metodológico |
| Overlap de Brave apresentado como top 10 do Google | Identificar motor e unidade; separar comparação futura com Google | Plano do Paper 2 |
| Tabelas exemplificativas de resultados e referências não revalidadas na KB/OS | Remover da orientação ativa; preservar versão anterior no Git | KB, OS e registro de governança |
| Banco do clone usado para medir progresso | Consultar a fonte R2 conforme governança, com extração datada | OS; nenhum novo número de progresso é afirmado aqui |

A revisão não declara falsas todas as referências antigas. Retira autoridade operacional de afirmações cuja origem, método ou aplicabilidade não foram confirmados. Para reconstruir a versão anterior da base e do playbook, consultar o [estado do repo em 249f548](https://github.com/alexandrebrt14-sys/papers/tree/249f548). Incidentes e ondas históricas permanecem disponíveis.

## O que está implementado e o que depende de novo estudo?

| Capacidade | Situação inspecionada | Limite |
|---|---|---|
| Menção por NER, versão e janela | Implementada no citation tracker | Menção na janela observada, sem inferência automática de recomendação ou sustentação |
| Seleção/absorção por observação | Heurística implementada em `failure_classifier.py` | Matching textual de URL e indicador `cited`; não revela documentos recuperados internamente |
| Colunas agregadas CSR/CAR e entropia | Presentes na migração 0009 | Existência de coluna não comprova cálculo, preenchimento ou validação; não foi identificado produtor de CSR/CAR agregado na busca em `src/` e `scripts/` |
| Texto integral e tamanho da janela | Suporte da migração 0010 | Não recupera texto perdido antes de sua implantação |
| Overlap SERP/IA | Módulo opcional, consultas EN, Brave top 10, conjuntos de domínios | Código disponível não prova coleta em produção; não mede ranking de entidades nem Google |
| Fidelidade de afirmações e independência das fontes | Proposta de anotação | Exige pares fonte/afirmação, snapshots e avaliação de concordância |
| Painel GSC generativo | Contrato externo documentado | Nenhuma integração ou leitura de propriedade foi realizada nesta atualização |
| Construtos 51 a 63 | Dicionário e desenhos propostos | Tags documentais; não são novas colunas, métricas publicadas ou fatores oficiais |

A inspeção tomou como base o checkout `249f548`. Entradas concretas: [citation tracker](../../../src/collectors/citation_tracker.py), [classificador](../../../src/collectors/failure_classifier.py), [overlap](../../../src/collectors/serp_overlap.py), [migração 0009](../../../src/db/migrate_0009_citation_absorption.py) e [configuração v2](../../../src/config_v2.py).

## Quais pesquisas podem nascer daqui?

As propostas abaixo não são pré-registros nem resultados. Seus identificadores não reutilizam H1 a H5 da metodologia v2.

| Proposta | Questão | Desfecho primário candidato | Requisito antes de executar |
|---|---|---|---|
| P-SEO-01 | Evidência original muda a chance de uso como fonte? | Proporção de respostas com afirmação sustentada pelo documento, anotada | Intervenção isolada, alocação por página ou grupo e registro de exposição |
| P-SEO-02 | Fontes sobre subtarefas ampliam a cobertura além da SERP original? | Cobertura de URLs citadas em SERPs pareadas, por motor e consulta | Captura de URLs e consultas observadas; subconsultas propostas não são fan-out interno observado |
| P-SEO-03 | Cápsulas preservam condições, população e ressalvas? | Erros de fidelidade por afirmação avaliável | Mesmo conteúdo factual nos braços, anotação cega, texto integral |
| P-SEO-04 | Fontes independentes se associam à persistência de citação? | Persistência por URL e entidade em consultas repetidas | Origem e republicações identificadas; modelo, idioma e janela controlados no desenho |
| P-SEO-05 | As proxies locais representam seleção e absorção semântica? | Precisão e sensibilidade de cada proxy contra referência anotada | Amostra estratificada incluindo negativos, desconhecidos, recusa e ambiguidade |

P-SEO-05 vem primeiro porque valida a régua usada nas demais. O [Paper 2 revisado](../../outlines/PAPER_2_GEO_VS_SEO.md) descreve a comparação possível com a instrumentação de overlap e as extensões necessárias. Nenhuma dessas propostas autoriza alterar a bateria atual para favorecer empresas, estimular citações ou ajustar a pergunta até obter significância.

## Qual decisão encerra esta integração?

O repositório passa a ensinar conceitos modernos com definições observacionais e propostas separadas do estudo em curso. A próxima mudança de instrumento deve começar pelo protocolo da P-SEO-05 e pela avaliação dos limites já identificados, com versão e critérios definidos antes da nova coleta. O [registro de governança](../../../governance/APRENDIZADOS-SEO-IA-20260910.md) fixa essa decisão e as pendências.
