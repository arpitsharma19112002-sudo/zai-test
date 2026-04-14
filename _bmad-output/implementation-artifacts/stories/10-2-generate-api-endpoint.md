# Story 10.2: Generate API Endpoint for BioPress Designer

**Epic:** 10 - API Support (Future Phase)
**Status:** backlog
**Priority:** Future
**Note:** Not implementing in current phase

## Story

As an API user, I want a generation endpoint, so I create quizzes programmatically.

## Acceptance Criteria

- POST `/generate` endpoint
- Accepts quiz specification
- Returns job ID for polling

## Implementation Notes

### Future Implementation

1. **Generate Endpoint** (`src/biopress/api/routes.py`)
   - POST `/api/v1/generate`
   - Request: QuizConfig model
   - Response: Job ID + status URL

2. **Async Processing**
   - Queue generation jobs
   - Poll for status
   - Webhook回调 option

## Files to Create

- `src/biopress/api/routes.py` - Generation route
- `src/biopress/api/queue.py` - Job queue

## Notes

- Future Phase - Not implementing now
- Requires async job queue (Redis/celery)
- Consider webhook for completion
