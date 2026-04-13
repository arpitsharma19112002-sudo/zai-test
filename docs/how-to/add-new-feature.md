# How-To: Add a New Feature

This guide walks you through the process of adding a new feature to the project.

---

## Prerequisites

- Project set up locally (see [Getting Started](../tutorials/getting-started.md))
- Understanding of the project structure
- Git installed and configured

---

## Steps

### 1. Create an Issue

Before writing code, create a GitHub issue:

1. Go to **Issues** → **New Issue**
2. Use the **Feature Request** template
3. Describe the feature clearly
4. Add relevant labels

### 2. Create a Branch

Create a feature branch from main:

```bash
# Ensure you're on main
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/your-feature-name
```

**Branch naming conventions:**
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring

### 3. Plan Your Changes

Before coding:

1. Review existing code for patterns
2. Check related documentation
3. Consider edge cases
4. Plan your approach

### 4. Implement the Feature

Write your code following project conventions:

```bash
# Source code goes in
src/
├── components/    # UI components
├── services/      # Business logic
├── utils/         # Utility functions
└── types/         # Type definitions
```

**Code checklist:**
- [ ] Follows existing code style
- [ ] Includes TypeScript types
- [ ] Has appropriate error handling
- [ ] Is well-documented

### 5. Write Tests

Add tests for your feature:

```bash
# Tests go in
tests/
├── unit/          # Unit tests
├── integration/   # Integration tests
└── e2e/           # End-to-end tests
```

```bash
# Run tests
npm test

# Run with coverage
npm run test:coverage
```

**Testing checklist:**
- [ ] Unit tests for new functions
- [ ] Integration tests if applicable
- [ ] Edge cases covered
- [ ] All tests pass

### 6. Update Documentation

Keep documentation in sync:

1. Update README if needed
2. Add/update API documentation
3. Update relevant guides
4. Add examples if complex

### 7. Commit Your Changes

Use conventional commit messages:

```bash
git add .
git commit -m "feat: add user authentication feature"
```

**Commit message format:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `test:` - Tests
- `refactor:` - Refactoring

### 8. Push and Create PR

```bash
# Push your branch
git push origin feature/your-feature-name

# Create PR via GitHub web interface or CLI
gh pr create
```

### 9. Code Review

Address review feedback:

1. Check PR comments
2. Make requested changes
3. Push updates
4. Respond to comments

### 10. Merge

Once approved:

1. Ensure CI passes
2. Squash commits if required
3. Merge to main
4. Delete your branch

---

## Checklist Summary

- [ ] GitHub issue created
- [ ] Feature branch created
- [ ] Code implemented
- [ ] Tests written and passing
- [ ] Documentation updated
- [ ] Commit messages follow convention
- [ ] PR created and reviewed
- [ ] Changes merged

---

## Troubleshooting

### Tests failing?
- Check error messages carefully
- Ensure all dependencies are installed
- Run tests locally before pushing

### CI failing?
- Check the workflow logs
- Ensure linting passes
- Verify test configuration

---

## Related Guides

- [Set Up Testing](./setup-testing.md)
- [Write Documentation](./write-documentation.md)
- [Configure CI/CD](./configure-ci-cd.md)
