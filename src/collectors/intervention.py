"""Module 4: Content Intervention Tracker (A/B for content).

Framework for controlled experiments: register a content intervention (e.g., adding
Schema.org, llms.txt, academic citations), then measure citation rate changes at
7, 14, and 30 days post-intervention.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from src.collectors.base import BaseCollector


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
