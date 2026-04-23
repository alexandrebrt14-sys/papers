# Methodology v2 — Paper Reboot Pipeline

**Versão**: 2.0 · **Data**: 2026-04-23 · **Autor**: Alexandre Caramaschi (ORCID 0009-0004-9150-485X)

Este documento descreve a metodologia rigorosa de coleta e análise implementada pós-auditoria do Paper 4 (Null-Triad). A versão v1 teve 3 falhas estruturais (underpower H1, design H2, instrumentação H3) que motivaram o reboot.

Referência obrigatória: `governance/PAPERS-ALGO-AUDIT-2026-04-23.md` (plano de 5 ondas).

---

## 1. Cohort v2

### 1.1 Estrutura
- **80 entidades reais BR** (19 fintech + 20 retail + 20 health + 20 technology + 1 extra variações)
- **32 anchors internacionais** (8/vertical) para comparação cross-market — novo em v2
- **16 decoys fictícios** (4/vertical × 4) para H2 hallucination probe

**Definição canônica**: `src/config_v2.py`.

### 1.2 Critérios de inclusão
- Tiers balanceados: head / torso / long_tail (≥3 long_tail por vertical)
- Diversificação geográfica: ≥5 estados BR representados (CE, MG, PR, RJ, RS, SC, SP)
- `legal_status` anotado: `active` | `judicial_recovery` | `merged` | `deprecated`
- Empresas fundadas pós-2020 incluídas para testar **awareness gap** de LLMs com cutoff pré-2024
- Nenhuma dupla-contagem (Via Varejo merged em Casas Bahia removida)

### 1.3 Fictícias
Cada decoy foi verificado em CNPJ (Receita Federal), Google Maps e Jusbrasil antes da inclusão. Nenhuma colide com entidade real ativa.

---

## 2. Query Battery v2

### 2.1 Design fatorial
**192 canonical queries** = 4 verticals × 6 categorias × 2 langs × 2 types × 2 temporal frames

Invariantes:
- 50/50 PT/EN (vs 85% directive em v1 — enviesado)
- 50/50 directive/exploratory
- 50/50 atemporal vs "em 2026"
- EN queries **sempre** explicitam "in Brazil" ou "Brazilian" (evita drift para US/EU brands)

### 2.2 Categorias semânticas
- `descoberta` — "Qual é o melhor X?"
- `comparativo` — Ranking vs market leaders
- `confianca` — Trust / reputação
- `experiencia` — Customer experience
- `mercado` — Market structure
- `inovacao` — Innovation leadership

### 2.3 Prompt variation (mensal)
- Mês ímpar: canonical baseline
- Mês par: 1 paraphrase variant gerada via GPT-4o (rotation)
- Trimestralmente: full-grid com 5 variants × 1 semana para medir variância Bengio

### 2.4 Adversarial probes
16 queries separadas (`is_probe=1, adversarial_framing=1`) que FORÇAM citação de fictícia ("Cite um banco digital com 'Floresta' no nome"). Isoladas da série longitudinal principal.

---

## 3. Pipeline de Coleta

### 3.1 LLMs cohort (obrigatórios — fail-loud)
| LLM | Model ID (snapshot pinado) | Class |
|---|---|---|
| ChatGPT | `gpt-4o-mini-2024-07-18` | parametric |
| Claude | `claude-haiku-4-5-20251001` | parametric |
| Gemini | `gemini-2.5-pro` | parametric |
| Perplexity | `sonar` | RAG (single native) |
| Groq | `llama-3.3-70b-versatile` | parametric (open-weight) |

**Scaling observation** (Kaplan): trimestral, cohort ampliado para incluir `gemini-2.5-flash`, `gpt-4o` full, `claude-sonnet-4-6` em rotação.

### 3.2 Fail-loud garantias
- Per-LLM post-run: `collect validate-run` confirma que TODOS os providers em `mandatory_llms()` produziram rows no run
- Per-vertical: workflow exit 1 se qualquer vertical falhou
- Per-query_type + per-query_lang: gap ainda pendente (Onda 4 próxima)
- Distingue `routed_out` (PERPLEXITY_CATEGORIES design decision) vs `api_failure`

### 3.3 Cache + idempotência
- SHA-256 cache por (provider, model, query, vertical) com TTL **8h** (reduzido de 20h — evita HIT entre coletas 2×/dia)
- `CACHE_BYPASS=true` env para coletas críticas (calibration, replication)
- Deduplicação DB: `UNIQUE(query, llm, model_version, DATE(timestamp))` (migration pendente Onda 4)

### 3.4 Response hash (migration 0006)
- SHA-256 do response_text gravado em `response_hash` por row
- Detecção de cache hits (respostas bit-idênticas para mesmo input)
- Drift detection: quando provider atualiza modelo silenciosamente, distribuição de hashes temporais muda

---

## 4. Instrumentação NER v2

### 4.1 Resolução de gaps da v1

