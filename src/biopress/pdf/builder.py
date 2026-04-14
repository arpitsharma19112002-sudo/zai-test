"""PDF builder - Main interface for PDF generation."""

import json
from typing import Optional, List, Dict, Any

from biopress.core.models import PerseusQuiz, MCQItem, MCQOptions
from biopress.pdf.renderer import PDFRenderer


def _normalize_item(item: Dict[str, Any]) -> MCQItem:
    """Normalize a quiz item to MCQItem format."""
    if isinstance(item, MCQItem):
        return item
    
    options = item.get("options")
    if isinstance(options, dict):
        options = MCQOptions(**options)
    elif isinstance(options, list):
        if len(options) >= 4:
            options = MCQOptions(A=options[0], B=options[1], C=options[2], D=options[3])
        else:
            options = MCQOptions(A="", B="", C="", D="")
    else:
        options = MCQOptions(A="", B="", C="", D="")
    
    return MCQItem(
        question=item.get("question", ""),
        options=options,
        correct_answer=item.get("correct_answer", ""),
        explanation=item.get("explanation", ""),
    )


class PDFBuilder:
    """Main PDF builder class."""

    def __init__(self, style: str = "default"):
        self.style = style

    @staticmethod
    def load_quiz(input_path: str) -> PerseusQuiz:
        """Load quiz from JSON file."""
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        if "items" in data:
            return PerseusQuiz(**data)
        elif isinstance(data, list):
            return PerseusQuiz(items=data)
        else:
            return PerseusQuiz(items=[data])

    def build_from_data(
        self,
        quiz_data: List[Dict[str, Any]],
        output_path: str,
        style: str = "default",
        title: Optional[str] = None,
        subject: Optional[str] = None,
        exam_type: Optional[str] = None,
        include_answers: bool = True,
    ) -> None:
        """Build PDF from quiz data dictionary."""
        normalized_items = [_normalize_item(item) for item in quiz_data]
        quiz = PerseusQuiz(items=normalized_items)
        
        renderer = PDFRenderer(
            quiz=quiz,
            style=style,
            title=title,
            subject=subject,
            exam_type=exam_type,
            include_review=include_answers,
        )
        
        renderer.render(output_path)

    @staticmethod
    def build(
        input_path: str,
        output_path: str,
        style: str = "default",
        title: Optional[str] = None,
        subject: Optional[str] = None,
        exam_type: Optional[str] = None,
        include_review: bool = False,
    ) -> None:
        """Build PDF from input JSON."""
        quiz = PDFBuilder.load_quiz(input_path)
        
        renderer = PDFRenderer(
            quiz=quiz,
            style=style,
            title=title,
            subject=subject,
            exam_type=exam_type,
            include_review=include_review,
        )
        
        renderer.render(output_path)
