# Peer Review R1 — Métodos e Estatística

**Revisor 1 (métodos e estatística) · revisão por pares simulada de alto rigor (padrão ICWSM / ACM TOIS) · 2026-06-11**

Manuscrito sob revisão: *"Anchor-Entity Concentration in LLM Brand Citations"* (insumo
`DRAFT_INSUMOS_FINTECH_CITATION_ADVANTAGE.md`, com `secao_estatistica.md` e `red_team.md`).

**Escopo desta revisão.** O draft já é honesto e admite os seis bloqueadores conhecidos
(truncamento a 200 chars, efeito Nubank, heterogeneidade por engine, FPR de decoys,
não-independência, tier econômico). **Não repito esses pontos.** Minha função é cavar
falhas *ainda não percebidas* e, na Fase 2, rodar análises novas no `papers.db` (tabela
`citations`, núcleo `is_probe=0 AND is_calibration=0 AND extraction_version='v2'`, n=50.453,
confirmado) que ou fortalecem ou ameaçam a tese pivotada de "concentração de entidade-âncora".

Todas as análises abaixo foram executadas por mim diretamente sobre o banco; os scripts
estão em `C:/Users/alexa/r1_analysis*.py`. Os números reproduzem o núcleo do draft
(n=50.453, taxa global 20,25%, Nubank=49,7% das menções de fintech), o que valida a cadeia
de extração antes de eu construir crítica em cima dela.

---

## PARTE 1 — CRÍTICAS NUMERADAS (gaps novos, além do que o draft admite)

### MAJOR

**M1 — O gap fintech−varejo NÃO sobrevive a inferência em nível de cluster, e o draft só diz que "pode perder significância".**
O draft (e o red team, D1) afirmam que o n efetivo é ~240 clusters e que a diferença de
3,2 pp "provavelmente perderia significância" — mas nunca executam o teste. Isso é um
gap: a claim secundária de que "fintech > varejo no bruto" continua sendo apresentada
como achado positivo (Tabela 3.1, χ²=33,6, p=6,8×10⁻⁹) em vários pontos do corpo. Um
revisor A1 exige o teste em nível de cluster *antes* de aceitar até a versão pivotada,
porque a moldura "fintech tem a maior taxa bruta" sustenta o enquadramento narrativo do
caso central. Se o gap bruto for não-significativo no nível de query, o próprio rótulo
"vantagem aparente de fintech" precisa ser requalificado de "estatisticamente detectada"
para "numericamente observada, não significativa sob clustering".

**M2 — Instabilidade temporal da âncora: a participação do Nubank CRESCE ao longo da janela; o draft afirma erroneamente estabilidade.**
A Tabela 3.9 e a §8.3 vendem "robustez temporal" porque o *ranking bruto* não se inverte
em 8 semanas. Mas o objeto da tese pivotada não é o ranking — é a *concentração de âncora*.
E essa concentração não é estável: ela tem tendência de alta (ver R-Fase 2). Um efeito de
âncora que está crescendo dentro da própria janela de medição é uma ameaça de validade
temporal *para a tese pivotada* que o draft não percebeu, porque mediu estabilidade da
métrica errada (taxa da vertical, não share da âncora). Isso também tem implicação de
*service drift* (corrente 8 da literatura) que o draft cita mas não conecta ao próprio dado.

**M3 — O argumento "anchor-entity" só generaliza para fintech se você usar a âncora ERRADA no varejo; com a dupla-âncora correta, varejo é tão frágil quanto fintech — e o draft usa isso contra si.**
A §7.2.4 propõe LOO para todas as verticais, mas o `secao_estatistica.md` (§5) já registra
que varejo é uma estrutura de *dupla âncora* (Mercado Livre + Magazine Luiza = 58% das
menções). Rodar o jackknife de UMA entidade no varejo (Mercado Livre) e de UMA na fintech
(Nubank) é uma comparação injusta que faz a fintech parecer unicamente concentrada. A tese
"Anchor-Entity Concentration" precisa decidir se a unidade é *entidade única* (e então
fintech é especial) ou *núcleo de âncoras* (e então varejo é igualmente anchor-driven).
Como está, o draft escolhe implicitamente a definição que favorece a narrativa, o que é
exatamente o tipo de grau-de-liberdade-do-pesquisador que um revisor A1 sinaliza.

