"""L2 Validator - combines all L2 quality checks with async support."""

import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass

from biopress.validators.l2.relevance_checker import RelevanceChecker
from biopress.validators.l2.difficulty_checker import DifficultyChecker
from biopress.validators.l2.context_checker import ContextChecker
from biopress.validators.l2.single_pass import (
    SinglePassValidator,
)
from biopress.core.types import ValidationResult, L2Result

logger = logging.getLogger(__name__)


class L2Validator:
    """Main L2 validator that runs all quality checks with async support."""

    DEFAULT_THRESHOLD = 0.7

    def __init__(
        self,
        llm_adapter,
        threshold: float = DEFAULT_THRESHOLD,
        relevance_threshold: float = DEFAULT_THRESHOLD,
        difficulty_threshold: float = DEFAULT_THRESHOLD,
        context_threshold: float = DEFAULT_THRESHOLD,
        single_pass_mode: bool = False,
        max_workers: int = 4,
    ):
        self.llm = llm_adapter
        # Thresholds can be passed as 0-100 or 0.0-1.0
        self.threshold = threshold if threshold <= 1.0 else threshold / 100.0
        self.single_pass_mode = single_pass_mode
        self.max_workers = max_workers
        self._executor = ThreadPoolExecutor(max_workers=max_workers)

        rel_t = relevance_threshold if relevance_threshold <= 1.0 else relevance_threshold
        diff_t = difficulty_threshold if difficulty_threshold <= 1.0 else difficulty_threshold
        ctx_t = context_threshold if context_threshold <= 1.0 else context_threshold

        if single_pass_mode:
            self.single_validator = SinglePassValidator(llm_adapter, int(self.threshold * 100))
        else:
            self.relevance = RelevanceChecker(llm_adapter, int(rel_t))
            self.difficulty = DifficultyChecker(llm_adapter, int(diff_t))
            self.context = ContextChecker(llm_adapter, int(ctx_t))

    def validate(self, question: dict) -> L2Result:
        """Validate a question against all L2 checks.
        
        Args:
            question: Dictionary containing question with keys like:
                - question/text: question text
                - topic: topic for relevance check
                - difficulty: expected difficulty level
                - context: dict with grade_level, exam_type, etc.
                
        Returns:
            L2Result with all check results and combined score
        """
        if self.single_pass_mode:
            return self._validate_single_pass(question)

        topic = question.get("topic", "")
        expected_difficulty = question.get("difficulty", "medium")
        context = question.get("context", {"grade_level": "9", "exam_type": "board"})

        relevance_result = self.relevance.check(question, topic)
        difficulty_result = self.difficulty.check(question, expected_difficulty)
        context_result = self.context.check(question, context)

        combined_score = self._calculate_combined_score(
            relevance_result,
            difficulty_result,
            context_result
        )

        overall_pass = (
            relevance_result.is_valid and
            difficulty_result.is_valid and
            context_result.is_valid and
            combined_score >= self.threshold
        )

        flagged = combined_score < self.threshold

        return L2Result(
            relevance=relevance_result,
            difficulty=difficulty_result,
            context=context_result,
            overall_pass=overall_pass,
            score=combined_score,
            flagged=flagged
        )

    def _calculate_combined_score(
        self,
        relevance: ValidationResult,
        difficulty: ValidationResult,
        context: ValidationResult
    ) -> float:
        """Calculate combined score from all checks."""
        weights = {
            "relevance": 0.4,
            "difficulty": 0.35,
            "context": 0.25,
        }
        
        score = (
            relevance.score * weights["relevance"] +
            difficulty.score * weights["difficulty"] +
            context.score * weights["context"]
        )
        
        return score

    def validate_batch(self, questions: list[dict]) -> list[L2Result]:
        """Validate multiple questions.
        
        Args:
            questions: List of question dictionaries
            
        Returns:
            List of L2Result for each question
        """
        if self.single_pass_mode:
            return self._batch_single_pass(questions)
        
        results = []
        for question in questions:
            result = self.validate(question)
            results.append(result)
        return results

    def _batch_single_pass(self, questions: list[dict]) -> list[L2Result]:
        """Batch validation in single-pass mode."""
        results = self.single_validator.validate_batch(questions)
        l2_results = []
        for result in results:
            l2_results.append(L2Result(
                relevance=ValidationResult(
                    is_valid=result.l2_valid,
                    score=result.score,
                    issues=result.issues,
                    suggestions=result.suggestions,
                ),
                difficulty=ValidationResult(
                    is_valid=result.l2_valid,
                    score=result.score,
                    issues=result.issues,
                    suggestions=result.suggestions,
                ),
                context=ValidationResult(
                    is_valid=result.l1_valid,
                    score=result.score,
                    issues=result.issues,
                    suggestions=result.suggestions,
                ),
                overall_pass=result.is_valid,
                score=result.score,
                flagged=not result.is_valid,
            ))
        return l2_results

    async def _validate_async(self, question: dict) -> L2Result:
        """Async validation for a single question."""
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(self._executor, self.validate, question)
        return result

    async def validate_batch_async(self, questions: list[dict]) -> list[L2Result]:
        """Validate multiple questions concurrently.

        Args:
            questions: List of question dictionaries

        Returns:
            List of L2Result for each question
        """
        tasks = [self._validate_async(q) for q in questions]
        results = await asyncio.gather(*tasks)
        return list(results)

    def _validate_single_pass(self, question: dict) -> L2Result:
        """Single-pass validation combining L1+L2."""
        result = self.single_validator.validate(question)
        
        return L2Result(
            relevance=ValidationResult(
                is_valid=result.l2_valid,
                score=result.score,
                issues=result.issues,
                suggestions=result.suggestions,
            ),
            difficulty=ValidationResult(
                is_valid=result.l2_valid,
                score=result.score,
                issues=result.issues,
                suggestions=result.suggestions,
            ),
            context=ValidationResult(
                is_valid=result.l1_valid,
                score=result.score,
                issues=result.issues,
                suggestions=result.suggestions,
            ),
            overall_pass=result.is_valid,
            score=result.score,
            flagged=not result.is_valid,
        )

    def get_flagged_questions(self, results: list[L2Result]) -> list[tuple[int, L2Result]]:
        """Get list of flagged questions (below threshold).
        
        Args:
            results: List of L2Result from validate_batch
            
        Returns:
            List of (index, result) tuples for flagged questions
        """
        flagged = []
        for i, result in enumerate(results):
            if result.flagged:
                flagged.append((i, result))
        return flagged


class MockLLMAdapter:
    """Mock LLM adapter for testing."""

    def generate(self, prompt: str, max_tokens: int = 1000) -> str:
        prompt_lower = prompt.lower()
        
        if "relevan" in prompt_lower:
            if "chemistry" in prompt_lower:
                return "SCORE: 85\nREASONING: Question tests understanding of chemical bonds"
            elif "physics" in prompt_lower:
                return "SCORE: 75\nREASONING: Question relates to physics concepts"
            else:
                return "SCORE: 60\nREASONING: Question partially relates to topic"
        
        elif "difficulty" in prompt_lower:
            if "easy" in prompt_lower.split()[0]:
                return "easy"
            elif "medium" in prompt_lower.split()[0]:
                return "medium"
            elif "hard" in prompt_lower.split()[0]:
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


def create_l2_validator(
    llm_adapter=None,
    threshold: int = L2Validator.DEFAULT_THRESHOLD,
    single_pass_mode: bool = False,
) -> L2Validator:
    """Factory function to create L2Validator with defaults."""
    if llm_adapter is None:
        llm_adapter = MockLLMAdapter()
    return L2Validator(llm_adapter, threshold, single_pass_mode=single_pass_mode)