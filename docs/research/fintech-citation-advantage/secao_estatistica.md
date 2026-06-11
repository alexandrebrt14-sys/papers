# Seção estatística — vantagem de citação espontânea de empresas brasileiras por LLMs

> Janela confirmatória v2 (23/04/2026 a 09/06/2026, dia 50 de 90). Extração NER v2 (`cited_v2`). Amostra-núcleo = observações sem probes adversariais e sem itens de calibração. Todos os números derivam diretamente do banco `papers.db` (SQLite, 62.820 observações brutas); nenhum valor foi estimado ou arredondado a partir de fonte secundária. As análises adicionais (leave-one-out, normalização de roster, regressão logística, Mantel-Haenszel, Breslow-Day) foram executadas com `pandas`, `scipy` e `statsmodels` sobre o mesmo banco.

---

## 1. Sumário executivo dos achados quantitativos

1. **A vantagem aparente de fintech é frágil e quase totalmente explicada por uma única entidade-estrela (Nubank).** Na leitura ingênua, fintech lidera a taxa de citação espontânea (28,15%; IC95 27,38–28,95%), acima de varejo (24,94%), tecnologia (14,50%) e saúde (13,35%). Contudo, **59,31% das respostas com citação em fintech são respostas em que o Nubank é a única entidade mencionada**, e o Nubank concentra **49,68% de todas as menções de entidade na vertical**.

2. **Leave-one-out de Nubank inverte o ranking.** Recodificando como "não-citada" toda resposta de fintech cujo único nome próprio citado é o Nubank, a taxa de fintech cai de 28,15% para **11,46%** (IC95 10,91–12,02%), tornando-a a **menor** das quatro verticais. No modelo logístico multivariado, a razão de chances (OR) de fintech em relação à saúde **inverte de 4,13 para 0,77** (IC95 0,70–0,84). Ou seja: o que o desenho mede como "efeito vertical fintech" é, na quase totalidade, um "efeito entidade-estrela".

3. **O efeito de motor (LLM) domina todos os demais.** Perplexity (sonar) cita ~12× mais que o motor de referência (Gemini); Gemini quase nunca cita (OR=0,06). O efeito de LLM tem amplitude muito maior que o efeito de vertical.

4. **A categoria da consulta é forte confundidor.** Consultas de `mercado`, `descoberta` e `comparativo` citam muito mais que `experiencia`, `inovacao` e `confianca`. O mix de categorias é idêntico por desenho (mesmas 6 categorias por vertical), o que controla parcialmente o confundimento, mas a interação categoria×vertical é heterogênea (Breslow-Day p=0,0001).

5. **Idioma importa:** consultas em português citam menos que em inglês (OR pt vs en = 0,61; IC95 0,58–0,65), efeito consistente em todas as verticais exceto saúde.

6. **A taxa de falso-positivo dos decoys fictícios é altíssima (96,9–98,6%)** — discutida como limitação crítica de validade na Seção 7.

---

## 2. Tabelas prontas para o paper

### Tabela 1 — Taxa de citação espontânea por vertical (amostra-núcleo, IC95 Wilson)

| Vertical    |      n | Citadas | Taxa (%) | IC95 (%)        |
|-------------|-------:|--------:|---------:|-----------------|
| Fintech     | 12.648 |   3.561 |   28,15  | 27,38 – 28,95   |
| Varejo      | 12.648 |   3.154 |   24,94  | 24,19 – 25,70   |
| Tecnologia  | 12.547 |   1.819 |   14,50  | 13,89 – 15,12   |
| Saúde       | 12.610 |   1.684 |   13,35  | 12,77 – 13,96   |
| **Total**   | 50.453 |  10.218 |   20,25  | —               |

Qui-quadrado (1 g.l.), fintech vs demais: vs varejo χ²=33,6 (p=6,8×10⁻⁹); vs tecnologia χ²=699,6 (p<10⁻¹⁵); vs saúde χ²=840,6 (p<10⁻¹⁵).

### Tabela 2 — Matriz vertical × LLM (taxa %, amostra-núcleo)

