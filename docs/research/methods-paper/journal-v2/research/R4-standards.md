# R4 — Standards dossier for the BRGEO-1 methods paper

One operational document covering everything the manuscript must satisfy to (a) survive editorial triage at an Elsevier Q1 journal, (b) be accepted as a book block by Eliva Press, and (c) pass the house style ruler that keeps the prose from reading as machine output.

- Manuscript governed: `journal-v2/OUTLINE.md`, working title *Measuring Entity Citation in Generative Engines: The BRGEO-1 Protocol and a Five-Month Field Record*.
- Target venues: SSRN, then *Information Processing & Management* (IP&M, ISSN 0306-4573) or *Information Sciences* (ISSN 0020-0255). Same text, reformatted, becomes the Eliva Press book.
- External requirements verified on **11 September 2026** against the sources named in each row. Date of verification is repeated per block because guides change without notice.
- Confirmation markers used throughout:
  - **[P]** confirmed in a primary source (publisher or journal page, quoted).
  - **[S]** confirmed only in a secondary source (style repository, editor talk, trade press).
  - **[NAO CONFIRMADA]** could not be confirmed in a primary source; what was found is recorded next to the claim.

---

# PART A — Journal standards (Elsevier)

## A.0 The venue decision is a standards decision, not only a fit decision

The two candidate journals differ on four rules that change the shape of the submission package. The difference that matters most is preprinting.

| Rule | Information Processing & Management | Information Sciences |
|---|---|---|
| Peer review | Double anonymized **[P]** | Single anonymized **[P]** |
| Preprint before decision | "submissions should not be published as a preprint before a final decision has been made" **[P]** | Free SSRN posting offered at submission; posted "as soon as it passes the journal's initial desk review" **[P]** |
| Highlights | Not requested anywhere in the current Guide for Authors **[P, by absence]** | "You are encouraged to provide article highlights at submission"; 3 to 5 bullets, max 85 characters each including spaces **[P]** |
| Abstract ceiling | 250 words **[P]** | Guide states 250 words in the Abstract block and "up to 200 words" in the Article types block — internal conflict, see A.4 **[P]** |
| Section numbering | Not prescribed; "Divide your manuscript into clearly defined sections covering all essential elements using headings" **[P]** | "Divide your article into clearly defined and **numbered** sections. Number subsections 1.1 (then 1.1.1, 1.1.2, ...), then 1.2, etc." **[P]** |
| Reference style at submission | No reference-format block in the guide; published style is author-year **[S]** | "does not set strict requirements on reference formatting at submission... any style or format as long as the style is consistent"; published style is numeric **[P for the submission rule, S for the published style]** |
| Length guidance | None stated **[P, by absence]** | Experimental: max 40 double-spaced pages, 8 figures + tables. Theoretical: max 45 pages, 10 figures + tables **[P]** |
| Author bio | Not requested | Vitae: max 100 words per author plus a passport-type photograph, in editable format **[P]** |
| Data | Option C: deposit, cite and link, or state why data cannot be shared **[P]** | Data statement required at submission; reason accepted when data cannot be posted **[P]** |

**Consequence for the SSRN-first plan.** Posting to SSRN before a decision is compatible with *Information Sciences* and incompatible with IP&M as its guide currently reads. If IP&M is the target, the SSRN posting either waits for the final decision or the venue changes. This is a decision for the author, and it has to be taken before the preprint goes up, not after.

Source (both journals): ScienceDirect Guide for authors pages, fetched in full on 11/09/2026.
`https://www.sciencedirect.com/journal/information-processing-and-management/publish/guide-for-authors`
`https://www.sciencedirect.com/journal/information-sciences/publish/guide-for-authors`

## A.1 Article type and scope fit

IP&M names four manuscript types in its aims and scope, and the second one is the slot this paper occupies **[P]**:

1. Research manuscripts addressing topics at the intersection of computer and information science.
2. **Methods manuscripts focusing on the application of novel methods at the intersection of computer and information science.**
3. Review manuscripts assessing a broad trend in a critical and in-depth manner.
4. Critical application manuscripts concerning system design research.

The scope sentence to match: the journal "publishes cutting-edge original research at the intersection of computing and information science concerning theory, methods, or applications" **[P]**.

*Information Sciences* declares one type, "Original research work", and requires an Abstract and a **Conclusions section**, "which particularly in the case of theoretical papers translates the results into terms readily accessible to most readers" **[P]**.

Operational consequence: the introduction must state the information-processing or information-management contribution in its own words, not the machine-learning contribution. A protocol that only measures model output, with no informational claim, is the profile that editors at these venues screen out (see A.10).

## A.2 Structure and order of the manuscript

Neither guide prescribes a rigid IMRaD order. What both require, and what the file layout must deliver:

**Files at submission (IP&M, because of double anonymization) [P]:**
- Title page file: title, author names, affiliations with full postal addresses, corresponding author with full address and email, present/permanent address footnotes, **acknowledgements**, and the declaration of competing interests when a separate declaration file is not uploaded.
- Anonymized manuscript file: main body, references and tables, with **no** author names, affiliations or acknowledgements anywhere.
- Figures as separate files, one per figure, named `Figure_1`, `Figure_2`.
- Highlights as a separate editable file with the word "highlights" in the file name (Information Sciences only).
- Declarations Word document (.doc/.docx) uploaded at the "attach/upload files" step. Author signatures are not required **[P]**.

**Order inside the manuscript that satisfies both guides:**

1. Title, abstract, keywords.
2. Numbered body sections (1, 1.1, 1.1.1 …). Abstract is not included in the section numbering **[P, Information Sciences]**.
3. Conclusions section (mandatory for *Information Sciences*).
4. Acknowledgements, in a separate section directly before the reference list **[P, Information Sciences]**, and in the title page only, for IP&M **[P]**.
5. **CRediT author contributions statement** (published above the acknowledgements) **[P]**.
6. **Declaration of competing interest.**
7. **Funding** statement.
8. **Data availability** statement.
9. **Declaration of generative AI and AI-assisted technologies in the manuscript preparation process**, placed in "a new section before the references list" **[P]**.
10. References.
11. Appendices A, B, … with their own equation, table and figure numbering: Eq. (A.1), Table A.1, Fig. A.1 **[P, both]**.
12. Vitae (Information Sciences only): max 100 words per author plus photograph **[P]**.

Cross-references must use the section number, not "see above": "Use the numbering format when cross-referencing within your article. Do not just refer to 'the text'" **[P, Information Sciences]**.

## A.3 Title page fields

Required in both guides **[P]**: concise informative title with abbreviations avoided; given name and family name of every author in the same order as the submission system; affiliation addresses below the author names with lower-case superscript letters, full postal address including country and, where available, each author's email; a clearly indicated corresponding author with contact details kept current through publication; present/permanent address in a superscript-Arabic-numeral footnote when the author has moved.

## A.4 Abstract, keywords, highlights, JEL

**Abstract [P].** "You are required to provide a concise and factual abstract which does not exceed 250 words", stating purpose, principal results and major conclusions; it must stand alone; references avoided and, if essential, given as author and year; non-standard abbreviations avoided and defined at first mention. Identical wording in both guides.

Conflict to resolve: the *Information Sciences* Article types block says contributions "should contain an Abstract (of up to 200 words)" while its Abstract block says 250. **House rule: write to 200 words.** A 200-word abstract satisfies both readings; a 240-word abstract satisfies only one.

**Keywords [P].** "You are required to provide 1 to 7 keywords for indexing purposes. Keywords should be written in English. Please try to avoid keywords consisting of multiple words (using 'and' or 'of')." Abbreviations only when firmly established. Identical in both guides. The outline's six keywords comply; the prohibition is on joining words, not on multi-word terms of art.

