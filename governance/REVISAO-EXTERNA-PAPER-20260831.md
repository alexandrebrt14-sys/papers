# Revisão externa adversarial do paper BRGEO-1 · 2026-08-31

**Severidade**: Alta. Quatro achados barram a submissão, um deles porque um número publicado no manuscrito foi refutado por medição, e dois atingem a proposição central do trabalho.
**Status**: Achados registrados e verificados contra o repositório e o banco. A reescrita do manuscrito não foi feita nesta sessão.
**Data**: 2026-08-31
**Escopo**: manuscrito `docs/research/methods-paper/MANUSCRIPT.md`, implementação de referência `scripts/brgeo1_index.py`, base bibliográfica do projeto.
**Documento irmão**: `governance/HEALTH-CHECK-COLETA-20260831.md`, que registra os achados do instrumento e da coleta.

---

## Sumário

A revisão foi conduzida em modo adversarial, procurando o que derruba o paper em vez do que o confirma. Produziu três classes de achado.

A primeira barra a submissão antes de qualquer leitura de mérito: o manuscrito não tem uma única referência bibliográfica, alega um pré-registro que não existe nos termos em que a palavra é usada na literatura, viola a regra de conformidade que ele próprio especifica, e sustenta a conclusão da seção 7 num teste estatístico que mede a coisa errada. O último item entrou nesta classe durante a revisão: o teste correto foi rodado em 31-08 e refutou a afirmação publicada.

A segunda ataca a substância. A justificativa matemática da média geométrica está errada, a implementação de referência aplica um limiar que não aparece na especificação e que muda o índice, e a especificação deixa de fora dois parâmetros que alteram o resultado. Um item desta classe mudou de estado para melhor: a anomalia do Gemini, que o revisor apontou como não investigada, foi investigada em 31-08 e o resultado reforça a tese central.

A terceira não é defeito, é posicionamento. A citação fundadora do campo estava errada em quatro documentos canônicos, e o campo deixou de estar vazio entre março e julho de 2026. O paper precisa se situar contra cinco trabalhos que não existiam quando a janela abriu.

---

## Classe 1. Bloqueadores de submissão

### D1. O paper não tem nenhuma referência bibliográfica

Zero citações no manuscrito atual. Para periódico Q1 isso é rejeição na triagem editorial, antes de qualquer avaliação de mérito, porque um trabalho sem posicionamento na literatura não é avaliável como contribuição.

**Alvo**: 40 a 60 referências, cobrindo medição de citação em motores generativos, metodologia de instrumento e viés de medição, avaliação de alucinação, e a literatura de índices compostos que sustenta a discussão da seção 7.

A base para isso existe em parte: o levantamento do item E2 deste documento entrega seis trabalhos verificados, e a correção do item E1 entrega a referência fundadora com registro correto.

### D2. O paper viola a conformidade que ele mesmo especifica

O parâmetro P4 exige versão de modelo pinada em toda observação. As tabelas do manuscrito nomeiam produtos: "ChatGPT", "Claude", "Gemini". Nomear produto é exatamente a prática que P4 declara insuficiente, e um revisor atento encontra a contradição na primeira leitura das tabelas.

Os snapshots existem e estão corretos em `docs/METHODOLOGY_V2.md` §3.1 (`gpt-4o-mini-2024-07-18`, `claude-haiku-4-5-20251001`, `gemini-2.5-pro`, `sonar`, `grok-4.6`). Nunca chegaram ao manuscrito.

Correção: toda tabela do paper que nomeia braço passa a carregar o identificador pinado, e as fronteiras de estrato da seção 6.1 passam a nomear as versões dos dois lados de cada fronteira.

### D3. A alegação de pré-registro não é um pré-registro

Duas coisas erradas na mesma alegação.

