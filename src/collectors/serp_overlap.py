"""Module 3: SERP vs AI Overlap Tracker (cost-optimized).

Cost comparison:
- OLD: SerpAPI $50/mo for Google SERP data
- NEW: Brave Search API $0/mo (free: 2,000 queries/month)

Measures divergence between traditional search results and AI-generated responses.
"""

from __future__ import annotations

from typing import Any

from src.collectors.base import BaseCollector, BraveSearchClient


class SerpAIOverlap(BaseCollector):
    """Track overlap between SERP and AI responses."""

    def module_name(self) -> str:
        return "serp_ai_overlap"

    def collect(self) -> list[dict[str, Any]]:
        """Rodar o overlap SERP vs IA.

        Toggle de ativação (Onda 9 — 2026-04-19):
        - `ENABLE_SERP_OVERLAP=true` em env: roda normalmente
        - `ENABLE_SERP_OVERLAP` ausente/falsy: pula silently retornando []
          (protege quota mensal do Brave; SERP só roda quando explicitamente ligado)
        - Adicionalmente, sem `BRAVE_API_KEY`, o BraveSearchClient já
          retorna [] internamente e o loop encerra sem INSERTs.
        """
        import os
        enabled = os.getenv("ENABLE_SERP_OVERLAP", "false").lower() == "true"
        if not enabled:
            self.logger.info(
                "[serp_ai_overlap] ENABLE_SERP_OVERLAP=false — módulo desligado por toggle. "
                "Para ativar, exporte ENABLE_SERP_OVERLAP=true."
            )
            return []

        results: list[dict[str, Any]] = []
        brave = BraveSearchClient()
        if not getattr(brave, "_key", ""):
            self.logger.warning(
                "[serp_ai_overlap] BRAVE_API_KEY ausente — impossível coletar SERP. "
                "Cadastre o secret BRAVE_API_KEY e reative."
            )
            return []

        # Use EN queries for SERP
        serp_queries = [q for q in self.queries if q["lang"] == "en"]

        for q in serp_queries:
            serp_results = brave.search(q["query"], count=10)
            if not serp_results:
                continue
            serp_domains = {r["domain"] for r in serp_results if r["domain"]}

            for llm_cfg in self.config.llms:
                response = self.llm_client.query(llm_cfg, q["query"])
                if response is None:
                    continue

                ai_domains = set()
                for url in response.sources:
                    parts = url.split("/")
                    if len(parts) >= 3:
                        d = parts[2].lower()
                        if d.startswith("www."):
                            d = d[4:]
                        ai_domains.add(d)

                overlap = serp_domains & ai_domains
                union = serp_domains | ai_domains
                overlap_pct = len(overlap) / max(len(union), 1) * 100

                results.append({
                    "module": self.module_name(),
                    "llm": llm_cfg.name,
                    "model": response.model,
                    "query": q["query"],
                    "query_category": q["category"],
                    "timestamp": response.timestamp,
                    "serp_domain_count": len(serp_domains),
                    "ai_domain_count": len(ai_domains),
                    "overlap_count": len(overlap),
                    "overlap_pct": round(overlap_pct, 1),
                    "serp_only_count": len(serp_domains - ai_domains),
                    "ai_only_count": len(ai_domains - serp_domains),
                    "overlap_domains": sorted(overlap),
                    "serp_only_domains": sorted(serp_domains - ai_domains),
                    "ai_only_domains": sorted(ai_domains - serp_domains),
                })

        brave.close()
        self.logger.info(f"Coletados {len(results)} registros de overlap SERP-IA")
        return results
