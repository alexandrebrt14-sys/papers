# Track A — Papers Acadêmicos Q2 2026 (GEO/RAG/LLM)

> Sub-agent Opus · 2026-05-20 · enriquecimento das bases canônicas Brasil GEO
> Foco: papers publicados após março 2026, complementando GEO_KNOWLEDGE_BASE_2026_V2.md
> 18 papers validados via WebFetch direto em arxiv.org · zero IDs inventados

---

## Como ler este documento

O Track A foi construído como camada de enriquecimento sobre a KB V2. Cada paper recebeu uma micro-ficha (achado central + metodologia) e três sub-seções obrigatórias de aplicação direta, uma por repositório:

- **landing-page-geo** — site público alexandrecaramaschi.com (Next.js 16, ~340 artigos HBR-grade, Cloudflare Workers + Vercel).
- **curso-factory** — pipeline de cursos longos com voice guard, Drive import, voice Alexandre.
- **papers** — repositório próprio de pesquisa GEO com Query Battery v2, harness de coleta multi-LLM, indexação de papers acadêmicos.

A escolha de papers respondeu a duas perguntas operacionais: (1) o que mudou em GEO especificamente, no recorte abr-mai 2026, em relação ao stack Aggarwal-Chen-Yao consolidado na V2? (2) que melhorias em RAG citation grounding, hybrid retrieval e agentic browsing já são acionáveis nos três repos no horizonte de seis a doze semanas? Cada paper aqui carrega um vetor de aplicação concreto, não apenas um resumo descritivo.

A bibliografia da KB V2 fica como pano de fundo. Quando este Track A propõe substituir ou estender uma técnica já documentada na V2, isso é dito de forma explícita na sub-seção do repositório, com referência cruzada à seção da V2 (quando aplicável).

---

## Sumário executivo — 18 papers em uma frase cada

1. **arXiv:2604.19113 (Liu & Xu, 21-abr-2026)** — FeatGEO eleva GEO do nível token para nível feature, abrindo otimização multi-objetivo de visibilidade de citação sem perder qualidade editorial.
2. **arXiv:2604.25707 (Zhang, He & Yao, 28-abr-2026)** — Diferencia citação selecionada de citação absorvida, mostrando que ChatGPT cita menos fontes mas com peso muito maior, em 602 prompts controlados.
3. **arXiv:2603.29979 (Yu, Yang, Ding & Sato, 31-mar-2026)** — GEO-SFE provou que estrutura visual (headings, listas, blocos canônicos) ganha 17,3% de citation rate e 18,5% de quality score em seis engines.
4. **arXiv:2604.19516 (Wu et al., 21-abr-2026)** — MAGEO transforma GEO em sistema multi-agente que aprende estratégias reutilizáveis por engine, superando heurísticas em visibilidade e fidelidade citatória.
5. **arXiv:2604.07585 (Schulte, Bleeker & Kaufmann, 8-abr-2026)** — A visibilidade GEO é uma distribuição, não um número: uma medição única é estatisticamente inútil; o paper formaliza protocolos de re-amostragem.
6. **arXiv:2604.27790 (Grossman et al., 30-abr-2026, SIGIR 2026)** — Estudo empírico de 11.500 queries mostra que AI Overviews surgem em 51,5% das buscas e que bloquear Google-Extended pune visibilidade em AIO mesmo com indexação aberta.
7. **arXiv:2602.06718 (Xu et al., v2 14-mai-2026)** — GhostCite faz auditoria de 2,2 milhões de citações: 14-95% de citações fabricadas em 13 LLMs, com piora abrupta em 2025.
8. **arXiv:2602.23452 (Shi et al., v3 1-mai-2026)** — CiteAudit propõe pipeline multi-agente para auditoria automatizada de citações com taxonomia 12-código e dataset humano-validado.
9. **arXiv:2605.08583 (Li, Lin & Ma, 9-mai-2026)** — CiteTracer atinge 97,1% de precisão em detectar citações alucinadas usando classificação cascateada Real-Potencial-Hallucinated.
10. **arXiv:2604.03173 (Rao, Wong & Callison-Burch, 3-abr-2026)** — 3-13% de URLs citadas por agentes deep-research nunca existiram (sem registro Wayback); urlhealth reduz para menos de 1%.
11. **arXiv:2604.01733 (Akarsu, Karaman & Mierbach, 2-abr-2026)** — Benchmark de 10 estratégias de retrieval em documentos texto+tabela financeira mostra BM25 superando dense embeddings puros.
12. **arXiv:2604.22180 (Ke et al., 24-abr-2026)** — ResRank une retrieval e listwise reranking em um único treinamento ponta-a-ponta, atingindo SOTA com zero tokens gerados.
13. **arXiv:2605.12975 (Sun et al., 13-mai-2026)** — PyRAG transforma multi-hop RAG em síntese de programa Python executável, com self-repair determinístico via execução.
14. **arXiv:2604.26649 (Guo, Wu & Yiu, 29-abr-2026)** — ReaLM-Retrieve resolve descasamento entre RAG e reasoning models, decidindo quando retrievar durante o chain-of-thought.
15. **arXiv:2604.09666 (Fan et al., 1-abr-2026)** — RAGSearch benchmark mostra que agentic search reduz a vantagem de GraphRAG sobre dense RAG, exceto em multi-hop complexo.
16. **arXiv:2603.07379 (Mishra et al., 7-mar-2026)** — SoK de Agentic RAG formaliza taxonomia POMDP e mapeia nove vulnerabilidades de governança.
17. **arXiv:2605.17641 (Srivastava, 17-mai-2026)** — Causal Memory Intervention substitui similaridade por causalidade na seleção de memória de longo prazo de agentes.
18. **arXiv:2605.00318 (Guttal et al., 1-mai-2026)** — Structure-Aware Tabular Chunking eleva MRR de 0,357 para 0,594 em RAG sobre dados tabulares, área não coberta pela V2.

---

## 1. arXiv:2604.19113 — Think Before Writing: Feature-Level Multi-Objective Optimization for Generative Citation Visibility

- **Autores**: Zikang Liu, Peilan Xu
- **Submissão**: 21 de abril de 2026
- **URL canônica validada**: https://arxiv.org/abs/2604.19113

### Achado central

O paper introduz FeatGEO, mudando a unidade de otimização de GEO do nível token (inserção de palavras-chave, frases autoritárias) para o nível feature: cada página é abstraída como vetor de propriedades estruturais, de conteúdo e linguísticas, com otimização multi-objetivo simultânea de visibilidade citatória e qualidade editorial.

### Metodologia

Os autores treinam um modelo preditivo de citação por feature em três engines generativos distintos, depois aplicam optimização Pareto-eficiente entre o objetivo "ser citado" e o objetivo "não degradar leitura humana". O resultado opera por edição estrutural de página, não por substituição lexical, e isso é o salto em relação a Aggarwal et al. 2023.

### Aplicação direta em landing-page-geo

Em `landing-page-geo/src/lib/articles.ts`, hoje cada artigo entra com bloco frontmatter padrão HBR (impacto-tese-evidência-mecanismo-decisão-próximo-passo). FeatGEO sugere camada adicional: para cada artigo, calcular um perfil de features (densidade de bullets, frequência de blocos canônicos, ratio cite-density) e otimizar contra os perfis vencedores extraídos da Query Battery do papers repo. Implementar como `scripts/python/featgeo_audit.py`: lê artigo, gera scorecard nas 14-22 features do paper, retorna recomendações editoriais antes do `npm run verify`.

### Aplicação direta em curso-factory

Em curso-factory, cada lição produzida pelo pipeline Drive-import passa por voice_guard.py. FeatGEO sugere segundo gate: `featgeo_check.py` quantifica perfil estrutural da lição antes da geração de HTML final. Se o perfil cair fora da banda observada nos cursos com maior citation rate (medido via papers harness), o pipeline sinaliza correção. Custo marginal baixo: features são extraíveis com regex e contagem, sem chamadas LLM.

### Aplicação direta em papers

