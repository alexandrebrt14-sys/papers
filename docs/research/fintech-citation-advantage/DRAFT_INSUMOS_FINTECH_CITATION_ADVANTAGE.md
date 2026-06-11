# Documento de insumos — "Anchor-Entity Concentration in LLM Brand Citations"

> Insumo definitivo para o artigo peer-reviewed do projeto Papers
> (github.com/alexandrebrt14-sys/papers). Não é o artigo: é a base de escrita,
> verificada e brutalmente honesta, da qual o manuscrito será derivado.

---

## 0. Cabeçalho do documento

**Propósito.** Consolidar, em um único documento autocontido, todo o material de
pesquisa produzido sobre a "vantagem de citação da fintech" para servir de base de
redação de um artigo científico submissível a periódico/conferência A1. O documento
fixa: (i) os números oficiais verificados, (ii) o pivô da tese ocorrido durante a
investigação, (iii) os mecanismos explicativos, (iv) o posicionamento na literatura,
(v) o plano estatístico final, (vi) os bloqueadores de submissão e (vii) o roadmap
executável. Onde as fontes divergem, **os números verificados do `papers.db` vencem**;
as ressalvas dos especialistas são preservadas integralmente.

**Data de consolidação.** 11 de junho de 2026 (editor científico chefe).

**Fontes deste documento.**
- Banco: `papers.db` (SQLite), 62.820 observações brutas, janela confirmatória v2.
- Análise quantitativa: `analysis_quant.md` (números oficiais do `papers.db`).
- Seção estatística: `secao_estatistica.md` (estatístico — leave-one-out de Nubank,
  modelos logísticos, OR, Mantel-Haenszel, Breslow-Day, normalização por roster).
- Mecanismos: `mecanismos.md` (teórico — taxonomia causal em três camadas).
- Literatura: `literatura.md` (8 correntes, referências verificadas e [A VERIFICAR]).
- Red team: `red_team.md` (revisor metodologista hostil, A1 — objeções e bloqueadores).
- Board de 5 LLMs externos: `wave_1.log` a `wave_5.log` (hipóteses, teoria, plano
  estatístico, red team, estrutura IMRaD). Ver nota de aproveitamento abaixo.
- Scripts reprodutíveis: `_run_stats.py`, `_run_stats2.py`, `extract_analysis.py`,
  `run_waves.sh` (mesmo diretório).

**Status do dataset.** Janela confirmatória **v2**, em **dia 50 de 90** (coleta de
23/04/2026 a 09/06/2026; encerramento previsto ~21/07/2026). Extração NER **v2**
(`cited_v2`). Amostra-núcleo (`is_probe=0 AND is_calibration=0 AND
extraction_version='v2'`) = **50.453 observações**. A coleta segue ativa (2 coletas/dia
via GitHub Actions); a recuperação/reprocessamento de 11/jun está documentada nos
scripts `_run_stats.py`/`_run_stats2.py`, que leem o banco diretamente e reproduzem
todos os números aqui tabulados. **A análise é, portanto, interina.**

**Nota de aproveitamento do board (waves 1–5).** O board externo rodou em modo de 5
LLMs em paralelo. O provedor Google (Gemini) caiu em todas as ondas por circuit breaker
(HTTP 429) e o Perplexity (sonar-deep-research) retornou corpo vazio; o gpt-5.5 só
aparece com cabeçalho de custo, sem texto renderizado nos logs. As contribuições
substantivas aproveitáveis vêm de **Claude/Opus** (truncado em ~2.000 tokens em cada
onda) e de **Groq/llama-4-scout** (listas mais rasas). O sinal mais valioso do board é
**convergente e já incorporado** ao corpo analítico: o Opus, na onda 1, abriu exatamente
com "a primeira tarefa é desconfundir Nubank da vertical" e classificou o teste
leave-one-out como gate obrigatório — o mesmo veredito a que o estatístico e o red team
chegaram independentemente. Trechos de erro e respostas vazias foram ignorados conforme
instrução.

---

## 1. Sumário executivo (1 página)

**A pergunta original.** Por que a vertical fintech brasileira obtém taxa de citação
espontânea sistematicamente maior em LLMs (28,15%) do que varejo (24,94%), tecnologia
(14,50%) e saúde (13,35%)?

**O pivô da tese.** A investigação respondeu à pergunta de um modo que a desmonta como
estava formulada. A vantagem agregada de fintech **não é um efeito difuso da vertical**.
Ela é, em ordem decrescente de importância:
1. **Concentração extrema numa entidade-âncora.** Nubank responde por **49,68%** de
   todas as menções de fintech; **59,31%** das respostas com citação em fintech citam
   *exclusivamente* o Nubank. O leave-one-out de Nubank derruba a taxa de fintech de
   28,15% para **11,46%** — último lugar entre as quatro verticais — e inverte a razão
   de chances ajustada de **4,13 para 0,77**.
2. **Heterogeneidade radical por engine.** Apenas **2 de 5** engines mostram fintech
   acima de varejo (Claude e Gemini); ChatGPT, Groq e Perplexity mostram fintech
   *abaixo* de varejo. O efeito agregado da fintech é, em decomposição, quase
   inteiramente um efeito do Claude Haiku (+574 respostas citadas vs varejo) somado a um
   artefato do Gemini (+134).
3. **Parcialmente artefato de medição.** O `response_text` foi persistido **truncado em
   exatamente 200 caracteres** em 4 dos 5 engines (ChatGPT, Claude, Gemini: 100% das
   linhas com exatos 200 chars; Perplexity é a exceção). O NER mede citação na
   *abertura* da resposta (front-loading), não citação plena; os zeros do Gemini em
   varejo e saúde são, em parte, preâmbulo retórico cortado antes da marca aparecer.

**A tese pivotada (o artigo honesto e mais publicável).** *Anchor-Entity Concentration
in LLM Brand Citations*: a visibilidade setorial em LLMs é dominada por **entidades
superstar**, com forte **heterogeneidade por engine** e **lições metodológicas de
medição**. O fenômeno fintech/Nubank deixa de ser a tese e passa a ser o **caso central**
que demonstra a tese.

**Os 5 números que definem o artigo.**
1. **49,68%** — participação do Nubank nas menções de fintech (concentração de âncora).
2. **28,15% → 11,46%** — queda da taxa de fintech sob leave-one-out de Nubank (inversão
   de ranking: de 1º para último).
3. **OR 4,13 → 0,77** — inversão da razão de chances ajustada de fintech vs saúde ao
   remover o efeito Nubank.
4. **2 de 5** — engines que sustentam a direção da claim (sinal não consistente).
5. **96,9%–98,6%** — taxa de falso-positivo dos decoys fictícios (ameaça aberta à
   validade de construto da medida `cited`).

---

## 2. O dataset e a infraestrutura

> Base: `analysis_quant.md` §0; `red_team.md` blocos A, B, C; `secao_estatistica.md`
> cabeçalho e §6.1.

### 2.1 Desenho de coleta

- **Engines (5).** ChatGPT (`gpt-4o-mini-2024-07-18`), Claude (`claude-haiku-4-5`),
  Gemini (`gemini-2.5-pro`), Perplexity (`sonar`), Groq (`llama-3.3-70b`).
- **Verticais (4).** Fintech, varejo, tecnologia, saúde (mercado brasileiro).
- **Janela.** 23/04/2026 a 09/06/2026 (confirmatória v2), 2 coletas/dia via GitHub
  Actions; dia 50 de uma janela planejada de 90 dias.
