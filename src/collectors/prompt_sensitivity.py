"""Prompt sensitivity analyzer — test robustness to query reformulation.

Expert critique (Bengio): Results may be specific to the exact phrasing
of each query. A paraphrase of the same question could produce completely
different citation behavior. This module generates variants and measures
agreement between original and reformulated queries.
"""
from __future__ import annotations

import logging
from typing import Any

from src.collectors.base import BaseCollector, LLMClient

logger = logging.getLogger(__name__)

# Hand-crafted paraphrases for key queries (most robust approach)
QUERY_VARIANTS: list[dict[str, str]] = [
    # Fintech entity queries — test if phrasing affects citation
    {"original": "What is Nubank?",
     "variant": "Tell me about the company Nubank",
     "type": "paraphrase"},
    {"original": "What is Nubank?",
     "variant": "Nubank - what do they do?",
     "type": "reformulation"},

    {"original": "Is Nubank safe and reliable?",
     "variant": "Can I trust Nubank with my money?",
     "type": "paraphrase"},
    {"original": "Is Nubank safe and reliable?",
     "variant": "Nubank safety and reliability review",
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

    # Fintech comparison queries
    {"original": "Best digital banks in Brazil 2026",
     "variant": "Which are the top digital banks in Brazil right now?",
     "type": "paraphrase"},
    {"original": "Compare Nubank PagBank Inter C6 Bank",
     "variant": "Nubank vs PagBank vs Banco Inter vs C6 Bank comparison",
     "type": "reformulation"},

    # Translation variants
    {"original": "What is Nubank?",
     "variant": "O que é o Nubank?",
     "type": "translation"},
    {"original": "Best digital banks in Brazil 2026",
     "variant": "Melhores bancos digitais do Brasil 2026",
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
        """Check if response cites any cohort entity."""
        text = (response.response_text or "").lower()
        entities = [e.lower() for e in (response.cited_entities or [])]

        for target in self.cohort:
            target_lower = target.lower()
            if target_lower in text or target_lower in entities:
                return True
        return False
