# Prompt: Performance Debugger

Identify and resolve performance issues in your code.

---

## Purpose

Use this prompt to analyze slow code, memory issues, or optimization opportunities. The AI will identify bottlenecks and suggest optimizations.

---

## Prompt

```
Analyze the following code for performance issues:

## Code to Analyze
```{language}
{code}
```

## Performance Problem
{problem_description}

## Metrics
- Execution time: {execution_time}
- Memory usage: {memory_usage}
- Input size: {input_size}

## Constraints
- Language: {language}
- Framework: {framework}
- Environment: {environment}

## Requirements
- Expected performance: {expected_performance}
- Constraints: {constraints}

Please provide:
1. Performance analysis
2. Identified bottlenecks
3. Optimized solution with code
4. Performance comparison (before/after)
5. Additional recommendations
```

---

## Parameters

| Parameter | Description | Required | Example |
|-----------|-------------|----------|---------|
| {code} | Code to analyze | Yes | The slow code |
| {problem_description} | What's slow | Yes | "Takes 30 seconds to process 1000 items" |
| {execution_time} | Current execution time | No | "30 seconds" |
| {memory_usage} | Memory consumed | No | "500MB peak" |
| {input_size} | Size of input data | No | "10,000 records" |
| {language} | Programming language | Yes | TypeScript, Python |
| {framework} | Framework used | No | React, Express |
| {environment} | Runtime environment | No | "Node.js 18, 4GB RAM" |
| {expected_performance} | Target performance | No | "Under 1 second" |
| {constraints} | Limitations | No | "Cannot add new dependencies" |

---

## Example Usage

### Filled Prompt

```
Analyze the following code for performance issues:

## Code to Analyze
```typescript
async function processUsers(userIds: string[]) {
  const results = [];
  for (const id of userIds) {
    const user = await db.users.findUnique({ where: { id } });
    const posts = await db.posts.findMany({ where: { userId: id } });
    const comments = await db.comments.findMany({ where: { userId: id } });
    results.push({ user, posts, comments });
  }
  return results;
}
```

## Performance Problem
Processing 100 users takes over 30 seconds. Need to improve to under 2 seconds.

## Metrics
- Execution time: 30+ seconds for 100 users
- Memory usage: Not measured
- Input size: 100 user IDs

## Constraints
- Language: TypeScript
- Framework: Next.js with Prisma
- Environment: Node.js 18

## Requirements
- Expected performance: Under 2 seconds for 100 users
- Constraints: Must use existing Prisma client

Please provide:
1. Performance analysis
2. Identified bottlenecks
3. Optimized solution with code
4. Performance comparison (before/after)
5. Additional recommendations
```

---

## Tips

1. **Provide metrics** - Actual numbers help prioritize optimizations
2. **Include data sizes** - Algorithm complexity depends on input size
3. **Mention constraints** - Some optimizations may not be allowed
4. **Describe the problem** - Is it slow? Memory hungry? Both?
5. **Share context** - What calls this code? How often?

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-13 | Initial version |
