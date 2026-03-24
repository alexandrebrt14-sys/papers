"""Module 3: SERP vs AI Overlap Tracker.

Measures divergence between traditional Google SERP results and AI-generated responses
for the same queries. Proves empirically that GEO is different from SEO.
"""

from __future__ import annotations

from typing import Any
from urllib.parse import urlparse

import httpx

from src.config import STANDARD_QUERIES, config
from src.collectors.base import BaseCollector


class SerpAIOverlap(BaseCollector):
    """Track overlap between Google SERP and AI responses."""

    def module_name(self) -> str:
        return "serp_ai_overlap"

    def collect(self) -> list[dict[str, Any]]:
        """Compare Google SERP with LLM responses for each query."""
        results: list[dict[str, Any]] = []

        # Use English queries for SERP (Google is English-primary for API)
        serp_queries = [q for q in STANDARD_QUERIES if q["lang"] == "en"]

        for q in serp_queries:
            # Get Google SERP top 10
            serp_domains = self._get_serp_domains(q["query"])
            if not serp_domains:
                self.logger.warning(f"No SERP data for: {q['query'][:50]}")
                continue

            # Query each LLM and compare
            for llm_cfg in self.config.llms:
                response = self.llm_client.query(llm_cfg, q["query"])
                if response is None:
                    continue

                ai_domains = self._extract_domains(response.sources)

                # Calculate overlap
                serp_set = set(serp_domains)
                ai_set = set(ai_domains)
                overlap = serp_set & ai_set
                serp_only = serp_set - ai_set
                ai_only = ai_set - serp_set
                overlap_pct = len(overlap) / max(len(serp_set | ai_set), 1) * 100

                results.append({
                    "module": self.module_name(),
                    "llm": llm_cfg.name,
                    "model": response.model,
                    "query": q["query"],
                    "query_category": q["category"],
                    "timestamp": response.timestamp,
                    "serp_domain_count": len(serp_set),
                    "ai_domain_count": len(ai_set),
                    "overlap_count": len(overlap),
                    "overlap_pct": round(overlap_pct, 1),
                    "serp_only_count": len(serp_only),
                    "ai_only_count": len(ai_only),
                    "overlap_domains": sorted(overlap),
                    "serp_only_domains": sorted(serp_only),
                    "ai_only_domains": sorted(ai_only),
                    "primary_in_serp": self.config.primary_domain in serp_set,
                    "primary_in_ai": self.config.primary_domain in ai_set,
                })

        self.logger.info(f"Collected {len(results)} SERP-AI overlap records")
        return results

    def _get_serp_domains(self, query: str) -> list[str]:
        """Fetch Google SERP top 10 domains via SerpAPI."""
        if not self.config.serpapi_key:
            self.logger.warning("SERPAPI_KEY not configured — using empty SERP")
            return []

        try:
            resp = httpx.get(
                "https://serpapi.com/search",
                params={
                    "q": query,
                    "api_key": self.config.serpapi_key,
                    "num": 10,
                    "engine": "google",
                },
                timeout=30.0,
            )
            resp.raise_for_status()
            data = resp.json()
            results = data.get("organic_results", [])
            return [self._domain_from_url(r["link"]) for r in results if "link" in r]
        except Exception as e:
            self.logger.error(f"SerpAPI error: {e}")
            return []

    @staticmethod
    def _domain_from_url(url: str) -> str:
        """Extract root domain from URL."""
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        if domain.startswith("www."):
            domain = domain[4:]
        return domain

    @staticmethod
    def _extract_domains(urls: list[str]) -> list[str]:
        """Extract unique domains from a list of URLs."""
        domains = set()
        for url in urls:
            try:
                parsed = urlparse(url)
                domain = parsed.netloc.lower()
                if domain.startswith("www."):
                    domain = domain[4:]
                if domain:
                    domains.add(domain)
            except Exception:
                continue
        return sorted(domains)
