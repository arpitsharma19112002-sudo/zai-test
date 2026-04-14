"""Knowledge base bootstrapper - generates KB entries from syllabus documents."""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional

from biopress.kb.syllabus import Syllabus, Topic


class KBBootstrapper:
    """Bootstrap knowledge base from syllabus documents."""

    def __init__(self, templates_dir: Optional[Path] = None):
        if templates_dir is None:
            templates_dir = Path(__file__).parent / "templates"
        self.templates_dir = templates_dir

    def bootstrap_from_text(self, exam: str, subject: str, text: str) -> Syllabus:
        """Generate KB entries from raw text syllabus."""
        topics = self._parse_text_syllabus(text, exam, subject)
        return Syllabus(
            exam=exam,
            subject=subject,
            topics=topics,
            patterns=self._extract_patterns(text),
        )

    def bootstrap_from_file(self, exam: str, subject: str, file_path: Path) -> Syllabus:
        """Load and bootstrap from a syllabus file."""
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        if file_path.suffix == ".json":
            return self._bootstrap_from_json(content, exam, subject)
        else:
            return self.bootstrap_from_text(exam, subject, content)

    def _bootstrap_from_json(self, content: str, exam: str, subject: str) -> Syllabus:
        """Bootstrap from JSON format."""
        try:
            data = json.loads(content)
            if isinstance(data, dict) and "topics" in data:
                topics = [Topic(**t) if isinstance(t, dict) else t for t in data["topics"]]
                return Syllabus(
                    exam=exam,
                    subject=subject,
                    topics=topics,
                    patterns=data.get("patterns", {}),
                )
        except json.JSONDecodeError:
            pass

        return self.bootstrap_from_text(exam, subject, content)

    def _parse_text_syllabus(self, text: str, exam: str, subject: str) -> List[Topic]:
        """Parse text syllabus into topics."""
        topics = []
        lines = text.split("\n")

        topic_pattern = re.compile(r"^(\d+\.?\d*)[.\-–]\s*(.+)$", re.IGNORECASE)
        weightage_pattern = re.compile(r"\((\d+)%\)|(\d+)%", re.IGNORECASE)
        subtopic_pattern = re.compile(r"^\s*[-•]\s*(.+)$")

        current_topic = None

        for line in lines:
            line = line.strip()
            if not line:
                continue

            topic_match = topic_pattern.match(line)
            if topic_match:
                if current_topic:
                    topics.append(current_topic)

                topic_title = topic_match.group(2).strip()
                weightage_match = weightage_pattern.search(topic_title)
                weightage = int(weightage_match.group(1) or weightage_match.group(2)) if weightage_match else 10

                topic_title = weightage_pattern.sub("", topic_title).strip()

                current_topic = Topic(
                    id=f"{subject.lower()}-{len(topics) + 1:03d}",
                    name=topic_title,
                    subtopics=[],
                    weightage=weightage,
                    difficulty="medium",
                )
                continue

            if current_topic:
                subtopic_match = subtopic_pattern.match(line)
                if subtopic_match:
                    current_topic.subtopics.append(subtopic_match.group(1).strip())

        if current_topic:
            topics.append(current_topic)

        return topics

    def _extract_patterns(self, text: str) -> Dict:
        """Extract question patterns from text."""
        patterns = {}

        mcq_match = re.search(r"(\d+)\s*MCQ", text, re.IGNORECASE)
        if mcq_match:
            patterns["mcq_count"] = int(mcq_match.group(1))

        duration_match = re.search(r"(\d+)\s*(?:minutes?|mins?)", text, re.IGNORECASE)
        if duration_match:
            patterns["duration_minutes"] = int(duration_match.group(1))

        marks_match = re.search(r"(\d+)\s*marks?", text, re.IGNORECASE)
        if marks_match:
            patterns["total_marks"] = int(marks_match.group(1))

        return patterns

    def bootstrap_exam(self, exam: str, syllabus_files: Dict[str, Path]) -> Dict[str, Syllabus]:
        """Bootstrap entire exam from multiple subject files."""
        syllabi = {}

        for subject, file_path in syllabus_files.items():
            try:
                syllabus = self.bootstrap_from_file(exam, subject, file_path)
                syllabi[subject] = syllabus
            except Exception as e:
                print(f"Warning: Failed to bootstrap {subject} for {exam}: {e}")

        return syllabi

    def save_bootstrap(self, syllabus: Syllabus, output_dir: Optional[Path] = None) -> Path:
        """Save bootstrapped syllabus to file."""
        if output_dir is None:
            output_dir = self.templates_dir

        output_dir.mkdir(parents=True, exist_ok=True)
        filename = f"{syllabus.exam.lower()}_{syllabus.subject.lower()}.json"
        file_path = output_dir / filename

        with open(file_path, "w") as f:
            json.dump(syllabus.model_dump(), f, indent=2)

        return file_path

    def generate_entry(self, exam: str, subject: str, topic_data: dict) -> Topic:
        """Generate a single KB entry from data."""
        return Topic(
            id=topic_data.get("id", f"{subject.lower()}-{hash(topic_data.get('name', '')) % 1000:03d}"),
            name=topic_data["name"],
            subtopics=topic_data.get("subtopics", []),
            weightage=topic_data.get("weightage", 10),
            difficulty=topic_data.get("difficulty", "medium"),
        )


def bootstrap_kb(exam: str, syllabus_file: Path, subject: str = None) -> Syllabus:
    """Convenience function to bootstrap KB from a syllabus file."""
    bootstrapper = KBBootstrapper()

    if subject is None:
        subject = syllabus_file.stem.replace(exam.lower(), "").strip("_").title()

    return bootstrapper.bootstrap_from_file(exam, subject, syllabus_file)