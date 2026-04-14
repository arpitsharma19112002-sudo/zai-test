"""NCERT Textbook style PDF for BioPress."""

from dataclasses import dataclass
from biopress.pdf.styles.base import PDFStyle


@dataclass
class NCERTStyle(PDFStyle):
    """NCERT Textbook PDF style configuration."""
    title_font: str = "Times-Bold"
    heading_font: str = "Times-Bold"
    body_font: str = "Times-Roman"
    
    title_size: int = 22
    margin_top: float = 90
    line_spacing: float = 1.6
    
    devanagari_font: str = "Helvetica"
    chapter_summary_enabled: bool = True
    topic_headers_enabled: bool = True
    typography: str = "NCERT-standard"


NCERT = NCERTStyle()

def get_ncert_style() -> NCERTStyle:
    """Get NCERT style."""
    return NCERT