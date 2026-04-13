# Prompt: Documentation Generator

Generate comprehensive documentation for code, APIs, and projects.

---

## Purpose

Use this prompt to generate various types of documentation including README files, API docs, code comments, and guides.

---

## Prompt

```
Generate {doc_type} documentation for the following:

## Subject
{subject_description}

## Code (if applicable)
```{language}
{code}
```

## Documentation Requirements
- Format: {format}
- Audience: {audience}
- Sections needed: {sections}
- Style: {style}

## Additional Context
{context}

Please provide:
1. Complete documentation
2. Code examples where appropriate
3. Usage instructions
4. Any warnings or notes
```

---

## Parameters

| Parameter | Description | Required | Example |
|-----------|-------------|----------|---------|
| {doc_type} | Type of documentation | Yes | README, API docs, JSDoc |
| {subject_description} | What to document | Yes | "A user authentication library" |
| {code} | Code to document | No | Function or class code |
| {language} | Programming language | No | TypeScript, Python |
| {format} | Output format | No | Markdown, HTML, JSDoc |
| {audience} | Target readers | No | "Beginner developers" |
| {sections} | Required sections | No | "Install, Usage, API, Examples" |
| {style} | Writing style | No | "Concise", "Detailed" |
| {context} | Additional context | No | "Part of larger system" |

---

## Documentation Types

### README

For project overview:

```
Generate README documentation for the following:

## Subject
{project_name} - {project_description}

## Documentation Requirements
- Format: Markdown
- Audience: Developers
- Sections needed: Installation, Quick Start, Usage, API, Contributing
- Style: Clear and concise

## Additional Context
{project_context}
```

### API Documentation

For functions and endpoints:

```
Generate API documentation for the following:

## Subject
{api_name} - {api_description}

## Code
```{language}
{api_code}
```

## Documentation Requirements
- Format: Markdown
- Audience: API consumers
- Sections needed: Parameters, Returns, Examples, Errors
- Style: Technical and precise
```

### Code Comments

For inline documentation:

```
Generate inline code comments for the following:

## Code
```{language}
{code}
```

## Documentation Requirements
- Format: {JSDoc, Python docstrings}
- Audience: Developers maintaining the code
- Style: Clear explanations of complex logic

## Additional Context
Include type information and examples
```

---

## Tips

1. **Know your audience** - Adjust complexity accordingly
2. **Include examples** - Show, don't just tell
3. **Be consistent** - Use consistent terminology and formatting
4. **Keep it updated** - Documentation should match code
5. **Add cross-references** - Link to related documentation

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-13 | Initial version |
