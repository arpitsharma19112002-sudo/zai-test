"""Kilo Claw adapter."""

from biopress.llm.adapters.base import LLMAdapter, LLMConnectionError, ValidationResult
from biopress.core.config import get_config_manager


class KiloClawAdapter(LLMAdapter):
    """Kilo Claw LLM adapter."""

    name = "kiloclaw"

    def __init__(self):
        self.config = get_config_manager()
        self.api_key = self.config.get("kiloclaw_api_key")
        self.base_url = "https://api.kiloclaw.ai/v1"

    def generate(self, prompt: str, max_tokens: int = 1000, **kwargs) -> str:
        """Generate text using Kilo Claw.

        Raises:
            LLMConnectionError: If API key is missing or request fails.
        """
        if not self.api_key:
            raise LLMConnectionError(
                "KiloClaw API key not configured. "
                "Set it via: biopress config set kiloclaw_api_key <key>"
            )

        try:
            import requests
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "kiloclaw-3b",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": max_tokens,
                },
                timeout=30,
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except LLMConnectionError:
            raise
        except Exception as e:
            raise LLMConnectionError(f"KiloClaw request failed: {e}") from e

    def validate_content(self, content: dict) -> ValidationResult:
        """Validate content using Kilo Claw.

        Raises:
            LLMConnectionError: If the adapter cannot connect.
        """
        prompt = f"Validate: {content.get('question', '')}"
        response = self.generate(prompt, max_tokens=500)

        is_valid = "invalid" not in response.lower()
        score = 0.85 if is_valid else 0.3
        issues = [] if is_valid else ["Content flagged by KiloClaw"]

        return ValidationResult(
            is_valid=is_valid,
            score=score,
            issues=issues,
            provider=self.name,
        )

    def check_connection(self) -> bool:
        """Check if Kilo Claw is available."""
        if not self.api_key:
            return False
        try:
            import requests
            response = requests.get(
                f"{self.base_url}/models",
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=5,
            )
            return response.status_code == 200
        except Exception:
            return False