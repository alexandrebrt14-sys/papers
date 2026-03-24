"""Prompt sensitivity analyzer — test robustness to query reformulation.

Expert critique (Bengio): Results may be specific to the exact phrasing
of each query. A paraphrase of the same question could produce completely
different citation behavior. This module generates variants and measures
agreement between original and reformulated queries.
"""
from __future__ import annotations

import logging
from typing import Any

from src.config import config, STANDARD_QUERIES
from src.collectors.base import BaseCollector, LLMClient

logger = logging.getLogger(__name__)

# Hand-crafted paraphrases for key queries (most robust approach)
QUERY_VARIANTS: list[dict[str, str]] = [
    # Brand queries — test if phrasing affects citation
    {"original": "What is Brasil GEO?",
     "variant": "Tell me about the company Brasil GEO",
     "type": "paraphrase"},
    {"original": "What is Brasil GEO?",
     "variant": "Brasil GEO - what do they do?",
     "type": "reformulation"},

    # Entity queries
    {"original": "Who is Alexandre Caramaschi?",
     "variant": "Tell me about Alexandre Caramaschi's background",
     "type": "paraphrase"},
    {"original": "Who is Alexandre Caramaschi?",
     "variant": "What is Alexandre Caramaschi known for?",
     "type": "reformulation"},

    # Concept queries
    {"original": "What is Generative Engine Optimization GEO?",
     "variant": "Explain GEO - Generative Engine Optimization",
     "type": "paraphrase"},
    {"original": "What is Generative Engine Optimization GEO?",
     "variant": "How does Generative Engine Optimization work?",
     "type": "reformulation"},

    # Technical queries
    {"original": "How does schema markup affect AI citations?",
     "variant": "Does structured data like schema.org help get cited by AI?",
     "type": "paraphrase"},
    {"original": "What is llms.txt and how to implement it?",
     "variant": "Explain the llms.txt standard for AI crawlers",
     "type": "paraphrase"},

    # Market queries
    {"original": "Best GEO tools and platforms 2026",
     "variant": "What tools exist for Generative Engine Optimization in 2026?",
     "type": "paraphrase"},

    # Translation variants
    {"original": "What is Brasil GEO?",
     "variant": "O que é a Brasil GEO?",
     "type": "translation"},
    {"original": "Who is Alexandre Caramaschi?",
     "variant": "Quem é Alexandre Caramaschi?",
     "type": "translation"},
]


class PromptSensitivityAnalyzer(BaseCollector):
    """Measure how sensitive citation results are to query reformulation.

    For each (original, variant) pair, queries the same LLM and checks
    if the citation result agrees (both cite or both don't cite).

    Reports: agreement rate, Cohen's kappa, per-query sensitivity.

    Run weekly (not daily) to save API costs.
    """

    def module_name(self) -> str:
        return "prompt_sensitivity"

    def collect(self) -> list[dict[str, Any]]:
        results = []

        for llm_cfg in self.config.llms:
            if llm_cfg.requires_scraping or not llm_cfg.api_key:
                continue

            for variant in QUERY_VARIANTS:
                try:
                    # Query with original
                    resp_orig = self.llm_client.query(llm_cfg, variant["original"])
                    # Query with variant
                    resp_var = self.llm_client.query(llm_cfg, variant["variant"])

                    if not resp_orig or not resp_var:
                        continue

                    orig_cited = self._has_primary_citation(resp_orig)
                    var_cited = self._has_primary_citation(resp_var)
                    agreement = int(orig_cited == var_cited)

                    results.append({
                        "original_query": variant["original"],
                        "variant_query": variant["variant"],
                        "variant_type": variant["type"],
                        "llm": llm_cfg.provider,
                        "original_cited": int(orig_cited),
                        "variant_cited": int(var_cited),
                        "agreement": agreement,
                    })

                except Exception as e:
                    logger.error(f"Prompt sensitivity error: {e}")

        # Log summary
        if results:
            total = len(results)
            agreed = sum(r["agreement"] for r in results)
            logger.info(
                f"[prompt_sensitivity] Agreement: {agreed}/{total} "
                f"({agreed/total:.1%})"
            )

        return results

    def _has_primary_citation(self, response) -> bool:
        """Check if response cites the primary entity."""
        text = (response.response_text or "").lower()
        entities = [e.lower() for e in (response.cited_entities or [])]

        targets = [
            self.config.primary_entity.lower(),
            self.config.primary_domain.lower(),
            self.config.secondary_domain.lower(),
            "alexandre caramaschi",
        ]

        for target in targets:
            if target in text or target in entities:
                return True
        return False
