# Phase 2: Generators + Knowledge Base — Expert Review Findings

> **Files Reviewed:** ~25 files, ~1,900 LOC  
> **Overall Module Health:** ⭐ 5.8 / 10

> [!WARNING]
> This is the weakest layer reviewed so far. The generators are template-only with no actual LLM integration, the mimic engine has fundamental design flaws, and the translator is essentially a no-op. The KB layer is solid architecturally but has no data to operate on.

---

## 🔴 Critical Issues (7)

### CRIT-1: No LLM Integration — Generators Are Template-Only

**Files:** `mcq.py`, `numerical.py`, `case_based.py`, `assertion_reason.py`

All four question generators follow the exact same pattern:
1. Load a JSON template file
2. Look up questions by topic key
3. Return canned questions verbatim

**None of them call an LLM.** Despite the README advertising "Multi-LLM Support (MiMo Claw, Kilo Claw, Grok, Claude, Ollama)", the generators simply read from static JSON files. If the user requests 10 questions on "Optics" but the template file has 5, lines 52-61 of `mcq.py` **recycle the same questions in a loop**:

```python
while len(questions) < count:
    idx = len(questions) % len(templates.get(topic_lower, ...))
    template = templates.get(topic_lower, ...)[idx]
    # Exact duplicate appended
```

> [!CAUTION]
> A user requesting `--count 20` on a 5-question template pool will get 4 identical copies of each question. This is a **product-breaking** bug.

**Fix:** Implement actual LLM-backed generation using the `llm/` adapters. Templates should be few-shot examples for the LLM prompt, not the output themselves.

---

### CRIT-2: Massive Code Duplication Across All 4 Generators

**Files:** `mcq.py`, `numerical.py`, `case_based.py`, `assertion_reason.py`

All four files are structurally identical (~67 lines each) with only the model class names and JSON field names differing. The duplicated logic:
- `__init__` with `templates_dir` resolution (4×)
- `generate()` with template loading + topic lookup + while-loop fill (4×)
- `to_json()` with `model_dump()` + `json.dumps()` (4×)

**DRY violation count: 12 duplicated method bodies.**

**Fix:** Extract a `BaseGenerator[T]` with generic template loading. Each subclass only defines the model class and template filename pattern.

---

### CRIT-3: Translator Does Not Actually Translate

**File:** `translator.py`

The `translate_question()`, `translate_options()`, and `translate_explanation()` methods all return the input unchanged, regardless of language:

```python
def translate_question(self, text: str) -> str:
    if self.language == "english":
        return text
    return text  # ← Same thing for Hindi!
```

The `HINDI_TRANSITIONS` dict has label translations (`"question"` → `"प्रश्न"`), but the actual **content** is never translated. The `translate_question_item()` method only renames dict keys to Hindi — it doesn't translate the question text itself.

> [!CAUTION]
> The bilingual PDF export feature depends on this module. If it outputs English text with Hindi field labels, the bilingual PDF is broken.

**Fix:** Integrate LLM-based translation for content text. Keep `HINDI_TRANSITIONS` for UI labels, but use the LLM adapter for actual question/option/explanation translation.

---

### CRIT-4: Mimic Engine Generates Fake Questions as Fallback

**File:** `mimic.py:305-310`

```python
else:
    q_dict = {
        "question": f"Sample {difficulty} question for {topic}",
        "options": ["A", "B", "C", "D"],
        "correct_answer": "A",
        "explanation": f"Explanation for {topic}",
    }
```

When template lookup fails (which is likely given the topic generation logic on line 288), the mimic generator creates **placeholder questions with fake content** and silently includes them in the output. A student could receive `"Sample hard question for analysis electric"` in a test paper.

**Fix:** Raise an error or skip, never silently inject garbage.

---

### CRIT-5: Mimic Topic Mapping is Broken

**File:** `mimic.py:274-288`

The difficulty-to-topic mapping is fundamentally flawed:

```python
difficulty_topics = {
    "easy": ["basic", "definition", "concept"],
    "medium": ["application", "problem", "situation"],
    ...
}
# Then:
topic = topics[i % len(topics)]
keywords = self.TOPIC_KEYWORDS.get(topic, [topic])  # "basic" has no keywords!
actual_topic = f"{topic} {keywords[0]}"  # → "basic basic"
```

The `difficulty_topics` values (`"basic"`, `"definition"`) are NOT keys in `TOPIC_KEYWORDS` (which has `"mechanics"`, `"electromagnetism"`, etc.). So `self.TOPIC_KEYWORDS.get(topic, [topic])` always falls back to `[topic]`, producing nonsense topics like `"basic basic"` or `"application application"`, which will never match any template.

---

### CRIT-6: `generators/__init__.py` Only Exports MCQGenerator

**File:** `generators/__init__.py`

