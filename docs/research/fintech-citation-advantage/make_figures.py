# -*- coding: utf-8 -*-
"""Gera as 7 figuras do manuscrito a partir do papers.db (estilo academico)."""
import sqlite3, json, math, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DIR = r"C:/Sandyboxclaude/papers/docs/research/fintech-citation-advantage"
DB = r"C:/Users/alexa/AppData/Local/Temp/planb/data/papers.db"
FILT = "COALESCE(is_probe,0)=0 AND COALESCE(is_calibration,0)=0"
VORDER = ["fintech", "varejo", "tecnologia", "saude"]
VLABEL = {"fintech": "Fintech", "varejo": "Retail", "tecnologia": "Technology", "saude": "Healthcare"}
VCOLOR = {"fintech": "#1f4e79", "varejo": "#c0504d", "tecnologia": "#9bbb59", "saude": "#8064a2"}
ANCHORS = {"fintech": ["Nubank"], "varejo": ["Mercado Livre", "Magazine Luiza"],
           "tecnologia": ["Totvs"], "saude": ["Hypera Pharma"]}

plt.rcParams.update({
    "font.family": "serif", "font.size": 9, "axes.titlesize": 9.5,
    "axes.labelsize": 9, "figure.dpi": 180, "savefig.bbox": "tight",
    "axes.spines.top": False, "axes.spines.right": False,
})

db = sqlite3.connect(DB)
cur = db.cursor()

def wilson(p, n, z=1.96):
    d = 1 + z*z/n
    c = p + z*z/(2*n)
    s = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))
    return ((c-s)/d, (c+s)/d)

def entities_of(js):
    try:
        out = []
        for e in json.loads(js or "[]"):
            out.append(e if isinstance(e, str) else (e.get("entity") or e.get("name") or str(e)))
        return out
    except Exception:
        return []

# ── dados base por vertical
base = {}
for v, n, c in cur.execute(f"SELECT vertical, COUNT(*), SUM(cited_v2) FROM citations WHERE {FILT} GROUP BY 1"):
    base[v] = (n, c, 100.0*c/n)

# ── FIG 1: weekly citation rate by vertical
rows = cur.execute(f"SELECT strftime('%W', timestamp), vertical, COUNT(*), SUM(cited_v2) FROM citations WHERE {FILT} GROUP BY 1,2 ORDER BY 1").fetchall()
weeks = sorted(set(int(r[0]) for r in rows))
fig, ax = plt.subplots(figsize=(6.3, 2.9))
for v in VORDER:
    ys = []
    for w in weeks:
        m = [r for r in rows if int(r[0]) == w and r[1] == v]
        ys.append(100.0*m[0][3]/m[0][2] if m and m[0][2] else None)
    ax.plot([f"W{w}" for w in weeks], ys, marker="o", ms=3, lw=1.3, label=VLABEL[v], color=VCOLOR[v])
ax.set_ylabel("Citation rate (%)"); ax.set_ylim(0, 35)
ax.legend(frameon=False, ncol=4, fontsize=8, loc="lower center", bbox_to_anchor=(0.5, -0.42))
fig.savefig(f"{DIR}/fig1.png"); plt.close(fig)

# ── leave-one-out por vertical (recodifica not-cited quando so a(s) ancora(s) citadas)
loo = {}
for v in VORDER:
    anchors = set(ANCHORS[v])
    n_tot, c_tot, _ = base[v]
    only_anchor = 0
    for (js,) in cur.execute(f"SELECT cited_entities_v2_json FROM citations WHERE {FILT} AND vertical=? AND cited_v2=1", (v,)):
        ents = set(entities_of(js))
        if ents and ents.issubset(anchors):
            only_anchor += 1
    loo[v] = 100.0*(c_tot-only_anchor)/n_tot

