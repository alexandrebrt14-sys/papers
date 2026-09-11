# V6 — Aplicação das revisões V4 e V5 aos blocos E e F

**Data:** 2026-09-11 · **Arquivos editados:** `sections/E-findings-index-plan.md`, `sections/F-governance-threats-discussion.md`. **Arquivos novos:** `stats/s6_index.py` e sete CSV em `stats/data/s6_*.csv`. Nenhum outro arquivo foi alterado. Nenhum comando git alterou estado. O banco foi aberto apenas com `mode=ro`.

---

## 1. A tarefa extra: o índice recalculado

O achado E-1 estava certo. Toda a §10 rodava sobre o corte de 2026-08-31, com 66.399 observações canônicas, sob legendas que declaravam a série até 2026-09-08 com 68.624, e o script que produziu esses números não aparecia no Apêndice E.

### 1.1 O que foi escrito

`stats/s6_index.py`, modelado em `s4_concentration.py` e `s5_window_validity.py`: conexão `mode=ro` via `tables/_common.py`, mesmo extrator de entidades das tabelas do manuscrito, mesma coorte v2 com âncoras e chamarizes, janela uniforme de 200 caracteres sobre `response_text[:200]`, estrato canônico `COALESCE(is_probe,0)=0`. Calcula por vertical os três componentes (cobertura, proeminência, amplitude), o índice pela média geométrica, as quatro agregações, a correlação de posto do índice contra a cobertura simples nos quatro recortes que a tabela publica, a matriz 4 × 4 entre agregações, a decomposição de variância do log do índice e o deslocamento de posto. Escreve `s6_components.csv`, `s6_spearman_subsets.csv`, `s6_aggregation_matrix.csv`, `s6_variance_decomposition.csv`, `s6_rank_displacement.csv`, `s6_panel.csv` e `s6_run.csv`. Roda em 23 segundos.

Três decisões de método, todas declaradas no cabeçalho do script:

1. **Painel.** A especificação não fixa a regra de painel, e a implementação de referência a resolveu duas vezes em código. O script calcula sob as duas: `series`, os seis braços que contribuíram para a série, que mantém o denominador nas 68.624 da §9 e não usa parâmetro não declarado; e `recency`, a regra de 14 dias do commit `51159fd`, que neste corte descarta o Groq e admite o Grok. A §10 publica a primeira e reporta a segunda como sensibilidade. A opção `--min-obs` reproduz o limiar antigo.
2. **Numerador e denominador no mesmo painel.** A implementação de referência divide um numerador somado sobre todos os braços por um denominador somado só sobre o painel. O script não reproduz essa assimetria; restringe os dois. A divergência está registrada na linha nova da Tabela F14.
3. **Cheque de identidade.** O script repete a verificação da `NUMBERS.md` V2: nas linhas cujo texto armazenado já cabe na janela, a reextração tem de reproduzir o `cited_v2` gravado. Resultado: **0 divergências em 61.189 linhas**. Sai com código diferente de zero se falhar.

### 1.2 O recálculo, contra o publicado

Corte 2026-04-23 a 2026-09-08, 68.624 observações canônicas, painel de seis braços, 66 entidades citadas ao menos uma vez (o mesmo 66 de antes; as 61 nunca citadas continuam 61).

| Quantidade | Publicado (corte 2026-08-31) | Recalculado (corte declarado) |
|---|---:|---:|
| rho, índice contra cobertura, todas | 0,982 (n = 66) | **0,982** (n = 66) |
| rho, sem o líder de cada vertical | 0,978 (n = 62) | **0,979** (n = 62) |
| rho, cobertura entre 0,1% e 5% | 0,945 (n = 42) | **0,949** (n = 42) |
| rho, cobertura abaixo de 1% | 0,960 (n = 44) | **0,956** (n = 42) |
| Var(log) cobertura / contribuição | 4,490 / 74,7% | **4,360 / 72,4%** |
| Var(log) amplitude / contribuição | 0,306 / 16,9% | **0,369 / 18,8%** |
| Var(log) proeminência / contribuição | 0,198 / 8,4% | **0,188 / 8,7%** |
| Geométrica × aritmética | 0,816 | **0,870** |
| Geométrica × harmônica | 0,983 | **0,983** |
| Geométrica × ponderada | 0,787 | **0,836** |
| Aritmética × harmônica | 0,734 | **0,788** |
| Aritmética × ponderada | 0,984 | **0,985** |
| Harmônica × ponderada (o mínimo) | 0,706 | **0,752** |
| Contra cobertura: geo / arit / harm / pond | 0,982 / 0,728 / 1,000 / 0,700 | **0,982 / 0,784 / 0,9997 / 0,748** |
| Deslocamento: mediana / p90 / máximo | 2 / 6 / 10 | **2 / 6 / 14** |
| Entidades que mantêm posto exato | 7 de 66 | **9 de 66** |

