# Red Team — "Vantagem de citação da fintech brasileira em LLMs"

**Revisor 2 (metodologista hostil), periódico A1 · 2026-06-11**

CLAIM SOB ATAQUE: *"A vertical fintech brasileira obtém taxa de citação espontânea sistematicamente maior em LLMs (28,15% vs 13–25% nas demais), explicada por densidade de corpus digital, marcas-categoria e fatores estruturais do setor."*

Veredito antecipado: **a claim, como redigida, não sobrevive a peer review.** Há três defeitos fatais (truncamento de resposta a 200 caracteres, efeito Nubank de entidade única e ausência de consistência direcional entre engines) e vários defeitos graves de inferência. O desenho experimental é, porém, melhor do que o usual em alguns eixos (queries estruturalmente paralelas, balanceamento de categorias, decoys), o que permite uma reformulação honesta e defensável — apresentada no fim.

Todas as queries abaixo foram rodadas no banco `papers.db` sobre o núcleo `is_probe=0 AND is_calibration=0 AND extraction_version='v2'` (n=50.453), que reproduz exatamente os números do `analysis_quant.md`.

---

## A. VALIDADE DE CONSTRUTO — o que "citação espontânea" realmente mede

### A1. As respostas foram TRUNCADAS a exatamente 200 caracteres antes da extração. (GRAVIDADE: ALTA — FATAL)
Verificação direta sobre `LENGTH(response_text)`:

| engine | true text min | avg | max | % linhas com exatamente 200 |
|---|---|---|---|---|
| ChatGPT | 200 | 200 | 200 | 100% (11.328/11.328) |
| Claude | 200 | 200 | 200 | 100% (11.194/11.194) |
| Gemini | 200 | 200 | 200 | 100% (10.939/10.939) |
| Perplexity | 198 | 722 | 2502 | 0% (0/5.664) |

Quatro dos cinco engines tiveram **a resposta inteira persistida cortada em 200 caracteres**. O NER v2 rodou sobre esse snippet, não sobre a resposta completa. Amostra real do Gemini (varejo): *"Excelente pergunta! A resposta para 'qual é o melhor' não é simples, pois o varejo e o e-commerce no Brasil são extremamente competitivos e o 'melhor' depende muito do critério que usamos: volume de v"* — cortada no meio da palavra "volume de v[endas]", antes de qualquer marca.

Consequência: "citação espontânea" NÃO mede se o modelo cita a marca; mede **se o modelo cita a marca nos primeiros ~200 caracteres**. Isso transforma o construto em "velocidade de menção / front-loading", não "propensão de citação". Engines/verticais que abrem com preâmbulo retórico (Gemini, "Excelente pergunta!...") são penalizados artificialmente; verticais cuja marca-líder é citada cedo (fintech/Nubank) são premiados.
- **Respondível com os dados atuais?** NÃO. As respostas completas foram destruídas no armazenamento. É preciso **re-coletar** salvando o texto integral e re-rodar o NER. Sem isso, toda a tabela de taxas é confundida com um artefato de truncamento. **Bloqueia a submissão.**

### A2. NER v2 com alias matching aplica leniência radicalmente desigual entre verticais. (GRAVIDADE: ALTA)
`SUM(via_alias_count_v2)` e `via_fold_count_v2` por vertical (núcleo):

| vertical | respostas citadas | hits via alias | hits via fold |
|---|---|---|---|
| fintech | 3.561 | 164 | 1 |
| varejo | 3.154 | 138 | 0 |
| tecnologia | 1.819 | **4** | 0 |
| saude | 1.684 | **991** | 4 |

Saúde recebe 991 matches por alias (≈59% das suas citações), tecnologia recebe 4. Isso significa que a tabela de alias não é uniforme: algumas verticais ganham crédito por variações ("EMS"/"EMS Pharma"/"Empresa Brasileira...") e outras quase não. O construto "citação" passa a depender de quão generosa foi a curadoria manual de aliases por vertical — uma fonte de viés do anotador, não do modelo.
- **Respondível?** PARCIAL. Auditar a tabela de aliases; reportar taxas com matching estrito (exact only) ao lado das com alias; mostrar que o ranking de verticais é robusto às duas. Hoje não está feito.

