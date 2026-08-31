# Health-check da coleta e do instrumento · 2026-08-31

**Severidade**: Alta. Um evento de série, oito dias sem persistência e um defeito de instrumento que atravessa toda a janela v2.
**Status**: Corrigido no código e verificado em produção. Três lacunas continuam abertas e estão listadas no fim.
**Data**: 2026-08-31
**Escopo**: pipeline de coleta diária, coluna sobre a qual a extração de citação roda, contagem de alucinação nos probes adversariais.
**Fora de escopo**: manuscrito e achados da revisão adversarial, registrados em `governance/REVISAO-EXTERNA-PAPER-20260831.md`.

---

## Sumário

O health-check começou como diagnóstico de uma coleta travada e terminou num achado sobre o instrumento. A parte operacional era resolvível em uma tarde: um braço monopolizava o relógio do job e o saldo de um provedor tinha acabado. A parte do instrumento pesa mais, porque afeta o número que o estudo publica. A extração de citação nunca leu a resposta dos modelos; leu os primeiros 200 caracteres em cinco braços e a resposta inteira no sexto, que é justamente o braço RAG contra o qual os cinco são comparados.

Três coisas mudaram de status neste dia. A coleta voltou a persistir. A janela de observação virou decisão declarada e uniforme. E a explicação que o paper dava para o viés da janela caiu, substituída por outra mais simples e mais geral, depois de contestada na revisão externa e verificada contra o banco.

---

## Parte 1. A série ficou oito dias parada

### 1.1 Sintoma

Último dia persistido antes do conserto: 23-08. O painel de runs do GitHub Actions alternava `cancelled` e `failure` sem indicar onde a coleta morria. Duas causas independentes produziam os dois estados, e nenhuma delas aparecia acima do nível do log do job.

### 1.2 Causa raiz A: o braço Grok consumia 72% do tempo de coleta

O `grok-4.6` raciocina por padrão e o raciocínio é cobrado como saída. Medição feita em 31-08 contra a API, com a mesma query de citação usada na coleta:

| Configuração | Latência | Tokens de raciocínio |
|---|---:|---:|
| Sem o parâmetro (default do modelo) | 73,7 s | 2.746 |
| `reasoning_effort=low` | 19,7 s | 419 |
| `reasoning_effort=none` | HTTP 400 | o modelo recusa o valor |

Na run `33303260035` o braço consumiu 129 dos 179 minutos de wall-clock, contra 17 minutos do Gemini, 15 do Claude, 12 do ChatGPT e 5 da Perplexity. O job morria no `timeout-minutes: 180` com a quarta vertical pela metade. Cinco runs canceladas nesse padrão entre 24 e 30-08 queimaram cerca de 900 minutos de GitHub Actions sem persistir um único dia, com o orçamento de Actions já em 514%.

**Correção**: `XAI_REASONING_EFFORT` com default `low`, commit `ee5144c`. Modelo pinado intacto, mudança forward-only, fronteira de estrato registrada em `docs/METHODOLOGY_V2.md` §3.1.

### 1.3 O que a correção entregou, e o que eu previ errado

A run `33404549276` concluiu com sucesso em 2h12. Medições antes e depois:

| Métrica | Antes | Depois |
|---|---:|---:|
| Mediana de latência do Grok | 32,4 s | 16,2 s |
| Wall-clock do braço Grok | 129,0 min | 71,6 min |
| Wall-clock total da coleta | 178,6 min | 129,7 min |

A estimativa que eu registrei antes do fix era de aproximadamente 95 minutos de total, e estava otimista. A margem real sobre o teto de 180 minutos é de 50 minutos, não os 85 que a estimativa implicava. O Grok segue respondendo por 55% do tempo de coleta mesmo com o esforço de raciocínio reduzido, o que significa que o próximo aumento de cohort ou de bateria de queries volta a encostar no teto por causa dele.

O registro da previsão errada fica aqui de propósito. Estimativa que erra e é corrigida em cima da medição tem valor de calibração para a próxima decisão de capacidade; estimativa apagada depois de errar não tem valor nenhum e ainda ensina o hábito de apagar.

### 1.4 Causa raiz B: saldo da Anthropic esgotado

As runs que morriam em um minuto caíam no preflight com `credit balance is too low`. A chave é a canônica do projeto, fingerprint `cfcc92e901a33d04`, registrada desde 07-04, e voltou a responder 200 em 31-08. Foi recarga de saldo, não rotação de credencial.

