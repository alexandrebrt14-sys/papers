# g1_kpis_reports (Gemini 3.1 Pro grounded)

Olá. Como pesquisador sênior em GEO (Generative Engine Optimization) e SEO, estruturei este mapeamento denso e acionável para apoiar as estratégias da sua consultoria (alexandrecaramaschi.com / brasilgeo.ai). 

O mercado de ferramentas de GEO consolidou-se rapidamente entre julho e agosto de 2026. O paradigma mudou de "posição no ranking (SERP)" para "frequência de citação (Citation Rate) em respostas geradas por IA". A seguir, detalho os frameworks de medição, KPIs e dashboards dos principais vendors e agências do mercado, respeitando a sua janela de interesse e distinguindo a natureza de cada fonte.

---

### 1. Frameworks de KPIs e Métricas de Visibilidade em GEO (Jul–Ago 2026)

A tabela abaixo consolida os KPIs operacionais adotados pela indústria para medir a visibilidade em Answer Engines (ChatGPT, Perplexity, Gemini, Google AI Overviews, Claude, etc.). Quando a fórmula exata não é aberta pelo vendor (algoritmos proprietários), o status é assinalado como "Fórmula não localizada/proprietária".

| Nome do KPI | Definição Operacional | Fórmula / Cálculo | Vendor / Plataforma | Fonte (Natureza, Data e URL) |
| :--- | :--- | :--- | :--- | :--- |
| **AI Visibility Score** | Pontuação agregada (geralmente classificada em *Low*, *Medium*, *High*) que consolida a presença da marca em respostas sintéticas (LLMs e AI Overviews). | *Fórmula proprietária*. Calcula a intersecção entre volume de menções, sentimento favorável e citações com link ao longo de prompts pré-definidos. | **Semrush** (AI Visibility Toolkit) | **Primária**: Semrush (*Website marketing guide*), 22-jul-2026.<br>**Secundária**: Behind Rankings, 02-ago-2026. |
| **Mention Rate (Taxa de Menção)** | Frequência com que a marca é citada pelo nome (*named entity*) pelo modelo ao responder a um set de prompts, independentemente de haver link. | `(Nº de Prompts em que a marca é nomeada / Total de Prompts testados) * 100`. | **Peec AI**, **Semrush**, **Strivelabs** | **Secundária**: Strivelabs, 17-ago-2026; SkySync, 27-jul-2026. *(Fonte primária com fórmula explícita não localizada para Strivelabs).* |
| **Citation Rate (Taxa de Citação)** | Frequência com que o domínio da marca é usado como fonte (*grounding URL* / link direto) na geração da resposta da IA. Difere da menção simples. | `(Nº de respostas com link direto para o domínio / Total de Prompts testados) * 100`. | **Peec AI**, **Ahrefs** (Brand Radar) | **Primária**: Peec AI, 15-ago-2026.<br>**Secundária**: TopCited, 2026. |
| **AI Answer Share of Voice (SoV)** | Frequência com que a marca aparece ou é recomendada em comparação com os concorrentes diretos no mesmo set de prompts. | `(Suas Menções ou Citações / Total de Menções ou Citações do mercado no set de prompts) * 100`. | **Profound**, **Peec AI**, **Semrush** | **Secundária**: Strivelabs, 17-ago-2026; Layer3Labs, 28-jul-2026. *(Métrica validada pela indústria, porém sem publicação primária da Profound localizada no período).* |
| **Identifiable AI Referrals** | Tráfego de referência originado de domínios ou agentes de IA identificáveis (ex: `chatgpt.com`, `perplexity.ai`, `claude.ai`, `google (AI Mode)`). | Medição direta em Analytics (Sessões via *referral string* dos LLMs vs Sessões Totais). | **Conductor**, **Similarweb** | **Primária**: Similarweb, 29-jul-2026.<br>**Secundária**: Opollo (citando benchmark da Conductor de 2026), 23-jul-2026. |
| **Answer Position / Position in Answer** | Onde exatamente a citação aparece no texto gerado (ex: início, meio, fim, ou em carrossel de fontes). | *Não localizado* (Geralmente relatado como uma posição ordinal média ou quadrante). | **Dageno AI**, **Peec AI** | **Secundária**: Dageno AI, 03-ago-2026. *(Fonte primária não localizada).* |
| **Favorable Sentiment (Sentimento)** | Avaliação da polaridade (positiva, neutra, negativa) do contexto em que a marca foi mencionada pela IA. | *Fórmula proprietária baseada em NLP/LLM-as-a-judge*. | **Semrush**, **Peec AI** | **Primária**: Semrush (*Website marketing guide*), 22-jul-2026. |

