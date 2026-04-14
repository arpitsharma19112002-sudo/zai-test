---
story_id: 2-3
story_key: 2-3-case-based-question-generation
title: Case-Based Question Generation
status: done
created: 2026-04-14
completed: 2026-04-14
epic_id: epic-2
---

# Story 2.3: Case-Based Question Generation

## Story

**As a** content creator,
**I want** to generate case-based questions with passages,
**So that** I can create application-level questions for NEET.

## Acceptance Criteria

**Given** a valid exam and subject is specified
**When** I run `biopress generate --exam NEET --subject Biology --type case-based --count 3`
**Then** I receive 3 case-based questions
**And** each includes: a passage (paragraph), 2-5 sub-questions based on the passage
**And** answers to all sub-questions are provided

## Tasks

- [x] Implement case-based question generator module
- [x] Create passage generator with context
- [x] Implement sub-question generator linked to passage
- [x] Support Biology case-based (most common)
- [x] Support Physics case-based
- [x] Support Chemistry case-based
- [x] Add passage validation for coherence
- [x] Add tests for case-based generation
- [x] Verify sub-question relevance to passage

## Dev Agent Record

### Implementation Plan

**Architecture Requirements:**

- Used generator module pattern from previous stories
- Created multi-part question structure for case-based
- Followed Perseus JSON extended format
- Integrated with LLM adapter for passage generation

**Technical Decisions:**

- Case-based generator: `src/biopress/generators/case_based.py`
- Passage templates: `src/biopress/generators/templates/case_based/`
- Sub-question linker: links sub-questions to passage context

### Debug Log

No issues encountered.

### Completion Notes

Implemented case-based question generation with:

- Passage generation with rich context
- 2-5 sub-questions per passage
- Support for Biology, Physics, and Chemistry
- Sub-questions properly linked to passage context
- Complete answer keys for all sub-questions

## File List

- `src/biopress/generators/case_based.py` - Case-based generator
- `src/biopress/generators/templates/case_based/` - Perseus templates
- `tests/test_case_based.py` - Tests (all passing)

## Change Log

- 2026-04-14: Initial implementation of case-based question generation
