# Wave Setembro 2026 · GEO + SEO: consolidação maio a setembro, frameworks de execução, KPIs e reports (03-set-2026)

**Data:** 03-set-2026 · **Janela:** delta 27-ago → 03-set-2026 sobre um corpus consolidado de maio a setembro de 2026 · **Método:** cinco provedores com web ao vivo mais doublecheck do Claude em fonte primária. Gemini 3.1 Pro grounding ×2, xAI `grok-4.6` Agent Tools API (`x_search` + `web_search`) ×1, OpenAI `gpt-5.5` Responses + `web_search` ×2 concluídas (camada semântico-vetorial e lançamentos de modelos; o briefing executivo e cinco rodadas caíram por ReadTimeout aos 900 s, sem erro HTTP), Perplexity **web** (conta alexandre.brt14@gmail.com, plano gratuito, navegador logado por CDP, respostas de 9 a 18 mil caracteres com fontes) ×7 como substituto da API. A API do Perplexity respondeu `401 insufficient_quota` nas duas chaves e nos dois endpoints (`chat/completions` e `/v1/agent`): crédito zerado, não chave inválida. O Claude abriu a listagem de busca do arXiv (seis consultas, ordenação por data de anúncio), conferiu 24 IDs na página `abs` com pausa de 3 s, e abriu 49 URLs de vendor, motor e imprensa com string-sentinela. Proveniência em `raw/`.

**Precedência:** cadeia vigente: **Setembro §8 > Agosto §8 > Julho-22C §7 > Julho-22B §7 > Julho-22 §7 > Julho §7 > Wave 19 §7 > 15B §8**. Esta wave (a) fecha o inventário científico de maio a setembro com 23 papers abertos, 8 deles da última semana; (b) registra a virada dos motores para medição oficial (relatório de IA do Search Console para todos os sites) e para comércio por feed (ChatGPT 5.6); (c) entrega a versão 2 do framework de execução, com regra de parada de coleta baseada em convergência e com a separação por motor que a evidência exige; (d) consolida o report em três níveis, reconciliando o "GEO URL Ledger" da Wave Agosto com o modelo que a Semrush publicou em 02-set.

---

## 0. TL;DR: o que muda para uma operação de GEO brasileira

1. **A medição oficial chegou e é só impressão.** Em 31-ago-2026 o Google liberou o relatório de desempenho em IA generativa do Search Console para todos os sites do mundo, junto com o controle de exclusão das superfícies de IA (AI Overviews, AI Mode, Discover). O relatório traz impressões por página, país, dispositivo e data; não traz cliques nem consultas (Search Console Help, primária). A camada 2 de medição (infra) deixa de ser "em rollout" e vira linha obrigatória do report (§2.1, §5.1).
2. **O modelo por trás do AI Mode muda dentro de um ciclo de report.** Gemini 3.7 Flash entrou no AI Mode em meados de agosto e o Gemini 3.8 Flash em 02-set (blog do Google, primária; disponível para assinantes Pro e Ultra pelo menu de modelo). Em 03-set a comunidade registrou respostas do 3.8 Flash sem links (Search Engine Roundtable, secundária). Toda medição de citação no AI Mode passa a declarar o modelo ativo, ou não compara nada (§2.1, §5.2).
3. **ChatGPT virou canal pago de escala e a resposta orgânica continua separada.** Em 31-ago a OpenAI declarou US$ 1 bilhão de receita anualizada em anúncios em menos de 200 dias, mais de 40 países, maioria das campanhas em CPC ou lance por resultado, autoatendimento aberto a Índia, Europa, Oriente Médio e Norte da África (OpenAI, primária). No Brasil, os primeiros anúncios apareceram em 04-ago e o Ads Manager abriu em 06-ago (Meio & Mensagem, primária de imprensa). A trilha "pago em IA" do report ganha número próprio: 26% das respostas do ChatGPT no desktop dos EUA tinham anúncio em junho, CTR de 0,50% (Similarweb, 03-set) (§2.2, §5.3).
4. **No comércio, o feed passou a valer mais que a página.** Após o GPT 5.6 (09-jul), a recuperação por feed integrado no Shopping do ChatGPT saltou de 8,26% para 61,54% das recomendações em um dia, e os 10 maiores lojistas subiram de 22,5% para 41,8% da participação; lojistas únicos caíram mais de 20% (Profound, 03-set, 687 clientes, jul a ago). Sem feed (Merchant Center, Shopify, UCP), o produto não entra na resposta (§2.2, §4 etapa 6).
5. **Reddit saiu de vez da lista de fontes estáveis.** Citações ao Reddit no ChatGPT caíram de 3,8% para 0,5% entre 18-jul/07-ago e 14/17-ago, queda de 86% em quatro dias (Promptwatch via Semrush, 26-ago). O ChatGPT continua a buscar subreddits por nome, com janela de até 3.650 dias, e pode buscar 84 threads e citar zero (Suganthan, SEJ 25 e 27-ago). Buscar não é citar: a fonte vira insumo invisível (§2.2, §8.e).
6. **Marca recomendada não é marca citada.** Em 60 categorias de compra, páginas próprias da marca foram 2,8% de 1.851 fontes citadas por AI Mode, ChatGPT e Perplexity; 59% foram sites de terceiros (Shero Commerce, 26-ago, secundária). Em três indústrias, comunidade e conteúdo de usuário são cerca de metade das citações (Trendos, 107 milhões de respostas, 27-ago, conteúdo patrocinado). A etapa "auditoria de fontes citáveis" do framework é a que mais decide (§4 etapa 5).
7. **A ciência da semana é sobre defesa e sobre o ecossistema, não sobre "como citar mais".** Counter-GEO-Bench (`2609.02316`, 02-set) mostra que guardrails de prateleira reduzem o ataque por GEO distorcivo em no máximo 5,7% e que um detector leve reduz 47,6%. CHASE (`2608.30466`, 31-ago) simula 20 rodadas de otimização e mede a queda de alinhamento entre ranking e qualidade em seis domínios. O mecanismo VCR (`2608.11390`) recompensa conteúdo verificável e supera a melhor defesa em 12,1 pontos. A leitura operacional: a única estratégia que sobrevive ao motor que aprende a se defender é evidência checável (§6).
8. **Coleta de visibilidade tem regra de parada, não número fixo.** `2607.10341` (v2, 26-ago) define estabilidade de ranking e suficiência estrutural a partir da distribuição observada, testadas em 30 combinações plataforma-tópico em Gemini, SearchGPT e Perplexity: nenhum orçamento fixo de consultas se justifica em todos os contextos. Substitui o "N≥30" da Wave Julho-22 por convergência medida (§5.1, §9.2).
9. **`llms.txt` e Markdown "para IA" seguem sem consumidor.** Common Crawl analisou 584.107 arquivos `llms.txt` do crawl de julho: 68,27% gerados por plugin, 22,56% sem nenhum link, 6,59% com política que a especificação não prevê (31-ago, primária). John Mueller (31-ago): nos sites de teste dele, os únicos crawlers que declaram aceitar Markdown são ferramentas de SEO. Status da Wave Agosto mantido e reforçado (§8.b).
10. **Setembro tem três prazos externos.** Cloudflare muda os defaults de bots em 15-set (Wave Agosto §2.6). Perplexity aposenta os endpoints Sonar em 27-set (fórum oficial, 13-ago): o `geo-orchestrator` e o `papers` precisam migrar para a Agent API. Google abre contratos do programa europeu de licenciamento de dados de busca em 17-set (amostras em 16-nov) e a Comissão Europeia designou o ChatGPT como motor de busca de grande porte em 31-ago, com quatro meses para cumprir o DSA (§2.6, §8.h).

---

## 1. Corpus científico: papers verificados (maio a setembro de 2026)

Todos os IDs abaixo foram abertos em `arxiv.org/abs/<id>` em 03-set-2026; título, autores, data e abstract conferem e estão em `raw/arxiv_abs_verificados.md`. PDFs não lidos: ler antes de citar número em copy ou paper. Marcação: ✓ = abstract lido nesta sessão; ○ = verificado em wave anterior, listado para consolidação.

### 1.1. Novos na janela (27-ago → 03-set) ou revisados nela

