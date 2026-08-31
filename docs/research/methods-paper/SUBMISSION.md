# Pacote de submissão — SSRN (Elsevier)

Metadata e checklist do methods paper. O manuscrito está em `MANUSCRIPT.md`.

**Status:** pronto para revisão do autor. Não submetido.

---

## 1. Metadata para o formulário do SSRN

Campos na ordem em que o formulário pede. Copiar e colar.

### Title

```
Measuring Entity Citation in Generative Engines: A Longitudinal Protocol and the Observation-Window Problem
```

### Abstract

O abstract do manuscrito, sem markdown, sem quebras de parágrafo duplas. O SSRN
corta acima de 1.920 caracteres — a versão abaixo tem folga.

```
Large language models increasingly stand between consumers and the firms they might choose, yet the field that has grown around this shift - generative engine optimization (GEO) - reports citation rates without stating the conditions under which a citation was counted. This paper documents the protocol of an ongoing 90-day longitudinal study of six commercial engines across four Brazilian industry verticals, and isolates one design parameter the literature leaves implicit: the observation window, meaning how much of a model's answer the instrument reads before deciding whether an entity was cited. The parameter is not innocuous. In our own pipeline the window was set once per provider and drifted apart unnoticed: five parametric arms were measured on the first 200 characters of each answer while the single retrieval-augmented arm was measured on the entire response. Across 64,191 canonical observations the asymmetry inflated that arm's citation rate from 52.0% to 75.8% - 23.8 percentage points produced by the instrument rather than by the model. Re-measuring the five truncated arms under the same window moves none of them by a tenth of a point, which is what separates a correction from a new number. We report the full design, the extraction instrument, the missingness ledger that records every collection gap instead of imputing it, and the pre-registered analysis plan. We argue that a citation rate is not interpretable as a cross-engine comparison unless the window is declared, and that retrieval-augmented engines are the most affected, because they open with framing prose before naming anything. Dataset, code and collection logs are public.
```

### Keywords

```
generative engine optimization; large language models; entity citation; measurement validity; longitudinal design; retrieval-augmented generation
```

### JEL Classification

```
C81, C83, L86, M31
```

`C81` metodologia de coleta de dados · `C83` desenho amostral e de survey ·
`L86` serviços de informação e software · `M31` marketing.

### Author

| Campo | Valor |
|---|---|
| Nome | Alexandre Caramaschi |
| Affiliation (primary) | Independent AI Researcher |
| ORCID | 0009-0004-9150-485X |
| E-mail | o cadastrado no SSRN |

A afiliação primária segue o `PUBLISHING_PLAYBOOK.md`: Independent AI
Researcher enquanto a indexação Elsevier da Brasil GEO não conclui. O vínculo
comercial não fica omitido — está declarado na §12 do manuscrito, que é onde a
Elsevier exige que apareça.

### Rede SSRN

Information Systems & eBusiness Network (primária). Considerar também
Marketing Science eJournal como secundária, pois o objeto toca descoberta de
marca.

---

## 2. Checklist antes de submeter

### Conteúdo

- [ ] Reler o manuscrito inteiro em voz alta — releitura anti-tique.
- [ ] Conferir cada número contra o banco. Toda porcentagem precisa das quatro
      conferências: amostra, período, método, denominador.
- [ ] Abrir todo identificador citado (ORCID, URL do repositório). DOI e
      arXiv ID errados se propagam sozinhos para o depósito e para a página
      pública.
- [ ] Confirmar que nenhuma afirmação sobre ausência foi feita sem medição
      correspondente.

### Números que o manuscrito afirma

Todos reproduzíveis. Os comandos estão em `VERIFICATION.md`.

| Afirmação | Valor | Onde conferir |
|---|---|---|
| Observações canônicas | 64.191 | `SELECT COUNT(*) FROM citations WHERE is_probe=0` |
| Observações totais | 80.638 | `SELECT COUNT(*) FROM citations` |
| Dias com dado | 49 | `COUNT(DISTINCT date(timestamp))` |
| Runs abortadas | 296 | `collection_runs WHERE status='aborted'` |
| Perplexity, como coletada | 75,8% | `harmonize_citation_window.py --check --canonical-only` |
| Perplexity, janela uniforme | 52,0% | idem |
| Delta | −23,8 pp | idem |
| Demais braços, delta | +0,0 pp | idem |
| Refusals entre os "hallucinations" | 67,4% | script de amostragem em `VERIFICATION.md` |
| Coorte | 127 (111 reais + 16 decoys) | `src/config_v2.py` |
| Bateria | 192 canônicas + 64 probes | idem |

### Formato

- [ ] Exportar para PDF. O SSRN aceita PDF e DOCX; PDF preserva as tabelas.
- [ ] Página de rosto com título, autor, afiliação, ORCID e data.
- [ ] Sem cabeçalho ou rodapé com marca comercial.
- [ ] Numeração de página.

### Governança

- [ ] Declaration of competing interest conferida com
      `feedback_credencial_tres_chapeus_alexandre`. O texto atual declara o
      chapéu (Founder da Brasil GEO), o cargo na Nuvini e o conflito comercial.
- [ ] Nenhum uso de "Especialista #1", "Source Rank", "geobrasil.com.br",
      "sourcerank.ai" ou dos cargos obsoletos.
- [ ] Repositório público e navegável no momento da submissão — o manuscrito
      aponta para ele como fonte dos dados.

### Depois de submeter

- [ ] SSRN devolve o DOI em 24-72 h.
- [ ] Registrar o DOI no ORCID via auto-import Crossref.
- [ ] Adicionar a linha ao histórico de publicações do `PUBLISHING_PLAYBOOK.md`.
- [ ] Referenciar o DOI nos papers 1 e 3, que passam a citar este protocolo em
      vez de repetir a metodologia.

---

## 3. O que este paper deliberadamente não faz

Registrado para que a decisão fique explícita e não pareça omissão.

**Não reporta resultados confirmatórios.** A janela de 90 dias fecha em
28/09/2026. Publicar o protocolo antes é o que dá valor ao pré-registro: o
plano de análise entra no registro público antes das estimativas que ele vai
produzir.

**Não compara com estudos de terceiros.** A tese central é que taxas de citação
publicadas sem janela declarada não são comparáveis. Compará-las aqui
contradiria o argumento. O paper mostra o efeito no próprio dado, onde as duas
medidas existem sob condições controladas.

**Não afirma que a janela de 200 caracteres é a escolha certa.** Afirma que é
uma escolha, que precisa ser declarada, e que a nossa é reportada com
sensibilidade nas duas direções.

---

## 4. Relação com os outros papers da linha

| # | Paper | Venue | O que passa a herdar daqui |
|---|---|---|---|
| 1 | Vertical citation, 90 dias | arXiv `cs.IR` | metodologia inteira por referência |
| 2 | GEO vs SEO, divergência de fontes | SIGIR Gen-IR / WWW | coorte, bateria, instrumento |
| 3 | Padrões setoriais, econométrico | *Information Sciences* (Elsevier Q1) | metodologia + o parâmetro janela como covariável |
| 4 | Null-Triad | Zenodo (publicado) | — |

O ganho prático de publicar este primeiro: os três seguintes deixam de gastar
seções de método repetindo o mesmo desenho, e passam a citar um DOI. Um revisor
do Q1 que queira auditar o instrumento encontra um documento dedicado em vez de
um apêndice.