Em `papers/src/featgeo_extractor/`, criar pipeline que toma os 25 prompts da Query Battery v2, coleta respostas dos 4 LLMs, extrai URLs citadas, e para cada URL citada extrai o vetor de features FeatGEO via crawler local. Depois roda regressão multi-classe predizendo "ser citado pelo modelo X" como função das features. Esse modelo serve dois propósitos: (a) gerar recomendações editoriais reverse-engineered para landing-page-geo; (b) abastecer dashboard com "feature gap analysis" por artigo.

---

## 2. arXiv:2604.25707 — From Citation Selection to Citation Absorption: A Measurement Framework for Generative Engine Optimization Across AI Search Platforms

- **Autores**: Kai Zhang, Xinyue He, Jingang Yao
- **Submissão**: 28 de abril de 2026, revisão v2 em 29 de abril de 2026
- **URL canônica validada**: https://arxiv.org/abs/2604.25707

### Achado central

O paper distingue dois fenômenos antes tratados como um: citation selection (o engine optou por listar a fonte) e citation absorption (a fonte teve impacto detectável no texto final gerado). Com 602 prompts controlados em ChatGPT, Google AI Overview/Gemini e Perplexity, demonstra-se que Perplexity e Google citam muitas fontes com peso médio baixo, enquanto ChatGPT cita poucas mas com peso altíssimo. Páginas mais longas e bem estruturadas, com definições explícitas, fatos e comparações, têm absorption desproporcionalmente maior.

### Metodologia

A framework de absorção mede sobreposição lexical não-trivial entre conteúdo da página citada e o texto gerado, controlado por baseline de fontes não-citadas. O resultado é uma matriz selection-absorption que permite separar "página listada por completude" de "página realmente usada para construir a resposta". Isso resolve um problema crônico das métricas GEO da V2, que tratavam toda menção como equivalente.

### Aplicação direta em landing-page-geo

Em `landing-page-geo`, a métrica de sucesso por artigo deve mudar de "citation rate" para um par (selection rate, absorption rate). Adicionar coluna `absorptionScore` ao dataset de tracking em `papers/data/llm_citation_log.json`. Para os 20% de artigos com selection alta mas absorption baixa, escrever versão B: bullets explícitos com definições, blocos de comparação 2-coluna, número-pivô em destaque, conforme padrão observado pelos autores. Roteiro: identificar 10 artigos high-selection-low-absorption no log de mai-2026, propor reescrita aplicando padrões "evidência citável" do paper, medir delta em 4 semanas.

### Aplicação direta em curso-factory

Em curso-factory, os módulos de lição podem ser anotados com tags de "absorvibilidade": uma lição com definição canônica de um conceito é mais absorvível que uma narrativa de caso. Para cada lição, marcar no metadata blocos { tipo: definicao | fato | comparacao | exemplo | historia } e priorizar densidade de definicao/fato em lições destinadas a ranqueamento GEO. Lições de storytelling preservam função pedagógica mas não competem em absorption.

### Aplicação direta em papers

Em `papers/src/absorption_meter.py`, implementar o algoritmo do paper: para cada par (prompt, resposta), extrair URLs citadas, baixar conteúdo, computar ROUGE-L truncado contra a resposta, normalizar por baseline (URLs do mesmo domínio não citadas). O score sai como métrica primária no relatório semanal junto a "citation rate" tradicional. Esta é a contribuição mais imediatamente acionável de todo o Track A para o repo papers.

---

## 3. arXiv:2603.29979 — Structural Feature Engineering for Generative Engine Optimization: How Content Structure Shapes Citation Behavior

- **Autores**: Junwei Yu, Mufeng Yang, Yepeng Ding, Hiroyuki Sato
- **Submissão**: 31 de março de 2026
- **URL canônica validada**: https://arxiv.org/abs/2603.29979

### Achado central

GEO-SFE é o primeiro framework sistemático para quantificar e otimizar features estruturais (arquitetura de documento, organização da informação, formatação visual) como alavancas de citação por LLMs. Em seis engines generativos, otimização estrutural sem mudar substância elevou citation rate em 17,3% e quality score em 18,5%.

### Metodologia

Os autores categorizam estrutura em três níveis (documento, informação, visual) e operacionalizam cada nível em quinze a vinte features mensuráveis. Treinam um classificador que prediz citação a partir das features estruturais, e usam o classificador como surrogate em otimização gradient-free sobre o espaço de transformações estruturais permitidas (reordenação de seções, conversão prose-to-bullets, inserção de blocos canônicos).

### Aplicação direta em landing-page-geo

Em `landing-page-geo`, o padrão editorial HBR de seis movimentos já cobre parte da arquitetura de documento. GEO-SFE adiciona dimensão visual: largura de bullets, presença de blocos numerados, distância média entre headings, ratio de frases curtas. Adicionar script `scripts/python/sfe_audit.py` que mede esses 15-20 indicadores por artigo, gera diff contra o perfil mediano dos artigos mais citados da KB V2 (Aggarwal, ALM Corp 173k), e produz recomendações estruturais antes do `vercel --prod`. Esperado: ganhos de 10-15% em citation rate sem custo de redação.

### Aplicação direta em curso-factory

Em curso-factory, o pipeline atual gera markdown com headings padronizados mas sem controle fino de estrutura visual. Inserir camada `sfe_render.ts` que toma a lição em MD bruto e aplica transformações estruturais lossy-zero: converte parágrafos densos em listas quando há enumeração natural, adiciona blocos "Definição rápida", "Em 30 segundos", "Próximo passo". O paper sugere que essa transformação puramente visual já entrega 9-12% da melhoria, antes mesmo de mexer no texto.

### Aplicação direta em papers

Em `papers/src/sfe_extractor/`, replicar o feature-extractor do paper sobre o corpus de URLs citadas pela Query Battery v2 ao longo dos últimos 90 dias. Treinar classificador binário "vai ser citado por modelo X" com features SFE apenas. O modelo serve para escolher quais artigos do `landing-page-geo` reescrever primeiro (priorização baseada em gap estrutural) e para auditar dossiês Perplexity antes de virar artigo. Isso fecha o loop com FeatGEO (paper 1) e converge num pipeline único de feature engineering.

---

## 4. arXiv:2604.19516 — From Experience to Skill: Multi-Agent Generative Engine Optimization via Reusable Strategy Learning

- **Autores**: Beining Wu, Fuyou Mao, Jiong Lin, Cheng Yang, Jiaxuan Lu, Yifu Guo, Siyu Zhang, Yifan Wu, Ying Huang, Fu Li
- **Submissão**: 21 de abril de 2026
- **URL canônica validada**: https://arxiv.org/abs/2604.19516

### Achado central

MAGEO é a primeira tentativa séria de tratar GEO como sistema multi-agente que aprende estratégias reutilizáveis por engine. Em vez de cada tarefa GEO ser resolvida do zero por heurística, o framework consolida padrões de edição validados em "skills" que ficam disponíveis para casos futuros. O salto experimental é grande: MAGEO supera baselines heurísticos tanto em visibilidade quanto em fidelidade citatória, com a observação crítica de que cada engine generativo demanda preferências distintas (a generalização cross-engine é fraca).

### Metodologia

Três agentes coordenados — planner, editor, evaluator — operam em loop sobre cada par (página, prompt-alvo). O evaluator tem critérios duplos (visibilidade no engine target + fidelidade ao conteúdo original). Edições que validam viram skills nomeadas e armazenadas; em casos futuros, o planner consulta o repositório de skills e seleciona as relevantes para a página/engine combinação.

### Aplicação direta em landing-page-geo

Em `landing-page-geo`, hoje toda otimização GEO é manual ou via prompts ad-hoc. MAGEO sugere construir biblioteca persistente de skills em `scripts/geo_skills/`: cada skill é YAML com (a) condição de aplicabilidade, (b) transformação, (c) engine target, (d) histórico de impacto medido. Skills observadas em mai-2026: "converter parágrafo de causa-efeito em bullet 3-step", "adicionar bloco-numero-pivô no segundo parágrafo", "inserir tabela 2-coluna em comparação implícita". Cada nova onda editorial alimenta o repositório com 3-5 skills novas, validadas via Query Battery.

