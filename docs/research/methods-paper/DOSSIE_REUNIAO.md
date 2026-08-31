# Dossiê para reunião interna — BRGEO-1

**Protocolo aberto de medição de citação em motores generativos**

Documento de trabalho para discussão. Consolida o health-check da coleta, as
decisões de posicionamento tomadas em 31/08/2026, o manuscrito completo, o
passo a passo de publicação no SSRN e os pontos de alerta.

| | |
|---|---|
| **Data** | 31 de agosto de 2026 |
| **Autor do paper** | Alexandre Caramaschi — ORCID 0009-0004-9150-485X |
| **Custodiante do protocolo** | Brasil GEO |
| **Repositório** | github.com/alexandrebrt14-sys/papers |
| **Alvo de publicação** | SSRN (Elsevier), rede Information Systems & eBusiness |
| **Janela confirmatória** | fecha em 28/09/2026 |

---

# Parte 1 — O pedido e o contexto

## 1.1 O que foi pedido

A sessão começou com dois pedidos, o segundo redirecionado no meio do trabalho.

> Continue rodando research de e https://github.com/alexandrebrt14-sys/papers a
> partir de um healthcheck da coleta. Precisamos que se prepare para publicar o
> paper explicando toda a metodologia e defendendo para que possamos submeter o
> SSDN a Elsevier.

E, depois de o health-check e a primeira versão do paper ficarem prontos:

> O paper que vamos escrever deve priorizar a definição de uma nova metodologia
> de GEO, de Alexandre Caramaschi e da Brasil GEO e como ela se prova útil, se
> candidatando a algo que possa ser utilizado como padrão para o mercado
> brasileiro.

O primeiro pedido produziu um paper de metodologia defensivo: aqui está o nosso
protocolo, e aqui está um problema que encontramos nele. O segundo mudou o eixo
para uma especificação candidata a padrão. É a versão que está na Parte 4.

Nota de nomenclatura: "SSDN" no pedido original é o SSRN — Social Science
Research Network, repositório de working papers da Elsevier.

## 1.2 O estado em que a coleta foi encontrada

A série estava **parada havia oito dias**. O último dia persistido era 23/08 e o
painel do GitHub Actions mostrava uma alternância de `cancelled` e `failure`
sem indicar onde. As duas causas eram independentes e nenhuma aparecia sem
abrir o log do job.

## 1.3 O que foi feito nesta sessão

Quatro commits no `main`, todos com teste e documentação de evento de série.

| Commit | Conteúdo |
|---|---|
| `ee5144c` | Destrava o timeout da coleta: `XAI_REASONING_EFFORT=low` |
| `c8ba558` | Janela de observação unificada, migration 0010, Perplexity nos probes, script de harmonização |
| `53f782c` | Primeira versão do methods paper |
| `4405e92` | Reposicionamento como BRGEO-1 e implementação de referência do índice |

A suíte passou de 223 para **237 testes**, todos verdes.

---

# Parte 2 — Health-check da coleta

## 2.1 Por que a série parou

### O Grok consumia 72% do tempo de coleta

O `grok-4.6` raciocina por padrão, e o raciocínio é cobrado como saída. Medindo
a API com a mesma query que a coleta envia:

| Configuração | Latência | Tokens de raciocínio |
|---|---:|---:|
| Sem parâmetro (como estava) | 73,7 s | 2.746 |
| `reasoning_effort=low` | 19,7 s | 419 |
| `reasoning_effort=none` | HTTP 400 — o modelo recusa o valor | — |

Na run 33303260035 o braço consumiu **129 dos 179 minutos** de wall-clock,
contra 17 do Gemini, 15 do Claude, 12 do ChatGPT e 5 da Perplexity. O job
morria no teto de 180 minutos com a quarta vertical pela metade.

Cinco runs canceladas assim entre 24 e 30/08 queimaram cerca de **900 minutos
de GitHub Actions sem persistir um único dia** — com o orçamento de Actions já
em 514% em 31/08. Efeito colateral do fix: cerca de US$ 3,20 a menos por run
em token de raciocínio.

### Saldo da Anthropic esgotado

