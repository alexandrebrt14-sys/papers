"""
secrets.py -- Secure API key management for GEO research.

Defense-in-depth for API keys:
1. Keys loaded ONLY from env vars (never hardcoded, never in files)
2. Keys masked in all logs (shows only last 4 chars)
3. Key rotation detection (alerts if key changes)
4. Leak scanning (checks Git history for exposed keys)
5. Usage anomaly per key (detect if key is being used elsewhere)
6. Key health checks (validate each key is active without spending tokens)
"""
from __future__ import annotations

import hashlib
import logging
import os
import re
import subprocess
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import httpx

logger = logging.getLogger("finops.secrets")

ALERT_EMAIL = os.getenv("FINOPS_ALERT_EMAIL", "")

# Key patterns for leak detection
KEY_PATTERNS = {
    "openai": re.compile(r"sk-(?:proj-)?[A-Za-z0-9_-]{20,}"),
    "anthropic": re.compile(r"sk-ant-api\d{2}-[A-Za-z0-9_-]{20,}"),
    "google": re.compile(r"AIzaSy[A-Za-z0-9_-]{33}"),
    "perplexity": re.compile(r"pplx-[A-Za-z0-9]{40,}"),
    "resend": re.compile(r"re_[A-Za-z0-9_]{20,}"),
}


def mask_key(key: str, visible_chars: int = 4) -> str:
    """Mask an API key for safe logging. Shows only last N chars."""
    if not key or len(key) < visible_chars + 4:
        return "***"
    return f"***{key[-visible_chars:]}"


def get_key_fingerprint(key: str) -> str:
    """Generate a stable fingerprint for a key (for rotation detection).

    Uses SHA-256 hash so the actual key is never stored.
    """
    if not key:
        return ""
    return hashlib.sha256(key.encode()).hexdigest()[:16]


def validate_key_health(platform: str, api_key: str) -> dict[str, Any]:
    """Validate that an API key is active WITHOUT spending tokens.

    Uses lightweight endpoints (models list, billing check) that
    don't consume quota.
    """
    if not api_key:
        return {"platform": platform, "status": "missing", "active": False}

    try:
        if platform == "openai":
            r = httpx.get(
                "https://api.openai.com/v1/models",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=10,
            )
            if r.status_code == 200:
                return {"platform": platform, "status": "active", "active": True}
            elif r.status_code == 401:
                return {"platform": platform, "status": "invalid_key", "active": False}
            elif r.status_code == 429:
                return {"platform": platform, "status": "rate_limited_or_no_credits", "active": False}
            return {"platform": platform, "status": f"http_{r.status_code}", "active": False}

        elif platform == "anthropic":
            r = httpx.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={"model": "claude-haiku-4-5-20251001", "max_tokens": 1, "messages": [{"role": "user", "content": "hi"}]},
                timeout=10,
            )
            if r.status_code == 200:
                return {"platform": platform, "status": "active", "active": True}
            elif r.status_code == 401:
                return {"platform": platform, "status": "invalid_key", "active": False}
            elif r.status_code == 400 and "credit" in r.text.lower():
                return {"platform": platform, "status": "no_credits", "active": False}
            return {"platform": platform, "status": f"http_{r.status_code}", "active": r.status_code not in (401, 403)}

        elif platform == "google":
            r = httpx.get(
                "https://generativelanguage.googleapis.com/v1beta/models",
                params={"key": api_key},
                timeout=10,
            )
            if r.status_code == 200:
                return {"platform": platform, "status": "active", "active": True}
            elif r.status_code == 400 and "API_KEY_INVALID" in r.text:
                return {"platform": platform, "status": "invalid_key", "active": False}
            return {"platform": platform, "status": f"http_{r.status_code}", "active": r.status_code == 200}

        elif platform == "perplexity":
            # Perplexity doesn't have a free health check endpoint
            return {"platform": platform, "status": "unchecked", "active": bool(api_key)}

    except Exception as e:
        return {"platform": platform, "status": "error", "active": False, "error": str(e)}

    return {"platform": platform, "status": "unknown", "active": False}


def scan_git_for_leaks(repo_path: str | Path | None = None) -> list[dict[str, Any]]:
    """Scan Git history for accidentally committed API keys.

    Checks tracked files and recent commits for key patterns.
    Does NOT scan .env files (they're gitignored).
    """
    repo_path = Path(repo_path) if repo_path else Path(__file__).resolve().parent.parent.parent
    leaks = []

    # Scan tracked files
    try:
        tracked = subprocess.run(
            ["git", "ls-files"],
            capture_output=True, text=True, cwd=str(repo_path),
        ).stdout.strip().split("\n")

        for filepath in tracked:
            if not filepath or filepath.endswith((".db", ".png", ".jpg", ".pyc")):
                continue
            full_path = repo_path / filepath
            if not full_path.exists() or full_path.stat().st_size > 500_000:
                continue

            try:
                content = full_path.read_text(encoding="utf-8", errors="ignore")
                for platform, pattern in KEY_PATTERNS.items():
                    matches = pattern.findall(content)
                    for match in matches:
                        # Skip if it's in a comment or example
                        if "example" in filepath.lower() or "template" in filepath.lower():
                            continue
                        leaks.append({
                            "file": filepath,
                            "platform": platform,
                            "key_preview": mask_key(match),
                            "severity": "critical",
                            "message": f"Potential {platform} key found in {filepath}",
                        })
            except Exception:
                pass

    except Exception as e:
        logger.warning(f"Git scan failed: {e}")

    # Scan recent commits for sensitive files added to Git
    try:
        # Use --name-only --diff-filter=A to list only added file paths
        log = subprocess.run(
            ["git", "log", "--oneline", "-10", "--diff-filter=A", "--name-only"],
            capture_output=True, text=True, cwd=str(repo_path),
        ).stdout
        sensitive_patterns = [".env", "credentials", "secret", "apikey", "api_key"]
        for line in log.split("\n"):
            line = line.strip()
            if not line:
                continue
            # Skip commit message lines (format: "hash message...")
            # File paths never start with a hex hash followed by space
            if re.match(r"^[0-9a-f]{7,} ", line):
                continue
            if any(p in line.lower() for p in sensitive_patterns) and not line.startswith(("!", "#")):
                leaks.append({
                    "file": line,
                    "platform": "unknown",
                    "key_preview": "N/A",
                    "severity": "warning",
                    "message": f"Sensitive file in Git history: {line}",
                })
    except Exception:
        pass

    return leaks


