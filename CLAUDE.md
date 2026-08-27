# CLAUDE.md — Papers (refatorado 2026-04-19)

## REGRA #0 — IDIOMA
Todo conteúdo em PT-BR com acentuação completa. Exceção: código, commits, docstrings técnicas (inglês acadêmico).

## REGRA #1 — Contexto enriquecido GEO 2026 (mandatório)

Em **toda** decisão metodológica (escolha de dataset, framing de paper, definição de métrica estatística, escolha de conference de submissão, prompt portfolio de validação): ler primeiro [`docs/GEO_KNOWLEDGE_BASE_2026.md`](docs/GEO_KNOWLEDGE_BASE_2026.md) e [`docs/GEO_OPERATING_SYSTEM.md`](docs/GEO_OPERATING_SYSTEM.md).

- **KB (~21 KB)** consolida estado da arte 2025-2026 adaptado ao repo papers: papers fundadores GEO (Aggarwal SIGIR 2023 arXiv:2311.09735, Chen arXiv:2509.08919, Yao EMNLP 2025), datasets benchmark (GEO-bench, AI-citation-bench, MentionGen), metodologias estatísticas canônicas (n mínimo, IC, replicação inter-LLM), top conferences (SIGIR, ACL, EMNLP, KDD, WWW, ECIR), tooling open source (AthenaHQ public, Peec API). **§11 é a aplicação específica deste repo.**
- **OS (~24 KB)** é o playbook operacional alinhado a calendário de submissões: cadência diária (coleta + cache), semanal (review estatístico), mensal (preprint draft), trimestral (submission window). KPIs estatísticos (n por vertical, intervalo de confiança, pré-registro OSF). Prompt portfolio para validar replicabilidade do dataset.
- **Pesquisa bruta** em [`docs/research/geo-knowledge-2026/`](docs/research/geo-knowledge-2026/) (Perplexity sonar-pro com citações reais).

**Incremento Q2 2026 (17-05-2026)** — adiciona ao KB/OS sem substituir:
- [`docs/research/geo-q2-2026/GEO_KNOWLEDGE_2026_Q2_INCREMENT.md`](docs/research/geo-q2-2026/GEO_KNOWLEDGE_2026_Q2_INCREMENT.md) — doc canônico específico deste repo de pesquisa (sumário executivo, mudanças metodológicas Q1-Q2 2026, novos papers a integrar no pipeline arXiv, novos critérios de scoring, preregistration, 7 artefatos a produzir). Gerado por Claude Opus 4.7 sobre síntese Gemini 2.5 Pro de 5 Perplexity sonar-pro + 5 sonar-deep-research + 1 GPT-4o web_search.
- [`docs/research/geo-q2-2026/SYNTHESIS_STATE_OF_ART_2026.md`](docs/research/geo-q2-2026/SYNTHESIS_STATE_OF_ART_2026.md) — síntese geral (estado da arte, 8 seções, papers AgenticGEO/AdaptOrch/MoA/DAAO/CASTER, frameworks evaluation BiGGen-Bench/GEO-Bench/Arena-Hard, métricas GEO 2026).
- [`docs/research/geo-q2-2026/CITATIONS_POOL.md`](docs/research/geo-q2-2026/CITATIONS_POOL.md) — **325 URLs verificáveis** (arXiv IDs prioritários para ingestão).
- [`docs/research/geo-q2-2026/raw/`](docs/research/geo-q2-2026/raw/) — 10 JSONs originais das waves.

