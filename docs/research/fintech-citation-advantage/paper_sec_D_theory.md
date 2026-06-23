# 5 The Anchor-Entity Effect: A Formal Account

The empirical regularity this paper sets out to explain is simple to state and easy to misread. Across the analytic core (n = 50,453), the fintech vertical attains spontaneous citation in 28.15% of responses, ahead of retail (24.94%), technology (14.50%), and healthcare (13.35%). Read at face value, this is a sectoral advantage. Our claim is that it is not. It is the projection of a single dominant firm onto the category average, and naming that projection precisely is what turns a description into a construct.

## 5.1 Three objects, not one

Prior treatments conflate three distinct objects. We separate them. Let *s(e, v)* denote the share of mentions captured by entity *e* within vertical *v*, that is *s(e, v) = mentions(e, v) / mentions(v)*.

The **anchor entity** of a vertical is the modal firm *e\* = argmax s(e, v)*, but only when it clears two pre-registered thresholds: a share floor, *s(e\*, v) ≥ τ*, and a separation from the runner-up, *s(e\*, v) − s(e₂, v) ≥ δ*. With τ = 0.40 and δ = 0.15, the definition is discrete and falsifiable rather than circular. Fintech qualifies: Nubank holds 49.68% of fintech mentions with a wide gap to second place. Retail does not: its leader Mercado Livre sits near 29.5%, below τ, with Magazine Luiza close behind. Retail is a two-leader category, not a single-anchor one — a distinction the thresholds make formal rather than rhetorical.

**Anchor concentration** is the pair (HHIᵥ, *s(e\*, v)*). Reporting the Herfindahl index alone is insufficient, because it cannot distinguish "concentrated around one" (fintech) from "concentrated around a few" (retail). The share of the modal entity is what carries that information.

The **anchor effect**, the quantity the thesis turns on, is the difference between the observed citation rate and the counterfactual rate under leave-one-out (LOO) removal of the anchor: *Δᵥ = rate(v) − rate_LOO(v)*. For fintech, Δ = 28.15 − 11.46 = 16.69 points. This is the clean operationalization of the "superstar component" of an apparent sectoral rate.

## 5.2 The convex cumulative-advantage mechanism

Concentration alone does not distinguish an anchor effect from ordinary popularity bias. The missing piece is a functional claim about *how* market presence becomes citation. We posit that the probability of spontaneous citation is a convex transform of an entity's relative frequency in the training corpus, which is in turn a convex (cumulative-advantage) transform of its real market share:

```
P(cite e | v) ≈ g( f(e) ),   f(e) ∝ m(e)^γ   with γ > 1
g convex and saturating (logistic in the parametric weights)
```

Because γ > 1, the mechanism predicts super-linear over-representation: a firm holding, say, 30% of a market should capture closer to half of its category's mentions. This is the Matthew effect — cumulative advantage in the sense of Merton (1968) and DiPrete & Eirich (2006) — ported to a new substrate, the parametric attention of LLMs. The anchor entity is thus not a novel phenomenon in isolation; it is what cumulative advantage looks like when it is projected onto model weights, with the upstream concentration supplied by winner-take-most dynamics in digital markets (Autor et al., 2020) and the canonical-brand reading supplied by mental availability theory (Sharp, 2010; Romaniuk & Sharp, 2022).

## 5.3 Five falsifiable predictions and their status

The construct yields five predictions, ordered by the strength of the test available in the present data.

**P1 (LOO inversion).** Removing the anchor inverts the sector's rank. *Confirmed.* Fintech falls 28.15% → 11.46%, from first to last, and its adjusted odds ratio versus healthcare inverts from 4.13 to 0.77. The reversal survives cluster-level inference (Welch t = −3.35 on per-cluster means, against t = 0.65 for the fragile raw gap) and holds across all eight observed weeks (LOO gap between −7.6 and −8.2 points throughout).

**P2 (convex over-representation).** *s(e\*, v)* exceeds the firm's true market share. *Testable, not yet run.* This is the decisive test of γ > 1 and requires crossing the 49.68% citation share against Nubank's actual Brazilian market share.

**P3 (engine gradient).** The anchor effect is larger in purely parametric engines, where γ acts on the weights, than under RAG, where live retrieval resamples the tail. *Supported.* Claude shows a 40-point parametric gap (51.0% fintech vs 10.4% technology); under Perplexity the gap compresses, with fintech-LOO at 67.9% — still below retail's 92.9%, but the retriever no longer lets the anchor stand alone.

