# Metodologia Estatistica — GEO Papers Research

Documento tecnico detalhando os metodos matematicos, testes estatisticos, pressupostos, limitacoes e criterios de validacao utilizados na pesquisa empirica multi-vertical sobre citacoes de empresas brasileiras em LLMs.

**Versao:** 2.0 (26/03/2026)
**Implementacao:** `src/analysis/statistical.py`, `src/collectors/context_analyzer.py`

---

## 1. Design Experimental

### 1.1 Estrutura Fatorial

O estudo segue um design fatorial incompleto com 3 fatores:

- **Modelo LLM** (4 niveis): GPT-4o-mini, Claude Haiku 4.5, Gemini 2.5 Flash, Perplexity Sonar
- **Vertical** (4 niveis): Fintech, Varejo, Saude, Tecnologia
- **Categoria de query** (8+ categorias): descoberta, comparativo, confianca, produto, b2b, reputacao, etc.

Variavel dependente principal: **citacao** (binaria: 0/1) — se pelo menos uma entidade do cohort foi mencionada na resposta do LLM.

Variaveis dependentes secundarias: posicao (ordinal 1-3), sentimento (categorica), atribuicao (categorica), tamanho da resposta (continua), latencia (continua).

### 1.2 Unidade de Observacao

Cada observacao = 1 query enviada a 1 modelo LLM, com os seguintes campos coletados:

| Campo | Tipo | Descricao |
|-------|------|-----------|
| `cited` | bool | Se alguma entidade do cohort foi citada |
| `cited_entity` | text | Primeira entidade citada (por ordem do cohort) |
| `cited_entities_json` | JSON | Todas as entidades citadas |
| `position` | int (1-3) | Tercil da posicao da primeira mencao |
| `response_length` | int | Comprimento da resposta em caracteres |
| `latency_ms` | int/null | Tempo de resposta (NULL para cache hits) |
| `source_count` | int | Numero de fontes citadas pelo LLM |
| `hedging_detected` | bool | Se linguagem hedging foi detectada |

### 1.3 Controles Experimentais

**Entidades ficticias (Proposal 5):** 8 entidades inexistentes (2 por vertical) incluidas no cohort para calibracao de falsos positivos. Se um LLM cita "Banco Floresta Digital", isso indica alucinacao ou falso positivo no regex.

**Entidades cross-market (Proposal 8):** 5 fintechs internacionais (Revolut, Monzo, N26, Chime, Wise) para comparacao cross-market.

**Entidades ambiguas:** Nomes curtos ("Neon", "Stone", "99") mapeados para formas canonicas ("Banco Neon", "Stone Pagamentos", "99Pay") com regex word-boundary para evitar falsos positivos.

---

## 2. Testes Estatisticos

### 2.1 Chi-squared (Associacao Categorica)

**Quando:** Testar se a taxa de citacao difere significativamente entre dois grupos categoricos (ex: conteudo otimizado vs. nao-otimizado).

**Implementacao:**
```
H0: Taxa de citacao e independente do grupo
H1: Taxa de citacao difere entre grupos

Tabela de contingencia 2x2:
             Citado  Nao-citado
Grupo A      a       b
Grupo B      c       d

Estatistica: chi2 = sum((O - E)^2 / E)
GL: (r-1)(c-1) = 1
Effect size: Cramer's V = sqrt(chi2 / (n * (min(r,c) - 1)))
```

**Pressupostos:** N >= 5 em cada celula esperada. Se violado, usar Fisher exact test.

### 2.2 ANOVA / Kruskal-Wallis (Comparacao Multi-grupo)

**Quando:** Comparar taxas de citacao entre 4+ modelos LLM ou entre 4 verticais.

**Procedimento com verificacao de pressupostos:**

```
1. Teste de Levene (homogeneidade de variancias)
   H0: sigma_1^2 = sigma_2^2 = ... = sigma_k^2

2a. Se Levene p > 0.05:
    -> ANOVA one-way (F-test)
    H0: mu_1 = mu_2 = ... = mu_k
    Effect size: eta^2 = SS_between / SS_total
    Classificacao: 0.01 small, 0.06 medium, 0.14 large

2b. Se Levene p <= 0.05:
    -> Kruskal-Wallis (nao-parametrico)
    H0: As distribuicoes dos k grupos sao identicas
    Effect size: eta^2 = (H - k + 1) / (N - k)
```

