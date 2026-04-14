"""Tests for L1 Mathematical Validator."""

import pytest
from biopress.validators.l1.math_validator import (
    MathValidator,
    evaluate_expression,
    check_answer,
    verify_solution_steps,
)
from biopress.validators.l1.unit_validator import (
    convert_units,
    check_unit_consistency,
    get_base_units,
)


class TestMathValidator:
    """Tests for MathValidator class."""

    def test_evaluate_simple_expression(self):
        """Test evaluating simple arithmetic expressions."""
        assert evaluate_expression("2 + 2") == 4.0
        assert evaluate_expression("10 - 5") == 5.0
        assert evaluate_expression("3 * 4") == 12.0
        assert evaluate_expression("20 / 4") == 5.0

    def test_evaluate_complex_expression(self):
        """Test evaluating complex mathematical expressions."""
        assert abs(evaluate_expression("sqrt(16)") - 4.0) < 1e-6
        assert abs(evaluate_expression("2**3") - 8.0) < 1e-6
        assert abs(evaluate_expression("sin(0)") - 0.0) < 1e-6

    def test_evaluate_trigonometric(self):
        """Test evaluating trigonometric expressions."""
        result = evaluate_expression("sin(pi/2)")
        assert abs(result - 1.0) < 1e-6

    def test_evaluate_logarithmic(self):
        """Test evaluating logarithmic expressions."""
        result = evaluate_expression("log(10)")
        assert abs(result - 2.302585) < 1e-3

    def test_evaluate_constants(self):
        """Test evaluating mathematical constants."""
        result = evaluate_expression("pi")
        assert abs(result - 3.14159265358979) < 1e-6
        result = evaluate_expression("E")
        assert abs(result - 2.718281828459045) < 1e-6

    def test_check_answer_correct(self):
        """Test check_answer with correct answers."""
        assert check_answer(10.0, 10.0) is True
        assert check_answer(3.14159, 3.1416, tolerance=1e-4) is True

    def test_check_answer_incorrect(self):
        """Test check_answer with incorrect answers."""
        assert check_answer(10.0, 5.0) is False

    def test_validate_numerical_answer_valid(self):
        """Test validating correct numerical answers."""
        validator = MathValidator()
        is_valid, message = validator.validate_numerical_answer("2 + 2", 4.0)
        assert is_valid is True

    def test_validate_numerical_answer_invalid(self):
        """Test validating incorrect numerical answers."""
        validator = MathValidator()
        is_valid, message = validator.validate_numerical_answer("2 + 2", 5.0)
        assert is_valid is False

    def test_verify_solution_steps(self):
        """Test verifying solution steps."""
        steps = [
            {"expression": "2 + 2", "result": 4},
            {"expression": "4 * 3", "result": 12},
        ]
        results = verify_solution_steps(steps)
        assert len(results) == 2
        assert results[0][0] is True
        assert results[1][0] is True


class TestUnitValidator:
    """Tests for UnitValidator class."""

    def test_convert_length_units(self):
        """Test converting length units."""
        result = convert_units(1.0, "km", "m")
        assert result == 1000.0

    def test_convert_velocity_units(self):
        """Test converting velocity units."""
        result = convert_units(1.0, "km/h", "m/s")
        assert abs(result - 0.277778) < 1e-5

    def test_convert_mass_units(self):
        """Test converting mass units."""
        result = convert_units(1.0, "kg", "g")
        assert result == 1000.0

    def test_convert_incompatible_units(self):
        """Test converting incompatible units raises error."""
        with pytest.raises(ValueError):
            convert_units(1.0, "m", "kg")

    def test_check_unit_consistency_valid(self):
        """Test checking unit consistency with valid units."""
        assert check_unit_consistency("velocity", "m/s") is True
        assert check_unit_consistency("force", "N") is True

    def test_check_unit_consistency_invalid(self):
        """Test checking unit consistency with invalid units."""
        assert check_unit_consistency("velocity", "kg") is False

    def test_get_base_units(self):
        """Test getting base SI units."""
        units = get_base_units("m/s")
        assert "L" in units or "T" in units


class TestL1Validator:
    """Tests for complete L1 validation."""

    def test_validate_complete_question_pass(self):
        """Test validating a complete question that passes."""
        validator = MathValidator()
        question = {
            "expression": "20 / 4",
            "expected_answer": 5.0,
            "quantity": "velocity",
            "unit": "m/s",
            "solution_steps": [
                {"expression": "20 / 4"},
            ],
        }
        result = validator.validate(question)
        assert result["status"] == "L1_PASS"
        assert len(result["errors"]) == 0

    def test_validate_complete_question_fail(self):
        """Test validating a complete question that fails."""
        validator = MathValidator()
        question = {
            "expression": "2 + 2",
            "expected_answer": 5.0,
        }
        result = validator.validate(question)
        assert result["status"] == "L1_FAIL"

    def test_validate_unit_inconsistency(self):
        """Test validating unit inconsistency."""
        validator = MathValidator()
        question = {
            "expression": "10",
            "expected_answer": 10.0,
            "quantity": "velocity",
            "unit": "kg",
        }
        result = validator.validate(question)
        assert result["status"] == "L1_FAIL"