**Wave Maio 2026 Pós-IO (24-05-2026)** — adiciona aos anteriores sem substituir:
- [`docs/research/geo-wave-maio-posio-2026/WAVE_MAIO_2026_POSIO_CANONICAL.md`](docs/research/geo-wave-maio-posio-2026/WAVE_MAIO_2026_POSIO_CANONICAL.md) — **doc canônico de 511 linhas** cobrindo delta 17-mai → 24-mai-2026 com foco metodológico-acadêmico: (a) 6 novos arXiv IDs prioritários para ingestão (2604.25707 Citation Selection→Absorption framework dual-stage, 2603.09296 7-type failure taxonomy, 2604.03656 Semantic Entropy Drift, 2509.08919 v2, 2603.10913 LLM2Vec-Gen, 2508.21038 ICLR'26 limites teóricos embeddings); (b) **AutoGEO ICLR'26** (Wu/Zhong/Kim/Xiong CMU, +50,99% lift, github.com/cxcscmu/AutoGEO) — replicar em PT-BR como preprint ECIR 2027; (c) novos campos de schema SQLite (`citation_selection_rate`, `citation_absorption_rate`, `failure_type` enum, `semantic_entropy_drift`); (d) novo módulo `src/collectors/failure_classifier.py` (taxonomia 7 tipos); (e) glossário CAR vs CSR como métricas distintas com fonte primária; (f) **Profound 27M citation dataset** (owned-content só 4,3% global); (g) convergência cross-disciplina (GEO + RAG + citation patterns + vector retrieval) — pre-registro Q3/2026 deve declarar hipóteses cross-camada; (h) 3 camadas de KPI (Visibilidade → Infraestrutura → Negócio) — Camada 2 é a menos explorada cientificamente; (i) **24 URLs verificáveis** adicionais. Inclui apêndice §10 com achados complementares do orchestrator 5 LLMs (raw em [`raw/orchestrator_5llm_20260524_213700.json`](docs/research/geo-wave-maio-posio-2026/raw/orchestrator_5llm_20260524_213700.json)). **§6.2 é a aplicação específica deste repo** (5 entregáveis 60 dias, métrica de sucesso preprint AutoGEO-PT-BR no arXiv com IC 95% para lift até 23-jul-2026).

**Wave Junho 2026 (07-06-2026)** — adiciona aos anteriores sem substituir:
- [`docs/research/geo-wave-junho-2026/GEO_WAVE_JUNHO_2026_CANONICAL.md`](docs/research/geo-wave-junho-2026/GEO_WAVE_JUNHO_2026_CANONICAL.md) — **doc canônico (300 linhas)** cobrindo o delta 03-jun → 07-jun, gerado pelo orchestrator 5 LLMs (4 deep-research Perplexity + 1 board). Foco metodológico-acadêmico: (a) **framework de 5 camadas de medição de GEO** (captura de canal → logs/crawlers → SOV + interrogação estruturada → pipeline influenciado por IA → difference-in-differences) — esqueleto do prompt portfolio camada 3b; (b) **5 papers novos GEO/AEO** para ingestão: `2509.10762` (GEO-16/GEO score G, 70 prompts→1.702 citações→1.100 URLs), `2605.25517` (What Gets Cited, 252k experimentos RAG pareado, fatores-gatekeeper — **verificado via WebFetch**), `2605.12887` (EcoGEO, trajetória de evidências — **verificado**), GEO-Bench (ID a confirmar), GEO–GEU; (c) **~25 papers da camada semântica/vetorial** (chunking `2603.06976`/SemRAG, dense retrieval LREM, reranking, semantic entropy `2508.14496`, embeddings de entidade `2508.10003`/`2509.04011`) — base técnica de recuperabilidade; (d) detalhamento do dataset `geo-citation-lab` (602 prompts, 72 features) de `2604.25707` para desenho de CSR×CAR; (e) hierarquia de KPIs com metodologia formal (Microsoft Clarity Citation Rate, AIO×AI Mode 13,7% overlap). **§7.2 é a aplicação específica deste repo** (5 entregáveis: campos CSR/CAR + influência por página, prompt portfolio camada 3b por plataforma, ingestão dos 4 papers tagueados, fatores-gatekeeper como hipóteses PT-BR falsificáveis, GEO-16 como variável de controle). Raw em [`raw/`](docs/research/geo-wave-junho-2026/raw/).

**Wave Junho 15 2026 (15-06-2026)** — adiciona aos anteriores sem substituir:
- [`docs/research/geo-wave-junho-15-2026/GEO_WAVE_JUNHO_15_2026_CANONICAL.md`](docs/research/geo-wave-junho-15-2026/GEO_WAVE_JUNHO_15_2026_CANONICAL.md) — **doc canônico**, delta 07-jun → 15-jun, ancorado em pesquisa web verificada ao vivo (WebSearch/WebFetch jun/2026) + orchestrator 5 LLMs no fundamento técnico atemporal (§5). Foco metodológico-acadêmico: (a) **2 papers verificados via WebFetch para ingestão** — `2603.29979` (GEO-SFE, Yu/Yang/Ding/Sato 31-mar-2026; estrutura em macro/meso/micro; +17,3% citation rate, +18,5% qualidade em 6 motores) e `2603.09296` (AgentGEO, Tian et al. 10-mar-2026; diagnóstico-reparo de falha de citação; +40% citação modificando 5% do conteúdo vs 25% baseline — reconcilia a antiga referência "taxonomia de 7 tipos de falha"); (b) **novo KPI Share of Answer vs Share of Voice** (estar na lista de fontes ≠ ser a resposta) + bateria consolidada (Answer Inclusion Rate, Recommendation Rate, Prompt Coverage, Assisted Click Yield); (c) **benchmarks de impacto** — RCT de AIO (-38% cliques, UX inalterada, jan-fev/26) e Seer 2026 (citado em AIO = +120% cliques/impressão) como hipóteses de negócio falsificáveis; (d) os 3 níveis estruturais de GEO-SFE como **variáveis de controle** mensuráveis na coleta, correlacionadas com taxa de citação por vertical. **§7.2 é a aplicação específica deste repo** (ingestão de `2603.29979`/`2603.09296` tagueados contra Conceitos 11/13/15/24/25 e CSR/CAR; features macro/meso/micro no schema; campo Share of Answer/Recommendation Rate; hipóteses pré-registradas do lift AgentGEO e do RCT de AIO; nota no METHODOLOGY de que "deep research" sem busca live fabrica citações). Raw do orchestrator em [`raw/`](docs/research/geo-wave-junho-15-2026/raw/).

**Wave Junho 15B 2026 (15-06-2026, 2ª passada)** — adiciona aos anteriores; foco de ingestão acadêmica:
- [`docs/research/geo-wave-junho-15b-2026/GEO_WAVE_JUNHO_15B_2026_CANONICAL.md`](docs/research/geo-wave-junho-15b-2026/GEO_WAVE_JUNHO_15B_2026_CANONICAL.md) — **doc canônico**, pesquisa viva cruzada (Perplexity `sonar-pro` com `citations`/`search_results` reais — raws `P1..P7.json` — + WebSearch/WebFetch do Claude verificando `arxiv.org/abs/<id>` página a página). **Papers novos para ingestão prioritária (§1, todos verificados via abs):** `2606.12439` (Wen et al., ICML 2026 Position Track, 18-mai — formaliza GEO como otimização conjunta de **retrievability** × **ranking impact**, via *retrieval booster* e *ranking shifter messages*); `2605.25517` (What Gets Cited, 252k trials, 6 LLMs — relevância tópica + posição na lista + preço/timestamp explícitos = preditores; formatação cosmética rende pouco); `2605.29107` (GEO-Bench, cs.CR — reescrita black-box iguala/supera ataques gradient-based e evade detecção por perplexidade); RAG/chunking: `2603.06976` (Paragraph Group Chunking lidera, nDCG@5≈0,459; fixo-por-caractere é fraco), `2601.15457` (rerank → faithfulness 0,797 vs 0,621), `2605.01664` (híbrido+rerank Cohere, 100% grounding), `2604.04936` (W-RAC, custo de chunking −1 ordem de magnitude). Marcar `2602.02961` (Pinterest GEO/VLM) como caso de produto, não benchmark. **Anti-GhostCite reforçado:** o `sonar-deep-research` chegou a **inventar IDs** (`2603.04567`/`2605.11203` — NÃO verificados); regra: nunca canonizar ID sem abrir o `abs` via WebFetch. **§7.2 = aplicação deste repo** (ingestão dos IDs por eixo: frameworks de execução / medição / recuperação-chunking / riscos-manipulação; cada paper entra com link abs + status de verificação). **CORREÇÕES (§8):** GEO-16 `2509.10762` e "How to Dominate" `2509.08919` são de **set/2025** (não 2026); "Share of Answer" não é KPI normalizado; Profound Index existe (5-nov-2025) e os 400M são do Conversation Explorer. Raws + proveniência em [`raw/`](docs/research/geo-wave-junho-15b-2026/raw/).

**Wave Junho 19 2026 (19-06-2026)** — adiciona aos anteriores sem substituir (sincronizada dos repos irmãos em 14-07):
- [`docs/research/geo-wave-junho-19-2026/GEO_WAVE_JUNHO_19_2026_CANONICAL.md`](docs/research/geo-wave-junho-19-2026/GEO_WAVE_JUNHO_19_2026_CANONICAL.md) — **doc canônico delta** mai–19/jun: (a) **Google oficializa "GEO para Search é SEO"** — guia de AI optimization do Search Central (15-mai/15-jun) revela **RAG + query fan-out** e lista **5 táticas "não precisa fazer"** (llms.txt, markup-p/-IA, chunking, reescrita-p/-IA, overfoco em structured data); (b) **estudos causais Ahrefs** — schema não move citação em IA (1.885 páginas diff-in-diff: AIO −4,6%) e **97% dos llms.txt nunca recebem requisição** (137k domínios); (c) infra de medição — GA4 canal "AI Assistant", GSC AI reports (impressão, sem CTR); (d) papers `2605.12887` EcoGEO e `2605.21948` SCI-Defense; (e) série AWR/Fiorelli (4 pilares Retrieval/Reasoning/Agency/Authority + 4 camadas de execução). **§7 = desmistificações que revogam clichês** ("schema +67%", "llms.txt aumenta citação", "Reddit nº 1 fixo", "um prompt = um ranking"). Para este repo: os estudos causais são o padrão-ouro metodológico a replicar em PT-BR; medição exige múltiplas execuções e média de mention rate.

**Wave Julho 2026 (14-07-2026)** — adiciona aos anteriores sem substituir; **inclui uma revogação de correção da 15B**:
- [`docs/research/geo-wave-julho-2026/GEO_WAVE_JULHO_2026_CANONICAL.md`](docs/research/geo-wave-julho-2026/GEO_WAVE_JULHO_2026_CANONICAL.md) — **doc canônico delta** 19-jun → 14-jul, 6 rodadas em 4 provedores cloud (Perplexity ×2, OpenAI, Anthropic, xAI) + doublecheck Claude em fonte primária. Núcleo: (a) **§7.1 REVOGA a correção §8.5 da 15B** — a Adobe **concluiu** a compra da Semrush (anúncio 19-nov-2025, US$ 1,9 bi; fechamento final de abr/2026; press release + 8-K verificados); (b) **Semrush AI Visibility Index 2026 expandido** (26-jun; 126 mi prompts EUA jan–abr; ChatGPT ~15 fontes/resposta vs Gemini ~3; só 36 marcas no top-100 das 4 plataformas); **81% vs 36%** (integração SEO+GEO vs separado); (c) **Ahrefs Brand Radar abre metodologia** (PAA + fan-out semântico, 5 engines, limitações declaradas — baseline de transparência para os 3 papers-alvo) + correlatos em 75k marcas (menções↔AIO r=0,664; YouTube = correlato nº 1 cross-engine); (d) **Profound 6,8 mi citações**: padrões por engine (Gemini 52,15% owned; ChatGPT 48,73% terceiros; Perplexity reviews); (e) **concentração de referral** (Previsible/SEL jul-26: ChatGPT 92,4%; Claude cresceu 64x e ultrapassou Perplexity em mar-26); conversão por vertical (faixa 1,3x–23x — §7.3 proíbe "4–5x" como constante); (f) **§5 funil vetorial mensurável** (`similarity → hit rate@k → rerank survival → citation share`, 7 métricas operacionais) — operacionaliza a Camada 2 (Infraestrutura), a menos explorada cientificamente; (g) §4 framework de execução consolidado (workflow 7 etapas, 10 papéis, cadência, 5 gates, report de 8 perguntas). **§8.1 = aplicação deste repo** (hipóteses H-a/H-b/H-c pré-registráveis; campo `citation_style` por engine no schema; ponderação do painel por share de referral). §7.2 refuta 2 alucinações do Grok (rodada xAI = sinal qualitativo apenas). Raws em [`raw/`](docs/research/geo-wave-julho-2026/raw/).
- [`docs/research/geo-wave-julho-22-2026/GEO_WAVE_JULHO_22_2026_CANONICAL.md`](docs/research/geo-wave-julho-22-2026/GEO_WAVE_JULHO_22_2026_CANONICAL.md) — **doc canônico delta** 14-jul → 22-jul, foco no CORPUS CIENTÍFICO: **32 papers arXiv verificados** (existência+abstract via API, XMLs em raw/; PDFs não lidos — ler antes de citar em copy/paper). Núcleo: (a) **survey crítico `2607.14035`** (45 estudos): GEO é pipeline estocástico; "nenhuma técnica demonstra efeito causal estável cross-plataforma sobre descobribilidade orgânica" (abstract textual) → antídoto contra promessa inflada; adota o **vetor de visibilidade em 4 camadas** (descobribilidade/citação/absorção/resultado); (b) **medição**: visibilidade como DISTRIBUIÇÃO com N execuções (`2604.07585`; mínimos: N≥5 monitoramento, N≥30 pré/pós), **controle on-domain** para descontar tailwind da plataforma (`2606.04362`: glasp 5,7x bruto vira 1,63x na razão e 1,82x no modelo; placebo p=0,16), **seleção ≠ absorção de citação** (`2604.25707`: ChatGPT cita menos com mais influência; rubrica mensal de absorção no §2.4), escada de estatura de marca (`2606.20065` Ranqo: global 73% / mid 44% / nicho 11%; listicles best-of ~21% das citações; sentimento flipa 6,7x mais que menção); (c) **alavancas com evidência** (§3, em ordem): relevância+posição no contexto (`2605.25517`, 252k trials), evidência extraível, preço explícito e data com atualização substantiva, estrutura 3 níveis (+17,3% citação, `2603.29979`), perfil documento-nível (`2604.19113`), portfólio de queries (`2601.13938`); formatação pura tem efeito pequeno; (d) **fronteira agêntica** (§4): diagnóstico ANTES de reescrita (`2603.09296`: +40% mudando 5% do conteúdo), skills por motor com validação causal (`2604.19516`), sites **agent-ready** (`2607.12056`: 89,3% vs 49,3% de sucesso de agente), horizonte pós-citação DAH (`2604.03656`); (e) **defesas e governança** (§5): SCI-Defense e afins classificam autoridade fabricada/comparativos/alegações temporais como manipulação (propostas acadêmicas, não implementação confirmada dos motores) → GEO agressivo tem prazo de validade; `2601.00912` (Discovery Gap): scores GEO não predizem descoberta, SEO tradicional sim → confirma "GEO = camada sobre SEO sólido"; (f) **indústria pós-14-jul** (§6): Brand Radar 406M+ prompts (atualiza ~340M), Ahrefs CTR −58% vs esperado (bruto ~79% em 2 anos, parte secular), seoClarity: ChatGPT REDUZIU citações externas desde mar/26 (janela AEO estreitando), Conductor AgentStack (apps LLM+MCP), llms.txt: 97% dos arquivos com zero requisição de IA; (g) **§7.4 NOVA regra de precedência epistemológica intra-wave** (7 níveis de fonte; níveis 6-7 nunca canonizam número sozinhos). Precedência entre waves: **Julho-22 §7 > Julho §7 > Wave 19 §7 > 15B §8**. **§8.1 = aplicação neste repo** (lista-mestre = related work vivo dos 4 papers; `2606.20065` e `2604.25707` são os comparáveis diretos do nosso desenho; METHODOLOGY_V2 incorpora distribuição+IC e discute controle on-domain como limitação declarada; lacuna publicável: nenhum dos 32 cobre PT-BR/Brasil — escopo arXiv apenas; anti-GhostCite: reabrir abs antes de canonizar). Crítica GPT-5.5 (65 pontos) aplicada; raws em [`raw/`](docs/research/geo-wave-julho-22-2026/raw/).
- [`docs/research/geo-wave-julho-22b-2026/GEO_WAVE_JULHO_22B_2026_CANONICAL.md`](docs/research/geo-wave-julho-22b-2026/GEO_WAVE_JULHO_22B_2026_CANONICAL.md) — **doc canônico delta** (22-jul): INFRAESTRUTURA de GEO — crawlers, controle de acesso e atribuição, aterrado em docs oficiais acessadas em 22-jul-2026. Núcleo: (a) **matriz de crawlers por finalidade** (§2.1: treino=GPTBot/ClaudeBot/Google-Extended-token; busca=OAI-SearchBot/Claude-SearchBot/PerplexityBot; ação de usuário=ChatGPT-User/Claude-User/Perplexity-User, e estes dois últimos podem ignorar robots.txt por doc oficial); default Brasil GEO = liberar tudo, matriz restritiva só p/ conteúdo sensível, com linha EXPLÍCITA de Google-Extended; (b) **§7 REVOGA do corpus** o claim "bloquear Google-Extended remove de AIO" — AIO/AI Mode usam o Googlebot NORMAL (doc oficial); exposição em AIO gerencia-se com nosnippet/max-snippet/noindex; (c) **GA4**: canal default "AI Assistants" (medium ai-assistant; EXCLUI AIO/AI Mode que seguem em Organic Search; Perplexity ausente da lista em 22-jul) + custom channel group com regex ANCORADA (§4.1) + convenção utm_medium=ai-assistant; (d) **dark traffic**: ~70,6% das visitas de IA chegam sem referrer [vendor Loamly] → GA4 é o PISO do canal, declarar em todo report; (e) **crawl-to-referral** como métrica de troca justa (Anthropic ~70.900:1 em jun/2025; painel vivo radar.cloudflare.com/ai-insights prevalece); (f) Cloudflare: Content Signals Policy, AI Crawl Control, e POLÍTICA ANUNCIADA de bloqueio default Training/Agent em páginas com anúncios (15-set-2026, novos domínios CF); (g) **claims machine-readable com validade** (§6, novo padrão). **§5.2 = aplicação neste repo** (caso Cloudflare×Perplexity e ratios como material de economia da atribuição; distinção treino/busca/usuário como variável de confusão em experimentos de acesso).
- [`docs/research/geo-wave-julho-22c-2026/GEO_WAVE_JULHO_22C_2026_CANONICAL.md`](docs/research/geo-wave-julho-22c-2026/GEO_WAVE_JULHO_22C_2026_CANONICAL.md) — **doc canônico delta** (22-jul): BRASIL + regulatório + segurança agêntica. Núcleo: (a) **Brasil primeira linha**: Modo IA pt-BR desde 08-set-2025 (primária Google BR); UCP/checkout no AI Mode reportado desde 19-mai-2026 [imprensa; primária pendente]; 3º maior usuário de ChatGPT [vendor via secundária]; Datafolha 93% usam IA MAS inclui IA embutida (não equivale a busca por IA); delegação de compra a agentes ainda 15%; (b) **mapa imprensa×IA**: Estadão×Google (dez/25), Folha×Google, Folha+UOL×OpenAI (25-mai-26); frente ANJ+Abert+Aner; CADE em fase avançada [classe processual a confirmar] — efeito dos acordos sobre citação é HIPÓTESE testável, não fato; (c) **regulatório com vetos**: PL 2338 NÃO aprovado (nunca citar como lei; reavaliar trimestral); CONAR = corresponsabilidade AUTORREGULATÓRIA por conteúdo de IA desde 01-jun-2026; LGPD já rege dados em pipelines; sandbox ANPD não é salvo-conduto; "OWASP LLM Top 10 2026" NÃO existe (vigente = 2025); (d) **segurança agêntica** (§6): prompt injection indireta demonstrada (Comet/Atlas, PoC) E observada in the wild (Unit 42) — checklist "agent-friendly sem virar vetor" (§6.2, 5 itens); Web Bot Auth/Signed Agents = padrão EMERGENTE draft (sinal positivo, nunca bloqueio único); (e) claims machine-readable (§9). **§8.1 = aplicação neste repo** (contexto BR completo para introdução dos papers; hipótese nova monitorável: acordos de licenciamento deslocando citação de Gemini/ChatGPT p/ domínios licenciados — testável na cohort de mídia).

**Wave Agosto 2026 (27-08-2026)** — adiciona aos anteriores e em parte **CORRIGE**; 10 rodadas em 5 provedores com web ao vivo (Perplexity `sonar-pro` ×6 — as 4 `sonar-deep-research` em paralelo deram ReadTimeout aos 25 min —, Gemini 3.1 Pro grounding ×2, OpenAI `gpt-5.5` web_search, xAI `grok-4.6` via Agent Tools API) + doublecheck Claude (5 arXiv de jul–ago na página do arXiv, 30 URLs com sentinela):
- [`docs/research/geo-wave-agosto-2026/GEO_WAVE_AGOSTO_2026_CANONICAL.md`](docs/research/geo-wave-agosto-2026/GEO_WAVE_AGOSTO_2026_CANONICAL.md) — **doc canônico delta** 22-jul → 27-ago: FRAMEWORKS DE EXECUÇÃO, KPIs, REPORT e motores. Núcleo: (a) **o motor escolhe onde buscar antes de buscar** — 16–17% das fan-out queries do ChatGPT com `site:` desde 08-ago [Promptwatch/Willison]; Reddit 12% → 3% no ChatGPT Search [Similarweb 23-ago]; (b) **Google, em doc oficial, ignora `llms.txt`/markup especial e não exige chunking**; Mueller 24-ago: "nothing really special"; fan-out pages para manipular = scaled content abuse; **Preferred Sources (20-ago)** com badge em AIO/AI Mode; goto URLs (26-ago) quebram séries de scraping; **NÃO existe core update de agosto** (só spam 18–20-ago); (c) **ChatGPT Ads no Brasil (11-ago, OpenAI)** + Similarweb AI Ads → report separa orgânico | citação IA | referral | **pago em IA** | conversão (§5.3); (d) **volume de prompt não existe**: Ahrefs "AI adjusted volume" (17-ago, só proxy após 31-ago); Rand 12-ago: análise de citação engana; (e) **Cloudflare 15-set**: Training e Agent bloqueados por default em páginas com ads de domínios novos; (f) **corpus**: GEO-Flag `2608.16824` (detector F1 0,944; 8,90% das páginas recuperadas são GEO-otimizadas, 16,36% em 2026 → anti-padrões 1/5 viram risco mensurável), `2608.13956` (diversidade de documentos > duplicata/paráfrase, experimento controlado), `2606.00898` v2 (métrica de alucinação mede cobertura do grafo), reranker por rubrica `2608.03527`; (g) **framework de execução em 10 etapas** com cadência e papéis (§4) e **"GEO URL Ledger"** de 10 blocos (§5.4) — Conductor Pages Report (23-jul), Semrush ROI direto/assistido/autodeclarado/modelado (27-jul), Profound Index Summer 2026 (1,9 bi conversas; liderança é local em 24/30 indústrias); (h) vendors: Ahrefs 38% overlap AIO×top-10 (era 76%), CTR −58% com AIO, 5,3% do top é 100% IA. **§8 CORRIGE**: `llms.txt` rebaixado a "opcional, nunca entregável/KPI"; AI Mode 1 bi MAU × 0,13% das visitas são medidas diferentes (não compor); Reddit sai dos exemplos; xAI `chat/completions`+`search_parameters` está morto (410 → `/v1/responses`+`x_search`). Raw em [`raw/`](docs/research/geo-wave-agosto-2026/raw/). **§9.2 = aplicação neste repo** (ingestão tagueada de `2608.16824`/`2608.13956`/`2608.03527`/`2608.03487`/`2608.02011`/`2606.00898`v2; toda métrica de citação verificada declara cobertura do índice; coletar `search_queries` do ChatGPT para medir share de `site:` em pt-BR como hipótese pré-registrável; score GEO-Flag como variável de controle; METHODOLOGY registra deep-research paralelo pendurado e migração da API xAI).

Citar `§X.Y` do KB/OS/INCREMENT/WAVE ao tomar decisões. **Em conflito de fato datado, prevalece a wave mais recente nos itens explicitamente marcados como correção (Agosto (§8 — `llms.txt` rebaixado, AI Mode 1 bi MAU × 0,13% visitas não se compõem, Reddit fora dos exemplos, core update de agosto inexistente, API xAI) > Julho §7 > Junho-19 §7 > 15B §8); fora desses itens, o corpus anterior permanece válido.** Atualizar trimestralmente (ciclo de submissão).

## REGRA #2 — Taxonomia canônica de 50 conceitos GEO/SEO 2026 (classificação obrigatória)

[`docs/GEO_50_CONCEITOS_CANONICAL.md`](docs/GEO_50_CONCEITOS_CANONICAL.md) é o **dicionário obrigatório de classificação** ao catalogar paper acadêmico, análise de fonte, ou produção de research neste repo. 14 eixos, 50 conceitos numerados, anti-padrões proibidos (pseudo-GEO, schema inflado, llms.txt como talismã).

**Mapeamento obrigatório:**

- **Ao resumir um paper** (entrada em `docs/research/` ou ingestão arXiv): tagueá-lo contra os Conceitos **11** (Answer capsules), **13** (Schema.org), **15** (Clareza de entidade), **21** (Referências externas), **22** (Autoria), **24** (Citabilidade GEO), **25** (Recuperabilidade generativa), **30** (llms.txt). Anotar quais o paper cobre, quais ignora, e quais ele desafia.
- **Em pesquisa nova com Perplexity sonar-deep-research**: usar os 50 conceitos como template de checklist da query — incorporar conceitos pertinentes ao tópico para evitar lacunas estruturais comuns em reviews ad hoc.
- **Em prompt portfolio de validação**: garantir que cobertura por vertical toca os 14 eixos (não só os de citação direta).
- **Em pré-registro OSF**: declarar quais conceitos a hipótese testa explicitamente.

Citar `Conceito N — Nome` ao referenciar (ex.: "Conceito 24 — Citabilidade GEO"). Documento revisado trimestralmente em sincronia com KB/OS.

## Propósito

Pesquisa empírica multi-vertical sobre como LLMs citam empresas brasileiras em respostas generativas. Framework de 4 verticais com coortes independentes monitoradas em 5 LLMs. Dataset longitudinal alvo: 6-12 meses para sustentar 3 papers peer-reviewed.

## Arquitetura (2026-04-19)

```
papers/
├── data/
│   ├── papers.db                  # SQLite — source of truth no git (protege pós-incidente 08/04)
│   ├── dashboard_data.json        # artefato para UIs externas
│   └── cache/                     # cache SHA-256 de respostas (não versionado)
├── src/
│   ├── config.py                  # 4 verticais, 5 LLMs, queries, pricing, entidades fictícias
│   ├── cli.py                     # Click CLI — --vertical, --module, --all
│   ├── collectors/                # Módulos de coleta (Onda 7: split aplicado)
│   │   ├── base.py                # Fachada enxuta + re-exports (85 linhas após split)
│   │   ├── llm_client.py          # LLMClient + LLMResponse (extraído Onda 7)
│   │   ├── response_cache.py      # ResponseCache SHA-256 TTL (extraído Onda 7)
│   │   ├── brave_search.py        # BraveSearchClient (extraído Onda 7)
│   │   ├── citation_tracker.py    # Módulo 1: principal, gera linha em citations
│   │   ├── competitor.py          # Módulo 2: benchmark entre verticais
│   │   ├── serp_overlap.py        # Módulo 3: SERP vs IA (Onda 9: toggle ENABLE_SERP_OVERLAP)
│   │   ├── intervention.py        # Módulo 4: A/B testing (estrutura pronta)
│   │   ├── context_analyzer.py    # Módulo 7: sentimento, atribuição, hedging
│   │   ├── drift_detector.py      # Detector de non-stationarity
│   │   └── prompt_sensitivity.py  # Variância por prompt
│   ├── db/
│   │   ├── schema.sql             # Schema SQLite + Supabase
│   │   ├── client.py              # DBClient (INSERTs, migrations)
│   │   └── migrate_*.py           # Migrations versionadas
│   ├── persistence/
│   │   └── timeseries.py          # Módulo 5: daily_snapshots
│   ├── analysis/
│   │   ├── statistical.py         # Módulo 6: 8 testes + effect sizes + corrections
│   │   └── visualization.py       # Charts publicação-ready
│   ├── finops/
│   │   ├── tracker.py             # record_usage → finops_usage
│   │   ├── monitor.py             # dashboards, rollups, alertas
│   │   ├── hooks.py               # integration post-coleta
│   │   └── secrets.py             # rotação de API keys (exploratório)
│   ├── api/
│   │   ├── main.py                # FastAPI endpoints por vertical
│   │   └── models.py              # Pydantic schemas
│   └── logging/
│       └── logger.py              # CollectionLogger (não integrado — TODO)
├── scripts/
│   ├── export_data.py             # CONSOLIDADO (Onda 4) — substitui 3 scripts duplicados
│   ├── generate_report.py         # Markdown diário
│   ├── sync_to_supabase.py        # Replica SQLite → Supabase
│   ├── health_check.py            # Valida coleta; exit 1 trava pipeline (anti-silent-fail)
│   ├── send-report.py             # Email via Resend
│   ├── update-docs.py             # Atualiza docs/STATUS.md
│   └── calibrate_score.py         # Fine-tune de detecção (exploratório)
├── tests/
├── .github/workflows/
│   ├── daily-collect.yml          # 06:00 e 18:00 BRT, job único sequencial
│   ├── weekly-benchmark.yml       # Domingo 05:00 BRT, análise agregada
│   ├── finops-monitor.yml         # Budget check
│   └── security-scan.yml          # Bandit + gitleaks
└── docs/
    ├── ARCHITECTURE.md            # Fluxograma completo (Onda 5)
    ├── METHODOLOGY.md             # Desenho estatístico (auditado)
    ├── REQUIREMENTS.md            # Especificação funcional
    ├── GOVERNANCE.md              # ADRs, roadmap
    ├── STATUS.md                  # Auto-gerado a cada coleta
    ├── MANUAL.md                  # Procedimentos operacionais
    └── audits/                    # Auditorias arquivadas por data
        └── 2026-03-26/            # Primeira auditoria (N=397, histórica)
```

## Verticais e Coortes

**Total: 127 entidades (79 reais BR + 32 âncoras internacionais + 16 fictícias), 4 verticais, 5 LLMs.** Fonte canônica: `src/config_v2.py`. As listas detalhadas abaixo são do cohort v1 (legado) e estão sendo migradas — ver README §Verticals para o roster v2 atual.

### Fintech (21 entidades)
Nubank, PagBank, Cielo, Stone, Banco Inter, Mercado Pago, Itaú, Bradesco, C6 Bank, PicPay, Neon, Safra, BTG Pactual, XP Investimentos
— Internacional: Revolut, Monzo, N26, Chime, Wise
— Fictícias: **Banco Floresta Digital**, **FinPay Solutions**

### Varejo (16 entidades)
Magazine Luiza, Casas Bahia, Americanas, Amazon Brasil, Mercado Livre, Shopee Brasil, Renner, Riachuelo, C&A Brasil, Leroy Merlin, Centauro, Netshoes, Via Varejo, Grupo Pão de Açúcar
— Fictícias: **MegaStore Brasil**, **ShopNova Digital**

### Saúde (16 entidades)
Dasa, Hapvida, Unimed, Fleury, Rede D'Or, Einstein, Sírio-Libanês, Raia Drogasil, Eurofarma, Aché, EMS, Hypera Pharma, NotreDame Intermédica, SulAmérica Saúde
— Fictícias: **HealthTech Brasil**, **Clínica Horizonte Digital**

### Tecnologia (16 entidades)
Totvs, Stefanini, Tivit, CI&T, Locaweb, Linx, Movile, iFood, Vtex, RD Station, Conta Azul, Involves, Accenture Brasil, IBM Brasil
— Fictícias: **TechNova Solutions**, **DataBridge Brasil**

As **entidades fictícias** calibram o false-positive rate: se um LLM "cita" Banco Floresta Digital (que não existe), sabemos o quanto ele alucina nomes plausíveis. Crítico para a metodologia do Paper 1.

## LLM cohort (5 providers, todos obrigatórios)

| LLM | Provider | Modelo | Pricing in/out (USD/MTok) |
|-----|----------|--------|----------------------------|
| ChatGPT | OpenAI | `gpt-4o-mini-2024-07-18` | 0.15 / 0.60 |
| Claude | Anthropic | `claude-haiku-4-5-20251001` | 0.80 / 4.00 |
| Gemini | Google | `gemini-2.5-pro` | 1.25 / 5.00 |
| Perplexity | Perplexity | `sonar` | 1.00 / 1.00 + search |
| Groq | Groq | `llama-3.3-70b-versatile` | 0.59 / 0.79 |

Env var `MANDATORY_LLMS` (defaults a todos os 5) — falha de provider obrigatório dispara fail-loud.

## Pipeline (simplificado)

```
cron (06:00/18:00 BRT)
  → daily-collect.yml
    → for V in [fintech, varejo, saude, tecnologia]:
        citation_tracker   ← 5 LLMs × N queries
        competitor         ← benchmark
        context_analyzer   ← post-processing
        timeseries         ← daily_snapshots
    → sync_to_supabase
    → export_data --format json
    → send-report
    → health_check (exit 1 se validação falhar)
    → git commit data/papers.db + push
```

## Comandos

```bash
# Coleta
python -m src.cli collect --all                              # Tudo
python -m src.cli collect --module citation --vertical fintech

# Análise
python -m src.cli analyze --report
python -m src.cli analyze --visualize

# DB
python -m src.cli db migrate
python -m src.cli db health

# Export (Onda 4 — consolidado)
python scripts/export_data.py --format json
python scripts/export_data.py --format csv --vertical fintech
python scripts/export_data.py --format html
```

## Env vars obrigatórias

Ver `.env.example`. Resumo:
- 5 chaves LLM (OPENAI, ANTHROPIC, GOOGLE_AI, PERPLEXITY, GROQ)
- 2 chaves SERP (BRAVE, SERPAPI — opcional fallback)
- 2 chaves persistência (SUPABASE_URL, SUPABASE_KEY)
- 1 chave notificação (RESEND_API_KEY)

## Convenções de código

- Type hints em todas as funções públicas
- Docstrings em inglês (padrão acadêmico)
- Nomes de variáveis em inglês
- Logs e output CLI em PT-BR com acentuação
- Testes com pytest (parametrizados por vertical quando aplicável)
- Coluna `vertical` obrigatória em todas as tabelas de citação
- Schema migrations em `src/db/migrate_NNNN_*.py` versionadas
- Sem emojis em qualquer conteúdo

## Regras anti-retrabalho

- `papers.db` é **source of truth no git**. Artifact é safety-net apenas.
- Pipeline é **fail-loud**: qualquer vertical falha → exit 1 (protege desbalanceamento de N).
- Entidades fictícias são **parte da metodologia**. Nunca desativar em produção sem publicar os resultados já coletados.
- Auditorias antigas vão para `docs/audits/<data>/` — nunca deletar, nunca usar como source of truth atual.
- `AUDIT_*.txt` na raiz = red flag: deve ser movido para `docs/audits/<data>/` no próximo refactor.


## Plugin Resend Claude Code (instalado 2026-05-28)

`resend@claude-plugins-official` v1.0.0 ativo (escopo user + project). Expõe 5 skills carregadas automaticamente quando o trabalho toca email, templates, deliverability ou inbound:

- `resend:resend` — SDK + gotchas (idempotência, webhook signing, template vars)
- `resend:react-email` — templates HTML via React Email
- `resend:email-best-practices` — SPF/DKIM/DMARC, CAN-SPAM/GDPR/CASL, retry, bounces, complaints
- `resend:agent-email-inbox` — patterns seguros para processar email inbound (sender allowlist, sandbox, content filtering)
- `resend:resend-cli` — flags non-interativas para shell/CI/CD (`--react-email` envia .tsx direto)

MCP server `resend-mcp` lê `RESEND_API_KEY` do env (configurado em `~/.claude/.env`). Para fixes em código que envia email, deixar essas skills acionarem por palavra-chave em vez de reimplementar lógica de retry/auth/headers.

Helper Python canônico para precheck sandbox: `C:/Sandyboxclaude/scripts/python/resend_precheck.py` (porta `landing-page-geo/src/lib/resend-precheck.ts`).

## Padrão editorial obrigatório (doutrina v4, 11/08/2026)

Antes de produzir qualquer texto de leitura humana neste repositório (documentação, onda de pesquisa, síntese, relatório, rascunho de divulgação, descrição de PR, mensagem longa de commit), leia e aplique a cadeia que vive na raiz: `DIRETRIZ_EDITORIAL.md` é a regra (versão 4, de 11 de agosto de 2026), `GUIA_ESCRITA_HUMANIZADA.md` é o anexo prático com exemplos antes e depois, heurísticas mensuráveis e fontes, e `DOUTRINA_EDITORIAL_NESTE_REPO.md` é a tradução da doutrina para o escopo deste pipeline de pesquisa. Os três documentos prevalecem sobre este resumo.

A v4 substituiu a v2, de 23 de julho de 2026, que era construída quase só de proibições e cujo efeito medido foi texto curto e sem argumento aprovado em todos os gates. O que mudou:

- **Piso de substância** (seção 2.1). Toda peça precisa ter tese identificável com a qual daria para discordar, evidência ligada a essa tese, ganho de informação, critério de decisão explícito quando houver alternativas, arco de leitura e consequência prática para quem lê. Peça que falha em um dos seis itens é reescrita, não aparada. Aprovação em gate automático nunca é aprovação editorial.
- **Prova antes da escrita** (seção 2.2). A evidência se levanta antes da primeira frase e limita o tamanho da peça: blocos que afirmam resultado não passam do número de provas datadas disponíveis. Na falta de prova, quatro saídas antes do marcador (pesquisar, reduzir a afirmação, restringir o uso, segurar a publicação), com teto de cinco marcadores abertos por documento.
- **Narrativa obrigatória** (seção 3). Abertura em situação e não em definição, tensão antes da solução, caso condutor com rótulo de tipo, promessa paga no desenvolvimento, fechamento com callback em vez de recapitulação, mostrar em vez de qualificar, e um pedido por peça.
- **Estrutura visual como ferramenta legítima** (seção 6). Tabela comparativa, matriz de decisão e checklist entram sempre que ajudarem de verdade. Sai a lista que faz o trabalho de argumentar.
- **Revisão em três passadas com travas verificáveis** (seção 13), entre elas as quatro conferências que todo símbolo de porcentagem dispara: origem, data, método e denominador na mesma frase. Base pequena se conta em unidades.
- **Nenhuma cota mecânica de ritmo, em direção alguma** (seção 4, item 8). A amplitude num bloco de dez frases é diagnóstico do texto pronto, com defeito abaixo de 15 palavras e conforto acima de 30, e nunca fórmula de produção nem contagem durante a escrita.

Permanecem valendo: português do Brasil com acentuação completa, tipografia à brasileira (sem title case, números de zero a dez por extenso, vírgula decimal), travessão vetado em prosa, atribuição nomeada em vez de "estudos mostram", zero emoji, parágrafos justificados em HTML e PDF, e nada de dado inventado.

Aplicação específica deste repositório, detalhada em `DOUTRINA_EDITORIAL_NESTE_REPO.md`: os prompts de coleta em `src/config.py`, `src/shared/llm_utils.py`, `src/config_v2.py` e `src/collectors/prompt_sensitivity.py` são instrumento de medição da série longitudinal e não recebem regra editorial, porque mudá-los altera o tratamento experimental. Prompt que redige texto em português carrega o bloco condensado de `scripts/prompts/BLOCO_EDITORIAL_PROMPT.md` dentro da própria demanda, já que instrução vista só no contexto não sobrevive a geração longa.

Convenção explícita deste repositório prevalece sobre convenção genérica, com a única ressalva de segurança e corretude.

Sub-agentes que geram texto longo em português recebem o bloco de `scripts/prompts/BLOCO_EDITORIAL_PROMPT.md` carimbado no início do prompt, que é a versão condensada desta cadeia. O prefixo genérico do ecossistema (`C:/Sandyboxclaude/scripts/prompts/COPY_PROMPT_PREFIX.md`) continua servindo para copy de marketing fora deste repositório; aqui a fonte de verdade é a cadeia da raiz, e a passagem anterior que apontava `docs/ESTILO_EDITORIAL.md` do repo GEO-Pesquisador como fonte completa está revogada, porque duas fontes de verdade para a mesma regra é o mesmo que nenhuma.
