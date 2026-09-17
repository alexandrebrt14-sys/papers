# R5 — The citation rate as a measurand: metrological framing for BRGEO-1

Prepared 2026-09-11 for the journal-length manuscript. Every definition below was read in the primary document, not in a secondary summary: JCGM 200:2012 (VIM, third edition) and JCGM 100:2008 (GUM), both downloaded from bipm.org on 2026-09-11 and quoted from the PDF text.

This document supplies a vocabulary the manuscript currently lacks. The paper argues that a citation rate reported without its conditions is not comparable with another. Metrology has named that problem for decades, has a term for the floor it sets, and has an established procedure for the exercise the paper promises but has not run. Borrowing the vocabulary costs nothing and gains three things: it makes the central claim precise, it supplies an uncertainty budget as a reporting format, and it tells an adopter which of the six parameters carries which kind of error.

---

## 1. The measurand

VIM 2.3 defines a measurand as a "quantity intended to be measured", and Note 1 sets the requirement that makes the definition operational:

> **2.3 measurand** — quantity intended to be measured
> NOTE 1 The specification of a measurand requires knowledge of the kind of quantity, description of the state of the phenomenon, body, or substance carrying the quantity, including any relevant component, and the chemical entities involved.

The quantity the commercial market reports is the citation rate: the share of prompts in which a model names a given firm. Stated that way it is not yet a measurand, because the specification is missing the state of the phenomenon that carries the quantity. Which prompts. Asked of which model version. Under which generation configuration. Read to which length. With which rule for deciding that a string names the firm.

The six parameters of BRGEO-1 are exactly that missing specification. P1 to P6 are not an implementation checklist; they are what VIM Note 1 requires before the quantity can be said to exist as a measurand at all.

## 2. Definitional uncertainty, and why it is the floor

VIM 2.27 names the component of uncertainty that comes from an incomplete specification:

> **2.27 definitional uncertainty** — component of measurement uncertainty resulting from the finite amount of detail in the definition of a measurand
> NOTE 1 Definitional uncertainty is the practical minimum measurement uncertainty achievable in any measurement of a given measurand.
> NOTE 2 Any change in the descriptive detail leads to another definitional uncertainty.

Note 2 is the sentence this paper is an instance of. Changing the observation window changes the descriptive detail of the measurand, and therefore produces a different measurand with a different uncertainty. The 23.8 percentage point movement reported in the manuscript is not measurement error in the ordinary sense, and calling it error concedes too much: no amount of care, no larger sample and no better extractor would reduce it, because the two figures answer two different questions. One measures head-of-response citation, the other whole-response citation.

Note 1 supplies the argument against the market's current reporting practice in one line. Definitional uncertainty is the practical minimum, so a vendor who reports a confidence interval from sample size alone is reporting a quantity smaller than the floor. The interval is arithmetically correct and substantively misleading, because the dominant term was never in the budget.

## 3. Repeatability and reproducibility conditions

VIM separates two sets of conditions, and the separation maps onto this study cleanly.

> **2.20 repeatability condition of measurement** — condition of measurement, out of a set of conditions that includes the same measurement procedure, same operators, same measuring system, same operating conditions and same location, and replicate measurements on the same or similar objects over a short period of time

> **2.24 reproducibility condition of measurement** — condition of measurement, out of a set of conditions that includes different locations, operators, measuring systems, and replicate measurements on the same or similar objects
> NOTE 1 The different measuring systems may use different measurement procedures.

Under repeatability conditions, the same battery is sent to the same pinned model version, at the same temperature, through the same client, twice on the same day. What varies is the model's own sampling behaviour and whatever the provider changes without announcing it. The study's twice-daily cadence with an eight-hour cache time-to-live, shorter than the twelve-hour interval, is a repeatability design: it was built so that no observation in the series is served from cache, which is what makes the replicate a replicate.

Under reproducibility conditions, a second party implements the same specification with its own code, its own client library and its own entity matcher, and measures the same stored responses. That exercise is what BRGEO-1 promises and has not yet run, and §10 of the manuscript already states it as the specification's principal gap. ISO 5725-2 gives the standard design for it: an interlaboratory study in which the same items are measured by several laboratories, and the discrepancy is decomposed into a repeatability component and a between-laboratory component. Naming the missing work as an ISO 5725-2 interlaboratory exercise is more useful than calling it future work, because the design is already written and a reader can hold the project to it.

The vocabulary also sharpens what the paper's own window defect was. Five arms and one arm were not measured under reproducibility conditions by design; they were measured under conditions that differed in a parameter nobody had declared, which is neither repeatability nor reproducibility. It is the unlabelled third case, and it is the one the market lives in.

## 4. An uncertainty budget with two kinds of component

The GUM classifies the evaluation of uncertainty components into two types, and is explicit that the classification concerns the method of evaluation and not the nature of the component:

> **3.3.4** The purpose of the Type A and Type B classification is to indicate the two different ways of evaluating uncertainty components and is for convenience of discussion only; the classification is not meant to indicate that there is any difference in the nature of the components resulting from the two types of evaluation.

Type A is evaluated from a series of repeated observations (GUM 3.3.5, 4.2); Type B is evaluated by any other means, from prior knowledge, specifications or judgement (GUM 4.3).

