#!/usr/bin/env python3
"""Sincroniza dados agregados do SQLite local com o Supabase.

Lê o papers.db local, agrega dados de citação por vertical e faz
upsert nas tabelas do Supabase via supabase-py. Projetado para
rodar como etapa final do GitHub Actions após a coleta diária.

Uso via CLI:
    python scripts/sync_to_supabase.py [--dry-run] [--vertical fintech]

Uso via comando integrado ao CLI principal:
    python -m src.cli sync

Variáveis de ambiente necessárias:
    SUPABASE_URL  — URL do projeto Supabase (ex: https://xxx.supabase.co)
    SUPABASE_KEY  — Chave service_role do Supabase (acesso total de escrita)
    PAPERS_DB_PATH — Caminho para o SQLite (padrão: data/papers.db)
"""

from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

# Carrega .env do diretório raiz do projeto (papers/)
try:
    from dotenv import load_dotenv
    # Resolve o diretório raiz independente de onde o script é chamado
    _root = Path(__file__).resolve().parent.parent
    load_dotenv(_root / ".env", override=False)
except ImportError:
    pass  # dotenv opcional — variáveis podem vir do ambiente

try:
    from supabase import create_client, Client as SupabaseClient
    _SUPABASE_PY_AVAILABLE = True
except ImportError:
    _SUPABASE_PY_AVAILABLE = False

# ---------------------------------------------------------------------------
# Configuração
# ---------------------------------------------------------------------------

SUPABASE_URL: str = os.getenv("SUPABASE_URL", "").rstrip("/")
SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
DB_PATH: str = os.getenv("PAPERS_DB_PATH", "data/papers.db")

VERTICALS: list[str] = ["fintech", "varejo", "saude", "tecnologia"]

# Tabelas que serão sincronizadas
TABLE_DASHBOARD = "papers_dashboard_data"
TABLE_FINOPS = "papers_finops"

# ---------------------------------------------------------------------------
# SQLite — helpers
# ---------------------------------------------------------------------------


def _open_db(db_path: str) -> sqlite3.Connection:
    """Abre conexão SQLite com row_factory. Usa :memory: se banco não existir."""
    path = Path(db_path)
    if not path.exists():
        print(f"[AVISO] Banco não encontrado: {db_path} — usando banco vazio em memória")
        conn = sqlite3.connect(":memory:")
        conn.row_factory = sqlite3.Row
        return conn
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    return conn


def _query(conn: sqlite3.Connection, sql: str, params: tuple = ()) -> list[dict]:
    """Executa query e retorna lista de dicts. Retorna [] em caso de erro."""
    try:
        rows = conn.execute(sql, params).fetchall()
        return [dict(r) for r in rows]
    except Exception as exc:
        print(f"  [AVISO] Query falhou: {exc}")
        return []


# ---------------------------------------------------------------------------
# Agregações — espelham os padrões de main.py/client.py
# ---------------------------------------------------------------------------


def _citation_rates(conn: sqlite3.Connection, vertical: str) -> list[dict]:
    """Taxa de citação por LLM nos últimos 30 dias para uma vertical."""
    rows = _query(conn, """
        SELECT llm,
               COUNT(*) AS total,
               SUM(CASE WHEN cited THEN 1 ELSE 0 END) AS cited_count,
               AVG(CASE WHEN cited AND position IS NOT NULL
                        THEN CAST(position AS FLOAT) ELSE NULL END) AS avg_pos
        FROM citations
        WHERE timestamp >= datetime('now', '-30 days')
          AND vertical = ?
        GROUP BY llm
        ORDER BY cited_count DESC
    """, (vertical,))

    return [
        {
            "llm": r["llm"],
            "total_queries": r["total"],
            "cited_count": r["cited_count"],
            "citation_rate": round(r["cited_count"] / max(r["total"], 1), 4),
            "avg_position": round(r["avg_pos"], 2) if r["avg_pos"] else None,
        }
        for r in rows
    ]


