================================================================================
RELATÓRIO FINAL DA REVISÃO POR PARES SIMULADA
+ CONTEÚDO COMPLEMENTAR PARA PUBLICAÇÃO
================================================================================

Manuscrito: "Anchor-Entity Concentration in LLM Brand Citations"
Projeto: Papers (github.com/alexandrebrt14-sys/papers)
Consolidação: editor científico chefe, 11 de junho de 2026
Fontes: peer_review_R1_metodos.md, peer_review_R2_teoria.md,
        peer_review_R3_editorial.md, board externo de 5 LLMs (pr_wave_1..5),
        DRAFT_INSUMOS_FINTECH_CITATION_ADVANTAGE.md

Regra editorial deste documento: números somente dos arquivos de insumo e das
análises rodadas pelos revisores sobre o papers.db; dado verificado vence
opinião; honestidade total; nenhum número inventado.

--------------------------------------------------------------------------------
ÍNDICE
--------------------------------------------------------------------------------
PARTE I   — CRÍTICAS E GAPS (consolidado dos 3 revisores + board)
   1.  Veredito agregado da banca e a frase-tese canônica
   2.  Críticas consolidadas, deduplicadas e priorizadas (FATAL/MAJOR/MINOR)

PARTE II  — RESPOSTAS COMPLEMENTARES ROBUSTAS (resposta dos autores)
   3.  Resposta a cada crítica FATAL/MAJOR com os números reais
   4.  O construto formal do R2 (Anchor-Entity Effect) e as 5 predições
   5.  Reformulação da tese: de "superstar única" para "núcleo de âncoras top-k"
   6.  Os 3 parágrafos de "related work delta" (EN) e o contraste com 2512.09483

PARTE III — POR QUE A VERTICAL FINTECH TEM MAIS CITAÇÕES EM GEO
   7.  Explicação em camadas reconciliando tudo + lições de GEO

PARTE IV  — PACOTE DE PUBLICAÇÃO ATUALIZADO
   8.  Abstract EN revisado, cover letter, 6 figuras, checklist, cronograma

================================================================================
PARTE I — CRÍTICAS E GAPS
================================================================================

--------------------------------------------------------------------------------
1. VEREDITO AGREGADO DA BANCA E A FRASE-TESE CANÔNICA
--------------------------------------------------------------------------------

Veredito unânime dos três revisores: MAJOR REVISION.

  - R1 (métodos e estatística): major revision. A espinha dorsal — efeito de
    entidade-âncora + heterogeneidade por engine — é publicável em ICWSM/WWW
    após seis exigências (re-coleta íntegra incluindo as 48 queries do
    Perplexity; GLMM cluster-robusto com desfecho duplo; jackknife top-k por
    vertical com IC sobre os drops; reframe de "superstar única" para "núcleo
    de âncoras"; série temporal do share da âncora; correção da narrativa de
    front-loading pelos offsets reais).

  - R2 (teoria, literatura e contribuição): major revision. "A contribuição
    empírica é real e o dataset é diferenciado, mas o manuscrito descreve um
    fenômeno sem construí-lo como teoria, e subexplora correntes de literatura
    que decidem a novidade. Não é rejeição: é um paper a uma camada teórica de
    distância de ser defensável."

  - R3 (editor de venue, ICWSM/WWW): major revision rumo à submissão, com a
    Semana 1 do roadmap (re-coleta sem truncamento + auditoria de decoys +
    decisão sobre Gemini) como pré-condição inegociável. A versão "vantagem
    setorial sistemática de fintech" seria desk-rejected; a versão "concentração
    de entidade-âncora + heterogeneidade por engine + lições de medição" é
    defensável após resolver os três bloqueadores de medição e a inferência
    com clustering.

  - Board externo de 5 LLMs (waves 1 a 5; Gemini caiu por HTTP 429 em todas as
    ondas, Perplexity/gpt-5.5 majoritariamente sem corpo renderizado, Opus
    truncado em ~2.000 tokens). O sinal substantivo é convergente: a onda 1
    (revisores ICWSM/WWW) abriu por major revision e tratou o leave-one-out
    como gate obrigatório; a onda 3 (economistas) construiu a explicação em
    camadas do efeito-âncora; a onda 2 fundamentou o reframe do truncamento
    como "saliência primária de marca" (primazia / serial position, Murdock
    1962; Glanzer & Cunitz); a onda 4 propôs o dual-track de re-coleta; a onda 5
    entregou o pacote de figuras. Nenhuma contribuição do board contradiz os
    três revisores formais; todas reforçam.

A FRASE-TESE CANÔNICA do paper (a espinha dorsal de abertura, abstract e
conclusão, na formulação do R3):

  "A aparente vantagem setorial da fintech na citação espontânea por LLMs não é
   um efeito da vertical, mas a sombra de uma única entidade-âncora (Nubank):
   removê-la derruba a fintech de primeiro para último lugar (28,15% para
   11,46%) e inverte a razão de chances ajustada (4,13 para 0,77), revelando que
   'vantagens setoriais' em visibilidade de LLM são, em larga medida,
   concentração de marca em nível de superstar, modulada pelo motor."

Tudo no manuscrito que não serve a essa frase deve virar apêndice ou ser
cortado. A pergunta original ("por que a fintech é mais citada?") é o gancho,
não a tese.

--------------------------------------------------------------------------------
2. CRÍTICAS CONSOLIDADAS, DEDUPLICADAS E PRIORIZADAS
--------------------------------------------------------------------------------

As críticas dos três revisores e do board foram unificadas e deduplicadas.
Onde dois revisores apontam o mesmo ponto, a fonte é creditada de forma
combinada. Prioridade: FATAL (bloqueia submissão) > MAJOR (bloqueia aceitação)
> MINOR (corrigir antes de câmera-pronta).

............................. CRÍTICAS FATAIS .............................

C1 [FATAL] — Construto medido sobre texto truncado a 200 caracteres.
   (Fonte: R3-b1; draft §2.4 bloqueador nº 1; board wave_2/wave_4)
   O response_text foi persistido cortado em exatamente 200 chars em 4 dos 5
   engines (ChatGPT, Claude, Gemini: 100% das linhas; só Perplexity íntegro). O
   NER mede front-loading na abertura, não citação plena. Se um revisor de
   measurement perceber — e perceberá — o paper é rejeitado sem discussão de
   mérito. Não submeter antes de re-coletar com texto íntegro.

C2 [FATAL] — Inferência sem clustering com p-values absurdos.
   (Fonte: R3-b2; R1-M1; draft §7 bloqueador nº 5)
   Os qui-quadrados e IC tratam ~293 repetições por query como i.i.d. O n
   efetivo é da ordem de ~240 clusters (48 queries x 5 engines), não 50.453.
   p<10^-170 sobre ~240 clusters é sinal vermelho de não-independência ignorada;
   um editor de WWW measurement track devolve na triagem.

C3 [FATAL] — FPR de decoys de 96,9 a 98,6% sem explicação definitiva.
   (Fonte: R3-b3; draft §8 bloqueador nº 4)
   O instrumento "encontra" marcas fictícias em ~98% dos casos. Se a
   especificidade do detector é quase nula, a validade de construto da medida
   `cited` inteira fica sob suspeita. O insumo admite não saber se é por design
   (decoy plantado no prompt) ou bug — isso é inadmissível em submissão. Exige
   uma frase definitiva no manuscrito.

C4 [FATAL] — Mistura de RAG e paramétrico como número-título.
   (Fonte: R3-b4; draft §3.11; R1 veredito)
   Os 28,15% do título misturam Perplexity (RAG, satura em 86 a 93%) com modelos
   paramétricos. É incoerência de construto. Corrigível por reframing e
   estratificação: sem Perplexity, fintech = 20,80%.

(Observação: C1, C2 e C3 são bloqueio absoluto pré-submissão; C4 é corrigível
 por reframing. Todos os quatro são da Semana 1/2 do roadmap.)

............................ CRÍTICAS MAJOR .............................

C5 [MAJOR] — O gap bruto fintech-varejo MORRE sob inferência em nível de
   cluster (descoberta nova do R1).
   (Fonte: R1-M1 + R1-R-M1, executado no banco)
   O draft afirma que o gap de 3,2 pp "provavelmente perderia significância" mas
   nunca roda o teste, e segue apresentando o gap como achado positivo (Tabela
   3.1, chi2=33,6, p=6,8x10^-9). O R1 executou o teste de Welch entre as médias
   por-cluster: fintech 26,51% vs varejo 23,30%, com desvio entre clusters de
   ~24 pp; Welch t = 0,645 (df aprox. 94), NÃO significativo. A claim "fintech
   tem a maior taxa" deve ser rebaixada de "estatisticamente detectada" para
   "numericamente observada, não significativa sob clustering".

