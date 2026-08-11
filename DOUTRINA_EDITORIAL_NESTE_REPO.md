# Doutrina editorial aplicada ao repositório papers

Tradução local da versão 4 da `DIRETRIZ_EDITORIAL.md` (11 de agosto de 2026) para o trabalho concreto deste pipeline. A regra vive na diretriz, o exemplo prático vive no `GUIA_ESCRITA_HUMANIZADA.md`, e este anexo cobre apenas o que muda quando o texto nasce de coleta automatizada e de leitura de paper. Nada aqui substitui os dois documentos da cadeia.

Em 10 de agosto de 2026 o painel público deste projeto anunciava "dia 90 de 90" da janela longitudinal. O banco tinha 41 dias com linha e um vazio de 59, porque a contagem somava dias de calendário em vez de dias que produziram dado. O número existia, o cálculo rodava sozinho todo dia e ninguém tinha olhado a definição do denominador. A correção está registrada em `scripts/window_progress.py`, e o episódio é o caso condutor deste anexo. Num repositório de pesquisa o defeito editorial mais comum é a prova publicada sem a definição que a torna interpretável, e não a falta de prova.

## A evidência existe por construção; a proveniência é que falta

A seção 2.2 da diretriz manda levantar o material de prova antes da primeira frase. Aqui essa lista já existe: `data/papers.db`, os rollups em `output/reports/`, os raws de cada wave em `docs/research/*/raw/` e os JSON de proveniência que acompanham cada onda de pesquisa. A regra que morde neste repositório é a outra metade da mesma seção, a de proveniência completa por número: origem, data, método e denominador dentro da mesma frase em que o número aparece, porque é a frase, não a seção, que viaja quando alguém recorta um trecho para um slide ou para um post.

A conta de dimensionamento continua valendo nas peças derivadas. Quando um resultado do banco vira rascunho em `drafts/` ou página em `docs/research/`, o número de blocos que afirmam resultado precisa ser menor ou igual ao número de resultados datados que existem hoje no banco. Onda de pesquisa com quatro achados verificados e nove parágrafos de conclusão está declarando que cinco parágrafos são adjetivo.

O aviso sobre número medido no registro errado tem um caso caro na história do repo. Até a auditoria de junho de 2026, quatro dos cinco coletores gravavam `response_text` truncado em 200 caracteres, e o NER media citação apenas na abertura da resposta. A taxa medida ali não é taxa de citação plena, é citação em abertura, e nomear a métrica pelo que ela mede de fato foi o que salvou o paper de uma afirmação insustentável em revisão por pares.

## As quatro conferências que todo símbolo de porcentagem dispara

Antes de publicar qualquer porcentagem vinda do banco, confira quatro coisas dentro da mesma frase: qual amostra, qual período, qual método e qual denominador. Uma frase que passa nas quatro fica assim: "no núcleo de 50.453 observações coletadas entre 23 de abril e 9 de junho de 2026, com citação espontânea detectada por NER v2, a fintech aparece em 28,15% das consultas do vertical". Uma frase que reprova nas quatro fica assim: "a fintech lidera com 28,15%".

Base pequena se conta em unidades, sem exceção. Suponha três acertos em quarenta tentativas de decoy: o relato correto é três em quarenta, nunca "7,5% de falso positivo", porque a porcentagem em base curta transmite precisão que a amostra não tem. O mesmo vale para variação entre semanas de coleta: quando o denominador semanal cai, a variação percentual cresce sozinha e não descreve mudança de comportamento do modelo.

## Atribuição nomeada, com o identificador em mãos

"Estudos mostram" e "a literatura indica" são defeito grave neste repositório, e a razão é específica: quem escreve aqui tem o identificador aberto na tela. Diga qual estudo, de quem e de quando. A forma mínima aceitável cita autor ou grupo, ano e identificador, como em "Wen et al., ICML 2026 Position Track, `2606.12439`" ou "What Gets Cited, 252 mil ensaios pareados, `2605.25517`". Quando o achado for do próprio grupo, o mesmo rigor vale para a peça companheira: nome do paper, data e DOI ou link do depósito.

## Identificador se abre e se confere antes de entrar no texto

DOI, arXiv ID, número de seção e nome de arquivo se validam antes da citação, um por um, porque identificador errado se propaga sozinho. Ele sai do rascunho para a tabela do paper, da tabela para o `CITATIONS_POOL.md`, do pool para a página pública, e cada salto ganha uma aparência maior de verificado sem que ninguém tenha aberto nada. O repo já tem o registro de onde isso começa: em junho de 2026 o `sonar-deep-research` devolveu os IDs `2603.04567` e `2605.11203`, e nenhum dos dois se confirmou. A única barreira que funcionou foi abrir `arxiv.org/abs/<id>` um por um antes de canonizar.

Duas notas operacionais evitam falso alarme e falsa tranquilidade. HTTP 403 do `doi.org` significa cliente automatizado bloqueado, nunca DOI morto: confira pela API do Crossref ou pelo navegador antes de declarar identificador inválido. E validar sintaxe não é validar existência, porque um ID inventado costuma ter formato perfeito; a conferência só conta quando a página de destino abre e o título casa com o que o texto afirma.

## Intermediário não vira fonte primária

