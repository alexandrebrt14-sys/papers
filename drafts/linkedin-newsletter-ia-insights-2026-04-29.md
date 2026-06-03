# O monopólio invisível dentro dos LLMs: o que 8.571 queries em 5 modelos revelam sobre Generative Engine Optimization

*Newsletter IA Insights — Alexandre Caramaschi · CEO da Brasil GEO, ex-CMO da Semantix (Nasdaq), advisor estratégico de IA da Nuvini (Nasdaq: NVNI), cofundador da AI Brasil*

---

Nubank apareceu **244 vezes** nas respostas do Claude e **apenas 19 vezes** nas respostas do Gemini, na mesma janela de sete dias, para o mesmo conjunto de 192 perguntas. Magazine Luiza foi citada **207 vezes** pelo Perplexity e **45 vezes** pelo Claude. EMS Pharma teve **144 menções** no Perplexity e **7 no Claude**. Treze vezes mais variação entre dois modelos consultando exatamente as mesmas perguntas, em exatamente o mesmo período.

A tese contraintuitiva que sustenta a Brasil GEO ficou empiricamente verificável em 23 de abril de 2026: **Generative Engine Optimization não é Search Engine Optimization rebatizado**. Cada modelo de linguagem opera um índice próprio de marcas, com hierarquias divergentes, e a estratégia de visibilidade por LLM precisa ser modelada como cinco canais distintos — não um.

Os números abaixo vêm da janela confirmatória v2 do estudo longitudinal que mantemos em código aberto no repositório `alexandrebrt14-sys/papers`. Sete dias de coleta, 8.571 observações, 1.785 citações nominais, 5 LLMs (ChatGPT, Claude, Gemini, Perplexity, Groq), 4 verticais (fintech, varejo, saúde, tecnologia), 192 queries balanceadas 50/50 entre português e inglês, dois runs diários (06h e 18h BRT). A janela completa fecha em 22 de julho de 2026. O que segue são os primeiros achados — todos reproduzíveis pelo dataset público.

## A metodologia em uma linha

| Dimensão | Valor |
|---|---|
| Coorte real BR | 79 entidades · 4 verticais |
| Anchors internacionais | 32 entidades (cross-vertical) |
| Decoys fictícios | 16 (calibração false-positive Onda 16) |
| Bateria canônica | 192 queries · 50% PT / 50% EN · 50% directiva / 50% exploratória |
| LLMs avaliados | 5 (modelos canônicos pinned por SHA-256) |
| Cadência | 2 runs/dia · 90 dias contínuos |
| Estimadores | NER v2 (NFKD + aliases + stops) · CR1 sandwich · GLMM Bayesian |

A coleta não usa scraping. Cada query é submetida via API oficial dos cinco provedores e a resposta é processada por um pipeline de extração nominal com calibração contra entidades fictícias. Isso elimina a contaminação por substring match que invalidou metodologias anteriores publicadas — gap documentado em nosso paper "Three Ways to Fail to Conclude" (Zenodo DOI 10.5281/zenodo.19712217).

## Achado 1 — A regra "82-26-17-8-1" reescreve o ranking de visibilidade

A taxa global de citação nominal nas respostas é de **20,8%**. Esse número agregado, no entanto, esconde o achado mais importante da janela.

| LLM | Queries | Citações | Taxa | Latência média |
|---|---|---|---|---|
| Perplexity (sonar) | 960 | 792 | **82,5%** | 3,7 s |
| Claude (haiku-4-5) | 1.851 | 482 | 26,0% | 4,2 s |
| ChatGPT (4o-mini) | 1.920 | 331 | 17,2% | 6,7 s |
| Groq (Llama 3.3 70B) | 1.920 | 158 | 8,2% | 2,0 s |
| Gemini (2.5 pro) | 1.920 | 22 | 1,1% | 27,8 s |

Cada quartil de citação corresponde a um **regime arquitetural distinto**. Perplexity é RAG-first: a resposta é construída a partir de fontes recuperadas em tempo real, com obrigação de citar. Claude e ChatGPT operam memória paramétrica com hedging conservador — citam quando "lembram" da entidade com confiança suficiente. Groq executa o mesmo Llama 3.3 70B disponível em uso geral, sem camada RAG nem fine-tune editorial. Gemini, na configuração atual, sofre com alocação de tokens entre o canal de raciocínio interno e a saída final, o que está sendo investigado em janela paralela.

