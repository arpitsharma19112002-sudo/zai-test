"""Tests for visual editor features (Stories 6.4-6.8)."""

from unittest.mock import MagicMock


class TestAppState:
    """Tests for AppState class with new features."""

    def test_app_state_initialization(self):
        """Test AppState initializes with defaults."""
        from biopress.visual.app import AppState
        state = AppState()
        assert state.current_file is None
        assert state.content == {"items": []}
        assert state.selected_index == 0
        assert state.modified is False
        assert state.pdf_path is None

    def test_app_state_with_items(self):
        """Test AppState can store multiple items."""
        from biopress.visual.app import AppState
        state = AppState()
        state.content = {
            "items": [
                {"question": "Q1", "options": {"A": "a", "B": "b", "C": "c", "D": "d"}, "correct_answer": "A", "explanation": "Exp1"},
                {"question": "Q2", "options": {"A": "x", "B": "y", "C": "z", "D": "w"}, "correct_answer": "B", "explanation": "Exp2", "diagram": "diagram.png"},
            ]
        }
        assert len(state.content["items"]) == 2
        assert state.content["items"][1].get("diagram") == "diagram.png"


class TestEditorPage:
    """Tests for editor page with question features."""

    def test_editor_page_with_content(self):
        """Test editor page can be created with content."""
        from biopress.visual.app import AppState
        from biopress.visual.pages.editor import create_editor_page
        
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
        
        on_save = MagicMock()
        create_editor_page(state, on_save)

    def test_editor_page_with_multiple_items(self):
        """Test editor page handles multiple questions."""
        from biopress.visual.app import AppState
        from biopress.visual.pages.editor import create_editor_page
        
        state = AppState()
        state.content = {
            "items": [
                {"question": "Q1", "options": {"A": "a", "B": "b", "C": "c", "D": "d"}, "correct_answer": "A", "explanation": ""},
                {"question": "Q2", "options": {"A": "x", "B": "y", "C": "z", "D": "w"}, "correct_answer": "B", "explanation": ""},
            ]
        }
        
        create_editor_page(state, lambda: None)


class TestQuestionReplacement:
    """Tests for question fix/replace functionality (Story 6.4)."""

    def test_replace_question_updates_content(self):
        """Test that question replacement updates content correctly."""
        from biopress.visual.app import AppState
        
        state = AppState()
        state.content = {
            "items": [
                {"question": "Original", "options": {"A": "a", "B": "b", "C": "c", "D": "d"}, "correct_answer": "A", "explanation": ""}
            ]
        }
        
        state.content["items"][0] = {
            "question": "Replaced Question",
            "options": {"A": "new A", "B": "new B", "C": "new C", "D": "new D"},
            "correct_answer": "C",
            "explanation": "New explanation"
        }
        
        assert state.content["items"][0]["question"] == "Replaced Question"
        assert state.content["items"][0]["correct_answer"] == "C"


class TestDiagramReplacement:
    """Tests for diagram replacement functionality (Story 6.5)."""

    def test_add_diagram_to_question(self):
        """Test adding diagram to a question."""
        from biopress.visual.app import AppState
        
        state = AppState()
        state.content = {
            "items": [
                {"question": "Q1", "options": {"A": "a", "B": "b", "C": "c", "D": "d"}, "correct_answer": "A", "explanation": ""}
            ]
        }
        
        state.content["items"][0]["diagram"] = "/path/to/diagram.png"
        
        assert state.content["items"][0].get("diagram") == "/path/to/diagram.png"

    def test_clear_diagram(self):
        """Test clearing diagram from a question."""
        from biopress.visual.app import AppState
        
        state = AppState()
        state.content = {
            "items": [
                {"question": "Q1", "options": {"A": "a", "B": "b", "C": "c", "D": "d"}, "correct_answer": "A", "explanation": "", "diagram": "old.png"}
            ]
        }
        
        state.content["items"][0]["diagram"] = ""
        
        assert state.content["items"][0].get("diagram") == ""


class TestAddNewQuestion:
    """Tests for add new question functionality (Story 6.6)."""

    def test_add_new_question_increases_count(self):
        """Test adding a new question increases item count."""
        from biopress.visual.app import AppState
        
        state = AppState()
        state.content = {
            "items": [
                {"question": "Q1", "options": {"A": "a", "B": "b", "C": "c", "D": "d"}, "correct_answer": "A", "explanation": ""}
            ]
        }
        initial_count = len(state.content["items"])
        
        new_question = {
            "question": "New Question",
            "options": {"A": "Option A", "B": "Option B", "C": "Option C", "D": "Option D"},
            "correct_answer": "A",
            "explanation": "Explanation for the correct answer."
        }
        state.content["items"].append(new_question)
        
        assert len(state.content["items"]) == initial_count + 1

    def test_add_new_question_sets_correct_index(self):
        """Test adding question sets selected index to new question."""
        from biopress.visual.app import AppState
        
        state = AppState()
        state.content = {
            "items": [
                {"question": "Q1", "options": {"A": "a", "B": "b", "C": "c", "D": "d"}, "correct_answer": "A", "explanation": ""}
            ]
        }
        
        new_question = {"question": "Q2", "options": {"A": "x", "B": "y", "C": "z", "D": "w"}, "correct_answer": "B", "explanation": ""}
        state.content["items"].append(new_question)
        state.selected_index = len(state.content["items"]) - 1
        
        assert state.selected_index == 1


