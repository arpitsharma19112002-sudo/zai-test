"""Diagram sourcing from OER sources for BioPress."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
import os
import logging
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from biopress.generators.content.diagram import Diagram

logger = logging.getLogger(__name__)


class LicenseType(str, Enum):
    """License types for OER diagram sources."""
    CC_BY = "CC BY"
    CC_BY_SA = "CC BY-SA"
    CC_BY_NC = "CC BY-NC"
    CC_BY_NC_SA = "CC BY-NC-SA"
    CC_BY_ND = "CC BY-ND"
    CC_BY_NC_ND = "CC BY-NC-ND"
    CC0 = "CC0"
    GPL = "GPL"
    MIT = "MIT"
    Apache = "Apache-2.0"
    ODBL = "ODbL"
    UNKNOWN = "Unknown"


@dataclass
class License:
    """License information for a diagram."""
    license_type: LicenseType = LicenseType.UNKNOWN
    attribution_required: bool = True
    commercial_use_allowed: bool = True
    modifications_allowed: bool = True
    share_alike_required: bool = False
    source_url: str = ""
    license_text: str = ""


class DiagramSource(ABC):
    """Abstract base class for diagram sources."""

    def __init__(self, name: str, license_info: Optional[License] = None):
        self.name = name
        self.license_info = license_info or License()

    @abstractmethod
    def search(self, topic: str, subject: str) -> list[Diagram]:
        """Search for diagrams matching topic and subject."""
        pass

    def _create_local_diagram(self, topic: str, subject: str, ext: str = "png") -> list[Diagram]:
        from biopress.generators.content.diagram import Diagram
        
        search_term = topic.lower().replace(" ", "_")
        local_path = f"assets/diagrams/{self.name}/{search_term}.{ext}"
        
        if not os.path.exists(local_path):
            logger.warning(
                f"\n[DOWNLOAD REQUIRED] Missing visual asset for {self.name}: '{topic}'\n"
                f"Please manually download a suitable diagram and save it to:\n"
                f"  -> {os.path.abspath(local_path)}\n"
            )
            
        diagram = Diagram(
            topic=topic,
            subject=subject,
            source=self.name,
            url=local_path,
            description=f"{self.name} diagram for {topic}",
            alt_text=f"{topic} - {subject}",
        )
        return [diagram]

    def verify_license(self, diagram: "Diagram") -> tuple[bool, str]:
        """Verify if diagram can be used under license."""
        from biopress.generators.content.license_checker import LicenseChecker
        
        checker = LicenseChecker()
        return checker.verify_diagram_license(diagram)

    def get_source_license(self) -> License:
        """Get license information for this source."""
        return self.license_info


class OpenStaxSource(DiagramSource):
    """OpenStax textbook diagrams."""

    LICENSE = License(
        license_type=LicenseType.CC_BY,
        attribution_required=True,
        commercial_use_allowed=True,
        modifications_allowed=True,
    )

    def __init__(self):
        super().__init__("OpenStax", self.LICENSE)

    def search(self, topic: str, subject: str) -> list[Diagram]:
        """Search OpenStax for diagrams."""
        return self._create_local_diagram(topic, subject)


class LibreTextsSource(DiagramSource):
    """LibreTexts textbook diagrams."""

    LICENSE = License(
        license_type=LicenseType.CC_BY,
        attribution_required=True,
        commercial_use_allowed=True,
        modifications_allowed=True,
    )

    def __init__(self):
        super().__init__("LibreTexts", self.LICENSE)

    def search(self, topic: str, subject: str) -> list[Diagram]:
        """Search LibreTexts for diagrams."""
        return self._create_local_diagram(topic, subject)


class HyperPhysicsSource(DiagramSource):
    """HyperPhysics physics diagrams."""

    LICENSE = License(
        license_type=LicenseType.CC_BY_NC_SA,
        attribution_required=True,
        commercial_use_allowed=False,
        modifications_allowed=True,
        share_alike_required=True,
    )

    def __init__(self):
        super().__init__("HyperPhysics", self.LICENSE)

    def search(self, topic: str, subject: str) -> list[Diagram]:
        """Search HyperPhysics for diagrams."""
        if subject.lower() != "physics":
            return []
        return self._create_local_diagram(topic, subject)


class ServierSource(DiagramSource):
    """Servier medical illustrations."""

    LICENSE = License(
        license_type=LicenseType.CC_BY,
        attribution_required=True,
        commercial_use_allowed=True,
        modifications_allowed=True,
    )

    def __init__(self):
        super().__init__("Servier", self.LICENSE)

    def search(self, topic: str, subject: str) -> list[Diagram]:
        """Search Servier for diagrams."""
        if subject.lower() not in ("biology", "chemistry", "medicine"):
            return []
        return self._create_local_diagram(topic, subject)


class BioiconsSource(DiagramSource):
    """Bioicons open source biology icons."""

    LICENSE = License(
        license_type=LicenseType.CC_BY,
        attribution_required=True,
        commercial_use_allowed=True,
        modifications_allowed=True,
    )

    def __init__(self):
        super().__init__("Bioicons", self.LICENSE)

    def search(self, topic: str, subject: str) -> list[Diagram]:
        """Search Bioicons for diagrams."""
        if subject.lower() not in ("biology", "medicine"):
            return []
        return self._create_local_diagram(topic, subject, ext="svg")


class WikimediaSource(DiagramSource):
    """Wikimedia Commons diagrams."""

    LICENSE = License(
        license_type=LicenseType.CC_BY_SA,
        attribution_required=True,
        commercial_use_allowed=True,
        modifications_allowed=True,
        share_alike_required=True,
    )

    def __init__(self):
        super().__init__("Wikimedia", self.LICENSE)

    def search(self, topic: str, subject: str) -> list[Diagram]:
        """Search Wikimedia for diagrams."""
        return self._create_local_diagram(topic, subject, ext="svg")


def get_default_sources() -> list[DiagramSource]:
    """Get all default diagram sources."""
    return [
        OpenStaxSource(),
        LibreTextsSource(),
        HyperPhysicsSource(),
        ServierSource(),
        BioiconsSource(),
        WikimediaSource(),
    ]
