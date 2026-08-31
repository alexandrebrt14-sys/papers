"""Migration 0010 — response_full_text + citation_window_chars.

Health-check 2026-08-31. A extração de entidades sempre rodou sobre
`response_text`, e `response_text` nunca foi a resposta do modelo: em cinco dos
seis braços era `text[:200]`, os primeiros 200 caracteres. A Perplexity escapou
do corte por usar outro caminho no cliente (`_query_perplexity` gravava o texto
inteiro, até 2.502 caracteres). Duas consequências:

1. A janela de observação era **assimétrica entre os braços** do estudo, e a
   comparação entre motores — o objeto do paper — ficou confundida com o
   tamanho da janela. Recortando a Perplexity nos mesmos 200 caracteres, sua
   taxa de citação cai de 75,8% para 52,0%: 23,8 pontos eram instrumento, não
   comportamento do modelo.
2. Nenhuma resposta ficou auditável na íntegra. Sem o texto completo não há
   como um revisor reproduzir a extração, nem como o projeto medir o que a
   janela deixa de fora.

Esta migration não altera dado existente. Ela abre espaço para o que passa a
ser gravado daqui em diante:

- `response_full_text` — a resposta completa, antes de qualquer corte.
- `citation_window_chars` — o tamanho da janela sob a qual AQUELA linha foi
  extraída, para que a fronteira fique legível na própria tabela em vez de
  depender de quem lembra da data da mudança.

Linhas antigas ficam com `response_full_text` NULL e `citation_window_chars`
NULL, o que é a leitura correta: para elas a íntegra não existe e a janela
efetiva precisa ser inferida do braço (200 em todos, menos Perplexity).
O backfill de `citation_window_chars` abaixo escreve essa inferência.

Forward-only.
"""
from __future__ import annotations

import logging
import sqlite3

logger = logging.getLogger(__name__)

# Janela canônica da série: os 200 caracteres iniciais da resposta.
DEFAULT_WINDOW_CHARS = 200


def apply(conn: sqlite3.Connection) -> list[str]:
    cur = conn.cursor()
    existing = {r[1] for r in cur.execute("PRAGMA table_info(citations)").fetchall()}

    added = []
    if "response_full_text" not in existing:
        cur.execute("ALTER TABLE citations ADD COLUMN response_full_text TEXT")
        added.append("response_full_text")
    if "citation_window_chars" not in existing:
        cur.execute("ALTER TABLE citations ADD COLUMN citation_window_chars INTEGER")
        added.append("citation_window_chars")

    conn.commit()
    logger.info("migrate_0010_full_response: added %d cols: %s", len(added), added)
    return added


def backfill_window(conn: sqlite3.Connection) -> int:
    """Anota a janela efetiva sob a qual cada linha histórica foi extraída.

    Não é estimativa: `length(response_text)` é exatamente o que o extrator viu,
    porque a extração rodou sobre essa string. Para os braços truncados o valor
    dá 200 (ou menos, quando a resposta inteira era mais curta que a janela);
    para a Perplexity dá o comprimento real da resposta, que é justamente a
    assimetria que a coluna torna visível.
    """
    cur = conn.cursor()
    cur.execute(
        "UPDATE citations SET citation_window_chars = length(response_text) "
        "WHERE citation_window_chars IS NULL AND response_text IS NOT NULL"
    )
    n = cur.rowcount
    conn.commit()
    logger.info("backfill citation_window_chars: %d rows", n)
    return n
