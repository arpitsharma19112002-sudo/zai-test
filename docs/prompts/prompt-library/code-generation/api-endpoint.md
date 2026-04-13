# Prompt: API Endpoint Generator

Generate RESTful API endpoints with validation, error handling, and documentation.

---

## Purpose

Use this prompt to generate complete API endpoints including route handlers, validation, error handling, and documentation.

---

## Prompt

```
Generate a {http_method} API endpoint for {framework} with the following specifications:

## Endpoint Details
- Route: {route}
- Purpose: {purpose}
- Authentication: {auth_requirements}

## Request
- Body: {request_body}
- Query params: {query_params}
- Path params: {path_params}

## Response
- Success (200): {success_response}
- Error responses: {error_responses}

## Business Logic
{business_logic}

## Validation Requirements
{validation_requirements}

## Constraints
- {constraints}
- Include error handling
- Follow REST best practices
- Include input validation

Please provide:
1. Complete route handler implementation
2. Input validation middleware/schema
3. Error handling
4. TypeScript types/interfaces
5. API documentation comments
6. Example requests/responses
```

---

## Parameters

| Parameter | Description | Required | Example |
|-----------|-------------|----------|---------|
| {http_method} | HTTP method | Yes | GET, POST, PUT, DELETE |
| {framework} | Web framework | Yes | Express, Fastify, NestJS |
| {route} | Endpoint route | Yes | /api/users/:id |
| {purpose} | What the endpoint does | Yes | "Get user by ID" |
| {auth_requirements} | Auth requirements | No | "JWT required, admin role" |
| {request_body} | Request body schema | No | JSON schema or description |
| {query_params} | Query parameters | No | "page, limit, sort" |
| {path_params} | Path parameters | No | "id: string" |
| {success_response} | Success response shape | Yes | "{ user: User }" |
| {error_responses} | Error response shapes | No | "404 if not found, 403 if unauthorized" |
| {business_logic} | Core logic description | Yes | "Fetch user from database" |
| {validation_requirements} | Input validation rules | No | "Email must be valid" |
| {constraints} | Additional constraints | No | "Rate limit: 100/minute" |

---

## Example Usage

### Filled Prompt

```
Generate a POST API endpoint for Express with the following specifications:

## Endpoint Details
- Route: /api/users
- Purpose: Create a new user account
- Authentication: None (public registration)

## Request
- Body: { email: string, password: string, name: string }
- Query params: None
- Path params: None

## Response
- Success (201): { user: { id: string, email: string, name: string }, token: string }
- Error responses:
  - 400: Invalid input data
  - 409: Email already exists
  - 500: Server error

## Business Logic
1. Validate input data
2. Check if email already exists
3. Hash password
4. Create user in database
5. Generate JWT token
6. Return user and token

## Validation Requirements
- Email: valid email format, required
- Password: min 8 chars, at least 1 number and 1 special char
- Name: min 2 chars, required

## Constraints
- Use bcrypt for password hashing
- Use jsonwebtoken for tokens
- Follow Express best practices

Please provide:
1. Complete route handler implementation
2. Input validation middleware/schema
3. Error handling
4. TypeScript types/interfaces
5. API documentation comments
6. Example requests/responses
```

---

## Tips

1. **Define request/response shapes** - Be explicit about data structures
2. **List all error cases** - Include all possible error responses
3. **Specify authentication** - What auth mechanism is required
4. **Include validation rules** - Be specific about input constraints
5. **Mention dependencies** - Libraries available for use

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-13 | Initial version |