As runs de um minuto morriam no preflight com `credit balance is too low`. A
chave é a canônica do projeto (fingerprint `cfcc92e901a33d04`, registrado desde
07/04) e voltou a responder 200 em 31/08 — foi recarga de saldo, não rotação.

O preflight fez exatamente o que deveria: barrou a coleta em vez de gravar um
dia com quatro dos cinco braços. Dia parcial é pior que dia ausente, porque
entra na série parecendo completo.

## 2.2 O achado central: a extração nunca leu a resposta do modelo

A detecção de citação roda sobre a coluna `response_text`. Essa coluna nunca foi
a resposta do modelo: cinco braços gravavam os primeiros 200 caracteres, e a
Perplexity — por percorrer outro caminho no cliente — gravava a resposta
inteira, até 2.502 caracteres.

**A janela de observação ficou assimétrica entre os braços do estudo**, que é
exatamente a comparação que o paper faz.

### Por que nada detectou

Nenhum teste pegou, porque todos afirmavam sobre a coluna e a coluna estava
preenchida nos dois casos. Nenhum validador pegou, porque os dois valores são
strings bem-formadas de tamanho plausível. Os health-checks diários conferiam
que os seis braços produziam linhas, que o split de idioma se mantinha em
50/50, e que os probes estavam marcados — tudo verdade. Os 223 testes passavam.

O defeito vivia um nível abaixo de toda afirmação que o pipeline fazia sobre si
mesmo. Apareceu numa checagem distribucional: o comprimento médio armazenado
batia em exatamente 200,0 em cinco braços e 691,8 no sexto. Uma variável cujo
máximo é igual ao mínimo em 18.560 observações não está medindo nada — está
reportando um limite.

### O tamanho do efeito

| Braço | n | Como coletado | Janela uniforme | Delta | Linhas cortadas |
|---|---:|---:|---:|---:|---:|
| ChatGPT | 14.400 | 17,2% | 17,2% | +0,0 pp | 0 |
| Claude | 14.266 | 25,8% | 25,8% | +0,0 pp | 0 |
| Groq | 14.208 | 8,5% | 8,5% | +0,0 pp | 0 |
| Gemini | 14.011 | 1,8% | 1,8% | +0,0 pp | 0 |
| Grok | 158 | 39,2% | 39,2% | +0,0 pp | 0 |
| **Perplexity** | **7.148** | **75,8%** | **52,0%** | **−23,8 pp** | **7.147** |

Os cinco deltas de +0,0 são a verificação, não decoração: provam que a
re-extração reproduz o instrumento original onde a janela não mudou. É isso que
autoriza ler a sexta linha como correção, e não como código novo produzindo
número novo.

O efeito é grande o bastante para inverter uma interpretação. A 75,8% o motor
RAG parece categoricamente diferente dos paramétricos, quase o dobro do
segundo colocado. A 52,0% segue o mais alto, mas dentro da mesma família — e
qualquer explicação de *por quê* teria de ser outra.

### O viés tem direção previsível

Um motor com busca compõe a resposta depois de buscar fontes e abre com
enquadramento: reformula a pergunta, delimita escopo, comenta o que as fontes
cobrem. Só então nomeia. Um modelo paramétrico nomeia candidatos mais cedo.

| Braço | Observações com citação | Offset médio da 1ª menção | Offset máximo |
|---|---:|---:|---:|
| Perplexity | 5.418 | 157 chars | 1.994 |
| Claude | 3.674 | 124 chars | 194 |
| ChatGPT | 2.471 | 116 chars | 194 |
| Groq | 1.210 | 108 chars | 193 |
| Gemini | 252 | 97 chars | 187 |
| Grok | 62 | 25 chars | 182 |

Uma janela estreita não penaliza todos igualmente: penaliza quem adia o nome. O
confundimento é invisível, sistemático e aponta sempre para o mesmo lado.

## 2.3 Os outros três achados

