# V5-style-EF. Auditoria de estilo dos blocos E e F contra a PARTE C

Revisão de estilo da casa sobre `sections/E-findings-index-plan.md` e `sections/F-governance-threats-discussion.md`, contra a PARTE C inteira de `research/R4-standards.md` (C.1 reprovação, C.2 aviso, C.3 diagnóstico, C.4 exigências positivas, C.6 léxico de máquina), com a PARTE D acionada onde a PARTE C remete a ela. Continuação de `reviews/V2-style.md`, que auditou A a D.

**Estado do disco.** A medição foi feita em 11/09/2026 às 13h47 por `reviews/style_check.py`, estendido nesta auditoria. Os blocos E e F estavam estáveis desde 13h37 e 13h41 e é a versão entregue deles que segue auditada. Os blocos A, B, C e D estavam sendo editados durante a leitura (mtime 13h45 a 13h47): os redatores aplicaram parte das correções da V2 enquanto esta auditoria rodava. Todas as comparações entre blocos da seção 6 foram refeitas às 13h47 e descrevem o estado daquele minuto. Duas correções da V2 já entraram e mudam o diagnóstico: as duas antíteses do bloco D foram removidas (`C.1.1` agora zerada em D) e as seis referências a `v1.0` do bloco C sumiram. O efeito colateral é que **E e F passam a ser os únicos blocos que ainda carregam rótulo de versão interna na prosa e nas tabelas do manuscrito**.

**Escopo de prosa do medidor.** Ficam fora do denominador: tabelas, blocos de código, títulos, listas, listas de referência, legendas de tabela e figura, a seção "Reference keys used", a seção "Anti-tic pass", e duas seções novas que o medidor passou a excluir nesta rodada porque são nota ao editor e não texto do manuscrito: "Open marks and number provenance" (bloco E) e "Notes for the integrator" (bloco F). A auditoria das declarações do redator é feita à parte, na seção 3.

---

## 1. Sumário medido, por regra e por bloco

Os seis blocos aparecem para dar escala; E e F são as colunas auditadas.

| Regra e limiar | A | B | C | D | **E** | **F** |
|---|---:|---:|---:|---:|---:|---:|
| Palavras de prosa | 3.906 | 4.575 | 3.468 | 3.415 | **3.870** | **5.411** |
| Caracteres de prosa | 26.718 | 29.382 | 22.014 | 22.319 | **24.867** | **34.922** |
| Parágrafos de prosa | 33 | 45 | 33 | 42 | **43** | **61** |
| **C.1.1** antítese de fórmula fechada | 0 | 0 | 0 | 0 | **0** | **0** |
| **C.1.1** antítese graduada | 0 | 0 | 0 | 0 | **1** | **0** |
| **C.1.1 veredito** (avisa na 1ª, reprova na 2ª) | ok | ok | ok | ok | **AVISO** | **ok** |
| **C.1.2** fecho pseudo-profundo da lista fechada | 0 | 0 | 0 | 0 | **0** | **0** |
| **C.1.3** conectivo de enchimento abrindo parágrafo | 0 | 0 | 0 | 0 | **0** | **0** |
| **C.1.3** densidade de conectivo gasto por 250 palavras (limiar 1,00, piso 4) | 0,06 | 0,00 | 0,00 | 0,00 | **0,00** | **0,00** |
| **C.1.4** primeira frase de seção acima de 45 palavras | 0 | 0 | 0 | 0 | **2** | **1**¹ |
| **C.1.4** abertura que anuncia em vez de concluir | — | — | — | — | **0** | **3** |
| **C.1.5** autonarração fora do parágrafo de contribuições | — | — | — | — | **2** | **1** |
| **C.1.6** meta-discurso de verificação fora do método | 0 | 0 | 0 | 0 | **0** | **0** |
| **C.1.7** travessão ou meia-risca em prosa corrida | 0 | 0 | 0 | 0 | **0** | **0** |
| **C.1.8** atribuição vaga sem fonte na frase | — | — | — | — | **1** | **3** |
| **C.1.9** maior parágrafo em caracteres (avisa 1.500, reprova 2.200) | 1.359 | 1.685 | 1.159 | 1.095 | **1.168** | **1.717** |
| **C.1.9** parágrafos acima de 2.200 | 0 | 0 | 0 | 0 | **0** | **0** |
| **C.1.10** adjetivos vazios (reprova em 5 ou raiz acima de 2) | 0 | 0 | 1 técnico | 0 | **1 técnico** | **0** |
| **C.1.11** rótulo de confiança sem medição | — | — | — | — | **0** | **0** |
| **C.1.12** alerta rotulado abrindo parágrafo | 0 | 0 | 0 | 0 | **0** | **0** |
| **C.1.13** porcentagem sem denominador recuperável | — | — | — | — | **2** | **3** |
| **C.1.14** rótulo de versão ou errata na prosa do manuscrito | — | — | — | — | **1** | **2** |
| **PARTE D.2** afirmação de ausência não medida | — | — | — | — | **1** | **2** |
| **C.2** aposição contrastiva por 1.000 palavras (avisa 3, reprova 5) | 0,00 | 0,44 | 0,00 | 0,00 | **0,26** | **0,37** |
| **C.2** abertura de parágrafo repetida 3 vezes | 0 | 0 | 0 | 0 | **0** | **0** |
| **C.2** abertura de parágrafo repetida 2 vezes | 0 | 0 | 0 | 0 | **0** | **0** |
| **C.2** parágrafos acima de 1.500 caracteres | 0 | 1 | 0 | 0 | **0** | **1** |
| **C.2** intensificadores em série (avisa em 3) | 0 | 0 | 1 | 0 | **0** | **0** |
| **C.2** advérbios em `-ly` no parágrafo mais carregado (avisa em 4) | 3 | 3 | 3 | 3 | **3** | **3** |
| **C.2** perguntas retóricas (avisa acima de 1 por 300 palavras) | 0 | 0 | 0 | 0 | **0** | **0** |
| **C.2** introdutores de fonte por 120 palavras (avisa acima de 1) | 0,00 | 0,00 | 0,00 | 0,00 | **0,00** | **0,00** |
| **C.2** caracteres de prosa por item visual (avisa acima de 5.000) | 13.359 | 3.673 | 7.338 | 1.860 | **2.072** | **2.494** |
| **C.2** conclusão-espelho, sobreposição de palavras de conteúdo | — | — | — | — | — | **29,8% / 55,4%** |
| **C.6** entradas do léxico de 40 itens | 0 | 0 | 0 | 0 | **0** | **0** |
| **C.3** frase média em palavras (diagnóstico) | 26,0 | 25,7 | 24,3 | 24,9 | **26,7** | **24,3** |
| **C.3** desvio padrão da frase (diagnóstico) | 13,6 | 14,2 | 11,4 | 13,4 | **13,2** | **12,4** |
| **C.3** frase mais curta e mais longa (diagnóstico) | 2 / 63 | 3 / 68 | 3 / 58 | 1 / 55 | **5 / 77** | **1 / 55** |
| **C.3** frases acima de 60 palavras (diagnóstico) | 2 | 3 | 0 | 0 | **2** | **0** |
| **C.3** três parágrafos seguidos com a mesma contagem de frases | 2 | 4 | 2 | 3 | **3** | **5** |
| **C.3** frases abrindo por adjunto (diagnóstico) | 15,3% | 8,4% | 15,4% | 16,1% | **10,3%** | **13,5%** |
| **C.4.6** fechos de parágrafo sem número | 39,4% | 53,3% | 60,6% | 38,1% | **25,6%** | **57,4%** |
| Fora da régua: `rather than` por 1.000 palavras | 0,77 | 6,34 | 3,75 | 2,34 | **3,36** | **6,10** |

¹ A única em F é a primeira frase de Acknowledgements, 52 palavras. Acknowledgements é bloco de declaração e não seção de argumento, o que põe o caso fora da intenção da regra; vai como aviso na seção 4 e não entra na contagem de reprovações.

As colunas A a D trazem travessão nas sete regras que exigem julgamento e não contagem literal. Essas regras não foram reauditadas nos quatro blocos nesta rodada, e os quatro arquivos estavam em edição durante a medição; os números da V2 para elas descrevem um estado que já mudou. Nas demais linhas as seis colunas são medidas pelo mesmo script, na mesma passagem, às 13h47.

