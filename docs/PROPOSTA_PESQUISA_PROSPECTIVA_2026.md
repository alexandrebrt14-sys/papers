# Proposta de pesquisa prospectiva: três meses e orçamento de tokens

Proposta registrada em 11/09/2026. **Proposta metodológica: não aprovada para execução, não agendada e sem chamadas experimentais realizadas.** O ciclo papers encerrado permanece fechado.

## Decisão de desenho

Um próximo estudo deve coletar durante **pelo menos três meses completos de calendário**, com duração exata definida no protocolo. Cumprir o calendário não demonstra suficiência estatística: o piloto e a simulação precisam verificar a precisão pretendida para cada contraste principal. Se o orçamento não sustentar esse padrão, reduzir o escopo de perguntas antes de iniciar, estender o estudo mediante nova decisão ou declarar os resultados inconclusivos; não truncar respostas, omitir falhas ou escolher apenas efeitos favoráveis.

O desenho econômico recomendado para ser avaliado no piloto é **painel de sentinelas fixas com rotação estratificada de queries**, mantendo todos os serviços elegíveis nas mesmas células query/data. Ele preserva acompanhamento temporal das sentinelas e cobertura periódica da bateria, com menos chamadas que a bateria completa diária. Não fornece automaticamente a mesma precisão nem permite estimar uma série diária de todas as queries sem modelagem adicional.

## Atualização metodológica e fontes primárias verificadas

