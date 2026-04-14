---
story_id: 6-4
story_key: 6-4-question-fix-replace
title: Question Fix/Replace
status: done
created: 2026-04-14
completed: 2026-04-14
epic_id: epic-6
---

# Story 6.4: Question Fix/Replace

## Story

**As a** user reviewing questions,
**I want** to fix or replace entire questions,
**So that** I can correct major errors by replacing the whole question content.

## Acceptance Criteria

**Given** I have a question selected in the editor
**When** I click the replace button (refresh icon)
**Then** a dialog appears with all question fields
**And** I can enter new question, options, correct answer, and explanation
**And** clicking Replace updates the entire question
**And** the change is saved to the content

## Tasks

- [x] Add replace button in editor toolbar
- [x] Create replace dialog with all question fields
- [x] Implement replace logic to update entire question
- [x] Save changes after replacement

## File List

- Modified: `src/biopress/visual/pages/editor.py` - Added question replacement functionality

## Change Log

- 2026-04-14: Implemented question fix/replace with dialog UI
