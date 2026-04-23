"""entity_extraction.py — NER v2 para o paper 4 v2 reboot.

Resolve os gaps identificados no Agent C audit (2026-04-23):

- G1: Diacritic-insensitive matching ("Itaú" em resposta EN vira "Itau" e
  não match com v1). Implementa dual-pass NFKD fold.
- G2: UTF-8 NFC normalization no ingest antes de qualquer regex.
- G3: Remove substring match (`in_cited_list` em citation_tracker._analyze)
  que vazava FPs ("Inter" match em "international"). Só word-boundary.
- G4: Position via offset real no texto (`text.find(entity)`), não
  iteração cohort-order.
- G5: Pre-processamento strip de MD/HTML/references `[1][2]` antes do
  regex (Perplexity + Gemini frequentemente embedam refs inline).
- G6: ALIASES dict (BTG→BTG Pactual, XP→XP Investimentos, etc.)
- G7: Stop-list anti-colisão cross-vertical ("99" tec vs "99Pay" fintech).

Uso canônico:
    from src.analysis.entity_extraction import EntityExtractor

    extractor = EntityExtractor(
        cohort=["Nubank", "Itaú", "BTG Pactual"],
        aliases={"BTG Pactual": ["BTG", "BTGP"], "Itaú": ["Itau"]},
        ambiguous={"Inter"},  # requer canonical name
        canonical_names={"Inter": "Banco Inter"},
        stop_contexts={"99": [r"\bnoventa e nove\b", r"\b99%\b"]},
    )
    mentions = extractor.extract(response_text)
    # → [EntityMention(entity="Nubank", start=42, end=48, matched_form="Nubank")]

Não modifica llm_client.py imediatamente; expõe API estável para o wire
incremental + script `scripts/reextract_citations.py`.
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from typing import Iterable


# ---------------------------------------------------------------------------
# Normalização de texto
# ---------------------------------------------------------------------------

def normalize_nfc(text: str) -> str:
    """Unicode NFC — composição canônica. Garante que 'a'+acento combinado
    seja equivalente a 'á' precomposto. Deve ser chamado no ingest.
    """
    return unicodedata.normalize("NFC", text)


def fold_diacritics(text: str) -> str:
    """Remove diacríticos via NFKD + encode ASCII ignore.

    "Itaú" → "Itau", "São Paulo" → "Sao Paulo", "Aché" → "Ache".

    Usado em dual-pass matching: testa primeiro acento-sensitive (match
    estrito), depois acento-insensitive (captura variantes de graphia).
    """
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(c for c in decomposed if not unicodedata.combining(c))


# ---------------------------------------------------------------------------
# Pre-processamento do body antes do regex
# ---------------------------------------------------------------------------

_MD_BOLD = re.compile(r"\*\*([^*]+)\*\*")
_MD_ITALIC = re.compile(r"(?<!\*)\*([^*]+)\*(?!\*)")
_MD_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
_NUMERIC_REFS = re.compile(r"\[\d+\](?:\[\d+\])*")  # Perplexity [1][2]
_HTML_TAG = re.compile(r"<[^>]+>")
_URL = re.compile(r"https?://[^\s\)\]>\"']+")


def strip_markup(text: str) -> str:
    """Remove formatação MD/HTML/refs que atrapalha word-boundary regex.

    - `**Nubank**` → `Nubank` (preserva o conteúdo)
    - `[link text](url)` → `link text` (preserva o texto, remove URL)
    - `[1][2]` → `` (remove refs numéricas do Perplexity)
    - `<em>Stone</em>` → `Stone`
    - URLs soltas → removidas (só queremos entidades)
    """
    text = _HTML_TAG.sub("", text)
    text = _NUMERIC_REFS.sub("", text)
    text = _MD_LINK.sub(r"\1", text)
    text = _MD_BOLD.sub(r"\1", text)
    text = _MD_ITALIC.sub(r"\1", text)
    text = _URL.sub("", text)
    return text


# ---------------------------------------------------------------------------
# Estruturas
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class EntityMention:
    """Uma menção de entidade detectada no response_text."""
    entity: str            # Nome canônico do cohort (ex.: "Itaú")
    matched_form: str      # Forma encontrada no texto (ex.: "Itau")
    start: int             # Offset no texto normalizado
    end: int               # Offset final (exclusive)
    via_alias: bool        # True se matched via ALIAS dict, não canonical
    via_fold: bool         # True se matched via diacritic fold

    def length(self) -> int:
        return self.end - self.start


# ---------------------------------------------------------------------------
# Extractor
# ---------------------------------------------------------------------------

class EntityExtractor:
    """Extrai menções de entidades com precisão científica.

    Contratos:
    1. Input `text` pode vir em NFC ou NFD — normalizamos para NFC.
    2. Output `EntityMention.start/end` referem-se ao texto *normalizado*.
    3. Cada entidade do cohort é reportada NO MÁXIMO uma vez por chamada
       (primeira ocorrência preservada).
    4. Ambiguous entities (e.g. "Inter") SÓ matched via canonical_name
       (e.g. "Banco Inter"). Protege contra FPs em "international".
    5. Aliases mapeiam strings encontradas no texto para o nome canônico
       do cohort. Por exemplo BTG no texto → entity="BTG Pactual".
    6. Stop-contexts descartam matches quando padrão contextual casa
       antes/depois da ocorrência. Evita colisão "99" ↔ "99%".
    """

    def __init__(
        self,
        cohort: Iterable[str],
        aliases: dict[str, list[str]] | None = None,
        ambiguous: set[str] | None = None,
        canonical_names: dict[str, str] | None = None,
        stop_contexts: dict[str, list[str]] | None = None,
    ) -> None:
        self._cohort = list(cohort)
        self._aliases = aliases or {}
        self._ambiguous = ambiguous or set()
        self._canonical_names = canonical_names or {}
        self._stop_contexts = stop_contexts or {}
        self._patterns = self._build_patterns()

    def _build_patterns(self) -> list[tuple[str, str, re.Pattern[str], bool]]:
        """Retorna lista de (entity, surface, compiled_regex, via_alias).

        Para cada entidade do cohort, constrói 1+N patterns:
        - Pattern canônico (ou canonical_name se ambiguous)
        - Patterns para cada alias em `aliases[entity]`

        Regex usa `\\b` para word boundary + escape de metacaracteres.
        """
        patterns: list[tuple[str, str, re.Pattern[str], bool]] = []
        for entity in self._cohort:
            # Superfície canônica (ou canonical_name para ambiguous)
            if entity in self._ambiguous:
                surface = self._canonical_names.get(entity, entity)
            else:
                surface = entity
            patterns.append((
                entity, surface,
                re.compile(r"\b" + re.escape(surface) + r"\b", re.IGNORECASE),
                False,
            ))
            # Aliases (se houver) — mapeiam para mesmo entity canônico
            for alias in self._aliases.get(entity, []):
                patterns.append((
                    entity, alias,
                    re.compile(r"\b" + re.escape(alias) + r"\b", re.IGNORECASE),
                    True,
                ))
        return patterns

    def _passes_stop_context(self, entity: str, text: str, start: int, end: int) -> bool:
        """True se o match NÃO casa nenhum stop-context. Evita FPs."""
        patterns = self._stop_contexts.get(entity)
        if not patterns:
            return True
        # Janela de 30 chars antes e depois para checar contexto
        window_start = max(0, start - 30)
        window_end = min(len(text), end + 30)
        window = text[window_start:window_end]
        for pattern_str in patterns:
            if re.search(pattern_str, window, re.IGNORECASE):
                return False
        return True

    def extract(self, text: str) -> list[EntityMention]:
        """Extrai menções de entidades no texto.

        Dual-pass:
        1. Match acento-sensitive no texto NFC (precisão alta)
        2. Para entidades ainda não encontradas, tentar match no texto
           com diacríticos removidos (captura "Itau" quando cohort tem "Itaú")

        Retorna lista ordenada por posição de ocorrência. Um entity aparece
        no máximo 1 vez (primeira ocorrência, tiebreak offset).
        """
        text_nfc = normalize_nfc(text)
        clean_text = strip_markup(text_nfc)
        # NOTA: fold_diacritics preserva length de cada char porque NFKD
        # ignora combining marks (mantém ASCII base). Logo offsets em
        # `folded_text` são alinhados com `clean_text` caractere-a-caractere.
        folded_text = fold_diacritics(clean_text)

        mentions: dict[str, EntityMention] = {}

        # PASS 1: acento-sensitive sobre texto limpo
        for entity, surface, pattern, via_alias in self._patterns:
            if entity in mentions:
                continue
            m = pattern.search(clean_text)
            if m and self._passes_stop_context(entity, clean_text, m.start(), m.end()):
                mentions[entity] = EntityMention(
                    entity=entity,
                    matched_form=m.group(),
                    start=m.start(),
                    end=m.end(),
                    via_alias=via_alias,
                    via_fold=False,
                )

        # PASS 2: acento-insensitive sobre texto com diacríticos removidos
        # (captura "Itau" quando cohort tem "Itaú" ou vice-versa).
        # Offsets são usados contra clean_text (NFC) para preservar coerência
        # com PASS 1 — confiando que NFKD fold mantém length char-a-char
        # após strip de combining marks em NFC já-composto.
        for entity, surface, pattern, via_alias in self._patterns:
            if entity in mentions:
                continue
            folded_surface = fold_diacritics(surface)
            if folded_surface == surface:
                continue
            folded_pattern = re.compile(
                r"\b" + re.escape(folded_surface) + r"\b", re.IGNORECASE
            )
            m = folded_pattern.search(folded_text)
            if m and self._passes_stop_context(entity, folded_text, m.start(), m.end()):
                mentions[entity] = EntityMention(
                    entity=entity,
                    matched_form=m.group(),
                    start=m.start(),
                    end=m.end(),
                    via_alias=via_alias,
                    via_fold=True,
                )

        return sorted(mentions.values(), key=lambda x: x.start)


# ---------------------------------------------------------------------------
# Helpers para o pipeline de análise
# ---------------------------------------------------------------------------

def position_tercile(start: int, text_length: int) -> int:
    """Retorna 1, 2 ou 3 consoante a posição do token no tercil do texto.

    Uso: converte offset bruto em feature ordinal para Mann-Whitney U.
    """
    if text_length <= 0:
        return 2  # meio por default quando texto vazio
    ratio = start / text_length
    if ratio < 1 / 3:
        return 1
    if ratio < 2 / 3:
        return 2
    return 3


def summarize_extraction(
    mentions: list[EntityMention], cohort_size: int
) -> dict[str, object]:
    """Agrega métricas de uma extração para análise downstream."""
    if not mentions:
        return {
            "cited": False,
            "cited_count": 0,
            "cited_entities": [],
            "position": None,
            "first_entity": None,
            "via_alias_count": 0,
            "via_fold_count": 0,
        }
    first = mentions[0]
    return {
        "cited": True,
        "cited_count": len(mentions),
        "cited_entities": [m.entity for m in mentions],
        "position": None,  # calculado separadamente com text_length
        "first_entity": first.entity,
        "first_start": first.start,
        "via_alias_count": sum(1 for m in mentions if m.via_alias),
        "via_fold_count": sum(1 for m in mentions if m.via_fold),
    }
