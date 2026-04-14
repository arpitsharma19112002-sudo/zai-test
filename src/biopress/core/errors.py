"""Core exception types for BioPress."""

class LLMConnectionError(Exception):
    """Raised when an LLM adapter cannot connect or generate content."""
    pass


class BudgetExceededError(Exception):
    """Raised when the configured budget limit is reached."""
    pass
