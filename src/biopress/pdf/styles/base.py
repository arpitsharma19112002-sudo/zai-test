"""Base PDF style for BioPress."""

from dataclasses import dataclass


@dataclass
class PDFStyle:
    """Base PDF style configuration."""
    title_font: str = "Helvetica-Bold"
    heading_font: str = "Helvetica-Bold"
    body_font: str = "Helvetica"
    title_size: int = 24
    heading_size: int = 18
    body_size: int = 12
    question_size: int = 12
    option_size: int = 11
    margin_top: float = 72
    margin_bottom: float = 72
    margin_left: float = 72
    margin_right: float = 72
    line_spacing: float = 1.5
    page_width: float = 595.28
    page_height: float = 841.89
