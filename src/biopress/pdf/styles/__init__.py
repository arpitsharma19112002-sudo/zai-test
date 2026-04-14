"""PDF styles package."""

from biopress.pdf.styles.default import PDFStyle, get_style, DEFAULT
from biopress.pdf.styles.neet import NEET_2COLUMN
from biopress.pdf.styles.ncert import NCERT
from biopress.pdf.styles.bilingual import BILINGUAL
from biopress.pdf.styles.omr import OMR_READY

__all__ = [
    "PDFStyle",
    "get_style",
    "DEFAULT",
    "NEET_2COLUMN",
    "NCERT",
    "BILINGUAL",
    "OMR_READY",
]