**Mudanças materiais, todas declaradas no texto com o valor anterior ao lado:** as três contribuições de variância; o mínimo da matriz, que sobe de 0,706 para 0,752; o máximo de deslocamento, que sobe de 10 para 14; e a afirmação de que a média harmônica reproduz a ordenação da cobertura **exatamente**, que deixou de valer. No corte declarado a correlação é 0,9997, e dez das 66 entidades trocam de lugar com a vizinha imediata, nenhuma andando mais que um posto. A §10.3 passou a dizer isso e a registrar que o corte anterior arredondava para 1,000.

Sensibilidade ao painel, publicada na §10.2 e na §10.3: sob a regra de recência, as contribuições leem 73,6% / 17,5% / 9,0%, o mínimo da matriz é 0,757, e o deslocamento tem a mesma mediana e o mesmo p90, com máximo 12 e 13 entidades mantendo posto. A conclusão da seção não depende da regra de painel.

### 1.3 O que o recálculo descobriu sobre a tabela antiga

Com `--until 2026-08-31 --min-obs 500`, isto é, no corte e sob a regra de painel vigentes quando os números foram produzidos, as três contribuições voltam em **74,7% / 16,9% / 8,4%, idênticas às publicadas**, e a matriz volta a menos de 0,007 de cada célula publicada. Mas dois valores publicados não saem dessa configuração: `Var(log)` da cobertura em 4,490 e as sete entidades que mantêm posto exato só se reproduzem no painel de seis braços sobre o mesmo corte, que devolve contribuições de 72,9% / 19,1% / 8,1%.

A Tabela 10 do `MANUSCRIPT.md`, portanto, **não é uma única execução**: mistura duas. Isso está registrado na §10.2 como segunda razão para ler o recálculo em vez dela. A tabela publicada não é reproduzível como um objeto coerente, e o recálculo é.

### 1.4 Onde o script entrou

Duas linhas novas na Tabela F14 do Apêndice E: `python s6_index.py` para a §10, e `python scripts/brgeo1_index.py --vertical all --compare` para a implementação de referência, com a nota de que ela escolhe o painel por recência e calcula a cobertura sobre um numerador não restrito ao painel. A primeira frase do Apêndice E deixou de ser uma afirmação falsa: a §10 agora tem comando de regeneração.

---

## 2. Os seis BLOQUEIA

| # | O que ficou no texto |
|---|---|
| **E-1** | Resolvido pelo recálculo, não pela legenda. As duas legendas declaram o corte, o número de observações, o painel, o script e o CSV de origem, e nomeiam os valores superados. |
| **E-2** | A §10.3 passou ao passado e ao fato: o limiar não declarado vigorou até 2026-08-31, o commit `51159fd` o substituiu por regra de recência de 14 dias ancorada no último timestamp do dado, toda figura de índice publicada antes de 2026-09-11 é superada pelo recálculo, e **o código não carrega mais o defeito**. Mesmo tratamento que o bloco B §12.3 já dava. |
| **F-1** | 64,10% → **65,10% sobre 384 observações**, nos dois lugares (linha 8 da Tabela F1 e §14). Confere com `NUMBERS.md` T13, que imprime 65,1042% [60,21; 69,70] e 250/384. O §15 do mesmo bloco já dizia 65,10%; a contradição interna acabou. |
| **F-2** | 68.624 → **66.399** nos dois lugares (Data availability e Apêndice E). Conferido no banco: 66.399 canônicas até 2026-08-31 e 2.225 depois, somando 68.624. |
| **F-3** | Linha 5 da Tabela F1 no passado, com a janela nomeada: o limiar valeu até 2026-08-31, as 96 observações do braço vivo são do corte daquela data (na série declarada são 288), o braço aposentado saiu em 2026-08-16 com 3.552, e o commit `51159fd` trocou a contagem pela regra de recência. A coluna "o que fica em aberto" aponta para o recálculo. |
| **F-4** | **Não aplicado como o manuscrito instruía, porque o manuscrito estava errado.** Testei `build/assemble.py`: `_K = r"[A-Z][A-Za-z0-9&.\-]{2,}[0-9][A-Za-z0-9&.\-]*"` casa `[JCGM200]`, `[JCGM100]`, `[ISO5725-2]` e `[VIM2012]`, e `CHAVE` aceita vírgula e ponto e vírgula, de modo que `[Jacobs2021; Borsboom2004]` casa. O `ASSEMBLY-REPORT.md` confirma pelo outro lado: nenhuma chave citada sem entrada, nenhuma entrada sem citação. Os pontos 2 e 3 da seção "Notes for the integrator" foram substituídos pelo fato testado e datado, e a seção declara que as sete edições que instruía nos blocos A e B eram desnecessárias. O ponto 1, sobre o `ALIAS`, estava correto e ficou. |

