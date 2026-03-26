"""Module 1: Multi-LLM Citation Tracker (cost-optimized).

Cost comparison (30 queries x 4 LLMs = 120 calls/day):
- OLD: ~$0.80/day — gpt-4o, sonnet, unlimited tokens, free-text
- NEW: ~$0.03/day — mini, haiku, flash(free), JSON mode, 250 max_tokens, cache

Optimizations:
- JSON structured output: LLM returns {cited:[], sources:[], summary:""}
- Entity detection from JSON `cited` array (no regex needed)
- max_tokens=250 prevents verbose responses
- Cache skips identical queries within 20h window
"""

from __future__ import annotations

import re
from typing import Any

from src.collectors.base import BaseCollector, LLMResponse
from src.config import AMBIGUOUS_ENTITIES, CANONICAL_NAMES


class CitationTracker(BaseCollector):
    """Track citations of entities across multiple LLMs."""

    def module_name(self) -> str:
        return "citation_tracker"

    def collect(self) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        cache_hits = 0

        for q in self.queries:
            for llm_cfg in self.config.llms:
                response = self.llm_client.query(llm_cfg, q["query"], category=q.get("category", ""))
                if response is None:
                    continue
                if response.from_cache:
                    cache_hits += 1

                analysis = self._analyze(response)
                results.append({
                    "module": self.module_name(),
                    "llm": llm_cfg.name,
                    "model": response.model,
                    "query": q["query"],
                    "query_category": q["category"],
                    "query_lang": q["lang"],
                    "timestamp": response.timestamp,
                    "latency_ms": response.latency_ms,
                    "input_tokens": response.input_tokens,
                    "output_tokens": response.output_tokens,
                    "from_cache": response.from_cache,
                    **analysis,
                })

        self.logger.info(
            f"Coletados {len(results)} registros "
            f"({cache_hits} do cache, {len(results)-cache_hits} da API)"
        )
        return results

    def _analyze(self, response: LLMResponse) -> dict[str, Any]:
        """Analyze citation data from structured response for cohort entities."""
        cited_lower = [e.lower() for e in response.cited_entities]
        text = response.response_text

        # Check which cohort entities are cited using word boundary matching
        cohort_cited: dict[str, bool] = {}
        for entity in self.cohort:
            entity_lower = entity.lower()
            in_cited_list = any(entity_lower in c or c in entity_lower for c in cited_lower)
            # Word boundary matching for text (Proposal 3)
            if entity in AMBIGUOUS_ENTITIES:
                canonical = CANONICAL_NAMES.get(entity, entity)
                in_text = bool(re.search(r'\b' + re.escape(canonical) + r'\b', text, re.IGNORECASE))
            else:
                in_text = bool(re.search(r'\b' + re.escape(entity) + r'\b', text, re.IGNORECASE))
            cohort_cited[entity] = in_cited_list or in_text

        cited_count = sum(1 for v in cohort_cited.values() if v)
        cited = cited_count > 0

        # List of all cited entities for this query
        cited_entities_list = [e for e, v in cohort_cited.items() if v]

        # Position of first cohort entity in cited_entities order
        position = None
        if cited:
            for i, c in enumerate(cited_lower):
                for entity in self.cohort:
                    if entity.lower() in c or c in entity.lower():
                        total = max(len(cited_lower), 1)
                        position = 1 if i < total / 3 else (2 if i < 2 * total / 3 else 3)
                        break
                if position is not None:
                    break

        return {
            "cited": cited,
            "cited_count": cited_count,
            "cohort_cited": cohort_cited,
            "cited_entity": cited_entities_list[0] if cited_entities_list else None,
            "cited_entities_json": cited_entities_list,
            "position": position,
            "source_count": len(response.sources),
            "response_length": len(response.response_text),
            "response_text": response.response_text,
            "all_sources": response.sources,
            "all_cited_entities": response.cited_entities,
        }
