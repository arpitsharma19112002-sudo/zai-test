# Prompt: Error Analyzer

Analyze error messages and stack traces to identify root causes and solutions.

---

## Purpose

Use this prompt when encountering errors or exceptions. The AI will analyze the error, identify the root cause, and provide a solution.

---

## Prompt

```
Analyze the following error and provide a solution:

## Error Message
```
{error_message}
```

## Stack Trace
```
{stack_trace}
```

## Code That Produces the Error
```{language}
{code}
```

## Context
- Language: {language}
- Framework: {framework}
- When it occurs: {when_occurs}

## What I've Tried
{attempts}

Please provide:
1. Root cause analysis
2. Step-by-step debugging approach
3. Solution with code fix
4. Prevention strategies
```

---

## Parameters

| Parameter | Description | Required | Example |
|-----------|-------------|----------|---------|
| {error_message} | The error message | Yes | "TypeError: Cannot read property 'x' of undefined" |
| {stack_trace} | Stack trace if available | No | Full stack trace |
| {code} | Code producing the error | Yes | Relevant code snippet |
| {language} | Programming language | Yes | TypeScript, Python |
| {framework} | Framework being used | No | React, Express |
| {when_occurs} | When the error occurs | No | "On form submission" |
| {attempts} | What you've already tried | No | "Checked for null" |

---

## Example Usage

### Filled Prompt

```
Analyze the following error and provide a solution:

## Error Message
```
TypeError: Cannot read properties of undefined (reading 'id')
```

## Stack Trace
```
TypeError: Cannot read properties of undefined (reading 'id')
    at updateUser (src/services/user.ts:45:18)
    at processTicksAndRejections (node:internal/process/task_queues:95:5)
```

## Code That Produces the Error
```typescript
async function updateUser(req: Request, res: Response) {
  const user = await UserRepository.findById(req.params.id);
  const updated = { ...user, name: req.body.name };
  await UserRepository.save(updated);
  return res.json(updated);
}
```

## Context
- Language: TypeScript
- Framework: Express
- When it occurs: When user ID doesn't exist in database

## What I've Tried
- Checked if the ID is being passed correctly
- Verified the database connection

Please provide:
1. Root cause analysis
2. Step-by-step debugging approach
3. Solution with code fix
4. Prevention strategies
```

---

## Tips

1. **Include the full error** - Don't truncate error messages
2. **Show the exact code** - Line numbers should match
3. **Describe when it happens** - Context helps identify the issue
4. **Share what you tried** - Avoid suggesting things you've done
5. **Include environment** - Language version, OS, etc.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-13 | Initial version |
