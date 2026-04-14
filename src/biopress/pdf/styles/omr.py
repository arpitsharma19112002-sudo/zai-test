"""OMR-Ready PDF style for BioPress."""

from dataclasses import dataclass
from biopress.pdf.styles.base import PDFStyle


@dataclass
class OMRReadyStyle(PDFStyle):
    """OMR-Ready PDF style configuration."""
    title_size: int = 18
    heading_size: int = 14
    body_size: int = 10
    question_size: int = 10
    option_size: int = 9
    margin_left: float = 54
    margin_right: float = 54
    line_spacing: float = 1.4
    
    omr_bubble_size: float = 14
    omr_bubble_spacing: float = 18
    id_alignment_enabled: bool = True
    answer_key_page_enabled: bool = True
    timing_instructions: str = "Time: 3 hours | Max Marks: 720"


OMR_READY = OMRReadyStyle()

def get_omr_style() -> OMRReadyStyle:
    """Get OMR-ready style."""
    return OMR_READY