# Wave Junho 15B 2026 · Incremento canônico GEO/SEO/AEO — pesquisa viva multi-fonte

> **Data de corte:** 15 de junho de 2026 (segunda passada do dia).
> **Status:** complementa — não substitui — o `GEO_WAVE_JUNHO_15_2026_CANONICAL.md` (mesma data, primeira passada) e todo o corpus anterior (`geo-wave-junho-2026`, `geo-q3-2026-pos-io`, `state-of-art-2026-05`). A primeira passada de 15-jun **rodou sem busca Perplexity ao vivo** (o `sonar-deep-research` retornou `search results = None` e foi corretamente descartado como fonte de fato). Esta passada **fecha essa lacuna**: foi ancorada em pesquisa viva de duas frentes independentes e cruzadas.
> **Fontes e método (transparência):** (1) **Perplexity `sonar-pro`** (modelo online, com `search_results`+`citations` reais), 7 queries cirúrgicas em inglês — runner `geo-orchestrator/scripts/research_geo_pplx_sonarpro_20260615.py`, raws em [`raw/P1..P7.json`](raw/); (2) **WebSearch + WebFetch do Claude** em 3 sub-agentes paralelos (fornecedores, papers acadêmicos, produto/algoritmo+KPIs), com verificação de fontes primárias e arXiv `abs` página a página. **Toda afirmação datada abaixo aparece com fonte; o que uma frente não confirmou está isolado em §8.** Aprendizado operacional reforçado: `sonar-deep-research` não fez grounding neste ambiente — usar **`sonar-pro`** para fato datado e **WebFetch** para verificar arXiv/valuation.
> **Como aplicar:** leitura obrigatória **antes** de qualquer decisão sobre dashboard/KPI de cliente, escolha de ferramenta de AI visibility, briefing de sub-agent de pesquisa ou copy, design de schema/llms.txt, rubrica de redação ou auditoria GEO em portfolio Brasil GEO. As correções de §8 **revogam** fatos antes canonizados — preferir esta versão em caso de conflito.

---

## 0. Sumário executivo (TL;DR)

O delta desta passada não muda a tese (GEO = engenharia de relevância para recuperação e citação), mas **fundamenta com fontes primárias vivas** o que a primeira passada do dia teve de afirmar sem busca, **adiciona papers e um pipeline técnico verificável**, e **corrige quatro fatos** que estavam errados ou imprecisos no corpus canônico.

| Achado | Fonte primária verificada | Impacto canônico |
|---|---|---|
| **Paper-posição ICML 2026: "GEO Creates Underexamined Risks"** — `arXiv:2606.12439` (Wen et al., 18-mai-2026) | arxiv.org/abs/2606.12439 | Formaliza GEO como otimização conjunta de **retrievability** (entrar no pool de evidências) × **ranking impact** (deslocar a resposta), via *retrieval booster messages* e *ranking shifter messages*. Dá o vocabulário acadêmico para separar "ser recuperável" de "ser influente". |
| **What Gets Cited** — `arXiv:2605.25517` (252.000 trials, 6 LLMs) | arxiv.org/abs/2605.25517 | Em testbed RAG de 2 documentos: **relevância tópica e posição na lista** são os maiores preditores de ser citado primeiro; **preço explícito e timestamp recente** ajudam de forma consistente; edições só de formatação têm impacto pequeno. |
| **GEO-Bench** — `arXiv:2605.29107` (manipulação de ranking) | arxiv.org/abs/2605.29107 | Reescrita black-box de conteúdo **iguala ou supera** ataques gradient-based, com texto mais fluente e evasão a detecção — nível de acesso ao modelo não prediz força do ataque. Define a fronteira spam↔GEO legítimo. |
| **Pipeline de AI search em 4 estágios (consenso 2026)** | leapd.ai, openai.com/index/introducing-chatgpt-search, winstondigital | Indexação (lexical BM25 + vetorial + grafo de entidades) → recall híbrido + **query fan-out** → **reranking neural (cross-encoder)** + seleção de chunks citáveis → geração + atribuição com viés a domínios confiáveis. |
| **Profound Série C: US$ 96M a valuation de US$ 1 bi (unicórnio), lead Lightspeed** | Fortune + SiliconANGLE, 24-fev-2026 | Total acumulado US$ 155M em ~18 meses. Cobre ~9–10 motores; **Profound Index** (5-nov-2025) + **Conversation Explorer (400M+ conversas)** + **Profound Agents** (workflows GA, fev-2026). |
| **Scrunch AI adquirida pela Sitecore** (~US$ 225M, Bloomberg) | Sitecore newsroom + Bloomberg, 3-jun-2026 | Consolidação do setor de AI visibility dentro de DXPs. |
| **Semrush × Perplexity: MCP Connector nativo no Perplexity** | Semrush news 460693, 3-jun-2026 | Expõe 28,4bi keywords / 261mi prompts LLM dentro do Perplexity. AI Visibility Index público = **2 engines** (ChatGPT ~80% peso + AI Mode ~20%); Enterprise AIO = 5 engines. |
| **RCT de campo de AI Overviews** (ISB + Carnegie Mellon, N=1.065) | Search Engine Journal / AEA RCT #17393, abr-2026 | **−38% de cliques orgânicos**; cliques/busca 0,61→0,38; zero-click 54%→72%. Primeira evidência causal randomizada (não revisada por pares ainda). |
| **Seer Interactive 2026** (5,47M queries, 53 marcas) | seerinteractive.com, abr-2026 | Citação no AIO entrega **+120% de cliques/impressão** vs não citado; CTR com AIO recuperou de 1,3% (dez/25) para 2,4% (fev/26). |
| **SparkToro: 68,01% de buscas sem clique** (jan–abr/2026) | sparktoro.com, 8-jun-2026 | Vs 60,45% em 2024; AIO em >20% das buscas reduz CTR ~60%; **AI Mode = só 0,34%** das buscas. |
| **Microsoft Clarity AI Citations (GA)** | learn.microsoft.com/clarity, 13-mai-2026 | Métricas grátis: Page Citations, Share of Authority, AI Referral Traffic, Grounding Queries — democratiza medição que antes era só enterprise. |
| **Lily Ray: táticas populares de GEO tratadas como spam** | ppc.land, 14-mai-2026 | Google/Microsoft classificam *prompt injection* ("summarize with AI") e *scaled content* como spam → risco de penalidade. Freio de qualidade ao GEO agressivo. |
| **llms.txt: 10,13% de adoção e ZERO correlação com citação** | SE Ranking (300k domínios), mar-2026 | Google rejeitou (Illyes: "no plans to support"). Padrão real: **IETF AIPREF** — header HTTP `Content-Usage` + diretiva no robots.txt (NÃO `/.well-known/ai-preferences`). |

