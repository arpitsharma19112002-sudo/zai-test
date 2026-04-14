"""Pydantic schemas for API request/response models."""

from typing import List, Optional
from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    exam: str = Field(default="NEET", description="Exam type (NEET, JEE, CBSE)")
    subject: str = Field(default="Physics", description="Subject (Physics, Chemistry, Biology)")
    type: str = Field(default="mcq", description="Question type (mcq, numerical, case-based, assertion-reason)")
    count: int = Field(default=10, ge=1, le=50, description="Number of questions to generate")
    topic: Optional[str] = Field(default=None, description="Topic to generate questions for")
    language: str = Field(default="english", description="Language for content (english, hindi)")


class QuestionModel(BaseModel):
    id: str
    question: str
    options: Optional[List[str]] = None
    correct_answer: Optional[str] = None
    explanation: Optional[str] = None


class GenerateResponse(BaseModel):
    status: str
    questions: List[QuestionModel]
    count: int
    exam: str
    subject: str
    type: str
    format: str = Field(default="perseus", description="Response format")


class ValidateRequest(BaseModel):
    questions: List[QuestionModel]
    level: str = Field(default="l2", description="Validation level (l1, l2)")


class ValidationIssue(BaseModel):
    question_id: str
    issue_type: str
    severity: str
    message: str


class ValidateResponse(BaseModel):
    status: str
    issues: List[ValidationIssue]
    total_questions: int
    valid_count: int


class PDFRequest(BaseModel):
    questions: List[QuestionModel]
    style: str = Field(default="default", description="PDF style (default, ncert, neet)")
    title: Optional[str] = Field(default=None, description="PDF title")
    include_answers: bool = Field(default=True, description="Include answer key")


class PDFResponse(BaseModel):
    status: str
    message: str
    file_path: Optional[str] = None