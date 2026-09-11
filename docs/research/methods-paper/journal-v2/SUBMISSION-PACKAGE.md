# Submission package — BRGEO-1 v2.0

Everything a submission form asks for, written out and ready to paste. Two destinations, one manuscript, different fields.

---

## 1. Eliva Press author portal

The editor's instructions of 2026-09-09 (minimum 35 pages, Times New Roman 16, line spacing 1.5, table of contents with matching pagination) are met by the PDF in this package. The portal asks for the fields below, in this order.

### Book title (max 100 characters)

```
Measuring Entity Citation in Generative Engines
```
46 characters.

### Subtitle (max 100 characters)

```
The BRGEO-1 Protocol and a Five-Month Field Record
```
49 characters.

### Spine (max 70 characters; required above 110 pages)

```
Measuring Entity Citation in Generative Engines
```

### Main author name

```
Alexandre Caramaschi
```
Capitalised case, not upper case, as the portal guide requires. No co-authors.

### Blurb (minimum 600 characters)

```
Large language models now stand between customers and the companies they might choose, and an industry has formed around measuring which companies get named. The figures that industry reports are not comparable with one another, because the conditions under which a citation is counted are almost never stated.

This book specifies BRGEO-1, an open protocol that declares six of those conditions, and reports what happened when one of them was measured instead of assumed. Reading a model's whole answer rather than its first 200 characters raised the citation rate by 23 to 56 percentage points across five engines, on the same observations, with no answer losing a citation. One engine that appeared to name almost no companies turned out to name them past the point where the instrument had stopped reading.

Alongside the specification, the book gives the field record behind it: five months of daily collection against six commercial engines, 86,543 observations, a 59-day interruption declared rather than hidden, and a series of defects that passed every automated check the pipeline ran on itself. It is written for anyone who buys, sells, or publishes a number about visibility in generative search, and for researchers who need a measurement standard before the comparisons start.
```
1,318 characters.

### Author biography (max 500 characters)

```
Alexandre Caramaschi is Chief Strategy Officer of Nuvini (Nasdaq: NVNI), Founder of Brasil GEO and co-founder of NAIA and of AI Brasil. He was CMO of Semantix (Nasdaq). He researches how generative engines cite companies, maintaining an open longitudinal study of Brazilian firms across four sectors, and is the author of the BRGEO-1 measurement specification. ORCID 0009-0004-9150-485X.
```
386 characters. This book is written in his capacity at Brasil GEO and does not represent a position of Nuvini; the same statement appears in the competing-interest declaration inside the book.

### Author photo

Portrait format, under 1 MB, jpg or png. Use one of the 2026 official press photographs.

### Keywords

```
generative engine optimization, AI search visibility, measurement standard, entity citation, large language models, brand monitoring, research methodology, Brazil
```

### Category

Computer science, or business and economics if the portal offers only broad categories. The subject sits between measurement methodology and marketing analytics.

### Previously published with other publishers

**Yes**, with this explanation:

```
An earlier and shorter version of this specification circulates as a working paper in the author's public research repository (github.com/alexandrebrt14-sys/papers). The author intends to deposit the specification as a working paper on SSRN, which assigns a DOI. The present book is an expanded derivative containing the field record, the descriptive evidence and the adoption guide, which the working paper does not carry. The author retains copyright in all versions.
```

---

## 2. SSRN (Elsevier)

### Title

```
Measuring Entity Citation in Generative Engines: The BRGEO-1 Protocol and a Five-Month Field Record
```

### Abstract (SSRN cuts above 1,920 characters; this is 1372)

```
Citation rates from generative engines travel as comparable figures while the conditions producing them stay unstated, so two honest measurements of the same firm disagree with no way to adjudicate. This paper specifies BRGEO-1, an open protocol that declares six of those conditions: observation window, cohort, query battery, engine panel with pinned versions, generation configuration and entity matching rule. On 2,225 matched observations, reading the whole response instead of the first 200 characters raised the citation rate by 22.95 to 55.73 points on five engines, with no observation losing its citation. Three engines running the full battery agree at a Fleiss kappa of 0.086. A multilevel model over 38,195 responses puts 45.6% of the variance at the prompt, 34.9% at the engine and 0.03% at the collection day, and the four factors the battery was balanced on explain under 1% of the variance between prompts, so declaring a battery is not the same as characterising it. Clustering by prompt gives a design effect of 63.3, cutting the effective sample to 1,083. A composite index built on of the same components ranks entities at correlations from 0.752 to 0.985 across defensible aggregations, so the specification constrains observation and leaves aggregation free. No inter-implementation exercise has been run, so comparability remains a design argument.
```

