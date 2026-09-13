# V3 — Aplicação das revisões V1 e V2 aos blocos A a D

**Data:** 2026-09-11 · **Arquivos editados:** `sections/A-front-intro-related.md`, `B-specification-instantiation-adoption.md`, `C-field-record-missingness.md`, `D-window-decoys.md`. Nenhum outro arquivo foi alterado. Nenhum comando git alterou estado. O banco foi aberto somente em modo leitura.

---

## 1. Os quatro BLOQUEIA

| # | Onde | O que ficou no texto |
|---|---|---|
| 1 | A §2.2 | A frase que chamava [Xu2026] de ancoragem revisada por pares e negava que qualquer número viesse de preprint saiu. Entrou a contagem real, **oito dos doze trabalhos de 2026 citados na seção são preprints de autor único**, as quatro ancoragens corrigidas para [Aggarwal2024], [Wen2026], [Grossman2026] e [Mosnar2025], e a distinção entre reportar o número como alegação da obra e depender dele: nenhuma figura de §§3 a 16 depende de preprint. |
| 2 | B §4.1 | A alegação de coorte com empresas fundadas depois de 2020 saiu inteira. Conferi `src/config_v2.py` diretamente: 111 entidades reais, ano mínimo 1849, **ano máximo 2019**, e apenas três membros de 2018 ou 2019. O texto agora declara a ausência da propriedade: a coorte foi desenhada para sondar a defasagem de pré-treino, **não a alcança**, o indicador de fundação pós-corte não tem casos e §9 não o ajusta, de modo que o mecanismo de [Xu2024] permanece não testado aqui. |
| 3 | B §4.7 | A frase do TTL de oito horas saiu. Conferi `src/config.py:549`, `src/shared/llm_utils.py:38` e `src/collectors/response_cache.py:27`: padrão 20 horas nos três, nenhum workflow ou `.env` sobrescreve. O texto agora diz qual é o valor (20 h), por que ele sozinho **permitiria** um HIT entre a rodada da manhã e a da noite, e qual é a proteção real: `data/cache/` fora do versionamento e runner efêmero, tanto no `schedule` quanto no `workflow_dispatch` de `daily-collect.yml`. A exposição é declarada: uma corrida disparada de cópia local com cache persistente não tem essa proteção, e **nenhuma coluna de `citations` registra se a linha veio de cache**, então ela não seria identificável depois. Acrescentei a única evidência que existe contra a hipótese, que é do próprio dossiê: a concordância teste-reteste no mesmo dia vai de 0,835 a 0,992 e um cache servido devolveria exatamente 1,0. |
| 4 | B §4.4 | O texto dizia que as 206 observações de 2026-08-23 foram descartadas e que 206 de ~18.000 seria arredondamento. Recontei no banco: 158 canônicas + 48 de sondagem = 206, e **as 158 estão dentro das 1.118 do arm**. O texto agora declara a divergência: a decisão declarada foi descartar, as tabelas não a implementam, a discrepância é 14% do arm, e reconciliá-la mudaria toda figura do Grok em §9. |

---

## 2. Os vinte CORRIGIR

Aplicados, conferidos contra a fonte antes de colar.

**Bloco A.** Resumo: kappa 0,086 recolocado sobre **9.129 células e 50 dias** (S3 Tabela S3.1a) e 39,3% recolocado como variância do logit da cobertura sobre **62 entidades por 6 motores** (S3 Tabela S3.4-bis). Destaque 4: "over 53 days" → "over 9,129 cells" (74 caracteres). §1.1: par de taxas reescrito. §1.2: "over 53 collection days" → "over the collection days of the series". §1.3 e §2.8: cinco defeitos → **sete**.