Log de wave, síntese do orchestrator, resumo de terceiro e resposta de LLM são insumo de apuração. Nenhum deles entra no texto final ocupando o lugar da publicação original. Os arquivos em `docs/research/*/raw/` existem para dar rastro do que foi lido e por qual caminho, e o que aparece na frase citável é a fonte que alguém abriu. A regra tem consequência prática no fluxo de ondas: quando a rodada de pesquisa devolve um número interessante sem link primário, o número fica em quarentena até a verificação, e não vira parágrafo antes disso.

## Onde entra cada marcador de lacuna

`[FALTA EVIDÊNCIA: o que buscar]` marca o que a etapa seguinte do pipeline resolve com trabalho: uma consulta nova ao banco, uma busca em fonte viva, a leitura de um `abs` ainda não aberto. `[PREENCHER-HUMANO: o que falta]` marca o que só o autor tem: autorização para nomear cliente, número proprietário fora do banco, decisão de posicionamento, escolha de venue. O teto é de cinco marcadores abertos por documento, e acima disso a peça não está pronta para revisão, está pedindo apuração. Nenhum dos dois autoriza estimativa: em repositório que publica dataset aberto, número inventado contamina retroativamente tudo o que já foi publicado sob a mesma assinatura.

## Arquivos governados pela cadeia

| Superfície | O que produz | O que a doutrina exige ali |
|---|---|---|
| `docs/*.md` (METHODOLOGY_V2, GOVERNANCE, STATUS, ROADMAP, PUBLISHING_PLAYBOOK, WRITING_GUIDE, MANUAL, ARCHITECTURE) | Documentação de leitura humana | Prosa de especialista, número com proveniência, identificador conferido |
| `docs/research/**/*.md` | Ondas de pesquisa e sínteses canônicas | Atribuição nomeada, `abs` aberto antes de canonizar ID, raw citado como rastro e não como fonte |
| `docs/outlines/*.md`, `docs/PREREGISTRATION_*`, `docs/ARXIV_SUBMISSION_PLAN.md` | Planejamento de submissão | Quatro conferências em todo resultado citado, marcador no lugar do dado ausente |
| `drafts/*.md` | Divulgação (LinkedIn, Medium, Dev.to, Hashnode, OSF) | Arco de leitura da seção 3, um pedido por peça, denominador ao lado de toda taxa |
| `analysis/MARKET_INSIGHTS_*.md`, `analysis/paper4_tables.py`, `analysis/_market_insights_*.py` | Análise de mercado e tabelas do paper | Amostra, período, método e denominador em cada linha publicada |
| `scripts/send-report.py` | Relatório diário por email | Taxa sempre acompanhada da fração que a origina; nenhuma contagem fixa no código |
| `scripts/update-docs.py` | Reescreve CHANGELOG, GOVERNANCE, STATUS e badges | Texto gerado obedece à mesma tipografia e proveniência do texto escrito à mão |
| `scripts/generate_dashboard_json.py` | `data/dashboard_data.json` consumido por página pública | Métrica derivada do banco e do cohort canônico, com definição do denominador explícita |
| `scripts/generate_report.py`, `scripts/export_data.py`, `scripts/window_progress.py`, `scripts/health_check.py`, `src/cli.py` | Relatórios e saída de terminal em português | Rótulo sem title case, número com unidade e base, mensagem de erro que diz onde mexer |
| `docs/research/fintech-citation-advantage/build_paper_html.py`, `build_brasilgeo_page.py`, `extract_analysis.py` | Manuscrito em HTML e página em brasilgeo.ai | Parágrafo justificado, resultado com base, legenda autossuficiente |
| `docs/research/fintech-citation-advantage/run_waves.sh`, `run_waves_peer_review.sh` | Prompts que geram texto longo em português | Bloco de regras carregado dentro do prompt, conforme `scripts/prompts/BLOCO_EDITORIAL_PROMPT.md` |
| `.github/workflows/daily-collect.yml` | Corpo do email de alerta e da issue de falha | Falha descrita pelo artefato, com o movimento de saída na mesma mensagem |

## O que a doutrina não governa: o instrumento de medição

Os prompts de coleta são instrumento científico, não superfície editorial. `SYSTEM_PROMPT` em `src/config.py` e em `src/shared/llm_utils.py`, os templates de consulta em `src/config_v2.py` e as variações de `src/collectors/prompt_sensitivity.py` definem o tratamento experimental da série longitudinal. Injetar regra de estilo neles mudaria o estímulo enviado ao modelo no meio da janela e destruiria a comparabilidade com tudo o que já foi coletado, que é justamente o ativo que este repositório protege. Mudança ali é decisão metodológica, entra pelo `METHODOLOGY_V2.md` e por pré-registro, nunca por revisão de texto.

A separação é simples de aplicar: prompt que mede recebe versionamento e registro de método; prompt que redige recebe o bloco editorial condensado.

## Nenhum gate deste repo mede substância

A integração contínua roda pytest com sentinela de bateria e o `secret_guard` no pre-commit. Verde ali significa ausência de regressão de código e ausência de segredo vazado, e não diz nada sobre tese, evidência ou proveniência. O `voice_guard.py` canônico fica em `C:/Sandyboxclaude/scripts/python/voice_guard.py`, mede forma, e nunca deve ser executado em modo de correção em lote sobre texto acadêmico, porque a correção automática já corrompeu palavras corretas em outros repositórios do ecossistema. A única proteção de substância disponível aqui é a revisão em três passadas da seção 13 da diretriz, feita por quem assina.
