# -*- coding: utf-8 -*-
"""Gera a pagina do paper para brasilgeo.ai (worker assets)."""
import io, os, re, shutil

SRC = r"C:/Sandyboxclaude/papers/docs/research/fintech-citation-advantage"
DST = r"C:/Sandyboxclaude/brasilgeo-worker/site/pesquisa"
os.makedirs(DST, exist_ok=True)

body = io.open(f"{SRC}/paper_body_web.html", encoding="utf-8").read()
body = body.replace('src="/papers/anchor-entity-effect/', 'src="/pesquisa/')

for i in range(1, 8):
    shutil.copyfile(f"{SRC}/fig{i}.png", f"{DST}/fig{i}.png")
shutil.copyfile(
    r"C:/Users/alexa/OneDrive/Área de Trabalho/Caramaschi_2026_Anchor_Entity_Effect_LLM_Brand_Citations.pdf",
    f"{DST}/Caramaschi_2026_Anchor_Entity_Effect.pdf",
)

ABSTRACT = ("We report a complete 48-day audit (April 23 - June 9, 2026) of spontaneous brand citation "
            "across five economy-tier LLMs for four Brazilian verticals (62,820 observations). Fintech leads "
            "at 28.15%, but the advantage is dominated by a single anchor entity: Nubank accounts for 49.7% "
            "of fintech mentions, and a leave-one-out recoding drops fintech to 11.46% (last place), inverting "
            "its adjusted odds ratio from 4.13 to 0.77. Every vertical is anchor-driven; the effect is "
            "engine-heterogeneous; the anchor's share grows from 41% to 57% within the window.")

