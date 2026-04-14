"""Utility for rendering LaTeX math to ReportLab-compatible images."""

import io
import os
import re
import tempfile
from typing import List, Union

import matplotlib
matplotlib.use("Agg")  # Use non-interactive backend
import matplotlib.pyplot as plt
from reportlab.platypus import Image, Flowable, Paragraph
from reportlab.lib.styles import ParagraphStyle


class LaTeXRenderer:
    """Renderer for LaTeX math using matplotlib."""

    def __init__(self, dpi: int = 300, fontsize: int = 12):
        self.dpi = dpi
        self.fontsize = fontsize
        self.temp_dir = tempfile.mkdtemp(prefix="biopress_latex_")

    def render_to_file(self, latex: str) -> str:
        """Render a LaTeX string to a temporary image file and return the path."""
        # Clean the latex string (ensure it has delimiters for matplotlib)
        if not latex.startswith("$"):
            latex = f"${latex}$"

        # Create figure and axis
        fig = plt.figure(figsize=(0.1, 0.1))  # Size will be adjusted
        fig.text(0, 0, latex, fontsize=self.fontsize)

        # Save to buffer to calculate bbox
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=self.dpi, bbox_inches="tight", pad_inches=0.05, transparent=True)
        plt.close(fig)

        # Save to real temp file
        filename = f"math_{hash(latex)}.png"
        filepath = os.path.join(self.temp_dir, filename)
        
        with open(filepath, "wb") as f:
            f.write(buf.getvalue())
        
        return filepath

    def process_text(self, text: str, style: ParagraphStyle) -> List[Union[Paragraph, Image]]:
        """Process text containing LaTeX and return a list of Flowables."""
        # Match $...$ or $$...$$
        pattern = r"(\$\$.*?\$\$|\$.*?\$)"
        parts = re.split(pattern, text)
        
        elements = []
        current_text = ""
        
        for part in parts:
            if part.startswith("$"):
                # If we have accumulated text, append it as a Paragraph
                if current_text:
                    elements.append(Paragraph(current_text, style))
                    current_text = ""
                
                # Render the LaTeX
                try:
                    img_path = self.render_to_file(part)
                    # Use a small height to keep it roughly inline (this is a limitation of Flowables)
                    # For true inline, we'd need to use a custom Flowable or complex Paragraph tags.
                    # Here we append as a block image for now, or use a tiny Spacer.
                    img = Image(img_path)
                    
                    # Estimate width/height based on DPI
                    # This is simple for now
                    elements.append(img)
                except Exception as e:
                    # Fallback to raw text if rendering fails
                    current_text += f" {part} "
            else:
                current_text += part
        
        if current_text:
            elements.append(Paragraph(current_text, style))
            
        return elements

    def __del__(self):
        """Cleanup temporary files."""
        try:
            import shutil
            if hasattr(self, "temp_dir") and os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
        except Exception:
            pass