**Bloco B.** §12.1, §12.2 linha 3 e passe anti-tique: 68.624 → **66.399** (NUMBERS T3 confirma o corte de 2026-08-31 com 66.399 e o acréscimo de 2.225). §12.1: as três taxas de recuperação de P1 e a ablação de P6 passam a nomear a coorte de três dias e seu n. §4.1: `legal_status` passa a declarar a variância real, 110 ativas e uma em recuperação judicial. Tabela B4, linha de variação entre execuções: "small at temperature 0 and not zero" → a medição, 0,835 a 0,992 por arm com kappa 0,669 no arm de recuperação (S3 Tabela S3.0b). §12.3: a aritmética de 49 contra 50 recebe a ressalva de R3 §4.3. §3.1 P2: [Chu2026] reescrito conforme R1 N7, colapso disparado por vantagem de avaliação e não por composição do conjunto.

**Bloco C.** Legenda da Tabela C1: "Seven" → **"Eight defects ... grouped into the seven episodes §5.3 narrates"**, com o título da subseção mantido em sete. §5.3: mesma ressalva de 49/50. §8.2: as duas regras de dia parcial passam a aparecer lado a lado, 19 pela regra do table build e **8** pela regra da análise temporal (S2 Tabela 3, conferida), com a regra de cada uma enunciada. Tabela C2, linha do marcador de alucinação: 67,5% ganha o denominador, **11.195 de 16.579 no snapshot daquele dia** (R3 T44). §5.3: "(Table 9)" → **"(Table D8)"**. Chave [Zatuchin2026] → **[Zatuchin2026a]** nas duas ocorrências.

**Bloco D.** §6.4: "a factor of two to nine" → **"factors of 2.9 to 5.3"**, recalculado contra as MDD pareadas de S5 Tabela S5.12 (ChatGPT 12,5; Claude 13,0; Gemini 5,8; Grok 13,1; Perplexity 12,5). §7.3: a faixa 4.096–4.463 passa a nomear **os quatro arms paramétricos da série inteira, com 368 para o arm de agosto**. §7.1: "ran for seventeen days" → **"contributed five collection days inside a seventeen-day calendar span"**, confirmado no banco (5 dias canônicos distintos). Chaves [Pan2025] → [Pan2026], [JCGM2008] → [JCGM100], [JCGM2012] → [JCGM200].

### CONFERIR resolvidos com dado novo

- **D §7.2, exemplo de recusa.** Em vez de remover, extraí do banco em modo leitura uma linha verbatim: resposta Gemini de 2026-04-29 que declara, sobre o chamariz do próprio prompt, *o "Banco Floresta Digital" não é uma instituição financeira real ou registrada no Brasil*. O exemplo agora é verificável.
- **D §6.3, "that table" sem antecedente.** Resolvido sem inventar remissão: a frase passa a dizer que, sob a mesma re-extração, **os outros cinco arms** têm delta exatamente zero (NUMBERS T3 confirma cinco).
- **D §6.6, percentual sem denominador.** O n por célula saiu de `stats/data/s5_preamble_by_cell.csv`: cada célula motor-por-vertical do Grok tem 96 en + 96 pt = **192 observações**, e as médias reproduzem 2,6% / 16,7% e +35,4 / +72,9. A frase agora nomeia os 192.
- **B §4.1, "at least three long-tail firms per vertical".** V1 não conseguiu separar por vertical. Separei: fintech 5, varejo 6, saúde 5, tecnologia 7. O texto foi **fortalecido** para "at least five", que é o que a coorte sustenta.
- **A §2.4, [Pan2026] e probabilidade de erro.** Sem acesso ao arXiv nesta sessão, apliquei a redução que V1 autoriza: a frase agora diz que a recusa consciente do conhecimento é medida em tarefas factuais, sem atribuir a relação entre probabilidade de recusa e probabilidade de erro.
- **C §5.2, data da auditoria de cinco agentes.** A data de 2026-04-22 foi removida por não ter fonte; ficou "A five-agent audit listed more than 95 gaps", com a implementação datada em 2026-04-23, que R3 T10/I3 sustentam.
- **Transversal, 52 contra 53 dias.** Não adotei um número único, porque tanto 52 quanto 53 estão corretos sob a própria regra e trocar a régua invalidaria os 19 dias parciais, os 328/344 e a Tabela B4, todos computados sob a regra do table build. Em vez disso a convenção foi escrita em C §8.2: as duas regras são enunciadas com sua razão física, e o texto declara que **toda figura que depende de contagem de dia diz qual das duas usa, e que a contagem sem qualificação é a do table build**. A regra foi propagada a B §4.7, à legenda da Tabela B4 e ao formulário de §12.1, que agora traz "53 collected days under the table-build date rule; 52 under the local-date rule of §8.2". A menos segura das três aparições, o meio-intervalo 0,29/2,29 de A §1.2, perdeu o número de dias porque S2 não o atribui a uma contagem específica.

