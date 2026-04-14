"""Shared test fixtures for BioPress test suite.

Centralizes commonly used fixtures (sample quizzes, temp template dirs,
temp files) so individual test modules don't duplicate boilerplate.
"""

import json
import os
import tempfile

import pytest

from biopress.core.models import MCQItem, MCQOptions, PerseusQuiz


# ------------------------------------------------------------------
# Quiz fixtures
# ------------------------------------------------------------------

@pytest.fixture
def sample_mcq_options():
    """Standard 4-option MCQ options."""
    return MCQOptions(
        A="Nucleus",
        B="Mitochondria",
        C="Ribosome",
        D="Golgi apparatus",
    )


@pytest.fixture
def sample_quiz():
    """A minimal PerseusQuiz with 2 biology questions."""
    items = [
        MCQItem(
            question="What is the powerhouse of the cell?",
            options=MCQOptions(
                A="Nucleus",
                B="Mitochondria",
                C="Ribosome",
                D="Golgi apparatus",
            ),
            correct_answer="B",
            explanation="Mitochondria produce ATP through cellular respiration.",
        ),
        MCQItem(
            question="What is the chemical formula for water?",
            options=MCQOptions(
                A="H2O",
                B="CO2",
                C="NaCl",
                D="O2",
            ),
            correct_answer="A",
            explanation="Water is composed of two hydrogen atoms and one oxygen atom.",
        ),
    ]
    return PerseusQuiz(items=items)


@pytest.fixture
def sample_quiz_file(sample_quiz):
    """Write a sample quiz to a temp JSON file and yield its path.

    Automatically cleaned up after the test.
    """
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump({"items": [item.model_dump() for item in sample_quiz.items]}, f)
        temp_path = f.name
    yield temp_path
    os.unlink(temp_path)


# ------------------------------------------------------------------
# Template directory fixture
# ------------------------------------------------------------------

_TEMPLATE_DATA = {
    "default": [
        {
            "question": "A ball is thrown vertically upward. What is its velocity at the highest point?",
            "options": {"A": "Maximum", "B": "Zero", "C": "9.8 m/s", "D": "Depends on mass"},
            "correct_answer": "B",
            "explanation": "At the highest point, all kinetic energy has been converted to potential energy.",
        },
        {
            "question": "What is Newton's first law also known as?",
            "options": {"A": "Law of acceleration", "B": "Law of inertia", "C": "Law of gravity", "D": "Law of motion"},
            "correct_answer": "B",
            "explanation": "Newton's first law states that an object at rest stays at rest unless acted upon by an external force.",
        },
    ]
}


@pytest.fixture
def temp_templates(tmp_path):
    """Create a temporary templates directory with sample physics data.

    Returns the directory Path.
    """
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()

    physics_file = templates_dir / "physics.json"
    physics_file.write_text(json.dumps(_TEMPLATE_DATA, indent=2))

    return str(templates_dir)
