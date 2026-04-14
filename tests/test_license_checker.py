"""Tests for license checker."""


from biopress.generators.content.diagram import Diagram
from biopress.generators.content.diagram_source import LicenseType
from biopress.generators.content.license_checker import (
    ComplianceReport,
    ComplianceResult,
    ComplianceStatus,
    LicenseChecker,
)


class TestLicenseChecker:
    """Tests for LicenseChecker class."""

    def test_check_diagram_cc_by(self):
        """Test CC BY license is fully compliant."""
        checker = LicenseChecker()
        diagram = Diagram(
            topic="Cell",
            subject="Biology",
            source="OpenStax",
            url="https://example.com/cell.svg",
        )

        result = checker.check_diagram(diagram)

        assert result.license_type == LicenseType.CC_BY
        assert result.status == ComplianceStatus.COMPLIANT

    def test_check_diagram_cc_by_nc(self):
        """Test CC BY-NC license for non-commercial use only."""
        checker = LicenseChecker()
        diagram = Diagram(
            topic="Cell",
            subject="Biology",
            source="HyperPhysics",
            url="https://example.com/cell.svg",
        )

        result = checker.check_diagram(diagram)

        assert result.license_type == LicenseType.CC_BY_NC_SA
        assert result.is_commercial_use_allowed is False

    def test_verify_diagram_license_compliant(self):
        """Test verifying a compliant diagram."""
        checker = LicenseChecker()
        diagram = Diagram(
            topic="Cell",
            subject="Biology",
            source="Servier",
            url="https://example.com/cell.svg",
        )

        is_valid, message = checker.verify_diagram_license(diagram)

        assert is_valid is True
        assert message == "License compliant"

    def test_verify_diagram_non_compliant(self):
        """Test verifying a non-compliant diagram."""
        checker = LicenseChecker()
        diagram = Diagram(
            topic="Cell",
            subject="Biology",
            source="HyperPhysics",
            url="https://example.com/cell.svg",
        )

        is_valid, message = checker.verify_diagram_license(diagram)

        assert is_valid is False
        assert "Non-commercial" in message or "Review required" in message

    def test_generate_report(self):
        """Test generating compliance report."""
        checker = LicenseChecker()
        diagrams = [
            Diagram(topic="Cell", subject="Biology", source="OpenStax"),
            Diagram(topic="DNA", subject="Biology", source="Servier"),
            Diagram(topic="Mitochondria", subject="Biology", source="HyperPhysics"),
        ]

        report = checker.generate_report(diagrams)

        assert report.total_diagrams == 3
        assert report.compliant > 0

    def test_report_json_export(self):
        """Test exporting report as JSON."""
        checker = LicenseChecker()
        diagrams = [
            Diagram(topic="Cell", subject="Biology", source="OpenStax"),
        ]

        report = checker.generate_report(diagrams)
        json_str = checker.to_json(report)

        assert '"total_diagrams": 1' in json_str
        assert '"compliant":' in json_str

    def test_report_summary(self):
        """Test getting report summary."""
        checker = LicenseChecker()
        diagrams = [
            Diagram(topic="Cell", subject="Biology", source="OpenStax"),
        ]

        report = checker.generate_report(diagrams)
        summary = checker.get_summary(report)

        assert "total" in summary
        assert "compliance_rate" in summary
        assert summary["total"] == 1


class TestComplianceResults:
    """Tests for compliance results."""

    def test_compliance_result_creation(self):
        """Test creating compliance result."""
        result = ComplianceResult(
            diagram_id="test-123",
            status=ComplianceStatus.COMPLIANT,
            license_type=LicenseType.CC_BY,
            is_commercial_use_allowed=True,
            is_modification_allowed=True,
            attribution_required=True,
            issues=[],
        )

        assert result.diagram_id == "test-123"
        assert result.status == ComplianceStatus.COMPLIANT

    def test_compliance_report_creation(self):
        """Test creating compliance report."""
        report = ComplianceReport(
            total_diagrams=5,
            compliant=3,
            non_compliant=1,
            review_required=1,
        )

        assert report.total_diagrams == 5
        assert report.compliant == 3
        assert report.review_required == 1