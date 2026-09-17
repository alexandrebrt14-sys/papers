# V7 — Incorporating the S1 multilevel model into blocks E and F

Editorial pass of 2026-09-11. Source dossier: `stats/S1-multilevel.md`, produced by `stats/s1_multilevel.py` into `stats/s1_results.json` in a run of 1,596.7 s over the read-only snapshot. Every figure below was taken from that dossier or from the JSON beside it; nothing was recomputed by hand and no git operation that alters state was run.

---

## 1. What entered, and where

### Block E

| Passage | Change |
|---|---|
| §9.1 | New paragraph tying the model's standard-error inflation to the design effect already reported. The clustered errors run 2.4 to 10.4 times the binomial ones, an inflation of 8.0 is a design effect of 64, and the 63.3 of Table E1 is the same quantity on the variance scale. States that the inflation is smallest on the engine contrasts, which vary inside a prompt, and largest on the prompt-level covariates, whose block tests carry design effects of 74 to 90. The original design-effect paragraph was split so that no paragraph crosses the 1,500-character warning |
| §9.2 heading | "Citation differs by engine more than by anything else" became "Citation belongs to the prompt and to the firm-engine pair, and almost none of it belongs to the day". The old heading is contradicted by the model, which puts the prompt at an intraclass correlation of 0.4559 against 0.3492 for the engine |
| §9.2 body | Rewritten with the model as the inferential result and the two-way decomposition of Table E2 kept as the convergent one. Carries the specification, the two estimators and why both are reported, the version and window caveats on two engine coefficients, the design-corrected block tests, the interaction tests, the variance decomposition at two levels, the unexplained between-prompt variance and its consequence for P3, and a closing paragraph stating exactly where the two analyses can and cannot be compared. The kappa, Jaccard and instrument passages of the old §9.2 are untouched |
| **Table E12** (new) | Fixed effects under both estimators: conditional odds ratio with credible interval, population-averaged odds ratio with `t(51)` interval, standard-error inflation, p |
| **Table E13** (new) | Variance decomposition by level at the response and the entity level, with σ² and intraclass correlation in each panel |
| §9.4 | Reordered so the paired contrast is the principal result and the marginal one is context. Opens on the paired effect of −4.54 points, defines the pair, and states why the pairing is the design-valid contrast. The marginal figures of the old opener are retained verbatim in the third paragraph, now labelled as the reading the design cannot support, with the odds ratio, the clustered p of 0.552 and the design-corrected p of 0.549 beside them |
| **Table E14** (new) | McNemar on 21,862 matched pairs, overall and by engine, with discordant counts and exact p |
| §9.4 prose | The within-pair engine-by-language regression: Perplexity +17.03 pp over ChatGPT [6.86, 27.20], Gemini +10.47 [3.02, 17.93], block F(5, 51) = 3.17 at p = 0.0145, surviving Benjamini-Hochberg, against p = 0.354 for the same interaction on the marginal model |
| Open marks, item 2 | Rewritten. It had recorded that `S1-multilevel.md` was absent and that §9.2 stated the model was not fitted. It now records that both files exist, names the three tables and the three subsections that draw on them, and points at the Table F14 row corrected in block F |
| Anti-tic pass | Every declared count refreshed against `reviews/style_check.py`: 6,228 words, 40,141 characters, 55 paragraphs, 217 sentences, 83 percentages, 15 display items, C.1.10 total 2, closers carrying a figure 76.4% |

### Block F

| Passage | Change |
|---|---|
| §14, Table F1 | Three rows added. **23**, the battery's design factors account for none of the variance between prompts. **24**, repeated runs return byte-identical text and the series cannot say why. **25**, `src/analysis/mixed_effects.py` stores a standard deviation under a key named for a variance |
| §14, lead-in | "Six of those rows carry an argument the table cannot hold" became "Nine" |
| §14, new prose | Four paragraphs. One on the P3 consequence; two on the byte-identity measurement, its two competing readings and the requirement it creates for P5; one on the wrapper defect and why it belongs in the register rather than in a changelog |
| §15, opener | "Four results … and four of its propositions" became "Five … five" |
| §15, Table F2 | One row added, pairing the prompt-above-engine measurement with the untested proposition that a battery published with its factorial invariants is a characterised battery |
| §15, firm-engine paragraph | Extended with the model's response-level reading and with one sentence carrying the paired language result into the discussion |
| Appendix E, Table F14 | The row for `s1_multilevel.py` said "No table or figure of this paper draws on it: §9.2 states that the mixed-effects model is not fitted". It now names §9.1, §9.2, §9.4 and §14, the three new E tables, rows 23 to 25 of Table F1, and the runtime |
| Reference keys intro | `../stats/S1-multilevel.md` added to the list of files the block's figures come from, with the specific figures named |
| Anti-tic pass | Counts refreshed: 6,177 words, 39,956 characters, 64 paragraphs, 238 sentences, 30 percentages, 25 rows in Table F1, closers carrying a figure 51.6% |

