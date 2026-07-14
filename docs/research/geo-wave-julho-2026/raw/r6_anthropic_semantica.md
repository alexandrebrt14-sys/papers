# Fundamentos Técnicos de LLMs Aplicados a GEO

## 1. Nuvem Semântica e Espaço Vetorial

### 1.1 Representação por embeddings

Um modelo de embedding (e.g., `text-embedding-3-large`, `bge-large`, `e5`) mapeia tokens/spans para vetores densos em ℝ^d (tipicamente d ∈ {768, 1024, 1536, 3072}). A função de codificação é aprendida via objetivos contrastivos ou de reconstrução, de modo que a geometria do espaço reflita relações distribucionais: dois textos que aparecem em contextos semelhantes no corpus de treino recebem vetores próximos. Isso é a materialização operacional da hipótese distribucional de Firth ("*you shall know a word by the company it keeps*").

### 1.2 Similaridade coseno

A métrica dominante é

$$
\text{sim}(a,b) = \frac{\mathbf{a}\cdot\mathbf{b}}{\|\mathbf{a}\|\,\|\mathbf{b}\|}
$$

Usa-se coseno (e não distância euclidiana) porque a **direção** do vetor carrega o significado semântico, enquanto a **magnitude** tende a correlacionar-se com frequência/comprimento — ruído para fins de recuperação. Muitos índices vetoriais normalizam L2 os vetores, o que torna coseno e produto interno (dot product) equivalentes, e a recuperação vira Maximum Inner Product Search (MIPS), acelerável por HNSW/IVF-PQ.

### 1.3 Por que proximidade marca–conceito importa

No estágio de *dense retrieval*, a query é embedada e comparada contra os vetores dos chunks. Se o vetor da sua marca/entidade está distante do vetor do conceito-alvo (e.g., "plataforma de observabilidade"), seus chunks caem abaixo do top-k e **nunca entram na janela de contexto do sintetizador** — logo, não podem ser citados. GEO opera, portanto, sobre a probabilidade de *retrieval*, que é função monotônica da similaridade coseno agregada entre a distribuição de queries do domínio e seus chunks.

### 1.4 Consolidação de entidade no espaço latente

O objetivo é reduzir a variância direcional dos vetores associados à entidade e ancorá-la próxima aos conceitos-alvo:

- **Co-ocorrência consistente**: mencionar sistematicamente `marca + categoria + atributos definidores` no mesmo span. Isso empurra o centróide da entidade em direção ao cluster do conceito, tanto no treino (memória paramétrica) quanto na indexação (memória não paramétrica).
- **Definições canônicas**: um enunciado do tipo "X é um [gênero] que [diferença específica]" (estrutura aristotélica) fornece um vetor de alta densidade factual e baixa ambiguidade, facilmente alinhável a queries definicionais.
- **Consistência inter-documento**: repetição da mesma formulação canônica em múltiplas fontes reduz o ruído e reforça o *knowledge graph* implícito que os motores extraem (desambiguação de entidade, sameAs).

---

## 2. Pipeline RAG dos Motores de Resposta

Fluxo canônico: **query understanding → query fan-out → retrieval híbrido → reranking → síntese com atribuição.**

### 2.1 Query understanding
Normalização, detecção de intenção, resolução de entidades e classificação (navegacional/informacional/transacional). *Oportunidade*: conteúdo que casa explicitamente com a intenção reformulada (e não só com a query literal) tem vantagem. Cobrir variantes de intenção sobre o mesmo tópico amplia o *matching*.

### 2.2 Query fan-out (decomposição)
A query original é expandida em N sub-queries (decomposição de aspectos, reformulações, questões implícitas). Ex.: "melhor CRM para B2B" → {preço, integrações, segurança, casos de uso, alternativas}. *Oportunidade*: **cobertura de sub-queries**. Cada sub-query é um slot de recuperação independente; conteúdo que responde exaustivamente aos aspectos previsíveis do fan-out captura mais slots.

### 2.3 Retrieval híbrido (BM25 + dense)
- **BM25** (esparso, lexical): sensível a *term matching* exato, TF-IDF saturado; premia presença de termos-chave literais e keywords raras (IDF alto).
- **Dense** (denso, semântico): captura paráfrase e sinonímia via embeddings.
- Fusão tipicamente via **Reciprocal Rank Fusion (RRF)**.

*Oportunidade dupla*: otimizar simultaneamente para vocabulário exato (nomes técnicos, termos canônicos → BM25) **e** para similaridade semântica (definições, contexto → dense). Ignorar o lado lexical é erro comum: entidades e termos específicos precisam aparecer literalmente.

### 2.4 Reranking
Um *cross-encoder* (e.g., estilo `bge-reranker`, `Cohere Rerank`) reprocessa os top-k candidatos com atenção conjunta query–passagem, produzindo scores de relevância muito mais precisos que a similaridade bi-encoder. *Oportunidade*: **alinhamento direto pergunta-resposta** no nível do parágrafo — o cross-encoder recompensa passagens que respondem a query de forma autocontida, não apenas topicamente relacionadas.

### 2.5 Síntese com atribuição
O LLM gera a resposta condicionada aos top-k passages e emite citações. *Oportunidade*: ver Seção 5. A citação exige que o trecho seja (a) recuperado, (b) sobrevivente ao rerank, (c) selecionado na síntese.

---

## 3. Chunking e Self-Containment em Nível de Passagem

### 3.1 Mecânica do chunking
O indexador segmenta a página em chunks (por tamanho de token com overlap, ou — melhor — por fronteiras estruturais: headings, parágrafos, itens de lista, células/linhas de tabela). Cada chunk é embedado **isoladamente**. A implicação é crítica: **o chunk é a unidade atômica de recuperação e citação**, não a página.

