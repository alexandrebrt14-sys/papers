# Mecanismos da vantagem de citação fintech: oferta de corpus, demanda/treino e estrutura de mercado

## Introdução: o que precisa ser explicado

A regularidade empírica a ser explicada não é uma curiosidade marginal. No núcleo do experimento (n=50.453), a vertical fintech obtém citação espontânea em 28,15% das respostas (IC95 27,38-28,95%), à frente do varejo (24,94%), e muito à frente de tecnologia (14,50%) e saúde (13,35%). A diferença é estatisticamente robusta (fintech vs. tecnologia: chi2=699,6, p<1e-15; fintech vs. saúde: chi2=840,6, p<1e-15) e temporalmente estável: a ordenação das quatro verticais não se inverte em nenhuma das oito semanas observadas (W16 a W23), e a magnitude do gap oscila menos de dois pontos percentuais. Não é ruído amostral nem artefato de uma semana de cutoff.

Qualquer explicação candidata precisa ser disciplinada por um conjunto de fatos que, tomados em conjunto, eliminam vários suspeitos óbvios:

1. **O mix de categorias de query é comparável entre verticais.** Cada vertical recebeu aproximadamente a mesma proporção de queries de mercado, descoberta, comparativo, inovação, experiência e confiança. A vantagem fintech, portanto, não pode ser reduzida a "fizeram mais perguntas fáceis para fintech". (Há, porém, uma nuance importante discutida adiante: a vantagem fintech é maior justamente nas categorias de alta taxa de citação, sugerindo que o desenho experimental não inflou artificialmente o gap, mas também não o anulou.)
2. **O gap sobrevive em português e em inglês.** Fintech cita 31,8% em inglês e 24,5% em português; tecnologia, 17,4% e 11,6%. O efeito não é puramente um artefato de idioma de query.
3. **As covariáveis de resposta são quase idênticas.** Comprimento de resposta (~258-261 caracteres), tokens (~646-665), latência (~8.760-9.119ms) e densidade média de fontes (0,85-0,90) praticamente não variam entre verticais. O modelo não "trabalha mais" em fintech; ele simplesmente tem mais a dizer com nome próprio.
4. **A heterogeneidade entre modelos é dramática e informativa.** Claude cita fintech em 51,0% e tecnologia em apenas 10,4%; Gemini cita ~0% fora de fintech; Perplexity (RAG) cita 86,5% em fintech. A vantagem fintech não é uniforme entre arquiteturas — e essa não-uniformidade é o nosso principal instrumento discriminante.

Este é o ônus probatório que qualquer mecanismo precisa carregar. A seguir, organizamos os candidatos em três camadas causais — **oferta de corpus**, **demanda/treino** e **estrutura de mercado** — e, para cada mecanismo, derivamos predições observáveis distintas e um teste discriminante quando possível.

---

## 1. Taxonomia de mecanismos em três camadas

A intuição organizadora é uma cadeia de produção da citação. Um nome próprio só aparece numa resposta de LLM se (a) existe massa textual sobre ele no mundo digital, (b) essa massa foi absorvida pelo modelo — paramétrica (pré-treino/RLHF) ou recuperável (RAG) — e (c) a estrutura semântica do mercado faz daquele nome a resposta "canônica" para a classe de perguntas. As três camadas são logicamente sequenciais (oferta é pré-condição de absorção, que é pré-condição de saliência), mas empiricamente parcialmente separáveis, porque cada uma deixa assinaturas diferentes na matriz vertical×LLM, na concentração de entidades e no sentimento.

### Camada A — OFERTA DE CORPUS (densidade e qualidade do texto-fonte em PT-BR)

A hipótese central da camada A é que a fintech brasileira gera, por unidade de relevância econômica, muito mais texto digital indexável e de boa qualidade extrativa do que as outras três verticais. As fontes plausíveis dessa assimetria de oferta são:

