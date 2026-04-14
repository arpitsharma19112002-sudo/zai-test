"""Ollama adapter for local models."""

from biopress.core.config import get_config_manager
from biopress.core.errors import LLMConnectionError
from biopress.core.types import ValidationResult
from biopress.llm.adapters.base import LLMAdapter


class OllamaAdapter(LLMAdapter):
    """Ollama local LLM adapter."""

    name = "ollama"

    def __init__(self):
        self.config = get_config_manager()
        self.base_url = self.config.get("ollama_url") or "http://localhost:11434"
        self.model = self.config.get("ollama_model") or "llama2"

    def generate(self, prompt: str, max_tokens: int = 1000, **kwargs) -> str:
        """Generate text using Ollama.

        Raises:
            LLMConnectionError: If Ollama server is not reachable.
        """
        try:
            import requests
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                },
                timeout=60,
            )
            response.raise_for_status()
            return response.json().get("response", "")
        except Exception as e:
            raise LLMConnectionError(
                f"Ollama server not reachable at {self.base_url}: {e}"
            ) from e

    def validate_content(self, content: dict) -> ValidationResult:
        """Validate content using Ollama.

        Raises:
            LLMConnectionError: If the adapter cannot connect.
        """
        prompt = f"Validate: {content.get('question', '')}"
        response = self.generate(prompt, max_tokens=500)

        is_valid = "invalid" not in response.lower()
        score = 0.8 if is_valid else 0.3
        issues = [] if is_valid else ["Content flagged by Ollama"]

        return ValidationResult(
            is_valid=is_valid,
            score=score,
            issues=issues,
            provider=self.name,
        )

    def check_connection(self) -> bool:
        """Check if Ollama is available."""
        try:
            import requests
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception:
            return False