"""MiMo Claw adapter."""

from biopress.core.config import get_config_manager
from biopress.core.errors import LLMConnectionError
from biopress.core.types import ValidationResult
from biopress.llm.adapters.base import LLMAdapter


class MiMoClawAdapter(LLMAdapter):
    """MiMo Claw LLM adapter."""

    name = "mimoclaw"

    def __init__(self):
        self.config = get_config_manager()
        self.api_key = self.config.get("mimoclaw_api_key")
        self.base_url = "https://api.mimoclaw.ai/v1"

    def generate(self, prompt: str, max_tokens: int = 1000, **kwargs) -> str:
        """Generate text using MiMo Claw.

        Raises:
            LLMConnectionError: If API key is missing or request fails.
        """
        if not self.api_key:
            raise LLMConnectionError(
                "MiMoClaw API key not configured. "
                "Set it via: biopress config set mimoclaw_api_key <key>"
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
                    "model": "mimoclaw-8b",
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
            raise LLMConnectionError(f"MiMoClaw request failed: {e}") from e

    def validate_content(self, content: dict) -> ValidationResult:
        """Validate content using MiMo Claw.

        Raises:
            LLMConnectionError: If the adapter cannot connect.
        """
        prompt = f"Validate the following question: {content.get('question', '')}"
        response = self.generate(prompt, max_tokens=500)

        # Parse response for actual validation signals
        is_valid = "invalid" not in response.lower()
        score = 0.9 if is_valid else 0.3
        issues = [] if is_valid else ["Content flagged by MiMoClaw"]

        return ValidationResult(
            is_valid=is_valid,
            score=score,
            issues=issues,
            provider=self.name,
        )

    def check_connection(self) -> bool:
        """Check if MiMo Claw is available."""
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