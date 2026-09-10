# Sistema operacional de pesquisa em SEO e busca com IA

**Revisão:** 10/09/2026. **Aplicação:** organizar investigação, análise e redação do `papers` sem modificar implicitamente o instrumento longitudinal.

Uma melhoria na documentação só melhora o estudo se o próximo pesquisador souber qual dado usar e o que pode concluir. Este playbook substitui receitas antigas de volume, resultados esperados e prompts “otimizados” por um fluxo de decisões verificáveis. A [metodologia v2](METHODOLOGY_V2.md) permanece canônica para a série; a [KB](GEO_KNOWLEDGE_BASE_2026.md) explica os conceitos e o [guia científico](research/geo-wave-setembro-10-2026/GUIA_CONCEITOS_SEO_IA_PESQUISA.md) desenvolve os desenhos novos.

## 1. Como iniciar uma tarefa?

Identificar se a tarefa é revisão de literatura, auditoria do instrumento, análise de dados existentes, redação ou desenho de novo experimento. Essa escolha define os artefatos e impede que um pedido de atualização conceitual dispare coleta paga, troque modelos ou reformule prompts.

Ler a cadeia editorial da raiz e as seções pertinentes da metodologia. Registrar o commit usado na inspeção. Para interpretar a história do dado, consultar [governance/README.md](../governance/README.md), sobretudo os incidentes sobre janela de leitura, dias parciais e banco desatualizado.

| Tipo de tarefa | Entrada mínima | Saída verificável |
|---|---|---|
| Revisão de literatura | Pergunta, recorte e fontes primárias | Registro de buscas, ficha de evidências e síntese com limites |
| Auditoria de instrumento | Versão de código, contrato e exemplos de observação | Mapa de campos, falsos positivos/negativos e propostas de correção |
| Análise do painel | Extração canônica datada e protocolo | Estimativas com denominadores, incerteza e exclusões |
| Redação de paper | Tabelas verificadas, método e referências abertas | Texto que distingue resultado, hipótese e limitação |
| Novo experimento | Estimando, mensuração, comparação e amostra | Protocolo revisável antes de coleta e implementação |

## 2. Como executar fan-out de pesquisa?

Partir da pergunta, decompor as incertezas e buscar evidências que possam confirmar ou enfraquecer a explicação inicial. Para a onda de 10/09, o [registro original](research/geo-wave-setembro-10-2026/registro-query-fan-out.md) preserva 24 consultas e o [relatório](research/geo-wave-setembro-10-2026/relatorio-seo-ia-query-fan-out.md) reúne 30 referências. Esse registro não pretende representar as subconsultas internas do Google.

Registrar consulta executada, data, fonte encontrada e motivo de inclusão ou descarte. Buscas repetidas e resultados improdutivos podem permanecer no rastro; não inventar consultas retrospectivamente para dar aparência de cobertura.

Ao abrir um paper, conferir título, autores e versão no identificador primário. Ao ler um painel de mercado, extrair janela observada, denominador, unidade, seleção e alterações de parser. Se a informação necessária não estiver disponível, reduzir o alcance da conclusão.

## 3. Como transformar a leitura em conhecimento ativo?

Classificar cada afirmação como requisito oficial, resultado experimental, associação observacional, julgamento profissional ou hipótese. Depois explicitar a decisão que ela permite no contexto do `papers`.

Uma ficha de evidência deve conter:

| Campo | Registro |
|---|---|
| Identificação | Título, autores, publicação, URL e data de acesso |
| Tempo | Data da publicação e janela dos dados |
| Escopo | Motor/produto, país, idioma, consulta, entidade, página ou URL |
| Método | Desenho, seleção, amostra, denominador e comparador |
| Resultado | Estimativa com unidade e incerteza quando informada |
| Limites | Ausências, confundimento, mudança de parser ou suporte |
| Integração | Conceitos pertinentes, arquivos afetados e estado da recomendação |

