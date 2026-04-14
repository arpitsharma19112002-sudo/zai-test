"""Question rendering component for PDF."""

from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Spacer
from typing import List

from biopress.core.models import MCQItem


def render_question(
    question: MCQItem,
    question_number: int,
    question_style: ParagraphStyle,
    option_style: ParagraphStyle,
    option_spacing: float,
) -> List:
    """Render a single question with options."""
    elements = []
    
    q_text = f"<b>{question_number}.</b> {question.question}"
    q_para = Paragraph(q_text, question_style)
    elements.append(q_para)
    elements.append(Spacer(1, 6))
    
    options = [
        ("A", question.options.A),
        ("B", question.options.B),
        ("C", question.options.C),
        ("D", question.options.D),
    ]
    
    for label, text in options:
        opt_text = f"<b>{label}.</b> {text}"
        opt_para = Paragraph(opt_text, option_style)
        elements.append(opt_para)
        elements.append(Spacer(1, option_spacing))
    
    return elements
