"""Core data types and validation schemas for BioPress."""

from dataclasses import dataclass, field


@dataclass
class ValidationResult:
    """Standardized result for any validation check (L1, L2, LLM)."""
    is_valid: bool
    score: float  # Normalized 0.0 to 1.0
    issues: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)
    provider: str = "internal"


@dataclass
class L2Result:
    """Combined L2 validation results from multiple dimensions."""
    relevance: ValidationResult
    difficulty: ValidationResult
    context: ValidationResult
    overall_pass: bool
    score: float
    flagged: bool = False
