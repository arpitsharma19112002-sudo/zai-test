"""Case-based question generator."""

from typing import Any, Optional
from biopress.core.models import CaseBasedItem, CaseBasedQuiz
from .base import BaseGenerator


class CaseBasedGenerator(BaseGenerator[CaseBasedQuiz, CaseBasedItem]):
    """Generate case-based questions with passage and sub-questions."""

    QUIZ_CLASS = CaseBasedQuiz
    ITEM_CLASS = CaseBasedItem

    def _parse_item(self, item: dict[str, Any]) -> Optional[CaseBasedItem]:
        """Override parse logic for CaseBased item structure."""
        try:
            # Need to convert dictionary of questions into just list of dicts with question/answer
            sub_questions = []
            if "questions" in item:
                for sq in item["questions"]:
                    if isinstance(sq, dict) and "question" in sq and "answer" in sq:
                        sub_questions.append({"question": sq["question"], "answer": sq["answer"]})
            
            # Allow fallback if standard Pydantic validation handles it directly
            if not sub_questions and "questions" in item:
                sub_questions = item["questions"]
                
            return CaseBasedItem(
                passage=item["passage"],
                questions=sub_questions
            )
        except Exception as e:
            return super()._parse_item(item)

    def generate(
        self,
        exam: str,
        subject: str,
        count: int,
        topic: str,
    ) -> CaseBasedQuiz:
        """Generate case-based questions for the specified topic."""
        return super().generate(
            exam=exam,
            subject=subject,
            count=count,
            topic=topic,
            prefix="case_based_",
            default_prefix="case_based_"
        )
