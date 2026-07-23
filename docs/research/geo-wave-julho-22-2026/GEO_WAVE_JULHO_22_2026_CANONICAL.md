# Wave Julho-22 2026 · Corpus científico arXiv + estado da arte de medição e execução GEO (14-jul → 22-jul-2026)

**Data:** 22-jul-2026 · **Método:** orquestrador multi-LLM Brasil GEO (Perplexity `sonar-deep-research` ×3, Grok live search ×1, conselho GPT/Gemini/Claude) + 2 subagentes de pesquisa web com verificação de fonte primária + coleta direta na API do arXiv (https, 3 queries, XMLs brutos preservados). Proveniência bruta em `raw/`.

**Precedência:** em conflito de fatos, esta wave prevalece sobre as anteriores: **Julho-22 §7 > Julho §7 > Wave 19 §7 > 15B §8**. Esta wave é **delta e aprofundamento**: não substitui a Wave Julho (14-jul), que permanece canônica no que não for atualizado aqui.

---

## 0. Sumário executivo (TL;DR) — o que é NOVO em relação à Wave Julho (14-jul)

A novidade estrutural desta wave não é mais um número de mercado: é a **maturação do corpus científico de GEO**. Em 22-jul-2026 existem **32 papers únicos relevantes no arXiv** (31 com ID de 2026; 1 submetido em 30-dez-2025 e anunciado em jan/2026), todos com existência e abstract verificados via API nesta coleta — incluindo um survey crítico do campo (jul/2026), frameworks de medição em dois estágios (seleção vs absorção de citação), o primeiro baseline de visibilidade de marca em escala que localizamos (100k+ respostas), benchmarks de manipulação e defesas propostas, e a fronteira "agent-ready". A ciência de 2026 valida parte do nosso corpus, corrige exageros do mercado e entrega protocolos de medição prontos para adoção. Profundidade de verificação: existência + abstract; os números citados derivam dos abstracts; PDFs completos NÃO foram lidos nesta wave (ler antes de citar em paper ou copy).

