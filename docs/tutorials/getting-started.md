# Getting Started Tutorial

Welcome! This tutorial will help you set up your development environment and understand the project structure.

---

## Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** (v18 or higher) - [Download](https://nodejs.org/)
- **Git** - [Download](https://git-scm.com/)
- **A code editor** - VS Code recommended

### Verify Installations

```bash
node --version  # Should show v18.x or higher
git --version   # Should show git version
```

---

## Learning Objectives

By the end of this tutorial, you will:

- ✅ Clone and set up the project locally
- ✅ Understand the directory structure
- ✅ Install dependencies
- ✅ Run the project locally
- ✅ Know where to find documentation

---

## Step 1: Clone the Repository

First, clone the repository to your local machine:

```bash
# Using HTTPS
git clone https://github.com/arpitsharma19112002-sudo/zai-test.git

# Or using SSH (if you have SSH keys set up)
git clone git@github.com:arpitsharma19112002-sudo/zai-test.git

# Navigate into the project
cd zai-test
```

---

## Step 2: Understand the Structure

Let's explore the project structure:

```bash
# View the structure
tree -L 2
```

You should see:

```
zai-test/
├── README.md          # Start here!
├── docs/              # All documentation
│   ├── tutorials/     # Learning guides (you are here)
│   ├── how-to/        # Task-oriented guides
│   └── prompts/       # AI prompt management
├── src/               # Source code
├── tests/             # Test files
└── .github/           # GitHub templates
```

### Key Directories

| Directory | Purpose |
|-----------|---------|
| `docs/` | All project documentation |
| `src/` | Application source code |
| `tests/` | Test files |
| `.github/` | Issue templates, workflows |

---

## Step 3: Install Dependencies

Install the project dependencies:

```bash
# Using npm
npm install

# Or using yarn
yarn install

# Or using pnpm
pnpm install
```

---

## Step 4: Explore the Documentation

The `docs/` folder is your knowledge hub:

1. **[docs/index.md](../index.md)** - Navigation hub for all docs
2. **[docs/tutorials/](./)** - Learning-oriented guides (like this one)
3. **[docs/how-to/](../how-to/)** - Task-oriented guides
4. **[docs/prompts/](../prompts/)** - AI prompt library

---

## Step 5: Run the Project

Start the development server:

```bash
# Development mode
npm run dev

# Or build for production
npm run build
npm start
```

---

## Summary

Congratulations! You've successfully:

- ✅ Cloned the repository
- ✅ Explored the project structure
- ✅ Installed dependencies
- ✅ Located key documentation
- ✅ Started the development server

---

## Next Steps

Now that you're set up, here are some recommended next steps:

1. **Read the [README](../../README.md)** for project overview
2. **Browse [How-To Guides](../how-to/)** for specific tasks
3. **Check [Contributing Guidelines](../../CONTRIBUTING.md)** to contribute
4. **Explore the [Prompt Library](../prompts/)** for AI-assisted development

---

## Need Help?

- Check the [documentation](../index.md)
- Open an [issue](https://github.com/arpitsharma19112002-sudo/zai-test/issues)
- Review [FAQ](../reference/faq.md) (if available)
