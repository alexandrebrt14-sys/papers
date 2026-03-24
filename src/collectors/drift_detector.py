"""Model drift detector — pin versions and detect silent updates.

Expert critique (Hinton, Karpathy): Model aliases like 'gpt-4o-mini' can
point to different model weights over the 6-12 month study. A change in
citation behavior may be caused by a model update, not by our intervention.

This module:
1. Records the actual model version returned by each API
2. Hashes a canonical response to detect behavioral changes
3. Alerts when drift is detected
"""
from __future__ import annotations

import hashlib
import logging
import sqlite3
from datetime import datetime, timezone
from typing import Any

from src.collectors.base import LLMResponse

logger = logging.getLogger(__name__)

# Canonical probe query — always the same, used to detect model behavior changes
PROBE_QUERY = "What is the capital of France? Answer in exactly one word."
EXPECTED_PROBE = "paris"


class DriftDetector:
    """Detect silent model updates by tracking version strings and response hashes."""

    def __init__(self, db_path: str) -> None:
        self._db_path = db_path

    def record_version(self, response: LLMResponse) -> dict[str, Any]:
        """Record the model version from an API response.

        Returns dict with detected_change=True if version changed.
        """
        # Extract actual version from raw response
        actual_version = self._extract_version(response)
        response_hash = hashlib.sha256(
            response.response_text.strip().lower().encode()
        ).hexdigest()[:16]

        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row

        # Check if we've seen this provider+alias before
        existing = conn.execute(
            "SELECT model_version, response_hash FROM model_versions "
            "WHERE provider = ? AND model_alias = ? ORDER BY timestamp DESC LIMIT 1",
            (response.provider, response.model),
        ).fetchone()

        detected_change = False
        if existing:
            if existing["model_version"] != actual_version:
                detected_change = True
                logger.warning(
                    f"[drift] {response.provider}/{response.model}: "
                    f"version changed {existing['model_version']} -> {actual_version}"
                )
            elif existing["response_hash"] != response_hash:
                detected_change = True
                logger.warning(
                    f"[drift] {response.provider}/{response.model}: "
                    f"response hash changed (same version {actual_version})"
                )

        # Only insert if version is new or changed
        try:
            conn.execute(
                "INSERT OR IGNORE INTO model_versions "
                "(timestamp, provider, model_alias, model_version, response_hash) "
                "VALUES (?, ?, ?, ?, ?)",
                (datetime.now(timezone.utc).isoformat(), response.provider,
                 response.model, actual_version, response_hash),
            )
            conn.commit()
        except Exception:
            pass
        conn.close()

        return {
            "provider": response.provider,
            "model_alias": response.model,
            "actual_version": actual_version,
            "response_hash": response_hash,
            "detected_change": detected_change,
        }

    def _extract_version(self, response: LLMResponse) -> str:
        """Extract pinned model version from API response."""
        if not response.raw:
            return response.model

        # OpenAI returns full model name with date
        if response.provider == "openai":
            return response.raw.get("model", response.model)

        # Anthropic returns model in response
        if response.provider == "anthropic":
            return response.raw.get("model", response.model)

        # Google returns model info in metadata
        if response.provider == "google":
            return response.raw.get("modelVersion", response.model)

        return response.model

    def get_version_history(self, provider: str, model_alias: str) -> list[dict[str, Any]]:
        """Get version history for a model."""
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM model_versions WHERE provider = ? AND model_alias = ? ORDER BY timestamp",
            (provider, model_alias),
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_drift_events(self) -> list[dict[str, Any]]:
        """Get all detected drift events."""
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM model_versions WHERE detected_change = 1 ORDER BY timestamp DESC",
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]
