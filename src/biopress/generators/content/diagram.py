"""Diagram verification and management for BioPress."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from biopress.generators.content.diagram_source import DiagramSource


class DiagramStatus(str, Enum):
    """Status of a diagram in verification workflow."""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    REFINED = "refined"


@dataclass
class Diagram:
    """Diagram data model."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    topic: str = ""
    subject: str = ""
    source: str = ""
    url: str = ""
    description: str = ""
    alt_text: str = ""
    status: DiagramStatus = DiagramStatus.PENDING
    rejection_reason: Optional[str] = None
    search_attempts: int = 0


class DiagramVerifier:
    """Smart diagram verification workflow for BioPress Designer."""

    def __init__(self):
        self.diagrams: list[Diagram] = []
        self.approved: list[Diagram] = []
        self.rejected: list[Diagram] = []
        self._sources: list[DiagramSource] = []

    def add_source(self, source: DiagramSource) -> None:
        """Add a diagram source."""
        self._sources.append(source)

    def add_diagram(self, diagram: Diagram) -> None:
        """Add diagram to verification queue."""
        self.diagrams.append(diagram)

    def preview_all(self) -> list[Diagram]:
        """Stage 2: Preview all diagrams."""
        return self.diagrams.copy()

    def get_diagram_by_id(self, diagram_id: str) -> Optional[Diagram]:
        """Find diagram by ID."""
        for diag in self.diagrams:
            if diag.id == diagram_id:
                return diag
        return None

    def approve(self, diagram_id: str) -> None:
        """Stage 3: Approve a diagram."""
        diagram = self.get_diagram_by_id(diagram_id)
        if diagram:
            diagram.status = DiagramStatus.APPROVED
            if diagram not in self.approved:
                self.approved.append(diagram)
            if diagram in self.rejected:
                self.rejected.remove(diagram)

    def reject(self, diagram_id: str, reason: str) -> None:
        """Stage 3: Reject a diagram."""
        diagram = self.get_diagram_by_id(diagram_id)
        if diagram:
            diagram.status = DiagramStatus.REJECTED
            diagram.rejection_reason = reason
            if diagram not in self.rejected:
                self.rejected.append(diagram)
            if diagram in self.approved:
                self.approved.remove(diagram)

    def refine_rejected(self) -> list[Diagram]:
        """Stage 4: Re-process rejected diagrams."""
        refined_diagrams = []
        for diagram in self.rejected:
            diagram.search_attempts += 1
            new_diagram = self._search_new_diagram(diagram)
            if new_diagram:
                self.diagrams.remove(diagram)
                self.diagrams.append(new_diagram)
                refined_diagrams.append(new_diagram)
                diagram.status = DiagramStatus.REFINED
        self.rejected.clear()
        return refined_diagrams

    def _search_new_diagram(self, diagram: Diagram) -> Optional[Diagram]:
        """Search for a new diagram from available sources."""
        for source in self._sources:
            results = source.search(diagram.topic, diagram.subject)
            if results:
                new_diag = results[0]
                new_diag.search_attempts = diagram.search_attempts
                return new_diag
        return None

    def is_ready_for_pdf(self) -> bool:
        """Stage 5: Check if all diagrams approved."""
        if not self.diagrams:
            return True
        return all(d.status == DiagramStatus.APPROVED for d in self.diagrams)

    def get_status_summary(self) -> dict[str, int]:
        """Get count of diagrams by status."""
        return {
            "pending": sum(1 for d in self.diagrams if d.status == DiagramStatus.PENDING),
            "approved": len(self.approved),
            "rejected": len(self.rejected),
        }
