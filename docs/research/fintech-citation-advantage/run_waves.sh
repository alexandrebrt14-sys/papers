#!/usr/bin/env bash
# 5 waves do board (5 LLMs em paralelo por wave) — insumos para o artigo
# "Fintech Citation Advantage". Saidas em wave_N.json/log neste diretorio.
set -u
DIR="C:/Sandyboxclaude/papers/docs/research/fintech-citation-advantage"
REPO="C:/Sandyboxclaude/papers"
BRIDGE="C:/Sandyboxclaude/scripts/bin/geo-bridge.sh"

# Doutrina editorial v4 (11/08/2026): regra em DIRETRIZ_EDITORIAL.md, exemplo em
# GUIA_ESCRITA_HUMANIZADA.md, tradução para este repo em
# DOUTRINA_EDITORIAL_NESTE_REPO.md, todos na raiz. Prompt não recebe link: as
# regras viajam DENTRO da demanda, porque instrução carregada só no contexto do
# agente não sobrevive a geração longa. O arquivo abaixo é a versão condensada.
BLOCO_FILE="$REPO/scripts/prompts/BLOCO_EDITORIAL_PROMPT.md"
if [ ! -s "$BLOCO_FILE" ]; then
  echo "ERRO: $BLOCO_FILE ausente ou vazio. Sem ele as waves geram texto fora do padrão editorial; abortando em vez de rodar sem a regra." >&2
  exit 1
fi
BLOCO="$(cat "$BLOCO_FILE")"

DATA="Dataset: 62.820 observacoes (queries a 5 LLMs: ChatGPT gpt-4o-mini, Claude haiku-4.5, Gemini 2.5-pro, Perplexity sonar, Groq llama-3.3-70b), 23/abr a 09/jun de 2026, 4 verticais brasileiras (fintech, varejo, tecnologia, saude), cohort de 127 entidades (79 BR reais + 32 ancoras internacionais + 16 decoys ficticios), 2 coletas/dia via GitHub Actions, NER v2, probes adversariais e calibracao com decoys. Nucleo sem probes/calibracao: n=50.453, taxa global de citacao espontanea 20,3%. Taxas por vertical: fintech 28,15% (IC95 27,38-28,95), varejo 24,94%, tecnologia 14,50%, saude 13,35% — qui-quadrado fintech vs varejo p=7e-9, vs tecnologia e saude p<1e-15. Interacao vertical x LLM: Claude cita fintech em 51,0% vs 10,4% tecnologia; Perplexity 86,5% fintech vs 54,3% tecnologia; Gemini quase zero fora de fintech (4,9% fintech, 0,0% varejo/saude). Concentracao de mencoes: Nubank sozinho = 3.533 de 7.112 mencoes fintech (49,7%); top3 fintech = 70,9% (HHI 0,283, o mais alto); tecnologia HHI 0,110. Roster: fintech 19 entidades vs 15 nas demais. FPR dos decoys baixo (calibracao ok)."

run_wave () {
  local n="$1"; shift
  local demanda="$1"
  local demanda_full
  demanda_full="$demanda

$BLOCO"
  # Teto de 5 KB de input do orchestrator (ROADMAP_2026Q2-Q4.md, "Política de
  # qualidade"). Aviso visível em vez de truncamento silencioso.
  local tam
  tam=$(printf '%s' "$demanda_full" | wc -c)
  if [ "$tam" -gt 5000 ]; then
    echo "AVISO: demanda da wave $n tem $tam bytes, acima do teto de 5000 do orchestrator. Encurte o contexto da wave, não o bloco editorial." >&2
  fi
  echo "=== WAVE $n start $(date -u +%H:%M:%S) (demanda $tam bytes) ==="
  bash "$BRIDGE" board "$demanda_full" > "$DIR/wave_${n}.log" 2>&1
  echo "=== WAVE $n exit=$? end $(date -u +%H:%M:%S) ==="
}

