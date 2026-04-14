"""Tests for visual review tool."""

import json
import os
import tempfile

from typer.testing import CliRunner

from biopress.cli.app import app

runner = CliRunner()


def test_review_launch_help():
    """Test that launch command has proper help."""
    result = runner.invoke(app, ["review", "launch", "--help"])
    assert result.exit_code == 0
    assert "--load" in result.stdout
    assert "--port" in result.stdout


def test_review_run_help():
    """Test that run command has proper help."""
    result = runner.invoke(app, ["review", "run", "--help"])
    assert result.exit_code == 0
    assert "--load" in result.stdout
    assert "--port" in result.stdout


def test_review_command_shows_available():
    """Test that 'biopress review' has subcommands available."""
    result = runner.invoke(app, ["review", "--help"])
    assert result.exit_code == 0
    assert "launch" in result.stdout or "run" in result.stdout


def test_load_nonexistent_file():
    """Test that loading a nonexistent file shows error."""
    result = runner.invoke(app, ["review", "launch", "--load", "/nonexistent/file.json"])
    assert result.exit_code == 1


class TestAppState:
    """Tests for AppState class."""

    def test_app_state_initialization(self):
        """Test AppState initializes with defaults."""
        from biopress.visual.app import AppState
        state = AppState()
        assert state.current_file is None
        assert state.content == {"items": []}
        assert state.selected_index == 0
        assert state.modified is False
        assert state.pdf_path is None

    def test_app_state_can_store_content(self):
        """Test AppState can store content."""
        from biopress.visual.app import AppState
        state = AppState()
        state.content = {
            "items": [
                {
                    "question": "Test question?",
                    "options": {"A": "a", "B": "b", "C": "c", "D": "d"},
                    "correct_answer": "A",
                    "explanation": "Test explanation"
                }
            ]
        }
        assert len(state.content["items"]) == 1
        assert state.content["items"][0]["question"] == "Test question?"


class TestElementList:
    """Tests for element list component."""

    def test_element_list_creation(self):
        """Test element list can be created with empty items."""
        from biopress.visual.app import AppState
        from biopress.visual.components.element_list import create_element_list
        state = AppState()
        create_element_list(state)


class TestEditorPage:
    """Tests for editor page component."""

    def test_editor_page_creation(self):
        """Test editor page can be created."""
        from biopress.visual.app import AppState
        from biopress.visual.pages.editor import create_editor_page
        state = AppState()
        create_editor_page(state, lambda: None)


class TestPDFViewer:
    """Tests for PDF viewer component."""

    def test_pdf_viewer_creation(self):
        """Test PDF viewer can be created."""
        from biopress.visual.app import AppState
        from biopress.visual.components.pdf_viewer import create_pdf_viewer
        state = AppState()
        create_pdf_viewer(state)


class TestLoadSave:
    """Tests for file loading and saving."""

    def test_save_content_to_file(self):
        """Test saving content to a temp file."""
        from biopress.visual.app import AppState
        state = AppState()
        state.content = {
            "items": [
                {
                    "question": "Test question?",
                    "options": {"A": "a", "B": "b", "C": "c", "D": "d"},
                    "correct_answer": "A",
                    "explanation": "Test"
                }
            ]
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            temp_path = f.name

        try:
            with open(temp_path, "w") as f:
                json.dump(state.content, f, indent=2)

            with open(temp_path) as f:
                loaded = json.load(f)

            assert len(loaded["items"]) == 1
            assert loaded["items"][0]["question"] == "Test question?"
        finally:
            os.unlink(temp_path)

    def test_load_content_from_file(self):
        """Test loading content from a temp file."""
        from biopress.visual.app import AppState

        test_content = {
            "items": [
                {
                    "question": "Loaded question?",
                    "options": {"A": "x", "B": "y", "C": "z", "D": "w"},
                    "correct_answer": "B",
                    "explanation": "Loaded explanation"
                }
            ]
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(test_content, f)
            temp_path = f.name

        try:
            state = AppState()
            with open(temp_path) as f:
                state.content = json.load(f)

            assert len(state.content["items"]) == 1
            assert state.content["items"][0]["question"] == "Loaded question?"
        finally:
            os.unlink(temp_path)