| arXiv | Data | Título (autores) | Achado com número | Uso |
|---|---|---|---|---|
| `2609.02316` ✓ | 02-set-2026 | Counter-GEO-Bench: Evaluating Defenses Against Information-Distorting GEO (Zheng, Zhao, Yang) | 247 consultas verificadas por humanos com reescritas GEO que preservam ou distorcem informação; três LLMs vítimas. Guardrails de prateleira (Granite Guardian, Llama Guard 3, NeMo Self-Check) reduzem a taxa de sucesso do ataque em no máximo 5,7% relativo; o baseline C-GEO Guard reduz 47,6% com perda de utilidade quase zero. | GEO distorcivo passa por filtros de segurança como "conteúdo informativo fluente"; a defesa específica é viável e vai ser adotada. Anti-padrões 1 e 5 dos 50 Conceitos ganham segundo detector (§6.2). |
| `2609.00319` ✓ | 31-ago-2026 | Sources of Truth: A Multi-Platform, Multilingual Audit of Citations in AI Mental Health Information Queries (Nguyen et al., Torous) | ChatGPT, Perplexity e AI Overview; 20 perguntas em inglês, 3 delas em mais 6 idiomas; 15.942 citações em 1.140 respostas e 1.713 domínios. Os 10 domínios mais citados concentram 43,6% das citações em inglês; governo, saúde comercial e acadêmico com cerca de 22% cada. Pedir fontes explicitamente muda pouco a composição. Consultas fora do inglês recebem menos citações e são roteadas a recursos no idioma com frequência significativamente menor. | Evidência primária de concentração de fontes e de penalidade de idioma: a hipótese pt-BR do `papers` (§9.2) ganha comparável direto. |
| `2608.30466` ✓ | 31-ago-2026 | CHASE: How Content Ecosystems Are Reshaped When Ranking Is the Only Target (Gao et al.) | Simulação controlada de 20 rodadas de adaptação a um sinal de ranking de LLM em seis domínios; ranking validado contra citação em respostas fundamentadas (AUC 0,853 ± 0,093). Alinhamento entre ranking e qualidade julgada cai em todos os domínios (Δρ de Spearman de −0,107 a −0,018, média −0,068); controle com alvo aleatório mostra que o efeito vem da adaptação ao incentivo, não da reescrita em si. | Otimizar repetidamente contra o mesmo sinal homogeneíza e piora; a regra "diversidade > redundância" da Wave Agosto ganha o lado populacional (§6.1). |
| `2608.30023` ✓ | 30-ago-2026 | Demand-Side Measurement for GEO: Constructing and Validating a Million-Persona, Intent-Annotated Buyer Corpus (Żatuchin, Dzemesjuk) | PersonaGen-1M: 1.031.732 personas sintéticas de comprador, 511 rótulos de indústria, 4 contextos de mercado, 5.160.046 consultas; intenção primária 78,3% informacional, 17,4% comercial, 4,3% transacional; campo `preferred_sources` por persona. Subconjunto estratificado publicado abertamente. | Primeira base pública para montar "universo de prompts" a partir da demanda, em vez de keyword; a etapa 3 do framework ganha instrumento (§4). |
| `2608.29063` ✓ | 29-ago-2026 | Agent2UCB: Agentic System for GEO (Yu, Wang, Yu, Kim, Dogan, Wu, McAuley) | Sistema agêntico que avalia nove estratégias de GEO por item de conteúdo e escolhe por política de bandit com priors de LLM; avaliação de prontidão SEO (legibilidade, cobertura, credibilidade tipo E-E-A-T) como monitor de efeito colateral; ganhos consistentes no GEO-Bench preservando qualidade SEO. | Demo acadêmica do que os vendors chamam de "AI marketer"; confirma que a otimização será automatizada e, portanto, detectável (§6.2). |
| `2608.27631` ✓ | 27-ago-2026 | Beyond the Vacuum: Combinatorial Strategy Selection for Competitor-Aware GEO (Sourirajan et al.) | Formaliza GEO como escolha de estratégia dependente do que os concorrentes fazem; otimização bayesiana combinatória (BOCS) mais fine-tuning com traços de raciocínio; estado da arte em métricas de impressão no geo-bench e no `geo-bench_comp`; transfere a domínios fora da distribuição. | A "estratégia ótima" muda conforme a adoção cresce: nenhuma tática é estável (confirma o survey `2607.14035`) (§6.2). |
| `2607.10341` ✓ (v2 26-ago) | 11-jul-2026, rev. 26-ago | From Stochastic to Stable: Rank Stability and Structural Sufficiency in AI Visibility Measurement (Sielinski) | Critério sequencial de convergência: estabilidade de ranking (platô da correlação de postos) e suficiência estrutural (dispersão das cotas de citação entre domínios estabelecidos maior que a incerteza). Sem alvo externo de número de consultas; aplicado a 30 combinações plataforma-tópico (Gemini, SearchGPT, Perplexity): nenhum orçamento fixo se justifica em todos os contextos. | Substitui o N fixo por regra de parada; entra na metodologia do `papers` e no report (§5.1). |
| `2607.04282` ✓ (v3 25-ago) | 05-jul-2026, rev. 25-ago | The New Shape of Search: How Conversational AI Recomposes Information Seeking (Iannelli, Ai) | Painel com prompts e navegação dos mesmos usuários (assistentes autônomos; AIO e AI Mode fora do escopo). O conteúdo precede o assistente mais do que o segue: diferença pareada de +20,6 [19,9; 21,3] pontos. 34,1% das sessões com assistente não têm nenhum passo externo observado, contra 19,5% das sessões centradas em busca dos mesmos usuários (+13,0 pontos). Contido não significa resolvido. | Muda a premissa de funil: o assistente fica no meio da jornada, não na boca. Copy de "IA substitui a busca" é falsa na evidência (§5.2). |

### 1.2. Papers de maio a agosto que o corpus ainda não registrava (abertos nesta sessão)

| arXiv | Data | Título (autores) | Achado com número | Uso |
|---|---|---|---|---|
| `2608.18352` ✓ | 18-ago-2026 | AI in Search Reduces Publisher Referrals Without Improving User Experience: Experimental Evidence (Wang, Gleason, Bart, Wilson, Metaxa) | Experimento de campo pré-registrado (N=1.100) no Google: remover AIO e AI Mode aumenta a taxa de clique para publishers; experiência só com AI Mode reduz cliques e corrói experiência e confiança. | Primeira evidência causal, não observacional, do custo de referral das superfícies de IA. Entra em toda aula e copy sobre zero-click (§5.2). |
| `2608.04831` ✓ | 05-ago-2026 | Investigating Click Behaviors On Google Search Result Pages That Produce an AI Overview (Chapekis, Lieb, Shah, Smith) | Painel representativo de 900 adultos dos EUA, um mês de navegação. Clique em fonte citada no AIO ocorre em cerca de 1% das visitas com AIO; AIO associado a menos cliques e a mais encerramento de sessão, com efeitos mantidos em regressão mista controlando por painelista e por atributos da consulta. | O "1%" tem fonte primária com método; substitui as estimativas de vendor (§5.2). |
| `2608.15896` ✓ | 16-ago-2026 | When Search Eats the Web: A Model of Corpus Erosion under Generative Extraction (Peyronnet) | Modela o corpus rastreável como recurso comum (volume, qualidade média, vida útil). Extração sem visita degrada os três; existe limiar de erosão após o qual o corpus se extingue; com vários motores concorrentes a taxa de extração de equilíbrio converge ao limiar; a taxa socialmente ótima fica estritamente abaixo. | Base teórica para o argumento de licenciamento e para a decisão de opt-out do Search Console (§2.6). |
| `2608.11390` ✓ | 11-ago-2026 | Mechanism Design for Generative Engines: From Exploitation toward Win-Win Outcomes (Xu, Guo, Xiong) | "Guerras de citação": ataques GEO se adaptam às defesas produzindo reescritas que degradam qualidade e inserem alegações sem suporte. Mecanismo VCR (recompensa por conteúdo verificável) supera a melhor defesa em 12,1 pontos de utilidade líquida em três benchmarks. | Confirma a regra da casa: evidência verificável é o que a plataforma tem incentivo a recompensar (§6.2). |
| `2608.15814` ✓ | 16-ago-2026 | Assessing Attack Surfaces in Generative Search Engines through Publisher Attributes (Mochizuki et al.) | Métrica "content-injection barrier" (dificuldade de injetar conteúdo dado o nível de autoridade do publisher); três motores, EUA e Japão; a superfície de ataque difere por motor, é moldada pela função de busca, e perfis de usuário pouco influenciam. | Personalização não é a alavanca; autoridade do publisher é. Reforça earned media (§4 etapa 8). |
| `2608.21702` ✓ | 22-ago-2026 | From Association to Causation: Improving Retrieval Precision of RAG via Causal Relations and an Attention Mechanism (Liu et al.) | Reordenação sem treinamento pela estrutura causal da recuperação (palavras compartilhadas como causa comum; palavras residuais ligadas à resposta): em base empresarial de 471 documentos, diretriz relevante sobe da posição 6 para o top-3; no corpus de diagnóstico com keyword stuffing, rank médio do alvo cai de 2,88 para 1,25 (cross-encoder treinado: 2,63); fica abaixo da similaridade em três conjuntos do BEIR. | Recuperadores estão aprendendo a descontar palavra-chave repetida; evidência específica ligada à pergunta sobrevive melhor (§6.3). Localizado pelo Perplexity web e aberto no arXiv. |
| `2607.23893` ✓ (v2 01-ago) | 26-jul-2026 | Who Gets Named: Citation Type Predicts Individual Naming by Grounded Language Models (Żatuchin) | 2.400 chamadas fundamentadas em 24-jul (GPT-5.6 Sol, Gemini 3.6 Flash, Sonar Pro, Grok 4.5), 4 mercados europeus, 5 idiomas. Modelos nomeiam um profissional em 25,8% das respostas; imobiliário 35,4%, concessionárias 32,9%, seguros 9,1%; Grok 38,0% contra Gemini 9,3%. Prompt em inglês nomeia 36,7% contra 15,6% no idioma local. Roster de 939 pessoas captura 0,47% das menções. | Visibilidade de pessoa (consultor, corretor) é medível e depende do tipo de citação; o idioma penaliza (§9.1). |
| `2607.27686` ✓ | 30-jul-2026 | Evaluating and Pricing Advertisements in AI-Generated Responses (Turner-Smith et al.) | Avaliador de intenção de clique para anúncios dentro da resposta; supera juízes zero-shot em sensibilidade a relevância (79% contra 60 a 67%); concordância com humanos em 86% dos pares; regra de pagamento com lance verdadeiro ótimo. | Base para entender o leilão do ChatGPT Ads e o que "relevância" significa lá (§2.2). |
| `2607.15771` ✓ | 17-jul-2026 | What Do Chinese-Language Generative Search Engines Cite and Surface? (Zhen, Liu, Zhang, Niu) | 8 interfaces, 614 consultas, 3 réplicas; 160.860 registros de citação. Taxa de seleção de marca 8,3%; meia-vida de página citada de 39 dias (alta temporalidade) a 68 dias (baixa); app e web da mesma plataforma citam conjuntos diferentes. | Frescor tem número (meia-vida) e a interface é dimensão de medição (§6.3). |
| `2606.28356` ✓ | 08-jun-2026 | SafeGEO: Understanding GEO Risks in Recommendation Agents (Wen et al.) | 22 variantes de ataque GEO em 600 casos de recomendação; produtos defeituosos entram no conjunto recomendado até 83,2% mais; defesas simples reduzem até 39,2% sem restaurar o nível sem GEO. | Motor de recomendação é atacável e os vendors vão filtrar: argumento contra pseudo-GEO (§6.2). |
| `2606.16344` ✓ | 15-jun-2026 | Whose hotel does the AI recommend? An algorithm audit of reputation signals (Baig, Gillani, Ali) | Conjoint randomizado em 12 modelos; nota do hóspede eleva a seleção em 31,6 pontos; preço alto reduz 30,0; posição na lista, sem conteúdo, desloca a recomendação e vale cerca de US$ 12 por noite; resposta da gerência é ignorada. | Evidência causal de que posição em lista importa; entra na aula de turismo e no guia de hospedagem do portal (§9.3). |
| `2606.12439` ✓ | 18-mai-2026 | Position: GEO Creates Underexamined Risks, Governance Must Target Concentration, Disclosure, and Academic Blind Spots (Wen et al.) | Três riscos: influência concentrada, influência comercial não divulgada, e pontos cegos entre academia e indústria; propõe governança no nível da resposta (contestabilidade, disclosure, auditoria caixa-preta, métricas de persistência de exposição). | Vocabulário de governança para contratos e para a página de ética do site (§9.1). |
| `2607.14197` ✓ | 15-jul-2026 | How AI LLM Engines Shape the Global Conflict Information Environment (Miklian) | 5.460 respostas de cinco motores sobre 28 conflitos; quanto mais rala a evidência recuperável, mais o motor inventa; 1.048 sites de origem analisados, otimização GEO de fonte já ocorre. | Registro de que GEO já opera em informação de conflito; fica como contexto, não como alavanca. |
| `2607.03421` ✓ | 03-jul-2026 | AI Overviews in Academic Search (Schott et al.) | Estudo de usuário (n=30): tendências não significativas a favor dos resumos; participantes raramente expandem o resumo. | Contexto acadêmico; sem uso em copy. |
| `2609.02246` ✓ | 02-set-2026 | LLM-as-a-Judge Is Not an Oracle (Wahi) | Onze modos de falha do juiz-LLM em loops de auto-otimização; agentes com 100% de aprovação escondendo 68% de capacidade real; guardrails determinísticos que o juiz não pode anular. | Regra para o `quality_judge` do orchestrator e para o reviewer do curso-factory: o juiz é conselheiro, não oráculo (§9.2, §9.3). |

