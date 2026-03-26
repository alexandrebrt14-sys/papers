# Painel de Revisao Estatistica — GEO Papers Research

**Projeto:** Pesquisa empirica multi-vertical sobre citacoes de empresas brasileiras em LLMs
**Autor:** Alexandre Caramaschi (Brasil GEO)
**Dataset:** 397 observacoes, 4 modelos, 4 verticais, 69 entidades
**Data da revisao:** 26 de marco de 2026

---

## 1. Michael I. Jordan (UC Berkeley) — Inferencia Bayesiana e Fundamentos de ML

### Critica principal: Ausencia de modelagem probabilistica

O framework atual trata citacao como variavel binaria deterministica (cited=0/1) e aplica testes frequentistas diretamente. Isso ignora a natureza estocastica dos LLMs. Uma mesma query ao mesmo modelo pode produzir respostas diferentes dependendo da temperatura, do estado do cache de contexto, e de atualizacoes silenciosas do modelo.

**Problema especifico:** O pipeline envia cada query uma unica vez por modelo e trata o resultado como verdade deterministica. Com N=397 observacoes, ha 47 queries unicas distribuidas entre 4 modelos e 4 verticais. Isso produz, em media, ~2 observacoes por celula (query x modelo), insuficiente para estimar a variancia intrinseca da resposta.

**Recomendacao:**
- Implementar coleta repetida: cada query deve ser enviada k >= 3 vezes ao mesmo modelo (com temperatura > 0) para estimar a probabilidade de citacao P(cited | query, model), nao apenas um ponto binario.
- Adotar um modelo hierarquico bayesiano: P(cited) ~ Beta(alpha, beta) por entidade, com priors informativos por vertical. Isso permitiria shrinkage entre entidades com pouca evidencia (como Gemini com N=3) e produziria intervalos crediveis ao inves de p-values pontuais.
- O pseudo R-squared de McFadden da regressao logistica (implementada em `statistical.py`) e um diagnostico pobre para modelos com alta desproporacao de classes. Com taxa de citacao de 41.6%, o modelo logistico pode ter boa calibracao aparente sem poder discriminativo real.

### Veredicto
> "Voce esta tratando um processo generativo estocastico como se fosse uma medicao deterministica. O bootstrap ajuda, mas nao substitui uma modelagem generativa adequada. Sem replicacoes por query, seus intervalos de confianca sao ficticios."

---

## 2. David Donoho (Stanford) — Ciencia de Dados e Rigor Teorico

### Critica principal: Confusao entre exploracao e confirmacao

O projeto mistura dois modos de pesquisa sem demarcacao clara:

1. **Exploracao:** Descobrir quais fatores afetam citacao (query category, modelo, vertical)
2. **Confirmacao:** Testar hipoteses pre-registradas com poder estatistico adequado

O dashboard apresenta resultados exploratorios (Kruskal-Wallis p=0.022) como se fossem confirmativos. A tabela `hypotheses` no banco esta vazia — nenhuma hipotese foi pre-registrada antes da coleta.

**Problema especifico da multiplicidade:**
- 20 categorias de query distintas, com taxas variando de 0% (`academic`) a 100% (`fintech_trust`, `confianca`)
- Queries como "fintech_trust" (100% citacao, N=45) e "academic" (0%, N=34) nao estao testando citacao espontanea — estao testando se o LLM responde ao que lhe foi perguntado
- Se voce perguntar "Quais sao os melhores bancos digitais do Brasil?", a taxa de citacao de bancos brasileiros sera trivialmente alta. O design experimental confunde a variavel de tratamento (tipo de query) com o desfecho (citacao)

**Recomendacao:**
- Separar rigorosamente queries "diretivas" (que mencionam o setor explicitamente) de queries "neutras" (conceituais, onde citacao seria espontanea)
- Pre-registrar hipoteses ANTES das proximas coletas, usando a tabela `hypotheses` ja disponivel no schema
- Aplicar Benjamini-Hochberg (ja implementado no codigo, mas nunca usado no dashboard) para todas as comparacoes multiplas
- Calcular poder estatistico a priori: para detectar effect size d=0.3 (pequeno-medio) com alpha=0.05 e power=0.80, sao necessarios N >= 176 por grupo. O Gemini com N=3 nao tem poder para detectar nenhum efeito

