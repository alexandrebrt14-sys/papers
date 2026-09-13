# Editorial decisions for the journal-length manuscript

Decided on 2026-09-11 from the Wave 1 and Wave 2 dossiers. Every writer follows these without relitigating them. Where a decision reverses something the v1.0 manuscript says, the reversal is listed with what has to change.

---

## 1. Data cut-off

The manuscript reports the series from **2026-04-23 to 2026-09-08**, the date of the local database snapshot used for every table. Collection continued after that date; the published dashboard shows 56 collected days on 2026-09-11. Stating a cut-off is standard practice and it keeps every number in the paper recomputable from one artefact. Say it once, in the methods section, and once in the data availability statement.

## 2. The confirmatory window does not close on 28 September

The v1.0 manuscript states that the window closes on 2026-09-28. That date was a forecast recorded on 2026-08-10 and it no longer holds: the window is ninety **collected** days, not ninety calendar days, and the credit outage of August and September cost seventeen days of series. The published projection is **2026-10-15**, with 56 of 90 collected days as of 2026-09-11, and the calendar ninetieth day passed on 2026-07-21.

What changes: §9 (analysis plan) and any sentence that dates the close. The correction is itself worth one sentence in the missingness section, because a window defined in collected days is a design choice that a reader should see declared rather than inferred.

## 3. Venue and reference style

**Information Sciences** is the target, not Information Processing & Management. IP&M states that submissions should not be published as a preprint before a final decision, which is incompatible with the SSRN-first sequence the project has already committed to; Information Sciences offers SSRN posting at submission and publishes in numeric style by order of appearance, which is the style the manuscript already uses.

Consequences: numeric citations in square brackets stay; highlights of five bullets at 85 characters stay, since Information Sciences asks for three to five; the abstract is written to **200 words**, the tighter of the two figures in that journal's own guide; a Conclusions section is mandatory and already exists.

Information Sciences also caps length (about 40 double-spaced pages for an experimental article, with eight display items). The journal-length manuscript will exceed that. The resolution is explicit: this manuscript is the SSRN working paper and the Eliva Press book block; the journal submission is a condensed derivative prepared afterwards, with §5, §9, §12 and the appendices moved to supplementary material. Do not shorten the argument now to fit a cap that applies to a later artefact.

## 4. The derived book

The Elsevier exception list for prior publication covers abstracts, lectures, theses, preprints and registered reports. It does not name a derived book. The sequence that preserves both routes: SSRN first, so the specification carries a dated DOI; the book published afterwards as an expanded derivative with material the article does not carry; and the book declared in the cover letter at journal submission. The paper itself says nothing about the book.

## 5. Positioning against the Dice Roll Method

Żatuchin, *The Dice Roll Method: A Standardized Protocol for Repeated-Query Auditing of Large Language Model Brand Recommendations*, arXiv:2609.04047, submitted 2026-09-03, is the only other published attempt to standardise measurement of entity mention in generative engines. It fixes iteration counts (5, 10, 15 by tier), stability metrics, and reliability thresholds expressed as generalizability coefficients, decomposing variance into sampling, prompt-phrasing, run-to-run and model-version components with a negative-binomial mixed model.

The two standards are disjoint and complementary, and the manuscript says so plainly. The Dice Roll Method answers how many times to repeat a query and when the resulting measure is reliable. BRGEO-1 answers under which conditions a single figure means anything: which text is read, which entities can be detected, which queries are asked, which model version answered, under which generation configuration, and by which matching rule. A measurement that adopts both is better specified than one that adopts either.

Two further consequences. First, generalizability theory is the right vocabulary for the variance decomposition in the multilevel analysis, and using it makes the relationship between the two protocols legible to a reviewer. Second, claiming to be the first standard in this space is no longer available and should not be attempted anywhere in the text.

## 6. Metrological framing

