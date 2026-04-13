# Prompt Templates

Templates for creating new prompts with consistent structure.

---

## Basic Prompt Template

```markdown
# Prompt: {Name}

Brief description of what this prompt does.

---

## Purpose
Detailed explanation of when and why to use this prompt.

---

## Prompt

```
{The actual prompt with {placeholders}}
```

---

## Parameters

| Parameter | Description | Required | Example |
|-----------|-------------|----------|---------|
| {param} | What it does | Yes/No | Example value |

---

## Example Usage

### Input
```
[Filled-in example]
```

### Output
```
[Expected output example]
```

---

## Tips
- Tip 1
- Tip 2

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | Date | Initial version |
```

---

## Advanced Prompt Template

For complex prompts with multiple sections:

```markdown
# Prompt: {Name}

---

## Metadata
- Category: [code-generation | debugging | documentation | other]
- Complexity: [simple | moderate | complex]
- Model Tested: [GPT-4 | Claude | etc.]
- Last Updated: YYYY-MM-DD

---

## Purpose
[Detailed purpose]

---

## When to Use
- Use case 1
- Use case 2
- Use case 3

---

## Prompt

### System Message (if applicable)
```
[System prompt content]
```

### User Message Template
```
[User prompt with {placeholders}]
```

---

## Parameters

### Required Parameters
| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| {param} | type | description | example |

### Optional Parameters
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| {param} | type | default | description |

---

## Examples

### Example 1: {Title}
**Input:**
```
[Filled prompt]
```

**Output:**
```
[Result]
```

### Example 2: {Title}
**Input:**
```
[Filled prompt]
```

**Output:**
```
[Result]
```

---

## Customization Options

### For Different Skill Levels
- Beginner: [Adjustments]
- Advanced: [Adjustments]

### For Different Contexts
- Context 1: [Adjustments]
- Context 2: [Adjustments]

---

## Known Limitations
- Limitation 1
- Limitation 2

---

## Related Prompts
- [Related prompt 1](link)
- [Related prompt 2](link)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | Date | Initial version |
```

---

## Quick Reference: Placeholder Types

| Placeholder | Use For |
|-------------|---------|
| {language} | Target programming language |
| {framework} | Framework being used |
| {code} | Code snippets |
| {description} | Natural language descriptions |
| {constraints} | Limitations and requirements |
| {examples} | Input/output examples |
| {context} | Additional background info |

---

## Creating New Prompts

1. **Copy a template** above
2. **Fill in all sections**
3. **Test with multiple scenarios**
4. **Document results**
5. **Add to appropriate library folder**
6. **Submit via PR**
