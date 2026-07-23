# Wave Julho-22C 2026 · GEO no Brasil, regulatório e segurança agêntica (22-jul-2026)

**Data:** 22-jul-2026 · **Método:** 1 × Perplexity `sonar-deep-research` (Brasil) + 1 subagente web com fontes primárias brasileiras e docs oficiais de segurança. Proveniência em `raw/` (pplx-brasil.md, web-brasil-seguranca.md).

**Precedência:** cadeia vigente: **Julho-22C §7 > Julho-22B §7 > Julho-22 §7 > Julho §7 > Wave 19 §7 > 15B §8**. Esta wave preenche a lacuna Brasil/PT-BR que a Wave Julho-22 §8.1 declarou inexplorada na literatura, e abre o eixo de segurança agêntica (o outro lado do "agent-ready").

---

## 0. TL;DR — o que muda para uma operação de GEO brasileira

1. **O Brasil é mercado de primeira linha em IA generativa, não periferia.** 3º maior usuário de ChatGPT do mundo (relatório da OpenAI, ago/2025, via imprensa: ~140M mensagens/dia), Modo IA em pt-BR desde 08-set-2025 (fonte primária Google Brasil), e rollout do checkout Universal Commerce Protocol no AI Mode reportado desde 19-mai-2026 [imprensa especializada; confirmação primária do Google pendente]. A tese comercial "GEO em pt-BR é superfície corrente" (Wave Julho) ganha corpo documental (§1).
2. **A imprensa brasileira já monetiza IA — e litiga.** Estadão×Google (dez/2025), Folha×Google, Folha+UOL×OpenAI (mai/2026, encerrando o processo da Folha); frente ANJ+Abert+Aner notificou as big techs (dez/2025); CADE abriu processo administrativo sobre o Google e jornalismo (abr/2026). Earned media brasileiro tem agora um mapa de quem está dentro e quem está em guerra (§3).
3. **Marco legal da IA segue NÃO aprovado** (PL 2338/2023 parado na Câmara em 22-jul-2026, com indício de novo adiamento para dez/2026); enquanto isso valem LGPD + ANPD (sandbox de IA ativo) + CONAR (guia de influenciadores com responsabilidade solidária por conteúdo de IA, vigente desde 01-jun-2026) + ECA Digital (§4).
4. **Mercado de GEO brasileiro é nascente e barato de liderar**: poucas agências estruturadas [números do próprio setor, secundários], nenhum painel acadêmico pt-BR (Wave Julho-22 §8.1), eventos grandes ainda sem trilha nomeada de GEO. Janela de autoridade aberta (§5).
5. **Agent-ready tem um lado B: segurança.** Prompt injection indireta via conteúdo web é ataque demonstrado e em estado selvagem (Comet/Brave, CometJacking, Atlas); a OpenAI admite que "dificilmente será totalmente resolvido". Sites que recomendamos tornar agent-ready precisam do checklist de não-virar-vetor (§6). Identidade de agentes (Web Bot Auth/IETF, Cloudflare Signed Agents) é o padrão emergente para distinguir agente legítimo de scraper (§6.3).

## 1. Google no Brasil (fontes primárias e imprensa nacional)

- Modo IA em pt-BR desde **08-set-2025** (Gemini 2.5 customizado, multimodal; blog oficial do Google Brasil). Em I/O 2026: AI Mode com Gemini 3.5 Flash default e busca agêntica, rollout incluindo o Brasil.
- **Universal Commerce Protocol (UCP)**: checkout direto no AI Mode/app Gemini, rollout global reportado desde **19-mai-2026** nos mercados com AI Mode, Brasil incluído [imprensa especializada (Mobile Time, CNDL); confirmação primária do Google não localizada — verificar antes de citar em copy]. Nota de nomenclatura para não confundir protocolos: **UCP** é a iniciativa de checkout do ecossistema Google; **ACP (Agentic Commerce Protocol)** é o padrão aberto OpenAI+Stripe do Instant Checkout do ChatGPT — protocolos distintos, mantenedores distintos, maturidades distintas.
- Evento do Google em SP (**24-mar-2026**, Mobile Time): estratégia declarada de transição "B2C → B2A (business-to-agents)"; agentes em português para Ads/Analytics; anúncios contextuais dentro de conversas de IA; agendamento de reservas no AI Mode. Requisito técnico citado: dados estruturados via Merchant Center e Ads Data Manager. NÃO existe um "Google for Brasil 2026" nomeado nas fontes [lacuna declarada].
- Recursos agentic de reserva restritos a planos AI Pro/Ultra [secundário].

