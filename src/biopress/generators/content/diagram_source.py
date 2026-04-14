"""Diagram sourcing from OER sources for BioPress."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from biopress.generators.content.diagram import Diagram


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

    BASE_URL = "https://openstax.atlassian.net/wiki/spaces/CORE"
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
        from biopress.generators.content.diagram import Diagram
        diagrams = []
        search_term = f"{topic} {subject}".lower()
        diagram = Diagram(
            topic=topic,
            subject=subject,
            source=self.name,
            url=f"{self.BASE_URL}/figures/{search_term.replace(' ', '_')}",
            description=f"OpenStax diagram for {topic}",
            alt_text=f"{topic} - {subject}",
        )
        diagrams.append(diagram)
        return diagrams


class LibreTextsSource(DiagramSource):
    """LibreTexts textbook diagrams."""

    BASE_URL = "https://chem.libretexts.org"
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
        from biopress.generators.content.diagram import Diagram
        diagrams = []
        search_term = f"{topic}".lower().replace(" ", "-")
        diagram = Diagram(
            topic=topic,
            subject=subject,
            source=self.name,
            url=f"{self.BASE_URL}/Bookshells/{search_term}",
            description=f"LibreTexts diagram for {topic}",
            alt_text=f"{topic} - {subject}",
        )
        diagrams.append(diagram)
        return diagrams


class HyperPhysicsSource(DiagramSource):
    """HyperPhysics physics diagrams."""

    BASE_URL = "http://hyperphysics.phy-astr.gsu.edu/hbase"
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
        from biopress.generators.content.diagram import Diagram
        if subject.lower() != "physics":
            return []
        diagrams = []
        search_term = f"{topic}".lower().replace(" ", "")
        diagram = Diagram(
            topic=topic,
            subject=subject,
            source=self.name,
            url=f"{self.BASE_URL}/{search_term[0]}/{search_term}.html",
            description=f"HyperPhysics diagram for {topic}",
            alt_text=f"{topic} - Physics",
        )
        diagrams.append(diagram)
        return diagrams


class ServierSource(DiagramSource):
    """Servier medical illustrations."""

    BASE_URL = "https://smart.servier.com"
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
        from biopress.generators.content.diagram import Diagram
        if subject.lower() not in ("biology", "chemistry", "medicine"):
            return []
        diagrams = []
        search_term = f"{topic}".lower().replace(" ", "-")
        diagram = Diagram(
            topic=topic,
            subject=subject,
            source=self.name,
            url=f"{self.BASE_URL}/search-by-term/{search_term}",
            description=f"Servier illustration for {topic}",
            alt_text=f"{topic} - {subject}",
        )
        diagrams.append(diagram)
        return diagrams


class BioiconsSource(DiagramSource):
    """Bioicons open source biology icons."""

    BASE_URL = "https://bioicons.com"
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
        from biopress.generators.content.diagram import Diagram
        if subject.lower() not in ("biology", "medicine"):
            return []
        diagrams = []
        search_term = f"{topic}".lower().replace(" ", "-")
        diagram = Diagram(
            topic=topic,
            subject=subject,
            source=self.name,
            url=f"{self.BASE_URL}/icons/{search_term}",
            description=f"Bioicons icon for {topic}",
            alt_text=f"{topic} - {subject}",
        )
        diagrams.append(diagram)
        return diagrams


class WikimediaSource(DiagramSource):
    """Wikimedia Commons diagrams."""

    BASE_URL = "https://commons.wikimedia.org/wiki"
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
        from biopress.generators.content.diagram import Diagram
        diagrams = []
        search_term = f"{topic}".lower().replace(" ", "_")
        diagram = Diagram(
            topic=topic,
            subject=subject,
            source=self.name,
            url=f"{self.BASE_URL}/File:{search_term}.svg",
            description=f"Wikimedia Commons diagram for {topic}",
            alt_text=f"{topic} - {subject}",
        )
        diagrams.append(diagram)
        return diagrams


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