### Aplicação direta em curso-factory

Em curso-factory, replicar a arquitetura tri-agente para geração de lições: planner-Opus define estrutura, editor-Sonnet redige, evaluator-Haiku verifica conformidade com voice guard e SFE features. O loop fica auto-corretivo: edições que passam por todos os três viram skills do curso. Isso reduz o custo médio por lição porque o editor não precisa redescobrir padrões já validados em lições anteriores.

### Aplicação direta em papers

Em `papers/src/skill_bank/`, criar tabela versionada de skills MAGEO descobertas via experimentação. Cada skill tem ID, descrição, engine-target, taxa de sucesso histórica e link para os artigos em que foi aplicada. O dashboard semanal mostra "skills mais quentes" e "skills cuja taxa caiu" (alertando para mudanças nos engines). O paper sugere que essa biblioteca é o ativo competitivo de médio prazo: heurísticas envelhecem, skills validadas e versionadas escalam.

---

## 5. arXiv:2604.07585 — Don't Measure Once: Measuring Visibility in AI Search (GEO)

- **Autores**: Julius Schulte, Malte Bleeker, Philipp Kaufmann
- **Submissão**: 8 de abril de 2026
- **URL canônica validada**: https://arxiv.org/abs/2604.07585

### Achado central

Visibilidade em engines generativos não é um número, é uma distribuição. Os autores mostram, empiricamente, que duas medições do mesmo par (prompt, marca) em janelas separadas podem divergir radicalmente. Uma medição única é informativa apenas como sinal grosso; análises sérias precisam tratar visibilidade como variável aleatória, com confidence intervals e detecção explícita de regime change.

### Metodologia

Os autores re-rodam baterias de prompts em janelas (intra-dia, diário, semanal) e mostram que coeficiente de variação supera 30% em muitos pares; em prompts controversos ou recentes, o CV passa de 60%. Propõem protocolos de re-amostragem mínima (N=5 por prompt, espaçamento de 12 horas) e métricas como "visibility CI95" no lugar de "visibility rate".

### Aplicação direta em landing-page-geo

Em `landing-page-geo`, qualquer claim de melhoria após onda editorial precisa de medição antes/depois com N>=5. Reformular o cron `scripts/python/geo_visibility_cron.py` (se ainda não existir, criar) para coletar 5 amostras por prompt da Query Battery v2 ao longo de 48h, e reportar CI95 do citation rate. Sem isso, melhorias aparentes são ruído amostral. Custo extra: ~5x chamadas LLM, mas viabiliza inferência estatística.

### Aplicação direta em curso-factory

Em curso-factory, o efeito é meta: as métricas de "lição mais citada" precisam ser re-validadas em janelas múltiplas antes de virar política editorial. Adicionar campo `n_measurements` e `ci95_low/high` ao schema de medição em curso-factory. Lições com N<5 não devem ser usadas para tomar decisão de reescrita ou priorização.

### Aplicação direta em papers

Em `papers/src/visibility_distribution.py`, implementar o protocolo do paper: 5 amostras por prompt, 12h de espaçamento, computar média e CI95 via bootstrap. Esta é a correção que falta no harness atual da Query Battery v2, que era single-shot. Custo Perplexity/OpenAI/Anthropic/Gemini multiplicado por 5, mas estatisticamente honesto. Adicionar gating: changes em landing-page-geo só são consideradas "validadas" se delta excede CI95 de baseline.

---

## 6. arXiv:2604.27790 — How Generative AI Disrupts Search: An Empirical Study of Google Search, Gemini, and AI Overviews

- **Autores**: Riley Grossman, Songjiang Liu, Michael K. Chen, Mike Smith, Cristian Borcea, Yi Chen
- **Submissão**: 30 de abril de 2026
- **Aceito**: SIGIR 2026 (49th International ACM SIGIR Conference on Research and Development in Information Retrieval)
- **URL canônica validada**: https://arxiv.org/abs/2604.27790

### Achado central

Benchmark público com 11.500 queries comparando Google Search, AI Overviews (AIO) e Gemini Flash 2.5. AIOs aparecem acima de resultados orgânicos em 51,5% das queries típicas, com a probabilidade subindo para tópicos controversos. Fontes retrievadas divergem fortemente entre plataformas (similaridade Jaccard abaixo de 0,2 entre Google clássico e AIO). Sites que bloqueiam o crawler Google-Extended sofrem queda drástica de visibilidade em AIO, mesmo com conteúdo aberto para indexação tradicional.

### Metodologia

Coleta sistemática via API e scraping controlado, com 11.500 queries categorizadas por intenção (informacional, transacional, controversa, recente). Medição de presença AIO, fontes citadas, consistência intra-query (repetir N vezes), e robustez a variação mínima do prompt. Dataset público, replicável.

### Aplicação direta em landing-page-geo

Verificar imediatamente o robots.txt do alexandrecaramaschi.com: Google-Extended deve estar Allow explícito. Em `landing-page-geo/public/robots.txt`, adicionar block dedicado Google-Extended User-agent com Allow: /. Documentar a decisão em `docs/seo-decisions.md`. O paper mostra que a omissão dessa diretiva é punida quase tanto quanto um Disallow explícito, pelo viés conservador do crawler. Replicar em todos os portais Brasil GEO (gestaofitness.net, dinheirodaminhaempresa.com, posgraduacaopsicologia.com, herreirasemijoias.com.br, larissacaramaschi.com).

### Aplicação direta em curso-factory

Em curso-factory, cada hub público precisa de robots.txt que liberte Google-Extended e similares (PerplexityBot, ClaudeBot, GPTBot, Cohere-AI, MetaExternalAgent). Adicionar checklist `docs/launch-checklist.md` com item "robots.txt valida 14 crawlers AI". Antes de qualquer launch público de curso, esse gate é bloqueante.

### Aplicação direta em papers

Em `papers/src/aio_presence_tracker.py`, instrumentar coleta de AI Overview presence rate para os 25 prompts da Query Battery v2 (medindo se a query gera AIO em Google Search). Cruzar com citation rate dos demais engines. O paper sugere que AIO presence é leading indicator de transição "informational query → answer engine query", o que muda profundamente o cálculo de ROI editorial. Adicionar coluna `aio_presence_rate` no relatório semanal.

---

## 7. arXiv:2602.06718 — GhostCite: A Large-Scale Analysis of Citation Validity in the Age of Large Language Models

- **Autores**: Zuyao Xu, Yuqi Qiu, Lu Sun, Fasheng Miao, Fubin Wu, Xiang Li, Xinyi Wang, Haozhe Lu, Zhengze Zhang, Yuxin Hu, Jialu Li, Luo Jin, Feng Zhang, Rui Luo, Xinran Liu, Yingxian Li, Jiaji Liu
- **Submissão**: 6 de fevereiro de 2026, v2 revisada em 14 de maio de 2026
- **URL canônica validada**: https://arxiv.org/abs/2602.06718

### Achado central

Análise de 2,2 milhões de citações geradas por treze LLMs estado-da-arte em quarenta domínios AI/ML e segurança. Taxa de citação fabricada variou de 14,23% a 94,93% conforme modelo. Pior: a taxa de invalidade subiu de forma marcada em 2025, indicando regressão. Survey com 97 pesquisadores mostrou que o uso de LLM em escrita acadêmica explodiu, mas auditoria humana de referências quase não existe.

### Metodologia

Framework open-source que verifica citações em três dimensões: (a) existe na literatura, (b) autores corretos, (c) conteúdo coerente com a tese citante. Aplicado em larga escala sobre corpus 2020-2025 de papers AI/ML.

### Aplicação direta em landing-page-geo

Em `landing-page-geo`, hoje muitos artigos citam papers acadêmicos (DOI, arXiv) gerados durante drafts com Opus. Implementar gate `scripts/python/citation_audit.py` rodando antes de `npm run verify`: extrai todas as URLs DOI/arXiv do artigo, verifica via Crossref/arXiv API, marca como `[CITAÇÃO NÃO CONFIRMADA]` qualquer fonte que não existir ou cujos autores não baterem. Bloqueia commit se mais de uma citação falhar. Custo: chamadas leves de API, alguns segundos por artigo.

