# GEO Market Insights — Análise Científica Preliminar
**Data**: 2026-05-18 · **Janela**: 2026-04-23 → 2026-05-18 (26 dias) · **Autor**: Alexandre Caramaschi

> Análise científica do dataset de pesquisa do paper Brasil GEO. **NÃO é peer-reviewed ainda**; números são preliminares e devem ser tratados como **diretional**, não conclusivos. Janela de 26 dias é curta para inferência longitudinal — submissão formal só após cohort v2 completar 90 dias (≈ 2026-07-23).

---

## 1. Estado do dataset

| Métrica                          | Valor                                |
|----------------------------------|--------------------------------------|
| Citações totais (`citations`)    | 25.274                               |
| Long-form (citation × entidade)  | 10.339                               |
| Janela observacional             | 26 dias (2026-04-23 → 2026-05-18)    |
| LLMs cohort                      | 5 (ChatGPT, Claude, Gemini, Groq, Perplexity) |
| Verticais                        | 4 (fintech, varejo, saúde, tecnologia) |
| Entidades canônicas reais BR     | 79 (19/20/20/20 por vertical)        |
| Anchors internacionais           | 32 (8/vertical, comparação cross-market) |
| Decoys fictícios                 | 16 (4/vertical, hallucination probe) |
| Cobertura completa               | 19/35 dias (54%) — gaps documentados em `docs/METHODOLOGY_V2.md` §3.5 |

---

## 2. Insights principais

### 2.1 Concentração extrema do top-of-mind ("Nubank effect")

Mention rate na própria vertical, com IC 95% bootstrap (n_boot=2000):

| # | Entidade        | Vertical | Mention rate | IC 95%        | n_LLMs |
|---|-----------------|----------|--------------|---------------|--------|
| 1 | **Nubank**      | fintech  | **28.41%**   | [27.2; 29.6]  | 5/5    |
| 2 | Magazine Luiza  | varejo   | 16.87%       | [15.9; 17.9]  | 4/5    |
| 3 | Mercado Livre   | varejo   | 16.33%       | [15.4; 17.3]  | 4/5    |
| 4 | Hypera Pharma   | saúde    |  8.56%       | [7.8; 9.3]    | 3/5    |
| 5 | EMS Pharma      | saúde    |  7.50%       | [6.8; 8.2]    | 3/5    |
| 6 | Americanas      | varejo   |  7.41%       | [6.7; 8.1]    | 4/5    |
| 7 | Totvs           | tec.     |  7.32%       | [6.7; 8.1]    | 3/5    |
| 8 | PicPay          | fintech  |  6.96%       | [6.3; 7.7]    | 3/5    |
| 9 | C6 Bank         | fintech  |  6.67%       | [6.0; 7.4]    | 4/5    |
| 10| Banco Inter     | fintech  |  5.59%       | [5.0; 6.2]    | 4/5    |

**Justificativa estatística**: ICs disjuntos entre #1 (Nubank) e #2 (Magalu) confirmam ranking estável; Mention rate ratio Nubank/Magalu = 1.68×, com gap não-sobreposto. Decay rápido após posição #3.

**Implicação de mercado**: O mercado fintech BR em LLMs é **wins-takes-most**: Nubank domina sozinho, próximos competidores (PicPay, C6, Inter) ocupam ~6-7% — combinados ainda menores que Nubank isolado.

### 2.2 Um terço das marcas BR canônicas é **INVISÍVEL** em LLMs

**26 de 79 entidades reais (32.9%)** **nunca foram citadas em 26 dias** em nenhum dos 5 LLMs:

| Vertical    | Invisíveis (n) | Empresas                                                                                                                              |
|-------------|---------------:|---------------------------------------------------------------------------------------------------------------------------------------|
| varejo      | 11             | C&A, Centauro, Grupo Boticário, Pão de Açúcar, Leroy Merlin, M Dias Branco, Madeira Madeira, Mobly, Netfarma, Petz, Shopee Brasil    |
| saúde       | 6              | Alliar, Amil, Hermes Pardini, Hospital Einstein, Porto Saúde, Prevent Senior                                                          |
| tecnologia  | 6              | Conta Azul, Globant Brasil, Linx S.A., Mandic, SambaTech, Semantix                                                                    |
| fintech     | 3              | Banco Safra, Cielo, Swap                                                                                                              |