- **A1 — Imprensa especializada de alta cadência.** Existe um ecossistema editorial dedicado quase exclusivamente a fintechs (publicações setoriais tipo Fintechs Brasil, NeoFeed, Finsiders, além de editorias de finanças em veículos generalistas) que produz texto fresco, factual e nomeado diariamente. A cobertura de tecnologia B2B é mais escassa e mais corporativa; a de saúde é diluída entre consumo, regulatório e científico; a de varejo é razoável (e o varejo, de fato, fica em segundo lugar).
- **A2 — Conteúdo de comparação e de consumidor.** Comparadores de cartões/contas, finanças pessoais, "melhor banco digital", e — crucialmente — Reclame Aqui. Fintechs vivem de reputação digital de massa; cada produto financeiro gera milhares de páginas de comparação e reclamação que mencionam a marca por extenso. O análogo em saúde (avaliação de medicamento/hospital) é menor e mais sensível; em tecnologia B2B, comparação de fornecedores é nicho.
- **A3 — SEO agressivo do próprio setor.** Fintechs são nativas digitais e investem pesadamente em conteúdo de fundo de funil otimizado para busca ("o que é Pix", "como funciona conta digital"), produzindo material auto-referente e altamente nomeado. Isso eleva tanto a densidade quanto a "extraibilidade" (texto bem estruturado, em PT-BR, com a marca no H1).
- **A4 — Documentação pública institucional.** Banco Central, regulamentação do Pix e do Open Finance criaram um corpus oficial, citável e estável que ancora a entidade-categoria (ver camada C). Não há equivalente de mesma densidade e nomeação para tecnologia ou para a maior parte da saúde de consumo.

**Predições observáveis distintas da camada A:**
- *(P-A1)* O efeito deve ser **maximamente visível em Perplexity** (RAG, freshness, recuperação ao vivo), porque RAG converte oferta de corpus quase diretamente em citação. Observamos Perplexity citando fintech a 86,5% — mas, atenção, varejo a 92,9%. Isto é um problema parcial para A pura (ver §3 do teste discriminante).
- *(P-A2)* Deve haver **gap fintech>tecnologia também em inglês**, mas comprimido, porque a oferta diferencial de corpus está concentrada no PT-BR. Confirmado: o gap fintech-tecnologia é de ~20pp em inglês (31,8 vs 17,4) e ~13pp em português (24,5 vs 11,6) — na verdade o gap em inglês é *maior*, o que é parcialmente desfavorável a uma versão estritamente PT-BR-cêntrica de A e favorece a hipótese de que a entidade fintech BR (Nubank) é grande o bastante para ter corpus em inglês também (cf. camada C).
- *(P-A3)* Oferta de corpus prediz **densidade de fontes mais alta em fintech sob RAG**. Os dados agregados de `sources` quase não variam (0,85-0,90), o que é fracamente contrário a uma assinatura de oferta forte — mas a métrica agregada mistura modelos paramétricos (sem fontes) e RAG, diluindo o sinal.

**Teste discriminante da camada A:** comparar, *dentro de Perplexity/RAG*, a densidade de fontes e a freshness das URLs citadas por vertical. Se A é o motor, fintech deve exibir mais URLs únicas, mais recentes e de maior autoridade de domínio do que tecnologia, *condicional ao modelo RAG*. O dado de `sources` agregado não testa isso — é necessário desagregar por engine.

### Camada B — DEMANDA/TREINO (como a oferta vira probabilidade paramétrica e recuperabilidade)

A camada B é o mecanismo de transmissão: como a massa textual da camada A se converte em comportamento do modelo. Há dois canais, e eles são separáveis pelos dados:

- **B1 — Frequência em corpora de pré-treino → probabilidade paramétrica.** Quanto mais um nome aparece no pré-treino, maior a probabilidade de ser emitido sem recuperação. Esse canal opera nos modelos paramétricos puros (Claude, ChatGPT em modo sem ferramenta, Gemini, Groq) e prediz que a vantagem fintech aparece *mesmo sem RAG*.
- **B2 — RLHF com perguntas de finanças pessoais.** Modelos de assistente recebem volume desproporcional de perguntas reais sobre dinheiro, cartões, bancos. O ajuste por preferência humana pode ter recompensado respostas que nomeiam instituições financeiras concretas e úteis (recomendar "Nubank" é útil e raramente perigoso), enquanto em saúde a recompensa foi para hedging e respostas genéricas (ver camada C). Esse canal prediz uma **assinatura por modelo**, mais forte em modelos fortemente RLHF-ados para utilidade ao consumidor.
- **B3 — Recência do cutoff e recuperabilidade em RAG.** Para RAG, o que importa não é o pré-treino mas a autoridade de domínio, o schema (marcação estruturada) e a freshness do índice. Fintechs, por A1-A3, dominam SERPs de PT-BR, logo são desproporcionalmente recuperadas.