**Highlights.** Required by neither journal as a condition of submission. *Information Sciences*: "You are encouraged to provide article highlights at submission... 3 to 5 bullet points, each a maximum of 85 characters, including spaces", submitted as a separate editable file with "highlights" in the file name **[P]**. IP&M's current guide contains no highlights block at all **[P, by absence; the guide's own table of contents lists no Highlights section, checked 11/09/2026]**. The outline's plan of five bullets at 85 characters is the correct target: it satisfies the Information Sciences ceiling and is harmless at IP&M. The house adds one constraint the publisher does not: **no citation inside a highlight**, because a highlight is indexed and displayed without its reference list.

**JEL classification. [NAO CONFIRMADA as a journal requirement.]** Neither guide mentions JEL codes; the fetched pages contain no JEL field. JEL is an economics classification and is used by SSRN's submission form, which is where the outline's C81; C83; L86; M31 belong. Carry the codes in the SSRN metadata, drop them from the journal manuscript unless the submission system asks.

## A.5 Section numbering and headings

*Information Sciences* **[P]**: numbered sections, subsections 1.1, then 1.1.1, 1.1.2, then 1.2; headings on a separate line; abstract outside the numbering.

IP&M **[P]**: "Divide your manuscript into clearly defined sections covering all essential elements using headings." No numbering rule is stated. Numbering is therefore safe for both and is what the house uses.

Footnotes: "use footnotes sparingly... numbered consecutively" **[P, Information Sciences]**.

## A.6 Tables, figures, captions and artwork

Identical requirements in both guides **[P]**:

- Tables as **editable text, never images**. Placed next to the relevant text or on separate pages at the end. **Every table cited in the text.** Numbered consecutively by order of appearance. Captions supplied with the tables. Table notes below the table body. **No vertical rules, no cell shading.** Tables used sparingly and never duplicating data described elsewhere.
- Figures supplied as **separate files**, one per figure, logically named. Every image cited in the text and numbered by order of appearance.
- "All images must have a caption. A caption should consist of a brief title (not displayed on the figure itself) and a description of the image." Text inside images kept to a minimum; symbols and abbreviations explained.
- Resolution: vector as EPS or PDF with fonts embedded or text saved as graphics; halftones as TIFF/JPG/PNG at **minimum 300 dpi** (single column ≥ 1063 px, full page ≥ 2244 px); bitmapped line drawings at **minimum 1000 dpi** (≥ 3543 px / ≥ 7480 px); line-halftone combinations at **minimum 500 dpi** (≥ 1772 px / ≥ 3740 px).
- Colour figures appear in colour online at no charge; print colour is quoted after acceptance. Colour must be accessible to readers with impaired colour vision.

Captions are the caption's own title plus a description. The house adds: the caption states what the figure shows as a claim, and carries the source and date of every number in it once (Part D).

## A.7 Mandatory declarations

### A.7.1 CRediT authorship **[P]**

"Corresponding authors are required to acknowledge co-author contributions using CRediT (Contributor Roles Taxonomy) roles." Fourteen roles, reproduced exactly as the guides list them: Conceptualization; Data curation; Formal analysis; Funding acquisition; Investigation; Methodology; Project administration; Resources; Software; Supervision; Validation; Visualization; Writing – original draft; Writing – review and editing.

Placement: roles are entered in the submission system, and "CRediT statements should be provided during the submission process and will appear above the acknowledgment section of the published paper" **[P, `https://www.elsevier.com/researcher/author/policies-and-guidelines/credit-author-statement`, fetched 11/09/2026]**.

Published format example from that page: `Zhang San: Conceptualization, Methodology, Software. Priya Singh: Data Curation, Writing - Original Draft.`

Single-author note: the taxonomy still applies and the statement still appears. A single-author paper lists the roles that author actually performed, not all fourteen.

### A.7.2 Declaration of competing interest **[P]**

"All authors must disclose any financial and personal relationships with other people or organizations that could inappropriately influence or bias their work." Examples the guide names: employment, consultancies, stock ownership, honoraria, paid expert testimony, patent applications or registrations, grants or any other funding, affiliation with the journal as an editor or advisory board member.

"The declarations tool should always be completed." Authors with nothing to declare "should select the option 'I have nothing to declare'". The resulting Word document is uploaded at the attach/upload step in .doc/.docx; author signatures are not required.

The canonical published sentence ("The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper") is **[NAO CONFIRMADA]** as an Elsevier-published template. It appears in tens of thousands of Elsevier articles and was returned by a Perplexity search on 11/09/2026 without a quotable Elsevier URL; the pages that do quote it are third-party. Elsevier's own declaration-of-interest page returned HTTP 404 on 11/09/2026. Use the sentence, since it is the field standard, but drive compliance through the declarations tool, which is the requirement the guide actually states.

Author-specific point for this manuscript: Brasil GEO is the custodian of the specification being evaluated. That relationship is a competing interest under "employment" and "affiliation", and it is declared, with the role named, in the manuscript declaration and in the submission tool. A protocol paper whose author owns the protocol is publishable; one that hides the ownership is retractable.

### A.7.3 Declaration of generative AI use **[P]**

The rule, quoted from both guides as fetched on 11/09/2026:

> "The use of AI Tools in the manuscript preparation process must be declared by adding a statement at the end of the manuscript when the paper is first submitted. The statement will appear in the published work and should be placed in a **new section before the references list**."
>
> - Title of new section: **Declaration of generative AI and AI-assisted technologies in the manuscript preparation process.**
> - Statement: **"During the preparation of this work the author(s) used [NAME OF TOOL / SERVICE] in order to [REASON]. After using this tool/service, the author(s) reviewed and edited the content as needed and take(s) full responsibility for the content of the published article."**

Surrounding obligations from the same block **[P]**:
- AI tools "must never be used as a substitute for human critical thinking, expertise and evaluation".
- The author is accountable for verifying accuracy and comprehensiveness of all AI-generated output, "including checking the sources, as AI-generated references can be incorrect or fabricated".
- The author must edit and adapt all material so the manuscript "represents the author's authentic and original contribution".
- "Authors must not list or cite AI Tools as an author or co-author."
- The declaration "does not apply to the use of basic tools, such as tools used to check grammar, spelling and references. If you have nothing to disclose, you do not need to add a statement."
- Images: "We do not permit the use of Generative AI or AI-assisted tools to create or alter images in submitted manuscripts", with a single exception where AI is part of the research design or methods, and then it must be described reproducibly in the methods section including model or tool name, version and extension numbers, and manufacturer. AI in graphical abstracts is not permitted; AI in cover art needs prior permission from editor and publisher.
- Reviewers and editors at these journals may not use generative AI in peer review at all.

Two consequences specific to this manuscript:

1. The paper *studies* generative engines. Model calls that are part of the instrument are **research methods**, not writing assistance, and belong in the methods section with pinned versions, which the outline already plans in §4.3 and §4.4. They do not go in the AI declaration. Mixing the two categories invites a reviewer to read the instrument as undisclosed writing assistance.
2. Any AI used for language, structure or literature triage during drafting goes in the declaration, with the tool named and the reason stated. The house position: declare it. The cost of declaring is zero, the cost of an undeclared tell found by a reviewer is a desk reject under ethics (see A.10, rank 8).

### A.7.4 Funding **[P]**

"Authors must disclose any funding sources who provided financial support for the conduct of the research and/or preparation of the article. The role of sponsors, if any, should be declared in relation to the study design, collection, analysis and interpretation of data, writing of the report and decision to submit the article for publication. If funding sources had no such involvement this should be stated."

Standard format: `Funding: This work was supported by the National Institutes of Health [grant numbers xxxx, yyyy]; ...`

No-funding sentence, quoted from the guide: **"This research did not receive any specific grant from funding agencies in the public, commercial, or not-for-profit sectors."**

