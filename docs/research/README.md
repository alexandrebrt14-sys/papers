# docs/research

Ondas de pesquisa e sínteses canônicas. As pastas guardam documentos canônicos em português e registros de proveniência. Quando disponível, a subpasta `raw/` contém o material bruto que originou a onda (retorno de Perplexity, board do orchestrator, capturas de arXiv, saídas de script de pesquisa).

Regra editorial vigente, versão 4 de 11 de agosto de 2026, na raiz do repositório: `DIRETRIZ_EDITORIAL.md` (regra), `GUIA_ESCRITA_HUMANIZADA.md` (exemplo prático) e `DOUTRINA_EDITORIAL_NESTE_REPO.md` (tradução para este pipeline, com as quatro conferências de porcentagem, a validação de identificador e o tratamento das lacunas).

Quatro exigências específicas de onda de pesquisa, que a doutrina geral cobre e aqui se aplicam todo dia:

1. `raw/` é rastro de apuração, nunca fonte primária no texto. Log de wave, síntese de orchestrator e resposta de LLM entram como registro de como o achado apareceu; o que a frase cita é a publicação que alguém abriu.
2. Identificador se abre antes de canonizar. Nenhum arXiv ID entra num documento canônico sem que `arxiv.org/abs/<id>` tenha sido aberto e o título confira. O repositório já recebeu de um modelo de deep research os IDs `2603.04567` e `2605.11203`, nenhum dos dois confirmado ao abrir a página `abs`, e essa verificação foi a única barreira que funcionou.
3. Atribuição nomeada, com data. "A literatura indica" é defeito grave numa pasta onde o identificador está na tela; escreva autor ou grupo, ano e ID.
4. Número de terceiro carrega a medida junto: qual amostra, qual período, qual método, qual denominador. Achado sem essas quatro informações fica em quarentena com `[FALTA EVIDÊNCIA: ...]` até a verificação, e não vira parágrafo antes disso.

Quando a onda for gerada por prompt de LLM, o prompt carrega o bloco condensado de `scripts/prompts/BLOCO_EDITORIAL_PROMPT.md` dentro da própria demanda. Referência por link não funciona em geração longa: o modelo não abre o arquivo e escreve fora do padrão.

## Integração vigente de 10/09/2026

A [onda de setembro-10](geo-wave-setembro-10-2026/GEO_WAVE_SETEMBRO_10_2026_CANONICAL.md) incorpora a pesquisa de fatores de ranking da Zyppy e os conceitos modernos de SEO e IA ao desenho científico do `papers`. Contém [guia aprofundado](geo-wave-setembro-10-2026/GUIA_CONCEITOS_SEO_IA_PESQUISA.md), [relatório com 30 fontes](geo-wave-setembro-10-2026/relatorio-seo-ia-query-fan-out.md) e [registro das 24 consultas originais](geo-wave-setembro-10-2026/registro-query-fan-out.md), transferidos com proveniência do `landing-page-geo`.

Esta onda distingue código implementado, proxies e propostas; amplia a taxonomia para 63 conceitos e prevalece sobre recomendações conceituais conflitantes anteriores. O protocolo da série longitudinal e os registros históricos são preservados. O registro de buscas serve como rastro da investigação, sem necessidade de criar uma pasta `raw/` vazia ou apresentar a síntese como fonte primária.