- **Cohort de entidades (127).** 79 entidades BR reais + 32 âncoras internacionais + 16
  decoys fictícios. O **roster** efetivamente avaliado por vertical (entidades BR reais):
  fintech=19, varejo=15, tecnologia=15, saúde=15 (`analysis_quant.md` §11).
- **Queries.** 48 queries distintas por vertical, geradas pelos mesmos templates com
  apenas a frase-da-vertical trocada; 8 queries por `query_category` (comparativo,
  confiança, descoberta, experiência, inovação, mercado) em todas as verticais; 24
  directive / 24 exploratory em todas; PT e EN. **Nenhuma das 48 queries de qualquer
  vertical contém o nome de marca do roster (0/48)** — não há vazamento de construto pelo
  enunciado (`red_team.md` B3, achado favorável). Cada query é repetida ~293 vezes ao
  longo da janela (estrutura de clusters; ver §7).

### 2.2 Tamanhos de amostra

- **Bruto:** n=62.820, `cited_v2`=22.096 (35,2%).
- **Núcleo** (sem probes adversariais e sem itens de calibração): **n=50.453**,
  `cited_v2`=10.218 (**20,25%** taxa global).

### 2.3 NER v2, decoys e probes

- **NER v2 (`cited_v2`).** Detector de entidade nomeada que marca, por resposta, se
  alguma entidade do roster foi citada. Suporta *alias matching* (`via_alias_count_v2`)
  e *folding* (`via_fold_count_v2`).
- **Probes adversariais e calibração.** Itens fora do núcleo, usados para estressar o
  pipeline (`is_probe`, `is_calibration`).
- **Decoys fictícios.** 16 entidades inventadas no cohort; deveriam quase nunca ser
  "citadas". Servem de teste de especificidade do detector (ver §2.5 e §8).

### 2.4 LIMITAÇÃO EM DESTAQUE — truncamento de `response_text` em 200 caracteres

> `red_team.md` A1 — gravidade ALTA, FATAL. **É o bloqueador nº 1.**

A resposta inteira foi persistida **cortada em exatamente 200 caracteres** em 4 dos 5
engines. Verificação direta sobre `LENGTH(response_text)`:

| engine     | min | média | máx  | % linhas com exatamente 200 chars |
|------------|----:|------:|-----:|-----------------------------------|
| ChatGPT    | 200 |   200 |  200 | 100% (11.328/11.328)              |
| Claude     | 200 |   200 |  200 | 100% (11.194/11.194)              |
| Gemini     | 200 |   200 |  200 | 100% (10.939/10.939)              |
| Perplexity | 198 |   722 | 2502 | 0% (0/5.664)                      |

**Consequência.** O NER v2 rodou sobre o *snippet* de abertura, não sobre a resposta
completa. "Citação espontânea" mede, na verdade, **se a marca aparece nos primeiros ~200
caracteres** — isto é, *front-loading*/velocidade de menção, não propensão plena a citar.
Engines que abrem com preâmbulo retórico (Gemini: "Excelente pergunta! ...") são
penalizados artificialmente; verticais cuja marca-líder é citada cedo (fintech/Nubank)
são premiadas. Amostra real do Gemini (varejo) corta no meio de "volume de v[endas]"
antes de qualquer marca. **Não é respondível com os dados atuais** — exige re-coleta
salvando o texto íntegro e re-execução do NER. Toda taxa absoluta deve, até lá, ser lida
como artefato potencial de truncamento.

### 2.5 Reprodutibilidade e manifests

- Scripts: `_run_stats.py` e `_run_stats2.py` leem `papers.db` diretamente e imprimem
  todos os números das seções 3–7; `extract_analysis.py` gera `analysis_quant.md`;
  `run_waves.sh` orquestra o board de 5 LLMs.
- **Manifests SHA-256 [A PRODUZIR].** O checklist de reprodutibilidade exige hash
  SHA-256 do `papers.db` (na versão congelada da submissão), dos scripts de análise e do
  dump público do dataset (Zenodo/GitHub). Estes manifests **ainda não estão materializados**
  neste diretório e constam do roadmap (§10).

---

## 3. Resultados quantitativos consolidados

> Base: `analysis_quant.md` integral; `secao_estatistica.md` §2–§5, §7.
> Todos os valores derivam diretamente do `papers.db`; nenhum foi estimado.

### Tabela 3.1 — Taxa de citação espontânea por vertical (núcleo, IC95 Wilson)

| Vertical    |      n | Citadas | Taxa (%) | IC95 (%)       |
|-------------|-------:|--------:|---------:|----------------|
| Fintech     | 12.648 |   3.561 |   28,15  | 27,38 – 28,95  |
| Varejo      | 12.648 |   3.154 |   24,94  | 24,19 – 25,70  |
| Tecnologia  | 12.547 |   1.819 |   14,50  | 13,89 – 15,12  |
| Saúde       | 12.610 |   1.684 |   13,35  | 12,77 – 13,96  |
| **Total**   | 50.453 |  10.218 |   20,25  | —              |

Qui-quadrado (1 g.l.), fintech vs demais: vs varejo χ²=33,6 (p=6,8×10⁻⁹); vs tecnologia
χ²=699,6 (p<10⁻¹⁵); vs saúde χ²=840,6 (p<10⁻¹⁵). **Ressalva crítica (§7/§8):** estes
qui-quadrados tratam as observações como independentes; o n efetivo é da ordem de
clusters de query (≈240), não 50.453, de modo que os IC reais são bem mais largos.

### Tabela 3.2 — Matriz vertical × LLM (taxa %, núcleo)

| Vertical    | ChatGPT (4o-mini) | Claude (haiku-4.5) | Gemini (2.5-pro) | Groq (llama-3.3) | Perplexity (sonar) |
|-------------|------------------:|-------------------:|-----------------:|-----------------:|-------------------:|
| Fintech     | 18,1              | 51,0               | 4,9              | 8,7              | 86,5               |
| Varejo      | 22,2              | 30,7               | 0,0              | 12,0             | 92,9               |
| Tecnologia  | 20,4              | 10,4               | 0,7              | 6,0              | 54,3               |
| Saúde       | 8,0               | 10,7               | 0,0              | 6,1              | 69,8               |

n por célula ≈ 2.832 (≈1.416 para Perplexity, coletado em metade da cadência).
**Leitura:** Perplexity (RAG) satura no teto; Gemini opera no piso; o gap fintech>varejo
só existe em Claude (+20,3 pp) e Gemini (+4,9 pp, contaminado por truncamento). Em
ChatGPT (−4,1), Groq (−3,3) e Perplexity (−6,4) a fintech fica **abaixo** do varejo.

### Tabela 3.3 — Tamanhos de efeito: fintech vs cada vertical (desfecho original)

| Comparação            | RD       | IC95 RD            |   RR  |   OR  | IC95 OR       |
|-----------------------|---------:|--------------------|------:|------:|---------------|
| Fintech vs varejo     | +0,0322  | +0,0213 .. +0,0431 | 1,129 | 1,180 | 1,115 – 1,247 |
| Fintech vs tecnologia | +0,1366  | +0,1266 .. +0,1465 | 1,942 | 2,311 | 2,170 – 2,462 |
| Fintech vs saúde      | +0,1480  | +0,1382 .. +0,1578 | 2,108 | 2,543 | 2,384 – 2,711 |

### Tabela 3.4 — Modelo logístico principal (desfecho `cited_v2`), OR (IC95)

Referências: vertical = saúde; LLM = ChatGPT; categoria = comparativo. N=50.453;
pseudo-R² (McFadden)=0,339.

