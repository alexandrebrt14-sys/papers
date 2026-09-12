"""Encerramento: entradas recusadas sem rede, cache ou novas observações."""
from __future__ import annotations

import importlib
import json
import sys
import urllib.request
from datetime import UTC, datetime
from pathlib import Path

import httpx
import pytest
import requests
from click.testing import CliRunner
from fastapi.testclient import TestClient

from src.collection_policy import (
    COLLECTION_CLOSED_ON,
    CollectionClosedError,
    require_collection_open,
)


def forbidden(*args, **kwargs):
    pytest.fail("A operação encerrada tentou acessar rede, cache ou banco")


@pytest.fixture(autouse=True)
def isolated(monkeypatch, tmp_path):
    # HTTP real proibido; o transporte em memória do TestClient continua permitido.
    monkeypatch.setattr(httpx.HTTPTransport, "handle_request", forbidden)
    monkeypatch.setattr(requests.Session, "send", forbidden)
    monkeypatch.setattr(urllib.request, "urlopen", forbidden)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("PAPERS_DB_PATH", str(tmp_path / "never-created.db"))
    monkeypatch.setenv("PAPERS_PARTIAL_DAYS_PATH", str(tmp_path / "partial.json"))
    monkeypatch.setenv("GITHUB_ENV", str(tmp_path / "github-env"))
    yield
    assert list(tmp_path.iterdir()) == [], "A entrada bloqueada escreveu no disco"


def test_encerramento_nao_pode_ser_reaberto_por_ambiente(monkeypatch):
    monkeypatch.setenv("PAPERS_COLLECTION_ENABLED", "1")
    monkeypatch.setenv("PAPERS_COLLECTION_CLOSED", "0")
    monkeypatch.setenv("PAPERS_METHODOLOGY_VERSION", "v1")
    assert COLLECTION_CLOSED_ON == "2026-09-11"
    with pytest.raises(CollectionClosedError, match="11/09/2026"):
        require_collection_open()


@pytest.mark.parametrize("command", [
    ["collect", "all"], ["collect", "citation"], ["collect", "competitor"],
    ["collect", "serp"], ["intervention", "check"],
])
@pytest.mark.parametrize("vertical", ["fintech", "all"])
def test_cli_recusa_antes_de_abrir_banco(monkeypatch, command, vertical):
    from src import cli
    monkeypatch.setattr(cli, "get_db", forbidden)
    result = CliRunner().invoke(cli.main, ["--vertical", vertical, *command])
    assert result.exit_code == 1
    assert "11/09/2026" in result.output
    assert "consulta, exportação e análise" in result.output


@pytest.mark.parametrize("name", [
    "query", "_dispatch", "_query_openai", "_query_anthropic", "_query_google",
    "_query_groq", "_query_xai", "_query_perplexity", "_query_perplexity_agent",
])
def test_cliente_recusa_inclusive_adaptadores_diretos(name):
    from src.collectors.llm_client import LLMClient
    # Sem configuração, chave ou cache: a trava precisa ser a primeira operação.
    client = object.__new__(LLMClient)
    args = (None, "consulta") if name == "query" else (None, "consulta", datetime.now(UTC))
    with pytest.raises(CollectionClosedError):
        getattr(client, name)(*args)


@pytest.mark.parametrize("module,cls", [
    ("citation_tracker", "CitationTracker"), ("competitor", "CompetitorBenchmark"),
    ("serp_overlap", "SerpAIOverlap"), ("dual_collector", "DualCollector"),
    ("prompt_sensitivity", "PromptSensitivityAnalyzer"), ("intervention", "InterventionTracker"),
])
def test_coletores_recusam_antes_de_log_e_consulta(module, cls):
    collector = getattr(importlib.import_module(f"src.collectors.{module}"), cls)
    with pytest.raises(CollectionClosedError):
        object.__new__(collector).collect()


def test_intervencao_recusa_antes_de_ler_o_banco():
    from src.collectors.intervention import InterventionTracker
    with pytest.raises(CollectionClosedError):
        InterventionTracker.check_active_interventions(None)


@pytest.mark.parametrize("name", [
    "query_openai", "query_anthropic", "query_gemini", "query_perplexity",
    "query_grok", "query_groq", "query_all_llms", "query_single_llm",
])
def test_adaptadores_legados_nao_leem_cache(monkeypatch, name):
    from src.shared import llm_utils
    monkeypatch.setattr(llm_utils, "_cache_get", forbidden)
    with pytest.raises(CollectionClosedError):
        getattr(llm_utils, name)("consulta", "test-key")


def test_brave_e_verificacao_de_urls_nao_fazem_novas_observacoes():
    from src.collectors.brave_search import BraveSearchClient
    from src.collectors.url_verifier import URLVerifier
    with pytest.raises(CollectionClosedError):
        object.__new__(BraveSearchClient).search("consulta")
    with pytest.raises(CollectionClosedError):
        object.__new__(URLVerifier).verify_url("https://example.org")
    with pytest.raises(CollectionClosedError):
        object.__new__(URLVerifier).verify_batch(["https://example.org"])


def test_preflight_terminal_recusa_antes_das_sondas(monkeypatch, capsys):
    from scripts import preflight_llm_check as pf
    for name in ["check_openai", "check_anthropic", "check_google", "check_perplexity", "check_grok"]:
        monkeypatch.setattr(pf, name, forbidden)
    assert pf.main() == 2
    assert "11/09/2026" in capsys.readouterr().err


@pytest.mark.parametrize("name", ["check_openai", "check_anthropic", "check_google", "check_perplexity", "check_grok"])
def test_preflight_direto_recusa_antes_do_http(name):
    from scripts import preflight_llm_check as pf
    with pytest.raises(CollectionClosedError):
        getattr(pf, name)("test-key")