### Block B

Two edits, both minimal and both disclosed here because the brief allowed one line.

1. **The P3 remission (the line the brief authorised).** One sentence appended to the P3 entry of §3.1: publishing the invariants makes a battery checkable by a second party without making two balanced batteries interchangeable, since the four factors this battery balances account for none of the variance between its own prompts. The normative text, the requirement identifier and the failure mode are untouched.
2. **Two stale numbers in block B's own anti-tic pass**, invalidated by edit 1. The apposition row read "across 4,575 words" and now reads 4,617; the diagnostic row read "standard deviation of 13.8" and now reads 13.9. Leaving a measurement declaration that the script contradicts would have been worse than a second scoped line, but the integrator should know both edits exist.

---

## 2. The two questions the brief asked me to check

**The standard errors and the design effect are one measurement.** They are. The design effect is the variance ratio and the inflation is its square root: 63.3 corresponds to an inflation of 7.96, and the dossier's range of 2.4 to 10.4 spans design effects of 5.7 to 108. The two are now tied in one sentence in §9.1, with the reason the range is wide stated beside it — engine varies inside a prompt and carries the small inflations, while vertical, language, query type and category are properties of the prompt and carry the large ones. The dossier's block-level design effects of 74 to 90 for prompt-level covariates and 29.51 for engine are the same quantity measured per block instead of pooled, and §9.2 reports them as such.

**Whether any number in this paper depended on the mislabelled key.** None does. `random_variances` is defined in `src/analysis/mixed_effects.py` and read by no other module in the repository; `s1_multilevel.py` converts from `log σ` itself and publishes σ and σ² separately. The defect was placed in the threats register rather than in the field record of block C, because block C is outside the scope of this edit and because the consequence is prospective: H1 of Table E11 names that module as the committed code for the confirmatory mixed-effects test, which is where a mislabelled variance component would first reach a published number. That is the sentence row 25 and its paragraph carry.

---

## 3. The cache ambiguity, and how it is stated

The measurement is reported with all three figures the coordinator asked for: 47.84% of the 22,495 multi-run cells byte-identical, 71.88% on the retired open-weights arm against 0.04% on the retrieval-augmented one, and 14,391 distinct response hashes over 68,624 canonical rows. The text names both explanations, says the by-arm distribution favours near-deterministic decoding because the arm that searches the web almost never repeats while the parametric arms repeat constantly, and then says without hedging that the series cannot separate them, because no column of `citations` carries a cache flag and the information was never written. The adopter consequence is stated as a requirement on P5: an implementation measuring run-to-run variation records per observation whether the response came from cache, since otherwise the run-to-run term of an uncertainty budget cannot be told apart from a replay. The passage is tied to the converse claim the paper already makes, that P5 pins the request and not the response because hosted models do not reproduce their outputs exactly at temperature zero [Atil2025, Coqueret2026], and it states that neither passage is evidence about the other until the flag exists.

**One correction against the dossier.** `stats/S1-multilevel.md` §1.3 describes the protocol as arguing "an 8-hour TTL against a 12-hour interval". The paper's §4.7 and `src/collectors/response_cache.py`, `src/config.py` and `src/shared/llm_utils.py` all give a default of **20 hours**, which makes a cache hit possible by construction rather than impossible. The manuscript uses 20 hours. The dossier's sentence should be corrected before S1 is circulated as a supplement.

---

## 4. What I left out of the dossier, and why

| Left out | Reason |
|---|---|
| **Table 1 of S1, the window asymmetry arm by arm** | Block D already carries the window measurement at greater length and on the matched 2,225-observation cohort. The coefficient-level version of the same finding, cut F at an odds ratio of 21.341 against 6.794, is in §9.2 because it is the model's own statement of it |
| **The 1.74-point gap between S1's start rule (0.53779) and S2's containment rule (0.52035) for the retrieval arm** | It is a definitional footnote about two defensible boundary rules, and block D already sets the boundary policy under P6. Carrying it into §9 would put a third Perplexity level in front of a reader who already has to hold two |
| **The partial-day audit of S1 §1.3 and its disagreement with `data/partial_days.json`** | Appendix D of block F already carries a partial-day ledger under a different and declared definition, derived from battery completeness per arm. Two ledgers with different definitions in one manuscript is a defect, not a robustness check. S1's 44 complete days appear only inside cut B of the robustness list |
| **Table 6d in full, the engine-as-random stability ladder** | Reported as one clause in §9.2, the entity-level engine share being 0.69 instead of 0.10 without the ladder. The five-row table is a negative result about a specification the paper does not use, and it belongs in the supplement |
| **The full multiplicity tables, families `S1-contrasts` (7 of 12 survive) and `S1-robustness` (54 of 93)** | Only the confirmatory family carries weight, and §9.2 states its result: 13 of 17 survive Benjamini-Hochberg at a declared false discovery rate of 5%. The robustness family is redundant by construction and the dossier says so |
| **Model M1full on the full canonical cut** | The dossier reports it "for completeness only" and says it identifies neither engine nor category cleanly. Publishing it would invite the extrapolation the core-3 split exists to prevent |
| **The Grok caveats as a separate expanded item** | §9 and Table F1 already carry them, and §9.2 reports Grok's coefficient inside Table E12 where the interval does the work. Five collection days is stated wherever Grok's figures appear elsewhere in the block |
| **S1's per-engine Jaccard and entity-slot benchmarks** | §9.2's existing agreement passage covers the same ground from the S3 dossier, which is the source the block already cites for agreement |

