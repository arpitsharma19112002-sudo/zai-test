---
story_id: 6-3
story_key: 6-3-text-correction-in-editor
title: Text Correction in Editor
status: done
created: 2026-04-14
completed: 2026-04-14
epic_id: epic-6
---

# Story 6.3: Text Correction in Editor

## Story

**As a** user reviewing a PDF,
**I want** to correct any text errors directly in the editor,
**So that** I can fix mistakes without regenerating the entire PDF.

## Acceptance Criteria

**Given** I have a PDF open in visual review
**When** I click on text to select it
**Then** an inline editor appears
**And** I can edit and save the correction
**And** the change is reflected in the PDF

## Tasks

- [x] Add text selection functionality
- [x] Implement inline text editor
- [x] Save corrections to source data
- [x] Regenerate PDF with corrections

## File List

- Modified: `src/biopress/cli/commands/review.py` - Added text correction

## Change Log

- 2026-04-14: Implemented text correction in editor
