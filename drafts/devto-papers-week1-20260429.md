---
title: "Coletei 8.571 queries em sete dias e descobri que ser citado por IA é uma métrica que não existe"
tags: ai, marketing, datascience, research
canonical_url: https://alexandrecaramaschi.com/artigos/dia-7-paper-citacao-llms-marcas-brasileiras-2026
---

Há sete dias eu liguei o cronômetro de uma janela de 90 dias. Pré-registrei a metodologia no OSF, travei a versão 2 do pipeline, e deixei a coleta rodar no automático em cinco LLMs (ChatGPT, Claude, Gemini, Groq e Perplexity), 69 entidades brasileiras (61 reais e 8 fictícias plantadas como controle), quatro verticais (Fintech, Varejo, Saúde e Tecnologia). Hoje, dia 7 de 90, já temos **8.571 queries empíricas** e **1.785 citações** no banco. E os primeiros sinais já desmontam uma premissa que circula em quase todo deck de marketing brasileiro.

O dado mais importante deste post é uma frase. **Não existe uma métrica única chamada "ser citado por IA".** Existem cinco mercados completamente diferentes acontecendo ao mesmo tempo, e a maior parte das marcas está otimizando para o errado.

## Cinco mercados, 75 vezes de diferença

A taxa de citação global, sobre 8.571 queries, é de **20,8%** (intervalo de confiança de 95%: 20,0%–21,7%). Esse número, sozinho, é inútil. Quando se decompõe por LLM:

- **Perplexity:** 82,5% de citação
- **Claude:** 26,0%
- **ChatGPT:** 17,2%
- **Groq:** 8,2%
- **Gemini:** 1,1%

**Setenta e cinco vezes de diferença** entre o melhor e o pior. Não é ruído. São 8.571 queries pareadas, com a mesma cohort, na mesma janela, com o mesmo prompt-set. O modelo com RAG ativo (Perplexity) e o modelo paramétrico puro (Gemini) são, do ponto de vista de visibilidade de marca, dois universos. Quando uma marca declara "fui citada pela IA", precisa terminar a frase: por qual.

Reportar "presença em IA" como métrica única é esconder duas ordens de grandeza atrás de uma média ponderada. Cada engine opera com pipeline diferente — recuperação ao vivo, augmentação seletiva, inferência paramétrica pura — e a barra de entrada para cada uma é radicalmente distinta.

## Três achados que estão me tirando o sono

Além do gap entre engines, três sinais preliminares já mostram que a leitura ingênua do mercado está errada em pelo menos três frentes.

**1. Vertical importa duas vezes mais do que eu esperava.** Fintech tem 28,6% de taxa de citação. Saúde tem 14,0%. Mesma metodologia, mesma janela, mesma cohort. O recall setorial dos LLMs é profundamente desigual, e o setor de saúde está órfão.

**2. Inglês cita mais do que português.** Queries em inglês geram 23,0% de citações. As mesmas queries em português, sobre as mesmas marcas, geram 18,7%. Eu esperava o oposto. O sinal prático: hoje, perguntar *"best Brazilian fintechs"* devolve mais marcas brasileiras do que perguntar "melhores fintechs brasileiras". Provavelmente envolve o volume de corpus de treinamento em inglês citando marcas brasileiras, mais do que a presença em conteúdo nativo em português.

**3. Quase ninguém fala mal.** De 3.841 contextos com sentimento classificado, 0,2% são negativos. Os LLMs raramente criticam quem citam. Qualquer dashboard tipo "share of voice em IA" mede presença, não reputação. Reputação exige outro experimento.

E ainda: **97% das menções identificadas usam o nome próprio da marca** (167 em 172 contextos auditados). Os modelos preferem citar pelo nome a inserir um link. A unidade competitiva no GEO é a entidade nomeada, não a URL.

## Por que confio nesses números aos sete dias

Resultado parcial do dia 7 que talvez seja o mais importante: **especificidade de 100,0%**. As oito entidades fictícias plantadas na cohort — nomes plausíveis em português que correspondem a empresas que não existem — receberam **zero falsos positivos** em 8.571 queries. A instrumentação está calibrada.

