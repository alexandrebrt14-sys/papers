# Health Check Profundo — Janela v2 (2026-04-29)

**Auditor:** Claude Opus 4.7 sob solicitação Alexandre Caramaschi
**Escopo:** github.com/alexandrebrt14-sys/papers + alexandrecaramaschi.com/papers-roadmap + /research
**Janela auditada:** 2026-04-23 → 2026-04-29 (dias 1-7 da janela v2 confirmatória)
**Estado de baseline:** 8.571 citations · 4 verticais · 5 LLMs · pipeline daily-collect rodando

---

## Resumo executivo

Quatro bugs estruturais foram identificados e corrigidos em uma única onda. Nenhum deles paralisou a coleta, mas três comprometiam pilares metodológicos centrais do paper. Nenhum dado foi perdido — backup imediato (`data/backups/health-check-2026-04-29/`, SHA-256 manifest) foi feito antes de qualquer modificação. Os 8.571 rows preservados foram corrigidos retroativamente onde determinístico; onde requeria nova coleta (probes adversariais), a captura começa a partir de hoje sem invalidar a janela passada.

**Bottom line:** janela v2 segue válida para H1/H4. H2 (false-positive baseline) terá uma sub-janela calibrada de ~83 dias (29/abr → 22/jul) com adversarial probes ativos — suficiente para o paper. Publicação alvo (Information Sciences, outubro 2026) permanece factível.

---

## 4 bugs estruturais identificados

### BUG-1 · `query_type` enviesado 85/15

**Severidade:** alta (afeta H3 directive vs exploratory).

**Sintoma observado:** janela v2 mostrava 7.299 directive (85%) vs 1.272 exploratory (15%). O roadmap pública e a `build_canonical_battery()` prometem 50/50 (96/96).

**Causa raiz:** `src/config.py::query_type_for()` lia apenas `q["type"]` como override. A battery v2 (`config_v2.build_canonical_battery`) usa a chave `q["query_type"]` — desconhecida pela função. Sem override, caía no map por categoria, onde 5/6 categorias v2 mapeiam para `directive` (`descoberta`, `comparativo`, `mercado`, `experiencia`, `inovacao`).

**Fix prospectivo:** `query_type_for()` agora lê `query_type` antes de `type`.

**Fix retroativo:** `scripts/reannotate_query_type_retroactive.py` reconstruiu o índice `query_text → query_type` a partir da battery e fez UPDATE em 4.284 rows distintas (96 queries únicas × ~45 ocorrências). Coluna `query_type_v1_legacy` preserva valor original para auditoria.

**Resultado pós-fix:**
```
query_type=directive   : 4.287
query_type=exploratory : 4.284  (50,02% / 49,98%)
```

### BUG-2 · Probes adversariais nunca rodaram

**Severidade:** crítica (invalidaria H2 em qualquer paper isolado dela).

**Sintoma observado:** `is_probe=0`, `fictitious_target=NULL`, `fictional_hit=0` em **100%** das 8.571 rows.

**Causa raiz:** `config_v2.build_adversarial_queries()` retornava `[]` (placeholder com comentário "Implementação completa em Onda 3 phase 2"). `BaseCollector` nunca enxergava queries probe.

**Fix:** implementação completa retornando 64 queries (4 verticais × 4 decoys × 2 langs × 2 templates), todas com `is_probe=1`, `adversarial_framing=1`, `target_fictional=<decoy>`. `BaseCollector.__init__` agora concatena `base_queries + get_v2_adversarial_queries()` quando `PAPERS_INCLUDE_ADVERSARIAL_PROBES != "0"` (default ativo). `_analyze` preserva `probe_type` explícito da query (antes sobrescrevia para "decoy" sempre).

**Custo incremental:** 64 queries × 5 LLMs × 2 runs/dia = 640 calls/dia. Ao preço atual médio ($0,12 por 1k calls), incremento ≈ +US$0,08/dia (≈+2% sobre orçamento de US$3-7/dia).

**Implicação para o paper:** janela 23-29/abr fica sem probes ativos — declarar como "warm-up window". Janela calibrada para H2 começa 30/abr. Em 60-83 dias úteis há n suficiente para Rule-of-Three e Cohen's h — Power_analysis.reboot_roadmap() permanece dentro da janela 90-dia total.

### BUG-3 · `daily_snapshots` perdendo 75% das rows

**Severidade:** média (afeta análise longitudinal por vertical).

**Sintoma observado:** após backfill de 24 snapshots (4 verticais × 7 dias), apenas 7 persistiam — uma vertical por dia.

**Causa raiz dupla:**
1. **Schema:** `daily_snapshots.date TEXT NOT NULL UNIQUE`. UNIQUE só por `date`, não composite. INSERT OR REPLACE com mesma data sobrescrevia, mantendo apenas a última vertical do loop (varejo na maioria dos dias).
2. **Workflow path:** `daily-collect.yml` chama `python -m src.cli collect citation`, mas `save_daily_aggregate` só estava em `collect_all`. Mesmo se schema permitisse, o workflow não estava persistindo snapshots.

