# CLAUDE.md — Papers

## REGRA #0 — IDIOMA
Todo conteúdo em PT-BR com acentuação completa. Exceção: código, commits, docstrings técnicas.

## Propósito
Pesquisa empírica multi-vertical sobre como LLMs citam empresas brasileiras em respostas generativas.
Framework de 4 verticais com coortes independentes monitoradas em 4 LLMs.
Objetivo: gerar datasets longitudinais de 6-12 meses que suportem publicação acadêmica peer-reviewed.

## Verticais e Coortes

### Fintech (16 entidades)
Nubank, PagBank, Cielo, Stone, Banco Inter, Mercado Pago, Itaú, Bradesco, C6 Bank, PicPay, Ame Digital, Neon, Original, BS2, Safra, Banco Carrefour

### Varejo (15 entidades)
Magazine Luiza, Casas Bahia, Mercado Livre, Amazon Brasil, Shopee Brasil, Americanas, Carrefour, Pão de Açúcar, Renner, Riachuelo, C&A Brasil, Havan, Leroy Merlin, Netshoes, Dafiti

### Saúde (15 entidades)
Dasa, Hapvida, Unimed, Fleury, Rede D'Or, Einstein, Sírio-Libanês, Mater Dei, Hermes Pardini, Sabin, Amil, SulAmérica Saúde, Prevent Senior, HCor, A.C. Camargo

### Tecnologia (15 entidades)
Tivit, Totvs, Stefanini, Accenture, CI&T, Globant, Softplan, Linx, Locaweb, Movile, iFood Tech, Vtex, RD Station, Involves, Tempest Security

**Total: 61 entidades, 4 verticais, 4 LLMs**

## Stack
- Python 3.11+
- FastAPI + Uvicorn (API REST para seleção de vertical)
- Supabase (persistência)
- APIs: OpenAI, Anthropic, Google AI, Perplexity, SerpAPI
- Análise: scipy, statsmodels, matplotlib, seaborn
- CLI: click (com --vertical flag para seleção de setor)
- CI/CD: GitHub Actions (coleta diária + benchmark semanal)

## Estrutura
```
src/
  config.py              # Configuração central (.env, constantes, coortes por vertical)
  cli.py                 # CLI principal (click, --vertical flag)
  collectors/
    base.py              # Classe base para coletores
    citation_tracker.py  # Módulo 1: Multi-LLM Citation Tracker
    competitor.py        # Módulo 2: Multi-Vertical Benchmark
    serp_overlap.py      # Módulo 3: SERP vs AI Overlap Tracker
    intervention.py      # Módulo 4: Content Intervention Tracker
    context_analyzer.py  # Módulo 7: Citation Context Analyzer
  db/
    schema.sql           # Schema Supabase/SQLite (coluna vertical)
    client.py            # Cliente de persistência
  persistence/
    timeseries.py        # Módulo 5: Série temporal
  analysis/
    statistical.py       # Módulo 6: Análise estatística
    visualization.py     # Gráficos publicáveis
  api/
    main.py              # FastAPI app (endpoints por vertical)
tests/
data/                    # Dados locais (gitignored, exceto schemas)
.github/workflows/
  daily-collect.yml      # Coleta diária 06:00 UTC (4 verticais sequenciais)
  weekly-benchmark.yml   # Benchmark semanal domingo 08:00 UTC
```

## Comandos
```bash
# Coleta multi-vertical
python -m src.cli collect --all                              # Todas as verticais
python -m src.cli collect --all --vertical fintech           # Só fintech
python -m src.cli collect --all --vertical varejo            # Só varejo
python -m src.cli collect --all --vertical saude             # Só saúde
python -m src.cli collect --all --vertical tecnologia        # Só tecnologia

# Coleta por módulo
python -m src.cli collect --module citation                  # Citation tracker (todas as verticais)
python -m src.cli collect --module citation --vertical fintech  # Citation tracker só fintech
python -m src.cli collect --module competitor                # Multi-Vertical Benchmark
python -m src.cli collect --module serp                      # SERP overlap

# Análise
python -m src.cli analyze --report                           # Relatório (todas as verticais)
python -m src.cli analyze --report --vertical saude          # Relatório só saúde
python -m src.cli analyze --visualize                        # Gráficos por vertical

# Intervenções
python -m src.cli intervention add <slug>                    # Registra intervenção

# Banco de dados
python -m src.cli db migrate                                 # Aplica schema (inclui coluna vertical)
python -m src.cli db export --format csv                     # Exporta todas as verticais
python -m src.cli db export --format csv --vertical fintech  # Exporta só fintech
python -m src.cli db health                                  # Saúde do banco por vertical
```

## Env Vars necessárias
- `OPENAI_API_KEY` — ChatGPT queries
- `ANTHROPIC_API_KEY` — Claude queries
- `GOOGLE_AI_API_KEY` — Gemini queries
- `PERPLEXITY_API_KEY` — Perplexity queries (já tem)
- `SERPAPI_KEY` — Google SERP data
- `SUPABASE_URL` — Persistência
- `SUPABASE_KEY` — Persistência
- `PAPERS_DB_PATH` — Fallback SQLite local (default: data/papers.db)

## Convenções de código
- Type hints em todas as funções públicas
- Docstrings em inglês (padrão acadêmico)
- Nomes de variáveis em inglês
- Logs e output CLI em PT-BR
- Testes com pytest (parametrizados por vertical)
- Coluna `vertical` obrigatória em todas as tabelas de citação
