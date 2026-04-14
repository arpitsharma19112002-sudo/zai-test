"""Tests for BioPress API."""

import os
from fastapi.testclient import TestClient

from biopress.api.main import app

os.environ["BIOPRESS_API_KEY"] = "test-api-key"

client = TestClient(app)


def test_health_endpoint():
    """Test health check endpoint returns ok status."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "biopress"


def test_health_check_endpoint():
    """Test dedicated health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "biopress"


def test_docs_endpoint():
    """Test /docs returns HTML Swagger UI (not a JSON stub)."""
    response = client.get("/docs")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")


def test_generate_endpoint_invalid_exam():
    """Test generate endpoint with invalid exam."""
    response = client.post(
        "/api/v1/generate",
        json={
            "exam": "INVALID",
            "subject": "Physics",
            "type": "mcq",
            "count": 10,
        },
        headers={"X-API-Key": "test-api-key"},
    )
    assert response.status_code == 400


def test_generate_endpoint_invalid_subject():
    """Test generate endpoint with invalid subject."""
    response = client.post(
        "/api/v1/generate",
        json={
            "exam": "NEET",
            "subject": "Invalid",
            "type": "mcq",
            "count": 10,
        },
        headers={"X-API-Key": "test-api-key"},
    )
    assert response.status_code == 400


def test_generate_endpoint_invalid_type():
    """Test generate endpoint with invalid type."""
    response = client.post(
        "/api/v1/generate",
        json={
            "exam": "NEET",
            "subject": "Physics",
            "type": "invalid",
            "count": 10,
        },
        headers={"X-API-Key": "test-api-key"},
    )
    assert response.status_code == 400


def test_generate_endpoint_count_limit():
    """Test generate endpoint with count out of range."""
    response = client.post(
        "/api/v1/generate",
        json={
            "exam": "NEET",
            "subject": "Physics",
            "type": "mcq",
            "count": 100,
        },
        headers={"X-API-Key": "test-api-key"},
    )
    assert response.status_code in [400, 422]


def test_validate_endpoint_invalid_level():
    """Test validate endpoint with invalid level."""
    response = client.post(
        "/api/v1/validate",
        json={
            "questions": [
                {
                    "id": "q1",
                    "question": "What is 2+2?",
                }
            ],
            "level": "invalid",
        },
    )
    assert response.status_code == 400


def test_pdf_endpoint_invalid_style():
    """Test PDF endpoint with invalid style."""
    response = client.post(
        "/api/v1/pdf",
        json={
            "questions": [
                {
                    "id": "q1",
                    "question": "What is 2+2?",
                    "options": ["3", "4", "5", "6"],
                    "correct_answer": "4",
                }
            ],
            "style": "invalid",
        },
    )
    assert response.status_code == 400


def test_generate_requires_api_key():
    """Test generate endpoint requires API key."""
    response = client.post(
        "/api/v1/generate",
        json={
            "exam": "NEET",
            "subject": "Physics",
            "type": "mcq",
            "count": 10,
        },
    )
    assert response.status_code == 401


def test_generate_rejects_invalid_api_key():
    """Test generate endpoint rejects invalid API key."""
    response = client.post(
        "/api/v1/generate",
        json={
            "exam": "NEET",
            "subject": "Physics",
            "type": "mcq",
            "count": 10,
        },
        headers={"X-API-Key": "invalid-key"},
    )
    assert response.status_code == 403