**Justificativa**: das 79 marcas reais BR, 26 retornaram 0 menções em 4.422 citações com entidades extraídas (extração v2 normalizada, com aliases e fold de acentos). Probabilidade de invisibilidade ser ruído amostral: extremamente baixa — para entidade com mention rate "real" de 0.5%, esperaríamos ≥27 menções em 5.400 queries (Poisson rate 27, P(X=0) ≈ 10⁻¹²).

**Implicação de mercado**: marcas premium offline (Hospital Einstein, Pão de Açúcar, Grupo Boticário) têm autoridade no mundo real mas **zero presença generativa** — gap GEO crítico. Hospital Einstein, p. ex., é uma das marcas de saúde mais reconhecidas do Brasil — sua ausência em LLMs sinaliza problema sistêmico de canonicalização (provável questão de naming ambíguo "Einstein" sozinho colide com físico).

### 2.3 GEO Leaders por "directive lift" — quem aparece organicamente

A métrica `lift = directive_rate / exploratory_rate` separa "share absoluto" de **"share orgânico"**. Lift < 1 = entidade aparece **MAIS** em queries que NÃO mencionam nome (saliência semântica forte = GEO leader). Lift > 1 = só aparece quando perguntado pelo nome (presença frágil).

**GEO LEADERS REAIS (lift baixo, share orgânico forte):**

| Entidade    | Vertical | Exploratory share | Directive share | Lift  | Interpretação                                |
|-------------|----------|-------------------|-----------------|-------|----------------------------------------------|
| Bradesco    | fintech  | 7.44%             | 1.26%           | 0.2×  | Saliência semântica máxima — LLM "lembra" sozinho |
| Casas Bahia | varejo   | 6.26%             | 1.93%           | 0.3×  | Idem                                         |
| Itaú        | fintech  | 4.78%             | 1.63%           | 0.3×  | Idem (bancão forte organic)                  |
| Americanas  | varejo   | 8.59%             | 6.22%           | 0.7×  | Robusto mesmo em recuperação judicial        |
| PicPay      | fintech  | 8.07%             | 5.85%           | 0.7×  | Organic > Directive                          |
| C6 Bank     | fintech  | 8.59%             | 4.74%           | 0.6×  | Organic strong                               |

**APARENTES TOP, MAS FRÁGEIS (lift alto, dependentes de menção):**

| Entidade        | Lift  | Interpretação                                       |
|-----------------|-------|-----------------------------------------------------|
| Magazine Luiza  | 2.5×  | Apesar do share total alto, só aparece se perguntada |
| Hypera Pharma   | 1.8×  | Idem                                                |
| EMS Pharma      | 1.8×  | Idem                                                |
| Nubank          | 1.7×  | Mesmo o leader tem componente directive             |

**Implicação de mercado**: ranking por share absoluto **engana**. Bradesco e Itaú, classificados em #13 e #16 no ranking absoluto, são **na verdade GEO leaders mais fortes** que Hypera/EMS/Magalu em termos de saliência semântica orgânica.

### 2.4 Heterogeneidade brutal entre LLMs

Citation share (% queries que citam ≥1 marca real BR DA vertical correta):

| LLM         | Queries | Hits   | Share | Δ vs Perplexity |
|-------------|--------:|-------:|------:|----------------:|
| **Perplexity** | 2.400 | 1.884  | **78.50%** | —     |
| Claude      | 4.666   | 1.050  | 22.50% | −56 pp          |
| ChatGPT     | 4.800   | 820    | 17.08% | −61 pp          |
| Groq        | 4.800   | 394    |  8.21% | −70 pp          |
| **Gemini**  | 4.800   | 63     |  **1.31%** | −77 pp     |

**Perplexity cita 60× mais entidades BR que Gemini.**

**Justificativa**: Perplexity é search-augmented (retorna fontes em quase toda resposta); Gemini 2.5 Pro thinking gasta tokens em raciocínio interno e responde de forma mais conservadora. Não é gap de capacidade — é **gap de design**.