### 1.3. Índice consolidado maio a setembro (referência cruzada)

Verificados em waves anteriores e mantidos como base: `2605.06635` (Cited but Not Verified, 07-mai), `2605.25517` (What Gets Cited, Sprinklr; publicado no SIGIR '26, DOI `10.1145/3805712.3808445`, confirmado por busca nesta sessão), `2606.04362` (controle on-domain, 03-jun), `2606.20065` (Ranqo, 18-jun), `2606.00898` v2 (cobertura do grafo), `2607.14035` (survey crítico, 15-jul), `2608.16824` (GEO-Flag), `2608.13956` (diversidade), `2608.03527`, `2608.03487`, `2608.02011` (pipeline). Os 32 IDs da Wave Julho-22 continuam listados lá. Total do corpus maio a setembro após esta wave: 56 IDs abertos.

**Não localizado na janela** (afirmar ausência, não inventar): paper primário sobre tamanho ideal de chunk para GEO; estudo controlado de headings-pergunta; modelo novo de embedding com resultado completo no MTEB entre 20-ago e 03-set (ver §6.3). O Gemini 3.1 devolveu "GEO Flag" e "survey crítico" como "ID não verificado" e a busca do OpenAI ainda estava em curso no fechamento deste doc; os raws registram.

---

## 2. Motores de resposta: o que mudou (27-ago → 03-set)

### 2.1. Google (fontes primárias abertas em 03-set)

- **Relatório de desempenho em IA generativa, para todos (31-ago):** "As of August 31, 2026, we've rolled out these insights to all websites worldwide" (Search Console Help, `answer/16984139`). Mostra impressões em AI Overviews e AI Mode (Discover em relatório próprio), por página, país, dispositivo e data; limite de 1.000 linhas; sem cliques. O controle de exclusão das superfícies de IA ("Search generative AI control") chegou junto: o site pode sair de AIO, AI Mode e Discover como link ou como base de resposta, sem perder ranking clássico (SEJ e Search Engine Roundtable, 31-ago e 01-set, secundárias concordantes). O rollout começou em junho (blog do Search Central, primária).
- **Gemini 3.8 Flash no AI Mode (02-set):** blog do Google (primária) lista "AI Mode in Google Search" entre as superfícies; Robby Stein: "Gemini 3.8 Flash has landed in Search", para assinantes Pro e Ultra, selecionável pelo ícone de mais. Preço de API US$ 0,75/M entrada e US$ 3,75/M saída até 31-dez-2026, depois US$ 1,50/US$ 7,50. É o terceiro Flash em seis semanas (SEJ, 02-set). Em 03-set Barry Schwartz publicou "Google AI Mode Gemini 3.8 Flash Not Link / Citation Friendly?" (secundária, título e data conferidos; corpo não aberto): usuários relataram respostas sem links. A página de ajuda do AI Mode ainda lista só "Fast" e "Pro" (SEJ). Regra: declarar modelo em toda medição de AI Mode (§5.2).
- **Preferred Sources (doc atualizado 20-ago):** "In AI Mode and AI Overviews, your content can be highlighted with a 'preferred' badge for users who have selected your site as a preferred source" (primária). Carrosséis de tema em desenvolvimento no AI Mode passaram a incluir fontes preferidas (SEJ, 25-ago, secundária). Mais de 600 mil fontes únicas selecionadas por leitores em 20-ago, contra 345 mil em 27-mai, e botão incorporável para o publisher pedir a seleção na própria página (declarações do Google relatadas pela ppc.land, secundária; o post do blog do Google devolveu 404 na verificação).
- **Spam update de agosto:** começou em 18-ago e terminou em **21-ago** (Search Engine Roundtable, relatório de setembro; a Wave Agosto registrava 20-ago com dashboard indisponível). Nenhum core update em agosto; nenhum em 27-ago → 03-set.
- **Documentação:** política de spam com seção de reputação de site atualizada em 28-ago (página oficial, "last updated August 28, 2026 UTC"); página do programa europeu de licenciamento de dados de busca atualizada em 31-ago e 01-set (§2.6).
- **AI Max (Ads):** a partir de 01-set o Google migra automaticamente campanhas de Search com broad match de campanha ou ativos automáticos para AI Max; DSA adiado para fevereiro de 2027 (blog do Google, atualizado 11-jun, primária; SEL, secundária). O Google declara média de 7% mais conversões ou valor com o conjunto completo de recursos (primária, número do vendor sobre si).
- **Goto URLs:** confirmação do Google em 26-ago; em 28-ago a Ahrefs publicou aviso de "Google keyword ranking data disruption" (Glenn Gabe via ppc.land, secundária). Séries de rank tracking de terceiros quebram a partir do fim de agosto; declarar no report.
- **Comércio no AI Mode:** reserva de hotel com checkout pelo Google Pay, alerta de preço de voo e preço em milhas em rollout (SEJ, 27-ago, secundária; blog do Google devolveu 404 na verificação). Estudo Productrise (SEJ, 03-set, secundária): em 2 milhões de listagens e 100 mil consultas, só 1,28% dos produtos do carrossel apareceram no AI Mode no mesmo dia; AI Mode mostra 3,9 produtos por consulta contra 27,8 do carrossel; quando o mesmo produto aparece, o primeiro vendedor difere em 49,6% das vezes e o AI Mode mostra o preço maior em 68,4%. O Google respondeu que ambos usam o Shopping Graph.
- **Analytics:** dados de 01-set sumiram dos gráficos do GA4 (Search Engine Roundtable, 02-set): quebra de série a anotar.

### 2.2. ChatGPT / OpenAI

- **US$ 1 bilhão em anúncios (31-ago, OpenAI, primária, página aberta):** "In less than 200 days after launch, ChatGPT Ads has reached $1 billion in annualized revenue run rate"; mais de 40 países; mais de 50 parceiros de tecnologia e medição; Ads Manager para PMEs desde maio; "CPC and outcome-optimized bidding now account for the majority of campaigns"; Pixel e Conversions API como base de medição; "Advertising does not influence the answers ChatGPT provides". Um parceiro reportou que mais de 80% do tráfego de anúncio no ChatGPT é de clientes novos (número do vendor sobre um parceiro). O ecommerce citado teve ROAS de 3× em 28 dias (idem).
- **Números de mercado (Similarweb, 03-set, primária do vendor):** 26% das respostas do ChatGPT no desktop dos EUA tinham anúncio em junho (14% em maio); 65,3% das sessões continuam depois do anúncio; 66,3% dos anúncios aparecem do segundo prompt em diante; CTR 0,50% em junho (0,68% em maio) contra cerca de 6,4% de referência em Google Ads; CPM inicial em torno de US$ 60 com mínimo de US$ 200 mil, mínimo reduzido a US$ 50 mil em maio e passagem a CPC. Formatos de agosto (Search Engine Roundtable, 07-ago): oCPC beta, macros de URL, carrossel multiproduto, Automatic Advanced Matching como padrão desde 17-ago.
- **Motor de busca de grande porte na UE (31-ago):** a Comissão Europeia designou o ChatGPT como VLOSE sob o DSA, "a hybrid service that qualifies as an online search engine"; 159,1 milhões de destinatários mensais médios na UE no semestre até 31-mar-2026 (SEJ citando a divulgação da OpenAI; a página da Comissão, aberta, confirma a designação e o prazo de quatro meses). Obrigações: auditoria anual independente, dados a autoridades e pesquisadores, repositório público de anúncios.
- **Ferramenta de busca reescrita (25-ago, Suganthan Mohanadasan via SEJ, secundária):** o payload deixou o JSON por linhas delimitadas por pipe com tipo de chamada (`fast`, `product`, `business`, `image`), texto da consulta, janela de frescor em dias e slot de domínio; exemplo `fast|Zendesk AI agents pricing 2026|30|zendesk.com`. Janelas observadas: 2 dias para cotação, 7 para futebol, 30 para preço, 90 para guidance, 365 a 3.650 para local e histórico. O campo `search_queries` que a Wave Agosto usava desapareceu do payload: a medição de share de `site:` proposta em Agosto §9.2 precisa de novo extrator.
- **Reddit:** 3,8% → 0,5% (Promptwatch via Semrush, 26-ago); em 27-ago o mesmo autor documentou busca por `r/whatnotapp` com janela de 3.650 dias, 48 threads recuperadas de 71 e 6 das 8 citações da resposta para o subreddit. A OpenAI: "doesn't set a fixed level of visibility for individual sites".
- **Shopping (Profound, 03-set, primária do vendor):** ver TL;DR 4. Modelo estatístico da Profound explica 83% das variações de visibilidade observadas; 450 lojistas com queda ≥33% e 67 com alta ≥33%; Shopify responde por cerca de 35% da recuperação por feed.
- **Operação no Brasil (evento em São Paulo em 18-ago; Poder360 21-ago e Olhar Digital 27-ago, secundárias citando a OpenAI):** 215 milhões de mensagens por dia no ChatGPT no Brasil (140 milhões um ano antes); terceiro maior mercado em usuários semanais e segundo em uso de API por desenvolvedores; ChatGPT Ads disponível no Brasil desde 11-ago nos planos Free e Go; acordo com a Prefeitura de São Paulo (Prodam) e ChatGPT Edu no ITA. A página da OpenAI em pt-BR devolveu 403 na verificação.
- **WebMCP no navegador do ChatGPT (25-ago, SEJ, secundária):** "Site tools" para usuários Work e Codex; Shopify ativou ferramentas WebMCP em todas as lojas Liquid; Cloudflare lançou bridge em preview; a especificação está em origin trial no Chrome 149 (doc do Chrome, primária). Sem métrica pública de adoção.
- **Claude e Claude Code são motores distintos (Profound, 24-ago, primária do vendor):** 24.135 respostas em 1.724 prompts (13 a 23-jul): Claude Code aciona busca em 13% das respostas contra 93% do Claude; só 1 em 5 marcas coincide; 74% das visitas do agente do Claude Code vão a documentação, páginas informativas e de preço, enquanto 60% das do Claude vão a robots.txt, sitemaps e home.

### 2.3. Perplexity

- **Sonar aposentado em 27-set (fórum oficial, 13-ago, primária):** "Sonar endpoints are fully available today and retire on September 27, in 45 days"; a Agent API "more than doubles the best Sonar score" em BrowseComp e WideSearch. Seis presets (fast, low, medium, high, xhigh, wide-research) mapeiam os tiers antigos (secundária). Nesta sessão, `/v1/agent` respondeu com o mesmo `insufficient_quota`: a chave é aceita pelo endpoint novo.
- Sem lançamento de produto localizado na janela além do que a Wave Agosto já registrava (Comet, Comet Plus, decisão do 9º Circuito).

### 2.4. Microsoft / Bing / Copilot

- Bing testa snippets sem nome do site (Search Engine Roundtable, 02-set, secundária). O relatório de IA do Bing Webmaster Tools (11-fev-2026) segue como camada 2 gratuita; nenhuma mudança na janela.

### 2.5. Anthropic, xAI, Meta, Apple

- **Anthropic: Claude Fable 5.1 e Claude Mythos 5.1 (01-set, página oficial, primária):** mesmo modelo em dois níveis de salvaguarda; Mythos 5.1 só para defensores cibernéticos e cientistas verificados (organizações dos EUA por ora); Fable 5.1 em disponibilidade geral com salvaguardas que intervêm 85% menos em pedidos benignos; US$ 10 por milhão de tokens de entrada e US$ 50 de saída; nenhuma mudança localizada em busca ou citação.
- Anthropic: alerta sobre roubo de sessões do Claude por infostealer (SEJ, 30-ago). YouGov (SEJ, 26-ago, secundária): Claude preferido por 10,6% dos usuários de IA da Geração Z contra 1,4% dos boomers; ChatGPT lidera todas as gerações (44,4% na Geração Z). Sem lançamento de modelo localizado na janela.
- xAI, Meta, Apple: nada localizado em 27-ago → 03-set pelas rodadas.

### 2.6. Infraestrutura, acesso e regulação

- **Cloudflare 15-set:** prazo mantido (Wave Agosto §2.6). A SEJ publicou em 03-set orientação de bloqueio em servidor ou WAF em vez de só robots.txt (secundária).
- **`llms.txt` (Common Crawl, 31-ago, primária):** 584.107 arquivos do crawl de julho (CC-MAIN-2026-30); 68,27% gerados por plugin (Wix 41,34%; All in One SEO 73.136 arquivos; Yoast 40.509); 49,90% seguem a especificação; 32,94% têm nota descritiva nos links; 22,56% não têm link nenhum; 6,59% carregam política que a spec não prevê; 10 casos de prompt injection; sites listam negação de crawler no `llms.txt` sem bloquear no robots.txt.
- **Agent readiness (SALT.agency via SEJ, 01-set, secundária):** auditoria de 50 sites grandes em três camadas: recuperabilidade média 74,4%, atribuição e significado 38,5%, transação e descoberta por agente 2,1%; 70% com JSON-LD; 5 de 50 com Content Signals Policy; 46 de 48 com zero na camada 3; "nearly two-thirds leave the question of which AI bots can access which content entirely to luck".
- **Dados de busca na Europa (Google, primária, atualizado 01-set):** o programa europeu de licenciamento abre contratos em 17-set-2026 e amostras em 16-nov-2026; dados de ranking, consulta, clique e visualização no EEE; elegíveis são motores de busca com 50 mil usuários mensais e dois anos de operação (ou capital de EUR 50 milhões); preço FRAND limitado a custo incremental mais retorno. Decisão vinculante da Comissão de julho sob o DMA.
- **PL 2338 (Brasil):** o vice-presidente do Senado declarou que a votação deve ficar para 2027 (Telesíntese, secundária, data não confirmada na verificação). Ver §7.

---

## 3. Vendors e colunas: lançamentos e estudos datados (27-ago → 03-set, com fronteira de 20-ago)

| Data | Quem | O quê | Número ou feature | Fonte |
|---|---|---|---|---|
| 04-ago e 20-ago | Adobe | Brand Visibility (ex-LLM Optimizer) em disponibilidade geral; em 20-ago as métricas passam a contagem por resposta (responses with mentions, responses with citations) | release notes oficiais | primária ✓ |
| 20-ago | Ahrefs | What Is Information Gain in SEO | patente do Google (2018/2022); páginas com 15+ dados únicos pontuam 62 contra 40 (On-page.ai, 150 páginas top-3, secundária dentro da primária) | primária ✓ |
| 24-ago | Profound | Claude and Claude Code are distinct Answer Engines | 24.135 respostas; busca em 13% contra 93%; 1 em 5 marcas coincide | primária ✓ |
| 25-ago | Search Institute | Is GEO Really Different From SEO? | overlap de citações com o top-10 do Google: Perplexity 82%, AIO 67%, AI Mode cerca de 35% (Semrush, 5.000 keywords, 2025); Ahrefs média 11,9%; KDD 2024 mudou fonte já no contexto, não provou descoberta | secundária ✓ |
| 25-ago | Suganthan / SEJ | ChatGPT Rebuilt Its Search Tool | formato pipe, janela de frescor por tipo, 84 threads do Reddit buscadas e zero citadas | secundária ✓ |
| 26-ago | Semrush | conector nativo para o Claude (MCP) | 28,8 bilhões de keywords, 43 trilhões de backlinks, 317 milhões de prompts expostos ao assistente; planos Semrush One e SEO Classic | secundária (ppc.land) |
| 26-ago | Semrush | Reddit's citations in ChatGPT fall from 3.8% to 0.5% | queda de 86% em quatro dias (Promptwatch); AIO −11%, AI Mode −31% no mesmo período | primária do vendor ✓ |
| 26-ago | Shero Commerce / SEJ | AI Tools Recommend Brands But Cite Other Sites | 60 categorias; páginas próprias 2,8% de 1.851 fontes; terceiros 59%; 31% das 159 recomendações citam a página da marca; 20% de descrições idênticas em 883 lojas Shopify | secundária ✓ |
| 26-ago | YouGov / SEJ | AI Brand Preference Splits By Generation | Claude 10,6% Geração Z contra 1,4% boomers; 28% dos americanos confiam em assistentes de IA | secundária ✓ |
| 27-ago | Ahrefs | Reddit Appears in 83.9% of Google's Discussions and Forums Results | 145 milhões de SERPs dos EUA; recurso em 11,7%; Reddit 87,8% nos EUA; três sites concentram 76,75%; 98,7% em intenção informacional | primária ✓ |
| 27-ago | Trendos / SEJ (patrocinado) | We Analyzed 107 Million AI Answers | comunidade e UGC cerca de 50% das citações em três indústrias; marca própria 2% em TI, 46% em bens de consumo | secundária, patrocinada ✓ |
| 27-ago | Duane Forrester / SEJ | AI Search Didn't Remove Cognitive Load, It Moved It | síntese primeiro, evidência depois; medir "o que a informação tem de sobreviver" | secundária ✓ |
| 28-ago | Profound | Adobe Experience Manager nodes em Profound Agents | agente edita fragmentos de conteúdo no AEM | primária ✓ |
| 28-ago | Ahrefs | How We Use AI for Every Article Without Making AI Slop | processo editorial com IA | primária (título) |
| 28-ago | Tim Soulo (X) | seis takeaways de AEO com Dan Petrovic | Reddit rejeitado, `llms.txt` inútil para descoberta, sem "volume de prompt", LLMs usam índices clássicos | secundária (X, via Grok) |
| 31-ago | Ahrefs (FR) | Citation ChatGPT: as 1.000 páginas mais citadas | relatório de páginas citadas do Brand Radar: só 32,3% das citações são "influenciáveis" (posts, mídia, reviews); 28% das páginas citadas têm zero visibilidade orgânica; DR mediano 90; 65,3% de sites com DR ≥ 81; 76,4% atualizadas nos últimos 30 dias; 52,1% no top-3 do Google para a keyword principal | primária ✓ |
| 31-ago | Google | GSC AI report e controle de exclusão para todos | impressões por página, país, dispositivo, data | primária ✓ |
| 31-ago | OpenAI | ChatGPT Ads US$ 1 bi run rate | 40+ países; CPC majoritário; autoatendimento na Europa, Índia, Oriente Médio e Norte da África | primária ✓ |
| 31-ago | Common Crawl | Content analysis of llms.txt files | 584.107 arquivos; 68,27% por plugin; 22,56% sem link | primária ✓ |
| 31-ago | Comissão Europeia | ChatGPT designado VLOSE | 159,1 milhões de destinatários na UE | primária ✓ |
| 31-ago | John Mueller / SEJ | Markdown para IA | "the only crawlers who claim to accept markdown are SEO tools" | secundária ✓ |
| 31-ago | Jason Shafton / SEJ | Restructure Your Marketing Team & Budget | mover 15 a 20% do orçamento no primeiro trimestre; exemplo de US$ 60 mil/mês com US$ 10 mil para programa de AI search; cliente de 3 para 12 citações em 20 respostas | secundária ✓ |
| 01-set | Ahrefs (FR) | AI Overviews en santé: top 50 domínios na França | 498.325 citações em agosto; YouTube 16,98%, Facebook 8,59%, Instagram 4,43%, fr.wikipedia 3,66%, Reddit 2,54%; empresas privadas 46,6%, instituições públicas 13,8%, mídia de saúde 7,6% | primária ✓ |
| 01-set | Semrush | Where does AI get its information | treinamento, recuperação ao vivo (ChatGPT usa índices do Google, Bing e próprio), licenciamento (Reddit, Stack Overflow, Yelp, Time) | primária ✓ |
| 01-set | Profound | Context Manager | conhecimento de negócio estruturado para o agente de marketing | primária ✓ |
| 01-set | SALT.agency / SEJ | The Technical Signals AI Search Uses | 50 sites; 74,4% / 38,5% / 2,1% por camada | secundária ✓ |
| 01-set | Loren Baker / SEJ | Schema For AI Citations | "Schema can only help a machine verify authority that already exists"; quatro fontes que precisam concordar | secundária ✓ |
| 02-set | Semrush | Create an AI Brand Visibility Report [+ Template] | três níveis de métrica; GA4 + "como nos conheceu"; mensal e trimestral; template em Sheets | primária ✓ |
| 02-set | Semrush | How to prepare your site for AI agents | páginas que falham em carregar são citadas cerca de 18 vezes menos (número do vendor, método não aberto); conteúdo no HTML bruto; um título, uma pergunta | primária ✓ |
| 02-set | Ahrefs | The 50 Most-Cited Websites in Google AI Overviews (September 2026) | 3 milhões de consultas dos EUA, Brand Radar; YouTube 22,9%, Reddit 18,5%, Facebook 10,1%, Google 8,8%, Instagram 5,6%, Quora 4,7%, Wikipedia 4,0% | primária ✓ |
| 02-set | Google | Gemini 3.8 Flash | AI Mode entre as superfícies; US$ 0,75 / 3,75 por milhão | primária ✓ |
| 02-set | NIQ + Similarweb | Agentic Commerce Measurement | cinco medidas (intenção, prateleira agêntica, prontidão de conteúdo, tráfego por IA, conversão por IA); versão inicial no Q4 2026 | primária ✓ |
| 03-set | Profound | ChatGPT 5.6 has transformed Shopping mode | feed 8,26% → 61,54%; top-10 lojistas 22,5% → 41,8%; lojistas únicos −20% | primária ✓ |
| 03-set | Similarweb | AI Referral Traffic by Industry: 770 Million Monthly Visits | 770,7 milhões de visitas mensais (jun/2025 a mai/2026), +117,4% ano a ano; marketplaces 46,8 milhões; beleza +312,5%; ChatGPT mais de 80% dos referrals ao top-1.000 | primária ✓ |
| 03-set | Similarweb | How ChatGPT Ads Are Reshaping Paid Search | 26% das respostas com anúncio; CTR 0,50% | primária ✓ |
| 03-set | Duane Forrester / SEJ | When AI Has Nothing On Your Company, It Describes Someone Else | substituição silenciosa; auditoria de conteúdo não enxerga o que falta fora do site | secundária ✓ |
| ago | SEOFOMO (Aleyda Solis) | State of AI Search Optimization 2026 | 171 profissionais de 36 países (17 a 27-ago); 69% com orçamento para IA (38% em 2025); 92% medem citações; medir com confiabilidade é o desafio nº 1 (19%); 46% atribuem 0 a 5% da receita à IA; 35% não conseguem atribuir | primária ✓ |
| ago | Peec AI | changelog 03-ago | Brand Perception para todos; página de anúncios em respostas de IA; MCP e API | primária ✓ (nada em 15-ago → 03-set) |
| jan a ago | Otterly, Scrunch, AthenaHQ, Conductor | sem lançamento novo localizado na janela | Conductor: nada após 29-jul no blog | secundárias |

**Vozes (via Grok em X e imprensa, secundárias):** Lily Ray (SEL, 02-set): abandonar SEO para focar só em IA é falso, atalhos queimam. Tim Soulo (28-ago): LLMs usam índices "old school". Aleyda Solis (03-set): recorte Similarweb de citações do ChatGPT em agosto, social e referência caem, sites de categoria sobem. Glenn Gabe (02 a 03-set): casos do spam update e o problema de links no 3.8 Flash. Rand Fishkin e Kevin Indig: nada específico de GEO localizado na janela. Profound: sem posts em X localizados; o blog é a fonte.

---

## 4. Framework de EXECUÇÃO de um trabalho de GEO, versão 2 (setembro de 2026)

Tese mantida da Wave Agosto: GEO é a camada de otimização da presença em motores generativos e depende de SEO técnico, conteúdo útil, autoridade externa, dados estruturados coerentes, PR digital, medição por URL e atribuição de receita. Quatro sustentações novas: Google (relatório oficial e controle de exclusão), OpenAI (anúncio separado da resposta; feed decide o Shopping), a ciência de defesa (Counter-GEO-Bench, VCR, CHASE) e a prova causal de custo de referral (`2608.18352`).

| Etapa | Duração | Objetivo | Entregáveis (mudanças v2 em negrito) | KPIs da etapa |
|---|---:|---|---|---|
| 1. Kickoff e baseline | Sem. 1 | Produto × ICP × jornada, concorrentes, vocabulário, riscos | matriz, lista, glossário, **decisão registrada de opt-in ou opt-out das superfícies de IA no Search Console** | baseline de leads, receita orgânica, brand search |
| 2. Instrumentação | Sem. 1 a 2 | Separar as cinco trilhas | GA4 canal "AI Assistants"; **GSC relatório de IA generativa (impressões) como série oficial desde 31-ago**; Bing WMT AI Performance; ferramenta de prompts; **anotação de quebras de série: goto URLs (26-ago), GA4 01-set, mudança de modelo do AI Mode** | AI impressions; AI sessions; conversões assistidas; URLs citadas |
| 3. Universo de prompts | Sem. 2 a 3 | Clusters de prompt por intenção e por motor | biblioteca por ICP e mercado; **derivada de demanda (PersonaGen-1M, `2608.30023`) e de janela de frescor do motor (2 a 3.650 dias por tipo de consulta)** | prompts por etapa; cobertura por ICP; AI adjusted volume só como proxy |
| 4. Auditoria de visibilidade | Sem. 3 a 4 | Onde aparece, não aparece, aparece errado | SOV por engine, mention rate, citation rate, sentimento, **modelo declarado por execução**, **regra de parada por convergência (`2607.10341`) em vez de N fixo** | AI SoV; citation frequency; respostas corretas × incorretas; **substituição (Forrester): o motor descreve outro no seu lugar** |
| 5. Auditoria de fontes citáveis | Sem. 4 a 5 | Quais domínios alimentam o tema, por motor | mapa owned, earned, comunidade, reviews, mídia, YouTube, marketplaces; **por motor: AIO (YouTube 22,9%, Reddit 18,5%), ChatGPT (referência e trade media), Perplexity (comunidade e prova)**; **lista de domínios candidatos do `site:` e do slot de domínio** | nº de fontes influenciadoras; source gap; **share de página própria entre as citadas (piso de mercado: 2,8%)** |
| 6. Auditoria técnica para IA e agentes | Sem. 4 a 6 | Crawl, render, estrutura, schema, feeds, bot rules, agentes | robots.txt e matriz de crawlers; Cloudflare/WAF antes de 15-set; sitemaps; IndexNow; schema; **feeds (Merchant Center, Shopify, UCP) como entregável de primeira ordem no comércio**; **três camadas de agent readiness (recuperabilidade, atribuição, transação) e decisão sobre WebMCP** | % indexável; schema coverage; bloqueios por CDN; **cobertura de feed**; **score por camada** |
| 7. Conteúdo e entidades | Sem. 5 a 8 | Recuperabilidade, clareza de entidade, resposta direta, **evidência verificável** | briefs por cluster; pilar; FAQ; tabelas; about/entity page; autoria; evidência diversa (Agosto §6.1); **cada fato-chave com fonte checável (VCR, `2608.11390`)**; **quatro fontes alinhadas: página, schema, plataforma de registro, terceiros (Baker)** | cited pages; information gain; AI citation lift; conversão |
| 8. PR digital e autoridade externa | Sem. 6 a 12 | Fazer a web corroborar os claims | fontes-alvo, pitches, listicles, reviews, dados proprietários; **orçamento de PR como canal de aquisição com meta trimestral de citações (Shafton)** | menções qualificadas; inclusão em comparativos; citation lift em prompts não-branded |
| 9. Correção de representação | contínua | Corrigir descrições erradas, atributos ausentes e **substituições** | dossiê "como a IA descreve a marca"; correções em site, perfis, terceiros; **teste de substituição: perguntar pela marca e pela categoria e comparar** | % respostas corretas; menções negativas falsas |
| 10. Operação mensal de experimentos | mensal | hipótese → implementação → medição → aprendizado | backlog, changelog por URL, cohort, controle on-domain (`2606.04362`), report; **juiz-LLM como conselheiro com gate determinístico (`2609.02246`)** | tempo até citação; AI referrals; ROI direto e modelado |

**Cadência:** mantida (semanal, quinzenal, mensal, trimestral). **Papéis:** os cinco da Wave Agosto mais **dono do feed e do catálogo** em qualquer cliente que venda produto.

**Prazos do trimestre:** 15-set Cloudflare; 17-set contratos do dataset europeu; 27-set fim do Sonar; 01-out fim do Max CPC no Bing Ads (Agosto §2.4); 13-out Semrush Spotlight (Londres); 12 e 13-out Ahrefs Evolve; Q4 solução NIQ + Similarweb.

---

## 5. Medição, KPIs e report

### 5.1. Hierarquia em três níveis (reconciliação com Semrush 02-set)

A Semrush publicou em 02-set um modelo de report em três níveis: nível 1 (impacto no negócio: conversões orgânicas e conversões de referral de IA), nível 2 (contexto de visibilidade: AI Visibility Score, citações e menções, rankings, share of voice), nível 3 (sinais de apoio: backlinks, sentimento); mensal para os níveis 1 e 2, trimestral para o 3; atribuição por GA4 mais formulário "como nos conheceu". O "GEO URL Ledger" da Wave Agosto (§5.4) continua o formato por URL; o que muda é a ordem de apresentação, que passa a ser negócio primeiro.

| Nível | KPI | Definição operacional | Fonte primária localizada? |
|---|---|---|---|
| 1 Negócio | AI referral conversions | conversões em sessões com referrer ou UTM de assistente (piso: a maioria chega sem referrer) | Semrush 02-set ✓; Similarweb 03-set (770,7 milhões de visitas mensais como universo) |
| 1 Negócio | Conversão autodeclarada | "como nos conheceu" no formulário e no CRM | Semrush 27-jul e 02-set ✓ |
| 1 Negócio | Paid AI: share de respostas com anúncio, CTR, CPC | Similarweb AI Ads; Ads Manager do ChatGPT | Similarweb 03-set ✓; OpenAI 31-ago ✓ |
| 2 Visibilidade | Citation rate, mention rate, AI SoV | por motor, **com modelo declarado**, com N por convergência | Peec, Semrush; `2607.10341` |
| 2 Visibilidade | Impressões em IA (GSC) | relatório oficial; por página, país, dispositivo | Google 31-ago ✓ |
| 2 Visibilidade | Share de página própria entre citadas | páginas do domínio ÷ fontes citadas para prompts de compra da categoria | Shero 26-ago (secundária) como referência de mercado |
| 2 Visibilidade | Cobertura de feed | SKUs no feed ÷ SKUs vendidos; presença no Shopping do ChatGPT | Profound 03-set ✓ |
| 3 Apoio | Sentimento, substituição, accuracy | juiz-LLM com gate humano; teste marca × categoria | Forrester 03-set; `2609.02246` |
| 3 Apoio | Agent readiness por camada | score das três camadas | SALT via SEJ (secundária) |
| 3 Apoio | Crawl-to-referral; bloqueios | logs; radar.cloudflare.com | Julho-22B §5 |

**Clique quando citado, para calibrar expectativa:** Seer Interactive (abr-2026, 53 marcas, 5,47 milhões de consultas, 2,43 bilhões de impressões, jan/2025 a fev/2026): CTR orgânico de 3,3% sem AIO, 2,1% quando citado no AIO, 0,9% quando não citado; ser citado rende 120% mais cliques por impressão que não ser, e ainda assim 38% abaixo de uma consulta sem AIO. É a régua para a promessa comercial de "ser citado".

**Regra dos 9 KPIs** (Wave Junho) mantida: ≤11 no board. **Regra de parada:** coleta de citação para no platô de estabilidade de ranking mais suficiência estrutural (`2607.10341`); reportar o número de execuções que a regra exigiu, por plataforma.

### 5.2. O que foi desmentido ou perdeu força no período

| Narrativa | Evidência | Regra editorial |
|---|---|---|
| "O relatório de IA do Search Console traz cliques" | Search Console Help: só impressões | dizer "impressões em IA"; nunca "cliques em AIO" a partir do GSC |
| "AI Mode é um motor, mede-se uma vez" | 3.7 Flash em agosto, 3.8 Flash em 02-set, respostas sem link em 03-set | declarar modelo e data em toda leitura de AI Mode |
| "Reddit é fonte estável do ChatGPT" | 3,8% → 0,5% (Semrush); 84 buscadas, zero citadas (Suganthan) | Reddit é insumo de busca, não citação; diversificar |
| "Ser recomendado é ser citado" | Shero: página própria 2,8% das fontes; Trendos: UGC cerca de 50% | separar mention share de citation share em todo report |
| "Clique em fonte do AIO é relevante" | `2608.04831`: cerca de 1% das visitas com AIO; `2608.18352`: remover IA aumenta cliques | citar o experimento, não o painel de vendor |
| "A IA substitui a busca" | `2607.04282`: conteúdo precede o assistente (+20,6 pontos); assistente fica no meio da jornada | copy de "fim da busca" está errada na evidência |
| "AI Mode mostra os mesmos produtos e preços" | Productrise: 1,28% de overlap; preço maior em 68,4% | auditar preço no AI Mode como item próprio |
| "`llms.txt` e Markdown ajudam" | Common Crawl 584 mil arquivos; Mueller 31-ago | mantido em §8.b |
| "Basta um N fixo de execuções" | `2607.10341`: nenhum orçamento fixo se justifica em todos os contextos | regra de parada por convergência |
| "GEO é separado de SEO" | Search Institute 25-ago; Lily Ray 02-set; overlap Perplexity 82% | GEO = camada de resposta sobre a mesma fundação |
| "Guardrail de segurança filtra GEO enganoso" | `2609.02316`: no máximo 5,7% de redução | conteúdo verificável é a defesa que o motor vai premiar |

### 5.3. Separação obrigatória em todo report

`orgânico clássico` | `citação orgânica em IA (com modelo declarado)` | `AI referral (piso)` | `AI paid (share de respostas com anúncio, CTR, CPC)` | `conversão assistida e autodeclarada`. Novidade v2: a coluna de comércio (`cobertura de feed`, `presença no Shopping`) é obrigatória para quem vende produto.

### 5.4. Template de report mensal ("GEO URL Ledger" v2)

1. Sumário executivo em cinco bullets (ganhos, perdas, riscos, decisões, próximos testes). 2. Nível 1: conversões orgânicas, conversões de AI referral, autodeclaradas, paid AI. 3. Nível 2: visibilidade por engine (ChatGPT, Perplexity, Gemini, AIO, AI Mode com modelo, Copilot, Claude e Claude Code separados) com N exigido pela regra de parada e faixa. 4. Impressões em IA do GSC por página. 5. Páginas vencedoras e perdedoras por URL. 6. Concorrentes e fontes citáveis por motor (SoV, source gaps, share de página própria). 7. Técnico e agentes (crawl, schema, feeds, bot rules, camadas de agent readiness, quebras de série). 8. Conteúdo publicado e hipótese de cada peça. 9. Nível 3 trimestral (sentimento, substituição, backlinks). 10. Plano de 30 dias (ICE ou RICE, owner, prazo).

**Incerteza, como bastidor (DIRETRIZ §12):** faixa e amostra; modelo e data; "observado" ≠ "inferido"; controle on-domain declarado; cobertura do índice quando o KPI é citação verificada; número de execuções até a convergência.

---

## 6. Camada semântico-vetorial: o que a evidência de setembro acrescenta

### 6.1. O sinal que se otimiza degrada o ecossistema (primária)
CHASE (`2608.30466`) mostra em simulação controlada que 20 rodadas de adaptação a um sinal fixo de ranking de LLM reduzem o alinhamento entre ranking e qualidade em todos os seis domínios testados, com controle que isola o efeito do incentivo. Somado a `2608.13956` (diversidade > redundância) e ao survey `2607.14035`, o quadro é: ganhos de citação por reescrita são reais no curto prazo, coletivamente autodestrutivos e detectáveis. A regra de composição de conteúdo da casa continua: formas distintas de evidência para um mesmo fato, nunca clones, e cada fato com fonte que o próprio motor consiga checar.

### 6.2. Ataque, defesa e mecanismo
- **Lado ofensivo automatizado:** Agent2UCB (`2608.29063`, bandit sobre nove estratégias) e a seleção combinatória com consciência de concorrente (`2608.27631`). O "AI marketer" dos vendors (Profound Context Manager, 01-set) é a versão comercial do mesmo desenho.
- **Lado defensivo:** Counter-GEO-Bench (`2609.02316`) mede que guardrails de segurança deixam passar GEO distorcivo como "conteúdo informativo fluente" (redução de ASR de no máximo 5,7%) e que um detector leve reduz 47,6% quase sem custo de utilidade; GEO-Flag (`2608.16824`, Agosto §6.3) já detectava sobre-otimização com F1 0,944; SafeGEO (`2606.28356`) mostra que defesas simples do agente cortam até 39,2% da promoção de produto defeituoso.
- **Mecanismo:** VCR (`2608.11390`) demonstra que a plataforma que recompensa conteúdo verificável obtém o melhor resultado líquido (+12,1 pontos sobre a melhor defesa). É o incentivo que os motores têm para premiar exatamente o que a DIRETRIZ exige: número com origem, data, método e denominador.
- **Superfície de ataque:** `2608.15814` mostra que a barreira de injeção depende da autoridade do publisher e da função de busca do motor, não do perfil do usuário. Earned media em domínios de autoridade é, além de tática, defesa.

### 6.3. Recuperação, frescor, rerank e embeddings
- **Frescor com número:** meia-vida de página citada de 39 dias em consultas de alta temporalidade e 68 dias em baixa (`2607.15771`, motores em chinês); janelas de frescor do ChatGPT de 2 a 3.650 dias por tipo de consulta (Suganthan, secundária). Data de atualização substantiva continua alavanca (Julho-22 §3).
- **Regra de parada de coleta:** `2607.10341` (§5.1).
- **Concentração de fontes:** 43,6% das citações em inglês nos 10 domínios mais citados em saúde mental (`2609.00319`); YouTube e Reddit somam 41,4% das citações do AIO nos EUA (Ahrefs, 02-set). O espaço vetorial que importa é o dos domínios candidatos por tema; entrar nele é trabalho de entidade e de autoridade, não de chunk.
- **Embeddings e rerank:** nenhum lançamento primário com resultado completo no MTEB localizado entre 20-ago e 03-set. Referências de mercado (secundárias, conferir na página do vendor antes de citar): Qwen3-Embedding-8B 70,75 no MTEB multilingual v2 (Apache 2.0); voyage-4, voyage-4-large e Cohere embed-v4.0 com resultados em 2 de 131 tarefas em 20-ago; Gemini Embedding 2 (março) e Jina v5-omni (maio) são os fundadores do semestre.
- **Chunking:** sem primária nova; regra da casa mantida (Agosto §6.2). A Semrush (02-set) converge: um título, uma pergunta; conteúdo no HTML bruto; parágrafo com uma ideia.

---

## 7. Brasil (20-ago → 03-set)

| Fato | Data | Fonte | Rótulo |
|---|---|---|---|
| Primeiros anúncios do ChatGPT exibidos no Brasil; oitavo mercado; só Free e Go; "20% dessas pesquisas têm intenção comercial direta"; agências WPP, Publicis, Omnicom, Monks, BETC Havas | 04-ago | Meio & Mensagem ✓ | PRIMÁRIA de imprensa; a OpenAI datou o anúncio global em 11-ago (Agosto §7) |
| Lançamento oficial do ChatGPT Ads no Brasil e abertura do Ads Manager | 11-ago | OpenAI (Agosto §7) ✓; Poder360 | PRIMÁRIA; blogs que citam 06-ago não têm confirmação |
| OpenAI abre operação no Brasil (São Paulo): 215 milhões de mensagens por dia, terceiro maior mercado, segundo em uso de API; Prodam e ITA | 18-ago (evento), 27-ago (início comercial) | Poder360 21-ago, Olhar Digital 27-ago ✓ | SECUNDÁRIO citando a OpenAI; página pt-BR da OpenAI 403 |
| ChatGPT: 324,3 milhões de visitas no Brasil em junho | 19-ago | EducaSEO citando Similarweb | SECUNDÁRIO; painel não aberto |
| GEO como 30,4% das prioridades de marketing em 2026 | 22-ago | Tecnois citando 8D Hubify e PipeLovers | SECUNDÁRIO; estudo primário não localizado; não citar |
| "GEO é a nova onda do marketing digital" | 26-ago | O Globo, conteúdo patrocinado (Dino) | PATROCINADO; não é imprensa |
| SEO Summit '26 em São Paulo | 05-nov | agregador de eventos | SECUNDÁRIO |
| Conversion: notas sobre expansão seletiva de AIO, teste de Markdown do Mueller, consultas do AI Mode três vezes mais longas, UCP | 25-ago a 02-set | blog Conversion ✓ (títulos; datas por inferência da listagem) | SECUNDÁRIO |
| Case Icatu Seguros: 82% de share de referências em AIO e 353 mil cliques em 16 meses | 2026 | Conversion (case do vendor) | SECUNDÁRIO; sem método aberto; não citar como benchmark |
| PL 2338 deve ficar para 2027 (Eduardo Gomes) | ago | Telesíntese | SECUNDÁRIO; data não conferida |
| Gemini 3.8 Flash no AI Mode para assinantes Pro e Ultra "ao redor do mundo" | 02-set | Google ✓ | PRIMÁRIA (inclui Brasil por inferência; não verificado em conta brasileira) |
| CADE, ANPD, RD Summit, Web Summit Rio, Folha, Estadão, UOL, Valor sobre GEO ou busca por IA | — | não localizado na janela pelas rodadas | manter Julho-22C §4 |

Leitura: o fato brasileiro do mês continua sendo o anúncio dentro do ChatGPT, agora com a data local (04-ago) e a regra de exibição (Free e Go, maiores de 18). A imprensa nacional segue rala em GEO; a Conversion é a única casa brasileira publicando em cadência semanal sobre o tema, e o faz como tradução de notícia internacional, sem dado próprio. Janela de autoridade aberta (Julho-22C §5 confirmada pela terceira wave seguida).

---

## 8. Correções e conflitos (precedência sobre o corpus anterior)

- **a) Spam update de agosto terminou em 21-ago, não em 20-ago.** Search Engine Roundtable, relatório de setembro. Corrige Agosto §2.1 e §8.d na data de fim; a inexistência de core update se mantém.
- **b) `llms.txt` e Markdown "para IA": status reforçado.** Common Crawl (584.107 arquivos, 68,27% por plugin, 22,56% sem link) e Mueller (31-ago). Continua opcional, custo zero, nunca entregável cobrado, nunca KPI. Adendo: gerar `llms.txt` por plugin sem revisão pode publicar política de crawler que o robots.txt não aplica; onde existir, conferir o conteúdo.
- **c) Medição do AI Mode exige modelo declarado.** Três Flash em seis semanas (3.7 em agosto, 3.8 em 02-set). Qualquer série de citação no AI Mode sem o campo "modelo" fica inválida a partir desta wave. Julho-22 §2 (N execuções) ganha a dimensão "modelo".
- **d) N fixo de execuções sai; regra de parada entra.** `2607.10341` substitui "N≥5 monitoramento, N≥30 pré/pós" por convergência medida; os mínimos antigos viram piso de segurança, não alvo.
- **e) Reddit: de "fonte instável" para "insumo invisível".** 3,8% → 0,5% e busca sem citação. Sai de todo exemplo de fonte citada; entra como exemplo de fonte consultada.
- **f) A medição de share de `site:` proposta em Agosto §9.2 perdeu o campo.** `search_queries` não existe mais no payload; o slot de domínio do novo formato é a variável a extrair.
- **g) "Clique em fonte de AIO" tem número primário: cerca de 1% (`2608.04831`).** Substitui as estimativas de vendor da Wave Agosto onde o assunto for clique em citação.
- **h) Perplexity: `sonar-pro` sequencial deixa de ser plano B em 27-set.** A Agent API é o único caminho; o alias `pplx` do `geo-orchestrator` e o braço do `papers` precisam migrar antes. Nesta sessão a API estava sem crédito (`insufficient_quota`): recarga é decisão do titular (alexandre.brt14@gmail.com), não do agente.
- **i) Comércio: feed antes de página.** No Shopping do ChatGPT o feed integrado passou a decidir (61,54%). Qualquer guia de e-commerce do portal que ensine "otimize a página de produto para o ChatGPT" sem falar de feed está desatualizado.
- **j) GEO = camada sobre SEO: passa de tese da casa a consenso público.** Google (guia e Mueller), Search Institute, Lily Ray, Tim Soulo e o survey SEOFOMO (77% dos times de SEO lideram IA) convergem. Copy que venda "GEO em vez de SEO" está errada.