**Predições observáveis distintas da camada B:**
- *(P-B1)* O canal paramétrico (B1/B2) prevê vantagem fintech **dentro de modelos sem ferramenta**. Confirmado de forma espetacular em Claude: 51,0% fintech vs 10,4% tecnologia — um gap de 40pp num modelo paramétrico. Isto é a evidência mais forte de que a vantagem fintech **não depende de RAG**; está gravada nos pesos. ChatGPT mostra padrão mais fraco (18,1 vs 20,4 — quase invertido!), o que indica que a assinatura paramétrica é **idiossincrática por laboratório**, compatível com B2 (diferentes pipelines de RLHF).
- *(P-B2)* O caso **Gemini** é diagnóstico: cita ~0% fora de fintech (4,9% fintech, 0,0% varejo, 0,7% tecnologia, 0,0% saúde). Um modelo com política de moderação que suprime nomes próprios em quase tudo, mas deixa passar fintech (ainda que baixo), sugere que a saliência paramétrica de fintech é alta o bastante para vencer um guardrail conservador. Isto separa B de A: a oferta de corpus não explica por que *o mesmo* corpus produz 0% em Gemini e 51% em Claude — a diferença está na política de treino/decodificação, não no mundo.
- *(P-B3)* O canal RAG (B3) prevê que **Perplexity comprime o gap**, porque a recuperação ao vivo nivela parcialmente verticais que têm corpus suficiente. Confirmado: em Perplexity, fintech (86,5) e varejo (92,9) e até saúde (69,8) ficam todos altos; o gap fintech-tecnologia cai para ~32pp (86,5 vs 54,3), bem menor que os 40pp paramétricos do Claude. RAG é parcialmente equalizador.

**Teste discriminante da camada B:** a variância da taxa fintech *entre modelos paramétricos* (Claude 51 vs ChatGPT 18 vs Gemini ~5 vs Groq 8,7) é o teste decisivo. Se a vantagem fosse puramente oferta de corpus (camada A operando via mundo), modelos paramétricos diferentes treinados em corpora web sobrepostos deveriam concordar mais. A enorme dispersão *entre* laboratórios, com a ordenação interna preservada (fintech ≥ outras em quase todos), indica um **componente comum de mundo (A) modulado por políticas de treino idiossincráticas (B)**. Em termos estatísticos: um modelo de efeitos com termo vertical (fixo, forte) + interação vertical×modelo (forte) — exatamente o que a matriz mostra.

### Camada C — ESTRUTURA DE MERCADO (marcas-categoria, fragmentação e cautela YMYL)

A camada C é a explicação semântica de mais alto nível: a *forma* do mercado determina se existe uma resposta canônica de uma palavra.

- **C1 — Marcas-categoria (entity salience).** Na fintech BR, há marcas que *são* a categoria na mente coletiva: Nubank ≈ banco digital; Pix ≈ pagamento instantâneo. Quando existe um mapeamento quase 1-para-1 entre uma classe de produto e um nome, o modelo tem um alvo de baixa entropia para emitir. Isto prediz **alta concentração** de citações.
- **C2 — Fragmentação em tecnologia B2B.** Tecnologia de serviço/integração é um mercado pulverizado (consultorias, ERPs, integradores), sem um campeão semântico óbvio. A entropia do "qual nome citar" é alta, e o modelo, na dúvida, ou não cita ou se espalha. Prediz **baixa concentração e baixa taxa**.
- **C3 — Cautela regulatória / YMYL em saúde.** Saúde é "Your Money or Your Life": tanto a oferta de corpus (revisão editorial, disclaimers) quanto o treino (RLHF para não dar conselho médico nomeado) empurram para respostas genéricas e hedged, sem nomear marcas específicas. Prediz **taxa baixa apesar de existirem entidades grandes (Hypera, EMS)**, com sentimento deslocado e padrão de posição distinto.

**Predições observáveis distintas da camada C — e o que os dados dizem:**

- *(P-C1) Concentração.* Fintech tem HHI=0,283 e top3=70,9% — a vertical **mais concentrada** das quatro. Confirmado. Varejo, que também tem campeões (Mercado Livre, Magazine Luiza), tem top3=69,4% mas HHI menor (0,202), porque tem dois campeões e não um. Tecnologia tem HHI=0,110 e top3=43,9% — exatamente a assinatura de fragmentação prevista por C2. Saúde fica no meio (HHI=0,154). A ordenação de concentração (fintech > varejo > saúde > tecnologia) acompanha de perto a ordenação de taxa de citação — forte evidência de que **concentração e citabilidade são duas faces da mesma estrutura de mercado**.

