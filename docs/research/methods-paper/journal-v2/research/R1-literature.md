# R1 — Literature base for the journal version of BRGEO-1

Paper: *BRGEO-1: An Open Protocol for Measuring Entity Citation in Generative Engines*
Source manuscript: `docs/research/methods-paper/MANUSCRIPT.md` (v1.0, September 2026, 47 references)
Prepared: 2026-09-11

## Verification method

Every identifier below was resolved against a primary record, not against memory and not
against a secondary summary.

- **arXiv** identifiers: resolved through the arXiv Atom API (`export.arxiv.org/api/query?id_list=...`),
  which returns arXiv's own title, author list, submission date, journal reference and author comment.
- **DOIs**: resolved through the Crossref REST API (`api.crossref.org/works/<doi>`), which returns the
  registrant's title, container title, volume, issue, pages and issued date.
- **RFC 8174**: resolved against the canonical text at `rfc-editor.org/rfc/rfc8174.txt` after Crossref
  returned a variant title.
- Candidate works suggested by a literature-search LLM were treated as leads only. A large share of
  those suggestions carried fabricated author names or fabricated identifiers; nothing entered
  section B without an independent resolution. Where a venue claim rests only on an arXiv author
  comment rather than on a publisher record, that is stated in the entry.

Status vocabulary (Portuguese, as requested): **VERIFICADA**, **CORRIGIR: <o que está errado>**,
**NAO VERIFICADA**.

---

## A. Existing references (v1.0), verification status

| [n] | Short citation | Identifier | Status |
|---|---|---|---|
| 1 | Aggarwal et al., 2024, GEO: Generative Engine Optimization, KDD '24, 5–16 | 10.1145/3637528.3671900 | VERIFICADA — title, venue, pages and year confirmed. Preprint is arXiv:2311.09735 if a dual citation is wanted. |
| 2 | Bagga et al., 2025, E-GEO: A Testbed for Generative Engine Optimization in E-Commerce | arXiv:2511.20867 | VERIFICADA |
| 3 | Yu, Yang, Ding, Sato, 2026, Structural Feature Engineering for GEO | arXiv:2603.29979 | VERIFICADA |
| 4 | Sielinski, 2026, Quantifying Uncertainty in AI Visibility | arXiv:2603.08924 | VERIFICADA — now at v3. Author has a 2026 follow-up (see B.2) that should be cited alongside it. |
| 5 | Schulte, Bleeker, Kaufmann, 2026, Don't Measure Once | arXiv:2604.07585 | VERIFICADA |
| 6 | Zhang, He, Yao, 2026, From Citation Selection to Citation Absorption | arXiv:2604.25707 | VERIFICADA |
| 7 | Varga, 2026, Per-Entity Bias Mapping for AI Visibility | arXiv:2606.21595 | VERIFICADA — arXiv comment also records a Zenodo deposit, 10.5281/zenodo.20419277, usable as a data citation. |
| 8 | Kumar, 2026, Generative Engine Optimization at Scale | arXiv:2606.20065 | VERIFICADA |
| 9 | Martinez, 2026, Optimizing Visibility in Generative Engines: A Critical Survey (2023–2026) | arXiv:2607.14035 | VERIFICADA — arXiv renders the year range with a hyphen, the manuscript with an en dash. Cosmetic only. |
| 10 | Rashkin et al., 2023, Measuring Attribution in NLG Models, Comput. Linguist. 49(4), 777–840 | 10.1162/coli_a_00486 | VERIFICADA |
| 11 | Liu, Zhang, Liang, 2023, Evaluating Verifiability in Generative Search Engines, Findings EMNLP, 7001–7025 | 10.18653/v1/2023.findings-emnlp.467 | VERIFICADA |
| 12 | Gao, Yen, Yu, Chen, 2023, Enabling LLMs to Generate Text with Citations, EMNLP, 6465–6488 | 10.18653/v1/2023.emnlp-main.398 | VERIFICADA |
| 13 | Venkit et al., 2024, Search Engines in an AI Era | arXiv:2410.22349 | VERIFICADA |
| 14 | Venkit et al., 2025, DeepTRACE | arXiv:2509.04499 | VERIFICADA |
| 15 | Jung, Gonen, 2026, PhantomBench | arXiv:2606.11105 | VERIFICADA |
| 16 | Bang et al., 2025, HalluLens, ACL 2025, 24128–24156 | 10.18653/v1/2025.acl-long.1176 | VERIFICADA |
| 17 | Kirichenko, Ibrahim, Chaudhuri, Bell, 2025, AbstentionBench | arXiv:2506.09038 | VERIFICADA |
| 18 | Pan et al., "2026", Can LLMs Refuse Questions They Do Not Know? | arXiv:2510.01782 | **CORRIGIR: ano errado.** The preprint was submitted in October 2025, not 2026. The arXiv record also states acceptance at ICLR 2026. Cite either as `Pan, W., et al., 2025. ... arXiv:2510.01782` or, preferably, upgrade to the conference version: `Pan, W., et al., 2026. ..., in: Proceedings of the International Conference on Learning Representations (ICLR 2026). arXiv:2510.01782`. |
| 19 | Ji et al., 2023, Survey of Hallucination in NLG, ACM CSUR 55(12), 1–38 | 10.1145/3571730 | VERIFICADA |
| 20 | Huang et al., 2025, A Survey on Hallucination in LLMs, ACM TOIS | 10.1145/3703155 | **CORRIGIR: referência incompleta.** Crossref records volume 43, issue 2, pages 1–55. Elsevier style expects them. |
| 21 | Jacobs, Wallach, 2021, Measurement and Fairness, FAccT '21, 375–385 | 10.1145/3442188.3445901 | VERIFICADA |
| 22 | Raji, Denton, Bender, Hanna, Paullada, 2021, AI and the Everything in the Whole Wide World Benchmark | (nenhum) | **CORRIGIR: ordem de autores errada e identificador ausente.** The canonical author order is Raji, I.D., Bender, E.M., Paullada, A., Denton, E., Hanna, A. Add `arXiv:2111.15366`. The arXiv record confirms acceptance in the NeurIPS 2021 Datasets and Benchmarks track, so the venue as written is correct. |
| 23 | Bowman, Dahl, 2021, What Will it Take to Fix Benchmarking in NLU?, NAACL-HLT, 4843–4855 | 10.18653/v1/2021.naacl-main.385 | VERIFICADA |
| 24 | Reiter, 2018, A Structured Review of the Validity of BLEU, Comput. Linguist. 44(3), 393–401 | 10.1162/coli_a_00322 | VERIFICADA |
| 25 | Bean et al., 2025, Measuring what Matters: Construct Validity in LLM Benchmarks | arXiv:2511.04703 | VERIFICADA — arXiv comment confirms NeurIPS 2025 Datasets and Benchmarks track. |
| 26 | Hochlehnert et al., 2025, A Sober Look at Progress in Language Model Reasoning | arXiv:2504.07086 | VERIFICADA — arXiv comment confirms COLM 2025. |
| 27 | Encarnación, Behzad, Lurie, Metaxa, 2026, What Current AI Benchmarks Leave Unmeasured | arXiv:2608.06202 | VERIFICADA |
| 28 | Breuer, Keller, Schaer, 2022, ir_metadata, SIGIR '22, 3078–3089 | 10.1145/3477495.3531738 | VERIFICADA |
| 29 | Ferro et al., 2016, Increasing Reproducibility in IR, SIGIR Forum 50(1), 68–82 | 10.1145/2964797.2964808 | VERIFICADA — Crossref carries the short title "Increasing Reproducibility in IR"; the full subtitle in the manuscript matches the published article. |
| 30 | Ghosh et al., 2026, Evaluation Cards | arXiv:2606.09809 | VERIFICADA |
| 31 | Mitchell et al., 2019, Model Cards for Model Reporting, FAT* '19, 220–229 | 10.1145/3287560.3287596 | VERIFICADA |
| 32 | Gebru et al., 2021, Datasheets for Datasets, CACM 64(12), 86–92 | 10.1145/3458723 | VERIFICADA |
| 33 | Metaxa et al., 2021, Auditing Algorithms, FnT HCI 14(4), 272–344 | 10.1561/1100000083 | VERIFICADA |
| 34 | Liang et al., 2023, Holistic Evaluation of Language Models, TMLR | arXiv:2211.09110 | VERIFICADA — the arXiv journal reference states "Published in Transactions on Machine Learning Research (TMLR), 2023", so the 2023 year with a 2022 preprint ID is correct. |
| 35 | Muennighoff, Tazi, Magne, Reimers, 2023, MTEB, EACL, 2014–2037 | 10.18653/v1/2023.eacl-main.148 | VERIFICADA |
| 36 | Thakur et al., 2021, BEIR | arXiv:2104.08663 | VERIFICADA — arXiv comment confirms NeurIPS 2021 Datasets and Benchmarks track. |
| 37 | Enevoldsen et al., 2025, MMTEB | arXiv:2502.13595 | VERIFICADA — arXiv comment confirms ICLR acceptance. |
| 38 | Craswell, Mitra, Yilmaz, Campos, Voorhees, 2020, Overview of the TREC 2019 Deep Learning Track | arXiv:2003.07820 | VERIFICADA — arXiv renders the title in sentence case ("deep learning track"). Cosmetic. |
| 39 | Voorhees, 2000, Variations in relevance judgments..., IP&M 36(5), 697–716 | 10.1016/S0306-4573(00)00010-8 | VERIFICADA |
| 40 | Bailey, Moffat, Scholer, Thomas, 2016, UQV100, SIGIR '16, 725–728 | 10.1145/2911451.2914671 | VERIFICADA — Crossref stores the short title "UQV100"; the full title in the manuscript matches the published paper. |
| 41 | Liu et al., 2024, Lost in the Middle, TACL 12, 157–173 | 10.1162/tacl_a_00638 | VERIFICADA |
| 42 | Guo, Vosoughi, 2024, Serial Position Effects of Large Language Models | arXiv:2406.15981 | VERIFICADA |
| 43 | Menschikov et al., 2025, Beyond Early-Token Bias | arXiv:2505.16134 | VERIFICADA |
| 44 | Nardo et al., 2008, Handbook on Constructing Composite Indicators, OECD | 10.1787/9789264043466-en | VERIFICADA — the OECD Crossref record carries no author list, which is normal for OECD monographs; title and year confirmed. |
| 45 | Bradner, 1997, RFC 2119 | 10.17487/RFC2119 | VERIFICADA |
| 46 | Leiba, 2017, Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words, RFC 8174 | 10.17487/RFC8174 | VERIFICADA — Crossref returns a different string ("RFC 2119 Key Words: Clarifying the Use of Capitalization"), but the canonical RFC Editor text confirms the title exactly as written in the manuscript. Do not "correct" this. |
| 47 | Ferro, Kelly, 2018, SIGIR Initiative to Implement ACM Artifact Review and Badging, SIGIR Forum 52(1), 4–10 | 10.1145/3274784.3274786 | VERIFICADA |

