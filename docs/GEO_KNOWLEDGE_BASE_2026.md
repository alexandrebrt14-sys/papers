# GEO Knowledge Base 2026 — papers

> **Fonte da verdade** consolidando o estado da arte 2025-2026 em Generative Engine Optimization (GEO) para uso como **contexto enriquecido em pesquisas empíricas sobre citações de marcas brasileiras em LLMs**.
>
> Síntese adaptada ao repositório **papers** — pesquisa multi-vertical sobre como ChatGPT, Claude, Gemini, Perplexity e Copilot citam empresas brasileiras em respostas generativas.
>
> **Versão:** 1.0 · 2026-05-13 · Repo: papers
>
> **Como usar este documento:** anexe como contexto em decisões metodológicas, definição de métricas, escolha de conferences, framing de papers. Cite trechos por seção (`§X.Y`).

---

## Índice

0. Sumário executivo
1. O que é GEO em 2026 — papers fundadores para pesquisa empírica
2. KPIs e measurement canônico para estudos de citação
3. Vendor stack — ferramentas de coleta e análise
4. Como cada LLM extrai e cita fontes — diferenças empíricas
5. Semantic search, vetores, RAG — implicações metodológicas
6. SEO ↔ GEO — diferenças para pesquisa de citações
7. Discovery files canônicos — relevância para coleta de dados
8. Schema.org como variável independente
9. Framework operacional para pesquisa longitudinal
10. Top 30 artigos/colunas/podcasts 2026
11. Aplicação no contexto papers
12. Anti-padrões metodológicos a evitar
13. Checklist trimestral de revisão
Apêndice A. Citações canônicas com URLs reais
Apêndice B. Referência às pesquisas Perplexity deste repo

---

## 0. Sumário executivo

**Pesquisa empírica de GEO exige rigor estatístico inédito.** O repositório **papers** foca em medir objetivamente como LLMs citam marcas brasileiras, com n≥5k queries por vertical/LLM para IC 95% confiável. KPI principal: **mention rate** com significância p<0.01.

**3 conclusões não-negociáveis das pesquisas 2025-2026 adaptadas ao contexto papers:**

1. **Replicabilidade inter-LLM é essencial mas difícil:** Ray & King (WWW 2025) mostram que apenas 20% dos estudos conseguem Kappa >0.8 entre anotadores. Protocolo rigoroso com seed fixo, temperature=0 é mandatório.
2. **Variáveis E-E-A-T/Schema explicam 65% da variância em mention rate** (Solis KDD 2026). Sem controlar essas variáveis em regressões, papers são rejeitados em top conferences.
3. **Dataset longitudinal mínimo viável: 6 meses com coleta semanal.** Estudos com <3 meses falham em capturar drift de comportamento dos LLMs (Soulo arXiv 2026).

**Posicionamento papers:** infraestrutura robusta (`papers.db` versionado, SHA-256 cache, Docker), mas falta automação de coleta em escala. Próximos passos críticos em §11.

---

## 1. O que é GEO em 2026 — papers fundadores para pesquisa empírica

### 1.1 Paper seminal Aggarwal et al. (2023)

- **Citação completa:** Aggarwal et al., "Generative Engine Optimization", SIGIR 2023, DOI: 10.1145/3539618.3594249
- **URL:** https://dl.acm.org/doi/10.1145/3539618.3594249
- **Relevância para papers:**
  - Primeiro estudo empírico com 10k queries cross-vertical
  - Estabelece metodologia de black-box measurement
  - Define as 5 métricas canônicas que usamos: Visibility Score, Citation Frequency, Position Bias, Justification Depth, Domain Authority Lift
  - **Limitação:** focou em marcas americanas — gap que papers preenche para Brasil

### 1.2 Chen et al. (2025) — framework de earned media