Para E e F, as sete linhas de julgamento vêm da leitura contra a régua, com o medidor fornecendo a lista de candidatos: os 79 percentuais com contexto para a C.1.13, a varredura de rótulo de versão para a C.1.14, a de atribuição para a C.1.8. A varredura literal só pega uma das três ocorrências de C.1.14, `the v1.0` em E §11; as duas de F escapam dela porque uma está escrita "the earlier version of this work", que não contém o rótulo, e a outra está numa célula de tabela, que fica fora do escopo de prosa.

**Contagem de reprovações confirmadas: E 8, F 12.** Nenhuma delas está no vocabulário. O léxico da C.6 está limpo nos dois blocos, o travessão está limpo, nenhum parágrafo chega perto do teto de 2.200 caracteres, nenhum parágrafo abre por conectivo gasto, e a densidade de aposição contrastiva é a terça parte do limiar de aviso. As reprovações estão em três lugares: rótulo de versão interna (C.1.14), porcentagem sem denominador (C.1.13) e afirmação sobre o mercado ou sobre o campo sem medição (C.1.8 com PARTE D.2). O bloco F acrescenta um quarto: a abertura que anuncia a arrumação do documento em vez de concluir (C.1.4).

**Dois falsos positivos do medidor, verificados a mão e descartados.** `robust` no bloco E é `cluster-robust`, o termo de erro padrão, e não adjetivo de elogio; a única frase mínima de 1 palavra no bloco F é o subtítulo corrido em negrito (`Custody.`, `Licensing.`, `Scope.`, `Independence.`), que o separador de frases conta como período. Esse segundo artefato explica a maior parte da divergência entre as 223 frases que o medidor lê em F e as 246 que a passagem anti-tique declara.

---

## 2. Achados de reprovação, bloco a bloco

As reescritas abaixo estão prontas para colar. Nenhuma altera um número, nenhuma enfraquece uma ressalva. Onde a reescrita precisa de um dado que o bloco não publica, isso vem dito na própria linha.

### 2.1 Bloco E

| # | Trecho literal | Regra | Reescrita proposta |
|---|---|---|---|
| E1 | §11: "the correction to the close date matters to a reader: **the v1.0 manuscript** named 2026-09-28, a forecast made on 2026-08-10 under an assumed collection rate that the credit outages of August and September broke, costing seventeen days of series (§8.3)." Na mesma abertura: "**This paper reports no confirmatory result.**" | **C.1.14** histórico de versão na prosa, agravado por **C.1.5**. O leitor do artigo publicado não tem acesso a um documento interno chamado v1.0 e não consegue resolver a referência. O bloco C removeu as suas seis ocorrências nesta mesma tarde; E ficou com a última do manuscrito, e a passagem anti-tique do bloco declara a regra como "None" e argumenta contra ela | "The confirmatory window closes at 90 collected days, projected for 2026-10-15, with 56 of the 90 reached on 2026-09-11. Nothing below is confirmatory. The plan is recorded in advance of one, and the close date has moved: a forecast made on 2026-08-10 put it at 2026-09-28 under an assumed collection rate that the credit outages of August and September broke, costing seventeen days of series (§8.3). A window defined in collected days converts an outage into a schedule extension, which is a design choice a reader should see declared rather than infer from a moving date." (todos os quatro números e as duas datas permanecem; saem o rótulo interno e a autonarração) |
| E2 | §9.5, primeira frase, 51 palavras: "A question that asks for a named best is answered with a name two and a half times as often as a question that asks for the landscape: 25.93% of the 34,319 directive observations carry a citation against 10.00% of the 34,305 exploratory ones, and the ordering holds in every one of the six arms." | **C.1.4**, teto de 45 palavras na primeira frase de seção | "A question that asks for a named best is answered with a name two and a half times as often as one that asks for the landscape. Directive queries carry a citation in 25.93% of 34,319 observations against 10.00% of 34,305 exploratory ones, and the ordering holds in every one of the six arms." (primeira frase: 26 palavras) |
| E3 | §9.7, primeira frase, 49 palavras: "No decoy was named spontaneously in any of the 68,624 canonical observations, on any of the six engines, inside the window or in the text as stored, which puts the 95% Wilson upper bound on the instrument's spontaneous false-positive rate at 0.0056% of the panel and at 0.342% on the seventeen-day Grok arm." | **C.1.4**, teto de 45 palavras. Resolve junto o aviso de C.1.13 sobre o denominador de 0,342% | "No decoy was named spontaneously in any of the 68,624 canonical observations, on any of the six engines, inside the window or in the text as stored. The 95% Wilson upper bound on the instrument's spontaneous false-positive rate is therefore 0.0056% on the panel and 0.342% on the 1,118 observations of the seventeen-day Grok arm." (primeira frase: 33 palavras. O 1.118 não é novo: é o mesmo número que o bloco F publica em §15 para o mesmo braço e a mesma série) |
| E4 | §9.5: "Within-arm the type contrast runs from **2.73% against 0.98%** on Gemini to **74.03% against 30.02%** on Perplexity, so its magnitude is engine-specific even where its sign is not." | **C.1.13**. Quatro porcentagens cujo n não está na frase, na frase anterior nem na Tabela E6, que é de nível painel (34.319 e 34.305) e de cinco braços, e não desce a braço por tipo de consulta | "Within-arm the type contrast runs from 2.73% against 0.98% on Gemini over n = [x] and n = [y] to 74.03% against 30.02% on Perplexity over n = [z] and n = [w], so its magnitude is engine-specific even where its sign is not." Os quatro n saem de `stats/data/`; esta auditoria não os inventa. Alternativa sem dado novo: acrescentar à Tabela E6 uma nota com a contagem por braço e tipo e apontar a frase para ela |
| E5 | §9.8: "Grok entered at **39.2%** in its first week, second in the panel, demoting Claude and ChatGPT one place each" | **C.1.13**. O n da primeira semana do braço Grok não está na frase, na anterior nem na Tabela E8, que dá 5 dias coletados e a taxa de 29,61% sobre todos os dias | "Grok entered at 39.2% in its first week, over the [n] observations that week, second in the panel, demoting Claude and ChatGPT one place each". O n sai de `stats/data/s2_daily_engine.csv`. Alternativa sem dado novo: trocar a porcentagem pela contagem, "Grok entered second in the panel in its first week, ahead of Claude and ChatGPT", e deixar a Tabela E8 carregar o nível |
| E6 | §10.1: "**It is described in the market as** non-compensatory, and that holds only in the limit" | **C.1.8**, atribuição vaga sem fonte na frase. Quem descreve assim não está nomeado, e o parágrafo seguinte é justamente o que corrige a descrição | "The geometric mean is called non-compensatory, and that holds only in the limit: it vanishes when a component is exactly zero, and an entity absent from one engine of six retains *B* = 5/6, so the penalty is gradual." (se houver fonte para a atribuição, ela entra com a chave; sem fonte, a correção é o conteúdo e a atribuição é supérflua) |
| E7 | §10.3: "which is **the opposite of the market practice of publishing a single branded score with the components withheld** [Zatuchin2026d]" | **PARTE D.2**. Afirmação de ausência ("components withheld") sobre a prática do mercado inteiro, apoiada numa referência única que é um mapeamento de uma indústria. O bloco A recusa explicitamente esta classe de afirmação, e a V2 já reprovou a forma irmã em B §3.7 | "which is the opposite of the practice one recent multi-industry map records, a single branded score published with the components withheld [Zatuchin2026d]." |
| E8 | §11: "Those two facts are not equivalent, and **the paper does not present the first as if it were the second**." | **C.1.5**, autonarração da conduta retórica do documento, numa seção de plano. O parágrafo já entrega o argumento nas duas frases seguintes, sem precisar declarar a própria honestidade | Corte da frase. O parágrafo fica: "The plan is published in the project repository with a verifiable commit date, and it is not registered with any independent third party. A repository under the author's control offers no guarantee that the plan was not edited after the data were seen, since the same party holds the history and the authority to rewrite it. What publication in the repository does buy is a dated artefact a reviewer can diff against the analysis code; what it does not buy is the property that makes a pre-registration worth citing." (corte puro, nenhum fato alterado) |

