# Investigação — Gemini 2.5 Pro com 1.4% de citation rate (suspeita de bug)

**Data**: 2026-04-26 (auditoria periódica)
**Status**: NÃO CORRIGIDO — mudança no `_query_google` invalida cientificamente
os 4 dias já coletados na janela v2 (cohort decision pendente do Alexandre).

## Observação

Snapshot `dashboard_data.json` em 2026-04-26 12:13 UTC:

| LLM | Queries | Cited | Rate |
|---|---:|---:|---:|
| Perplexity | 480 | 394 | **82.1%** |
| Claude | 891 | 240 | 26.9% |
| ChatGPT | 960 | 166 | 17.3% |
| Groq | 960 | 78 | 8.1% |
| **Gemini** | **960** | **13** | **1.4%** |

Gemini citou 12,8× menos que ChatGPT com mesmo `n=960`. Distribuição
**indistinguível** do incidente Groq de 13 dias silenciosos
(memória `feedback_mandatory_llms_fail_loud`).

## Hipótese mais provável: max_tokens esgotado pelo thinking

`src/collectors/llm_client.py` linhas 332-336:

```python
# Gemini 2.5 Pro usa thinking mode (gasta tokens internos antes de gerar output).
# Se max_output_tokens for igual ao texto desejado, o thinking esgota os tokens
# e candidates[0].content vem sem 'parts'. Solucao: 4x para modelos *-pro.
is_pro = "pro" in llm.model.lower()
max_tokens = llm.max_output_tokens * 4 if is_pro else llm.max_output_tokens
```

Para `gemini-2.5-pro` com `max_output_tokens=800` no config, isso resulta
em `maxOutputTokens=3200`.

Linhas 358-369 (handler do response vazio):

```python
candidates = data.get("candidates") or []
if not candidates:
    text = ""
else:
    content = candidates[0].get("content") or {}
    parts = content.get("parts") or []
    text_parts = [p.get("text", "") for p in parts if "text" in p]
    text = "".join(text_parts)
```

→ Quando o thinking esgota o orçamento, `parts` vem sem `text`, `text=""`,
e `_analyze_response_posthoc("")` retorna `cited=False` silenciosamente.
A row é gravada normalmente — apenas com `cited=False` e `output_tokens=0`.

## Evidência empírica anterior

Memória `feedback_gemini_25_pro_thinking_budget` (2026-04-24):

> Gemini 2.5 Pro thinking consome 1000-3000 tokens de maxOutputTokens.
> Com 1024 saía vazio (finishReason MAX_TOKENS, thoughtsTokenCount=1021).
> Fix: maxOutputTokens=8192. thinkingBudget=0 só funciona Flash.

3200 tokens está **dentro da zona de risco** documentada: queries de
fintech/saúde com thinking longo facilmente passam de 3000 tokens.

## Como confirmar (sem alterar nada)

Query SQL no `papers.db` (após 26/04 23:00 quando próximo run completar):

```sql
SELECT
    llm,
    COUNT(*) AS n,
    SUM(CASE WHEN output_tokens = 0 THEN 1 ELSE 0 END) AS zero_output,
    SUM(CASE WHEN LENGTH(response_text) = 0 THEN 1 ELSE 0 END) AS empty_text,
    SUM(CASE WHEN cited THEN 1 ELSE 0 END) AS cited
FROM citations
WHERE timestamp >= '2026-04-23'
GROUP BY llm
ORDER BY llm;
```

**Confirmação esperada**: `zero_output` e `empty_text` para Gemini ≈ 947
(960 - 13). Para os outros LLMs, ambos próximos de 0.

## Por que NÃO corrigir agora

A janela confirmatória v2 começou em 2026-04-23 com tag git
`v2-collection-start-20260423`. Mudar `max_tokens` para 8192 agora:

1. **Invalida cientificamente os 4 dias coletados.** O Gemini de 27/04 em
   diante teria distribuição diferente do Gemini de 23-26/04.
2. **Quebra a stopping rule pré-registrada** ("collect até 2026-07-21,
   sem peek") — qualquer mudança em meio à janela = p-hacking.
3. **Possível alternativa científica**: tratar Gemini como instrumento
   defeituoso desta janela e relatá-lo no Paper 5 como L8 (Limitação 8) +
   abrir janela v2.1 separada começando hoje.

## Decisão pendente do Alexandre

Três opções:

**A. Não mexer.** Aceita Gemini como instrumento ruidoso, registra
limitação no Paper 5. Janela v2 segue intacta até 21/07.

**B. Truncate + restart janela v2.** Apaga rows 23-26/04, ajusta
`max_tokens` para 8192, retoma com nova tag `v2-collection-start-20260427`,
janela vira 86 dias.

**C. Janela paralela v2-gemini-fixed.** Mantém v2 atual + roda v2.1 em
paralelo (só Gemini, max_tokens=8192) e usa para sensitivity analysis no
Paper 5 ("e se Gemini não tivesse o bug?"). Mais caro (Gemini paid),
mas cientificamente mais elegante.

Recomendação técnica (sem julgar mérito científico): **A** se prazo é
crítico, **C** se quer paper mais robusto, **B** se descobriu o bug
cedo o suficiente (dia 4 de 90 ainda permite restart com pouco prejuízo).
