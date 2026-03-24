"""
update-docs.py -- Atualização automática de documentação evolutiva
Roda após cada coleta para manter docs sincronizados com o estado real.

Atualiza:
  - docs/CHANGELOG.md (métricas auto-geradas)
  - docs/GOVERNANCE.md (resumo FinOps)
  - docs/STATUS.md (snapshot completo do estado atual)
  - README.md (badges e métricas)

Uso:
  python scripts/update-docs.py              # Atualiza tudo
  python scripts/update-docs.py --commit     # Atualiza e commita
  python scripts/update-docs.py --status     # Só gera STATUS.md
"""
import sys
import os
import re
import sqlite3
import subprocess
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).parent.parent
DB_PATH = ROOT / "data" / "papers.db"
SCRIPTS_DB = Path("C:/Sandyboxclaude/Logss/geo_metrics.db")
DOCS = ROOT / "docs"


def get_db():
    """Conecta ao banco de dados (papers ou geo_metrics)"""
    path = DB_PATH if DB_PATH.exists() else SCRIPTS_DB
    if not path.exists():
        return None
    return sqlite3.connect(str(path))


def count_lines():
    """Conta linhas de código Python no projeto"""
    total = 0
    for f in ROOT.rglob("*.py"):
        if ".git" in str(f) or "__pycache__" in str(f) or "venv" in str(f):
            continue
        try:
            total += len(f.read_text(encoding="utf-8").splitlines())
        except Exception:
            pass
    return total


def count_tests():
    """Conta testes no projeto"""
    total = 0
    for f in (ROOT / "tests").rglob("*.py"):
        try:
            content = f.read_text(encoding="utf-8")
            total += len(re.findall(r"def test_", content))
        except Exception:
            pass
    return total


def get_git_stats():
    """Obtém estatísticas do git"""
    try:
        commits = subprocess.run(
            ["git", "rev-list", "--count", "HEAD"],
            capture_output=True, text=True, cwd=str(ROOT)
        ).stdout.strip()
        last_commit = subprocess.run(
            ["git", "log", "-1", "--format=%H %s"],
            capture_output=True, text=True, cwd=str(ROOT)
        ).stdout.strip()
        branch = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True, text=True, cwd=str(ROOT)
        ).stdout.strip()
        return {
            "total_commits": int(commits) if commits else 0,
            "last_commit": last_commit,
            "branch": branch,
        }
    except Exception:
        return {"total_commits": 0, "last_commit": "", "branch": "main"}


def get_db_stats():
    """Obtém estatísticas do banco de dados"""
    conn = get_db()
    if not conn:
        return {"tables": 0, "citations": 0, "citation_rate": "—", "last_collection": "—",
                "competitors": 0, "experiments": 0}

    try:
        cursor = conn.cursor()
        tables = cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
        table_count = len(tables)

        stats = {"tables": table_count}

        # Citations
        try:
            total = cursor.execute("SELECT COUNT(*) FROM citations").fetchone()[0]
            cited = cursor.execute("SELECT COUNT(*) FROM citations WHERE cited = 1").fetchone()[0]
            rate = round(cited / max(total, 1) * 100, 1)
            stats["citations"] = total
            stats["citation_rate"] = f"{rate}%"
        except Exception:
            stats["citations"] = 0
            stats["citation_rate"] = "—"

        # Last collection
        try:
            last = cursor.execute(
                "SELECT MAX(timestamp) FROM citations"
            ).fetchone()[0]
            stats["last_collection"] = last[:16] if last else "—"
        except Exception:
            stats["last_collection"] = "—"

        # Competitors
        try:
            stats["competitors"] = cursor.execute(
                "SELECT COUNT(*) FROM competitor_citations"
            ).fetchone()[0]
        except Exception:
            stats["competitors"] = 0

        # Experiments
        try:
            stats["experiments"] = cursor.execute(
                "SELECT COUNT(*) FROM experiments"
            ).fetchone()[0]
        except Exception:
            stats["experiments"] = 0

        # FinOps
        try:
            finops = {}
            for platform in ["openai", "anthropic", "gemini", "perplexity"]:
                row = cursor.execute(
                    "SELECT COALESCE(SUM(cost_usd), 0) FROM finops_usage WHERE platform = ? AND timestamp >= ?",
                    [platform, datetime.now(timezone.utc).strftime("%Y-%m-01T00:00:00")]
                ).fetchone()
                finops[platform] = round(row[0], 4) if row else 0
            finops["global"] = sum(finops.values())
            stats["finops"] = finops
        except Exception:
            stats["finops"] = {}

        conn.close()
        return stats
    except Exception:
        conn.close()
        return {"tables": 0, "citations": 0, "citation_rate": "—", "last_collection": "—"}


