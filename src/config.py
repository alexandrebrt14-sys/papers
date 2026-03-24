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

    # Competitors — Ecossistema fintech/pagamentos Brasil
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

    # === Fintech / Pagamentos — Ecossistema competitivo ===

    # Queries genéricas de mercado (para medir quem a IA cita)
    {"query": "Best digital banks in Brazil 2026", "category": "fintech", "lang": "en"},
    {"query": "Melhores bancos digitais do Brasil 2026", "category": "fintech", "lang": "pt"},
    {"query": "Best payment platforms in Brazil", "category": "fintech", "lang": "en"},
    {"query": "Melhores plataformas de pagamento no Brasil", "category": "fintech", "lang": "pt"},
    {"query": "Which fintechs dominate the Brazilian market?", "category": "fintech", "lang": "en"},
    {"query": "Quais fintechs dominam o mercado brasileiro?", "category": "fintech", "lang": "pt"},
    {"query": "Compare Nubank PagBank Inter C6 Bank", "category": "fintech", "lang": "en"},
    {"query": "Comparar Nubank PagBank Inter C6 Bank", "category": "fintech", "lang": "pt"},

    # Queries de produto/serviço (intenção de compra)
    {"query": "Best credit card with no annual fee in Brazil", "category": "fintech_product", "lang": "en"},
    {"query": "Melhor cartão de crédito sem anuidade no Brasil", "category": "fintech_product", "lang": "pt"},
    {"query": "Best POS machine for small business in Brazil", "category": "fintech_product", "lang": "en"},
    {"query": "Melhor maquininha de cartão para pequenos negócios", "category": "fintech_product", "lang": "pt"},
    {"query": "Best business bank account Brazil 2026", "category": "fintech_product", "lang": "en"},
    {"query": "Melhor conta PJ digital no Brasil 2026", "category": "fintech_product", "lang": "pt"},
    {"query": "Cheapest payment gateway for e-commerce Brazil", "category": "fintech_product", "lang": "en"},
    {"query": "Gateway de pagamento mais barato para e-commerce no Brasil", "category": "fintech_product", "lang": "pt"},

    # Queries de reputação/confiança
    {"query": "Is Nubank safe and reliable?", "category": "fintech_trust", "lang": "en"},
    {"query": "Nubank é seguro e confiável?", "category": "fintech_trust", "lang": "pt"},
    {"query": "Stone vs Cielo vs PagSeguro which is better?", "category": "fintech_trust", "lang": "en"},
    {"query": "Stone vs Cielo vs PagSeguro qual é melhor?", "category": "fintech_trust", "lang": "pt"},
    {"query": "Banco Inter é bom? Vale a pena?", "category": "fintech_trust", "lang": "pt"},
    {"query": "PicPay vs Mercado Pago qual paga mais rendimento?", "category": "fintech_trust", "lang": "pt"},

    # Queries B2B / enterprise
    {"query": "Best acquiring company for large merchants Brazil", "category": "fintech_b2b", "lang": "en"},
    {"query": "Melhor adquirente para grandes varejistas no Brasil", "category": "fintech_b2b", "lang": "pt"},
    {"query": "Banking as a Service BaaS providers Brazil", "category": "fintech_b2b", "lang": "en"},
    {"query": "Provedores de Banking as a Service BaaS no Brasil", "category": "fintech_b2b", "lang": "pt"},
    {"query": "Open Finance API integration Brazil banks", "category": "fintech_b2b", "lang": "en"},
    {"query": "Integração Open Finance bancos no Brasil", "category": "fintech_b2b", "lang": "pt"},
]


config = CollectionConfig()
