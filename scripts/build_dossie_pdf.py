"""Monta o dossiê BRGEO-1 em PDF a partir dos arquivos versionados do repo.

Junta DOSSIE_REUNIAO.md (contexto, health-check, decisões, guia de publicação,
ressalvas, pauta) com o MANUSCRIPT.md inteiro na Parte 4, e converte via Chrome
headless. Gerar a partir dos arquivos, em vez de manter uma cópia separada,
evita que o PDF da reunião divirja do que está no repositório.

USO
    python scripts/build_dossie_pdf.py
    python scripts/build_dossie_pdf.py --out "C:/Users/alexa/Desktop/dossie.pdf"
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

import markdown

RAIZ = Path(__file__).resolve().parents[1]
BASE = RAIZ / "docs" / "research" / "methods-paper"
EXTENSOES = ["tables", "attr_list", "fenced_code", "toc", "sane_lists"]

CHROMES = [
    r"C:/Program Files/Google/Chrome/Application/chrome.exe",
    r"C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
    r"C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
]

CSS = """
@page { size: A4; margin: 20mm 17mm 18mm 17mm; }
/* a capa e uma pagina inteira sangrada: sem margem de pagina nela */
@page:first { margin: 0; }

:root{
  --ink:#15181E; --ink-2:#3A4250; --muted:#5C6573;
  --line:#D8DCE4; --line-2:#B9C0CC;
  --accent:#0F4B57; --accent-soft:#EAF3F5;
  --crit:#8F2C19; --crit-soft:#FAEAE6;
  --ok:#1F5740;
}
*{box-sizing:border-box}
body{
  font-family:"Source Serif 4","Georgia","Times New Roman",serif;
  font-size:10.2pt; line-height:1.55; color:#15181E; margin:0;
  -webkit-print-color-adjust:exact; print-color-adjust:exact;
}
h1,h2,h3,h4,.ui{font-family:"Archivo","Helvetica Neue",Arial,sans-serif}
code,pre,.mono{font-family:"JetBrains Mono","Consolas",monospace}

/* capa */
.capa{
  height:297mm; width:210mm; display:flex; flex-direction:column;
  justify-content:center; page-break-after:always;
  background:#0F4B57; color:#FFFFFF; padding:26mm 24mm;
}
/* h1 global e azul-petroleo; dentro da capa isso seria tinta sobre a mesma
   tinta. Cor propria, explicita, e sem quebra de pagina antes. */
