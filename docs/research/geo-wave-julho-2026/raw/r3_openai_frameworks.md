## 1) Workflow operacional completo de GEO (do baseline à iteração)

### 1.1. Auditoria de baseline: “onde a marca aparece, como aparece e por quê”

**Objetivo:** medir presença, precisão e preferência da marca em respostas de mecanismos generativos: ChatGPT/SearchGPT, Google AI Overviews/AI Mode, Perplexity, Copilot, Claude, Gemini, You.com, ferramentas verticais e assistentes com busca.

#### Checklist de baseline

**A. Inventário de entidades**
- Nome oficial da empresa.
- Variações de marca.
- Produtos, linhas, categorias e soluções.
- Fundadores, executivos, autores e especialistas.
- Concorrentes diretos e indiretos.
- Categorias em que a empresa quer ser recomendada.
- Localizações, mercados atendidos, segmentos, ICPs.
- Páginas canônicas: homepage, produto, pricing, estudos de caso, comparativos, docs, páginas institucionais.

**B. Auditoria de presença em AI**
Executar prompts padronizados em múltiplos motores:

- “Quais são as melhores empresas para [categoria]?”
- “Compare [marca] vs [concorrente].”
- “Qual ferramenta escolher para [caso de uso]?”
- “Quais fornecedores atendem [segmento] no Brasil?”
- “Quais alternativas a [concorrente]?”
- “Quem é referência em [tema]?”
- “Quais são os prós e contras da [marca]?”
- “A [marca] é confiável?”
- “Quanto custa [tipo de solução]?”
- “Quais empresas oferecem [feature específica]?”

Para cada resposta, registrar:

- A marca apareceu?
- Em qual posição?
- Foi recomendada ou apenas mencionada?
- Houve citação/link?
- Quais fontes foram usadas?
- A descrição estava correta?
- Havia erro factual?
- Quais concorrentes dominaram a resposta?
- O modelo usou fontes recentes ou antigas?
- A resposta indicou intenção comercial, informacional ou comparativa?
- A marca foi associada às entidades corretas?

**C. Auditoria de fontes citadas pelos motores**
Mapear os domínios que aparecem como fonte:

- Sites próprios.
- Reviews.
- Diretórios.
- Reddit.
- YouTube.
- Wikipedia/Wikidata.
- Sites de notícias.
- Blogs especializados.
- Documentação técnica.
- Comunidades.
- Marketplaces.
- G2/Capterra/Trustpilot/Reclame Aqui, quando aplicável.
- Estudos, pesquisas, relatórios setoriais.

**D. Auditoria de conteúdo próprio**
Verificar se o site possui páginas claras para:

- O que a empresa faz.
- Para quem serve.
- Casos de uso.
- Comparativos.
- Alternativas.
- Preços ou lógica de pricing.
- Integrações.
- Segmentos atendidos.
- Páginas “best for”.
- FAQ factual.
- Estatísticas próprias.
- Estudos de caso.
- Páginas autorais com especialistas.
- Conteúdo atualizado.
- Conteúdo com tabelas, definições, listas e dados facilmente extraíveis.

**E. Auditoria técnica**
- Indexação no Google/Bing.
- Renderização de conteúdo.
- Schema.org.
- Sitemaps.
- Canonicals.
- Páginas órfãs.
- Conteúdo bloqueado por robots.txt.
- Bloqueio ou permissão para crawlers de IA.
- Velocidade e acessibilidade.
- Estrutura semântica de headings.
- Conteúdo duplicado.
- Dados estruturados válidos.
- Presença ou não de `llms.txt`.

---

### 1.2. Pesquisa de prompts: “prompt research”, não apenas keyword research

Em GEO, a unidade de demanda não é só a palavra-chave. É o **prompt**: uma pergunta, tarefa ou cenário que o usuário entrega a um motor generativo.

#### Tipos de prompts a mapear

**A. Prompts de descoberta**
- “Quais são as melhores plataformas de [categoria]?”
- “Me indique fornecedores de [solução] para [tipo de empresa].”
- “Quais empresas brasileiras fazem [serviço]?”

**B. Prompts comparativos**
- “[Marca A] vs [Marca B].”
- “Alternativas a [concorrente].”
- “Qual é melhor: [marca] ou [concorrente]?”
- “Compare preços, recursos e reputação.”

**C. Prompts de decisão**
- “Qual ferramenta escolher para uma empresa de [segmento] com [necessidade]?”
- “Monte uma shortlist de fornecedores.”
- “Quais critérios usar para contratar [solução]?”

**D. Prompts de validação**
- “A [marca] é confiável?”
- “A [marca] tem boas avaliações?”
- “Quais reclamações existem sobre [marca]?”
- “Quais clientes usam [marca]?”

**E. Prompts de implementação**
- “Como implementar [solução]?”
- “Como integrar [produto] com [sistema]?”
- “Quais boas práticas para [processo]?”

**F. Prompts de definição**
- “O que é [conceito]?”
- “Como funciona [categoria]?”
- “Quais os benefícios de [tipo de solução]?”

#### Como construir uma biblioteca de prompts

Para cada prompt, registrar:

- Cluster de intenção.
- Persona.
- Etapa do funil.
- Categoria.
- Mercado/região.
- Modelo testado.
- Frequência estimada.
- Valor comercial.
- Grau de competição.
- Resposta atual dos motores.
- Fontes citadas.
- Oportunidade de conteúdo.
- Oportunidade de PR/distribuição.
- Oportunidade técnica.
- Prioridade.

#### Score de priorização de prompts

Use um score simples de 1 a 5:

| Critério | Pergunta |
|---|---|
| Valor comercial | Esse prompt pode influenciar compra? |
| Probabilidade de menção | A marca tem autoridade para aparecer? |
| Lacuna atual | A marca está ausente ou mal descrita? |
| Competição | Concorrentes dominam a resposta? |
| Capacidade de ação | Podemos criar fonte/citação/conteúdo para esse prompt? |
| Risco reputacional | Há erros ou narrativas ruins sobre a marca? |