---

### 2. Visão de Dashboards e Relatórios Mensais (Jul–Ago 2026)

Consultorias de GEO (como a Brasil GEO) precisam empacotar esses KPIs em relatórios executivos e painéis de monitoramento. Abaixo, exemplos da estrutura de dashboards revelados pelas plataformas no período:

#### A. Semrush (AI Visibility Toolkit)
A Semrush acoplou seu módulo de IA ao ecossistema tradicional de SEO, o que é ideal para clientes que já operam a suíte. 
*   **Dashboards Existentes**: 
    *   **Visibility Overview**: Apresenta a tríade "AI Visibility Score", "Mentions", e "Citations" acompanhados de "Cited Pages".
    *   **Narrative Drivers**: Focado no cálculo de Share of Voice contra os concorrentes escolhidos.
    *   **Perception**: Mede como o LLM descreve a marca e classifica o sentimento (Favorable Sentiment over time).
    *   **Competitor Research**: Mapeia *gaps* em prompts específicos onde concorrentes são citados (e a sua marca não).
*   **Fonte**: Primária. Semrush (*How to find AI visibility gaps with Semrush*), 27-jul-2026 e 22-jul-2026.

#### B. Peec AI
Altamente elogiado no mercado B2B e por agências, o Peec foca na "pureza" da métrica, sendo rigoroso na separação conceitual entre o que é *Mention* e o que é *Citation*.
*   **Dashboards/Outputs**:
    *   **Visibility Analytics Dashboard**: Centraliza Visibilidade, Posição e Sentimento. A ferramenta testa um conjunto fechado de perguntas de intenção de compra ao longo de meses.
    *   **Citation Source Analysis**: Identifica quais domínios (ex: Reddit, Forbes) estão alimentando as respostas da IA no seu nicho de mercado, permitindo ações de Digital PR (uma vez que backlinks tradicionais e conteúdo de terceiros impactam o LLM).
    *   **Slack/MCP Loop**: Produz *one-sliders* semanais para agências com resumos de variações de Visibilidade e Share of Voice (SoV) vs concorrentes.
*   **Fonte**: Primária (Peec AI, *AI Search Visibility Tracking for Marketing Agencies*) / Secundária (AIclicks, 12-ago-2026).

#### C. Similarweb (AI Visibility)
Foco em *Market Intelligence*. Em vez de olhar apenas para *prompts* individuais, a Similarweb analisa o impacto a nível macro.
*   **Dashboards Existentes**:
    *   **AI Brand Visibility / Gen AI Intelligence**: Compara o tráfego encaminhado pelos LLMs (ex: queda de acesso orgânico puro vs aumento de referrals do ChatGPT) e *industry-level benchmarking*.
*   **Fonte**: Primária. Similarweb (*AI Search Stats 2026*), 29-jul-2026. / Secundária (DemandSage, 10-ago-2026).

#### D. Profound, Conductor, Otterly e Ahrefs (Brand Radar)
*   **Profound**: Atende grandes *enterprises* mapeando 9+ modelos LLM em profundidade, provendo dados de "Share of Voice de Respostas" e "Analytics de Citações". Tem interface com foco no impacto financeiro/atribuição. *(Fontes secundárias: AIclicks; LLM Pulse).*
*   **Ahrefs Brand Radar**: Relatórios focados em conectar citações geradas por IA no ChatGPT, AI Overviews e Perplexity diretamente ao índice de backlinks e E-E-A-T já mensurados pelo Ahrefs. *(Fonte secundária: TopCited, 2026).*
*   **Otterly AI**: Dashboard voltado para monitoramento recorrente de citações com exportação (conector para Looker Studio) para montagem de relatórios personalizados por agências. *(Fonte secundária: TopCited, 2026).*

