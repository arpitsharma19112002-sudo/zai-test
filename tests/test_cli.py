"""Tests for BioPress CLI."""

from typer.testing import CliRunner

from biopress.cli.app import app

runner = CliRunner()


def test_help_command():
    """Test that --help shows all available commands."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "generate" in result.stdout
    assert "validate" in result.stdout
    assert "review" in result.stdout
    assert "export" in result.stdout
    assert "config" in result.stdout
    assert "kb" in result.stdout


def test_version_command():
    """Test that --version shows the version."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "BioPress Designer version" in result.stdout
    assert "0.1.0" in result.stdout


def test_generate_command_help():
    """Test generate subcommand help."""
    result = runner.invoke(app, ["generate", "--help"])
    assert result.exit_code == 0
    assert "Generate questions for NEET/JEE exams" in result.stdout


def test_validate_command_help():
    """Test validate subcommand help."""
    result = runner.invoke(app, ["validate", "--help"])
    assert result.exit_code == 0
    assert "Validate generated content quality" in result.stdout


def test_review_command_help():
    """Test review subcommand help."""
    result = runner.invoke(app, ["review", "--help"])
    assert result.exit_code == 0
    assert "Review and edit content visually" in result.stdout


def test_export_command_help():
    """Test export subcommand help."""
    result = runner.invoke(app, ["export", "--help"])
    assert result.exit_code == 0
    assert "Export content to PDF" in result.stdout


def test_config_command_help():
    """Test config subcommand help."""
    result = runner.invoke(app, ["config", "--help"])
    assert result.exit_code == 0
    assert "Manage BioPress configuration" in result.stdout


def test_kb_command_help():
    """Test kb subcommand help."""
    result = runner.invoke(app, ["kb", "--help"])
    assert result.exit_code == 0
    assert "Manage knowledge base" in result.stdout
