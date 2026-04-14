---
story_id: 2-2
story_key: 2-2-numerical-question-generation
title: Numerical Question Generation
status: done
created: 2026-04-14
completed: 2026-04-14
epic_id: epic-2
---

# Story 2.2: Numerical Question Generation

## Story

**As a** content creator,
**I want** to generate numerical questions with calculations,
**So that** students can practice problem-solving skills.

## Acceptance Criteria

**Given** a valid exam and subject is specified
**When** I run `biopress generate --exam NEET --subject Physics --type numerical --count 5 --topic "Kinematics"`
**Then** I receive 5 numerical questions
**And** each question includes: problem statement, numerical answer, step-by-step solution
**And** numerical values are mathematically correct

## Tasks

- [x] Implement numerical question generator module
- [x] Create Perseus template for numerical questions
- [x] Add SymPy integration for answer verification
- [x] Implement step-by-step solution generator
- [x] Support Physics numerical topics
- [x] Support Chemistry numerical topics
- [x] Add unit validation
- [x] Add tests for numerical generation
- [x] Verify mathematical correctness

## Dev Agent Record

### Implementation Plan

**Architecture Requirements:**

- Used generator module pattern from Story 2.1
- Used Perseus JSON template system
- Integrated SymPy for mathematical validation
- Followed multi-LLM adapter pattern

**Technical Decisions:**

- Numerical generator: `src/biopress/generators/numerical.py`
- Templates: `src/biopress/generators/templates/numerical/`
- SymPy validator: `src/biopress/validators/sympy_validator.py`

### Debug Log

No issues encountered.

### Completion Notes

Implemented numerical question generation with:

- Support for Physics and Chemistry numerical questions
- Step-by-step solution generation with proper units
- SymPy-based answer verification
- Unit conversion and validation
- Template-based generation for token optimization

## File List

- `src/biopress/generators/numerical.py` - Numerical generator
- `src/biopress/generators/templates/numerical/` - Perseus templates
- `src/biopress/validators/sympy_validator.py` - SymPy validator
- `tests/test_numerical.py` - Tests (all passing)

## Change Log

- 2026-04-14: Initial implementation of numerical question generation
