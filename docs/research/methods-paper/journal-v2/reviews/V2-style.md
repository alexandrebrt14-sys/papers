# V2-style. Auditoria de estilo dos blocos A a D contra a PARTE C

Revisão de estilo da casa sobre `sections/A-front-intro-related.md`, `sections/B-specification-instantiation-adoption.md`, `sections/C-field-record-missingness.md` e `sections/D-window-decoys.md`, contra a PARTE C inteira de `research/R4-standards.md` (C.1 reprovação, C.2 aviso, C.3 diagnóstico, C.4 exigências positivas, C.5 regras que ficaram de fora, C.6 léxico de máquina), com a PARTE D.2 acionada onde a PARTE C remete a ela.

Medição feita por `reviews/style_check.py`, executado sobre o estado em disco de 11/09/2026 às 13h35. Os blocos A e C foram revistos pelos redatores durante a leitura desta auditoria (mtime 13h34 e 13h35); tudo o que segue descreve a versão revista, e as declarações do bloco que já foram corrigidas nessa passagem aparecem marcadas como tal.

Escopo de prosa do medidor: fora do denominador ficam tabelas, blocos de código, títulos, listas de referência, legendas de tabela e figura, a especificação da Figura D1, a seção "Reference keys used" e a própria seção "Anti-tic pass". A auditoria das declarações do redator é feita à parte, na seção 3.

---

## 1. Sumário medido, por regra e por bloco

| Regra e limiar | A | B | C | D |
|---|---:|---:|---:|---:|
| Palavras de prosa | 3.835 | 4.360 | 3.412 | 3.455 |
| Caracteres de prosa | 26.314 | 28.276 | 21.754 | 22.498 |
| Parágrafos de prosa | 33 | 44 | 32 | 43 |
| **C.1.1** antítese de fórmula fechada | 0 | 0 | 0 | 0 |
| **C.1.1** antítese graduada (`is not X: it is Y`) | 0 | 0 | 0 | **2** |
| **C.1.1 veredito** (avisa na 1ª, reprova na 2ª) | ok | ok | ok | **FALHA** |
| **C.1.2** fecho pseudo-profundo | 0 | 0 | 0 | 0 |
| **C.1.3** conectivo de enchimento abrindo parágrafo | 0 | 0 | 0 | 0 |
| **C.1.3** densidade de conectivo gasto, por 250 palavras (limiar 1,00 com piso de 4) | 0,07 | 0,00 | 0,00 | 0,00 |
| **C.1.4** primeira frase de seção acima de 45 palavras | 0 | **2** | 0 | **1** |
| **C.1.5** autonarração fora do parágrafo de contribuições | **1** | 0 | 0 | 0 |
| **C.1.6** meta-discurso de verificação fora do método | 0 | 0 | 1 (limítrofe) | 1 (limítrofe) |
| **C.1.7** travessão ou meia-risca em prosa corrida | 0 | 0 | 0 | 0 |
| **C.1.8** atribuição vaga sem fonte na frase | **1** | 0 | 0 | **1** |
| **C.1.9** maior parágrafo, em caracteres (avisa 1.500, reprova 2.200) | 1.331 | 1.671 | 1.159 | 1.152 |
| **C.1.9** parágrafos acima de 2.200 | 0 | 0 | 0 | 0 |
| **C.1.10** adjetivos vazios (reprova em 5 no texto ou raiz acima de 2) | 0 | 0 | 1 técnico | 0 |
| **C.1.11** rótulo de confiança sem medição | 0 | 0 | 0 | **1** |
| **C.1.12** alerta rotulado abrindo parágrafo | 0 | 0 | 0 | 0 |
| **C.1.13** porcentagem sem denominador recuperável | 0 | 0 | 0 | **2** |
| **C.1.14** histórico de versão ou nota de edição na prosa | 0 | 0 | **6** | **7** |
| **PARTE D.2** afirmação de ausência não medida | **1** | **2** | 0 | **1** |
| **C.2** aposição contrastiva `X, not Y`, por 1.000 palavras (avisa 3, reprova 5) | 0,00 | 0,46 | 0,00 | 0,00 |
| **C.2** abertura de parágrafo repetida 3 vezes | 0 | 0 | 0 | 0 |
| **C.2** parágrafos acima de 1.500 caracteres | 0 | 1 | 0 | 0 |
| **C.2** intensificadores em série (avisa em 3) | 0 | 0 | 1 | 0 |
| **C.2** advérbios em `-ly` no parágrafo mais carregado (avisa em 4) | **5** | 3 | 3 | 3 |
| **C.2** perguntas retóricas (avisa acima de 1 por 300 palavras, piso 3) | 0 | 0 | 0 | 0 |
| **C.2** introdutores de fonte, por 120 palavras (avisa acima de 1) | 0,00 | 0,00 | 0,00 | 0,00 |
| **C.2** caracteres de prosa por item visual (avisa acima de 5.000) | **13.157** | 3.534 | **10.877** | 1.875 |
| **C.6** entradas do léxico de 40 itens | 0 | 0 | 0 | 0 |
| **C.3** frase média, em palavras (diagnóstico) | 25,6 | 25,1 | 24,2 | 24,5 |
| **C.3** desvio padrão da frase (diagnóstico) | 13,5 | 14,1 | 11,7 | 13,2 |
| **C.3** frase mais curta e mais longa (diagnóstico) | 2 / 65 | 3 / 70 | 3 / 58 | 1 / 55 |
| **C.3** frases acima de 60 palavras (diagnóstico) | 1 | 2 | 0 | 0 |
| **C.3** três parágrafos seguidos com a mesma contagem de frases (diagnóstico) | 5 | 2 | 3 | 2 |
| **C.3** frases abrindo por adjunto (diagnóstico) | 14,7% | 8,6% | 14,9% | 13,5% |
| Fora da régua: `rather than` em prosa, por 1.000 palavras | 0,5 | **6,7** | 3,8 | 1,4 |

