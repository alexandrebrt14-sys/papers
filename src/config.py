"""Central configuration for the Papers data collection platform.

Optimized for cost-efficiency:
- Cheapest models per provider (nano/haiku/flash-lite)
- Batch API support (50% discount)
- Structured JSON output (minimal tokens)
- Local response cache (skip repeated queries)
- max_tokens caps (prevent runaway costs)
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
CACHE_DIR = DATA_DIR / "cache"
CACHE_DIR.mkdir(exist_ok=True)


@dataclass(frozen=True)
class LLMConfig:
    """Configuration for a single LLM provider."""
    name: str
    provider: str
    model: str
    api_key: str | None
    input_cost_per_mtok: float   # USD per 1M input tokens
    output_cost_per_mtok: float  # USD per 1M output tokens
    max_output_tokens: int = 300  # Hard cap on response length
    supports_json_mode: bool = True
    supports_batch: bool = False
    batch_discount: float = 0.5   # 50% off via Batch API
    requires_scraping: bool = False


@dataclass(frozen=True)
class CollectionConfig:
    """Global collection configuration."""

    # Primary entity
    primary_entity: str = os.getenv("PRIMARY_ENTITY", "Brasil GEO")
    primary_domain: str = os.getenv("PRIMARY_DOMAIN", "brasilgeo.ai")
    secondary_domain: str = os.getenv("SECONDARY_DOMAIN", "alexandrecaramaschi.com")

    # Competitors
    competitor_entities: list[str] = field(default_factory=lambda: [
        e.strip() for e in os.getenv(
            "COMPETITOR_ENTITIES",
            "Nubank,PagBank,Cielo,Stone,Banco Inter,Mercado Pago,Itaú,Bradesco,C6 Bank,PicPay,Ame Digital,Neon,Original,BS2,Safra"
        ).split(",") if e.strip()
    ])

    # Database
    supabase_url: str = os.getenv("SUPABASE_URL", "")
    supabase_key: str = os.getenv("SUPABASE_KEY", "")
    db_path: str = os.getenv("PAPERS_DB_PATH", str(DATA_DIR / "papers.db"))

    # SERP — Brave Search API (free: 2,000 queries/mo) replaces SerpAPI ($50/mo)
    brave_api_key: str = os.getenv("BRAVE_API_KEY", "")
    serpapi_key: str = os.getenv("SERPAPI_KEY", "")  # Fallback

    # Cache TTL in hours (skip identical queries within this window)
    cache_ttl_hours: int = int(os.getenv("CACHE_TTL_HOURS", "20"))

    # LLMs — optimized: cheapest model per provider that can detect citations
    llms: list[LLMConfig] = field(default_factory=lambda: [
        LLMConfig(
            name="ChatGPT",
            provider="openai",
            model="gpt-4o-mini",          # $0.15/$0.60 per MTok (33x cheaper than gpt-4o)
            api_key=os.getenv("OPENAI_API_KEY"),
            input_cost_per_mtok=0.15,
            output_cost_per_mtok=0.60,
            max_output_tokens=250,
            supports_json_mode=True,
            supports_batch=True,
            batch_discount=0.5,
        ),
        LLMConfig(
            name="Claude",
            provider="anthropic",
            model="claude-haiku-4-5-20251001",  # $1.00/$5.00 per MTok (cheapest Anthropic)
            api_key=os.getenv("ANTHROPIC_API_KEY"),
            input_cost_per_mtok=1.00,
            output_cost_per_mtok=5.00,
            max_output_tokens=250,
            supports_json_mode=True,
            supports_batch=True,
            batch_discount=0.5,
        ),
        LLMConfig(
            name="Gemini",
            provider="google",
            model="gemini-2.0-flash",      # Free tier: 15 RPM, 1M tokens/day
            api_key=os.getenv("GOOGLE_AI_API_KEY"),
            input_cost_per_mtok=0.0,
            output_cost_per_mtok=0.0,
            max_output_tokens=250,
            supports_json_mode=True,
            supports_batch=False,
        ),
        LLMConfig(
            name="Perplexity",
            provider="perplexity",
            model="sonar",                  # $1.00/$1.00 per MTok + $5/1K search requests
            api_key=os.getenv("PERPLEXITY_API_KEY"),
            input_cost_per_mtok=1.00,
            output_cost_per_mtok=1.00,
            max_output_tokens=300,          # Perplexity includes citations, needs more room
            supports_json_mode=False,       # Perplexity doesn't support JSON mode
            supports_batch=False,
        ),
    ])


# === Optimized System Prompt (reused across all queries — enables prompt caching) ===

SYSTEM_PROMPT = """You are a citation analyst. For each user query, respond ONLY with this JSON:
{"cited":[],"sources":[],"summary":""}

