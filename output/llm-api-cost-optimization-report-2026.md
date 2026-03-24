# Relatório: Otimização de Custos com APIs de LLM para Monitoramento de Citações de Fintechs

**Data:** 2026-03-24
**Caso de uso:** Monitoramento de coorte de 15 fintechs brasileiras -- verificar como LLMs citam cada entidade e quais fontes referenciam.

---

## 1. Tabela de Preços por Modelo (Março 2026)

Todos os preços em USD por 1 milhão de tokens (MTok).

### OpenAI

| Modelo | Input | Output | Cached Input | Batch Input | Batch Output |
|--------|-------|--------|-------------|-------------|--------------|
| GPT-5.2 (flagship) | $1.75 | $14.00 | $0.175 | ~$0.875 | ~$7.00 |
| GPT-5 nano | **$0.05** | **$0.40** | $0.005 | ~$0.025 | ~$0.20 |
| GPT-4o-mini (legado) | $0.15 | $0.60 | $0.075 | $0.075 | $0.30 |
| GPT-4o (legado) | $2.50 | $10.00 | $1.25 | $1.25 | $5.00 |

**Batch API:** 50% de desconto, processamento assíncrono em até 24h, até 50.000 requests por batch.
**Prompt Caching:** Automático para prompts >1.024 tokens. Cache hit = 50% de desconto (algumas fontes indicam até 90%). Cache expira em 5-10 minutos de inatividade.

### Anthropic (Claude)

| Modelo | Input | Output | Cache Write 5m | Cache Read | Batch Input | Batch Output |
|--------|-------|--------|---------------|------------|-------------|--------------|
| Opus 4.6 | $5.00 | $25.00 | $6.25 | $0.50 | $2.50 | $12.50 |
| Sonnet 4.6 | $3.00 | $15.00 | $3.75 | $0.30 | $1.50 | $7.50 |
| **Haiku 4.5** | **$1.00** | **$5.00** | $1.25 | $0.10 | **$0.50** | **$2.50** |
| Haiku 3.5 | $0.80 | $4.00 | $1.00 | $0.08 | $0.40 | $2.00 |
| **Haiku 3** | **$0.25** | **$1.25** | $0.30 | $0.03 | **$0.125** | **$0.625** |

**Batch API:** 50% de desconto, até 10.000 queries por batch, processamento em até 24h.
**Prompt Caching:** Cache read = 10% do preço base de input. Cache write 5m = 1.25x, cache write 1h = 2x. Se paga após 1 leitura (5m) ou 2 leituras (1h).
**Combinação:** Batch + Cache podem ser combinados (descontos cumulativos).

### Google Gemini

| Modelo | Input | Output | Batch Input | Batch Output | Cache Read |
|--------|-------|--------|-------------|--------------|------------|
| Gemini 3.1 Pro Preview | $2.00 | $12.00 | $1.00 | $6.00 | $0.20 |
| **Gemini 3.1 Flash-Lite** | **$0.25** | **$1.50** | **$0.125** | **$0.75** | -- |
| Gemini 3 Flash Preview | $0.50 | $3.00 | $0.25 | $1.50 | $0.05 |
| Gemini 2.5 Pro | $1.25 | $10.00 | $0.625 | $5.00 | $0.125 |
| **Gemini 2.5 Flash** | **$0.30** | **$2.50** | **$0.15** | **$1.25** | $0.03 |
| **Gemini 2.5 Flash-Lite** | **$0.10** | **$0.40** | **$0.05** | **$0.20** | -- |

**Batch API:** 50% de desconto em todos os modelos pagos.
**Free Tier:** Gemini Flash-Lite tem tier gratuito disponível.
**Google Grounding (Search):** $14/1.000 queries (Gemini 3.x), $35/1.000 queries (Gemini 2.x). Primeiros 1.500 queries/dia grátis no tier pago.

### Perplexity Sonar

| Modelo | Input/MTok | Output/MTok | Request Fee (Low) | Request Fee (Med) | Request Fee (High) |
|--------|-----------|------------|-------------------|-------------------|--------------------|
| **Sonar** | **$1.00** | **$1.00** | $5/1K req | $8/1K req | $12/1K req |
| Sonar Pro | $3.00 | $15.00 | $6/1K req | $10/1K req | $14/1K req |
| Sonar Reasoning Pro | $2.00 | $8.00 | $6/1K req | $10/1K req | $14/1K req |
| Sonar Deep Research | $2.00 | $8.00 | -- | -- | -- |