C6 [MAJOR] — O share do Nubank CRESCE dentro da janela (41% para 57%); o draft
   afirma erroneamente estabilidade (descoberta nova do R1).
   (Fonte: R1-M2 + R1-R-M2, executado no banco)
   A "robustez temporal" que o draft celebra (Tabela 3.9) é da TAXA da vertical,
   estável por acaso. O objeto da tese é a CONCENTRAÇÃO da âncora, e ela não é
   estável: o share do Nubank sobe de ~41% (W16 a W18) para ~53 a 59% (W19 a
   W23), aumento relativo de ~30% dentro da própria janela de medição. Um efeito
   de âncora crescente é ameaça de validade temporal (service drift) para a tese
   pivotada, medida na métrica errada pelo draft.

C7 [MAJOR] — O truncamento contamina o HHI e infla a própria concentração de
   49,7% (ameaça nova mais perigosa do R1).
   (Fonte: R1-M4 + R1-R-M4b, executado no banco)
   O draft tratou o truncamento só como ameaça à taxa absoluta, não à métrica
   de concentração. Mas dentro da fintech, as âncoras de cauda aparecem tarde —
   Itaú 402, PicPay 515, Banco Inter 838, BTG 906 chars — enquanto o Nubank
   aparece em offset médio 118 chars (dentro da janela de 200). O corte apaga
   justamente os rivais domésticos, exagerando a dominância do Nubank. A
   concentração de 49,7% (o número-título) é, ela própria, parcialmente artefato
   de truncamento, e deve ser declarada como limite SUPERIOR até a re-coleta.

C8 [MAJOR] — Varejo front-loada MAIS que fintech: a narrativa "fintech é
   premiada por front-loading do Nubank" é empiricamente falsa (descoberta nova
   do R1).
   (Fonte: R1-M4 + R1-R-M4, executado no banco)
   O draft (§2.4) asseriu, sem medir, que o truncamento premia verticais cuja
   marca-líder é citada cedo (fintech). O R1 mediu no Perplexity íntegro: offset
   médio da 1ª entidade é varejo 111,1 < fintech 123,1 < saúde 159,9 <
   tecnologia 173,3 chars. Varejo é mais front-loaded. O viés de truncamento é
   real, mas opera PENALIZANDO os rivais: se truncado, perde-se 51,6% das
   citações de tecnologia e 30,7% de saúde, contra ~20% de fintech/varejo. Logo
   o truncamento infla o gap fintech vs tecnologia/saúde, mas NÃO o gap fintech
   vs varejo. A direção alegada no draft está errada.

C9 [MAJOR] — A validação no Perplexity íntegro é SUB-POTENTE (descoberta nova
   do R1).
   (Fonte: R1-M5 + R1-R-M5, executado no banco)
   O draft trata o Perplexity como o caminho de validação limpa, mas ele foi
   coletado com apenas 24 queries distintas por vertical (12 PT + 12 EN), contra
   48 nos demais engines. A validação confirmatória limpa vive sobre ~24
   query-clusters por vertical, num único engine RAG — metade da diversidade de
   prompt do desenho — e confunde "citação limpa" com "comportamento de RAG". A
   re-coleta íntegra (bloqueador nº 1) precisa restaurar as 48 queries do
   Perplexity também, não só destruncar os outros quatro.

C10 [MAJOR] — "Anchor-Entity Concentration" é construto ou rótulo descritivo?
   (Fonte: R2-Crítica 1; board wave_1/Groq)
   O manuscrito nomeia o fenômeno mas não o define como construto. Falta (i)
   definição operacional independente do dado (hoje circular: a âncora é quem
   concentra, e a concentração é a participação dela); (ii) limiar (a partir de
   que share/HHI uma vertical "tem âncora"? varejo com dois líderes é bi-âncora
   ou sem âncora?); (iii) mecanismo causal formal com retorno super-linear; (iv)
   demarcação dos vizinhos batizados (popularity bias, entity salience, Matthew
   effect, category entry point). Como está, é rótulo evocativo para uma
   estatística descritiva.

C11 [MAJOR] — Risco de "já sabemos disso": qual o delta sobre popularity bias?
   (Fonte: R2-Crítica 2 e Crítica 4)
   O achado central — uma marca domina metade das menções do setor — é
   exatamente o que popularity bias prediz (Lehmann 2510.16815). Pior: a busca
   web do R2 mostrou que o ranking setorial fintech > tecnologia já é folclore de
   indústria (vendor studies: "Financial Services 13 a 23% de citações;
   Technology/Consumer Goods 5 a 6%"). E surgiu arXiv:2512.09483 (Zhang et al.,
   10/dez/2025), que aplica concentração de citação (HHI/Gini) em LLM — embora
   para DOMÍNIOS-fonte, não marcas por setor. A novidade NÃO pode ser o ranking
   bruto; tem que ser a decomposição e o mecanismo.

C12 [MAJOR] — A ponte fintech->GEO da Camada A é anedótica e parcialmente
   autorrefutada.
   (Fonte: R2-Crítica 3)
   A Camada A (oferta de corpus PT-BR: imprensa, Reclame Aqui, SEO, docs do BC)
   é narrativa post-hoc; nenhuma medida de tamanho de corpus foi cruzada com a
   taxa. É "just-so story": toda vertical perdedora também tem história
   plausível. Além disso, as próprias predições da Camada A falham (P-A1: varejo
   92,9% > fintech 86,5% no RAG; P-A2: o gap é maior em inglês, contra a tese
   PT-cêntrica). Camada A deve ser rebaixada a hipótese explicitamente não
   testada e P-A1/P-A2 reportadas como REFUTAÇÕES, não "parcialmente
   confirmadas". O elo defensável é B1 (gap de 40 pp paramétrico no Claude) x C1
   (marca-categoria).

C13 [MAJOR] — Enquadramento monodisciplinar (só CS/NLP); faltam três corpora
   teóricos que explicariam o mecanismo.
   (Fonte: R2-Crítica 5)
   As 8 correntes do draft são todas de CS/NLP/IR. Faltam: Ehrenberg-Bass
   (mental availability, Category Entry Points, Distinctive Brand Assets) que dá
   fundação teórica de 20+ anos à "marca-categoria"; economia winner-take-all /
   superstar firms (além da citação única a Autor et al. 2020) para o mecanismo
   de geração da concentração; e Matthew effect / cumulative advantage (Merton
   1968; DiPrete & Eirich 2006) para formalizar a convexidade. A ausência é o
   que faz o paper parecer descritivo.

C14 [MAJOR] — Heterogeneidade por engine refuta a "sistematicidade setorial".
   (Fonte: draft §3.11 bloqueador nº 3; R2-Crítica 2 Delta-3; R3-c)
   Só 2 de 5 engines (Claude, Gemini) colocam fintech acima de varejo; ChatGPT,
   Groq e Perplexity mostram o contrário. A vantagem agregada vem de +574
   respostas do Claude Haiku e +134 do Gemini (este contaminado por
   truncamento), contra três engines que apontam ao contrário. A "sistematicidade
   setorial" é falsa entre engines. Tornar isto achado de primeira ordem, não
   ressalva.

C15 [MAJOR] — Riscos éticos de publicar ranking de marcas reais brasileiras.
   (Fonte: R3-e)
   Publicar que "Nubank domina a atenção dos LLMs" ou que a saúde tem "0% de
   citações negativas" tem implicações reputacionais e concorrenciais. Exige
   ethics statement: medição observacional (não auditoria de qualidade); viés
   atribuído ao MODELO, não à conduta das empresas; sem dado pessoal (LGPD,
   pessoas jurídicas); dataset/protocolo públicos como direito de resposta
   factual. Anonimizar é contraproducente (o caso Nubank É o paper) e não reduz
   risco real.

C16 [MAJOR] — Reprodutibilidade incompleta.
   (Fonte: R3-f; draft §2.5)
   Faltam, de forma bloqueante: manifests SHA-256 do papers.db congelado, dos
   scripts e do dump público (citados como [A PRODUZIR]); dataset público
   versionado (Zenodo/DOI) com dicionário de dados; codebook do NER (aliases por
   vertical, regras de folding, desambiguação) — sem ele a assimetria de alias
   (saúde 991 vs tecnologia 4 hits) não é auditável; protocolo de seleção do
   roster (não cego, não pré-registrado); environment lock dos scripts.

............................ CRÍTICAS MINOR .............................

C17 [MINOR] — Partição arbitrária de entidades do mesmo grupo econômico.
   (Fonte: R1-m6 + R1-R-m6, executado)
   Verificado: ZERO strings de entidade aparecem em mais de uma vertical (sem
   vazamento). Mas Mercado Pago (fintech, 299) e Mercado Livre (varejo, 2003) são
   o mesmo grupo (MercadoLibre); iFood (tecnologia, 216) é Movile. A alocação de
   cada marca a uma vertical é decisão de analista que afeta as taxas e o HHI por
   vertical, não pré-registrada. Declarar como grau de liberdade do desenho.

