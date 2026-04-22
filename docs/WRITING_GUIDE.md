# Writing Guide — Scientific Writing for GEO / LLM Research

Guia de escrita científica para a linha de pesquisa GEO/LLM. Foca no que é específico deste domínio (LLMs como sujeitos de pesquisa, reprodutibilidade de sistemas não-determinísticos, N pequeno por design) e não repete o óbvio de style guides gerais.

**Versão:** 1.0 (2026-04-21)
**Público-alvo:** Alexandre Caramaschi e co-autores futuros preparando submissões SSRN, ArXiv, Q1 journals.
**Linguagem:** manuscripts em inglês acadêmico. Este guia em PT-BR com exemplos bilíngues.

---

## 1. Estrutura IMRAD e Variações

### 1.1 IMRAD clássico (aplicável a estudos empíricos quantitativos)

1. **Introduction** — problema, research question, contribution statement, roadmap.
2. **Methods** — design, participants/objects, instruments, procedure, analysis plan.
3. **Results** — achados objetivos, tabelas, figuras, sem interpretação.
4. **Discussion** — interpretação, comparação com literatura, limitações, implicações, threats to validity.

Apêndices e Related Work normalmente entram como seções 2 (Related Work entre Intro e Methods) e final (Appendices).

### 1.2 Design Science Research (DSR — Hevner 2004)

Quando o paper propõe um **artefato** (framework, método, sistema, modelo), IMRAD não basta. Estrutura DSR:

1. **Introduction** + **problem relevance**.
2. **Research Background** — estado da arte do problema.
3. **Artefact Design** — construção do artefato (modelo, método, instanciação).
4. **Evaluation** — como o artefato foi avaliado (experimento, case study, analytical).
5. **Discussion** — contribuições para knowledge base, implications for practice.

Sete diretrizes de Hevner (2004): design as artifact, problem relevance, design evaluation, research contributions, research rigor, design as search process, communication of research.

### 1.3 Action Design Research (ADR — Sein 2011)

Apropriado quando o pesquisador intervém em um contexto real (ex.: sprint de 7 dias de GEO em uma empresa) e co-constrói o artefato com os atores do contexto.

Quatro estágios ADR:
1. **Problem formulation** — compreensão situada.
2. **Building, intervention, evaluation (BIE)** — ciclos iterativos.
3. **Reflection and learning** — generalização.
4. **Formalization of learning** — articulação dos princípios de design.

O paper SSRN 6460680 (7-Day Sprint) se enquadra em ADR. Explicitar isso na section Methods evita críticas "where is the statistical test?" — ADR não depende de testes inferenciais clássicos.

### 1.4 Action Research (AR)

Parente de ADR, mas centrado em mudança organizacional, não em artefato tecnológico. Menos aplicável a GEO research, mas relevante se o foco for change management de equipes SEO adaptando-se a LLMs.

---

## 2. Hedging Language — Escrita Cautelosa em Inglês

LLMs produzem resultados estocásticos. Overclaiming é fatal em peer review. Use hedging sistematicamente.

### 2.1 Verbos e expressões hedged

| Forte (evitar sem evidência robusta) | Hedged (preferir) |
|--------------------------------------|--------------------|
| "proves that" | "suggests that" / "is consistent with" |
| "shows that" (conclusivo) | "indicates that" / "provides evidence that" |
| "demonstrates" | "illustrates" / "appears to demonstrate" |
| "confirms" | "supports" / "lends support to" |
| "will" | "may" / "could" / "is likely to" |
| "always" / "never" | "in the observed conditions" / "under the tested configurations" |
| "significantly better" (sem teste) | "numerically higher" / "trended higher" |

### 2.2 Fórmulas úteis

- "These results are consistent with the interpretation that..."
- "Under the conditions tested, the framework appears to..."
- "While causal claims would require further investigation, the pattern observed..."
- "Subject to the limitations discussed in Section X, the findings suggest..."

### 2.3 Quando NÃO hedge

- Definições operacionais: "We define citation rate as the proportion of queries in which..."
- Procedimentos: "All queries were executed between [date] and [date]."
- Fatos sobre o dataset: "The cohort contains 69 entities across four verticals."

Hedge interpretações, não fatos.

---

## 3. Citar LLMs como Sujeitos de Pesquisa, Não Como Fontes

LLMs em research sobre LLMs são **objetos de estudo**, não autores ou fontes.

### 3.1 Certo

