"""License checking and compliance for diagram sources."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from biopress.generators.content.diagram import Diagram

from biopress.generators.content.diagram_source import (
    LicenseType,
)


class ComplianceStatus(str, Enum):
    """Compliance status for diagram license."""
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    REVIEW_REQUIRED = "review_required"
    UNKNOWN = "unknown"


@dataclass
class ComplianceResult:
    """Result of license compliance check."""
    diagram_id: str
    status: ComplianceStatus
    license_type: LicenseType
    is_commercial_use_allowed: bool
    is_modification_allowed: bool
    attribution_required: bool
    issues: list[str]
    checked_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class ComplianceReport:
    """Overall compliance report for multiple diagrams."""
    total_diagrams: int = 0
    compliant: int = 0
    non_compliant: int = 0
    review_required: int = 0
    unknown: int = 0
    results: list[ComplianceResult] = field(default_factory=list)
    generated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class LicenseChecker:
    """Verify diagram licenses and generate compliance reports."""

    SOURCE_LICENSES = {
        "OpenStax": LicenseType.CC_BY,
        "LibreTexts": LicenseType.CC_BY,
        "HyperPhysics": LicenseType.CC_BY_NC_SA,
        "Servier": LicenseType.CC_BY,
        "Bioicons": LicenseType.CC_BY,
        "Wikimedia": LicenseType.CC_BY_SA,
    }

    def __init__(self):
        self._checked_diagrams: dict[str, ComplianceResult] = {}

    def verify_diagram_license(self, diagram: "Diagram") -> tuple[bool, str]:
        """Verify if a single diagram can be used."""
        result = self.check_diagram(diagram)
        self._checked_diagrams[diagram.id] = result

        if result.status == ComplianceStatus.COMPLIANT:
            return True, "License compliant"
        elif result.status == ComplianceStatus.NON_COMPLIANT:
            return False, f"Non-compliant: {'; '.join(result.issues)}"
        else:
            return False, f"Review required: {'; '.join(result.issues)}"

    def check_diagram(self, diagram: "Diagram") -> ComplianceResult:
        """Check license compliance for a diagram."""
        issues = []
        license_type = self.SOURCE_LICENSES.get(diagram.source, LicenseType.UNKNOWN)

        is_commercial_allowed = True
        is_modification_allowed = True
        attribution_required = True

        if license_type in (
            LicenseType.CC_BY_NC,
            LicenseType.CC_BY_NC_SA,
            LicenseType.CC_BY_NC_ND,
        ):
            is_commercial_allowed = False
            issues.append("Non-commercial use only")

        if license_type == LicenseType.CC_BY_ND:
            is_modification_allowed = False
            issues.append("No derivatives allowed")

        if license_type == LicenseType.UNKNOWN:
            issues.append("Unknown license type")
            status = ComplianceStatus.UNKNOWN
        elif issues:
            status = ComplianceStatus.REVIEW_REQUIRED
        else:
            status = ComplianceStatus.COMPLIANT

        return ComplianceResult(
            diagram_id=diagram.id,
            status=status,
            license_type=license_type,
            is_commercial_use_allowed=is_commercial_allowed,
            is_modification_allowed=is_modification_allowed,
            attribution_required=attribution_required,
            issues=issues,
        )

    def generate_report(self, diagrams: list["Diagram"]) -> ComplianceReport:
        """Generate compliance report for multiple diagrams."""
        report = ComplianceReport(total_diagrams=len(diagrams))

        for diagram in diagrams:
            result = self.check_diagram(diagram)
            report.results.append(result)

            if result.status == ComplianceStatus.COMPLIANT:
                report.compliant += 1
            elif result.status == ComplianceStatus.NON_COMPLIANT:
                report.non_compliant += 1
            elif result.status == ComplianceStatus.REVIEW_REQUIRED:
                report.review_required += 1
            else:
                report.unknown += 1

        return report

    def to_json(self, report: ComplianceReport, output_path: Optional[str] = None) -> str:
        """Export compliance report as JSON."""
        data = {
            "total_diagrams": report.total_diagrams,
            "compliant": report.compliant,
            "non_compliant": report.non_compliant,
            "review_required": report.review_required,
            "unknown": report.unknown,
            "generated_at": report.generated_at.isoformat(),
            "results": [
                {
                    "diagram_id": r.diagram_id,
                    "status": r.status.value,
                    "license_type": r.license_type.value,
                    "is_commercial_use_allowed": r.is_commercial_use_allowed,
                    "is_modification_allowed": r.is_modification_allowed,
                    "attribution_required": r.attribution_required,
                    "issues": r.issues,
                    "checked_at": r.checked_at.isoformat(),
                }
                for r in report.results
            ],
        }

        json_str = json.dumps(data, indent=2)

        if output_path:
            with open(output_path, "w") as f:
                f.write(json_str)

        return json_str

    def get_summary(self, report: ComplianceReport) -> dict:
        """Get summary of compliance report."""
        return {
            "total": report.total_diagrams,
            "compliant": report.compliant,
            "non_compliant": report.non_compliant,
            "review_required": report.review_required,
            "compliance_rate": (
                report.compliant / report.total_diagrams * 100
                if report.total_diagrams > 0
                else 0
            ),
        }