**Summary.** 44 of 47 verified without change. Three require editing: [18] (wrong year, upgradeable
to ICLR 2026), [20] (missing volume, issue and pages), [22] (wrong author order, missing identifier).
No reference in v1.0 was found to be non-existent.

---

## B. Proposed new references

Each entry gives the Elsevier-style bibliographic record, what the work establishes, and the section
of the paper it serves. Priority is marked **[essencial]**, **[forte]** or **[opcional]** so the set
can be pruned without re-deriving the argument.

### B.1 Direct competitors: protocols and measurement instruments for entity citation

This is the cluster that decides whether the paper's novelty claim survives review. Three of these
postdate the v1.0 literature cut and at least one proposes a standardised protocol in the same
problem space.

**N1 [essencial]** Żatuchin, D., 2026. The Dice Roll Method: A Standardized Protocol for
Repeated-Query Auditing of Large Language Model Brand Recommendations. arXiv:2609.04047.

Formalises a reusable protocol for repeated-query auditing of LLM brand recommendations, decomposing
total response variance into sampling, prompt-phrasing, run-to-run and model-version components. It
reanalyses five prior brand-auditing studies (roughly 190,000 observations, 270+ brands, six
languages, iteration counts 5 to 40) and derives three tiers of iteration guidance from a
generalisability-theory D-study, reporting G = 0.58 at n = 5 and G = 0.74 at n = 10.
*Where it enters:* §2.1 and §9. This is the closest published analogue to BRGEO-1 and it is dated
2026-09-03, i.e. after the v1.0 manuscript was written. The paper must position against it
explicitly: the Dice Roll Method standardises *how many times you ask*, BRGEO-1 standardises *what
the instrument reads and over which cohort*. The two are complementary and the complementarity
should be stated, not implied. It also supplies external support for §7.1 (model-version as a
variance component) and for the H-series in §9.

**N2 [essencial]** Sielinski, R., 2026. From Stochastic to Stable: Rank Stability and Structural
Sufficiency in AI Visibility Measurement. arXiv:2607.10341.

Introduces a sequential convergence framework with two criteria — rank stability, testing whether the
rank-correlation trajectory has reached a plateau, and structural sufficiency, testing whether the
spread of citation shares among domains whose confidence intervals exclude zero exceeds the
uncertainty of those estimates — to decide when enough data has been collected.
*Where it enters:* §2.1 (extends the existing [4] citation from the same author) and §8.3. It is the
strongest available answer to the reviewer question "how do you know 50 days and 66,399 observations
is enough?", and it gives a principled counterpart to the rank-displacement statistics reported in
§8.3.

**N3 [essencial]** Żatuchin, D., 2026. Where Does the Noise Come From? A Variance-Components
Decomposition of Non-Determinism in LLM Brand Answers. arXiv:2607.13304.