Repositório git sob controle do autor não é registro independente com carimbo de tempo de terceiro. A propriedade que faz um pré-registro valer é a impossibilidade de alteração posterior pelo próprio pesquisador, e um repositório que o autor administra não tem essa propriedade, mesmo com histórico de commits assinado.

O marco declarado também está errado. O texto situa o registro "antes do fechamento da janela", e pré-registro precede a **coleta**, não o fechamento. Um plano registrado depois de o pesquisador já ter visto dados não cumpre a função para a qual pré-registro existe.

Correção: remover a alegação ou reescrevê-la para o que é verdade, que é plano de análise documentado publicamente em data verificável, sem chamar isso de pré-registro. Se o registro independente for desejado para a próxima janela, ele precisa acontecer antes de a coleta começar.

### D8. A seção 7.2 do manuscrito está factualmente incorreta

Este item entrou como correção de substância e virou bloqueador depois que a medição foi feita. O manuscrito publica um número e uma conclusão que o teste correto refuta.

**O que o paper afirma hoje.** A seção 7.2 apresenta rho de Spearman de 0,980 entre o índice GCI e a cobertura simples, e a 7.3 conclui que "duas escolhas defensáveis de agregação produzem quase a mesma ordenação". A revisão observou que comparar um índice com o componente que domina sua variância logarítmica não mede arbitrariedade de agregação. A observação estava certa, e o teste correto mostra o contrário do que o paper diz.

**Agregações alternativas entre si**, rho de Spearman, n = 66:

|  | geométrica | aritmética | harmônica | ponderada |
|---|---:|---:|---:|---:|
| geométrica (GCI) | 1,000 | 0,816 | 0,983 | 0,787 |
| aritmética | 0,816 | 1,000 | 0,734 | 0,984 |
| harmônica | 0,983 | 0,734 | 1,000 | 0,706 |
| ponderada 60/25/15 | 0,787 | 0,984 | 0,706 | 1,000 |

Duas agregações igualmente defensáveis chegam a discordar com rho de 0,706. O desacordo entre fórmulas é bem maior que os 0,982 de acordo entre o GCI e a cobertura, que era a evidência oferecida.

**Cada agregação contra a cobertura simples**: geométrica 0,982, harmônica 1,000, aritmética 0,728, ponderada 0,700. A harmônica reproduz a ordenação da cobertura de forma exata, porque é a mais dominada pelo menor componente. As agregações que não têm essa dominância divergem bastante.

**Por que, decomposição da variância de log(GCI).** Contribuição de cada componente calculada como Cov(log X, log GCI) dividido por 3 · Var(log GCI), somando 100%:

| Componente | var(log) | Contribuição |
|---|---:|---:|
| Cobertura | 4,490 | 74,7% |
| Amplitude | 0,306 | 16,9% |
| Proeminência | 0,198 | 8,4% |

A cobertura varia por ordens de grandeza entre entidades; proeminência e amplitude ficam confinadas em faixa estreita. A média geométrica herda essa dominância por construção. O rho de 0,982 entre GCI e cobertura não é achado empírico sobre agregação, é consequência algébrica de a cobertura responder por três quartos da variância do índice.

**Deslocamento de posto, GCI contra cobertura**: mediana de |Δ| igual a 2, p90 igual a 6, máximo igual a 10, e apenas 7 das 66 entidades mantêm o posto exato. O manuscrito afirma que "o movimento é de uma ou duas posições, não um retrato diferente do mercado". A mediana sustenta a frase; o p90 de 6 e o máximo de 10 em 66 entidades, não. A frase sai e entram os quatro números.

**Reprodução.** Os rhos, a decomposição e os deslocamentos saem de `scripts/brgeo1_index.py::componentes` sobre o banco da run `33404549276`, janela de 200 caracteres, as quatro verticais, entidades com cobertura acima de zero (n = 66). A ponderada usa 0,6·C + 0,25·P + 0,15·B, escolha arbitrária declarada como tal: ela existe no teste justamente para mostrar que uma ponderação plausível diverge.

