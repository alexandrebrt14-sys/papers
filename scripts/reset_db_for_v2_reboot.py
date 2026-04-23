"""Reset papers.db for v2 methodology reboot.

CRITICAL: This script is intentionally destructive. It truncates tables that
hold empirical collection data from v1 methodology (NER v1, cohort v1, query
battery v1) so the v2 reboot starts from a clean slate.

Runs on 2026-04-23 before the v2 collection window opens.

Preserved (operational config, not empirical data):
  - finops_budgets       — budget limits per provider
  - finops_key_fingerprints — API-key hash audit trail
  - verticals            — cohort metadata

Truncated (v1 dataset, frozen in tag paper-4-dataset-frozen-20260423):
  - citations (main dataset)
  - citation_context
  - collection_runs
  - competitor_citations
  - daily_snapshots
  - dual_responses
  - finops_alerts
  - finops_daily_rollup
  - finops_usage
  - model_versions
  - url_verifications
  - scaling_observations
  - hypotheses
  - interventions / intervention_measurements
  - prompt_variants
  - score_calibration_inputs
  - serp_ai_overlap

Also resets sqlite_sequence and VACUUMs the file.

Usage:
    python scripts/reset_db_for_v2_reboot.py --confirm
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path

# Tables to truncate (empirical v1 data — frozen in git tag)
TRUNCATE_TABLES = [
    "citations",
    "citation_context",
    "collection_runs",
    "competitor_citations",
    "daily_snapshots",
    "dual_responses",
    "finops_alerts",
    "finops_daily_rollup",
    "finops_usage",
    "model_versions",
    "url_verifications",
    "scaling_observations",
    "hypotheses",
    "interventions",
    "intervention_measurements",
    "prompt_variants",
    "score_calibration_inputs",
    "serp_ai_overlap",
]

# Tables intentionally preserved (operational config)
PRESERVE_TABLES = [
    "finops_budgets",
    "finops_key_fingerprints",
    "verticals",
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default="data/papers.db", help="Path to papers.db")
    parser.add_argument("--confirm", action="store_true", required=True,
                        help="Required safety flag — operation is irreversible")
    parser.add_argument("--dry-run", action="store_true",
                        help="Report what would be deleted, don't execute")
    args = parser.parse_args()

    db_path = Path(args.db)
    if not db_path.exists():
        print(f"[FATAL] DB not found: {db_path}", file=sys.stderr)
        return 2

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    print(f"=== papers.db v2-reboot reset ===")
    print(f"DB:   {db_path.resolve()}")
    print(f"Mode: {'DRY-RUN' if args.dry_run else 'EXECUTE'}")
    print()

    print(">> Pre-truncate row counts:")
    for t in TRUNCATE_TABLES:
        try:
            n = conn.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0]
            print(f"   {n:>10}  {t}")
        except sqlite3.OperationalError as e:
            print(f"   [skip]      {t}  ({e})")

    print()
    print(">> Preserved tables (unchanged):")
    for t in PRESERVE_TABLES:
        try:
            n = conn.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0]
            print(f"   {n:>10}  {t}")
        except sqlite3.OperationalError as e:
            print(f"   [skip]      {t}  ({e})")

    if args.dry_run:
        print("\n[DRY-RUN] No changes made. Pass --confirm without --dry-run to execute.")
        conn.close()
        return 0

    print()
    print(">> Truncating...")
    total_deleted = 0
    for t in TRUNCATE_TABLES:
        try:
            cur = conn.execute(f'DELETE FROM "{t}"')
            print(f"   [{cur.rowcount:>10}]  {t}")
            total_deleted += cur.rowcount
        except sqlite3.OperationalError as e:
            print(f"   [skip]       {t}  ({e})")

    # Reset AUTOINCREMENT counters so new rows start at id=1
    print()
    print(">> Resetting AUTOINCREMENT counters (sqlite_sequence)...")
    for t in TRUNCATE_TABLES:
        conn.execute("DELETE FROM sqlite_sequence WHERE name = ?", (t,))

    conn.commit()

    print()
    print(">> VACUUM (reclaim disk space)...")
    conn.execute("VACUUM")
    conn.close()

    # Report final size
    print()
    print(f"=== Reset complete ===")
    print(f"Rows deleted: {total_deleted}")
    print(f"New DB size:  {db_path.stat().st_size:,} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
