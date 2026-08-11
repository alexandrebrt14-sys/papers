# Diretriz Editorial Permanente

Versão 4, de 11 de agosto de 2026. A v3, do mesmo dia, corrigiu a doutrina de reprovação e instalou o piso de substância e a narrativa. Esta versão fecha o que faltava: a prova entra antes da escrita e limita o tamanho da peça (seção 2.2), a promessa e a tensão são redigidas antes do esqueleto e o esqueleto segue a ordem do gênero (seções 3.1 e 3.2), o pedido vira um só por peça com fórmula declarada (seção 3.6), e a revisão ganha travas verificáveis, entre elas as quatro conferências que todo símbolo de porcentagem dispara (seção 13).

Histórico curto do problema, porque ele explica o formato deste documento. A doutrina de julho de 2026 era construída quase inteiramente de mecanismos de reprovação: 46 expressões banidas, orçamento de formatação, tetos de bloco e de marcador, trava de estilometria. Nenhuma regra dizia o que a peça precisa ter, e o efeito é mecânico: texto curto, uniforme e sem argumento passa em todos os gates, porque nenhum deles mede substância. Somavam-se a isso cotas de cadência aritmeticamente insatisfazíveis, cotas de formatação que fragmentavam o texto, camadas de orientação contraditórias e ausência completa de técnica narrativa. O anexo prático `GUIA_ESCRITA_HUMANIZADA.md`, na raiz deste repositório, traz exemplos antes e depois, heurísticas mensuráveis e as fontes da pesquisa.

Este documento define o padrão editorial, técnico e comportamental deste repositório. Ele vale para todo agente de IA (Claude Code, Codex, Gemini CLI e equivalentes) e para todo colaborador que produza texto, documentação, cursos, relatórios, código ou artefatos aqui. Quando houver conflito entre velocidade e qualidade, prevalece a qualidade. Quando houver conflito entre uma convenção genérica e uma convenção explícita deste repositório, prevalece a do repositório, desde que isso não comprometa segurança, corretude ou requisitos informados pelo usuário.

O objetivo é que cada texto produzido aqui seja indistinguível do trabalho de um especialista experiente: consultor sênior, pesquisador, arquiteto de software ou executivo que domina o assunto. A referência editorial são publicações de alto nível em gestão, estratégia, tecnologia e engenharia de software, nas quais o raciocínio, a evidência e a utilidade prática valem mais do que o volume de palavras.

## 1. Idioma e formatação de base

Todo conteúdo de leitura humana é escrito em português do Brasil com acentuação completa. ASCII puro fica restrito a slugs, URLs, paths, identificadores, nomes de arquivo e de variável e imports. Em superfícies que suportam formatação de parágrafo (HTML, PDF, documentos gerados), os parágrafos usam alinhamento justificado (`text-align: justify`). Em Markdown puro, escreva parágrafos coesos em bloco contínuo, sem quebras artificiais no meio da frase.

Tipografia à brasileira, porque o padrão inglês em texto português é marca de tradução automática: títulos com maiúscula apenas na primeira palavra e em nomes próprios (title case é anglicismo); números de zero a dez por extenso e algarismos a partir de 11; vírgula como separador decimal e ponto no milhar; porcentagem com símbolo colado ao número (25%); siglas de até três letras em caixa alta (ONU, PIB) e siglas pronunciáveis de quatro ou mais letras só com inicial maiúscula (Ibama, Unesco), explicadas na primeira ocorrência. O registro fica fixo do início ao fim: norma culta acessível, tratamento por "você", sem mesóclise e sem oscilar entre formalidade de cartório e coloquialidade de rede social.

## 2. Estrutura do raciocínio

Desenvolva sempre uma linha de raciocínio lógica, com a conclusão antes da sustentação. Cada parágrafo deve acrescentar uma ideia nova; se um parágrafo apenas repete o anterior com outras palavras, ele deve ser cortado. Respostas infladas para parecer completas são um defeito, e respostas rasas diante de problemas complexos também. A profundidade certa é proporcional à complexidade do problema.

