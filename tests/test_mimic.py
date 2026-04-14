"""Tests for mimic mode generator."""


from biopress.generators.mimic import (
    DifficultyBlueprint,
    ExamPattern,
    MimicConfig,
    MimicGenerator,
    get_mimic_generator,
)


class TestMimicGenerator:
    """Tests for MimicGenerator class."""

    def test_generator_creation(self):
        """Test creating mimic generator."""
        generator = MimicGenerator()
        assert generator is not None

    def test_get_mimic_generator(self):
        """Test getting mimic generator instance."""
        gen = get_mimic_generator()
        assert isinstance(gen, MimicGenerator)

    def test_get_default_pattern_neet_physics(self):
        """Test getting NEET Physics default pattern."""
        generator = MimicGenerator()
        pattern = generator.get_default_pattern("NEET", "Physics")
        
        assert pattern.exam == "NEET"
        assert pattern.subject == "Physics"
        assert "easy" in pattern.difficulty_distribution

    def test_get_default_pattern_jee_chemistry(self):
        """Test getting JEE Chemistry default pattern."""
        generator = MimicGenerator()
        pattern = generator.get_default_pattern("JEE", "Chemistry")
        
        assert pattern.exam == "JEE"
        assert "easy" in pattern.difficulty_distribution

    def test_get_default_pattern_unknown(self):
        """Test getting pattern for unknown exam/subject."""
        generator = MimicGenerator()
        pattern = generator.get_default_pattern("UNKNOWN", "Unknown")
        
        assert pattern.exam == "UNKNOWN"
        assert pattern.subject == "Unknown"

    def test_generate_blueprint(self):
        """Test generating difficulty blueprint."""
        generator = MimicGenerator()
        questions = [
            {"question": "What is force?", "options": ["A", "B", "C", "D"], "correct_answer": "A"},
            {"question": "Define momentum", "options": ["A", "B", "C", "D"], "correct_answer": "B"},
        ]
        
        blueprint = generator.generate_blueprint(questions)
        
        assert blueprint.sample_size == 2
        assert blueprint.easy_pct >= 0

    def test_generate_blueprint_empty(self):
        """Test generating blueprint from empty questions."""
        generator = MimicGenerator()
        blueprint = generator.generate_blueprint([])
        
        assert blueprint.sample_size == 0

    def test_analyze_question_difficulty_easy(self):
        """Test analyzing easy question."""
        generator = MimicGenerator()
        difficulty = generator.analyze_question_difficulty(
            "What is gravity?",
            "A force of attraction",
            ["A", "B", "C", "D"],
        )
        
        assert difficulty == "easy"

    def test_analyze_question_difficulty_hard(self):
        """Test analyzing hard question with calculation."""
        generator = MimicGenerator()
        difficulty = generator.analyze_question_difficulty(
            "Calculate the final velocity",
            "derive the expression",
            ["A very long option text", "B", "C", "D"],
        )
        
        assert difficulty in ["hard", "very_hard"]

    def test_bootstrap_blueprint(self):
        """Test bootstrap blueprint generation."""
        generator = MimicGenerator()
        questions = [
            {"question": "What is force?", "options": ["A", "B", "C", "D"], "correct_answer": "A"},
            {"question": "Define momentum", "options": ["A", "B", "C", "D"], "correct_answer": "B"},
            {"question": "What is energy?", "options": ["A", "B", "C", "D"], "correct_answer": "C"},
        ]
        
        blueprint = generator.bootstrap_blueprint(questions, n_samples=10)
        
        assert blueprint.sample_size == 3

    def test_match_difficulty_distribution(self):
        """Test matching distribution."""
        generator = MimicGenerator()
        target = ExamPattern(
            exam="NEET",
            subject="Physics",
            total_questions=10,
            difficulty_distribution={"easy": 0.3, "medium": 0.4, "hard": 0.2, "very_hard": 0.1},
            topic_weights={},
        )
        blueprint = DifficultyBlueprint(
            easy_pct=0.3,
            medium_pct=0.4,
            hard_pct=0.2,
            very_hard_pct=0.1,
            sample_size=10,
        )
        
        is_match, quality = generator.match_difficulty_distribution(blueprint, target)
        
        assert is_match is True
        assert quality > 90

    def test_generate_standard_mode(self):
        """Test generate in standard mode."""
        generator = MimicGenerator()
        questions = generator.generate("NEET", "Physics", 5)
        
        assert len(questions) <= 5

    def test_generate_with_seed(self):
        """Test generate with seed."""
        generator1 = MimicGenerator()
        generator2 = MimicGenerator()
        
        q1 = generator1.generate("NEET", "Physics", 5, seed=42)
        q2 = generator2.generate("NEET", "Physics", 5, seed=42)
        
        assert len(q1) == len(q2)

    def test_to_json(self):
        """Test JSON export."""
        generator = MimicGenerator()
        questions = [
            {"question": "What is force?", "correct_answer": "A"},
        ]
        
        json_str = generator.to_json(questions)
        
        assert '"question": "What is force?"' in json_str


class TestExamPattern:
    """Tests for ExamPattern model."""

    def test_exam_pattern_creation(self):
        """Test creating exam pattern."""
        pattern = ExamPattern(
            exam="NEET",
            subject="Physics",
            total_questions=45,
            difficulty_distribution={"easy": 0.35, "medium": 0.40, "hard": 0.20, "very_hard": 0.05},
            topic_weights={"mechanics": 0.30},
        )
        
        assert pattern.exam == "NEET"
        assert pattern.total_questions == 45


class TestDifficultyBlueprint:
    """Tests for DifficultyBlueprint model."""

    def test_blueprint_creation(self):
        """Test creating difficulty blueprint."""
        blueprint = DifficultyBlueprint(
            easy_pct=0.3,
            medium_pct=0.4,
            hard_pct=0.2,
            very_hard_pct=0.1,
            sample_size=10,
        )
        
        assert blueprint.easy_pct == 0.3
        assert blueprint.sample_size == 10


class TestMimicConfig:
    """Tests for MimicConfig model."""

    def test_config_creation(self):
        """Test creating mimic config."""
        config = MimicConfig(
            exam="NEET",
            subject="Physics",
            count=10,
            bootstrap_samples=1000,
        )
        
        assert config.exam == "NEET"
        assert config.count == 10
        assert config.bootstrap_samples == 1000