1. [Schulte, Bleeker e Kaufmann, *Don't Measure Once: Measuring Visibility in AI Search (GEO)*, arXiv:2604.07585, abril de 2026](https://arxiv.org/abs/2604.07585). Preprint recente que enfatiza medições repetidas e visibilidade como distribuição. Motiva separar variação entre execuções e datas; não prescreve um n universal para este novo painel.
2. [Sielinski, *From Stochastic to Stable: Rank Stability and Structural Sufficiency in AI Visibility Measurement*, arXiv:2607.10341, julho de 2026](https://arxiv.org/abs/2607.10341). O estudo distingue estabilidade de ordenação de precisão suficiente para comparar. O [texto integral](https://arxiv.org/html/2607.10341v1) considera 30 combinações plataforma/tópico. É preprint: seu critério de convergência pode ser comparado como diagnóstico exploratório, não importado como garantia de validade no painel longitudinal nem usado para encurtar os três meses.
3. [Koo e Pashley, *Design-based Causal Inference for Incomplete Block Designs*, versão 4, agosto de 2025](https://arxiv.org/abs/2405.19312v4). Desenvolve estimadores e variâncias para desenhos incompletos e balanceados. Sustenta avaliar desenhos formais quando não cabe todo o painel em cada bloco. Os pressupostos de atribuição do artigo não transformam automaticamente uma auditoria de APIs em experimento causal.
4. [NIST, definição operacional de blocos incompletos balanceados](https://www.itl.nist.gov/div898/software/dataplot/refman1/auxillar/durbin.htm). Um BIBD exige tamanho de bloco constante, igual frequência de cada tratamento e igual coocorrência de todos os pares. A rotação simples descrita neste adendo **não é denominada BIBD**, porque equilíbrio de frequência não garante equilíbrio de pares.
5. [Cameron e Miller, *A Practitioner’s Guide to Cluster-Robust Inference*, 2015](https://cameron.econ.ucdavis.edu/research/Cameron_Miller_JHR_2015.pdf) e [MacKinnon, Nielsen e Webb, *Cluster-robust inference: A guide to empirical practice*, 2023](https://doi.org/10.1016/j.jeconom.2022.04.001). Fundamentam tratar dependência, agrupamentos cruzados e limitações com poucos clusters. Ter muitas respostas por poucos prompts não substitui variedade de clusters.
6. [Howard, Ramdas, McAuliffe e Sekhon, *Time-uniform, nonparametric, nonasymptotic confidence sequences*, Annals of Statistics, 2021](https://arxiv.org/abs/1810.08240), DOI [10.1214/20-AOS1991](https://doi.org/10.1214/20-AOS1991). Referência para inferência válida sob inspeções sequenciais quando seus pressupostos são satisfeitos. Uma sequência de confiança para amostras independentes não pode ser aplicada ingenuamente às respostas dependentes deste painel.

A novidade aqui é a combinação prospectiva de repetição calibrada, células comparáveis, rotação planejada, avaliação de precisão e governança de versões/custos. Métodos consolidados continuam necessários; “atualizado” não significa substituir uma técnica adequada por uma novidade sem validação.

## Fase preparatória: usar o arquivo antes de gastar

1. Congelar os desfechos primários: por exemplo, presença de entidade no payload retido e contraste entre janelas derivadas; separar apoio factual, recomendação e citação de fonte. Definir população-alvo, denominadores, resolução de entidades e quais comparações serão confirmatórias.
2. Reanalisar offline o arquivo disponível para estimar faixas de prevalência, tamanho de resposta e dependência. Essas estimativas são informação preliminar; o regime antigo de truncamento e provedores não é transplante válido para o futuro.
3. Preparar testes locais de integridade, parsing, aliases, idempotência, retries e bloqueio de orçamento. Usar fixtures; não chamar LLM para tarefas determinísticas.
4. Planejar piloto prospectivo curto, por exemplo 7–14 dias, **somente em outro projeto autorizado**. O piloto antecede o período confirmatório de três meses, salvo protocolo que congele critérios antes e defina formalmente como incorporá-lo.
5. No piloto, distribuir repetições por serviços, verticais, idiomas, categorias e horários. Estimar comprimento de saída, taxas de falha, variabilidade dentro da célula e entre dias/queries. Validar entidades em amostra humana, não usar outro LLM como verdade de referência.
6. Simular o desenho candidato sob vários cenários: prevalência rara, alta correlação por query, autocorrelação temporal, mudança de versão e faltantes diferenciais. Registrar cobertura empírica e amplitude dos intervalos para os contrastes principais. Escolher densidade/repetições a partir da precisão desejada, não do número que cabe primeiro no orçamento.

Critério ilustrativo a definir no protocolo: intervalo de 95% com semiamplitude máxima de cinco pontos percentuais para um contraste primário. **Cinco pontos é exemplo de decisão científica, não garantia nem meta já aprovada.** Não confundir essa precisão de um agregado com precisão para cada entidade rara.

## Coleta de pelo menos três meses

### Opção A: sentinelas e rotação, a ser testada

- Universo ilustrativo de 192 queries, semelhante em dimensão à bateria anterior, mas submetido a revisão e versionamento.
- Selecionar aleatoriamente 24 sentinelas dentro dos estratos declarados, mantendo seu texto fixo. A inclusão diária das sentinelas não deve ser confundida com amostragem representativa de demanda real.
- Dividir as 168 restantes em quatro painéis de 42 queries, com balanceamento marginal e de estratos auditado. Como 42 não é divisível por todas as margens fatoriais, declarar o desequilíbrio diário residual e garantir equilíbrio no ciclo; não prometer balanceamento completo de todas as interações por dia.
- Coletar sentinelas mais um painel rotativo: 66 queries por serviço/dia. Nos cinco serviços, usar exatamente as mesmas queries e uma janela horária comum, com ordem de serviço randomizada/alternada e horários efetivos registrados.
- Randomizar a ordem dos quatro painéis dentro de cada ciclo de quatro dias sob restrições previamente definidas; evitar que uma query fique sistematicamente ligada ao mesmo dia da semana ou posição do ciclo.
- Planejar repetição nova em subamostra estratificada, distribuída em horários, para medir variação de geração. A proporção ilustrativa de 10% abaixo depende do piloto.
- Estimar separadamente a série diária das sentinelas e os agregados de ciclos completos da bateria. Nos agregados da bateria, equalizar pesos por query/célula ou usar probabilidades de inclusão conhecidas; não dar peso quatro vezes maior à sentinela só porque foi coletada mais vezes.
- Se a pergunta exige resposta diária de cada query ou interações raras não bem representadas, esse desenho pode ser inadequado: usar maior densidade ou escopo menor.

### Opção B: blocos incompletos formalmente balanceados

Quando não é possível observar todos os serviços em toda célula, gerar e verificar um desenho de blocos em que cada serviço tenha igual exposição e cada par de serviços tenha igual coocorrência nos blocos, com conectividade do grafo de comparações e estratificação temporal. Conferir as condições b·k=v·r e λ(v−1)=r(k−1), além da matriz real de incidência; as equações são necessárias e não demonstram sozinhas a existência do desenho.

Essa alternativa perde algumas comparações diretas em cada célula e precisa de estimador compatível com a atribuição e de simulação de precisão. **A primeira preferência continua sendo preservar todos os serviços nas queries selecionadas**, porque isso mantém comparação pareada contemporânea simples. BIBD não é rótulo decorativo para qualquer amostra menor.

## Integridade, versões e faltantes

- **Texto integral capturado:** persistir a resposta recebida, fontes expostas, metadados e motivo de término; derivar prefixos depois. Uma média de tokens usada no orçamento não é teto de truncamento.
- **Limites de geração:** selecionar limite de saída adequado no piloto, registrar finish/stop reason e tratar respostas encerradas por limite como observações com condição própria. Não cortar a persistência para reduzir armazenamento.
- **Versões:** modelo, endpoint, modo de busca, parâmetros expostos, prompt de sistema, extrator e léxico recebem identificação/versionamento. Uma atualização gera novo estrato/regime. Registrar ponte de sobreposição se tecnicamente possível e previamente planejada; não atribuir drift oculto a uma causa não observada.
- **Cache:** resposta recuperada do cache local serve para reanálise ou prevenção de duplicação acidental, não é nova observação. Repetição científica intencional tem ID e timestamp próprios. Hash igual, sozinho, não prova cache do provedor.
- **Idempotência:** a chave da tarefa deve incluir query, serviço/modelo, data/janela, regime e réplica planejada; novas tentativas da mesma tarefa não se tornam múltiplos sucessos amostrais.
- **Falhas:** distinguir ausência planejada pela rotação, tentativa não enviada por orçamento, timeout, rate limit, erro persistente e resposta válida sem menção. Faltante nunca vira zero.
- **Retries:** teto por tarefa e prazo dentro da célula temporal; retry apenas para falhas transitórias apropriadas, com backoff/jitter e registro. Não insistir em autenticação inválida ou entrada rejeitada. Tentativa tardia pertence ao horário efetivo e não preenche retroativamente uma data.
- **Completude:** relatório por serviço/data/estrato com chamadas previstas, enviadas, bem-sucedidas e elegíveis. Ajustes por faltantes exigem pressupostos; ponderação por probabilidade estimada não garante corrigir ausência não ignorável.

Essas regras são recomendações de implementação derivadas das falhas do BRGEO-1 e do desenho proposto. Precisam de especificação e testes antes de qualquer novo ciclo.

## Análise e critério de encerramento

Pré-especificar agregação por célula, pesos, regras de réplica e análise dos contrastes pareados. Avaliar erros-padrão ou reamostragem compatíveis com agrupamento cruzado por query e data e com autocorrelação temporal; comparar com modelos hierárquicos como sensibilidade. Escolher bloco temporal e correções para poucos clusters por simulação, sem prometer que a simples opção “cluster robusto” resolve todos os regimes.

Manter estratos de versão separados; declarar população comum e perdas de interseção. Reportar contagem de datas, queries, células, respostas e faltantes. Pares de conjuntos vazios ficam separados de estabilidade informativa. Não imputar silêncio do coletor como ausência de entidade.

Acompanhamento operacional pode ser diário. Avaliações inferenciais devem obedecer aos pontos de análise pré-especificados. Se houver adaptação orientada pelos resultados, justificar método sequencial compatível com o processo observado; não usar repetidos intervalos ordinários como regra de parada oportunista.

**Regra mínima proposta:** três meses completos transcorridos + cobertura/qualidade pré-definidas avaliadas + precisão dos desfechos principais examinada. Se o horizonte terminar com precisão insuficiente, resultado inconclusivo ou extensão explicitamente decidida, dentro de orçamento próprio. Não prometer três meses “sem comprometer resultados”: oferecer critérios verificáveis e limites, pois nenhum desenho garante achado ou significância.

## Cenário matemático de chamadas e tokens: totalmente hipotético

Exemplo de **92 dias que cubram três meses completos de calendário**, cinco serviços, uma resposta base por célula, 192 queries no universo. Datas reais não estão marcadas.

| Cenário | Cálculo | Chamadas novas previstas |
|---|---|---:|
| Bateria completa diária | 92 × 5 × 192 | 88.320 |
| Sentinelas + rotação | 92 × 5 × (24 + 42) | 30.360 |
| Repetições novas planejadas, 10% no cenário rotativo | 30.360 × 0,10 | 3.036 |
| Total com réplicas | 30.360 + 3.036 | 33.396 |
| Reserva de até 5% de novas tentativas | teto de 33.396 × 0,05 | 1.670 |
| Limite ilustrativo de tentativas, incluindo reserva | 33.396 + 1.670 | 35.066 |

A redução das chamadas-base é **65,625%**. É economia aritmética contra a bateria completa diária, **não equivalência de informação, precisão ou custo monetário**. Com réplicas de 10% também no cenário denso, a redução relativa continua igual; retries e comprimento de saída podem diferir.

Em 92 dias há 23 ciclos completos de quatro dias: cada query rotativa tem 23 observações-base por serviço, enquanto cada sentinela tem 92. Essas contagens podem ser insuficientes para alguns contrastes e tornam obrigatório corrigir pesos de inclusão/agregação.

Hipótese exclusivamente contábil: média de 600 tokens de entrada e 900 de saída por chamada, sem ferramentas/reasoning extras. Em 33.396 chamadas: **20.037.600 tokens de entrada + 30.056.400 de saída = 50.094.000 tokens**. Se todas as 1.670 tentativas adicionais consumissem a mesma média, seriam **52.599.000 tokens**. Falhas podem consumir menos, o mesmo ou ter cobrança específica; a reserva deve usar a regra real do fornecedor. O piloto, os custos de anotação, busca, armazenamento e análises assistidas são adicionais.

Não existe garantia de saída com 900 tokens nem autorização para cortá-la nesse valor. O orçamento de reserva deve considerar quantis altos do uso e o limite máximo permitidos pelo protocolo, não apenas a média ilustrativa.


### Alternativas de escopo restrito: menor custo e pergunta menor

O cenário de 33.396 chamadas não é o ponto de partida obrigatório. Escolher **o menor plano que atenda à precisão por contraste primário nas simulações do piloto**. Quando a pergunta puder ser limitada a uma bateria menor, avaliar:

| Escopo hipotético | Base em 92 dias e cinco serviços | Réplicas novas de 10% | Total com réplicas | Reserva máxima de retries de 5% | Máximo ilustrativo de tentativas |
|---|---:|---:|---:|---:|---:|
| 12 prompts diários | 5.520 | 552 | 6.072 | 304 | 6.376 |
| 24 prompts diários | 11.040 | 1.104 | 12.144 | 608 | 12.752 |
| 24 sentinelas + 42 rotativos por dia | 30.360 | 3.036 | 33.396 | 1.670 | 35.066 |

As baterias de 12 ou 24 prompts devem ser selecionadas para uma pergunta restrita; não representam a cobertura de 192 prompts, quatro verticais e todas as interações. Estratos com pouca informação serão exploratórios ou excluídos do escopo confirmatório antes de iniciar. Cinco serviços com apenas 12 prompts ainda são apenas 12 clusters de query, exigindo cautela e métodos compatíveis; repetir diariamente não resolve esse limite sozinho.

Não escolher o plano de 12 porque é mais barato se ele falha no critério de precisão. Se nenhum plano viável passar na simulação, reformular a pergunta ou orçamento; não prometer resultados conclusivos.

Para mostrar sensibilidade contábil ao tamanho da resposta, supondo 600 tokens de entrada por chamada e médias de saída **hipotéticas** de 300, 900 ou 2.000 tokens:

| Plano, incluindo réplicas e sem retries | Saída média 300 | Saída média 900 | Saída média 2.000 |
|---|---:|---:|---:|
| 6.072 chamadas | 5.464.800 tokens totais | 9.108.000 | 15.787.200 |
| 12.144 chamadas | 10.929.600 tokens totais | 18.216.000 | 31.574.400 |
| 33.396 chamadas | 30.056.400 tokens totais | 50.094.000 | 86.829.600 |

Essas faixas não são medições do piloto nem limites de geração. Os valores reais por serviço, reasoning, busca e ferramenta podem mudar o custo substancialmente. O piloto deve fornecer a distribuição de uso e um limite de saída suficientemente alto, acompanhado do motivo de término. Toda resposta recebida será persistida; não haverá truncamento posterior para enquadrar o custo.

## FinOps antes da chamada, sem substituir o objeto científico

Definir teto total e mensal, moedas, modelos e preços datados em um manifesto de orçamento. Para cada fornecedor s:

**C_s = (T_entrada_nova × P_entrada + T_entrada_cache × P_cache + T_saida × P_saida + T_escrita_cache × P_escrita_cache)/1.000.000 + C_ferramentas + C_armazenamento + C_requisições.**

Quando houver cobrança distinta, adicionar T_reasoning × P_reasoning / 1.000.000 e N_search × P_search à fórmula, observando se reasoning já está incluído em T_saida para não contar duas vezes. Separar tokens de reasoning quando a tarifa os tratar distintamente. Preço efetivo de batch deve ser parâmetro verificado, não desconto presumido universal. Não contar novamente a mesma parcela de entrada como nova e cacheada.

Antes de enviar: reservar atomicamente o máximo de custo compatível com a chamada e a reserva de retries; após conclusão, reconciliar uso faturável real e liberar saldo. Interromper novos envios quando a reserva necessária não couber, registrar motivo e notificar. Cobranças em voo e jobs batch precisam permanecer provisionados. Não “recuperar orçamento” alterando a pergunta ou o modelo no meio do painel.

Fontes oficiais verificadas para cotação futura:
- [Tabela oficial Gemini API](https://ai.google.dev/gemini-api/docs/pricing).
- [Tabela oficial Claude API](https://platform.claude.com/docs/en/about-claude/pricing).
- [Processamento batch Claude](https://platform.claude.com/docs/en/build-with-claude/batch-processing): o modo assíncrono altera a janela de execução; só usar na coleta quando essa janela for compatível com o desenho, registrando o horário efetivo. É mais simples aplicá-lo ao processamento offline previamente autorizado.
- [Context caching Gemini](https://ai.google.dev/gemini-api/docs/caching): cache de contexto de entrada pode reduzir cobrança sem reutilizar a resposta pronta; registrar a condição e custos de armazenamento. Não confundir com cache de saída.

Nenhum preço monetário foi fixado neste adendo, nenhuma compra foi feita e nenhuma chave foi usada para pesquisa experimental. A fórmula deverá ser preenchida com tarifas oficiais do modelo e modalidade realmente escolhidos no início do projeto.

A economia recomendada vem de remover trabalho redundante: extração e normalização locais, reuso do arquivo, consultas curtas mas metodologicamente completas, cache de entradas quando aplicável, número de réplicas informado por piloto e amostragem planejada. Modelos locais/baratos podem apoiar organização e triagem **fora da medição**, com validação de qualidade; não substituem silenciosamente o motor que constitui o objeto da pesquisa e não contam como anotadores humanos.

## Texto curto para publicar na agenda futura

> Próximo ciclo proposto: no mínimo três meses completos de coleta, com desenho prospectivo, piloto de precisão e sentinelas fixas combinadas a queries rotativas. Cada comparação preservará células comuns entre serviços, versões identificadas, respostas integralmente capturadas e falhas separadas de ausências de menção. O orçamento será validado antes de cada chamada, com reserva limitada de retries e processamento local sempre que suficiente. Economizar tokens não autoriza truncar a evidência nem reduzir a amostra abaixo da precisão definida. A duração e o volume final dependerão do protocolo e de avaliação do piloto; o projeto encerrado não será reativado por esta proposta.

## Limite desta atualização

Esta é uma revisão bibliográfica focada e uma proposta de desenho. Os artigos de GEO de 2026 citados são preprints; as técnicas estatísticas e preços disponíveis precisam ser revalidados no início de um eventual projeto. Não foi executado piloto, simulação de poder, desenho BIBD computacional, anotação nem nova coleta. O cenário numérico foi verificado aritmeticamente e serve apenas ao planejamento.
