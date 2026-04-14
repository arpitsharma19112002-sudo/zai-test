---
story_id: 7-2
story_key: 7-2-kb-query-and-search
title: KB Query and Search
status: done
created: 2026-04-14
completed: 2026-04-14
epic_id: epic-7
---

# Story 7.2: KB Query and Search

## Story

**As a** user,
**I want** to query and search the knowledge base,
**So that** I can find specific topics and content quickly.

## Acceptance Criteria

**Given** a loaded knowledge base
**When** I run `kb search <query>` or `kb query --exam X`
**Then** I receive ranked results based on relevance
**And** I can filter by subject or topic ID
**And** results include topic details (name, weightage, difficulty)

## Tasks

- [x] Implement search() method in KBManager
- [x] Add scoring algorithm for relevance ranking
- [x] Add search command to CLI
- [x] Add query command to CLI (already exists)
- [x] Write tests for search functionality

## File List

- Modified: `src/biopress/kb/manager.py` - Added search() method
- Modified: `src/biopress/cli/commands/kb.py` - Added search command

## Change Log

- 2026-04-14: Implemented search functionality with relevance scoring
- 2026-04-14: Added CLI search command