### 2.2 Bloco F

| # | Trecho literal | Regra | Reescrita proposta |
|---|---|---|---|
| F1 | §15: "which inverts the architectural account **the earlier version of this work** advanced" | **C.1.14**. É a forma canônica que a regra nomeia ("An earlier version of this paper"), na seção de discussão, e a passagem anti-tique do bloco declara "None in the manuscript sections" | "which inverts the architectural expectation that retrieval-augmented composition would suffer most, and §6.6 reports the test that rejects it." |
| F2 | Tabela F1, linha 16: "The re-specified pattern diverges from the published **v1.0** shares by up to 5.2 pp per arm; Gemini reads 36.46% on the three-day cohort against 80.03% on the full series under one pattern" | **C.1.14** dentro de célula de tabela do manuscrito, mais **C.1.13** nos dois percentuais da mesma célula | "The re-specified pattern diverges by up to 5.2 pp per arm from the shares computed under the criterion as first described in prose; Gemini reads 36.46% on the 768 observations of the three-day cohort against 80.03% on the 15,355 canonical observations of the full series under one pattern." (os dois denominadores já estão publicados em §15 do mesmo bloco) |
| F3 | §13, primeira frase: "Custody, licensing, versioning and scope are settled and **are stated below** in the form an adopter can rely on. Verification of a conformance claim is not, and **the rest of this section declares** the design of the exercise that would settle it, so that the project can be held to a specification rather than to an intention." | **C.1.4**. Duas cláusulas anunciam a arrumação do documento. A regra manda que a primeira frase da seção seja a conclusão da seção, não o seu aviso. A passagem anti-tique declara "Each section opens with its conclusion" e mede só o comprimento, que de fato está sob o teto (19 palavras) | "Custody, licensing, versioning and scope are settled. Verification of a conformance claim is not: neither a conformance test suite nor an interlaboratory study exists, so Level 1 and Level 2 conformance is self-declared, and the design that would replace the declaration with evidence is specified here rather than deferred as future work." (a conclusão da seção passa a estar na primeira frase; nenhum fato novo, tudo já está no parágrafo "What conformance does not yet establish") |
| F4 | §15: "**Table F2 separates them before the argument goes further.**" | **C.1.4**, navegação do documento no lugar da coisa. A legenda da Tabela F2 já diz o que a tabela faz | Corte da frase. Se o editor quiser manter a ponte, ela vira conteúdo: "Table F2 sets each measurement beside the proposition it does not support." |
| F5 | §15: "**Five threads run through those rows and each one changes something a reader does next.**" | **C.1.4**, roteiro. Anuncia a estrutura dos cinco parágrafos seguintes, que já se anunciam sozinhos | Corte do parágrafo. O parágrafo seguinte abre em "The defect this paper reports about itself...", que é a primeira linha do argumento |
| F6 | §16: "They are the description of the state of the phenomenon that the vocabulary of metrology requires before a quantity can be called a measurand [VIM2012], and **the field currently publishes the quantity without them**." | **PARTE D.2** e **C.1.8**. Afirmação universal sobre o que o campo publica, sem levantamento e sem fonte na frase, na conclusão do artigo. O bloco A registra em §2.8 que esse levantamento não foi feito, o que deixa a conclusão em contradição com a ressalva do próprio manuscrito | "They are the description of the state of the phenomenon that the vocabulary of metrology requires before a quantity can be called a measurand [VIM2012], and a rate published without them names no measurand a second party can reproduce." |
| F7 | §15: "One control in that list costs almost nothing and **is the one most often skipped**." | **PARTE D.2**. Afirmação de frequência sobre a prática, sem medição | "One control in that list costs almost nothing. Sixteen of the 127 cohort slots hold firms that do not exist, verified against the federal tax registry, mapping services and court records before collection, and they travel inside the same battery on the same days through the same adapters as the real entities." (corte puro da cláusula) |
| F8 | §15: "part of what **the market reads as** models disagreeing about a firm is one aperture being applied to answers of very different lengths" | **C.1.8**, afirmação sobre o que um conjunto de atores lê, sem fonte e sem medição | "part of what reads as models disagreeing about a firm is one aperture applied to answers of very different lengths" (corte de duas palavras) |
| F9 | §14: "Gemini's stored responses on 2026-09-07 and 2026-09-08 end mid-word at means of 3,540 and 3,684 characters, and **Grok's do so on 9.1% of its responses**." Mesma lacuna na Tabela F1, linha 8 | **C.1.13**. O n das respostas do braço Grok não está na frase, na anterior nem na tabela apontada | "and Grok's do so on 9.1% of the [n] Grok responses retained whole." O n sai de `stats/data/`; esta auditoria não o inventa. O candidato natural é o 1.118 que §15 publica como a contagem canônica do braço, mas só o autor pode confirmar se o denominador de 9,1% é a contagem canônica ou o subconjunto com texto inteiro retido |
| F10 | §16: "It reverses one published reading, since an engine reported at 1.86% over 15,355 observations cites at **33.3%** when the same responses are read whole." | **C.1.13**, agravado. O denominador que está na frase (15.355) pertence ao outro número, o que convida o leitor a atribuí-lo ao 33,3%. O n verdadeiro é 768, publicado em §15 do mesmo bloco | "It reverses one published reading, since an engine reported at 1.86% over 15,355 observations cites at 33.3% on the 768 of those observations whose whole response was retained." |
| F11 | §15: "A rate arrives with the window that produced it and the recall target that window meets, because **200 characters recovers 35.4% of first mentions across the panel and between 7.8% and 70.2% by arm**." | **C.1.13**. Os três percentuais têm o denominador (1.367 observações que nomeiam uma entidade) na linha 19 da Tabela F1, que a frase não aponta e que está na seção anterior | "...because 200 characters recovers 35.4% of first mentions across the panel, and between 7.8% and 70.2% by arm, over the 1,367 observations that name an entity (Table F1, row 19)." |
| F12 | §13: "Conformance at Level 1 and Level 2 is self-declared, which reproduces in miniature the unverifiable claim **this paper opens by criticising**." | **C.1.5**, autonarração da conduta retórica. Fora da introdução, a regra adaptada reprova | "...which reproduces in miniature the unverifiable vendor claim of §1.1." |

---

## 3. Auditoria das declarações do "Anti-tic pass"

O enunciado da tarefa trata uma declaração de limpeza que não se sustenta como achado de severidade alta. A V2 encontrou cinco nos blocos A a D. Aqui são **sete**, quatro em E e três em F. As duas passagens são, no conjunto, mais precisas que as de A a D: contam certo em cinco medidas exatas (as porcentagens de prosa dos dois blocos, as primeiras frases das quatro seções de F, e os itens visuais dos dois blocos). O que falha nelas é sempre a mesma coisa: a busca literal pelo termo proibido, que não pega a variante.

### Não se sustentam

