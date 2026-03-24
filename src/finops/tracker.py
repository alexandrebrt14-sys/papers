"""
tracker.py -- FinOps cost tracker for Papers
Tracks token usage and costs per LLM platform.
Enforces budgets and triggers alerts.
"""
import os
import json
import sqlite3
import requests
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

ALERT_EMAIL = "caramaschiai@caramaschiai.io"

# Pricing per 1M tokens (USD) — updated Mar 2026
PRICING = {
    "openai": {
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        "gpt-4o": {"input": 2.50, "output": 10.00},
        "default": {"input": 0.15, "output": 0.60},
    },
    "anthropic": {
        "claude-haiku-4-5-20251001": {"input": 0.80, "output": 4.00},
        "claude-sonnet-4-20250514": {"input": 3.00, "output": 15.00},
        "default": {"input": 0.80, "output": 4.00},
    },
    "google": {
        "gemini-2.0-flash": {"input": 0.10, "output": 0.40},
        "default": {"input": 0.10, "output": 0.40},
    },
    "perplexity": {
        "default": {"input": 0.20, "output": 0.20},
    },
}

DEFAULT_BUDGETS = {
    "openai": {"monthly": 10.0, "daily": 1.0, "alert_pct": 0.70, "hard_stop_pct": 0.95},
    "anthropic": {"monthly": 10.0, "daily": 1.0, "alert_pct": 0.70, "hard_stop_pct": 0.95},
    "google": {"monthly": 5.0, "daily": 0.5, "alert_pct": 0.80, "hard_stop_pct": 1.0},
    "perplexity": {"monthly": 10.0, "daily": 1.0, "alert_pct": 0.70, "hard_stop_pct": 0.95},
    "global": {"monthly": 30.0, "daily": 3.0, "alert_pct": 0.70, "hard_stop_pct": 0.95},
}


