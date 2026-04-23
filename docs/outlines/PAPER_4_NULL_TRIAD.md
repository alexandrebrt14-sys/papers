# Paper 4 — Null-Triad (outline canônico)

**Status**: v2 draft em `papers/drafts/null-triad-v1.md` (8.156 palavras, 36 seções) — integração 2026 agentic-commerce literature (Liu, Cao, Mao) completada 23/04.

## Thesis

Três teses dominantes do mercado GEO brasileiro falham em ser rejeitadas com *n*=7.052 em 12 dias — mas **por três mecanismos independentes**: underpower (H1 RAG), design falho (H2 hallucination probe desligado), instrumentação assimétrica (H3 sources_json). O *Null-Triad* é a contribuição organizadora.

**Elevação de stakes (v2)**: cada null mapeia para uma classe de decisão em agentic commerce 2026 — backing-model selection (AgenticPay, Liu et al 2026), adversarial-robustness certification (SoK, Mao et al 2026), cross-agent comparability audit (Solicit-Then-Suggest, Cao & Hu 2026). Citações de LLM deixam de ser metadado e viram decisão econômica.

## Título

> **Three Ways to Fail to Conclude: A Null-Report on Large Language Model Citation Claims for Brazilian Brands (N=7,052, 12 days)**

## Hipóteses focais

| # | Claim popular | H0 | Test | Corrective design |
|---|---|---|---|---|
| **H1** | Perplexity (RAG) > parametric-only | *p*_RAG ≤ mean(*p*_param) | 2-prop z + logistic cluster-robust | n≈4.2k Perplexity (vs 1.0k atual) |
| **H2** | Hallucination é desprezível em state-of-art | *p*_fictional = 0 ∀ modelo | Wilson 95 % CI por LLM | Ativar `INCLUDE_FICTITIOUS_ENTITIES=true` |
| **H3** | Universos de citação disjuntos por LLM | Jaccard-median ≥ 0.30 | Sign test vs 0.30 | Extrair `cited_entities` do body, ignorar `sources_json` |

## Descritivos robustos (sobreviveram FDR+cluster+subsample)

- Vertical heterogeneity: χ²=384, V=0.23, fintech 90 % vs saúde 63 %
- PT vs EN: Cohen's *h*=0.136 (colapsa sob cluster-robust → nota inline)
- Gemini lead: 83.5 % vs outros ~75 %

## Timeline submissão

| Data | Marco |
|---|---|
| 2026-04-23 | Draft v1 completo ✓ |
| 2026-04-24 | OSF preregistration submetido |
| 2026-04-25 | Git tag `paper-4-dataset-closed`; SHA-256 no manuscript |
| 2026-04-28 | IA adversarial review (Opus 4.7 + Gemini 2.5 Pro + GPT-4o validator) |
| 2026-05-02 | Revisão humana final |
| 2026-05-08 | Submissão SSRN + Zenodo release |
| 2026-05-15 | Cross-post arXiv cs.IR (pending endorsement) |
| Q3/2026 | SIGIR 2027 Short Papers submission |

## Compliance (estado atual)

- [x] OSF SDA template redigido (`papers/docs/PREREGISTRATION_PAPER_4_OSF.md`)
- [x] 6 tabelas com números reais + script reprodutível (`papers/analysis/paper4_tables.py`)
- [x] 34 refs BibTeX consolidadas
- [x] Section 6.4 honesty about cluster-SE collapse em PT-EN
- [x] Incidents 1-4 disclosed explicitly no Appendix D
- [x] COI framing em Section 7.3
- [x] Honest note sobre Wave 4 exploratório → confirmatory rerun pós-OSF
- [ ] Bootstrap resample real dos 3 testes focais após tag congelar DB
- [ ] SHA-256 do `papers.db`
- [ ] Cohen's κ humano sobre 200 rows (Limitação L7, scheduled v2)
- [ ] Prompt-variation pilot (Limitação L4, scheduled v2)

## Gaps conhecidos vs critérios roadmap

- **Hinton (drift / model version)**: atendido — `model_version` gravado por row.
- **Bengio (prompt sensitivity)**: declarado como L4 limitação, scheduled v2.
- **LeCun (human validation)**: declarado como L7, scheduled v2.
- **Karpathy (stats correctness)**: atendido — BCa, cluster-robust, Mann-Kendall sensitivity.
- **Kaplan (scaling)**: declarado como L9 limitação. Paper futuro com tiers maiores.
- **Gomez (RAG vs parametric)**: é H1 central do paper.

## Venue decision rationale

**Why SSRN first**: null-result, peer-review bar alto em Q1 journals (IF>8 = desk-reject risco), autor sem endorsement cs.IR ainda. SSRN dá DOI persistente, sem peer-review, citável.

**Why arXiv cs.IR depois**: precisa endorsement de ≥2 papers em IR nos últimos 5 anos. Alexandre ainda não tem. Candidatos endorser: Berthier Ribeiro-Neto (UFMG, co-autor do Baeza-Yates), Nick Craswell (Microsoft), Jimmy Lin (Waterloo).

**Why SIGIR 2027 Short Papers**: dataset artifact + corrective design explicitado = contribution fit. 4-6 páginas + Reproducibility badge.

**Why evitar Information Sciences / ESwA**: null-result recebe desk-reject em IF>8. Deixar para Paper 3 (econometric positive result).

## Próximos passos imediatos

1. Criar git tag `paper-4-dataset-closed` no `papers/` repo
2. Computar SHA-256 do `papers.db` e inserir em Appendix E
3. Rodar `paper4_tables.py` com seed reproduzível e congelar tabelas
4. Submeter OSF preregistration
5. Iniciar review adversarial via `/api/admin/executive-digest` (Opus 4.7 + Gemini 2.5 Pro + GPT-4o)