Para chegar aqui, eu tive que jogar fora a versão 1 desse pipeline. Em fevereiro publiquei um paper chamado **Null-Triad: Three Ways to Fail to Conclude** no Zenodo (DOI [10.5281/zenodo.19712217](https://doi.org/10.5281/zenodo.19712217)) admitindo que a primeira metodologia tinha três falhas estruturais simultâneas: poder estatístico insuficiente em H1, design que não testava o que media em H2, e um casamento de string que inflava H3. A migração para a v2 derrubou **45% das "citações"** que estávamos contando, porque eram falsos positivos do tipo "Inter" sendo capturado dentro de "international", ou "Stone" dentro de "cornerstone".

Foi humilhante e foi necessário. Publicar o Null-Triad antes de iniciar a v2 foi a forma mais honesta que encontrei de declarar publicamente: o que eu disse antes estava errado, e aqui está exatamente como.

## O que muda no pipeline v2

A versão 2 está formalizada em [METHODOLOGY_V2.md](https://github.com/alexandrebrt14-sys/papers/blob/main/docs/METHODOLOGY_V2.md) e aberta sob licença MIT em [github.com/alexandrebrt14-sys/papers](https://github.com/alexandrebrt14-sys/papers):

- **NER com word-boundary rigoroso** e normalização Unicode dupla (NFC + NFKD).
- **Dicionário canônico de aliases** (BTG ↔ BTG Pactual, XP ↔ XP Investimentos, C6 ↔ C6 Bank, Magalu ↔ Magazine Luiza).
- **Oito decoys fictícios** plantados como canários de especificidade.
- **Estimador sanduíche cluster-robust (CR1)** respeitando a estrutura de cluster diário.
- **Simulação Monte Carlo** substituindo thresholds arbitrários por percentis empíricos.
- **Correção BH-FDR** para múltiplas comparações.
- **Regra de decisão pré-registrada**: rejeito H₀ apenas se o p-valor ajustado for menor que 0,05 *e* o intervalo de 95% excluir o valor nulo.
- **Reprodutibilidade container-level**: Dockerfile com `PYTHONHASHSEED` pinado, `requirements-lock.txt` imutável, manifest SHA-256 dos outputs.

A janela vai até **21 de julho de 2026**. No **dia 25** o estudo atinge poder estatístico para H1, no **dia 38** para H2. Só vou bater no peito sobre conclusões definitivas em **outubro**, quando o paper for submetido à *Information Sciences* (Elsevier, fator de impacto 8,1). Até lá, prometo o que prometi no OSF: vou publicar também os resultados nulos, se aparecerem.

## O que já dá para usar na prática (com cautela)

- **Pare de tratar "presença em IA" como métrica única.** Reporte por modelo. Idealmente por modelo e por idioma.
- **Se você é fintech ou varejo, o jogo está aberto.** Barra de entrada estruturalmente menor — Fintech 28,6%, Varejo 25,5%.
- **Se você é saúde, o trabalho é estrutural.** Com 14,0% de taxa, ganhar visibilidade exige construção de autoridade externa em ciclo longo.
- **Se você está investindo em conteúdo só em português, está deixando dinheiro na mesa.** Conteúdo bilíngue, com base inglesa sólida, é hoje uma alavanca subestimada.
- **Não confie em dashboards que prometem "share of voice em IA" sem mostrar intervalo de confiança, tamanho de amostra e metodologia de extração.** A v1 deste mesmo estudo cometeu o erro de contar "international" como "Inter" durante meses.

## Sete dias. Mais oitenta e três pela frente

Dataset e dashboard atualizados em tempo real:

- [alexandrecaramaschi.com/research](https://alexandrecaramaschi.com/research) — números do dia, intervalos de confiança, distribuição por vertical, LLM e idioma.
- [alexandrecaramaschi.com/papers-roadmap](https://alexandrecaramaschi.com/papers-roadmap) — fases, hipóteses, venues alvo, ondas entregues.
- [github.com/alexandrebrt14-sys/papers](https://github.com/alexandrebrt14-sys/papers) — código completo, pipeline, testes, migrations, Dockerfile.

A próxima vez que alguém te disser que "a IA está citando" a sua marca, a resposta correta tem quatro componentes: **qual IA, em que idioma, em que vertical e com que intervalo de confiança**. Se faltar qualquer um dos quatro, o que está sendo medido não é visibilidade — é folclore.

---

*Alexandre Caramaschi — CEO da Brasil GEO, ex-CMO da Semantix (Nasdaq), advisor estratégico de IA da Nuvini (Nasdaq: NVNI), cofundador da AI Brasil.*