1. **Bloco E, C.1.14, severidade alta.** Declara "None. The 2026-09-28 date is discussed in §11 as a superseded forecast with the reason it moved, not as a correction notice". O texto entregue diz "the v1.0 manuscript named 2026-09-28". A regra não é sobre a data, é sobre o rótulo de versão interna na prosa, e a declaração argumenta contra a regra em vez de aplicá-la. Agrava: o bloco C removeu as suas seis ocorrências da mesma classe nesta mesma tarde, o que deixa E §11 e F como os dois últimos lugares do manuscrito em que o leitor encontra a palavra `v1.0` fora do formulário de conformidade, onde ela é o número legítimo da especificação.
2. **Bloco E, C.1.13, severidade alta.** Declara "Checked against PART D on the 56 percentages in the prose of §9, §10 and §11... Each names its n in the sentence, the preceding sentence or the caption of the table it sits under". A contagem está exata (o medidor lê 56), e a checagem não cobriu duas frases: o contraste por braço de §9.5, cujos quatro percentuais não recuperam n em nenhuma tabela do bloco, e o 39,2% da primeira semana do Grok em §9.8. É a repetição literal do achado que a V2 fez no bloco D, item 5.
3. **Bloco E, C.1.4, severidade alta.** Declara "Every subsection opens on its conclusion inside the first sentence" e lista nove subseções, omitindo §9.7. A medição confirma que as doze subseções abrem na conclusão, o que é o melhor resultado de C.4.4 do manuscrito, mas a regra C.1.4 tem duas metades e a segunda é o teto de 45 palavras: §9.5 abre com 51 e §9.7 com 49. A declaração cobriu a metade que o bloco cumpre e não rodou a que ele não cumpre.
4. **Bloco E, C.1.2, severidade média.** Declara "§9.8 closes on the reporting rule and its interval". O fecho medido de §9.8 é "Findings of this kind carry a shelf life, which is the reproduction problem algorithm audits have already met [Mosnar2025] and the reason P4 pins a model snapshot against silent provider updates [Chen2024]". A regra de reporte e o intervalo estão dois parágrafos antes. Nenhum fecho pseudo-profundo da lista fechada da C.1.2 aparece no bloco, de modo que a regra está cumprida; o que não se sustenta é a descrição do texto entregue, e o fecho real é uma generalidade com duas remissões onde cabia a consequência (ver 5, C.4.6).
5. **Bloco F, C.1.14, severidade alta.** Declara "None in the manuscript sections". §15 diz "the architectural account the earlier version of this work advanced", que é a forma que a regra nomeia palavra por palavra, e a linha 16 da Tabela F1 diz "the published v1.0 shares". Duas ocorrências, uma delas na discussão, a seção que o revisor lê depois do resumo.
6. **Bloco F, C.1.4, severidade alta.** Declara "Each section opens with its conclusion. First sentences measure 19 words in §13, 35 in §14, 33 in §15 and 31 in §16, all under the 45-word ceiling". As quatro contagens estão exatas, e é a medição mais precisa das seis passagens anti-tique do manuscrito. A primeira metade da afirmação não se sustenta em §13, cuja primeira frase anuncia duas vezes o que vem abaixo ("are stated below", "the rest of this section declares"), e o bloco acrescenta em §15 duas frases inteiras de roteiro que a mesma regra proíbe e que a passagem não procurou porque não abrem seção.
7. **Bloco F, C.2 conclusão-espelho, severidade média.** Declara que §16 "adds four quantities the abstract does not carry: the 37.4% coverage, the false-positive upper bound of 0.0056%, the 39.33% interaction share, and the 2,225 against 68,624 retention precondition". Três das quatro se sustentam. A quarta não: o resumo do bloco A já carrega a mesma quantidade, escrita "39.3% of the variance in coverage", e §16 a reescreve como "39.33%". A declaração conta como novidade o número que o resumo repete, e deixa de fora a novidade mais forte da seção, a reversão de 1,86% para 33,3% sobre 15.355 observações, que o resumo não carrega. Efeito colateral: as duas grafias do mesmo número, 39,3% e 39,33%, ficam a dois parágrafos de distância no manuscrito montado (ver seção 9).

### Lacunas de cobertura, que não são falsidade mas explicam as reprovações

| Bloco | Regras da C.1 que a passagem não roda | Onde isso custou |
|---|---|---|
| E | PARTE D.2 (só a D.1 dos quatro eixos do percentual é rodada); C.1.8 apenas na forma literal de três expressões; C.1.4 apenas na metade da conclusão-primeiro | As reprovações E4, E5 (D.1 incompleta), E6, E7 (D.2 e C.1.8), E2, E3 (teto de 45 palavras) |
| F | PARTE D.2; C.1.4 fora da primeira frase de seção; C.1.5 apenas na forma literal de três expressões; C.4.5 declarada sem ser rodada parágrafo a parágrafo | As reprovações F6, F7 (D.2), F4, F5 (C.1.4 fora da abertura), F12 (C.1.5), e o parágrafo sem proveniência de §15 (seção 5, C.4.5) |

### Declarações que a medição confirma

Vale registrar o que se sustenta, porque é a maior parte, e porque duas destas passagens são mais rigorosas que as quatro da V2.

- **C.6 nos dois blocos.** Zero acertos nas 40 entradas. O único levantamento do medidor, `robust` em E, é `cluster-robust`, verificado a mão.
- **C.1.7 nos dois blocos.** Zero travessões e zero meias-riscas em prosa corrida. As ocorrências restantes estão em marcador de nulo de célula, em faixas de página da lista de referências e, em F, nos nomes de papel do CRediT, que são a grafia da própria taxonomia.
- **C.1.3 nos dois blocos.** Nenhum parágrafo abre por conectivo de enchimento e nenhum abre por conectivo de transição da C.2. A declaração de F registra que dois parágrafos de §15 abriam em *However* e foram refeitos; a medição confirma que nenhum sobrou. É a única das seis passagens do manuscrito que descreve a correção e o resultado.
- **C.1.6 nos dois blocos.** Zero. Todas as ocorrências de primeira pessoa e de meta-verificação que o medidor levanta estão dentro das próprias tabelas de anti-tique.
- **C.1.13, as duas contagens.** E declara 56 percentuais na prosa e o medidor lê 56; F declara 23 e o medidor lê 23. As contagens são exatas nos dois blocos; o que falha é a checagem do denominador em cinco frases, não o levantamento.
- **C.2 apoio visual nos dois blocos.** E declara onze tabelas e uma figura, F declara quatorze tabelas e um formulário; o medidor conta 12 e 14 itens de exibição, e a densidade resultante, 2.072 e 2.494 caracteres por item, é a melhor do manuscrito junto com a do bloco D.
- **C.1.9 em F.** Declara 1.729 caracteres no parágrafo "What conformance does not yet establish". O medidor lê 1.717, diferença que vem da marcação, e a defesa da manutenção, não separar o desenho interlaboratorial das duas escalas que tornam o resultado legível, é boa.
- **C.2 aposição contrastiva em F.** Declara duas ocorrências; o medidor lê duas, a 0,37 por mil palavras contra um aviso em 3.
- **C.1.1 em E.** Declara uma antítese estrutural mantida de propósito, o fecho de §9.4, e nenhuma outra. O medidor confirma exatamente uma, depois de a expressão regular ter sido estendida nesta auditoria para pegar a variante com advérbio intercalado ("is therefore not X; it is Y"), que a versão anterior do medidor não via. A regra avisa na primeira e reprova na segunda; o bloco fica no aviso, e a defesa escrita é honesta.
- **C.4.1 e C.4.3 em F.** As duas declarações se sustentam em quatro dos seis parágrafos expandidos de §14 e nas duas recomendações de §13 e §15 (ver seção 5).

---

## 4. Avisos da C.2, agregados

Treze avisos nos dois blocos, para 9.281 palavras de prosa. Nenhum deles é dívida. A lista separa os cinco que valem correção dos oito que valem resposta escrita.

**Valem correção:**

