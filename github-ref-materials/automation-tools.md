# Automation Tools & Hidden Features

As of April 13, 2026, the most effective "hidden tools" (advanced, lesser-known, or tucked-away features/configs inside your GitHub repo) that run in full **auto mode** to slash workload for documentation, prompts library, development plans, roadmaps, dev logs, and project tracking are a mix of native GitHub capabilities and tightly integrated AI-powered extensions. These build directly on the folder structure + Issues + Projects setup outlined earlier. They make your repo largely self-managing: changes to code/docs automatically update plans, prompts get versioned/reviewed, issues auto-triage into projects, and reports generate themselves.

The goal: zero manual copying, minimal clicking, and proactive maintenance. Everything stays 100% inside (or synced to) the repo, with Git history as the audit trail.

---

## 1. GitHub Native "Hidden" Automations (All Inside Your Repo – No Extra Tools)

These live in `.github/` or the Projects UI and are often overlooked ("hidden") but incredibly powerful once enabled.

### GitHub Projects Built-in Automations (Best "Hidden" Project Manager)

**What it does in auto mode:**
- Auto-add issues/PRs/Discussions to your board based on labels, keywords, or assignees.
- Auto-move cards across columns (To Do → In Progress → Done) when PRs merge or statuses change.
- Auto-set custom fields (e.g., "Sprint", "Prompt-Version", "Effort").
- Auto-archive completed items.
- Auto-generate charts/velocity reports.

**How it reduces workload:**
No more dragging cards or updating spreadsheets. Your `docs/plans/`, `docs/prompts/experiments/`, and dev-logs auto-flow into the board.

**Setup (2 minutes):**
1. Open your Project → Settings → Workflows.
2. Turn on "Add items automatically" (filter: label `type:task` or `docs` or `prompt-experiment`).
3. Create rules like: "When PR is merged → move to Done + set Status = Completed".
4. Add custom fields (Priority, AI-Model-Used, Prompt-Version) and auto-populate them.

**2026 nuance:**
Integrates with iteration fields (week-by-week sprints) and hierarchy views for nested plans/roadmaps. Works perfectly with your `docs/` structure.

**Edge case:**
For very large repos, combine with labels like `auto:docs` to prevent noise.

---

### GitHub Actions + Marketplace (The Real "Auto Mode" Engine in `.github/workflows/`)

**Key hidden gems:**
- Auto-generate `CHANGELOG.md` from conventional commits (actions like `BobAnkh/auto-generate-changelog` or `requarks/changelog-action`).
- Auto-update docs/TOC on push (TOC Generator, GitHub Actions Auto-Docs).
- Auto-create issues from TODOs in code/docs/prompts.
- Auto-label and assign prompt experiments.

**Workload win:**
Push code or update a prompt → changelog, roadmap snippet, and project card all update automatically. No more manual release notes.

**Quick start example (for your prompts & plans):**

```yaml
# .github/workflows/auto-changelog.yml
name: Auto Changelog & Docs
on: push
  branches: [main]
jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: BobAnkh/auto-generate-changelog@v1  # or semantic-release
        with: path: CHANGELOG.md
      - name: Update prompts index
        run: python docs/prompts/generate-index.py  # custom script
```

**2026 status:**
Actions now have better security roadmaps (workflow-level locking, policy-driven execution) so you can run these safely at scale.

---

### Automatic Release Notes (`.github/release.yml`)

Auto-generates release notes with PR links, contributors, and categorized changelog. Perfect for your `ROADMAP.md` updates.

---

## 2. 2026 Breakthrough: GitHub Agentic Workflows (The Ultimate "Auto Mode" Tool)

This is the newest "hidden" powerhouse (technical preview since Feb 2026) that turns plain-English instructions into fully autonomous repo maintenance.

**What it is:**
You write a Markdown file describing intent ("Keep all prompts in docs/prompts/ up-to-date and summarized"), and AI agents (Copilot CLI, Claude Code, etc.) execute it as a GitHub Action. Runs on schedule, on issue creation, or manually.