Specifies a crossed random-effects decomposition partitioning the variance of a response-level brand
outcome into within-prompt resampling, prompt paraphrase, model identity and query language, applied
to a fully crossed corpus of 12,933 responses across 20 brands, 8 languages and 3 models, with a
stability subset of 1,435 cells resampled about five times. The abstract reports query language as the
largest systematic factor.
*Where it enters:* §2.1 and §11. Directly relevant to the bilingual battery of P3 and to the
"market, language and model tier" threat. It also shows that the field already has a variance
vocabulary BRGEO-1 does not use; the paper should either adopt it or say why the window parameter is
prior to it.

**N4 [forte]** Żatuchin, D., 2026. The Language Blind Spot: How Query Language and Brand Recognition
Tier Shape AI-Constructed Brand Reputation Across Twelve European Languages. arXiv:2606.23165.

Queries three grounded LLMs about 66 brands from eleven European markets in twelve languages across
four language families, generating 35,640 responses, and reports that cross-language mean cosine
similarity is 0.825, that same-family responses are more similar than cross-family (0.844 vs 0.820,
d = 0.31), and that sentiment varies by language (F = 268.5, eta² = 0.077).
*Where it enters:* §4 ("Why a Brazilian instantiation") and §11. It is the best external evidence
that an English-only instrument is not representative, which is exactly the argument §4 makes from
first principles rather than from data.

**N5 [forte]** Huang, J., Situ, R., Ye, R., 2026. Cultural Encoding in Large Language Models: The
Existence Gap in AI-Mediated Brand Discovery. arXiv:2601.00869.

Analyses 1,909 English-only queries across six LLMs and 30 brands and reports that Chinese-developed
models mention brands at 88.9% against 58.3% for international models, a 30.6 percentage point gap
that persists under identical English queries. Introduces the "Existence Gap": brands absent from
training corpora have no presence in model answers regardless of quality.
*Where it enters:* §4 and §6.1. The existence gap is the positive-side mirror of the decoy
instrument — BRGEO-1 measures the false-positive floor, this work measures the false-negative
ceiling for entities that postdate or fall outside the training corpus. It supports the cohort design
choice of deliberately including firms founded after 2020.
*Note:* the arXiv submission timestamp is 2025-12-30 while the identifier is in the 2601 (January
2026) block. Cite as 2026 to match the identifier.

**N6 [forte]** Żatuchin, D., 2026. Who Owns the AI Recommendation? A Multi-Industry Empirical Map of
Brand Category Ownership Across Large Language Models. arXiv:2606.23057.

Uses 3,750 responses across 50 brands, five industries and 250 brand-free category queries on three
models, each query repeated five times, to propose a Category Ownership Index, a Competitive Vacuum
Index and a Displacement Score.
*Where it enters:* §8. This is a live example of the composite-index proliferation §8.4 warns about,
and citing it makes the warning concrete rather than rhetorical.

**N7 [forte]** Chu, X., Hou, Y., 2026. Incumbent Advantage: Brand Bias and Cognitive Manipulation
Dynamics in LLM Recommendation Systems. arXiv:2606.17443.

Three experiments on skincare across GPT-4o-mini, Claude Sonnet and Gemini 3 Flash report a
"Conditional Monopoly" in which well-known brands are recommended 100% of the time when product
specifications are held identical, and that this dominance collapses under a rating advantage of less
than +0.1 stars for a competitor.
*Where it enters:* §2.1 and §11. Evidence that citation rate is sensitive to cohort composition —
which is why P2 fixes the cohort before collection — and a counterweight to the objection that
measuring citation rate is a purely descriptive exercise.

### B.2 GEO benchmarks, testbeds and governance

**N8 [forte]** Nimase, O., Chen, Z., Qi, G., Zhao, Y., Hu, X., 2026. GEO-Bench: Benchmarking Ranking
Manipulation in Generative Engine Optimization. arXiv:2605.29107.

Unifies black-box prompt attacks, white-box gradient attacks and ten white-hat content strategies
under one protocol, scored on five datasets against a fixed open-weight ranker.
*Where it enters:* §2.1. Note for the author: this shares a name with Aggarwal et al.'s GEO-bench
[1] and is a different artefact. The Related work section should disambiguate, because a reviewer
who knows one will assume the other.

**N9 [forte]** Wu, Y., Zhong, S., Kim, Y., Xiong, C., 2025. What Generative Search Engines Like and
How to Optimize Web Content Cooperatively. arXiv:2510.11438.

An open-domain GEO benchmark studying which content features affect source selection in generative
search.
*Where it enters:* §2.1, alongside [2] and [3], to establish that the testbed line of work optimises
content and does not standardise the instrument.

**N10 [essencial]** Wen, Y., Zhang, N., Yuan, H., Chen, X., Zhang, H., Guo, H., 2026. Position:
Generative Engine Optimization Creates Underexamined Risks, Governance Must Target Concentration,
Disclosure, and Academic Blind Spots, in: Proceedings of the International Conference on Machine
Learning (ICML 2026), Position Paper Track. arXiv:2606.12439.

Identifies three risks in the SEO-to-GEO transition — concentrated influence from low contestability,
undisclosed commercial influence embedded in evidence and reasoning, and academic-industry blind
spots driven by evaluation asymmetries between offline setups and deployed systems — and argues for
answer-level governance, black-box auditing of material influence and deployment-aligned metrics.
*Where it enters:* §1, §10 and §12. This is the field's own statement that measurement standards are
needed, published at a top venue, and it is the single most useful citation for justifying why a
protocol paper belongs in a journal rather than in a vendor white paper. It also anticipates the
competing-interest question the paper answers in its declaration.

**N11 [opcional]** Liu, Z., Xu, P., 2026. Think Before Writing: Feature-Level Multi-Objective
Optimization for Generative Citation Visibility. arXiv:2604.19113.

Feature-level multi-objective optimisation for citation visibility.
*Where it enters:* §2.1, as one more instance of the optimisation line, only if the Related work
section wants density there.

### B.3 Auditing deployed generative search: the empirical baseline

BRGEO-1 currently cites almost no large-scale measurement of deployed AI search. A Q1 reviewer in
IP&M will expect it.

**N12 [essencial]** Xu, H., Iqbal, U., Montgomery, J.M., 2026. Measuring Google AI Overviews:
Activation, Source Quality, Claim Fidelity, and Publisher Impact. arXiv:2605.14021.

A longitudinal measurement study issuing 55,393 trending queries across 19 topical categories over a
40-day window (13 March to 21 April 2026). Reports AI Overview activation at 13.7% overall and 64.7%
for question-form queries; that nearly 30% of AIO-cited domains do not appear in the co-displayed
first-page results; and that of 98,020 atomic claims, 11.0% are unsupported by the cited pages, with
omission the dominant failure mode.
*Where it enters:* §2.2 and §12. It is the methodological peer of BRGEO-1's own series — comparable
scale, declared window, published category stratification — and gives the paper a reference point for
"this is what a well-reported measurement study of a generative engine looks like".

