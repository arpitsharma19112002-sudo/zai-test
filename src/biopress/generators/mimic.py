"""Mimic Mode: Statistical exam-pattern replication for BioPress."""

from __future__ import annotations

import json
import random
from dataclasses import dataclass
from typing import Optional

from biopress.generators.questions.mcq import MCQGenerator


@dataclass
class DifficultyBlueprint:
    """Question difficulty blueprint from bootstrap analysis."""
    easy_pct: float = 0.0
    medium_pct: float = 0.0
    hard_pct: float = 0.0
    very_hard_pct: float = 0.0
    sample_size: int = 0


@dataclass
class ExamPattern:
    """Statistical pattern of exam questions."""
    exam: str
    subject: str
    total_questions: int
    difficulty_distribution: dict[str, float]
    topic_weights: dict[str, float]
    year: Optional[int] = None


@dataclass
class MimicConfig:
    """Configuration for mimic mode generation."""
    exam: str = "NEET"
    subject: str = "Physics"
    count: int = 10
    target_blueprint: Optional[ExamPattern] = None
    bootstrap_samples: int = 1000
    seed: Optional[int] = None


class MimicGenerator:
    """Generate questions that replicate exam patterns using statistical analysis."""

    DEFAULT_PATTERNS = {
        ("NEET", "Physics"): ExamPattern(
            exam="NEET",
            subject="Physics",
            total_questions=45,
            difficulty_distribution={"easy": 0.35, "medium": 0.40, "hard": 0.20, "very_hard": 0.05},
            topic_weights={"mechanics": 0.30, "electromagnetism": 0.25, "optics": 0.15, "modern_physics": 0.20, "thermodynamics": 0.10},
            year=2024,
        ),
        ("NEET", "Chemistry"): ExamPattern(
            exam="NEET",
            subject="Chemistry",
            total_questions=45,
            difficulty_distribution={"easy": 0.40, "medium": 0.35, "hard": 0.20, "very_hard": 0.05},
            topic_weights={"organic": 0.30, "inorganic": 0.25, "physical": 0.30, "biomolecules": 0.15},
            year=2024,
        ),
        ("NEET", "Biology"): ExamPattern(
            exam="NEET",
            subject="Biology",
            total_questions=90,
            difficulty_distribution={"easy": 0.45, "medium": 0.35, "hard": 0.15, "very_hard": 0.05},
            topic_weights={"BOTANY": 0.45, "ZOOLOGY": 0.45, "human_health": 0.10},
            year=2024,
        ),
        ("JEE", "Physics"): ExamPattern(
            exam="JEE",
            subject="Physics",
            total_questions=25,
            difficulty_distribution={"easy": 0.20, "medium": 0.40, "hard": 0.30, "very_hard": 0.10},
            topic_weights={"mechanics": 0.35, "electromagnetism": 0.30, "optics": 0.15, "modern_physics": 0.20},
            year=2024,
        ),
        ("JEE", "Chemistry"): ExamPattern(
            exam="JEE",
            subject="Chemistry",
            total_questions=25,
            difficulty_distribution={"easy": 0.15, "medium": 0.40, "hard": 0.35, "very_hard": 0.10},
            topic_weights={"organic": 0.25, "inorganic": 0.25, "physical": 0.50},
            year=2024,
        ),
    }

    TOPIC_KEYWORDS = {
        "mechanics": ["motion", "force", "Newton", "energy", "momentum", "velocity", "acceleration"],
        "electromagnetism": ["electric", "magnetic", "field", "charge", "current", "voltage", "capacitor"],
        "optics": ["light", "ray", "lens", "mirror", "reflection", "refraction", "wave"],
        "modern_physics": ["photon", "electron", "nucleus", "atom", "quantum", "relativity"],
        "thermodynamics": ["heat", "temperature", "entropy", "energy", "gas", "pressure"],
        "organic": ["carbon", "hydrocarbon", "reaction", "compound", "bond"],
        "inorganic": ["element", "periodic", "metal", "nonmetal", "compound"],
        "physical": ["equilibrium", "rate", "concentration", "reaction", "mol"],
        "human_health": ["disease", "infection", "immune", "cell", "organ", "system"],
    }

    def __init__(self):
        self.config: Optional[MimicConfig] = None
        self._rng = random.Random()
        self._blueprint_history: list[DifficultyBlueprint] = []

    def analyze_question_difficulty(
        self,
        question_text: str,
        answer: str,
        options: list[str],
    ) -> str:
        """Analyze difficulty of a question based on content complexity."""
        text = question_text.lower() + " " + " ".join(options).lower()
        word_count = len(text.split())
        has_calculation = any(
            keyword in text
            for keyword in ["calculate", "find", "determine", "express", "value"]
        )
        has_derivation = any(
            keyword in text
            for keyword in ["derive", "prove", "show that", "verify"]
        )
        is_long = word_count > 50
        has_multiple_concepts = sum(1 for kw in ["and", "also", "furthermore"] if kw in text)

        if has_derivation or (has_calculation and is_long):
            return "very_hard"
        elif has_calculation or has_multiple_concepts >= 2:
            return "hard"
        elif word_count > 25 or is_long:
            return "medium"
        else:
            return "easy"

    def generate_blueprint(
        self,
        questions: list[dict],
    ) -> DifficultyBlueprint:
        """Generate difficulty blueprint from bootstrapped sample."""
        if not questions:
            return DifficultyBlueprint()

        difficulties = [
            self.analyze_question_difficulty(
                q.get("question", ""),
                q.get("correct_answer", ""),
                q.get("options", []),
            )
            for q in questions
        ]

        total = len(difficulties)
        easy = sum(1 for d in difficulties if d == "easy") / total
        medium = sum(1 for d in difficulties if d == "medium") / total
        hard = sum(1 for d in difficulties if d == "hard") / total
        very_hard = sum(1 for d in difficulties if d == "very_hard") / total

        blueprint = DifficultyBlueprint(
            easy_pct=easy,
            medium_pct=medium,
            hard_pct=hard,
            very_hard_pct=very_hard,
            sample_size=total,
        )

        self._blueprint_history.append(blueprint)
        return blueprint

    def bootstrap_blueprint(
        self,
        existing_questions: list[dict],
        n_samples: int = 1000,
    ) -> DifficultyBlueprint:
        """Generate statistical blueprint using bootstrap sampling."""
        if not existing_questions:
            return DifficultyBlueprint()

        self._rng.seed(self.config.seed if self.config and self.config.seed else None)

        sample_difficulties = []
        for _ in range(n_samples):
            sample = self._rng.choices(
                existing_questions,
                k=len(existing_questions),
            )
            blueprint = self.generate_blueprint(sample)
            sample_difficulties.append(blueprint)

        avg_easy = sum(b.easy_pct for b in sample_difficulties) / n_samples
        avg_medium = sum(b.medium_pct for b in sample_difficulties) / n_samples
        avg_hard = sum(b.hard_pct for b in sample_difficulties) / n_samples
        avg_very_hard = sum(b.very_hard_pct for b in sample_difficulties) / n_samples

        return DifficultyBlueprint(
            easy_pct=avg_easy,
            medium_pct=avg_medium,
            hard_pct=avg_hard,
            very_hard_pct=avg_very_hard,
            sample_size=len(existing_questions),
        )

    def get_default_pattern(self, exam: str, subject: str) -> ExamPattern:
        """Get default exam pattern."""
        return self.DEFAULT_PATTERNS.get(
            (exam, subject),
            ExamPattern(
                exam=exam,
                subject=subject,
                total_questions=10,
                difficulty_distribution={"easy": 0.30, "medium": 0.40, "hard": 0.20, "very_hard": 0.10},
                topic_weights={"default": 1.0},
            ),
        )

    def match_difficulty_distribution(
        self,
        blueprint: DifficultyBlueprint,
        target: ExamPattern,
    ) -> tuple[bool, float]:
        """Match generated blueprint to target distribution."""
        target_dist = target.difficulty_distribution
        diff = abs(blueprint.easy_pct - target_dist.get("easy", 0))
        diff += abs(blueprint.medium_pct - target_dist.get("medium", 0))
        diff += abs(blueprint.hard_pct - target_dist.get("hard", 0))
        diff += abs(blueprint.very_hard_pct - target_dist.get("very_hard", 0))

        match_quality = max(0, 100 - diff * 100)
        is_good_match = diff < 0.15

        return is_good_match, match_quality

    def generate(
        self,
        exam: str,
        subject: str,
        count: int,
        target_pattern: Optional[ExamPattern] = None,
        seed: Optional[int] = None,
    ) -> list[dict]:
        """Generate questions using mimic mode."""
        self.config = MimicConfig(
            exam=exam,
            subject=subject,
            count=count,
            target_blueprint=target_pattern,
            seed=seed,
        )

        pattern = target_pattern or self.get_default_pattern(exam, subject)

        target_dist = pattern.difficulty_distribution
        distribution = {
            "easy": int(count * target_dist.get("easy", 0.3)),
            "medium": int(count * target_dist.get("medium", 0.4)),
            "hard": int(count * target_dist.get("hard", 0.2)),
            "very_hard": int(count * target_dist.get("very_hard", 0.1)),
        }

        remaining = count - sum(distribution.values())
        if remaining > 0:
            distribution["medium"] += remaining
        elif remaining < 0:
            for key in list(distribution.keys()):
                if distribution[key] > 0 and remaining < 0:
                    reduction = min(distribution[key], -remaining)
                    distribution[key] -= reduction
                    remaining += reduction

        generator = MCQGenerator()
        generated_questions = []

        difficulty_topics = {
            "easy": ["basic", "definition", "concept"],
            "medium": ["application", "problem", "situation"],
            "hard": ["analysis", "comparison", "multiple"],
            "very_hard": ["critical", "synthesis", "evaluation"],
        }

        for difficulty, num in distribution.items():
            if num <= 0:
                continue
            topics = difficulty_topics.get(difficulty, ["basic"])
            for i in range(num):
                topic = topics[i % len(topics)]
                keywords = self.TOPIC_KEYWORDS.get(topic, [topic])
                actual_topic = f"{topic} {keywords[0]}" if keywords else topic

                quiz = generator.generate(
                    exam=exam,
                    subject=subject,
                    count=1,
                    topic=actual_topic,
                )
                if quiz and quiz.items:
                    question = quiz.items[0]
                    q_dict = {
                        "question": question.question,
                        "options": list(question.options.model_dump().values()) if hasattr(question.options, 'model_dump') else [],
                        "correct_answer": question.correct_answer,
                        "explanation": question.explanation,
                    }
                else:
                    q_dict = {
                        "question": f"Sample {difficulty} question for {topic}",
                        "options": ["A", "B", "C", "D"],
                        "correct_answer": "A",
                        "explanation": f"Explanation for {topic}",
                    }
                q_dict["difficulty"] = difficulty
                generated_questions.append(q_dict)

        return generated_questions

    def to_json(self, questions: list[dict]) -> str:
        """Export questions as JSON."""
        return json.dumps(questions, indent=2)


def get_mimic_generator() -> MimicGenerator:
    """Get mimic generator instance."""
    return MimicGenerator()