**Recusa correta contava como alucinação.** O probe adversarial pergunta sobre
uma entidade fictícia, então qualquer resposta que engaje com a pergunta contém
o nome dela — inclusive a recusa. De 15.993 respostas marcadas como alucinação,
**67,4% traziam recusa explícita**, uma delas afirmando que a instituição não é
real nem registrada no Brasil. A taxa publicável não é 97%; é cerca de um terço
disso. O paper passa a reportar uma taxonomia de três casos.

**H2 excluía o único braço RAG do painel.** A Perplexity tinha zero linhas com
`is_probe=1`: o roteamento por categoria nunca incluiu `calibracao_fp`. O
baseline de falso-positivo media só os cinco braços paramétricos e deixava de
fora o caso que motiva a hipótese. Custo de incluir: cerca de US$ 0,64/dia.

**Nenhuma das 80.638 observações era auditável.** O texto além da janela era
descartado no cliente e nunca chegou ao banco. Este é o mais grave dos dois
defeitos de janela: a assimetria é corrigível porque a string truncada ainda é
a string que o extrator viu, mas nenhum cuidado recupera texto que nunca foi
gravado.

**Bônus, e uma lição:** a própria migration que criou a coluna da íntegra caiu
no mesmo padrão de skip silencioso — rodava antes da tabela existir, morria em
`no such table` e o `except` virava log DEBUG. Foi pega por teste de regressão
que falha se um banco novo nascer sem as colunas. É o mesmo padrão do restore
R2 que ficou dois meses inerte.

---

# Parte 3 — As decisões de posicionamento

Três decisões tomadas em 31/08/2026 definem o eixo do paper.

## 3.1 Nome e atribuição: especificação numerada, custódia declarada

**BRGEO-1**, identificador no formato de RFC. Brasil GEO como custodiante,
Alexandre Caramaschi como autor.

O trade-off é real. Padrão vira padrão por adoção de terceiros, e um nome com a
marca da empresa dentro da métrica, num paper que já declara conflito de
interesse, tende a ser lido como peça comercial — e dá ao concorrente um motivo
para não adotar. A numeração resolve os dois lados: a marca aparece no
identificador e na linha de custódia, o terceiro cita a especificação, e a série
fica aberta (BRGEO-2 para divergência de fontes e SERP, BRGEO-3 para medição de
intervenção).

**Alternativas descartadas:** "Brasil GEO Citation Standard" (atribuição máxima,
mas revisor de Q1 trata como métrica de vendor); nome neutro sem marca alguma
(adoção acadêmica máxima, mas o mercado brasileiro não associa o padrão à casa).

## 3.2 Saída: especificação com índice derivado

Camada 1 são as regras de medição. Camada 2 é o GCI, índice reportável, sempre
publicado junto dos três componentes que o formam.

A evidência confirmou a escolha por um caminho inesperado — ver 3.4.

## 3.3 Alcance: protocolo geral, calibrado no Brasil

As regras servem qualquer mercado; a calibração é brasileira. Candidata-se a
padrão do mercado brasileiro sem se fechar nele, o que preserva a rota até
*Information Sciences*.

O argumento técnico para calibrar em português é bom e está no paper: medição
em português quebra de formas que ferramental english-first não antecipa —
diacríticos que os modelos renderizam de forma inconsistente entre idiomas,
marcas que colidem com palavras comuns, e um mercado cujas empresas líderes são
posteriores ao corte de pré-treino de vários modelos em produção. Um protocolo
que sobrevive ao português foi testado em condição mais dura.

## 3.4 O achado que muda o discurso comercial

Depois de definir o índice, medimos se ele faz alguma coisa. Não faz muito:

| Recorte | rho de Spearman | n |
|---|---:|---:|
| Todas as entidades | 0,980 | 66 |
| Sem o líder de cada vertical | 0,977 | 62 |
| Faixa média (0,1% a 5% de cobertura) | 0,945 | 42 |
| Cauda (abaixo de 1%) | 0,957 | 44 |

O índice composto reordena quase nada em relação à cobertura simples. E a
correlação alta **não** é artefato de concentração de mercado: sobrevive à
remoção do líder de cada vertical e ao recorte por faixa.

Isso precisa ser dito na reunião antes de virar surpresa, porque contraria o
instinto comercial de transformar o índice em produto.

