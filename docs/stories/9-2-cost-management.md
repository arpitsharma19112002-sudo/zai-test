# Story 9.2: Cost Management for BioPress Designer

**Status: Done**

## Story

As a cost-conscious user, I want to set budget caps for LLM usage, so I don't overspend on generation.

## Acceptance Criteria

- Given I'm using cloud LLM, When I set budget, Then generation stops at budget
- I can see token usage and cost reports
- Budget resets for new sessions

## Implementation

### 1. Config (src/biopress/core/config.py)

- Added `budget` config key (float, dollars)
- Added `budget_reset` config key (boolean)

### 2. Cost Manager (src/biopress/core/cost_manager.py)

- `CostManager` tracks costs per provider
- Token prices per model (per 1M tokens)
- `add_cost()` adds cost entry and returns calculated cost
- `get_total_cost()` returns total spent
- `get_budget()` returns configured budget
- `can_spend()` checks if budget allows estimated spend
- `check_budget()` returns (allowed, message) tuple
- `get_report()` returns CostReport with totals and per-provider breakdown

### 3. CLI Commands (src/biopress/cli/commands/config.py)

- `config set budget 1.00` - Sets budget cap
- `config set budget_reset true` - Enables budget reset per session
- `config report` - Shows cost usage report

### 4. LLM Adapters

- ClaudeAdapter: checks budget before generation, tracks token usage
- GrokAdapter: checks budget before generation, tracks token usage

BudgetExceededError raised when limit exceeded.

### 5. Tests (tests/test_cost_management.py)

- test_add_cost
- test_get_total_cost
- test_can_spend_no_budget
- test_can_spend_with_budget
- test_check_budget_exceeded
- test_check_budget_ok
- test_get_report
- test_budget_config_key
- test_budget_reset_config

## Files Modified

- src/biopress/core/config.py
- src/biopress/core/cost_manager.py (new)
- src/biopress/cli/commands/config.py
- src/biopress/llm/adapters/claude.py
- src/biopress/llm/adapters/grok.py
- tests/test_cost_management.py (new)
- docs/stories/9-2-cost-management.md (new)