C18 [MINOR] — O modelo LOO ajusta MELHOR (sinal genuíno vive no dado sem-âncora).
   (Fonte: R1-m7)
   O pseudo-R² de McFadden sobe de 0,339 (cited_v2) para 0,352 (cited_loo): o
   desfecho recodificado é mais explicável pelas covariáveis estruturais —
   evidência adicional, não comentada no draft, de que o sinal genuíno de
   vertical/engine vive no dado sem-âncora.

C19 [MINOR] — Falta teste formal da assimetria do jackknife entre verticais.
   (Fonte: R1-m8)
   O draft propõe LOO para todas as verticais mas não propõe um teste da
   DIFERENÇA de drops (fintech cai 16,7 pp; demais 2,5 a 5,7 pp). É essa
   diferença que sustenta "a concentração de âncora é máxima em fintech". Precisa
   de IC sobre o drop, não só os pontos.

C20 [MINOR] — Restringir explicitamente a claim a "modelos de tier econômico".
   (Fonte: draft §8 bloqueador nº 6; R3 checklist)
   4 de 5 engines são tiers econômicos (gpt-4o-mini, haiku-4.5, sonar,
   llama-3.3-70b); os resultados não generalizam para flagships. Declarar as
   model_version exatas e a natureza interina dos dados (dia 50/90).

C21 [MINOR] — "Share of model" é buzzword industrial sem formalização acadêmica.
   (Fonte: R2-Crítica 4 Busca 9; R2 formulação final)
   "Share of Model" e "Share of Voice" são termos exclusivamente de
   marketing/indústria. Usar como termo técnico primário é arriscado (parece
   pop); mas não há formalização acadêmica, então formalizá-lo é oportunidade.
   Subordinar "share of model" a "within-category citation share" no corpo; deixá-lo
   como sinônimo informal/ponte com a indústria.

================================================================================
PARTE II — RESPOSTAS COMPLEMENTARES ROBUSTAS
================================================================================

--------------------------------------------------------------------------------
3. RESPOSTA A CADA CRÍTICA FATAL/MAJOR (com os números reais)
--------------------------------------------------------------------------------

Princípio das respostas: a honestidade vira força. Um paper que reporta as
próprias predições falhando e as próprias métricas como limites superiores ganha
credibilidade de revisor, não perde.

R-C1 (truncamento, FATAL) — Aceito integralmente. A re-coleta com response_text
   íntegro é o item nº 1 do roadmap. Enquanto isso, toda taxa absoluta é lida
   como limite, e o achado central (efeito-âncora) é blindado por uma validação
   independente do truncamento: no Perplexity ÍNTEGRO, a fintech-LOO (67,9%) já
   fica abaixo do varejo (92,9%) — ou seja, o efeito-âncora NÃO é artefato de
   truncamento (R1-R-M5). Adotaremos o dual-track da onda 4 do board: a coorte
   íntegra nova roda em paralelo à série truncada histórica, permitindo medir
   exatamente quanto o corte distorce cada vertical.

R-C2 (clustering, FATAL) — Aceito. GLMM logístico com interceptos aleatórios por
   query, dia e engine, desfecho duplo (cited_v2 e cited_loo), OR com IC95
   robustos, mais bootstrap por cluster de query. A análise de poder passa para o
   nível de cluster (~240), não de observação. Já executamos o teste-piloto em
   nível de cluster (ver R-C5): ele faz exatamente o que se espera de um achado
   honesto — derruba o frágil e preserva o robusto.

R-C3 (decoys, FATAL) — Aceito como bloqueador. A regra de fontes do projeto já
   resolveu o conflito: o briefing do board dizia "FPR baixo (calibração ok)",
   mas os números verificados do papers.db (96,9 a 98,6%) VENCEM. Auditaremos se
   o FPR alto é por design (decoy plantado no prompt para testar obediência — e
   então não é comparável à citação espontânea, devendo ser descrito como tal) ou
   bug do detector (e então corrige-se a especificidade). Precisão/recall do NER
   serão reportados por vertical em amostra estratificada revisada manualmente.

R-C4 (RAG vs paramétrico, FATAL) — Aceito; é correção de reframing. Nunca
   reportar a média conjunta como número-título. Sem Perplexity, fintech = 20,80%
   e o ranking se mantém. O paper estratifica sempre: o sinal "puro" de B1 é o gap
   de 40 pp paramétrico no Claude (51,0% fintech vs 10,4% tecnologia); o Perplexity
   é reportado à parte como comportamento de RAG. Sun et al. (2410.00857) sustenta
   que sob RAG o modelo se apoia no contexto recuperado — por isso o gap comprime
   em Perplexity e a cauda é reamostrada.

R-C5 (gap bruto morre no clustering, MAJOR) — Confirmado com número, e
   transformado em resultado de primeira ordem. O R1 rodou o teste de Welch entre
   as médias por-cluster (48 clusters/vertical, >=30 obs cada):

      Quantidade                    fintech    varejo
      Query-clusters                  48         48
      Média da taxa por cluster     26,51%     23,30%
      Desvio (pop.) entre clusters  24,74 pp   23,60 pp
      Welch t = 0,645 (df ~94)  ->  NÃO significativo

   A variância entre queries (~24 pp) engole o gap de 3,2 pp. A claim "fintech tem
   a maior taxa" passa a observação descritiva. MAS a assimetria é decisiva: o
   mesmo teste com a taxa LOO da fintech vs varejo bruto dá

      fintech-LOO média por cluster = 10,50%; varejo = 23,30%
      Welch t = -3,353  ->  significativo, sinal NEGATIVO

   O achado frágil (vantagem setorial) cai exatamente onde deve (t=0,65); o achado
   robusto (dominância de âncora, agora reversão) sobrevive ao clustering
   (t=-3,35). Elevamos este contraste a resultado de primeira ordem.

R-C6 (share do Nubank cresce 41% para 57%, MAJOR) — Confirmado e incorporado como
   série temporal (figura nova). Trajetória semanal medida pelo R1:

      Semana    Menções  Nubank  Share Nubank  Sole-Nubank das citadas
      2026-W16    872      365      41,9%           53,5%
      2026-W17  1.036      423      40,8%           51,7%
      2026-W18    306      126      41,2%           53,5%
      2026-W19  1.218      620      50,9%           61,1%
      2026-W20    984      583      59,2%           66,7%
      2026-W21    929      468      50,4%           59,3%
      2026-W22  1.449      767      52,9%           59,8%
      2026-W23    318      181      56,9%           61,5%

   A "robustez temporal" do draft era da TAXA da vertical (estável por
   compensação: a cauda encolhe enquanto a âncora cresce, mantendo o agregado
   fixo). Reportamos o share da âncora como SÉRIE, declaramos o crescimento como
   ameaça de service drift e o medimos até o dia 90. A estabilidade do agregado
   deixa de ser argumento de robustez e vira possível artefato compensatório.

R-C7 (truncamento contamina o HHI, MAJOR) — Aceito; declaramos 49,7% como LIMITE
   SUPERIOR. Onde o Nubank aparece (R1-R-M4b): offset médio 118 chars quando é a
   primeira entidade da fintech (dentro da janela de 200). As âncoras de cauda
   aparecem tarde — Itaú 402, PicPay 515, Banco Inter 838, BTG 906 chars — e
   seriam apagadas pelo corte. Logo o truncamento exagera a dominância do Nubank
   DENTRO da fintech, não só entre verticais. A re-coleta íntegra é pré-requisito
   para o próprio número-título da tese.

R-C8 (front-loading, MAJOR) — Corrigimos a direção da narrativa com os offsets
   reais (Perplexity íntegro, só citadas):

      Vertical     Offset médio 1ª entidade   n
      Varejo            111,1               3.154
      Fintech           123,1               3.561
      Saúde             159,9               1.684
      Tecnologia        173,3               1.819

      Fração cuja 1ª entidade aparece DEPOIS do char 200 (= perdida se truncado):
      Fintech     20,5%   |  Varejo  20,9%  |  Saúde 30,7%  |  Tecnologia 51,6%

   Conclusão: (a) varejo front-loada MAIS que fintech, logo "fintech é premiada
   por front-loading" é falsa; (b) o truncamento opera penalizando os rivais —
   apaga 51,6% das citações de tecnologia e 30,7% de saúde. Isso infla o gap
   fintech vs tecnologia/saúde (os 13,7 e 14,8 pp da Tabela 3.3 estão
   parcialmente fabricados pelo corte), mas NÃO o gap fintech vs varejo (ambos
   ~20%). Substituímos a narrativa "Nubank citado cedo" pela narrativa correta:
   "o truncamento remove diferencialmente as âncoras de cauda longa de
   tecnologia/saúde, que aparecem tarde".