---

## 3. Estilo: as dezesseis reprovações

Aplicadas todas. As duas antíteses do bloco D receberam as formas que B §3.1 P1 e B §12.3 / C §5.4 já usavam para os mesmos fatos, sem reescrita nova. As três primeiras frases acima de 45 palavras (B §4.2, B §4.5, D §6.4) foram reordenadas com a conclusão na frente. A autonarração de A §2.8 e a afirmação de ausência de A §1.1 ("the one no vendor publishes") saíram. As duas negativas universais de B (§3.1 P6, §3.7) e a de D §6.3 ("the market did not") saíram. Os dois percentuais sem denominador de D §6.6 ganharam base. O rótulo de confiança de D §7.2 ("a fraction of it") foi trocado pelas duas proporções medidas.

**As treze referências a "v1.0" na prosa** foram substituídas pelo registro datado a que remetem, com todos os números preservados: em C, o "event table of v1.0" virou "the event register as it stood at the first analysis" e os quatro eventos viraram "the four registered events"; em D, a errata de §6.3 virou uma medição sobre a série que fechou em 2026-08-31. O medidor lê **zero** em C.1.14 nos quatro blocos. Três ocorrências ficam fora da prosa e foram mantidas de propósito: o campo "Specification version BRGEO-1, v1.0" do formulário de conformidade, que é conteúdo do campo, e as duas notas de proveniência das listas de referência de A e D, que dizem de qual lista cada entrada veio e são o rastro que um editor precisa.

**A nota de rascunho de C §8.2** ("The manuscript should settle on one before submission") saiu, substituída pela convenção descrita acima.

**As declarações de limpeza falsas.** Os quatro "Anti-tic pass" foram reescritos para descrever o texto entregue, e agora cada afirmação com número foi medida em `style_check.py` sobre o arquivo entregue. As cinco declarações que a V2 derrubou estão corrigidas e nomeadas como corrigidas: a antítese de D item 1 que tinha reintroduzido a forma banida, o "every percentage was checked" de D item 5 que não cobria o parágrafo de preâmbulo, a afirmação de ausência sobrevivente em A §1.1, o fecho de §2.8 que trocou C.1.2 por C.1.5, e a citação desatualizada de "Three recent measurements" quando o texto diz quatro. Cada passe agora declara também as regras que a passagem anterior **não** rodou.

### Avisos da C.2 tratados

Os quatro que a V2 marcou como "valem correção": Tabela C3 criada em C §8.4 a partir dos quatro rompimentos não declarados, o que baixa a densidade de apoio visual de 10.877 para 7.338 caracteres por item; dois advérbios em `-ly` retirados de A §2.7, que cai de cinco para três no parágrafo mais carregado; as duas quantidades sem contagem de A §2.2 e §2.5 agora trazem número; e os dois títulos de gaveta do bloco D viraram afirmação, "One arm moves 22.8 points on re-extraction" e "Every arm gains and no arm loses".

---

## 4. A redundância entre blocos