O preflight fez exatamente o trabalho para o qual foi escrito: barrou a coleta em vez de gravar um dia com quatro dos cinco braços. Um dia parcial gravado silenciosamente custaria mais caro que oito dias de gap declarado, porque o gap entra no ledger de missingness e o dia parcial entra na série como se fosse observação completa.

Histórico de paradas por saldo nesta janela: 25-07, 06-08, 09 e 10-08, e a sequência de 23 a 31-08. A frequência já é alta o bastante para justificar alerta de saldo antes do esgotamento, que continua pendente.

---

## Parte 2. O defeito de instrumento

### 2.1 Sintoma

A detecção de citação roda sobre `citations.response_text`. Essa coluna nunca foi a resposta do modelo. Cinco braços gravavam `text[:200]`; a Perplexity, por percorrer outro caminho dentro do cliente, gravava a resposta inteira, até 2.502 caracteres.

A janela de observação, portanto, era assimétrica **entre os braços**, que é precisamente o eixo da comparação que o estudo faz. Comparar um motor RAG com motores paramétricos sob janelas diferentes confunde a diferença entre motores com a diferença entre janelas.

### 2.2 Por que nada detectou

Cada camada de verificação olhava para o lugar errado pelo motivo certo.

Os testes afirmavam sobre a coluna, e a coluna estava preenchida nos dois casos. Os validadores conferiam boa formação de string, e ambas as strings eram bem formadas, de tamanho plausível. Os health-checks diários confirmavam que os seis braços produziam linhas, que o split de idioma se mantinha em 50/50 e que os probes estavam marcados, e tudo isso era verdade. Os 223 testes passavam.

O defeito vivia um nível abaixo de toda afirmação que o pipeline fazia sobre si mesmo. Nenhuma asserção do pipeline era falsa; o conjunto delas simplesmente não cobria a pergunta "essa string é a resposta do modelo?".

O que expôs o problema foi uma checagem distribucional, não funcional. O comprimento médio armazenado batia em exatamente 200,0 em cinco braços e em 691,8 no sexto. Uma variável cujo máximo é igual ao mínimo em 18.560 observações não está medindo nada, está reportando um limite. Distribuição de comprimento com desvio zero é assinatura de truncamento, e nenhum teste de igualdade a um valor esperado teria produzido esse sinal, porque ninguém sabia qual valor esperar.

### 2.3 Tamanho do efeito

Re-extração sobre a série até 31-08, janela uniforme de 200 caracteres, apenas queries canônicas. Denominador: 66.399 observações, 50 dias.

| Braço | n | Como coletado | Janela uniforme | Delta | Linhas cortadas |
|---|---:|---:|---:|---:|---:|
| ChatGPT | 14.976 | 17,2% | 17,2% | +0,0 pp | 0 |
| Claude | 14.842 | 25,8% | 25,8% | +0,0 pp | 0 |
| Gemini | 14.587 | 1,8% | 1,8% | +0,0 pp | 0 |
| Groq | 14.208 | 8,5% | 8,5% | +0,0 pp | 0 |
| **Perplexity** | **7.436** | **75,7%** | **51,9%** | **−23,8 pp** | **7.435** |
| Grok | 350 | 32,3% | 32,3% | +0,0 pp | 0 |

Os 23,8 pontos que a Perplexity perde sob janela uniforme são instrumento, não motor. A 75,7% o braço RAG parece categoricamente diferente dos paramétricos; a 51,9% continua o mais alto e passa a pertencer à mesma família, o que muda a interpretação e a explicação exigida.

**Ressalva sobre os cinco deltas de +0,0.** Eu os apresentei originalmente como verificação de sanidade da re-extração. A revisão externa apontou, com razão, que aplicar `texto[:200]` a uma string que já tem 200 caracteres é a identidade, então o delta zero está garantido por construção e não é observação independente. A verificação continua útil como prova de que o script de harmonização não introduziu efeito colateral, e perde o valor que eu atribuía a ela como confirmação de que a re-extração reproduz o instrumento original. Registro a correção porque o texto do manuscrito ainda carrega a leitura antiga.

### 2.4 Eu estava errado sobre o mecanismo

Esta é a correção mais importante do bloco, e a que mais muda o texto do paper.

O manuscrito afirmava que a janela estreita penaliza motores RAG porque eles "abrem com prosa de enquadramento antes de nomear". A revisão externa contestou a afirmação. A verificação empírica confirmou a contestação.

Offset relativo da primeira menção, calculado por observação como offset dividido pelo comprimento do texto observado:

| Braço | n | Offset absoluto | Comprimento | Relativo médio | Relativo mediano |
|---|---:|---:|---:|---:|---:|
| Grok | 113 | 33 | 200 | 0,164 | 0,000 |
| Perplexity | 5.631 | 158 | 662 | 0,228 | 0,169 |
| Gemini | 265 | 97 | 197 | 0,493 | 0,375 |
| Groq | 1.210 | 108 | 200 | 0,539 | 0,530 |
| ChatGPT | 2.571 | 116 | 200 | 0,582 | 0,600 |
| Claude | 3.823 | 124 | 200 | 0,621 | 0,645 |

Teste de uniformidade na Perplexity: se as menções fossem distribuídas uniformemente ao longo da resposta, a fração além do caractere 200 seria 1 − 200/662 = 69,8%. O observado é 28,8%. O braço RAG concentra menções na abertura relativa da própria resposta, e nomeia mais cedo que qualquer paramétrico exceto o Grok. O mecanismo que o paper descrevia aponta para o lado oposto do que os dados mostram.

**Ressalva obrigatória.** Os denominadores dos braços paramétricos estão censurados em 200 caracteres, então os valores de 0,49 a 0,62 são limites superiores do offset relativo verdadeiro e a inversão não pode ser afirmada como fato. A conclusão defensável é mais fraca e mais útil: **a direção do viés da janela não é identificada pelos dados coletados sob janela assimétrica**. Afirmar a direção antiga era erro; afirmar a direção nova seria o mesmo erro com o sinal trocado.

O mecanismo mais simples, e provavelmente o correto, é quantidade de texto lido. Ler 662 caracteres em vez de 200 encontra mais menções, e encontraria em qualquer motor cuja resposta completa tivesse sido guardada. Isso torna o achado mais geral, não menos: o problema deixa de ser uma peculiaridade retórica de motores RAG e passa a ser uma propriedade de qualquer comparação entre janelas de leitura desiguais.

A evidência mais didática do defeito veio da investigação do Gemini, feita no mesmo dia e detalhada em `REVISAO-EXTERNA-PAPER-20260831.md` (item D9). O braço que mais abre com preâmbulo no painel é paramétrico: 79,6% das respostas do Gemini começam com saudação, hedge ou reformulação da pergunta, contra 9,2% da Perplexity e 0,0% do Claude. O Gemini gasta a janela inteira antes de nomear qualquer empresa, e a taxa de citação de 1,8% mede esse gasto, não a disposição do modelo em citar. O estilo de abertura que faz a janela morder pertence ao modelo e não à classe arquitetural, o que remove qualquer regra de bolso que permitisse a um leitor estimar o efeito da janela sem medir.

### 2.5 Nenhuma das 83.486 observações era auditável

O texto além da janela era descartado no cliente e nunca chegou ao banco. Um revisor externo não tinha como reproduzir a extração, porque o insumo dela não existia em lugar nenhum.

Dos dois defeitos de janela, este é o mais grave. A assimetria é corrigível porque a string truncada ainda é a string que o extrator viu, e re-extrair sobre ela reproduz exatamente a decisão original. Nenhum cuidado recupera texto que nunca foi gravado.

Corrigido daqui em diante com `response_full_text` (migration 0010). A correção é forward-only por construção: o histórico continua sem íntegra, e qualquer análise de sensibilidade de janela sobre a série anterior a 31-08 está limitada aos 200 caracteres nos cinco braços paramétricos.

### 2.6 A própria migration 0010 caiu no skip silencioso

Escrita para consertar o problema de auditabilidade, a migration 0010 foi chamada de dentro de `_migrate_add_vertical`. Rodava antes do `executescript` que cria a tabela `citations`, morria em `no such table`, e o `except` transformava a falha em log DEBUG. Num banco existente a coluna aparecia; num banco novo, nunca apareceria, e ninguém saberia.

É o mesmo padrão do restore R2 que ficou dois meses inerte: proteção escrita, proteção chamada, exceção engolida, pipeline verde. Pego por teste de regressão que falha se um banco novo nascer sem as colunas.

A lição operacional que sai daqui não é sobre esta migration. Todo `except` que degrada para log de nível baixo dentro de caminho de inicialização precisa de teste que exercite o caminho a partir do zero, porque o caminho incremental esconde a falha por definição.

---

## Parte 3. Recusa contada como alucinação

### 3.1 Sintoma

O probe adversarial pergunta sobre entidade fictícia. Qualquer resposta que engaje com a pergunta contém o nome da entidade, inclusive a recusa. A implementação original marcava alucinação sempre que o nome aparecia na resposta, o que faz o instrumento contar como erro a resposta mais correta possível.

