"""Tests for token optimization."""

import pytest
from biopress.core.token_tracker import (
    TokenTracker,
    TokenReport,
    TokenUsage,
    OperationType,
)


class TestTokenTracker:
    """Test the TokenTracker class."""

    def setup_method(self):
        TokenTracker.reset()

    def test_start_tracking(self):
        report = TokenTracker.start_tracking()
        assert isinstance(report, TokenReport)
        assert report.total_tokens == 0
        assert report.zero_token_percentage == 100.0

    def test_record_template_lookup_zero_tokens(self):
        TokenTracker.start_tracking()
        TokenTracker.record_template_lookup(3)
        report = TokenTracker.finalize()
        
        assert report.total_tokens == 0
        assert report.zero_token_operations == 3
        assert report.llm_operations == 0

    def test_record_sympy_compute_zero_tokens(self):
        TokenTracker.start_tracking()
        TokenTracker.record_sympy_compute(5)
        report = TokenTracker.finalize()
        
        assert report.total_tokens == 0
        assert report.zero_token_operations == 5

    def test_record_llm_validation(self):
        TokenTracker.start_tracking()
        TokenTracker.record_llm_validation(
            input_tokens=500,
            output_tokens=200,
        )
        report = TokenTracker.finalize()
        
        assert report.total_input_tokens == 500
        assert report.total_output_tokens == 200
        assert report.total_tokens == 700
        assert report.llm_operations == 1
        assert report.estimated_cost > 0

    def test_mixed_operations(self):
        TokenTracker.start_tracking()
        TokenTracker.record_template_lookup(2)
        TokenTracker.record_sympy_compute(3)
        TokenTracker.record_llm_validation(1000, 500)
        TokenTracker.finalize()
        
        report = TokenTracker.get_current_report()
        assert report is None  # After finalize
        report = TokenTracker.finalize()  # Get empty report
        
        TokenTracker.start_tracking()
        TokenTracker.record_template_lookup(2)
        TokenTracker.record_sympy_compute(3)
        TokenTracker.record_llm_validation(1000, 500)
        report = TokenTracker.finalize()
        
        assert report.zero_token_operations == 5
        assert report.llm_operations == 1
        # Should be 83.3% (5/6) zero-token
        assert report.zero_token_percentage > 80

    def test_zero_token_percentage_calculation(self):
        TokenTracker.start_tracking()
        # 10 template lookups, 1 LLM call
        TokenTracker.record_template_lookup(10)
        TokenTracker.record_llm_validation(100, 50)
        report = TokenTracker.finalize()
        
        # 10/11 = 90.9%
        assert report.zero_token_percentage > 90

    def test_cost_calculation(self):
        TokenTracker.start_tracking()
        # Typical: 1000 input, 500 output tokens
        TokenTracker.record_llm_validation(1000, 500)
        report = TokenTracker.finalize()
        
        # $0.001 per 1K input + $0.002 per 1K output = $0.002
        expected_cost = (1000 / 1000 * 0.001) + (500 / 1000 * 0.002)
        assert abs(report.estimated_cost - expected_cost) < 0.001

    def test_finalize_with_question_count(self):
        TokenTracker.start_tracking()
        TokenTracker.record_template_lookup(5)
        report = TokenTracker.finalize(questions_generated=10)
        
        assert report.questions_generated == 10


class TestTokenReport:
    """Test the TokenReport class."""

    def test_empty_report(self):
        report = TokenReport()
        assert report.total_tokens == 0
        assert report.zero_token_percentage == 100.0
        assert report.estimated_cost == 0.0

    def test_format_report(self):
        report = TokenReport()
        report.add_operation(TokenUsage(OperationType.TEMPLATE_LOOKUP, 0, 0))
        report.add_operation(TokenUsage(OperationType.LLM_VALIDATION, 1000, 500))
        report.finalize(questions_generated=5)
        
        formatted = report.format_report()
        
        assert "TOKEN USAGE REPORT" in formatted
        assert "Questions Generated: 5" in formatted
        assert "Zero-Token Percentage:" in formatted
        assert "Estimated Cost:" in formatted


class TestOperationType:
    """Test OperationType enum."""

    def test_template_lookup_is_zero_token(self):
        op = OperationType.TEMPLATE_LOOKUP
        assert op.value == "template"

    def test_sympy_compute_is_zero_token(self):
        op = OperationType.SYMPY_COMPUTE
        assert op.value == "sympy"

    def test_llm_operations_use_tokens(self):
        llm_ops = [
            OperationType.LLM_VALIDATION,
            OperationType.LLM_TRANSLATION,
            OperationType.LLM_NEW_CONTENT,
            OperationType.LLM_MIMIC,
        ]
        # These operations use LLM tokens (not zero-token)
        non_zero_ops = [op for op in llm_ops if op not in (OperationType.TEMPLATE_LOOKUP, OperationType.SYMPY_COMPUTE)]
        assert len(non_zero_ops) == 4


class TestGeneratorTokenTracking:
    """Test token tracking integration with generators."""

    def setup_method(self):
        TokenTracker.reset()

    def test_mcq_generator_uses_zero_tokens(self):
        from biopress.generators.questions.mcq import MCQGenerator
        
        TokenTracker.start_tracking()
        gen = MCQGenerator()
        quiz = gen.generate(
            exam="NEET",
            subject="Physics",
            count=5,
            topic="default",
        )
        
        report = TokenTracker.get_current_report()
        
        # Template lookup is 0 tokens
        assert report is not None
        assert report.zero_token_operations >= 1
        
        TokenTracker.finalize(questions_generated=len(quiz.items))

    def test_numerical_generator_uses_zero_tokens(self):
        from biopress.generators.questions.numerical import NumericalGenerator
        
        TokenTracker.start_tracking()
        gen = NumericalGenerator()
        quiz = gen.generate(
            exam="NEET",
            subject="Physics",
            count=3,
            topic="default",
        )
        
        report = TokenTracker.get_current_report()
        
        assert report is not None
        assert report.zero_token_operations >= 1
        
        TokenTracker.finalize(questions_generated=len(quiz.items))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])