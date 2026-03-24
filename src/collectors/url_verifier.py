"""URL verification — detect hallucinated sources.

Expert critique (Aidan Gomez): LLMs return URLs in sources[] that may
be hallucinated. Only Perplexity returns verified URLs from its index.
This module verifies each URL with HTTP HEAD requests to distinguish
real citations from fabricated ones.
"""
from __future__ import annotations

import logging
from typing import Any
from urllib.parse import urlparse

import httpx

logger = logging.getLogger(__name__)


class URLVerifier:
    """Verify URLs returned by LLMs are real (not hallucinated)."""

    def __init__(self, timeout: float = 5.0) -> None:
        self._http = httpx.Client(
            timeout=timeout,
            follow_redirects=True,
            headers={"User-Agent": "Mozilla/5.0 (Papers-Research-Bot)"},
        )

    def verify_url(self, url: str) -> dict[str, Any]:
        """Send HEAD request to verify URL exists."""
        try:
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                return {"url": url, "http_status": 0, "is_real": False, "domain": "", "content_type": ""}

            resp = self._http.head(url)
            domain = parsed.netloc.removeprefix("www.")

            return {
                "url": url,
                "http_status": resp.status_code,
                "is_real": resp.status_code < 400,
                "domain": domain,
                "content_type": resp.headers.get("content-type", "")[:100],
            }
        except Exception:
            return {
                "url": url,
                "http_status": 0,
                "is_real": False,
                "domain": urlparse(url).netloc if url else "",
                "content_type": "",
            }

    def verify_batch(self, urls: list[str], llm: str = "", query: str = "") -> list[dict[str, Any]]:
        """Verify a batch of URLs and add metadata."""
        results = []
        seen = set()
        for url in urls:
            if url in seen or not url.startswith("http"):
                continue
            seen.add(url)
            result = self.verify_url(url)
            result["llm"] = llm
            result["query"] = query[:200]
            results.append(result)
        return results

    def hallucination_rate(self, verifications: list[dict[str, Any]]) -> dict[str, Any]:
        """Compute hallucination rate from verification results."""
        if not verifications:
            return {"total": 0, "real": 0, "hallucinated": 0, "rate": 0.0}
        total = len(verifications)
        real = sum(1 for v in verifications if v["is_real"])
        return {
            "total": total,
            "real": real,
            "hallucinated": total - real,
            "rate": round((total - real) / total, 3) if total > 0 else 0.0,
        }

    def close(self) -> None:
        self._http.close()
