# Outlines — Papers Brasil GEO

Índice dos outlines dos três working papers do projeto `papers/`. Cada outline abaixo é um documento vivo; a coleta longitudinal ativa (08/04/2026 → 06/07/2026) alimenta os três simultaneamente, e toda referência numérica a "dados atuais" deve ser lida como **preliminar / descritiva**, não confirmatória.

Os outlines são escritos em inglês acadêmico (padrão dos papers submetidos), mas este índice, títulos de seção internos e notas operacionais seguem a regra PT-BR do repositório.

---

## Os três papers

| # | Título curto | Arquivo | Venue alvo | Janela de submissão |
|---|--------------|---------|------------|----------------------|
| 1 | Vertical Citation (90-day empirical) | [PAPER_1_VERTICAL_CITATION.md](PAPER_1_VERTICAL_CITATION.md) | arXiv `cs.IR` (moderated preprint, no APC) | julho/2026 |
| 2 | GEO vs SEO source divergence | [PAPER_2_GEO_VS_SEO.md](PAPER_2_GEO_VS_SEO.md) | SIGIR Gen-IR Workshop 2027 ou WWW 2027 Companion | janeiro–abril/2027 |
| 3 | Industry patterns — econometric | [PAPER_3_INDUSTRY_PATTERNS.md](PAPER_3_INDUSTRY_PATTERNS.md) | *Information Sciences* (Elsevier, Q1) | dezembro/2026 |

**Dataset compartilhado:** todos reusam os mesmos 69 entidades (61 reais + 8 fictícias de controle), quatro verticais (fintech, varejo, saúde, tecnologia), cinco LLMs (GPT-4o-mini, Claude Haiku 4.5, Gemini 2.5, Perplexity Sonar, Groq Llama 3.3 70B) e bateria de queries canônicas versionada em `src/config.py`.

**Infra compartilhada:** pipeline GitHub Actions 2×/dia (06:00 + 18:00 BRT), persistência SQLite (`data/papers.db`, source of truth no git) + projeção Supabase, health gate (`scripts/health_check.py`, exit 1 on underrun), dataset aberto em Zenodo (DOI emitido na submissão do Paper 1 e reutilizado nos Papers 2 e 3).

---

## Timeline consolidado

```
2026
├── ABR 08  ◉  Início da coleta longitudinal (cron 06:00/18:00 BRT)
├── ABR 21  ◉  Estado atual: ~4.148 observações, 75,8% taxa agregada (preliminary)
│
├── ABR/30  ▲  Pré-registro no OSF — hipóteses H1–H6 (Paper 1) + H1–H6 (Paper 3)
│             ▲  Congelar query battery + cohort
│             ▲  Ativar ENABLE_SERP_OVERLAP=true (destravar coleta Paper 2)
│
├── MAI/31  ▲  Consolidação tabela `entity_attributes` (Paper 3 §5.2)
│             ▲  Validação amostral Brave vs Google Programmable Search (Paper 2 §5.6)
│
├── JUN/30  ▲  Snapshot intermediário N=12 semanas — primeiras análises SERP (Paper 2)
│             ▲  BSTS / CausalImpact do GEO Score (roadmap METHODOLOGY §11)
│
├── JUL 06  ◉  Fechamento da janela de 90 dias (Paper 1)
│             ◉  Congelamento de `data/papers.db` para análise confirmatória
│             ◉  Tag git `paper-1-dataset-closed` + Zenodo DOI emitido
│
├── JUL/31  ▲  Draft 1 Paper 1 finalizado (arXiv-ready)
│             ▲  Submissão arXiv `cs.IR` → DOI imediato
│
├── AGO–SET ▲  Análise econométrica Paper 3 (mixed-effects logit + ICC)
│             ▲  Draft 1 Paper 3 (target Information Sciences)
│
├── OUT     ▲  Draft 1 Paper 2 (Jaccard + Kendall tau + Beta regression)
│
├── NOV     ▲  Voice review editorial (Alexandre voice guard) em todos os drafts
│
├── DEZ/15  ▲  Submissão Paper 3 → Information Sciences (gold OA, USD 2.700 APC)
│
2027
├── JAN     ▲  Submissão Paper 2 → WWW 2027 Companion (posters)
├── ABR     ▲  Submissão Paper 2 (fallback) → SIGIR 2027 Gen-IR Workshop
├── JUN–NOV ▲  Ciclo de revisão Paper 3 (3–6 meses a primeira decisão)
└── DEZ     ▲  Aceitação esperada Paper 3 (acceptance window 9–14 meses pós-submissão)
```

