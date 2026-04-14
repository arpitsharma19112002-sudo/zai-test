"""Tests for persistent memory module."""

import tempfile
from pathlib import Path


from biopress.core.memory import Memory, get_memory, reset_memory


class TestMemory:
    """Test cases for Memory class."""

    def test_memory_disabled_by_default(self):
        """Memory should be disabled by default."""
        memory = Memory()
        assert memory.enabled is False
        assert memory._conn is None

    def test_memory_enabled_via_init(self):
        """Memory can be enabled via constructor."""
        with tempfile.TemporaryDirectory() as tmpdir:
            memory = Memory(enabled=True, limit=100)
            db_path = Path(tmpdir) / "test.db"
            memory.initialize(db_path)
            assert memory.enabled is True
            assert memory._conn is not None
            memory.close()

    def test_track_question_pattern_disabled(self):
        """Track should not record when memory is disabled."""
        memory = Memory(enabled=False)
        memory.track_question_pattern("physics", "mcq", 0.8)
        assert memory._conn is None

    def test_track_question_pattern_enabled(self):
        """Track should record when memory is enabled."""
        with tempfile.TemporaryDirectory() as tmpdir:
            memory = Memory(enabled=True, limit=100)
            db_path = Path(tmpdir) / "test.db"
            memory.initialize(db_path)

            memory.track_question_pattern("physics", "mcq", 0.8)
            stats = memory.get_question_stats("physics")
            assert "mcq" in stats
            assert stats["mcq"]["count"] == 1

            memory.close()

    def test_track_correction_enabled(self):
        """Track should record corrections when enabled."""
        with tempfile.TemporaryDirectory() as tmpdir:
            memory = Memory(enabled=True, limit=100)
            db_path = Path(tmpdir) / "test.db"
            memory.initialize(db_path)

            memory.track_correction("old text", "new text", "editor_save")
            stats = memory.get_correction_stats()
            assert "editor_save" in stats
            assert stats["editor_save"] == 1

            memory.close()

    def test_get_question_stats_empty(self):
        """Get stats returns empty dict when disabled."""
        memory = Memory(enabled=False)
        assert memory.get_question_stats("physics") == {}

    def test_clear_memory(self):
        """Clear should remove all patterns."""
        with tempfile.TemporaryDirectory() as tmpdir:
            memory = Memory(enabled=True, limit=100)
            db_path = Path(tmpdir) / "test.db"
            memory.initialize(db_path)

            memory.track_question_pattern("physics", "mcq", 0.8)
            stats = memory.get_question_stats("physics")
            assert "mcq" in stats

            memory.clear()
            stats = memory.get_question_stats("physics")
            assert stats == {}

            memory.close()

    def test_memory_limit_pruning(self):
        """Memory should prune old records over limit."""
        with tempfile.TemporaryDirectory() as tmpdir:
            memory = Memory(enabled=True, limit=3)
            db_path = Path(tmpdir) / "test.db"
            memory.initialize(db_path)

            for i in range(5):
                memory.track_question_pattern(f"topic{i}", "mcq", 0.5)

            stats = memory.get_question_stats("topic")
            assert len(stats) <= 3

            memory.close()


class TestMemoryIntegration:
    """Integration tests for memory with config."""

    def test_get_memory_uses_config_disabled(self):
        """Get memory should respect config when disabled."""
        reset_memory()
        memory = get_memory()
        assert memory.enabled is False

    def test_memory_singleton(self):
        """Get memory should return singleton."""
        reset_memory()
        mem1 = get_memory()
        mem2 = get_memory()
        assert mem1 is mem2
        mem1.close()
        reset_memory()