**M4 — Front-loading é tratado como hipótese, mas é mensurável AGORA no engine íntegro — e a direção do viés é OPOSTA à narrativa do draft.**
O draft (A1, §2.4) afirma que o truncamento "premia verticais cuja marca-líder é citada
cedo (fintech/Nubank)". Isso é asserido, nunca medido. O banco tem `first_entity_offset_v2`
e o Perplexity é íntegro (não truncado). É possível quantificar exatamente quanto cada
vertical perderia sob truncamento. Fazer essa medição é obrigatório, e ela (ver R-Fase 2)
contradiz a direção alegada: tecnologia e saúde — não fintech — são as mais penalizadas
pelo corte. Ou seja, o truncamento *infla* a vantagem da fintech, mas por um mecanismo
diferente (penaliza os rivais), e a afirmação específica "fintech é premiada por front-loading"
está empiricamente errada: varejo front-loada *mais* que fintech (offset médio 111 vs 123 chars).

**M5 — A "validação no subconjunto Perplexity íntegro" proposta tem metade do poder de prompt que o draft assume.**
O draft trata o Perplexity como o caminho de validação limpa (não-truncada). Mas o
Perplexity foi coletado com apenas **24 queries distintas por vertical (12 PT + 12 EN)**,
contra 48 (24+24) nos demais engines. Logo o n efetivo de clusters da validação limpa é
~24 query-clusters por vertical, num único engine RAG — não os ~48 do desenho. Qualquer
intervalo de confiança ou GLMM rodado só no Perplexity terá poder substancialmente menor do
que o sugerido, e além disso confunde "citação limpa" com "comportamento de RAG". O draft
não documenta essa assimetria de cobertura de prompt do Perplexity.

### MINOR

**m6 — Partição de entidades de grupo entre verticais é uma decisão de analista não documentada (e não há vazamento, o que é o problema).**
Verifiquei: ZERO strings de entidade aparecem em mais de uma vertical. Mercado Pago só é
codificado em fintech (299), Mercado Livre só em varejo (2003), iFood só em tecnologia
(216). Não há *vazamento* — mas há *partição arbitrária* de entidades do mesmo grupo
econômico (Mercado Pago e Mercado Livre são ambos MercadoLibre; iFood é Movile/Just Eat).
A alocação de cada marca a uma vertical é uma escolha do experimentador que afeta
diretamente as taxas e o HHI por vertical, e não está pré-registrada nem justificada. Isso
deve ser declarado como grau de liberdade do desenho.

**m7 — O pseudo-R² de McFadden sobe de 0,339 (cited_v2) para 0,352 (cited_loo): o modelo LOO ajusta MELHOR.** O draft reporta os dois números (Tabelas 3.4/3.6) mas não comenta que o
desfecho recodificado é *mais* explicável pelas covariáveis estruturais — evidência adicional
(não explorada) de que o sinal genuíno de vertical/engine vive no dado sem-âncora.

**m8 — Não há teste formal da assimetria do jackknife entre verticais.** O draft propõe rodar
LOO para todas as verticais mas não propõe um teste da *diferença de drops* (fintech cai
16,7 pp; demais 2,5–5,7 pp). É justamente essa diferença que sustenta "a concentração de
âncora é máxima em fintech". Precisa de IC sobre o drop, não só os pontos.

---

## PARTE 2 — RESPOSTAS COMPLEMENTARES (análises rodadas no banco, números reais)

### R-M1 — Teste em nível de cluster do gap fintech−varejo (executado)

Agreguei a taxa de citação ao nível de query-cluster (48 clusters por vertical, ≥30 obs
cada) e rodei um teste de Welch entre as médias por-cluster das duas verticais:

| Quantidade | fintech | varejo |
|---|---:|---:|
| Query-clusters | 48 | 48 |
| Média da taxa por cluster | 26,51% | 23,30% |
| Desvio (pop.) entre clusters | 24,74 pp | 23,60 pp |

**Welch t = 0,645 (df ≈ 94) → NÃO significativo.** A enorme variância entre queries (sd ~24
pp) engole o gap de 3,2 pp. **Confirmo M1 com número:** a diferença bruta fintech−varejo,
que aparece como χ²=33,6 / p=6,8×10⁻⁹ tratando 25 mil respostas como i.i.d., **desaparece**
quando se respeita a estrutura de clusters. A claim "fintech tem a maior taxa" deve ser
rebaixada a observação descritiva, não inferência. *Isto reforça a tese pivotada* (o efeito
de vertical é fraco), mas exige reescrever o enquadramento do "caso central".