Contagem de reprovações confirmadas: **A 2, B 4, C 3, D 7**. O léxico da C.6 está limpo nos quatro blocos, o travessão está limpo nos quatro, e nenhum parágrafo chega perto do teto de 2.200 caracteres. As reprovações não estão no vocabulário; estão na estrutura, e concentram-se no bloco D.

Dois falsos positivos do medidor, verificados a mão e descartados: `Overall` no bloco A é o quantificador de "13.7% of queries overall", não conectivo; `not only` no bloco D é "and not only in aggregate", não a fórmula `not only X but also Y` da C.6 #31.

---

## 2. Achados de reprovação, bloco a bloco

As reescritas abaixo estão prontas para colar. Nenhuma altera um número, nenhuma enfraquece uma ressalva. Onde a reescrita precisa de um dado que o bloco não publica, isso vem dito na própria linha.

### 2.1 Bloco A

| Trecho literal | Regra | Reescrita proposta |
|---|---|---|
| §2.8, fecho: "The contribution of this paper sits in the row that the others leave blank, and it arrives with its own failures attached: the specification in §3, the field record of five defects that passed every automated check in §5, the symmetric measurement of the window in §6.5, five months of descriptive evidence in §9, and the evidence against the reporting index in §10, published by the custodian of the index." | **C.1.5** autonarração fora da única passagem de roteiro permitida, que a regra adaptada localiza no fim da introdução. §2.8 é trabalho relacionado. Agrava: o próprio "Anti-tic pass" declara que esta passagem foi escrita para substituir um fecho pseudo-profundo, ou seja, a correção de C.1.2 produziu a violação de C.1.5. | "The row that the others leave blank is where BRGEO-1 sits, and it arrives with its failures attached: six parameters with a failure mode each (§3), five defects that passed every automated check (§5), the window measured symmetrically on 2,225 matched observations (§6.5), five months of descriptive evidence (§9), and the evidence against the reporting index, published by its custodian (§10)." |
| §1.1: "The last of those four is the one no vendor publishes." | **PARTE D.2** afirmação de ausência sem medição, e **C.1.8** atribuição vaga sem fonte na frase. O mesmo bloco recusa explicitamente esta classe de afirmação em §2.8 ("whether published visibility studies declare an extraction window at all has not been surveyed here"), o que deixa o parágrafo de abertura em contradição com a ressalva do bloco. | "The last of those four is the condition §6.5 measures, and §2.8 records that whether published studies declare it has not been surveyed here." |

### 2.2 Bloco B

| Trecho literal | Regra | Reescrita proposta |
|---|---|---|
| §4.5, primeira frase, 70 palavras: "The rule is the project's own extractor over the v2 cohort with anchors and decoys included: word-boundary matching under `\b`, a dual pass preserving NFC and folding NFKD so that a Portuguese name written without diacritics in an English response still matches, markup stripping so that bold formatting and bracketed reference markers do not break the boundary, an alias table, an ambiguity guard requiring the canonical form, and exclusion contexts." | **C.1.4**, teto de 45 palavras na primeira frase de seção. | "The rule is the project's own extractor over the v2 cohort, with anchors and decoys included. It matches on word boundaries under `\b`, runs a dual pass preserving NFC and folding NFKD so that a Portuguese name written without diacritics in an English response still matches, strips markup so that bold formatting and bracketed reference markers do not break the boundary, and applies an alias table, an ambiguity guard requiring the canonical form, and exclusion contexts." (primeira frase: 17 palavras) |
| §4.2, primeira frase, 48 palavras: "The 192 canonical queries are generated rather than curated, from five declared axes, so the balance is a property of the construction and not of an editorial pass: 96 Portuguese and 96 English, 96 directive and 96 exploratory, 48 per vertical, with half of each cell carrying the temporal frame "em 2026" and half atemporal." | **C.1.4**, teto de 45 palavras. | "The 192 canonical queries are generated from five declared axes, so the balance is a property of the construction and not of an editorial pass. The cells run 96 Portuguese and 96 English, 96 directive and 96 exploratory, 48 per vertical, with half of each cell carrying the temporal frame "em 2026" and half atemporal." (primeira frase: 26 palavras; sai também um `rather than`) |
| §3.1, P6: "A parameter that nobody has measured stops being a rhetorical declaration when somebody publishes its magnitude, including when the magnitude is zero." | **PARTE D.2**, negativa universal sobre a literatura sem a busca que a licencia. O bloco A recusa a mesma classe de afirmação. | "The magnitude, including when it is zero, is what turns a declared parameter into a checkable one, which is why the ablation is published here with its flip counts." |
| §3.7: "Applied to a citation rate, the division does work that no existing reporting format in this market does." | **PARTE D.2**, afirmação de ausência sobre todos os formatos de reporte do mercado, sem levantamento. | "Applied to a citation rate, the division separates the components a sample count can estimate from the components only a declared parameter removes, which is what Table B4 carries." |

### 2.3 Bloco C

