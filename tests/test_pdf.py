"""Tests for PDF generation."""

import json
import os
import tempfile
from pathlib import Path

import pytest

from biopress.core.models import MCQItem, MCQOptions, PerseusQuiz
from biopress.pdf.builder import PDFBuilder
from biopress.pdf.renderer import PDFRenderer
from biopress.pdf.styles.default import get_style, DEFAULT, NEET, NCERT
from biopress.pdf.styles.neet import NEET_2COLUMN


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


def test_get_style():
    """Test style retrieval."""
    assert get_style("default") == DEFAULT
    assert get_style("neet") == NEET
    assert get_style("ncert") == NCERT
    assert get_style("unknown") == DEFAULT


def test_pdf_renderer_init(sample_quiz):
    """Test PDF renderer initialization."""
    renderer = PDFRenderer(quiz=sample_quiz)
    assert renderer.quiz == sample_quiz
    assert renderer.style == DEFAULT


def test_pdf_renderer_with_style(sample_quiz):
    """Test PDF renderer with custom style."""
    renderer = PDFRenderer(quiz=sample_quiz, style="neet")
    assert renderer.style == NEET_2COLUMN


def test_pdf_builder_load_quiz(sample_quiz_file):
    """Test loading quiz from JSON file."""
    quiz = PDFBuilder.load_quiz(sample_quiz_file)
    assert len(quiz.items) == 2
    assert quiz.items[0].question == "What is the powerhouse of the cell?"


def test_pdf_builder_build(sample_quiz_file):
    """Test PDF building."""
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        output_path = f.name
    
    try:
        PDFBuilder.build(
            input_path=sample_quiz_file,
            output_path=output_path,
        )
        assert Path(output_path).exists()
        assert Path(output_path).stat().st_size > 0
    finally:
        os.unlink(output_path)


def test_pdf_builder_with_custom_title(sample_quiz_file):
    """Test PDF building with custom title."""
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        output_path = f.name
    
    try:
        PDFBuilder.build(
            input_path=sample_quiz_file,
            output_path=output_path,
            title="My Custom Quiz",
            subject="Biology",
            exam_type="NEET",
        )
        assert Path(output_path).exists()
    finally:
        os.unlink(output_path)


def test_pdf_builder_with_style(sample_quiz_file):
    """Test PDF building with different styles."""
    for style_name in ["default", "neet", "ncert"]:
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            output_path = f.name
        
        try:
            PDFBuilder.build(
                input_path=sample_quiz_file,
                output_path=output_path,
                style=style_name,
            )
            assert Path(output_path).exists()
        finally:
            os.unlink(output_path)


def test_empty_quiz():
    """Test handling of empty quiz."""
    quiz = PerseusQuiz(items=[])
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        output_path = f.name
    
    try:
        renderer = PDFRenderer(quiz=quiz)
        renderer.render(output_path)
        assert Path(output_path).exists()
    finally:
        os.unlink(output_path)