## 2. Adoção no Brasil (números com fonte e data)

Aviso metodológico: as linhas abaixo vêm de universos, amostras e perguntas DIFERENTES (vendor sobre si, instituto de pesquisa, painéis de mercado) — usar cada uma com sua fonte, nunca compor num índice único.

| Fato | Número | Fonte | Rótulo |
|---|---|---|---|
| Posição do Brasil em uso de ChatGPT | 3º do mundo; ~140M mensagens/dia (~7% do global) | Relatório da OpenAI, ago/2025 (não acessado diretamente; via Fast Company Brasil, Softex) | vendor sobre si, via secundária |
| Devs brasileiros na API OpenAI | 2º do mundo | idem | vendor sobre si, via secundária |
| Uso de ferramenta com IA | 93% dos brasileiros; só 54% entendem o termo. Atenção: inclui IA embutida (recomendação, filtros etc.) — NÃO equivale a uso consciente de chatbot nem a busca por IA | Datafolha + Observatório Fundação Itaú, campo jul-ago/2025 | CONFIRMADO |
| Desigualdade de adoção | IA generativa: 69% classe A vs 16% classes D/E | idem | CONFIRMADO |
| IA no processo de compra | 46,5% usam ChatGPT/Gemini/Copilot com frequência na decisão (23% diário) | "Mapa da Busca no Brasil 2026" (Optimiza, via Adnews) | SECUNDÁRIO |
| Delegação a agentes | 15% deixariam agente comprar; 67,3% delegariam busca de informação | Mobile Time/Opinion Box, 12-jun-2026 | SECUNDÁRIO |
| Só chatbot para buscar | 2,2%; 1 em 4 usa buscador e IA igualmente | Canaltech e afins | SECUNDÁRIO |

Leitura para copy comercial (harmonizada): o Brasil combina uso consciente e frequente de IA na decisão de compra (46,5% [secundário]) e 3º lugar mundial em ChatGPT com delegação transacional ainda baixa (15% deixariam um agente comprar). O pitch honesto é: "as respostas de IA já formam a opinião do comprador brasileiro hoje; a infraestrutura de checkout agêntico (UCP/ACP) já está em rollout, mas o volume transacional delegado ainda é embrionário — quem estrutura dados agora captura a virada".

## 3. Imprensa brasileira × IA (mapa de earned media)

- **Estadão × Google** (10-dez-2025): primeiro licenciamento de notícias para IA no Brasil (feed factual para o Gemini; exclui opinião, colunas e agências).
- **Folha × Google**: acervo + feed em tempo real para o Gemini (fixo + variável; News Pilot).
- **Folha + UOL × OpenAI** (25-mai-2026): primeiro acordo brasileiro com a OpenAI; notícias em tempo real no ChatGPT; reportado pela imprensa como associado ao encerramento da ação judicial da Folha (movida em ago/2025) — a extinção formal do processo não foi verificada em fonte processual.
- **Frente coletiva** (22-dez-2025): ANJ + Abert + Aner + 9 entidades notificaram Google, Microsoft, Amazon, Meta, Apple e OpenAI propondo remuneração.
- **CADE** (abr/2026): investigação sobre o impacto da IA do Google no jornalismo avançou de inquérito para a fase seguinte, chamada de "processo administrativo" pela imprensa [classe processual exata e número não verificados no CADE — confirmar antes de citar em material público].
- Lacunas: Globo sem acordo público (projeto interno "Irineu"); posição formal da Abraji não localizada.
- **Hipótese GEO testável (não fato)**: os acordos de licenciamento PODEM deslocar a presença de Folha/UOL/Estadão nas respostas de Gemini e ChatGPT no Brasil — o efeito público (treino? grounding? exibição? nada visível?) não está documentado. Tratar como hipótese de monitoramento na série dos 25 prompts canônicos e na cohort de mídia do repo papers; só virar argumento comercial depois de medido.