---

## 9. Aplicação por repositório

### 9.1. `landing-page-geo` (alexandrecaramaschi.com)
1. **Painel `/roadmap` e digest:** adicionar a série "impressões em IA (GSC)" desde 31-ago e as quebras de série (goto 26-ago, GA4 01-set, modelo do AI Mode 02-set); exibir "modelo ativo" ao lado de toda leitura do AI Mode.
2. **Decisão de opt-in:** o site permanece nas superfícies de IA (a tese comercial é ser citado); registrar a decisão e o motivo na página de metodologia.
3. **Artigos HBR novos (3):** "O que o relatório de IA do Search Console mostra e o que esconde" (impressões sem clique; `2608.04831`, `2608.18352`); "O feed venceu a página: o que o ChatGPT 5.6 fez com o Shopping" (Profound); "Marca recomendada não é marca citada" (Shero, Trendos, `2609.00319`). Cada um com evidência diversa e fontes checáveis.
4. **Oferta:** "Auditoria de fontes citáveis por motor" (etapa 5 v2) e "Prontidão para agentes em três camadas" (etapa 6 v2, com WebMCP como decisão, não promessa).
5. **Visibilidade de pessoa:** `2607.23893` fundamenta a página do Alexandre como entidade nomeada; medir "o motor nomeia o consultor?" em pt-BR e em inglês.
6. Copy comercial: separar "citação orgânica" de "ChatGPT Ads" com os números de 03-set (26% das respostas com anúncio; CTR 0,50%).

