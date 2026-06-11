# -*- coding: utf-8 -*-
"""Extração quantitativa para o draft 'Fintech Citation Advantage' (papers.db v2)."""
import sqlite3, json, math, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
DB = r"C:/Users/alexa/AppData/Local/Temp/planb/data/papers.db"
db = sqlite3.connect(DB)
cur = db.cursor()

def wilson(p, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    s = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - s) / d, (c + s) / d)

def chi2_2x2(a, b, c, d):
    n = a + b + c + d
    den = (a + b) * (c + d) * (a + c) * (b + d)
    if den == 0:
        return 0.0, 1.0
    x2 = n * (a * d - b * c) ** 2 / den
    p = math.erfc(math.sqrt(x2 / 2))
    return x2, p

FILT = "COALESCE(is_probe,0)=0 AND COALESCE(is_calibration,0)=0"

print("# Análise quantitativa — papers.db (62.820 obs, 2026-04-23 a 2026-06-09)")
print()
print("Base: janela confirmatória v2, extração NER v2 (cited_v2). Núcleo = sem probes/calibração.")
print()

total = cur.execute("SELECT COUNT(*), SUM(cited_v2) FROM citations").fetchone()
core = cur.execute(f"SELECT COUNT(*), SUM(cited_v2) FROM citations WHERE {FILT}").fetchone()
print("## 0. Visão geral")
print(f"- Bruto: n={total[0]}, cited_v2={total[1]} ({100*total[1]/total[0]:.1f}%)")
print(f"- Núcleo: n={core[0]}, cited_v2={core[1]} ({100*core[1]/core[0]:.1f}%)")
print()

print("## 1. Taxa de citação por vertical (núcleo) + IC95 Wilson")
rows = cur.execute(
    f"SELECT vertical, COUNT(*), SUM(cited_v2) FROM citations WHERE {FILT} "
    "GROUP BY vertical ORDER BY CAST(SUM(cited_v2) AS REAL)/COUNT(*) DESC"
).fetchall()
vert = {}
for v, n, c in rows:
    p = c / n
    lo, hi = wilson(p, n)
    vert[v] = (n, c, p)
    print(f"- {v}: n={n}, cited={c}, rate={100*p:.2f}% (IC95 {100*lo:.2f}-{100*hi:.2f}%)")

print()
print("### Qui-quadrado (fintech vs outras, 1 g.l.)")
fn, fc, _ = vert.get("fintech", (0, 0, 0))
for v, (n, c, p) in vert.items():
    if v == "fintech":
        continue
    x2, pv = chi2_2x2(fc, fn - fc, c, n - c)
    pstr = "<1e-15" if pv < 1e-15 else f"{pv:.2e}"
    print(f"- fintech vs {v}: chi2={x2:.1f}, p={pstr}")

print()
print("## 2. Matriz vertical x LLM (rate %, núcleo)")
rows = cur.execute(
    f"SELECT vertical, llm, COUNT(*), SUM(cited_v2) FROM citations WHERE {FILT} GROUP BY vertical, llm"
).fetchall()
llms = sorted(set(r[1] for r in rows))
m = {(r[0], r[1]): (r[2], r[3]) for r in rows}
print("| vertical | " + " | ".join(llms) + " |")
print("|---|" + "---|" * len(llms))
for v in vert:
    cells = []
    for l in llms:
        n, c = m.get((v, l), (0, 0))
        cells.append(f"{100*c/n:.1f} (n={n})" if n else "-")
    print(f"| {v} | " + " | ".join(cells) + " |")

print()
print("## 3. Concentração de citações por entidade (NER v2, núcleo)")
for v in vert:
    ents = {}
    for (js,) in cur.execute(
        f"SELECT cited_entities_v2_json FROM citations WHERE {FILT} AND vertical=? AND cited_v2=1", (v,)
    ):
        try:
            for e in json.loads(js or "[]"):
                name = e if isinstance(e, str) else (e.get("entity") or e.get("name") or str(e))
                ents[name] = ents.get(name, 0) + 1
        except Exception:
            pass
    tot = sum(ents.values())
    if not tot:
        print(f"- {v}: sem dados de entidades")
        continue
    top = sorted(ents.items(), key=lambda x: -x[1])[:8]
    hhi = sum((cnt / tot) ** 2 for cnt in ents.values())
    top3 = sum(cnt for _, cnt in top[:3]) / tot
    print(f"- {v}: {len(ents)} entidades, {tot} menções | top3={100*top3:.1f}% | HHI={hhi:.3f}")
    print("  top: " + ", ".join(f"{nme} ({cnt})" for nme, cnt in top))

print()
print("## 4. Mix de query_category por vertical (confounder) e rate por categoria")
for v, cat, n, c in cur.execute(
    f"SELECT vertical, query_category, COUNT(*), SUM(cited_v2) FROM citations WHERE {FILT} GROUP BY 1,2 ORDER BY 1,3 DESC"
).fetchall():
    print(f"- {v} | {cat}: n={n}, rate={100*c/n:.1f}%")

print()
print("## 5. Por idioma da query")
for v, lang, n, c in cur.execute(
    f"SELECT vertical, query_lang, COUNT(*), SUM(cited_v2) FROM citations WHERE {FILT} GROUP BY 1,2"
).fetchall():
    print(f"- {v} | {lang}: n={n}, rate={100*c/n:.1f}%")

