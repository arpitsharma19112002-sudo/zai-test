---
story_id: 7-4
story_key: 7-4-kb-update-and-sync
title: KB Update and Sync
status: done
created: 2026-04-14
completed: 2026-04-14
epic_id: epic-7
---

# Story 7.4: KB Update and Sync

## Story

**As a** user,
**I want** to update and sync the knowledge base,
**So that** I can keep content current across multiple sources.

## Acceptance Criteria

**Given** a rules file (JSON) and sync directory
**When** I run `kb update --rules file.json --sync-dir dir`
**Then** topics can be updated individually
**And** syllabi can be synced from external directories
**And** version comparison is available
**And** last-modified timestamps are tracked

## Tasks

- [x] Add save_syllabus() method to loader
- [x] Add update_topic() method to loader
- [x] Add sync_from_directory() method to loader
- [x] Add get_last_modified() method to loader
- [x] Add compare_versions() method to loader
- [x] Add update command to CLI
- [x] Write tests for sync functionality

## File List

- Modified: `src/biopress/kb/loader.py` - Added sync and update methods
- Modified: `src/biopress/cli/commands/kb.py` - Added update command

## Change Log

- 2026-04-14: Added save, update, sync functionality to loader
- 2026-04-14: Added version comparison and last-modified tracking
- 2026-04-14: Added CLI update command