Priorizar prompts com:

- Alto valor comercial.
- Alta lacuna atual.
- Alta chance de intervenção.
- Forte presença de concorrentes.
- Risco de erro factual.

---

### 1.3. Produção e otimização de conteúdo para GEO

O conteúdo para GEO deve ser **citável, factual, estruturado, verificável e alinhado a entidades**.

#### Tipos de páginas prioritárias

**A. Páginas de entidade**
- Sobre a empresa.
- Página institucional com dados objetivos.
- Página de liderança/executivos.
- Página de autores/especialistas.
- Página de imprensa/media kit.
- Página de dados da empresa: ano de fundação, sede, clientes, categorias, certificações.

**B. Páginas comerciais**
- Produto.
- Solução por segmento.
- Solução por caso de uso.
- Preços.
- Integrações.
- Comparativos.
- Alternativas a concorrentes.
- “Melhor para [ICP]”.
- “Como escolher [categoria]”.

**C. Conteúdo citável**
- Relatórios próprios.
- Benchmarks.
- Pesquisas.
- Estatísticas.
- Glossários.
- Guias definitivos.
- Tabelas comparativas.
- Estudos de caso.
- FAQs com respostas diretas.
- Páginas com metodologia.
- Páginas de dados atualizadas periodicamente.

**D. Conteúdo de prova**
- Depoimentos.
- Logos de clientes, quando permitido.
- Certificações.
- Avaliações.
- Selos.
- Estudos de ROI.
- Cases com números.
- Demonstrações públicas.
- Vídeos explicativos.

#### Checklist de otimização de conteúdo para IA

Cada página relevante deve responder claramente:

- Quem é a empresa?
- O que oferece?
- Para quem?
- Em quais mercados?
- Quais problemas resolve?
- Quais diferenciais?
- Quais limitações?
- Quais integrações?
- Quais provas existem?
- Como se compara a alternativas?
- Quais dados podem ser citados?
- Quando foi atualizada?
- Quem escreveu ou revisou?
- Quais fontes sustentam as afirmações?

#### Estrutura recomendada de uma página GEO-ready

1. Resumo objetivo em 2 a 4 frases.
2. Definição da categoria.
3. Para quem é indicado.
4. Principais recursos.
5. Casos de uso.
6. Diferenciais comprováveis.
7. Tabela de comparação.
8. Dados, estatísticas ou benchmarks.
9. Exemplos reais.
10. FAQs.
11. Autor/revisor.
12. Data de atualização.
13. Schema.org adequado.
14. Links internos para entidades relacionadas.
15. Links externos confiáveis, quando fizer sentido.

---

### 1.4. Distribuição: onde influenciar as fontes que os modelos usam

GEO não é só publicar no próprio site. Motores generativos tendem a compor respostas a partir de sinais distribuídos de autoridade.

#### Canais prioritários

### A. PR digital

Objetivo: gerar menções em veículos e sites setoriais confiáveis.

Checklist:

- Criar ângulos noticiáveis baseados em dados.
- Publicar estudos proprietários.
- Oferecer porta-vozes.
- Conseguir entrevistas.
- Criar rankings ou benchmarks.
- Distribuir releases com dados concretos.
- Priorizar veículos que aparecem como fonte em respostas de IA.
- Buscar menções com contexto semântico, não apenas backlinks.
- Garantir consistência de nome, descrição e categoria da empresa.

Boas pautas para GEO:

- “Relatório 2026 sobre [tema].”
- “Benchmark de [mercado].”
- “Dados inéditos sobre comportamento de [perfil].”
- “Estudo mostra impacto de [tendência].”
- “Guia para escolher fornecedores de [categoria].”

---

### B. Comunidades

Objetivo: inserir a marca em conversas reais, com legitimidade.

Canais:

- Reddit.
- Quora.
- Stack Overflow, se técnico.
- Hacker News.
- Product Hunt.
- Comunidades Slack/Discord.
- Fóruns de nicho.
- Grupos profissionais.
- Comunidades locais.

Checklist:

- Não fazer spam.
- Responder dúvidas reais.
- Declarar afiliação quando aplicável.
- Compartilhar experiência prática.
- Publicar comparações honestas.
- Coletar linguagem real de usuários.
- Identificar objeções recorrentes.
- Mapear concorrentes citados organicamente.
- Transformar perguntas recorrentes em conteúdo próprio.

---

### C. Wikipedia e Wikidata

Objetivo: fortalecer entidade, quando houver notoriedade suficiente.

Checklist:

- Não criar página promocional.
- Verificar critérios de notoriedade.
- Buscar cobertura independente antes.
- Usar fontes secundárias confiáveis.
- Evitar linguagem de marketing.
- Corrigir apenas fatos verificáveis.
- Criar ou melhorar item no Wikidata quando cabível.
- Garantir consistência de:
  - Nome legal.
  - Nome comercial.
  - Fundadores.
  - Data de fundação.
  - Sede.
  - Categoria.
  - Site oficial.
  - Identificadores externos.

Atenção: Wikipedia não é canal de aquisição direta. É infraestrutura de entidade. Usar mal pode gerar remoção, bloqueio e dano reputacional.

---

### D. YouTube

Objetivo: gerar sinais audiovisuais e conteúdo transcrito que modelos podem usar.

Checklist:

- Criar vídeos explicativos sobre categorias.
- Publicar comparativos honestos.
- Fazer demos.
- Publicar webinars com especialistas.
- Otimizar títulos, descrições e capítulos.
- Incluir transcrição.
- Responder perguntas nos comentários.
- Usar dados e exemplos claros.
- Linkar para páginas canônicas.
- Criar playlists por caso de uso.

Formatos úteis:

- “Como escolher [solução].”
- “[Categoria] explicado em 10 minutos.”
- “Comparativo entre [abordagens].”
- “Erros comuns ao contratar [serviço].”
- “Demonstração prática de [produto].”

---

### E. Reddit

Objetivo: aparecer em discussões autênticas que influenciam respostas de IA e percepção de compra.

Checklist:

- Mapear subreddits relevantes.
- Entender regras de cada comunidade.
- Participar antes de publicar.
- Usar contas pessoais com histórico legítimo.
- Responder perguntas com profundidade.
- Evitar autopromoção direta.
- Compartilhar aprendizados, não propaganda.
- Monitorar menções negativas.
- Corrigir informações falsas com transparência.
- Identificar prompts baseados em perguntas reais.

---

### 1.5. Medição

A medição de GEO deve combinar:

1. Visibilidade em respostas de IA.
2. Qualidade da menção.
3. Fontes citadas.
4. Tráfego e conversões vindas de AI.
5. Impacto em pipeline e receita.
6. Correção factual.

#### KPIs principais

**Visibilidade**
- AI Share of Voice.
- Taxa de presença por prompt.
- Posição média na resposta.
- Frequência de citação/link.
- Presença em listas recomendadas.
- Cobertura por modelo.

**Qualidade**
- Sentimento da menção.
- Precisão factual.
- Categoria correta.
- Diferenciais mencionados.
- Concorrentes associados.
- Risco reputacional.
- Consistência da descrição.

**Fontes**
- Domínios mais citados.
- Fontes próprias vs terceiras.
- Fontes novas conquistadas.
- Autoridade das fontes.
- Frescor das fontes.

**Negócio**
- Sessões vindas de AI referral.
- Conversões assistidas.
- Leads influenciados.
- Pipeline influenciado.
- Receita influenciada.
- CAC por canal assistido.
- Taxa de conversão de tráfego AI.
- Queries/perguntas que geram demanda.

---

### 1.6. Report

O report deve traduzir GEO em linguagem executiva:

- Onde estamos aparecendo?
- Onde não estamos?
- Quem está ganhando?
- Quais erros os modelos dizem sobre nós?
- Quais prompts têm valor comercial?
- Que ações executamos?
- Qual impacto em tráfego, pipeline e receita?
- O que faremos no próximo ciclo?

Estrutura detalhada está na seção 3.

---

### 1.7. Iteração

GEO é ciclo contínuo. Os motores mudam respostas, fontes, ranking implícito e citações.

#### Loop mensal de iteração

1. Reexecutar biblioteca de prompts.
2. Comparar respostas com baseline.
3. Identificar ganhos e perdas.
4. Mapear novas fontes citadas.
5. Atualizar páginas com dados novos.
6. Corrigir erros factuais.
7. Produzir novos ativos.
8. Distribuir ativos em canais externos.
9. Atualizar dashboards.
10. Redefinir prioridades para o próximo sprint.

---

## 2) Estrutura de um programa de GEO

### 2.1. Papéis essenciais

#### 1. GEO Lead / Strategist

Responsável por:

- Estratégia geral.
- Priorização de prompts.
- Interface com SEO, conteúdo, PR, produto e dados.
- Definição de KPIs.
- Roadmap trimestral.
- Governança do programa.

#### 2. Prompt Research Analyst

Responsável por:

- Criar e manter biblioteca de prompts.
- Rodar testes em múltiplos motores.
- Classificar intenções.
- Monitorar presença de concorrentes.
- Identificar fontes usadas por IA.
- Transformar prompts em briefs.

#### 3. Content Strategist

Responsável por:

- Arquitetura de conteúdo.
- Briefs editoriais.
- Mapeamento de páginas comerciais e informacionais.
- Criação de clusters por entidade.
- Definição de formatos citáveis.

#### 4. Redator/Editor especialista

Responsável por:

- Produzir conteúdo factual e denso.
- Evitar linguagem genérica.
- Incluir dados, tabelas, exemplos e FAQs.
- Garantir clareza semântica.
- Manter consistência de entidade.

#### 5. Especialista técnico SEO/GEO

Responsável por:

- Schema.org.
- Indexação.
- Crawlers.
- Logs.
- Sitemaps.
- `robots.txt`.
- `llms.txt`, se adotado.
- Performance.
- Dados estruturados.
- Auditoria de renderização.

#### 6. Digital PR / Authority Builder

Responsável por:

- Conquistar menções externas.
- Relacionamento com jornalistas.
- Relatórios proprietários.
- Distribuição em veículos setoriais.
- Coordenação com comunidades.

#### 7. Community Manager

Responsável por:

- Monitorar Reddit, fóruns, grupos e comunidades.
- Responder perguntas.
- Capturar insights.
- Evitar práticas de spam.
- Gerenciar reputação.

#### 8. Data Analyst

Responsável por:

- Dashboard.
- Tracking de AI referrals.
- Atribuição.
- Integração com CRM.
- Análise de conversão.
- Modelagem de receita influenciada.

#### 9. SME / Especialista de assunto

Responsável por:

- Validar conteúdo técnico.
- Assinar ou revisar materiais.
- Fornecer quotes.
- Participar de webinars.
- Dar autoridade ao conteúdo.

#### 10. Legal/Compliance, quando necessário

Responsável por:

- Validar claims.
- Revisar comparativos.
- Aprovar uso de dados.
- Mitigar risco em setores regulados.

---

### 2.2. Cadência operacional

### Sprint semanal

**Segunda-feira**
- Revisão rápida de métricas.
- Prompts com queda ou erro.
- Novas menções detectadas.
- Priorização da semana.

**Terça e quarta**
- Produção/otimização de conteúdo.
- Implementações técnicas.
- Outreach de PR.
- Participação em comunidades.

**Quinta**
- QA de conteúdo.
- Validação técnica.
- Publicação.
- Atualização de links internos.

**Sexta**
- Medição parcial.
- Registro de aprendizados.
- Planejamento da próxima semana.

---

