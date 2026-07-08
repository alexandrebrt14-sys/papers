# Política de Segurança

## Como reportar uma vulnerabilidade

Este é um repositório de pesquisa mantido por uma pessoa. Se você encontrar
uma vulnerabilidade (segredo exposto, injeção em script, dependência
comprometida), reporte de forma privada:

- **E-mail:** ti@brasilgeo.ai
- Ou abra um **Security Advisory** privado neste repositório
  (aba *Security* → *Report a vulnerability*).

Não abra issue pública com detalhes exploráveis. Resposta esperada em até
7 dias corridos.

## Escopo

- Código em `src/`, `scripts/` e workflows em `.github/workflows/`.
- Segredos: o repo usa GitHub Actions Secrets e `.env` local (ignorado no
  git, com `.env.example` versionado). Qualquer segredo real encontrado no
  histórico deve ser reportado imediatamente.
- `data/papers.db` contém apenas respostas brutas de LLMs coletadas pelo
  próprio estudo — não contém credenciais nem dados pessoais.

## Verificações automáticas

- `security-scan.yml`: bandit + pip-audit + gitleaks, semanal e em PRs que
  tocam Python ou requirements. Severidade alta bloqueia o PR.
