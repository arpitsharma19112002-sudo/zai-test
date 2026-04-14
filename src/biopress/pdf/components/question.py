"""Question rendering component for PDF."""

from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Spacer, Image
from typing import List, Optional

from biopress.core.models import MCQItem


def render_question(
    question: MCQItem,
    question_number: int,
    question_style: ParagraphStyle,
    option_style: ParagraphStyle,
    option_spacing: float,
    latex_renderer = None,
) -> List:
    """Render a single question with options."""
    elements = []
    
    # Question text
    q_prefix = f"<b>{question_number}.</b> "
    if latex_renderer:
        # We need to handle the prefix separately if we want inline, 
        # but for now we prepend it to the first text part.
        q_elements = latex_renderer.process_text(f"{q_prefix}{question.question}", question_style)
        elements.extend(q_elements)
    else:
        q_text = f"{q_prefix}{question.question}"
        q_para = Paragraph(q_text, question_style)
        elements.append(q_para)
    
    elements.append(Spacer(1, 6))
    
    # Options
    options = [
        ("A", question.options.A),
        ("B", question.options.B),
        ("C", question.options.C),
        ("D", question.options.D),
    ]
    
    for label, text in options:
        opt_prefix = f"<b>{label}.</b> "
        if latex_renderer:
            opt_elements = latex_renderer.process_text(f"{opt_prefix}{text}", option_style)
            elements.extend(opt_elements)
        else:
            opt_text = f"{opt_prefix}{text}"
            opt_para = Paragraph(opt_text, option_style)
            elements.append(opt_para)
        
        elements.append(Spacer(1, option_spacing))
    
    return elements