This gives the paper a reporting format that does not exist in the GEO literature: a citation-rate figure published with a budget separating what was estimated from repetition from what was estimated from knowledge of the instrument.

| Component | Type | Source of the estimate | Status in this study |
|---|---|---|---|
| Query sampling | A | variance across the 192-query battery | estimable from the series |
| Day-to-day variation | A | variance across collected days | estimable; the temporal analysis reports it |
| Run-to-run variation of the model | A | two runs per day at temperature 0 | estimable; small at temperature 0, not zero |
| Observation window (P1) | B | re-extraction under two declared windows | measured: 23.8 pp on one arm; the window curve extends this to every arm |
| Entity matching rule (P6) | B | ablation of alias table and exclusion contexts | measurable with the same data; not previously quantified |
| Model version drift (P4) | B | series events with dated boundaries | bounded by stratification, not by an estimate |
| Generation configuration (P5) | B | one documented series event caused by reasoning effort alone | bounded, not estimated |
| Provider routing and unequal sampling | B | one arm receives roughly half the battery | reported, not corrected |
| Elicitation mode | B | plain prompt against structured request | **not estimated**; the manuscript names it as the highest-priority open item |
| Cohort and battery composition | B | design choice fixed before collection | fixed by declaration, which is what a Closed division means |

Two readings follow. First, the components the market reports are the Type A ones, and they are the small ones. Second, the protocol's function is to convert Type B components into declared constants: a parameter that is fixed and published stops contributing uncertainty to comparisons between figures that declare the same value, which is the precise sense in which BRGEO-1 "produces comparability".

The table also exposes the study's own weakest point without being asked. Two Type B components are bounded rather than estimated, and one is not estimated at all.

## 5. Traceability, and the limit of the analogy

VIM 2.41 defines metrological traceability as the property of a result that can be related to a reference "through a documented unbroken chain of calibrations, each contributing to the measurement uncertainty".

A citation rate has no SI unit and no calibration hierarchy, and there is no national institute holding a reference copy of the quantity. The chain that BRGEO-1 can offer is documentary rather than metrological in the strict sense: a published figure resolves to a version of the specification, which resolves to the six declared parameter values, which resolve to published artefacts (cohort, battery, matching rule, pinned versions, generation configuration) and to stored responses that a third party can re-extract. The conformance test suite named in §10 of the manuscript is the closest available analogue to a calibration standard: a fixed set of reference responses with expected figures under declared parameters, against which any implementation can be checked.

Overclaiming here would be easy and would be caught. The honest formulation is that the study borrows the metrological framework for its vocabulary and its reporting discipline, not for its epistemic guarantees, and that the measurand is constituted by convention rather than discovered. That is the position Jacobs and Wallach [21] describe for unobservable constructs in social measurement, and it is compatible with the framing above: the convention has to be written down before anyone can argue about whether it is the right one.

## 6. What to change in the manuscript

1. **Introduction.** One paragraph naming the citation rate as an incompletely specified measurand, with VIM 2.3 Note 1 as the requirement the field skips.
2. **Specification (§3).** Open with definitional uncertainty (VIM 2.27, Notes 1 and 2) as the reason the six parameters are normative rather than advisory. The sentence "any change in the descriptive detail leads to another definitional uncertainty" is the strongest one-line defence of P1 available.
3. **The window section.** State explicitly that the 23.8 points are definitional, not error, and that this is why no sample size removes them.
4. **New subsection in the specification or in the discussion.** The uncertainty budget of §4 above, published as a table, as the reporting format BRGEO-1 recommends alongside a figure.
5. **Governance (§10).** Rename the promised inter-implementation exercise as an interlaboratory study in the sense of ISO 5725-2, and state the design: same stored responses, independent implementations, discrepancy decomposed into repeatability and between-implementation components.
6. **Threats to validity.** Keep the honest limit of the analogy: no unit, no calibration hierarchy, measurand constituted by convention.

## 7. References to add

| Entry | Use |
|---|---|
| JCGM 200:2012, *International Vocabulary of Metrology — Basic and general concepts and associated terms (VIM)*, 3rd ed., BIPM, 2012. | measurand (2.3), definitional uncertainty (2.27), repeatability and reproducibility conditions (2.20, 2.24), metrological traceability (2.41) |
| JCGM 100:2008, *Evaluation of measurement data — Guide to the expression of uncertainty in measurement (GUM)*, BIPM, 2008. | Type A and Type B evaluation (3.3.4, 3.3.5, 4.2, 4.3) |
| ISO 5725-1:1994 and ISO 5725-2:1994, *Accuracy (trueness and precision) of measurement methods and results*. | interlaboratory design for the reproducibility exercise |
| ISO/IEC 17000:2020, *Conformity assessment — Vocabulary and general principles*. | already cited for the attestation axis of the conformance levels |

Verification note: clause numbers for VIM and GUM were confirmed by extracting the text of the official PDFs on 2026-09-11. ISO 5725 and ISO/IEC 17000 are paywalled; their clause numbers are **NOT VERIFIED** here and must be cited at document level unless someone opens the standard.