def get_finops_limits():
    """Obtém limites FinOps do banco"""
    conn = get_db()
    if not conn:
        return {}
    try:
        cursor = conn.cursor()
        rows = cursor.execute("SELECT platform, monthly_limit_usd FROM finops_budgets").fetchall()
        conn.close()
        return {r[0]: r[1] for r in rows}
    except Exception:
        conn.close()
        return {}


def update_changelog(stats, db_stats):
    """Atualiza seção auto-gerada do CHANGELOG.md"""
    path = DOCS / "CHANGELOG.md"
    if not path.exists():
        return

    content = path.read_text(encoding="utf-8")
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    replacement = f"""<!-- AUTOGENERATED SECTION — atualizado por scripts/update-docs.py -->
## Métricas do Projeto (auto-atualizado)

| Métrica | Valor |
|---------|-------|
| Linhas de código | {stats['lines']:,} |
| Testes | {stats['tests']} |
| Tabelas no banco | {db_stats['tables']} |
| Queries monitoradas | 55 |
| Concorrentes | 15 |
| LLMs suportados | 5 |
| Última coleta | {db_stats['last_collection']} |
| Total de citações | {db_stats['citations']:,} |
| Taxa de citação | {db_stats['citation_rate']} |

*Atualizado automaticamente em {now}*
<!-- END AUTOGENERATED -->"""

    content = re.sub(
        r"<!-- AUTOGENERATED SECTION.*?<!-- END AUTOGENERATED -->",
        replacement, content, flags=re.DOTALL
    )
    path.write_text(content, encoding="utf-8")
    print(f"  [OK] CHANGELOG.md atualizado")


def update_governance(db_stats):
    """Atualiza seção FinOps do GOVERNANCE.md"""
    path = DOCS / "GOVERNANCE.md"
    if not path.exists():
        return

    content = path.read_text(encoding="utf-8")
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    finops = db_stats.get("finops", {})
    limits = get_finops_limits()

    rows = ""
    for p in ["openai", "anthropic", "gemini", "perplexity"]:
        spend = finops.get(p, 0)
        limit = limits.get(p, 10)
        pct = round(spend / max(limit, 0.001) * 100, 1)
        rows += f"| {p} | ${spend:.4f} | ${limit:.2f} | {pct}% |\n"

    global_spend = finops.get("global", 0)
    global_limit = limits.get("global", 30)
    global_pct = round(global_spend / max(global_limit, 0.001) * 100, 1)
    rows += f"| **global** | **${global_spend:.4f}** | **${global_limit:.2f}** | **{global_pct}%** |"

    replacement = f"""<!-- AUTOGENERATED: Resumo FinOps -->
## Resumo FinOps (auto-atualizado)

| Plataforma | Gasto Mensal | Limite | % Usado |
|-----------|-------------|--------|---------|
{rows}

*Atualizado automaticamente em {now}*
<!-- END AUTOGENERATED -->"""

    content = re.sub(
        r"<!-- AUTOGENERATED: Resumo FinOps -->.*?<!-- END AUTOGENERATED -->",
        replacement, content, flags=re.DOTALL
    )

    # Atualizar data no header
    content = re.sub(
        r"\*\*Última atualização:\*\* \d{4}-\d{2}-\d{2}",
        f"**Última atualização:** {datetime.now(timezone.utc).strftime('%Y-%m-%d')}",
        content
    )

    path.write_text(content, encoding="utf-8")
    print(f"  [OK] GOVERNANCE.md atualizado")


