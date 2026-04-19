"""Brave Search API client (free SERP alternative, replaces SerpAPI).

Extraído de `src/collectors/base.py` em 2026-04-19 (Onda 7).

Plano Brave tier gratuito: 2.000 queries/mês. Usado pelo Módulo 3 (SERP vs
IA overlap) para medir divergência entre resultados de busca tradicional e
respostas generativas.
"""

from __future__ import annotations

import logging

import httpx

from src.config import config

logger = logging.getLogger(__name__)


class BraveSearchClient:
    """Brave Search API — free tier: 2,000 queries/month.
    Replaces SerpAPI ($50/mo) for SERP vs AI overlap tracking.
    """

    def __init__(self, api_key: str = "") -> None:
        self._key = api_key or config.brave_api_key
        self._http = httpx.Client(timeout=15.0)

    def search(self, query: str, count: int = 10) -> list[dict[str, str]]:
        """Return top N organic results as [{title, url, domain}]."""
        if not self._key:
            logger.warning("[brave] No API key — returning empty SERP")
            return []
        try:
            resp = self._http.get(
                "https://api.search.brave.com/res/v1/web/search",
                headers={"X-Subscription-Token": self._key},
                params={"q": query, "count": count},
            )
            resp.raise_for_status()
            data = resp.json()
            results = []
            for r in data.get("web", {}).get("results", []):
                url = r.get("url", "")
                domain = url.split("/")[2] if url.count("/") >= 2 else ""
                if domain.startswith("www."):
                    domain = domain[4:]
                results.append({
                    "title": r.get("title", ""),
                    "url": url,
                    "domain": domain,
                })
            return results
        except Exception as e:
            logger.error(f"[brave] Search error: {e}")
            return []

    def close(self) -> None:
        self._http.close()