| Passagem | Dono | O que os outros carregam agora |
|---|---|---|
| Conversão de medição de resposta inteira em medição de cabeça de resposta | **B §3.1, P1** | A §2.7 e D §6.2 remetem em uma linha: "the conversion P1 describes (§3.1)". A célula P1 da Tabela B1 fica, por ser a coluna de modo de falha do próprio parâmetro. |
| História da detecção distribucional | **C §5.3** | B §12.3 e D §6.2 remetem em uma linha. B mantém só o cheque transferível, "run that check on day one"; D mantém a Tabela D1 e a leitura de máximo igual a mínimo. |
| As duas notas do VIM 2.27 | **A §1.2** | B §3 e D §6.1 citam a cláusula e apontam para §1.2. D mantém o que é só dele, que chamar a diferença de erro de medição concede a coisa errada. |

O parágrafo "**Declaration.**" de D §6.7 foi cortado para uma linha que aponta para o fecho de §6.5, que já o conclui.

Os cortes somam cerca de 330 palavras de prosa. O bloco A perde 45, B perde 95, D perde 190. O total dos quatro blocos **sobe** mesmo assim, porque três dos quatro BLOQUEIA trocam uma alegação curta e falsa por uma declaração de ausência, que é mais longa por construção: a coorte sem casos pós-corte, o cache sem proteção de TTL e as 206 linhas que continuam nos denominadores custam juntas cerca de 250 palavras que não existiam.

---

## 5. Chaves de citação

Uniformizadas nos quatro blocos: **[Zatuchin2026a]** para o Dice Roll (C corrigido), **[Pan2026]** para Pan e colegas com ano 2026 conforme DECISIONS §8 (D corrigido, citação de §7.2 incluída), **[JCGM200]** e **[JCGM100]** para VIM e GUM (B saía de [VIM2012]/[GUM2008], D de [JCGM2012]/[JCGM2008]), **[ISO17000]** e **[ISO5725-2]** para as normas, que já estavam corretas em A e B. As entradas renomeadas foram reposicionadas na ordem alfabética da lista de B. Uma varredura por [Zatuchin2026], [Pan2025], [VIM2012], [GUM2008], [JCGM2008] e [JCGM2012] nos quatro arquivos retorna zero.

---

## 6. A voz do bloco B

Os três movimentos mínimos, aplicados sem achatar a diferença entre seção normativa e relato de campo:

1. **Teto de uma máxima por seção, no fecho da seção.** A de §4.5 ficou onde é ganha. A de §12.1 ("A claim form whose only possible answers are favourable is a marketing artefact") virou sua própria evidência: "The Level 2 line is the one a claimant would omit, and it is the line that tells a reader that 66,399 of the 68,624 observations behind every rate in §9 cannot be re-extracted by anyone."
2. **Número ao lado da máxima, em C §5.3.** A frase sobre credenciais compartilhadas passou a carregar as 49 execuções de que 3 tiveram sucesso dentro da mesma sentença.
3. **As duas antíteses de D** trocadas pelas formas de B e C, conforme §3 acima.

O `MUST`/`SHOULD` de B, a ancoragem em linha de arquivo de C, as cadeias de citação de A e a densidade numérica de D não foram tocados.

---

## 7. O que foi recusado, e por quê

