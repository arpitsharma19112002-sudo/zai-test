"""Knowledge base loader."""

import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

from biopress.kb.syllabus import Syllabus


class KBLoader:
    """Loads knowledge base from JSON files."""

    def __init__(self, templates_dir: Optional[Path] = None):
        if templates_dir is None:
            templates_dir = Path(__file__).parent / "templates"
        self.templates_dir = templates_dir

    def load_syllabus(self, exam: str, subject: str) -> Syllabus:
        """Load syllabus for a specific exam and subject."""
        file_path = self.templates_dir / f"{exam.lower()}_{subject.lower()}.json"
        if not file_path.exists():
            raise FileNotFoundError(f"Syllabus file not found: {file_path}")

        with open(file_path, "r") as f:
            data = json.load(f)

        return Syllabus(**data)

    def load_exam(self, exam: str) -> Dict[str, Syllabus]:
        """Load all subjects for a given exam."""
        syllabi = {}
        subject_files = {
            "Physics": f"{exam.lower()}_physics.json",
            "Chemistry": f"{exam.lower()}_chemistry.json",
            "Biology": f"{exam.lower()}_biology.json",
        }

        for subject, filename in subject_files.items():
            file_path = self.templates_dir / filename
            if file_path.exists():
                with open(file_path, "r") as f:
                    data = json.load(f)
                syllabi[subject] = Syllabus(**data)

        return syllabi

    def list_available_exams(self) -> List[str]:
        """List all available exams in the templates directory."""
        exams = set()
        for file_path in self.templates_dir.glob("*.json"):
            parts = file_path.stem.rsplit("_", 1)
            if len(parts) == 2:
                exams.add(parts[0].upper())
        return sorted(list(exams))

    def list_subjects(self, exam: str) -> List[str]:
        """List all subjects available for an exam."""
        subjects = []
        for file_path in self.templates_dir.glob(f"{exam.lower()}_*.json"):
            subject = file_path.stem.rsplit("_", 1)[1].title()
            subjects.append(subject)
        return subjects

    def save_syllabus(self, syllabus: Syllabus, file_path: Optional[Path] = None) -> Path:
        """Save syllabus to a JSON file."""
        if file_path is None:
            file_path = self.templates_dir / f"{syllabus.exam.lower()}_{syllabus.subject.lower()}.json"

        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, "w") as f:
            json.dump(syllabus.model_dump(), f, indent=2)

        return file_path

    def update_topic(self, exam: str, subject: str, topic_id: str, updates: dict) -> bool:
        """Update a specific topic in the syllabus."""
        file_path = self.templates_dir / f"{exam.lower()}_{subject.lower()}.json"

        if not file_path.exists():
            return False

        with open(file_path, "r") as f:
            data = json.load(f)

        topics = data.get("topics", [])
        for topic in topics:
            if topic.get("id") == topic_id:
                topic.update(updates)
                with open(file_path, "w") as f:
                    json.dump(data, f, indent=2)
                return True

        return False

    def sync_from_directory(self, source_dir: Path) -> Dict[str, List[str]]:
        """Sync all syllabi from a source directory."""
        results = {"added": [], "updated": [], "failed": []}

        for file_path in source_dir.glob("*.json"):
            try:
                with open(file_path, "r") as f:
                    data = json.load(f)

                exam = data.get("exam", file_path.stem.split("_")[0].upper())
                subject = data.get("subject", file_path.stem.split("_")[1].title() if "_" in file_path.stem else "Unknown")

                dest_path = self.templates_dir / f"{exam.lower()}_{subject.lower()}.json"

                if dest_path.exists():
                    results["updated"].append(f"{exam}/{subject}")
                else:
                    results["added"].append(f"{exam}/{subject}")

                with open(dest_path, "w") as f:
                    json.dump(data, f, indent=2)

            except Exception as e:
                results["failed"].append(f"{file_path.name}: {str(e)}")

        return results

    def get_last_modified(self, exam: str, subject: str) -> Optional[datetime]:
        """Get last modified timestamp for a syllabus."""
        file_path = self.templates_dir / f"{exam.lower()}_{subject.lower()}.json"

        if file_path.exists():
            return datetime.fromtimestamp(file_path.stat().st_mtime)

        return None

    def compare_versions(self, exam: str, subject: str, other_path: Path) -> dict:
        """Compare local and remote syllabus versions."""
        local_path = self.templates_dir / f"{exam.lower()}_{subject.lower()}.json"

        with open(local_path, "r") as f:
            local_data = json.load(f)

        with open(other_path, "r") as f:
            remote_data = json.load(f)

        local_topics = {t["id"] for t in local_data.get("topics", [])}
        remote_topics = {t["id"] for t in remote_data.get("topics", [])}

        return {
            "added": list(remote_topics - local_topics),
            "removed": list(local_topics - remote_topics),
            "common": list(local_topics & remote_topics),
        }