**P4 (anchor specificity / negative control).** Verticals without an anchor (retail, which does not reach τ) do not invert under removal of any single leader. *Testable, with a leading signal:* the LOO of a single entity drops retail only −5.67 points versus fintech's −16.70; removing retail's two anchors together drops it −14.35, confirming that every vertical is anchor-driven and fintech is the extreme k = 1 case.

**P5 (mental availability).** *s(e\*, v)* correlates with survey-measured brand mental availability. *Future work* — the bridge to Ehrenberg-Bass that would most raise the paper from measurement to theory; no published study has crossed mental availability with LLM citation.

# 6 Why Fintech? Mechanisms Behind the Apparent Sectoral Advantage

The aggregate phenomenon is real: fintech does lead spontaneous citation, and the ordering of concentration (HHI 0.283 > retail 0.202 > healthcare 0.154 > technology 0.110) tracks the ordering of citation rate closely. The error is not in seeing the phenomenon but in attributing it to a diffuse property of the sector. The aggregate is produced by four chained mechanisms, not by a sectoral spirit. We set them out in causal order and close by stating what each explains and what it cannot.

## 6.1 Layer (i): the sector produced the country's strongest anchor entity

Brazilian fintech generated, in Nubank, the strongest anchor entity in the national market, through a conjunction no other vertical assembles at the same intensity.

*Category brand (maximal mental availability).* "Nubank" occupies the semantic slot of "Brazilian digital bank" almost one-to-one — it is the canonical answer evoked across the largest number of the category's entry points (opening an account, a no-fee card, a bank on the phone, a first card). In Ehrenberg-Bass terms it is the brand most likely to be retrieved across the most Category Entry Points.

*Lexically unique name (verbal distinctive brand asset).* "Nubank" is a rare, unambiguous string, unlike "Amazon," "Oracle," or "Google," which suffer NER false negatives and positives and dissolve into other senses. A unique name maximizes both corpus salience and extractability.

*Scale and external validation.* The anchor's offline scale is independently documented: Nubank listed on the NYSE in December 2021 in one of the year's largest fintech IPOs (CNBC, 2021), and by March 2026 reported surpassing 115 million customers in Brazil, making it the country's largest private financial institution by customer count (Nu Holdings, 2026). The within-category citation share we measure (49.7%) nonetheless far exceeds any plausible market-share figure, which is precisely the convexity the construct predicts.

*Narrative infrastructure (Pix / Open Finance).* Instant payment and open-banding rails gave the sector a dense national narrative in which the brand sits glued to the category, multiplying the category's entry points. Alongside it runs a high-cadence text stream that names the brand daily — specialized press, comparison and consumer content, aggressive native-digital SEO, and institutional documentation from the Central Bank. *Honest caveat:* we did not measure corpus volume. This corpus-supply layer is a candidate upstream hypothesis, not established causation, and its direct predictions failed — the effect was not maximal under RAG (retail 92.9% > fintech 86.5%) and the fintech–technology gap was larger in English, not Portuguese. We report these as refutations, not partial confirmations.

## 6.2 Layer (ii): entity → category transmission via cumulative advantage

This is the theoretical core. Popularity bias is an item-level phenomenon; what we measure is the *transmission* of that item-level bias into an apparent property of the category. The mechanism is cumulative advantage: because the market-share-to-citation-share map is convex (γ > 1), a single firm captures a disproportionate slice of the category's mentions, and the category average inherits the firm's dominance. The live evidence of transmission in progress is that the anchor's share *grows within the measurement window itself*: Nubank rises from about 41% (W16–W18) to roughly 53–59% (W19–W23), a relative increase near 30% over fifty days. The rich get richer inside the experiment. This is also why the vertical's headline rate looks stable while the thesis quantity does not: the tail (PicPay, C6, Inter) shrinks as the anchor grows, holding the aggregate fixed by compensation while concentration climbs. The apparent sectoral advantage is, literally, one superstar firm's shadow cast across the category mean.

## 6.3 Layer (iii): amplification by parametric engines