| Trecho literal | Regra | Reescrita proposta |
|---|---|---|
| §8.2: "the table build counts 53 and its stated conventions fix no day rule. **The manuscript should settle on one before submission.**" | **C.1.14**, instrução de processo editorial dentro da prosa. Histórico e decisão de edição vivem no repositório, não no texto publicado. | Corte da última frase. Se o editor puder garantir a afirmação, a alternativa que preserva a informação é: "Every figure in this paper that depends on the day count states which of the two it uses." Enquanto a decisão não estiver tomada, o corte é a opção segura, e a decisão 52 contra 53 entra na lista de prioridades. |
| §8, abertura: "The event table of **v1.0** carried four of the seventeen boundaries the record supports." §8.1: "The four events in **v1.0** were the ones that forced an analytic decision at the time". Legenda da Tabela C2: "the four events declared in the **v1.0** event table". §8.4: "The one that coincides is not in the **v1.0** event table". §5.3: "Two of the four series events declared in **v1.0**". Seis ocorrências. | **C.1.14**, histórico de versão na prosa. O leitor do artigo publicado não tem acesso a um documento interno chamado v1.0 e não consegue resolver a referência. | Substituir o rótulo interno pelo registro datado a que ele se refere, mantendo todos os números. §8: "The event register as it stood at the first analysis carried four of the seventeen boundaries the record supports." §8.1: "The four registered events were the ones that forced an analytic decision at the time". Legenda da Tabela C2: "the four events in the register as first published". §8.4: "The one that coincides is not among the four registered events." §5.3: "Two of the four registered series events came from generation configuration, which is why it became parameter P5." |
| §5.3: "The magnitude appears in §6. **What belongs here is that** 223 tests passed on the day it was found." | **C.1.4**, anúncio no lugar da coisa. A frase narra o arranjo do documento antes de dar o dado. | "The magnitude appears in §6. On the day the asymmetry was found, 223 tests passed." |

### 2.4 Bloco D

| Trecho literal | Regra | Reescrita proposta |
|---|---|---|
| §6.1, primeira frase: "Entity extraction runs over a string, and that string **is not** the model's answer**: it is** whatever the pipeline retained." | **C.1.1**, forma graduada `it is not X: it is Y`, primeira ocorrência. Agrava: o "Anti-tic pass" do bloco declara que a antítese da abertura de §6.1 foi removida, e a frase que ocupou o lugar reintroduz a mesma estrutura. | A reparação já está escrita no bloco B, §3.1 P1, com os mesmos fatos: "Entity extraction runs over a string, and that string is whatever the pipeline retained rather than the model's answer." |
| §6.2: "A variable whose maximum equals its minimum across 15,168 observations **is not** measuring anything**; it is** reporting a boundary." | **C.1.1**, forma listada `this is not X; it is Y`. Segunda ocorrência no mesmo texto, o que converte o aviso da regra graduada em reprovação do bloco. | A reparação já está escrita no bloco B, §12.3: "A variable whose maximum equals its minimum across 15,168 observations is reporting a boundary rather than measuring a length." O bloco C, §5.4, resolve o mesmo fato pela mesma via: "A mean equal to a maximum across tens of thousands of rows reports a boundary rather than a measurement." |
| §6.3: "**Manuscript v1.0** reported the same contrast on the series that closed on 2026-08-31, 75.7% against 51.9% over 66,399 observations, a difference of 23.8 points; the gap between the two figures is the 305 rows collected under the uniform window after 2026-08-31, which the earlier snapshot did not contain." | **C.1.14**, errata de versão anterior dentro do texto. O parágrafo explica a diferença entre dois números publicados por duas versões do mesmo manuscrito, que é exatamente o registro de correção que a regra manda sair da prosa. | "On the series that closed on 2026-08-31, the same contrast runs 75.7% against 51.9% over 66,399 observations, a difference of 23.8 points; the gap between that figure and the one above is the 305 rows collected under the uniform window after 2026-08-31, which the earlier snapshot did not contain." (os quatro números permanecem) |
| §6.6: "The discourse-structure account advanced in **v1.0**…"; "…a criterion that **v1.0** described in prose and never committed, and it diverges from the published **v1.0** shares by up to 5.2 points"; §6.3: "the reading **v1.0** avoided". Sete ocorrências no bloco. | **C.1.14**. | "The discourse-structure account, that retrieval-augmented engines compose after fetching sources and therefore defer naming, is refuted by Table D2"; "…a criterion described in prose and never committed, and it diverges from the shares computed under that prose criterion by up to 5.2 points on individual arms". |
| §6.3: "Reading them as evidence that the window does not matter on the parametric arms was the reading v1.0 avoided and **the market did not**, and §6.4 shows what it would have cost." | **PARTE D.2** e **C.1.8**. Afirmação sobre o que "o mercado" fez, sem medição e sem fonte na frase. O bloco A recusa explicitamente afirmar o que a prática publicada faz. | "Reading them as evidence that the window does not matter on the parametric arms is the misreading the table invites, and §6.4 shows what it would have cost." |
| §6.6: "Grok shows the same pattern across verticals, with preamble share running from **2.6%** in fintech to **16.7%** in technology and the window delta from +35.4 to +72.9 points over those cells." | **C.1.13**. O n das células por vertical não está na frase, na frase anterior, nem em nenhuma tabela do bloco: a Tabela D7 é por motor (Grok n = 768) e não desce a vertical. | "Grok shows the same pattern across verticals, with preamble share running from 2.6% in fintech to 16.7% in technology over cells of n = [x] and n = [y], and the window delta from +35.4 to +72.9 points over those cells." Os dois n saem de `stats/data/`; esta auditoria não os inventa. Alternativa sem dado novo: publicar a coluna de n por célula numa nota da Tabela D7 e apontar a frase para ela. |
| §6.6: "Gemini's preamble share is 36.46% on this three-day cohort against **80.03% on the full series** under the same pattern". | **C.1.13**. O 36,46% recupera o denominador na Tabela D7 (n = 768); o 80,03% não aponta para tabela alguma. | "Gemini's preamble share is 36.46% on the 768 observations of this three-day cohort against 80.03% on the 15,355 canonical observations of the full series under the same pattern". Os dois denominadores já estão no bloco: 768 na Tabela D7 e 15.355 na Tabela D1. O autor confirma que a base da série completa é a mesma linha canônica com `response_text` não nulo. |
| §7.2: "Only the third is a hallucination, and a protocol that pools all three reports a false-positive rate near 97% **where the defensible figure is a fraction of it**." | **C.1.11** adaptada. O parágrafo seguinte declara que não há "measured distribution across the three categories", ou seja, o texto afirma o tamanho de um número que ele diz não ter medido. | "Only the third is a hallucination, and a protocol that pools all three reports a false-positive rate of 96.7% on 17,919 probe observations, of which 66.8% of the 17,328 flagged responses carrying text already show an explicit refusal marker, so the pooled figure counts refusals as hallucinations." As duas proporções são as da Tabela D9 e nada é estimado. |
| §6.4, primeira frase, 47 palavras, e é procedimento, não conclusão: "Since migration 0010 the pipeline writes the whole response to `citations.response_full_text` while continuing to write the windowed string to `response_text`, which makes the comparison run inside the arm: extract over `response_full_text[:200]`, extract over `response_full_text`, hold the cohort, the battery and the matching rule fixed, and read the difference." | **C.1.4**, teto de 45 palavras e abertura que anuncia em vez de concluir. Também é o único ponto do bloco que quebra a C.4.4. | Antepor a conclusão e manter o procedimento intacto: "Inside the arm, on identical observations, reading the whole response instead of the first 200 characters moves the rate by 22.95 to 55.73 points and loses no citation. Since migration 0010 the pipeline writes the whole response to `citations.response_full_text` while continuing to write the windowed string to `response_text`, which is what makes the comparison a within-observation one: extract over `response_full_text[:200]`, extract over `response_full_text`, hold the cohort, the battery and the matching rule fixed, and read the difference." (primeira frase: 26 palavras; a faixa é a da própria Tabela D2) |