1. **Trocar 53 por 52 em todo o manuscrito** (V1 Nota A-i). Recusado. As duas contagens estão corretas sob a própria regra, e a regra do table build é a que produziu os 19 dias parciais, os 328 contra 344 e a linha de split par-ímpar da Tabela B4. Adotar 52 e manter esses números seria trocar uma incoerência silenciosa por outra. O manuscrito passa a declarar as duas regras e qual cada figura usa, que é o que a própria proposta da V1 para C §8.2 já pedia.
2. **Substituir "v1.0" nas notas de proveniência das listas de referência de A e D.** Recusado. A V2 contou treze ocorrências, todas em prosa de C e D, e essas não estão entre elas. Elas dizem de qual lista cada entrada de referência veio, servem ao editor que monta o manuscrito e somem na montagem junto com a seção que as contém.
3. **Renomear B §4.3 e B §4.4** (títulos de gaveta, aviso 4 da V2). Recusado. As sete subseções de §4 são nomeadas pelos parâmetros P1 a P6 que instanciam, em paralelo com §3.1. Renomear duas delas quebraria o mapeamento que o leitor usa para ir de um requisito à sua instanciação. Os títulos de gaveta do bloco D, que não têm esse paralelo, foram trocados.
4. **Converter os dez usos tautológicos de `rather than` no bloco B** (V2 §8 item 3). Recusado nesta passagem. A PARTE C não lista a construção, a própria V2 a propõe como aviso para a próxima revisão da régua, e converter dez ocorrências é reescrita de voz num bloco normativo assinado pelo custodiante, que é exatamente onde uma reescrita ampla arrisca mudar a força de um requisito. A contagem medida, 29 na prosa de B contra 3, 13 e 8 nos outros, ficou registrada no passe anti-tique do próprio bloco.
5. **As quatro subseções de A §2 em que a afirmação chega depois da palavra 120** (V2 item 8). Aplicado em §2.1, §2.3 e §2.7, com a frase existente movida para a cabeça do primeiro parágrafo. Não aplicado em §2.4, que estava quatro palavras acima do teto e cuja primeira frase já enuncia a diferença de papel dos chamarizes; mover a frase seguinte desmontaria a montagem do argumento sobre entidades fictícias sem ganho mensurável.
6. **Corrigir `stats/S5-window-validity.md` §6 e §3, `src/config.py:549` e `docs/METHODOLOGY_V2.md:105`.** Fora do escopo desta tarefa, que autoriza apenas os quatro blocos. Ficam registrados: S5 §6 repete o "between two and nine times" que D §6.4 acaba de corrigir; S5 §3 põe Perplexity em quarto quando a própria Tabela S5.1 a põe em segundo com 77,0; `config.py:549` traz TTL 20 contra as 8 horas que `METHODOLOGY_V2.md:105` declara reduzidas. Um dos dois lados tem de ceder antes da submissão.
7. **A colisão do número 0,086 entre A e D** (V2 §8 item 1). Não alterado, por decisão explícita: em A é um nível de kappa de Fleiss e em D é uma diferença de kappa, ambos corretos, e §9 está fora do escopo desta tarefa. Fica registrado como pergunta que um revisor fará.
8. **Tabela E10 do bloco E**, a origem de 0,706 a 0,984 (V1, item 1 do que não conseguiu verificar). O número fica no resumo de A porque confere contra o bloco E, mas continua sem instrução registrada em `NUMBERS.md`, o que viola a regra final daquele arquivo. Bloco E está fora do escopo.
9. **O mesmo erro de 68.624 contra 66.399 sobrevive no bloco F.** Depois de corrigir as três ocorrências de B, varri os seis blocos: `F-governance-threats-discussion.md:149` ainda diz "the whole response was not retained before 2026-08-31, so 68,624 canonical observations cannot be re-extracted by any party at any other window". O número correto é **66.399**, pela mesma aritmética que D §6.7 já publica (68.624 − 2.225). Não editei, porque F está fora dos quatro arquivos autorizados. Corrigir antes da montagem, senão o manuscrito reunido contradiz a si mesmo em duas seções.

---

## 8. Palavras por bloco, antes e depois

Prosa corrida medida por `style_check.py`, que exclui tabelas, blocos de código, títulos, listas de referência, legendas, a especificação da Figura D1 e o próprio passe anti-tique.

| Bloco | Prosa antes | Prosa depois | Δ | Arquivo inteiro depois |
|---|---:|---:|---:|---:|
| A | 3.835 | 3.908 | +73 | 8.774 |
| B | 4.360 | 4.575 | +215 | 9.321 |
| C | 3.412 | 3.468 | +56 | 6.126 |
| D | 3.455 | 3.415 | −40 | 7.088 |
| **Total** | **15.062** | **15.366** | **+304** | **31.309** |

O resumo do bloco A permanece em **exatamente 200 palavras**, conforme DECISIONS §3, e os cinco destaques permanecem em 74, 70, 71, 74 e 65 caracteres, todos abaixo do teto de 85.

---

## 9. Medição de estilo final

`python reviews/style_check.py`, sobre o estado em disco depois das edições.

