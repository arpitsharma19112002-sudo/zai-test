---
story_id: 2-5
story_key: 2-5-batch-question-generation
title: Batch Question Generation
status: done
created: 2026-04-14
completed: 2026-04-14
epic_id: epic-2
---

# Story 2.5: Batch Question Generation

## Story

**As a** content creator,
**I want** to generate multiple questions in a single command,
**So that** I can efficiently create large question banks.

## Acceptance Criteria

**Given** I specify multiple topics or a chapter
**When** I run `biopress generate --exam NEET --subject Physics --count 100`
**Then** I receive up to 100 questions
**And** questions are distributed across topics proportionally
**And** generation completes within reasonable time (<2 minutes)

## Tasks

- [x] Implement batch generator orchestrator
- [x] Add topic distribution logic
- [x] Implement parallel generation for speed
- [x] Add progress tracking for large batches
- [x] Support mixed question types in batch
- [x] Add batch size validation (up to 500)
- [x] Add tests for batch generation
- [x] Verify performance (<2 min for 100 questions)

## Dev Agent Record

### Implementation Plan

**Architecture Requirements:**

- Used parallel processing for batch operations
- Implemented topic distribution algorithm
- Created batch orchestrator module
- Followed existing generator patterns

**Technical Decisions:**

- Batch orchestrator: `src/biopress/generators/batch.py`
- Topic distribution: proportional by weight
- Parallel execution: ThreadPoolExecutor for LLM calls

### Debug Log

No issues encountered.

### Completion Notes

Implemented batch question generation with:

- Support for up to 500 questions per batch
- Proportional topic distribution
- Parallel generation for performance
- Progress tracking and ETA display
- Mixed question type support
- Performance targets met (<2 min for 100 questions)

## File List

- `src/biopress/generators/batch.py` - Batch orchestrator
- `src/biopress/generators/topic_distributor.py` - Topic distribution
- `tests/test_batch.py` - Tests (all passing)

## Change Log

- 2026-04-14: Initial implementation of batch question generation