| Achado NOVO (não estava na Wave Julho) | Número-chave / fonte primária | Impacto canônico |
|---|---|---|
| **Survey crítico de GEO (2023-2026)** | `arXiv:2607.14035` (15-jul-2026): 45 estudos revisados; GEO é pipeline estocástico e parcialmente observável; **"nenhuma técnica revisada demonstra efeito causal estável, longitudinal e cross-plataforma sobre descobribilidade orgânica"** (conclusão textual do abstract); os ganhos do paper fundacional são condicionais à fonte já estar no contexto | Antídoto canônico contra promessa inflada; base para contratos de medição honestos; adota o **vetor de visibilidade** (descobribilidade / citação / absorção / resultado econômico) como decomposição oficial de KPI |
| **Medição como distribuição, nunca ponto único** | `arXiv:2604.07585`: respostas variam entre execuções, prompts e tempo; visibilidade deve ser reportada como distribuição (N execuções + variância) | Regra de report: screenshot único de ChatGPT **não é evidência**; todo painel/report Brasil GEO declara N de execuções e janela |
| **Controle on-domain para descontar o crescimento da plataforma** | `arXiv:2606.04362` (experimento natural glasp.co): páginas tratadas com AEO cresceram 5,7x em referral do ChatGPT, mas o controle não tratado cresceu 3,5x (razão bruta ~1,63x); o **1,82x** (IC 95% 1,31–2,54) é o efeito de nível estimado pelo modelo de série temporal interrompida sobre a razão tratado/controle, não a divisão simples; placebo permutacional p=0,16 (sugestivo, não conclusivo) | Cases de mercado ("AEO deu 5x") superestimam efeito causal; auditorias e relatórios de resultado passam a exigir grupo de controle on-domain |
| **Seleção ≠ absorção de citação** | `arXiv:2604.25707` (dataset geo-citation-lab: 602 prompts, 21.143 citações, 72 features): Perplexity e Google citam mais fontes; ChatGPT cita menos com influência maior por citação; páginas de alta absorção são mais longas, estruturadas e ricas em **evidência extraível** (definições, números, comparações, passos) | Contar citações é KPI insuficiente; nasce o KPI de **absorção** (a página contribuiu com linguagem/fato/estrutura para a resposta?); redação otimiza densidade de evidência extraível |
| **Escada de estatura de marca (baseline em escala)** | `arXiv:2606.20065` (Ranqo: 100k+ respostas, 100+ marcas, mar–mai/2026): marcas globais aparecem em 73% das respostas relevantes, mid-market 44%, nicho 11% (~30 pp por degrau); ~78% das citações vão a sites corporativos; **listicles "best-of" de terceiros = ~21% de todas as citações**; YouTube lidera fora do owned; sentimento flipa 6,7x mais que menção | Expectativa por porte do cliente vira régua; fora do tier 1, prioridade nº 1 é presença em listicles de terceiros e YouTube; menção e sentimento são KPIs separados com volatilidades distintas |
| **Drivers causais de citação (maior experimento controlado)** | `arXiv:2605.25517` (252.000 trials, 6 LLMs, 18 fatores, pareado): maiores drivers = relevância temática e posição no contexto; **preço explícito e timestamp recente ajudam consistentemente**; formatação pura tem pouco impacto | Checklist de redação reordenado: relevância > preço/data explícitos > completude > formatação; casa com §5 da Wave Julho |
| **Estrutura é alavanca própria (+17,3% citação)** | `arXiv:2603.29979` (GEO-SFE): macro/meso/microestrutura otimizadas por arquitetura de motor: +17,3% taxa de citação, +18,5% qualidade em 6 motores | Disciplina separada da reescrita semântica; reforça §5.3 da Wave Julho (chunk é a unidade) com número experimental |
| **Diagnóstico antes de reescrita (+40% mudando 5%)** | `arXiv:2603.09296` (AgentGEO): taxonomia de modos de falha de citação por estágio + reparo direcionado: +40% relativo na citação modificando só 5% do conteúdo (baselines: 25%) | Muda o desenho de serviço: auditoria diagnostica ONDE o pipeline falha (retrieval? rerank? citação?) e intervém cirurgicamente; preserva voz editorial |
| **Fronteira agent-ready** | `arXiv:2607.12056` (13-jul-2026): mesmo site, versão agent-ready vs baseline, 3 browser-agents, 300 execuções: sucesso estrito 89,3% vs 49,3%; BrightEdge (08-abr-2026) [vendor-stated, metodologia não publicada]: requisições de agentes de IA = 88% da atividade de busca humana, ~15% do tráfego dos sites, 95% disso da OpenAI | GEO expande de "ser citado" para "ser operável por agente"; auditoria ganha camada agêntica (interpretabilidade, executabilidade, confiabilidade de decisão) |
| **Defesas contra manipulação estão sendo publicadas** | `arXiv:2605.21948` (SCI-Defense: Precision 1,000/FPR 0,000 no benchmark próprio de 600 descrições, dataset fechado; classifica como manipulação autoridade fabricada, comparativos e alegações temporais) + `arXiv:2605.09314` (persuasão é circuito estreito de attention heads, monitorável) + `arXiv:2606.28356` (SafeGEO). São propostas acadêmicas: NÃO implica que ChatGPT/Google/Perplexity as implementaram | Risco direcional: GEO "agressivo" (autoridade fabricada, superlativo comparativo) tende a virar alvo de filtro; GEO ético/verificável é resiliência do investimento, não só postura |
| **Fundação SEO primeiro tem número acadêmico** | `arXiv:2601.00912` (Discovery Gap: 112 startups, 2.240 queries): reconhecimento por nome 99,4%/94,3% vs descoberta 3,32%/8,29% (gap 30:1); **scores GEO não correlacionaram com descoberta real**; no Perplexity, o que prediz é SEO tradicional (referring domains r=+0,319; Reddit r=+0,395) | Confirma com dado acadêmico a tese "GEO = camada sobre SEO sólido" (81%/36% da Semrush ganha um irmão causalmente mais limpo) |
| **Janela de citações do ChatGPT estreitou** | seoClarity (mar/2026, `seoclarity.net/chatgpt-citation-decline-analysis`): desde mar/2026 o ChatGPT reduziu fortemente o share de respostas com citação externa e o nº de citações por resposta | Rebaixa a expectativa de tráfego citável via ChatGPT; sobe o peso relativo de **menção** (billboard) e de AI Mode/AIO no plano de medição |
| **llms.txt: adoção sobe, uso real quase nulo** | ppc.land: adoção 8,8x maior, mas **97% dos arquivos recebem zero requisições de sistemas de IA**; Google (15-jun-2026, docs oficiais): llms.txt não é usado pelos recursos de IA do Google Search | Veredicto canônico: llms.txt é sinal de agent-readiness para docs técnicas (agentes de código/MCP), irrelevante para busca; manter no template como higiene barata, nunca prometer como alavanca |
| **Mercado de ferramentas: commodity + consolidação** | Tim Soulo (05-mar-2026): 47 vendors de GEO; mecanismo (prompts agendados + dashboard) é commodity; ~80% devem sumir em 3–5 anos; diferencial = origem dos dados de prompts. Ahrefs Brand Radar: 406M+ prompts/mês (jul/2026; era ~340M na metodologia de abr); Conductor lançou AgentStack (apps nativos ChatGPT/Claude/Copilot + MCP); seoClarity lançou LiveWire (jul/2026) | Nossa diferenciação segue sendo diagnóstico causal + execução (não tracking); atualizar número do Brand Radar; observar a categoria "apps LLM nativos + MCP" como canal de distribuição de plataforma |

### Premissas operacionais consequentes (a partir de 22-jul-2026, somam-se às 6 da Wave Julho)

