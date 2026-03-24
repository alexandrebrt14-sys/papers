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

from typing import Any

from src.config import STANDARD_QUERIES
from src.collectors.base import BaseCollector, LLMResponse


class CitationTracker(BaseCollector):
    """Track citations of entities across multiple LLMs."""

    def module_name(self) -> str:
        return "citation_tracker"

    def collect(self) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        cache_hits = 0

        for q in STANDARD_QUERIES:
            for llm_cfg in self.config.llms:
                response = self.llm_client.query(llm_cfg, q["query"])
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
        """Analyze citation data from structured response."""
        entity = self.config.primary_entity.lower()
        domain = self.config.primary_domain.lower()
        secondary = self.config.secondary_domain.lower()
        person = "alexandre caramaschi"

        # From JSON structured output
        cited_lower = [e.lower() for e in response.cited_entities]

        cited_entity = any(entity in c or c in entity for c in cited_lower)
        cited_domain = any(domain in c for c in cited_lower) or any(
            domain in s for s in response.sources
        )
        cited_person = any(person in c for c in cited_lower)
        cited_secondary = any(secondary in c for c in cited_lower) or any(
            secondary in s for s in response.sources
        )
        cited = cited_entity or cited_domain or cited_person or cited_secondary

        # Position from cited_entities order (first = prominent)
        position = None
        if cited:
            for i, c in enumerate(cited_lower):
                if entity in c or person in c or domain in c:
                    total = max(len(cited_lower), 1)
                    position = 1 if i < total / 3 else (2 if i < 2 * total / 3 else 3)
                    break

        # Attribution
        attribution = "none"
        if any(domain in s or secondary in s for s in response.sources):
            attribution = "linked"
        elif cited_entity or cited_person:
            attribution = "named"

        our_sources = [s for s in response.sources if domain in s or secondary in s]

        return {
            "cited": cited,
            "cited_entity": cited_entity,
            "cited_domain": cited_domain,
            "cited_person": cited_person,
            "position": position,
            "attribution": attribution,
            "source_count": len(response.sources),
            "our_source_count": len(our_sources),
            "our_sources": our_sources,
            "response_length": len(response.response_text),
            "response_text": response.response_text,
            "all_sources": response.sources,
            "all_cited_entities": response.cited_entities,
        }
