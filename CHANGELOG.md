# CHANGELOG

Formato [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) · SemVer.

---

## [v2.2.0-onda16] — 2026-04-29 (Onda 16 — health-check profundo + 4 fixes estruturais)

Auditoria completa da janela v2 (dias 1-7) identificou 4 bugs estruturais que comprometiam pilares metodológicos do paper sem paralisar a coleta. Todos corrigidos sem perda de dados; janela v2 segue válida com calibração H2 a partir de 2026-04-30.

Documento canônico: `docs/audits/2026-04-29/HEALTH-CHECK-DEEP.md`.

### Fixed

- **BUG-1 query_type 85/15 (CRÍTICO)**: `config.py::query_type_for()` lia apenas `q["type"]` como override; battery v2 usa `q["query_type"]` → caía no map por categoria onde 5/6 categorias v2 viram directive. Real era 7299 directive vs 1272 exploratory. Fix: precedência `query_type` → `type` → map. Re-anotação retroativa via `scripts/reannotate_query_type_retroactive.py` corrigiu 4284 rows; janela agora 4287/4284 (50,02% / 49,98%). Coluna `query_type_v1_legacy` preserva valor original.

- **BUG-2 probes adversariais inativos (CRÍTICO)**: `config_v2.build_adversarial_queries()` retornava `[]` (placeholder). 100% das 8571 rows tinham `is_probe=0`, `fictional_hit=0`. Fix: implementação completa com 64 queries (4 verticais × 4 decoys × 2 langs × 2 templates) carregando `is_probe=1`, `adversarial_framing=1`, `target_fictional`. `BaseCollector.__init__` concatena via env `PAPERS_INCLUDE_ADVERSARIAL_PROBES` (default ativo). `_analyze` preserva `probe_type` explícito. Custo +~US$0,08/dia.

- **BUG-3 daily_snapshots perdendo 75% (MÉDIO)**: schema tinha `UNIQUE(date)` simples — INSERT OR REPLACE sobrescrevia entre verticais. Backfill resultava em 7 rows (last vertical) em vez de 28. Workflow rodava `collect citation`, mas `save_daily_aggregate` só estava em `collect_all`. Fix triplo: (1) `migrate_0008_snapshot_composite_unique.py` cria nova tabela com `UNIQUE(date, module, vertical)`, idempotente, wired em `DatabaseClient._migrate_snapshot_composite_unique`; (2) `cli.py::collect_citation` chama `save_daily_aggregate` por vertical; (3) `scripts/backfill_daily_snapshots.py` reconstrói retroativo. Resultado: 24 snapshots persistidos.

- **BUG-4 backup off-site ausente (MÉDIO)**: papers.db existia apenas em git + artifact 90d. Fix: novo step "Off-site backup to Cloudflare R2" em `daily-collect.yml` envia `papers/db/{timestamp}-{sha8}.db` + `latest.db` com metadata SHA-256. Skip silencioso sem secrets. Pendente operacional: criar bucket + secrets.

### Added

- `scripts/reannotate_query_type_retroactive.py` — fix retroativo determinístico do BUG-1.
- `scripts/backfill_daily_snapshots.py` — reconstrói daily_snapshots a partir de citations.
- `src/db/migrate_0008_snapshot_composite_unique.py` — UNIQUE composto.
- `src/config_v2.get_v2_adversarial_queries(slug)` — public helper.
- `tests/test_v2_hot_path.py::test_v2_tracker_includes_adversarial_probes_by_default` — guard contra regressão BUG-2.
- `data/backups/health-check-2026-04-29/papers.db.bak` (sha256 b7d2ae22f776a0…) — snapshot pré-fix preservado.

### Changed

- `config.py::query_type_for()` precedência atualizada (BUG-1).
- `config_v2.build_adversarial_queries()` agora retorna 64 probes reais (BUG-2).
- `collectors/base.py::BaseCollector.__init__` concatena adversarial queries por default (BUG-2).
- `collectors/citation_tracker.py::_analyze` preserva `probe_type` explícito (BUG-2).
- `cli.py::collect_citation` persiste daily snapshot por vertical (BUG-3).
- `db/client.py` chama `_migrate_snapshot_composite_unique` em todo connect.
- Test `test_v2_tracker_loads_cohort_and_battery` agora desliga probes via `monkeypatch` para isolar battery canonical (48 vs 64 com probes).

### Testing

- 204/204 passing (203 antes + 1 novo: probe inclusion default).

### Implicações para o paper

- Janela 23-29/abr declarada **warm-up window** (sem probes).
- **Janela calibrada H2 inicia 2026-04-30**, fechando em 2026-07-22 (~83 dias). Suficiente para Rule-of-Three e Cohen's h projetados.
- SIGIR 2026 (Melbourne, Jul) **infeasível** — deadline fev/2026 já fechou. Re-target para SIGIR 2027 (deadline ~fev/2027), com 6+ meses de janela.
- Information Sciences (Elsevier, IF 8.1, rolling) **realista** para outubro 2026.

---

## [v2.1.0-observability] — 2026-04-23 (Onda 6 — observabilidade + Actions v5)

Onda 6 fecha gaps de observability e dívida técnica de CI identificados durante o reboot.

### Added
- **DriftDetector wire** (`src/collectors/llm_client.py` + `src/collectors/drift_detector.py`): lazy-instanciado, grava `model_versions` row a cada resposta LLM via `_log_drift`. Opt-in via `DRIFT_DETECTION_ENABLED=1` (default). Fix: `detected_change` flag agora é gravado corretamente no INSERT (antes ficava sempre 0). 5 testes novos.
- **CollectionLogger auto-persist** (`src/logging/logger.py`): context manager `run()` agora persiste JSONL automaticamente em `.logs/structured/` via `finally` block. Path aparece como artifact `structured-logs-{run_number}` no workflow daily-collect (retention 30d). Opt-out via `PAPERS_STRUCTURED_LOG_PERSIST=0`. 4 testes novos.
- **Triple-LLM kappa validator** (`src/analysis/kappa_validator.py`): framework interim de inter-annotator agreement. Calcula Cohen's κ par-a-par entre regex NER v2 + 3 LLMs (ChatGPT/Claude/Gemini) + consensus majority-vote. Dependency injection dos extractors para testes sem rede. Landis & Koch interpretation bands. 15 testes novos.

### Changed
- **GitHub Actions** bump em 7 workflows: `checkout@v4→v5`, `setup-python@v5→v6`, `upload-artifact@v4→v5` (Node 20 deprecation cleared).
- **`.gitignore`**: `.logs/` adicionado com `.gitkeep` preservado.

### Fixed
- **`model_versions` drift flag**: `INSERT OR IGNORE` sem coluna `detected_change` fazia com que `get_drift_events()` sempre retornasse lista vazia mesmo em drift real. Agora grava `1 if detected_change else 0`.

### Testing
- **102/102 testes passing** (24 novos na Onda 6 sobre os 78 da Onda 2-5):
  - `test_drift_detector.py` (5)
  - `test_collection_logger_persist.py` (4)
  - `test_kappa_validator.py` (15)

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