def _entity_rankings(conn: sqlite3.Connection, vertical: str, top: int = 15) -> list[dict]:
    """Top entidades por contagem de citação dentro de uma vertical."""
    # Usa citation_context + citations quando disponível
    rows = _query(conn, """
        SELECT cc.entity,
               COUNT(*) AS citation_count,
               (SELECT COUNT(*) FROM citations c2
                WHERE c2.vertical = ? AND c2.cited = 1) AS total_cited,
               (SELECT c3.model
                FROM citations c3
                JOIN citation_context cc3 ON cc3.citation_id = c3.id
                WHERE cc3.entity = cc.entity AND c3.vertical = ?
                GROUP BY c3.model
                ORDER BY COUNT(*) DESC
                LIMIT 1) AS top_llm
        FROM citation_context cc
        JOIN citations c ON cc.citation_id = c.id
        WHERE c.vertical = ?
        GROUP BY cc.entity
        ORDER BY citation_count DESC
        LIMIT ?
    """, (vertical, vertical, vertical, top))

    # Fallback: agrega direto de citations.cited_entity quando citation_context vazio
    if not rows:
        rows = _query(conn, """
            SELECT cited_entity AS entity,
                   COUNT(*) AS citation_count,
                   (SELECT COUNT(*) FROM citations c2
                    WHERE c2.vertical = ? AND c2.cited = 1) AS total_cited,
                   (SELECT llm FROM citations c3
                    WHERE c3.cited_entity = c.cited_entity AND c3.vertical = ?
                    GROUP BY c3.llm ORDER BY COUNT(*) DESC LIMIT 1) AS top_llm
            FROM citations c
            WHERE vertical = ?
              AND cited = 1
              AND cited_entity IS NOT NULL
            GROUP BY cited_entity
            ORDER BY citation_count DESC
            LIMIT ?
        """, (vertical, vertical, vertical, top))

    total_cited = rows[0]["total_cited"] if rows else 1
    return [
        {
            "entity": r["entity"],
            "citation_count": r["citation_count"],
            "citation_rate": round(r["citation_count"] / max(total_cited, 1), 4),
            "top_llm": r["top_llm"] or "N/A",
        }
        for r in rows
    ]


def _timeseries(conn: sqlite3.Connection, vertical: str, days: int = 90) -> list[dict]:
    """Série temporal diária de taxa de citação nos últimos N dias."""
    rows = _query(conn, """
        SELECT date(timestamp) AS dt,
               AVG(CASE WHEN cited THEN 1.0 ELSE 0.0 END) AS rate,
               COUNT(*) AS n
        FROM citations
        WHERE vertical = ?
          AND timestamp >= datetime('now', ?)
        GROUP BY dt
        ORDER BY dt ASC
    """, (vertical, f"-{days} days"))

    return [
        {
            "date": r["dt"],
            "rate": round(r["rate"], 4),
            "observations": r["n"],
        }
        for r in rows
    ]


def _collection_status(conn: sqlite3.Connection, vertical: str) -> dict:
    """Status de coleta para uma vertical: último run, runs em 24h, módulos."""
    last = _query(conn, """
        SELECT MAX(timestamp) AS ts
        FROM collection_runs
        WHERE vertical = ? AND status = 'success'
    """, (vertical,))
    last_run = last[0]["ts"] if last and last[0].get("ts") else None

    count_rows = _query(conn, """
        SELECT COUNT(*) AS n
        FROM collection_runs
        WHERE vertical = ?
          AND timestamp >= datetime('now', '-1 day')
    """, (vertical,))
    total_runs_24h = count_rows[0]["n"] if count_rows else 0

    modules_rows = _query(conn, """
        SELECT module, status
        FROM collection_runs
        WHERE vertical = ?
          AND id IN (
              SELECT MAX(id)
              FROM collection_runs
              WHERE vertical = ?
              GROUP BY module
          )
    """, (vertical, vertical))
    modules = {r["module"]: r["status"] for r in modules_rows}

    return {
        "last_run": last_run,
        "total_runs_24h": total_runs_24h,
        "modules": modules,
    }


