#!/usr/bin/env python3
"""backfill_daily_snapshots.py — popula daily_snapshots retroativamente.

Bug identificado em 2026-04-29 health-check:
  - Workflow daily-collect.yml roda `collect citation`, mas só `collect all`
    chamava save_daily_aggregate. Resultado: daily_snapshots ficou com 0 rows
    durante toda a janela v2 inicial (23-29 abril).
  - Fix prospectivo já aplicado em src/cli.py (Onda 16): collect_citation
    persiste snapshot agora.
  - Este script reconstrói os snapshots passados a partir das rows reais em
    citations, idempotente via INSERT OR REPLACE em (date, module, vertical).

Usage:
    python scripts/backfill_daily_snapshots.py [--since 2026-04-23] [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

DB_PATH_DEFAULT = Path(__file__).resolve().parent.parent / "data" / "papers.db"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default=str(DB_PATH_DEFAULT))
    parser.add_argument("--since", default="2026-04-23",
                        help="Data inicial (YYYY-MM-DD)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row

    # Datas com pelo menos 1 row na janela
    dates = [
        r["d"] for r in conn.execute(
            "SELECT DISTINCT date(timestamp) AS d FROM citations "
            "WHERE date(timestamp) >= ? ORDER BY d",
            (args.since,),
        ).fetchall()
    ]
    print(f"[info] datas a backfillar: {dates}")

    verticals = [
        r["v"] for r in conn.execute(
            "SELECT DISTINCT vertical AS v FROM citations WHERE vertical IS NOT NULL"
        ).fetchall()
    ]
    print(f"[info] verticais: {verticals}")

    inserted = 0
    for d in dates:
        for vert in verticals:
            rows = conn.execute(
                """SELECT llm,
                          COUNT(*) AS queries,
                          SUM(CASE WHEN cited_v2 = 1 THEN 1 ELSE 0 END) AS cited,
                          AVG(response_length) AS avg_len,
                          AVG(latency_ms) AS avg_lat
                   FROM citations
                   WHERE date(timestamp) = ? AND vertical = ?
                   GROUP BY llm""",
                (d, vert),
            ).fetchall()
            if not rows:
                continue
            by_llm = {}
            total_q = 0
            total_c = 0
            for r in rows:
                by_llm[r["llm"]] = {
                    "queries": r["queries"],
                    "cited": r["cited"] or 0,
                    "rate": round((r["cited"] or 0) / max(r["queries"], 1), 3),
                    "avg_response_length": round(r["avg_len"] or 0),
                    "avg_latency_ms": round(r["avg_lat"] or 0),
                }
                total_q += r["queries"]
                total_c += r["cited"] or 0
            payload = {
                "date": d,
                "vertical": vert,
                "total_queries": total_q,
                "total_cited": total_c,
                "overall_rate": round(total_c / max(total_q, 1), 3),
                "by_llm": by_llm,
                "backfilled": True,
                "backfill_source": "scripts/backfill_daily_snapshots.py",
            }
            data_json = json.dumps(payload, ensure_ascii=False)
            if args.dry_run:
                print(f"[dry-run] {d} {vert}: queries={total_q} cited={total_c}")
                continue
            conn.execute(
                """INSERT OR REPLACE INTO daily_snapshots
                       (date, module, vertical, data_json)
                   VALUES (?, ?, ?, ?)""",
                (d, "citation_tracker", vert, data_json),
            )
            inserted += 1

    if not args.dry_run:
        conn.commit()
    print(f"[ok] snapshots upserted: {inserted}")

    # Verifica
    n = conn.execute("SELECT COUNT(*) FROM daily_snapshots").fetchone()[0]
    print(f"[info] daily_snapshots agora: {n} rows")

    conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