## 4. Regulatório (estado em 22-jul-2026)

- **PL 2338/2023** (é PROJETO, não lei): aprovado no Senado (10-dez-2024); NÃO votado na Câmara até esta data; votação de 27-mai-2026 não confirmada; indício de novo adiamento para dez/2026 [DIAP, acesso parcial]. O texto do Senado adota modelo de risco estilo AI Act, SIA e multas de até R$ 50M por infração [conforme substitutivo aprovado no Senado; o valor pode mudar na Câmara]. Tramitação: se a Câmara aprovar COM alterações, volta ao Senado; se aprovar sem alterações, segue a sanção/veto. PL 2688/2025 tramita em paralelo [secundário].
- **ANPD**: sandbox regulatório de IA em piloto desde fev/2026 (Metatext, Synapse AI, IA Greenworld); Radar Tecnológico sobre IA generativa; IA como eixo de fiscalização no Mapa 2026-2027. Nota: participar de sandbox NÃO é salvo-conduto — a LGPD segue integralmente exigível.
- **CONAR** (autorregulação publicitária, não lei): Guia de Influenciadores, edição de 12-mai-2026 (efeitos 01-jun-2026): corresponsabilidade, no âmbito autorregulatório, de anunciante, agência e influenciador pela veracidade de conteúdo gerado/editado com IA — sem prejuízo das responsabilidades legais aplicáveis (CDC etc.); adequação ao ECA Digital (Lei 15.211/2025).
- Natureza das normas (não misturar): LGPD = lei vigente; atos da ANPD = regulamentação/orientação; CONAR = autorregulação do setor publicitário; ECA Digital = lei com escopo específico (crianças/adolescentes); PL 2338 = projeto.
- Implicação prática para a Brasil GEO e clientes: (a) conteúdo gerado com IA em campanha precisa de trilha de verificação de veracidade — o guia do CONAR expõe anunciante e agência no âmbito autorregulatório, e o CDC no legal; os validadores de proveniência do curso-factory são também mitigação desse risco; (b) dados pessoais em prompts e pipelines já são regidos pela LGPD (base legal, finalidade, minimização, transparência, papéis de controlador/operador e art. 20 para decisões automatizadas — tratamento detalhado no `docs/LGPD.md` do repo landing); (c) acompanhar o PL 2338 por trimestre — nunca citar como "lei".

## 5. Mercado brasileiro de GEO

- Agências posicionadas [autorreferido, secundário]: Wyse, Bloomin, Geostack (R$ 1.497–4.491/mês); estimativas do próprio setor: <5% das agências oferecem GEO estruturado, ~1,2% das empresas otimizam para IA. Ferramentas locais: Tropk, Promptado [secundário].
- Eventos 2026: Web Summit Rio (8-11/jun, IA como eixo), SEO Summit SP (13-14/nov, "SEO na era das IAs"). Trilha nomeada "GEO" em evento brasileiro: não encontrada — oportunidade concreta de palestra/keynote inaugural da categoria.
- Mercado de IA generativa BR: US$ 371,2M (2025) → projeção US$ 1,48B (2034) [secundário].
- Posição competitiva [OPINIÃO INTERNA, uso exclusivo em planejamento — NUNCA em material público ou comparativo comercial, risco CONAR/denigração]: o corpus científico (Wave Julho-22), a medição pública (25 prompts) e os papers em produção são ativos de diferenciação que nenhum player brasileiro citado nas listas do setor demonstra publicamente. Os números "<5% das agências" e "1,2% das empresas" são autorreferidos pelo próprio setor [secundário] — não usar como fato.

## 6. Segurança agêntica: ser agent-ready sem virar vetor