| Vertical    | ChatGPT (gpt-4o-mini) | Claude (haiku-4.5) | Gemini (2.5-pro) | Groq (llama-3.3-70b) | Perplexity (sonar) |
|-------------|----------------------:|-------------------:|-----------------:|---------------------:|-------------------:|
| Fintech     | 18,1                  | 51,0               | 4,9              | 8,7                  | 86,5               |
| Varejo      | 22,2                  | 30,7               | 0,0              | 12,0                 | 92,9               |
| Tecnologia  | 20,4                  | 10,4               | 0,7              | 6,0                  | 54,3               |
| Saúde       | 8,0                   | 10,7               | 0,0              | 6,1                  | 69,8               |

*n por célula ≈ 2.832 (≈1.416 para Perplexity, coletado em metade da cadência).*

### Tabela 3 — Tamanhos de efeito: fintech vs cada vertical (desfecho original)

| Comparação              | Dif. de risco (RD) | IC95 RD           |   RR  |   OR  | IC95 OR       |
|-------------------------|-------------------:|-------------------|------:|------:|---------------|
| Fintech vs varejo       | +0,0322            | +0,0213 .. +0,0431 | 1,129 | 1,180 | 1,115 – 1,247 |
| Fintech vs tecnologia   | +0,1366            | +0,1266 .. +0,1465 | 1,942 | 2,311 | 2,170 – 2,462 |
| Fintech vs saúde        | +0,1480            | +0,1382 .. +0,1578 | 2,108 | 2,543 | 2,384 – 2,711 |

### Tabela 4 — Modelo logístico principal (desfecho `cited_v2`), odds ratios (IC95)

Referências: vertical = saúde; LLM = ChatGPT; categoria = comparativo. N=50.453; pseudo-R² (McFadden)=0,339.

| Termo                          |    OR  | IC95          |
|--------------------------------|-------:|---------------|
| Vertical: tecnologia           |  1,152 | 1,056 – 1,256 |
| Vertical: varejo               |  3,197 | 2,947 – 3,467 |
| **Vertical: fintech**          |  **4,127** | **3,807 – 4,474** |
| LLM: Claude (haiku-4.5)        |  1,788 | 1,669 – 1,915 |
| LLM: Gemini (2.5-pro)          |  0,061 | 0,052 – 0,072 |
| LLM: Groq (llama-3.3-70b)      |  0,400 | 0,367 – 0,437 |
| LLM: Perplexity (sonar)        | 12,122 | 11,122 – 13,213 |
| Categoria: confiança           |  0,469 | 0,428 – 0,514 |
| Categoria: descoberta          |  0,664 | 0,614 – 0,718 |
| Categoria: experiência         |  0,078 | 0,067 – 0,092 |
| Categoria: inovação            |  0,298 | 0,269 – 0,330 |
| Categoria: mercado             |  0,781 | 0,723 – 0,844 |

---

## 3. Análise de robustez decisiva: leave-one-out de Nubank

Esta é a análise central para separar **efeito vertical** de **efeito entidade-estrela**, e ela reposiciona a interpretação de todo o artigo.

### 3.1 Concentração da entidade

- O Nubank responde por **3.533 de 7.112 menções de entidade em fintech = 49,68%** das menções da vertical.
- Das 3.561 respostas com citação em fintech, **2.112 (59,31%) citam exclusivamente o Nubank** (nenhuma outra entidade do roster). Em termos da amostra total de fintech, isso é 16,70% de todas as respostas.

### 3.2 Recálculo da taxa

| Definição de "citada"                                              |   k   |   n    | Taxa (%) | IC95 Wilson (%) |
|--------------------------------------------------------------------|------:|-------:|---------:|-----------------|
| Original (`cited_v2`)                                              | 3.561 | 12.648 |   28,15  | 27,38 – 28,95   |
| **Leave-one-out** (remove respostas com Nubank como única entidade)| 1.449 | 12.648 |   **11,46** | 10,91 – 12,02 |
| Exige ≥1 entidade não-Nubank (idêntico ao LOO)                     | 1.449 | 12.648 |   11,46  | 10,91 – 12,02   |

