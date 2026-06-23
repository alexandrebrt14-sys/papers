# The Anchor-Entity Effect — Sections 7–8 and Consolidated References

> Closing sections of the manuscript. All quantities are taken from the verified
> reviewer analyses over `papers.db`; all citations are drawn only from entries
> confirmed in `literatura.md`, `peer_review_R2_teoria.md`, and the author's
> companion-work record. Data cover the complete collection record (April 23 - June 9, 2026) and every
> absolute rate is reported as an upper bound pending the dual-track recollection.

---

## 7. Discussion

The headline of this study is not that one Brazilian vertical out-cites the
others. It is that the question "which sector do LLMs prefer?" is, on inspection,
malformed. When we asked it of our data, the data answered with a single firm.
Fintech leads spontaneous citation at 28.15%, ahead of retail (24.94%),
technology (14.50%), and healthcare (13.35%); recode as uncited every fintech
response whose only named entity is Nubank, and the vertical falls to 11.46% —
dead last — while its adjusted odds ratio against healthcare inverts from 4.13 to
0.77. A "sectoral advantage" that does not survive the removal of one brand was
never an advantage of the sector. This is the first lesson for anyone measuring
brand visibility in LLMs: the unit that the field reports (the category) and the
unit that actually carries the signal (the anchor entity) are not the same, and
conflating them manufactures findings that evaporate under decomposition.

We propose the leave-one-out of the modal entity as a routine validity check, not
a robustness afterthought. The estimator is cheap — recode, re-tabulate, compare —
and it discriminates sharply: under per-cluster inference, the raw fintech-retail
gap is not significant (Welch t = 0.645 across 48 query-clusters per vertical, the
~24-point between-query variance swallowing the 3.2-point gap), whereas the
leave-one-out reversal is (t = -3.35, negative sign). The fragile claim dies
exactly where it should and the robust one survives. We therefore advance a
general prescription: any claim that an LLM favors sector X should be required to
survive removal of X's modal entity, lest the study be measuring a firm and
reporting a sector. The anchor lens generalizes beyond fintech — jackknifing each
vertical's top entity drops retail by 5.67 points, technology by 2.89, healthcare
by 2.55, and fintech by 16.70; remove retail's two co-leaders (Mercado Livre plus
Magazine Luiza) and retail falls 14.35 points. Every vertical is anchor-driven.
The difference between fintech and the rest is the *number* of anchors (one versus
two or more), not the presence of concentration. Fintech is simply the extreme
k = 1 case, and the construct is the top-k anchor core, not a Nubank curiosity.

Engine heterogeneity is the second first-class finding, and it is destructive of
the "systematic sectoral bias" framing. Only two of five engines place fintech
above retail. The aggregate gap decomposes into +574 cited responses from Claude
Haiku and +134 from Gemini — the latter contaminated by truncation — against
ChatGPT (-117), Perplexity (-91), and Groq (-93). The "sector effect" is, almost
entirely, one parametric model's idiosyncrasy plus an artifact, opposed by three
engines pointing the other way. A brand's GEO reality is therefore not a single
number; it is a vector over engines. Strong visibility in Claude does not transfer
to ChatGPT or Perplexity, and a study that averages across engines reports a
fiction that holds for none of them. We treat the vertical-by-engine interaction
as a primary result and recommend that visibility be measured engine by engine.

The third contribution is methodological, and it is the part most transferable to
other sectoral audits. Two measurement threats shaped — and partly fabricated —
our raw numbers. First, `response_text` was persisted truncated at exactly 200
characters in four of five collectors (only Perplexity intact), so the NER scored
*front-loading* in the opening of the answer rather than full citation. This does
not reward fintech for early mention — retail front-loads more (first-entity
offset 111 versus 123 characters) — it penalizes rivals whose anchors arrive late:
truncation erases 51.6% of technology citations and 30.7% of healthcare, against
~20% for fintech and retail, inflating the fintech-versus-technology gap while
leaving the fintech-versus-retail gap untouched. Worse for the thesis metric,
truncation inflates the within-fintech concentration itself: Nubank sits at offset
118 (inside the window) while Itaú (402), PicPay (515), Banco Inter (838), and BTG
(906) fall outside it, so the 49.68% concentration figure is itself partly a
truncation artifact and must be declared an upper bound. Second, fictitious decoy
brands were "found" 96.9–98.6% of the time; until we determine whether this
false-positive rate is by design (a decoy planted in the prompt, hence not
comparable to spontaneous citation) or a detector defect, the construct validity
of `cited` carries an asterisk. Decoy design and truncation auditing are not
housekeeping — they are the difference between measuring citation and measuring an
opening-sentence heuristic, and we report them as such.

