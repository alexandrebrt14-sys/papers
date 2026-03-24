# Guia de Obtenção de API Keys — Papers

## 1. OpenAI (ChatGPT) — ~$2/mês

1. Acesse https://platform.openai.com/api-keys
2. Faça login com sua conta
3. Clique em "Create new secret key"
4. Nome: `papers-fintech-research`
5. Copie a key (formato: `sk-...`)
6. Adicione crédito mínimo: $5 (Settings > Billing)

**Modelo usado:** `gpt-4o` (custo: ~$0.005/1K tokens)

## 2. Anthropic (Claude) — ~$2/mês

1. Acesse https://console.anthropic.com/settings/keys
2. Faça login com sua conta
3. Clique em "Create Key"
4. Nome: `papers-fintech-research`
5. Copie a key (formato: `sk-ant-...`)
6. Adicione crédito mínimo: $5 (Settings > Plans & Billing)

**Modelo usado:** `claude-sonnet-4-20250514` (custo: ~$0.003/1K tokens)

## 3. Google AI (Gemini) — GRÁTIS

1. Acesse https://aistudio.google.com/apikey
2. Faça login com sua conta Google
3. Clique em "Create API Key"
4. Selecione o projeto existente ou crie "papers-fintech"
5. Copie a key (formato: `AI...`)

**Modelo usado:** `gemini-2.0-flash` (grátis: 15 RPM, 1M tokens/dia)

## 4. Perplexity — ~$5/mês (mínimo)

1. Acesse https://www.perplexity.ai/settings/api
2. Faça login
3. Clique em "Generate API Key"
4. Copie a key (formato: `pplx-...`)
5. Adicione crédito mínimo: $5

**Modelo usado:** `sonar` (custo: ~$0.005/1K tokens)

## 5. SerpAPI (opcional) — $50/mês ou grátis (100 buscas)

1. Acesse https://serpapi.com/users/sign_up
2. Registre uma conta
3. Plano gratuito: 100 buscas/mês (suficiente para começar)
4. Copie a key em Dashboard > API Key

## Após obter as keys

### Opção A: GitHub Secrets (para Actions automatizados)
```bash
bash scripts/setup-secrets.sh
```

### Opção B: .env local (para testes locais)
```bash
cp .env.example .env
# Edite .env com as keys
```

### Opção C: Via API do GitHub (sem gh CLI)
```bash
# Use o script Python:
python scripts/set-github-secrets.py
```

## Custo Mensal Estimado

| Provedor | Custo | Queries/dia | Total/mês |
|----------|-------|-------------|-----------|
| OpenAI | ~$2 | 55 queries | 1.650 |
| Anthropic | ~$2 | 55 queries | 1.650 |
| Google AI | $0 | 55 queries | 1.650 |
| Perplexity | ~$5 | 55 queries | 1.650 |
| SerpAPI | $0 | 13/semana | ~52 |
| **Total** | **~$9/mês** | | |