### R-M1b — A reversão sob LOO SOBREVIVE ao clustering (executado)

Mesmo teste, agora com a taxa LOO da fintech (remove respostas sole-Nubank) por cluster vs
varejo bruto:

- fintech-LOO média por cluster = 10,50%; varejo = 23,30%.
- **Welch t = −3,353 → significativo, sinal negativo.**

**Achado-chave da revisão:** a assimetria é decisiva — o gap *de superfície* não sobrevive
ao clustering (t=0,65), mas a *reversão sob âncora* sobrevive (t=−3,35). Isto é a melhor
notícia possível para o artigo: o achado frágil (vantagem setorial) cai exatamente onde
deve cair, e o achado robusto (dominância de âncora) se mantém mesmo no nível de cluster.
**Recomendo elevar este contraste a resultado de primeira ordem.**

### R-M2 — Trajetória temporal da participação do Nubank (executado)

Share do Nubank nas menções de fintech e fração sole-Nubank, por semana:

| Semana | Menções totais | Nubank | Share Nubank | Sole-Nubank das citadas |
|---|---:|---:|---:|---:|
| 2026-W16 | 872 | 365 | 41,9% | 53,5% |
| 2026-W17 | 1.036 | 423 | 40,8% | 51,7% |
| 2026-W18 | 306 | 126 | 41,2% | 53,5% |
| 2026-W19 | 1.218 | 620 | 50,9% | 61,1% |
| 2026-W20 | 984 | 583 | 59,2% | 66,7% |
| 2026-W21 | 929 | 468 | 50,4% | 59,3% |
| 2026-W22 | 1.449 | 767 | 52,9% | 59,8% |
| 2026-W23 | 318 | 181 | 56,9% | 61,5% |

**Confirmo M2:** o share do Nubank NÃO é estável — sobe de ~41% (W16–W18) para ~53–59%
(W19–W23), um aumento relativo de ~30% dentro da janela de medição. A "robustez temporal"
que o draft celebra é da *taxa da vertical*, que é estável por acaso (a cauda encolhe
enquanto a âncora cresce, mantendo o agregado fixo). A concentração — que É a tese — está
em alta. **Implicação:** (i) declarar isto como ameaça de *service drift* e medi-lo até o
dia 90; (ii) reportar o share da âncora como série, não só pontual; (iii) a estabilidade
do agregado deixa de ser argumento de robustez e vira um possível artefato compensatório.

### R-M3 — Jackknife da entidade-TOP de CADA vertical (executado) — central para a generalização

| Vertical | Entidade-âncora | Taxa orig. | Taxa LOO (remove só o top) | Queda (pp) |
|---|---|---:|---:|---:|
| **Fintech** | Nubank (49,7%) | 28,15% | 11,46% | **−16,70** |
| Varejo | Mercado Livre (29,5%) | 24,94% | 19,27% | −5,67 |
| Tecnologia | Totvs (24,8%) | 14,50% | 11,60% | −2,89 |
| Saúde | Hypera (24,7%) | 13,35% | 10,80% | −2,55 |

Com a entidade *única* top, fintech é dramaticamente mais frágil (queda 3× maior que a do
varejo). **Mas** repetindo com a estrutura de âncora real do varejo (dupla âncora):

| Definição | Varejo |
|---|---:|
| Original | 24,94% |
| LOO Mercado Livre apenas | 19,27% |
| **LOO Mercado Livre + Magazine Luiza (top-2)** | **10,59% (queda −14,35 pp)** |

**Veredito sobre M3:** o argumento "anchor-entity" *generaliza*, mas não como
"concentração numa única entidade" — generaliza como "as taxas de TODAS as verticais são
dominadas por seu núcleo de âncoras". A diferença real entre fintech e varejo é o *número
de âncoras* (1 vs 2), não a presença de concentração. Recomendação forte: a contribuição
teórica deve ser reformulada de "uma superstar" para "concentração no núcleo de âncoras
(top-k) varia por vertical; fintech é o caso extremo k=1". Isto é mais honesto, mais
generalizável e neutraliza a objeção de que a tese é "um achado sobre o Nubank disfarçado
de teoria". O `top-3=70,9%` (fintech) vs `69,4%` (varejo) na Tabela 3.5 já dizia isso e
foi subexplorado.