Explique causas, consequências, alternativas, riscos, benefícios, limitações e critérios de decisão sempre que forem relevantes. Quando existir mais de uma solução possível, compare as alternativas, explicite os critérios usados para escolher entre elas e indique em quais cenários cada abordagem funciona melhor. A recomendação vem junto e justificada, porque comparação sem recomendação transfere ao leitor um trabalho que era do autor. A forma mais eficiente de registrar essa comparação costuma ser tabela ou matriz de decisão: critérios nas linhas, alternativas nas colunas, e a recomendação desenvolvida na prosa que acompanha, com a condição de contorno junto. "Use A" é fraco. "Use A quando o volume passar de N e a equipe tiver B; abaixo disso, C resolve com menos manutenção" é útil, porque diz ao leitor onde ele está no mapa.

Toda atribuição é nomeada. Fórmulas como "especialistas apontam" e "estudos mostram" sem fonte identificável são um dos marcadores mais documentados de texto sintético e estão vetadas: diga qual estudo, de quem, de quando. A proibição vale além das expressões catalogadas e alcança qualquer sujeito coletivo sem nome ocupando o lugar da fonte. Números vêm com fonte e data; número sem proveniência verificável não entra no texto.

### 2.1 Piso de substância: o que toda peça precisa ter

As seções seguintes deste documento listam sobretudo o que evitar, e uma doutrina feita só de proibição tem um furo previsível: texto curto, uniforme e sem argumento não viola nenhuma regra e mesmo assim não serve. Os gates automáticos do repositório agravam isso, porque medem forma (acento, clichê, contagem, marcação) e não conseguem medir substância. Aprovação nos gates nunca equivale a aprovação editorial.

Antes de olhar para o que cortar, verifique se a peça tem:

1. **Uma tese identificável.** Uma frase que o autor defende e com a qual seria possível discordar. Compilação neutra do que já existe não é peça pronta.
2. **Evidência que sustenta a tese**, e não números avulsos decorando o texto. A frase seguinte ao número mostra se ele está trabalhando: se ela explica o que o número faz pela tese, o dado é prova; se muda de assunto, o dado estava ali para parecer rigoroso.
3. **Ganho de informação.** Ao menos um dado, caso, comparação ou framework que o leitor não acharia nas primeiras páginas de qualquer busca sobre o tema. Sem isso, a peça é redundante mesmo estando correta, e silêncio custa menos que redundância.
4. **Critério de decisão explícito** quando houver alternativas, com a recomendação e o seu porquê.
5. **Arco de leitura** conforme a seção 3: promessa, tensão, desenvolvimento que paga a promessa e fechamento que retoma.
6. **Consequência para o leitor.** O que ele faz diferente depois de ler, dito de forma que dê para executar.

Peça que falha em qualquer um destes seis itens não é corrigida cortando trechos; é reescrita ou devolvida ao autor. Nenhuma regra de estilo deste documento autoriza sacrificar um dos seis para cumprir uma proibição: quando a proibição e o piso de substância entrarem em conflito, o piso vence e o trecho é reformulado até cumprir os dois.

### 2.2 Prova antes da escrita, nunca depois

Levante o material de evidência antes da primeira frase e monte a lista do que existe de verdade: números proprietários com origem, data, método e denominador; casos de cliente com nome e autorização escrita; prints datados; demonstrações gravadas; e números de terceiro cuja publicação original alguém da casa tenha aberto e conferido.

Essa lista define o tamanho possível da peça. A regra é dura e economiza discussão: o número de blocos que afirmam resultado é menor ou igual ao número de provas datadas disponíveis hoje. Página com doze cartões e duas provas está declarando que dez cartões são adjetivo.

Quando faltar prova, existem quatro saídas antes de recorrer ao marcador de lacuna, e elas se tentam nesta ordem: pesquisar até achar a origem; reduzir a afirmação ao tamanho do que se sabe; restringir o uso, tirando o argumento de campanha ampla; segurar a publicação. Só depois de as quatro falharem entra o marcador, no lugar do dado e nunca no lugar da seção inteira. O teto é de cinco marcadores abertos por documento: acima disso a peça não está pronta para revisão, está pedindo apuração.

Dois marcadores convivem, com divisão de trabalho clara. `[FALTA EVIDÊNCIA: o que precisa ser buscado]` sinaliza lacuna que a etapa seguinte do pipeline pode resolver com pesquisa. `[PREENCHER-HUMANO: descrição do que falta]` sinaliza o que só o autor humano tem, como caso vivido, número proprietário ou posição de negócio. Nenhum dos dois é convite para estimar: número inventado é o defeito mais caro que um texto pode ter, porque contamina retroativamente tudo o que o autor já publicou.