---

## 3. Auditoria das declarações do "Anti-tic pass"

O enunciado da tarefa trata uma declaração de limpeza que não se sustenta como achado de severidade alta. Cinco não se sustentam.

### Não se sustentam

1. **Bloco D, item 1, severidade alta.** Declara "Three occurrences removed" e que sobrevive uma única antítese estrutural, em §6.6, justificada como conteúdo. A medição encontra mais duas, ambas na forma graduada que a C.1.1 bane, e uma delas ocupa exatamente a posição que a declaração diz ter limpado, a primeira frase de §6.1. A C.1.1 avisa na primeira e reprova na segunda, de modo que o bloco reprova por uma regra que sua própria passagem final declara zerada.
2. **Bloco D, item 5, severidade alta.** Declara "Every percentage was checked against its table". Dois percentuais de §6.6 não recuperam denominador em nenhuma tabela do bloco (achados D.1.13 acima). A checagem descrita não cobriu o parágrafo de preâmbulo.
3. **Bloco A, bloco final sobre a PARTE D.2, severidade alta.** Declara que três afirmações de ausência foram reescritas, entre elas "Published studies do not declare their extraction window", substituída em §2.8 pela ressalva de que o levantamento não foi feito. A mesma classe de afirmação sobreviveu em §1.1, na forma mais curta e mais exposta: "The last of those four is the one no vendor publishes". A passagem corrigiu a ocorrência da seção que a discute e não a da seção que a usa como argumento de abertura.
4. **Bloco A, item 8, severidade alta.** Declara a remoção de um fecho pseudo-profundo em §2.8, "replaced by the list of the five places in the paper where the contribution is delivered". A substituição é a violação de C.1.5 registrada em 2.1. A correção de uma regra criou a infração de outra e a passagem não releu o resultado.
5. **Bloco A, item 3, severidade baixa.** Cita como texto entregue a frase "Three recent measurements establish how much the conditions move the answer". O texto entregue diz "Four recent measurements establish how far the conditions move the answer", e cita quatro trabalhos, o que torna o texto correto e a declaração desatualizada. A correção declarada aconteceu; a citação dela não foi refeita.

### Lacunas de cobertura, que não são falsidade mas explicam as reprovações

| Bloco | Regras da C.1 que a passagem não roda | Onde isso custou |
|---|---|---|
| A | C.1.4, C.1.6, C.1.11, C.1.12, C.1.14 | Nenhuma reprovação nessas regras. Cobertura suficiente. |
| B | C.1.4 pela metade (avalia a abertura de §12 e o segundo parágrafo de §4.5, nunca a primeira frase de §4.2 e de §4.5); PARTE D.2 não é rodada, só a D.1 dos quatro eixos do percentual | As duas reprovações de C.1.4 e as duas de D.2. |
| C | C.1.2, C.1.4, C.1.8, C.1.11, C.1.12, **C.1.14**, e o aviso de apoio visual da C.2 | As três reprovações do bloco estão em C.1.14 e C.1.4, exatamente as regras não rodadas. |
| D | C.1.2, C.1.4, C.1.8, C.1.12, **C.1.14**, PARTE D.2, e as exigências da C.4 | Quatro das sete reprovações do bloco estão em regras não rodadas. |

### Declarações que a medição confirma

Vale registrar o que se sustenta, porque é a maior parte.