run_wave 1 "Voce e um painel de especialistas em GEO (Generative Engine Optimization) e LLMs. $DATA PERGUNTA CENTRAL: por que a vertical fintech obtem taxa de citacao espontanea sistematicamente maior que varejo, tecnologia e saude em LLMs? Gere o conjunto mais completo possivel de HIPOTESES MECANICISTAS testaveis (minimo 10), cada uma com: nome, mecanismo causal detalhado (training data density, digital-first content, midia especializada, brand entity strength tipo Nubank, frequencia em corpora PT-BR, estrutura competitiva do setor, recencia, RAG vs conhecimento parametrico), predicoes observaveis no dataset descrito, e como falsea-la. Considere tambem que ~50% das mencoes fintech sao Nubank: o efeito e da vertical ou de uma entidade-estrela? Responda em portugues do Brasil."

run_wave 2 "Voce e um painel de pesquisadores academicos em information retrieval, NLP e media studies. $DATA TAREFA: construa o ENQUADRAMENTO TEORICO para um artigo peer-reviewed que explica vies setorial de citacao em LLMs. Conecte com literaturas: visibility bias e source preference em LLMs, GEO (Aggarwal et al. 2024), brand entity salience, knowledge cutoff e training data composition, popularity bias em sistemas de recomendacao, teoria de agenda-setting aplicada a IA generativa, economia da atencao. Para cada corrente: conceitos-chave, autores/trabalhos seminais e como nosso resultado contribui/contradiz. Proponha 3 frames teoricos candidatos para o paper e recomende 1. Responda em portugues do Brasil."

run_wave 3 "Voce e um painel de estatisticos e metodologistas de pesquisa quantitativa. $DATA TAREFA: especifique o PLANO DE ANALISE ESTATISTICA completo para sustentar em peer review a claim 'fintech obtem mais citacoes': modelo principal (regressao logistica multinivel com efeitos de LLM, categoria de query, idioma, semana; cluster-robust SE), tratamento da concentracao Nubank (leave-one-out, efeitos por entidade), normalizacao por tamanho de roster (19 vs 15), testes de robustez, correcao de multiplas comparacoes, tamanhos de efeito (odds ratio, risk difference) com ICs, analise de poder, e o que reportar (tabelas/figuras). Aponte tambem quais analises ADICIONAIS precisamos rodar no SQLite antes de submeter. Responda em portugues do Brasil."

run_wave 4 "Voce e um painel red-team de revisores cetico-hostis de um periodico A1 (Information Sciences / ACM TOIS). $DATA TAREFA: liste TODAS as ameacas a validade e objecoes que um revisor faria contra a claim 'fintech obtem mais citacoes por causa de X': vies de construcao do roster (19 vs 15; selecao das marcas), vies das queries (mix de categorias difere?), NER v2 (alias matching favorece nomes unicos tipo Nubank?), confundimento Perplexity-RAG vs modelos parametricos, janela curta, modelos mini/haiku nao representativos, generalizabilidade alem do Brasil, multiple testing, e qualquer outra. Para cada objecao: gravidade (alta/media/baixa), resposta possivel com os dados existentes, ou experimento adicional necessario. Responda em portugues do Brasil."

run_wave 5 "Voce e um painel de editores academicos experientes em NLP/IR. $DATA TAREFA: proponha a ESTRUTURA COMPLETA do artigo (IMRaD detalhado, secao a secao com bullets do conteudo), 5 titulos candidatos (EN), abstract candidato (EN, 250 palavras), 4 contribution claims defensaveis, venues-alvo ranqueadas (Information Sciences, ACM TOIS, EMNLP/ACL findings, ICWSM, Web Conference) com justificativa de fit, e checklist de artefatos para reproducibilidade (dataset publico, codigo, manifests SHA-256). Considere que o dataset e publico no GitHub e ja existem papers companion na SSRN/Zenodo do mesmo grupo. Responda em portugues do Brasil."

echo "ALL_WAVES_DONE"