Finally, honesty about what the current data cannot yet support. We cannot make
confirmatory rate claims: the inference is not yet clustered (the published
chi-squared values treat ~293 repetitions per query as independent, when the
effective n is ~240 clusters), and that work is pending. We cannot claim temporal
stability of the anchor: Nubank's share rises within the window, from ~41% (W16–
W18) to 53–59% (W19–W23), a ~30% relative increase that is a service-drift threat,
not a robustness result — the aggregate rate looks stable only because the tail
shrinks as the anchor grows. We cannot yet test the mechanism's signature
prediction, that citation share exceeds real market share (the convex,
super-linear mapping), because we have not crossed the 49.68% citation share with
Nubank's actual Brazilian market share. And the corpus-supply story — that
fintech's dense Portuguese-language press, comparison, and institutional corpus
feeds the anchor — remains an untested upstream hypothesis whose own predictions
(largest effect under RAG; larger gap in Portuguese) were in fact refuted by the
data. What survives, robustly, is the decomposition: the apparent sectoral
advantage is the shadow of a category's anchor core, modulated more by engine than
by sector.

## 7.X Implications for Generative Engine Optimization

If the vertical is an epiphenomenon and the anchor is the asset, the practical
counsel for brands inverts the prevailing intuition. Being in the "right" vertical
buys nothing; being the category's anchor buys a disproportionate share of the
model's attention. Nubank captures 49.68% of fintech mentions, and 59.31% of
fintech responses that cite anyone cite Nubank alone. The objective of GEO is not
to "appear" — it is to become the category entity, the default name a model emits
when the category is evoked. A brand that becomes the canonical answer to a class
of questions captures attention out of all proportion to its share of the market
that produced it.