### Sete premissas operacionais consequentes (a partir de 15-jun-2026, 2ª passada)

1. **GEO acadêmico agora separa retrievability de ranking impact.** (`2606.12439`) Otimizar para entrar no pool de evidências é um problema; influenciar a resposta uma vez dentro do contexto é outro. **Aplicação:** auditoria mede os dois eixos separadamente — "fomos recuperados?" e "fomos usados/citados?".
2. **O que faz ser citado primeiro é relevância tópica + posição + preço/recência explícitos.** (`2605.25517`, 252k trials) Formatação cosmética rende pouco. **Aplicação:** a rubrica de redação prioriza casamento tópico forte, dados/números datados e (em páginas comerciais) preço explícito; para de superinvestir em "negrito bonito".
3. **A fronteira entre GEO e spam ficou nítida e perigosa.** (`2605.29107` + Lily Ray) Reescrita manipulativa funciona tecnicamente mas é detectável e punível. **Aplicação:** Brasil GEO entrega engenharia de relevância legítima (estrutura, evidência, entidade), nunca *prompt injection* ou *strategic text sequences*.
4. **O pipeline de citação é híbrido (BM25 + vetor) com fan-out e reranking.** **Aplicação:** conteúdo precisa vencer recall lexical E semântico; chunks autocontidos, curtos, com números/nomes ganham no reranking; cobrir o **leque de reformulações** (fan-out) de um tópico, não uma única keyword.
5. **A medição democratizou (Clarity grátis) mas não padronizou.** "Share of Answer" **não é** KPI normalizado; o conceito é coberto por SoV + Answer Inclusion Rate + Prompt Coverage. **Aplicação:** todo report nomeia a metodologia e a fonte de cada número; nunca apresentar SoV de fornecedores diferentes lado a lado como se fossem comparáveis.
6. **A citação tem ROI mesmo no zero-clique, com evidência causal.** RCT: −38% de cliques agregados; Seer: +120% por impressão para quem é citado. **Aplicação:** o pitch é "capturar a fração qualificada que clica + a lembrança de marca que não clica", com o RCT como prova de causalidade.
7. **O controle de acesso de IA é header `Content-Usage` + robots.txt (AIPREF), não llms.txt nem `/.well-known`.** **Aplicação:** llms.txt fica como defensivo de baixo custo (não como alavanca de citação — correlação zero); acompanhar `draft-ietf-aipref-vocab` (v06 ativo) e `draft-ietf-aipref-attach`.

---

## 1. Papers 2026 — verificados via arXiv `abs` (frameworks, KPIs, citação)

> Critério de inclusão: existência e tema confirmados via WebFetch da página `arxiv.org/abs/<id>` (frente Claude) ou `search_results` do Perplexity. Resultado quantitativo só listado quando estava no abstract. IDs marcados ⚠ têm existência confirmada mas número principal não recuperado.

### 1.1 Núcleo GEO

