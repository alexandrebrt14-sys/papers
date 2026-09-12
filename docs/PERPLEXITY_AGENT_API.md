# Perplexity: virada da Sonar Chat Completions para a Agent API

> **Ciclo encerrado em 11/09/2026.** Este documento preserva planejamento e procedimentos históricos. Coletas, calibrações e consultas experimentais estão bloqueadas; datas futuras abaixo não são agendamentos vigentes. Consulte [o registro final](ENCERRAMENTO_2026-09-11.md) antes de reutilizar o acervo ou propor outro estudo.

**Data**: 2026-09-09 · **Status**: implementado atrás de flag, desligado por padrão · **Prazo externo**: 27/09/2026

## Por que existe

A Perplexity lançou a Agent API em 13/08/2026 e marcou o fim de suporte da Sonar Chat Completions (`POST /chat/completions`) para **27/09/2026**. A janela confirmatória v2 deste repositório fecha, projetada, em 15/10/2026. Sem a virada, o braço Perplexity, o único com busca e o de maior taxa de citação (74,7% em 09/09), para 18 dias antes do fim da série.

Fontes consultadas em 09/09/2026: a referência da Agent API em `docs.perplexity.ai/docs/agent-api/quickstart` (endpoint `POST https://api.perplexity.ai/v1/agent`, alias `/v1/responses`; campos `model`, `input`, `instructions`, `tools`, `max_output_tokens`, `temperature`; resposta com `output[]` tipado em `message`, `search_results`, `fetch_url_results`) e o changelog em `docs.perplexity.ai/docs/resources/changelog`, que registra o fim de suporte em 27/09/2026 e o guia de mapeamento campo a campo.

## O que está implementado

| Componente | Arquivo | Comportamento com `PAPERS_PPLX_AGENT_API=1` |
|---|---|---|
| Coletor | `src/collectors/llm_client.py` (`_query_perplexity_agent`, `_parse_pplx_agent_output`) | `POST /v1/agent` com `model: perplexity/sonar` (o mesmo Sonar da rota legada), `instructions` = system prompt, `input` = pergunta, `tools: [{type: web_search}]`, `temperature 0`, `max_output_tokens` igual ao legado. Texto vem de `output[].type == message`, fontes de `search_results[].url` e `annotations[].type == url_citation`. Devolve o mesmo `LLMResponse` (janela de citação, `raw_text`, `sources`, `engine_type = rag`). |
| Preflight | `scripts/preflight_llm_check.py` (`check_perplexity`) | Sonda `/v1/agent` em vez de `/chat/completions`, para que o preflight teste a rota que a coleta vai usar. |
| Gate | `src/collectors/llm_client.py` (`pplx_agent_api_enabled`) | Lê `PAPERS_PPLX_AGENT_API`; só `"1"` liga. |
| Workflow | `.github/workflows/daily-collect.yml` | `PAPERS_PPLX_AGENT_API: ${{ vars.PAPERS_PPLX_AGENT_API || '0' }}` |

Decisões fixadas pela sondagem ao vivo de 08/09/2026 (documentada no código):

- **Não usar `preset`** (`fast`, `low`, `medium`, `high`): eles roteiam para modelos de terceiros (`fast` devolveu `openai/gpt-5.6-luna`) e trocariam o braço do estudo sem aviso. O modelo é sempre `perplexity/sonar`; `perplexity/sonar-pro` devolve 400.
- **Sempre com a tool `web_search`**: sem ela o Sonar responde sem fonte alguma, e a citação com fonte é o objeto da medição.
- **`model_version` gravado permanece `sonar`**: a série não muda de instrumento no meio.
- **Custo**: `usage.cost.total_cost` é o valor faturado; `web_search` custa US$ 0,0025 por chamada, contra US$ 0,005 de `request_cost` na rota legada.

## Testes (sem rede)

`tests/test_perplexity_agent_api.py` cobre: gate desligado por padrão; parse de `output` (texto, citações, hits); requisição com flag ligada (URL, modelo, ausência de `preset`, tools, headers) e forma da resposta; flag desligada mantendo `/chat/completions`; resposta sem `message` falhando alto; erro HTTP do `/v1/agent` propagando (`raise_for_status`) para que o circuit breaker trate como qualquer outro braço; preflight sondando `/v1/agent` quando a flag está ligada.

```
python -m pytest tests/test_perplexity_agent_api.py -q
```

## Como ativar (decisão do dono, sem custo adicional de código)

1. Confirmar que a chave `PERPLEXITY_API_KEY` tem saldo (a chave é a mesma para as duas rotas).
2. Rodar o preflight local com a flag para provar a rota antes de virar o cron:
   ```
   PAPERS_PPLX_AGENT_API=1 python scripts/preflight_llm_check.py
   ```
   Custo: uma chamada de 16 tokens de saída, mais uma `web_search` (US$ 0,0025).
3. Virar a variável de repositório:
   ```
   gh variable set PAPERS_PPLX_AGENT_API -R alexandrebrt14-sys/papers -b "1"
   ```
4. Observar a primeira coleta: `validate_v2_collection.py` e `distribution_guard.py` precisam passar com o braço Perplexity produzindo linhas e a janela de citação com a mesma forma.
5. Para voltar: `gh variable set PAPERS_PPLX_AGENT_API -R alexandrebrt14-sys/papers -b "0"` (vale até 27/09/2026; depois disso a rota legada deixa de responder).

## O que fica em aberto

- A decisão de virar antes de 27/09 é do dono; recomendação: virar assim que o saldo dos cinco provedores estiver normalizado, para que a primeira coleta pela nova rota aconteça com os outros braços presentes e a comparação entre motores não fique confundida com a troca de rota.
- O monitor de citação do `landing-page-geo` (`/api/cron/llm-citation-monitor`) usa a mesma rota legada e a mesma chave; a virada dele é trabalho daquele repositório.