### 9.2. `papers` (pipeline arXiv e coleta)
1. **Ingestão tagueada:** `2609.02316`, `2609.00319`, `2608.30466`, `2608.30023`, `2608.29063`, `2608.27631`, `2607.10341` v2, `2607.04282` v3, `2608.18352`, `2608.04831`, `2608.15896`, `2608.11390`, `2608.15814`, `2607.23893`, `2607.27686`, `2607.15771`, `2606.28356`, `2606.16344`, `2606.12439`, `2609.02246`.
2. **Metodologia:** adotar a regra de parada de `2607.10341` na coleta diária (reportar convergência por braço e por vertical); registrar o modelo ativo em cada braço, especialmente Gemini (3.7 e 3.8 Flash na janela); `2609.00319` é o comparável direto da hipótese de penalidade de idioma em pt-BR (pré-registrar: "consultas em português recebem menos citações e menor roteamento a fontes em português").
3. **Braço Perplexity:** migrar para a Agent API antes de 27-set; sem crédito, o braço fica `api_failure`, não `routed_out`.
4. **Extrator novo:** o campo `search_queries` do ChatGPT desapareceu; capturar o slot de domínio do formato pipe quando disponível.
5. **Related work:** `2608.18352` (experimento causal), `2608.04831` (painel representativo) e `2607.04282` (topologia da jornada) entram na discussão de limitações dos quatro papers.

