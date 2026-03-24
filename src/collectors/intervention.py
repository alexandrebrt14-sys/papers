"""Module 4: Content Intervention Tracker (A/B for content).

Framework for controlled experiments: register a content intervention (e.g., adding
Schema.org, llms.txt, academic citations), then measure citation rate changes at
7, 14, and 30 days post-intervention.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from typing import Any

from src.collectors.base import BaseCollector

logger = logging.getLogger(__name__)


class InterventionTracker(BaseCollector):
    """Track content interventions and their impact on AI citations."""

    def module_name(self) -> str:
        return "intervention_tracker"

    def collect(self) -> list[dict[str, Any]]:
        """Check active interventions and measure current citation state."""
        # This module works differently: it reads registered interventions
        # from the database and runs citation checks for each one.
        # The `register_intervention` method adds new interventions.
        self.logger.info("Intervention tracker runs via `check_interventions` — use CLI")
        return []

    @staticmethod
    def create_intervention(
        slug: str,
        intervention_type: str,
        description: str,
        url: str,
        queries: list[str],
        baseline_citations: dict[str, bool] | None = None,
    ) -> dict[str, Any]:
        """Create a new intervention record.

        Args:
            slug: Unique identifier for the intervention.
            intervention_type: One of: schema_org, llms_txt, academic_citations,
                structured_data, statistics_addition, quotation_addition, entity_fix.
            description: What was changed.
            url: URL of the modified content.
            queries: List of queries to monitor for this intervention.
            baseline_citations: Pre-intervention citation state per LLM.
        """
        valid_types = [
            "schema_org", "llms_txt", "academic_citations", "structured_data",
            "statistics_addition", "quotation_addition", "entity_fix", "combined",
        ]
        if intervention_type not in valid_types:
            raise ValueError(f"Invalid type '{intervention_type}'. Valid: {valid_types}")

        return {
            "module": "intervention_tracker",
            "slug": slug,
            "intervention_type": intervention_type,
            "description": description,
            "url": url,
            "queries": queries,
            "baseline_citations": baseline_citations or {},
            "registered_at": datetime.now(timezone.utc).isoformat(),
            "status": "active",
            "measurements": [],  # Will be populated by check_interventions
        }

    @staticmethod
    def create_measurement(
        intervention_slug: str,
        days_since: int,
        citations: dict[str, bool],
        details: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Create a measurement for an active intervention.

        Args:
            intervention_slug: Which intervention this measurement is for.
            days_since: Days since intervention was applied.
            citations: Citation state per LLM {llm_name: cited_bool}.
            details: Additional measurement details.
        """
        baseline_rate = 0.0  # Will be computed from stored baseline
        current_rate = sum(citations.values()) / max(len(citations), 1)

        return {
            "module": "intervention_tracker",
            "intervention_slug": intervention_slug,
            "days_since_intervention": days_since,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "citations_by_llm": citations,
            "citation_rate": round(current_rate, 3),
            "delta_from_baseline": None,  # Computed when baseline is known
            "details": details or {},
        }

    @staticmethod
    def check_active_interventions(db) -> list[dict[str, Any]]:
        """Check all active interventions and record measurements at day +7, +14, +30.

        Args:
            db: DatabaseClient instance (connected).

        Returns:
            List of measurement records created.
        """
        from src.collectors.base import LLMClient
        from src.config import config

        active = db.get_active_interventions()
        if not active:
            logger.info("Nenhuma intervenção ativa encontrada.")
            return []

        measurement_days = [7, 14, 30]
        results = []

        for intervention in active:
            slug = intervention["slug"]
            registered_at = datetime.fromisoformat(intervention["registered_at"].replace("Z", "+00:00"))
            days_elapsed = (datetime.now(timezone.utc) - registered_at).days

            queries = json.loads(intervention["queries_json"]) if intervention["queries_json"] else []
            baseline = json.loads(intervention["baseline_json"]) if intervention["baseline_json"] else {}

            # Compute baseline rate
            baseline_rate = sum(baseline.values()) / max(len(baseline), 1) if baseline else 0.0

            # Check existing measurements to avoid duplicates
            existing = db.get_intervention_measurements(slug)
            existing_days = {m["days_since_intervention"] for m in existing}

            for target_day in measurement_days:
                if days_elapsed < target_day:
                    continue
                if target_day in existing_days:
                    continue

                logger.info(f"Medindo intervenção '{slug}' no dia +{target_day}")

                # Query each LLM for each intervention query
                client = LLMClient()
                citations_by_llm: dict[str, bool] = {}

                for llm_cfg in config.llms:
                    if not llm_cfg.api_key or llm_cfg.requires_scraping:
                        continue
                    cited_any = False
                    for query in queries[:3]:  # Limit to 3 queries per LLM to save cost
                        resp = client.query(llm_cfg, query)
                        if resp and resp.cited_entities:
                            cited_any = True
                            break
                    citations_by_llm[llm_cfg.name] = cited_any

                client.close()

                current_rate = sum(citations_by_llm.values()) / max(len(citations_by_llm), 1)
                delta = current_rate - baseline_rate if baseline else None

                measurement = {
                    "intervention_slug": slug,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "days_since_intervention": target_day,
                    "citations_by_llm": citations_by_llm,
                    "citation_rate": round(current_rate, 3),
                    "delta_from_baseline": round(delta, 3) if delta is not None else None,
                    "details": {"days_elapsed_actual": days_elapsed},
                }

                db.insert_intervention_measurement(measurement)
                results.append(measurement)
                logger.info(
                    f"  Intervenção '{slug}' dia +{target_day}: "
                    f"taxa={current_rate:.1%}, delta={delta:+.1%}" if delta is not None else f"taxa={current_rate:.1%}"
                )

            # Mark completed if 30-day measurement is done
            if 30 in existing_days or days_elapsed >= 30:
                all_days_measured = all(d in existing_days or d in {m["days_since_intervention"] for m in results if m["intervention_slug"] == slug} for d in measurement_days)
                if all_days_measured:
                    db._conn.execute(
                        "UPDATE interventions SET status = 'completed' WHERE slug = ?", (slug,)
                    )
                    db._conn.commit()
                    logger.info(f"  Intervenção '{slug}' marcada como concluída.")

        return results
