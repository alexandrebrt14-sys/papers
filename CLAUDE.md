# CLAUDE.md — Papers

## REGRA #0 — IDIOMA
Todo conteúdo em PT-BR com acentuação completa. Exceção: código, commits, docstrings técnicas.

## Propósito
Pesquisa empírica sobre como LLMs citam bancos e fintechs brasileiras em respostas generativas.
Coorte de estudo: Nubank, PagBank, Cielo, Stone, Banco Inter, Mercado Pago, Itaú, Bradesco, C6 Bank, PicPay, Ame Digital, Neon, Original, BS2, Safra.
Objetivo: gerar datasets longitudinais de 6-12 meses que suportem publicação acadêmica peer-reviewed.

## Stack
- Python 3.11+
- Supabase (persistência)
- APIs: OpenAI, Anthropic, Google AI, Perplexity, SerpAPI
- Análise: scipy, statsmodels, matplotlib, seaborn
- CLI: click
- CI/CD: GitHub Actions (coleta diária + benchmark semanal)

## Estrutura
```
src/
  config.py              # Configuração central (.env, constantes)
  cli.py                 # CLI principal (click)
  collectors/
    base.py              # Classe base para coletores
    citation_tracker.py  # Módulo 1: Multi-LLM Citation Tracker
    competitor.py        # Módulo 2: Competitor Benchmark Dataset
    serp_overlap.py      # Módulo 3: SERP vs AI Overlap Tracker
    intervention.py      # Módulo 4: Content Intervention Tracker
    context_analyzer.py  # Módulo 7: Citation Context Analyzer
  db/
    schema.sql           # Schema Supabase/SQLite
    client.py            # Cliente de persistência
  persistence/
    timeseries.py        # Módulo 5: Série temporal
  analysis/
    statistical.py       # Módulo 6: Análise estatística
    visualization.py     # Gráficos publicáveis
tests/
data/                    # Dados locais (gitignored, exceto schemas)
.github/workflows/
  daily-collect.yml      # Coleta diária 06:00 UTC
  weekly-benchmark.yml   # Benchmark semanal domingo 08:00 UTC
```

## Comandos
```bash
python -m src.cli collect --all              # Roda todos os coletores
python -m src.cli collect --module citation   # Só citation tracker
python -m src.cli collect --module competitor # Só competitor benchmark
python -m src.cli collect --module serp       # Só SERP overlap
python -m src.cli analyze --report           # Gera relatório estatístico
python -m src.cli analyze --visualize        # Gera gráficos
python -m src.cli intervention add <slug>    # Registra intervenção
python -m src.cli db migrate                 # Aplica schema
python -m src.cli db export --format csv     # Exporta dados
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
- Testes com pytest