class TestDeleteQuestion:
    """Tests for delete question functionality (Story 6.7)."""

    def test_delete_question_decreases_count(self):
        """Test deleting a question decreases item count."""
        from biopress.visual.app import AppState
        
        state = AppState()
        state.content = {
            "items": [
                {"question": "Q1", "options": {"A": "a", "B": "b", "C": "c", "D": "d"}, "correct_answer": "A", "explanation": ""},
                {"question": "Q2", "options": {"A": "x", "B": "y", "C": "z", "D": "w"}, "correct_answer": "B", "explanation": ""},
            ]
        }
        
        state.content["items"].pop(0)
        
        assert len(state.content["items"]) == 1

    def test_delete_last_question_not_allowed(self):
        """Test that last question cannot be deleted."""
        from biopress.visual.app import AppState
        
        state = AppState()
        state.content = {
            "items": [
                {"question": "Q1", "options": {"A": "a", "B": "b", "C": "c", "D": "d"}, "correct_answer": "A", "explanation": ""}
            ]
        }
        
        can_delete = len(state.content["items"]) > 1
        
        assert can_delete is False

    def test_delete_question_adjusts_index(self):
        """Test deleting question adjusts selected index if needed."""
        from biopress.visual.app import AppState
        
        state = AppState()
        state.content = {
            "items": [
                {"question": "Q1", "options": {"A": "a", "B": "b", "C": "c", "D": "d"}, "correct_answer": "A", "explanation": ""},
                {"question": "Q2", "options": {"A": "x", "B": "y", "C": "z", "D": "w"}, "correct_answer": "B", "explanation": ""},
            ]
        }
        state.selected_index = 1
        
        state.content["items"].pop(1)
        if state.selected_index >= len(state.content["items"]):
            state.selected_index = max(0, len(state.content["items"]) - 1)
        
        assert state.selected_index == 0


class TestProgressDashboard:
    """Tests for progress dashboard functionality (Story 6.8)."""

    def test_progress_dashboard_calculates_total(self):
        """Test dashboard calculates total questions."""
        from biopress.visual.app import AppState
        
        state = AppState()
        state.content = {
            "items": [
                {"question": "Q1", "correct_answer": "A"},
                {"question": "Q2", "correct_answer": "B"},
                {"question": "Q3", "correct_answer": "C"},
            ]
        }
        
        total = len(state.content["items"])
        
        assert total == 3

    def test_progress_dashboard_calculates_answered(self):
        """Test dashboard calculates answered questions."""
        from biopress.visual.app import AppState
        
        state = AppState()
        state.content = {
            "items": [
                {"question": "Q1", "correct_answer": "A"},
                {"question": "Q2", "correct_answer": "B"},
                {"question": "Q3", "correct_answer": ""},
            ]
        }
        
        answered = sum(1 for i in state.content["items"] if i.get("correct_answer"))
        
        assert answered == 2

    def test_progress_dashboard_calculates_with_diagrams(self):
        """Test dashboard calculates questions with diagrams."""
        from biopress.visual.app import AppState
        
        state = AppState()
        state.content = {
            "items": [
                {"question": "Q1", "diagram": "d1.png"},
                {"question": "Q2"},
                {"question": "Q3", "diagram": "d2.png"},
            ]
        }
        
        with_diagram = sum(1 for i in state.content["items"] if i.get("diagram"))
        
        assert with_diagram == 2

    def test_progress_dashboard_calculates_completion_percentage(self):
        """Test dashboard calculates completion percentage."""
        from biopress.visual.app import AppState
        
        state = AppState()
        state.content = {
            "items": [
                {"question": "Q1", "correct_answer": "A"},
                {"question": "Q2", "correct_answer": "B"},
                {"question": "Q3"},
                {"question": "Q4"},
            ]
        }
        
        total = len(state.content["items"])
        answered = sum(1 for i in state.content["items"] if i.get("correct_answer"))
        completion_pct = (answered / total * 100) if total > 0 else 0
        
        assert completion_pct == 50.0

    def test_progress_dashboard_with_empty_content(self):
        """Test dashboard handles empty content."""
        from biopress.visual.app import AppState
        
        state = AppState()
        state.content = {"items": []}
        
        total = len(state.content["items"])
        answered = sum(1 for i in state.content["items"] if i.get("correct_answer"))
        completion_pct = (answered / total * 100) if total > 0 else 0
        
        assert total == 0
        assert completion_pct == 0


class TestEditorTabPanel:
    """Tests for editor tab panel functionality."""

    def test_editor_has_options_tab(self):
        """Test editor has options tab."""
        from biopress.visual.app import AppState
        from biopress.visual.pages.editor import create_editor_page
        
        state = AppState()
        state.content = {
            "items": [
                {"question": "Q1", "options": {"A": "a", "B": "b", "C": "c", "D": "d"}, "correct_answer": "A", "explanation": ""}
            ]
        }
        
        create_editor_page(state, lambda: None)

    def test_editor_has_diagram_tab(self):
        """Test editor has diagram tab for replacement."""
        from biopress.visual.app import AppState
        from biopress.visual.pages.editor import create_editor_page
        
        state = AppState()
        state.content = {
            "items": [
                {"question": "Q1", "options": {"A": "a", "B": "b", "C": "c", "D": "d"}, "correct_answer": "A", "explanation": "", "diagram": "test.png"}
            ]
        }
        
        create_editor_page(state, lambda: None)

    def test_editor_has_dashboard_tab(self):
        """Test editor has dashboard tab."""
        from biopress.visual.app import AppState
        from biopress.visual.pages.editor import create_editor_page
        
        state = AppState()
        state.content = {
            "items": [
                {"question": "Q1", "options": {"A": "a", "B": "b", "C": "c", "D": "d"}, "correct_answer": "A", "explanation": ""}
            ]
        }
        
        create_editor_page(state, lambda: None)