**A leitura correta fortalece o padrão.** Duas escolhas defensáveis de
agregação produzem quase o mesmo ranking; duas escolhas defensáveis de janela
produzem 23,8 pontos e uma reversão qualitativa. O padrão deve gastar
autoridade onde existe desacordo, e o desacordo está nas condições de medição.

Publicar isso responde, antes de ser feita, à objeção-padrão contra índice
composto — que a agregação é arbitrária. É também o argumento mais forte
disponível contra a leitura de "métrica de vendor": a custodiante testou o
próprio instrumento contra o próprio interesse comercial e publicou o resultado
desfavorável.

**Consequência para a oferta.** O ativo defensável da Brasil GEO não é um número
proprietário. É ser a casa que definiu as condições sob as quais o número de
qualquer um passa a significar alguma coisa. A pergunta que separa medição de
afirmação — *sob que janela isso foi medido?* — é ferramenta comercial melhor
que um índice, porque nenhum concorrente consegue respondê-la hoje.

---

# Parte 5 — Guia de publicação no SSRN

## 5.1 O que o SSRN é e o que não é

| | |
|---|---|
| **O que é** | Repositório de working papers da Elsevier. Revisão editorial de admissibilidade, **sem peer review**. |
| **Prazo** | 24 a 72 horas até o DOI |
| **Custo** | US$ 0 |
| **Indexação** | Google Scholar; Scopus a nível de paper, de forma lenta |
| **Status do trabalho** | *Working paper* — permite republicar depois em periódico |

O ponto que importa para a estratégia: publicar no SSRN **não queima** a
submissão posterior a um periódico Q1. Elsevier, Springer, Wiley, ACM e IEEE
aceitam preprint prévio. O SSRN dá DOI permanente, data de precedência e um
identificador citável pelos outros três papers da linha.

O que ele não dá: validação por pares. Um working paper no SSRN não é evidência
de que a metodologia foi aprovada por ninguém, e nenhum material comercial deve
sugerir que é. Ver Parte 6.

## 5.2 Passo a passo

