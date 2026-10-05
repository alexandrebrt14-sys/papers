The International Vocabulary of Metrology (VIM, JCGM 200:2012) and the GUM (JCGM 100:2008) define **measurand**, **repeatability/reproducibility conditions**, **measurement uncertainty / Type A–Type B evaluation**, and **metrological traceability** in a way that has been deliberately adopted in a number of non‑physical measurement domains (software benchmarking, information retrieval, social measurement). Below I first give the formal definitions with clause numbers and exact wording, then discuss applications outside traditional metrology, with concrete examples and DOIs.

---

## (1) Measurand and definitional uncertainty (VIM)

### VIM definition of “measurand”

In VIM 3 (JCGM 200:2012), the measurand is defined in clause **2.3** roughly as:

> **Measurand**  
> quantity intended to be measured

Note 1 to entry clarifies that the definition in VIM 2 had been:

> “quantity subject to measurement”[24].

The VIM introduction explicitly discusses measurand and definitional uncertainty:

> “Clause 1 of this vocabulary is devoted to the concept of quantity and to the definition of a measurand. The definition of a measurand involves specifying the kind of quantity subject to measurement and the state of the phenomenon, body or substance carrying that quantity.”[16][24]

### Definitional uncertainty

The same introduction to VIM explains **definitional uncertainty** as the part of uncertainty that arises because the measurand cannot be specified perfectly:

> “Because it is not possible to specify a measurand completely, there is inevitably a component of measurement uncertainty associated with this incomplete definition, called definitional uncertainty. The definitional uncertainty, therefore, sets a minimum limit to any measurement uncertainty.”[16]

So formally:

- **Definitional uncertainty** is the component of measurement uncertainty due solely to the imperfect specification of the measurand.
- It exists even in a hypothetical, ideal measurement system.
- It is a *lower bound* on the achievable measurement uncertainty for that measurand.

In physical metrology this appears, for example, when measuring “the average body temperature of an adult human at rest”: the state of the subject (rest, ambient temperature, physiological conditions) can never be fully specified, so there is irreducible definitional uncertainty.

---

## (2) Repeatability conditions and reproducibility conditions (VIM and ISO 5725‑1/2)

### VIM (JCGM 200:2012)

In VIM 3, the key concepts are:

- **Repeatability of measurement**: clause **2.20** (precision under repeatability conditions).
- **Repeatability conditions of measurement**: clause **2.21**.
- **Reproducibility of measurement**: clause **2.24**.
- **Reproducibility conditions of measurement**: clause **2.25**.

The wording is aligned with ISO 3534/ISO 5725. Paraphrasing the VIM 3 text as it is normally presented:

> **Repeatability conditions of measurement** (2.21):  
> conditions of measurement in a set of conditions that includes the same measurement procedure, the same observer, the same measuring system, the same operating conditions and location, and repetition over a short period of time

> **Reproducibility conditions of measurement** (2.25):  
> conditions of measurement in a set of conditions that includes different locations, different observers, different measuring systems, and replication of measurements on the same or similar objects

These clauses make clear:

- “Conditions of measurement” refers to everything that can influence the measurement: procedure, operator, equipment, environment, time.
- Repeatability conditions are **the narrowest, most controlled subset** of those conditions.
- Reproducibility conditions are **the widest, most varied subset** of those conditions.

### ISO 5725‑1 (1994 and 2023 revisions) / ISO 3534‑1

ISO 5725‑1 and ISO 3534‑1 give very explicit definitions, which are quoted in many secondary sources[20][21][22]:

> **Repeatability conditions**  
> “[ISO 3534‑1] 3.14 repeatability conditions: Conditions where independent test results are obtained with the same method on identical test items in the same laboratory by the same operator using the same equipment within short intervals of time.”[20][25]

The current ISO 5725‑1:2023 wording (clause 3.x) similarly states:

> **repeatability conditions**  
> “observation conditions where independent test results (3.1) are obtained with the same method on identical test or measurement items in the same test or measuring facility by the same operator using the same equipment within short intervals of time.  
> Note 1 to entry: Repeatability conditions include:  
> a) the same measurement procedure or test procedure;  
> b) the same operator;  
> c) the same measuring or test equipment used under the same conditions;  
> d) the same location;  
> e) repetition over a short period of time.”[19][22][27]

> **Reproducibility conditions**  
> “[ISO 3534‑1] 3.18 reproducibility conditions: Conditions where test results are obtained with the same method on identical test items in different laboratories with different operators using different equipment.”[20][25]

And ISO 5725‑1:2023/FDIS confirms:

> **reproducibility conditions**  
> “observation conditions where independent test results are obtained with the same method on identical test or measurement items in different test or measurement facilities with different operators using different equipment”[22].

ISO 5725‑1 emphasizes that:

> “Under repeatability conditions, all factors that influence the measurement are considered constant and do not contribute to the variability, while under reproducibility conditions some or all influential factors vary and do contribute to the variability of the test results. Thus repeatability and reproducibility are the two extremes of precision, the first describing the minimum and the second the maximum variability in results.”[21][22][27]

So:

- **Repeatability conditions**: same method, same item, same lab/facility, same operator, same equipment, short time.
- **Reproducibility conditions**: same method, same item, *different* labs/facilities, operators, equipment; other influential factors allowed to vary.

---

## (3) Measurement uncertainty and GUM Type A / Type B evaluation

### Measurement uncertainty (VIM)

VIM 3 defines **measurement uncertainty** in clause **2.26**. The wording, as reflected in related documents[14], is:

> **Measurement uncertainty**  
> non‑negative parameter characterizing the dispersion of the quantity values being attributed to a measurand, based on the information used

Notes to entry (in VIM/GUM context) clarify that:

- It is often expressed as a **standard deviation**, **variance**, or a **coverage interval**.
- It encompasses all recognized sources of variability (random and systematic components), given the information available[17][28].

### GUM (JCGM 100:2008): Type A and Type B evaluation

GUM differentiates **evaluation methods** for uncertainty:

> **Type A evaluation (of uncertainty)**  
> “method of evaluation of uncertainty by the statistical analysis of series of observations”[17].

> **Type B evaluation (of uncertainty)**  
> “method of evaluation of uncertainty by means other than the statistical analysis of series of observations” (e.g., using prior information such as calibration certificates, specifications, handbooks, or expert judgment)[17][28].

The essential points, as summarized in current guidance[28]:

- **Type A**:
  - Uses *repeated observations* on the measurand.
  - Uncertainty is quantified by statistical quantities (experimental standard deviation, standard error of the mean, etc.).
- **Type B**:
  - Uses *all other information*: calibration certificates, datasheets, manufacturer tolerances, previous measurements, theoretical models, judgment.
  - Converts that information into a **standard uncertainty** assuming an appropriate probability distribution (normal, rectangular, triangular, etc.).

Critically, as many guides emphasize:

> “The labels Type A and Type B describe **how the contribution was evaluated**, not whether it is random or systematic.”[28]

GUM then combines Type A and Type B standard uncertainties (under independence assumptions) to obtain the **combined standard uncertainty**, and applies a coverage factor to obtain an **expanded uncertainty**.

---

## (4) Metrological traceability (VIM)

### VIM definition

VIM 3 (JCGM 200:2012) defines **metrological traceability** in clause **2.41**. The authoritative wording is widely quoted, for example by NIST[26][29][30]:

> **Metrological traceability** (VIM 3, 2.41):  
> “property of a measurement result whereby the result can be related to a reference through a documented unbroken chain of calibrations, each contributing to the measurement uncertainty”[18][26][29][30].

Important clarifications:

- The property attaches to the **measurement result**, not to a laboratory or instrument[26].
- The “reference” is typically:
  - A *measurement standard* (often an SI unit realization), or
  - A *reference material* or *reference method*.
- Each step in the calibration chain must:
  - Be documented,
  - Have known measurement uncertainty, and
  - Be part of an unbroken chain.

VIM’s related concept “metrological traceability chain” is described in clause **2.43**:

> “A metrological traceability chain is used to establish metrological traceability of a measurement result.”[24]

---

## Applications of these concepts outside physical measurement

Metrological ideas have been explicitly imported into fields such as **software benchmarking**, **information retrieval (IR) evaluation**, and **social / computational measurement**. The adaptation is not always by name (“VIM”, “GUM”), but the structure—measurand definition, repeatability/reproducibility, uncertainty, traceability—is recognizable and increasingly explicit.

### (A) Software benchmarking and performance evaluation

#### Measurand, repeatability, reproducibility, uncertainty

Several recent software engineering papers treat benchmark results as **measurements** with uncertainty:

- Kalibera & Jones (2012, 2013) popularized rigorous experimental design for performance benchmarking, emphasizing repeated runs, randomization, and explicit treatment of variability to reduce “measurement bias and benchmark variability”[1].
- Dorn, Apel & Siegmund, *Mastering uncertainty in performance estimations of configurable software systems* (Empirical Software Engineering 28, 33 (2023), DOI: **10.1007/s10664‑022‑10250‑2**) explicitly identify **measurement error** and **representation error** as sources of uncertainty in performance predictions, and provide **confidence intervals** for performance estimates[9]. This parallels GUM’s treatment of uncertainty: performance is a measurand, and uncertainty is expressed via probabilistic intervals.
- Lukasczyk et al., *Quantifying Performance Changes with Effect Size Confidence* (arXiv:2007.10899)[10] argue that any paper reporting execution time without treating **uncertainty of the metric** is “methodologically flawed” and advocate confidence intervals around ratios of mean execution times as the uncertainty measure of the benchmark metric, closely echoing GUM’s approach to uncertainty[10].