| Termo                       |     OR | IC95           |
|-----------------------------|-------:|----------------|
| Vertical: tecnologia        |  1,152 | 1,056 – 1,256  |
| Vertical: varejo            |  3,197 | 2,947 – 3,467  |
| **Vertical: fintech**       |  **4,127** | **3,807 – 4,474** |
| LLM: Claude (haiku-4.5)     |  1,788 | 1,669 – 1,915  |
| LLM: Gemini (2.5-pro)       |  0,061 | 0,052 – 0,072  |
| LLM: Groq (llama-3.3-70b)   |  0,400 | 0,367 – 0,437  |
| LLM: Perplexity (sonar)     | 12,122 | 11,122 – 13,213 |
| Categoria: confiança        |  0,469 | 0,428 – 0,514  |
| Categoria: descoberta       |  0,664 | 0,614 – 0,718  |
| Categoria: experiência      |  0,078 | 0,067 – 0,092  |
| Categoria: inovação         |  0,298 | 0,269 – 0,330  |
| Categoria: mercado          |  0,781 | 0,723 – 0,844  |

### Tabela 3.5 — Concentração de citações por entidade (HHI, núcleo)

| Vertical    | Entidades citadas | Menções | top3 (%) |   HHI  | Entidade-âncora (participação) |
|-------------|------------------:|--------:|---------:|-------:|--------------------------------|
| Fintech     | 20                |   7.112 |   70,9   | 0,283  | Nubank — 3.533 (**49,68%**)    |
| Varejo      | 16                |   6.793 |   69,4   | 0,202  | Mercado Livre — 2.003 (29,5%); Magazine Luiza — 1.961 |
| Saúde       | 18                |   3.788 |   61,9   | 0,154  | Hypera Pharma — 935; EMS — 834 |
| Tecnologia  | 22                |   3.772 |   43,9   | 0,110  | Totvs — 936                    |

Cauda da fintech (além do Nubank): PicPay 770, C6 Bank 737, Banco Inter 558, Bradesco
438, Mercado Pago 299, Itaú 289, PagBank 160. **A ordenação de concentração (fintech >
varejo > saúde > tecnologia) acompanha de perto a ordenação de taxa** — concentração e
citabilidade são duas faces da mesma estrutura de mercado.

### Tabela 3.6 — Leave-one-out de Nubank (a análise decisiva)

| Definição de "citada"                                | k     |   n    | Taxa (%) | IC95 Wilson (%) |
|------------------------------------------------------|------:|-------:|---------:|-----------------|
| Original (`cited_v2`)                                | 3.561 | 12.648 |   28,15  | 27,38 – 28,95   |
| **Leave-one-out** (remove respostas Nubank-only)     | 1.449 | 12.648 |   **11,46** | 10,91 – 12,02 |

Sob LOO, fintech (11,46%) cai **abaixo de saúde (13,35%), tecnologia (14,50%) e varejo
(24,94%)** — inversão completa de ranking. Modelo logístico com desfecho `cited_loo`
(mesmas referências, N=50.453, pseudo-R²=0,352): tecnologia OR=1,157; varejo OR=3,296;
**fintech OR=0,769 (IC95 0,702–0,844)**. Comparação direta LOO fintech vs varejo:
χ²=772,0 (p=6,5×10⁻¹⁷⁰) — robusta, mas no sentido **oposto** ao da leitura ingênua.

### Tabela 3.7 — Normalização por tamanho de roster

| Vertical    | Taxa (%) | Roster | Taxa/roster | Entidades/resposta | Menções/entidade |
|-------------|---------:|-------:|------------:|-------------------:|-----------------:|
| Fintech     |   28,15  |   19   |   0,01482   |       0,562        |      187,4       |
| Varejo      |   24,94  |   15   | **0,01662** |       0,537        |      210,3       |
| Tecnologia  |   14,50  |   15   |   0,00966   |       0,301        |      121,3       |
| Saúde       |   13,35  |   15   |   0,00890   |       0,300        |      112,3       |

**Já na taxa por entidade-roster, varejo (0,01662) supera fintech (0,01482).** Sob LOO e
roster de 18 entidades (sem Nubank), a taxa por entidade de fintech despenca para
**0,00636**, menos da metade de varejo. Fintech cita **mais nomes por resposta** (0,562
vs 0,300 em tecnologia/saúde) — assinatura de categoria densa, não de entidade única.

### Tabela 3.8 — Mantel-Haenszel (fintech vs varejo, estratificado por categoria)

- **OR comum de M-H (fintech vs varejo) = 1,205.**
- OR por estrato: comparativo 1,152; confiança 1,348; descoberta 1,036; experiência
  2,293; inovação 1,257; mercado 1,259.
- **Teste de Breslow-Day: χ²=25,42 (5 g.l.), p=0,0001** — as OR por estrato **não são
  homogêneas** (interação vertical×categoria). A OR de M-H carrega o efeito Nubank; sob
  LOO o sinal se inverte (§3.6).

### Tabela 3.9 — Robustez temporal (série semanal, taxa %)

| semana   | fintech | varejo | tecnologia | saúde |
|----------|--------:|-------:|-----------:|------:|
| 2026-W16 |    28,9 |   25,5 |       14,8 |  14,0 |
| 2026-W17 |    28,4 |   25,5 |       15,2 |  13,9 |
| 2026-W18 |    29,4 |   24,8 |       14,4 |  14,1 |
| 2026-W19 |    28,9 |   24,6 |       14,1 |  13,7 |
| 2026-W20 |    27,1 |   23,7 |       14,3 |  12,8 |
| 2026-W21 |    27,3 |   24,7 |       14,5 |  12,3 |
| 2026-W22 |    28,3 |   25,7 |       14,6 |  13,5 |
| 2026-W23 |    28,1 |   25,5 |       13,7 |  13,3 |

O ranking **bruto** não se inverte em nenhuma das 8 semanas; o gap fintech−saúde oscila
13,1–14,9 pp. Estável — mas estabilidade do ranking bruto não corrige o efeito Nubank
nem o truncamento.

### Quadro 3.10 — Tamanhos de efeito consolidados (IC95)

| Quantidade                                       | Estimativa | IC95              |
|--------------------------------------------------|-----------:|-------------------|
| Taxa global de citação (núcleo)                  |   20,25%   | —                 |
| RD fintech − saúde (original)                    |  +14,80 pp | +13,82 .. +15,78  |
| RD fintech − varejo (original)                   |   +3,22 pp |  +2,13 .. +4,31   |
| OR fintech vs saúde, ajustada (principal)        |    4,13    | 3,81 – 4,47       |
| **OR fintech vs saúde, ajustada (LOO)**          |  **0,77**  | **0,70 – 0,84**   |
| OR Perplexity vs ChatGPT                         |   12,12    | 11,12 – 13,21     |
| OR Gemini vs ChatGPT                             |    0,061   | 0,052 – 0,072     |
| OR pt vs en                                      |    0,61    | 0,58 – 0,65       |
| OR exploratory vs directive                      |    0,25    | 0,24 – 0,27       |
| Fração de citações fintech sole-Nubank           |   59,31%   | —                 |
| Participação do Nubank nas menções de fintech    |   49,68%   | —                 |

### 3.11 Decomposição do gap por engine (fintech − varejo)

> `red_team.md` E2. Excesso de respostas citadas fintech-menos-varejo:

| engine     | fintech citadas | varejo citadas | diferença |
|------------|----------------:|---------------:|----------:|
| Claude     |           1.443 |            869 |  **+574** |
| Gemini     |             134 |              0 |  **+134** |
| ChatGPT    |             513 |            630 |      −117 |
| Perplexity |           1.225 |          1.316 |       −91 |
| Groq       |             246 |            339 |       −93 |