- **C.1.7 em todos os quatro blocos.** Zero travessões e zero meias-riscas em prosa corrida. As ocorrências restantes estão em faixas de página da lista de referências, no título de norma dentro da tabela de referências do bloco D, no marcador de nulo da Tabela B6 e no cabeçalho de trabalho do bloco B, todas posições que a C.1.7 tolera.
- **C.6 em todos os quatro blocos.** Zero acertos nas 40 entradas. As duas ocorrências que o medidor levantou são falsos positivos verificados a mão.
- **C.1.3 em todos os quatro blocos.** Nenhum parágrafo abre por conectivo de enchimento, e a densidade de conectivo gasto no bloco A, o único com uma ocorrência, é 0,07 por 250 palavras contra um limiar de 1,00 com piso de quatro.
- **Bloco C, C.4.4.** Declara que a primeira frase de §5 tem 29 palavras e a de §8 tem 27. A medição confirma 29 e 27, e as dez aberturas de subseção do bloco enunciam achado, não anúncio. É a declaração mais precisa das quatro passagens.
- **Bloco C, diagnóstico de ritmo.** Declara faixa de 3 a 60 palavras por frase e sete blocos de §5.3 com 5, 5, 6, 7, 6, 5 e 5 frases. O medidor lê 3 a 58 e 6, 6, 7, 8, 7, 6 e 6, diferença que vem de contar a entrada em negrito de cada defeito como frase. O padrão declarado, dois pares vizinhos iguais e nenhuma corrida de três, sustenta-se nas duas contagens.
- **Bloco B, C.1.9.** Declara 1.669 caracteres no parágrafo do P6. A medição lê 1.671, e a defesa da manutenção, não separar o resultado da ablação da ressalva de transferência que o qualifica, é boa.
- **Bloco D, item 4.** Declara zero aposições contrastivas e sete ocorrências de `rather than`, a 1,9 por mil palavras. A medição confirma zero aposições e sete ocorrências, contando o título de §7.2 e a especificação da Figura D1.
- **Bloco B, C.2, gerúndio vago.** Declara "contributing to" ausente. A expressão aparece uma vez em §3.7, em "stops contributing to comparisons between figures", onde é verbo pleno com objeto e não gerúndio vago fechando frase. A regra está satisfeita, a afirmação sobre a palavra não. Severidade nula para o texto, registrada só para que a próxima passagem não confie na busca literal.

---

## 4. Avisos da C.2, agregados

Onze avisos nos quatro blocos, o que é pouco para quinze mil palavras. Nenhum deles é dívida; a lista abaixo separa os quatro que valem correção dos sete que valem resposta escrita.

**Valem correção:**

1. **Bloco C, apoio visual.** Duas tabelas para 21.754 caracteres de prosa, 10.877 por item contra um piso de um a cada 5.000. A passagem final do bloco não roda este aviso. §8.4 é o lugar natural: os quatro rompimentos detectados e não declarados, com data, braço, magnitude em pontos e correspondência com commit, são cinco colunas que hoje o parágrafo enumera em prosa.
2. **Bloco A, advérbios em `-ly` concentrados.** Cinco num parágrafo de §2.7, contra um aviso em quatro: `unevenly`, `primarily`, `directly`, `weakly`, `non-monotonically`. Dois saem sem custo: "those effects are primarily model-specific" vira "most of those effects are model-specific", e "position bias in recommendation output is measured directly" vira "position bias in recommendation output is measured". Os outros três carregam informação e ficam.
3. **Bloco A, quantidade sem contagem, duas ocorrências.** §2.2, "A large share of this 2026 literature is single-author preprints without peer review", e §2.5, "Such indices are already proliferating here", apoiado em um único índice citado. A C.2 manda dar o número onde ele é barato, e aqui ele sai da própria lista de referências do bloco. Reescritas: "Of the 2026 works cited in this section, [n] of [N] are single-author preprints without peer review" e "At least one index of this kind is already in circulation: one recent study proposes a Category Ownership Index…".
4. **Blocos B e D, títulos de gaveta em subseções que têm afirmação.** §4.3 "Engine panel with pinned versions" e §4.4 "Generation configuration" carregam achados que o título não diz (a fronteira dupla do braço Gemini, o custo do esforço de raciocínio); §6.3 "Magnitude in the historical series" e §6.4 "The symmetric test" nomeiam a operação em vez do resultado. Nas subseções normativas de §3 o título é o nome do requisito e deve ficar como está.

**Valem resposta escrita, não correção:**

5. Bloco A, apoio visual: duas tabelas para 26.314 caracteres. A passagem final já responde, e a resposta é boa: uma introdução e um trabalho relacionado não têm item empírico a exibir, e as Tabelas A1 e A2 carregam conteúdo de especificação que a prosa teria de enumerar.
6. Bloco B, um parágrafo de 1.671 caracteres. Declarado e defendido.
7. Bloco B, duas aposições contrastivas em 4.360 palavras, 0,46 por mil contra um aviso em 3.
8. Bloco C, um intensificador (`entirely`), contra um aviso em três.
9. Bloco C, três parágrafos seguidos com a mesma contagem de frases. Declarado como diagnóstico e defendido pela estrutura fixa dos sete defeitos.
10. Bloco D, §7.1: o par "It says that the extractor is not manufacturing cohort matches…" seguido de "It says nothing about a model's willingness…" é contraste estrutural distribuído em duas frases. Isolado, fica sob o limiar. Se as duas reprovações de C.1.1 forem corrigidas, este par passa a ser o único resto do hábito no bloco e merece leitura.
11. Bloco A, uma frase acima de 60 palavras; bloco B, duas. Diagnóstico da C.3, que a régua manda reportar e nunca transformar em meta.

---

## 5. Exigências positivas da C.4

Esta é a parte em que os quatro blocos se separam de verdade.

### C.4.1 Raciocínio encadeado

Dentro de cada bloco o encadeamento é bom: medi as 152 transições de parágrafo e não achei parágrafo que apenas reescreva o anterior. O defeito está entre blocos, é grande, e nenhuma passagem anti-tique individual pode vê-lo, porque cada uma roda sobre o seu próprio arquivo. Três passagens estão escritas quatro, três e três vezes:

**(a) A conversão da medida, em quatro lugares.** A §2.7: "Truncation of the response by the collection pipeline converts a whole-response measurement into a head-of-response measurement, at a cut point that varies between providers because it is set by adapter code written for cost or log volume and not by measurement design." B §3.1 P1: "It is an incidental consequence of how a provider adapter was written, for reasons of cost or log volume, and it therefore varies between providers, which is where the comparison lives." B Tabela B1, linha P1: "The instrument silently measures head-of-response citation and reports it as whole-response citation, at a cut-off that differs between providers." D §6.2: "truncation on the collection path converts whole-response measurement into head-of-response measurement, at a cut-off that differs between providers because adapter code sets it, which places the variation exactly where cross-engine comparison lives."

