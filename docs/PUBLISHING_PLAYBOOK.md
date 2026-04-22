# Publishing Playbook — GEO Papers

Documento mestre de publicação acadêmica para a linha de pesquisa sobre Generative Engine Optimization (GEO) conduzida por Alexandre Caramaschi. Consolida canais-alvo, políticas de cross-posting, metadata canônica e playbook de submissão.

**Versão:** 1.0 (2026-04-21)
**Responsável:** Alexandre Caramaschi (ORCID 0009-0004-9150-485X)
**Primeiro paper publicado:** SSRN DOI [10.2139/ssrn.6460680](https://doi.org/10.2139/ssrn.6460680)

---

## 1. Canais-alvo — Matriz Comparativa

### 1.1 Preprint Servers

| Canal | Escopo | Review | Tempo típico | Custo (APC) | Indexação | Exclusividade |
|-------|--------|--------|--------------|-------------|-----------|---------------|
| **SSRN** | Social sciences, business, management, IS | Editorial check (sem peer review) | 24-72 h | US$ 0 | Elsevier Scopus (paper-level, vagaroso), Google Scholar | Working paper status — permite republicar |
| **ArXiv `cs.IR`** | Information Retrieval, ML, NLP | Endorsement + moderação | 24-48 h (após endorsement) | US$ 0 | DBLP, Google Scholar, Semantic Scholar | Permite submissão simultânea a journals — checar política |
| **Zenodo** | Multidisciplinar (CERN/OpenAIRE) | Sem peer review | Instantâneo | US$ 0 | OpenAIRE, DataCite DOI, Google Scholar | Permitido — DOI imutável por versão |
| **OSF Preprints** | Multidisciplinar, open science | Sem peer review | Instantâneo | US$ 0 | Google Scholar, Crossref | Permitido — versioning nativo |
| **ResearchGate** | Auto-indexação via DOI | Sem review | Automático (via Crossref) | US$ 0 | Google Scholar (indireto) | Não é canal primário — espelho do DOI |

### 1.2 Workshops e Conferências (Tier-1 IR/IS)

| Canal | Escopo | Review | Acceptance rate | Custo | Indexação | Deadline típico |
|-------|--------|--------|------------------|-------|-----------|-----------------|
| **SIGIR** (full paper) | IR top-tier | Double-blind peer | ~20% | US$ 700-1.200 | ACM DL, DBLP, Scopus | Janeiro (main), abril (short) |
| **SIGIR workshops** (Gen-IR, LLM4Eval) | GEO, LLM retrieval | Light peer | ~40-60% | Incluído na inscrição SIGIR | ACM DL (via proceedings) | Abril-maio |
| **WWW / TheWebConf** | Web, IR, systems | Double-blind peer | ~17-20% | US$ 800-1.400 | ACM DL, DBLP, Scopus | Outubro |
| **CHIIR** | Human IR, user behavior | Single-blind peer | ~30% | US$ 500-800 | ACM DL | Outubro |
| **ECIR** | IR (europeu) | Double-blind peer | ~25% | EUR 500-800 | Springer LNCS, Scopus | Outubro |
| **CIKM** | Info & Knowledge Management | Double-blind peer | ~22% | US$ 700-1.000 | ACM DL, DBLP, Scopus | Maio |

### 1.3 Journals Q1 (peer-reviewed, Scopus/WoS)

| Journal | Publisher | Scope | JCR IF | SJR | APC (open access) | Tempo médio review |
|---------|-----------|-------|--------|-----|-------------------|---------------------|
| **Information Sciences** | Elsevier | IS, AI, ML | 8.1 | Q1 | US$ 3.650 | 4-8 meses |
| **Information Processing & Management** | Elsevier | IR, info science | 8.6 | Q1 | US$ 3.650 | 3-7 meses |
| **Journal of the Association for Information Science and Technology (JASIST)** | Wiley | Info science | 3.4 | Q1 | US$ 2.800 | 4-9 meses |
| **ACM Transactions on Information Systems (TOIS)** | ACM | IR top journal | 5.6 | Q1 | US$ 1.800 (ACM Open) | 6-12 meses |
| **Expert Systems with Applications** | Elsevier | Applied AI, IS | 8.5 | Q1 | US$ 3.600 | 3-6 meses |
| **MIS Quarterly** | AIS | IS, managerial | 7.2 | Q1 | Sem APC (assinatura) | 12-24 meses |
| **Decision Support Systems** | Elsevier | DSS, IS | 6.7 | Q1 | US$ 3.400 | 4-9 meses |

**Nota sobre APC:** Open access golden (APC) é caro. Open access green (auto-arquivamento em repositório institucional pós-embargo) e híbrido (APC opcional) são alternativas. Checar política do journal em **[Sherpa Romeo](https://v2.sherpa.ac.uk/romeo/)** antes de submeter.

### 1.4 Canais Setoriais / Trade

| Canal | Uso | Review | Observações |
|-------|-----|--------|-------------|
| **Medium / Dev.to / Hashnode** | Divulgação, não citável | Nenhum | Útil para traffic, não conta como publicação |
| **Harvard Business Review / HBR Digital** | Executive-level summary | Editorial | Alto prestígio, difícil aceite |
| **MIT Sloan Management Review** | Managerial IS research | Editorial + peer leve | Bridge entre journal e trade |
| **IEEE Spectrum** | Engenharia, tech público | Editorial | Bom para visibilidade |

---

## 2. Cross-Posting Strategy — Políticas de Exclusividade

### 2.1 Regras gerais

| Combinação | Permitido? | Observações |
|------------|-----------|-------------|
| SSRN + ArXiv | Sim | SSRN explicitamente permite. ArXiv pede disclosure em notas. |
| SSRN + Journal Q1 (pré-submissão) | Sim | Working paper status; citar SSRN DOI no manuscript. |
| ArXiv + Journal Q1 (pré-submissão) | Maioria sim | Elsevier, Springer, Wiley, ACM, IEEE permitem. Verificar com **Sherpa Romeo**. |
| Journal após aceite + ArXiv update | Sim (maioria) | Pós-print permitido após embargo (6-24 meses típico). |
| Zenodo + qualquer outro | Sim | Zenodo aceita multiple versions e DOI por versão. |
| Workshop + Journal Q1 (mesmo conteúdo) | **Não** | Journals exigem originalidade substancial. Workshop = 30-70% overlap máximo. |
| SIGIR full + Journal Q1 | Extensão permitida | Journal precisa ter ≥30% material novo (experimentos adicionais, análise extendida). |

### 2.2 Matriz de decisão para GEO papers

Para o paper atual (Algorithmic Authority, SSRN 6460680), o roadmap recomendado é:

1. **Já feito:** SSRN working paper (DOI permanente, Crossref).
2. **Próximo (30 dias):** ArXiv `cs.IR` com disclosure do SSRN DOI.
3. **Próximo (60 dias):** Zenodo snapshot versionado com dataset suplementar (se dados permitirem).
4. **Próximo (90 dias):** Submissão a workshop SIGIR/Gen-IR ou ECIR (extended abstract ou short paper).
5. **Médio prazo (6 meses):** Submissão a journal Q1 (Information Processing & Management ou JASIST) após coleta longitudinal ≥6 meses.

### 2.3 Copyright armadilhas

- **Elsevier / Springer / Wiley:** transferem copyright ao aceite (a menos que APC open access). Pós-print em repositório institucional geralmente permitido após embargo.
- **ACM:** autor retém copyright com ACM Open (APC) ou transfere com ACM Digital Library License.
- **IEEE:** transferência padrão, pós-print permitido com versão author-accepted manuscript.
- **AIS / MIS Quarterly:** autor retém com não-exclusividade; política autor-friendly.

**Regra operacional:** salvar cópia AAM (Author-Accepted Manuscript) e a **camera-ready** em `papers/archive/<year>/<venue>/` antes de assinar contracts.

---

## 3. Playbook de Submissão — Passo a Passo

### 3.1 SSRN (modelo canônico do primeiro paper)

1. Login em [papers.ssrn.com](https://papers.ssrn.com) com ORCID iD ou institucional.
2. **Submit a Paper** → escolher rede SSRN apropriada (ex.: Information Systems & eBusiness Network).
3. Campos obrigatórios:
   - Title, abstract (≤ 500 palavras), JEL codes, keywords (5-8).
   - Affiliation: **Independent AI Researcher** (primary). Adicionar Brasil GEO como secondary após indexação Elsevier completar.
   - Co-authors: inserir via email + ORCID (cada co-autor recebe invite).
4. Upload PDF (máx 15 MB) + optional datasets.
5. Abstract structure: Purpose / Design / Findings / Originality / Limitations (5 parágrafos curtos).
6. Pós-publicação: SSRN envia DOI em 24-72 h. Registrar no ORCID via Crossref auto-import.

### 3.2 ArXiv `cs.IR`

1. **Endorsement obrigatório** na primeira submissão a cada categoria. Pedir a um researcher já endorsed (idealmente com h-index > 5 em IR).
2. Preparar submission:
   - LaTeX source (preferível) ou PDF. Formato `\documentclass{article}` com `\usepackage{hyperref}`.
   - ACM Computing Classification codes em metadata.
   - Abstract em texto puro (≤ 1.920 caracteres).
3. Submit em [arxiv.org/submit](https://arxiv.org/submit).
4. Categoria primária: `cs.IR`. Secundárias úteis: `cs.CL` (NLP), `cs.LG` (ML), `cs.CY` (Computers & Society).
5. Disclose SSRN DOI em nota de rodapé do título ou em Acknowledgments.
6. Versioning: updates geram `v2`, `v3` — o DOI ArXiv permanece estável.

### 3.3 Zenodo

1. Login OAuth via ORCID em [zenodo.org](https://zenodo.org).
2. **Upload** → tipo "Publication → Preprint" ou "Dataset" (para suplementar).
3. Campos:
   - Creators com ORCID, affiliations.
   - Keywords, communities (ex.: "OpenAIRE", "Information Retrieval").
   - License: **CC-BY 4.0** (recomendado para máxima reutilização).
   - Related identifiers: adicionar SSRN DOI como `isAlternateIdentifier`.
4. DOI Zenodo gerado instantaneamente.
5. Reservar DOI antes do upload se precisar colocá-lo dentro do próprio PDF.

### 3.4 Journal Q1 (fluxo genérico)

1. **Pre-submission:**
   - Validar scope em `Aims & Scope` do journal.
   - Usar **[Journal Finder](https://journalfinder.elsevier.com/)** ou **[Wiley Journal Finder](https://journalfinder.wiley.com/)** para fit.
   - Preparar cover letter (1 página): novelty, significance, fit com journal, disclosure de preprints.
2. **Submission via Editorial Manager / ScholarOne:**
   - Manuscript em formato LaTeX (preferível) com template do journal.
   - Highlights (3-5 bullets, ≤ 85 caracteres cada).
   - Graphical abstract (opcional, mas favorece aceite em desk review).
   - Funding statement, conflict of interest, data availability statement.
   - Suggested reviewers (3-5, sem conflito — evitar co-autores últimos 5 anos).
3. **Pós-submissão:**
   - Desk review: 1-4 semanas (editor decide se envia a peers).
   - Peer review: 2-6 meses primeira rodada típica.
   - Revisão: responder ponto a ponto a cada reviewer. Rejeição com encorajamento de re-submit = major revision.
4. **Aceite:**
   - Assinar Copyright Transfer Agreement ou Open Access agreement.
   - Proofs chegam em 2-4 semanas.
   - Publicação online first com DOI Crossref em 4-8 semanas após aceite final.

### 3.5 Workshop SIGIR / ECIR

1. Site do workshop tem CFP específico. Deadlines geralmente 3-4 meses antes da conferência.
2. Submeter via EasyChair ou OpenReview (dependendo do workshop).
3. Short paper típico: 4-6 páginas ACM format, double-blind.
4. Aceite: apresentar oralmente (15-20 min) ou poster.
5. Proceedings publicados em ACM DL ou CEUR-WS (CEUR tem DOI).

---

## 4. Metadata Universal — Copy-Paste Ready

### 4.1 Identificadores pessoais

- **ORCID iD:** `0009-0004-9150-485X`
- **ORCID URL:** `https://orcid.org/0009-0004-9150-485X`
- **Wikidata Q:** `Q138755507`
- **Wikidata URL:** `https://www.wikidata.org/wiki/Q138755507`

### 4.2 Afiliações canônicas

**Primária (atual):**

> Alexandre Caramaschi, Independent AI Researcher

**Secundária (quando Brasil GEO concluir indexação Elsevier):**

> Alexandre Caramaschi, Brasil GEO, Goiânia, GO, Brazil

**Endereço postal institucional (BRGEO LTDA, após CNPJ abrir):** preencher após 2026-05.

### 4.3 Email canônico

- **Acadêmico:** `caramaschiai@caramaschiai.io`
- **Corporativo:** `alexandre@brasilgeo.ai`

### 4.4 Keywords GEO research (5-8, reusáveis)

- Generative Engine Optimization (GEO)
- Large Language Models (LLMs)
- Information Retrieval
- AI Search
- Citation Analysis
- Longitudinal Study
- Algorithmic Authority
- Content Optimization

### 4.5 JEL Classification (para SSRN / economics-adjacent)

- **M31** — Marketing
- **O33** — Technological Change: Choices and Consequences
- **L86** — Information and Internet Services; Computer Software
- **D83** — Search, Learning, Information, Knowledge

### 4.6 ACM Computing Classification (para ArXiv / ACM venues)

- **Information systems → Information retrieval → Retrieval models and ranking**
- **Computing methodologies → Artificial intelligence → Natural language processing**
- **Information systems → World Wide Web → Web searching and information discovery**

### 4.7 Funding statement padrão

> This research was conducted independently without external funding. The author declares no conflicts of interest related to the findings presented.

### 4.8 Data availability statement padrão

> All data, code, and replication materials are available in the public repository at [URL]. Raw LLM responses are archived with SHA-256 hashes for reproducibility. Queries to proprietary LLM APIs were executed between [date range] using model versions specified in the manuscript.

---

## 5. Histórico de Publicações

| # | Data | Canal | Título | DOI / URL | Status |
|---|------|-------|--------|-----------|--------|
| 1 | 2026-04 | SSRN | Algorithmic Authority: A Practitioner Framework for Generative Engine Optimization Based on a 7-Day Implementation Sprint | [10.2139/ssrn.6460680](https://doi.org/10.2139/ssrn.6460680) | Publicado |

Entradas futuras devem seguir o mesmo formato e serem adicionadas aqui no ato da publicação.

---

## 6. Checklist Pré-Submissão (universal)

- [ ] Manuscript revisado por voice_guard.py (se aplicável) — sem emojis, sem hype.
- [ ] ORCID iD em cada autor.
- [ ] Afiliação canônica.
- [ ] DOI de preprints anteriores disclosed.
- [ ] Keywords consistentes com outros papers da linha.
- [ ] Funding statement e COI.
- [ ] Data availability statement com URL pública.
- [ ] Reproducibility: seed, temperature, model version, prompt templates em apêndice.
- [ ] Referências com DOI sempre que disponível.
- [ ] Cover letter com 3 bullets: novelty, significance, fit.
- [ ] Limitação e threats to validity seção explícita.
- [ ] Ethics statement (mesmo que "no human subjects").
- [ ] Template do journal aplicado (LaTeX preferível).

---

## 7. Referências bibliográficas (suporte metodológico)

- Hevner, A. R., March, S. T., Park, J., & Ram, S. (2004). Design Science in Information Systems Research. *MIS Quarterly*, 28(1), 75-105.
- Sein, M. K., Henfridsson, O., Purao, S., Rossi, M., & Lindgren, R. (2011). Action Design Research. *MIS Quarterly*, 35(1), 37-56.
- Wieringa, R. J. (2014). *Design Science Methodology for Information Systems and Software Engineering*. Springer.
- Peffers, K., Tuunanen, T., Rothenberger, M. A., & Chatterjee, S. (2007). A Design Science Research Methodology for Information Systems Research. *Journal of Management Information Systems*, 24(3), 45-77.