**N13 [forte]** Hu, D., Baumann, J., Urman, A., Lichtenegger, E., Forsberg, R., Hannak, A., et al.,
2026. Auditing Google's AI Overviews and Featured Snippets: A Case Study on Baby Care and Pregnancy,
in: Proceedings of the International AAAI Conference on Web and Social Media (ICWSM 2026).
arXiv:2511.12920.

Domain-specific audit of AI Overviews and featured snippets.
*Where it enters:* §2.5, extending the algorithm-auditing genealogy of [33] into the generative
setting with a recent, peer-reviewed instance.

**N14 [forte]** Grossman, R., Liu, S., Chen, M.K., Smith, M., Borcea, C., Chen, Y., 2026. How
Generative AI Disrupts Search: An Empirical Study of Google Search, Gemini, and AI Overviews, in:
Proceedings of the 49th International ACM SIGIR Conference on Research and Development in Information
Retrieval (SIGIR 2026). arXiv:2604.27790.

Empirical comparison of classical search, Gemini and AI Overviews.
*Where it enters:* §1. Supplies a peer-reviewed SIGIR citation for the opening claim that answer
reading is displacing link reading, which currently rests on assertion.

**N15 [essencial]** Khosravi, M., Yoganarasimhan, H., 2026. Impact of AI Search Summaries on Website
Traffic: Evidence from Google AI Overviews and Wikipedia. arXiv:2602.18455.

A difference-in-differences design exploiting the staggered geographic rollout of AI Overviews and
Wikipedia's multilingual structure, comparing monthly external-search referrals to English Wikipedia
against the same articles in German and French. Finds that default AIO availability reduced English
search traffic by 5.45% and 4.82% respectively.
*Where it enters:* §1. The paper's premise — that being named in an answer carries economic
consequence — is currently stated without evidence. This is a clean causal estimate of the
displacement side of that premise and it makes the introduction defensible.

**N16 [forte]** Watanabe, K., Nakayashiki, K., 2026. Disentangling Answer Engine Optimization from
Platform Growth: A Log-Based Natural Experiment on ChatGPT Referral Traffic. arXiv:2606.04362.

A single-domain longitudinal field study using first-party analytics and server logs rather than
third-party estimators, with untreated pages on the same domain as a contemporaneous control. Reports
that total ChatGPT referrals grew 5.7x while untreated pages on the same domain grew 3.5x over the
same window, so raw growth is dominated by the platform tailwind.
*Where it enters:* §1 and §12. The cleanest published demonstration that headline figures in this
market are confounded, which is the paper's motivating claim, established by an independent route.

**N17 [forte]** Lurie, E., Encarnación, R., Friedler, S.A., Metaxa, D., 2026. The Beginning of
ChatGPT Ads, in: Proceedings of the AAAI/ACM Conference on AI, Ethics, and Society (AIES 2026).
arXiv:2608.05008.

*Where it enters:* §1 and §10. Same research group as the existing [27]. Commercial placement inside
generative answers changes what a citation rate means and raises the stakes of an unstandardised
metric; this is the citation that makes the governance argument in §10 timely rather than abstract.

**N18 [forte]** Morosini, A., Cen, S.H., Ilyas, A., Driss, H., Mądry, A., Podimata, C., 2026. Using
AI Agents to Automate Black-Box Audits of Personalization Algorithms at Scale. arXiv:2606.30801.

*Where it enters:* §2.5 and §10. Method precedent for automated black-box auditing at scale, which is
what a BRGEO-1 conformance test suite would have to be.

**N19 [essencial]** Mosnar, M., Skurla, A., Pecher, B., Tibensky, M., Jakubcik, J., Bindas, A.,
Sakalik, P., Srba, I., 2025. Revisiting Algorithmic Audits of TikTok: Poor Reproducibility and
Short-Term Validity of Findings, in: Proceedings of the International ACM SIGIR Conference on
Research and Development in Information Retrieval (SIGIR 2025). arXiv:2504.18140.
*Venue note:* the arXiv comment states "ACM SIGIR 2025" without an ordinal; confirm the proceedings
ordinal and pages from the ACM record before submission.

Reproduction attempt on published algorithmic audits finding poor reproducibility and short-term
validity of the original findings.
*Where it enters:* §2.5, §7 and §10. This is the empirical case for the paper's central claim that
audits of commercial systems do not reproduce unless the conditions are pinned, made in an IR venue
by an independent group. It is also the natural citation for §10's admission that BRGEO-1 has no
inter-implementation reproducibility evidence yet.

**N20 [opcional]** Damião, Í., Reis, J.M., Almeida, P., Santos, N., Gonçalves-Sá, J., 2025. Digital
Gatekeeping: An Audit of Search Engine Results Shows Tailoring of Queries on the Israel-Palestine
Conflict. arXiv:2502.04266.

*Where it enters:* §2.5, if the Related work section wants a second auditing instance showing
query-level and locale-level tailoring.

### B.4 Non-determinism, drift and reproducibility of LLM measurement

The manuscript leans on [26] and [27] for this. The line is much better developed than v1.0 suggests,
and a reviewer will know it.

**N21 [essencial]** Atıl, B., Aykent, S., Chittams, A., Fu, L., Passonneau, R.J., Radcliffe, E., et
al., 2025. Non-Determinism of "Deterministic" LLM System Settings in Hosted Environments, in:
Proceedings of the 5th Workshop on Evaluation and Comparison of NLP Systems (Eval4NLP), pp. 135–148.
https://doi.org/10.18653/v1/2025.eval4nlp-1.12

Establishes that temperature-0 and fixed-seed settings do not make hosted LLM outputs deterministic.
*Where it enters:* §4 (Table 2, P5 generation configuration) and §7.1. BRGEO-1 sets temperature 0.0
and presents that as pinning the configuration. This work shows that pinning the configuration does
not pin the output, which the paper should concede rather than have a reviewer raise. The preprint is
arXiv:2408.04667 under a slightly different title; cite the published version.

**N22 [essencial]** Chen, L., Zaharia, M., Zou, J., 2024. How Is ChatGPT's Behavior Changing Over
Time? Harvard Data Science Review 6 (2). https://doi.org/10.1162/99608f92.5317da47

The canonical demonstration that a commercial model changes behaviour under a stable product name.
*Where it enters:* §3.1 (P4, pinned versions) and §7.1. P4's entire rationale — "providers update the
model behind a stable product name without notice" — is currently asserted without a citation. This
is the citation.

**N23 [forte]** Coqueret, G., Llull, J., Oswald, F., Pérignon, C., Scheuch, C., Vilhuber, L., 2026.
Randomness in Large Language Models: What Researchers Need to Know (and Report). arXiv:2607.24372.

Distinguishes deliberate sampling from silent model updates, numerical rounding and expert routing,
and concludes that exact reproduction is generally not possible through proprietary APIs even at
temperature zero.
*Where it enters:* §3.1 (P5), §5.5 and §10. It is a reporting-practice paper, so it sits naturally
beside [28]–[32] as well, and its conclusion strengthens rather than weakens the case for retaining
full responses: if outputs cannot be regenerated, the stored text is the only reproducible artefact.

