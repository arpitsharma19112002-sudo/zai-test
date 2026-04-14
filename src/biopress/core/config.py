"""BioPress configuration management."""

import json
from pathlib import Path
from typing import Literal, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class BioPressConfig(BaseSettings):
    """BioPress configuration model."""

    model_config = SettingsConfigDict(
        config_file=".biopress.json",
        env_prefix="BIOPRESS_",
        extra="ignore",
    )

    provider: Optional[str] = Field(
        default=None,
        description="LLM provider (ollama, grok, claude, etc.)",
    )
    output_dir: Optional[str] = Field(
        default=None,
        description="Default output directory",
    )
    language: Optional[Literal["english", "hindi"]] = Field(
        default=None,
        description="Default language",
    )
    budget: Optional[float] = Field(
        default=None,
        description="Budget cap for LLM usage (in dollars)",
    )
    budget_reset: Optional[bool] = Field(
        default=None,
        description="Reset budget for new sessions",
    )


class ConfigManager:
    """Manages BioPress configuration persistence."""

    CONFIG_DIR = Path.home() / ".config" / "biopress"
    CONFIG_FILE = CONFIG_DIR / "config.json"

    def __init__(self) -> None:
        self._ensure_config_dir()

    def _ensure_config_dir(self) -> None:
        """Ensure config directory exists."""
        self.CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    def _load_config(self) -> dict:
        """Load configuration from file."""
        if not self.CONFIG_FILE.exists():
            return {}
        try:
            with open(self.CONFIG_FILE) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}

    def _save_config(self, config: dict) -> None:
        """Save configuration to file."""
        with open(self.CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=2)

    def get(self, key: str) -> Optional[str]:
        """Get a configuration value."""
        config = self._load_config()
        return config.get(key)

    def set(self, key: str, value: str) -> None:
        """Set a configuration value."""
        config = self._load_config()
        config[key] = value
        self._save_config(config)

    def list(self) -> dict:
        """List all configuration values."""
        return self._load_config()

    def delete(self, key: str) -> None:
        """Delete a configuration value."""
        config = self._load_config()
        if key in config:
            del config[key]
            self._save_config(config)


def get_config_manager() -> ConfigManager:
    """Get the global config manager instance."""
    return ConfigManager()
