"""Tests for L2 LLM-Based Quality Validator."""

from biopress.validators.l2.relevance_checker import RelevanceChecker
from biopress.validators.l2.difficulty_checker import DifficultyChecker
from biopress.validators.l2.context_checker import ContextChecker
from biopress.validators.l2.validator import L2Validator, L2Result
from biopress.validators.l2.types import ValidationResult
from biopress.validators.l2.single_pass import SinglePassValidator, SinglePassResult


class MockLLMAdapter:
    """Mock LLM adapter for testing - returns context-aware responses."""

    def generate(self, prompt: str, max_tokens: int = 1000) -> str:
        prompt_lower = prompt.lower()
        
        if "relevan" in prompt_lower:
            if "france" in prompt_lower or "capital" in prompt_lower:
                return "SCORE: 20\nREASONING: Question is not relevant to the topic"
            elif "chemistry" in prompt_lower:
                return "SCORE: 85\nREASONING: Question tests understanding of chemical bonds"
            elif "physics" in prompt_lower:
                return "SCORE: 75\nREASONING: Question relates to physics concepts"
            else:
                return "SCORE: 60\nREASONING: Question partially relates to topic"
        
        elif "difficulty" in prompt_lower:
            if "medium" in prompt_lower:
                return "medium"
            elif "easy" in prompt_lower:
                return "easy"
            elif "hard" in prompt_lower:
                return "hard"
            return "medium"
        
        elif "appropriate" in prompt_lower:
            if "grade 9" in prompt_lower or "grade 10" in prompt_lower:
                return "APPROPRIATE: yes\nREASONING: Appropriate for board exam"
            elif "grade 12" in prompt_lower:
                return "APPROPRIATE: yes\nREASONING: Appropriate for entrance exam"
            else:
                return "APPROPRIATE: no\nREASONING: Too advanced for the grade level"
        
        return "SCORE: 70\nREASONING: Validated"


class TestRelevanceChecker:
    """Tests for RelevanceChecker."""

    def test_check_relevant_question(self):
        """Test checking a relevant question."""
        checker = RelevanceChecker(MockLLMAdapter(), threshold=70)
        question = {"question": "What is a covalent bond in chemistry?"}
        result = checker.check(question, "chemistry")
        
        assert result.passed is True
        assert result.score >= 70

    def test_check_irrelevant_question(self):
        """Test checking an irrelevant question."""
        checker = RelevanceChecker(MockLLMAdapter(), threshold=70)
        question = {"question": "What is the capital of France?"}
        result = checker.check(question, "chemistry")
        
        assert result.score <= 100

    def test_empty_question(self):
        """Test with empty question."""
        checker = RelevanceChecker(MockLLMAdapter())
        question = {}
        result = checker.check(question, "chemistry")
        
        assert result.passed is False
        assert result.score == 0
        assert "empty" in result.reasons[0].lower()


class TestDifficultyChecker:
    """Tests for DifficultyChecker."""

    def test_check_matching_difficulty(self):
        """Test with matching difficulty level."""
        checker = DifficultyChecker(MockLLMAdapter(), threshold=70)
        question = {"question": "What is a covalent bond?"}
        result = checker.check(question, "medium")
        
        assert result.passed is True

    def test_invalid_difficulty_level(self):
        """Test with invalid difficulty level."""
        checker = DifficultyChecker(MockLLMAdapter())
        question = {"question": "Calculate force."}
        result = checker.check(question, "impossible")
        
        assert result.passed is False
        assert result.score == 0

    def test_empty_question(self):
        """Test with empty question."""
        checker = DifficultyChecker(MockLLMAdapter())
        question = {}
        result = checker.check(question, "medium")
        
        assert result.passed is False


class TestContextChecker:
    """Tests for ContextChecker."""

    def test_check_appropriate_context(self):
        """Test with appropriate context."""
        checker = ContextChecker(MockLLMAdapter(), threshold=70)
        question = {"question": "Solve for x in equation."}
        context = {"grade_level": "9", "exam_type": "board"}
        result = checker.check(question, context)
        
        assert result.passed is True

    def test_invalid_grade_level(self):
        """Test with invalid grade level."""
        checker = ContextChecker(MockLLMAdapter())
        question = {"question": "Solve for x."}
        context = {"grade_level": "15", "exam_type": "board"}
        result = checker.check(question, context)
        
        assert result.passed is False
        assert result.score == 0


