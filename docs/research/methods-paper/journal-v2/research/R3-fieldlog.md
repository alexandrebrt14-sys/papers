# R3 — Field log: instrument history of BRGEO-1, March to September 2026

**Purpose.** Evidence base for two manuscript chapters: the field report (what broke and what each failure taught about measurement) and the section on instrument drift and honest absence.

**Compiled.** 2026-09-11, against the `papers` repository at `C:/Sandyboxclaude/papers`.

**Evidence rule.** Every claim below carries a file path with line number, or a commit hash, or both. Anything the project remembers without a written record is marked **NOT DOCUMENTED** and must not be asserted in the manuscript without new verification.

**Repository state at compilation.** The working tree sits at `main` = `1db0730` (2026-09-08). `origin/main` is ahead by fourteen commits, the newest being `f4d4534` (2026-09-11). Files introduced after `1db0730` — notably `data/partial_days.json`, `docs/PERPLEXITY_AGENT_API.md` and `governance/CHAVES-COMPARTILHADAS-ENTRE-INSTRUMENTOS-20260909.md` — were read from `origin/main` via `git show` and are cited as such. The divergence is itself an instance of a recurring failure mode recorded in `governance/HEALTH-CHECK-APIS-20260908.md:56`: a stale local clone reporting stale window progress.

**Numbering.** Timeline rows are T1 to T60. Incidents are I1 to I19. The two cross-reference.

---

## 1. Master timeline

Dates are ISO. "Analytic consequence" states what the event does to the series: a stratum boundary, a lost day, a number that moved, or a claim that had to be withdrawn.

### 1.1 Pre-reboot period (v1 series, later discarded)

| # | Date | What changed | Evidence | Analytic consequence |
|---|---|---|---|---|
| T1 | 2026-03-24 | v1 infrastructure ships: seven collection modules, five LLMs, 55 queries, eight-table schema, daily cron at 06:00 BRT and weekly benchmark. Four release entries dated the same day (1.0.0, 1.1.0, 1.2.0, 2.0.0). | `docs/CHANGELOG.md:46-61`, `:37-43`, `:27-34`, `:8-23` | Start of the v1 series. All v1 rows are deleted at T12; no v1 observation survives into the analysed window. |
| T2 | 2026-03-25 21:59 | Commit `0e6e709` introduces an f-string with nested quotes at `src/finops/tracker.py:613`. Valid on Python 3.12 (PEP 701), a `SyntaxError` on the 3.11 used by CI. | `docs/INCIDENT_PIPELINE_2026-03-29.md:20`, `:39-47` | Collection dies at import. Four days lost (see I1). |
| T3 | 2026-03-26 | First statistical audit at N=397: 12/12 items PASS, eight statistical methods verified. | `docs/audits/2026-03-26/README.md:3`, `docs/audits/2026-03-26/EXECUTIVE_SUMMARY.txt:12-15` | A green methodological audit ran while the collector had been dead for a day. The audit examined statistical code, not data arrival. |
| T4 | 2026-03-26 to 2026-03-29 | Daily collection reports "success" in CI and collects nothing, because `\|\| true` masks the import failure. FinOps Monitor fails correctly and is not investigated. | `docs/INCIDENT_PIPELINE_2026-03-29.md:22-26`, `:51-54` | Four days lost (25, 27, 28, 29 March); approximately 768 citations never collected and irrecoverable, because model responses are non-deterministic and vary daily (`:104`). |
| T5 | 2026-03-29 16:51 | Fix applied: `json.dumps()` replaces the f-string; three workflows hardened with an import-validation step; `\|\| true` removed from the critical collection step. | `docs/INCIDENT_PIPELINE_2026-03-29.md:28-29`, `:68-86` | First control designed against silent death. It does not cover the class of failure that arrives next (T6). |
| T6 | 2026-03-30 to 2026-04-07 | All `daily-collect` runs marked "success" while collecting zero data. API keys were rotated externally and never propagated to the `papers` repository; all four providers returned HTTP 401; `continue-on-error` let the workflow exit 0. Supabase dashboard aggregates overwritten daily with zeros. Detected only by manual inspection of the dashboard. | commit `19df1c9` (2026-04-07), message body | Nine further days lost. Second consecutive incident in which the failure is invisible above job-log level. |
| T7 | 2026-04-07 | Three fixes: fail-loud `SystemExit(1)` when zero citations are collected across all verticals; Gemini 2.5 Pro thinking handling (4× `max_output_tokens` for `*-pro`, graceful empty-`parts`); new `daily-collect-alert.yml` firing on `workflow_run` failure. | commit `19df1c9` | The Gemini thinking patch enters here and is the direct ancestor of I6 and of the 2026-06-17 series event (T18). |
| T8 | 2026-04-07 | Anthropic key fingerprint `cfcc92e901a33d04` registered; it remains the project's canonical key through 2026-08-31. | `governance/HEALTH-CHECK-COLETA-20260831.md:55` | Later matters because every Anthropic credit stop is a balance event, not a credential rotation. |
| T9 | 2026-04-22 | Paper 4 "Null-Triad" submitted to SSRN; Zenodo preprint `10.5281/zenodo.19712217` published; GitHub release `paper-4-submission-v1`. | `CHANGELOG.md:351-357` | The diagnosis that authorises the reboot (see I3). |

### 1.2 The v2 reboot and the first month

