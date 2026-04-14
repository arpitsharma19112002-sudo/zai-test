"""Syllabus data structures."""

from pydantic import BaseModel, Field
from typing import List


class Topic(BaseModel):
    """Represents a single topic in the syllabus."""
    id: str = Field(..., description="Unique topic identifier")
    name: str = Field(..., description="Topic name")
    subtopics: List[str] = Field(default_factory=list, description="List of subtopics")
    weightage: int = Field(default=0, description="Weightage percentage")
    difficulty: str = Field(default="medium", description="Difficulty level")


class Syllabus(BaseModel):
    """Represents the complete syllabus for an exam and subject."""
    exam: str = Field(..., description="Exam name (e.g., NEET)")
    subject: str = Field(..., description="Subject name (e.g., Physics)")
    topics: List[Topic] = Field(default_factory=list, description="List of topics")
    patterns: dict = Field(default_factory=dict, description="Question patterns")