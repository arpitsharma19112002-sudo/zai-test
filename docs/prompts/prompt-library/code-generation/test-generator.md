# Prompt: Test Generator

Generate comprehensive unit tests for your code.

---

## Purpose

Use this prompt to generate thorough unit tests for functions, classes, or modules. Covers happy paths, edge cases, and error scenarios.

---

## Prompt

```
Generate comprehensive unit tests for the following {language} code using {test_framework}:

## Code to Test
```{language}
{code}
```

## Testing Requirements
- Framework: {test_framework}
- Coverage goals: {coverage_requirements}
- Test types needed:
  - [ ] Happy path tests
  - [ ] Edge case tests
  - [ ] Error handling tests
  - [ ] Integration tests (if applicable)

## Specific Test Cases
{specific_cases}

## Mocking Requirements
{mocking_requirements}

## Constraints
- {constraints}
- Follow {style_guide} testing conventions
- Include descriptive test names
- Use AAA pattern (Arrange, Act, Assert)

Please provide:
1. Complete test file with imports
2. Test cases organized by category
3. Mock implementations if needed
4. Brief explanation of coverage approach
```

---

## Parameters

| Parameter | Description | Required | Example |
|-----------|-------------|----------|---------|
| {language} | Programming language | Yes | TypeScript, Python |
| {code} | The code to test | Yes | Function or class code |
| {test_framework} | Testing framework | Yes | Jest, Vitest, pytest |
| {coverage_requirements} | Coverage goals | No | "80% minimum, all branches" |
| {specific_cases} | Specific scenarios to test | No | "Test with empty array" |
| {mocking_requirements} | What needs mocking | No | "Mock database calls" |
| {constraints} | Testing constraints | No | "No external API calls" |
| {style_guide} | Testing style | No | "Jest best practices" |

---

## Example Usage

### Filled Prompt

```
Generate comprehensive unit tests for the following TypeScript code using Jest:

## Code to Test
```typescript
export function validateUser(user: unknown): user is User {
  if (!user || typeof user !== 'object') return false;

  const { id, email, name } = user as User;

  return (
    typeof id === 'string' &&
    typeof email === 'string' &&
    email.includes('@') &&
    typeof name === 'string' &&
    name.length >= 2
  );
}
```

## Testing Requirements
- Framework: Jest
- Coverage goals: 100% branch coverage
- Test types needed:
  - [x] Happy path tests
  - [x] Edge case tests
  - [x] Error handling tests

## Specific Test Cases
- Valid user object
- Missing fields
- Invalid email format
- Name too short
- Null/undefined input

## Mocking Requirements
None needed

## Constraints
- Use descriptive test names with "should" pattern
- Follow Jest best practices
- Include AAA pattern

Please provide:
1. Complete test file with imports
2. Test cases organized by category
3. Brief explanation of coverage approach
```

---

## Tips

1. **Include the actual code** - Paste the complete function/class to test
2. **Specify edge cases** - List specific scenarios that need testing
3. **Define coverage goals** - What percentage or specific paths
4. **Mention dependencies** - External services that need mocking
5. **Use describe blocks** - Group related tests logically

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-13 | Initial version |
