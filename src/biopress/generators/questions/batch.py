"""Batch question generator for multiple types with performance optimization."""

from __future__ import annotations
import json
import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from threading import Lock
from typing import Any, Callable, Optional, List, Dict, Union
from biopress.core.models import BatchQuiz

from biopress.generators.questions.mcq import MCQGenerator
from biopress.generators.questions.numerical import NumericalGenerator
from biopress.generators.questions.case_based import CaseBasedGenerator
from biopress.generators.questions.assertion_reason import AssertionReasonGenerator
from biopress.core.memory import get_memory

logger = logging.getLogger(__name__)


class PerformanceMonitor:
    """Track performance metrics for batch generation."""

    def __init__(self):
        self.start_time: float = 0.0
        self.first_question_time: float | None = None
        self.total_questions: int = 0
        self.questions_per_second: float = 0.0
        self.bottlenecks: list[str] = []
        self._lock = Lock()

    def start(self):
        """Start timing."""
        self.start_time = time.time()
        self.first_question_time = None
        self.total_questions = 0
        self.questions_per_second = 0.0
        self.bottlenecks = []

    def record_first_question(self):
        """Record when first question is generated."""
        if self.first_question_time is None:
            self.first_question_time = time.time() - self.start_time
            logger.info(f"Time to first question: {self.first_question_time:.2f}s")

    def finalize(self, question_count: int):
        """Calculate final metrics."""
        self.total_questions = question_count
        elapsed = time.time() - self.start_time
        if elapsed > 0:
            self.questions_per_second = question_count / elapsed

        if self.first_question_time and self.first_question_time > 30:
            self.bottlenecks.append(f"First question delay: {self.first_question_time:.2f}s > 30s threshold")
        if self.questions_per_second < 100 / 60:
            self.bottlenecks.append(f"Rate: {self.questions_per_second:.1f} q/s < 100 q/min target")

        logger.info(f"Final rate: {self.questions_per_second:.1f} questions/second")
        for bottleneck in self.bottlenecks:
            logger.warning(f"Bottleneck detected: {bottleneck}")

    def get_metrics(self) -> dict[str, Any]:
        """Get current metrics."""
        elapsed = time.time() - self.start_time
        current_rate = self.total_questions / elapsed if elapsed > 0 else 0
        return {
            "time_to_first": self.first_question_time,
            "total_questions": self.total_questions,
            "questions_per_second": current_rate,
            "bottlenecks": self.bottlenecks,
        }


class TemplateCache:
    """Cache for loaded templates to avoid repeated file I/O."""

    def __init__(self, max_size: int = 128):
        self._cache: dict[str, Any] = {}
        self._lock = Lock()
        self._max_size = max_size

    def get(self, key: str, loader: Callable[[], Any]) -> Any:
        """Get template from cache or load it."""
        with self._lock:
            if key in self._cache:
                return self._cache[key]

        value = loader()
        with self._lock:
            if len(self._cache) >= self._max_size:
                oldest_key = next(iter(self._cache))
                del self._cache[oldest_key]
            self._cache[key] = value
            return value

    def clear(self):
        """Clear the cache."""
        with self._lock:
            self._cache.clear()


