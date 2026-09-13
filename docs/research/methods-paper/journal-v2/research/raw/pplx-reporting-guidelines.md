A range of reporting guidelines and documentation frameworks from medicine, computer science, and AI ethics can be used or adapted for empirical audits of algorithmic systems and language models. Below is a structured overview of the ones you asked for, followed by an explicit assessment of which would apply to your proposed longitudinal observational study of commercial LLM APIs and what each would typically require beyond what such studies usually report.

---

## 1. STROBE and extensions for observational studies

**Full name and maintaining group**

- **STROBE**: *Strengthening the Reporting of Observational Studies in Epidemiology*  
  Maintained by the **STROBE Initiative**, an international group of epidemiologists, statisticians, and methodologists, with resources hosted via the STROBE website and the EQUATOR Network.[1][15]

**Core requirements**

STROBE is a 22‑item checklist for cohort, case‑control, and cross‑sectional studies covering:[2][11][15]

- Title/abstract: Indicate study design; provide informative abstract.
- Introduction: Scientific background and objectives.
- Methods:
  - Study design and setting.
  - Participants: eligibility criteria, sources, methods of selection, follow‑up.
  - Variables: explicit definition of exposures, outcomes, confounders.
  - Data sources/measurement: how variables were measured or obtained.
  - Bias: efforts to address sources of bias.
  - Study size: rationale for sample size.
  - Statistical methods: handling of missing data, subgroup analyses, confounding.
- Results:
  - Participant flow: numbers at each stage, reasons for non‑participation.
  - Descriptive data: characteristics of participants, distributions of exposures.
  - Outcome data and main results: effect estimates with precision, adjusted and unadjusted.
- Discussion:
  - Limitations, including potential bias.
  - Interpretation in light of results and external evidence.
  - Generalisability.
- Other: funding and role of funders.

**Extensions relevant to algorithmic audits**

While STROBE was developed for epidemiology, several extensions (e.g., for routinely collected data, infectious disease modelling, etc.) emphasize issues like data provenance, measurement error, and time‑varying exposures, which are analogous to challenges in LLM/API audits.[6][9][15]

**Stable URL / DOI**

- Website: strobe‑statement.org[1][15]  
- Original statement (e.g. Lancet version): doi:10.1016/S0140‑6736(07)61602‑X[11]  
- J Clin Epidemiol version: doi:10.1016/j.jclinepi.2007.11.008[2]

---

## 2. PRISMA 2020 for systematic reviews

**Full name and maintaining group**

- **PRISMA 2020**: *Preferred Reporting Items for Systematic Reviews and Meta‑Analyses 2020 statement*  
  Maintained by the **PRISMA group**, with materials on the PRISMA website and EQUATOR.[5][12]

**Core requirements**

PRISMA 2020 is a 27‑item checklist plus a flow diagram for transparent reporting of systematic reviews and meta‑analyses.[5][7][8][12] It requires:

- Protocol and registration: pre‑specified objectives, eligibility criteria, and methods.
- Information sources and search strategy: detailed search strings, databases, dates.
- Study selection process: screening and inclusion/exclusion procedures.
- Data collection and items: what was extracted, how, and by whom.
- Risk of bias assessment in included studies.
- Synthesis methods: meta‑analytic models, measures of effect, heterogeneity.
- Reporting of results including effect sizes, confidence intervals, and certainty of evidence.

**Stable URL / DOI**

- Statement: BMJ 2021;372:n71, doi:10.1136/bmj.n71[5][12]  
- Explanation and elaboration: BMJ 2021;372:n160, doi:10.1136/bmj.n160[7][8]

---

## 3. CONSORT‑AI and SPIRIT‑AI

**Full names and maintaining group**

- **CONSORT‑AI**: *Consolidated Standards of Reporting Trials – Artificial Intelligence extension*  
- **SPIRIT‑AI**: *Standard Protocol Items: Recommendations for Interventional Trials – Artificial Intelligence extension*  

Developed by an international consortium of clinical trialists and AI researchers; promoted by the EQUATOR Network and major medical journals.[14]

**Core requirements**

These guidelines provide standards for **clinical trials involving AI systems**.[14]

- SPIRIT‑AI: Protocol‑level requirements:
  - Description of the AI intervention, versioning, and how it will be updated.
  - Input data characteristics, training/validation datasets.
  - Integration into clinical workflow and human‑AI interaction.
  - Handling of technical failures and monitoring performance drift.
- CONSORT‑AI: Reporting requirements for completed trials:
  - Clear description of AI system, including architecture and training data.
  - Participant flow and how the AI system was used in practice.
  - Outcomes including performance of AI vs. comparator.
  - Failure modes, fairness/robustness issues, and external validity.

**Stable URL / DOI**

- Overview of SPIRIT‑AI and CONSORT‑AI standards: doi:10.1186/s13063‑020‑04951‑6[14]

---

## 4. TRIPOD+AI

**Full name and maintaining group**

- **TRIPOD+AI**: *Transparent Reporting of a multivariable prediction model for Individual Prognosis Or Diagnosis plus Artificial Intelligence*  
  Maintained by the TRIPOD steering group; extension for prediction models using regression or machine learning.[10]