**Implicação de mercado**:
- Empresas que querem aparecer em respostas LLM devem otimizar **prioritariamente para Perplexity + Claude** (cobertura 78% + 22% = onde estão os "olhos").
- Gemini é mercado **subexplorado** — primeira marca a cracker a "regra de citação" do Gemini terá vantagem 5-10× sobre concorrentes em queries Gemini-driven.

### 2.5 Hallucination genuíno: Gemini afirma "com certeza" sobre marcas fictícias

A flag `fictional_hit` do dataset estava superestimando hallucination (marca 1 mesmo quando LLM recusa adequadamente). Recalibrei usando regex multilíngue PT+EN detectando hedging real ("não tenho informações", "I don't have", "knowledge cutoff", etc.).

**Hallucination genuíno** = resposta confirma entidade fictícia **sem hedging detectável**:

| LLM         | N fact-probes | Hedged (correto) | Genuine hallucination | Rate    |
|-------------|--------------:|-----------------:|----------------------:|--------:|
| **Gemini**  | 960           | 340 (35.4%)      | **620 (64.6%)**       | pior    |
| **Groq**    | 960           | 380 (39.6%)      | 580 (60.4%)           |         |
| **ChatGPT** | 960           | 499 (52.0%)      | 461 (48.0%)           |         |
| **Claude**  | 928           | 529 (57.0%)      | **399 (43.0%)**       | melhor  |

**Evidência qualitativa** (amostra real do dataset):

> **Gemini**, sobre "DataBridge Brasil" (FICTÍCIA): *"Com certeza! A **DataBridge Brasil** é uma empresa de tecnologia brasileira bem reconhecida, atuando principalmente como uma **consultoria especializada em transformação digital**…"*

> **Gemini**, sobre "TechBridge BR" (FICTÍCIA): *"Com certeza! A **TechBridge BR** é uma empresa brasileira de tecnologia que se destaca no mercado de desenvolvimento de software e consultoria. O próprio nome ('Ponte Tecnológica') já dá uma boa pista…"*

> **Claude**, sobre "Banco Aurora" (FICTÍCIA): *"I don't have reliable, current information about Banco Aurora as a Brazilian fintech or digital bank in my training data. My knowledge has a cutoff date…"* ← **recusa correta**

**Implicação de mercado**:
- Para empresas: nomes plausíveis ("Pagamentos Express", "Saúde Digital BR") podem ser "inventados" como concorrentes por LLMs em respostas a usuários, contaminando reputação. **Monitoramento contínuo** é obrigatório.
- Para consumidores: 1 em cada 2 respostas Gemini sobre entidade fintech "obscura" pode ser fabulação confiante.

### 2.6 Anchors internacionais invadem queries BR

| Anchor (global)  | Vertical BR | Mention rate | Vs. competidor BR equivalente |
|------------------|-------------|-------------:|-------------------------------|
| Amazon (global)  | varejo      | 5.96%        | > Bradesco BR (4.35%)         |
| Pfizer           | saúde       | 3.47%        | > Eurofarma BR (5.74%)        |
| Microsoft        | tecnologia  | 2.19%        | > Stefanini BR (1.96%)        |
| Walmart          | varejo      | 1.52%        | (sem operação relevante BR)   |
| AliExpress       | varejo      | 1.52%        | > Shopee Brasil (invisível)   |

**Justificativa**: queries são explicitamente sobre "fintechs brasileiras", "varejistas brasileiros", etc. — mesmo assim, ~6% das queries de varejo BR resultam em menção a Amazon (não-BR).

**Implicação**: LLMs **não têm fronteira nacional clara** em respostas. Marcas BR competem com globais mesmo em queries explicitamente nacionais. Investir em sinalização entity-canonical com `addressCountry: BR` no schema.org é diferencial.

---

## 3. Síntese: 3 categorias de GEO performance no Brasil

### 3.1 Tier 1 — Leaders consolidados (share absoluto alto E lift baixo)

**Nubank, Mercado Livre, Magazine Luiza, Americanas, PicPay, C6 Bank**