### A3. Nomes únicos vs ambíguos enviesam o matching a favor da fintech. (GRAVIDADE: MÉDIA)
"Nubank", "PicPay", "C6 Bank" são strings raras e não-ambíguas — qualquer ocorrência é quase certamente a marca. Já varejo ("Amazon" aparece como "Amazon" e "Amazon Brasil" — duas entradas no top-8, possível dupla contagem ou fusão arbitrária) e tecnologia ("Oracle", "Microsoft", "Google", "Accenture" — multinacionais cuja menção pode ser genérica, não "empresa brasileira do setor") sofrem com falsos negativos (desambiguação conservadora) ou falsos positivos. A vertical fintech tem o roster mais "limpo" para string matching, o que infla sua taxa por construção do NER, não por comportamento do modelo.
- **Respondível?** PARCIAL. Exige revisão manual de uma amostra estratificada (precision/recall do NER por vertical). Sem isso, não se pode separar "fintech é mais citada" de "marcas de fintech são mais fáceis de casar".

### A4. "Espontânea" não é validada contra a self-report do modelo. (GRAVIDADE: BAIXA)
Existe a tabela `dual_responses` (json_cited vs natural_cited, self_report_match) que poderia validar se a menção é genuína citação ou ruído. Não foi usada na análise principal.

---

## B. VALIDADE INTERNA — roster, seleção de marcas, queries, decoys

### B1. Roster desbalanceado: fintech=19, demais=15. (GRAVIDADE: MÉDIA)
`analysis_quant.md` §11 confirma fintech=19 entidades, varejo/tecnologia/saude=15. Mais entidades no roster = maior probabilidade de que ALGUMA marca apareça nos 200 caracteres → `cited_v2=1`. A taxa de citação por-resposta é mecanicamente crescente no tamanho do roster. A "normalização por entidade" do §11 (187 vs 210/121/112) na verdade mostra fintech ABAIXO de varejo por entidade — um resultado que contradiz a claim e não foi destacado.
- **Respondível?** SIM, com os dados atuais. Reamostrar rosters de tamanho fixo (15) por bootstrap, ou modelar a taxa controlando por |roster|. Deve ser feito antes de submeter.

### B2. Critério de seleção das marcas não é cego nem pré-registrado. (GRAVIDADE: MÉDIA)
Não há documentação de como as 19/15 marcas foram escolhidas. Se foram escolhidas por "serem conhecidas/citáveis", há circularidade: seleciona-se marcas citáveis e conclui-se que a vertical é citável. Risco de viés de seleção do experimentador.

### B3. As queries SÃO estruturalmente equivalentes entre verticais — ponto a FAVOR do estudo. (GRAVIDADE: BAIXA, achado favorável)
Verificado no banco: cada vertical tem **48 queries distintas**, geradas pelo mesmo conjunto de templates com apenas a frase-da-vertical trocada. Exemplos pareados:
- fintech: *"Como está estruturado o mercado de fintechs e bancos digitais no Brasil?"*
- varejo: *"Como está estruturado o mercado de varejo e e-commerce no Brasil?"*
- saude: *"Como está estruturado o mercado de saúde e farmacêutica no Brasil?"*

Balanceamento perfeito: 8 queries por `query_category` (comparativo/confianca/descoberta/experiencia/inovacao/mercado) em TODAS as verticais; 24 directive / 24 exploratory em todas. **Nenhuma das 48 queries de qualquer vertical contém o nome de uma marca do roster** (0/48 em todas) — não há vazamento de construto pelo enunciado. Este é o eixo mais forte do desenho e deve ser reportado explicitamente para neutralizar a objeção óbvia de "as perguntas de fintech induziam marcas".

