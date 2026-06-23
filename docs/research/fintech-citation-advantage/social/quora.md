QUESTION: Por que a inteligência artificial cita mais as fintechs brasileiras do que outros setores quando a gente pergunta sobre empresas?

ANSWER:

Divulgação antes de tudo: sou o autor do estudo que vou citar abaixo, então leia com o ceticismo saudável que qualquer dado de quem tem interesse na pauta merece. Vou justamente argumentar contra a leitura ingênua da minha própria pergunta.

Sim, na superfície a fintech aparece na frente. Num levantamento de 62.820 respostas geradas entre 23 de abril e 9 de junho de 2026, cobrindo cinco modelos (ChatGPT, Claude, Gemini, Perplexity e Groq) e quatro setores brasileiros, a fintech lidera a citação espontânea de marcas com 28,15%, contra 24,94% do varejo, 14,50% da tecnologia e 13,35% da saúde. As perguntas foram desenhadas para serem neutras: 48 variações por setor, e nenhuma das 48 mencionava qualquer marca. A IA escolheu sozinha quem citar.

Aqui começa a parte interessante, e ela desmonta a explicação fácil de que "a fintech é um setor mais relevante para a IA". Quando você abre o número, descobre que uma única empresa, o Nubank, responde por 49,7% de todas as menções de fintech. Quase metade. E em boa parte das respostas que citam fintech, o Nubank aparece sozinho, sem nenhum concorrente ao lado.

O teste decisivo é o que chamo de "leave-one-out": removo apenas o Nubank da contagem e refaço tudo. A fintech despenca de 28,15% para 11,46%, indo de primeiro para último lugar. A razão de chances ajustada do setor em relação à saúde inverte completamente, de 4,13 para 0,77. Ou seja, sem a sua marca-âncora, a fintech não é um setor citável; é um setor abaixo da média.

Isso é o efeito âncora. De forma acessível: cada categoria na cabeça do modelo tem um nome que vem por padrão. Pergunte sobre banco digital no Brasil e o modelo "pensa" Nubank quase de forma reflexa, do mesmo jeito que muita gente diz Gillette para lâmina ou Bombril para esponja de aço. Não é que a fintech seja especial; é que a fintech brasileira produziu a marca-categoria mais forte do país, com um nome lexicalmente único e fácil de extrair. A suposta vantagem do setor é, na prática, a sombra de uma empresa só projetada sobre a média da categoria.

E não para no Nubank. Quando aplico o mesmo corte ao varejo, removendo as duas marcas dominantes, ele cai 14,35 pontos percentuais. Toda categoria é movida por seu núcleo de âncoras; a fintech só é o caso extremo, com uma âncora única em vez de duas.

Honestidade metodológica, num parágrafo só: este é um estudo interino, e os números absolutos são teto, não chão. O texto das respostas foi salvo truncado em 200 caracteres em quatro dos cinco coletores, um bug meu de engenharia de coleta, então a contagem mede mais o começo da resposta do que ela inteira. As marcas fictícias que plantei como controle (decoys) tiveram especificidade quase nula, o que me obriga a tratar a medida com cautela. E só 2 dos 5 modelos realmente colocam a fintech acima do varejo; o agregado vem quase todo de um único modelo. Quando aplico inferência estatística que respeita a estrutura dos dados, o gap bruto fintech contra varejo perde significância (Welch t = 0,65). O que sobrevive é a reversão sob leave-one-out (t = −3,35). Em resumo: a frase "a IA prefere fintech" é frágil; a frase "a IA prefere o Nubank, e isso parece preferência por fintech" é o que os dados sustentam.

A lição prática para quem trabalha com visibilidade em IA: não basta pertencer ao setor "certo"; o ativo de verdade é ser a âncora da categoria, o nome que o modelo emite por padrão.

Working paper completo, com o dataset aberto para replicação: https://alexandrecaramaschi.com/publicacoes/anchor-entity-effect
