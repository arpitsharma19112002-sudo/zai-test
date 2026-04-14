# Story 9.3: Persistent Memory (Optional) for BioPress Designer

**Status: Done**

## Story

As a user who wants improvement over time, I want the system to optionally track patterns, so future generations improve based on past feedback.

## Acceptance Criteria

- Given persistent memory is enabled, When I use system, Then it tracks patterns
- By default, memory is disabled
- Memory can be enabled via config

## Implementation

### 1. Memory Module (src/biopress/core/memory.py)

- `Memory` class with lightweight pattern tracking
- Disabled by default via `enabled=False` constructor parameter
- Optional SQLite storage in `~/.config/biopress/memory.db`
- `track_question_pattern(topic, question_type, quality_score)` - tracks question generation patterns
- `track_correction(original, corrected, correction_type)` - learns from editor corrections
- `get_question_stats(topic)` - retrieves question stats
- `get_correction_stats()` - retrieves correction stats
- `clear()` - clears all memory data (privacy control)
- `limit` parameter controls max records (default 1000)
- Auto-prunes oldest records when limit exceeded
- No personal data stored (only pattern keys and counts)

### 2. Config (src/biopress/core/config.py + cli/commands/config.py)

- Added `memory` config key (values: "enabled", "disabled")
- Added `memory_limit` config key (positive integer)
- CLI validation for both keys
- `biopress config set memory enabled` - enables memory
- `biopress config set memory_limit 1000` - sets max records

### 3. Generator Integration (src/biopress/generators/questions/batch.py)

- Batch generator imports and uses memory
- Tracks question patterns after generation (topic + question type)
- Quality score defaults to 0.5 for batch generation

### 4. Editor Integration (src/biopress/visual/pages/editor.py)

- Tracks editor corrections when saving changes
- Records original vs corrected text for learning
- Only active when memory is enabled

### 5. Tests (tests/test_memory.py)

- test_memory_disabled_by_default
- test_memory_enabled_via_init
- test_track_question_pattern_disabled
- test_track_question_pattern_enabled
- test_track_correction_enabled
- test_get_question_stats_empty
- test_clear_memory
- test_memory_limit_pruning
- test_get_memory_uses_config_disabled
- test_memory_singleton

## Files Modified

- src/biopress/core/memory.py (new)
- src/biopress/core/config.py
- src/biopress/cli/commands/config.py
- src/biopress/generators/questions/batch.py
- src/biopress/visual/pages/editor.py
- tests/test_memory.py (new)
- docs/stories/9-3-persistent-memory.md (new)
