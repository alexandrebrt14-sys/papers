#!/usr/bin/env bash
# 5 waves do board (5 LLMs) — PEER REVIEW do draft + respostas complementares.
# Saidas em pr_wave_N.log neste diretorio.
set -u
DIR="C:/Sandyboxclaude/papers/docs/research/fintech-citation-advantage"
BRIDGE="C:/Sandyboxclaude/scripts/bin/geo-bridge.sh"

CTX="Estudo: citacao espontanea de marcas brasileiras por 5 LLMs (ChatGPT gpt-4o-mini, Claude haiku-4.5, Gemini 2.5-pro, Perplexity sonar, Groq llama-3.3-70b), 4 verticais (fintech, varejo, tecnologia, saude), 62.820 observacoes (23/abr-09/jun/2026, dia 50 de 90 da janela), 48 queries template-paralelas por vertical (0/48 mencionam marca), nucleo n=50.453. Resultados: fintech 28,15% > varejo 24,94% > tecnologia 14,50% > saude 13,35% (p<1e-8). PORENS verificados: (1) Nubank = 49,68% das mencoes fintech; excluindo respostas so-Nubank a taxa fintech cai para 11,46% (ultimo lugar) e a OR vs saude inverte de 4,13 para 0,77; (2) apenas 2 de 5 engines mostram fintech>varejo (Claude +20pp e Gemini; ChatGPT, Groq e Perplexity mostram o contrario); (3) ARTEFATO: response_text truncado em 200 chars em 4 dos 5 coletores (so Perplexity integro) - o NER mede citacao na ABERTURA da resposta (front-loading), nao citacao plena; (4) decoys ficticios com especificidade quase nula (FPR ~97-99%); (5) dependencia estatistica: 48 queries x ~293 repeticoes = n efetivo ~240 clusters, exige GLMM cluster-robusto. Tese pivotada do paper: Anchor-Entity Concentration in LLM Brand Citations - a visibilidade setorial em LLMs e dominada por entidades-ancora (caso Nubank), com heterogeneidade radical por engine e licoes de medicao. Janela v2 aberta ate ~21/jul permite re-coleta sem truncamento."

run_wave () {
  local n="$1"; shift
  local demanda="$1"
  echo "=== PR_WAVE $n start $(date -u +%H:%M:%S) ==="
  bash "$BRIDGE" board "$demanda" > "$DIR/pr_wave_${n}.log" 2>&1
  echo "=== PR_WAVE $n exit=$? end $(date -u +%H:%M:%S) ==="
}

run_wave 1 "Voce e um painel de revisores por pares de ICWSM/WWW/TOIS avaliando o estudo a seguir. $CTX TAREFA: emita o RELATORIO DE REVISAO mais duro e completo possivel: 12+ criticas e gaps priorizados (major/minor), cobrindo validade de construto, desenho, estatistica, framing, novidade e etica de auditoria de marcas. NAO repita o que ja esta admitido (truncamento, Nubank, clusters) sem ADICIONAR angulo novo - procure o que AINDA NAO foi percebido. Responda em portugues do Brasil."

run_wave 2 "Voce e um painel de especialistas em GEO e NLP empirico. $CTX TAREFA: o truncamento em 200 chars pode virar FEATURE? Avalie reframing 'citacao em abertura de resposta' (front-loading) como metrica valida de saliencia primaria de marca: fundamento cognitivo/IR (primacy, serial position), o que muda nas claims, como validar com o subset Perplexity integro (comparar taxa nos primeiros 200 chars vs resposta completa), e desenho da re-coleta dual-track (resposta integra + janela de abertura). Liste analises complementares concretas executaveis no SQLite atual. Responda em portugues do Brasil."

run_wave 3 "Voce e um painel de economistas e estrategistas de mercado. $CTX TAREFA: construa a EXPLICACAO DEFINITIVA em camadas de POR QUE a vertical fintech obtem mais citacoes em motores generativos (GEO): (a) por que o setor fintech BR produz a entidade-ancora mais forte (Nubank como marca-categoria: 100+ milhoes de clientes, IPO NYSE, cobertura massiva de imprensa tech global e local, Pix/Open Finance como infraestrutura narrativa, midia especializada densa); (b) por que isso se converte em probabilidade de citacao em LLM (densidade de corpus, consenso entre fontes, nome unico sem ambiguidade lexical); (c) por que varejo chega perto (Mercado Livre/Magalu) e tecnologia B2B e saude ficam atras (fragmentacao, YMYL/cautela regulatoria); (d) implicacoes praticas de GEO para marcas que querem ser citadas. Profundo e citavel. Responda em portugues do Brasil."

run_wave 4 "Voce e um painel de metodologistas. $CTX TAREFA: especifique as RESPOSTAS COMPLEMENTARES robustas as 5 fraquezas verificadas, uma a uma: (1) truncamento - dual-track e validacao com Perplexity; (2) efeito Nubank - desenho de decomposicao formal (Gini/HHI por vertical, jackknife por entidade, modelo com efeito aleatorio de entidade); (3) inconsistencia entre engines - tratar heterogeneidade como achado com meta-analise por engine (forest plot); (4) decoys com especificidade nula - redesenho dos nomes ficticios e do criterio de match; (5) clusters - especificacao GLMM exata (formula, software, graus de liberdade). Para cada uma: o paragrafo de resposta ao revisor pronto para usar. Responda em portugues do Brasil."

run_wave 5 "Voce e um painel de editores de periodico e cientistas de dados. $CTX TAREFA: monte o PACOTE FINAL DE PUBLICACAO: (a) figuras-chave do paper (6 figuras: descricao exata de cada uma, eixos, dados); (b) tabelas obrigatorias; (c) secao de implicacoes praticas para GEO/marketing; (d) declaracoes de etica, dados e reproducibilidade; (e) carta ao editor (cover letter) em 200 palavras EN; (f) cronograma realista de submissao considerando re-coleta ate 21/jul. Responda em portugues do Brasil."

echo "ALL_PR_WAVES_DONE"
