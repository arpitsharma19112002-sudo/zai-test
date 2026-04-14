"""Connection pool for LLM adapters."""

from typing import Optional

from biopress.llm.adapters.base import LLMAdapter
from biopress.llm.factory import get_adapter, get_fallback_adapter


class ConnectionPool:
    """Manages LLM adapter connections with fallback support."""

    def __init__(self, provider: Optional[str] = None):
        self._provider = provider
        self._adapter: Optional[LLMAdapter] = None

    @property
    def adapter(self) -> LLMAdapter:
        """Get the current adapter, initializing if needed."""
        if self._adapter is None:
            self._adapter = get_adapter(self._provider)
        return self._adapter

    def get(self) -> LLMAdapter:
        """Get an available adapter with fallback."""
        if self.adapter.check_connection():
            return self.adapter
        return get_fallback_adapter()

    def set_provider(self, provider: str) -> None:
        """Switch to a different provider."""
        self._provider = provider
        self._adapter = None

    def reset(self) -> None:
        """Reset the adapter."""
        self._adapter = None

    def is_available(self) -> bool:
        """Check if current adapter is available."""
        return self.adapter.check_connection()


_default_pool: Optional[ConnectionPool] = None


def get_pool(provider: Optional[str] = None) -> ConnectionPool:
    """Get the default connection pool."""
    global _default_pool
    if _default_pool is None:
        _default_pool = ConnectionPool(provider)
    return _default_pool