Adopt the vocabulary of VIM (JCGM 200:2012) and GUM (JCGM 100:2008), with clause numbers verified in the primary documents on 2026-09-11 (see `research/R5-metrology.md`). The three load-bearing uses:

- The citation rate is a **measurand** whose specification (VIM 2.3, Note 1) is incomplete without P1 to P6.
- The window effect is **definitional uncertainty** (VIM 2.27), not error: Note 1 makes it the practical minimum uncertainty achievable, and Note 2 states that any change in descriptive detail produces another definitional uncertainty. No sample size removes it. This is the strongest available defence of P1 and it replaces the looser language of v1.0.
- The promised inter-implementation exercise is an **interlaboratory study** in the sense of ISO 5725-2, with repeatability and between-implementation components, rather than unnamed future work.

Publish an **uncertainty budget** table separating Type A components (estimated from repeated observation) from Type B components (estimated from knowledge of the instrument). The argument it carries: the market reports the Type A components, which are the small ones.

Keep the limit of the analogy in threats to validity. There is no unit, no calibration hierarchy and no true value; the measurand is constituted by convention, which is Jacobs and Wallach's position for unobservable constructs.

## 7. The window result is now panel-wide, and it reverses a published reading

With full responses retained since 2026-08-31, the same observations can be extracted under both windows in every arm. On 06 to 08 September, matched by observation, with McNemar and no citation lost in any arm:

| Engine | n | Rate at 200 characters | Rate on the full response | Delta |
|---|---:|---:|---:|---:|
| Grok | 768 | 28.4% | 84.1% | +55.7 pp |
| ChatGPT | 192 | 17.2% | 53.6% | +36.5 pp |
| Gemini | 768 | 2.6% | 33.3% | +30.7 pp |
| Perplexity | 305 | 54.1% | 77.0% | +23.0 pp |

What this changes in the argument: the v1.0 paper reports a 23.8 point movement on one engine and treats the other five zero deltas as a sanity check guaranteed by construction. That framing stands for the historical series, and it is now known to have concealed the size of the effect rather than bounded it. The window is the dominant parameter across the whole panel.

It also reverses a published reading. The 1.8% attributed to Gemini is a property of the window, not of the engine: read whole, the same responses cite at 33.3%. Any sentence in v1.0 that characterises an engine's citation behaviour from the truncated series must be rewritten to characterise head-of-response citation, and §5.4's account of Gemini's preamble is confirmed as the mechanism rather than left as a post hoc explanation.

Limits that travel with the result: three collection days, 192 to 768 observations per arm, Claude and the retired Groq arm covered unevenly, and the period sits after several instrument changes. Report it as a matched within-observation comparison on a small window of days, which is exactly what it is.

## 8. Corrections to existing references

- [18] Pan et al.: the preprint is 2025, not 2026; promote to the ICLR 2026 version.
- [22] Raji et al.: author order is Raji, Bender, Paullada, Denton, Hanna; add arXiv:2111.15366.
- [20] Huang et al.: add volume 43, issue 2, pages 1–55.
- [46] RFC 8174: the manuscript title is correct; Crossref returns a divergent title. Do not "fix" it.

## 9. Claims that need a citation they do not have

- The economic premise that named firms inherit attention: cite the difference-in-differences estimate of traffic loss following the staged rollout of AI Overviews.
- The rationale of P4, that providers update the model behind a stable product name: cite the canonical study of behaviour drift in hosted models over time.
- The composite-index discussion of §8: cite the sensitivity-analysis literature for composite indicators, which prescribes the exact test the paper runs, and the work formalising the distance between nominal and effective weights, which is what the variance decomposition measures.

## 10. Concede the limit of P5

Pinned temperature does not buy determinism in a hosted model: silent updates, numerical rounding and expert routing keep the output non-deterministic at temperature zero. The specification pins the request, not the response. Concede this in §3.1 under P5 and use it as a further argument for retaining the full response rather than regenerating it, which strengthens §5.5 instead of weakening it.

