"""Base LLM adapter interface."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


from biopress.core.errors import LLMConnectionError
from biopress.core.types import ValidationResult


class LLMAdapter(ABC):
    """Abstract base class for LLM adapters."""

    name: str = "base"

    @abstractmethod
    def generate(self, prompt: str, max_tokens: int = 1000, **kwargs) -> str:
        """Generate text from prompt."""
        pass

    @abstractmethod
    def validate_content(self, content: dict) -> ValidationResult:
        """Validate content quality."""
        pass

    @abstractmethod
    def check_connection(self) -> bool:
        """Check if adapter is available."""
        pass