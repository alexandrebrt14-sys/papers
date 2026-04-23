#!/usr/bin/env python3
"""reextract_citations.py — popular colunas *_v2 com o NER v2.

Contexto: Onda 2 do plano de correção do algoritmo papers (2026-04-23).
Após migration 0005, re-processa todas as rows históricas usando
EntityExtractor para gerar as métricas corrigidas (G1-G7 do Agent C audit).

Preserva intocada a série v1. Permite comparação v1↔v2 para medir impacto
das correções (estimativa preliminar: 5-15% delta em `cited`).

Uso:
    # Dry-run (não grava, reporta estatísticas):
    python scripts/reextract_citations.py --dry-run

    # Aplica migration e re-extrai tudo:
    python scripts/reextract_citations.py

    # Re-extrai só uma vertical:
    python scripts/reextract_citations.py --vertical fintech

    # Limita batch:
    python scripts/reextract_citations.py --limit 100
"""
from __future__ import annotations

import argparse
import json
import logging
import sqlite3
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.analysis.entity_extraction import (
    EntityExtractor,
    position_tercile,
)
from src.config import (
    AMBIGUOUS_ENTITIES,
    CANONICAL_NAMES,
    ENTITY_ALIASES,
    ENTITY_STOP_CONTEXTS,
    get_real_cohort,
    list_verticals,
)
from src.db.migrate_0005_ner_v2 import apply as apply_migration_0005

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("reextract")


# Consolidação 2026-04-23: ALIASES e STOP_CONTEXTS foram migrados para
# src/config.py (ENTITY_ALIASES, ENTITY_STOP_CONTEXTS) como single source
# of truth. Este script apenas consome — evitando drift entre NER online
# e re-extração offline.

# Aliases backward-compat para imports externos (tests, notebooks):
ALIASES = ENTITY_ALIASES
STOP_CONTEXTS = ENTITY_STOP_CONTEXTS


def build_extractor(vertical: str) -> EntityExtractor:
    """Constrói EntityExtractor com cohort REAL (exclui fictícias).

    Fictícias são processadas separadamente via `build_probe_extractor`
    em scripts de análise de hallucination (probe_type='decoy').
    """
    cohort = get_real_cohort(vertical)
    return EntityExtractor(
        cohort=cohort,
        aliases=ENTITY_ALIASES,
        ambiguous=set(AMBIGUOUS_ENTITIES),
        canonical_names=CANONICAL_NAMES,
        stop_contexts=ENTITY_STOP_CONTEXTS,
    )


