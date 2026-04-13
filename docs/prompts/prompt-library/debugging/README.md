# Debugging Prompts

Prompts for identifying, analyzing, and fixing issues in your code.

---

## Available Prompts

| Prompt | Purpose | Best For |
|--------|---------|----------|
| [error-analyzer.md](error-analyzer.md) | Analyze and explain errors | Runtime errors, exceptions |
| [performance-debugger.md](performance-debugger.md) | Identify performance issues | Slow code, memory leaks |

---

## Debugging Best Practices

### 1. Provide Context

Include relevant information:

- Error messages and stack traces
- Code that produces the error
- Expected vs actual behavior
- Environment details

### 2. Share Minimal Reproducible Example

- Isolate the problem
- Remove unrelated code
- Include necessary imports
- Provide sample data

### 3. Describe What You've Tried

- Solutions attempted
- What didn't work
- Any partial fixes

---

## Prompt Structure

```markdown
## Error/Issue
[Error message or description]

## Code
[Relevant code snippet]

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]

## Environment
- Language/Version:
- Framework:
- OS:

## What I've Tried
- [Attempt 1]
- [Attempt 2]
```