For a self-funded protocol with a real API cost envelope (outline §4.7), the honest form names the entity that paid the inference bill even when no grant exists, because the cost envelope is reported in the paper and an unfunded paper with a five-figure cost line reads as an omission.

### A.7.5 Ethics **[P]**

"Authors must follow ethical guidelines stated in Elsevier's Publishing Ethics Policy." Neither guide imposes an ethics-approval statement for non-human-subjects work. This study queries commercial engines about organizations, not people; the statement needed is not an IRB approval but a paragraph on terms-of-service compliance and on the handling of any personal data that appeared in engine output. That paragraph is the house's own requirement, not the publisher's.

Submission declaration, implied by the act of submitting **[P]**: the work has not been published previously except as a preprint, abstract, published lecture, academic thesis or registered report; it is not under consideration elsewhere; publication is approved by all authors; if accepted it will not be published elsewhere in the same form, in any language, without the copyright holder's written consent.

**That last clause is the one the Eliva Press book collides with. See A.9.3.**

### A.7.6 Data availability **[P]**

IP&M applies **Option C**: "you are required to deposit your research data in a relevant data repository; cite and link to this dataset in your article; if this is not possible, make a statement explaining why research data cannot be shared."

*Information Sciences*: "To foster transparency, you are required to state the availability of any data at submission... If your data is unavailable to access or unsuitable to post, you can state the reason why."

Research data is defined broadly enough to cover this instrument **[P]**: "results of observations or experimentation that validate research findings, which may also include **software, code, models, algorithms, protocols, methods** and other useful materials related to the project."

Operational consequence: the query battery, the cohort file, the entity-matching rule, the collection pipeline and the missingness ledger are research data under this definition and are expected in a repository with a persistent identifier, cited in the reference list with the `[dataset]` prefix (A.8). Terms of service that forbid redistributing raw engine output are a legitimate reason to withhold the raw responses; they are not a reason to withhold the battery, the code or the derived tables.

Data linking: provide the repository link during submission; entities can also be linked inline as `Database: 12345` **[P]**.

Co-submission: both journals encourage a companion article in *MethodsX* or *Data in Brief*, submitted at the same time as a separate item on the "Attach files" page, auto-forwarded, linked on ScienceDirect if both are accepted, each carrying its own APC **[P]**. For a protocol paper this is the natural home for the full parameter tables that would otherwise bloat the appendix.

## A.8 References

### A.8.1 Rules common to both guides **[P]**

- Everything cited in the text appears in the list and vice versa.
- References cited in the abstract must be given in full.
- Unpublished results and personal communications should not appear in the list; if they do, they follow journal style with "unpublished results" or "personal communication" in place of the date.
- "in press" means accepted for publication.
- Reference data must be correct before submission: wrong surnames, journal or book titles, years or pagination break Scopus, Crossref and PubMed linking.
- "We encourage the use of Digital Object Identifiers (DOIs) as reference links."
- Web references: full URL plus last-accessed date as a minimum; DOI, authors, dates where known. May be listed separately after the reference list or inside it.
- **Preprint references**: mark preprints clearly, and include the word "preprint" or the preprint server name in the reference and give the **preprint DOI**. Where a preprint has since been published, cite the formal publication instead.
- **Data references**: author name(s), dataset title, data repository, version where available, year, global persistent identifier, with `[dataset]` immediately before the reference. The marker does not appear in the published article.
- **Software references** (stated in the Information Sciences guide, and good practice at IP&M): creator(s), title, publication venue (preferably an archive giving permanent identifiers), date or "n.d.", resolvable identifier (DOI preferred; Handle, RRID, ASCL, swMath, Software Heritage, ARK also named), version or date of access, and a bracketed type such as `[Computer software]` where the style requires one. "If an article exists that describes the software, it should be cited as an additional reference, as well as citing the software itself. Do not cite the article instead of the software."

### A.8.2 Style at submission

*Information Sciences* **[P]**: "This journal does not set strict requirements on reference formatting at submission... References can be in any style or format as long as the style is consistent... Author names, journal or book titles, chapter or article titles, year of publication, volume numbers, article numbers or pagination must be included, where applicable. Use of DOIs is recommended. Our journal reference style will be applied to your article after acceptance, at proof stage."

IP&M: the fetched guide contains **no reference-format block at all** **[P, by absence]**. The instruction it does give is that a template exists in reference management software and, failing that, "follow the format given in examples in the reference style section of this Guide for Authors", a section that is not present in the page as served on 11/09/2026.

### A.8.3 Published style of each journal **[S]**

The brief assumed numbered references in square brackets. That is right for one journal and wrong for the other.

| Journal | Published style | Evidence |
|---|---|---|
| Information Sciences | **Numeric, square brackets, order of appearance**, article titles retained | CSL dependent style `information-sciences.csl` declares `citation-format="numeric"` with independent parent `elsevier-with-titles`; EndNote style "Information Sciences" declares Citation Style: Non-superscripted Number, Bibliography Sort Order: Appearance-Order |
| Information Processing & Management | **Author-year (APA family)**, alphabetical then chronological | EndNote style "Information Processing and Management" declares Citation Style: Author-Year, Bibliography Sort Order: Author-Year-Title; Paperpile: "References should be cited in the text by name and year in parentheses" |

Elsevier's numeric model, for the Information Sciences case: `Text: Indicate references by number(s) in square brackets in line with the text. The actual authors can be referred to, but the reference number(s) must always be given.` List example: `[1] J. van der Geer, J.A.J. Hanraads, R.A. Lupton, The art of writing a scientific article, J. Sci. Commun. 163 (2010) 51–59. https://doi.org/10.1016/j.Sc.2010.00372.`

**House rule.** Draft the bibliography in a reference manager with both styles installed, keep every field populated (authors, full title, container, volume, article number or pages, year, DOI), and switch styles at venue selection. Both journals restyle at proof anyway; what neither will fix is a missing DOI or a wrong page range.

## A.9 Preprint, prior publication and the derived book

### A.9.1 Preprint **[P]**

Elsevier policy: "Authors can share their preprint anywhere at any time", and "if accepted for publication, we encourage authors to link from the preprint to their formal publication via its Digital Object Identifier (DOI)." Updating a preprint on arXiv or RePEc with the accepted manuscript is allowed, with the licence updated to **CC BY-NC-ND** and a DOI link to the formal publication.
Source: `https://www.elsevier.com/about/policies-and-standards/sharing`

Journal-level overrides, which beat the general policy:
- IP&M: "Sharing preprints, such as on a preprint server, will not count as prior publication." Then: "**Note that this journal follows a double anonymized peer review process, and therefore submissions should not be published as a preprint before a final decision has been made.**" **[P]**
- *Information Sciences*: "In support of Open Science, this journal offers its authors a free preprint posting service on SSRN, Elsevier's preprint and early research repository. During submission to this journal, you can choose to post your manuscript on SSRN, and it will be made publicly available **as soon as it passes the journal's initial desk review**... Your decision to post or not post your preprint will have no effect on the editorial process or publication outcome... It is expected that the corresponding author will seek approval from all co-authors before agreeing to post the manuscript publicly, prior to peer review, on SSRN." **[P]**

SSRN is Elsevier's own preprint server **[S: `https://www.elsevier.support/ssrn/answer/ssrn-elseviers-preprint-server`]**.

**How to declare the preprint.** For *Information Sciences* the declaration is a checkbox inside Editorial Manager, not a paragraph. For any other venue: name the preprint server and the preprint DOI in the cover letter, and cite the preprint in the manuscript only if the paper builds on it. Once the article is published, update the preprint record with the DOI of the version of record.

### A.9.2 Prior publication **[P]**