**(b) A história da detecção, em três lugares quase literais.** B §12.3: "No test detected it, because every test asserted on the field and the field was populated in both cases; no validator detected it, because both values are well-formed strings of plausible length. Detection came from a distributional check." C §5.3: "Tests asserted on the column, and the column was populated in both cases; validators checked that the string was well formed, and both were". D §6.2: "No test caught it, because every test asserted that the field was populated and the field was populated in both cases. No validator caught it, because both values are well-formed strings of plausible length. Detection came from a distributional check."

**(c) As notas do VIM, em três lugares.** A §1.2, B §3 (primeiro parágrafo) e D §6.1 (terceiro parágrafo) reescrevem as mesmas duas notas, e dois deles fecham com a mesma expressão, "arithmetically correct and substantively misleading".

A C.4.1 manda cortar, não reescrever. Alocação proposta, uma por passagem: **(a)** fica em §3.1 P1, que é normativo e é onde o parâmetro se define; A §2.7 e D §6.2 passam a "the conversion P1 describes (§3.1)". **(b)** fica em §5.3, que é o registro de campo e é onde a história pertence; B §12.3 e D §6.2 remetem por número de seção. **(c)** fica em §1.2, que estabelece o mensurando; §3 e §6.1 citam as cláusulas e não reenunciam as notas. A economia é de cerca de 600 palavras de prosa, e o ganho maior é que a reincidência some: hoje o leitor encontra a mesma frase quatro vezes com quatro redações, que é o padrão que a A.10 linha 5 chama de estrutura pouco clara.

Um caso dentro do bloco D: §6.7, parágrafo "**Declaration.**", enuncia o que o fecho de §6.5 já concluiu ("A published ranking of engines by citation rate is therefore a statement about the window"). Corte o parágrafo e deixe o requisito como uma linha que aponte para §6.5.

### C.4.2 Variação real de tamanho de período

Medida e satisfeita nos quatro. Desvio padrão de 11,7 a 14,1 palavras sobre médias de 24,2 a 25,6, com mínimos de 1 a 3 palavras e máximos de 55 a 70. A variação é produzida por sentido, não por cota: as frases curtas caem nas viradas ("The other is whole-response citation.", "It splits.", "One hole dominates.", "Detection came from a distributional check.", "Run that check on day one."). O bloco C é o mais uniforme dos quatro, com desvio 11,7, e é também o único que declara e defende a própria simetria. A régua proíbe transformar isso em meta e nada há a fazer.

### C.4.3 Recomendação sempre justificada

O bloco B é o padrão da casa nesta exigência: a Tabela B1 dá modo de falha para cada um dos seis parâmetros, a Tabela B8 dá coluna de evidência para cada uma das dez decisões, e §12.3 dá o incidente que produziu cada um dos seis erros. O bloco C justifica cada lição pelo defeito que a gerou, com linha de arquivo. O bloco A faz uma recomendação, o pareamento com o Dice Roll Method em §2.2, e a justifica pela tabela de disjunção.

O bloco D tem uma falha pequena e fácil: §6.7 lista quatro requisitos e promete que "each carries the cost of skipping it". Três carregam (uniformidade carrega os quatro meses de abertura assimétrica, retenção carrega o braço Groq irrecuperável, declaração carrega a troca de líder da Tabela D4). O quarto, "**Sensitivity reporting.** The headline figure published under both windows, per engine, in the form of Table D2", dá a forma e não o custo. Uma frase fecha: "Publishing one window only leaves a reader unable to tell a 22.95-point arm from a 55.73-point arm, which is the spread Table D2 measures."

### C.4.4 A conclusão nas primeiras 120 palavras

Medida por subseção, contando as palavras até a frase que enuncia a conclusão da subseção.

- **C, o melhor dos quatro.** Dez de dez aberturas enunciam achado na primeira frase. §5 abre em "Every defect described below passed a green test suite"; §8.2 em "The series spans 139 calendar days and holds data on 52 of them, a coverage of 37.4%".
- **B, forte no nível de seção e falho em duas subseções.** §3, §4 e §12 abrem na conclusão. §4.2 e §4.5 abrem num inventário de 48 e 70 palavras, o que é a reprovação de C.1.4 já registrada em 2.2; as reescritas propostas lá resolvem também esta exigência.
- **D, uma quebra.** §6.4 abre com 94 palavras de procedimento antes do resultado. A reescrita proposta em 2.4 antepõe a conclusão e mantém o procedimento inteiro.
- **A, quatro quebras, todas no §2.** A afirmação própria de cada subseção chega tarde: §2.1 na palavra 190, §2.3 na 145, §2.7 na 150, §2.4 na 124, quatro palavras acima do teto. A correção é a mesma nas quatro e não custa uma palavra nova: a frase que hoje fecha o segundo parágrafo passa para a cabeça do primeiro. Exemplo em §2.1: "BRGEO-1 works one level below the optimisation literature: it specifies the conditions under which a citation rate is a comparable quantity. The generative engine optimization literature asks how to raise the probability that a source is selected, and each study fixes an evaluation harness adequate to its own comparison." Mesmas palavras, ordem invertida.

### C.4.5 Uma fonte e data por parágrafo

Satisfeita nos quatro. A chave de citação e a data da série acompanham o primeiro número de praticamente todo parágrafo, e os seguintes herdam. As duas exceções são os percentuais de §6.6 já registrados em 2.4.

### C.4.6 O fecho entrega