> "We submitted 480 queries to GPT-4o-mini (`gpt-4o-mini-2024-07-18`), Claude Haiku 4.5 (`claude-haiku-4-5-20251001`), Gemini 2.5 Pro, Perplexity Sonar, and Llama 3.3 70B (via Groq). Temperature was fixed at 0.0 for all calls."

### 3.2 Errado

> "According to GPT-4o, Nubank is the leading digital bank in Brazil."

**Nunca** cite o output do LLM como se fosse uma fonte. Cite sempre a versão do modelo, data de execução, parâmetros, prompt.

### 3.3 Versioning de modelos

Sempre especifique o model ID exato (não apenas o nome marketing):

- GPT-4o-mini → `gpt-4o-mini-2024-07-18`
- Claude Haiku 4.5 → `claude-haiku-4-5-20251001`
- Gemini 2.5 Pro → `gemini-2.5-pro` (data de acesso)
- Perplexity Sonar → `sonar` (data de acesso)
- Llama 3.3 70B via Groq → `llama-3.3-70b-versatile` (data de acesso)

LLM providers deprecam versões. Sem snapshot exato, o paper é irreprodutível.

---

## 4. Reproducibility Checklist para LLM Research

Este é o ponto mais escrutinado em peer review de papers sobre LLMs. Cheque **todos**:

- [ ] **Model IDs exatos** (não marketing names).
- [ ] **Temperature** especificado (0.0 para determinismo ou distribuição de seeds).
- [ ] **Top-p, top-k, max_tokens** — documentados mesmo se default.
- [ ] **Seed value** quando o provider suporta (OpenAI suporta `seed` param).
- [ ] **Prompt templates** no apêndice, literal (não parafraseado).
- [ ] **System prompt** se houver (mesmo que vazio: declarar).
- [ ] **Retrieval cutoff / knowledge cutoff** do modelo citado.
- [ ] **Data de execução** das queries (mês/ano mínimo; dia quando relevante).
- [ ] **API endpoint** (ex.: `api.openai.com/v1/chat/completions`).
- [ ] **Rate limits** encontrados e como foram tratados.
- [ ] **Caching strategy** — respostas foram cacheadas por hash SHA-256 do prompt? Quando cache foi invalidado?
- [ ] **Regiões / providers intermediários** (ex.: Azure OpenAI vs. OpenAI direto).
- [ ] **Tool use / function calling** — se desativado, declarar.
- [ ] **Web search habilitado** (Perplexity, Gemini com grounding) — declarar claramente.
- [ ] **Post-processing** — regex, normalização, stopwords — código publicado.
- [ ] **Anotação humana** — se houver, quantos anotadores, kappa/agreement, guidelines.
- [ ] **Replication package** em repositório público com README e licença.

---

## 5. Ethics em LLM Research

### 5.1 Quando IRB approval é necessário

- **Sempre** que humanos produzem dados (entrevistas, surveys, usability tests).
- **Sempre** que humanos avaliam outputs de LLMs (inter-rater, anotação de qualidade).
- **Discutível** quando LLM é o único sujeito — alguns IRBs exigem review mesmo sem humanos, por risco de dual-use.

No contexto atual (pesquisa independente, sem afiliação universitária ativa), documente no paper:

> "This research did not involve human subjects and therefore did not require Institutional Review Board (IRB) approval. All data collected consists of responses generated by publicly accessible large language model APIs under commercial terms of service."

Se tiver anotadores humanos (mesmo pagos em plataformas crowd), adicionar:

> "Annotators were recruited via [platform], compensated at [USD X/hour], and provided informed consent. The annotation task involved [description]. No personally identifying information was collected. The study was conducted in accordance with ethical guidelines for computational research [reference to ACM Code of Ethics or APA guidelines]."

### 5.2 Dual-use e harm considerations

Para papers sobre GEO, discutir em Discussion ou Ethical Considerations section:

- Risk de manipulação adversarial de LLMs (content farms otimizando para citação).
- Equity — quem tem recursos para fazer GEO vs. quem não tem.
- Transparência com usuários finais quando conteúdo é GEO-optimized.

### 5.3 Terms of Service

LLM APIs têm TOS que restringem certos usos (scraping massivo, treinamento de competidores, publicação de saídas completas). Revisar TOS antes de publicar raw outputs. Publicar **hashes** + **prompt** geralmente é seguro; publicar **full responses** de grandes volumes pode violar TOS.

---

## 6. Estatística para N Pequeno

GEO research frequentemente tem N pequeno (ex.: 69 entidades, 480 queries). Testes clássicos p-value falham por baixo poder. Soluções:

### 6.1 Effect sizes em vez de (ou além de) p-values

