
================================================================
ESCALONAMENTO CLOUD SUGERIDO (precisa da sua permissão)
----------------------------------------------------------------
  Motivos     : --provider explicito
  Modelo cloud: OpenAI · GPT-5.5
  Por que     : provider forcado pelo usuario (--provider openai)
  Custo est.  : ~$0.0504 USD (estimativa)
  Via         : API direta
================================================================
Permissão: auto-aprovada (--yes)
1. **§1 — Contagem do corpus está errada: “33 papers” não fecha.**  
   A tabela lista 33 linhas apenas porque `2606.04362` aparece duas vezes, sendo a última marcada como duplicata. Isso produz **32 IDs únicos**, não 33 papers. O §0 afirma “33 papers relevantes no arXiv” e “32 de 2026, 1 de dez/2025”; com a duplicata, essa contagem é inconsistente. Corrigir para “32 papers únicos” ou substituir a duplicata pelo paper faltante.

2. **§1 — A duplicata `2606.04362*` é tratada como paper, mas tem eixo “—”.**  
   Se a intenção era documentar que o mesmo paper apareceu em outra query, isso deve ir em nota metodológica, não na tabela de corpus. Do jeito atual, infla artificialmente o total e quebra qualquer uso automático da tabela por agentes.

3. **§0 e §1 — “1 de dez/2025” conflita com o ID `2601.00869`.**  
   Um identificador `2601.xxxxx` indica submissão arXiv em jan/2026, não “30-dez-2025” como aparece no §1. Pode haver versão anterior, preprint externo ou data de escrita, mas não é isso que a tabela diz. A linha `2601.00869 | 30-dez-2025` precisa ser explicada ou corrigida.

4. **§1 — Datas incompatíveis com o mês do arXiv ID.**  
   `2606.12439` está datado como **18-mai-2026**, mas o ID é de junho/2026. Isso é erro factual ou mistura de data de versão, data de publicação externa e data arXiv. Para documento canônico, cada coluna precisa distinguir: `submitted`, `announced`, `v1`, `latest version`, `published elsewhere`.

5. **§1 — Várias datas parecem incompatíveis com a ordenação sequencial dos IDs arXiv.**  
   Exemplos: `2606.28356` datado como 08-jun-2026 é improvável para um ID tão alto no mês; `2603.20213` aparece como 02-mar-2026, enquanto `2603.09296` aparece como 10-mar-2026. A sequência de IDs arXiv dentro do mês é aproximadamente cronológica. Isso sugere erro de extração ou de digitação.

6. **§0, §1 e §8.1 — “todos verificados por ID via API” é insuficiente.**  
   Verificar que um ID existe não verifica que ele é relevante para GEO, nem que os números citados no documento estão no abstract. O texto afirma que “os resumos derivam exclusivamente dos abstracts reais”, mas o documento usa métricas detalhadas — 252.000 trials, 21.143 citações, 72 features, 100k+ respostas, IC 95%, p=0,16 — que podem não estar no abstract. Precisa separar: “existência verificada”, “abstract verificado”, “PDF lido”, “número extraído do PDF”.

7. **§0 — O cálculo glasp.co parece inconsistente: 5,7x / 3,5x não dá 1,82x.**  
   O texto diz: tratadas cresceram 5,7x, controle 3,5x, efeito líquido 1,82x. A razão simples é **1,63x**. Se 1,82x vem de modelo estatístico, diferença-em-diferenças logarítmica ou ajuste por covariáveis, isso precisa ser explicitado. Do jeito atual, parece erro aritmético.

8. **§2.3 — O mesmo problema do glasp.co é repetido sem explicação.**  
   “Reportar razão tratado/controle” levaria o leitor a calcular 5,7 / 3,5 = 1,63, mas o §0 canoniza 1,82. Há contradição metodológica entre a regra operacional e o número apresentado.

