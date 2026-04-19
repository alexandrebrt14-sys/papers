"""Base collector + re-exports (Onda 7 — split 2026-04-19).

Este módulo foi de 623 linhas (god object: LLMClient + ResponseCache +
BraveSearchClient + BaseCollector) para uma fachada enxuta após extração.

Todos os símbolos antigos continuam importáveis daqui por backward-compat
— nenhum código cliente precisa mudar.

Estrutura após o split:
    src/collectors/
    ├── response_cache.py     — SHA-256 file cache (classe ResponseCache)
    ├── brave_search.py       — Brave Search SERP (classe BraveSearchClient)
    ├── llm_client.py         — LLMResponse + LLMClient (providers, cache, finops)
    └── base.py               — este arquivo: BaseCollector + re-exports
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any

from src.collectors.brave_search import BraveSearchClient
from src.collectors.llm_client import LLMClient, LLMResponse
from src.collectors.response_cache import ResponseCache
from src.config import config, get_cohort, get_queries

logger = logging.getLogger(__name__)


__all__ = [
    "BaseCollector",
    "LLMClient",
    "LLMResponse",
    "ResponseCache",
    "BraveSearchClient",
]


class BaseCollector(ABC):
    """Base class for all data collection modules.

    Accepts a vertical parameter to resolve cohort and queries
    from the VERTICALS registry in config.py.

    O TODO [F1-05] sobre integração do CollectionLogger (anterior a esta
    onda) foi resolvido em Onda 8 (2026-04-19): ``self.structured_logger``
    expõe uma instância de `src.logging.logger.CollectionLogger` de forma
    lazy, sem forçar dependência de disco em testes unitários.
    """

    def __init__(self, vertical: str = "fintech") -> None:
        self.vertical = vertical
        self.cohort = get_cohort(vertical)
        self.queries = get_queries(vertical, include_common=True)
        self.llm_client = LLMClient(cohort=self.cohort, vertical=vertical)
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self._structured_logger = None  # lazy

    @property
    def structured_logger(self):
        """Lazy accessor para CollectionLogger estruturado (Onda 8)."""
        if self._structured_logger is None:
            try:
                from src.logging.logger import CollectionLogger
                self._structured_logger = CollectionLogger(
                    module=self.module_name(),
                    vertical=self.vertical,
                )
            except Exception as exc:
                logger.debug("CollectionLogger indisponível: %s", exc)
                return None
        return self._structured_logger

    @abstractmethod
    def collect(self) -> list[dict[str, Any]]:
        ...

    @abstractmethod
    def module_name(self) -> str:
        ...

    def close(self) -> None:
        self.llm_client.close()
