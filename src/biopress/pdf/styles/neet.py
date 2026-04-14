"""NEET 2-Column PDF style for BioPress."""

from dataclasses import dataclass
from biopress.pdf.styles.base import PDFStyle


@dataclass
class NEET2ColumnStyle(PDFStyle):
    """NEET 2-Column PDF style configuration."""
    title_size: int = 20
    heading_size: int = 14
    body_size: int = 10
    question_size: int = 10
    option_size: int = 9
    margin_bottom: float = 54
    margin_left: float = 36
    margin_right: float = 36
    line_spacing: float = 1.3
    
    columns: int = 2
    column_width: float = 255
    column_gap: float = 20
    question_number_font: str = "Helvetica-Bold"
    question_number_size: int = 10
    omr_bubble_size: float = 12
    omr_font: str = "Helvetica"
    header_font: str = "Helvetica-Bold"
    header_size: int = 11


NEET_2COLUMN = NEET2ColumnStyle()

def get_neet_style() -> NEET2ColumnStyle:
    """Get NEET 2-column style."""
    return NEET_2COLUMN