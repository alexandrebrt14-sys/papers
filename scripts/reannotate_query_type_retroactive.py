#!/usr/bin/env python3
"""reannotate_query_type_retroactive.py — corrige query_type das 8.571 rows v2.

Bug identificado em 2026-04-29 health-check:
  - config_v2.build_canonical_battery() gera 192 queries balanceadas 50/50
    directive/exploratory (96 cada).
  - O collector grava query_type via config.query_type_for(q), que lia
    APENAS q["type"] como override. As queries v2 usam a chave "query_type"
    (não "type"), então o override era ignorado e caía no map por categoria.
  - QUERY_TYPE_BY_CATEGORY mapeia 5/6 categorias v2 para "directive"
    (descoberta, comparativo, mercado, experiencia, inovacao) e só
    "confianca" para "exploratory" → 85/15 directive/exploratory no DB.

Este script:
  1. Reconstrói o índice (vertical, category, lang, query_text) → query_type
     a partir de config_v2.build_canonical_battery() (já com fix aplicado).
  2. Faz match por query_text exato em citations.query.
  3. UPDATEs as rows com novo query_type. Original permanece em
     query_type_v1_legacy para auditoria.

Idempotente: re-executar produz 0 mudanças quando DB já está corrigido.

Usage:
    python scripts/reannotate_query_type_retroactive.py [--dry-run] [--db PATH]
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from collections import Counter
from pathlib import Path

DB_PATH_DEFAULT = Path(__file__).resolve().parent.parent / "data" / "papers.db"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default=str(DB_PATH_DEFAULT))
    parser.add_argument("--dry-run", action="store_true", help="Preview only, no writes")
    args = parser.parse_args()

    # Importa apenas após argparse para que --help não falhe sem deps.
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src.config_v2 import build_canonical_battery
    from src.config import query_type_for

    canonical = build_canonical_battery()
    # Index: query_text → query_type canonical
    index: dict[str, str] = {}
    for q in canonical:
        index[q["query"]] = query_type_for(q)
    print(f"[info] index built: {len(index)} canonical queries")
    print(f"[info] balance: {Counter(index.values())}")

    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row

    # Adiciona coluna de auditoria se não existir
    cols = {r[1] for r in conn.execute("PRAGMA table_info(citations)").fetchall()}
    if "query_type_v1_legacy" not in cols:
        if args.dry_run:
            print("[dry-run] would ALTER TABLE citations ADD COLUMN query_type_v1_legacy TEXT")
        else:
            conn.execute("ALTER TABLE citations ADD COLUMN query_type_v1_legacy TEXT")
            print("[ok] coluna query_type_v1_legacy criada")

    # Snapshot atual
    print("\n[before] distribuição query_type na janela v2:")
    for r in conn.execute(
        "SELECT query_type, COUNT(*) FROM citations "
        "WHERE date(timestamp) >= '2026-04-23' GROUP BY query_type"
    ):
        print(f"  {r[0] or 'NULL':<12} {r[1]}")

    # Plan: para cada query distinta, ver se tem entrada no índice
    rows = conn.execute(
        "SELECT DISTINCT query, query_type FROM citations "
        "WHERE date(timestamp) >= '2026-04-23'"
    ).fetchall()
    print(f"\n[info] queries distintas v2-window: {len(rows)}")

    matched = 0
    unmatched = 0
    diff_count = 0
    fixes: list[tuple[str, str, str]] = []  # (query, old, new)
    for r in rows:
        q = r["query"]
        old_type = r["query_type"]
        new_type = index.get(q)
        if new_type is None:
            unmatched += 1
            continue
        matched += 1
        if old_type != new_type:
            diff_count += 1
            fixes.append((q, old_type, new_type))

    print(f"[info] matched: {matched}, unmatched: {unmatched}, requires_fix: {diff_count}")
    if fixes[:3]:
        print("[sample fixes]")
        for q, old, new in fixes[:3]:
            print(f"  {old} -> {new}: {q[:60]}...")

    if args.dry_run:
        print("\n[dry-run] no writes performed.")
        conn.close()
        return 0

    if not fixes:
        print("\n[ok] nada a corrigir.")
        conn.close()
        return 0

    updated_total = 0
    for q, old, new in fixes:
        cur = conn.execute(
            "UPDATE citations SET "
            "  query_type_v1_legacy = COALESCE(query_type_v1_legacy, query_type), "
            "  query_type = ? "
            "WHERE query = ? AND date(timestamp) >= '2026-04-23'",
            (new, q),
        )
        updated_total += cur.rowcount
    conn.commit()
    print(f"\n[ok] updated {updated_total} rows across {len(fixes)} distinct queries")

    # Snapshot final
    print("\n[after] distribuição query_type na janela v2:")
    for r in conn.execute(
        "SELECT query_type, COUNT(*) FROM citations "
        "WHERE date(timestamp) >= '2026-04-23' GROUP BY query_type"
    ):
        print(f"  {r[0] or 'NULL':<12} {r[1]}")

    conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
