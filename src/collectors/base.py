"""Base collector with cost-optimized LLM querying.

Optimizations applied:
1. Cheapest models: gpt-4o-mini, haiku-4.5, gemini-flash, sonar
2. Structured JSON output: ~60% fewer output tokens vs free-text
3. max_tokens cap: 250-300 tokens per response (was unlimited ~2000+)
4. System prompt caching: identical prefix across all queries (Anthropic 90% off cached)
5. Local SHA-256 cache: skip identical queries within TTL window (20h default)
6. Brave Search API: free 2K queries/mo (replaces SerpAPI $50/mo)
7. Retry with exponential backoff: handles 429s without wasting budget
8. Multi-vertical support: cohort and queries resolved per vertical
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

import httpx

from src.config import (
    LLMConfig, config, SYSTEM_PROMPT, PERPLEXITY_SYSTEM,
    CACHE_DIR, VERTICALS, get_cohort, get_queries,
    AMBIGUOUS_ENTITIES, CANONICAL_NAMES,
)

logger = logging.getLogger(__name__)


@dataclass
class LLMResponse:
    """Structured response from an LLM query."""
    model: str
    provider: str
    query: str
    response_text: str
    sources: list[str]
    cited_entities: list[str]
    timestamp: str
    latency_ms: int
    token_count: int | None = None
    input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float = 0.0
    from_cache: bool = False
    raw: dict[str, Any] | None = None
    raw_text: str = ""  # Complete unprocessed LLM response before any truncation
    engine_type: str = "parametric"  # "parametric" for ChatGPT/Claude/Gemini, "rag" for Perplexity


# === Response Cache ===

class ResponseCache:
    """SHA-256 keyed file cache to skip identical queries within TTL."""

    def __init__(self, cache_dir: Path = CACHE_DIR, ttl_hours: int = 20) -> None:
        self._dir = cache_dir
        self._dir.mkdir(exist_ok=True)
        self._ttl = timedelta(hours=ttl_hours)

    def _key(self, provider: str, model: str, query: str, vertical: str = "") -> str:
        raw = f"{provider}:{model}:{query}:{vertical}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    def get(self, provider: str, model: str, query: str, vertical: str = "") -> dict | None:
        """Return cached response if within TTL, else None."""
        key = self._key(provider, model, query, vertical)
        path = self._dir / f"{key}.json"
        if not path.exists():
            return None
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            cached_at = datetime.fromisoformat(data["_cached_at"])
            if datetime.now(timezone.utc) - cached_at > self._ttl:
                path.unlink(missing_ok=True)
                return None
            return data
        except Exception:
            path.unlink(missing_ok=True)
            return None

    def put(self, provider: str, model: str, query: str, response: dict, vertical: str = "") -> None:
        """Store response in cache."""
        key = self._key(provider, model, query, vertical)
        path = self._dir / f"{key}.json"
        response["_cached_at"] = datetime.now(timezone.utc).isoformat()
        path.write_text(json.dumps(response, ensure_ascii=False), encoding="utf-8")

    def stats(self) -> dict[str, int]:
        """Return cache stats."""
        files = list(self._dir.glob("*.json"))
        valid = 0
        for f in files:
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                cached_at = datetime.fromisoformat(data["_cached_at"])
                if datetime.now(timezone.utc) - cached_at <= self._ttl:
                    valid += 1
            except Exception:
                pass
        return {"total_files": len(files), "valid": valid, "expired": len(files) - valid}


# === LLM Client ===

class LLMClient:
    """Cost-optimized multi-provider LLM client.

    Per-query cost estimate (30 queries/day, 4 LLMs):
    - Old: ~$0.80/day ($24/mo) — gpt-4o + sonnet + unlimited tokens
    - New: ~$0.04/day ($1.20/mo) — mini + haiku + flash + JSON mode + cache
    """

    MAX_RETRIES = 1
    RETRY_BACKOFF = [3]  # seconds — single retry, then circuit break

    # Per-provider rate limiting (seconds between queries)
    # Gemini billing ativo (R$500 credito) = 30 RPM → 2s between queries
    PROVIDER_DELAY: dict[str, float] = {
        "openai": 0.3,
        "anthropic": 0.3,
        "google": 2.0,      # 30 RPM limit → 60/30 = 2s spacing (billing ativo)
        "perplexity": 0.5,
    }

    # Perplexity query routing: only high-value categories (saves ~50% search cost)
    # Other LLMs receive all queries. Perplexity only where web search adds value.
    PERPLEXITY_CATEGORIES: set[str] = {
        "descoberta",    # Queries de descoberta de marca — alto valor de busca web
        "comparativo",   # Comparativos diretos — Perplexity traz fontes reais
        "reputacao",     # Cross-vertical reputação — busca web essencial
        "mercado",       # Dados de mercado — requer fontes atualizadas
    }

    def __init__(self, cohort: list[str] | None = None, vertical: str = "",
                 json_mode: bool = False) -> None:
        self._http = httpx.Client(timeout=60.0)
        self._cache = ResponseCache(ttl_hours=config.cache_ttl_hours)
        self._run_id = ""
        self._circuit_broken: set[str] = set()
        self._cohort = cohort or config.cohort_entities
        self._vertical = vertical
        self._last_query_time: dict[str, float] = {}  # provider → timestamp
        self._json_mode = json_mode  # If True, use SYSTEM_PROMPT forcing JSON output

    def set_run_id(self, run_id: str) -> None:
        self._run_id = run_id

    def should_query(self, llm: LLMConfig, category: str = "") -> bool:
        """Check if this LLM should receive this query category.

        Perplexity is expensive ($0.005/search) so we route only high-value
        queries to it. Other LLMs receive all queries.
        Returns False if the query should be skipped for this provider.
        """
        if llm.provider == "perplexity" and category:
            return category in self.PERPLEXITY_CATEGORIES
        return True

    def query(self, llm: LLMConfig, prompt: str, category: str = "") -> LLMResponse | None:
        """Query an LLM with all optimizations applied."""
        if llm.requires_scraping or not llm.api_key:
            return None

        # Perplexity query routing: skip low-value categories
        if not self.should_query(llm, category):
            return None

        # Circuit breaker: if this provider already 429'd, skip immediately
        if llm.provider in self._circuit_broken:
            return None

        # 1. Check cache (vertical-aware to prevent cross-vertical collisions)
        cached = self._cache.get(llm.provider, llm.model, prompt, self._vertical)
        if cached:
            logger.debug(f"[cache-hit] {llm.name}/{self._vertical}: {prompt[:40]}...")
            return LLMResponse(
                model=llm.model, provider=llm.provider, query=prompt,
                response_text=cached.get("text", ""),
                sources=cached.get("sources", []),
                cited_entities=cached.get("cited", []),
                timestamp=cached.get("_cached_at", ""),
                latency_ms=0, from_cache=True,
            )

        # 2. Per-provider rate limiting (prevents Gemini 429)
        delay = self.PROVIDER_DELAY.get(llm.provider, 0.3)
        last = self._last_query_time.get(llm.provider, 0)
        elapsed = time.time() - last
        if elapsed < delay and last > 0:
            time.sleep(delay - elapsed)
        self._last_query_time[llm.provider] = time.time()

        # 3. Query with retries
        start = datetime.now(timezone.utc)
        for attempt in range(self.MAX_RETRIES + 1):
            try:
                response = self._dispatch(llm, prompt, start)
                if response:
                    # 3. Cache the response (vertical-aware key)
                    self._cache.put(llm.provider, llm.model, prompt, {
                        "text": response.response_text,
                        "sources": response.sources,
                        "cited": response.cited_entities,
                    }, self._vertical)
                return response
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:
                    if attempt < self.MAX_RETRIES:
                        wait = self.RETRY_BACKOFF[attempt]
                        logger.warning(f"[429] {llm.name} rate-limited, retry in {wait}s...")
                        time.sleep(wait)
                        continue
                    # Circuit break: skip all remaining queries for this provider
                    self._circuit_broken.add(llm.provider)
                    logger.warning(f"[circuit-break] {llm.name} 429 after retries — skipping remaining queries")
                    return None
                logger.error(f"[{llm.name}] HTTP {e.response.status_code}: {e.response.text[:200]}")
                return None
            except Exception as e:
                logger.error(f"[{llm.name}] Error: {e}")
                return None
        return None

    def _dispatch(self, llm: LLMConfig, prompt: str, start: datetime) -> LLMResponse | None:
        """Route to the correct provider."""
        dispatch = {
            "openai": self._query_openai,
            "anthropic": self._query_anthropic,
            "google": self._query_google,
            "perplexity": self._query_perplexity,
        }
        fn = dispatch.get(llm.provider)
        if not fn:
            return None
        return fn(llm, prompt, start)

    def _query_openai(self, llm: LLMConfig, prompt: str, start: datetime) -> LLMResponse:
        """OpenAI query. Uses natural free-text by default; JSON mode only if json_mode=True."""
        messages: list[dict[str, str]] = []
        if self._json_mode:
            messages.append({"role": "system", "content": SYSTEM_PROMPT})
        messages.append({"role": "user", "content": prompt})

        body: dict[str, Any] = {
            "model": llm.model,
            "messages": messages,
            "temperature": 0.0,
            "max_tokens": llm.max_output_tokens,
        }
        if self._json_mode and llm.supports_json_mode:
            body["response_format"] = {"type": "json_object"}

        resp = self._http.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {llm.api_key}"},
            json=body,
        )
        resp.raise_for_status()
        data = resp.json()
        text = data["choices"][0]["message"]["content"]
        usage = data.get("usage", {})

        if self._json_mode:
            parsed = self._parse_json_response(text)
            return self._build_response(
                llm, prompt, start, text, parsed,
                input_tokens=usage.get("prompt_tokens", 0),
                output_tokens=usage.get("completion_tokens", 0),
                raw=data,
            )
        # Natural mode: post-hoc entity extraction from free-text
        posthoc = self._analyze_response_posthoc(text)
        return self._build_response(
            llm, prompt, start, text, posthoc,
            input_tokens=usage.get("prompt_tokens", 0),
            output_tokens=usage.get("completion_tokens", 0),
            raw=data,
        )

    def _query_anthropic(self, llm: LLMConfig, prompt: str, start: datetime) -> LLMResponse:
        """Anthropic query. Uses natural free-text by default; JSON mode only if json_mode=True."""
        body: dict[str, Any] = {
            "model": llm.model,
            "max_tokens": llm.max_output_tokens,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.0,
        }
        if self._json_mode:
            body["system"] = [
                {
                    "type": "text",
                    "text": SYSTEM_PROMPT,
                    "cache_control": {"type": "ephemeral"},  # Prompt caching
                }
            ]

        resp = self._http.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": llm.api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json=body,
        )
        resp.raise_for_status()
        data = resp.json()
        text = data["content"][0]["text"]
        usage = data.get("usage", {})

        if self._json_mode:
            parsed = self._parse_json_response(text)
        else:
            parsed = self._analyze_response_posthoc(text)

        return self._build_response(
            llm, prompt, start, text, parsed,
            input_tokens=usage.get("input_tokens", 0),
            output_tokens=usage.get("output_tokens", 0),
            raw=data,
        )

    def _query_google(self, llm: LLMConfig, prompt: str, start: datetime) -> LLMResponse:
        """Google Gemini query. Uses natural free-text by default; JSON mode only if json_mode=True."""
        if self._json_mode:
            prompt_text = f"{SYSTEM_PROMPT}\n\nQuery: {prompt}"
        else:
            prompt_text = prompt

        body: dict[str, Any] = {
            "contents": [
                {"role": "user", "parts": [{"text": prompt_text}]}
            ],
            "generationConfig": {
                "temperature": 0.0,
                "maxOutputTokens": llm.max_output_tokens,
            },
        }
        if self._json_mode and llm.supports_json_mode:
            body["generationConfig"]["responseMimeType"] = "application/json"

        resp = self._http.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/{llm.model}:generateContent",
            params={"key": llm.api_key},
            json=body,
        )
        resp.raise_for_status()
        data = resp.json()
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        usage = data.get("usageMetadata", {})

        if self._json_mode:
            parsed = self._parse_json_response(text)
        else:
            parsed = self._analyze_response_posthoc(text)

        return self._build_response(
            llm, prompt, start, text, parsed,
            input_tokens=usage.get("promptTokenCount", 0),
            output_tokens=usage.get("candidatesTokenCount", 0),
            raw=data,
        )

    def _query_perplexity(self, llm: LLMConfig, prompt: str, start: datetime) -> LLMResponse:
        """Perplexity with built-in citations (no JSON mode needed)."""
        resp = self._http.post(
            "https://api.perplexity.ai/chat/completions",
            headers={"Authorization": f"Bearer {llm.api_key}"},
            json={
                "model": llm.model,
                "messages": [
                    {"role": "system", "content": PERPLEXITY_SYSTEM},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.0,
                "max_tokens": llm.max_output_tokens,
            },
        )
        resp.raise_for_status()
        data = resp.json()
        text = data["choices"][0]["message"]["content"]
        # Perplexity returns citations in response metadata
        citations = data.get("citations", [])
        sources = citations if citations else self._extract_urls(text)
        usage = data.get("usage", {})

        return LLMResponse(
            model=llm.model, provider=llm.provider, query=prompt,
            response_text=text,
            sources=sources,
            cited_entities=self._extract_entity_mentions(text),
            timestamp=start.isoformat(),
            latency_ms=int((datetime.now(timezone.utc) - start).total_seconds() * 1000),
            input_tokens=usage.get("prompt_tokens", 0),
            output_tokens=usage.get("completion_tokens", 0),
            raw=data,
            raw_text=text,
            engine_type="rag",
        )

    # === Helpers ===

    def _build_response(
        self, llm: LLMConfig, prompt: str, start: datetime,
        text: str, parsed: dict, input_tokens: int, output_tokens: int,
        raw: dict,
    ) -> LLMResponse:
        """Build LLMResponse from parsed output (JSON or post-hoc)."""
        return LLMResponse(
            model=llm.model, provider=llm.provider, query=prompt,
            response_text=parsed.get("summary", text[:200]),
            sources=parsed.get("sources", self._extract_urls(text)),
            cited_entities=parsed.get("cited", self._extract_entity_mentions(text)),
            timestamp=start.isoformat(),
            latency_ms=int((datetime.now(timezone.utc) - start).total_seconds() * 1000),
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            raw=raw,
            raw_text=text,
            engine_type="rag" if llm.provider == "perplexity" else "parametric",
        )

    @staticmethod
    def _parse_json_response(text: str) -> dict:
        """Parse JSON from LLM response, handling edge cases."""
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # Try to extract JSON from markdown code block
            match = re.search(r'\{[^{}]*"cited"[^{}]*\}', text, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group())
                except json.JSONDecodeError:
                    pass
        return {"cited": [], "sources": [], "summary": text[:200]}

    @staticmethod
    def _extract_urls(text: str) -> list[str]:
        return re.findall(r'https?://[^\s\)\]>"\']+', text)

    def _extract_entity_mentions(self, text: str) -> list[str]:
        """Extract known entity mentions from free-text response using word boundary matching.

        Ambiguous entities (e.g., "Neon", "Inter") require their canonical name
        (e.g., "Banco Inter") to avoid false positives from common words.
        """
        entities = []
        for entity in self._cohort:
            if entity in AMBIGUOUS_ENTITIES:
                # Require the full canonical name for ambiguous entities
                canonical = CANONICAL_NAMES.get(entity, entity)
                if re.search(r'\b' + re.escape(canonical) + r'\b', text, re.IGNORECASE):
                    entities.append(entity)
            else:
                if re.search(r'\b' + re.escape(entity) + r'\b', text, re.IGNORECASE):
                    entities.append(entity)
        return entities

    def _analyze_response_posthoc(self, text: str) -> dict:
        """Extract entities from natural free-text response via post-hoc analysis.

        Used in natural (non-JSON) mode: the query goes to the LLM clean,
        and entity extraction happens after the fact using regex word-boundary
        matching against the cohort list.
        """
        cited = self._extract_entity_mentions(text)
        sources = self._extract_urls(text)
        return {
            "cited": cited,
            "sources": sources,
            "summary": text[:200],
        }

    def get_cache_stats(self) -> dict:
        return self._cache.stats()

    def close(self) -> None:
        self._http.close()


# === Brave Search (free SERP alternative) ===

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


# === Base Collector ===

class BaseCollector(ABC):
    """Base class for all data collection modules.

    Accepts a vertical parameter to resolve cohort and queries
    from the VERTICALS registry in config.py.
    """

    # TODO [F1-05]: Integrate CollectionLogger from src.logging.logger into collectors.
    # Replace self.logger with CollectionLogger(self.module_name()) and use its
    # structured log_query() / run() context manager for tracing, metrics, and
    # per-run JSONL log files. Requires updating all subclass collect() methods
    # to yield structured events instead of plain log calls.

    def __init__(self, vertical: str = "fintech") -> None:
        self.vertical = vertical
        self.cohort = get_cohort(vertical)
        self.queries = get_queries(vertical, include_common=True)
        self.llm_client = LLMClient(cohort=self.cohort, vertical=vertical)
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def collect(self) -> list[dict[str, Any]]:
        ...

    @abstractmethod
    def module_name(self) -> str:
        ...

    def close(self) -> None:
        self.llm_client.close()