- *(P-C3) Sentimento e hedging.* C3 prevê que saúde, quando cita, o faz com perfil qualitativamente diferente. Confirmado de modo gritante: saúde tem **0% de citações negativas e 42,6% positivas** (vs ~25% nas outras três) e **57,4% neutras** (vs ~74% nas outras). O padrão "ou neutro factual ou explicitamente positivo, nunca negativo" é exatamente a assinatura de uma resposta YMYL curada/cautelosa: o modelo só nomeia um laboratório quando o contexto é seguro e elogioso, evitando qualquer associação negativa. O hedging textual explícito também é maior em saúde (1,0%) e tecnologia (1,0%) do que em fintech e varejo (0,3% cada).

- *(P-C3) Tercil de posição.* C3 prevê que, em saúde, a citação tende a vir cedo (quando vem, é uma resposta âncora segura) e raramente no fechamento exploratório. Confirmado: saúde T1=39,1% e T3=26,1% (mais front-loaded), e varejo ainda mais (T1=42,0%, T3=21,8%), enquanto fintech é quase uniforme (T1=35,5%, T2=30,6%, T3=33,8%). A uniformidade de posição em fintech sugere que o nome é citável em qualquer ponto do raciocínio — abertura, meio e conclusão — o que é coerente com uma entidade-categoria de altíssima saliência (C1), enquanto a concentração no T1 das outras verticais sugere citação mais "obrigatória/protocolar" do que "fluente".

- *(P-C2) Intensidade multi-entidade.* C1 (uma resposta densa em nomes quando o mercado é nomeável) prevê maior número médio de entidades por resposta em fintech/varejo. Confirmado: fintech 0,562 e varejo 0,537 entidades por resposta, contra tecnologia 0,301 e saúde 0,300 — quase o dobro. O modelo, em fintech, não só cita mais frequentemente como cita **mais nomes por vez**, sinal de um mapa mental denso e estruturado da categoria.

**Teste discriminante da camada C:** o contraste saúde-vs-resto no sentimento (0% negativo, alta positividade) é uma assinatura que **nenhuma das camadas A ou B prediz sozinha**. Oferta de corpus e frequência paramétrica explicariam uma taxa baixa em saúde, mas não explicariam *por que a baixa taxa vem acompanhada de ausência total de negatividade e mais hedging*. Esse é o impressão digital específico do mecanismo YMYL/regulatório (C3). Logo, C é necessária e não redutível a A+B.

---

## 2. Quadro-resumo: qual padrão cada mecanismo explica

| Padrão empírico | Camada A (oferta) | Camada B (treino) | Camada C (mercado) |
|---|---|---|---|
| Taxa fintech > varejo > tec ≈ saúde | parcial (mais corpus) | parcial (mais frequência) | **forte** (nomeabilidade) |
| Gap estável em 8 semanas | sim (corpus estável) | **sim** (pesos estáveis) | sim (estrutura estável) |
| Claude 51% vs tec 10% (paramétrico) | não explica a magnitude | **forte** (B1/B2) | reforça (alvo de baixa entropia) |
| Gemini ~0% fora de fintech | não | **forte** (política de treino) | reforça |
| Perplexity comprime o gap (RAG) | **forte** (B3 via A) | parcial | parcial |
| HHI/top3 fintech mais alto | parcial | não | **forte** (C1/C2) |
| Saúde 0% negativo, +hedging | não | parcial (RLHF) | **forte** (C3 YMYL) |
| 0,56 vs 0,30 entidades/resposta | parcial | não | **forte** (densidade de categoria) |
| Gap maior em inglês que PT | contra A PT-cêntrica | neutro | **a favor** (entidade global, C1) |

A leitura do quadro é inequívoca: **nenhuma camada isolada explica todos os padrões**. A camada A é necessária (sem corpus não há o que citar) mas insuficiente (não explica a variância entre modelos nem o sentimento de saúde). A camada B explica a heterogeneidade entre laboratórios e a robustez paramétrica. A camada C explica a concentração, o sentimento e a posição. O modelo parcimonioso é uma cadeia, não um vencedor único.