def reextract_row(row: sqlite3.Row, extractor: EntityExtractor) -> dict[str, Any]:
    """Extrai métricas v2 para uma única row de `citations`."""
    text = row["response_text"] or ""
    mentions = extractor.extract(text)

    cited = bool(mentions)
    cited_count = len(mentions)
    cited_entities = [m.entity for m in mentions]

    first_entity = mentions[0].entity if mentions else None
    first_offset = mentions[0].start if mentions else None
    response_length = len(text)
    position = (
        position_tercile(mentions[0].start, response_length)
        if mentions else None
    )

    via_alias = sum(1 for m in mentions if m.via_alias)
    via_fold = sum(1 for m in mentions if m.via_fold)

    return {
        "cited_v2": int(cited),
        "cited_count_v2": cited_count,
        "cited_entities_v2_json": json.dumps(cited_entities, ensure_ascii=False),
        "first_entity_v2": first_entity,
        "first_entity_offset_v2": first_offset,
        "position_v2": position,
        "via_alias_count_v2": via_alias,
        "via_fold_count_v2": via_fold,
        "response_length_chars_v2": response_length,
        "extraction_version": "v2",
        "extracted_at_v2": datetime.now(timezone.utc).isoformat(),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default="data/papers.db")
    ap.add_argument("--vertical", default=None,
                    help="Filtra por vertical (default: todas)")
    ap.add_argument("--limit", type=int, default=None,
                    help="Processa apenas N rows (teste)")
    ap.add_argument("--dry-run", action="store_true",
                    help="Não grava; reporta delta v1 vs v2")
    ap.add_argument("--force", action="store_true",
                    help="Re-extrai rows já em v2")
    args = ap.parse_args()

    db_path = Path(args.db).resolve()
    if not db_path.exists():
        log.error("DB não encontrado: %s", db_path)
        return 1

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row

    # Apply migration se necessário (mesmo em dry-run, para permitir filtrar
    # por extraction_version). Migration é idempotente e forward-only.
    added = apply_migration_0005(conn)
    if added:
        log.info("Migration 0005 aplicada: %d colunas novas", len(added))

    verticals = [args.vertical] if args.vertical else list_verticals()
    log.info("Verticals: %s", verticals)

    # Agregados para resumo
    stats = {
        "total_processed": 0,
        "v1_cited": 0, "v2_cited": 0,
        "v1_only": 0, "v2_only": 0, "both": 0,
        "via_alias_total": 0, "via_fold_total": 0,
    }
    deltas = []

    for vert in verticals:
        extractor = build_extractor(vert)
        log.info("Processing vertical %s (real cohort size: %d)", vert,
                 len(get_real_cohort(vert)))

        where = "WHERE vertical = ? AND response_text IS NOT NULL"
        params: list[Any] = [vert]
        if not args.force:
            where += " AND (extraction_version IS NULL OR extraction_version = 'v1')"
        if args.limit:
            query = f"SELECT * FROM citations {where} ORDER BY id LIMIT ?"
            params.append(args.limit)
        else:
            query = f"SELECT * FROM citations {where} ORDER BY id"

        rows = conn.execute(query, params).fetchall()
        log.info("  %d rows to re-extract", len(rows))

        t0 = time.time()
        for row in rows:
            v2 = reextract_row(row, extractor)
            stats["total_processed"] += 1
            stats["v1_cited"] += int(bool(row["cited"]))
            stats["v2_cited"] += v2["cited_v2"]
            stats["via_alias_total"] += v2["via_alias_count_v2"]
            stats["via_fold_total"] += v2["via_fold_count_v2"]
            if row["cited"] and v2["cited_v2"]:
                stats["both"] += 1
            elif row["cited"] and not v2["cited_v2"]:
                stats["v1_only"] += 1
            elif not row["cited"] and v2["cited_v2"]:
                stats["v2_only"] += 1
                deltas.append((row["id"], row["query"][:60], row["llm"],
                              json.loads(row.get("all_cited_entities",
                                                  "[]") if False else "[]")))

            if not args.dry_run:
                conn.execute(
                    """
                    UPDATE citations SET
                        cited_v2 = ?,
                        cited_count_v2 = ?,
                        cited_entities_v2_json = ?,
                        first_entity_v2 = ?,
                        first_entity_offset_v2 = ?,
                        position_v2 = ?,
                        via_alias_count_v2 = ?,
                        via_fold_count_v2 = ?,
                        response_length_chars_v2 = ?,
                        extraction_version = ?,
                        extracted_at_v2 = ?
                    WHERE id = ?
                    """,
                    (
                        v2["cited_v2"], v2["cited_count_v2"],
                        v2["cited_entities_v2_json"],
                        v2["first_entity_v2"], v2["first_entity_offset_v2"],
                        v2["position_v2"], v2["via_alias_count_v2"],
                        v2["via_fold_count_v2"],
                        v2["response_length_chars_v2"],
                        v2["extraction_version"], v2["extracted_at_v2"],
                        row["id"],
                    ),
                )

        elapsed = time.time() - t0
        log.info("  done %d rows in %.1fs (%.1f rows/s)", len(rows), elapsed,
                 len(rows) / max(elapsed, 0.001))

    if not args.dry_run:
        conn.commit()

    log.info("=" * 60)
    log.info("REEXTRACTION SUMMARY")
    log.info("=" * 60)
    log.info(f"  Total processed:     {stats['total_processed']}")
    log.info(f"  v1 cited:            {stats['v1_cited']}")
    log.info(f"  v2 cited:            {stats['v2_cited']}")
    log.info(f"  Delta (v2-v1):       {stats['v2_cited'] - stats['v1_cited']:+d}")
    log.info(f"  Both v1 & v2:        {stats['both']}")
    log.info(f"  v1-only (v2 misses): {stats['v1_only']}")
    log.info(f"  v2-only (v2 gains):  {stats['v2_only']}")
    log.info(f"  Via alias total:     {stats['via_alias_total']}")
    log.info(f"  Via fold total:      {stats['via_fold_total']}")

    if args.dry_run:
        log.info("  [DRY-RUN — sem gravação]")
    else:
        log.info("  [DB atualizado com colunas _v2]")

    conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
