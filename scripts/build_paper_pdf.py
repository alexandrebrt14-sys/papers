"""Gera o PDF do paper BRGEO-1 em formato acadêmico, pronto para compartilhar.

Diferente de `build_dossie_pdf.py`, que monta o dossiê interno em português,
este script produz apenas o manuscrito em inglês, com página de rosto, abstract
destacado, seções numeradas, tabelas com legenda e referências — o arquivo que
vai para o SSRN e para quem for ler o paper sem o contexto da reunião.

USO
    python scripts/build_paper_pdf.py
    python scripts/build_paper_pdf.py --out "C:/caminho/BRGEO-1.pdf"
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import markdown

RAIZ = Path(__file__).resolve().parents[1]
FONTE = RAIZ / "docs" / "research" / "methods-paper" / "MANUSCRIPT.md"
EXTENSOES = ["tables", "attr_list", "fenced_code", "sane_lists", "footnotes"]

CHROMES = [
    r"C:/Program Files/Google/Chrome/Application/chrome.exe",
    r"C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
    r"C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
]

CSS = """
@page{ size:A4; margin:24mm 22mm 22mm 22mm; }
@page:first{ margin:0; }

*{box-sizing:border-box}
body{
  font-family:"Source Serif 4",Georgia,"Times New Roman",serif;
  font-size:10.4pt; line-height:1.5; color:#111418; margin:0;
  -webkit-print-color-adjust:exact; print-color-adjust:exact;
}
h1,h2,h3,h4,.ui{font-family:"Archivo","Helvetica Neue",Arial,sans-serif}
code,pre{font-family:"JetBrains Mono",Consolas,monospace}

