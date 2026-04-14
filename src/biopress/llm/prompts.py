"""Structured prompt templates for LLM-powered question generation.

Each prompt is a callable that returns a fully formed system+user prompt pair
ready for injection into any LLM adapter's generate() method.
"""

from typing import Dict, Tuple

# Type alias: (system_prompt, user_prompt)
PromptPair = Tuple[str, str]


def mcq_prompt(
    exam: str,
    subject: str,
    topic: str,
    count: int,
    difficulty: str = "medium",
) -> PromptPair:
    """Generate a structured MCQ generation prompt.

    Returns:
        Tuple of (system_prompt, user_prompt).
    """
    system = (
        f"You are a senior {exam} exam paper setter specializing in {subject}. "
        f"You create questions that match the exact difficulty and style of "
        f"official {exam} papers. You always respond in valid JSON."
    )

    user = (
        f"Generate exactly {count} multiple-choice questions on the topic "
        f"'{topic}' for the {exam} exam ({subject}).\n\n"
        f"Difficulty level: {difficulty}\n\n"
        f"Respond ONLY with a JSON array. Each element must have exactly "
        f"these keys:\n"
        f'{{"question": "...", "options": {{"A": "...", "B": "...", '
        f'"C": "...", "D": "..."}}, "correct_answer": "A|B|C|D", '
        f'"explanation": "2-3 sentence explanation"}}\n\n'
        f"Rules:\n"
        f"- All options must be plausible distractors\n"
        f"- Explanations must reference the underlying concept\n"
        f"- Questions must align with the {exam} syllabus for {subject}\n"
        f"- Use LaTeX for mathematical expressions: $...$\n"
        f"- Do NOT include question numbers in the question text"
    )

    return system, user


def numerical_prompt(
    exam: str,
    subject: str,
    topic: str,
    count: int,
) -> PromptPair:
    """Generate a structured prompt for numerical-type questions."""
    system = (
        f"You are a senior {exam} numerical problem designer for {subject}. "
        f"You create step-by-step solvable numerical problems that match "
        f"official {exam} standards. You always respond in valid JSON."
    )

    user = (
        f"Generate exactly {count} numerical problems on '{topic}' "
        f"for the {exam} exam ({subject}).\n\n"
        f"Respond ONLY with a JSON array. Each element must have:\n"
        f'{{"question": "...", "answer": <number>, '
        f'"solution_steps": ["step 1", "step 2", ...], '
        f'"units": "SI unit"}}\n\n'
        f"Rules:\n"
        f"- Each problem must be solvable in 3-5 steps\n"
        f"- Use realistic physical quantities\n"
        f"- Include proper SI units\n"
        f"- Use LaTeX for formulas: $F = ma$"
    )

    return system, user


def assertion_reason_prompt(
    exam: str,
    subject: str,
    topic: str,
    count: int,
) -> PromptPair:
    """Generate assertion-reason question prompt (NEET-specific format)."""
    system = (
        f"You are a {exam} question designer creating Assertion-Reason "
        f"questions for {subject}. These follow the standard NEET format "
        f"with 4 options. You always respond in valid JSON."
    )

    user = (
        f"Generate exactly {count} Assertion-Reason questions on '{topic}' "
        f"for the {exam} exam ({subject}).\n\n"
        f"Respond ONLY with a JSON array. Each element must have:\n"
        f'{{"assertion": "...", "reason": "...", '
        f'"correct_option": "A|B|C|D", '
        f'"explanation": "..."}}\n\n'
        f"Option meanings:\n"
        f"  A = Both Assertion and Reason are true; Reason is the correct "
        f"explanation of Assertion\n"
        f"  B = Both Assertion and Reason are true; Reason is NOT the "
        f"correct explanation of Assertion\n"
        f"  C = Assertion is true but Reason is false\n"
        f"  D = Assertion is false but Reason is true\n\n"
        f"Rules:\n"
        f"- Each assertion must be a clear, testable statement\n"
        f"- Reasons must be scientifically sound\n"
        f"- Distribute correct options across A-D"
    )

    return system, user


def parse_llm_json(raw: str) -> list[dict]:
    """Safely extract a JSON array from LLM output.

    Handles common LLM quirks: markdown fences, leading text, etc.
    """
    import json
    import re

    # Strip markdown code fences
    cleaned = re.sub(r"```(?:json)?\s*", "", raw)
    cleaned = cleaned.strip()

    # Find the outermost JSON array
    start = cleaned.find("[")
    end = cleaned.rfind("]")
    if start == -1 or end == -1:
        raise ValueError("LLM response does not contain a JSON array")

    return json.loads(cleaned[start : end + 1])


# Registry for easy lookup by question type
PROMPT_REGISTRY: Dict[str, callable] = {
    "mcq": mcq_prompt,
    "numerical": numerical_prompt,
    "assertion-reason": assertion_reason_prompt,
}
