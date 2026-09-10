# Chaves de API compartilhadas entre três instrumentos

**Severidade**: alta (risco de disponibilidade, não de vazamento) · **Status**: aberto, decisão do dono · **Data**: 2026-09-09 · **Escopo**: `papers/.env`, `geo-orchestrator/.env`, cron `llm-citation-monitor` e morning-digest do `landing-page-geo`; secrets do GitHub Actions dos três repositórios.

Este documento não move segredo nenhum e não cita valor de chave. Registra o risco, o incidente que o provou e a recomendação.

## Sintoma

Entre 28/08 e 08/09/2026 três medições independentes pararam ao mesmo tempo:

| Instrumento | O que mede | Como parou |
|---|---|---|
| `papers` (`daily-collect`) | Citação de 127 entidades por 5 LLMs, série de 90 dias | Preflight abortou 28 runs: Anthropic 400 "credit balance is too low" (28/08 a 06/09), OpenAI 429 "no credits remaining" (01/09 a 03/09, 06/09 a 07/09), Perplexity 401 `insufficient_quota` (01/09 a 03/09, 08/09), Gemini 429 "prepayment credits depleted" (09/09 21:10 UTC) |
| Monitor de citação da marca (`landing-page-geo`) | Menção de Alexandre Caramaschi e Brasil GEO em 37 prompts por 4 engines | Anthropic http_400 em 25 de 25 linhas em 28/08 (saldo negativo em US$ 0,30); gravado como coleta morta |
| Morning-digest (`landing-page-geo`) | Resumo diário por e-mail | Sem saída no mesmo período (mesma chave Anthropic) |

Causa comum, verificada no `HEALTH-CHECK-APIS-20260908.md`: as seis chaves de `papers/.env` são idênticas às de `geo-orchestrator/.env`, e a chave Anthropic do cron de citação é a mesma do morning-digest. Uma conta esgotada derruba os três ao mesmo tempo, e cada um deles tem o seu próprio alerta, o seu próprio incidente e o seu próprio agente tentando recarregar a mesma conta.

## Por que é um risco e não só um inconveniente

1. **Correlação de falhas entre séries que deveriam ser independentes.** A série do `papers` e a do monitor de marca são usadas juntas na home do brasilgeo.ai e no `/research`. Quando as duas param no mesmo dia, o buraco parece um evento do mundo e não do caixa.
2. **Consumo invisível.** O `geo-orchestrator` gasta em rodadas de pesquisa factual (US$ 2 a 3,7 por rodada em 09/09), o `papers` em coleta (US$ 2 a 3 por dia). Como saem da mesma conta, o teto diário do FinOps do `papers` (`finops_checkpoint.json`) mede só a parte dele e o saldo acaba antes do previsto.
3. **Rotação difícil.** Trocar uma chave vazada exige atualizar três `.env` locais, três conjuntos de secrets no GitHub e a Vercel, com janela em que um deles fica fora.
4. **Atribuição de custo impossível.** O painel de billing do provedor mostra uma linha; não há como saber qual instrumento gastou.

## Recomendação

| Ação | Quem | Custo |
|---|---|---|
| Uma chave por instrumento e por provedor (mínimo: `papers`, `geo-orchestrator`, `landing-page-geo`), com nome da chave = nome do instrumento no painel do provedor | dono (cria) e agente (grava nos secrets) | zero; OpenAI, Anthropic, Google, Perplexity e xAI permitem várias chaves por conta |
| Onde o provedor permitir, projeto ou workspace separado por instrumento, com **teto de gasto por projeto** (OpenAI projects, Anthropic workspaces, Google Cloud projects) | dono | zero |
| Alerta de saldo por provedor com limiar em dias de coleta, não em valor absoluto: o `papers` gasta ~US$ 2 a 3 por dia, então US$ 15 de saldo é aviso e US$ 6 é crítico | agente (`src/finops/monitor.py` já tem o gancho) | zero |
| Auto-reload desligado desde 24/07 por decisão do dono: manter, mas com o alerta acima chegando antes do preflight falhar | dono | decisão |
| Documentar no `README` de cada repo qual chave ele usa e onde está o billing, apontando para `reference_billing_apis_geo_orchestrator_contas_e_urls_20260908.md` da memória do operador | agente | zero |
| Preflight do `papers` em modo `degrade` (implementado neste PR): provedor sem saldo vira dia parcial em vez de dia perdido | feito | — |

## O que continua em aberto

- Criar as chaves é ação de billing e fica com o dono; o agente não deve gerar chave nem alterar plano.
- Enquanto as chaves forem compartilhadas, todo incidente de saldo deve ser registrado uma vez só, no repo do instrumento que detectou primeiro, com referência cruzada nos outros dois, para não abrir três issues sobre a mesma conta.