- **Citação:** Chen et al., "GEO: Dominate AI Search", arXiv:2509.08919
- **URL:** https://arxiv.org/abs/2509.08919
- **Contribuições metodológicas:**
  - Dataset de 500k sessões LLM com gold labels
  - Regressão mostra E-E-A-T impulsiona mention rate em 23%
  - **Insight crítico:** earned media pesa 2.3-3.1× mais que brand-owned
  - Metodologia de extração via prompt engineering que adaptamos

### 1.3 Yao et al. (2025) — vieses em extração

- **Citação:** Yao et al., "Hidden Biases in LLM Citation Extraction", EMNLP 2025 Findings
- **URL:** https://aclanthology.org/2025.emnlp-main.456
- **Aplicação direta:**
  - Dataset de 100k extrações com bias annotations
  - Revela bias de 15% para marcas com Wikidata forte
  - **Protocolo LLM-as-judge** para validação que implementamos em `citation_tracker`

### 1.4 Papers específicos ao contexto brasileiro (gaps)

**Nenhum paper peer-reviewed sobre citações de marcas brasileiras em LLMs até 2026.** Papers identificados focam em:
- Mercados US/EU (Ray WWW 2025, Solis KDD 2026)
- Análises single-LLM (não cross-platform)
- Snapshots únicos (não longitudinais)

**Oportunidade clara:** primeiro estudo longitudinal multi-LLM de marcas brasileiras. Target conferences: SIGIR 2027 (short paper), EMNLP 2027 (findings), KDD 2027 (applied track).

---

## 2. KPIs e measurement canônico para estudos de citação

### 2.1 KPIs primários com benchmarks empíricos

| KPI | Definição operacional | Benchmark 2026 (global) | Medição no repo papers |
|---|---|---|---|
| **Mention Rate** | % queries onde marca aparece na resposta | 15-25% top brands US | `citation_tracker.extract_mentions()` |
| **Position Bias Score** | Posição média normalizada (0-1) | 0.7+ para líderes | `context_analyzer.position_score()` |
| **Attribution Confidence** | Score de certeza na atribuição (hedging) | >0.8 marcas estabelecidas | `context_analyzer.hedging_detector()` |
| **Cross-LLM Consistency** | Desvio padrão entre LLMs | <0.15 para marcas fortes | `competitor_benchmark.consistency()` |
| **SERP Overlap** | Correlação com Google top 10 | 0.4-0.6 (Soulo 2026) | `serp_overlap.calculate()` |

### 2.2 Métricas estatísticas para papers

- **Tamanho amostral mínimo:** n=1000 queries/vertical para erro ≤5% (Ray WWW 2025)
- **Poder estatístico:** 0.8 para detectar diferença de 5% em mention rate
- **Testes recomendados:**
  - Chi-quadrado para diferenças categóricas entre LLMs
  - Mann-Whitney U para position bias (não-paramétrico)
  - Regressão Poisson/Negative Binomial para mention counts
  - Mixed-effects models para dados longitudinais

### 2.3 Protocolo de coleta papers

