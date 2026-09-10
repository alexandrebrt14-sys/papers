"""dashboard_public.py — regras de integridade do dashboard_data.json público.

Três defeitos observados no arquivo publicado em 09/09/2026 (commit 5f09e65):

1. `topEntities`, `weeklyDeltas`, `verticalsFull[*].citedEntities` e
   `crossVerticalEntities` misturavam decoys fictícios de calibração (Banco
   Floresta Digital, FinPay Solutions, ShopNova Digital, DataBridge Brasil...)
   com marcas reais. A origem é o probe adversarial `calibracao_fp`: o nome
   fictício vai dentro da pergunta, o modelo o ecoa (~95% de "citação") e a
   linha entra em `citation_context` como qualquer outra. O bloco
   `calibration` já excluía probes ao medir falso-positivo (0,0%), mas os
   rankings públicos não. Quem publicasse o "top 10" citava empresa que não
   existe.
2. `verticalsFull.fintech.coverage` = 118,8%: 19 entidades citadas para 16 no
   roster, porque o numerador contava toda entidade detectada (fictícias e
   âncoras fora do roster) e o denominador só o roster. Coverage é "quantas
   marcas DO ROSTER apareceram ao menos uma vez", limitado a 100%.
3. `windowEnd` = 2026-07-21 com `lastCollection` em 09/09: a data era o 90º
   dia de CALENDÁRIO a partir de 23/04, mas a janela é de 90 dias COLETADOS
   (ver `collectedDays`), e a coleta seguiu depois de julho. Quem lia
   `windowEnd` concluía que a pesquisa tinha acabado.

Este módulo é puro (sem banco) para que as mesmas funções sirvam ao gerador
(`scripts/generate_dashboard_json.py`) e a um pós-processamento determinístico
do JSON já publicado (`--from-json`), e para que o teste prove por mutação que
uma fictícia injetada é removida.
"""
from __future__ import annotations

import json
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Iterable

WINDOW_TOTAL_DAYS = 90

# Marcador que o dashboard carrega para que a página explique a exclusão.
PUBLIC_RANKINGS_NOTE = (
    "Rankings públicos (topEntities, weeklyDeltas, verticalsFull.citedEntities, "
    "crossVerticalEntities) excluem os decoys fictícios de calibração listados em "
    "calibration.fictitiousEntities. Eles aparecem em citation_context porque o "
    "probe adversarial injeta o nome na pergunta; não são citação orgânica."
)


def _norm(name: str) -> str:
    return " ".join(str(name).split()).casefold()


def is_fictitious(name: str, fictitious: Iterable[str]) -> bool:
    """Compara sem distinguir caixa nem espaçamento (ex.: 'VareJo Express')."""
    n = _norm(name)
    return any(n == _norm(f) for f in fictitious)


def filter_entities(rows: list[dict], fictitious: Iterable[str], key: str) -> list[dict]:
    return [r for r in rows if not is_fictitious(r.get(key, ""), fictitious)]


def roster_coverage(roster: list[str], cited_names: Iterable[str]) -> tuple[int, float]:
    """Quantas marcas do roster têm ao menos uma citação detectada.

    Casamento por substring nos dois sentidos, o mesmo critério de
    `uncitedByVertical` ('Banco Inter' vs 'Inter'). Resultado nunca passa de
    100% porque o numerador é um subconjunto do roster.
    """
    cited = [_norm(c) for c in cited_names]
    matched = 0
    for brand in roster:
        b = _norm(brand)
        if any(b in c or c in b for c in cited):
            matched += 1
    return matched, round(matched / max(len(roster), 1) * 100, 1)


def sanitize_public_rankings(data: dict, fictitious: Iterable[str] | None = None) -> dict:
    """Remove fictícias dos rankings públicos e recalcula coverage. Idempotente.

    Mantém `calibration.fictitiousEntities` intacto: o bloco de calibração é o
    lugar certo para elas. Devolve o mesmo dict, alterado in-place.
    """
    fict = list(fictitious if fictitious is not None
                else data.get("calibration", {}).get("fictitiousEntities", []))
    if not fict:
        return data

    if "topEntities" in data:
        data["topEntities"] = filter_entities(data["topEntities"], fict, "name")

    if "crossVerticalEntities" in data:
        data["crossVerticalEntities"] = filter_entities(
            data["crossVerticalEntities"], fict, "entity")

    for vslug, block in (data.get("weeklyDeltas") or {}).items():
        for group in ("risers", "fallers", "newEntrants"):
            if group in block:
                block[group] = filter_entities(block[group], fict, "entity")

    for vslug, vf in (data.get("verticalsFull") or {}).items():
        cited = filter_entities(vf.get("citedEntities", []), fict, "entity")
        vf["citedEntities"] = cited
        vf["citedCount"] = len(cited)
        roster = vf.get("roster", [])
        matched, cov = roster_coverage(roster, (c["entity"] for c in cited))
        vf["rosterCited"] = matched
        vf["coverage"] = cov
        vf["coverageDefinition"] = (
            "rosterCited / rosterCount: marcas do roster com ao menos uma citação "
            "detectada, casamento por substring; teto 100%."
        )

    data["publicRankingsNote"] = PUBLIC_RANKINGS_NOTE
    return data


