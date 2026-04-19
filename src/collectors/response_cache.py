"""SHA-256 keyed file cache for LLM responses.

Extraído de `src/collectors/base.py` em 2026-04-19 (Onda 7 — split de
responsabilidades). Mantém API idêntica para preservar backward-compat.

Função: evita re-consultar o mesmo (provider, model, query, vertical)
dentro de uma janela TTL. Reduz custos em ~50% das queries repetidas.
Estratégia complementar ao Batch API (que não foi implementado ainda).
"""

from __future__ import annotations

import hashlib
import json
import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path

from src.config import CACHE_DIR

logger = logging.getLogger(__name__)


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
        """Return cache stats: total files, valid (within TTL), expired."""
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
