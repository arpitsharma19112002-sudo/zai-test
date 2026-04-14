---
story_id: 7-3
story_key: 7-3-kb-bootstrapper
title: KB Bootstrapper
status: done
created: 2026-04-14
completed: 2026-04-14
epic_id: epic-7
---

# Story 7.3: KB Bootstrapper

## Story

**As a** user,
**I want** to bootstrap new exams from syllabus documents,
**So that** I can quickly populate the knowledge base.

## Acceptance Criteria

**Given** a syllabus document (text or JSON)
**When** I run `kb bootstrap --exam X --syllabus file.pdf`
**Then** the syllabus is parsed and KB entries are generated
**And** topics include name, subtopics, weightage
**And** patterns are extracted (MCQ count, duration, marks)

## Tasks

- [x] Create bootstrapper.py module
- [x] Implement text parsing for syllabus format
- [x] Implement JSON parsing for structured data
- [x] Add weightage extraction
- [x] Add pattern extraction
- [x] Add bootstrap command to CLI
- [x] Write tests for bootstrapper

## File List

- Added: `src/biopress/kb/bootstrapper.py` - New bootstrapper module
- Modified: `src/biopress/cli/commands/kb.py` - Added bootstrap command

## Change Log

- 2026-04-14: Created KB bootstrapper module
- 2026-04-14: Implemented text and JSON syllabus parsing
- 2026-04-14: Added CLI bootstrap command
