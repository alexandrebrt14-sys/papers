"""Base collector interface and LLM query helpers."""

from __future__ import annotations

import json
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

import httpx

from src.config import LLMConfig, config
from src.finops.tracker import FinOpsTracker, get_tracker

logger = logging.getLogger(__name__)


@dataclass
class LLMResponse:
    """Structured response from an LLM query."""
    model: str
    provider: str
    query: str
    response_text: str
    sources: list[str]
    timestamp: str
    latency_ms: int
    token_count: int | None = None
    input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float = 0.0
    raw: dict[str, Any] | None = None


class LLMClient:
    """Unified client for querying multiple LLM providers.

    Integrated with FinOps: every query is automatically cost-tracked
    using real token counts from API responses. Budget checks run
    BEFORE each query; recording runs AFTER.
    """

    def __init__(self, finops: FinOpsTracker | None = None) -> None:
        self._http = httpx.Client(timeout=60.0)
        self._finops = finops or get_tracker()
        self._run_id = ""

    def set_run_id(self, run_id: str) -> None:
        """Set run_id for cost attribution across a collection run."""
        self._run_id = run_id

    def query(self, llm: LLMConfig, prompt: str, operation: str = "llm_query") -> LLMResponse | None:
        """Send a query to an LLM and return structured response.

        Automatically:
        1. Checks budget BEFORE calling API (can_spend)
        2. Extracts REAL token counts from API response
        3. Records cost in FinOps tracker
        """
        if llm.requires_scraping:
            logger.warning(f"{llm.name} requires scraping — skipping in API mode")
            return None
        if not llm.api_key:
            logger.warning(f"{llm.name} has no API key configured — skipping")
            return None

        # Pre-flight: check budget
        if not self._finops.can_spend(llm.provider):
            logger.warning(f"[finops] {llm.name} BLOCKED by budget — skipping query")
            return None

        start = datetime.now(timezone.utc)
        response: LLMResponse | None = None
        try:
            if llm.provider == "openai":
                response = self._query_openai(llm, prompt, start)
            elif llm.provider == "anthropic":
                response = self._query_anthropic(llm, prompt, start)
            elif llm.provider == "google":
                response = self._query_google(llm, prompt, start)
            elif llm.provider == "perplexity":
                response = self._query_perplexity(llm, prompt, start)
            else:
                logger.error(f"Unknown provider: {llm.provider}")
                return None
        except Exception as e:
            logger.error(f"Error querying {llm.name}: {e}")
            return None

        # Post-flight: record cost with REAL tokens from API
        if response and response.raw:
            in_tok, out_tok = FinOpsTracker.extract_tokens(llm.provider, response.raw)
            record = self._finops.record(
                platform=llm.provider,
                model=llm.model,
                operation=operation,
                input_tokens=in_tok,
                output_tokens=out_tok,
                query=prompt,
                run_id=self._run_id,
                raw_response=response.raw,
            )
            # Enrich response with cost data
            response.input_tokens = record.input_tokens
            response.output_tokens = record.output_tokens
            response.cost_usd = record.cost_usd

        return response

    def _query_openai(self, llm: LLMConfig, prompt: str, start: datetime) -> LLMResponse:
        """Query OpenAI ChatGPT."""
        resp = self._http.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {llm.api_key}"},
            json={
                "model": llm.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.0,
            },
        )
        resp.raise_for_status()
        data = resp.json()
        latency = int((datetime.now(timezone.utc) - start).total_seconds() * 1000)
        text = data["choices"][0]["message"]["content"]
        return LLMResponse(
            model=llm.model,
            provider=llm.provider,
            query=prompt,
            response_text=text,
            sources=self._extract_urls(text),
            timestamp=start.isoformat(),
            latency_ms=latency,
            token_count=data.get("usage", {}).get("total_tokens"),
            raw=data,
        )

    def _query_anthropic(self, llm: LLMConfig, prompt: str, start: datetime) -> LLMResponse:
        """Query Anthropic Claude."""
        resp = self._http.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": llm.api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": llm.model,
                "max_tokens": 4096,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.0,
            },
        )
        resp.raise_for_status()
        data = resp.json()
        latency = int((datetime.now(timezone.utc) - start).total_seconds() * 1000)
        text = data["content"][0]["text"]
        return LLMResponse(
            model=llm.model,
            provider=llm.provider,
            query=prompt,
            response_text=text,
            sources=self._extract_urls(text),
            timestamp=start.isoformat(),
            latency_ms=latency,
            token_count=data.get("usage", {}).get("input_tokens", 0)
            + data.get("usage", {}).get("output_tokens", 0),
            raw=data,
        )

    def _query_google(self, llm: LLMConfig, prompt: str, start: datetime) -> LLMResponse:
        """Query Google Gemini."""
        resp = self._http.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/{llm.model}:generateContent",
            params={"key": llm.api_key},
            json={
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.0},
            },
        )
        resp.raise_for_status()
        data = resp.json()
        latency = int((datetime.now(timezone.utc) - start).total_seconds() * 1000)
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        return LLMResponse(
            model=llm.model,
            provider=llm.provider,
            query=prompt,
            response_text=text,
            sources=self._extract_urls(text),
            timestamp=start.isoformat(),
            latency_ms=latency,
            token_count=data.get("usageMetadata", {}).get("totalTokenCount"),
            raw=data,
        )

    def _query_perplexity(self, llm: LLMConfig, prompt: str, start: datetime) -> LLMResponse:
        """Query Perplexity (OpenAI-compatible API)."""
        resp = self._http.post(
            "https://api.perplexity.ai/chat/completions",
            headers={"Authorization": f"Bearer {llm.api_key}"},
            json={
                "model": llm.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.0,
            },
        )
        resp.raise_for_status()
        data = resp.json()
        latency = int((datetime.now(timezone.utc) - start).total_seconds() * 1000)
        text = data["choices"][0]["message"]["content"]
        # Perplexity includes citations in response
        citations = data.get("citations", [])
        sources = citations if citations else self._extract_urls(text)
        return LLMResponse(
            model=llm.model,
            provider=llm.provider,
            query=prompt,
            response_text=text,
            sources=sources,
            timestamp=start.isoformat(),
            latency_ms=latency,
            token_count=data.get("usage", {}).get("total_tokens"),
            raw=data,
        )

    @staticmethod
    def _extract_urls(text: str) -> list[str]:
        """Extract URLs from response text."""
        import re
        return re.findall(r'https?://[^\s\)\]>"\']+', text)

    def close(self) -> None:
        self._http.close()


class BaseCollector(ABC):
    """Base class for all data collection modules."""

    def __init__(self) -> None:
        self.llm_client = LLMClient()
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def collect(self) -> list[dict[str, Any]]:
        """Run the collection and return structured results."""
        ...

    @abstractmethod
    def module_name(self) -> str:
        """Return the module identifier."""
        ...

    def close(self) -> None:
        self.llm_client.close()