1. **Bloco F, parágrafo de §15 com treze números e nenhuma proveniência.** O parágrafo "For anyone buying measurement..." carrega 35,4%, 7,8%, 70,2%, 1,91%, 53,09%, 68.624, 192, 1.083, 0,94 pp, 5,25 pp, 2.225, 0,52 e 0,58 sem uma única chave de citação, remissão de seção ou apontamento de tabela. A C.2 avisa sobre percentual sem fonte no parágrafo ou no anterior, e aqui são cinco. Correção: uma remissão por frase, às seções que já publicam cada número (§6.5 para a recuperação, §9.3 para 1,91 e 53,09, Tabela E1 para 1.083, §3.7 e a Tabela B8 para a ablação). Os dois últimos números não têm para onde apontar: ver o item 1 da seção 9.
2. **Bloco F, cadência anafórica de cinco tempos no mesmo parágrafo.** "A rate arrives with...", "It arrives per engine...", "It arrives with the effective sample...", "It arrives with the matching rule...", "And it arrives with a note...". A C.2 mede repetição de abertura entre parágrafos e não dentro deles, de modo que a declaração "No three-word opening repeats anywhere in the block" é literalmente verdadeira e cega para este caso; a nota estrutural da C.6 sobre o parágrafo de quatro tempos é o que se aplica. A lista é eficaz e não precisa morrer: basta quebrar a terceira ou a quarta ocorrência ("The effective sample travels with it, because...") para a cadência deixar de ser metronômica.
3. **Bloco E, título de gaveta em §9.1.** "What this section can and cannot claim" é o único título do bloco que nomeia a gaveta em vez da afirmação, num bloco cujos outros onze títulos carregam achado e são o melhor conjunto do manuscrito nessa exigência. Substituição que mantém a função: "Every figure here is descriptive, and the confirmatory window is still open".
4. **Bloco E, §10.3, quantidade sem contagem.** "Composite indicators serve advocacy as often as analysis [Saltelli2007]" faz uma afirmação de frequência apoiada num ensaio que não a mede. A citação satisfaz a C.1.8 e a frequência não tem número. Reescrita: "Composite indicators are used for advocacy as well as for analysis [Saltelli2007], and a custodian that sells services in the measured domain answers that objection by measuring how arbitrary its own index is and publishing the measurement."
5. **Bloco F, Tabela F1, linha 22.** A abertura de §14 declara que três linhas não carregam medição e as nomeia. A linha 22, "The metrological analogy has no unit and no hierarchy", é uma quarta que não carrega medição nem diz que não é estimável, porque por natureza não é uma quantidade. Correção de uma palavra na célula: "Not a quantity: metrological traceability requires a documented unbroken chain of calibrations [VIM2012], and no such chain, reference material or national reference exists for a citation rate."

**Valem resposta escrita, não correção:**

6. Bloco E, uma antítese graduada (§9.4), declarada e defendida. A régua avisa na primeira ocorrência e reprova na segunda; não há segunda.
7. Bloco E, §9.8, "57.5% of active entities move three or more ranks" e "35.5% move five or more". A contagem de entidades ativas não está na frase; o leitor a recupera duas frases adiante em "66 of the 111 are ever cited". Recuperável, e por isso aviso e não reprovação.
8. Bloco F, um parágrafo de 1.717 caracteres em §13. Declarado e defendido.
9. Bloco F, primeira frase de Acknowledgements com 52 palavras. Acknowledgements é bloco de declaração e não seção de argumento, o que põe o caso fora da intenção da C.1.4; registrado para o editor decidir.
10. Bloco F, cinco corridas de três parágrafos com a mesma contagem de frases, a maior do manuscrito. A passagem anti-tique declara uma, nas declarações; as outras quatro estão em §13, §14 e no Apêndice D, onde a estrutura fixa de item por item as produz. A C.3 manda reportar e nunca transformar em meta.
11. Bloco E, duas frases acima de 60 palavras (§9.8, estabilidade de ranking; §10.1, a definição dos três componentes). Diagnóstico da C.3.
12. Bloco E, três parágrafos seguidos com a mesma contagem de frases. Diagnóstico.
13. Bloco E, §9.7, o 0,342% sem denominador dentro do próprio bloco. A reescrita E3 resolve.

---

## 5. Exigências positivas da C.4

### C.4.1 Raciocínio encadeado

Dentro de E o encadeamento é bom: as 42 transições entre os seus 43 parágrafos não produzem um único parágrafo que apenas reescreva o anterior. A exceção é de subseção, não de parágrafo: **§9.7 tem 84 palavras, é a menor subseção do bloco por larga margem (a penúltima, §10.2, tem 147), e o seu conteúdo é um número que §7.1 já publica mais duas remissões que ela própria declara** ("§7.1 carries the construction... §7.2 carries the refusal taxonomy"). Não acrescenta ideia que a antecessora não contivesse. A régua manda cortar, não reescrever: a frase do piso entra no fim de §9.6, que é onde a exclusão e a concentração já estão, e §9.7 deixa de existir como subseção.

Dentro de F o defeito é maior e está em dois lugares declarados como se fossem o contrário. A passagem anti-tique afirma que "The six expanded threats in §14 each add the argument the table row cannot hold rather than restating it". Isso vale para quatro dos seis. Não vale para o segundo, sobre o intervalo, cujas duas primeiras frases refazem o cálculo que E §9.1 faz com os mesmos números; e não vale para o quinto, sobre os tetos de concordância, cujas duas primeiras frases repetem a última frase de E §9.2 quase palavra por palavra e as linhas 11 e 12 da própria Tabela F1. Em §15, três dos cinco fios abrem refazendo a derivação que E e C já fizeram, e o que cada um acrescenta são uma ou duas frases no fim. O detalhe está na seção 6, com dono e corte.

A precondição de retenção (2.225 contra 68.624) aparece três vezes dentro de F, em §13, §16 e no Apêndice E. As três são defensáveis: §13 é onde ela é a precondição do desenho interlaboratorial, §16 é a conclusão e pode reenunciar uma vez, e o Apêndice E fala do que a reprodução alcança, que é outro registro. Não proponho corte.

### C.4.2 Variação real de tamanho de período

Medida e satisfeita nos dois. E tem desvio 13,2 sobre média 26,7, com mínimo real de 5 e máximo de 77; F tem desvio 12,4 sobre média 24,3, com máximo de 55 e mínimo real de 7 se descontados os subtítulos corridos. A variação é produzida por sentido e não por cota, e as frases curtas caem nas viradas: "Answers name firms in clumps.", "Rank stability splits by unit.", "Entity ordering behaves the opposite way.", "It has no rate there.", "No pilot has compared the two." A régua proíbe transformar isso em meta e nada há a fazer.

### C.4.3 Recomendação sempre justificada

Satisfeita nos dois, e os dois têm um modelo cada.

Em E é §10.3: a recomendação ("BRGEO-1 therefore fixes the conditions of observation, requires the three components to be published beside any index, and leaves the aggregation free") vem com a evidência de um lado, 22,95 a 55,73 pontos para a janela, e com o custo do outro, mediana de 2 posições de deslocamento para a fórmula. É a justificativa mais limpa do manuscrito porque compara as duas grandezas na mesma frase.

Em F é §16: "Retention from the first observation is therefore the requirement an adopter should implement before any other, because it is the only one in the specification that cannot be satisfied retroactively [Jiang2026]", seguido do custo medido em quatro meses de respostas não guardadas. §13 (Scope) e §15 (o objeto publicado) também cumprem.

### C.4.4 A conclusão nas primeiras 120 palavras

Medida por subseção, contando as palavras até a frase que enuncia a conclusão da subseção.

- **E é o melhor bloco do manuscrito nesta exigência, com 12 de 12.** As doze subseções enunciam o achado na primeira frase: §9.2 na palavra 9 ("Citation rate is a property of the firm-engine pair"), §9.3 na 17, §9.8 na 20, §10.1 na 12, §10.2 na 17, §10.3 na 13, §11 na 14. Nenhuma quebra. As duas reprovações de C.1.4 registradas em 2.1 são de comprimento da frase, não de posição da conclusão, e as reescritas E2 e E3 preservam a posição.
- **F cumpre nas quatro seções numeradas e falha na forma em uma.** §14 entrega a conclusão em 35 palavras, §15 em 33 e §16 em 31. §13 entrega em 19 palavras, e metade dessa frase é anúncio: "are stated below" e "the rest of this section declares the design of the exercise". A reescrita F3 põe a conclusão da seção, que hoje está no sexto parágrafo, na primeira frase. Acrescente-se que §15 introduz dois anúncios que nenhuma abertura de seção cobre, F4 e F5.

### C.4.5 Uma fonte e data por parágrafo

Satisfeita em E com duas exceções, as mesmas de 2.1: o contraste por braço de §9.5 e o 39,2% de §9.8.

Em F há uma falha grande e uma pequena. A grande é o parágrafo de §15 descrito no item 1 da seção 4: treze números, nenhuma proveniência. A pequena é que §15 e §16 herdam a série e o denominador de seções anteriores sem os nomear em parágrafos que um leitor pode encontrar isolados, que é exatamente a situação de uma discussão lida depois do resumo.

### C.4.6 O fecho entrega decisão ou consequência

Medida: fecham parágrafo sem número 25,6% em E e 57,4% em F. O número por si não decide nada, porque um fecho pode entregar consequência sem cifra; E é o bloco mais numérico do manuscrito por fecho e F é o segundo menos, atrás só de C. Os defeitos são de seção.

