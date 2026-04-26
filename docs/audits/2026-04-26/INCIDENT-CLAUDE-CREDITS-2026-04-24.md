# Incident — Anthropic credit balance esgotado durante coleta v2

**Data**: 2026-04-24 (manhã, 10:18-10:48 UTC)
**Run afetado**: [#51 — 24884442588](https://github.com/alexandrebrt14-sys/papers/actions/runs/24884442588)
**Janela**: confirmatória v2 — Dia 2 de 90
**Severidade**: gap seletivo no dataset (afeta paper 5 — fintech/Claude)

## Resumo

Durante a coleta matinal de 2026-04-24, a chave `ANTHROPIC_API_KEY`
do repo `papers` parou de responder com:

```
HTTP 400: Your credit balance is too low to access the Anthropic API.
Please go to Plans & Billing to upgrade or purchase credits.
```

O loop sequencial executou ~15 queries da vertical **fintech** (PT+EN)
em Claude antes do `FAILED_VERTICALS` abortar com `exit 1`. Cada query
falhou com `api_failure`, gerando rows `cited=False` no banco para Claude
naquele subset.

## Linha do tempo

| Timestamp UTC | Evento |
|---|---|
| 2026-04-24 10:18 | Cron 06:00 BRT dispara run #51 |
| 2026-04-24 10:18:36 | Primeira `Claude HTTP 400 credit balance` |
| 2026-04-24 10:18-10:48 | ~15 queries Claude fintech retornam api_failure |
| 2026-04-24 12:23 | `FAILED_VERTICALS=fintech` aborta o job |
| 2026-04-24 21:48 | Cron 18:00 BRT roda com sucesso (creditos recargados) |

## Impacto científico

**Bias de seleção controlado.** Todas as queries Claude da fintech
matinal viraram `api_failure` na coluna `error_type`, distinguíveis das
respostas válidas. O comando de análise para H1 (Paper 5) deve filtrar
`error_type IS NULL` para excluir esse subset.

**Magnitude**: ~15 rows em ~960 queries Claude no dia 2 = ~1,6%.
Não invalida cientificamente a janela, mas precisa registro no
**Appendix E (Limitations)** do Paper 5.

## Por que falhou silenciosamente até abortar

1. O loop `for V in $VERTICALS` só checa `exit code` do `collect citation`.
2. `collect citation` só dá exit != 0 se o módulo Python crashar — `api_failure`
   por LLM individual é absorvido como linha no DB com `error_type='api_failure'`.
3. Resultado: 30min de queries sem Claude antes de qualquer alerta.

## Mitigação aplicada (2026-04-26)

Adicionado step **`Preflight LLM connectivity + auth check`** em
`.github/workflows/daily-collect.yml` ANTES do loop de verticais:

```yaml
- name: Preflight LLM connectivity + auth check
  run: python scripts/preflight_llm_check.py
```

Faz 1 call de 1 token para cada uma das 5 APIs (~US$0.0001 total).
Se qualquer 4xx aparecer (auth, quota, credit balance), aborta o job
**antes** de gravar dados parciais.

Exit code 2 do preflight bloqueia o workflow → dispara o alerting do
step `Alert on failure` (issue + email Resend).

## Lições

1. **Health check pré-coleta > pós-coleta.** Detectar 4xx auth antes de
   pagar pelo runner GitHub Actions e antes de viesar dados.
2. **`continue-on-error` em `collect citation` agora é seguro** porque o
   preflight garante que o handshake básico funciona. Se um provider cair
   no meio do loop (rate-limit transitório), continue-on-error dropa só
   essa query, não 30min.
3. **Anthropic é o único provider sem watchdog de balance ativo.** Fora de
   escopo desta correção, mas Alexandre deve adicionar à pendência P1.

## Próximos passos (humano)

- [ ] Ativar billing alert na Anthropic em US$5 mínimo
- [ ] Considerar pre-buy de US$50 mensal para janela v2 (até 21/07/2026)
- [ ] Auditar se há outros providers em risco similar (OpenAI, Groq prepay)