---

## 3. Os quinze CORRIGIR

Todos aplicados, cada um conferido contra a fonte antes de colar. Três precisaram de correção sobre a correção do revisor, marcadas com ▲.

**Bloco E.** E-3: legenda da Tabela E8, "fifteen rows" → "the twelve rows that were run, the three Grok rows carrying no p-value" (confirmado em `s2_trend.csv`: 15 linhas, 12 com p, 3 `NOT RUN`). E-4: "declared in §3" → "declared in §8.3" (o bloco C declara a janela confirmatória na §8.3; `grep confirmatory` no bloco B não devolve nada). E-5: 52 dias ganham a regra, "under the local-date rule of §8.2 ... or on 53 under the UTC rule of Appendix D" (banco: 53 UTC, 52 local). E-6: o deff de 63,3 passa a ser da célula motor-por-consulta com 1.056 clusters, e os deffs por braço, de 27,8 a 71,6, entram na mesma frase; a legenda da Tabela E1 declara as duas unidades de clusterização. E-7: os três coeficientes de preâmbulo separados por recorte, coorte agrupada (−0,154 / +0,800 / +0,300) e conjunto restrito (+0,667 / +0,900 / +0,900), conferidos nas linhas 192 e 204 de `S5-window-validity.md`. E-8: legenda da Tabela E11 nomeia a coorte de 2.225 observações de três dias da Tabela S5.12 e declara que a janela confirmatória terá mais poder. E-9: Huang2026 sai da literatura cross-language e entra como resultado sobre procedência do modelo, com os números de `R1-literature.md` N5 (1.909 consultas só em inglês, seis modelos, 30 marcas, 88,9% contra 58,3%, diferença de 30,6 pontos). E-10: a frase sobre painel como parâmetro declarado saiu; a §10.1 agora diz que a especificação não fixa o painel e que a implementação o resolveu duas vezes em código.

**Bloco F.** F-5: 13 → **17** CSV do `s2_temporal.py` e 18 → **19** do `s5_window_validity.py` (contados no script e conferidos em `stats/data/`). F-6: o estrato de fundação em 2010 ou depois deixa de ser apresentado como sonda da defasagem de pré-treino e passa a declarar que nesta coorte não alcança, com o ano máximo de 1895–2019 e o corte posterior de todos os modelos fixados. F-7: "Tables 11 to 13" → **"Tables F11 to F13"**, porque `ROTULO_TAB` só renumera rótulos da forma `Table F11` e a forma antiga sobrevive literal ao manuscrito montado, onde 11, 12 e 13 são C1, C2 e D1. F-8: "the same cohort and the same battery" corrigido, com os denominadores 9.455 e 4.737 e a declaração explícita de que os dois braços não respondem a mesma bateria. F-9: "Six arms produced rows daily..." saiu inteira, junto com o inventário de controles que pertence ao C §5.3 (ver §5 abaixo); a frase falsa desapareceu com o corte de redundância, o que é mais limpo que reatribuí-la. F-10: 1,86% sobre 15.355 e 33,3% sobre 768 deixam de ser "as mesmas respostas"; o texto agora dá os três números na mesma frase, incluindo os **2,60%** que a mesma janela produz nas 768. F-11: nos quatro lugares, deploy e dado separados — a retenção foi implantada em 2026-08-31, a primeira linha retida é de 2026-09-06, e as 2.225 cobrem 2026-09-06 a 2026-09-08 (banco: 2026-08-31 tem 864 linhas canônicas e nenhuma com texto completo).

