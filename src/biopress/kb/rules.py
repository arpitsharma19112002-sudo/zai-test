"""Validation rules for knowledge base."""

from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional


class Rule(BaseModel):
    """Represents a single validation rule."""
    id: str = Field(..., description="Unique rule identifier")
    name: str = Field(..., description="Rule name")
    description: str = Field(..., description="Rule description")
    condition: str = Field(..., description="Condition to evaluate")
    severity: str = Field(default="error", description="Severity level")


class ValidationRules(BaseModel):
    """Collection of validation rules for an exam."""
    exam: str = Field(..., description="Exam name")
    rules: List[Rule] = Field(default_factory=list, description="List of rules")

    def get_rule(self, rule_id: str) -> Rule | None:
        """Get a rule by its ID."""
        for rule in self.rules:
            if rule.id == rule_id:
                return rule
        return None


class RulesEngine:
    """Engine for evaluating validation rules."""

    def __init__(self, rules: ValidationRules):
        self.rules = rules

    def evaluate(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Evaluate all rules against the given data."""
        results = []
        for rule in self.rules.rules:
            result = self._evaluate_rule(rule, data)
            results.append({
                "rule_id": rule.id,
                "rule_name": rule.name,
                "passed": result,
                "severity": rule.severity,
            })
        return results

    def _evaluate_rule(self, rule: Rule, data: Dict[str, Any]) -> bool:
        """Evaluate a single rule based on its condition."""
        if rule.condition == "has_syllabus":
            return "syllabus" in data and len(data["syllabus"]) > 0
        if rule.condition == "has_topics":
            return "topics" in data and len(data["topics"]) > 0
        if rule.condition == "has_weightage":
            return all(t.get("weightage", 0) > 0 for t in data.get("topics", []))
        return True