"""Tests for style system."""

import tempfile
from pathlib import Path

import pytest

from biopress.pdf.style_system import (
    StyleSystem,
    StyleLayout,
    create_style_from_description,
    save_style_layout,
)


class TestStyleSystem:
    """Tests for StyleSystem."""

    @pytest.fixture
    def temp_layouts_dir(self, tmp_path):
        """Create temporary layouts directory."""
        layouts_dir = tmp_path / "layouts"
        layouts_dir.mkdir()
        return layouts_dir

    def test_create_style_basic(self):
        """Test creating style from basic description."""
        system = StyleSystem()
        layout = system.create_style("two column exam style")
        assert layout.columns == 2
        assert layout.omr_bubbles is True
        assert layout.font_family == "Helvetica"

    def test_create_style_ncert(self):
        """Test creating NCERT style."""
        system = StyleSystem()
        layout = system.create_style("NCERT textbook style")
        assert layout.columns == 1
        assert "chapter_summary" in layout.special_features
        assert "topic_headers" in layout.special_features
        assert layout.font_family == "Times"

    def test_create_style_bilingual(self):
        """Test creating bilingual style."""
        system = StyleSystem()
        layout = system.create_style("bilingual Hindi English style")
        assert "devanagari_font" in layout.special_features

    def test_create_style_omr(self):
        """Test creating OMR style."""
        system = StyleSystem()
        layout = system.create_style("OMR ready exam style")
        assert layout.omr_bubbles is True
        assert "answer_key_page" in layout.special_features

    def test_create_style_with_name(self):
        """Test creating style with custom name."""
        system = StyleSystem()
        layout = system.create_style("two column exam", name="my_style")
        assert layout.name == "my_style"

    def test_save_layout(self, tmp_path):
        """Test saving layout to file."""
        system = StyleSystem()
        system.LAYOUTS_DIR = tmp_path / "layouts"
        system.LAYOUTS_DIR.mkdir()

        layout = StyleLayout(
            name="test",
            description="test layout",
            columns=2,
            question_layout="grid",
            omr_bubbles=True,
            font_family="Helvetica",
            font_sizes={"title": 20},
            margins={"top": 72.0},
            headers={"exam_name": "include"},
            special_features=[],
        )

        filepath = system.save_layout(layout, "test_layout.json")
        assert filepath.exists()
        assert filepath.name == "test_layout.json"

    def test_load_layout(self, tmp_path):
        """Test loading layout from file."""
        system = StyleSystem()
        system.LAYOUTS_DIR = tmp_path / "layouts"
        system.LAYOUTS_DIR.mkdir()

        layout = StyleLayout(
            name="test",
            description="test layout",
            columns=2,
            question_layout="grid",
            omr_bubbles=True,
            font_family="Helvetica",
            font_sizes={"title": 20},
            margins={"top": 72.0},
            headers={"exam_name": "include"},
            special_features=[],
        )

        system.save_layout(layout, "test_layout.json")
        loaded = system.load_layout("test_layout.json")

        assert loaded.name == "test"
        assert loaded.columns == 2


class TestStyleLayout:
    """Tests for StyleLayout dataclass."""

    def test_style_layout_creation(self):
        """Test creating StyleLayout."""
        layout = StyleLayout(
            name="test",
            description="test",
            columns=1,
            question_layout="vertical",
            omr_bubbles=False,
            font_family="Helvetica",
            font_sizes={"title": 20},
            margins={"top": 72.0},
            headers={},
            special_features=[],
        )

        assert layout.name == "test"
        assert layout.columns == 1


class TestConvenienceFunctions:
    """Tests for convenience functions."""

    def test_create_style_from_description(self):
        """Test convenience function."""
        layout = create_style_from_description("2 column exam style")
        assert layout.columns == 2

    def test_save_style_layout(self, tmp_path):
        """Test saving style layout."""
        layout = StyleLayout(
            name="test",
            description="test",
            columns=1,
            question_layout="vertical",
            omr_bubbles=False,
            font_family="Helvetica",
            font_sizes={"title": 20},
            margins={"top": 72.0},
            headers={},
            special_features=[],
        )

        with tempfile.TemporaryDirectory() as td:
            from biopress.pdf import style_system
            original = style_system.StyleSystem.LAYOUTS_DIR
            style_system.StyleSystem.LAYOUTS_DIR = Path(td) / "layouts"
            style_system.StyleSystem().LAYOUTS_DIR.mkdir(parents=True, exist_ok=True)

            try:
                filepath = save_style_layout(layout, "test.json")
                assert filepath.exists()
            finally:
                style_system.StyleSystem.LAYOUTS_DIR = original