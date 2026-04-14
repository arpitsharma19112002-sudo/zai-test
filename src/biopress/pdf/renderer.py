"""PDF renderer using ReportLab.

Supports single-column (default/NCERT) and multi-column (NEET 2-column)
layouts via ReportLab's Frame / PageTemplate system.
"""

from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageTemplate,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    PageBreak,
)
from typing import List, Optional

from biopress.core.models import PerseusQuiz
from biopress.pdf.styles.default import PDFStyle, DEFAULT
from biopress.pdf.styles.neet import NEET_2COLUMN
from biopress.pdf.styles.ncert import NCERT
from biopress.pdf.styles.bilingual import BILINGUAL
from biopress.pdf.styles.omr import OMR_READY
from biopress.pdf.components.question import render_question
from biopress.pdf.components.omr import render_omr_sheet
from biopress.pdf.review_section import ReviewSectionGenerator
from biopress.pdf.fonts import ensure_fonts_for_style
from biopress.pdf.utils.latex_renderer import LaTeXRenderer


STYLE_MAP = {
    "default": DEFAULT,
    "neet-2column": NEET_2COLUMN,
    "neet": NEET_2COLUMN,
    "ncert": NCERT,
    "bilingual": BILINGUAL,
    "omr-ready": OMR_READY,
    "omr": OMR_READY,
}


def get_pdf_style(style: str) -> PDFStyle:
    """Get PDF style by name."""
    return STYLE_MAP.get(style.lower(), DEFAULT)


class PDFRenderer:
    """PDF renderer using ReportLab."""
    
    def __init__(
        self,
        quiz: PerseusQuiz,
        style: str = "default",
        title: Optional[str] = None,
        subject: Optional[str] = None,
        exam_type: Optional[str] = None,
        include_review: bool = False,
        include_omr: bool = False,
    ):
        self.quiz = quiz
        self.style = get_pdf_style(style)
        self.title = title or "BioPress Quiz"
        self.subject = subject or ""
        self.exam_type = exam_type or ""
        self.include_review = include_review
        self.include_omr = include_omr or self._style_wants_omr()
        self._setup_styles()
        
        # Register any special fonts the style requires
        ensure_fonts_for_style(self.style)
        
        # Initialize LaTeX renderer
        self.latex_renderer = LaTeXRenderer()
    
    def _style_wants_omr(self) -> bool:
        """Check if the current style implies OMR sheet generation."""
        return hasattr(self.style, "omr_bubble_size")

    def _setup_styles(self) -> None:
        """Setup paragraph styles."""
        s = self.style
        self.styles = getSampleStyleSheet()
        
        self.title_style = ParagraphStyle(
            "Title",
            parent=self.styles["Title"],
            fontName=s.title_font,
            fontSize=s.title_size,
            spaceAfter=20,
            alignment=1,
        )
        
        self.heading_style = ParagraphStyle(
            "Heading",
            parent=self.styles["Heading1"],
            fontName=s.heading_font,
            fontSize=s.heading_size,
            spaceAfter=15,
            alignment=1,
        )
        
        self.body_style = ParagraphStyle(
            "Body",
            parent=self.styles["BodyText"],
            fontName=s.body_font,
            fontSize=s.body_size,
            leading=s.body_size * s.line_spacing,
            spaceAfter=10,
        )
        
        self.question_style = ParagraphStyle(
            "Question",
            fontName=s.body_font,
            fontSize=s.question_size,
            leading=s.question_size * s.line_spacing,
            spaceAfter=5,
        )
        
        self.option_style = ParagraphStyle(
            "Option",
            fontName=s.body_font,
            fontSize=s.option_size,
            leading=s.option_size * s.line_spacing,
            spaceAfter=3,
            leftIndent=20,
        )
    
    # ------------------------------------------------------------------
    # Story helpers
    # ------------------------------------------------------------------

    def _create_title_page(self, story: List) -> None:
        """Create title page."""
        story.append(Spacer(1, 2 * inch))
        story.append(Paragraph(self.title, self.title_style))
        
        if self.subject:
            story.append(Paragraph(f"Subject: {self.subject}", self.heading_style))
        
        if self.exam_type:
            story.append(Paragraph(f"Exam Type: {self.exam_type}", self.body_style))
        
        story.append(Spacer(1, 0.5 * inch))
        story.append(Paragraph(f"Total Questions: {len(self.quiz.items)}", self.body_style))
        story.append(PageBreak())
    
    def _create_questions(self, story: List) -> None:
        """Create questions pages."""
        story.append(Paragraph("Questions", self.heading_style))
        story.append(Spacer(1, 20))
        
        for i, item in enumerate(self.quiz.items, 1):
            question_elements = render_question(
                item,
                i,
                self.question_style,
                self.option_style,
                4,
                latex_renderer=self.latex_renderer,
            )
            story.extend(question_elements)
            story.append(Spacer(1, 15))

    def _append_review(self, story: List) -> None:
        """Append review / answer-key section."""
        review_style = ParagraphStyle(
            "Review",
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            spaceAfter=10,
        )
        story.append(PageBreak())
        review_text = ReviewSectionGenerator.generate()
        for line in review_text.split("\n"):
            story.append(Paragraph(line, review_style))

    def _append_omr(self, story: List) -> None:
        """Append a full OMR answer sheet."""
        story.append(PageBreak())
        omr_style = self.style if hasattr(self.style, "omr_bubble_size") else None
        omr_elements = render_omr_sheet(
            total_questions=len(self.quiz.items),
            style=omr_style,
            title="OMR Answer Sheet",
        )
        story.extend(omr_elements)

    # ------------------------------------------------------------------
    # Multi-column support
    # ------------------------------------------------------------------

    def _is_multicolumn(self) -> bool:
        """Return True if the current style requests columnar layout."""
        return getattr(self.style, "columns", 1) > 1

    def _build_multicolumn_doc(self, output_path: str, story: List) -> None:
        """Build a multi-column PDF using BaseDocTemplate + Frames."""
        s = self.style
        columns = getattr(s, "columns", 2)
        col_width = getattr(s, "column_width", 255)
        col_gap = getattr(s, "column_gap", 20)

        frames = []
        x = s.margin_left
        for _ in range(columns):
            frames.append(
                Frame(
                    x,
                    s.margin_bottom,
                    col_width,
                    s.page_height - s.margin_top - s.margin_bottom,
                    leftPadding=4,
                    rightPadding=4,
                    topPadding=6,
                    bottomPadding=6,
                )
            )
            x += col_width + col_gap

        page_template = PageTemplate(
            id="MultiCol",
            frames=frames,
            pagesize=(s.page_width, s.page_height),
        )

        doc = BaseDocTemplate(
            output_path,
            pagesize=(s.page_width, s.page_height),
            leftMargin=s.margin_left,
            rightMargin=s.margin_right,
            topMargin=s.margin_top,
            bottomMargin=s.margin_bottom,
        )
        doc.addPageTemplates([page_template])
        doc.build(story)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def render(self, output_path: str) -> None:
        """Render PDF to file."""
        s = self.style
        story: List = []
        
        self._create_title_page(story)
        self._create_questions(story)
        
        if self.include_review:
            self._append_review(story)

        if self.include_omr:
            self._append_omr(story)

        # Choose layout engine
        if self._is_multicolumn():
            self._build_multicolumn_doc(output_path, story)
        else:
            doc = SimpleDocTemplate(
                output_path,
                pagesize=(s.page_width, s.page_height),
                leftMargin=s.margin_left,
                rightMargin=s.margin_right,
                topMargin=s.margin_top,
                bottomMargin=s.margin_bottom,
            )
            doc.build(story)