### B4. Mix de categorias é idêntico, mas a SENSIBILIDADE por categoria difere. (GRAVIDADE: MÉDIA)
Embora o mix seja balanceado (B3), o §4 mostra que as categorias de alta taxa (mercado 43,5%, descoberta 40,6%, comparativo 39,5% na fintech) puxam a média. Como o mix é igual, isso não é confounding de composição — mas indica que o "efeito vertical" é heterogêneo por tipo de pergunta e a média de 28,15% mascara que em "experiencia" (6,9%) e "confianca" (12,6%) a fintech não se destaca. A claim de vantagem "sistemática" é falsa no nível de categoria.

### B5. Decoys fictícios revelam FPR catastrófico de ~97–99% em TODAS as verticais. (GRAVIDADE: ALTA)
§8: fintech FPR=98,61%, saude=97,73%, tecnologia=96,94%, varejo=97,49%. Ou seja, quando o roster contém uma marca **inventada**, o detector a "encontra" em ~98% dos casos. Isso é um alarme vermelho sobre o pipeline de matching: ou os decoys foram injetados no texto, ou o detector marca presença indiscriminadamente. Um FPR de 98% torna a especificidade do instrumento praticamente nula — e um instrumento sem especificidade não pode sustentar diferenças de 3pp entre verticais.
- **Respondível?** Precisa de explicação metodológica urgente. Se o FPR alto é por design (decoy plantado no prompt para testar obediência), então NÃO é comparável à citação espontânea e não valida nada sobre falsos positivos na medição real. Se não for por design, **invalida o detector**. Tem de ser esclarecido antes de qualquer claim.

---

## C. VALIDADE EXTERNA — generalização

### C1. Modelos são as variantes BARATAS/pequenas. (GRAVIDADE: ALTA)
`model_version` no banco: ChatGPT=`gpt-4o-mini-2024-07-18`, Claude=`claude-haiku-4-5`, Gemini=`gemini-2.5-pro`, Groq=`llama-3.3-70b`, Perplexity=`sonar`. Quatro dos cinco são tiers mini/haiku/sonar/70B. Resultados de modelos pequenos não generalizam para os flagships (GPT-4o full, Opus, Gemini Ultra) que dominam o tráfego real de citação. A claim deve ser restrita a "modelos de tier econômico".

### C2. Versão única e congelada; sem replicação cross-version. (GRAVIDADE: MÉDIA)
Uma `model_version` por engine. Citação em LLM é instável entre releases; uma vantagem medida em `gpt-4o-mini-2024-07-18` pode evaporar na próxima versão. Sem teste de robustez a versões, a validade temporal é nula.

### C3. Janela de 90 dias (W16–W23) é curta e o gap é estável SÓ nessa janela. (GRAVIDADE: BAIXA)
§6 mostra estabilidade semanal (fintech 27–29%), o que é bom para confiabilidade interna, mas não diz nada sobre estações de notícias (ex.: pico de IPO/regulatório de fintech) que poderiam inflar o corpus naquele trimestre específico.

### C4. PT-BR + Brasil — restrição correta, mas a claim de "densidade de corpus digital" não é testada. (GRAVIDADE: MÉDIA)
A explicação causal ("densidade de corpus, marcas-categoria, fatores estruturais") é especulativa: nenhuma medida de tamanho de corpus, share de notícias ou volume de busca foi cruzada com a taxa. A claim explicativa não tem evidência — é narrativa post-hoc.

---

## D. VALIDADE ESTATÍSTICA

