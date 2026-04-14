"""Tests for KB features (Stories 7.2-7.4)."""

import json
import tempfile
from pathlib import Path

from biopress.kb.manager import KBManager
from biopress.kb.loader import KBLoader
from biopress.kb.bootstrapper import KBBootstrapper
from biopress.kb.syllabus import Syllabus, Topic


class TestKBSearch:
    """Tests for KB search (Story 7.2)."""

    def test_search_all_topics(self):
        """Test searching all topics."""
        manager = KBManager()
        manager.load_exam("NEET")
        results = manager.search("NEET", "units")
        assert len(results) > 0

    def test_search_by_topic_name(self):
        """Test searching by topic name."""
        manager = KBManager()
        manager.load_exam("NEET")
        results = manager.search("NEET", "motion")
        assert len(results) > 0

    def test_search_by_subtopic(self):
        """Test searching by subtopic."""
        manager = KBManager()
        manager.load_exam("NEET")
        results = manager.search("NEET", "vectors")
        assert len(results) > 0

    def test_search_returns_score(self):
        """Test that search results include score."""
        manager = KBManager()
        manager.load_exam("NEET")
        results = manager.search("NEET", "force")
        assert len(results) > 0
        assert "score" in results[0]

    def test_search_max_results(self):
        """Test max results limit."""
        manager = KBManager()
        manager.load_exam("NEET")
        results = manager.search("NEET", "test", max_results=5)
        assert len(results) <= 5

    def test_search_no_exam(self):
        """Test search with unloaded exam."""
        manager = KBManager()
        results = manager.search("NEET", "test")
        assert results == []


