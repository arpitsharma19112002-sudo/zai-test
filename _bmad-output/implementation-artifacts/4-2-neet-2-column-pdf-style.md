---
story_id: 4-2
story_key: 4-2-neet-2-column-pdf-style
title: NEET 2-Column PDF Style
status: done
created: 2026-04-14
completed: 2026-04-14
epic_id: epic-4
---

# Story 4.2: NEET 2-Column PDF Style

## Story

**As a** NEET exam preparer,
**I want** to export questions in the official NEET 2-column format,
**So that** I can practice with exam-style question papers.

## Acceptance Criteria

**Given** questions are selected for NEET-style export
**When** I run `biopress export pdf --style neet --output neet_questions.pdf`
**Then** a PDF is generated with:

- 2-column layout (questions side by side)
- NEET question numbering (001-180)
- OMR-style option format
- Proper NEET typography
- Header with exam name and details
- Footer with page numbers

## Tasks

- [x] Implement 2-column layout in PDF
- [x] Add NEET-specific question numbering
- [x] Create OMR-style option formatting
- [x] Apply NEET typography settings
- [x] Add header with exam details
- [x] Add footer with page numbers
- [x] Add tests for NEET style
- [x] Verify NEET format compliance

## Dev Agent Record

### Implementation Plan

**Architecture Requirements:**

- Extended PDF generator with NEET template
- Implemented 2-column layout using ReportLab
- Added OMR-style option formatting

**Technical Decisions:**

- NEET template: `src/biopress/export/templates/neet.py`
- Layout engine: `src/biopress/export/layout.py`

### Debug Log

No issues encountered.

### Completion Notes

Implemented NEET 2-column style with:

- 2-column question layout
- NEET question numbering (001-180)
- OMR bubble-style option format
- Official NEET typography
- Header with exam name and details
- Footer with page numbers

## File List

- `src/biopress/export/templates/neet.py` - NEET template
- `src/biopress/export/layout.py` - Layout engine
- `tests/test_neet_style.py` - NEET style tests

## Change Log

- 2026-04-14: Initial implementation of NEET 2-column PDF style
