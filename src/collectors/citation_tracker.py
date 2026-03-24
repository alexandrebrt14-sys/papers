"""Module 1: Multi-LLM Citation Tracker.

Monitors whether the primary entity (Brasil GEO / Alexandre Caramaschi) is cited
across 5 LLMs for a standardized set of queries. Captures: cited (bool), position,
full response context, sentiment, sources listed, timestamp.
"""

from __future__ import annotations

import re
from typing import Any

from src.config import STANDARD_QUERIES, config
from src.collectors.base import BaseCollector, LLMResponse


class CitationTracker(BaseCollector):
    """Track citations of the primary entity across multiple LLMs."""

    def module_name(self) -> str:
        return "citation_tracker"

    def collect(self) -> list[dict[str, Any]]:
        """Query all configured LLMs with standard queries and analyze citations."""
        results: list[dict[str, Any]] = []

        for q in STANDARD_QUERIES:
            for llm_cfg in self.config.llms:
                self.logger.info(f"[{llm_cfg.name}] Query: {q['query'][:60]}...")
                response = self.llm_client.query(llm_cfg, q["query"])
                if response is None:
                    continue

                analysis = self._analyze_citation(response)
                results.append({
                    "module": self.module_name(),
                    "llm": llm_cfg.name,
                    "model": response.model,
                    "query": q["query"],
                    "query_category": q["category"],
                    "query_lang": q["lang"],
                    "timestamp": response.timestamp,
                    "latency_ms": response.latency_ms,
                    "token_count": response.token_count,
                    **analysis,
                })

        self.logger.info(f"Collected {len(results)} citation records")
        return results

    def _analyze_citation(self, response: LLMResponse) -> dict[str, Any]:
        """Analyze a single LLM response for citations of the primary entity."""
        text = response.response_text.lower()
        entity = self.config.primary_entity.lower()
        domain = self.config.primary_domain.lower()
        secondary = self.config.secondary_domain.lower()
        person = "alexandre caramaschi"

        # Check if cited
        cited_entity = entity in text
        cited_domain = domain in text
        cited_secondary = secondary in text
        cited_person = person in text
        cited = cited_entity or cited_domain or cited_secondary or cited_person

        # Determine position (first third, second third, final third)
        position = None
        if cited:
            for term in [entity, person, domain, secondary]:
                idx = text.find(term)
                if idx >= 0:
                    relative = idx / max(len(text), 1)
                    if relative < 0.33:
                        position = 1
                    elif relative < 0.66:
                        position = 2
                    else:
                        position = 3
                    break

        # Check attribution type
        attribution = "none"
        if cited_domain or cited_secondary:
            attribution = "linked"
        elif cited_entity or cited_person:
            attribution = "named"

        # Count how many sources the LLM listed
        source_count = len(response.sources)
        our_sources = [s for s in response.sources if domain in s or secondary in s]

        # Detect hedging language
        hedging_patterns = [
            r"according to", r"segundo", r"reportedly", r"supostamente",
            r"it is claimed", r"some suggest", r"may be", r"possibly",
            r"possivelmente", r"aparentemente",
        ]
        hedging = any(re.search(p, text) for p in hedging_patterns)

        return {
            "cited": cited,
            "cited_entity": cited_entity,
            "cited_domain": cited_domain,
            "cited_person": cited_person,
            "position": position,
            "attribution": attribution,
            "source_count": source_count,
            "our_source_count": len(our_sources),
            "our_sources": our_sources,
            "hedging_detected": hedging,
            "response_length": len(response.response_text),
            "response_text": response.response_text,
            "all_sources": response.sources,
        }
