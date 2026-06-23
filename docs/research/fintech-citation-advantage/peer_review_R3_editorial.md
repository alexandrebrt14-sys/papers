# Peer Review R3 — Meta-revisor / Editor de Venue

**Revisor 3 (editor científico de venue, ICWSM/WWW) · 11 de junho de 2026**
**Manuscrito:** *Anchor-Entity Concentration in LLM Brand Citations* (insumo consolidado)
**Material avaliado:** `DRAFT_INSUMOS_FINTECH_CITATION_ADVANTAGE.md`, `analysis_quant.md`, `red_team.md`.

Esta revisão tem duas fases. A Fase 1 traz as críticas editoriais (clareza, impacto, completude, riscos éticos e reprodutibilidade). A Fase 2 entrega o material complementar pronto para colar no manuscrito — a parte mais importante deste retorno.

---

## FASE 1 — CRÍTICAS EDITORIAIS

### (a) A história do paper está clara em uma frase?

Não, ainda não — e essa é a fragilidade editorial central. O insumo carrega **duas histórias concorrentes** no mesmo corpo: a pergunta original ("por que a fintech é mais citada?") e a tese pivotada ("a vantagem setorial é, na verdade, concentração numa entidade-âncora"). Um leitor de venue precisa entender a tese antes do fim do resumo, e hoje o documento só resolve o conflito no fim da seção 1.

A frase única que o paper deveria defender, e que recomendo adotar como espinha dorsal de abertura, abstract e conclusão:

> *A aparente vantagem setorial da fintech na citação espontânea por LLMs não é um efeito da vertical, mas a sombra de uma única entidade-âncora (Nubank): removê-la derruba a fintech de primeiro para último lugar (28,15% para 11,46%) e inverte a razão de chances ajustada (4,13 para 0,77), revelando que "vantagens setoriais" em visibilidade de LLM são, em larga medida, concentração de marca em nível de superstar, modulada pelo motor.*

Tudo no manuscrito que não serve a essa frase deve virar apêndice ou ser cortado. A pergunta original é o gancho, não a tese — e o manuscrito precisa sinalizar essa transição com clareza, não deixá-la implícita.

### (b) O que um editor de ICWSM/WWW rejeitaria de cara (riscos de desk reject)

Quatro riscos de desk reject, em ordem de letalidade:

1. **Construto medido sobre texto truncado a 200 caracteres.** Este é o risco fatal. Se um revisor de measurement percebe (e perceberá) que `cited` mede front-loading nos primeiros 200 caracteres e não citação plena, e que isso não foi resolvido por re-coleta, o paper é rejeitado sem discussão de mérito. **Não submeter antes de re-coletar com texto íntegro.** O insumo é honesto ao classificar isto como bloqueador nº 1; o editor concorda integralmente.
2. **Inferência sem clustering com p-values absurdos.** p<10⁻¹⁷⁰ sobre ~240 clusters efetivos é um sinal vermelho imediato de não-independência ignorada. Um editor de WWW measurement track devolve na triagem.
3. **FPR de decoys de 97–99% sem explicação.** Se o instrumento "encontra" marcas fictícias em 98% dos casos, a validade de construto da medida inteira está sob suspeita. Precisa de uma frase definitiva no manuscrito explicando se é por design (decoy plantado no prompt) ou bug. Hoje o próprio insumo admite não saber — isso é inadmissível em submissão.
4. **Mistura de RAG e paramétrico como número-título.** Reportar 28,15% misturando Perplexity (RAG, satura em 86–93%) com modelos paramétricos é incoerência de construto que um revisor competente sinaliza de imediato.

Os três primeiros são bloqueio absoluto; o quarto é corrigível por reframing e estratificação.

### (c) Figuras e tabelas — o que falta para a narrativa visual