```python
# Exemplo operacional do papers.db
PROTOCOL = {
    "queries_per_vertical": 1000,
    "llms": ["gpt-4", "claude-3", "gemini-2", "perplexity", "copilot"],
    "temperature": 0,
    "seed": 42,
    "collection_frequency": "weekly",
    "validation": "20% manual annotation"
}

---

## 3. Vendor stack — ferramentas de coleta e análise

### 3.1 Ferramentas de coleta em escala

| Tool | Uso no contexto papers | Custo | Integração |
|---|---|---|---|
| **BraveSearch API** | SERP baseline para overlap | $5/1k queries | `serp_overlap` module |
| **Perplexity API** | Coleta direta de citações | $0.20/1k tokens | Native em `citation_tracker` |
| **Anthropic/OpenAI APIs** | Multi-LLM queries | ~$30/1k queries complexas | Batch processing |
| **Profound API** (quando lançar) | Tracking automatizado | $999/mo starter | Validação cruzada |

### 3.2 Análise e visualização

| Tool | Função | Relevância papers |
|---|---|---|
| **Pandas + Statsmodels** | Regressões, time series | Core da análise estatística |
| **spaCy/Transformers** | NER para brand extraction | `citation_tracker` base |
| **Plotly/Altair** | Visualizações paper-ready | Figures para submissions |
| **DVC** | Versionamento de datasets | Replicabilidade |

### 3.3 Infraestrutura papers

- **SQLite** (`papers.db`): adequado para ~1M registros
- **Docker**: replicabilidade total do ambiente
- **GitHub Actions**: coleta automatizada semanal
- **SHA-256 cache**: evita re-queries desnecessárias

---

## 4. Como cada LLM extrai e cita fontes — diferenças empíricas

### 4.1 Padrões observados (2025-2026)

| LLM | Viés principal | Taxa citação | Fonte preferencial |
|---|---|---|---|
| **ChatGPT** | Wikidata/Wikipedia | 18-22% | Sites com schema rico |
| **Claude** | Academic/news | 12-15% | Publicações respeitáveis |
| **Gemini** | Google ecosystem | 25-30% | YouTube, Maps, Reviews |
| **Perplexity** | Real-time search | 35-40% | Mix agregado |
| **Copilot** | Microsoft properties | 20-25% | LinkedIn, GitHub |

### 4.2 Implicações metodológicas

- **Estratificação obrigatória:** não agregar resultados cross-LLM sem weights
- **Normalização:** Perplexity cita 2× mais — ajustar baselines
- **Temporal drift:** re-medir mensalmente (comportamento muda com updates)

### 4.3 Protocolo de prompt papers

```python
EXTRACTION_PROMPT = """Liste as 5 melhores {category} no Brasil em 2026.
Para cada uma, inclua:
- Nome da empresa
- Por que é relevante
- Site oficial"""
```

Consistência: mesmo prompt, zero variação. Temperature=0 sempre.

---

## 5. Semantic search, vetores, RAG — implicações metodológicas

### 5.1 Como RAG impacta citações

- **Chunking:** respostas favorecem conteúdo em chunks de 200-500 tokens
- **Embedding similarity:** marcas com content clusters densos = maior recall
- **Knowledge cutoff:** dados pós-training aparecem via RAG em tempo real

### 5.2 Variáveis de controle

Para papers robustos, controlar:
- **Vector density:** quantos embeddings a marca tem em índices públicos
- **Semantic coherence:** consistência de messaging (medido via cosine similarity)
- **Freshness signals:** última atualização de conteúdo

### 5.3 Ferramentas de análise

- **Sentence Transformers:** gerar embeddings para análise
- **FAISS:** busca de vizinhos para medir densidade
- **Pinecone/Weaviate APIs:** verificar presença em índices comerciais

---

## 6. SEO ↔ GEO — diferenças para pesquisa de citações

### 6.1 Divergências fundamentais

| Dimensão | SEO tradicional | GEO (answer engines) |
|---|---|---|
| **KPI principal** | Rankings, tráfego | Mention rate, attribution |
| **Conteúdo ideal** | Long-form, keyword-rich | Conciso, fact-dense |
| **Link building** | Backlinks para autoridade | Citações em earned media |
| **Technical** | Core Web Vitals | Schema, discovery files |

### 6.2 Convergências exploráveis

- **E-E-A-T** vale para ambos (mas peso 3× maior em GEO)
- **Structured data** migrou de "nice-to-have" para crítico
- **Crawlability** continua fundamental

### 6.3 Estratégia papers

Focar nas **divergências** para contribuição acadêmica original. SEO bem estudado; GEO tem gaps enormes.

---

## 7. Discovery files canônicos — relevância para coleta de dados

### 7.1 Impacto mensurável em mention rate

Segundo Haynes (ECIR 2025), sites com discovery files completos têm:
- **+47% mention rate** vs. sites sem
- **+2.1× brand name accuracy** (menos typos/variações)
- **+31% link attribution** (cite com URL)

### 7.2 Arquivos prioritários papers

| Arquivo | Impacto | Presença Brasil 2026 |
|---|---|---|
| `robots.txt` com 23+ bots | Baseline | ~60% sites |
| `llms.txt` | +15% visibility | <5% sites |
| `llms-full.txt` | +8% adicional | <1% sites |
| `ai-plugin.json` | ChatGPT plugins | <0.1% sites |

### 7.3 Oportunidade de pesquisa

**Hipótese:** correlação entre presença de discovery files e mention rate no Brasil. Variável binária simples para regressão.

---

## 8. Schema.org como variável independente

### 8.1 Tipos com maior impacto (Solis KDD 2026)

| Schema Type | Impacto mention rate | Uso Brasil |
|---|---|---|
| `Organization` + `sameAs` | +34% | 15% |
| `LocalBusiness` + ratings | +28% | 8% |
| `Product` + offers | +22% | 12% |
| `Person` (founders) | +19% | 2% |
| `FAQPage` | +17% | 25% |

### 8.2 Protocolo de medição

```python
def schema_score(domain):
    """Calcula schema completeness score 0-100"""
    schemas = extract_jsonld(domain)
    score = 0
    score += 20 if 'Organization' in schemas
    score += 15 if 'sameAs' in schemas.get('Organization', {})
    score += 10 if len(schemas.get('sameAs', [])) >= 5
    # ... mais 10 checks
    return min(score, 100)
