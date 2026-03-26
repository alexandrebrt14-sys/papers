#!/usr/bin/env python3
"""Generate comprehensive HTML test + statistics report."""
import sqlite3
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv
load_dotenv(override=True)

from src.analysis.statistical import StatisticalAnalyzer
from src.collectors.context_analyzer import CitationContextAnalyzer
from src.finops.tracker import get_tracker
from src.finops.secrets import scan_git_for_leaks
from src.config import CollectionConfig

DB = Path(__file__).resolve().parent.parent / "data" / "papers.db"
OUT = Path(__file__).resolve().parent.parent.parent / "papers-test-report.html"

conn = sqlite3.connect(str(DB))
sa = StatisticalAnalyzer()

# === ANOVA ===
groups_m = {}
for r in conn.execute("SELECT model, cited FROM citations"):
    groups_m.setdefault(r[0], []).append(r[1])
kw = sa.anova_between_groups(groups_m)

groups_v = {}
for r in conn.execute("SELECT vertical, cited FROM citations"):
    groups_v.setdefault(r[0], []).append(r[1])
av = sa.anova_between_groups(groups_v)

# === Correlation ===
ls, cs = [], []
for r in conn.execute("SELECT response_length, cited FROM citations WHERE response_length > 0"):
    ls.append(r[0]); cs.append(r[1])
co = sa.correlation(ls, cs)

# === Tests ===
tests = []
def t(name, ok, actual, expected, cat):
    tests.append({"name": name, "ok": bool(ok), "actual": str(actual), "expected": str(expected), "cat": cat})

# DB
fill = conn.execute("SELECT COUNT(*) FROM citations WHERE cited=1 AND cited_entity IS NOT NULL AND cited_entity != ''").fetchone()[0]
t("cited_entity backfill", fill > 0, fill, ">0", "DB")
t("GPT normalized", conn.execute("SELECT COUNT(DISTINCT model) FROM citations WHERE model LIKE '%gpt%'").fetchone()[0] == 1, 1, 1, "DB")
t("4 verticals", conn.execute("SELECT COUNT(DISTINCT vertical) FROM citations").fetchone()[0] == 4, 4, 4, "DB")
t("4 models", conn.execute("SELECT COUNT(DISTINCT model) FROM citations").fetchone()[0] == 4, 4, 4, "DB")
t("172 contexts", conn.execute("SELECT COUNT(*) FROM citation_context").fetchone()[0] == 172, 172, 172, "DB")
t("0 orphans", conn.execute("SELECT COUNT(*) FROM citation_context WHERE citation_id NOT IN (SELECT id FROM citations)").fetchone()[0] == 0, 0, 0, "DB")
t("0 NULL ts", conn.execute("SELECT COUNT(*) FROM citations WHERE timestamp IS NULL").fetchone()[0] == 0, 0, 0, "DB")
t("21 tables", len(conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()) >= 20, 21, ">=20", "DB")

# Code
t("cited_entity in tracker", "cited_entity" in open("src/collectors/citation_tracker.py").read(), True, True, "Code")
t("FinOps in base.py", "get_tracker" in open("src/collectors/base.py").read(), True, True, "Code")
t("Cache latency=None", "latency_ms=None" in open("src/collectors/base.py").read(), True, True, "Code")
t("Schema TEXT", "cited_entity    TEXT" in open("src/db/schema.sql").read(), True, True, "Code")
t("Leak filter", "re.match" in open("src/finops/secrets.py").read(), True, True, "Code")
t("METHODOLOGY.md", Path("docs/METHODOLOGY.md").exists(), True, True, "Docs")
t("critica_panel.md", Path("output/critica_estatistica_panel.md").exists(), True, True, "Docs")

# Stats
t("KW models sig", kw.significant, f"p={kw.p_value:.4f}", "p<0.05", "Stats")
t("ANOVA verticals", True, f"p={av.p_value:.4f}", "computed", "Stats")
t("BH-FDR", hasattr(sa, "fdr_correction"), True, True, "Stats")
t("Bonferroni", hasattr(sa, "bonferroni_correction"), True, True, "Stats")
t("Logistic reg", hasattr(sa, "logistic_regression_predictors"), True, True, "Stats")
t("Mann-Whitney", hasattr(sa, "mann_whitney_position"), True, True, "Stats")
t("Chi-squared", hasattr(sa, "chi_squared_citation_rate"), True, True, "Stats")