**Core requirements**

TRIPOD+AI provides a checklist for studies that **develop or validate prediction models using statistical or machine‑learning methods**.[10] It requires detailed reporting on:

- Study design and data sources for model development and validation.
- Prediction target and time horizon; inclusion/exclusion criteria.
- Predictor selection and pre‑processing, including handling missing data.
- Model specification (architecture, hyperparameters, training procedures).
- Performance metrics across relevant subgroups and settings.
- Calibration, discrimination, and clinical utility.
- Transparency around overfitting, external validation, and model updating.

**Stable URL / DOI**

- BMJ 2024;385:e078378, doi:10.1136/bmj‑2023‑078378[10]

---

## 5. ACM Artifact Review and Badging Policy

**Full name and maintaining group**

- **ACM Artifact Review and Badging Policy (current version)**  
  Maintained by the **Association for Computing Machinery (ACM)**, with adoption by SIGs such as SIGIR.[31][34][39][41]

**Core requirements**

This policy defines standardized **badges** for artifacts accompanying CS papers.[31][40][41] Two tracks:

- Artifact‑quality track:
  - **Artifacts Available**: Artifacts placed on a publicly accessible, persistent archival repository with a DOI or equivalent stable identifier.[31][40]
  - **Artifacts Evaluated – Functional**: Reviewers exercised the artifact; it is documented, consistent, complete, and exercisable.[31][40]
  - **Artifacts Evaluated – Reusable** (in some venues): Documentation and structure adequate for reuse.
- Results‑outcome track:
  - **Results Reproduced/Validated**: Independent reviewers confirm that running the artifacts reproduces key results.[31][40]

Requirements emphasize:

- Clear documentation and instructions.
- Preservation via DOI‑minting repositories (e.g., Zenodo).[35][41]
- Separation between paper review and artifact review, often via an Artifact Evaluation Committee.[34][39]

**Stable URL / DOI**

- Policy page: ACM Artifact Review and Badging – Current (version 1.1, 20 August 2020).[31][41]  
- SIGIR implementation discussion: SIGIR Forum article (ACM DL): “SIGIR Initiative to Implement ACM Artifact Review and Badging”.[39]

---

## 6. ir_metadata for information retrieval experiments

**Full name and maintaining group**

While I do not have a direct citation in the retrieved material, **“ir_metadata”** typically refers to emerging conventions or tools in the IR community (especially SIGIR/SIGIR‑adjacent) for **structured metadata describing IR experiments**—for example, recording:

- Collections used (name, source, version).
- Indexing settings and pre‑processing.
- Retrieval models and parameters.
- Evaluation metrics and test topics.

In practice, the ACM SIGIR artifact badging policies and associated templates explicitly require metadata sufficient to understand and replicate IR experiments, which is conceptually aligned with “ir_metadata”.[34][39]

Given limited tool access for this turn, I cannot provide a specific DOI or canonical URL for an “ir_metadata” paper, but the closest formal structure in the retrieved data is the SIGIR artifact badging documentation and ACM policy pages.[34][31][39]

---

## 7. Model Cards

**Full name and maintaining group**

- **Model Cards for Model Reporting**  
  Proposed by Margaret Mitchell and colleagues; widely adopted by industry (e.g., Google, Meta) as a documentation standard.[32][42][45]

**Core requirements**

A **model card** is a structured document accompanying a trained ML model.[32][45] Typical sections include:[32][45]

- **Model details**: developer, version, date, type of model, license.
- **Intended use**: primary use cases, out‑of‑scope uses.
- **Factors**: relevant demographic, environmental, or technical factors affecting performance.
- **Metrics**: evaluation metrics and rationale.
- **Evaluation data**: data used for testing, its sources and demographic composition.
- **Training data**: sources, collection and curation procedures.
- **Quantitative analyses**: performance across subgroups, robustness tests.
- **Ethical considerations**: fairness, safety, and known limitations.
- **Caveats and recommendations**: known failure modes; recommended monitoring and retraining.

**Stable URL / DOI**

- ArXiv: Model Cards for Model Reporting, doi:10.48550/arXiv.1810.03993.[32]  
  (Presented at the 2019 ACM Conference on Fairness, Accountability, and Transparency.[42])

---

## 8. Datasheets for Datasets

**Full name and maintaining group**

- **Datasheets for Datasets**  
  Proposed by Timnit Gebru and colleagues; later published in *Communications of the ACM*.[33][44]

**Core requirements**

Datasheets are structured documentation for datasets, analogous to electronic component datasheets.[33][44] They require:

- **Motivation**: why the dataset was created; intended uses and non‑intended uses.
- **Composition**: types of instances, labels, demographics, sensitive attributes.
- **Collection process**: how, when, and by whom data was collected; consent.
- **Pre‑processing/cleaning/labeling**: transformations and labeling processes.
- **Uses**: how the dataset has been used; recommended and discouraged uses.
- **Distribution**: licensing, access, versioning, and maintenance plans.
- **Maintenance**: contact person or team, plan for updates and error correction.

