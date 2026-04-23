"""Migration 0005 — NER v2 column pack.

Adiciona colunas *_v2 em `citations` para permitir re-extração com o novo
EntityExtractor (src/analysis/entity_extraction.py) sem destruir a série
histórica v1.

Strategy: forward-only. v1 permanece intocada; análises futuras optam por
`WHERE extraction_version = 'v2'` quando querem dados corrigidos.

Incidentes cobertos (Agent C audit 2026-04-23):
- G1 diacritic-insensitive matching
- G2 UTF-8 NFC normalization
- G3 remove substring match FPs
- G4 position via offset real
- G6 aliases
- G7 stop-contexts

Novas colunas:
- `cited_v2` BOOLEAN — novo flag após extração v2
- `cited_count_v2` INTEGER — contagem única de entidades v2
- `cited_entities_v2_json` TEXT — array JSON de cited entities
- `first_entity_v2` TEXT — primeira entidade na ordem do texto
- `first_entity_offset_v2` INTEGER — offset char da primeira menção
- `position_v2` INTEGER — tercile (1/2/3) calculado via offset real
- `via_alias_count_v2` INTEGER — menções via ALIAS dict
- `via_fold_count_v2` INTEGER — menções via diacritic-fold
- `response_length_chars_v2` INTEGER — len(NFC) para position ratio
- `extraction_version` TEXT — 'v1' (legado) ou 'v2' (novo pipeline)
- `extracted_at_v2` TEXT — timestamp da re-extração (para reproducibilidade)
"""
from __future__ import annotations

import logging
import sqlite3

logger = logging.getLogger(__name__)


def apply(conn: sqlite3.Connection) -> None:
    """Aplica migration 0005 idempotentemente."""
    cur = conn.cursor()

    # Verifica se migration já foi aplicada
    existing_cols = {
        row[1] for row in cur.execute("PRAGMA table_info(citations)").fetchall()
    }

    additions = [
        ("cited_v2",                  "INTEGER"),          # 0/1 boolean
        ("cited_count_v2",            "INTEGER DEFAULT 0"),
        ("cited_entities_v2_json",    "TEXT DEFAULT '[]'"),
        ("first_entity_v2",           "TEXT"),
        ("first_entity_offset_v2",    "INTEGER"),
        ("position_v2",               "INTEGER"),
        ("via_alias_count_v2",        "INTEGER DEFAULT 0"),
        ("via_fold_count_v2",         "INTEGER DEFAULT 0"),
        ("response_length_chars_v2",  "INTEGER"),
        ("extraction_version",        "TEXT DEFAULT 'v1'"),
        ("extracted_at_v2",           "TEXT"),
    ]

    added = []
    for col, type_def in additions:
        if col not in existing_cols:
            cur.execute(f"ALTER TABLE citations ADD COLUMN {col} {type_def}")
            added.append(col)

    # Índice para filtrar rapidamente quem está em v2 vs v1
    cur.execute(
        "CREATE INDEX IF NOT EXISTS idx_citations_extraction_version "
        "ON citations(extraction_version)"
    )

    conn.commit()
    logger.info("migrate_0005_ner_v2: added %d columns: %s", len(added), added)
    return added


def rollback(conn: sqlite3.Connection) -> None:
    """Rollback manual: SQLite não suporta DROP COLUMN nativo; recomendação
    é NÃO rollback (forward-only). Se necessário, recriar tabela sem as cols.
    """
    logger.warning(
        "migrate_0005_ner_v2: rollback não implementado (SQLite lacks DROP COLUMN). "
        "Recriar tabela manualmente se necessário."
    )
