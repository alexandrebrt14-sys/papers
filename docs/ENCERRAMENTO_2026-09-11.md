# Encerramento do ciclo papers em 11 de setembro de 2026

O ciclo de coleta do papers foi encerrado pelo autor em 11 de setembro de 2026, no fuso de São Paulo. O acervo existente permanece como material de pesquisa e reanálise. Novas coletas, calibrações e consultas experimentais estão bloqueadas; a meta anterior de ampliar a janela deixa de ser compromisso operacional.

A revisão empírica do BRGEO-1 mostra por que preservar o instrumento e seu histórico importa. Nas mesmas respostas, mudar a janela de texto, resolver nomes sobrepostos ou corrigir a população elegível pode alterar o indicador. O legado deste ciclo é uma auditoria dos limites de medição, com resultados descritivos e falhas documentadas que orientam o desenho de pesquisas futuras.

## Publicação e versão de referência

Alexandre Caramaschi publicou em 11/09/2026 o preprint corrigido [BRGEO-1: A longitudinal audit of entity-mention measurement in generative engines](https://zenodo.org/records/22711743), DOI [10.5281/zenodo.22711743](https://doi.org/10.5281/zenodo.22711743), com 41 páginas. Esta é a referência para as conclusões empíricas registradas aqui.

O [depósito SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7446519), DOI [10.2139/ssrn.7446519](https://doi.org/10.2139/ssrn.7446519), preserva a versão anterior de 183 páginas, intitulada *Measuring Entity Citation in Generative Engines: The BRGEO-1 Protocol and a Five-Month Field Record*. Os dois depósitos representam versões da mesma pesquisa. A disponibilidade pública do preprint não constitui revisão por periódico nem replicação independente.

O Zenodo publica o manuscrito sob CC BY 4.0. O pacote de auditoria em nível de resposta permanece sob custódia do autor e não foi publicado junto com esse preprint, conforme a declaração de disponibilidade na página 29. A licença do manuscrito não altera automaticamente a licença ou o acesso ao banco. O código permanece neste repositório.

## Os três recortes de dados

| Recorte | Período e unidade | Quantidade | Uso correto |
|---|---|---|---|
| Artigo corrigido, snapshot auditado | Respostas persistidas de 23/04 a 11/09/2026; 56 datas UTC observadas | 91.392, sendo 72.145 canônicas e 19.247 sondas | Descrever a base da revisão empírica |
| Análises históricas do artigo | Respostas anteriores a 01/09/2026 UTC; 50 datas observadas | 83.486, sendo 66.399 canônicas e 17.087 sondas | Interpretar o contraste histórico de janelas e os diagnósticos históricos |
| Dashboard operacional final | Agregado legado gerado em 11/09/2026 às 22h57 UTC | 92.064 consultas; 33.439 marcadas pelo detector legado; 56 datas registradas | Consultar o retrato operacional preservado, com suas definições históricas |

Os dois primeiros recortes estão nas páginas 7 a 13 do PDF corrigido. O terceiro vem de [data/dashboard_data.json no commit a8810be](https://github.com/alexandrebrt14-sys/papers/blob/a8810bee6896202dbd3aaa345f8cc6d16db0d065/data/dashboard_data.json). A diferença de 672 entre os totais não autoriza atribuir uma causa sem reconciliação em nível de resposta. Tampouco as contagens brutas representam observações independentes.

O [manifesto de encerramento](../data/project_status.json) registra a origem e a integridade desse agregado. Seu SHA-256 é `ea9f7926c873b82192849734b3c84c7be2117b6d44dc2c67eb8677890eff3bb4`. As páginas públicas usam uma cópia versionada desse arquivo, sem atualização por coleta. O campo de projeção de fechamento presente no JSON original é histórico e não agenda execução nem altera a data de encerramento.

## Conclusões sustentadas pelo artigo corrigido

### A janela observada muda a detecção

No contraste histórico do BRGEO-1, entre 23/04 e 31/08/2026, a presença de ao menos uma entrada elegível foi detectada em 75,73% das mesmas 7.436 respostas Perplexity usando o texto retido, contra 51,95% usando seus primeiros 200 pontos de código. A diferença de prefixo menos texto retido foi de −23,78 pontos percentuais; 1.768 respostas positivas no texto retido deixaram de ser positivas no prefixo. A comparação mantém a resposta fixa e altera somente a janela examinada (páginas 13 e 14, Tabelas 2 e 3).

Essa evidência demonstra sensibilidade do indicador ao instrumento. Ela não mede qual provedor é melhor. Nas 83.486 linhas históricas, o campo dedicado ao texto integral estava nulo; a Perplexity retinha texto maior em outro campo, enquanto as partes descartadas das outras respostas não podem ser reconstruídas a partir dos prefixos. Mesmo o texto integral retido continua sujeito ao limite de saída da API.

A extensão recente inclui 5.746 respostas canônicas de 6 a 11/09 com texto integral retido no campo dedicado. A comparação com população comum usa 272 células de consulta e data, entre 8 e 10/09, e 2.096 respostas. Primeiro são agregadas as repetições dentro de cada célula, depois cada célula recebe o mesmo peso (páginas 14 a 17). O contraste por serviço permanece um diagnóstico de janela.

### Menção lexical exige interpretação semântica própria

Na auditoria dos controles fictícios do BRGEO-1, das 16.579 respostas com marcador de nome fictício e texto, 11.195, ou 67,53%, também correspondiam à regra lexical de expressões de recusa ou indisponibilidade. O resultado abrange o recorte histórico definido no artigo; a regra identifica expressões, sem adjudicar se cada resposta é uma recusa verdadeira. O restante tampouco foi classificado como fabricação (páginas 18 e 22 a 23).

Uma entidade mencionada em uma recusa continua sendo uma menção lexical. Avaliar recomendação, apoio factual ou afirmação sobre uma organização exige definição separada e validação humana. Na mesma auditoria, `absorption_status` reproduzia `cited` em todas as 33.052 linhas preenchidas, por atribuição direta no código; esse campo não era medida independente de absorção semântica (página 19).

### Ausências e aliases mudam indicadores agregados

Na análise histórica de estabilidade do BRGEO-1, 31.372 dos 39.686 pares de datas observadas, ou 79,05%, tinham os dois conjuntos de entidades vazios. O Jaccard médio nos 8.314 pares informativos era 0,7423; atribuir similaridade um aos vazios elevava a média de todos os pares a 0,9460. A ausência compartilhada, portanto, dominava a leitura agregada de estabilidade (página 20, Figura 4).

A resolução de nomes também alterava diversidade sem mudar positividade. Em 316 respostas, Amazon e Amazon Brasil apareciam no mesmo trecho. Colapsar o par reduziu a diversidade efetiva de Shannon no varejo de 5,203 para 4,589, preservando as 3.838 respostas positivas. Esse achado separa presença binária de distribuição entre entidades (páginas 20 e 21).

### Numerador e denominador precisam representar a mesma população

A regra de serviços ativos retirava 14.208 respostas Groq do denominador canônico histórico, deixando 52.191 respostas elegíveis, mas o numerador ainda recebia suas menções. A inconsistência inflava a cobertura de 13 entradas. A correção offline reparou a elegibilidade; ela não validou o índice como medida de autoridade ou de eficácia de GEO (página 21).

O artigo também mostra que zeros compartilhados elevam correlações entre índices. Depois do reparo, a correlação de Spearman entre índice geométrico e cobertura era 0,9853 nas 66 entradas positivas e 0,9977 nas 127 entradas, incluindo 61 zeros. Concordância entre índices agregados precisa ser interpretada junto de seus componentes e de sua população.

## Falhas documentadas e mudanças de procedimento

| Falha observada | Consequência para a interpretação | Aprimoramento para outro ciclo | Evidência |
|---|---|---|---|
| Texto histórico truncado e campo integral nulo | A mensuração posterior fica limitada ao que foi retido | Preservar payload e texto capturados; versionar cada transformação e janela derivada | PDF, páginas 9 e 12 a 15 |
| Dias sem respostas persistidas | Calendário não equivale a cobertura observada | Registrar datas esperadas, datas observadas, tentativas reais e faltantes separadamente | PDF, página 13 |
| Anotações retrospectivas com horário sintético | Entradas administrativas parecem execuções observadas | Identificar proveniência administrativa e nunca usar essas linhas como telemetria de tentativas | PDF, página 13 |
| Bateria e participação de serviços variáveis | Variação temporal pode refletir mudança da população comparada | Definir células comuns e regras explícitas de elegibilidade e faltantes | PDF, página 17 |
| Marcador lexical de nome fictício tratado como falsidade | Recusa, repetição do nome e afirmação factual ficam misturadas | Validar construtos em anotação humana independente, com categoria inconclusiva | PDF, páginas 18 e 34 a 35 |
| Coluna de absorção duplicada e tabelas sem dados | Estrutura do esquema aparenta evidência que não foi medida | Documentar a medida realmente implementada; exibir ausência quando não houver observação | PDF, páginas 18 a 19 e 36 a 39 |
| Conjuntos vazios tratados como estabilidade perfeita | A média fica dominada por ausência compartilhada | Separar pares informativos, vazios e análise de sensibilidade à convenção | PDF, página 20 |
| Aliases sobrepostos e elegibilidade divergente | Diversidade e cobertura mudam sem novo dado | Versionar resolução de entidades e compartilhar a função de elegibilidade entre componentes | PDF, páginas 20 a 21 |
| Histórico operacional de restauração de banco e artefatos | Execução verde pode coexistir com perda de persistência | Verificar invariantes de continuidade e recuperação sobre cópia antes de promover um snapshot | Histórico Git e comentários dos workflows anteriores ao encerramento |

O recorte histórico continha 131 dias de calendário: 50 com respostas e 81 sem persistência. As 324 entradas administrativas `aborted`, quatro por dia ausente, foram retrospectivas, e não 324 falhas de execução diretamente observadas. Julho inteiro não tinha respostas naquele recorte. Separar essas duas fontes de tempo evita transformar anotação posterior em evidência operacional.

Os dados descrevem saídas retidas de serviços e configurações históricos. Groq e Grok representam períodos distintos; Gemini Pro e Flash exigem estratificação. Repetição de hash de prefixo não comprova cache nem identidade de respostas integrais. O projeto não mediu uma intervenção GEO atribuída, impacto comercial, recuperação interna de fontes ou sustentação semântica independente de URLs.

## Agenda proposta para novas pesquisas

Qualquer novo estudo com coleta longitudinal deverá durar **no mínimo três meses completos de calendário**, conforme a diretriz do autor. A [proposta prospectiva com controle de tokens](PROPOSTA_PESQUISA_PROSPECTIVA_2026.md) detalha métodos atualizados, sentinelas e rotação planejada, comparação por células comuns, simulação de precisão, preservação integral e orçamento antes de cada chamada. Os planos econômicos reduzem escopo ou frequência de forma explícita; não prometem a mesma informação com menos dados.

As propostas abaixo não estão agendadas, não receberam orçamento e não reabrem este projeto. Um novo ciclo precisa de escopo e autorização próprios. A prioridade favorece primeiro o reaproveitamento offline do acervo e a validação da medida, antes de contratar novas chamadas.

| Prioridade e pergunta | Desenho proposto | Critério de aceite antes de interpretar resultados |
|---|---|---|
| Primeira: implementações diferentes medem o mesmo corpus da mesma forma? | Corpus congelado com janelas, aliases, controles e regras de elegibilidade explícitos; duas implementações independentes | Toda divergência rastreável à entrada, transformação ou regra, com manifesto e testes reproduzíveis |
| Primeira: o marcador lexical distingue nome, recusa e afirmação? | Amostra estratificada de positivos e negativos, com e sem expressão de recusa; dois anotadores independentes, piloto e adjudicação | Guia de anotação congelado, categorias mistas/inconclusivas e métricas separadas por construto |
| Segunda: como a escolha de população altera comparações temporais? | Reanálise offline por células comuns, configuração, datas observadas e tratamento explícito de faltantes | Denominadores publicados por recorte e incerteza compatível com dependência por consulta e data |
| Segunda: índices acrescentam informação além de cobertura? | Comparar componentes, pesos, zeros e resolução de entidades; validar contra desfecho externo definido previamente | Ganho incremental demonstrado no desfecho escolhido, sem equiparar correlação interna a validade |
| Terceira: um painel prospectivo conserva comparabilidade? | Novo projeto com prompts e configurações versionados, política de mudanças de modelo, células compartilhadas e regra de parada | Plano registrado antes da coleta, teste de preservação integral e dimensionamento pela precisão desejada |
| Terceira: uma intervenção de conteúdo altera o desfecho definido? | Novo experimento com comparação planejada, alocação ou identificação causal defensável e medidas de resultado independentes | Hipótese, desfecho, unidade de análise, população e análise definidos antes do tratamento |

As duas primeiras propostas derivam diretamente da conclusão e do Apêndice B do preprint corrigido. Os demais desenhos desenvolvem as limitações discutidas nas páginas 23 a 28. Os critérios de aceite desta tabela são sugestões de aprimoramento, não tarefas executadas ou resultados do artigo.

## Encerramento operacional

Os workflows `daily-collect.yml`, `weekly-benchmark.yml` e `weekly-calibration.yml` foram desativados no GitHub. A revisão de código retira seus gatilhos de cron e seus corpos de coleta. Um acionamento manual futuro desses arquivos informa o encerramento e termina sem coletar.

A trava central impede novas chamadas experimentais pela CLI, API, coletores, adaptadores legados e preflight. Não existe variável de ambiente de retomada. Análises históricas, consulta, exportação e inspeção do acervo permanecem disponíveis nos comandos apropriados; elas não tornam os dados históricos equivalentes à revisão empírica sem aplicar o mesmo recorte e método.

O monitoramento FinOps e a manutenção de segurança permanecem separados da coleta. As chaves compartilhadas com outros projetos não foram revogadas. O gerador de documentação deixa de sobrescrever o estado final com metas antigas. Nenhum banco histórico foi apagado ou regravado nesta operação.

Para reutilizar o trabalho, comece pelo manuscrito corrigido e declare o recorte da análise. Uma nova pergunta científica deve nascer com sua própria medida, regra de elegibilidade e critério de encerramento.

## Fontes

- Caramaschi, Alexandre. *BRGEO-1: A longitudinal audit of entity-mention measurement in generative engines*. Preprint corrigido, 11/09/2026. [Registro e PDF no Zenodo](https://zenodo.org/records/22711743).
- Caramaschi, Alexandre. *Measuring Entity Citation in Generative Engines: The BRGEO-1 Protocol and a Five-Month Field Record*. Versão anterior, 11/09/2026. [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7446519).
- [Snapshot operacional do papers no commit a8810be](https://github.com/alexandrebrt14-sys/papers/tree/a8810bee6896202dbd3aaa345f8cc6d16db0d065), gerado em 11/09/2026.
- [Manifesto de encerramento](../data/project_status.json), com estado, fontes, recortes e integridade da cópia final.


## Aprofundamento para outro estudo

A leitura do `landing-page-geo` e a revisão adicional de fontes primárias fundamentam o [protocolo futuro baseado no site](PROTOCOLO_FUTURO_BASEADO_NO_SITE_2026.md). A proposta transforma recomendações em artefatos e critérios de avanço: coleta principal de pelo menos três meses completos, referência humana retida, orçamento com reserva transacional, resposta preservada e análise de versões. O [mapa do código](MAPA_SITE_PESQUISA_FUTURA_2026.md) separa componentes reutilizáveis de lacunas ainda não implementadas. Não foi iniciada nova coleta.