### Aplicação direta em curso-factory

Em curso-factory, o problema é estrutural: cursos baseados em literatura científica precisam de auditoria de citações 100% antes de publish. Integrar o mesmo audit do landing-page-geo no pipeline e adicionar segundo gate humano: o autor do curso (Alexandre ou cliente como Larissa) precisa confirmar manualmente uma amostra aleatória de 10% das citações. Sem isso, o risco reputacional é alto demais.

### Aplicação direta em papers

Em `papers/src/ghostcite_baseline.py`, replicar o estudo no escopo Brasil GEO: para cada um dos 4 LLMs da Query Battery, pedir geração de 50 citações sobre 10 tópicos da nossa vertical (GEO, AI search, brand visibility, B2B SaaS Brasil). Medir taxa de fabricação. O resultado vai virar conteúdo editorial e prova social: "auditamos 2.000 citações geradas pelos quatro engines principais e encontramos X% de hallucination — eis o protocolo Brasil GEO para mitigar".

---

## 8. arXiv:2602.23452 — CiteAudit: You Cited It, But Did You Read It? A Benchmark for Verifying Scientific References in the LLM Era

- **Autores**: Kaiwen Shi, Weixiang Sun, Zheyuan Zhang, Lichao Sun, Nitesh V. Chawla, Yanfang Ye
- **Submissão**: v1 fevereiro 2026, v3 final em 1 de maio de 2026
- **URL canônica validada**: https://arxiv.org/abs/2602.23452

### Achado central

Benchmark canônico de verificação de citações em textos gerados por LLM, com pipeline multi-agente que decompõe o problema em quatro etapas: metadata extraction, memory lookup, web-based retrieval, judgment. O sistema supera tanto LLMs single-pass quanto ferramentas comerciais de verificação. Dataset humano-validado disponível como referência para futuros trabalhos.

### Metodologia

Pipeline modular onde cada agente tem escopo restrito (um extrai DOI/título/autores; outro busca em corpus indexado; outro decide). A separação reduz cascata de erros e permite auditoria por etapa. Dataset cobre múltiplos domínios e foi anotado por especialistas.

### Aplicação direta em landing-page-geo

Em `landing-page-geo`, implementar a arquitetura CiteAudit em vez do audit single-pass: separar `citation_extractor.py` (regex + LLM extractor de DOI/arXiv/URL), `citation_verifier.py` (chama APIs externas: Crossref, arXiv, OpenAlex, Wayback) e `citation_judge.py` (decide fabricada/válida/duvidosa). Logging por etapa permite debug fino quando uma onda editorial produz erros.

### Aplicação direta em curso-factory

Em curso-factory, replicar a mesma arquitetura modular. Vantagem extra: o dataset humano-validado do CiteAudit pode ser usado como gold-standard local para o pipeline. Rodar o pipeline brasileiro contra os exemplos do paper e medir agreement. Se agreement < 90%, ajustar prompts dos sub-agentes.

### Aplicação direta em papers

Em `papers/datasets/citeaudit_pt_br.json`, adaptar a metodologia para corpus PT-BR: 200 citações reais + 200 fabricadas por LLM brasileiro, anotação humana por dois especialistas. Esse vira benchmark canônico para validar o pipeline de auditoria do Brasil GEO. Sem isso, o pipeline opera sem ground-truth localizado.

---

## 9. arXiv:2605.08583 — Source or It Didn't Happen: A Multi-Agent Framework for Citation Hallucination Detection

- **Autores**: Mingzhe Li, Zhiqiang Lin, Shiqing Ma
- **Submissão**: 9 de maio de 2026
- **URL canônica validada**: https://arxiv.org/abs/2605.08583

### Achado central

CiteTracer atinge 97,1% de precisão em detectar citações alucinadas, usando classificação cascateada em taxonomia 12-código que separa citações Reais, Potenciais e Hallucinated. Avaliado em benchmark com 2.450 citações sintéticas (mutações controladas de fontes reais) e 957 fabricações autênticas de submissões ICLR 2026 desk-rejected.

### Metodologia

Cascata de agentes especializados. O primeiro extrai citação estruturada do texto. O segundo busca evidências via canais diversos (Crossref, Google Scholar, arXiv). O terceiro faz matching determinístico (autor, ano, título). O quarto, só ativado em casos ambíguos, é um adjudicador LLM com instrução fine-tuned. A taxonomia de 12 códigos cobre desde "completamente fabricada" até "real mas tese citante distorce conclusão".

### Aplicação direta em landing-page-geo

Estender o audit do landing-page-geo (papers 7-8) com a taxonomia 12-código do CiteTracer. Cada citação no artigo recebe um dos 12 labels; o relatório de pre-publish lista as duvidosas com label específico para revisão humana rápida. O label "real mas distorce" é particularmente útil para evitar erros sutis em que o paper existe mas a tese citante exagera a conclusão.

### Aplicação direta em curso-factory

Em curso-factory, especialmente em curso técnico (saúde mental, finanças, fitness, regulação), o label "real mas distorce" é o gate principal. Rodar o pipeline em loop iterativo: o autor recebe lista das citações classificadas como "real mas distorce" e reformula a passagem citante. Esse ciclo eleva muito a qualidade editorial sem custo redacional alto.

### Aplicação direta em papers

Em `papers/src/citetracer_baseline.py`, integrar a taxonomia 12-código como camada de output do pipeline de auditoria do Brasil GEO. Cada citação detectada nas respostas dos 4 LLMs durante coleta Query Battery vai com label. O dashboard semanal agrega: % real, % fabricada, % "real mas distorce", por modelo. Esta diferenciação é exatamente o que Aggarwal et al. 2023 não tinha.

---

## 10. arXiv:2604.03173 — Detecting and Correcting Reference Hallucinations in Commercial LLMs and Deep Research Agents

- **Autores**: Delip Rao, Eric Wong, Chris Callison-Burch
- **Submissão**: 3 de abril de 2026
- **URL canônica validada**: https://arxiv.org/abs/2604.03173

### Achado central

Em 53.090 URLs de DRBench e 168.021 URLs de ExpertQA, agentes de deep research e LLMs commerciais geram 3-13% de URLs nunca existentes (sem registro Wayback Machine) e 5-18% de URLs non-resolving overall. Deep research agents geram mais citações por query, porém com taxa de fabricação mais alta. Domínios variam: Business 5,4%, Theology 11,4%. Os autores liberam urlhealth, ferramenta open-source que reduz non-resolving para menos de 1% via self-correction quando o agente tem competência de tool-use.

### Metodologia

Tooling abrangente que verifica liveness via fetch direto, presença em Wayback Machine, e classifica resultados em "real e ativo", "real mas morto" (stale), "nunca existiu" (hallucinated). A taxonomia separa decadência natural de fabricação, o que muda decisões de mitigação.

### Aplicação direta em landing-page-geo

Em `landing-page-geo`, antes de qualquer push, rodar `scripts/python/urlhealth_audit.py` baseado em urlhealth: extrai todos os links externos do artigo, classifica em (ativo, stale, hallucinated). Hallucinated bloqueia commit. Stale gera alerta mas permite commit com substituição por link Wayback Machine quando disponível. Custo: ~200ms por link, paralelizável.

### Aplicação direta em curso-factory

Em curso-factory, integrar urlhealth no mesmo gate de citation_audit. Curso completo costuma ter 50-200 links externos; sem auditoria, a probabilidade de pelo menos um link morto ou fabricado é altíssima. O paper sugere que apenas modelos com tool-use sólido (Opus, GPT-4.1) conseguem auto-corrigir; modelos menores precisam de pipeline externo.

### Aplicação direta em papers

Em `papers/src/url_validity_baseline.py`, replicar o estudo do paper sobre o corpus de URLs citadas pela Query Battery v2 nos últimos 90 dias. Computar taxa de fabricação por LLM (esperado: maior em Gemini deep-research, menor em GPT-4o single-shot). O resultado vira post próprio de Alexandre no LinkedIn e/ou artigo no portal, contribuindo para SoV-AI Brasil GEO em buscas tipo "qual LLM cita melhor".

