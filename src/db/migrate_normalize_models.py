"""Migration: normalize gpt-4o-mini model strings.

The DB has two model strings for the same model:
  - gpt-4o-mini        (N=118, from early collections)
  - gpt-4o-mini-2024-07-18  (N=18, after pinning in config.py)

This script unifies them to the pinned version.
"""

import sqlite3
import sys
from pathlib import Path

# Resolve DB path (same logic as config.py)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "papers.db"


def migrate(db_path: str | Path = DB_PATH) -> int:
    """Update all 'gpt-4o-mini' rows to 'gpt-4o-mini-2024-07-18'. Returns rows updated."""
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    cur.execute(
        "UPDATE citations SET model = ? WHERE model = ?",
        ("gpt-4o-mini-2024-07-18", "gpt-4o-mini"),
    )
    updated = cur.rowcount
    conn.commit()
    conn.close()
    return updated


if __name__ == "__main__":
    db = sys.argv[1] if len(sys.argv) > 1 else DB_PATH
    n = migrate(db)
    print(f"Linhas atualizadas: {n} (gpt-4o-mini -> gpt-4o-mini-2024-07-18)")
