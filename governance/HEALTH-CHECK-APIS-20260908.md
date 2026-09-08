# Health-check das APIs e do crédito · 2026-09-08

**Severidade**: Alta. Dezessete dias de série perdidos entre 16-08 e 08-09-2026 por saldo esgotado em três provedores, dois dias coletados com metade do painel e uma retirada de API marcada para dentro da janela.
**Status**: Crédito restabelecido nos cinco provedores obrigatórios e verificado por chamada real. Gate para a nova API da Perplexity mesclado com o padrão desligado. Uma decisão continua aberta e está listada no fim.
**Data**: 2026-09-08
**Escopo**: chaves de API dos cinco braços, variável `MANDATORY_LLMS`, histórico do `daily-collect`, progresso da janela de 90 dias, retirada da Sonar Chat Completions.
**Fora de escopo**: saldo em dólar de cada conta. A extensão do navegador não pareou nesta sessão e os consoles não foram lidos; o que se sabe dos saldos vem da sessão paralela do `geo-orchestrator` na mesma data (wiki, página "Verificação com crédito 08/09/2026").

---

## Sumário

Às 09:10 UTC de 08-09 o cron ainda barrava no preflight: OpenAI devolvia 429 "no credits remaining", Anthropic 400 "credit balance is too low" e Perplexity 401 `insufficient_quota`. Às 12:30 UTC, depois da recarga manual feita pelo Alexandre nas três contas, `scripts/preflight_llm_check.py` com as chaves de `.env` passou 5 de 5 (ChatGPT 570 ms, Claude 737 ms, Gemini 1.908 ms, Perplexity 1.641 ms, Grok 3.376 ms). As seis chaves de `papers/.env` são idênticas às de `geo-orchestrator/.env`.

Três coisas estavam erradas além do saldo. A variável de repositório `MANDATORY_LLMS` tinha sido rebaixada para `Gemini,Perplexity,Grok` em 07-09 às 23:15 UTC, o que tornava ChatGPT e Claude opcionais e contrariava a metodologia. O clone local estava 13 commits atrás e com um `papers.db` de 17-06, o que fazia `window_progress.py` reportar 38 dias coletados quando o banco do R2 tem 53. E `test.yml` estava vermelho desde 03-09 sem defeito algum no instrumento.

## Parte 1. O que o saldo custou à série

### 1.1 Histórico do `daily-collect` entre 16-08 e 08-09

Medido em `gh run list` (49 runs, conclusão e causa lida no log de cada falha):

| Resultado | Runs | Detalhe |
|---|---:|---|
| Sucesso | 3 | 16-08 (2 runs), 23-08 09:06, 31-08 14:45 (manual) |
| Falha no preflight por saldo ou modelo | 28 | ver tabela abaixo |
| Cancelada | 17 | timeout de 180 min ou concorrência, 19-08 a 30-08 |
| Falha na coleta (vertical) | 2 | 31-08 21:10 e 07-09 23:15 (manual com o trio degradado) |

Provedor que barrou o preflight, por período:

| Provedor | Runs barradas | Período | Causa registrada no log |
|---|---:|---|---|
| Groq | 5 | 17-08 a 19-08 | modelo `llama-3.3-70b-versatile` aposentado (404); Grok entrou no lugar em 19-08 |
| Grok | 2 | 23-08 21:05 e 24-08 09:16 | saldo xAI |
| Claude | 12 | 28-08 a 06-09 | 400 "credit balance is too low" |
| ChatGPT | 7 | 01-09 a 03-09 e 06-09 a 07-09 | 429 "no credits remaining" |
| Perplexity | 6 | 01-09 a 03-09 e 08-09 09:09 | 401 `insufficient_quota` |

Um run conta em mais de uma linha quando dois provedores falharam juntos.

### 1.2 Efeito no banco

Consulta ao `papers.db` do R2 em 08-09 (`GROUP BY date(created_at), llm`, sem probes): dos 35 dias entre 05-08 e 08-09, **13 têm dado**. Os dias 06-09 e 07-09 têm só Gemini, Grok e Perplexity, produto de coletas locais com a variável degradada; são dias metodologicamente incompletos e a análise por braço precisa tratá-los como tal. O dia 08-09 começou assim e foi completado pela run manual das 17:16 UTC com os cinco braços. A janela acumulada está em **53 de 90 dias, 85.359 observações, 1.611 por dia coletado**, com fechamento projetado para **15-10-2026** se as duas coletas diárias voltarem a persistir sem interrupção.

A previsão anterior, registrada em 10-08, era 28-09-2026 com 49 dias por coletar. Entre 10-08 e 08-09 passaram 29 dias e só 12 entraram na série; a diferença de 17 dias é o custo da falta de crédito.

### 1.3 Correção

- Recarga manual de OpenAI, Anthropic e Perplexity pelo Alexandre em 08-09 (ação de console, não de API). Recarga automática segue desligada nas três por decisão de 24-07-2026.
- `MANDATORY_LLMS` removida como variável de repositório em 08-09; vale de novo o padrão do workflow, `ChatGPT,Claude,Gemini,Perplexity,Grok`.
- Coleta manual `workflow_dispatch` disparada às 17:16 UTC com os cinco obrigatórios (run 34256141784) para recuperar a rodada da manhã e validar os secrets do CI. Terminou verde às 19:32 UTC; detalhe na seção Verificação.

## Parte 2. O clone local mentia sobre a janela