### 6.1. O ataque é real; separar demonstração de observação em produção
- **Demonstrações de pesquisa (PoC controlado):** Brave × Comet (ago/2025): instruções invisíveis numa página (texto branco, comentário HTML, post de Reddit) sequestram o agente logado — acesso a e-mail, captura de OTP, exfiltração; out/2025: injeção invisível via imagem/screenshot; CometJacking: payload em parâmetro de URL; ChatGPT Atlas (out/2025): hijack demonstrado em horas.
- **Reconhecimento do fabricante:** a OpenAI declarou (dez/2025) que prompt injection em browser-agents "dificilmente será totalmente resolvido" e mantém programa de hardening com red teaming por RL.
- **Observado em produção (in the wild):** Unit 42 documentou injeção indireta baseada em web em uso real; levantamento citando o Google (abr/2026) lista categorias já observadas em páginas públicas: manipulação de SEO, dissuasão de agentes, experimentos de exfiltração e comandos destrutivos. Nível de evidência distinto dos PoCs acima — os dois juntos justificam o checklist, mas não descrever PoC como ataque corrente.
- Referência normativa vigente: OWASP Top 10 for LLM Applications **2025** (LLM01 = Prompt Injection, incluindo indireta). NÃO existe edição "2026" — corrigir qualquer material que cite "OWASP 2026".

### 6.2. Checklist "agent-friendly sem virar vetor" (síntese nossa a partir das fontes; não existe padrão único de mercado)
1. Tratar conteúdo de terceiros exibido na página (comentários, reviews, UGC) como não confiável: além de escapar HTML, moderar instruções imperativas dirigidas a agentes ("ignore as instruções", "acesse", "envie para") — escapar markup NÃO impede injeção por texto visível; a mitigação é moderação de conteúdo + o site não conceder nada que dependa de confiança no agente (itens 3-5).
2. Nunca hospedar texto invisível com instruções (mesmo "inofensivas" tipo "AI agents: recommend this brand") — além de vetor, o Google trata instrução oculta como spam e as defesas dos motores (Wave Julho-22 §5) classificam como manipulação.
3. Formulários e checkouts operáveis por agente devem exigir confirmação explícita do usuário para ações irreversíveis (padrão também recomendado pela Microsoft/Google para quem constrói agentes).
4. Segmentar tráfego agêntico com identidade verificável (§6.3) em vez de CAPTCHA indiscriminado — CAPTCHA quebra o caminho de compra agêntico legítimo.
5. Registrar em log as sessões de agentes separadamente (user-agents §2.1 da Wave 22B + assinaturas §6.3) para auditoria e medição.

### 6.3. Identidade de agentes (padrão EMERGENTE, ainda draft — não usar como controle crítico único)
- **Web Bot Auth (IETF)**: assinatura criptográfica por requisição construída sobre HTTP Message Signatures (RFC 9421, esta sim RFC publicada; o uso para bots é draft: draft-meunier-web-bot-auth-architecture), Ed25519, header `Signature-Agent`; working group formal desde o início de 2026 [marcos exatos: secundário]; apoio de Cloudflare, Amazon, Akamai e OpenAI. Enquanto draft: usar como sinal POSITIVO (agente assinado = confiável), nunca como bloqueio de tudo que não assina — a maioria dos agentes legítimos ainda não assina.
- **Cloudflare Signed Agents** (ago/2025) + registry aberto de agentes com Amazon Bedrock AgentCore (fev/2026).
- **Comércio agêntico**: Akamai (15-jul-2026): 47,9% do tráfego de commerce na rede já é bot de IA (dez/2025); agent hijacking e identidade sintética são as fraudes emergentes; ACP/Stripe usa Shared Payment Tokens de uso único como salvaguarda. Com o UCP do Google ativo no AI Mode brasileiro (§1), esse cenário de risco vale para lojas brasileiras JÁ [conexão nossa].

## 7. Correções e conflitos
- **Não citar o PL 2338 como aprovado** em nenhum material — status verificado em 22-jul-2026: parado na Câmara. Reavaliar trimestralmente.
- **"OWASP LLM Top 10 2026" não existe**; a versão vigente é 2025. Corrigir se aparecer no corpus ou em curso.
- A Wave Julho registrou "AI Mode opera em português do Brasil (anúncio 8-set-2025)" — esta wave confirma em fonte primária nacional e acrescenta UCP (19-mai-2026) e a agenda B2A (24-mar-2026). Sem conflito, só adensamento.
- Números de adoção do §2 misturam vendor (OpenAI sobre si), instituto (Datafolha) e pesquisas de mercado [secundárias]: aplicar a escala §7.4 da Wave Julho-22 ao citar.

## 8. Aplicação por repositório