| Comparação | Effect size | Interpretação |
|------------|-------------|---------------|
| Duas médias (contínuo) | **Cohen's d** (N grande) / **Hedges's g** (N pequeno, correção) | 0.2 small, 0.5 medium, 0.8 large |
| Duas proporções | **Cohen's h** | 0.2 small, 0.5 medium, 0.8 large |
| Correlação | **Pearson r** ou **Spearman ρ** | 0.1 small, 0.3 medium, 0.5 large |
| Associação 2x2 | **Phi (φ)** ou **Cramér's V** | 0.1 small, 0.3 medium, 0.5 large |
| Ordinal / ranks | **Cliff's delta (δ)** | 0.147 small, 0.33 medium, 0.474 large |

**Hedges's g** é preferível a Cohen's d quando N < 20. Fórmula: `g = d × (1 - 3/(4×(n1+n2)-9))`.

### 6.2 Confidence intervals

Sempre reportar CI95% junto com effect size. Ex.:

> "The intervention group showed a higher citation rate (g = 0.62, 95% CI [0.21, 1.03]), which is consistent with a medium-sized effect."

Para proporções com N pequeno, usar **Wilson score interval** em vez de Wald (que falha com p próximo de 0 ou 1).

### 6.3 Bayesian alternatives

Para N muito pequeno (< 30 por grupo), **Bayes Factor** é mais informativo que p-value. Interpretação:

| BF10 | Evidência para H1 |
|------|-------------------|
| 1-3 | Anedótica |
| 3-10 | Moderada |
| 10-30 | Forte |
| 30-100 | Muito forte |
| > 100 | Extrema |

Pacotes: R `BayesFactor`, Python `pingouin.bayesfactor_ttest()`.

### 6.4 Non-parametric tests

Quando distribuição é desconhecida ou N muito pequeno:

- **Mann-Whitney U** (comparar dois grupos independentes).
- **Wilcoxon signed-rank** (paired).
- **Kruskal-Wallis** (> 2 grupos).
- **Fisher exact test** (2x2 com N pequeno — substitui chi-squared quando expected count < 5).

---

## 7. Multiple Testing Corrections

Com múltiplas comparações (4 verticais × 5 LLMs × 8 query categories = 160 testes potenciais), inflation of Type I error é inevitável sem correção.

### 7.1 Family-Wise Error Rate (FWER)

Mantém P(pelo menos 1 falso positivo) ≤ α.

- **Bonferroni:** α_adjusted = α / k. Conservador, perde poder rápido.
- **Holm-Bonferroni (sequencial):** ordena p-values, testa em ordem. Uniformemente mais potente que Bonferroni. **Preferir este**.
- **Šidák:** α_adjusted = 1 - (1-α)^(1/k). Entre Bonferroni e Holm em conservadorismo.

### 7.2 False Discovery Rate (FDR)

Controla E[false discoveries / total discoveries]. Mais potente que FWER.

- **Benjamini-Hochberg (BH):** ordena p-values, encontra maior i tal que p_i ≤ (i/k) × α. **Standard em exploratory LLM research**.
- **Benjamini-Yekutieli (BY):** versão conservadora para correlações positivas.

### 7.3 Quando usar qual

| Contexto | Correção recomendada |
|----------|----------------------|
| Hypothesis-driven, poucos testes pré-especificados | Bonferroni ou Holm |
| Exploratory, muitos testes | Benjamini-Hochberg FDR |
| Dependência forte entre testes | Benjamini-Yekutieli FDR |
| Replication confirmatory | α = 0.05 sem correção (teste único) |

### 7.4 Sempre reportar

- Número de testes feitos (not just the significant ones).
- Correção aplicada.
- p-values originais E corrigidos.
- Se correção não foi aplicada, justificar (ex.: "We report unadjusted p-values and rely on effect sizes for interpretation; the study is exploratory").

---

## 8. Writing Tips Q1-Ready

### 8.1 Abstract estruturado (250-300 palavras)

Formato que editors Q1 esperam:

- **Purpose** (1-2 frases): qual problema.
- **Design/methodology/approach** (2-3 frases): como.
- **Findings** (3-4 frases): o que encontrou.
- **Originality/value** (1-2 frases): por que importa.
- **Research limitations/implications** (1 frase): caveat.

Evitar: frases como "This paper presents...", "In this work we...". Começar direto: "Generative engines (LLMs with retrieval) increasingly mediate business discovery, yet no systematic framework exists for measuring..."

### 8.2 Uma research question clara

Papers Q1 têm **UMA** pergunta central. Se tiver 3, provavelmente são 3 papers.

