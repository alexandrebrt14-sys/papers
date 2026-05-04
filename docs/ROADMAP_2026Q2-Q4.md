# Roadmap 2026 Q2-Q3-Q4 — papers

> Fonte: [`.cto/review-2026-05-04-masterplan-15-repos.md`](.cto/review-2026-05-04-masterplan-15-repos.md) e `planoCTO.html` (913 linhas).
> Próxima revisão CTO: **2026-08-01**.
> Owner: **Alexandre Caramaschi**.

## Sumário

- **Categoria:** pesquisa-cientifica
- **Criticidade:** media
- **Deadline principal do trimestre:** 2026-12 (deadline submissao SIGIR 2027)
- **Gates obrigatórios:** secret-scan

## Decisões pendentes do owner

- B-017 finalizar sync Supabase + secrets CI

## Q2 2026 (mai-jun-jul) — janelas críticas

_Sem ondas planejadas para Q2 2026._

## Q3 2026 (ago-set-out) — consolidação e infraestrutura

| ID | Janela | Esforço (h) | Owner | Critical path | Saída esperada | Pré-requisitos |
|---|---|---|---|---|---|---|
| Q3-W1 | 23-07 a 15-08 | 40 | Alexandre | Não | Analise H2 + manuscrito v0 SIGIR 2027 | Janela H2 fechada |

## Q4 2026 (nov-dez-jan/27) — captação 2027.1 + colheita

| ID | Janela | Esforço (h) | Owner | Critical path | Saída esperada | Pré-requisitos |
|---|---|---|---|---|---|---|
| Q4-W4 | 01-11 a 15-12 | 50 | Alexandre | Não | Submissao SIGIR 2027 (deadline esperado dez/2026) | Q3-W1 fechado |

## Observabilidade

papers.db SQLite, sync Supabase, dashboard probes marcados, balanceamento battery.

## Política de qualidade

Toda mudança neste repo passa pelos gates transversais aplicáveis:

- **Quality gate canônico** (Next.js/TS): `tsc` + `lint` + `vitest` + `next build` antes de push.
- **Voice Guard** (conteúdo Alexandre): `python scripts/python/voice_guard.py check --file ...` antes de publicar.
- **Migration gate pt_br** (SQL): grep de acentos obrigatório antes de `apply` via Management API.
- **Pre-commit hook** (todo repo cliente): `secret_guard` ativo via `git config core.hooksPath .githooks`.
- **Snapshot Shopify** (mutations produto/variant): JSON em `data/raw/shopify-audit-logs/` antes de `productUpdate`/`variantsBulkUpdate`.
- **Browser MCP visual double-check** (mudanças de UI): `getComputedStyle` antes/depois em 1440x900 e 390x844.
- **Schema.org JSON-LD** (todo conteúdo público): validação com `validate_graphql_codeblocks` ou Rich Results.

## Disciplina de deploy

- `landing-page-geo` no Vercel: máximo **2 pushes/dia** (build minutes ~$0,26/push).
- Pre-push hook roda `next build` localmente; falhar localmente = abortar push.
- Janelas com 2+ streams paralelos exigem revisão semanal de carga em segunda 09h BRT.

## FinOps

- LLM API spend rastreado em [`geo-finops/calls.db`](https://github.com/alexandre-/geo-finops).
- Build minutes Vercel monitorados; alertas WhatsApp/email em ≥80% da quota.
- Quebrar prompts no orchestrator: `< 5KB` input e `< 30KB` output (limite Gemini MAX_TOKENS).

## Política de revisão

- Toda decisão arquitetural significativa registrada como ADR em `docs/adr/`.
- Drift entre `adminalexandre` e `landing-page-geo`: pre-commit hook (deadline 20-05).
- Revisão CTO trimestral próxima: **2026-08-01**.

---

_Gerado automaticamente pela skill `/cto` em 2026-05-04 a partir do masterplan dos 15 repositórios._