**N24 [forte]** Ouyang, S., Zhang, J.M., Harman, M., Wang, M., 2025. An Empirical Study of the
Non-Determinism of ChatGPT in Code Generation. ACM Transactions on Software Engineering and
Methodology 34 (2), 1–28. https://doi.org/10.1145/3697010

Large-scale measurement of output variation at temperature 0 in a hosted model.
*Where it enters:* §7.1, as the peer-reviewed journal instance of the same phenomenon, useful because
IP&M reviewers weight journal evidence.

**N25 [opcional]** Cui, J., Alexander, R., 2026. Same Prompt, Different Outcomes: Evaluating the
Reproducibility of Data Analysis by LLMs. arXiv:2602.14349.

480 attempts across two prompting strategies, six models, four temperature settings and ten
independent executions per configuration; finds substantial variation in analytical results even
within a fixed configuration, and recommends reporting a distribution rather than a point result.
*Where it enters:* §5.1, as support for the distributional framing that [5] also argues for.

**N26 [opcional]** Song, Y., Wang, G., Li, S., Lin, B.Y., 2024. The Good, The Bad, and The Greedy:
Evaluation of LLMs Should Not Ignore Non-Determinism. arXiv:2407.10457.

*Where it enters:* §9, as prior support for reporting inferential results over repeated runs.

### B.5 Attribution and citation auditing

**N27 [forte]** Alaofi, M., Arabzadeh, N., Clarke, C.L.A., Sanderson, M., 2024. Generative
Information Retrieval Evaluation, in: Shah, C., White, R. (Eds.), Information Access in the Era of
Generative AI. Springer. arXiv:2404.08137.

A book chapter surveying evaluation of generative IR systems from two directions: LLMs as assessors,
and the evaluation of LLM-based generative retrieval systems end to end.
*Where it enters:* §2.2 and §2.5. It is the bridge between the paper's IR genealogy ([38]–[40]) and
its generative-engine subject, and it is written by IR insiders, which matters for an IR journal.
*Venue note:* the book association comes from the arXiv author comment; confirm the final chapter
pages and book DOI before submission.

**N28 [opcional]** Agrawal, A., Suzgun, M., Mackey, L., Kalai, A.T., 2024. Do Language Models Know
When They're Hallucinating References?, in: Findings of the Association for Computational
Linguistics: EACL 2024, pp. 912–928. https://doi.org/10.18653/v1/2024.findings-eacl.62

*Where it enters:* §6.2, as prior work on a model's own signal about fabricated entities, relevant to
the unvalidated fabrication detector.

**N29 [opcional]** Zhao, Z., Wang, Y., Stuart, T., De Vaan, M., Ginsparg, P., Yin, Y., 2026. LLM
Hallucinations in the Wild: Large-Scale Evidence from Non-Existent Citations. arXiv:2605.07723.

*Where it enters:* §6.1. Large-scale use of non-existent items as observable evidence, the closest
published analogue to the decoy instrument, though applied to bibliographic references rather than to
firms.

### B.6 Abstention, refusal and non-existent entities

**N30 [essencial]** Wen, B., Yao, J., Feng, S., Xu, C., Tsvetkov, Y., Howe, B., et al., 2025. Know
Your Limits: A Survey of Abstention in Large Language Models. Transactions of the Association for
Computational Linguistics 13, 529–556. https://doi.org/10.1162/tacl_a_00754

The survey of abstention in LLMs, in a top journal.
*Where it enters:* §6.2. The three-way taxonomy (ontological refusal, epistemic refusal, fabrication)
is currently proposed without reference to the abstention literature's own categories. A reviewer will
ask how it relates to them. Citing this survey and stating the mapping — or stating explicitly where
the taxonomy departs from it and why — converts a weakness into a contribution.

**N31 [forte]** Zhao, W., Goyal, T., Chiu, Y.Y., Jiang, L., Newman, B., Ravichander, A., et al.,
2024. WildHallucinations: Evaluating Long-Form Factuality in LLMs with Real-World Entity Queries.
arXiv:2407.17468.

Evaluates long-form factuality using real-world entity queries.
*Where it enters:* §6.1. It is the entity-level counterpart to [15]–[18], which are question-level,
and it makes the point that entity queries are a distinct evaluation surface.
*Venue note:* no publisher DOI resolved; cite as a preprint, or confirm the conference version before
submission.

### B.7 Construct validity, measurement theory and benchmark critique

**N32 [essencial]** Borsboom, D., Mellenbergh, G.J., van Heerden, J., 2004. The Concept of Validity.
Psychological Review 111 (4), 1061–1071. https://doi.org/10.1037/0033-295X.111.4.1061

The psychometric source for the position that validity is a property of the causal relation between
attribute and measurement outcome, not of the evidence assembled about a test.
*Where it enters:* §2.4, upstream of [21]. Jacobs and Wallach import measurement modelling into
computing; this is where it comes from. A measurement paper in IP&M that cites the derivative work
and not the source will be read as having encountered the idea secondhand.

**N33 [forte]** Salaudeen, O., Reuel, A., Ahmed, A., Bedi, S., Robertson, Z., Sundar, S., et al.,
2025. Measurement to Meaning: A Validity-Centered Framework for AI Evaluation. arXiv:2505.10573.

A validity-centred framework for reasoning about what an AI evaluation licenses one to conclude.
*Where it enters:* §2.4 and §3.3. It gives vocabulary for the conformance-level argument: BRGEO-1's
levels are about attestation, and this framework separates that axis from the validity axis, which is
exactly the distinction §3.3 makes informally.

**N34 [forte]** Jiang, H., Zhang, S., Zhu, D., Bai, Y., Truong, S.T., Yi, X., Koyejo, S., Xie, X.,
Xiao, Z., 2026. AI Evaluation Should Require Standardized Item-Level Data Releases. arXiv:2604.03244.

Position paper arguing that aggregate model scores are the root cause of underspecified item
selection and construct misalignment, and that standardised item-level data release should be default
evaluation infrastructure.
*Where it enters:* §8.4 and §10. This is independent support for the paper's own conclusion —
publish the components, treat the composite as subordinate — argued from a different starting point.
It is the strongest available external validation of §8.4 and should be cited there explicitly.

**N35 [opcional]** Ye, H., Jin, J., Xie, Y., Zhang, X., Song, G., 2025. Large Language Model
Psychometrics: A Systematic Review of Evaluation, Validation, and Enhancement. arXiv:2505.08245.

*Where it enters:* §2.4, as a systematic-review anchor alongside [25].

**N36 [opcional]** Xu, C., Guan, S., Greene, D., Kechadi, M-T., 2024. Benchmark Data Contamination of
Large Language Models: A Survey. arXiv:2406.04244.

*Where it enters:* §11. Contamination is the mechanism behind the "awareness gap" the cohort design
probes by including firms founded after 2020; naming it makes that design choice legible.

### B.8 Reporting standards and reproducibility infrastructure