page = f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large" />
  <meta name="theme-color" content="#0F2543" />
  <title>The Anchor-Entity Effect — Working Paper · Pesquisa Brasil GEO</title>
  <meta name="description" content="Working paper completo: por que a vertical fintech obtém mais citações espontâneas de LLMs. Auditoria de 62.820 observações (23 abr - 9 jun 2026, 5 LLMs, 4 verticais) mostra que a vantagem setorial aparente é o efeito de uma entidade-âncora: o Nubank concentra 49,7% das menções e, removido, a fintech cai de 28,15% para 11,46%." />
  <link rel="canonical" href="https://brasilgeo.ai/pesquisa/anchor-entity-effect" />
  <meta property="og:type" content="article" />
  <meta property="og:title" content="The Anchor-Entity Effect — Working Paper" />
  <meta property="og:description" content="62.820 observações, 5 LLMs, 4 verticais: a vantagem de citação da fintech é o efeito Nubank. Paper completo com dados abertos." />
  <meta property="og:url" content="https://brasilgeo.ai/pesquisa/anchor-entity-effect" />
  <meta property="og:site_name" content="Brasil GEO" />
  <meta property="og:locale" content="pt_BR" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="citation_title" content="The Anchor-Entity Effect: How Superstar Brands Drive Sectoral Citation Concentration in Large Language Models" />
  <meta name="citation_author" content="Alexandre Caramaschi" />
  <meta name="citation_publication_date" content="2026/06/11" />
  <meta name="citation_pdf_url" content="https://brasilgeo.ai/pesquisa/Caramaschi_2026_Anchor_Entity_Effect.pdf" />
  <meta name="citation_language" content="en" />
  <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Exo:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "ScholarlyArticle",
    "@id": "https://brasilgeo.ai/pesquisa/anchor-entity-effect#article",
    "headline": "The Anchor-Entity Effect: How Superstar Brands Drive Sectoral Citation Concentration in Large Language Models",
    "alternativeHeadline": "A aparente vantagem setorial da fintech em citações de LLMs é o efeito de uma entidade-âncora (Nubank), não da vertical",
    "abstract": "{ABSTRACT}",
    "datePublished": "2026-06-11",
    "inLanguage": "en",
    "isAccessibleForFree": true,
    "license": "https://creativecommons.org/licenses/by/4.0/",
    "url": "https://brasilgeo.ai/pesquisa/anchor-entity-effect",
    "sameAs": ["https://alexandrecaramaschi.com/publicacoes/anchor-entity-effect"],
    "author": {{
      "@type": "Person",
      "name": "Alexandre Caramaschi",
      "jobTitle": "CEO Brasil GEO",
      "url": "https://brasilgeo.ai/fundador",
      "sameAs": ["https://orcid.org/0009-0004-9150-485X"]
    }},
    "publisher": {{
      "@type": "Organization",
      "name": "Brasil GEO",
      "url": "https://brasilgeo.ai",
      "logo": {{"@type": "ImageObject", "url": "https://brasilgeo.ai/favicon.svg"}}
    }},
    "encoding": {{
      "@type": "MediaObject",
      "contentUrl": "https://brasilgeo.ai/pesquisa/Caramaschi_2026_Anchor_Entity_Effect.pdf",
      "encodingFormat": "application/pdf"
    }},
    "isBasedOn": "https://github.com/alexandrebrt14-sys/papers",
    "numberOfPages": 30
  }}
  </script>
  <style>
    :root {{ --navy: #0F2543; --accent: #0a4d8c; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; background: #eef1f5; font-family: Inter, system-ui, sans-serif; color: #111111; }}
    .topbar {{ background: var(--navy); color: #ffffff; padding: 14px 20px; }}
    .topbar .inner {{ max-width: 1020px; margin: 0 auto; display: flex; align-items: center;
                      justify-content: space-between; gap: 12px; flex-wrap: wrap; }}
    .topbar a {{ color: #ffffff; text-decoration: none; }}
    .topbar .brand {{ font-family: Exo, Inter, sans-serif; font-weight: 800; font-size: 1.1rem;
                      letter-spacing: 0.02em; }}
    .topbar .nav a {{ font-size: 0.88rem; font-weight: 600; margin-left: 18px; opacity: 0.95; }}
    .lead-strip {{ max-width: 1020px; margin: 0 auto; padding: 22px 20px 6px; }}
    .lead-strip h1 {{ display: none; }}
    .actions {{ display: flex; gap: 12px; flex-wrap: wrap; margin: 4px 0 16px; }}
    .actions a {{ font-size: 0.9rem; font-weight: 700; text-decoration: none; border-radius: 8px;
                  padding: 10px 18px; }}
    .actions .pdf {{ background: var(--navy); color: #ffffff; }}
    .actions .repo {{ color: var(--navy); border: 1.5px solid var(--navy); }}
    .paper {{ background: #ffffff; color: #111111; max-width: 1020px; margin: 0 auto 48px;
              padding: 48px clamp(20px, 6vw, 76px); border-radius: 12px;
              box-shadow: 0 2px 26px rgba(15, 37, 67, 0.12);
              font-family: Georgia, 'Times New Roman', serif; font-size: 1.02rem; line-height: 1.6; }}
    .paper p {{ text-align: justify; margin: 0.55em 0; color: #111111; }}
    .paper h1 {{ font-family: Georgia, serif; font-size: 1.7rem; line-height: 1.25; color: var(--navy);
                 margin: 0.2em 0 0.5em; }}
    .paper h2 {{ font-size: 1.25rem; color: var(--navy); border-bottom: 1px solid #c5cedd;
                 padding-bottom: 3px; margin: 1.6em 0 0.5em; }}
    .paper h3 {{ font-size: 1.08rem; color: #111111; margin: 1.2em 0 0.4em; }}
    .paper h4 {{ font-size: 1rem; font-style: italic; color: #111111; margin: 1em 0 0.3em; }}
    .paper a {{ color: var(--accent); }}
    .paper table {{ border-collapse: collapse; margin: 1.1em auto; font-size: 0.85rem; width: 100%;
                    display: block; overflow-x: auto; }}
    .paper th {{ border-top: 2px solid #111; border-bottom: 1px solid #111; padding: 5px 9px;
                 text-align: left; color: #111111; }}
    .paper td {{ padding: 4px 9px; color: #111111; }}
    .paper tr:last-child td {{ border-bottom: 2px solid #111; }}
    .paper .abstractbox {{ background: #f5f5f3; border: 1px solid #b9bdc4; padding: 1em 1.2em;
                           margin: 1.1em 0; font-size: 0.95rem; }}
    .paper .abstractbox .ablabel {{ font-weight: 700; font-variant: small-caps; }}
    .paper figure.paperfig {{ margin: 1.4em 0; text-align: center; }}
    .paper figure.paperfig img {{ max-width: 100%; height: auto; border: 1px solid #e3e5e9;
                                  border-radius: 6px; background: #ffffff; }}
    .paper figure.paperfig figcaption {{ font-size: 0.84rem; text-align: justify; margin-top: 0.5em;
                                         color: #333333; padding: 0 0.5em; }}
    .paper .refs p {{ text-align: left; font-size: 0.9rem; padding-left: 2em; text-indent: -2em;
                      margin: 0.4em 0; }}
    .paper code {{ font-family: 'JetBrains Mono', Consolas, monospace; font-size: 0.85rem;
                   background: #f2f2f0; color: #111111; padding: 0 3px; }}
    .paper blockquote {{ margin: 0.9em 1.4em; font-size: 0.95rem; color: #222222;
                         border-left: 3px solid #c5cedd; padding-left: 1em; }}
    .paper hr {{ border: none; border-top: 1px solid #c5cedd; margin: 1.8em 0; }}
    .paper .missing {{ background: #fff3a8; color: #111111; padding: 0 3px; }}
  </style>
</head>
<body>
  <header class="topbar">
    <div class="inner">
      <a class="brand" href="/">BRASIL GEO</a>
      <nav class="nav">
        <a href="/fundador">Fundador</a>
        <a href="/casenubankgeo">Case Nubank</a>
        <a href="/conceitos">Conceitos</a>
      </nav>
    </div>
  </header>
  <div class="lead-strip">
    <h1>The Anchor-Entity Effect — Working Paper</h1>
    <div class="actions">
      <a class="pdf" href="/pesquisa/Caramaschi_2026_Anchor_Entity_Effect.pdf">Baixar PDF (30 páginas)</a>
      <a class="repo" href="https://github.com/alexandrebrt14-sys/papers" target="_blank" rel="noopener noreferrer">Dataset e código abertos →</a>
    </div>
  </div>
  <article class="paper">
{body}
  </article>
</body>
</html>"""

io.open(f"{DST}/anchor-entity-effect.html", "w", encoding="utf-8").write(page)
print("OK:", f"{DST}/anchor-entity-effect.html", len(page)//1024, "KB")
print("assets:", sorted(os.listdir(DST)))
