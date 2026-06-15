# Proveniência — Wave Junho 15B 2026

Pesquisa viva cruzada de DUAS frentes independentes (15-jun-2026):

1. **Perplexity `sonar-pro`** (online, com `search_results`+`citations` reais) — 7 queries
   cirúrgicas em inglês. Arquivos `P1.json`..`P7.json` (cada um traz `content`,
   `citations` e `search_results`). Runner:
   `geo-orchestrator/scripts/research_geo_pplx_sonarpro_20260615.py`.
   - P1 Profound · P2 Ahrefs/Semrush · P3 papers · P4 KPIs · P5 produto/algoritmo ·
     P6 playbooks praticantes · P7 camada semântica/vetorial.

2. **WebSearch + WebFetch do Claude** — 3 sub-agentes paralelos (fornecedores; papers
   acadêmicos com verificação de `arxiv.org/abs/<id>`; produto/algoritmo + KPIs).
   Relatórios consolidados diretamente no doc canônico (§1–§6) com seções
   "NÃO VERIFICADO" preservadas no §8.

NOTA ANTI-GHOSTCITE: o `sonar-deep-research` (primeira tentativa) retornou
`search results = None` e chegou a inventar arXiv IDs (2603.04567, 2605.11203 etc.,
NÃO verificados) — descartado como fonte de fato. Só `sonar-pro` (busca live) e
WebFetch de fonte primária foram usados para fatos datados.