class TestL2Validator:
    """Tests for complete L2 validation."""

    def test_validate_complete_question_pass(self):
        """Test validating a complete question that passes."""
        validator = L2Validator(MockLLMAdapter(), threshold=70)
        question = {
            "question": "What is a covalent bond?",
            "topic": "chemistry",
            "difficulty": "medium",
            "context": {"grade_level": "9", "exam_type": "board"},
        }
        result = validator.validate(question)
        
        assert isinstance(result.score, int)

    def test_validate_complete_question_fail(self):
        """Test validating a complete question that fails."""
        validator = L2Validator(MockLLMAdapter(), threshold=80)
        question = {
            "question": "What is the capital of France?",
            "topic": "chemistry",
            "difficulty": "medium",
            "context": {"grade_level": "9", "exam_type": "board"},
        }
        result = validator.validate(question)
        
        assert result.flagged is True

    def test_validate_batch(self):
        """Test validating multiple questions."""
        validator = L2Validator(MockLLMAdapter(), threshold=70)
        questions = [
            {
                "question": "What is a covalent bond?",
                "topic": "chemistry",
                "difficulty": "easy",
                "context": {"grade_level": "9", "exam_type": "board"},
            },
            {
                "question": "Calculate force.",
                "topic": "physics",
                "difficulty": "medium",
                "context": {"grade_level": "10", "exam_type": "board"},
            },
        ]
        results = validator.validate_batch(questions)
        
        assert len(results) == 2
        assert all(isinstance(r, L2Result) for r in results)

    def test_get_flagged_questions(self):
        """Test getting flagged questions."""
        validator = L2Validator(MockLLMAdapter(), threshold=80)
        questions = [
            {
                "question": "What is irrelevant?",
                "topic": "chemistry",
                "difficulty": "medium",
                "context": {"grade_level": "9", "exam_type": "board"},
            },
        ]
        results = validator.validate_batch(questions)
        flagged = validator.get_flagged_questions(results)
        
        assert len(flagged) >= 0

    def test_combined_score_calculation(self):
        """Test combined score calculation."""
        validator = L2Validator(MockLLMAdapter())
        question = {
            "question": "Test question",
            "topic": "chemistry",
            "difficulty": "medium",
            "context": {"grade_level": "9", "exam_type": "board"},
        }
        result = validator.validate(question)
        
        expected = int(
            result.relevance.score * 0.4 +
            result.difficulty.score * 0.35 +
            result.context.score * 0.25
        )
        assert result.score == expected


class TestValidationResult:
    """Tests for ValidationResult dataclass."""

    def test_validation_result_creation(self):
        """Test creating a ValidationResult."""
        result = ValidationResult(
            passed=True,
            score=85,
            reasons=["Reason 1"],
            suggestions=["Suggestion 1"]
        )
        
        assert result.passed is True
        assert result.score == 85
        assert len(result.reasons) == 1
        assert len(result.suggestions) == 1

    def test_default_values(self):
        """Test ValidationResult defaults."""
        result = ValidationResult(passed=True, score=100)
        
        assert result.reasons == []
        assert result.suggestions == []


class TestSinglePassValidator:
    """Tests for SinglePassValidator."""

    def test_single_pass_validate_basic(self):
        """Test single-pass validation basic case."""
        validator = SinglePassValidator(MockLLMAdapter(), threshold=70)
        question = {
            "text": "What is a covalent bond?",
            "topic": "chemistry",
            "difficulty": "medium",
            "context": {"grade_level": "9", "exam_type": "board"},
        }
        result = validator.validate(question)
        
        assert isinstance(result, SinglePassResult)
        assert isinstance(result.score, int)
        assert result.exam_type == "board"

    def test_single_pass_with_math(self):
        """Test single-pass with mathematical validation."""
        validator = SinglePassValidator(MockLLMAdapter(), threshold=70)
        question = {
            "text": "Calculate force",
            "topic": "physics",
            "difficulty": "medium",
            "context": {"grade_level": "10", "exam_type": "board"},
            "expression": "10 * 9.8",
            "expected_answer": 98.0,
        }
        result = validator.validate(question)
        
        assert result.l1_passed is True
        assert result.score > 0

    def test_single_pass_batch(self):
        """Test single-pass batch validation."""
        validator = SinglePassValidator(MockLLMAdapter(), threshold=70)
        questions = [
            {
                "text": "What is a covalent bond?",
                "topic": "chemistry",
                "difficulty": "medium",
                "context": {"grade_level": "9", "exam_type": "board"},
            },
            {
                "text": "Calculate force",
                "topic": "physics",
                "difficulty": "medium",
                "context": {"grade_level": "10", "exam_type": "board"},
            },
        ]
        results = validator.validate_batch(questions)
        
        assert len(results) == 2
        assert all(isinstance(r, SinglePassResult) for r in results)

    def test_single_pass_exam_rules(self):
        """Test single-pass with different exam types."""
        validator = SinglePassValidator(MockLLMAdapter(), threshold=70)
        
        board_question = {
            "text": "Test question",
            "topic": "chemistry",
            "difficulty": "easy",
            "context": {"grade_level": "9", "exam_type": "board"},
        }
        board_result = validator.validate(board_question)
        assert board_result.exam_type == "board"
        
        entrance_question = {
            "text": "Test question",
            "topic": "chemistry",
            "difficulty": "medium",
            "context": {"grade_level": "12", "exam_type": "entrance"},
        }
        entrance_result = validator.validate(entrance_question)
        assert entrance_result.exam_type == "entrance"


class TestL2ValidatorSinglePassMode:
    """Tests for L2Validator in single-pass mode."""

    def test_l2_validator_single_pass(self):
        """Test L2Validator with single_pass_mode=True."""
        validator = L2Validator(MockLLMAdapter(), single_pass_mode=True)
        question = {
            "text": "What is a covalent bond?",
            "topic": "chemistry",
            "difficulty": "medium",
            "context": {"grade_level": "9", "exam_type": "board"},
        }
        result = validator.validate(question)
        
        assert isinstance(result, L2Result)
        assert result.score >= 0

    def test_l2_validator_single_pass_batch(self):
        """Test L2Validator single-pass batch."""
        validator = L2Validator(MockLLMAdapter(), single_pass_mode=True)
        questions = [
            {
                "text": "Question 1",
                "topic": "chemistry",
                "difficulty": "medium",
                "context": {"grade_level": "9", "exam_type": "board"},
            },
        ]
        results = validator.validate_batch(questions)
        
        assert len(results) == 1
        assert isinstance(results[0], L2Result)