"""Tests for assertion-reason question generator."""

import pytest
import json
from biopress.generators.questions.assertion_reason import AssertionReasonGenerator
from biopress.core.models import AssertionReasonQuiz


class TestAssertionReasonGenerator:
    """Test cases for AssertionReasonGenerator."""

    @pytest.fixture
    def generator(self, tmp_path):
        templates_dir = tmp_path / "templates"
        templates_dir.mkdir()
        
        template_data = {
            "newton's laws": [
                {
                    "assertion": "All mammals are warm-blooded.",
                    "reason": "Warm-blooded animals maintain constant body temperature.",
                    "correct_option": "A",
                    "explanation": "Both A and R are true and R explains A."
                }
            ],
            "default": [
                {
                    "assertion": "Acceleration due to gravity is 9.8 m/s².",
                    "reason": "Earth's gravitational pull.",
                    "correct_option": "A",
                    "explanation": "Both are true."
                }
            ]
        }
        
        with open(templates_dir / "assertion_reason_physics.json", "w") as f:
            json.dump(template_data, f)
        
        return AssertionReasonGenerator(templates_dir=str(templates_dir))

    def test_generate_assertion_reason_questions(self, generator):
        """Test generating assertion-reason questions."""
        quiz = generator.generate(
            exam="NEET",
            subject="Physics",
            count=2,
            topic="newton's laws",
        )
        
        assert isinstance(quiz, AssertionReasonQuiz)
        assert len(quiz.items) == 2
        assert quiz.items[0].assertion == "All mammals are warm-blooded."
        assert quiz.items[0].correct_option in ["A", "B", "C", "D"]

    def test_generate_with_default_topic(self, generator):
        """Test generating with default topic."""
        quiz = generator.generate(
            exam="NEET",
            subject="Physics",
            count=1,
            topic="nonexistent",
        )
        
        assert len(quiz.items) == 1
        assert quiz.items[0].assertion == "Acceleration due to gravity is 9.8 m/s²."

    def test_to_json(self, generator):
        """Test JSON serialization."""
        quiz = generator.generate(
            exam="NEET",
            subject="Physics",
            count=1,
            topic="newton's laws",
        )
        
        json_output = generator.to_json(quiz)
        parsed = json.loads(json_output)
        
        assert "items" in parsed
        assert len(parsed["items"]) == 1

    def test_correct_option_values(self, generator):
        """Test that correct_option has valid NEET format values."""
        quiz = generator.generate(
            exam="NEET",
            subject="Physics",
            count=1,
            topic="newton's laws",
        )
        
        assert quiz.items[0].correct_option in ["A", "B", "C", "D"]

    def test_explanation_optional(self, generator):
        """Test that explanation field is optional."""
        quiz = generator.generate(
            exam="NEET",
            subject="Physics",
            count=1,
            topic="newton's laws",
        )
        
        assert hasattr(quiz.items[0], "explanation")
