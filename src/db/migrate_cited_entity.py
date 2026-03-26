"""Migration: backfill cited_entity from citation_context table.

SQLite cannot ALTER column types, but since the schema now defines
cited_entity/cited_domain/cited_person as TEXT DEFAULT NULL,
new rows will use the correct type. This script backfills existing
rows where cited=1 by looking up the entity name in citation_context.
"""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "papers.db"


def migrate(db_path: str | None = None) -> None:
    path = db_path or str(DB_PATH)
    if not Path(path).exists():
        print(f"Banco não encontrado: {path}")
        sys.exit(1)

    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row

    # Count rows that need backfill
    total_cited = conn.execute(
        "SELECT COUNT(*) as cnt FROM citations WHERE cited = 1 AND (cited_entity IS NULL OR cited_entity = '' OR cited_entity = '0')"
    ).fetchone()["cnt"]
    print(f"Registros com cited=1 sem cited_entity preenchido: {total_cited}")

    if total_cited == 0:
        print("Nenhum registro para atualizar.")
        conn.close()
        return

    # For each citation where cited=1, find the entity from citation_context
    rows = conn.execute("""
        SELECT c.id, cc.entity
        FROM citations c
        JOIN citation_context cc ON cc.citation_id = c.id
        WHERE c.cited = 1
          AND (c.cited_entity IS NULL OR c.cited_entity = '' OR c.cited_entity = '0')
        GROUP BY c.id
    """).fetchall()

    updated = 0
    for row in rows:
        conn.execute(
            "UPDATE citations SET cited_entity = ? WHERE id = ?",
            (row["entity"], row["id"]),
        )
        updated += 1

    conn.commit()
    print(f"Atualizados {updated} registros com cited_entity preenchido.")

    # Also reset old boolean '0' values to NULL for rows where cited=0
    reset = conn.execute(
        "UPDATE citations SET cited_entity = NULL WHERE cited_entity = '0'"
    ).rowcount
    reset += conn.execute(
        "UPDATE citations SET cited_domain = NULL WHERE cited_domain = '0'"
    ).rowcount
    reset += conn.execute(
        "UPDATE citations SET cited_person = NULL WHERE cited_person = '0'"
    ).rowcount
    conn.commit()

    if reset:
        print(f"Resetados {reset} valores booleanos '0' para NULL.")

    conn.close()
    print("Migração concluída.")


if __name__ == "__main__":
    db = sys.argv[1] if len(sys.argv) > 1 else None
    migrate(db)