7. **Report de visibilidade é distribuição com controle.** N execuções por prompt, variância declarada, e (quando medir efeito de intervenção) grupo de controle on-domain para descontar o crescimento da plataforma. Sem isso, número de "resultado GEO" não entra em relatório executivo.
8. **KPI em 4 camadas do vetor de visibilidade:** descobribilidade (fui recuperado?), citação (fui citado?), absorção (a resposta usou meu conteúdo?), resultado econômico (tráfego/lead/receita). Cada camada tem instrumento e gargalo próprios; o diagnóstico nomeia a camada onde o cliente falha.
9. **Diagnóstico antes de reescrita.** O serviço padrão passa a ser: localizar o estágio de falha (crawling, retrieval, rerank, citação, absorção) e intervir no mínimo conteúdo necessário; reescrita em massa é exceção, não regra.
10. **Redação para absorção:** cada página relevante carrega evidência extraível (definição citável, número com fonte, comparação, passo a passo), preço explícito quando aplicável e data visível. Estrutura em 3 níveis (macro/meso/micro) é disciplina separada com meta própria.
11. **Camada agêntica na auditoria.** Interpretabilidade por máquina, acionabilidade (formulários/CTAs operáveis por agente) e sinais de confiabilidade entram no checklist técnico, ao lado de schema e crawlability.
12. **Linha ética com fundamento técnico:** não fabricar autoridade, não inflar comparativos nem alegações temporais — não apenas por ética, mas porque as defesas dos motores (SCI-Defense e similares) já detectam esses padrões com precisão alta.

---

## 1. O corpus científico 2026 (32 papers únicos, existência + abstract verificados nesta coleta)

Regra anti-GhostCite cumprida: os 32 IDs abaixo foram retornados pela API do arXiv em 22-jul-2026 (XMLs em `raw/geo_q1.xml`, `raw/geo_q2.xml`, `raw/geo_q3.xml`); os resumos derivam exclusivamente dos abstracts reais; PDFs não foram lidos. Digest completo por eixo em `raw/arxiv-digest-geo.md`. Nota sobre datas: a coluna Data reproduz o campo `published` da API (data da v1 submetida); o mês do ID arXiv é o mês de ANÚNCIO e pode divergir da submissão (ex.: `2601.00869` submetido em 30-dez-2025; `2606.12439` com `published` de 18-mai-2026). Em caso de dúvida, o campo da API prevalece sobre inferência pelo ID. `2606.04362` foi retornado também na query de controle "answer engine optimization" (deduplicated aqui).

| ID arXiv | Data | Título (abreviado) | Eixo |
|---|---|---|---|
| 2607.14035 | 15-jul-2026 | Critical Survey of GEO (2023-2026) | Medição |
| 2607.14197 | 15-jul-2026 | LLM Engines e ambiente informacional de conflitos | Risco |
| 2607.12056 | 13-jul-2026 | Agent-Ready Websites | Agêntico |
| 2606.27736 | 26-jun-2026 | ToE: verificação de claims vs GEO poisoning | Defesa |
| 2606.20065 | 18-jun-2026 | GEO at Scale (Ranqo, 100k+ respostas) | Medição |
| 2606.17443 | 16-jun-2026 | Incumbent Advantage (viés de marca em recomendação) | Mercado |
| 2606.16344 | 15-jun-2026 | Auditoria de recomendação de hotéis | Mercado |
| 2606.28356 | 08-jun-2026 | SafeGEO (riscos em agentes de recomendação) | Defesa |
| 2606.04362 | 03-jun-2026 | Disentangling AEO from Platform Growth (glasp.co) | Medição |
| 2606.12439 | 18-mai-2026 | Position: riscos e governança de GEO | Governança |
| 2605.29107 | 27-mai-2026 | GEO-Bench (manipulação de ranking) | Defesa |
| 2605.25517 | 25-mai-2026 | What Gets Cited (252k trials) | Técnica |
| 2605.21948 | 21-mai-2026 | SCI-Defense | Defesa |
| 2605.12887 | 13-mai-2026 | EcoGEO / TRACE (ecossistema de evidência) | Agêntico |
| 2605.09314 | 10-mai-2026 | How LLMs Are Persuaded (attention heads) | Defesa |
| 2604.27790 | 30-abr-2026 | How Generative AI Disrupts Search (11.500 queries) | Mercado |
| 2604.25707 | 28-abr-2026 | Citation Selection → Citation Absorption | Medição |
| 2604.19516 | 21-abr-2026 | MAGEO (multi-agente, skills por motor) | Agêntico |
| 2604.19113 | 21-abr-2026 | FeatGEO (otimização por features) | Técnica |
| 2604.07585 | 08-abr-2026 | Don't Measure Once | Medição |
| 2604.03656 | 04-abr-2026 | Beyond Retrieval (Deterministic Agent Handoff) | Agêntico |
| 2603.29979 | 31-mar-2026 | GEO-SFE (engenharia estrutural) | Técnica |
| 2603.09296 | 10-mar-2026 | AgentGEO (diagnóstico de falha de citação) | Técnica |
| 2603.12282 | 05-mar-2026 | Algorithmic Trust (UK iGaming) | Mercado |
| 2603.20213 | 02-mar-2026 | AgenticGEO (auto-evolutivo, MAP-Elites) | Agêntico |
| 2602.12187 | 12-fev-2026 | SAGEO Arena (avaliação realista) | Medição |
| 2602.02961 | 03-fev-2026 | GEO na Pinterest (VLM + agentes, produção) | Agêntico |
| 2601.16858 | 23-jan-2026 | Navigating the Shift (web search vs IA) | Mercado |
| 2601.13938 | 20-jan-2026 | IF-GEO (multi-query, fusão de instruções) | Técnica |
| 2601.12263 | 18-jan-2026 | MGEO (ataque multimodal a rankers VLM) | Defesa |
| 2601.00912 | 01-jan-2026 | The Discovery Gap (Product Hunt) | Mercado |
| 2601.00869 | 30-dez-2025 | Cultural Encoding / Existence Gap | Mercado |