Sob a definição leave-one-out, **fintech (11,46%) passa a ficar abaixo de saúde (13,35%), tecnologia (14,50%) e varejo (24,94%)** — uma inversão completa do ranking.

### 3.3 Comparação direta LOO

| Comparação (desfecho LOO em fintech)   | Dif. de risco | IC95 RD            |   RR  |   OR  |
|----------------------------------------|--------------:|--------------------|------:|------:|
| Fintech(LOO) vs varejo                 | −0,1348       | −0,1442 .. −0,1254 | 0,459 | 0,389 |
| Fintech(LOO) vs tecnologia             | −0,0304       | −0,0387 .. −0,0221 | 0,790 | 0,763 |
| Fintech(LOO) vs saúde                  | −0,0190       | −0,0271 .. −0,0109 | 0,858 | 0,839 |

Mesmo contra varejo, χ²(LOO-fintech vs varejo)=772,0 (p=6,5×10⁻¹⁷⁰): a diferença é estatisticamente robusta, mas no sentido **oposto** ao da leitura ingênua.

### 3.4 Modelo logístico com desfecho leave-one-out

Refeito o modelo da Tabela 4 com o desfecho recodificado (`cited_loo`), apenas os termos de vertical (mesmas referências, N=50.453, pseudo-R²=0,352):

| Vertical                |    OR  | IC95          |
|-------------------------|-------:|---------------|
| Tecnologia              |  1,157 | 1,059 – 1,264 |
| Varejo                  |  3,296 | 3,035 – 3,579 |
| **Fintech**             |  **0,769** | **0,702 – 0,844** |

**Conclusão substantiva:** controlando LLM e categoria de consulta, a remoção do efeito Nubank faz a OR de fintech inverter de 4,13 para 0,77. A "vantagem de citação de fintech" reportável é, em quase sua totalidade, a saliência de uma única marca no espaço de embeddings/treino dos modelos — não uma propriedade estrutural da vertical.

---

## 4. Normalização por tamanho de roster (efeito de oferta de entidades)

As verticais têm rosters de tamanhos diferentes (fintech=19 entidades BR reais; varejo, tecnologia e saúde=15 cada). Normalizar a taxa pelo número de entidades que poderiam ser citadas remove o artefato de "fintech tem mais alvos".

| Vertical    | Taxa (%) | Roster | Taxa/roster | Entidades/resposta | Menções/entidade |
|-------------|---------:|-------:|------------:|-------------------:|-----------------:|
| Fintech     |  28,15   |   19   |   0,01482   |       0,562        |      187,4       |
| Varejo      |  24,94   |   15   |   **0,01662** |     0,537        |      210,3       |
| Tecnologia  |  14,50   |   15   |   0,00966   |       0,301        |      121,3       |
| Saúde       |  13,35   |   15   |   0,00890   |       0,300        |      112,3       |

Já na taxa por entidade-roster, **varejo (0,01662) supera fintech (0,01482)** — a vantagem bruta de fintech encolhe ao corrigir pela oferta de alvos. Sob a definição leave-one-out e roster sem o Nubank (18 entidades), a taxa por entidade de fintech despenca para **0,00636**, menos da metade de varejo.

---

## 5. Mantel-Haenszel estratificado e homogeneidade

Para isolar o contraste fintech vs varejo (verticais com comportamento mais próximo) do confundidor `query_category`, estimou-se a OR comum de Mantel-Haenszel estratificando pelas 6 categorias de consulta.

- **OR comum de M-H (fintech vs varejo) = 1,205.**

| Categoria   |   a (fin+) |   b (fin−) |   c (var+) |   d (var−) | OR estrato |
|-------------|-----------:|-----------:|-----------:|-----------:|-----------:|
| Comparativo |        926 |      1.418 |        848 |      1.496 |      1,152 |
| Confiança   |        236 |      1.636 |        181 |      1.691 |      1,348 |
| Descoberta  |        952 |      1.392 |        932 |      1.412 |      1,036 |
| Experiência |        130 |      1.742 |         59 |      1.813 |      2,293 |
| Inovação    |        298 |      1.574 |        245 |      1.627 |      1,257 |
| Mercado     |      1.019 |      1.325 |        889 |      1.455 |      1,259 |