Quando uma nova fonte corrigir uma recomendação ativa, atualizar KB, dicionário e instruções de entrada. Uma nota isolada no fim de uma onda não resolve um conflito que os agentes encontram no início do trabalho. Documentos históricos recebem precedência datada; registros de governança conservam sua sequência.

## 4. Como auditar uma métrica antes de usá-la?

Seguir o caminho completo: definição documental, campo gravado, função que calcula, ponto de chamada e denominador na agregação. A [migração 0009](../src/db/migrate_0009_citation_absorption.py) criou campos de seleção, absorção e entropia; isso não demonstra que todos sejam preenchidos ou validados.

No estado inspecionado em 10/09, `absorption_status` deriva de `cited`; `selection_status` faz matching de nomes em URLs. O [guia](research/geo-wave-setembro-10-2026/GUIA_CONCEITOS_SEO_IA_PESQUISA.md) descreve a escolha de candidatos e os zeros ambíguos. Para afirmar apoio semântico, exigir material fonte, afirmação e rubrica de anotação.

Não interpretar `failure_type` como diagnóstico causal sem verificar argumentos e chamadas. Um rótulo compatível com falha de recuperação não prova que o recuperador perdeu uma página; pode faltar exposição de fontes ou captura adequada.

## 5. Como analisar a série existente?

A fonte canônica off-site é o R2, conforme o [incidente de 08/09](../governance/HEALTH-CHECK-APIS-20260908.md). Antes de uma tarefa autorizada de análise do banco, seguir o procedimento de sincronização ali documentado e verificar origem, atualização e integridade da cópia. Esta revisão documental não baixou nem recalculou a série.

Montar o recorte com provedor, modelo, endpoint/configuração relevante, versão metodológica, idioma, vertical, tipo de consulta, período, janela textual, cache e probes. Declarar o número de dias coletados e os braços presentes, sem substituir coleta efetiva por dias transcorridos.

Preservar a janela principal da seção 4.1bis da metodologia. Texto integral só pode ser usado onde foi retido; uma sensibilidade com esse material precisa declarar a mudança de população observável. Não completar períodos antigos com respostas geradas hoje.

Separar resultados por estratos que mudaram de modelo, raciocínio, endpoint ou janela. A redução de braços por crédito produz dia parcial, não ausência de menção. O novo comportamento do preflight está documentado no README e não elimina a necessidade de controlar a cobertura.

Aplicar os estimadores e a regra de decisão correspondentes à versão do protocolo. Não trocar a regra porque outra métrica tornou o resultado mais favorável. Se a análise exploratória motivar uma regra nova, registrar essa origem e planejar validação futura.

## 6. Como planejar uma medição nova?

Escolher conceitos pertinentes do dicionário e preencher a ficha do guia. O novo protocolo deve nomear o estimando, a unidade de alocação, a unidade de análise, a menor diferença relevante e o tratamento de dependência e ausências.

| Proposta | Entrega anterior à implementação | Critério de prontidão |
|---|---|---|
| P-SEO-05: validar proxies | Rubrica e amostra de positivos, negativos e desconhecidos | Seleção lexical e apoio semântico podem ser avaliados separadamente |
| P-SEO-02 / Paper 2: overlap | Contrato de SERP, fontes, idioma, unidade e pareamento | Motor e denominadores estão explícitos; campos necessários existem |
| P-SEO-03: fidelidade | Pares de conteúdo factual equivalente, com apresentações distintas | Anotador pode avaliar a resposta sem conhecer o tratamento |
| P-SEO-01: informação original | Intervenção e controles com snapshots | Conteúdo, distribuição e infraestrutura não mudam juntos sem declaração |
| P-SEO-04: persistência e fontes | Regras de independência e repetição | Republicação, cache, falha e mudança de modelo têm tratamento definido |

As propostas não têm coleta ou pré-registro concluídos por constarem nesta tabela. Uma hipótese que não pode ser medida ainda precisa de instrumentação, não de um resultado escrito de antemão.

## 7. Como lidar com GSC e outras superfícies?

