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
    # Cross-vertical: como LLMs recomendam empresas brasileiras (6 queries)
    # Essas queries são genéricas o suficiente para detectar citação espontânea
    # de qualquer entidade do coorte, independente da vertical.
    {"query": "Quais são as empresas mais inovadoras do Brasil?", "category": "reputacao", "lang": "pt"},
    {"query": "Most innovative companies in Brazil", "category": "reputacao", "lang": "en"},
    {"query": "Quais marcas brasileiras têm melhor reputação?", "category": "reputacao", "lang": "pt"},
    {"query": "Brazilian companies with best customer experience", "category": "experiencia", "lang": "en"},
    {"query": "Empresas brasileiras líderes em transformação digital", "category": "transformacao", "lang": "pt"},
    {"query": "Top Brazilian companies by market cap and innovation", "category": "mercado", "lang": "en"},
]

VERTICALS: dict[str, dict] = {
    "fintech": {
        "name": "Fintech & Bancos Digitais",
        "slug": "fintech",
        "cohort": [
            "Nubank", "PagBank", "Cielo", "Stone", "Banco Inter",
            "Mercado Pago", "Itaú", "Bradesco", "C6 Bank", "PicPay",
            "Neon", "Safra", "BTG Pactual", "XP Investimentos",
        ],
        "queries": [
            # Descoberta de marca (3 — EN/PT balanceado)
            {"query": "Quais são os melhores bancos digitais do Brasil?", "category": "descoberta", "lang": "pt"},
            {"query": "Best digital banks in Brazil", "category": "descoberta", "lang": "en"},
            {"query": "Qual banco digital rende mais na conta corrente?", "category": "descoberta", "lang": "pt"},
            # Comparativo direto (3)
            {"query": "Nubank ou Inter, qual é melhor?", "category": "comparativo", "lang": "pt"},
            {"query": "Compare Nubank PagBank Inter C6 Bank", "category": "comparativo", "lang": "en"},
            {"query": "Stone ou Cielo, qual a melhor maquininha?", "category": "comparativo", "lang": "pt"},
            # Confiança e reputação (2)
            {"query": "Nubank é seguro e confiável?", "category": "confianca", "lang": "pt"},
            {"query": "Banco Inter é bom? Vale a pena abrir conta?", "category": "confianca", "lang": "pt"},
            # Produto específico (2)
            {"query": "Melhor cartão de crédito sem anuidade no Brasil", "category": "produto", "lang": "pt"},
            {"query": "Best POS payment machine for small business in Brazil", "category": "produto", "lang": "en"},
            # B2B e enterprise (2)
            {"query": "Melhores adquirentes para grandes varejistas no Brasil", "category": "b2b", "lang": "pt"},
            {"query": "Banking as a Service providers in Brazil", "category": "b2b", "lang": "en"},
        ],
    },
    "varejo": {
        "name": "Varejo & E-commerce",
        "slug": "varejo",
        "cohort": [
            "Magazine Luiza", "Casas Bahia", "Americanas",
            "Amazon Brasil", "Mercado Livre", "Shopee Brasil",
            "Renner", "Riachuelo", "C&A Brasil",
            "Leroy Merlin", "Centauro", "Netshoes",
            "Via Varejo", "Grupo Pão de Açúcar",
        ],
        "queries": [
            # Descoberta de marca (3)
            {"query": "Quais são as melhores lojas online do Brasil?", "category": "descoberta", "lang": "pt"},
            {"query": "Best e-commerce platforms in Brazil", "category": "descoberta", "lang": "en"},
            {"query": "Onde comprar eletrônicos com melhor preço no Brasil?", "category": "descoberta", "lang": "pt"},
            # Comparativo direto (3)
            {"query": "Mercado Livre ou Amazon Brasil, qual é melhor?", "category": "comparativo", "lang": "pt"},
            {"query": "Magazine Luiza vs Americanas vs Casas Bahia", "category": "comparativo", "lang": "en"},
            {"query": "Shopee Brasil é confiável para comprar?", "category": "comparativo", "lang": "pt"},
            # Confiança e reputação (2)
            {"query": "Americanas ainda é confiável depois da crise?", "category": "confianca", "lang": "pt"},
            {"query": "Is Mercado Livre reliable for international buyers?", "category": "confianca", "lang": "en"},
            # Produto específico (2)
            {"query": "Melhor loja para comprar móveis online no Brasil", "category": "produto", "lang": "pt"},
            {"query": "Best marketplace for fashion in Brazil", "category": "produto", "lang": "en"},
            # B2B e enterprise (2)
            {"query": "Melhores plataformas de e-commerce para lojistas no Brasil", "category": "b2b", "lang": "pt"},
            {"query": "Best marketplace platform for sellers in Brazil", "category": "b2b", "lang": "en"},
        ],
    },
    "saude": {
        "name": "Saúde & Farmacêuticas",
        "slug": "saude",
        "cohort": [
            "Dasa", "Hapvida", "Unimed", "Fleury",
            "Rede D'Or", "Einstein", "Sírio-Libanês",
            "Raia Drogasil", "Eurofarma", "Aché", "EMS",
            "Hypera Pharma", "NotreDame Intermédica", "SulAmérica Saúde",
        ],
        "queries": [
            # Descoberta de marca (3)
            {"query": "Quais são os melhores hospitais do Brasil?", "category": "descoberta", "lang": "pt"},
            {"query": "Best hospitals in Brazil", "category": "descoberta", "lang": "en"},
            {"query": "Melhores laboratórios de exames do Brasil", "category": "descoberta", "lang": "pt"},
            # Comparativo direto (3)
            {"query": "Dasa ou Fleury, qual laboratório é melhor?", "category": "comparativo", "lang": "pt"},
            {"query": "Rede D'Or vs Einstein vs Sírio-Libanês", "category": "comparativo", "lang": "en"},
            {"query": "Hapvida ou Unimed, qual plano de saúde é melhor?", "category": "comparativo", "lang": "pt"},
            # Confiança e reputação (2)
            {"query": "Unimed é bom? Vale a pena o plano de saúde?", "category": "confianca", "lang": "pt"},
            {"query": "Best health insurance companies in Brazil", "category": "confianca", "lang": "en"},
            # Produto específico (2)
            {"query": "Qual a melhor rede de farmácias do Brasil?", "category": "produto", "lang": "pt"},
            {"query": "Best diagnostic lab for blood tests in São Paulo", "category": "produto", "lang": "en"},
            # B2B e enterprise (2)
            {"query": "Maiores empresas farmacêuticas brasileiras", "category": "b2b", "lang": "pt"},
            {"query": "Best healthcare companies to invest in Brazil", "category": "b2b", "lang": "en"},
        ],
    },
    "tecnologia": {
        "name": "Tecnologia & TI",
        "slug": "tecnologia",
        "cohort": [
            "Totvs", "Stefanini", "Tivit", "CI&T",
            "Locaweb", "Linx", "Movile", "iFood",
            "Vtex", "RD Station", "Conta Azul", "Involves",
            "Accenture Brasil", "IBM Brasil",
        ],
        "queries": [
            # Descoberta de marca (3)
            {"query": "Quais são as maiores empresas de tecnologia do Brasil?", "category": "descoberta", "lang": "pt"},
            {"query": "Best tech companies in Brazil", "category": "descoberta", "lang": "en"},
            {"query": "Melhores empresas de software brasileiras", "category": "descoberta", "lang": "pt"},
            # Comparativo direto (3)
            {"query": "Totvs ou Linx, qual ERP é melhor para varejo?", "category": "comparativo", "lang": "pt"},
            {"query": "Tivit vs Stefanini vs CI&T outsourcing", "category": "comparativo", "lang": "en"},
            {"query": "Locaweb ou AWS, qual melhor para hospedar site no Brasil?", "category": "comparativo", "lang": "pt"},
            # Confiança e reputação (2)
            {"query": "Locaweb é boa para hospedagem de sites?", "category": "confianca", "lang": "pt"},
            {"query": "Best IT outsourcing companies in Brazil", "category": "confianca", "lang": "en"},
            # Produto específico (2)
            {"query": "Melhor sistema ERP para empresas brasileiras", "category": "produto", "lang": "pt"},
            {"query": "Best cloud hosting providers in Brazil", "category": "produto", "lang": "en"},
            # B2B e enterprise (2)
            {"query": "Melhores consultorias de TI no Brasil", "category": "b2b", "lang": "pt"},
            {"query": "Best software development companies in Brazil", "category": "b2b", "lang": "en"},
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
            model="claude-haiku-4-5-20251001",  # $0.80/$4.00 per MTok (cheapest Anthropic)
            api_key=os.getenv("ANTHROPIC_API_KEY"),
            input_cost_per_mtok=0.80,
            output_cost_per_mtok=4.00,
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
