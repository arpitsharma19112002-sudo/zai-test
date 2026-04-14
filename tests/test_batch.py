"""Tests for batch question generator."""

import pytest
import json
from biopress.generators.questions.batch import BatchGenerator
from biopress.core.models import BatchQuiz


class TestBatchGenerator:
    """Test cases for BatchGenerator."""

    @pytest.fixture
    def generator(self, tmp_path):
        templates_dir = tmp_path / "templates"
        templates_dir.mkdir()
        
        mcq_data = {
            "default": [
                {"question": "What is force?", "options": {"A": "1", "B": "2", "C": "3", "D": "4"}, "correct_answer": "A", "explanation": "Test"}
            ]
        }
        
        numerical_data = {
            "default": [
                {"question": "Calculate force", "answer": 10, "solution_steps": ["F=ma"], "units": "N"}
            ]
        }
        
        case_based_data = {
            "default": [
                {"passage": "Test passage", "questions": [{"question": "Q1", "answer": "A1"}]}
            ]
        }
        
        assertion_reason_data = {
            "default": [
                {"assertion": "A", "reason": "R", "correct_option": "A", "explanation": "Test"}
            ]
        }
        
        with open(templates_dir / "physics.json", "w") as f:
            json.dump(mcq_data, f)
        with open(templates_dir / "numerical_physics.json", "w") as f:
            json.dump(numerical_data, f)
        with open(templates_dir / "case_based_biology.json", "w") as f:
            json.dump(case_based_data, f)
        with open(templates_dir / "assertion_reason_physics.json", "w") as f:
            json.dump(assertion_reason_data, f)
        
        return BatchGenerator(templates_dir=str(templates_dir))

    def test_generate_batch_questions_all_types(self, generator):
        """Test generating batch questions with all types."""
        quiz = generator.generate(
            exam="NEET",
            subject="Physics",
            count=4,
            topic="default",
            types=["mcq", "numerical", "case-based", "assertion-reason"],
        )
        
        assert isinstance(quiz, BatchQuiz)
        assert len(quiz.items) == 4
        assert "mcq" in quiz.type_counts
        assert "numerical" in quiz.type_counts
        assert "case-based" in quiz.type_counts
        assert "assertion-reason" in quiz.type_counts

    def test_generate_batch_with_single_type(self, generator):
        """Test generating batch with single type."""
        quiz = generator.generate(
            exam="NEET",
            subject="Physics",
            count=2,
            topic="default",
            types=["mcq"],
        )
        
        assert len(quiz.items) == 2

    def test_batch_generation_time_recorded(self, generator):
        """Test that generation time is recorded."""
        quiz = generator.generate(
            exam="NEET",
            subject="Physics",
            count=4,
            topic="default",
        )
        
        assert quiz.generation_time >= 0

    def test_to_json(self, generator):
        """Test JSON serialization."""
        quiz = generator.generate(
            exam="NEET",
            subject="Physics",
            count=2,
            topic="default",
        )
        
        json_output = generator.to_json(quiz)
        parsed = json.loads(json_output)
        
        assert "items" in parsed
        assert "type_counts" in parsed
        assert "generation_time" in parsed

    def test_distribution_count(self, generator):
        """Test that questions are distributed among types."""
        quiz = generator.generate(
            exam="NEET",
            subject="Physics",
            count=10,
            topic="default",
            types=["mcq", "numerical"],
        )
        
        total = sum(quiz.type_counts.values())
        assert total == 10
