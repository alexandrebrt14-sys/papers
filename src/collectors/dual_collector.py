"""Dual response collector — JSON structured + natural language.

Addresses expert critique: JSON mode measures self-report (what the LLM
*says* it would cite), not organic behavior (what it *actually* cites).
By collecting both, we can measure the discrepancy and report it.

Also classifies citations as:
- parametric: from model training data (GPT, Claude, Gemini)
- retrieval: from web search/RAG (Perplexity)
"""
from __future__ import annotations

import json
import logging
import re
from typing import Any

from src.config import config, SYSTEM_PROMPT, PERPLEXITY_SYSTEM, LLMConfig
from src.collectors.base import BaseCollector, LLMClient, LLMResponse

logger = logging.getLogger(__name__)

# Natural language prompt (no JSON instruction)
NATURAL_PROMPT = "Answer the following question thoroughly in 2-3 sentences. Cite any sources or entities you reference."

# RAG-based providers (use web retrieval, not just parametric knowledge)
RAG_PROVIDERS = {"perplexity"}


class DualCollector(BaseCollector):
    """Collects both JSON structured and natural language responses per query.

    For each (query, LLM) pair, makes TWO API calls:
    1. JSON mode (existing system prompt) → self-reported citations
    2. Natural language mode → organic citations extracted via regex

    Stores both in dual_responses table for discrepancy analysis.
    """

    def module_name(self) -> str:
        return "dual_collector"

    def collect(self) -> list[dict[str, Any]]:
        results = []
        queries = [q for q in self.queries if q["category"] in ("concept", "technical") or q["category"].startswith(self.vertical)][:10]

        for llm_cfg in self.config.llms:
            if llm_cfg.requires_scraping or not llm_cfg.api_key:
                continue

            for q in queries:
                try:
                    record = self._collect_dual(llm_cfg, q["query"], q["category"])
                    if record:
                        results.append(record)
                except Exception as e:
                    logger.error(f"Dual collection error ({llm_cfg.name}, {q['query'][:40]}): {e}")

        return results

    def _collect_dual(self, llm: LLMConfig, query: str, category: str) -> dict[str, Any] | None:
        # 1. JSON structured response (existing behavior)
        json_response = self.llm_client.query(llm, query)
        if not json_response:
            return None

        # 2. Natural language response (new: organic behavior)
        natural_response = self._query_natural(llm, f"{NATURAL_PROMPT}\n\nQuestion: {query}")

        # Extract entities from natural text
        natural_cited = self._extract_entities_from_text(
            natural_response.response_text if natural_response else ""
        )

        # Classify citation type
        citation_type = "retrieval" if llm.provider in RAG_PROVIDERS else "parametric"
        if not json_response.cited_entities and not natural_cited:
            citation_type = "none"

        # Compute self-report match (Jaccard similarity)
        json_set = set(e.lower() for e in json_response.cited_entities)
        natural_set = set(e.lower() for e in natural_cited)
        union = json_set | natural_set
        match_score = len(json_set & natural_set) / len(union) if union else 1.0

        return {
            "llm": llm.provider,
            "model": llm.model,
            "model_version": self._extract_model_version(json_response),
            "query": query,
            "query_category": category,
            "json_response": json_response.response_text[:500],
            "json_cited": json.dumps(json_response.cited_entities),
            "json_sources": json.dumps(json_response.sources),
            "natural_response": (natural_response.response_text if natural_response else "")[:500],
            "natural_cited": json.dumps(natural_cited),
            "natural_sources": json.dumps(natural_response.sources if natural_response else []),
            "self_report_match": round(match_score, 3),
            "citation_type": citation_type,
        }

    def _query_natural(self, llm: LLMConfig, prompt: str) -> LLMResponse | None:
        """Query LLM in natural language mode (no JSON instruction)."""
        # Create a modified config that doesn't use JSON mode
        from dataclasses import replace
        natural_llm = replace(llm, supports_json_mode=False)
        return self.llm_client.query(natural_llm, prompt)

    def _extract_entities_from_text(self, text: str) -> list[str]:
        """Extract known entity mentions from free-text response."""
        if not text:
            return []
        text_lower = text.lower()
        entities = []
        for entity in self.cohort:
            if entity.lower() in text_lower:
                entities.append(entity)
        return entities

    def _extract_model_version(self, response: LLMResponse) -> str:
        """Extract pinned model version from API response if available."""
        if not response.raw:
            return ""
        # OpenAI returns model with date suffix
        return response.raw.get("model", response.model)