### 3.2 Por que a estrutura determina recuperabilidade
Um parágrafo que depende de contexto anafórico externo ("como mencionado acima", "essa técnica") produz um vetor semanticamente diluído e, isolado, é inútil para o sintetizador — que não tem o "acima". Requisitos de **passage-level self-containment**:

- **Parágrafos autocontidos de 2–4 frases**: densos o suficiente para carregar uma resposta completa, curtos o suffiente para não diluir o embedding com múltiplos tópicos (que empurram o vetor para um centróide médio, reduzindo similaridade com qualquer query específica).
- **Headings descritivos**: frequentemente prependados ao chunk como contexto; um H2 na forma de pergunta ("Como funciona X?") alinha o chunk a queries interrogativas.
- **Tabelas e FAQs**: estruturas de alta densidade factual, com pares atributo–valor / pergunta–resposta que mapeiam quase 1:1 para sub-queries do fan-out. FAQs são o formato de maior "citabilidade" por construção.
- **Repetição de entidade**: cada chunk deve nomear a entidade explicitamente (sem depender de pronomes), pois será lido fora de contexto.

---

## 4. Memória Paramétrica vs. Recuperação

### 4.1 Duas fontes de resposta
- **Memória paramétrica**: conhecimento comprimido nos pesos durante o pré-treino. Ativada para fatos estáveis, populares, presentes redundantemente no corpus. Sem citação, sujeita a *staleness* (cutoff) e alucinação.
- **Recuperação (não paramétrica)**: contexto injetado em tempo de inferência via RAG. Ativada para queries recentes, de nicho, ou quando o sistema tem gate de *retrieval*.

### 4.2 Gating
Sistemas modernos decidem *quando* recuperar (retrieval é caro/latente). Fatos de alta confiança paramétrica podem dispensar busca; incerteza/atualidade/especificidade disparam recuperação.

### 4.3 Implicação dupla para GEO
Para maximizar presença, é preciso estar em **ambos** os substratos:
1. **Corpus de treino**: presença ampla, redundante e consistente em fontes crawladas → maior probabilidade de a entidade ser "memorizada" nos pesos e emergir mesmo sem busca. Efeito de longo prazo, ligado a cobertura e autoridade histórica.
2. **Índice de busca**: chunks recuperáveis e frescos → presença nas respostas *grounded*. Efeito de curto prazo, sensível a estrutura e atualização.
Conteúdo bem estruturado mas obscuro perde no substrato paramétrico; conteúdo popular mas mal estruturado perde no substrato de recuperação.

---

## 5. Como o LLM Seleciona o que Citar na Síntese

Dado o conjunto de passagens no contexto, a seleção efetiva é governada por:

- **Fluência / encaixe generativo**: passagens cuja formulação se integra com baixa perplexidade ao texto gerado são preferencialmente incorporadas e citadas. Prosa clara e afirmativa > texto fragmentado ou promocional.
- **Densidade factual**: passagens com fatos concretos, números, datas, definições verificáveis ancoram melhor a geração e reduzem risco de contradição — o modelo tende a citá-las para *grounding*.
- **Alinhamento com a query (aboutness)**: correspondência direta e específica com a intenção; responder *a pergunta exata* supera relevância tópica difusa.
- **Autoridade percebida**: sinais de fonte (domínio, consistência com outras passagens recuperadas, corroboração cruzada). Convergência entre múltiplas fontes recuperadas aumenta a confiança e a probabilidade de citação.

Nota: a citação é condicional à sobrevivência nas etapas 2.3–2.4. Otimizar apenas a "citabilidade" sem garantir recuperação é ineficaz.

---

## 6. Métricas Mensuráveis Derivadas

| Métrica | Definição operacional | Como medir |
|---|---|---|
| **Embedding similarity score (marca↔tópico)** | Coseno médio entre o vetor da entidade e vetores dos conceitos-alvo | Embedar N formulações da marca e M queries do domínio; computar matriz de similaridade; monitorar o centróide ao longo do tempo |
| **Cobertura de sub-queries do fan-out** | Fração das sub-queries previsíveis que têm ≥1 chunk com score de relevância acima de threshold | Simular fan-out (decompor query semente em sub-queries via LLM) e rodar retrieval local contra seu corpus |
| **Taxa de trechos autocontidos** | % de chunks que respondem a alguma query sem dependência de contexto externo | Classificar chunks (LLM-as-judge) por self-containment + presença explícita de entidade |
| **Retrieval hit rate @k** | P(algum chunk seu ∈ top-k) para queries-alvo | Índice espelho (BM25+dense) reproduzindo o pipeline |
| **Rerank survival rate** | P(chunk permanece no top-n pós-reranker \| entrou no top-k) | Aplicar cross-encoder aos candidatos |
| **Citation share / share of voice generativo** | Frequência de citação da marca nas respostas geradas por um painel de queries | Amostragem sistemática de motores (perplexity, AI Overviews, etc.) |
| **Densidade factual do chunk** | Fatos verificáveis por 100 tokens | Extração de claims + contagem normalizada |

### 6.1 Encadeamento causal das métricas
`similarity ↑ → hit rate@k ↑ → rerank survival ↑ → citation share ↑`, modulado por `self-containment` e `densidade factual` nas duas últimas transições. O funil deve ser instrumentado ponta a ponta: um gargalo em qualquer estágio anula ganhos a montante — otimizar densidade factual não adianta se a similaridade mantém o chunk fora do top-k.
