# Code Generation Prompts

Prompts for generating code from specifications and requirements.

---

## Available Prompts

| Prompt | Purpose | Best For |
|--------|---------|----------|
| [function-generator.md](function-generator.md) | Generate functions | Utility functions, algorithms |
| [test-generator.md](test-generator.md) | Generate tests | Unit tests, integration tests |
| [api-endpoint.md](api-endpoint.md) | Generate REST endpoints | CRUD operations, APIs |

---

## Best Practices for Code Generation

### 1. Be Specific About Requirements

❌ Bad: "Create a function to process data"

✅ Good: "Create a TypeScript function that:
- Takes an array of User objects
- Filters out inactive users
- Returns users sorted by lastLoginDate
- Throws on invalid input"

### 2. Provide Context

Include relevant information:

- Language and version
- Framework being used
- Existing patterns to follow
- Dependencies available

### 3. Specify Output Format

- Type definitions needed
- Documentation style (JSDoc, etc.)
- Error handling approach
- Testing requirements

### 4. Include Examples

- Sample input/output
- Edge cases to handle
- Error scenarios

---

## Prompt Structure

```markdown
## Context
- Language: [language]
- Framework: [framework]
- Pattern: [pattern to follow]

## Requirements
[Detailed requirements]

## Input
[Expected input format]

## Output
[Expected output format]

## Constraints
- [Constraint 1]
- [Constraint 2]

## Examples
### Example 1
Input: ...
Output: ...
```

---

## Common Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| {language} | Target language | TypeScript, Python |
| {framework} | Framework to use | React, Express |
| {description} | What to generate | "A user authentication function" |
| {constraints} | Limitations | "No external dependencies" |
| {style} | Code style | "Functional", "OOP" |