### D1. Observações NÃO são independentes; os IC e qui-quadrado estão inflados. (GRAVIDADE: ALTA)
Verificado: cada vertical tem 48 queries distintas, cada uma repetida ~293 vezes (top-3 fintech: 293/293/293 observações por query). Os n=12.648 são **clusters de ~293 repetições de 48 queries × 5 engines × 2 idiomas**, não 12.648 ensaios independentes. O qui-quadrado de §1 (chi2=33,6, p=6,8e-9 para fintech vs varejo) trata cada linha como i.i.d. — viola frontalmente a independência. O n efetivo é da ordem de **48 queries × 5 engines = 240 clusters**, não 12.648. Recalculado com erros-padrão cluster-robustos (por query e por engine), o IC de 28,15% (hoje 27,38–28,95%) alargaria drasticamente e a diferença de 3,2pp fintech-vs-varejo provavelmente perderia significância.
- **Respondível?** SIM, obrigatório. Usar GLMM logístico com efeitos aleatórios para query e engine (e idioma), ou bootstrap por cluster de query. Sem isso, todos os p-values do paper são inválidos.

### D2. Múltiplas comparações sem correção. (GRAVIDADE: MÉDIA)
São 4 verticais × 5 engines × 6 categorias = **108 células** testadas (verificado), além de 3 testes par-a-par no §1. Nenhuma correção (Bonferroni/Holm/FDR). Com 108 células, achados marginais são esperados por acaso.

### D3. O "efeito" depende de uma única entidade — efeito Nubank. (GRAVIDADE: ALTA — FATAL)
Recomputei a taxa de citação da fintech **excluindo Nubank** do roster:

> **fintech com todos: 28,15% → fintech sem Nubank: 11,46%** (n=12.648)

Sem Nubank a fintech cai de **primeiro para ÚLTIMO lugar** (varejo 24,94%, tecnologia 14,50%, saude 13,35%). A "vantagem da vertical" é inteiramente carregada por **uma marca**. Isso não é um achado sobre "a vertical fintech"; é um achado sobre Nubank. A claim de fenômeno setorial está falsificada pelos próprios dados.
- **Respondível?** SIM (já respondido aqui). A reformulação honesta tem de centrar em Nubank, não na vertical.

---

## E. CONFUNDIMENTO POR ENGINE

### E1. O gap NÃO é consistente entre engines — só 2 de 5 apontam na direção da claim. (GRAVIDADE: ALTA — FATAL)
Teste de sinal fintech vs varejo por engine:

| engine | fintech | varejo | direção |
|---|---|---|---|
| ChatGPT (gpt-4o-mini) | 18,1% | 22,2% | **contra** (−4,1) |
| Claude (haiku) | 51,0% | 30,7% | a favor (+20,3) |
| Gemini (2.5-pro) | 4,9% | 0,0% | a favor (+4,9, mas ver E3) |
| Groq (llama-3.3) | 8,7% | 12,0% | **contra** (−3,3) |
| Perplexity (sonar) | 86,5% | 92,9% | **contra** (−6,4) |

Três dos cinco engines mostram a fintech ABAIXO do varejo. Um "fenômeno setorial sistemático" deveria ter o mesmo sinal na maioria dos engines. Não tem.

### E2. Decomposição do gap: ele é quase inteiramente um efeito Claude. (GRAVIDADE: ALTA)
Excesso de respostas citadas fintech-menos-varejo, por engine:

| engine | fintech citadas | varejo citadas | diferença |
|---|---|---|---|
| Claude | 1.443 | 869 | **+574** |
| Gemini | 134 | 0 | **+134** |
| ChatGPT | 513 | 630 | −117 |
| Perplexity | 1.225 | 1.316 | −91 |
| Groq | 246 | 339 | −93 |

A vantagem agregada da fintech vem de **+574 do Claude (Haiku) e +134 do Gemini** (este último contaminado por truncamento, ver E3), contra a maré dos outros três. Como o Claude Haiku é o modelo da própria casa do harness, há sério risco de o "efeito" ser uma idiossincrasia de um modelo, não uma propriedade do corpus brasileiro de fintech.