Medida: fecham parágrafo sem número 39% em A, 61% em B, 56% em C, 44% em D. O número por si não decide nada, porque um fecho pode entregar consequência sem cifra. Os defeitos são de seção, não de parágrafo:

- A §2.2 fecha em "Generalizability theory is also the vocabulary §9 uses for its variance decomposition", uma remissão onde cabe uma consequência.
- A §2.6 fecha num inventário de origens de vocabulário normativo.
- A §2.8 fecha na passagem de autonarração, que entrega sumário e não decisão (reprovação A.1).
- B §12.3 e C §8.4 são o modelo: "the requirement is that the choice, the date it changed, and its effect on the ledger are published rather than inferred" e "a pooled rate for that arm over the whole series, reported without the confrontation, would be an average across regimes nobody can date".
- D §6.6 fecha numa ressalva sobre um teste fraco, que é o fecho certo para aquela subseção e não deve ser mexido.

---

## 6. Voz

Os quatro registros diferem de forma mensurável, e três das quatro diferenças são legítimas.

| Marcador | A | B | C | D |
|---|---:|---:|---:|---:|
| Máxima generalizante fechando parágrafo | 0 | 3 | 3 | 0 |
| Fechos de parágrafo sem número | 39% | 61% | 56% | 44% |
| `rather than` por 1.000 palavras | 0,5 | 6,7 | 3,8 | 1,4 |
| Percentuais na prosa | 17 | 4 | 8 | 41 |
| Frases abrindo por adjunto | 14,7% | 8,6% | 14,9% | 13,5% |

**A** é voz de levantamento. Cadeias longas de citação, período ramificado, registro elevado, e uma abertura de lede jornalístico em §1.1 ("A consumer who once read ten ranked links now reads one answer") que é o único momento em que o bloco sobe o tom.

**B** é voz normativa com aresta de advocacia. Fecha três parágrafos em máxima ("A protocol paper that asks others to declare their matching rule has to declare where its own leaks"; "A claim form whose only possible answers are favourable is a marketing artefact"), usa `rather than` como dobradiça padrão a 6,7 por mil palavras, e é o bloco com menos números por fecho. A aresta é o problema, não o registro: num artigo escrito pelo custodiante da especificação avaliada, a A.10 linha 6 já trata autointeresse como risco de triagem, e o tom de slogan é exatamente o que um revisor lê como promocional.

**C** é voz forense. Registro de relatório de incidente, períodos curtos, cada afirmação ancorada em linha de arquivo, e a mesma tentação de máxima que B ("An adopter who shares credentials across instruments buys correlated outages"; "An instrument that leaks into a public number stops being a control").

**D** é voz de resultado, a mais seca das quatro e a mais densa em número: 41 percentuais na prosa contra 4 em B. É por isso que as duas antíteses sobreviventes destoam tanto ali: são os únicos dois lugares do bloco em que a frase toma uma forma retórica emprestada em vez de relatar.

**Ajuste mínimo, três movimentos, sem uniformizar.**

1. **Teto de uma máxima por seção, e no fecho da seção, não no fecho de um parágrafo interno.** Em B isso preserva "A protocol paper that asks others to declare their matching rule has to declare where its own leaks" como fecho de §4.5, que é onde ela é ganha, e converte a de §12.1 na sua própria evidência: "The Level 2 line is the one a claimant would omit, and it is the line that tells a reader the 68,624 observations collected before retention cannot be re-extracted."
2. **Onde o bloco já tem o número ao lado da máxima, junte os dois.** Em C, "An adopter who shares credentials across instruments buys correlated outages and loses cost attribution" fica a duas frases de "49 runs and 3 succeeded". Unir: "Three measurements presented as independent stopped at the same time for the same reason, and the ledger shows it as 49 runs of which 3 succeeded: an adopter who shares credentials across instruments buys correlated outages and loses cost attribution." A cadência aforística sai, o conteúdo fica, e a voz forense de C se reafirma em vez de se diluir.
3. **Em D, trocar as duas antíteses pelas formas que B e C já usam para os mesmos fatos** (reprovações D nas linhas 1 e 2 da tabela em 2.4). É o movimento que mais aproxima D dos outros três, porque as duas frases são os únicos pontos do bloco em que a voz sai do relato.

O que não deve ser tocado: a densidade numérica de D, a ancoragem em linha de arquivo de C, as cadeias de citação de A e o `MUST`/`SHOULD` de B. A diferença entre uma seção normativa e um relato de campo é a razão de os dois existirem separados.

---

## 7. O que eu mudaria primeiro, em ordem de impacto

1. **As duas antíteses do bloco D** (§6.1 primeira frase, §6.2). Duas frases, reparo já escrito em B e em C com os mesmos fatos, e são as únicas reprovações de C.1.1 em quinze mil palavras. Corrigi-las também põe de pé a declaração da passagem anti-tique de D.
2. **A tripla e a quádrupla repetição entre blocos** (C.4.1, item (a), (b) e (c) da seção 5). Nenhuma passagem individual enxerga, o revisor lê o manuscrito montado, e são cerca de 600 palavras de prosa que saem sem perda de informação.
3. **As duas afirmações do bloco A que a própria passagem diz ter removido**: o fecho de autonarração de §2.8 e "the one no vendor publishes" de §1.1. Uma afirmação de ausência que o mesmo bloco recusa duas seções adiante é o tipo de inconsistência que um revisor acha primeiro, e a A.10 linha 8 já trata o rastro não declarado como categoria de ética.
4. **As treze referências a "v1.0" nos blocos C e D** (C.1.14). Substituição mecânica pelo registro datado. Enquanto ficarem, o artigo lê como revisão de um documento que o leitor não pode obter.
5. **A nota de edição em C §8.2** ("The manuscript should settle on one before submission") e, junto com ela, a decisão entre 52 e 53 dias que ela adia. Uma frase para tirar, uma decisão para tomar, e a decisão propaga para os 19 dias parciais "among the 53".
6. **Os dois percentuais sem denominador em D §6.6.** Um resolve com números que já estão nas Tabelas D1 e D7 do mesmo bloco; o outro precisa do n por célula, que sai de `stats/data/`.
7. **As três primeiras frases acima de 45 palavras** (B §4.2, B §4.5, D §6.4). Uma edição cada, e as três melhoram a C.4.4 no mesmo movimento.
8. **As quatro subseções de A §2 em que a afirmação chega depois da palavra 120.** A frase já existe; basta subi-la para a cabeça do primeiro parágrafo.
9. **As duas negativas universais de B** (§3.1 P6, §3.7), que são as únicas afirmações de ausência não medidas num bloco que, no resto, é o mais disciplinado dos quatro em justificar recomendação.
10. **Os quatro avisos que valem correção** (seção 4, itens 1 a 4): apoio visual em C, cinco advérbios em `-ly` em A §2.7, duas quantidades sem contagem em A, e os quatro títulos de gaveta de B §4.3, B §4.4, D §6.3 e D §6.4.

