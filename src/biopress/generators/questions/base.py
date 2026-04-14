"""Base Generator for dual-mode LLM and static template generation."""

import json
import re
from pathlib import Path
from typing import Any, Generic, TypeVar, Optional, Type
from pydantic import BaseModel
import logging

from biopress.core.token_tracker import TokenTracker
from biopress.llm.factory import get_fallback_adapter
from biopress.llm.adapters.base import LLMAdapter

T_Item = TypeVar("T_Item", bound=BaseModel)
T_Quiz = TypeVar("T_Quiz", bound=BaseModel)
logger = logging.getLogger(__name__)

class BaseGenerator(Generic[T_Quiz, T_Item]):
    """Base class for question generators with dual-mode LLM and static support."""
    
    QUIZ_CLASS: Type[T_Quiz]
    ITEM_CLASS: Type[T_Item]
    
    def __init__(self, templates_dir: str | None = None, use_llm: bool = True):
        if templates_dir:
            self.templates_dir = Path(templates_dir)
        else:
            self.templates_dir = Path(__file__).parent.parent / "templates"
        self.use_llm = use_llm
        self._llm: Optional[LLMAdapter] = None

    def _get_llm(self) -> Optional[LLMAdapter]:
        """Lazy load the LLM adapter."""
        if not self.use_llm:
            return None
        if self._llm is None:
            try:
                self._llm = get_fallback_adapter()
            except Exception as e:
                logger.warning(f"Failed to initialize LLM generator fallback adapter: {e}")
                self.use_llm = False
        return self._llm

    def _load_templates(self, subject: str, prefix: str = "", default_prefix: str = "") -> dict[str, Any]:
        """Load static JSON templates for the given subject and prefix."""
        template_file = self.templates_dir / f"{prefix}{subject.lower()}.json"
        if not template_file.exists():
            template_file = self.templates_dir / f"{default_prefix}physics.json"
            
        try:
            with open(template_file) as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load templates from {template_file}: {e}")
            return {"default": []}

    def _parse_json(self, response: str) -> list[dict[str, Any]]:
        """Robustly parse JSON, stripping markdown code blocks if necessary."""
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            pass

        match = re.search(r"```(?:json)?\s*(.*?)\s*```", response, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass
                
        start = response.find("[")
        end = response.rfind("]")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(response[start:end+1])
            except json.JSONDecodeError:
                pass
                
        return []

    def _generate_with_llm(
        self,
        exam: str,
        subject: str,
        count: int,
        topic: str,
        topic_lower: str,
        templates: dict[str, Any],
    ) -> list[T_Item]:
        """Attempt to generate questions using the LLM backend."""
        llm = self._get_llm()
        if not llm:
            return []
            
        type_name = self.ITEM_CLASS.__name__
        schema = self.ITEM_CLASS.model_json_schema()
        
        examples = templates.get(topic_lower, templates.get("default", []))
        example_str = json.dumps(examples[:2], indent=2) if examples else "[]"
        
        prompt = (
            f"Generate exactly {count} {type_name} questions for the {exam} exam on the subject of {subject}, "
            f"specifically focusing on the topic '{topic}'.\n\n"
            f"You MUST output a valid JSON array of objects that strictly adhere to this schema:\n"
            f"{json.dumps(schema, indent=2)}\n\n"
            f"Here are some examples of the expected quality and format:\n"
            f"{example_str}\n\n"
            f"Return ONLY the raw JSON array. Do not include markdown formatting or explanations."
        )

        try:
            response = llm.generate(prompt, max_tokens=count * 300)
            parsed = self._parse_json(response)
            
            if not parsed or not isinstance(parsed, list):
                logger.warning(f"LLM produced invalid JSON structure: {parsed}")
                return []
                
            questions = []
            for item in parsed:
                q = self._parse_item(item)
                if q:
                    questions.append(q)
            return questions
        except Exception as e:
            logger.warning(f"LLM generation failed: {e}. Falling back to static templates.")
            return []

    def _parse_item(self, item: dict[str, Any]) -> Optional[T_Item]:
        """Convert a raw dictionary item into a Pydantic model instance."""
        try:
            return self.ITEM_CLASS(**item)
        except Exception as e:
            logger.warning(f"Failed to parse item into {self.ITEM_CLASS.__name__}: {e}")
            return None

    def generate(
        self,
        exam: str,
        subject: str,
        count: int,
        topic: str,
        prefix: str = "",
        default_prefix: str = "",
    ) -> T_Quiz:
        """Generate questions using dual-mode fallback (LLM -> Static)."""
        templates = self._load_templates(subject, prefix, default_prefix)
        topic_lower = topic.lower()
        
        TokenTracker.record_template_lookup(1)
        
        llm_questions = []
        if self.use_llm:
            llm_questions = self._generate_with_llm(exam, subject, count, topic, topic_lower, templates)
            if len(llm_questions) >= count:
                return self.QUIZ_CLASS(items=llm_questions[:count])
            elif len(llm_questions) > 0:
                logger.warning(f"LLM returned {len(llm_questions)} questions, needed {count}. Filling remainder with templates.")
        
        questions = llm_questions.copy()
        pool = templates.get(topic_lower, templates.get("default", []))
        
        if not pool:
            return self.QUIZ_CLASS(items=questions)
            
        for template in pool:
            if len(questions) >= count:
                break
            q = self._parse_item(template)
            if q:
                questions.append(q)

        while len(questions) < count:
            idx = len(questions) % len(pool)
            template = pool[idx]
            q = self._parse_item(template)
            if q:
                questions.append(q)

        return self.QUIZ_CLASS(items=questions[:count])

    def to_json(self, quiz: T_Quiz) -> str:
        """Convert quiz to JSON string."""
        return json.dumps(quiz.model_dump(), indent=2)
