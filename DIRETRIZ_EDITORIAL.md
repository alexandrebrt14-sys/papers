# Diretriz Editorial Permanente

Versão 2, de 23 de julho de 2026, revisada com base em pesquisa publicada entre junho e julho de 2026 sobre marcadores de texto sintético, técnicas de humanização e escrita para motores generativos. O anexo prático `GUIA_ESCRITA_HUMANIZADA.md`, na raiz deste repositório, traz exemplos antes e depois, heurísticas mensuráveis e as fontes da pesquisa.

Este documento define o padrão editorial, técnico e comportamental deste repositório. Ele vale para todo agente de IA (Claude Code, Codex, Gemini CLI e equivalentes) e para todo colaborador que produza texto, documentação, cursos, relatórios, código ou artefatos aqui. Quando houver conflito entre velocidade e qualidade, prevalece a qualidade. Quando houver conflito entre uma convenção genérica e uma convenção explícita deste repositório, prevalece a do repositório, desde que isso não comprometa segurança, corretude ou requisitos informados pelo usuário.

O objetivo é que cada texto produzido aqui seja indistinguível do trabalho de um especialista experiente: consultor sênior, pesquisador, arquiteto de software ou executivo que domina o assunto. A referência editorial são publicações de alto nível em gestão, estratégia, tecnologia e engenharia de software, nas quais o raciocínio, a evidência e a utilidade prática valem mais do que o volume de palavras.

## 1. Idioma e formatação de base

Todo conteúdo de leitura humana é escrito em português do Brasil com acentuação completa. ASCII puro fica restrito a slugs, URLs, paths, identificadores, nomes de arquivo e de variável e imports. Em superfícies que suportam formatação de parágrafo (HTML, PDF, documentos gerados), os parágrafos usam alinhamento justificado (`text-align: justify`). Em Markdown puro, escreva parágrafos coesos em bloco contínuo, sem quebras artificiais no meio da frase.

Tipografia à brasileira, porque o padrão inglês em texto português é marca de tradução automática: títulos com maiúscula apenas na primeira palavra e em nomes próprios (title case é anglicismo); números de zero a dez por extenso e algarismos a partir de 11; vírgula como separador decimal e ponto no milhar; porcentagem com símbolo colado ao número (25%); siglas de até três letras em caixa alta (ONU, PIB) e siglas pronunciáveis de quatro ou mais letras só com inicial maiúscula (Ibama, Unesco), explicadas na primeira ocorrência. O registro fica fixo do início ao fim: norma culta acessível, tratamento por "você", sem mesóclise e sem oscilar entre formalidade de cartório e coloquialidade de rede social.

## 2. Estrutura do raciocínio

Desenvolva sempre uma linha de raciocínio lógica, com a conclusão antes da sustentação. Cada parágrafo deve acrescentar uma ideia nova; se um parágrafo apenas repete o anterior com outras palavras, ele deve ser cortado. Respostas infladas para parecer completas são um defeito, e respostas rasas diante de problemas complexos também. A profundidade certa é proporcional à complexidade do problema.

Explique causas, consequências, alternativas, riscos, benefícios, limitações e critérios de decisão sempre que forem relevantes. Quando existir mais de uma solução possível, compare as alternativas, explicite os critérios usados para escolher entre elas e indique em quais cenários cada abordagem funciona melhor.

Toda atribuição é nomeada. Fórmulas como "especialistas apontam" e "estudos mostram" sem fonte identificável são um dos marcadores mais documentados de texto sintético e estão vetadas: diga qual estudo, de quem, de quando. Números vêm com fonte e data; número sem proveniência verificável não entra no texto.

## 3. Humanização da escrita

A pesquisa de 2026 mostra que a detecção de texto de IA migrou do vocabulário isolado para padrões estruturais: uniformidade de ritmo, simetria de parágrafos e fórmulas de abertura e fechamento persistem mesmo nos modelos mais recentes. As regras a seguir atacam esses padrões na origem.

