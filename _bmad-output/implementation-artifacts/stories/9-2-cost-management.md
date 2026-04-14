# Story 9.2: Cost Management for BioPress Designer

**Epic:** 9 - Optimization & Optional Features
**Status:** done
**Priority:** High

## Story

As a budget-conscious user, I want cost tracking and limits, so I control expenses.

## Acceptance Criteria

- Given I generate questions, Then I see estimated cost before execution
- Cost alerts when threshold exceeded
- Budget limits can be set

## Implementation Notes

### Cost Management Implemented

1. **Cost Estimation** (`src/biopress/utils/cost_tracker.py`)
   - Estimate based on prompt tokens + completion tokens
   - Show cost per question type
   - Display total estimated cost

2. **Budget Limits** (`src/biopress/utils/cost_tracker.py`)
   - Set max budget per session
   - Stop generation when limit reached
   - Warning at 80% threshold

3. **Cost Reports** (`src/biopress/utils/cost_tracker.py`)
   - Session cost summary
   - Compare across question types
   - Export cost logs

## Files Modified

- `src/biopress/utils/cost_tracker.py` - New cost tracking module
- CLI commands updated for cost display

## Notes

- Default budget: $10/session
- Cost calculated using OpenAI pricing
- Can be customized via config