9. **§6 — Cálculo de CTR da Ahrefs está numericamente errado ou mal explicado.**  
   O texto diz: “CTR da posição 1 com AIO caiu 58% (0,076 dez/2023 → 0,016 dez/2025 com AIO)”. A queda de 0,076 para 0,016 é cerca de **79%**, não 58%. Talvez 58% compare 0,039 sem AIO contra 0,016 com AIO; se for isso, a redação está errada.

10. **§0 — “Primeiro survey crítico do campo” é uma afirmação forte sem prova.**  
    O documento afirma que `arXiv:2607.14035` é “o primeiro survey crítico do campo”. Isso exige busca bibliográfica ampla fora do próprio corpus, não apenas coleta arXiv. Deve receber rótulo: **[alegação dos autores]**, **[não verificado fora do arXiv]** ou ser removido.

11. **§0 — “Nenhuma técnica revisada demonstra efeito causal estável, longitudinal e cross-plataforma” é forte demais sem citação textual.**  
    Essa frase pode ser conclusão dos autores do survey, interpretação do revisor ou extrapolação. Como ela vira “antídoto canônico” e base de contratos, precisa de citação literal, página/trecho do PDF e escopo: quais técnicas, quais plataformas, qual definição de causalidade.

12. **§0 e §5 — SCI-Defense com “Precision 1,000/FPR 0,000” deve ser tratado como resultado de benchmark fechado, não como verdade operacional.**  
    Precisão perfeita e falso positivo zero são sinais de possível avaliação em dataset limitado/sintético. O documento transforma isso em “motores estão erguendo defesas” e “já detectam esses padrões”. Um paper propor uma defesa não significa que ChatGPT, Google, Perplexity ou Claude a implementaram.

13. **§5 — “Punidos” é linguagem indevida.**  
    O texto diz que certos sinais “são punidos”. Um detector acadêmico detectar manipulação não implica punição em ranking, citação ou geração. Trocar por “foram classificados como manipulativos no benchmark X” ou provar mecanismo de punição em motores reais.

14. **§0 e §4 — BrightEdge é usado como fato de mercado sem rótulo vendor-stated.**  
    “Agentes de IA = 88% da atividade de busca humana”, “~15% do tráfego dos sites”, “95% disso da OpenAI” vêm de press release/vendor data. O §0 trata como fato canônico. Precisa de rótulo **[vendor-stated; metodologia não auditada]** e definição de “atividade de busca humana”.

15. **§6 — Profound é citado com números autopromocionais sem isolamento claro.**  
    “500+ clientes diários”, “5M+ citações processadas/dia”, “unicórnio” e roadmap são claims de empresa/investidor. O texto até diz “afirmação da empresa” em uma parte, mas mistura com fatos de mercado. Para agentes, cada número precisa carregar `source_type: vendor_claim`.

16. **§6 — OpenAI ads/checkout contém timeline parcialmente secundária, mas está no corpo canônico.**  
    O próprio texto diz “timeline parcialmente secundária” e “tese emergente com dado de terceiros não confirmado”. Isso não deveria estar em §6 como atualização de régua sem rótulos por frase. Mover para §7.2 ou marcar explicitamente cada claim como **[SECUNDÁRIO]**, **[NÃO USAR EM COPY]**.

17. **§7.2 — Contradição de governança: materiais “não canônicos” alimentam o canônico.**  
    O §7.2 diz que relatórios Perplexity truncados e Grok sem URLs “não são canônicos”. Mas o §0 declara o método como “orquestrador multi-LLM” e o §6 inclui “Pulso social (Grok)” e vários sinais de mercado não primários. A política precisa dizer exatamente quais claims derivados desses materiais entraram, quais foram confirmados e onde está a confirmação.

18. **§2.2 — Limiares de 70% e 30% são fracos de proveniência.**  
    “Repetibilidade acima de ~70% indica presença forte; abaixo de ~30%, aparição oportunista” vem de “Maximus Labs, raw Perplexity”, mas Maximus Labs não aparece nas referências principais. Isso é métrica operacional crítica; não pode depender de raw truncado ou fonte não listada. Precisa de rótulo **[heurística interna]** ou validação.