R-C9 (Perplexity sub-potente, MAJOR) — Aceito. O LOO só no Perplexity, como teste
   de sanidade (R1-R-M5):

      Vertical     Taxa Perplexity   Taxa LOO (sem Nubank)
      Fintech         86,5%               67,9%
      Varejo          92,9%               92,9%
      Tecnologia      54,3%               54,3%
      Saúde           69,8%               69,8%

   Resultado tranquilizador: mesmo no engine não-truncado, fintech-LOO (67,9%)
   fica abaixo do varejo (92,9%); e varejo/tech/saúde têm LOO igual à taxa
   original (o RAG raramente cita a âncora sozinha), reforçando que a dependência
   de âncora-única é genuinamente específica da fintech mesmo em dado limpo. MAS
   isto se apoia em apenas 24 clusters; declaramos a validação confirmatória limpa
   como sub-potente e exigimos a re-coleta restaurando as 48 queries do Perplexity.

R-C10 (construto vs rótulo, MAJOR) — Resolvido pela formalização do R2 (ver §4):
   definição com limiar τ/δ, concentração como par (HHI, share da âncora),
   efeito-âncora como Δᵥ via leave-one-out, e o mecanismo convexo γ>1. O construto
   passa a ser falsificável e discreto: varejo (Mercado Livre 29,5%, abaixo de τ,
   com Magalu colado) NÃO tem âncora única; fintech (Nubank 49,68%, gap enorme)
   tem.

R-C11 (delta sobre popularity bias, MAJOR) — Precisamos a UNIDADE de novidade.
   Popularity bias é por-item; nossa contribuição é por-categoria: documentamos a
   TRANSMISSÃO de um viés por-item para uma aparente propriedade de categoria, e
   damos o estimador que a desmonta (Δᵥ via LOO). Em relação a 2512.09483: eles
   medem concentração de domínios-fonte (long-tailed); nós medimos concentração de
   marca dentro de categoria (winner-take-most) — unidades diferentes, demarcação
   obrigatória. E o ranking bruto fintech > tecnologia vira MOTIVAÇÃO, não
   contribuição (é folclore de indústria).

R-C12 (ponte fintech->GEO, MAJOR) — Disciplinada. Rebaixamos a Camada A a hipótese
   explicitamente não testada (nenhuma medida de corpus foi cruzada) e reportamos
   P-A1/P-A2 como REFUTAÇÕES. O peso mecanístico migra para o que tem assinatura
   discriminante: o gap de 40 pp paramétrico no Claude (B1) — que exclui uma
   explicação puramente RAG e localiza o efeito nos pesos — e a concentração HHI +
   posição uniforme (C1). A Camada A fica como mecanismo candidato a montante, a
   testar por cruzamento com share-of-voice de mídia em trabalho futuro.

R-C13 (três corpora teóricos, MAJOR) — Incorporados (ver §6, parágrafos prontos):
   Ehrenberg-Bass (mental availability/CEP/DBA) reescreve C1 e gera a predição P5;
   superstar firms / winner-take-most dá a cadeia network effects -> dominância de
   mercado -> dominância de corpus -> dominância paramétrica; Matthew effect /
   cumulative advantage (Merton 1968; DiPrete & Eirich 2006) formaliza o γ>1. A
   entidade-âncora deixa de ser fenômeno isolado e vira a projeção da vantagem
   cumulativa sobre a atenção paramétrica dos LLMs.

R-C14 (heterogeneidade por engine, MAJOR) — Promovido a achado de primeira ordem.
   Decomposição do gap fintech-varejo por engine (excesso de respostas citadas):
   Claude +574; Gemini +134 (artefato de truncamento); ChatGPT -117; Perplexity
   -91; Groq -93. A vantagem agregada vem quase inteira de um engine mais um
   artefato, contra três engines que apontam ao contrário. GLMM com interação
   vertical x LLM; sinal reportado por engine; Gemini removido/re-coletado.

R-C15 (ética, MAJOR) — Atendido com ethics statement (ver §8). Medição
   observacional; viés atribuído ao modelo; sem MNPI nem dado pessoal; dataset e
   protocolo públicos como direito de resposta factual; sem anonimização.

R-C16 (reprodutibilidade, MAJOR) — Atendido pelo checklist (ver §8): manifests
   SHA-256, release Zenodo/DOI com dicionário de dados, codebook do NER,
   protocolo de roster, environment lock.

--------------------------------------------------------------------------------
4. O CONSTRUTO FORMAL DO R2 — ANCHOR-ENTITY EFFECT
--------------------------------------------------------------------------------

O construto separa três objetos que o draft fundia: a ENTIDADE-âncora (o item),
a CONCENTRAÇÃO de âncora (propriedade do setor) e o EFEITO-âncora (a transmissão
do item para a taxa do setor).

DEFINIÇÃO FORMAL. Seja, num setor (vertical) v, a participação de menções da
entidade e dada por s(e,v) = menções(e,v) / menções(v). Então:

  - Entidade-âncora de v: a entidade e* = argmax s(e,v) SE E SOMENTE SE
       s(e*,v) >= τ  (limiar; sugerido τ = 0,40, pré-registrado)
       E  s(e*,v) - s(e2,v) >= δ  (gap para a 2ª colocada; sugerido δ = 0,15).
    Isto resolve a circularidade: varejo (Mercado Livre 29,5%, abaixo de τ, com
    Magalu colado) NÃO tem âncora — é bi-líder; fintech (Nubank 49,68%, gap
    enorme) TEM. O construto fica falsificável e discreto.

  - Concentração de âncora de v: o par (HHIᵥ, s(e*,v)). Não é só o HHI — é o HHI
    atribuível a uma única entidade, o que distingue "concentrado em torno de um"
    (fintech) de "concentrado em torno de poucos" (varejo).

  - Efeito-âncora (a quantidade-tese): Δᵥ = taxa(v) - taxa_LOO-âncora(v), a
    diferença entre a taxa observada e a contrafactual sob leave-one-out da
    âncora. Para fintech: Δ = 28,15 - 11,46 = 16,69 pp. É a operacionalização
    limpa do "componente superstar".

MECANISMO FORMAL (a peça que faltava — o retorno super-linear). Postula-se que a
probabilidade de citação espontânea de uma entidade é uma transformação CONVEXA
de sua frequência relativa no corpus, que por sua vez é uma transformação
CONVEXA (cumulative-advantage) de sua participação de mercado real:

      P(citar e | v)  ~=  g( f(e) ),    f(e)  proporcional a  m(e)^γ   com γ > 1
      (Matthew / cumulative advantage; g convexa e saturante — logística nos
       pesos paramétricos)

A predição-chave que distingue ANCHOR EFFECT de mera CONCENTRAÇÃO: como γ > 1, a
participação de citação s(e*,v) deve ser ESTRITAMENTE MAIOR que a participação de
mercado real da firma e* — sobre-representação super-linear. É o teste que separa
o construto de "popularity bias genérico" e que pode ser confrontado com market
share real (Nubank market share BR vs. 49,68% de share-of-citation).

AS 5 PREDIÇÕES FALSIFICÁVEIS (ordenadas por força do teste no dataset atual) e o
STATUS de cada uma:

  P1 (inversão sob LOO): remover a âncora inverte o ranking do setor.
     STATUS: CONFIRMADO. 28,15% -> 11,46%; OR ajustada 4,13 -> 0,77. A reversão
     sobrevive ao clustering (Welch t=-3,35) e é estável nas 8 semanas (gap sob
     LOO entre -7,6 e -8,2 pp em todas).

  P2 (sobre-representação convexa): s(e*,v) > market share real de e*.
     STATUS: TESTÁVEL, ainda não feito. É o teste DECISIVO de γ>1 e exige cruzar
     o 49,68% de share-of-citation com o market share real do Nubank no Brasil.

  P3 (gradiente engine): o efeito-âncora é maior em engines paramétricos puros
     (onde γ atua nos pesos) que em RAG (onde a recuperação ao vivo reamostra a
     cauda).
     STATUS: SUPORTADO. Claude (efeito forte, gap 40 pp paramétrico) vs Perplexity
     (gap comprimido; fintech-LOO 67,9% ainda < varejo 92,9%, mas o RAG reamostra
     a cauda).

  P4 (especificidade da âncora / controle negativo): setores sem âncora (varejo,
     τ não atingido) não invertem sob LOO de qualquer líder único.
     STATUS: TESTÁVEL via LOO-para-todas-as-verticais (draft §7.2.4). É o controle
     negativo que blinda contra "todo setor desmorona sob LOO". Já há sinal: o LOO
     de UMA entidade derruba varejo só -5,67 pp vs fintech -16,70 pp (ver §5).

  P5 (mental availability): s(e*,v) correlaciona com a mental availability da
     marca medida por survey (ponte Ehrenberg-Bass).
     STATUS: TRABALHO FUTURO. É a predição que mais eleva o paper de medição a
     teoria; nenhum paper acadêmico cruzou mental availability com citação de LLM
     (R2 Busca 5).

