"""L2 Context Checker - validates question context appropriateness."""

import re

from biopress.core.types import ValidationResult


VALID_GRADE_LEVELS = {"1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"}
VALID_EXAM_TYPES = {"board", "entrance", "olympiad", "unit test", "midterm", "final"}


class ContextChecker:
    """Checks if question context is appropriate (grade level, exam type, etc.)."""

    DEFAULT_THRESHOLD = 70

    GRADE_TO_SCORE = {
        (1, 5): 70,
        (6, 8): 60,
        (9, 10): 50,
        (11, 12): 40,
    }

    def __init__(self, llm_adapter, threshold: int = DEFAULT_THRESHOLD):
        self.llm = llm_adapter
        self.threshold = threshold

    def check(self, question: dict, context: dict) -> ValidationResult:
        """Check if question context is appropriate.
        
        Args:
            question: Dictionary containing question text and metadata
            context: Context dict with grade_level, exam_type, etc.
            
        Returns:
            ValidationResult with score, reasons, and suggestions
        """
        question_text = question.get("question", question.get("text", ""))
        if not question_text:
            return ValidationResult(
                is_valid=False,
                score=0.0,
                issues=["Question text is empty"],
                suggestions=["Provide a question text"]
            )

        grade_level = context.get("grade_level", "9")
        exam_type = context.get("exam_type", "board")

        grade_valid = self._validate_grade_level(grade_level)
        if not grade_valid:
            return ValidationResult(
                is_valid=False,
                score=0.0,
                issues=[f"Invalid grade level: {grade_level}"],
                suggestions=[f"Use valid grade level: {', '.join(VALID_GRADE_LEVELS)}"]
            )

        prompt = self._build_prompt(question_text, grade_level, exam_type)
        
        try:
            response = self.llm.generate(prompt, max_tokens=300)
            appropriate, reasoning = self._parse_response(response)
        except Exception as e:
            return ValidationResult(
                is_valid=False,
                score=0.5,
                issues=[f"LLM error: {str(e)}"],
                suggestions=["Check LLM connection"]
            )

        score_int = self._calculate_score(appropriate, grade_level, exam_type)
        score = score_int / 100.0
        is_valid = score_int >= self.threshold
        
        issues = [
            f"Grade: {grade_level}, Exam: {exam_type}",
            reasoning if reasoning else "Context check completed"
        ]
        
        if not is_valid:
            suggestions = [
                "Ensure question is appropriate for the grade level",
                f"Adjust complexity for {exam_type} exam type",
                "Verify question matches curriculum requirements"
            ]
        else:
            suggestions = []

        return ValidationResult(
            is_valid=is_valid,
            score=score,
            issues=issues,
            suggestions=suggestions
        )

    def _validate_grade_level(self, grade_level: str) -> bool:
        """Validate grade level format."""
        return grade_level in VALID_GRADE_LEVELS

    def _build_prompt(self, question_text: str, grade_level: str, exam_type: str) -> str:
        """Build validation prompt for LLM."""
        return f"""Evaluate if this question is appropriate for grade {grade_level} {exam_type} exam.

Question: {question_text}

Respond with:
APPROPRIATE: yes or no
REASONING: <brief explanation>"""

    def _parse_response(self, response: str) -> tuple[bool, str]:
        """Parse LLM response to extract appropriateness."""
        response_lower = response.lower()
        
        appropriate = True
        if "inappropriate" in response_lower or "no" in response_lower.split()[0:2]:
            appropriate = False
        
        reason_match = re.search(r"reasoning:\s*(.+)", response_lower, re.DOTALL)
        reasoning = reason_match.group(1).strip() if reason_match else ""
        
        return appropriate, reasoning

    def _calculate_score(self, appropriate: bool, grade_level: str, exam_type: str) -> int:
        """Calculate score based on context appropriateness."""
        if appropriate:
            return 100
        
        try:
            grade = int(grade_level)
        except ValueError:
            return 50
        
        for (low, high), score in self.GRADE_TO_SCORE.items():
            if low <= grade <= high:
                return score
        
        return 50


class MockLLMAdapter:
    """Mock LLM adapter for testing."""

    def generate(self, prompt: str, max_tokens: int = 1000) -> str:
        if "grade 9" in prompt.lower() or "grade 10" in prompt.lower():
            return "APPROPRIATE: yes\nREASONING: Appropriate for board exam"
        elif "grade 12" in prompt.lower():
            return "APPROPRIATE: yes\nREASONING: Appropriate for entrance exam"
        else:
            return "APPROPRIATE: no\nREASONING: Too advanced for the grade level"