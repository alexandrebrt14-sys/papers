# Três falhas que quase invalidaram minha pesquisa com LLMs — e como reconstruí tudo em 72 horas

*Edição #X da Newsletter IA Insights — 23 de abril de 2026*

Oi, Alexandre aqui.

Hoje quero te contar uma história que normalmente não se conta publicamente: **quando você faz um estudo científico e descobre que errou**.

Há algumas semanas submeti um paper ao SSRN sobre como os cinco maiores LLMs (ChatGPT, Claude, Gemini, Perplexity e Groq) citam empresas brasileiras. Investi três meses de coleta diária. Sete mil queries. Quatro verticais (fintech, varejo, saúde, tecnologia).

Quando abri os resultados para escrever, vi algo que me incomodou profundamente: **os dados não permitiam concluir nada.**

Em vez de engavetar, resolvi publicar mesmo assim — com o título *"Null-Triad: Three Ways to Fail to Conclude"*. E nas últimas 72 horas, reconstruí a pesquisa inteira do zero. Amanhã começa uma nova janela de coleta de 90 dias.

Esta newsletter é sobre **o que falhou, o que consertei e o que vem pela frente**.

---

## 🧪 O que eu estava tentando descobrir

Três perguntas simples, três hipóteses estatísticas:

**H1 — RAG é melhor?** Modelos com acesso a busca em tempo real (como Perplexity) citam mais empresas do que modelos puramente paramétricos (como ChatGPT)?

**H2 — LLMs alucinam?** Se eu inserir nomes de empresas *fictícias* no estudo, com que frequência os modelos acabam "citando" algo que não existe?

**H3 — LLMs concordam entre si?** Diferentes modelos convergem para o mesmo conjunto de empresas citáveis, ou cada um tem seu próprio universo?

Pergunta de bilhão de dólares, na prática. Se os LLMs divergem, o mercado que chamamos de *generative engine optimization* (GEO) não é um mercado só — são cinco mercados.

---

## 💥 Os três modos de falha

Quando abri os dados, descobri que **todas as três análises estavam comprometidas, cada uma por uma razão diferente**.

### 1. Subpotência estatística em H1

O tamanho da amostra por célula era pequeno. Os erros-padrão calculados ignoravam a estrutura de *cluster* (cada dia de coleta é um cluster — todas as queries daquele dia compartilham o mesmo estado do modelo). Resultado: o intervalo de confiança cruzava o zero. Não dava para dizer "RAG é melhor" nem "RAG é pior".

### 2. Design nulo em H2

Este foi o pior. Eu pensava que estava testando alucinação: incluí oito empresas fictícias na coorte e esperava que os LLMs não as citassem. Resultado: zero hits. Vitória? Não. Eu **nunca perguntei** a eles sobre essas empresas. As fictícias estavam na lista de observação mas jamais em queries que forçassem menção. Zero hits + zero desafio = **zero informação**.

### 3. Instrumentação assimétrica em H3

O threshold de "baixa concordância" entre LLMs era 0.30 de Jaccard. Onde peguei esse número? No chute. Pior: a extração de entidades usava correspondência por substring. *Inter* aparecia dentro de *international*. *Stone* dentro de *keystone*. *Itaú* e *Itau* (sem acento) eram contabilizados como entidades diferentes. A métrica estava inflada por ruído instrumental.

---

## 🔧 O reboot em doze pilares