Two entity-level levers follow directly. Entity disambiguation and lexical
uniqueness matter: "Nubank" is a rare, clean string with no competing senses,
unlike "Amazon," "Oracle," or "Google," which suffer NER false negatives and
positives and dilute into other meanings. A unique name maximizes both salience in
the corpus and extractability by the detector — a verbal distinctive brand asset
in the Ehrenberg-Bass sense, paired with mental availability: the anchor is the
brand evoked across the largest number of category entry points ("open an
account," "no-fee card," "bank on your phone"). Consensus density across sources is
the second lever. The vertical's tail is itself robust — PicPay, C6, and Inter sum
to roughly 2,065 mentions — so non-anchor brands still capture meaningful
attention by building presence in high-cadence Portuguese-language corpora:
specialized press, comparison and consumer sites, and institutional documentation
(Banco Central, Pix, Open Finance). A brand that recurs consistently across many
independent sources accrues the cumulative advantage that the parametric weights
later encode.

For the Brazilian market specifically, the opportunity is in the fragmented
categories. Technology B2B (HHI 0.110) has no consolidated anchor; it is precisely
where a brand can still become the category entity through directed corpus
investment. Already-anchored categories such as fintech are defense for the leader
and an uphill attack for everyone else. Sensitive categories play by different
rules: in healthcare, RLHF pushes toward generic, hedged answers (0% negative
mentions, heavy hedging), so GEO there competes not on brand salience but on being
the citable institutional source that survives the caution guardrail. Across all
categories, the engine matters more than the sector — visibility must be measured
engine by engine — and honest measurement is itself a competitive edge: a serious
GEO program reports within-category citation share per entity and per engine, with
and without the anchor, and separates RAG from parametric behavior, because the
"sectoral advantages" the industry sells are fragile to a single firm and to
measurement artifacts.

## 8. Conclusion

We set out to explain why Brazilian fintech brands appeared most cited by large
language models and found that the premise dissolved under decomposition. The
apparent sectoral advantage is not a property of the sector. Recoding away a
single anchor entity drops fintech from first place to last (28.15% to 11.46%) and
inverts its adjusted odds ratio (4.13 to 0.77); the same leave-one-out, applied to
every vertical, shows each is governed by its top-k anchor core, with fintech the
extreme single-anchor case. The contribution is the construct and the estimator
that go with it: the anchor entity (defined by a share threshold and a gap to the
runner-up), anchor concentration (the Herfindahl index together with the anchor's
share), and the anchor effect — the rate that a vertical loses when its anchor is
removed — read as the projection of cumulative advantage onto the parametric
attention of LLMs, and modulated more by engine than by sector.

We do not claim more than the current data support. The rates are upper bounds
until recollection removes the 200-character truncation and restores the full
48-query Perplexity arm; the inference awaits a clustered model at the ~240-cluster
level; the decoy false-positive rate awaits a definitive design-versus-bug
verdict; the convex over-representation prediction awaits a market-share contrast.
The roadmap to window close on 21 July 2026 runs a dual-track recollection (intact
text in parallel with the historical truncated series, to quantify exactly how
much the cut distorts each vertical), a logistic GLMM with random intercepts for
query, day, and engine and dual outcomes, per-vertical top-k leave-one-out with
confidence intervals over the drops, and the reproducibility package — SHA-256
manifests, a versioned public dataset, and the NER codebook. The finding we expect
to carry to the final window is the one already robust to clustering: sectoral
citation advantage in LLMs is, in large part, anchor-entity concentration.

---

## References

Aggarwal, P., Murahari, V., Rajpurohit, T., Kalyan, A., Narasimhan, K., &
Deshpande, A. (2024). GEO: Generative Engine Optimization. In *Proceedings of the
30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining (KDD)* (pp.
5–16). DOI: 10.1145/3637528.3671900. arXiv:2311.09735.

Autor, D., Dorn, D., Katz, L. F., Patterson, C., & Van Reenen, J. (2020). The Fall
of the Labor Share and the Rise of Superstar Firms. *Quarterly Journal of
Economics*, 135(2), 645–709. DOI: 10.1093/qje/qjaa004.

Caramaschi, A. (2026). *Algorithmic Authority: A Practitioner Framework for
Generative Engine Optimization Based on a 7-Day Implementation Sprint*. SSRN.
DOI: 10.2139/ssrn.6460680. Also archived as preprint on Zenodo, DOI:
10.5281/zenodo.19687866.

Caramaschi, A. (2026). *alexandrebrt14-sys/papers: v0.1.0* [Software]. Zenodo.
DOI: 10.5281/zenodo.19687958.

Chen, M., Wang, X., Chen, K., & Koudas, N. (2025). Generative Engine Optimization:
How to Dominate AI Search. arXiv:2509.08919.

CNBC (2021, December 9). Buffett-backed Nubank rises in trading on the NYSE in
blockbuster IPO. https://www.cnbc.com/2021/12/09/buffett-backed-nubank-rises-in-trading-on-the-nyse-in-blockbuster-ipo.html.

DiPrete, T. A., & Eirich, G. M. (2006). Cumulative Advantage as a Mechanism for
Inequality: A Review of Theoretical and Empirical Developments. *Annual Review of
Sociology*, 32, 271–297. DOI: 10.1146/annurev.soc.32.061604.123127.

Kamruzzaman, M., Nguyen, H. M., & Kim, G. L. (2024). "Global is Good, Local is
Bad?": Understanding Brand Bias in LLMs. In *Proceedings of EMNLP 2024*.
arXiv:2406.13997.

Lehmann, H. H., Lee, J. H., Schockaert, S., & Wermter, S. (2026). Knowing the
Facts but Choosing the Shortcut: Understanding How Large Language Models Compare
Entities. *EACL 2026*. arXiv:2510.16815.

Lichtenberg, J. M., Buchholz, A., & Schwöbel, P. (2024). Large Language Models as
Recommender Systems: A Study of Popularity Bias. In *Gen-IR Workshop at SIGIR*.
arXiv:2406.01285.

Merton, R. K. (1968). The Matthew Effect in Science. *Science*, 159(3810), 56–63.
DOI: 10.1126/science.159.3810.56.

Nu Holdings Ltd. (2026, March). Company disclosure: Nu surpasses 115 million
customers in Brazil. Nu International newsroom and SEC Form 6-K filings,
https://international.nubank.com.br/company/nubank-celebrates-two-years-of-ipo-with-significant-growth-and-expansion-into-new-markets/.

Romaniuk, J., & Sharp, B. (2022). *How Brands Grow: Part 2* (rev. ed.). Oxford
University Press.

Sharp, B. (2010). *How Brands Grow: What Marketers Don't Know*. Oxford University
Press.

Sun, et al. (2024). Quantifying Reliance on External Information over Parametric
Knowledge during Retrieval-Augmented Generation (RAG) Using Mechanistic Analysis.
arXiv:2410.00857.

Vishwakarma, R., Kumar, S., & Jamidar, R. (2026). What Gets Cited: Competitive GEO
in AI Answer Engines. arXiv:2605.25517.

Yang, K.-C. (2025). News Source Citing Patterns in AI Search Systems.
arXiv:2507.05301.

Ye, H., Mao, J., Guan, Z., & Tian, Z. (2026). EcoGEO: Trajectory-Aware Evidence
Ecosystems for Web-Enabled LLM Search Agents. arXiv:2605.12887.

Zhang, et al. (2025). Source Coverage and Citation Bias in LLM-based vs.
Traditional Search Engines. arXiv:2512.09483.

Zhong, et al. (2026). AutoGEO: What Generative Search Engines Like and How to
Optimize Web Content Cooperatively. *ICLR 2026*. arXiv:2510.11438.

(2025). The Matthew Effect of AI Programming Assistants. arXiv:2509.23261.

(2025). AI Answer Engine Citation Behavior: An Empirical Analysis of the GEO-16
Framework. arXiv:2509.10762.
