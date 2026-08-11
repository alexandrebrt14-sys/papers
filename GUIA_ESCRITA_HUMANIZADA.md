# Guia de escrita humanizada

Anexo prático da `DIRETRIZ_EDITORIAL.md` (versão 4, 11 de agosto de 2026). A diretriz define as regras; este guia mostra como aplicá-las, com exemplos antes e depois em português do Brasil, heurísticas mensuráveis e as fontes da pesquisa de junho e julho de 2026 que sustentam cada prática. Os exemplos são ilustrativos, criados para este guia.

A versão 3 acrescentou a seção 3, sobre narrativa, e endureceu o veto a cotas mecânicas de ritmo (seções 2 e 8), depois que a geração anterior dos prompts deste repositório produziu o defeito oposto ao que pretendia corrigir.

## 1. Por que o problema mudou em 2026

As listas de palavras-dedo-duro de 2024 e 2025 ("delve", travessão, "robusto") perderam poder: humanos passaram a evitá-las e os modelos foram ajustados (o ChatGPT, por exemplo, passou a obedecer instruções de não usar travessão em novembro de 2025). O que persiste, mesmo nos modelos de 2026, são os padrões estruturais: ritmo uniforme, simetria de parágrafos, fórmulas de abertura e fechamento, atribuição vaga. A estilometria publicada em 2026 quantificou o mais forte deles: a dispersão do tamanho das frases em texto de modelo fica em torno de 5, contra cerca de 16 em texto humano. Ao mesmo tempo, a detecção virou recurso de plataforma (o Substack integrou um detector aberto a qualquer leitor em julho de 2026), o que torna o texto sintético um risco reputacional direto para quem publica.

A consequência prática: revisar léxico sem revisar estrutura não resolve. Este guia trata dos dois, nessa ordem de importância.

## 2. Ritmo: diagnóstico, nunca fórmula

Pegue qualquer bloco de dez frases do texto. Subtraia o tamanho da menor do tamanho da maior. Amplitude abaixo de 15 palavras é forte indício de texto de máquina; acima de 30, compatível com escrita humana. O teste se aplica ao texto pronto, para localizar o trecho que precisa de reescrita. Ele não vira regra de produção.

Uma armadilha aritmética explica por que a versão anterior desta doutrina não funcionava. Se o guia manda o parágrafo abrir curto e crescer, digamos, uma palavra e meia por frase, e ao mesmo tempo raciona a frase de veredito em uma por bloco, um bloco que abre em 11 palavras chega à décima frase perto de 24. A amplitude resultante fica em 13, ou 16 contando a frase curta de fechamento, e o mesmo documento que prescreveu o crescimento reprova o resultado por amplitude insuficiente. Três regras derrubavam a quarta, e o texto produzido por quem tentava obedecer às quatro era justamente o de faixa estreita que a diretriz classifica como assinatura de máquina. Daí a regra da seção 4.1 da diretriz: este diagnóstico não se combina com nenhuma outra regra de comprimento.

Antes (amplitude 9; toda frase entre 14 e 23 palavras):

> A otimização para motores generativos exige uma abordagem estruturada e consistente ao longo do tempo. As empresas precisam entender como os modelos de linguagem selecionam as fontes que citam. A produção de conteúdo deve considerar tanto os leitores humanos quanto os sistemas automatizados. Os resultados costumam aparecer de forma gradual conforme a autoridade do domínio se consolida.

Correção errada (a métrica melhora, o texto piora):

> Motores generativos escolhem fontes. Isso muda tudo. A equipe precisa entender o critério de seleção antes de escrever qualquer linha de conteúdo novo. O ganho é real. Vale investir.

Cinco frases, três delas curtas de enchimento, nenhuma informação nova. É o staccato de manchete: passa no teste de amplitude e continua soando a máquina, porque a ênfase virou rotina e a rotina se percebe na leitura.

Depois (amplitude 33; a frase curta carrega a ênfase porque há o que enfatizar):

> Motores generativos não citam quem publica mais; citam quem oferece evidência extraível. Isso muda o trabalho. Em vez de calibrar densidade de palavra-chave, a equipe passa a garantir que cada seção tenha uma definição clara, um número datado com fonte e uma comparação que um modelo consiga recortar sem perder o sentido, porque é esse recorte que aparece na resposta.

## 3. Narrativa: o que separa texto lido de texto abandonado

Profundidade que ninguém lê não ensina nada. As técnicas abaixo são as que a diretriz (seção 3) torna obrigatórias em conteúdo longo, com o efeito de cada uma.

