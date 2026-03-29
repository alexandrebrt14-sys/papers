# Incidente: Pipeline de Coleta Parado por 4 Dias

**Data do incidente:** 2026-03-25 a 2026-03-29
**Data da resolução:** 2026-03-29
**Severidade:** Alta — coleta de dados completamente interrompida
**Impacto:** 4 dias de dados perdidos (25, 27, 28, 29/mar), páginas /research e /papers-roadmap desatualizadas

---

## Resumo Executivo

Um SyntaxError introduzido no commit `0e6e709` (25/mar) quebrou toda a cadeia de imports do Python, impedindo qualquer execução do CLI. O erro foi mascarado por `|| true` nos workflows do GitHub Actions, que reportavam "success" mesmo sem executar nada. A coleta ficou silenciosamente morta por 4 dias.

---

## Timeline

| Data | Evento |
|------|--------|
| 25/mar 21:59 | Commit `0e6e709` (feat: add Groq/Llama 3.3 70B) introduz f-string com aspas aninhadas em `tracker.py:613` |
| 25/mar 22:00+ | Todos os comandos `python -m src.cli` passam a falhar com SyntaxError |
| 26/mar 09:00 | Daily collection "sucede" no CI (|| true mascara o erro) — 0 dados coletados |
| 26/mar 20:01 | Última coleta REAL (rodada localmente, não via CI) — DB chega a 397 citações |
| 27-29/mar | Daily collections continuam "sucedendo" no CI sem coletar nada |
| 27-29/mar | FinOps Monitor falha corretamente (sem || true) — mas ninguém investiga |
| 29/mar 11:22 | Weekly Benchmark falha no step "FinOps monitor cycle" |
| 29/mar 13:32 | Investigação iniciada via `geo preflight` |
| 29/mar 16:51 | Fix aplicado, coleta local executada com sucesso (64 novas citações) |
| 29/mar 17:05 | Push do fix, FinOps Monitor passa no CI pela primeira vez em 4 dias |

---

## Causa Raiz

### O bug

Linha 613 de `src/finops/tracker.py`:

```python
# ANTES (Python 3.12 OK, Python 3.11 FALHA)
f'["{(row[6] or "").replace(",", '","')}"]'

# DEPOIS (compatível com todas as versões)
json.dumps((row[6] or "").split(","))
```

Python 3.12 (PEP 701) permite aspas aninhadas em f-strings. Python 3.11 (usado no CI) não permite. O código foi escrito e testado localmente com 3.12, mas o CI roda 3.11.

### Por que não foi detectado

1. **`|| true` nos steps de coleta** — O daily-collect.yml tinha `python -m src.cli ... collect citation || true`, que silencia qualquer falha incluindo SyntaxError
2. **CI reportava "success"** — O workflow inteiro passava sem alertas
3. **Commits automáticos continuavam** — `git diff --cached --quiet || git commit` commitava docs atualizados mesmo sem dados novos
4. **FinOps Monitor falhava, mas era ignorado** ��� O monitor standalone (sem || true) falhava corretamente, mas as falhas não tinham alerta configurado

### A cadeia de imports

```
cli.py → collectors/__init__.py → base.py → finops/tracker.py → SyntaxError
```

Qualquer comando `python -m src.cli` falhava imediatamente no import, antes de executar qualquer lógica.

---

## O que foi corrigido

### 1. SyntaxError no tracker.py
- Substituído f-string com aspas aninhadas por `json.dumps()`
- Adicionado `import json` no topo do arquivo
- Verificado com `ast.parse()` que todos os arquivos .py do projeto compilam sem erros

### 2. Workflows endurecidos (3 arquivos)

**daily-collect.yml:**
- Adicionado step "Validate Python imports" antes de qualquer coleta
- Removido `|| true` do Citation Tracker (step crítico — deve falhar alto)
- Trocado `|| true` por `continue-on-error: true` no FinOps (visível no GitHub mas não bloqueia)

**weekly-benchmark.yml:**
- Adicionado step "Validate Python imports"
- Removido `|| true` da coleta principal

**finops-monitor.yml:**
- Adicionado step "Validate Python imports"

### 3. Coleta executada e verificada
- 64 novas citações coletadas (fintech, 4 LLMs)
- Total DB: 461 citações (era 397)
- FinOps checkpoint atualizado com gastos reais

---

## Dados perdidos

| Dia | Citações esperadas | Citações coletadas | Status |
|-----|--------------------|--------------------|--------|
| 25/mar | ~64/vertical | 0 | Perdido |
| 27/mar | ~64/vertical | 0 | Perdido |
| 28/mar | ~64/vertical | 0 | Perdido |
| 29/mar manhã | ~64/vertical | 0 | Perdido (CI) |
| 29/mar tarde | ~64 (fintech) | 64 | Recuperado (local) |

**Estimativa de perda:** ~768 citações (4 dias x 4 verticais x ~48 citações/vertical) não foram coletadas. Esses dados são irrecuperáveis (respostas de LLMs são não-determinísticas e variam dia a dia).

---

## Lições Aprendidas

### 1. `|| true` é veneno em pipelines de dados
**Regra:** NUNCA usar `|| true` em steps que produzem dados. Usar `continue-on-error: true` (que mostra warning no GitHub) ou simplesmente deixar falhar.

### 2. Validação de imports é barata e salva dias
**Regra:** Sempre ter um step de "smoke test" que importa os módulos críticos antes de rodar coleta. Custo: 2 segundos. Benefício: detecta qualquer quebra de import instantaneamente.

### 3. Python 3.11 vs 3.12 é uma armadilha real
**Regra:** Se o CI roda 3.11, desenvolver localmente com 3.11 também. Ou: ter um check de sintaxe (`py_compile` ou `ast.parse`) que roda com a versão do CI.

### 4. "Success" no CI não significa que dados foram coletados
**Regra:** O critério de sucesso deve ser verificável — ex: checar que o DB cresceu, que `collection_runs` tem registro novo, que o count de citações aumentou.

### 5. Workflows de monitoramento devem alertar
**Regra:** O FinOps Monitor falhava corretamente, mas ninguém via. Configurar alertas (email/Slack) para falhas em workflows scheduled.

---

## Ações de seguimento

- [x] Fix do SyntaxError
- [x] Hardening dos 3 workflows
- [x] Coleta local de teste bem-sucedida
- [x] Push e validação no CI (FinOps Monitor passou)
- [ ] Rodar coleta completa das 4 verticais para o dia de hoje
- [ ] Configurar Supabase sync para que /research mostre dados reais
- [ ] Criar tabelas `papers_dashboard_data` e `papers_finops` no Supabase
- [ ] Adicionar RESEND_API_KEY aos GitHub Secrets para relatórios por email
- [ ] Considerar migrar CI para Python 3.12 (alinhado com ambiente local)
- [ ] Adicionar check de contagem de citações no finalize job do daily