class ParallelBatchGenerator:
    """Optimized batch generator with parallel processing."""

    DEFAULT_WORKERS = 4
    MAX_WORKERS = 8

    def __init__(self, templates_dir: str | None = None, max_workers: int | None = None):
        if templates_dir:
            self.templates_dir = Path(templates_dir)
        else:
            self.templates_dir = Path(__file__).parent.parent / "templates"

        self.max_workers = max_workers or self.DEFAULT_WORKERS
        self.template_cache = TemplateCache()
        self.monitor = PerformanceMonitor()

        self.generators = {
            "mcq": MCQGenerator(templates_dir),
            "numerical": NumericalGenerator(templates_dir),
            "case-based": CaseBasedGenerator(templates_dir),
            "assertion-reason": AssertionReasonGenerator(templates_dir),
        }

    def _generate_single_type(
        self,
        qtype: str,
        exam: str,
        subject: str,
        count: int,
        topic: str,
    ) -> tuple[str, list, int]:
        """Generate questions of a single type."""
        start = time.time()
        generator = self.generators.get(qtype)
        if not generator:
            return qtype, [], 0

        quiz = generator.generate(
            exam=exam,
            subject=subject,
            count=count,
            topic=topic,
        )

        items = quiz.items if hasattr(quiz, "items") else []
        elapsed = time.time() - start

        logger.debug(f"Generated {len(items)} {qtype} questions in {elapsed:.2f}s")

        return qtype, items, len(items)

    def generate(
        self,
        exam: str,
        subject: str,
        count: int,
        topic: str,
        types: list[str] | None = None,
    ) -> BatchQuiz:
        """Generate questions of multiple types with parallel processing."""
        if types is None:
            types = ["mcq", "numerical", "case-based", "assertion-reason"]

        self.monitor.start()
        start_time = time.time()

        all_questions = []
        type_counts = {}

        total_per_type = count // len(types)
        remainder = count % len(types)

        type_assignments = []
        for i, qtype in enumerate(types):
            type_count = total_per_type + (1 if i < remainder else 0)
            if type_count > 0 and qtype in self.generators:
                type_assignments.append((qtype, type_count))

        first_generated = False
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(
                    self._generate_single_type,
                    qtype,
                    exam,
                    subject,
                    type_count,
                    topic,
                ): qtype
                for qtype, type_count in type_assignments
            }

            for future in as_completed(futures):
                qtype, items, num_generated = future.result()
                all_questions.extend(items)
                type_counts[qtype] = num_generated

                if not first_generated and num_generated > 0:
                    first_generated = True
                    self.monitor.record_first_question()

        elapsed_time = time.time() - start_time

        self.monitor.finalize(len(all_questions))
        metrics = self.monitor.get_metrics()

        memory = get_memory()
        if memory.enabled:
            for qtype, count in type_counts.items():
                memory.track_question_pattern(topic, qtype, 0.5)

        return BatchQuiz(
            items=all_questions,
            type_counts=type_counts,
            generation_time=elapsed_time,
            metrics=metrics,
        )

    def generate_streaming(
        self,
        exam: str,
        subject: str,
        count: int,
        topic: str,
        types: list[str] | None = None,
        batch_size: int = 50,
    ) -> list[BatchQuiz]:
        """Generate questions in batches for streaming output (e.g., first question appears fast)."""
        if types is None:
            types = ["mcq", "numerical", "case-based", "assertion-reason"]

        batches = []
        remaining = count
        current_batch = 0

        while remaining > 0:
            batch_count = min(batch_size, remaining)
            quiz = self.generate(
                exam=exam,
                subject=subject,
                count=batch_count,
                topic=topic,
                types=types,
            )
            batches.append(quiz)
            remaining -= batch_count
            current_batch += 1

        return batches


class BatchGenerator:
    """Generate multiple question types in batch (legacy interface)."""

    def __init__(self, templates_dir: str | None = None):
        if templates_dir:
            self.templates_dir = Path(templates_dir)
        else:
            self.templates_dir = Path(__file__).parent.parent / "templates"

        self.generators = {
            "mcq": MCQGenerator(templates_dir),
            "numerical": NumericalGenerator(templates_dir),
            "case-based": CaseBasedGenerator(templates_dir),
            "assertion-reason": AssertionReasonGenerator(templates_dir),
        }
        self._parallel = ParallelBatchGenerator(templates_dir)

    def generate(
        self,
        exam: str,
        subject: str,
        count: int,
        topic: str,
        types: list[str] | None = None,
    ) -> BatchQuiz:
        """Generate questions of multiple types."""
        if types is None:
            types = ["mcq", "numerical", "case-based", "assertion-reason"]

        if count > 100:
            return self._parallel.generate(
                exam=exam,
                subject=subject,
                count=count,
                topic=topic,
                types=types,
            )

        start_time = time.time()

        all_questions = []
        type_counts = {}

        total_per_type = count // len(types)
        remainder = count % len(types)

        for i, qtype in enumerate(types):
            type_count = total_per_type + (1 if i < remainder else 0)

            if qtype in self.generators:
                generator = self.generators[qtype]
                quiz = generator.generate(
                    exam=exam,
                    subject=subject,
                    count=type_count,
                    topic=topic,
                )
                all_questions.extend(quiz.items)
                type_counts[qtype] = type_count

        elapsed_time = time.time() - start_time

        return BatchQuiz(
            items=all_questions,
            type_counts=type_counts,
            generation_time=elapsed_time,
        )

    def to_json(self, quiz: BatchQuiz) -> str:
        """Convert quiz to JSON string."""
        return json.dumps(quiz.model_dump(), indent=2)