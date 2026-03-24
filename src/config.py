"""Central configuration for the Papers data collection platform.

Optimized for cost-efficiency:
- Cheapest models per provider (nano/haiku/flash-lite)
- Batch API support (50% discount)
- Structured JSON output (minimal tokens)
- Local response cache (skip repeated queries)
- max_tokens caps (prevent runaway costs)

Multi-vertical support:
- fintech, varejo, saude, tecnologia
- Each vertical has its own cohort + queries
- Common queries (GEO concepts) shared across all verticals
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


# ============================================================
# Multi-Vertical Framework
# ============================================================

COMMON_QUERIES: list[dict[str, str]] = [
    # GEO concept (3)
    {"query": "What is Generative Engine Optimization GEO?", "category": "concept", "lang": "en"},
    {"query": "How to optimize content for AI search engines?", "category": "concept", "lang": "en"},
    {"query": "Difference between SEO and GEO", "category": "concept", "lang": "en"},

    # Technical (3)
    {"query": "How does schema markup affect AI citations?", "category": "technical", "lang": "en"},
    {"query": "What is llms.txt and how to implement it?", "category": "technical", "lang": "en"},
    {"query": "Best practices for entity consistency across platforms", "category": "technical", "lang": "en"},

    # Academic (2)
    {"query": "GEO research papers Aggarwal Princeton", "category": "academic", "lang": "en"},
    {"query": "Empirical evidence for Generative Engine Optimization", "category": "academic", "lang": "en"},
]

VERTICALS: dict[str, dict] = {
    "fintech": {
        "name": "Fintech & Bancos Digitais",
        "slug": "fintech",
        "cohort": [
            "Nubank", "PagBank", "Cielo", "Stone", "Banco Inter",
            "Mercado Pago", "Itaú", "Bradesco", "C6 Bank", "PicPay",
            "Ame Digital", "Neon", "Original", "BS2", "Safra",
            "Banco Carrefour",
        ],
        "queries": [
            # Brand awareness (2)
            {"query": "Best digital banks in Brazil 2026", "category": "fintech", "lang": "en"},
            {"query": "Melhores bancos digitais do Brasil 2026", "category": "fintech", "lang": "pt"},
            # Comparisons (2)
            {"query": "Compare Nubank PagBank Inter C6 Bank", "category": "fintech", "lang": "en"},
            {"query": "Stone vs Cielo vs PagSeguro which is better?", "category": "fintech_trust", "lang": "en"},
            # Trust (2)
            {"query": "Is Nubank safe and reliable?", "category": "fintech_trust", "lang": "en"},
            {"query": "Banco Inter é bom? Vale a pena?", "category": "fintech_trust", "lang": "pt"},
            # Product (3)
            {"query": "Best credit card no annual fee Brazil", "category": "fintech_product", "lang": "en"},
            {"query": "Best POS machine small business Brazil", "category": "fintech_product", "lang": "en"},
            {"query": "Best business bank account Brazil 2026", "category": "fintech_product", "lang": "en"},
            # B2B (3)
            {"query": "Best acquiring company for large merchants Brazil", "category": "fintech_b2b", "lang": "en"},
            {"query": "Banking as a Service BaaS providers Brazil", "category": "fintech_b2b", "lang": "en"},
            {"query": "Open Finance API integration Brazil banks", "category": "fintech_b2b", "lang": "en"},
        ],
    },
    "varejo": {
        "name": "Varejo & E-commerce",
        "slug": "varejo",
        "cohort": [
            "Magazine Luiza", "Casas Bahia", "Ponto Frio", "Americanas",
            "Amazon Brasil", "Mercado Livre", "Shopee Brasil", "AliExpress Brasil",
            "Leroy Merlin", "Tok&Stok", "Renner", "Riachuelo",
            "C&A Brasil", "Centauro", "Netshoes",
        ],
        "queries": [
            # Brand awareness (2)
            {"query": "Best online stores in Brazil 2026", "category": "varejo", "lang": "en"},
            {"query": "Melhores lojas online do Brasil 2026", "category": "varejo", "lang": "pt"},
            # Comparisons (2)
            {"query": "Compare Magazine Luiza and Americanas", "category": "varejo", "lang": "en"},
            {"query": "Mercado Livre vs Amazon Brasil vs Shopee", "category": "varejo", "lang": "en"},
            # Trust (2)
            {"query": "Is Shopee Brasil reliable?", "category": "varejo_trust", "lang": "en"},
            {"query": "Americanas é confiável para comprar online?", "category": "varejo_trust", "lang": "pt"},
            # Product (2)
            {"query": "Best marketplace for electronics Brazil", "category": "varejo_product", "lang": "en"},
            {"query": "Best furniture stores online Brazil 2026", "category": "varejo_product", "lang": "en"},
            # B2B (2)
            {"query": "Best marketplace platform for sellers Brazil", "category": "varejo_b2b", "lang": "en"},
            {"query": "Melhores plataformas de e-commerce para lojistas no Brasil", "category": "varejo_b2b", "lang": "pt"},
        ],
    },
    "saude": {
        "name": "Saúde & Farmacêuticas",
        "slug": "saude",
        "cohort": [
            "Dasa", "Hapvida", "Unimed", "Eli Lilly Brasil",
            "Raia Drogasil", "Fleury", "Rede D'Or", "Einstein",
            "Sírio-Libanês", "Eurofarma", "Aché", "EMS",
            "Hypera Pharma", "NotreDame Intermédica", "SulAmérica Saúde",
        ],
        "queries": [
            # Brand awareness (2)
            {"query": "Best hospitals in Brazil 2026", "category": "saude", "lang": "en"},
            {"query": "Melhores hospitais do Brasil 2026", "category": "saude", "lang": "pt"},
            # Comparisons (2)
            {"query": "Compare Dasa and Fleury labs", "category": "saude", "lang": "en"},
            {"query": "Rede D'Or vs Einstein vs Sírio-Libanês", "category": "saude", "lang": "en"},
            # Trust (2)
            {"query": "Best health insurance Brazil", "category": "saude_trust", "lang": "en"},
            {"query": "Unimed é bom? Vale a pena o plano de saúde?", "category": "saude_trust", "lang": "pt"},
            # Product (2)
            {"query": "Best pharmacy chains in Brazil", "category": "saude_product", "lang": "en"},
            {"query": "Best diagnostic labs Brazil 2026", "category": "saude_product", "lang": "en"},
            # B2B (2)
            {"query": "Best pharmaceutical companies Brazil", "category": "saude_b2b", "lang": "en"},
            {"query": "Melhores empresas de saúde para investir no Brasil", "category": "saude_b2b", "lang": "pt"},
        ],
    },
    "tecnologia": {
        "name": "Tecnologia & TI",
        "slug": "tecnologia",
        "cohort": [
            "Tivit", "Accenture Brasil", "Stefanini", "Totvs",
            "Linx", "Locaweb", "Positivo Tecnologia", "Movile",
            "CI&T", "Vivo Empresas", "Embraer", "WEG",
            "Natura &Co", "iFood", "99",
        ],
        "queries": [
            # Brand awareness (2)
            {"query": "Best IT companies in Brazil 2026", "category": "tecnologia", "lang": "en"},
            {"query": "Melhores empresas de tecnologia do Brasil 2026", "category": "tecnologia", "lang": "pt"},
            # Comparisons (2)
            {"query": "Compare Totvs and Linx ERP", "category": "tecnologia", "lang": "en"},
            {"query": "Tivit vs Stefanini vs Accenture Brasil outsourcing", "category": "tecnologia", "lang": "en"},
            # Trust (2)
            {"query": "Best outsourcing companies Brazil", "category": "tecnologia_trust", "lang": "en"},
            {"query": "Locaweb é boa para hospedagem?", "category": "tecnologia_trust", "lang": "pt"},
            # Product (2)
            {"query": "Best ERP systems for Brazilian companies", "category": "tecnologia_product", "lang": "en"},
            {"query": "Best cloud hosting providers Brazil 2026", "category": "tecnologia_product", "lang": "en"},
            # B2B (2)
            {"query": "Best IT consulting firms Brazil", "category": "tecnologia_b2b", "lang": "en"},
            {"query": "Melhores empresas de outsourcing de TI no Brasil", "category": "tecnologia_b2b", "lang": "pt"},
        ],
    },
}


def get_vertical(slug: str) -> dict:
    """Return vertical config by slug. Raises KeyError if not found."""
    if slug not in VERTICALS:
        raise KeyError(f"Vertical '{slug}' não encontrada. Opções: {list(VERTICALS.keys())}")
    return VERTICALS[slug]


def get_cohort(slug: str) -> list[str]:
    """Return cohort entities for a vertical."""
    return get_vertical(slug)["cohort"]


def get_queries(slug: str, include_common: bool = True) -> list[dict[str, str]]:
    """Return queries for a vertical, optionally including common queries."""
    vertical = get_vertical(slug)
    queries = list(vertical["queries"])
    if include_common:
        queries = COMMON_QUERIES + queries
    return queries


def list_verticals() -> list[str]:
    """Return list of all vertical slugs."""
    return list(VERTICALS.keys())


# ============================================================
# LLM Configuration
# ============================================================

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

    # Vertical selection (default: fintech for backward compatibility)
    vertical: str = os.getenv("VERTICAL", "fintech")

    # Study cohort — resolved from VERTICALS dict
    # COHORT_ENTITIES env var overrides fintech cohort for backward compat
    cohort_entities: list[str] = field(default_factory=lambda: [
        e.strip() for e in os.getenv(
            "COHORT_ENTITIES",
            ",".join(VERTICALS["fintech"]["cohort"]),
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
            model="gemini-2.5-flash",      # Free tier: 15 RPM — 2.0-flash has limit:0 as of 2026-03-24
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


# === Standard queries (legacy — kept for backward compat, now derived from VERTICALS) ===
# Use get_queries("fintech") for vertical-aware query lists

STANDARD_QUERIES: list[dict[str, str]] = get_queries("fintech", include_common=True)


config = CollectionConfig()
