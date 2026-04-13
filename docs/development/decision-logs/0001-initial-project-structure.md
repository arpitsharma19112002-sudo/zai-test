# ADR-0001: Initial Project Structure

## Status

Accepted

## Context

When starting a new project, we needed to decide on a repository structure that would:

1. Scale from prototype to production
2. Support comprehensive documentation
3. Enable AI-assisted development with prompt management
4. Follow industry best practices
5. Be intuitive for new contributors

Without a well-defined structure, projects often become disorganized, making it difficult to find information and maintain consistency.

## Decision

We adopted a structure with:

- **Root-level files** for essential project information (README, LICENSE, etc.)
- **`.github/`** for GitHub-specific configurations and templates
- **`docs/`** as the central documentation hub with organized subdirectories
- **`docs/prompts/`** specifically for AI prompt management
- **`src/`** for source code
- **`tests/`** for test files

This follows the Diátaxis documentation framework principles (tutorials, how-to guides, reference, explanation).

## Consequences

### Positive

- Clear organization makes it easy to find information
- Dedicated prompt folder enables systematic AI prompt management
- GitHub templates ensure consistent issue and PR formatting
- Documentation hub prevents scattered docs
- Structure scales well as project grows

### Negative

- Initial setup requires creating many directories
- May seem complex for very small projects
- Requires discipline to maintain organization

## Alternatives Considered

1. **Flat structure** - Simpler but doesn't scale
2. **Docs in wiki** - Separated from code, can get out of sync
3. **Monorepo structure** - Overkill for this project size

## Related Decisions

None yet.

## References

- [Diátaxis Documentation Framework](https://diataxis.fr/)
- [GitHub Repository Best Practices](https://docs.github.com/en/repositories)