A vantagem agregada da fintech vem de **+574 do Claude Haiku e +134 do Gemini** (este
contaminado por truncamento), contra três engines que apontam ao contrário. Sem
Perplexity, fintech=20,80% e o ranking se mantém — mas os 28,15% do título são inflados
pela mistura com o RAG.

---

## 4. A decomposição central: vertical vs entidade-âncora vs artefato de medição

> Esta seção é o coração do artigo pivotado. Cada linha indica qual evidência **sustenta**
> ou **enfraquece** cada componente. Base: `secao_estatistica.md` §3; `mecanismos.md` §3;
> `red_team.md` D3, E1–E3, A1.

### 4.1 Três componentes do "efeito fintech" observado

| Componente | O que afirma | Evidência que sustenta | Evidência que enfraquece | Veredito |
|---|---|---|---|---|
| **Efeito vertical** (genuíno, estrutural) | Fintech tem propriedade setorial que eleva citação | Cauda própria (PicPay 770, C6 737, Inter 558 = 2.065 menções); 0,562 entidades/resposta (≈2× tecnologia); 20 entidades citadas | Sob LOO cai para último; taxa por roster < varejo; só 2/5 engines | **Existe um efeito fino, amplificado** — não o efeito de 28% |
| **Efeito entidade-âncora** (superstar) | A vantagem é a saliência de uma única marca (Nubank) | LOO 28,15%→11,46%; OR 4,13→0,77; Nubank=49,68% das menções; 59,31% sole-Nubank | A categoria existe abaixo da âncora (cauda robusta) | **Dominante** — explica a maior parte do gap agregado |
| **Artefato de medição** | A taxa é parcialmente um efeito do pipeline | Truncamento a 200 chars (4/5 engines); zeros do Gemini por preâmbulo cortado; FPR decoys 96,9–98,6%; assimetria de alias (saúde 991 vs tecnologia 4 hits) | Perplexity (não truncado) também mostra padrão de saturação | **Material e não quantificado** — bloqueia a taxa absoluta |

### 4.2 O que cada peça de evidência sustenta — em uma frase cada

- **LOO de Nubank (28,15%→11,46%, OR 4,13→0,77):** sustenta que o "efeito vertical
  fintech" reportável é, em quase sua totalidade, saliência de uma marca-âncora.
- **Cauda própria (PicPay/C6/Inter) e 0,562 entidades/resposta:** sustenta que existe um
  efeito-vertical *fino e genuíno* abaixo da âncora — citar Nubank sozinho daria no
  máximo ~0,28 entidades/resposta; o excedente vem do reconhecimento de uma categoria
  povoada. Logo, **(ii)** na taxonomia de cenários do teórico (efeito-vertical fino
  amplificado por superstar), não (i) superstar isolada nem (iii) vertical puro.
- **Heterogeneidade por engine (2/5; +574 Claude):** sustenta que o efeito de engine
  domina o efeito de vertical; a "sistematicidade setorial" é falsa entre engines.
- **Truncamento + zeros do Gemini + FPR de decoys:** sustenta que parte do número é
  artefato; impede afirmar qualquer taxa absoluta como propriedade do mundo.

### 4.3 Reconciliação superstar — não é rival, é a estrutura observada em dois níveis

`mecanismos.md` §3.3 e a literatura de *superstar firms* (Autor et al., 2020) reconciliam
o aparente conflito: efeito-entidade e efeito-vertical **não são rivais** — são a mesma
estrutura de mercado em dois níveis de agregação. Nubank é alta porque a categoria "banco
digital BR" é semanticamente nomeável e densa em corpus; a categoria é nomeável porque
gerou uma superstar; a superstar é citável porque o treino converteu sua frequência em
probabilidade paramétrica. **Recomendação metodológica:** reportar todas as taxas com e
sem a âncora e tratar a exclusão como **decomposição informativa do componente
superstar**, não como "correção de viés". O artigo pivotado adota essa moldura como sua
contribuição teórica central.

---

## 5. Mecanismos explicativos

> Base: `mecanismos.md` integral (teórico — 3 camadas); hipóteses do board (wave_1,
> Opus/Groq). Cada mecanismo traz predição observável e teste discriminante.

A intuição organizadora é uma cadeia de produção da citação: um nome só aparece se (A)
existe massa textual sobre ele, (B) essa massa foi absorvida (paramétrica ou via RAG) e
(C) a estrutura semântica do mercado o torna a resposta canônica.

### 5.1 Camada A — OFERTA DE CORPUS (densidade/qualidade do texto-fonte PT-BR)

- **A1 — Imprensa especializada de alta cadência** (Finsiders, NeoFeed, editorias de
  finanças). Texto fresco, factual e nomeado diariamente.
- **A2 — Conteúdo de comparação e consumidor** (comparadores de cartões/contas,
  Reclame Aqui). Cada produto financeiro gera milhares de páginas que nomeiam a marca.
- **A3 — SEO agressivo nativo digital** ("o que é Pix", "conta digital") — eleva
  densidade e extraibilidade (marca no H1).
- **A4 — Documentação institucional** (Banco Central, Pix, Open Finance) — corpus
  oficial, citável, estável que ancora a entidade-categoria.

**Predições.** (P-A1) efeito máximo em Perplexity/RAG — *parcialmente refutado*: varejo
(92,9%) supera fintech (86,5%) no RAG. (P-A2) gap fintech>tecnologia também em inglês,
comprimido — *parcialmente refutado*: o gap em inglês é **maior** (20 pp vs 13 pp),
favorecendo entidade global (Nubank) sobre versão PT-cêntrica de A. (P-A3) densidade de
fontes maior em fintech sob RAG — *não testável no agregado* (`sources` 0,85–0,90 quase
invariante; métrica mistura paramétrico e RAG).
**Teste discriminante:** desagregar `sources`, freshness e autoridade de domínio das URLs
**dentro de Perplexity**, por vertical.

### 5.2 Camada B — DEMANDA/TREINO (como a oferta vira probabilidade)

- **B1 — Frequência no pré-treino → probabilidade paramétrica** (modelos sem ferramenta).
- **B2 — RLHF de finanças pessoais** recompensa nomear instituição útil ("Nubank"); em
  saúde recompensa hedging — assinatura idiossincrática por laboratório.
- **B3 — Recuperabilidade em RAG** (autoridade/schema/freshness do índice).

**Predições.** (P-B1) vantagem fintech dentro de modelos sem ferramenta — *confirmado
espetacularmente* em Claude (51,0% fintech vs 10,4% tecnologia, gap de 40 pp
paramétrico). ChatGPT quase inverte (18,1 vs 20,4), indicando assinatura idiossincrática
por laboratório (B2). (P-B2) Gemini diagnóstico: ~0% fora de fintech — política de
moderação suprime nomes, mas saliência de fintech vence o guardrail. **Ressalva
fundamental:** os zeros do Gemini estão *confundidos com o truncamento* (preâmbulo cortado
antes da marca) — não se pode atribuir só a política de treino. (P-B3) Perplexity comprime
o gap — *confirmado* (fintech 86,5 / varejo 92,9 / saúde 69,8 todos altos).
**Teste discriminante:** a variância da taxa fintech *entre modelos paramétricos* (Claude
51 vs ChatGPT 18 vs Gemini ~5 vs Groq 8,7) — assinatura de B sobre A. Modelar com termo
de interação vertical×LLM.

### 5.3 Camada C — ESTRUTURA DE MERCADO (marcas-categoria, fragmentação, YMYL)

- **C1 — Marcas-categoria** (Nubank ≈ banco digital; Pix ≈ pagamento instantâneo):
  mapeamento quase 1-para-1 → alvo de baixa entropia → **alta concentração**.
