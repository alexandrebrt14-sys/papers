# CHANGELOG

Formato [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) · SemVer.

---

## [v2.0.0-reboot] — 2026-04-23 (Onda 2-5 do reboot algorítmico)

Reboot metodológico pós-Paper 4 (Null-Triad SSRN + Zenodo `10.5281/zenodo.19712217` published). Auditoria em 5 agents paralelos identificou 95+ gaps; este release implementa os P0+P1.

Ver governance completa: `governance/PAPERS-ALGO-AUDIT-2026-04-23.md`.

### Added
- **NER v2** (`src/analysis/entity_extraction.py`): EntityExtractor com NFC+NFKD dual-pass, strip_markup (refs `[1][2]`, `**bold**`, `[link](url)`, HTML, URLs), word-boundary rigoroso, aliases, stop-contexts. 24 testes passando.
- **Cluster-robust CR1** (`src/analysis/cluster_robust.py`): estimador sanduíche com cross-group covariance para H1 diff-proportions.
- **Null simulation Monte Carlo** (`src/analysis/null_simulation.py`): substitui threshold Jaccard arbitrário 0.30 por P5 empírico.
- **Power analysis** (`src/analysis/power_analysis.py`): Rule-of-Three inverse (H2), Cohen's h → n (H1/H4), design effect (H5). `reboot_roadmap()` gera cronograma de dias até target power.
- **Mixed-effects logit** (`src/analysis/mixed_effects.py`): GLMM via `statsmodels.BinomialBayesMixedGLM` com random intercepts aninhados (query, day, entity).
- **Hypothesis engine** (`src/analysis/hypothesis_engine.py`): pipeline canônico de análise. BH-FDR automático + decision rule pré-registrada + export JSON.
- **Config v2** (`src/config_v2.py`): cohort 80 BR + 32 anchors + 16 decoys; query battery 192 balanceadas 50/50 PT/EN + 50/50 directive/exploratory.
- **Migrations DB**:
  - `migrate_0005_ner_v2.py` — 11 colunas `*_v2` + `extraction_version` (forward-only)
  - `migrate_0006_response_hash.py` — SHA-256 response_text para drift detection
  - `migrate_0007_probe_fictitious.py` — `is_probe`, `probe_type`, `adversarial_framing`, `fictitious_target`, `is_calibration` para design factorial H2
- **CLI command** `collect validate-run --since-minutes N`: fail-loud per-LLM **após** loop de verticais (gap B2).
- **Script** `scripts/reextract_citations.py`: re-processa histórico com NER v2 (preserva v1).
- **Dockerfile** + `scripts/reproduce.sh`: ambiente reproduzível com SHA-256 manifest.
- **docs/METHODOLOGY_V2.md**: documento canônico do pipeline v2.

### Changed
- **AMBIGUOUS_ENTITIES expandido**: `Stone`, `Aché`, `EMS`, `Linx`, `Amazon`, `Amil`, `C&A` com canonical_names.
- **Fail-loud per-LLM**: removido de `collect_citation` (rodava per-vertical e matava bash loop); novo comando standalone `collect validate-run` invocado pós-loop no workflow.
- **citation_tracker.py**: distingue `routed_out` (PERPLEXITY_CATEGORIES design decision) de `api_failure` (erro real).
- **`get_real_cohort(slug)`** e **`get_fictitious_cohort(slug)`**: funções separadas. `get_cohort` deprecated para análise científica — pode contaminar cited_count com fictícias.
- **daily-collect.yml**: step `validate-run` adicionado pós-loop de verticais.
- **ENTITY_ALIASES** + **ENTITY_STOP_CONTEXTS**: movidos para `config.py` como single source of truth.
- **LLM cohort**: Groq agora obrigatório em `MANDATORY_LLMS` default.

### Fixed
- **Paper4 Null-Triad gaps**:
  - G1 (diacritic-insensitive): dual-pass NFKD agora captura "Itau" quando cohort tem "Itaú"
  - G2 (UTF-8 NFC): normalização no ingest antes de regex
  - G3 (substring match): removido de `citation_tracker._analyze`; só word-boundary
  - G4 (position ordering): via `text.find()` real em vez de iteração cohort-order
  - G6 (aliases): BTG, XP, C6, Magalu, etc.
  - G7 (stop-contexts): "99%", "floresta amazônica", "emergency medical"
  - G13 (fictitious contamination): separação `cohort_real` vs `cohort_fictitious`
- **FinOps CHECK constraint**: mapping `period='monthly' → prefix='budget'` (mantido, validado).
- **Skipped_or_failed ambiguity**: Perplexity routing filter agora logado como `routed_out` em vez de confundir com `api_failure`.

### Deprecated
- `get_cohort()`: retornado para compat com `citation_tracker.py` v1. Novos códigos devem usar `get_real_cohort()` ou `get_fictitious_cohort()`.
- `analysis/paper4_tables.py` cálculos inline: consolidados em `hypothesis_engine.py`.

### Testing
- **78 testes passing** — toda nova metodologia validada:
  - `test_entity_extraction_v2.py` (24)
  - `test_cluster_robust.py` (6)
  - `test_null_simulation.py` (8)
  - `test_power_analysis.py` (10)
  - `test_config_v2.py` (16)
  - `test_hypothesis_engine.py` (14)

### Re-extraction impact preview
Dry-run NER v2 sobre 2.000 rows históricas:
- v1 cited: 1.409
- v2 cited: 776
- **Delta: -633 (45% de v1 cited=1 eram FPs por substring match)**
- v2-only gains: 6 (novos matches capturados via alias/fold)

---

## [v1.0.0] — 2026-04-22 (Paper 4 submission)

Paper 4 "Null-Triad" submetido. Ver `drafts/null-triad-v1.md` + `build/null-triad.pdf`.

- SSRN: submitted, DOI pending
- Zenodo preprint: `10.5281/zenodo.19712217` published
- GitHub release: `paper-4-submission-v1`

---

## Pendências Onda 5 (próximas 2 semanas)

- **Dataset Zenodo DOI** (separado do preprint): depositar `papers.db` + `CITATION.cff` + schema.sql
- **OSF preregistration v2**: submeter antes do reboot confirmatório
- **DriftDetector wire**: invocar em `LLMClient._log_response`
- **CollectionLogger JSONL** persistido em `.logs/structured/` + artifact upload no workflow
- **Backup daily** papers.db para Cloudflare R2 / S3
- **Actions upgrade**: checkout@v5, setup-python@v6 (Node 20 deprecated)
- **200 rows Cohen's κ** humano-annotated (ou triple-LLM proxy interim)
- **Prompt sensitivity cron** mensal (Bengio gap)
- **Scaling observations** cron trimestral com Gemini Flash + GPT-4o full + Claude Sonnet
- **Dashboard `/admin/papers`** com 4 seções (Scientific Health, Reprodutibilidade, FinOps, Pipeline)
