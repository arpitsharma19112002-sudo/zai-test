"""Font registration for BioPress PDF generation.

Handles registration of non-standard fonts (e.g. Devanagari) with ReportLab.
"""

import logging
from pathlib import Path
from typing import Optional

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

logger = logging.getLogger(__name__)

# Bundled font search paths (project-local, then system)
_FONT_SEARCH_PATHS = [
    Path(__file__).parent / "fonts",            # src/biopress/pdf/fonts/
    Path.home() / ".biopress" / "fonts",        # ~/.biopress/fonts/
    Path("/usr/share/fonts/truetype/noto"),      # Linux system
    Path("/Library/Fonts"),                       # macOS system
]

_registered: set[str] = set()


def _find_font_file(filename: str) -> Optional[Path]:
    """Search known paths for a font file."""
    for search_dir in _FONT_SEARCH_PATHS:
        candidate = search_dir / filename
        if candidate.is_file():
            return candidate
    return None


def register_devanagari(font_name: str = "NotoSansDevanagari") -> bool:
    """Register a Devanagari-capable TTF font with ReportLab.

    Searches for NotoSansDevanagari-Regular.ttf (and Bold variant)
    in the standard font search paths.

    Returns:
        True if at least the regular weight was registered, False otherwise.
    """
    if font_name in _registered:
        return True

    regular_file = _find_font_file(f"{font_name}-Regular.ttf")
    if regular_file is None:
        logger.warning(
            "Devanagari font '%s-Regular.ttf' not found in any search path. "
            "Hindi PDF export will fall back to Helvetica. "
            "Install via: pip install noto-fonts  OR  place the .ttf in ~/.biopress/fonts/",
            font_name,
        )
        return False

    try:
        pdfmetrics.registerFont(TTFont(font_name, str(regular_file)))
        _registered.add(font_name)
        logger.info("Registered font '%s' from %s", font_name, regular_file)
    except Exception as exc:
        logger.error("Failed to register '%s': %s", font_name, exc)
        return False

    # Attempt bold variant (non-fatal if missing)
    bold_file = _find_font_file(f"{font_name}-Bold.ttf")
    if bold_file:
        bold_name = f"{font_name}-Bold"
        try:
            pdfmetrics.registerFont(TTFont(bold_name, str(bold_file)))
            _registered.add(bold_name)
        except Exception:
            pass

    return True


def ensure_fonts_for_style(style) -> None:
    """Auto-register any special fonts required by a PDFStyle instance.

    Inspects the style for 'devanagari_font' attribute and registers it
    if present and not yet loaded.
    """
    devanagari = getattr(style, "devanagari_font", None)
    if devanagari and devanagari != "Helvetica":
        register_devanagari(devanagari)
