"""Migration 0011 — engine_call_outcomes: success, failure and timeout per engine call.

Motivação (30/09/2026). O fork treg retirou a Perplexity do seu painel de
visibilidade em IA com base em dado, não em impressão: em 14 dias de produção,
1.395 chamadas, 51% falharam e 38% passaram de 90 s, contra 0,3% a 8% nos outros
quatro motores. Este repositório não tinha como fazer a mesma conta: a tabela
`collection_runs` registra o resultado por módulo e vertical, e a tabela
`citations` só guarda as chamadas que deram certo. A falha de um motor sumia
do banco, e a decisão de manter ou retirar um braço ficava sem denominador.

A tabela nova guarda um registro por chamada a um motor, com o desfecho
(`success`, `failure`, `timeout`, `skipped`), a latência, o código HTTP e a
classe do erro. `arm` separa o braço de API (`api`) do braço de interface
(`interface`, coleta pela interface do produto via Cloro), porque a mesma marca
de motor falha de modos diferentes em cada um.

`skipped` existe para o motor que não atende o país pedido (a Cloro recusa, por
exemplo, CN e RU no ChatGPT): não é falha e fica fora do denominador.

Forward-only e idempotente (CREATE ... IF NOT EXISTS). Não altera dado existente.
"""
from __future__ import annotations

import logging
import sqlite3

logger = logging.getLogger(__name__)

OUTCOME_STATUSES: tuple[str, ...] = ("success", "failure", "timeout", "skipped")

DDL = """
CREATE TABLE IF NOT EXISTS engine_call_outcomes (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp    TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    engine       TEXT NOT NULL,
    arm          TEXT NOT NULL DEFAULT 'api',
    provider     TEXT NOT NULL DEFAULT '',
    status       TEXT NOT NULL,
    latency_ms   INTEGER,
    http_status  INTEGER,
    error_class  TEXT,
    vertical     TEXT NOT NULL DEFAULT '',
    run_id       TEXT NOT NULL DEFAULT '',
    CHECK (status IN ('success', 'failure', 'timeout', 'skipped')),
    CHECK (arm IN ('api', 'interface'))
);
CREATE INDEX IF NOT EXISTS idx_engine_outcomes_engine_ts ON engine_call_outcomes(engine, timestamp);
CREATE INDEX IF NOT EXISTS idx_engine_outcomes_arm ON engine_call_outcomes(arm);
"""


def apply(conn: sqlite3.Connection) -> bool:
    """Create the table if missing. Returns True when it was created now."""
    existed = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name='engine_call_outcomes'"
    ).fetchone()
    conn.executescript(DDL)
    conn.commit()
    if not existed:
        logger.info("migrate_0011_engine_call_outcomes: tabela criada")
    return not existed