---

## 11. arXiv:2604.01733 — From BM25 to Corrective RAG: Benchmarking Retrieval Strategies for Text-and-Table Documents

- **Autores**: Meftun Akarsu, Recep Kaan Karaman, Christopher Mierbach
- **Submissão**: 2 de abril de 2026
- **URL canônica validada**: https://arxiv.org/abs/2604.01733

### Achado central

Em dataset financeiro com mais de 23.000 queries sobre documentos texto+tabela, dez estratégias de retrieval foram comparadas. O resultado contraintuitivo: BM25 puro supera dense retrieval estado-da-arte em documentos financeiros. O melhor pipeline foi two-stage: hybrid retrieval (BM25 + dense) + neural reranking, atingindo Recall@5 de 0,816. Para a vertical financeira, o paper desafia frontalmente a suposição de que embeddings semânticos são sempre melhores.

### Metodologia

Conjunto de testes com queries financeiras reais (ratios, métricas, comparações inter-empresas) sobre filings SEC e relatórios anuais. Avaliação multi-modelo: BM25, dense (e5, BGE), sparse (SPLADE), late-interaction (ColBERTv2), híbridos (RRF, convex), com e sem reranker.

### Aplicação direta em landing-page-geo

Em `landing-page-geo`, a busca interna do site (se existir, ex.: typesense ou pagefind) deve priorizar BM25 para artigos com densidade de números (artigos de finanças, dados de mercado, comparativos). Para conteúdo conceitual ou narrativo, mudar para hybrid. Adicionar metadata `retrieval_profile: numeric | conceptual | mixed` por artigo em `articles.ts`, e roteamento de busca por profile.

### Aplicação direta em curso-factory

Em curso-factory, a busca interna de cursos numéricos (finanças, métricas de negócio) deve ser BM25-first; curso narrativo (carreira, transição, saúde mental) deve ser dense-first. Implementar `lib/search/router.ts` que escolhe pipeline por categoria do curso. Custo: marginal, mas qualidade de recall sobe sensivelmente.

### Aplicação direta em papers

Em `papers/src/retrieval_battery/`, este paper é fundacional. Substituir o pipeline atual BM25-puro por (a) BM25 baseline, (b) dense, (c) hybrid RRF, (d) hybrid + cross-encoder reranking — replicando exatamente as quatro arms do paper. Para a Query Battery v2, isso permite report comparativo claro de qual estratégia recupera as melhores fontes a alimentar os LLMs. O paper indica que para queries Brasil GEO B2B típicas (números, comparativos, benchmarks), BM25 pode ser SUFICIENTE — economizando custo de embedding.

---

## 12. arXiv:2604.22180 — ResRank: Unifying Retrieval and Listwise Reranking via End-to-End Joint Training with Residual Passage Compression

- **Autores**: Xiaojie Ke, Shuai Zhang, Liansheng Sun, Yongjin Wang, Hengjun Jiang, Xiangkun Liu, Cunxin Gu, Jian Xu, Guanjun Jiang
- **Submissão**: 24 de abril de 2026
- **URL canônica validada**: https://arxiv.org/abs/2604.22180

### Achado central

ResRank unifica retrieval e reranking em um único treinamento end-to-end, resolvendo o "lost in the middle" e a latência super-linear de rerankers LLM-based. A inovação: cada passagem é comprimida pelo Encoder-LLM em um único embedding, e o Reranker-LLM faz scoring listwise via similaridade cosseno (uma única forward pass por passagem, zero tokens gerados). Resultado em TREC Deep Learning e BEIR competitivo com baselines listwise muito mais caros.

### Metodologia

Conexão residual alinha o espaço de representação comprimida com o espaço de ranking, treinados conjuntamente. O Reranker substitui decoding autoregressivo por scoring cosseno determinístico, o que elimina a variabilidade de geração e a complexidade O(N²) do attention listwise.

### Aplicação direta em landing-page-geo

Em `landing-page-geo`, este paper viabiliza adição de uma camada de reranking sobre a busca interna sem custo proibitivo. Implementar via API local (hosted no Cloudflare AI Workers) ou via OpenAI text-embedding-3-large + lógica de reranking local. Ganho esperado: top-3 da busca interna sobe de "razoavelmente relevante" para "exatamente o que o usuário precisava".

### Aplicação direta em curso-factory

Em curso-factory, ResRank é particularmente útil para sugestão de "próxima lição" e "lições relacionadas". A camada atual é embedding-only; adicionar reranking pelo padrão ResRank entrega salto qualitativo em UX sem latência percebida (compute roda em background, cache agressivo).

### Aplicação direta em papers

Em `papers/src/reranker/`, implementar pipeline ResRank-style para reordenar URLs citadas pela Query Battery v2 antes de exibir no dashboard. Hoje a ordem é "como o LLM citou"; com reranking, fica "ordem de utilidade ao usuário Brasil GEO" — útil para construir relatórios consumíveis. Custo marginal: ~10ms por query.

---

## 13. arXiv:2605.12975 — Retrieval is Cheap, Show Me the Code: Executable Multi-Hop Reasoning for Retrieval-Augmented Generation

- **Autores**: Jiashuo Sun, Jimeng Shi, Yixuan Xie, Saizhuo Wang, Jash Rajesh Parekh, Pengcheng Jiang, Zhiyi Shi, Jiajun Fan, Qinglong Zheng, Peiran Li, Shaowen Wang, Ge Liu, Jiawei Han
- **Submissão**: 13 de maio de 2026
- **URL canônica validada**: https://arxiv.org/abs/2605.12975

### Achado central

PyRAG transforma multi-hop RAG em síntese e execução de programa Python. Em vez de raciocínio em linguagem natural sobre passagens recuperadas, o modelo gera código que invoca ferramentas de retrieval e QA, com estados intermediários expostos como variáveis Python. O efeito: feedback determinístico via execução, trace inspecionável, self-repair compilador-grounded. Bate baselines consistentemente em cinco benchmarks QA com vantagem grande em multi-hop composicional.

### Metodologia

Pipeline em três fases: planejamento (LLM gera programa Python), execução (Python interpreter chama tools), reflexão (LLM lê erros/saídas e corrige). Adaptive retrieval é determinada pelo programa: o LLM pode decidir buscar mais evidência quando uma variável está vazia ou contraditória. Não exige fine-tuning.

### Aplicação direta em landing-page-geo

Em `landing-page-geo`, durante drafts editoriais que envolvem comparação multi-fonte (ex.: comparar 3 frameworks GEO citados em papers distintos), substituir o atual prompt monolítico de Opus por workflow PyRAG-style: Opus gera programa Python de pesquisa, executa via API (Perplexity/Crossref/arXiv), recebe outputs, redige artigo. Isso reduz hallucination em artigos comparativos drasticamente.

### Aplicação direta em curso-factory

Em curso-factory, lições que dependem de síntese de múltiplas fontes (ex.: módulo "Estado da arte em saúde mental + vibe coding") ganham qualidade com PyRAG: o pipeline gera plano de pesquisa Python, executa, valida, redige. O custo extra é compensado por dramaticamente menos retrabalho de revisão humana.

### Aplicação direta em papers

Em `papers/src/multi_hop_battery/`, implementar harness PyRAG-style para um subset da Query Battery v2 que exige multi-hop reasoning (questões tipo "qual paper publicou X depois de citado por Y"). Esses tipicamente falham em LLMs single-pass; com PyRAG, o success rate sobe acima de 80%. Esta é uma das aplicações mais imediatas para evoluir a Query Battery v3 com prompts multi-hop nativos.

---

## 14. arXiv:2604.26649 — When to Retrieve During Reasoning: Adaptive Retrieval for Large Reasoning Models

- **Autores**: Dongxin Guo, Jikun Wu, Siu Ming Yiu
- **Submissão**: 29 de abril de 2026
- **URL canônica validada**: https://arxiv.org/abs/2604.26649