--------------------------------------------------------------------------------
5. REFORMULAÇÃO DA TESE — DE "SUPERSTAR ÚNICA" PARA "NÚCLEO DE ÂNCORAS TOP-K"
--------------------------------------------------------------------------------

O R1 executou o jackknife da entidade-TOP de CADA vertical — a análise central
para a generalização:

   Vertical     Entidade-âncora      Taxa orig.  Taxa LOO (só o top)  Queda (pp)
   Fintech      Nubank (49,7%)         28,15%        11,46%            -16,70
   Varejo       Mercado Livre (29,5%)  24,94%        19,27%             -5,67
   Tecnologia   Totvs (24,8%)          14,50%        11,60%             -2,89
   Saúde        Hypera (24,7%)         13,35%        10,80%             -2,55

Com a entidade ÚNICA top, fintech é dramaticamente mais frágil (queda 3x maior
que a do varejo). MAS o varejo é uma estrutura de DUPLA âncora (Mercado Livre +
Magazine Luiza = 58% das menções). Repetindo com a âncora real do varejo:

   Definição                                          Varejo
   Original                                           24,94%
   LOO Mercado Livre apenas                           19,27%
   LOO Mercado Livre + Magazine Luiza (top-2)         10,59%  (queda -14,35 pp)

VEREDITO: o argumento "anchor-entity" GENERALIZA, mas não como "concentração numa
única entidade" — generaliza como "as taxas de TODAS as verticais são dominadas
pelo seu núcleo de âncoras". A diferença real entre fintech e varejo é o NÚMERO
de âncoras (1 vs 2), não a presença de concentração. O top-3 já dizia isso e foi
subexplorado: fintech 70,9% vs varejo 69,4% (Tabela 3.5).

O QUE ISSO MUDA NAS CLAIMS:

  1. A contribuição teórica migra de "uma superstar (Nubank)" para "concentração
     no núcleo de âncoras top-k, que varia por vertical; fintech é o caso extremo
     k=1". É mais honesto, mais generalizável e neutraliza a objeção de que a tese
     é "um achado sobre o Nubank disfarçado de teoria".

  2. A estabilidade da reversão protege a tese: o gap fintech-varejo sob LOO
     (ambas âncoras removidas em cada vertical) é negativo e estável (-7,6 a -8,2
     pp) em todas as 8 semanas — a reversão é estruturalmente consistente, não
     artefato de uma semana, desarmando "a reversão é dirigida por semanas
     específicas".

  3. Exige o teste formal da assimetria dos drops (C19/R1-m8): IC sobre a
     DIFERENÇA entre o drop da fintech (-16,70 pp para k=1) e os demais — é essa
     diferença que sustenta "a concentração de âncora é máxima em fintech".

  4. O construto τ/δ (§4) é o que torna a reformulação rigorosa: a "âncora única"
     é o regime s(e*,v) >= τ com gap >= δ; o "núcleo top-k" é a generalização
     quando a soma das k primeiras participações domina o HHI sem que nenhuma
     isolada atinja τ.

--------------------------------------------------------------------------------
6. OS 3 PARÁGRAFOS DE "RELATED WORK DELTA" (EN) + CONTRASTE COM arXiv:2512.09483
--------------------------------------------------------------------------------

Contraste obrigatório com arXiv:2512.09483 (Zhang, Ye, Peng, Garimella, Tyson,
10/dez/2025, "Source Coverage and Citation Bias in LLM-based vs. Traditional
Search Engines"). Verificado por WebFetch pelo R2: estuda DOMÍNIOS-fonte (não
menções espontâneas de entidades comerciais); NÃO é setorial/vertical; NÃO é
longitudinal (corte transversal); NÃO menciona mercado não-anglófono; o abstract
não usa HHI nem Gini (a métrica veio de literatura secundária); 55.936 queries,
6 LLM-SEs + 2 TSEs; "fewer than ten distinct URLs appear in 80% of responses". É o
vizinho mais próximo em concentração de citação, mas em UNIDADE DE ANÁLISE
(domínio, não marca), RECORTE (sem setor, sem mercado emergente) e DESENHO (sem
longitudinal) distintos. É de citação obrigatória e o principal contraste da
seção 2.

Parágrafo 1 — delta sobre popularity bias e concentração de domínio:

  Prior work on popularity bias in LLMs operates at the item level: popular
  entities are favored when models compare or recommend (Lehmann et al., 2026;
  Lichtenberg et al., 2024), and recent audits show that citation of source
  domains is more concentrated in LLM search engines than in traditional ones
  (Zhang et al., 2025). We depart from both along two axes. First, our unit of
  concern is the category, not the item or the domain: we show that an item-level
  popularity bias, when a category has produced a single superstar firm, surfaces
  as an apparent sectoral citation advantage, and we provide a leave-one-out
  estimator of the anchor effect (Delta_v) that separates the two. Second, we
  treat the anchor decomposition as a construct-validity test for the broader
  "sectoral bias" literature: any claim that LLMs favor sector X should survive
  removal of the sector's modal entity, lest it measure a firm rather than a
  sector.

Parágrafo 2 — delta sobre a literatura de indústria:

  A growing body of industry analyses reports that financial-services content is
  cited more often than technology or consumer-goods content (e.g., vendor
  studies of millions of AI citations), and popularizes "share of model" as the
  AI-era successor to share of voice. We treat these as motivation rather than
  evidence: they lack statistical testing, entity-level decomposition,
  longitudinal design, and peer review, and they conflate source-domain
  concentration -- which is long-tailed (Zhang et al., 2025) -- with
  within-category brand concentration, which we show is winner-take-most. Our
  contribution is to formalize the latter as a measurable construct (anchor
  entity / anchor effect) and to test it across engines and over time.

Parágrafo 3 — delta interdisciplinar (as três literaturas ausentes):

  We bridge three literatures absent from prior GEO and LLM-bias work. From
  marketing science, the Ehrenberg-Bass account of mental availability -- brands
  evoked across many Category Entry Points and retrieved via Distinctive Brand
  Assets (Sharp, 2010; Romaniuk & Sharp, 2022) -- gives a falsifiable reading of
  why a single brand becomes the category's anchor: it predicts that
  within-category citation share tracks survey-measured mental availability. From
  economics, the theory of superstar firms (Autor et al., 2020) and digital
  winner-take-most dynamics supplies the upstream mechanism by which market
  concentration becomes corpus concentration. From sociology, cumulative
  advantage / the Matthew effect (Merton, 1968; DiPrete & Eirich, 2006), recently
  applied to LLM substrates (e.g., AI programming assistants, 2025), formalizes
  the convex, super-linear mapping from market share to citation share that
  distinguishes an anchor effect from mere concentration. The anchor entity is
  thus not a new phenomenon in isolation but the projection of cumulative
  advantage onto the parametric attention of LLMs -- a contribution that ports an
  established mechanism to a new substrate and measures it.

Referências verificadas a entrar no BibTeX (reconfirmar DOIs clássicos no final):
  - Merton, R. K. (1968). "The Matthew Effect in Science." Science, 159(3810),
    56-63. DOI 10.1126/science.159.3810.56.
  - DiPrete, T. A., & Eirich, G. M. (2006). "Cumulative Advantage as a Mechanism
    for Inequality." Annual Review of Sociology, 32, 271-297.
    DOI 10.1146/annurev.soc.32.061604.123127.
  - Autor, Dorn, Katz, Patterson, Van Reenen (2020). "The Fall of the Labor
    Share and the Rise of Superstar Firms." QJE, 135(2), 645-709.
    DOI 10.1093/qje/qjaa004.
  - Sharp, B. (2010), How Brands Grow, Oxford; Romaniuk, J., & Sharp, B. (2022),
    How Brands Grow Part 2, Oxford (rev. ed.).
  - Zhang et al. (2025), arXiv:2512.09483 (related work obrigatório).
  - Lehmann et al. (2510.16815, EACL 2026); arXiv:2509.23261 (Matthew effect em
    substrato LLM).

================================================================================
PARTE III — POR QUE A VERTICAL FINTECH TEM MAIS CITAÇÕES EM GEO
================================================================================

--------------------------------------------------------------------------------
7. A EXPLICAÇÃO EM CAMADAS (reconciliando tudo o que foi descoberto)
--------------------------------------------------------------------------------

