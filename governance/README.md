# Governança do projeto papers

Esta pasta guarda o registro narrativo do projeto: incidentes, marcos e revisões. O `CHANGELOG.md` na raiz diz **o que mudou no código**; os documentos aqui dizem **o que aconteceu, por que aconteceu e o que ficou em aberto**. Quando os dois divergem, o CHANGELOG é a fonte de verdade sobre a mudança e o documento de governança é a fonte sobre a decisão que a motivou.

Nada aqui é apagado depois de escrito. Documento com número errado ganha correção datada no próprio corpo, com a versão anterior visível, porque a série de decisões é parte do dado.

## Índice

| Documento | O que registra | Quando consultar |
|---|---|---|
| [`DIA-1-MARCO-20260423.md`](DIA-1-MARCO-20260423.md) | Abertura da janela confirmatória v2: estado do dataset zerado, infraestrutura, secrets, tags git, pendências mapeadas e cronograma de potência estatística. | Ao reconstruir o estado inicial da janela, ao auditar o que estava prometido no dia 1, ou ao verificar quais pendências da Onda 5 continuam abertas. |
| [`INCIDENT-RUN-CANCELLED-20260423.md`](INCIDENT-RUN-CANCELLED-20260423.md) | Run manual cancelada por overlap com o cron. Causa no `concurrency group` do GitHub Actions e o fix preventivo por `github.event_name`. | Ao investigar cancelamento de run sem erro no log, ou antes de mexer na configuração de concorrência do workflow. |
| [`HEALTH-CHECK-COLETA-20260831.md`](HEALTH-CHECK-COLETA-20260831.md) | Oito dias de série parada (timeout causado pelo raciocínio do Grok, saldo Anthropic esgotado) e o defeito de instrumento: a janela de observação era assimétrica entre os braços, a íntegra das respostas nunca foi gravada, e recusa era contada como alucinação. | Antes de usar qualquer número de taxa de citação anterior a 31-08-2026; ao investigar timeout de coleta; ao trabalhar em H2 ou na taxonomia de recusa. |
| [`REVISAO-EXTERNA-PAPER-20260831.md`](REVISAO-EXTERNA-PAPER-20260831.md) | Revisão adversarial do manuscrito BRGEO-1: quatro bloqueadores de submissão, sete correções de substância, a citação fundadora do campo corrigida e o levantamento do estado da arte de março a julho de 2026. | Antes de qualquer edição do manuscrito ou de `scripts/brgeo1_index.py`; ao montar a lista de referências; ao decidir a ordem de trabalho para a submissão. |

## Convenção de escrita

Cabeçalho com **Severidade**, **Status**, **Data** e **Escopo**. Corpo com sintoma, sequência de eventos quando houver, causa raiz, impacto, correção aplicada e verificação. Fecha com o que continua em aberto.

Três regras que a casa aprendeu na prática:

1. **Todo número traz o denominador e a data da medição.** Percentual sem denominador esconde mudança de amostra entre versões do mesmo documento.
2. **Todo critério de medição vai declarado junto do resultado.** Expressão regular, limiar de elegibilidade e janela de leitura são parte do número, não detalhe de implementação.
3. **Previsão que erra fica registrada com a medição que a corrigiu.** Estimativa apagada depois de errar não ensina nada e ainda cria o hábito de apagar.

## Relação com os outros registros

- `CHANGELOG.md` (raiz): mudança de código, formato Keep a Changelog. Eventos de série ficam marcados lá como tal.
- `docs/METHODOLOGY_V2.md`: metodologia canônica. As fronteiras de estrato vivem em §3.1 e a janela de observação em §4.1-bis.
- `data/finops_alerts.jsonl` e issues com label `pipeline-failure`: trilha de auditoria operacional das falhas de coleta.

- [`ASSINATURA-DISTRIBUCIONAL-20260831.md`](ASSINATURA-DISTRIBUCIONAL-20260831.md) — por que um limite de instrumento é invisível para teste funcional e evidente numa distribuição, e os três guards instalados em resposta. Consultar antes de confiar em suíte verde como evidência de que a medição está correta.