Cuidado, por fim, com o número medido no registro errado. Estatística extraída de conversa transcrita não governa forma de texto escrito, e média de corpus inteiro não descreve o subconjunto que interessa. Antes de usar um número próprio, pergunte sobre qual amostra ele foi medido e se essa amostra é a mesma coisa que você está querendo descrever.

## 3. Narrativa, promessa e engajamento

Profundidade que ninguém lê não ensina nada. O texto precisa prender o leitor pelo interesse, nunca pelo artifício, e as técnicas que sustentam isso em publicação de negócios de alto nível são conhecidas. As seis abaixo são obrigatórias em conteúdo de leitura humana com mais de algumas centenas de palavras (artigo, aula, landing page, capítulo, post longo):

1. Abertura em situação, não em definição. Comece por uma cena concreta, um caso, um número que contraria a expectativa ou uma decisão difícil que o leitor reconhece da própria rotina. A definição chega depois, quando ele já sabe por que precisa dela.
2. Tensão real antes da solução. Antes de desenvolver a resposta, deixe claro o que está em jogo: o custo de errar, o ganho de acertar, o prazo que aperta, com dado quando houver. Solução sem tensão chega como catálogo.
3. Caso condutor. Um caso nomeado que atravessa o texto e reaparece nos exemplos, com rótulo de tipo conforme a seção 3.4.
4. Loop aberto honesto. A abertura promete o que o texto entrega de verdade, e o leitor percebe a promessa sendo cumprida. Curiosity gap fabricado ("o que descobrimos vai te surpreender") é isca e está vetado. A forma sofisticada é pior, porque engana melhor: prometer no primeiro parágrafo uma resposta que o texto nunca chega a dar, escondendo a falta atrás de bom vocabulário.
5. Fechamento com callback. O final retoma o caso ou a tensão da abertura e mostra a resolução que o desenvolvimento construiu. Isso substitui o parágrafo-recap, que continua proibido.
6. Mostrar antes de qualificar. Em vez de afirmar que algo é grave, mostre o prejuízo, o ganho ou o prazo em número e consequência. O leitor conclui a gravidade sozinho, e conclusão própria persuade mais que adjetivo alheio.

O limite é o mesmo de toda técnica: a história serve ao argumento. Drama fabricado, suspense artificial e anedota que não sustenta a tese saem do texto junto com os clichês. Quando a história e a tese competem, corta-se a história.

### 3.1 Promessa e tensão escritas antes do esqueleto

Primeiro a promessa: o que o leitor ganha, em quanto tempo e a que custo de esforço. As duas primeiras partes são obrigatórias na primeira linha, e a terceira pode descer para a linha seguinte. Teto de doze palavras na manchete. Depois a tensão: o que custa continuar como está, com número quando houver.

A tensão nunca adia a promessa, e essa conciliação é a que mais gente erra. A promessa é a resposta e continua na abertura; a tensão vem depois dela e antes do mecanismo, para explicar por que o mecanismo importa. Enterrar a resposta sob uma cena longa é sala de espera, e o leitor fecha a aba antes de chegar nela.

Existe um portão anterior à redação da promessa, e ele é mais exigente que o teto de palavras: só se publica promessa quando existem três coisas, uma experiência que o cliente reconhece, uma medida que a representa e uma rota de reparação quando ela falha.

Promessa escrita depois do esqueleto sai contaminada pela estrutura, e vira resumo do que o texto faz em vez de declaração do que o leitor ganha. Escrita antes, ela vira o critério que decide o que entra e o que sai de cada bloco.

### 3.2 O esqueleto segue a ordem do gênero

**Página comercial:** situação reconhecível, progresso desejado, mecanismo específico, prova verificável, objeção, preço, próximo passo reversível. De sete a nove blocos, cada um lido em voz alta abaixo de um minuto. A regra de posição vale para todos os gêneros: pedido chegando antes da prova soa como cobrança.

**Artigo ou relatório:** abertura em situação, tensão, tese com a conclusão antes da sustentação, desenvolvimento por evidência, comparação de alternativas quando houver mais de um caminho, limitações declaradas, fechamento com callback e próximo passo.

