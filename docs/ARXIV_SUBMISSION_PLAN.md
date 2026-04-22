# ArXiv Submission Plan — cs.IR track

**Status:** Planning stage (endorsement pending)
**Created:** 2026-04-22
**Primary author:** Alexandre Caramaschi (ORCID 0009-0004-9150-485X)

---

## Why ArXiv after SSRN + Zenodo

| Aspect | SSRN | Zenodo | ArXiv |
|---|---|---|---|
| DOI persistente | ✓ `10.2139/ssrn.6460680` | ✓ `10.5281/zenodo.19687866` | ✓ `arXiv:xxxx.xxxxx` |
| Indexado em Google Scholar | Sim (lento) | Sim | Sim (rápido) |
| Indexado em Semantic Scholar | Sim | Sim | Sim |
| Indexado em DBLP | Não | Não | **Sim (único)** |
| Peer review audience | Marketing, Management | Open Science general | **CS/IR researchers** |
| Endorsement requirement | Não | Não | **Sim (first submission)** |
| Version control | Via revise | Via versioning API | **Nativo (v1, v2, ...)** |
| Categoria alvo | JEL M31/O33 | Publication/Preprint | **cs.IR** (Information Retrieval) |

**Decisão:** submeter após a primeira citação em literatura peer-reviewed (ou aguardar 6 meses + coletar signal de impacto) para justificar migração para venue CS-nativo.

---

## Endorsement strategy

ArXiv cs.IR exige endorsement por um autor ativo que publicou ≥2 papers no track nos últimos 5 anos. Candidatos elegíveis:

1. **Contato via colaboração direta**:
   - Prof. autor de working paper SIGIR 2025 sobre LLM citation (identificar via semantic scholar)
   - Membro SIG-IR brasileiro (USP, UNICAMP, UFMG) que assine GEO research
2. **Via institutional endorsement**:
   - Se Alexandre obtiver visiting researcher role em universidade com alumni IR ativos
3. **Via shared co-authorship futura**:
   - Paper 2 (GEO vs SEO) planejado como co-authored com IR researcher → endorsement pós-fato

**Critério de decisão:** submeter só quando endorsement estiver garantido. Evitar rejeição por lack-of-endorsement que marca o autor no sistema.

---

## Preparação do manuscrito para cs.IR

### Diferenças vs. versão SSRN (action research)

A versão ArXiv precisa ser **empírica-first**, não practitioner-first. Reescrever:

| Seção SSRN | Reescrita ArXiv |
|---|---|
| Intro focada em "Brasil GEO sprint" | Intro focada em "RQ: how do LLMs cite entities?" |
| Methods = "7-day implementation" | Methods = experimental protocol, cohort, queries |
| Results = ECS 20% → 80% | Results = citation rates, effect sizes, statistical tests |
| Discussion = framework 10-layer | Discussion = theoretical implications + future work |
| Contribution = practitioner framework | Contribution = empirical benchmark + ECS as measurable construct |

### Template LaTeX recomendado
- **acmart.cls** (SIGIR/CIKM template) — se alvo é workshop antes
- **article.cls** padrão — se pre-print genérico
- Usar BibLaTeX + biber para referências

### Keywords cs.IR recomendados
- H.3.3 Information Search and Retrieval
- H.3.5 Online Information Services
- I.2.7 Natural Language Processing

### ACM CCS codes
- 500 (primary): `10003317.10003338` Information systems → Retrieval models and ranking
- 300 (secondary): `10003317.10003347` Information systems → Evaluation of retrieval results

---

## Timeline sugerida

| Mês | Ação |
|---|---|
| Abril/2026 (atual) | SSRN + Zenodo publicados · planejamento |
| Mai/2026 | Coletar signal de impacto SSRN (views, downloads, early citations) |
| Jun–Jul/2026 | Working papers 1-3 chegam a dados 90 dias completos |
| Jul/2026 | Decidir endorsement route: solicitar colaboração com IR researcher |
| Ago/2026 | Rewrite manuscrito para empírica-first + adaptar ao template ArXiv |
| Set/2026 | Submeter com endorsement |

---

## Checklist pré-submissão

- [ ] Endorsement obtido (via colaboração ou institucional)
- [ ] Manuscrito reescrito empírica-first
- [ ] Template LaTeX aplicado
- [ ] Bibliografia em BibLaTeX
- [ ] Abstract estruturado (purpose/methods/findings/value) — max 300 palavras
- [ ] Keywords cs.IR + ACM CCS codes
- [ ] Related Identifiers: DOI SSRN (Is version of) + DOI Zenodo (Is identical to)
- [ ] Figure/table legendas accessíveis (alt text)
- [ ] Reproducibility supplement (link GitHub papers repo + snapshot DOI Zenodo)
- [ ] Author ORCID no header
- [ ] Afiliação canônica ("Independent AI Researcher · Brasil GEO")
- [ ] Declaração conflito de interesses (nenhum declarado; CEO Brasil GEO é declared affiliation)
- [ ] Ética: "no human subjects; all data from public LLM API calls"

---

## Riscos e mitigações

| Risco | Mitigação |
|---|---|
| Rejeição por escopo (action research não encaixa cs.IR) | Empírica-first rewrite + ênfase em benchmark longitudinal |
| Endorsement não obtido | Começar por venue SIGIR workshop (não exige endorsement) |
| Duplicação percebida com SSRN | Sempre citar SSRN como "early version" + Zenodo como "archival snapshot" |
| Copyright conflict (SSRN reserva rights?) | SSRN permite cross-post como working paper; validar em "Publisher policies" do paper antes de submeter |

---

## Referências ArXiv policy

- [arXiv submission guidelines](https://info.arxiv.org/help/submit.html) — check current version
- [cs.IR category description](https://info.arxiv.org/help/arxiv_identifier.html) — IR-specific guidance
- [ArXiv endorsement policy](https://info.arxiv.org/help/endorsement.html) — 2+ papers in 5 years
- [ArXiv Open Access](https://info.arxiv.org/help/license/index.html) — CC BY / CC BY-SA / CC-0 options

---

## Next steps após aceitação

1. Adicionar arXiv ID nas sameAs do Person JSON-LD global
2. Atualizar ORCID · SSRN · Semantic Scholar · Wikidata (P818 arXiv id) com identifier
3. Footer alexandrecaramaschi.com ganha link ArXiv
4. LinkedIn post + Substack + Medium article referenciando os 3 DOIs (SSRN + Zenodo + ArXiv)
