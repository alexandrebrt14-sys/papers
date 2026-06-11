# Análise quantitativa — papers.db (62.820 obs, 2026-04-23 a 2026-06-09)

Base: janela confirmatória v2, extração NER v2 (cited_v2). Núcleo = sem probes/calibração.

## 0. Visão geral
- Bruto: n=62820, cited_v2=22096 (35.2%)
- Núcleo: n=50453, cited_v2=10218 (20.3%)

## 1. Taxa de citação por vertical (núcleo) + IC95 Wilson
- fintech: n=12648, cited=3561, rate=28.15% (IC95 27.38-28.95%)
- varejo: n=12648, cited=3154, rate=24.94% (IC95 24.19-25.70%)
- tecnologia: n=12547, cited=1819, rate=14.50% (IC95 13.89-15.12%)
- saude: n=12610, cited=1684, rate=13.35% (IC95 12.77-13.96%)

### Qui-quadrado (fintech vs outras, 1 g.l.)
- fintech vs varejo: chi2=33.6, p=6.83e-09
- fintech vs tecnologia: chi2=699.6, p=<1e-15
- fintech vs saude: chi2=840.6, p=<1e-15

## 2. Matriz vertical x LLM (rate %, núcleo)
| vertical | ChatGPT | Claude | Gemini | Groq | Perplexity |
|---|---|---|---|---|---|
| fintech | 18.1 (n=2832) | 51.0 (n=2832) | 4.9 (n=2736) | 8.7 (n=2832) | 86.5 (n=1416) |
| varejo | 22.2 (n=2832) | 30.7 (n=2832) | 0.0 (n=2736) | 12.0 (n=2832) | 92.9 (n=1416) |
| tecnologia | 20.4 (n=2832) | 10.4 (n=2736) | 0.7 (n=2731) | 6.0 (n=2832) | 54.3 (n=1416) |
| saude | 8.0 (n=2832) | 10.7 (n=2794) | 0.0 (n=2736) | 6.1 (n=2832) | 69.8 (n=1416) |

## 3. Concentração de citações por entidade (NER v2, núcleo)
- fintech: 20 entidades, 7112 menções | top3=70.9% | HHI=0.283
  top: Nubank (3533), PicPay (770), C6 Bank (737), Banco Inter (558), Bradesco (438), Mercado Pago (299), Itaú (289), PagBank (160)
- varejo: 16 entidades, 6793 menções | top3=69.4% | HHI=0.202
  top: Mercado Livre (2003), Magazine Luiza (1961), Americanas (753), Amazon Brasil (585), Amazon (574), Casas Bahia (364), Walmart (198), Shein (136)
- tecnologia: 22 entidades, 3772 menções | top3=43.9% | HHI=0.110
  top: Totvs (936), Accenture (445), Involves (274), Oracle (274), Microsoft (272), CI&T (228), Google (218), iFood (216)
- saude: 18 entidades, 3788 menções | top3=61.9% | HHI=0.154
  top: Hypera Pharma (935), EMS Pharma (834), Eurofarma (577), Pfizer (350), Novartis (302), Roche (196), Sírio-Libanês (158), Raia Drogasil (118)

## 4. Mix de query_category por vertical (confounder) e rate por categoria
- fintech | mercado: n=2344, rate=43.5%
- fintech | descoberta: n=2344, rate=40.6%
- fintech | comparativo: n=2344, rate=39.5%
- fintech | inovacao: n=1872, rate=15.9%
- fintech | experiencia: n=1872, rate=6.9%
- fintech | confianca: n=1872, rate=12.6%
- saude | descoberta: n=2344, rate=18.2%
- saude | comparativo: n=2344, rate=30.2%
- saude | mercado: n=2328, rate=17.5%
- saude | confianca: n=1872, rate=5.3%
- saude | experiencia: n=1866, rate=0.0%
- saude | inovacao: n=1856, rate=2.3%
- tecnologia | mercado: n=2328, rate=19.7%
- tecnologia | descoberta: n=2328, rate=11.5%
- tecnologia | comparativo: n=2328, rate=26.4%
- tecnologia | experiencia: n=1856, rate=0.3%
- tecnologia | confianca: n=1856, rate=22.3%
- tecnologia | inovacao: n=1851, rate=3.2%
- varejo | mercado: n=2344, rate=37.9%
- varejo | descoberta: n=2344, rate=39.8%
- varejo | comparativo: n=2344, rate=36.2%
- varejo | inovacao: n=1872, rate=13.1%
- varejo | experiencia: n=1872, rate=3.2%
- varejo | confianca: n=1872, rate=9.7%

