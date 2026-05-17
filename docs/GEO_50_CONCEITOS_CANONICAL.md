# Os 50 Conceitos Canônicos de GEO/SEO 2026

> Documento canônico interno — referência obrigatória para qualquer trabalho de SEO, GEO (Generative Engine Optimization) ou AISO (Answer Engine Optimization) nos repos da Brasil GEO.
>
> Última revisão: 2026-05-17
> Mantenedor: Alexandre Caramaschi (CEO Brasil GEO)
> Fonte: Framework canônico Brasil GEO 2026 (consolida Aggarwal SIGIR 2023, AutoGEO ICLR 2026, AgenticGEO, Profound, Ahrefs Brand Radar, iPullRank, Google AI Optim Guide 15-mai-2026)

## Aplicação em papers

Estes 50 conceitos são **taxonomia de classificação** ao catalogar paper acadêmico de GEO/AISO/SEO — todo paper indexado neste repo deve ser tagueado contra os eixos relevantes. Em particular:

- **Ao resumir um paper** (abstract, contribuição, metodologia), aplicar tags contra os Conceitos 11 (Answer capsules), 13 (Schema.org), 15 (Clareza de entidade), 21 (Referências externas), 22 (Autoria), 24 (Citabilidade GEO), 25 (Recuperabilidade generativa) e 30 (llms.txt).
- **Ao desenhar nova vertical de pesquisa** (citation tracker, intervention, context_analyzer), validar que os prompts do portfólio cobrem os 14 eixos.
- **Em revisão de literatura** (`docs/research/` e `docs/research/geo-q2-2026/`), usar a Tabela síntese (auditoria técnica, conteúdo, GEO/AISO, local, autoridade, conversão, governança, priorização) como checklist obrigatório antes de declarar a revisão completa.
- **Em pipeline Perplexity sonar-deep-research**, gerar a query incorporando os conceitos pertinentes ao tópico — evita lacunas estruturais comuns em reviews ad hoc.

## Como usar este documento

- Use estes 50 conceitos como **checklist de auditoria** ao avaliar qualquer página, site ou conteúdo gerado para mecanismos de busca tradicionais e generativos.
- Em diagnósticos, **sempre referencie o conceito pelo número e nome canônico** (ex.: "Conceito 24 — Citabilidade GEO").
- Em geração de conteúdo (HBR, FAQs, pillars), os conceitos 8, 10, 11, 12, 22, 23, 24, 25 são prioridade absoluta.
- Em auditorias técnicas, os conceitos 1, 2, 13, 14, 28, 29, 30, 34, 35, 36 são prioridade.
- Em planos de Trust/E-E-A-T, os conceitos 17, 18, 22, 23, 43, 47, 48 são prioridade.

---

## Eixo 1 — Fundamentos técnicos de descoberta

### 1. Crawlabilidade
Mede se bots de busca conseguem acessar o site sem bloqueios técnicos.
Avalia status HTTP, links internos, robots meta, bloqueios indevidos, páginas órfãs e acesso ao conteúdo principal.

### 2. Indexabilidade
Mede se as páginas têm condições reais de entrar no índice.
Avalia canonical, noindex, redirects, duplicidade, páginas finas, parâmetros de URL e conflitos entre robots.txt e meta robots.

### 3. Arquitetura de informação
Mede se o site está organizado de forma lógica.
Avalia menu, hierarquia de páginas, profundidade de clique, categorias, páginas de serviço, páginas locais e relação entre conteúdos.

---

## Eixo 2 — On-page tradicional

### 4. Title tags
Mede se os títulos das páginas comunicam corretamente tema, intenção e entidade.
Avalia tamanho, unicidade, palavra-chave principal, cidade quando local, marca e clareza semântica.

### 5. Meta descriptions
Mede se as descrições ajudam clique, contexto e compreensão.
Avalia tamanho, promessa, intenção de busca, diferenciação, CTA e duplicidade.

### 6. H1 único
Mede se cada página possui um título principal claro.
Avalia ausência de H1, múltiplos H1, H1 genérico, H1 desalinhado com title e intenção da página.

### 7. Hierarquia H2/H3
Mede se o conteúdo está organizado em blocos compreensíveis.
Avalia subtítulos, sequência lógica, escaneabilidade, tópicos, perguntas e estrutura editorial.

---

## Eixo 3 — Conteúdo e semântica

### 8. Conteúdo visível
Mede se a página entrega informação real ao usuário e aos sistemas de busca.
Avalia profundidade, clareza, resposta direta, originalidade, utilidade, densidade temática e ausência de conteúdo genérico.

### 9. Intenção de busca
Mede se a página responde ao que o usuário realmente procura.
Avalia intenção informacional, comercial, local, transacional, comparativa e decisória.

### 10. Cobertura semântica
Mede se o conteúdo cobre entidades, tópicos e subtópicos relevantes.
Avalia termos relacionados, perguntas frequentes, variações de serviço, dores, soluções e contexto de mercado.

### 11. Answer capsules
Mede se a página possui blocos curtos e claros que podem ser extraídos como resposta.
Avalia definições, listas objetivas, perguntas e respostas, comparativos e explicações diretas.