Elsevier publishing ethics, quoted:
- "An author should not in general publish manuscripts describing essentially the same research in more than one journal of primary publication."
- "Submitting the same manuscript to more than one journal concurrently constitutes unethical behaviour and is unacceptable."
- "An author should not submit for consideration in another journal a paper that has been published previously, **except in the form of an abstract or as part of a published lecture or academic thesis or as an electronic preprint**."
- Secondary publication is "sometimes justifiable, provided certain conditions are met": both sets of authors and editors agree, the secondary version "must reflect the same data and interpretation of the primary document", and "the primary reference must be cited in the secondary publication."

Source: `https://www.elsevier.com/about/policies-and-standards/publishing-ethics`, fetched 11/09/2026.

The IP&M submission declaration adds **registered report** to the list of things that do not count as prior publication **[P]**.

**A book is not on the exemption list.** Neither is a book chapter.

### A.9.3 The derived book: the unresolved collision

The facts, stated plainly:

1. Elsevier's submission declaration says that if accepted, "the article will not be published elsewhere in the same form, in English or in any other language, including electronically, without the written consent of the copyright-holder" **[P]**.
2. The exemptions for prior publication are abstract, published lecture, academic thesis, electronic preprint and registered report. A commercially published book is not among them **[P]**.
3. Elsevier publishes no page that tells an author how to disclose a derived or parallel book at submission. **[NAO CONFIRMADA.]** Searched on 11/09/2026 across the sharing policy, the hosting policy, the policies-and-guidelines index and the publishing-ethics page; a Perplexity sonar-pro run over the same corpus also failed to surface one and said so explicitly. What exists is the general redundant-publication rule and the secondary-publication conditions quoted above.
4. Elsevier screens with Crossref Similarity Check and Editorial Manager's duplicate submission check, and warns that "a high similarity score does not necessarily indicate plagiarized text" **[P, `https://www.elsevier.com/editor/perk/plagiarism-complaints/plagiarism-detection`]**. **No numeric similarity threshold is published anywhere. [NAO CONFIRMADA]**

Given those four facts, the defensible sequence, which is house position and not publisher instruction:

- The **journal article comes first** in time, or at least in submission. A book published before the article converts the article into a secondary publication of a book, which the exemption list does not cover.
- The book is **disclosed in the cover letter** at submission, naming the publisher, the planned date, and the proportion of overlapping text, with the offer to supply the manuscript for similarity comparison. Disclosure that the editor did not ask for costs nothing; an overlap found by iThenticate after review costs the submission.
- The two texts are **differentiated at the level of what they contain**, not at the level of paraphrase. Reworded overlap still scores as overlap. The article carries the specification, the field record and the evidence; the book carries the operational chapters, the worked instantiation and the material a journal would cut for length.
- If the journal accepts, the book **cites the article as the primary reference** and states on the copyright page that it derives from it, which is the condition Elsevier sets for any secondary publication.
- Eliva Press's own portal asks for a declaration of previous publication (Part B). That declaration and the cover letter must say the same thing.

## A.10 What causes desk rejection at these venues

Ranked, with the evidence level marked. The ranking is synthesized from editorial studies and editor statements rather than from a published policy at either journal; treat the order as a risk register, not as a measured distribution.

| # | Cause | Evidence | What it means for this manuscript |
|---|---|---|---|
| 1 | **Out of scope / poor journal fit** | Most frequently cited cause across editorial analyses; one content analysis of rejection letters put it at 17.4% of desk rejections, one transport journal reported 35% **[S]** | The abstract and §1.3 must name the information-science contribution, not only the measurement engineering |
| 2 | **No novelty / incremental contribution** | Same content analysis found lack of novelty or originality in 46.3% of desk-rejection cases **[S]** | A protocol is novel only if §2.8 shows, with citations, what the literature leaves unmeasured |
| 3 | **Methodological weakness visible at triage**: no baseline, unjustified sample, design that cannot support the claim | Editorial guides and cross-journal studies **[S]** | The cohort size, tier stratification and factorial balance must be defended in the abstract, not deferred to §4 |
| 4 | **Guide-for-authors non-compliance and missing declarations** | Editor checklists reported in publishing guides **[S]** | Everything in A.7 present before the first upload; over word count is on the same checklist |
| 5 | **Poor English, unclear structure** | Repeatedly named in editorials **[S]** | Part C is the mechanism for this row |
| 6 | **Ethics: plagiarism, citation manipulation, excessive self-citation** | Publisher ethics policies; screening happens pre-review **[S]** | Self-citation to Brasil GEO material is a live risk in a protocol paper by the protocol's custodian. Cap it, and justify each one |
| 7 | **No reproducibility where the field expects it** | Emerging; informetrics venues expect transparent, reproducible method **[S]** | Repository, pinned model versions, seeds, prompts. Absence here is fatal in 2026 for an LLM-evaluation paper |
| 8 | **Undisclosed LLM-generated text** | Publisher GenAI policies now make this an ethics category **[S]** | A.7.3 plus Part C |
| 9 | **No statistical testing where the claim requires it** | Subsumed under row 3 **[S]** | Any comparative claim in §5 or §6 carries a test, an effect size and an interval |

**Desk-reject rate at IP&M: approximately 67%. [NAO CONFIRMADA.]** The number comes from a presentation by Bernard J. Jansen, a co-editor of IP&M ("The Perilous Journey of Journal Publishing"), reported via secondary sources on 11/09/2026, not from a journal editorial or an Elsevier page. Treat it as an order of magnitude that matches the 30-70% band reported for selective journals, and never cite it in the manuscript.

IP&M publishes no "we will not consider" list **[P, by absence]**. The screening criteria attributed to the same editor presentation are: out of scope, not novel or purely exploratory, over word count, non-compliance with submission guidelines **[S]**.

## A.11 Method, protocol, benchmark and resource papers

- **IP&M accepts methods manuscripts by name** in its aims and scope **[P]**, which is the strongest single argument for IP&M over *Information Sciences* for this paper.
- **MethodsX** exists precisely for method and protocol articles and is offered as a co-submission from both journals, with a mandatory template **[P]**.
- **Data in Brief** exists for dataset descriptions, same co-submission route **[P]**.
- *Information Sciences* declares one article type, "Original research work", with page and figure guidance **[P]**. A protocol paper fits only if it is framed as original research with results, which the five-month field record supplies.
- **Registered reports** are named in the IP&M submission declaration as a format that does not count as prior publication **[P]**, which implies the format is recognised; whether IP&M accepts registered-report submissions is **[NAO CONFIRMADA]**, because the guide has no registered-report block.
- Neither guide publishes special requirements for method, benchmark or resource papers beyond the general rules. **[P, by absence.]** What the field expects in 2026 (prompt disclosure, pinned model versions and dates, seeds and decoding parameters, a reproducibility package, an explicit statement of what is not reproducible because the vendor changed the model) is convention, not a published journal rule, and this dossier records it as house policy rather than as an external requirement.

## A.12 Pre-submission checklist

Elsevier's own list **[P]**: corresponding author designated with email, full postal address and phone; all files uploaded including keywords, figure captions and tables with title, description and footnotes, plus supplementary material and videos; spelling and grammar checked; every reference in the text present in the list and vice versa; permission obtained for copyrighted material including material from the web; open-access authors aware they are responsible for the APC if accepted.

House additions, in the order they are checked:

1. Abstract at or under 200 words, keywords between 1 and 7, no joining words.
2. Highlights file, 5 bullets, each at 85 characters or fewer including spaces, no citations.
3. Sections numbered; abstract outside the numbering; every cross-reference by number.
4. Title page separated from the anonymized manuscript; the manuscript searched for the author's name, the affiliation, the ORCID, "Brasil GEO" and every self-citation that reveals authorship.
5. All six declarations present and in order: CRediT, competing interest, funding, ethics or terms-of-service, data availability, generative AI.
6. Every table editable text, cited in the text, no vertical rules, no shading.
7. Every figure a separate file at the right resolution, cited in the text, caption with a brief title plus description.
8. Every reference carries a DOI where one exists; preprints marked with the server name and preprint DOI; datasets prefixed `[dataset]`; software cited as software.
9. Repository deposited, cited and linked; or the statement explaining why not.
10. Cover letter naming the preprint and the Eliva Press book.
11. Part C run over the full text. Part D run over every percentage.

---

# PART B — Book publisher standards (Eliva Press)

Canonical facts supplied by the house and recorded here as the binding specification for the book block. Where a published Eliva document confirms the item, the source is named; the two items that come from the editor's email of 09/09/2026 are marked as such, and that email prevails over the general guide where they conflict.

## B.1 Extent and file

| Requirement | Value | Source |
|---|---|---|
| Minimum extent | **35 pages** | House canonical; the published Formatting Recommendations specify margins for the band "From 35 to 300 Pages", which is consistent with 35 as the floor |
| File format | PDF | House canonical |
| Page orientation | **Every page portrait** | House canonical |
| Page size | **A4** | Eliva Press, *Formatting Recommendations*, item 1 |
| Margins (35–300 pages) | **2 cm / 0.79 in on all four sides**; text and images must not overlap the margins | Eliva Press, *Formatting Recommendations*, item 10 |
| Margins (301–700 pages) | 3 cm left and right, 2 cm top and bottom; mirrored margins preferred (3 cm inside, 2 cm outside, 2 cm top and bottom) | Same source; recorded in case the book grows |

## B.2 Typography

| Requirement | Value | Source |
|---|---|---|
| Body face | Times New Roman | Editor instruction by email, **09/09/2026**; the published guide names Arial, Times New Roman or Calibri as best choices |
| Body size | **16 pt** | **Editor instruction by email, 09/09/2026. This overrides the published guide**, which says "Font size 14" (*Formatting Recommendations*, item 2) |
| Line spacing | **1.5** | Editor email 09/09/2026; the published guide allows 1.1 to 2 and calls 1.5 "the best choice" |
| Fonts embedded | All fonts embedded | *Formatting Recommendations*, item 5 |
| Overlapping text | None | *Formatting Recommendations*, item 6 |

Body at 16 pt with 1.5 spacing on A4 with 2 cm margins yields roughly 26 to 28 lines per page. A 20,000-word manuscript lands well past the 35-page floor; the risk at this size is the opposite one, a book block that runs long enough to cross the 300-page margin band. Recount pages after the first full build.

## B.3 Front matter and pagination

| Requirement | Value | Source |
|---|---|---|
| Table of contents | Present, at the front of the book block | *Formatting Recommendations*, item 12 |
| TOC numbered | Yes | *Formatting Recommendations*, Table of contents block |
| TOC length | **Maximum 3 pages** (recommendation) | Same block |
| TOC accuracy | "Table of contents page numbers should match with content" | Same block |
| Page numbers | **All pages continuously numbered** | *Formatting Recommendations*, item 11 |
| Certificate pages | Removed | *Formatting Recommendations*, item 13 |

A TOC generated by the build script from real page numbers is the only version that satisfies the matching rule after a reflow. A hand-typed TOC breaks on the first edit.

## B.4 File hygiene

| Requirement | Value | Source |
|---|---|---|
| Watermarks | None; any watermark removed | *Formatting Recommendations*, item 7 and the Watermarks block |
| PDF creation logos | None | *Formatting Recommendations*, item 7 |
| Security | "Passwords, locks, restrictions, encryptions (if any) should be removed" | *Formatting Recommendations*, File protection block |

## B.5 Tables, figures and notes

| Requirement | Value | Source |
|---|---|---|
| Table titles | "Each table should have a short title" | *Formatting Recommendations*, Tables block |
| Table body size | **Minimum 10 pt** | Same block |
| Tables and margins | All tables fit inside the required margins; split large tables; landscape acceptable | Same block |
| Figure titles | "Each figure should have a short title" | Figures block |
| Figure and illustration text | **Minimum 10 pt** | Figures block |
| Image resolution | **Minimum 300 dpi** | Figures block and item 9 |
| Colour | **"All color figures will be converted in black and white version"** | Figures block |
| Footnotes | Acceptable, minimum 10 pt | Footnotes block |
| References | May be at the end of the manuscript or after each chapter; citation required; "Plagiarism is not acceptable" | References block |
| Appendices | At the end of the manuscript; photographs, maps and scanned pages recommended for appendices | Appendices block |

**The black-and-white conversion is a design constraint, not a printing detail.** Every figure that separates series by hue alone becomes unreadable in the printed book. Series are separated by shape, dash pattern, direct labelling or fill texture, and the figure is checked in greyscale before it ships. This applies to the same figures that will run in colour online in the journal version: one artwork, legible in both.

Source for B.1 to B.5 where marked: Eliva Press SRL, *Formatting Recommendations*, updated 04/09/2020, registration number 1020600000328, `www.elivapress.com`. Copy on file in the session scratchpad, read 11/09/2026.

## B.6 Portal metadata

Canonical, supplied by the house:

| Field | Requirement |
|---|---|
| Blurb | **Above 600 characters** |
| Author biography | **Up to 500 characters** |
| Keywords | Required |
| Category | Required |
| Previous publication | Declaration required |

Three operational notes. The blurb is the only piece of house copy that a stranger reads before deciding, and it is written under Part C like any other prose. The 500-character biography is the same object as the *Information Sciences* Vitae (100 words, roughly 600-700 characters) with a tighter belt, so write the biography once at 500 characters and let the journal version expand. The previous-publication declaration must agree with the journal cover letter, word for word on the facts (A.9.3).

---

# PART C — Anti-AI style ruler, operational checklist in English

Converted from `C:/Sandyboxclaude/Escrita-Empresarial` (README.md, DIRETRIZ.md, MANUAL.md, exemplos/bom.md, exemplos/ruim.md), read 11/09/2026, and adapted to English academic prose. The source system grades findings at three levels and refuses to turn rhythm measurements into targets; both properties are preserved here.

Three adaptations are deliberate and are flagged where they occur, because applying the Portuguese rule unchanged would damage an academic manuscript:

- **The roadmap paragraph.** The house bans self-narration ("este artigo apresenta"). Academic convention expects a contributions-and-structure paragraph at the end of the introduction, and IP&M reviewers look for it. Adapted rule in C.1.5.
- **The methods section.** The house bans verification meta-discourse ("verificamos que"). A methods section is nothing but the narration of procedure, and it is mandatory. Adapted rule in C.1.6.
- **Limitations.** The house bans confidence labels without a measured number ("amostra de conveniência"). Construct-validity and limitations sections are required by the field and by this paper's own argument. Adapted rule in C.1.11.

## C.1 FAIL — the text does not ship until these are zero

**C.1.1 Formulaic antithesis.** The structure that denies a weak version of a claim in order to inflate the strong one. English forms: *not merely X, but Y* · *it is not about X, it is about Y* · *this is not X; it is Y* · *X is not the problem, Y is the problem* · *less about X and more about Y* · *far from being X* · *not only X but also Y* used as rhetorical addition · *the question is not whether, but when* · *more than X, this is Y*.
Fix: assert what the evidence supports. Denying X adds no information about Y.
Not covered: plain negation, which is correct English and stays: *the guide does not state a word limit*, *no engine cited the entity*. Deleting the "not" to dodge the rule produces a broken sentence; when the sentence must negate, negate.
Graduation, as in the source system: an isolated structural antithesis without a set formula (*it is not X: it is Y*) warns on first occurrence and fails on the second in the same text.

