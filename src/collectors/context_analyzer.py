"""Module 7: Citation Context Analyzer.

Analyzes HOW entities are cited, not just IF. Extracts: sentiment, attribution type,
factual accuracy, position in response, confidence/hedging language.
"""

from __future__ import annotations

import re
from typing import Any


class CitationContextAnalyzer:
    """Analyze the qualitative context of citations in LLM responses."""

    # Sentiment indicators
    POSITIVE_SIGNALS = [
        r"leading", r"pioneer", r"innovative", r"expert", r"renowned",
        r"líder", r"pioneiro", r"inovador", r"especialista", r"referência",
        r"recommended", r"recomendado", r"best", r"melhor", r"top",
        r"comprehensive", r"abrangente", r"authoritative", r"autoritativo",
    ]

    NEGATIVE_SIGNALS = [
        r"controversial", r"questionable", r"unproven", r"limited",
        r"controverso", r"questionável", r"não comprovado", r"limitado",
        r"criticized", r"criticado", r"lacks", r"carece",
    ]

    HEDGING_PATTERNS = [
        r"according to", r"segundo", r"reportedly", r"supostamente",
        r"it is claimed", r"some suggest", r"may be", r"might be",
        r"possibly", r"possivelmente", r"aparentemente", r"apparently",
        r"it appears", r"parece que", r"is said to", r"dizem que",
        r"claims to", r"afirma ser", r"self-described", r"autodenominado",
    ]

    # Known facts for accuracy checking (key fintechs in the study cohort)
    CANONICAL_FACTS = {
        "nubank": {
            "founded": "2013",
            "ceo": "David Vélez",
            "headquarters": "São Paulo",
            "type": "digital bank",
        },
        "pagbank": {
            "parent_company": "PagSeguro",
            "founded": "2006",
            "type": "digital bank and payments",
        },
        "banco inter": {
            "founded": "1994",
            "headquarters": "Belo Horizonte",
            "type": "digital bank",
        },
        "stone": {
            "founded": "2012",
            "headquarters": "Rio de Janeiro",
            "type": "payments and fintech",
        },
        "c6 bank": {
            "founded": "2018",
            "headquarters": "São Paulo",
            "type": "digital bank",
        },
    }

    def analyze(self, entity: str, response_text: str) -> dict[str, Any]:
        """Perform full context analysis of how an entity is cited.

        Args:
            entity: The entity name to analyze (e.g., "Nubank").
            response_text: Full LLM response text.

        Returns:
            Dictionary with sentiment, attribution, accuracy, position, hedging.
        """
        text_lower = response_text.lower()
        entity_lower = entity.lower()

        if entity_lower not in text_lower:
            return {
                "entity": entity,
                "cited": False,
                "sentiment": None,
                "attribution": "none",
                "factual_accuracy": None,
                "position_tercile": None,
                "hedging": False,
                "hedging_phrases": [],
                "context_window": None,
                "sentiment_signals": [],
            }

        # Extract context window (200 chars around first mention)
        idx = text_lower.find(entity_lower)
        start = max(0, idx - 100)
        end = min(len(response_text), idx + len(entity) + 100)
        context_window = response_text[start:end]

        return {
            "entity": entity,
            "cited": True,
            "sentiment": self._detect_sentiment(context_window),
            "attribution": self._detect_attribution(entity, response_text),
            "factual_accuracy": self._check_accuracy(entity, response_text),
            "position_tercile": self._compute_position(entity_lower, text_lower),
            "hedging": self._detect_hedging(context_window),
            "hedging_phrases": self._extract_hedging_phrases(context_window),
            "context_window": context_window,
            "sentiment_signals": self._extract_sentiment_signals(context_window),
        }

    def _detect_sentiment(self, context: str) -> str:
        """Detect sentiment around the entity mention."""
        ctx_lower = context.lower()
        pos = sum(1 for p in self.POSITIVE_SIGNALS if re.search(p, ctx_lower))
        neg = sum(1 for p in self.NEGATIVE_SIGNALS if re.search(p, ctx_lower))

        if pos > neg:
            return "positive"
        elif neg > pos:
            return "negative"
        return "neutral"

    def _detect_attribution(self, entity: str, text: str) -> str:
        """Detect how the entity is attributed: linked, named, paraphrased."""
        entity_lower = entity.lower()
        text_lower = text.lower()

        # Check for URLs (entity domains)
        domain_patterns = [
            r"nubank\.com\.br", r"pagbank\.com\.br", r"bancointer\.com\.br",
            r"stone\.com\.br", r"c6bank\.com\.br", r"picpay\.com",
        ]
        for pattern in domain_patterns:
            if re.search(pattern, text_lower):
                return "linked"

        # Check for explicit naming
        if entity_lower in text_lower:
            return "named"

        return "paraphrased"

    def _check_accuracy(self, entity: str, text: str) -> dict[str, Any]:
        """Check factual accuracy against canonical facts."""
        entity_lower = entity.lower()
        facts = self.CANONICAL_FACTS.get(entity_lower, {})
        if not facts:
            return {"checkable": False, "errors": []}

        text_lower = text.lower()
        errors: list[str] = []
        verified: list[str] = []

        for key, value in facts.items():
            if value.lower() in text_lower:
                verified.append(key)

        # Check for common hallucinations about fintechs
        hallucination_checks = {
            "wrong_founding_date": [
                r"nubank.*(?:2010|2011|2012|2014|2015)",
                r"stone.*(?:2000|2005|2015)",
            ],
            "wrong_ceo": [
                r"nubank.*CEO.*(?!David\s*V[eé]lez)",
            ],
            "wrong_headquarters": [
                r"nubank.*(?:Rio de Janeiro|Brasília|Belo Horizonte)",
            ],
        }
        for error_type, patterns in hallucination_checks.items():
            for p in patterns:
                if re.search(p, text_lower):
                    errors.append(error_type)

        return {
            "checkable": True,
            "verified_facts": verified,
            "errors": errors,
            "accuracy_score": len(verified) / max(len(facts), 1),
        }

    @staticmethod
    def _compute_position(entity_lower: str, text_lower: str) -> int | None:
        """Compute position tercile (1=first third, 2=middle, 3=last)."""
        idx = text_lower.find(entity_lower)
        if idx < 0:
            return None
        relative = idx / max(len(text_lower), 1)
        if relative < 0.33:
            return 1
        elif relative < 0.66:
            return 2
        return 3

    def _detect_hedging(self, context: str) -> bool:
        """Check if hedging language is used near the entity."""
        ctx_lower = context.lower()
        return any(re.search(p, ctx_lower) for p in self.HEDGING_PATTERNS)

    def _extract_hedging_phrases(self, context: str) -> list[str]:
        """Extract specific hedging phrases found."""
        ctx_lower = context.lower()
        found = []
        for p in self.HEDGING_PATTERNS:
            match = re.search(p, ctx_lower)
            if match:
                found.append(match.group())
        return found

    def _extract_sentiment_signals(self, context: str) -> list[str]:
        """Extract all sentiment signals found in context."""
        ctx_lower = context.lower()
        signals = []
        for p in self.POSITIVE_SIGNALS:
            if re.search(p, ctx_lower):
                signals.append(f"+{p}")
        for p in self.NEGATIVE_SIGNALS:
            if re.search(p, ctx_lower):
                signals.append(f"-{p}")
        return signals
