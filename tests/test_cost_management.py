"""Tests for cost management."""

from unittest.mock import patch

from biopress.core.cost_manager import CostManager
from biopress.core.config import ConfigManager


class TestCostManager:
    """Test CostManager functionality."""

    def test_add_cost(self):
        """Test adding a cost entry."""
        with patch.object(CostManager, '_load_costs'):
            with patch.object(CostManager, '_save_costs'):
                with patch.object(CostManager, '_check_reset'):
                    manager = CostManager()
                    manager._entries.clear()
                    cost = manager.add_cost("claude", 1000, 500)
                    assert cost > 0
                    assert manager.get_total_cost() == cost

    def test_get_total_cost(self):
        """Test getting total cost."""
        with patch.object(CostManager, '_load_costs'):
            with patch.object(CostManager, '_save_costs'):
                with patch.object(CostManager, '_check_reset'):
                    manager = CostManager()
                    manager._entries.clear()
                    manager.add_cost("claude", 1000, 500)
                    manager.add_cost("grok", 500, 250)
                    total = manager.get_total_cost()
                    assert total > 0

    def test_can_spend_no_budget(self):
        """Test can_spend returns True when no budget set."""
        with patch.object(CostManager, '_load_costs'):
            with patch.object(CostManager, '_save_costs'):
                with patch.object(CostManager, '_check_reset'):
                    manager = CostManager()
                    manager._entries.clear()
                    assert manager.can_spend() is True

    def test_can_spend_with_budget(self):
        """Test can_spend respects budget."""
        with patch.object(CostManager, '_load_costs'):
            with patch.object(CostManager, '_save_costs'):
                with patch.object(CostManager, '_check_reset'):
                    manager = CostManager()
                    manager._entries.clear()
                    with patch.object(manager, 'get_budget', return_value=0.001):
                        manager.add_cost("claude", 1000000, 500000)
                        assert manager.can_spend(0.001) is False

    def test_check_budget_exceeded(self):
        """Test check_budget returns False when exceeded."""
        with patch.object(CostManager, '_load_costs'):
            with patch.object(CostManager, '_save_costs'):
                with patch.object(CostManager, '_check_reset'):
                    manager = CostManager()
                    manager._entries.clear()
                    with patch.object(manager, 'get_budget', return_value=0.001):
                        allowed, msg = manager.check_budget(0.01)
                        assert allowed is False
                        assert "exceeded" in msg.lower()

    def test_check_budget_ok(self):
        """Test check_budget returns True when under budget."""
        with patch.object(CostManager, '_load_costs'):
            with patch.object(CostManager, '_save_costs'):
                with patch.object(CostManager, '_check_reset'):
                    manager = CostManager()
                    manager._entries.clear()
                    with patch.object(manager, 'get_budget', return_value=10.0):
                        allowed, msg = manager.check_budget(0.01)
                        assert allowed is True

    def test_get_report(self):
        """Test cost report generation."""
        with patch.object(CostManager, '_load_costs'):
            with patch.object(CostManager, '_save_costs'):
                with patch.object(CostManager, '_check_reset'):
                    manager = CostManager()
                    manager._entries.clear()
                    manager.add_cost("claude", 1000, 500)
                    manager.add_cost("grok", 500, 250)
                    report = manager.get_report()
                    assert report.total_cost > 0
                    assert report.requests == 2
                    assert "claude" in report.by_provider
                    assert "grok" in report.by_provider


class TestBudgetConfig:
    """Test budget configuration."""

    def test_budget_config_key(self):
        """Test budget is a valid config key."""
        with patch.object(ConfigManager, '_load_config', return_value={"budget": "1.0"}):
            with patch.object(ConfigManager, '_save_config'):
                config = ConfigManager()
                assert config.get("budget") == "1.0"

    def test_budget_reset_config(self):
        """Test budget_reset is a valid config key."""
        with patch.object(ConfigManager, '_load_config', return_value={"budget_reset": "true"}):
            with patch.object(ConfigManager, '_save_config'):
                config = ConfigManager()
                assert config.get("budget_reset") == "true"