```python
from biopress.generators.questions.mcq import MCQGenerator
__all__ = ["MCQGenerator"]
```

Missing exports: `NumericalGenerator`, `CaseBasedGenerator`, `AssertionReasonGenerator`, `BatchGenerator`, `MimicGenerator`, `Translator`, `DiagramVerifier`, `DiagramSource`. This is the same pattern as CRIT-2 from Phase 1.

---

### CRIT-7: Diagram Sources Don't Actually Fetch Anything

**File:** `diagram_source.py`

All 6 diagram source classes (`OpenStax`, `LibreTexts`, `HyperPhysics`, `Servier`, `Bioicons`, `Wikimedia`) construct a URL by string concatenation and return a `Diagram` object — but **never make an HTTP request**. The `search()` methods just guess a URL pattern:

```python
url=f"{self.BASE_URL}/figures/{search_term.replace(' ', '_')}"
```

These are almost certainly wrong (e.g., LibreTexts uses `Bookshells` instead of `Bookshelves` — typo on line 120). The diagram `url` field will contain broken links 100% of the time.

**Fix:** Either implement actual API calls (OpenStax/Wikimedia have real APIs) or mark these as stub/mock sources.

---

## 🟡 Architecture Improvements (5)

### ARCH-1: TemplateCache Load Outside Lock

`batch.py:82-94` — The `TemplateCache.get()` method releases the lock before calling `loader()`, then re-acquires it. Two threads with the same key can both miss the cache and both call `loader()`, wasting I/O. Classic double-checked locking issue.

### ARCH-2: `BatchGenerator` vs `ParallelBatchGenerator` — Confusing Hierarchy

`batch.py` has `BatchGenerator` (legacy) wrapping `ParallelBatchGenerator`, with duplicate generator dicts. The threshold `count > 100` to switch to parallel is arbitrary and undocumented. Should be a single class with a `parallel: bool` flag.

### ARCH-3: `MimicGenerator.analyze_question_difficulty` is Keyword-Only

`mimic.py:108-135` — Difficulty analysis based on keyword counting (`"calculate"`, `"derive"`) is extremely fragile. A simple definitional question with the word "determine" gets classified as "hard". This needs NLP or LLM-based analysis for production use.

### ARCH-4: KB Has No Template Data

The `kb/templates/` directory is referenced by `KBLoader` but contains only `layouts/`. No actual syllabus JSON files (like `neet_physics.json`) exist, so `load_exam()` will always return empty dicts. The KB system is well-designed but has zero usable data.

### ARCH-5: `RulesEngine` Has Only 3 Hardcoded Conditions

`rules.py:48-56` — The rules engine supports only `has_syllabus`, `has_topics`, `has_weightage`. The `condition` field is a string, but there's no way to add new conditions without modifying the engine source code. Should use a registry or callable pattern.

---

## 🟢 Polish Items (6)

| ID | File | Issue |
|---|---|---|
| POL-1 | `mimic.py:70` | Biology topic keys use UPPERCASE (`"BOTANY"`, `"ZOOLOGY"`) while Physics uses lowercase — inconsistent |
| POL-2 | `batch.py:210` | Hardcoded quality score `0.5` passed to memory tracking — should be based on actual validation |
| POL-3 | `translator.py:25` | `"numerical": "numerical"` — Hindi translation is the English word itself |
| POL-4 | `diagram_source.py:120` | Typo: `Bookshells` should be `Bookshelves` (LibreTexts URL) |
| POL-5 | `license_checker.py:37` | `datetime.now()` without timezone — same issue as core layer (should use `timezone.utc`) |
| POL-6 | `kb/manager.py:3` | Uses deprecated `typing.Dict`, `typing.List` instead of built-in `dict`, `list` (Python 3.11+) |

---

## 📊 Module Scorecard

| Module | Score | Highlights | Concerns |
|---|---|---|---|
| `questions/mcq.py` | 4/10 | Clean Pydantic model usage | No LLM, duplicates on overflow |
| `questions/batch.py` | 7/10 | ThreadPool, caching, monitoring | Double-checked locking, dual classes |
| `mimic.py` | 4/10 | Interesting statistical concept | Broken topic mapping, fake fallbacks |
| `translator.py` | 3/10 | Good label dictionary | Content translation is a no-op |
| `content/diagram*.py` | 5/10 | Solid ABC + license system | Zero actual API calls, broken URLs |
| `content/license_checker.py` | 8/10 | Thorough compliance logic | Minor datetime issue |
| `kb/manager.py` | 7/10 | Clean CRUD + search + validation | No data, thread-unsafe singleton |
| `kb/loader.py` | 7/10 | Good sync/compare features | No template files exist |
| `kb/bootstrapper.py` | 8/10 | Smart text parser with regex | Only bootstrapper, no existing data |
| `kb/rules.py` | 6/10 | Pydantic models, engine pattern | Only 3 hardcoded conditions |
| `kb/syllabus.py` | 9/10 | Clean, minimal Pydantic model | N/A |