Esta é a explicação final, profunda e citável — o coração do pedido. Ela parte de
uma advertência que o board (onda 3, economistas) colocou como pré-condição de
honestidade e que torna o paper citável: a liderança da fintech é, em grande
parte, a liderança de UMA marca. Mas, dito isso, o fenômeno bruto é REAL no nível
agregado, e merece uma explicação mecanística completa. As quatro camadas abaixo
reconciliam o número bruto (28,15%) com tudo o que a decomposição revelou.

PONTO DE PARTIDA — o fenômeno bruto existe e é real NO NÍVEL AGREGADO.
   No núcleo de 50.453 observações, fintech lidera a citação espontânea com
   28,15%, à frente de varejo (24,94%), tecnologia (14,50%) e saúde (13,35%). Esse
   ordenamento é estável nas 8 semanas e a ordenação de CONCENTRAÇÃO (HHI fintech
   0,283 > varejo 0,202 > saúde 0,154 > tecnologia 0,110) acompanha de perto a
   ordenação de TAXA. Concentração e citabilidade são duas faces da mesma
   estrutura de mercado. O erro do draft não foi enxergar o fenômeno — foi
   atribuí-lo a uma propriedade DIFUSA da vertical. A explicação correta é que o
   agregado é produzido por quatro mecanismos encadeados, não por um "espírito
   setorial".

CAMADA (a) — O SETOR FINTECH BR GEROU A ENTIDADE-ÂNCORA MAIS FORTE DO PAÍS.
   A fintech brasileira produziu, no Nubank, a entidade-âncora mais forte do
   mercado nacional, por uma conjunção que nenhuma outra vertical reúne na mesma
   intensidade:
     - Marca-categoria (mental availability máxima). "Nubank" ocupa quase 1-para-1
       o slot semântico de "banco digital brasileiro" — é a resposta canônica
       evocada pelo maior número de Category Entry Points do setor (abrir conta,
       cartão sem anuidade, banco no celular, primeiro cartão). Em vocabulário
       Ehrenberg-Bass, é a marca com maior probabilidade de ser evocada através do
       maior número de pontos de entrada da categoria.
     - Nome lexicalmente único e limpo (Distinctive Brand Asset verbal). "Nubank"
       é uma string rara, sem ambiguidade — ao contrário de "Amazon", "Oracle" ou
       "Google", que sofrem falsos negativos/positivos no NER e diluem-se em outros
       sentidos. Um nome único maximiza tanto a saliência no corpus quanto a
       extraibilidade pelo detector.
     - Densidade de corpus. O setor alimenta um fluxo textual de altíssima cadência
       que nomeia a marca diariamente: imprensa especializada (Finsiders, NeoFeed,
       editorias de finanças), conteúdo de comparação e consumidor (comparadores de
       cartões/contas, Reclame Aqui), SEO nativo digital agressivo ("o que é Pix",
       "conta digital", marca no H1) e documentação institucional (Banco Central,
       Pix, Open Finance) — corpus oficial, estável e citável. RESSALVA HONESTA: o
       paper NÃO mediu volume de corpus; esta camada (a Camada A do draft) é
       hipótese candidata a montante, não causalidade estabelecida, e suas predições
       diretas (efeito máximo no RAG; gap maior em PT) foram REFUTADAS pelos dados.
     - Pix / Open Finance como narrativa. A infraestrutura de pagamento instantâneo
       e finanças abertas deu ao setor uma narrativa nacional densa em que a marca
       aparece colada à categoria ("Pix" aproxima-se de "pagamento instantâneo" do
       mesmo modo que "Nubank" de "banco digital"), multiplicando os pontos de
       entrada da categoria.

CAMADA (b) — TRANSMISSÃO ENTIDADE -> CATEGORIA VIA VANTAGEM CUMULATIVA.
   Aqui está o coração teórico. O viés de popularidade é por-ITEM (entidades
   populares são favorecidas); o que medimos é a TRANSMISSÃO desse viés por-item
   para uma aparente propriedade de CATEGORIA. O mecanismo é a vantagem cumulativa
   (Matthew effect): como o mapeamento de market share para citation share é
   convexo (γ > 1), uma firma com, digamos, 30% de participação de mercado captura
   ~50% das menções — sobre-representação super-linear. A evidência VIVA dessa
   transmissão em curso é que o share do Nubank CRESCE dentro da própria janela de
   medição: de ~41% (W16 a W18) para ~53 a 59% (W19 a W23), aumento relativo de
   ~30% em 50 dias. O rico fica mais rico DENTRO do experimento. É por isso que a
   "taxa da vertical" parece estável (a cauda — PicPay, C6, Inter — encolhe
   enquanto a âncora cresce, compensando o agregado) enquanto a CONCENTRAÇÃO, que é
   a tese, está em alta. A vantagem setorial aparente é, literalmente, a sombra de
   uma firma superstar projetada sobre a média da categoria.

CAMADA (c) — AMPLIFICAÇÃO POR ENGINES PARAMÉTRICOS.
   A transmissão não é uniforme entre motores — e é por isso que a "sistematicidade
   setorial" é falsa. Em modelos paramétricos puros, o γ atua diretamente nos
   pesos: o Claude Haiku cita fintech em 51,0% contra 10,4% em tecnologia — um gap
   de 40 pp que é a evidência mais forte e menos anedótica do paper, porque mostra
   que a vantagem vive NOS PESOS, não na recuperação ao vivo. A decomposição do gap
   agregado fintech-varejo confirma: +574 respostas vêm do Claude e +134 do Gemini
   (este contaminado por truncamento), contra ChatGPT -117, Perplexity -91 e Groq
   -93. Ou seja, a vantagem agregada é quase inteiramente uma idiossincrasia de UM
   engine paramétrico mais um artefato. Sob RAG (Perplexity), a recuperação ao vivo
   reamostra a cauda e comprime o gap: a fintech-LOO cai para 67,9%, ainda abaixo do
   varejo (92,9%), mas o motor já não deixa a âncora citar sozinha. O engine importa
   MAIS que o setor.

CAMADA (d) — MEDIÇÃO EM JANELA DE ABERTURA QUE FAVORECE QUEM É CITADO PRIMEIRO.
   Por fim, parte do número bruto é uma propriedade do INSTRUMENTO e do MOMENTO. O
   NER rodou sobre os primeiros ~200 caracteres em 4 de 5 engines, medindo
   front-loading, não citação plena. Esse corte NÃO premia a fintech por
   front-loading (varejo front-loada mais: offset 111 < 123 chars) — ele PENALIZA
   os rivais: apagaria 51,6% das citações de tecnologia e 30,7% de saúde, que
   aparecem tarde, contra ~20% de fintech/varejo. E, dentro da própria fintech, o
   corte exagera a dominância do Nubank (offset 118, dentro da janela) ao apagar as
   âncoras de cauda que aparecem tarde (Itaú 402, PicPay 515, Inter 838, BTG 906
   chars). Some-se a isso a natureza interina da janela (dia 50 de 90): estamos
   medindo na ABERTURA do fenômeno, quando a vantagem cumulativa ainda está
   acelerando, o que favorece quem já é citado primeiro. Por isso o 28,15% e o
   49,68% são limites SUPERIORES até a re-coleta íntegra.

SÍNTESE — POR QUE A FINTECH "GANHA". A fintech não ganha por ser fintech. Ela
ganha porque (a) gerou a âncora de categoria mais forte do país, (b) essa âncora
transmite seu viés por-item para uma aparente vantagem de categoria via vantagem
cumulativa super-linear em pleno crescimento, (c) um ou dois engines paramétricos
amplificam essa transmissão nos seus pesos, e (d) o instrumento e o momento da
medição favorecem quem aparece primeiro. Remova a âncora e o "setor" desaba de
primeiro para último (28,15% -> 11,46%; OR 4,13 -> 0,77). O fenômeno agregado é
real; a sua atribuição à vertical não é.