▲ **Três ajustes sobre o revisor.**

1. **E-11.** A V4 ofereceu duas saídas: reapontar para T7c ou confirmar `rates.by_category_five_arm` depois da reexecução do S1. A segunda não existe: `stats/s1_results.json` não está no disco. Reapontei para `tables/NUMBERS.md` T7c, e conferi a subtração célula a célula (mercado 3.183 − 1.074 = 2.109 sobre 12.709 − 2.573 = 10.136 → 20,81%; comparativo 2.029/10.158 → 19,97%; descoberta 1.662/10.160 → 16,36%; experiencia 313/10.146 → 3,08%).
2. **F-9 (estilo V5).** A V5 dizia que o denominador dos 9,1% do Grok podia ser 1.118 ou o subconjunto com texto retido, e que só o autor poderia dizer. É **768**: `s5_response_censoring.csv` dá `Grok, n = 768, ends_without_terminal_punctuation = 70, 9,114583%`. Escrito assim nos dois lugares.
3. **F-12.** Aplicada a correção da V4 (o custo veio do padrão de raciocínio do braço novo, e a mudança declarada de `reasoning_effort` foi o remédio), confirmada em `R3-fieldlog.md` I13 e T40. A V4 observa que o bloco B, Tabela B4, carrega a mesma imprecisão; **não corrigi o bloco B**, que está fora do escopo. Fica registrado em §7.

---

## 4. Os nove CONFERIR

E-12: nota na legenda da Tabela E2 separando as duas bases (62 na grade reduzida de 42.487 células, 66 sobre as 68.624 observações), conferido em `S3-agreement.md` §7 e na Tabela S4.1. E-13: nota na legenda da Tabela E1 declarando a omissão do Grok com a razão (`NOT RUN (5 days)`). E-14: "the median displacement is 3.5 ranks" → "the mean of the twelve weekly median displacements is 3.5 ranks against a median of 3"; as doze medianas semanais de `s2_rank_tau.csv` são 2, 3, 3, 3, 3, 2, 3, 6, 5, 3, 5, 4, cuja média é 3,5 e mediana 3,0. **A fonte `S2-temporal.md` linha 265 continua rotulando errado e está fora do escopo.** E-15: os dois estimadores separados, com o q de 0,157 da família Hamed-Rao dito explicitamente e a observação de que nenhum braço cruza 0,05 sob ela.

F-13: dois invariantes pelos validadores do módulo e o terceiro por `tests/test_config_v2.py`, conferido em `src/config_v2._validate_query_battery` (assere 192, 96/96 de língua, 96/96 de tipo, 48 por vertical, e nada sobre "Brazil") e em `tests/test_config_v2.py:124-129`. F-14: as três alíneas tratadas — o índice ganhou linha na Tabela F14 (a); a linha do `s1_multilevel.py` declara que nenhuma tabela do paper usa a saída (b); as linhas de figura passaram a nomear D1 e E1 com a numeração montada, e o terceiro PNG é declarado como produzido sem legenda numerada, batendo com "Figures numbered: 2" do `ASSEMBLY-REPORT.md` (c). F-15: a passagem anti-tique diz o que a contagem mostra — 21 travessões longos no arquivo, 18 em células da Tabela do Apêndice D e 3 dentro de títulos de norma na lista de referências, não em faixas de página, com a atribuição anterior nomeada como errada.

---

## 5. Estilo, redundância e os dois marcadores

