"""Validation API route."""

from fastapi import APIRouter, HTTPException

from biopress.api.models.schemas import (
    ValidateRequest,
    ValidateResponse,
    ValidationIssue,
)
from biopress.validators.l1.math_validator import MathValidator
from biopress.validators.l1.unit_validator import UnitValidator

router = APIRouter()


@router.post("/validate", response_model=ValidateResponse)
async def validate_questions(request: ValidateRequest):
    """Validate questions via API.

    L1 validation checks mathematical correctness and unit consistency.
    L2 validation requires an LLM adapter and performs semantic checks.
    """
    if request.level not in ["l1", "l2"]:
        raise HTTPException(status_code=400, detail="Invalid level. Valid: l1, l2")

    try:
        issues = []

        if request.level == "l1":
            math_validator = MathValidator()
            unit_validator = UnitValidator()

            for question in request.questions:
                # Build a dict compatible with MathValidator.validate()
                q_data = {
                    "question": question.question,
                }

                # If options are present, check for numerical content
                if question.correct_answer:
                    try:
                        expected = float(question.correct_answer)
                        q_data["expected_answer"] = expected
                        q_data["expression"] = question.correct_answer
                    except (ValueError, TypeError):
                        pass  # Non-numeric answer, skip math validation

                result = math_validator.validate(q_data)
                if result["status"] == "L1_FAIL":
                    for error in result["errors"]:
                        issues.append(
                            ValidationIssue(
                                question_id=question.id,
                                issue_type="math",
                                severity="error",
                                message=error,
                            )
                        )

                # Unit consistency checks on question text
                if question.question:
                    unit_issues = _check_units_in_text(
                        unit_validator, question.id, question.question
                    )
                    issues.extend(unit_issues)

        elif request.level == "l2":
            # L2 validation requires LLM — return clear message
            raise HTTPException(
                status_code=400,
                detail="L2 validation requires an LLM adapter. "
                "Configure a provider first via: biopress config set provider <name>",
            )

        total = len(request.questions)
        valid_count = total - len(set(i.question_id for i in issues))

        return ValidateResponse(
            status="success" if len(issues) == 0 else "has_issues",
            issues=issues,
            total_questions=total,
            valid_count=valid_count,
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")


def _check_units_in_text(
    validator: UnitValidator, question_id: str, text: str
) -> list[ValidationIssue]:
    """Extract and check unit mentions in question text."""
    issues = []
    # Simple heuristic: look for common quantity-unit patterns
    quantity_patterns = {
        "velocity": ["m/s", "km/h"],
        "force": ["N", "kN"],
        "energy": ["J", "kJ", "eV"],
        "mass": ["kg", "g", "mg"],
        "length": ["m", "cm", "mm", "km"],
    }

    for quantity, units in quantity_patterns.items():
        for unit in units:
            if unit in text:
                if not validator.check_unit_consistency(quantity, unit):
                    issues.append(
                        ValidationIssue(
                            question_id=question_id,
                            issue_type="unit",
                            severity="warning",
                            message=f"Unit '{unit}' may be inconsistent with quantity '{quantity}'",
                        )
                    )
    return issues