O insumo tem tabelas em excesso e figuras em falta. Um paper de measurement vende-se por figuras, não por tabelas densas. Faltam, em ordem de prioridade narrativa: (1) a figura do leave-one-out que mostra o ranking invertendo; (2) o forest plot da inversão de OR (4,13 para 0,77); (3) o small-multiples da heterogeneidade por engine. As seis figuras estão especificadas integralmente na Fase 2 (item 4). Tabelas 3.4, 3.8 e 3.9 podem migrar para apêndice; ficam no corpo apenas 3.1, 3.5 (HHI) e 3.6 (LOO).

### (d) O abstract candidato vende o achado certo?

O abstract do insumo (§9.3) é tecnicamente sólido e já vende a tese pivotada — é raro um abstract tão honesto. Dois ajustes: ele enterra a frase-tese no meio e gasta a abertura com generalidades sobre "canal de visibilidade econômica". A versão revisada na Fase 2 (item 2) puxa o número-choque (49,7% / inversão de ranking) para mais cedo e adiciona a ressalva de tier econômico e a natureza interina dos dados, que o revisor de measurement exigirá. Vende o achado de medição (não a falsa vantagem setorial), que é o achado certo e mais publicável.

### (e) Riscos éticos e legais de publicar ranking de marcas reais brasileiras (Nubank, Itaú etc.)

Risco real e endereçável. Publicar que "Nubank domina a atenção dos LLMs" ou que a saúde tem "0% de citações negativas" tem implicações reputacionais e potencialmente concorrenciais. Mitigações que o editor exige no manuscrito:

- **Enquadramento como medição observacional, não auditoria de qualidade.** O paper mede frequência de menção espontânea, não recomenda marcas nem afere mérito. Declarar explicitamente que alta citação não implica superioridade do produto nem endosso, e que baixa citação não implica deficiência.
- **Sem dados proprietários nem MNPI.** Toda entidade é nomeada apenas por aparecer em saída pública de LLM; nenhum dado interno de empresa é usado. Declarar isso.
- **Atribuição ao modelo, não à marca.** O viés medido é propriedade dos LLMs e do corpus de treino, não conduta das empresas. A redação deve sempre dizer "o modelo X cita Nubank", nunca "Nubank é mais citável por ser melhor".
- **Conformidade com LGPD irrelevante (pessoas jurídicas, dado público), mas declarar.** Não há dado pessoal; marcas são pessoas jurídicas e as menções vêm de saída pública. Uma frase de ethics statement basta.
- **Direito de resposta factual.** Disponibilizar o protocolo e o dataset permite que qualquer marca reproduza e conteste — o que neutraliza alegação de arbitrariedade.
- **Anonimização é contraproducente.** Anonimizar marcas destruiria a contribuição (o caso Nubank É o paper) e não reduz risco real, pois a tese é sobre o mecanismo, favorável a todas. Recomendo nomear, com o ethics statement acima.

### (f) Reprodutibilidade — o que falta no pacote

O pacote está a meio caminho. Faltam, de forma bloqueante: (1) os **manifests SHA-256** do `papers.db` congelado, dos scripts e do dump público (citados como [A PRODUZIR]); (2) o **dataset público versionado** (Zenodo/DOI) com dicionário de dados; (3) o **codebook do NER** (tabela de aliases por vertical, regras de folding, critério de desambiguação) — sem ele, a assimetria de alias (saúde 991 vs tecnologia 4) não é auditável; (4) o **protocolo de seleção do roster** (como as 19/15 marcas foram escolhidas — hoje não cego nem pré-registrado); (5) o **environment lock** (versões de Python/libs dos scripts de stats). O checklist completo está na Fase 2 (item 6).

---

## FASE 2 — MATERIAL COMPLEMENTAR PRONTO PARA USO

### (1) Narrativa de abertura da Introdução (PT-BR, para o draft, ~4 parágrafos)