def test_sonda_anthropic_do_finops_nao_gera_tokens():
    from src.finops.secrets import validate_key_health
    result = validate_key_health("anthropic", "test-key")
    assert result["status"] == "skipped_project_closed"
    assert "11/09/2026" in result["reason"]


def test_api_recusa_sem_tarefa_em_segundo_plano(monkeypatch):
    from src.api import main as api
    monkeypatch.setattr(api, "_tasks", {})
    monkeypatch.setattr(api, "get_db", forbidden)
    api.app.dependency_overrides[api.verify_api_key] = lambda: None
    try:
        # Sem iniciar lifespan: verifica somente o contrato desta requisição.
        client = TestClient(api.app)
        response = client.post("/api/collections/trigger", json={"vertical": "all"})
        assert response.status_code == 410
        assert "11/09/2026" in response.json()["detail"]
        assert api._tasks == {}
    finally:
        api.app.dependency_overrides.clear()
        client.close()


def test_api_tarefa_antiga_nao_conecta_no_banco(monkeypatch):
    from src.api import main as api
    from src.api.models import TaskStatus
    task = TaskStatus(task_id="old", status="queued", vertical="fintech")
    monkeypatch.setattr(api, "_tasks", {"old": task})
    monkeypatch.setattr(api, "DatabaseClient", forbidden)
    api._run_collection("old", "fintech", ["citation_tracker"])
    assert task.status == "failed"
    assert "11/09/2026" in task.error


def test_funcoes_de_analise_historica_continuam_disponiveis():
    from src.collectors.context_analyzer import CitationContextAnalyzer
    from src.collectors.llm_client import apply_citation_window
    from src.collectors.url_verifier import URLVerifier
    context = CitationContextAnalyzer().analyze("Nubank", "Nubank is the leading digital bank.")
    assert context["cited"] and context["sentiment"] == "positive"
    assert apply_citation_window("Nubank") == "Nubank"
    assert object.__new__(URLVerifier).hallucination_rate([
        {"is_real": True}, {"is_real": False},
    ]) == {"total": 2, "real": 1, "hallucinated": 1, "rate": 0.5}


def test_cli_preserva_comandos_historicos(monkeypatch):
    from src import cli
    from src.config import mandatory_llms
    class Rows:
        def fetchall(self):
            return [(llm, 1) for llm in mandatory_llms()]
    class DB:
        def execute(self, *args):
            return Rows()
        def close(self):
            pass
        @property
        def _conn(self):
            return self
    monkeypatch.setattr(cli, "get_db", DB)
    result = CliRunner().invoke(cli.main, ["collect", "validate-run"])
    assert result.exit_code == 0, result.output
    for command in [["collect", "context", "--help"], ["analyze", "report", "--help"], ["db", "export", "--help"]]:
        assert CliRunner().invoke(cli.main, command).exit_code == 0


@pytest.mark.parametrize("filename", ["daily-collect.yml", "weekly-benchmark.yml", "weekly-calibration.yml"])
def test_workflows_sem_agendamento_ou_execucao_de_coleta(filename):
    root = Path(__file__).resolve().parents[1]
    text = (root / ".github/workflows" / filename).read_text(encoding="utf-8")
    assert "schedule:" not in text and "cron:" not in text
    assert "workflow_dispatch:" in text
    assert "exit 1" in text and "11/09/2026" in text
    assert "secrets." not in text and "actions/checkout" not in text
    assert "python" not in text and "pip install" not in text


@pytest.mark.parametrize("args", [[], ["--json"], ["--no-alert"], ["--min-obs-per-day", "1"]])
def test_health_check_encerrado_nao_carrega_credenciais_nem_envia_alertas(monkeypatch, capsys, args):
    from scripts import health_check as hc
    monkeypatch.setattr(sys, "argv", ["health_check.py", *args])
    monkeypatch.setattr(hc, "_get_conn", forbidden)
    monkeypatch.setattr(hc, "check_db_exists", forbidden)
    monkeypatch.setattr(hc, "check_api_keys_valid", forbidden)
    monkeypatch.setattr(hc, "send_alert", forbidden)
    monkeypatch.setattr(hc.Path, "read_text", forbidden)
    assert hc.main() == 0
    output = capsys.readouterr().out
    if "--json" in args:
        result = json.loads(output)
        assert result["status"] == "closed"
        assert result["closed_on"] == "2026-09-11"
        assert result["collection_enabled"] is False
        assert result["alerts_sent"] is False
        assert result["checks"] == [] and result["total"] == 0
    else:
        assert "11/09/2026" in output


def test_health_check_sondas_diretas_recusadas_com_chaves_presentes(monkeypatch):
    from scripts import health_check as hc
    for key in ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GOOGLE_AI_API_KEY", "PERPLEXITY_API_KEY"]:
        monkeypatch.setenv(key, "test-key")
    with pytest.raises(CollectionClosedError):
        hc.check_api_keys_valid()


def test_health_check_alerta_antigo_nao_e_enviado(monkeypatch):
    from scripts import health_check as hc
    monkeypatch.setenv("RESEND_API_KEY", "test-key")
    monkeypatch.setenv("WHATSAPP_API_TOKEN", "test-key")
    monkeypatch.setenv("WHATSAPP_PHONE_ID", "test-id")
    checks = [hc.Check("Coleta diária").fail("Sem novas observações")]
    assert hc.send_alert(checks, {}) is False


def test_health_check_preserva_verificacao_local_do_detector():
    from scripts import health_check as hc
    result = hc.check_word_boundary_matching()
    assert result.passed
