"""Default PDF styles for BioPress."""

from biopress.pdf.styles.base import PDFStyle

DEFAULT = PDFStyle()

def get_style(name: str) -> PDFStyle:
    """Get style by name."""
    from biopress.pdf.styles.neet import NEET_2COLUMN
    from biopress.pdf.styles.ncert import NCERT
    from biopress.pdf.styles.bilingual import BILINGUAL
    from biopress.pdf.styles.omr import OMR_READY

    styles = {
        "default": DEFAULT,
        "neet": NEET_2COLUMN,
        "ncert": NCERT,
        "bilingual": BILINGUAL,
        "omr": OMR_READY,
    }
    
    return styles.get(name.lower(), DEFAULT)