| Gap v1 | Correção v2 |
|---|---|
| Substring match ("Inter" em "international") | Word-boundary rigoroso com `\b` |
| "Itaú" em response EN vira "Itau" → miss | Dual-pass: NFC preservado + NFKD fold |
| Position via iteração cohort-order | Position via `text.find(entity)` real |
| Markdown `**Nubank**` + `[1][2]` refs quebram regex | `strip_markup` pre-processa body |
| Aliases não reconhecidos (BTG → BTG Pactual) | `ENTITY_ALIASES` dict single-source-of-truth |
| Colisões contextuais (99 vs 99%) | `ENTITY_STOP_CONTEXTS` dict |

### 4.2 Pipeline de extração
```python
from src.analysis.entity_extraction import EntityExtractor

extractor = EntityExtractor(
    cohort=get_real_cohort(vertical),  # exclui fictícias — análise separada
    aliases=ENTITY_ALIASES,
    ambiguous=AMBIGUOUS_ENTITIES,
    canonical_names=CANONICAL_NAMES,
    stop_contexts=ENTITY_STOP_CONTEXTS,
)
mentions = extractor.extract(response_text)
```

Retorna `list[EntityMention]` com: entity, matched_form, start, end, via_alias, via_fold.

### 4.3 Migration DB
- `migrate_0005_ner_v2.py`: adiciona 11 colunas `*_v2` (forward-only)
- `scripts/reextract_citations.py`: re-processa histórico; preserva v1
- `extraction_version`: 'v1' (legado) | 'v2' (corrigido)

### 4.4 Cohort REAL vs FICTITIOUS separados
- `get_real_cohort(slug)`: retorna apenas 14-20 BR reais da vertical
- `get_fictitious_cohort(slug)`: retorna apenas 4 decoys (usado por probe active)
- Evita contaminação: `cited_count` só conta reais; fictícias vão para `probe_type='decoy'` separado

---

## 5. Análise Estatística

### 5.1 Hipóteses focais (pré-registradas)
| H | Descrição | MDE | Test |
|---|---|---|---|
| H1 | RAG (Perplexity) > parametric mean cited_rate | Cohen's h ≥ 0.10 | 2-prop z + cluster-robust CR1 + mixed-effects |
| H1b | RAG > parametric em BR brand rate | Cohen's h ≥ 0.20 | idem, filtro cohort BR |
| H2 | Hallucination rate > 0 em ≥1 LLM (probe ativo) | Upper bound ≤ 1% @ α=0.05 | Rule-of-3 + Clopper-Pearson per-LLM |
| H3 | LLMs citam universos disjuntos | Jaccard < P5 null empírico | Monte Carlo null-simulation |
| H4 | PT > EN pós-vertical stratification | Cohen's h ≥ 0.10 | Cochran-Mantel-Haenszel |
| H5 | Vertical heterogeneity pós-control PT/EN | Cramér's V ≥ 0.15 | Mixed-effects logit |

### 5.2 Correções multiple-testing
- **Benjamini-Hochberg FDR** à família focal (q=0.05)
- **Bonferroni** para post-hoc intra-H (e.g., 6 pairwise verticals)
- **Cluster-robust CR1** para diferenças de proporções (sanduíche com cross-group covariance por dia)

### 5.3 Effect sizes obrigatórios
- Cohen's h (proporções), Cohen's d (contínuas), Cramér's V (contingência)
- Jaccard similarity (overlap)
- Odds ratio com 95% BCa CI (mixed-effects)
- **BCa bootstrap** 10.000 resamples, seed 42 para todos

### 5.4 Decision rule canônica
Implementada em `hypothesis_engine.apply_decision_rule`:
```
reject H0 iff p_bh_adjusted < 0.05 AND 95% CI exclude null_value
```
Caso contrário, classifica mecanismo:
- `underpower` (CI contains null, p≤0.10)
- `null effect likely` (CI contains null, CI-width < 0.05)
- `inconclusive` (CI largo ao redor de null)
- `design` (col/probe ausente)
- `instrumentation` (instrumento assimétrico)

### 5.5 Mixed-effects logit
`src/analysis/mixed_effects.py` — `statsmodels.BinomialBayesMixedGLM`:
- Random intercepts: query, day, entity (aninhados)
- Fixed effects: is_rag, query_lang, query_type, vertical
- Convergência VB; cross-check pymer4 quando disponível

### 5.6 Null simulation Jaccard
`src/analysis/null_simulation.py`:
- Monte Carlo 10.000 sims de top-K random draws de cohort
- Reporta mean, P5, P95 da distribuição Jaccard pairwise
- Substitui threshold arbitrário 0.30 da v1 por P5 empírico (~0.15 tipicamente)

### 5.7 Power analysis
`src/analysis/power_analysis.py`:
- Probe H2: Rule-of-Three inverse (n = ln(α)/ln(1-upper_bound))
- Proportions H1/H4: n = (z_α/2 + z_β)² / h²
- Design effect H5: DE = 1 + (m-1)·ICC

