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
import os
from abc import ABC, abstractmethod
from typing import Any

from src.collectors.brave_search import BraveSearchClient
from src.collectors.llm_client import LLMClient, LLMResponse
from src.collectors.response_cache import ResponseCache
from src.config import config, get_cohort, get_queries

logger = logging.getLogger(__name__)

# Feature flag da Onda 7 — wire v2 no hot path. Default v2 a partir de 2026-04-24
# (v2-collection-start tag). Quando ativado:
#   1. self.cohort vem de config_v2.get_v2_cohort (real + anchors + decoys)
#   2. self.queries vem de config_v2.get_v2_queries (48 canonical/vertical)
#   3. self.entity_extractor disponibiliza o NER v2 (NFKD, aliases, stops)
#   4. citation_tracker._analyze popula colunas v2 (is_probe, response_hash, ...)
# Para rodar scripts históricos em metodologia v1: export PAPERS_METHODOLOGY_VERSION=v1
DEFAULT_METHODOLOGY_VERSION = "v2"


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
        self.methodology_version = os.getenv(
            "PAPERS_METHODOLOGY_VERSION", DEFAULT_METHODOLOGY_VERSION
        )

        if self.methodology_version == "v2":
            from src.config_v2 import get_v2_cohort, get_v2_queries, get_v2_decoys
            self.cohort = get_v2_cohort(vertical, include_anchors=True, include_decoys=True)
            self.queries = get_v2_queries(vertical)
            self._v2_decoys: set[str] = {d.lower() for d in get_v2_decoys(vertical)}
        else:
            self.cohort = get_cohort(vertical)
            self.queries = get_queries(vertical, include_common=True)
            self._v2_decoys = set()

        self.llm_client = LLMClient(cohort=self.cohort, vertical=vertical)
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self._structured_logger = None  # lazy
        self._entity_extractor = None  # lazy (v2 only)

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

    @property
    def entity_extractor(self):
        """Lazy accessor para EntityExtractor v2 (NER v2 com NFKD+aliases+stops).

        Retorna None em modo v1 (legado), for�ando fallback regex em
        citation_tracker._analyze.
        """
        if self.methodology_version != "v2":
            return None
        if self._entity_extractor is None:
            try:
                from src.analysis.entity_extraction import EntityExtractor
                from src.config import (
                    AMBIGUOUS_ENTITIES, CANONICAL_NAMES,
                    ENTITY_ALIASES, ENTITY_STOP_CONTEXTS,
                )
                self._entity_extractor = EntityExtractor(
                    cohort=self.cohort,
                    aliases=ENTITY_ALIASES,
                    ambiguous=AMBIGUOUS_ENTITIES,
                    canonical_names=CANONICAL_NAMES,
                    stop_contexts=ENTITY_STOP_CONTEXTS,
                )
            except Exception as exc:
                logger.warning("EntityExtractor v2 indisponível: %s — fallback v1", exc)
                return None
        return self._entity_extractor

    @abstractmethod
    def collect(self) -> list[dict[str, Any]]:
        ...

    @abstractmethod
    def module_name(self) -> str:
        ...

    def close(self) -> None:
        self.llm_client.close()
