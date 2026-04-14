"""Cost management for LLM usage."""

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .config import get_config_manager


@dataclass
class CostEntry:
    """Individual cost entry."""
    provider: str
    tokens_in: int
    tokens_out: int
    cost: float
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class CostReport:
    """Cost report summary."""
    total_cost: float
    total_tokens_in: int
    total_tokens_out: int
    by_provider: dict[str, float]
    requests: int


class CostManager:
    """Manages LLM costs and budget enforcement."""

    COST_FILE = Path.home() / ".config" / "biopress" / "costs.json"

    TOKEN_PRICES = {
        "claude": {"input": 0.015, "output": 0.075},
        "grok": {"input": 0.005, "output": 0.015},
        "openai": {"input": 0.01, "output": 0.03},
        "ollama": {"input": 0.0, "output": 0.0},
        "mimoclaw": {"input": 0.015, "output": 0.075},
        "kiloclaw": {"input": 0.01, "output": 0.03},
    }

    def __init__(self) -> None:
        self._entries: list[CostEntry] = []
        self._load_costs()
        self._check_reset()

    def _load_costs(self) -> None:
        """Load cost entries from file."""
        if not self.COST_FILE.exists():
            return
        try:
            with open(self.COST_FILE) as f:
                data = json.load(f)
                for entry in data.get("entries", []):
                    self._entries.append(CostEntry(
                        provider=entry["provider"],
                        tokens_in=entry["tokens_in"],
                        tokens_out=entry["tokens_out"],
                        cost=entry["cost"],
                        timestamp=datetime.fromisoformat(entry["timestamp"]),
                    ))
        except (json.JSONDecodeError, IOError, KeyError):
            pass

    def _save_costs(self) -> None:
        """Save cost entries to file."""
        self.COST_FILE.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "entries": [
                {
                    "provider": e.provider,
                    "tokens_in": e.tokens_in,
                    "tokens_out": e.tokens_out,
                    "cost": e.cost,
                    "timestamp": e.timestamp.isoformat(),
                }
                for e in self._entries
            ]
        }
        with open(self.COST_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def _check_reset(self) -> None:
        """Check if budget should be reset."""
        config = get_config_manager()
        if config.get("budget_reset") == "true":
            self._entries.clear()
            self._save_costs()

    def add_cost(
        self,
        provider: str,
        tokens_in: int,
        tokens_out: int,
    ) -> float:
        """Add a cost entry and return the cost."""
        prices = self.TOKEN_PRICES.get(provider, {"input": 0.01, "output": 0.03})
        cost = (tokens_in / 1_000_000 * prices["input"] +
                tokens_out / 1_000_000 * prices["output"])
        entry = CostEntry(
            provider=provider,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            cost=cost,
        )
        self._entries.append(entry)
        self._save_costs()
        return cost

    def get_total_cost(self) -> float:
        """Get total cost spent."""
        return sum(e.cost for e in self._entries)

    def get_budget(self) -> Optional[float]:
        """Get the configured budget."""
        config = get_config_manager()
        value = config.get("budget")
        return float(value) if value else None

    def can_spend(self, estimated_cost: float = 0.001) -> bool:
        """Check if budget allows spending."""
        budget = self.get_budget()
        if budget is None:
            return True
        return self.get_total_cost() + estimated_cost <= budget

    def get_report(self) -> CostReport:
        """Generate cost report."""
        by_provider: dict[str, float] = {}
        total_in = 0
        total_out = 0
        for e in self._entries:
            by_provider[e.provider] = by_provider.get(e.provider, 0.0) + e.cost
            total_in += e.tokens_in
            total_out += e.tokens_out
        return CostReport(
            total_cost=sum(e.cost for e in self._entries),
            total_tokens_in=total_in,
            total_tokens_out=total_out,
            by_provider=by_provider,
            requests=len(self._entries),
        )

    def check_budget(self, estimated_cost: float = 0.001) -> tuple[bool, str]:
        """Check budget and return (allowed, message)."""
        budget = self.get_budget()
        if budget is None:
            return True, "No budget set"
        spent = self.get_total_cost()
        remaining = budget - spent
        if remaining < estimated_cost:
            return False, f"Budget exceeded! Spent ${spent:.2f} of ${budget:.2f}"
        return True, f"Remaining: ${remaining:.2f} / ${budget:.2f}"


import threading

_cost_manager: Optional[CostManager] = None
_lock = threading.Lock()


def get_cost_manager() -> CostManager:
    """Get the global cost manager instance with thread safety."""
    global _cost_manager
    if _cost_manager is None:
        with _lock:
            if _cost_manager is None:
                _cost_manager = CostManager()
    return _cost_manager