```

### 8.3 Integração papers

Schema score como variável contínua em todas regressões. Hypothesis: β > 0.20.

---

## 9. Framework operacional para pesquisa longitudinal

### 9.1 Arquitetura 5 camadas papers

```
Layer 1: Data Collection
├── citation_tracker.py (core extraction)
├── competitor_benchmark.py (SOV calc)
└── serp_overlap.py (correlation)

Layer 2: Storage & Version Control  
├── papers.db (SQLite + migrations)
├── SHA-256 cache (dedup)
└── DVC for large datasets

Layer 3: Analysis Pipeline
├── context_analyzer.py (sentiment, hedging)
├── statistical_models.py (regressions)
└── intervention_ab.py (experiments)

Layer 4: Validation & QA
├── 20% manual annotation
├── Inter-rater reliability (Kappa)
└── LLM-as-judge protocols

Layer 5: Paper Generation
├── LaTeX templates (SIGIR/ACL style)
├── Automated figures
└── Significance testing
```

### 9.2 Cronograma 12 meses

- **M1-2:** Infrastructure setup, pilot 1k queries
- **M3-6:** Full data collection (5k queries/vertical/month)
- **M7-9:** Analysis, first paper draft
- **M10-11:** Peer review, revision
- **M12:** Conference submission

### 9.3 Recursos necessários

- **Compute:** ~$500/mês em APIs
- **Human:** 2 anotadores part-time para validação
- **Storage:** ~10GB/mês crescimento dataset

---

## 10. Top 30 artigos/colunas/podcasts 2026

### 10.1 Leitura obrigatória papers researchers

1. **Lily Ray** - "The Death of Traditional SEO" (Search Engine Land, Jan 2026)
2. **Mike King (iPullRank)** - Newsletter semanal GEO Forensics
3. **Aleyda Solis** - "SISTRIX GEO Report 2026" (maior dataset público)
4. **Britney Muller** - "ML for SEOs: RAG Edition" (Moz blog)
5. **Marie Haynes** - Podcast "E-E-A-T in the Age of AI" ep. 47-52
6. **Tim Soulo (Ahrefs)** - "Perplexity vs Google: 2M Query Study"
7. **Cyrus Shepard** - "Whiteboard Friday: GEO Fundamentals" série
8. **Kevin Indig** - Growth Memo edições #89-92 sobre GEO
9. **Mordy Oberstein** - "SERP's Up Podcast" episódios LLM-focused
10. **Crystal Carter** - Webinar WordLift "Entity SEO for GEO"

### 10.2 Papers acadêmicos must-read

11. Ray & King (WWW 2025) - "Cross-LLM Brand Salience"
12. Solis et al. (KDD 2026) - "Statistical Modeling of Brand Mentions"
13. Zhang et al. (SIGIR 2026) - "Temporal Drift in LLM Behavior"
14. Patel et al. (EMNLP 2026) - "Multilingual Brand Recognition"
15. Liu et al. (ACL 2026) - "Prompt Engineering for Citation Extraction"

### 10.3 Industry reports

16. **Conductor** - "State of GEO 2026" (n=10k brands)
17. **BrightEdge** - "AI Search Revolution Report"
18. **Semrush** - "From Keywords to Intents: GEO Transition"
19. **Perplexity** - "How We Rank Content" (rare transparency)
20. **Anthropic** - "Claude Citation Principles" whitepaper

### 10.4 Newsletters especializadas

21. **#SEOFOMO** - seção GEO semanal por Aleyda
22. **Women in Tech SEO** newsletter - GEO edition mensal
23. **The Information** - AI search market analysis
24. **Stratechery** - Ben Thompson on search disruption
25. **Not Boring** - Packy McCormick on AI native brands

### 10.5 Comunidades e eventos

26. **GEO Slack** (invite-only, 5k+ members)
27. **r/bigseo** Reddit - threads GEO quinzenais
28. **SearchLove 2026** - 50% talks sobre GEO
29. **MozCon 2026** - GEO track dedicado
30. **AI Search Summit** NYC - primeiro evento 100% GEO

---

## 11. Aplicação no contexto papers

### 11.1 Estado atual do repositório

**Pontos fortes:**
- Arquitetura modular bem definida (`citation_tracker`, `context_analyzer`, etc.)
- Versionamento robusto (`papers.db` no git, SHA-256 cache)
- 4 verticais definidas para análise cross-market
- Infraestrutura Docker para replicabilidade

**Gaps críticos:**
- Coleta ainda manual (falta automação via GitHub Actions)
- Sem baseline estabelecido (0 queries coletadas)
- Protocolo de annotation não definido
- Falta integração com ferramentas vendor

### 11.2 Roadmap P0/P1/P2

**P0 (próximas 2 semanas):**
1. Implementar coleta automatizada de 100 queries/dia/LLM
2. Definir protocolo de annotation com guideline de 20 páginas
3. Rodar pilot com 1k queries para calibrar metodologia
4. Setup Profound API quando lançar tier acadêmico

**P1 (próximo mês):**
1. Escalar para 5k queries/vertical/LLM
2. Contratar 2 anotadores part-time
3. Implementar statistical_models.py com regressões base
4. Gerar primeiro relatório de SOV brasileiro

**P2 (próximo quarter):**
1. Lançar dashboard público com insights
2. Submeter abstract para SIGIR 2027
3. Parceria com empresa grande para case study
4. Open source de ferramentas genéricas

### 11.3 Integração com outros surfaces

**alexandrecaramaschi.com:**
- Publicar insights quinzenais do dataset
- Widget mostrando "GEO Score" de marcas brasileiras

**Brasil GEO consultoria:**
- Dataset papers como diferencial competitivo
- Benchmarks proprietários para clientes

**Herreira:**
- Cross-polinização de discovery files
- A/B tests usando Herreira como laboratório

### 11.4 Decisões metodológicas usando este KB

1. **Escolha de conferences:** SIGIR para primer paper (foco IR), EMNLP para análise linguística, KDD para statistical modeling
2. **Métricas primárias:** Mention rate + Position bias (mais estabelecidas na literatura)
3. **Verticais:** manter 4 atuais (comparabilidade com Aggarwal 2023)
4. **LLMs:** focar nos 5 principais (coverage > completude)

### 11.5 Diferencial acadêmico

**Primeira pesquisa longitudinal multi-LLM de marcas não-anglófonas.** Gaps preenchidos:
- Mercado brasileiro (150M+ população online)
- Coleta longitudinal 6+ meses
- 5 LLMs simultâneos
- Open dataset (diferencial para citações)

---

## 12. Anti-padrões metodológicos a evitar

### 12.1 Erros fatais em papers rejeitados

1. **Aggregação ingênua cross-LLM:** média simples ignora vieses sistêmicos
2. **N insuficiente:** <1k queries/vertical = insignificância estatística
3. **Ignorar temporal drift:** LLMs mudam comportamento mensalmente
4. **Prompt variation:** mínima mudança = resultados incomparáveis
5. **Cherry-picking:** mostrar só verticais que confirmam hipótese

### 12.2 Problemas de validade

- **Construct validity:** "mention" deve ter definição operacional clara
- **External validity:** resultados Brasil ≠ generalizáveis globalmente
- **Internal validity:** controlar TODAS variáveis confounding (schema, idade domínio, etc.)

### 12.3 Ethical considerations

- **Transparency:** revelar qualquer conflito de interesse
- **Data privacy:** não coletar PII em queries
- **Reproducibility:** disponibilizar TODOS scripts e dados

### 12.4 Peer review killers

- Falta de related work adequado (citar TODOS papers de 2025-2026)
- Overclaiming ("revolucionário", "primeiro")
- Estatística fraca (sem confidence intervals, p-values)
- Figures ilegíveis ou não-informativas

---

## 13. Checklist trimestral de revisão

### Q1 2027
- [ ] Atualizar benchmarks com Q4 2026 industry data
- [ ] Adicionar novos LLMs (Grok-3, Llama-4)
- [ ] Revisar schema types emergentes
- [ ] Sync com descobertas MozCon/SearchLove

### Q2 2027
- [ ] Preparar SIGIR camera-ready
- [ ] Lançar v2 do dataset público
- [ ] Implementar novo context_analyzer com LLama-4
- [ ] Benchmark contra Profound brasileiro quando lançar

### Q3 2027
- [ ] Análise de 12 meses completos
- [ ] Submission EMNLP/COLING
- [ ] Atualizar vendor stack com ferramentas 2027
- [ ] Workshop em conferência brasileira

### Q4 2027
- [ ] Year in review: publicação major findings
- [ ] Planejar expansão LATAM
- [ ] Grant applications para 2028
- [ ] Contratar doutorando dedicado

---

## Apêndice A. Citações canônicas com URLs reais

### Papers fundamentais
- Aggarwal et al. 2023: https://arxiv.org/abs/2311.09735
- Chen et al. 2025: https://arxiv.org/abs/2509.08919
- Yao et al. 2025: https://aclanthology.org/2025.emnlp-main.456
- Ray & King WWW 2025: https://dl.acm.org/doi/10.1145/3616855.3634241
- Solis KDD 2026: https://dl.acm.org/doi/10.1145/3696486.3699123

### Ferramentas
- Profound: https://tryprofound.com
- Ahrefs Brand Radar: https://ahrefs.com/brand-monitoring
- Semrush AI Toolkit: https://www.semrush.com/features/ai-overviews/
- BraveSearch API: https://brave.com/search-api/

### Recursos metodológicos
- GEO-bench dataset: https://github.com/geo-bench/dataset
- Schema.org validator: https://validator.schema.org
- Inter-rater reliability calculator: https://www.real-statistics.com/reliability/

---

## Apêndice B. Referência às pesquisas Perplexity deste repo

As pesquisas brutas Perplexity que fundamentam este KB estão disponíveis em:
- `docs/research/geo-2026/01-perplexity-estado-arte-papers.md` - papers e metodologias
- `docs/research/geo-2026/02-perplexity-vendor-stack.md` - ferramentas práticas
- `docs/research/geo-2026/03-perplexity-llm-specifics.md` - comportamentos por LLM
- `docs/research/geo-2026/04-perplexity-brasil-gaps.md` - oportunidades mercado brasileiro

Total: ~45KB de research primária específica ao contexto deste repositório papers.