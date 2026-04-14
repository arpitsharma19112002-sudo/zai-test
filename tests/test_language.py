"""Tests for language selection feature."""

import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock



class TestLanguageSelection:
    """Test language selection at CLI start."""

    def test_language_option_english(self):
        """Test that --language english works."""
        from biopress.generators.translator import Translator

        translator = Translator("english")
        assert translator.language == "english"

    def test_language_option_hindi(self):
        """Test that --language hindi works."""
        from biopress.generators.translator import Translator

        translator = Translator("hindi")
        assert translator.language == "hindi"

    def test_translator_hindi_labels(self):
        """Test Hindi translations for UI labels."""
        from biopress.generators.translator import Translator

        translator = Translator("hindi")

        assert translator.get_label("question") == "प्रश्न"
        assert translator.get_label("options") == "विकल्प"
        assert translator.get_label("correct_answer") == "सही उत्तर"
        assert translator.get_label("explanation") == "स्पष्टीकरण"

    def test_translator_english_labels(self):
        """Test English labels remain unchanged."""
        from biopress.generators.translator import Translator

        translator = Translator("english")

        assert translator.get_label("question") == "question"
        assert translator.get_label("options") == "options"

    def test_translate_quiz_hindi(self):
        """Test quiz translation to Hindi."""
        from biopress.generators.translator import Translator

        translator = Translator("hindi")
        quiz_data = {
            "items": [
                {
                    "question": "What is physics?",
                    "options": ["A", "B", "C", "D"],
                    "correct_answer": "A",
                }
            ]
        }

        result = translator.translate_quiz(quiz_data)
        assert "items" in result

    def test_config_persists_language(self):
        """Test that language is saved to config."""
        from biopress.core.config import ConfigManager

        with tempfile.TemporaryDirectory() as tmpdir:
            config_mgr = ConfigManager()
            config_mgr.CONFIG_DIR = Path(tmpdir)
            config_mgr.CONFIG_FILE = Path(tmpdir) / "config.json"

            config_mgr.set("language", "hindi")
            assert config_mgr.get("language") == "hindi"

            config_mgr.set("language", "english")
            assert config_mgr.get("language") == "english"

    def test_resolve_language_from_config(self):
        """Test that language is resolved from saved config."""
        from biopress.cli.commands.generate import _resolve_language

        with patch("biopress.cli.commands.generate.get_config_manager") as mock_config:
            mock_mgr = MagicMock()
            mock_mgr.get.return_value = "hindi"
            mock_config.return_value = mock_mgr

            result = _resolve_language(None)
            assert result == "hindi"

    def test_resolve_language_from_argument(self):
        """Test that language argument takes precedence."""
        from biopress.cli.commands.generate import _resolve_language

        with patch("biopress.cli.commands.generate.get_config_manager"):
            result = _resolve_language("hindi")
            assert result == "hindi"

    def test_resolve_language_default(self):
        """Test default language when none saved."""
        from biopress.cli.commands.generate import _resolve_language

        with patch("biopress.cli.commands.generate.get_config_manager") as mock_config:
            mock_mgr = MagicMock()
            mock_mgr.get.return_value = None
            mock_config.return_value = mock_mgr

            result = _resolve_language(None)
            assert result == "english"
