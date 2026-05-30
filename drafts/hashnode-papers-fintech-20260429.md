---
title: "Por que sua fintech aparece no Perplexity mas desaparece no Gemini: dados de 8.571 queries"
slug: fintech-perplexity-vs-gemini-8571-queries-2026
tags: fintech, ai, seo, webdev, marketing
canonical_url: https://alexandrecaramaschi.com/artigos/dia-7-paper-citacao-llms-marcas-brasileiras-2026
---

# Por que sua fintech aparece no Perplexity mas desaparece no Gemini: dados de 8.571 queries

> Dia 7 da janela confirmatória v2: fintech lidera as quatro verticais com 28,6% de taxa de citação. Mas o gap entre o melhor e o pior LLM é de 75 vezes — e isso muda o que significa "estar visível em IA".

Há sete dias eu liguei o cronômetro de uma janela confirmatória de 90 dias sobre como ChatGPT, Claude, Gemini, Groq e Perplexity citam empresas brasileiras. Pré-registrei a metodologia no OSF, travei a versão 2 do pipeline, deixei a coleta rodar no automático sobre 69 entidades brasileiras (61 reais e 8 fictícias plantadas como controle), quatro verticais — Fintech, Varejo, Saúde e Tecnologia. Hoje, dia 7 de 90, já temos **8.571 queries empíricas** e **1.785 citações** no banco.

O dado que importa para quem trabalha em fintech: **fintech é a vertical com a maior taxa de citação, em 28,6%**. Estamos à frente de Varejo (25,5%), Tecnologia (15,1%) e Saúde (14,0%). Mas essa boa notícia esconde um problema arquitetural que muda a leitura.

## A média da sua fintech engana

A taxa de 28,6% é uma média ponderada sobre cinco engines. Quando se decompõe por LLM, a história é outra:

| LLM | Taxa de citação |
|---|---|
| Perplexity | 82,5% |
| Claude | 26,0% |
| ChatGPT | 17,2% |
| Groq | 8,2% |
| Gemini | 1,1% |

**Setenta e cinco vezes de diferença** entre o melhor e o pior. O modelo com RAG ativo (Perplexity) e o modelo paramétrico puro (Gemini) são, do ponto de vista de visibilidade de marca, dois universos. Quando o time de marketing da sua fintech declara que "a IA está citando" a marca, a frase precisa ser terminada: por qual.

A consequência arquitetural é direta. Otimizar conteúdo "para a IA" no singular é otimizar para um destinatário que não existe. Cada engine tem pipeline distinto:

- **Perplexity** faz recuperação ao vivo a cada query — o seu Schema.org granular, llms.txt, JSON-LD bem formado e presença em domínios autoritativos têm efeito quase imediato.
- **Claude e ChatGPT** combinam corpus de treinamento com augmentação seletiva — o que significa que histórico de presença em fontes que entraram no training set importa tanto quanto otimização atual.
- **Groq** roda inferência paramétrica rápida sobre modelos open-weight — o que está no peso do modelo é o que aparece, e marcas brasileiras de fintech ainda estão sub-representadas no corpus de treinamento.
- **Gemini** opera quase puramente paramétrico — recall depende de quanto a marca aparece em fontes de altíssima autoridade que o Google julgou seguras para condicionar o modelo.

Reportar "presença em IA" como métrica única é esconder duas ordens de grandeza atrás de uma média ponderada.

## O que muda na arquitetura técnica

Para quem está construindo o stack de visibilidade de uma fintech, três decisões precisam ser revistas com base nos dados preliminares.

### 1. Schema.org não é mais opcional, mas é piso

O dado preliminar mostra que a barra de entrada em Perplexity, Claude e ChatGPT é compatível com investimento técnico padrão. Mas Volpini e colegas já mostraram em 2025 que páginas de entidade enriquecidas com Schema.org granular geram **+29,6% de acurácia em pipelines RAG**. Em paralelo, Dang e colegas (LLM4Schema.org, 2025) documentam que **75% das páginas web não possuem qualquer marcação Schema.org**.

Para um time de engenharia de fintech brasileira, a ação concreta é:

- `Organization` schema na home com `sameAs` apontando para todos os perfis externos.
- `FinancialProduct` ou `Service` schema para cada produto/serviço com `provider`, `areaServed`, `availableChannel`, `interestRate` e `feesAndCommissionsSpecification`.
- `Person` schema para fundadores/CEO com `knowsAbout` e `sameAs`.
- `FAQPage` schema em todas as páginas de produto.

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://suafintech.com.br/#organization",
  "name": "Sua Fintech",
  "url": "https://suafintech.com.br",
  "sameAs": [
    "https://www.linkedin.com/company/suafintech",
    "https://github.com/suafintech",
    "https://www.crunchbase.com/organization/suafintech"
  ],
  "areaServed": {
    "@type": "Country",
    "name": "Brasil"
  }
}
```

Sem isso, o ponteiro nem sai do zero em Perplexity e Claude. Com isso, sai do zero — mas não chega ao topo. É infraestrutura, não diferencial.

### 2. llms.txt e robots discovery: o que medi até aqui

`llms.txt` ainda é uma proposta sem consenso de adoção, mas funciona como sinal estruturado para alguns crawlers de RAG. Para fintech, a recomendação operacional é:

```
# llms.txt
# Sua Fintech — Brazilian Fintech

