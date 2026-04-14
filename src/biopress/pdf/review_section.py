"""Editorial review section generator for PDF."""

from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class QualityScore:
    """Quality score for a validation level."""
    level: str
    status: str
    percentage: float


@dataclass
class ReviewMetadata:
    """Metadata for editorial review section."""
    sources: List[str]
    image_attributions: List[str]
    quality_scores: List[QualityScore]
    generated_at: datetime
    pipeline_version: str
    additional_notes: Optional[List[str]] = None


class ReviewSectionGenerator:
    """Generates editorial review section for PDFs."""
    
    @staticmethod
    def generate(
        sources: Optional[List[str]] = None,
        image_attributions: Optional[List[str]] = None,
        quality_scores: Optional[List[Dict[str, Any]]] = None,
        pipeline_version: str = "BioPress v0.1.0",
    ) -> str:
        """Generate editorial review section text."""
        sources = sources or []
        image_attributions = image_attributions or []
        quality_scores = quality_scores or []
        
        lines = []
        lines.append("═" * 45)
        lines.append("EDITORIAL REVIEW & SOURCES")
        lines.append("═" * 45)
        lines.append("")
        
        if sources:
            lines.append("Sources:")
            for source in sources:
                lines.append(f"- {source}")
            lines.append("")
        
        if image_attributions:
            lines.append("Image Attributions:")
            for attr in image_attributions:
                lines.append(f"- {attr}")
            lines.append("")
        
        if quality_scores:
            lines.append("Quality Scores:")
            for qs in quality_scores:
                level = qs.get("level", "Unknown").replace(" Validation", "")
                status = qs.get("status", "PENDING")
                percentage = qs.get("percentage", 0.0)
                lines.append(f"- {level} Validation: {status} ({percentage}%)")
            lines.append("")
        
        lines.append(f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}")
        lines.append(f"Pipeline: {pipeline_version}")
        
        return "\n".join(lines)
    
    @staticmethod
    def create_metadata(
        sources: Optional[List[str]] = None,
        image_attributions: Optional[List[str]] = None,
        quality_scores: Optional[List[Dict[str, Any]]] = None,
        pipeline_version: str = "BioPress v0.1.0",
    ) -> ReviewMetadata:
        """Create review metadata object."""
        q_scores = []
        if quality_scores:
            for qs in quality_scores:
                q_scores.append(QualityScore(
                    level=qs.get("level", "Unknown"),
                    status=qs.get("status", "PENDING"),
                    percentage=qs.get("percentage", 0.0),
                ))
        
        return ReviewMetadata(
            sources=sources or [],
            image_attributions=image_attributions or [],
            quality_scores=q_scores,
            generated_at=datetime.now(timezone.utc),
            pipeline_version=pipeline_version,
        )
    
    @staticmethod
    def format_for_pdf() -> str:
        """Format review section for PDF rendering."""
        return ReviewSectionGenerator.generate()


def generate_review_section(
    sources: Optional[List[str]] = None,
    image_attributions: Optional[List[str]] = None,
    quality_scores: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """Convenience function to generate review section."""
    return ReviewSectionGenerator.generate(
        sources=sources,
        image_attributions=image_attributions,
        quality_scores=quality_scores,
    )