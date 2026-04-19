# Auditoria 2026-03-26 (arquivo histórico)

Snapshot da auditoria estatística feita quando o projeto tinha N=397 observações.

Estado na época:
- 4 verticais ativas com 5 LLMs configurados
- Persistência SQLite + Supabase já funcionando
- Pipeline diário ativo mas ainda sem incidente de abril/2026 resolvido
- Entidades fictícias ainda não acionadas nas queries

## Arquivos

- [EXECUTIVE_SUMMARY.txt](EXECUTIVE_SUMMARY.txt) — resumo executivo para stakeholders
- [MATRIX.txt](MATRIX.txt) — matriz de achados
- [STATISTICAL_METHODOLOGY.md](STATISTICAL_METHODOLOGY.md) — revisão da metodologia estatística

## Por que está arquivado

Essas auditorias refletem um estado que não existe mais:
- N aumentou para 1.244+ após a expansão de queries de 16/04
- Pipeline foi endurecido após incidente de 08-12/04 (papers.db como source-of-truth no git)
- Pricing e modelos mudaram (Gemini 2.5 Pro, Groq adicionado)

A auditoria ativa mais recente vive em [`../../audits/2026-04-19/`](../2026-04-19/).

Consulte estes arquivos apenas como contexto histórico — não use para decisões atuais.
