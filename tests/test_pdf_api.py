"""Tests for PDF export API."""

import json

import pytest
from fastapi.testclient import TestClient

from biopress.api.main import app
from biopress.api.routes.pdf import VALID_STYLES


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def sample_questions():
    """Sample questions for testing."""
    return [
        {
            "id": "q1",
            "question": "What is the powerhouse of the cell?",
            "options": {"A": "Nucleus", "B": "Mitochondria", "C": "Ribosome", "D": "Golgi apparatus"},
            "correct_answer": "B",
            "explanation": "Mitochondria produce ATP through cellular respiration.",
        },
        {
            "id": "q2",
            "question": "What is the chemical formula for water?",
            "options": {"A": "H2O", "B": "CO2", "C": "NaCl", "D": "O2"},
            "correct_answer": "A",
            "explanation": "Water is composed of two hydrogen atoms and one oxygen atom.",
        },
    ]


@pytest.fixture
def quiz_json(sample_questions):
    """Create JSON string from questions."""
    return json.dumps({"items": sample_questions})


def test_export_pdf_with_content(client, quiz_json):
    """Test PDF export with JSON content."""
    response = client.post(
        "/api/v1/export",
        data={"content": quiz_json, "style": "default"},
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"


def test_export_pdf_with_file(client, sample_questions):
    """Test PDF export with file upload."""
    quiz_json = json.dumps({"items": sample_questions})
    response = client.post(
        "/api/v1/export",
        files={"file": ("quiz.json", quiz_json, "application/json")},
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"


def test_export_pdf_invalid_style(client, quiz_json):
    """Test PDF export with invalid style."""
    response = client.post(
        "/api/v1/export",
        data={"content": quiz_json, "style": "invalid_style"},
    )
    assert response.status_code == 400
    assert "Invalid style" in response.json()["detail"]


def test_export_pdf_no_content(client):
    """Test PDF export without content or file."""
    response = client.post("/api/v1/export")
    assert response.status_code == 400
    assert "Either content or file must be provided" in response.json()["detail"]


def test_export_pdf_invalid_json(client):
    """Test PDF export with invalid JSON."""
    response = client.post(
        "/api/v1/export",
        data={"content": "not valid json"},
    )
    assert response.status_code == 400
    assert "Invalid JSON" in response.json()["detail"]


def test_export_pdf_empty_questions(client):
    """Test PDF export with empty questions."""
    response = client.post(
        "/api/v1/export",
        data={"content": json.dumps({"items": []})},
    )
    assert response.status_code == 400
    assert "No questions provided" in response.json()["detail"]


def test_export_pdf_all_styles(client, quiz_json):
    """Test PDF export with all valid styles."""
    for style in VALID_STYLES:
        response = client.post(
            "/api/v1/export",
            data={"content": quiz_json, "style": style},
        )
        assert response.status_code == 200, f"Style {style} failed"
        assert response.headers["content-type"] == "application/pdf"


def test_export_pdf_with_title(client, quiz_json):
    """Test PDF export with custom title."""
    response = client.post(
        "/api/v1/export",
        data={"content": quiz_json, "style": "default", "title": "My Custom Quiz"},
    )
    assert response.status_code == 200


def test_export_pdf_without_answers(client, quiz_json):
    """Test PDF export without answer key."""
    response = client.post(
        "/api/v1/export",
        data={"content": quiz_json, "style": "default", "include_answers": "false"},
    )
    assert response.status_code == 200


def test_pdf_endpoint_json_body(client, sample_questions):
    """Test legacy PDF endpoint with JSON body."""
    formatted_questions = []
    for q in sample_questions:
        formatted_questions.append({
            "id": q["id"],
            "question": q["question"],
            "options": list(q["options"].values()),
            "correct_answer": q["correct_answer"],
            "explanation": q["explanation"],
        })
    response = client.post(
        "/api/v1/pdf",
        json={
            "questions": formatted_questions,
            "style": "default",
            "include_answers": True,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "questions" in data["message"]


def test_pdf_endpoint_invalid_style(client, sample_questions):
    """Test legacy PDF endpoint with invalid style."""
    formatted_questions = []
    for q in sample_questions:
        formatted_questions.append({
            "id": q["id"],
            "question": q["question"],
            "options": list(q["options"].values()),
            "correct_answer": q["correct_answer"],
            "explanation": q["explanation"],
        })
    response = client.post(
        "/api/v1/pdf",
        json={
            "questions": formatted_questions,
            "style": "invalid",
        },
    )
    assert response.status_code == 400
    assert "Invalid style" in response.json()["detail"]