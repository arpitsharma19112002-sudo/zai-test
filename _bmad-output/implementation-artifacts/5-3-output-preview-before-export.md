---
story_id: 5-3
story_key: 5-3-output-preview-before-export
title: Output Preview Before Export
status: done
created: 2026-04-14
completed: 2026-04-14
epic_id: epic-5
---

# Story 5.3: Output Preview Before Export

## Story

**As a** user,
**I want** to preview the generated content before exporting,
**So that** I can review and make corrections if needed.

## Acceptance Criteria

**Given** I have generated questions
**When** I use the `--preview` flag
**Then** I see a preview of the output in the terminal
**And** I can choose to proceed or cancel
**And** I can export after confirmation

## Tasks

- [x] Add `--preview` flag to generate command
- [x] Preview output in formatted table/list
- [x] Add confirmation prompt before export
- [x] Allow abort without saving

## File List

- Modified: `src/biopress/cli/commands/generate.py` - Added preview flag

## Change Log

- 2026-04-14: Implemented output preview before export