**Teste de Breslow-Day de homogeneidade: χ²=25,42 (5 g.l.), p=0,0001.** As OR por estrato **não são homogêneas** (variam de 1,04 em descoberta a 2,29 em experiência), de modo que a OR comum de M-H deve ser reportada com a ressalva de que existe interação vertical×categoria. A OR de M-H (1,205) ainda usa o desfecho original e, portanto, carrega o efeito Nubank; sob LOO o sinal se inverte (ver Seção 3).

---

## 6. Especificação formal dos modelos

### 6.1 Modelo principal recomendado

Regressão logística de efeitos fixos, unidade de observação = resposta individual:

```
logit( P(cited_v2 = 1) ) =
      β0
    + β1 · I(vertical)        [ref. = saúde]
    + β2 · I(llm)             [ref. = ChatGPT/gpt-4o-mini]
    + β3 · I(query_category)  [ref. = comparativo]
```

Estimação por máxima verossimilhança. Reportar OR = exp(β) com IC95 de Wald. N=50.453; pseudo-R² (McFadden)=0,339. **Recomendação de inferência:** reportar com **erros-padrão robustos (HC1) ou agrupados por dia de coleta** (`collection_runs` / `timestamp`), porque há ~100 respostas correlacionadas por execução e 2 coletas/dia ao longo de 50 dias — a independência entre observações é violada e os IC de Wald acima são otimisticamente estreitos. Uma alternativa preferível é um **modelo logístico de efeitos mistos** com intercepto aleatório por dia de coleta e, idealmente, por `query` (a mesma pergunta repetida ao longo do tempo).

### 6.2 Modelo de robustez 1 — co-variáveis de desenho

```
logit( P(cited_v2 = 1) ) = ... (principal) ... + β4·I(query_lang) + β5·I(query_type)
```

Resultados: vertical fintech OR=4,62 (IC95 4,25–5,03); pt vs en OR=0,61 (IC95 0,58–0,65); exploratory vs directive OR=0,25 (IC95 0,24–0,27). Pseudo-R²=0,387. As estimativas de vertical são estáveis frente à inclusão de idioma e tipo de consulta.

### 6.3 Modelo de robustez 2 — desfecho leave-one-out (entidade-estrela)

Idêntico ao principal, mas com desfecho `cited_loo` (Seção 3.4). É o teste decisivo de que o efeito vertical de fintech é, na prática, o efeito Nubank. **Deve constar do corpo do artigo, não de apêndice.**

### 6.4 Modelos de robustez adicionais sugeridos (não estimados aqui)

- **Interação vertical×LLM:** dado que Perplexity satura (até 92,9%) e Gemini zera, o efeito de vertical é potencialmente modificado pelo motor. Recomenda-se um termo de interação e/ou modelos estratificados por LLM.
- **Interação vertical×categoria:** justificada pela heterogeneidade de Breslow-Day (Seção 5).
- **Análise de sensibilidade por entidade-estrela em outras verticais:** repetir o leave-one-out para Mercado Livre/Magazine Luiza (varejo, top-2 = 58,3% das menções), Totvs (tecnologia) e Hypera/EMS (saúde), para verificar se a fragilidade é específica de fintech ou geral.

---

## 7. Tamanhos de efeito com IC95 — quadro consolidado

| Quantidade                                            | Estimativa | IC95              |
|-------------------------------------------------------|-----------:|-------------------|
| Taxa global de citação (núcleo)                       |   20,25%   | —                 |
| RD fintech − saúde (original)                         |  +14,80 pp | +13,82 .. +15,78 pp |
| RD fintech − varejo (original)                        |   +3,22 pp |  +2,13 ..  +4,31 pp |
| OR fintech vs saúde, ajustada (principal)             |    4,13    | 3,81 – 4,47       |
| **OR fintech vs saúde, ajustada (LOO)**               |  **0,77**  | **0,70 – 0,84**   |
| OR Perplexity vs ChatGPT                              |   12,12    | 11,12 – 13,21     |
| OR Gemini vs ChatGPT                                  |    0,061   | 0,052 – 0,072     |
| OR pt vs en                                           |    0,61    | 0,58 – 0,65       |
| OR exploratory vs directive                           |    0,25    | 0,24 – 0,27       |
| Fração de citações fintech que são sole-Nubank        |   59,31%   | —                 |
| Participação do Nubank nas menções de fintech         |   49,68%   | —                 |

