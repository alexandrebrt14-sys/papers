# Ingestão de papers GEO/AEO — Wave Junho 2026

> **Data:** 07-jun-2026 · **Escopo:** entradas de *Related Work / Discussion* para o Paper 5 (janela confirmatória v2). Os papers abaixo foram catalogados conforme a **REGRA #2** (tagueamento obrigatório contra os 50 conceitos canônicos) e conectados ao schema SQLite via **Migration 0009** (`citations.selection_status`/`absorption_status`/`failure_type`, `daily_snapshots.citation_selection_rate`/`citation_absorption_rate`/`semantic_entropy_drift`).
> **Verificação:** IDs marcados ✓ confirmados via WebFetch em 07-jun-2026. Os demais ficam "a confirmar na ingestão" (LLMs alucinam arXiv IDs — validar `arxiv.org/abs/<ID>` antes de citar em preprint).
> **Convenção de tags:** cada paper é anotado contra os Conceitos **11** (Answer capsules), **13** (Schema.org), **15** (Clareza de entidade), **21** (Referências externas), **22** (Autoria), **24** (Citabilidade GEO), **25** (Recuperabilidade generativa), **30** (llms.txt) — indicando o que **cobre**, o que **ignora** e o que **desafia**.

---

## 1. GEO: How to Dominate AI Search — arXiv:2509.08919 (Chen et al., cs.IR, 2025)

**Status:** já no cânone (KB/V3). Reforçado aqui como base do **share of model** e do **big brand bias**.

- **Método:** consultas idênticas em Google vs motores generativos; mede sobreposição de domínios citados e taxa de citação por grupo de autoridade.
- **Achados-âncora:** viés a favor de *earned media*; big brand bias mais intenso que no Google; share of model tende a ser **concentrado**.
- **Tags 50 conceitos:** cobre **24** (Citabilidade GEO), **21** (Referências externas — earned media como prova), **15** (Clareza de entidade). Ignora **13/30**. Desafia a suficiência de SEO on-page isolado.
- **Conexão com o schema:** alimenta a métrica observacional de taxa de citação (`citations.cited` + `position` + `attribution`).

## 2. AI Answer Engine Citation Behavior: GEO-16 Framework — arXiv:2509.10762 (cs.AI, 2025)

**Status:** ingerir como **rubrica aberta de auditoria on-page** e variável de controle.

- **Método:** 70 prompts industriais → Brave + Google AIO + Perplexity → 1.702 citações → 1.100 URLs auditadas pelos 16 pilares → **GEO score G** (0-1).
- **Achado-âncora:** qualidade on-page é forte preditor de citação **independente da autoridade de domínio**. Pilares de maior peso: **Metadata & Freshness**, **Semantic HTML**, **Structured Data**.
- **Tags 50 conceitos:** cobre **13** (Schema.org — JSON-LD Article/TechArticle/FAQPage com `datePublished`/`dateModified`/`author`/`breadcrumb`), **22** (Autoria), **25** (Recuperabilidade generativa), **11** (Answer capsules, via seções de resumo). Toca **15**. Ignora **30** (llms.txt). 
- **Conexão com o schema:** GEO score G entra como **variável de controle** correlacionável com `citations.cited`. Ponte direta entre §5 da wave e o desenho estatístico do Paper 5.
- **Hipótese testável (PT-BR):** H) páginas com GEO score G alto têm taxa de citação maior **mesmo controlando por autoridade de domínio**, em entidades brasileiras reais — não há replicação PT-BR.

## 3. What Gets Cited: Competitive GEO in AI Answer Engines — arXiv:2605.25517 ✓ (Vishwakarma, Kumar, Jamidar, 25-mai-2026)

**Status:** ingerir como fonte dos **fatores-gatekeeper**.

- **Método:** **252 mil experimentos de RAG pareado** sobre 6 LLMs, isolando que característica faz o modelo citar uma fonte em vez de outra.
- **Achado-âncora:** existem **fatores-gatekeeper** (recência, presença de preço, match estrito de tópico) que praticamente anulam a chance de citação quando violados.
- **Tags 50 conceitos:** cobre **24** (Citabilidade GEO), **25** (Recuperabilidade generativa), **15** (Clareza/match de tópico). Toca **11**. Ignora **13/22/30**. Desafia a ideia de que "mais conteúdo" ou "mais autoridade" basta — fatores editoriais objetivos são gate.
- **Hipóteses testáveis (PT-BR), falsificáveis no dataset longitudinal:**
  - H1) entidades sem `dateModified` recente (>12 meses) têm taxa de citação significativamente menor (gatekeeper de recência).
  - H2) queries comerciais/transacionais sem presença de preço explícito na página reduzem citação.
  - H3) match estrito de tópico (entidade ↔ query) domina sobre profundidade de domínio.

## 4. EcoGEO: Trajectory-Aware Evidence Ecosystems for Web-Enabled LLM Search Agents — arXiv:2605.12887 ✓ (Ye, Mao, Guan, Tian, 13-mai-2026)

**Status:** ingerir como mudança de **unidade de análise** (página → ecossistema/trajetória).

- **Tese:** otimizar páginas isoladas é insuficiente quando o motor é um **agente de navegação** que executa múltiplas consultas e constrói a resposta a partir de um ecossistema de evidências. Propõe otimização de **trajetória** — coordenar páginas interligadas para moldar quais o agente visita e em que ordem.
- **Tags 50 conceitos:** cobre **21** (Referências externas/ecossistema), **25** (Recuperabilidade generativa), **15** (Clareza de entidade entre páginas). Ignora **13/22/30**. Desafia a métrica página-a-página.
- **Conexão com o schema:** sugere campo futuro de "trajetória" (sequência de fontes visitadas); por ora, `sources_json` já registra o conjunto de fontes por resposta — base para análise de ecossistema.

