# Protocolo futuro baseado no site: medição, execução e orçamento

**Proposta de 11/09/2026, sem coleta agendada.** Este documento aprofunda o [desenho prospectivo](PROPOSTA_PESQUISA_PROSPECTIVA_2026.md) a partir do código do [landing-page-geo no commit 653e6438](https://github.com/alexandrebrt14-sys/landing-page-geo/tree/653e643828c886ca8741951f5615724d78bf6269) e de fontes primárias verificadas até 11/09/2026. O ciclo Papers encerrado continua bloqueado. Nenhuma proposta abaixo foi implantada como infraestrutura de pesquisa, testada com novas chamadas ou aprovada para iniciar um estudo.

O compromisso mínimo permanece: **piloto antes da fase principal e pelo menos três meses completos de calendário na coleta principal**. O piloto pode indicar que o desenho precisa de mais tempo, outra amostra ou pergunta menor. Não poderá reduzir o período mínimo, transformar falhas em zeros ou ajustar a coleta para perseguir significância.

## 1. Decisão principal: medir um fenômeno definido

O próximo estudo deve escolher uma pergunta confirmatória e uma população sobre a qual pretende concluir. Três trilhas são possíveis; não devem ser agregadas em uma única taxa de “visibilidade”.

| Trilha | Pergunta e unidade principal | O que permite concluir |
|---|---|---|
| Validade da medida | A mesma resposta recebe rótulos de menção, recusa, recomendação e apoio factual corretos? Unidade: resposta ou par afirmação–fonte, conforme a rubrica. | Erro do instrumento em uma população e época definidas; não efeito de marketing. |
| Variação longitudinal | Qual a distribuição de um desfecho sob consultas, superfícies e versões definidas? Unidade de comparação: célula pergunta × serviço/configuração × janela, com réplicas identificadas. | Mudanças e contrastes observacionais, com incerteza e limites de cobertura. |
| Intervenção editorial | Uma mudança previamente especificada no HTML altera o desfecho? Unidade de alocação: página ou grupo de páginas/tópico; observações permanecem agrupadas. | Efeito causal somente se alocação, controles, interferência, exposição e análise forem defensáveis. Caso contrário, descrição. |

A prioridade recomendada é consolidar a validade da medida e a execução econômica antes de um ensaio editorial. Um estudo não precisa medir todos os idiomas, mercados, modelos, rubricas e efeitos de negócio ao mesmo tempo.

### Cadeia de evidência

**Página disponível → acesso/recuperação observável → URL citada → apoio da fonte à afirmação → comportamento do usuário.** Cada etapa exige registro e denominador próprios. A seta organiza a auditoria, não afirma que toda resposta percorreu essas etapas nem que uma etapa causou a seguinte.

Um acesso de robô não prova treinamento; uma URL não prova apoio factual; clique ou conversão não prova efeito causal da otimização. Recuperação interna não exposta pelo provedor recebe “não observável”, não zero. Página encontrada numa busca separada não é automaticamente a página que o motor utilizou.

O [Search Arena, ICLR 2026](https://proceedings.iclr.cc/paper_files/paper/2026/hash/4476dd7320e0eba63961990d73525064-Abstract-Conference.html), motiva separar preferência humana de suporte das citações. O [SourceBench, preprint de fevereiro de 2026](https://arxiv.org/abs/2602.16942), motiva uma rubrica própria para qualidade da fonte, sem importar o desempenho de seu avaliador: a calibração humana descrita é pequena e de outro domínio. O [trabalho de Kakimov et al., Canadian AI/PMLR 2026](https://proceedings.mlr.press/v318/kakimov26a.html), fornece uma referência de auditoria observacional por consulta/documento; não revela o processo interno de todo motor comercial.

## 2. O que o repositório oferece e o que ainda precisa ser construído

A inspeção confirma código, não configuração ou execução em produção. As rotinas comerciais do site não são automaticamente o próximo experimento científico. Componentes podem ser reaproveitados após adaptação; nenhum comando de coleta existente deve ser acionado como atalho para este protocolo.

| Evidência no código inspecionado | Reuso possível | Requisito que falta para pesquisa |
|---|---|---|
| [Monitor e scheduler](https://github.com/alexandrebrt14-sys/landing-page-geo/blob/653e643828c886ca8741951f5615724d78bf6269/src/lib/admin/citation-collector-scheduler.ts#L1): adaptadores, concorrência e retries transitórios | Transportes e controle de rajadas | Tarefa/tentativa duráveis, gravação incremental, horário individual e idempotência. Limite de 240 segundos é temporal, não financeiro. |
| [Fila e aquisição atômica](https://github.com/alexandrebrt14-sys/landing-page-geo/blob/653e643828c886ca8741951f5615724d78bf6269/supabase/migrations/20260621_geo_jobs_concurrency.sql#L46) e [admissão do produto](https://github.com/alexandrebrt14-sys/landing-page-geo/blob/653e643828c886ca8741951f5615724d78bf6269/src/app/api/geo-check/route.ts#L192) | Posse de trabalho e recuperação de tarefas | Consulta financeira e admissão são separadas, com exceções comerciais e compatibilidade de schema. Criar reserva e admissão transacionais próprias; não anunciar teto rígido já existente. |
| [Log do monitor](https://github.com/alexandrebrt14-sys/landing-page-geo/blob/653e643828c886ca8741951f5615724d78bf6269/supabase/migrations/20260702_llm_citation_log.sql#L19) e [sondas de compreensão](https://github.com/alexandrebrt14-sys/landing-page-geo/blob/653e643828c886ca8741951f5615724d78bf6269/src/lib/geo-checker/llm-probes.ts#L118) | Classificações e texto bruto em parte do Checker | O monitor conserva excerto; os componentes não compartilham um arquivo completo por tentativa. Preservar o envelope exposto e o texto recebido antes de derivar métricas. |
| [Estimativas de custo](https://github.com/alexandrebrt14-sys/landing-page-geo/blob/653e643828c886ca8741951f5615724d78bf6269/src/app/api/cron/llm-citation-monitor/route.ts#L315) e [cache de domínio](https://github.com/alexandrebrt14-sys/landing-page-geo/blob/653e643828c886ca8741951f5615724d78bf6269/src/lib/geo-checker/queue.ts#L110) | Planejamento preliminar e reanálise de resultados pagos | Falhas podem ser registradas com custo zero; estimativa não é fatura. Cache por domínio/24h, versão e capacidades não identifica todas as condições experimentais nem uma réplica nova. |
| [Extração de citações](https://github.com/alexandrebrt14-sys/landing-page-geo/blob/653e643828c886ca8741951f5615724d78bf6269/src/lib/geo-checker/citation-probes.ts#L334) e [varredura de concorrentes](https://github.com/alexandrebrt14-sys/landing-page-geo/blob/653e643828c886ca8741951f5615724d78bf6269/src/app/api/cron/competitor-geo-scan/route.ts#L87) | URLs e triagem estática econômica | URL não comprova acesso/suporte. A fase paga de concorrentes é planejada pelo handler, não executada. Triagem de alvos visíveis não define amostra representativa. |
| [Classificação local](https://github.com/alexandrebrt14-sys/landing-page-geo/blob/653e643828c886ca8741951f5615724d78bf6269/src/lib/admin/brand-mention-classifier.ts#L57), testes e [estatística](https://github.com/alexandrebrt14-sys/landing-page-geo/blob/653e643828c886ca8741951f5615724d78bf6269/src/lib/geo-checker/inference.ts#L127) | Fixtures, regras e análises offline | Janela lexical e concordância entre motores não equivalem a validação semântica humana. Integrar conjunto humano retido, erro por classe e inferência longitudinal. |

**Banco de perguntas separado da intervenção.** Nesse commit, o monitor combina 37 perguntas e, por padrão, 16 subperguntas com quatro motores: **212 pares pergunta × motor por corrida**, antes de retries e corte de tempo. É conta da configuração, não volume executado ou plano científico. Comentários antigos de 25 perguntas não devem alimentar a projeção financeira. O arquivo de desdobramento também fornece conteúdo às páginas; alterar simultaneamente o site e o instrumento confundiria intervenção e medida. Congelar painel/hash fora da edição de produção, separar perguntas com e sem marca e registrar a seleção rotativa. Desdobramento local não é telemetria das buscas internas dos provedores.

O [mapa completo do código](MAPA_SITE_PESQUISA_FUTURA_2026.md) registra oito achados, limitações e permalinks no commit inspecionado.

**Consequência prática:** criar um espaço de pesquisa separado, com identificador de protocolo, filas e contabilidade próprias, armazenamento do bruto e extratores versionados. O painel deve ler projeções reproduzíveis desse arquivo. O acervo encerrado pode apoiar reanálise e desenvolvimento local; não será misturado a respostas novas.

## 3. Desenho de pelo menos três meses com custo justificado

Manter como candidatos o painel de sentinelas fixas com rotação estratificada e baterias menores para perguntas restritas. Todas as comparações principais devem preservar as mesmas perguntas e janelas entre os serviços elegíveis. Serviço, produto, modelo, endpoint e modo de busca são dimensões distintas: ter o mesmo nome comercial não demonstra o mesmo instrumento.

### Critério de escolha

Escolher o **menor custo total entre os desenhos que atendam à precisão e à cobertura pré-definidas**. O critério não garante que exista um desenho barato adequado. Antes do piloto, registrar o contraste primário, a menor diferença relevante, a largura aceitável do intervalo, os estratos confirmatórios e as hipóteses usadas na simulação.

O piloto estima variabilidade entre respostas, perguntas e datas, erros de anotação, perdas e distribuição do consumo. Simular também cenários desfavoráveis: raridades, alta dependência, mudanças de versão, faltantes diferenciais e custos maiores. Sete a quatorze dias são uma hipótese para organizar o piloto, não prova de que ele capturou sazonalidade ou deriva de três meses.

| Cenário contábil, 92 dias e cinco serviços | Chamadas com 10% de réplicas | Reserva de até 5% de tentativas | Máximo ilustrativo |
|---|---:|---:|---:|
| 12 perguntas diárias, escopo restrito | 6.072 | 304 | 6.376 |
| 24 perguntas diárias, escopo restrito | 12.144 | 608 | 12.752 |
| 24 sentinelas + 42 rotativas por dia | 33.396 | 1.670 | 35.066 |

Os números são aritmética de planejamento, não amostra aprovada ou orçamento monetário. Doze perguntas repetidas por três meses continuam sendo apenas doze grupos de perguntas. As opções não têm cobertura nem precisão equivalentes. O [primeiro protocolo](PROPOSTA_PESQUISA_PROSPECTIVA_2026.md) mostra a composição e a sensibilidade aos tokens.

### Análise e adaptação

- Pré-especificar pesos por consulta/célula, probabilidades de inclusão, agregação de réplicas e tratamento de conjuntos vazios.
- A inferência precisa refletir dependência por pergunta, data e, quando relevante, página/tópico. Avaliar por simulação modelos hierárquicos e reamostragem/erros agrupados; poucos grupos limitam métodos assintóticos.
- Inspeção operacional diária não autoriza testes repetidos com parada oportunista. Usar momentos inferenciais e regras de adaptação definidos previamente.
- Amostragem ativa pode primeiro ser comparada à amostragem simples para **selecionar anotações de um corpus congelado**. As garantias do [FAQ de Wu, Nair e Candès, v3 de maio de 2026](https://arxiv.org/abs/2601.20251v3), são condicionadas ao desenho e ao banco estudado; não se transferem automaticamente para respostas novas, dependentes e sujeitas a deriva. Manter probabilidades positivas e auditar pesos extremos.
- Temperatura zero, semente fixa ou réplicas adicionais não garantem determinismo. [Blackwell, Barry e Cohn, versão de junho de 2025](https://arxiv.org/abs/2410.03492v2), estudam incerteza em tarefas fechadas; seu tamanho de repetição não dimensiona este painel. Não mudar parâmetros apenas para estreitar o intervalo: a média também pode mudar.

## 4. Referência humana e juiz econômico

A extração lexical e as verificações de integridade devem priorizar processamento determinístico local. Um juiz LLM é um instrumento secundário com erro; sua concordância não é um rótulo verdadeiro. Economizar exige escolher onde ele acrescenta informação.

1. **Rubrica e conjunto retido.** Preservar os rótulos individuais de dois avaliadores antes da adjudicação. Separar dados usados para desenvolver a rubrica dos usados para avaliar seu desempenho. Estratificar por idioma, tipo de pergunta, raridade, ambiguidade e regime de modelo. Não esconder discordâncias: [Elangovan et al., ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/hash/8798321486948322be2b4d658744ba72-Abstract-Conference.html), mostram os limites de resumir avaliação humana por correlação agregada.
2. **Auditoria probabilística.** Manter amostra humana aleatória por regime e probabilidades registradas; casos difíceis podem receber seleção adicional com pesos compatíveis. Anotar só discordâncias não estima o erro da população. Mascarar a identidade do gerador quando viável. Na subamostra de comparação direta humano–juiz, a referência deve ser formada por outros avaliadores, sem incluir o humano avaliado; prever avaliador adicional ou adjudicação independente para essa finalidade. Dois avaliadores podem permanecer na anotação ordinária. Comparar humano e juiz contra essa mesma referência independente.
3. **Incerteza da calibração.** Comparar estimativa humana direta e correção assistida por juiz. O [preprint de Chen et al., janeiro de 2026](https://arxiv.org/abs/2601.05420v1), mostra por que erro e incerteza da calibração entram na inferência. Fórmulas de observações independentes, como as de PPI/EIF nesse enquadramento, exigem adaptação e validação antes do painel agrupado; não basta corrigir uma porcentagem de falsos positivos e tratá-la como conhecida.
4. **Consenso não basta.** Auditar também decisões em que os juízes concordam. A [v2 de setembro de 2026 de Mukherjee et al.](https://arxiv.org/abs/2606.03043v2) discute erro compartilhado e corrige o comparador humano da versão anterior. O arXiv registra aceite EMNLP declarado pelos autores; os anais não foram confirmados nesta revisão. Um segundo juiz só entra se melhorar a métrica escolhida no conjunto retido o suficiente para justificar custo e latência.
5. **Duas referências temporais.** Manter sentinelas com respostas novas para o serviço e um pequeno arquivo fixo para auditar o avaliador. Assim, uma mudança de juiz pode ser investigada sem confundi-la com uma mudança do motor. O [artigo de Wiese, PLOS One, fevereiro de 2026](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0339920), motiva âncoras humanas longitudinais; suas dez semanas não satisfazem o período mínimo deste projeto. O desenho das duas referências aqui é uma proposta a validar.

Uma decisão do juiz pode ter saída estruturada e curta. Isso não autoriza retirar da entrada trechos necessários ao julgamento nem truncar a resposta observada. Manter referência ao texto completo e auditar qualquer extração intermediária. A aprovação do juiz deve considerar erro por classe, incerteza e custo; não uma nota global conveniente.

## 5. Superfície, idioma, fontes e intervenção editorial

### API e interface pública são estratos diferentes

Uma bateria de APIs define conclusões sobre aqueles endpoints/configurações. Para estudar validade externa, propor uma subamostra previamente sorteada e orçada na interface pública, quando o acesso autorizado e as condições de uso permitirem. Não somá-la à API como réplica do mesmo instrumento.

Registrar idioma, localização solicitada/exposta, contexto de sessão, busca ativada, modelo retornado quando disponível e horário efetivo. Não inventar a versão por trás de uma interface fechada. O [preprint exploratório de Żatuchin, agosto de 2026](https://arxiv.org/abs/2608.30052v1), motiva controlar idioma/localização/superfície, mas seus poucos prompts e dois dias não sustentam equivalência geral nem um efeito universal. A localização não fornecida ao pesquisador permanece desconhecida.

### Contraste de fonte verificável

A unidade semântica é a relação entre uma afirmação e uma fonte, com rubrica explícita. Guardar URL original/final, vínculo com o trecho, instante de consulta, status de acesso e hash de captura permitida. Uma página acessada semanas depois pode ter mudado. Fonte inacessível deve receber esse estado, acompanhado de sensibilidade, sem ser classificada automaticamente como falsa ou correta.

### Ensaio editorial compatível com um site real

Um A/B por visitante ou cookie não assegura qual variante foi observada pelo motor. Se o objetivo for testar conteúdo, alocar páginas ou grupos de tópicos, com versão estável no HTML e a mesma apresentação para pessoas e robôs. Registrar sorteio, conteúdo, commit, data, controle e intervenções paralelas.

Escolher uma mudança isolada ou combinação explicitamente definida. Não assumir que adicionar schema, citações ou extensão de texto terá efeito positivo. Bloquear a alocação por características anteriores quando apropriado; controlar alterações globais de templates e links que contaminem os controles. Prever atraso de indexação/recuperação e interferência entre páginas. A exposição só é conhecida quando há evidência; uma visita de crawler não prova uso na resposta.

A análise principal deve seguir a alocação original quando esse for o estimando pré-especificado, com grupos e calendário adequados. Não selecionar apenas páginas citadas depois da intervenção. Conversões, cliques ou tráfego podem ser resultados secundários com regras próprias; não substituem citação apoiada nem identificam seu efeito por correlação. Se o site não oferecer grupos separáveis, número suficiente de unidades e desenho defensável, declarar o estudo observacional.

## 6. Contrato mínimo de dados e custódia

Esquema abaixo é **proposto**, não uma migração instalada. Identificadores de tarefa e tentativa são diferentes; uma tentativa extra não se torna réplica científica.

| Registro | Campos mínimos propostos | Regra |
|---|---|---|
| Protocolo/plano | ID, versão, pergunta, desfechos, datas, estratos, pesos, painel, tarifas e critérios de pausa | Congelar antes da fase principal; alterações criam versão e justificativa. |
| Tarefa científica | ID, consulta/hash, estrato, janela/prazo, serviço/superfície, parâmetros, réplica e probabilidade de inclusão | Determinar elegibilidade antes da execução. |
| Tentativa | ID próprio, tarefa-pai, envio/retorno, request ID, estado, erro, custo reservado e reconciliado | Recuperação e retries não duplicam o denominador. |
| Resposta bruta | Objeto exposto pela API, texto integral recebido, identificadores de modelo, uso, razões de término e hash | Projeções curtas são derivadas; não substituir o bruto. Não exigir raciocínio interno não disponibilizado. |
| Documento e citação | URL, trecho associado, tempos, acesso, hash e captura permitida | Diferenciar referência citada, documento recuperado observável e página encontrada depois. |
| Anotação | Rubrica/versão, rótulos individuais, adjudicação, avaliador, regime e inclusão na amostra | Juiz automático não se apresenta como anotador humano. |
| Custos/manifesto | Unidades faturáveis, tarifa/vigência, estimativa, reserva, conciliação e referências aos objetos | Uso ausente é desconhecido; não registrar zero como se não tivesse havido cobrança. |

Separar ausência planejada, orçamento bloqueado antes do envio, falha técnica, saída incompleta, recusa, texto válido sem menção e campo não observável. Preservar o horário efetivo; resposta tardia não preenche retroativamente uma data.

Manter arquivo de objetos e manifesto com contagens/hashes; testar restauração em destino vazio e regeneração de uma tabela. Fonte congelada por hash pode ser reprocessada localmente sem novas chamadas. Definir política de acesso e retenção: licença do código não determina licença de respostas e páginas de terceiros. O export público deve ser o pacote realmente permitido, com limitações identificadas.

## 7. Orçamento completo e bloqueio antes do envio

O orçamento inclui respostas novas, avaliação, réplicas, retries, busca/ferramentas, cache, armazenamento, transferência, infraestrutura e trabalho humano. Aplicar a tarifa do produto e unidade reais; não contar duas vezes raciocínio já incluído na saída, nem a mesma parcela de entrada como nova e cacheada.

**Critério de admissão proposto:** custo conciliado + reservas em aberto + compromissos não duplicados + máximo admissível da nova tarefa ≤ cada teto aplicável. Verificar limites por tarefa, período e estudo em uma transação persistente compartilhada entre trabalhadores. Médias do piloto ajudam a planejar; o máximo efetivo de consumo e as tarifas sustentam a reserva de admissão.

Se o uso, a tarifa ou o limite de ferramenta não puderem ser determinados, não anunciar teto rígido garantido para aquele adaptador. Timeout não demonstra ausência de cobrança e não libera automaticamente a reserva. Cobranças tardias e lotes em execução ficam provisionados; reconciliar antes de liberar saldo. Reiniciar o worker não zera a contabilidade.

| Condição real da API | Regra a validar antes da coleta |
|---|---|
| Tokens + busca/ferramenta/requisição | Manifesto de preço por produto/modelo/unidade, URL, vigência e modalidade. Revisar mudanças durante os três meses. [Perplexity](https://docs.perplexity.ai/docs/getting-started/pricing), [Claude](https://platform.claude.com/docs/en/about-claude/pricing), [Gemini](https://ai.google.dev/gemini-api/docs/pricing), [xAI](https://docs.x.ai/developers/pricing). |
| Lotes assíncronos, resultados parciais e cancelamento não imediato | Orçar todo o compromisso antes do envio; associar respostas pelo ID, nunca pela ordem. Reservar o uso durante cancelamento. Usar lote na medição somente se sua janela for compatível; priorizar avaliação posterior. [OpenAI Batch](https://developers.openai.com/api/docs/guides/batch), [Claude Batch](https://platform.claude.com/docs/en/build-with-claude/batch-processing), [Gemini Batch](https://ai.google.dev/gemini-api/docs/batch-api). |
| Cache com mínimo, TTL e armazenamento | Medir com os prompts e cadência reais. Não inflar o prompt para atingir limiar; não presumir acerto ou desconto. Cache de prefixo não é cache de resposta pronta. [Claude caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching), [Gemini caching](https://ai.google.dev/gemini-api/docs/caching). |
| Alias mutável ou parâmetro não suportado | Guardar capacidades, identificador solicitado/retornado e alterações. Aceitação no cliente não prova parâmetro aplicado. Uma versão não congela a web. [xAI Models](https://docs.x.ai/developers/models). |
| Limites compartilhados e fusos diferentes | Coordenar fila por projeto/provedor, com prazo por célula; separar relógio de cota e janela científica. Outra chave não é solução para contornar a cota do projeto. [Gemini rate limits](https://ai.google.dev/gemini-api/docs/rate-limits). |
| Saída vazia ou incompleta com consumo | Persistir estados/uso/razões de término; não repetir automaticamente como erro grátis. Não exigir acesso a raciocínio oculto. [OpenAI reasoning](https://developers.openai.com/api/docs/guides/reasoning#allocating-space-for-reasoning). |
| Arquivos/resultados temporários | Recuperar antes do vencimento documentado para cada produto, conferir hashes e conservar o pacote conforme a política aprovada. [Claude Batch](https://platform.claude.com/docs/en/build-with-claude/batch-processing), [OpenAI Batch](https://developers.openai.com/api/docs/guides/batch#5-retrieve-the-results), [Gemini Files](https://ai.google.dev/gemini-api/docs/files). |

As fontes oficiais foram consultadas em 11/09/2026 e são documentos vivos. A cotação deste projeto não foi feita, saldo/contrato de conta não foi presumido e não há desconto universal aplicado. A política efetiva deve ser revalidada no lançamento e quando houver mudança. As chamadas hipotéticas acima não incluem automaticamente anotação e todos esses serviços.

### Ensaios sem chamadas pagas que antecedem o piloto

Usar fixtures para disputar o último saldo entre workers, interromper após envio, simular timeout cobrado, lote parcial, uso ausente, mudança de tarifa, gravação fracassada, repetição de tarefa concluída e restauração de backup. A regra esperada é não admitir gastos sem reserva consistente, preservar trabalho em andamento e registrar a causa. Aprovar a implementação só depois de demonstrar esses comportamentos.

## 8. Sequência de execução e critérios para avançar

Papéis indicam responsabilidades propostas, não equipe já contratada. A revisão precisa registrar quem verificou cada entrega.

| Fase | Artefato | Responsável e critério de avanço |
|---|---|---|
| Formular | Pergunta, estimando, população, desfecho, calendário mínimo e acesso | Ciência: plano não depende de resultado favorável e distingue estudo anterior. |
| Preparar offline | Adaptadores, contrato de dados, fixtures, reserva financeira e restauração | Engenharia/curadoria: ensaio completo reproduzível, sem duplicação ou gasto não admitido. |
| Pilotar | Uso/custo, falhas, rubrica humana, capacidades e simulações | Ciência/FinOps: precisão e integridade cabem no orçamento; caso contrário, reformular antes da coleta principal. |
| Congelar e autorizar | Manifesto versionado, datas reais, amostra, parâmetros, preços e regras de pausa | Responsável científico com revisão técnica/financeira: todos os requisitos têm evidência. |
| Coletar ≥ três meses completos | Livro diário de tarefas, respostas, faltantes, custos e versões | Operação: seguir o protocolo; uma trava de qualidade/orçamento pausa novas admissões de modo explícito. |
| Fechar e analisar | Manifesto final, conciliação, cobertura, estimativas e sensibilidades | Analista: avaliar os critérios definidos; inconclusão ou extensão prospectiva se necessário, sem busca de significância. |
| Publicar e reproduzir | Manuscrito, pacote permitido, código e instruções | Curadoria/revisor: outra pessoa refaz as tabelas e registra divergências. |

No arranjo Geo-Hermes, a execução autônoma deverá usar ambiente autorizado e sandbox, com estado durável e jobs de duração limitada. O computador interativo não se torna um servidor de coleta. A infraestrutura será escolhida depois de validar duração, cotas e custo, aproveitando o que existir sem criar serviços redundantes por padrão.

## 9. Prioridades de implementação futura

**P0 — antes de qualquer piloto pago:** definir pergunta/denominadores; separar tarefa/tentativa/resposta; preservar bruto; orçamento transacional; distinguir custo desconhecido de zero; teste de restauração; capacidades/versões explícitas. Resultado exigido: uma rodada simulada auditável e aprovada.

**P1 — antes dos três meses principais:** referência humana retida, simulação de precisão, desenho e pesos, cadência que caiba nas cotas, ledger de preços, política de faltantes, piloto satisfatório e protocolo congelado. Resultado exigido: decisão documentada de viabilidade, inclusive possibilidade de não avançar.

**P2 — somente quando acrescentar informação:** juiz adicional, seleção ativa, ponte API/interface, idiomas adicionais e ensaio editorial. Cada extensão precisa de ganho definido, orçamento e validação próprios. Publicar primeiro resultados da pergunta principal; não tornar todos os experimentos dependências de um primeiro estudo viável.

## 10. Limites desta proposta

Trata-se de análise de código, revisão bibliográfica focada e desenho proposto. Não é revisão sistemática exaustiva, dimensionamento concluído ou garantia de economia. As publicações recentes têm regimes, tarefas e pressupostos distintos; quando uma fonte é preprint ou seu aceite é apenas declarado, isso foi identificado. Nenhum ganho percentual de outro trabalho foi convertido em promessa para BRGEO.

Os controles e fases descritos são recomendações para outro projeto. O [encerramento em 11/09/2026](ENCERRAMENTO_2026-09-11.md), a trava de novas coletas e os dados históricos permanecem preservados.
