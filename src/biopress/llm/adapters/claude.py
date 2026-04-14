"""Claude adapter."""

from biopress.core.errors import LLMConnectionError, BudgetExceededError
from biopress.core.types import ValidationResult


class ClaudeAdapter(LLMAdapter):
    """Claude LLM adapter."""

    name = "claude"

    def __init__(self):
        self.config = get_config_manager()
        self.cost_manager = get_cost_manager()
        self.api_key = self.config.get("claude_api_key")
        self.base_url = "https://api.anthropic.com/v1"

    def generate(self, prompt: str, max_tokens: int = 1000, **kwargs) -> str:
        """Generate text using Claude.

        Raises:
            BudgetExceededError: If budget limit is reached.
            LLMConnectionError: If API key is missing or request fails.
        """
        allowed, msg = self.cost_manager.check_budget(estimated_cost=0.001)
        if not allowed:
            raise BudgetExceededError(msg)

        if not self.api_key:
            raise LLMConnectionError(
                "Claude API key not configured. "
                "Set it via: biopress config set claude_api_key <key>"
            )

        try:
            import requests
            response = requests.post(
                f"{self.base_url}/messages",
                headers={
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "claude-3-5-sonnet-20241022",
                    "max_tokens": max_tokens,
                    "messages": [{"role": "user", "content": prompt}],
                },
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            tokens_in = len(prompt.split()) * 1.3
            tokens_out = len(data["content"][0]["text"].split()) * 1.3
            self.cost_manager.add_cost(self.name, int(tokens_in), int(tokens_out))
            return data["content"][0]["text"]
        except (LLMConnectionError, BudgetExceededError):
            raise
        except Exception as e:
            raise LLMConnectionError(f"Claude request failed: {e}") from e

    def validate_content(self, content: dict) -> ValidationResult:
        """Validate content using Claude.

        Raises:
            LLMConnectionError: If the adapter cannot connect.
        """
        prompt = f"Validate: {content.get('question', '')}"
        response = self.generate(prompt, max_tokens=500)

        is_valid = "invalid" not in response.lower()
        score = 0.98 if is_valid else 0.3
        issues = [] if is_valid else ["Content flagged by Claude"]

        return ValidationResult(
            is_valid=is_valid,
            score=score,
            issues=issues,
            provider=self.name,
        )

    def check_connection(self) -> bool:
        """Check if Claude is available."""
        if not self.api_key:
            return False
        try:
            import requests
            response = requests.get(
                "https://api.anthropic.com/v1/models",
                headers={
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01",
                },
                timeout=5,
            )
            return response.status_code == 200
        except Exception:
            return False