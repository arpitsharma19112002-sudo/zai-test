# Story 10.3: PDF Export API for BioPress Designer

**Epic:** 10 - API Support (Future Phase)
**Status:** backlog
**Priority:** Future
**Note:** Not implementing in current phase

## Story

As an API user, I want PDF download endpoint, so I get generated documents via API.

## Acceptance Criteria

- GET `/download/{job_id}` endpoint
- Returns PDF file
- Supports all PDF styles

## Implementation Notes

### Future Implementation

1. **Download Endpoint** (`src/biopress/api/routes.py`)
   - GET `/api/v1/download/{job_id}`
   - Returns PDF file
   - Sets correct content-type

2. **Status Endpoint** (`src/biopress/api/routes.py`)
   - GET `/api/v1/status/{job_id}`
   - Returns job status + preview URL

## Files to Create

- Additional routes in `routes.py`

## Notes

- Future Phase - Not implementing now
- Depends on 10.2 Generate endpoint
- Consider streaming for large files