| ID | Título / autores | Data | Método | Resultado canônico |
|---|---|---|---|---|
| `2606.12439` | **Position: GEO Creates Underexamined Risks** — Wen, Zhang, Yuan, Chen, Zhang, Guo (ICML 2026 Position Track) | 18-mai-2026 | Paper de posição; formaliza pipeline de GEO | GEO = otimização conjunta de **retrievability** (prob. de entrar no pool de evidências) × **ranking impact**; decompõe conteúdo em *retrieval booster messages* e *ranking shifter messages*. Conceitual, sem coeficientes. |
| `2605.25517` | **What Gets Cited: Competitive GEO in AI Answer Engines** — Vishwakarma, Kumar, Jamidar | 25-mai-2026 | Testbed RAG de 2 documentos, **252.000 trials** em 6 LLMs, marca anonimizada, ordem contrabalançada | **Relevância tópica e posição na lista** = maiores preditores; **preço explícito + timestamp recente** ajudam consistentemente; completude e sinais de confiança dão ganhos menores; formatação pura, pouco. Entrega protocolo + checklist. |
| `2605.29107` | **GEO-Bench: Benchmarking Ranking Manipulation in GEO** — Nimase, Chen, Qi, Zhao, Hu (cs.CR) | 27-mai-2026 | Compara ataques gradient-based (STS) × reescrita black-box | Reescrita black-box **iguala/supera** gradient-based, mais fluente e furtiva (evade detecção por keyword e perplexidade); acesso ao modelo não prediz força do ataque. |
| `2603.29979` | **GEO-SFE: Structural Feature Engineering for GEO** — Yu, Yang, Ding, Sato | 31-mar-2026 | Estrutura em 3 níveis: macro (arquitetura), meso (chunking), micro (ênfase visual); 6 engines | **+17,3% citation rate**, **+18,5% qualidade**; "definition-first" e markup estruturado (FAQ/HowTo) entre top-5 preditivos; densidade informacional > densidade de keyword. |
| `2603.09296` | **AgentGEO: Diagnosing and Repairing Citation Failures** — Tian, Chen, Tang, Liu, Jia | 10-mar-2026 | Sistema agêntico: taxonomia de falhas + reparo cirúrgico iterativo | **>40% de citação relativa modificando 5% do conteúdo** (vs 25% de baselines); alerta que otimização genérica pode prejudicar long-tail. |
| `2605.12887` ⚠ | **EcoGEO: Trajectory-Aware Evidence Ecosystems** — Ye, Mao, Guan, Tian | 13-mai-2026 | TRACE: ecossistema de evidência (página-entrada agêntica + páginas de suporte) | Reposiciona GEO de **página única → ecossistema** para agentes que percorrem múltiplas páginas. Número principal não no abstract. |
| `2602.02961` ⚠ | **GEO em cenário de produto (Pinterest, VLM+agentes)** | 2026 | Framework GEO para crescimento de aquisição | Existência confirmada via Perplexity; detalhes quantitativos não recuperados. Tratar como caso de produto, não benchmark. |

### 1.2 Contexto (set/2025 — citados como base, não "novo de 2026")

- `2509.10762` **GEO-16** (Kumar, Palkhouski, 13-set-2025) — auditoria de 16 pilares, GEO score G∈[0,1]; 1.702 citações em 1.100 URLs (Brave, AIO, Perplexity); Metadata, Freshness, Semantic HTML e Structured Data são as associações mais fortes.
- `2509.08919` **GEO: How to Dominate AI Search** (Chen, Wang, Chen, Koudas, 10-set-2025) — viés sistemático de AI search por **Earned media** sobre Brand-owned e Social ("big brand bias" que desfavorece nichos).
- `2311.09735` **GEO (fundacional)** (Aggarwal et al., KDD 2024) — origem das "9 técnicas de citação" (Cite Sources +115%, Stats +41%, Quotation +28%); visibilidade até +40%.

### 1.3 Recuperação / RAG / chunking / reranking (2026, verificados)

- `2603.06976` **Document Chunking Strategies & Embedding Sensitivity** (Shaukat, Adnan, Kuhn, 7-mar-2026): 36 métodos × 6 domínios × 5 embeddings. **Paragraph Group Chunking lidera** (nDCG@5≈0,459); chunking fixo por caractere é fraco (<0,244). → *Chunk por unidade semântica (parágrafo/seção), não por contagem fixa de caracteres.*
- `2601.15457` **Chunking, Retrieval & Re-ranking (policy QA)** (Maharjan, Yadav, 21-jan-2026): Advanced RAG com re-ranking = faithfulness 0,797 vs Basic 0,621 vs Vanilla 0,347. → *O reranking é o estágio que mais move fidelidade.*
- `2605.01664` **Hybrid Retrieval + Reranking (evidence-grounded RAG)** (Irany, Akwafuo, 3-mai-2026): híbrido + rerank Cohere → 100% grounding em 200 alegações (domínio saúde).
- `2604.04936` **W-RAC: Web Retrieval-Aware Chunking** (Allu et al., 8-jan-2026): performance comparável/melhor reduzindo custo de chunking em **uma ordem de magnitude**.