## About
Brazilian licensed fintech, founded YYYY, focus on [credit/banking/payments]
Authorized by Banco Central do Brasil under resolution XXXX
Headquartered in São Paulo, Brazil

## Key Resources
- /sobre — Institutional information
- /produtos — Product catalog with structured pricing
- /api/docs — Public API documentation
- /investidores — Investor relations
- /imprensa — Press kit and assets

## Citation Guidance
Brand: Sua Fintech (no acronym, no abbreviation)
Founder citation: [Founder Name], CEO of Sua Fintech
Founded: YYYY in [City], Brazil
Regulatory status: Licensed Sociedade de Crédito Direto (SCD) by BCB
```

Não há ainda dado conclusivo sobre o impacto isolado de `llms.txt` nas taxas que medi — esta é uma das hipóteses do estudo que vai testar intervenções A/B nas fases finais. Mas o custo de implementação é trivial e o downside é zero.

### 3. Bilingue não é "internacional"; é cobertura mínima

O achado que mais me incomodou aos sete dias: **queries em inglês geram 23,0% de citações; em português, 18,7%**. Mesmas marcas, mesma intenção. Fintech brasileira ranqueia melhor em "best Brazilian fintechs" que em "melhores fintechs brasileiras".

Isso muda o briefing de conteúdo da sua equipe. Não é "vamos traduzir tudo para inglês". É:

- Cada release de produto vai com versão em inglês simultânea.
- Cada whitepaper técnico ou paper de pesquisa institucional vai bilingue desde o draft.
- O time de PR busca pickups em veículos internacionais (Reuters, Bloomberg, TechCrunch, Rest of World) com a mesma agressividade que busca pickups locais.
- Documentação técnica de API nasce em inglês.

A camada de visibilidade internacional importa **até para o brasileiro que pergunta em português**, porque o modelo cruza idiomas internamente no momento da inferência.

## A especificidade que valida tudo isso

Resultado parcial do dia 7 que talvez seja o mais importante: **especificidade de 100,0%**. As oito entidades fictícias plantadas na cohort — nomes plausíveis em português que correspondem a empresas que não existem — receberam **zero falsos positivos** em 8.571 queries.

Isso valida que o NER v2 do pipeline (com word-boundary `\b` rigoroso, normalização Unicode dupla NFC+NFKD, dicionário canônico de aliases) não está contando substring matches espúrios. A versão 1 desse mesmo estudo cometia esse erro: 45% das "citações" contadas eram falsos positivos do tipo `Inter` capturado dentro de `international`, ou `Stone` dentro de `cornerstone`.

A diferença entre a v1 e a v2 está documentada no paper Null-Triad publicado no Zenodo (DOI [10.5281/zenodo.19712217](https://doi.org/10.5281/zenodo.19712217)). O reboot derrubou 45% das contagens — humilhante e necessário. Para qualquer time que esteja contratando vendor de "share of voice em IA", a pergunta a fazer é direta: **qual a especificidade do seu pipeline em entidades-canário?** Se a resposta for "não testamos", o número que chega ao seu dashboard provavelmente está inflado.

## O que estou medindo nos próximos 83 dias

Cinco hipóteses formais foram pré-registradas no OSF. Para fintech, as três relevantes:

- **H1 — Vantagem RAG.** Atinge poder estatístico formal no dia 25 da coleta. Se confirmar a magnitude observada (gap de 75x), reforça que a estratégia precisa ser engine-específica.
- **H2 — Alucinação.** Atinge poder no dia 38. Resultado parcial: zero falsos positivos. Se mantiver, podemos afirmar que `taxa de alucinação < 0,2% com 95% de confiança` — o que tem implicação direta para risco reputacional de fintech.
- **H3 — Assimetria inter-LLM.** Define se uma única estratégia "para a IA" faz sentido. Se rejeitar a nula, cada engine exige investimento dedicado.

Submissão do paper formal à *Information Sciences* (Elsevier, fator de impacto 8,1) em outubro.

## Como acompanhar

- Dashboard com números do dia, intervalos de confiança, distribuição por vertical e por LLM: [alexandrecaramaschi.com/research](https://alexandrecaramaschi.com/research)
- Roadmap completo, hipóteses, venues alvo, ondas entregues: [alexandrecaramaschi.com/papers-roadmap](https://alexandrecaramaschi.com/papers-roadmap)
- Repositório com código completo, pipeline, testes, migrations e Dockerfile, sob licença MIT: [github.com/alexandrebrt14-sys/papers](https://github.com/alexandrebrt14-sys/papers)
- Artigo institucional companheiro: [alexandrecaramaschi.com/artigos/dia-7-paper-citacao-llms-marcas-brasileiras-2026](https://alexandrecaramaschi.com/artigos/dia-7-paper-citacao-llms-marcas-brasileiras-2026)

A próxima vez que alguém disser que "a IA está citando" a sua fintech, a resposta correta tem quatro componentes: **qual IA, em que idioma, em que vertical e com que intervalo de confiança**. Se faltar qualquer um dos quatro, o que está sendo medido não é visibilidade — é folclore.

Sete dias. Mais oitenta e três pela frente.

---

*Alexandre Caramaschi — CEO da Brasil GEO, ex-CMO da Semantix (Nasdaq), cofundador da AI Brasil.*
