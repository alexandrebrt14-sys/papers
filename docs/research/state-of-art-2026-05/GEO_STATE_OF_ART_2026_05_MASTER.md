# GEO State of the Art · 20-mai-2026 · Brasil GEO Master Index

> **Versão**: 1.0 · 20-mai-2026
> **Owner**: Brasil GEO (Alexandre Caramaschi — CEO Brasil GEO, ex-CMO Semantix (Nasdaq), conselheiro estratégico de IA da Nuvini (Nasdaq: NVNI), cofundador AI Brasil).
> **Repositórios cobertos**: [landing-page-geo](https://github.com/alexandrebrt14-sys/landing-page-geo) · [papers](https://github.com/alexandrebrt14-sys/papers) · [curso-factory](https://github.com/alexandrebrt14-sys/curso-factory).
> **Método**: 6 sub-agents Opus paralelos, 30+ chamadas Perplexity sonar-deep-research, ~50 WebFetches em fontes primárias, ~47.300 palavras de pesquisa densa, custo total ~US$ 11 em Perplexity + Opus.
>
> **Como usar este documento**: anexe-o (e/ou os 6 tracks que ele consolida) como contexto enriquecido em qualquer prompt operacional GEO/SEO nos 3 repos. Cite `§X.Y` ao tomar decisões. Substitui (não acumula) o snapshot anterior `curso-factory/docs/GEO_KNOWLEDGE_BASE_2026_V2.md` no que diz respeito a estado da arte abr-mai 2026. Mantém retro-compatibilidade com `GEO_KNOWLEDGE_BASE_2026.md` (V1, teoria), `GEO_OPERATING_SYSTEM.md` (playbook semanal), `GEO_50_CONCEITOS_CANONICAL.md` (taxonomia) e `SEO_GEO_INCREMENT_20260520.md` (pós Google I/O 2026, 15-mai).
>
> Os 6 tracks completos estão em `docs/research/state-of-art-2026-05/` em cada repo (cópias idênticas) e em `C:/Sandyboxclaude/_geo-research-20260520-evening/` (origem).

---

## Índice

0. Como usar este documento
1. Sumário executivo — 12 conclusões cross-track
2. O que mudou em relação à V2 e ao SEO_GEO_INCREMENT 20-mai-2026
3. Mapa dos 6 tracks
4. Playbook integrado por repositório
5. Cross-references entre tracks
6. Roadmap operacional 12 semanas (jun-ago 2026)
7. Anti-padrões consolidados 2026
8. Apêndice — arquivos e custo

---

## 0. Como usar este documento

Este master index existe para resolver um problema operacional: quando você (ou um sub-agent) está prestes a tomar uma decisão GEO concreta — escrever um artigo, escolher um vector DB, configurar `robots.txt`, definir uma métrica, comparar vendors —, qual é o snapshot canônico de **estado da arte** que serve como contexto?

- Para **decisões editoriais e de conteúdo** (qual fórmula de citação usar, qual densidade, qual estrutura de página): combine `§1` deste doc + Track E (§Parte 1 e §Sumário operacional Top 10).
- Para **decisões de arquitetura RAG, embeddings, vector DB**: combine `§1` + Track C inteiro + §4 por repo.
- Para **decisões de medição, KPI, dashboard**: combine `§1` + Track B + Track A papers de measurement.
- Para **decisões sobre vendors, contratos, billing**: combine §1 + Track D.
- Para **decisões sobre `robots.txt`, llms.txt, MCP, schema**: combine §1 + Track F + Track E §1.3-1.4.
- Para **decisões sobre o que escrever em papers acadêmicos**: combine §1 + Track A (18 papers Q2 2026 fichados).

---

## 1. Sumário executivo — 12 conclusões cross-track

As 12 conclusões abaixo foram extraídas dos 6 tracks via síntese semântica e cruzam pelo menos 2 tracks cada. Ordem: por impacto operacional descendente.

1. **A unidade de otimização GEO migrou do token para a feature estrutural.** [Track A §1, FeatGEO arXiv:2604.19113] O paper de Liu & Xu (21-abr-2026) mostra que GEO em nível de feature (densidade de bullets, blocos canônicos, ratio de citações por parágrafo) bate optimization lexical de keyword/frase autoritária. Combinado com Track E §Top-10 ação 4 (semantic unit 134-167 palavras) e Track C §6 (chunking semântico), define-se um novo paradigma de "estrutura otimizada para retrieval" que substitui copy hacks pré-2025.

2. **Citação tem duas dimensões, não uma: selection e absorption.** [Track A §2, Zhang/He/Yao arXiv:2604.25707] ChatGPT cita poucas fontes com peso altíssimo; Perplexity e Google AI Overviews citam muitas com peso médio-baixo. KPI antigo "citation rate" trata os dois como equivalentes — está obsoleto. Substitua por par `(selection_rate, absorption_rate)` em todo tracking (Track B §22 KPIs novos cobre instrumentação).

3. **Visibilidade GEO é distribuição, não número.** [Track A §5, Schulte/Bleeker/Kaufmann arXiv:2604.07585] Medir uma única vez é estatisticamente inútil. Protocolo canônico: 5+ amostras por prompt × modelo × dia. Track B §Framework 2 (Multi-LLM Sampling Wave) operacionaliza com `n_samples` por tier P0/P1/P2 (20-50/10/5) e dois perfis (deterministic T=0 + stochastic T=0.7).

4. **Apenas 38% das citações em AIO vêm do top-10 orgânico (mai-2026), contra 76% em mar-2025.** [Track E §1.2 + Ahrefs] É o "fan-out drift" estrutural: AI Overviews coleta sources de fan-out SERPs paralelos, não só do SERP principal. Implicações: SEO clássico já não suficiente; track a Mention Rate / Citation Rate em paralelo a posição orgânica (Track B §KPIs K-NEW-007 a K-NEW-009).

5. **Schema JSON-LD sozinho não move citações em LLMs.** [Track D §Ahrefs 11-mai-2026 + Track E §1.2] Estudo controlado Ahrefs (1.885 páginas vs 4.000 controles, ago/25-mar/26) mediu -4,6% AIO, +2,4% AI Mode, +2,2% ChatGPT — todos noise estatístico. MAS: schema enriquece Knowledge Graph que melhora organic ranking que aumenta probabilidade de citação. Esta é a **Two-Phase JSON-LD Theory** (SEO_GEO_INCREMENT §3). Schema continua sendo core infrastructure, não AI citation button.

6. **`llms.txt` continua zero correlation com citações em LLMs.** [Track F §3.1 + Track E §3 + SE Ranking 10,13% adoção em 300k domínios] Mueller (Google), Illyes, Sullivan, Splitt todos públicos contra. Anthropic ativamente pede `llms-full.txt` em docs de B2B onde já decidiu visitar — vale **para reduzir custo de ingestão pós-visita**, não para placement. Mantenha llms.txt+llms-full.txt no portal Brasil GEO, mas pare de prometer "GEO escape hatch" a clientes.

7. **MCP (Model Context Protocol) é o padrão emergente "site como ferramenta agentic".** [Track F §2] Lançado Anthropic 25-nov-2024, agora suportado nativamente em Claude, ChatGPT, Cursor, Windsurf, Zed, VS Code. NLWeb endpoint do Microsoft é nativamente MCP server. Recomendação para os 3 repos: expor um MCP server `tools=[get_article, search_articles, list_glossary, get_paper_abstract]` em 12-18 meses. Cria moat: agentes vão preferir sites com MCP exposto a sites que precisam ser scrapeados.

8. **Três crawlers OpenAI distintos exigem decisões separadas.** [Track F §1.1] `GPTBot` (training) ≠ `OAI-SearchBot` (busca) ≠ `ChatGPT-User` (live retrieval). Bloquear training data NÃO bloqueia search citation. Crawl-to-referral ratio Cloudflare jan-2026: OpenAI 1.700:1, Anthropic 73.000:1, Google 14:1. Decisão canônica Brasil GEO: allow OAI-SearchBot/Claude-SearchBot/PerplexityBot/Google-Extended para search; allow {ChatGPT,Claude,Perplexity}-User para retrieval ao vivo; **pay-per-crawl** Cloudflare em GPTBot/ClaudeBot/Bytespider em sites comerciais.

9. **Vendor landscape consolidou em 3 camadas com US$ 192M+ em funding pure-play GEO.** [Track D §1] Pure-play (Profound US$ 96M Série C, Bluefish US$ 43M, Peec US$ 21M, Daydream US$ 15M, Scrunch US$ 15M, AthenaHQ US$ 2,7M, Otterly bootstrapped, Goodie bootstrapped); SEO incumbente que pivotou (Ahrefs Brand Radar US$ 420-740/mês, Semrush AI Toolkit, Surfer AI Tracker desde US$ 49, Frase AI Mode, Clearscope, Writesonic, BrightEdge, Similarweb, Conductor); plataforma (Google AI Mode/AIO, ChatGPT Search, Perplexity, Copilot, Claude). Stack canônico Brasil GEO por tier em §4 deste doc.

10. **Híbrido retrieval (BM25 + dense + reranker cross-encoder) virou padrão de fato.** [Track C §2-3] Anthropic Contextual Retrieval reduz failure rate 49-67% (49% sem rerank, 67% com). Para PT-BR crítico, BGE-M3 self-hosted (MIRACL 69,2 incluindo português) é insuperável em custo. Para multimodal, Cohere embed-v4. Vector DBs: Turbopuffer 10× mais barato que Pinecone para storage (US$ 0,02 vs US$ 0,33/GB/mês); Qdrant binary quantization 32× redução de memória. Aplicação por repo em §4.

11. **Agentic RAG saiu do laboratório para produção em 2026.** [Track C §5 + Track A §15-16] GraphRAG 1.0 Microsoft em abr-2025 (3.0.9 em abr-2026), Self-RAG, CRAG, Adaptive-RAG, RAPTOR, HippoRAG 2 são componentes nativos em LlamaIndex Workflows 1.0 e LangGraph Platform GA. ZenML LLMOps 2025: 57% dos sistemas em produção usam Router+Retriever+Reranker+Reader; GraphRAG já em 21%. Adaptive-RAG router é o padrão dominante.

12. **A faixa SEO ↔ GEO ainda diverge mas tem playbook integrado.** [Track E §Top-10 + SEO_GEO_INCREMENT §2] SEO continua sendo a fundação técnica (indexability, snippet-eligibility, Core Web Vitals, schema como Knowledge Graph driver) — sem isso nada do GEO funciona. GEO é camada operacional adicional cross-platform (medição multi-LLM, prompt portfolio, citation persistence, attribution multi-touch). Reuters Institute 2026 projeta -43% no tráfego search em 3 anos: a transição cita > clique já é estrutural.

---

## 2. O que mudou em relação à V2 e ao SEO_GEO_INCREMENT 20-mai-2026

A V2 (`curso-factory/docs/GEO_KNOWLEDGE_BASE_2026_V2.md`, 17-mai-2026) e o SEO_GEO_INCREMENT (mesma data) cobriram bem: papers Q1 e início Q2 2026 (Aggarwal 2023, Chen 2025, VMAO, IRS, CONSTRUCT, AutoGEO), vendor landscape com Profound/Bluefish/Peec/Daydream/Scrunch/AthenaHQ, 14 KPIs canônicos, timeline updates Google 2026, Google I/O 2026 (15-mai), Two-Phase JSON-LD theory, Princeton GEO playbook, llms.txt zero adoção, NLWeb MCP, bots 14 IA, B2A/ASO inicial.

Este Master Index ADICIONA, sem duplicar:

| Camada | V2/Incremento já cobria | Master Index adiciona (deltas) |
|---|---|---|
| **Papers acadêmicos** | ~10 papers Q1 2026 fundadores | 18 papers Q2 2026 (abr-mai) validados arXiv, incl. FeatGEO, selection/absorption, GEO-SFE, MAGEO, distribuição não-número, AIO SIGIR 2026, GhostCite/CiteAudit/CiteTracer/urlhealth (citation auditing), ResRank, PyRAG, ReaLM-Retrieve, RAGSearch agentic, Causal Memory Intervention, Tabular Chunking |
| **KPIs** | 14 canônicos | +22 KPIs operacionais NOVOS (Citation Persistence Index, Brand Echo Decay, Velocity, Cross-LLM Consistency, Token-Weighted Mention Rate, Snippet vs Full-Text origin, Geo-AI Visibility PT/EN/ES, etc) |
| **Frameworks** | conceituais (Aggarwal táticas, 5 ondas master prompt) | 6 frameworks operacionais end-to-end com etapas, inputs/outputs, custo, cadência: PPL, MLSW, CPDL, MLA, CLCA, GAAD |
| **Vendors** | snapshot fev-mai 2026 | Detalhe completo 17 vendors com pricing WebFetch-validado em 20-mai-2026 + 25 colunas/posts dos top SEO/GEO commentators (abr-mai 2026) |
| **Ranking factors** | Top 10 ações pós-I/O 2026 | Tabela cross-surface 22 sinais × 10 surfaces (AIO, AI Mode, ChatGPT Search, Perplexity, Copilot, Claude Research, You.com, Apple Intelligence, Meta AI, Grok) + sinais [CONFIRMADO]/[TESTADO INDEPENDENTE]/[ESPECULAÇÃO] |
| **RAG/Vector** | menção tangencial | Estado da arte completo: 18 modelos embedding tabelados, retrieval híbrido/SPLADE/ColBERT, 11 vector DBs comparados, agentic RAG patterns, semantic chunking, prompt caching Anthropic |
| **B2A/ASO** | 14 bots básicos | 30+ crawlers catalogados com UA canônico, robots.txt token, IP ranges, rate limit, documentação; MCP completo; 10 templates funcionais (robots.txt, llms.txt v2, mcp.json, ai-policy.json, Schema, MCP server stubs) |

---

## 3. Mapa dos 6 tracks

### Track A — Papers acadêmicos Q2 2026 (GEO/RAG/LLM)
- **Arquivo**: `track-A-papers-q2-2026.md` · 8.475 palavras · 18 papers validados arXiv (Q2 2026) + 11 leads adicionais
- **Pergunta central**: o que mudou em GEO/RAG/citation/agentic acadêmico em abr-mai 2026 que ainda não está na V2?
- **Achados-chave**: par selection/absorption (2604.25707); distribuição não-número (2604.07585); 14-95% citações fabricadas em LLMs (GhostCite 2602.06718); 51,5% queries com AIO (SIGIR 2026 2604.27790); bloquear Google-Extended pune visibilidade AIO; BM25 ainda bate dense embeddings em domínios texto+tabela financeira (2604.01733); ResRank une retrieve+rerank ponta-a-ponta (2604.22180); PyRAG executável (2605.12975).

### Track B — Frameworks operacionais + 22 KPIs novos
- **Arquivo**: `track-B-frameworks-kpis.md` · 7.587 palavras · 6 frameworks + 22 KPIs + reference architecture
- **Pergunta central**: como operacionalizar GEO como engenharia de dados em 2026?
- **Achados-chave**: PPL (Prompt Portfolio Lifecycle), MLSW (Multi-LLM Sampling Wave), CPDL (Citation Persistence & Decay Loop), MLA (Multi-Touch LLM Attribution), CLCA (Cross-LLM Consistency Auditing), GAAD (Geo-AI Visibility & Locale Drift); 22 KPIs com fórmula + unidade + benchmark + instrumentação + anti-padrão; 3 scripts quick-start (Python multi-LLM, bash snapshot, dbt CPI).

### Track C — LLM/Vector/Semantic state of the art
- **Arquivo**: `track-C-llm-vector-stateofart.md` · 7.645 palavras · 18 modelos embedding + 11 vector DBs + 97 URLs primárias
- **Pergunta central**: qual é a stack canônica de retrieval/embedding/vector em mai-2026 para os 3 repos?
- **Achados-chave**: BGE-M3 self-hosted (MIRACL 69,2) é insuperável para PT-BR; embed-v4 Cohere (multimodal, 128k context); Anthropic Contextual Retrieval reduz failure rate 49-67%; Turbopuffer 10× barato que Pinecone; GraphRAG 1.0 Microsoft custou US$ 50-200 ingestão de 1.000 docs vs US$ 5-20 chunking simples; Matryoshka Representation Learning permite truncar dim 3072→256 mantendo 91% qualidade.

### Track D — Vendors GEO + colunas recentes (atualização 20-mai-2026)
- **Arquivo**: `track-D-vendors-columns.md` · 8.126 palavras · 17 vendors + 25 colunas + mapa M&A
- **Pergunta central**: qual é o mercado comercial GEO em mai-2026 e quem está dizendo o quê?
- **Achados-chave**: zero M&A pure-play em jan-mai 2026 (toda consolidação via VC); ChatGPT Search citing fewer sites em mai-2026, top 50 domínios concentram 47% das citações (vs 38% jan-2026) — janela GEO fechando para novos entrantes; estudo Ahrefs 11-mai mostra schema sozinho não move citation; Lily Ray lançou Algorythmic.co solo agency em mai-2026 confirmando categoria que é o positioning de Brasil GEO; Stack Solo Brasil GEO ~US$ 88/mês validado (Otterly Lite + Surfer Discovery + Perplexity API).

### Track E — Ranking factors AI search surfaces (mai-2026)
- **Arquivo**: `track-E-ranking-factors.md` · 6.951 palavras · 10 surfaces × 22 sinais + 146 URLs
- **Pergunta central**: que sinais movem citação em cada surface IA-search em mai-2026?
- **Achados-chave**: Top 10 ações de ROI (indexável-snippet-eligible, citation block nomeado, author entity Wikidata+ORCID+LinkedIn, semantic unit 134-167 palavras BLUF top 150, 15+ entidades Wikidata, FAQPage onde genuíno, robots.txt granular 10+ bots, sitemap lastmod real, dateModified republish editorial, IndexNow imediato); 38% top-10 drift; Bing AI Performance dashboard único oficial dedicado a GEO; 3 crawlers OpenAI distintos; Princeton GEO playbook lifts (Cite Sources +115%, Statistics +41%, Quotation +28%).

### Track F — B2A/ASO/Agent Standards (mai-2026)
- **Arquivo**: `track-F-b2a-aso-agentic.md` · 8.512 palavras · 30+ crawlers + 10 templates canônicos
- **Pergunta central**: como otimizar sites para serem PREFERIDOS por agentes IA em mai-2026?
- **Achados-chave**: 4 camadas de tráfego (humanos, busca clássica, IA training/search, agentic operators); ChatGPT Agent verificável via RFC 9421 + Signature-Agent header + /.well-known/http-message-signatures-directory; Comet ultrapassou ChatGPT Agent em set-2025 como maior agentic source (52,5% vs 42%); HUMAN Security mediu +1.300% tráfego agentic jan-ago/2025; Snowplow +6.900% YoY; MCP é o padrão moat para "site como ferramenta agentic"; ai-plugin.json deprecado em mai-2026; 10 templates canônicos prontos (robots.txt, llms.txt v2, llms-full.txt, mcp.json site discovery, ai-policy.json, Schema Person+WebSite+Org, MCP server Node.js, middleware Next.js, Schema FAQPage+Speakable, Cloudflare Workers MCP remote).

---

## 4. Playbook integrado por repositório

### 4.1 landing-page-geo (alexandrecaramaschi.com)

**Stack hoje**: Next.js 16 + Cloudflare Workers + Vercel; ~340 artigos HBR em `src/lib/articles.ts` + waves; sitemap auto-discover; IndexNow `https://alexandrecaramaschi.com/api/indexnow` (key `2775badc566a4f93ac0a60417b4f14fe`); FinOps máx 2 pushes/dia.

**6 mudanças canônicas próximos 12 semanas**:

1. **(Track A §1 + Track E §Top 10 4)** Implementar `scripts/python/featgeo_audit.py`: para cada artigo, extrair vetor de features (densidade bullets, blocos canônicos, ratio cite-density, semantic unit 134-167 palavras presente, BLUF nos primeiros 150 palavras). Rodar antes do `npm run verify` como gate adicional ao `voice_guard.py`.

2. **(Track A §2 + Track B §K-NEW-007 a K-NEW-009)** Trocar métrica `citation_rate` por par `(selection_rate, absorption_rate)` no log `papers/data/llm_citation_log.json`. Para artigos high-selection-low-absorption, reescrever com bullets explícitos de definição, blocos comparação 2-coluna, número-pivô em destaque.

3. **(Track C §10.1)** Vector search interno do portal usando pgvector + Neon + OpenAI text-embedding-3-small + Voyage rerank-2.5-lite. Custo estimado US$ 20-40/mês. Servirá rota nova `/api/search-semantic` para que LLMs descobrindo o site via MCP possam consultar o índice diretamente.

4. **(Track F §Parte 7)** Expor MCP server canônico em `https://alexandrecaramaschi.com/.well-known/mcp.json` declarando tools: `get_article(slug)`, `search_articles(query)`, `list_glossary()`, `get_credentials()`. Implementação Cloudflare Workers (template em Track F Apêndice A). Habilitar nos planos de roadmap próximos 6-12 meses.

5. **(Track E §1.3 + Track B §Framework 2)** Multi-LLM Sampling Wave semanal: 50 prompts P0 sobre "Alexandre Caramaschi", "Brasil GEO", "consultor GEO Brasil" × 5 LLMs × 10 amostras = 2.500 chamadas/onda × 4 ondas/mês = US$ 40-80/mês. Persistir em DuckDB local + commit ao repo do dashboard.

6. **(Track D §3.1 + Track F §3.3)** Atualizar `robots.txt`, `llms.txt`, `ai-policy.json` para versões canônicas mai-2026: allow `OAI-SearchBot`/`Claude-SearchBot`/`PerplexityBot`/`Google-Extended` para search; allow `*-User` agents para retrieval ao vivo; **disallow** `GPTBot`/`ClaudeBot`/`Bytespider` por crawl-to-referral ratio péssimo. Considerar Cloudflare AI Audit + pay-per-crawl em q4 2026.

**Stack vendor recomendado tier Solo (~US$ 100/mês)**:
- Otterly Lite US$ 29 (15 prompts, 4 LLMs, Looker Studio connector quando Standard)
- Surfer Discovery US$ 49 (AI Tracker em todos os planos + Multi-Model em Pro+)
- Perplexity API ~US$ 10-20 (cron semanal para citation sampling)
- Brand Radar Ahrefs Select Platforms US$ 420 (já assinado para o tier Multi-portal — usar)

### 4.2 papers

**Stack hoje**: Python + Query Battery v2 (192 canonical queries, 4 verticais × 6 categorias × 2 langs × 2 types × 2 temporal frames, 50/50 PT/EN); coleta multi-LLM (Anthropic/OpenAI/Google/Groq/Perplexity); 80 entidades reais BR + 32 anchors internacionais + 16 decoys fictícios.

**6 mudanças canônicas próximos 12 semanas**:

1. **(Track A §5 + Track B §Framework 2-3)** Atualizar metodologia v2 para v3 explicitando: amostragem por distribuição (mín 5 amostras por prompt × modelo × dia, sampling perfis deterministic + stochastic). Documentar como `papers/docs/METHODOLOGY_V3.md` substituindo o V2.

2. **(Track A §7-10 GhostCite/CiteAudit/CiteTracer/urlhealth)** Adicionar pipeline de validação automática de URLs citadas: `papers/src/citation_validator/`. Toda URL citada pela coleta multi-LLM é submetida a urlhealth (`urlhealth.research`) para detectar URLs nunca-existentes (3-13% no estudo). Atualizar Paper 4 com seção sobre citation hallucination measurement.

3. **(Track C §10.2)** Pipeline RAG sobre os papers acadêmicos coletados: LlamaParse v2 (parse de PDF de papers) → BGE-M3 (embedding 1024 dim, multilíngue PT-BR) → Qdrant 1.16 self-hosted → Cohere Rerank 4 → Adaptive-RAG router. Custo US$ 530-740/mês. Habilita Q&A semântico sobre toda biblioteca + cross-check de citações dos próprios papers do programa.

4. **(Track A §11-12 ResRank/PyRAG)** Considerar substituir BM25 puro da Query Battery por ResRank em queries texto+tabela. Mas Track A §11 lembra: BM25 ainda bate dense embeddings em documentos texto+tabela financeira — fazer A/B antes de migrar.

5. **(Track B §K-NEW-013 a K-NEW-018)** Adicionar 6 KPIs novos ao dashboard papers: Citation Persistence Index (CPI), Brand Echo Decay (BED), Cross-LLM Consistency Index (CLCI), Citation Velocity, Token-Weighted Mention Rate, Geo-AI Visibility PT/EN.

6. **(Track A §17-18 Causal Memory + Tabular Chunking)** Para o Paper 5 (próximo da fila), incorporar: (a) Causal Memory Intervention para seleção de memória de longo prazo do harness; (b) Structure-Aware Tabular Chunking para tabelas no corpus (MRR 0,357→0,594 documentado).

**Stack vendor recomendado tier Multi-portal (~US$ 800/mês)**:
- Peec Pro US$ 245 (3 LLMs core + Claude/DeepSeek/Gemini, 2 projetos)
- Scrunch Starter US$ 250 (350 custom prompts + 1.000 industry, 3 personas, page audits)
- Ahrefs base + Brand Radar Select US$ 420 (já validado)

### 4.3 curso-factory

**Stack hoje**: pipeline Drive-import → drafts markdown → voice_guard.py → publicação. CLI `cli.py` (22 KB); voice canônico Alexandre; FinOps multi-client.

**6 mudanças canônicas próximos 12 semanas**:

1. **(Track A §1 + Track A §3 GEO-SFE)** Adicionar gate `scripts/python/featgeo_check.py` antes da geração de HTML final de cada lição. Quantifica perfil estrutural (headings, listas, blocos canônicos) — GEO-SFE provou +17,3% citation rate + 18,5% quality score.

2. **(Track C §10.3)** Implementar LanceDB embedded para cross-link automático entre lições do curso: OpenAI text-embedding-3-small + RAPTOR para clustering hierárquico. Custo ~US$ 0/mês (LanceDB local-first). Servirá módulo "lições relacionadas" e "siga aprendendo".

3. **(Track B §Framework 1 + 2)** Por curso publicado, prompt portfolio de 50 prompts × 5 LLMs × 10 amostras = 2.500 chamadas/onda × 1 onda/semana × 5 cursos = US$ 100-200/mês. Detecta citation rate por curso e identifica cursos com selection alta + absorption baixa para reescrita.

4. **(Track F §Parte 7)** Para cada curso, expor MCP server canônico declarando: `get_lesson(slug)`, `search_lessons(query)`, `get_course_structure()`. Implementação: rota Next.js `/api/mcp` retornando JSON-RPC 2.0 conforme spec MCP 2025-06-18.

5. **(Track E §Top 10 ações 2-5)** Padronizar template HBR-grade dos cursos para conter sempre: (a) BLUF nos primeiros 150 palavras de cada lição; (b) author entity com sameAs Wikidata + ORCID + LinkedIn de Alexandre; (c) 15+ entidades Wikidata por lição via JSON-LD `mentions`; (d) bloco "fontes nomeadas" em cada lição com `<cite>` + URL canônica.

6. **(Track A §16 SoK Agentic RAG)** Para cursos que envolvem agentic AI (curso "Agentes IA na prática" se vier a existir), incorporar taxonomia POMDP do SoK 2603.07379 e mapeamento das 9 vulnerabilidades de governança.

**Stack vendor recomendado tier Solo+Multi (~US$ 300/mês para 3-5 cursos ativos)**:
- AthenaHQ Self-Serve US$ 95 anual (8+ LLMs incl. Grok, integração GA4/GSC/Shopify, RBAC team seats)
- Frase Scale US$ 129 (AI Agent 80+ skills, AI Visibility integrada)
- OpenAI/Voyage/BGE-M3 embeddings ~US$ 0-50

---

## 5. Cross-references entre tracks

| Tema | Track principal | Tracks que ampliam |
|---|---|---|
| Citation measurement (selection × absorption) | A §2 | B §K-NEW-007 a 009; E §1.2 |
| Distribuição não-número | A §5 | B §Framework 2 |
| Citation hallucination (URLs inventadas) | A §7-10 | F §6 (agent analytics) |
| Anti-padrões llms.txt | F §3.1 | E §3; D §Mike King 18-mai |
| MCP como moat agentic | F §2 | C §5 (agentic RAG); §4 deste doc |
| Schema não move citação | D §Ahrefs 11-mai | E §1.2 (Two-Phase JSON-LD) |
| Top 50 domínios concentram 47% citations | D §Sumário | E §1.2 (Wikipedia+Reddit lideram) |
| Embeddings PT-BR (Serafim PT, BGE-M3) | C §1.1-1.2 | A §11 (BM25 ainda relevante texto+tabela) |
| Robots.txt granular 10+ bots | F §1 | E §Top 10 ação 7; §4 deste doc |
| Princeton GEO playbook lifts | E §Top 10 ação 2 | A §1-2 (FeatGEO + selection/absorption) |
| Multi-Touch Attribution AI surfaces | B §Framework 4 | E §1.4 (Subscription Linking) |
| Cloudflare AI Audit + pay-per-crawl | F §6 | D §Stack vendor recommendation |
| RFC 9421 ChatGPT Agent verification | F §1.1 | E §Parte 8 cross-surface |
| AIO em 51,5% das queries | A §6 (SIGIR 2026) | E §1.1 (Google AI Optim Guide 15-mai) |
| Bloquear Google-Extended pune AIO | A §6 + F §1.3 | §4 deste doc (cada repo decide caso a caso) |

---

## 6. Roadmap operacional 12 semanas (jun-ago 2026)

### Semanas 1-2 (26-mai a 8-jun)
- [ ] Copiar os 6 tracks + este Master Index em `docs/research/state-of-art-2026-05/` dos 3 repos
- [ ] Atualizar `robots.txt` + `llms.txt` + `ai-policy.json` dos 3 portais (template Track F Apêndice A)
- [ ] Implementar `featgeo_audit.py` em landing-page-geo (gate antes de `npm run verify`)
- [ ] Trocar KPI `citation_rate` por par `(selection_rate, absorption_rate)` no harness papers

### Semanas 3-4 (9 a 22-jun)
- [ ] Multi-LLM Sampling Wave operacional em landing-page-geo (50 prompts × 5 LLMs × 10 amostras × 1/semana)
- [ ] urlhealth check pipeline em papers (validação de URLs citadas)
- [ ] LanceDB embedded em curso-factory (cross-link entre lições)

### Semanas 5-8 (23-jun a 20-jul)
- [ ] METHODOLOGY_V3.md em papers (substitui V2 com sampling por distribuição)
- [ ] MCP server canônico em landing-page-geo (`/.well-known/mcp.json` + Cloudflare Workers stub)
- [ ] Citation Persistence Index recálculo mensal habilitado (Track B §Framework 3)
- [ ] Dashboard GEO operacional em produção (Hex ou Metabase, ingestão DuckDB)

### Semanas 9-12 (21-jul a 17-ago)
- [ ] Pipeline RAG completo em papers (LlamaParse v2 + BGE-M3 + Qdrant + Cohere Rerank 4 + Adaptive-RAG router)
- [ ] MCP server em curso-factory (por curso, rotas `/api/mcp`)
- [ ] Cloudflare AI Audit + pay-per-crawl avaliado em landing-page-geo (decisão de bloquear GPTBot/ClaudeBot/Bytespider)
- [ ] V3 do KB em curso-factory consolidando este Master Index + 12 semanas de medição

---

## 7. Anti-padrões consolidados 2026

Lista canônica do que **NÃO fazer**, extraída dos 6 tracks:

1. **Tratar selection e absorption como uma só métrica** (Track A §2) — confunde Perplexity (muitas citações peso baixo) com ChatGPT (poucas citações peso alto).
2. **Medir citation rate em snapshot único** (Track A §5) — é distribuição, exige 5+ amostras por prompt × modelo × dia.
3. **Implementar schema JSON-LD esperando lift de citação direto** (Track D Ahrefs 11-mai) — schema é Knowledge Graph infrastructure, não AI citation button. Faz parte da Phase 1, não Phase 2.
4. **Implementar llms.txt esperando ranking** (Track F §3.1) — Mueller, Illyes, Sullivan, Splitt todos públicos contra. Vale para reduzir custo de ingestão pós-visita, não para placement.
5. **Bloquear Google-Extended sem entender consequência** (Track A §6 + Track F §1.3) — pune visibilidade em AIO mesmo com indexação aberta. Decisão consciente caso a caso.
6. **Bite-sized chunking artificial "para LLMs"** (Track E §1.4) — Danny Sullivan canônico: "write for users, not for LLMs". Conteúdo otimizado para humano + estrutura semântica + entity grounding já é o ótimo.
7. **FAQPage schema decorativo** (Track E §1.2) — apenas onde FAQ é genuíno (pergunta real do leitor). Decorativo é anti-padrão; Google removeu rich results 7-mai-2026 mas mantém sinal semântico.
8. **Republicar com `dateModified` sem mudança editorial real** (Track E §Top 10 ação 9) — Google detecta thin-update.
9. **Acrônimos PT-BR sem fonte primária** (V2 §6 mantém): AIGVR, AECR, CTAM, RTAS, Brand Echo Score (LLM Visibility Index e GEO Authority Rank também ficam ambíguos). Use "Position-Weighted SoV" em vez de "RTAS".
10. **Sub-agent que produz copy SEM o prefix PT-BR canônico** (CLAUDE.md global incidente curso `saude-mental-vibecoding` 14-05-2026) — sempre carimbar `C:/Sandyboxclaude/scripts/prompts/COPY_PROMPT_PREFIX.md`.
11. **Disparar wave sem `git status` antes** (memória `feedback_claude_paralelo_mesmo_working_tree` 19-mai-2026) — outro agente paralelo no mesmo working tree clobba silenciosamente.
12. **Push em projeto Vercel sem confirmar Git connection** (memória `feedback_vercel_project_sem_git_connection`) — incidente 19-mai-2026 com `web` (larissacaramaschi.com), 7 commits silenciosamente ignorados.

---

## 8. Apêndice — arquivos e custo

### 8.1 Arquivos produzidos nesta sessão

| Arquivo | Palavras | Linhas | KB |
|---|---|---|---|
| `track-A-papers-q2-2026.md` | 8.475 | 634 | 62 |
| `track-B-frameworks-kpis.md` | 7.587 | 939 | 63 |
| `track-C-llm-vector-stateofart.md` | 7.645 | 771 | 63 |
| `track-D-vendors-columns.md` | 8.126 | 424 | 57 |
| `track-E-ranking-factors.md` | 6.951 | 686 | 59 |
| `track-F-b2a-aso-agentic.md` | 8.512 | 1.460 | 69 |
| `GEO_STATE_OF_ART_2026_05_MASTER.md` (este) | ~3.500 | ~280 | ~30 |
| **Total** | **~50.800** | **~5.200** | **~403** |

### 8.2 Custo total da pesquisa

| Item | Valor estimado USD |
|---|---|
| Perplexity sonar-deep-research (30+ chamadas) | ~10,91 |
| Anthropic Opus 4.7 (6 sub-agents + main) | ~35-50 |
| OpenAI / Gemini / Groq / Grok (chamadas auxiliares) | ~0,50 |
| **Total** | **~46-62 USD** |

### 8.3 Quem usar este documento

- Alexandre Caramaschi (CEO Brasil GEO) — referência operacional canônica para próximas 12 semanas
- Sub-agents Opus em paralelo nos 3 repos — anexar este doc + Tracks relevantes como contexto de cada wave
- Clientes Brasil GEO em auditoria GEO — usar §1 (12 conclusões), §4 (playbook por repo), §7 (anti-padrões)
- Pesquisadores/autores de papers — usar Track A (18 papers Q2 2026) como referência bibliográfica

### 8.4 Próxima revisão

Recomendação: revisão completa em **30-jun-2026** (delta jun) e **30-set-2026** (delta jul-set, deve incluir SIGIR 2026 ago/2026, ACL findings, KDD 2026). Mantenedor: Alexandre Caramaschi.

---

> Fim do Master Index. Os 6 tracks completos vivem ao lado deste arquivo em `_geo-research-20260520-evening/` e são copiados para `docs/research/state-of-art-2026-05/` em cada repo.