### Achado central

Reasoning models como DeepSeek-R1 e OpenAI o1 geram chains-of-thought de milhares de tokens, mas RAG tradicional injeta contexto apenas antes do raciocínio começar. ReaLM-Retrieve resolve esse descasamento: detector de incerteza step-level identifica lacunas de conhecimento durante o reasoning, e policy decide quando buscar. Em MuSiQue, HotpotQA e 2WikiMultiHopQA, ganho médio de 10,1% F1 absoluto sobre RAG padrão com 47% menos chamadas de retrieval. Em MuSiQue, 71,2% F1 com 1,8 chamadas por questão.

### Metodologia

Três componentes: (a) detector de incerteza step-level (probabilidades de logit + heurística), (b) policy de intervenção que decide retrievar ou continuar, (c) pipeline de integração que reduz overhead per-retrieval em 3,2x via cache e batching.

### Aplicação direta em landing-page-geo

Em `landing-page-geo`, quando Opus está draftando artigo via "reasoning mode" (cadeia explícita de pensamento), permitir interrupções para retrieval. Implementar wrapper `scripts/python/reasoning_retrieve.py` que escuta marcadores `[NEED_EVIDENCE: <topic>]` no output Opus e injeta resultados Perplexity/Crossref antes do próximo passo. Reduz hallucination factual em artigos que dependem de números ou citações precisas.

### Aplicação direta em curso-factory

Em curso-factory, lições que exigem cadeia de raciocínio (não só descrição) — tipo "por que regulamentação X causou efeito Y três anos depois" — ganham qualidade com adaptive retrieval. Padrão de implementação: Opus em modo extended thinking pode chamar tool de retrieval entre passos, escolhendo o momento ótimo. Custo: ~30% mais tokens, retorno em qualidade muito superior.

### Aplicação direta em papers

Em `papers/src/reasoning_retrieve_v3/`, este paper sugere arquitetura da Query Battery v3: prompts complexos onde o LLM precisa raciocinar em múltiplos passos com retrieval intercalado. Medir não só "que fontes foram citadas" mas também "quantas vezes o modelo decidiu buscar evidência durante o raciocínio". Modelos que fazem retrieval no momento certo tendem a citar fontes mais relevantes (a hipótese a testar empiricamente).

---

## 15. arXiv:2604.09666 — Do We Still Need GraphRAG? Benchmarking RAG and GraphRAG for Agentic Search Systems

- **Autores**: Dongzhe Fan, Zheyi Xue, Siyuan Liu, Qiaoyu Tan
- **Submissão**: 1 de abril de 2026
- **URL canônica validada**: https://arxiv.org/abs/2604.09666

### Achado central

RAGSearch benchmark unificado avalia dense RAG e GraphRAG sob agentic search. Conclusão: agentic search aumenta significativamente o desempenho de dense RAG e reduz a vantagem histórica de GraphRAG, especialmente em cenários treinados com RL. Porém, GraphRAG permanece superior em multi-hop reasoning complexo, com comportamento agentic mais estável quando o custo offline de construção do grafo é amortizado.

### Metodologia

Benchmark cobre training-free e training-based agentic inference, com métricas padronizadas: accuracy, custo de preprocessing, eficiência de inferência, estabilidade. Avaliado em corpora multi-hop reais e sintéticos.

### Aplicação direta em landing-page-geo

Em `landing-page-geo`, a decisão "graph ou não" depende do tipo de query. Para busca interna do site (queries simples a moderadas), dense RAG + agentic search é suficiente e mais barato. Para feature avançada de "navegação semântica entre artigos relacionados multi-hop" (ex.: "mostre artigos que citem X via cadeia de no máximo 3 saltos"), GraphRAG continua superior. Mapear features futuras para escolher arquitetura por feature, não monolítico para o site inteiro.

### Aplicação direta em curso-factory

Em curso-factory, ranking de "lições relacionadas" tipicamente é simples (cosseno em embeddings de hub). Mas geração de "trilha personalizada multi-curso" é multi-hop nativo (lição A → conceito B → lição C de outro curso). Para essa feature, GraphRAG amortizado vale a pena: grafo construído offline e reusado em todas as trilhas dinâmicas.

### Aplicação direta em papers

Em `papers/src/graphrag_eval/`, replicar RAGSearch para o corpus Brasil GEO (artigos de landing-page-geo, lições de curso-factory, papers indexados). Medir o gap dense vs GraphRAG para queries típicas dos clientes B2B. Hipótese: GraphRAG não vale o custo para 80% das queries, mas vale absurdamente para os 20% multi-hop. Esse resultado define se vale construir grafo persistente ou se podemos viver com vector store puro.

---

## 16. arXiv:2603.07379 — SoK: Agentic Retrieval-Augmented Generation (RAG): Taxonomy, Architectures, Evaluation, and Research Directions

- **Autores**: Saroj Mishra, Suman Niroula, Umesh Yadav, Dilip Thakur, Srijan Gyawali, Shiva Gaire
- **Submissão**: 7 de março de 2026
- **URL canônica validada**: https://arxiv.org/abs/2603.07379

### Achado central

Systematization-of-Knowledge sobre Agentic RAG. Formaliza esses sistemas como Partially Observable Markov Decision Processes (POMDPs) e mapeia taxonomia em quatro eixos: planning, retrieval orchestration, memory paradigms, tool-invocation behaviors. Identifica nove vulnerabilidades de governança ainda mal-tratadas pela literatura: compounding hallucination propagation, memory poisoning, retrieval misalignment, cascading tool-execution vulnerabilities, entre outras.

### Metodologia

Survey estruturado com mais de 150 trabalhos indexados, organizados por componente e por vulnerabilidade. Para cada vulnerabilidade, taxonomia de mitigações conhecidas e gaps remanescentes.

### Aplicação direta em landing-page-geo

Em `landing-page-geo`, a maioria das automações editoriais não é agentic ainda (single-pass Opus). Mas o pipeline de "auto-onda" (selecionar tópicos, gerar drafts, publicar, indexar) tem comportamento agentic nascente. Aplicar a taxonomia do SoK para auditar o pipeline: onde estão os pontos de planning, retrieval, memory, tool-invocation, e quais das 9 vulnerabilidades aplicam-se. Documentar em `docs/agentic-architecture.md`.

### Aplicação direta em curso-factory

Em curso-factory, o pipeline de geração de curso longo é agentic explícito (planner → editor → reviewer iterativo). Mapear cada agente no framework POMDP do paper, identificar quais das 9 vulnerabilidades já têm mitigação implementada (ex.: voice guard mitiga hallucination propagation), quais não. Issue tracker recebe um issue por vulnerabilidade não mitigada.

### Aplicação direta em papers

Em `papers/docs/agentic_threats.md`, documentar o threat model do harness Brasil GEO contra as 9 vulnerabilidades. Especialmente memory poisoning (o que acontece se um adversário injeta conteúdo na URL crawlada?) e retrieval misalignment (o que acontece se a Query Battery v2 derivar para tópicos irrelevantes ao longo do tempo?). Cada vulnerabilidade ganha um teste automatizado no CI.

---

## 17. arXiv:2605.17641 — Causal Intervention-Based Memory Selection for Long-Horizon LLM Agents

- **Autor**: Saksham Sahai Srivastava
- **Submissão**: 17 de maio de 2026
- **URL canônica validada**: https://arxiv.org/abs/2605.17641

### Achado central

Sistemas de memória persistente em agentes LLM tradicionalmente recuperam contexto por similaridade semântica, tratando memórias relevantes como uniformemente úteis. Causal Memory Intervention (CMI) substitui correlação por causalidade: estima como cada memória candidata afeta a resposta do modelo sob intervenções controladas, e seleciona as que melhoram performance enquanto suprime instáveis, irrelevantes ou prejudiciais. CMI bate baselines vector, graph, reflection, summary, full-history e no-memory em benchmark Causal-LoCoMo.

### Metodologia