### Ciclo mensal

1. Rodada completa da biblioteca de prompts.
2. Benchmark contra concorrentes.
3. Auditoria de fontes citadas.
4. Report executivo.
5. Revisão de roadmap.
6. Atualização de páginas prioritárias.
7. Planejamento de novos ativos.
8. Priorização de PR e distribuição.
9. Revisão técnica.
10. Retrospectiva.

---

### Ciclo trimestral

1. Revisão de estratégia.
2. Repriorização de categorias.
3. Revisão de ICP e mensagens.
4. Grande estudo proprietário ou relatório.
5. Análise de impacto em pipeline.
6. Auditoria de autoridade de entidade.
7. Expansão para novos mercados/prompts.
8. Ajuste do modelo de atribuição.

---

### 2.3. Gates de qualidade

Antes de publicar ou distribuir qualquer ativo GEO, passar por gates.

#### Gate 1: Factualidade

- Afirmações verificáveis?
- Dados com fonte?
- Números atualizados?
- Claims comerciais comprováveis?
- Sem exageros?
- Comparações justas?
- Data de atualização visível?

#### Gate 2: Clareza de entidade

- A marca está descrita de forma consistente?
- A categoria está explícita?
- Produtos e soluções estão nomeados corretamente?
- Há conexão semântica com casos de uso?
- Há links internos para páginas canônicas?
- O conteúdo evita ambiguidade?

#### Gate 3: Citabilidade

- Há estatísticas?
- Há tabelas?
- Há definições curtas?
- Há quotes de especialistas?
- Há FAQs?
- Há resumo executivo?
- O conteúdo pode ser extraído facilmente por IA?

#### Gate 4: Técnica

- Página indexável?
- Sem bloqueios indevidos?
- Schema válido?
- Title e meta claros?
- Headings estruturados?
- Canonical correto?
- Sitemap atualizado?
- Boa renderização mobile/desktop?

#### Gate 5: Autoridade

- Autor identificado?
- Revisor especialista?
- Bio com credenciais?
- Links para fontes confiáveis?
- Prova social?
- Estudos de caso?
- Menções externas planejadas?

#### Gate 6: Distribuição

- Canais definidos?
- Ângulo de PR?
- Posts para comunidades adaptados?
- Vídeo ou snippet planejado?
- Outreach com lista de alvos?
- Monitoramento pós-publicação?

---

## 3) Anatomia de um report de GEO para executivos

### 3.1. Estrutura recomendada

#### 1. Sumário executivo

Responder em uma página:

- AI Share of Voice atual.
- Variação vs mês anterior.
- Principais ganhos.
- Principais perdas.
- Concorrente que mais cresceu.
- Prompts de maior valor onde ainda estamos ausentes.
- Erros factuais críticos.
- Impacto estimado em tráfego, leads, pipeline e receita.
- Próximas 3 prioridades.

---

#### 2. Scorecard executivo

Exemplo:

| Métrica | Atual | Mês anterior | Variação | Meta |
|---|---:|---:|---:|---:|
| AI Share of Voice | 24% | 18% | +6 pp | 35% |
| Presença em prompts comerciais | 42% | 31% | +11 pp | 60% |
| Citações com link | 19% | 14% | +5 pp | 30% |
| Precisão factual | 86% | 78% | +8 pp | 95% |
| Tráfego referral de AI | 3.200 | 2.400 | +33% | 5.000 |
| Leads assistidos por AI | 84 | 61 | +38% | 120 |
| Pipeline influenciado | R$ 780 mil | R$ 520 mil | +50% | R$ 1,2 mi |

---

### 3.2. KPIs de GEO

#### KPIs de visibilidade em IA

**1. AI Share of Voice**

Mede a participação da marca nas respostas para um conjunto de prompts.

Fórmula simples:

```text
AI Share of Voice = menções da marca / total de menções de marcas concorrentes
```

Fórmula ponderada:

```text
AI SoV ponderado =
Σ(presença × peso do prompt × peso da posição × peso do modelo) / total possível
```

Pesos sugeridos:

- Prompt comercial: peso 3.
- Prompt comparativo: peso 2,5.
- Prompt informacional: peso 1.
- Aparece como primeira recomendação: peso 3.
- Aparece no top 3: peso 2.
- Aparece apenas em menção lateral: peso 1.
- Com citação/link: multiplicador 1,2.
- Com descrição errada: redutor 0,5.
- Com sentimento negativo: redutor 0,5.

---

**2. Prompt Coverage**

```text
Prompt Coverage = prompts em que a marca aparece / total de prompts monitorados
```

Separar por:

- Comercial.
- Comparativo.
- Informacional.
- Reputacional.
- Implementação.
- Região.
- Persona.

---

**3. Citation Rate**

```text
Citation Rate = respostas com link/citação para a marca / respostas em que a marca aparece
```

---

**4. Answer Accuracy**

```text
Answer Accuracy = respostas factualmente corretas / total de respostas analisadas
```

Classificar erros:

- Erro de categoria.
- Erro de produto.
- Erro de preço.
- Erro de localização.
- Erro de cliente.
- Erro de feature.
- Erro de comparação.
- Informação desatualizada.

---

**5. Recommendation Rate**

```text
Recommendation Rate = respostas em que a marca é recomendada / total de prompts comerciais
```

---

**6. Source Influence Score**

Mede quanto os domínios conquistados aparecem como fontes nas respostas.

Critérios:

- Fonte citada por IA.
- Fonte tem autoridade temática.
- Fonte ranqueia no Google/Bing.
- Fonte contém menção correta.
- Fonte é recente.
- Fonte é independente.

---

### 3.3. Como visualizar Share of Voice em AI

#### Visualizações úteis

**A. Matriz prompt × concorrente**