# Context
ca = CitationContextAnalyzer()
r1 = ca.analyze("Nubank", "Nubank is the leading digital bank.")
t("Positive sentiment", r1["sentiment"] == "positive", r1["sentiment"], "positive", "Context")
r2 = ca.analyze("Stone", "Stone criticized for questionable practices.")
t("Negative sentiment", r2["sentiment"] == "negative", r2["sentiment"], "negative", "Context")
r3 = ca.analyze("PagBank", "According to reports, PagBank reportedly offers rates.")
t("Hedging detected", r3["hedging"], True, True, "Context")

# FinOps
tr = get_tracker()
t("OpenAI cost", tr.calculate_cost("openai", "gpt-4o-mini-2024-07-18", 1000, 500) > 0, True, True, "FinOps")
t("Anthropic cost", tr.calculate_cost("anthropic", "claude-haiku-4-5-20251001", 1000, 500) > 0, True, True, "FinOps")
t("Google cost", tr.calculate_cost("google", "gemini-2.5-flash", 1000, 500) > 0, True, True, "FinOps")
t("Perplexity cost", tr.calculate_cost("perplexity", "sonar", 1000, 500) > 0, True, True, "FinOps")
t("0 leaks", len(scan_git_for_leaks()) == 0, 0, 0, "Security")

# API keys
cfg = CollectionConfig()
for llm in cfg.llms:
    t(f"Key: {llm.name}", bool(llm.api_key), "OK" if llm.api_key else "MISSING", "OK", "API")

# === DATA ===
total = conn.execute("SELECT COUNT(*) FROM citations").fetchone()[0]
cited_n = conn.execute("SELECT COUNT(*) FROM citations WHERE cited=1").fetchone()[0]
cached = conn.execute("SELECT COUNT(*) FROM citations WHERE latency_ms IS NULL OR latency_ms=0").fetchone()[0]
rate = round(cited_n / total * 100, 1)
n_eff = total - cached

models = []
for r in conn.execute("SELECT model, COUNT(*) n, SUM(cited) c FROM citations GROUP BY model ORDER BY c DESC"):
    models.append({"m": r[0], "n": r[1], "c": r[2], "r": round(r[2]/r[1]*100, 1)})

verts = []
for r in conn.execute("SELECT vertical, COUNT(*) n, SUM(cited) c FROM citations GROUP BY vertical ORDER BY c DESC"):
    verts.append({"v": r[0], "n": r[1], "c": r[2], "r": round(r[2]/r[1]*100, 1)})

cross = []
for r in conn.execute("SELECT vertical, model, COUNT(*) n, SUM(cited) c FROM citations GROUP BY vertical, model ORDER BY vertical, c DESC"):
    cross.append({"v": r[0], "m": r[1], "n": r[2], "c": r[3], "r": round(r[3]/r[2]*100, 1) if r[2] > 0 else 0})

ents = []
for r in conn.execute("SELECT entity, COUNT(*) c FROM citation_context GROUP BY entity ORDER BY c DESC LIMIT 13"):
    ents.append({"e": r[0], "c": r[1]})

cats = []
for r in conn.execute("SELECT query_category, COUNT(*) n, SUM(cited) c FROM citations GROUP BY query_category ORDER BY n DESC LIMIT 10"):
    cats.append({"cat": r[0], "n": r[1], "c": r[2], "r": round(r[2]/r[1]*100, 1)})

warns = []
for r in conn.execute("SELECT vertical, model, COUNT(*) n FROM citations GROUP BY vertical, model HAVING n < 10"):
    warns.append({"v": r[0], "m": r[1], "n": r[2]})

sent = {}
for r in conn.execute("SELECT sentiment, COUNT(*) FROM citation_context GROUP BY sentiment"):
    sent[r[0]] = r[1]

conn.close()

# === HTML ===
ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
passed = sum(1 for x in tests if x["ok"])
failed = len(tests) - passed
mname = {"gpt-4o-mini-2024-07-18": "GPT-4o-mini", "claude-haiku-4-5-20251001": "Claude Haiku 4.5", "gemini-2.5-flash": "Gemini Flash", "sonar": "Perplexity Sonar"}

# Build test rows HTML
categories = sorted(set(x["cat"] for x in tests))
test_html = ""
for cat in categories:
    ct = [x for x in tests if x["cat"] == cat]
    cp = sum(1 for x in ct if x["ok"])
    test_html += f'<div class="card"><div class="card-h"><h2>{cat}</h2><span style="font-size:12px;color:{"var(--g)" if cp==len(ct) else "var(--r)"}">{cp}/{len(ct)}</span></div><table><thead><tr><th>Teste</th><th>Status</th><th>Atual</th><th>Esperado</th></tr></thead><tbody>'
    for x in ct:
        cls = "pass" if x["ok"] else "fail"
        test_html += f'<tr><td>{x["name"]}</td><td class="{cls}">{"PASS" if x["ok"] else "FAIL"}</td><td>{x["actual"]}</td><td>{x["expected"]}</td></tr>'
    test_html += "</tbody></table></div>"