# ── FIG 2: baseline vs anchor-removed (dumbbell)
fig, ax = plt.subplots(figsize=(6.3, 2.7))
ypos = list(range(len(VORDER)))[::-1]
for y, v in zip(ypos, VORDER):
    b, a = base[v][2], loo[v]
    ax.plot([a, b], [y, y], color="#999", lw=1.4, zorder=1)
    ax.scatter([b], [y], s=46, color=VCOLOR[v], zorder=2, label=None)
    ax.scatter([a], [y], s=46, facecolors="white", edgecolors=VCOLOR[v], zorder=2)
    ax.text(b+0.5, y, f"{b:.1f}", va="center", fontsize=8)
    ax.text(a-0.5, y, f"{a:.1f}", va="center", ha="right", fontsize=8)
ax.set_yticks(ypos); ax.set_yticklabels([f"{VLABEL[v]} (top-{len(ANCHORS[v])})" for v in VORDER])
ax.set_xlabel("Citation rate (%) — filled: baseline; open: top-k anchors removed")
ax.set_xlim(0, 33)
fig.savefig(f"{DIR}/fig2.png"); plt.close(fig)

# ── FIG 3: excess fintech-vs-retail cited responses per engine
rows = cur.execute(f"SELECT llm, vertical, SUM(cited_v2) FROM citations WHERE {FILT} AND vertical IN ('fintech','varejo') GROUP BY 1,2").fetchall()
m = {(r[0], r[1]): r[2] for r in rows}
llms = sorted(set(r[0] for r in rows))
excess = {l: (m.get((l, "fintech"), 0) - m.get((l, "varejo"), 0)) for l in llms}
fig, ax = plt.subplots(figsize=(6.3, 2.7))
xs = list(excess.keys()); ys = [excess[x] for x in xs]
colors = ["#1f4e79" if y > 0 else "#c0504d" for y in ys]
ax.bar(xs, ys, color=colors, width=0.55)
ax.axhline(0, color="#333", lw=0.8)
for x, y in zip(xs, ys):
    ax.text(x, y + (14 if y >= 0 else -26), f"{y:+d}", ha="center", fontsize=8)
ax.set_ylabel("Excess cited responses\n(fintech − retail)")
fig.savefig(f"{DIR}/fig3.png"); plt.close(fig)

# ── FIG 4: HHI vs rate
hhi = {}
for v in VORDER:
    ents = {}
    for (js,) in cur.execute(f"SELECT cited_entities_v2_json FROM citations WHERE {FILT} AND vertical=? AND cited_v2=1", (v,)):
        for e in entities_of(js):
            ents[e] = ents.get(e, 0) + 1
    tot = sum(ents.values())
    hhi[v] = sum((c/tot)**2 for c in ents.values())
fig, ax = plt.subplots(figsize=(4.6, 3.0))
for v in VORDER:
    ax.scatter(hhi[v], base[v][2], s=70, color=VCOLOR[v])
    ax.annotate(VLABEL[v], (hhi[v], base[v][2]), textcoords="offset points", xytext=(7, -3), fontsize=8.5)
ax.set_xlabel("Mention concentration (HHI)"); ax.set_ylabel("Citation rate (%)")
ax.set_xlim(0.05, 0.33); ax.set_ylim(8, 33)
fig.savefig(f"{DIR}/fig4.png"); plt.close(fig)

# ── FIG 5: heatmap vertical x engine
rows = cur.execute(f"SELECT vertical, llm, COUNT(*), SUM(cited_v2) FROM citations WHERE {FILT} GROUP BY 1,2").fetchall()
mm = {(r[0], r[1]): 100.0*r[3]/r[2] for r in rows}
llms = sorted(set(r[1] for r in rows))
data = [[mm.get((v, l), 0) for l in llms] for v in VORDER]
fig, ax = plt.subplots(figsize=(6.3, 2.4))
im = ax.imshow(data, cmap="Blues", aspect="auto", vmin=0, vmax=95)
ax.set_xticks(range(len(llms))); ax.set_xticklabels(llms, fontsize=8)
ax.set_yticks(range(len(VORDER))); ax.set_yticklabels([VLABEL[v] for v in VORDER], fontsize=8)
for i, v in enumerate(VORDER):
    for j, l in enumerate(llms):
        val = mm.get((v, l), 0)
        ax.text(j, i, f"{val:.1f}", ha="center", va="center", fontsize=7.5,
                color="white" if val > 55 else "#111")
