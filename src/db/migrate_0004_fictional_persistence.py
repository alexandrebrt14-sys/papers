"""Migration 0004 — Persistência de fictional_hit (Double-check 2026-04-19).

Gap identificado no segundo double-check: o citation_tracker detecta
`fictional_hit` em memória (Onda 3), mas o valor não era persistido no DB
— perdia o sinal de false-positive entre runs.

Changes:
    1. NEW COLUMN: citations.fictional_hit (INTEGER 0|1, default 0)
       Flag quando LLM menciona entidade fictícia na resposta.
    2. NEW COLUMN: citations.fictional_names_json (TEXT, default '[]')
       JSON array com os nomes fictícios detectados (suporta múltiplos).
    3. NEW INDEX: idx_citations_fictional_hit
       Permite filtrar rapidamente os casos de false-positive para análise.
    4. BACKFILL retroativo: varre response_text existente e marca
       fictional_hit=1 onde encontra entidade fictícia. Calcula taxa de
       false-positive do dataset histórico sem re-executar o pipeline.

Idempotente + dry-run.

Uso:
    python -m src.db.migrate_0004_fictional_persistence --db data/papers.db
    python -m src.db.migrate_0004_fictional_persistence --db data/papers.db --dry-run
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path


NEW_COLUMNS = [
    ("fictional_hit", "INTEGER NOT NULL DEFAULT 0"),
    ("fictional_names_json", "TEXT NOT NULL DEFAULT '[]'"),
]
NEW_INDEXES = [
    ("idx_citations_fictional_hit", "citations(fictional_hit)"),
]


def _has_column(cur: sqlite3.Cursor, table: str, column: str) -> bool:
    cur.execute(f"PRAGMA table_info({table})")
    return any(row[1] == column for row in cur.fetchall())


def _has_index(cur: sqlite3.Cursor, name: str) -> bool:
    cur.execute("SELECT 1 FROM sqlite_master WHERE type='index' AND name=?", (name,))
    return cur.fetchone() is not None


def _load_fictional_names() -> list[str]:
    """Carrega a lista completa de fictícias do config.py.

    Import lazy para evitar dependência circular em contextos de migration
    sem src no path.
    """
    try:
        from src.config import FICTIONAL_ENTITIES
    except ImportError:
        # Fallback estático — lista precisa bater com src/config.py
        return [
            "Banco Floresta Digital", "FinPay Solutions",
            "MegaStore Brasil", "ShopNova Digital",
            "HealthTech Brasil", "Clínica Horizonte Digital",
            "TechNova Solutions", "DataBridge Brasil",
        ]
    names: list[str] = []
    for lst in FICTIONAL_ENTITIES.values():
        names.extend(lst)
    return names


def _backfill_fictional_hits(cur: sqlite3.Cursor, dry_run: bool) -> tuple[int, int]:
    """Marca fictional_hit=1 em registros legados cujo response_text
    menciona entidade fictícia.

    Returns: (registros_avaliados, registros_marcados). Retorna (0, 0) se
    a tabela não tiver coluna response_text (DBs minimalistas usados em
    testes ou schemas legados).
    """
    # Checa se response_text existe (DBs enxutos de teste podem não ter)
    cols = [r[1] for r in cur.execute("PRAGMA table_info(citations)").fetchall()]
    if "response_text" not in cols:
        return 0, 0

    fictional_names = _load_fictional_names()
    if not fictional_names:
        return 0, 0

    cur.execute(
        "SELECT id, response_text FROM citations "
        "WHERE response_text IS NOT NULL AND response_text != ''"
    )
    rows = cur.fetchall()

    marked = 0
    updates: list[tuple[str, int]] = []
    for cid, text in rows:
        if not text:
            continue
        lower = text.lower()
        hits = [n for n in fictional_names if n.lower() in lower]
        if hits:
            updates.append((json.dumps(hits, ensure_ascii=False), cid))
            marked += 1

    if updates and not dry_run:
        cur.executemany(
            "UPDATE citations SET fictional_hit = 1, fictional_names_json = ? WHERE id = ?",
            updates,
        )

    return len(rows), marked


def migrate(db_path: Path, dry_run: bool = False) -> dict:
    summary: dict = {
        "added_columns": [],
        "added_indexes": [],
        "rows_scanned": 0,
        "rows_marked_fictional": 0,
        "dry_run": dry_run,
    }

    con = sqlite3.connect(db_path)
    con.execute("PRAGMA journal_mode=WAL")
    cur = con.cursor()

    try:
        for col, defn in NEW_COLUMNS:
            if not _has_column(cur, "citations", col):
                if not dry_run:
                    cur.execute(f"ALTER TABLE citations ADD COLUMN {col} {defn}")
                summary["added_columns"].append(col)

        for name, tbl_cols in NEW_INDEXES:
            if not _has_index(cur, name):
                if not dry_run:
                    cur.execute(f"CREATE INDEX IF NOT EXISTS {name} ON {tbl_cols}")
                summary["added_indexes"].append(name)

        # Backfill só faz sentido se a coluna existe (após ALTER). Em dry-run,
        # a ALTER não acontece, então o PRAGMA acha a coluna ausente e o
        # UPDATE falharia — skip o backfill em dry-run (apenas reporta).
        if not dry_run and _has_column(cur, "citations", "fictional_hit"):
            scanned, marked = _backfill_fictional_hits(cur, dry_run=False)
            summary["rows_scanned"] = scanned
            summary["rows_marked_fictional"] = marked

        if not dry_run:
            con.commit()
    finally:
        con.close()

    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Migration 0004")
    parser.add_argument("--db", type=Path, default=Path("data/papers.db"))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not args.db.exists():
        print(f"ERRO: DB não encontrado em {args.db}", file=sys.stderr)
        return 1

    print("Migration 0004: Persistência de fictional_hit")
    print(f"  DB:      {args.db}")
    print(f"  Dry-run: {args.dry_run}\n")

    summary = migrate(args.db, dry_run=args.dry_run)

    if summary["added_columns"]:
        print(f"  [+] {len(summary['added_columns'])} colunas adicionadas: {summary['added_columns']}")
    else:
        print("  [=] Colunas já existiam")

    if summary["added_indexes"]:
        print(f"  [+] Índices criados: {summary['added_indexes']}")
    else:
        print("  [=] Índices já existiam")

    print(
        f"  [+] Backfill: {summary['rows_marked_fictional']} / {summary['rows_scanned']} "
        f"registros marcados como fictional_hit"
    )

    if summary["dry_run"]:
        print("\nDRY RUN — nada persistido.")
    else:
        print("\nMigration aplicada com sucesso.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