**As vinte reprovações de estilo, aplicadas.** Rótulo de versão interna: as três saíram (E §11 "the v1.0 manuscript", F §15 "the earlier version of this work", linha 16 da Tabela F1 "the published v1.0 shares"), preservando data, número e sentido em cada caso. Porcentagens sem denominador: as cinco ganharam base (E §9.5 com 7.679/7.676/3.873/3.868 de T7b; E §9.7 com as 158 observações da primeira semana do Grok de `s2_weekly_engine_rank.csv`; F §14 com as 768 do Grok; F §16 com as 768 do Gemini; F §15 com as 1.367 da linha 19). Afirmações sobre "o mercado" e "o campo": as três saíram (E §10.3 "the market practice", F §16 "the field currently publishes", F §15 "the one most often skipped"), mais a atribuição vaga de E §10.1 e a de F §15 "what the market reads as". Aberturas que anunciam o documento: cinco tratadas (F §13 com dois anúncios na mesma frase, F §15 com duas frases de roteiro, E §9.5 e E §9.7 acima do teto de 45 palavras). Autonarração: as duas saíram. Título de gaveta de E §9.1 substituído por afirmação. Máximas de F reduzidas a uma por seção, com a de §14 saindo porque o bloco A já a diz e a de §13 unida à sua evidência de licenciamento.

**A repetição entre blocos, cortada e não reescrita.** Os sete itens da seção 6 da V5, com os donos já fixados na aplicação anterior:

| Passagem | Dono | O que foi cortado |
|---|---|---|
| Decomposição de variância | E §9.2 | As duas primeiras frases de F §15 ¶4, que viraram uma remissão |
| Efeito de desenho por prompt | E §9.1 + Tabela E1 | As duas primeiras frases de F §14 ¶2 |
| Notas do VIM e o aforismo da convenção | A §1.2 | O fecho aforístico de F §14 ¶6, que passa a apontar para §1.2 |
| História da detecção | C §5.3 | O inventário de controles de F §15 ¶3, hoje a única cópia do de C §5.3. Resolve F-9 no mesmo movimento |
| Calendário | C §8.2 e F Apêndice D | As duas primeiras frases de F §14 ¶3 |
| Tetos de concordância | E §9.2 | As duas primeiras frases de F §14 ¶5 |
| Piso de chamarizes | D §7.1 | A subseção E §9.7 inteira, reduzida a uma frase no fim de §9.6, e a construção reenunciada em F §15 ¶6 |

**As sete declarações de limpeza.** As duas seções "Anti-tic pass" foram reescritas do zero para descrever o arquivo entregue, com todo número saindo de `reviews/style_check.py` rodado sobre o arquivo entregue em 2026-09-11 e nenhum estimado. As sete afirmações que não se sustentavam estão nomeadas como corrigidas dentro das próprias passagens: o "None" de C.1.14 nos dois blocos, a checagem de C.1.13 que não cobria duas frases em E e quatro em F, o teto de 45 palavras que E não rodava, a descrição errada do fecho de §9.8, a afirmação de que cada seção de F abre pela conclusão, e a contagem do 39,33% como quantidade nova na conclusão-espelho, que o resumo do bloco A já carrega escrita 39,3%. O escopo de prosa também passou a ser declarado: F declarava 6.362 palavras sobre um escopo desenhado à mão, e agora declara as 5.483 que o medidor lê sobre o escopo que o medidor define.

**O marcador em português.** `stats/S1-multilevel.md` **não existe**, e `stats/s1_results.json` também não — o arquivo estava no disco às 13h33 de 2026-09-11 e sumiu na reescrita de `s1_multilevel.py` às 13h42. O marcador `[INCLUIR: modelo multinível de S1]` foi **removido**, e a passagem funciona com a decomposição de variância que já estava no texto: uma frase diz o que o modelo multinível acrescentaria, diz que não foi ajustado, e devolve o achado para a Tabela E2 e o painel do S3, que o sustentam sem ele. **Registro exigido pelo enunciado: o modelo multinível não entrou.** A legenda da Tabela E6, que apontava para a mesma chave morta, foi reapontada.

**A citação sem suporte.** Huang2026 saiu da frase de literatura cross-language, que fica só com Zatuchin2026c, e entrou numa frase própria sobre procedência do modelo, com os números do R1 N5. A atribuição corrigida, não a citação removida, porque a obra sustenta a afirmação nova.

**Os dois números órfãos.** **Confirmados na fonte, não removidos.** `S3-agreement.md` Tabela S3.3c: tau-b mediano de 0,518 em fintech e 0,579 em varejo. Mas a mesma tabela dá 0,269 em saúde e 0,181 em tecnologia, o que o manuscrito não dizia. A frase de F §15 passou a carregar os quatro valores e a declarar que a propriedade que ela afirma — a ordenação dentro da vertical sobrevive à troca de fornecedor — vale em duas das quatro verticais medidas, com a fonte nomeada. Um número órfão virou um achado qualificado; a ressalva ficou mais forte, não mais fraca.

