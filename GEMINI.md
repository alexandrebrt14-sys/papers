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
