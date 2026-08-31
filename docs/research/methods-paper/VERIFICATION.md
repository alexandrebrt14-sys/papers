# Verificação dos números do manuscrito

Cada afirmação quantitativa do `MANUSCRIPT.md` com o comando que a reproduz.
Rodar antes de submeter e a cada revisão que mexa em número.

O banco não é versionado em git (cruzou 100 MB). Obter a cópia corrente antes:

```bash
gh run download -R alexandrebrt14-sys/papers -n papers-db-latest -D /tmp/dbcheck
export DB=/tmp/dbcheck/papers.db
```

---

## §4.3 — Tabela do efeito da janela

A tabela inteira sai de um comando só. É o número mais importante do paper.

```bash
python scripts/harmonize_citation_window.py --db "$DB" --check --canonical-only
```

Esperado:

```
  braco              n   original  harmonizado    delta   linhas cortadas
  ChatGPT        14400      17.2%        17.2%    +0.0p                 0
  Claude         14266      25.8%        25.8%    +0.0p                 0
  Groq           14208       8.5%         8.5%    +0.0p                 0
  Gemini         14011       1.8%         1.8%    +0.0p                 0
  Perplexity      7148      75.8%        52.0%   -23.8p              7147
  Grok             158      39.2%        39.2%    +0.0p                 0
```

Os cinco deltas de +0,0 são a verificação, não decoração: eles provam que a
re-extração reproduz o instrumento original onde a janela não mudou. Se algum
deles se mover, a harmonização está introduzindo diferença própria e o número
da Perplexity deixa de ser confiável.

## §4.2 — Comprimento armazenado (a pista que revelou o defeito)

```bash
sqlite3 "$DB" "SELECT llm, COUNT(*), ROUND(AVG(length(response_text)),1),
  MIN(length(response_text)), MAX(length(response_text)),
  ROUND(100.0*SUM(CASE WHEN length(response_text)=200 THEN 1 ELSE 0 END)/COUNT(*),1)
  FROM citations GROUP BY llm ORDER BY 2 DESC;"
```

## §4.4 — Offsets da primeira menção

```bash
sqlite3 "$DB" "SELECT llm, COUNT(*), ROUND(AVG(first_entity_offset_v2),0),
  MAX(first_entity_offset_v2)
  FROM citations WHERE is_probe=0 AND cited_v2=1
  AND first_entity_offset_v2 IS NOT NULL GROUP BY llm ORDER BY 2 DESC;"
```

Perplexity além de 200 caracteres e observações que perdem a citação no corte:

```bash
sqlite3 "$DB" "SELECT
  SUM(CASE WHEN first_entity_offset_v2>200 THEN 1 ELSE 0 END) AS alem_de_200,
  COUNT(*) AS citadas
  FROM citations WHERE llm='Perplexity' AND is_probe=0 AND cited_v2=1
  AND first_entity_offset_v2 IS NOT NULL;"
```

## §5.3 — Recusas contadas como alucinação

O número que sustenta a taxonomia de três casos. Regex conservador: conta como
recusa apenas o que traz marcador explícito, então 67,4% é piso, não teto.

```bash
python - <<'PY'
import sqlite3, os, re
con = sqlite3.connect(os.environ["DB"]); con.row_factory = sqlite3.Row
rows = con.execute("""SELECT response_text FROM citations
    WHERE is_calibration=1 AND fictional_hit=1
    AND response_text IS NOT NULL AND length(response_text)>0""").fetchall()
pt = re.compile(r"n[ãa]o (tenho|encontrei|há|ha|existe|consigo|possuo|disponho|localizei)"
                r"|desconhe|sem informa|n[ãa]o (é|e) (uma|um) (empresa|institui)"
                r"|fict[ií]cia|n[ãa]o consta|nenhuma informa|n[ãa]o reconhe", re.I)
en = re.compile(r"i (don't|do not|couldn't|could not|cannot|can't) (have|find|know|locate)"
                r"|no (information|record|data|publicly)|not aware"
                r"|does not (appear|seem) to exist|fictional|unable to find"
                r"|i'm not familiar|no verifiable", re.I)
rec = sum(1 for r in rows if pt.search(r["response_text"]) or en.search(r["response_text"]))
print(f"marcadas como hallucination: {len(rows)}")
print(f"com marcador de recusa     : {rec} ({100*rec/len(rows):.1f}%)")
PY
```

Esperado: 15.993 marcadas, 10.775 com recusa (67,4%).

## §3.1 e §3.2 — Coorte e bateria

```bash
python - <<'PY'
from src.config_v2 import get_v2_cohort, get_v2_decoys, get_v2_queries, get_v2_adversarial_queries
reais, decoys, nq, na = set(), set(), 0, 0
for v in ("fintech","varejo","saude","tecnologia"):
    reais |= set(get_v2_cohort(v, include_anchors=True, include_decoys=False))
    decoys |= set(get_v2_decoys(v)); nq += len(get_v2_queries(v)); na += len(get_v2_adversarial_queries(v))
print(f"reais+anchors {len(reais)} · decoys {len(decoys)} · coorte {len(reais)+len(decoys)}")
print(f"canonical {nq} · probes {na}")
PY
```

Esperado: 111 reais+anchors, 16 decoys, coorte 127, 192 canônicas, 64 probes.

## §7.1 — Ledger de gaps

```bash
sqlite3 "$DB" "SELECT
  (SELECT COUNT(DISTINCT date(timestamp)) FROM citations) AS dias_com_dado,
  (SELECT COUNT(*) FROM collection_runs WHERE status='aborted') AS abortadas,
  (SELECT COUNT(*) FROM collection_runs WHERE status='success') AS ok;"
```

## §1 e §10 — Volume e cobertura de teste

```bash
sqlite3 "$DB" "SELECT COUNT(*) FROM citations;"                       # 80.638
sqlite3 "$DB" "SELECT COUNT(*) FROM citations WHERE is_probe=0;"      # 64.191
python -m pytest -q | tail -1
```

O manuscrito cita 223 testes passando no momento da descoberta, em 31/08/2026,
antes das correções. A suíte hoje tem mais, porque as correções trouxeram os
seus. O ponto do §10 é que 223 testes verdes não detectaram o defeito — se for
atualizar o número, atualizar junto a data a que ele se refere.

---

## Regra

Nenhum número entra no manuscrito sem constar desta lista com o comando que o
produz. Se um número aparecer no texto e não aqui, ou ele saiu de uma medição
que ninguém consegue repetir, ou saiu de lugar nenhum.
