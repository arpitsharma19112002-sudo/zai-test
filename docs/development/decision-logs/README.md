# Architecture Decision Records (ADR)

This directory contains Architecture Decision Records for the zai-test project.

## What is an ADR?

An Architecture Decision Record (ADR) captures a significant architectural decision along with its context and consequences. ADRs help teams understand why certain decisions were made.

## ADR Template

Use this template for new ADRs:

```markdown
# ADR-NNNN: Brief Title

## Status

[Proposed | Accepted | Deprecated | Superseded]

## Context

What is the issue that we're seeing that is motivating this decision or change?

## Decision

What is the change that we're proposing and/or doing?

## Consequences

What becomes easier or more difficult to do because of this change?

## Alternatives Considered

What other options were considered?

## Related Decisions

Links to related ADRs.
```

## Index of ADRs

| Number | Title | Status | Date |
|--------|-------|--------|------|
| 0001 | Initial Project Structure | Accepted | 2026-04-13 |

## Creating a New ADR

1. Copy the template above
2. Name the file `NNNN-brief-title.md` (e.g., `0002-use-typescript.md`)
3. Fill in all sections
4. Submit for review via PR

## Best Practices

- Write ADRs for significant decisions that affect:
  - System architecture
  - Technology choices
  - Security decisions
  - Performance trade-offs
  - Major refactoring

- Keep ADRs concise but complete
- Include the "why" not just the "what"
- Update status as decisions evolve
- Link related ADRs