The idea of **unstable benchmarks** is explicitly defined as high variability among repeated measurements:

> “Unstable benchmarks show high variability among repeated measurements, which causes uncertainty about the actual performance…”[1][8].

Moussa‑Haider et al., *Predicting Unstable Software Benchmarks Using Static Source Code Features* (Empirical Software Engineering, DOI: **10.1007/s10664‑021‑09996‑y**)[1][8], treat repeated runs of benchmarks under controlled conditions as an analogue of **repeatability conditions**: same code, same hardware, same environment, short time intervals—exactly mirroring ISO 5725 repeatability conditions.

#### Benchmarking reference pairs and traceability in computational tools

In computational metrology, NPL’s report *Benchmarking Reference Pairs for Measurement Uncertainty Evaluation* describes “benchmarking reference pairs … to test a candidate software implementation” of Measurement Uncertainty Evaluation[7]. The procedure:

- Specifies reference data and reference results \(\{y_k, u(y_k), I_k\}\).
- Requires that test software reproduce these results within specified tolerances proportional to the reference uncertainty[7].

This mimics **metrological traceability** for software: the software’s output is related to reference values via documented test procedures and uncertainty limits, thereby establishing traceability of computed results to reference models.

More broadly, “Benchmarking as Empirical Standard in Software Engineering” (arXiv:2105.00272, DOI: **10.1145/3463274.3463361**) discusses benchmark suites as **empirical standards** for evaluating techniques[5], a conceptual analogue of **measurement standards** in metrology.

### (B) Information retrieval (IR) evaluation



## Fontes
- https://www.ifi.uzh.ch/dam/jcr:ca478034-b709-4a7e-a7c8-b8d9f6d154f2/emse-instability-prediction.pdf
- https://dl.acm.org/doi/10.1145/3239572
- https://dl.acm.org/doi/abs/10.1145/3582524.3582540
- https://dl.acm.org/doi/10.1145/1277741.1277754
- https://arxiv.org/abs/2105.00272
- https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=03ce64a6d092ef3a9d634e99c40623e148a4d0b2
- https://eprintspublications.npl.co.uk/6642/1/MS17.pdf
- https://dl.acm.org/doi/abs/10.1007/s10664-021-09996-y
- https://link.springer.com/article/10.1007/s10664-022-10250-2
- https://arxiv.org/pdf/2007.10899
- https://www.sigir.org/wp-content/uploads/2022/07/p12.pdf
- https://arxiv.org/abs/2505.07459
- https://arxiv.org/abs/2510.11483
- https://amt.copernicus.org/articles/16/2067/2023/amt-16-2067-2023.pdf
- https://discovery.researcher.life/article/an-uncertainty-aware-query-selection-model-for-evaluation-of-ir-systems/cb1d4c5fb0063fe1890f55f1f348650d
- https://www.iso.org/sites/JCGM/VIM/JCGM_200e_FILES/MAIN_JCGM_200e/Intro_e.html
- https://ncc.nesdis.noaa.gov/documents/documentation/JCGM_100_2008_E.pdf
- https://www.bipm.org/documents/20126/2071204/JCGM_200_2012.pdf
- https://cdn.standards.iteh.ai/samples/69418/a7c3fb78cdce4a6398bd3f759670d72e/ISO-5725-1-2023.pdf
- https://standards.iteh.ai/catalog/standards/iso/fd911a40-20f6-4c0b-ac29-30ba48191e7d/iso-5725-1-1994
- https://webstore.ansi.org/preview-pages/ISO/preview_ISO+5725-1-1994.pdf
- https://cdn.standards.iteh.ai/samples/69418/7efb673806c343d3a5657d69dde621e5/ISO-FDIS-5725-1.pdf
- https://standards.iteh.ai/catalog/standards/sist/00c8e420-a808-4ab7-ad01-2b52581198b8/sist-iso-5725-1-2003
- https://www.iso.org/sites/JCGM/VIM/JCGM_200e_FILES/MAIN_JCGM_200e/02_e.html
- https://lists.w3.org/Archives/Public/www-qa-wg/2003Oct/0038.html
- https://www.nist.gov/metrology/metrological-traceability
- https://standards.iteh.ai/catalog/standards/iso/7bf20a65-f59b-48f6-8e45-306b7c5ac3db/iso-5725-1-2023
- https://www.spilma.com/en/guides/calibration-measurement-uncertainty-gum
- https://blqs.dmsc.moph.go.th/th/download/3876/km/2501
- https://metrologyatlas.org/dictionary/metrological-traceability