> A citação espontânea de marcas nas respostas de grandes modelos de linguagem tornou-se um canal econômico de visibilidade comparável ao que a busca orgânica representou nas duas décadas anteriores. Quando um usuário pergunta a um LLM qual é o melhor banco digital do Brasil e o modelo responde nomeando uma instituição, sem que o usuário tenha citado nenhuma marca, essa menção carrega valor de mercado real: molda percepção, dirige consideração de compra e, no limite, redistribui demanda. Medir quem é citado, com que frequência e por quê, deixou de ser curiosidade acadêmica e passou a ser uma questão de estrutura de mercado. Nosso ponto de partida foi um fenômeno aparentemente setorial: numa janela longitudinal de coleta sobre cinco LLMs e quatro verticais do mercado brasileiro, a vertical fintech exibia a maior taxa de citação espontânea, 28,15%, à frente de varejo (24,94%), tecnologia (14,50%) e saúde (13,35%). A leitura natural — e a hipótese com que começamos — era de que a fintech possui propriedades estruturais (densidade de corpus digital, marcas-categoria, agressividade de conteúdo) que a tornam sistematicamente mais visível aos modelos.

> Esta hipótese não sobrevive à decomposição dos próprios dados. Quando desagregamos as menções da fintech por entidade, uma única marca explica quase metade de tudo: o Nubank responde por 49,68% de todas as menções de fintech, e 59,31% das respostas com citação na vertical citam exclusivamente o Nubank. O teste decisivo é o leave-one-out: ao recodificar como não-citada toda resposta de fintech cuja única entidade mencionada é o Nubank, a taxa da vertical desaba de 28,15% para 11,46% — o último lugar entre as quatro verticais, atrás inclusive de saúde — e a razão de chances ajustada da fintech contra a saúde inverte de 4,13 para 0,77. A "vantagem setorial" não sobrevive à remoção de uma marca. Ela nunca foi setorial: era a sombra de uma entidade.

> O fenômeno se reproduz, em menor magnitude, em todas as verticais, e é por isso que ele é a tese e não um defeito do caso fintech. A visibilidade de uma vertical em LLMs é governada menos por propriedades difusas do setor e mais pela existência, ou não, de uma entidade-âncora: uma marca que se tornou quase sinônimo de sua categoria ("Nubank" ≈ banco digital, como "Pix" ≈ pagamento instantâneo), e cuja saliência no corpus de treino foi convertida em probabilidade paramétrica de menção. A concentração de citação por entidade, medida por um índice de Herfindahl aplicado à atenção do modelo — um *share of model* análogo ao *share of market* —, acompanha de perto a taxa de citação entre verticais (fintech HHI=0,283, a mais concentrada e a de maior taxa; tecnologia HHI=0,110, a mais fragmentada e de menor taxa). Concentração e citabilidade são duas faces da mesma estrutura de mercado, lidas em dois níveis de agregação: a entidade e a categoria.

> A contribuição deste artigo é, portanto, deslocar o objeto de análise da vertical para a entidade-âncora, e mostrar que o que se costuma chamar de "vantagem setorial" em visibilidade de LLM é, em larga medida, concentração de marca em nível de superstar, fortemente modulada pelo motor — apenas dois de cinco engines sustentam sequer a direção do efeito agregado, que é em grande parte uma idiossincrasia de um único modelo. Ao longo do caminho, documentamos as ameaças de medição que qualquer auditoria de citação de LLM enfrenta — front-loading versus citação plena, assimetria de aliases entre verticais, especificidade do detector — e oferecemos um protocolo reprodutível, com dataset público, para um mercado emergente não-anglófono ainda ausente dessa literatura. O fenômeno fintech/Nubank deixa de ser a tese e passa a ser o caso central que a demonstra.

### (2) Abstract revisado (EN, ~250 palavras)

