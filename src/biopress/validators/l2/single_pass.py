"""Single-Pass L2 Validator - validates in one pass without rejection loops."""

from dataclasses import dataclass, field

from biopress.validators.l2.types import ValidationResult


EXAM_RULES = {
    "board": {
        "topics_weight": 0.4,
        "difficulty_range": ("easy", "medium"),
        "requires_context": True,
    },
    "entrance": {
        "topics_weight": 0.35,
        "difficulty_range": ("medium", "hard"),
        "requires_context": True,
    },
    "olympiad": {
        "topics_weight": 0.3,
        "difficulty_range": ("hard",),
        "requires_context": False,
    },
}


@dataclass
class SinglePassResult:
    """Result of single-pass validation."""
    is_valid: bool
    score: float
    l1_valid: bool
    l2_valid: bool
    issues: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)
    exam_type: str = "board"
    rules_used: str = ""


class SinglePassValidator:
    """Single-pass validation combining L1 and L2 checks in one call."""

    DEFAULT_THRESHOLD = 0.7

    def __init__(
        self,
        llm_adapter,
        threshold: float = DEFAULT_THRESHOLD,
    ):
        self.llm = llm_adapter
        self.threshold = threshold if threshold <= 1.0 else threshold / 100.0

    def validate(self, question: dict) -> SinglePassResult:
        """Validate question in single pass without rejection loops.

        Args:
            question: Dictionary with:
                - text/question: question text
                - topic: topic for relevance
                - difficulty: expected difficulty
                - context: dict with grade_level, exam_type
                - expression: (optional) math expression
                - expected_answer: (optional) numeric answer

        Returns:
            SinglePassResult with L1+L2 combined validation
        """
        exam_type = question.get("context", {}).get("exam_type", "board")
        if not exam_type:
            exam_type = "board"

        rules = EXAM_RULES.get(exam_type, EXAM_RULES["board"])

        l1_result = self._validate_l1(question)
        l2_result = self._validate_l2(question, rules)

        l1_valid = l1_result.is_valid
        l2_valid = l2_result.is_valid

        combined_score = self._calculate_combined_score(l1_result, l2_result, rules)
        is_valid = l1_valid and l2_valid and combined_score >= self.threshold

        issues = l1_result.issues + l2_result.issues
        suggestions = l1_result.suggestions + l2_result.suggestions

        return SinglePassResult(
            is_valid=is_valid,
            score=combined_score,
            l1_valid=l1_valid,
            l2_valid=l2_valid,
            issues=issues,
            suggestions=suggestions,
            exam_type=exam_type,
            rules_used=exam_type,
        )

    def _validate_l1(self, question: dict) -> ValidationResult:
        """Run L1 (mathematical) validation."""
        from sympy import sympify, N

        issues = []
        suggestions = []
        score_int = 100

        expression = question.get("expression", "")
        expected_answer = question.get("expected_answer")

        if expression and expected_answer is not None:
            try:
                evaluated = float(N(sympify(expression)))
                expected = float(expected_answer)
                if abs(evaluated - expected) < 1e-6:
                    issues.append("L1: Mathematical answer correct")
                else:
                    score_int = 0
                    issues.append(f"L1: Answer mismatch (expected {expected}, got {evaluated})")
                    suggestions.append("Fix the mathematical expression or expected answer")
            except Exception as e:
                score_int = 50
                issues.append(f"L1: Math evaluation error - {str(e)}")
                suggestions.append("Check mathematical expression syntax")
        elif expression:
            try:
                sympify(expression)
                issues.append("L1: Mathematical expression valid")
            except Exception as e:
                score_int = 50
                issues.append(f"L1: Invalid expression - {str(e)}")
                suggestions.append("Fix mathematical expression")
        else:
            issues.append("L1: No mathematical validation needed")

        return ValidationResult(
            is_valid=score_int >= (self.threshold * 100),
            score=score_int / 100.0,
            issues=issues,
            suggestions=suggestions,
        )

    def _validate_l2(self, question: dict, rules: dict) -> ValidationResult:
        """Run L2 (quality) validation in single pass."""
        issues = []
        suggestions = []
        total_score_int = 0
        checks_performed = 0

        topic = question.get("topic", "")
        question_text = question.get("text", question.get("question", ""))
        expected_difficulty = question.get("difficulty", "medium")
        context = question.get("context", {})

        if topic and question_text:
            prompt = self._build_relevance_prompt(question_text, topic)
            try:
                response = self.llm.generate(prompt, max_tokens=300)
                score_int, reasoning = self._parse_llm_response(response)
                total_score_int += score_int
                checks_performed += 1
                issues.append(f"Relevance: {reasoning}")
            except Exception as e:
                total_score_int += 50
                checks_performed += 1
                issues.append(f"Relevance check failed: {str(e)}")

        if expected_difficulty:
            prompt = self._build_difficulty_prompt(question_text, expected_difficulty)
            try:
                response = self.llm.generate(prompt, max_tokens=200)
                score_int, reasoning = self._parse_llm_response(response)
                total_score_int += score_int
                checks_performed += 1
                issues.append(f"Difficulty: {reasoning}")
            except Exception:
                total_score_int += 50
                checks_performed += 1

        if rules.get("requires_context") and context:
            prompt = self._build_context_prompt(question_text, context)
            try:
                response = self.llm.generate(prompt, max_tokens=200)
                score_int, reasoning = self._parse_llm_response(response)
                total_score_int += score_int
                checks_performed += 1
                issues.append(f"Context: {reasoning}")
            except Exception:
                total_score_int += 50
                checks_performed += 1
        else:
            total_score_int += 70
            checks_performed += 1

        avg_score_int = total_score_int // checks_performed if checks_performed > 0 else 50
        is_valid = avg_score_int >= (self.threshold * 100)

        if not is_valid:
            suggestions.extend([
                "Ensure question directly relates to topic",
                "Adjust difficulty to match exam level",
                "Verify content is appropriate for grade level",
            ])

        return ValidationResult(
            is_valid=is_valid,
            score=avg_score_int / 100.0,
            issues=issues,
            suggestions=suggestions,
        )

    def _calculate_combined_score(
        self, l1: ValidationResult, l2: ValidationResult, rules: dict
    ) -> float:
        """Calculate combined L1+L2 score."""
        l1_weight = 0.25
        l2_weight = 0.75

        return l1.score * l1_weight + l2.score * l2_weight

    def _build_relevance_prompt(self, question_text: str, topic: str) -> str:
        """Build relevance check prompt."""
        return f"""Evaluate if question is relevant to topic "{topic}".

Question: {question_text}

Respond with:
SCORE: <0-100>
REASONING: <brief explanation>"""

    def _build_difficulty_prompt(self, question_text: str, expected: str) -> str:
        """Build difficulty check prompt."""
        return f"""Evaluate if question difficulty matches "{expected}" level.

Question: {question_text}

Respond with:
SCORE: <0-100>
REASONING: <brief explanation>"""

    def _build_context_prompt(self, question_text: str, context: dict) -> str:
        """Build context appropriateness prompt."""
        grade = context.get("grade_level", "9")
        exam = context.get("exam_type", "board")
        return f"""Evaluate if question is appropriate for grade {grade} {exam} exam.

Question: {question_text}

Respond with:
SCORE: <0-100>
REASONING: <brief explanation>"""

    def _parse_llm_response(self, response: str) -> tuple[int, str]:
        """Parse LLM response to extract score and reasoning."""
        import re

        score = 50
        reasoning = ""

        score_match = re.search(r"SCORE:\s*(\d+)", response, re.IGNORECASE)
        if score_match:
            score = min(100, max(0, int(score_match.group(1))))

        reason_match = re.search(r"REASONING:\s*(.+)", response, re.IGNORECASE | re.DOTALL)
        if reason_match:
            reasoning = reason_match.group(1).strip()

        return score, reasoning or "Validation completed"

    def validate_batch(self, questions: list[dict]) -> list[SinglePassResult]:
        """Validate multiple questions in single pass each.

        Args:
            questions: List of question dictionaries

        Returns:
            List of SinglePassResult for each question
        """
        return [self.validate(q) for q in questions]


class MockLLMAdapter:
    """Mock LLM adapter for testing."""

    def generate(self, prompt: str, max_tokens: int = 1000) -> str:
        prompt_lower = prompt.lower()

        if "relevan" in prompt_lower:
            return "SCORE: 85\nREASONING: Question directly relates to topic"
        elif "difficulty" in prompt_lower:
            return "SCORE: 75\nREASONING: Appropriate difficulty level"
        elif "appropriate" in prompt_lower or "grade" in prompt_lower:
            return "SCORE: 80\nREASONING: Appropriate for grade level"
        else:
            return "SCORE: 70\nREASONING: Validated"


def create_single_pass_validator(
    llm_adapter=None,
    threshold: int = SinglePassValidator.DEFAULT_THRESHOLD,
) -> SinglePassValidator:
    """Factory function to create SinglePassValidator."""
    if llm_adapter is None:
        llm_adapter = MockLLMAdapter()
    return SinglePassValidator(llm_adapter, threshold)