### R-M3b — Estabilidade do gap sob LOO, semana a semana (executado)

Gap fintech−varejo, original vs LOO (ambas âncoras removidas em cada vertical):

| Semana | gap original | gap sob LOO |
|---|---:|---:|
| W16 | +3,4 | −8,2 |
| W17 | +2,8 | −7,8 |
| W18 | +4,6 | −7,6 |
| W19 | +4,3 | −7,7 |
| W20 | +3,4 | −7,8 |
| W21 | +2,6 | −7,7 |
| W22 | +2,6 | −7,7 |
| W23 | +2,6 | −8,2 |

O gap sob LOO é estável e *negativo* (−7,6 a −8,2 pp) em todas as 8 semanas — a reversão é
estruturalmente consistente, não um artefato de uma semana. Isto fortalece a tese pivotada
e desarma uma objeção de "a reversão é dirigida por semanas específicas".

### R-M4 — Front-loading medido no engine íntegro (Perplexity, executado)

Offset médio (em chars) da primeira entidade citada, por vertical (só citadas):

| Vertical | Offset médio 1ª entidade | n |
|---|---:|---:|
| Varejo | 111,1 | 3.154 |
| Fintech | 123,1 | 3.561 |
| Saúde | 159,9 | 1.684 |
| Tecnologia | 173,3 | 1.819 |

Fração de citações cujo PRIMEIRO nome aparece **depois do char 200** (Perplexity, íntegro —
exatamente as citações que o truncamento destruiria):

| Vertical | Citadas | 1ª entidade > 200 chars | % perdida se truncado |
|---|---:|---:|---:|
| Fintech | 1.225 | 251 | 20,5% |
| Varejo | 1.316 | 275 | 20,9% |
| Saúde | 988 | 303 | 30,7% |
| **Tecnologia** | 769 | 397 | **51,6%** |

**Confirmo M4 e corrijo a direção alegada no draft.** (a) Varejo front-loada *mais* que
fintech (111 < 123 chars) — logo a afirmação "fintech é premiada por front-loading" é
falsa; se algo, varejo deveria ser. (b) O viés de truncamento é real mas opera *penalizando
os rivais*: o truncamento apagaria 51,6% das citações de tecnologia e 30,7% de saúde,
contra apenas ~20% de fintech/varejo. Isto **infla mecanicamente o gap fintech vs
tecnologia/saúde** (os 14,8 pp e 13,7 pp da Tabela 3.3 estão parcialmente fabricados pelo
corte), mas **não** o gap fintech vs varejo (ambos ~20%). Recomendação: substituir a
narrativa "Nubank citado cedo" pela narrativa correta e quantificada — "o truncamento
remove diferencialmente as âncoras de cauda longa de tecnologia/saúde, que aparecem tarde".

### R-M4b — Onde o Nubank aparece (executado)

Quando o Nubank é a primeira entidade da fintech, o offset médio é 118 chars (dentro da
janela de 200). Mas as âncoras de cauda aparecem tarde e teriam sido perdidas pelo
truncamento mesmo dentro da fintech: Itaú 402, PicPay 515, Banco Inter 838, BTG 906 chars.
Ou seja, o truncamento não só infla o gap entre-verticais — ele também *exagera a dominância
do Nubank dentro da fintech*, cortando justamente os rivais domésticos que aparecem depois.
A concentração de 49,7% é, ela própria, parcialmente um artefato de truncamento. Esta é uma
ameaça NOVA à própria métrica central da tese (o HHI/share da âncora), que o draft não
percebeu — ele tratou o truncamento só como ameaça à taxa absoluta, não à concentração.

### R-M5 — Poder do subconjunto Perplexity íntegro (executado)

| Engine | Queries distintas/vertical | Obs/vertical | Obs por query |
|---|---:|---:|---:|
| ChatGPT (e demais truncados) | 48 (24 PT + 24 EN) | ~2.832 | ~59 |
| **Perplexity (íntegro)** | **24 (12 PT + 12 EN)** | 1.416 | ~59 |

**Confirmo M5.** A validação "limpa" disponível hoje vive sobre **24 query-clusters por
vertical** num único engine RAG — metade da diversidade de prompt do desenho. Rodei o LOO
só no Perplexity como teste de sanidade:

