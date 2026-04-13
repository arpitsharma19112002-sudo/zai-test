# GitHub Reference Materials

This folder contains reference materials for using GitHub effectively for software development documentation, AI prompt management, development plans, and project tracking.

> **Note:** This is external reference material for learning purposes, not part of the project documentation itself.

---

## Contents

### 1. [Repository Structure & Project Management](./repo-structure-management.md)

**Topics covered:**
- Recommended repository folder structure (docs-first focus)
- GitHub's built-in project manager (Issues + Projects)
- Specific handling for prompts, developments, and plans
- Best practices and nuances
- Real-world examples and implications

**Key takeaways:**
- All documentation in Markdown → GitHub renders it beautifully
- `docs/` is the single place new contributors look first
- `prompts/` keeps AI experimentation versioned and reusable
- Everything is searchable with GitHub's code search

---

### 2. [Automation Tools & Hidden Features](./automation-tools.md)

**Topics covered:**
- GitHub Native "Hidden" Automations (Projects, Actions, Release Notes)
- GitHub Agentic Workflows (2026 breakthrough)
- GitHub Copilot Hidden Configs & Agents
- Bidirectional Git-Synced Docs Tools (GitBook)
- Overall best combo for minimal workload

**Key takeaways:**
- GitHub Projects built-in automations for auto-add and auto-move
- Actions for auto-changelog, auto-TOC, auto-issue creation
- Agentic Workflows for autonomous repo maintenance
- Copilot instructions and Spaces for context-aware AI

---

## Quick Reference

### Folder Structure Summary

```
your-repo/
├── README.md                  # Single source of truth
├── LICENSE
├── CHANGELOG.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── ROADMAP.md
├── .github/
│   ├── ISSUE_TEMPLATE/
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows/
├── docs/
│   ├── index.md
│   ├── architecture/
│   ├── development/
│   ├── plans/
│   ├── prompts/
│   ├── tutorials/
│   ├── how-to/
│   ├── reference/
│   └── images/
├── src/
├── tests/
└── .gitignore
```

### Automation Quick Win

1. Enable Projects automations
2. Add `.github/copilot-instructions.md`
3. Add one Agentic workflow for daily reports

---

*Last updated: April 13, 2026*