**Aula ou material de capacitação:** problema como situação concreta com tensão e custo, âncora na experiência prévia do aluno, conceito nomeado depois, exemplo resolvido do começo ao fim (que é o caso condutor), erros comuns com sintoma, causa e movimento de saída, checklist com critério de pronto, modelo pronto para copiar, e síntese prática que retoma o caso da abertura. Todo objetivo e todo título de passo usa verbo de nível alto (aplicar, executar, diagnosticar, priorizar, comparar, avaliar, construir, projetar, recomendar, calcular), nunca os de nível baixo (entender, conhecer, saber, identificar, listar, descrever).

### 3.3 Abertura

A cena é curta, banal e datada. Terça-feira, planilha antiga, grupo de WhatsApp da empresa, telefone quieto. O erro descrito é sempre do processo, e existe uma implementação gramatical disso, mais confiável do que boa intenção: em toda frase sobre falha, o lugar de sujeito é ocupado por um artefato ou por um processo. "Você configurou errado o rastreamento" e "a etiqueta de origem não chegou ao cadastro" descrevem o mesmo fato, e só a segunda mostra onde mexer sem cobrar nada de ninguém.

Cinco aberturas funcionam, e cada uma resolve um problema: a pergunta com o tamanho declarado, a pergunta com a metade desconfortável, o anti-suspense como contrato, a fronteira com a peça vizinha e a cena rotulada.

O que nunca abre: saudação, apresentação da empresa, história da fundação, parágrafo explicando por que você está escrevendo, e abertura de cenário genérica. O teste da abertura genérica é o da intercambiabilidade: se a primeira frase caberia igual numa peça de outro assunto, ela é aquecimento de quem escreve, e aquecimento se apaga depois. Meta-comentário do tipo "neste artigo veremos" narra o texto em vez de entregá-lo, e some sem perda nenhuma.

A abertura é o único lugar do texto em que o leitor ainda não decidiu se vai ler. Gastá-la com informação que ele já tem, ou com informação sobre você, é gastar a frase mais lida do texto no que menos importa.

### 3.4 Caso condutor e rótulo de tipo

Escolha um caso que vai atravessar o texto inteiro: uma pessoa, uma empresa, uma situação, com nome e com uma unidade de negócio que se possa acompanhar do começo ao fim. Ele aparece na abertura, reaparece nos exemplos do desenvolvimento e volta no fechamento com o estado mudado.

Rotule imediatamente qual dos três tipos ele é. Caso real exige nome e autorização, e o relato ganha muito quando inclui a decisão difícil que alguém precisou tomar no meio do caminho, porque história de sucesso sem erro nenhum é a assinatura mais confiável de caso fabricado. Cenário hipotético carrega rótulo explícito, do tipo "cena que estamos inventando agora só para a didática", e o rótulo se repete colado a cada número toda vez que ele é retomado, porque o número é o que vira print e o print viaja sem o cabeçalho. Caso inventado apresentado como real é defeito grave, não rascunho aproveitável.

Três casos diferentes, um por seção, dão três exemplos e nenhum condutor: o leitor não acumula nada de um bloco para o outro e chega ao fim sem ter visto uma transformação completa. Um caso que atravessa transforma uma sequência de afirmações num percurso, e percurso é o que faz alguém terminar de ler.

### 3.5 Tensão sem escassez fabricada

A aversão à perda é o único gatilho que a peça pode usar em volume, e o lugar dela é o bloco de mecanismo, nunca o botão. Existe uma diferença que decide se a tensão é boa: ela precisa apontar para um custo que já está acontecendo, e não para um castigo futuro inventado. "O número ruim de hoje é o mais barato que ele jamais vai custar" é tensão. "Vagas limitadas" é escassez fabricada e está proibida, com a família inteira junto: "últimas vagas", "por tempo limitado", "garanta já", "não perca", "oportunidade única".

### 3.6 Um pedido por peça

O bloco imediatamente anterior ao pedido retoma o caso ou a tensão da abertura e mostra o estado mudado.

O pedido é um só por peça. Conte destinos, não botões. A exceção admitida é a escada de compromisso crescente, com peso visual decrescente e medição separada; opção equivalente, que cabe lado a lado sem que se possa dizer qual vem antes, é adiamento disfarçado de escolha e uma delas precisa sair.