### 9.3. `curso-factory` (EAD)
1. **Aulas novas:** "O relatório de IA do Search Console: impressões, não cliques"; "Feed antes de página: comércio nos motores de resposta"; "Marca recomendada não é marca citada"; "Quando parar de medir: convergência em vez de N fixo".
2. **Reviewer:** quatro vetos novos: "cliques do AIO no Search Console", "AI Mode" sem modelo declarado, "Reddit como fonte citada", "GEO em vez de SEO". Mantidos os quatro da Wave Agosto.
3. **`writer.py` e `quality_judge`:** o juiz-LLM vira conselheiro com gate determinístico (`2609.02246`): acentuação, links, números com fonte são gates que o juiz não anula.
4. Guia de hospedagem e turismo: `2606.16344` (nota, preço e posição na lista) entra como evidência causal.

### 9.4. `Escrita-Empresarial` (gate e fichas)
1. **Fichas de fato** em `pesquisa/geo-wave-setembro-2026-fichas.md` para os 14 fatos primários desta wave; são os únicos números de GEO de setembro autorizados em texto.
2. **Léxico candidato ao gate:** "cliques em AI Overviews" com origem no Search Console; "AI Mode" sem modelo e data; "Reddit" como fonte citada do ChatGPT; "GEO substitui SEO".
3. **Regra de evidência verificável** como orientação (não cota): todo número em texto executivo precisa ser localizável pelo próprio motor de resposta, isto é, publicado em página aberta com data.

