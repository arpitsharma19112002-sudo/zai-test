# Story 10.2: Generate API Endpoint for BioPress Designer

**Epic:** 10. REST API  
**Owner:** Development Team  
**Status:** Done

## Story

As a developer, I want to generate content via API, so I can automate content creation.

## Acceptance Criteria

- [x] Given API is running, When POST to `/api/v1/generate` with exam, subject, type, count, Then I receive generated questions in JSON
- [x] Response follows Perseus JSON format
- [x] Authentication required (API key)

## Technical Specification

### Implementation Details

1. **API Route** (`src/biopress/api/routes/generate.py`)
   - POST `/api/v1/generate` endpoint
   - Input validation: exam, subject, type, count, topic, language
   - Returns generated questions as JSON with `format: "perseus"`
   - API key authentication via `X-API-Key` header

2. **Request/Response Models** (`src/biopress/api/models/schemas.py`)
   - `GenerateRequest` - exam, subject, type, count, topic, language
   - `GenerateResponse` - status, questions, count, exam, subject, type, format

3. **API Key Authentication**
   - Header: `X-API-Key`
   - Env var: `BIOPRESS_API_KEY`
   - Returns 401 if missing, 403 if invalid

4. **Tests** (`tests/test_api.py`)
   - `test_generate_requires_api_key` - 401 when no key
   - `test_generate_rejects_invalid_api_key` - 403 when invalid key

### Usage

```bash
# Generate questions via API
curl -X POST http://localhost:8000/api/v1/generate \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "exam": "NEET",
    "subject": "Physics",
    "type": "mcq",
    "count": 10,
    "topic": "Mechanics"
  }'

# Response
{
  "status": "success",
  "questions": [...],
  "count": 10,
  "exam": "NEET",
  "subject": "Physics",
  "type": "mcq",
  "format": "perseus"
}
```

### Configuration

Set API key via environment variable:

```bash
export BIOPRESS_API_KEY="your-secret-key"
```