> Spontaneous brand mentions in large language model (LLM) outputs are an emerging channel of economic visibility, yet systematic, longitudinal, and calibrated measurement remains scarce, especially outside English-language markets. We report an interim 50-day audit (April–June 2026) of spontaneous brand citation across five economy-tier LLMs (GPT-4o-mini, Claude Haiku-4.5, Gemini-2.5-pro, Perplexity sonar, Llama-3.3-70B) for four Brazilian verticals (fintech, retail, technology, healthcare), using 48 structurally paired prompts per vertical in Portuguese and English and per-entity NER over a 127-entity cohort with fictitious decoys. Naively, fintech leads spontaneous citation (28.2% vs 24.9% / 14.5% / 13.3%). We show this aggregate advantage is not a diffuse sectoral effect but is dominated by a single anchor entity: Nubank accounts for 49.7% of fintech mentions, and 59.3% of fintech citations name Nubank exclusively. A leave-one-out recoding drops fintech to 11.5% — last place — and inverts its adjusted odds ratio from 4.13 to 0.77. The effect is also engine-driven: only two of five engines place fintech above retail, and the aggregate gap is largely a Claude-Haiku idiosyncrasy. Citation concentration (Herfindahl index) tracks citation rate across verticals, consistent with a market-structure account in which nameable category brands behave as attentional superstar firms — a *share of model* analogous to share of market. We document measurement threats — 200-character response truncation in four engines (capturing front-loading rather than full citation) and a 97–99% decoy false-positive rate — and specify the recollection and clustered-inference protocol required for confirmatory claims. Our contribution is a reproducible anchor-entity framework for sectoral LLM citation bias in a non-Anglophone market.

### (3) Cover letter (EN, ~200 palavras)

> Dear Program Chairs,
>
> We submit *Anchor-Entity Concentration in LLM Brand Citations* for consideration at [VENUE]. The paper began as an investigation into an apparent sectoral citation advantage — Brazilian fintech brands appeared most cited by LLMs — and arrived at a more durable and, we believe, more interesting finding: the advantage is not sectoral at all. It is the shadow of a single anchor entity. Removing one brand (Nubank) drops the vertical from first to last place and inverts its adjusted odds ratio from 4.13 to 0.77.
>
> We think this matters to the [VENUE] community for three reasons. First, it reframes "sectoral bias" in LLM visibility as anchor-entity concentration — a *share-of-model* analogue to market concentration, measurable with a Herfindahl index. Second, it is the first longitudinal, multi-engine audit of spontaneous commercial-entity citation in a non-Anglophone emerging market, with paired prompts, decoys, and a public dataset. Third, it is candid about measurement: we surface and quantify the construct-validity threats (front-loading from response truncation, decoy specificity, engine heterogeneity) that any citation audit must confront, and we ship a reproducibility package.
>
> The work is observational and explicitly scoped to economy-tier models. We declare all data as interim pending window close. We have no competing interests and name no brand evaluatively.
>
> Sincerely, The Authors

### (4) Descrição exata das 6 figuras principais

**Figura 1 — Taxa de citação por vertical, original vs leave-one-out (a figura-tese).**
Gráfico de barras agrupadas. Eixo X: as quatro verticais (fintech, varejo, tecnologia, saúde). Eixo Y: taxa de citação espontânea (%), 0–30%. Duas barras por vertical: clara = `cited_v2` original; escura = `cited_loo` (sem âncora). Barras de erro = IC95 Wilson. Anotação destacando a fintech: 28,15% → 11,46%, com seta indicando a queda de 1º para último lugar. **Mensagem:** a remoção da âncora colapsa e inverte o ranking — só na fintech a queda é dramática.

**Figura 2 — Forest plot da inversão de OR (fintech vs saúde, ajustada).**
Forest plot horizontal. Eixo X: razão de chances em escala log, com linha de referência em 1,0. Dois pontos com IC95: OR original = 4,13 (3,81–4,47), claramente à direita de 1; OR sob LOO = 0,77 (0,70–0,84), à esquerda de 1. **Mensagem:** o efeito não só encolhe — cruza a linha de nulidade e inverte de sinal. É a prova estatística da frase-tese.

**Figura 3 — Heterogeneidade por engine (small multiples).**
Painel de cinco mini-gráficos, um por engine (ChatGPT, Claude, Gemini, Groq, Perplexity), cada um com barras de fintech vs varejo. Eixo Y comum (0–100%). Cor verde quando fintech > varejo, vermelho quando fintech < varejo. Visualmente: só Claude (+20,3) e Gemini (+4,9, marcado com asterisco de "artefato de truncamento") são verdes; ChatGPT, Groq e Perplexity são vermelhos. **Mensagem:** o "efeito setorial" não é consistente entre engines — só 2 de 5 o sustentam.