### 12. FAQ visível
Mede se há perguntas reais respondidas no HTML visível.
Avalia qualidade das perguntas, clareza das respostas, intenção do usuário e potencial de recuperação por IA.

---

## Eixo 4 — Dados estruturados e entidade

### 13. Schema.org
Mede se os dados estruturados estão presentes, válidos e coerentes.
Avalia Organization, LocalBusiness, Service, WebPage, Article, FAQPage, BreadcrumbList, Person, ImageObject e ContactPoint.

### 14. Coerência entre schema e conteúdo
Mede se o JSON-LD reflete o que aparece na página.
Avalia divergências entre dados estruturados e conteúdo visível, dados inflados, informações invisíveis e marcações inconsistentes.

### 15. Clareza de entidade
Mede se máquinas entendem quem é a empresa, o que ela faz e onde atua.
Avalia nome, categoria, serviços, cidade, autor, organização, descrição institucional e relações entre entidades.

---

## Eixo 5 — Sinais locais

### 16. Autoridade local
Mede a força territorial do site.
Avalia cidade, bairro, região atendida, endereço, telefone, páginas locais, conteúdo geográfico e consistência territorial.

### 17. Google Business Profile
Mede a coerência entre o site e o perfil da empresa no Google.
Avalia categoria, descrição, serviços, NAP, avaliações, fotos, produtos, postagens, horário e link do site.

### 18. NAP
Mede consistência de nome, endereço e telefone.
Avalia se os dados aparecem iguais no site, Google Business Profile, redes sociais, diretórios e páginas externas.

### 19. Páginas de serviço
Mede se cada serviço importante possui uma página própria ou seção clara.
Avalia título, descrição, benefícios, processo, FAQ, provas, CTA e relação com intenção de busca.

### 20. Páginas locais
Mede se o site comunica presença territorial.
Avalia páginas por cidade, bairro, região, mapas, rotas, endereço, áreas atendidas e provas locais.

---

## Eixo 6 — Autoridade e confiança (E-E-A-T)

### 21. Referências externas
Mede se o conteúdo é sustentado por fontes verificáveis.
Avalia links para documentos oficiais, estudos, pesquisas, entidades reconhecidas, fontes técnicas e dados públicos.

### 22. Autoria
Mede se existe responsável editorial ou técnico pelo conteúdo.
Avalia nome do autor, biografia, cargo, especialidade, página de autor, data de publicação e data de atualização.

### 23. E-E-A-T
Mede sinais de experiência, especialidade, autoridade e confiança.
Avalia provas reais, cases, equipe, credenciais, histórico, avaliações, fotos, documentos e reputação externa.

---

## Eixo 7 — GEO/AISO (núcleo da prática Brasil GEO)

### 24. Citabilidade GEO
Mede se a página tem potencial de ser usada como fonte por sistemas generativos.
Avalia conteúdo visível, clareza, fontes, autoria, resposta direta, baixa linguagem promocional e estrutura editorial.

### 25. Recuperabilidade generativa
Mede se a página pode ser encontrada e usada por answer engines e IAs com busca.
Avalia tema, entidade, fragmentos citáveis, perguntas, referências, atualidade e autoridade.

### 26. Risco de pseudo-GEO
Mede se o site usa discurso exagerado ou promessas sem evidência.
Avalia frases como "apareça garantido na IA", "schema garante citação", "llms.txt faz o ChatGPT citar" ou "AI Overview garantido".

### 27. Governança de IA
Mede se o site está preparado para buscadores, LLMs, answer engines e agentes.
Avalia robots.txt, llms.txt, sitemap, dados estruturados, páginas institucionais e políticas claras de acesso.

---

## Eixo 8 — Arquivos de descoberta

### 28. robots.txt
Mede se o site declara regras para crawlers.
Avalia bloqueios, permissões, sitemap declarado, bots de busca, bots de IA e conflitos com indexação.

### 29. sitemap.xml
Mede se o site facilita descoberta das páginas.
Avalia URLs listadas, status das páginas, última modificação, páginas importantes ausentes e coerência com a arquitetura.

### 30. llms.txt
Mede se o site possui sinalização organizada para sistemas de IA.
Avalia clareza, links prioritários, resumo institucional, páginas importantes e uso sem prometer garantia de citação.

---

## Eixo 9 — Social e mídia

### 31. Open Graph
Mede se a página aparece corretamente em compartilhamentos.
Avalia og:title, og:description, og:image, og:url, dimensões da imagem e coerência visual.

### 32. Twitter/X Card
Mede se a página tem preview adequado em redes que usam cards.
Avalia tipo de card, imagem, título, descrição e consistência com Open Graph.

### 33. Imagem social
Mede se existe imagem 1200x630 ou equivalente para compartilhamento.
Avalia qualidade visual, legibilidade, branding, peso do arquivo e alt text.

---

## Eixo 10 — Performance e experiência

### 34. Performance
Mede velocidade e experiência técnica.
Avalia LCP, CLS, INP, peso da página, CSS, JavaScript, imagens, fontes e carregamento acima da dobra.

