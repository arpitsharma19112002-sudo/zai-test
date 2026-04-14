"""Style creation system from natural language descriptions."""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class StyleLayout:
    """Layout configuration for PDF style."""
    name: str
    description: str
    columns: int
    question_layout: str
    omr_bubbles: bool
    font_family: str
    font_sizes: Dict[str, int]
    margins: Dict[str, float]
    headers: Dict[str, Any]
    special_features: list[str]


class StyleSystem:
    """System for creating PDF styles from natural language."""
    
    LAYOUTS_DIR = Path(__file__).parent.parent.parent / "kb" / "layouts"
    
    def __init__(self):
        self.LAYOUTS_DIR.mkdir(parents=True, exist_ok=True)
    
    def create_style(
        self,
        description: str,
        name: Optional[str] = None,
    ) -> StyleLayout:
        """Create a style layout from natural language description."""
        layout = self._parse_description(description)
        
        if name:
            layout.name = name
        
        return layout
    
    def _parse_description(self, description: str) -> StyleLayout:
        """Parse natural language description into style layout."""
        desc_lower = description.lower()
        
        columns = 1
        if "2-column" in desc_lower or "two column" in desc_lower or "2 column" in desc_lower:
            columns = 2
        elif "3-column" in desc_lower or "three column" in desc_lower or "3 column" in desc_lower:
            columns = 3
        
        omr_bubbles = "omr" in desc_lower or "bubble" in desc_lower or "exam" in desc_lower
        
        question_layout = "vertical"
        if columns > 1:
            question_layout = "grid"
        
        font_family = "Helvetica"
        if "ncert" in desc_lower or "textbook" in desc_lower:
            font_family = "Times"
        elif "bilingual" in desc_lower or "hindi" in desc_lower:
            font_family = "Helvetica"
        
        font_sizes = {
            "title": 20,
            "heading": 16,
            "body": 12,
            "question": 12,
            "option": 11,
        }
        
        if "neet" in desc_lower or "exam" in desc_lower:
            font_sizes = {
                "title": 18,
                "heading": 14,
                "body": 10,
                "question": 10,
                "option": 9,
            }
        
        margins = {
            "top": 72.0,
            "bottom": 72.0,
            "left": 72.0,
            "right": 72.0,
        }
        
        if columns > 1:
            margins = {
                "top": 72.0,
                "bottom": 54.0,
                "left": 36.0,
                "right": 36.0,
            }
        
        headers = {
            "exam_name": "include" if "exam" in desc_lower else "exclude",
            "date": "include" if "exam" in desc_lower else "exclude",
            "subject": "include" if "subject" in desc_lower else "exclude",
        }
        
        special_features = []
        if "bilingual" in desc_lower or "hindi" in desc_lower:
            special_features.append("devanagari_font")
        if "ncert" in desc_lower or "textbook" in desc_lower:
            special_features.append("chapter_summary")
            special_features.append("topic_headers")
        if "omr" in desc_lower:
            special_features.append("answer_key_page")
            special_features.append("id_alignment")
        
        return StyleLayout(
            name="custom",
            description=description,
            columns=columns,
            question_layout=question_layout,
            omr_bubbles=omr_bubbles,
            font_family=font_family,
            font_sizes=font_sizes,
            margins=margins,
            headers=headers,
            special_features=special_features,
        )
    
    def save_layout(self, layout: StyleLayout, filename: Optional[str] = None) -> Path:
        """Save style layout to JSON file."""
        if filename is None:
            safe_name = layout.name.replace(" ", "_").lower()
            filename = f"{safe_name}_layout.json"
        
        filepath = self.LAYOUTS_DIR / filename
        
        layout_dict = asdict(layout)
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(layout_dict, f, indent=2)
        
        return filepath
    
    def load_layout(self, filename: str) -> StyleLayout:
        """Load style layout from JSON file."""
        filepath = self.LAYOUTS_DIR / filename
        
        with open(filepath, "r", encoding="utf-8") as f:
            layout_dict = json.load(f)
        
        return StyleLayout(**layout_dict)
    
    def list_layouts(self) -> list[str]:
        """List all saved style layouts."""
        return [f.name for f in self.LAYOUTS_DIR.glob("*_layout.json")]


def create_style_from_description(description: str, name: Optional[str] = None) -> StyleLayout:
    """Convenience function to create style from description."""
    system = StyleSystem()
    return system.create_style(description, name)


def save_style_layout(layout: StyleLayout, filename: Optional[str] = None) -> Path:
    """Convenience function to save style layout."""
    system = StyleSystem()
    return system.save_layout(layout, filename)