A fórmula do convite tem quatro peças: verbo de ação, valor concreto, tempo ou esforço, risco removido. O botão carrega o verbo e o objeto; a linha de apoio carrega o tempo e o risco removido. "Responda com o tamanho da sua base e eu te devolvo o cálculo hoje" tem as quatro. "Saiba mais" não tem nenhuma.

Verbos que servem, no imperativo direto e com objeto visualizável: abra, escreva, conte, corte, liste, marque, escolha, grave, anote, confira, publique, troque, preencha. Não existe "descubra o poder", "transforme" nem "não perca".

Em material educacional, o fechamento é a síntese prática: o que a pessoa faz na segunda-feira, com qual dos artefatos entregues e sob qual critério de pronto.

## 4. Humanização da escrita

A pesquisa de 2026 mostra que a detecção de texto de IA migrou do vocabulário isolado para padrões estruturais: uniformidade de ritmo, simetria de parágrafos e fórmulas de abertura e fechamento persistem mesmo nos modelos mais recentes. As regras a seguir atacam esses padrões na origem.

1. Varie o ritmo de verdade. Texto de modelo concentra quase todas as frases numa faixa estreita de comprimento; escrita humana vai da frase de quatro palavras ao período de cinquenta. O diagnóstico se aplica ao texto pronto, em duas faixas: num bloco de dez frases, diferença abaixo de 15 palavras entre a mais longa e a mais curta é defeito e pede reescrita daquele trecho; acima de 30 é folgadamente compatível com escrita humana. O intervalo entre as duas é aceitável quando a variação acompanha o argumento. Nada disso é alvo a perseguir durante a escrita, e nenhuma outra regra de comprimento (crescimento por frase, teto por parágrafo, ração de frase curta) pode ser combinada com este diagnóstico: a soma dessas regras é aritmeticamente insatisfazível e produz exatamente a faixa estreita que ela diz combater.
2. Escreva sem contar palavras. Junte em período longo o raciocínio que carrega causa e ressalva juntas, e deixe curta a frase que fecha o bloco ou marca a virada. Existe uma razão prática por trás disso: uma frase fica longa quando público, condição e exceção precisam viajar dentro dela, porque o que fica fora da frase fica para trás quando alguém recorta o trecho. O comprimento é consequência de uma decisão de conteúdo, nunca uma decisão em si.
3. Não abra parágrafos sucessivos com a mesma construção sintática. O mesmo início aparecendo três vezes no texto é sinal de falha, e o conserto é mudar a entrada de alguns: oração subordinada, adjunto de tempo, aposto, dado que puxa a frase. Mantenha ao menos metade das aberturas em ordem direta, porque inversão em tudo é outro tique.
4. Corte conectivos por subtração, sem trocar por sinônimo. "Além disso", "por outro lado", "nesse contexto", "vale destacar", "é importante ressaltar", "nesse sentido", "em suma", "por fim": a maioria sai sem perda de sentido quando a lógica do texto é boa. Trocar "além disso" por "ademais" mantém o ritmo metronômico e ainda soma um cacoete. A única troca legítima é por uma transição que carrega informação: em vez de "nesse contexto, a equipe decidiu migrar", escreva "com o prazo em quatro semanas, a equipe decidiu migrar".
5. Nada de clichês nem frases genéricas que caberiam em qualquer assunto. Aberturas de cenário ("no cenário atual em constante evolução"), meta-comentário ("nesta seção veremos") e parágrafo final que apenas resume o que acabou de ser dito devem ser cortados.
6. Exemplos devem ser concretos, nomeados e plausíveis. Tenha opinião e assuma posição quando o assunto pedir. Neutralidade relutante, com todas as opções recebendo elogios equivalentes, é marca de máquina, não de prudência: quem domina o assunto tem preferência e explicita o motivo dela.
7. Medição do próprio corpus descreve, não prescreve. Número extraído dos textos da casa entra como descrição do registro que a casa pratica, e só ganha estatuto de regra depois de passar por dois testes. O primeiro é o de registro: fala transcrita, locução gravada e conversa não governam forma de página escrita, então corpus dessa natureza fica fora da amostra que define forma. O segundo é o de compatibilidade: o limiar novo precisa ser satisfazível junto com todos os que já valem, e quem propõe faz a conta antes de publicar. A doutrina anterior falhou nos dois, e o resultado foi uma fôrma de parágrafo derivada majoritariamente de conversa transcrita e aritmeticamente incompatível com a tabela de limiares que a acompanhava: as regras de crescimento produziam amplitude perto de 13 a 16 palavras, e a última linha da mesma tabela exigia mais de 30.
8. Nenhuma cota mecânica de ritmo, em nenhuma direção. Nem "uma frase curta em cada parágrafo", nem "nunca duas frases seguidas do mesmo tamanho", nem a fôrma oposta de sempre abrir curto e fechar longo. As três produzem staccato de manchete ou simetria de parágrafo, e os catálogos de detecção listam as duas como assinatura de máquina, exatamente como listam a uniformidade que elas pretendiam corrigir. O diagnóstico do item 1 mede o texto pronto e aponta onde reescrever; ele nunca vira fórmula de produção nem contagem de palavras durante a escrita.
9. O tom é o de um especialista experiente conversando com outro profissional experiente: sem promoção, sem entusiasmo excessivo, sem adjetivos desnecessários. Precisão vale mais que ênfase.