### 35. Core Web Vitals
Mede experiência real de carregamento e interação.
Avalia Largest Contentful Paint, Cumulative Layout Shift e Interaction to Next Paint.

### 36. Mobile
Mede se o site funciona bem no celular.
Avalia responsividade, tamanho de fonte, botões, espaçamentos, menu, formulários e velocidade mobile.

### 37. Acessibilidade
Mede se a página é utilizável por mais pessoas e tecnologias assistivas.
Avalia contraste, labels, aria-labels, foco, alt text, navegação por teclado e semântica HTML.

### 38. UX
Mede clareza da jornada do usuário.
Avalia primeira dobra, leitura, seções, escaneabilidade, confiança, objeções, fluxo e facilidade de ação.

---

## Eixo 11 — Conversão

### 39. CTA
Mede se há chamada clara para ação.
Avalia WhatsApp, formulário, ligação, rota, agendamento, orçamento, botão fixo, texto do botão e posição na página.

### 40. Conversão
Mede se a página transforma visita em ação.
Avalia formulário, WhatsApp, telefone, proposta, prova social, benefícios, urgência ética e caminho de decisão.

### 41. Formulários
Mede se os formulários são claros, seguros e funcionais.
Avalia campos obrigatórios, LGPD, validação, mensagem de erro, estado de envio e integração com WhatsApp ou CRM.

### 42. WhatsApp
Mede se o canal de contato está pronto para conversão.
Avalia link wa.me, mensagem pré-preenchida, número correto, botão visível e rastreamento de clique.

---

## Eixo 12 — Privacidade e segurança

### 43. LGPD
Mede sinais básicos de privacidade e confiança.
Avalia política de privacidade, cookies, termos de uso, consentimento, aviso em formulário e tratamento de dados.

### 44. Segurança
Mede sinais técnicos de proteção.
Avalia HTTPS, conteúdo misto, headers básicos, exposição de dados, formulários inseguros e scripts externos.

---

## Eixo 13 — Linkagem e institucional

### 45. Links internos
Mede a distribuição de autoridade e navegação.
Avalia links quebrados, links para páginas importantes, âncoras, profundidade e coerência temática.

### 46. Links externos
Mede qualidade das referências e conexões.
Avalia fontes confiáveis, links quebrados, excesso de links, links sem contexto e autoridade das fontes.

### 47. Páginas institucionais
Mede confiança básica.
Avalia Sobre, Contato, Política de Privacidade, Termos, Serviços, Autor, Equipe e endereço.

### 48. Prova social
Mede sinais de confiança para usuários e mecanismos.
Avalia avaliações, depoimentos, cases, clientes, selos, fotos reais, números e evidências verificáveis.

---

## Eixo 14 — Inteligência competitiva e priorização

### 49. Concorrência
Mede diferença entre o site e competidores.
Avalia conteúdo, autoridade, GBP, estrutura, páginas locais, schema, velocidade, UX e citabilidade.

### 50. Prioridade de ação
Mede o que deve ser corrigido primeiro.
Classifica problemas por impacto, urgência, dificuldade e potencial de ganho.

---

## Tabela síntese — Mapeamento por uso

| Atividade | Conceitos-chave |
|---|---|
| Auditoria técnica inicial | 1, 2, 13, 14, 28, 29, 30, 34, 35, 36, 37 |
| Auditoria de conteúdo | 4, 5, 6, 7, 8, 9, 10, 11, 12 |
| Auditoria GEO/AISO | 11, 12, 13, 14, 15, 24, 25, 26, 27, 30 |
| Auditoria local | 16, 17, 18, 19, 20 |
| Auditoria de autoridade | 21, 22, 23, 47, 48 |
| Auditoria de conversão | 38, 39, 40, 41, 42 |
| Auditoria de governança | 27, 28, 29, 30, 43, 44 |
| Priorização final | 49, 50 |

## Referências canônicas Brasil GEO 2026

- Papers: Aggarwal SIGIR 2023 ("Generative Engine Optimization"), AutoGEO ICLR 2026, AgenticGEO 2025, Bui et al. AISO 2026.
- Ferramentas: Profound (Series C US$ 96M fev/2026), Ahrefs Brand Radar, Peec.ai, Otterly, iPullRank Generative Visibility Score.
- Guias oficiais: Google AI Optimization Guide (15-mai-2026), Schema.org v30 (mai/2026), llms.txt spec.
- KPIs internos: SoV-AI, AECR, RTAS, Anchor Coverage, CTAM (ver `CITATION_METRICS.md`).

## Anti-padrões proibidos (regra Brasil GEO)

1. **Pseudo-GEO** — Prometer citação garantida em IA. Banido em copy, propostas e materiais comerciais.
2. **Schema inflado** — JSON-LD com informações que não aparecem na página visível (viola Conceito 14).
3. **llms.txt como talismã** — Tratar o arquivo como garantia de citação. É sinalização, não contrato.
4. **Slugs com acento** — URLs sempre ASCII. Acentuação só em texto visível.
5. **Pseudo-autoridade** — "#1", "líder", "especialista número um" sem evidência verificável (viola Conceito 26).