**N37 [forte]** Dhar, R., Sanchez Villegas, D., Karamolegkou, A., Schiavone, A., Yuan, Y., Chen, X.,
et al., 2025. EvalCards: A Framework for Standardized Evaluation Reporting. arXiv:2511.21695.

*Where it enters:* §2.5 and §3.4. A structured reporting format contemporaneous with [30]. Citing
both establishes that structured declaration is a converging practice rather than an idiosyncrasy of
this paper, which is the argument §3.4 needs.

**N38 [forte]** Breuer, T., Ferro, N., Maistro, M., Schaer, P., 2021. repro_eval: A Python Interface
to Reproducibility Measures of System-Oriented IR Experiments, in: Advances in Information Retrieval
(ECIR 2021), Lecture Notes in Computer Science, pp. 481–486.
https://doi.org/10.1007/978-3-030-72240-1_51

Operationalises reproducibility measures for system-oriented IR experiments as runnable software.
*Where it enters:* §10. §10 states that a conformance test suite does not yet exist. This is the IR
community's existing answer to the same problem and the natural model for what BRGEO-1's suite should
look like. Citing it converts "future work" into a specified piece of future work.

**N39 [opcional]** Breuer, T., Maistro, M., 2024. Toward Evaluating the Reproducibility of
Information Retrieval Systems with Simulated Users, in: Proceedings of the 2nd ACM Conference on
Reproducibility and Replicability, pp. 25–29. https://doi.org/10.1145/3641525.3663619

*Where it enters:* §10, second-order support for the same argument.

**N40 [opcional]** Aloqalaa, M., Soiland-Reyes, S., Goble, C., 2026. PRIMAD-LID: A Developed
Framework for Computational Reproducibility. arXiv:2601.02349.

*Where it enters:* §2.5. The manuscript cites the PRIMAD model through [29]; this is its current
development and shows the line is live.

**N41 [opcional]** Adel, T., Bilson, S., Levene, M., Thompson, A., 2024. Trustworthy Artificial
Intelligence in the Context of Metrology, in: Ferreira, M.I.A. (Ed.), Producing Artificial Intelligent
Systems: The Roles of Benchmarking, Standardisation and Certification, Studies in Computational
Intelligence. Springer. arXiv:2406.10117.

*Where it enters:* §3.3 and §10. The paper invokes ISO/IEC 17000 and ISO 5725 without any citation
into the metrology-for-AI literature. This chapter supplies one and links benchmarking,
standardisation and certification in the same frame the conformance levels use.

### B.9 Position effects in generated output

§2.6 currently covers position in the input and then asserts that the output analogue is
under-studied. That assertion is no longer safe.

**N42 [essencial]** Hou, Y., Zhang, J., Lin, Z., Lu, H., Xie, R., McAuley, J., Zhao, W.X., 2024.
Large Language Models Are Zero-Shot Rankers for Recommender Systems, in: Advances in Information
Retrieval (ECIR 2024), Lecture Notes in Computer Science, pp. 364–381.
https://doi.org/10.1007/978-3-031-56060-6_24

Establishes that LLMs used as rankers are sensitive to the order of candidates and to popularity, and
that the ordering they emit is not a neutral function of the input.
*Where it enters:* §2.6 and §5.4. The nearest IR-venue precedent for the paper's claim that where an
entity appears in a generated answer is itself a measurement-bearing quantity.

**N43 [forte]** Bito, E., Ren, Y., He, E., 2025. Evaluating Position Bias in Large Language Model
Recommendations. arXiv:2508.02020.

**N44 [forte]** Bito, E., Ren, Y., He, E., 2026. Position Bias Undermines Preference Consistency in
Listwise LLM-Based Reranking, in: Proceedings of the ACM Conference on Recommender Systems (RecSys
2026). arXiv:2608.03091.

Together these establish position bias in LLM-generated recommendation and reranking output as a
measured, venue-accepted phenomenon.
*Where it enters:* §2.6 and §5.4. §5.4's finding — that susceptibility to the observation window
tracks per-model response style rather than architecture — is a claim about output position. These
give it a literature to sit in, and force the paper to state precisely what is new: not that output
position matters, but that the *instrument's truncation of* output position is an unreported
measurement parameter.

**N45 [forte]** Wadi, D., Ma, Y., 2026. Does Rank Still Matter? Position Bias When AI Agents Shop on
Our Behalf. arXiv:2608.22697.

Randomises the order of one hundred hotel listings across 5,000 agent sessions against four models
and human field data. Reports that position predicts inspection weakly and non-monotonically, with
the middle of the page least likely to be inspected, and that whether position reaches the choice
stage is model-specific in a way that tracks neither provider nor capability.
*Where it enters:* §5.4 and §12. The heterogeneity result is structurally identical to the paper's
own: an effect that is model-specific and not predictable from provider or architecture. Citing it
turns §5.4 from an isolated observation into an instance of a pattern others have measured.

### B.10 Composite indicators: aggregation, weighting and sensitivity

§8 currently rests on a single citation, the OECD handbook [44]. The critical literature is where the
paper's own argument already lives.

**N46 [essencial]** Saisana, M., Saltelli, A., Tarantola, S., 2005. Uncertainty and Sensitivity
Analysis Techniques as Tools for the Quality Assessment of Composite Indicators. Journal of the Royal
Statistical Society Series A: Statistics in Society 168 (2), 307–323.
https://doi.org/10.1111/j.1467-985X.2005.00350.x

The foundational statement that a composite indicator must be accompanied by uncertainty and
sensitivity analysis across defensible construction choices.
*Where it enters:* §8.3. This is precisely what Table 11 does, and the paper currently presents it as
an ad hoc robustness check rather than as an instance of an established methodology. Citing this
raises the standing of §8.3 considerably.

**N47 [essencial]** Paruolo, P., Saisana, M., Saltelli, A., 2013. Ratings and Rankings: Voodoo or
Science? Journal of the Royal Statistical Society Series A: Statistics in Society 176 (3), 609–634.
https://doi.org/10.1111/j.1467-985X.2012.01059.x

Shows that the nominal weights assigned to components of a composite index are not the weights that
actually drive the ranking, and provides the importance measures that recover the effective ones.
*Where it enters:* §8.2. Table 10 decomposes variance and finds coverage contributing 74.7%. That is
the same finding these authors formalise as the gap between nominal and effective weight. Naming it
makes the decomposition a recognised method rather than an improvised one.
*Note:* Crossref records the online-first year as 2012 and the print issue as 176(3), 2013. Cite 2013.

**N48 [forte]** Saltelli, A., 2007. Composite Indicators between Analysis and Advocacy. Social
Indicators Research 81 (1), 65–77. https://doi.org/10.1007/s11205-006-0024-9

The argument that composite indicators serve advocacy as often as analysis and must be defended
against that reading.
*Where it enters:* §8.4 and the competing-interest declaration. Given that the custodian of the
specification sells services in the domain it measures, this citation does real work: the paper is
publishing evidence against its own index, which is the response this literature prescribes.

