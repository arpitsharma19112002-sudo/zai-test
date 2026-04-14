"""L1 Mathematical Validator using SymPy with performance optimization."""

import logging
from typing import Any

from sympy import N, sympify

logger = logging.getLogger(__name__)


_evaluation_cache = {}


class MathValidator:
    """Validates mathematical expressions and answers using SymPy with caching."""

    def evaluate_expression(self, expr: str) -> float:
        """
        Evaluate a mathematical expression using SymPy (cached).

        Args:
            expr: Mathematical expression as a string

        Returns:
            Evaluated result as float

        Raises:
            ValueError: If expression cannot be evaluated
        """
        global _evaluation_cache

        if expr in _evaluation_cache:
            return _evaluation_cache[expr]

        try:
            sympy_expr = sympify(expr)
            result = N(sympy_expr)
            float_result = float(result)

            if len(_evaluation_cache) < 4096:
                _evaluation_cache[expr] = float_result

            return float_result
        except Exception as e:
            raise ValueError(f"Cannot evaluate expression '{expr}': {str(e)}")

    def validate_numerical_answer(
        self, expression: str, expected_answer: float, tolerance: float = 1e-6
    ) -> tuple[bool, str]:
        """
        Validate if a mathematical expression evaluates to the expected answer.

        Args:
            expression: The mathematical expression to evaluate
            expected_answer: The expected numerical answer
            tolerance: Allowed numerical tolerance

        Returns:
            Tuple of (is_valid, message)
        """
        try:
            evaluated = self.evaluate_expression(expression)
            return self._check_answer(evaluated, expected_answer, tolerance)
        except Exception as e:
            return False, f"Failed to evaluate expression: {str(e)}"

    def _check_answer(
        self, numerical_answer: float, expected: float, tolerance: float = 1e-6
    ) -> tuple[bool, str]:
        diff = abs(numerical_answer - expected)
        if diff <= tolerance:
            return True, f"Answer correct (difference: {diff:.2e})"
        return False, f"Answer incorrect (expected: {expected}, got: {numerical_answer}, diff: {diff:.2e})"

    def verify_solution_steps(self, steps: list[dict[str, Any]]) -> list[tuple[bool, str]]:
        results = []
        for i, step in enumerate(steps):
            expr = step.get("expression", "")
            try:
                result = self.evaluate_expression(expr)
                results.append((True, f"Step {i + 1}: {expr} = {result}"))
            except Exception as e:
                results.append((False, f"Step {i + 1}: Invalid - {str(e)}"))
        return results

    def validate_units(self, quantity: str, unit: str) -> tuple[bool, str]:
        unit_map = {
            "velocity": ["m/s", "km/h", "cm/s", "mm/s", "km/s"],
            "acceleration": ["m/s^2", "cm/s^2", "km/h^2"],
            "force": ["N", "kN", "dyn", "lbf"],
            "energy": ["J", "kJ", "cal", "kcal", "eV"],
            "power": ["W", "kW", "MW"],
            "pressure": ["Pa", "kPa", "atm", "bar", "mmHg"],
            "mass": ["kg", "g", "mg", "tonne"],
            "length": ["m", "cm", "mm", "km"],
            "time": ["s", "min", "h", "ms"],
            "temperature": ["K", "C", "F"],
        }

        quantity_lower = quantity.lower()
        if quantity_lower in unit_map:
            if unit.lower() in [u.lower() for u in unit_map[quantity_lower]]:
                return True, f"Unit '{unit}' is valid for quantity '{quantity}'"
            return False, f"Unit '{unit}' is not valid for quantity '{quantity}'"

        return True, f"Unknown quantity '{quantity}', skipping unit validation"

    def validate(self, question: dict[str, Any]) -> dict[str, Any]:
        result = {
            "status": "L1_PASS",
            "checks": {},
            "errors": [],
        }

        if "expected_answer" in question and "expression" in question:
            is_valid, message = self.validate_numerical_answer(
                question["expression"],
                question["expected_answer"],
            )
            result["checks"]["numerical_answer"] = {"valid": is_valid, "message": message}
            if not is_valid:
                result["status"] = "L1_FAIL"
                result["errors"].append(message)

        if "unit" in question and "quantity" in question:
            is_valid, message = self.validate_units(question["quantity"], question["unit"])
            result["checks"]["units"] = {"valid": is_valid, "message": message}
            if not is_valid:
                result["status"] = "L1_FAIL"
                result["errors"].append(message)

        if "solution_steps" in question:
            step_results = self.verify_solution_steps(question["solution_steps"])
            all_steps_valid = all(r[0] for r in step_results)
            result["checks"]["solution_steps"] = {
                "valid": all_steps_valid,
                "details": step_results,
            }
            if not all_steps_valid:
                result["status"] = "L1_FAIL"
                result["errors"].append("Some solution steps are invalid")

        return result

    def validate_batch(self, questions: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [self.validate(q) for q in questions]


_validator_instance = None


def get_validator() -> MathValidator:
    global _validator_instance
    if _validator_instance is None:
        _validator_instance = MathValidator()
    return _validator_instance


def evaluate_expression(expr: str) -> float:
    return get_validator().evaluate_expression(expr)


def check_answer(numerical_answer: float, expected: float, tolerance: float = 1e-6) -> bool:
    is_valid, _ = get_validator()._check_answer(numerical_answer, expected, tolerance)
    return is_valid


def verify_solution_steps(steps: list[dict[str, Any]]) -> list[tuple[bool, str]]:
    return get_validator().verify_solution_steps(steps)


def validate(question: dict[str, Any]) -> dict[str, Any]:
    return get_validator().validate(question)


def validate_batch(questions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return get_validator().validate_batch(questions)