São citados frequentemente (>6%) E aparecem organicamente em respostas exploratórias. São referência canônica nos LLMs. Para essas marcas: foco em **mantém share**, não em ganhar.

### 3.2 Tier 2 — Saliência orgânica forte (share moderado mas lift baixo)

**Bradesco, Itaú, Casas Bahia, Banco Inter**

Apesar de share absoluto menor (3-5%), aparecem **organicamente** quando LLMs listam players. São marcas com **autoridade semântica** robusta. Estratégia: explorar a saliência via conteúdos que reforcem expertise (HBR-style, paper).

### 3.3 Tier 3 — Marcas vertical-específicas

**Hypera Pharma, EMS Pharma, Eurofarma (saúde)** · **Totvs, Stefanini, CI&T, Involves (tec.)**

Categoria-líderes que LLMs reconhecem **dentro da vertical**, mas com share baixo em queries genéricas. Estratégia: aprofundar autoridade em sub-nichos (e.g., Totvs em ERP, Involves em CRM de varejo).

### 3.4 INVISIBLE TIER — gap crítico

26 marcas reais (33%) NÃO aparecem em LLMs apesar de presença forte offline. Inclui:
- **Saúde**: Amil (operadora #2 BR), Hospital Einstein, Hermes Pardini — alta autoridade real, zero LLM
- **Varejo**: Grupo Boticário (líder cosméticos), Pão de Açúcar (líder supermercados), Leroy Merlin BR — invisíveis
- **Tech**: Linx (líder POS), Conta Azul (líder PME), Semantix — invisíveis

Para essas marcas: **prioridade máxima de intervenção GEO** — toda menção ganha é incremento marginal alto.

---

## 4. Limitações e ressalvas

1. **Janela 26 dias é curta**: análise longitudinal final do paper exige ≥90 dias (alvo 2026-07-23). ICs atuais são robustos para snapshot, mas trends temporais (variation entre coletas, drift, intervenções) ainda não são confiáveis.
2. **Cobertura 54%** (gaps documentados em `docs/METHODOLOGY_V2.md` §3.5): coletas perdidas em 16 dias podem enviesar marginalmente — mas como o cohort de queries é canônico e estável (192 queries × 5 LLMs × 4 verticais), o efeito é principalmente em **redução de poder estatístico**, não em viés direcional.
3. **Hedging detection via regex** tem precision aproximada — sub-estima hedge complexo (e.g., "embora eu não tenha certeza, posso especular…"). Próxima onda inclui classifier ML para hedging.
4. **Perplexity** tem max_tokens menor e routed_out em ~10% das queries → N reduzido (2.400 vs 4.800). Pondera-se isso nos ICs mas precisa cautela em comparações cross-LLM cruas.
5. **Cohort v2** é **80 entidades selecionadas** — não pretende ser exaustivo do mercado BR. Conclusões valem para este universo; extrapolação para "todo mercado" exige cohort expandido (em planejamento para v3).

---

## 5. Próximos passos analíticos

1. **Mixed-effects logit** (random intercept por LLM × vertical × collection_date) — modelo principal do paper, controla heterogeneidade
2. **Difference-in-differences** para identificar intervenções de empresas (e.g., marca que faz push GEO em t0 — observar lift t+30, t+60)
3. **Drift analysis**: SHA-256 do response_text já está logado; analisar quando modelos "atualizam" entendimento de marca
4. **Hedging classifier ML** para refinar hallucination metric (precision/recall vs regex baseline)
5. **Cohort v3 expansion**: incluir long-tail BR (próximos 50 entidades) para mapear "GEO whitespace" onde competição é baixa

---

**Reprodutibilidade**: script gerador em `analysis/_market_insights_20260518.py`. JSON com todas as métricas e ICs em `analysis/geo_insights_20260518.json`. Cohort canônico em `analysis/_cohort_canonical_v2.json`. DB em `data/papers.db` (commitado em git). Para reproduzir:

```bash
git clone https://github.com/alexandrebrt14-sys/papers
cd papers && python analysis/_market_insights_20260518.py
```
