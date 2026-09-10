# Paper 2: divergência entre fontes de respostas de IA e resultados de busca

**Revisão:** 10/09/2026. **Estado:** proposta de estudo, sem novos resultados ou coleta executada nesta revisão. **Responsável:** Alexandre Caramaschi. **Versão anterior:** [outline de abril no estado 249f548](https://github.com/alexandrebrt14-sys/papers/blob/249f548/docs/outlines/PAPER_2_GEO_VS_SEO.md).

O módulo disponível compara domínios de fontes expostas por APIs com domínios retornados pelo Brave. Esse recorte pode produzir uma contribuição útil se for apresentado pelo que observa. O título alternativo antigo sobre top 10 do Google, as alegações de resultados preliminares e os dados supostamente publicados foram retirados porque não são demonstrados por esse módulo.

## 1. Qual é a pergunta do estudo?

**Título de trabalho:** “Sobreposição de domínios entre Brave Search e fontes expostas por APIs de modelos: desenho de um painel multivertical”.

Pergunta principal: entre consultas para as quais ambos os conjuntos são observáveis, quanto os domínios de fontes de uma resposta coincidem com os domínios dos dez resultados solicitados ao Brave? A palavra “observáveis” exige verificar o que o provedor realmente expõe; ausência de lista não pode ser tratada automaticamente como ausência de fonte interna.

A comparação com Google é uma possível extensão independente. Exigiria fonte de SERP, localidade, dispositivo, horário e parser específicos, além de coleta autorizada e contrato de dados verificado. Brave não é uma amostra intercambiável do índice do Google.

## 2. O que já existe no código?

| Capacidade | Estado inspecionado em 10/09 |
|---|---|
| Cliente de busca | `BraveSearchClient` importado de [base.py](../../src/collectors/base.py) |
| Coletor de overlap | [serp_overlap.py](../../src/collectors/serp_overlap.py) |
| Ativação | Condicionada a `ENABLE_SERP_OVERLAP=true` e chave de busca; esta revisão não alterou o toggle |
| Idioma | O coletor seleciona somente consultas com `lang == "en"` |
| SERP | Solicita dez resultados e forma conjunto de domínios não vazios |
| IA | Consulta os modelos configurados e forma conjunto de domínios a partir de `response.sources` |
| Métrica | Jaccard de domínios em `overlap_pct`, multiplicado por cem e arredondado |
| Outros campos | Contagens e listas de domínios comuns, exclusivos da SERP e exclusivos da IA |
| Posição e entidade | Não preserva um ranking pareado de entidades ou URLs no resultado do módulo |
| Pareamento | Busca e chamadas aos modelos são sequenciais; não há verificação de diferença máxima entre timestamps de SERP e resposta no registro produzido |

Disponibilidade do código não comprova ativação ou cobertura de produção. O módulo não deve ser ligado apenas para validar esta documentação. Antes de planejar a coleta, confirmar o estado operacional, a proveniência das fontes, o esquema persistido e o orçamento em uma tarefa específica.

## 3. Quais perguntas e hipóteses são candidatas?

Os IDs P2 abaixo pertencem a este outline. Não substituem H1 a H5 da metodologia longitudinal.

| ID | Pergunta ou previsão candidata | Situação |
|---|---|---|
| P2-RQ1 | Como o overlap varia por consulta, vertical e configuração de API? | Descrição principal possível após auditoria dos campos |
| P2-RQ2 | Quanto da diferença resulta de fontes não expostas, conjuntos vazios ou normalização? | Sensibilidade obrigatória de observabilidade |
| P2-H1 | Há associação entre provedor/configuração e cobertura de domínios | Hipótese a operacionalizar e dimensionar |
| P2-H2 | A sobreposição de uma consulta muda ao longo de versões e datas? | Requer painel repetido e registro de configuração |
| P2-H3 | A cobertura aumenta quando o referencial inclui subtarefas explicitamente definidas? | Extensão ligada a P-SEO-02; requer coleta nova |

Não há limiar universal de Jaccard que demonstre “divergência relevante”. Definir a diferença de interesse e a comparação nula antes da análise. RAG não pode ser considerado causa isolada se a arquitetura estiver confundida com um único provedor.

## 4. Como definir unidades e métricas?

Para uma oportunidade pareada, S é o conjunto de domínios dos resultados do Brave; L é o conjunto de domínios de fontes expostas pela resposta. Fixar regras para subdomínios, redirecionamentos, URLs inválidas, provedores agregadores e identidade institucional antes de analisar.

| Métrica candidata | Definição | Condição |
|---|---|---|
| Jaccard | tamanho da interseção dividido pelo tamanho da união | União não vazia |
| Cobertura das fontes de IA | tamanho da interseção dividido por tamanho de L | L não vazio e lista observável |
| Deslocamento | tamanho de L fora de S dividido por tamanho de L | Mesmo denominador da cobertura |
| Persistência | Presença do domínio em oportunidades repetidas comparáveis | Distinguir cache, falha e execução nova |
| Disponibilidade | Oportunidades com fontes efetivamente observáveis por superfície | Não confundir lista vazia e recurso não exposto |

O módulo atual devolve zero quando ambos os conjuntos estão vazios por usar denominador mínimo um. Preservar o bruto e propor uma camada analítica que trate esse caso separadamente. Quando apenas L está vazio, cobertura e deslocamento não são definidos; não os preencher com zero.

As listas gravadas são ordenadas alfabeticamente. Elas não recuperam o ranking original. Kendall, deslocamento de posição e nDCG ficam fora da análise principal até existir instrumentação que preserve ordem, empates, unidade e critério de relevância. nDCG também exige justificar por que o julgamento escolhido representa relevância, em vez de usar a própria posição como verdade automática.

## 5. Como obter um painel comparável?

Reutilizar o inventário de consultas somente mediante identificação da versão em [config_v2.py](../../src/config_v2.py) e da configuração carregada pelo coletor. A bateria canônica v2 contém 192 consultas e o módulo filtra EN; o N realizado deve ser lido do conjunto efetivamente despachado e elegível, não presumido a partir de um outline antigo.

Preservar vertical, consulta, idioma, provedor, modelo devolvido, versão, horário de busca, horário da resposta, disponibilidade de fontes e cache. Parte desses metadados precisa de extensão no módulo ou persistência: não estão garantidos por este documento. Definir tolerância temporal e o tratamento das chamadas que a excederem.

O plano anterior usava janelas de uma e de seis horas como se fossem o mesmo pareamento. A versão revisada exige escolher e verificar uma regra antes da coleta. Mudança de endpoint, busca habilitada ou modelo durante o painel deve produzir estrato explícito.

Dimensionar custo a partir de consultas despachadas, repetições, duração, chamadas por braço e preços confirmados no momento da decisão. O cálculo antigo de 96 consultas, duas rodadas diárias e 84 dias corresponderia, em exemplo aritmético, a 16.128 chamadas de busca antes de cache, não às 1.614 anteriormente declaradas. Esse exemplo não é plano aprovado nem cotação de API.

## 6. Como analisar sem escolher o resultado antes?

Começar por auditoria de cobertura e distribuição das métricas por estrato. Publicar oportunidades previstas, observadas, com falha, com fontes não expostas e com conjunto vazio. Declarar se a análise é por domínio ou URL e se a unidade é consulta, resposta ou par.

O modelo inferencial precisa respeitar a dependência entre consultas repetidas, provedores e datas. Bootstrap, se usado, deve reproduzir a unidade de dependência adequada ao desenho; reamostrar todas as linhas independentemente subestima incerteza quando há agrupamento.

O Jaccard pode assumir zero e um. A regressão beta convencional descrita por [Cribari-Neto e Zeileis (2010)](https://www.jstatsoft.org/article/view/v034i02) trabalha no intervalo aberto. Escolher um tratamento compatível com os extremos, justificá-lo no protocolo e apresentar sensibilidades. Não retirar os extremos ou deslocá-los arbitrariamente depois de ver qual ajuste produz significância.

Definir a família de contrastes antes de escolher correção de multiplicidade. O número de consultas vezes o número de modelos não cria automaticamente esse número de hipóteses. Reportar estimativa, incerteza e heterogeneidade, sem exigir direção favorável.

Os períodos de modelo e de observabilidade de fontes devem permanecer distintos. Nenhum método estatístico recupera timestamps ausentes, ranking descartado ou documentos nunca expostos pelo provedor.

## 7. Como comparar com a literatura recente?

A [Ahrefs, em 02/03/2026](https://ahrefs.com/blog/ai-overview-citations-top-10/), analisou 863 mil SERPs e cerca de quatro milhões de URLs citadas em AI Overviews. A proporção de URLs citadas presentes nos dez links orgânicos principais foi 37,1%; ao incluir blocos da SERP, 37,9%, no mesmo estudo. É uma referência de pergunta e método, não valor esperado para Jaccard de domínios do Brave.

O survey da [Zyppy de 09/09/2026](https://signal.zyppy.com/p/google-ranking-factors-expert-survey) organiza percepção profissional de ranking. Não informa a distribuição de overlap nem fundamenta um limiar nulo para este paper.

A documentação do [Google sobre recursos de IA](https://developers.google.com/search/docs/appearance/ai-features) explica que técnicas de fan-out podem buscar tópicos relacionados. A hipótese P2-H3 pode testar cobertura de subtarefas declaradas pelo pesquisador; não reconstrói subconsultas internas não observadas.

[Aggarwal et al., KDD 2024](https://arxiv.org/abs/2311.09735) oferece uma base experimental de visibilidade. Seus construtos precisam ser mapeados aos campos do estudo, sem assumir identidade entre métricas com nomes semelhantes.

## 8. Quais ameaças à validade precisam viajar com o resultado?

Brave, Google e APIs de modelos têm bases e interfaces distintas. A fonte pode ser nomeada no texto, exposta em metadado ou ausente por design; esses mecanismos mudam o denominador. Uma URL com a marca no caminho não estabelece identidade institucional.

O painel EN não representa automaticamente consultas em português. Repetição e cache afetam independência, atualizações de modelo afetam estabilidade e orçamento pode selecionar quais braços são observados. Tendência temporal agregada pode resultar da composição do painel.

A taxa de menção em janela de 200 caracteres pertence ao estudo longitudinal de entidades. O overlap de fontes do módulo usa outro conjunto e não deve ser descrito como a mesma variável. Citação, sustentação de afirmação e recuperação interna permanecem etapas distintas, conforme o [guia científico](../research/geo-wave-setembro-10-2026/GUIA_CONCEITOS_SEO_IA_PESQUISA.md).

## 9. O que precisa existir antes do manuscrito?

| Entrega | Critério verificável |
|---|---|
| Protocolo versionado | Pergunta, estimando, unidades, exclusões e análise definidos |
| Auditoria de instrumentação | Fontes, timestamps, campos e limitações conferidos |
| Piloto delimitado | Custo, disponibilidade e normalização avaliados sem contaminar a análise confirmatória |
| Dataset de análise | Proveniência, hash, dicionário e N realizado |
| Resultados | Tabelas calculadas, incerteza e sensibilidades |
| Artefato de reprodução | Código e permissões compatíveis com o material publicado |

Pré-registro e depósito de dados precisam de endereço, data e versão verificáveis antes de constarem como concluídos. Venue e calendário serão escolhidos quando o estudo e a chamada de submissão estiverem confirmados. Não se mantém uma promessa de prazo baseada em doze semanas de coleta que esta revisão não demonstrou existir.

A próxima entrega deste Paper 2 é o contrato de observabilidade e pareamento. Com ele, a equipe poderá decidir se a comparação de domínios do Brave responde à pergunta pretendida ou se deve implementar outra superfície antes de coletar.
