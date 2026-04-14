# Story 10.1: FastAPI Setup for BioPress Designer

**Epic:** 10. REST API  
**Owner:** Development Team  
**Status:** Done

## Story

As a developer, I want BioPress to expose a REST API, so I can integrate it into other applications.

## Acceptance Criteria

- [x] Given biopress installed, When `biopress api start`, Then FastAPI server starts on port 8000
- [x] I can access `/docs` for Swagger UI
- [x] Basic health check endpoint returns status

## Technical Specification

### Implementation Details

1. **API Module** (`src/biopress/api/`) (new)
   - `__init__.py` - Module exports
   - `main.py` - FastAPI app with health endpoints and routes
   - CORS middleware enabled

2. **Routes** (`src/biopress/api/routes/`) (new)
   - `__init__.py` - Package init
   - `generate.py` - POST /api/v1/generate endpoint
   - `validate.py` - POST /api/v1/validate endpoint
   - `pdf.py` - POST /api/v1/pdf endpoint

3. **Models** (`src/biopress/api/models/`) (new)
   - `__init__.py` - Package exports
   - `schemas.py` - Pydantic request/response models

4. **CLI Integration** (`src/biopress/cli/commands/api.py`)
   - `biopress api start` command starts uvicorn server
   - `biopress api docs` shows endpoint info

5. **Tests** (`tests/test_api.py`)
   - Health endpoint tests
   - Validation tests for endpoint inputs

### Dependencies Added

```toml
fastapi>=0.109.0
uvicorn>=0.27.0
httpx>=0.26.0  # dev
```

### API Endpoints

| Endpoint           | Method | Description        |
| ------------------ | ------ | ------------------ |
| `/`                | GET    | Health check       |
| `/health`          | GET    | Detailed health    |
| `/docs`            | GET    | Swagger UI         |
| `/api/v1/generate` | POST   | Generate questions |
| `/api/v1/validate` | POST   | Validate questions |
| `/api/v1/pdf`      | POST   | Generate PDF       |

### Usage

```bash
# Start API server
biopress api start

# Or with custom port
biopress api start --port 8080 --reload

# Access Swagger UI
# http://localhost:8000/docs

# Health check
curl http://localhost:8000/health
```
