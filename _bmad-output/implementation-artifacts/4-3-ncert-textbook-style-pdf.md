---
story_id: 4-3
story_key: 4-3-ncert-textbook-style-pdf
title: NCERT Textbook Style PDF
status: done
created: 2026-04-14
completed: 2026-04-14
epic_id: epic-4
---

# Story 4.3: NCERT Textbook Style PDF

## Story

**As a** textbook author,
**I want** to export questions in NCERT textbook format,
**So that** I can include them as chapter-end exercises.

## Acceptance Criteria

**Given** questions are organized by chapter/topic
**When** I run `biopress export pdf --style ncert --output textbook.pdf`
**Then** a PDF is generated with:

- Chapter-wise question organization
- NCERT typography (proper serif fonts)
- Section headers for each chapter
- Question numbering by chapter
- Includes "Solutions" section at end
- Proper textbook formatting and layout

## Tasks

- [x] Implement chapter-wise organization
- [x] Apply NCERT typography (serif fonts)
- [x] Add section headers for chapters
- [x] Implement chapter-based question numbering
- [x] Create solutions section
- [x] Add textbook layout formatting
- [x] Add tests for NCERT style
- [x] Verify NCERT format compliance

## Dev Agent Record

### Implementation Plan

**Architecture Requirements:**

- Extended PDF generator with NCERT template
- Implemented chapter organization
- Added textbook typography

**Technical Decisions:**

- NCERT template: `src/biopress/export/templates/ncert.py`
- Chapter manager: `src/biopress/export/chapters.py`

### Debug Log

No issues encountered.

### Completion Notes

Implemented NCERT textbook style with:

- Chapter-wise question organization
- NCERT typography (serif fonts)
- Section headers for each chapter
- Question numbering by chapter
- Complete solutions section
- Professional textbook formatting

## File List

- `src/biopress/export/templates/ncert.py` - NCERT template
- `src/biopress/export/chapters.py` - Chapter manager
- `tests/test_ncert_style.py` - NCERT style tests

## Change Log

- 2026-04-14: Initial implementation of NCERT textbook style PDF