### 3. Recomendações Acionáveis para a Brasil GEO

Para montar o pacote da consultoria (alexandrecaramaschi.com / brasilgeo.ai):

1.  **Auditoria Inicial (Semrush ou Peec AI)**: Levante o *AI Visibility Score* ou a *Taxa de Menção Inicial* do cliente (Baseline) contra 3 concorrentes num pool de 50 a 150 *prompts* focados na jornada de compra (*bottom of funnel*).
2.  **Separe "Menção" de "Citação" nos seus relatórios**: Eduque seu cliente de que ser lembrado pelo nome pela IA (Menção) constrói autoridade, mas é a inclusão da URL como fonte raiz (Citação) que vai gerar tráfego qualificado de fato, que converte até 4,4x mais que a busca tradicional.
3.  **Relatórios Mensais de "Narrative Drivers"**: Utilize a abordagem visual do *Share of Voice* da Semrush ou Peec AI para comprovar o ganho de visibilidade mês a mês no ecossistema (ChatGPT, Google AI Overviews, Gemini, Perplexity).

*Nota de Transparência: Conforme instruído, não foram fabricados URLs ou dados. Algumas fórmulas absolutas de vendor (ex: cálculo exato do AI Visibility Score da Semrush e Share of Voice do Profound) são algoritmos matemáticos e pesos não publicados abertamente como código aberto por suas respectivas plataformas ("Fórmula não localizada / proprietária").*