**N49 [forte]** Greco, S., Ishizaka, A., Tasiou, M., Torrisi, G., 2019. On the Methodological
Framework of Composite Indices: A Review of the Issues of Weighting, Aggregation and Robustness.
Social Indicators Research 141 (1), 61–94. https://doi.org/10.1007/s11205-017-1832-9

Systematic review of weighting, aggregation and robustness for composite indices.
*Where it enters:* §8.1, to justify the geometric mean against the alternatives rather than asserting
its properties.
*Note:* Crossref records the online-first year as 2018; the print issue 141(1) is 2019. Cite 2019.

### B.11 Portuguese and Brazilian evaluation

The manuscript justifies a Brazilian instantiation on linguistic grounds (§4) with no citation into
Portuguese-language evaluation. That is an easy reviewer objection.

**N50 [forte]** Santos, J.G.A., Bonás, G.K., Laitz, T., Almeida, T.S., Pedrini, H., 2026. BLUEX v2:
Benchmarking LLMs on Open-Ended Questions from Brazilian University Entrance Exams. arXiv:2606.22723.

*Where it enters:* §4. A current, Brazilian-authored benchmark establishing that Brazilian-Portuguese
evaluation is an active research area rather than a convenience choice by this author.

**N51 [opcional]** Wilkens, R., Zilio, L., Villavicencio, A., 2023. Assessing Linguistic
Generalisation in Language Models: A Dataset for Brazilian Portuguese. arXiv:2305.14070.

*Where it enters:* §4. The arXiv comment states that the final version appeared in *Language
Resources and Evaluation*; obtain that DOI before submission if the journal version is preferred.

**N52 [opcional]** Hada, R., Gumma, V., de Wynter, A., Diddee, H., Ahmed, M., Choudhury, M., Bali,
K., Sitaram, S., 2024. Are Large Language Model-Based Evaluators the Solution to Scaling Up
Multilingual Evaluation?, in: Findings of the Association for Computational Linguistics: EACL 2024.
arXiv:2309.07462.

*Where it enters:* §4 and §11. Evidence that evaluation instruments themselves degrade outside
English, which is the stress-test argument §4 makes.
*Venue note:* EACL 2024 Findings acceptance comes from the arXiv author comment; confirm the
Anthology DOI before submission.

---

## C. Positioning material for an expanded Related work

Raw material, English, for §2. Each paragraph states what a line of work establishes, what it leaves
unmeasured, and where BRGEO-1 sits relative to it.

**Optimisation and its instruments.** The GEO literature that begins with Aggarwal et al. is an
optimisation literature. It asks which content modifications raise the probability that a source is
selected, and it answers with controlled rewriting against a benchmark. E-GEO extends the testbed to
commerce, structural feature engineering isolates content organisation, and the ranking-manipulation
benchmark of Nimase et al. unifies attack and white-hat strategies under one scoring protocol. What
none of this literature does is standardise the instrument that observes the outcome. Each study
fixes an evaluation harness adequate to its own comparison and reports the harness as an
implementation detail. That is defensible within a single study, where the harness is held constant
across arms, and it is exactly what breaks when figures produced under different harnesses are placed
side by side. BRGEO-1 operates one level down: it does not propose a way to increase citation, it
specifies the conditions under which a citation rate is a comparable quantity.

**Measurement of visibility has become its own line, and it has converged on sampling.** During 2026
several independent authors began treating AI visibility as a statistical estimation problem.
Sielinski first treated visibility metrics as sample estimators and then, in a follow-up, derived
convergence criteria for deciding when enough data has been collected. Schulte and colleagues argued
for characterising visibility as a distribution rather than a point. Żatuchin decomposed the variance
of brand answers into resampling, paraphrase, model identity and query language, and then formalised
a repeated-query auditing protocol with iteration guidance derived from a generalisability-theory
decomposition. The convergence is striking and it is nearly complete on one axis: how many times to
ask, and how to characterise the spread of what comes back. It is silent on a different axis: how
much of each answer the instrument reads before deciding whether an entity was named. A variance
decomposition that partitions total response variance into four sources implicitly assumes that the
response is the unit being observed. If the pipeline truncates the response at a length that differs
between providers, the decomposition is computed on four different units and the components are not
comparable across arms. BRGEO-1's contribution is prior to the sampling question rather than parallel
to it.

**Relation to the Dice Roll Method specifically.** Żatuchin's protocol and BRGEO-1 are the only two
published attempts to standardise measurement of entity mention in generative engines, and they
standardise disjoint things. The Dice Roll Method fixes iteration count, stability metric and
reliability threshold, and is agnostic about the cohort, the panel and the extraction rule. BRGEO-1
fixes the observation window, the cohort with fictitious calibration decoys, the query battery, the
engine panel with pinned versions, the generation configuration and the entity matching rule, and is
agnostic about how many repetitions to buy. A measurement declared under both would be considerably
better specified than one declared under either. The journal version should say this plainly and
should adopt the Dice Roll iteration tiers as a recommended, non-normative companion rather than
treating repetition as out of scope.

**Attribution measures a different object.** The attribution literature — Rashkin's AIS framework,
Liu's citation precision and recall, ALCE, the Venkit audits, and now the claim-level decomposition
of Xu and colleagues on AI Overviews, which finds 11.0% of 98,020 atomic claims unsupported by their
cited pages — asks whether a source that was cited supports what the answer says. That question
presupposes the entity or source has already been named. Entity citation as this paper defines it is
upstream: whether the firm appears in the answer at all. The two are not substitutes and the
commercial market reports the upstream quantity almost exclusively, which is why standardising it has
practical consequence. The attribution literature is nonetheless the right methodological neighbour,
because it is where the discipline of publishing an explicit matching and support criterion came from.

**Fictitious entities are a target elsewhere and an instrument here.** PhantomBench, HalluLens,
AbstentionBench and the knowledge-aware refusal work of Pan and colleagues all use non-existent or
unanswerable items to characterise a model's failure to abstain; the abstention survey of Wen and
colleagues organises that field. WildHallucinations moves the unit of analysis to real-world entity
queries, and the large-scale study of non-existent citations by Zhao and colleagues shows what
fabricated items look like at scale in the wild. In every case the fictitious item is what is being
measured. BRGEO-1 embeds decoys in the measured cohort so that the citation rate carries an empirical
false-positive floor produced by the same run that produced the rate. We have not located prior work
using fictitious entities this way, and the honest report of what happened when we implemented it
badly — a marker that detected the prompt rather than the answer, flagging 97% of probe responses —
is part of the contribution rather than an embarrassment to be edited out.