### E3. Perplexity-RAG domina as taxas absolutas; Gemini é quase zero por BUG, não por sinal. (GRAVIDADE: ALTA)
- Perplexity (com busca) cita 54–93% em tudo; ele responde "qual é a melhor vertical para RAG", não "qual vertical o modelo cita espontaneamente". Misturar engine-RAG com engines paramétricos numa média única é incoerente: a média de 28,15% é uma quimera de dois construtos. Sem Perplexity, fintech=20,80% e o ranking se mantém — mas os 28,15% do título são inflados pelo RAG.
- Gemini: varejo=0,0% e saude=0,0% citações, com `avg_sources≈0,05` e resposta cortada em 200 chars no meio do preâmbulo. Não é "Gemini não cita fintech menos que varejo"; é **o pipeline não capturou a resposta do Gemini** (preâmbulo retórico longo + truncamento → marca nunca entra na janela). Os zeros do Gemini são artefato de medição e ainda assim contribuem +134 a favor da fintech (E2). **Tem de ser removido ou re-coletado.**

---

## VEREDITO FINAL

### O que a claim atual afirma e por que cai
"Vantagem de citação **sistemática** da **vertical** fintech (28,15%), explicada por **fatores estruturais do setor**" é insustentável porque: (1) o número 28,15% é produto de respostas truncadas a 200 caracteres e da inclusão do RAG-Perplexity; (2) sem Nubank a fintech cai para 11,46% (último lugar) — é efeito de uma marca, não da vertical; (3) só 2 de 5 engines apontam na direção alegada, e o gap é majoritariamente um efeito do Claude Haiku + um artefato do Gemini; (4) os IC/p-values ignoram a dependência de ~293 repetições por query (n efetivo ≈ 240 clusters, não 50 mil); (5) a explicação causal ("densidade de corpus") não foi medida.

### O que os dados HONESTAMENTE permitem afirmar hoje
1. **Descritivo, condicionado e sem causalidade:** "Em uma janela de 90 dias (abr–jun/2026), sobre 48 prompts genéricos estruturalmente pareados por vertical em PT/EN e cinco LLMs de tier econômico, **Nubank** foi a entidade de marca brasileira mais frequentemente mencionada nos primeiros ~200 caracteres das respostas, sustentando sozinha a taxa agregada da vertical fintech." (Forte: o desenho de prompts pareados e o balanceamento de categorias são reais.)
2. **Heterogeneidade por engine é o achado central**, não a vertical: Claude-Haiku exibe forte preferência por marcas de fintech (+20pp vs varejo); ChatGPT-mini, Groq e Perplexity não. Isso é interessante por si — viés de modelo, não de setor.

### Reformulação que sobreviveria ao peer review
> *"Concentração de menção espontânea em entidades-âncora: o caso Nubank em LLMs de tier econômico para o mercado brasileiro."*
> Claim defensável: "A menção espontânea de marcas brasileiras em respostas curtas de LLMs econômicos é altamente concentrada em poucas entidades-âncora e fortemente dependente do engine; na vertical fintech essa concentração é máxima (HHI=0,283; top-3=70,9%) e dominada por Nubank, cuja remoção elimina toda a vantagem agregada da vertical. Não encontramos evidência de vantagem setorial robusta entre engines."

### Bloqueadores obrigatórios ANTES de qualquer submissão
1. **Re-coletar salvando a resposta íntegra** (sem corte de 200 chars) e re-rodar o NER; reportar como a taxa muda. (Sem isso, nada vale.)
2. **Inferência com clustering** (GLMM com efeitos aleatórios de query/engine/idioma) e correção de múltiplas comparações.
3. **Análise leave-one-entity-out** (já prototipada: Nubank) reportada para todas as verticais.
4. **Separar engines RAG (Perplexity) de paramétricos**; nunca reportar a média conjunta como número-título.
5. **Auditar o FPR de 98% dos decoys** e a precisão/recall do NER por vertical (especialmente a assimetria de alias: saúde 991 vs tecnologia 4).
6. **Remover/re-coletar Gemini** (zeros são artefato) e **restringir a claim a modelos de tier econômico**.
