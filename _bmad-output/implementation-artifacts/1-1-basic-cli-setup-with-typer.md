---
story_id: 1-1
story_key: 1-1-basic-cli-setup-with-typer
title: Basic CLI Setup with Typer
status: review
created: 2026-04-14
completed: 2026-04-14
epic_id: epic-1
---

# Story 1.1: Basic CLI Setup with Typer

## Story

**As a** CLI user,
**I want** to run `biopress --help` and see all available commands,
**So that** I can understand what the tool can do.

## Acceptance Criteria

**Given** the biopress package is installed
**When** I run `biopress --help`
**Then** I see a help message with all available commands (generate, validate, review, export, config, kb)
**And** each command has a brief description
**And** `--version` flag shows current version

## Tasks

- [x] Set up project structure (pyproject.toml, src/biopress/)
- [x] Create main Typer app with subcommands
- [x] Implement help command with all subcommands listed
- [x] Implement version flag
- [x] Create generate, validate, review, export, config, kb subcommands (stubs)
- [x] Add tests for CLI commands
- [x] Verify --help and --version work

## Dev Agent Record

### Implementation Plan

**Architecture Requirements:**

- Used Typer for CLI framework
- Used Pydantic for configuration models
- Followed project structure from architecture.md

**Technical Decisions:**

- Main entry point: `src/biopress/cli/app.py`
- Subcommands in: `src/biopress/cli/commands/`

### Debug Log

No issues encountered.

### Completion Notes

Implemented the complete CLI foundation with:

- Main app with 6 subcommands: generate, validate, review, export, config, kb
- Version flag (`--version`) showing "BioPress Designer version 0.1.0"
- All subcommands have help documentation
- 8 unit tests all passing

## File List

- `pyproject.toml` - Package configuration
- `README.md` - Project documentation
- `src/biopress/__init__.py` - Package init
- `src/biopress/__version__.py` - Version file
- `src/biopress/cli/__init__.py` - CLI module init
- `src/biopress/cli/app.py` - Main CLI app
- `src/biopress/cli/commands/__init__.py` - Commands module
- `src/biopress/cli/commands/generate.py` - Generate command stub
- `src/biopress/cli/commands/validate.py` - Validate command stub
- `src/biopress/cli/commands/review.py` - Review command stub
- `src/biopress/cli/commands/export.py` - Export command stub
- `src/biopress/cli/commands/config.py` - Config command stub
- `src/biopress/cli/commands/kb.py` - KB command stub
- `tests/__init__.py` - Test package init
- `tests/test_cli.py` - CLI tests (8 tests)

## Change Log

- 2026-04-14: Initial implementation of CLI foundation with all subcommands and tests