- **C2 — Fragmentação em tecnologia B2B** (consultorias/ERPs/integradores) → alta
  entropia → **baixa concentração e baixa taxa**.
- **C3 — Cautela YMYL em saúde** (Your Money or Your Life) → RLHF empurra para respostas
  genéricas/hedged → **taxa baixa apesar de entidades grandes**.

**Predições — todas confirmadas.** (P-C1) Fintech HHI=0,283 e top3=70,9% — a mais
concentrada. (P-C2) Tecnologia HHI=0,110, top3=43,9% — assinatura de fragmentação. (P-C3)
Saúde tem **0% de citações negativas e 42,6% positivas** (vs ~25% nas outras) e mais
hedging (1,0%) — assinatura YMYL pura. (P-C3 posição) Saúde mais front-loaded (T1=39,1%,
T3=26,1%); fintech quase uniforme (T1=35,5%, T3=33,8%) — nome citável em qualquer ponto,
coerente com âncora de altíssima saliência. (P-C1 densidade) 0,562 vs 0,300
entidades/resposta.
**Teste discriminante:** o contraste de sentimento (0% negativo em saúde) é assinatura
que **nem A nem B preveem sozinhas** — impressão digital do mecanismo YMYL (C). Logo C é
necessária e irredutível a A+B.

### 5.4 Quadro-síntese: qual padrão cada camada explica

| Padrão empírico | Camada A | Camada B | Camada C |
|---|---|---|---|
| Taxa fintech>varejo>tec≈saúde | parcial | parcial | **forte** |
| Gap estável em 8 semanas | sim | **sim** | sim |
| Claude 51% vs tec 10% (paramétrico) | não explica magnitude | **forte** | reforça |
| Gemini ~0% fora de fintech | não | **forte** (mas ver truncamento) | reforça |
| Perplexity comprime o gap | **forte** | parcial | parcial |
| HHI/top3 fintech mais alto | parcial | não | **forte** |
| Saúde 0% negativo, +hedging | não | parcial | **forte** |
| 0,56 vs 0,30 entidades/resp | parcial | não | **forte** |
| Gap maior em inglês que PT | contra A PT-cêntrica | neutro | **a favor** (entidade global) |

**Leitura.** Nenhuma camada isolada explica tudo. O modelo parcimonioso é uma **cadeia**:
estrutura de mercado (C) é o organizador de mais alto nível — única camada que explica
simultaneamente taxa, concentração e sentimento — operando através da oferta (A) e dos
conversores de treino/recuperação (B). O efeito Nubank não é um quarto mecanismo: é a
sombra de C1 projetada sobre A e B quando a categoria gera uma superstar.

### 5.5 Papel do Nubank — marca-categoria e superstar firm

Nubank é a manifestação observável de C1 (marca-categoria) que, sob a lente de IO
(*superstar firms*, Autor et al., 2020), arrasta a média da vertical para cima. O HHI de
0,283 é uma medida de Herfindahl aplicada à **atenção do modelo** ("share of model"
análogo ao "share of market"). O artigo pivotado promove esse conceito — **anchor entity
/ entidade-âncora** — a unidade explicativa central.

---

## 6. Posicionamento na literatura

> Base: `literatura.md` integral. Avisos [A VERIFICAR] preservados.

### 6.1 As 8 correntes

1. **GEO (Generative Engine Optimization) — fundação e medição.** Aggarwal et al., KDD
   2024 (arXiv:2311.09735, GEO-bench, *Cite Sources*/*Quotation*/*Statistics*); AutoGEO,
   ICLR 2026 (2510.11438); *What Gets Cited* (Vishwakarma et al., 2026, 2605.25517 — **ID
   confirmado**, 252 mil trials); Chen-Koudas (2509.08919, viés por *earned media*);
   EcoGEO (2605.12887 — **ID confirmado**, ecossistema de evidências); AgenticGEO
   (2603.20213). Medimos a mesma visibilidade, mas como **fenômeno observacional por
   setor**, não como alavanca de otimização.
2. **Comportamento de citação de motores de busca de IA.** Yang (2025, 2507.05301 —
   referência metodológica-âncora, 366.087 citações); GEO-16 (2509.10762 — **confirmado**,
   metadados/frescor/HTML semântico predizem citação); relatórios de indústria
   (Profound/Seer — **só contexto, não peer-reviewed**).
3. **RAG vs conhecimento paramétrico.** Sun et al. (2024, 2410.00857, efeito de atalho
   para o contexto recuperado) — mecanismo por trás de Perplexity citar mais; Survey de
   domínios críticos (2405.01769); RAG fairness (2603.07368 **[A VERIFICAR]**).
4. **Viés de popularidade e saliência de entidade.** Lehmann et al. (2510.16815, EACL
   2026, "shortcut" por popularidade/ordem/coocorrência — explicação teórica direta da
   concentração em Nubank); Lichtenberg et al. (2406.01285, *contraponto*: LLM como
   recomendador tem **menos** viés de popularidade); Kamruzzaman et al. (EMNLP 2024,
   2406.13997, *Global is Good* — efeito país-de-origem **pode inflar** Nubank em prompt
   PT-BR local); 2502.01349.
5. **Auditoria de preferência de marca/cultura.** 2603.18300 (vizinho metodológico);
   2601.12374 **[A VERIFICAR]**; 2503.08750 (product bias em investimento); 2601.13749
   **[A VERIFICAR]**.
6. **Viés setorial em finanças.** 2507.20957 (finanças entre os setores de viés mais
   severo); Fin-Bias (2605.09106 **[A VERIFICAR]**); *Who Invests* (Journal of Business
   Ethics, DOI 10.1007/s10551-026-06251-6).
7. **Avaliação em mercado não-anglófono PT-BR.** ClinicalBr (2606.07853); ALBA
   (2603.26516); CLARIN-PT-LDB (2603.12872 **[A VERIFICAR]**); BRoverbs (2509.08960
   **[A VERIFICAR]**). Todos de **língua/cultura/clínica**, nenhum de **mercado**.
8. **Deriva longitudinal e estabilidade temporal.** BeliefShift (2603.23848
   **[A VERIFICAR]**); Geometry of Forgetting (2605.09195 **[A VERIFICAR]**);
   Longitudinal Monitoring (2510.01255 **[A VERIFICAR]**, conceito de *service drift*).

### 6.2 A lacuna exata

Nenhum trabalho combina simultaneamente: (i) longitudinal (~10 semanas, captura *service
drift*); (ii) multi-LLM (5 motores, RAG + paramétricos); (iii) multi-setor com teste
estatístico formal entre verticais; (iv) mercado emergente não-anglófono (Brasil, PT-BR),
medindo **entidades comerciais reais**; (v) com decoys/calibração e controle de
confounders; (vi) sobre dataset publicável. **É, ao que tudo indica, o primeiro estudo
longitudinal multi-LLM de concentração/viés setorial de citação espontânea de entidades
comerciais em mercado não-anglófono, isolando setor de motor (RAG vs paramétrico) e de
conteúdo.**

### 6.3 Tabela de posicionamento

| Trabalho | Longitudinal | Multi-LLM | Multi-setor (teste formal) | Mercado não-anglófono | Decoys/calibração | Dataset público |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Nosso (2026)** | **Sim** (~10 sem.) | **Sim** (5, RAG+param.) | **Sim** (χ², Wilson, 4 verticais) | **Sim** (Brasil, PT-BR) | **Sim** | **Sim** (62.820 obs, NER) |
| GEO — Aggarwal, KDD 2024 | Não | Parcial | Parcial (vertical=teste de prompt) | Não | Não | Sim (GEO-bench) |
| What Gets Cited — 2605.25517 | Não | **Sim** (6) | Não (pares de docs) | Não | Parcial | Parcial |
| News Source — Yang 2025 | Parcial | **Sim** (3) | Não (domínios de notícia) | Não | Não | Parcial |
| GEO-16 — 2509.10762 | Não | **Sim** (3) | Parcial | Não | Não | Parcial |
| Global is Good — EMNLP 2024 | Não | **Sim** (2) | Não (global vs local) | Parcial (país-de-origem) | Parcial | Parcial |

