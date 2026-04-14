---
story_id: 5-2
story_key: 5-2-language-selection-at-start
title: Language Selection at Start
status: done
created: 2026-04-14
completed: 2026-04-14
epic_id: epic-5
---

# Story 5.2: Language Selection at Start

## Story

**As a** user generating bilingual content,
**I want** to select the output language at the start of generation,
**So that** I don't have to specify it for each question individually.

## Acceptance Criteria

**Given** I run a generation command
**When** I provide a `--language` flag at the start
**Then** all generated questions use that language
**And** the language selection applies to both question text and options

## Tasks

- [x] Add `--language` flag to generate command
- [x] Support English, Hindi, and Bilingual options
- [x] Pass language selection to generation pipeline
- [x] Store default language in config

## File List

- Modified: `src/biopress/cli/commands/generate.py` - Added language flag

## Change Log

- 2026-04-14: Implemented language selection at start
