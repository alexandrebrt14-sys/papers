# Três maneiras de falhar em concluir: o que aprendemos reconstruindo do zero um estudo sobre como LLMs citam empresas brasileiras

**Por Alexandre Caramaschi — CEO da Brasil GEO · 23 de abril de 2026**

*Tempo de leitura: ~12 min*

---

## Por que este texto existe

Em abril de 2026, submeti um paper chamado **"Null-Triad: Three Ways to Fail to Conclude"** ao SSRN e depositei o pré-print no Zenodo sob DOI [10.5281/zenodo.19712217](https://doi.org/10.5281/zenodo.19712217). Ele não foi escrito para celebrar um resultado. Foi escrito para documentar — com honestidade metodológica — **três falhas simultâneas** que tornaram meu próprio estudo longitudinal sobre como ChatGPT, Claude, Gemini, Perplexity e Groq citam empresas brasileiras inconclusivo.

Este artigo é sobre o que veio depois: o reboot metodológico inteiro que executei nas últimas 72 horas antes de iniciar uma nova janela de coleta de 90 dias corridos. É um relato técnico, mas que importa para qualquer pessoa que esteja pesquisando sistemas generativos no mundo real — porque as três falhas que cometi são falhas que a maior parte dos estudos sobre LLMs comete em silêncio.

## O que o Paper 4 diagnosticou

O paper original testava quatro hipóteses sobre comportamento de citação em quatro verticais (fintech, varejo, saúde, tecnologia) através de 7.052 queries coletadas em cinco LLMs ao longo de ~40 dias. Quando abri a caixa preta das inferências, encontrei um padrão incômodo:

**H1 — RAG cita mais do que modelos paramétricos?** O efeito estimado apontava na direção correta, mas o intervalo de confiança cruzava o zero. O *n* por célula era pequeno demais, e os erros-padrão naïve não respeitavam a estrutura de cluster (cada dia de coleta é um cluster que compartilha o mesmo estado do modelo). **Subpotência.**

**H2 — LLMs alucinam entidades inexistentes?** O design previa injetar oito "decoys" fictícias (nomes plausíveis de empresas que não existem) na *coorte*, esperando que a taxa de menção dessas entidades em respostas fosse zero. O problema é sutil: o estudo contava apenas *probes passivos* — as fictícias apareciam na coorte, mas nunca em queries que *forçassem* menção. Resultado: zero hits, mas sem poder para distinguir "o modelo é bom em não alucinar" de "o modelo nunca foi desafiado". **Desenho nulo.**

**H3 — Diferentes LLMs convergem ou divergem em que entidades citam?** O estudo usava um threshold de Jaccard de 0.30 como critério de "concordância baixa". Esse 0.30 era arbitrário. Pior: a extração de entidades usava correspondência por substring, que contamina positivamente o score (Inter dentro de *international*, Stone dentro de *keystone*, Itaú reconhecido diferente de Itau sem acento). **Instrumentação assimétrica.**

Um único modo de falha seria um revés. Três simultâneos são um diagnóstico: **o pipeline inteiro precisa ser reconstruído antes de qualquer afirmação sobre o comportamento desses modelos ser cientificamente defensável**.

## O reboot — doze pilares metodológicos

Entre 21 e 23 de abril executei seis ondas de reimplementação no repositório [alexandrebrt14-sys/papers](https://github.com/alexandrebrt14-sys/papers). O resultado é a versão 2.x do pipeline, documentada no [CHANGELOG](https://github.com/alexandrebrt14-sys/papers/blob/main/CHANGELOG.md) e formalizada no [METHODOLOGY_V2.md](https://github.com/alexandrebrt14-sys/papers/blob/main/docs/METHODOLOGY_V2.md). Os doze pilares:

**1. NER v2 com NFC+NFKD dual-pass.** A extração de entidades agora normaliza o texto em Unicode composto (NFC) e, em um segundo passe, dobra diacríticos via NFKD. Isso significa que "Itau" escrito sem acento é capturado como "Itaú". Sobre 2.000 linhas do dataset histórico, o NER v2 eliminou **45% dos falsos positivos** do NER v1 (1.409 → 776 citações verdadeiras).

**2. Word-boundary regex rigoroso.** Cada match agora é ancorado em `\b` (word boundary). "Stone" em "cornerstone" já não conta.

**3. Dicionário de aliases canônicos.** "BTG" no texto resolve para "BTG Pactual". "XP" para "XP Investimentos". "Magalu" para "Magazine Luiza". Quatorze aliases totais, testados.

**4. Stop-contexts.** "99" não é uma entidade quando seguido por "%". "Amazon" não é a empresa quando precedido por "floresta". Um mini-parser de contexto elimina colisões semânticas que poluíam o dataset anterior.

**5. Estimador sanduíche cluster-robust (CR1).** Para a hipótese H1, o novo código implementa o estimador de variância CR1 com covariância cruzada entre grupos. Isso dá erros-padrão e intervalos de confiança que respeitam o fato de que observações do mesmo dia compartilham estado do modelo.

**6. Simulação Monte Carlo para threshold Jaccard.** O antigo 0.30 arbitrário foi substituído pelo percentil 5 empírico da distribuição nula (2.000 simulações do universo de citações sob uniformidade). Agora "baixa concordância" tem um critério pré-registrado.

**7. Análise de potência pré-registrada.** Cada hipótese tem um roadmap de *n* mínimo computado via Regra de Três inversa (para H2), *h* de Cohen (para H1 e H4) e correção por efeito de desenho (para H5). Isso me diz, *antes* de começar, quantos dias de coleta preciso para cada teste ter potência estatística suficiente.

**8. Modelo linear generalizado misto (GLMM).** Para controlar a variação entre queries, dias e entidades simultaneamente, o pipeline agora usa `statsmodels.BinomialBayesMixedGLM` com interceptos aleatórios aninhados. Isso substitui as regressões logísticas planas do estudo anterior.

**9. Coorte v2.** 79 empresas brasileiras reais (20 por vertical, exceto fintech com 19) + 32 *anchors* internacionais (Revolut, Klarna, Monzo e outros — para permitir comparação cross-vertical) + 16 *decoys* fictícias (4 por vertical, nomes plausíveis em português). Total: 127 entidades monitoradas.

**10. Bateria de queries canônica balanceada.** 192 queries (48 por vertical), balanceadas 50/50 em português/inglês e 50/50 em formato diretivo/exploratório. Cobre 6 categorias (descoberta, comparativo, confiança, experiência, mercado, inovação) em 2 marcos temporais (atemporal e "em 2026").

**11. Motor de hipóteses com FDR de Benjamini-Hochberg.** Todo teste passa por correção de múltiplas comparações, com regra de decisão pré-registrada: rejeita-se H₀ se e somente se o p-valor ajustado por BH for < 0,05 **e** o intervalo de confiança a 95% excluir o valor nulo.

**12. Reprodutibilidade container-level.** O repositório agora inclui um Dockerfile com `PYTHONHASHSEED=20260424` pinado, um `requirements-lock.txt` com 12 dependências versionadas, e um script `scripts/reproduce.sh` que regenera as tabelas do paper a partir de uma tag git, com um manifest SHA-256 de verificação bit-a-bit dos outputs.

Dois pilares complementares da onda de observabilidade (v2.1.0):

**13. Detector de deriva de modelo.** Cada resposta agora grava a versão exata retornada pela API (OpenAI devolve o modelo com data, Anthropic devolve idem, Google devolve `modelVersion`) e um hash SHA-256 dos primeiros 16 caracteres da resposta em uma tabela `model_versions`. Se "gpt-4o-mini" silenciosamente mudar de pesos em junho de 2026, a tabela captura.

**14. Log estruturado JSONL persistido.** Cada rodada de coleta grava um arquivo JSONL em `.logs/structured/` com um evento por query (módulo, LLM, categoria, latência, tokens, custo, citou ou não, erro). O GitHub Actions faz upload desse arquivo como artefato por 30 dias para auditoria post-mortem.

Ao todo, 203 testes automatizados cobrem os módulos novos. Os commits relevantes são `deea1bb`, `680240f`, `93cea8b`, `addf3b8`, `a032560`, `e4df151` — todos em 23 de abril.

## A última correção antes do sinal verde

Na manhã de hoje, com o reboot supostamente pronto, rodei uma auditoria paralela em cinco agentes independentes — cada um investigando uma dimensão (data flow, segredos, pipeline estatístico, observabilidade, cobertura de testes). O agente que mapeou o fluxo de dados identificou um problema que me fez pausar tudo:

**os doze pilares estavam implementados, mas o caminho de coleta real ainda chamava o código v1 legado.**

O pipeline de produção usava a coorte antiga (69 entidades), a bateria antiga (40 queries), a extração antiga (regex simples), não populava as colunas de design de *probe* adicionadas pela migração 0007, e não gravava o hash de resposta da migração 0006. A metodologia v2 era *dead code* — existia, mas ninguém chamava.

A Onda 7 corrigiu isso. Introduzi uma variável de ambiente `PAPERS_METHODOLOGY_VERSION` (default v2 a partir de amanhã), fiz o `BaseCollector` carregar coorte e bateria do `config_v2` quando v2 está ativo, instanciei o `EntityExtractor` v2 preguiçosamente no coletor, e estendi o SQL `insert_citations` de 25 para 43 parâmetros para gravar todas as colunas novas em cada linha. Onze novos testes travam o comportamento no caminho crítico e garantem que regressões futuras sejam flagradas em CI.

Depois disso, a base de dados foi truncada de 18.537 linhas (o dataset v1 completo) para zero. O Paper 4 continua reprodutível: há uma tag git imutável `paper-4-dataset-frozen-20260423` e um backup físico de 11 MB, ambos apontando para o estado de produção no momento da submissão SSRN.

## O que estou buscando nos próximos 90 dias

Amanhã, 24 de abril de 2026 às 06:00 horário de Brasília, o workflow `daily-collect.yml` vai rodar pela primeira vez sobre a nova infraestrutura. Vai rodar de novo às 18:00. Vai continuar rodando duas vezes por dia até 22 de julho. Ao fim da janela, o dataset terá aproximadamente 1.920 linhas por dia × 90 dias = 172.800 citações. Cinco LLMs × quatro verticais × 48 queries × duas coletas diárias.

Sobre esse dataset, pré-registrarei os seguintes testes (antes do início, no OSF, na sexta-feira):

**H1 — Vantagem RAG.** *Modelos com acesso a busca em tempo real (Perplexity) citam empresas com taxa consistentemente maior do que modelos paramétricos (ChatGPT, Claude, Gemini, Groq)?* A expectativa teórica é sim, e o tamanho de efeito esperado (Cohen's *h* ≈ 0,20) exige 1.920 linhas por braço para detecção a 80% de potência — três dias de coleta completa. Se H1 for rejeitado, reforça a narrativa de mercado de que *generative engine optimization* precisa se orientar a fontes citáveis, não só a autoridade de domínio.

**H2 — Alucinação de entidades inexistentes.** *Quando expostos a queries que incluem decoys fictícias na coorte e, em probes adversariais, forçam o modelo a citar algo daquele setor, qual é a taxa real de menção dessas entidades inexistentes?* O teste aqui é um bound superior via Rule-of-Three inversa: com *n* suficiente e zero hits, podemos afirmar que a taxa de alucinação é < 0,2% com 95% de confiança. Se *algum* LLM passar de 1%, é um sinal público de risco.

**H3 — Assimetria inter-LLM.** *Diferentes modelos convergem para o mesmo conjunto de entidades "canonicamente citáveis" em cada vertical, ou cada um tem seu próprio universo?* Aqui o teste é contra a distribuição nula Jaccard simulada. A hipótese que estou disposto a defender é que **há divergência significativa** — o que implicaria que o *pool* de empresas visíveis na internet generativa não é monolítico, e que o posicionamento depende de em qual LLM você está sendo visto.

**H4 — Sensibilidade a formulação de query.** *O mesmo fato (ex.: "quem lidera fintechs no Brasil") produz respostas diferentes quando formulado como pergunta diretiva vs. exploratória?* Métrica: variância entre pares de queries equivalentes do ponto de vista semântico.

**H5 — Estabilidade temporal.** *A citação é estacionária ao longo da janela de 90 dias, ou há deriva atribuível a atualizações silenciosas de modelo?* Testado via detector de drift em `model_versions`.

Para cada hipótese, a publicação do Paper 5 trará não só o resultado, mas também o intervalo de confiança, o ajuste de Benjamini-Hochberg, o *verdict* da regra de decisão pré-registrada (*reject H0* / *fail to reject* / *supported null bounded*), o κ de Cohen da validação inter-anotador entre NER v2 e três LLMs anotadores, e o link para o dataset no Zenodo com SHA-256 manifest.

O target é a [Information Sciences](https://www.sciencedirect.com/journal/information-sciences) (Elsevier, fator de impacto 8,1).

## O que este trabalho tenta provar

Mais do que validar qualquer hipótese individual, o Paper 5 é uma declaração operacional: **é possível fazer ciência empírica sobre sistemas generativos de maneira reprodutível, publicável e falsificável.** A indústria de marketing digital criou uma disciplina chamada *generative engine optimization* que ainda é, em grande parte, folclore. Afirmações sobre "como fazer seu produto aparecer em ChatGPT" circulam em apresentações corporativas sem referência a dados, sem intervalos de confiança, sem pré-registro.

O que estou construindo é a contramedida: um pipeline de observação longitudinal, com coorte formal, bateria de queries canônica, extração de entidades testada e documentada, inferência estatística pré-registrada, reprodutibilidade bit-a-bit, e código aberto sob licença MIT. Se a comunidade achar os resultados incômodos, que refaça os testes com a mesma metodologia — os dados estarão no Zenodo.

Paper 4 mostrou que o silêncio estatístico também é uma forma de honestidade quando a metodologia falha. Paper 5, se tudo correr dentro do plano, vai mostrar o que esses modelos *realmente* fazem quando perguntamos a eles sobre empresas brasileiras — com 192 queries balanceadas, 31-32 entidades por vertical, 172.800 observações, FDR controlado e intervalos que respeitam a estrutura de cluster dos dados.

Vou publicar atualizações aqui ao longo dos 90 dias. A coleta começa amanhã.

---

*O repositório completo é público:* [github.com/alexandrebrt14-sys/papers](https://github.com/alexandrebrt14-sys/papers)

*O Paper 4 está depositado em:* [Zenodo DOI 10.5281/zenodo.19712217](https://doi.org/10.5281/zenodo.19712217) *e SSRN (ID a ser emitido).*

*O progresso da coleta pode ser acompanhado em:* [alexandrecaramaschi.com/papers-roadmap](https://alexandrecaramaschi.com/papers-roadmap) *e* [alexandrecaramaschi.com/research](https://alexandrecaramaschi.com/research)

*Tags: #LLM #GenerativeAI #GEO #GenerativeEngineOptimization #Metodologia #DataScience #Reprodutibilidade #PaperScientifico*