**Limitacao atual:** O teste e aplicado sobre taxas agregadas por grupo, nao sobre observacoes individuais. Com N desbalanceado (Gemini N=30 vs. Sonar N=113), o poder estatistico difere entre comparacoes par-a-par.

### 2.3 Mann-Whitney U (Comparacao de Posicao)

**Quando:** Comparar posicao de citacao (variavel ordinal, 3 niveis) entre dois grupos.

```
H0: A distribuicao de posicoes e identica entre os grupos
H1: As distribuicoes diferem

Estatistica: U
Effect size: r = 1 - (2U) / (n1 * n2)
  |r| >= 0.5: large
  |r| >= 0.3: medium
  |r| >= 0.1: small
```

**Justificativa:** Posicao de citacao e ordinal e nao-normal, invalidando pressupostos do t-test.

### 2.4 Regressao Logistica (Preditores de Citacao)

**Quando:** Identificar quais fatores predizem citacao (variavel binaria).

```
log(p / (1-p)) = beta_0 + beta_1*x_1 + ... + beta_k*x_k

Variaveis independentes candidatas:
- schema_org (bool): presenca de dados estruturados
- word_count (int): tamanho do conteudo
- academic_refs (int): numero de referencias academicas
- wikidata_statements (int): propriedades no Wikidata
- vertical (categorica): setor da entidade
- model (categorica): LLM utilizado

Metricas de ajuste:
- Pseudo R^2 (McFadden): 1 - (LL_model / LL_null)
- AIC, BIC
- Odds ratios por preditor (exp(beta_i))
- LLR test p-value

Significancia por preditor: p < 0.05 (com correcao B-H para multiplos preditores)
```

**Implementacao:** `statsmodels.discrete.discrete_model.Logit` com `sm.add_constant`.

### 2.5 Correlacao (Spearman/Pearson)

**Quando:** Medir associacao entre variaveis continuas/ordinais.

```
Default: Spearman rho (nao-parametrico, robusto a outliers)
Alternativa: Pearson r (requer normalidade bivariada)

Classificacao de forca:
  |r| >= 0.7: forte
  |r| >= 0.4: moderada
  |r| >= 0.2: fraca
  |r| < 0.2: negligivel
```

### 2.6 T-test (Comparacao de Medias)

**Quando:** Comparar medias antes/depois de uma intervencao (A/B test).

```
Independente: t = (X1_bar - X2_bar) / SE_pooled
Pareado: t = D_bar / (SD_D / sqrt(n))

Effect size: Cohen's d = (X1_bar - X2_bar) / SD_pooled
  SD_pooled = sqrt(((n1-1)*s1^2 + (n2-1)*s2^2) / (n1+n2-2))
  d >= 0.8: large, d >= 0.5: medium, d >= 0.2: small
```

---

## 3. Correcao para Comparacoes Multiplas

### 3.1 Bonferroni

```
p_corrigido = min(p_original * m, 1.0)
onde m = numero de comparacoes

Uso: comparacoes family-wise (ex: 4 verticais = 6 pares)
Conservador: controla family-wise error rate (FWER)
```

### 3.2 Benjamini-Hochberg (FDR)

```
1. Ordenar p-values: p(1) <= p(2) <= ... <= p(m)
2. Para cada i, calcular threshold: (i/m) * alpha
3. Encontrar k = max{i : p(i) <= (i/m) * alpha}
4. Rejeitar H0 para todos i <= k

Uso: testes per-entity (69 entidades = muitas comparacoes)
Menos conservador: controla false discovery rate (FDR)
```

---

## 4. Analise de Contexto

### 4.1 Deteccao de Sentimento

Abordagem rule-based (nao ML) com 28 padroes regex bilingues:

**Sinais positivos (16):** "leading", "pioneer", "lider", "recomendado", "best", "top", "inovador", "referencia", "destaque", "sucesso", etc.

**Sinais negativos (12):** "controversial", "questionable", "criticado", "limitado", "problematico", "falha", "risco", etc.

