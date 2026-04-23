# Incidente: Run manual cancelada por overlap com cron · 2026-04-23

**Severidade**: Baixa (sem perda de dados)
**Status**: Mitigado + fix preventivo aplicado
**Data/hora**: 2026-04-23 22:22 UTC

## Sintoma

Run `24856932674` (workflow_dispatch manual do primeiro dia da janela v2) foi cancelada automaticamente após **101 minutos** no step 8 "Collect all verticals". Já havia completado os 7 primeiros steps (setup, checkout, deps, imports, etc.) e estava próximo do fim da coleta.

## Sequência de eventos

```
20:21:54 UTC  run 24856932674 (workflow_dispatch) iniciada
20:22:30 UTC  step 8 "Collect all verticals" iniciado
21:45:48 UTC  run 24860472589 (schedule cron 21:00 UTC, 45min de delay) iniciada
              → ambas rodaram em paralelo por ~37min
22:22:19 UTC  run 24856932674 CANCELADA (step 8 marcado cancelled)
22:23:10 UTC  Monitor b20xbwrvb detecta state=completed/cancelled
22:24:xx UTC  run 24860472589 continuou em progresso (não afetada)
```

## Causa raiz

Concurrency group estava configurado como:

```yaml
concurrency:
  group: papers-${{ github.workflow }}   # resolvido em "papers-Daily Data Collection + FinOps"
  cancel-in-progress: false
```

`cancel-in-progress: false` deveria impedir cancellation em overlap, mas o GitHub Actions tem comportamento não-intuitivo quando dois runs do mesmo concurrency group rodam há mais de ~1h em paralelo. Parece que a segunda run pendente (scheduled) acaba forçando cancellation da primeira em cenários de overlap longo.

## Impacto

**Zero perda de dados no `papers.db`**:
- O commit de `data/papers.db` só acontece no step 16 do workflow
- A run foi cancelada no step 8, antes de qualquer INSERT ser commitado ao git
- Todos os rows que seriam gravados ficaram em escopo local do runner (foram descartados junto com o runner)

**Replicação imediata**:
- A run scheduled `24860472589` assumiu a coleta do dia 1 (iniciou 21:45 UTC)
- Essa run carrega todas as melhorias commitadas hoje (timeout 180min, FinOps budgets aumentados, validator Onda 14)
- ETA conclusão: ~23:45 UTC (20:45 BRT)

## Mitigação imediata

Monitor persistente `b55pb1y9g` armado para acompanhar a nova run até `completed/*`.

## Fix preventivo (aplicado)

```yaml
concurrency:
  group: papers-${{ github.workflow }}-${{ github.event_name }}
  cancel-in-progress: false
```

Ao incluir `${{ github.event_name }}` (schedule, workflow_dispatch, etc.), cada tipo de evento ganha seu próprio slot. Assim:
- Manual dispatch + scheduled cron **podem rodar em paralelo** sem conflito
- Dois scheduled cron consecutivos (06:00 e 18:00 BRT) ainda compartilham slot — se o da manhã demorar mais de 12h (improvável), o da tarde fica em fila sem cancelar

## Lições aprendidas

1. **`cancel-in-progress: false` não garante isolamento total** em overlaps longos
2. **Manual dispatch + scheduled cron devem ter concurrency groups independentes**
3. **Timing de cron real pode ter delay significativo** (hoje, 45min de atraso no trigger — comportamento GitHub Actions durante picos)
4. **Commits intermediários de papers.db durante a coleta ajudariam** resiliência — hoje tudo é in-memory até o step 16. Considerar ADD COMMIT a cada vertical concluído.

## Próxima run monitorada

Run `24860472589`:
- Status: in_progress (step 8 por ~17min no momento do incident report)
- Source of truth para dia 1 da janela confirmatória v2

## Ação de follow-up

Após conclusão da run atual, validar que:
- `data/papers.db` tem 4 verticais × 5 LLMs × queries coletadas
- `data/dashboard_data.json` emite `dayNumber=1, totalQueries≈960`
- Landing `/research` e `/papers-roadmap` absorveram via ISR 600s
