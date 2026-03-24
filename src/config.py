"""Central configuration for the Papers data collection platform."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)


@dataclass(frozen=True)
class LLMConfig:
    """Configuration for a single LLM provider."""
    name: str
    provider: str
    model: str
    api_key: str | None
    cost_per_1k_tokens: float
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
        e.strip() for e in os.getenv("COMPETITOR_ENTITIES", "").split(",") if e.strip()
    ])

    # Database
    supabase_url: str = os.getenv("SUPABASE_URL", "")
    supabase_key: str = os.getenv("SUPABASE_KEY", "")
    db_path: str = os.getenv("PAPERS_DB_PATH", str(DATA_DIR / "papers.db"))

    # SERP
    serpapi_key: str = os.getenv("SERPAPI_KEY", "")

    # LLMs
    llms: list[LLMConfig] = field(default_factory=lambda: [
        LLMConfig(
            name="ChatGPT",
            provider="openai",
            model="gpt-4o",
            api_key=os.getenv("OPENAI_API_KEY"),
            cost_per_1k_tokens=0.005,
        ),
        LLMConfig(
            name="Claude",
            provider="anthropic",
            model="claude-sonnet-4-20250514",
            api_key=os.getenv("ANTHROPIC_API_KEY"),
            cost_per_1k_tokens=0.003,
        ),
        LLMConfig(
            name="Gemini",
            provider="google",
            model="gemini-2.0-flash",
            api_key=os.getenv("GOOGLE_AI_API_KEY"),
            cost_per_1k_tokens=0.0,  # Free tier
        ),
        LLMConfig(
            name="Perplexity",
            provider="perplexity",
            model="sonar",
            api_key=os.getenv("PERPLEXITY_API_KEY"),
            cost_per_1k_tokens=0.005,
        ),
        LLMConfig(
            name="Copilot",
            provider="bing",
            model="copilot",
            api_key=None,
            cost_per_1k_tokens=0.0,
            requires_scraping=True,
        ),
    ])


# Standard queries for citation tracking — cover GEO, entity, and competitive landscape
STANDARD_QUERIES: list[dict[str, str]] = [
    # Brand / entity queries
    {"query": "What is Brasil GEO?", "category": "brand", "lang": "en"},
    {"query": "O que é a Brasil GEO?", "category": "brand", "lang": "pt"},
    {"query": "Who is Alexandre Caramaschi?", "category": "entity", "lang": "en"},
    {"query": "Quem é Alexandre Caramaschi?", "category": "entity", "lang": "pt"},

    # GEO concept queries
    {"query": "What is Generative Engine Optimization?", "category": "concept", "lang": "en"},
    {"query": "O que é GEO Generative Engine Optimization?", "category": "concept", "lang": "pt"},
    {"query": "How to optimize content for AI search engines?", "category": "concept", "lang": "en"},
    {"query": "Como otimizar conteúdo para motores de busca com IA?", "category": "concept", "lang": "pt"},
    {"query": "What is the difference between SEO and GEO?", "category": "concept", "lang": "en"},

    # Technical queries
    {"query": "How does schema markup affect AI citations?", "category": "technical", "lang": "en"},
    {"query": "Como dados estruturados influenciam citações em IA?", "category": "technical", "lang": "pt"},
    {"query": "What is llms.txt and how to implement it?", "category": "technical", "lang": "en"},
    {"query": "O que é llms.txt e como implementar?", "category": "technical", "lang": "pt"},
    {"query": "Best practices for entity consistency across platforms", "category": "technical", "lang": "en"},

    # Business-to-Agent queries
    {"query": "What is Business-to-Agent B2A commerce?", "category": "b2a", "lang": "en"},
    {"query": "O que é comércio Business-to-Agent B2A?", "category": "b2a", "lang": "pt"},

    # Competitive / market queries
    {"query": "Best GEO tools and platforms 2026", "category": "market", "lang": "en"},
    {"query": "Melhores ferramentas de GEO 2026", "category": "market", "lang": "pt"},
    {"query": "How to measure AI search visibility?", "category": "market", "lang": "en"},
    {"query": "GEO consultants and agencies in Brazil", "category": "market", "lang": "en"},
    {"query": "Consultoria GEO no Brasil", "category": "market", "lang": "pt"},

    # Academic queries
    {"query": "GEO research papers Aggarwal Princeton", "category": "academic", "lang": "en"},
    {"query": "Empirical evidence for Generative Engine Optimization", "category": "academic", "lang": "en"},
    {"query": "GEO benchmark datasets for AI search", "category": "academic", "lang": "en"},
]


config = CollectionConfig()