**A conclusão do paper sobrevive, com argumento melhor.** A tese de que o padrão deve gastar autoridade nas condições de medição em vez da fórmula continua correta, por um motivo mais forte que o alegado. A agregação não é irrelevante. Ela é instável entre escolhas defensáveis, com rho descendo a 0,706, e não há base nos dados para preferir uma delas, porque elas diferem sobretudo em quanto peso dão a componentes que quase não variam. A janela move um motor em 23,8 pontos percentuais com mecanismo agora compreendido e critério declarável. Desacordo grande e resolvível de um lado, desacordo grande e arbitrário do outro. O padrão fixa o que dá para fixar.

Este é ajuste de fato, não de ênfase, e por isso entra como bloqueador ao lado de D1 e D3. Um número publicado que a própria equipe já refutou não pode acompanhar uma submissão.

---

## Classe 2. Correções de substância

### D4. A justificativa da média geométrica está errada

O manuscrito afirma que a média geométrica é escolhida por ser não-compensatória, e que ausência em um motor não pode ser compensada por força em outro.

A propriedade só vale no limite. Com seis motores no painel, ausência total em um deles dá B = 5/6, e cobertura ou proeminência maiores compensam a perda com folga. O termo B só zera o índice quando a entidade está ausente de todos os motores, caso em que qualquer agregação também zera.

Correção: trocar a justificativa por duas que são verdadeiras e mais modestas. A média geométrica é invariante a reescalonamento dos componentes, o que importa porque C, P e B têm escalas naturais diferentes. E penaliza desequilíbrio de forma gradual, favorecendo entidades com os três componentes próximos sobre entidades que compensam um componente fraco com outro muito forte. Nenhuma das duas exige a alegação forte que está no texto.

### D5. A implementação de referência não implementa a especificação

`scripts/brgeo1_index.py` define `MIN_OBS_PARA_ENTRAR_NO_PAINEL = 500` (linha 53) e filtra o painel por esse limiar (linha 92). O limiar não aparece em lugar nenhum do manuscrito, e altera B, que é um terço do índice.

A consequência foi verificada em 31-08 na vertical fintech. O Grok tem 96 observações e **fica de fora** do painel. O Groq, aposentado em 19-08 por retirada do modelo pelo provedor, **entra** com 3.552. O índice de referência roda sobre um painel que inclui um motor morto e exclui um motor vivo.

Para um paper que propõe padrão de medição, este é o achado mais constrangedor da classe: a implementação que serve de referência para terceiros aplica uma regra de elegibilidade não declarada, que é a categoria exata de problema que o paper denuncia.

Correção: o limiar vira parâmetro declarado, com valor publicado junto do índice, ou some do código. E a elegibilidade precisa de regra que trate braço descontinuado, porque contagem acumulada de observações favorece motores que rodaram por mais tempo, independentemente de estarem vivos.

### D6. A regra de correspondência é anunciada como problema e não vira parâmetro

A seção 2.2 enumera três parâmetros que circulam sem declaração: janela de observação, regra de correspondência e tratamento do caso de recusa. A seção 3.1 formaliza cinco parâmetros, e a regra de correspondência não está entre eles.

O buraco derruba a proposição central do padrão. Duas implementações que usem regras de correspondência diferentes, uma com limite de palavra rigoroso e outra com correspondência de substring, ou uma que resolva aliases e outra que não, produzem números diferentes sobre as mesmas respostas enquanto declaram conformidade sob os cinco parâmetros idênticos. Um padrão que permite isso não entrega comparabilidade, que é a única coisa que um padrão de medição promete.

A regra existe no projeto e está bem documentada em `docs/METHODOLOGY_V2.md` §4.1, com limite de palavra, dual-pass NFC mais NFKD, aliases e contextos de parada. O trabalho é elevá-la a parâmetro declarado do padrão, com os componentes que uma implementação precisa publicar para ser comparável.

