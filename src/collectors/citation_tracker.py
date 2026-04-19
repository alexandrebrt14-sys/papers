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
from src.config import AMBIGUOUS_ENTITIES, CANONICAL_NAMES, is_fictional, query_type_for


class CitationTracker(BaseCollector):
    """Track citations of entities across multiple LLMs."""

    def module_name(self) -> str:
        return "citation_tracker"

    def collect(self) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        cache_hits = 0
        # Onda 8: structured_logger emite 1 evento por query + summary.
        # Lazy — se o módulo de logging falhar em CI sem disco, silently
        # passa adiante.
        slog = self.structured_logger

        for q in self.queries:
            for llm_cfg in self.config.llms:
                response = self.llm_client.query(llm_cfg, q["query"], category=q.get("category", ""))
                if response is None:
                    if slog is not None:
                        slog.log_query(
                            llm=llm_cfg.name,
                            query=q["query"],
                            category=q.get("category", ""),
                            error="skipped_or_failed",
                        )
                    continue
                if response.from_cache:
                    cache_hits += 1

                analysis = self._analyze(response, query_entry=q)
                record = {
                    "module": self.module_name(),
                    "llm": llm_cfg.name,
                    "model": response.model,
                    "query": q["query"],
                    "query_category": q["category"],
                    "query_lang": q["lang"],
                    "query_type": query_type_for(q),
                    "timestamp": response.timestamp,
                    "latency_ms": response.latency_ms,
                    "input_tokens": response.input_tokens,
                    "output_tokens": response.output_tokens,
                    "from_cache": response.from_cache,
                    **analysis,
                }
                results.append(record)

                if slog is not None:
                    slog.log_query(
                        llm=llm_cfg.name,
                        query=q["query"],
                        category=q.get("category", ""),
                        duration_ms=response.latency_ms or 0,
                        tokens=(response.input_tokens + response.output_tokens),
                        cost=response.cost_usd or 0.0,
                        cited=bool(record.get("cited")),
                    )

        self.logger.info(
            f"Coletados {len(results)} registros "
            f"({cache_hits} do cache, {len(results)-cache_hits} da API)"
        )
        if slog is not None:
            summary = slog.get_summary()
            self.logger.info(
                f"[structured] run={summary['run_id']} queries={summary['total_queries']} "
                f"cited={summary['total_cited']} rate={summary['citation_rate']} "
                f"cost=${summary['total_cost_usd']} errors={summary['errors']}"
            )
        return results

    def _analyze(self, response: LLMResponse, query_entry: dict[str, Any] | None = None) -> dict[str, Any]:
        """Analyze citation data from structured response for cohort entities.

        Args:
            response: LLMResponse from provider.
            query_entry: the query dict (used to flag fictional-entity probes).
        """
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

        # False-positive calibration (Onda 3): flag quando a resposta menciona
        # uma entidade fictícia (Proposal 5). target_fictional=True em probe
        # queries E entidade fictícia aparece no texto → sinal de alucinação.
        fictional_hit = False
        fictional_names: list[str] = []
        for name in response.cited_entities:
            if is_fictional(name):
                fictional_hit = True
                fictional_names.append(name)
        # Também checa texto livre (LLMs podem alucinar sem listar em `cited`)
        target_fictional = (query_entry or {}).get("target_fictional")
        if target_fictional and target_fictional.lower() in text.lower():
            fictional_hit = True
            if target_fictional not in fictional_names:
                fictional_names.append(target_fictional)

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
            # False-positive calibration (Onda 3)
            "fictional_hit": fictional_hit,
            "fictional_names": fictional_names,
        }