Leituras obrigatórias por papel: **estrategista** → 2607.14035, 2606.20065, 2601.00912; **redator** → 2605.25517, 2603.29979, 2604.25707; **analista de dados** → 2604.07585, 2606.04362, 2602.12187; **engenheiro** → 2603.09296, 2604.19516, 2607.12056.

## 2. Ciência da medição: o protocolo que passa a valer

1. **Vetor de visibilidade em 4 camadas** (2607.14035): descobribilidade, citação, absorção, resultado econômico. Auditorias e reports decompõem o KPI nessas camadas; "visibilidade" sem qualificador fica proibido em documento técnico.
2. **Distribuição, não ponto** (2604.07585): toda métrica de resposta de IA é reportada com N execuções, janela temporal e variância. Mínimos operacionais desta casa: N≥5 execuções por prompt para monitoramento contínuo; N≥30 para comparação pré/pós intervenção. Repetibilidade (share de execuções em que a marca aparece) acima de ~70% indica presença forte; abaixo de ~30%, aparição oportunista [heurística de mercado atribuída a Maximus Labs em raw Perplexity truncado; proveniência fraca — usar como régua interna, nunca em contrato].
3. **Controle on-domain** (2606.04362): para medir efeito de intervenção, comparar páginas tratadas vs não tratadas do MESMO domínio no mesmo período; reportar a razão tratado/controle (no caso glasp: 5,7/3,5 ≈ 1,63x bruto) e, quando houver série temporal suficiente, o efeito de nível modelado (o 1,82x do paper vem de série temporal interrompida, não da divisão simples). O crescimento bruto embute o vento de cauda da plataforma (no caso glasp: 3,5x só de tailwind).
4. **Seleção vs absorção** (2604.25707): além de contar citações, verificar se a resposta usou conteúdo da página. Rubrica mínima executável: amostra mensal de 10 respostas citando o domínio; para cada uma, marcar sim/não em três eixos (a) linguagem: paráfrase direta de frase nossa; (b) fato: número/definição nosso presente na resposta; (c) estrutura: ordem de argumentos/passos espelhada; 2 avaliadores, divergência resolvida por terceiro. ChatGPT: menos citações, mais influência por citação; Perplexity/Google: mais citações, influência diluída.
5. **Sentimento como KPI separado** (2606.20065): flipa ~6,7x mais que menção; nunca compor num score único com menção sem declarar a volatilidade.
6. **Cuidado com "score GEO" sintético** (2601.00912): scores agregados de ferramenta não correlacionaram com descoberta real; o que correlacionou no Perplexity foi SEO tradicional. Score de vendor é termômetro interno, nunca promessa de resultado.
7. **AIO/AI Mode divergem do Google clássico e entre si** (2604.27790): Jaccard <0,2 entre fontes; sites que bloqueiam o crawler de IA do Google são significativamente menos recuperados em AIO. Atenção técnica: distinguir Googlebot (índice clássico; bloquear remove do Search) de Google-Extended (uso em IA) antes de qualquer recomendação de bloqueio; o abstract não especifica qual diretiva foi medida — ler o PDF antes de aconselhar cliente. Estratégia de fontes é por superfície.

## 3. Alavancas de conteúdo com evidência experimental (ordem de prioridade)

1. **Relevância temática e posição no contexto** — maiores drivers (2605.25517, 252k trials; confirma o survey).
2. **Evidência extraível** — definições citáveis, números com fonte, comparações, passos (2604.25707); é o que separa página absorvida de página apenas citada.
3. **Preço explícito e data recente/visível** — ajudam consistentemente (2605.25517). Regra editorial anexa: data recente só acompanha atualização substantiva registrada (changelog); trocar `dateModified` sem mudar conteúdo é exatamente a alegação temporal manipulativa que as defesas do §5 classificam como abuso.
4. **Estrutura em 3 níveis** — macro (arquitetura), meso (chunking), micro (ênfase): +17,3% de citação quando otimizada por arquitetura de motor (2603.29979).
5. **Perfil do documento inteiro, não micro-edição de frase** — otimização por features documento-nível supera reescrita token a token (2604.19113); otimizar para o PORTFÓLIO de queries que a página serve, não para um prompt (2601.13938).
6. **Presença em listicles de terceiros e YouTube** — ~21% de todas as citações são listicles "best-of"; YouTube lidera o não-owned (2606.20065; número do baseline Ranqo, segmentar por vertical/idioma antes de generalizar); em vertical regulado o viés por earned media é esmagador (2603.12282). Limite ético: earned media legítimo com disclosure; compra de posição em listicle sem identificação é a influência não divulgada que a agenda de governança (§5) mira.
7. **O que NÃO priorizar:** formatação pura (efeito pequeno, 2605.25517); "keywords persuasivas" e autoridade fabricada (detectáveis e filtráveis, 2605.21948/2605.09314); reescrita que sacrifica retrieval (técnicas GEO frequentemente degradam retrieval/rerank em condições realistas, 2602.12187).