**C.1.2 Pseudo-profound closers.** *The future is already here* · *this changes everything* · *the best is yet to come* · *one thing is certain: change* · *this is only the beginning* · *the writing is on the wall* · *at the end of the day*.
Fix: close with the decision, the number or the consequence the section promised.

**C.1.3 Filler connective opening a paragraph.** *Moreover,* · *Furthermore,* · *Additionally,* · *It is worth noting that* · *It is important to note that* · *In this context,* · *In this regard,* · *That said,* · *Notably,* · *Importantly,*.
Fix: delete. When the logic of the text is sound the transition is already implicit. Substituting a synonym keeps the metronome and adds a tic.
The best replacement is a transition that carries information: not *In this context, the panel was re-pinned*, but *With three of five models deprecated inside the window, the panel was re-pinned*.
Density rule from the source system: more than one worn connective per 250 words, floor of four in the text, fails regardless of position. The same connective opening two consecutive paragraphs fails.

**C.1.4 Preamble.** *Before we begin* · *In this document* · *It is important to contextualize* · *First of all* · *In what follows we present* · *This section will discuss*.
Fix: say the thing. The first sentence of every section is that section's conclusion, not its announcement, and it stays under 45 words.

**C.1.5 Self-narration.** *This paper presents* · *This study aims to* · *The present article seeks to* · *In this work, we will explore*.
**Adapted for academic prose.** The convention of a contributions paragraph is preserved: one roadmap passage is allowed, at the end of the introduction, and one first-person framing sentence is allowed in the abstract. Both must carry the claim rather than the act. *This paper presents a protocol for measuring entity citation* fails. *The BRGEO-1 protocol fixes six parameters that any citation-rate claim must declare, and a five-month record shows what happens to the number when one of them moves* passes. Everywhere else, in results, discussion and conclusions, self-narration fails.

**C.1.6 Verification meta-discourse outside the methods section.** *We verified that* · *After extensive research* · *Sources consulted* · *Our methodology suggests* · *As calculated using our approach* · *Data were checked*.
**Adapted for academic prose.** Inside Methods, procedure narration is the section's job and is required. Outside Methods, in the introduction, results, discussion and conclusions, the finding arrives with its number and its citation, and the story of how it was checked stays in Methods. *We verified that 62% of responses cited a source* fails in Results; *62% of responses (n = 1,440) cited at least one source* passes.

**C.1.7 Stylistic em dash in prose.** The em dash and en dash are banned in running prose and tolerated in headings and table cells. Rewrite with a comma, a colon, parentheses or two sentences.
Note on evidence: the claimed rise of the em dash in LLM output is **[NAO CONFIRMADA]**: a Perplexity run on 11/09/2026 found no peer-reviewed study that quantifies it, only field guides. The rule stands as a house preference, not as a detection result.

**C.1.8 Vague attribution with no source in the sentence.** *Studies show* · *Research suggests* · *Experts agree* · *It is widely believed* · *The literature indicates* · *Recent work has shown*, each without a citation in the same sentence.
Fix: name the source with its year, or cut the claim. In a paper this rule is nearly free, because the citation is required anyway; what it catches is the sentence that gestures at a body of work no reference supports.

**C.1.9 Paragraph over 2,200 characters.** Warns at 1,500. Measured on prose only: lists, tables, code and source notes are outside the count, and a block of three paragraphs separated by blank lines answers for each paragraph separately.
The ceiling limits size and never demands haste. One 1,400-character paragraph that develops the whole argument beats four 300-character paragraphs that slice the same argument into scannable pieces.

**C.1.10 Repeated empty adjective.** *robust* · *crucial* · *strategic* · *transformative* · *disruptive* · *powerful* · *innovative* · *essential* · *pivotal* · *seamless* · *comprehensive* · *cutting-edge* · *state-of-the-art* used as praise · *significant* used non-statistically.
A single root repeated more than twice fails; five empty adjectives across the text fails as a series. The fix is never the synonym: replace the adjective with the number, the variance or the consequence that would have justified it.

**C.1.11 Confidence label with no measurement.** *the data are robust* · *this is a convenience sample* · *no denominator was declared* · *treat as an order of magnitude* · *correlation, not experiment*, when the paragraph carries no number.
**Adapted for academic prose.** Limitations and construct-validity discussion are mandatory, and this paper argues about measurement validity for a living, so it cannot hedge its own hedging. The adapted rule: every limitation statement carries its measurement. *The cohort is a convenience sample* fails. *The cohort of 84 organizations was drawn from one national registry and one tier is represented by 11 entities, which bounds any tier-level claim* passes. The banned form is the caveat with no number anywhere in the paper.
The decision rule behind it survives the adaptation intact: **if the data do not support the claim, rewrite the claim or cut the data.** A number that can only be stated with three caveats should not be stated. A caveat glued to a number transfers to the reader a decision that belongs to the author.

**C.1.12 Labelled alert opening a paragraph.** *Note:* · *Important:* · *Caveat:* · *Disclaimer:* · *Warning:*.
Fix: the caveat that matters becomes a sentence of the argument, with its condition and its number inside.

**C.1.13 Percentage without a denominator.** See Part D. Any percentage whose n is not recoverable from the sentence, the previous sentence or the table it points at fails.

**C.1.14 Published errata inside the text.** *An earlier version of this paper* · *corrected figures* · *updated on 23/08*. Version history lives in the repository and in the publisher's correction record, not in the prose.

**C.1.15 Fabricated scarcity and advertisement imperatives.** Irrelevant in the manuscript, live in the Eliva blurb and any launch copy: *limited spots* · *act now* · *don't miss* · *unlock the power of* · *learn more* as a sentence.

## C.2 WARN — passes, and the author answers each one in writing or fixes it

- **Transition connective opening a paragraph**: *However,* · *In contrast,* · *On the other hand,* · *In summary,* · *Finally,* · *Overall,* · *Thus,* · *Consequently,*. These are legitimate glue at low dose; opening two consecutive paragraphs with the same one is scaffolding and fails under C.1.3. Paragraph-initial *Furthermore*, *Moreover* and *Overall* are the single clearest empirical marker of machine-drafted essays reported to date (Inside Higher Ed, *Anatomy of an AI Essay*, 2024) **[S]**.
- **Contrastive apposition in series**: *X, not Y* (*a hypothesis, not a verdict*). Warns at 3 per 1,000 words, fails at 5 per 1,000, with absolute floors of 3 and 5 for short texts. The coordinated form *, and not* is coordination and does not count.
- **Mirror conclusion**: a conclusions section that restates the abstract with no new consequence. Detected by content-word overlap; 50-60% warns, 60% or more with five shared words and no new number fails. Restating the recommendation is legitimate; adding nothing is the defect.
- **Repeated paragraph opening**: the same three opening words three times.
- **Paragraph over 1,500 characters.**
- **Generic heading**: *Introduction* and *Conclusions* are conventional and stay. Subsection headings that name a drawer rather than a claim (*Context*, *Discussion*, *General considerations*, *Other findings*) warn. The subsection heading carries the section's message.
- **Nominalization that hides the agent**: *the implementation of the measurement of* · *the utilization of* · *the operationalization of*. Use the verb and say who does what.
- **Copula evasion and posture verbs**: *serves as* · *acts as* · *functions as* · *positions itself as* · *plays the role of* where *is* resolves.
- **Vague gerund closing a sentence**: *contributing to* · *promoting* · *enabling* · *facilitating* · *paving the way for*. Say the result instead of gesturing at it.
- **Wordy locutions**: *due to the fact that* → because · *in order to* → to · *with regard to* / *in the realm of* → about, in · *a number of* → give the number · *it should be emphasized that* → delete.
- **Intensifier adverbs in series**: *extremely*, *highly*, *entirely*, *truly*, *basically*. Three or more in the text warns.
- **Concentrated -ly adverbs**: four or more in one paragraph warns. The fix is the strong verb or the number.
- **Source-introducer density**: more than one *according to* / *as shown by* / *following* per 120 words is citation ceremony. Name the source in full at first mention, short after that.
- **Percentage with no source in the paragraph or the one before it.**
- **Scarce visual support in long material**: fewer than one table or figure per 5,000 characters of prose, counted from the first multiple. Code listings, prompt examples and source notes are apparatus and do not count as visual relief.
- **Rhetorical questions in series**: warns above one per 300 words with a floor of three; five or more at double density fails. A paper that lists the questions a protocol must answer is content; a run of rhetorical questions is not.
- **Duplicated function word** (*the the*, *of of*) and **emoji in prose**.