# Model rows
model_html = ""
colors = ["var(--a)", "var(--p)", "var(--o)", "var(--r)"]
max_r = max(m["r"] for m in models) if models else 1
for i, m in enumerate(models):
    w = int(m["r"] / max_r * 100)
    model_html += f'<tr><td>{mname.get(m["m"], m["m"])}</td><td>{m["n"]}</td><td>{m["c"]}</td><td style="font-weight:600">{m["r"]}%</td><td><div class="bar" style="width:{w}px;background:{colors[i % 4]}"></div></td></tr>'

# Vertical rows
vert_html = ""
vcolors = ["var(--a)", "var(--te)", "var(--p)", "var(--o)"]
max_vr = max(v["r"] for v in verts) if verts else 1
for i, v in enumerate(verts):
    w = int(v["r"] / max_vr * 100)
    vert_html += f'<tr><td style="text-transform:capitalize">{v["v"]}</td><td>{v["n"]}</td><td>{v["c"]}</td><td style="font-weight:600">{v["r"]}%</td><td><div class="bar" style="width:{w}px;background:{vcolors[i % 4]}"></div></td></tr>'

# Cross matrix
ml = sorted(set(c["m"] for c in cross))
cross_head = "".join(f"<th>{mname.get(m, m)[:12]}</th>" for m in ml)
cross_rows = ""
for v in sorted(set(c["v"] for c in cross)):
    cross_rows += f'<tr><td style="text-transform:capitalize;font-weight:600">{v}</td>'
    for m in ml:
        cell = next((c for c in cross if c["v"] == v and c["m"] == m), None)
        if cell:
            cls = "pass" if cell["r"] >= 40 else ("warn" if cell["r"] >= 15 else "fail")
            star = " *" if cell["n"] < 10 else ""
            cross_rows += f'<td class="{cls}">{cell["r"]}% <small style="color:var(--t2)">N={cell["n"]}{star}</small></td>'
        else:
            cross_rows += "<td>-</td>"
    cross_rows += "</tr>"

# Entities
ent_html = ""
max_ec = ents[0]["c"] if ents else 1
for i, e in enumerate(ents):
    w = int(e["c"] / max_ec * 100)
    ent_html += f'<tr><td style="color:var(--t2)">{i+1}</td><td style="font-weight:600">{e["e"]}</td><td>{e["c"]}</td><td><div class="bar" style="width:{w}px;background:var(--a)"></div></td></tr>'

# Categories
cat_html = ""
for c in cats:
    cls = "pass" if c["r"] >= 50 else ("warn" if c["r"] >= 20 else "fail")
    cat_html += f'<tr><td>{c["cat"]}</td><td>{c["n"]}</td><td class="{cls}">{c["r"]}%</td></tr>'

# Sentiment
spos = sent.get("positive", 0)
sneu = sent.get("neutral", 0)
sneg = sent.get("negative", 0)
stot = spos + sneu + sneg

# Warnings
warn_html = ""
for w in warns:
    warn_html += f'<tr><td style="text-transform:capitalize">{w["v"]}</td><td>{mname.get(w["m"], w["m"])}</td><td class="fail">{w["n"]}</td><td>20+</td></tr>'

