"""Numerical question generator."""

from biopress.core.models import NumericalItem, NumericalQuiz
from .base import BaseGenerator


class NumericalGenerator(BaseGenerator[NumericalQuiz, NumericalItem]):
    """Generate numerical questions with step-by-step solutions."""

    QUIZ_CLASS = NumericalQuiz
    ITEM_CLASS = NumericalItem

    def generate(
        self,
        exam: str,
        subject: str,
        count: int,
        topic: str,
    ) -> NumericalQuiz:
        """Generate numerical questions for the specified topic."""
        return super().generate(
            exam=exam,
            subject=subject,
            count=count,
            topic=topic,
            prefix="numerical_",
            default_prefix="numerical_"
        )
