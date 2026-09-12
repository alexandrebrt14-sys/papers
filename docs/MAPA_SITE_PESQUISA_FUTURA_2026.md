# Infraestrutura de landing-page-geo para a próxima pesquisa

Inspeção somente de código realizada na sessão de encerramento de 11 de setembro de 2026. Repositório: `alexandrebrt14-sys/landing-page-geo`. Referência conferida: `HEAD = origin/master = 653e643828c886ca8741951f5615724d78bf6269`. Os links abaixo apontam para esse commit, preservando a evidência mesmo após outras publicações.

O repositório contém componentes reutilizáveis para uma pesquisa prospectiva com duração de pelo menos três meses. O aproveitamento mais promissor é combinar o monitor de citações, os classificadores locais e a fila do GEO Checker com um protocolo científico e um registro próprio de tentativas, evidências e orçamento. Essa integração ainda precisa ser implementada e testada. A pesquisa encerrada em `papers` permanece encerrada.

Esta inspeção não executou coletores, endpoints, testes, migrações ou consultas ao banco, nem verificou credenciais. “Presente no código” não comprova que uma migração foi aplicada ou que um agendamento esteja ativo em produção. Comentários sobre preço, disponibilidade de modelo e incidentes anteriores foram tratados como documentação do repositório, sem validação externa.

## Seis capacidades para a matriz pública

| Capacidade presente no código | Aproveitamento para o novo estudo | Lacuna que deve aparecer na publicação |
|---|---|---|
| Monitor com quatro adaptadores, banco de perguntas e amostra rotativa; concorrência por provedor e repetição em erros transitórios | Reutilizar transporte e extração local de várias métricas da mesma resposta | O monitor roda em memória e grava ao final; não há identidade durável da tentativa nem deduplicação da corrida. O limite de 240 segundos é de tempo, não financeiro. [E01] [E02] |
| Fila do GEO Checker com aquisição atômica de trabalho, recuperação de tarefas interrompidas e incremento de custo no banco | Adaptar o mecanismo de posse para tarefas pequenas de pesquisa | A consulta de orçamento e a admissão de trabalho são operações separadas; existe exceção de quota do produto. Isso ainda não é um teto rígido de pesquisa. [E03] [E04] |
| Log de citações com estados de falha, campos de entidades e URLs; sondas de compreensão do Checker com texto bruto | Separar resposta coletada, classificação e análise histórica | O monitor guarda excerto, não resposta completa; a sonda de citações guarda URLs, não o corpo das fontes. Falta um arquivo de evidências comum às rotas. [E05] [E06] |
| Custos calculados por tokens e tabela local; cache de resultado de 24 horas com validação de versão e capacidade | Evitar reanálises de produto e reaproveitar respostas já pagas para extrações locais | Estimativa de custo não é fatura; falhas do monitor podem terminar com custo zero. Cache por domínio não identifica protocolo, contexto ou repetição independente. [E07] [E08] |
| Varredura estática de concorrentes, agrupamento por domínio e planejador de etapa paga | Coletar primeiro sinais baratos e dimensionar uma etapa exploratória | A rota produz `deep_plan`, mas não executa essa etapa paga. Selecionar apenas concorrentes já visíveis também mudaria a amostra científica. [E09] |
| Classificação local de menção, validadores de resultado, testes de scheduler e utilitários estatísticos | Reutilizar regras, fixtures e ferramentas de análise | Teste de software e concordância entre modelos não substituem validação por anotadores humanos nem desenho longitudinal pré-especificado. [E10] [E11] |

## Oito achados com consequências para a pesquisa

### 1. Há um instrumento reutilizável, mas seu painel é orientado à marca e pode mudar

`GEO_CITATION_PROMPTS` fornece IDs, texto, categoria, intenção, prioridade e expectativa de marca. A contagem estática do array nesse commit encontrou **37 perguntas**, embora alguns comentários ainda mencionem 25. O monitor acrescenta, por padrão, **16 subperguntas rotativas** e consulta quatro motores: são **212 pares pergunta × motor por corrida**, antes de repetições por falha e de eventual interrupção pelo limite de tempo. Isso é uma conta da configuração, não um registro de chamadas realizadas. [E01] [E12]