| Prompt | Marca | Conc. A | Conc. B | Conc. C | Vencedor |
|---|---:|---:|---:|---:|---|
| melhores soluções para X | 1 | 1 | 1 | 0 | Conc. A |
| alternativa a Y | 0 | 1 | 1 | 1 | Conc. B |
| ferramenta para empresa Z | 1 | 0 | 1 | 0 | Marca |

Use intensidade de cor por:

- Presença.
- Posição.
- Sentimento.
- Citação.

---

**B. Radar por intenção**

Eixos:

- Descoberta.
- Comparação.
- Decisão.
- Reputação.
- Implementação.
- Definição.

Mostrar marca vs principais concorrentes.

---

**C. Funil de GEO**

```text
Prompts monitorados
→ Prompts onde a marca aparece
→ Prompts onde aparece no top 3
→ Prompts com citação/link
→ Prompts com descrição correta
→ Prompts que geraram tráfego/leads
```

---

**D. Heatmap por modelo**

| Modelo | Presença | Top 3 | Citação | Precisão | Sentimento |
|---|---:|---:|---:|---:|---:|
| ChatGPT | 45% | 28% | 14% | 89% | Positivo |
| Perplexity | 52% | 35% | 41% | 93% | Positivo |
| Gemini | 31% | 18% | 12% | 81% | Neutro |
| Copilot | 39% | 22% | 25% | 85% | Neutro |

---

**E. Mapa de fontes**

Visualizar:

- Quais domínios aparecem como fontes.
- Quais citam a marca.
- Quais citam concorrentes.
- Quais são controláveis, influenciáveis ou inacessíveis.

Classificação:

| Fonte | Tipo | Cita marca? | Cita concorrente? | Prioridade |
|---|---|---:|---:|---:|
| Site próprio | Própria | Sim | Não | Alta |
| G2 | Terceira | Sim | Sim | Alta |
| Reddit | Comunidade | Parcial | Sim | Alta |
| Wikipedia | Entidade | Não | Sim | Média |
| Blog setorial | Mídia | Não | Sim | Alta |

---

### 3.4. Como atribuir receita a tráfego de AI

A atribuição em GEO é imperfeita, porque muitos motores não passam referrer completo, usuários copiam URLs, usam dark social ou chegam depois via busca direta. Use modelo combinado.

#### Fontes de dados

- GA4.
- Adobe Analytics.
- Logs de servidor.
- CRM.
- HubSpot/Salesforce.
- UTMs em links próprios.
- Parâmetros em páginas distribuídas.
- Self-reported attribution no formulário.
- Call tracking.
- Ferramentas de enrichment.
- Dados de chat comercial.
- First-party cookies, respeitando privacidade.

#### Identificar tráfego de AI

Criar agrupamento de canais com referrers como:

- chatgpt.com
- chat.openai.com
- perplexity.ai
- copilot.microsoft.com
- gemini.google.com
- claude.ai
- you.com
- phind.com
- poe.com
- consensys/search vertical, quando aplicável
- outros assistentes com referral detectável

Também monitorar:

- Landing pages que recebem picos sem origem clara.
- Crescimento de direct após menções em AI.
- Busca de marca após melhora de SoV em AI.
- Conversões com resposta “ChatGPT”, “Perplexity”, “Gemini” em campo “como nos conheceu?”.

#### Modelos de atribuição

**A. Atribuição direta**

```text
Receita direta de AI = negócios fechados com primeira ou última sessão vinda de referrer AI
```

Uso: conservador.

---

**B. Atribuição assistida**

```text
Receita assistida por AI = negócios em que AI apareceu em qualquer ponto da jornada
```

Uso: mais realista para B2B.

---

**C. Atribuição por influência de prompt**

Conectar:

- Prompts com ganho de visibilidade.
- Páginas citadas por IA.
- Aumento de tráfego nessas páginas.
- Leads originados dessas páginas.
- Oportunidades no CRM.
- Receita fechada.

---

**D. Atribuição declarada**

Adicionar em formulários:

“Como você nos conheceu?”

Opções:

- Google.
- ChatGPT ou outra IA.
- Perplexity.
- LinkedIn.
- Indicação.
- Evento.
- YouTube.
- Comunidade.
- Outro.

Campo aberto complementar:

“O que você pesquisou?”

---

**E. Modelo incremental**

Comparar antes/depois:

- Prompts trabalhados vs grupo controle.
- Páginas otimizadas vs não otimizadas.
- Regiões/categorias com GEO ativo vs sem GEO.
- Variação de branded search.
- Variação de tráfego direto qualificado.
- Variação de pipeline por categoria.

---

## 4) Checklists técnicos de GEO

## 4.1. Schema.org

Schema não garante citação em IA, mas ajuda motores a entender entidade, relacionamento e tipo de conteúdo.

#### Schemas prioritários

**Para empresa**
- `Organization`
- `LocalBusiness`, se aplicável
- `Corporation`
- `Brand`
- `Product`
- `Service`
- `SoftwareApplication`, para SaaS
- `Person`, para autores e especialistas
- `WebSite`
- `WebPage`

**Para conteúdo**
- `Article`
- `BlogPosting`
- `FAQPage`
- `HowTo`
- `VideoObject`
- `Dataset`
- `Review`
- `AggregateRating`, se legítimo
- `CaseStudy`, quando suportado ou via `Article`
- `BreadcrumbList`

#### Checklist de Organization Schema

Incluir, quando verdadeiro:

- Nome oficial.
- Nome alternativo.
- URL.
- Logo.
- Descrição curta.
- Data de fundação.
- Fundadores.
- Endereço.
- País/área atendida.
- Canais sociais oficiais via `sameAs`.
- Contato.
- Identificadores externos.
- Produtos/serviços relacionados.

#### Checklist de Product/Service

- Nome do produto.
- Descrição clara.
- Categoria.
- Marca.
- Público-alvo.
- Features.
- Ofertas/preço, se público.
- Avaliações, se legítimas.
- FAQs relacionadas.
- Links para documentação.

---

## 4.2. `llms.txt`