Rules:
- "cited": array of entity names mentioned in your answer (exact strings)
- "sources": array of URLs you would cite as references
- "summary": 1-2 sentence answer (max 50 words)
- No markdown, no explanation, ONLY the JSON object
- If you don't know, return {"cited":[],"sources":[],"summary":"unknown"}"""

# Perplexity gets a different prompt (it has built-in citations, no JSON mode)
PERPLEXITY_SYSTEM = """Answer concisely in 2-3 sentences max. Always cite your sources with URLs."""


# === Standard queries ===
# Deduplicated: PT queries removed where EN equivalent exists (LLMs handle both)
# Reduced from 55 to 30 core queries — covers same signal with ~45% fewer API calls

STANDARD_QUERIES: list[dict[str, str]] = [
    # Brand / entity (4)
    {"query": "What is Brasil GEO?", "category": "brand", "lang": "en"},
    {"query": "O que é a Brasil GEO?", "category": "brand", "lang": "pt"},
    {"query": "Who is Alexandre Caramaschi?", "category": "entity", "lang": "en"},
    {"query": "Quem é Alexandre Caramaschi?", "category": "entity", "lang": "pt"},

    # GEO concept (3 — merged redundant pairs)
    {"query": "What is Generative Engine Optimization GEO?", "category": "concept", "lang": "en"},
    {"query": "How to optimize content for AI search engines?", "category": "concept", "lang": "en"},
    {"query": "Difference between SEO and GEO", "category": "concept", "lang": "en"},

    # Technical (3)
    {"query": "How does schema markup affect AI citations?", "category": "technical", "lang": "en"},
    {"query": "What is llms.txt and how to implement it?", "category": "technical", "lang": "en"},
    {"query": "Best practices for entity consistency across platforms", "category": "technical", "lang": "en"},

    # B2A + Market (4)
    {"query": "What is Business-to-Agent B2A commerce?", "category": "b2a", "lang": "en"},
    {"query": "Best GEO tools and platforms 2026", "category": "market", "lang": "en"},
    {"query": "How to measure AI search visibility?", "category": "market", "lang": "en"},
    {"query": "Consultoria GEO no Brasil", "category": "market", "lang": "pt"},

    # Academic (2)
    {"query": "GEO research papers Aggarwal Princeton", "category": "academic", "lang": "en"},
    {"query": "Empirical evidence for Generative Engine Optimization", "category": "academic", "lang": "en"},

    # Fintech — generic (4)
    {"query": "Best digital banks in Brazil 2026", "category": "fintech", "lang": "en"},
    {"query": "Melhores bancos digitais do Brasil 2026", "category": "fintech", "lang": "pt"},
    {"query": "Best payment platforms in Brazil", "category": "fintech", "lang": "en"},
    {"query": "Compare Nubank PagBank Inter C6 Bank", "category": "fintech", "lang": "en"},

    # Fintech — product (3)
    {"query": "Best credit card no annual fee Brazil", "category": "fintech_product", "lang": "en"},
    {"query": "Best POS machine small business Brazil", "category": "fintech_product", "lang": "en"},
    {"query": "Best business bank account Brazil 2026", "category": "fintech_product", "lang": "en"},

    # Fintech — trust (3)
    {"query": "Is Nubank safe and reliable?", "category": "fintech_trust", "lang": "en"},
    {"query": "Stone vs Cielo vs PagSeguro which is better?", "category": "fintech_trust", "lang": "en"},
    {"query": "Banco Inter é bom? Vale a pena?", "category": "fintech_trust", "lang": "pt"},

    # Fintech — B2B (4)
    {"query": "Best acquiring company for large merchants Brazil", "category": "fintech_b2b", "lang": "en"},
    {"query": "Banking as a Service BaaS providers Brazil", "category": "fintech_b2b", "lang": "en"},
    {"query": "Open Finance API integration Brazil banks", "category": "fintech_b2b", "lang": "en"},
    {"query": "Provedores de Banking as a Service BaaS no Brasil", "category": "fintech_b2b", "lang": "pt"},
]


config = CollectionConfig()