A seleção rotativa usa dia do ano e posição do array. IDs de subpergunta incluem o índice dentro do grupo. O mesmo arquivo também alimenta conteúdo das páginas que se pretende medir. Isso facilita manutenção do produto, mas uma alteração editorial pode alterar simultaneamente a intervenção e o instrumento de observação. O banco contém perguntas com nomes da própria marca; elas medem reconhecimento induzido e devem ser separadas das perguntas de descoberta sem marca. [E12]

Para o estudo, congelar uma versão do painel com hash do texto e da configuração, separar perguntas com e sem marca e manter um painel principal balanceado ao longo dos três meses. A exploração rotativa pode existir como braço secundário, com regra de inclusão registrada. Não apresentar o desdobramento editorial das perguntas como se fosse telemetria das buscas internas que um provedor realmente executou.

### 2. O monitor controla rajadas, mas a corrida ainda não sobrevive a uma interrupção

O scheduler limita a concorrência a três tarefas por motor, admite até três tentativas, classifica 408, 429 e 5xx como transitórios, aplica espera progressiva e usa um orçamento compartilhado de 240 segundos. Há injeção de relógio, espera e aleatoriedade para testes. Erros persistentes e tarefas que não couberam no tempo aparecem no resumo. [E02]

O handler monta todas as tarefas em memória e só insere o lote no banco depois da coleta e classificação. A tabela básica tem uma chave de linha gerada e índice temporal, sem chave única de corrida/pergunta/motor. Uma nova invocação não procura uma corrida já concluída antes de chamar os provedores. O cron de Vercel está declarado para 06h UTC; a declaração no arquivo não foi confrontada com a configuração de produção. [E01] [E05] [E13]

Para três meses de observação, criar IDs persistentes de protocolo, rodada, observação e tentativa, com chave de idempotência e escrita incremental. Separar falha de provedor, tempo esgotado, falta de orçamento e resposta válida sem citação. Balancear a ordem das perguntas: a ordem fixa combinada com corte por tempo pode concentrar ausências nas posições finais. Deduplicação de gravação não basta para evitar cobrança duplicada se o processo cair depois da resposta e antes de salvá-la; o protocolo precisa registrar esse estado incerto e definir sua recuperação.

### 3. A fila oferece boas peças, mas seu orçamento foi desenhado para o produto

A função SQL `claim_next_geo_job` usa `FOR UPDATE SKIP LOCKED`, incrementa tentativas e recupera trabalhos com posse vencida. A função `increment_geo_job_cost` soma o custo em um único `UPDATE`. O worker verifica a posse após a fase estática e antes da primeira fase paga. Essas peças estão conectadas ao fluxo de execução do GEO Checker. [E03] [E14]

O orçamento não tem a mesma garantia. `geo_budget_committed_usd` é uma consulta `STABLE`: soma custos e acrescenta uma estimativa para trabalhos pendentes cujo custo ainda é zero. A rota consulta esse valor e depois chama `enqueueJob` em operação separada. Duas admissões simultâneas podem observar o mesmo saldo. O trabalho que já recebeu um custo parcial deixa de carregar aquela estimativa de saldo restante. A quota mensal garantida de usuários do produto permite passar acima do limite diário. Se a RPC falha, o caminho alternativo considera apenas o gasto já registrado. [E04]

Também há caminhos de compatibilidade quando faltam funções SQL; neles, a soma de custo retorna a leitura seguida de escrita. Portanto, não afirmar que toda implantação já possui as garantias da migração. Para a pesquisa, implementar uma admissão transacional com reserva por tentativa, por rodada, por dia e pelo estudo completo, sem exceção de quota comercial, com comportamento definido quando a contabilidade estiver indisponível. Testar concorrência real em banco isolado antes do piloto.

