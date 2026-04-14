"""Tests for BioPress Knowledge Base."""


from biopress.kb.manager import KBManager, get_kb_manager
from biopress.kb.loader import KBLoader
from biopress.kb.syllabus import Syllabus, Topic
from biopress.kb.rules import Rule, ValidationRules, RulesEngine


class TestKBLoader:
    """Tests for KB loader."""

    def test_list_available_exams(self):
        """Test listing available exams."""
        loader = KBLoader()
        exams = loader.list_available_exams()
        assert "NEET" in exams

    def test_list_subjects(self):
        """Test listing subjects for an exam."""
        loader = KBLoader()
        subjects = loader.list_subjects("NEET")
        assert "Physics" in subjects
        assert "Chemistry" in subjects
        assert "Biology" in subjects

    def test_load_syllabus(self):
        """Test loading a specific syllabus."""
        loader = KBLoader()
        syllabus = loader.load_syllabus("NEET", "Physics")
        assert syllabus.exam == "NEET"
        assert syllabus.subject == "Physics"
        assert len(syllabus.topics) > 0

    def test_load_exam(self):
        """Test loading all subjects for an exam."""
        loader = KBLoader()
        syllabi = loader.load_exam("NEET")
        assert "Physics" in syllabi
        assert "Chemistry" in syllabi
        assert "Biology" in syllabi


class TestKBManager:
    """Tests for KB manager."""

    def test_load_exam(self):
        """Test loading an exam."""
        manager = KBManager()
        success = manager.load_exam("NEET")
        assert success is True
        assert manager.is_loaded("NEET")

    def test_load_invalid_exam(self):
        """Test loading an invalid exam."""
        manager = KBManager()
        success = manager.load_exam("INVALID")
        assert success is False

    def test_get_syllabus(self):
        """Test getting a syllabus."""
        manager = KBManager()
        manager.load_exam("NEET")
        syllabus = manager.get_syllabus("NEET", "Physics")
        assert syllabus is not None
        assert syllabus.exam == "NEET"

    def test_get_subjects(self):
        """Test getting subjects."""
        manager = KBManager()
        manager.load_exam("NEET")
        subjects = manager.get_subjects("NEET")
        assert len(subjects) == 3

    def test_get_topics(self):
        """Test getting topics."""
        manager = KBManager()
        manager.load_exam("NEET")
        topics = manager.get_topics("NEET", "Physics")
        assert len(topics) > 0

    def test_get_loaded_exams(self):
        """Test getting loaded exams."""
        manager = KBManager()
        manager.load_exam("NEET")
        exams = manager.get_loaded_exams()
        assert "NEET" in exams

    def test_get_load_status(self):
        """Test getting load status."""
        manager = KBManager()
        manager.load_exam("NEET")
        status = manager.get_load_status("NEET")
        assert status is not None
        assert "loaded_at" in status
        assert "subjects" in status
        assert "total_topics" in status

    def test_get_info(self):
        """Test getting KB info."""
        manager = KBManager()
        manager.load_exam("NEET")
        info = manager.get_info("NEET")
        assert info is not None
        assert info["exam"] == "NEET"
        assert len(info["subjects"]) == 3

    def test_query_all(self):
        """Test querying all topics."""
        manager = KBManager()
        manager.load_exam("NEET")
        results = manager.query("NEET")
        assert len(results) > 0

    def test_query_by_subject(self):
        """Test querying by subject."""
        manager = KBManager()
        manager.load_exam("NEET")
        results = manager.query("NEET", subject="Physics")
        assert all("Physics" in r.get("subject", "") or r.get("subject") == "Physics" for r in results)

    def test_query_by_topic_id(self):
        """Test querying by topic ID."""
        manager = KBManager()
        manager.load_exam("NEET")
        results = manager.query("NEET", topic_id="phy-001")
        assert len(results) == 1
        assert results[0]["id"] == "phy-001"

    def test_validate(self):
        """Test validation."""
        manager = KBManager()
        manager.load_exam("NEET")
        results = manager.validate("NEET")
        assert len(results) > 0


class TestSyllabus:
    """Tests for syllabus data structures."""

    def test_topic_creation(self):
        """Test creating a topic."""
        topic = Topic(
            id="test-001",
            name="Test Topic",
            subtopics=["Subtopic 1", "Subtopic 2"],
            weightage=10,
            difficulty="medium"
        )
        assert topic.id == "test-001"
        assert topic.name == "Test Topic"
        assert len(topic.subtopics) == 2

    def test_syllabus_creation(self):
        """Test creating a syllabus."""
        syllabus = Syllabus(
            exam="NEET",
            subject="Physics",
            topics=[],
            patterns={"mcq_count": 45}
        )
        assert syllabus.exam == "NEET"
        assert syllabus.patterns["mcq_count"] == 45


class TestRules:
    """Tests for validation rules."""

    def test_validation_rules(self):
        """Test validation rules."""
        rules = ValidationRules(
            exam="NEET",
            rules=[
                Rule(
                    id="test-001",
                    name="Test Rule",
                    description="A test rule",
                    condition="has_topics",
                    severity="error"
                )
            ]
        )
        assert len(rules.rules) == 1
        assert rules.get_rule("test-001") is not None

    def test_rules_engine(self):
        """Test rules engine evaluation."""
        rules = ValidationRules(
            exam="NEET",
            rules=[
                Rule(
                    id="test-001",
                    name="Has Topics",
                    description="Must have topics",
                    condition="has_topics",
                    severity="error"
                )
            ]
        )
        engine = RulesEngine(rules)
        results = engine.evaluate({"topics": [{"id": "1", "name": "Test"}]})
        assert len(results) == 1
        assert results[0]["passed"] is True


class TestGlobalManager:
    """Tests for global KB manager."""

    def test_get_kb_manager(self):
        """Test getting global KB manager."""
        manager1 = get_kb_manager()
        manager2 = get_kb_manager()
        assert manager1 is manager2