### Veredicto
> "O manifesto da ciencia de dados e claro: rigor requer separar exploracao de confirmacao. Voce tem um excelente framework exploratorio, mas nenhuma hipotese pre-registrada. Antes de publicar, cristalize suas hipoteses e colete dados frescos para testa-las."

---

## 3. Xiao-Li Meng (Harvard) — Vieses em Dados Massivos

### Critica principal: O data defect index (ddi) e catastrofico

Meng demonstrou que um dataset enviesado de 2.3 milhoes pode ser menos confiavel que uma amostra aleatoria de 400. O conceito-chave e o "data defect index" (ddi): a correlacao entre o mecanismo de selecao e a variavel de interesse.

Neste estudo, o ddi e alto por multiplas razoes:

1. **Vies de selecao nas queries:** As queries foram escritas pelo pesquisador, nao amostradas de um universo definido de buscas reais. Queries como "melhores bancos digitais do Brasil 2026" sao altamente conducentes a citacao. O universo real de perguntas que usuarios fazem a LLMs inclui bilhoes de queries onde empresas brasileiras nunca seriam mencionadas.

2. **Vies de deteccao:** O sistema usa regex word-boundary para detectar citacao. Entidades com nomes ambiguos ("Neon", "Stone", "99") podem gerar falsos positivos ou falsos negativos. As entidades ficticias (Banco Floresta Digital, etc.) existem no cohort mas nunca foram incluidas nas queries — o controle de falsos positivos esta completamente inoperante.

3. **Vies temporal:** 351 de 397 observacoes (88.4%) vem de um unico dia (24/mar). Apenas 46 observacoes sao do segundo dia (26/mar, com apenas 3 modelos). A "taxa de citacao de 41.6%" e essencialmente uma fotografia de um unico dia, nao uma tendencia.

4. **Cache como confundidor:** 54.4% das observacoes sao cache hits (latencia=0 ou NULL). Se o cache retorna a mesma resposta da primeira query, essas observacoes nao sao independentes — sao duplicatas. O N efetivo pode ser ~181, nao 397.

**Recomendacao:**
- Calcular e reportar o N efetivo: descontar cache hits que retornaram respostas identicas
- Incluir queries-controle negativas ("qual e a capital da Franca?") para calibrar a taxa base de citacao espuria
- Reportar o ddi estimado: proporcao de queries no dataset que representam queries reais vs. queries artificiais conducentes

### Veredicto
> "Seus 397 registros nao sao 397 observacoes independentes. Com 54% de cache hits e 88% dos dados de um unico dia, o N efetivo e dramaticamente menor. O intervalo de confianca real da sua taxa de citacao e muito mais largo do que qualquer teste frequentista vai lhe dizer."

---

## 4. Andrew Gelman (Columbia) — Modelagem Bayesiana e Critica de P-values

### Critica principal: Garden of forking paths

O resultado mais proeminente no dashboard (Kruskal-Wallis p=0.022, eta2=0.079) sofre de multiplos problemas:

1. **Efeito minusculo:** eta2=0.079 classifica como "efeito pequeno" (0.06-0.14). Em termos praticos, o modelo LLM usado explica apenas 7.9% da variancia nas taxas de citacao. Os outros 92.1% sao query, entidade, e ruido.

2. **Flexibilidade analitica nao reportada:** O pipeline implementa 7 testes estatisticos diferentes. Quantos foram rodados antes de reportar o Kruskal-Wallis como "significativo"? Se o ANOVA parametrico desse p > 0.05, o pesquisador teria parado ou tentado o teste nao-parametrico? Isso e o classico "garden of forking paths".

3. **Dicotomizacao de p-values:** O codigo classifica resultados como `significant = p < 0.05` (booleano). Gelman argumenta consistentemente contra essa pratica. Um p=0.049 nao e qualitativamente diferente de p=0.051.

4. **Intervalos de confianca ausentes nas metricas-chave:** A visualization.py implementa IC de 95% (SEM * 1.96) nos graficos, mas o dashboard HTML nao mostra nenhum intervalo. Taxas de citacao sao reportadas como pontos fixos ("54.0%", "13.3%") sem indicacao de incerteza.

