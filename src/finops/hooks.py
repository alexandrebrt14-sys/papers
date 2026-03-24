"""
hooks.py -- Post-collection hooks for automated FinOps.

These hooks are called automatically by the CLI after each collection
command completes, ensuring FinOps data is always fresh.
"""
from __future__ import annotations

import logging

logger = logging.getLogger("finops.hooks")


def post_collection_hook(module_name: str, records_count: int, duration_ms: int) -> None:
    """Run after every collection module completes.

    Called automatically by CLI collect commands.
    Triggers: rollup, budget check, checkpoint export.
    """
    from src.finops.monitor import run_monitor

    logger.info(f"[finops] Post-collection hook: {module_name} ({records_count} records, {duration_ms}ms)")

    # Run the full monitor cycle (non-verbose in hook mode)
    try:
        run_monitor(verbose=False)
    except Exception as e:
        # Never let FinOps errors block data collection
        logger.error(f"[finops] Monitor error (non-blocking): {e}")