19. **§2.4 — “Amostragem manual mensal já basta” é operacionalmente inexequível.**  
    Falta definir tamanho da amostra, critérios de seleção, rubrica de absorção, escala de julgamento, número de avaliadores, desempate, inter-rater agreement, exemplos positivos/negativos e tratamento de paráfrase. Um agente não consegue executar “verificar se usou linguagem/fato/estrutura” de forma consistente.

20. **§2.1 — O vetor de visibilidade é nomeado, mas não formalizado.**  
    “Descobribilidade, citação, absorção, resultado econômico” precisa de definição computável. Exemplo: descobribilidade é presença no contexto recuperado? presença na resposta sem link? posição entre alternativas? citação é link, domínio, URL canônica ou menção textual? absorção é overlap semântico, factual ou estrutural? resultado econômico é sessão, lead, receita assistida ou atribuição last-click?

21. **§2.7 — “Bloquear o crawler de IA do Google” é tecnicamente ambíguo e perigoso.**  
    O texto não identifica qual crawler: Googlebot, Google-Extended, APIs específicas, crawlers de Search, AIO, AI Mode. Isso é crítico porque bloquear Googlebot pode remover páginas do índice clássico; Google-Extended historicamente não controla Search. A recomendação precisa de granularidade técnica e fonte primária.

22. **§3.1 — “Relevância temática e posição no contexto” não vira ação executável.**  
    Site owners não controlam diretamente a “posição no contexto” do LLM. O documento precisa traduzir isso em ações: arquitetura de informação, headings, ordem de evidências no chunk, internal linking, canonicalização, snippets, schema, sitemaps, entidades, páginas hub/spoke. Sem isso, é diagnóstico abstrato.

23. **§3.3 — “Data recente/visível” incentiva freshness spam se não houver regra editorial.**  
    Falta política: quando atualizar `dateModified`, como registrar mudanças substantivas, como exibir histórico, como evitar trocar data sem alterar conteúdo. Isso colide com §5, que condena alegações temporais manipulativas.

24. **§3.4 — “Estrutura em 3 níveis” é vaga demais.**  
    Macro/meso/microestrutura são termos úteis, mas sem checklist. Falta: número/tamanho de chunks, hierarquia H1-H3, blocos FAQ, tabelas comparativas, bullets, densidade de claims, localização de definição, presença de resumo, schema, exemplos e limites de over-optimization.

25. **§3.6 — Recomendação de priorizar listicles de terceiros é eticamente e operacionalmente incompleta.**  
    “Prioridade nº 1 é presença em listicles” pode virar compra de rankings, afiliados sem disclosure e manipulação editorial. Falta política de disclosure, critérios de qualidade, separação earned/paid/affiliate e risco de conflito regulatório.

26. **§3.6 e §0 — Generalização indevida dos “~21% de citações em listicles”.**  
    O número parece vir de um baseline específico da Ranqo. O documento generaliza para “fora do tier 1, prioridade nº 1”. Precisa segmentar por vertical, idioma, país, tipo de query e motor. Em B2B técnico, saúde, jurídico ou governo, listicles podem não ter o mesmo peso.

27. **§4 — “Biblioteca de estratégias validadas por motor” não tem formato.**  
    Falta especificar como uma estratégia entra/sai da biblioteca: hipótese, motor, superfície, vertical, métrica, baseline, N execuções, janela, critério de sucesso, validade temporal, rollback. “Teste de ramo gêmeo” também não é definido.

28. **§4 — “Crítico surrogate” pode induzir overfitting, mas o risco não é tratado.**  
    Simular um motor com modelo barato é útil apenas se calibrado contra medições reais. Falta protocolo de calibração, frequência de revalidação, métrica de divergência e regra para não otimizar contra o simulador.

29. **§4 — “Sites operáveis por agente” é conceitual, não auditável.**  
    Interpretabilidade, executabilidade e confiabilidade de decisão não têm testes. Um checklist agent-ready deveria incluir: login, formulários, carrinho, busca interna, filtros, APIs, schema/action markup, erros, CAPTCHAs, consentimento, acessibilidade, políticas, rastreabilidade de preço/estoque, fallback humano e logs de agente.

