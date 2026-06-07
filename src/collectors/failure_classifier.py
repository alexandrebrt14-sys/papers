"""Citation status derivation + failure taxonomy (Migration 0009).

Materializa, na camada de coleta, a distinção seleção × absorção de citação
(arXiv:2604.25707) e a taxonomia de 7 tipos de falha (arXiv:2603.09296) que o
schema passou a suportar via Migration 0009.

Definições observacionais (proxies, não ground-truth do motor):

- **selection_status** (CSR por observação): a fonte da entidade foi
  *selecionada* para o conjunto de fontes da resposta — i.e., o domínio/slug da
  entidade aparece na lista de fontes (`sources`) que o motor expôs. É a camada
  de busca do framework de absorção.
- **absorption_status** (CAR por observação): a entidade foi *absorvida* no
  texto final — i.e., foi efetivamente citada/nomeada no corpo da resposta. É a
  camada de geração.

As duas são distintas: uma entidade pode ser absorvida (nomeada no texto) sem
ser selecionada (sem fonte linkada) — isso é `attribution-drop`; e pode ser
selecionada (na lista de fontes) sem ser absorvida (listada, não discutida).

failure_type (enum, None = sem falha): broken-fetch | parsing-failure |
retrieval-miss | summarization-collapse | attribution-drop |
hallucinated-source | blocked-by-robots. Apenas os casos detectáveis de forma
robusta na camada de observação são classificados; o resto fica None.
"""
from __future__ import annotations

import re
from collections.abc import Iterable, Sequence

FAILURE_TYPES: tuple[str, ...] = (
    "broken-fetch",
    "parsing-failure",
    "retrieval-miss",
    "summarization-collapse",
    "attribution-drop",
    "hallucinated-source",
    "blocked-by-robots",
)

_NON_ALNUM = re.compile(r"[^a-z0-9]+")


def slug(name: str) -> str:
    """Normaliza um nome de entidade para matching de domínio.

    "Mercado Pago" -> "mercadopago"; "C6 Bank" -> "c6bank".
    """
    return _NON_ALNUM.sub("", (name or "").lower())


def _entity_in_sources(entity: str, sources: Iterable[str]) -> bool:
    s = slug(entity)
    if len(s) < 3:  # slugs curtos demais geram falso-positivo em URLs
        return False
    for src in sources or ():
        if s in slug(str(src)):
            return True
    return False


def derive_citation_status(
    *,
    cited: bool,
    cited_entities: Sequence[str],
    cohort: Sequence[str],
    sources: Sequence[str],
) -> tuple[int | None, int | None]:
    """Deriva (selection_status, absorption_status) para uma observação.

    - absorption = 1 se qualquer entidade do cohort foi citada no texto (`cited`).
    - selection  = 1 se qualquer entidade do cohort tem fonte no source set.

    Retorna ints (0/1). Não retorna None aqui — a ausência de dados é tratada
    como 0 (nem selecionado, nem absorvido), o que é o significado correto:
    quando não há fontes e não há citação, ambos são falsos, não "desconhecido".
    Use NULL no schema apenas para linhas legacy gravadas antes da migration.
    """
    absorption = 1 if cited else 0
    # selection: testa cohort inteiro (uma entidade pode estar na lista de
    # fontes mesmo sem ter sido nomeada no texto).
    candidates = list(cited_entities) or list(cohort)
    selection = 1 if any(_entity_in_sources(e, sources) for e in candidates) else 0
    return selection, absorption


def classify_failure(
    *,
    cited: bool,
    selection_status: int | None,
    absorption_status: int | None,
    fictional_hit: bool = False,
    response_error: str | None = None,
    response_text: str | None = None,
    expected: bool = False,
) -> str | None:
    """Classifica o tipo de falha de citação. None = sem falha detectável.

    Cobre os casos robustamente detectáveis na camada de observação:
      - broken-fetch:        erro de rede/HTTP na chamada (response_error).
      - parsing-failure:     resposta vazia/sem texto sem erro de transporte.
      - hallucinated-source: citou entidade fictícia (fictional_hit).
      - attribution-drop:    absorvida mas não selecionada (texto sem fonte).
      - retrieval-miss:      esperada (expected) mas nem citada nem em fontes.
    Os demais (summarization-collapse, blocked-by-robots) exigem sinais de
    infraestrutura indisponíveis aqui e ficam como None.
    """
    if response_error:
        low = response_error.lower()
        if "robot" in low or "403" in low or "forbidden" in low:
            return "blocked-by-robots"
        return "broken-fetch"
    if response_text is not None and not response_text.strip():
        return "parsing-failure"
    if fictional_hit:
        return "hallucinated-source"
    if absorption_status == 1 and selection_status == 0:
        return "attribution-drop"
    if expected and not cited and selection_status == 0:
        return "retrieval-miss"
    return None
