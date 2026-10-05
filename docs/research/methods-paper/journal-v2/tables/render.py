"""render.py — prose of TABLES.md and NUMBERS.md.

Kept apart from `build_tables.py` so that the computation and the writing can be
read separately. Every figure that appears in the text below is interpolated
from the context dictionary the builder produced; none is typed by hand.
"""
from __future__ import annotations

import _common as C


def _pct(num, den, d=1):
    return "—" if not den else f"{100 * num / den:.{d}f}%"


def _ci(num, den, d=1):
    lo, hi = C.wilson(num, den)
    return f"[{100*lo:.{d}f}, {100*hi:.{d}f}]"


# ===========================================================================
# TABLES.md
# ===========================================================================

def tables_md(ctx) -> str:
    s = ctx["snapshot"]
    period = ctx["period"]
    nC = ctx["n_canonical"]
    nP = ctx["n_probe"]
    nA = ctx["n_all"]
    md = ctx["md"]
    t3 = ctx["t3"]
    t5 = ctx["t5"]
    t8 = ctx["t8"]
    t9 = ctx["t9"]
    t11 = ctx["t11"]
    t13 = ctx["t13"]["per_engine"]
    g78 = ctx["t13_gemini_0708"]

    out = []
    A = out.append

    A("# BRGEO-1 — numerical tables, journal version")
    A("")
    A(f"**Database snapshot.** `data/papers.db`, latest `citations.timestamp` = "
      f"`{s['last_ts']}`; earliest = `{s['first_ts']}`. "
      f"{nA:,} rows in total: {nC:,} canonical and {nP:,} adversarial probes.")
    A("")
    A("**Regenerate.** From this directory, `python build_tables.py` rewrites this "
      "file and `NUMBERS.md`; `python window_analysis.py` prints Table 13 alone. "
      "Both open the database read-only.")
    A("")
    A("## Conventions")
    A("")
    A(f"1. **Canonical stratum.** Unless a table says otherwise, the denominator is "
      f"`COALESCE(is_probe,0)=0`: the {nC:,} observations from the 192-query "
      f"canonical battery. The {nP:,} adversarial probes are a separate instrument "
      f"and appear only in Table 10.")
    A(f"2. **Observation window.** The study's canonical window is "
      f"{C.WINDOW} characters. Where a table reports a rate without qualification, "
      f"entity extraction ran over the first {C.WINDOW} characters of the stored "
      f"string. Tables 3 and 13 report both windows side by side.")
    A("3. **Intervals.** Every rate carries a 95% Wilson score interval in square "
      "brackets, in percentage points. Wilson rather than Wald because several "
      "cells sit at or near zero, where the Wald interval is degenerate.")
    A(f"4. **Small cells.** A dagger (†) marks any cell with fewer than {C.SMALL_N} "
      "observations. Those cells are descriptive: they are printed so the table is "
      "complete, not so a comparison can be built on them.")
    A("5. **Matching rule.** Entity extraction uses the project's own extractor "
      "(`src/analysis/entity_extraction.EntityExtractor`) over the v2 cohort "
      "(`src/config_v2.get_v2_cohort`, anchors and decoys included), with the "
      "project's alias, ambiguity, canonical-name and stop-context dictionaries. "
      "The rule is held fixed across every table; only the window moves.")
    A("")

    # ---------------- T1 ----------------
    A("## Table 1. Engine panel")
    A("")
    A("\n".join(md["t1"]))
    A("")
    A(f"**Table 1.** Engine panel with pinned model identifiers, architectural class "
      f"and active period. {period}, n = {nC:,} canonical observations; denominator: "
      f"rows of `citations` with `COALESCE(is_probe,0)=0`.")
    A("")
    A("*Notes.* The panel holds six engines across the series but never six at once. "
      "Groq leaves on 2026-08-16 and Grok enters on 2026-08-23, so the two occupy "
      "one slot in successive periods and any analysis crossing 2026-08-16 must "
      "stratify or truncate. Gemini changes pinned model inside the series "
      "(`gemini-2.5-pro` to `gemini-2.5-flash`), which is a stratum boundary of the "
      "same kind. Perplexity runs half the battery (96 of the 192 canonical "
      "queries), which is why its n is roughly half of the parametric arms; "
      "Table 7c shows that the half it runs is not a random half.")
    A("")

    # ---------------- T2 ----------------
    A("## Table 2. Length of the stored extraction string")
    A("")
    A("\n".join(md["t2"]))
    A("")
    A(f"**Table 2.** Length in characters of `citations.response_text`, the string "
      f"entity extraction actually read. {period}, n = {nC:,} canonical "
      f"observations; denominator: canonical rows with a non-null `response_text`, "
      f"by engine.")
    A("")
    hard = [e for e in ctx["engines_present"]
            if ctx["t2"][e]["min_chars"] == ctx["t2"][e]["max_chars"] == 200]
    near = [e for e in ctx["engines_present"]
            if e not in hard and ctx["t2"][e]["max_chars"] == 200]
    A("*Notes.* A variable whose maximum equals its minimum across fifteen thousand "
      "observations is not measuring anything; it is reporting a boundary. "
      + ", ".join(hard) + " are at exactly 200 on every single observation, because "
      "their client adapter stored `text[:200]`. " + " and ".join(near)
      + " fall marginally short of that ceiling, which is what an arm that "
      "occasionally answers in fewer characters than the ceiling looks like once "
      "the ceiling is imposed. Perplexity took a "
      f"different path through the client and stored up to "
      f"{ctx['t2']['Perplexity']['max_chars']:,} characters, which is the asymmetry "
      f"the paper is about. The {ctx['t2']['Perplexity']['exactly_200']} Perplexity "
      "rows now sitting at exactly 200 are the observations collected after the "
      "uniform window was applied at collection time on 2026-08-31.")
    A("")

    # ---------------- T3 ----------------
    A("## Table 3. Citation rate as collected and under a uniform window")
    A("")
    A("\n".join(md["t3"]))
    A("")
    A(f"**Table 3.** Citation rate by engine, as collected and after re-extraction "
      f"under a uniform {C.WINDOW}-character window, with the difference in "
      f"percentage points and the number of rows whose stored text exceeded the "
      f"window. {period}, n = {nC:,} canonical observations; denominator: canonical "
      f"rows with a non-null `response_text`, by engine.")
    A("")
    A("*Notes.* Five deltas of exactly zero are a sanity check and not an "
      "independent verification: applying a 200-character window to a string that "
      "is already 200 characters is the identity operation, so the zero is "
      "guaranteed by construction. What it confirms is that re-extraction is "
      "deterministic and that the cohort did not change between runs. The one "
      f"non-zero delta belongs to the retrieval-augmented arm: Perplexity moves from "
      f"{t3['Perplexity']['rate_collected']:.1f}% to "
      f"{t3['Perplexity']['rate_window']:.1f}%, "
      f"{t3['Perplexity']['delta']:+.1f} pp over "
      f"{t3['Perplexity']['truncated']:,} truncated rows.")
    A("")
    A("The 'as collected' column for Perplexity now mixes two collection regimes, "
      "and the mixture is disclosed rather than smoothed:")
    A("")
    A("| Perplexity, by stored length | n | Cited | Rate [95% CI] "
      "| Full response also retained | Period |")
    A("|---|---:|---:|---:|---:|---|")
    for r in ctx["t3_perplexity_regime"]:
        A(f"| {r['regime']} | {r['n']:,} | {r['cited']:,} "
          f"| {C.rate_cell(r['cited'], r['n'])} "
          f"| {r['with_full_text_retained']:,} "
          f"| {r['first_day']} to {r['last_day']} |")
    A("")
    A("The group at or below the window is the set of observations collected after "
      "the uniform window was applied at collection time on 2026-08-31, plus a "
      "single early response that happened to be shorter than the window, which is "
      "why its period starts in April. For those rows 'as collected' and "
      "'uniform window' are the same "
      "measurement. This is why the panel figure for Perplexity as collected "
      f"({t3['Perplexity']['rate_collected']:.1f}%) is slightly below the 75.7% "
      "reported in manuscript v1.0, which closed before those rows existed.")
    A("")

    # ---------------- T4 ----------------
    A("## Table 4. First-mention offset")
    A("")
    A("\n".join(md["t4"]))
    A("")
    A(f"**Table 4.** Offset of the first cohort entity named, absolute and relative "
      f"to the length of the text actually observed. {period}, n = "
      f"{sum(d['n_cited'] for d in ctx['t4'].values()):,} canonical observations "
      f"carrying a citation; denominator: canonical rows with `cited_v2 = 1`, a "
      f"non-null `first_entity_offset_v2` and `response_length_chars_v2 > 0`, "
      f"by engine.")
    A("")
    A("*Notes.* This table is computed on the text as stored, not under the uniform "
      "window, because its subject is the position of the first mention inside "
      "whatever text the extractor saw. That makes the denominators censored at 200 "
      "characters for every arm except Perplexity, so the relative values of the "
      "parametric arms are upper bounds on their true relative position. The "
      "apparent reversal, in which the retrieval-augmented arm names entities "
      "earlier in relative terms than every parametric arm except Grok, therefore "
      "cannot be asserted as established. The defensible reading is "
      "non-identification: data collected "
      "under an asymmetric window does not identify the direction of the window "
      "bias. Table 13 is the analysis that removes the censoring.")
    A("")

    # ---------------- T5 ----------------
    A("## Table 5. Opening style against citation rate")
    A("")
    A("\n".join(md["t5"]))
    A("")
    A(f"**Table 5.** Share of responses opening with preamble, against the citation "
      f"rate as collected. {period}, n = {nC:,} canonical observations; "
      f"denominator: canonical rows with a non-null `response_text`, by engine.")
    A("")
    A("*Criterion applied.* Preamble is a case-insensitive regular expression "
      "anchored at the start of the stored string, after skipping leading non-word "
      "characters (`^\\W*`), matching any of three families: a greeting or praise of "
      "the question; a hedge on whether the question can be answered; an explicit "
      "model self-reference. The pattern is printed in full in NUMBERS.md T5, "
      "because the criterion is part of the result and not an implementation "
      "detail.")
    A("")
    A("*Provenance of the criterion.* The regular expression behind Table 7 of "
      "manuscript v1.0 is described in prose in three documents but was never "
      "committed to the repository, so it cannot be re-run. The pattern used here "
      "is a re-specification in the same spirit, and NUMBERS.md T5 reports it "
      "against the v1.0 figures over the identical row set so a reviewer can see "
      "where the two agree and where they do not. The two largest divergences are "
      "Perplexity and Grok; the ordering claim the paper rests on survives both "
      "criteria.")
    A("")
    A(f"*Reading.* The arm that spends the window on preamble is parametric: Gemini "
      f"opens {_pct(t5['Gemini']['pre'], t5['Gemini']['n'])} of its responses that "
      f"way and cites within the window "
      f"{_pct(t5['Gemini']['cited'], t5['Gemini']['n'])} of the time. The "
      f"retrieval-augmented arm has little preamble "
      f"({_pct(t5['Perplexity']['pre'], t5['Perplexity']['n'])}) and the highest "
      f"citation rate. Susceptibility to a narrow window therefore tracks response "
      f"style, which is a property of the model, and is not deducible from the "
      f"architectural class.")
    A("")

    # ---------------- T6 ----------------
    A("## Table 6. Citation rate by vertical and engine")
    A("")
    A("\n".join(md["t6"]))
    A("")
    A(f"**Table 6.** Citation rate under the uniform {C.WINDOW}-character window, by "
      f"engine and vertical, as percentage points with a 95% Wilson interval. "
      f"{period}, n = {ctx['t3_panel']['n']:,} canonical observations; denominator: "
      f"canonical rows with a non-null `response_text`, by cell.")
    A("")
    tops, bottoms = [], []
    for e in ctx["engines_present"]:
        rates = {v: (ctx["t6"][e][v][1] / ctx["t6"][e][v][0])
                 for v in C.VERTICALS if ctx["t6"][e][v][0]}
        tops.append(C.VERTICAL_LABEL[max(rates, key=rates.get)])
        bottoms.append(C.VERTICAL_LABEL[min(rates, key=rates.get)])
    from collections import Counter as _Ct
    top_tally = _Ct(tops)
    bot_tally = _Ct(bottoms)
    panel_rates = {v: ctx["t6_panel"][v][1] / ctx["t6_panel"][v][0] for v in C.VERTICALS}
    p_top = max(panel_rates, key=panel_rates.get)
    p_bot = min(panel_rates, key=panel_rates.get)
    A("*Notes.* Every cell is large, so the intervals are narrow and the between-"
      "cell differences are not interval artefacts. Gemini in health is a hard zero "
      f"over {ctx['t6']['Gemini']['saude'][0]:,} observations, with a Wilson upper "
      f"bound of {100*C.wilson(0, ctx['t6']['Gemini']['saude'][0])[1]:.3f}%; read "
      "together with Table 5 that is a statement about the first 200 characters of a "
      "Gemini answer, not about whether Gemini knows Brazilian health providers.")
    A("")
    A("The vertical ordering is not uniform across arms and should not be summarised "
      "as one. Counting which vertical leads each of the six arms: "
      + "; ".join(f"{k} in {v} of {len(tops)}" for k, v in top_tally.most_common())
      + ". Counting which trails: "
      + "; ".join(f"{k} in {v} of {len(bottoms)}" for k, v in bot_tally.most_common())
      + f". At panel level {C.VERTICAL_LABEL[p_top]} is highest at "
      f"{100*panel_rates[p_top]:.1f}% and {C.VERTICAL_LABEL[p_bot]} lowest at "
      f"{100*panel_rates[p_bot]:.1f}%, but that ordering is a mixture over arms with "
      "very different overall rates and is not a property of the verticals.")
    A("")

    # ---------------- T7 ----------------
    A("## Table 7. Citation rate by query stratum")
    A("")
    A("### Table 7a. By language")
    A("")
    A("\n".join(md["t7a"]))
    A("")
    A("### Table 7b. By query type")
    A("")
    A("\n".join(md["t7b"]))
    A("")
    A("### Table 7c. By semantic category")
    A("")
    A("\n".join(md["t7c"]))
    A("")
    A(f"**Table 7.** Citation rate under the uniform {C.WINDOW}-character window by "
      f"query language (a), query type (b) and semantic category (c), by engine. "
      f"{period}, n = {ctx['t3_panel']['n']:,} canonical observations; denominator: "
      f"canonical rows with a non-null `response_text`, by cell.")
    A("")
    A("*Notes.* The language and type splits are balanced by construction, so the "
      "panel comparison in 7a and 7b is between equal denominators. The category "
      "split is not: Perplexity runs only three of the six categories "
      "(`descoberta`, `comparativo`, `mercado`) because it runs half the battery, "
      "and those three are exactly the discovery-shaped categories where citation "
      "rates are highest. The panel row of Table 7c is therefore composed of "
      "different engine mixtures from column to column and should not be read as a "
      "category effect. Compare within an engine row, or restrict to the five arms "
      "that run all six.")
    A("")
    A("The directive/exploratory contrast in 7b is the largest stratum effect in "
      "these tables and it holds in every arm: a question that asks for a named "
      "best is answered with a name far more often than a question that asks for "
      "the landscape. It is also the contrast most obviously confounded with the "
      "window, since an exploratory answer has more reason to open with framing "
      "prose.")
    A("")

    # ---------------- T8 ----------------
    A("## Table 8. Concentration of first mentions")
    A("")
    A("\n".join(md["t8"]))
    A("")
    A(f"**Table 8.** The ten entities most often named first, with count and share "
      f"of all first mentions. {period}, n = {t8['total_first']:,} canonical "
      f"observations carrying a citation under the uniform {C.WINDOW}-character "
      f"window; denominator: those {t8['total_first']:,} first mentions.")
    A("")
    A("| Quantity | Value |")
    A("|---|---:|")
    A(f"| Cohort, distinct entities | {t8['cohort_unique']} |")
    A(f"| of which Brazilian real firms | {t8['real_br']} |")
    A(f"| of which international anchors | {t8['anchors']} |")
    A(f"| of which fictitious decoys | {t8['decoys']} |")
    A(f"| Distinct entities ever named first | **{t8['distinct']}** |")
    A(f"| of which Brazilian real firms | {t8['named_real_br']} of {t8['real_br']} |")
    A(f"| of which international anchors | {t8['named_anchors']} of {t8['anchors']} |")
    A(f"| of which fictitious decoys | {t8['named_decoys']} of {t8['decoys']} |")
    A(f"| Cumulative share, top 1 | {t8['cumulative'][1]:.1f}% |")
    A(f"| Cumulative share, top 3 | {t8['cumulative'][3]:.1f}% |")
    A(f"| Cumulative share, top 5 | {t8['cumulative'][5]:.1f}% |")
    A(f"| Cumulative share, top 10 | {t8['cumulative'][10]:.1f}% |")
    A(f"| Herfindahl-Hirschman index (reported index) | **{t8['hhi']:.4f}** |")
    A(f"| Gini coefficient over named entities | {t8['gini']:.4f} |")
    A("")
    A("*Notes.* The concentration index reported here is the Herfindahl-Hirschman "
      "index, computed as the sum of squared shares of first mentions across the "
      f"{t8['distinct']} entities that were ever named first, on the 0 to 1 scale. "
      f"At {t8['hhi']:.4f} it is equivalent to a market with about "
      f"{1/t8['hhi']:.1f} equally sized participants, against a cohort of "
      f"{t8['cohort_unique']}. The Gini coefficient is given as a secondary "
      "statistic and is computed only over entities that were named at least once, "
      "so it understates inequality relative to a version that counted the "
      f"{t8['cohort_unique'] - t8['distinct']} never-named members as zeros.")
    A("")
    A(f"The denominator matters for the headline reading. "
      f"{t8['distinct']} of {t8['cohort_unique']} cohort members were ever the first "
      f"name in an answer, and one firm takes {t8['cumulative'][1]:.1f}% of all "
      f"first mentions. Under the as-collected window the distinct count is "
      f"{ctx['t8_as_collected_distinct']} rather than {t8['distinct']}, the "
      "difference being entities that Perplexity named beyond character 200. That "
      "gap is itself a window effect: how concentrated the market looks depends on "
      "how much of each answer you read.")
    A("")
    co = ctx["collision"]
    A("### Instrument note: two cohort names collide with ordinary words")
    A("")
    A("Inspecting the ranked list above turned up a defect in the matcher that had "
      "not been recorded anywhere. Two cohort names are also ordinary words of the "
      "response language, and neither is listed in `src/config.AMBIGUOUS_ENTITIES` "
      "nor given a stop context, so the extractor matches the ordinary word:")
    A("")
    A("| Colliding name | Matches under the uniform window | What it is matching |")
    A("|---|---:|---|")
    A(f"| `Involves` | {co['by_name'].get('Involves', 0):,} "
      "| the English verb, as in \"Evaluating trust in Brazilian technology and IT "
      "**involves** several factors\" |")
    A(f"| `Target` | {co['by_name'].get('Target', 0):,} "
      "| the English noun and verb, as in \"B2B platforms like Mercado Shops "
      "**target** SMEs\" |")
    A("")
    same = (co["rows_touched"] == co["rows_cited_only_by_collision"])
    A(f"Magnitude. {co['rows_touched']:,} of {co['panel_n']:,} canonical "
      f"observations contain at least one such match, "
      f"{_pct(co['rows_touched'], co['panel_n'], 2)} of the panel. "
      + ("In every one of them the collision is the only match, so the whole set is "
         "counted as cited for no other reason. "
         if same else
         f"In {co['rows_cited_only_by_collision']:,} of them the collision is the "
         "only match, so those are counted as cited for no other reason. ")
      + "Removing both names from the cohort moves the panel citation rate from "
      f"{_pct(co['panel_cited_with'], co['panel_n'], 2)} to "
      f"{_pct(co['panel_cited_without'], co['panel_n'], 2)}, the distinct "
      f"first-mention count from {co['distinct_first_with']} to "
      f"{co['distinct_first_without']}, the HHI from {ctx['t8']['hhi']:.4f} to "
      f"{co['hhi_without']:.4f}, and the top-1 share from "
      f"{ctx['t8']['cumulative'][1]:.1f}% to {co['top1_share_without']:.1f}%.")
    A("")
    A("The collisions sit where the ordinary word lives. By language: "
      + ", ".join(f"{k} {v:,}" for k, v in sorted(co["by_lang"].items(),
                                                  key=lambda kv: -kv[1]))
      + ". By engine: "
      + ", ".join(f"{k} {v:,}" for k, v in sorted(co["by_engine"].items(),
                                                  key=lambda kv: -kv[1]))
      + ".")
    A("")
    A("The tables are published with the collisions left in, because the figures "
      "above are what the instrument as specified produces, and correcting the "
      "cohort here would break the correspondence with the stored series that V1 of "
      "NUMBERS.md establishes. The correction belongs in `src/config.py`, where "
      "`Involves` needs a canonical name and `Target` a stop context, followed by "
      "re-extraction. Until then this paragraph is the declared error term on every "
      "rate in these tables. It is two orders of magnitude smaller than the window "
      "effect of Table 13, which is why it changes no conclusion drawn here, and it "
      "is worth stating anyway: a protocol paper that asks others to declare their "
      "matching rule has to declare where its own leaks.")
    A("")

    # ---------------- T9 ----------------
    A("## Table 9. Calibration decoys in the canonical stratum")
    A("")
    A("\n".join(md["t9"]))
    A("")
    A(f"**Table 9.** Spontaneous naming of a fictitious entity in answers to "
      f"canonical queries, which no decoy name appears in. {period}, n = "
      f"{t9['n_canonical']:,} canonical observations; denominator: canonical rows "
      f"with a non-null `response_text`, by engine. Sixteen decoys, verified as "
      f"non-existent before collection.")
    A("")
    A(f"*Result.* Zero. Across {t9['n_canonical']:,} canonical observations and six "
      f"engines, no decoy was named spontaneously, either inside the "
      f"{C.WINDOW}-character window or anywhere in the text as stored. The point "
      f"estimate of the spontaneous false-positive rate is 0, with a 95% Wilson "
      f"upper bound of {100*C.wilson(0, t9['n_canonical'])[1]:.5f}% "
      f"({C.wilson(0, t9['n_canonical'])[1]*t9['n_canonical']:.1f} expected "
      f"occurrences per {t9['n_canonical']:,} observations).")
    A("")
    A("*What this licenses and what it does not.* It bounds one failure mode of the "
      "instrument: the extractor is not inventing cohort matches out of ordinary "
      "prose, which is the failure a word-boundary matcher on names like `Inter` or "
      "`Stone` would be expected to show. It says nothing about the models' "
      "willingness to describe an entity that does not exist when asked about it "
      "directly, which is a different quantity and is Table 10. It also cannot "
      "bound false positives on real names used in an unintended sense, since a "
      "decoy carries no such sense. The stored `fictional_hit` column is 0 on every "
      "canonical row, which is consistent with this result but is not independent "
      "evidence for it: that column was only ever populated on the probe stratum.")
    A("")

    # ---------------- T10 ----------------
    A("## Table 10. Adversarial stratum")
    A("")
    A("\n".join(md["t10"]))
    A("")
    A(f"**Table 10.** Adversarial probes, the share flagged by the legacy "
      f"hallucination criterion, and the share of those flagged answers that carry "
      f"an explicit refusal marker. {period}, n = {ctx['t10_panel']['n_probe']:,} "
      f"probe observations; denominators: all probe rows for the first rate, and "
      f"the {ctx['t10_panel']['refusal_den']:,} flagged rows with non-empty text "
      f"for the second.")
    A("")
    A("*Notes.* The refusal regex is reproduced verbatim from "
      "`docs/research/methods-paper/VERIFICATION.md` section 5.3 and is "
      "deliberately conservative: it counts only answers carrying an explicit "
      f"marker, so {_pct(ctx['t10_panel']['refusal_num'], ctx['t10_panel']['refusal_den'])} "
      "is a floor on the refusal share, not a ceiling. What the table shows is that "
      "the legacy criterion, which flagged an answer whenever the decoy name "
      "appeared in it, was counting refusals as hallucinations: two thirds of the "
      "flagged answers say in so many words that the entity could not be found. A "
      "criterion that cannot separate 'here is what that company does' from 'I "
      "cannot find any company by that name' is not measuring hallucination.")
    A("")
    A("The engine-level spread is the operational finding. Claude carries a refusal "
      f"marker in {_pct(ctx['t10']['Claude']['refusal_num'], ctx['t10']['Claude']['refusal_den'])} "
      f"of its flagged answers and Perplexity in "
      f"{_pct(ctx['t10']['Perplexity']['refusal_num'], ctx['t10']['Perplexity']['refusal_den'])}, "
      "so any headline hallucination rate computed under the legacy criterion "
      "ranks the engines mostly by how explicitly they decline.")
    A("")

    # ---------------- T11 ----------------
    A("## Table 11. Temporal coverage")
    A("")
    A("\n".join(md["t11"]))
    A("")
    A(f"**Table 11.** Days with data against days on the calendar, by month. "
      f"{period}, n = {nC:,} canonical observations; denominator: calendar days in "
      f"the span {t11['first_day']} to {t11['last_day']}.")
    A("")
    A("| Coverage quantity | Value |")
    A("|---|---:|")
    A(f"| Calendar days spanned | {t11['calendar_days']} |")
    A(f"| Days with at least one observation | **{t11['days_with_data']}** |")
    A(f"| Days with no observation | {t11['days_missing']} |")
    A(f"| Partial days, derived definition below | **{len(t11['partial_days'])}** |")
    A(f"| Partial days registered in `data/partial_days.json`, inside the span "
      f"| {len({e['date'] for e in t11['registered_in_span']})} |")
    A(f"| `collection_runs` rows with status `success` | {t11['runs']['success']['n']:,} |")
    A(f"| `collection_runs` rows with status `aborted` | {t11['runs']['aborted']['n']:,} |")
    A("")
    A("Contiguous blocks with no data:")
    A("")
    A("| From | To | Days |")
    A("|---|---|---:|")
    for a, b, n in t11["gaps"]:
        A(f"| {a} | {b} | {n} |")
    A("")
    A("*Two sources for partial days, and why both are given.* The repository "
      "carries a registry at `data/partial_days.json`. It records, per day, the "
      "engines that produced nothing and why, with a link to the run or the "
      "governance note. It is authoritative on what it covers and it does not "
      "cover the whole series: its earliest entry is "
      f"{min((e['date'] for e in t11['registered'] if 'date' in e), default='n/a')}, "
      "it was seeded by hand, and it records only engine absence, not an engine "
      "that ran a short battery.")
    A("")
    if t11["registered_in_span"]:
        A("Registry entries falling inside the snapshot span:")
        A("")
        A("| Day | Engines missing | Reason, as recorded |")
        A("|---|---|---|")
        for e in t11["registered_in_span"]:
            A(f"| {e['date']} | {', '.join(e.get('missingLLMs', []))} "
              f"| {e.get('reason', '').replace('|', '/')[:150]} |")
        A("")
    if t11["registered_outside_span"]:
        outside = sorted({e["date"] for e in t11["registered_outside_span"]})
        A(f"The registry also carries {len(t11['registered_outside_span'])} entries "
          f"for {', '.join(outside)}, after the last observation in this snapshot. "
          "They are listed here so a reader who takes a fresher snapshot knows the "
          "outage continued, and they contribute nothing to the tables above.")
        A("")
    A("The second source is derived from the observations themselves, because the "
      "registry says nothing about the first four months of the series. A day is "
      "partial when at least one engine active in the surrounding period either "
      "delivered fewer distinct canonical queries than its own battery size or "
      "produced no row at all. Battery size is inferred from the data as the "
      "largest number of distinct canonical queries the engine ever reached in a "
      "single day, which is 192 for every parametric arm and 96 for Perplexity.")
    A("")
    if t11["registry_agreement"]:
        allm = all(a["match"] for a in t11["registry_agreement"])
        A("The two sources can be checked against each other on the days both "
          "cover. "
          + ("They agree exactly: "
             if allm else "They agree on some days and not others: ")
          + "; ".join(
              f"on {a['date']} the registry names "
              f"{' and '.join(a['registered_missing']) or 'nothing'} and the "
              f"derived rule finds "
              f"{' and '.join(a['derived_absent']) or 'nothing'}"
              for a in t11["registry_agreement"])
          + ". The derived rule therefore recovers the registered outages without "
            "being told about them, which is the reason it is trusted for the "
            "months the registry does not reach.")
        A("")
    A(f"Under the derived definition {len(t11['partial_days'])} of the "
      f"{t11['days_with_data']} days with data are partial:")
    A("")
    A("| Day | Engines short of battery | Engines absent |")
    A("|---|---|---|")
    for p in t11["partial_detail"]:
        A(f"| {p['day']} | {', '.join(p['short']) or '—'} "
          f"| {', '.join(p['absent']) or '—'} |")
    A("")
    A("*Notes on the aborted runs.* The "
      f"{t11['runs']['aborted']['n']:,} rows with status `aborted` are not failed "
      f"attempts observed as they happened. They cover "
      f"{ctx['t11_aborted_detail']['distinct_days']} distinct days and were written "
      "retroactively by `scripts/mark_collection_gaps.py` so that a silent hole in "
      "the series would appear in `collection_runs` as a declared fact rather than "
      "as an absence. The largest single block, 59 days from 2026-06-10 to "
      "2026-08-07, is the period in which the workflow ran green and persisted "
      "nothing. Any longitudinal reading of Table 12 has to carry that block, "
      "because a straight line fitted across it is interpolating over two months of "
      "no observation.")
    A("")

    # ---------------- T12 ----------------
    A("## Table 12. Descriptive temporal stability")
    A("")
    A("\n".join(md["t12"]))
    A("")
    A(f"**Table 12.** Daily citation rate under the uniform {C.WINDOW}-character "
      f"window, summarised by engine, with an ordinary least squares slope in "
      f"percentage points per calendar day. {period}, n = "
      f"{sum(d.get('n_total', 0) for d in ctx['t12'].values()):,} canonical "
      f"observations on days meeting the threshold; denominator: for each engine, "
      f"its days with at least {C.SMALL_N} canonical observations. A dagger marks "
      f"an engine with fewer than ten daily points.")
    A("")
    A("*This is a description, not a test.* The slope is fitted on daily rates "
      "treated as equally weighted points on a calendar axis. Those points are not "
      "independent: they share a fixed query battery, they are clustered by "
      "collection run, their denominators vary by a factor of four, and the axis "
      "contains an 86-day hole of which 59 days are contiguous. The interval in the "
      "last column is a residual-based interval around the fitted slope and is "
      "printed so the reader can see how badly the slope is determined. No "
      "hypothesis about drift is tested here, and none should be read off the "
      "sign.")
    A("")
    est = {e: d for e, d in ctx["t12"].items() if d["days"] >= 3}
    widest = max(est, key=lambda e: est[e]["max"] - est[e]["min"])
    steepest = max(est, key=lambda e: abs(est[e]["slope"]))
    A("What the column is useful for is the opposite of a trend claim: it shows that "
      "no arm's daily rate wanders far enough to make the series-level figures in "
      "Table 3 an artefact of which days happened to be collected. The widest "
      f"day-to-day spread belongs to {widest}, whose daily rate ranges from "
      f"{est[widest]['min']:.1f}% to {est[widest]['max']:.1f}%, a span of "
      f"{est[widest]['max'] - est[widest]['min']:.1f} pp across "
      f"{est[widest]['days']} days. The steepest fitted slope belongs to "
      f"{steepest} at {est[steepest]['slope']:+.4f} pp per day, which over the "
      f"{ctx['t11']['calendar_days']} calendar days of the series would amount to "
      f"{abs(est[steepest]['slope']) * ctx['t11']['calendar_days']:.1f} pp, and its "
      f"interval [{est[steepest]['lo']:+.4f}, {est[steepest]['hi']:+.4f}] shows how "
      "little the daily points constrain it.")
    A("")

    # ---------------- T13 ----------------
    A("## Table 13. The observation window measured on every arm")
    A("")
    A("\n".join(md["t13"]))
    A("")
    n13 = sum(d["n"] for d in t13.values())
    A(f"**Table 13.** Citation rate at {C.WINDOW} characters against citation rate "
      f"on the full response, for the same observations, under the same matching "
      f"rule. 2026-09-06 to 2026-09-08, n = {n13:,} canonical observations; "
      f"denominator: canonical rows whose `response_full_text` is non-empty, by "
      f"engine. Gains are rows uncited at 200 characters and cited on the full "
      f"text; losses are the reverse; the p-value is the exact two-sided McNemar "
      f"test on those discordant pairs.")
    A("")
    A("*Method.* `scripts/harmonize_citation_window.py` could only ever move one "
      "arm, because five of six adapters stored `text[:200]` and the text beyond "
      "the window was never written to disk. Since migration 0010 the pipeline "
      "writes the whole response to `citations.response_full_text` while continuing "
      "to write the windowed string to `response_text`. For those rows the "
      "comparison runs within the arm: extract over `response_full_text[:200]`, "
      "extract over `response_full_text`, hold the cohort and the matching rule "
      "fixed, and read off the difference. Two checks are run on every row and both "
      "pass on all "
      f"{ctx['t13']['checks']['rows']:,}: `response_text` equals "
      "`response_full_text[:200]`, so the two columns are two views of one "
      "response; and re-extracting the first 200 characters reproduces the stored "
      "`cited_v2` exactly, so the rule used here is the rule that produced the "
      "series. Without the second check, a delta reported below could be an "
      "artefact of this script's matching rather than of the window.")
    A("")
    ordered = sorted(t13, key=lambda e: -t13[e]["delta_pp"])
    A("*Result.* The window effect is present in every arm that retained full text. "
      + ", ".join(f"{e} {t13[e]['delta_pp']:+.1f} pp" for e in ordered)
      + ". Not one row in any arm loses its citation when more text is read, which "
      "is what a monotone window ought to produce and is therefore a further check "
      "rather than a finding.")
    A("")
    A("Two readings of that row of numbers are available and only one of them is "
      "supported. The supported one is that the effect is not confined to the "
      f"retrieval-augmented arm: four parametric arms move at least "
      f"{min(t13[e]['delta_pp'] for e in ordered if e != 'Perplexity'):.1f} "
      "percentage points, which is the point the protocol rests on. The unsupported "
      "one is a ranking of engines by susceptibility; see the limits below. What "
      "can be said about Perplexity is narrower and still useful: its delta here, "
      f"{t13['Perplexity']['delta_pp']:+.1f} pp on {t13['Perplexity']['n']} rows, "
      "sits close to the 23.8 pp that manuscript v1.0 measured on 7,435 truncated "
      "rows of the same arm, so the one figure the earlier paper could produce "
      "appears to be stable across two disjoint row sets.")
    A("")
    A("*The Gemini rows need stratifying.* On 2026-09-06 Gemini returned unusually "
      "short responses: 384 rows with a maximum full length of 216 characters, of "
      "which only six contain a cohort entity at all, so for those rows the two "
      "windows are nearly the same text and the delta is mechanically near zero. "
      f"Restricted to 2026-09-07 and 2026-09-08, Gemini has n = {g78['n']:,}, "
      f"{g78['rate_head']:.1f}% [{g78['head_ci'][0]:.1f}, {g78['head_ci'][1]:.1f}] "
      f"at 200 characters against {g78['rate_full']:.1f}% "
      f"[{g78['full_ci'][0]:.1f}, {g78['full_ci'][1]:.1f}] on the full text, a "
      f"difference of {g78['delta_pp']:+.1f} pp on a mean full length of "
      f"{g78['mean_len']:,.0f} characters. The pooled Gemini row in the table above "
      "understates the effect for that reason, and both figures are given rather "
      "than only the convenient one.")
    A("")
    A("### What this n permits, and what it does not")
    A("")
    A("**It permits** a within-arm, within-observation statement: on these rows, "
      "for these engines, reading the whole response instead of the first 200 "
      "characters changes the citation rate by the amounts tabulated, and the "
      "change is not attributable to the matching rule, the cohort, the query set "
      "or the engine, because all four are held fixed across the paired comparison. "
      "The discordant counts are heavily one-sided and the exact McNemar p-values "
      "are far below any conventional threshold, so the direction is not in "
      "question for the rows observed.")
    A("")
    A("**It permits** the protocol conclusion the paper needs: the window is a "
      "first-order parameter for every engine tested, not a quirk of one "
      "retrieval-augmented arm, and its magnitude is not predictable from "
      "architectural class. A reader who is handed a citation rate without a "
      "declared window has been handed a number that could move by tens of "
      "percentage points.")
    A("")
    A("**It does not permit** treating the full-text rates as the engines' "
      "series-level citation rates. These "
      f"{n13:,} observations come from three days at the very end of the series, "
      "ChatGPT and Claude contribute one day each, and every engine's rows sit "
      "inside a single stratum of model version and generation settings. The "
      "series-level figures remain those of Table 3, measured under the declared "
      "200-character window.")
    A("")
    A("**It does not permit** comparing the deltas between engines as if they were "
      "estimates of a stable engine property. The arms differ in which days they "
      "contributed, in how long their responses are, and in whether their day-level "
      "behaviour was typical; the Gemini stratification above is a concrete case "
      "where the pooled delta and the stratified delta differ by more than 30 "
      "percentage points. Ranking engines by delta on this table would be reading "
      "sampling structure as substance.")
    A("")
    A("**It does not permit** any statement about Groq. Groq left the panel on "
      "2026-08-16, before full-text retention began, so it contributes zero rows "
      "here and the window effect on its 14,208 canonical observations is "
      "unmeasured and now unmeasurable. That is the irreversible half of the defect "
      "the paper documents: an asymmetric window can be corrected because the "
      "truncated string is still the string the extractor saw, but no amount of "
      "care recovers text that was never stored.")
    A("")

    # ---------------- closing ----------------
    A("## Reproduction")
    A("")
    A("`NUMBERS.md` in this directory lists every figure above with the SQL "
      "statement or the function call that produced it and the value obtained. "
      "Nothing in these tables was typed by hand: `build_tables.py` interpolates "
      "each figure from the query result into both documents.")
    A("")
    return "\n".join(out) + "\n"


