# A assinatura distribucional de um defeito de instrumento · 2026-08-31

**Severidade:** alta, metodológica
**Status:** defeito corrigido; três guards instalados
**Origem:** pergunta feita durante a revisão do paper — por que a coluna
"share at exactly 200" da Perplexity está zerada?

---

## A pergunta

A Tabela 4 do manuscrito reporta o comprimento do texto armazenado por braço.
A última coluna mede a fração de respostas com exatamente 200 caracteres:

| Braço | n | Média | Mín | Máx | Fração em exatamente 200 |
|---|---:|---:|---:|---:|---:|
| ChatGPT | 19.328 | 200,0 | 200 | 200 | 100,0% |
| Claude | 19.162 | 200,0 | 200 | 200 | 100,0% |
| Groq | 18.304 | 199,8 | 74 | 200 | 99,8% |
| Grok | 462 | 200,0 | 187 | 200 | 99,6% |
| Gemini | 18.794 | 197,0 | 87 | 200 | 94,8% |
| **Perplexity** | **7.436** | **687,2** | **198** | **2.502** | **0,0%** |

O zero da Perplexity não é arredondamento. Conferido linha a linha: **nenhuma
das 7.436 respostas tem exatamente 200 caracteres.**

## A resposta, e por que ela é o achado

O zero é a assinatura de que aquele braço **não foi truncado**. Nos outros
cinco, o pipeline gravava `texto[:200]`, então toda resposta que passasse do
limite terminava exatamente ali. Na Perplexity o comprimento é livre, e acertar
exatamente 200 num intervalo que vai de 198 a 2.502 seria coincidência.

A distribuição confirma que não há corte algum nesse braço:

| Percentil | Comprimento |
|---|---:|
| mínimo | 198 |
| p1 | 289 |
| p25 | 479 |
| mediana | 618 |
| p75 | 799 |
| p95 | 1.341 |
| máximo | 2.502 |

Contínua e bem espalhada, sem acúmulo em ponto nenhum. Nos braços truncados
acontece o oposto: toda a massa empilhada num único valor. O mínimo de 198
parece suspeito de tão perto de 200, e não é — é uma resposta só, a mais curta
da série inteira, com um vazio completo entre ela e o p1. Truncamento parcial
produziria um pico em 200, não um ponto isolado abaixo dele.

**A generalização vale mais que o caso.** Um limite de instrumento é invisível
para teste funcional e evidente numa distribuição. Teste funcional pergunta se
o pipeline faz o que foi escrito; ele não pergunta se o que foi escrito mede o
que se pretende medir. Toda asserção que o repositório fazia sobre essa coluna
era sobre presença de valor, e o valor estava lá nos dois casos.

O que passou por 223 testes verdes:

- os seis braços produziam linhas todo dia;
- o split de idioma se mantinha exatamente em 50/50;
- os probes estavam marcados;
- os hashes de resposta variavam, então não era cache;
- nenhuma coluna vinha nula.

Nada disso perguntava **quanto texto o extrator estava lendo**.

## O que foi instalado

Três guards, um por etapa do pipeline. Cada um cobre uma classe de defeito que
já ocorreu neste repositório, não uma hipótese.

### 1. Coleta — `scripts/distribution_guard.py`

Roda no `daily-collect.yml`, depois do validador v2, **sem `continue-on-error`**:
assimetria de janela invalida a comparação entre motores, que é o objeto do
estudo, e um dia gravado assim entra na série parecendo bom.

Checa quatro coisas: massa empilhada num único comprimento; variável sem
variância; janela declarada divergente entre braços; e íntegra declarada mas
não gravada.

**A decisão de projeto que importa** está na distinção entre corte deliberado e
corte destrutivo. Depois da correção, todos os braços passam a ser recortados
em 200 caracteres de propósito, produzindo em `response_text` exatamente a mesma
forma distribucional do defeito. O que os separa é `response_full_text`: com a
íntegra guardada, o recorte é o parâmetro P1 funcionando; sem ela, o texto se
perdeu no cliente e não volta.

A primeira versão do guard não fazia essa distinção e reprovaria toda coleta
futura. Um guard que reprova sempre é indistinguível de um guard desligado — o
mesmo padrão do restore R2 que ficou dois meses inerte, invertido. Há teste
dedicado para as duas metades: `test_reprova_o_defeito_de_31_08` e
`test_aprova_a_configuracao_corrigida`.

### 2. Análise — dois defeitos declarados no paper, agora corrigidos