Transmission is not uniform across engines, which is precisely why "systematic sectoral bias" is false. In purely parametric models γ acts directly on the weights: Claude cites fintech at 51.0% against 10.4% for technology — a 40-point gap that is the strongest and least anecdotal evidence in the study, because it shows the advantage lives in the weights, not in live retrieval. Decomposing the aggregate fintech–retail gap by engine confirms the asymmetry: Claude contributes +574 cited responses and Gemini +134 (the latter contaminated by truncation), against ChatGPT −117, Perplexity −91, and Groq −93. The aggregate advantage is almost entirely one parametric engine plus one artifact, against three engines pointing the other way. Under RAG, Perplexity resamples the tail and compresses the gap. The engine matters more than the sector.

## 6.4 Layer (iv): the opening-window measurement artifact

Part of the headline number is a property of the instrument and the moment. The NER ran over the first ~200 characters in four of five engines, measuring front-loading rather than full citation. This cut does not reward fintech for being front-loaded — retail front-loads more (mean first-entity offset 111.1 vs 123.1 characters). It *penalizes the rivals*: truncation would erase 51.6% of technology citations and 30.7% of healthcare citations, whose entities appear late, against ~20% for fintech and retail. It therefore inflates the fintech–technology and fintech–healthcare gaps but not the fintech–retail gap. Within fintech, the cut also exaggerates Nubank's dominance (offset 118, inside the window) by erasing tail anchors that surface late (Itaú 402, PicPay 515, Inter 838, BTG 906 characters). Compounded with the fact that the snapshot captures the opening of the phenomenon, when cumulative advantage is still accelerating, this means 28.15% and 49.68% are upper bounds pending untruncated recollection.

## 6.5 Discriminating-evidence table

| Observed pattern | (i) Anchor entity | (ii) Cumulative advantage | (iii) Parametric amplification | (iv) Window artifact |
|---|---|---|---|---|
| Fintech rate leads aggregate | partial | **explains** | partial | inflates vs tech/health only |
| LOO inversion 28.15 → 11.46% | **explains** | **explains** | — | does not explain |
| HHI/top-3 highest in fintech | **explains** | partial | — | inflates Nubank's share |
| Anchor share grows 41% → 57% in-window | — | **explains** | — | fails to explain |
| Claude 40-pt parametric gap | reinforces | reinforces | **explains** | does not explain |
| Only 2/5 engines rank fintech top | fails to explain | fails to explain | **explains** | partial |
| Gap larger in English than PT | reinforces (global entity) | — | — | fails to explain |
| Tech/health citations appear late | — | — | — | **explains** |
| Retail front-loads more than fintech | — | — | — | **explains** (refutes the draft's claim) |

No single layer explains every pattern. Layer (i) is necessary but cannot explain the engine variance or the in-window growth. Layer (ii) explains the rate and the growth but not the engine heterogeneity. Layer (iii) explains the heterogeneity but not the concentration ordering. Layer (iv) explains the late-citation asymmetry and the inflated gaps but is silent on the parametric signal. The parsimonious account is the chain, not a winner.

## 6.6 Correlational versus identified

We state the epistemic status plainly, because the contribution depends on it.

**Identified (within the data, robust to clustering).** The anchor effect itself: that removing the modal entity inverts the fintech rank (P1), that the inversion survives cluster-robust inference and is stable across all eight weeks, and that the per-vertical jackknife shows every sector is anchor-driven with fintech the extreme k = 1 case. The engine heterogeneity (Layer iii) is also identified — it is a direct observation of the vertical × engine interaction, not an inference about the world. The directional correction of the front-loading narrative (Layer iv) is measured on the untruncated Perplexity cohort.

**Correlational or unmeasured.** The corpus-supply story (Layer i, the press/SEO/Reclame Aqui/Central Bank chain) is an untested upstream hypothesis: no measure of corpus size, news volume, or search volume was crossed with citation rate, and its own direct predictions were refuted. The convex over-representation claim (P2) is not yet tested against real market share, so γ > 1 remains posited rather than demonstrated. The mental-availability bridge (P5) is future work. The anchor's offline scale (NYSE listing in December 2021; 115M+ customers in Brazil reported in March 2026) is documented in public filings and company disclosures, but the mapping from offline scale to citation share remains correlational. In short: the *decomposition* and the *engine heterogeneity* are identified results; the *upstream causal chain* that would explain why fintech produced the anchor in the first place remains a disciplined hypothesis, not a finding.
```