## 11. Narrow the novelty claim on position effects

Output-side position effects are studied, and the related-work section must say so. The narrow claim that survives: instrument-side truncation of the output converts whole-response measurement into head-of-response measurement, at a cut-off that varies between providers because it is set by adapter code rather than by design.

## 12. Vocabulary discipline for proxy fields

The repository's own review of 2026-09-10 records that `selection_status` and `absorption_status` are proxies derived from mention and from name matching in exposed URLs, and that neither demonstrates semantic support by a source nor internal retrieval. Any use of these fields in the paper carries that qualification, or the field stays out.

---

## 13. Counting rules fixed at assembly (2026-09-11)

Three quantities were reported with two values across the dossiers. These are the values the manuscript uses, and every block is reconciled to them.

**Collected days: 53.** A collected day is a calendar date in UTC carrying at least one canonical observation. Under that rule the snapshot from 2026-04-23 to 2026-09-08 has 53 days, every one of them with at least 100 canonical observations, the thinnest being 2026-09-07 with 209. The figure of 52 that appears in the temporal analysis excludes one day under a stricter per-arm rule; where that analysis is cited, the manuscript says which rule produced the number rather than switching silently between them. The published dashboard counts 56 on 2026-09-11, which adds the three days collected after the cut-off.

**Observation counts: 86,543 total, of which 68,624 canonical and 17,919 adversarial probes.** The figures of 80,638 and 83,486 are from earlier snapshots and belong to the v1.0 manuscript; they do not appear in this version except where the field record quotes a dated document.

**Calendar span: 139 days**, of which 53 carry data, giving 37.4% coverage, with a contiguous 59-day interruption from 2026-06-10 to 2026-08-07.

## 14. Every cross-engine figure uses the uniform 200-character window

Figures quoted from the stored outcome differ from figures computed under a uniform window, because five arms stored 200 characters and one stored the whole response. The difference is not small: pooled by language the stored outcome gives 22.9% in English against 18.2% in Portuguese, and the uniform window gives 20.22% against 15.72%; by query type the stored outcome gives 27.7% directive against 13.4% exploratory, and the uniform window gives 25.93% against 10.00%; the category range narrows from 33.3%-3.1% to 27.00%-3.08%.

The manuscript reports the uniform-window figures in every cross-engine comparison, which is the recomputed series in `tables/NUMBERS.md`. Where the stored series is quoted, as in the historical account of §6.3, the text says so. Any figure carried over from an earlier internal note without this harmonisation is wrong for the purpose of comparing arms, and this is the same defect the paper is about, reproduced one level up in our own reporting.

## 15. The aggregation correlation of 0.706

The lowest rank correlation among defensible aggregations, 0.706, is the harmonic against the weighted mean. Geometric against weighted is 0.787. Earlier internal notes attached 0.706 to the wrong pair; the manuscript states the minimum without naming a pair, and Table E10 carries the full matrix.

## 16. The index was recomputed on the declared cut (2026-09-11)

The values of the index section came from a run ending 2026-08-31 while the captions declared the series to 2026-09-08, and no script in the package recomputed them. `stats/s6_index.py` now does, reusing the shared extractor, with zero identity mismatches on 61,189 rows. The figures that moved, with the superseded value declared beside each in the text:

| Quantity | Published | Recomputed |
|---|---:|---:|
| Lowest correlation between defensible aggregations | 0.706 | 0.752 |
| Highest | 0.984 | 0.985 |
| Variance of the log index carried by coverage | 74.7% | 72.4% |
| Maximum rank displacement | 10 | 14 |
| Entities holding their exact rank | 7 | 9 |

One claim did not survive: the harmonic mean no longer reproduces the coverage ordering exactly (rho 0.9997, ten of 66 entities swapping with a neighbour). A second finding came out of the exercise: the published table was assembled from two different runs, since the variance shares reproduce only under the older cut and the rank counts only under the six-arm panel.
