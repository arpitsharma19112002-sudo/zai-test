"""Translator module for multi-language support."""

import json
import logging
from typing import Any, Optional
from biopress.llm.factory import get_fallback_adapter
from biopress.llm.adapters.base import LLMAdapter

logger = logging.getLogger(__name__)

class Translator:
    """Translates content between English and other languages using LLM."""

    HINDI_TRANSITIONS = {
        "question": "प्रश्न",
        "options": "विकल्प",
        "correct_answer": "सही उत्तर",
        "explanation": "स्पष्टीकरण",
        "select_the_correct_answer": "सही उत्तर चुनें",
        "assertion": "अभिकथन",
        "reason": "कारण",
        "statement_i": "कथन I",
        "statement_ii": "कथन II",
        "both_assertion_and_reason": "अभिकथन और कारण दोनों सही हैं",
        "assertion_true_reason_false": "अभिकथन सही है लेकिन कारण गलत है",
        "assertion_false_reason_true": "अभिकथन गलत है लेकिन कारण सही है",
        "both_false": "दोनों गलत हैं",
        "case_study": "केस स्टडी",
        "read_the_passage": "पैसेज पढ़ें और प्रश्नों का उत्तर दें",
        "numerical": "numerical",
        "solve_the_following": "निम्नलिखित प्रश्नों को हल करें",
        "topic": "विषय",
        "difficulty": "कठिनाई",
        "easy": "आसान",
        "medium": "मध्यम",
        "hard": "कठिन",
    }

    HINDI_UNIT_TRANSITIONS = {
        "m": "मी",
        "kg": "किग्रा",
        "s": "से",
        "A": "A",
        "K": "K",
        "mol": "मोल",
        "cd": "cd",
        "Hz": "Hz",
        "N": "N",
        "J": "J",
        "W": "W",
        "Pa": "Pa",
        "V": "V",
        "ohm": "ओम",
        "m/s": "मी/से",
        "m/s²": "मी/से²",
        "kg/m³": "किग्रा/मी³",
    }

    def __init__(self, language: Any = "english"):
        self.language = language if language else "english"
        self._llm: Optional[LLMAdapter] = None
        self.use_llm = self.language.lower() != "english"

    def _get_llm(self) -> Optional[LLMAdapter]:
        if not self.use_llm:
            return None
        if self._llm is None:
            try:
                self._llm = get_fallback_adapter()
            except Exception as e:
                logger.warning(f"Failed to initialize Translator LLM adapter: {e}")
                self.use_llm = False
        return self._llm

    def translate_question(self, text: str) -> str:
        """Translate question text."""
        if self.language.lower() == "english":
            return text
        llm = self._get_llm()
        if not llm:
            return text
        prompt = f"Translate the following educational question text into {self.language} accurately, preserving any scientific formatting or math:\n{text}\n\nReturn EXACTLY the translated string, no quotes or markdown."
        try:
            return llm.generate(prompt, max_tokens=300).strip()
        except:
            return text

    def translate_options(self, options: list[str]) -> list[str]:
        """Translate options."""
        if self.language.lower() == "english":
            return options
        return [self.translate_question(opt) for opt in options]

    def translate_explanation(self, text: str) -> str:
        """Translate explanation text."""
        return self.translate_question(text)

    def get_label(self, key: str) -> str:
        """Get translated label for UI elements."""
        if self.language.lower() == "english":
            return key
        # We only have Hindi static labels currently, expand as needed
        if self.language.lower() == "hindi":
            return self.HINDI_TRANSITIONS.get(key, key)
        return key

    def translate_field(self, field_name: str) -> str:
        """Translate field names in question data."""
        if self.language.lower() == "english":
            return field_name
        if self.language.lower() == "hindi":
            return self.HINDI_TRANSITIONS.get(field_name, field_name)
        return field_name

    def translate_quiz(self, quiz_data: dict) -> dict:
        """Translate entire quiz data."""
        if self.language.lower() == "english":
            return quiz_data

        translated = quiz_data.copy()
        if "items" in translated:
            translated["items"] = [
                self.translate_question_item(item) for item in translated["items"]
            ]
        return translated

    def translate_question_item(self, item: dict) -> dict:
        """Translate a single question item using a single batch LLM call to save tokens and time."""
        if self.language.lower() == "english":
            return item

        llm = self._get_llm()
        if not llm:
            # Fallback to pure dictionary mapping if LLM fails
            translated = item.copy()
            if self.language.lower() == "hindi":
                for en, hi in self.HINDI_TRANSITIONS.items():
                    if en in translated:
                        if isinstance(translated[en], str):
                            translated[hi] = translated.pop(en)
                        elif en == "options" and isinstance(translated[en], list):
                            translated[hi] = translated.pop(en)
            return translated

        # Collect text fields to translate
        text_fields = {}
        for key in ["question", "explanation", "assertion", "reason", "passage", "answer"]:
            if key in item and isinstance(item[key], str) and item[key].strip():
                text_fields[key] = item[key]
        
        if "options" in item and isinstance(item["options"], list):
            text_fields["options"] = item["options"]
            
        if "solution_steps" in item and isinstance(item["solution_steps"], list):
            text_fields["solution_steps"] = item["solution_steps"]

        if not text_fields:
            return item

        prompt = (
            f"You are an expert academic translator. Translate the following JSON object's values from English to {self.language}.\n"
            f"Preserve the exact JSON structure and keys, but translate all the string values.\n"
            f"Maintain any scientific terms, chemical formulas, and mathematical notation accurately.\n\n"
            f"{json.dumps(text_fields, indent=2)}\n\n"
            f"Return ONLY the translated JSON object."
        )

        translated = item.copy()
        try:
            response = llm.generate(prompt, max_tokens=1000)
            
            # Simple JSON parse attempt
            start = response.find("{")
            end = response.rfind("}")
            if start != -1 and end != -1:
                parsed = json.loads(response[start:end+1])
                for k, v in parsed.items():
                    if k in translated:
                        translated[k] = v
        except Exception as e:
            logger.warning(f"Batch translation failed: {e}")
            
        # Translate keys based on language (e.g. Hindi static map)
        if self.language.lower() == "hindi":
            final_item = {}
            for k, v in translated.items():
                new_key = self.HINDI_TRANSITIONS.get(k, k)
                final_item[new_key] = v
            return final_item
            
        return translated
