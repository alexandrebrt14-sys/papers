
================================================================
ESCALONAMENTO CLOUD SUGERIDO (precisa da sua permissão)
----------------------------------------------------------------
  Motivos     : --provider explicito
  Modelo cloud: OpenAI · GPT-5.5
  Por que     : provider forcado pelo usuario (--provider openai)
  Custo est.  : ~$0.029 USD (estimativa)
  Via         : API direta
================================================================
Permissão: auto-aprovada (--yes)
1. **§Precedência** — O doc 22B declara que **Julho-22C §7 tem precedência sobre ele**. Se 22C não estiver no mesmo commit/corpus, agentes vão tratar este documento “canônico” como já supersedido por material ausente. Também há confusão em “precedência epistemológica intra-wave: §7.4 da Wave Julho-22” — isso não é intra-wave.

2. **§0.1 / §2.2 / §5.3** — Contradição de default: o TL;DR canoniza “citável sem ceder treino” e §2.2 chama isso de “postura canônica”, mas logo depois diz que, para Brasil GEO e maioria dos clientes GEO, o default é **liberar tudo, inclusive treino**. Um template de robots baseado nisso pode aplicar o default oposto ao pretendido.

3. **§1** — A narrativa “quem não configurar nada herdará defaults cada vez mais restritivos” generaliza decisões da **Cloudflare** para a web inteira. Isso só vale para zonas/planos/configurações Cloudflare afetadas, não para sites fora da Cloudflare nem necessariamente para domínios antigos.

4. **§1 / §6 b5** — “Bloqueio default de Training e Agent em páginas com anúncios a partir de 15-set-2026” é tratado como fato operacional definitivo, mas é anúncio futuro. Precisa ser rotulado como política anunciada/sujeita a mudança, não como estado vigente.

5. **§1 / §6 b5** — `tipo_fonte: doc_oficial` está mal rotulado para blog/anúncio da Cloudflare. É fonte primária de vendor, não documentação normativa estável. Use `blog_primario_vendor` ou similar.

6. **§2.1 / §2.2 / §6 b3** — A afirmação de que **ChatGPT-User** “pode ignorar robots.txt” precisa de citação literal e data. Se a doc da OpenAI oferece controle por robots para `ChatGPT-User`, dizer que “controle real é via WAF/CDN” é factualmente perigoso e incentiva bloqueios desnecessários de fetches iniciados por usuário.

7. **§2.1 / §2.2** — “Liberados: OAI-SearchBot, Claude-SearchBot, PerplexityBot, Googlebot...” no comentário do robots.txt é ambíguo. O snippet só bloqueia `GPTBot` e `ClaudeBot`; outros bots ficam liberados **apenas se não houver regras globais existentes** (`User-agent: * Disallow`, paths sensíveis etc.). Em template real, isso pode quebrar citação/indexação.

8. **§2.2 / §5.3** — O template recomendado não mostra uma configuração explícita para `Google-Extended`. Como o doc diz que essa decisão é crítica por cliente, deixar só comentário pode levar a comportamento não auditável. Melhor exigir bloco explícito `Allow`/`Disallow` documentado por decisão.

9. **§2.1 / §2.2 / §6 b1** — “Google-Extended controla treino do Gemini **e grounding**” é uma formulação arriscada. A documentação do Google historicamente separa Search/AI Overviews de controles como `Google-Extended`; “grounding” pode não significar todas as formas de recuperação/citação do Gemini. Precisa citar o texto oficial exato ou remover “grounding”.

10. **§2.3** — “Sites que bloqueiam o crawler de IA do Google são menos recuperados em AIO” conflita com a própria tese de que AIO usa **Googlebot normal** e que `Google-Extended` não controla AIO. “Crawler de IA do Google” é termo ambíguo/inexistente nesse contexto; pode ser lido como `Google-Extended`, produzindo a conclusão errada.

11. **§2.3** — O estudo arXiv é usado para sustentar uma leitura quase causal sobre recuperação em AIO. Se for observacional, deve ser rotulado como evidência correlacional/secundária, não como regra operacional combinada com doc oficial.

12. **§3** — “Mistral ~0,1:1 crawls por 1 visita referida” exige explicação metodológica. Uma razão inferior a 1 é possível por cache/janela de medição, mas contradiz a leitura intuitiva “crawls consumidos por visita devolvida”. Sem nota, parece erro de unidade ou razão invertida.

13. **§3 / §6 b6** — Inconsistência de proveniência: o texto chama Radar AI Insights de “[secundário]”, mas também diz que é “painel vivo” prevalente da Cloudflare; em claims, blog Cloudflare vira `doc_oficial`. Padronizar: Radar/blog Cloudflare são fontes primárias de vendor, snapshots datados.

14. **§4.1 / §6 b2** — “GA4 ganhou canal nativo AI Assistants” + “medium `ai-assistant` automático” parece misturar **canal** com **medium**. GA4 não necessariamente reescreve `medium`; default channel grouping pode classificar source/referrer sem alterar `session medium`. Isso afeta regras, UTMs e relatórios.

15. **§4.1 / §5.1** — “Criar o canal AI Assistants” é impreciso se ele é nativo/default do GA4. O que se cria é canal customizado ou custom channel group. Agentes podem tentar configurar algo inexistente ou duplicar o canal nativo.

16. **§4.1 / §5.1** — “Canal customizado... não retroage” é provavelmente falso ou pelo menos impreciso para **custom channel groups** no GA4, que podem ser aplicados a dados históricos em relatórios. O que não retroage são UTMs/eventos não coletados. Separar essas duas coisas.

17. **§4.1** — Regex perigosa: `chatgpt.com|claude.ai|perplexity.ai...` não escapa pontos nem ancora domínio. `chatgpt.com` casa `chatgptXcom` e domínios maliciosos contendo a string. Usar algo como `(^|\\.)chatgpt\\.com$` por domínio, conforme a sintaxe do GA4.

18. **§4.1 / §4.2 / §6 b2** — “NÃO inclui Perplexity” no canal nativo GA4 é claim muito específico e volátil. Precisa listar a tabela oficial de sources do GA4 ou marcar como “verificar antes de configurar”; caso contrário, o canal customizado pode duplicar/classificar errado.

19. **§4.1** — UTM sugerido `utm_source=llm` para “copiar link” é insuficiente e pode poluir atribuição. Se a tese depende de `medium=ai-assistant`, deveria recomendar também `utm_medium=ai-assistant` ou uma convenção própria explícita.

20. **§7** — “Nada das waves anteriores é revogado” contradiz “qualquer material antigo... está superado por esta wave”. Isso é revogação parcial. Para agentes, precisa declarar explicitamente: “revoga apenas claims que digam X”.