**Em E, nove dos doze fechos de subseção entregam.** Os três que não entregam:
- §9.6 fecha em "Position inside the answer is reported in §6.6, where the relative offset stops separating the engines once the truncation is removed", que é remissão onde cabe consequência. A consequência está escrita quatro frases antes ("nothing in the count distribution requires a separate abstention mechanism") e basta trocar a ordem.
- §9.7 fecha em duas remissões, e o item de C.4.1 acima propõe dissolver a subseção.
- §9.8 fecha em "Findings of this kind carry a shelf life", uma generalidade com duas citações, quando o parágrafo anterior entrega a regra de reporte com o intervalo. Fecho proposto, com as mesmas palavras em outra ordem: "A brand in the middle band, measured in any single week, has a better than even chance of being placed three or more ranks from where the next week would place it, which is why a claim about its position needs a multi-week average or an explicit interval, and why P4 pins a model snapshot against silent provider updates [Chen2024, Mosnar2025]."

**Em F, três das quatro seções entregam e uma fecha em máxima.** §13 fecha na precondição material ("The custodian cannot presently supply the item set for the exercise it proposes"), §15 no custo de não publicar, §16 no que nunca foi guardado, que é o melhor fecho do manuscrito porque a decisão que ele impõe é irreversível e a frase diz isso em treze palavras. §14 fecha em "Writing the convention down is what makes it arguable, and it does not make it correct", que é aforismo, não decisão, e que além disso é a mesma frase com que o bloco A fecha §1.2 ("A convention has to be written down before anyone can argue about whether it is the right one"). Um dos dois sai; ver seção 6, item 3.

### C.2 Conclusão-espelho, medida

Sobreposição de palavras de conteúdo entre §16 (bloco F) e o resumo do bloco A, com lista de parada de 126 palavras funcionais e corte em três letras:

| Medida | Valor | Limiar da C.2 |
|---|---:|---|
| Palavras de conteúdo distintas em §16 | 188 | — |
| Palavras de conteúdo distintas no resumo | 101 | — |
| Compartilhadas | 56 | — |
| Sobreposição sobre a conclusão | **29,8%** | avisa em 50%, reprova em 60% |
| Sobreposição sobre o resumo | **55,4%** | faixa de aviso |
| Jaccard | **24,0%** | — |

**Veredito: passa.** A leitura que a régua pede é a da conclusão, porque o defeito que ela descreve é uma conclusão que não acrescenta, e nessa direção o valor é 29,8%, quase vinte pontos abaixo do aviso. Na direção inversa, 55,4% do vocabulário do resumo reaparece na conclusão, o que é esperado quando o resumo tem 101 palavras de conteúdo e a conclusão tem 188. As duas leituras vão registradas porque o enunciado pede a medição, e porque a segunda explica a impressão de eco que a seção deixa.

A condição de reprovação da C.2 exige, além da sobreposição, que a conclusão não traga número novo. §16 traz cinco: a reversão de 1,86% para 33,3%, a cobertura de 37,4% sobre 139 dias, o piso de falso positivo de 0,0056%, os 56 de 90 dias com fechamento projetado em 2026-10-15, e a precondição de 2.225 contra 68.624 como consequência de fecho. Repete cinco: a faixa da janela, 68.624, o efeito de desenho de 63,3, a amostra efetiva de 1.083 e a partilha de variância. Deixa de fora dois que o resumo carrega: o kappa de 0,086 e a faixa de 0,706 a 0,984. O saldo é uma conclusão que acrescenta mais do que espelha, e o único reparo é o da declaração, no item 7 da seção 3.

---

## 6. Redundância entre blocos

Foi o maior achado da V2 e continua sendo o maior aqui. O detector de 7-gramas de palavras de conteúdo acusa **zero** casamentos entre E e F, o que não é ausência de repetição: é a assinatura de repetição reescrita, que nenhum detector literal pega e que só a leitura acha. As sete passagens abaixo foram achadas lendo. Duas delas já estavam na lista da V2 e pioraram, porque F acrescentou uma quarta e uma quinta ocorrência.

| # | Passagem | Onde aparece hoje | Dono proposto | Corte proposto |
|---|---|---|---|---|
| 1 | **Decomposição de variância** (34,46 / 26,21 / 39,33; dia a 0,28% sobre 42.487 células) | A resumo · **E §9.2 + Tabela E2** · F Tabela F2 · **F §15 ¶4** · F §16 | **E §9.2** | As duas primeiras frases de F §15 ¶4, que reenunciam as duas primeiras de E §9.2 |
| 2 | **Efeito de desenho por prompt** (1,32 / 63,3 / 1.083 / 0,29 para 2,29) | A destaque · A resumo · A §1.2 · **E §9.1 + Tabela E1** · E §11 · F Tabela F1 l.6 · **F §14 ¶2** · F §15 ¶5 · F §16. Nove enunciados | **E §9.1 com a Tabela E1** | As duas primeiras frases de F §14 ¶2 |
| 3 | **Notas do VIM e "constituted by convention"** | **A §1.2** (três parágrafos) · B §3 · D §6.1 · F Tabela F1 l.22 · **F §14 ¶6** · F §15 ¶2 | **A §1.2** para a montagem (VIM 2.3 Nota 1 e 2.27) e **F §14 ¶6** para o limite (a cadeia documentária, que só F tem) | A segunda frase e o fecho de A §1.2 último parágrafo, que F §14 reenuncia com outras palavras, inclusive o mesmo aforismo em duas redações |
| 4 | **História da detecção** (nenhum controle pegou, 223 testes verdes, máximo igual ao mínimo em 15.168) | Inventário de controles: **C §5.3** e **F §15 ¶3**. Regra do máximo igual ao mínimo: B §12.3 · C §5.4 · D §6.2 · **F §15 ¶3**. Quatro blocos | **C §5.3** para o incidente e o inventário, **F §15** para a lição transferível, uma frase | O inventário de controles de F §15 ¶3, hoje a única cópia do de C §5.3 depois que D o reduziu a remissão às 13h47; e a terceira e a quarta enunciação da regra do máximo igual ao mínimo, em B §12.3 e D §6.2, que passam a remissão. A V2 já havia alocado esta passagem a C §5.3; D e B aplicaram parte da alocação nesta tarde e F acrescentou uma ocorrência nova que nenhuma das duas passagens viu |
| 5 | **Calendário** (52 dias em 139, 37,4%, buraco de 59 dias, julho vazio) | **C §8.2** · E §9.8 ¶1 · F Tabela F1 l.7 · **F §14 ¶3** · F Apêndice D | **C §8.2** para a análise e **F Apêndice D** para o registro (é o razão, e enumerar é a sua função) | As duas primeiras frases de F §14 ¶3, que a linha 7 da Tabela F1 já carrega |
| 6 | **Tetos de concordância** (kappa teste-reteste 0,669 sobre 2.687 e 0,725 sobre 288; painel de seis que nunca existiu) | **E §9.2** ¶final · F Tabela F1 l.11 e l.12 · **F §14 ¶5** | **E §9.2** | As duas primeiras frases de F §14 ¶5 |
| 7 | **Piso de decoys** (0 em 68.624, Wilson 0,0056%) | A §2.4 · B Tabela B8 l.5 · **D §7.1** · **E §9.7** · F Tabela F1 l.4 · F Tabela F2 · **F §15 ¶6** · F §16. Oito enunciados | **D §7.1** | A subseção E §9.7 inteira, reduzida a uma frase no fim de §9.6; e a construção reenunciada em F §15 ¶6 (16 vagas, verificação, mesma bateria e mesmos adaptadores), que D §7.1 já publica |

**Economia: cerca de 500 palavras de prosa, sem perda de um número.** O ganho maior não é o espaço. É que hoje o revisor que lê o manuscrito montado encontra o mesmo cálculo do efeito de desenho nove vezes em quatro redações, e a regra do máximo igual ao mínimo em quatro blocos, o que a linha 5 da A.10 chama de estrutura pouco clara e o que a nota estrutural da C.6 descreve como texto que lê como gerado mesmo com o léxico limpo.

### Reescritas prontas, para os quatro cortes maiores

