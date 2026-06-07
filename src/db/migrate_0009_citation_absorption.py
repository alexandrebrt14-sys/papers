"""migrate_0009 — Citation Selection vs Absorption + failure taxonomy + semantic entropy drift.

Materializa o contrato documentado na Wave Maio 2026 Pós-I/O (§ schema) e
reforçado na Wave Junho 2026 (§7.2), que até então só existia em prosa:

    citations.selection_status   INTEGER  -- CSR por observação (1/0/NULL)
    citations.absorption_status  INTEGER  -- CAR por observação (1/0/NULL)
    citations.failure_type       TEXT     -- enum de falha de citação (7 tipos)
    daily_snapshots.citation_selection_rate   REAL  -- CSR agregada do dia
    daily_snapshots.citation_absorption_rate  REAL  -- CAR agregada do dia
    daily_snapshots.semantic_entropy_drift    REAL  -- deriva de entropia semântica

Fonte primária da distinção seleção × absorção: arXiv:2604.25707
("From Citation Selection to Citation Absorption", dataset geo-citation-lab,
602 prompts, 72 features). Taxonomia de 7 tipos de falha: arXiv:2603.09296.
Entropia semântica: arXiv:2604.03656 / arXiv:2508.14496.

`selection_status` = a fonte foi recuperada/selecionada para o source set.
`absorption_status` = a fonte selecionada influenciou de fato o texto final.
São fenômenos distintos: uma fonte pode ser selecionada e não absorvida.
NULL = legacy/desconhecido (coletor v1 não popula) — preserva retrocompat.

failure_type (enum, NULL = sem falha):
    broken-fetch | parsing-failure | retrieval-miss | summarization-collapse
    | attribution-drop | hallucinated-source | blocked-by-robots

Idempotente: detecta colunas existentes via PRAGMA antes de cada ALTER.
"""
from __future__ import annotations

import sqlite3

# Colunas adicionadas por tabela. (nome, definição SQL pós "ADD COLUMN <nome>")
_CITATIONS_COLUMNS: list[tuple[str, str]] = [
    ("selection_status", "INTEGER DEFAULT NULL"),
    ("absorption_status", "INTEGER DEFAULT NULL"),
    ("failure_type", "TEXT DEFAULT NULL"),
]
_SNAPSHOT_COLUMNS: list[tuple[str, str]] = [
    ("citation_selection_rate", "REAL DEFAULT NULL"),
    ("citation_absorption_rate", "REAL DEFAULT NULL"),
    ("semantic_entropy_drift", "REAL DEFAULT NULL"),
]

# Valores válidos do enum failure_type (NULL = sem falha). Apenas referência
# documental — SQLite não impõe CHECK aqui para não quebrar coletores legacy.
FAILURE_TYPES: tuple[str, ...] = (
    "broken-fetch",
    "parsing-failure",
    "retrieval-miss",
    "summarization-collapse",
    "attribution-drop",
    "hallucinated-source",
    "blocked-by-robots",
)


def _existing_columns(conn: sqlite3.Connection, table: str) -> set[str]:
    try:
        return {r[1] for r in conn.execute(f"PRAGMA table_info({table})").fetchall()}
    except sqlite3.OperationalError:
        return set()


def _add_missing(conn: sqlite3.Connection, table: str, columns: list[tuple[str, str]]) -> int:
    existing = _existing_columns(conn, table)
    if not existing:  # tabela ainda não existe; schema.sql a criará já com as colunas
        return 0
    added = 0
    for name, ddl in columns:
        if name not in existing:
            conn.execute(f"ALTER TABLE {table} ADD COLUMN {name} {ddl}")
            added += 1
    return added


def apply(conn: sqlite3.Connection) -> int:
    """Aplica a migration. Retorna o número de colunas efetivamente adicionadas."""
    added = 0
    added += _add_missing(conn, "citations", _CITATIONS_COLUMNS)
    added += _add_missing(conn, "daily_snapshots", _SNAPSHOT_COLUMNS)
    # Índices idempotentes (IF NOT EXISTS)
    try:
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_citations_selection_status ON citations(selection_status)"
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_citations_absorption_status ON citations(absorption_status)"
        )
    except sqlite3.OperationalError:
        pass
    conn.commit()
    return added