## 5. GEO-Bench: Benchmarking Ranking Manipulation in Generative Engines — arXiv ID a confirmar na ingestão (2026)

**Status:** ingerir como referência do eixo **manipulação vs otimização legítima**.

- **Método:** ataques de manipulação de ranking (caixa-preta e gradiente) + estratégias *white-hat*, num protocolo unificado sobre rankeador aberto baseado em Llama-3.1-8B-Instruct.
- **Tags 50 conceitos:** toca **24/25**; relevante para o eixo de **anti-padrões** (pseudo-GEO/manipulação). Desafia a fronteira entre GEO legítimo e gaming.
- **Cautela:** ID não verificado — confirmar antes de citar em preprint.

## 6. From Citation Selection to Citation Absorption — arXiv:2604.25707 (Zhang, He, Yao, 2026)

**Status:** já ingerido na Wave Maio; aqui **conectado ao schema** via Migration 0009.

- **Dataset:** `geo-citation-lab` — 602 prompts, 72 features por citação, >21k citações na camada de busca, >23k registros de atributos, ~18k páginas.
- **Achado-âncora:** seleção ≠ absorção. ChatGPT cita **menos** fontes porém com **influência maior** por página; Perplexity/Google citam mais com influência distribuída. Páginas longas, estruturadas, semanticamente alinhadas e densas em evidência extraível têm maior absorção.
- **Mapeamento direto no schema (Migration 0009):**
  - `citations.selection_status` = a fonte foi selecionada para o source set (**CSR** por observação).
  - `citations.absorption_status` = a fonte selecionada influenciou o texto final (**CAR** por observação).
  - `daily_snapshots.citation_selection_rate` / `citation_absorption_rate` = agregados diários por módulo/vertical.
- **Tags 50 conceitos:** cobre **24** (Citabilidade GEO), **25** (Recuperabilidade generativa), **11** (Answer capsules/evidência extraível), **15**. Ignora **30**. Desafia a métrica "ser citado" como objetivo final.
- **Hipóteses testáveis (do contrato Wave Maio §, agora instrumentável):**
  - H1) verticais YMYL (saúde, finanças) têm **CAR/CSR mais baixo** que verticais não-YMYL.
  - H2) presença de `ClaimReview` + `reviewedBy` aumenta **CAR independente de CSR**.

---

## 7. Taxonomia de falha de citação (failure_type) — arXiv:2603.09296

`citations.failure_type` (enum, NULL = sem falha) classifica por que um prompt **não** retornou a citação esperada:

| Valor | Significado |
|---|---|
| `broken-fetch` | a fonte não pôde ser buscada (erro de rede/HTTP) |
| `parsing-failure` | a fonte foi buscada mas não pôde ser parseada |
| `retrieval-miss` | a fonte não entrou no retrieval inicial |
| `summarization-collapse` | a fonte foi recuperada mas colapsou na sumarização |
| `attribution-drop` | a fonte influenciou a resposta mas perdeu a atribuição |
| `hallucinated-source` | citação fabricada (cf. GhostCite, 14-95%) |
| `blocked-by-robots` | a fonte foi bloqueada por robots/crawl policy |

Permite report mensal direcional (ex.: "X% das falhas de coleta são `parsing-failure`"). Implementação do classificador (`src/collectors/failure_classifier.py`) fica como próximo passo — este doc + o schema preparam o terreno.

---

## 8. Estado de implementação (07-jun-2026)

| Item | Status |
|---|---|
| Schema `citations`: `selection_status`, `absorption_status`, `failure_type` | ✅ `schema.sql` + Migration 0009 |
| Schema `daily_snapshots`: `citation_selection_rate`, `citation_absorption_rate`, `semantic_entropy_drift` | ✅ `schema.sql` + Migration 0009 |
| Migration standalone `src/db/migrate_0009_citation_absorption.py` (idempotente) | ✅ aplicada ao `data/papers.db` |
| Método inline `_migrate_add_citation_absorption_columns()` em `client.py` | ✅ na cadeia de migrations |
| Testes `tests/test_migration_0009.py` (fresh/legacy/idempotência/enum) | ✅ 4 passed (suíte total 208 verde) |
| Catálogo dos papers tagueado (REGRA #2) | ✅ este doc |
| Popular `selection_status`/`absorption_status` na coleta (`citation_tracker.py` + `insert_citations`) | ✅ via `failure_classifier.derive_citation_status` |
| `src/collectors/failure_classifier.py` (taxonomia de 7 tipos + derivação CSR/CAR) | ✅ + `tests/test_failure_classifier.py` (9 testes) |
| **PENDENTE:** confirmar arXiv ID do GEO-Bench | ⏳ |
| **PENDENTE:** detectar `summarization-collapse` / `retrieval-miss` com ground-truth de expectativa por query | ⏳ próximo ciclo |

**Como funciona a derivação (observacional, proxies — ver docstrings):**
- `absorption_status` = 1 se a entidade foi citada no texto da resposta (camada de geração).
- `selection_status` = 1 se o slug da entidade aparece em alguma URL do source set (camada de busca).
- `failure_type`: `hallucinated-source` (entidade fictícia citada), `attribution-drop` (absorvida sem fonte), `broken-fetch`/`blocked-by-robots`/`parsing-failure` (sinais de transporte/parsing), `retrieval-miss` (esperada mas ausente). `NULL` quando não há falha.
- Agregar para as taxas `daily_snapshots.citation_selection_rate`/`citation_absorption_rate` é o passo de persistência diária (consumir `AVG(selection_status)`/`AVG(absorption_status)` por dia/módulo/vertical).
