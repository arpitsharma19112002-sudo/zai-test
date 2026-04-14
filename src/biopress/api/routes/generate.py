"""Generation API route."""

import os
from fastapi import APIRouter, HTTPException, Security
from fastapi.security import APIKeyHeader

from biopress.api.models.schemas import (
    GenerateRequest,
    GenerateResponse,
    QuestionModel,
)
from biopress.generators.questions.mcq import MCQGenerator
from biopress.generators.questions.numerical import NumericalGenerator
from biopress.generators.questions.case_based import CaseBasedGenerator
from biopress.generators.questions.assertion_reason import AssertionReasonGenerator
from biopress.core.constants import (
    VALID_EXAMS,
    VALID_SUBJECTS,
    VALID_TYPES,
    VALID_LANGUAGES,
)

router = APIRouter()

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(key: str = Security(api_key_header)):
    """Verify API key from header."""
    if key is None:
        raise HTTPException(status_code=401, detail="API key missing")
    expected_key = os.getenv("BIOPRESS_API_KEY")
    if not expected_key:
        raise HTTPException(status_code=500, detail="Server API key not configured")
    if key != expected_key:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return key


def get_generator(qtype: str):
    generators = {
        "mcq": MCQGenerator,
        "numerical": NumericalGenerator,
        "case-based": CaseBasedGenerator,
        "assertion-reason": AssertionReasonGenerator,
    }
    return generators.get(qtype, MCQGenerator)()


@router.post("/generate", response_model=GenerateResponse)
async def generate_questions(request: GenerateRequest, api_key: str = Security(verify_api_key)):
    """Generate questions for exams via API."""
    if request.exam not in VALID_EXAMS:
        raise HTTPException(status_code=400, detail=f"Invalid exam. Valid: {VALID_EXAMS}")
    if request.subject not in VALID_SUBJECTS:
        raise HTTPException(status_code=400, detail=f"Invalid subject. Valid: {VALID_SUBJECTS}")
    if request.type not in VALID_TYPES:
        raise HTTPException(status_code=400, detail=f"Invalid type. Valid: {VALID_TYPES}")
    if request.language not in VALID_LANGUAGES:
        raise HTTPException(status_code=400, detail=f"Invalid language. Valid: {VALID_LANGUAGES}")
    if request.count < 1 or request.count > 50:
        raise HTTPException(status_code=400, detail="Count must be between 1 and 50")

    try:
        generator = get_generator(request.type)
        quiz = generator.generate(
            exam=request.exam,
            subject=request.subject,
            count=request.count,
            topic=request.topic,
        )

        questions = []
        for i, q in enumerate(quiz.items):
            questions.append(
                QuestionModel(
                    id=f"q{i+1}",
                    question=q.question,
                    options=q.options if hasattr(q, "options") else None,
                    correct_answer=q.correct_answer if hasattr(q, "correct_answer") else None,
                    explanation=q.explanation if hasattr(q, "explanation") else None,
                )
            )

        return GenerateResponse(
            status="success",
            questions=questions,
            count=len(questions),
            exam=request.exam,
            subject=request.subject,
            type=request.type,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")