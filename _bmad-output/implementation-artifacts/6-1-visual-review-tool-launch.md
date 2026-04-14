---
story_id: 6-1
story_key: 6-1-visual-review-tool-launch
title: Visual Review Tool Launch
status: done
created: 2026-04-14
completed: 2026-04-14
epic_id: epic-6
---

# Story 6.1: Visual Review Tool Launch

## Story

**As a** user,
**I want** to launch a visual review tool for PDF documents,
**So that** I can visually inspect generated PDFs in a dedicated window.

## Acceptance Criteria

**Given** I have a generated PDF
**When** I run `biopress review --visual <file>`
**Then** a visual review window opens
**And** I can see the PDF content in a reader

## Tasks

- [x] Create new review visual command
- [x] Integrate PDF viewer library
- [x] Open PDF in dedicated window
- [x] Handle file not found error

## File List

- Added: `src/biopress/cli/commands/review.py` - Visual review command

## Change Log

- 2026-04-14: Implemented visual review tool launch