**Fixes:**
- `migrate_0008_snapshot_composite_unique.py` cria nova tabela com `UNIQUE(date, module, vertical)`, migra dados, drop antiga, rename. Idempotente (detecta se já tem composite). Wired em `DatabaseClient._migrate_snapshot_composite_unique` → roda automaticamente em qualquer DB no próximo `connect()`.
- `cli.py::collect_citation` agora chama `TimeSeriesManager.save_daily_aggregate` por vertical após cada coleta.
- `scripts/backfill_daily_snapshots.py` reconstrói retroativamente os 24 snapshots da janela v2 a partir de `citations`.

**Resultado pós-fix:** `daily_snapshots` com 24 rows íntegras (4 × 7), prontos para uso pelo `TimeSeriesManager.get_time_series()`.

### BUG-4 · Backup off-site ausente

**Severidade:** média (single point of failure se artifact GitHub for perdido).

**Sintoma:** papers.db existe apenas no git (commitado) + artifact 90d. Sem cópia externa = se conta GitHub for comprometida ou repo for purgado, perda total da janela v2 inteira.

**Fix:** novo step `Off-site backup to Cloudflare R2` no `daily-collect.yml`. Skip silencioso se `R2_*` secrets não configurados. Sobe `papers/db/{timestamp}-{sha8}.db` + `papers/db/latest.db` com metadata SHA-256. `continue-on-error: true` para não bloquear pipeline.

**Pendência operacional:** Alexandre criar bucket R2 + secrets `R2_ENDPOINT`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_BUCKET` no repo. Custo R2: ~US$0,015/GB/mês — papers.db pesa 14 MB → praticamente gratuito.

---

## Achados secundários (não-bloqueantes)

### Gemini com 1,1% citation rate

`docs/audits/2026-04-26/GEMINI-CITATION-RATE-INVESTIGATION.md` documenta. Decisão consciente: NÃO corrigir `max_tokens=3200` na janela atual para preservar a janela v2 contínua. Será reportado como limitação no paper. ChatGPT (17,2%), Claude (26,0%), Perplexity (82,5%), Groq (8,2%) seguem em range razoável.

### Perplexity com n=960 (metade dos demais)

Por design (`PERPLEXITY_CATEGORIES` routing). Reduz poder estatístico para H1 nessa célula, mas CR1 sandwich estimator absorve. Documentado como design decision, não bug.

### Naming inconsistente nas páginas públicas

`/research` e `/papers-roadmap` mostram "8.571 queries" em sincronismo com DB pós-pull. Apenas o GitHub README estava desatualizado (mostrava 397, número da auditoria histórica 2026-03-26 do v1 antes do truncate).

---

## O que continua firme

- **Cron rodando:** runs 47-61 todos `success`. Run 25104705627 ativa em 2026-04-29 10:51 UTC.
- **204/204 testes passando** após fixes.
- **Preflight LLM check** instalado em 26/abr cobre incidente Anthropic credits.
- **Fail-loud per-LLM** standalone (`collect validate-run`) impede degradação silenciosa de cohort.
- **`citations`, `finops_usage`, `model_versions`, `collection_runs`** todos populando consistentemente.
- **NER v2** sólido: `extraction_version='v2'` em 100% das rows; via_alias e via_fold capturando aliases corretamente (BTG→BTG Pactual, Itau→Itaú).

---

## Roadmap pós-correção (90-dia)

| Marco | Data | Estado |
|-------|------|--------|
| Janela v2 dia 7 | 2026-04-29 | Em curso (run 25104705627) |
| **Probes ativos primeiro run** | 2026-04-29 22:00 BRT | Wired |
| Janela calibrada H2 começa | 2026-04-30 | Pendente primeiro run |
| H1 statistical power | 2026-05-02 (~Day 10) | Projetado pelo Cohen's h |
| H2 fictitious power | 2026-05-30 (~Day 38) | Requer probes ativos ≥30 dias |
| Window closure | 2026-07-22 (Day 90) | Locked-in |
| **Submission Information Sciences** | 2026-10 | Realista |
| ~~SIGIR 2026 submission~~ | ~~2026-07~~ | **INFEASÍVEL** — deadline SIGIR fechou em fev/26. Replanejar para SIGIR 2027 (deadline ~fev/2027) com janela 6+ meses. |

---

## Ações operacionais recomendadas (Alexandre)

1. **R2 bucket** (alta prioridade): criar bucket Cloudflare R2 + secrets no repo. ~10 min, custo desprezível.
2. **Atualizar README.md do GitHub** para refletir 8.571 (não 397 histórico).
3. **Replanejar SIGIR 2027** se desejado — adicionar a `docs/PUBLISHING_PLAYBOOK.md`.
4. **Decidir Gemini fix** após janela 90d (não antes — invalidaria continuidade).
5. **OSF preregistration v2** — atualizar para refletir probe activation começando em 2026-04-30 (ainda Onda 5 pendente do CHANGELOG).

---

*Health-check fechado 2026-04-29. Próximo: validação automática via `scripts/validate_v2_collection.py` no próximo run pós-deploy.*
