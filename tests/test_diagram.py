"""Tests for diagram verification workflow."""


from biopress.generators.content.diagram import (
    Diagram,
    DiagramStatus,
    DiagramVerifier,
)
from biopress.generators.content.diagram_source import (
    DiagramSource,
    OpenStaxSource,
    ServierSource,
    WikimediaSource,
    get_default_sources,
)


class MockDiagramSource(DiagramSource):
    """Mock source for testing."""

    def __init__(self, results: list[Diagram] | None = None):
        super().__init__("Mock")
        self._results = results or []

    def search(self, topic: str, subject: str) -> list[Diagram]:
        return self._results


class TestDiagram:
    """Tests for Diagram model."""

    def test_diagram_creation(self):
        """Test basic diagram creation."""
        diagram = Diagram(
            topic="Mitochondria",
            subject="Biology",
            source="Servier",
            url="https://example.com/mitochondria.svg",
        )
        assert diagram.topic == "Mitochondria"
        assert diagram.subject == "Biology"
        assert diagram.status == DiagramStatus.PENDING
        assert diagram.id is not None

    def test_diagram_id_unique(self):
        """Test each diagram gets unique ID."""
        d1 = Diagram()
        d2 = Diagram()
        assert d1.id != d2.id


class TestDiagramVerifier:
    """Tests for DiagramVerifier workflow."""

    def test_add_diagram(self):
        """Test adding diagram to queue."""
        verifier = DiagramVerifier()
        diagram = Diagram(topic="Mitochondria", subject="Biology")
        verifier.add_diagram(diagram)
        assert len(verifier.diagrams) == 1

    def test_preview_all(self):
        """Stage 2: Preview all diagrams."""
        verifier = DiagramVerifier()
        d1 = Diagram(topic="Mitochondria", subject="Biology")
        d2 = Diagram(topic="Nucleus", subject="Biology")
        verifier.add_diagram(d1)
        verifier.add_diagram(d2)
        preview = verifier.preview_all()
        assert len(preview) == 2

    def test_approve_diagram(self):
        """Stage 3: Approve a diagram."""
        verifier = DiagramVerifier()
        diagram = Diagram(topic="Mitochondria", subject="Biology")
        verifier.add_diagram(diagram)
        verifier.approve(diagram.id)
        assert diagram.status == DiagramStatus.APPROVED
        assert diagram in verifier.approved

    def test_reject_diagram(self):
        """Stage 3: Reject a diagram."""
        verifier = DiagramVerifier()
        diagram = Diagram(topic="Mitochondria", subject="Biology")
        verifier.add_diagram(diagram)
        verifier.reject(diagram.id, "Low quality")
        assert diagram.status == DiagramStatus.REJECTED
        assert diagram.rejection_reason == "Low quality"
        assert diagram in verifier.rejected

    def test_refine_rejected(self):
        """Stage 4: Re-process rejected diagrams."""
        verifier = DiagramVerifier()
        mock_source = MockDiagramSource([
            Diagram(topic="Mitochondria", subject="Biology", source="NewSource"),
        ])
        verifier.add_source(mock_source)
        
        diagram = Diagram(topic="Mitochondria", subject="Biology", source="Old")
        verifier.add_diagram(diagram)
        verifier.reject(diagram.id, "Low quality")
        
        refined = verifier.refine_rejected()
        assert len(refined) == 1
        assert refined[0].source == "NewSource"
        assert len(verifier.rejected) == 0

    def test_is_ready_for_pdf_all_approved(self):
        """Stage 5: Ready when all approved."""
        verifier = DiagramVerifier()
        d1 = Diagram(topic="Mitochondria", subject="Biology")
        d2 = Diagram(topic="Nucleus", subject="Biology")
        verifier.add_diagram(d1)
        verifier.add_diagram(d2)
        verifier.approve(d1.id)
        verifier.approve(d2.id)
        assert verifier.is_ready_for_pdf() is True

    def test_is_ready_for_pdf_not_all_approved(self):
        """Stage 5: Not ready if any pending/rejected."""
        verifier = DiagramVerifier()
        d1 = Diagram(topic="Mitochondria", subject="Biology")
        d2 = Diagram(topic="Nucleus", subject="Biology")
        verifier.add_diagram(d1)
        verifier.add_diagram(d2)
        verifier.approve(d1.id)
        assert verifier.is_ready_for_pdf() is False

    def test_is_ready_for_pdf_empty(self):
        """Stage 5: Ready when no diagrams."""
        verifier = DiagramVerifier()
        assert verifier.is_ready_for_pdf() is True

    def test_get_status_summary(self):
        """Test status summary."""
        verifier = DiagramVerifier()
        d1 = Diagram(topic="Mitochondria", subject="Biology")
        d2 = Diagram(topic="Nucleus", subject="Biology")
        verifier.add_diagram(d1)
        verifier.add_diagram(d2)
        verifier.approve(d1.id)
        summary = verifier.get_status_summary()
        assert summary["approved"] == 1
        assert summary["pending"] == 1


class TestDiagramSources:
    """Tests for diagram source implementations."""

    def test_openstax_source(self):
        """Test OpenStax source search."""
        source = OpenStaxSource()
        results = source.search("Mitochondria", "Biology")
        assert len(results) == 1
        assert results[0].source == "OpenStax"
        assert results[0].topic == "Mitochondria"

    def test_servier_source_biology(self):
        """Test Servier source for biology."""
        source = ServierSource()
        results = source.search("Cell", "Biology")
        assert len(results) == 1
        assert results[0].source == "Servier"

    def test_servier_source_physics_excluded(self):
        """Test Servier excludes physics topics."""
        source = ServierSource()
        results = source.search("Force", "Physics")
        assert len(results) == 0

    def test_wikimedia_source(self):
        """Test Wikimedia source."""
        source = WikimediaSource()
        results = source.search("DNA", "Biology")
        assert len(results) == 1
        assert results[0].source == "Wikimedia"

    def test_get_default_sources(self):
        """Test default sources include all expected sources."""
        sources = get_default_sources()
        source_names = [s.name for s in sources]
        assert "OpenStax" in source_names
        assert "LibreTexts" in source_names
        assert "HyperPhysics" in source_names
        assert "Servier" in source_names
        assert "Bioicons" in source_names
        assert "Wikimedia" in source_names
        assert len(sources) == 6