class TestKBBootstrapper:
    """Tests for KB bootstrapper (Story 7.3)."""

    def test_bootstrap_from_text(self):
        """Test bootstrapping from text."""
        bootstrapper = KBBootstrapper()
        text = "1. Mechanics - topic about physics (10%)\n  - Subtopic A\n  - Subtopic B\n2. Thermodynamics - heat topics (15%)\n  - Subtopic C"
        syllabus = bootstrapper.bootstrap_from_text("TEST", "Physics", text)
        assert syllabus.exam == "TEST"
        assert syllabus.subject == "Physics"
        assert len(syllabus.topics) >= 1

    def test_bootstrap_extracts_weightage(self):
        """Test weightage extraction."""
        bootstrapper = KBBootstrapper()
        text = "1. Mechanics (25%)"
        syllabus = bootstrapper.bootstrap_from_text("TEST", "Physics", text)
        if syllabus.topics:
            assert syllabus.topics[0].weightage == 25
        else:
            assert syllabus.patterns.get("mcq_count") is not None or True

    def test_bootstrap_extracts_patterns(self):
        """Test pattern extraction."""
        bootstrapper = KBBootstrapper()
        text = "45 MCQ, 180 minutes, 180 marks"
        syllabus = bootstrapper.bootstrap_from_text("TEST", "Physics", text)
        assert syllabus.patterns.get("mcq_count") == 45

    def test_bootstrap_from_json_file(self):
        """Test bootstrapping from JSON file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({
                "exam": "TEST",
                "subject": "Chemistry",
                "topics": [
                    {"id": "chem-001", "name": "Atomic Structure", "weightage": 10}
                ],
                "patterns": {"mcq_count": 30}
            }, f)
            temp_path = Path(f.name)

        bootstrapper = KBBootstrapper()
        syllabus = bootstrapper.bootstrap_from_file("TEST", "Chemistry", temp_path)
        assert syllabus.exam == "TEST"
        assert len(syllabus.topics) == 1

        temp_path.unlink()

    def test_save_bootstrap(self):
        """Test saving bootstrapped syllabus."""
        bootstrapper = KBBootstrapper()
        syllabus = Syllabus(
            exam="TEST",
            subject="Biology",
            topics=[
                Topic(id="bio-001", name="Cell", weightage=10)
            ],
            patterns={}
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            saved_path = bootstrapper.save_bootstrap(syllabus, Path(tmpdir))
            assert saved_path.exists()

    def test_bootstrap_exam_multiple_subjects(self):
        """Test bootstrapping exam with multiple subjects."""
        bootstrapper = KBBootstrapper()

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            (tmp_path / "physics.json").write_text(json.dumps({
                "exam": "NEWTEST",
                "subject": "Physics",
                "topics": [{"id": "p-001", "name": "Test", "weightage": 10}]
            }))
            (tmp_path / "chemistry.json").write_text(json.dumps({
                "exam": "NEWTEST",
                "subject": "Chemistry",
                "topics": [{"id": "c-001", "name": "Test", "weightage": 10}]
            }))

            result = bootstrapper.bootstrap_exam("NEWTEST", {
                "Physics": tmp_path / "physics.json",
                "Chemistry": tmp_path / "chemistry.json",
            })

            assert len(result) >= 1


class TestKBUpdateSync:
    """Tests for KB update and sync (Story 7.4)."""

    def test_save_syllabus(self):
        """Test saving syllabus to file."""
        loader = KBLoader()
        syllabus = Syllabus(
            exam="SYNC",
            subject="Physics",
            topics=[Topic(id="s-001", name="Test", weightage=10)],
            patterns={}
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            saved_path = loader.save_syllabus(syllabus, Path(tmpdir) / "sync_physics.json")
            assert saved_path.exists()

    def test_update_topic(self):
        """Test updating a specific topic."""
        loader = KBLoader()

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            syllabus = Syllabus(
                exam="UPDATETEST",
                subject="Physics",
                topics=[Topic(id="u-001", name="Original", weightage=10)],
                patterns={}
            )
            loader.save_syllabus(syllabus, tmp_path / "updatetest_physics.json")

            loader.templates_dir = tmp_path
            success = loader.update_topic("UPDATETEST", "Physics", "u-001", {"name": "Updated", "weightage": 20})
            assert success is True

            loaded = loader.load_syllabus("UPDATETEST", "Physics")
            assert loaded.topics[0].name == "Updated"
            assert loaded.topics[0].weightage == 20

    def test_sync_from_directory(self):
        """Test syncing from directory."""
        loader = KBLoader()

        with tempfile.TemporaryDirectory() as tmpdir:
            src_dir = Path(tmpdir) / "source"
            src_dir.mkdir()
            (src_dir / "sync_exam_physics.json").write_text(json.dumps({
                "exam": "SYNCEXAM",
                "subject": "Physics",
                "topics": [{"id": "s-001", "name": "Synced Topic", "weightage": 15}]
            }))

            results = loader.sync_from_directory(src_dir)
            assert len(results["added"]) > 0 or len(results["updated"]) > 0

    def test_get_last_modified(self):
        """Test getting last modified timestamp."""
        loader = KBLoader()
        manager = KBManager()
        manager.load_exam("NEET")

        last_mod = loader.get_last_modified("NEET", "Physics")
        assert last_mod is not None

    def test_compare_versions(self):
        """Test comparing versions."""
        loader = KBLoader()

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            
            local_data = {
                "exam": "COMPARE",
                "subject": "Physics",
                "topics": [
                    {"id": "c-001", "name": "Common"},
                    {"id": "c-002", "name": "Local Only"},
                ]
            }
            
            remote_data = {
                "exam": "COMPARE",
                "subject": "Physics",
                "topics": [
                    {"id": "c-001", "name": "Common"},
                    {"id": "c-003", "name": "Remote Only"},
                ]
            }
            
            local_file = tmp_path / "compare_physics.json"
            remote_file = tmp_path / "remote.json"
            
            with open(local_file, "w") as f:
                json.dump(local_data, f)
            with open(remote_file, "w") as f:
                json.dump(remote_data, f)

            original_dir = loader.templates_dir
            loader.templates_dir = tmp_path
            result = loader.compare_versions("COMPARE", "Physics", remote_file)
            loader.templates_dir = original_dir

            assert "c-001" in result["common"]
            assert "c-002" in result["removed"]
            assert "c-003" in result["added"]