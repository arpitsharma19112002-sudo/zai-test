"""Tests for progress tracking module."""

import time

from biopress.core.progress import ProgressTracker


class TestProgressTracker:
    """Test cases for ProgressTracker class."""

    def test_initialization(self):
        """Test ProgressTracker initializes correctly."""
        tracker = ProgressTracker(show_eta_threshold=2.0)
        assert tracker.show_eta_threshold == 2.0
        assert tracker.start_time is None
        assert tracker.current_step == 0

    def test_start(self):
        """Test starting the progress tracker."""
        tracker = ProgressTracker()
        tracker.start()
        assert tracker.start_time is not None
        assert tracker.step_start_time is not None
        assert tracker.current_step == 0

    def test_get_elapsed_time(self):
        """Test getting elapsed time."""
        tracker = ProgressTracker()
        tracker.start()
        time.sleep(0.1)
        elapsed = tracker.get_elapsed_time()
        assert elapsed >= 0.1

    def test_should_show_eta_below_threshold(self):
        """Test ETA check below threshold."""
        tracker = ProgressTracker(show_eta_threshold=2.0)
        tracker.start()
        time.sleep(0.1)
        assert tracker.should_show_eta() is False

    def test_should_show_eta_above_threshold(self):
        """Test ETA check above threshold."""
        tracker = ProgressTracker(show_eta_threshold=0.05)
        tracker.start()
        time.sleep(0.1)
        assert tracker.should_show_eta() is True

    def test_set_step(self):
        """Test setting current step."""
        tracker = ProgressTracker()
        tracker.start()
        tracker.set_step(2)
        assert tracker.current_step == 2
        assert tracker.step_start_time is not None

    def test_context_manager(self):
        """Test using tracker as context manager."""
        with ProgressTracker() as tracker:
            assert tracker.start_time is not None
        assert tracker.progress is None

    def test_steps_list(self):
        """Test that STEPS list is correctly defined."""
        expected_steps = [
            "Loading templates",
            "Generating questions",
            "Validating",
            "Building output",
        ]
        assert ProgressTracker.STEPS == expected_steps

    def test_create_progress_bar(self):
        """Test creating progress bar."""
        tracker = ProgressTracker()
        progress = tracker.create_progress_bar()
        assert progress is not None

    def test_get_elapsed_time_before_start(self):
        """Test elapsed time returns 0 before starting."""
        tracker = ProgressTracker()
        assert tracker.get_elapsed_time() == 0.0


class TestProgressTrackerStepStatus:
    """Test cases for step status display."""

    def test_show_step_status_all_complete(self):
        """Test step status when all steps complete."""
        tracker = ProgressTracker()
        tracker.start()
        tracker.current_step = 4
        table = tracker.show_step_status()
        assert table is not None

    def test_show_step_status_current_step(self):
        """Test step status showing current step."""
        tracker = ProgressTracker()
        tracker.start()
        tracker.current_step = 2
        table = tracker.show_step_status()
        assert table is not None

    def test_show_step_status_pending_steps(self):
        """Test step status with pending steps."""
        tracker = ProgressTracker()
        tracker.start()
        tracker.current_step = 0
        table = tracker.show_step_status()
        assert table is not None
