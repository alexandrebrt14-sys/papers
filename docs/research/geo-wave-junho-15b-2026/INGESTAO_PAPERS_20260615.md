# Ingestão de papers — Wave 15B (15-jun-2026)

> Catálogo de ingestão dos arXiv IDs novos da Wave 15B, classificados contra os **50 conceitos canônicos** (`docs/GEO_50_CONCEITOS_CANONICAL.md`, REGRA #2) e organizados pelos **4 eixos de leitura** do §7.2 do doc canônico. Cada paper entra com link `abs`, status de verificação e a **consequência metodológica** para este repo (hipótese a pré-registrar, variável de controle, campo de schema ou consideração de red-team). Critério: só ingere ID com existência/tema confirmados via WebFetch da página `abs` — IDs alegados sem verificação (ex.: os que o `sonar-deep-research` inventou) ficam de fora.

## Eixo A — Frameworks de execução

### `2606.12439` — Position: GEO Creates Underexamined Risks (ICML 2026 Position Track)
- **Verificação:** ✓ `arxiv.org/abs/2606.12439` (Wen, Zhang, Yuan, Chen, Zhang, Guo — 18-mai-2026).
- **Conceitos:** 24 (Citabilidade GEO), 25 (Recuperabilidade generativa), 26 (Risco de pseudo-GEO), 27 (Governança de IA).
- **Núcleo:** formaliza GEO como otimização **conjunta** de `retrievability` (probabilidade de entrar no pool de evidências) × `ranking impact` (deslocar a resposta uma vez no contexto), via *retrieval booster messages* e *ranking shifter messages*.
- **Consequência (papers):** separar formalmente os **dois desfechos** na coleta/análise — "fomos recuperados?" ≠ "fomos usados/citados?". Pré-registrar como duas variáveis dependentes distintas; hoje a coleta colapsa as duas em `cited`. Candidato a campo derivado `retrieval_vs_impact` no schema v2.

### `2605.25517` — What Gets Cited: Competitive GEO in AI Answer Engines
- **Verificação:** ✓ `arxiv.org/abs/2605.25517` (Vishwakarma, Kumar, Jamidar — 25-mai-2026). **252.000 trials**, 6 LLMs, testbed RAG de 2 documentos, marca anonimizada, ordem contrabalançada.
- **Conceitos:** 9 (Intenção de busca), 10 (Cobertura semântica), 11 (Answer capsules), 24, 25.
- **Núcleo:** **relevância tópica** e **posição na lista** são os maiores preditores de ser citado primeiro; **preço explícito** e **timestamp recente** ajudam de forma consistente; completude e sinais de confiança rendem menos; formatação cosmética, pouco.
- **Consequência (papers):** os fatores-gatekeeper viram **hipóteses falsificáveis PT-BR** (já parcialmente referenciado na Wave Junho 07-jun — agora com o número verificado de 252k trials e o desenho pareado). Variáveis de controle no modelo: `topical_match`, `list_position`, `has_price`, `has_recent_timestamp`. Separa efeito de conteúdo de viés de posição — replicável no nosso testbed.

## Eixo B — Medição / KPIs

(Sem paper novo dedicado nesta passada; a camada de medição é coberta pelo §3 do doc canônico — taxonomia SoV/Answer Inclusion Rate/Citation Rate e benchmarks de impacto com fonte primária. **Correção a propagar no METHODOLOGY:** "Share of Answer" não é KPI normalizado — não usar como termo técnico.)

## Eixo C — Recuperação / chunking / reranking

### `2603.06976` — Document Chunking Strategies & Embedding Sensitivity
- **Verificação:** ✓ (Shaukat, Adnan, Kuhn — 07-mar-2026). 36 métodos × 6 domínios × 5 embeddings.
- **Conceitos:** 10 (Cobertura semântica), 11 (Answer capsules), 25 (Recuperabilidade).
- **Núcleo:** **Paragraph Group Chunking** lidera (nDCG@5≈0,459); chunking fixo por caractere é fraco (<0,244).
- **Consequência (papers):** fundamento empírico da rubrica de recuperabilidade — chunk por unidade semântica (parágrafo/seção), não por contagem fixa. Variável de controle de qualidade de extração na coleta.

### `2601.15457` — Chunking, Retrieval & Re-ranking (policy QA)
- **Verificação:** ✓ (Maharjan, Yadav — 21-jan-2026).
- **Conceitos:** 25, 24.
- **Núcleo:** Advanced RAG com re-ranking → faithfulness 0,797 vs 0,621 (basic) vs 0,347 (vanilla).
- **Consequência:** o reranking é o estágio que mais move fidelidade — relevante para o desenho dos agentes sintéticos de teste (RAG local) e para interpretar por que páginas recuperadas nem sempre são citadas.

### `2605.01664` — Hybrid Retrieval + Reranking (evidence-grounded RAG)
- **Verificação:** ✓ (Irany, Akwafuo — 03-mai-2026). Domínio saúde.
- **Conceitos:** 25, 23 (E-E-A-T), 21 (Referências externas).
- **Núcleo:** híbrido (BM25+vetor) + rerank Cohere → 100% grounding em 200 alegações.
- **Consequência:** referência para a vertical `saude` do nosso painel; reforça que vencer recall lexical E semântico é pré-condição.

### `2604.04936` — W-RAC: Web Retrieval-Aware Chunking
- **Verificação:** ✓ (Allu, Kedia, Odapally, Ahmed — 08-jan-2026).
- **Conceitos:** 25, 10.
- **Núcleo:** performance comparável/melhor reduzindo custo de chunking por LLM em **uma ordem de magnitude**.
- **Consequência (FinOps):** padrão de chunking custo-eficiente — alinha com a disciplina de custo da coleta (`finops_usage`).

## Eixo D — Riscos / manipulação / red-team

### `2605.29107` — GEO-Bench: Benchmarking Ranking Manipulation in GEO
- **Verificação:** ✓ `arxiv.org/abs/2605.29107` (Nimase, Chen, Qi, Zhao, Hu — 27-mai-2026, cs.CR).
- **Conceitos:** 26 (Risco de pseudo-GEO), 27 (Governança de IA).
- **Núcleo:** reescrita black-box de conteúdo **iguala/supera** ataques gradient-based (STS), com texto mais fluente e **evasão de detecção por keyword e por perplexidade**; nível de acesso ao modelo não prediz força do ataque.
- **Consequência (papers):** entra na seção de **ética/limitações e red-team** dos nossos papers — define a fronteira entre GEO legítimo (engenharia de relevância) e manipulação detectável. Variável de governança: nossas intervenções (`intervention.py`) ficam do lado legítimo e auditável da linha. Cruza com o alerta da Lily Ray (táticas populares tratadas como spam).

## Já ingeridos antes (reconciliação, não re-ingestão)
- `2603.29979` GEO-SFE e `2603.09296` AgentGEO — ingeridos na Wave Junho 15 (1ª passada); existência reconfirmada via `abs` nesta passada. AgentGEO reconcilia a antiga referência "taxonomia de 7 tipos de falha" usada em `failure_classifier.py`.
- `2605.12887` EcoGEO — ✓ existência/tema; resultado quantitativo principal não está no abstract (precisa do PDF).

## Caso de produto (não benchmark)
- `2602.02961` — GEO em cenário de produto (Pinterest, VLM+agentes). Útil como caso aplicado; **não** usar como benchmark de citação.

## Correções de datação (anti-drift)
- `2509.10762` (GEO-16) e `2509.08919` ("How to Dominate AI Search") são de **set/2025**, não 2026 — datar corretamente em qualquer citação/related-work.

---

**Tags `classify.md` sugeridas para esta leva:** `retrievability-vs-impact` (de `2606.12439`), `gatekeeper-factors` (de `2605.25517`), `chunking-empirical` (de `2603.06976`/`2604.04936`), `manipulation-redteam` (de `2605.29107`).