**Regra de decisao:**
```
count(positive_matches) > count(negative_matches) -> "positive"
count(negative_matches) > count(positive_matches) -> "negative"
else -> "neutral"
```

**Janela:** 200 caracteres ao redor da primeira mencao da entidade.

### 4.2 Verificacao de Precisao Factual

Para 5 entidades-chave (Nubank, PagBank, Banco Inter, Stone, C6 Bank), verifica:
- Ano de fundacao
- CEO atual
- Sede
- Tipo de empresa

Detecta alucinacoes via regex (ex: Nubank fundado em data incorreta, CEO errado).

```
accuracy_score = verified_facts / total_checkable_facts
```

### 4.3 Deteccao de Hedging

16 padroes que indicam incerteza na citacao:
"according to", "segundo", "reportedly", "supostamente", "may be", "possibly", "claims to", "afirma ser", "self-described"

Presenca de hedging indica que o LLM nao tem alta confianca na informacao — relevante para Paper 3.

---

## 5. Intervalos de Confianca

### 5.1 IC para Taxas de Citacao (Visualizacao)

```
IC 95% = taxa +/- 1.96 * SEM
onde SEM = sqrt(p * (1-p) / N)
```

Implementado em `visualization.py` para graficos de barra.

### 5.2 IC Bayesiano (Recomendado para Publicacao)

```
Prior: Beta(1, 1) (uniforme)
Posterior: Beta(1 + citacoes, 1 + nao_citacoes)
IC 95% credivel: quantis 2.5% e 97.5% da posterior

Exemplo Gemini (4/30):
  Posterior: Beta(5, 27)
  IC 95%: [4.5%, 30.4%]
  vs. ponto fixo: 13.3%
```

---

## 6. Power Analysis

### 6.1 Tamanho Amostral Minimo

Para detectar effect size medio (d=0.3) com alpha=0.05 e power=0.80:

```
N_por_grupo >= (z_alpha/2 + z_beta)^2 * 2 * sigma^2 / delta^2
N_por_grupo >= (1.96 + 0.84)^2 * 2 / 0.3^2
N_por_grupo >= 176
```

**Status atual:**

| Modelo | N atual | N minimo | Adequado? |
|--------|---------|----------|-----------|
| GPT-4o-mini | 136 | 176 | Nao |
| Claude Haiku | 118 | 176 | Nao |
| Perplexity Sonar | 113 | 176 | Nao |
| Gemini Flash | 30 | 176 | Nao |

### 6.2 N Efetivo

```
N_eff = N_total - N_cache_hits_identicos
N_eff_atual ~ 181 (397 - 216 cache hits)
```

Cache hits que retornam respostas identicas nao sao observacoes independentes.

---

## 7. Limitacoes Metodologicas

### 7.1 Ameacas a Validade Interna

1. **Vies de selecao nas queries:** Queries escritas pelo pesquisador, nao amostradas de buscas reais. Queries diretivas ("melhores bancos digitais") inflam taxa de citacao.

2. **Non-stationarity dos LLMs:** Modelos atualizam sem aviso. A mesma query pode produzir respostas diferentes em dias diferentes, nao por variacao natural, mas por mudanca de modelo.

3. **Dependencia entre observacoes:** Queries similares na mesma sessao compartilham estado interno do LLM (temperatura, KV-cache).

4. **Sentimento rule-based:** 28 padroes regex nao capturam ironia, contexto complexo ou sentimento implicito. Tendencia a classificar como "neutro" por default.

### 7.2 Ameacas a Validade Externa

1. **Amostra de conveniencia:** 69 entidades brasileiras nao representam o universo de todas as empresas.

2. **4 modelos LLM:** Nao inclui Copilot (Bing), Llama (Meta), Mistral, ou modelos open-source.

3. **Queries em ingles e portugues:** Proporcao nao reflete distribuicao real de idiomas dos usuarios.

4. **Periodo temporal:** Dados de 2-3 dias nao permitem generalizacao temporal.

### 7.3 Mitigacoes Planejadas

