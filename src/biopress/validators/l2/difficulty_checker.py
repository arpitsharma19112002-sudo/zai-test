"""L2 Difficulty Checker - validates question difficulty level."""


from biopress.core.types import ValidationResult


VALID_DIFFICULTY_LEVELS = {"easy", "medium", "hard"}


class DifficultyChecker:
    """Checks if question difficulty matches expected level."""

    DEFAULT_THRESHOLD = 70

    DIFFICULTY_SCORES = {
        "easy": 30,
        "medium": 60,
        "hard": 90,
    }

    def __init__(self, llm_adapter, threshold: int = DEFAULT_THRESHOLD):
        self.llm = llm_adapter
        self.threshold = threshold

    def check(self, question: dict, expected_level: str) -> ValidationResult:
        """Check if question difficulty matches expected level.
        
        Args:
            question: Dictionary containing question text and metadata
            expected_level: Expected difficulty level (easy/medium/hard)
            
        Returns:
            ValidationResult with score, reasons, and suggestions
        """
        expected_level = expected_level.lower()
        if expected_level not in VALID_DIFFICULTY_LEVELS:
            return ValidationResult(
                is_valid=False,
                score=0.0,
                issues=[f"Invalid difficulty level: {expected_level}"],
                suggestions=["Use 'easy', 'medium', or 'hard'"]
            )

        question_text = question.get("question", question.get("text", ""))
        if not question_text:
            return ValidationResult(
                is_valid=False,
                score=0.0,
                issues=["Question text is empty"],
                suggestions=["Provide a question text"]
            )

        prompt = self._build_prompt(question_text, expected_level)
        
        try:
            response = self.llm.generate(prompt, max_tokens=300)
            detected_level, reasoning = self._parse_response(response)
        except Exception as e:
            return ValidationResult(
                is_valid=False,
                score=0.5,
                issues=[f"LLM error: {str(e)}"],
                suggestions=["Check LLM connection"]
            )

        score_int = self._calculate_score(detected_level, expected_level)
        score = score_int / 100.0
        is_valid = score_int >= self.threshold
        
        issues = [f"Expected: {expected_level}, Detected: {detected_level}"]
        if reasoning:
            issues.append(reasoning)
        
        if not is_valid:
            suggestions = [
                f"Adjust question complexity for {expected_level} difficulty",
                "Review the question's cognitive demand",
                "Ensure question matches target grade level"
            ]
        else:
            suggestions = []

        return ValidationResult(
            is_valid=is_valid,
            score=score,
            issues=issues,
            suggestions=suggestions
        )

    def _build_prompt(self, question_text: str, expected_level: str) -> str:
        """Build validation prompt for LLM."""
        return f"""Determine the difficulty level of this question: {expected_level} (expected).

Question: {question_text}

Respond with only one word: easy, medium, or hard."""

    def _parse_response(self, response: str) -> tuple[str, str]:
        """Parse LLM response to extract difficulty level."""
        response_lower = response.lower().strip()
        
        for level in VALID_DIFFICULTY_LEVELS:
            if level in response_lower:
                return level, f"Detected as {level}"
        
        return "medium", "Default level due to parsing uncertainty"

    def _calculate_score(self, detected: str, expected: str) -> int:
        """Calculate score based on match between detected and expected difficulty."""
        if detected == expected:
            return 100
        
        expected_val = self.DIFFICULTY_SCORES.get(expected, 50)
        detected_val = self.DIFFICULTY_SCORES.get(detected, 50)
        
        difference = abs(expected_val - detected_val)
        
        if difference == 30:
            return 70
        elif difference == 60:
            return 60
        return 40


class MockLLMAdapter:
    """Mock LLM adapter for testing."""

    def generate(self, prompt: str, max_tokens: int = 1000) -> str:
        if "easy" in prompt.lower().split()[0]:
            return "easy"
        elif "medium" in prompt.lower().split()[0]:
            return "medium"
        elif "hard" in prompt.lower().split()[0]:
            return "hard"
        return "medium"