O QUE ISSO ENSINA SOBRE GEO. Para uma marca ser citada, SER A ÂNCORA DA CATEGORIA
vale mais que pertencer à vertical "certa". A vertical é epifenômeno; a âncora é o
ativo. Implicações práticas para marcas brasileiras:

  - A âncora é o ativo, não a presença. O objetivo de GEO não é "aparecer" — é
    tornar-se a entidade-categoria, o nome que o modelo emite por padrão quando a
    categoria é evocada. Nubank captura 49,68% das menções de fintech e 59,31% das
    respostas com citação na vertical o citam SOZINHO. Quem se torna a resposta
    canônica de uma classe de perguntas captura uma fração desproporcional da
    atenção do modelo.

  - O motor importa mais que o setor. Como o efeito é fortemente heterogêneo por
    engine (forte no Claude, comprimido no Perplexity, invertido no ChatGPT/Groq), a
    estratégia de GEO não pode ser única: a marca precisa medir sua visibilidade
    engine por engine. Forte desempenho em Claude não se traduz em ChatGPT nem
    Perplexity.

  - A oportunidade está nas categorias fragmentadas. Tecnologia B2B (HHI 0,110) não
    tem âncora consolidada — é onde uma marca ainda pode se tornar a entidade-
    categoria com investimento dirigido em corpus. Categorias já ancoradas (fintech)
    são defesa para o líder, ataque difícil para os demais.

  - Mental availability e nome único são alavancas. Maximizar Category Entry Points
    (ser a resposta para o maior número de perguntas da categoria) e manter um nome
    lexicalmente único e limpo aumentam tanto a saliência no corpus quanto a
    extraibilidade pelos motores.

  - Densidade de cauda protege a categoria. A fintech tem cauda própria robusta
    (PicPay 770, C6 737, Inter 558, somando ~2.065 menções) — marcas não-âncora
    ainda capturam atenção significativa. Construir presença em corpus PT-BR de alta
    cadência (imprensa especializada, comparadores, documentação institucional) é a
    alavanca da camada de oferta.

  - YMYL muda o jogo em categorias sensíveis. Em saúde, o RLHF empurra para
    respostas genéricas e hedged (0% de menções negativas, mais hedging); ali o GEO
    compete não por saliência de marca, mas por ser a fonte institucional citável
    que sobrevive ao guardrail de cautela.

  - Medição honesta é vantagem competitiva. O setor de GEO vende "vantagens
    setoriais" e taxas absolutas; este estudo mostra que tais números são frágeis a
    uma única entidade e a artefatos de medição. Um programa de GEO sério mede share
    of model por entidade E por engine, reporta com e sem a âncora, e separa RAG de
    paramétrico.

================================================================================
PARTE IV — PACOTE DE PUBLICAÇÃO ATUALIZADO
================================================================================

--------------------------------------------------------------------------------
8. PACOTE DE PUBLICAÇÃO
--------------------------------------------------------------------------------

