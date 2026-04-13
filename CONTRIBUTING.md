# Contributing to zai-test

Thank you for your interest in contributing to zai-test! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Process](#development-process)
- [Pull Request Guidelines](#pull-request-guidelines)
- [Coding Standards](#coding-standards)
- [Commit Messages](#commit-messages)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Getting Started

1. Fork the repository
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/zai-test.git
   cd zai-test
   ```
3. Create a branch for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. Make your changes and commit them
5. Push to your fork and submit a pull request

## How to Contribute

### Reporting Bugs

- Use the [Bug Report template](.github/ISSUE_TEMPLATE/bug_report.md)
- Include detailed steps to reproduce
- Describe expected vs actual behavior

### Requesting Features

- Use the [Feature Request template](.github/ISSUE_TEMPLATE/feature_request.md)
- Explain the use case and benefits
- Consider implementation suggestions

### Improving Documentation

- Fix typos or clarify existing docs
- Add missing documentation
- Improve examples and tutorials

### Contributing Code

- Follow the [development process](#development-process)
- Write tests for new functionality
- Update documentation as needed

## Development Process

1. **Pick an issue** - Look for open issues or create one for your proposed changes
2. **Create a branch** - Use descriptive names like `feature/add-login` or `fix/memory-leak`
3. **Make changes** - Follow our coding standards
4. **Test thoroughly** - Ensure all tests pass
5. **Update docs** - Keep documentation in sync with code changes
6. **Submit PR** - Fill out the PR template completely

## Pull Request Guidelines

- Fill out the [PR template](.github/PULL_REQUEST_TEMPLATE.md) completely
- Link to related issues
- Include tests for new functionality
- Update documentation
- Keep PRs focused - one feature/fix per PR
- Be responsive to code review feedback

### PR Checklist

- [ ] Code follows project style guidelines
- [ ] Tests added/updated and passing
- [ ] Documentation updated
- [ ] Commit messages follow conventions
- [ ] PR linked to relevant issues

## Coding Standards

### General Principles

- Write clean, readable, and maintainable code
- Follow DRY (Don't Repeat Yourself) principles
- Add comments for complex logic
- Use meaningful variable and function names

### File Organization

- Place source code in `src/` directory
- Place tests in `tests/` directory
- Update documentation in `docs/` as needed

## Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding/updating tests
- `chore`: Maintenance tasks

### Examples

```
feat(auth): add OAuth2 login support
fix(api): resolve memory leak in request handler
docs(readme): update installation instructions
```

## Questions?

Feel free to open an issue for questions or reach out to the maintainers.

Thank you for contributing! 🎉