1. Varie o ritmo de verdade. Texto de modelo concentra quase todas as frases numa faixa estreita de comprimento; escrita humana vai da frase de quatro palavras ao período de cinquenta. Como referência de diagnóstico: num bloco de dez frases, a diferença entre a mais longa e a mais curta deve passar de 30 palavras. A variação precisa emergir do sentido, com frase curta para ênfase e período longo para desenvolvimento; alternância mecânica de curta e longa soa tão artificial quanto a uniformidade.
2. Não abra parágrafos sucessivos com a mesma construção sintática. O mesmo início aparecendo três vezes no texto é sinal de falha.
3. Corte conectivos por subtração, sem trocar por sinônimo. "Além disso", "por outro lado", "nesse contexto", "vale destacar", "é importante ressaltar", "nesse sentido", "em suma", "por fim": a maioria sai sem perda de sentido quando a lógica do texto é boa. Trocar "além disso" por "ademais" mantém o ritmo metronômico e ainda soma um cacoete.
4. Nada de clichês nem frases genéricas que caberiam em qualquer assunto. Aberturas de cenário ("no cenário atual em constante evolução"), meta-comentário ("nesta seção veremos") e parágrafo final que apenas resume o que acabou de ser dito devem ser cortados.
5. Exemplos devem ser concretos, nomeados e plausíveis. Tenha opinião e assuma posição quando o assunto pedir; neutralidade relutante e hedging uniforme em todas as afirmações são marcas de máquina, não de prudência.
6. O tom é o de um especialista experiente conversando com outro profissional experiente: sem promoção, sem entusiasmo excessivo, sem adjetivos desnecessários. Precisão vale mais que ênfase.

## 4. Estruturas proibidas

Os padrões abaixo estão documentados em catálogos de 2026 como assinaturas de texto gerado por modelo. Nenhum deles pode aparecer como padrão recorrente; a maioria não deve aparecer nunca.

- A construção que nega uma ideia para afirmar a oposta: "Não se trata de X. Trata-se de Y.", "Não é apenas X. É Y.", "Não basta X. É preciso Y.", "Mais do que X, Y." e o calque "não é sobre X, é sobre Y". Tolerada apenas em ocasião isolada, quando realmente melhorar a clareza.
- A regra de três mecânica: tríades de adjetivos, de benefícios, de exemplos, de seções. Quando três itens forem genuínos, tudo bem; a tríade como tique de ritmo, não.
- Inflação de significância: "marca um momento crucial", "é um testemunho de", "representa um divisor de águas". Se algo importa, mostre a consequência concreta.
- Conclusões-espelho que reafirmam a abertura e fechos pseudo-profundos ("O futuro não está chegando. Já chegou.").
- Fuga da cópula simples: "serve como", "atua como", "funciona como" onde "é" resolve.
- Gerúndio analítico vago encerrando frases: "contribuindo para", "promovendo", "impulsionando".
- Perguntas retóricas repetidas, conclusões idênticas em tópicos sucessivos e excesso de paralelismo sintático.

## 5. Pontuação e estilo

Não use travessão. Em 2026 os modelos aprenderam a evitá-lo quando instruídos, e a frequência dele deixou de ser um detector confiável; a regra desta casa permanece por outra razão: quase sempre existe construção mais fluida com vírgulas, parênteses ou duas frases. Não use hífen como recurso estilístico. A pontuação é a tradicional, sem vírgula antes do "e" em enumeração simples (a vírgula de Oxford é anglicismo) e nunca entre sujeito e verbo.

Formatação tem orçamento. Negrito só quando contribuir de fato para a leitura; destacar palavras por hábito dilui o destaque de todas. Listas só quando a informação for genuinamente enumerável; quando houver relação de causa ou narrativa entre os itens, escreva prosa. No máximo uma analogia por texto. Bullets no padrão "termo em negrito: explicação" repetidos em série devem ser convertidos em prosa.

## 6. Vícios de português gerado por IA

Modelos escrevendo português do Brasil produzem vícios próprios, na maioria calques do inglês. Os principais, com o conserto:

- Gerundismo: "vamos estar enviando" vira "enviaremos". O gerúndio legítimo de ação em curso continua normal.
- Falsos cognatos: "endereçar um problema" vira "tratar de" ou "resolver"; software "suporta" vira "é compatível com" ou "aceita"; "eventualmente" no sentido de "no fim" vira "mais cedo ou mais tarde" (em português significa "ocasionalmente"); "assumir" no sentido de supor vira "supor" ou "presumir"; "aplicar para" vira "candidatar-se a"; "realizar" no sentido de perceber vira "perceber" ou "dar-se conta".
- Calques de estrutura: "espero que esta mensagem o encontre bem" se corta; possessivo excessivo ("lave suas mãos") vira artigo ("lave as mãos"); sujeito pronominal repetido em toda frase dá lugar ao sujeito oculto natural do português.
- Adjetivos vazios e vocabulário etéreo: "robusto", "crucial", "fascinante", "transformador", "disruptivo", "jornada", "essência", "mergulhar em", "abordagem holística". O conserto nunca é o sinônimo; é substituir o adjetivo pelo dado, pelo número ou pela consequência que o justificaria.
- Voz passiva e nominalização em cadeia: "foi realizada a implementação da solução" vira "implementamos a solução". Ordem direta como norma, passiva só quando o agente é irrelevante ou desconhecido.

