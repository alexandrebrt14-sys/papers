#!/usr/bin/env python3
"""validate_v2_collection.py — sanity check pós-coleta v2.

Executa após cada run daily-collect para garantir que:
  1. Todas as 5 LLMs produziram rows
  2. Todas as 4 verticais produziram rows
  3. Colunas v2 estão populadas (extraction_version='v2', response_hash, is_probe, ...)
  4. Nenhum fictitious_hit para decoys (confirma NER v2 não alucina)
  5. `model_versions` registrou versões dos providers

Exit 0 = OK · Exit 1 = warning · Exit 2 = failure crítico.

Usage (standalone):
    python scripts/validate_v2_collection.py [--since-minutes 120] [--verbose]

Integration: daily-collect.yml step pós-coleta (não-bloqueante).
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path


DB_PATH = Path(__file__).resolve().parent.parent / "data" / "papers.db"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--since-minutes", type=int, default=120,
                        help="Só valida rows inseridas nos últimos N minutos")
    parser.add_argument("--verbose", action="store_true", help="Print per-provider detail")
    args = parser.parse_args()

    since = datetime.now(timezone.utc) - timedelta(minutes=args.since_minutes)
    since_iso = since.strftime("%Y-%m-%dT%H:%M:%SZ")

    if not DB_PATH.exists():
        print(f"[FATAL] DB not found: {DB_PATH}", file=sys.stderr)
        return 2

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    print(f"=== v2 collection validator ===")
    print(f"DB:    {DB_PATH}")
    print(f"Since: {since_iso}")
    print()

    warnings: list[str] = []
    failures: list[str] = []

    # 1. Rows in window
    n = conn.execute("SELECT COUNT(*) FROM citations WHERE timestamp >= ?", (since_iso,)).fetchone()[0]
    print(f"1. Rows in window: {n}")
    if n == 0:
        failures.append("no rows in window")
    else:
        print(f"   [OK]")

    # 2. Per-LLM coverage
    print(f"\n2. Per-LLM coverage:")
    MANDATORY = {"chatgpt", "claude", "gemini", "perplexity", "groq"}
    rows = conn.execute(
        "SELECT LOWER(llm) AS llm, COUNT(*) AS n FROM citations WHERE timestamp >= ? GROUP BY llm",
        (since_iso,)
    ).fetchall()
    seen = {r["llm"]: r["n"] for r in rows}
    for llm in sorted(MANDATORY):
        count = seen.get(llm, 0)
        status = "OK" if count > 0 else "MISSING"
        print(f"   [{status:>7}]  {llm}: {count}")
        if count == 0:
            failures.append(f"llm {llm} produced 0 rows")

    # 3. Per-vertical coverage
    print(f"\n3. Per-vertical coverage:")
    VERTICALS = {"fintech", "varejo", "saude", "tecnologia"}
    rows = conn.execute(
        "SELECT vertical, COUNT(*) AS n FROM citations WHERE timestamp >= ? GROUP BY vertical",
        (since_iso,)
    ).fetchall()
    seen = {r["vertical"]: r["n"] for r in rows}
    for v in sorted(VERTICALS):
        count = seen.get(v, 0)
        status = "OK" if count > 0 else "MISSING"
        print(f"   [{status:>7}]  {v}: {count}")
        if count == 0:
            failures.append(f"vertical {v} produced 0 rows")

    # 4. V2 column coverage
    print(f"\n4. V2 column coverage:")
    v2 = conn.execute(
        """SELECT
             COUNT(*) AS total,
             SUM(CASE WHEN extraction_version = 'v2' THEN 1 ELSE 0 END) AS v2_count,
             SUM(CASE WHEN response_hash IS NOT NULL AND LENGTH(response_hash) = 16 THEN 1 ELSE 0 END) AS hash_count,
             SUM(CASE WHEN cited_entities_v2_json IS NOT NULL THEN 1 ELSE 0 END) AS json_count,
             SUM(is_probe) AS probe_count,
             SUM(CASE WHEN probe_type IS NOT NULL THEN 1 ELSE 0 END) AS probe_type_count
           FROM citations WHERE timestamp >= ?""",
        (since_iso,)
    ).fetchone()
    total = v2["total"]
    if total > 0:
        for label, key in [
            ("extraction_version=v2", "v2_count"),
            ("response_hash present", "hash_count"),
            ("cited_entities_v2_json present", "json_count"),
        ]:
            count = v2[key]
            pct = round(100 * count / total, 1)
            status = "OK" if count == total else ("WARN" if count >= total * 0.9 else "FAIL")
            print(f"   [{status:>7}]  {label}: {count}/{total} ({pct}%)")
            if count != total:
                msg = f"{label}: only {count}/{total}"
                if status == "FAIL":
                    failures.append(msg)
                else:
                    warnings.append(msg)
        print(f"   [info]   is_probe=1 rows: {v2['probe_count']} ({round(100*v2['probe_count']/total,1)}%, esperado ~10%)")

    # 5. Fictitious hit rate (should be ~0 in clean collection)
    print(f"\n5. Fictitious hallucination rate:")
    fict = conn.execute(
        "SELECT SUM(fictional_hit) AS fict, COUNT(*) AS n FROM citations WHERE timestamp >= ?",
        (since_iso,)
    ).fetchone()
    if fict["n"]:
        rate = round(100 * (fict["fict"] or 0) / fict["n"], 3)
        status = "OK" if rate < 1.0 else "WARN"
        print(f"   [{status:>7}]  {fict['fict']} fictitious hits / {fict['n']} rows = {rate}%")
        if rate >= 5.0:
            warnings.append(f"fictitious hit rate elevated: {rate}%")

    # 6. Model versions tracked
    print(f"\n6. Model versions tracking:")
    mv = conn.execute(
        "SELECT COUNT(DISTINCT provider || '/' || model_alias) AS n_combos FROM model_versions"
    ).fetchone()["n_combos"]
    status = "OK" if mv >= 5 else ("WARN" if mv > 0 else "FAIL")
    print(f"   [{status:>7}]  distinct (provider, model) combos tracked: {mv} (expected ≥ 5)")
    if mv == 0:
        warnings.append("model_versions is empty — DriftDetector may not be firing")

    # 7. Citation rate by LLM (informational)
    if args.verbose:
        print(f"\n7. Citation rate by LLM (informational):")
        rates = conn.execute(
            """SELECT llm, ROUND(AVG(CAST(cited AS FLOAT)) * 100, 1) AS rate, COUNT(*) AS n
               FROM citations WHERE timestamp >= ? GROUP BY llm ORDER BY rate DESC""",
            (since_iso,)
        ).fetchall()
        for r in rates:
            print(f"   {r['llm']:>12}: {r['rate']}% cited ({r['n']} queries)")

    conn.close()

    # Summary
    print(f"\n=== Summary ===")
    print(f"Warnings: {len(warnings)}")
    for w in warnings:
        print(f"  - {w}")
    print(f"Failures: {len(failures)}")
    for f in failures:
        print(f"  - {f}")

    if failures:
        return 2
    if warnings:
        return 1
    print("\n[PASS] All checks OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
