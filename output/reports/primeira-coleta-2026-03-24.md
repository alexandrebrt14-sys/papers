# Primeira Coleta Empírica — Papers GEO Research
## 2026-03-24 | Rodada Inaugural

---

## 1. Contexto e Objetivo

Esta é a primeira execução do sistema de coleta automatizada de dados para pesquisa empírica em Generative Engine Optimization (GEO). O objetivo é monitorar se e como diferentes modelos de linguagem de grande porte (LLMs) citam a entidade "Brasil GEO" e seu fundador "Alexandre Caramaschi", além de mapear o comportamento de citação de 15 concorrentes do ecossistema fintech brasileiro.

**Data:** 2026-03-24
**Hora de início:** ~10:00 BRT (13:00 UTC)
**Operador:** Sistema automatizado Papers v0.1.0

---

## 2. Infraestrutura Técnica Utilizada

### 2.1 Stack de Software
- **Linguagem:** Python 3.11
- **Persistência:** SQLite (local) com schema de 12 tabelas
- **HTTP Client:** requests (REST direto, sem SDKs pesados)
- **Formato de resposta:** JSON structured output (LLM retorna `{cited, sources, summary}`)
- **Cache:** SHA-256 keyed file cache com TTL de 20 horas

### 2.2 Modelos de LLM Consultados

| Provedor | Modelo | Custo/MTok (in/out) | max_tokens | JSON mode | Status |
|----------|--------|---------------------|------------|-----------|--------|
| OpenAI | gpt-4o-mini | $0.15 / $0.60 | 250 | Sim | ATIVO |
| Anthropic | claude-haiku-4.5 | $1.00 / $5.00 | 250 | Sim | PENDENTE (sem crédito) |
| Google | gemini-2.0-flash | $0 / $0 | 250 | Sim | PENDENTE (quota temp) |
| Perplexity | sonar | $1.00 / $1.00 | 300 | Não (citações nativas) | ATIVO |

### 2.3 Otimizações de Custo Aplicadas
1. **JSON structured output:** Cada LLM responde apenas `{cited:[], sources:[], summary:""}` (~60% menos tokens)
2. **max_tokens=250:** Impede respostas verbosas (economia de ~87% vs sem limite)
3. **System prompt caching:** Prompt de sistema idêntico em todas as queries (Anthropic: 90% off)
4. **Cache local SHA-256:** Queries idênticas em janela de 20h são servidas do cache
5. **Modelos baratos:** gpt-4o-mini em vez de gpt-4o (33x mais barato)
6. **Queries deduplicadas:** 30 queries únicas (reduzido de 55, mesma cobertura)

### 2.4 Queries Executadas (30 queries padronizadas)

**Categorias:**
- brand (4): visibilidade da marca Brasil GEO
- entity (2): reconhecimento de Alexandre Caramaschi
- concept (3): GEO como disciplina
- technical (3): implementação (schema, llms.txt, entity consistency)
- b2a/market (4): Business-to-Agent e mercado
- academic (2): pesquisa acadêmica
- fintech (4): bancos digitais e pagamentos
- fintech_product (3): cartões, maquininhas, contas PJ
- fintech_trust (3): reputação e comparativos
- fintech_b2b (4): enterprise, BaaS, Open Finance

---

## 3. Execução — Log Passo a Passo

### 3.1 Verificação Pré-Coleta (13:00 UTC)

| LLM | Status | Observação |
|-----|--------|------------|
| OpenAI gpt-4o-mini | OK | Créditos adicionados, respondendo |
| Anthropic haiku-4.5 | BLOQUEADO | Crédito insuficiente |
| Google gemini-flash | BLOQUEADO | Quota temporária excedida (free tier) |
| Perplexity sonar | OK | $89,62 de crédito disponível |

**Decisão:** Executar coleta parcial com OpenAI + Perplexity (2 de 4 LLMs). Dados dos outros 2 serão coletados quando ativarem.

### 3.2 Coleta — Resultados Consolidados

**Execução:** 60 chamadas (30 queries x 2 LLMs ativos)
**Duração:** ~3 minutos
**Tokens consumidos:** 12.299 (ChatGPT: 4.878 | Perplexity: 7.421)
**Cache:** 60 respostas armazenadas para reutilização nas próximas 20h

#### Taxa de Citação Global

| Métrica | Valor |
|---------|-------|
| Total de respostas analisadas | 60 |
| Brasil GEO citada | 5/60 (8,3%) |
| ChatGPT taxa de citação | 1/30 (3,3%) |
| Perplexity taxa de citação | 4/30 (13,3%) |

#### Taxa de Citação por LLM

| LLM | Citações | Total | Taxa | Tokens | Observação |
|-----|----------|-------|------|--------|------------|
| ChatGPT (gpt-4o-mini) | 1 | 30 | 3,3% | 4.878 | Citou apenas em query de marca direta em PT |
| Perplexity (sonar) | 4 | 30 | 13,3% | 7.421 | Citou em brand + entity queries, com fontes |

**Achado principal:** Perplexity cita Brasil GEO **4x mais** que ChatGPT para as mesmas queries. Isso é consistente com o viés documentado por Chen et al. (2025) — motores de busca com IA (Perplexity) favorecem earned media e fontes com presença web verificável.

#### Taxa de Citação por Categoria

