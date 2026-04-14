"""Knowledge base manager."""

from typing import Dict, List, Optional
from datetime import datetime, timezone

from biopress.kb.loader import KBLoader
from biopress.kb.syllabus import Syllabus
from biopress.kb.rules import ValidationRules, RulesEngine


class KBManager:
    """Manages the knowledge base for BioPress."""

    def __init__(self):
        self.loader = KBLoader()
        self._loaded_kb: Dict[str, Dict[str, Syllabus]] = {}
        self._load_status: Dict[str, dict] = {}
        self._rules: Dict[str, ValidationRules] = {}

    def load_exam(self, exam: str) -> bool:
        """Load knowledge base for a specific exam."""
        try:
            syllabi = self.loader.load_exam(exam)
            if not syllabi:
                return False

            self._loaded_kb[exam] = syllabi
            self._load_status[exam] = {
                "loaded_at": datetime.now(timezone.utc).isoformat(),
                "subjects": list(syllabi.keys()),
                "total_topics": sum(len(s.topics) for s in syllabi.values()),
            }

            self._rules[exam] = self._create_default_rules(exam)
            return True
        except Exception:
            return False

    def _create_default_rules(self, exam: str) -> ValidationRules:
        """Create default validation rules for an exam."""
        rules = [
            {
                "id": f"{exam.lower()}-rule-001",
                "name": "Syllabus must have topics",
                "description": "Each subject must have at least one topic",
                "condition": "has_topics",
                "severity": "error",
            },
            {
                "id": f"{exam.lower()}-rule-002",
                "name": "Topics must have weightage",
                "description": "All topics must have weightage assigned",
                "condition": "has_weightage",
                "severity": "warning",
            },
        ]
        return ValidationRules(exam=exam, rules=rules)

    def is_loaded(self, exam: str) -> bool:
        """Check if an exam is loaded."""
        return exam in self._loaded_kb

    def get_syllabus(self, exam: str, subject: str) -> Optional[Syllabus]:
        """Get syllabus for a specific exam and subject."""
        if exam in self._loaded_kb:
            return self._loaded_kb[exam].get(subject)
        return None

    def get_subjects(self, exam: str) -> List[str]:
        """Get list of subjects for an exam."""
        if exam in self._loaded_kb:
            return list(self._loaded_kb[exam].keys())
        return []

    def get_topics(self, exam: str, subject: str) -> List[dict]:
        """Get all topics for a subject."""
        syllabus = self.get_syllabus(exam, subject)
        if syllabus:
            return [topic.model_dump() for topic in syllabus.topics]
        return []

    def get_loaded_exams(self) -> List[str]:
        """Get list of loaded exams."""
        return list(self._loaded_kb.keys())

    def get_load_status(self, exam: str) -> Optional[dict]:
        """Get load status for an exam."""
        return self._load_status.get(exam)

    def get_all_status(self) -> Dict[str, dict]:
        """Get load status for all exams."""
        return self._load_status

    def validate(self, exam: str) -> List[dict]:
        """Validate the loaded knowledge base."""
        if exam not in self._rules:
            return []

        rules_engine = RulesEngine(self._rules[exam])
        data = {
            "syllabus": list(self._loaded_kb.get(exam, {}).values()),
            "topics": [
                t.model_dump() for s in self._loaded_kb.get(exam, {}).values()
                for t in s.topics
            ],
        }
        return rules_engine.evaluate(data)

    def get_info(self, exam: str) -> Optional[dict]:
        """Get detailed information about a loaded exam."""
        if exam not in self._loaded_kb:
            return None

        syllabi = self._loaded_kb[exam]
        return {
            "exam": exam,
            "subjects": list(syllabi.keys()),
            "topics_per_subject": {s: len(syllabi[s].topics) for s in syllabi},
            "total_topics": sum(len(s.topics) for s in syllabi.values()),
            "patterns": syllabi[list(syllabi.keys())[0]].patterns if syllabi else {},
        }

    def search(self, exam: str, query: str, max_results: int = 20) -> List[dict]:
        """Search the knowledge base for topics matching the query."""
        if exam not in self._loaded_kb:
            return []

        query_lower = query.lower()
        results = []
        syllabi = self._loaded_kb[exam]

        for subject, syllabus in syllabi.items():
            for topic in syllabus.topics:
                score = 0
                matched_fields = []

                if query_lower in topic.name.lower():
                    score += 10
                    matched_fields.append("name")

                for subtopic in topic.subtopics:
                    if query_lower in subtopic.lower():
                        score += 5
                        if "subtopics" not in matched_fields:
                            matched_fields.append("subtopics")

                if score > 0:
                    results.append({
                        "id": topic.id,
                        "name": topic.name,
                        "subject": subject,
                        "weightage": topic.weightage,
                        "difficulty": topic.difficulty,
                        "score": score,
                        "matched_fields": matched_fields,
                    })

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:max_results]

    def query(self, exam: str, subject: Optional[str] = None, topic_id: Optional[str] = None) -> List[dict]:
        """Query the knowledge base."""
        if exam not in self._loaded_kb:
            return []

        results = []
        syllabi = self._loaded_kb[exam]

        if subject is not None and subject in syllabi:
            syllabus = syllabi[subject]
            if topic_id:
                for topic in syllabus.topics:
                    if topic.id == topic_id:
                        results.append({**topic.model_dump(), "subject": subject})
            else:
                results.extend([{**t.model_dump(), "subject": subject} for t in syllabus.topics])
        elif topic_id and not subject:
            for s, syllabus in syllabi.items():
                for topic in syllabus.topics:
                    if topic.id == topic_id:
                        results.append({**topic.model_dump(), "subject": s})
                        break
        else:
            for s, syllabus in syllabi.items():
                results.extend([{**t.model_dump(), "subject": s} for t in syllabus.topics])

        return results


_kb_manager = None


def get_kb_manager() -> KBManager:
    """Get the global KB manager instance."""
    global _kb_manager
    if _kb_manager is None:
        _kb_manager = KBManager()
    return _kb_manager