---

## 3. O papel do "efeito Nubank": efeito-entidade vs efeito-vertical

Esta é a ameaça mais séria à interpretação "vantagem da vertical fintech". Nubank responde por 3.533 de 7.112 menções fintech, ou **49,7%** — metade de toda a citação da vertical é uma única empresa. Surge a pergunta honesta: existe uma "vantagem fintech", ou existe uma "vantagem Nubank" que, por agregação, faz a vertical inteira parecer privilegiada?

### 3.1 A analogia das superstar firms

A literatura de organização industrial sobre *superstar firms* (Autor, Dorn, Katz, Patterson e Van Reenen, 2020) descreve setores em que uma fração desproporcional da atividade — vendas, lucro, atenção — concentra-se numa ou poucas firmas líderes, deslocando a participação do trabalho e remodelando a estrutura do setor. A citação por LLM é um análogo atencional perfeito: o "share of model" comporta-se como o "share of market" de um setor winner-take-most. Nubank é, na economia da atenção dos LLMs, a superstar firm da fintech BR — uma entidade tão saliente que arrasta a média da vertical para cima. O HHI de 0,283 é, literalmente, uma medida de concentração à la Herfindahl aplicada à atenção do modelo, e é o mais alto das quatro verticais.

Isto sugere que parte do "efeito vertical" é mecanicamente um "efeito entidade superstar". Mas a analogia também desarma a objeção: em IO, ninguém diz que "o setor de tecnologia não é dominante, é só a Apple/Google". A existência de uma superstar **é uma propriedade da estrutura do setor**, não um confound a ser removido. Que a fintech BR tenha gerado uma marca-categoria de saliência única é, em si, o mecanismo C1 — não uma alternativa a ele.

### 3.2 Teste de decomposição: vertical robusta a remover a superstar?

A questão empírica testável é: **se removermos Nubank do roster, a fintech ainda lidera?** Com Nubank fora, restam 7.112 − 3.533 = 3.579 menções fintech distribuídas entre as demais 19 entidades (PicPay 770, C6 737, Inter 558, Bradesco 438, Mercado Pago 299, Itaú 289, PagBank 160, etc.). Comparada ao top de varejo sem o líder (6.793 − 2.003 = 4.790 sem Mercado Livre, ainda com Magazine Luiza 1.961 forte), a fintech *sem* Nubank provavelmente **cai abaixo do varejo** em volume bruto de menções, mas a comparação correta não é volume e sim **taxa de citação por resposta**.

O teste discriminante limpo, que o dataset permite e que recomendamos executar na análise de robustez, é: recomputar a taxa de citação fintech **excluindo respostas cuja única entidade citada é Nubank**. Três cenários:
- *(i)* Se a taxa fintech residual cair para o nível de tecnologia (~14%), a "vantagem vertical" é majoritariamente **efeito-entidade Nubank** — um caso de superstar isolada.
- *(ii)* Se a taxa residual ficar entre varejo e tecnologia (~18-22%), há um **efeito-vertical genuíno mais fino, amplificado por uma superstar** — a hipótese mais provável dado que PicPay, C6 e Inter sozinhos somam 2.065 menções, sinal de uma cauda própria robusta.
- *(iii)* Se a taxa residual permanecer ~28%, o efeito é vertical puro e Nubank é só o representante modal.

A evidência circunstancial favorece **(ii)**: a fintech tem **20 entidades citadas** (mais que saúde, 18, e perto de tecnologia, 22) e a segunda, terceira e quarta colocadas (PicPay, C6, Inter) têm volumes que, isolados, já superam o líder de saúde fora do top (Pfizer 350) ou as posições médias de tecnologia. Existe densidade abaixo da superstar. Além disso, o padrão de **0,562 entidades por resposta** (vs 0,30 em tecnologia) não pode ser produzido por uma entidade única — citar Nubank sozinho daria no máximo ~0,28 de média; o excedente vem do reconhecimento de uma *categoria* povoada.

### 3.3 Veredito honesto

