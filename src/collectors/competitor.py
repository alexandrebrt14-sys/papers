"""Module 2: Competitor Benchmark Dataset.

Monitors the same queries for 5-10 competitor/comparable entities to build a control
group. Without a control group, no journal will accept the research. Measures:
citation frequency, LLM coverage, entity consistency comparison.
"""

from __future__ import annotations

from typing import Any

from src.config import STANDARD_QUERIES, config
from src.collectors.base import BaseCollector


class CompetitorBenchmark(BaseCollector):
    """Track competitor citations for controlled comparison."""

    def module_name(self) -> str:
        return "competitor_benchmark"

    def collect(self) -> list[dict[str, Any]]:
        """Query LLMs and check which competitors are cited."""
        results: list[dict[str, Any]] = []

        if not self.config.competitor_entities:
            self.logger.warning("No competitor entities configured — skipping")
            return results

        # Use a subset of queries (market + concept) for competitor tracking
        competitor_queries = [
            q for q in STANDARD_QUERIES
            if q["category"] in ("concept", "market", "technical")
        ]

        for q in competitor_queries:
            for llm_cfg in self.config.llms:
                response = self.llm_client.query(llm_cfg, q["query"])
                if response is None:
                    continue

                text_lower = response.response_text.lower()

                for competitor in self.config.competitor_entities:
                    cited = competitor.lower() in text_lower
                    position = None
                    if cited:
                        idx = text_lower.find(competitor.lower())
                        relative = idx / max(len(text_lower), 1)
                        position = 1 if relative < 0.33 else (2 if relative < 0.66 else 3)

                    results.append({
                        "module": self.module_name(),
                        "llm": llm_cfg.name,
                        "model": response.model,
                        "query": q["query"],
                        "query_category": q["category"],
                        "query_lang": q["lang"],
                        "timestamp": response.timestamp,
                        "entity": competitor,
                        "entity_type": "competitor",
                        "cited": cited,
                        "position": position,
                        "response_length": len(response.response_text),
                    })

                # Also check primary entity for comparison
                primary_cited = (
                    self.config.primary_entity.lower() in text_lower
                    or self.config.primary_domain.lower() in text_lower
                    or "alexandre caramaschi" in text_lower
                )
                results.append({
                    "module": self.module_name(),
                    "llm": llm_cfg.name,
                    "model": response.model,
                    "query": q["query"],
                    "query_category": q["category"],
                    "query_lang": q["lang"],
                    "timestamp": response.timestamp,
                    "entity": self.config.primary_entity,
                    "entity_type": "primary",
                    "cited": primary_cited,
                    "position": None,
                    "response_length": len(response.response_text),
                })

        self.logger.info(f"Collected {len(results)} competitor benchmark records")
        return results
