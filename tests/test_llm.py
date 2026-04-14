"""Tests for LLM module."""

import pytest
from unittest.mock import patch, MagicMock

from biopress.llm.adapters.base import LLMAdapter, LLMConnectionError, ValidationResult
from biopress.llm.adapters.mimoclaw import MiMoClawAdapter
from biopress.llm.adapters.kiloclaw import KiloClawAdapter
from biopress.llm.adapters.grok import GrokAdapter
from biopress.llm.adapters.claude import ClaudeAdapter
from biopress.llm.adapters.ollama import OllamaAdapter
from biopress.llm.factory import get_adapter, list_providers
from biopress.llm.pool import ConnectionPool


class TestValidationResult:
    """Test ValidationResult dataclass."""

    def test_validation_result_creation(self):
        result = ValidationResult(
            is_valid=True,
            score=0.95,
            issues=["test issue"],
            provider="grok",
        )
        assert result.is_valid is True
        assert result.score == 0.95
        assert result.issues == ["test issue"]
        assert result.provider == "grok"


class TestLLMConnectionError:
    """Test LLMConnectionError exception."""

    def test_is_exception(self):
        assert issubclass(LLMConnectionError, Exception)

    def test_message(self):
        err = LLMConnectionError("test error")
        assert str(err) == "test error"


class TestLLMAdapterBase:
    """Test LLMAdapter abstract base class."""

    def test_cannot_instantiate_directly(self):
        with pytest.raises(TypeError):
            LLMAdapter()


class TestMiMoClawAdapter:
    """Test MiMo Claw adapter."""

    @patch("biopress.llm.adapters.mimoclaw.get_config_manager")
    def test_name(self, mock_config):
        mock_config.return_value.get.return_value = None
        adapter = MiMoClawAdapter()
        assert adapter.name == "mimoclaw"

    @pytest.mark.skip("Requires actual API key")
    @patch("biopress.llm.adapters.base.get_config_manager")
    @patch("requests.post")
    def test_generate_with_api_key(self, mock_post, mock_config):
        mock_config.return_value.get.return_value = "test-key"
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Test response"}}]
        }
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        adapter = MiMoClawAdapter()
        result = adapter.generate("test prompt")
        assert result == "Test response"

    @patch("biopress.llm.adapters.mimoclaw.get_config_manager")
    def test_generate_without_api_key_raises(self, mock_config):
        """Verify that generate raises LLMConnectionError when no API key is set."""
        mock_config.return_value.get.return_value = None
        adapter = MiMoClawAdapter()
        with pytest.raises(LLMConnectionError, match="MiMoClaw API key not configured"):
            adapter.generate("test prompt")

    @patch("biopress.llm.adapters.mimoclaw.get_config_manager")
    def test_validate_content_raises_without_key(self, mock_config):
        """Verify that validate_content raises when adapter can't connect."""
        mock_config.return_value.get.return_value = None
        adapter = MiMoClawAdapter()
        with pytest.raises(LLMConnectionError):
            adapter.validate_content({"question": "test"})

    @patch("biopress.llm.adapters.mimoclaw.get_config_manager")
    def test_check_connection_no_api_key(self, mock_config):
        mock_config.return_value.get.return_value = None
        adapter = MiMoClawAdapter()
        assert adapter.check_connection() is False


class TestGrokAdapter:
    """Test Grok adapter."""

    @patch("biopress.llm.adapters.grok.get_config_manager")
    @patch("biopress.llm.adapters.grok.get_cost_manager")
    def test_name(self, mock_cost, mock_config):
        mock_config.return_value.get.return_value = None
        mock_cost.return_value.check_budget.return_value = (True, "ok")
        adapter = GrokAdapter()
        assert adapter.name == "grok"

    @patch("biopress.llm.adapters.grok.get_config_manager")
    @patch("biopress.llm.adapters.grok.get_cost_manager")
    def test_generate_without_api_key_raises(self, mock_cost, mock_config):
        """Verify that generate raises LLMConnectionError when no API key is set."""
        mock_config.return_value.get.return_value = None
        mock_cost.return_value.check_budget.return_value = (True, "ok")
        adapter = GrokAdapter()
        with pytest.raises(LLMConnectionError, match="Grok API key not configured"):
            adapter.generate("test prompt")


