"""Cria draft no Zenodo com PDF + metadata. NAO publica (user revisa UI).

Uso:
  export ZENODO_TOKEN=...
  python zenodo_create_draft.py <pdf_path> <metadata_json>
"""
import json
import os
import sys
import pathlib
import requests

BASE = os.environ.get("ZENODO_BASE", "https://zenodo.org/api")
TOKEN = os.environ["ZENODO_TOKEN"]
H = {"Authorization": f"Bearer {TOKEN}"}


def main(pdf_path: str, meta_path: str) -> None:
    pdf = pathlib.Path(pdf_path)
    assert pdf.exists(), f"PDF nao encontrado: {pdf}"
    metadata = json.loads(pathlib.Path(meta_path).read_text(encoding="utf-8"))

    # 1) cria deposit vazio
    r = requests.post(f"{BASE}/deposit/depositions", headers=H, json={}, timeout=30)
    r.raise_for_status()
    dep = r.json()
    dep_id = dep["id"]
    bucket = dep["links"]["bucket"]
    print(f"[OK] deposit criado id={dep_id}")

    # 2) upload PDF via bucket API (suporta arquivos grandes)
    with pdf.open("rb") as fh:
        r = requests.put(
            f"{bucket}/{pdf.name}",
            headers={**H, "Content-Type": "application/octet-stream"},
            data=fh,
            timeout=600,
        )
    r.raise_for_status()
    print(f"[OK] upload {pdf.name} ({pdf.stat().st_size/1024:.1f} KB)")

    # 3) grava metadata
    r = requests.put(
        f"{BASE}/deposit/depositions/{dep_id}",
        headers={**H, "Content-Type": "application/json"},
        json={"metadata": metadata},
        timeout=30,
    )
    r.raise_for_status()
    record_url = r.json()["links"]["html"]

    print(f"[OK] metadata gravada")
    print(f"\nDRAFT pronto (NAO publicado):")
    print(f"  deposit_id : {dep_id}")
    print(f"  revisar em : {record_url}")
    print(f"\nPara publicar apos revisao na UI, clique 'Publish' OU rode:")
    print(f"  curl -X POST {BASE}/deposit/depositions/{dep_id}/actions/publish \\")
    print(f"    -H 'Authorization: Bearer $ZENODO_TOKEN'")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("uso: python zenodo_create_draft.py <pdf> <metadata.json>")
    main(sys.argv[1], sys.argv[2])
