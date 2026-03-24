"""Module 2: Cohort Benchmark Dataset.

Monitors the same queries for the full study cohort (Brazilian fintechs/banks)
to build a comparative dataset. Measures: citation frequency, LLM coverage,
entity consistency comparison.
"""

from __future__ import annotations

from typing import Any

from src.collectors.base import BaseCollector


class CompetitorBenchmark(BaseCollector):
    """Track cohort entity citations for comparative analysis."""

    def module_name(self) -> str:
        return "competitor_benchmark"

    def collect(self) -> list[dict[str, Any]]:
        """Query LLMs and check which cohort entities are cited."""
        results: list[dict[str, Any]] = []

        if not self.cohort:
            self.logger.warning("No cohort entities configured — skipping")
            return results

        # Use a subset of queries relevant to this vertical
        # Include common categories plus any vertical-specific categories
        cohort_queries = [
            q for q in self.queries
            if q["category"] in ("concept", "market", "technical")
            or q["category"].startswith(self.vertical)
        ]

        for q in cohort_queries:
            for llm_cfg in self.config.llms:
                response = self.llm_client.query(llm_cfg, q["query"], category=q.get("category", ""))
                if response is None:
                    continue

                text_lower = response.response_text.lower()

                for entity in self.cohort:
                    cited = entity.lower() in text_lower
                    position = None
                    if cited:
                        idx = text_lower.find(entity.lower())
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
                        "entity": entity,
                        "entity_type": "cohort",
                        "cited": cited,
                        "position": position,
                        "response_length": len(response.response_text),
                    })

        self.logger.info(f"Collected {len(results)} cohort benchmark records")
        return results