## 4. Fronteira agêntica (executar e observar)

- **Diagnóstico automatizado** (2603.09296): taxonomia de falha por estágio + reparo mínimo dirigido. Modelo de serviço: +40% de citação mexendo em 5% do conteúdo.
- **Skills por motor** (2604.19516): preferências de Gemini/ChatGPT/Perplexity são estruturalmente diferentes (casa com Profound 6,8M citações, Wave Julho); manter biblioteca de estratégias validadas POR MOTOR, com teste de ramo gêmeo antes de rolar em produção.
- **Loop com crítico surrogate** (2603.20213): simular o motor com um crítico barato antes de gastar medição real; código aberto disponível (github.com/AIcling/agentic_geo).
- **Sites operáveis por agente** (2607.12056): interpretabilidade + executabilidade + confiabilidade de decisão; ganho medido de 49,3% → 89,3% de sucesso estrito de tarefas de agente. Combina com BrightEdge (agentes = 88% da atividade de busca humana; 95% do tráfego de agentes vem da OpenAI) e com o ecossistema de commerce agêntico (ACP/Instant Checkout; tese emergente "descobrir na IA, comprar no site").
- **Horizonte pós-citação** (2604.03656): "Deterministic Agent Handoff" — o LLM roteia a intenção para um agente proprietário que responde com dado canônico (alucinação próxima de zero no caso industrial EasyNote). Para a Brasil GEO: MCP/apps (ChatGPT Apps SDK, Conductor AgentStack) são a materialização comercial disso; entra no radar de produto.
- **Ecossistema, não página** (2605.12887): malha de páginas de suporte com terminologia e atributos consistentes influencia a trajetória do agente; é também o mapa do ataque — usar com disclosure.

## 5. Riscos, defesas e governança (o que muda o aconselhamento a cliente)

- Defesas propostas na literatura detectam manipulação semântica com precisão alta em benchmark fechado: autoridade fabricada, propositividade narrativa, comparativos e alegações temporais são os sinais classificados como manipulação (2605.21948, avaliado em 600 descrições de produto); prompting defensivo e checagem de evidência reduzem promoção nociva em experimento (2606.28356); a persuasão em si é circuito monitorável (2605.09314). Nada disso prova implementação pelos motores comerciais hoje — é a direção do vento, não o clima atual.
- Agenda de governança pede disclosure de influência comercial e auditoria black-box (2606.12439); captura informacional por GEO já é observada em zonas de conflito (2607.14197). Antecipar disclosure em contrato e metodologia é diferencial defensável.
- Dinâmica competitiva tem dilema social documentado em benchmark (2606.17443, cenário experimental de recomendação em skincare): quando todas as marcas adotam a mesma tática, o payoff experimental de recomendação colapsa (+0,802 → +0,007), e marcas não participantes deixaram de ser recomendadas naquele cenário. Tradução comercial honesta: táticas de copy comoditizam rápido; a vantagem durável vem de ativos difíceis de copiar (dados proprietários, earned media real, estrutura), não de truques de linguagem.
- Existence Gap (2601.00869): em respostas dependentes de memória paramétrica (sem retrieval web ativo), marca ausente do corpus de treino tende a não existir na resposta; a geografia dos dados de treino dirige o efeito (LLMs chineses +30,6 pp de menção). Com busca/RAG ativo a marca pode ser recuperada mesmo fora do treino — o gap vale para a camada paramétrica. Para clientes com ambição internacional, presença por ecossistema de LLM é KPI próprio.

## 6. Indústria: delta pós-14-jul e atualizações de régua