O `llms.txt` é um arquivo proposto para ajudar modelos e agentes de IA a entenderem quais páginas são importantes, resumos e caminhos úteis de um site.

### Exemplo simplificado

```txt
# Empresa X

> Empresa X oferece software de gestão de contratos para empresas B2B.

## Páginas principais

- Sobre: https://www.exemplo.com/sobre
- Produto: https://www.exemplo.com/produto
- Preços: https://www.exemplo.com/precos
- Comparativo: https://www.exemplo.com/comparativos
- Documentação: https://docs.exemplo.com
- Relatório 2026: https://www.exemplo.com/relatorio-2026
```

### Checklist de `llms.txt`

- Colocar em `https://dominio.com/llms.txt`.
- Manter curto e útil.
- Apontar páginas canônicas.
- Incluir descrição objetiva da empresa.
- Evitar propaganda.
- Priorizar páginas de alta qualidade.
- Atualizar quando houver mudança relevante.
- Não incluir URLs bloqueadas por robots.
- Não substituir sitemap, schema ou SEO técnico.
- Monitorar logs para ver se algum crawler acessa.

### Controvérsia sobre eficácia

Pontos importantes:

- Não há adoção universal.
- Muitos modelos não declaram uso do arquivo.
- Não é protocolo oficial equivalente ao `robots.txt`.
- Pode ser ignorado por crawlers.
- Não garante indexação, citação ou preferência.
- Pode ajudar agentes, ferramentas e crawlers que optem por respeitar o padrão.
- Seu custo de implementação é baixo, mas não deve ser tratado como alavanca principal.

Recomendação prática:

> Implementar `llms.txt` como higiene técnica de baixo custo, mas priorizar conteúdo citável, autoridade externa, schema, indexação e distribuição.

---

## 4.3. Robots para crawlers de IA

O `robots.txt` controla permissões de crawling para agentes que declaram obedecer ao protocolo. Ele não garante remoção de dados já coletados nem impede uso por todos os modelos.

### Crawlers comuns

Exemplos de user-agents que empresas costumam avaliar:

- `GPTBot` — OpenAI.
- `ChatGPT-User` — navegação/ações iniciadas por usuário.
- `OAI-SearchBot` — busca/indexação da OpenAI, quando aplicável.
- `PerplexityBot` — Perplexity.
- `ClaudeBot` — Anthropic.
- `anthropic-ai` — Anthropic, dependendo do caso.
- `Google-Extended` — controle para uso em treinamento/serviços generativos do Google, sem bloquear necessariamente Google Search tradicional.
- `Googlebot` — busca tradicional.
- `Bingbot` — busca tradicional, importante para Copilot.
- `CCBot` — Common Crawl.
- `Applebot` — Apple.
- `Bytespider` — ByteDance.
- `Amazonbot` — Amazon.

### Estratégias possíveis

#### Estratégia aberta

Permitir crawlers de IA em páginas públicas.

Indicado quando:

- GEO é prioridade.
- Conteúdo é feito para descoberta.
- Baixo risco de uso indevido.
- Empresa quer maximizar presença em IA.

#### Estratégia seletiva

Permitir alguns bots e bloquear outros.

Indicado quando:

- Há preocupação com propriedade intelectual.
- Existe política jurídica específica.
- Alguns motores são mais relevantes comercialmente.

#### Estratégia restritiva

Bloquear crawlers de IA.

Indicado quando:

- Conteúdo é premium.
- Há risco regulatório.
- Há estratégia de licenciamento.
- GEO não compensa o risco.

### Exemplo: permitir busca, bloquear alguns usos de IA

```txt
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

User-agent: GPTBot
Disallow: /

User-agent: Google-Extended
Disallow: /

User-agent: CCBot
Disallow: /
```

### Exemplo: permitir GPTBot e PerplexityBot

```txt
User-agent: GPTBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /
```

### Checklist de decisão

- Quais motores geram tráfego/leads?
- Quais crawlers respeitam robots?
- Há conteúdo sensível?
- O jurídico aprova?
- SEO tradicional pode ser afetado?
- Bing/Google precisam acessar para busca?
- Páginas de conversão estão liberadas?
- Páginas premium estão protegidas por autenticação, não apenas robots?
- Logs confirmam comportamento dos bots?

---

## 4.4. Dados estruturados

Checklist:

- JSON-LD preferencialmente.
- Validar no Rich Results Test e Schema Markup Validator.
- Usar schema compatível com o conteúdo real.
- Não marcar avaliações falsas.
- Não usar FAQ se não há FAQ visível.
- Incluir `sameAs` para perfis oficiais.
- Usar `about` e `mentions` quando fizer sentido.
- Conectar páginas de produto a organização.
- Conectar autores a páginas de autor.
- Marcar vídeos com `VideoObject`.
- Marcar datasets e relatórios com `Dataset`.
- Atualizar schema quando conteúdo mudar.

---

## 4.5. Freshness

Motores generativos podem preferir fontes recentes para temas dinâmicos.

Checklist:

- Mostrar “última atualização”.
- Atualizar páginas prioritárias trimestralmente ou mensalmente.
- Atualizar estatísticas anualmente.
- Substituir dados obsoletos.
- Manter changelog em guias importantes.
- Reexecutar comparativos após mudanças de produto.
- Atualizar screenshots.
- Atualizar preços.
- Remover claims vencidos.
- Usar URLs persistentes quando possível.
- Criar relatórios anuais com edição clara: 2026, 2027 etc.

---

## 4.6. Conteúdo citável

Conteúdo citável é aquele que um modelo pode usar como evidência.

Checklist:

- Estatísticas próprias.
- Dados com metodologia.
- Tabelas.
- Rankings transparentes.
- Benchmarks.
- Definições curtas.
- Resumos executivos.
- Quotes de especialistas.
- Exemplos reais.
- FAQs objetivas.
- Estudos de caso com números.
- Gráficos com texto alternativo.
- Transcrições de vídeos.
- Arquivos HTML, não apenas PDF.
- PDFs acompanhados de página HTML resumida.
- Citações externas confiáveis.

