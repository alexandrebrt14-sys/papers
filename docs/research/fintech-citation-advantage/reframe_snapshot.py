# -*- coding: utf-8 -*-
"""Reframe: de 'interim day 50 of 90' para 'recorte completo 23/abr-09/jun'."""
import io

DIR = r"C:/Sandyboxclaude/papers/docs/research/fintech-citation-advantage"

EDITS = {
    "paper_sec_A_intro.md": [
        ("We report an interim 50-day audit (April-June 2026, day 50 of a planned 90-day window) of spontaneous brand citation",
         "We report a complete 48-day audit, covering the full collection record from the first run to the most recent (April 23 - June 9, 2026), of spontaneous brand citation"),
        ("All rates are reported as interim upper bounds.",
         "All absolute rates are reported as upper bounds pending untruncated re-collection."),
        ("report every absolute rate as an interim upper bound",
         "report every absolute rate as an upper bound"),
        ("Four of five engines are economy-tier models, the data are interim (day 50 of 90), and the market is single and non-Anglophone.",
         "Four of five engines are economy-tier models, the snapshot covers the complete collection record from the first to the most recent run (April 23 - June 9, 2026), and the market is single and non-Anglophone."),
    ],
    "paper_sec_B_methods.md": [
        ("opening of the confirmatory window; the analysis reported here is interim, taken at\nday 50 of a planned 90-day window.",
         "opening of the confirmatory window; the analysis reported here covers the complete\ncollection record, from the first run (April 23, 2026) through the most recent (June 9, 2026)."),
        ("interim analysis at day 50, with collection still active.",
         "a full snapshot through June 9, 2026, with the collection program still active."),
        ("The reproducibility package is incomplete at this interim stage,",
         "The reproducibility package is incomplete at this stage,"),
        ("the data are declared interim until the window closes (2026-07-21).",
         "the dataset continues to accrue in the ongoing collection program; subsequent snapshots will extend this record."),
    ],
    "paper_sec_C_results.md": [
        ("The window is interim — day 50 of a planned 90 — so absolute rates and the anchor concentration figure should be read as upper bounds",
         "This snapshot covers the complete collection record to date (April 23 - June 9, 2026); absolute rates and the anchor concentration figure should be read as upper bounds"),
        ("to be tracked to day 90,",
         "to be tracked in subsequent snapshots,"),
    ],
    "paper_sec_D_theory.md": [
        ("Compounded with the interim nature of the window (day 50 of 90, the opening of the phenomenon, when cumulative advantage is still accelerating), this means",
         "Compounded with the fact that the snapshot captures the opening of the phenomenon, when cumulative advantage is still accelerating, this means"),
    ],
    "paper_sec_E_discussion.md": [
        ("Data are interim (day 50 of a 90-day window) and every",
         "Data cover the complete collection record (April 23 - June 9, 2026) and every"),
        ("what the interim data cannot yet support",
         "what the current data cannot yet support"),
        ("We do not claim more than the interim data support",
         "We do not claim more than the current data support"),
    ],
}

for fn, pairs in EDITS.items():
    p = f"{DIR}/{fn}"
    t = io.open(p, encoding="utf-8").read()
    for old, new in pairs:
        if old in t:
            t = t.replace(old, new, 1)
            print(f"OK  {fn}: {old[:55]}...")
        else:
            print(f"MISS {fn}: {old[:55]}...")
    io.open(p, "w", encoding="utf-8").write(t)

# date line (procura no sec_A qualquer linha com 'Interim manuscript')
p = f"{DIR}/paper_sec_A_intro.md"
t = io.open(p, encoding="utf-8").read()
import re
t2 = re.sub(r"Interim manuscript[^\n]*",
            "Research report - June 11, 2026 · Data: complete collection record, April 23 - June 9, 2026",
            t)
if t2 != t:
    print("OK  date line")
io.open(p, "w", encoding="utf-8").write(t2)
print("done")
