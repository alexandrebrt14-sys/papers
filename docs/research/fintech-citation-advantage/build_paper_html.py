# -*- coding: utf-8 -*-
"""Integra as 5 secoes do manuscrito em paper_final.html (A4, print-ready)."""
import io, re
import markdown

DIR = r"C:/Sandyboxclaude/papers/docs/research/fintech-citation-advantage"
SECTIONS = [
    "paper_sec_A_intro.md",
    "paper_sec_B_methods.md",
    "paper_sec_C_results.md",
    "paper_sec_D_theory.md",
    "paper_sec_E_discussion.md",
]

CSS = """
@page { size: A4; margin: 2.2cm; }
body { font-family: Georgia, 'Times New Roman', serif; font-size: 11pt;
       line-height: 1.55; color: #111; background: #fff;
       max-width: 17cm; margin: 0 auto; padding: 1em; }
p { text-align: justify; margin: 0.55em 0; }
h1 { font-size: 21pt; line-height: 1.25; text-align: left; margin: 0.2em 0 0.4em; }
h2 { font-size: 14pt; margin: 1.5em 0 0.5em; border-bottom: 1px solid #999; padding-bottom: 2px; }
h3 { font-size: 12pt; margin: 1.2em 0 0.4em; }
h4 { font-size: 11pt; margin: 1em 0 0.3em; font-style: italic; }
.authorblock { margin: 0.8em 0 1.2em; font-size: 11pt; }
.authorblock .name { font-size: 13pt; font-weight: bold; }
.authorblock a { color: #0a4d8c; text-decoration: none; }
.dateline { font-size: 10pt; color: #333; margin-bottom: 0.3em; }
.companion { font-size: 9.5pt; color: #333; margin-bottom: 1.2em; }
.abstractbox { background: #f5f5f3; border: 1px solid #bbb; padding: 0.9em 1.1em;
               margin: 1em 0; font-size: 10.5pt; }
.abstractbox p { text-align: justify; }
.abstractbox .ablabel { font-weight: bold; font-variant: small-caps; }
table { border-collapse: collapse; margin: 1em auto; font-size: 9.5pt; width: 100%;
        page-break-inside: avoid; }
th { border-top: 1.5pt solid #111; border-bottom: 0.75pt solid #111; padding: 4px 7px;
     text-align: left; }
td { padding: 3px 7px; }
tr:last-child td { border-bottom: 1.5pt solid #111; }
.figbox { border: 1px dashed #777; background: #fafaf8; padding: 0.8em 1em; margin: 1em 0;
          font-size: 9.5pt; color: #222; page-break-inside: avoid; }
.figbox .figlabel { font-weight: bold; }
figure.paperfig { margin: 1.2em 0; text-align: center; page-break-inside: avoid; }
figure.paperfig img { max-width: 100%; height: auto; }
figure.paperfig figcaption { font-size: 9pt; text-align: justify; margin-top: 0.4em;
                             color: #222; padding: 0 0.5em; }
.missing { background: #fff3a8; padding: 0 3px; font-size: 9.5pt; }
.refs p, .refs li { text-align: left; font-size: 10pt; padding-left: 2em; text-indent: -2em;
                    margin: 0.35em 0; }
code { font-family: Consolas, monospace; font-size: 9.5pt; background: #f2f2f0; padding: 0 2px; }
blockquote { margin: 0.8em 1.5em; font-size: 10.5pt; color: #222; }
hr { border: none; border-top: 1px solid #aaa; margin: 1.6em 0; }
strong { font-weight: bold; }
"""

def load(fn):
    return io.open(f"{DIR}/{fn}", encoding="utf-8").read()

parts = []
for fn in SECTIONS:
    t = load(fn)
    # remove a lista de referencias parcial da secao A (compilador usa a consolidada do E)
    if fn == "paper_sec_A_intro.md":
        t = re.split(r"\n#+\s*References cited.*", t, flags=re.I)[0]
        t = re.split(r"\n#+\s*Cited references.*", t, flags=re.I)[0]
        t = re.split(r"\n#+\s*Reference list for the compiler.*", t, flags=re.I)[0]
    parts.append(t)

