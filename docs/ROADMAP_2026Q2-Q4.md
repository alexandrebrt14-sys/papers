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

### 2026-06-05 — Resiliência + economia do Gemini no pipeline diário

Otimizações de FinOps e resiliência aplicadas à coleta diária, **forward-only** e com a integridade científica preservada. O Gemini responde por ~91% do custo de LLM do paper (US$ 166 acumulados, contra US$ 16 da Anthropic, US$ 5,67 do Groq, US$ 2,50 da OpenAI e US$ 1,16 da Perplexity), o que justifica tratá-lo como ponto de atenção tanto de custo quanto de disponibilidade.

**(a) Resiliência do Gemini nos gates (a coleta não cai mais).**
`scripts/preflight_llm_check.py` e `scripts/health_check.py` passam a respeitar a variável `MANDATORY_LLMS`, tornando o Gemini **opcional** nos gates. O workflow `daily-collect.yml` define `MANDATORY_LLMS=ChatGPT,Claude,Perplexity,Groq`. Consequência prática: se o billing do Gemini esgotar (HTTP 429 / prepay obrigatório sem método), a coleta **degrada com WARNING** em vez de falhar — segue com os outros quatro LLMs e o gap fica registrado, em vez de zerar o dia inteiro de coleta. Commits `29152b4` e `cf802fe`.

**(b) Economia via `GEMINI_THINKING_BUDGET` (modelo permanece pinado).**
`src/collectors/llm_client.py` ganhou o cap configurável `GEMINI_THINKING_BUDGET` (default **1024** tokens, definido no `daily-collect.yml`), que limita apenas os tokens de "thinking" (raciocínio interno) do `gemini-2.5-pro`. Pontos críticos para a reprodutibilidade:

- O **modelo continua pinado** em `gemini-2.5-pro` — o check `check_model_pinning` segue válido e a reprodutibilidade permanece intacta. O teto atua sobre o orçamento de raciocínio, **não** sobre a identidade do modelo.
- A mudança é **forward-only**: os dados já coletados **não são reprocessados nem alterados**. As 54.980 citations acumuladas e o equilíbrio do cohort (ChatGPT 12.672, Claude 12.506, Gemini 12.138, Groq 12.672, Perplexity 4.992) permanecem como estão.
- Sem degradação observada: em teste, o modelo usou apenas ~323 thinking tokens, bem abaixo do teto de 1024 — ou seja, o cap não corta o raciocínio efetivo nas tarefas do paper, apenas evita gastos de cauda.

Commit `1cedf14`.

**Conclusão.** As duas mudanças reduzem custo e risco de indisponibilidade do componente mais caro do paper sem tocar na identidade do modelo nem nos dados históricos, preservando integridade científica e reprodutibilidade.

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
- Gemini = ~91% do custo de LLM do paper. Cap `GEMINI_THINKING_BUDGET` (default 1024) e Gemini opcional nos gates (`MANDATORY_LLMS`) reduzem custo e risco de indisponibilidade — ver entrada **2026-06-05** em Q2 2026.

## Política de revisão

- Toda decisão arquitetural significativa registrada como ADR em `docs/adr/`.
- Drift entre `adminalexandre` e `landing-page-geo`: pre-commit hook (deadline 20-05).
- Revisão CTO trimestral próxima: **2026-08-01**.

---

_Gerado automaticamente pela skill `/cto` em 2026-05-04 a partir do masterplan dos 15 repositórios._
