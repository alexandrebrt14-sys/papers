"""Adapter papers -> geo-finops calls.db unificado.

Mantém compat com o tracker SQLite existente (papers.db::finops_usage),
e adicionalmente escreve no calls.db central.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

_GEO_FINOPS_PATH = Path("C:/Sandyboxclaude/geo-finops")
if _GEO_FINOPS_PATH.exists() and str(_GEO_FINOPS_PATH) not in sys.path:
    sys.path.insert(0, str(_GEO_FINOPS_PATH))

try:
    from geo_finops import track_call as _track_call
    _AVAILABLE = True
except ImportError as exc:
    logger.warning("geo_finops nao disponivel em papers adapter: %s", exc)
    _AVAILABLE = False
    _track_call = None


PROJECT_NAME = "papers"


def record(
    platform: str,
    model: str,
    tokens_in: int,
    tokens_out: int,
    cost_usd: float,
    operation: str | None = None,
    vertical: str | None = None,
    run_id: str | None = None,
    timestamp: str | None = None,
) -> None:
    """Espelha record do papers/finops/tracker.py para o calls.db unificado."""
    if not _AVAILABLE:
        return
    try:
        _track_call(
            project=PROJECT_NAME,
            model_id=model,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            cost_usd=cost_usd,
            run_id=run_id,
            task_type=operation or vertical,
            success=True,
            provider=platform,
            timestamp=timestamp,
            metadata={"vertical": vertical} if vertical else None,
        )
    except Exception as exc:
        logger.error("papers unified adapter falhou: %s", exc)
