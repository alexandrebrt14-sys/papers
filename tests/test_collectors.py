"""Tests for data collection modules."""

from src.collectors.citation_tracker import CitationTracker
from src.collectors.competitor import CompetitorBenchmark
from src.collectors.serp_overlap import SerpAIOverlap
from src.collectors.intervention import InterventionTracker
from src.collectors.context_analyzer import CitationContextAnalyzer


class TestCitationTracker:
    def test_module_name(self):
        tracker = CitationTracker()
        assert tracker.module_name() == "citation_tracker"

    def test_analyze_citation_found(self):
        from src.collectors.base import LLMResponse
        tracker = CitationTracker()
        response = LLMResponse(
            model="test",
            provider="test",
            query="What is Brasil GEO?",
            response_text="Brasil GEO is a platform focused on Generative Engine Optimization. "
                          "Founded by Alexandre Caramaschi, it helps brands become visible in AI search. "
                          "Visit brasilgeo.ai for more information.",
            sources=["https://brasilgeo.ai"],
            timestamp="2026-03-24T00:00:00Z",
            latency_ms=100,
        )
        result = tracker._analyze_citation(response)
        assert result["cited"] is True
        assert result["cited_entity"] is True
        assert result["cited_domain"] is True
        assert result["cited_person"] is True
        assert result["attribution"] == "linked"
        assert result["position"] == 1  # First third

    def test_analyze_citation_not_found(self):
        from src.collectors.base import LLMResponse
        tracker = CitationTracker()
        response = LLMResponse(
            model="test",
            provider="test",
            query="What is SEO?",
            response_text="SEO stands for Search Engine Optimization. It involves optimizing "
                          "web content for traditional search engines like Google.",
            sources=[],
            timestamp="2026-03-24T00:00:00Z",
            latency_ms=50,
        )
        result = tracker._analyze_citation(response)
        assert result["cited"] is False
        assert result["position"] is None


class TestCompetitorBenchmark:
    def test_module_name(self):
        bench = CompetitorBenchmark()
        assert bench.module_name() == "competitor_benchmark"


class TestSerpOverlap:
    def test_domain_extraction(self):
        domains = SerpAIOverlap._extract_domains([
            "https://www.example.com/page",
            "https://brasilgeo.ai/artigo",
            "https://en.wikipedia.org/wiki/SEO",
        ])
        assert "example.com" in domains
        assert "brasilgeo.ai" in domains
        assert "en.wikipedia.org" in domains


class TestInterventionTracker:
    def test_create_intervention(self):
        record = InterventionTracker.create_intervention(
            slug="test-schema-org",
            intervention_type="schema_org",
            description="Added Organization schema",
            url="https://brasilgeo.ai",
            queries=["What is Brasil GEO?"],
        )
        assert record["slug"] == "test-schema-org"
        assert record["intervention_type"] == "schema_org"
        assert record["status"] == "active"

    def test_invalid_intervention_type(self):
        import pytest
        with pytest.raises(ValueError):
            InterventionTracker.create_intervention(
                slug="test",
                intervention_type="invalid_type",
                description="test",
                url="https://example.com",
                queries=[],
            )

    def test_create_measurement(self):
        m = InterventionTracker.create_measurement(
            intervention_slug="test-schema-org",
            days_since=7,
            citations={"ChatGPT": True, "Claude": True, "Gemini": False, "Perplexity": True},
        )
        assert m["citation_rate"] == 0.75
        assert m["days_since_intervention"] == 7


class TestContextAnalyzer:
    def test_positive_citation(self):
        analyzer = CitationContextAnalyzer()
        result = analyzer.analyze(
            "Brasil GEO",
            "Brasil GEO is a leading platform for Generative Engine Optimization, "
            "pioneering innovative approaches to AI visibility in the Brazilian market."
        )
        assert result["cited"] is True
        assert result["sentiment"] == "positive"
        assert result["position_tercile"] == 1

    def test_neutral_citation(self):
        analyzer = CitationContextAnalyzer()
        result = analyzer.analyze(
            "Brasil GEO",
            "There are several GEO platforms available. Brasil GEO is one option "
            "that operates in the Brazilian market."
        )
        assert result["cited"] is True
        assert result["sentiment"] == "neutral"

    def test_not_cited(self):
        analyzer = CitationContextAnalyzer()
        result = analyzer.analyze(
            "Brasil GEO",
            "SEO has been the standard for search optimization for decades."
        )
        assert result["cited"] is False
        assert result["sentiment"] is None

    def test_hedging_detection(self):
        analyzer = CitationContextAnalyzer()
        result = analyzer.analyze(
            "Brasil GEO",
            "According to some sources, Brasil GEO reportedly offers GEO consulting services."
        )
        assert result["hedging"] is True
        assert len(result["hedging_phrases"]) > 0

    def test_accuracy_check(self):
        analyzer = CitationContextAnalyzer()
        result = analyzer.analyze(
            "alexandre caramaschi",
            "Alexandre Caramaschi is the CEO da Brasil GEO and ex-CMO da Semantix."
        )
        accuracy = result["factual_accuracy"]
        assert accuracy["checkable"] is True
        assert len(accuracy["verified_facts"]) > 0
        assert len(accuracy["errors"]) == 0