> **Aviso editorial:** ao pivotar a tese para "concentração de entidade-âncora", o
> posicionamento deve dar **mais peso à corrente 4** (popularidade/saliência/superstar) e
> menos à narrativa de "vantagem setorial", que o próprio dado refuta. As entradas
> [A VERIFICAR] precisam de confirmação de abstract/autoria antes da submissão.

---

## 7. Plano estatístico para a versão final

> Base: `secao_estatistica.md` §6; `red_team.md` D1, D2; wave_3 (Opus).

### 7.1 Modelo principal recomendado — GLMM logístico cluster-robusto

A unidade de observação é a resposta binária `cited`. O modelo de efeitos fixos atual
(Tabela 3.4) **trata 50.453 respostas como independentes**, o que é falso: cada uma das
48 queries por vertical é repetida ~293 vezes (2 coletas/dia × 50 dias × engines ×
idiomas). O **n efetivo ≈ 48 queries × 5 engines = ~240 clusters**, não 50 mil. Logo:

```
logit( P(cited = 1) ) =
      β0
    + β1 · I(vertical)        [ref. = saúde]
    + β2 · I(llm)             [ref. = ChatGPT]
    + β3 · I(query_category)  [ref. = comparativo]
    + β4 · I(query_lang)
    + (1 | query) + (1 | dia_de_coleta)   [interceptos aleatórios]
```

- **Estimação:** GLMM logístico com interceptos aleatórios por `query` e por
  `dia_de_coleta` (e idealmente por `engine`). Reportar OR=exp(β) com IC95 de perfil.
- **Alternativa/robustez:** erros-padrão cluster-robustos (por query e por engine) ou
  **bootstrap por cluster de query**. Sem clustering, todos os p-values são inválidos
  (`red_team.md` D1, gravidade ALTA, obrigatório).
- **Desfecho duplo obrigatório no corpo:** rodar o modelo com `cited_v2` E com `cited_loo`
  (sem Nubank-only). A inversão da OR de fintech (4,13→0,77) **deve constar do corpo, não
  de apêndice** (`secao_estatistica.md` §6.3).

### 7.2 Robustez

1. **Interação vertical×LLM** — Perplexity satura e Gemini zera; o efeito de vertical é
   modificado pelo motor. Modelos estratificados por engine são mais informativos que o
   efeito principal agregado (`secao_estatistica.md` §6.4, §8.5).
2. **Interação vertical×categoria** — justificada por Breslow-Day p=0,0001.
3. **Separar RAG de paramétrico** — nunca reportar a média conjunta como número-título
   (`red_team.md` bloqueador 4). Sem Perplexity, fintech=20,80%.
4. **Leave-one-entity-out para TODAS as verticais** — repetir o LOO para Mercado
   Livre/Magazine Luiza (varejo), Totvs (tecnologia), Hypera/EMS (saúde), para mostrar se
   a fragilidade é específica de fintech ou geral.
5. **Roster de tamanho fixo** — reamostrar rosters de 15 por bootstrap, ou modelar a taxa
   controlando por |roster|, para neutralizar o desbalanceamento 19 vs 15
   (`red_team.md` B1).
6. **Matching estrito vs alias** — reportar taxas com matching exato ao lado das com
   alias, dada a assimetria (saúde 991 alias hits vs tecnologia 4).

### 7.3 Múltiplas comparações e poder

- **Correção de múltiplas comparações** (Holm/FDR) sobre as 4×5×6=108 células testadas e
  os 3 testes par-a-par (`red_team.md` D2).
- **Poder:** com n bruto enorme, o poder para o efeito médio é trivial; o gargalo é o
  **n efetivo de clusters** (~240). A análise de poder deve ser feita no nível de cluster
  (número de queries × engines), não de observação. As reversões de ranking entre
  verticais *próximas* sob LOO (fintech vs saúde/tecnologia) é onde o poder importa e onde
  os IC ainda podem mudar até o fechamento da janela (dia 90).

---

## 8. Ameaças à validade e os 6 bloqueadores pré-submissão

> Base: `red_team.md` integral (veredito do metodologista hostil A1) +
> `secao_estatistica.md` §8.

### 8.1 Os 6 bloqueadores obrigatórios (com plano de mitigação)

**Bloqueador nº 1 — Truncamento de resposta a 200 caracteres (FATAL).**
*Problema:* 4/5 engines com `response_text` cortado em exatos 200 chars; NER mede
front-loading, não citação plena; zeros do Gemini = preâmbulo cortado.
*Mitigação:* **re-coletar salvando o texto íntegro e re-rodar o NER**; reportar como a
taxa muda. Sem isso, nada vale. É o item nº 1 do roadmap (§10). A janela v2 segue até
21/jul, dando ~6 semanas de re-coleta íntegra antes do fechamento.

**Bloqueador nº 2 — Efeito Nubank de entidade única (FATAL).**
*Problema:* sem Nubank fintech cai de 28,15% para 11,46% (último lugar); a "vantagem
vertical" está carregada por uma marca.
*Mitigação:* **já prototipada** (LOO). A reformulação da tese centra na entidade-âncora e
trata a decomposição como contribuição, não como conserto. Rodar LOO para todas as
verticais (§7.2.4).

**Bloqueador nº 3 — Ausência de consistência direcional entre engines (FATAL).**
*Problema:* só 2/5 engines (Claude, Gemini) apontam fintech>varejo; o gap é quase só
efeito do Claude Haiku (+574) e do Gemini (+134, artefato).
*Mitigação:* tornar a **heterogeneidade por engine o achado central**; reportar sinal por
engine; GLMM com interação vertical×LLM; remover/re-coletar Gemini.

**Bloqueador nº 4 — Especificidade dos decoys / FPR de 96,9–98,6%.**
*Problema:* decoys fictícios são "citados" em ~98% dos casos sob probe — especificidade
do instrumento praticamente nula; mina a validade de construto da medida `cited`.
*Mitigação:* **esclarecer urgentemente o desenho dos decoys.** Se o FPR alto é *por
design* (decoy plantado no prompt para testar obediência), não é comparável à citação
espontânea e deve ser explicado como tal; se **não** for por design, invalida o detector
e exige correção. Auditar precisão/recall do NER por vertical em amostra estratificada
revisada manualmente. **Corrigir a especificidade dos decoys é mitigação explícita.**
*Nota de conflito de fontes:* o briefing do board (waves) afirmou "FPR dos decoys baixo
(calibração ok)"; **os números verificados do `papers.db` (`analysis_quant.md` §8 e
`red_team.md` B5) vencem** — o FPR é alto (96,9–98,6%) e é uma ameaça aberta.

**Bloqueador nº 5 — Não-independência / inferência sem clustering.**
*Problema:* IC e qui-quadrados tratam ~293 repetições por query como i.i.d.; n efetivo
≈ 240 clusters; a diferença de 3,2 pp fintech-vs-varejo pode perder significância.
*Mitigação:* GLMM com efeitos aleatórios de query/engine/idioma + correção de múltiplas
comparações (§7). **Consistência direcional:** garantir que a direção do efeito é
reportada por engine e por categoria, não só na média (a claim de vantagem "sistemática"
é falsa no nível de categoria — fintech não se destaca em experiência 6,9% nem confiança
12,6%).

