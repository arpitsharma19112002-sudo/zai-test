# Repository Structure & Project Management

The best way to structure and manage software development documentation, plans, prompts (including AI prompts), development logs, and overall project tracking entirely *within* a single GitHub repository is a hybrid approach that combines:

1. **A clean, version-controlled folder structure** (Markdown files for everything that needs to be searchable, diffable, and historically tracked).
2. **GitHub's native built-in project management tools** (Issues + Projects + Milestones + Discussions + Templates).

This gives you a full-featured, zero-extra-tool project manager that lives 100% inside your repo—no Jira, Notion, or Trello required. Everything stays in Git history, is searchable via GitHub's UI/search, and scales from solo developers to teams.

---

## 1. Recommended Repository Folder Structure (Docs-First Focus)

GitHub's own best practices and community standards (Diátaxis framework, common open-source templates) recommend keeping documentation close to the code so it is versioned together and easy to maintain.

Here is a battle-tested structure optimized for documentation + project management:

```
your-repo/
├── README.md                  # Single source of truth: what, why, how-to-get-started, quick links
├── LICENSE
├── CHANGELOG.md               # Auto-generated or manually kept (use conventional commits)
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── ROADMAP.md                 # High-level vision & milestones (or move to docs/roadmap/)
├── .github/
│   ├── ISSUE_TEMPLATE/        # .md files for Bug, Feature, AI-Prompt-Experiment, etc.
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows/             # CI/CD + optional automation (e.g., auto-add issues to project)
├── docs/                      # ← Core documentation hub (everything else lives here)
│   ├── index.md               # Table of contents / navigation hub
│   ├── architecture/          # Design decisions, diagrams (PlantUML/Mermaid)
│   ├── development/
│   │   ├── decision-logs/     # ADR (Architecture Decision Records)
│   │   ├── meeting-notes/
│   │   └── dev-logs/          # Daily/weekly development journal
│   ├── plans/
│   │   ├── roadmap/
│   │   ├── sprints/           # sprint-2026-04.md etc.
│   │   └── backlog.md
│   ├── prompts/               # ← Dedicated folder for AI prompts (highly recommended)
│   │   ├── system-prompts/
│   │   ├── prompt-library/
│   │   │   ├── code-generation/
│   │   │   ├── debugging/
│   │   │   └── documentation.md
│   │   ├── experiments/       # Prompt v1 vs v2 results, performance notes
│   │   └── templates/
│   ├── tutorials/             # Learning-oriented (Diátaxis)
│   ├── how-to/                # Goal-oriented guides
│   ├── reference/             # API, config, specs
│   └── images/                # Screenshots, diagrams (kept versioned)
├── src/ or app/               # Your actual code
├── tests/
└── .gitignore
```

### Why this structure works:

- All documentation is Markdown → GitHub renders it beautifully.
- `docs/` is the single place new contributors look first.
- `prompts/` keeps AI experimentation versioned and reusable (critical if you use Grok, Claude, GPT, etc.).
- Everything is searchable with GitHub's code search (`docs/ prompts/ roadmap`).
- You can generate a static docs site later (MkDocs, Docusaurus, GitHub Pages) without moving files.

Add a small `PROJECT_STRUCTURE.md` or section in README.md that explains this layout—onboarding becomes instant.

---

## 2. GitHub's Built-in Project Manager (Issues + Projects)

This is the "project manager tool built within the repo". GitHub Projects (the modern version, not the old classic boards) is designed exactly for this.

### Setup (takes < 5 minutes):

1. Go to your repo → **Projects** tab → **New project**.
2. Choose a template: "Board", "Table", or "Roadmap".
3. Name it (e.g., "Product Backlog", "AI Development", "Q2 2026 Sprint").
4. Enable **Auto-add** workflow (in project settings): any new issue with label `type:task` or `priority:high` is automatically added.
5. Add custom fields: Status, Priority, Effort (story points), Sprint, AI-Model-Used, Prompt-Version, etc.

### Views you will use daily:

- **Board** → Kanban (To Do → In Progress → Review → Done).
- **Table** → Spreadsheet-like with filters/sorts.
- **Roadmap** → Gantt-style timeline for plans & milestones.
- **Charts** → Burndown, velocity, etc. (built-in).

### Linking everything together:

- Every task, bug, feature, or AI-prompt experiment = a GitHub **Issue**.
- Use issue templates so every prompt-related issue has fields: "Prompt used", "Model", "Temperature", "Result", "Lessons learned".
- Reference docs files directly in issues: `See docs/prompts/experiments/prompt-v3.md`.
- Link issues to PRs automatically (GitHub does this).
- Milestones = Sprints or releases.
- Discussions = Brainstorming sessions or "prompt idea" threads.

### Automation tips (all inside the repo):

- GitHub Actions can auto-label, move cards, or post status updates.
- Use labels: `docs`, `prompt-experiment`, `planning`, `bug`, `enhancement`, `ai-generated`.
- Conventional commits + `CHANGELOG.md` keep development history clean.

---

## 3. Specific Handling for "Prompts, Developments, Plans"

### AI Prompts
Treat them as first-class artifacts. Store in `docs/prompts/` with clear filenames and front-matter YAML (title, version, date, model, performance score). Version them like code. Reference the exact prompt file in every related issue/PR. This solves the common "I can't remember which prompt gave me that great result" problem.

### Development Plans & Roadmaps
Keep high-level in `ROADMAP.md` or `docs/plans/`. Break down into issues + project roadmap view. Update the Markdown file after each sprint (keeps Git history).

### Development Logs / Meeting Notes
`docs/development/dev-logs/YYYY-MM.md` or use Issues with label `type:log`. For quick notes, GitHub Discussions works well and can be converted to issues later.

### Decision Records
Use lightweight ADRs in `docs/development/decision-logs/adr-001.md` (template widely available).

---

## 4. Best Practices & Nuances

### Keep it lightweight
Start with one project and one `docs/` folder. Split into multiple projects only when the repo grows very large (e.g., separate "AI Experiments" project).

### Team vs Solo
For solo, still use Issues/Projects—it becomes your personal knowledge base. For teams, add `@mentions` and required reviewers.

### Edge cases:

- **Very large monorepo** → Use sub-folders + repository topics/labels for filtering.
- **Private vs public** → Same structure works; just control visibility.
- **AI-heavy projects** → Add a `prompts/` folder + custom fields for model/version/performance.
- **Compliance/audit needs** → Everything is in Git → perfect audit trail.

### Common pitfalls to avoid:

- Don't scatter plans across Notion/Google Docs (breaks the "within repo" rule).
- Don't put large binary files (videos, big PDFs) in the repo—use Git LFS or links.
- Keep README.md concise; detailed docs go in `docs/`.

---

## 5. Real-World Examples & Implications

Many successful open-source and internal projects follow exactly this pattern:

- GitHub's own repos, Vercel, NestJS, Astro, and thousands of ML/AI repos use `docs/` + Issues + Projects.
- The Diátaxis framework (Tutorials / How-to / Reference / Explanation) inside `docs/` is now the de-facto standard for developer documentation.

### Implications of doing it this way:

- **Onboarding**: New contributor opens the repo → README → `docs/index.md` → project board → instantly knows status and next steps.
- **Maintainability**: Documentation and plans evolve with the code (same PRs).
- **Searchability & History**: Git blame on a prompt file shows exactly when/why it changed.
- **Scalability**: Starts simple, grows without tool switching.
- **Zero cost**: No extra SaaS subscriptions.

---

## Quick Start Checklist

1. Create the folder structure above.
2. Add issue & PR templates in `.github/`.
3. Create your first GitHub Project and turn on auto-add.
4. Move any existing plans/prompts into `docs/`.
5. Update README.md with links to the project board and docs.

---

This setup turns your GitHub repo into a complete, self-contained project management + documentation system. It is the approach used by most mature open-source projects and professional teams that want everything version-controlled and inside one repo.