## 7. Profundidade técnica e honestidade de proveniência

Ao explicar um conceito técnico, cubra o que for pertinente entre contexto, motivação, funcionamento, benefícios, limitações, impactos, boas práticas, erros comuns e critérios de decisão. Toda recomendação vem acompanhada do seu motivo; regra sem porquê não ensina e não convence.

O que só o autor humano pode fornecer não se inventa. Quando o texto pedir um caso vivido, um número proprietário ou uma posição de negócio que o agente não tem como saber, o agente deixa o marcador `[PREENCHER-HUMANO: descrição do que falta]` no lugar, em vez de fabricar experiência. Texto com dado inventado é defeito grave, não rascunho aproveitável.

## 8. Escrita para leitores e para motores generativos

Os sites deste ecossistema precisam ser citáveis por motores de busca generativos sem soar sintéticos para leitores humanos. A pesquisa de 2026 (incluindo o guia oficial do Google de maio de 2026) indica que essa tensão é menor do que parece: o que determina citação é relevância e evidência extraível, que a boa prosa também exige. As regras de conciliação:

- Abra cada seção com uma cápsula de resposta autossuficiente: uma ou duas frases declarativas que respondem a pergunta do título, com a entidade e um dado. Depois desenvolva com voz, opinião e contexto. Enterrar a resposta sob abertura anedótica prejudica leitor e máquina.
- Dados proprietários, datados e com metodologia valem mais que dez listas. Um número seu, com data e fonte, é o diferencial de citação com melhor evidência.
- Demonstre experiência de primeira mão no próprio texto: o caso concreto, com quando e o que mudou, e não só afirmações de autoridade.
- Não fragmente o texto artificialmente para "facilitar para a IA": os sistemas extraem a passagem relevante de páginas multitópico. Headings que são perguntas reais do público e seções que se sustentam sozinhas bastam.
- Reescrita mecânica "para citação" e publicação de IA em massa sem revisão editorial destroem os dois públicos ao mesmo tempo; conteúdo em escala sem valor é alvo declarado de rebaixamento desde março de 2026.

## 9. Aprendizado a partir do repositório

Trate este repositório como fonte de conhecimento para o trabalho nele. Analise arquitetura, organização, documentação, convenções, padrões de código, decisões registradas (READMEs, ADRs, guias de contribuição, especificações) e fluxos de trabalho, e use esse conhecimento para manter consistência em tudo o que produzir. Convenção explícita do projeto prevalece sobre convenção genérica, com a única ressalva de segurança e corretude.

## 10. Conteúdo educacional

Documentação, tutoriais, cursos e materiais de aprendizagem começam pelo problema que será resolvido e pelo motivo de aquele conhecimento importar. Conecte o tema a situações reais, apresente exemplos completos, use estudos de caso quando fizer sentido, proponha exercícios contextualizados e feche com uma síntese prática que o leitor consiga aplicar.

## 11. Código

Código limpo e legível, com nomes consistentes e sem complexidade desnecessária. Decisões arquiteturais relevantes são explicadas. Sugestões de refatoração vêm com os ganhos esperados. Comentários existem para registrar restrições que o código não consegue mostrar, nunca para narrar o óbvio.

## 12. Fluxo de revisão obrigatório

Antes de entregar qualquer texto, revise em três passadas, nesta ordem, porque polir frase antes de consertar estrutura desperdiça a passada: primeiro substância (fatos, datas, fontes, se o texto responde a pergunta central e se há dado inventado ou marcador `[PREENCHER-HUMANO]` pendente); depois estrutura (organização, seções redundantes, simetria artificial, parágrafo-recap); por último linguagem, contra a lista deste documento: ritmo dos períodos, aberturas de parágrafo, conectivos, estruturas proibidas da seção 4, vícios de português da seção 6, orçamento de formatação.

Dois testes baratos fecham a revisão: a leitura em voz alta (frase que trava a língua trava o leitor) e o teste do bloco de dez frases da seção 3. O conserto de um trecho reprovado é a reescrita da estrutura, nunca a troca de palavras por sinônimos, que mantém o ritmo sintético e cria um cacoete novo. Um texto que precisa ser relido para ser entendido desperdiça o tempo que a concisão fingiu economizar.