---

## 8. Fora da régua, para decisão do editor

Nada aqui é regra da PARTE C. São seis pontos que incomodaram durante a leitura e que a régua não cobre.

1. **Colisão do número 0,086 entre A e D.** O highlight e o abstract do bloco A dizem "three engines running the full battery agree at a Fleiss kappa of 0.086" sobre 68.624 observações e 53 dias, com remissão a §9. O bloco D, §6.7, diz "analysing the outcome as stored rather than harmonised understates agreement by 0.086 on the five-arm panel of 4,231 complete cells", onde 0,086 é uma diferença e não um nível. As duas leituras podem coexistir por coincidência de valor, e §9 está fora do escopo desta auditoria, mas um revisor que encontre o mesmo número descrevendo duas quantidades vai perguntar. Não alterei nenhum dos dois.

2. **Remissão cruzada que não resolve, em B §4.5.** "The instantiation also supplies the demonstration for a claim the specification makes in the abstract. §4.6 argues that collision between a brand and an ordinary word is the failure mode most likely to inflate a naive count." O abstract do bloco A não faz essa afirmação (fala de janela, kappa, efeito de desenho e índice; colisão lexical não aparece). E §4.6, para onde a frase aponta, remete de volta a §4.5 para a evidência, de modo que a afirmação nunca é enunciada em lugar nenhum. Duas remissões apontando uma para a outra, e a terceira apontando para um texto que não contém o que ela atribui.

3. **`rather than` como o destino de todas as antíteses removidas.** Medido: 0,5 por mil palavras em A, 1,4 em D, 3,8 em C, 6,7 em B (29 ocorrências na prosa de B). A PARTE C não lista a construção, e as quatro passagens anti-tique deste manuscrito a tratam como vizinha tolerada. O que o conjunto mostra é que ela virou o lugar onde a estrutura banida pela C.1.1 foi parar: "normative rather than advisory", "calibration rather than specification", "declared rather than smoothed", "generated rather than curated", "documented rather than hypothetical". São dez usos em B em que os dois termos são o mesmo objeto visto duas vezes, e nenhum deles acrescenta informação sobre o primeiro termo, que é exatamente o defeito que a C.1.1 descreve. Proposta para a próxima revisão da PARTE C: aviso acima de 4 por mil palavras, sem reprovação, porque o uso legítimo é comum. Proposta para este manuscrito: converter os dez usos tautológicos de B.

4. **A divergência 52 contra 53 dias, que C §8.2 declara e não resolve.** A auditoria de estilo só pode registrar que a frase que a resolve foi escrita como nota ao editor. O número circula por §4.7, pelo formulário de conformidade de §12.1, pela legenda da Tabela C2 e pelos 19 dias parciais.

5. **Andaime de rascunho ainda no texto.** O bloco B abre com um cabeçalho de trabalho ("# Block B — §3 The BRGEO-1 specification · §4 Reference instantiation · §12 Adopting the protocol") seguido de um parágrafo de procedência ("Draft for the journal-length manuscript. Numbers are drawn from `../tables/TABLES.md`…"), e os blocos C e D abrem direto em "## 5." e "## 6." sem cabeçalho. Some na montagem, mas hoje esse cabeçalho carrega o único travessão do bloco B fora da lista de referências.

6. **Cobertura.** Esta auditoria leu §1 a §8 e §12. Toda remissão proposta acima assume que §9, §10, §11, §13, §14, §15 e §16 existem com a numeração que os quatro blocos usam. A alocação sugerida em C.4.1 deve ser conferida contra os blocos que não vi antes de ser aplicada.

---

## Anexo. Como reproduzir a medição

```
cd journal-v2/reviews
python style_check.py          # relatório legível
python style_check.py --json   # os mesmos números em JSON
```

O script lê os quatro arquivos de `sections/`, separa prosa de aparato pelas regras descritas no cabeçalho desta revisão e mede: tamanho de parágrafo e de frase, densidade de conectivo gasto, aposição contrastiva por mil palavras, antítese nas formas fechadas e na forma graduada, travessão em prosa, adjetivos vazios, intensificadores, advérbios em `-ly` por parágrafo, perguntas retóricas, introdutores de fonte, apoio visual, aberturas de parágrafo repetidas, as 40 entradas da C.6, a primeira frase de cada seção contra o teto de 45 palavras, e a lista de percentuais com contexto para julgamento manual do denominador. Os limiares estão escritos ao lado de cada medida, no formato "medido contra limiar", e nenhum deles é convertido em meta.

Uma correção aplicada durante esta auditoria: a contagem de itens visuais estava duplicando tabelas, o que subestimava o aviso de apoio visual pela metade. Os números da seção 1 já são os corrigidos.