**Benchmark critique supplies the warrant, and one recent position paper supplies the conclusion.**
The construct-validity line runs from Borsboom's definition of validity as a property of the relation
between attribute and measurement outcome, through Jacobs and Wallach's import of measurement
modelling into computing, to the systematic finding of Bean and colleagues that validity problems
across 445 benchmarks are structural rather than incidental. Two recent works are closer still.
Hochlehnert and colleagues show that decoding parameters, seed and prompt format move reasoning
results enough to reverse conclusions. Jiang and colleagues argue that the root cause of evaluation
failure is a misplaced focus on aggregate scores and that item-level data release should be default
infrastructure. The second of these reaches, from a different starting point, the conclusion this
paper reaches in §8.4: publish the components, treat the composite as a reporting convenience. A
standard that constrains the conditions of observation and refuses to constrain the aggregation
formula is the operational form of that argument.

**The IR genealogy is the one that licenses the design.** Voorhees established that relative system
ordering survives judge variability provided the protocol is fixed, which is the strongest available
answer to the objection that non-deterministic answers cannot be measured. UQV100 provides precedent
for a test collection built explicitly on query variability. ir_metadata and the PRIMAD model provide
the reporting schema; repro_eval shows what it looks like when the IR community turns a
reproducibility claim into runnable software. Against that background, the reproduction study of
Mosnar and colleagues on TikTok audits is the cautionary case: published audits of commercial systems
did not reproduce, and the failure was traced to conditions the original studies had not pinned.
BRGEO-1's self-declared conformance is subject to the same failure mode, and the specification says
so; what it has in its favour is that the conditions it pins are the ones that failed.

**Position within the answer is a measurement-bearing quantity, and the evidence is now mixed enough
to matter.** The input-side literature — lost in the middle, serial position effects, and the
model-specific and language-specific effects Menschikov and colleagues report — establishes that
position within a prompt is not neutral. The output side has caught up. LLMs used as zero-shot
rankers are sensitive to candidate order; position bias undermines preference consistency in listwise
reranking; and in a randomised study of agent shopping sessions, position predicts inspection weakly
and non-monotonically, with the effect on final choice varying by model in a way that tracks neither
provider nor capability. That last result has the same shape as the finding in §5.4: susceptibility
is a property of the model, not of a class it belongs to. The novel claim in this paper is therefore
narrower and more defensible than "output position matters". It is that the instrument's truncation
of the output silently converts a whole-response measurement into a head-of-response measurement, at
a cut point that varies between providers because it is set by adapter code rather than by design,
and that the magnitude of the resulting incomparability was 23.8 percentage points on one engine.

---

## D. Gaps and risks a Q1 reviewer will raise

**1. The preprint-heavy evidence base in the closest related work.** A substantial share of the
2026 AI-visibility literature the paper depends on — references [4]–[9] in v1.0 and N1–N6 here — are
single-author arXiv preprints without institutional affiliation or peer review, several by the same
two authors. Every identifier resolves and every title is real; that is not the risk. The risk is a
reviewer observing that the paper's claim to novelty rests on a survey of grey literature. Mitigation:
state the maturity of the field explicitly in §2.1, separate peer-reviewed work (Aggarwal, Wen et al.
at ICML, Xu et al., Mosnar et al.) from preprints in the prose, and avoid resting any load-bearing
numerical claim on a preprint.

**2. No inter-implementation evidence, and now a published precedent for why that matters.** §10
already concedes that comparability is a design argument rather than a measured result. The Mosnar
reproduction study makes the concession sharper: audits of commercial systems have been shown not to
reproduce. A reviewer may reasonably ask why BRGEO-1 should be published before the reproducibility
exercise it names as its principal gap. The strongest available answer is the analysis-plan argument
in §12 — the specification is published ahead of confirmatory results precisely so that the window is
on record as a declared parameter — and that answer should be made in §1, not only in §12.

**3. Temperature 0.0 is presented as pinning the configuration, and it does not.** P5 sets temperature
0.0 and the reference instantiation presents it as a fixed condition. Atıl et al. and Coqueret et al.
establish that hosted LLM outputs remain non-deterministic at temperature zero through silent updates,
numerical rounding and expert routing. Unaddressed, this is a direct hit on P5. Addressed — by citing
both, conceding that P5 pins the request and not the response, and pointing out that this is an
additional argument for retaining full responses rather than regenerating them — it strengthens §5.5.

**4. The refusal taxonomy has no relation to the abstention literature's categories.** §6.2 proposes
ontological refusal, epistemic refusal and fabrication without reference to the taxonomies in the
abstention survey. A reviewer who works in that area will ask whether the three-way split is novel,
a relabelling, or a coarsening. The question must be answered in the text, with the mapping stated,
before the unvalidated-classifier limitation is acknowledged.

**5. The economic premise of §1 is asserted.** "Firms named in that answer inherit attention formerly
spread across a results page" carries the entire motivation and has no citation. The
difference-in-differences estimate of Khosravi and Yoganarasimhan and the log-based natural experiment
of Watanabe and Nakayashiki are the two cleanest available pieces of evidence; without one of them the
introduction is an industry claim in an academic register.

**6. Sample and power are not discussed, and a framework now exists for it.** The paper reports
66,399 canonical observations and 50 days without arguing that either is sufficient for the
conclusions drawn, and the H-series in §9 states minimum meaningful effects without a power
calculation. Sielinski's convergence criteria and the D-study tiers in Żatuchin's protocol are
directly applicable. Adding a short subsection on sufficiency would close an obvious gap.

**7. Elicitation mode remains the largest unmeasured parameter, and §11 says so.** Declaring a
seventh parameter of unknown magnitude as the highest-priority open item is honest, and a reviewer may
still treat it as disqualifying for a paper whose thesis is that unfixed parameters destroy
comparability. Even a small pilot — the same battery under structured-list elicitation on two engines
for one week — would convert the admission from an open question into a bounded one. Consider running
it before submission.

**8. The window finding is descriptive, and its generality is asserted from one arm.** The 23.8
percentage point movement is measured on one engine, and the mechanism section concedes that the
parametric denominators are censored at 200 characters so the relative-position reversal cannot be
established. §5.4 handles this well. What is missing is any external evidence that asymmetric windows
occur outside this pipeline. The claim in §12 that "defects of this shape are likely common" is
reasoning, not evidence. If a survey of two or three published visibility studies could establish
whether they report an extraction window at all, that would be a small, cheap, and genuinely novel
empirical addition — and it is the kind of thing a reviewer is likely to request anyway.

**9. Conformance levels borrow ISO vocabulary with no citation into the standards literature.** §3.3
invokes ISO/IEC 17000 and §10 invokes ISO 5725 without citing either, and without any reference to the
metrology-for-AI literature. Cite the standards directly and add at least one work connecting
benchmarking, standardisation and certification, so the level scheme reads as informed by that
tradition rather than as an analogy to it.

**10. Journal fit.** IP&M will want the IR genealogy foregrounded. The paper has it — Voorhees,
UQV100, TREC, ir_metadata, BEIR — but the Related work section leads with GEO, which is a young and
largely non-peer-reviewed area. Consider reordering §2 so the measurement-and-reproducibility
tradition in IR comes first and the GEO market is positioned as the applied setting where that
tradition has not yet been applied. The Alaofi et al. chapter on generative IR evaluation is the
natural hinge between the two.