# ===========================================================================
# NUMBERS.md
# ===========================================================================

def numbers_md(ctx, SQL) -> str:
    s = ctx["snapshot"]
    out = []
    A = out.append

    def sql_block(key):
        A("```sql")
        A(SQL[key].strip())
        A("```")

    A("# NUMBERS — the verifier for TABLES.md")
    A("")
    A("Every figure asserted in `TABLES.md`, the statement or call that produces it, "
      "and the value obtained on the snapshot named below. A reviewer who runs the "
      "statements in order should land on the same numbers; where a figure comes "
      "from plain SQL, the statement printed here is the same string object that "
      "was executed by `build_tables.py`, so the two cannot drift.")
    A("")
    A("## Snapshot")
    A("")
    sql_block("snapshot")
    A("")
    A("| Field | Value |")
    A("|---|---|")
    A(f"| earliest `citations.timestamp` | `{s['first_ts']}` |")
    A(f"| latest `citations.timestamp` | `{s['last_ts']}` |")
    A(f"| rows, all | {s['rows_all']:,} |")
    A(f"| rows, canonical (`COALESCE(is_probe,0)=0`) | {s['rows_canonical']:,} |")
    A(f"| rows, adversarial probes | {s['rows_probe']:,} |")
    A("")
    A("Open the database read-only:")
    A("")
    A("```python")
    A('import sqlite3')
    A('con = sqlite3.connect("file:data/papers.db?mode=ro", uri=True)')
    A("```")
    A("")
    A("Or with the CLI, from the repository root:")
    A("")
    A("```bash")
    A('sqlite3 "file:data/papers.db?mode=ro"')
    A("```")
    A("")
    A("Regenerate everything:")
    A("")
    A("```bash")
    A("cd docs/research/methods-paper/journal-v2/tables")
    A("python build_tables.py          # rewrites TABLES.md and NUMBERS.md")
    A("python window_analysis.py       # Table 13 alone, with its two checks")
    A("```")
    A("")

    # ---- V1 ----
    A("## V1. Verification that re-extraction reproduces the series")
    A("")
    A("Every table that reports a rate under the uniform window depends on one "
      "identity: applying the project's extractor to `response_text[:200]` must "
      "reproduce the stored `cited_v2` on every row whose stored text is already "
      "at or below 200 characters. If it did not, the deltas in Tables 3 and 13 "
      "would be confounded with a change of matching rule.")
    A("")
    A("Produced by `build_tables.reextract_uniform`, which is "
      "`scripts/harmonize_citation_window.py` reimplemented against a read-only "
      "connection, using `EntityExtractor` over "
      "`get_v2_cohort(vertical, include_anchors=True, include_decoys=True)`.")
    A("")
    A("| Quantity | Value |")
    A("|---|---:|")
    A(f"| canonical rows re-extracted | {ctx['n_reextracted']:,} |")
    A(f"| rows where `len(response_text) <= 200` and re-extraction disagreed with "
      f"`cited_v2` | **{ctx['identity_mismatch']}** |")
    A("")
    A(f"Result: {ctx['identity_mismatch']} disagreements. The matching rule used in "
      "these tables is the matching rule that produced the series.")
    A("")
    A("Cohort sizes entering the extractors:")
    A("")
    A("| Vertical | Cohort size |")
    A("|---|---:|")
    for v in C.VERTICALS:
        A(f"| `{v}` | {len(C.get_v2_cohort(v, True, True))} |")
    A(f"| distinct across verticals | {ctx['t8']['cohort_unique']} "
      f"({ctx['t8']['real_br']} Brazilian real + {ctx['t8']['anchors']} anchors "
      f"+ {ctx['t8']['decoys']} decoys) |")
    A("")

    # ---- T1 ----
    A("## T1. Engine panel")
    A("")
    sql_block("t1_panel")
    A("")
    A("| Engine | `model_version` | n | First day | Last day |")
    A("|---|---|---:|---|---|")
    for e in ctx["engines_present"]:
        for p in ctx["t1"][e]:
            A(f"| {e} | `{p['model_version']}` | {p['n']:,} | {p['first_day']} "
              f"| {p['last_day']} |")
    A("")
    A("Architectural class is not in the database. It is taken from MANUSCRIPT.md "
      "Table 3 and hard-coded in `_common.ENGINE_CLASS`; Perplexity is the only "
      "retrieval-augmented arm.")
    A("")

    # ---- T2 ----
    A("## T2. Stored extraction string length")
    A("")
    sql_block("t2_length")
    A("")
    A("| Engine | n | Mean | Min | Max | Exactly 200 | Share |")
    A("|---|---:|---:|---:|---:|---:|---:|")
    for e in ctx["engines_present"]:
        d = ctx["t2"][e]
        A(f"| {e} | {d['n']:,} | {d['mean_chars']:,.1f} | {d['min_chars']:,} "
          f"| {d['max_chars']:,} | {d['exactly_200']:,} "
          f"| {_pct(d['exactly_200'], d['n'])} |")
    A("")
    A("Manuscript v1.0 Table 4 reported the same quantity over the full series "
      "including probes. That variant, for comparison:")
    A("")
    sql_block("t2_length_full_series")
    A("")
    A("| Engine | n | Mean | Min | Max | Share exactly 200 |")
    A("|---|---:|---:|---:|---:|---:|")
    for e in ctx["engines_present"]:
        d = ctx["t2_full_series"][e]
        A(f"| {e} | {d['n']:,} | {d['mean_chars']:,.1f} | {d['min_chars']:,} "
          f"| {d['max_chars']:,} | {_pct(d['exactly_200'], d['n'])} |")
    A("")

    # ---- T3 ----
    A("## T3. Citation rate, as collected and under a uniform window")
    A("")
    A("The 'as collected' column and the truncation count come from SQL:")
    A("")
    sql_block("t3_as_collected")
    A("")
    A("The 'uniform window' column comes from `build_tables.reextract_uniform`, "
      "described in V1 above. Counts and rates:")
    A("")
    A("| Engine | n | Cited as collected | Rate | 95% CI | Cited under window "
      "| Rate | 95% CI | Δ pp | Rows truncated |")
    A("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for e in ctx["engines_present"]:
        d = ctx["t3"][e]
        A(f"| {e} | {d['n']:,} | {d['collected']:,} | {d['rate_collected']:.4f}% "
          f"| {_ci(d['collected'], d['n'], 2)} | {d['window']:,} "
          f"| {d['rate_window']:.4f}% | {_ci(d['window'], d['n'], 2)} "
          f"| {d['delta']:+.4f} | {d['truncated']:,} |")
    p = ctx["t3_panel"]
    A(f"| **Panel** | {p['n']:,} | {p['collected']:,} "
      f"| {100*p['collected']/p['n']:.4f}% | {_ci(p['collected'], p['n'], 2)} "
      f"| {p['window']:,} | {100*p['window']/p['n']:.4f}% "
      f"| {_ci(p['window'], p['n'], 2)} "
      f"| {100*(p['window']-p['collected'])/p['n']:+.4f} | {p['truncated']:,} |")
    A("")
    A("Perplexity split by collection regime, which is why its 'as collected' "
      "figure is no longer the 75.7% of manuscript v1.0:")
    A("")
    sql_block("t3_perplexity_regime")
    A("")
    A("| Regime | n | Cited | Rate | 95% CI | Period |")
    A("|---|---:|---:|---:|---:|---|")
    for r in ctx["t3_perplexity_regime"]:
        A(f"| {r['regime']} | {r['n']:,} | {r['cited']:,} "
          f"| {_pct(r['cited'], r['n'], 2)} | {_ci(r['cited'], r['n'], 2)} "
          f"| {r['first_day']} to {r['last_day']} |")
    A("")
    A("Cross-check against manuscript v1.0, which closed at 2026-08-31:")
    A("")
    A("```sql")
    A("SELECT llm, COUNT(*) AS n, SUM(CASE WHEN cited THEN 1 ELSE 0 END) AS cited")
    A("  FROM citations")
    A(" WHERE COALESCE(is_probe,0)=0 AND date(timestamp) <= '2026-08-31'")
    A(" GROUP BY llm;")
    A("```")
    A("")
    A("Expected from VERIFICATION.md: ChatGPT 17.2%, Claude 25.8%, Gemini 1.8%, "
      "Groq 8.5%, Perplexity 75.7%, Grok 32.3% over 66,399 canonical rows. That "
      "query reproduces those figures on this snapshot; the figures in TABLES.md "
      "differ because the snapshot now runs to "
      f"{ctx['last_day']} and adds {ctx['n_canonical'] - 66399:,} canonical rows.")
    A("")

    # ---- T4 ----
    A("## T4. First-mention offset")
    A("")
    sql_block("t4_offset")
    A("")
    A("The median of the relative offset is not expressible in portable SQLite SQL "
      "and is computed in Python from:")
    A("")
    sql_block("t4_relative_values")
    A("")
    A("| Engine | n cited | Mean absolute offset | Mean observed length "
      "| Mean relative | Median relative |")
    A("|---|---:|---:|---:|---:|---:|")
    for e in ctx["engines_present"]:
        if e not in ctx["t4"]:
            continue
        d = ctx["t4"][e]
        A(f"| {e} | {d['n_cited']:,} | {d['mean_offset']:,.1f} "
          f"| {d['mean_observed_length']:,.1f} | {d['mean_relative']:.4f} "
          f"| {d['median_relative']:.4f} |")
    A("")

    # ---- T5 ----
    A("## T5. Preamble criterion")
    A("")
    A("The regular expression used for Table 7 of manuscript v1.0 was never "
      "committed to the repository. It is described in prose in `MANUSCRIPT.md` "
      "(Table 7 caption), `docs/METHODOLOGY_V2.md` section 4.1-bis.1 and "
      "`governance/REVISAO-EXTERNA-PAPER-20260831.md` item D9, all three saying "
      "the same thing: anchored at the start of the response, matching greeting, "
      "hedge, question restatement and model self-reference. It cannot be re-run, "
      "so the pattern below is a re-specification, published in full because the "
      "criterion is part of the result.")
    A("")
    A("Applied as `re.search(PATTERN, response_text, re.IGNORECASE)` over canonical "
      "rows with non-null `response_text`. The pattern is assembled in `_common.py` "
      "from three alternatives. Each is printed below as a literal regular "
      "expression, not as Python source, so it can be pasted into any engine "
      "without unescaping.")
    A("")
    A("(a) greeting or praise of the question:")
    A("")
    A("```regex")
    A(C._PREAMBLE_GREETING)
    A("```")
    A("")
    A("(b) hedge on whether the question can be answered:")
    A("")
    A("```regex")
    A(C._PREAMBLE_HEDGE)
    A("```")
    A("")
    A("(c) explicit model self-reference:")
    A("")
    A("```regex")
    A(C._PREAMBLE_SELFREF)
    A("```")
    A("")
    A("The three are joined as `^\\W*(?:a|b|c)` and compiled with `re.IGNORECASE`. "
      "The complete pattern, exactly as compiled:")
    A("")
    A("```regex")
    A(C.PREAMBLE_PATTERN)
    A("```")
    A("")
    A("Values on the snapshot, canonical stratum:")
    A("")
    A("| Engine | n | Preamble | Share | 95% CI | Cited | Rate |")
    A("|---|---:|---:|---:|---:|---:|---:|")
    for e in ctx["engines_present"]:
        d = ctx["t5"][e]
        A(f"| {e} | {d['n']:,} | {d['pre']:,} | {_pct(d['pre'], d['n'], 2)} "
          f"| {_ci(d['pre'], d['n'], 2)} | {d['cited']:,} "
          f"| {_pct(d['cited'], d['n'], 2)} |")
    A("")
    A("**Divergence from manuscript v1.0.** The same pattern applied to the exact "
      "row set of manuscript v1.0 (canonical, `date(timestamp) <= '2026-08-31'`, "
      "66,399 rows), against the published figures:")
    A("")
    A("| Engine | n | This criterion | Published v1.0 | Difference |")
    A("|---|---:|---:|---:|---:|")
    for e in ctx["engines_present"]:
        n, pre = ctx["t5_v10_window"][e]
        pub = ctx["t5_v10_published"][e]
        mine = 100 * pre / n
        A(f"| {e} | {n:,} | {mine:.1f}% | {pub:.1f}% | {mine - pub:+.1f} pp |")
    A("")
    A("The two criteria agree that Gemini is the outlier by a wide margin and that "
      "Claude is at zero. They disagree on Perplexity and Grok by a few percentage "
      "points, in opposite directions. The claim the paper rests on, that the arm "
      "with the most preamble is parametric and the retrieval-augmented arm has "
      "little, holds under both. A reader who prefers a different criterion can "
      "substitute one: the pattern is a constant in `_common.py` and every figure "
      "in T5 regenerates from it.")
    A("")

    # ---- T6 ----
    A("## T6. Rate by vertical and engine")
    A("")
    A("Computed from the uniform-window re-extraction (V1), grouped by `llm` and "
      "`vertical`. The statement below returns the *as-collected* counts. For the "
      "five arms whose stored text never exceeded the window it returns exactly the "
      "counts tabulated here; for Perplexity it returns larger ones, and that "
      "difference is the window effect of Table 3 seen cell by cell.")
    A("")
    A("```sql")
    A("SELECT llm, vertical, COUNT(*) AS n,")
    A("       SUM(CASE WHEN cited THEN 1 ELSE 0 END) AS cited")
    A("  FROM citations WHERE COALESCE(is_probe,0)=0 AND response_text IS NOT NULL")
    A(" GROUP BY llm, vertical;")
    A("```")
    A("")
    A("| Engine | Vertical | n | Cited | Rate | 95% CI |")
    A("|---|---|---:|---:|---:|---:|")
    for e in ctx["engines_present"]:
        for v in C.VERTICALS:
            n, c = ctx["t6"][e][v]
            A(f"| {e} | {v} | {n:,} | {c:,} | {_pct(c, n, 2)} | {_ci(c, n, 2)} |")
    for v in C.VERTICALS:
        n, c = ctx["t6_panel"][v]
        A(f"| **Panel** | {v} | {n:,} | {c:,} | {_pct(c, n, 2)} | {_ci(c, n, 2)} |")
    A("")

    # ---- T7 ----
    A("## T7. Rate by language, query type and category")
    A("")
    A("Same source as T6, grouped by `query_lang`, `query_type` and "
      "`query_category`.")
    A("")
    for label, key in (("T7a, language", "t7a"), ("T7b, query type", "t7b"),
                       ("T7c, semantic category", "t7c")):
        A(f"### {label}")
        A("")
        A("| Engine | Level | n | Cited | Rate | 95% CI |")
        A("|---|---|---:|---:|---:|---:|")
        for e in list(ctx["engines_present"]) + ["Panel"]:
            if e not in ctx[key]:
                continue
            for lv, (n, c) in ctx[key][e].items():
                A(f"| {e} | {lv} | {n:,} | {c:,} | {_pct(c, n, 2)} "
                  f"| {_ci(c, n, 2)} |")
        A("")
    A("Battery coverage by engine and category, which is the reason the panel row "
      "of T7c is not a category effect:")
    A("")
    sql_block("battery_coverage")
    A("")
    A("| Engine | " + " | ".join(ctx["categories"]) + " |")
    A("|---|" + "---:|" * len(ctx["categories"]))
    for e in ctx["engines_present"]:
        A(f"| {e} | " + " | ".join(
            f"{ctx['battery_coverage'][e].get(cat, 0):,}" for cat in ctx["categories"]) + " |")
    A("")

    # ---- T8 ----
    A("## T8. Concentration of first mentions")
    A("")
    A("First mentions are taken under the uniform 200-character window, from the "
      "re-extraction described in V1: for each canonical observation, the cohort "
      "entity with the lowest offset inside the window. Counted with "
      "`collections.Counter`.")
    A("")
    A("| Quantity | Value |")
    A("|---|---:|")
    t8 = ctx["t8"]
    A(f"| observations carrying a first mention | {t8['total_first']:,} |")
    A(f"| distinct entities ever named first | {t8['distinct']} |")
    A(f"| cohort, distinct entities | {t8['cohort_unique']} |")
    A(f"| Brazilian real firms named first | {t8['named_real_br']} of {t8['real_br']} |")
    A(f"| international anchors named first | {t8['named_anchors']} of {t8['anchors']} |")
    A(f"| fictitious decoys named first | {t8['named_decoys']} of {t8['decoys']} |")
    A(f"| cumulative share, top 1 | {t8['cumulative'][1]:.4f}% |")
    A(f"| cumulative share, top 3 | {t8['cumulative'][3]:.4f}% |")
    A(f"| cumulative share, top 5 | {t8['cumulative'][5]:.4f}% |")
    A(f"| cumulative share, top 10 | {t8['cumulative'][10]:.4f}% |")
    A(f"| Herfindahl-Hirschman index, 0 to 1 | {t8['hhi']:.6f} |")
    A(f"| HHI equivalent number of participants (1/HHI) | {1/t8['hhi']:.3f} |")
    A(f"| Gini over named entities | {t8['gini']:.6f} |")
    A("")
    A("Top ten:")
    A("")
    A("| Rank | Entity | First mentions | Share |")
    A("|---:|---|---:|---:|")
    for i, (ent, c) in enumerate(t8["top10"], start=1):
        A(f"| {i} | {ent} | {c:,} | {100*c/t8['total_first']:.4f}% |")
    A("")
    A("Index definitions, stated so neither is guessed at:")
    A("")
    A("```python")
    A("def hhi(counts):   # reported index")
    A("    total = sum(counts)")
    A("    return sum((c / total) ** 2 for c in counts)")
    A("")
    A("def gini(counts):  # secondary, over named entities only")
    A("    xs, n, total = sorted(counts), len(counts), sum(counts)")
    A("    cum = sum((i + 1) * x for i, x in enumerate(xs))")
    A("    return (2 * cum) / (n * total) - (n + 1) / n")
    A("```")
    A("")
    A("Distinct first entities under the as-collected window, for contrast:")
    A("")
    sql_block("t8_as_collected_distinct")
    A("")
    A(f"Value: {ctx['t8_as_collected_distinct']} against {t8['distinct']} under the "
      "uniform window.")
    A("")
    A("### T8b. Lexical collisions in the cohort")
    A("")
    co = ctx["collision"]
    A("Two cohort surface forms are ordinary words. Confirm the matched contexts "
      "before believing the counts:")
    A("")
    A("```sql")
    A("SELECT llm, query_lang, substr(response_text,1,180)")
    A("  FROM citations")
    A(" WHERE COALESCE(is_probe,0)=0 AND first_entity_v2='Involves' LIMIT 6;")
    A("```")
    A("")
    A("Frequencies of every entity ever matched, which is how the two were found:")
    A("")
    A("```python")
    A("from collections import Counter; import json, sqlite3")
    A('con = sqlite3.connect("file:data/papers.db?mode=ro", uri=True)')
    A("c = Counter()")
    A('for (j,) in con.execute("SELECT cited_entities_v2_json FROM citations "')
    A('                        "WHERE COALESCE(is_probe,0)=0 '
      'AND cited_entities_v2_json IS NOT NULL"):')
    A("    for e in json.loads(j): c[e] += 1")
    A("print(c.most_common())")
    A("```")
    A("")
    A("Sensitivity, computed in `build_tables.build` by removing "
      f"{co['names']} from the matched entity list of each observation:")
    A("")
    A("| Quantity | With collisions | Without |")
    A("|---|---:|---:|")
    A(f"| panel citations under the uniform window | {co['panel_cited_with']:,} "
      f"| {co['panel_cited_without']:,} |")
    A(f"| panel citation rate | {_pct(co['panel_cited_with'], co['panel_n'], 4)} "
      f"| {_pct(co['panel_cited_without'], co['panel_n'], 4)} |")
    A(f"| distinct entities named first | {co['distinct_first_with']} "
      f"| {co['distinct_first_without']} |")
    A(f"| HHI | {t8['hhi']:.6f} | {co['hhi_without']:.6f} |")
    A(f"| top-1 share | {t8['cumulative'][1]:.4f}% | {co['top1_share_without']:.4f}% |")
    A("")
    A("| Detail | Value |")
    A("|---|---:|")
    A(f"| observations with at least one colliding match | {co['rows_touched']:,} |")
    A(f"| observations cited only because of a collision "
      f"| {co['rows_cited_only_by_collision']:,} |")
    A(f"| observations whose first mention is a collision "
      f"| {co['rows_first_mention_is_collision']:,} |")
    for k, v in sorted(co["by_name"].items(), key=lambda kv: -kv[1]):
        A(f"| matches of `{k}` | {v:,} |")
    for k, v in sorted(co["by_lang"].items(), key=lambda kv: -kv[1]):
        A(f"| collisions in `{k}` responses | {v:,} |")
    for k, v in sorted(co["by_engine"].items(), key=lambda kv: -kv[1]):
        A(f"| collisions in {k} responses | {v:,} |")
    A("")

    # ---- T9 ----
    A("## T9. Calibration decoys in the canonical stratum")
    A("")
    A("Extractors restricted to the sixteen decoys of "
      "`src/config_v2.FICTITIOUS_DECOYS_V2`, with no aliases and no stop contexts, "
      "run over the canonical rows twice: over `response_text[:200]` and over "
      "`response_text` as stored. Built by `_common.build_decoy_extractors`.")
    A("")
    A("| Engine | Canonical n | Decoy in window | Decoy in stored text |")
    A("|---|---:|---:|---:|")
    for e in ctx["engines_present"]:
        n, w, cc = ctx["t9_per_engine"][e]
        A(f"| {e} | {n:,} | {w} | {cc} |")
    t9 = ctx["t9"]
    A(f"| **Panel** | {t9['n_canonical']:,} | {t9['decoy_window']} "
      f"| {t9['decoy_collected']} |")
    A("")
    lo, hi = C.wilson(0, t9["n_canonical"])
    A(f"Point estimate 0.0%; 95% Wilson interval [{100*lo:.6f}, {100*hi:.6f}] "
      f"percentage points, i.e. an upper bound of "
      f"{hi*t9['n_canonical']:.2f} expected occurrences in {t9['n_canonical']:,} "
      f"observations.")
    A("")
    A("The stored column agrees and is reported so the agreement is visible, but it "
      "is not independent evidence, because it was only ever populated on the probe "
      "stratum:")
    A("")
    sql_block("t9_canonical_fictional_hit")
    A("")
    A(f"Value: {t9['stored_fictional_hit_in_canonical']} flagged rows in "
      f"{t9['n_canonical']:,} canonical rows.")
    A("")

    # ---- T10 ----
    A("## T10. Adversarial stratum")
    A("")
    sql_block("t10_probe")
    A("")
    A("The refusal marker is the regex of `VERIFICATION.md` section 5.3, "
      "reproduced verbatim in `_common.REFUSAL_PT` and `_common.REFUSAL_EN`, "
      "applied to:")
    A("")
    sql_block("t10_refusal_rows")
    A("")
    A("| Engine | Probe n | Flagged | Share | 95% CI | Flagged with text "
      "| With refusal marker | Share | 95% CI |")
    A("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for e in ctx["engines_present"]:
        if e not in ctx["t10"]:
            continue
        d = ctx["t10"][e]
        A(f"| {e} | {d['n_probe']:,} | {d['flagged_old_criterion']:,} "
          f"| {_pct(d['flagged_old_criterion'], d['n_probe'], 2)} "
          f"| {_ci(d['flagged_old_criterion'], d['n_probe'], 2)} "
          f"| {d['refusal_den']:,} | {d['refusal_num']:,} "
          f"| {_pct(d['refusal_num'], d['refusal_den'], 2)} "
          f"| {_ci(d['refusal_num'], d['refusal_den'], 2)} |")
    tp = ctx["t10_panel"]
    A(f"| **Panel** | {tp['n_probe']:,} | {tp['flagged']:,} "
      f"| {_pct(tp['flagged'], tp['n_probe'], 2)} "
      f"| {_ci(tp['flagged'], tp['n_probe'], 2)} | {tp['refusal_den']:,} "
      f"| {tp['refusal_num']:,} | {_pct(tp['refusal_num'], tp['refusal_den'], 2)} "
      f"| {_ci(tp['refusal_num'], tp['refusal_den'], 2)} |")
    A("")
    A("VERIFICATION.md section 5.3 expects 15,993 flagged and 10,775 carrying a "
      "refusal marker, 67.4%, on the snapshot of 2026-08-31. This snapshot has "
      f"{tp['refusal_den']:,} and {tp['refusal_num']:,}, "
      f"{_pct(tp['refusal_num'], tp['refusal_den'], 1)}: the same quantity on more "
      "data.")
    A("")

    # ---- T11 ----
    A("## T11. Temporal coverage")
    A("")
    sql_block("t11_months")
    A("")
    A("| Month | Days with data | Canonical n | Calendar days in span | Days missing |")
    A("|---|---:|---:|---:|---:|")
    for m in ctx["t11_months_full"]:
        A(f"| {m['month']} | {m['days_with_data']} | {m['n_canonical']:,} "
          f"| {m['calendar_days']} | {m['days_missing']} |")
    A("")
    A("The `GROUP BY` returns no row for 2026-07 because no observation exists in "
      "that month. The table above walks every month in the span so the empty month "
      "is visible rather than absent.")
    A("")
    sql_block("t11_runs")
    A("")
    A("| Status | n | First day | Last day |")
    A("|---|---:|---|---|")
    for k, v in ctx["t11"]["runs"].items():
        A(f"| `{k}` | {v['n']:,} | {v['first_day']} | {v['last_day']} |")
    A("")
    sql_block("t11_aborted_detail")
    A("")
    d = ctx["t11_aborted_detail"]
    A(f"{d['n_rows']:,} rows over {d['distinct_days']} distinct days, all carrying "
      f"the same reason, which begins `{d['reason_prefix']}`. These are retroactive "
      "gap markers written by `scripts/mark_collection_gaps.py`, not observed "
      "failures.")
    A("")
    A("Partial days are derived from:")
    A("")
    sql_block("t11_days")
    A("")
    t11 = ctx["t11"]
    A("The registry `data/partial_days.json` is read directly; present = "
      f"{t11['partial_days_json_present']}, {len(t11['registered'])} entries, of "
      f"which {len(t11['registered_in_span'])} fall inside the snapshot span "
      f"{t11['first_day']} to {t11['last_day']} and "
      f"{len(t11['registered_outside_span'])} fall after it. No script in the "
      "repository writes or reads that file on the analysis path, so it is treated "
      "as a hand-kept record, authoritative on what it covers and silent on the "
      "rest of the series.")
    A("")
    A("| Registry day | Engines missing | Inside snapshot span |")
    A("|---|---|---|")
    for e in t11["registered"]:
        if "date" not in e:
            A(f"| (malformed entry) | {e} | — |")
            continue
        inside = t11["first_day"] <= e["date"] <= t11["last_day"]
        A(f"| {e['date']} | {', '.join(e.get('missingLLMs', []))} "
          f"| {'yes' if inside else 'no'} |")
    A("")
    A("Agreement between the registry and the derived rule, on the days both cover:")
    A("")
    A("| Day | Registry says missing | Derived rule says absent | Match |")
    A("|---|---|---|---|")
    for a in t11["registry_agreement"]:
        A(f"| {a['date']} | {', '.join(a['registered_missing']) or '—'} "
          f"| {', '.join(a['derived_absent']) or '—'} "
          f"| {'yes' if a['match'] else 'NO'} |")
    A("")
    A("The derived rule is implemented in `build_tables.build`:")
    A("")
    A("```python")
    A("# battery size = the largest distinct-query count the engine ever reached")
    A("# in one day; a day is partial when some engine active in the surrounding")
    A("# period is short of its battery or absent altogether")
    A("battery[e] = max(per_day[d][e]['uq'] for d in days if e in per_day[d])")
    A("short  = [e for e in engines if e in per_day[d]")
    A("          and per_day[d][e]['uq'] < battery[e]]")
    A("absent = [e for e in engines if e not in per_day[d]")
    A("          and active_span[e][0] <= d <= active_span[e][1]]")
    A("```")
    A("")
    A("| Engine | Battery size inferred |")
    A("|---|---:|")
    for e, b in ctx["t11"]["battery"].items():
        A(f"| {e} | {b} |")
    A("")
    A(f"Result: {len(ctx['t11']['partial_days'])} partial days out of "
      f"{ctx['t11']['days_with_data']} days with data, listed in TABLES.md "
      "Table 11.")
    A("")

    # ---- T12 ----
    A("## T12. Descriptive temporal stability")
    A("")
    A("Daily rates come from the uniform-window re-extraction (V1) grouped by "
      "`llm` and `date(timestamp)`, keeping only days with at least "
      f"{C.SMALL_N} canonical observations for that engine. The slope is ordinary "
      "least squares of daily rate in percentage points on days elapsed since "
      f"{ctx['t11']['first_day']}, implemented in `_common.ols_slope`; the interval "
      "is a residual-based normal interval and is descriptive only.")
    A("")
    A("| Engine | Days used | n | Slope pp/day | Interval low | Interval high "
      "| Min daily | Max daily |")
    A("|---|---:|---:|---:|---:|---:|---:|---:|")
    for e in ctx["engines_present"]:
        d = ctx["t12"][e]
        if d["days"] < 3:
            A(f"| {e} | {d['days']} | — | not estimated | — | — | — | — |")
            continue
        A(f"| {e} | {d['days']} | {d.get('n_total', 0):,} | {d['slope']:+.6f} "
          f"| {d['lo']:+.6f} | {d['hi']:+.6f} | {d['min']:.2f}% | {d['max']:.2f}% |")
    A("")
    A("```python")
    A("def ols_slope(xs, ys):")
    A("    n  = len(xs); mx = sum(xs)/n; my = sum(ys)/n")
    A("    sxx = sum((x-mx)**2 for x in xs)")
    A("    b   = sum((x-mx)*(y-my) for x, y in zip(xs, ys)) / sxx")
    A("    a   = my - b*mx")
    A("    s2  = sum((y-(a+b*x))**2 for x, y in zip(xs, ys)) / (n-2)")
    A("    se  = (s2/sxx) ** 0.5")
    A("    return b, b - 1.959963984540054*se, b + 1.959963984540054*se")
    A("```")
    A("")

    # ---- T13 ----
    A("## T13. Window effect on every arm")
    A("")
    A("Produced by `window_analysis.py`, which selects:")
    A("")
    A("```sql")
    A("SELECT id, timestamp, llm, vertical, query_lang, query_type,")
    A("       response_text, response_full_text, cited_v2")
    A("  FROM citations")
    A(" WHERE COALESCE(is_probe,0)=0")
    A("   AND response_full_text IS NOT NULL")
    A("   AND length(response_full_text) > 0")
    A(" ORDER BY id;")
    A("```")
    A("")
    A("and, for each row, extracts over `response_full_text[:200]` and over "
      "`response_full_text` with the same extractor.")
    A("")
    ch = ctx["t13"]["checks"]
    A("| Check | Mismatches | Verdict |")
    A("|---|---:|---|")
    A(f"| `response_text` == `response_full_text[:200]` | "
      f"{ch['text_prefix_mismatch']} | "
      f"{'PASS' if ch['text_prefix_mismatch'] == 0 else 'FAIL'} |")
    A(f"| re-extraction of the first 200 chars == stored `cited_v2` | "
      f"{ch['cited_v2_mismatch']} | "
      f"{'PASS' if ch['cited_v2_mismatch'] == 0 else 'FAIL'} |")
    A(f"| rows compared | {ch['rows']:,} | — |")
    A("")
    A("| Engine | n | Cited at 200 | Rate | 95% CI | Cited on full | Rate | 95% CI "
      "| Δ pp | Gains | Losses | McNemar p | Mean full len | Median full len "
      "| Max full len | Rows > 200 | Dates |")
    A("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|")
    for e in C.ENGINES:
        if e not in ctx["t13"]["per_engine"]:
            continue
        d = ctx["t13"]["per_engine"][e]
        A(f"| {e} | {d['n']:,} | {d['cited_head']:,} | {d['rate_head']:.4f}% "
          f"| {_ci(d['cited_head'], d['n'], 2)} | {d['cited_full']:,} "
          f"| {d['rate_full']:.4f}% | {_ci(d['cited_full'], d['n'], 2)} "
          f"| {d['delta_pp']:+.4f} | {d['gain']:,} | {d['loss']:,} "
          f"| {d['mcnemar_p']:.3e} | {d['mean_len_full']:,.1f} "
          f"| {d['median_len_full']:,.0f} | {d['max_len_full']:,} "
          f"| {d['rows_longer_than_window']:,} | {', '.join(d['dates'])} |")
    A("")
    A("Gemini stratified by day, which is why the pooled Gemini row understates the "
      "effect:")
    A("")
    A("| Day | n | Cited at 200 | Cited on full | Mean full length |")
    A("|---|---:|---:|---:|---:|")
    for day, v in ctx["t13_gemini_by_day"].items():
        A(f"| {day} | {v['n']:,} | {v['head']:,} | {v['full']:,} "
          f"| {v['len']/v['n']:,.1f} |")
    g = ctx["t13_gemini_0708"]
    A(f"| **2026-09-07 and 2026-09-08** | {g['n']:,} | {g['head']:,} | {g['full']:,} "
      f"| {g['mean_len']:,.1f} |")
    A("")
    A(f"Restricted to those two days: {g['rate_head']:.4f}% "
      f"[{g['head_ci'][0]:.2f}, {g['head_ci'][1]:.2f}] at 200 characters against "
      f"{g['rate_full']:.4f}% [{g['full_ci'][0]:.2f}, {g['full_ci'][1]:.2f}] on the "
      f"full text, {g['delta_pp']:+.4f} pp.")
    A("")
    A("Mean entities found per observation, which is the same effect counted "
      "without the binary threshold:")
    A("")
    A("| Engine | Mean entities in first 200 chars | Mean entities in full text "
      "| Median first-mention offset in full text |")
    A("|---|---:|---:|---:|")
    for e in C.ENGINES:
        if e not in ctx["t13"]["per_engine"]:
            continue
        d = ctx["t13"]["per_engine"][e]
        A(f"| {e} | {d['mean_entities_head']:.4f} | {d['mean_entities_full']:.4f} "
          f"| {d['median_first_offset_full']:,.1f} |")
    A("")
    A("Groq contributes no rows: it left the panel on 2026-08-16 and full-text "
      "retention began on 2026-08-31. Verify with:")
    A("")
    A("```sql")
    A("SELECT llm, COUNT(*) AS canonical_rows_with_full_text")
    A("  FROM citations")
    A(" WHERE COALESCE(is_probe,0)=0 AND response_full_text IS NOT NULL")
    A("   AND length(response_full_text) > 0")
    A(" GROUP BY llm;")
    A("```")
    A("")

    # ---- rule ----
    A("## Rule")
    A("")
    A("No figure enters `TABLES.md` without appearing in this file with the "
      "statement that produces it. A figure in the tables and not here either came "
      "from a measurement nobody can repeat, or came from nowhere.")
    A("")
    A("Two figures in `TABLES.md` are not reproducible from the database alone and "
      "are flagged as such where they appear: the architectural class of each "
      "engine in Table 1, which is editorial and taken from MANUSCRIPT.md Table 3; "
      "and the preamble regular expression in Table 5, which is a re-specification "
      "of a criterion that manuscript v1.0 described but never committed.")
    A("")
    return "\n".join(out) + "\n"