---

## 10. Claims machine-readable

```yaml
wave: setembro-2026
data: 2026-09-03
precedencia: [setembro, agosto, julho-22c, julho-22b, julho-22, julho, wave19, 15b]
claims:
  - id: gsc-ai-report-global
    valor: "relatorio de desempenho em IA generativa e controle de exclusao para todos os sites do mundo; impressoes por pagina, pais, dispositivo, data; sem cliques"
    fonte: {tipo: primaria, nome: Google Search Console Help, data: 2026-08-31, url: https://support.google.com/webmasters/answer/16984139}
  - id: gemini-3-8-flash-ai-mode
    valor: "Gemini 3.8 Flash disponivel no AI Mode para assinantes Pro e Ultra; US$ 0,75 / 3,75 por milhao ate 31-dez-2026"
    fonte: {tipo: primaria, nome: Google, data: 2026-09-02, url: https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/}
  - id: chatgpt-ads-1bi
    valor: "US$ 1 bilhao de receita anualizada em anuncios em menos de 200 dias; 40+ paises; maioria das campanhas em CPC ou lance por resultado; anuncios nao influenciam respostas"
    fonte: {tipo: primaria, nome: OpenAI, data: 2026-08-31, url: https://openai.com/index/expanding-access-to-ai-with-chatgpt-ads/}
  - id: chatgpt-ads-brasil-04-ago
    valor: "primeiros anuncios exibidos no Brasil em 04-ago-2026; oitavo mercado; apenas planos Free e Go"
    fonte: {tipo: primaria-imprensa, nome: Meio & Mensagem, data: 2026-08-04, url: https://www.meioemensagem.com.br/midia/chatgpt-comeca-a-exibir-anuncios-aos-usuarios-do-brasil}
  - id: similarweb-chatgpt-ads-penetracao
    valor: "26% das respostas do ChatGPT no desktop dos EUA com anuncio em junho de 2026 (14% em maio); CTR 0,50%"
    fonte: {tipo: primaria-vendor, nome: Similarweb, data: 2026-09-03, url: https://aisearch.similarweb.com/blog/chatgpt-ads-reshaping-paid-search/}
  - id: profound-chatgpt-56-shopping-feed
    valor: "recuperacao por feed integrado de 8,26% para 61,54% em 10-jul-2026; top-10 lojistas de 22,5% para 41,8%; lojistas unicos -20%"
    fonte: {tipo: primaria-vendor, nome: Profound, data: 2026-09-03, url: https://www.tryprofound.com/blog/chatgpt-5.6-shopping-transformation}
  - id: semrush-reddit-chatgpt-0-5
    valor: "citacoes ao Reddit no ChatGPT de 3,8% para 0,5% entre 18-jul/07-ago e 14/17-ago-2026 (Promptwatch)"
    fonte: {tipo: primaria-vendor, nome: Semrush, data: 2026-08-26, url: https://www.semrush.com/blog/reddits-citations-in-chatgpt-fall/}
  - id: ahrefs-aio-most-cited-set-2026
    valor: "AIO nos EUA, 3 milhoes de consultas: YouTube 22,9%, Reddit 18,5%, Facebook 10,1%, Google 8,8%, Instagram 5,6%, Quora 4,7%, Wikipedia 4,0%"
    fonte: {tipo: primaria-vendor, nome: Ahrefs, data: 2026-09-02, url: https://ahrefs.com/blog/most-cited-domains-ai-overviews/}
  - id: common-crawl-llms-txt
    valor: "584.107 arquivos llms.txt no crawl de julho de 2026; 68,27% gerados por plugin; 49,90% seguem a spec; 22,56% sem link"
    fonte: {tipo: primaria, nome: Common Crawl, data: 2026-08-31, url: https://commoncrawl.org/blog/a-content-analysis-of-llms-txt-files-from-the-july-2026-crawl-archive}
  - id: perplexity-sonar-retire
    valor: "endpoints Sonar aposentados em 27-set-2026; Agent API como sucessora"
    fonte: {tipo: primaria, nome: Perplexity API Platform Forum, data: 2026-08-13, url: https://community.perplexity.ai/t/sonar-is-moving-to-the-agent-api/5802}
  - id: eu-chatgpt-vlose
    valor: "Comissao Europeia designa o ChatGPT como Very Large Online Search Engine; quatro meses para cumprir o DSA"
    fonte: {tipo: primaria, nome: Comissao Europeia, data: 2026-08-31, url: https://digital-strategy.ec.europa.eu/en/news/commission-designates-chatgpt-reddit-roblox-under-digital-services-act}
  - id: google-eu-search-dataset
    valor: "contratos de licenciamento a partir de 17-set-2026; amostras a partir de 16-nov-2026; dados de ranking, consulta, clique e visualizacao no EEE"
    fonte: {tipo: primaria, nome: Google Search Central, data: 2026-09-01, url: https://developers.google.com/search/help/about-search-data-program}
  - id: seofomo-state-2026
    valor: "171 profissionais de 36 paises (17 a 27-ago-2026): 69% com orcamento para IA; 92% medem citacoes; medir com confiabilidade e o desafio n1 (19%); 46% atribuem 0 a 5% da receita a IA"
    fonte: {tipo: primaria, nome: SEOFOMO, data: 2026-08, url: https://hub.seofomo.co/surveys/state-ai-search-optimization/}
  - id: ahrefs-chatgpt-1000-paginas
    valor: "das 1.000 paginas mais citadas pelo ChatGPT, 32,3% sao influenciaveis; 28% sem visibilidade organica; DR mediano 90; 76,4% atualizadas nos ultimos 30 dias"
    fonte: {tipo: primaria-vendor, nome: Ahrefs (FR), data: 2026-08-31, url: https://ahrefs.com/fr/blog/pages-plus-citees-par-chatgpt/}
  - id: adobe-brand-visibility-ga
    valor: "Adobe Brand Visibility em disponibilidade geral em 04-ago-2026; metricas por resposta desde 20-ago"
    fonte: {tipo: primaria, nome: Adobe Experience League release notes, data: 2026-08-20, url: https://experienceleague.adobe.com/en/docs/brand-visibility/using/essentials/release-notes}
  - id: seer-ctr-citado-aio
    valor: "CTR organico 3,3% sem AIO, 2,1% citado no AIO, 0,9% nao citado; 53 marcas, 5,47 milhoes de consultas, jan/2025 a fev/2026"
    fonte: {tipo: primaria-vendor, nome: Seer Interactive, data: 2026-04, url: https://www.seerinteractive.com/insights/aio-impact-on-google-ctr-2026-update}
  - id: counter-geo-bench
    valor: "guardrails de prateleira reduzem ASR em no maximo 5,7% relativo; C-GEO Guard reduz 47,6% com perda de utilidade quase zero"
    fonte: {tipo: primaria, nome: arXiv 2609.02316, data: 2026-09-02, url: https://arxiv.org/abs/2609.02316}
  - id: chase-homogenizacao
    valor: "20 rodadas de adaptacao a ranking de LLM reduzem alinhamento ranking-qualidade em seis dominios (delta rho medio -0,068); AUC ranking-citacao 0,853"
    fonte: {tipo: primaria, nome: arXiv 2608.30466, data: 2026-08-31, url: https://arxiv.org/abs/2608.30466}
  - id: rank-stability-regra-de-parada
    valor: "nenhum orcamento fixo de consultas se justifica em todos os contextos; parada por estabilidade de ranking e suficiencia estrutural; 30 combinacoes plataforma-topico"
    fonte: {tipo: primaria, nome: arXiv 2607.10341 v2, data: 2026-08-26, url: https://arxiv.org/abs/2607.10341}
  - id: aio-clique-1-por-cento
    valor: "clique em fonte citada no AIO em cerca de 1% das visitas com AIO; painel representativo de 900 adultos dos EUA"
    fonte: {tipo: primaria, nome: arXiv 2608.04831, data: 2026-08-05, url: https://arxiv.org/abs/2608.04831}
  - id: aio-experimento-referral
    valor: "experimento de campo pre-registrado (N=1.100): remover AIO e AI Mode aumenta cliques a publishers; AI Mode sozinho reduz cliques e confianca"
    fonte: {tipo: primaria, nome: arXiv 2608.18352, data: 2026-08-18, url: https://arxiv.org/abs/2608.18352}
  - id: sources-of-truth-concentracao
    valor: "15.942 citacoes em 1.140 respostas; 10 dominios concentram 43,6% das citacoes em ingles; consultas fora do ingles recebem menos citacoes"
    fonte: {tipo: primaria, nome: arXiv 2609.00319, data: 2026-08-31, url: https://arxiv.org/abs/2609.00319}
  - id: profound-claude-vs-claude-code
    valor: "24.135 respostas: Claude Code busca em 13% contra 93% do Claude; 1 em 5 marcas coincide"
    fonte: {tipo: primaria-vendor, nome: Profound, data: 2026-08-24, url: https://www.tryprofound.com/blog/claude-and-claude-code-are-distinct-answer-engines}
vetos:
  - "cliques em AI Overviews com origem no Search Console (o relatorio so tem impressoes)"
  - "leitura de AI Mode sem modelo e data declarados"
  - "Reddit como fonte citada estavel do ChatGPT"
  - "GEO em vez de SEO"
  - "core update de agosto de 2026 (nao existe; spam update 18 a 21-ago)"
  - "volume de prompt sem rotulo de estimativa"
  - "llms.txt como entregavel, KPI ou fator"
  - "IA converte 4-5x como constante"
  - "taxa de alucinacao sem declarar cobertura do indice verificador"
  - "otimizar pagina de produto para o ChatGPT sem feed"
```