---

## 6. Contagem de palavras

Prosa corrida medida por `reviews/style_check.py`, que exclui tabelas, legendas, títulos, blocos de código, lista de referências, "Open marks", "Notes for the integrator" e a própria passagem anti-tique.

| Bloco | Prosa antes | Prosa depois | Δ | Arquivo inteiro depois |
|---|---:|---:|---:|---:|
| E | 3.870 | 4.491 | **+621** | 9.770 |
| F | 5.411 | 5.483 | **+72** | 13.707 |
| **Total** | **9.281** | **9.974** | **+693** | **23.477** |

O bloco F cortou cerca de 320 palavras de redundância e recuperou quase tudo em denominadores, remissões de proveniência e a qualificação dos dois tau-b. O bloco E sobe porque três dos seis BLOQUEIA trocam uma alegação curta por uma declaração de proveniência, que é mais longa por construção: o parágrafo que declara o recálculo e o que declara a execução sobre o corte superado somam sozinhos cerca de 280 palavras que não existiam, e a seção "Open marks" foi reescrita com o registro de tudo o que fechou. A subseção §9.7 dissolvida devolveu 84 palavras.

---

## 7. Medição de estilo final

`python reviews/style_check.py --blocks EF`, sobre o estado em disco depois das edições.

| Regra da C.1 (reprovação) | E antes | E depois | F antes | F depois |
|---|---:|---:|---:|---:|
| C.1.1 antítese de fórmula fechada | 0 | 0 | 0 | 0 |
| C.1.1 antítese graduada (veredito) | AVISO | **AVISO** | ok | ok |
| C.1.2 fecho pseudo-profundo | 0 | 0 | 0 | 0 |
| C.1.3 conectivo de enchimento abrindo parágrafo | 0 | 0 | 0 | 0 |
| C.1.4 primeira frase acima de 45 palavras | 2 | **0** | 1¹ | 1¹ |
| C.1.4 abertura que anuncia em vez de concluir | 0 | 0 | 3 | **0** |
| C.1.5 autonarração | 2 | **0** | 1 | **0** |
| C.1.6 meta-discurso de verificação | 0 | 0 | 0 | 0 |
| C.1.7 travessão em prosa | 0 | 0 | 0 | 0 |
| C.1.8 atribuição vaga | 1 | **0** | 3 | **0** |
| C.1.9 parágrafos acima de 2.200 | 0 | 0 | 0 | 0 |
| C.1.10 adjetivos vazios (veredito) | ok | ok | ok | ok |
| C.1.12 alerta rotulado | 0 | 0 | 0 | 0 |
| C.1.13 porcentagem sem denominador | 2 | **0** | 3 | **0** |
| C.1.14 rótulo de versão na prosa | 1 | **0** | 2 | **0** |
| PARTE D.2 afirmação de ausência não medida | 1 | **0** | 2 | **0** |
| C.2 aposição contrastiva (veredito) | ok | ok | ok | ok |

**Reprovações de C.1 restantes: zero nos dois blocos.** Eram E 8 e F 12.

**Três levantamentos remanescentes, nomeados e justificados:**

1. **E, C.1.1 antítese graduada, 1 ocorrência, veredito AVISO.** É o fecho de §9.4, "is therefore not a courtesy to the reader; it is the condition under which the figure identifies a quantity", a única antítese estrutural do bloco, mantida de propósito. A régua avisa na primeira e reprova na segunda; não há segunda. A passagem anti-tique declara e defende.
2. **E, C.1.10 e C.6, `robust`, 1 ocorrência.** É `cluster-robust`, nome do estimador de variância, não adjetivo de elogio. O limiar de reprovação da C.1.10 é cinco ocorrências ou raiz acima de duas, de modo que o veredito já é "ok" antes do julgamento. Mesmo falso positivo que a V2 e a V5 verificaram a mão.
3. **F, C.1.4, primeira frase de Acknowledgements com 52 palavras.** Acknowledgements é bloco de declaração e não seção de argumento, o que põe o caso fora da intenção da regra. As quatro seções numeradas medem 7, 35, 33 e 31 palavras. A V5 já o havia classificado como aviso e não reprovação.