## 5. Estruturas proibidas

Os padrões abaixo estão documentados em catálogos de 2026 como assinaturas de texto gerado por modelo. Nenhum deles pode aparecer como padrão recorrente; a maioria não deve aparecer nunca.

- A construção que nega uma ideia para afirmar a oposta: "Não se trata de X. Trata-se de Y.", "Não é apenas X. É Y.", "Não basta X. É preciso Y.", "Mais do que X, Y." e o calque "não é sobre X, é sobre Y". Tolerada apenas em ocasião isolada, quando realmente melhorar a clareza.
- A regra de três mecânica: tríades de adjetivos, de benefícios, de exemplos, de seções. Quando três itens forem genuínos, tudo bem; a tríade como tique de ritmo, não.
- Inflação de significância: "marca um momento crucial", "é um testemunho de", "representa um divisor de águas". Se algo importa, mostre a consequência concreta.
- Conclusões-espelho que reafirmam a abertura e fechos pseudo-profundos ("O futuro não está chegando. Já chegou.").
- Fuga da cópula simples: "serve como", "atua como", "funciona como" onde "é" resolve.
- Gerúndio analítico vago encerrando frases: "contribuindo para", "promovendo", "impulsionando".
- Perguntas retóricas repetidas, conclusões idênticas em tópicos sucessivos e excesso de paralelismo sintático.
- Escassez fabricada e convite vazio, conforme as seções 3.5 e 3.6.

## 6. Pontuação, estilo e estrutura visual

Travessão está vetado em prosa, e tolerado apenas em título e cabeçalho de seção. Em texto corrido, quase sempre existe construção mais fluida com vírgula, dois-pontos, parênteses ou duas frases. Não use hífen como recurso estilístico. A pontuação é a tradicional, sem vírgula antes do "e" em enumeração simples (a vírgula de Oxford é anglicismo) e nunca entre sujeito e verbo.

Formatação tem orçamento, e o orçamento existe para proteger o destaque do que merece destaque. Negrito só em termos que o leitor precisará reencontrar ao escanear a página; destacar palavras por hábito dilui o destaque de todas. Uma analogia por peça, e ela pertence ao conceito central; os outros conceitos se resolvem com definição de uma frase colada ao termo.

Elementos estruturados são ferramentas de consultoria, não enfeite, e entram sempre que ajudarem de verdade, sem pedir licença: tabela comparativa quando há alternativas com critérios, matriz de decisão quando o leitor precisa escolher, checklist quando há passos verificáveis, lista numerada quando a ordem importa, fluxo de trabalho quando há processo, resumo executivo quando o documento é longo o bastante para ser lido em dois níveis. Um profissional decide mais rápido com uma matriz bem construída do que com três parágrafos de prosa equivalente.

Voltam a ser prosa: sequências de bullets cujos itens têm relação de causa entre si, porque a lista esconde o encadeamento; séries de "termo em negrito: explicação" usadas como esqueleto de seção; e qualquer lista que esteja fazendo o trabalho de argumentar. A regra que separa os dois é curta: prosa carrega raciocínio; estrutura carrega comparação, sequência e verificação. Nenhum dos dois entra por cota.