### 4. O grau de preservação da evidência varia entre componentes

O monitor persiste pergunta, motor, classificações, tamanho da resposta, excerto, custo e horário. A resposta completa existe durante a execução, mas não integra `CitationRow`. O horário salvo é comum ao lote, produzido após a fase de chamadas. As URLs próprias, URLs citadas e posições entram em JSON de entidades quando a coluna existe; o código aceita remover campos novos se encontrar schema antigo. Essa compatibilidade ajuda o produto a continuar operando, mas muda a riqueza do dado de uma rodada para outra. [E05] [E15]

Há uma base mais rica nas sondas de compreensão: `LlmBrandEvaluation` inclui `rawText`, modelo e duração, e o worker persiste o resultado de compreensão. Mesmo ali, trata-se do texto retornado, não de um envelope completo de requisição/resposta com cabeçalhos, request ID e uso por tentativa. Falhas de parsing e respostas truncadas podem retornar a avaliação vazia. [E06] [E14]

O script Python alternativo grava somente os primeiros 400 caracteres, usa custo fixo aproximado por chamada e sobrescreve `public/data/prompt-bank.json`. Ele não é um arquivo longitudinal completo. [E16]

A próxima arquitetura deve salvar primeiro a evidência bruta, com hash e horário por tentativa, e derivar as tabelas analíticas depois. Incluir texto exato do prompt, parâmetros, modelo solicitado e efetivamente retornado quando disponível, uso reportado, status, erro, motivo de término, versão do parser, IDs de requisição e versão do conteúdo/intervenção. O manifesto deve permitir reprocessar dados históricos sem gerar outra resposta paga.

### 5. Extração de URL já existe; comprovar o conteúdo da fonte exige outra camada

`citation-probes.ts` implementa adaptação para metadados de citação de Perplexity, OpenAI, Gemini e Anthropic, incluindo busca nativa ou ferramenta de busca conforme o adaptador. O resultado retém o modelo, até vinte URLs, indicação de domínio próprio, duração e custo estimado. A presença de URLs determina `searchUsed`; isso não é uma confirmação independente de que a busca foi realizada nem de que a fonte sustenta uma afirmação. [E17]

A função retorna URLs e sinais derivados, sem guardar o payload integral ou baixar e arquivar o corpo da fonte citada. O monitor diário usa outro conjunto de adaptadores: seus pedidos de Claude, Gemini e OpenAI não incluem ferramentas de busca, enquanto o Sonar tem comportamento diferente. A comparabilidade entre memória paramétrica e recuperação com busca deve ser um desenho explícito, não uma média única por “IA”. Os IDs de modelos presentes no código não foram validados junto aos provedores nesta inspeção. [E01] [E17]

Reutilizar os extratores, preservando também metadados originais, redirecionamentos e cobertura da extração. Se a pergunta científica for sustentação da afirmação, arquivar uma amostra das fontes com status HTTP, data, trecho relevante e hash do conteúdo, respeitando restrições de acesso. Distinguir menção nominal, URL presente, referência acessível e afirmação sustentada. Uma referência inacessível ou não verificada permanece nessa categoria.

### 6. O custo registrado é heterogêneo e pode subestimar falhas

No monitor, Claude, Gemini, OpenAI e Sonar usam consumo reportado multiplicado por preços locais. Campos ausentes de uso tendem a zero. Gemini considera `promptTokenCount` e `candidatesTokenCount`; o payload enviado configura orçamento de raciocínio, mas o cálculo não incorpora um campo separado de tokens de raciocínio. Sonar soma entrada e saída, sem parcela própria de requisição nesse adaptador. A alternativa Perplexity Agent API também calcula tokens multiplicados por preço local. Nenhum desses caminhos equivale à reconciliação de fatura. [E07]

Existe uma perda concreta: o adaptador pode retornar custo com uma resposta vazia, mas a conversão para `TaskOutcome` descarta esse valor quando há erro. A reconstrução final cria `cost_usd: 0` para tarefas não concluídas. O custo de tentativas anteriores também não compõe um registro durável por tentativa. Zero nessa linha não comprova que não houve cobrança. [E07]

