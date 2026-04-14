---
story_id: 6-5
story_key: 6-5-diagram-replacement
title: Diagram Replacement
status: done
created: 2026-04-14
completed: 2026-04-14
epic_id: epic-6
---

# Story 6.5: Diagram Replacement

## Story

**As a** user reviewing questions with diagrams,
**I want** to replace or remove diagrams,
**So that** I can update visual content when needed.

## Acceptance Criteria

**Given** I have a question with a diagram in the editor
**When** I switch to the Diagram tab
**Then** I see the current diagram path/URL
**And** I can enter a new path or URL
**And** I can browse for a file
**And** I can clear the diagram
**And** the diagram is saved with the question

## Tasks

- [x] Add Diagram tab to editor tab panel
- [x] Display current diagram path/URL
- [x] Add input field for new diagram path
- [x] Add browse button for file selection
- [x] Add clear button to remove diagram
- [x] Save diagram with question

## File List

- Modified: `src/biopress/visual/pages/editor.py` - Added diagram replacement UI in tab

## Change Log

- 2026-04-14: Implemented diagram replacement with browse and clear functionality
