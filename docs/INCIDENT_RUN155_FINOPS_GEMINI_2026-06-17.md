# Incidente Run #155 + Fix do teto FinOps do Google + estado das LLMs

**Data da análise:** 2026-06-17
**Disparador:** e-mail de alerta "Papers daily-collect falhou — Run #155"
**Severidade:** baixa (incidente já encerrado; ação preventiva aplicada)

---

## 1. O que houve na Run #155

- **Run:** `27351297994`, 2026-06-11 13:45 UTC (run_number 155).
- **Step vermelho real:** **não foi coleta nem push** — foi o **Health check de cobertura**.
  O step "Health check (gating)" tem `continue-on-error: true`, então aparece "success" na
  lista de steps; o que falhou foi seu `outcome`, que disparou o step final
  "Fail workflow if health check failed" (`exit 1`) e enviou o e-mail.
- **Log decisivo:**
  ```
  [OK]   Coleta >= 200 obs nas ultimas 24h: 216 obs em 1 verticais x 4 LLMs
  [FAIL] 4/4 verticais coletaram nas ultimas 24h: faltando {varejo, tecnologia, saude}. presente: {fintech: 216}
  ```
- **Causa:** a #155 foi um de vários re-runs manuais (#148–#155) no meio da crise do
  `papers.db` cruzar 100 MB e sair do versionamento git (PR #20). O run regenerou o
  dashboard a partir da base pequena (216 queries) em vez da base recuperada
  (62.820 citations), porque o artifact do `recover-historical-db.yml` era invisível ao
  `daily-collect.yml`.
- **Resolução:** corrigido na **Run #156** (mesma noite) — download do artifact do recover
  + restore do R2 como source of truth (ver comentários no `daily-collect.yml`, steps
  "Download recovered DB" e "Restore DB from Cloudflare R2"). Desde então **6 dias
  consecutivos verdes (#156 → #167)**.

## 2. Estado atual (Run #167, 2026-06-17) — saudável

Todos os checks `[OK]`: DB 104,8 MB / 22 tabelas / **63.684 citações**;
**864 obs em 4/4 verticais × 4 LLMs** nas últimas 24h; 4/4 API keys válidas;
FinOps $58,88/$165 (36%); `/research` HTTP 200.

## 3. Teste funcional das 6 LLMs do orquestrador (geo-bridge ping)

| Provider | HTTP | Estado |
|---|---|---|
| Anthropic / OpenAI / Perplexity / Groq / xAI | 200 | OK, com crédito |
| **Google (Gemini)** | **429** | **wallet pré-pago AI Studio esgotado** |

Gemini é best-effort desde 2026-06-05 (fora de `MANDATORY_LLMS`,
`GEMINI_THINKING_BUDGET=1024`): sua falha não derruba mais a coleta, só deixa
lacuna de 1 dos 5 LLMs.

## 4. Fix aplicado — teto FinOps do Google (commit `5c269e0`)

**Problema:** o teto mensal vive na tabela SQLite `finops_budgets` **dentro do
`papers.db`** (restaurado do R2/artifact a cada run), **não no código**. E
`_ensure_budgets()` só faz INSERT quando a plataforma está ausente — **nunca
atualiza** um teto já existente. Resultado: o teto do Google ficou preso em **$50**
e bateu **108% (`is_blocked`)** em 2026-06-11, o que reprovaria o provider mesmo
após reabastecer o wallet.

**Correção:**
- `daily-collect.yml`: novo step **"Reconcile FinOps budget (Google ceiling)"** que
  aplica o teto via `python -m src.cli finops set-budget google` (UPDATE idempotente)
  sobre o DB restaurado, antes da coleta. Ajustável por repo var
  `GOOGLE_MONTHLY_BUDGET` / `GOOGLE_DAILY_BUDGET` (default 90/3).
- `tracker.py`: `DEFAULT_BUDGETS` google 15→90 (coerência para DB novo).

**Gotcha registrado:** o `papers.db` **local** diverge do CI (global 200 local vs
165 no CI). Nunca tratar o DB local como fonte de verdade do FinOps.

## 5. Causa raiz do 429 do Gemini (billing — verificado ao vivo 2026-06-17)

A API Gemini do projeto **`papers-geo`** (`gen-lang-client-0752800219`) pertence à
conta **`alexandre.brt14@gmail.com`** (owner IAM, provado por `gcloud`). NÃO é
`caramaschiai` nem `nuvini.ai`. O 429 vem do **wallet pré-pago do AI Studio**
(sistema separado do billing GCP, que está ativo).

Estado do billing (AI Studio → Billing, account `018118-741106-692775`, Tier 2):
- **Credit balance: −R$ 3,59 (negativo)** → "A credit balance above $0 is required to resume service".
- Última recarga **prepay R$ 400,00 em 2026-06-11**, consumida em ~6 dias.
- Consumo: Abr R$ 0,00 · Mai **R$ 334,57** · Jun(1–17) negativo.
- **Auto-reload: OFF** ← causa raiz sistêmica do esgotamento recorrente.

## 6. Ações do operador (não automatizáveis)

1. **Recarregar o wallet** em `https://aistudio.google.com/u/1/billing` (login
   `alexandre.brt14`) — botão "Buy credits".
2. **Ligar o auto-reload** ("Set up auto-reload") para evitar o esgotamento
   recorrente — correção durável.
3. (Opcional) Após reabastecer, re-incluir o Gemini nos obrigatórios:
   `gh variable set MANDATORY_LLMS -R alexandrebrt14-sys/papers -b "ChatGPT,Claude,Gemini,Perplexity,Groq"`.