30. **§4 — “Alucinação próxima de zero no caso industrial EasyNote” é claim anedótico.**  
    Não há referência na lista principal para EasyNote nem descrição do caso. “Próxima de zero” exige métrica, baseline e escopo. Marcar como **[case vendor/industrial não auditado]** ou remover.

31. **§5 — A conclusão comercial “entrada cedo importa” não decorre claramente do dado apresentado.**  
    O texto diz que quando todos usam a mesma tática o payoff colapsa de +0,802 para +0,007. Isso sugere comoditização, não necessariamente vantagem de entrada. A inferência “entrada cedo importa” precisa de modelo temporal, evidência de lock-in ou ativos cumulativos.

32. **§5 — “Quem fica fora recebe zero” é absoluto demais.**  
    Receber zero em qual métrica? Citação? payoff experimental? share of voice? tráfego? Sem unidade, o número vira slogan. Precisa de métrica, cenário experimental e limitação.

33. **§5 — “Marca ausente do corpus de treino não existe na resposta” é falso como regra geral.**  
    Motores com busca/RAG podem recuperar marcas que não estavam no treino. A frase deve ser qualificada: “em modelos sem recuperação web ou em tarefas dependentes de memória paramétrica”. Do jeito atual, conflita com todo o documento, que trata retrieval, citações e fontes web como centrais.

34. **§6 — “Similarweb: homepage volta a ser superfície de conversão de IA” extrapola de um evento específico.**  
    O aumento de referrals após links clicáveis no ChatGPT pode ser transitório, dependente de UI, categoria e base Similarweb. Transformar isso em regra para homepage exige validação por vertical e por cliente.

35. **§6 — “Perplexity privilegia conteúdo editorial de terceiros com autor e data” está sem evidência operacional.**  
    Isso pode ser observação de mercado, mas precisa de métrica: aumento relativo, corpus, vertical, período, comparação com owned media. Caso contrário, vira recomendação editorial sem base.

36. **§6 — “Ghost citations” conecta diretamente com absorção, mas o conceito está mal posicionado.**  
    Ghost citation — domínio linkado sem marca nomeada — é problema de menção/atribuição, não necessariamente absorção. Absorção é uso de conteúdo na resposta. Um link sem menção pode ainda ter alta absorção factual. A conexão com §2.4 precisa ser reescrita.

37. **§6 e §7.1 — Uso inconsistente de “não contradição”.**  
    O documento declara que Brand Radar 340M → 406M é “atualização, não contradição”, mas não aplica o mesmo rigor a outros números temporais. Ex.: CTR Ahrefs, BrightEdge, Similarweb, Adobe, Profound e Google I/O aparecem em bases diferentes sem quadro de comparabilidade.

38. **§6 — “Google Search Console: impressões de AIO/AI Mode separadas, SEM cliques/CTR/queries” tem erro de clareza.**  
    “SEM” parece caixa alta acidental de “sem”. Além disso, “impressões separadas” precisa dizer separadas de quê: relatório próprio? filtro? dimensão? exportável via API? visível por URL? por query? O texto é insuficiente para implementação.

39. **§7.3 — “Regra de conversão por vertical com faixa” é referenciada, mas a faixa não está neste documento.**  
    Como esta wave é delta e não substitui a anterior, ainda assim agentes que leem este arquivo isoladamente não conseguem aplicar a regra. Repetir a regra mínima ou linkar seção/arquivo exato.

40. **§8.1 — “Cohort de 5 LLMs, 127 entidades” surge sem descrição.**  
    O documento menciona dataset próprio como se o leitor já soubesse. Falta especificar quais LLMs, quais entidades, critérios de seleção, idioma, prompts, período e desenho observacional. Para paper, isso é essencial.

41. **§8.1 — “Nenhum dos 33 papers cobre mercado brasileiro/língua portuguesa” é afirmação bibliográfica forte.**  
    Com a própria contagem do corpus inconsistente, essa conclusão é frágil. Precisa demonstrar query strategy, termos em português/inglês, bases fora do arXiv, exclusões e possibilidade de trabalhos não arXiv.

