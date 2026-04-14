"""Grok adapter."""

from biopress.core.config import get_config_manager
from biopress.core.cost_manager import get_cost_manager
from biopress.core.errors import LLMConnectionError, BudgetExceededError
from biopress.core.types import ValidationResult
from biopress.llm.adapters.base import LLMAdapter


class GrokAdapter(LLMAdapter):
    """Grok LLM adapter."""

    name = "grok"

    def __init__(self):
        self.config = get_config_manager()
        self.cost_manager = get_cost_manager()
        self.api_key = self.config.get("grok_api_key")
        self.base_url = "https://api.x.ai/v1"

    def generate(self, prompt: str, max_tokens: int = 1000, **kwargs) -> str:
        """Generate text using Grok.

        Raises:
            BudgetExceededError: If budget limit is reached.
            LLMConnectionError: If API key is missing or request fails.
        """
        allowed, msg = self.cost_manager.check_budget(estimated_cost=0.001)
        if not allowed:
            raise BudgetExceededError(msg)

        if not self.api_key:
            raise LLMConnectionError(
                "Grok API key not configured. "
                "Set it via: biopress config set grok_api_key <key>"
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
                    "model": "grok-2",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": max_tokens,
                },
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            usage = data.get("usage", {})
            tokens_in = usage.get("prompt_tokens", 0)
            tokens_out = usage.get("completion_tokens", 0)
            if tokens_in or tokens_out:
                self.cost_manager.add_cost(self.name, tokens_in, tokens_out)
            return data["choices"][0]["message"]["content"]
        except (LLMConnectionError, BudgetExceededError):
            raise
        except Exception as e:
            raise LLMConnectionError(f"Grok request failed: {e}") from e

    def validate_content(self, content: dict) -> ValidationResult:
        """Validate content using Grok.

        Raises:
            LLMConnectionError: If the adapter cannot connect.
        """
        prompt = f"Validate this question: {content.get('question', '')}"
        response = self.generate(prompt, max_tokens=500)

        is_valid = "invalid" not in response.lower()
        score = 0.95 if is_valid else 0.3
        issues = [] if is_valid else ["Content flagged by Grok"]

        return ValidationResult(
            is_valid=is_valid,
            score=score,
            issues=issues,
            provider=self.name,
        )

    def check_connection(self) -> bool:
        """Check if Grok is available."""
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