O GEO Checker tem registro `finops_calls` com modelo, tokens e custo, porém o envio é feito sem aguardar confirmação, com erros silenciados. Seu `run_id` usa o horário da chamada e não recebe o ID do trabalho. As sondas de citação incluem parcelas locais de busca e estimativas de tokens quando o uso está ausente. O script Python usa custos fixos por chamada. Esses números precisam carregar seu tipo: uso observado com preço estimado, estimativa aproximada, valor reconciliado ou desconhecido. [E06] [E16] [E17]

Para dimensionar a pesquisa, usar contagem de chamadas por desenho e medir a distribuição real do custo no piloto. Não projetar um preço de três meses a partir de comentários antigos que citam 25 perguntas ou três motores. Fixar limite máximo de saída e repetição, contabilizar todas as tentativas e conciliar periodicamente o registro com o provedor. Se faltar custo, reservar conservadoramente e registrar a incerteza.

### 7. Cache e triagem economizam, mas não podem selecionar silenciosamente a amostra

O cache do GEO Checker procura o último trabalho concluído para o mesmo domínio nas últimas 24 horas. Depois verifica a versão do pipeline e a presença das capacidades necessárias. Ele não busca por hash de prompt, modelo, localidade, condição experimental ou versão do conteúdo. Reaproveitar essa resposta como se fosse uma repetição nova inflaria a amostra sem produzir informação nova. [E08]

A varredura de concorrentes agrupa alvos por domínio e busca sinais estáticos com `deep: false`. Ela combina esses sinais com citações anteriores e chama `planDeepPhase`, que estima custo e escolhe alvos. A classe `DeepBudgetGuard` existe e é testada, mas não é chamada pelo handler para executar uma fase paga: a rota grava o plano. Seu `upsert` por dia e relatório conserva um estado diário, não cada tentativa. Além disso, o handler não inspeciona o objeto de erro retornado pelo `upsert` antes de marcar `persisted = true`; a mensagem de persistência, isoladamente, não prova que uma observação foi salva. [E09]

Para a pesquisa, separar cache de transporte e deduplicação de observação. Reuso exige origem explícita e não conta como nova repetição. A triagem de site fora do ar ou alvo inacessível deve gerar ausência registrada; excluir apenas alvos sem citação anterior favoreceria os já visíveis. É possível manter uma coorte principal fixa e usar triagem econômica somente no braço exploratório.

### 8. Testes e estatística local são um ponto de partida, não validação científica concluída

Há testes executáveis do scheduler para concorrência, espera, repetição e esgotamento de tempo; fixtures para classificação e leitura do log; testes de extração de citações e validação estrutural de resultados. O teste do handler do monitor inspeciona o texto-fonte e explicitamente não executa a rota. `geo-queue.test.ts` cobre reconhecimento de erros de schema e resolução de categoria de usuário; não demonstra reserva financeira sob várias transações concorrentes. [E11]

O classificador separa citação com contexto, eco, negação e ambiguidade por regras locais, com janela de 200 caracteres. O leitor distingue varredura realizada sem acerto e entidade não medida. Essas regras são reaproveitáveis e permitem corrigir rótulos sem pagar por outra geração, desde que o texto tenha sido preservado. [E10]

Existem funções de Cohen/Fleiss kappa, bootstrap BCa e diagrama de confiabilidade. A aplicação de kappa presente no produto compara respostas de motores, incluindo presença de fragmentos de texto; não é uma validação por anotadores humanos independentes. Esta inspeção não identificou uma integração de pré-registro, anotação humana cega, protocolo congelado e análise longitudinal de três meses nos fluxos examinados. [E18]

Antes do piloto, montar um conjunto de referência anotado por duas pessoas, com adjudicação, positivos, negativos, ecos, homônimos e fontes inacessíveis. Medir erros do classificador por categoria e motor. Na análise longitudinal, considerar dependência entre repetições da mesma pergunta, dia, motor e domínio, em vez de aplicar intervalos como se todas as linhas fossem independentes. Mudança de modelo, intervenção e parser precisa ficar visível na série.