- **Ahrefs Brand Radar:** página oficial declara 406M+ prompts/mês (jul/2026); planos US$ 398 e US$ 699/mês. Atualiza o ~340M citado na metodologia de abril (atualização de número, não contradição). Estudo CTR atualizado (04-fev-2026, Ryan Law + Xibeijia Guan, GSC agregado, desktop): os **58%** são a redução atribuída à presença de AIO frente ao CTR esperado sem AIO no mesmo período (0,039 vs 0,016 em dez/2025); a queda bruta de dez/2023 (0,076) para dez/2025 com AIO (0,016) é ~79%, da qual parte é secular (o próprio CTR sem AIO caiu para 0,039). A queda por posição decresce até −19,4% na posição 10.
- **seoClarity:** declínio de citações externas do ChatGPT desde mar/2026 (menos respostas com citação e menos citações por resposta) + lançamento do LiveWire (jul/2026).
- **Conductor:** AgentStack (apps LLM nativos para ChatGPT, Claude e Copilot + servidor MCP) + parceria Optimizely; publica 2026 AEO/GEO Benchmarks Report.
- **Profound:** pós-Series C (US$ 96M, unicórnio, fev/2026 — já canônico na 15B): Profound Agents (500+ clientes diários, afirmação da empresa), Ask Profound (conversacional + Slack + MCP), integração Contentful, evento Zero Click New York (11-jun-2026, ~1.000 líderes); roadmap: Docs, Teams, Background Agents. Métrica da casa: 5M+ citações processadas/dia (afirmação da empresa, desenho amostral não publicado).
- **Semrush/Adobe:** integração revelada no Adobe Summit 2026 — Semrush no pilar brand visibility do Adobe CX Enterprise com AEM, LLM Optimizer, Commerce e Brand Concierge; Adobe: tráfego de IA para varejo +1.324% (out/2024 → mai/2026, telemetria própria).
- **Similarweb (07-mai-2026):** ChatGPT passou a exibir links de marca clicáveis na resposta → referrals +157,7% semana a semana, homepage +354,7%, share de referral na homepage ~60% (antes 26–32%); conversão do referral do ChatGPT 7,1% vs 7,8% do paid search (painel clickstream). Leitura prudente: evento recente de mudança de UI, pode ser transitório; a consequência operacional (homepage "answer-ready") vale como hipótese a validar por vertical, não como regra.
- **OpenAI:** ads no ChatGPT (teste anunciado 16-jan-2026, tiers Free/Go; visíveis desde 09-fev; self-serve EUA desde mai/2026 — timeline parcialmente secundária); Instant Checkout/ACP com PayPal e Shopify; expansão "Buy it in ChatGPT" (16-fev-2026). Tese emergente com dado de terceiros não confirmado na fonte: checkout in-chat estagnou; padrão vencedor é "descobrir na IA, comprar no site próprio" (Walmart ~3x pior conversão in-chat — NÃO citar sem verificar fonte primária).
- **Google:** relatório de performance de IA generativa no Search Console (03-jun-2026): relatório próprio que separa impressões de AI Overviews e AI Mode do relatório clássico, por página/país/dispositivo; ainda sem cliques, CTR ou queries; histórico desde 18-mai-2026; rollout gradual (relatos iniciais no Reino Unido), sem data global — já anunciado na Wave Julho §2.4, agora com datas e limitações confirmadas em fonte secundária múltipla. Números de I/O 2026 (1B usuários AI Mode; 2,5B AIO) seguem vendor-stated sem confirmação primária localizada: usar com rótulo.
- **Perplexity:** Comet gratuito mundial (out/2025); Comet Plus US$ 5/mês com pool de US$ 42,5M e split 80/20 pró-publisher (Wired, New Yorker, WaPo, Fortune); shopping agêntico gratuito nos EUA (fev/2026) [SECUNDÁRIO]. A tese "síntese da Perplexity privilegia conteúdo editorial de terceiros com autor e data" é observação de mercado [SECUNDÁRIO, sem métrica]; como fato mensurado temos apenas o padrão de mais citações por resposta (2604.25707) e a correlação com sinais SEO tradicionais e Reddit (2601.00912).
- **Kevin Indig (Growth Memo):** "ghost citations" — em ~62% das citações o domínio ganha link mas a marca não é nomeada; formato de query e tipo de conteúdo produzem até 30x mais menções; autoridade off-property é específica por tópico. Precisão conceitual: ghost citation é problema de MENÇÃO/atribuição (a marca não é nomeada), distinto de absorção (§2.4, o conteúdo é usado); uma página pode ter link sem menção e ainda assim alta absorção factual. Medir os três separadamente: citação, menção, absorção.
- **Pulso social (Grok, sem URLs — sinal direcional apenas):** ceticismo com llms.txt (Mike King, Aleyda Solis), consenso "medir só tráfego ficou obsoleto", share of voice em respostas de IA como métrica emergente (Kevin Indig, Profound), imprevisibilidade dos AIO (Barry Schwartz, Wil Reynolds). Nada canonizado sem fonte escrita.

## 7. Correções e conflitos (com prevalência declarada)

### 7.1. Atualizações de número (não são contradições)
- Brand Radar: ~340M prompts/mês (metodologia abr/2026, Wave Julho) → **406M+** (página oficial, jul/2026). Usar o número novo com data.
- AIO em ~48% das queries rastreadas pela BrightEdge (fev/2026) convive com a série da Semrush (~15,7% em nov/2025 sobre 10M keywords): são amostras e metodologias diferentes; citar sempre com a fonte e a base, nunca "AIO aparece em X% das buscas" sem qualificador.

