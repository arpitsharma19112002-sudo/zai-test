"""Tests for case-based question generator."""

import pytest
import json
from biopress.generators.questions.case_based import CaseBasedGenerator
from biopress.core.models import CaseBasedQuiz


class TestCaseBasedGenerator:
    """Test cases for CaseBasedGenerator."""

    @pytest.fixture
    def generator(self, tmp_path):
        templates_dir = tmp_path / "templates"
        templates_dir.mkdir()
        
        template_data = {
            "diabetes": [
                {
                    "passage": "A 45-year-old patient presents with increased thirst.",
                    "questions": [
                        {"question": "What is the diagnosis?", "answer": "Type 2 Diabetes"},
                        {"question": "What test confirms?", "answer": "HbA1c"}
                    ]
                }
            ],
            "default": [
                {
                    "passage": "A patient presents with fever and cough.",
                    "questions": [
                        {"question": "What is the likely diagnosis?", "answer": "Pneumonia"}
                    ]
                }
            ]
        }
        
        with open(templates_dir / "case_based_biology.json", "w") as f:
            json.dump(template_data, f)
        
        return CaseBasedGenerator(templates_dir=str(templates_dir))

    def test_generate_case_based_questions(self, generator):
        """Test generating case-based questions."""
        quiz = generator.generate(
            exam="NEET",
            subject="Biology",
            count=2,
            topic="diabetes",
        )
        
        assert isinstance(quiz, CaseBasedQuiz)
        assert len(quiz.items) == 2
        assert quiz.items[0].passage == "A 45-year-old patient presents with increased thirst."
        assert len(quiz.items[0].questions) == 2

    def test_generate_with_default_topic(self, generator):
        """Test generating with default topic."""
        quiz = generator.generate(
            exam="NEET",
            subject="Biology",
            count=1,
            topic="nonexistent",
        )
        
        assert len(quiz.items) == 1
        assert quiz.items[0].passage == "A patient presents with fever and cough."
        assert len(quiz.items[0].questions) == 1

    def test_to_json(self, generator):
        """Test JSON serialization."""
        quiz = generator.generate(
            exam="NEET",
            subject="Biology",
            count=1,
            topic="diabetes",
        )
        
        json_output = generator.to_json(quiz)
        parsed = json.loads(json_output)
        
        assert "items" in parsed
        assert len(parsed["items"]) == 1

    def test_sub_questions_count(self, generator):
        """Test that sub-questions are properly formatted."""
        quiz = generator.generate(
            exam="NEET",
            subject="Biology",
            count=1,
            topic="diabetes",
        )
        
        item = quiz.items[0]
        assert all(hasattr(q, "question") and hasattr(q, "answer") for q in item.questions)