**Nota importante:** Tokens de citação NÃO são cobrados no Sonar e Sonar Pro. Citações vêm embutidas na resposta sem custo adicional.

---

## 2. Modelo Recomendado por Provedor para Monitoramento

O caso de uso é simples: enviar uma pergunta ("O que é Nubank?" ou "Quais são as melhores fintechs do Brasil?"), receber resposta e verificar se cada entidade da coorte foi mencionada e quais fontes foram citadas.

| Provedor | Modelo Recomendado | Custo por Query Estimado | Justificativa |
|----------|--------------------|--------------------------|---------------|
| **OpenAI** | GPT-5 nano | ~$0.0001-0.0005 | Mais barato da OpenAI, suficiente para classificação |
| **Anthropic** | Haiku 3 (Batch) | ~$0.0002-0.0008 | Batch = $0.125 input. Mais barato possível |
| **Google** | Gemini 2.5 Flash-Lite (Batch) | ~$0.0001-0.0003 | $0.05 input em batch. Custo quase zero |
| **Perplexity** | Sonar (Low context) | ~$0.005-0.01 | Citações grátis embutidas. Único que faz busca real |

**Recomendação final para monitoramento de citações de fintechs:**
- **Perplexity Sonar (Low)** para queries que precisam de busca web real + citações ($5/1K requests + tokens)
- **Gemini 2.5 Flash-Lite Batch** para queries de classificação/análise ($0.05-0.10/MTok)

---

## 3. Descontos de Batch API -- Resumo

| Provedor | Desconto | Limite por Batch | Prazo de Entrega | Endpoint |
|----------|----------|-----------------|------------------|----------|
| OpenAI | 50% | 50.000 requests / 200 MB | 24h | POST /v1/batches |
| Anthropic | 50% | 10.000 requests | 24h | POST /v1/messages/batches |
| Google Gemini | 50% | Variável | 24h | BatchGenerateContent |

**Workflow padrão (OpenAI/Anthropic):**
1. Preparar arquivo JSONL com requests
2. Upload do arquivo via Files API
3. Criar batch job com file_id
4. Polling de status até completar
5. Download dos resultados

---

## 4. Técnicas de Redução de Tokens com Estimativa de Economia

### 4.1. TOON (Token-Oriented Object Notation) -- Economia: 30-60%

Substitui JSON por formato otimizado que remove pontuação redundante. Ideal para dados tabulares/planos.

```
# JSON (mais tokens):
{"name": "Nubank", "segment": "digital bank", "market": "Brazil"}

# TOON (menos tokens):
name: Nubank
segment: digital bank
market: Brazil
```

### 4.2. Structured Output / JSON Mode -- Economia: 40-60% vs texto livre

Forçar resposta JSON mínima em vez de texto verboso:

```python
# OpenAI - Structured Output
response = client.chat.completions.create(
    model="gpt-5-nano",
    response_format={"type": "json_schema", "json_schema": {
        "name": "citation_check",
        "schema": {
            "type": "object",
            "properties": {
                "mentioned": {"type": "boolean"},
                "sources": {"type": "array", "items": {"type": "string"}},
                "context": {"type": "string"}
            },
            "required": ["mentioned", "sources"]
        }
    }},
    messages=[{"role": "user", "content": "Did you mention Nubank in your response?"}]
)
```

### 4.3. Prompt Caching -- Economia: até 90% em input tokens

Para monitoramento repetitivo com system prompt idêntico:

```python
# Anthropic - Prompt Caching
response = client.messages.create(
    model="claude-haiku-4-5-20250514",
    max_tokens=256,
    system=[{
        "type": "text",
        "text": "You are a citation monitor. Check if the fintech entity...",
        "cache_control": {"type": "ephemeral"}  # cache por 5 min
    }],
    messages=[{"role": "user", "content": query}]
)
# Primeiro request: 1.25x do preço base (cache write)
# Requests subsequentes (5 min): 0.1x do preço base (cache read)
```

### 4.4. Minimizar Output com max_tokens -- Economia: 50-80% em output tokens