### 7.2. Materiais desta wave com proveniência degradada (NÃO canônicos)
- Os três relatórios Perplexity `sonar-deep-research` desta coleta (raw/pplx-*.md) foram truncados no limite de 8.192 tokens e as notas numeradas ([1], [15] etc.) ficaram sem lista de URLs resolvida. Valem como corroboração e leitura de contexto; nenhum número exclusivo deles entra em copy sem confirmação independente. Os que entraram neste canônico foram confirmados por fonte nomeada nos relatórios dos subagentes web.
- Pulso social via Grok: sem URLs verificáveis; direcional apenas (registrado em §6).
- Dados marcados [SECUNDÁRIO] nos raws (ex.: Walmart 3x, números de I/O 2026, Microsoft Clarity 1,66%/0,15%): manter rótulo; não citar em material público sem achar a fonte primária.

### 7.3. Reafirmações
- Regra de conversão por vertical com faixa (Wave Julho §7.3) sai REFORÇADA. Regra mínima repetida aqui para leitura isolada deste arquivo: a faixa canonizada é **1,3x (e-commerce de baixo ticket) a 23x (B2B SaaS)**, sempre citada com vertical + fonte + período; proibido "IA converte 4–5x" como constante. O quadro desta wave corrobora: 4,4x (Semrush, multi-site), ~23x (Ahrefs, 1 site first-party), 7,1% absoluto (Similarweb, clickstream) — metodologias incomparáveis entre si.
- Nada da Wave Julho é revogado. A cadeia de precedência passa a ser **Julho-22 §7 > Julho §7 > Wave 19 §7 > 15B §8**.

### 7.4. Precedência epistemológica DENTRO da wave (nova regra)
Conflito entre fontes da mesma wave resolve-se por esta escala, da mais forte para a mais fraca: (1) experimento acadêmico controlado com protocolo publicado; (2) documento primário de empresa (press release, docs oficiais, blog assinado); (3) telemetria de vendor com metodologia declarada; (4) telemetria de vendor sem metodologia; (5) agregador/imprensa secundária; (6) relatório de LLM com fontes não resolvidas; (7) pulso social. Fontes dos níveis 6 e 7 nunca canonizam número sozinhas.

## 8. Aplicação por repositório

### 8.1. `papers` (pesquisa acadêmica)
- **Literatura pronta:** a lista-mestre do §1 é a revisão de literatura viva dos 4 papers em produção; 2606.20065 (Ranqo) e 2604.25707 (geo-citation-lab) são os comparáveis diretos do nosso desenho (cohort de 5 LLMs, 127 entidades). Citar o survey 2607.14035 no related work de todos.
- **METHODOLOGY_V2:** incorporar formalmente (a) visibilidade como distribuição com N execuções e IC (2604.07585); (b) vetor de 4 camadas como variáveis dependentes distintas; (c) discutir controle on-domain (2606.04362) como padrão-ouro de causalidade que nosso desenho observacional não alcança — limitação declarada e agenda futura.
- **Oportunidade de contribuição:** nenhum dos 32 papers coletados nas 3 queries cobre mercado brasileiro/língua portuguesa (escopo: arXiv apenas; bases fora do arXiv não foram varridas nesta wave); nosso dataset de 127 entidades BR segue como lacuna publicável (conversa com Existence Gap 2601.00869).
- **Anti-GhostCite:** os 33 IDs deste doc foram verificados via API em 22-jul-2026; qualquer citação futura reabre o `abs` antes de canonizar.

### 8.2. `landing-page-geo` (site alexandrecaramaschi.com)
- **MEASUREMENT_ARCHITECTURE:** evoluir o funil de medição para as 4 camadas (descobribilidade, citação, absorção, resultado); nos 25 prompts canônicos (docs/geo/llm-mention-rate-canonical-25-prompts.md), registrar N≥5 execuções por prompt com variância e repetibilidade, e rodar a rubrica mensal de absorção do §2.4.
- **Redação e páginas:** aplicar §3 nas páginas comerciais e educacionais: evidência extraível por página, data visível, estrutura macro/meso/micro; homepage "answer-ready" (Similarweb: referral de IA agora cai ~60% na homepage).
- **Auditoria (produto):** incluir camada agent-ready (§4) no checklist técnico; desenho de serviço "diagnóstico antes de reescrita" (§4, item diagnóstico automatizado/AgentGEO) como proposta de valor.
- **Copy comercial:** o argumento honesto ganha músculo: survey diz que promessa inflada não tem base causal; nosso diferencial é medição com controle e diagnóstico por camada. Usar 2601.00912 (SEO primeiro) ao lado do 81%/36%.

### 8.3. `curso-factory` (fábrica de cursos)
- **Aulas candidatas novas (spine):** "Medição como distribuição" (2604.07585 + 2606.04362), "Seleção vs absorção de citação" (2604.25707), "Diagnóstico antes de reescrita" (2603.09296), "Sites agent-ready" (2607.12056), "Defesas dos motores e GEO ético" (2605.21948/2605.09314).
- **Prompts do pipeline:** `research.md` passa a exigir arXiv ID verificado para claim acadêmico; o Checklist de Citabilidade GEO em `draft.md` ganha os itens do §3 (evidência extraível, preço/data explícitos, estrutura 3 níveis, portfólio de queries).
- **Gates:** `content_checker.py` (bloco `geo_2026` do client.yaml): considerar contadores para "definição citável" e "data visível" além de Cite Sources/Statistics/Quotation; `reviewer.py` pune autoridade fabricada e comparativo sem fonte (alinha com SCI-Defense).
- **Corrigir ponteiro obsoleto no CLAUDE.md:** a linha que referencia `docs/knowledge/geo-aeo/` aponta para pasta inexistente; substituir pela trilha de waves.