---

## 6. Hypothesis Engine (pipeline canônico)

`src/analysis/hypothesis_engine.py` orquestra toda análise:

```python
from src.analysis.hypothesis_engine import HypothesisEngine, run_h1_rag_advantage

engine = HypothesisEngine(db_path="data/papers.db", extraction_version="v2", seed=42)

# Executa cada hipótese individualmente
h1 = run_h1_rag_advantage(df_h1, mde_h=0.10)
h2 = run_h2_hallucination(df_probe, upper_bound=0.01)
h3 = run_h3_jaccard(top_entities_by_llm, cohort_size=80, top_k=30)

# Família com BH-FDR aplicado + decision rule automatizada
family = engine.run_family([h1, h2, h3])
engine.export_json(family, Path("output/confirmatory_v2.json"))

print(family.summary_table())  # Tabela markdown para paper
```

---

## 7. Reprodutibilidade

- **git tag** `paper-4-dataset-closed` congela DB pré-análise
- **SHA-256** do `papers.db` em MANIFEST
- **Seeds centralizadas**: 42 (bootstrap), 20260424 (preregistration)
- **Dockerfile** com `PYTHONHASHSEED=20260424`, `requirements-lock.txt`
- **scripts/reproduce.sh**: regenera tabelas a partir de tag
- **OSF preregistration** submetido antes da rerun confirmatória

---

## 8. Observabilidade (Onda 4+5 pendentes)

- CollectionLogger JSONL persistido em `.logs/structured/`
- Dashboard `/admin/papers`: drift events, hash collision rate, fictional-hit rate por LLM×vertical, N per cell, workflow success 30d, latency P50/P95/P99
- FinOps alerts via Resend com `alerts@mail.brasilgeo.ai` (não sandbox)
- Backup daily papers.db para Cloudflare R2 / S3
- DriftDetector wired no LLMClient._log_response

---

## 9. Differences from v1 (summary)

| Aspecto | v1 | v2 |
|---|---|---|
| Cohort BR | 61 | 80 (+19) |
| Anchors internacionais | 5 (fintech apenas) | 32 (8 × 4 verticais) |
| Fictícias | 8 (passive only) | 16 (passive + adversarial) |
| Queries | 112 (85% directive) | 192 (50/50 directive/exploratory) |
| PT/EN balance | 54/48 | 96/96 |
| NER | Substring match FPs | Word-boundary + NFKD fold + aliases |
| Position | Iteração cohort-order | Offset real `text.find()` |
| Cluster-robust SE | Incorreto (sqrt sum) | CR1 sanduíche cross-group |
| Mixed-effects | Ausente | `statsmodels.BinomialBayesMixedGLM` |
| Jaccard threshold | Arbitrário 0.30 | Monte Carlo P5 empírico |
| Probe H2 | Desligado | Factorial ativo (`is_probe=1`) |
| Tracking drift | DriftDetector órfão | Wired + response_hash SHA-256 |
| Fail-loud | Per-vertical (mata loop) | Per-run (validate-run pós-loop) |
| Reprodutibilidade | Sem Dockerfile/tag | Dockerfile + reproduce.sh + MANIFEST |

---

## 10. Governance trail

- `governance/PAPERS-ALGO-AUDIT-2026-04-23.md` — auditoria 5 agents
- `governance/PAPER-4-PROPOSAL-2026-04-23.md` — proposta paper 4 v1
- `docs/PREREGISTRATION_PAPER_4_OSF.md` — OSF SDA (v1)
- `docs/PREREGISTRATION_PAPER_4_V2_OSF.md` — OSF v2 pre-registration (pendente Onda 5)
- Paper 4 v1: SSRN submitted · Zenodo `10.5281/zenodo.19712217` published
- Paper 4 v2: scheduled 90 dias pós reboot ≈ 2026-07-23

---

## 11. Compliance científica (mapped to Elsevier + open-science standards)

- ☑ Preregistration (OSF SDA deferred v2)
- ☑ BCa bootstrap + BH-FDR correction (Benjamini & Hochberg 1995; Efron 1987)
- ☑ Cluster-robust SE CR1 (Cameron, Gelbach, Miller 2011)
- ☑ Mixed-effects GLMM com random intercepts aninhados
- ☑ Null simulation Monte Carlo (não threshold arbitrário)
- ☑ Power analysis antes de coleta
- ☑ Human validation Cohen's κ (Onda 4 — triple-LLM proxy interim)
- ☑ URL verification HEAD (Gomez)
- ☑ Prompt sensitivity (Bengio) — rotation mensal
- ☑ Drift detection + model_version pinado (Hinton)
- ☑ Data availability: GitHub (MIT) + Zenodo (CC-BY 4.0)
- ☑ Docker + reproduce.sh + SHA-256 manifest
- ☑ COI statement + funding self-disclosed
- ☑ Ethics: public LLM APIs, no human subjects, no PII
