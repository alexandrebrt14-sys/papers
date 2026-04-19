"""Migration 0003 — Eficácia, Consistência e Índices (2026-04-19).

Aplicado durante refactor baseado em auditoria 2026-04-19.

Changes:
    1. NEW COLUMN: citations.query_type ('directive' | 'exploratory')
       Permite isolar efeito de framing das queries nos testes estatísticos.
    2. NEW INDEXES: compostos em citations para queries analíticas frequentes
       - (vertical, cited)
       - (vertical, llm)
       - (timestamp, vertical)
       - (llm, model_version)
       Previne table scans quando N > 10K.
    3. BACKFILL: citations.model_version NULL → citations.model
       Para registros antigos que não tinham model_version ainda.
    4. BACKFILL: finops_usage.vertical NULL → 'unknown' (preserva consistência)
       Registros pré-migration da coluna ficam marcados explicitamente.

Idempotente — pode ser executado múltiplas vezes sem efeito adicional.

Uso:
    python -m src.db.migrate_0003_eficacia_consistencia --db data/papers.db
    python -m src.db.migrate_0003_eficacia_consistencia --db data/papers.db --dry-run
"""

from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path


NEW_INDEXES = [
    ("idx_citations_vertical_cited",  "citations(vertical, cited)"),
    ("idx_citations_vertical_llm",    "citations(vertical, llm)"),
    ("idx_citations_timestamp_vert",  "citations(timestamp, vertical)"),
    ("idx_citations_llm_modelver",    "citations(llm, model_version)"),
    ("idx_citations_query_type",      "citations(query_type)"),
]


def _has_column(cur: sqlite3.Cursor, table: str, column: str) -> bool:
    cur.execute(f"PRAGMA table_info({table})")
    return any(row[1] == column for row in cur.fetchall())


def _has_index(cur: sqlite3.Cursor, name: str) -> bool:
    cur.execute("SELECT 1 FROM sqlite_master WHERE type='index' AND name=?", (name,))
    return cur.fetchone() is not None


def migrate(db_path: Path, dry_run: bool = False) -> dict:
    """Apply migration 0003. Returns summary of actions taken."""
    summary: dict = {
        "added_column_query_type": False,
        "added_indexes": [],
        "backfilled_model_version": 0,
        "backfilled_finops_vertical": 0,
        "dry_run": dry_run,
    }

    con = sqlite3.connect(db_path)
    con.execute("PRAGMA journal_mode=WAL")
    con.execute("PRAGMA foreign_keys=ON")
    cur = con.cursor()

    try:
        # 1. Nova coluna: citations.query_type
        if not _has_column(cur, "citations", "query_type"):
            if not dry_run:
                cur.execute(
                    "ALTER TABLE citations ADD COLUMN query_type TEXT DEFAULT 'exploratory'"
                )
            summary["added_column_query_type"] = True

        # 2. Índices compostos
        for name, defn in NEW_INDEXES:
            if not _has_index(cur, name):
                if not dry_run:
                    cur.execute(f"CREATE INDEX IF NOT EXISTS {name} ON {defn}")
                summary["added_indexes"].append(name)

        # 3. Backfill model_version onde NULL (colunas antigas sem rastreio)
        cur.execute(
            "SELECT COUNT(*) FROM citations WHERE model_version IS NULL OR model_version = ''"
        )
        n_backfill = cur.fetchone()[0]
        if n_backfill > 0 and not dry_run:
            cur.execute(
                "UPDATE citations SET model_version = model "
                "WHERE model_version IS NULL OR model_version = ''"
            )
        summary["backfilled_model_version"] = n_backfill

        # 4. Backfill finops_usage.vertical onde NULL
        cur.execute(
            "SELECT COUNT(*) FROM finops_usage "
            "WHERE vertical IS NULL OR vertical = ''"
        )
        n_finops = cur.fetchone()[0]
        if n_finops > 0 and not dry_run:
            cur.execute(
                "UPDATE finops_usage SET vertical = 'unknown' "
                "WHERE vertical IS NULL OR vertical = ''"
            )
        summary["backfilled_finops_vertical"] = n_finops

        if not dry_run:
            con.commit()
    finally:
        con.close()

    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Migration 0003")
    parser.add_argument(
        "--db",
        type=Path,
        default=Path("data/papers.db"),
        help="Caminho para o papers.db (default: data/papers.db)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Não aplica, apenas relata o que seria feito.",
    )
    args = parser.parse_args()

    if not args.db.exists():
        print(f"ERRO: DB não encontrado em {args.db}", file=sys.stderr)
        return 1

    print(f"Migration 0003: Eficácia + Consistência + Índices")
    print(f"  DB:      {args.db}")
    print(f"  Dry-run: {args.dry_run}")
    print()

    summary = migrate(args.db, dry_run=args.dry_run)

    print("Resultado:")
    if summary["added_column_query_type"]:
        print("  [+] Coluna citations.query_type adicionada")
    else:
        print("  [=] Coluna citations.query_type já existe")

    if summary["added_indexes"]:
        print(f"  [+] {len(summary['added_indexes'])} índices criados:")
        for idx in summary["added_indexes"]:
            print(f"        - {idx}")
    else:
        print("  [=] Todos os índices já existem")

    print(f"  [+] model_version backfill: {summary['backfilled_model_version']} registros")
    print(f"  [+] finops vertical backfill: {summary['backfilled_finops_vertical']} registros")

    if summary["dry_run"]:
        print("\nDRY RUN — nenhuma alteração persistida.")
    else:
        print("\nMigration aplicada com sucesso.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