8.1 ABSTRACT EN REVISADO (R3, ajustado à tese top-k, ~250 palavras)

  Spontaneous brand mentions in large language model (LLM) outputs are an emerging
  channel of economic visibility, yet systematic, longitudinal, and calibrated
  measurement remains scarce, especially outside English-language markets. We
  report an interim 50-day audit (April-June 2026) of spontaneous brand citation
  across five economy-tier LLMs (GPT-4o-mini, Claude Haiku-4.5, Gemini-2.5-pro,
  Perplexity sonar, Llama-3.3-70B) for four Brazilian verticals (fintech, retail,
  technology, healthcare), using 48 structurally paired prompts per vertical in
  Portuguese and English and per-entity NER over a 127-entity cohort with
  fictitious decoys. Naively, fintech leads spontaneous citation (28.2% vs 24.9% /
  14.5% / 13.3%). We show this aggregate advantage is not a diffuse sectoral effect
  but is dominated by a category's top-k anchor entities: in fintech a single
  anchor (Nubank) accounts for 49.7% of mentions, and 59.3% of fintech citations
  name Nubank exclusively. A leave-one-out recoding drops fintech to 11.5% -- last
  place -- and inverts its adjusted odds ratio from 4.13 to 0.77; the same jackknife
  applied per vertical shows every sector is anchor-driven (retail falls 14.4 points
  once its two anchors are removed), with fintech the extreme k=1 case. The effect
  is engine-driven: only two of five engines place fintech above retail, and the
  aggregate gap is largely a Claude-Haiku idiosyncrasy. Citation concentration
  (Herfindahl index) tracks citation rate across verticals, consistent with a
  cumulative-advantage account in which nameable category brands behave as
  attentional superstar firms. We document measurement threats -- 200-character
  response truncation in four engines (capturing front-loading, and inflating the
  anchor's apparent concentration) and a 97-99% decoy false-positive rate -- and
  specify the dual-track recollection and clustered-inference protocol required for
  confirmatory claims. Our contribution is a reproducible anchor-entity framework
  for sectoral LLM citation bias in a non-Anglophone market.

  (Ajustes vs. abstract do draft §9.3: a frase-tese migrou de "single anchor" para
   "top-k anchor entities", com o jackknife per-vertical e o retail -14,4 pp
   explícitos; o número-choque puxado para cedo; ressalva de que o truncamento
   também infla a concentração aparente da âncora; tier econômico e natureza
   interina declarados.)

8.2 COVER LETTER EN (~200 palavras)

  Dear Program Chairs,

  We submit "Anchor-Entity Concentration in LLM Brand Citations" for consideration
  at [VENUE]. The paper began as an investigation into an apparent sectoral
  citation advantage -- Brazilian fintech brands appeared most cited by LLMs -- and
  arrived at a more durable and, we believe, more interesting finding: the advantage
  is not sectoral at all. It is the shadow of a category's anchor entities. Removing
  one brand (Nubank) drops fintech from first to last place and inverts its adjusted
  odds ratio from 4.13 to 0.77; the same leave-one-out, applied per vertical, shows
  every sector is anchor-driven, with fintech the extreme single-anchor case.

  We think this matters to the [VENUE] community for three reasons. First, it
  reframes "sectoral bias" in LLM visibility as anchor-entity concentration -- a
  share-of-model analogue to market concentration, measurable with a Herfindahl
  index and a leave-one-out anchor estimator. Second, it is the first longitudinal,
  multi-engine audit of spontaneous commercial-entity citation in a non-Anglophone
  emerging market, with paired prompts, decoys, and a public dataset. Third, it is
  candid about measurement: we surface and quantify the construct-validity threats
  (front-loading from response truncation, decoy specificity, engine heterogeneity)
  that any citation audit must confront, and we ship a reproducibility package.

  The work is observational and explicitly scoped to economy-tier models. We declare
  all data as interim pending window close. We have no competing interests and name
  no brand evaluatively.

  Sincerely, The Authors

8.3 AS 6 FIGURAS (a Figura 7 nova: série temporal do share do Nubank)

  Figura 1 — Taxa de citação por vertical, original vs leave-one-out (figura-tese).
     Barras agrupadas. X: as 4 verticais. Y: taxa de citação espontânea (%), 0-30%.
     Duas barras por vertical: clara = cited_v2; escura = cited_loo (sem âncora).
     Barras de erro = IC95 Wilson. Anotação na fintech: 28,15% -> 11,46%, com seta
     indicando a queda de 1º para último. NOVO (top-k): incluir a barra LOO top-2 do
     varejo (24,94% -> 10,59%) para mostrar que o varejo também é anchor-driven.
     Mensagem: a remoção da âncora colapsa e inverte o ranking; toda vertical é
     anchor-driven, fintech no extremo k=1.

  Figura 2 — Forest plot da inversão de OR (fintech vs saúde, ajustada).
     Forest plot horizontal. X: OR em escala log, linha de referência em 1,0. Dois
     pontos com IC95: OR original 4,13 (3,81-4,47), à direita; OR sob LOO 0,77
     (0,70-0,84), à esquerda. Mensagem: o efeito não só encolhe — cruza a linha de
     nulidade e inverte de sinal. Prova estatística da frase-tese.

  Figura 3 — Heterogeneidade por engine (small multiples).
     Cinco mini-gráficos (ChatGPT, Claude, Gemini, Groq, Perplexity), cada um com
     barras fintech vs varejo, eixo Y comum (0-100%). Verde quando fintech > varejo,
     vermelho quando fintech < varejo. Só Claude (+20,3) e Gemini (+4,9, asterisco
     "artefato de truncamento") são verdes; ChatGPT, Groq, Perplexity vermelhos.
     Mensagem: o "efeito setorial" não é consistente; só 2 de 5 engines o sustentam.

  Figura 4 — Concentração (HHI) vs taxa de citação, por vertical (scatter).
     Dispersão. X: HHI (0,11-0,283). Y: taxa (%). Quatro pontos rotulados com linha
     de tendência; tamanho do ponto proporcional ao nº de menções. Mensagem:
     concentração e citabilidade são correlacionadas; share of model segue share of
     market.

  Figura 5 — Decomposição do gap fintech-varejo por engine (barras divergentes).
     Barras divergentes em torno de zero. Y: engines. X: excesso de respostas
     citadas (fintech menos varejo), de -150 a +600. Claude +574, Gemini +134
     (hachurada, "artefato"), ChatGPT -117, Perplexity -91, Groq -93. Mensagem: a
     vantagem agregada vem quase inteira de um engine mais um artefato, contra três
     engines que apontam ao contrário.

  Figura 6 — A ameaça de medição: distribuição de comprimento de resposta por engine.
     Densidade ou boxplot. X: LENGTH(response_text) em chars (0-2500). ChatGPT,
     Claude, Gemini colapsadas numa linha vertical em exatos 200 chars (100%
     truncadas); Perplexity espalhada de 198 a 2502. Inset com a amostra do Gemini
     cortada em "volume de v[endas]". Mensagem: o que medimos como "citação" é, em 4
     de 5 engines, front-loading nos primeiros 200 chars — não citação plena.

  Figura 7 (NOVA) — Série temporal do share do Nubank nas menções de fintech.
     Linha (ou área) por semana (W16 a W23). Y esquerdo: share do Nubank (%),
     41,9 -> 40,8 -> 41,2 -> 50,9 -> 59,2 -> 50,4 -> 52,9 -> 56,9. Segunda linha:
     fração sole-Nubank das citadas (53,5 a 66,7%). Sobrepor, em linha pontilhada
     plana, a TAXA bruta da vertical fintech (estável ~27 a 29%) para mostrar o
     contraste: a concentração SOBE enquanto o agregado fica estável (compensação
     pela cauda). Mensagem: a vantagem cumulativa está em curso dentro da própria
     janela — service drift a favor da âncora; a "robustez temporal" do agregado é
     artefato compensatório, não solidez.

  (Layout do corpo: Figuras 1, 2, 3, 4 e 7 no corpo; Figuras 5 e 6 conforme espaço;
   tabelas 3.4, 3.8 e 3.9 para apêndice; corpo retém 3.1, 3.5 (HHI), 3.6 (LOO).)

8.4 CHECKLIST DE SUBMISSÃO

  Bloqueadores de medição (resolver antes de qualquer submissão):
   [ ] Re-coletar com response_text íntegro (remover corte de 200 chars), re-rodar
       NER v2; validar MAX(LENGTH) > 200 em todos os engines; reportar como a taxa
       muda. RESTAURAR as 48 queries do Perplexity (não só destruncar os 4 demais).
   [ ] Auditar e explicar o FPR de decoys (96,9-98,6%): por design ou bug; corrigir
       a especificidade se for bug.
   [ ] Decidir sobre o Gemini: remover da análise principal ou re-coletar.

  Inferência estatística:
   [ ] GLMM logístico com interceptos aleatórios (query, dia, engine) e desfecho
       duplo (cited_v2 e cited_loo); OR com IC95 robustos.
   [ ] Correção de múltiplas comparações (Holm/FDR) sobre as 108 células e os testes
       par-a-par.
   [ ] Bootstrap por cluster de query; análise de poder no nível de cluster (~240).
   [ ] Leave-one-entity-out para as 4 verticais, top-k por vertical, com IC SOBRE OS
       DROPS (Nubank; Mercado Livre + Magalu; Totvs; Hypera/EMS).
   [ ] Teste de Welch por-cluster do gap bruto (já feito: t=0,65 n.s.) e da reversão
       LOO (já feito: t=-3,35 sig.) no corpo.
   [ ] Roster de tamanho fixo (15) por bootstrap; matching estrito vs alias lado a
       lado.

  Reprodutibilidade e artefatos:
   [ ] Manifests SHA-256 do papers.db congelado, scripts e dump público.
   [ ] Dataset público versionado (Zenodo/DOI) com dicionário de dados.
   [ ] Codebook do NER: aliases por vertical, regras de folding, desambiguação.
   [ ] Protocolo de seleção do roster (idealmente pré-registrado); declarar a
       partição de grupos econômicos (Mercado Pago/Mercado Livre; iFood) como grau
       de liberdade.
   [ ] Environment lock dos scripts de análise.

  Enquadramento e claims:
   [ ] Frase-tese (âncora top-k, não vertical) no título, abstract e conclusão.
   [ ] Construto formal τ/δ + Δᵥ + função convexa γ>1 na seção 2/3.
   [ ] Reframe "superstar única" -> "núcleo de âncoras top-k; fintech extremo k=1".
   [ ] Nunca reportar a média RAG+paramétrico como número-título; separar Perplexity
       (sem ele, fintech = 20,80%).
   [ ] Restringir a claim a "modelos de tier econômico"; declarar model_version.
   [ ] Declarar os dados como interinos (dia 50/90) até o fechamento (~21/jul/2026);
       declarar 49,68% e 28,15% como limites superiores.
   [ ] Rebaixar a Camada A a hipótese não testada; reportar P-A1/P-A2 como REFUTAÇÕES.
   [ ] Inserir as três literaturas (Ehrenberg-Bass; superstar/winner-take-all;
       Matthew/cumulative advantage) e o related work obrigatório 2512.09483.
   [ ] Verificar todas as entradas [A VERIFICAR] da literatura (correntes 3,5,6,7,8).

  Ética e legal:
   [ ] Ethics statement: medição observacional, sem juízo de mérito de marca; sem
       dado pessoal (LGPD, pessoas jurídicas); viés atribuído ao modelo, não às
       empresas; alta citação não implica superioridade, baixa não implica
       deficiência.
   [ ] Declaração de ausência de conflito de interesse e de dados proprietários/MNPI.
   [ ] Dataset e protocolo públicos como direito de resposta factual; sem
       anonimização (o caso Nubank é o paper e o mecanismo é favorável a todos).

  Figuras e tabelas:
   [ ] Seis figuras principais + Figura 7 (série do share do Nubank) conforme 8.3;
       tabelas 3.4/3.8/3.9 para apêndice; corpo retém 3.1, 3.5, 3.6.

8.5 CRONOGRAMA ATÉ 21/JUL (re-coleta dual-track como item 1)

  Semana 1 (crítica) — DESTRAVAR A MEDIÇÃO (pré-condição inegociável do R3):
     1. RE-COLETA DUAL-TRACK (ITEM 1). Remover o corte de 200 chars no pipeline de
        persistência; rodar a coorte íntegra nova EM PARALELO à série truncada
        histórica (onda 4 do board), para medir exatamente quanto o corte distorce
        cada vertical. Restaurar as 48 queries do Perplexity. Validar
        LENGTH(response_text) > 200 em todos os engines.
     2. Auditar/explicar o FPR de 98% dos decoys (design vs bug; corrigir se bug).
     3. Decisão sobre Gemini (remover da análise principal ou re-coletar).

  Semana 2 — INFERÊNCIA CORRETA:
     - GLMM logístico (interceptos aleatórios query/dia/engine, desfecho duplo).
     - Correção de múltiplas comparações (Holm/FDR) sobre 108 células + par-a-par.
     - Bootstrap por cluster de query; consolidar Welch por-cluster (t=0,65 / t=-3,35).

  Semana 3 — ROBUSTEZ DE DECOMPOSIÇÃO:
     - Leave-one-entity-out top-k para as 4 verticais, com IC SOBRE OS DROPS.
     - Roster de tamanho fixo (15) por bootstrap; modelo controlando por |roster|.
     - Matching estrito vs alias; precisão/recall do NER por vertical (amostra
       estratificada revisada manualmente).

  Semana 4 — MECANISMOS DISCRIMINANTES:
     - Desagregar sources/freshness/autoridade de domínio DENTRO do Perplexity por
       vertical (testa A vs B3).
     - Interação vertical x LLM e vertical x categoria; fração de variância da
       interação com o laboratório.
     - Contraste de sentimento condicional à citação (testa C3/YMYL).
     - Cruzar 49,68% de share-of-citation com market share real do Nubank (testa P2,
       a sobre-representação convexa γ>1).

  Semana 5 — LITERATURA E ARTEFATOS:
     - Confirmar abstract/autoria de todas as entradas [A VERIFICAR] (correntes
       3,5,6,7,8); reconfirmar DOIs clássicos (Merton, DiPrete & Eirich, Autor).
     - Produzir manifests SHA-256 (papers.db congelado, scripts, dump público);
       preparar release Zenodo/GitHub com dicionário de dados e codebook do NER.

  Semana 6 — ESCRITA E FECHAMENTO:
     - Fechar a janela v2 (dia 90); re-rodar todas as tabelas no dataset final.
     - Redigir o manuscrito; escolher título e venue (ICWSM > WWW measurement >
       Information Sciences/TOIS > EMNLP/ACL Findings).
     - Passada final: garantir que nenhuma claim afirma "vantagem setorial
       sistemática" sem a ressalva de âncora top-k / engine; confirmar que toda taxa
       absoluta carrega a ressalva de limite superior até a re-coleta.

================================================================================
Fim do relatório. A espinha dorsal (efeito-entidade-âncora top-k + heterogeneidade
por engine + lições de medição) é publicável em ICWSM/WWW após a Semana 1 do
roadmap. A versão "vantagem setorial sistemática de fintech" seria desk-rejected.
================================================================================
