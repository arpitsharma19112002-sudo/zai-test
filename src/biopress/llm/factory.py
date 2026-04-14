"""LLM adapter factory."""

from typing import Optional

from biopress.core.config import get_config_manager
from biopress.llm.adapters.base import LLMAdapter
from biopress.llm.adapters.mimoclaw import MiMoClawAdapter
from biopress.llm.adapters.kiloclaw import KiloClawAdapter
from biopress.llm.adapters.grok import GrokAdapter
from biopress.llm.adapters.claude import ClaudeAdapter
from biopress.llm.adapters.ollama import OllamaAdapter


ADAPTERS = {
    "mimoclaw": MiMoClawAdapter,
    "kiloclaw": KiloClawAdapter,
    "grok": GrokAdapter,
    "claude": ClaudeAdapter,
    "ollama": OllamaAdapter,
}

_fallback_order = ["ollama", "claude", "grok", "kiloclaw", "mimoclaw"]


def get_adapter(provider: Optional[str] = None) -> LLMAdapter:
    """Get the LLM adapter based on config or specified provider.
    
    Args:
        provider: Optional provider name. If not specified, uses config.
        
    Returns:
        LLMAdapter instance
        
    Raises:
        ValueError: If provider is not supported
    """
    if provider is None:
        config = get_config_manager()
        provider = config.get("provider") or "ollama"
    
    provider = provider.lower()
    
    if provider not in ADAPTERS:
        raise ValueError(f"Unknown provider: {provider}. Available: {list(ADAPTERS.keys())}")
    
    return ADAPTERS[provider]()


def get_fallback_adapter() -> LLMAdapter:
    """Get the first available fallback adapter."""
    for provider_name in _fallback_order:
        adapter = ADAPTERS[provider_name]()
        if adapter.check_connection():
            return adapter
    return ADAPTERS["ollama"]()


def list_providers() -> list[str]:
    """List all available provider names."""
    return list(ADAPTERS.keys())