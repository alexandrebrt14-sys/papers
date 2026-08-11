# docs/research

Ondas de pesquisa e sínteses canônicas. Cada pasta guarda um documento canônico em português e uma subpasta `raw/` com o material bruto que o originou (retorno de Perplexity, board do orchestrator, capturas de arXiv, saídas de script de pesquisa).

Regra editorial vigente, versão 4 de 11 de agosto de 2026, na raiz do repositório: `DIRETRIZ_EDITORIAL.md` (regra), `GUIA_ESCRITA_HUMANIZADA.md` (exemplo prático) e `DOUTRINA_EDITORIAL_NESTE_REPO.md` (tradução para este pipeline, com as quatro conferências de porcentagem, a validação de identificador e o tratamento das lacunas).

Quatro exigências específicas de onda de pesquisa, que a doutrina geral cobre e aqui se aplicam todo dia:

1. `raw/` é rastro de apuração, nunca fonte primária no texto. Log de wave, síntese de orchestrator e resposta de LLM entram como registro de como o achado apareceu; o que a frase cita é a publicação que alguém abriu.
2. Identificador se abre antes de canonizar. Nenhum arXiv ID entra num documento canônico sem que `arxiv.org/abs/<id>` tenha sido aberto e o título confira. O repositório já recebeu de um modelo de deep research os IDs `2603.04567` e `2605.11203`, nenhum dos dois confirmado ao abrir a página `abs`, e essa verificação foi a única barreira que funcionou.
3. Atribuição nomeada, com data. "A literatura indica" é defeito grave numa pasta onde o identificador está na tela; escreva autor ou grupo, ano e ID.
4. Número de terceiro carrega a medida junto: qual amostra, qual período, qual método, qual denominador. Achado sem essas quatro informações fica em quarentena com `[FALTA EVIDÊNCIA: ...]` até a verificação, e não vira parágrafo antes disso.

Quando a onda for gerada por prompt de LLM, o prompt carrega o bloco condensado de `scripts/prompts/BLOCO_EDITORIAL_PROMPT.md` dentro da própria demanda. Referência por link não funciona em geração longa: o modelo não abre o arquivo e escreve fora do padrão.