O efeito Nubank é real e grande, e seria desonesto apresentar "fintech" como uma propriedade homogênea da vertical. Mas a leitura correta, ancorada na literatura de superstar firms, é que **efeito-entidade e efeito-vertical não são rivais — são a mesma estrutura observada em dois níveis de agregação**. Nubank é alta porque a categoria "banco digital BR" é semanticamente nomeável e densa em corpus (A+C1); a categoria é nomeável porque produziu uma superstar; e a superstar é citável porque o treino converteu sua frequência em probabilidade paramétrica (B1). A recomendação metodológica para o artigo é **reportar todas as taxas com e sem Nubank** e tratar a sensibilidade dessa exclusão como uma estimativa do "componente superstar" do efeito vertical — não como uma correção que "limpa" um viés, mas como uma decomposição informativa.

---

## 4. Síntese: modelo causal em camadas

O modelo mais parcimonioso compatível com **todos** os padrões observados é uma cadeia em que o mundo (oferta de corpus) é filtrado por dois conversores parcialmente independentes (treino paramétrico e recuperação RAG) e modulado, em ambas as pontas, pela estrutura semântica do mercado (nomeabilidade + regime YMYL). A estrutura de mercado age duas vezes: a montante, determinando *quanto* corpus nomeado existe e *com que concentração*; e a jusante, determinando se o treino *permite* nomear (saúde reprimida por YMYL).

```
                         ESTRUTURA DE MERCADO (C)
                  nomeabilidade da categoria + regime YMYL
                  /  (modula a montante)        \  (modula a jusante)
                 v                                v
   [A] OFERTA DE CORPUS PT-BR  ----->  [B] CONVERSAO  ----->  TAXA DE CITACAO
   imprensa setorial (A1)              em probabilidade        observada por
   comparadores/Reclame Aqui (A2)      |                       resposta
   SEO agressivo (A3)                  +-- B1 frequencia ---> Claude 51% (paramétrico)
   docs BC/Pix/Open Finance (A4)       |   pré-treino  ------> Gemini ~0% (política reprime)
                                       |   (paramétrico)       ChatGPT 18% (RLHF idiossincr.)
                                       |
                                       +-- B2 RLHF utilidade -> fintech recompensada,
                                       |   consumidor            saúde hedged
                                       |
                                       +-- B3 recuperabilidade -> Perplexity 86% (RAG
                                           (autoridade/schema/      comprime o gap)
                                           freshness no índice)

   SUPERSTAR (Nubank, 49,7%) = manifestação de C1 dentro de A+B, não causa rival
       |
       v
   ASSINATURAS DISTINTAS:
   - concentração (HHI/top3): efeito C predominante
   - variância entre modelos: efeito B predominante
   - sentimento 0% neg em saúde: efeito C3 (YMYL) puro
   - gap em RAG comprimido: efeito B3 sobre base A
   - 0,56 vs 0,30 entidades/resp: efeito C1 (densidade de categoria)
```

**Leitura do diagrama em uma frase:** a fintech brasileira é mais citada porque produziu, num idioma e num mercado nativamente digitais, uma categoria semanticamente nomeável e densa em corpus de boa qualidade extrativa (A+C1), que o pré-treino converteu em alta probabilidade paramétrica de modo idiossincrático por laboratório (B1/B2) e que o RAG recupera com facilidade (B3), enquanto a saúde, mesmo tendo entidades grandes, é estruturalmente reprimida pelo regime YMYL no treino (C3) e a tecnologia B2B carece de uma resposta canônica por fragmentação (C2).

**A explicação mais parcimoniosa, portanto, não é monocausal.** Ela é uma cadeia de três elos em que a estrutura de mercado (C) é o organizador de mais alto nível — porque é a única camada que explica simultaneamente a *taxa*, a *concentração* e o *sentimento* — operando através da oferta de corpus (A) e dos conversores de treino/recuperação (B). O "efeito Nubank" não é um quarto mecanismo: é a sombra projetada por C1 sobre A e B quando uma categoria gera uma superstar.

### Roteiro de testes discriminantes para a seção empírica de robustez
1. **Desagregar `sources` e freshness por engine** (testa A vs B3): fintech deve dominar URLs únicas/recentes *dentro* de Perplexity.
2. **Decomposição com/sem Nubank** (testa efeito-entidade vs efeito-vertical, §3.2): reportar as quatro taxas excluindo respostas Nubank-only.
3. **Modelo de efeitos vertical + vertical×modelo** (testa B): quantificar a fração da variância explicada pela interação com o laboratório — assinatura de B sobre A.
4. **Contraste de sentimento condicional à citação** (testa C3): confirmar que a ausência de negatividade em saúde sobrevive a controles de categoria de query e modelo.