| Ameaca | Mitigacao | Status |
|--------|-----------|--------|
| Queries diretivas | Separar categorias "diretivas" vs "neutras" na analise | Pendente |
| Non-stationarity | Tabela `model_versions` com hash de respostas canonicas | Schema pronto, nao implementado |
| Dependencia | Replicacoes (k >= 3 por query) com temperatura > 0 | Pendente |
| Sentimento simplista | Validacao manual de amostra aleatoria (50+ registros) | Pendente |
| N insuficiente | Coleta diaria automatizada por 90+ dias | Em andamento |
| Entidades ficticias | Incluir nas queries e verificar taxa de falsos positivos | Pendente |

---

## 8. Revisao por Painel de Especialistas

Em 26/03/2026, uma revisao critica foi conduzida simulando a perspectiva de 7 especialistas em estatistica e ML:

- **Michael I. Jordan** (Berkeley): Necessidade de modelagem bayesiana hierarquica e replicacoes
- **David Donoho** (Stanford): Separar exploracao de confirmacao; pre-registrar hipoteses
- **Xiao-Li Meng** (Harvard): N efetivo dramaticamente menor que N bruto; data defect index alto
- **Andrew Gelman** (Columbia): Effect sizes minusculos; garden of forking paths; parar de dicotomizar p-values
- **Grace Wahba** (Wisconsin): Infraestrutura longitudinal sem dados temporais suficientes
- **Bradley Efron** (Stanford): Ausencia de bootstrap para validacao de robustez
- **Terence Tao** (UCLA): LLMs sao nao-estacionarios; mixed-effects models necessarios

Documento completo: `output/critica_estatistica_panel.md`

---

## 9. Roadmap Metodologico

### Fase atual: Exploratoria (marco 2026)
- Coleta automatizada diaria
- Testes descritivos e explorativos
- Nenhum resultado deve ser reportado como confirmativo

### Fase 2: Pre-registro (abril 2026)
- Pre-registrar >= 3 hipoteses na tabela `hypotheses`
- Definir alpha, power, effect size esperado, N minimo por hipotese
- Congelar design experimental

### Fase 3: Coleta confirmatoria (maio-junho 2026)
- 60+ dias de coleta com design congelado
- Bootstrap (B=10.000) para todas as metricas
- Mixed-effects models (query como random effect)
- Cross-validation (k=5) para regressao logistica

### Fase 4: Publicacao (julho 2026)
- Paper 1 (ArXiv): resultados descritivos + ANOVA/KW
- Paper 3 (Info Sciences): Fisher exact + odds ratios + A/B tests
- Paper 2 (SIGIR): dados SERP overlap (requer 12+ semanas)

---

## 10. Inferencia robusta: BCa, Beta-binomial e kappa (entregue 08/04/2026)

A revisao metodologica de abril 2026 fechou tres lacunas declaradas em
secoes anteriores:

### 10.1 Bootstrap BCa (Efron, 1987)

`StatisticalAnalyzer.bootstrap_ci_bca(sample, statistic, n_resamples, confidence)`
implementa o intervalo de confianca Bias-Corrected and Accelerated, hoje
o padrao defensivel para qualquer estatistica escalar com distribuicao
amostral assimetrica.

Formulacao:

```
z0     = Phi^-1( P(theta_b < theta_obs) )       # bias correction
a      = sum( (theta_bar - theta_(i))^3 )       # acceleration via jackknife
         / ( 6 * (sum(...^2))^(3/2) )
alpha1 = Phi( z0 + (z0 + z_{a/2})  / (1 - a*(z0 + z_{a/2})) )
alpha2 = Phi( z0 + (z0 + z_{1-a/2}) / (1 - a*(z0 + z_{1-a/2})) )
CI     = [ F^-1_boot(alpha1), F^-1_boot(alpha2) ]
```

Vantagens sobre o percentile bootstrap puro: corrige vies de localizacao
e assimetria, segunda-ordem correto (O(1/n)), aplicavel a qualquer
estatistica. Aceita `statistic ∈ {"mean", "median", "proportion"}` ou
callable arbitraria. Default `n_resamples = 10_000`. Cobertura empirica
testada em `tests/test_analysis.py::test_bootstrap_bca_*`.

### 10.2 Beta-binomial bayesiano

`StatisticalAnalyzer.beta_binomial_ci(cited, n, prior_alpha, prior_beta, confidence)`
substitui o intervalo Wald (1.96 SE) — invalido para `k=0`, `k=n` ou `n` pequeno.