**Stable URL / DOI**

- ArXiv version: doi:10.48550/arXiv.1803.09010.[33]  
- CACM article: *Communications of the ACM* 64(12):86–92 (2021).[44]

---

## 9. Data Statements for NLP

**Full name and maintaining group**

- **Data Statements for Natural Language Processing: Toward Mitigating System Bias and Enabling Better Science**  
  Proposed by Emily M. Bender and Batya Friedman.[36][43]

**Core requirements**

A **data statement** is a structured description accompanying NLP datasets and corpora.[36][43] It typically includes:

- **Language and linguistic variety**: including dialect, register, and script.
- **Speaker characteristics**: demographics and sociolinguistic background.
- **Annotator characteristics**: who labeled data and under what conditions.
- **Collection process**: source, context, and communicative setting.
- **Text characteristics**: genre, topic, length, modality.
- **Pre‑processing and annotation**: tokenization, normalization, labeling schemes.
- **Known biases and limitations**: coverage gaps, representativeness issues.

Designed to support careful reasoning about generalization and bias in NLP systems.[36][43]

**Stable URL / DOI**

- Transactions of the Association for Computational Linguistics 6:587–604, doi:10.1162/tacl_a_00041.[36]

---

## 10. Evaluation Cards (for ML/LLMs)

“Evaluation cards” are more recent and less standardized than model cards or datas

## Fontes
- https://www.strobe-statement.org/
- https://pubmed.ncbi.nlm.nih.gov/18313558/
- https://pubmed.ncbi.nlm.nih.gov/25046131/
- https://pubmed.ncbi.nlm.nih.gov/18038077/
- https://www.bmj.com/content/372/bmj.n71
- https://pubmed.ncbi.nlm.nih.gov/33825815/
- https://www.bmj.com/content/372/bmj.n160
- https://www.sciencedirect.com/science/article/pii/S1743919121000406
- https://jamanetwork.com/journals/jamasurgery/fullarticle/2778474
- https://www.bmj.com/content/385/bmj-2023-078378
- https://pubmed.ncbi.nlm.nih.gov/18064739/
- https://www.prisma-statement.org/prisma-2020-statement
- https://www.sciencedirect.com/science/article/pii/S174391911400212X
- https://pubmed.ncbi.nlm.nih.gov/33407780/
- https://www.equator-network.org/reporting-guidelines/strobe/
- https://arxiv.org/pdf/2302.04556
- https://eticasfoundation.org/wp-content/uploads/2024/04/ETICAS-Adversarial-Algorithmic-Auditing-Guide-2023.pdf
- https://arxiv.org/html/2409.13210v1
- https://www.wik.org/fileadmin/user_upload/Unternehmen/Veroeffentlichungen/Working_Papers/2025/WIK-Working_paper_No12.pdf
- https://openreview.net/forum?id=0vMLqSdsKW
- https://dl.acm.org/doi/10.1109/INFOCOM.2019.8737486
- https://en.panoptykon.org/sites/default/files/2023-09/Panoptykon_ICCL_PvsBT_Fixing-recommender-systems_Aug%202023_rev.pdf
- https://www.interface-eu.org/publications/auditing-recommender-systems-overview-existing-audits-risk-assessments-and-studies
- https://arxiv.org/html/2609.06964v1
- https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- https://www.lamsade.dauphine.fr/fileadmin/mediatheque/lamsade/documents/Rapport_HCERES/portfolio/pole3/1_Paper_AAAI_22.pdf
- https://kgi.georgetown.edu/research-and-commentary/dsa-ambiguity-to-accountability/
- https://www.themoonlight.io/en/review/a-unified-causal-framework-for-auditing-recommender-systems-for-ethical-concerns
- https://mmoww.net/ai/audit/auditing-recommendation-systems/
- https://dsa-observatory.eu/2025/06/11/shortcomings-of-the-first-dsa-audits-and-how-to-do-better/
- https://www.acm.org/publications/policies/artifact-review-and-badging-current
- https://arxiv.org/abs/1810.03993
- https://arxiv.org/abs/1803.09010
- https://sigir.org/general-information/acm-sigir-artifact-badging/
- https://icpe2024.spec.org/tracks-and-submissions/artifact-evaluation-track/
- https://www.morgan-klaus.com/readings/data-statements-for-nlp.html
- https://ctuning.org/ae/reviewing-20171101.html
- https://ctuning.org/ae/reviewing-20170414.html
- https://dl.acm.org/doi/10.1145/3274784.3274786
- https://casrai.org/dictionary/term/acm-artifact-review-and-badging
- https://www.acm.org/publications/artifacts
- https://www.centerconsulting.com/ai-library/facts/model-cards-introduced-2019
- https://www.semanticscholar.org/paper/Data-Statements-for-Natural-Language-Processing:-Bender-Friedman/97bfa89addc6e5d76361e4c1e296949cad887b86
- https://ar5iv.labs.arxiv.org/html/2207.02848
- https://arxiv.org/pdf/2307.11525