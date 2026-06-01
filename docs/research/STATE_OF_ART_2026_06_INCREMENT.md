# Estado da arte GEO — incremento de junho de 2026

**Escopo:** documento de *related work* / *discussion* para o Paper 5 (janela confirmatória v2). Consolida o cânone GEO de 2026 que sustenta a interpretação dos resultados longitudinais — **sem alterar a mecânica de coleta**. Nenhum parâmetro de coleta, query, cohort, schema ou workflow é tocado por este documento; ele é puramente bibliográfico/conceitual.

**Data:** 2026-06-01 · **Autor:** Alexandre Caramaschi · **Status:** vivo (incrementa `state-of-art-2026-05/`).

> Como usar: este arquivo alimenta as seções *Related Work* e *Discussion* do paper. Os números de lift e prevalência abaixo são da literatura citada, não do nosso dataset — o nosso dataset os **testa** longitudinalmente em entidades brasileiras reais.

---

## 1. Métricas canônicas de visibilidade: GEO Score e GEU Score

**Fonte primária:** AutoGEO (ICLR 2026, CMU; Liu/Xu et al.).

- **GEO Score (visibilidade):** função de (i) posição do documento na resposta gerada, (ii) número de tokens atribuídos à fonte e (iii) frequência de citação ao longo de um portfólio de prompts.
- **GEU Score (utilidade):** função de (i) qualidade/precisão da citação, (ii) cobertura dos *keypoints* da resposta e (iii) coerência global da resposta gerada.
- **Princípio de tensão:** maximizar GEO **sem degradar** GEU. Otimizações que inflam visibilidade às custas da utilidade são insustentáveis — os engines acabam penalizando.
- **Método empírico (sem GPU, API-only):** extração de regras específicas por engine comparando pares vencedor/perdedor (`argmax |Vis(d_i) − Vis(d_j)|` → explainer → extractor → merger → filter). Lift reportado de **+50% a +82%** no GEO Score; **+46,4%** adicional com reescrita multi-turno (*AgenticGEO*, mar-2026). Overlap de regras entre engines: Gemini–Claude 84,2%, Gemini–GPT 79%.

**Conexão com o nosso estudo:** nossa coleta mede o equivalente observacional do GEO Score (taxa de citação, posição em tercil, atribuição *named* vs *linked*) de forma não-intervencionista e longitudinal — uma contribuição complementar à abordagem intervencionista da AutoGEO.

---

## 2. Alavancas de redação com lift medido (checklist de 12 itens)

**Fonte:** consolidação Princeton (Aggarwal et al.) / GEO-SFE / AutoGEO, sintetizada no cânone interno `landing-page-geo/docs/GEO_CHECKLIST_REDACAO_2026.md`.

| Alavanca | Lift de citação | Mecanismo |
|---|---|---|
| Citação de especialista atribuída (nome+cargo+org) | **+42,6%** | Sinal de autoridade verificável |
| Fontes inline em cada claim | **+40%** (**+115%** em páginas rank 5+) | Rastreabilidade da afirmação |
| Estatística com número específico | **+32,8%** | Densidade factual (15+ dados ≈ +50%) |
| Fluência e coerência lógica | **+28,7%** | Chunkability para RAG |
| Termos técnicos precisos | **+18,5%** | Desambiguação de entidade |
| Seção autossuficiente (heading→claim→evidência) | **+17,3%** | Self-containment para retrieval |
| Answer-first / BLUF (40-60 palavras pós-H2) | **+1,9×** (44,2% das citações nos primeiros 30%) | Posição privilegiada |
| Tabela comparativa com dados | **2,5×** (**4,1×** com dado original) | Formato preferido por extração |
| Unicidade / Information Gain | **4,1×** | Conteúdo sem equivalente no corpus |
| Profundidade (>2.000 palavras) | **3×** | Cobertura de mecanismo causal |
| Frescor (<30 dias) | **3,2×** | *Recency signal* |
| **Keyword stuffing (anti-padrão)** | **−8,7%** | Única técnica com lift negativo comprovado |

**Conexão:** estes lifts são hipóteses falsificáveis. A janela v2 permite verificar quais se sustentam em entidades BR reais ao longo de 90 dias (vs. estudos pontuais).

---

## 3. Deltas conceituais de 2026 (pós Google I/O, 13-15 mai)

1. **"GEO é o novo SEO" → falso.** Posição oficial Google (15-mai-2026): *"For Google Search, optimizing for AEO/GEO continues to be SEO."* SEO permanece o ativo central; GEO é a **camada operacional cross-platform** (ChatGPT, Perplexity, Claude, Copilot).
2. **"Schema = citação" → falso.** Ahrefs (mai-2026): 1.885 URLs com schema vs 4.000 controles → ganho ≈ zero em amplificação. Schema é **higiene semântica e desambiguação**, necessário mas não suficiente. Divergência schema↔conteúdo dispara flag "Spammy Structured Data".
3. **"FAQ rich result garante destaque" → desatualizado.** FAQ rich results encerrados no Google Search em 07-mai-2026; porém `FAQPage` segue como *trust signal* (3,2× mais propensa a entrar em AI Overview — Wellows 2026).
4. **"Redating sem mudança gera lift" → falso.** Google Publisher Center 2026 detecta *fake-fresh*. Cadência canônica: pillar mensal, spoke trimestral, atualização de `dateModified` apenas com delta editorial ≥15% ou ≥1 dado novo verificável.

