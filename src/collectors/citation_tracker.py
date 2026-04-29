"""Module 1: Multi-LLM Citation Tracker (cost-optimized).

Cost comparison (30 queries x 4 LLMs = 120 calls/day):
- OLD: ~$0.80/day — gpt-4o, sonnet, unlimited tokens, free-text
- NEW: ~$0.03/day — mini, haiku, flash(free), JSON mode, 250 max_tokens, cache

Optimizations:
- JSON structured output: LLM returns {cited:[], sources:[], summary:""}
- Entity detection from JSON `cited` array (no regex needed)
- max_tokens=250 prevents verbose responses
- Cache skips identical queries within 20h window
"""

from __future__ import annotations

import hashlib
import json
import re
from typing import Any

from src.collectors.base import BaseCollector, LLMResponse
from src.config import AMBIGUOUS_ENTITIES, CANONICAL_NAMES, is_fictional, query_type_for


class CitationTracker(BaseCollector):
    """Track citations of entities across multiple LLMs."""

    def module_name(self) -> str:
        return "citation_tracker"

    def collect(self) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        cache_hits = 0
        # Onda 8: structured_logger emite 1 evento por query + summary.
        # Lazy — se o módulo de logging falhar em CI sem disco, silently
        # passa adiante.
        slog = self.structured_logger

        for q in self.queries:
            for llm_cfg in self.config.llms:
                # Distingue "routed_out" (deliberadamente pulado por
                # PERPLEXITY_CATEGORIES filter) de "failed" (erro real de API,
                # circuit-break, timeout). Gap B5 Agent B audit 2026-04-23:
                # logar ambos como "skipped_or_failed" gerava falsos-alarmes
                # de fail-loud porque Perplexity recebe apenas 4/N categorias
                # por design — mas em logs era indistinguível de falha real.
                should_process = self.llm_client.should_query(
                    llm_cfg, q.get("category", "")
                )
                if not should_process:
                    if slog is not None:
                        slog.log_query(
                            llm=llm_cfg.name,
                            query=q["query"],
                            category=q.get("category", ""),
                            error="routed_out",  # não é failure — design decision
                        )
                    continue
                response = self.llm_client.query(llm_cfg, q["query"], category=q.get("category", ""))
                if response is None:
                    if slog is not None:
                        slog.log_query(
                            llm=llm_cfg.name,
                            query=q["query"],
                            category=q.get("category", ""),
                            error="api_failure",  # falha real — API, timeout, circuit
                        )
                    continue
                if response.from_cache:
                    cache_hits += 1

                analysis = self._analyze(response, query_entry=q)
                # token_count = input + output (fix 2026-04-23: campo estava
                # 100% NULL em 6.568 rows porque o record só expunha
                # input_tokens/output_tokens separados, mas client.py lê
                # r.get("token_count") na insert, que caía em None).
                total_tokens = (response.input_tokens or 0) + (response.output_tokens or 0)
                record = {
                    "module": self.module_name(),
                    "llm": llm_cfg.name,
                    "model": response.model,
                    "query": q["query"],
                    "query_category": q["category"],
                    "query_lang": q["lang"],
                    "query_type": query_type_for(q),
                    "timestamp": response.timestamp,
                    "latency_ms": response.latency_ms,
                    "token_count": total_tokens or None,
                    "input_tokens": response.input_tokens,
                    "output_tokens": response.output_tokens,
                    "from_cache": response.from_cache,
                    **analysis,
                }
                results.append(record)

                if slog is not None:
                    slog.log_query(
                        llm=llm_cfg.name,
                        query=q["query"],
                        category=q.get("category", ""),
                        duration_ms=response.latency_ms or 0,
                        tokens=(response.input_tokens + response.output_tokens),
                        cost=response.cost_usd or 0.0,
                        cited=bool(record.get("cited")),
                    )

        self.logger.info(
            f"Coletados {len(results)} registros "
            f"({cache_hits} do cache, {len(results)-cache_hits} da API)"
        )
        if slog is not None:
            summary = slog.get_summary()
            self.logger.info(
                f"[structured] run={summary['run_id']} queries={summary['total_queries']} "
                f"cited={summary['total_cited']} rate={summary['citation_rate']} "
                f"cost=${summary['total_cost_usd']} errors={summary['errors']}"
            )
        return results

    def _analyze(self, response: LLMResponse, query_entry: dict[str, Any] | None = None) -> dict[str, Any]:
        """Analyze citation data from structured response for cohort entities.

        Onda 7 (2026-04-23): quando methodology_version=v2, usa EntityExtractor
        (NER v2 com NFKD+aliases+stops) e popula colunas v2 (is_probe, probe_type,
        response_hash, cited_entities_v2_json, position_v2, ...).

        Args:
            response: LLMResponse from provider.
            query_entry: the query dict (used to flag fictional-entity probes).
        """
        text = response.response_text or ""
        extractor = self.entity_extractor  # None em v1
        use_v2 = extractor is not None

        # -- Entity extraction --------------------------------------------------
        if use_v2:
            # NER v2 — NFKD dual-pass + aliases + stop-contexts
            mentions = extractor.extract(text)
            cited_entities_list = [m.entity for m in mentions]
            cohort_cited = {e: (e in cited_entities_list) for e in self.cohort}
            cited_count = len(cited_entities_list)
            cited = cited_count > 0
            first_entity = mentions[0].entity if mentions else None
            first_offset = mentions[0].start if mentions else None
            via_alias_count = sum(1 for m in mentions if getattr(m, "via_alias", False))
            via_fold_count = sum(1 for m in mentions if getattr(m, "via_fold", False))
            # Position tercile via offset real (G4 do Null-Triad)
            text_len = max(len(text), 1)
            position: int | None = None
            if first_offset is not None:
                ratio = first_offset / text_len
                position = 1 if ratio < 1/3 else (2 if ratio < 2/3 else 3)
        else:
            # V1 legacy fallback (reprodutibilidade Paper 4)
            cited_lower = [e.lower() for e in response.cited_entities]
            cohort_cited = {}
            for entity in self.cohort:
                entity_lower = entity.lower()
                in_cited_list = any(
                    entity_lower in c or c in entity_lower for c in cited_lower
                )
                if entity in AMBIGUOUS_ENTITIES:
                    canonical = CANONICAL_NAMES.get(entity, entity)
                    in_text = bool(re.search(
                        r'\b' + re.escape(canonical) + r'\b', text, re.IGNORECASE
                    ))
                else:
                    in_text = bool(re.search(
                        r'\b' + re.escape(entity) + r'\b', text, re.IGNORECASE
                    ))
                cohort_cited[entity] = in_cited_list or in_text
            cited_count = sum(1 for v in cohort_cited.values() if v)
            cited = cited_count > 0
            cited_entities_list = [e for e, v in cohort_cited.items() if v]
            first_entity = cited_entities_list[0] if cited_entities_list else None
            first_offset = None
            via_alias_count = 0
            via_fold_count = 0
            # Position via ordem em response.cited_entities (legacy)
            position = None
            if cited:
                for i, c in enumerate(cited_lower):
                    for entity in self.cohort:
                        if entity.lower() in c or c in entity.lower():
                            total = max(len(cited_lower), 1)
                            position = 1 if i < total / 3 else (2 if i < 2 * total / 3 else 3)
                            break
                    if position is not None:
                        break

        # -- Probe detection (Onda 7 G4) ----------------------------------------
        qe = query_entry or {}
        target_fictional = qe.get("target_fictional") or qe.get("fictitious_target")
        is_probe = 0
        probe_type: str | None = None
        adversarial_framing = 0
        is_calibration = 0

        if target_fictional:
            is_probe = 1
            # Preserva probe_type explícito da query (ex.: "adversarial");
            # default "decoy" para retro-compat com probes passivos.
            probe_type = qe.get("probe_type") or "decoy"
            is_calibration = 1
            adversarial_framing = int(bool(
                qe.get("adversarial") or qe.get("adversarial_framing")
            ))
        elif qe.get("is_probe"):
            is_probe = 1
            probe_type = qe.get("probe_type") or "control"

        # -- Fictitious calibration (Onda 3 preserved) --------------------------
        fictional_hit = False
        fictional_names: list[str] = []
        for name in response.cited_entities:
            if is_fictional(name):
                fictional_hit = True
                fictional_names.append(name)
        if target_fictional and target_fictional.lower() in text.lower():
            fictional_hit = True
            if target_fictional not in fictional_names:
                fictional_names.append(target_fictional)
        # Também checa decoys v2 (nunca devem ser citados em coleta limpa)
        text_lower = text.lower()
        for decoy in self._v2_decoys:
            if decoy in text_lower and decoy not in [n.lower() for n in fictional_names]:
                fictional_hit = True
                fictional_names.append(decoy)

        # -- Response hash (Onda 6b drift + Onda 7 G5) --------------------------
        response_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]

        return {
            # --- v1 compat fields (preserve API de clientes downstream) ---
            "cited": cited,
            "cited_count": cited_count,
            "cohort_cited": cohort_cited,
            "cited_entity": first_entity,
            "cited_entities_json": cited_entities_list,
            "position": position,
            "source_count": len(response.sources),
            "response_length": len(text),
            "response_text": text,
            "all_sources": response.sources,
            "all_cited_entities": response.cited_entities,
            "fictional_hit": fictional_hit,
            "fictional_names": fictional_names,
            # --- v2 fields (Onda 2/3/6/7) ---
            "extraction_version": "v2" if use_v2 else "v1",
            "extracted_at_v2": response.timestamp if use_v2 else None,
            "cited_v2": int(cited) if use_v2 else None,
            "cited_count_v2": cited_count if use_v2 else None,
            "cited_entities_v2_json": (
                json.dumps(cited_entities_list, ensure_ascii=False) if use_v2 else None
            ),
            "first_entity_v2": first_entity if use_v2 else None,
            "first_entity_offset_v2": first_offset,
            "position_v2": position if use_v2 else None,
            "via_alias_count_v2": via_alias_count,
            "via_fold_count_v2": via_fold_count,
            "response_length_chars_v2": len(text) if use_v2 else None,
            # Probe design (migrate_0007)
            "is_probe": is_probe,
            "probe_type": probe_type,
            "adversarial_framing": adversarial_framing,
            "fictitious_target": target_fictional,
            "is_calibration": is_calibration,
            # Drift (migrate_0006)
            "response_hash": response_hash,
        }