**Bloqueador nº 6 — Tier dos modelos / generalização.**
*Problema:* 4/5 engines são tiers econômicos (`gpt-4o-mini`, `haiku-4.5`, `sonar`,
`llama-3.3-70b`); resultados não generalizam para flagships; versão única e congelada.
*Mitigação:* **restringir explicitamente a claim a "modelos de tier econômico"**; declarar
as `model_version` exatas; adicionar (se houver orçamento) uma sonda de replicação
cross-version/cross-tier em uma amostra de queries, como teste de robustez de validade
externa.

### 8.2 Demais ameaças (gravidade média/baixa) e respostas

- **Roster 19 vs 15 (média).** Mecanicamente, mais entidades → maior chance de alguma
  aparecer nos 200 chars. Já parcialmente respondido: na taxa por entidade-roster,
  **varejo supera fintech** (§3.7). Mitigar com roster de tamanho fixo (§7.2.5).
- **Seleção das marcas não cega/não pré-registrada (média).** Risco de circularidade
  (escolher marcas citáveis e concluir que a vertical é citável). Documentar o critério
  de seleção; idealmente pré-registrar.
- **Nomes únicos vs ambíguos (média).** "Nubank"/"PicPay" são strings raras e limpas;
  "Amazon"/"Oracle"/"Google" sofrem com falsos negativos/positivos. Revisar precisão/recall
  do NER por vertical.
- **Self-report não usado (baixa).** A tabela `dual_responses` (json_cited vs
  natural_cited, self_report_match) poderia validar se a menção é genuína; não foi usada na
  análise principal. Usar como validação cruzada.
- **Sazonalidade do trimestre (baixa).** Picos de IPO/regulatório de fintech no trimestre
  poderiam inflar o corpus; discutir como limitação de validade externa temporal.
- **Causal não medido (média).** A explicação "densidade de corpus" é narrativa post-hoc:
  nenhuma medida de tamanho de corpus, share de notícias ou volume de busca foi cruzada
  com a taxa. Apresentar os mecanismos como **hipóteses com testes discriminantes**
  (§5), não como causalidade estabelecida.

### 8.3 Limitações estatísticas honestas a declarar

Não-independência (IC otimisticamente estreitos; p<10⁻¹⁵⁰ = "altamente significativo",
não precisão literal); contaminação do construto "vertical" pela entidade-âncora;
normalização de roster grosseira (assume probabilidade a priori igual, falsa dado
HHI=0,283); FPR de decoys; saturação/censura por engine (Perplexity teto, Gemini piso);
janela parcial (dia 50/90); confundimento residual de categoria (Breslow-Day p=0,0001);
validade externa restrita a 5 versões específicas em ~7 semanas.

---

## 9. Estrutura IMRaD, títulos, abstract, contribution claims e venues

> Base: wave_5 (Opus editorial) + reformulação do `red_team.md` (veredito final).

### 9.1 Estrutura IMRaD proposta

- **1. Introduction.** Citação espontânea de marcas por LLM como novo canal de
  visibilidade econômica (a "nova SEO"). Gap: falta medição sistemática, longitudinal,
  calibrada e multi-LLM em mercado não-anglófono. Pergunta inicial (vantagem fintech) e o
  pivô para **concentração de entidade-âncora**.
- **2. Related Work.** As 8 correntes (§6), com peso na corrente 4 (popularidade/superstar).
- **3. Data and Methodology.** Desenho (5 engines × 4 verticais × 48 queries pareadas ×
  PT/EN), NER v2, decoys/probes/calibração, janela longitudinal, **declaração franca do
  truncamento de 200 chars** e das `model_version` de tier econômico, manifests SHA-256.
- **4. Results.** (4.1) taxas brutas e ranking; (4.2) matriz vertical×LLM e heterogeneidade
  por engine; (4.3) concentração/HHI; (4.4) **leave-one-out de âncora (resultado central)**;
  (4.5) normalização por roster; (4.6) GLMM cluster-robusto com desfecho duplo.
- **5. Mechanisms / Discussion.** Cadeia A→B→C; superstar firms; o que cada evidência
  sustenta; testes discriminantes pendentes.
- **6. Threats to Validity.** Os 6 bloqueadores e mitigações (§8).
- **7. Conclusion.** Visibilidade setorial em LLM é dominada por entidades-âncora;
  heterogeneidade por engine; lições de medição (front-loading vs citação plena).
- **Apêndices/Artefatos.** Dataset público, código, manifests, tabelas estendidas.

### 9.2 Cinco títulos candidatos (EN)

1. **Anchor-Entity Concentration in LLM Brand Citations: The Nubank Case in an
   Emerging-Market, Multi-Engine, Longitudinal Audit**
2. Superstar Firms in the Attention of LLMs: How a Single Anchor Entity Drives an
   Apparent Sectoral Citation Advantage
3. It Is Not the Sector, It Is the Star: Decomposing Spontaneous Brand-Citation Bias
   Across Five LLMs and Four Brazilian Verticals
4. Share of Model, Not Share of Market: Engine Heterogeneity and Anchor-Entity
   Dominance in Spontaneous LLM Citations
5. Measuring What We Think We Measure: Front-Loading, Anchor Entities, and Engine
   Effects in LLM Brand-Citation Audits

### 9.3 Abstract candidato (EN, ~250 palavras) — alinhado à tese pivotada

> Spontaneous brand mentions in large language model (LLM) outputs are becoming a
> consequential channel of economic visibility, yet systematic, longitudinal, and
> calibrated measurement remains scarce, especially outside English-language markets. We
> present a 50-day audit (April–June 2026) of spontaneous brand citation across five
> economy-tier LLMs (GPT-4o-mini, Claude Haiku-4.5, Gemini-2.5-pro, Perplexity sonar, and
> Llama-3.3-70B) for four Brazilian verticals (fintech, retail, technology, healthcare),
> using 48 structurally paired prompts per vertical in Portuguese and English and
> per-entity NER over a 127-entity cohort with fictitious decoys. Naively, fintech leads
> spontaneous citation (28.2% vs 24.9%/14.5%/13.3%). We show this aggregate advantage is
> not a diffuse sectoral effect but is dominated by a single anchor entity: Nubank
> accounts for 49.7% of fintech mentions, and removing responses citing only Nubank drops
> fintech to 11.5% (last place) and inverts its adjusted odds ratio from 4.13 to 0.77.
> The effect is also engine-driven: only two of five engines place fintech above retail,
> and the aggregate gap is largely a Claude-Haiku idiosyncrasy. Citation concentration
> (Herfindahl index) tracks citation rate across verticals, consistent with a
> market-structure account in which nameable category brands behave as attentional
> superstar firms. We further document measurement threats — response truncation to 200
> characters in four engines (capturing front-loading rather than full citation) and a
> 97–99% decoy false-positive rate — and outline the recollection and clustered-inference
> protocol required for confirmatory claims. Our contribution is a reproducible framework
> and an anchor-entity account of sectoral LLM citation bias in a non-Anglophone market.

### 9.4 Contribution claims defensáveis

1. **Primeiro audit longitudinal multi-LLM de citação espontânea de entidades comerciais
   reais em mercado emergente não-anglófono**, com prompts pareados, decoys e dataset
   publicável.
2. **Decomposição entidade-âncora vs vertical:** a aparente vantagem setorial é, em quase
   sua totalidade, concentração numa superstar (Nubank); LOO inverte o ranking e a OR
   ajustada. Conceito de **anchor entity / share of model**.