| Regra da C.1 (reprovação) | A | B | C | D |
|---|---:|---:|---:|---:|
| C.1.1 antítese, fórmula fechada | 0 | 0 | 0 | 0 |
| C.1.1 antítese graduada | 0 | 0 | 0 | **0** (era 2) |
| **C.1.1 veredito** | ok | ok | ok | **ok** (era FALHA) |
| C.1.2 fecho pseudo-profundo | 0 | 0 | 0 | 0 |
| C.1.3 conectivo de enchimento abrindo parágrafo | 0 | 0 | 0 | 0 |
| C.1.3 densidade de conectivo gasto (limiar 1,00) | 0,06 | 0,00 | 0,00 | 0,00 |
| C.1.4 primeira frase de seção acima de 45 palavras | 0 | **0** (era 2) | 0 | **0** (era 1) |
| C.1.5 autonarração | **0** (era 1) | 0 | 0 | 0 |
| C.1.6 meta-discurso de verificação | 0 | 0 | 0 | 0 |
| C.1.7 travessão em prosa corrida | 0 | 0 | 0 | 0 |
| C.1.8 atribuição vaga | **0** (era 1) | 0 | 0 | **0** (era 1) |
| C.1.9 parágrafos acima de 2.200 caracteres | 0 | 0 | 0 | 0 |
| C.1.10 veredito de adjetivos vazios | ok | ok | ok | ok |
| C.1.12 alerta rotulado | 0 | 0 | 0 | 0 |
| C.1.14 histórico de versão na prosa | 0 | 0 | **0** (era 6) | **0** (era 7) |
| C.2 aposição contrastiva, veredito | ok | ok | ok | ok |

**Reprovações de C.1 restantes: zero nos quatro blocos.** As reprovações contadas pela V2 eram A 2, B 4, C 3, D 7, total 16.

### Os dois falsos positivos que sobrevivem

1. **Bloco C, C.6 e C.1.10, `robust`.** A única ocorrência é `cluster-robust standard errors` em §5.2, nome de um estimador de variância. Não é adjetivo de elogio, e o limiar de reprovação da C.1.10 é cinco no texto ou raiz acima de dois, de modo que uma ocorrência fica em "ok" mesmo antes do julgamento. A V2 já o havia classificado como técnico.
2. **Bloco D, C.6, `not only`.** A ocorrência é "and not only in aggregate" em §6.4, um advérbio de escopo sobre o resultado de perdas zero. A entrada #31 da C.6 visa a fórmula `not only X but also Y`, que não ocorre. É o mesmo falso positivo que a V2 já havia verificado a mão.

### Avisos da C.2 que permanecem, com a resposta

- **Apoio visual em A**, 13.366 caracteres por item contra o piso de 5.000. Uma introdução e um trabalho relacionado não têm item empírico a exibir e as tabelas do artigo começam em §3. Respondido no passe do bloco, não corrigido.
- **Apoio visual em C**, 7.338 caracteres por item, vindo de 10.877. A Tabela C3 cobriu o lugar que a V2 apontou. O que resta acima do piso é §5.3, onde cada defeito é um bloco de prosa, e §8.3, onde duas políticas são comparadas.
- **Um parágrafo de B acima de 1.500 caracteres**, a entrada de P6 em §3.1 com 1.685. Declarado e defendido no passe: separar o resultado da ablação da ressalva de transferência que o qualifica custaria mais do que o comprimento. O parágrafo do cache em §4.7 chegou a 1.542 na primeira versão desta edição e foi partido no ponto em que o assunto muda do cache para o hash armazenado.
- **`rather than` no bloco B**, 29 ocorrências na prosa, 6,3 por mil palavras. Fora da régua, recusado acima e registrado no passe do bloco.
- **Diagnósticos da C.3**, que a régua manda reportar e nunca transformar em meta: frase média de 24,3 a 25,9 palavras, desvio de 11,4 a 13,8, mínimo de 1 a 3 e máximo de 55 a 68, com uma frase acima de 60 em A e duas em B.