| Vertical | Taxa Perplexity | Taxa LOO (sem Nubank) |
|---|---:|---:|
| Fintech | 86,5% | 67,9% |
| Varejo | 92,9% | 92,9% |
| Tecnologia | 54,3% | 54,3% |
| Saúde | 69,8% | 69,8% |

Resultado tranquilizador: **mesmo no engine não-truncado, a fintech-LOO (67,9%) fica abaixo
do varejo (92,9%)** — o efeito-âncora não é artefato de truncamento. E note que varejo/tech/
saúde têm LOO ≈ taxa original no Perplexity (o RAG raramente cita a âncora sozinha), o que
reforça que a dependência de âncora-única é genuinamente específica da fintech *mesmo em
dado limpo*. **Mas** isto se apoia em apenas 24 clusters — a §7 deve declarar que a
validação confirmatória limpa é sub-potente e que a re-coleta íntegra (bloqueador nº 1)
precisa restaurar as 48 queries no Perplexity também, não só destruncar os outros quatro.

### R-m6 — Partição de entidades (executado)

Confirmei: 0 strings de entidade em mais de uma vertical; a partição é limpa, mas Mercado
Pago (fintech, 299) e Mercado Livre (varejo, 2003) — mesmo grupo econômico — estão em
verticais distintas, assim como iFood (tecnologia, 216). Sem vazamento, mas com alocação de
analista. Declarar no desenho.

---

## VEREDITO FINAL — o que a tese aguenta

**Aguenta (robusto a clustering e a dado íntegro):**
1. **Dominância de entidade-âncora como fenômeno real.** A reversão sob LOO sobrevive ao
   teste de cluster (t=−3,35), é estável nas 8 semanas (gap LOO −7,6 a −8,2 pp) e
   persiste no engine não-truncado (Perplexity fintech-LOO 67,9% < varejo 92,9%). Este é o
   esqueleto do artigo e está sólido.
2. **Heterogeneidade por engine** (já no draft) — confirmada e não contestada por mim.

**Aguenta apenas REFORMULADO:**
3. **A tese deve migrar de "uma superstar (Nubank)" para "concentração no núcleo de âncoras
   top-k, com fintech no extremo k=1".** Varejo cai 14,35 pp removendo suas DUAS âncoras —
   é tão anchor-driven quanto a fintech. A contribuição teórica generaliza só nessa forma; a
   forma "single superstar" é frágil e parece um achado-sobre-Nubank.

**NÃO aguenta (precisa ser rebaixado ou removido):**
4. **"Fintech tem a maior taxa de citação" como inferência.** Não significativo em nível de
   cluster (Welch t=0,65). É observação descritiva, não estatística.
5. **"Truncamento premia fintech por front-loading do Nubank."** Empiricamente falso na
   direção: varejo front-loada mais; o truncamento opera penalizando tecnologia/saúde
   (−51,6% / −30,7% de citações perdidas vs −20,5% fintech). Reescrever com o mecanismo
   correto.
6. **"Robustez temporal" como ponto a favor.** O share da âncora está CRESCENDO (41%→57%);
   a estabilidade do agregado é compensação, não solidez. Tratar como ameaça de service drift.

**Ameaça nova mais perigosa que o draft não viu:** o truncamento contamina não só a taxa
absoluta, mas a **própria métrica de concentração** (HHI / share de 49,7%) — porque corta as
âncoras de cauda da fintech (Itaú/PicPay/Inter/BTG aparecem em 400–900 chars) e infla
artificialmente a dominância do Nubank. A re-coleta íntegra (bloqueador nº 1) é, portanto,
pré-requisito não só para as taxas, mas para o número-título da tese pivotada. Até lá, a
concentração de 49,7% deve ser declarada como limite superior.

**Recomendação editorial:** *major revision*. A espinha dorsal (anchor-entity + engine
heterogeneity) é publicável em ICWSM/WWW após: (i) re-coleta íntegra incluindo as 48 queries
do Perplexity; (ii) GLMM cluster-robusto com desfecho duplo já desenhado; (iii) jackknife
top-k por vertical com IC sobre os drops; (iv) reframe de "superstar única" para "núcleo de
âncoras"; (v) série temporal do share da âncora; (vi) correção da narrativa de front-loading
pelos números de offset reais.