3. **Heterogeneidade por engine como achado de primeira ordem:** o efeito de motor (RAG
   vs paramétrico; idiossincrasia por laboratório) domina o efeito de setor; só 2/5
   engines sustentam a direção ingênua.
4. **Lições metodológicas de medição:** front-loading vs citação plena (truncamento),
   assimetria de alias por vertical e FPR de decoys — um *checklist* de validade de
   construto para auditorias de citação em LLM.

### 9.5 Venues ranqueadas

1. **ICWSM** (AAAI Conf. on Web and Social Media) — fit alto: audit observacional, viés
   de plataforma, dataset social-econômico, tolera achado "negativo/desmistificador".
2. **The Web Conference (WWW)** — fit alto: medição de viés em sistemas web/IA, trilha de
   *measurement*.
3. **Information Sciences / ACM TOIS** — fit médio-alto: rigor de IR e dataset público;
   exige o GLMM e a re-coleta resolvidos.
4. **EMNLP/ACL Findings** — fit médio: enquadrar como NER/medição e viés de modelo; a
   dimensão de mercado/longitudinal é diferencial, mas menos central para a venue.

> O veredito do red team é claro: a versão "vantagem setorial sistemática de fintech" não
> passa por revisão A1; a versão "concentração de entidade-âncora + heterogeneidade por
> engine + lições de medição" é defensável **após** resolver os 6 bloqueadores.

---

## 10. Roadmap executável (até o fechamento da janela v2, ~21/jul/2026)

Aproveitando que restam ~6 semanas de coleta v2:

**Semana 1 (crítica) — destravar a medição.**
- [ ] **Re-coletar salvando `response_text` íntegro** (remover o corte de 200 chars no
  pipeline de persistência) e re-rodar o NER v2. Bloqueador nº 1. Validar com query de
  `LENGTH(response_text)` que todos os engines passam a ter máx > 200.
- [ ] **Auditar/explicar o FPR de 98% dos decoys.** Determinar se é por design (decoy
  plantado no prompt) ou bug do detector; documentar e, se bug, corrigir a especificidade.
- [ ] **Decisão sobre Gemini:** remover da análise principal ou re-coletar (os zeros são
  artefato de truncamento + preâmbulo).

**Semana 2 — inferência correta.**
- [ ] Implementar o **GLMM logístico** com interceptos aleatórios (query, dia, engine) e
  desfecho duplo (`cited_v2` e `cited_loo`); reportar OR com IC robustos.
- [ ] Correção de múltiplas comparações (Holm/FDR) sobre 108 células + par-a-par.
- [ ] Bootstrap por cluster de query como robustez.

**Semana 3 — robustez de decomposição.**
- [ ] **Leave-one-entity-out para as 4 verticais** (Nubank; Mercado Livre/Magalu; Totvs;
  Hypera/EMS) — testar se a fragilidade é geral ou específica de fintech.
- [ ] Roster de tamanho fixo (15) por bootstrap; modelo controlando por |roster|.
- [ ] Matching estrito vs alias lado a lado; precisão/recall do NER por vertical em amostra
  estratificada revisada manualmente.

**Semana 4 — mecanismos discriminantes.**
- [ ] Desagregar `sources`/freshness/autoridade de domínio **dentro de Perplexity** por
  vertical (testa A vs B3).
- [ ] Modelo com interação vertical×LLM e vertical×categoria; quantificar fração de
  variância da interação com o laboratório.
- [ ] Contraste de sentimento condicional à citação, controlando categoria e engine
  (testa C3/YMYL).

**Semana 5 — literatura e artefatos.**
- [ ] Confirmar abstract/autoria de todas as entradas [A VERIFICAR] (correntes 3, 5, 6,
  7, 8).
- [ ] Produzir **manifests SHA-256** do `papers.db` congelado, scripts e dump público;
  preparar release Zenodo/GitHub.

**Semana 6 — escrita e fechamento.**
- [ ] Fechar a janela v2 (dia 90); re-rodar todas as tabelas no dataset final.
- [ ] Redigir o manuscrito sobre este insumo; escolher título e venue (ICWSM/WWW).
- [ ] Passada final de validade: garantir que nenhuma claim afirma "vantagem setorial
  sistemática" sem a ressalva de âncora/engine.

---

## Apêndice — Inventário de insumos e reprodução

### A.1 Arquivos de insumo (diretório `docs/research/fintech-citation-advantage/`)

| Arquivo | Conteúdo | Como reproduzir |
|---|---|---|
| `analysis_quant.md` | Números oficiais do `papers.db` (62.820 obs; taxas, matriz, HHI, categorias, idioma, série semanal, decoys, covariáveis, roster) | `extract_analysis.py` lê `papers.db` e gera o markdown |
| `secao_estatistica.md` | Leave-one-out de Nubank, modelos logísticos (principal/robustez/LOO), OR/RD/RR com IC, Mantel-Haenszel, Breslow-Day, normalização de roster, especificação formal, limitações | `_run_stats.py` e `_run_stats2.py` leem `papers.db` e imprimem todos os números |
| `mecanismos.md` | Taxonomia causal em 3 camadas (A oferta / B treino / C mercado), predições, testes discriminantes, superstar firms, modelo causal em cadeia | Documento teórico (sem código); valida-se contra as tabelas de `analysis_quant.md` |
| `literatura.md` | 8 correntes, lacuna, tabela de posicionamento, referências BibTeX (confirmadas e [A VERIFICAR]) | Verificação por busca web/arXiv (10–11/jun/2026); reconfirmar [A VERIFICAR] |
| `red_team.md` | Revisor metodologista hostil A1: validade de construto/interna/externa/estatística/engine, veredito e 6 bloqueadores | Queries diretas ao núcleo `is_probe=0 AND is_calibration=0 AND extraction_version='v2'` |
| `wave_1.log`–`wave_5.log` | Board de 5 LLMs (hipóteses, teoria, plano estatístico, red team, IMRaD) | `run_waves.sh` via geo-orchestrator; Gemini caiu (429), Perplexity/gpt-5.5 sem corpo renderizado |
| `_run_stats.py`, `_run_stats2.py`, `extract_analysis.py` | Scripts de análise | Executar sobre `papers.db` (mesma versão congelada) |
| `run_waves.sh` | Orquestração do board | Requer chaves do geo-orchestrator `.env` |

### A.2 Convenções de filtro do núcleo

Núcleo = `is_probe=0 AND is_calibration=0 AND extraction_version='v2'` → n=50.453.
Bruto = 62.820. Desfecho principal `cited_v2`; desfecho de decomposição `cited_loo`
(recodifica como não-citada toda resposta de fintech cuja única entidade é Nubank).

### A.3 Conflitos de fonte resolvidos (regra: dado verificado vence)

- **FPR dos decoys.** Briefing do board: "baixo (calibração ok)". `papers.db`/`red_team.md`:
  **96,9–98,6% (alto)**. → Vence o dado verificado: é ameaça aberta (bloqueador nº 4).
- **"Vantagem sistemática da vertical fintech".** Leitura ingênua/board inicial.
  `papers.db` (LOO, por-engine): **refutada** — efeito de âncora + engine. → Tese pivotada.
- **Cohort/roster.** Briefing cita "127 entidades (79 BR + 32 âncoras + 16 decoys)";
  `analysis_quant.md` §11 fixa o **roster avaliado por vertical** (19/15/15/15). Ambos
  coexistem: 127 é o cohort total; 19/15 é o roster BR real por vertical.

---

*Fim do documento de insumos. Próximo passo: redigir o manuscrito sobre esta base, após
executar os bloqueadores da Semana 1 do roadmap (re-coleta sem truncamento, auditoria de
decoys, decisão sobre Gemini).*
