"""Tests for PDF styles."""

import json
import os
import tempfile
from pathlib import Path

import pytest

from biopress.core.models import MCQItem, MCQOptions, PerseusQuiz
from biopress.pdf.builder import PDFBuilder
from biopress.pdf.renderer import PDFRenderer, get_pdf_style
from biopress.pdf.styles.neet import get_neet_style, NEET_2COLUMN
from biopress.pdf.styles.ncert import get_ncert_style, NCERT
from biopress.pdf.styles.bilingual import get_bilingual_style, BILINGUAL
from biopress.pdf.styles.omr import get_omr_style, OMR_READY


@pytest.fixture
def sample_quiz():
    """Create a sample quiz for testing."""
    items = [
        MCQItem(
            question="What is the powerhouse of the cell?",
            options=MCQOptions(
                A="Nucleus",
                B="Mitochondria",
                C="Ribosome",
                D="Golgi apparatus",
            ),
            correct_answer="B",
            explanation="Mitochondria produce ATP through cellular respiration.",
        ),
        MCQItem(
            question="What is the chemical formula for water?",
            options=MCQOptions(
                A="H2O",
                B="CO2",
                C="NaCl",
                D="O2",
            ),
            correct_answer="A",
            explanation="Water is composed of two hydrogen atoms and one oxygen atom.",
        ),
    ]
    return PerseusQuiz(items=items)


@pytest.fixture
def sample_quiz_file(sample_quiz):
    """Create a temporary JSON file with quiz data."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump({"items": [item.model_dump() for item in sample_quiz.items]}, f)
        temp_path = f.name
    yield temp_path
    os.unlink(temp_path)


class TestNEETStyle:
    """Tests for NEET 2-column style."""

    def test_get_neet_style(self):
        """Test getting NEET style."""
        style = get_neet_style()
        assert style == NEET_2COLUMN
        assert style.columns == 2
        assert style.omr_bubble_size == 12

    def test_neet_style_columns(self):
        """Test NEET style has 2 columns."""
        assert NEET_2COLUMN.columns == 2

    def test_neet_style_omr_bubbles(self):
        """Test NEET style has OMR bubble configuration."""
        assert hasattr(NEET_2COLUMN, "omr_bubble_size")
        assert NEET_2COLUMN.omr_bubble_size > 0


class TestNCERTStyle:
    """Tests for NCERT style."""

    def test_get_ncert_style(self):
        """Test getting NCERT style."""
        style = get_ncert_style()
        assert style == NCERT
        assert style.typography == "NCERT-standard"

    def test_ncert_style_features(self):
        """Test NCERT style has expected features."""
        assert NCERT.chapter_summary_enabled is True
        assert NCERT.topic_headers_enabled is True

    def test_ncert_style_typography(self):
        """Test NCERT style typography."""
        assert NCERT.title_font == "Times-Bold"
        assert NCERT.body_font == "Times-Roman"


class TestBilingualStyle:
    """Tests for Bilingual style."""

    def test_get_bilingual_style(self):
        """Test getting bilingual style."""
        style = get_bilingual_style()
        assert style == BILINGUAL

    def test_bilingual_style_devanagari(self):
        """Test bilingual style has Devanagari font."""
        assert BILINGUAL.devanagari_font == "NotoSansDevanagari"

    def test_bilingual_style_layout_mode(self):
        """Test bilingual style layout mode."""
        assert BILINGUAL.layout_mode == "sequential"


class TestOMRStyle:
    """Tests for OMR-ready style."""

    def test_get_omr_style(self):
        """Test getting OMR style."""
        style = get_omr_style()
        assert style == OMR_READY

    def test_omr_style_bubble_size(self):
        """Test OMR style has large bubble size."""
        assert OMR_READY.omr_bubble_size == 14

    def test_omr_style_features(self):
        """Test OMR style has expected features."""
        assert OMR_READY.id_alignment_enabled is True
        assert OMR_READY.answer_key_page_enabled is True


class TestStyleMap:
    """Tests for style mapping."""

    def test_get_pdf_style_default(self):
        """Test getting default style."""
        style = get_pdf_style("default")
        assert style is not None

    def test_get_pdf_style_neet_2column(self):
        """Test getting NEET 2-column style."""
        style = get_pdf_style("neet-2column")
        assert style == NEET_2COLUMN

    def test_get_pdf_style_neet_alias(self):
        """Test getting NEET style alias."""
        style = get_pdf_style("neet")
        assert style == NEET_2COLUMN

    def test_get_pdf_style_ncert(self):
        """Test getting NCERT style."""
        style = get_pdf_style("ncert")
        assert style == NCERT

    def test_get_pdf_style_bilingual(self):
        """Test getting bilingual style."""
        style = get_pdf_style("bilingual")
        assert style == BILINGUAL

    def test_get_pdf_style_omr_ready(self):
        """Test getting OMR-ready style."""
        style = get_pdf_style("omr-ready")
        assert style == OMR_READY

    def test_get_pdf_style_omr_alias(self):
        """Test getting OMR style alias."""
        style = get_pdf_style("omr")
        assert style == OMR_READY


class TestPDFRendererWithStyles:
    """Tests for PDF renderer with different styles."""

    def test_renderer_with_neet_style(self, sample_quiz):
        """Test renderer with NEET style."""
        renderer = PDFRenderer(quiz=sample_quiz, style="neet-2column")
        assert renderer.style == NEET_2COLUMN

    def test_renderer_with_ncert_style(self, sample_quiz):
        """Test renderer with NCERT style."""
        renderer = PDFRenderer(quiz=sample_quiz, style="ncert")
        assert renderer.style == NCERT

    def test_renderer_with_bilingual_style(self, sample_quiz):
        """Test renderer with bilingual style."""
        renderer = PDFRenderer(quiz=sample_quiz, style="bilingual")
        assert renderer.style == BILINGUAL

    def test_renderer_with_omr_style(self, sample_quiz):
        """Test renderer with OMR-ready style."""
        renderer = PDFRenderer(quiz=sample_quiz, style="omr-ready")
        assert renderer.style == OMR_READY


class TestPDFBuilderWithStyles:
    """Tests for PDF builder with different styles."""

    def test_build_neet_2column(self, sample_quiz_file):
        """Test building PDF with NEET 2-column style."""
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            output_path = f.name

        try:
            PDFBuilder.build(
                input_path=sample_quiz_file,
                output_path=output_path,
                style="neet-2column",
            )
            assert Path(output_path).exists()
            assert Path(output_path).stat().st_size > 0
        finally:
            os.unlink(output_path)

    def test_build_ncert(self, sample_quiz_file):
        """Test building PDF with NCERT style."""
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            output_path = f.name

        try:
            PDFBuilder.build(
                input_path=sample_quiz_file,
                output_path=output_path,
                style="ncert",
            )
            assert Path(output_path).exists()
        finally:
            os.unlink(output_path)

    def test_build_bilingual(self, sample_quiz_file):
        """Test building PDF with bilingual style."""
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            output_path = f.name

        try:
            PDFBuilder.build(
                input_path=sample_quiz_file,
                output_path=output_path,
                style="bilingual",
            )
            assert Path(output_path).exists()
        finally:
            os.unlink(output_path)

    def test_build_omr_ready(self, sample_quiz_file):
        """Test building PDF with OMR-ready style."""
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            output_path = f.name

        try:
            PDFBuilder.build(
                input_path=sample_quiz_file,
                output_path=output_path,
                style="omr-ready",
            )
            assert Path(output_path).exists()
        finally:
            os.unlink(output_path)