**Auto-mode magic for your use case:**
- Daily/weekly status reports on project progress, prompt experiments, roadmap health.
- Auto-triage new prompt issues → label, summarize results, move to Projects board.
- Continuous documentation: "When code changes, update architecture docs and flag outdated prompts".
- Prompt library hygiene: "Review experiments folder, suggest improvements, create PR".

**Setup (5-10 minutes):**
1. Install `gh` extension: `gh extension install github/gh-aw`.
2. Create `daily-prompts-report.md` in `.github/workflows/` with YAML frontmatter + natural language instructions.
3. Run `gh aw compile` → generates locked workflow.
4. Commit & push. Add any needed secrets (agent API keys).
5. Trigger: schedule daily or on `issues:opened`.

**Example prompt in the Markdown:**

```
# Daily Prompts & Plans Health
Create a report on docs/prompts/experiments/.
Include recent results, performance trends, and actionable next steps.
Open a PR if any prompt needs versioning update.
```

**Workload reduction:**
Replaces hours of manual review with one file that runs forever. Human only approves final PRs.

**Nuances/edge cases:**
- Read-only by default (safe). Write ops need approval.
- Costs: Uses Copilot premium requests (2 per run). Fine for solo; monitor in enterprise.
- Best for judgment-based tasks (not pure CI/CD).

---

## 3. GitHub Copilot Hidden Configs & Agents (Repo-Level AI That "Knows" Your Docs/Prompts)

Copilot in 2026 is far beyond autocomplete.

**Hidden config files** (drop these in your repo):
- `.github/copilot-instructions.md` (or `.github/copilot/*.instructions.md`): Global rules like "Always version prompts with YAML frontmatter, link experiments to issues, use Diátaxis structure in docs/".
- **Copilot Spaces**: Create a Space pointing to `docs/`, `prompts/`, and your Projects board → Copilot now has perfect context for plans and prompts.

**Agent features:**
- Copilot Cloud Agent / Edits (Agent Mode): Assign an issue like "Summarize this prompt experiment" and it researches the whole repo, updates files, opens PR.
- Memory (public preview): Remembers your repo-specific patterns across sessions.

**Workload win:**
Ask Copilot in the repo "Update roadmap from latest sprint" → it does it. Or "Generate prompt template for new feature" → stores it automatically.

---

## 4. Bidirectional Git-Synced Docs Tools (For Non-Dev Team Members)

If you want non-technical people (PMs, writers) to edit without touching Git:

**GitBook (top recommendation in 2026):**
Two-way sync with your `docs/` folder. Engineers PR Markdown → GitBook updates instantly. PMs edit visually in browser → GitHub updates. Built-in AI Assistant for prompts/docs. Auto-generates `llms.txt` for AI consumption.

**Workload impact:**
Zero sync meetings or copy-paste. Your prompts library and roadmap stay perfectly in sync.

---

## 5. Overall Best Combo for Your Setup (Minimal Workload)

| Layer | Tools |
|-------|-------|
| **Core** | Projects + built-in automations (daily tracking) |
| **Docs & Prompts** | GitBook sync + Copilot instructions + Agentic Workflows (auto-maintenance) |
| **Plans & Logs** | Actions for changelog/TOC + Agentic daily reports |
| **Everything else** | Issue templates that force structured prompt data |

---

## Implications & Edge Cases (2026 Reality)

| Scenario | Approach |
|----------|----------|
| **Solo vs Team** | Solo → Agentic + Copilot = near-zero admin. Team → add approvals & policies. |
| **Cost** | Free tier sufficient for most; Agentic/Copilot = usage-based (monitor via GitHub metrics). |
| **Security/Privacy** | Everything stays in-repo (or private GitBook). Use read-only agents first. |
| **Scalability** | Starts simple; scales to monorepos via repository rulesets and custom properties. |
| **Fallback** | If Agentic feels too new, start with classic Actions + Projects automations — still 80% workload reduction. |

---

## Quick Win Today

1. Enable Projects automations
2. Add `.github/copilot-instructions.md`
3. Add one Agentic workflow for daily reports

You'll immediately see the difference.

---

*These tools evolve fast — Agentic Workflows especially — so this is the state-of-the-art on April 13, 2026.*