---

## 5. Numbers and consistency, checked

- Every figure added to E and F traces to `stats/S1-multilevel.md` Tables 2 to 11 or to `stats/s1_results.json`. Table captions name the source, the series, the denominator and the design.
- Two claims were written, checked against Table 10 of the dossier and corrected before delivery. The first said five robustness cuts "move nothing beyond the third digit"; collapsing byte-identical repeats moves the retrieval arm from 6.794 to 6.508 and Gemini from 0.089 to 0.078, so the sentence now names those two movements and says the cuts leave the coefficients inside one another's intervals. The second attributed a seven-fold error to the engine standard deviation of the stability ladder; the seven-fold figure is the intraclass correlation consequence, 0.69 against 0.10, and the sentence now says so.
- No citation key was created. The only keys used in new prose are `[Atil2025, Coqueret2026]`, both already in block F's list.
- Table numbering runs E12, E13, E14 with no gap and no collision. No new F table was needed, so the F15 reserve is unused; block F took three rows in Table F1 and one in Table F2.

---

## 6. Style ruler

`reviews/style_check.py` against PART C of `research/R4-standards.md`, run on the delivered files.

| Check | B | E | F |
|---|---|---|---|
| C.1.9 paragraphs over 2,200 chars | 0 | 0 | 0 |
| C.1.3 worn connectives, verdict | ok | ok | ok |
| C.1.1 antithesis, closed formula | 0 | 0 | 0 |
| C.1.1 antithesis, graduated | 0 | 1 | 0 |
| C.1.1 verdict | ok | warn | ok |
| C.1.7 em dash in prose | 0 | 0 | 0 |
| C.1.10 empty adjectives, verdict | ok | ok | ok |
| C.1.2, C.1.5, C.1.6, C.1.8, C.1.12, C.1.14 | 0 | 0 | 0 |
| C.6 machine-drafted lexicon | 0 | 2 | 0 |

Every C.1 failure count is zero in all three blocks. Block E's C.1.1 warning is the single pre-existing graduated antithesis at the close of §9.4, unchanged by this pass and kept deliberately; the rule fails at two occurrences and the passages added here carry none. Block E's two C.6 levies are both "robust" inside "cluster-robust", the standard-error term, which fails above two occurrences of one root: the estimator is named "two-way clustered" everywhere else in the new §9.2 and §9.4 to hold the count at two.

Warnings, unchanged in count from before the pass: one paragraph above 1,500 characters in B (the P6 entry, 1,685) and one in F (the §13 conformance entry, 1,700). Block E has none, which required splitting the §9.1 design-effect paragraph after the new material pushed it to 1,778.

---

## 7. For the integrator

1. **`MANUSCRIPT-JOURNAL.md` is stale.** It carries the pre-pass text of both blocks, including the Table F14 row asserting that no table draws on `s1_multilevel.py` and the §15 sentence that cites §9.2 for the interaction alone. Re-run `cd J/build && python assemble.py` before any circulation.
2. **The S1 dossier's 8-hour TTL sentence needs correcting** to 20 hours, per §3 above. The manuscript is already right; the supplement is not.
3. **Block B's P5 entry in §3.1 has no cache-provenance clause.** §14 of block F now argues that an implementation measuring run-to-run variation must record cache provenance per observation, and names P5 as the parameter that should carry it. Writing that into the normative text of P5 would have been a specification change, which the brief's scope rule excluded, so the requirement currently lives only in the threats register. Someone with authority over §3 should decide whether P5 gains a `[BRGEO1-S-…]` clause or whether the threat stands as a threat.
4. **Superseded span carried forward unchanged.** Item 5 of block E's open marks still applies: the aggregation span 0.706 to 0.984 in blocks A and B contradicts the 0.752 to 0.985 in E and F. This pass did not touch it.
