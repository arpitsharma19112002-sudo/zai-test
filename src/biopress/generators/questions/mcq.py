"""MCQ Generator module."""

from biopress.core.models import MCQItem, PerseusQuiz
from .base import BaseGenerator


class MCQGenerator(BaseGenerator[PerseusQuiz, MCQItem]):
    """Generate MCQ questions based on templates or LLM."""

    QUIZ_CLASS = PerseusQuiz
    ITEM_CLASS = MCQItem

    def generate(
        self,
        exam: str,
        subject: str,
        count: int,
        topic: str,
    ) -> PerseusQuiz:
        """Generate MCQ questions for the specified topic."""
        return super().generate(
            exam=exam,
            subject=subject,
            count=count,
            topic=topic,
            prefix="",
            default_prefix=""
        )