### D7. Falta o parâmetro de configuração de geração

Temperature, top_p, seed, limites de saída, esforço de raciocínio e system prompt não são declarados em lugar nenhum do manuscrito.

A própria seção de eventos de série prova que isso importa. Um dos quatro eventos listados foi causado por mudança de `reasoning_effort` num braço, e outro por `GEMINI_THINKING_BUDGET=0` em 17-06. O paper registra que a configuração de geração altera a série e não a exige de quem adota o padrão.

Correção: sexto parâmetro declarado, cobrindo a configuração de geração completa por braço, com a exigência de que qualquer mudança nela seja tratada como fronteira de estrato.

### D9. A anomalia do Gemini, investigada em 31-08

O revisor apontou que o Gemini reporta 1,8% de taxa de citação contra 25,8% do Claude, fator de 14, e que o paper não investiga. A investigação foi feita no mesmo dia, motivada por este apontamento, e o resultado é bom para o paper.

Não é extrator quebrado. É a janela.

Fração de respostas que abrem com preâmbulo, contra a taxa de citação de cada braço:

| Braço | n | Abre com preâmbulo | Taxa de citação |
|---|---:|---:|---:|
| Gemini | 14.587 | 79,6% | 1,8% |
| Perplexity | 7.436 | 9,2% | 75,7% |
| Grok | 350 | 4,0% | 32,3% |
| ChatGPT | 14.976 | 2,1% | 17,2% |
| Groq | 14.208 | 1,1% | 8,5% |
| Claude | 14.842 | 0,0% | 25,8% |

Critério de medição, que precisa acompanhar o número: preâmbulo é definido por regex ancorada no início da resposta (`^`), casando saudação, hedge, reformulação da pergunta e auto-referência de modelo. Medido sobre `response_text` das linhas canônicas do banco baixado da run `33404549276`. A regex é critério de medição e vai declarada junto do resultado, porque este documento não pode cometer o pecado que denuncia.

Amostras reais das aberturas do Gemini: "It's tricky to name a single company that dominates...", "Excelente pergunta! O cenário de tecnologia e TI no Brasil é extremamente diversificado...", "É muito difícil prever com certeza qual empresa dominará...".

O Gemini gasta os 200 caracteres da janela em preâmbulo, e as entidades nunca chegam a aparecer dentro do trecho observado.

**Por que isso reforça a tese central.** O motor com mais preâmbulo do painel é paramétrico, com 79,6%, e o motor RAG tem pouco, 9,2%. O estilo de abertura que faz a janela morder é propriedade do modelo, não da arquitetura, e não é dedutível da classe. Some o último resquício da explicação "motores RAG adiam a nomeação", que a seção 4.4 do manuscrito ainda carrega e que a verificação de offset relativo já tinha derrubado. Entra no lugar uma afirmação mais forte e mais geral: a janela interage com o estilo de resposta de cada modelo de um jeito que não se deduz da arquitetura, e é exatamente por isso que ela precisa ser declarada em vez de presumida inócua. Não existe regra de bolso que permita ao leitor estimar o efeito sem medir.

**Ressalva obrigatória.** A taxa de 1,8% do Gemini não significa "o Gemini cita pouco". Significa "o Gemini cita pouco nos primeiros 200 caracteres". Quanto ele citaria na resposta inteira é desconhecido, porque o texto além da janela nunca foi gravado. O número correto de reportar é o condicional, com a janela declarada junto, e o paper não pode afirmar nada sobre o comportamento do Gemini fora dela.

**Controle a favor da leitura acima.** Entre as observações em que o Gemini efetivamente cita, 23,0% das primeiras menções caem depois do caractere 150, proporção parecida com a do ChatGPT (24,5%) e menor que a do Claude (36,1%). Quando o Gemini chega a nomear dentro da janela, a distribuição da posição não é anômala. O anômalo é ele raramente chegar lá.