| Técnica | O que fazer | Efeito |
|---|---|---|
| Abertura em situação | Comece por cena, caso ou número que contraria a expectativa. A definição vem depois. | O leitor entende por que o tema é dele antes de receber teoria |
| Tensão antes da solução | Explicite o custo de errar, o prazo, o que se perde ao ignorar. | Transforma catálogo de conceitos em problema a resolver |
| Caso condutor | Um caso nomeado atravessa o texto e reaparece nos exemplos. | Dá continuidade e memória ao argumento |
| Loop honesto | A promessa da abertura é paga no desenvolvimento. | Sustenta a leitura sem recorrer a isca |
| Fechamento com callback | O final retoma a abertura e mostra o que mudou. | Substitui o parágrafo-recap proibido |
| Mostrar em vez de qualificar | Prejuízo, prazo e consequência em número, no lugar do adjetivo. | O leitor conclui sozinho, e conclusão própria persuade |

Antes (abre em definição, sem tensão, sem caso):

> A governança de dados é um conjunto de políticas, processos e responsabilidades que garante a qualidade e a segurança das informações corporativas. Empresas que implementam governança de dados obtêm melhores resultados em seus projetos de análise e inteligência artificial.

Depois (abre em situação, instala tensão, ancora em caso e mostra em vez de qualificar):

> O projeto de precificação dinâmica de uma rede varejista com 120 lojas parou por seis semanas em 2025. O modelo estava pronto; o cadastro de produtos, não. Três sistemas divergiam sobre o preço vigente do mesmo item, e ninguém tinha autoridade formal para decidir qual deles valia. Governança de dados é exatamente isso que faltava ali: a definição de quem responde por cada dado e sob qual regra, antes que o dado vire insumo de decisão automática.

O limite, que vale como regra: a história serve ao argumento. Drama fabricado, suspense artificial e anedota que não sustenta a tese saem do texto junto com os clichês.

## 4. Vícios de português de LLM: antes e depois

| Vício | Antes | Depois |
|---|---|---|
| Gerundismo | Vamos estar enviando o relatório amanhã. | Enviaremos o relatório amanhã. |
| "Endereçar" (calque de address) | O time vai endereçar o problema de latência. | O time vai resolver o problema de latência. |
| "Suportar" (calque de support) | A plataforma suporta três idiomas. | A plataforma aceita três idiomas. |
| "Eventualmente" (calque de eventually) | Eventualmente o cache expira e o dado é recarregado. | Mais cedo ou mais tarde o cache expira e o dado é recarregado. |
| "Assumir" (calque de assume) | Assumimos que o usuário já está logado. | Presumimos que o usuário já está logado. |
| Adjetivo vazio | Uma solução robusta e escalável para um desafio crucial. | Uma solução que aguentou 40 mil requisições por minuto no pico de novembro sem fila. |
| Inflação de significância | O lançamento marca um momento crucial na jornada da empresa. | Com o lançamento, a empresa passa a atender o segmento que respondia por 60% dos pedidos recusados. |
| Fuga da cópula | A ferramenta serve como ponto central de observabilidade. | A ferramenta é o ponto central de observabilidade. |
| Gerúndio analítico vago | O programa foi expandido, contribuindo para o fortalecimento do ecossistema. | O programa foi expandido e o ecossistema ganhou 12 fornecedores certificados. |
| Atribuição vaga | Especialistas apontam que a busca por IA vai crescer. | O relatório da empresa X, de maio de 2026, projeta crescimento de N% na busca por IA. |
| Passiva nominalizada | Foi realizada a implementação da validação dos formulários. | Implementamos a validação dos formulários. |
| Vírgula de Oxford | O sistema exporta CSV, JSON, e XML. | O sistema exporta CSV, JSON e XML. |
| Title case | Como Montar uma Estratégia de Conteúdo Para IA | Como montar uma estratégia de conteúdo para IA |
| Calque "não é sobre X" | Não é sobre tecnologia, é sobre pessoas. | A tecnologia é o meio; a decisão continua sendo das pessoas. |

## 5. Estrutura: o que cortar primeiro num rascunho de IA

A ordem de corte que os fluxos editoriais de 2026 recomendam, do mais nocivo ao menos:

1. Abertura de cenário genérica ("No cenário atual em constante evolução da inteligência artificial...") e meta-comentário ("Neste artigo vamos explorar..."). O texto começa na primeira informação que o leitor não tinha, e a seção 3 diz com o que substituir.
2. Parágrafo-recap final que apenas resume o que acabou de ser dito e fecho pseudo-profundo ("O futuro da busca não está chegando. Já chegou."). O lugar dele é o callback da seção 3.
3. Séries de bullets "termo em negrito: explicação" onde os itens têm relação de causa entre si. Convertem-se em prosa, porque a lista esconde o encadeamento.
4. Seções espelhadas (toda seção com o mesmo número de parágrafos do mesmo tamanho) e tríades mecânicas. Quebra-se a simetria fundindo, cortando ou expandindo pelo peso real de cada assunto.
5. Conectivos de abertura de parágrafo. Deletar, não substituir: na maioria dos casos a transição já está implícita na lógica.

## 6. Orçamento de formatação por texto

Cotas que funcionam como regra de casa em system prompts editoriais publicados em 2026, ajustadas ao veto de travessão desta diretriz: zero travessão; no máximo uma analogia por peça; negrito apenas em termos que o leitor precisará reencontrar ao escanear a página; no máximo um bloco de lista a cada tela de texto. Estourou o orçamento, reescreve-se em prosa.

O orçamento limita o excesso, não o uso. Tabela comparativa, matriz de decisão, checklist e lista de passos são ferramentas de consultoria e entram sempre que houver alternativas com critérios, escolha a fazer ou passos verificáveis: um profissional decide mais rápido com uma matriz bem construída do que com três parágrafos equivalentes. O que sai é a lista que substitui argumentação, aquela cujos itens têm relação de causa entre si. Prosa carrega raciocínio; estrutura carrega comparação, sequência e verificação.

## 7. Fluxo de revisão em três passadas

Antes de tudo, uma conta que se faz na fase de apuração e não na revisão: quantos blocos da peça afirmam resultado e quantas provas datadas existem para sustentá-los. Se as afirmações passarem das provas, o conserto acontece antes da redação, reduzindo afirmação ou buscando origem, porque revisar uma peça superdimensionada é reescrevê-la inteira. As quatro saídas na falta de prova, na ordem: pesquisar a origem, reduzir a afirmação ao tamanho do que se sabe, restringir o uso, segurar a publicação. Só depois entra o marcador, sempre no lugar do dado e nunca no lugar da seção, com teto de cinco por documento.

Antes das três passadas, uma verificação que nenhum gate automático faz: os seis itens do piso de substância (diretriz, seção 2.1). Tese identificável, evidência ligada à tese, ganho de informação, critério de decisão, arco de leitura e consequência para o leitor. Os validadores do repositório medem forma, e forma limpa em texto vazio continua sendo texto vazio.

1. Substância: os seis itens acima; fatos, datas, números e fontes conferidos; a pergunta central do texto respondida; nenhum dado inventado; slots `[PREENCHER-HUMANO]` resolvidos com o autor (caso vivido, número proprietário, posição de negócio) ou o trecho cortado.
2. Estrutura: seções 3 e 5 deste guia aplicadas; arco narrativo verificado (a abertura prende, a promessa é paga, o fechamento retoma); cápsula de resposta presente na abertura de cada seção interna; headings que são perguntas reais do público; nenhuma seção que não se sustente sozinha.
3. Linguagem: heurística do bloco de dez frases; aberturas de parágrafo todas distintas; conectivos cortados; tabela da seção 4 varrida; orçamento de formatação da seção 6 conferido; leitura em voz alta do texto inteiro.

Duas travas merecem atenção separada, porque são as que mais escapam. Todo símbolo de porcentagem dispara quatro conferências dentro da mesma frase: origem, data, método e denominador. Base pequena se conta em unidades, já que sem denominador "cresceu 300%" pode significar três clientes. E o teste do parágrafo solto vale para toda frase de prova, de limite e de preço: leia a frase isolada, sem o contexto em volta, e pergunte se ela se sustenta. Público, condição e exceção precisam viajar dentro da mesma sentença, porque um "não serve para X" recortado sem o "somente" chega ao leitor como "serve", e é assim que o trecho viaja quando alguém tira um print.

O conserto de trecho reprovado é reescrita de estrutura. Troca de sinônimo mantém o ritmo de máquina e ainda cria o cacoete novo do vocabulário artificialmente variado.

## 8. O que não fazer (modinhas sem evidência)