Modelo:
```
theta ~ Beta(prior_alpha, prior_beta)
k | theta ~ Binomial(n, theta)
theta | k ~ Beta(prior_alpha + k, prior_beta + n - k)
```

Defaults Beta(1, 1) (uniforme, equivalente ao smoothing de Laplace).
O `generate_summary_report` agora reporta o posterior mean + CI 95%
para cada LLM em `bayesian_by_llm`.

### 10.3 Cohen's e Fleiss' kappa

`StatisticalAnalyzer.cohen_kappa(rater_a, rater_b)` e `fleiss_kappa(ratings)`
substituem "agreement bruto" por concordancia corrigida por chance:

```
kappa_Cohen = (p_o - p_e) / (1 - p_e)
kappa_Fleiss: variante para R raters por sujeito
```

Interpretacao: Landis & Koch (1977). O `generate_summary_report` agora
reporta `inter_llm_fleiss_kappa` quando o painel for retangular,
medindo se 4 LLMs concordam na decisao binaria "citou ou nao" para a
mesma query alem do esperado por sorteio.

### 10.4 Fisher exact fallback

`chi_squared_citation_rate` agora detecta automaticamente
`min(expected) < 5` e cai para `scipy.stats.fisher_exact`. Restaura
validade quando o desenho fica desbalanceado (verticais com baixo N).

### 10.5 Brier score e reliability diagram

`brier_score(probabilities, outcomes)` retorna a decomposicao de Murphy (1973):
```
BS = reliability - resolution + uncertainty
```
e `reliability_diagram(probabilities, outcomes, n_bins)` gera os bins
empiricos. Estas duas funcoes alimentam diretamente o pipeline de
calibracao do GEO Score Checker (proxima secao).

---

## 11. Bridge Papers ↔ GEO Score Checker (entregue 08/04/2026)

A tabela `score_calibration_inputs` (ver `src/db/schema.sql`) une, por
dominio e vertical, o vetor de 8 dimensoes do Score Checker
(`d1_retrieval_fitness` ... `d8_entity_authority`) com a taxa empirica
de citacao observada nos paineis Papers (`k_cited / n_observations`).

O script `scripts/calibrate_score.py` consome essa tabela (ou gera
dataset sintetico via `--simulate N`) e ajusta:

```
logit(P(cited|site)) = beta_0 + sum_d beta_d * D_d(site)
```

Os pesos calibrados sao:

```
w*_d = 100 * max(0, beta_d) / sum_k max(0, beta_k)
```

substituindo os pesos cravados (15, 15, 20, 15, 10, 10, 10, 5).

Diagnosticos do script:
- coeficientes, IC 95% via Wald, p-valores, odds ratios;
- pseudo-R2 McFadden, AIC, BIC;
- AUROC + Brier sob 5-fold CV;
- reliability diagram in-sample;
- Spearman entre score atual e calibrado;
- delta de pesos (atual -> calibrado).

Demonstracao end-to-end (modo simulate, n=200):
```
$ python scripts/calibrate_score.py --simulate 200 --diagram
pseudo R2 (McFadden): 0.1742
5-fold CV AUROC: 0.8146 (+/- 0.0253)
5-fold CV Brier: 0.0370 (+/- 0.0039)
Spearman(score_atual, score_calibrado): 0.9495
```

A coluna `model_version` (adicionada a `citations` em 08/04) habilita
analise longitudinal valida sob non-stationarity dos modelos LLM.

### Proximos passos (roadmap atualizado)

- (mai/2026) GLMM hierarquico com efeito aleatorio por dominio + vertical
- (mai/2026) IRT 2-PL para reduzir 8 dimensoes a 3-4 fatores latentes
- (jun/2026) BSTS / CausalImpact para a 9a dimensao "Causal Impact"
- (jun/2026) Bootstrap BCa do score em producao (4+ replicas LLM por dim)
- (jul/2026) Pre-registro publico no OSF

---

*Ultima atualizacao: 08/04/2026 (secoes 10 e 11 adicionadas)*
*Autor: Alexandre Caramaschi — Brasil GEO*
*Revisao: Painel simulado de 7 especialistas (Jordan, Donoho, Meng, Gelman, Wahba, Efron, Tao)*