def compute_window_fields(
    window_start: date,
    last_collection: date | None,
    collected_days: int,
    total_days: int = WINDOW_TOTAL_DAYS,
) -> dict:
    """Campos de janela coerentes com a semântica "90 dias coletados".

    - `windowEnd`: fim PROJETADO — última coleta + dias que faltam coletar.
      Se a janela já fechou (collected_days >= total), é a data da última
      coleta. É o número que o health-check de 08/09 chamou de "fechamento
      projetado" (15/10/2026 com 54 de 90 em 09/09).
    - `windowEndCalendar`: o antigo valor (start + 89 dias), preservado para
      quem comparar versões do arquivo.
    - `windowEndSemantics`: frase que explica a diferença, porque um número
      sem denominador foi o que produziu "dia 90 de 90" em 10/08.
    """
    calendar_end = window_start + timedelta(days=total_days - 1)
    remaining = max(total_days - collected_days, 0)
    if last_collection is None:
        projected = calendar_end
    else:
        projected = last_collection + timedelta(days=remaining)
    return {
        "windowStart": window_start.isoformat(),
        "windowEnd": projected.isoformat(),
        "windowEndProjected": projected.isoformat(),
        "windowEndCalendar": calendar_end.isoformat(),
        "windowTotalDays": total_days,
        "windowRemainingDays": remaining,
        "windowEndSemantics": (
            f"Janela de {total_days} dias COLETADOS (collectedDays), não de calendário. "
            "windowEnd é o fechamento projetado: última coleta mais os dias que faltam, "
            "assumindo uma coleta persistida por dia. windowEndCalendar é o 90º dia "
            "corrido desde windowStart e só serve de referência histórica."
        ),
    }


def parse_last_collection(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00")).date()
    except ValueError:
        return date.fromisoformat(str(value)[:10])


def load_partial_days(path: Path) -> list[dict]:
    """Lê data/partial_days.json (lista de {date, missingLLMs, reason, source}).

    Arquivo escrito pelo preflight em modo degradado e, para os dias anteriores
    ao mecanismo, semeado à mão a partir do health-check. Ordena por data e
    funde entradas do mesmo dia (união de missingLLMs).
    """
    if not path.exists():
        return []
    raw = json.loads(path.read_text(encoding="utf-8") or "[]")
    merged: dict[str, dict] = {}
    for e in raw:
        d = str(e.get("date", ""))[:10]
        if not d:
            continue
        cur = merged.setdefault(d, {"date": d, "missingLLMs": [], "reason": "", "source": ""})
        for llm in e.get("missingLLMs", []):
            if llm not in cur["missingLLMs"]:
                cur["missingLLMs"].append(llm)
        for k in ("reason", "source"):
            if e.get(k) and e[k] not in cur[k]:
                cur[k] = (cur[k] + "; " + e[k]).strip("; ")
    return [merged[k] for k in sorted(merged)]


def apply_partial_days(data: dict, partial: list[dict]) -> dict:
    """Anexa `partialDays` e marca `partial: true` nos pontos de dailySeries."""
    by_date = {p["date"]: p for p in partial}
    data["partialDays"] = partial
    for point in data.get("dailySeries", []):
        if point.get("date") in by_date:
            point["partial"] = True
            point["missingLLMs"] = by_date[point["date"]]["missingLLMs"]
    data["partialDaysNote"] = (
        "Dia parcial: coleta persistida com menos braços que MANDATORY_LLMS (provedor "
        "sem crédito ou quota no preflight). Entra em collectedDays, mas a comparação "
        "entre motores deve excluí-lo ou tratá-lo como incompleto."
    )
    return data


def postprocess(data: dict, partial_days_path: Path | None = None) -> dict:
    """Pipeline completo sobre um dashboard já montado (gerador ou --from-json)."""
    sanitize_public_rankings(data)
    start = date.fromisoformat(data["windowStart"])
    data.update(compute_window_fields(
        start,
        parse_last_collection(data.get("lastCollection")),
        int(data.get("collectedDays", 0)),
        int(data.get("windowTotalDays", WINDOW_TOTAL_DAYS)),
    ))
    if partial_days_path is not None:
        apply_partial_days(data, load_partial_days(partial_days_path))
    return data