### Keywords

```
generative engine optimization; measurement standard; entity citation; large language models; construct validity; retrieval-augmented generation
```

### JEL classification

```
C81, C83, L86, M31
```

### Author

| Field | Value |
|---|---|
| Name | Alexandre Caramaschi |
| Affiliation | `Independent; Brasil GEO` |
| ORCID | 0009-0004-9150-485X |
| Networks | Information Technology & Systems; Quantitative Marketing |

The affiliation string and the two networks are the ones the author's previous
SSRN deposit uses (abstract 6460680, posted 2026-04-20), read from the public
record on 2026-09-11. Keeping them identical is what makes the two papers
resolve to the same author page. The earlier deposit also declares a Date
Written distinct from the posting date; do the same here, with the date the
manuscript was finished.

---

## 3. Order of operations

The order matters more than the dates, because publishing the book first closes the journal route.

1. **SSRN first.** The specification gets a dated DOI. Register it with ORCID through the Crossref auto-import.
2. **Eliva Press second.** The book is an expanded derivative; declare the SSRN deposit in the portal field above.
3. **Journal third.** Information Sciences, not Information Processing & Management: IP&M states that submissions should not be published as a preprint before a final decision, which is incompatible with an SSRN deposit. The journal version is a condensed derivative under that journal's length cap, with the field record, the descriptive evidence, the adoption guide and the appendices moved to supplementary material, and the cover letter declaring both the preprint and the book.

## 4. What is not ready, and should not be claimed

Three items from the manuscript's own limitations travel with any announcement.

- Conformance is self-declared. The conformance test suite and the interlaboratory study do not exist, so the claim that the protocol produces comparability is a design argument and not a measured result.
- The confirmatory window has not closed. Every finding in the book is descriptive; the projected close is 2026-10-15 at 90 collected days.
- The refusal taxonomy is proposed, not validated: no inter-annotator agreement, no gold standard, no measured distribution across the three categories.

---

## 5. Submission record

**SSRN, submitted 2026-09-11.**

| Field | Value |
|---|---|
| SSRN Abstract ID | 7446519 |
| Abstract page | https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7446519 |
| Content type | Preprint |
| License | Creative Commons Attribution (CC BY) |
| Author record | Alexandre Caramaschi, Independent AI Researcher, ORCID 0009-0004-9150-485X, contact author |
| Classifications | Information Technology & Systems; Marketing: Consumer Decision Making & Search; Marketing: Marketing Other; Artificial Intelligence; Generative AI |
| JEL | C81, C83, L86, M31 |
| Date written | 2026-09-11 |
| File | BRGEO-1-paper-v2.pdf, 183 pages, 2.23 MB |
| Status | under completeness review by SSRN staff; the DOI is issued on acceptance |

Two choices departed from the author's earlier deposit and both were deliberate.

**The licence is CC BY, where the 2026 deposit of abstract 6460680 reserved all rights.** The manuscript states in its governance section that the specification is published under CC BY 4.0 and the reference implementation under Apache-2.0. Depositing under a more restrictive licence would have made the record contradict the document, and an open standard nobody may reuse is not a standard.

**The affiliation reads Independent AI Researcher alone**, where the earlier deposit shows `Independent; Brasil GEO`. That string comes from the author profile rather than from the submission form, and changing it means editing the account. Brasil GEO appears inside the manuscript, on the custody line and throughout the competing-interest declaration, so nothing is concealed. Adding the second affiliation to the profile is a one-line change the author can make, and it applies to both papers at once.

### Next in sequence

1. Wait for the completeness review and the DOI, then register it with ORCID through the Crossref auto-import.
2. Eliva Press: the same PDF already meets the editor's format instruction. Declare the SSRN deposit in the portal field on prior publication.
3. Information Sciences: a condensed derivative under that journal's length cap, cover letter declaring both the preprint and the book.
