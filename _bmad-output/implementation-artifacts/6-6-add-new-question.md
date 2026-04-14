---
story_id: 6-6
story_key: 6-6-add-new-question
title: Add New Question
status: done
created: 2026-04-14
completed: 2026-04-14
epic_id: epic-6
---

# Story 6.6: Add New Question

## Story

**As a** user editing a quiz,
**I want** to add new questions,
**So that** I can expand the question set.

## Acceptance Criteria

**Given** I have content loaded in the editor
**When** I click the add button (+ icon) in the toolbar
**Then** a new question is added to the end of the list
**And** the editor switches to the new question
**And** the new question has default placeholder values
**And** I can edit and save the new question

## Tasks

- [x] Add new question button in editor toolbar
- [x] Create new question with default values
- [x] Append to items list
- [x] Set selected index to new question
- [x] Trigger save callback

## File List

- Modified: `src/biopress/visual/pages/editor.py` - Added add new question functionality

## Change Log

- 2026-04-14: Implemented add new question with default template values