Formato: "**RQ: How does [independent variable] affect [dependent variable] under [context/constraints]?**"

Exemplo GEO:
> "RQ: How does a structured 7-day GEO sprint affect the citation rate of entities across five leading LLMs, compared to their baseline citation rates prior to intervention?"

### 8.3 Contribution statement explícito no fim da Introduction

Bullet list de 3-5 contribuições. Reviewers procuram isso.

> "This paper makes the following contributions:
> - We propose a replicable 7-day GEO sprint framework grounded in Action Design Research.
> - We operationalize citation rate as a measurable construct across five LLMs.
> - We provide a public replication package with prompts, entity cohorts, and raw responses.
> - We identify three threats to validity specific to LLM-based research."

### 8.4 Related Work tematizado, não cronológico

**Ruim (cronológico):**
> "In 2023, Smith et al. studied X. In 2024, Johnson et al. extended this. In 2025, our prior work showed..."

**Bom (tematizado):**
> "Prior work on LLM citation behavior clusters in three streams: (1) cognitive benchmarks measuring recall [A, B, C]; (2) adversarial robustness of retrieval-augmented generation [D, E]; and (3) content optimization strategies for discoverability [F, G, H]. Our work extends stream (3) by..."

### 8.5 Tabelas e figuras

- Cada tabela/figura deve ser **self-contained** (caption explica tudo).
- Tabelas com valores numéricos alinhadas à direita, decimais consistentes (2 casas tipicamente).
- Figuras vetoriais (PDF/SVG), não PNG em journals que aceitam.
- Color palettes colorblind-safe (viridis, cividis).
- Caption estrutura: "**Figure X.** One-sentence summary. Details about axes, groups, error bars. Interpretation cue."

### 8.6 Threats to Validity (section obrigatória em DSR/ADR)

Quatro categorias clássicas (Wieringa 2014, Runeson & Höst 2009):

- **Construct validity:** medimos o que dizemos medir? (Ex.: citation rate captura authority?)
- **Internal validity:** causa é mesmo a que afirmamos? (Ex.: confounding factors?)
- **External validity:** generaliza? (Ex.: 4 verticais brasileiras → mercados globais?)
- **Reliability:** outros pesquisadores replicariam? (Ex.: se LLM version muda, resultados mudam?)

Dedicar uma subseção por categoria em Discussion.

### 8.7 Evitar hype vocabulary

Listas negras para GEO papers:

- "revolutionary", "groundbreaking", "game-changing"
- "AI-powered" (todo paper de AI é AI-powered)
- "novel approach" (deixe o reviewer decidir)
- "state-of-the-art" (só se batido benchmark público)
- "unprecedented"

Substituir por descrição factual.

---

## 9. Ferramentas e Recursos

- **Grammarly Premium** ou **LanguageTool** — revisão de inglês.
- **Semantic Scholar** — busca de literatura com embeddings.
- **Connected Papers** (connectedpapers.com) — grafo de citações relacionadas.
- **Elicit** (elicit.com) — research assistant com LLM.
- **LaTeX + Overleaf** — padrão para journals STEM.
- **Zotero** + **Better BibTeX** — gestão de referências.
- **R `pwr` package** ou Python `statsmodels.stats.power` — power analysis.
- **JASP** ou **Pingouin** — Bayesian stats sem dor.

---

## 10. Referências bibliográficas

- Hevner, A. R., March, S. T., Park, J., & Ram, S. (2004). Design Science in Information Systems Research. *MIS Quarterly*, 28(1), 75-105.
- Sein, M. K., Henfridsson, O., Purao, S., Rossi, M., & Lindgren, R. (2011). Action Design Research. *MIS Quarterly*, 35(1), 37-56.
- Wieringa, R. J. (2014). *Design Science Methodology for Information Systems and Software Engineering*. Springer.
- Runeson, P., & Höst, M. (2009). Guidelines for conducting and reporting case study research in software engineering. *Empirical Software Engineering*, 14(2), 131-164.
- Benjamini, Y., & Hochberg, Y. (1995). Controlling the False Discovery Rate. *Journal of the Royal Statistical Society: Series B*, 57(1), 289-300.
- Holm, S. (1979). A simple sequentially rejective multiple test procedure. *Scandinavian Journal of Statistics*, 6(2), 65-70.
- Hedges, L. V., & Olkin, I. (1985). *Statistical Methods for Meta-Analysis*. Academic Press.
- Kass, R. E., & Raftery, A. E. (1995). Bayes Factors. *Journal of the American Statistical Association*, 90(430), 773-795.