```python
# Limitar output a 100-200 tokens para resposta sim/não com fontes
response = client.chat.completions.create(
    model="gpt-5-nano",
    max_tokens=150,  # Força resposta curta
    messages=[...]
)
```

### 4.5. LLM-as-Judge (Modelo Barato para Analisar) -- Economia: 80-95%

Padrão de dois estágios:
1. **Estágio 1 (Query):** Perplexity Sonar (Low) faz a busca e retorna texto + citações
2. **Estágio 2 (Análise):** GPT-5 nano ou Gemini Flash-Lite classifica a resposta

```python
# Estágio 1: Perplexity busca (custo: ~$0.006/query)
search_result = perplexity_client.chat.completions.create(
    model="sonar",
    web_search_options={"search_context_size": "low"},
    messages=[{"role": "user", "content": "What are the best digital banks in Brazil?"}]
)

# Estágio 2: GPT-5 nano classifica (custo: ~$0.0001/query)
analysis = openai_client.chat.completions.create(
    model="gpt-5-nano",
    max_tokens=100,
    response_format={"type": "json_object"},
    messages=[{
        "role": "system",
        "content": "Analyze if the fintech entities were mentioned. Return JSON: {entities: [{name: str, mentioned: bool}], sources: [urls]}"
    }, {
        "role": "user",
        "content": search_result.choices[0].message.content
    }]
)
```

**Custo total estimado:** ~$0.006/query (vs $0.05+ usando modelo premium)

---

## 5. Fontes Alternativas Gratuitas/Baratas para SERP e Citações

| Serviço | Preço | Free Tier | Melhor Para |
|---------|-------|-----------|-------------|
| **SearXNG** | Grátis (self-hosted) | Ilimitado | Meta-search gratuito, sem rastreamento |
| **Brave Search API** | $5/1K requests | $5/mês em créditos (~1K queries) | Índice próprio, grounding API |
| **Tavily** | $0.008/crédito | 1.000 créditos/mês | Busca otimizada para AI/RAG |
| **Serper.dev** | $0.001/query | 2.500 queries/mês | Google SERP barato |
| **SerpAPI** | $15/1K queries | 250 queries/mês | Multi-engine SERP |
| **Google Grounding** | $14/1K queries | 1.500/dia (tier pago) | Citações integradas no Gemini |
| **Perplexity Sonar** | $5-12/1K requests | -- | Busca + citações num só request |

### Recomendação para Monitoramento de Citações de Fintechs

**Combinação mais barata:**

1. **SearXNG self-hosted** (custo: $0) -- Para busca SERP básica e comparação
2. **Perplexity Sonar Low** ($5/1K) -- Para verificar citações em LLMs com busca real
3. **Gemini 2.5 Flash-Lite Batch** ($0.05/MTok input) -- Para classificação barata
4. **Brave Search** ($5/1K, com $5 grátis/mês) -- Como fonte adicional de SERP

**Custo estimado para 100 queries de monitoramento/dia:**
- 30 dias x 100 queries = 3.000 queries/mês
- Perplexity Sonar Low: 3.000 x $0.006 = **$18/mês**
- Classificação via Gemini Flash-Lite Batch: ~**$0.50/mês**
- SearXNG: **$0/mês**
- **Total estimado: ~$18.50/mês**

---

## 6. Estratégias de Rate Limit e Controle de Orçamento

### 6.1. Token Budget por Execução

```python
class TokenBudget:
    def __init__(self, max_input_tokens=50000, max_output_tokens=10000, max_cost_usd=1.0):
        self.max_input = max_input_tokens
        self.max_output = max_output_tokens
        self.max_cost = max_cost_usd
        self.used_input = 0
        self.used_output = 0
        self.cost = 0.0

    def can_proceed(self, estimated_input, estimated_output, price_per_mtok_in, price_per_mtok_out):
        est_cost = (estimated_input * price_per_mtok_in + estimated_output * price_per_mtok_out) / 1_000_000
        return (self.used_input + estimated_input <= self.max_input and
                self.used_output + estimated_output <= self.max_output and
                self.cost + est_cost <= self.max_cost)
```

### 6.2. Exponential Backoff com Jitter