**Normalização da proeminência.** O componente P normalizava pelo comprimento
do texto observado. A mesma entidade no mesmo offset absoluto recebia P
diferente conforme o modelo tivesse respondido curto ou longo, e o componente
deixava de ser comparável entre motores — que é a comparação que o índice faz.
Passa a normalizar pela janela declarada, como a especificação sempre disse.

Sob janela fixa os dois denominadores coincidem para quase toda resposta, então
**a correção não move nenhum número já publicado**: proeminência média 0,335 e
rho de 0,981 antes e depois. Ela importa quando a janela é desligada
(`--window 0`) e os comprimentos passam a variar por ordens de grandeza.

**Definição do painel.** A amplitude B é um terço do índice e era calculada
contra um painel definido por contagem de observações. Qualquer limiar de
contagem favorece o braço aposentado contra o braço novo, e o resultado
concreto era este: o painel incluía o Groq, encerrado em 16/08 com meses de
volume acumulado, e excluía o Grok, que o substituiu em 23/08 e ainda tinha 96
observações em fintech. O índice de referência rodava sobre um painel com um
motor morto e sem um motor vivo.

Trocar o número absoluto por uma fração do maior braço não resolveria: 5% de
3.744 são 187, e o Grok continuaria fora. O problema é temporal, não de volume.
O painel passa a ser definido por **atividade na janela recente do período
analisado**, ancorada no último timestamp do dado e não no relógio — o mesmo
banco precisa dar o mesmo painel hoje e daqui a um ano. Verificado: o painel de
fintech agora traz ChatGPT, Claude, Gemini, Grok e Perplexity, sem o Groq.

Retirada também a justificativa errada da média geométrica, que o repositório
descrevia como não-compensatória. Ela só é no limite: zera apenas quando um
componente é exatamente zero, e uma entidade ausente de um motor entre seis
mantém B = 5/6, que uma cobertura maior compensa sem dificuldade.

### 3. Escrita — `scripts/manuscript_guard.py`

Confere o que é verificável por máquina: integridade de referência nos dois
sentidos, forma de DOI e de identificador arXiv, numeração e citação de tabela,
âncoras de seção, aritmética de delta em linha de tabela, e extensão do
abstract contra o limite do periódico-alvo.

Os três defeitos que a revisão externa encontrou eram todos desta natureza. A
citação fundadora do campo estava errada em venue, ano e DOI, com o DOI sequer
resolvendo. Um delta de tabela podia divergir das colunas que o originam sem
ninguém notar. Uma âncora podia apontar para seção que não existe.

O guard pegou uma falha real na primeira execução: o abstract estava com 205
palavras contra o limite de 200 do periódico-alvo.

**A fronteira está declarada em teste.** `test_o_guard_nao_avalia_argumento`
registra que uma afirmação falsa e bem formada passa incólume. Foi exatamente
esse tipo de afirmação — forma correta, sem apoio na medição — que a revisão
externa derrubou na §8 do paper. Verde no guard não é verificação de conteúdo,
e o teste existe para que ninguém confunda as duas coisas.

## O que continua em aberto

**A anotação humana da taxonomia de recusa.** A taxonomia de três casos é
proposta e nunca foi medida: sem kappa entre anotadores, sem padrão-ouro, sem
distribuição das três categorias. Estimar fabricação pelo complemento de um
detector de recusa é inferência do mesmo tipo que o paper critica.

**A comparação entre modo JSON e linguagem natural.** `dual_responses` continua
vazia. Se a diferença entre os modos for da ordem dos 23,8 pontos da janela, a
especificação fixa seis parâmetros enquanto um sétimo, de tamanho desconhecido,
corre solto.

**O exercício interlaboratorial.** Nenhuma evidência de que duas implementações
independentes da especificação convergem. É a proposição central do padrão e
não tem uma observação a favor.

**Verificação jurisdicional dos decoys.** Foram checados contra registros
brasileiros. Vários são construções genéricas com homônimos internacionais
prováveis, e um modelo que descreva corretamente uma empresa real de mesmo nome
em outro país entra hoje como fabricação.

---

## Relacionados

- `governance/HEALTH-CHECK-COLETA-20260831.md` — o incidente que originou tudo
- `governance/REVISAO-EXTERNA-PAPER-20260831.md` — os achados da revisão
- `docs/METHODOLOGY_V2.md` §4.1-bis — a janela como parâmetro declarado
- `docs/research/methods-paper/VERIFICATION.md` — reprodução de cada número
