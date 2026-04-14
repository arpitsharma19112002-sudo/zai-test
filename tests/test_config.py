"""Tests for BioPress config functionality."""

import json
import tempfile
from pathlib import Path
from typing import Generator

import pytest
from typer.testing import CliRunner

from biopress.cli.app import app

runner = CliRunner()


@pytest.fixture
def temp_config_dir(monkeypatch: pytest.MonkeyPatch) -> Generator[Path, None, None]:
    """Create a temporary config directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_dir = Path(tmpdir) / ".config" / "biopress"
        config_dir.mkdir(parents=True)
        config_file = config_dir / "config.json"

        monkeypatch.setattr("biopress.core.config.ConfigManager.CONFIG_DIR", config_dir)
        monkeypatch.setattr("biopress.core.config.ConfigManager.CONFIG_FILE", config_file)

        yield config_dir


class TestConfigSet:
    """Tests for config set command."""

    def test_set_provider(self, temp_config_dir: Path) -> None:
        """Test setting provider configuration."""
        result = runner.invoke(app, ["config", "set", "provider", "ollama"])
        assert result.exit_code == 0
        assert "Set provider = ollama" in result.stdout

    def test_set_output_dir(self, temp_config_dir: Path) -> None:
        """Test setting output_dir configuration."""
        result = runner.invoke(app, ["config", "set", "output_dir", "/tmp/output"])
        assert result.exit_code == 0
        assert "Set output_dir = /tmp/output" in result.stdout

    def test_set_language(self, temp_config_dir: Path) -> None:
        """Test setting language configuration."""
        result = runner.invoke(app, ["config", "set", "language", "hindi"])
        assert result.exit_code == 0
        assert "Set language = hindi" in result.stdout

    def test_set_invalid_key(self, temp_config_dir: Path) -> None:
        """Test setting invalid configuration key."""
        result = runner.invoke(app, ["config", "set", "invalid_key", "value"])
        assert result.exit_code == 1
        assert "Invalid key" in result.output

    def test_set_invalid_provider(self, temp_config_dir: Path) -> None:
        """Test setting invalid provider."""
        result = runner.invoke(app, ["config", "set", "provider", "invalid"])
        assert result.exit_code == 1
        assert "Invalid provider" in result.output

    def test_set_invalid_language(self, temp_config_dir: Path) -> None:
        """Test setting invalid language."""
        result = runner.invoke(app, ["config", "set", "language", "spanish"])
        assert result.exit_code == 1
        assert "Invalid language" in result.output


class TestConfigGet:
    """Tests for config get command."""

    def test_get_existing_key(self, temp_config_dir: Path) -> None:
        """Test getting existing configuration value."""
        runner.invoke(app, ["config", "set", "provider", "ollama"])
        result = runner.invoke(app, ["config", "get", "provider"])
        assert result.exit_code == 0
        assert "ollama" in result.output

    def test_get_nonexistent_key(self, temp_config_dir: Path) -> None:
        """Test getting non-existent configuration value."""
        result = runner.invoke(app, ["config", "get", "provider"])
        assert result.exit_code == 1
        assert "not set" in result.output

    def test_get_invalid_key(self, temp_config_dir: Path) -> None:
        """Test getting with invalid key."""
        result = runner.invoke(app, ["config", "get", "invalid_key"])
        assert result.exit_code == 1
        assert "Invalid key" in result.output


class TestConfigList:
    """Tests for config list command."""

    def test_list_empty(self, temp_config_dir: Path) -> None:
        """Test listing with no configuration."""
        result = runner.invoke(app, ["config", "list"])
        assert result.exit_code == 0
        assert "No configuration found" in result.stdout

    def test_list_with_values(self, temp_config_dir: Path) -> None:
        """Test listing configuration values."""
        runner.invoke(app, ["config", "set", "provider", "ollama"])
        runner.invoke(app, ["config", "set", "language", "english"])
        result = runner.invoke(app, ["config", "list"])
        assert result.exit_code == 0
        assert "provider = ollama" in result.stdout
        assert "language = english" in result.stdout


class TestConfigPersistence:
    """Tests for configuration persistence."""

    def test_config_persists(self, temp_config_dir: Path) -> None:
        """Test that configuration persists between sessions."""
        runner.invoke(app, ["config", "set", "provider", "grok"])
        config_file = temp_config_dir / "config.json"

        assert config_file.exists()
        with open(config_file) as f:
            config = json.load(f)
        assert config["provider"] == "grok"
