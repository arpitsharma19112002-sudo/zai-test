# Prompt Library

A collection of tested, reusable prompts for common development tasks.

## Categories

### [Code Generation](code-generation/)
Prompts for generating code from specifications, tests, and requirements.

| Prompt | Purpose |
|--------|---------|
| [function-generator.md](code-generation/function-generator.md) | Generate functions from descriptions |
| [test-generator.md](code-generation/test-generator.md) | Generate unit tests |
| [api-endpoint.md](code-generation/api-endpoint.md) | Generate API endpoints |

### [Debugging](debugging/)
Prompts for identifying and fixing issues.

| Prompt | Purpose |
|--------|---------|
| [error-analyzer.md](debugging/error-analyzer.md) | Analyze and explain errors |
| [performance-debugger.md](debugging/performance-debugger.md) | Identify performance issues |

### [Documentation](documentation.md)
Prompts for generating documentation.

---

## Using Prompts

1. **Select** - Choose the appropriate prompt for your task
2. **Copy** - Copy the prompt template
3. **Customize** - Fill in the placeholders
4. **Execute** - Use with your AI assistant
5. **Iterate** - Refine based on results

## Prompt Template

Each prompt follows this structure:

```markdown
# Prompt: [Name]

## Purpose
[What this prompt is for]

## Prompt
[The actual prompt with placeholders]

## Parameters
| Parameter | Description | Required |
|-----------|-------------|----------|
| {param1} | Description | Yes |

## Example Usage
[Example of filled-in prompt]

## Tips
[Best practices and tips]
```

## Contributing

To add a prompt to the library:

1. Test thoroughly with multiple scenarios
2. Document parameters and examples
3. Add to appropriate category folder
4. Submit via PR

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines.