## Prioridades propostas, sem alteração de infraestrutura nesta tarefa

| Prioridade | Entrega proposta | Critério verificável antes de usar dados como evidência |
|---|---|---|
| P0 | Protocolo e manifesto do novo estudo | Pergunta primária, unidade de análise, coorte, braços, duração mínima, regras de parada e painel congelados; repositório ou espaço de dados separado do `papers` encerrado |
| P0 | Registro de observações e tentativas com evidência bruta | Reinício após falha simulada preserva a tentativa e o estado incerto; hashes e IDs permitem reanálise sem nova chamada |
| P0 | Reserva e admissão financeiras na mesma transação | Teste com várias admissões simultâneas não ultrapassa o limite reservado; falha contábil interrompe a admissão; nenhuma exceção de quota comercial |
| P0 | Validação offline e piloto limitado | Fixtures dos provedores, falha de gravação, queda após resposta, uso ausente, resposta vazia e troca de modelo cobertos; matriz de erro contra anotação humana |
| P1 | Coleta de pelo menos três meses em painel balanceado | Calendário e denominadores por braço/dia/motor preservados; execução realizada em ambiente apropriado, sem usar notebook como servidor |
| P1 | Arquivo de fontes citadas e verificação de sustentação | Cobertura de acesso e de anotação informada; URL, conteúdo e afirmação tratados como objetos distintos |
| P1 | Economia por extração local e cache rastreável | Uma resposta gera várias métricas; reaproveitamentos não viram novas observações; custo por observação válida acompanha custo total |
| P1 | Análise longitudinal e publicação reproduzível | Versões e mudanças identificadas; código reprocessa o arquivo congelado; relatório separa custo estimado, reconciliado e desconhecido |

Uma sequência econômica é preparar primeiro o protocolo e os testes offline, executar depois um piloto com limite pequeno e finalmente dimensionar a janela de três meses com o custo observado. O piloto deve ficar identificado como piloto. A amostra confirmatória não pode ser escolhida retrospectivamente pelos melhores resultados. A observação de tendências pode começar com poucos motores e painel menor, mantendo repetições e equilíbrio; ampliar perguntas sem preservar evidência e contabilidade apenas multiplica as lacunas atuais.

## Evidências no commit inspecionado

Os intervalos descritos no texto podem ser conferidos a partir das linhas de entrada abaixo.