Exemplo de bloco citável:

```text
Segundo o Relatório X 2026, com base em 1.248 empresas brasileiras, 63% das equipes de marketing B2B afirmam usar ferramentas generativas na etapa de pesquisa de fornecedores.
```

---

## 4.7. Autoridade de entidade

GEO depende de a máquina entender “quem é quem” e “por que essa entidade importa”.

Checklist:

- Consistência de nome em todos os canais.
- Perfis sociais oficiais completos.
- Wikidata, quando cabível.
- Wikipedia, apenas se houver notoriedade.
- Crunchbase, LinkedIn, GitHub, Product Hunt, G2 etc., conforme setor.
- Menções em veículos independentes.
- Autores com bios robustas.
- Especialistas participando de eventos.
- Citações de terceiros.
- Backlinks de qualidade.
- Reviews legítimos.
- Dados de empresa coerentes: fundação, sede, categoria, descrição.
- Páginas “Sobre”, “Imprensa” e “Contato” claras.
- `sameAs` no schema.
- Conteúdo assinado e revisado.

---

## 5) Como GEO difere de SEO clássico — e como integrar

### 5.1. Diferenças principais

| Dimensão | SEO clássico | GEO |
|---|---|---|
| Unidade de demanda | Palavra-chave | Prompt/tarefa/pergunta |
| Resultado alvo | Ranking e clique | Menção, recomendação, citação e clique |
| Interface | SERP | Resposta sintetizada |
| Métrica central | Posição, CTR, tráfego | AI SoV, presença, precisão, citações |
| Conteúdo | Otimizado para busca e usuário | Otimizado para extração, síntese e autoridade |
| Autoridade | Backlinks e E-E-A-T | Entidade, consenso de fontes, citações distribuídas |
| Conversão | Sessão no site | Jornada assistida, muitas vezes sem clique |
| Pesquisa | Keyword research | Prompt research + source research |
| Distribuição | Link building/conteúdo | PR, comunidades, bases de conhecimento, vídeos, reviews |
| Risco | Perder ranking | Ser omitido, descrito errado ou substituído por concorrente |

---

### 5.2. Onde SEO e GEO se integram

GEO não substitui SEO. Em geral, o melhor caminho é um **pipeline único com camadas específicas de GEO**.

#### Pipeline integrado recomendado

1. Pesquisa de mercado.
2. Keyword research.
3. Prompt research.
4. Mapeamento de entidades.
5. Arquitetura de informação.
6. Produção de conteúdo.
7. SEO on-page.
8. Otimização GEO:
   - Resumos.
   - Tabelas.
   - FAQs.
   - Dados.
   - Schema.
   - Clareza factual.
   - Páginas de entidade.
9. SEO técnico.
10. Distribuição:
   - PR.
   - Comunidades.
   - YouTube.
   - Reviews.
   - Diretórios.
11. Medição:
   - Rankings.
   - Tráfego orgânico.
   - AI SoV.
   - Referrals de IA.
   - Pipeline.
12. Iteração.

---

### 5.3. Quando separar SEO e GEO

Separar times/processos pode fazer sentido quando:

- A empresa tem alto volume de conteúdo SEO legado.
- Há forte risco reputacional em IA.
- O produto depende muito de shortlist gerada por assistentes.
- Mercado é altamente competitivo em comparativos.
- PR, comunidade e dados precisam de governança própria.
- Há múltiplos países/idiomas.
- Há compliance regulatório.

Mesmo separado, deve compartilhar:

- Calendário editorial.
- Briefs.
- Dados de performance.
- Pesquisa de intenção.
- Arquitetura do site.
- Diretrizes de marca.
- Repositório de entidades.
- CRM e atribuição.

---

## 6) Erros comuns e anti-padrões em programas de GEO

### 6.1. Erro: tratar GEO como “SEO com outro nome”

Problema:

- Só otimiza title, H1 e palavras-chave.
- Ignora prompts, fontes externas e respostas reais dos modelos.

Correção:

- Criar biblioteca de prompts.
- Medir presença em IA.
- Mapear fontes citadas.
- Otimizar para síntese e recomendação.

---

### 6.2. Erro: focar apenas no próprio site

Problema:

- Modelos usam fontes externas.
- Concorrentes dominam Reddit, reviews, mídia e diretórios.

Correção:

- Programa ativo de PR.
- Comunidades.
- Reviews.
- YouTube.
- Dados proprietários.
- Entidades externas consistentes.

---

### 6.3. Erro: criar conteúdo genérico com IA

Problema:

- Conteúdo sem dados, sem experiência e sem diferenciação.
- Não vira fonte.
- Não melhora autoridade.

Correção:

- Incluir pesquisa própria.
- Quotes de especialistas.
- Casos reais.
- Metodologia.
- Comparativos úteis.
- Demonstrações práticas.

---

### 6.4. Erro: manipular comunidades

Problema:

- Spam em Reddit/fóruns.
- Perfis falsos.
- Astroturfing.
- Risco reputacional alto.

Correção:

- Participação transparente.
- Respostas úteis.
- Declaração de afiliação.
- Monitoramento ético.
- Foco em suporte e educação.

---

### 6.5. Erro: acreditar que `llms.txt` resolve GEO

Problema:

- Implementa arquivo e espera aparecer em modelos.
- Ignora autoridade, conteúdo e distribuição.

Correção:

- Usar `llms.txt` como complemento.
- Priorizar páginas canônicas, schema, conteúdo citável e menções externas.

---

### 6.6. Erro: bloquear bots sem estratégia

Problema:

- Bloqueia crawlers de IA e depois quer aparecer em respostas.
- Bloqueia Google/Bing por engano.
- Não monitora logs.

Correção:

- Definir política por crawler.
- Separar busca tradicional de crawlers de IA quando possível.
- Validar com jurídico.
- Testar impacto.
- Monitorar logs.

---

### 6.7. Erro: medir só tráfego

Problema:

- GEO muitas vezes influencia sem clique.
- Executivos não veem impacto real.
- O programa parece menor do que é.

Correção:

- Medir AI Share of Voice.
- Medir presença em prompts comerciais.
- Medir branded search lift.
- Medir self-reported attribution.
- Medir pipeline assistido.
- Medir evolução de shortlists.

---

### 6.8. Erro: ignorar precisão factual

Problema:

- Modelo descreve produto errado.
- Cita preço antigo.
- Recomenda concorrente por uma feature que a marca também tem.
- Cria risco comercial e reputacional.

Correção:

- Monitorar erros.
- Criar páginas canônicas.
- Atualizar dados.
- Distribuir correções em fontes externas.
- Usar FAQs e schema.
- Acionar canais de feedback dos próprios motores quando disponíveis.

---

### 6.9. Erro: comparativos enviesados demais

Problema:

- Página “Marca vs Concorrente” soa como propaganda.
- Não é confiável para usuários nem para modelos.
- Pode gerar risco legal.

Correção:

- Usar critérios claros.
- Mostrar quando o concorrente é melhor.
- Atualizar periodicamente.
- Incluir fontes.
- Separar fato de opinião.
- Validar com jurídico.

---

### 6.10. Erro: não conectar GEO ao CRM

Problema:

- Não há prova de receita.
- Programa vira iniciativa de branding abstrata.

Correção:

- Criar canal “AI referral”.
- Adicionar campo “como nos conheceu?”.
- Registrar touchpoints.
- Integrar páginas GEO com campanhas e UTMs.
- Criar dashboard de pipeline influenciado.

---

## 7) Modelo prático de operação mensal de GEO

### Semana 1 — Diagnóstico e priorização

Checklist:

- Rodar prompts principais.
- Atualizar AI SoV.
- Identificar concorrentes em alta.
- Mapear fontes citadas.
- Selecionar 5 a 10 prompts prioritários.
- Abrir tickets de conteúdo, técnico e PR.

Entregáveis:

- Lista de prompts prioritários.
- Briefs.
- Backlog técnico.
- Lista de fontes-alvo.

---

### Semana 2 — Produção e otimização

Checklist:

- Criar/atualizar páginas.
- Inserir dados citáveis.
- Criar tabelas e FAQs.
- Revisar schema.
- Validar factualidade.
- Publicar conteúdo.
- Atualizar links internos.

Entregáveis:

- Páginas publicadas.
- Schema validado.
- Changelog editorial.
- Documentos de QA.

---

### Semana 3 — Distribuição e autoridade

Checklist:

- Enviar pitches para jornalistas.
- Publicar snippets em LinkedIn/YouTube.
- Responder comunidades.
- Atualizar perfis externos.
- Solicitar reviews legítimos.
- Distribuir relatório ou benchmark.
- Monitorar menções.

Entregáveis:

- Menções conquistadas.
- Posts publicados.
- Vídeos/transcrições.
- Atualizações em diretórios.
- Lista de oportunidades de PR.

---

### Semana 4 — Medição e reporte

Checklist:

- Reexecutar prompts.
- Comparar baseline.
- Atualizar dashboard.
- Medir tráfego AI.
- Cruzar com leads/CRM.
- Documentar aprendizados.
- Apresentar report executivo.
- Planejar próximo ciclo.

Entregáveis:

- Report executivo.
- Dashboard atualizado.
- Backlog priorizado.
- Recomendações do próximo mês.

---

## 8) Checklist final de implantação de um programa GEO

### Estratégia

- [ ] Categorias prioritárias definidas.
- [ ] Concorrentes mapeados.
- [ ] ICPs definidos.
- [ ] Biblioteca de prompts criada.
- [ ] KPIs aprovados.
- [ ] Política de bots definida.
- [ ] Integração com SEO planejada.

### Conteúdo

- [ ] Páginas de entidade completas.
- [ ] Páginas comerciais atualizadas.
- [ ] Comparativos honestos.
- [ ] FAQs factuais.
- [ ] Dados proprietários publicados.
- [ ] Estudos de caso com números.
- [ ] Autores e revisores identificados.
- [ ] Conteúdo com freshness.

### Técnico

- [ ] Schema.org implementado.
- [ ] Sitemap atualizado.
- [ ] Indexação validada.
- [ ] Robots revisado.
- [ ] Logs monitorados.
- [ ] `llms.txt` avaliado/implementado.
- [ ] Canonicals corretos.
- [ ] Páginas renderizáveis.

### Distribuição

- [ ] Lista de fontes citadas por IA.
- [ ] Plano de PR digital.
- [ ] Plano de comunidades.
- [ ] YouTube/transcrições.
- [ ] Diretórios e reviews.
- [ ] Wikipedia/Wikidata avaliados.
- [ ] Social proof atualizado.

### Medição

- [ ] Dashboard de AI SoV.
- [ ] Tracking de AI referrals.
- [ ] Campo de atribuição declarada.
- [ ] Integração com CRM.
- [ ] Medição de precisão factual.
- [ ] Report executivo mensal.
- [ ] Processo de iteração contínua.

---

## 9) Princípio operacional central

Um programa de GEO eficiente em 2026 não tenta “enganar” modelos. Ele constrói um ecossistema de evidências para que motores generativos consigam concluir, com confiança, que a marca:

1. Existe como entidade clara.
2. Pertence à categoria certa.
3. É relevante para determinados casos de uso.
4. É citada por fontes confiáveis.
5. Tem conteúdo próprio verificável.
6. Está atualizada.
7. É recomendável para prompts comerciais específicos.

A execução diária é menos sobre truques técnicos e mais sobre **governança de entidade, conteúdo citável, distribuição estratégica, medição de presença em respostas e conexão com receita**.
