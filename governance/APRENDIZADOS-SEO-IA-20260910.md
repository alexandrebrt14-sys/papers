# Aprendizados de SEO e busca com IA incorporados ao papers

**Severidade:** revisão de validade conceitual e documentação científica.
**Status:** integração documental concluída; propostas de instrumentação e experimentos permanecem pendentes.
**Data:** 10/09/2026.
**Escopo:** KB, playbook, dicionário, instruções de agentes, adendo metodológico, plano do Paper 2 e rastro de pesquisa.

## O que motivou a revisão?

Alexandre solicitou ensinar ao `papers` as novidades estudadas a partir do survey da Zyppy, já integradas ao `landing-page-geo`. A transferência precisava respeitar o papel científico deste repositório: melhorar a definição e interpretação do estudo, sem otimizar seus prompts para obter mais citações.

A leitura do checkout `249f548` mostrou que ondas recentes conviviam com receitas antigas na KB e no OS. Havia recomendações universais de amostra, formatação e schema, exemplos com resultados não demonstrados e referências cuja identificação não fora revalidada. As instruções de classificação ainda exigiam cobertura de 14 eixos nos prompts experimentais.

## Qual foi o risco concreto identificado?

O vocabulário do código pode induzir uma interpretação mais forte que a observação. `absorption_status` deriva de menção; `selection_status` faz matching de nomes em URLs expostas e restringe candidatos quando há entidades mencionadas. Isso não demonstra apoio semântico de fonte nem recuperação interna.

O Paper 2 propunha ranking de entidades e comparação com Google, enquanto o módulo opcional solicita resultados ao Brave e calcula Jaccard de domínios em consultas EN. Seu outline também continha resultados preliminares e publicação de dados sem evidência apresentada, além de pareamento temporal e métricas ainda não garantidos pela instrumentação.

## O que foi corrigido?

A [onda de setembro-10](../docs/research/geo-wave-setembro-10-2026/GEO_WAVE_SETEMBRO_10_2026_CANONICAL.md) registra a matriz de compatibilidade e os estados implementado, proxy e proposta. O [guia científico](../docs/research/geo-wave-setembro-10-2026/GUIA_CONCEITOS_SEO_IA_PESQUISA.md) ensina operacionalização, denominadores, fidelidade, fan-out, amostra e causalidade.

A taxonomia ganhou os conceitos de 51 a 63 com IDs compatíveis com o [PR #514 de landing-page-geo](https://github.com/alexandrebrt14-sys/landing-page-geo/pull/514). A KB e o OS foram reconciliados; os artefatos antigos continuam no [estado anterior do Git](https://github.com/alexandrebrt14-sys/papers/tree/249f548). Não se declara falsidade de toda referência antiga: retirou-se autoridade operacional das afirmações não revalidadas.

A seção 13 da metodologia v2 esclarece a interpretação sem alterar o instrumento. O [Paper 2](../docs/outlines/PAPER_2_GEO_VS_SEO.md) passa a ser proposta compatível com Brave e domínios, com extensões explicitamente pendentes. AGENTS, CLAUDE, GEMINI e índices apontam para o conhecimento vigente. Documentos históricos recebem nota de precedência; seu conteúdo anterior é preservado.

## Como a integração foi verificada?

A apuração confrontou o texto com os arquivos de coleta, extração e migração, além das fontes primárias. O relatório original conserva 30 referências e o registro conserva 24 buscas, sem apresentar consultas antigas como novas execuções. A confirmação bibliográfica de Aggarwal e as leituras metodológicas adicionais estão identificadas no guia.

O escopo desta alteração é documental. Não houve leitura de saldo, coleta paga, alteração de chave, ingestão de GSC, sincronização do R2, recálculo de resultados ou alteração de prompts, código e dados. Progresso da série não foi medido novamente; continuam aplicáveis os cuidados dos incidentes de [31/08](HEALTH-CHECK-COLETA-20260831.md) e [08/09](HEALTH-CHECK-APIS-20260908.md).

Verificação documental local: 18 arquivos Markdown, 167 links relativos sem destino ausente, IDs de 1 a 63 sem lacunas, 30 referências e 24 consultas preservadas. Os corpos anteriores da metodologia v1, metodologia v2 e onda de setembro-03 foram conferidos como subsequência intacta das versões novas. O diff não contém alterações em código, dados, testes, workflows ou dependências; a checagem de whitespace passou.

## O que continua em aberto?

P-SEO-05 propõe validar as proxies contra referência anotada antes de usá-las para conclusões semânticas. A escolha de candidatos, o matching de URLs, a ambiguidade dos zeros e os rótulos de falha precisam de desenho e versão para eventual mudança de código.

P-SEO-01 a P-SEO-04 e o Paper 2 dependem dos contratos de dados e dos protocolos descritos na onda. Campos agregados existentes não devem ser reportados sem verificar cálculo e preenchimento. O novo relatório do Google permanece fonte externa, sem ingestão implementada aqui.

Nenhuma dessas propostas está pré-registrada ou executada por ter sido documentada. A próxima mudança de instrumento deverá declarar compatibilidade, validação e tratamento da série anterior antes da coleta.