O [anúncio oficial do Google](https://developers.google.com/search/blog/2026/06/gen-ai-performance-reports) registra a disponibilidade global do relatório generativo em 31/08/2026. Uma futura integração precisa conservar a extração e o contrato da [ajuda do produto](https://support.google.com/webmasters/answer/16984139).

Na leitura vigente em 10/09, a visão dedicada mede impressões; não fornece cliques, CTR, consultas nem divisão AIO/AI Mode. Não somar suas impressões às do total Web, onde já estão incluídas. Tabela por página, gráfico por propriedade e exportações limitadas não devem ser tratados como uma única série aditiva. Valores indisponíveis exportados como zero precisam manter essa condição na camada analítica.

Não existe ingestão de GSC implementada por esta atualização. Se ela for criada, distinguir disponibilidade de produto, disponibilidade na propriedade, valor observado e falha de exportação. Associar presença em API a exposição em Search exige estudo próprio; a coincidência de marca e data não resolve a atribuição.

## 8. Que rotina preserva a qualidade?

| Momento | Verificação | Decisão decorrente |
|---|---|---|
| Em cada rodada já programada | Cobertura de braços, falhas e integridade conforme pipeline | Registrar dia parcial e investigar erro; preservar o estímulo |
| Ao iniciar análise | Atualidade da base, filtros e estratos | Produzir extração datada ou interromper a conclusão sem dado |
| Na revisão de literatura | Novidade, fonte e compatibilidade metodológica | Integrar, qualificar ou manter como hipótese |
| Antes de mudar o instrumento | Efeito sobre comparabilidade e plano de validação | Nova versão e registro de método |
| Antes de redigir resultados | Tabelas, denominadores e incerteza | Escrever apenas conclusões sustentadas |
| Antes de submeter | Pré-registro verificável, dados, código e venue atual | Publicar o estado real de cada artefato |

Essa rotina não cria agendamentos novos nem redefine custos. Os workflows existentes continuam responsáveis pela execução. Preços, cotas e prazos de conferências devem ser confirmados quando a decisão depender deles.

## 9. Como escrever sem fabricar um resultado?

Abrir o paper com a pergunta e sua consequência, seguir para método e evidência, depois explicar o que o desenho não identifica. Tabelas de trabalho podem nomear colunas, mas não conter médias, intervalos ou coeficientes “esperados” que pareçam dados observados.

Para cada número, manter origem, data, método e denominador junto da afirmação. Informar tamanho de efeito e incerteza conforme o estimador. Se um intervalo for posterior, nomeá-lo como tal; se for intervalo de confiança, explicitar o procedimento.

Resultados negativos e inconclusivos fazem parte da contribuição. Não anunciar pioneirismo global, disponibilidade de dataset ou submissão concluída sem verificação. Modelos de documento, URLs de exemplo e DOIs ainda inexistentes não devem aparecer como artefatos publicados.

## 10. O que verificar ao entregar uma integração de conhecimento?

Conferir se os links resolvem, os conceitos mantêm IDs, as fontes sustentam as afirmações e o texto distingue implementação e proposta. Revisar o diff para garantir que prompts, dados e resultados não receberam alteração indireta. Executar os gates apropriados do repositório; testes verdes verificam software, não validade científica da teoria.

Registrar a decisão em governança e deixar a próxima ação vinculada a uma lacuna concreta. Nesta atualização, essa ação é validar as proxies de seleção/absorção antes de usá-las para alegações semânticas. A [onda de setembro-10](research/geo-wave-setembro-10-2026/GEO_WAVE_SETEMBRO_10_2026_CANONICAL.md) reúne os artefatos e a matriz de compatibilidade.

O [playbook anterior em 249f548](https://github.com/alexandrebrt14-sys/papers/blob/249f548/docs/GEO_OPERATING_SYSTEM.md) permanece como histórico. Seus exemplos de resultados, tabelas abstratas de banco e receitas de amostra não regem novas análises.