- "Humanizadores" automáticos para burlar detector: pesquisa de abril de 2026 mostrou que texto ajustado para evadir detecção continua distinguível por leitores humanos. Passar no detector e parecer humano são coisas diferentes.
- Cota de ritmo em prompt ou em revisão: "uma frase curta por parágrafo", "nunca duas frases seguidas na mesma faixa de comprimento", "parágrafo com no máximo cinco linhas". Foi o que degradou a geração anterior dos prompts deste repositório. A cota melhora a estatística e produz staccato, fatiamento e ênfase gasta; o diagnóstico da seção 2 substitui todas elas.
- Perseguir score de burstiness como alvo: alternância mecânica curta-longa-curta soa tão artificial quanto a uniformidade.
- O prompt mágico único ("escreva como humano"): sem restrições estruturais concretas, o modelo devolve o mesmo template com verniz informal.
- Detector de IA como portão de publicação: falsos positivos são altos; o uso recomendado em 2026 é sinal de apoio na revisão, nunca rejeição automática.
- Substituição de vocabulário em massa mantendo a estrutura: ver seção 7.
- Fragmentar páginas e criar arquivos "para IA ler" como estratégia principal de citação: o guia oficial do Google de maio de 2026 desmente a necessidade; um estudo de 300 mil domínios não achou correlação entre llms.txt e citação.

## 9. Fontes principais da pesquisa (data real de cada uma)

1. TextSight, "Sentence Length Variance", 22/06/2026. https://www.textsight.ai/blog/sentence-length-variance/
2. The Visual Communication Guy, "How Content Teams Can Build a Reliable AI Writing Review Process", 17/07/2026. https://thevisualcommunicationguy.com/2026/07/17/how-content-teams-can-build-a-reliable-ai-writing-review-process/
3. Wikipedia, "Signs of AI writing" (catálogo vivo do WikiProject AI Cleanup, revisões ao longo de 2026). https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
4. Bloomberry, "AI Sentence DNA" (corpus com 7.622 entradas, auditado em junho de 2026). https://www.bloomberry.ai/research/ai-writing-patterns
5. Przystalski et al., "Stylometric detection of AI-generated texts", Digital Scholarship in the Humanities, Oxford, 2026 (dispersão ~5 vs ~16). https://academic.oup.com/dsh/advance-article/doi/10.1093/llc/fqag064/8714041
6. Tabach, "Can Humans Detect AI?", arXiv, 25/04/2026 (evasão de detector não engana leitor). https://arxiv.org/abs/2604.23471
7. TechCrunch, "Substack's new tool tells you who's been writing their newsletters with AI", 22/07/2026. https://techcrunch.com/2026/07/22/substacks-new-tool-tells-you-whos-been-writing-their-newsletters-with-ai/
8. Envox, "Os 12 maiores vícios de linguagem de IA em 2026", 23/02/2026. https://envox.com.br/marketing-de-conteudo/vicios-linguagem-ia-2026-exemplos-reais/agencia-de-marketing-digital/trafego-pago/vendas/
9. Meio & Mensagem, "Como são as políticas e diretrizes de IA das redações", 05/01/2026. https://www.meioemensagem.com.br/midia/como-sao-as-politicas-e-diretrizes-de-ia-das-redacoes
10. CBL, "Manual de Boas Práticas de IA" do setor editorial brasileiro, 14/05/2026. https://cbl.org.br/2026/05/cbl-lanca-manual-de-boas-praticas-de-ia-para-orientar-editoras-brasileiras-no-uso-etico-da-inteligencia-artificial/
11. Google Search Central, "Optimizing your website for generative AI features", maio de 2026. https://developers.google.com/search/docs/fundamentals/ai-optimization-guide
12. Martinez, "Critical Survey of Generative Engine Optimization (2023-2026)", arXiv, 15/07/2026. https://arxiv.org/abs/2607.14035
13. "From Citation Selection to Citation Absorption", arXiv, 28/04/2026 (evidência extraível como fator de citação). https://arxiv.org/abs/2604.25707
14. Eduardo Martins, "Manual de Redação e Estilo de O Estado de S. Paulo" (referência permanente de prosa direta brasileira). https://fasam.edu.br/wp-content/uploads/2020/07/Manual-de-Reda%C3%A7%C3%A3o-e-Estilo-Estad%C3%A3o.pdf

Lacuna declarada: não existe, até julho de 2026, estudo de corpus acadêmico sobre marcadores de LLM específicos do português brasileiro; a tabela da seção 4 consolida convergência entre fontes de mercado brasileiras e os achados de corpus em inglês. Quando um estudo desses aparecer, este guia deve ser revisado contra ele.
