"""Core data models for BioPress."""

from pydantic import BaseModel, Field
from enum import Enum


class ExamType(str, Enum):
    """Supported exam types."""
    NEET = "NEET"
    JEE = "JEE"
    CBSE = "CBSE"


class Subject(str, Enum):
    """Supported subjects."""
    Physics = "Physics"
    Chemistry = "Chemistry"
    Biology = "Biology"


class QuestionType(str, Enum):
    """Supported question types."""
    mcq = "mcq"
    numerical = "numerical"
    case_based = "case-based"
    assertion_reason = "assertion-reason"


class MCQOptions(BaseModel):
    """Multiple choice options."""
    A: str
    B: str
    C: str
    D: str


class MCQItem(BaseModel):
    """Single MCQ question in Perseus format."""
    question: str
    options: MCQOptions
    correct_answer: str
    explanation: str


class PerseusQuiz(BaseModel):
    """Perseus JSON format for quiz export."""
    items: list[MCQItem] = Field(default_factory=list)


class NumericalItem(BaseModel):
    """Numerical question with step-by-step solution."""
    question: str
    answer: float | int
    solution_steps: list[str]
    units: str = ""


class NumericalQuiz(BaseModel):
    """Quiz containing numerical questions."""
    items: list[NumericalItem] = Field(default_factory=list)


class CaseBasedSubQuestion(BaseModel):
    """Sub-question in case-based question."""
    question: str
    answer: str


class CaseBasedItem(BaseModel):
    """Case-based question with passage and sub-questions."""
    passage: str
    questions: list[CaseBasedSubQuestion]


class CaseBasedQuiz(BaseModel):
    """Quiz containing case-based questions."""
    items: list[CaseBasedItem] = Field(default_factory=list)


class AssertionReasonItem(BaseModel):
    """Assertion-Reason question in NEET format."""
    assertion: str
    reason: str
    correct_option: str
    explanation: str = ""


class AssertionReasonQuiz(BaseModel):
    """Quiz containing assertion-reason questions."""
    items: list[AssertionReasonItem] = Field(default_factory=list)


class BatchQuiz(BaseModel):
    """Batch quiz containing multiple question types."""
    items: list = Field(default_factory=list)
    type_counts: dict = Field(default_factory=dict)
    generation_time: float = 0.0
    metrics: dict = Field(default_factory=dict)