@dataclass
class UsageRecord:
    """Single API usage record."""
    platform: str
    model: str
    operation: str
    input_tokens: int
    output_tokens: int
    cost_usd: float
    query: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class FinOpsTracker:
    """Tracks costs, enforces budgets, triggers alerts."""

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or os.environ.get(
            "PAPERS_DB_PATH",
            str(Path(__file__).parent.parent.parent / "data" / "papers.db")
        )
        self._ensure_tables()
        self._ensure_budgets()

    def _get_conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA journal_mode=WAL")
        return conn

    def _ensure_tables(self):
        conn = self._get_conn()
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS finops_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                platform TEXT NOT NULL,
                model TEXT NOT NULL,
                operation TEXT NOT NULL,
                input_tokens INTEGER DEFAULT 0,
                output_tokens INTEGER DEFAULT 0,
                total_tokens INTEGER DEFAULT 0,
                cost_usd REAL DEFAULT 0,
                query TEXT DEFAULT ''
            );
            CREATE INDEX IF NOT EXISTS idx_finops_usage_ts ON finops_usage(timestamp);
            CREATE INDEX IF NOT EXISTS idx_finops_usage_platform ON finops_usage(platform);

            CREATE TABLE IF NOT EXISTS finops_budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT UNIQUE NOT NULL,
                monthly_limit_usd REAL DEFAULT 10,
                daily_limit_usd REAL DEFAULT 1,
                alert_threshold_pct REAL DEFAULT 0.7,
                hard_stop_pct REAL DEFAULT 0.95,
                updated_at TEXT
            );

            CREATE TABLE IF NOT EXISTS finops_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                platform TEXT NOT NULL,
                alert_type TEXT NOT NULL,
                message TEXT,
                current_spend_usd REAL,
                limit_usd REAL,
                pct_used REAL,
                sent_email INTEGER DEFAULT 0,
                email_to TEXT
            );
            CREATE INDEX IF NOT EXISTS idx_finops_alerts_ts ON finops_alerts(timestamp);
        """)
        conn.commit()
        conn.close()

    def _ensure_budgets(self):
        conn = self._get_conn()
        for platform, budget in DEFAULT_BUDGETS.items():
            existing = conn.execute(
                "SELECT COUNT(*) FROM finops_budgets WHERE platform = ?", (platform,)
            ).fetchone()[0]
            if not existing:
                conn.execute(
                    "INSERT INTO finops_budgets (platform, monthly_limit_usd, daily_limit_usd, alert_threshold_pct, hard_stop_pct, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                    (platform, budget["monthly"], budget["daily"], budget["alert_pct"], budget["hard_stop_pct"], datetime.now(timezone.utc).isoformat())
                )
        conn.commit()
        conn.close()

    def calculate_cost(self, platform: str, model: str, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost in USD."""
        prices = PRICING.get(platform, {})
        model_prices = prices.get(model, prices.get("default", {"input": 0, "output": 0}))
        return round((input_tokens * model_prices["input"] + output_tokens * model_prices["output"]) / 1_000_000, 6)

    def record(self, platform: str, model: str, operation: str, input_tokens: int, output_tokens: int, query: str = "") -> float:
        """Record usage and return cost."""
        cost = self.calculate_cost(platform, model, input_tokens, output_tokens)
        conn = self._get_conn()
        conn.execute(
            "INSERT INTO finops_usage (timestamp, platform, model, operation, input_tokens, output_tokens, total_tokens, cost_usd, query) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (datetime.now(timezone.utc).isoformat(), platform, model, operation, input_tokens, output_tokens, input_tokens + output_tokens, cost, query[:200])
        )
        conn.commit()
        conn.close()
        self._check_budget(platform)
        return cost

    def get_spend(self, platform: Optional[str] = None, period: str = "month") -> dict:
        """Get current spend for platform and period."""
        now = datetime.now(timezone.utc)
        if period == "day":
            since = now.strftime("%Y-%m-%dT00:00:00")
        elif period == "week":
            since = (now - timedelta(days=7)).isoformat()
        else:
            since = now.strftime("%Y-%m-01T00:00:00")

        conn = self._get_conn()
        if platform and platform != "global":
            row = conn.execute(
                "SELECT COALESCE(SUM(cost_usd), 0), COALESCE(SUM(total_tokens), 0), COUNT(*) FROM finops_usage WHERE platform = ? AND timestamp >= ?",
                (platform, since)
            ).fetchone()
        else:
            row = conn.execute(
                "SELECT COALESCE(SUM(cost_usd), 0), COALESCE(SUM(total_tokens), 0), COUNT(*) FROM finops_usage WHERE timestamp >= ?",
                (since,)
            ).fetchone()
        conn.close()
        return {"cost_usd": round(row[0], 4), "tokens": row[1], "queries": row[2]}

    def can_spend(self, platform: str) -> bool:
        """Check if platform is within budget."""
        conn = self._get_conn()
        budget = conn.execute(
            "SELECT monthly_limit_usd, daily_limit_usd, hard_stop_pct FROM finops_budgets WHERE platform = ?",
            (platform,)
        ).fetchone()
        conn.close()
        if not budget:
            return True

        monthly = self.get_spend(platform, "month")
        daily = self.get_spend(platform, "day")

        if budget[1] > 0 and daily["cost_usd"] / budget[1] >= budget[2]:
            return False
        if budget[0] > 0 and monthly["cost_usd"] / budget[0] >= budget[2]:
            return False
        return True

    def _check_budget(self, platform: str):
        """Check budget and trigger alerts if needed."""
        conn = self._get_conn()
        budget = conn.execute(
            "SELECT monthly_limit_usd, daily_limit_usd, alert_threshold_pct, hard_stop_pct FROM finops_budgets WHERE platform = ?",
            (platform,)
        ).fetchone()
        if not budget:
            conn.close()
            return

        monthly = self.get_spend(platform, "month")
        if budget[0] > 0:
            pct = monthly["cost_usd"] / budget[0]
            if pct >= 1.0:
                self._alert(conn, platform, "budget_exceeded", monthly["cost_usd"], budget[0], pct)
            elif pct >= 0.90:
                self._alert(conn, platform, "budget_critical", monthly["cost_usd"], budget[0], pct)
            elif pct >= budget[2]:
                self._alert(conn, platform, "budget_warning", monthly["cost_usd"], budget[0], pct)
        conn.close()

    def _alert(self, conn, platform: str, alert_type: str, current: float, limit: float, pct: float):
        """Record and send alert."""
        six_hours_ago = (datetime.now(timezone.utc) - timedelta(hours=6)).isoformat()
        recent = conn.execute(
            "SELECT COUNT(*) FROM finops_alerts WHERE platform = ? AND alert_type = ? AND timestamp >= ?",
            (platform, alert_type, six_hours_ago)
        ).fetchone()[0]
        if recent > 0:
            return

        msg = f"{platform}: ${current:.4f} / ${limit:.2f} ({pct*100:.0f}%)"
        sent = self._send_email(alert_type, msg, platform, current, limit, pct)
        conn.execute(
            "INSERT INTO finops_alerts (timestamp, platform, alert_type, message, current_spend_usd, limit_usd, pct_used, sent_email, email_to) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (datetime.now(timezone.utc).isoformat(), platform, alert_type, msg, current, limit, round(pct * 100, 1), int(sent), ALERT_EMAIL)
        )
        conn.commit()

    def _send_email(self, alert_type: str, message: str, platform: str, current: float, limit: float, pct: float) -> bool:
        """Send alert email via Resend."""
        api_key = os.environ.get("RESEND_API_KEY", "")
        if not api_key:
            return False
        try:
            r = requests.post(
                "https://api.resend.com/emails",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json={
                    "from": "GEO FinOps <onboarding@resend.dev>",
                    "to": [ALERT_EMAIL],
                    "subject": f"[GEO FinOps] {alert_type.upper()}: {platform} — {pct*100:.0f}%",
                    "html": f"<h2>{alert_type}: {platform}</h2><p>{message}</p><p>Ajustar: <code>python -m src.cli finops set-budget {platform} --monthly X</code></p>",
                },
                timeout=10,
            )
            return r.status_code == 200
        except Exception:
            return False

    def get_summary(self) -> dict:
        """Get full FinOps summary for dashboard/docs."""
        platforms = ["openai", "anthropic", "google", "perplexity"]
        summary = {}
        for p in platforms:
            monthly = self.get_spend(p, "month")
            daily = self.get_spend(p, "day")
            summary[p] = {"monthly": monthly, "daily": daily, "can_spend": self.can_spend(p)}
        summary["global"] = self.get_spend(None, "month")
        return summary