**Figura 4 — Concentração (HHI) vs taxa de citação, por vertical (scatter).**
Dispersão. Eixo X: HHI da vertical (0,11–0,283). Eixo Y: taxa de citação (%). Quatro pontos rotulados (fintech, varejo, saúde, tecnologia) com linha de tendência. Tamanho do ponto proporcional ao número de menções. **Mensagem:** concentração e citabilidade são correlacionadas — a vertical mais concentrada (fintech) é a mais citada; a mais fragmentada (tecnologia) é a menos citada. *Share of model* segue *share of market*.

**Figura 5 — Decomposição do gap fintech−varejo por engine (waterfall/barras divergentes).**
Gráfico de barras divergentes em torno de zero. Eixo Y: engines. Eixo X: excesso de respostas citadas (fintech menos varejo), de −150 a +600. Barras: Claude +574, Gemini +134 (hachurada, "artefato"), ChatGPT −117, Perplexity −91, Groq −93. **Mensagem:** a vantagem agregada vem quase inteira de um engine (Claude Haiku) mais um artefato (Gemini), contra três engines que apontam ao contrário.

**Figura 6 — A ameaça de medição: distribuição de comprimento de resposta por engine.**
Gráfico de densidade ou boxplot. Eixo X: `LENGTH(response_text)` em caracteres (0–2500). Eixo Y: densidade. Cinco distribuições: ChatGPT, Claude, Gemini colapsadas numa linha vertical em exatos 200 chars (100% truncadas); Perplexity espalhada de 198 a 2502. Inset com a amostra real do Gemini cortada em "volume de v[endas]". **Mensagem:** o que medimos como "citação" é, em 4 de 5 engines, front-loading nos primeiros 200 caracteres — não citação plena. Justifica a re-coleta e a interpretação cautelosa de toda taxa absoluta.

### (5) Implicações práticas para GEO (Generative Engine Optimization)

**Para marcas individuais:**
- **A âncora é o ativo.** Em cada categoria, a primeira marca a se tornar sinônimo da categoria captura uma fração desproporcional da atenção do modelo (Nubank: 49,68% das menções de fintech; 59,31% das respostas a citam sozinha). O objetivo de GEO não é "aparecer", é tornar-se a entidade-categoria — o nome que o modelo emite por padrão quando a categoria é evocada.
- **O motor importa mais que o setor.** Como o efeito é fortemente heterogêneo por engine, uma estratégia de GEO não pode ser única: a marca precisa medir sua visibilidade engine por engine. Um forte desempenho em Claude não se traduz em ChatGPT ou Perplexity.
- **Front-loading é real.** Mesmo descontado o artefato de truncamento, ser nomeado cedo na resposta é um ativo — a saúde, mais front-loaded e hedged, e a fintech, citável em qualquer posição, mostram que a posição da menção é uma dimensão otimizável.
- **Densidade de cauda protege a categoria.** A fintech tem cauda própria robusta (PicPay, C6, Inter, somando ~2.065 menções) — marcas não-âncora ainda capturam atenção significativa. Construir presença em corpus PT-BR de alta cadência (imprensa especializada, comparadores, documentação institucional) é a alavanca da camada de oferta.

**Para o mercado brasileiro e o ecossistema GEO:**
- **A oportunidade está nas categorias fragmentadas.** Tecnologia B2B (HHI=0,110) não tem âncora consolidada — é onde uma marca ainda pode se tornar a entidade-categoria com investimento dirigido em corpus. Categorias já ancoradas (fintech) são defesa para o líder, ataque difícil para os demais.
- **Mercado não-anglófono é subexplorado e o gap em inglês é maior.** O efeito da âncora é maior em prompts em inglês (gap de 20 pp vs 13 pp em PT), favorecendo a entidade global. Marcas brasileiras com ambição internacional devem cuidar de sua presença em corpus anglófono, não só local.
- **Medição honesta é vantagem competitiva.** O setor de GEO tende a vender "vantagens setoriais" e taxas absolutas. Este estudo mostra que tais números são frágeis a uma única entidade e a artefatos de medição. Um programa de GEO sério mede *share of model* por entidade e por engine, reporta com e sem a âncora, e separa RAG de paramétrico — exatamente como o protocolo deste paper recomenda.
- **YMYL muda o jogo em saúde.** Em saúde, o RLHF empurra para respostas genéricas e hedged (0% de menções negativas, mais hedging); GEO em saúde compete não por saliência de marca, mas por ser a fonte institucional citável que sobrevive ao guardrail de cautela.