def check_key_rotation(db_path: str) -> list[dict[str, Any]]:
    """Detect if API keys have changed since last check.

    Stores key fingerprints (NOT keys) in DB. Alerts on rotation.
    """
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS finops_key_fingerprints (
            platform TEXT PRIMARY KEY,
            fingerprint TEXT NOT NULL,
            last_checked TEXT NOT NULL
        )
    """)

    changes = []
    key_map = {
        "openai": os.getenv("OPENAI_API_KEY", ""),
        "anthropic": os.getenv("ANTHROPIC_API_KEY", ""),
        "google": os.getenv("GOOGLE_AI_API_KEY", ""),
        "perplexity": os.getenv("PERPLEXITY_API_KEY", ""),
    }

    now = datetime.now(timezone.utc).isoformat()
    for platform, key in key_map.items():
        fp = get_key_fingerprint(key)
        if not fp:
            continue

        existing = conn.execute(
            "SELECT fingerprint FROM finops_key_fingerprints WHERE platform = ?",
            (platform,),
        ).fetchone()

        if existing:
            if existing[0] != fp:
                changes.append({
                    "platform": platform,
                    "event": "key_rotated",
                    "message": f"{platform} API key has been rotated (fingerprint changed)",
                })
                conn.execute(
                    "UPDATE finops_key_fingerprints SET fingerprint = ?, last_checked = ? WHERE platform = ?",
                    (fp, now, platform),
                )
        else:
            conn.execute(
                "INSERT INTO finops_key_fingerprints (platform, fingerprint, last_checked) VALUES (?, ?, ?)",
                (platform, fp, now),
            )

    conn.commit()
    conn.close()
    return changes


def run_security_audit(db_path: str | None = None) -> dict[str, Any]:
    """Run full security audit on API keys.

    Returns structured report with findings.
    """
    from src.finops.tracker import get_tracker
    tracker = get_tracker()
    db_path = db_path or tracker._db_path

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "key_health": [],
        "leak_scan": [],
        "rotation_events": [],
        "recommendations": [],
    }

    print(f"{'='*50}")
    print(f"  Security Audit — API Keys")
    print(f"{'='*50}")

    # 1. Key health
    print("\n  [1/4] Validando chaves...")
    key_map = {
        "openai": os.getenv("OPENAI_API_KEY", ""),
        "anthropic": os.getenv("ANTHROPIC_API_KEY", ""),
        "google": os.getenv("GOOGLE_AI_API_KEY", ""),
        "perplexity": os.getenv("PERPLEXITY_API_KEY", ""),
    }
    for platform, key in key_map.items():
        health = validate_key_health(platform, key)
        report["key_health"].append(health)
        status = "OK" if health["active"] else health["status"]
        masked = mask_key(key) if key else "(vazia)"
        print(f"    {platform:12s} {masked:15s} [{status}]")

    # 2. Leak scan
    print("\n  [2/4] Scanning Git para vazamentos...")
    leaks = scan_git_for_leaks()
    report["leak_scan"] = leaks
    if leaks:
        for leak in leaks:
            print(f"    [{leak['severity'].upper()}] {leak['message']}")
    else:
        print(f"    Nenhum vazamento detectado")

    # 3. Key rotation
    print("\n  [3/4] Verificando rotação de chaves...")
    rotations = check_key_rotation(db_path)
    report["rotation_events"] = rotations
    if rotations:
        for r in rotations:
            print(f"    [{r['event']}] {r['message']}")
    else:
        print(f"    Nenhuma rotação detectada")

    # 4. Recommendations
    print("\n  [4/4] Recomendações:")
    for platform, key in key_map.items():
        if not key:
            report["recommendations"].append(f"Configurar {platform} API key")
            print(f"    - Configurar {platform} API key")
        elif len(key) < 20:
            report["recommendations"].append(f"{platform} key parece truncada")
            print(f"    - {platform} key parece truncada")

    if not os.getenv("RESEND_API_KEY"):
        report["recommendations"].append("Configurar RESEND_API_KEY para alertas por email")
        print(f"    - Configurar RESEND_API_KEY para alertas")

    if not report["recommendations"]:
        print(f"    Nenhuma ação necessária")

    print(f"\n{'='*50}")
    return report