## Fontes
- behindrankings.com — https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEfcIMaiyjask6a93Zt0D_whp45iJdJvVf5v56W9DGwVwwn43Yz7jFqnIaSx12F1w9cRNQP6Lb77TO_-sRKLTjj_PkJww0f6gOxwwiOZbfWXoSr552miuL22ynqceSwiz1u2Wk-J32tO8SBj7i5AA==
- opollo.com — https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHSpuI8_YXOHHlvH3qnQJQPnhMD5AM_26s7-DpHzfQZdSg-e_sXiqzKMyxNyXVIDeSoKmXj5TwKP5FFR4sfEX7Ywhggaq71GzDwC5oSzx-iokXkT0g-nlqfo7VVKkNiUxyMXQ==
- semrush.com — https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEepjFqR6PXooEqiuTA2Bdz2PpPH-UbRkYp7BtzTjQIrRfAtj52dXrmX9498cabBM1UkFZTw9o26Oa6wZvwudQ2zKAT880YUQr7_SprbXz2pcl57OWTjZD791QTsxM0vh_L7Pty
- strivelabs.ai — https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEB57BQzJgeWPtyPuqhtBjd82RDNvC2_SUU6W4zDZyTIRpiKpdEkV2n0JSrlNnCYlWp6CmZCVe1f8zbsyaBCcOb2nu0vhg0pNz2kyvZtgQm3qhs1o26-ZF5HIkIMLhlplaqE9uJYOKYZs7w4Q==
- skysync.nyc — https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHjApGBSeto7RQMfd-krkz17xwpLatCbqNW1rsOW5Sk81Sn0ejzxYisn7LLXoJeFxcoKCCGNfqvDAoOfRt5v5RxHpDHCfzwkUy5YaXD_JHgg7YHbRxSaA==
- peec.ai — https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFlKmYlYKoclVfM1K_9WfXnz0dK8Bj-eVJQ7xJrGWCARMnpJrjR49pH9SQJ2HSuA_RzYpppkKVeWdpYVJKVXCgsoi6azZ3l475yfx4QXBjteYw=
- topcited.ai — https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEL6ez5fsqRigUikdh9JSRlH9Ff4DfPzHvkb7axjzIHfnNjh_X8he-vf12GGHy5m3Wem7WTD6tkO-xstBk-hJRYxrvhHrM1nGi5Wi_B3_XTCgkM3qIYLZegnFT8AGNAZeSJSgtdNKCuPAyVMiwuu9w=
- layer3labs.io — https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH0-4iUZlkBYziqA4rIGazEkDBY7GrwYE7PJIytKT6-Ny0bIG4LO1dVes-JvBCzv1SCRptnmGZJPVeHsv13qQOozhrtZ6LrYTpoWYSIup7wnnqENqDO8pdBvLFQX87GW7jxiJdt95nhhomz
- therankingrobot.com — https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE5KdEnXGTI6BUv4uWe8wtuZc9mXAm_CH4h0wFDm8Zt0klUoC4iFvQW-xnd9jNWe6odks2Q5FyLRaKkz18dMHRUIfpKGhWHLjkPVaCEjM0664XBqBa5KuLedIcdgWrJ5F-JNmpexm8=
- similarweb.com — https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHcOmXNyFt_NbwqvSM4CpeqaNT4xSy3wYJ1EOVRGb1DTDJH7CfE8jMkqas7DWBtjwo3B7RqKL0EgpvC6yc08uvSunv0bl-pYdHTn5M1eOmXX88gFAsUQb3v_5x4J-7AbD_zSFRknHid
- dageno.ai — https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHpVAce8IiaxHiPzy32Acc-Ib6aUVwHJcKf2iNqfcJbO4PmRM5f7sW_wv9TSRSuypArQt0Sy3Hr4tOQzIeSx1O473b9p9H13_nSrDaKq8rAK0KpZWZGYEWAJQ0wsNs_SYDeDeWQMAMryygE2T-vesLDELvG3NY7
- semrush.com — https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHwCywlZ_jwTxYkREgdY8K19tZmns-0LZdjFs1oyyU_qCR3ftqDaRVk98PNqdEkkdbm02qAs5TzS-7VrHFHBTtHU1tZs5VVqOqmQjY7ouKuAwl700fLaTEuLgWPODHIrc-UPnIdIkfjx0wKPAYJGrqABBcpyWqhIw==
- aiclicks.io — https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGT-E0xUaW7rPxMzxbbm5U9mlb8pThho0EupAL5vst6Xwz-PzCnYtB8K-fbyiSmX8sXEN_ng_ceLTlh5rC-JIW6KAbOVb2o3aM7D2ysPck9-LRgUer-WzmINk5Xb2mDD1lsiDSt6VaVlKAwQ8zQlZHSN4C60fVdOQ==
- riseatseven.com — https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG1RRTy8rylhlKaQX2P72GysBHHiqOJb57CgILSsCcPbB6aeg2AHnZekaR3ym7h54RRebyj60vCCJ4nXI_to9PQAIGKZbabstv0rjKXgCUGj1wbElehPqgd8k0VsFLa7PQysnUNPPo2obnmCQ==
- llmpulse.ai — https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEbKznKigyPA3J_lxcder5oRxgdDORtkcavBsaVm2xmQLkWy4XCgHjdEqQS3JliVaGut9eV3WOo93eX0VeGfV-xWR91XRNHZWT-_6rfc_OMUcb1Ip-uRx6pvJ2wQ4J0otOeF__TFqyN
- demandsage.com — https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF6rxHPh5iShPfjeXTRkiNOoKn1xStlMuT0h_8GV61iXbwV3QpIefdbPeAoKjJ7UHzhlxAgYMwjfDKpLxE_PLt9OIRWbk2kpFxGtSkhVeceI8t8TOhZLvyWqk54qeTwx5NFo9j6Cs8=
- llmpulse.ai — https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF7ZU-Je7VPq_hxZ0DARTm3gsA3OhSly4gaXL6wGp2xvaVGfYDgnseFUIOvOr73rsrQrXgcS7yoz8NCuaxsFg4u_SlAcVwANN3vxFIQ-zzy0s8BrCyELqhHSBoW3Zs=