Outros números finais: E com 4.491 palavras de prosa em 43 parágrafos e 164 frases, maior parágrafo de 1.386 caracteres, 12 itens visuais a 2.419 caracteres por item, 68 porcentagens na prosa, 69,8% dos fechos com cifra. F com 5.483 palavras em 60 parágrafos e 216 frases, maior parágrafo de 1.700 caracteres (o único acima de 1.500, declarado e defendido), 14 itens visuais a 2.533 caracteres por item, 19 porcentagens na prosa, 48,3% dos fechos com cifra. A conclusão-espelho de §16 contra o resumo do bloco A caiu de 29,8% para **26,7%** medida sobre a conclusão e de 55,4% para **52,6%** sobre o resumo. O detector de 7-gramas entre E e F continua em zero, e as cinco passagens que a leitura achava duplicadas foram cortadas.

---

## 8. O que foi recusado, e por quê

1. **A instrução de reparo da seção "Notes for the integrator" (F-4).** Recusada porque o montador não tem os dois defeitos que ela descreve. Testado e datado; a seção foi corrigida em vez de aplicada.
2. **Renumerar §10.2 pelo novo valor.** O título "One component carries three quarters of the index" continua, porque 72,4% é três quartos com a mesma honestidade que 74,7%. Não vale gastar um título numa mudança de 2,3 pontos.
3. **Adotar a regra de recência como painel primário da §10.** Recusada como primária e publicada como sensibilidade. A regra de recência descarta as 14.208 observações do braço aposentado, o que faria o denominador da §10 divergir das 68.624 de toda a §9 sem ganho de conclusão. A §10 declara o painel na legenda, que é o que a especificação exige e o que a implementação não fazia.
4. **Reproduzir a assimetria de numerador e denominador da implementação de referência.** Recusada. O `s6_index.py` restringe os dois ao painel, que é a definição que a §10.1 publica, e a divergência contra a implementação está declarada na Tabela F14 em vez de escondida.
5. **Corrigir `S5-window-validity.md` linha 404 (origem do 64,10%), `S2-temporal.md` linha 265 e a linha "Mean" da sua tabela (origem do 3,5), e a Tabela B4 do bloco B (mesma imprecisão de reasoning effort de F-12).** Fora do escopo, que autoriza apenas os dois blocos mais os arquivos novos de análise. Os três ficam registrados: enquanto não forem corrigidos, o manuscrito e os arquivos de estatística discordam nesses três pontos.
6. **Reduzir as duas máximas restantes de §13 a uma.** A V5 pede teto de uma máxima por seção e no fecho da seção. §13 ficou com uma no interior, "Adjacent problems take their own numbers, which is what allows an adopter to conform on observation without adopting anything else", que carrega a afirmação de modularidade ao lado dos números que a sustentam. Cortá-la retiraria conteúdo normativo, e a régua proíbe ganhar fluência às custas disso. Registrado como julgamento, não como omissão.
7. **Resolver 39,3% contra 39,33%.** O resumo do bloco A escreve 39,3% e F §16 escreve 39,33%; os dois estão certos e o resumo tem teto de palavras. Fora do escopo. A passagem anti-tique de F registra a divergência para o integrador.

---

## 9. Pendências que a montagem precisa resolver antes do merge

Registradas também no item 5 da seção "Open marks and number provenance" do bloco E, que a montagem remove, e repetidas aqui porque são de outro editor.

1. **A faixa 0,706 a 0,984 sobrevive nos blocos A e B.** O recálculo a leva a **0,752 a 0,985**. O bloco F foi atualizado nos dois lugares em que a carrega (§13 Scope e linha 20 da Tabela F1) e o bloco E na Tabela E10 e na §10.3. Enquanto A e B não forem atualizados, o manuscrito montado se contradiz. Mesma classe do 68.624 contra 66.399 que a V3 registrou e que este trabalho fechou no bloco F.
2. **As três fontes com número errado**, listadas no item 5 da seção 8.
3. **`stats/S1-multilevel.md` continua inexistente.** Se o modelo for ajustado depois, entra em E §9.2 no lugar da frase que hoje declara que ele não foi ajustado, e a linha do `s1_multilevel.py` na Tabela F14 deixa de precisar da nota que a acompanha.