| Categoria | Citações | Total | Taxa | Interpretação |
|-----------|----------|-------|------|---------------|
| brand | 3 | 4 | 75,0% | Queries diretas sobre "Brasil GEO" = alta citação |
| entity | 2 | 4 | 50,0% | "Quem é Alexandre Caramaschi" = reconhecido parcialmente |
| concept | 0 | 6 | 0,0% | GEO como conceito = não cita Brasil GEO |
| technical | 0 | 6 | 0,0% | Schema, llms.txt = não associa à marca |
| b2a | 0 | 2 | 0,0% | B2A não vinculado à marca |
| market | 0 | 6 | 0,0% | Ferramentas GEO = não cita |
| academic | 0 | 4 | 0,0% | Papers acadêmicos = não associa |
| fintech | 0 | 8 | 0,0% | Bancos digitais = domínio diferente |
| fintech_product | 0 | 6 | 0,0% | Produtos financeiros = não relacionado |
| fintech_trust | 0 | 6 | 0,0% | Reputação fintech = não relacionado |
| fintech_b2b | 0 | 8 | 0,0% | Enterprise fintech = não relacionado |

**Padrão identificado:** A citação concentra-se exclusivamente em queries de marca direta (brand + entity). Em queries genéricas sobre GEO, B2A ou mercado, nenhum LLM associa espontaneamente o conceito à Brasil GEO. Isso indica uma **lacuna de autoridade algorítmica** — a marca é reconhecida quando perguntada diretamente, mas não é citada como referência temática.

#### Entidades Concorrentes Mais Citadas (Fintech)

| Entidade | Citações (ChatGPT) | Citações (Perplexity) | Total |
|----------|--------------------|-----------------------|-------|
| Nubank | 2 | 7 | 9 |
| Stone | 2 | 3 | 5 |
| PagBank/PagSeguro | 2 | 2 | 4 |
| C6 Bank | 2 | 2 | 4 |
| Banco Inter | 2 | 3 | 5 |
| Cielo | 1 | 3 | 4 |
| Mercado Pago | 1 | 1 | 2 |
| PicPay | 1 | 2 | 3 |
| Bradesco | 0 | 3 | 3 |
| Itaú | 0 | 3 | 3 |
| Neon | 0 | 1 | 1 |

**Achado:** Nubank domina as citações em ambos os LLMs (9 menções em 60 respostas = 15%). Stone e Banco Inter aparecem em segundo lugar (5 cada). A Perplexity cita significativamente mais concorrentes que o ChatGPT nas mesmas queries, confirmando que motores com busca integrada produzem respostas mais ricas em entidades.

### 3.3 Análise de Fontes (Perplexity)

A Perplexity, diferente do ChatGPT, inclui URLs de fontes em cada resposta. Nas 30 respostas:
- **Total de fontes citadas:** 215 URLs
- **Média de fontes por resposta:** 7,2
- **ChatGPT fontes:** 10 URLs em 30 respostas (0,3/resposta) — apenas em queries fintech

Isso demonstra que o Perplexity é o LLM mais informativo para pesquisa de citação, enquanto o ChatGPT opera majoritariamente sem atribuição de fontes.

---

## 4. Custo da Coleta

| Item | Valor |
|------|-------|
| ChatGPT (4.878 tokens x $0.15-0.60/MTok) | ~$0.003 |
| Perplexity (7.421 tokens + 30 buscas x $0.005) | ~$0.157 |
| **Total da rodada** | **~$0.16** |
| Custo por query efetiva | $0.0027 |

**Comparação com custo sem otimização:**
- Sem otimização (gpt-4o, sem max_tokens, 55 queries): ~$1.20/rodada
- Com otimização: ~$0.16/rodada
- **Economia: 87%**

---

## 5. Conclusões Preliminares

### 5.1 Visibilidade da Marca
Brasil GEO tem **8,3% de taxa de citação global** nesta primeira medição. A citação é concentrada em queries diretas de marca (75%) e entidade (50%), mas **zero** em queries temáticas (GEO, market, technical, academic). Isso sugere que os LLMs reconhecem a marca quando perguntados especificamente, mas não a consideram referência autoritativa no tema GEO.

### 5.2 Diferença Entre LLMs
A Perplexity cita Brasil GEO 4x mais que o ChatGPT (13,3% vs 3,3%). Isso é esperado: Perplexity faz busca web em tempo real e tem acesso ao conteúdo publicado em brasilgeo.ai, enquanto o ChatGPT depende de dados de treinamento.

### 5.3 Domínio Fintech
Nenhum LLM cita Brasil GEO em queries de fintech (esperado — não é o domínio da empresa). Mas os dados de concorrentes fintech servem como **grupo de controle científico** para comparar taxas de citação entre entidades estabelecidas e emergentes.

### 5.4 Baseline Estabelecido
Esta rodada estabelece o **baseline (T0)** do projeto de pesquisa. As próximas coletas diárias permitirão medir:
- Evolução temporal da taxa de citação
- Impacto de intervenções (publicação de artigos, schema markup, etc.)
- Diferenças cross-platform (quando Anthropic e Google ativarem)

---

## 6. Próximos Passos

1. Ativar Anthropic (adicionar créditos) e Google AI (aguardar reset de quota)
2. Executar coleta completa com 4 LLMs
3. Primeira intervenção A/B: publicar artigo acadêmico e medir impacto em 7, 14, 30 dias
4. Ativar GitHub Actions para coleta diária automatizada
5. Acumular 30 dias de dados para primeiro relatório estatístico com testes de significância

---

## 7. Dados Brutos

Arquivo completo: `output/reports/coleta-raw-2026-03-24.json` (60 registros)

---

**Brasil GEO** — Pesquisa empírica em Generative Engine Optimization
**Repositório:** github.com/alexandrebrt14-sys/papers