print()
print("## 6. Série semanal por vertical (rate %) — estabilidade do gap")
rows = cur.execute(
    f"SELECT strftime('%Y-W%W', timestamp) wk, vertical, COUNT(*), SUM(cited_v2) "
    f"FROM citations WHERE {FILT} GROUP BY 1,2 ORDER BY 1"
).fetchall()
weeks = sorted(set(r[0] for r in rows))
mm = {(r[0], r[1]): (r[2], r[3]) for r in rows}
print("| semana | " + " | ".join(vert.keys()) + " |")
print("|---|" + "---|" * len(vert))
for w in weeks:
    cells = []
    for v in vert:
        n, c = mm.get((w, v), (0, 0))
        cells.append(f"{100*c/n:.1f}" if n else "-")
    print(f"| {w} | " + " | ".join(cells) + " |")

CFILT = "COALESCE(c.is_probe,0)=0 AND COALESCE(c.is_calibration,0)=0"
print()
print("## 7. Qualidade da citação (citation_context)")
agg = {}
for v, s, n in cur.execute(
    f"SELECT c.vertical, cc.sentiment, COUNT(*) FROM citation_context cc "
    f"JOIN citations c ON c.id=cc.citation_id WHERE {CFILT} GROUP BY 1,2"
).fetchall():
    agg.setdefault(v, {})[s] = n
for v, d in agg.items():
    t = sum(d.values())
    print(f"- {v}: " + ", ".join(f"{s}={100*n/t:.1f}%" for s, n in sorted(d.items(), key=lambda x: str(x[0]))) + f" (n={t})")

print()
print("### Tercil de posição (1=início)")
agg = {}
for v, tc, n in cur.execute(
    f"SELECT c.vertical, cc.position_tercile, COUNT(*) FROM citation_context cc "
    f"JOIN citations c ON c.id=cc.citation_id WHERE {CFILT} GROUP BY 1,2"
).fetchall():
    agg.setdefault(v, {})[tc] = n
for v, d in agg.items():
    t = sum(d.values())
    print(f"- {v}: " + ", ".join(f"T{tc}={100*n/t:.1f}%" for tc, n in sorted(d.items(), key=lambda x: str(x[0]))) + f" (n={t})")

print()
print("### Hedging por vertical")
for v, n, h in cur.execute(
    f"SELECT c.vertical, COUNT(*), SUM(CASE WHEN cc.hedging THEN 1 ELSE 0 END) FROM citation_context cc "
    f"JOIN citations c ON c.id=cc.citation_id WHERE {CFILT} GROUP BY 1"
).fetchall():
    print(f"- {v}: hedging={100*(h or 0)/n:.1f}% (n={n})")

print()
print("## 8. Decoys fictícios — FPR por vertical (probes/calibração)")
for v, n, h in cur.execute(
    "SELECT vertical, COUNT(*), SUM(COALESCE(fictional_hit,0)) FROM citations "
    "WHERE COALESCE(is_calibration,0)=1 OR COALESCE(is_probe,0)=1 OR fictitious_target IS NOT NULL GROUP BY 1"
).fetchall():
    print(f"- {v}: n={n}, hits={h or 0}, FPR={100*(h or 0)/n:.2f}%")

print()
print("## 9. Covariáveis por vertical (núcleo)")
for v, n, rl, sc, tk, lat in cur.execute(
    f"SELECT vertical, COUNT(*), AVG(response_length), AVG(source_count), AVG(token_count), AVG(latency_ms) "
    f"FROM citations WHERE {FILT} GROUP BY 1"
).fetchall():
    scs = "-" if sc is None else f"{sc:.2f}"
    print(f"- {v}: resp_len={rl:.0f} chars, sources={scs}, tokens={0 if tk is None else tk:.0f}, lat={lat:.0f}ms")

print()
print("## 10. Selection vs Absorption (CSR/CAR) por vertical, onde preenchido")
for v, sel, ab, n in cur.execute(
    f"SELECT vertical, selection_status, absorption_status, COUNT(*) FROM citations "
    f"WHERE {FILT} AND (selection_status IS NOT NULL OR absorption_status IS NOT NULL) GROUP BY 1,2,3 ORDER BY 1,4 DESC"
).fetchall():
    print(f"- {v} | sel={sel} ab={ab}: n={n}")

print()
print("## 11. Normalização por tamanho de roster e intensidade multi-entidade")
print("Roster v2: fintech=19 BR reais, varejo=15, saude=15, tecnologia=15.")
roster = {"fintech": 19, "varejo": 15, "saude": 15, "tecnologia": 15}
for v, (n, c, p) in vert.items():
    r = roster.get(v)
    if r:
        print(f"- {v}: {c} respostas com citação / {r} entidades no roster = {c/r:.0f} por entidade")
for v, avg in cur.execute(
    f"SELECT vertical, AVG(COALESCE(cited_count_v2,0)) FROM citations WHERE {FILT} GROUP BY 1"
).fetchall():
    print(f"  - {v}: média de entidades citadas por resposta = {avg:.3f}")

print()
print("## 12. Query types (núcleo) por vertical")
for v, qt, n, c in cur.execute(
    f"SELECT vertical, query_type, COUNT(*), SUM(cited_v2) FROM citations WHERE {FILT} GROUP BY 1,2 ORDER BY 1,3 DESC"
).fetchall():
    print(f"- {v} | {qt}: n={n}, rate={100*c/n:.1f}%")