## C.3 DIAGNOSTIC — reported, never a reason to reject

The source system is explicit that these are measurements and never targets, because a rhythm quota produces the staccato it was meant to prevent. They are printed for the author to judge.

- **Rhythm triad**: a three-term enumeration closing a sentence. Two warn in the source system's own grading; here it is reported only, because an enumeration of three is content as often as it is rhythm and the cheap fix (turning it into a list) fragments the text.
- **Sentence-length uniformity**: low standard deviation across the text.
- **Paragraph symmetry**: three consecutive paragraphs with the same sentence count.
- **Inversion share**: more than half the sentences opening with a subordinate clause or an adjunct.
- **Sentence over 60 words.**

## C.4 REQUIRED — what the ruler demands, not only what it forbids

1. **Chained reasoning.** Every paragraph adds an idea the previous one did not contain. A paragraph that restates its predecessor in new words is cut, not rewritten.
2. **Varied sentence length, produced by meaning.** Join into one long period the reasoning that carries cause and qualification together; leave short the sentence that closes the block or marks the turn. No quota in either direction.
3. **Justified recommendation.** Every recommendation states the evidence that produces it and the cost of not following it. In this manuscript that applies to each of the six parameters: the rationale and the failure mode, which the outline already demands in §3.1.
4. **The answer before the argument.** Recommendation, decision or conclusion inside the first 120 words of the section; the first sentence of each section is that section's conclusion.
5. **One source and date per paragraph.** The first number in a paragraph carries its source and date; the rest inherit.
6. **The close delivers.** Decision, cost, deadline, owner or next step. A close that only summarizes is the defect.
7. **Anti-tic re-read before delivery.** A final pass whose only job is to hunt the patterns in C.1 and C.2. In the source system this pass caught a published page that had eleven contrastive appositions and two antitheses after an instruction had forbidden both in writing. The instruction existed; the pass was what removed them.

## C.5 Rules that stayed behind, and why

These are in the Portuguese ruler and do not cross into English academic prose. Recording them prevents someone from re-importing them later as an oversight.

| Portuguese rule | Why it stays out |
|---|---|
| Full Brazilian orthographic accentuation | Language-specific. English has no equivalent obligation |
| Decimal comma, period for thousands (`1.290`, `4,5`) | **Inverts in English**: decimal point, comma for thousands. Elsevier copy-editing expects `1,290` and `4.5`. Carrying the Portuguese rule over would corrupt every number in the paper |
| No comma before "e" in a simple enumeration | **Inverts in English**: the serial comma is the dominant academic convention and Elsevier accepts it. Choose one and hold it |
| Numbers zero to ten spelled out, digits from 11 | Replaced by the English academic convention: spell out below ten in running prose, use digits with units, percentages, table references, section numbers and any statistic (`n = 8`, `8 engines`, `3 of 12`) |
| No title case in headings | Kept in spirit, not as a Portuguese rule: Elsevier's house style is sentence case for headings, so the outcome matches |
| Percentage attached to the numeral (`37%`) | Kept: English academic style also closes up `37%`. Carried over rather than dropped |
| *Gerundismo* (*vamos estar enviando*) | Grammatically impossible in English |
| Portuguese calques from English (*endereçar*, *suportar*, *alavancar*, *performar*, *eventualmente*, *no final do dia*, *dor do cliente*) | The calque runs the other way. English equivalents that do belong in the ruler (*leverage*, *utilize*, *at the end of the day*) are in C.6 |
| Duplicated Portuguese function words (*de de*, *que que*) | Replaced by the English equivalent (*the the*, *of of*) in C.2 |
| Excessive possessive (*lave suas mãos*) | English requires the possessive where Portuguese does not |
| Genre templates (memorando, parecer, proposta) and their word ceilings and H2 quotas | Business-document genres. The academic genre's structure comes from Part A |

## C.6 Expressions and constructions in English that mark a paper as machine-drafted