**Síntese para redação/auditoria:** a literatura de 2026 converge em três alavancas controláveis pelo produtor de conteúdo — (a) **estrutura/chunking** autocontido por unidade semântica (`2603.29979`, `2603.06976`), (b) **relevância tópica + recência + especificidade** (preço/números/timestamps) (`2605.25517`), (c) **diagnóstico-reparo cirúrgico** em vez de reescrita total (`2603.09296`). Os outros estágios (recall híbrido, reranking) são do motor — o produtor influencia indiretamente garantindo que o chunk vença tanto BM25 quanto a similaridade vetorial.

---

## 2. Camada semântica/vetorial — como o motor escolhe a fonte (2026)

Consenso de estudos comparativos de ChatGPT Search, Perplexity e Google AI Overviews (leapd.ai; OpenAI "Introducing ChatGPT Search"; winstondigital). **Pipeline médio em 4 estágios:**

1. **Indexação.** Crawlers próprios + APIs + dados de parceiros. Constrói: índice **lexical** (BM25) para keyword match; índice **vetorial** (embeddings) para similaridade semântica; **grafo de entidades/autores** + sinais de confiança de domínio. (ChatGPT Search = "fine-tuned GPT-4o" + "third-party search providers" + conteúdo de parceiros — camada de meta-search.)
2. **Recall híbrido + fan-out.** **Hybrid retrieval** (BM25 + vetor) puxa 100–1000 candidatos. O LLM gera **query fan-out**: múltiplas reformulações/sub-consultas rodando em paralelo no índice. → *cobrir o leque de formulações de um tópico, não uma keyword.*
3. **Reranking + seleção de chunks.** Reranker neural (cross-encoder) reordena por relevância fina, evidência factual e diversidade. Documentos são divididos em **chunks autocontidos**; o sistema prefere chunks curtos, específicos, com números/nomes ("chunk-level citability").
4. **Geração + atribuição.** O LLM recebe consulta + chunks + metadados (fonte, data, entidades) e gera via RAG; exibe um **subconjunto pequeno** de fontes como citação, com **viés forte a domínios confiáveis** e chunks limpos.

**Implicações práticas de relevance engineering (camada que o cliente controla):**
- **Embeddings:** otimizar para similaridade semântica = escrever a *resposta* à intenção, com a entidade e o termo-conceito explícitos no mesmo bloco (não dispersos). "Definition-first" (`2603.29979`) ajuda o embedding a casar a definição com a pergunta.
- **Chunking:** parágrafos/seções autocontidas que respondem uma sub-pergunta inteira; *answer capsules* de 40–80 palavras com o fato + número + fonte. Evitar dependência de contexto distante (o chunk pode ser recuperado isolado).
- **Hybrid:** vencer BM25 (termos exatos, sinônimos, entidades nomeadas) **e** o vetor (paráfrase semântica) — usar ambos os vocabulários no texto.
- **Reranking:** densidade de evidência, recência (timestamp visível), especificidade (números, nomes próprios) e confiança de domínio (E-E-A-T, autoria, citações de fonte).
- **Fan-out:** mapear as reformulações que um LLM geraria para o tópico e cobri-las com seções/FAQ.

---

## 3. KPIs, medição e reports (delta verificado)

### 3.1 Taxonomia 2026 — e a correção do "Share of Answer"

A primeira passada de 15-jun tratou "Share of Voice vs Share of Answer" como separação canônica. **Correção factual (Perplexity P4 + frente Claude):** "Share of Answer" **não aparece como KPI normalizado** em nenhum fornecedor consultado (LLM Pulse, Lumar, OptimizeGEO, Similarweb, BrightEdge, Discovered Labs). O que existe e é mensurável:

| KPI | Definição operacional | Quem usa |
|---|---|---|
| **AI Share of Voice** | % de respostas/menções da marca vs concorrentes numa cesta de prompts (às vezes ponderado por posição e/ou volume de busca do prompt) | Semrush, LLM Pulse, Similarweb, OptimizeGEO |
| **Mention** vs **Citation** | *Mention* = marca nomeada sem link; *Citation* = atribuída a uma URL/domínio | Ahrefs, Profound, Aurametrics |
| **Answer Inclusion Rate / Answer Presence** | % dos prompts relevantes em que a marca aparece **na** resposta | Lumar |
| **Prompt Coverage** | Amplitude: em quantos tipos de prompt/tópico/modelo a marca aparece | Lumar, Similarweb, LLM Pulse |
| **Citation Rate / Domain Retrieval Rate** | Frequência de citação com link / frequência de o domínio ser recuperado | Peec, Profound |
| **Sentiment** (0–100), **Position** (ranking médio na resposta) | Tom e ordem da menção | Peec, Semrush |
| **AI Referral Traffic / AI-referred pipeline** | Sessões e conversões originadas de respostas de IA | Similarweb, Clarity, Conductor |