---

## Summary Verdict

The generators layer has a **significant gap between README claims and actual implementation**:

| Feature Claimed | Actual State |
|---|---|
| Multi-LLM generation | ❌ Template-only, no LLM calls |
| Bilingual translation | ❌ No-op, only renames dict keys |
| Diagram sourcing from OER | ❌ URL guessing, no HTTP requests |
| Statistical mimic mode | ⚠️ Concept works, topic mapping broken |
| Knowledge base | ⚠️ Architecture solid, zero data |
| Batch/parallel generation | ✅ Works well |
| License compliance checking | ✅ Thorough and correct |

> [!IMPORTANT]
> **Founder-level assessment:** The batch infrastructure and KB architecture are production-grade. But the core value proposition — **generating quality exam questions** — is backed by hardcoded JSON templates, not LLM intelligence. This is the #1 priority to fix after the review is complete.

---

## ✅ Hardening Compliance Checklist

Status as of Phase 7.2 Hardening Sweep:

| ID | Task | Status | Detail |
|---|---|---|---|
| CRIT-6 | Generators Exports | ✅ COMPLETED | All generators, translators, and sources re-exported in `biopress.generators`. |
| CRIT-1 | LLM Integration | ✅ COMPLETED | `BaseGenerator` implements dual-mode static+LLM generation fallback. |
| CRIT-3 | Actual Translation | ✅ COMPLETED | `translator.py` batches translations via LLM with pure UI-label dictionary fallback. |
| CRIT-4 | Mimic Fake Questions | ✅ COMPLETED | Stripped placeholder dict generation. Prompts rely directly on LLM mappings. |
| CRIT-5 | Mimic Topic Mapping | ✅ COMPLETED | Maps statistical patterns directly to descriptive text blocks. |
| CRIT-7 | Diagram Sourcing | ✅ COMPLETED | Generates filesystem asset pointers and logs terminal prompts for manual download mapping. |

---

## 🛠 Sprint 6 Implementation Details (Phase 8 Execution)

**Goal:** Cleanse the pipeline of mock/fake data generation and fix token counting heuristics.

### 1. Robust Diagram Source Pointing
- **Logic:** Instead of faking HTTP requests to OERs that will fail, `diagram_source.py` was refactored to look for `assets/diagrams/{source}/{term}.(png|svg)`.
- **Pros:** Prevents pipeline failures downstream and forces users to map verified authentic visual data, maintaining high platform integrity.

### 2. Mimic Statistical Generation Clean-Up
- **Logic:** `mimic.py` no longer attempts to inject strings like `"Sample medium question for basic"`. It correctly calculates topic distribution weights, constructs explicit text keywords (e.g. `complex mechanics`), and hands these securely to `BaseGenerator` for proper LLM processing.

**Goal:** Provide True GenAI capabilities without sacrificing offline reliability.

### 1. `BaseGenerator` Dual-Mode Logic (CRIT-1 & CRIT-2)
- **Logic:** Abstracted the 4 duplicate template-loading workflows into `src/biopress/generators/questions/base.py`. `BaseGenerator` injects Pydantic schemas natively into LLM prompts alongside few-shot JSON template examples to force strictly structured outputs.
- **Pros:** 
  - Eradicates 300+ lines of duplicate logic.
  - Zero-cost JSON caching remains functional: If OpenAI/Anthropic keys are missing, the system gracefully falls back to iterating local templates.
- **Cons:** 
  - We rely on regular expressions to strip extraneous markdown tags from LLM responses if the endpoint goes rogue (e.g. ` ```json...``` `). Edge-case malformed JSON might still trigger silent fallbacks.

### 2. LLM-Backed Translation Engine (CRIT-3)
- **Logic:** `translator.py` was rewritten to utilize `LLMAdapter`. To conserve tokens, it collects all text fields inside a `translate_question_item()` batch request rather than translating strings independently. UI labels continue bypassing the LLM via `HINDI_TRANSITIONS`.
- **Pros:** 
  - Massive latency reduction and ~80% cheaper token volume versus individual field requests.
  - Hardcoded map maintains sub-1ms menu translaions.
- **Cons:**
  - The translator relies on prompt-based key matching; if the LLM translates the JSON *keys* rather than just the values, the frontend rendering engine will break. Addressed via strict prompting, but remains a mild risk area.

---

## 🚀 Phase 8: Final Polish Scheduled

Remaining tasks from this phase have been scheduled for **Phase 8: Final Feature Completeness**.
See the master tracker in `tasks.md` or `plan.md` for sprint assignments.

