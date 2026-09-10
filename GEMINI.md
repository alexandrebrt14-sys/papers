# GEMINI.md

## Padrão editorial obrigatório

Antes de produzir qualquer texto de leitura humana neste repositório (documentação, onda de pesquisa, síntese, relatório, rascunho de divulgação, descrição de PR, mensagem longa de commit), leia e aplique a cadeia que vive na raiz: `DIRETRIZ_EDITORIAL.md` é a regra (versão 4, de 11 de agosto de 2026), `GUIA_ESCRITA_HUMANIZADA.md` é o anexo prático com exemplos antes e depois, heurísticas mensuráveis e fontes, e `DOUTRINA_EDITORIAL_NESTE_REPO.md` é a tradução da doutrina para o escopo deste pipeline de pesquisa. Os três documentos prevalecem sobre este resumo.

A v4 substituiu a v2, de 23 de julho de 2026, que era construída quase só de proibições e cujo efeito medido foi texto curto e sem argumento aprovado em todos os gates. O que mudou:

- **Piso de substância** (seção 2.1). Toda peça precisa ter tese identificável com a qual daria para discordar, evidência ligada a essa tese, ganho de informação, critério de decisão explícito quando houver alternativas, arco de leitura e consequência prática para quem lê. Peça que falha em um dos seis itens é reescrita, não aparada. Aprovação em gate automático nunca é aprovação editorial.
- **Prova antes da escrita** (seção 2.2). A evidência se levanta antes da primeira frase e limita o tamanho da peça: blocos que afirmam resultado não passam do número de provas datadas disponíveis. Na falta de prova, quatro saídas antes do marcador (pesquisar, reduzir a afirmação, restringir o uso, segurar a publicação), com teto de cinco marcadores abertos por documento.
- **Narrativa obrigatória** (seção 3). Abertura em situação e não em definição, tensão antes da solução, caso condutor com rótulo de tipo, promessa paga no desenvolvimento, fechamento com callback em vez de recapitulação, mostrar em vez de qualificar, e um pedido por peça.
- **Estrutura visual como ferramenta legítima** (seção 6). Tabela comparativa, matriz de decisão e checklist entram sempre que ajudarem de verdade. Sai a lista que faz o trabalho de argumentar.
- **Revisão em três passadas com travas verificáveis** (seção 13), entre elas as quatro conferências que todo símbolo de porcentagem dispara: origem, data, método e denominador na mesma frase. Base pequena se conta em unidades.
- **Nenhuma cota mecânica de ritmo, em direção alguma** (seção 4, item 8). A amplitude num bloco de dez frases é diagnóstico do texto pronto, com defeito abaixo de 15 palavras e conforto acima de 30, e nunca fórmula de produção nem contagem durante a escrita.

Permanecem valendo: português do Brasil com acentuação completa, tipografia à brasileira (sem title case, números de zero a dez por extenso, vírgula decimal), travessão vetado em prosa, atribuição nomeada em vez de "estudos mostram", zero emoji, parágrafos justificados em HTML e PDF, e nada de dado inventado.

Aplicação específica deste repositório, detalhada em `DOUTRINA_EDITORIAL_NESTE_REPO.md`: os prompts de coleta em `src/config.py`, `src/shared/llm_utils.py`, `src/config_v2.py` e `src/collectors/prompt_sensitivity.py` são instrumento de medição da série longitudinal e não recebem regra editorial, porque mudá-los altera o tratamento experimental. Prompt que redige texto em português carrega o bloco condensado de `scripts/prompts/BLOCO_EDITORIAL_PROMPT.md` dentro da própria demanda, já que instrução vista só no contexto não sobrevive a geração longa.

Convenção explícita deste repositório prevalece sobre convenção genérica, com a única ressalva de segurança e corretude.

## Conhecimento científico vigente de SEO e IA

Atualização de 10/09/2026: antes de interpretar métricas, desenhar estudos ou integrar literatura de SEO e busca com IA, ler a [base de conhecimento](docs/GEO_KNOWLEDGE_BASE_2026.md), o [sistema operacional](docs/GEO_OPERATING_SYSTEM.md) e o [canônico de setembro-10](docs/research/geo-wave-setembro-10-2026/GEO_WAVE_SETEMBRO_10_2026_CANONICAL.md). O [guia científico](docs/research/geo-wave-setembro-10-2026/GUIA_CONCEITOS_SEO_IA_PESQUISA.md) explica operacionalização, denominadores e ameaças à validade.

A taxonomia contém **63 conceitos**, preservando os IDs de 1 a 50. Classificar somente os conceitos pertinentes. Não exigir cobertura dos 14 eixos nos prompts experimentais nem inserir regras de SEO/editoriais no estímulo longitudinal. A [metodologia v2, seção 13](docs/METHODOLOGY_V2.md) esclarece as proxies locais sem mudar H1 a H5 ou o instrumento.

Survey não é peso de ranking; associação não é efeito; menção não é sustentação semântica; fonte exposta não é log de recuperação. O comparador opcional usa Brave e domínios, não Google e ranking de entidades. Coluna existente não comprova métrica calculada. P-SEO-01 a P-SEO-05 são propostas, sem execução ou pré-registro concluído nesta integração.

Em conflito conceitual, setembro-10 prevalece sobre ondas anteriores. Protocolos e estratos históricos continuam regidos pela versão em que foram executados. Não sobrescrever dados, reformular prompts, alterar cache, iniciar coleta paga ou trocar parâmetros como consequência de uma atualização de conhecimento.
