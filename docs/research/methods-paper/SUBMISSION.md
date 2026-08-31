# Pacote de submissão — SSRN (Elsevier)

Metadata e checklist do paper que especifica o **BRGEO-1**. O manuscrito está em
`MANUSCRIPT.md`; a verificação de cada número, em `VERIFICATION.md`.

**Status:** pronto para revisão do autor. Não submetido.

---

## 1. Metadata para o formulário do SSRN

Campos na ordem em que o formulário pede. Copiar e colar.

### Title

```
BRGEO-1: An Open Protocol for Measuring Entity Citation in Generative Engines
```

### Abstract

Sem markdown, sem quebra dupla de parágrafo. O SSRN corta acima de 1.920
caracteres; a versão abaixo cabe.

```
Large language models now stand between consumers and the firms they might choose, and a market has formed around measuring which firms get named. That market reports citation rates that are not comparable with one another, because the conditions of measurement are left unstated. This paper specifies BRGEO-1, an open protocol for measuring entity citation in generative engines, and argues that a measurement standard - not a metric - is what the field is missing. The protocol fixes five parameters that published figures normally leave implicit: the observation window, the entity cohort with fictitious calibration decoys, the query battery, the engine panel with pinned model versions, and a missingness ledger that records every collection gap rather than imputing it. Of the five, the window is the one we show empirically to matter most. In our own pipeline it had drifted apart between arms unnoticed - five parametric engines measured on the first 200 characters of each answer, one retrieval-augmented engine on the whole response. Across 64,191 observations the asymmetry inflated that engine's citation rate from 52.0% to 75.8%. Re-measuring the five truncated arms under the same window moves none of them by a tenth of a point. We also specify a derived index and then report the result that argues against leaning on it: across 66 entities the composite reorders almost nothing relative to simple coverage (Spearman rho 0.980). A standard should spend its authority on the conditions of measurement, where two defensible choices differ by 23.8 points, not on an aggregation formula where they differ by almost nothing. BRGEO-1 is general in its rules and calibrated on Brazilian data, published with a reference implementation, a conformance definition and a versioning policy.
```

### Keywords