**Premissa corrigida:** o headline KPI é **AI Share of Voice**; "estar na resposta" é medido por **Answer Inclusion Rate**; "ser a fonte linkada" por **Citation Rate**. Não usar "Share of Answer" como termo técnico sem aspas e nota.

### 3.2 Metodologias por fornecedor (como cada um calcula — não comparáveis entre si)

- **Profound:** Profound Index (5-nov-2025) = % semanal de respostas onde a marca é mencionada; pipeline = filtragem semântica → clusterização por embeddings → coleta diária do ChatGPT + entity extraction; 12 indústrias. Conversation Explorer = 400M+ conversas reais (atualização semanal, recortes regionais/demográficos).
- **Ahrefs Brand Radar:** base de 376M+ prompts/mês (AIO 282,6M; AI Mode 23,9M; ~14–15M demais), **derivados de busca real, não sintéticos**; 6 engines; separa menção de citação. Add-on a partir de US$ 199–398/mês.
- **Semrush:** AI Visibility Index público = **2 engines** (ChatGPT ~80% peso + AI Mode ~20%), ~2.500 prompts; SoV ponderado por posição + (no ChatGPT) volume de busca do tópico. Enterprise AIO = 5 engines. MCP Server (set/2025) + **MCP Connector nativo no Perplexity** (3-jun-2026).
- **Peec AI:** Visibility, Share of Voice, Sentiment (0–100), Position, Citation Rate, Domain Retrieval Rate; coleta via UI scraping; 7 engines; ARR US$ 10M (mai/2026), Série A US$ 21M.
- **Microsoft Clarity AI Citations (GA, 13-mai-2026):** Page Citations, Share of Authority, AI Referral Traffic, Grounding Queries, My Cited Pages — **grátis**.

### 3.3 Benchmarks de impacto (fonte primária)

