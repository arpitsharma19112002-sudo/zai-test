"""Bilingual PDF style for BioPress (Hindi/English)."""

from dataclasses import dataclass
from biopress.pdf.styles.base import PDFStyle


@dataclass
class BilingualStyle(PDFStyle):
    """Bilingual PDF style configuration."""
    title_size: int = 20
    heading_size: int = 16
    body_size: int = 11
    question_size: int = 11
    option_size: int = 10
    margin_left: float = 54
    margin_right: float = 54
    
    devanagari_font: str = "NotoSansDevanagari"
    layout_mode: str = "sequential"
    column_width: float = 240
    language_separator: str = " | "


BILINGUAL = BilingualStyle()

def get_bilingual_style() -> BilingualStyle:
    """Get bilingual style."""
    return BILINGUAL