---

## 11. Fontes verificadas nesta sessão (03-set-2026)

Abertas com string-sentinela ou leitura integral (✓), só título e data (○), ou bloqueadas: Search Console Help 16984139 ✓ · Search Engine Roundtable relatório de setembro ✓ · Search Engine Roundtable recap 02-set ✓ · Search Engine Roundtable GSC live 01-set ✓ · Search Engine Roundtable Gemini 3.8 AI Mode ✓ · Search Engine Roundtable "Not Link / Citation Friendly" ○ · Google blog Gemini 3.8 Flash ✓ · Google preferred-sources ✓ · Google spam policies (28-ago) ✓ · Google programa europeu de dados ✓ · Google blog DSA→AI Max ✓ · Google Search Central updates ✓ · OpenAI ads milestone ✓ (via navegador logado) · Comissão Europeia DSA ✓ · Perplexity forum Sonar ✓ · Common Crawl llms.txt ✓ · Chrome WebMCP ✓ · Profound blog índice, Shopping 5.6, Claude vs Claude Code ✓ · Ahrefs most-cited AIO, discussions and forums, information gain, índice do blog, FR 1.000 páginas, FR santé ✓ · Adobe release notes ✓ · ppc.land Semrush Claude e Preferred Sources ✓ · Seer AIO CTR 2026 ✓ · Anthropic Mythos 5.1 ✓ · Poder360 OpenAI Brasil ✓ · Semrush Reddit, report template, where AI gets information, AI agents, índice do blog ✓ · Similarweb aisearch índice, referral by industry, ChatGPT Ads, AI search trends (jun), news 23-ago ✓ · NIQ + Similarweb ✓ · SEOFOMO survey ✓ · SEJ: Suganthan 25 e 27-ago, Trendos, Shero, YouGov, Mueller markdown, VLOSE, WebMCP, Gemini 3.8 AI Mode, SALT, Baker schema, Shafton, Forrester 27-ago e 03-set, Productrise, índice ✓ · Search Institute ✓ · Meio & Mensagem ✓ · Conversion índice ✓ · Peec changelog ✓ · Lily Ray Substack (abr) ✓ · The Register Gemini 3.8 ✓ · arXiv: 23 IDs na página `abs` ✓ (lista em §1). **Bloqueadas:** OpenAI pt-BR (403), Google blog Preferred Sources button (404), Search Engine Land (403 e desafio Cloudflare no navegador logado: GSC global 486269, AI Max 485006, Lily Ray 486614), CNBC (403), Kevin Indig (sem arquivo), Google blog hotel booking (404), Search Status Dashboard (404), ACM DOI 3805712.3808445 (desafio Cloudflare; confirmado por arXiv 2605.25517 e busca). **Perplexity API:** `insufficient_quota` em `chat/completions` e `/v1/agent`.