**1. Login.** [papers.ssrn.com](https://papers.ssrn.com) — entrar com ORCID iD
(0009-0004-9150-485X) ou com a conta institucional. Usar ORCID facilita o
auto-import do DOI depois.

**2. Submit a Paper.** Escolher a rede: *Information Systems & eBusiness
Network* como primária. Considerar *Marketing Science eJournal* como secundária,
já que o objeto toca descoberta de marca.

**3. Metadata.** Título, abstract, keywords e JEL estão prontos para copiar e
colar em `SUBMISSION.md`, seção 1, na ordem em que o formulário pede. O abstract
já está sem markdown e dentro do limite de 1.920 caracteres.

**4. Affiliation.** *Independent AI Researcher* como primária, conforme o
`PUBLISHING_PLAYBOOK.md`. A Brasil GEO entra na linha de custódia do protocolo,
logo abaixo do autor, e o vínculo comercial está declarado na §13 do
manuscrito.

**5. Upload.** PDF. O SSRN aceita DOCX, mas o PDF preserva as tabelas, que neste
paper carregam os números centrais.

**6. Aguardar.** O DOI chega em 24 a 72 horas.

## 5.3 Depois da publicação

- Registrar o DOI no ORCID via auto-import Crossref.
- Adicionar a linha ao histórico do `PUBLISHING_PLAYBOOK.md`.
- Publicar a página de especificação com **versão resolvível**: um adotante
  precisa citar "BRGEO-1 v1.0" e chegar ao documento exato. Sem isso a
  numeração da versão não significa nada.
- Fazer os papers 1, 2 e 3 declararem conformidade BRGEO-1 em vez de repetirem
  a seção de metodologia.

## 5.4 A rota até o Q1

| Etapa | Canal | Quando | Observação |
|---|---|---|---|
| 1 | SSRN | set/2026 | Este paper. DOI e precedência. |
| 2 | arXiv `cs.IR` | 30 dias depois | Exige *endorsement*; declarar o DOI do SSRN em nota. |
| 3 | Zenodo | fechamento da janela | Snapshot do dataset com DOI próprio, referenciando o SSRN como identificador alternativo. |
| 4 | *Information Sciences* (Elsevier, Q1) | dez/2026 | Paper 3, econométrico, declarando conformidade BRGEO-1. |

Links úteis: [Elsevier Journal Finder](https://journalfinder.elsevier.com/)
para checar aderência de escopo, e [Sherpa Romeo](https://v2.sherpa.ac.uk/romeo/)
para confirmar a política de preprint de cada periódico antes de submeter.

---

# Parte 6 — Ressalvas, boas práticas e pontos de alerta

## 6.1 Pontos de alerta — resolver antes de submeter

**O conflito de interesse é o mais direto que existe neste tipo de trabalho.**
Uma empresa que vende serviços de GEO propõe o padrão de medição de GEO e se
oferece para custodiá-lo. Isso não é impedimento, mas exige que a declaração
seja franca em vez de formal. A §13 do manuscrito diz, em letras: a custodiante
vende o serviço, se beneficia se o padrão for adotado, e o leitor deve pesar o
trabalho por isso. Três características do desenho limitam o que esse interesse
consegue fazer com o resultado — coorte fixada antes da coleta e sem cliente
escolhido a dedo, especificação e plano de análise públicos antes do fechamento
da janela, e um resultado publicado que contraria o interesse comercial (§7.2).
Enfraquecer essa declaração para parecer mais neutro produziria o efeito oposto.

**A implementação de referência precisa estar pública no momento da
submissão.** O manuscrito aponta o repositório como fonte dos dados e como
implementação de referência. Um padrão cuja implementação está privada não é um
padrão, e um revisor que clicar e não conseguir ver rejeita por isso.

**Não afirmar validação por pares.** O SSRN não faz peer review. Qualquer
material comercial que descreva o paper como "publicado" precisa dizer
*working paper*. Confundir os dois é o erro reputacional mais fácil de cometer
e o mais caro de desfazer.

**A janela de 90 dias ainda não fechou.** O paper não traz resultado
confirmatório, e é assim de propósito. Nenhum material derivado pode apresentar
os números descritivos deste dossiê como conclusão do estudo. Eles são
preliminares e o próprio manuscrito os declara como tal.

**Números com quatro conferências.** Toda porcentagem que sair daqui para
apresentação precisa de amostra, período, método e denominador. Os do dossiê
têm; os que forem recalculados na reunião precisam ter também.

## 6.2 Ressalvas científicas que o paper declara

Estão na §10 do manuscrito e é melhor que a reunião as conheça antes de um
revisor as levantar.

**A validação de modo de elicitação não rodou.** Enviamos prompts em linguagem
natural e extraímos entidades depois, o que é mais próximo do que o usuário vê
do que pedir ao modelo uma lista estruturada. Mas a comparação entre os dois
modos nunca rodou em escala: a tabela `dual_responses` está vazia. É a ameaça
declarada mais séria à validade de construto, e a mais fácil de resolver antes
da submissão.

**A janela de 200 caracteres é uma escolha, não uma verdade.** O paper afirma
que precisa ser declarada, não que 200 é o valor certo. Todo número principal é
reportado sob as duas janelas.

**O índice acrescenta pouco.** Reportado como limitação e como achado (§7.2).

**Quatro eventos de série em cinco meses.** Modelo do Gemini trocado, quinto
braço substituído, janela unificada, esforço de raciocínio reduzido. Cada um
datado e estratificado, mas comparação através de fronteira dentro do braço
afetado é descritiva.

**Amostragem desigual.** O roteamento envia à Perplexity cerca de metade da
bateria canônica, por custo. Poder por célula menor, reportado em vez de
corrigido por peso.

**49 dias com dado contra 296 runs abortadas.** E os gaps não são aleatórios:
concentram-se em esgotamento de crédito, que correlaciona com custo, que
correlaciona com comprimento de resposta. O ledger é publicado e os dias são
ponderados por cobertura; o paper não afirma que o mecanismo é ignorável.

## 6.3 Boas práticas que o repositório já impõe

- **Nada é imputado.** Todo gap entra no ledger com data, extensão e causa.
- **Nada é sobrescrito.** A harmonização grava colunas novas ao lado das
  originais, depois de backup SHA-256 com manifest.
- **Toda mudança de instrumento é evento de série datado**, no `CHANGELOG` e na
  `METHODOLOGY_V2`.
- **Modelo pinado em toda observação.** Provedor que atualiza modelo em silêncio
  aparece na distribuição de hashes antes de aparecer nas estimativas.
- **Preflight que aborta.** Melhor dia ausente que dia parcial.
- **Cada número do paper tem um comando que o reproduz**, em
  `VERIFICATION.md`. Número que não estiver lá não entra no manuscrito.

## 6.4 Alerta operacional em aberto

O orçamento de GitHub Actions estava em **514%** em 31/08, e boa parte disso foi
consumida por runs que não produziram dado. O fix do Grok deve derrubar o tempo
de coleta de mais de 180 minutos para cerca de 95, mas a métrica de controle é
minuto de Actions em `github.com/settings/billing`, não contagem de execuções.

---

# Parte 7 — Pauta sugerida para a reunião

**1. O achado da janela, e o que ele significa comercialmente.** 23,8 pontos em
um motor, com direção previsível. A pergunta *sob que janela isso foi medido?*
é o diferencial mais defensável que a casa tem hoje, e nenhum concorrente
consegue respondê-la.

**2. O índice não é o produto.** Discutir o resultado de 3.4 antes que alguém
construa oferta em cima de um número composto. A recomendação é vender a
especificação e a auditoria, não o índice.

**3. Nome e custódia.** Confirmar BRGEO-1 e a decisão de manter a marca na
custódia em vez de dentro da métrica. É reversível agora e caro de reverter
depois do DOI.

**4. A validação `dual_responses`.** Rodar antes ou depois da submissão. Rodar
antes fortalece o argumento; rodar depois acelera o DOI em algumas semanas.

**5. Governança da série.** Quem mantém a especificação, com que cadência, e o
que dispara incremento de versão maior. Sem isso, BRGEO-2 nunca sai.

**6. Cronograma.** Submissão em setembro, janela fechando em 28/09, análise
confirmatória em outubro, Paper 3 para *Information Sciences* em dezembro.

---

# Anexo A — Verificação dos números

Cada afirmação quantitativa deste dossiê e do manuscrito tem um comando que a
reproduz, listado em `VERIFICATION.md`. Os principais:

```bash
# obter a cópia corrente do banco (não é versionado em git: cruzou 100 MB)
gh run download -R alexandrebrt14-sys/papers -n papers-db-latest -D /tmp/dbcheck
export DB=/tmp/dbcheck/papers.db

# a tabela do efeito da janela — o número central do paper
python scripts/harmonize_citation_window.py --db "$DB" --check --canonical-only

# o índice contra a cobertura simples
python scripts/brgeo1_index.py --db "$DB" --vertical fintech --compare

# ledger de gaps
sqlite3 "$DB" "SELECT
  (SELECT COUNT(DISTINCT date(timestamp)) FROM citations) AS dias_com_dado,
  (SELECT COUNT(*) FROM collection_runs WHERE status='aborted') AS abortadas;"
```

**A regra:** nenhum número entra no manuscrito sem constar da lista de
verificação com o comando que o produz. Se um número aparecer no texto e não
lá, ou saiu de uma medição que ninguém consegue repetir, ou saiu de lugar
nenhum.

# Anexo B — Cronograma

| Quando | O quê |
|---|---|
| 31/08/2026 | Coleta destravada; paper reposicionado como BRGEO-1 |
| set/2026 | Revisão do autor, validação `dual_responses`, submissão ao SSRN |
| 28/09/2026 | Fecha a janela confirmatória de 90 dias |
| out/2026 | Análise confirmatória sobre a série fechada |
| out-nov/2026 | arXiv `cs.IR`; snapshot do dataset no Zenodo |
| dez/2026 | Paper 3 para *Information Sciences* (Elsevier Q1) |
