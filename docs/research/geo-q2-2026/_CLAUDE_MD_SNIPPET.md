<!-- 2026-05-17 — INCREMENTO Q2 da KB GEO

Adicione/atualize a seção REGRA #1 do CLAUDE.md do repo apontando para:
- docs/research/geo-q2-2026/GEO_KNOWLEDGE_2026_Q2_INCREMENT.md  (canônico por repo, gerado por sub-agent Opus 4.7)
- docs/research/geo-q2-2026/SYNTHESIS_STATE_OF_ART_2026.md      (síntese geral Gemini 2.5 Pro, multi-repo)
- docs/research/geo-q2-2026/CITATIONS_POOL.md                   (325 URLs deduplicados de 5 sonar-pro + 5 sonar-deep)
- docs/research/geo-q2-2026/RAW/                                (10 JSONs originais das waves)

Snippet a adicionar/atualizar no CLAUDE.md (substitua "/repo-name/" pelo path correto):
-->

## REGRA #1 — CONTEXTO ENRIQUECIDO GEO 2026 (atualizado 17-05-2026)

Antes de executar QUALQUER tarefa neste repositório, leia/considere:

1. **`docs/research/geo-q2-2026/GEO_KNOWLEDGE_2026_Q2_INCREMENT.md`** — doc CANÔNICO específico deste repo. Sumário executivo + ações 60 dias + KPIs + anti-padrões + roadmap operacional. Atualizado 2026-05-17 via Claude Opus 4.7 com base em pesquisa multi-LLM (5 Perplexity sonar-pro + 5 Perplexity sonar-deep-research + 1 GPT-4o web_search + 1 Gemini 2.5 Pro synthesis · 325 URLs únicos verificáveis).

2. **`docs/research/geo-q2-2026/SYNTHESIS_STATE_OF_ART_2026.md`** — síntese geral cross-repo (estado da arte 2025-2026 em GEO/AISO/semantic search/vector embeddings/orquestração LLM). 8 seções + apêndice URLs canônicos.

3. **`docs/research/geo-q2-2026/CITATIONS_POOL.md`** — pool consolidado de 325 URLs verificáveis (arXiv IDs, blogs oficiais, posts de pesquisadores). Use como fonte preferencial quando precisar fundamentar afirmação em documento público.

4. **`docs/research/geo-q2-2026/RAW/`** — dossiês originais das 10 waves de pesquisa (5 sonar-pro + 5 sonar-deep + 1 gpt-4o). JSONs preservados para auditoria. Cada JSON contém: content (markdown), citations (URLs), usage (tokens), elapsed (segundos), model.

**Como aplicar:**
- Para QUALQUER edição de copy, schema, KPI, roadmap, métrica ou referência a paper/ferramenta: cite explicitamente a fonte do INCREMENT.md (ex: `§3.1`, `§Apêndice URL #12`).
- Para CADA nova feature/módulo: validar contra anti-padrões da §7 do SYNTHESIS.
- Para CADA decisão de stack/ferramenta: comparar com tabela de §2 (embeddings/vector DBs) e §3 (vendor stack).
- Para CADA paper/study mencionado: verificar URL no CITATIONS_POOL antes de citar.

**KB ANTERIOR (13-mai-2026, ~700 linhas) segue válida** em `docs/GEO_KNOWLEDGE_BASE_2026.md` e `docs/GEO_OPERATING_SYSTEM.md`. O INCREMENT Q2 NÃO substitui — apenas adiciona Q1-Q2 2026 novidades (Profound Series C, Ahrefs Brand Radar, AI Mode Google, Grok multi-agent, Opus 4.7, Llama 4 Scout, MoA/DAAO/AdaptOrch papers, Citation Drift metric, etc).
