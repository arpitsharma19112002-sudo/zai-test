"""OMR (Optical Mark Recognition) bubble sheet rendering component.

Generates a scannable answer bubble grid using ReportLab canvas drawing
primitives. Intended for use as an appendix page in exam PDFs.
"""

from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Flowable, Paragraph, Spacer
from typing import List


class OMRBubbleRow(Flowable):
    """A single row of OMR bubbles for one question: (A) (B) (C) (D)."""

    def __init__(
        self,
        question_number: int,
        options: int = 4,
        bubble_radius: float = 4 * mm,
        bubble_spacing: float = 8 * mm,
        font_name: str = "Helvetica",
        font_size: int = 8,
    ):
        super().__init__()
        self.question_number = question_number
        self.options = options
        self.bubble_radius = bubble_radius
        self.bubble_spacing = bubble_spacing
        self.font_name = font_name
        self.font_size = font_size

        # Flowable dimensions
        self.width = (
            30 * mm  # question number column
            + options * (2 * bubble_radius + bubble_spacing)
        )
        self.height = 2 * bubble_radius + 2 * mm

    def draw(self):
        c = self.canv
        r = self.bubble_radius
        y_center = self.height / 2

        # Question number label
        c.setFont(self.font_name, self.font_size)
        c.drawRightString(25 * mm, y_center - self.font_size / 3, f"{self.question_number}.")

        # Bubble circles
        option_labels = "ABCDEFGH"[: self.options]
        x = 30 * mm + r
        for label in option_labels:
            c.circle(x, y_center, r, stroke=1, fill=0)
            c.setFont(self.font_name, self.font_size - 1)
            c.drawCentredString(x, y_center - (self.font_size - 1) / 3, label)
            x += 2 * r + self.bubble_spacing


def render_omr_sheet(
    total_questions: int,
    style=None,
    title: str = "OMR Answer Sheet",
) -> List:
    """Generate a list of ReportLab Flowables representing a full OMR sheet.

    Args:
        total_questions: Number of questions to create bubble rows for.
        style: An OMRReadyStyle instance (or None for defaults).
        title: Sheet header title.

    Returns:
        List of Flowable objects to be appended to a PDF story.
    """
    bubble_radius = 4 * mm
    bubble_spacing = 6 * mm
    font_name = "Helvetica"

    if style is not None:
        bubble_radius = getattr(style, "omr_bubble_size", 14) / 2 * mm / 3.5
        bubble_spacing = getattr(style, "omr_bubble_spacing", 18) / 2 * mm / 3.5
        font_name = getattr(style, "omr_font", font_name)

    header_style = ParagraphStyle(
        "OMRHeader",
        fontName="Helvetica-Bold",
        fontSize=16,
        spaceAfter=12,
        alignment=1,
    )
    instructions_style = ParagraphStyle(
        "OMRInstructions",
        fontName="Helvetica",
        fontSize=9,
        spaceAfter=8,
        leading=12,
    )

    elements: List = []
    elements.append(Paragraph(title, header_style))
    elements.append(
        Paragraph(
            "Instructions: Darken the bubble corresponding to your answer "
            "completely using a dark pencil. Do not use ink or ball-point pen.",
            instructions_style,
        )
    )

    timing = ""
    if style is not None:
        timing = getattr(style, "timing_instructions", "")
    if timing:
        elements.append(Paragraph(f"<b>{timing}</b>", instructions_style))

    elements.append(Spacer(1, 10))

    # Student info fields
    elements.append(
        Paragraph(
            "Name: ________________________  "
            "Roll No: ______________  "
            "Date: __________",
            instructions_style,
        )
    )
    elements.append(Spacer(1, 14))

    # Bubble rows
    for q in range(1, total_questions + 1):
        elements.append(
            OMRBubbleRow(
                question_number=q,
                options=4,
                bubble_radius=bubble_radius,
                bubble_spacing=bubble_spacing,
                font_name=font_name,
            )
        )

    return elements
