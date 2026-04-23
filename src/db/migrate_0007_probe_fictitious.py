"""Migration 0007 — probe fictitious design columns.

Resolve H2 design gap: Paper 4 reportou "hallucination rate = 0 / 7052"
mas TODA a série rodou com INCLUDE_FICTITIOUS_ENTITIES=false. O probe
fictício nunca foi ativado. Novas colunas permitem design factorial pra
separar decoy queries (adversarial) de cohort natural:

- `is_probe` BOOLEAN: 1 se esta row é parte de probe fictício
- `probe_type` TEXT: 'control' (baseline natural) OR 'decoy' (adversarial)
- `adversarial_framing` BOOLEAN: se prompt explicitamente força citação
  de nome fictício ("Cite um banco digital com 'Floresta' no nome")
- `fictitious_target` TEXT: nome da entidade fictícia alvo (se decoy)
- `is_calibration` BOOLEAN: 1 se row vem de weekly-calibration.yml
  (isolada da série longitudinal principal)

Forward-only.
"""
from __future__ import annotations

import logging
import sqlite3

logger = logging.getLogger(__name__)


def apply(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()
    existing = {r[1] for r in cur.execute("PRAGMA table_info(citations)").fetchall()}

    additions = [
        ("is_probe",              "INTEGER DEFAULT 0"),
        ("probe_type",            "TEXT"),         # 'control' | 'decoy' | NULL
        ("adversarial_framing",   "INTEGER DEFAULT 0"),
        ("fictitious_target",     "TEXT"),         # ex: "Banco Floresta Digital"
        ("is_calibration",        "INTEGER DEFAULT 0"),
    ]
    added = []
    for col, spec in additions:
        if col not in existing:
            cur.execute(f"ALTER TABLE citations ADD COLUMN {col} {spec}")
            added.append(col)

    # Índices: probes filtrados frequentemente em análise separada
    cur.execute(
        "CREATE INDEX IF NOT EXISTS idx_citations_probe "
        "ON citations(is_probe, probe_type, adversarial_framing)"
    )
    cur.execute(
        "CREATE INDEX IF NOT EXISTS idx_citations_calibration "
        "ON citations(is_calibration)"
    )

    conn.commit()
    logger.info("migrate_0007_probe_fictitious: added %d cols: %s", len(added), added)
    return added