---

## 8. Limitações estatísticas (honestas)

1. **Não-independência das observações.** Os IC de Wald do modelo logístico de efeitos fixos tratam 50.453 respostas como independentes, mas há ~100 respostas por execução e a mesma pergunta é repetida 2×/dia por 50 dias. Os IC reportados são, portanto, **otimisticamente estreitos**; a inferência definitiva exige erros-padrão agrupados por dia/pergunta ou efeitos aleatórios (Seção 6.1). Os valores-p extremos (p<10⁻¹⁵⁰) devem ser lidos como "altamente significativo", não como precisão literal.

2. **Efeito entidade-estrela contamina o construto "vertical".** Como demonstra o leave-one-out, o achado principal da leitura ingênua é um artefato de uma única marca. O artigo **não pode** afirmar "fintech é mais citada" sem a ressalva LOO; a formulação defensável é "fintech exibe a maior taxa bruta, integralmente atribuível à saliência do Nubank; descontado o Nubank, fintech é a vertical menos citada".

3. **Heterogeneidade de roster não totalmente corrigida.** A normalização por tamanho de roster (Seção 4) é uma aproximação grosseira: assume que todas as entidades têm igual probabilidade a priori de citação, o que é falso (a distribuição é fortemente concentrada — HHI fintech=0,283). Uma normalização rigorosa exigiria um modelo no nível entidade×consulta.

4. **Taxa de falso-positivo dos decoys é proibitivamente alta (96,9–98,6%).** Os decoys fictícios, que deveriam quase nunca ser "citados", são marcados como citados em ~98% dos casos sob probes adversariais. Isso indica que, sob enquadramento adversarial, o detector NER v2 e/ou os modelos confirmam entidades inexistentes em massa. Embora os decoys estejam fora da amostra-núcleo, essa FPR **mina a validade de construto da medida `cited`** e precisa ser auditada: ou o probe induz alucinação massiva, ou o NER tem viés de aceitação. Até esclarecimento, qualquer taxa absoluta deve ser interpretada como limite superior.

5. **Saturação e censura por motor.** Perplexity satura perto do teto (até 92,9%) e Gemini opera perto do piso (≈0%). Em regimes saturados/censurados, a taxa deixa de discriminar e o efeito logístico de LLM fica mal-condicionado nos extremos (IC de Gemini largo na escala de OR). Modelos estratificados por LLM são mais informativos que o efeito principal agregado.

6. **Janela parcial (dia 50 de 90).** A série semanal (W16–W23) é estável (gap fintech−saúde oscila 13,1–14,9 pp), o que sustenta a robustez temporal do **ranking bruto**, mas a análise é interina; os IC se estreitarão e pequenas reversões de ranking entre verticais próximas (fintech LOO vs saúde/tecnologia) podem mudar até o fechamento da janela.

7. **Confundimento residual de categoria.** O mix de 6 categorias é balanceado por desenho, mas a interação vertical×categoria é significativa (Breslow-Day p=0,0001), de modo que efeitos marginais de vertical agregam estratos não homogêneos; reportar também as estimativas estratificadas.

8. **Validade externa.** Cinco modelos em versões específicas (gpt-4o-mini, haiku-4.5, sonar, etc.) num intervalo de ~7 semanas; resultados não se generalizam para versões maiores dos mesmos provedores nem para além da janela, dada a volatilidade de atualização dos modelos.

---

*Análises executadas em `_run_stats.py` e `_run_stats2.py` (mesmo diretório) sobre `papers.db`. Para reprodução, ambos os scripts leem o banco diretamente e imprimem todos os números aqui tabulados.*
