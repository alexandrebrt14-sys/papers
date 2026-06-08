#!/usr/bin/env python3
"""gsc_reindex.py — (re)submete sitemap e inspeciona status de indexacao
das paginas do projeto papers no Google Search Console.

Uso:
    # 1) Autenticar (interativo, uma vez) com o escopo do Search Console:
    #    gcloud auth application-default login \
    #      --scopes=https://www.googleapis.com/auth/webmasters,https://www.googleapis.com/auth/cloud-platform
    # 2) Rodar:
    #    python scripts/gsc_reindex.py

Nao existe API publica para "Request Indexing" de paginas comuns. Este script
faz o que a API suporta: resubmete o sitemap (forca recrawl) e le o status de
indexacao via URL Inspection API.
"""
import json
import os
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request

DOMAIN = "alexandrecaramaschi.com"
SITEMAP = f"https://{DOMAIN}/sitemap-index.xml"
PAGES = [
    f"https://{DOMAIN}/research",
    f"https://{DOMAIN}/papers-roadmap",
    f"https://{DOMAIN}/roadmap",
]


def token() -> str:
    # Permite injetar o token via env (util no Windows, onde gcloud e .cmd).
    env_tok = os.environ.get("GSC_TOKEN")
    if env_tok:
        return env_tok.strip()
    gcloud = shutil.which("gcloud") or shutil.which("gcloud.cmd") or "gcloud"
    # shell=True only on Windows (os.name == "nt") to resolve the gcloud.cmd shim via
    # cmd.exe; on Linux/macOS shell=False. argv is a list of literals and gcloud path
    # comes from shutil.which — no user-controlled input, so CWE-78 does not apply.
    out = subprocess.run(  # nosec B602
        [gcloud, "auth", "application-default", "print-access-token"],
        capture_output=True, text=True, shell=(os.name == "nt"),
    )
    if out.returncode != 0:
        sys.exit("ERRO: sem ADC. Rode primeiro:\n"
                 "  gcloud auth application-default login "
                 "--scopes=https://www.googleapis.com/auth/webmasters,"
                 "https://www.googleapis.com/auth/cloud-platform")
    return out.stdout.strip()


def api(method: str, url: str, tok: str, body: dict | None = None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {tok}")
    req.add_header("Content-Type", "application/json")
    quota = os.environ.get("GSC_QUOTA_PROJECT")
    if quota:
        req.add_header("x-goog-user-project", quota)
    try:
        with urllib.request.urlopen(req) as r:
            raw = r.read().decode()
            return r.status, (json.loads(raw) if raw.strip() else {})
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()}


def main():
    tok = token()

    # --- Descobrir a propriedade que cobre o dominio ---
    st, sites = api("GET", "https://www.googleapis.com/webmasters/v3/sites", tok)
    if st != 200:
        sys.exit(f"Falha ao listar propriedades ({st}): {sites}")
    entries = sites.get("siteEntry", [])
    print("Propriedades no Search Console:")
    for e in entries:
        print(f"  - {e['siteUrl']}  [{e.get('permissionLevel')}]")

    candidates = [e["siteUrl"] for e in entries if DOMAIN in e["siteUrl"]]
    # Preferir domain property (sc-domain:) se existir
    candidates.sort(key=lambda s: (not s.startswith("sc-domain:"), s))
    if not candidates:
        sys.exit(f"Nenhuma propriedade cobre {DOMAIN}. Verifique a conta logada.")
    site_url = candidates[0]
    print(f"\nUsando propriedade: {site_url}")

    # --- (Re)submeter o sitemap-index ---
    feed = urllib.parse.quote(SITEMAP, safe="")
    su = urllib.parse.quote(site_url, safe="")
    st, _ = api("PUT", f"https://www.googleapis.com/webmasters/v3/sites/{su}/sitemaps/{feed}", tok)
    print(f"\nSubmit sitemap {SITEMAP}: HTTP {st} "
          f"({'OK' if st in (200, 204) else 'FALHOU'})")

    # --- Inspecionar status de indexacao das paginas ---
    print("\nStatus de indexacao (URL Inspection API):")
    for page in PAGES:
        st, res = api("POST",
                      "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect",
                      tok, {"inspectionUrl": page, "siteUrl": site_url})
        if st != 200:
            print(f"  {page}: HTTP {st} {res.get('error','')[:200]}")
            continue
        idx = res.get("inspectionResult", {}).get("indexStatusResult", {})
        print(f"  {page}")
        print(f"      veredito: {idx.get('verdict')} | cobertura: {idx.get('coverageState')}")
        print(f"      ultimo crawl: {idx.get('lastCrawlTime')} | google canonico: {idx.get('googleCanonical')}")


if __name__ == "__main__":
    main()
