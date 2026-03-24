#!/bin/bash
# Setup GitHub Secrets para o repositório papers
# Uso: bash scripts/setup-secrets.sh
#
# Pré-requisito: gh auth login (ou GH_TOKEN configurado)

REPO="alexandrebrt14-sys/papers"

echo "=== Configurando GitHub Secrets para $REPO ==="
echo ""

# Verificar se gh está autenticado
if ! gh auth status &>/dev/null; then
  echo "ERRO: gh CLI não autenticado. Execute: gh auth login"
  exit 1
fi

# Função para setar secret
set_secret() {
  local name=$1
  local prompt=$2

  read -sp "$prompt: " value
  echo ""

  if [ -n "$value" ]; then
    echo "$value" | gh secret set "$name" -R "$REPO"
    echo "  [OK] $name configurado"
  else
    echo "  [SKIP] $name vazio — pulando"
  fi
}

echo "Cole cada API key quando solicitado (input oculto):"
echo ""

set_secret "OPENAI_API_KEY" "OpenAI API Key (sk-...)"
set_secret "ANTHROPIC_API_KEY" "Anthropic API Key (sk-ant-...)"
set_secret "GOOGLE_AI_API_KEY" "Google AI API Key (AI...)"
set_secret "PERPLEXITY_API_KEY" "Perplexity API Key (pplx-...)"
set_secret "SERPAPI_KEY" "SerpAPI Key (opcional, Enter para pular)"

echo ""
echo "=== Verificando secrets configurados ==="
gh secret list -R "$REPO"
echo ""
echo "Pronto! Os GitHub Actions vão usar essas keys automaticamente."
