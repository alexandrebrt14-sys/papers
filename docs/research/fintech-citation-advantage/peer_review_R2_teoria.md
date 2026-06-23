# Peer Review R2 — Teoria, literatura e contribuição

> Revisor 2 (hostil, A1) numa revisão por pares simulada do manuscrito
> "Anchor-Entity Concentration in LLM Brand Citations". Foco exclusivo:
> teoria, contribuição e enquadramento na literatura. As questões de método,
> estatística e medição (truncamento de 200 chars, GLMM, FPR de decoys) são do
> Revisor 1 (metodologia) — aqui só entram quando contaminam a contribuição teórica.
>
> Estrutura: FASE 1 (críticas, brutalmente honestas) e FASE 2 (respostas
> complementares robustas, com referências verificadas e parágrafos prontos para o
> paper). Buscas web realizadas em 11 de junho de 2026 estão reportadas integralmente.
>
> Veredito de capa: **major revision**. A contribuição empírica é real e o dataset é
> diferenciado, mas o manuscrito, como está, descreve um fenômeno sem construí-lo
> como teoria, e subexplora correntes de literatura que decidem a novidade. Não é
> rejeição: é um paper a uma camada teórica de distância de ser defensável.

---

## FASE 1 — CRÍTICAS

### Crítica 1 (a) — "Anchor-Entity Concentration" é construto ou é rótulo descritivo?

Esta é a objeção mais grave e ela atinge o título. O manuscrito **nomeia** um
fenômeno ("entidade-âncora", "anchor entity", "share of model") mas não o **define
como construto**. Um construto teórico precisa de três coisas que o draft não entrega:

1. **Definição operacional independente do dado que ele explica.** Hoje a "entidade-âncora"
   é definida circularmente: é a entidade que concentra as menções (Nubank, 49,68%); e a
   "concentração de âncora" é medida pela participação dessa mesma entidade. Isto é uma
   estatística descritiva (um HHI alto com um líder destacado), não um construto. Um
   revisor de IO perguntaria: qual é o limiar? A partir de que participação/HHI uma
   vertical "tem âncora"? Varejo tem dois líderes (Mercado Livre + Magalu) — é "bi-âncora"
   ou "sem âncora"? Sem critério, o construto não é falsificável.

2. **Um mecanismo causal formal que ligue estrutura de mercado → frequência de corpus →
   probabilidade paramétrica → taxa de citação.** O `mecanismos.md` é excelente como
   narrativa em três camadas (A oferta / B treino / C mercado), mas é **uma taxonomia de
   hipóteses, não um modelo gerador**. Falta a peça que transformaria isso em teoria: uma
   afirmação funcional do tipo "a probabilidade de uma entidade *e* ser citada
   espontaneamente é uma função monotônica de sua frequência relativa no corpus de
   pré-treino, que por sua vez é uma função convexa (super-linear) de sua participação de
   mercado/atenção". É essa **convexidade** (o retorno super-linear) que distingue
   "concentração" de "anchor effect" e que explica por que uma única firma captura metade
   das menções enquanto detém bem menos da metade do mercado real. O draft *gesticula* na
   direção disso (superstar firms, Autor et al. 2020) mas nunca escreve a função nem deriva
   a predição que a função implica.

3. **Distinção entre o construto e seus vizinhos já batizados.** "Anchor entity" precisa
   se distinguir explicitamente de: *popularity bias* (Lehmann 2510.16815), *entity
   salience*, *Matthew effect*, *winner-take-most*, e — crucialmente — do conceito de
   marketing *category entry point* (Ehrenberg-Bass). Se "entidade-âncora" é apenas
   "popularity bias agregado por setor com um HHI", não é construto novo: é uma métrica
   nova de um fenômeno conhecido. **O delta tem que estar no nível de mercado/setor, não
   no nível de entidade** — e isso o draft não isola conceitualmente.

**Veredito 1:** como está, "Anchor-Entity Concentration" é um *rótulo evocativo para uma
estatística descritiva*. Vira construto se ganhar (i) definição operacional com limiar,
(ii) um mecanismo formal com retorno super-linear, (iii) demarcação dos vizinhos.

---

### Crítica 2 (b) — Risco de "já sabemos disso": qual é o delta sobre popularity bias?

Popularity bias em LLMs é literatura madura. O próprio draft cita Lehmann et al.
(2510.16815, "shortcut" por popularidade/ordem/coocorrência), Lichtenberg et al.
(2406.01285) e o produto-bias de investimento (2503.08750). Um revisor hostil escreve na
margem: *"You have rediscovered popularity bias and computed an HHI per sector. Where is
the theoretical contribution?"*

