# Wave Julho 2026 · Incremento canônico GEO/SEO — pesquisa profunda multi-LLM (19-jun → 14-jul-2026)

> **Data de corte:** 14 de julho de 2026.
> **Status:** **complementa — não substitui** o `GEO_WAVE_JUNHO_19_2026_CANONICAL.md` (19-jun) e todo o corpus anterior. Onde houver conflito de fato datado, **esta passada prevalece** apenas nos itens explicitamente marcados como correção (§7) — incluindo **uma revogação de correção da Wave 15B** (§7.1). Tudo o que a junho-19 canonizou (guia oficial do Google de AI optimization; estudos causais Ahrefs de schema e llms.txt; GA4 "AI Assistant"; GSC AI reports; EcoGEO; SCI-Defense; série AWR/Fiorelli) **permanece válido e não é repetido aqui** — este documento é o **delta** 19-jun → 14-jul-2026, mais duas camadas de síntese técnica (frameworks de execução §4 e física semântico-vetorial §5) que consolidam conhecimento atemporal.
> **Fontes e método (transparência):** pesquisa profunda em **quatro provedores cloud do geo-orchestrator, em seis rodadas paralelas**, orquestrada pelo Claude e cruzada com doublecheck próprio:
> 1. **Perplexity `sonar-deep-research`** (2 rodadas: papers acadêmicos; indústria/vendors) — profundidade com web ao vivo.
> 2. **OpenAI** (1 rodada) — playbook operacional de execução de GEO (workflow, papéis, cadência, gates, report).
> 3. **Anthropic Claude API** (1 rodada) — fundamentos semântico-vetoriais e funil de métricas derivadas.
> 4. **xAI Grok** (1 rodada) — pulso de comunidade; **dois fatos refutados no doublecheck** (§7.2), usado apenas como sinal qualitativo.
> 5. **Google Gemini indisponível** (HTTP 429 — créditos prepagos esgotados; problema conhecido, issue #4 do geo-orchestrator) e **Groq falhou** (HTTP 400 — `max_tokens` acima de 8192 no modelo `llama-4-scout`); registrado no apêndice.
> 6. **Doublecheck do Claude** (WebSearch + WebFetch em fonte primária: news.adobe.com, semrush.com/news, ahrefs.com, arxiv.org/abs) — toda afirmação datada abaixo foi conferida; conflitos isolados em §7.
> Raws preservados em [`raw/`](raw/).
> **Como aplicar:** leitura obrigatória antes de decisões sobre KPI/ferramenta de AI visibility, argumento comercial de integração SEO+GEO, priorização de engine na medição, ou copy que cite conversão de tráfego de IA. §7 revoga um item da 15B e refuta dois boatos de mercado.

---

## 0. Sumário executivo (TL;DR) — o que é NOVO em 19-jun → 14-jul-2026

O período confirma a **consolidação industrial da categoria GEO**: a aquisição da Semrush pela Adobe foi concluída (corrigindo o corpus, que a negava), a Semrush/Adobe publicou o maior estudo de visibilidade em IA já feito (126 milhões de prompts), a Ahrefs abriu a metodologia do Brand Radar, e os dados de tráfego mostram concentração extrema do referral de IA no ChatGPT com ascensão silenciosa do Claude. A tese Brasil GEO sai fortalecida em dois pontos com número novo: **pipeline único SEO+GEO** (81% vs 36% de resultado) e **estratégia distinta por engine** (os padrões de citação de Gemini, ChatGPT e Perplexity são estruturalmente diferentes).

| Achado NOVO (não estava na junho-19) | Número-chave / fonte primária | Impacto canônico |
|---|---|---|
| **Adobe concluiu a compra da Semrush** | Anúncio 19-nov-2025 (US$ 12,00/ação, ~US$ 1,9 bi; `news.adobe.com/news/2025/11/adobe-to-acquire-semrush`); **fechamento final de abril/2026** (8-K da Adobe na SEC; cobertura 29-abr) | **REVOGA a correção §8.5 da Wave 15B** ("Semrush NÃO é subsidiária da Adobe"). Enterprise AIO e AI Visibility Index agora são ativos Adobe; racional declarado: "brand visibility is being reshaped by generative AI". |
| **Semrush AI Visibility Index 2026 expandido** | 26-jun-2026: **126 milhões de prompts** de AI search (EUA, jan–abr/2026), 4 engines; ChatGPT cita **~15 fontes/resposta** vs Gemini **~3**; só **36 marcas** estão no top-100 das 4 plataformas ao mesmo tempo (`semrush.com/news/463141`) | Maior benchmark público de SoV em IA; confirma que visibilidade cross-engine é rara — medir e otimizar **por engine**. |
| **Integração SEO+GEO num workflow único tem número** | Pesquisa Semrush: **81%** das organizações que integram SEO e AI visibility num fluxo único reportam ganho de tráfego/leads de IA vs **36%** das que tratam separado | Argumento comercial central do posicionamento Brasil GEO ("GEO = SEO sólido + camada de engenharia de evidência"). |
| **Concentração do referral de IA no ChatGPT** | Estudo Previsible (via Search Engine Land, jul-2026, 6,77 mi sessões / 19 meses): ChatGPT = **92,4%** do AI referral standalone (era ~84% em dez-2025); **28,8%** dos referrals do ChatGPT vão para páginas de resultado de busca interna; **Claude cresceu 64x** desde fim de 2024 e **ultrapassou o Perplexity em mar-2026**; Perplexity **−61%** do pico; Copilot **−96%** | Painel de medição pondera engines pelo share real de referral: ChatGPT primeiro, Claude em vigilância, Perplexity/Copilot rebaixados na prioridade de tracking de tráfego (não de citação). |
| **Conversão de tráfego de IA: por vertical, nunca média única** | B2B: IA converte **14,2%** vs 2,8% do orgânico Google (~5x); e-commerce: ChatGPT 1,81% vs 1,39% não-branded (**+31%**); Adobe (mar-2026): compradores vindos de IA convertem **+42%**; faixa geral observada **1,3x (e-commerce de baixo ticket) a 23x (B2B SaaS)** | Todo report cita a faixa e o vertical; proibido "IA converte 4–5x" como constante (§7.4). |
| **Volume de AI referral: pequeno, crescendo rápido** | Opollo: AI referral = **6,4%** do tráfego de B2B tech em jan-2026 (era <1% em jan-2025; **+975% YoY**); Semrush clickstream 17 meses: **+206% YoY** de referrals do ChatGPT (jan-25→jan-26); Ahrefs: IA ≈ **0,1%** do tráfego geral da web; sites <10k visitas ≈ 0,3% | Expectativa honesta em proposta comercial: o canal é estreito hoje e composto por intenção alta; o argumento é a taxa de crescimento + conversão, não o volume. |
| **Profound: padrões de citação por engine (6,8 mi citações)** | Análise de 6,8 mi citações / 1,6 mi respostas: **Gemini = 52,15%** das citações em sites da própria marca (owned); **ChatGPT = 48,73%** em diretórios/consenso de terceiros; **Perplexity** enfatiza expertise setorial e reviews de clientes | Estratégia por engine: owned content forte move Gemini; earned media/diretórios movem ChatGPT; reviews movem Perplexity. Casa com o achado de absorção da `2604.25707` (ChatGPT: menos fontes, influência maior). |
| **Ahrefs Brand Radar abre a metodologia** | `ahrefs.com/blog/brand-radar-methodology`: prompts derivados de **People Also Ask reais + fan-out semântico** (base 110 bi keywords); execução mensal ~340 mi prompts em 5 engines (AIO 282 mi; ChatGPT 14,5 mi; Perplexity 14,6 mi; Gemini 14,6 mi; Copilot 13,3 mi); métricas: Mentions, Citations, AI Share of Voice, Estimated Impressions; **limitações declaradas** (viés inglês, janela 90 dias, "auditoria de visibilidade, não audiência real") | Padrão de transparência metodológica que nossos reports devem igualar (§8); vocabulário de métricas compatível com o corpus (menção ≠ citação ≠ impressão estimada). |
| **Ahrefs: correlatos de AI visibility em 75k marcas** | Estudo dez-2025: menções de marca na web têm correlação **0,664** com visibilidade em AI Overviews; **YouTube** é o correlato mais forte simultaneamente em ChatGPT, AI Mode e AIO; ChatGPT correlaciona mais com **Domain Rating**; AIO aparece em **>25%** das buscas (13% no início de 2025) | Earned media + YouTube seguem como alavancas nº 1 (consistente com "84% earned" do corpus); correlação ≠ causa — usar como priorização, não como promessa. |
| **iPullRank formaliza "Relevance Engineering" como disciplina** | `ipullrank.com/ai-search-manual` (manual aberto) + framework r19g: interseção de information retrieval + UX + IA + conteúdo + PR digital; prática de **semantic chunking analysis** (clareza, concisão e valor autocontido por passagem); caso: pruning de 500+ posts guiado por embeddings, **+2–3%** de relevância semântica sitewide | Framework irmão do nosso (fan-out, passage retrieval, embeddings, síntese); adota vocabulário compatível com §5 e com os 4 pilares AWR já canonizados. |
| **AI Mode opera em português do Brasil** | Anúncio 8-set-2025 (pt-BR entre os 5 primeiros idiomas além do inglês; TechCrunch/blog.google); Google for Brazil 2026: capacidades agentic no AI Mode para o Brasil | GEO em pt-BR é superfície corrente, não aposta futura — mercado direto da Brasil GEO. |
| **Peec AI: números de referência do concorrente europeu** | Série A de **US$ 21 mi** (nov-2025, Singular); US$ 10 mi ARR em 16 meses; negociação de rodada a valuation ~US$ 200 mi (2026); funding total do setor de GEO analytics > **US$ 255–300 mi** | O mercado de medição GEO é categoria consolidada com capital; validação externa do posicionamento — e commoditização à vista do tracking simples (diferencial migra para diagnóstico causal + execução). |

### Seis premissas operacionais consequentes (a partir de 14-jul-2026)

1. **Pipeline único SEO+GEO, sempre.** O número 81% vs 36% (Semrush) é o argumento de fechamento comercial e o desenho default de projeto: uma esteira só, com camada GEO em cima da base SEO. **Aplicação:** propostas e cursos apresentam GEO como camada integrada, nunca como serviço paralelo.
2. **Estratégia por engine, não "otimizar para IA" genérico.** Gemini responde a owned content; ChatGPT a consenso de terceiros/diretórios; Perplexity a reviews e expertise setorial; e só 36 marcas do top-100 são visíveis nas 4 plataformas ao mesmo tempo. **Aplicação:** auditoria e roadmap nomeiam a engine-alvo de cada ação; o mix de distribuição é dosado por engine prioritária do cliente.
3. **Pondere a medição pelo share real de referral.** ChatGPT = 92,4% do referral standalone; Claude em ascensão (ultrapassou Perplexity em mar-2026). **Aplicação:** painel de prompts roda em todas as engines, mas SLA de reação e report executivo priorizam ChatGPT e AI Mode/AIO; Claude entra em vigilância trimestral.
4. **Conversão por vertical com faixa; volume com honestidade.** Faixa 1,3x–23x conforme vertical; volume típico ainda 0,1–6,4% do tráfego. **Aplicação:** todo report/copy cita vertical + fonte + período; nunca a média única "4–5x" (§7.4).
5. **Instrumente o funil vetorial como camada própria de medição.** `similaridade → hit rate@k → sobrevivência ao rerank → citation share` (§5.6) operacionaliza a "Camada 2 (Infraestrutura)" do framework de 3 camadas do corpus — a menos explorada cientificamente. **Aplicação:** repo papers ganha hipóteses mensuráveis; auditorias ganham diagnóstico causal ("o gargalo é retrieval, não citabilidade").
6. **Ferramenta ≠ verdade: exigir metodologia declarada.** Ahrefs publicou limitações; Profound não publica desenho amostral completo; clickstream tem viés reconhecido pela própria comunidade. **Aplicação:** nenhum número de vendor entra em report Brasil GEO sem nome da metodologia, período e limitação — o mesmo padrão que a junho-19 fixou para SoV.

---

## 1. Adobe × Semrush: a correção que reorganiza o mapa de vendors

- **19-nov-2025** — Adobe anuncia acordo definitivo para adquirir a Semrush Holdings por US$ 12,00/ação em dinheiro (~US$ 1,9 bi de equity). Racional declarado no press release: *"Brand visibility is being reshaped by generative AI"*; a Semrush leva SEO + capacidades de **generative engine optimization (GEO)** para complementar Adobe Experience Manager, Adobe Analytics e Brand Concierge. Mais de 75% do poder de voto dos acionistas já comprometido no anúncio. Fonte primária: `news.adobe.com/news/2025/11/adobe-to-acquire-semrush`.
- **Final de abril/2026 (semana de 28-abr)** — transação **concluída** após aprovação regulatória (8-K da Adobe na SEC, FY2026; cobertura de 29-abr: "cleared regulatory review and closed this week").
- **Consequências para o mapa de vendors do corpus (15B §3/§8):** (a) o AI Visibility Index e o Enterprise AIO são agora ativos Adobe — integração esperada com a stack Adobe CX (28 mi usuários declarados); (b) a fileira "vendors enterprise com integração Adobe/Salesforce" (Conductor etc.) ganha um concorrente interno; (c) a leitura estratégica da 15B ("Conductor se a stack é Adobe") precisa ser refeita caso a caso.
- **Por que o corpus errou (nota de método):** a 15B (15-jun-2026) canonizou como correção que a Semrush *não* era subsidiária da Adobe, provavelmente validando contra o ticker NYSE: SEMR ainda ativo em fontes desatualizadas — mas o fechamento já tinha ocorrido em abril. Lição: **status societário se verifica em press release/SEC, não em listagem de bolsa nem em WebFetch de página de terceiros** (§7.1).

## 2. Medição: o trimestre em que os números ficaram grandes

### 2.1. Semrush (Adobe) — AI Visibility Index 2026 expandido (26-jun-2026)
- Escopo: **126 milhões de prompts** de AI search nos EUA (jan–abr/2026), cobrindo ChatGPT, Gemini, Google AI Mode e AI Overviews; 22 setores. Salto de escala: a edição anterior usava ~2.500 prompts (15B §3.2).
- Padrões de citação: **ChatGPT ~15 fontes por resposta** (peso alto de Reddit/Wikipedia e plataformas de referência); **Gemini ~3 fontes** (pool menor: Wikipedia, Reddit, YouTube). Coerente com a divergência largura×profundidade da `2604.25707` (já canonizada): ChatGPT concentra influência; Perplexity/Google distribuem.
- **Só 36 marcas do top-100 são visíveis nas 4 plataformas simultaneamente** — visibilidade cross-engine é exceção, não regra.
- Pesquisa complementar: **81%** das organizações com SEO+AI visibility integrados num workflow único reportam aumento de tráfego/leads de IA; **36%** entre as que gerenciam separado. **45%** dos líderes de marketing não conseguem medir a visibilidade da marca em respostas de IA; só **9%** dizem ter ferramentas para todas as métricas relevantes.
- Clickstream de 17 meses (blog Semrush): **+206% YoY** de tráfego referral do ChatGPT (jan-2025→jan-2026); projeção da casa: resultados gerados por IA ultrapassam o tráfego orgânico tradicional **até 2028** (projeção de vendor — tratar como cenário, não fato).

### 2.2. Ahrefs — metodologia aberta e correlatos em escala
- **Brand Radar publica a metodologia** (`ahrefs.com/blog/brand-radar-methodology`): prompts derivados de queries reais (People Also Ask) + **fan-out semântico** sobre base de 110 bi de keywords (28,7 bi com volume >0); execução mensal em 5 engines (AI Overviews 282 mi prompts; ChatGPT 14,5 mi; Perplexity 14,6 mi; Gemini 14,6 mi; Copilot 13,3 mi; Grok e AI Mode também rastreados). Métricas: **Mentions** (string na resposta), **Citations** (URLs linkadas), **AI Share of Voice**, **Estimated Impressions** (ponderadas por volume Google). Limitações declaradas: viés para inglês e queries populares, janela de 90 dias, links alucinados excluídos; autoclassificação como "auditoria de visibilidade, não medição de audiência real".
- **Estudo de correlatos (dez-2025, 75k marcas, milhões de respostas):** menções de marca na web ↔ visibilidade em AIO com correlação **0,664**; **YouTube** é o correlato mais forte simultaneamente em ChatGPT, AI Mode e AIO; visibilidade no ChatGPT correlaciona mais com **Domain Rating**; Perplexity e AIO com profundidade de conteúdo. Contexto de mercado: AIO em **>25%** das buscas (vs 13% no início de 2025); EUA ~1,6x mais propensos a receber tráfego de IA que Índia/Reino Unido; setor "Business & Industrial" com o dobro da propensão.
- Leitura canônica: correlação ≠ causa (a própria Ahrefs marca isso); usar para **priorizar** earned media + YouTube + menções, mantendo os estudos causais (junho-19 §2) como teto de promessa.

### 2.3. Profound (Adobe-independente; unicórnio desde fev-2026, cf. 15B)
- **Padrões de citação por engine** (análise de 6,8 mi citações em 1,6 mi respostas): **Gemini 52,15%** das citações em sites da própria marca; **ChatGPT 48,73%** em diretórios e consenso de terceiros; **Perplexity** com ênfase em expertise setorial e reviews de clientes.
- Metodologia (síntese Perplexity r2 + análises independentes): coleta em três fases — ingestão de prompts de painéis reais, logging de respostas por engine, processamento estatístico de taxa de menção por tema; captura o **front-end real** dos assistentes (não só API), sob o argumento de que a superfície de consumo difere da API. Ponto fraco reconhecido por avaliadores independentes: **não publica desenho amostral, precisão/recall nem cadência de refresh** — abaixo do padrão de transparência que a Ahrefs acabou de fixar.
- Já canonizado antes (não repetir): Série C US$ 96 mi / valuation US$ 1 bi (fev-2026, Lightspeed); tempo-até-citação mediana 6,81 dias; benchmark de 9 engines.

### 2.4. Google Search Console — consolidação dos relatórios de IA
- **3-jun-2026**: relatórios dedicados de **Generative AI Performance** no GSC (impressões de URLs em recursos generativos em Search e Discover, países, dispositivos), rollout gradual a partir de subconjunto de sites — consolida o teste UK registrado na junho-19 §5. Segmentos de Search Type para AI Overviews e AI Mode em disponibilização; segue **sem dados de clique** por superfície de IA em granularidade completa (crítica de Glenn Gabe permanece válida).
- Dado oficial de contexto (mar-2026): queries no AI Mode têm em média **3x o comprimento** das buscas tradicionais — reforça prompt research sobre keyword research (§4.1).

## 3. Tráfego e mercado: concentração, ascensão do Claude e capital

- **Previsible via Search Engine Land (jul-2026; 6,77 mi sessões, 19 meses de dados):** ChatGPT = **92,4%** de todo o AI referral standalone (era ~84% em dez-2025); **28,8%** dos referrals do ChatGPT apontam para páginas de resultado de busca interna dos sites (implicação técnica: essas URLs de busca interna precisam estar rastreáveis e renderizando bem); **Claude cresceu 64x** desde o fim de 2024 e **ultrapassou o Perplexity em mar-2026**; Perplexity caiu **−61%** do pico; Copilot **−96%**. Sessões mensais de LLM no dataset cresceram 9,9x (644 mil em mai-2026).
- **Conversão por vertical (compilação multi-fonte, 2025–2026):** B2B — visitantes de IA convertem em média **14,2%** vs 2,8% do orgânico Google (~5x); e-commerce — ChatGPT 1,81% vs 1,39% do orgânico não-branded (**+31%**); Adobe (mar-2026): compradores vindos de assistentes de IA convertem **+42%** vs tráfego não-IA; faixa cross-industry: **1,3x a 23x**. Volume: **6,4%** do tráfego de B2B tech em jan-2026 (Opollo; <1% um ano antes; +975% YoY) contra ~0,1% do tráfego geral da web (Ahrefs). Ou seja: canal estreito, intenção altíssima, crescimento composto.
- **Capital e consolidação:** além de Adobe×Semrush (§1) e Profound unicórnio (15B), a **Peec AI** (Berlim) levantou Série A de US$ 21 mi (nov-2025, Singular) após seed de €5,2 mi (jul-2025, 20VC), atingiu US$ 10 mi de ARR em 16 meses e negocia rodada a ~US$ 200 mi de valuation. Funding total identificado em GEO analytics: **> US$ 255–300 mi** (verão-2025→primavera-2026). Leitura: tracking simples de SoV vira commodity; o diferencial defensável migra para **diagnóstico causal + execução** (exatamente o desenho Brasil GEO).

## 4. Framework de execução de GEO — síntese operacional consolidada

> Síntese de conhecimento operacional (rodada OpenAI r3 + manual aberto iPullRank + corpus). **Não é fato datado** — é o playbook consolidado que o mercado maduro pratica em 2026; adotar como esqueleto default de projeto/curso, adaptando ao `GEO_OPERATING_SYSTEM.md`.

### 4.1. Workflow em 7 etapas (ciclo contínuo)
1. **Baseline** — auditoria de onde/como a marca aparece por engine (menção, sentimento, precisão factual, fontes usadas), concorrentes incluídos.
2. **Prompt research** (não keyword research) — biblioteca de prompts por intenção (informacional, comparativa, transacional, reputacional), com score de priorização por valor comercial × volume estimado × gap de presença. Justificativa nova: queries de AI Mode são 3x mais longas (§2.4); o portfólio canônico de 25 prompts do repo landing é a instância local disso.
3. **Produção/otimização** — páginas GEO-ready: resposta direta no topo (answer capsule), seções por sub-query do fan-out, estatísticas datadas, quotes, tabelas, FAQs, definições canônicas de entidade (rubrica Princeton do corpus).
4. **Distribuição** — earned media (PR digital), comunidades (sem spam), Wikipedia/Wikidata onde há notabilidade legítima, YouTube (correlato nº 1 cross-engine, §2.2), diretórios/reviews por engine-alvo (§2.3).
5. **Medição** — 4 famílias de KPI: **Visibilidade** (AI SoV, taxa de presença por prompt, posição na resposta, cobertura por engine), **Qualidade** (sentimento, precisão factual, categoria correta, diferenciais citados), **Fontes** (domínios citados, owned vs earned, fontes novas conquistadas, frescor), **Negócio** (sessões AI referral, conversões/leads/pipeline/receita influenciados, taxa de conversão por vertical).
6. **Report executivo** — responde 8 perguntas: onde aparecemos? onde não? quem ganha? que erros os modelos dizem sobre nós? quais prompts têm valor comercial? o que executamos? qual impacto em tráfego/pipeline/receita? o que faremos no próximo ciclo?
7. **Iteração mensal** — reexecutar biblioteca de prompts (múltiplas execuções e média — regra AWR da junho-19), comparar com baseline, mapear fontes novas citadas, corrigir erros factuais, redistribuir.

### 4.2. Programa: papéis e cadência
- **Papéis** (escala completa; num boutique, chapéus acumulados): GEO Lead/Strategist; Prompt Research Analyst; Content Strategist; Redator especialista; Técnico SEO/GEO (schema como higiene, indexação, logs, renderização); Digital PR/Authority Builder; Community Manager; Data Analyst (atribuição, CRM); SME (quotes e assinatura); Legal/Compliance em setores regulados.
- **Cadência**: sprint semanal (seg: métricas e priorização; ter–qua: produção/técnico/outreach; qui: QA e publicação; sex: medição parcial e aprendizados) · ciclo mensal (rodada completa de prompts, benchmark competitivo, auditoria de fontes, report executivo) · ciclo trimestral (revisão de estratégia, estudo proprietário/relatório de dados — o ativo que gera citação —, auditoria de autoridade de entidade, ajuste de atribuição).
- **5 gates de qualidade pré-publicação**: (1) Factualidade — claims verificáveis, dados com fonte e data visível; (2) Clareza de entidade — marca+categoria+diferencial consistentes, sem ambiguidade; (3) Citabilidade — estatísticas, tabelas, definições curtas, quotes, FAQ, resumo executivo; (4) Técnica — indexável, headings estruturados, canonical, renderização; (5) Autoridade — SME assinando, corroboração externa. Mapeia 1:1 para o quality gate do curso-factory (`content_checker.py`).

### 4.3. Relevance Engineering (iPullRank) — a disciplina irmã
- Definição r19g: interseção de information retrieval + UX + IA + estratégia de conteúdo + PR digital; a visibilidade em IA é tratada como **problema de engenharia** ("construir, não ajustar"). Manual aberto: `ipullrank.com/ai-search-manual`.
- Práticas adotáveis já: **semantic chunking analysis** (avaliar cada passagem por clareza, concisão e valor autocontido — instrumentável via §5.6); **pruning guiado por embeddings** (caso publicado: 1.000+ posts avaliados, 500+ cortados, +2–3% de relevância semântica sitewide); papel formal de "Relevance Engineer" conectando SEO técnico e arquitetura de conteúdo AI-first.
- Encaixe no corpus: mesmo objeto dos 4 pilares AWR (junho-19 §4) com ênfase mais operacional; vocabulário compatível com o funil §5.6.

## 5. Física semântico-vetorial do GEO — funil mensurável (síntese técnica)

> Síntese técnica (rodada Anthropic r6, alinhada aos ~25 papers da camada semântica já canonizados na wave junho-2026). Valor novo: transforma a teoria em **7 métricas operacionais + 1 cadeia causal instrumentável**.

### 5.1. Espaço vetorial e entidade
- Embeddings mapeiam textos para vetores densos (d ∈ {768…3072}); similaridade coseno domina porque a **direção** carrega o significado (magnitude ≈ frequência/comprimento = ruído). Recuperação = MIPS acelerada (HNSW/IVF-PQ).
- Se o vetor da entidade está longe do conceito-alvo, os chunks caem fora do top-k e **nunca entram na janela de contexto** — não podem ser citados. GEO opera sobre probabilidade de retrieval.
- **Consolidação de entidade no espaço latente:** (a) co-ocorrência consistente `marca + categoria + atributo definidor` no mesmo span; (b) definição canônica aristotélica ("X é um [gênero] que [diferença específica]"); (c) consistência inter-documento da mesma formulação (reduz variância direcional do centróide da entidade). Age nos dois substratos: treino (paramétrico) e índice (RAG).

### 5.2. Pipeline e oportunidades por etapa
`query understanding → fan-out → retrieval híbrido (BM25+dense, fusão RRF) → reranking (cross-encoder) → síntese com atribuição`. Oportunidade dupla no retrieval: **vocabulário exato** (termos canônicos literais → BM25) **e** paráfrase semântica (definições, contexto → dense) — ignorar o lado lexical é erro comum. O cross-encoder recompensa passagens que **respondem à pergunta de forma autocontida**, não apenas topicamente relacionadas.

### 5.3. Chunking: a página não é a unidade — o chunk é
- Parágrafos autocontidos de 2–4 frases (densos para responder; curtos para não diluir o embedding num centróide médio); headings descritivos em forma de pergunta (frequentemente prependados ao chunk); tabelas e FAQs mapeiam quase 1:1 para sub-queries do fan-out; **cada chunk nomeia a entidade explicitamente** (sem pronomes — será lido fora de contexto). Anáfora externa ("como visto acima") = vetor diluído + inútil na síntese.
- Nota de conciliação com a junho-19: o Google declarou "chunking obrigatório" desnecessário **para o Google Search** — a regra aqui não é técnica de arquivo, é **redação autocontida por passagem**, que vale para todos os motores RAG e não contradiz o guia oficial.

### 5.4. Paramétrico × recuperado
Presença dupla obrigatória: corpus de treino (redundância consistente em fontes crawladas → a marca "existe" mesmo sem busca; efeito de longo prazo) e índice de busca (chunks frescos e recuperáveis; efeito de curto prazo). Conteúdo estruturado mas obscuro perde no primeiro; popular mas mal estruturado perde no segundo.

### 5.5. O que a síntese cita
Fluência/encaixe generativo (baixa perplexidade ao incorporar), densidade factual (números, datas, definições ancoram o grounding), aboutness (responder a pergunta exata > relevância difusa), autoridade percebida + corroboração cruzada entre passagens recuperadas. Tudo condicional a sobreviver ao retrieval e ao rerank.

### 5.6. As 7 métricas operacionais e a cadeia causal

| Métrica | Definição operacional | Como medir |
|---|---|---|
| Embedding similarity (marca↔tópico) | Coseno médio entidade × conceitos-alvo | Embedar N formulações da marca × M queries do domínio; monitorar centróide no tempo |
| Cobertura de sub-queries do fan-out | % das sub-queries previsíveis com ≥1 chunk relevante | Simular fan-out via LLM + retrieval local contra o próprio corpus |
| Taxa de trechos autocontidos | % de chunks que respondem a alguma query sem contexto externo | LLM-as-judge de self-containment + presença explícita de entidade |
| Retrieval hit rate @k | P(chunk próprio ∈ top-k) nas queries-alvo | Índice espelho BM25+dense reproduzindo o pipeline |
| Rerank survival rate | P(permanecer no top-n pós-cross-encoder \| entrou no top-k) | Aplicar cross-encoder aos candidatos |
| Citation share / SoV generativo | Frequência de citação num painel de queries | Amostragem sistemática por engine (múltiplas execuções, média) |
| Densidade factual do chunk | Fatos verificáveis por 100 tokens | Extração de claims + contagem normalizada |

**Cadeia causal:** `similarity ↑ → hit rate@k ↑ → rerank survival ↑ → citation share ↑`, modulada por self-containment e densidade factual nas duas últimas transições. **Gargalo em qualquer estágio anula ganhos a montante** — instrumentar ponta a ponta antes de otimizar citabilidade.

## 6. Pulso da comunidade (sinal qualitativo, doublecheck aplicado)

- Sentimento dominante (convergência Grok + fontes verificadas): a comunidade saiu do hype e entrou em fase de **medição e experimentação controlada** — desconfiança de clickstream de terceiros (viés de amostragem reconhecido), migração para server logs + medição própria, demanda por testes controlados (linha Mike King/Lily Ray, consistente com os estudos causais Ahrefs do corpus).
- Conceitos em circulação: "LLM-first content architecture" (r/bigseo), "brand mention velocity" como métrica emergente (Kevin Indig/Aleyda Solís), "GEO attribution modeling" (série da Search Engine Land, jun-2026).
- Plataformas: Perplexity segue investindo na superfície agentic (browser Comet; Deep Research no assistente agentic, 19-jun-2026) apesar da queda de share de referral (§3) — citação e agência são jogos diferentes de tráfego. John Mueller aponta **WebMCP** (padrão apoiado pelo Google) como alternativa preferida ao llms.txt para interação com agentes — acompanhar, ainda cedo para canonizar.
- OpenAI: GPT-5.5 Instant Mini no ChatGPT (6-jul-2026) — relevância GEO indireta (respostas menos estruturadas repetitivas); ChatGPT Shopping/checkout agentic em expansão (fatos de produto com verificação parcial — não canonizar números).

## 7. Correções e conflitos (com prevalência declarada)

### 7.1. REVOGAÇÃO de correção anterior — Adobe × Semrush
A Wave 15B §8 item 5 canonizou: *"Semrush NÃO é subsidiária da Adobe (erro provável de leitura de WebFetch). É NYSE: SEMR, independente. Não tratar como fato."* **Esta correção estava errada** e fica **revogada**: a aquisição foi anunciada em 19-nov-2025 (press release da própria Adobe) e **concluída no final de abril/2026** — antes, portanto, da redação da 15B (15-jun). Prevalece: **Semrush é Adobe desde abril/2026**. Fontes primárias: `news.adobe.com/news/2025/11/adobe-to-acquire-semrush`; 8-K Adobe (SEC, FY2026); cobertura de fechamento 29-abr-2026. Lição de método incorporada: fato societário se confirma em press release/filing, e correções também envelhecem — toda "correção" carrega data e fica sujeita à mesma regra de prevalência.

### 7.2. Alucinações do Grok refutadas (manter fora do corpus)
- *"Profound levantou seed de US$ 8 mi em mai-2026"* — **FALSO**: a Profound fechou **Série C de US$ 96 mi** (fev-2026, Lightspeed, valuation US$ 1 bi), já canonizada na 15B.
- *"Peec foi adquirida por martech europeia em jun-2026"* — **sem qualquer evidência**; o verificável é Série A US$ 21 mi (nov-2025) + negociação de rodada a ~US$ 200 mi. Tratar a rodada xAI desta wave como **sinal qualitativo apenas** (r5 marcado no raw).

### 7.3. Números de conversão de IA — regra de citação
"Tráfego de IA converte 4–5x" **não pode ser citado como constante**: a faixa real é 1,3x–23x conforme vertical, e parte dos estudos compara bases diferentes (branded vs non-branded, assistido vs último clique). Regra: citar **vertical + fonte + período + base de comparação** (ex.: "B2B: 14,2% vs 2,8% orgânico, compilação 2026").

### 7.4. O que esta wave NÃO muda
Permanecem em vigor, sem alteração: as 5 táticas "não precisa fazer" do Google, os estudos causais Ahrefs (schema; llms.txt 97%), a regra anti-"Share of Answer" como KPI normalizado, a proibição dos acrônimos sem fonte (AIGVR/AECR/CTAM/RTAS/Brand Echo), e a taxonomia CSR×CAR. O paper `2604.25707` e o `GEO-Bench 2605.29107` seguem como canonizados (foram re-verificados em arxiv.org nesta wave; nenhum paper novo com ID verificável foi encontrado no período — o candidato "CORE" citado pelo Perplexity ficou **fora** por falta de ID verificável, regra anti-GhostCite).

## 8. Aplicação por repositório

### 8.1. `papers` (pesquisa acadêmica)
- **Hipóteses novas pré-registráveis:** (H-a) padrões de citação por engine em pt-BR reproduzem Profound/Semrush (Gemini→owned; ChatGPT→terceiros; nº médio de fontes 15 vs 3)? (H-b) correlato YouTube/menções (Ahrefs 0,664) se sustenta nas verticais brasileiras do dataset? (H-c) a cadeia causal §5.6 é testável com índice espelho — contribuição científica direta na "Camada 2 (Infraestrutura)", declarada no corpus como a menos explorada.
- **Coleta:** considerar campo/tag de `citation_style` por engine (owned/earned/diretório/review) no schema de citações — viabiliza H-a com o dataset existente; ponderar o painel de engines pelo share de referral (§3) ao interpretar impacto, sem desbalancear o N experimental.
- **Método:** o padrão Ahrefs de "limitações declaradas" (§2.2) é o baseline de transparência para os 3 papers-alvo; a revogação §7.1 vira exemplo interno de por que correções também precisam de data e re-verificação.

### 8.2. `landing-page-geo` (site alexandrecaramaschi.com)
- **Copy comercial:** incorporar 81% vs 36% (pipeline único) e conversão por vertical com a regra §7.3; posicionar medição própria da Brasil GEO com metodologia declarada (diferencial vs Profound, §2.3).
- **Conteúdo:** aplicar §5.3 na redação (chunks autocontidos 2–4 frases, headings-pergunta, entidade nomeada por chunk, tabelas/FAQ por sub-query do fan-out) — já compatível com o `GEO_CHECKLIST_REDACAO_2026.md`; priorizar as engines ChatGPT + AI Mode/AIO (pt-BR ativo, §0) no portfólio canônico de 25 prompts.
- **Medição:** quando o rollout do GSC Generative AI Performance chegar à propriedade, integrar ao `MEASUREMENT_ARCHITECTURE.md` (impressões de IA como KPI inicial, sem CTR); URLs de busca interna rastreáveis (28,8% dos referrals do ChatGPT, §3).

### 8.3. `curso-factory` (fábrica de cursos)
- **Conteúdo de cursos:** três blocos novos prontos para módulos — (a) "A consolidação do mercado de GEO" (Adobe×Semrush, Profound, Peec, §1/§3); (b) "O funil vetorial mensurável" (§5, com as 7 métricas como exercício prático); (c) "Como operar um programa de GEO" (§4: workflow, papéis, cadência, gates, report de 8 perguntas).
- **Prompts/gates:** o `draft.md` pode referenciar §5.3 (autocontenção por chunk) como técnica de citabilidade adicional à rubrica Princeton; o `review.py`/reviewer ganha duas proibições novas: "IA converte 4–5x" sem vertical/fonte (§7.3) e "Semrush independente da Adobe" (§7.1).
- **Pesquisa (researcher/Perplexity):** citar §2 como fonte de números atualizados de medição ao gerar cursos de GEO/SEO/marketing.

---

### Apêndice · método de orquestração desta wave (reaplicável)
Seis rodadas via CLI `llm` do orquestrador local (`--provider X --cloud on --yes --file prompt.txt`), em background paralelo, + doublecheck Claude (WebSearch/WebFetch em fonte primária). **Gotchas operacionais registrados:** (a) `perplexity:sonar-deep-research` falhou na 1ª tentativa da rodada indústria com `IncompleteRead` (stream interrompido) — retry simples resolveu; (b) `google:gemini-2.5-flash` retornou HTTP 429 "prepayment credits depleted" (créditos AI Studio esgotados — reincidência da issue #4 do geo-orchestrator); (c) `groq:llama-4-scout` retornou HTTP 400 porque o CLI envia `max_tokens` > 8192 (limite do modelo) — bug de config do orquestrador, sem workaround via flag. Raws em [`raw/`](raw/): `r1_perplexity_papers.md`, `r2_perplexity_industria.md`, `r3_openai_frameworks.md`, `r5_xai_tendencias.md` (baixa confiança factual, cf. §7.2), `r6_anthropic_semantica.md`.

### Referências principais (verificadas nesta wave)
- https://news.adobe.com/news/2025/11/adobe-to-acquire-semrush · 8-K Adobe (SEC EDGAR, FY2026) · cobertura de fechamento 29-abr-2026 (DesignRush News)
- https://www.semrush.com/news/463141-semrush-releases-expanded-2026-ai-visibility-index-analyzing-126-million-ai-search-prompts/ · https://www.semrush.com/blog/chatgpt-search-insights/ · https://www.semrush.com/blog/ai-seo-statistics/
- https://ahrefs.com/blog/brand-radar-methodology/ · https://ahrefs.com/blog/ai-traffic-research/ · https://ahrefs.com/blog/brand-radar-use-cases/
- https://searchengineland.com/chatgpt-ai-referral-traffic-sessions-data-481630 (Previsible)
- https://www.tryprofound.com/blog/how-to-track-your-visibility-in-ai-search (+ análises independentes de metodologia)
- https://ipullrank.com/ai-search-manual · https://ipullrank.com/relevance-engineering-introduction · https://ipullrank.com/relevance-engineering-at-scale
- https://arxiv.org/abs/2604.25707 · https://arxiv.org/abs/2605.29107 (re-verificados)
- https://techcrunch.com/2025/09/08/googles-ai-mode-adds-5-new-languages-including-hindi-japanese-and-korean/ · https://blog.google/company-news/inside-google/around-the-globe/google-latin-america/google-for-brazil-2026/
- https://techfundingnews.com/peec-ai-200m-valuation-10m-arr-geo-marketing/ · https://ppc.land/google-finally-gives-search-console-its-own-generative-ai-visibility-reports/