`data/papers.db` saiu do git em junho (issue #40) e a fonte de verdade é `papers/db/latest.db` no bucket R2 `papers-research-db`. O clone local guardava um banco de 17-06 com 58.340 linhas, e `scripts/window_progress.py` lido sobre ele dizia 38 dias e previsão 30-10. `python scripts/r2_sync.py pull` (política forward-only, adotou o R2 com 206.121 linhas contra 140.413) corrigiu a leitura para 53 dias e 15-10. Regra que fica: antes de citar qualquer número de progresso, fazer `pull` do R2; o banco do clone é cópia de trabalho, não fonte.

## Parte 3. CI vermelho sem defeito no instrumento

`test.yml` falhava em todo push desde 03-09 em dois testes de `tests/test_distribution_guard.py`. O guard distribucional media a retenção da íntegra com `timestamp >= now - 2 days` fixo, enquanto o perfil obedecia `--since-days`; os testes fixam linhas em 31-08, então passaram no dia em que o guard nasceu e reprovaram dois dias depois. PR #57 (commit `6a5ea63`) faz `avaliar()` receber a mesma janela do perfil. Sobre o banco do R2 o guard segue aprovando com "íntegra retida"; suíte com 263 testes verde.

## Parte 4. A Sonar Chat Completions acaba em 27-09-2026

A Perplexity retira a rota `/chat/completions` em 27-09-2026 (anúncio oficial de 13-08-2026 no fórum da plataforma), dezoito dias antes do fechamento projetado da janela. Como a Perplexity é braço obrigatório, sem ação o preflight passaria a falhar todo dia e a série pararia.

Sondagem ao vivo em 08-09 com a chave do projeto em `POST /v1/agent`:

| Chamada | Modelo devolvido | Observação |
|---|---|---|
| `preset: fast` | `openai/gpt-5.6-luna` | preset roteia para modelo de terceiros |
| `preset: low` e `preset: medium` | `openai/gpt-5.6-luna` | idem |
| `model: perplexity/sonar` | `perplexity/sonar` | mesmo modelo do braço atual |
| `model: perplexity/sonar-pro`, `sonar-reasoning-pro`, `sonar-reasoning` | HTTP 400 "not supported" | só o sonar básico segue endereçável |

Sem a tool `web_search` o sonar respondeu sem fonte alguma; com ela as URLs vêm no item `output[].type == "search_results"` e, quando cita, em `annotations[type == "url_citation"]`. O custo faturado vem em `usage.cost.total_cost`: US$ 0,0025 por busca contra US$ 0,005 de `request_cost` na rota legada.

**Correção**: PR #58 (commit `87ac7a2`) adiciona `LLMClient._query_perplexity_agent` e o mesmo caminho no preflight, atrás da variável de repositório `PAPERS_PPLX_AGENT_API` (padrão `0`). Mesmo modelo, mesma janela de citação, mesma íntegra em `response_full_text`, `raw` com o payload novo por linha. Cinco testes novos; suíte com 268 verde. Smoke real com a chave do projeto: preflight OK em 1.415 ms; uma query do coletor devolveu 832 caracteres, 15 fontes, 3 entidades da coorte, US$ 0,00442.

## Verificação: a run manual terminou verde

Run 34256141784, `workflow_dispatch` com `vertical=all`, de 17:16 a 19:32 UTC (135 minutos, dentro do timeout de 180). Todos os steps verdes, inclusive os que costumam esconder problema atrás de `continue-on-error`.

| Braço | Linhas na run | Taxa de citação na run |
|---|---:|---:|
| ChatGPT | 233 | 38,6% |
| Claude | 233 | 42,5% |
| Gemini | 233 | 25,8% |
| Grok | 233 | 44,6% |
| Perplexity | 144 | 62,5% |

A Perplexity tem menos linhas por desenho (só categorias de alto valor e probes). Probes adversariais: 320 linhas marcadas, 0 acertos espontâneos em 756 respostas. Guard distribucional aprovado com íntegra retida. Piso de integridade elevado: `citations` de 65.060 para 86.543, `collection_runs` de 516 para 672. Banco publicado no R2 e adotado localmente pelo `pull` forward-only (208.975 linhas totais). A janela segue em 53 de 90 dias porque 08-09 já contava; a previsão de fechamento permanece 15-10-2026.

Issue #54 `pipeline-failure` fechada com o link para este registro.

## O que continua em aberto

1. **Decisão de virar a chave antes de 27-09.** `gh variable set PAPERS_PPLX_AGENT_API -R alexandrebrt14-sys/papers -b "1"` seguido de uma coleta manual de validação. É troca de transporte do braço Perplexity com o modelo preservado; a linha grava `model` e `raw`, então a fronteira fica auditável. Sem a virada, a série para em 27-09 com 37 dias faltando.
2. **Saldos em dólar não lidos nesta verificação.** A regra de alerta (Anthropic abaixo de US$ 100, OpenAI abaixo de US$ 50, Perplexity abaixo de US$ 40) só pode ser aplicada com leitura de console. No ritmo dos 30 dias anteriores (Perplexity US$ 206, xAI US$ 184, lidos pela sessão do orquestrador) o saldo de hoje cobre cerca de duas semanas.
3. **O workflow não fecha a issue `pipeline-failure` quando volta ao verde.** A #54 foi fechada à mão em 08-09; a próxima falha abre outra. Vale um step de fechamento automático em sucesso.
4. **Dias 06-09 e 07-09 com três braços.** Marcar na análise como incompletos ou excluir da comparação entre motores; a decisão é do desenho, não do pipeline.