def generate_status(stats, db_stats, git_stats):
    """Gera STATUS.md com snapshot completo do estado atual"""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    finops = db_stats.get("finops", {})

    status = f"""# Status do Projeto — Papers

**Gerado automaticamente em:** {now}
**Branch:** {git_stats['branch']} | **Commits:** {git_stats['total_commits']}
**Último commit:** {git_stats['last_commit'][:80]}

---

## Saúde do Projeto

| Indicador | Valor | Status |
|-----------|-------|--------|
| Código (linhas Python) | {stats['lines']:,} | {'OK' if stats['lines'] > 1000 else 'Baixo'} |
| Testes unitários | {stats['tests']} | {'OK' if stats['tests'] >= 15 else 'Insuficiente'} |
| Tabelas no banco | {db_stats['tables']} | {'OK' if db_stats['tables'] >= 7 else 'Incompleto'} |
| Citações coletadas | {db_stats['citations']:,} | {'Coletando' if db_stats['citations'] > 0 else 'Aguardando API keys'} |
| Taxa de citação | {db_stats['citation_rate']} | — |
| Última coleta | {db_stats['last_collection']} | {'Ativo' if db_stats['last_collection'] != '—' else 'Pendente'} |

## FinOps — Gastos do Mês

| Plataforma | Gasto (USD) |
|-----------|------------|
| OpenAI | ${finops.get('openai', 0):.4f} |
| Anthropic | ${finops.get('anthropic', 0):.4f} |
| Gemini | ${finops.get('gemini', 0):.4f} |
| Perplexity | ${finops.get('perplexity', 0):.4f} |
| **Total** | **${finops.get('global', 0):.4f}** |

## Próximas Ações

- {'Adicionar créditos às APIs (OpenAI, Anthropic, Gemini)' if db_stats['citations'] == 0 else 'Coleta ativa — acumular dados'}
- {'Primeira coleta pendente' if db_stats['last_collection'] == '—' else f"Continuar coleta diária (objetivo: 90+ dias)"}
- {'Configurar GitHub Secrets para CI/CD' if db_stats['citations'] == 0 else 'CI/CD configurado'}

## Roadmap para Publicação

| Marco | Requisito | Status |
|-------|-----------|--------|
| Dados mínimos | 1.000 citações | {db_stats['citations']:,}/1.000 |
| Série temporal | 90 dias contínuos | {'Pendente' if db_stats['last_collection'] == '—' else 'Em progresso'} |
| Grupo de controle | 15 concorrentes | {db_stats.get('competitors', 0):,} observações |
| Análise estatística | p < 0.05 | {'Pendente' if db_stats['citations'] < 100 else 'Disponível'} |
| Preprint | ArXiv submission | Pendente |

---

*Gerado por `scripts/update-docs.py` — GEO Research*
"""
    (DOCS / "STATUS.md").write_text(status, encoding="utf-8")
    print(f"  [OK] STATUS.md gerado")


def main():
    print(f"{'='*50}")
    print(f"  Atualizando documentação — Papers")
    print(f"  {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"{'='*50}")

    # Coletar métricas
    stats = {
        "lines": count_lines(),
        "tests": count_tests(),
    }
    db_stats = get_db_stats()
    git_stats = get_git_stats()

    print(f"\n  Código: {stats['lines']:,} linhas | Testes: {stats['tests']}")
    print(f"  Banco: {db_stats['tables']} tabelas | Citações: {db_stats['citations']:,}")
    print(f"  Git: {git_stats['total_commits']} commits | Branch: {git_stats['branch']}")

    # Atualizar documentos
    print()
    update_changelog(stats, db_stats)
    update_governance(db_stats)
    generate_status(stats, db_stats, git_stats)

    # Commit se solicitado
    if "--commit" in sys.argv:
        print(f"\n  Commitando mudanças...")
        subprocess.run(["git", "add", "docs/"], cwd=str(ROOT))
        result = subprocess.run(
            ["git", "commit", "-m", f"docs: auto-update documentation ({datetime.now(timezone.utc).strftime('%Y-%m-%d')})"],
            capture_output=True, text=True, cwd=str(ROOT)
        )
        if result.returncode == 0:
            print(f"  [OK] Commit criado")
        else:
            print(f"  [INFO] Nada para commitar (docs já atualizados)")

    print(f"\n{'='*50}")
    print(f"  Documentação atualizada.")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