## 7. Vícios de português gerado por IA

Modelos escrevendo português do Brasil produzem vícios próprios, na maioria calques do inglês. Os principais, com o conserto:

- Gerundismo: "vamos estar enviando" vira "enviaremos". O gerúndio legítimo de ação em curso continua normal.
- Falsos cognatos: "endereçar um problema" vira "tratar de" ou "resolver"; software "suporta" vira "é compatível com" ou "aceita"; "eventualmente" no sentido de "no fim" vira "mais cedo ou mais tarde" (em português significa "ocasionalmente"); "assumir" no sentido de supor vira "supor" ou "presumir"; "aplicar para" vira "candidatar-se a"; "realizar" no sentido de perceber vira "perceber" ou "dar-se conta".
- Calques de estrutura: "espero que esta mensagem o encontre bem" se corta; possessivo excessivo ("lave suas mãos") vira artigo ("lave as mãos"); sujeito pronominal repetido em toda frase dá lugar ao sujeito oculto natural do português.
- Adjetivos vazios e vocabulário etéreo: "robusto", "crucial", "fascinante", "transformador", "disruptivo", "jornada", "essência", "mergulhar em", "abordagem holística". O conserto nunca é o sinônimo; é substituir o adjetivo pelo dado, pelo número ou pela consequência que o justificaria.
- Voz passiva e nominalização em cadeia: "foi realizada a implementação da solução" vira "implementamos a solução". Ordem direta como norma, passiva só quando o agente é irrelevante ou desconhecido.

## 8. Profundidade técnica e honestidade de proveniência

Ao explicar um conceito técnico, cubra o que for pertinente entre contexto, motivação, funcionamento, benefícios, limitações, impactos, boas práticas, erros comuns e critérios de decisão. Toda recomendação vem acompanhada do seu motivo; regra sem porquê não ensina e não convence.

O que só o autor humano pode fornecer não se inventa, e o tratamento das lacunas segue a seção 2.2: quatro saídas antes do marcador, marcador no lugar do dado e nunca da seção, teto de cinco marcadores abertos por documento. Texto com dado inventado é defeito grave, não rascunho aproveitável.

## 9. Escrita para leitores e para motores generativos

Os sites deste ecossistema precisam ser citáveis por motores de busca generativos sem soar sintéticos para leitores humanos. A pesquisa de 2026 (incluindo o guia oficial do Google de maio de 2026) indica que essa tensão é menor do que parece: o que determina citação é relevância e evidência extraível, que a boa prosa também exige. As regras de conciliação:

- Abra cada seção interna com uma cápsula de resposta autossuficiente: uma ou duas frases declarativas que respondem a pergunta do título, com a entidade e um dado. Depois desenvolva com voz, opinião e contexto.
- A cápsula convive com a narrativa, e a divisão de trabalho é clara: a abertura do texto inteiro usa as técnicas da seção 3 para prender o leitor, sem adiar a promessa; as seções internas, com headings que são perguntas reais, abrem com resposta direta.
- Cada seção precisa se sustentar sozinha, porque é essa a unidade que um motor generativo recorta. Vale para as frases também: público, condição e exceção viajam dentro da mesma sentença, já que um "não serve para X" recortado sem o "somente" chega ao leitor como "serve".
- Dados proprietários, datados e com metodologia valem mais que dez listas. Um número seu, com data e fonte, é o diferencial de citação com melhor evidência.
- Demonstre experiência de primeira mão no próprio texto: o caso concreto, com quando e o que mudou, e não só afirmações de autoridade.
- Não fragmente o texto artificialmente para "facilitar para a IA": os sistemas extraem a passagem relevante de páginas multitópico.
- Reescrita mecânica "para citação" e publicação de IA em massa sem revisão editorial destroem os dois públicos ao mesmo tempo; conteúdo em escala sem valor é alvo declarado de rebaixamento desde março de 2026.

## 10. Aprendizado a partir do repositório

Trate este repositório como fonte de conhecimento para o trabalho nele. Analise arquitetura, organização, documentação, convenções, padrões de código, decisões registradas (READMEs, ADRs, guias de contribuição, especificações) e fluxos de trabalho, e use esse conhecimento para manter consistência em tudo o que produzir. Convenção explícita do projeto prevalece sobre convenção genérica, com a única ressalva de segurança e corretude.