- **RCT ISB + Carnegie Mellon** (jan–fev/2026, N=1.065, AEA RCT #17393): AIO **−38%** de cliques orgânicos; cliques/busca 0,61→0,38; zero-click 54%→72%. *Primeira evidência causal randomizada; SSRN abr/2026, não revisado por pares.*
- **Seer Interactive** (abr/2026, 5,47M queries, 53 marcas): citação no AIO = **+120%** cliques/impressão vs não citado; CTR com AIO recuperou de 1,3% (dez/25) → 2,4% (fev/26). Estudo set/2025: CTR orgânico com AIO **−61%**.
- **Pew Research** (22-jul-2025, 68.879 buscas): clique em link cai para **8%** com AI summary vs **15%** sem; clique na fonte dentro do summary = **1%**; 26% encerram a sessão.
- **seoClarity** (out/2025): 97% dos AIO citam ao menos uma fonte do **top 20 orgânico**; >99% das fontes vêm do **top 10**; média 5 URLs/AIO. → *ranquear no orgânico ainda é pré-condição para ser citado no AIO.*
- **Conductor 2026 AEO/GEO Benchmarks** (13-nov-2025): AI referral = **1,08%** do tráfego total (média 10 indústrias); **ChatGPT = 87,4%** do AI referral; 3,3 bi de sessões; AIO acionado em 25,11% das buscas.
- **Similarweb Gen AI Stats** (2026): citações em respostas 0,6% (jan/25) → 2,8% (ago/25); conversão de referral do ChatGPT 7,1% (2ª maior atrás de paid search); top domínios Wikipedia 6,2% / Reddit 5,2%.
- **Google contesta** (blog oficial, 6-ago-2025): "more queries and higher quality clicks", cliques orgânicos "relativamente estáveis YoY"; chamou o Pew de "flawed methodology". *Registrar o contraditório no report.*

### 3.4 Padronização: ainda não há

Não existe órgão/padrão formal de KPI de GEO até meados de 2026; a própria Semrush declara ausência de "fórmula padrão da indústria" para AI SoV. O IAB AI Transparency Framework (jan/2026) é sobre disclosure de IA em **publicidade**, não métrica de GEO. → *Brasil GEO publica sua própria rubrica (GEO Score) sempre com metodologia explícita.*

---

## 4. Vendor stack — delta verificado (jan–jun/2026)

- **Profound** — Série C **US$ 96M a US$ 1 bi (unicórnio)**, lead Lightspeed (Fortune+SiliconANGLE, 24-fev-2026); total US$ 155M. Suporte a Claude Fable (9-jun-2026). Datasets de pesquisa publicados: 26M prompts/13.000 categorias; **3,25 bi de citações em 7 modelos/14 países** (21-abr-2026). Tese dos fundadores: IA dirigindo **>50% do e-commerce (~US$ 2,5 tri/ano) até 2027**.
- **Ahrefs Brand Radar** — 6 engines, 376M+ prompts; estudo **"50 Most-Cited Websites in Google AI Overviews"** (1-jun-2026, >3M queries US): YouTube 20,9% · Reddit 19,6% · Facebook 11,6% · Wikipedia 4,8% · Amazon 4,0% · Quora 4,0%. Custom AI Prompt Tracking (21-jan-2026).
- **Semrush** — ver §3.2; **AI Visibility Awards** (dez/2025). NYSE: SEMR (independente — *não* subsidiária da Adobe; ver §8).
- **Scrunch AI** — **adquirida pela Sitecore** (3-jun-2026; ~US$ 225M reportado pela Bloomberg, Sitecore declinou confirmar; earnout até ~US$ 315M). Produto: Agent Experience Platform (AXP).
- **Peec AI** — Série A US$ 21M (lead Singular, valuation >US$ 100M); ARR US$ 10M (mai/2026); Berlim.
- **Conductor** — **AgentStack** enterprise (servidor MCP + agentes AEO turnkey, 20-abr-2026); relatório de benchmarks (§3.3).
- **Otterly.ai** — Public API + **Claude Skill** + Marketplace 100+ workflows (1-jun-2026); MCP "planned".
- **Goodie** — bootstrapped; **Goodie 2.0** (6-mai-2026, heatmap de concorrentes + Goodie MCP).
- **SE Ranking** — AI Visibility Tracker (5 sistemas) + standalone **SE Visible**.
- **BrightEdge** — Generative Parser™ (orig. 19-dez-2023) + AI Catalyst.
- **Nightwatch** — Matrix Source Intelligence (Beta, 6-fev-2026).

---

## 5. Produto / algoritmo — mudanças dez/2025 → jun/2026

### 5.1 Google
- **AI Mode virou default global** da experiência de Search (desktop+mobile) no **Google I/O 2026** (19-mai-2026); caixa de busca reconstruída pela 1ª vez em ~25 anos. *Ressalva:* Google **desmentiu** AI Mode como default na omnibox do Chrome (recurso no Canary descrito como erro).
- **Gemini 3** virou modelo default dos AIO globalmente (~27-28 jan/2026); **Gemini 3.5 Flash** anunciado como novo default do AI Mode no I/O 2026.
- **Search agents / "information agents"** (19-mai-2026): rodam 24/7 em background, monitoram a web e enviam updates sintetizados com links; iniciaram por Google AI Ultra (US$ 99,99/mês), Pro (US$ 19,99) "later this summer"; expansão a todos idiomas confirmada (Robby Stein, 12-jun-2026).
- **Escala:** AIO 2,5 bi MAU; AI Mode 1 bi MAU no 1º ano (I/O 2026).

### 5.2 OpenAI / ChatGPT
- **Anúncios no ChatGPT** — teste iniciado nos EUA **9-fev-2026**; só Free e ChatGPT Go (Plus/Pro/Business/Enterprise/Edu sem ads); rótulo "Sponsored" **abaixo** da resposta. **ChatGPT Ads Manager** self-serve aberto 5-mai-2026 (CPC US$ 3–5; CPM US$ 25–60).
- **GPT-5.5** (abr/2026); GPT-5.5 Instant virou default.
- **Instant Checkout** (29-set-2025, Agentic Commerce Protocol + Shared Payment Token; Etsy/Shopify).

### 5.3 Agentic shopping (guerra de agentes de compra)
- **Amazon** descontinuou Rufus → **"Alexa for Shopping"** (~13-mai-2026); "Buy for Me" + Shop Direct (100M produtos, 400k+ merchants, 11-mar-2026).
- **Perplexity** "Instant Buy" com PayPal (25-nov-2025).
- → *auditoria GEO inclui elegibilidade em fluxos de compra agêntica, não só citação textual.*

### 5.4 Zero-click
- **SparkToro** (8-jun-2026): **68,01%** das buscas US sem clique (jan–abr/2026, vs 60,45% em 2024); AIO em >20% reduz CTR ~60%; **AI Mode = 0,34%** das buscas. *Nota: base 2024 do SparkToro mudou de painel (Datos→Similarweb) — não comparar séries diretamente.*

### 5.5 Controle de crawler — llms.txt vs AIPREF (correção)
- **llms.txt:** adoção **10,13%** (SE Ranking, 300k domínios, mar/2026) e **ZERO correlação** com frequência de citação; Limy.AI: só 408 requisições a `/llms.txt` em 515M eventos de bots em 90 dias (os bots ignoram). Google **rejeitou** (Illyes: "no plans to support"; Mueller comparou a meta keywords).
- **IETF AIPREF:** `draft-ietf-aipref-vocab` v06 **ativo** (atualizado 27-28 abr/2026, milestone standards-track ~ago/2026); `draft-ietf-aipref-attach` v04 (28-out-2025, expirado/arquivado) define header HTTP **`Content-Usage`** + diretiva `Content-Usage` no robots.txt (atualiza RFC 9309). **Correção:** o draft atual **NÃO** especifica `/.well-known/ai-preferences` — esse endpoint era uma suposição; o mecanismo escolhido é header + robots.txt.
- **Matriz de bots 2026:** OpenAI (GPTBot/OAI-SearchBot/ChatGPT-User), Anthropic (ClaudeBot/Claude-User/**Claude-SearchBot**, doc atualizada fev/2026), Google-Extended, PerplexityBot/Perplexity-User, Meta-ExternalAgent/Fetcher. Bloqueio na Cloudflare (abr/2026): GPTBot 5,20% · CCBot 5,14% · ClaudeBot 4,59%. Cloudflare reportou IA agêntica em 57,5% do share de bots (5-jun-2026).

---

## 6. Frameworks práticos de execução (praticantes, 2026)

- **Relevance Engineering (Michael King / iPullRank)** — disciplina-guarda-chuva (IR + UX + IA + estratégia de conteúdo + PR digital); **"The AI Search Manual"** (24 capítulos + prompt recipes/templates). Componentes: passage-level optimization (conteúdo "chunkable"), multimodalidade, **query fan-out**, candidate passages, mentalidade "raffle ticket" (cada passagem é um bilhete de rifa para ser a citada).
- **Aleyda Solis — "3-Layer Framework"**: Camada 1 **Presence** (prompt coverage, recommendation rate, linked citation rate), Camada 2 **Readiness** (accessibility, extractability, credibility), Camada 3 **Business Impact** (AI-referred sessions, conversion, branded search lift). Deck "Winning organic in 2026" (4-jun-2026): topical completeness > keyword targeting; brand authority/trust como sinal de ranking.
- **Bernard Huang (Clearscope) — "Dual System"**: rankings tradicionais + respostas de IA; AEO = tornar-se **interpretável**, não rankear alto; "Conversational Discoverability", "long long tail", topical depth/breadth, AI citability.
- **Lily Ray — freio de qualidade**: táticas populares de GEO tratadas como **spam** por Google/Microsoft (prompt injection "summarize with AI", scaled content em listicles/comparações programáticas) → risco de penalidade algorítmica. *Guardrail obrigatório no briefing dos escritores.*

**Loop operacional canônico (refinado):** OBSERVAR (medir SoV/citation/answer inclusion por prompt) → **DIAGNOSTICAR** (por que a página não é citada — taxonomia AgentGEO) → **REPARAR** (intervenção cirúrgica em ~5% do conteúdo: estrutura, evidência datada, entidade) → **MEDIR** (re-coleta e lift). Produzir menos, diagnosticar e reparar mais (`2603.09296`).

---

## 7. Aplicação por repositório (premissas enriquecidas)

### 7.1 `landing-page-geo` (alexandrecaramaschi.com + portais)
- **Rubrica de redação HBR** ganha três eixos estruturais de `2603.29979` (macro/meso/micro) e o gatilho de `2605.25517`: relevância tópica forte + **timestamp/recência visível** + especificidade (números). *Answer capsule* de 40–80 palavras no topo de cada seção-resposta.
- **Auditoria on-page** passa a medir **dois eixos** (`2606.12439`): retrievability (somos recuperáveis? — schema, semantic HTML, crawlability, chunk autocontido) e ranking impact (somos usados? — evidência, entidade, autoria).
- **Schema/llms.txt:** manter llms.txt como defensivo (correlação zero com citação — não vender como alavanca); priorizar Structured Data + Semantic HTML + Freshness (GEO-16). Preparar trilha AIPREF (`Content-Usage` em robots.txt) sem prometer `/.well-known/ai-preferences`.
- **API IndexNow / sitemap:** inalterado; reforço de que ranquear no top-10 orgânico ainda é pré-condição de citação no AIO (seoClarity 99%).
- **Guardrail anti-spam (Lily Ray):** proibido prompt injection e scaled content programático; engenharia de relevância legítima apenas.

### 7.2 `papers` (alexandrebrt14-sys/papers + papers-wiki)
- **Ingestão prioritária** dos IDs verificados de §1: `2606.12439`, `2605.25517`, `2605.29107`, `2603.29979`, `2603.09296`, `2605.12887`, e os de RAG/chunking (`2603.06976`, `2601.15457`, `2605.01664`, `2604.04936`). Marcar `2602.02961` como caso de produto.
- **Anti-GhostCite:** todo paper entra com link `arxiv.org/abs/<id>` e status de verificação; nunca canonizar ID não aberto via WebFetch. Registrar que o `sonar-deep-research` chegou a **inventar IDs** (`2603.04567`, `2605.11203` etc. — não verificados) — exemplo didático de alucinação de citação.
- **Eixo de leitura:** organizar por (a) frameworks de execução, (b) medição/KPI, (c) recuperação/chunking, (d) riscos/manipulação (`2605.29107` + `2606.12439`).

### 7.3 `curso-factory` (curso/educação GEO)
- **Módulo de medição:** ensinar a taxonomia corrigida (SoV / Answer Inclusion Rate / Citation Rate; "Share of Answer" não é termo técnico) e a leitura crítica de benchmarks (RCT vs estudo observacional vs vendor claim; sempre nomear metodologia).
- **Módulo técnico (vetorial/semântico):** o pipeline de 4 estágios (§2) como base conceitual; exercícios de answer capsule, chunking semântico e cobertura de fan-out.
- **Módulo de ferramentas:** mapa atualizado do vendor stack (§4) com a ressalva de que cada SoV não é comparável entre fornecedores; Microsoft Clarity AI Citations como porta de entrada grátis.
- **Parágrafos sempre justificados** (regra do repo) e acentuação PT-BR completa, inclusive em sub-agents de geração longa (carimbar `COPY_PROMPT_PREFIX.md`).

---

## 8. Correções ao corpus canônico anterior (anti-drift — REVOGAM fatos prévios)

1. **"Profound Index 400M" estava impreciso.** O **Profound Index** existe (lançado **5-nov-2025**) e é o visibility score semanal. Os **400M+** pertencem ao **Conversation Explorer** (conversas reais), não a um "índice de 400M". Corrigir `project_geo_wave_junho_2026` e o doc da 1ª passada.
2. **"Share of Answer" não é KPI normalizado.** Nenhum fornecedor de 2026 o usa como termo formal. Usar AI Share of Voice + Answer Inclusion Rate + Prompt Coverage. (Revoga a "separação canônica SoV vs Share of Answer" da 1ª passada de 15-jun.)
3. **AIPREF não usa `/.well-known/ai-preferences`.** O mecanismo é header HTTP **`Content-Usage`** + diretiva no **robots.txt** (`draft-ietf-aipref-attach`). Remover qualquer recomendação de criar `/.well-known/ai-preferences`.
4. **Ahrefs Brand Radar = 376M+ prompts** (não "199M"). O 199M era número antigo; a página oficial atual reporta 376M+. *Cuidado:* há divergência 199M/239M/250M/376M entre fontes — citar sempre 376M+ com a data 15-jun-2026.
5. **Semrush NÃO é subsidiária da Adobe** (erro provável de leitura de WebFetch numa frente). É NYSE: SEMR, independente. Não tratar como fato.
6. **GEO-16 (`2509.10762`) e "How to Dominate" (`2509.08919`) são de set/2025**, não 2026 — datar corretamente ao citar.

---

## 9. Fontes primárias verificadas (seleção)

**Papers:** arxiv.org/abs/{2606.12439, 2605.25517, 2605.29107, 2603.29979, 2603.09296, 2605.12887, 2602.02961, 2509.10762, 2509.08919, 2603.06976, 2601.15457, 2605.01664, 2604.04936}.
**Fornecedores:** fortune.com/2026/02/24 (Profound C); siliconangle.com 24-02-2026; ahrefs.com/blog/most-cited-domains-ai-overviews (1-jun-2026); semrush.com/news/460693 (MCP Perplexity, 3-jun-2026); sitecore.com/.../sitecore-acquires-scrunch (3-jun-2026); sifted.eu/.../peec-ai-raises-21m; tryprofound.com/blog/introducing-profound-index; learn.microsoft.com/clarity/ai-visibility/ai-citations (13-mai-2026).
**Impacto/medição:** searchenginejournal.com/.../ai-overviews-cut-organic-clicks-38 (RCT); seerinteractive.com/.../aio-impact-2026-update; pewresearch.org/short-reads/2025/07/22; seoclarity.net/research/ai-overviews-impact; conductor.com/academy/aeo-geo-benchmarks-report; sparktoro.com/blog/in-2026-less-than-one-third (8-jun-2026).
**Produto/algoritmo:** blog.google/.../google-io-2026-all-our-announcements; blog.google/.../sundar-pichai-io-2026; techcrunch.com/2026/01/27 (follow-up AIO→AI Mode); flyweel.co/blog/openai-launches-chatgpt-ads; cnbc.com/2026/05/13 (Alexa for Shopping).
**Crawler/AIPREF:** seranking.com/blog/llms-txt; datatracker.ietf.org/doc/draft-ietf-aipref-vocab; datatracker.ietf.org/doc/draft-ietf-aipref-attach; openshadow.io/guides/ai-bot-user-agents-2026.
**Praticantes:** ipullrank.com/ai-search-manual; aleydasolis.com/.../3-layer-framework; clearscope.io/blog/2026-seo-aeo-playbook; ppc.land/lily-ray-... (14-mai-2026).
**Pipeline técnico:** openai.com/index/introducing-chatgpt-search; leapd.ai/blog/ai-visibility/how-chatgpt-google-ai-overviews-and-perplexity-source-information-in-2026.

> Raws de pesquisa: Perplexity `sonar-pro` em [`raw/P1..P7.json`](raw/) (com `citations` e `search_results`); relatórios dos sub-agentes Claude consolidados neste documento (§1–§6).
