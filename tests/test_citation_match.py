"""Citação por domínio/URL nas fontes da resposta. Funções puras, sem rede."""
from __future__ import annotations

import base64
import json
from pathlib import Path

import pytest

from src.analysis.citation_match import (
    canonical_url,
    find_citation,
    host_matches_domain,
    normalize_host,
    source_urls,
    strip_tracking,
    unwrap_redirect,
)

FIXTURE = Path(__file__).parent / "fixtures" / "interface" / "cloro_chatgpt_br.json"


@pytest.mark.parametrize("entrada,esperado", [
    ("https://WWW.Nubank.com.br:443/conta", "nubank.com.br"),
    ("nubank.com.br", "nubank.com.br"),
    ("//m.nubank.com.br/x", "nubank.com.br"),
    ("https://user:senha@www.nubank.com.br./", "nubank.com.br"),
    ("https://" + "itaú.com.br".encode("idna").decode(), "itaú.com.br"),  # punycode
    ("", ""),
])
def test_normalize_host(entrada, esperado):
    assert normalize_host(entrada) == esperado


@pytest.mark.parametrize("host,dominio,esperado", [
    ("blog.nubank.com.br", "nubank.com.br", True),
    ("nubank.com.br", "https://www.nubank.com.br/", True),
    ("notnubank.com.br", "nubank.com.br", False),
    ("nubank.com.br.golpe.io", "nubank.com.br", False),
    ("nubank.com", "nubank.com.br", False),
])
def test_casamento_por_rotulo(host, dominio, esperado):
    assert host_matches_domain(host, dominio) is esperado


def test_subdominio_pode_ser_excluido():
    assert not host_matches_domain("blog.nubank.com.br", "nubank.com.br", include_subdomains=False)


def test_remove_utm_e_rastreadores_mas_preserva_parametros_reais():
    url = "https://nubank.com.br/p?id=7&utm_source=chatgpt.com&UTM_medium=x&gclid=abc&fbclid=z#topo"
    assert strip_tracking(url) == "https://nubank.com.br/p?id=7"


@pytest.mark.parametrize("url,alvo", [
    ("https://www.google.com/url?q=https://nubank.com.br/&sa=U", "https://nubank.com.br/"),
    ("https://www.google.com.br/url?url=https%3A%2F%2Fstone.com.br%2F", "https://stone.com.br/"),
    ("https://l.facebook.com/l.php?u=https%3A%2F%2Fpicpay.com%2F", "https://picpay.com/"),
    ("https://duckduckgo.com/l/?uddg=https%253A%252F%252Fcielo.com.br", "https://cielo.com.br"),
])
def test_desembrulha_redirecionadores(url, alvo):
    target, ok = unwrap_redirect(url)
    assert ok and target == alvo


def test_desembrulha_bing_em_base64():
    alvo = "https://www.inter.co/conta"
    code = base64.urlsafe_b64encode(alvo.encode()).decode().rstrip("=")
    target, ok = unwrap_redirect(f"https://www.bing.com/ck/a?!&&p=x&u=a1{code}&ntb=1")
    assert ok and target == alvo


@pytest.mark.parametrize("url", [
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AbC",
    "https://www.google.com/goto?enc=xyz",
    "https://t.co/abc",
])
def test_redirecionador_cifrado_fica_nao_resolvido(url):
    assert unwrap_redirect(url) == (url, False)


def test_busca_do_google_nao_e_redirecionador():
    url = "https://www.google.com/search?q=https://nubank.com.br"
    assert unwrap_redirect(url) == (url, True)


def test_canonical_url_une_variantes():
    a = canonical_url("https://www.google.com/url?q=https://WWW.nubank.com.br/conta/?utm_source=x")
    b = canonical_url("http://nubank.com.br/conta")
    assert a == b == "https://nubank.com.br/conta"
    assert canonical_url("") == ""


def test_source_urls_aceita_formatos_dos_motores():
    fontes = ["https://a.com", {"url": "https://b.com"}, {"link": "https://c.com"},
              {"web": {"uri": "https://d.com"}}, {"label": "sem url"}, "", None]
    assert source_urls(fontes) == ["https://a.com", "https://b.com", "https://c.com", "https://d.com"]


def test_fixture_cloro_citacao_por_dominio():
    result = json.loads(FIXTURE.read_text(encoding="utf-8"))["result"]
    fontes = result["sources"] + result["citationPills"]
    nubank = find_citation(fontes, "nubank.com.br")
    assert nubank.cited and nubank.matched_urls == ("https://nubank.com.br/conta",)
    inter = find_citation(fontes, "bancointer.com.br")
    assert inter.cited  # via google.com/url e subdomínio blog.
    c6 = find_citation(fontes, "https://www.c6bank.com.br")
    assert c6.cited
    picpay = find_citation(fontes, "picpay.com")
    assert not picpay.cited and picpay.unresolved_redirects == 1 and picpay.undetermined


def test_sem_fontes():
    m = find_citation(None, "nubank.com.br")
    assert not m.cited and not m.undetermined


def test_dominio_parecido_com_google_nao_e_redirecionador():
    url = "https://notgoogle.com/url?q=https://golpe.io"
    assert unwrap_redirect(url) == (url, True)
    assert unwrap_redirect("https://evil-duckduckgo.com/l/?uddg=https://x.io")[0].startswith("https://evil")