```python
import time, random

def call_with_backoff(fn, max_retries=5):
    for attempt in range(max_retries):
        try:
            return fn()
        except RateLimitError:
            delay = min(60, (2 ** attempt) + random.uniform(0, 1))
            time.sleep(delay)
    raise Exception("Max retries exceeded")
```

### 6.3. Cache Local com SHA-256

```python
import hashlib, json

_cache = {}

def cached_query(prompt, model, ttl_seconds=300):
    key = hashlib.sha256(f"{model}:{prompt}".encode()).hexdigest()
    if key in _cache and (time.time() - _cache[key]["ts"]) < ttl_seconds:
        return _cache[key]["result"]  # Economia: 100% (zero API calls)
    result = api_call(prompt, model)
    _cache[key] = {"result": result, "ts": time.time()}
    return result
```

**Economia estimada de cache local:** 20-40% do orçamento total (prompts repetitivos como system prompts, FAQs, queries idênticas).

---

## 7. Resumo: Stack Otimizado para Monitoramento de Citações de Fintechs

| Camada | Ferramenta | Custo | Função |
|--------|-----------|-------|--------|
| Busca SERP | SearXNG (self-hosted) | $0 | Comparação de rankings |
| Busca LLM | Perplexity Sonar (Low) | $5/1K req + tokens | Citações reais de LLMs |
| Classificação | GPT-5 nano ou Gemini 2.5 Flash-Lite | $0.05-0.10/MTok | Analisar se entidade fintech foi mencionada |
| Batch Processing | Anthropic Batch ou OpenAI Batch | 50% off | Queries não-urgentes |
| Cache | Prompt caching + cache local SHA-256 | 90% off em re-queries | Evitar chamadas repetidas |
| Rate Control | Token budget + exponential backoff | -- | Proteção de orçamento |

**Custo operacional estimado:** $15-25/mês para ~3.000 queries de monitoramento.

---

## Fontes

- [OpenAI API Pricing](https://developers.openai.com/api/docs/pricing)
- [OpenAI Batch API Guide](https://developers.openai.com/api/docs/guides/batch)
- [Anthropic Claude Pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- [Anthropic Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- [Anthropic Message Batches API](https://claude.com/blog/message-batches-api)
- [Google Gemini API Pricing](https://ai.google.dev/gemini-api/docs/pricing)
- [Google Grounding with Search](https://ai.google.dev/gemini-api/docs/google-search)
- [Perplexity Sonar Pricing](https://docs.perplexity.ai/docs/getting-started/pricing)
- [Perplexity Search Context Size Guide](https://docs.perplexity.ai/guides/search-context-size-guide)
- [Perplexity Improved Sonar Models](https://www.perplexity.ai/hub/blog/new-sonar-search-modes-outperform-openai-in-cost-and-performance)
- [Brave Search API](https://brave.com/search/api/)
- [Tavily Pricing](https://docs.tavily.com/documentation/api-credits)
- [TOON vs JSON - Token Optimization](https://www.tensorlake.ai/blog-posts/toon-vs-json)
- [LLM Structured Output 2026](https://dev.to/pockit_tools/llm-structured-output-in-2026-stop-parsing-json-with-regex-and-do-it-right-34pk)
- [OpenAI Prompt Caching](https://openai.com/index/api-prompt-caching/)
- [LLM Rate Limiting Strategies](https://oneuptime.com/blog/post/2026-01-30-llm-rate-limiting/view)
- [LLM-as-Judge Guide 2026](https://labelyourdata.com/articles/llm-as-a-judge)
- [Token Reduction Strategies](https://www.glukhov.org/post/2025/11/cost-effective-llm-applications)
- [SERP API Comparison 2025](https://dev.to/ritza/best-serp-api-comparison-2025-serpapi-vs-exa-vs-tavily-vs-scrapingdog-vs-scrapingbee-2jci)
- [GPT-5 Nano Model](https://platform.openai.com/docs/models/gpt-5-nano)
- [AI API Pricing Comparison 2026](https://intuitionlabs.ai/articles/ai-api-pricing-comparison-grok-gemini-openai-claude)
- [OpenAI Batch API HackerNews Discussion](https://news.ycombinator.com/item?id=40043845)
- [Save 90% on Claude API Costs - DEV.to](https://dev.to/stklen/how-to-save-90-on-claude-api-costs-3-official-techniques-3d4n)