## 5. Por idioma da query
- fintech | en: n=6324, rate=31.8%
- fintech | pt: n=6324, rate=24.5%
- saude | en: n=6304, rate=13.0%
- saude | pt: n=6306, rate=13.7%
- tecnologia | en: n=6274, rate=17.4%
- tecnologia | pt: n=6273, rate=11.6%
- varejo | en: n=6324, rate=28.2%
- varejo | pt: n=6324, rate=21.6%

## 6. Série semanal por vertical (rate %) — estabilidade do gap
| semana | fintech | varejo | tecnologia | saude |
|---|---|---|---|---|
| 2026-W16 | 28.9 | 25.5 | 14.8 | 14.0 |
| 2026-W17 | 28.4 | 25.5 | 15.2 | 13.9 |
| 2026-W18 | 29.4 | 24.8 | 14.4 | 14.1 |
| 2026-W19 | 28.9 | 24.6 | 14.1 | 13.7 |
| 2026-W20 | 27.1 | 23.7 | 14.3 | 12.8 |
| 2026-W21 | 27.3 | 24.7 | 14.5 | 12.3 |
| 2026-W22 | 28.3 | 25.7 | 14.6 | 13.5 |
| 2026-W23 | 28.1 | 25.5 | 13.7 | 13.3 |

## 7. Qualidade da citação (citation_context)
- fintech: negative=0.2%, neutral=74.4%, positive=25.4% (n=7371)
- saude: neutral=57.4%, positive=42.6% (n=3087)
- tecnologia: negative=0.0%, neutral=73.2%, positive=26.7% (n=2397)
- varejo: neutral=74.8%, positive=25.2% (n=5786)

### Tercil de posição (1=início)
- fintech: T1=35.5%, T2=30.6%, T3=33.8% (n=7371)
- saude: T1=39.1%, T2=34.8%, T3=26.1% (n=3087)
- tecnologia: T1=26.7%, T2=40.5%, T3=32.8% (n=2397)
- varejo: T1=42.0%, T2=36.2%, T3=21.8% (n=5786)

### Hedging por vertical
- fintech: hedging=0.3% (n=7371)
- saude: hedging=1.0% (n=3087)
- tecnologia: hedging=1.0% (n=2397)
- varejo: hedging=0.3% (n=5786)

## 8. Decoys fictícios — FPR por vertical (probes/calibração)
- fintech: n=3104, hits=3061, FPR=98.61%
- saude: n=3088, hits=3018, FPR=97.73%
- tecnologia: n=3071, hits=2977, FPR=96.94%
- varejo: n=3104, hits=3026, FPR=97.49%

## 9. Covariáveis por vertical (núcleo)
- fintech: resp_len=260 chars, sources=0.88, tokens=665, lat=9119ms
- saude: resp_len=261 chars, sources=0.85, tokens=646, lat=8760ms
- tecnologia: resp_len=258 chars, sources=0.90, tokens=647, lat=8942ms
- varejo: resp_len=255 chars, sources=0.89, tokens=657, lat=9017ms

## 10. Selection vs Absorption (CSR/CAR) por vertical, onde preenchido
- fintech | sel=0 ab=0: n=605
- fintech | sel=0 ab=1: n=217
- fintech | sel=1 ab=1: n=25
- fintech | sel=1 ab=0: n=17
- saude | sel=0 ab=0: n=743
- saude | sel=0 ab=1: n=92
- saude | sel=1 ab=1: n=22
- saude | sel=1 ab=0: n=7
- tecnologia | sel=0 ab=0: n=738
- tecnologia | sel=0 ab=1: n=126
- varejo | sel=0 ab=0: n=643
- varejo | sel=0 ab=1: n=217
- varejo | sel=1 ab=1: n=4

## 11. Normalização por tamanho de roster e intensidade multi-entidade
Roster v2: fintech=19 BR reais, varejo=15, saude=15, tecnologia=15.
- fintech: 3561 respostas com citação / 19 entidades no roster = 187 por entidade
- varejo: 3154 respostas com citação / 15 entidades no roster = 210 por entidade
- tecnologia: 1819 respostas com citação / 15 entidades no roster = 121 por entidade
- saude: 1684 respostas com citação / 15 entidades no roster = 112 por entidade
  - fintech: média de entidades citadas por resposta = 0.562
  - saude: média de entidades citadas por resposta = 0.300
  - tecnologia: média de entidades citadas por resposta = 0.301
  - varejo: média de entidades citadas por resposta = 0.537

## 12. Query types (núcleo) por vertical
- fintech | exploratory: n=6324, rate=20.0%
- fintech | directive: n=6324, rate=36.4%
- saude | directive: n=6307, rate=20.5%
- saude | exploratory: n=6303, rate=6.2%
- tecnologia | directive: n=6275, rate=16.7%
- tecnologia | exploratory: n=6272, rate=12.2%
- varejo | exploratory: n=6324, rate=16.3%
- varejo | directive: n=6324, rate=33.5%