**(1) F §15 ¶4, decomposição de variância.** Substituir o parágrafo por:

> Citation is a property of the firm-engine pair, and §9.2 puts the interaction above either main effect. A measurement bought from one engine therefore estimates a quantity that does not transfer, and the effect is visible at the level of individual firms: of the twenty entities named by exactly one engine in five months, seventeen are named only by the retrieval-augmented arm, and they are the mid-cap and long-tail names. A firm in that position does not have a low rate on the other engines. It has no rate there, and a dashboard that pools the panel into one number will report the two cases identically.

**(2) F §14 ¶2, efeito de desenho.** Substituir as duas primeiras frases por uma:

> **The interval this paper publishes depends on which claim it is making.** Table E1 puts the prompt design effect at 63.3 and the day-clustered inflation of the pooled standard error at 1.32, with three of five arms showing no day-level inflation at all, because every round re-asks the same fixed battery and a day is close to a census of the prompt population. Any statement in this paper that generalises beyond these 192 prompts carries the second interval, and any statement about these 192 prompts carries the first. The distinction is the reason §9 reports strata descriptively and the reason a published rate whose interval came from the observation count is reporting a quantity below the floor that definitional uncertainty already sets [VIM2012].

**(5) F §14 ¶3, calendário.** Substituir as duas primeiras frases:

> **The calendar removes the events that matter most.** The coverage of row 7 of Table F1 would be a power problem on its own; the shape of the hole makes it a design problem, since 15 of 21 event-by-arm pairs cannot be tested because a hole sits on the boundary. The events and the outages have common causes: the late-August gap exists because the fifth arm consumed 129 of 179 minutes of a run, and the fix for that consumption is itself a declared configuration event. A study that waits for its own instrument changes to happen cannot measure them, which is why §3 requires the boundary to be declared in advance and stratified by rule.

**(6) F §14 ¶5, tetos de concordância.** Substituir as duas primeiras frases:

> **Two of the paper's agreement statements are read against ceilings rather than against unity.** Rows 11 and 12 of Table F1 carry the two facts: the six-engine panel the design describes never existed, and the two affected arms disagree with themselves twelve hours apart. Part of what this paper counts as disagreement between engines on those arms is that self-disagreement, and no decomposition separates the two components. The Fleiss figures of §9 are therefore lower bounds on the agreement a stable instrument would report, in the same direction as the window correction and for a different reason.

---

## 7. Voz

Os dois registros são legítimos e diferentes, e um dos dois tem um problema.

| Marcador | A | B | C | D | **E** | **F** |
|---|---:|---:|---:|---:|---:|---:|
| Máxima generalizante fechando parágrafo | 0 | 3 | 3 | 0 | **2** | **6** |
| Fechos de parágrafo sem número | 39,4% | 53,3% | 60,6% | 38,1% | **25,6%** | **57,4%** |
| Percentuais na prosa | 19 | 5 | 8 | 46 | **56** | **23** |
| `rather than` por 1.000 palavras | 0,77 | 6,34 | 3,75 | 2,34 | **3,36** | **6,10** |
| Frases abrindo por adjunto | 15,3% | 8,4% | 15,4% | 16,1% | **10,3%** | **13,5%** |

As quatro linhas medidas por script trazem os seis blocos no estado de 13h47. A linha das máximas é contada a mão: os valores de A a D são os da V2 e podem ter mudado nas edições desta tarde; os de E e F são desta leitura.

**E é voz de resultado, e é a mais disciplinada do manuscrito.** Cinquenta e seis percentuais na prosa, o maior número dos seis blocos, e o menor índice de fecho sem cifra, 25,6% contra 38 a 61 nos outros cinco. A estrutura é sempre a mesma e sempre funciona: uma frase que enuncia o achado, uma tabela, um parágrafo que diz o que a tabela não pode sustentar. As duas melhores frases do bloco são as que recusam a conclusão fácil: "Fintech records 2 anchor matches in 137,800 entity slots, so its rate ratio is numerically unstable and is tabulated without interpretation" e "The sentence 'citation follows a power law' is not available from this design". Um artigo escrito pelo custodiante da especificação avaliada precisa exatamente disso, e a A.10 linha 6 explica por quê. Nada nesta voz deve ser mexido.

**F é voz de encerramento, e o risco previsto pelo enunciado se confirma: a máxima generalizante.** Seis fechos de parágrafo entregam um aforismo em vez de uma consequência, o dobro do que a V2 mediu em B e C e contra zero em A e D:

1. §13: "An adopter who forks the cohort file, the battery generator and the extractor owes nothing and asks nothing."
2. §13: "Adjacent problems take their own numbers, which is what allows an adopter to conform on observation without adopting anything else."
3. §14: "A protocol that fixes six parameters while a seventh of unknown magnitude varies freely has not finished the job."
4. §14: "A study that waits for its own instrument changes to happen cannot measure them."
5. §14: "Writing the convention down is what makes it arguable, and it does not make it correct."
6. §15: "A vendor who reports a confidence interval derived from the observation count is reporting a term below the floor."

Mais três de cadência aforística menor, no Apêndice C ("A claimant who cannot fill a field writes what is missing in it rather than deleting the line"), no Apêndice E ("A figure present in a table and absent from `NUMBERS.md` came from a measurement nobody can repeat") e em §15 ("which is a different instrument and a different number").

O problema não é o registro, é a concentração e o lugar. Todas as seis fecham parágrafo, e três fecham parágrafos vizinhos dentro de §14, o que converte o argumento numa sequência de sentenças. Num artigo em que o autor é o custodiante do que mede, o tom de sentença é lido como advocacia, que é a leitura que a A.10 linha 6 já trata como risco de triagem, e §13 e a declaração de interesse concorrente são precisamente as seções em que ela custa mais caro.

**Ajuste mínimo, três movimentos, sem uniformizar.**

1. **Teto de uma máxima por seção, e no fecho da seção, não no de um parágrafo interno.** Em §14 isso preserva a número 3, que é a máxima ganha do bloco porque vem depois dos 22,95 a 55,73 pontos que a justificam, e converte as outras duas nas suas evidências. A número 4 fica: "The events and the outages have common causes, which is why §3 requires the boundary to be declared in advance and stratified by rule." A número 5 sai, porque o bloco A já a diz (seção 6, item 3), e §14 passa a fechar na cadeia documentária, que é o que só ele tem.
2. **Onde a máxima está ao lado do número, junte os dois.** §13: "An adopter who forks the cohort file, the battery generator and the extractor owes nothing and asks nothing" fica a uma frase de CC BY 4.0 e Apache-2.0. Unir: "The specification is published under CC BY 4.0 and the reference implementation under Apache-2.0, which carries an explicit patent grant, so an adopter who forks the cohort file, the battery generator and the extractor owes no royalty and asks no permission." A cadência aforística sai, o conteúdo fica, e a declaração de licença ganha em precisão jurídica.
3. **Em §15, trocar as duas frases de roteiro pelo argumento** (reprovações F4 e F5). São os dois únicos pontos do bloco em que a voz sai do relato para narrar o documento, e sair delas aproxima F do registro de E sem tocar em nada que F faz bem.

O que não deve ser tocado: a densidade numérica de E, a estrutura de registro da Tabela F1, o fecho de §16, e o tom das declarações obrigatórias, que estão entre as melhores páginas do manuscrito. A declaração de interesse concorrente em particular faz o que a A.7.2 pede e mais: nomeia o interesse, nomeia o benefício comercial, e depois lista quatro restrições estruturais em vez de pedir confiança. Essa página não precisa de estilo nenhum, só de ficar como está.

---

## 8. O que eu corrigiria primeiro, em ordem de impacto

