# papers — reproducible analysis container
# Usage:
#   docker build -t papers-repro .
#   docker run --rm -v $(pwd)/output:/app/output papers-repro analyze --report
#
# Este Dockerfile fornece ambiente reprodutível (Python 3.11.15 pinado,
# deps via requirements-lock.txt) para rodar o pipeline de análise
# confirmatória do paper. NÃO contém as API keys — coleta requer .env
# montado via `-v` na execução.
#
# Resolve gaps E2/E3/E4/E6 do Agent E audit (2026-04-23).

FROM python:3.11.15-slim AS base

LABEL org.opencontainers.image.source="https://github.com/alexandrebrt14-sys/papers"
LABEL org.opencontainers.image.title="papers — LLM citation research pipeline"
LABEL org.opencontainers.image.description="Reproducible env for paper analysis (Null-Triad paper + v2 reboot)"
LABEL org.opencontainers.image.licenses="MIT"

WORKDIR /app

# Sistema mínimo: sqlite3 para CLI, git para tag resolution, build-essential
# para scipy/numpy se não houver wheel binário
RUN apt-get update && apt-get install -y --no-install-recommends \
    sqlite3 \
    git \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Pinned requirements (gerado via pip freeze — requirements-lock.txt)
# Se requirements-lock.txt ausente, cai pra pyproject.toml
COPY pyproject.toml ./
COPY requirements-lock.txt* ./

RUN pip install --upgrade pip && \
    if [ -f requirements-lock.txt ]; then \
        pip install --no-cache-dir -r requirements-lock.txt; \
    else \
        pip install --no-cache-dir -e .; \
    fi

# Código fonte
COPY src/ ./src/
COPY scripts/ ./scripts/
COPY tests/ ./tests/
COPY docs/ ./docs/

# Data seed (opcional) — permite reproduzir análise sem recoleta
# Use multi-stage ou volume mount para dados grandes
COPY data/papers.db /app/data/papers.db

# Env vars de reprodutibilidade — evita nondeterminismo de hash randomization
ENV PYTHONHASHSEED=20260424 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PAPERS_DB_PATH=/app/data/papers.db \
    PAPERS_BOOTSTRAP_SEED=42

# Entrypoint: o CLI Click
ENTRYPOINT ["python", "-m", "src.cli"]

# Default: roda validação + análise rápida (não coleta — requer API keys)
CMD ["--help"]
