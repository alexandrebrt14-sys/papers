"""Encerramento definitivo da coleta do projeto papers.

A decisão do responsável em 11/09/2026 encerrou novas observações. A política
não depende do relógio nem de variável de ambiente: outro estudo precisa de
protocolo próprio, sem reabrir a série publicada por configuração.
"""

COLLECTION_CLOSED_ON = "2026-09-11"
COLLECTION_CLOSED_MESSAGE = (
    "O projeto papers encerrou as coletas em 11/09/2026. "
    "Novas coletas e sondas de geração estão bloqueadas. "
    "Os dados existentes permanecem disponíveis para consulta, exportação e análise."
)


class CollectionClosedError(RuntimeError):
    """Tentativa de coletar depois do encerramento definitivo do projeto."""


def require_collection_open() -> None:
    """Recusa a operação antes de consultar cache, rede ou gravar observações."""
    raise CollectionClosedError(COLLECTION_CLOSED_MESSAGE)
