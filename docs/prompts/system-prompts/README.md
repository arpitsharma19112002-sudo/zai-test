# System Prompts

System prompts define the core behavior and capabilities of AI assistants. These prompts are used to "prime" an AI with a specific role, expertise, or behavioral pattern.

## What is a System Prompt?

A system prompt is the initial instruction given to an AI that defines:

- The role it should play
- Its areas of expertise
- How it should respond
- Any constraints or guidelines

## Available System Prompts

| Prompt | Purpose | Use Case |
|--------|---------|----------|
| [software-engineer.md](software-engineer.md) | Full-stack development | Code development, debugging |
| [code-reviewer.md](code-reviewer.md) | Code review | PR reviews, quality checks |
| [documentation-writer.md](documentation-writer.md) | Technical writing | Docs, READMEs, tutorials |

## System Prompt Template

```markdown
# System Prompt: [Name]

## Role
[Define the AI's role]

## Expertise
- Area 1
- Area 2
- Area 3

## Behavioral Guidelines
- Guideline 1
- Guideline 2

## Response Format
[Define how responses should be structured]

## Constraints
- Constraint 1
- Constraint 2

## Examples

### Example 1
Input: ...
Output: ...
```

## Best Practices

1. **Be Specific** - Vague prompts produce vague responses
2. **Set Boundaries** - Define what the AI should and shouldn't do
3. **Provide Examples** - Few-shot examples improve consistency
4. **Iterate** - Refine based on results
5. **Version** - Track changes to system prompts

## Integration

### With Chat APIs

```javascript
const response = await openai.chat.completions.create({
  model: "gpt-4",
  messages: [
    { role: "system", content: SYSTEM_PROMPT },
    { role: "user", content: userMessage }
  ]
});
```

### With CLI Tools

```bash
# Using a system prompt file
ai-cli --system-prompt ./system-prompts/software-engineer.md "Help me debug this function"
```