.capa h1, .capa .sub, .capa dd, .capa dt, .capa .tag, .capa .rodape{color:#FFFFFF}
.capa h1{page-break-before:auto; border-bottom:none; padding-bottom:0}
.capa .tag{
  font-family:"Archivo",sans-serif; font-size:9pt; font-weight:600;
  letter-spacing:.18em; text-transform:uppercase; opacity:.72; margin-bottom:14mm;
}
.capa h1{
  font-size:44pt; font-weight:700; line-height:1.05; letter-spacing:-.025em;
  margin:0 0 7mm; max-width:15em;
}
.capa .sub{font-size:13.5pt; opacity:.92; margin:0 0 16mm; max-width:26em; line-height:1.4}
.capa dl{display:grid; grid-template-columns:auto 1fr; gap:2.5mm 8mm; margin:0; font-size:9.5pt}
.capa dt{
  opacity:.62;
  font-family:"Archivo",sans-serif; font-size:8pt; font-weight:600;
  letter-spacing:.1em; text-transform:uppercase; padding-top:.4mm;
}
.capa dd{margin:0}
.capa .rodape{margin-top:auto; padding-top:14mm; font-size:8.5pt; opacity:.66}

/* estrutura */
h1{
  font-size:19pt; font-weight:700; letter-spacing:-.015em; line-height:1.15;
  color:#0F4B57; margin:0 0 5mm; padding-bottom:3mm; border-bottom:2px solid #0F4B57;
  page-break-before:always; page-break-after:avoid;
}
h1:first-of-type{page-break-before:auto}
h2{
  font-size:13pt; font-weight:600; letter-spacing:-.01em; line-height:1.25;
  margin:9mm 0 3mm; color:#15181E; page-break-after:avoid;
}
h3{
  font-size:10.8pt; font-weight:600; margin:6mm 0 2mm; color:#2B333F;
  page-break-after:avoid;
}
p{margin:0 0 3.2mm; text-align:justify; hyphens:auto}
strong{font-weight:600}
em{font-style:italic}
ul,ol{margin:0 0 3.5mm; padding-left:6mm}
li{margin-bottom:1.4mm}
blockquote{
  margin:4mm 0; padding:3mm 5mm; border-left:2.5pt solid #0F4B57;
  background:#EAF3F5; font-style:normal; color:#2B333F;
}
blockquote p{margin:0 0 2mm} blockquote p:last-child{margin:0}

code{
  font-size:8.6pt; background:#F1F3F6; border:.5pt solid #D8DCE4;
  border-radius:2pt; padding:.3mm 1mm; color:#2B333F;
}
pre{
  background:#F5F6F9; border:.5pt solid #D8DCE4; border-radius:3pt;
  padding:3mm 4mm; overflow-x:auto; page-break-inside:avoid; margin:3.5mm 0;
}
pre code{background:none; border:none; padding:0; font-size:8.2pt; line-height:1.45}

table{
  border-collapse:collapse; width:100%; margin:4mm 0; font-size:8.8pt;
  page-break-inside:avoid;
}
th,td{border-bottom:.5pt solid #D8DCE4; padding:1.7mm 2.5mm; text-align:left; vertical-align:top}
thead th{
  font-family:"Archivo",sans-serif; font-size:7.6pt; font-weight:600;
  letter-spacing:.06em; text-transform:uppercase; color:#5C6573;
  background:#F1F3F6; border-bottom:1pt solid #B9C0CC;
}
tbody tr:last-child td{border-bottom:.5pt solid #B9C0CC}
td:nth-child(n+2){font-variant-numeric:tabular-nums}

hr{border:none; border-top:.5pt solid #D8DCE4; margin:8mm 0}
a{color:#0F4B57; text-decoration:none; border-bottom:.4pt solid #A9C3C9}

/* sumario */
.toc{
  background:#F5F6F9; border:.5pt solid #D8DCE4; border-radius:3pt;
  padding:6mm 8mm; margin-bottom:6mm; page-break-after:always;
}
.toc h2{margin-top:0; font-size:12pt; color:#0F4B57}
.toc ul{list-style:none; padding-left:0; margin:0}
.toc > ul > li{
  font-family:"Archivo",sans-serif; font-weight:600; font-size:10pt;
  margin:3.5mm 0 1.5mm; color:#15181E;
}
.toc ul ul{padding-left:5mm; margin-top:1mm}
.toc ul ul li{
  font-family:"Source Serif 4",serif; font-weight:400; font-size:9.2pt;
  color:#3A4250; margin-bottom:.9mm;
}
.toc a{border:none; color:inherit}

/* separador do manuscrito */
.divisor{
  page-break-before:always; background:#EAF3F5; border:.5pt solid #A9C3C9;
  border-radius:3pt; padding:8mm 9mm; margin-bottom:7mm;
}
.divisor .tag{
  font-family:"Archivo",sans-serif; font-size:8pt; font-weight:600;
  letter-spacing:.14em; text-transform:uppercase; color:#0F4B57; margin-bottom:3mm;
}
.divisor h1{
  page-break-before:auto; border:none; padding:0; margin:0 0 3mm; font-size:17pt;
}
.divisor p{margin:0; font-size:9.6pt; color:#2B333F; text-align:left}
.divisor .en{
  margin-top:4mm; padding-top:3mm; border-top:.5pt solid #A9C3C9;
  font-size:8.8pt; color:#5C6573;
}
.manuscrito h1{font-size:16pt}
.manuscrito h2{font-size:11.6pt; color:#0F4B57}
"""


def md_para_html(caminho: Path) -> str:
    texto = caminho.read_text(encoding="utf-8")
    return markdown.markdown(texto, extensions=EXTENSOES)


def montar_html(hoje: str) -> str:
    dossie = md_para_html(BASE / "DOSSIE_REUNIAO.md")
    manuscrito = md_para_html(BASE / "MANUSCRIPT.md")

    # o primeiro <hr/> e o bloco de metadados da capa saem do corpo:
    # a capa dedicada já os apresenta.
    dossie = re.sub(r"^.*?<hr\s*/?>", "", dossie, count=1, flags=re.S)

    capa = f"""
<div class="capa">
  <div class="tag">Dossiê para reunião interna · {hoje}</div>
  <h1>BRGEO-1</h1>
  <p class="sub">Protocolo aberto de medição de citação em motores generativos.
  Health-check da coleta, decisões de posicionamento, manuscrito completo e
  guia de publicação.</p>
  <dl>
    <dt>Autor</dt><dd>Alexandre Caramaschi · ORCID 0009-0004-9150-485X</dd>
    <dt>Custódia</dt><dd>Brasil GEO</dd>
    <dt>Repositório</dt><dd>github.com/alexandrebrt14-sys/papers</dd>
    <dt>Alvo</dt><dd>SSRN (Elsevier) · Information Systems &amp; eBusiness Network</dd>
    <dt>Janela</dt><dd>confirmatória, fecha em 28/09/2026</dd>
    <dt>Estado</dt><dd>working paper · não submetido</dd>
  </dl>
  <div class="rodape">Documento de trabalho. Números descritivos são preliminares:
  a janela confirmatória ainda não fechou.</div>
</div>

<div class="toc">
  <h2>Conteúdo</h2>
  <ul>
    <li>Parte 1 — O pedido e o contexto
      <ul><li>O que foi pedido</li><li>O estado em que a coleta foi encontrada</li>
      <li>O que foi feito nesta sessão</li></ul></li>
    <li>Parte 2 — Health-check da coleta
      <ul><li>Por que a série parou</li>
      <li>O achado central: a extração nunca leu a resposta do modelo</li>
      <li>Os outros três achados</li></ul></li>
    <li>Parte 3 — As decisões de posicionamento
      <ul><li>Nome e atribuição</li><li>Saída: especificação com índice derivado</li>
      <li>Alcance</li><li>O achado que muda o discurso comercial</li></ul></li>
    <li>Parte 4 — O manuscrito completo <span class="mono">(em inglês)</span>
      <ul><li>BRGEO-1: An Open Protocol for Measuring Entity Citation
      in Generative Engines</li></ul></li>
    <li>Parte 5 — Guia de publicação no SSRN
      <ul><li>O que o SSRN é e o que não é</li><li>Passo a passo</li>
      <li>Depois da publicação</li><li>A rota até o Q1</li></ul></li>
    <li>Parte 6 — Ressalvas, boas práticas e pontos de alerta
      <ul><li>Pontos de alerta antes de submeter</li>
      <li>Ressalvas científicas declaradas</li>
      <li>Boas práticas que o repositório impõe</li>
      <li>Alerta operacional em aberto</li></ul></li>
    <li>Parte 7 — Pauta sugerida para a reunião</li>
    <li>Anexos — Verificação dos números · Cronograma</li>
  </ul>
</div>
"""

    divisor = """
<div class="divisor">
  <div class="tag">Parte 4 — O manuscrito</div>
  <h1>O paper, na íntegra</h1>
  <p>Versão 1.0, como seria submetida ao SSRN. É o texto que a Parte 5 explica
  como publicar e que a Parte 6 lista as ressalvas.</p>
  <p class="en">O manuscrito está em inglês acadêmico, padrão dos papers da
  linha e requisito prático da rede-alvo no SSRN. O restante deste dossiê está
  em português.</p>
</div>
"""

    # O manuscrito e a Parte 4 e precisa cair ENTRE a Parte 3 e a Parte 5, na
    # ordem que o sumario anuncia. O DOSSIE_REUNIAO.md salta de 3 para 5
    # justamente para abrir esse buraco; aqui ele e preenchido. Anexar no fim
    # deixaria o manuscrito depois dos anexos.
    marcador = re.search(r"<h1[^>]*>Parte 5\s", dossie)
    if not marcador:
        raise SystemExit(
            "nao achei o cabecalho da Parte 5 em DOSSIE_REUNIAO.md — o "
            "manuscrito nao tem onde ser inserido. Conferir se o titulo mudou."
        )
    corte = marcador.start()
    antes_da_parte5, dali_em_diante = dossie[:corte], dossie[corte:]

    return f"""<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="utf-8">
<title>Dossiê BRGEO-1</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&family=JetBrains+Mono:wght@400;500&display=swap">
<style>{CSS}</style>
</head><body>
{capa}
{antes_da_parte5}
{divisor}
<div class="manuscrito">{manuscrito}</div>
{dali_em_diante}
</body></html>"""


def achar_chrome() -> str | None:
    for c in CHROMES:
        if Path(c).exists():
            return c
    return shutil.which("chrome") or shutil.which("msedge")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    padrao = (Path(os.path.expanduser("~")) / "Desktop" /
              f"BRGEO-1-dossie-reuniao-{date.today():%Y-%m-%d}.pdf")
    ap.add_argument("--out", default=str(padrao))
    a = ap.parse_args()

    hoje = date.today().strftime("%d/%m/%Y")
    html = montar_html(hoje)

    tmp = Path(tempfile.mkdtemp()) / "dossie.html"
    tmp.write_text(html, encoding="utf-8")
    print(f"  html   {tmp}  ({len(html):,} bytes)".replace(",", "."))

    chrome = achar_chrome()
    if not chrome:
        print("Chrome/Edge não encontrado; o HTML acima pode ser impresso à mão.",
              file=sys.stderr)
        return 1

    saida = Path(a.out)
    saida.parent.mkdir(parents=True, exist_ok=True)
    perfil = Path(tempfile.mkdtemp()) / "perfil"

    cmd = [
        chrome, "--headless", "--disable-gpu", "--no-sandbox",
        f"--user-data-dir={perfil}",
        "--no-pdf-header-footer",
        "--virtual-time-budget=20000",
        f"--print-to-pdf={saida}",
        tmp.as_uri(),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    if not saida.exists():
        print("falha ao gerar o PDF", file=sys.stderr)
        print(r.stderr[-1500:], file=sys.stderr)
        return 1

    print(f"  pdf    {saida}  ({saida.stat().st_size/1_048_576:.2f} MB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