raw = "\n\n---\n\n".join(parts)

# figuras reais embutidas em base64 com captions
import base64
CAPTIONS = {
    1: "Weekly spontaneous citation rate by vertical (W16-W23, analytic core). The ordering is stable, but stability of the aggregate masks the anchor dynamics shown in Figure 7.",
    2: "Baseline citation rates (filled markers) versus rates after removing each vertical's top-k anchor entities (open markers). Every vertical is anchor-driven; fintech is the extreme k=1 case.",
    3: "Decomposition of the aggregate fintech-retail gap into excess cited responses per engine. The advantage concentrates in Claude (+574) and the truncation-contaminated Gemini (+134); the other three engines run the opposite way.",
    4: "Mention concentration (HHI) versus citation rate across the four verticals: concentration tracks rate, consistent with a cumulative-advantage account.",
    5: "Citation rate (%) by vertical and engine. The vertical ordering is engine-dependent; Perplexity (RAG) saturates near the ceiling while Gemini sits near the floor.",
    6: "Share of citations whose first entity mention appears beyond 200 characters, measured on the untruncated Perplexity cohort: truncation penalizes technology and healthcare far more than fintech and retail.",
    7: "Nubank's share of fintech mentions and the sole-Nubank fraction of cited responses by week: the anchor intensifies within the window (41.9% to 56.9%).",
}

def fig_html(n):
    try:
        b64 = base64.b64encode(open(f"{DIR}/fig{n}.png", "rb").read()).decode()
        return (f'<figure class="paperfig"><img src="data:image/png;base64,{b64}" '
                f'alt="Figure {n}"><figcaption><strong>Figure {n}.</strong> '
                f'{CAPTIONS[n]}</figcaption></figure>')
    except FileNotFoundError:
        return f'<div class="figbox"><span class="figlabel">Figure {n}.</span> {CAPTIONS[n]}</div>'

# remove o caption inline que seguia o callout (a legenda agora vem do CAPTIONS)
raw = re.sub(r"\[FIGURE\s+(\d+)\s+HERE[^\]]*\]",
             lambda m: "\n\n" + fig_html(int(m.group(1))) + "\n\n", raw)

raw = re.sub(
    r"\[MISSING EVIDENCE:\s*([^\]]+)\]",
    r'<span class="missing">[MISSING EVIDENCE: \1]</span>',
    raw,
)

html_body = markdown.markdown(raw, extensions=["tables", "smarty"])

# abstract box: envolve o bloco entre o heading Abstract e Keywords
html_body = re.sub(
    r"(<h2>Abstract</h2>)(.*?)(<p><strong>Keywords)",
    r'<div class="abstractbox"><p class="ablabel">Abstract</p>\2</div>\3',
    html_body, flags=re.S, count=1,
)
html_body = re.sub(
    r"(<h3>Abstract</h3>)(.*?)(<p><strong>Keywords)",
    r'<div class="abstractbox"><p class="ablabel">Abstract</p>\2</div>\3',
    html_body, flags=re.S, count=1,
)
# referencias com hanging indent
html_body = re.sub(r"<h2>References</h2>", '<h2>References</h2><div class="refs">', html_body, count=1)
if '<div class="refs">' in html_body:
    # fecha refs antes do proximo h2 apos References (Appendix) ou no fim
    idx = html_body.index('<div class="refs">')
    rest = html_body[idx:]
    m = re.search(r"<h2>(?!References)", rest[20:])
    if m:
        pos = idx + 20 + m.start()
        html_body = html_body[:pos] + "</div>" + html_body[pos:]
    else:
        html_body += "</div>"

doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>The Anchor-Entity Effect — Caramaschi (2026)</title>
<style>{CSS}</style>
</head>
<body>
{html_body}
</body>
</html>"""

io.open(f"{DIR}/paper_final.html", "w", encoding="utf-8").write(doc)
print("OK paper_final.html | chars:", len(doc), "| palavras:", len(re.sub(r'<[^>]+>', ' ', html_body).split()))