| # | Date | What changed | Evidence | Analytic consequence |
|---|---|---|---|---|
| T10 | 2026-04-23 | v2.0.0 reboot. Five-agent parallel audit identified 95+ gaps; P0 and P1 implemented in one release: NER v2 (NFC+NFKD dual pass, markup stripping, strict word boundary, aliases, stop contexts), cluster-robust CR1, Monte Carlo null simulation, power analysis, mixed-effects logit, hypothesis engine with BH-FDR, cohort v2 (127 entities), 192-query balanced battery, migrations 0005/0006/0007, Dockerfile. 78 tests passing. | `CHANGELOG.md:285-340`, `governance/DIA-1-MARCO-20260423.md:11` | The instrument the paper describes begins here. Everything before is a different instrument. |
| T11 | 2026-04-23 | Re-extraction dry run of NER v2 over 2,000 historical rows: v1 `cited` 1,409, v2 `cited` 776, delta −633. 45% of v1 `cited=1` were false positives from substring matching; six new matches gained via alias or fold. | `CHANGELOG.md:342-347` | Quantifies the matching-rule effect at roughly a factor of 1.8 on the headline rate. Relevant to the dashboard discrepancy recorded at I19. |
| T12 | 2026-04-23 16:40 | v1 dataset truncated: 18,537 rows deleted. Tag `paper-4-dataset-frozen-20260423`; physical backup at `data/backups/papers.db.pre-reboot-20260423.bak`. | `governance/DIA-1-MARCO-20260423.md:22`, `:37`, `:68` | Hard discontinuity. No comparison crosses this line. |
| T13 | 2026-04-23 20:21 | First v2 collection dispatched in CI (run 24856932674); tag `v2-collection-start-20260423`. Dataset state at the moment: `citations` 0 rows, `collection_runs` 0 rows, schema at 22 tables with 44 columns on `citations`. | `governance/DIA-1-MARCO-20260423.md:25`, `:72-79` | Day 1 of the declared 90-day confirmatory window. Planned close: 2026-07-21 (`:108`). |
| T14 | 2026-04-23 22:22 | That first run cancelled after 101 minutes by concurrency overlap with the 21:00 UTC cron, which itself started 45 minutes late. | `governance/INCIDENT-RUN-CANCELLED-20260423.md:9`, `:14-21` | Zero data loss: the database commit happens at step 16 and the cancel hit step 8. The scheduled run took over day 1. See I4. |
| T15 | 2026-04-24 10:18-10:48 | Anthropic credit exhausted mid-run (#51, run 24884442588). About 15 Claude fintech queries recorded as `api_failure` rows with `cited=False` before `FAILED_VERTICALS` aborted the job. | `docs/audits/2026-04-26/INCIDENT-CLAUDE-CREDITS-2026-04-24.md:25-31`, `:40` | First partial day. Approximately 1.6% of Claude's day-2 rows; distinguishable by `error_type`, so analysis must filter `error_type IS NULL`. Recorded for the limitations appendix. |
| T16 | 2026-04-24 | OSF preregistration v1 recorded as submitted, explicitly framed as a deferred/post-hoc secondary-data-analysis registration, with an honesty clause stating that full blinding is impossible. | `docs/PREREGISTRATION_PAPER_4_OSF.md:11`, `:13` | Superseded on 2026-08-31 by external review finding D3; the current manuscript states plainly that the plan is not registered with an independent third party (`docs/research/methods-paper/MANUSCRIPT.md:419`). |
| T17 | 2026-04-26 | Preflight LLM connectivity and auth check added before the vertical loop: one 1-token call per provider, roughly US$0.0001 total, exit code 2 aborts the job. | `docs/audits/2026-04-26/INCIDENT-CLAUDE-CREDITS-2026-04-24.md:51-66` | The control that later converts credit exhaustion from partial days into declared gaps — and, from 2026-09-09, back into declared partial days (T32). |
| T18 | 2026-04-26 | Gemini investigated at 1.4% citation rate against ChatGPT 17.3% on the same n=960. Leading hypothesis: thinking tokens exhaust `max_output_tokens`, `parts` returns without text, `cited=False` recorded silently. Decision taken: do not fix mid-window. | `docs/audits/2026-04-26/GEMINI-CITATION-RATE-INVESTIGATION.md:9-17`, `:23-53`, `:86-117` | A known suspected instrument defect deliberately carried for the sake of series continuity. The anomaly is re-explained on 2026-08-31 by a different mechanism (I13, I17). |
| T19 | 2026-04-29 | Deep health check of window days 1-7 finds four structural bugs: `query_type` skewed 85/15; adversarial probes never executed (`is_probe=0` on 100% of 8,571 rows); `daily_snapshots` losing 75% of rows to a non-composite UNIQUE; no off-site backup. All fixed; 4,284 rows retroactively re-annotated; 204/204 tests. | `CHANGELOG.md:213-250`, `docs/audits/2026-04-29/HEALTH-CHECK-DEEP.md:19-79` | 2026-04-23 to 2026-04-29 declared a **warm-up window** without probes. The H2 calibrated sub-window starts 2026-04-30 (`CHANGELOG.md:254-255`). SIGIR 2026 declared infeasible; re-target Information Sciences, October 2026. |
| T20 | 2026-05-18 | Missingness audit for 2026-04-14 to 2026-05-18: 19 of 35 days with all 20 LLM×vertical cells filled (54%); 16 days total gap (45.7%); five partial days itemised with cause. Zero-imputation policy written. | `docs/METHODOLOGY_V2.md:116-133` | The first published missingness ledger. Note the window start of 2026-04-14 precedes the declared v2 start of 2026-04-23 by nine days; the table's first row ("GAP TOTAL, 9 dias") is that pre-window interval. The inconsistency is unexplained — see §5.4. |

### 1.3 Cost, persistence and the first series event

| # | Date | What changed | Evidence | Analytic consequence |
|---|---|---|---|---|
| T21 | 2026-06-05 | Gemini made optional in the gates: `preflight_llm_check.py` and `health_check.py` honour `MANDATORY_LLMS`, set to `ChatGPT,Claude,Perplexity,Groq`. `GEMINI_THINKING_BUDGET` introduced at 1024. Commits `29152b4`, `cf802fe`, `1cedf14`. | `docs/ROADMAP_2026Q2-Q4.md:22-38` | Gemini failure degrades with a warning instead of zeroing the day. State at the time: 54,980 citations; arm balance ChatGPT 12,672 / Claude 12,506 / Gemini 12,138 / Groq 12,672 / Perplexity 4,992 (`:33`). |
| T22 | 2026-06-11 07:44 | `data/papers.db` reached 103 MB; GitHub rejects files above 100 MB at the pre-receive hook. Push failed, cascading into the R2 backup, the Vercel revalidation and the daily email. Database removed from git (PR #20, commit `3c25cbc`). | commit `3c25cbc` | The database stops being versioned. Every later progress claim depends on pulling the correct copy, which is the mechanism behind I16. |
| T23 | 2026-06-11 07:50 | PR #21 (`ef12647`) finds that `weekly-calibration.yml` did only `git add data/papers.db` plus push. After #20 the `.gitignore` would filter the file and the push would be a silent no-op: calibration would run, modify the database, and have the result discarded when the runner was destroyed. | commit `ef12647` | A weekly instrument-calibration path that would have failed invisibly, caught before it ran. Same class as I8 and I12. |
| T24 | 2026-06-11 08:13 | PR #22 (`19ab6a3`) adds the R2 restore step, adopting the larger base between artifact and R2, forward-only, with silent skip when secrets are absent and `continue-on-error`. | commit `19ab6a3` | Written as the fix for a single point of failure; inert for the next two months (I12). |
| T25 | 2026-06-11 | Run #155 (27351297994) fails on the coverage health check: 216 observations in one vertical of four. The dashboard was regenerated from that small base instead of the recovered 62,820, because the recover workflow's artifact was invisible to `daily-collect.yml`. Resolved in run #156 the same night. | `docs/INCIDENT_RUN155_FINOPS_GEMINI_2026-06-17.md:9-30` | A published figure was produced from 0.3% of the dataset and reported as a run outcome. |
| T26 | 2026-06-17 | FinOps ceiling for Google stuck at US$50 and hit 108% (`is_blocked`) because the ceiling lives in the restored SQLite table and `_ensure_budgets()` only INSERTs, never UPDATEs. Fixed by commit `5c269e0` plus a reconcile step on every run. | `docs/INCIDENT_RUN155_FINOPS_GEMINI_2026-06-17.md:48-65` | A budget guard would have blocked a provider that had already been refilled. Recorded gotcha: the local database diverges from CI (global ceiling 200 local vs 165 in CI), so the local copy is never the FinOps source of truth (`:64-65`). |
| T27 | 2026-06-17 | Gemini AI Studio prepaid wallet exhausted: credit balance −R$3.59, last top-up R$400.00 on 2026-06-11 consumed in about six days, auto-reload OFF. Consumption: April R$0.00, May R$334.57. | `docs/INCIDENT_RUN155_FINOPS_GEMINI_2026-06-17.md:67-79` | Root cause of the recurring Gemini gaps is a billing setting, not an API behaviour. |
| T28 | 2026-06-17 19:28 | **Series event.** Gemini switched from `gemini-2.5-pro` to `gemini-2.5-flash`, `GEMINI_THINKING_BUDGET` from 1024 to 0, and Gemini returned to `MANDATORY_LLMS` (5/5). Commit `f43a42b`. Stated motive: 2.5 Pro thinking tokens were about 91% of the paper's LLM cost. | commit `f43a42b`; `docs/METHODOLOGY_V2.md:91-92`; `docs/research/methods-paper/MANUSCRIPT.md:186` | Model identity and generation configuration changed in the same commit. Pre- and post-boundary observations are not comparable within the Gemini arm. See I9 and I18. |

### 1.4 Persistence, arm replacement and the instrument defect

| # | Date | What changed | Evidence | Analytic consequence |
|---|---|---|---|---|
| T29 | 2026-08-10 | The R2 restore added on 2026-06-11 had authenticated with four S3 secrets that were never created; every run took the silent-skip branch, so no off-site backup existed at all. With the restore inert, both weekly workflows fell back to an artifact download without an explicit `workflow:` and looped on their own degraded copy: they published `papers-db-latest` with 864 citations while `daily-collect` held 63,940, ran the weekly analysis on 1.4% of the dataset, and reported success. Fixed by `bba851f` (REST-API `r2_sync.py`, `db_integrity_guard.py` high-water mark in `data/db_floor.json`, `R2_REQUIRED=1`). | commit `bba851f` | Two months of weekly analyses ran on a dataset two orders of magnitude too small and were never flagged. See I12. |
| T30 | 2026-08-10 | Failure alerts re-triaged: 429 means top up billing, 401 means rotate the key, a degraded integrity guard means do not re-run. Issues deduplicated after one cause produced seven open issues in two weeks. Commit `3ba5c34`. | commit `3ba5c34` | The alert had been instructing the operator to rotate every key on a failure that was actually exhausted credit. Wrong diagnosis in the alert costs the same as no alert. |
| T31 | 2026-08-10 | Integrity floor raised after run #280: citations 63,940 → 65,060; `collection_runs` records 272 `aborted` against 244 `success`, so the 59-day gap becomes part of the record. On first use the R2 restore adopted the R2 base (153,785 rows) over the local one (151,099) after the artifact resolved to −1 rows — the June failure mode. Commit `79b5021`. | commit `79b5021`; `data/db_floor.json` | First time the aborted-run count is published alongside the success count. This ratio becomes the manuscript's missingness denominator. |
| T32 | 2026-08-14 | The integrity gate merged on 2026-08-10 queried `llm_calls`, a table that never existed; the FinOps tracker writes to `finops_usage` (58k+ rows, healthy). Every scheduled run since the merge aborted at the gate. Commit `e94ccbd`. | commit `e94ccbd` | A guard installed four days earlier to prevent silent data loss was itself blocking every run for a reason unrelated to data. |
| T33 | 2026-08-16 21:00 BRT | Last Groq observation. | `CHANGELOG.md:184` | End of the fifth arm as originally constituted. |
| T34 | approx. 2026-08-17 | Groq retires `llama-3.3-70b-versatile` (HTTP 404 `model_not_found`). Five consecutive collections abort at preflight (runs #294-#298, issue #52). | `CHANGELOG.md:180-186`; commit `37a7f3a` | Provider-initiated instrument change. The project did not choose the boundary and could not defer it. |
| T35 | 2026-08-19 | **Series event.** Fifth arm replaced: Groq out, xAI Grok `grok-4.6` in (literal id; `grok-latest` points at an older model). `provider="xai"`, `_query_xai`, `check_grok` preflight, `MANDATORY_LLMS` updated in default, workflow and repository variable, `XAI_API_KEY` secret, FinOps table for xai (US$2/US$6 per Mtok, monthly ceiling US$25). Same commit delegates TLS to the OS certificate store via `truststore` (antivirus MITM producing intermittent `CERTIFICATE_VERIFY_FAILED`; `VERIFY_X509_STRICT` on Python 3.13 makes the classic `SSL_CERT_FILE` fix inert). Commits `37a7f3a`, `a8fb976`. | `CHANGELOG.md:165-195`; `docs/METHODOLOGY_V2.md:72-77` | Pre- and post-boundary observations in the fifth arm are not comparable. `drift_detector` and temporal cuts must treat 2026-08-17→19 as gap plus boundary. The TLS change is explicitly declared to have no effect on collected data (`CHANGELOG.md:172-176`). |
| T36 | 2026-08-23 | First Grok observations persisted (206 rows in the arm that day, under default reasoning effort). Last day persisted before the eight-day stall. | `docs/METHODOLOGY_V2.md:87-90`; `governance/HEALTH-CHECK-COLETA-20260831.md:23` | Those 206 observations fall on the wrong side of the 2026-08-31 reasoning-effort boundary. Declared decision: discard 2026-08-23 in the Grok arm rather than stratify, because 206 of roughly 18,000 per-arm observations make discarding cheaper. |
| T37 | 2026-08-23 21:05 and 2026-08-24 09:16 | Two runs barred at preflight by xAI balance. | `governance/HEALTH-CHECK-APIS-20260908.md:36` | |
| T38 | 2026-08-24 to 2026-08-30 | Five runs cancelled at `timeout-minutes: 180`. In run 33303260035 the Grok arm consumed 129 of 179 wall-clock minutes (72%) against Gemini 17, Claude 15, ChatGPT 12, Perplexity 5; the job died with the fourth vertical half-collected. About 900 GitHub Actions minutes burned without persisting a single day, with the Actions budget already at 514%. | `governance/HEALTH-CHECK-COLETA-20260831.md:35`; `CHANGELOG.md:136-147` | Eight days with no persistence (last persisted day 2026-08-23). See I13. |
| T39 | 2026-08-28 to 2026-09-06 | Twelve runs barred at preflight by Anthropic 400 "credit balance is too low". | `governance/HEALTH-CHECK-APIS-20260908.md:36` | |
| T40 | 2026-08-31 | **Series event.** Grok runs with `reasoning_effort=low` (`XAI_REASONING_EFFORT`, default `low`; `none` rejected with HTTP 400). Measured against the API with the collection's own citation query: 73.7 s and 2,746 reasoning tokens without the parameter, 19.7 s and 419 with `low`. Pinned model unchanged; forward-only. Commit `ee5144c`. | `CHANGELOG.md:136-148`; `governance/HEALTH-CHECK-COLETA-20260831.md:27-37` | Generation configuration changed mid-series in one arm: separate stratum. Side effect: about US$3.20 less per run in reasoning tokens. |
| T41 | 2026-08-31 | **Series event.** Observation window unified. `apply_citation_window` becomes the single decision for all six arms, configurable by `PAPERS_CITATION_WINDOW_CHARS` (200 default; 0 = whole response, which is how the sensitivity analysis runs). Commit `c8ba558`. | `CHANGELOG.md:81-93`; `docs/METHODOLOGY_V2.md:159-170` | Perplexity's citation rate falls from 75.7% to 51.9% under the uniform window: 23.8 points were instrument. The other five arms do not move, which is the identity operation and not independent confirmation. See I14. |
| T42 | 2026-08-31 | `response_full_text` and `citation_window_chars` added (migration 0010) with a backfill annotating the effective window of each historical row from `length(response_text)`. `scripts/harmonize_citation_window.py` produces `cited_win`, `cited_count_win`, `first_entity_win`, `window_applied` without destroying the original columns, after a SHA-256 backup with manifest. | `CHANGELOG.md:113-124` | Auditability is forward-only. No observation before 2026-08-31 can be re-extracted by a third party. See I15. |
| T43 | 2026-08-31 | Perplexity added to the probe stratum. `PERPLEXITY_CATEGORIES` had never included `calibracao_fp`, so the retrieval-augmented arm had zero rows with `is_probe=1` and the false-positive baseline measured only the five parametric arms. Cost of inclusion about US$0.64/day. | `CHANGELOG.md:99-104`; `docs/research/methods-paper/MANUSCRIPT.md:316-318` | H2 figures published before this date describe five parametric arms only, and omit the case that motivates the hypothesis. |
| T44 | 2026-08-31 | Refusal separated from hallucination. Of 16,579 responses flagged as hallucination, 11,195 (67.5%) carry an explicit refusal marker; a stricter regex yields 11,100 (67.0%), with only 95 cases (0.6%) matching on the weak alternant alone. Three-way taxonomy specified: ontological refusal, epistemic refusal, fabrication. | `governance/HEALTH-CHECK-COLETA-20260831.md:145-165`; `docs/research/methods-paper/MANUSCRIPT.md:306-314` | The publishable false-positive figure is roughly a third of the 97% previously implied. The taxonomy is proposed and never measured: no kappa, no gold standard, no confusion matrix. See I17. |
| T45 | 2026-08-31 | Migration 0010 itself fell into a silent skip: called from inside `_migrate_add_vertical`, it ran before the `executescript` that creates `citations`, died on "no such table", and the `except` turned the failure into a DEBUG log. Moved next to migrations 0005/0006/0007 with a regression test that fails if a fresh database is born without the columns. | `CHANGELOG.md:106-111`; `governance/HEALTH-CHECK-COLETA-20260831.md:131-137` | The fix for an auditability defect was itself unauditable on any new database. Same pattern as T29. |
| T46 | 2026-08-31 | Three guards installed, one per pipeline stage: `scripts/distribution_guard.py` in `daily-collect.yml` without `continue-on-error`; `scripts/manuscript_guard.py`; plus two analysis fixes (prominence normalised by the declared window rather than observed length; panel membership defined by activity in the recent window anchored to the last data timestamp rather than by observation count). 21 new tests. | `CHANGELOG.md:7-36`; commit `51159fd`; `governance/ASSINATURA-DISTRIBUCIONAL-20260831.md:68-148` | The panel fix changes which arms enter the breadth component: fintech now holds ChatGPT, Claude, Gemini, Grok and Perplexity, without Groq. The prominence fix moves no published number under a fixed window and matters only at `--window 0`. |
| T47 | 2026-08-31 | External adversarial review of the manuscript: four submission blockers, seven substance corrections, the field's founding citation corrected, and six verified references covering March to July 2026. | `governance/REVISAO-EXTERNA-PAPER-20260831.md` | Two published claims withdrawn (§4.4 mechanism and §7.2 aggregation stability). See I17. |
| T48 | 2026-08-31 | Founding citation corrected in four canonical documents: "Aggarwal SIGIR 2023" with DOI 10.1145/3539618.3594249 replaced by Aggarwal et al. (2024), KDD '24, pp. 5-16, DOI 10.1145/3637528.3671900, arXiv:2311.09735. Commit `3cc4810`. Traced to `docs/research/geo-knowledge-2026/01-perplexity-academic-papers-llm-citations.md`, raw research output that confabulated DOI and title; the file was annotated rather than deleted. | `governance/REVISAO-EXTERNA-PAPER-20260831.md:173-185` | Not an instrument event, but the same failure class: an unverified artefact propagated into four documents because nothing required the identifier to resolve. |

### 1.5 September: credit, transport and the partial-day policy

| # | Date | What changed | Evidence | Analytic consequence |
|---|---|---|---|---|
| T49 | 2026-09-03 to 2026-09-08 | `test.yml` red on every push, with no defect in the instrument. The distribution guard's `avaliar()` hardcoded `timestamp >= now − 2 days` while `coletar_perfil()` honoured `--since-days`; the unit tests fix rows at 2026-08-31, so they passed on the day the guard was written and began failing two days later. Fixed by PR #57, commit `6a5ea63`. | commit `6a5ea63`; `governance/HEALTH-CHECK-APIS-20260908.md:60` | Six days of red CI on the guard installed to protect the instrument. Time-relative fixtures in a time-sensitive guard expire silently. |
| T50 | 2026-09-06 and 2026-09-07 | Two days collected with three arms only (Gemini, Grok, Perplexity). `MANDATORY_LLMS` had been downgraded as a repository variable to `Gemini,Perplexity,Grok` on 2026-09-07 at 23:15 UTC, making ChatGPT and Claude optional against the methodology. | `governance/HEALTH-CHECK-APIS-20260908.md:15`, `:44`; `git show origin/main:data/partial_days.json` | Two methodologically incomplete days. The health check states the decision belongs to the design, not the pipeline: mark as incomplete or exclude from the between-engine comparison (`:99`, item 4). |
| T51 | 2026-09-08 09:10 UTC | Cron still barred at preflight: OpenAI 429 "no credits remaining", Anthropic 400 "credit balance is too low", Perplexity 401 `insufficient_quota`. At 12:30 UTC, after manual top-up in the three consoles, preflight passed 5/5 (ChatGPT 570 ms, Claude 737 ms, Gemini 1,908 ms, Perplexity 1,641 ms, Grok 3,376 ms). | `governance/HEALTH-CHECK-APIS-20260908.md:13` | |
| T52 | 2026-09-08 | Accounting of 2026-08-16 to 2026-09-08: 49 runs, of which 3 succeeded, 28 failed at preflight on balance or model, 17 were cancelled on timeout or concurrency, and 2 failed in collection. Of the 35 days between 2026-08-05 and 2026-09-08, 13 have data. Seventeen days of series lost. | `governance/HEALTH-CHECK-APIS-20260908.md:21-40` | The forecast recorded on 2026-08-10 was a close on 2026-09-28 with 49 days left to collect; between 2026-08-10 and 2026-09-08, 29 days passed and 12 entered the series. The 17-day difference is the cost of the credit gap (`:46`). |
| T53 | 2026-09-08 | Local clone found 13 commits behind with a `papers.db` from 2026-06-17 holding 58,340 rows; `window_progress.py` read over it reported 38 days collected and a close on 2026-10-30. `python scripts/r2_sync.py pull` (forward-only; adopted R2's 206,121 rows over the local 140,413) corrected the reading to 53 days and 2026-10-15. | `governance/HEALTH-CHECK-APIS-20260908.md:56` | Rule recorded: pull from R2 before citing any progress figure; the clone's database is a working copy, not the source. |
| T54 | 2026-09-08 17:16-19:32 UTC | Manual run 34256141784 (`vertical=all`), 135 minutes, all steps green. Per-arm rows and rates: ChatGPT 233 / 38.6%, Claude 233 / 42.5%, Gemini 233 / 25.8%, Grok 233 / 44.6%, Perplexity 144 / 62.5%. Probes: 320 marked rows, 0 spontaneous hits in 756 responses. Integrity floor raised: `citations` 65,060 → 86,543, `collection_runs` 516 → 672. | `governance/HEALTH-CHECK-APIS-20260908.md:81-91` | Window at 53 of 90 collected days; projected close 2026-10-15. |
| T55 | 2026-09-08 | Perplexity Agent API implemented behind repository variable `PAPERS_PPLX_AGENT_API` (default `0`). PR #58, commit `87ac7a2`. | `governance/HEALTH-CHECK-APIS-20260908.md:62-77`; `git show origin/main:docs/PERPLEXITY_AGENT_API.md` | Scheduled external boundary: Perplexity retires `POST /chat/completions` on 2026-09-27, announced 2026-08-13, eighteen days before the projected window close. Without the switch the series stops with 37 days missing. See I18. |
| T56 | 2026-09-09 | Shared API keys documented as a risk: the six keys in `papers/.env` are identical to those in `geo-orchestrator/.env`, and the Anthropic key of the brand-citation cron is the same as the morning digest's. Between 2026-08-28 and 2026-09-08 three independent measurements stopped at the same time for the same reason. | `git show origin/main:governance/CHAVES-COMPARTILHADAS-ENTRE-INSTRUMENTOS-20260909.md:9-17` | Failure correlation between series that are presented together as independent. Also makes the FinOps ceiling in `papers` measure only part of the actual spend on the shared account (`:22`). |
| T57 | 2026-09-09/10 | **Policy change.** `PAPERS_PREFLIGHT_MODE=degrade` becomes the default: a mandatory provider without credit or quota is removed from `MANDATORY_LLMS` via `GITHUB_ENV`, the day is recorded as partial in `data/partial_days.json`, and collection continues if at least `PAPERS_MIN_LLMS` remain. `strict` restores the previous abort. Instrument failures still block. Same commit fixes the public dashboard (fictitious decoys were 8 of the 30 entries in `topEntities`; fintech coverage read 118.8%; `windowEnd` was published as 2026-07-21 while the last collection was 2026-09-09). Commit `427ab00`. | `git diff HEAD origin/main -- CHANGELOG.md` (entry `[integridade] — 2026-09-09`); commit `427ab00` | Direct reversal of the doctrine recorded on 2026-08-31 that an absent day is preferable to a partial day. Both are documented; the September rule supersedes the August one and the manuscript must state which regime each day belongs to. |
| T58 | 2026-09-10 and 2026-09-11 | Further partial days recorded automatically by the degrading preflight, with the Actions run URL as source: 2026-09-10 missing Claude and Gemini in one run and ChatGPT and Claude in another; 2026-09-11 missing ChatGPT. | `git show origin/main:data/partial_days.json` | Three of the four September partial days come from credit exhaustion at three different providers. |
| T59 | 2026-09-10 | Methodological addendum §13 published: `absorption_status` and `selection_status` declared proxies rather than observations; the `null effect likely` label declared not a formal equivalence test; the pre-registration markings in §7 and §11 declared insufficient evidence of a completed public registration. Does not alter the instrument, the hypotheses, the extractor, the cache or the prompts. Commit `3766b59`. | `git diff HEAD origin/main -- docs/METHODOLOGY_V2.md` (§13, lines 398-444 of the new file) | Semantic retraction without instrument change: the vocabulary of the code had been licensing a stronger reading than the observation supports. |
| T60 | 2026-09-11 | Published dashboard state: `collectedDays` 56, `calendarDay` 90, `windowStart` 2026-04-23, `windowEnd` 2026-10-15 (projected), `windowEndCalendar` 2026-07-21, `windowRemainingDays` 34, `totalQueries` 91,392, `collectionRounds` 348, `overallRate` 36.3. | `git show origin/main:data/dashboard_data.json` | The declared 90-day window is a window of ninety **collected** days, not ninety calendar days. The calendar 90th day passed on 2026-07-21 with 56 days collected by 2026-09-11. |

---

## 2. Incidents in depth

Each entry follows the same order: what happened, how it was detected, why the existing controls did not catch it, the fix, and the generalisable lesson for anyone measuring citation in generative engines.

### I1. The pipeline died for four days behind a green CI (2026-03-25 to 2026-03-29)

**What happened.** A commit adding Groq support introduced an f-string with nested quotes at `src/finops/tracker.py:613`. The syntax is legal on Python 3.12 and a `SyntaxError` on the 3.11 that CI ran. The import chain is `cli.py → collectors/__init__.py → base.py → finops/tracker.py`, so every `python -m src.cli` command failed before executing any logic (`docs/INCIDENT_PIPELINE_2026-03-29.md:56-62`).

**How it was detected.** Not by the collection pipeline. The FinOps Monitor, which had no `|| true`, failed correctly for three days and nobody looked; the Weekly Benchmark failure on 2026-03-29 at 11:22 started the investigation (`:26-27`).

**Why the controls missed it.** `daily-collect.yml` ran `collect citation || true`. The workflow reported success. Automatic commits continued, because `git diff --cached --quiet || git commit` committed refreshed documentation even with no new data (`:51-54`).

**The fix.** `json.dumps()` replaced the f-string; an import-validation step was added ahead of any collection in three workflows; `|| true` was removed from the critical step and replaced by `continue-on-error: true` on the non-critical one (`:68-86`).

**Lesson.** A collection pipeline's success criterion must be a property of the data, not the exit code of the job. The incident report states the rule directly: success in CI does not mean data was collected, and the criterion must be verifiable — that the database grew, that `collection_runs` has a new record (`:119-120`). Four days and about 768 observations were lost and are irrecoverable, because model responses are non-deterministic and cannot be re-collected for a past date (`:104`).

### I2. Nine days of green runs with zero data after an external key rotation (2026-03-30 to 2026-04-07)

**What happened.** API keys were rotated outside the repository and never propagated to the `papers` secrets. All four providers returned HTTP 401. The workflow continued under `continue-on-error` and exited 0. The Supabase dashboard aggregates were overwritten daily with zeros: `overall_rate=0`, `total_observations=0`, `days_collecting=0` (commit `19df1c9`).

**How it was detected.** By manual inspection of the published dashboard, nine days in.

**Why the controls missed it.** The control installed eight days earlier (I1) validated imports, not authentication, and not the volume of collected rows. The pipeline had learned to detect one shape of silence and met a different one.

**The fix.** Three, in one commit: fail-loud `SystemExit(1)` when zero citations are collected across all verticals; handling for Gemini 2.5 Pro thinking exhausting `max_output_tokens`; and a new `daily-collect-alert.yml` firing on `workflow_run` failure with a key-rotation runbook.

**Lesson.** Fail-loud on an aggregate that cannot be zero in a healthy run is cheap and catches an open-ended class of causes, while a check tied to one known cause catches only that one. The zero-citation guard would have caught I1 as well.

### I3. The v2.0.0 reboot and what Paper 4 had diagnosed (2026-04-22 to 2026-04-23)

**What Paper 4 concluded.** "Three Ways to Fail to Conclude" reports three dominant market claims that failed to be rejected at N=7,052 over 12 days, and its organising contribution is that they failed by three independent mechanisms (`docs/outlines/PAPER_4_NULL_TRIAD.md:7`):

- **H1, underpower.** The RAG-advantage test had about 1.0k Perplexity observations against a corrective design calling for about 4.2k (`:19`).
- **H2, a design that produces a null by construction.** The hallucination probe was switched off: the corrective action listed is to activate `INCLUDE_FICTITIOUS_ENTITIES=true` (`:20`). A hypothesis about fictitious-entity citation was tested on a design that never asked about fictitious entities.
- **H3, asymmetric instrumentation.** Citation universes were compared using `sources_json`, a field that different providers populate differently; the corrective action is to extract `cited_entities` from the response body and ignore `sources_json` (`:21`).

**What the reboot did.** On 2026-04-23 the P0 and P1 items from a five-agent audit that found 95+ gaps were implemented in one release: NER v2, cluster-robust CR1, Monte Carlo null simulation replacing an arbitrary Jaccard threshold of 0.30 with an empirical P5, power analysis, mixed-effects logit, a hypothesis engine with automatic BH-FDR and a pre-registered decision rule, cohort v2 at 127 entities and a 192-query battery balanced 50/50 on language and query type (`CHANGELOG.md:291-306`). Seven Null-Triad gaps were closed by name: diacritic insensitivity, UTF-8 normalisation at ingest, substring matching, position ordering, aliases, stop contexts and fictitious contamination (`:318-328`).

**The measured size of one of them.** A dry run of NER v2 over 2,000 historical rows moved `cited` from 1,409 to 776: 45% of v1 positives were substring false positives (`:342-348`).

**Why this matters to the field report.** The three mechanisms are three different ways for a measurement to produce a defensible-looking null, and only one of them is statistical. Two are properties of the instrument: a probe that was never activated, and a field compared across engines that populate it differently. The 2026-08-31 window defect (I14) is the same species as H3 — a quantity compared across arms where the arms did not produce it the same way — and arrived four months after the project had published a paper diagnosing exactly that failure in itself.

**Residual.** The reboot deleted 18,537 v1 rows and tagged the frozen state (`governance/DIA-1-MARCO-20260423.md:22`). The analysed series therefore begins at zero on 2026-04-23 (`:72-79`), and nothing in the field report can be traced back through the v1 data.

### I4. A manual run cancelled by concurrency overlap on day 1 (2026-04-23)

**What happened.** Run 24856932674, the manual dispatch opening the window, was cancelled after 101 minutes at step 8 of 16. The scheduled 21:00 UTC cron had started 45 minutes late and the two ran in parallel for about 37 minutes (`governance/INCIDENT-RUN-CANCELLED-20260423.md:9`, `:14-21`).

**How it was detected.** A persistent monitor observed `state=completed/cancelled` one minute after the event (`:19`).

**Why the controls missed it.** The concurrency group was `papers-${{ github.workflow }}` with `cancel-in-progress: false`, which was expected to prevent exactly this (`:27-33`).

**The fix.** The concurrency group gained `${{ github.event_name }}`, giving manual dispatch and scheduled cron independent slots (`:53-57`).

**Impact and the useful part.** Zero data loss, because the database commit happens at step 16 and the cancel hit step 8: everything collected lived in the runner's local scope and was discarded with it (`:37-42`). The report's fourth lesson is the one worth carrying into the manuscript: intermediate commits per completed vertical would have made the run resilient, and their absence means any cancellation before step 16 discards the whole run regardless of how much was collected (`:68`). That property explains why the five cancelled runs of I13 persisted nothing at all.

### I5. Credit exhaustion inside a running collection, and the preflight (2026-04-24 to 2026-04-26)

**What happened.** The Anthropic key stopped responding mid-run on window day 2. About 15 Claude fintech queries returned HTTP 400 "credit balance is too low" over 30 minutes before `FAILED_VERTICALS` aborted the job, each recorded as a row with `error_type='api_failure'` and `cited=False` (`docs/audits/2026-04-26/INCIDENT-CLAUDE-CREDITS-2026-04-24.md:18-31`).

**Why the controls missed it.** The vertical loop only checked the exit code of `collect citation`, and that command exits non-zero only if the Python module crashes; a per-LLM `api_failure` is absorbed as a row in the database (`:44-49`). The failure was, by design, data.

**The fix.** A preflight step ahead of the vertical loop making one 1-token call to each provider at about US$0.0001 total; any 4xx aborts the job before any row is written, and exit code 2 triggers the alert chain (`:51-66`).

**Lesson, and its later reversal.** The stated principle is that a pre-collection health check beats a post-collection one, because it detects the failure before paying for the runner and before biasing the data (`:70-72`). That principle produced the eight-day and seventeen-day gaps of I13 and I16, and on 2026-09-09 the project reversed it: a provider without balance now yields a partial day instead of a lost day (T57). Both positions are documented with reasons, and the field report should present the reversal as a genuine trade-off between two kinds of dishonesty — a partial day that enters the series looking complete, against a gap that costs statistical power — rather than as a correction of an error.

### I6. A suspected instrument defect deliberately carried (2026-04-26)

**What happened.** Gemini showed 1.4% citation rate against ChatGPT's 17.3% on the same n=960, a factor of 12.8, with a distribution described as indistinguishable from an earlier Groq incident of thirteen silent days (`docs/audits/2026-04-26/GEMINI-CITATION-RATE-INVESTIGATION.md:9-20`). The leading hypothesis was that 2.5 Pro thinking tokens exhausted `max_output_tokens` (set to 4× the configured value, 3,200), returning `parts` without text, so `_analyze_response_posthoc("")` recorded `cited=False` with `output_tokens=0` and no error (`:23-53`).

**How it was detected.** By periodic audit of the published dashboard snapshot, not by any pipeline check.

**Why the controls missed it.** An empty response is a well-formed row. The fail-loud guard from I2 triggers only when *all* verticals collect zero.

**The decision.** Not to fix inside the window, on three stated grounds: changing `max_tokens` would make Gemini from 2026-04-27 onward distributionally different from Gemini on 2026-04-23 to 26; it would break the pre-registered stopping rule; and the scientifically cleaner alternatives were to treat Gemini as a defective instrument for this window and report it as a limitation, or to open a parallel window (`:86-117`). Three options were put to the owner and the audit of 2026-04-29 records the outcome as "do not fix", to be reported as a limitation (`docs/audits/2026-04-29/HEALTH-CHECK-DEEP.md:85`).

**How it ended.** The hypothesis was never confirmed by the SQL check the document proposed (`:70-81`), and on 2026-08-31 the anomaly received a different and better-evidenced explanation: Gemini opens 79.6% of its responses with preamble and spends the 200-character window before naming anything (I17, D9). The two explanations are not exclusive — one concerns empty responses, the other concerns responses whose entities fall outside the window — and **NOT DOCUMENTED**: no record in the repository reconciles them or reports what fraction of Gemini rows had `output_tokens=0`.

**Lesson.** Freezing an instrument mid-window to protect comparability is defensible, but it converts a bug into a declared property of the series, and the declaration has to survive until the window closes. Here the bug outlived its own explanation, and the limitation that reached the manuscript ("an unexplained arm", `docs/research/methods-paper/MANUSCRIPT.md:467`) is weaker than the one the project could have written in April.

### I7. Four structural bugs found by audit rather than by the pipeline (2026-04-29)

**What happened.** A deep health check of window days 1-7 found four defects, none of which had stopped collection (`docs/audits/2026-04-29/HEALTH-CHECK-DEEP.md:13`):

1. **Query type skewed 85/15.** `config.py::query_type_for()` read only `q["type"]` as an override, while the v2 battery uses `q["query_type"]`; without the override it fell through to a category map in which five of six v2 categories resolve to `directive`. Real counts were 7,299 directive against 1,272 exploratory, against a designed 50/50. Retroactive re-annotation of 4,284 rows restored 4,287/4,284 (50.02%/49.98%), with `query_type_v1_legacy` preserving the original (`:15-41`).
2. **Adversarial probes never ran.** `config_v2.build_adversarial_queries()` returned `[]`, a placeholder. All 8,571 rows had `is_probe=0` (`:43-59`).
3. **`daily_snapshots` losing 75% of rows** to a `UNIQUE(date)` that was not composite, compounded by `save_daily_aggregate` living only in `collect_all` while the workflow called `collect citation` (`:61-77`).
4. **No off-site backup** (`:79-89`).

**Why the controls missed it.** All four are shape defects in data that was present and well-formed. The 204-test suite asserted behaviour, not distribution. Defect 2 is the starkest: a placeholder returning an empty list is indistinguishable, downstream, from a design that has no probes.

**Analytic consequences carried into the design.** 2026-04-23 to 2026-04-29 declared a warm-up window without probes; the H2 calibrated sub-window starts 2026-04-30 (`CHANGELOG.md:254-255`). A regression test was added specifically to guard defect 2 (`:235`).

**Lesson.** Defect 1 is the one that generalises best to anyone building a query battery: a factorial design is only balanced if the balancing key is the key the code reads. The design document and the executed design disagreed for seven days and the disagreement was visible only as a count.

### I8. The database left git, and a weekly calibration that would have been discarded (2026-06-11)

**What happened.** `data/papers.db` reached 103 MB and GitHub rejected the push at the pre-receive hook, which cascaded into the R2 backup, the Vercel revalidation and the daily email — runs #148, #149 and #150 (commit `3c25cbc`). The database was removed from version control. In the follow-up, `weekly-calibration.yml` was found to do only `git add data/papers.db` plus push: after the `.gitignore` change the push would have become a silent no-op, so the Sunday calibration would run, modify the database, and have the result destroyed with the runner, while the next morning's collection overwrote everything with the pre-calibration version (commit `ef12647`).

**How it was detected.** The first half by a hard push failure. The second half by deliberately auditing the other two workflows for the same pattern before they reached production; the commit message states that without the fix the weekly calibration would have become silently ineffective, surfacing only as gradual drift in the calibration metrics.

**Lesson.** A change that makes one path fail loudly can make a neighbouring path fail silently. Removing a file from version control converts every `git add` of it from an error into a no-op, and a no-op is the hardest failure to observe.

### I9. Gemini: model version and reasoning budget changed in one commit (2026-06-17)

**What happened.** Commit `f43a42b` switched the Gemini arm from `gemini-2.5-pro` to `gemini-2.5-flash`, changed `GEMINI_THINKING_BUDGET` from 1024 to 0, and returned Gemini to `MANDATORY_LLMS`. The stated motive is cost: 2.5 Pro thinking tokens were about 91% of the paper's LLM spend, roughly R$2.1k per month of real wallet usage. The commit declares the change forward-only, tracked per row through `citation.model_version`.

**Context that made it urgent.** The same day's incident report records the AI Studio prepaid wallet at −R$3.59 with auto-reload off, a R$400.00 top-up on 2026-06-11 consumed in about six days, and May consumption of R$334.57 (`docs/INCIDENT_RUN155_FINOPS_GEMINI_2026-06-17.md:67-79`). The root cause of recurring Gemini gaps is a billing setting.

**Why this is the hardest boundary in the series to analyse.** Two parameters moved together. Model identity changed (a P4 event) and generation configuration changed (a P5 event), so nothing in the data separates the effect of the smaller model from the effect of disabling reasoning. The methodology records the doctrine applied — the same one later applied to Grok — that a boundary affecting fewer observations than a declared threshold is dropped rather than stratified (`docs/METHODOLOGY_V2.md:89-92`), but here the boundary falls near the middle of the series and dropping is not available.

**The part that did not propagate.** The boundary reached the collector and the manuscript, and did not reach three other places. `src/config.py:586` collects with `gemini-2.5-flash`. `docs/research/methods-paper/MANUSCRIPT.md:186` correctly records `gemini-2.5-pro`, then `gemini-2.5-flash`, boundary 2026-06-17. But `docs/METHODOLOGY_V2.md:68` still lists the Gemini arm as `gemini-2.5-pro` in the canonical panel table; `scripts/generate_dashboard_json.py:55` hardcodes `"model": "gemini-2.5-pro"` for the public dashboard; and `scripts/preflight_llm_check.py:113` probes `gemini-2.5-pro`, which is not the model collection uses. **NOT DOCUMENTED**: no incident record, changelog entry or governance note in the repository mentions this divergence. It was found for this dossier by direct inspection and should be verified independently before it appears in the manuscript.

**Lesson.** A series event is not applied when the collector changes; it is applied when every artefact that names the instrument changes with it. The manuscript's own conformance parameter P4 requires a pinned model version on every observation, and the external review's finding D2 is that the manuscript violated it by naming products instead of snapshots (`governance/REVISAO-EXTERNA-PAPER-20260831.md:33-39`). The preflight probing a model the study no longer collects is the same defect one layer down: the health check attests to a component that is not in the instrument.

### I10. Run #155 and a published figure computed on 0.3% of the dataset (2026-06-11 to 2026-06-17)

**What happened.** Run #155 (27351297994) was one of several manual re-runs during the 100 MB crisis. It regenerated the dashboard from a base of 216 queries in one vertical instead of the recovered 62,820 citations, because the artifact produced by `recover-historical-db.yml` was invisible to `daily-collect.yml`. The failing step was the coverage health check, which carries `continue-on-error: true` and therefore appears as "success" in the step list while its `outcome` triggers the final `exit 1` (`docs/INCIDENT_RUN155_FINOPS_GEMINI_2026-06-17.md:9-30`).

**Why the controls missed it.** The health check worked. The reporting of the health check did not: a step that fails but is marked `continue-on-error` reads as green to anyone scanning the run.

**The fix.** Corrected in run #156 the same night by downloading the recover artifact and restoring from R2 as source of truth; six consecutive green runs followed (`:27-30`).

**Adjacent finding worth carrying.** The FinOps ceiling lives in a SQLite table inside the restored database rather than in code, and `_ensure_budgets()` only INSERTs, never UPDATEs, so the Google ceiling stayed at US$50 and hit 108% `is_blocked` — which would have failed the provider even after the wallet was refilled (`:48-65`). The recorded gotcha is that the local database diverges from CI and must never be treated as the FinOps source of truth.

**Lesson.** State that governs a gate must not live inside the artefact the gate protects. A budget ceiling stored in the restored database is restored along with everything else, including its own staleness.

### I11. The restoration path that had been inert for two months (2026-06-11 to 2026-08-10)

**What happened.** The R2 "source of truth" steps added on 2026-06-11 authenticated with four S3 secrets — `R2_ENDPOINT`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_BUCKET` — that were never created. Every run took the silent-skip branch, the restore never executed, and no off-site backup existed at all. With the restore inert, `weekly-benchmark.yml` and `weekly-calibration.yml` fell back to an artifact download without an explicit `workflow:`, which only sees artifacts from the workflow itself. Both closed a loop on their own degraded copy: they published `papers-db-latest` with 864 citations while `daily-collect` held 63,940, ran the weekly analysis on 1.4% of the dataset, and reported success (commit `bba851f`).

**How it was detected.** Two months later, during work on series persistence (PR #48/#51), not by any alert.

**Why the controls missed it.** The skip was written deliberately. The 2026-04-29 audit that introduced the R2 step specified it: "Skip silencioso se `R2_*` secrets não configurados", with `continue-on-error: true` so as not to block the pipeline, and left "create bucket + secrets" as an open operational item (`docs/audits/2026-04-29/HEALTH-CHECK-DEEP.md:75`, `:87`). A pending manual action and a code path designed to be invisible when that action is pending combine into a feature that does not exist and does not say so.

**The fix.** `scripts/r2_sync.py` authenticating over the R2 REST API with the same `CLOUDFLARE_API_TOKEN` used elsewhere — three secrets instead of four, no boto3, and a `push` that refuses to overwrite a larger remote base. `scripts/db_integrity_guard.py` keeps a high-water mark in `data/db_floor.json` and aborts a run whose dataset fell below the floor. `R2_REQUIRED=1` turns a missing secret into a visible failure rather than a skip. Weeklies pull from `daily-collect.yml` explicitly. Six regression tests (commit `bba851f`).

**Verified on first use.** Run #280 adopted the R2 base of 153,785 rows over the local 151,099 after the artifact resolved to −1 rows, which is exactly the June failure mode (commit `79b5021`).

**Lesson.** This is the clearest case in the series of the manuscript's stated generalisation: a degradation path that does not announce itself is indistinguishable from one that does not exist (`docs/research/methods-paper/MANUSCRIPT.md:343`). The inverse holds too, and the project recorded it when designing the 2026-08-31 distribution guard: a guard that always fails is indistinguishable from a guard that is switched off (`governance/ASSINATURA-DISTRIBUCIONAL-20260831.md:89-91`).

### I12. Two guards that blocked or broke the pipeline for reasons unrelated to data (2026-08-14, 2026-09-03 to 2026-09-08)

**What happened, first case.** The integrity gate merged on 2026-08-10 checked `llm_calls`, a table that never existed, while the FinOps tracker writes to `finops_usage` with more than 58,000 healthy rows. Every scheduled run since the merge aborted at the gate with the real spend data sitting untouched one table over (commit `e94ccbd`, 2026-08-14).

**What happened, second case.** The distribution guard's `avaliar()` hardcoded `timestamp >= now − 2 days` while `coletar_perfil()` honoured `--since-days`. Its unit tests fix rows at 2026-08-31, so they passed on the day the guard was written and began failing two days later. CI was red on every push from 2026-09-03 to 2026-09-08 with no defect in the instrument (commit `6a5ea63`; `governance/HEALTH-CHECK-APIS-20260908.md:60`).

**Why they matter together.** Both are guards installed in direct response to a data-loss incident, and both consumed operator attention for days while protecting nothing. The second is the more instructive: a time-relative condition tested against time-fixed fixtures is guaranteed to pass on the day it is written and to expire on a schedule nobody chose.

**Lesson.** A guard is part of the instrument and ages like the rest of it. Where a check uses relative time, the test must use relative time too, or the green result is a statement about the calendar rather than about the code.

### I13. The fifth arm consumed 72% of the run and stopped the series for eight days (2026-08-24 to 2026-08-31)

**What happened.** `grok-4.6` reasons by default and the reasoning is billed as output. In run 33303260035 the Grok arm consumed 129 of 179 wall-clock minutes against Gemini 17, Claude 15, ChatGPT 12 and Perplexity 5, and the job died at `timeout-minutes: 180` with the fourth vertical half-collected. Five runs were cancelled this way between 2026-08-24 and 2026-08-30, burning about 900 GitHub Actions minutes without persisting a single day, with the Actions budget already at 514% (`governance/HEALTH-CHECK-COLETA-20260831.md:35`). In parallel, the Anthropic balance was exhausted and the one-minute runs died at preflight (`:53-55`). The last day persisted before the fix was 2026-08-23.

**How it was detected.** By opening the job logs. The Actions run panel alternated `cancelled` and `failure` without indicating where the collection died, and neither cause surfaced above job-log level (`:23`).

**The measurement that fixed it.** Against the API, with the collection's own citation query: 73.7 s and 2,746 reasoning tokens without the parameter; 19.7 s and 419 with `reasoning_effort=low`; `none` rejected with HTTP 400 (`:27-33`).

**The fix and its verification.** `XAI_REASONING_EFFORT` defaulting to `low`, pinned model untouched, forward-only (commit `ee5144c`). Run 33404549276 completed in 2h12. Grok median latency 32.4 → 16.2 s; Grok wall-clock 129.0 → 71.6 min; total 178.6 → 129.7 min (`:41-47`).

**The forecast that was wrong, kept on purpose.** The estimate recorded before the fix was about 95 minutes total and was optimistic; the real margin over the 180-minute ceiling is 50 minutes, not the 85 the estimate implied, and Grok still accounts for 55% of collection wall-clock, so the next increase in cohort or battery meets the ceiling again (`:49-51`). The document keeps the error next to the measurement that corrected it, and the governance convention makes that a house rule (`governance/README.md:25`).

**Lesson for anyone measuring citation.** Provider-default reasoning is a generation parameter that changes both cost and wall-clock by a factor of three or four without changing the model identifier. A panel is only affordable to run twice a day if every arm's latency is bounded, and the arm that breaks the budget is not necessarily the one that costs the most per token. The external review turned this into specification text: generation configuration became the sixth declared parameter precisely because two of the four series events in this project were caused by changing it (`governance/REVISAO-EXTERNA-PAPER-20260831.md:118-124`).

### I14. The observation window was asymmetric across the study arms (discovered 2026-08-31)

**What happened.** Citation detection ran over `citations.response_text`, and that column was never the model's answer. Five of six client adapters stored `text[:200]`; Perplexity, by taking a different path inside the client, stored the whole response, up to 2,502 characters (`governance/HEALTH-CHECK-COLETA-20260831.md:67`). The asymmetry fell exactly on the axis of the comparison the study makes: a retrieval-augmented engine against parametric ones, under different reading windows.

**How it was detected.** By a distributional check, prompted by a question during the manuscript review about why the "share at exactly 200" column read 0.0% for Perplexity (`governance/ASSINATURA-DISTRIBUCIONAL-20260831.md:5`). Mean stored length was exactly 200.0 in five arms and 691.8 in the sixth. The Perplexity length distribution is continuous and well spread — minimum 198, p1 289, p25 479, median 618, p75 799, p95 1,341, maximum 2,502 — with no mass piled anywhere, and the minimum of 198 is a single response with a complete gap between it and p1, which is the opposite of what partial truncation would produce (`:36-50`).

**Why every control missed it.** The health check states it plainly: each layer looked in the wrong place for the right reason. Tests asserted on the column and the column was populated in both cases. Validators checked string well-formedness and both strings were well-formed and of plausible length. Daily health checks confirmed that six arms produced rows, that the language split held at 50/50, that probes were marked, and that response hashes varied so it was not a cache — all true, and none of it asking how much text the extractor was reading (`governance/HEALTH-CHECK-COLETA-20260831.md:75-79`; `governance/ASSINATURA-DISTRIBUCIONAL-20260831.md:58-66`). 223 tests passed.

**Magnitude.** Re-extraction over the series to 2026-08-31 under a uniform 200-character window, canonical queries only, 66,399 observations over 50 days: Perplexity falls from 75.7% to 51.9%, −23.8 points, with 7,435 rows truncated; the other five arms move by 0.0 points with 0 rows truncated (`governance/HEALTH-CHECK-COLETA-20260831.md:85-92`).

**The correction to the correction.** The five zero deltas were initially presented as a sanity check of the re-extraction. The external review pointed out that applying `text[:200]` to a string already 200 characters long is the identity, so the zero is guaranteed by construction and is not an independent observation. The check retains value as evidence that the harmonisation script introduced no side effect, and loses the value originally attributed to it (`:96`; `docs/research/methods-paper/MANUSCRIPT.md:243`).

**The mechanism, withdrawn.** The manuscript had argued that a narrow window penalises retrieval-augmented engines because they open with framing prose before naming. Relative first-mention offset, normalised by observed length, reverses the ordering: Grok 0.164, Perplexity 0.228, Gemini 0.493, Groq 0.539, ChatGPT 0.582, Claude 0.621. A uniformity test on Perplexity predicts 1 − 200/662 = 69.8% of mentions beyond character 200; the observed fraction is 28.8% (`governance/HEALTH-CHECK-COLETA-20260831.md:104-115`). The parametric denominators are censored at 200, so the 0.49-0.62 values are upper bounds and the reversal cannot be asserted. The defensible conclusion is non-identification: the direction of the window bias is not identified by data collected under an asymmetric window (`:117`).

**The replacement mechanism, and why it generalises.** Quantity of text read, not discourse structure: reading 662 characters instead of 200 finds more mentions, and would in any engine whose full response had been retained. The problem stops being a rhetorical peculiarity of RAG engines and becomes a property of any comparison across unequal reading windows (`:119`).

**Lesson.** The window is normally not a design decision at all. It is an incidental consequence of how a provider adapter was written, often for reasons of cost or log volume, and it therefore varies exactly where studies are least likely to look — between providers, which is where the comparison lives (`docs/research/methods-paper/MANUSCRIPT.md:228`).

### I15. No observation was reproducible by a third party until August (2026-04-23 to 2026-08-31)

**What happened.** Text beyond the window was discarded in the client and never reached the database. An external reviewer had no way to reproduce the extraction, because its input did not exist anywhere (`governance/HEALTH-CHECK-COLETA-20260831.md:125`).

**Scale.** The figure is reported three ways in three documents from the same period: 80,638 observations (`docs/research/methods-paper/DOSSIE_REUNIAO.md:178` and `docs/research/methods-paper/VERIFICATION.md:171`), 83,486 (`governance/HEALTH-CHECK-COLETA-20260831.md:123` and `docs/research/methods-paper/MANUSCRIPT.md:291`). The difference is consistent with snapshots taken at different times on 2026-08-31, before and after the recovery run; **the manuscript should state which snapshot it uses**, since the two cannot both be the total at a single moment.

**Why it is the worse of the two window defects.** The asymmetry is correctable, because the truncated string is still the string the extractor saw and re-extracting over it reproduces the original decision exactly. No amount of care recovers text that was never stored (`governance/HEALTH-CHECK-COLETA-20260831.md:127`).

**The fix and its limit.** `response_full_text` via migration 0010, forward-only by construction. Window sensitivity analysis over the series before 2026-08-31 is limited to 200 characters in the five parametric arms (`:129`; `docs/METHODOLOGY_V2.md:168`). The backfill is honest about what it can and cannot do: it annotates each historical row's effective window from `length(response_text)`, which is not an estimate but exactly what the extractor saw, and it does not attempt to reconstruct the discarded text (`CHANGELOG.md:115-118`).

**Lesson.** Retention of the raw observation is a separate requirement from correctness of the measurement, and it is the one that cannot be repaired retroactively. A study that stores only its derived variable has, at best, a reproducible analysis of an unreproducible measurement.

### I16. A protection that was written, called, and swallowed (2026-08-31)

**What happened.** Migration 0010, written to fix the auditability defect of I15, was called from inside `_migrate_add_vertical`. It ran before the `executescript` that creates the `citations` table, died on "no such table", and the `except` turned the failure into a DEBUG log. On an existing database the column appeared; on a new database it never would, and nobody would know (`governance/HEALTH-CHECK-COLETA-20260831.md:133`).

**How it was detected.** By a regression test written to fail if a new database is born without the columns.

**Why it belongs in the paper.** It is the same pattern as I11, stated by the health check itself: protection written, protection called, exception swallowed, pipeline green (`:135`). The operational rule extracted is general: every `except` that degrades to a low-level log inside an initialisation path needs a test exercising that path from zero, because the incremental path hides the failure by definition (`:137`).

### I17. External adversarial review: two published numbers withdrawn, and a reference implementation that did not implement the specification (2026-08-31)

**What happened.** An adversarial review of the manuscript produced three classes of finding (`governance/REVISAO-EXTERNA-PAPER-20260831.md`).

**Submission blockers.**

- **D1.** Zero bibliographic references in the manuscript; target set at 40 to 60 (`:25-31`).
- **D2.** The paper violates its own P4 conformance requirement: its tables name products ("ChatGPT", "Claude", "Gemini") while P4 declares product naming insufficient. The pinned snapshots existed in `docs/METHODOLOGY_V2.md` §3.1 and never reached the manuscript (`:33-39`).
- **D3.** The pre-registration claim is not a pre-registration. A git repository under the author's control is not an independent time-stamped registry, and the declared milestone was wrong: pre-registration precedes collection, not window closure (`:41-49`). The current manuscript states this plainly (`docs/research/methods-paper/MANUSCRIPT.md:419`).
- **D8.** §7.2 was factually incorrect. The paper compared its index against the component that dominates its logarithmic variance, which does not measure arbitrariness of aggregation. The correct test: Spearman rho between alternative aggregations over n=66 reaches 0.706 (harmonic against weighted) and 0.734 (arithmetic against harmonic), against the 0.982 the paper offered as evidence of agreement. Variance decomposition of log(GCI): coverage 74.7%, breadth 16.9%, prominence 8.4%. Rank displacement against simple coverage: median 2, p90 6, maximum 10, with only 7 of 66 entities holding exact rank (`:51-86`).

**Substance corrections.**

- **D4.** The geometric mean's stated non-compensatory justification holds only in the limit: with six engines, total absence from one gives B = 5/6, which greater coverage compensates easily (`:92-98`).
- **D5.** The reference implementation does not implement the specification. `scripts/brgeo1_index.py` defines `MIN_OBS_PARA_ENTRAR_NO_PAINEL = 500` at line 53 and filters the panel by it at line 92; the threshold appears nowhere in the manuscript and alters B, a third of the index. Verified consequence in fintech: Grok, with 96 observations, is excluded; Groq, retired on 2026-08-19, enters with 3,552. The reference index ran on a panel containing a dead engine and missing a live one (`:100-108`). The review calls this the most embarrassing finding of its class, because an undeclared eligibility rule in the reference implementation is the exact category of problem the paper denounces.
- **D6.** The matching rule is named as a problem in §2.2 and is not among the five formalised parameters in §3.1. Two implementations differing in matching rule produce different numbers on the same responses while both declaring conformance (`:110-116`). It became parameter P6.
- **D7.** Generation configuration was not declared anywhere. Two of the four series events were caused by changing it (`:118-124`). It became parameter P5.
- **D9.** The Gemini anomaly, investigated the same day at the reviewer's prompting, is not a broken extractor. Share of responses opening with preamble against citation rate: Gemini 79.6% / 1.8%, Perplexity 9.2% / 75.7%, Grok 4.0% / 32.3%, ChatGPT 2.1% / 17.2%, Groq 1.1% / 8.5%, Claude 0.0% / 25.8%. The engine with the most preamble is parametric and the retrieval-augmented engine has little, so susceptibility to the window is a property of the model rather than of the architecture and is not deducible from the class (`:126-153`). A control supports the reading: among Gemini observations that do cite, 23.0% of first mentions fall beyond character 150, comparable to ChatGPT at 24.5% and below Claude at 36.1%.
- **D10 and D11.** `dual_responses` is empty, so the JSON-versus-natural-language elicitation comparison has never run; and no inter-implementation reproducibility exercise exists, so the central proposition — that conformance produces comparability — has no direct evidence in its favour (`:155-167`).

**Why the existing controls missed all of it.** None of these is detectable by a test suite. The distributional-signature document states the boundary explicitly and encodes it in a test named `test_o_guard_nao_avalia_argumento`, which records that a false, well-formed claim passes the manuscript guard untouched — because exactly that kind of claim, correct in form and unsupported by measurement, is what the external review knocked down in §8 (`governance/ASSINATURA-DISTRIBUCIONAL-20260831.md:144-148`).

**What was fixed.** `scripts/manuscript_guard.py` now checks reference integrity in both directions, DOI and arXiv identifier form, table numbering and citation, section anchors, delta arithmetic in table rows, and abstract length against the target journal's limit. It caught a real failure on first execution: the abstract stood at 205 words against a 200-word limit (`:129-142`).

**Lesson.** The reference implementation of a measurement standard is part of the specification, and an undeclared constant inside it is an undeclared parameter. D5 is the finding a reviewer of the field report will find most quotable, because the project's own eligibility threshold reproduced, inside the artefact meant to demonstrate the standard, the failure the standard exists to prevent.

### I18. Credit exhaustion barring whole days, and the policy reversal (2026-07-25 to 2026-09-11)

**Recorded history of balance stops inside the v2 window.** 2026-07-25; 2026-08-06; 2026-08-09 and 2026-08-10; and the sequence from 2026-08-23 to 2026-08-31 (`governance/HEALTH-CHECK-COLETA-20260831.md:59`). Then, by provider, across 2026-08-16 to 2026-09-08: Groq 5 runs barred 2026-08-17 to 19 by model retirement; Grok 2 runs on 2026-08-23 and 24 by xAI balance; Claude 12 runs from 2026-08-28 to 2026-09-06; ChatGPT 7 runs across 2026-09-01 to 03 and 2026-09-06 to 07; Perplexity 6 runs across 2026-09-01 to 03 and 2026-09-08 (`governance/HEALTH-CHECK-APIS-20260908.md:32-38`).

**Cost to the series.** Of 35 days between 2026-08-05 and 2026-09-08, 13 have data. Seventeen days of series lost between 2026-08-16 and 2026-09-08. The forecast recorded on 2026-08-10 was a close on 2026-09-28 with 49 days left; between 2026-08-10 and 2026-09-08, 29 calendar days passed and 12 entered the series (`:44-46`).

**Two days collected with half a panel.** 2026-09-06 and 2026-09-07 hold only Gemini, Grok and Perplexity, the product of local collections with `MANDATORY_LLMS` downgraded to that trio as a repository variable on 2026-09-07 at 23:15 UTC, which made ChatGPT and Claude optional against the methodology (`:15`, `:44`). The variable was removed on 2026-09-08 (`:51`).

**Why the control behaved correctly and still produced the loss.** The preflight did exactly what it was written to do: it barred collection rather than recording a day with four of five arms, on the stated grounds that a silently recorded partial day costs more than a declared gap, because the gap enters the missingness ledger while the partial day enters the series as if it were a complete observation (`governance/HEALTH-CHECK-COLETA-20260831.md:57`).

**The reversal.** On 2026-09-09, `PAPERS_PREFLIGHT_MODE=degrade` became the default. A mandatory provider without credit or quota is removed from `MANDATORY_LLMS` through `GITHUB_ENV`, the day is written to `data/partial_days.json` with the missing arms, the provider's verbatim error and the Actions run URL as source, and collection continues if at least `PAPERS_MIN_LLMS` remain; `strict` restores the previous behaviour, and a failure that is not about balance still blocks (commit `427ab00`; `git diff HEAD origin/main -- CHANGELOG.md`). Within two days the new path had recorded three further partial days: 2026-09-10 twice and 2026-09-11 once (`git show origin/main:data/partial_days.json`).

**The structural cause, documented separately.** The six keys in `papers/.env` are identical to those in `geo-orchestrator/.env`, and the Anthropic key of the brand-citation monitor is the same as the morning digest's. Between 2026-08-28 and 2026-09-08 three independent measurements stopped at the same time for the same reason, each raising its own alert and its own incident about the same account. The consequences named are failure correlation between series presented together as independent, invisible consumption that makes the `papers` FinOps ceiling measure only part of the spend, difficult rotation, and impossible cost attribution (`git show origin/main:governance/CHAVES-COMPARTILHADAS-ENTRE-INSTRUMENTOS-20260909.md:9-24`). Auto-reload has been off on three providers by an owner decision of 2026-07-24 (`governance/HEALTH-CHECK-APIS-20260908.md:50`).

**Lesson, and the honest statement of the trade-off.** The missingness is not ignorable, and the manuscript says why: gaps cluster around provider credit exhaustion, which correlates with cost, which correlates with response length, which §5 establishes correlates with citation. Coverage weighting corrects data missing at random and does not address this mechanism; bounds analysis is required and has not been performed (`docs/research/methods-paper/MANUSCRIPT.md:463`). The degrade policy reduces lost days at the price of introducing days with unequal panels, which shifts the problem from the day dimension to the arm dimension without removing it. The field report should present both regimes with their dates rather than one as the fix for the other.

### I19. Two scheduled or standing divergences, recorded before they become incidents

**A. Perplexity retires the transport the study uses on 2026-09-27.** Announced 2026-08-13 on the platform forum; `POST /chat/completions` stops responding eighteen days before the projected window close of 2026-10-15. Perplexity is a mandatory arm, so without action the preflight would fail every day and the series would stop with 37 days missing (`governance/HEALTH-CHECK-APIS-20260908.md:64`; `git show origin/main:docs/PERPLEXITY_AGENT_API.md`).

Live probing on 2026-09-08 fixed three decisions. Presets route to third-party models — `fast`, `low` and `medium` all returned `openai/gpt-5.6-luna` — and would have swapped the study's arm without notice, so the model is always named explicitly as `perplexity/sonar`; `sonar-pro`, `sonar-reasoning-pro` and `sonar-reasoning` return HTTP 400 "not supported". Without the `web_search` tool the model answers with no sources at all, and cited-with-source is the object of the measurement. The pinned `model_version` recorded stays `sonar`, so the instrument does not change mid-series. Billed cost comes in `usage.cost.total_cost`: US$0.0025 per search against US$0.005 `request_cost` on the legacy route (`governance/HEALTH-CHECK-APIS-20260908.md:66-77`).

The implementation is merged behind `PAPERS_PPLX_AGENT_API`, default `0` (commit `87ac7a2`), and the decision to switch remains open (`:97`). For the drift chapter this is the cleanest example in the project of a boundary imposed from outside on a schedule the study does not control, prepared in advance and auditable per row because the line records `model` and `raw`.

**B. The Gemini boundary did not reach three artefacts.** As set out in I9: `src/config.py:586` collects with `gemini-2.5-flash` since 2026-06-17, while `docs/METHODOLOGY_V2.md:68` still lists `gemini-2.5-pro` in the canonical panel table, `scripts/generate_dashboard_json.py:55` publishes `gemini-2.5-pro` as the arm's model on the public dashboard, and `scripts/preflight_llm_check.py:113` probes `gemini-2.5-pro`. **NOT DOCUMENTED** as an incident.

**C. The public dashboard and the manuscript report different extractors and different denominators.** `scripts/generate_dashboard_json.py` aggregates `SUM(cited)` over the whole `citations` table at lines 188, 194, 210, 225, 316 and 338, with the non-probe filter (`_non_probe`, line 464) applied only to the entity rankings. The manuscript's figures use `cited_v2` with `is_probe=0` (`docs/research/methods-paper/VERIFICATION.md:52-55`) and the harmonisation script run with `--canonical-only` (`:20`). The published per-arm rates on 2026-09-11 are therefore Perplexity 74.1%, Grok 46.4%, Claude 42.5%, ChatGPT 35.2%, Groq 29.0%, Gemini 20.5% (`git show origin/main:data/dashboard_data.json`), against the manuscript's series figures of Perplexity 75.7%, Grok 32.3%, Claude 25.8%, ChatGPT 17.2%, Groq 8.5%, Gemini 1.8% (`docs/research/methods-paper/MANUSCRIPT.md:238-243`). The v1 extractor was measured in April at roughly 1.8× the v2 rate on a 2,000-row sample (`CHANGELOG.md:342-347`), which is the right order of magnitude for part of the gap, and probe inclusion accounts for more. **NOT DOCUMENTED**: no record in the repository reconciles the two published series or states which extractor the public dashboard reports. This was found by direct code inspection for this dossier and must be verified independently before it is asserted in the manuscript. It matters to the field report because it is the same defect the paper describes in the market — two figures for the same object, produced under undeclared conditions — occurring between two artefacts of the same project.

---

## 3. Series events, in manuscript table format

The manuscript's Table 8 format is `Date | Arm | Change class | Analytic consequence` (`docs/research/methods-paper/MANUSCRIPT.md:326-335`). The table below keeps that format and adds the rows the current Table 8 does not carry, flagged in the last column. Four events are declared as such in the CHANGELOG and the methodology; the remainder are candidates for declaration and are marked.

| Date | Arm | Change | Class | Analytic consequence | Status |
|---|---|---|---|---|---|
| 2026-04-23 | all | v1 dataset truncated, 18,537 rows deleted; NER v2 replaces v1 matching | cohort, matching rule, dataset reset | Hard discontinuity. No analysis crosses it. v1 positives were 1.8× v2 on a 2,000-row sample. | Declared (`CHANGELOG.md:285`, `governance/DIA-1-MARCO-20260423.md:22`) |
| 2026-04-30 | all | adversarial probes activated | battery | 2026-04-23 to 2026-04-29 is a warm-up window with no probes; the H2 calibrated sub-window starts here. | Declared (`CHANGELOG.md:254-255`) |
| 2026-04-30 | all | `query_type` re-annotated on 4,284 rows, 85/15 to 50.02/49.98 | battery annotation | H5 (directive inflation) on the pre-fix window would have been computed on a mislabelled factor; `query_type_v1_legacy` preserves the original. | Not in Table 8 — candidate |
| 2026-06-05 | Gemini | `GEMINI_THINKING_BUDGET` set to 1024; Gemini removed from `MANDATORY_LLMS` | generation configuration, panel obligation | Generation configuration changed twelve days before the model change, so the 2026-06-17 boundary is the second of two adjacent P5 events in the same arm. | Not in Table 8 — candidate (`docs/ROADMAP_2026Q2-Q4.md:26-36`) |
| 2026-06-17 | Gemini | `gemini-2.5-pro` to `gemini-2.5-flash`; `GEMINI_THINKING_BUDGET` 1024 to 0; Gemini returned to `MANDATORY_LLMS` | model version and reasoning budget | Pre and post not comparable within arm. Model identity and generation configuration moved together, so their effects are not separable in the data. | Declared (`docs/METHODOLOGY_V2.md:91-92`; `MANUSCRIPT.md:331`) |
| 2026-08-17 to 2026-08-19 | slot 5 | Groq retires `llama-3.3-70b-versatile`; five collections abort at preflight | provider-imposed outage | Gap in the fifth arm. Last Groq observation 2026-08-16 21:00 BRT. | Declared (`CHANGELOG.md:180-186`) |
| 2026-08-19 | slot 5 | engine replaced, Groq `llama-3.3-70b-versatile` to xAI `grok-4.6` | engine replacement | Not a continuous series. Stratify or truncate the fifth arm at this boundary. First Grok observations persist 2026-08-23. | Declared (`docs/METHODOLOGY_V2.md:72-77`; `MANUSCRIPT.md:332`) |
| 2026-08-19 | all | TLS delegated to the OS certificate store (`truststore`) | transport | Declared to have no effect on collected data. | Declared as non-event (`CHANGELOG.md:172-176`) |
| 2026-08-31 | Perplexity | observation window unified at 200 characters across all arms | window unified | Affects this arm only: 75.7% to 51.9%, −23.8 pp over 66,399 canonical observations. | Declared (`CHANGELOG.md:81-93`; `MANUSCRIPT.md:333`) |
| 2026-08-31 | all | `response_full_text` retained (migration 0010) | retention | Forward-only. Window sensitivity is unavailable for the parametric arms before this date. | Declared in text, not in Table 8 — candidate (`CHANGELOG.md:95-97`) |
| 2026-08-31 | Perplexity | arm added to the probe stratum (`calibracao_fp` routing) | battery coverage | H2 figures before this date describe five parametric arms and exclude the RAG case that motivates the hypothesis. | Not in Table 8 — candidate (`CHANGELOG.md:99-104`) |
| 2026-08-31 | Grok | `reasoning_effort` reduced to `low` (`XAI_REASONING_EFFORT`) | generation configuration | Separate stratum. 206 observations of 2026-08-23 fall on the prior side; declared decision is to discard that day in the Grok arm rather than stratify. | Declared (`CHANGELOG.md:136-148`; `MANUSCRIPT.md:334`) |
| 2026-08-31 | all | panel membership redefined from observation count to activity in the recent window | index computation | The fintech panel loses Groq and gains Grok; B is one third of the index. | Not in Table 8 — candidate (`CHANGELOG.md:32-34`; `governance/ASSINATURA-DISTRIBUCIONAL-20260831.md:109-122`) |
| 2026-08-31 | all | hallucination marker separated from refusal marker | outcome definition | The probe outcome variable changes meaning: rows previously counted as hallucination are now split three ways, and 67.5% of flagged rows carry an explicit refusal. | Not in Table 8 — candidate (`CHANGELOG.md` §governança; `MANUSCRIPT.md:306-314`) |
| 2026-09-06 to 2026-09-07 | ChatGPT, Claude | arms absent; `MANDATORY_LLMS` downgraded as a repository variable | panel composition | Two days with three of five arms. Mark as incomplete or exclude from the between-engine comparison. | Declared (`governance/HEALTH-CHECK-APIS-20260908.md:44`, `:99`) |
| 2026-09-09 | all | preflight default changes from abort to degrade | missingness policy | Days after this date may hold unequal panels by design, recorded in `data/partial_days.json`. Days before it are either complete or absent. | Declared (commit `427ab00`) |
| 2026-09-27 (scheduled) | Perplexity | `POST /chat/completions` retired; Agent API `POST /v1/agent` behind `PAPERS_PPLX_AGENT_API` | transport | Same model, same window, same retention; boundary auditable per row via `model` and `raw`. Without the switch the series stops with 37 days missing. | Prepared, not switched (`governance/HEALTH-CHECK-APIS-20260908.md:97`) |

---

## 4. Missingness ledger

### 4.1 Policy

The declared rule is zero imputation. Every gap is audited and reported instead of silently imputed; longitudinal analysis weights days by coverage through a random intercept per collection date; partial days are reported in a sensitivity analysis with and without them; total gaps are marked in `collection_runs` with `status='aborted'` and the interval is excluded from the formal analytic window (`docs/METHODOLOGY_V2.md:114`, `:133`). The dossier restates it as a house rule: nothing is imputed, every gap enters the ledger with date, extent and cause (`docs/research/methods-paper/DOSSIE_REUNIAO.md:408`).

The rule that governed acquisition until 2026-09-09 was the complement: better an absent day than a partial day, because a gap enters the missingness ledger while a partial day enters the series as if it were a complete observation (`governance/HEALTH-CHECK-COLETA-20260831.md:57`). From 2026-09-09 the default is the opposite, with the partial day written to `data/partial_days.json` (commit `427ab00`). Any analysis spanning September must know which regime each day belongs to.

### 4.2 Days with data, runs aborted

| Measurement date | Days with data | Aborted runs | Successful runs | Source |
|---|---:|---:|---:|---|
| 2026-05-18 | 19 of 35 with all 20 cells (54%); 16 total-gap days (45.7%) | — | — | `docs/METHODOLOGY_V2.md:131` |
| 2026-08-10 | 59-day gap recorded | 272 | 244 | commit `79b5021` |
| 2026-08-31 | 49 | 296 | — | `docs/research/methods-paper/DOSSIE_REUNIAO.md:401` |
| 2026-08-31 | 50 | 324 | — | `docs/research/methods-paper/MANUSCRIPT.md:341` |
| 2026-09-08 | 53 of 90 collected days; 85,359 observations; 1,611 per collected day | — | 516 → 672 `collection_runs` | `governance/HEALTH-CHECK-APIS-20260908.md:44`, `:91` |
| 2026-09-11 | 56 of 90 collected days; 91,392 queries; 348 collection rounds | — | — | `git show origin/main:data/dashboard_data.json` |

The 2026-08-31 row appears twice on purpose. Two documents written the same day report 49 days / 296 aborted runs and 50 days / 324 aborted runs. Both cannot be the state at one instant, and neither document explains the difference; the most likely reading is two queries run before and after that day's recovery run 33404549276. **The manuscript must pick one, state the query timestamp, and reproduce it from `VERIFICATION.md:159-166`.**

### 4.3 Itemised gaps and partial days

**Total gaps, with cause.**

| Interval | Days | Cause | Evidence |
|---|---:|---|---|
| 2026-03-25 to 2026-03-29 | 4 | `SyntaxError` behind `\|\| true`; CI green | `docs/INCIDENT_PIPELINE_2026-03-29.md:96-104` |
| 2026-03-30 to 2026-04-07 | 9 | Externally rotated keys, HTTP 401 on all providers, `continue-on-error` exit 0 | commit `19df1c9` |
| 2026-04-14 to 2026-04-22 | 9 | Preflight not yet implemented; silent failures on Anthropic credit | `docs/METHODOLOGY_V2.md:120` (precedes the declared v2 start; see §5.4) |
| 2026-05-02 to 2026-05-03 | 2 | Collection aborted by preflight | `docs/METHODOLOGY_V2.md:124` |
| 2026-05-06 to 2026-05-10 | 5 | Sequence of health-gate failures | `docs/METHODOLOGY_V2.md:127` |
| 2026-07-25 | 1 | Provider balance | `governance/HEALTH-CHECK-COLETA-20260831.md:59` |
| 2026-08-06 | 1 | Provider balance | idem |
| 2026-08-09 to 2026-08-10 | 2 | Provider balance | idem |
| 2026-08-24 to 2026-08-31 | 8 | Grok timeout (5 cancelled runs) and Anthropic balance (preflight) | `governance/HEALTH-CHECK-COLETA-20260831.md:23`, `:35`, `:53-59` |
| 2026-08-16 to 2026-09-08 | 17 lost of 24 | Balance on three providers plus Groq model retirement; of 35 days between 2026-08-05 and 2026-09-08, 13 have data | `governance/HEALTH-CHECK-APIS-20260908.md:44`, `:32-38` |

**Partial days, with cause.**

| Date | Coverage | Cause | Evidence |
|---|---|---|---|
| 2026-04-23 | 15 of 20 cells | Collection interrupted; first fail-loud activation | `docs/METHODOLOGY_V2.md:121` |
| 2026-04-24 | ~15 Claude fintech rows as `api_failure`, ~1.6% of the arm's day | Anthropic balance mid-run | `docs/audits/2026-04-26/INCIDENT-CLAUDE-CREDITS-2026-04-24.md:40` |
| 2026-05-01 | 9 of 20 cells | Health check failure | `docs/METHODOLOGY_V2.md:123` |
| 2026-05-04 | 15 of 20 cells | Partial recovery | `docs/METHODOLOGY_V2.md:125` |
| 2026-05-18 | 5 of 20 cells | Perplexity validation update: `max_tokens<16` rejected on `sonar` | `docs/METHODOLOGY_V2.md:129` |
| 2026-09-06 | Gemini, Grok, Perplexity only | ChatGPT 429, Claude 400; `MANDATORY_LLMS` downgraded | `git show origin/main:data/partial_days.json` |
| 2026-09-07 | Gemini, Grok, Perplexity only | idem | idem |
| 2026-09-08 | Started as above, completed by manual run 34256141784 with five arms | Balance, then manual top-up | `governance/HEALTH-CHECK-APIS-20260908.md:44`, `:81` |
| 2026-09-10 | missing Claude and Gemini (run 34459043572); missing ChatGPT and Claude (run 34530577090) | Anthropic 400, Google 429 "prepayment credits depleted", OpenAI 429 | `git show origin/main:data/partial_days.json` |
| 2026-09-11 | missing ChatGPT | OpenAI 429 | idem |

**Aborted runs with a cause on record, 2026-08-16 to 2026-09-08.** 49 runs: 3 succeeded (2026-08-16 twice, 2026-08-23 09:06, 2026-08-31 14:45 manual), 28 failed at preflight on balance or model, 17 were cancelled on 180-minute timeout or concurrency between 2026-08-19 and 2026-08-30, and 2 failed in collection (2026-08-31 21:10 and 2026-09-07 23:15, the latter with the degraded trio). A run counts on more than one line when two providers failed together (`governance/HEALTH-CHECK-APIS-20260908.md:21-40`).

### 4.4 Absences in the ledger itself

These are gaps in the record rather than gaps in the series, and the manuscript should either close them or declare them.

1. **The 2026-05-18 audit window starts nine days before the series.** The ledger table runs from 2026-04-14, while the confirmatory window opens 2026-04-23 with a zeroed dataset (`governance/DIA-1-MARCO-20260423.md:72-79`). The first row, "GAP TOTAL (9 dias)", therefore describes an interval in which the v2 instrument did not exist. **NOT DOCUMENTED**: nothing explains the choice of start date.
2. **No ledger entry exists for 2026-05-19 to 2026-07-24.** The itemised missingness table stops at 2026-05-18 and the next dated gaps are the balance stops from 2026-07-25 onward. The aggregate counts of aborted runs cover the period; the day-level causes do not.
3. **The reproducible query is defined but its output is not archived.** `VERIFICATION.md:159-166` gives the SQL that produces days-with-data, aborted and successful counts, and the file records no expected values for it, unlike every other entry in that document. That is why §4.2 carries two irreconcilable figures for 2026-08-31.
4. **Total-observation counts differ across same-day documents**: 80,638 and 83,486 for the non-auditable observations (§I15), and 18,560 against 19,328 observations in the two statements of the max-equals-min property (`governance/HEALTH-CHECK-COLETA-20260831.md:79` against `docs/research/methods-paper/MANUSCRIPT.md:226`). Both pairs are consistent with different snapshots on the same day, and neither document states its snapshot.
5. **The abstract and Table 5 disagree on one digit.** The abstract reports the Perplexity movement as 51.9% to 75.8% (`MANUSCRIPT.md:21`), Table 5 as 75.7% to 51.9% (`:245`), and `VERIFICATION.md:31` as 75.8% to 52.0% on a slightly different denominator (14,400 / 7,148 rows against the manuscript's 14,976 / 7,436). The 23.8-point delta is stable across all three; the levels are not.
6. **No document reconciles the published dashboard series with the manuscript series** (§I19C).
7. **The v1 window has no ledger.** Everything before 2026-04-23 is described in incident reports; no missingness table covers March and early April. Given that the v1 data was deleted, this is defensible, but the manuscript should say so rather than let the ledger appear to start at the beginning of the project.

---

## 5. Quotable passages

Ten short passages from internal documents that carry evidential weight in the paper. Portuguese originals with an English rendering; cite the original with file and line.

**Q1 — the distributional signature.** `governance/HEALTH-CHECK-COLETA-20260831.md:79`
> "Uma variável cujo máximo é igual ao mínimo em 18.560 observações não está medindo nada, está reportando um limite."
> *A variable whose maximum equals its minimum across 18,560 observations is not measuring anything; it is reporting a boundary.*

**Q2 — why a full test suite is not evidence of correct measurement.** `governance/HEALTH-CHECK-COLETA-20260831.md:77`
> "O defeito vivia um nível abaixo de toda afirmação que o pipeline fazia sobre si mesmo. Nenhuma asserção do pipeline era falsa; o conjunto delas simplesmente não cobria a pergunta 'essa string é a resposta do modelo?'."
> *The defect lived one level below every claim the pipeline made about itself. No assertion was false; the set of them simply did not cover the question "is this string the model's answer?"*

**Q3 — functional against distributional checking.** `governance/ASSINATURA-DISTRIBUCIONAL-20260831.md:52-55`
> "Um limite de instrumento é invisível para teste funcional e evidente numa distribuição. Teste funcional pergunta se o pipeline faz o que foi escrito; ele não pergunta se o que foi escrito mede o que se pretende medir."
> *An instrument ceiling is invisible to a functional test and obvious in a distribution. A functional test asks whether the pipeline does what was written; it does not ask whether what was written measures what is intended.*

**Q4 — the irreversible defect.** `governance/HEALTH-CHECK-COLETA-20260831.md:127`
> "A assimetria é corrigível porque a string truncada ainda é a string que o extrator viu, e re-extrair sobre ela reproduz exatamente a decisão original. Nenhum cuidado recupera texto que nunca foi gravado."
> *The asymmetry is correctable because the truncated string is still the string the extractor saw, and re-extracting over it reproduces the original decision exactly. No amount of care recovers text that was never stored.*

**Q5 — why a declared gap beats a silent partial day.** `governance/HEALTH-CHECK-COLETA-20260831.md:57`
> "Um dia parcial gravado silenciosamente custaria mais caro que oito dias de gap declarado, porque o gap entra no ledger de missingness e o dia parcial entra na série como se fosse observação completa."
> *A silently recorded partial day would cost more than eight days of declared gap, because the gap enters the missingness ledger and the partial day enters the series as if it were a complete observation.*

**Q6 — non-identification stated symmetrically.** `governance/HEALTH-CHECK-COLETA-20260831.md:117`
> "A direção do viés da janela não é identificada pelos dados coletados sob janela assimétrica. Afirmar a direção antiga era erro; afirmar a direção nova seria o mesmo erro com o sinal trocado."
> *The direction of the window bias is not identified by data collected under an asymmetric window. Asserting the old direction was an error; asserting the new one would be the same error with the sign flipped.*

**Q7 — the guard that always fails.** `governance/ASSINATURA-DISTRIBUCIONAL-20260831.md:89-91`
> "A primeira versão do guard não fazia essa distinção e reprovaria toda coleta futura. Um guard que reprova sempre é indistinguível de um guard desligado — o mesmo padrão do restore R2 que ficou dois meses inerte, invertido."
> *The first version of the guard did not draw that distinction and would have failed every future collection. A guard that always fails is indistinguishable from a guard that is switched off — the same pattern as the R2 restore that sat inert for two months, inverted.*

**Q8 — the initialisation path that hides its own failure.** `governance/HEALTH-CHECK-COLETA-20260831.md:137`
> "Todo `except` que degrada para log de nível baixo dentro de caminho de inicialização precisa de teste que exercite o caminho a partir do zero, porque o caminho incremental esconde a falha por definição."
> *Every `except` that degrades to a low-level log inside an initialisation path needs a test that exercises the path from zero, because the incremental path hides the failure by definition.*

**Q9 — CI success is not data.** `docs/INCIDENT_PIPELINE_2026-03-29.md:119-120`
> "'Success' no CI não significa que dados foram coletados. O critério de sucesso deve ser verificável — ex: checar que o DB cresceu, que `collection_runs` tem registro novo, que o count de citações aumentou."
> *"Success" in CI does not mean data was collected. The success criterion must be verifiable — that the database grew, that `collection_runs` has a new record, that the citation count rose.*

**Q10 — keeping the wrong forecast.** `governance/README.md:25`
> "Previsão que erra fica registrada com a medição que a corrigiu. Estimativa apagada depois de errar não ensina nada e ainda cria o hábito de apagar."
> *A forecast that misses stays on record next to the measurement that corrected it. An estimate deleted after being wrong teaches nothing and builds the habit of deleting.*

**Alternate, already in English, for the drift chapter.** `docs/research/methods-paper/MANUSCRIPT.md:343`
> "The generalisable lesson is that a degradation path which does not announce itself is indistinguishable from one that does not exist."

---

## 6. What is asserted here without documentary support

Nothing in §§1-5 is asserted from project memory. Three items were derived by direct inspection of code and data for this dossier rather than read from an existing record, and each is marked **NOT DOCUMENTED** at the point of use:

1. The 2026-06-17 Gemini boundary did not propagate to `docs/METHODOLOGY_V2.md:68`, `scripts/generate_dashboard_json.py:55` or `scripts/preflight_llm_check.py:113` (I9, I19B).
2. The public dashboard and the manuscript report different extraction columns and different probe filters, producing two per-arm series for the same object (I19C).
3. No record reconciles the 2026-04-26 empty-response explanation of the Gemini anomaly with the 2026-08-31 preamble explanation, and the fraction of Gemini rows with `output_tokens=0` was never reported (I6).

Each should be verified independently — the first two by reading the three files, the third by running the SQL already drafted at `docs/audits/2026-04-26/GEMINI-CITATION-RATE-INVESTIGATION.md:70-81` — before any of them appears in a submitted manuscript.
