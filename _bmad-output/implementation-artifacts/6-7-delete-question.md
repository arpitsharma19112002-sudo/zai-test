---
story_id: 6-7
story_key: 6-7-delete-question
title: Delete Question
status: done
created: 2026-04-14
completed: 2026-04-14
epic_id: epic-6
---

# Story 6.7: Delete Question

## Story

**As a** user editing a quiz,
**I want** to delete questions,
**So that** I can remove unwanted or duplicate questions.

## Acceptance Criteria

**Given** I have multiple questions in the editor
**When** I click the delete button (trash icon) in the toolbar
**Then** a confirmation dialog appears
**And** I can confirm or cancel the deletion
**When** I confirm deletion
**Then** the question is removed from the list
**And** the selected index is adjusted if needed
**And** I cannot delete the last remaining question

## Tasks

- [x] Add delete button in editor toolbar
- [x] Create confirmation dialog
- [x] Prevent deletion of last question
- [x] Remove question from list
- [x] Adjust selected index after deletion
- [x] Trigger save callback

## File List

- Modified: `src/biopress/visual/pages/editor.py` - Added delete question with confirmation

## Change Log

- 2026-04-14: Implemented delete question with confirmation dialog