1. **As três referências de versão interna** (E §11, F §15, F Tabela F1 linha 16). Três edições, reparos já escritos em 2.1 e 2.2. C acabou de limpar as suas seis nesta mesma tarde; enquanto estas ficarem, E e F são os dois blocos que fazem o artigo ler como revisão de um documento que o leitor não pode obter, e são também as três declarações anti-tique de severidade alta que caem junto.
2. **A repetição entre blocos** (seção 6, sete itens, cerca de 500 palavras). Nenhuma passagem anti-tique individual enxerga, porque cada uma roda sobre o seu próprio arquivo; o revisor lê o manuscrito montado. Dois dos sete itens já estavam na lista da V2 e ganharam uma quarta e uma quinta ocorrência em F, o que mostra que a alocação por dono precisa ser decidida antes da montagem e não depois.
3. **As cinco porcentagens sem denominador** (E §9.5, E §9.8, F §14, F §16, F §15). A de F §16 é a mais urgente das cinco, porque está na conclusão, porque o denominador que aparece na frase pertence ao outro número, e porque o reparo usa um número que o próprio bloco já publica duas seções antes. Duas das outras precisam de n que sai de `stats/data/`.
4. **As três afirmações de ausência não medidas** (F §16 "the field currently publishes the quantity without them", F §15 "the one most often skipped", E §10.3 "the market practice"). A de F §16 fecha o primeiro parágrafo da conclusão e contradiz a ressalva que o bloco A publica em §2.8; é o tipo de inconsistência que um revisor acha primeiro.
5. **O parágrafo de F §15 com treze números e nenhuma proveniência**, junto com os dois números órfãos que ele contém (mediana de Kendall tau-b 0,52 em fintech e 0,58 em varejo, que não aparecem em nenhum outro lugar do manuscrito). O Apêndice E do próprio bloco condena a frase: "A figure present in a table and absent from `NUMBERS.md` came from a measurement nobody can repeat."
6. **As cinco aberturas que anunciam em vez de concluir ou que estouram o teto** (F §13, F §15 duas vezes, E §9.5, E §9.7). Uma edição cada, e as cinco melhoram a C.4.4 no mesmo movimento.
7. **Os dois casos de autonarração** (E §11, F §13). Corte puro em um, cinco palavras no outro.
8. **Os seis fechos em máxima de F** (seção 7). Teto de uma por seção, e a que sai de §14 sai porque o bloco A já a diz.
9. **§9.7 de E dissolvido em §9.6** e o fecho de §9.8 reordenado (seção 5, C.4.1 e C.4.6). Oitenta e quatro palavras a menos e uma subseção a menos no sumário.
10. **Os cinco avisos que valem correção** (seção 4, itens 1 a 5).

---

## 9. Fora da régua, para decisão do editor

Nada aqui é regra da PARTE C. São sete pontos que incomodaram durante a leitura e que a régua não cobre.

1. **Dois números que não existem fora da frase que os usa.** F §15 fecha em "the ranking inside a vertical, at median Kendall tau-b of 0.52 in fintech and 0.58 in retail, rather than the level". Uma varredura dos seis blocos não encontra 0,52 nem 0,58 como tau-b em nenhum outro lugar; E §9.8 publica tau-b de 0,871 sobre a coorte inteira, 0,800 sobre as ativas e sobreposição de 0,892 no top-10, nenhum deles por vertical. Ou os dois números saem de um corte que nenhum bloco publica, e então precisam de tabela, ou são de outra grandeza. Não alterei nenhum dos dois.

2. **Marcador de tarefa em português dentro da prosa em inglês.** O bloco E carrega, entre dois parágrafos de §9.2, a linha `[INCLUIR: modelo multinível de S1]`. A seção "Open marks and number provenance" explica por que o buraco existe e o que entra ali, o que é a conduta certa, mas o marcador em si está no corpo do manuscrito e não pode chegar à montagem. A seção de marcas abertas também menciona "the commissioning brief" três vezes, que é aparato de produção e não texto de artigo; junto com "Notes for the integrator" do bloco F, são as duas seções que a montagem precisa remover explicitamente, ao lado de "Reference keys used" e "Anti-tic pass".

3. **A mesma quantidade com duas precisões, a dois parágrafos de distância no manuscrito montado.** O resumo do bloco A diz "39.3% of the variance in coverage"; F §16 diz "39.33% of the variance in coverage"; E Tabela E2 e F §15 dizem 39,33%. Uma das duas grafias deve ceder, e a do resumo é a que tem teto de palavras.

4. **Erro de concordância no fecho de §15.** "two figures that differ by tens of percentage points are both correct and **neither reader** can tell why". Não há um par de leitores no antecedente. A forma é "and no reader can tell why".

5. **`rather than` como destino de todas as antíteses removidas, agora medido em seis blocos.** A V2 propôs aviso acima de 4 por mil palavras. Com os seis blocos na mesa: A 0,77, D 2,34, E 3,36, C 3,75, F 6,10, B 6,34. F é o segundo mais carregado e a maior parte dos seus 33 usos é legítima, mas uns quinze são o mesmo objeto visto duas vezes sem informação sobre o primeiro termo: "declared here rather than deferred as future work", "a floor rather than an estimate", "constituted by convention rather than discovered", "argued rather than inherited from a passing suite", "the instrument of this study rather than assistance with manuscript preparation". A proposta da V2 continua de pé e agora tem seis pontos de dado.

6. **Travessão em título de norma dentro da lista de referências.** F declara que as meias-riscas restantes estão só nos nomes de papel do CRediT e que os travessões estão só em marcador de nulo e faixa de página. Os títulos de `[ISO5725]`, `[ISO17000]` e `[VIM2012]` carregam travessão, porque é a grafia oficial das normas. A C.1.7 tolera travessão em título e em célula de tabela e não fala de lista de referências; a grafia oficial de uma norma não é alterável de qualquer modo. Registro só para a próxima passagem não perder tempo com isso.

7. **Cobertura.** Esta auditoria leu E e F por inteiro e comparou-os contra A, B, C e D no estado de 11/09/2026 às 13h47, com quatro desses arquivos em edição ativa. Toda remissão proposta acima assume que §1 a §8 e §12 existem com a numeração que os seis blocos usam. A alocação por dono da seção 6 deve ser conferida contra a versão final de A, B, C e D antes de ser aplicada, e em particular o item 3 (notas do VIM) propõe um corte dentro do bloco A, que está fora do escopo de edição desta revisão.

---

## Anexo. Como reproduzir a medição

```
cd journal-v2/reviews
python style_check.py                  # os seis blocos, relatorio legivel
python style_check.py --blocks EF      # so E e F
python style_check.py --extra          # medidas entre blocos e exigencias positivas
python style_check.py --json           # os mesmos numeros em JSON
```

Quatro mudanças foram feitas em `style_check.py` nesta auditoria, todas dentro de `reviews/`, nenhuma no texto dos blocos.

1. **E e F entraram na lista de arquivos**, e o cabeçalho da tabela passou a ser gerado a partir dos blocos medidos em vez de ficar preso em quatro colunas. `--blocks` seleciona um subconjunto.
2. **Duas seções novas entraram na lista de exclusão de prosa**: "Open marks and number provenance" (bloco E) e "Notes for the integrator" (bloco F). São nota ao editor e ao montador, não texto do manuscrito, e o mesmo tratamento já se aplicava a "Provenance note" no bloco A. Sem essa exclusão, o bloco E ganharia 325 palavras de prosa que ninguém vai publicar e o bloco F ganharia 267.
3. **A expressão regular da antítese graduada ganhou a variante com advérbio intercalado**, `is/are + <advérbio> + not ... ; it is`. Sem ela, a antítese que o bloco E declara ter mantido de propósito no fecho de §9.4 não era medida, e a declaração não podia ser conferida. A mudança não altera nenhum resultado dos blocos A a D.
4. **Três medidas novas**: a sobreposição de palavras de conteúdo entre duas passagens, para a conclusão-espelho da C.2; o índice de 7-gramas de palavras de conteúdo entre blocos, para a redundância da C.4.1; e, por seção, as primeiras 120 palavras e a última frase, para a C.4.4 e a C.4.6, mais o percentual de fechos de parágrafo sem cifra.

O que o script continua não fazendo, e por quê: ele não julga denominador, não julga afirmação de ausência e não julga redundância parafraseada. Lista percentual com contexto, lista candidato e deixa a decisão para a leitura. O detector de 7-gramas desta rodada mediu zero casamentos entre E e F enquanto a leitura achava cinco passagens duplicadas entre eles, o que é a demonstração mais limpa de que um medidor literal não substitui a releitura que a C.4.7 exige.