### (6) Checklist final de submissão

**Bloqueadores de medição (resolver antes de qualquer submissão):**
- [ ] Re-coletar com `response_text` íntegro (remover corte de 200 chars) e re-rodar NER v2; validar `MAX(LENGTH) > 200` em todos os engines; reportar como a taxa muda.
- [ ] Auditar e explicar definitivamente o FPR de decoys (97–99%): documentar se é por design (decoy plantado no prompt) ou bug; corrigir a especificidade se for bug.
- [ ] Decidir sobre o Gemini: remover da análise principal ou re-coletar (zeros são artefato de truncamento + preâmbulo).

**Inferência estatística:**
- [ ] GLMM logístico com interceptos aleatórios (query, dia, engine) e desfecho duplo (`cited_v2` e `cited_loo`); reportar OR com IC95 robustos.
- [ ] Correção de múltiplas comparações (Holm/FDR) sobre as 108 células e os testes par-a-par.
- [ ] Bootstrap por cluster de query como robustez; análise de poder no nível de cluster (~240), não de observação.
- [ ] Leave-one-entity-out para as quatro verticais (não só Nubank: Mercado Livre/Magalu, Totvs, Hypera/EMS).
- [ ] Roster de tamanho fixo (15) por bootstrap; matching estrito vs alias lado a lado.

**Reprodutibilidade e artefatos:**
- [ ] Manifests SHA-256 do `papers.db` congelado, scripts e dump público.
- [ ] Dataset público versionado (Zenodo/DOI) com dicionário de dados.
- [ ] Codebook do NER: tabela de aliases por vertical, regras de folding, critério de desambiguação.
- [ ] Protocolo de seleção do roster documentado (idealmente pré-registrado).
- [ ] Environment lock dos scripts de análise (versões de libs).

**Enquadramento e claims:**
- [ ] Frase-tese (âncora, não vertical) no título, abstract e conclusão; coerência das duas histórias resolvida na abertura.
- [ ] Nunca reportar a média RAG+paramétrico como número-título; sempre separar Perplexity.
- [ ] Restringir explicitamente a claim a "modelos de tier econômico" e declarar `model_version` exatas.
- [ ] Declarar os dados como interinos (janela dia 50/90) até o fechamento (~21/jul/2026).
- [ ] Verificar todas as entradas [A VERIFICAR] da literatura (correntes 3, 5, 6, 7, 8); dar mais peso à corrente 4 (popularidade/saliência/superstar).

**Ética e legal:**
- [ ] Ethics statement: medição observacional, sem juízo de mérito de marca; sem dado pessoal (LGPD); viés atribuído ao modelo, não às empresas.
- [ ] Declaração de ausência de conflito de interesse e de dados proprietários/MNPI.
- [ ] Dataset e protocolo públicos como direito de resposta factual.

**Figuras e tabelas:**
- [ ] Seis figuras principais conforme item 4; tabelas 3.4/3.8/3.9 para apêndice; corpo retém 3.1, 3.5, 3.6.

---

*Fim do peer review R3. Veredito editorial: a tese pivotada (concentração de entidade-âncora + heterogeneidade por engine + lições de medição) é publicável em ICWSM ou WWW measurement track APÓS resolver os três bloqueadores de medição e a inferência com clustering. A versão "vantagem setorial sistemática de fintech" seria desk-rejected. Recomendação: major revision rumo à submissão, com a Semana 1 do roadmap como pré-condição inegociável.*