---

## 4. Conceitos de medição relevantes para a Discussion

- **Citation Drift / Persistence:** 40-60% dos domínios citados mudam por mês (AIO 59,3%; ChatGPT 54,1%; Perplexity 40,5%). Threshold de consenso forte: <20% de drift em D+0/D+14/D+30 sobre 30 prompts representativos. **Implicação direta para o paper:** justifica a janela de 90 dias — medições pontuais capturam ruído transitório, não o sinal estável.
- **Entity Boundary Drift:** consistência de identidade por similaridade de cosseno entre o vetor canônico da entidade e os vetores nas fontes externas. cos θ > 0,95 → persistência ~85% em 90 dias; cos θ < 0,80 → descarte pelo engine. Conecta-se aos nossos decoys fictícios (calibração de FPR).
- **Multi-Source Consensus:** corroboração de claims em ≥3 fontes externas (Wikipedia + Reddit + G2 + papers + gov). Marcas com presença simultânea Wikipedia+Reddit+G2 têm 2,8× mais chance de citação cruzada ChatGPT/Perplexity (Wellows 2026).
- **Answer Capsule:** 72,4% das páginas citadas pelo ChatGPT contêm um parágrafo auto-contido de 120-150 caracteres logo após o heading (Search Engine Land 2026).
- **Parsing por crawler de IA:** crawlers do ChatGPT não executam JS; SSR+schema rendem ~94% de parse vs ~23% em CSR. Reforça por que medimos respostas de APIs (não scraping de SERP renderizada).

---

## 5. Taxonomia de 8 sinais observáveis (operacional)

Espelha `landing-page-geo/src/lib/vertical-geo-canon.ts`. São os sinais auditáveis por entidade que correlacionamos (observacionalmente) com taxa de citação:

1. **Wikidata Qid** — claims P31/P159/P571/P127/P452 + sameAs (CNPJ, ticker, Crunchbase).
2. **Wikipedia EN** — >5k palavras, >30 referências externas.
3. **Schema.org Organization** — sameAs + foundingDate + contactPoint.
4. **Press kit datado** — sala de imprensa com dateModified <90 dias.
5. **llms.txt** — rotas declaradas para agentes não-Google.
6. **ai-policy** — política explícita por bot de IA.
7. **Mídia DA90+** — cobertura tier-1 nos últimos 12 meses.
8. **Recency signals** — sitemap lastmod real + Article dateModified + foundingDate.

Pesos: yes=1, partial=0,5, no=0, unknown=0,25.

---

## 6. O que NÃO muda (barreira de coleta)

Este incremento é **exclusivamente documental**. Permanecem congelados e fora de qualquer alteração até o fechamento da janela (dia 90, 21-jul-2026):

- Pipeline de coleta (`src/collectors/*`, `src/cli.py`), `config.py`/`config_v2.py` (cohort, battery de queries, decoys).
- Schema do banco (`data/papers.db`, migrations) e cache SHA-256.
- Workflows de coleta/sync (`.github/workflows/daily-collect.yml` e correlatos).
- Geradores de saída (`scripts/generate_dashboard_json.py`, `scripts/compute_weekly_deltas.py`) — lógica de cálculo intocada.
- Parâmetros de reprodutibilidade: temperature=0, seeds fixos, retry 2×, NER v2.

A reprodutibilidade bit-a-bit do dataset rumo ao paper peer-reviewed é preservada.

---

## Referências canônicas

- AutoGEO — *Generative Engine Optimization via rule extraction* (ICLR 2026, CMU).
- Aggarwal et al. — *GEO: Generative Engine Optimization* (Princeton).
- Ahrefs — *Schema markup study* (mai-2026).
- Wellows — *AI citation cross-source analysis* (2026).
- Search Engine Land — *Answer Capsule prevalence* (2026).
- Google I/O 2026 — declaração oficial sobre AEO/GEO (15-mai-2026).
- Cânone interno: `landing-page-geo/docs/GEO_INCREMENT_FONTES_EXTERNAS_20260531.md`, `GEO_CHECKLIST_REDACAO_2026.md`, `GEO_50_CONCEITOS_CANONICAL.md`, `GEO_OPERATING_SYSTEM.md`.
- Consolidação anterior: `docs/research/state-of-art-2026-05/GEO_STATE_OF_ART_2026_05_MASTER.md`.