Legenda: ◉ marco de dados · ▲ marco editorial / submissão.

---

## Research questions em uma linha

### Paper 1 (5 RQs)
- **RQ1.** Diferenças de taxa de citação entre verticais, controlando por query/modelo/idioma?
- **RQ2.** Estabilidade intra-modelo de um mesmo LLM ao longo dos 90 dias?
- **RQ3.** Concordância inter-modelos (Fleiss' kappa) sobre quais entidades são citadas?
- **RQ4.** False-positive rate nas entidades fictícias por vertical e por modelo — correlaciona com hedging?
- **RQ5.** Queries diretivas vs. exploratórias produzem gaps sistemáticos de citação, e isso interage com vertical?

### Paper 2 (4 RQs)
- **RQ1.** Qual o Jaccard médio entre SERP top-10 e citações LLM, por vertical?
- **RQ2.** Há correlação de rank (Kendall τ) entre posição no SERP e posição na resposta do LLM, no conjunto interseção?
- **RQ3.** Perplexity Sonar (retrieval-augmented explícito) diverge menos do SERP que os outros 4 LLMs?
- **RQ4.** Entidades citadas pelo LLM mas ausentes do SERP top-10 compartilham atributos mensuráveis (Wikidata, Wikipedia, academic)?

### Paper 3 (4 RQs)
- **RQ1.** Vertical permanece preditor significativo depois de controlar por atributos entity-level (brand age, revenue proxy, Wikidata, etc.)?
- **RQ2.** Qual atributo entity-level tem a maior odds-ratio de citação, e o ranking é estável entre os 5 LLMs?
- **RQ3.** Registro regulatório (BC/ANS/ANVISA/CVM) prediz citação diferencialmente em verticais regulados vs. não-regulados?
- **RQ4.** Ao longo dos 90 dias, os effect sizes entity-level derivam, e o drift correlaciona com eventos públicos (launches, regulação, notícias)?

---

## Integridade cruzada entre os três outlines

- **Dataset único.** Papers 1 e 3 compartilham a mesma `data/papers.db` congelada em 06/07/2026. Paper 2 adiciona `serp_ai_overlap` (tabela já no schema, toggle off hoje).
- **Pré-registro comum.** Ambos Paper 1 (H1–H6) e Paper 3 (H1–H6) são pré-registrados no OSF em abril/2026 antes do fechamento da janela. Paper 2 pré-registra no SIGIR / WWW conforme calendário de submissão da workshop.
- **Zenodo DOI único.** Um único deposit Zenodo versiona o dataset que alimenta os três papers; o DOI é citado em todos.
- **Pipeline único.** Nenhum fork do código de coleta. Todo o pipeline em `src/collectors/*`, versionado em `alexandrebrt14-sys/papers`.
- **Voice guard.** Antes de submeter qualquer um dos três, rodar `voice_guard.py` do repositório `curso-factory` (padrão editorial Alexandre — arco HBR, credenciais canônicas, naming canônico).

---

## Checklist operacional de pré-submissão

Aplicável individualmente a cada paper antes da submissão:

- [ ] Hipóteses pré-registradas no OSF com timestamp anterior ao fechamento da coleta.
- [ ] `data/papers.db` tagueado em git no hash de fechamento (`paper-N-dataset-closed`).
- [ ] Dataset exportado e publicado no Zenodo com DOI emitido.
- [ ] Data dictionary (`docs/data_dictionary.md`) alinhado com colunas do dataset publicado.
- [ ] Análises confirmatórias separadas de exploratórias no texto do paper (sem p-values para análises post-hoc).
- [ ] BCa bootstrap reportado para toda estatística escalar primária.
- [ ] FDR aplicado à family apropriada (vertical pairwise, per-entity, per-model).
- [ ] Power analysis e N efetivo reportados em §Methods.
- [ ] Threats to validity explicitamente listadas e mitigações discutidas.
- [ ] Ethics: no-IRB statement (public data only, no human subjects) em §5.6 ou equivalente.
- [ ] Voice guard passou (naming canônico, sem emojis, acentuação completa em PT-BR quando aplicável).
- [ ] Commit final com mensagem `paper(N): submission draft vX` e tag `paper-N-submission-vX`.

---

*Última atualização deste índice: 2026-04-21.*
*Autor responsável: Alexandre Caramaschi.*
*Dependência crítica transversal: finalização do pré-registro OSF e ativação do toggle SERP antes de 30/04/2026.*
