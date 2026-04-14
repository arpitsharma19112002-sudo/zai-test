"""Tests for MCQ generation."""

import json
from biopress.generators.questions.mcq import MCQGenerator
from biopress.core.models import MCQItem, PerseusQuiz


class TestMCQGenerator:
    """Test cases for MCQGenerator."""

    def test_generator_init(self):
        """Test generator initialization."""
        gen = MCQGenerator()
        assert gen.templates_dir is not None

    def test_generate_physics(self):
        """Test generating physics questions."""
        gen = MCQGenerator()
        quiz = gen.generate(exam="NEET", subject="Physics", count=3, topic="Newton's Laws")
        
        assert isinstance(quiz, PerseusQuiz)
        assert len(quiz.items) == 3
        
        for item in quiz.items:
            assert isinstance(item, MCQItem)
            assert item.question
            assert item.options.A
            assert item.options.B
            assert item.options.C
            assert item.options.D
            assert item.correct_answer in ["A", "B", "C", "D"]
            assert item.explanation

    def test_generate_chemistry(self):
        """Test generating chemistry questions."""
        gen = MCQGenerator()
        quiz = gen.generate(exam="NEET", subject="Chemistry", count=2, topic="Atomic Structure")
        
        assert isinstance(quiz, PerseusQuiz)
        assert len(quiz.items) == 2

    def test_generate_biology(self):
        """Test generating biology questions."""
        gen = MCQGenerator()
        quiz = gen.generate(exam="NEET", subject="Biology", count=2, topic="Cell Biology")
        
        assert isinstance(quiz, PerseusQuiz)
        assert len(quiz.items) == 2

    def test_generate_default_topic(self):
        """Test generating with default topic."""
        gen = MCQGenerator()
        quiz = gen.generate(exam="NEET", subject="Physics", count=3, topic="default")
        
        assert isinstance(quiz, PerseusQuiz)
        assert len(quiz.items) == 3

    def test_to_json(self):
        """Test JSON output."""
        gen = MCQGenerator()
        quiz = gen.generate(exam="NEET", subject="Physics", count=1, topic="default")
        json_output = gen.to_json(quiz)
        
        assert isinstance(json_output, str)
        data = json.loads(json_output)
        assert "items" in data
        assert len(data["items"]) == 1

    def test_question_format(self):
        """Test question has all required fields."""
        gen = MCQGenerator()
        quiz = gen.generate(exam="NEET", subject="Physics", count=1, topic="Newton's Laws")
        
        item = quiz.items[0]
        assert item.question is not None
        assert hasattr(item, "options")
        assert item.options.A is not None
        assert item.options.B is not None
        assert item.options.C is not None
        assert item.options.D is not None
        assert item.correct_answer in ["A", "B", "C", "D"]
        assert item.explanation is not None


class TestModels:
    """Test data models."""

    def test_mcq_item(self):
        """Test MCQItem model."""
        item = MCQItem(
            question="Test question?",
            options={"A": "opt1", "B": "opt2", "C": "opt3", "D": "opt4"},
            correct_answer="A",
            explanation="Test explanation",
        )
        assert item.question == "Test question?"
        assert item.correct_answer == "A"

    def test_perseus_quiz(self):
        """Test PerseusQuiz model."""
        quiz = PerseusQuiz()
        assert quiz.items == []
        
        item = MCQItem(
            question="Test?",
            options={"A": "a", "B": "b", "C": "c", "D": "d"},
            correct_answer="A",
            explanation="Exp",
        )
        quiz.items.append(item)
        assert len(quiz.items) == 1