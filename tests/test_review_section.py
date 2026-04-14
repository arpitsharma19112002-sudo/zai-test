"""Tests for review section generator."""

from datetime import datetime

from biopress.pdf.review_section import (
    ReviewSectionGenerator,
    QualityScore,
    ReviewMetadata,
    generate_review_section,
)


class TestReviewSectionGenerator:
    """Tests for ReviewSectionGenerator."""

    def test_generate_basic_review(self):
        """Test basic review section generation."""
        result = ReviewSectionGenerator.generate()
        assert "EDITORIAL REVIEW & SOURCES" in result
        assert "Generated:" in result
        assert "Pipeline:" in result

    def test_generate_with_sources(self):
        """Test review section with sources."""
        sources = [
            "NCERT Class 11 Physics Chapter 3",
            "OpenStax: Kinematics diagrams",
        ]
        result = ReviewSectionGenerator.generate(sources=sources)
        assert "Sources:" in result
        assert "NCERT Class 11 Physics Chapter 3" in result
        assert "OpenStax: Kinematics diagrams" in result

    def test_generate_with_image_attributions(self):
        """Test review section with image attributions."""
        attributions = ["CC-BY 4.0", "Public Domain"]
        result = ReviewSectionGenerator.generate(image_attributions=attributions)
        assert "Image Attributions:" in result

    def test_generate_with_quality_scores(self):
        """Test review section with quality scores."""
        quality_scores = [
            {"level": "L1 Validation", "status": "PASS", "percentage": 100.0},
            {"level": "L2 Validation", "status": "PASS", "percentage": 85.0},
        ]
        result = ReviewSectionGenerator.generate(quality_scores=quality_scores)
        assert "Quality Scores:" in result
        assert "L1 Validation: PASS (100.0%)" in result

    def test_generate_with_all_fields(self):
        """Test review section with all fields."""
        sources = ["NCERT Class 11 Physics"]
        attributions = ["CC-BY 4.0"]
        quality_scores = [{"level": "L1", "status": "PASS", "percentage": 100.0}]
        pipeline_version = "BioPress v0.2.0"

        result = ReviewSectionGenerator.generate(
            sources=sources,
            image_attributions=attributions,
            quality_scores=quality_scores,
            pipeline_version=pipeline_version,
        )

        assert "Sources:" in result
        assert "Image Attributions:" in result
        assert "Quality Scores:" in result
        assert "BioPress v0.2.0" in result

    def test_create_metadata(self):
        """Test creating review metadata."""
        sources = ["Test Source"]
        quality_scores = [{"level": "L1", "status": "PASS", "percentage": 100.0}]

        metadata = ReviewSectionGenerator.create_metadata(
            sources=sources,
            quality_scores=quality_scores,
        )

        assert isinstance(metadata, ReviewMetadata)
        assert metadata.sources == sources
        assert len(metadata.quality_scores) == 1
        assert metadata.quality_scores[0].level == "L1"


class TestQualityScore:
    """Tests for QualityScore dataclass."""

    def test_quality_score_creation(self):
        """Test creating quality score."""
        qs = QualityScore(level="L1", status="PASS", percentage=100.0)
        assert qs.level == "L1"
        assert qs.status == "PASS"
        assert qs.percentage == 100.0


class TestReviewMetadata:
    """Tests for ReviewMetadata dataclass."""

    def test_review_metadata_creation(self):
        """Test creating review metadata."""
        qs = [QualityScore(level="L1", status="PASS", percentage=100.0)]
        metadata = ReviewMetadata(
            sources=["Test Source"],
            image_attributions=[],
            quality_scores=qs,
            generated_at=datetime.now(),
            pipeline_version="BioPress v0.1.0",
        )

        assert metadata.sources == ["Test Source"]
        assert metadata.pipeline_version == "BioPress v0.1.0"


class TestGenerateReviewSection:
    """Tests for convenience function."""

    def test_convenience_function(self):
        """Test convenience function."""
        result = generate_review_section()
        assert isinstance(result, str)
        assert "EDITORIAL REVIEW & SOURCES" in result