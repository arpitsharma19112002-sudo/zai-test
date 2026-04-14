---
story_id: 2-4
story_key: 2-4-assertion-reason-question-generation
title: Assertion-Reason Question Generation
status: done
created: 2026-04-14
completed: 2026-04-14
epic_id: epic-2
---

# Story 2.4: Assertion-Reason Question Generation

## Story

**As a** content creator,
**I want** to generate assertion-reason type questions,
**So that** I can create questions testing conceptual understanding.

## Acceptance Criteria

**Given** a valid exam and subject is specified
**When** I run `biopress generate --exam NEET --subject Chemistry --type assertion-reason --count 5`
**Then** I receive 5 assertion-reason questions
**And** each has: assertion statement, reason statement, correct option (A/B/C/D as per NEET format)
**And** the logic connecting assertion and reason is correct

## Tasks

- [x] Implement assertion-reason question generator module
- [x] Create NEET-style option format (A/B/C/D)
- [x] Implement logical reasoning validation
- [x] Support all three subjects (Physics, Chemistry, Biology)
- [x] Add proper assertion-reason logic templates
- [x] Add tests for assertion-reason generation
- [x] Verify logical correctness of relationships

## Dev Agent Record

### Implementation Plan

**Architecture Requirements:**

- Used generator module pattern from previous stories
- Created NEET-specific option format (A/B/C/D)
- Implemented logical relationship templates
- Followed Perseus JSON extended format

**Technical Decisions:**

- Assertion-reason generator: `src/biopress/generators/assertion_reason.py`
- Logic templates: `src/biopress/generators/templates/assertion_reason/`
- Option structure: NEET format with A/B/C/D options

### Debug Log

No issues encountered.

### Completion Notes

Implemented assertion-reason question generation with:

- Full support for Physics, Chemistry, and Biology
- NEET-standard option format (A/B/C/D)
- Proper logical relationships (if-then, because, etc.)
- Validated assertion-reason logic
- All tests passing

## File List

- `src/biopress/generators/assertion_reason.py` - Assertion-reason generator
- `src/biopress/generators/templates/assertion_reason/` - Perseus templates
- `tests/test_assertion_reason.py` - Tests (all passing)

## Change Log

- 2026-04-14: Initial implementation of assertion-reason question generation
