"""Assertion-Reason question generator."""

from biopress.core.models import AssertionReasonItem, AssertionReasonQuiz
from .base import BaseGenerator


class AssertionReasonGenerator(BaseGenerator[AssertionReasonQuiz, AssertionReasonItem]):
    """Generate assertion-reason questions in NEET format."""

    QUIZ_CLASS = AssertionReasonQuiz
    ITEM_CLASS = AssertionReasonItem

    def generate(
        self,
        exam: str,
        subject: str,
        count: int,
        topic: str,
    ) -> AssertionReasonQuiz:
        """Generate assertion-reason questions for the specified topic."""
        return super().generate(
            exam=exam,
            subject=subject,
            count=count,
            topic=topic,
            prefix="assertion_reason_",
            default_prefix="assertion_reason_"
        )