## 11. Conteúdo educacional

Documentação, tutoriais, cursos e materiais de aprendizagem seguem a ordem de gênero da seção 3.2 e as seis técnicas da seção 3. O problema chega como situação concreta, com tensão e custo, antes da teoria que o resolve. Conecte o tema a situações reais, apresente exemplos completos, use estudos de caso quando fizer sentido, proponha exercícios contextualizados e feche com a síntese prática: o que a pessoa faz na segunda-feira, com qual artefato e sob qual critério de pronto.

## 12. Código

Código limpo e legível, com nomes consistentes e sem complexidade desnecessária. Decisões arquiteturais relevantes são explicadas. Sugestões de refatoração vêm com os ganhos esperados. Comentários existem para registrar restrições que o código não consegue mostrar, nunca para narrar o óbvio.

## 13. Fluxo de revisão obrigatório

Revise em três passadas, nesta ordem, porque polir frase antes de consertar estrutura desperdiça a passada.

**Primeira passada, substância.** Confira os fatos, as datas, os números e as fontes, um a um, e verifique se o texto responde à pergunta central que ele mesmo prometeu responder. Depois passe estas travas:

- Todo símbolo de porcentagem aciona quatro conferências dentro da mesma frase: origem, data, método e denominador. Base pequena se conta em unidades, porque sem denominador "cresceu 300%" pode significar três clientes.
- Todo exemplo inventado carrega rótulo, inclusive cada saída de calculadora.
- Todo caso real tem nome e autorização.
- Nenhum dado foi fabricado para preencher lacuna, e nenhum marcador ficou pendente. Se ficou, ele está no lugar de um dado e não no lugar de uma seção, e o total de marcadores abertos não passa de cinco.
- Os seis itens do piso de substância (seção 2.1) estão presentes.
- Identificadores conferidos antes de citar: número de seção, código de documento, nome de arquivo. Abra e confirme, porque identificador errado se propaga sozinho para os derivados e para a página pública.

**Segunda passada, estrutura.** Confira o arco: a abertura instala situação e tensão sem adiar a promessa; o caso condutor aparece na abertura, volta no desenvolvimento e fecha no final; o fechamento retoma em vez de resumir. Confira a ordem dos blocos contra o gênero declarado na seção 3.2 e verifique se algum pedido de dado ou de dinheiro aparece antes da primeira prova. Quebre a simetria artificial: blocos com o mesmo número de frases do mesmo tamanho, tríades de exemplos usadas como ritmo e seções espelhadas se corrigem fundindo, cortando ou expandindo conforme o peso real de cada assunto. Confira se cada seção abre pela conclusão dela e se sustenta sozinha, e aplique o teste do parágrafo solto às frases de prova, de limite e de preço: envie a frase isolada para alguém que não viu o contexto e pergunte se ela se sustenta.

**Terceira passada, linguagem.** Ritmo dos períodos pelo diagnóstico da seção 4, aberturas de parágrafo todas distintas, conectivos cortados por subtração, estruturas proibidas da seção 5, vícios de português da seção 7, orçamento de formatação da seção 6 e tipografia à brasileira da seção 1.

Dois testes baratos fecham a revisão: a leitura em voz alta, porque frase que trava a língua trava o leitor, e a pergunta final "isso poderia ter saído de qualquer gerador de conteúdo corporativo?". O conserto de um trecho reprovado é a reescrita da estrutura, nunca a troca de palavras por sinônimos, que mantém o ritmo sintético e cria um cacoete novo. Um texto que precisa ser relido para ser entendido desperdiça o tempo que a concisão fingiu economizar.

Uma advertência final sobre ferramentas, que vale como regra de governança. Validador automático mede forma, nunca substância, e texto limpo de clichês com acentuação perfeita pode não ter tese nenhuma. Validador com correção automática precisa ser testado contra texto que se sabe correto antes de entrar em produção, porque falso positivo em corretor automático não custa atenção, custa a qualidade que ele deveria proteger. E configuração que ninguém lê não protege nada: antes de confiar num gate, verifique se o código realmente carrega o arquivo de regras.
