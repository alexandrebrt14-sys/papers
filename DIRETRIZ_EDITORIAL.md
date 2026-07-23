# Diretriz Editorial Permanente

Este documento define o padrão editorial, técnico e comportamental deste repositório. Ele vale para todo agente de IA (Claude Code, Codex, Gemini CLI e equivalentes) e para todo colaborador que produza texto, documentação, cursos, relatórios, código ou artefatos aqui. Quando houver conflito entre velocidade e qualidade, prevalece a qualidade. Quando houver conflito entre uma convenção genérica e uma convenção explícita deste repositório, prevalece a do repositório, desde que isso não comprometa segurança, corretude ou requisitos informados pelo usuário.

O objetivo é que cada texto produzido aqui seja indistinguível do trabalho de um especialista experiente: consultor sênior, pesquisador, arquiteto de software ou executivo que domina o assunto. A referência editorial são publicações de alto nível em gestão, estratégia, tecnologia e engenharia de software, nas quais o raciocínio, a evidência e a utilidade prática valem mais do que o volume de palavras.

## 1. Idioma e formatação de base

Todo conteúdo de leitura humana é escrito em português do Brasil com acentuação completa. ASCII puro fica restrito a slugs, URLs, paths, identificadores, nomes de arquivo e de variável e imports. Em superfícies que suportam formatação de parágrafo (HTML, PDF, documentos gerados), os parágrafos usam alinhamento justificado (`text-align: justify`). Em Markdown puro, onde não há controle de alinhamento, escreva parágrafos coesos em bloco contínuo, sem quebras artificiais de linha no meio da frase.

## 2. Estrutura do raciocínio

Desenvolva sempre uma linha de raciocínio lógica. Cada parágrafo deve acrescentar uma ideia nova ao texto; se um parágrafo apenas repete o anterior com outras palavras, ele deve ser cortado. Respostas infladas para parecer completas são um defeito, e respostas rasas diante de problemas complexos também. A profundidade certa é proporcional à complexidade do problema.

Explique causas, consequências, alternativas, riscos, benefícios, limitações e critérios de decisão sempre que forem relevantes. Quando existir mais de uma solução possível, compare as alternativas, explicite os critérios usados para escolher entre elas e indique em quais cenários cada abordagem funciona melhor. Tabelas, listas numeradas, exemplos concretos, cenários reais, checklists, matrizes de decisão e resumos executivos são bem-vindos quando tornam a leitura mais eficiente; quando uma narrativa explica melhor, prefira a narrativa.

Responda como alguém que compreende profundamente o domínio do problema, com o porquê antes da regra, e não como alguém que apenas devolve instruções.

## 3. Humanização da escrita

Evite os padrões repetitivos que denunciam texto gerado por modelo. Na prática:

1. Não abra parágrafos sucessivos com a mesma construção sintática.
2. Alterne o tamanho das frases; misture períodos curtos, médios e longos quando isso melhorar a fluidez.
3. Varie os conectivos. Expressões como "além disso", "por outro lado", "nesse contexto", "vale destacar", "é importante ressaltar", "nesse sentido", "por fim", "assim" e "portanto" não podem se repetir ao longo do texto; quando precisar delas, troque por alternativas equivalentes ou reestruture a frase.
4. Evite blocos com exatamente o mesmo ritmo, listas onde uma narrativa explicaria melhor e narrativas de simetria artificial em que todos os parágrafos têm o mesmo formato.
5. Nada de clichês nem frases genéricas que caberiam em qualquer assunto. Todo texto se adapta ao contexto específico da conversa e do repositório.
6. Exemplos devem ser concretos e plausíveis, nunca abstratos ou decorativos.
7. O tom é o de um especialista experiente conversando com outro profissional experiente: sem promoção, sem entusiasmo excessivo, sem exageros, sem adjetivos desnecessários. Precisão vale mais que ênfase.

## 4. Estruturas proibidas

A construção que nega uma ideia para em seguida afirmar a oposta não pode virar padrão do texto. Exemplos do que evitar como recorrência: "Não se trata de X. Trata-se de Y.", "Não é apenas X. É Y.", "Não significa X. Significa Y.", "Não basta X. É preciso Y.", "Mais do que X, Y.". Esse recurso é tolerado apenas em ocasião isolada, quando realmente melhorar a clareza.

Também estão vetados como hábito: abrir muitos parágrafos com o mesmo formato argumentativo, repetir perguntas retóricas, encerrar tópicos sucessivos com conclusões idênticas, frases previsíveis e excesso de paralelismo sintático.

## 5. Pontuação e estilo

Não use travessão. Não use hífen como recurso estilístico quando existir construção equivalente naturalmente fluida; prefira vírgulas, parênteses ou a reescrita da frase. A pontuação é a tradicional, com frases bem organizadas e boa separação entre ideias. Negrito só quando contribuir de fato para a leitura; destacar palavras por hábito dilui o destaque de todas.

## 6. Profundidade técnica

Ao explicar um conceito técnico, cubra o que for pertinente entre: contexto, motivação, funcionamento, benefícios, limitações, impactos, boas práticas, erros comuns e critérios de decisão. Toda recomendação vem acompanhada do seu motivo; regra sem porquê não ensina e não convence.

## 7. Aprendizado a partir do repositório

Trate este repositório como fonte de conhecimento para o trabalho nele. Analise arquitetura, organização, documentação, convenções, padrões de código, estrutura de diretórios, decisões registradas (READMEs, ADRs, guias de contribuição, especificações) e fluxos de trabalho, e use esse conhecimento para manter consistência em tudo o que produzir. Quando o projeto tem padrões bem estabelecidos, siga esses padrões nas sugestões de código e de texto. Convenção explícita do projeto prevalece sobre convenção genérica, com a única ressalva de segurança e corretude.

## 8. Conteúdo educacional

Documentação, tutoriais, cursos e materiais de aprendizagem começam pelo problema que será resolvido e pelo motivo de aquele conhecimento importar. Conecte o tema a situações reais, apresente exemplos completos, use estudos de caso quando fizer sentido, proponha exercícios contextualizados e feche com uma síntese prática que o leitor consiga aplicar.

## 9. Código

Código limpo e legível, com nomes consistentes e sem complexidade desnecessária. Decisões arquiteturais relevantes são explicadas. Sugestões de refatoração vêm com os ganhos esperados. Comentários existem para registrar restrições que o código não consegue mostrar, nunca para narrar o óbvio.

## 10. Revisão final obrigatória

Antes de entregar qualquer texto, revise-o contra esta lista: clareza, coerência, profundidade, utilidade prática, boa organização, linguagem natural, variação sintática, ausência de clichês, ausência de repetições desnecessárias, adequação ao contexto e precisão técnica. Verifique em particular se há estruturas repetidas, palavras usadas muitas vezes, parágrafos sem variação ou ritmo artificial. Se algum critério falhar, reescreva o trecho antes de entregar. Um texto que precisa ser relido para ser entendido desperdiça o tempo que a concisão fingiu economizar.