### D10. Ameaça de construto não medida

A comparação entre modo JSON e linguagem natural nunca rodou em escala. A tabela `dual_responses` está vazia.

O risco é dimensionável pelo que já se sabe do eixo vizinho. A janela de observação produziu 23,8 pontos percentuais de diferença num braço. Se o formato de resposta produzir efeito da mesma ordem, o protocolo estará fixando cinco eixos enquanto um sexto, de magnitude desconhecida, corre solto, e a conformidade sob os cinco não garante comparabilidade nenhuma.

Correção: rodar o pareamento em escala suficiente para estimar o efeito, ou declarar o formato de resposta como parâmetro fixo do padrão e reportar a ameaça como limitação explícita, com a magnitude declarada como não medida.

### D11. Falta evidência de reprodutibilidade entre implementações

Para um padrão de medição, a evidência esperada é o exercício interlaboratorial: duas implementações independentes rodando sobre as mesmas respostas, com a discrepância entre elas reportada. É assim que padrões de medição em outras áreas demonstram que fazem o que prometem.

Nunca foi feito neste projeto. Sem ele, a proposição central do padrão, que é a de que conformidade produz comparabilidade, não tem uma única observação a favor. O item conversa diretamente com D6: enquanto a regra de correspondência não for parâmetro declarado, um exercício interlaboratorial provavelmente falharia, e a falha seria informativa.

---

## Classe 3. Reposicionamento

### E1. A citação fundadora do GEO estava errada em quatro documentos canônicos

Os documentos diziam "Aggarwal SIGIR 2023", e a base de conhecimento do projeto carregava o DOI 10.1145/3539618.3594249. Venue, ano e DOI errados, e o DOI não resolve para o trabalho.

Registro correto, conferido contra arXiv e dblp:

> Aggarwal, P., Murahari, V., Rajpurohit, T., Kalyan, A., Narasimhan, K. & Deshpande, A. (2024). *GEO: Generative Engine Optimization.* KDD '24, pp. 5-16. DOI 10.1145/3637528.3671900. Preprint arXiv:2311.09735.

Corrigido no commit `3cc4810`.

A origem foi rastreada até `docs/research/geo-knowledge-2026/01-perplexity-academic-papers-llm-citations.md`, output bruto de pesquisa que confabulou DOI e título. O arquivo ficou com aviso de correção no topo em vez de ser apagado, porque um output de pesquisa com erro documentado tem valor de registro e um arquivo removido não impede que o erro volte a ser copiado de outro lugar.

A lição que sai daqui vale para todo o projeto: output bruto de LLM não é fonte bibliográfica, e todo identificador precisa resolver antes de entrar em documento canônico.

### E2. O campo deixou de estar vazio entre março e julho de 2026

Quando a janela v2 abriu, medição de citação em motores generativos era terreno com pouco trabalho acadêmico. Cinco meses depois há pelo menos cinco trabalhos atacando o problema, todos propondo protocolo ou framework, e o paper precisa se situar contra eles.

Referências verificadas, com páginas abertas e metadados conferidos:

| Trabalho | Identificador | Data | Verificação |
|---|---|---|---|
| Sielinski, R. (2026). *Quantifying Uncertainty in AI Visibility: A Statistical Framework for Generative Search Measurement.* | arXiv:2603.08924 | v1 09-03-2026, v3 26-08-2026 | Página aberta, metadados conferidos |
| Schulte, J., Bleeker, M. & Kaufmann, P. (2026). *Don't Measure Once: Measuring Visibility in AI Search (GEO).* | arXiv:2604.07585 | 08-04-2026 | Página aberta, metadados conferidos |
| Zhang, K., He, X. & Yao, J. (2026). *From Citation Selection to Citation Absorption: A Measurement Framework for Generative Engine Optimization Across AI Search Platforms.* | arXiv:2604.25707 | 28-04-2026 | Página aberta, metadados conferidos |
| Kumar, P. (2026). *Generative Engine Optimization at Scale: Measuring Brand Visibility Across AI Search Engines.* | arXiv:2606.20065 | 18-06-2026 | Página aberta, metadados conferidos. Ressalva: autor com afiliação declarada a fornecedor |
| Varga, Z. (2026). *Per-Entity Bias Mapping for AI Visibility: Why Brand Mentions Require Entity-Specific Calibration.* | arXiv:2606.21595 | 19-06-2026 | Página aberta, metadados conferidos |
| Martinez, O. (2026). *Optimizing Visibility in Generative Engines: A Critical Survey of Generative Engine Optimization (2023-2026).* | arXiv:2607.14035 | 15-07-2026 | Página aberta, metadados conferidos |

