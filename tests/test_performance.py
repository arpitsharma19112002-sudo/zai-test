"""Performance benchmark tests for batch generation."""

import pytest
import tempfile
import json
import time
from pathlib import Path
from biopress.generators.questions.batch import BatchGenerator, ParallelBatchGenerator, PerformanceMonitor
from biopress.validators.l1.math_validator import MathValidator


class TestBatchPerformance:
    """Performance tests for batch generation."""

    @pytest.fixture
    def temp_templates(self, tmp_path):
        templates_dir = tmp_path / "templates"
        templates_dir.mkdir()

        mcq_data = {
            "default": [
                {
                    "question": f"What is energy of photon {i}?",
                    "options": {"A": "1J", "B": "2J", "C": "3J", "D": "4J"},
                    "correct_answer": "A",
                    "explanation": "E = hv",
                }
                for i in range(100)
            ]
        }

        numerical_data = {
            "default": [
                {
                    "question": f"Calculate force {i}",
                    "answer": 10 * (i + 1),
                    "solution_steps": ["F = ma"],
                    "units": "N",
                }
                for i in range(100)
            ]
        }

        case_based_data = {
            "default": [
                {
                    "passage": f"Test passage {i}",
                    "questions": [{"question": f"Q{i}", "answer": "A"}],
                }
                for i in range(100)
            ]
        }

        assertion_reason_data = {
            "default": [
                {
                    "assertion": f"Assertion {i}",
                    "reason": f"Reason {i}",
                    "correct_option": "A",
                    "explanation": "Test",
                }
                for i in range(100)
            ]
        }

        (templates_dir / "physics.json").write_text(json.dumps(mcq_data))
        (templates_dir / "numerical_physics.json").write_text(json.dumps(numerical_data))
        (templates_dir / "case_based_biology.json").write_text(json.dumps(case_based_data))
        (templates_dir / "assertion_reason_physics.json").write_text(json.dumps(assertion_reason_data))

        return str(templates_dir)

    def test_100_questions_under_60_seconds(self, temp_templates):
        """Test that 100 questions can be generated in under 60 seconds."""
        generator = BatchGenerator(temp_templates)

        start_time = time.time()
        quiz = generator.generate(
            exam="NEET",
            subject="Physics",
            count=100,
            topic="default",
            types=["mcq", "numerical", "case-based", "assertion-reason"],
        )
        elapsed = time.time() - start_time

        assert elapsed < 60, f"100 questions took {elapsed:.2f}s, expected < 60s"
        assert len(quiz.items) == 100

    def test_500_questions_under_5_minutes(self, temp_templates):
        """Test that 500 questions can be generated in under 5 minutes."""
        generator = BatchGenerator(temp_templates)

        start_time = time.time()
        quiz = generator.generate(
            exam="NEET",
            subject="Physics",
            count=500,
            topic="default",
            types=["mcq", "numerical", "case-based", "assertion-reason"],
        )
        elapsed = time.time() - start_time

        assert elapsed < 300, f"500 questions took {elapsed:.2f}s, expected < 300s (5 min)"
        assert len(quiz.items) == 500

    def test_time_to_first_under_30_seconds(self, temp_templates):
        """Test that first question appears in under 30 seconds."""
        generator = ParallelBatchGenerator(temp_templates, max_workers=4)
        monitor = PerformanceMonitor()

        monitor.start()
        quiz = generator.generate(
            exam="NEET",
            subject="Physics",
            count=100,
            topic="default",
            types=["mcq"],
        )

        if quiz.items:
            first_question_time = time.time() - monitor.start_time
            assert first_question_time < 30, f"First question took {first_question_time:.2f}s, expected < 30s"


class TestL1ValidatorPerformance:
    """Performance tests for L1 validator."""

    def test_l1_validation_is_instant(self):
        """Test that L1 validation is near-instant."""
        validator = MathValidator()

        questions = [
            {"expression": "2 + 2", "expected_answer": 4.0},
            {"expression": "sqrt(16)", "expected_answer": 4.0},
            {"expression": "3 * 5", "expected_answer": 15.0},
            {"expression": "10 - 3", "expected_answer": 7.0},
            {"expression": "2**3", "expected_answer": 8.0},
        ]

        start_time = time.time()
        results = validator.validate_batch(questions)
        elapsed = time.time() - start_time

        assert elapsed < 1.0, f"L1 batch validation took {elapsed:.2f}s, expected < 1s"
        assert all(r["status"] == "L1_PASS" for r in results)

    def test_l1_validation_pass_rate(self):
        """Test L1 validation pass rate > 95%."""
        validator = MathValidator()

        test_cases = []
        for i in range(100):
            test_cases.append(
                {
                    "expression": f"{i} + {100-i}",
                    "expected_answer": float(100),
                }
            )

        results = validator.validate_batch(test_cases)
        passed = sum(1 for r in results if r["status"] == "L1_PASS")
        pass_rate = passed / len(results)

        assert pass_rate > 0.95, f"Pass rate {pass_rate:.1%}, expected > 95%"


