"""Tests for preview feature."""

import json



class TestPreviewFeature:
    """Test output preview before export."""

    def test_preview_summary_generation(self):
        """Test that preview summary shows question count."""
        from biopress.cli.commands.review import generate_preview_summary

        data = {
            "items": [
                {"question": "What is physics?", "options": ["A", "B", "C", "D"], "type": "mcq"},
                {"question": "What is chemistry?", "options": ["A", "B", "C", "D"], "type": "mcq"},
                {"question": "What is biology?", "options": ["A", "B", "C", "D"], "type": "mcq"},
            ]
        }

        result = generate_preview_summary(data)
        assert "3" in result
        assert "questions" in result.lower()

    def test_preview_topic_coverage(self):
        """Test that preview shows topic coverage."""
        from biopress.cli.commands.review import generate_preview_summary
        from io import StringIO
        from contextlib import redirect_stdout

        data = {
            "items": [
                {"question": "Q1", "options": ["A", "B", "C", "D"], "topic": "mechanics"},
                {"question": "Q2", "options": ["A", "B", "C", "D"], "topic": "thermodynamics"},
            ]
        }

        output = StringIO()
        with redirect_stdout(output):
            generate_preview_summary(data)
        result = output.getvalue()
        assert "mechanics" in result
        assert "thermodynamics" in result

    def test_preview_validation_status(self):
        """Test that preview shows validation status."""
        from biopress.cli.commands.review import generate_preview_summary
        from io import StringIO
        from contextlib import redirect_stdout

        data = {
            "items": [
                {"question": "Q1", "options": ["A", "B", "C", "D"]},
                {"question": "Q2", "options": ["A", "B", "C", "D"]},
            ]
        }

        output = StringIO()
        with redirect_stdout(output):
            generate_preview_summary(data)
        result = output.getvalue()
        assert "Valid" in result

    def test_preview_partial_validation(self):
        """Test preview shows partial validation status."""
        from biopress.cli.commands.review import generate_preview_summary
        from io import StringIO
        from contextlib import redirect_stdout

        data = {
            "items": [
                {"question": "Q1", "options": ["A", "B", "C", "D"]},
                {"question": "Q2"},
            ]
        }

        output = StringIO()
        with redirect_stdout(output):
            generate_preview_summary(data)
        result = output.getvalue()
        assert "Partial" in result or "1/2" in result

    def test_preview_with_json_file(self):
        """Test preview with actual JSON file."""
        from biopress.cli.commands.review import generate_preview_summary
        import tempfile

        data = {
            "items": [
                {"question": "Test Q1", "options": ["A", "B", "C", "D"]},
            ]
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(data, f)
            f.flush()

            with open(f.name) as fh:
                loaded_data = json.load(fh)

        result = generate_preview_summary(loaded_data)
        assert "1" in result
        assert "questions" in result.lower()

    def test_preview_empty_questions(self):
        """Test preview with no questions."""
        from biopress.cli.commands.review import generate_preview_summary

        data = {"items": []}
        result = generate_preview_summary(data)
        assert "0" in result

    def test_preview_missing_items(self):
        """Test preview with missing items key."""
        from biopress.cli.commands.review import generate_preview_summary

        data = {}
        result = generate_preview_summary(data)
        assert "0" in result
