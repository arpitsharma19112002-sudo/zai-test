"""PDF styles package."""

from biopress.pdf.styles.default import PDFStyle, get_style, DEFAULT, NEET
from biopress.pdf.styles.ncert import get_ncert_style
from biopress.pdf.styles.bilingual import get_bilingual_style, BILINGUAL
from biopress.pdf.styles.omr import get_omr_style, OMR_READY

__all__ = [
    "PDFStyle",
    "get_style",
    "DEFAULT",
    "NEET",
    "get_ncert_style",
    "get_bilingual_style",
    "BILINGUAL",
    "get_omr_style",
    "OMR_READY",
]