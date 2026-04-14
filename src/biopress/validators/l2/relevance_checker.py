"""L2 Relevance Checker - validates question relevance to topic."""

import re

from biopress.core.types import ValidationResult


class RelevanceChecker:
    """Checks if question is relevant to the given topic."""

    DEFAULT_THRESHOLD = 70

    def __init__(self, llm_adapter, threshold: int = DEFAULT_THRESHOLD):
        self.llm = llm_adapter
        self.threshold = threshold

    def check(self, question: dict, topic: str) -> ValidationResult:
        """Check if question is relevant to topic.
        
        Args:
            question: Dictionary containing question text and metadata
            topic: The topic to check relevance against
            
        Returns:
            ValidationResult with score (0-100), reasons, and suggestions
        """
        question_text = question.get("question", question.get("text", ""))
        if not question_text:
            return ValidationResult(
                is_valid=False,
                score=0.0,
                issues=["Question text is empty"],
                suggestions=["Provide a question text"]
            )

        prompt = self._build_prompt(question_text, topic)
        
        try:
            response = self.llm.generate(prompt, max_tokens=500)
            score_int, reasoning = self._parse_response(response)
        except Exception as e:
            return ValidationResult(
                is_valid=False,
                score=0.5,
                issues=[f"LLM error: {str(e)}"],
                suggestions=["Check LLM connection"]
            )

        score = score_int / 100.0
        is_valid = score_int >= self.threshold
        issues = [reasoning] if reasoning else ["Relevance check completed"]
        
        if not is_valid:
            suggestions = [
                "Ensure question directly relates to the topic",
                "Add topic-specific keywords to the question",
                "Verify question tests understanding of the topic concept"
            ]
        else:
            suggestions = []

        return ValidationResult(
            is_valid=is_valid,
            score=score,
            issues=issues,
            suggestions=suggestions
        )

    def _build_prompt(self, question_text: str, topic: str) -> str:
        """Build validation prompt for LLM."""
        return f"""Evaluate if the following question is relevant to the topic "{topic}".

Question: {question_text}

Provide a relevance score from 0-100 and brief reasoning.
Format your response as:
SCORE: <number>
REASONING: <brief explanation>"""

    def _parse_response(self, response: str) -> tuple[int, str]:
        """Parse LLM response to extract score and reasoning."""
        score = 50
        reasoning = ""
        
        score_match = re.search(r"SCORE:\s*(\d+)", response, re.IGNORECASE)
        if score_match:
            score = min(100, max(0, int(score_match.group(1))))
        
        reason_match = re.search(r"REASONING:\s*(.+)", response, re.IGNORECASE | re.DOTALL)
        if reason_match:
            reasoning = reason_match.group(1).strip()
        
        if score == 50 and not reasoning:
            reasoning = "Default score due to parsing failure"
        
        return score, reasoning


class MockLLMAdapter:
    """Mock LLM adapter for testing."""

    def generate(self, prompt: str, max_tokens: int = 1000) -> str:
        if "chemistry" in prompt.lower():
            return "SCORE: 85\nREASONING: Question tests understanding of chemical bonds"
        elif "physics" in prompt.lower():
            return "SCORE: 75\nREASONING: Question relates to physics concepts"
        else:
            return "SCORE: 60\nREASONING: Question partially relates to topic"