Empirical basis, verified 11/09/2026. Kobak et al., *Delving into ChatGPT usage in academic writing through excess vocabulary* (arXiv:2406.07016), analysed roughly 14 to 15 million PubMed abstracts from 2010 to 2024 and identified "excess words" whose 2023-2024 frequency far exceeded the pre-LLM trend: *delves* rose about 25-fold, *showcasing* and *underscores* about 9-fold, with *potential*, *findings*, *crucial*, *pivotal*, *grappling*, *intricate* and *insights* also prominent; the study estimates that at least 10 to 13.5% of 2024 abstracts carry this vocabulary, higher in some subcorpora **[S: arXiv preprint, read via secondary summaries on 11/09/2026; the full 774-word list is in the authors' data release, not in the article text]**. A 2026 Wiley study, *Lexical Traces of AI: Linguistic Impact of Generative Tools on Scholarly Style*, reports the same top five stems across disciplines: *delv-*, *underscor-*, *intricat-*, *meticulous-*, *showcas-* **[S]**. Juzek and Ward (2025) report 21 LLM-associated terms including *delve*, *underscore* and *intricate* **[S]**.

Forty entries. The replacement column is the point: deleting the phrase without supplying the missing content only hides the defect.

| # | Avoid | Use instead |
|---|---|---|
| 1 | delve into | examine; analyse; test |
| 2 | it is worth noting that | delete and state the fact |
| 3 | it is important to note that | delete; if the point matters, it is a sentence of the argument |
| 4 | in today's rapidly evolving landscape | name the change, its date and its size |
| 5 | this study aims to shed light on | state the result the study produced |
| 6 | sheds light on / sheds new light on | measures; shows; quantifies |
| 7 | plays a crucial role in | name the mechanism: *determines*, *accounts for 41% of the variance* |
| 8 | a testament to | evidence of; or delete |
| 9 | navigating the complexities of | name the specific difficulty |
| 10 | rich tapestry / tapestry of | delete |
| 11 | underscores the importance of | shows that; or delete |
| 12 | showcases / showcasing | shows; reports; presents |
| 13 | intricate | complex; or name the interacting parts |
| 14 | meticulous / meticulously | delete and describe the procedure |
| 15 | pivotal | give the effect size |
| 16 | crucial / vital (as praise) | give the number that makes it matter |
| 17 | robust (unquantified) | give the variance, the interval or the stress test it survived |
| 18 | comprehensive overview | *a survey of 48 papers, searched on 12/03/2026* |
| 19 | state-of-the-art / cutting-edge | name the baseline, its citation and its date |
| 20 | paradigm shift | name what changed and what it replaced |
| 21 | leverage (verb) | use |
| 22 | utilize | use |
| 23 | seamless / seamlessly | delete |
| 24 | holistic | name what is included |
| 25 | multifaceted | name the facets |
| 26 | myriad / a plethora of | give the count |
| 27 | foster / fostering | cause; increase; or name the mechanism |
| 28 | has garnered significant attention | give the paper count, the database and the search date |
| 29 | the ever-growing / ever-increasing | give the rate and the period |
| 30 | bridge the gap | name the gap and cite the paper that leaves it open |
| 31 | not only X but also Y | split into two clauses, or drop the weaker one |
| 32 | Moreover, / Furthermore, opening a paragraph | delete; the strongest reported marker of machine drafting |
| 33 | as previously mentioned | cross-reference the section number |
| 34 | in the realm of | in |
| 35 | embark on | begin; or delete |
| 36 | unlock the potential of | state the measured gain |
| 37 | game-changer | give the delta against the baseline |
| 38 | to the best of our knowledge (as proof of novelty) | state the search: database, query string, date, number of hits screened |
| 39 | significant (non-statistical use) | reserve for statistical significance with the test and the p value; otherwise *large*, *3.4 points* |
| 40 | in conclusion, / ultimately, this underscores | delete; the heading already says Conclusions, and the sentence should carry the decision |

Structural tell to check alongside the lexical ones: the four-beat LLM paragraph, built from a world-state opening, a symmetrical expansion, a hedged concession and a forward-looking resolution **[S]**. A paper whose paragraphs all follow that arc reads as generated even when every individual phrase above has been removed.

---

# PART D — The house rule for numbers

## D.1 Four checks on every published percentage

Every percentage that appears in the manuscript, in the book, in a figure caption, in the abstract or in a highlight has been checked on four axes before it is written. The check is the author's; what reaches the page is the number with its provenance.

1. **Sample**: what n produced it, and how the units were selected.
2. **Period**: the window it covers, with start and end dates.
3. **Method**: the instrument, its version, and the rule that turned raw output into a count.
4. **Denominator**: what the percentage is a percentage *of*.

The denominator is the check that catches the most damage. Without it, a 300% increase can mean three clients. Small bases are reported in units, not in percent: *3 of 12 engines*, never *25% of engines*.

In the text, source and date appear once, at the first number of the paragraph, and subsequent numbers inherit. A percentage whose denominator is not recoverable from the sentence, the sentence before it or the table it points at does not ship (C.1.13).

For this manuscript specifically, the instrument version belongs in the method axis: a citation rate measured under a pinned model panel is not the same measurement as one taken after a vendor deprecates a model mid-window, and the field record in §5 exists precisely to show what that substitution does to the number.

## D.2 No claim of absence without a measurement

No statement that something is missing, absent, unmentioned or not cited is made unless the absence was measured. The measurement, not the impression, is what gets written.

- Fails: *the literature does not address abstention*.
- Passes: *a search of Scopus and the ACL Anthology on 12/03/2026 for `abstention AND (generative OR retrieval)` returned 31 records, none of which reports a refusal rate for non-existent entities*.
- Fails: *no engine cited the entity*.
- Passes: *across 1,440 responses in the window, the entity appeared in zero, and the missingness ledger records the 96 queries that returned an error and were therefore not evaluable*.

The second half of each pair is longer and is the only one that survives a reviewer. The missingness ledger the outline plans in §3.6 is the mechanism that makes this rule enforceable rather than aspirational: an absence that the ledger cannot account for is an untested claim, and it is cut.

---

# Sources and verification log

All entries verified on **11 September 2026** unless stated otherwise.

**Primary sources, journal guides (fetched in full):**
- Information Processing & Management, Guide for authors: `https://www.sciencedirect.com/journal/information-processing-and-management/publish/guide-for-authors`
- Information Sciences, Guide for authors: `https://www.sciencedirect.com/journal/information-sciences/publish/guide-for-authors`

**Primary sources, Elsevier policy pages:**
- Generative AI policies for journals: `https://www.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals`
- CRediT author statement: `https://www.elsevier.com/researcher/author/policies-and-guidelines/credit-author-statement`
- Publishing ethics (multiple, redundant or concurrent publication): `https://www.elsevier.com/about/policies-and-standards/publishing-ethics`
- Article sharing policy (preprints, CC BY-NC-ND, DOI linking): `https://www.elsevier.com/about/policies-and-standards/sharing`
- Plagiarism detection (Crossref Similarity Check): `https://www.elsevier.com/editor/perk/plagiarism-complaints/plagiarism-detection`
- Reference style examples: `https://www.elsevier.support/publishing/answer/how-should-i-prepare-the-references-in-my-manuscript`
- Returned HTTP 404 on 11/09/2026: `https://www.elsevier.com/researcher/author/policies-and-guidelines/declaration-of-interest` and `.../research-data`

**Secondary sources, published reference style:**
- `https://raw.githubusercontent.com/citation-style-language/styles/master/dependent/information-sciences.csl` (numeric, parent `elsevier-with-titles`)
- `https://endnote.com/downloads/styles/information-sciences/` (Non-superscripted Number, Appearance-Order)
- `https://endnote.com/downloads/styles/information-processing-and-management/` (Author-Year, Author-Year-Title)
- `https://paperpile.com/s/information-processing-and-management-citation-style/` (name and year in parentheses)
- SSRN as Elsevier's preprint server: `https://www.elsevier.support/ssrn/answer/ssrn-elseviers-preprint-server`

**Secondary sources, desk rejection and AI-tell evidence** (Perplexity sonar-pro runs on 11/09/2026, raw answers retained in the session scratchpad under `r4/`):
- Desk-reject causes and the ~67% IP&M figure attributed to a co-editor presentation.
- Kobak et al., arXiv:2406.07016; *Lexical Traces of AI*, Wiley 2026; Juzek and Ward 2025; Inside Higher Ed, *Anatomy of an AI Essay*, 2024.

**Primary source, book publisher:**
- Eliva Press SRL, *Formatting Recommendations*, updated 04/09/2020, registration number 1020600000328, `www.elivapress.com`.
- Editor instruction by email, 09/09/2026: Times New Roman 16 pt, line spacing 1.5. Prevails over the published guide's "Font size 14".

**Primary source, house style ruler:**
- `C:/Sandyboxclaude/Escrita-Empresarial`: README.md, DIRETRIZ.md, MANUAL.md, exemplos/bom.md, exemplos/ruim.md, escrita/lexicos.py. Read 11/09/2026.

## Open items, listed so they are not mistaken for settled

| Item | Status | What was found |
|---|---|---|
| IP&M reference style | **[NAO CONFIRMADA]** in the guide | No reference-format block in the page as served on 11/09/2026; style repositories agree on author-year |
| IP&M highlights | **[NAO CONFIRMADA]** as forbidden | Simply absent from the guide and from its table of contents. Supplying them is harmless |
| IP&M word or page limit | **[NAO CONFIRMADA]** | None stated. The "over word count" triage item comes from an editor presentation, not the guide |
| IP&M desk-reject rate ~67% | **[NAO CONFIRMADA]** | Editor presentation reported by secondary sources. Never cite it in the manuscript |
| Crossref Similarity Check threshold | **[NAO CONFIRMADA]** | Elsevier publishes no number and warns that a high score does not by itself indicate plagiarism |
| How to declare a derived commercial book at submission | **[NAO CONFIRMADA]** | No Elsevier page prescribes a form. A.9.3 records the house sequence, marked as house position |
| Elsevier "no known competing financial interests" template sentence | **[NAO CONFIRMADA]** as publisher-published | Field standard, quoted by third parties; the requirement the guide actually states is to complete the declarations tool and select "I have nothing to declare" |
| Registered reports at IP&M | **[NAO CONFIRMADA]** | Named in the submission declaration as not counting as prior publication; no registered-report submission track described |
| Rise of the em dash and of triadic lists in LLM output | **[NAO CONFIRMADA]** | No peer-reviewed quantification found on 11/09/2026; only practitioner field guides. C.1.7 stands as house preference |
| Eliva Press 35-page minimum, portrait-only, PDF, and the portal metadata fields | Recorded as house-canonical | The published *Formatting Recommendations* confirm the margin band "From 35 to 300 Pages" but do not state the 35-page floor, the orientation rule or the portal field sizes |
