"""Tests for numerical question generator."""

import pytest
import json
from biopress.generators.questions.numerical import NumericalGenerator
from biopress.core.models import NumericalQuiz


class TestNumericalGenerator:
    """Test cases for NumericalGenerator."""

    @pytest.fixture
    def generator(self, tmp_path):
        templates_dir = tmp_path / "templates"
        templates_dir.mkdir()
        
        template_data = {
            "kinematics": [
                {
                    "question": "A car accelerates from rest at 2 m/s². Calculate distance in 5 seconds.",
                    "answer": 25,
                    "solution_steps": ["v = u + at = 0 + 2*5 = 10 m/s", "s = ut + 0.5at² = 0 + 0.5*2*25 = 25 m"],
                    "units": "meters"
                }
            ],
            "default": [
                {
                    "question": "Find acceleration when force is 10N and mass is 2kg.",
                    "answer": 5,
                    "solution_steps": ["a = F/m = 10/2 = 5 m/s²"],
                    "units": "m/s²"
                }
            ]
        }
        
        with open(templates_dir / "numerical_physics.json", "w") as f:
            json.dump(template_data, f)
        
        return NumericalGenerator(templates_dir=str(templates_dir))

    def test_generate_numerical_questions(self, generator):
        """Test generating numerical questions."""
        quiz = generator.generate(
            exam="NEET",
            subject="Physics",
            count=2,
            topic="kinematics",
        )
        
        assert isinstance(quiz, NumericalQuiz)
        assert len(quiz.items) == 2
        assert quiz.items[0].question == "A car accelerates from rest at 2 m/s². Calculate distance in 5 seconds."
        assert quiz.items[0].answer == 25
        assert len(quiz.items[0].solution_steps) == 2

    def test_generate_with_default_topic(self, generator):
        """Test generating with default topic."""
        quiz = generator.generate(
            exam="NEET",
            subject="Physics",
            count=1,
            topic="nonexistent",
        )
        
        assert len(quiz.items) == 1
        assert quiz.items[0].answer == 5

    def test_to_json(self, generator):
        """Test JSON serialization."""
        quiz = generator.generate(
            exam="NEET",
            subject="Physics",
            count=1,
            topic="kinematics",
        )
        
        json_output = generator.to_json(quiz)
        parsed = json.loads(json_output)
        
        assert "items" in parsed
        assert len(parsed["items"]) == 1

    def test_answer_types(self, generator):
        """Test that answers can be int or float."""
        quiz = generator.generate(
            exam="NEET",
            subject="Physics",
            count=1,
            topic="kinematics",
        )
        
        assert isinstance(quiz.items[0].answer, (int, float))