Nas últimas 72 horas, reimplementei o pipeline inteiro. Ver o [CHANGELOG](https://github.com/alexandrebrt14-sys/papers/blob/main/CHANGELOG.md) completo se quiser os detalhes. Os doze pilares novos:

1. **NER v2** com normalização Unicode NFC + NFKD. "Itau" agora é detectado como "Itaú". Resultado: **45% menos falsos positivos** na extração.

2. **Word-boundary rigoroso**. Adeus ao Stone em *corner*stone.

3. **Aliases canônicos**. BTG resolve para BTG Pactual. XP para XP Investimentos. Magalu para Magazine Luiza.

4. **Stop-contexts**. "99" não é entidade quando seguido de "%". "Amazon" não é empresa quando precedido de "floresta".

5. **Erros-padrão cluster-robust (CR1)**. O estimador sanduíche CR1 respeita a estrutura de cluster dos dados.

6. **Simulação Monte Carlo** para thresholds. Adeus ao 0.30 arbitrário. O novo critério é o percentil 5 empírico sob hipótese nula (2.000 simulações).

7. **Análise de potência pré-registrada**. Cada hipótese tem *antes* um cronograma de quantos dias de coleta precisa para ter 80% de potência estatística.

8. **Modelo linear generalizado misto (GLMM)** com interceptos aleatórios aninhados em query, dia e entidade.

9. **Coorte v2**: 79 empresas brasileiras reais + 32 âncoras internacionais (Revolut, Klarna, Monzo — para comparação cross-vertical) + 16 *decoys* fictícias.

10. **Bateria canônica de 192 queries**, balanceadas 50/50 português/inglês e 50/50 diretivo/exploratório.

11. **Controle de FDR de Benjamini-Hochberg** com regra de decisão pré-registrada: rejeita H₀ *se e somente se* p-ajustado < 0,05 E intervalo de confiança 95% exclui o nulo.

12. **Reprodutibilidade bit-a-bit**. Dockerfile com seed Python pinado, requirements travados, script `reproduce.sh` que regenera todas as tabelas do paper a partir de uma tag git com manifest SHA-256.

Mais dois pilares de observabilidade:

13. **Detector de deriva de modelo**. Cada resposta grava a versão exata que a API retornou. Se "gpt-4o-mini" mudar silenciosamente os pesos em junho, a tabela captura.

14. **Logs estruturados persistidos** como artefatos do CI por 30 dias para auditoria.

**203 testes automatizados cobrem esse código novo.** Tudo público em [github.com/alexandrebrt14-sys/papers](https://github.com/alexandrebrt14-sys/papers).

---

## ⚠️ A última armadilha, descoberta hoje cedo

Aqui entra a parte que mais me ensinou.

Com os doze pilares prontos, rodei uma auditoria final em cinco agentes paralelos — cada um olhando uma dimensão do sistema. O agente que mapeou o fluxo de dados identificou algo que me fez pausar tudo:

**Os doze pilares estavam implementados. Mas o código de coleta em produção ainda chamava as versões v1 antigas.**

A metodologia nova existia em cada módulo, testada, validada. Mas ninguém a chamava. Era *dead code*. O pipeline real ia continuar rodando com a coorte antiga, a bateria antiga, a extração antiga. Os próximos 90 dias teriam sido desperdiçados.

Corrigi em cinco horas. Introduzi uma *feature flag*, fiz o coletor carregar os módulos v2 quando ativado, estendi o SQL de INSERT para gravar todas as colunas novas de cada linha. Onze testes travam esse comportamento contra regressões futuras.

**Lição**: ter a metodologia implementada não basta. A metodologia precisa estar no *hot path*. Teste de ponta-a-ponta importa mais do que teste unitário em pesquisa empírica.

---

## 🎯 O que estou buscando nos próximos 90 dias

Amanhã às 06:00 BRT o workflow roda pela primeira vez sobre a nova infraestrutura. Vai rodar duas vezes por dia até 22 de julho. Ao fim: **172.800 observações** (1.920 por dia × 90 dias).

As hipóteses reformuladas, com poder estatístico agora garantido:

**H1 — Vantagem RAG.** Expectativa: Perplexity cita substancialmente mais do que os paramétricos. Se confirmado, reforça que *GEO precisa se orientar a fontes citáveis, não só autoridade de domínio*.

**H2 — Taxa real de alucinação.** Com probes adversariais forçando menção de fictícias, espero taxas abaixo de 1% em todos os modelos. Se algum ultrapassar, é **sinal público de risco** para quem usa esses modelos como fonte.

**H3 — Assimetria inter-LLM.** A hipótese que estou disposto a defender: **há divergência significativa**. Ou seja, o pool de empresas visíveis na "internet generativa" não é monolítico. Você pode estar visível em ChatGPT e invisível em Claude, ou vice-versa.

**H4 — Sensibilidade a formulação.** "Quem lidera fintechs no Brasil" produz respostas diferentes quando formulado como pergunta diretiva vs. exploratória?

**H5 — Estabilidade temporal.** Modelos derivam silenciosamente em 90 dias?

Target de submissão: [Information Sciences](https://www.sciencedirect.com/journal/information-sciences) (Elsevier, fator de impacto 8,1), em outubro.

---

## 💡 Por que isso importa para quem acompanha IA no Brasil

A disciplina chamada *generative engine optimization* vira tema de apresentação corporativa semanalmente. A maior parte do que é dito sobre ela é **folclore** — afirmações sem dados, sem intervalos de confiança, sem pré-registro.

O que estou construindo é a contramedida: **um estudo empírico, longitudinal, aberto e falsificável** sobre o que esses modelos realmente fazem quando perguntamos sobre empresas brasileiras. Código aberto, dados depositados no Zenodo, metodologia publicada antes dos resultados.

O Paper 4 já foi publicado no [Zenodo com DOI 10.5281/zenodo.19712217](https://doi.org/10.5281/zenodo.19712217). Ele documenta as falhas com a mesma honestidade que vou documentar os achados.

Se você trabalha com IA, marketing digital, visibilidade de marca, ou simplesmente tem curiosidade sobre o que os LLMs dizem sobre o Brasil — **os próximos 90 dias vão produzir o primeiro dataset científico público sobre isso**.

Vou publicar atualizações quinzenais aqui na newsletter. A coleta começa amanhã.

---

**📎 Links para se aprofundar:**
- Repositório completo e público: [github.com/alexandrebrt14-sys/papers](https://github.com/alexandrebrt14-sys/papers)
- Paper 4 depositado no Zenodo: [DOI 10.5281/zenodo.19712217](https://doi.org/10.5281/zenodo.19712217)
- Progresso da coleta em tempo real: [alexandrecaramaschi.com/research](https://alexandrecaramaschi.com/research)
- Roadmap dos papers: [alexandrecaramaschi.com/papers-roadmap](https://alexandrecaramaschi.com/papers-roadmap)

**Se esta newsletter foi útil**, compartilhe com alguém que esteja pensando em fazer pesquisa empírica sobre LLMs — e me conta em comentário: qual hipótese você acha mais provável de se confirmar, H1, H2 ou H3?

*Até a próxima quinzena.*

*— Alexandre Caramaschi · CEO Brasil GEO · ex-CMO Semantix (Nasdaq) · cofundador AI Brasil*