/* ── página de rosto ─────────────────────────────────── */
.rosto{
  height:297mm; width:210mm; padding:38mm 30mm 24mm;
  display:flex; flex-direction:column; page-break-after:always;
}
.rosto .selo{
  font-family:"Archivo",sans-serif; font-size:8.5pt; font-weight:600;
  letter-spacing:.16em; text-transform:uppercase; color:#0F4B57;
  padding-bottom:5mm; border-bottom:1.5pt solid #0F4B57; margin-bottom:14mm;
}
.rosto h1{
  font-size:25pt; font-weight:700; line-height:1.16; letter-spacing:-.018em;
  color:#111418; margin:0 0 12mm; max-width:22em;
}
.rosto .autor{font-size:13pt; font-weight:600; margin:0 0 1.5mm; color:#111418}
.rosto .afil{font-size:10pt; color:#3C4450; margin:0 0 1mm; line-height:1.45}
.rosto .meta{
  margin-top:12mm; padding-top:7mm; border-top:.5pt solid #C9CFD9;
  font-size:9.5pt; color:#3C4450; line-height:1.7;
}
.rosto .meta b{font-family:"Archivo",sans-serif; font-size:8pt; font-weight:600;
  letter-spacing:.09em; text-transform:uppercase; color:#6B7480;
  display:inline-block; min-width:34mm;}
.rosto .aviso{
  margin-top:auto; padding:5mm 6mm; background:#F4F6F8;
  border-left:2.5pt solid #0F4B57; font-size:9pt; color:#3C4450; line-height:1.5;
}

/* ── abstract ────────────────────────────────────────── */
.abstract{
  background:#F4F6F8; border:.5pt solid #D5DAE2; border-radius:2pt;
  padding:7mm 9mm; margin:0 0 8mm;
}
.abstract h2{
  font-size:9pt; font-weight:600; letter-spacing:.14em; text-transform:uppercase;
  color:#0F4B57; margin:0 0 3.5mm; border:none; padding:0;
}
.abstract p{font-size:9.8pt; text-align:justify; margin:0 0 3mm}
.abstract p:last-child{margin:0}
.chaves{
  margin:0 0 9mm; font-size:9.4pt; color:#3C4450; line-height:1.6;
}
.chaves b{font-family:"Archivo",sans-serif; font-size:8.4pt; font-weight:600;
  letter-spacing:.07em; text-transform:uppercase; color:#6B7480;}

/* ── corpo ───────────────────────────────────────────── */
h2{
  font-size:12.5pt; font-weight:600; letter-spacing:-.008em; line-height:1.3;
  color:#0F4B57; margin:9mm 0 3mm; padding-bottom:1.6mm;
  border-bottom:.5pt solid #C9CFD9; page-break-after:avoid;
}
h3{font-size:10.6pt; font-weight:600; margin:6mm 0 2mm; color:#222A35;
   page-break-after:avoid;}
h4{font-size:10pt; font-weight:600; margin:4.5mm 0 1.5mm; color:#3C4450;
   page-break-after:avoid;}
p{margin:0 0 3.2mm; text-align:justify; hyphens:auto}
ul,ol{margin:0 0 3.5mm; padding-left:6mm}
li{margin-bottom:1.5mm; text-align:justify}
strong{font-weight:600}
blockquote{
  margin:4mm 0; padding:0 0 0 6mm; border-left:2pt solid #0F4B57;
  font-style:normal; color:#222A35;
}
blockquote p{margin:0; font-size:11pt; text-align:left}

code{
  font-size:8.8pt; background:#F1F3F6; border-radius:2pt;
  padding:.2mm 1mm; color:#222A35;
}
pre{background:#F4F6F8; border:.5pt solid #D5DAE2; border-radius:2pt;
    padding:3mm 4mm; margin:3.5mm 0; page-break-inside:avoid;}
pre code{background:none; padding:0; font-size:8.4pt; line-height:1.45}

/* equação em bloco */
.eq{
  margin:4.5mm 0; padding:3.5mm 5mm; background:#F4F6F8;
  border:.5pt solid #D5DAE2; border-radius:2pt; text-align:center;
  font-size:11.5pt; page-break-inside:avoid;
}

/* ── tabelas ─────────────────────────────────────────── */
table{
  border-collapse:collapse; width:100%; margin:2mm 0 5mm; font-size:8.9pt;
  page-break-inside:avoid;
}
th,td{padding:1.7mm 2.6mm; text-align:left; vertical-align:top}
thead th{
  font-family:"Archivo",sans-serif; font-size:7.7pt; font-weight:600;
  letter-spacing:.05em; text-transform:uppercase; color:#3C4450;
  border-top:1pt solid #111418; border-bottom:.5pt solid #6B7480;
}
tbody td{border-bottom:.4pt solid #E2E6EC}
tbody tr:last-child td{border-bottom:1pt solid #111418}
td:nth-child(n+2){font-variant-numeric:tabular-nums}
caption.legenda{
  caption-side:top; text-align:left;
  font-size:9pt; color:#111418; line-height:1.45;
  padding:0 0 1.8mm; margin:0;
}
.legenda b{font-family:"Archivo",sans-serif; font-weight:600; color:#111418}

/* ── referências ─────────────────────────────────────── */
.refs ol{padding-left:0; list-style:none; counter-reset:ref}
.refs li{
  position:relative; padding-left:9mm; margin-bottom:2.4mm;
  font-size:9.2pt; line-height:1.45; text-align:left;
}
.refs li::before{
  counter-increment:ref; content:"[" counter(ref) "]";
  position:absolute; left:0; font-family:"JetBrains Mono",monospace;
  font-size:8.4pt; color:#0F4B57;
}

hr{border:none; border-top:.5pt solid #D5DAE2; margin:7mm 0}
a{color:#0F4B57; text-decoration:none}
.rodape-doc{
  margin-top:9mm; padding-top:4mm; border-top:.5pt solid #D5DAE2;
  font-size:8.4pt; color:#6B7480; text-align:center;
}
"""


def promover_legendas(html: str) -> str:
    """Move a legenda para dentro da propria tabela, como <caption>.

    O markdown transforma "**Table 4.** ..." num <p> comum, e o motor de
    impressao o trata como paragrafo qualquer: a legenda fica no pe de uma
    pagina e a tabela comeca na seguinte. Emparelhar por posicao com um par
    de expressoes regulares e fragil — foi o que dessincronizou legenda e
    tabela na primeira tentativa. Como <caption> e filho de <table>, a
    separacao passa a ser impossivel por construcao, sem depender de
    page-break.

    So promove a legenda quando ela e imediatamente seguida por uma tabela;
    uma legenda solta permanece paragrafo, em vez de ser silenciosamente
    anexada a tabela errada.
    """
    padrao = re.compile(
        r"<p>(<strong>Table \d+\.</strong>.*?)</p>\s*(<table>)",
        re.S,
    )

    def troca(m: re.Match) -> str:
        return f'{m.group(2)}<caption class="legenda">{m.group(1)}</caption>'

    html, n = padrao.subn(troca, html)
    esperadas = len(re.findall(r"<strong>Table \d+\.</strong>", html))
    if n != esperadas:
        raise SystemExit(
            f"legendas promovidas: {n}, encontradas: {esperadas}. Alguma "
            "legenda nao esta seguida de tabela — conferir o manuscrito antes "
            "de gerar o PDF."
        )
    return html


def desktop() -> Path:
    """Área de trabalho real; com OneDrive ligado ela não é ~/Desktop."""
    if os.name == "nt":
        try:
            import winreg
            chave = (r"Software\Microsoft\Windows\CurrentVersion"
                     r"\Explorer\User Shell Folders")
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, chave) as k:
                bruto, _ = winreg.QueryValueEx(k, "Desktop")
            caminho = Path(os.path.expandvars(bruto))
            if caminho.is_dir():
                return caminho
        except OSError:
            pass
    return Path(os.path.expanduser("~")) / "Desktop"


def achar_chrome() -> str | None:
    for c in CHROMES:
        if Path(c).exists():
            return c
    return shutil.which("chrome") or shutil.which("msedge")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default=str(desktop() / "BRGEO-1-protocol-paper.pdf"))
    ap.add_argument("--src", default=str(FONTE))
    a = ap.parse_args()

    fonte = Path(a.src)
    if not fonte.exists():
        print(f"manuscrito nao encontrado: {fonte}", file=sys.stderr)
        return 1

    corpo = markdown.markdown(fonte.read_text(encoding="utf-8"),
                              extensions=EXTENSOES)

    corpo = promover_legendas(corpo)
    html = MOLDE.replace("<!--CORPO-->", corpo).replace("<!--CSS-->", CSS)

    tmp = Path(tempfile.mkdtemp()) / "paper.html"
    tmp.write_text(html, encoding="utf-8")

    chrome = achar_chrome()
    if not chrome:
        print("Chrome/Edge nao encontrado.", file=sys.stderr)
        return 1

    saida = Path(a.out)
    saida.parent.mkdir(parents=True, exist_ok=True)
    perfil = Path(tempfile.mkdtemp()) / "perfil"
    subprocess.run([
        chrome, "--headless", "--disable-gpu", "--no-sandbox",
        f"--user-data-dir={perfil}", "--no-pdf-header-footer",
        "--virtual-time-budget=20000", f"--print-to-pdf={saida}",
        tmp.as_uri(),
    ], capture_output=True, text=True, timeout=300)

    if not saida.exists():
        print("falha ao gerar o PDF", file=sys.stderr)
        return 1
    print(f"  pdf    {saida}  ({saida.stat().st_size/1_048_576:.2f} MB)")
    return 0


MOLDE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>BRGEO-1 Protocol</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400;1,8..60,600&family=JetBrains+Mono:wght@400;500&display=swap">
<style><!--CSS--></style>
</head><body>
<!--CORPO-->
</body></html>"""


if __name__ == "__main__":
    raise SystemExit(main())