De 16.579 respostas marcadas como alucinação, 11.195 (67,5%) traziam recusa explícita. Uma delas afirma que a instituição não é real nem registrada no Brasil.

### 3.2 Robustez da regex

Teste feito em 31-08. Uma versão estrita da expressão, sem os alternadores fracos capazes de casar negação de atributo dentro de resposta fabricada (`não há`, `não existe`, `no information`), produz 11.100 recusas (67,0%). Apenas 95 casos, 0,6% do total marcado, casavam exclusivamente pelo alternador fraco, e a inspeção manual mostrou que eram recusas legítimas do Gemini.

Duas conclusões, uma contra cada lado. A objeção do revisor de que a regex superestimaria a taxa de recusa não se sustentou nos dados. A afirmação do manuscrito de que a regex é "conservadora" e que 67,5% é piso também não foi demonstrada, e sai do texto. O que os dados sustentam é que **a estimativa é estável a essa variação de critério**, com meio ponto percentual de amplitude entre a versão permissiva e a estrita.

### 3.3 Taxonomia proposta, e a lacuna que ela ainda não fecha

Três casos, apenas o terceiro é alucinação:

1. **Recusa ontológica** — o modelo afirma que a entidade não existe. A resposta mais forte.
2. **Recusa epistêmica** — o modelo diz não ter informação, tipicamente citando corte de treino. Correta no efeito, mais fraca em espécie, porque declina sem afirmar inexistência.
3. **Fabricação** — o modelo descreve produtos, história ou posicionamento de entidade que não tem nada disso.

**Lacuna crítica.** A taxonomia é proposta e nunca foi medida. Não existe kappa entre anotadores, não existe amostra anotada por humano, não existe matriz de confusão do classificador contra rótulo humano, e a distribuição das três categorias não é reportada em lugar nenhum do projeto.

Há um problema de método além da falta de medição. Estimar fabricação pelo complemento de um detector de recusa é inferência do mesmo tipo que o paper critica em outros trabalhos: definir a quantidade de interesse como aquilo que sobrou depois de um filtro cuja acurácia ninguém mediu. Fabricação precisa de detecção positiva de conteúdo inventado, com amostra anotada e concordância reportada, antes de virar número publicável.

---

## Correções aplicadas

| Achado | Correção | Estado |
|---|---|---|
| Grok consumia 72% do wall-clock | `XAI_REASONING_EFFORT` default `low` (`ee5144c`) | Verificado na run `33404549276` |
| Saldo Anthropic esgotado | Recarga; chave canônica preservada | Chave responde 200 em 31-08 |
| Janela assimétrica entre braços | `apply_citation_window` como decisão única, `PAPERS_CITATION_WINDOW_CHARS` | Aplicado aos seis braços |
| Íntegra descartada no cliente | `response_full_text` (migration 0010) | Forward-only; histórico não recuperável |
| Migration 0010 em skip silencioso | Movida para junto de 0005/0006/0007 + teste de regressão | Banco novo nasce com as colunas |
| Recusa contada como alucinação | Marcador de recusa + taxonomia de três casos | Taxonomia proposta, não medida |
| Mecanismo do viés da janela | Correção registrada em §4.1-bis da metodologia | Direção declarada não identificada |

## Verificação

- Run `33404549276` concluída com sucesso em 2h12, com os cinco braços persistidos.
- Suíte de testes em 237 passando após as correções.
- Distribuição de comprimento armazenado deixa de ter máximo igual ao mínimo nos braços paramétricos a partir de 31-08.
- Teste de regressão falha se banco novo nascer sem `response_full_text` e `citation_window_chars`.

## Em aberto

1. **Alerta de saldo antes do esgotamento.** Quatro paradas por crédito nesta janela. O preflight barra a coleta, o que é correto, e não avisa antes de a barreira ser necessária.
2. **Margem de 50 minutos sobre o teto de 180.** O Grok ainda responde por 55% do wall-clock. Qualquer aumento de cohort ou de bateria encosta no timeout de novo.
3. **Taxonomia de recusa sem medição.** Sem amostra anotada por humano, sem kappa, sem matriz de confusão, e sem detecção positiva de fabricação. É a lacuna de maior consequência para o paper, porque H2 depende dela.
4. **Sensibilidade de janela limitada no histórico.** A íntegra só existe a partir de 31-08, então a análise sob janela completa não alcança a série anterior nos braços paramétricos.

---

**Documento versão 1.0 · 2026-08-31**