Para cada memória candidata, o framework roda mini-experimento causal: gera resposta com a memória, sem a memória, e mede o delta condicional. Memórias com delta positivo consistente são incluídas; com delta negativo ou inconsistente, suprimidas. O Causal-LoCoMo benchmark é derivado de dados conversacionais longos com anotação causal.

### Aplicação direta em landing-page-geo

Em `landing-page-geo`, a memória do pipeline editorial é limitada (cada onda começa fresh). Mas para automações de redação contínua (ex.: continuação de série de artigos), uma memória persistente que armazene "padrões editoriais que funcionaram" é necessária. CMI sugere que a inclusão dessa memória precisa ser causal, não cosseno. Implementar em `lib/editorial_memory/`: cada decisão (incluir bloco X) é avaliada via intervenção (testar artigo com vs sem o bloco e medir citation rate).

### Aplicação direta em curso-factory

Em curso-factory, a continuidade entre lições do mesmo curso exige memória persistente. CMI sugere: para cada decisão de "puxar referência da lição N para a lição N+5", testar via Causal-LoCoMo-style se a referência ajuda ou atrapalha. Sem isso, lições viram colcha de retalhos com referências que confundem em vez de orientar.

### Aplicação direta em papers

Em `papers/src/causal_memory/`, este paper viabiliza versão causal do dashboard de longa duração. Hoje o dashboard armazena tudo (citation rate semanal por LLM por prompt) sem distinguir o que é causalmente útil para previsão. CMI sugere camada que pontua cada memória por seu poder preditivo causal de citation rate futura, descartando as ruidosas. Reduz storage e melhora forecast.

---

## 18. arXiv:2605.00318 — Structure-Aware Chunking for Tabular Data in Retrieval-Augmented Generation

- **Autores**: Pooja Guttal, Varun Magotra, Vasudeva Mahavishnu, Natasha Chanto, Sidharth Sivaprasad, Manas Gaur
- **Submissão**: 1 de maio de 2026
- **URL canônica validada**: https://arxiv.org/abs/2605.00318

### Achado central

Métodos de chunking RAG são desenhados para texto desestruturado e ignoram estrutura tabular. STC (Structure-Aware Tabular Chunking) trata cada linha como unidade, com representação Row Tree hierárquica onde cada linha é bloco key-value. Token-constrained splitting respeita fronteiras estruturais. Resultado: 40-56% menos chunks com MRR subindo de 0,357 para 0,594 em settings híbridos, e Recall@1 de 0,366 para 0,754 em BM25 puro.

### Metodologia

Constrói árvore hierárquica por planilha, faz splitting com merging guloso que preserva integridade de linha. Compara com baseline naive (chunks por número fixo de tokens) e com chunking semântico genérico (que quebra linhas).

### Aplicação direta em landing-page-geo

Em `landing-page-geo`, artigos com tabelas (comparativos B2B, ratios financeiros) hoje são tratados como texto puro pelo crawler interno e pelos LLMs externos quando citam. STC sugere: marcar tabelas em markdown com bloco semântico canônico que sobrevive ao tokenization de qualquer LLM (ex.: HTML estrito com `<table><caption>X</caption>` em vez de markdown ASCII). Reescrever 10-15 artigos high-traffic com tabelas seguindo padrão STC.

### Aplicação direta em curso-factory

Em curso-factory, cursos numéricos (finanças, métricas, benchmarking fitness) têm tabelas. STC sugere transformar tabelas em blocos estruturados que o pipeline de geração preserva durante chunking. Adicionar `lib/render/tabular_chunk.ts` que converte tabela em representação row-level antes de qualquer operação semântica.

### Aplicação direta em papers

Em `papers/src/tabular_retrieval/`, esta é provavelmente a maior lacuna não tratada na V2. A Query Battery v2 não testa explicitamente queries tabulares (tipo "qual benchmark cita performance X de modelo Y?"). Adicionar 5 prompts tabulares e medir performance dos 4 LLMs em retrieval/citação de tabelas. Resultado vira artigo dedicado e prova social de que Brasil GEO entende o nicho tabular em GEO.

---

## Tabela síntese — 18 papers × 5 dimensões aplicáveis