def _kpis(conn: sqlite3.Connection, vertical: str) -> dict:
    """KPIs agregados: total de observações, taxa geral, entidades monitoradas, dias coletando."""
    stats = _query(conn, """
        SELECT COUNT(*) AS total,
               SUM(CASE WHEN cited THEN 1 ELSE 0 END) AS cited_count
        FROM citations
        WHERE vertical = ?
    """, (vertical,))
    total_obs = stats[0]["total"] if stats else 0
    cited_count = stats[0]["cited_count"] if stats else 0

    # Entidades distintas monitoradas (via citation_context ou verticals config)
    entities = _query(conn, """
        SELECT COUNT(DISTINCT cc.entity) AS n
        FROM citation_context cc
        JOIN citations c ON cc.citation_id = c.id
        WHERE c.vertical = ?
    """, (vertical,))
    if not entities or entities[0]["n"] == 0:
        entities = _query(conn, """
            SELECT json_array_length(cohort_json) AS n
            FROM verticals WHERE slug = ?
        """, (vertical,))
    entities_monitored = entities[0]["n"] if entities else 0

    days = _query(conn, """
        SELECT COUNT(DISTINCT date(timestamp)) AS n
        FROM collection_runs
        WHERE vertical = ? AND status = 'success'
    """, (vertical,))
    days_collecting = days[0]["n"] if days else 0

    return {
        "total_observations": total_obs,
        "overall_rate": round(cited_count / max(total_obs, 1), 4),
        "entities_monitored": entities_monitored,
        "days_collecting": days_collecting,
    }


def _finops_data(conn: sqlite3.Connection) -> dict:
    """Resumo FinOps: orçamento mensal, gasto e breakdown por plataforma."""
    rows = _query(conn, """
        SELECT platform, monthly_spend, monthly_limit, daily_spend, daily_limit,
               queries_today, tokens_today
        FROM finops_usage
    """)

    if not rows:
        return {"budget_monthly": 0, "spent_monthly": 0, "pct_used": 0, "by_platform": {}}

    total_budget = sum(r.get("monthly_limit") or 0 for r in rows)
    total_spent = sum(r.get("monthly_spend") or 0 for r in rows)

    by_platform: dict = {}
    for r in rows:
        by_platform[r["platform"]] = {
            "monthly_spend": r.get("monthly_spend") or 0,
            "monthly_limit": r.get("monthly_limit") or 0,
            "daily_spend": r.get("daily_spend") or 0,
            "daily_limit": r.get("daily_limit") or 0,
            "queries_today": r.get("queries_today") or 0,
            "tokens_today": r.get("tokens_today") or 0,
        }

    return {
        "budget_monthly": round(total_budget, 2),
        "spent_monthly": round(total_spent, 4),
        "pct_used": round(total_spent / max(total_budget, 0.001) * 100, 1),
        "by_platform": by_platform,
    }


# ---------------------------------------------------------------------------
# Supabase — cliente e upsert
# ---------------------------------------------------------------------------