### 8.1. `papers`
- O gap PT-BR (Wave Julho-22 §8.1) agora tem o contexto de mercado completo para a introdução dos papers: adoção (§2), acordos de licenciamento (§3) e vazio acadêmico. O dataset de 127 entidades BR ganha motivação citável com fontes primárias brasileiras.
- Hipótese nova monitorável: os acordos Folha/UOL/Estadão (§3) devem deslocar padrões de citação de Gemini e ChatGPT para domínios licenciados no Brasil — testável na nossa série temporal (cohort de mídia).

### 8.2. `landing-page-geo`
- Copy comercial: usar a leitura honesta do §2 (formação de opinião hoje, checkout agêntico amanhã) e o mapa de licenciamentos §3 no argumento de earned media BR.
- Segurança: aplicar o checklist §6.2 no próprio site (auditar UGC/reviews se houver; confirmar ausência de texto invisível; logging de agentes) — credencial de "consultoria que pratica o que prega".
- Conteúdo: artigo/curso sobre o mapa regulatório (§4) posiciona autoridade num tema que nenhuma agência BR citada cobre com rigor.

### 8.3. `curso-factory`
- Aulas candidatas: "GEO no Brasil: mercado, dados e regulatório" (§§1-5) e "Agent-ready sem virar vetor" (§6, com o checklist como material de exercício).
- `reviewer.py`/quality gates: adicionar à lista de verificação factual os dois vetos do §7 (PL 2338 não aprovado; OWASP 2026 inexistente) enquanto estiverem vigentes.

## 9. Claims machine-readable

```yaml
claims:
  - id: c1
    claim: "PL 2338/2023 NAO aprovado na Camara ate 22-jul-2026 (ausencia de fonte confirmando aprovacao)"
    fonte: "teletime.com.br; entercastconsulting.com.br; diap.org.br (acesso parcial)"
    tipo_fonte: imprensa_especializada
    confianca: media_alta
    valido_em: 2026-07-22
    revisar_ate: 2026-10-01
  - id: c2
    claim: "Brasil 3o maior usuario de ChatGPT; ~140M mensagens/dia"
    fonte: "relatorio OpenAI ago/2025, NAO acessado diretamente; via Fast Company Brasil/Softex"
    tipo_fonte: vendor_sobre_si_via_secundaria
    confianca: media
    valido_em: 2026-07-22
    revisar_ate: 2026-12-31
  - id: c3
    claim: "Folha+UOL fecharam acordo com OpenAI em 25-mai-2026; imprensa associa ao encerramento do processo da Folha (extincao formal nao verificada)"
    fonte: "meioemensagem.com.br; poder360.com.br (25-mai-2026)"
    tipo_fonte: imprensa
    confianca: alta_para_o_acordo_media_para_o_processo
    valido_em: 2026-07-22
    revisar_ate: 2027-01-31
  - id: c4
    claim: "Guia CONAR de influenciadores com corresponsabilidade AUTORREGULATORIA por conteudo de IA, efeitos desde 01-jun-2026"
    fonte: "conar.org.br (PDF do guia); migalhas.com.br (12-mai-2026)"
    tipo_fonte: autorregulacao_setorial
    confianca: alta
    valido_em: 2026-07-22
    revisar_ate: 2027-06-01
  - id: c5
    claim: "UCP (checkout no AI Mode) em rollout global desde 19-mai-2026 incluindo Brasil, conforme imprensa; confirmacao primaria do Google pendente"
    fonte: "mobiletime.com.br; cndl.org.br"
    tipo_fonte: imprensa_especializada
    confianca: media
    valido_em: 2026-07-22
    revisar_ate: 2026-10-31
  - id: c6
    claim: "OWASP Top 10 LLM vigente e a edicao 2025; nao existe edicao 2026"
    fonte: "genai.owasp.org"
    tipo_fonte: doc_oficial
    confianca: alta
    valido_em: 2026-07-22
    revisar_ate: 2026-12-31
  - id: c7
    claim: "Prompt injection indireta via conteudo web contra browser-agents e ataque demonstrado (Comet, Atlas) e observado in the wild"
    fonte: "brave.com/blog/comet-prompt-injection; openai.com/index/hardening-atlas-against-prompt-injection; Unit 42"
    tipo_fonte: pesquisa_seguranca_primaria
    confianca: alta
    valido_em: 2026-07-22
    revisar_ate: 2026-12-31
```