O risco é concreto porque o achado central — uma marca domina metade das menções de seu
setor — é **exatamente o que popularity bias prediz**. Se o paper parar em "medimos
popularity bias num mercado novo e por setor", é incremental: novo dataset, mesmo
fenômeno. A defesa do draft (corrente 7: "mercado não-anglófono") é uma defesa de
*ineditismo de amostra*, não de *contribuição teórica* — e revisores A1 (ICWSM/WWW)
punem isso como "dataset paper disfarçado de paper de teoria".

Há **três deltas teóricos potenciais** no material, mas nenhum está afiado:

- **Delta-1 (nível de agregação): popularity bias é de entidade; o achado é de setor.** A
  contribuição não é "Nubank é popular" — é "a *estrutura de concentração* de um setor
  prediz a *taxa média* de citação do setor inteiro, e essa relação é mediada por uma
  única entidade-âncora". Isto é uma afirmação sobre a **transmissão de um viés de entidade
  para um viés de categoria** — algo que popularity bias clássico (que é por-item) não
  formula. Mas o draft enterra isso na Tabela 3.5 ("a ordenação de concentração acompanha a
  ordenação de taxa") sem elevá-lo a tese.

- **Delta-2 (decomposição como método): o LOO como estimador do "componente superstar".** A
  inversão OR 4,13→0,77 sob leave-one-out é metodologicamente bonita e **não trivial**:
  mostra que um viés aparentemente setorial é, sob decomposição, um viés de item que se
  disfarça de propriedade de categoria. Isto é um *aviso de validade de construto para toda
  a literatura de "viés setorial"* — qualquer claim de "setor X é favorecido" pode ser um
  artefato de uma âncora. Esse é um delta real e citável, mas o draft o trata como
  "robustez" (§7.2.4), não como contribuição.

- **Delta-3 (heterogeneidade por engine refuta a sistematicidade):** só 2/5 engines
  sustentam a direção. Isto contradiz a moldura de "viés sistemático" da corrente GEO e é
  um achado negativo informativo. Mas, de novo, está no red team, não na contribuição.

**Veredito 2:** o delta existe (transmissão entidade→categoria; LOO como diagnóstico de
construto; heterogeneidade refutando sistematicidade), mas o draft o esconde sob "robustez"
e "ressalvas". O paper corre risco real de "já sabemos disso" enquanto não promover esses
três pontos à tese e ancorá-los em uma teoria formal de transmissão.

---

### Crítica 3 (c) — A ponte fintech→GEO está fundamentada ou é anedótica?

A camada A do `mecanismos.md` (oferta de corpus: imprensa setorial, Reclame Aqui, SEO
nativo digital, docs do BC/Pix) é **a parte mais fraca do paper teoricamente**, porque é
inteiramente narrativa post-hoc e o próprio draft admite (§8.2, "causal não medido"):
nenhuma medida de tamanho de corpus, volume de notícias ou volume de busca foi cruzada com
a taxa. Um revisor hostil chama isso de **just-so story**: depois de ver fintech alta,
inventa-se uma cadeia plausível de razões pelas quais fintech "deveria" ser alta. Toda
vertical perdedora também tem uma história plausível (saúde = YMYL; tecnologia =
fragmentação) — e histórias que explicam qualquer resultado não explicam nenhum.

Pior: a própria camada A é **parcialmente refutada pelos dados do próprio paper** e o draft
admite honestamente (P-A1: varejo 92,9% > fintech 86,5% no RAG; P-A2: o gap é *maior* em
inglês, contra a tese PT-cêntrica). Quando o mecanismo proposto é falsificado pelas suas
próprias predições e mantido mesmo assim ("parcialmente refutado"), o revisor pergunta por
que ele continua no paper.

A ponte que **está** fundamentada é a outra — fintech→GEO via *estrutura de mercado* (C1,
marca-categoria) e *frequência paramétrica* (B1, Claude 51% sem ferramenta). O gap de 40 pp
paramétrico no Claude é a evidência mais forte e menos anedótica do paper inteiro: mostra
que a vantagem está *nos pesos*, não na recuperação. Mas o paper a embrulha junto com a
camada A frágil, e a média conjunta dilui o sinal limpo.

**Veredito 3:** a ponte fintech→GEO é **mista**. O elo B1/C1 (paramétrico + marca-categoria)
é defensável e tem evidência discriminante. O elo A (oferta de corpus PT-BR) é anedótico,
parcialmente autorrefutado, e deveria ser rebaixado a hipótese explicitamente não testada —
ou removido da linha de frente.

---

### Crítica 4 (d) — Busca de novidade: 2024–2026 já matou a contribuição? (6+ buscas)

Realizei 9 buscas web em 11/jun/2026 e inspecionei o paper mais ameaçador via WebFetch.
Reporto o que encontrei, honestamente, incluindo o que enfraquece o nosso paper.

**Busca 1 — "anchor entity concentration LLM brand citation superstar firm 2025 2026".**
Resultado: dominado por literatura cinza de marketing/GEO (DigitalApplied, AirOps, 2PointAgency,
ALM Corp). Achado acadêmico tangencial: arXiv:2510.01286 ("Emergent evaluation hubs in a
decentralizing LLM ecosystem") descreve influência de benchmark com cauda pesada/concentrada
— é sobre concentração de *benchmarks*, não de marcas comerciais. **Não mata.** Confirma que
"anchor entity" como construto acadêmico **não existe** — só aparece como jargão de SEO
("schema markup qualifies a brand entity as the right anchor").

**Busca 2 — "brand dominance AI search share of model winner-take-all 2026".**
Resultado: inteiramente industrial (Contently, Stacker, Yotpo). Achado importante e
**desfavorável a uma das nossas molduras**: várias fontes argumentam que AI search é *long
tail, não winner-take-all* — "even the most-cited domain rarely exceeds 5% of total citations".
Isto contradiz superficialmente o nosso HHI alto. **Não mata** (eles medem concentração de
*domínios-fonte*; nós medimos concentração de *entidades nomeadas por setor* — unidades
diferentes), mas obriga o paper a demarcar essa diferença explicitamente, senão um revisor
usa essas fontes contra nós.

**Busca 3 — "popularity bias entity salience LLM citation concentration Herfindahl".**
Resultado: o mais perigoso. Surgiu **arXiv:2512.09483** (Zhang, Ye, Peng, Garimella, Tyson,
10/dez/2025, "Source Coverage and Citation Bias in LLM-based vs. Traditional Search Engines"),
e confirmou-se que Herfindahl/Gini **já são aplicados** à concentração de citação em LLM, e
que "fewer than ten distinct URLs appear in 80% of responses" — concentração mais apertada
que busca tradicional. Também reapareceu Lehmann (2510.16815) e a tese de popularity bias.

**Busca 4 — WebFetch de arXiv:2512.09483 (verificação direta do abstract).**
Confirmado: estuda **domínios-fonte**, não menções espontâneas de entidades comerciais; **não
é setorial/vertical**; **não é longitudinal** (corte transversal); **não menciona mercado
não-anglófono**; e o abstract **não usa HHI nem Gini** (a métrica de concentração veio de
literatura secundária sobre o paper, não do abstract). 55.936 queries, 6 LLM-SEs + 2 TSEs.
**Não mata** — é o vizinho mais próximo em "concentração de citação", mas em unidade de
análise (domínio, não marca comercial), recorte (sem setor, sem mercado emergente) e desenho
(sem longitudinal) **distintos**. É de citação obrigatória e deve ser o principal contraste
da seção 2.

**Busca 5 — "category entry points / distinctive brand assets LLM AI search Ehrenberg-Bass 2026".**
Resultado: confirma o framework Ehrenberg-Bass (CEPs, DBAs, mental availability; Romaniuk &
Sharp) como literatura viva e madura, **mas nenhum paper acadêmico que o cruze com citação de
LLM**. **Gap de enquadramento confirmado** (ver Crítica 5): o draft não usa Ehrenberg-Bass e
deveria — "marca-categoria" (C1) é, essencialmente, mental availability máxima + um DBA verbal
único ("Nubank" = banco digital), e existe vocabulário consagrado para isso que o paper ignora.

**Busca 6 — "sector vertical bias spontaneous brand mention LLM citation finance healthcare retail".**
Resultado: dominado por relatórios de indústria (Search Atlas 5,17 mi domínios; Writesonic;
Omniscient 23 mil citações; Goodie). Achado **convergente e desfavorável à novidade do
ranking bruto**: a indústria já reporta "Financial Services consistently shows higher citations
(13-23%), Technology/Consumer Goods lower (5-6%)" — ou seja, **o ranking fintech>tecnologia já é
folclore de mercado**. Mas: tudo é literatura cinza, sem teste estatístico, sem decomposição de
âncora, sem longitudinal, sem mercado emergente, sem peer review. **Não mata** o paper
acadêmico, mas **mata definitivamente** qualquer claim de que "fintech cita mais" seja a
novidade. Reforça que a novidade tem que ser a *decomposição* e o *mecanismo*, nunca o ranking.

**Busca 7 — "Matthew effect rich-get-richer LLM training data entity frequency citation 2025 2026".**
Resultado: confirma o Matthew effect como moldura ativa em IA — arXiv:2509.23261 ("Matthew
Effect of AI Programming Assistants": loop popular-framework→mais-geração→mais-adoção→mais-corpus)
e LSE Impact (mai/2026, "Matthew effect in AI summary"; LLMs "preferentially retrieve highly
cited works"). **Achado de oportunidade, não ameaça:** o Matthew effect é a teoria de feedback
que o nosso paper precisa para explicar a *convexidade* da Crítica 1 — e o draft não o cita.

**Busca 8 — "longitudinal multi-LLM brand visibility audit emerging market Portuguese Brazil sector".**
Resultado: nada acadêmico que case com o nosso recorte. Só guias de indústria e um paper de
NER clínico em PT-BR (anonimização de prontuário, não marcas). **Confirma a lacuna (vi) do draft**:
o desenho longitudinal × multi-LLM × multi-setor × mercado emergente, sobre entidades comerciais,
**não tem par publicado** que a busca encontre.

**Busca 9 — "share of model / share of voice generative engine brand single firm dominance arxiv 2026".**
Resultado: "Share of Model" e "Share of Voice" são termos **exclusivamente de marketing/indústria**
(Senso, LLMPulse, Yotpo, AuthorityTech, Waikay; "SoM is replacing SoV as the primary KPI"). MR
Research "State of Machine Relations Q1 2026" diz "citation is already highly concentrated /
winner-take-most". **Implicação dupla:** (a) usar "share of model" como contribuição teórica é
**arriscado** porque já é jargão comercial não-acadêmico — um revisor pode achar pop; (b) ao
mesmo tempo, **não há formalização acadêmica** do conceito, então há espaço para ser o primeiro
a formalizá-lo — desde que o paper o trate como construto medido, não como buzzword adotado.

**Veredito 4 — síntese de novidade.** Nenhum trabalho de 2024–2026 mata a contribuição, mas o
cerco apertou e o paper precisa reposicionar:
- "Anchor entity" como construto acadêmico: **inédito** (só existe como jargão de SEO). Espaço aberto.
- HHI/Gini de concentração de citação: **já feito** (2512.09483 e secundária) — mas para *domínios*,
  não *marcas por setor*. Demarcar.
- Ranking setorial fintech>tech: **folclore de indústria já estabelecido** — não pode ser a novidade.
- "Share of model": **buzzword industrial** sem formalização — formalizar é oportunidade, adotar
  ingenuamente é risco.
- Longitudinal × multi-setor × mercado emergente × entidade comercial: **lacuna real e sustentável**.

---

### Crítica 5 (e) — Gaps de enquadramento: literaturas que o draft deveria usar e não usa

O draft tem 8 correntes, mas todas são de *ciência da computação / NLP / IR*. Faltam três
corpora teóricos que **explicariam o mecanismo** em vez de só medi-lo. A ausência delas é o
que faz o paper parecer descritivo.

**Gap-1 — Ehrenberg-Bass (mental availability, Category Entry Points, Distinctive Brand Assets).**
A camada C1 ("marca-categoria: Nubank ≈ banco digital") está **reinventando, sem citar, a teoria
de mental availability de Romaniuk & Sharp**. "Ser a resposta canônica de uma palavra para uma
classe de perguntas" é a definição operacional de mental availability medida por *Category Entry
Points*. E "Nubank" sendo recuperável como string única e limpa é um *Distinctive Brand Asset*
verbal. Usar esse vocabulário (i) dá ao construto "anchor entity" uma fundação teórica de 20+
anos de ciência de marca, e (ii) gera uma predição nova: **a entidade-âncora de um setor é a que
maximiza CEPs × DBA verbal único** — testável cruzando saliência de marca (surveys de marca BR)
com taxa de citação. O draft não tem nenhuma referência de marketing científico. Isso é um buraco.

**Gap-2 — Mercados digitais winner-take-all / superstar firms (além de Autor 2020).** O draft cita
Autor et al. (2020) uma vez, de passagem. Falta a literatura de **economia de mercados de
plataforma e network effects** (winner-take-most em mercados digitais) que dá o *mecanismo de
geração* da concentração que depois aparece no corpus. A cadeia teórica correta é:
network effects no mercado real → dominância de mercado da firma → dominância de
*share-of-voice* na mídia/web → dominância de frequência no corpus de treino → dominância de
probabilidade paramétrica → dominância de citação. O paper só observa a última seta; precisa
nomear a primeira. (Nuance da Busca 2: a literatura de indústria diz que AI search *como um todo*
é long-tail; a reconciliação é que a cauda longa vale para *domínios-fonte*, enquanto a *atenção
a marcas dentro de uma categoria nomeável* é winner-take-most — exatamente o que o HHI por setor
mostra.)

**Gap-3 — Matthew effect / cumulative advantage (Merton; Price; DiPrete & Eirich 2006).** É a
teoria sociológica do "rich-get-richer" que formaliza a **convexidade** pedida na Crítica 1. O
Matthew effect prediz retorno super-linear da vantagem acumulada — exatamente por que uma firma
com, digamos, 30% de market share captura ~50% das menções. A Busca 7 confirma que essa moldura já
está sendo aplicada a LLMs (programming assistants, retrieval de papers). Citá-la transforma a
"entidade-âncora" de descrição em *instância de um efeito cumulativo conhecido aplicado a um novo
substrato (atenção paramétrica de LLM)* — o que é uma contribuição teórica legítima e modesta.

**Gap-4 (menor) — viés de concentração de fonte já formalizado (2512.09483).** Não é gap de
moldura mas de *related work obrigatório*: o vizinho mais próximo em concentração de citação não
está citado porque é de dez/2025 e provavelmente pós-data do `literatura.md`. Tem que entrar.

**Veredito 5:** o enquadramento é monodisciplinar (CS/NLP) e por isso descritivo. Três corpora
teóricos (ciência de marca Ehrenberg-Bass; economia winner-take-all; Matthew effect/cumulative
advantage) estão ausentes e são exatamente os que converteriam a descrição em mecanismo. Mais um
paper de related work obrigatório (2512.09483).

---

## FASE 2 — RESPOSTAS COMPLEMENTARES ROBUSTAS

Para cada crítica, o argumento teórico reforçado, as referências verificadas e o parágrafo de
"related work delta" pronto para colar no manuscrito.

### Resposta 1 — De rótulo a construto: definição formal de Anchor-Entity Concentration

**Argumento reforçado.** Promover "entidade-âncora" a construto exige separar três objetos que o
draft funde: a *entidade-âncora* (o item), a *concentração de âncora* (a propriedade do setor) e o
*efeito-âncora* (a transmissão do item para a taxa do setor). Proponho a formalização abaixo, que
torna o construto falsificável e gera predições.

Seja, num setor (vertical) *v*, a participação de menções da entidade *e* dada por
*s(e,v) = menções(e,v) / menções(v)*. Defina:

- **Entidade-âncora** de *v*: a entidade *e\** = argmax *s(e,v)* **se e somente se** *s(e\*,v)* ≥ τ
  (limiar; sugiro τ = 0,40, pré-registrado) **e** o gap para a segunda colocada
  *s(e\*,v) − s(e₂,v)* ≥ δ (sugiro δ = 0,15). Isto resolve a circularidade da Crítica 1: varejo
  (Mercado Livre 29,5%, abaixo de τ, com Magalu colado) **não tem âncora** — é bi-líder; fintech
  (Nubank 49,68%, gap enorme) **tem**. O construto passa a ser falsificável e discreto.
- **Concentração de âncora** de *v*: o par (HHI*ᵥ*, *s(e\*,v)*). Não é só o HHI — é o HHI
  *atribuível a uma única entidade*, o que distingue "concentrado em torno de um" (fintech) de
  "concentrado em torno de poucos" (varejo).
- **Efeito-âncora** (a quantidade-tese): a diferença entre a taxa de citação observada do setor e a
  taxa contrafactual sob leave-one-out da âncora, *Δᵥ = taxa(v) − taxa_LOO(v)*. Para fintech,
  Δ = 28,15 − 11,46 = **16,69 pp**. Esta é a operacionalização limpa do "componente superstar".

**Mecanismo formal (a peça que faltava).** Postule que a probabilidade de citação espontânea de uma
entidade é uma transformação **convexa** de sua frequência relativa no corpus, que por sua vez é
uma transformação **convexa** (cumulative-advantage) de sua participação de mercado real:

```
P(citar e | v) ≈ g( f(e) ),   f(e) ∝ m(e)^γ  com γ > 1   (Matthew/cumulative advantage)
g convexa e saturante (logística nos pesos paramétricos)
```

A predição-chave que distingue *anchor effect* de mera *concentração*: como γ > 1, a participação
de citação *s(e\*,v)* deve ser **estritamente maior** que a participação de mercado real da firma
*e\** — sobre-representação super-linear. Esse é o teste que separa o construto de "popularity bias
genérico" e que pode ser confrontado com dados de market share reais (Nubank market share BR vs.
49,68% de share-of-citation).

**Predições do construto (falsificáveis):**
1. *Δᵥ* > 0 e cresce com *s(e\*,v)* entre setores (mais âncora → mais efeito-âncora).
2. *s(e\*,v)* > market-share real de *e\** (sobre-representação convexa).
3. O efeito-âncora é maior em engines paramétricos puros (onde γ atua nos pesos) que em RAG (onde a
   recuperação ao vivo reamostra a cauda) — consistente com Claude (efeito forte) vs Perplexity
   (gap comprimido) no próprio dado.
4. Setores sem âncora (varejo) têm *Δ* pequeno e LOO de qualquer líder não inverte o ranking — a
   robustez do LOO-para-todas-as-verticais (§7.2.4) **testa diretamente isto**.

**Referências adicionais verificadas:**
- DiPrete, T. A., & Eirich, G. M. (2006). "Cumulative Advantage as a Mechanism for Inequality: A
  Review of Theoretical and Empirical Developments." *Annual Review of Sociology*, 32, 271–297.
  DOI 10.1146/annurev.soc.32.061604.123127. (Formaliza o γ > 1.)
- Merton, R. K. (1968). "The Matthew Effect in Science." *Science*, 159(3810), 56–63.
  DOI 10.1126/science.159.3810.56. (Verificado via Busca 7 / NCBI / ScienceDirect como base canônica.)
- Autor, Dorn, Katz, Patterson, Van Reenen (2020). "The Fall of the Labor Share and the Rise of
  Superstar Firms." *Quarterly Journal of Economics*, 135(2), 645–709. DOI 10.1093/qje/qjaa004.
  (Já no draft; promover de nota de rodapé a alicerce.)

### Resposta 2 — O delta sobre popularity bias: transmissão entidade→categoria + LOO como diagnóstico

**Argumento reforçado.** A resposta ao "já sabemos disso" é precisar a *unidade de novidade*.
Popularity bias é um fenômeno **por-item** (entidades populares são favorecidas). A nossa
contribuição é **por-categoria**: documentamos e medimos a *transmissão* de um viés por-item para
uma aparente propriedade de categoria — e damos o estimador que a desmonta (Δᵥ, o efeito-âncora via
LOO). A frase-tese para o abstract: *"viés de popularidade por entidade, quando uma categoria gera
uma única firma superstar, manifesta-se como um pseudo-viés setorial; mostramos como decompô-lo e
quantificá-lo."* Isto é novo em relação a Lehmann (que para no nível do item/comparação de pares) e
a 2512.09483 (que mede concentração de domínio sem decompô-la por entidade-âncora setorial).

O segundo delta é metodológico e transferível: **o LOO de âncora como teste de validade de construto
para toda a literatura de "viés setorial"**. Qualquer claim futura de "LLMs favorecem o setor X"
deve passar pelo LOO da entidade modal do setor — caso contrário pode estar medindo uma firma, não
um setor. Esse é um contributo de método citável independentemente do nosso resultado.

**Referências adicionais verificadas:**
- Lehmann, Lee, Schockaert, Wermter (2510.16815, EACL 2026) — já no draft; é o âncora de
  popularity bias por-item contra o qual contrastamos o delta por-categoria.
- Zhang, Ye, Peng, Garimella, Tyson (2512.09483, 10/dez/2025), "Source Coverage and Citation Bias
  in LLM-based vs. Traditional Search Engines" — **verificado por WebFetch**; concentração de
  *domínios-fonte* (6 LLM-SEs, 55.936 queries), não de marcas por setor, não setorial, não
  longitudinal. Contraste obrigatório.

**Parágrafo "related work delta" (pronto, EN):**

> *Prior work on popularity bias in LLMs operates at the item level: popular entities are favored
> when models compare or recommend (Lehmann et al., 2026; Lichtenberg et al., 2024), and recent
> audits show that citation of source domains is more concentrated in LLM search engines than in
> traditional ones (Zhang et al., 2025). We depart from both along two axes. First, our unit of
> concern is the **category**, not the item or the domain: we show that an item-level popularity
> bias, when a category has produced a single superstar firm, surfaces as an apparent **sectoral**
> citation advantage, and we provide a leave-one-out estimator of the anchor effect (Δᵥ) that
> separates the two. Second, we treat the anchor decomposition as a **construct-validity test for
> the broader "sectoral bias" literature**: any claim that LLMs favor sector X should survive
> removal of the sector's modal entity, lest it measure a firm rather than a sector.*

### Resposta 3 — Disciplinar a ponte fintech→GEO: rebaixar a camada A, blindar B1/C1

**Argumento reforçado.** A defesa contra "just-so story" é metodológica: **declarar a camada A como
hipótese explicitamente não testada** (porque nenhuma medida de corpus foi cruzada) e mover o peso
da contribuição mecanística para o que *tem* assinatura discriminante — o gap de 40 pp paramétrico
no Claude (B1) e a concentração HHI/posição-uniforme (C1). A honestidade vira força: o paper afirma
"não medimos volume de corpus, portanto não atribuímos causalidade à oferta; o que medimos é que a
vantagem persiste em modo paramétrico puro, o que *exclui* uma explicação puramente RAG/recuperação
e *localiza* o efeito nos pesos." Predições refutadas (P-A1, P-A2) devem ser reportadas como
**refutações**, não como "parcialmente confirmadas" — um paper que reporta predições próprias
falhando ganha credibilidade de revisor, não perde.

O elo fintech→GEO defensável é então: **frequência paramétrica (B1) × marca-categoria/mental
availability (C1)**, com a camada A reposicionada como mecanismo candidato a montante, a ser testado
em trabalho futuro pelo cruzamento com share-of-voice de mídia.

**Referências adicionais verificadas:**
- Sun et al. (2410.00857) — já no draft; sustenta que sob RAG o modelo se apoia no contexto
  recuperado (por isso o gap comprime em Perplexity), reforçando que o efeito paramétrico do Claude
  é o sinal "puro" de B1.
- Romaniuk & Sharp (mental availability / CEPs) — ver Resposta 5; dá a C1 fundação testável.

### Resposta 4 — Reposicionamento de novidade após a busca

**Argumento reforçado.** A novidade defensável, depois das 9 buscas, é a **interseção**, não
nenhuma dimensão isolada. Reescrever os contribution claims assim:
1. **Não** "fintech cita mais" (folclore de indústria — Busca 6) — isso vira *motivação*, não contribuição.
2. **Sim** o construto formal *anchor entity / anchor effect* com definição falsificável e estimador
   LOO (inédito academicamente — Buscas 1, 9).
3. **Sim** a demarcação contra concentração-de-domínio (2512.09483): concentração de **marca por
   categoria** ≠ concentração de **domínio-fonte**; e a reconciliação com o "AI search é long-tail"
   da indústria (long-tail de domínios coexiste com winner-take-most de marcas dentro de categoria
   nomeável).
4. **Sim** o recorte longitudinal × multi-LLM × multi-setor × mercado emergente sobre entidades
   comerciais (lacuna sustentável — Busca 8).

**Parágrafo "related work delta" sobre a literatura de indústria (pronto, EN):**

> *A growing body of industry analyses reports that financial-services content is cited more often
> than technology or consumer-goods content (e.g., vendor studies of millions of AI citations), and
> popularizes "share of model" as the AI-era successor to share of voice. We treat these as
> motivation rather than evidence: they lack statistical testing, entity-level decomposition,
> longitudinal design, and peer review, and they conflate source-domain concentration — which is
> long-tailed (Zhang et al., 2025) — with within-category brand concentration, which we show is
> winner-take-most. Our contribution is to formalize the latter as a measurable construct (anchor
> entity / anchor effect) and to test it across engines and over time.*

### Resposta 5 — Fechar os gaps de enquadramento: três corpora teóricos

**Argumento reforçado.** Incorporar as três literaturas converte cada camada do `mecanismos.md` de
narrativa em teoria fundamentada:

- **C1 (marca-categoria) ← Ehrenberg-Bass.** Reescrever C1 em termos de **mental availability**: a
  entidade-âncora é a marca com maior probabilidade de ser evocada através do maior número de
  *Category Entry Points*, recuperável por um *Distinctive Brand Asset* verbal único e limpo
  ("Nubank"). Predição nova e testável: a âncora de citação de um setor correlaciona com sua mental
  availability medida por survey de marca — uma ponte entre ciência de marca e GEO que **nenhum
  paper acadêmico fez** (Busca 5). Referências: Romaniuk, J., & Sharp, B. (2022), *How Brands Grow
  Part 2*, Oxford University Press (rev. ed.); Sharp, B. (2010), *How Brands Grow*, Oxford. (CEP/DBA
  são desse corpus; verificado como framework vivo via Ehrenberg-Bass Institute, Busca 5.)
- **Concentração ← economia winner-take-all/superstar.** Adicionar a cadeia network-effects →
  market dominance → corpus dominance → parametric dominance. Referência: Autor et al. (2020, já
  citado); e para network effects digitais, opcionalmente um clássico de platform economics como
  base do "winner-take-most" no mercado real (a montante do corpus).
- **Convexidade ← Matthew effect / cumulative advantage.** Merton (1968) e DiPrete & Eirich (2006)
  formalizam γ > 1 da Resposta 1. A Busca 7 confirma aplicação corrente a LLMs (arXiv:2509.23261,
  "The Matthew Effect of AI Programming Assistants"; LSE Impact mai/2026). Referência adicional
  verificada: arXiv:2509.23261 — útil como precedente de "Matthew effect aplicado a substrato LLM".

**Parágrafo "related work delta" interdisciplinar (pronto, EN):**

> *We bridge three literatures absent from prior GEO and LLM-bias work. From marketing science, the
> Ehrenberg-Bass account of **mental availability** — brands evoked across many Category Entry
> Points and retrieved via Distinctive Brand Assets (Sharp, 2010; Romaniuk & Sharp, 2022) — gives a
> falsifiable reading of why a single brand becomes the category's anchor: it predicts that
> within-category citation share tracks survey-measured mental availability. From economics, the
> theory of **superstar firms** (Autor et al., 2020) and digital winner-take-most dynamics supplies
> the upstream mechanism by which market concentration becomes corpus concentration. From sociology,
> **cumulative advantage / the Matthew effect** (Merton, 1968; DiPrete & Eirich, 2006), recently
> applied to LLM substrates (e.g., AI programming assistants, 2025), formalizes the convex,
> super-linear mapping from market share to citation share that distinguishes an anchor effect from
> mere concentration. The anchor entity is thus not a new phenomenon in isolation but the
> projection of cumulative advantage onto the parametric attention of LLMs — a contribution that
> ports an established mechanism to a new substrate and measures it.*

---

## Formulação teórica final recomendada

**Nome do construto.** *Anchor-Entity Effect* (efeito-entidade-âncora) — manter como nome de capa,
mas **subordinar "share of model"** a "within-category citation share" no corpo (share-of-model fica
como sinônimo informal/ponte com a indústria, nunca como termo técnico primário, por ser buzzword
não-acadêmico — Busca 9).

**Definição formal.** Num setor *v*, com *s(e,v)* = participação de menções da entidade *e*:
a *entidade-âncora* *e\** existe sse *s(e\*,v) ≥ τ* e *s(e\*,v) − s(e₂,v) ≥ δ* (τ, δ pré-registrados);
a *concentração de âncora* é o par (HHIᵥ, *s(e\*,v)*); o *efeito-âncora* é
*Δᵥ = taxa(v) − taxa_LOO-âncora(v)*. O construto afirma que parte substancial de uma vantagem de
citação aparentemente setorial é *Δᵥ* — atribuível a uma única firma superstar — e que essa
atribuição é gerada por vantagem cumulativa (γ > 1) convertida em probabilidade paramétrica.

**Predições (falsificáveis, ordenadas por força do teste no dataset atual).**
1. **P1 (inversão sob LOO):** remover a âncora inverte o ranking do setor — *confirmado*
   (28,15→11,46%; OR 4,13→0,77).
2. **P2 (sobre-representação convexa):** *s(e\*,v)* > market share real de *e\** — *testável* com
   dados de mercado BR (não feito; teste decisivo de γ > 1).
3. **P3 (gradiente engine):** efeito-âncora maior em paramétrico que em RAG — *suportado* (Claude
   forte vs Perplexity comprimido).
4. **P4 (especificidade da âncora):** setores sem âncora (varejo, τ não atingido) não invertem sob
   LOO de qualquer líder — *testável* via LOO-para-todas-as-verticais (§7.2.4); é o controle
   negativo que blinda contra "todo setor desmorona sob LOO".
5. **P5 (mental availability):** *s(e\*,v)* correlaciona com mental availability de marca medida por
   survey — *ponte Ehrenberg-Bass*, trabalho futuro, mas é a predição que mais eleva o paper de
   medição a teoria.

**Posição editorial final.** Aceitar com major revision condicionada a: (i) formalizar o construto
com τ/δ e a função convexa; (ii) reescrever contribution claims tirando o ranking bruto da frente e
pondo o efeito-âncora + LOO-diagnóstico; (iii) inserir as três literaturas (Ehrenberg-Bass,
superstar/winner-take-all, Matthew/cumulative advantage) e o related work obrigatório 2512.09483;
(iv) rebaixar a camada A a hipótese não testada e reportar P-A1/P-A2 como refutações; (v) confirmar
abstract/autoria das entradas [A VERIFICAR] do `literatura.md` antes da submissão.

---

*Fim do Peer Review R2 (teoria). Buscas web e WebFetch realizados em 11/jun/2026. As referências
novas (DiPrete & Eirich 2006; Merton 1968; Autor et al. 2020; Sharp 2010; Romaniuk & Sharp 2022;
Zhang et al. 2512.09483; arXiv:2509.23261) foram verificadas por busca direta; os DOIs de Merton,
DiPrete & Eirich e Autor et al. são clássicos estáveis e devem ser reconfirmados no BibTeX final.*