**Recomendacao:**
- Nunca usar "significativo/nao significativo" como dicotomia. Reportar p-value, effect size, e IC simultaneamente
- Adotar abordagem bayesiana: posterior P(taxa_citacao | dados) com prior Beta(1,1) fornece intervalos crediveis honestos
- Para Gemini com 4/30 citacoes: IC bayesiano 95% e [4.5%, 30.4%], nao o ponto fixo de 13.3%
- Para Sonar com 61/113: IC bayesiano 95% e [44.5%, 63.3%]
- Essas faixas se sobrepoem massivamente — a "diferenca significativa" entre modelos e muito mais incerta do que o p=0.022 sugere

### Veredicto
> "Type M error: seu efeito provavelmente esta inflado. Type S error: pode nem estar na direcao certa para Gemini com N=30. Pare de dicotomizar p-values e comece a reportar incertezas honestas."

---

## 5. Grace Wahba (Wisconsin-Madison) — Smoothing e Dados Funcionais

### Critica principal: Dados longitudinais tratados como cross-section

O projeto promete "serie temporal de 6-12 meses" mas trata os dados atuais como uma cross-section estatica. Com apenas 2 dias de coleta (e 88% concentrado em um unico dia), nao ha estrutura temporal para analisar.

**Problema especifico:** A tabela `daily_snapshots` existe no schema mas depende de coletas diarias consistentes. Sem smoothing temporal, qualquer tendencia aparente sera dominada por ruido day-to-day (atualizacoes de modelo, variacao de servidor, etc.).

**Recomendacao:**
- Quando houver >= 14 dias de dados, aplicar smoothing spline (B-spline com penalizacao) para estimar tendencias de citacao por entidade
- Usar cross-validation leave-one-out para selecionar o parametro de suavizacao
- Nao reportar tendencias com < 30 dias de dados — a volatilidade de curto prazo dos LLMs e alta

### Veredicto
> "Voce projetou uma infraestrutura para analise longitudinal, mas esta tentando tirar conclusoes de uma cross-section. Espere. Colete. Suavize. So entao interprete."

---

## 6. Bradley Efron (Stanford) — Bootstrap e Validacao

### Critica principal: Nenhuma validacao de robustez

O bootstrap (inventado por Efron) e mencionado conceptualmente mas nunca implementado no codigo. Os testes parametricos assumem propriedades distribucionais que nao foram verificadas.

**Problemas especificos:**
- A taxa de citacao geral (41.6%) e calculada sem qualquer indicacao de variabilidade. Um bootstrap com B=10.000 reamostras forneceria o IC empirico sem suposicoes distribucionais
- O Cramer's V e o eta-squared reportados sao estimativas pontuais sem IC
- A regressao logistica usa MLE (statsmodels Logit) sem cross-validation — o pseudo R-squared reportado sera otimistamente enviesado

**Recomendacao:**
- Implementar bootstrap para todas as metricas-chave (taxa de citacao, effect sizes, rankings de entidade)
- Usar k-fold cross-validation (k=5) para a regressao logistica, reportando AUC medio em vez de pseudo R-squared no conjunto de treinamento
- Para o ranking de entidades: bootstrap o ranking e reporte a mediana com IC do rank. "Nubank e #1" pode ser instavel — com N=172 contextos, a diferenca entre #1 e #2 pode nao ser robusta

### Veredicto
> "Seus testes estao todos no modo plug-in: calcula a estatistica, aplica a formula assintotica, reporta o p-value. Com N < 400 e distribuicoes assimetricas, o bootstrap seria muito mais honesto."

---

## 7. Terence Tao (UCLA) — Rigor Matematico e Escala

### Critica principal: A matematica dos LLMs invalida pressupostos classicos

Os testes estatisticos implementados (chi-squared, ANOVA, Mann-Whitney) assumem que as observacoes sao identicamente distribuidas. Mas LLMs nao sao processos estacionarios:

1. **Non-stationarity:** OpenAI, Anthropic e Google atualizam modelos sem aviso. O modelo "gpt-4o-mini-2024-07-18" de hoje pode ter comportamento diferente amanha, mesmo com o mesmo ID. A tabela `model_versions` existe mas esta vazia.