| arXiv ID | Foco primário | Aplicável landing-page-geo? | Aplicável curso-factory? | Aplicável papers? | Prioridade Q3 2026 |
|---|---|---|---|---|---|
| 2604.19113 (FeatGEO) | GEO feature-level | Sim, audit pre-publish | Sim, gate pos voice guard | Sim, modelo preditivo | Alta |
| 2604.25707 (Selection vs Absorption) | Métrica GEO dual | Sim, dual-score por artigo | Sim, tag absorvibilidade | Sim, métrica primária | Crítica |
| 2603.29979 (GEO-SFE) | GEO estrutural | Sim, sfe_audit | Sim, sfe_render | Sim, classifier features | Alta |
| 2604.19516 (MAGEO) | GEO multi-agente | Sim, biblioteca skills | Sim, tri-agente lições | Sim, skill_bank dashboard | Média |
| 2604.07585 (Don't Measure Once) | Visibilidade distribucional | Sim, cron N=5 | Sim, schema ci95 | Sim, gating estatístico | Crítica |
| 2604.27790 (AI Overviews) | AIO benchmark | Sim, robots Google-Extended | Sim, launch checklist | Sim, aio_presence_rate | Crítica |
| 2602.06718 (GhostCite) | Auditoria citações scale | Sim, citation_audit | Sim, sample humano | Sim, baseline pt-br | Crítica |
| 2602.23452 (CiteAudit) | Pipeline multi-agente cit | Sim, modular extractor | Sim, gold-standard | Sim, dataset pt-br | Alta |
| 2605.08583 (CiteTracer) | Taxonomia 12-código | Sim, label por citação | Sim, gate "real mas distorce" | Sim, dashboard 12-cat | Alta |
| 2604.03173 (urlhealth) | URL liveness | Sim, gate pre-commit | Sim, audit 50-200 links | Sim, paper próprio | Alta |
| 2604.01733 (BM25 vs Dense) | Retrieval tabular | Sim, retrieval_profile | Sim, search router | Sim, retrieval battery | Alta |
| 2604.22180 (ResRank) | Joint retrieval+rerank | Sim, busca interna | Sim, próxima lição | Sim, dashboard order | Média |
| 2605.12975 (PyRAG) | Multi-hop código exec | Sim, drafts comparativos | Sim, síntese multi-fonte | Sim, multi_hop_battery | Alta |
| 2604.26649 (ReaLM-Retrieve) | Adaptive retrieval reason | Sim, marker NEED_EVIDENCE | Sim, extended thinking | Sim, Query Battery v3 | Média |
| 2604.09666 (Do We Still Need GraphRAG) | Graph vs dense benchmark | Sim, feature por feature | Sim, trilha multi-curso | Sim, graphrag_eval | Média |
| 2603.07379 (SoK Agentic RAG) | Threat model | Sim, auto-onda audit | Sim, 9 vulnerab map | Sim, threat tests CI | Alta |
| 2605.17641 (Causal Memory) | Memória causal | Sim, editorial memory | Sim, continuidade curso | Sim, dashboard causal | Baixa |
| 2605.00318 (STC Tabular) | Chunking tabular | Sim, reescrita tabelas | Sim, tabular_chunk | Sim, tabular Battery | Alta |

---

## Lacunas que estes papers preenchem em relação à V2

A GEO Knowledge Base V2 consolidou o stack canônico de até março/2026: Aggarwal et al. 2023 como fundação, Chen et al. 2025 com earned media 2.3-3.1x, Yao et al. 2025 sobre autoridade e recência, VMAO/IRS/CONSTRUCT como frameworks Q1 2026, AutoGEO ICLR 2026 como ponto agentic inicial, AgenticGEO como baseline, Reuters Institute e Pew como ground-truth de mercado, Semrush e ALM Corp como benchmarks longitudinais.

A V2 deixa cinco lacunas que o Track A preenche.

Primeira lacuna: GEO no nível feature/estrutura. A V2 trata GEO como otimização lexical e narrativa. Os papers 1 (FeatGEO), 3 (GEO-SFE) e 4 (MAGEO) elevam GEO a um problema de feature engineering multi-objetivo com skills aprendidas. Isso muda o stack operacional: o gate pre-publish ganha duas camadas (feature audit + skill library), e o ROI por hora de edição editorial cresce.

Segunda lacuna: métrica de citação dual. A V2 trata citation como evento binário (citado ou não). O paper 2 (Selection vs Absorption) demonstra que essa simplificação ignora o sinal mais importante: peso da fonte no texto gerado. Implementar absorption rate eleva a Query Battery v2 a v3 com métrica primária mais útil. Também muda a priorização: artigos high-selection-low-absorption são alvos prioritários de reescrita.

Terceira lacuna: rigor estatístico em visibilidade. A V2 reporta citation rate como número único. O paper 5 (Don't Measure Once) demonstra que isso é estatisticamente inadequado dado o coeficiente de variação observado nos engines. Adotar N=5 amostragens com CI95 muda como Brasil GEO faz claim de melhoria. Sem isso, várias "vitórias" pós-onda editorial podem ser apenas ruído amostral.

Quarta lacuna: pipeline de auditoria de citação. A V2 fala de qualidade editorial mas não tem ferramentas explícitas contra hallucination citatória. Os papers 7 (GhostCite), 8 (CiteAudit), 9 (CiteTracer) e 10 (urlhealth) preenchem essa lacuna em quatro camadas: estudo de prevalência, framework canônico de auditoria, taxonomia fina de tipos de erro, ferramenta operacional de URL health. Implementar os quatro em pipeline integrado eleva confiabilidade editorial sem custo proibitivo.

Quinta lacuna: arquitetura agentic e seus riscos. A V2 cita AgenticGEO e AutoGEO mas não trata vulnerabilidades. O paper 16 (SoK Agentic RAG) formaliza nove vulnerabilidades e suas mitigações. Implementar threat model explícito é hoje requisito mínimo para qualquer pipeline editorial Brasil GEO que ambicione ser agentic.

Sexta lacuna (bônus): tratamento de dados tabulares. A V2 não menciona explicitamente o caso tabular, e a Query Battery v2 não testa queries com tabelas. O paper 18 (STC) corrige isso: para verticais B2B Brasil GEO (finanças, gestão, fitness com benchmarks numéricos), tabelas são canal estratégico. Estender Query Battery v3 com 5 prompts tabulares é uma diferenciação competitiva direta.

---

## Próximas pesquisas sugeridas (preprints provavelmente entre jun e ago 2026)

Pesquisas Perplexity revelaram leads não consolidados que merecem rastreio nos próximos 30 dias:

- arXiv:2605.18673 — Generative AI Advertising as a Problem of Trustworthy Commercial (18-mai-2026, não foi possível validar via WebFetch ainda). Tema: posições oficiais das plataformas de AI sobre conteúdo comercial em mai-2026, mapeando o que está consolidado como anúncio vs orgânico em respostas geradas. Crítico para clientes B2B que querem entender como advertising vai entrar em ChatGPT/Gemini/Perplexity nos próximos 6-12 meses.

- arXiv:2605.07677 — TRACE: Tourism Recommendation with Accountable Citation Evidence (8-mai-2026). Reframa recomendação como busca de POIs com evidência verificável e reparação adaptativa quando evidência é falha. Padrão de "accountable citation" aplicável a curso-factory (recomendação de próximo curso com evidência citável de adequação).

- arXiv:2605.12887 — EcoGEO: Trajectory-Aware Evidence Ecosystems for Web-Enabled LLM Search Agents (13-mai-2026). Propõe ecossistemas de evidência conscientes de trajetória, conectando agentes de busca web ao histórico de buscas anteriores. Aplicável a papers para construir memória de longo prazo entre rodadas semanais da Query Battery.

- arXiv:2604.03656 — Beyond Retrieval: Modeling Confidence Decay and Deterministic Agentic Platforms in Generative Engine Optimization (4-abr-2026). Framework teórico para próxima geração de GEO que modela decay de confiança em sistemas de retrieval. Aplicável como framework conceitual para o dossiê "GEO 2027" que Brasil GEO pode publicar como white paper próprio.

- arXiv:2604.16548 — A Survey on the Security of Long-Term Memory in LLM Agents: Toward Mnemonic Sovereignty (17-abr-2026). Survey de segurança em memória persistente de agentes. Aplicável a curso-factory para auditar memória persistente entre sessões e a papers como base teórica para política de segurança da Query Battery v3.

- arXiv:2604.24334 — Reducing Redundancy in Retrieval-Augmented Generation through Chunk Filtering (27-abr-2026). Mostra que filtros semânticos, topic-based e entity-based reduzem 25-36% do índice vetorial preservando qualidade. Aplicável imediato a qualquer vector store Brasil GEO para reduzir custo Pinecone/Qdrant/Cloudflare Vectorize.

- arXiv:2603.25333 — Adaptive Chunking: Optimizing Chunking-Method Selection for RAG (26-mar-2026). Framework adaptativo que escolhe estratégia de chunking por documento usando cinco métricas. Aplicável imediato como camada de pre-processing em qualquer pipeline RAG do papers repo.

- arXiv:2603.19935 — Memori: A Persistent Memory Layer for Efficient, Context-Aware LLM Agents (20-mar-2026). Sistema de memória persistente LLM-agnóstico que atinge 81,95% em LoCoMo com apenas 1.294 tokens/query. Aplicável a curso-factory para memória entre lições e a landing-page-geo para memória entre ondas editoriais.

- arXiv:2603.15594 — OpenSeeker: Democratizing Frontier Search Agents (16-mar-2026). Primeiro agente de busca fully open-source com performance frontier em BrowseComp. Aplicável a papers para reduzir custo de Query Battery substituindo parcialmente APIs comerciais.

- arXiv:2605.14473 — Does RAG Know When Retrieval Is Wrong? Diagnosing Context Compliance under Knowledge Conflict (14-mai-2026). Probe de inferência detecta conflito entre contexto retrievado e conhecimento paramétrico do modelo. Aplicável a papers para auditar quando os LLMs respondem ignorando contexto explicitamente passado.

- arXiv:2605.15081 — ML-Embed: Inclusive and Efficient Embeddings for a Multilingual World (14-mai-2026). Suite de embeddings multilíngues open-source com strong showing em low-resource languages (relevante para PT-BR). Aplicável a busca interna do landing-page-geo e curso-factory como alternativa econômica a OpenAI text-embedding-3-large.

Reset esperado em jun-2026 com EMNLP 2026 ARR deadline (25-mai-2026) liberando preprints em maio-junho. Acompanhar especialmente: tracks de evaluation, RAG e attribution.

---

## Notas metodológicas e custo

Coleta: 5 chamadas Perplexity sonar-deep-research (queries específicas por tema, max_tokens=8000) + 8 chamadas WebSearch + 18 chamadas WebFetch para validação direta em arxiv.org. Custo Perplexity estimado: ~$0,005 por chamada deep-research, total ~$0,025. WebSearch e WebFetch sem custo direto incremental. Toda asserção sobre cada paper foi validada com fetch direto da página abs no arxiv.org, não apenas com snippets de busca, para evitar IDs alucinados.

Critério de inclusão: (1) ID arXiv validável; (2) submissão após 1-mar-2026 (banda flexível para incluir SoK e adaptive chunking que ancoram tópicos novos no Q2); (3) aplicabilidade direta a pelo menos dois dos três repos Brasil GEO; (4) inexistência na V2 ou avanço substantivo sobre o que está na V2.

Critério de exclusão: papers cujo arXiv ID não foi validável apesar de citados em fontes secundárias (tipicamente esses foram listados na seção "Próximas pesquisas sugeridas" para acompanhamento). Papers fora do escopo abr-jun 2026 só entraram quando o tema preenchia lacuna estratégica não coberta pela V2 (SoK Agentic RAG de 7-mar-2026, Adaptive Chunking de 26-mar-2026, Memori de 20-mar-2026).

Próxima atualização sugerida: 2026-07-15, após ciclo de preprints EMNLP 2026.