O survey de Martinez muda o custo de não citar: existe uma revisão crítica do campo publicada seis semanas antes desta sessão, e um manuscrito que a ignora sinaliza desconhecimento da literatura mais recente.

### E3. Três lacunas confirmadas, que sustentam a originalidade

**Escopo da busca, declarado**: inglês, arXiv, ACL Anthology, dblp e web aberta, com múltiplas formulações de consulta. Ausência de resultado não é prova de inexistência, e as três lacunas abaixo são afirmações sobre o que a busca não encontrou dentro desse escopo.

**Primeira lacuna: a janela de observação de leitura nunca foi isolada como variável controlada.** O que existe é adjacente e distinto. Schulte trata de janela temporal, quantas vezes e ao longo de quanto tempo medir. Sielinski trata de tamanho de amostra e da incerteza estatística que dele decorre. Encarnación et al. (arXiv:2608.06202) tratam de modalidade de acesso, qual interface do motor é consultada. Nenhum trata de quanto do texto da resposta o instrumento lê antes de decidir se houve citação.

**Segunda lacuna: entidades fictícias existem como alvo de teste e nunca como instrumento de calibração do próprio medidor.** PhantomBench (arXiv:2606.11105) e HalluLens (ACL 2025) usam entidades inexistentes para medir a propensão do modelo a alucinar, que é uma pergunta sobre o modelo. Usá-las para estabelecer o piso de falso-positivo do instrumento de medição, dentro da mesma run que produz a taxa de citação, é pergunta sobre o medidor, e não foi encontrada.

**Terceira lacuna: não há literatura revisada por pares sobre "share of voice" de marca em respostas de LLM.** O que existe é material de fornecedor, com metodologia não publicada e incentivo comercial no resultado. A lacuna é evidência citável da premissa do paper, porque descreve exatamente o vácuo que um padrão aberto de medição vem ocupar.

---

## Prioridade de trabalho

| Ordem | Item | Por quê |
|---|---|---|
| 1 | D8 | Número publicado já refutado por medição própria. Reescrita das seções 7.2 e 7.3 antes de qualquer coisa. |
| 2 | D1, D3 | Barram a triagem. D3 é também questão de integridade. |
| 3 | D6 | Sem a regra de correspondência como parâmetro, a proposição central não se sustenta. |
| 4 | D5 | A implementação de referência precisa implementar a especificação antes de terceiros a usarem. |
| 5 | D2, D4, D7 | Correções de texto e de especificação, sem pesquisa nova. |
| 6 | E1, E2, E3 | Reposicionamento e construção das 40 a 60 referências. |
| 7 | D10, D11 | Exigem coleta e implementação novas. Podem entrar como limitação declarada nesta submissão. |

Fora desta lista, e registrado no documento irmão: a seção 4.4 do manuscrito afirma um mecanismo de viés da janela que os dados contradizem, e a seção 5.2 chama a regex de recusa de conservadora sem ter demonstrado isso. As duas correções estão em `governance/HEALTH-CHECK-COLETA-20260831.md`.

---

**Documento versão 1.0 · 2026-08-31**
