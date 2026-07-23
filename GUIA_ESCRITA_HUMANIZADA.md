# Guia de escrita humanizada

Anexo prático da `DIRETRIZ_EDITORIAL.md` (versão 2, 23 de julho de 2026). A diretriz define as regras; este guia mostra como aplicá-las, com exemplos antes e depois em português do Brasil, heurísticas mensuráveis e as fontes da pesquisa de junho e julho de 2026 que sustentam cada prática. Os exemplos são ilustrativos, criados para este guia.

## 1. Por que o problema mudou em 2026

As listas de palavras-dedo-duro de 2024 e 2025 ("delve", travessão, "robusto") perderam poder: humanos passaram a evitá-las e os modelos foram ajustados (o ChatGPT, por exemplo, passou a obedecer instruções de não usar travessão em novembro de 2025). O que persiste, mesmo nos modelos de 2026, são os padrões estruturais: ritmo uniforme, simetria de parágrafos, fórmulas de abertura e fechamento, atribuição vaga. A estilometria publicada em 2026 quantificou o mais forte deles: a dispersão do tamanho das frases em texto de modelo fica em torno de 5, contra cerca de 16 em texto humano. Ao mesmo tempo, a detecção virou recurso de plataforma (o Substack integrou um detector aberto a qualquer leitor em julho de 2026), o que torna o texto sintético um risco reputacional direto para quem publica.

A consequência prática: revisar léxico sem revisar estrutura não resolve. Este guia trata dos dois, nessa ordem de importância.

## 2. Ritmo: a heurística do bloco de dez frases

Pegue qualquer bloco de dez frases do texto. Subtraia o tamanho da menor do tamanho da maior. Amplitude abaixo de 15 palavras é forte indício de texto de máquina; acima de 30, compatível com escrita humana. Use como diagnóstico, nunca como alvo mecânico: a variação deve nascer do sentido.

Antes (amplitude 9; toda frase entre 14 e 23 palavras):

> A otimização para motores generativos exige uma abordagem estruturada e consistente ao longo do tempo. As empresas precisam entender como os modelos de linguagem selecionam as fontes que citam. A produção de conteúdo deve considerar tanto os leitores humanos quanto os sistemas automatizados. Os resultados costumam aparecer de forma gradual conforme a autoridade do domínio se consolida.

Depois (amplitude 33; a frase curta carrega a ênfase):

> Motores generativos não citam quem publica mais; citam quem oferece evidência extraível. Isso muda o trabalho. Em vez de calibrar densidade de palavra-chave, a equipe passa a garantir que cada seção tenha uma definição clara, um número datado com fonte e uma comparação que um modelo consiga recortar sem perder o sentido, porque é esse recorte que aparece na resposta.

## 3. Vícios de português de LLM: antes e depois

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

## 4. Estrutura: o que cortar primeiro num rascunho de IA

A ordem de corte que os fluxos editoriais de 2026 recomendam, do mais nocivo ao menos:

1. Abertura de cenário genérica ("No cenário atual em constante evolução da inteligência artificial...") e meta-comentário ("Neste artigo vamos explorar..."). O texto começa na primeira informação que o leitor não tinha.
2. Parágrafo-recap final que apenas resume o que acabou de ser dito e fecho pseudo-profundo ("O futuro da busca não está chegando. Já chegou."). Se o fecho não acrescenta consequência ou próximo passo, o texto termina no parágrafo anterior.
3. Séries de bullets "termo em negrito: explicação" onde os itens têm relação de causa entre si. Convertem-se em prosa, porque a lista esconde o encadeamento.
4. Seções espelhadas (toda seção com o mesmo número de parágrafos do mesmo tamanho) e tríades mecânicas. Quebra-se a simetria fundindo, cortando ou expandindo pelo peso real de cada assunto.
5. Conectivos de abertura de parágrafo. Deletar, não substituir: na maioria dos casos a transição já está implícita na lógica.

## 5. Orçamento de formatação por texto

Cotas que funcionam como regra de casa em system prompts editoriais publicados em 2026, ajustadas ao veto de travessão desta diretriz: zero travessão; no máximo uma analogia por peça; negrito apenas em termos que o leitor precisará reencontrar ao escanear a página; listas somente para conteúdo genuinamente enumerável (passos, requisitos, inventários), nunca para argumentação; no máximo um bloco de lista a cada tela de texto. Estourou o orçamento, reescreve-se em prosa.

## 6. Fluxo de revisão em três passadas

1. Substância: fatos, datas, números e fontes conferidos; a pergunta central do texto respondida; nenhum dado inventado; slots `[PREENCHER-HUMANO]` resolvidos com o autor (caso vivido, número proprietário, posição de negócio) ou o trecho cortado.
2. Estrutura: seção 4 deste guia aplicada; cápsula de resposta presente na abertura de cada seção; headings que são perguntas reais do público; nenhuma seção que não se sustente sozinha.
3. Linguagem: heurística do bloco de dez frases; aberturas de parágrafo todas distintas; conectivos cortados; tabela da seção 3 varrida; orçamento de formatação da seção 5 conferido; leitura em voz alta do texto inteiro.

O conserto de trecho reprovado é reescrita de estrutura. Troca de sinônimo mantém o ritmo de máquina e ainda cria o cacoete novo do vocabulário artificialmente variado.

## 7. O que não fazer (modinhas sem evidência)

- "Humanizadores" automáticos para burlar detector: pesquisa de abril de 2026 mostrou que texto ajustado para evadir detecção continua distinguível por leitores humanos. Passar no detector e parecer humano são coisas diferentes.
- Perseguir score de burstiness como alvo: alternância mecânica curta-longa-curta soa tão artificial quanto a uniformidade.
- O prompt mágico único ("escreva como humano"): sem restrições estruturais concretas, o modelo devolve o mesmo template com verniz informal.
- Detector de IA como portão de publicação: falsos positivos são altos; o uso recomendado em 2026 é sinal de apoio na revisão, nunca rejeição automática.
- Substituição de vocabulário em massa mantendo a estrutura: ver seção 6.
- Fragmentar páginas e criar arquivos "para IA ler" como estratégia principal de citação: o guia oficial do Google de maio de 2026 desmente a necessidade; um estudo de 300 mil domínios não achou correlação entre llms.txt e citação.

## 8. Fontes principais da pesquisa (data real de cada uma)

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

Lacuna declarada: não existe, até julho de 2026, estudo de corpus acadêmico sobre marcadores de LLM específicos do português brasileiro; a tabela da seção 3 consolida convergência entre fontes de mercado brasileiras e os achados de corpus em inglês. Quando um estudo desses aparecer, este guia deve ser revisado contra ele.