2. **Dependencia entre observacoes:** Se 3 queries diferentes sobre "bancos digitais no Brasil" sao enviadas ao mesmo modelo na mesma sessao, as respostas nao sao independentes — compartilham o mesmo contexto de sistema, a mesma amostragem de temperatura, e possivelmente o mesmo estado de KV-cache do lado do provedor.

3. **Problema de dimensionalidade:** Com 69 entidades, 4 modelos, 4 verticais, 47 queries, e multiplas categorias, o espaco de comparacoes possiveis e combinatorio. O teste Kruskal-Wallis com 4 grupos e um corte unidimensional de um espaco muito maior. Efeitos de interacao (modelo x vertical x query_category) sao provavelmente mais informativos que efeitos principais.

**Recomendacao:**
- Implementar model version tracking: hash das primeiras 100 respostas a um set de queries canonicas, salvar em `model_versions`. Qualquer mudanca de hash invalida comparacoes temporais
- Testar interacoes: ANOVA two-way (modelo x vertical) antes de reportar efeitos principais
- Para publicacao em venue de alta qualidade (SIGIR/WWW), considerar mixed-effects models onde query e random effect e modelo/vertical sao fixed effects

### Veredicto
> "A beleza do seu projeto esta na escala e sistematizacao. Mas LLMs nao sao dados experimentais — sao oraculados estocasticos nao-estacionarios. Seus testes frequentistas assumem um mundo mais simples do que o que voce esta medindo."

---

## Sintese do Painel

### O que esta BEM:
1. Framework de coleta automatizado e reprodutivel (GitHub Actions, CLI, DB)
2. Variedade de testes estatisticos com effect sizes (nao apenas p-values)
3. Correcao para multiplicidade implementada (Bonferroni + BH FDR)
4. Entidades ficticias para calibracao (design correto, falta execucao)
5. Schema preparado para pre-registro de hipoteses
6. FinOps com budget control (responsabilidade fiscal na pesquisa)

### O que precisa CORRECAO IMEDIATA:
1. **N efetivo:** Descontar cache hits e reportar N_eff, nao N bruto
2. **Entidades ficticias:** Ativar nas queries para calibracao de falsos positivos
3. **Separacao de queries:** Diretivas vs. neutras — nao misturar "melhores bancos" com "o que e machine learning"
4. **Intervalos de confianca:** Em toda metrica publica
5. **Pre-registro:** Preencher tabela `hypotheses` ANTES da proxima coleta

### O que precisa REDESIGN para publicacao:
1. Replicacoes por query (k >= 3) para estimar variancia intrinseca
2. Modelo hierarquico bayesiano (entidade nested in vertical, crossed with model)
3. Mixed-effects model como analise principal (query como random effect)
4. Cross-validation para regressao logistica
5. Bootstrap para rankings e metricas-chave
6. Model version tracking ativo

### Estimativa de readiness para submissao:

| Paper | Venue | Readiness | Bloqueador principal |
|-------|-------|-----------|---------------------|
| Paper 1 (ArXiv) | ArXiv preprint | 5% | N insuficiente (397/25.920), sem replicacoes, sem pre-registro |
| Paper 2 (SIGIR) | SIGIR/WWW | 1% | Zero dados SERP, BRAVE_API_KEY ausente |
| Paper 3 (Info Sci) | Information Sciences Q1 | 3% | Sem A/B experiments, entidades ficticias inoperantes, Gemini sub-amostrado |

**Conclusao consensual do painel:** A infraestrutura e excelente. A coleta precisa de 60-90 dias adicionais com as correcoes implementadas. Nenhum resultado atual deve ser publicado como confirmatorio — todos sao exploratoros e preliminares. O caminho para publicacao e viavel, mas requer disciplina metodologica nos proximos 3 meses.

---

*Documento gerado em 26/03/2026 — Brasil GEO Research*
*Baseado na metodologia de: Jordan (Bayesian ML), Donoho (Data Science), Meng (Data Defect), Gelman (Bayesian Critique), Wahba (Smoothing), Efron (Bootstrap), Tao (Mathematical Rigor)*