---

### Glossário mínimo (escopos que agentes não devem misturar)
**GEO**: otimizar para ser recuperado, citado e absorvido por motores generativos (termo guarda-chuva desta casa). **AEO**: rótulo de mercado equivalente, com ênfase em answer engines. **AIO**: AI Overviews do Google (resumo sobre a SERP). **AI Mode**: experiência conversacional de busca do Google (superfície distinta da AIO). **Agent-ready**: site operável por browser-agents (tarefas, não citações). **Answer-ready**: página estruturada para responder na própria superfície de IA. Superfícies distintas exigem estratégia e medição distintas (§2.7).

### Apêndice · método desta wave (reaplicável)

1. Reconhecimento: API do arXiv (3 queries; XMLs preservados em `raw/`) + mapeamento dos 3 repos. Queries exatas (export.arxiv.org/api/query, sortBy=submittedDate, desc): (q1) `all:"generative engine optimization"`, max_results=30; (q2) `all:"answer engine optimization"`, max_results=10; (q3) `all:"AI search" AND all:"brand visibility"`, max_results=10. q1 reportou totalResults=35; os 30 mais recentes foram capturados (5 mais antigos que dez/2025 ficaram fora).
2. Fan-out: 3 × Perplexity `sonar-deep-research` (plataformas, dados de mercado, KPIs) + Grok live search (pulso social) + 2 subagentes web com verificação de fonte primária e rótulo [CONFIRMADO]/[SECUNDÁRIO] + 1 subagente de digest arXiv com regra de proveniência estrita.
3. Síntese única com precedência declarada; crítica por conselho de LLMs antes do commit. Registro: GPT-5.5 entregou 65 pontos de crítica (raw em `raw/critica-gpt.md`; os de correção factual e rotulagem foram aplicados; os de expansão de protocolo viraram backlog); Gemini indisponível nesta rodada (HTTP 429, créditos prepagos esgotados); a ponta Anthropic é a própria síntese (Claude Fable 5, Claude Code).
4. Lições operacionais registradas: `sonar-deep-research` trunca em 8.192 tokens e perde a lista de referências — pedir relatórios mais curtos por tema ou usar `sonar-pro` em fatias; Grok recusa períodos futuros ("2026" no prompt) — formular "mais recentes disponíveis"; redirecionamento de shell precisa de caminho absoluto (falha silenciosa em `/`).

### Referências principais (verificadas nesta wave)
- arXiv: os 33 IDs do §1 (abs verificados em 22-jul-2026).
- ahrefs.com/blog/ai-overviews-reduce-clicks-update/ (04-fev-2026) · ahrefs.com/brand-radar (jul/2026) · blog.timsoulo.com/geo-tool-market-analysis-47-vendors-one-commodity-and-the-data-problem/ (05-mar-2026) · ahrefs.com/blog/ai-brand-visibility-correlations/ · ahrefs.com/blog/chatgpts-most-cited-pages/
- semrush.com/news/463141 (26-jun-2026) · news.adobe.com/news/2026/04/adobe-completes-semrush-acquisition (28-abr-2026) · experienceleague.adobe.com/en/docs/llm-optimizer/using/home
- seoclarity.net/chatgpt-citation-decline-analysis (mar/2026) · seoclarity.net/resources/news/seoclarity-launches-livewire-seo-and-aeo-intelligence (jul/2026) · conductor.com/academy/aeo-geo-benchmarks-report/
- similarweb.com/blog/insights/ai-news/chatgpt-referral-traffic-triples/ (mai/2026) · similarweb.com/blog/marketing/geo/gen-ai-stats/ (28-mai-2026)
- brightedge.com/news/press-releases/brightedge-data-ai-search-reaching-tipping-point-ai-agents-2026 (08-abr-2026)
- tryprofound.com/blog/profound-raises-96m-series-c (24-fev-2026) · tryprofound.com/blog/profound-2026 · lsvp.com/company/profound/
- growth-memo.com/p/the-ghost-citation-problem · growth-memo.com/p/2026-growth-memo-research-summary · ipullrank.com/ai-search-manual (mai/2026)
- ppc.land/llms-txt-adoption-rises-8-8x-but-97-of-files-get-zero-ai-requests/ · searchenginejournal.com/googles-says-its-fine-to-use-llms-txt-for-ai-seo/579608/ (jun/2026)
- pewresearch.org/short-reads/2025/07/22/google-users-are-less-likely-to-click-on-links-when-an-ai-summary-appears-in-the-results/
- cmswire.com/digital-experience/google-adds-ai-visibility-reports-to-search-console/ (jun/2026) · stripe.com/newsroom/news/stripe-openai-instant-checkout