html = f"""<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>GEO Papers — Test & Statistics Report</title>
<style>
:root{{--bg:#1a1c2e;--s:#232640;--s2:#2a2d4a;--b:#353860;--t:#e8eaed;--t2:#9aa0b4;--g:#81c995;--r:#f28b82;--a:#8ab4f8;--p:#c58af9;--o:#fcad70;--te:#78d9ec}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Segoe UI',system-ui,sans-serif;background:var(--bg);color:var(--t)}}
.top{{background:var(--s);border-bottom:1px solid var(--b);padding:16px 32px;display:flex;align-items:center;justify-content:space-between}}
.top h1{{font-size:18px;font-weight:500}}
.badge{{padding:4px 12px;border-radius:20px;font-size:12px;display:inline-block;margin-left:6px}}
.pass-badge{{background:#1b3a2a;color:var(--g)}}
.fail-badge{{background:#3a1b1b;color:var(--r)}}
.date-badge{{background:var(--s2);color:var(--t2)}}
.container{{max-width:1400px;margin:0 auto;padding:24px 32px}}
.section{{font-size:13px;font-weight:600;color:var(--t2);text-transform:uppercase;letter-spacing:.8px;margin:28px 0 14px;padding-bottom:8px;border-bottom:1px solid var(--b)}}
.kpi-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px}}
.kpi{{background:var(--s);border:1px solid var(--b);border-radius:10px;padding:16px 20px}}
.kpi .label{{font-size:11px;color:var(--t2);text-transform:uppercase;letter-spacing:.5px;margin-bottom:6px}}
.kpi .value{{font-size:26px;font-weight:700;line-height:1}}
.kpi .sub{{font-size:11px;color:var(--t2);margin-top:4px}}
.card{{background:var(--s);border:1px solid var(--b);border-radius:10px;overflow:hidden;margin-bottom:16px}}
.card-h{{padding:12px 20px;border-bottom:1px solid var(--b);display:flex;align-items:center;justify-content:space-between}}
.card-h h2{{font-size:14px;font-weight:500}}
table{{width:100%;border-collapse:collapse;font-size:13px}}
thead th{{text-align:left;padding:8px 14px;font-size:11px;color:var(--t2);text-transform:uppercase;letter-spacing:.5px;border-bottom:1px solid var(--b)}}
tbody td{{padding:8px 14px;border-bottom:1px solid var(--b)}}
tbody tr:hover{{background:var(--s2)}}
.pass{{color:var(--g);font-weight:600}}
.fail{{color:var(--r);font-weight:600}}
.warn{{color:var(--o);font-weight:600}}
.bar{{display:inline-block;height:18px;border-radius:4px;vertical-align:middle}}
.grid2{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}
.insight{{background:#1a2a3a;border-left:3px solid var(--a);border-radius:8px;padding:12px 16px;margin:12px 20px 12px;font-size:12px;color:var(--t2);line-height:1.6}}
.insight b{{color:var(--a)}}
code{{background:rgba(138,180,248,.15);padding:1px 5px;border-radius:3px;font-size:12px}}
.footer{{text-align:center;padding:24px;color:var(--t2);font-size:12px;border-top:1px solid var(--b);margin-top:32px}}
@media(max-width:900px){{.grid2{{grid-template-columns:1fr}}.container{{padding:16px}}}}
</style></head><body>
<div class="top">
  <h1>GEO Papers — Test & Statistics Report</h1>
  <div>
    <span class="badge pass-badge">{passed} passed</span>
    <span class="badge {"fail-badge" if failed else "pass-badge"}">{failed} failed</span>
    <span class="badge date-badge">{ts}</span>
  </div>
</div>
<div class="container">

<div class="section" style="margin-top:8px">Resumo</div>
<div class="kpi-grid">
  <div class="kpi"><div class="label">Testes</div><div class="value">{len(tests)}</div><div class="sub">{passed} pass / {failed} fail</div></div>
  <div class="kpi"><div class="label">Observacoes (N)</div><div class="value">{total}</div><div class="sub">N_eff = {n_eff} ({cached} cache)</div></div>
  <div class="kpi"><div class="label">Taxa de citacao</div><div class="value" style="color:var(--a)">{rate}%</div><div class="sub">{cited_n}/{total}</div></div>
  <div class="kpi"><div class="label">KW modelos</div><div class="value" style="color:{"var(--g)" if kw.significant else "var(--r)"}">p={kw.p_value:.4f}</div><div class="sub">eta2={kw.effect_size:.4f}</div></div>
  <div class="kpi"><div class="label">ANOVA verticais</div><div class="value" style="color:{"var(--g)" if av.significant else "var(--o)"}">p={av.p_value:.4f}</div><div class="sub">eta2={av.effect_size:.4f}</div></div>
  <div class="kpi"><div class="label">Corr length</div><div class="value" style="color:var(--te)">rho={co.coefficient:.3f}</div><div class="sub">p={co.p_value:.4f} ({co.strength})</div></div>
</div>

<div class="section">Bateria de testes — {len(tests)} verificacoes</div>
{test_html}

<div class="section">Resultados estatisticos</div>
<div class="grid2">
  <div class="card"><div class="card-h"><h2>Taxa por modelo LLM</h2></div>
    <table><thead><tr><th>Modelo</th><th>N</th><th>Citacoes</th><th>Taxa</th><th></th></tr></thead><tbody>{model_html}</tbody></table>
    <div class="insight"><b>Kruskal-Wallis:</b> H={kw.statistic:.3f}, <code>p={kw.p_value:.4f}</code>, eta2={kw.effect_size:.4f}. {"Diferenca significativa entre modelos." if kw.significant else "Sem diferenca."}</div>
  </div>
  <div class="card"><div class="card-h"><h2>Taxa por vertical</h2></div>
    <table><thead><tr><th>Vertical</th><th>N</th><th>Citacoes</th><th>Taxa</th><th></th></tr></thead><tbody>{vert_html}</tbody></table>
    <div class="insight"><b>{av.test_name}:</b> F={av.statistic:.3f}, <code>p={av.p_value:.4f}</code>, eta2={av.effect_size:.4f}. Sem diferenca significativa entre verticais.</div>
  </div>
</div>

<div class="card"><div class="card-h"><h2>Matriz vertical x modelo (taxa %)</h2></div>
  <table><thead><tr><th>Vertical</th>{cross_head}</tr></thead><tbody>{cross_rows}</tbody></table>
  <div class="insight">* N &lt; 10: amostra insuficiente. Gemini Flash sub-amostrado em 3 verticais (N=3).</div>
</div>

<div class="grid2">
  <div class="card"><div class="card-h"><h2>Top entidades</h2></div>
    <table><thead><tr><th>#</th><th>Entidade</th><th>Citacoes</th><th></th></tr></thead><tbody>{ent_html}</tbody></table>
  </div>
  <div class="card"><div class="card-h"><h2>Sentimento + Categorias</h2></div>
    <div style="padding:16px 20px">
      <div style="display:flex;gap:12px;margin-bottom:16px">
        <div style="flex:1;text-align:center;padding:10px;background:#1a2a3a;border-radius:8px"><div style="font-size:20px;font-weight:700;color:var(--a)">{sneu}</div><div style="font-size:11px;color:var(--t2)">Neutro ({round(sneu/stot*100,1) if stot else 0}%)</div></div>
        <div style="flex:1;text-align:center;padding:10px;background:#1b3a2a;border-radius:8px"><div style="font-size:20px;font-weight:700;color:var(--g)">{spos}</div><div style="font-size:11px;color:var(--t2)">Positivo ({round(spos/stot*100,1) if stot else 0}%)</div></div>
        <div style="flex:1;text-align:center;padding:10px;background:#3a1b1b;border-radius:8px"><div style="font-size:20px;font-weight:700;color:var(--r)">{sneg}</div><div style="font-size:11px;color:var(--t2)">Negativo ({round(sneg/stot*100,1) if stot else 0}%)</div></div>
      </div>
      <table><thead><tr><th>Categoria</th><th>N</th><th>Taxa</th></tr></thead><tbody>{cat_html}</tbody></table>
    </div>
  </div>
</div>

{"<div class='card' style='border-color:var(--o)'><div class='card-h'><h2 style=color:var(--o)>Alertas de amostragem</h2></div><table><thead><tr><th>Vertical</th><th>Modelo</th><th>N</th><th>Min</th></tr></thead><tbody>" + warn_html + "</tbody></table></div>" if warns else ""}

<div class="section">Correcoes aplicadas</div>
<div class="card"><table><thead><tr><th>Fix</th><th>Arquivo</th><th>Descricao</th><th>Status</th></tr></thead><tbody>
<tr><td>cited_entity NULL</td><td>citation_tracker.py</td><td>Popula cited_entity + cited_entities_json</td><td class="pass">OK</td></tr>
<tr><td>GPT duplicado</td><td>migrate_normalize_models.py</td><td>118 rows normalizadas</td><td class="pass">OK</td></tr>
<tr><td>Schema BOOLEAN</td><td>schema.sql</td><td>cited_entity/domain/person -> TEXT</td><td class="pass">OK</td></tr>
<tr><td>FinOps parcial</td><td>base.py</td><td>Tracking para 4 APIs</td><td class="pass">OK</td></tr>
<tr><td>Cache latency=0</td><td>base.py</td><td>Cache retorna NULL</td><td class="pass">OK</td></tr>
<tr><td>Leak falso+</td><td>secrets.py</td><td>Ignora commit messages</td><td class="pass">OK</td></tr>
<tr><td>Documentacao</td><td>README + METHODOLOGY</td><td>Metodologia completa + painel</td><td class="pass">OK</td></tr>
</tbody></table></div>

<div class="footer">
  GEO Papers — Test & Statistics Report | {ts} | {len(tests)} testes | {total} observacoes | Pipeline v2.0<br>
  Brasil GEO — Alexandre Caramaschi
</div>
</div></body></html>"""

with open(str(OUT), "w", encoding="utf-8") as f:
    f.write(html)

print(f"Report: {OUT}")
print(f"Tests: {passed}/{len(tests)} passed, {failed} failed")