[E01]: https://github.com/alexandrebrt14-sys/landing-page-geo/blob/653e643828c886ca8741951f5615724d78bf6269/src/app/api/cron/llm-citation-monitor/route.ts#L483
[E02]: https://github.com/alexandrebrt14-sys/landing-page-geo/blob/653e643828c886ca8741951f5615724d78bf6269/src/lib/admin/citation-collector-scheduler.ts#L1
[E03]: https://github.com/alexandrebrt14-sys/landing-page-geo/blob/653e643828c886ca8741951f5615724d78bf6269/supabase/migrations/20260621_geo_jobs_concurrency.sql#L46
[E04]: https://github.com/alexandrebrt14-sys/landing-page-geo/blob/653e643828c886ca8741951f5615724d78bf6269/src/app/api/geo-check/route.ts#L192
[E05]: https://github.com/alexandrebrt14-sys/landing-page-geo/blob/653e643828c886ca8741951f5615724d78bf6269/supabase/migrations/20260702_llm_citation_log.sql#L19
[E06]: https://github.com/alexandrebrt14-sys/landing-page-geo/blob/653e643828c886ca8741951f5615724d78bf6269/src/lib/geo-checker/llm-probes.ts#L118
[E07]: https://github.com/alexandrebrt14-sys/landing-page-geo/blob/653e643828c886ca8741951f5615724d78bf6269/src/app/api/cron/llm-citation-monitor/route.ts#L315
[E08]: https://github.com/alexandrebrt14-sys/landing-page-geo/blob/653e643828c886ca8741951f5615724d78bf6269/src/lib/geo-checker/queue.ts#L110
[E09]: https://github.com/alexandrebrt14-sys/landing-page-geo/blob/653e643828c886ca8741951f5615724d78bf6269/src/app/api/cron/competitor-geo-scan/route.ts#L87
[E10]: https://github.com/alexandrebrt14-sys/landing-page-geo/blob/653e643828c886ca8741951f5615724d78bf6269/src/lib/admin/brand-mention-classifier.ts#L57
[E11]: https://github.com/alexandrebrt14-sys/landing-page-geo/blob/653e643828c886ca8741951f5615724d78bf6269/src/lib/admin/__tests__/citation-collector-scheduler.test.ts#L70
[E12]: https://github.com/alexandrebrt14-sys/landing-page-geo/blob/653e643828c886ca8741951f5615724d78bf6269/src/lib/geo-query-fanout.ts#L199
[E13]: https://github.com/alexandrebrt14-sys/landing-page-geo/blob/653e643828c886ca8741951f5615724d78bf6269/vercel.json#L115
[E14]: https://github.com/alexandrebrt14-sys/landing-page-geo/blob/653e643828c886ca8741951f5615724d78bf6269/src/lib/geo-checker/worker-runner.ts#L88
[E15]: https://github.com/alexandrebrt14-sys/landing-page-geo/blob/653e643828c886ca8741951f5615724d78bf6269/src/app/api/cron/llm-citation-monitor/route.ts#L701
[E16]: https://github.com/alexandrebrt14-sys/landing-page-geo/blob/653e643828c886ca8741951f5615724d78bf6269/scripts/python/prompt_bank_run.py#L342
[E17]: https://github.com/alexandrebrt14-sys/landing-page-geo/blob/653e643828c886ca8741951f5615724d78bf6269/src/lib/geo-checker/citation-probes.ts#L334
[E18]: https://github.com/alexandrebrt14-sys/landing-page-geo/blob/653e643828c886ca8741951f5615724d78bf6269/src/lib/geo-checker/inference.ts#L127

| Ponto adicional de conferência | Arquivo e linha |
|---|---|
| Tamanho real do catálogo e perguntas com marca | `src/lib/geo-citation-prompts.ts:64`, `:125` |
| Quatro motores e schema de persistência | `src/app/api/cron/llm-citation-monitor/route.ts:57`, `:64` |
| Constantes de concorrência e limite de tempo | `src/app/api/cron/llm-citation-monitor/route.ts:190` |
| Modelo de falha que descarta custo e reconstrução com zero | `src/app/api/cron/llm-citation-monitor/route.ts:525`, `:543` |
| Custo da alternativa Perplexity Agent API | `src/lib/admin/perplexity-agent-api.ts:126` |
| Reserva estimada consultada, sem admissão transacional | `supabase/migrations/20260621_geo_jobs_concurrency.sql:112` |
| Caminhos alternativos de contabilidade | `src/lib/geo-checker/queue.ts:296`, `:489` |
| Registro `rawText` de compreensão | `src/lib/geo-checker/llm-probes.ts:200` |
| Validação de cache por versão e capacidades | `src/lib/geo-checker/result-validator.ts:77` |
| Leitura com estados medido e não medido | `src/lib/admin/llm-citation-log.ts:112`, `:176` |
| Planejador e guarda financeira local de concorrentes | `src/lib/admin/competitor-deep-routing.ts:165`, `:289` |
| Teste do monitor inspeciona fonte | `src/lib/__tests__/llm-citation-monitor-coleta.test.ts:13`, `:33` |
| Testes da fila não são ensaio concorrente de banco | `src/__tests__/geo-queue.test.ts:8` |
| Concordância entre motores no produto | `src/lib/geo-checker/comprehension-aggregator.ts:218` |
| Bootstrap e diagrama de confiabilidade | `src/lib/geo-checker/inference.ts:263`, `:346` |