def _build_client() -> "SupabaseClient":
    """Cria e retorna cliente Supabase. Lança RuntimeError se credenciais ausentes."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise RuntimeError(
            "SUPABASE_URL e/ou SUPABASE_KEY não configuradas.\n"
            "Configure em papers/.env ou como variável de ambiente."
        )
    if not _SUPABASE_PY_AVAILABLE:
        raise RuntimeError(
            "Pacote 'supabase' não instalado. Execute: pip install supabase"
        )
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def _upsert(
    client: "SupabaseClient",
    table: str,
    data: list[dict] | dict,
    dry_run: bool = False,
) -> bool:
    """Faz upsert em uma tabela Supabase. Retorna True se bem-sucedido."""
    rows = data if isinstance(data, list) else [data]
    if not rows:
        print(f"  [PULO] {table}: nenhum dado para enviar")
        return True

    if dry_run:
        # Exibe preview sem enviar — útil para testar localmente
        preview = json.dumps(rows[0], ensure_ascii=False, default=str)
        print(f"  [DRY-RUN] {table}: {len(rows)} linha(s) — preview: {preview[:120]}...")
        return True

    try:
        result = (
            client.table(table)
            .upsert(rows, on_conflict="vertical" if table == TABLE_DASHBOARD else "id")
            .execute()
        )
        # supabase-py 2.x levanta exceção em caso de erro HTTP — se chegou aqui, OK
        count = len(result.data) if hasattr(result, "data") and result.data else len(rows)
        print(f"  [OK] {table}: {count} linha(s) enviada(s)")
        return True
    except Exception as exc:
        print(f"  [ERRO] {table}: {exc}")
        return False


# ---------------------------------------------------------------------------
# Sync principal
# ---------------------------------------------------------------------------


def run_sync(
    db_path: str | None = None,
    verticals: list[str] | None = None,
    dry_run: bool = False,
    verbose: bool = True,
) -> int:
    """Executa sincronização completa do SQLite para o Supabase.

    Returns:
        0 — sucesso, 1 — um ou mais erros ocorreram, 2 — credenciais ausentes (skip)
    """
    _db = db_path or DB_PATH
    _verticals = verticals or VERTICALS

    # Verifica credenciais antes de abrir banco (evita trabalho desnecessário)
    if not dry_run and (not SUPABASE_URL or not SUPABASE_KEY):
        if verbose:
            print("[SKIP] SUPABASE_URL ou SUPABASE_KEY não configuradas. Sync ignorado.")
            print("       Configure em papers/.env ou adicione ao secrets do GitHub Actions.")
        return 2

    if verbose:
        mode = " (DRY-RUN — sem envio real)" if dry_run else ""
        print(f"=== Sync Papers -> Supabase{mode} ===")
        print(f"  Banco: {_db}")
        if not dry_run:
            print(f"  Supabase: {SUPABASE_URL}")
        print(f"  Verticais: {', '.join(_verticals)}")
        print()

    conn = _open_db(_db)
    now = datetime.now(timezone.utc).isoformat()
    errors = 0

    # Cria cliente Supabase (ou None em dry-run)
    client: SupabaseClient | None = None
    if not dry_run:
        try:
            client = _build_client()
        except RuntimeError as exc:
            print(f"[ERRO] {exc}")
            conn.close()
            return 1

    # ----- Dashboard data por vertical -----
    dashboard_rows: list[dict] = []
    for v in _verticals:
        if verbose:
            print(f"[{v}] Agregando dados...")

        cr = _citation_rates(conn, v)
        er = _entity_rankings(conn, v)
        ts = _timeseries(conn, v)
        cs = _collection_status(conn, v)
        kp = _kpis(conn, v)

        if verbose:
            obs = kp.get("total_observations", 0)
            print(f"  LLMs: {len(cr)} | Entidades: {len(er)} | Série temporal: {len(ts)} pts | Obs: {obs}")

        dashboard_rows.append({
            "vertical": v,
            "citation_rates": cr,
            "entity_rankings": er,
            "timeseries": ts,
            "collection_status": cs,
            "kpis": kp,
            "updated_at": now,
        })

    if verbose:
        print()
        print(f"Enviando {TABLE_DASHBOARD}...")

    if dry_run:
        if not _upsert(None, TABLE_DASHBOARD, dashboard_rows, dry_run=True):
            errors += 1
    else:
        if not _upsert(client, TABLE_DASHBOARD, dashboard_rows):
            errors += 1

    # ----- FinOps -----
    if verbose:
        print()
        print("Agregando FinOps...")

    finops = _finops_data(conn)
    finops["id"] = "global"
    finops["updated_at"] = now

    if verbose:
        print(
            f"  Orçamento: ${finops['budget_monthly']:.2f} | "
            f"Gasto: ${finops['spent_monthly']:.4f} | "
            f"Uso: {finops['pct_used']:.1f}%"
        )
        print(f"Enviando {TABLE_FINOPS}...")

    if dry_run:
        if not _upsert(None, TABLE_FINOPS, finops, dry_run=True):
            errors += 1
    else:
        if not _upsert(client, TABLE_FINOPS, finops):
            errors += 1

    conn.close()

    if verbose:
        print()
        if errors:
            print(f"=== Sync concluído com {errors} erro(s) ===")
        else:
            label = "DRY-RUN" if dry_run else "sucesso"
            print(f"=== Sync concluído com {label} ===")

    return 1 if errors else 0


# ---------------------------------------------------------------------------
# Entrada direta via linha de comando
# ---------------------------------------------------------------------------


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sincroniza dados agregados do papers.db para o Supabase.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python scripts/sync_to_supabase.py
  python scripts/sync_to_supabase.py --dry-run
  python scripts/sync_to_supabase.py --vertical fintech
  python scripts/sync_to_supabase.py --vertical fintech varejo --dry-run
        """,
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Agrega e exibe dados sem enviar ao Supabase.",
    )
    parser.add_argument(
        "--vertical",
        nargs="+",
        choices=VERTICALS,
        metavar="VERTICAL",
        help=f"Verticais a sincronizar (padrão: todas). Opções: {', '.join(VERTICALS)}",
    )
    parser.add_argument(
        "--db",
        default=None,
        metavar="PATH",
        help=f"Caminho para o banco SQLite (padrão: {DB_PATH})",
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suprime output informativo (apenas erros).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    return run_sync(
        db_path=args.db,
        verticals=args.vertical,
        dry_run=args.dry_run,
        verbose=not args.quiet,
    )


if __name__ == "__main__":
    sys.exit(main())