42. **§8.2 — “25 prompts canônicos” é insuficiente para medição robusta.**  
    O documento exige distribuição, variância e controle, mas em seguida propõe “amostragem mensal de absorção nos 25 prompts canônicos” sem N execuções por prompt, randomização, prompts alternativos, temperatura/modelo, localização, personalização, janela horária ou critérios de atualização.

43. **§8.2 — Referência quebrada: “§3.7/AgentGEO”.**  
    O §3.7 é “O que NÃO priorizar”; AgentGEO está no §4. Isso criará erro para agentes que resolvem ponteiros internos. Corrigir para “§4, bullet Diagnóstico automatizado” ou criar subseção própria.

44. **§8.3 — Requisitos para `content_checker.py` são vagos para implementação.**  
    “Considerar contadores para definição citável e data visível” não especifica como detectar definição, que regex/schema usar para data, quais thresholds aprovar/reprovar, como lidar com páginas sem preço, como evitar falso positivo e como reportar.

45. **§8.3 — `reviewer.py` “pune autoridade fabricada e comparativo sem fonte” precisa de regras formais.**  
    Um agente precisa saber o que conta como autoridade fabricada: logos? “líder”, “melhor”, “especialista”, “nº 1”, anos de experiência, clientes? Comparativo sem fonte: qualquer “mais rápido”, “melhor”, “maior”? Falta taxonomia e severidade.

46. **Apêndice — Método não é reprodutível.**  
    “API do arXiv (3 queries com controle)” não informa query strings, campos pesquisados, `max_results`, ordenação, timestamps UTC, filtros, deduplicação, critérios de inclusão/exclusão. Sem isso, não há reexecução possível.

47. **Apêndice — “Conselho GPT + Gemini + Claude” é validação opaca.**  
    Usar LLMs como revisão crítica pode ser útil, mas precisa registrar prompts, modelos, versões, datas, outputs e decisões aceitas/rejeitadas. Caso contrário, é apenas argumento de autoridade automatizado.

48. **Apêndice e §7.2 — O problema de truncamento do Perplexity deveria invalidar a etapa para claims factuais.**  
    Se as listas de URLs foram perdidas, os relatórios não deveriam contar sequer como corroboração factual. O documento precisa distinguir “insight para investigar” de “corroboração”.

49. **Documento inteiro — GEO e AEO são usados como quase sinônimos sem definição.**  
    §0 fala GEO, AEO, AI Mode, AIO, agent-ready, answer-ready, LLM Optimization. Falta glossário operacional: GEO vs AEO vs AIO optimization vs agent-ready vs LLMO. Agentes vão misturar escopos.

50. **Documento inteiro — Falta taxonomia por superfície.**  
    Um documento estado-da-arte deveria separar explicitamente: ChatGPT com browsing/search, ChatGPT sem browsing, Google AIO, Google AI Mode, Perplexity, Gemini, Copilot, Claude, AI shopping agents, browser agents, MCP/apps. Hoje o texto mistura motores conversacionais, SERP generativa, agentes e dashboards.

51. **Documento inteiro — Falta protocolo mínimo de medição.**  
    O texto diz “N execuções”, mas não define N recomendado por caso: monitoramento, pré/pós, teste A/B, diagnóstico por prompt, relatório executivo. Falta power analysis, intervalo de confiança, bootstrap/binomial, correção para múltiplos prompts e estabilidade temporal.

52. **Documento inteiro — Falta controle de variáveis de execução.**  
    Não há padrão para: modelo/versão, temperatura, conta logada/deslogada, histórico limpo, localização, idioma, device, horário, personalization, plano pago/free, uso de browsing, cache, SERP freshness, prompt variants e retry policy. Sem isso, “distribuição” vira ruído não controlado.

53. **Documento inteiro — Falta definição de atribuição econômica.**  
    A quarta camada “resultado econômico” aparece, mas não há modelo de atribuição: referral direto, dark traffic, assisted conversion, brand lift, incrementality, MMM, holdout, códigos/campanhas, server-side analytics, consent mode, CRM. Isso é lacuna grave para GEO comercial.