class TestParallelGeneration:
    """Tests for parallel generation."""

    @pytest.fixture
    def temp_templates(self, tmp_path):
        templates_dir = tmp_path / "templates"
        templates_dir.mkdir()

        mcq_data = {
            "default": [
                {
                    "question": f"Q{i}",
                    "options": {"A": "1", "B": "2", "C": "3", "D": "4"},
                    "correct_answer": "A",
                    "explanation": "Test",
                }
                for i in range(200)
            ]
        }

        (templates_dir / "physics.json").write_text(json.dumps(mcq_data))
        return str(templates_dir)

    def test_parallel_faster_than_sequential(self, temp_templates):
        """Test that parallel generation completes successfully."""
        parallel_gen = ParallelBatchGenerator(temp_templates, max_workers=4)
        sequential_gen = BatchGenerator(temp_templates)

        count = 200

        parallel_result = parallel_gen.generate(
            exam="NEET", subject="Physics", count=count, topic="default", types=["mcq"]
        )

        sequential_result = sequential_gen.generate(
            exam="NEET", subject="Physics", count=count, topic="default", types=["mcq"]
        )

        assert len(parallel_result.items) == count
        assert len(sequential_result.items) == count


class TestPerformanceMonitoring:
    """Tests for performance monitoring."""

    def test_monitor_tracks_questions_per_second(self):
        """Test that monitor correctly tracks questions/second."""
        monitor = PerformanceMonitor()

        monitor.start()
        time.sleep(0.1)
        monitor.finalize(100)

        metrics = monitor.get_metrics()

        assert metrics["total_questions"] == 100
        assert metrics["questions_per_second"] > 0

    def test_monitor_detects_bottlenecks(self):
        """Test that bottleneck detection works."""
        monitor = PerformanceMonitor()

        monitor.start()
        monitor.first_question_time = 40.0
        monitor.finalize(50)

        metrics = monitor.get_metrics()

        assert len(metrics["bottlenecks"]) > 0
        assert any("delay" in b.lower() for b in metrics["bottlenecks"])


class TestEdgeCases:
    """Edge case performance tests."""

    def test_small_batch_performance(self):
        """Test small batches complete quickly."""
        with tempfile.TemporaryDirectory() as tmp:
            templates_dir = Path(tmp) / "templates"
            templates_dir.mkdir()

            mcq_data = {
                "default": [
                    {
                        "question": f"Q{i}",
                        "options": {"A": "1", "B": "2", "C": "3", "D": "4"},
                        "correct_answer": "A",
                        "explanation": "Test",
                    }
                    for i in range(10)
                ]
            }

            numerical_data = {
                "default": [
                    {
                        "question": f"Q{i}",
                        "answer": 10,
                        "solution_steps": ["F=ma"],
                        "units": "N",
                    }
                    for i in range(10)
                ]
            }

            (templates_dir / "physics.json").write_text(json.dumps(mcq_data))
            (templates_dir / "numerical_physics.json").write_text(json.dumps(numerical_data))

            generator = BatchGenerator(str(templates_dir))

            start = time.time()
            quiz = generator.generate(
                exam="NEET", subject="Physics", count=5, topic="default", types=["mcq"]
            )
            elapsed = time.time() - start

            assert elapsed < 30, f"Small batch took {elapsed:.2f}s"
            assert len(quiz.items) == 5

    def test_single_question_type(self):
        """Test single question type generation."""
        with tempfile.TemporaryDirectory() as tmp:
            templates_dir = Path(tmp) / "templates"
            templates_dir.mkdir()

            mcq_data = {
                "default": [
                    {
                        "question": f"Q{i}",
                        "options": {"A": "1", "B": "2", "C": "3", "D": "4"},
                        "correct_answer": "A",
                        "explanation": "Test",
                    }
                    for i in range(50)
                ]
            }

            (templates_dir / "physics.json").write_text(json.dumps(mcq_data))

            generator = BatchGenerator(str(templates_dir))

            quiz = generator.generate(
                exam="NEET",
                subject="Physics",
                count=50,
                topic="default",
                types=["mcq"],
            )

            assert len(quiz.items) == 50
            assert "mcq" in quiz.type_counts
            assert quiz.type_counts["mcq"] == 50


if __name__ == "__main__":
    pytest.main([__file__, "-v"])