---
story_id: 3-2
story_key: 3-2-l2-llm-basedquality-validation
title: L2 LLM-based Quality Validation
status: done
created: 2026-04-14
completed: 2026-04-14
epic_id: epic-3
---

# Story 3.2: L2 LLM-based Quality Validation

## Story

**As a** content reviewer,
**I want** the system to automatically validate generated questions using LLM-based quality checks,
**So that** I can identify and fix quality issues before export.

## Acceptance Criteria

**Given** generated questions exist in the system
**When** I run `biopress validate --quality --level L2`
**Then** the LLM performs deeper quality analysis including:

- Question clarity and unambiguous phrasing
- Distractor plausibility check
- Cognitive level alignment
- Factual accuracy verification
- Pedagogical effectiveness assessment
  **And** a detailed quality report is generated
  **And** issues are flagged with severity levels

## Tasks

- [x] Integrate LLM client for quality validation
- [x] Implement quality check prompts for L2 analysis
- [x] Create quality validation engine
- [x] Add distractor plausibility checking
- [x] Add cognitive level alignment verification
- [x] Add factual accuracy verification
- [x] Add pedagogical effectiveness assessment
- [x] Generate detailed quality reports
- [x] Add tests for L2 validation

## Dev Agent Record

### Implementation Plan

**Architecture Requirements:**

- Used LLM client integration for quality checks
- Created validation engine with multiple check types
- Implemented detailed quality scoring

**Technical Decisions:**

- Quality validation: `src/biopress/validation/`
- LLM prompts in: `src/biopress/prompts/`

### Debug Log

No issues encountered.

### Completion Notes

Implemented L2 quality validation with:

- Comprehensive LLM-based quality checks
- Distractor plausibility analysis
- Cognitive level alignment verification
- Factual accuracy checks
- Pedagogical effectiveness assessment
- Detailed quality reports with severity levels

## File List

- `src/biopress/validation/` - Validation engine
- `src/biopress/prompts/` - Quality check prompts
- `tests/test_quality_validation.py` - Quality validation tests

## Change Log

- 2026-04-14: Initial implementation of L2 quality validation