A consequência operacional é que **uma marca brasileira que confia apenas no SEO clássico está cega para 4 dos 5 canais que importam em 2026**. Otimizar para Perplexity exige presença em fontes citáveis (notícia, paper, comparativo de terceiros). Otimizar para Claude e ChatGPT exige reconhecimento paramétrico — o que requer densidade de menções em corpora pré-treinamento, não backlinks.

## Achado 2 — Verticais não competem pelo mesmo espaço de citação

Quando segmentamos a taxa global por setor, a dispersão é de mais de duas vezes entre o melhor e o pior caso.

| Vertical | n | Citações | Taxa |
|---|---|---|---|
| Fintech | 2.160 | 617 | **28,6%** |
| Varejo | 2.160 | 551 | 25,5% |
| Tecnologia | 2.112 | 318 | 15,1% |
| Saúde | 2.139 | 299 | **14,0%** |

Fintech tem head-of-market concentrado: Nubank, Itaú, Bradesco, BTG e XP capturam quase toda a atenção paramétrica dos modelos. Varejo segue padrão similar com Magazine Luiza, Mercado Livre e Amazon Brasil. Já saúde apresenta o oposto — coorte fragmentada entre operadoras (Hapvida, NotreDame), redes hospitalares (Rede D'Or, Einstein, Sírio-Libanês), laboratórios (Dasa, Fleury) e farmacêuticas (Hypera, Eurofarma, EMS) sem que nenhum nome capture mais do que 9% das menções totais do setor.

A leitura estratégica é direta: **GEO em saúde brasileira é uma corrida de cauda longa**. Em fintech, é defesa de moat. Em varejo, é disputa de janelas comparativas. Em tecnologia, é construção de autoridade ainda inexistente nos modelos.

## Achado 3 — A inversão idiomática que ninguém esperava

Queries em inglês mencionando empresas brasileiras geram taxa de citação **23,0%**. Queries equivalentes em português geram **18,7%**.

A diferença de 4,3 pontos percentuais é estatisticamente robusta no n acumulado e contraintuitiva à primeira leitura. Marcas brasileiras aparecem **mais** quando o usuário pergunta em inglês do que em português. O mecanismo provável é que o corpora de pré-treinamento que cobre o Brasil em profundidade analítica (papers, relatórios setoriais, imprensa internacional, filings em Nasdaq) é majoritariamente em inglês. O conteúdo em português brasileiro indexado pelos modelos tende a ser disperso, repetitivo e menos co-citado.

A implicação prática para uma área de comunicação corporativa é não-óbvia: **press release em inglês para veículos internacionais de nicho rende mais visibilidade nos LLMs do que três peças equivalentes em português**. Isso inverte a regra clássica de que "marcar presença local" é prioritário.

## Achado 4 — Concentração extrema obedece a lei de potência

Três entidades concentram **75% das 1.785 citações nominais da janela**.

| Posição | Entidade | Menções |
|---|---|---|
| 1 | Nubank | 602 |
| 2 | Magazine Luiza | 394 |
| 3 | Mercado Livre | 354 |
| 4 | Hypera Pharma | 187 |
| 5 | Americanas | 183 |
| 6 | EMS Pharma | 174 |
| 7 | PicPay | 168 |
| 8 | Totvs | 155 |
| 9 | C6 Bank | 154 |
| 10 | Amazon Brasil | 146 |

Marcas internacionais também aparecem com força em queries focadas em Brasil — Amazon (sem qualificador), Pfizer, Novartis, Accenture, Roche e Shein dividem espaço com o cohort nacional, contaminando o "espaço de resposta" disponível.

A consequência tática é que **uma marca fora do top 10 da sua vertical disputa, na média, menos de 1% do tempo de menção dos LLMs**. Aumentar essa fatia exige intervenção deliberada — Schema.org, llms.txt, presença em fontes de alta autoridade citável, e conteúdo otimizado para os padrões de extração de cada modelo.

## Achado 5 — O framing da pergunta vale 12 pontos

Queries directivas ("Quais são as melhores fintechs brasileiras em 2026?") geram taxa de citação **26,8%**. Queries exploratórias ("Como avaliar a confiabilidade de fintechs brasileiras?") geram **14,9%**.

| Tipo de query | n | Citações | Taxa |
|---|---|---|---|
| Directiva | 4.287 | 1.147 | **26,8%** |
| Exploratória | 4.284 | 638 | 14,9% |

Esses 11,9 pontos percentuais de diferença não dependem de marca, vertical ou idioma. São efeito do prompt structure: queries que pedem listagem explícita acionam o modo de recuperação categorial dos modelos, no qual a saída privilegia nomes próprios. Queries abertas ativam o modo discursivo, que privilegia explicação de critérios sobre exemplos nominais.

A consequência para profissionais de marketing é que **a otimização GEO começa antes da resposta — ela começa na conversa que o usuário escolhe iniciar**. Aplicações que controlam o prompt (chatbots verticais, tools de comparação) podem amplificar visibilidade da própria marca via design de prompt. Para SEO clássico, isso não tem paralelo.

## A divergência entre LLMs é a maior oportunidade comercial não-precificada de 2026

Voltando à abertura: Nubank teve **13× mais menções no Claude do que no Gemini**. Magazine Luiza **4,6× mais no Perplexity do que no Claude**. EMS Pharma **20× mais no Perplexity do que no Claude**.

Isso não é ruído estatístico. É estrutura. Cada LLM operacionaliza um conjunto diferente de heurísticas — fontes confiáveis, datas de corte de treino, ponderação setorial, vieses idiomáticos — e o resultado é que a marca "vencedora" em um modelo pode ser invisível em outro.

A maioria das equipes de marketing brasileiras trata os LLMs como uma caixa única. Otimizam pensando em "o ChatGPT", como se fosse um Google sem a interface azul. O dataset acima mostra que essa simplificação custa três quartos do potencial de visibilidade.

## O que muda na sua estratégia segunda-feira

1. **Audite sua presença por LLM, não em agregado.** Rode a mesma query nos cinco modelos e compare. A divergência é o seu briefing.
2. **Trate Perplexity como canal de aquisição direta.** Citation rate de 82,5% e latência de 3,7 segundos transformam o modelo em uma máquina de tráfego qualificado quando há fonte citável.
3. **Construa autoridade paramétrica para Claude e ChatGPT.** Densidade de menções em corpora de alta qualidade (papers, imprensa de nicho internacional, dossiês setoriais) é o que move o ponteiro nesses dois modelos.
4. **Reavalie a alocação PT-EN da sua content strategy.** Se a meta é visibilidade global em LLMs, conteúdo em inglês especializado em Brasil rende mais por dólar gasto.
5. **Estruture seu próprio observatório de citação.** Sem medição contínua, qualquer afirmação sobre GEO é especulação. O dataset que dá origem a esta postagem é público — pode ser replicado para o seu setor em até quatro semanas com a infraestrutura correta.

A janela longitudinal completa (90 dias) fecha em 22 de julho de 2026, com submissão prevista para Information Sciences (Elsevier, IF 8.1) em outubro. Os achados desta postagem usam apenas os primeiros sete dias. À medida que o n cresce, a precisão das estimativas por célula sobe e novas hipóteses entram em escopo: detecção de drift silencioso entre versões dos modelos, calibração de hallucination rate via probes adversariais, e overlap entre fontes do Google SERP e fontes recuperadas pelo Perplexity.

A pergunta operacional que cada CMO brasileiro precisa responder até o fim deste trimestre não é mais "como aparecemos no Google?", e sim **"em qual dos cinco LLMs a nossa categoria foi decidida — e o que estamos fazendo para entrar nessa decisão?"**.

---

*O dataset, código de coleta, metodologia v2 e CHANGELOG estão em `github.com/alexandrebrt14-sys/papers` sob licença MIT. Comentários e sugestões para a próxima onda de coleta são bem-vindos diretamente nas issues do repositório.*

*Alexandre Caramaschi — CEO da Brasil GEO, ex-CMO da Semantix (Nasdaq), advisor estratégico de IA da Nuvini (Nasdaq: NVNI), cofundador da AI Brasil.*