class TestClaudeAdapter:
    """Test Claude adapter."""

    @patch("biopress.llm.adapters.claude.get_config_manager")
    @patch("biopress.llm.adapters.claude.get_cost_manager")
    def test_name(self, mock_cost, mock_config):
        mock_config.return_value.get.return_value = None
        mock_cost.return_value.check_budget.return_value = (True, "ok")
        adapter = ClaudeAdapter()
        assert adapter.name == "claude"

    @patch("biopress.llm.adapters.claude.get_config_manager")
    @patch("biopress.llm.adapters.claude.get_cost_manager")
    def test_generate_without_api_key_raises(self, mock_cost, mock_config):
        """Verify that generate raises LLMConnectionError when no API key is set."""
        mock_config.return_value.get.return_value = None
        mock_cost.return_value.check_budget.return_value = (True, "ok")
        adapter = ClaudeAdapter()
        with pytest.raises(LLMConnectionError, match="Claude API key not configured"):
            adapter.generate("test prompt")


class TestOllamaAdapter:
    """Test Ollama adapter."""

    @patch("biopress.llm.adapters.ollama.get_config_manager")
    def test_name(self, mock_config):
        mock_config.return_value.get.return_value = None
        adapter = OllamaAdapter()
        assert adapter.name == "ollama"

    @patch("biopress.llm.adapters.ollama.get_config_manager")
    def test_generate_without_connection_raises(self, mock_config):
        """Verify that generate raises LLMConnectionError when Ollama is unreachable."""
        mock_config.return_value.get.return_value = None
        adapter = OllamaAdapter()
        with pytest.raises(LLMConnectionError, match="Ollama server not reachable"):
            adapter.generate("test prompt")

    @patch("biopress.llm.adapters.ollama.get_config_manager")
    def test_validate_content_raises_without_connection(self, mock_config):
        """Verify that validate_content raises when Ollama is unreachable."""
        mock_config.return_value.get.return_value = None
        adapter = OllamaAdapter()
        with pytest.raises(LLMConnectionError):
            adapter.validate_content({"question": "test"})


class TestKiloClawAdapter:
    """Test Kilo Claw adapter."""

    @patch("biopress.llm.adapters.kiloclaw.get_config_manager")
    def test_name(self, mock_config):
        mock_config.return_value.get.return_value = None
        adapter = KiloClawAdapter()
        assert adapter.name == "kiloclaw"

    @patch("biopress.llm.adapters.kiloclaw.get_config_manager")
    def test_generate_without_api_key_raises(self, mock_config):
        """Verify that generate raises LLMConnectionError when no API key is set."""
        mock_config.return_value.get.return_value = None
        adapter = KiloClawAdapter()
        with pytest.raises(LLMConnectionError, match="KiloClaw API key not configured"):
            adapter.generate("test prompt")


class TestFactory:
    """Test adapter factory."""

    @patch("biopress.llm.factory.get_config_manager")
    def test_get_adapter_from_config(self, mock_config):
        mock_config.return_value.get.return_value = "grok"
        adapter = get_adapter()
        assert adapter.name == "grok"

    @patch("biopress.llm.factory.get_config_manager")
    def test_get_adapter_explicit_provider(self, mock_config):
        mock_config.return_value.get.return_value = None
        adapter = get_adapter("claude")
        assert adapter.name == "claude"

    @patch("biopress.llm.factory.get_config_manager")
    def test_get_adapter_unknown_provider(self, mock_config):
        mock_config.return_value.get.return_value = None
        with pytest.raises(ValueError) as exc_info:
            get_adapter("unknown")
        assert "Unknown provider" in str(exc_info.value)

    def test_list_providers(self):
        providers = list_providers()
        assert "mimoclaw" in providers
        assert "kiloclaw" in providers
        assert "grok" in providers
        assert "claude" in providers
        assert "ollama" in providers


class TestConnectionPool:
    """Test connection pool."""

    def test_set_provider(self):
        pool = ConnectionPool()
        pool.set_provider("grok")
        assert pool.adapter.name == "grok"

    def test_reset(self):
        pool = ConnectionPool("grok")
        pool.reset()
        assert pool._adapter is None

    def test_is_available_without_connection(self):
        pool = ConnectionPool("ollama")
        assert pool.is_available() is False

    @patch("biopress.llm.pool.get_fallback_adapter")
    def test_get_with_fallback(self, mock_fallback):
        mock_adapter = MagicMock()
        mock_adapter.check_connection.return_value = False
        mock_fallback.return_value = mock_adapter
        pool = ConnectionPool()
        result = pool.get()
        assert result == mock_adapter