```
generative engine optimization; measurement standard; entity citation; large language models; measurement validity; retrieval-augmented generation
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

A afiliação primária segue o `PUBLISHING_PLAYBOOK.md`: Independent AI Researcher
enquanto a indexação Elsevier da Brasil GEO não conclui. O vínculo comercial não
fica omitido — está na §13 do manuscrito, que é onde a Elsevier exige. A Brasil
GEO aparece na linha de custódia do protocolo, logo abaixo do autor.

### Rede SSRN

Information Systems & eBusiness Network (primária). Considerar Marketing Science
eJournal como secundária, já que o objeto toca descoberta de marca.

---

## 2. O que mudou na versão 1.0 e por quê

O paper nasceu como documentação de protocolo defensiva e foi reposicionado
como **especificação candidata a padrão**. Três decisões de 31/08/2026
sustentam o eixo atual.

**Especificação numerada, custódia declarada.** BRGEO-1 é identificador no
formato de RFC, com a Brasil GEO como custodiante e Alexandre Caramaschi como
autor. A marca aparece na custódia, não no nome da métrica. Um terceiro cita a
especificação sem citar a empresa, que é o que faz padrão ser adotado — e o que
evita que um revisor de periódico Q1 leia o trabalho como métrica de vendor.
A numeração sinaliza série: BRGEO-2 cobriria divergência de fontes e SERP,
BRGEO-3 cobriria medição de intervenção.

**Duas camadas: especificação e índice derivado.** A camada 1 são as regras de
medição; a camada 2 é o GCI, índice reportável. A evidência da §7.2 confirmou a
escolha por um caminho que não era o esperado — ver seção 5 abaixo.

**Protocolo geral, calibrado no Brasil.** As regras servem qualquer mercado; a
calibração é brasileira (PT/EN 50-50, coorte BR, 32 âncoras internacionais para
contraste). Candidata-se a padrão do mercado brasileiro sem se fechar nele, o
que preserva a rota até *Information Sciences*.

---

## 3. Checklist antes de submeter

### Conteúdo

- [ ] Reler o manuscrito inteiro em voz alta — releitura anti-tique.
- [ ] Conferir cada número contra o banco. Toda porcentagem precisa das quatro
      conferências: amostra, período, método, denominador.
- [ ] Abrir todo identificador citado (ORCID, URL do repositório).
- [ ] Confirmar que nenhuma afirmação sobre ausência foi feita sem medição.

### Números que o manuscrito afirma

Todos reproduzíveis; os comandos estão em `VERIFICATION.md`.

| Afirmação | Valor | Seção |
|---|---|---|
| Observações canônicas | 64.191 | Abstract, §4.3 |
| Observações totais | 80.638 | §4.5 |
| Dias com dado / runs abortadas | 49 / 296 | §3.3, §6.2 |
| Perplexity como coletada | 75,8% | §4.3 |
| Perplexity em janela uniforme | 52,0% | §4.3 |
| Delta | −23,8 pp | Abstract, §4.3, §11 |
| Demais braços, delta | +0,0 pp | §4.3 |
| Offset médio, RAG vs paramétricos | 157 vs 97-124 chars | §4.4 |
| Observações que perdem citação no corte | 1.698 | §4.4 |
| Recusas entre as "hallucinations" | 67,4% | §5.2 |
| rho GCI vs cobertura | 0,980 (0,945 na faixa média) | §7.2 |
| Coorte | 127 (111 reais + 16 decoys) | §3.3 |
| Bateria | 192 canônicas + 64 probes | §3.3 |

### Formato

- [ ] Exportar para PDF. O SSRN aceita PDF e DOCX; PDF preserva as tabelas.
- [ ] Página de rosto com título, autor, afiliação, ORCID, custódia e data.
- [ ] Sem cabeçalho ou rodapé com marca comercial. A custódia vai no corpo, na
      linha de autoria e na §9 — não em marca d'água.
- [ ] Numeração de página.

### Governança

- [ ] Declaration of competing interest conferida contra
      `feedback_credencial_tres_chapeus_alexandre`. O texto atual declara o
      cargo na Nuvini, o chapéu sob o qual publica e — o ponto sensível deste
      paper — que a custodiante do padrão vende serviços de GEO.
- [ ] Nenhum uso de "Especialista #1", "Source Rank", "geobrasil.com.br",
      "sourcerank.ai" ou dos cargos obsoletos ("CEO da Brasil GEO",
      "AI Advisor da Nuvini", "conselheiro da Nuvini").
- [ ] Repositório público e navegável no momento da submissão — o manuscrito
      aponta para ele como fonte dos dados E como implementação de referência.
      Um padrão cuja implementação de referência está privada não é um padrão.

### Depois de submeter

- [ ] SSRN devolve o DOI em 24-72 h.
- [ ] Registrar o DOI no ORCID via auto-import Crossref.
- [ ] Adicionar a linha ao histórico do `PUBLISHING_PLAYBOOK.md`.
- [ ] Referenciar o DOI nos papers 1, 2 e 3, que passam a declarar conformidade
      BRGEO-1 em vez de repetir a metodologia.
- [ ] Publicar a página de especificação com a versão resolvível. Um adotante
      precisa citar "BRGEO-1 v1.0" e chegar ao documento exato.

---

## 4. O que este paper deliberadamente não faz

**Não reporta resultados confirmatórios.** A janela de 90 dias fecha em
28/09/2026. Publicar o protocolo antes é o que dá valor ao pré-registro: o plano
de análise entra no registro público antes das estimativas que vai produzir.

**Não compara com estudos de terceiros.** A tese é que taxas publicadas sem
janela declarada não são comparáveis. Compará-las contradiria o argumento. O
efeito é demonstrado no próprio dado, onde as duas medidas existem sob condições
controladas.

**Não afirma que 200 caracteres é a escolha certa.** Afirma que é uma escolha,
que precisa ser declarada, e que a nossa é reportada com sensibilidade nas duas
direções.

**Não vende o índice.** Ver abaixo.

---

## 5. O achado que muda o discurso comercial

A §7.2 reporta que o GCI reordena quase nada em relação à cobertura simples:
rho de Spearman **0,980** na coorte completa, **0,977** removendo o líder de
cada vertical, **0,945** na faixa média da distribuição. A correlação alta não é
artefato de concentração de mercado — sobrevive à remoção do líder e ao recorte
por faixa.

Isso precisa ser dito na reunião antes de virar surpresa, porque contraria o
instinto comercial de transformar o índice em produto:

**O índice não é onde está o valor.** Duas escolhas defensáveis de agregação
produzem quase o mesmo ranking. Duas escolhas defensáveis de janela produzem
23,8 pontos de diferença no mesmo motor, e uma reversão qualitativa de como
aquele motor se compara aos concorrentes. O padrão gasta autoridade onde existe
desacordo, e o desacordo está nas condições de medição.

**Publicar isso fortalece, não enfraquece.** A objeção-padrão a índice composto
é que a agregação é arbitrária. Ao medir quanto a agregação importa e reportar
que é pouco, o paper responde à objeção antes de ela ser feita — e demonstra que
a custodiante testa o próprio instrumento contra o próprio interesse comercial.
É o argumento mais forte disponível contra a leitura de "métrica de vendor".

**Consequência prática para a oferta.** O que a Brasil GEO tem de defensável não
é um número proprietário: é ser a casa que definiu as condições sob as quais o
número de qualquer um passa a significar alguma coisa. A pergunta que separa
medição de afirmação — "sob que janela isso foi medido?" — é uma ferramenta
comercial melhor que um índice, porque nenhum concorrente consegue respondê-la
hoje.

---

## 6. Relação com os outros papers da linha

| # | Paper | Venue | O que herda |
|---|---|---|---|
| 1 | Vertical citation, 90 dias | arXiv `cs.IR` | declara conformidade BRGEO-1 Full + Calibrated |
| 2 | GEO vs SEO, divergência de fontes | SIGIR Gen-IR / WWW | conformidade + candidato a BRGEO-2 |
| 3 | Padrões setoriais, econométrico | *Information Sciences* (Elsevier Q1) | conformidade + a janela como covariável |
| 4 | Null-Triad | Zenodo (publicado) | — |

Ganho prático de publicar este primeiro: os três seguintes param de gastar
seções de método repetindo o desenho e passam a citar um DOI com número de
versão. Um revisor de Q1 que queira auditar o instrumento encontra um documento
dedicado, com implementação de referência, em vez de um apêndice.