fig.colorbar(im, ax=ax, shrink=0.85, label="Citation rate (%)")
fig.savefig(f"{DIR}/fig5.png"); plt.close(fig)

# ── FIG 6: truncation loss (% citations with first entity after char 200, Perplexity full text)
rows = cur.execute(f"""SELECT vertical, COUNT(*), SUM(CASE WHEN first_entity_offset_v2 > 200 THEN 1 ELSE 0 END)
  FROM citations WHERE {FILT} AND llm='Perplexity' AND cited_v2=1 AND first_entity_offset_v2 IS NOT NULL GROUP BY 1""").fetchall()
loss = {r[0]: 100.0*r[2]/r[1] for r in rows}
fig, ax = plt.subplots(figsize=(4.8, 2.7))
xs = [VLABEL[v] for v in VORDER]; ys = [loss.get(v, 0) for v in VORDER]
ax.bar(xs, ys, color=[VCOLOR[v] for v in VORDER], width=0.5)
for x, y in zip(xs, ys):
    ax.text(x, y + 1.2, f"{y:.1f}%", ha="center", fontsize=8.5)
ax.set_ylabel("Citations lost under\n200-char truncation (%)")
ax.set_ylim(0, max(ys) + 8)
fig.savefig(f"{DIR}/fig6.png"); plt.close(fig)

# ── FIG 7: Nubank share of fintech mentions, weekly + sole-Nubank fraction
rows = cur.execute(f"SELECT strftime('%W', timestamp), cited_entities_v2_json FROM citations WHERE {FILT} AND vertical='fintech' AND cited_v2=1").fetchall()
wk_mentions, wk_nubank, wk_resp, wk_sole = {}, {}, {}, {}
for w, js in rows:
    w = int(w)
    ents = entities_of(js)
    wk_mentions[w] = wk_mentions.get(w, 0) + len(ents)
    wk_nubank[w] = wk_nubank.get(w, 0) + sum(1 for e in ents if e == "Nubank")
    wk_resp[w] = wk_resp.get(w, 0) + 1
    if set(ents) == {"Nubank"}:
        wk_sole[w] = wk_sole.get(w, 0) + 1
wks = sorted(wk_mentions)
share = [100.0*wk_nubank[w]/wk_mentions[w] for w in wks]
sole = [100.0*wk_sole.get(w, 0)/wk_resp[w] for w in wks]
fig, ax = plt.subplots(figsize=(6.3, 2.9))
ax.plot([f"W{w}" for w in wks], share, marker="o", ms=3.5, lw=1.5, color="#1f4e79",
        label="Nubank share of fintech mentions")
ax.plot([f"W{w}" for w in wks], sole, marker="s", ms=3.5, lw=1.3, color="#c0504d", ls="--",
        label="Sole-Nubank fraction of cited responses")
ax.set_ylabel("Share (%)"); ax.set_ylim(30, 75)
ax.legend(frameon=False, fontsize=8, loc="upper left")
fig.savefig(f"{DIR}/fig7.png"); plt.close(fig)

print("FIGS OK:", [f"fig{i}.png={os.path.getsize(f'{DIR}/fig{i}.png')//1024}KB" for i in range(1, 8)])
print("check: base rates", {v: round(base[v][2], 2) for v in VORDER})
print("check: LOO", {v: round(loo[v], 2) for v in VORDER})
print("check: HHI", {v: round(hhi[v], 3) for v in VORDER})
print("check: excess per engine", excess)
print("check: trunc loss", {v: round(loss.get(v, 0), 1) for v in VORDER})
print("check: nubank share first/last", round(share[0], 1), round(share[-1], 1))