54. **Documento inteiro — Falta integração com logs técnicos.**  
    Um GEO moderno deveria cruzar respostas de IA com server logs, bots/crawlers, user agents, referrers, cache, CDN, robots, sitemap, indexação, status codes, renderização JS e acesso a assets. O texto fica excessivamente em prompts e citações.

55. **Documento inteiro — Falta política de robots/opt-out/licenciamento.**  
    Há menção a llms.txt, mas não há matriz para `robots.txt`, `Google-Extended`, `GPTBot`, `CCBot`, `PerplexityBot`, `ClaudeBot`, paywalls, licensing, publisher deals e trade-off entre visibilidade e proteção de conteúdo.

56. **Documento inteiro — Falta segurança agêntica.**  
    “Agent-ready” sem tratar prompt injection, tool injection, malicious instructions em páginas, data exfiltration, consentimento de ações, autenticação, confirmação de compra, rollback e auditoria é incompleto para 2026.

57. **Documento inteiro — Falta camada legal/regulatória brasileira.**  
    Para um documento Brasil GEO, faltam LGPD, direito autoral, publicidade identificável, CONAR, CDC, setores regulados, uso de dados pessoais em prompts, scraping, logs e consentimento. O §5 fala governança genericamente, mas não operacionaliza.

58. **Documento inteiro — Falta tratamento de língua portuguesa e variação regional.**  
    O texto afirma lacuna brasileira, mas não define como GEO muda em PT-BR: entidades locais, fontes brasileiras, português/inglês, geolocalização, mídia local, domínios `.br`, dados estruturados, queries híbridas e diferença entre motores no Brasil.

59. **Documento inteiro — Falta matriz de qualidade de fonte.**  
    O texto recomenda evidência, números e fontes, mas não define níveis de fonte: primária, regulatória, acadêmica, vendor, mídia, newsletter, social, raw LLM. Sem essa matriz, o próprio documento cai em mistura de proveniência.

60. **Documento inteiro — Falta formato machine-readable para agentes.**  
    Como o arquivo será lido por agentes como premissa de trabalho, deveria conter tabelas normalizadas ou YAML/JSON para: claims, fonte, confiança, validade temporal, seção, ação operacional, métrica, owner, status canônico. Hoje há muita prosa ambígua.

61. **Documento inteiro — Falta data de validade por claim.**  
    Em GEO, números de citações, UI, tráfego e políticas mudam semanalmente. O documento só tem data da wave. Cada claim operacional deveria ter `valid_from`, `review_by` e `staleness risk`.

62. **Documento inteiro — Falta distinção entre evidência acadêmica, benchmark sintético e evidência em produção.**  
    Papers com trials controlados, vendor telemetry, newsletters e cases são tratados lado a lado. Um documento canônico precisa classificar força de evidência e risco de generalização.

63. **Documento inteiro — Falta regra para conflitos entre fontes dentro da própria wave.**  
    Há precedência entre waves, mas não entre tipos de fonte desta wave. Exemplo: se paper contradiz vendor report, quem vence? Se fonte primária empresarial contradiz newsletter, quem vence? A regra de precedência atual só resolve conflito histórico, não epistemológico.

64. **Documento inteiro — Problema de clareza temporal.**  
    Mistura “jul/2026”, “mar/2026”, “out/2025”, “dez/2025”, “I/O 2026”, “desde mar/2026” sem separar evento, coleta, publicação e atualização. Para agentes, isso causa uso de número vencido como atual.

65. **Documento inteiro — Há excesso de slogans normativos sem condições de aplicação.**  
    Exemplos: “GEO = camada sobre SEO sólido”, “diagnóstico antes de reescrita”, “homepage answer-ready”, “ecossistema, não página”, “linha ética com fundamento técnico”. Todos precisam de critérios de decisão: quando aplicar, quando não aplicar, pré-requisitos, custo, risco e métrica de sucesso.
