---
story_id: 5-1
story_key: 5-1-progress-indicator-during-generation
title: Progress Indicator During Generation
status: done
created: 2026-04-14
completed: 2026-04-14
epic_id: epic-5
---

# Story 5.1: Progress Indicator During Generation

## Story

**As a** user generating multiple questions,
**I want** to see a progress indicator during question generation,
**So that** I know the system is working and can estimate time remaining.

## Acceptance Criteria

**Given** I have started a question generation command
**When** the generation is processing multiple items
**Then** I see a progress bar or percentage indicator
**And** the indicator updates in real-time
**And** I can see which item is currently being processed

## Tasks

- [x] Add progress indicator library (tqdm or rich)
- [x] Integrate progress bar into question generation pipeline
- [x] Show current item count / total count
- [x] Update progress in real-time during generation
- [x] Handle keyboard interrupt gracefully

## File List

- Modified: `src/biopress/cli/commands/generate.py` - Added progress indicator

## Change Log

- 2026-04-14: Implemented progress indicator with tqdm
