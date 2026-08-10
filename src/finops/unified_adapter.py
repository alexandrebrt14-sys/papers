"""Adapter papers -> geo-finops calls.db unificado.

Mantém compat com o tracker SQLite existente (papers.db::finops_usage),
e adicionalmente escreve no calls.db central.
"""

from __future__ import annotations

import logging
import os
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

def _resolver_geo_finops() -> Path | None:
    """Descobre onde o pacote geo_finops vive nesta maquina.

    CORRECAO 2026-08-09. Ate aqui o caminho era o literal
    `Path("C:/Sandyboxclaude/geo-finops")`, que nao existe em maquina nenhuma:
    o diretorio real na estacao do operador se chama `C:/SandyClaude` (grafia
    diferente) e o clone canonico do geo-finops vive junto dos repos irmaos, em
    `.../alexandrebrt14-sys/geo-finops`.

    O efeito era um no-op permanente: `_GEO_FINOPS_PATH.exists()` sempre falso,
    nada entrava no sys.path, o import estourava e o adapter passava a
    descartar toda chamada. Cada registro que deveria alimentar o calls.db
    central simplesmente nao existia, e a unica pista era um logger.warning que
    ninguem le. Custo medido em outro lugar do mesmo ecossistema: o endpoint
    publico de FinOps esta congelado desde 19/04/2026.

    Ordem de resolucao, do mais explicito ao mais provavel:
      1. variavel GEO_FINOPS_PATH, que permite apontar para qualquer lugar;
      2. repo irmao, que e o layout real do GENESIS_GITHUB;
      3. caminhos historicos, mantidos para nao quebrar maquina antiga.
    Valida a existencia do PACOTE (`geo_finops/`), nao so do diretorio: um
    clone vazio nao serve e nao deve passar no teste.
    """
    candidatos: list[Path] = []

    do_ambiente = os.environ.get("GEO_FINOPS_PATH", "").strip()
    if do_ambiente:
        candidatos.append(Path(do_ambiente))

    # .../alexandrebrt14-sys/papers/src/finops/unified_adapter.py
    #  parents[3] = .../alexandrebrt14-sys
    try:
        candidatos.append(Path(__file__).resolve().parents[3] / "geo-finops")
    except IndexError:
        pass

    candidatos.append(Path("C:/SandyClaude/geo-finops"))
    candidatos.append(Path("C:/Sandyboxclaude/geo-finops"))

    for c in candidatos:
        try:
            if (c / "geo_finops").is_dir():
                return c
        except OSError:
            continue
    return None


_GEO_FINOPS_PATH = _resolver_geo_finops()
if _GEO_FINOPS_PATH and str(_GEO_FINOPS_PATH) not in sys.path:
    sys.path.insert(0, str(_GEO_FINOPS_PATH))

try:
    from geo_finops import track_call as _track_call
    _AVAILABLE = True
except ImportError as exc:
    logger.warning(
        "geo_finops nao disponivel em papers adapter (%s). Caminho resolvido: %s. "
        "Enquanto isso, TODA chamada deste projeto fica fora do calls.db central. "
        "Aponte GEO_FINOPS_PATH para o clone do geo-finops para religar.",
        exc,
        _GEO_FINOPS_PATH or "nenhum candidato encontrado",
    )
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
