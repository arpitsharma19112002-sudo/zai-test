# Phase 3: LLM Adapters + Validators — Expert Review Findings

> **Files Reviewed:** ~14 files, ~1,650 LOC  
> **Overall Module Health:** ⭐ 6.5 / 10

> [!NOTE]
> The architecture is well-designed with clean abstractions (ABC for adapters, L1/L2 validation pipeline, single-pass optimization). However, every LLM adapter silently degrades to useless fallback strings, validators have duplicate type definitions, and the `validate_content()` method across all adapters is fake.

---

## 🔴 Critical Issues (6)

### CRIT-1: All Adapters Silently Degrade to Useless Fallback Strings

**Files:** `claude.py:87-89`, `grok.py:85-87`, `kiloclaw.py:68-70`, `mimoclaw.py:68-70`, `ollama.py:55-57`

Every adapter has the same fallback pattern:

```python
def _fallback_generate(self, prompt: str, max_tokens: int) -> str:
    return f"[Claude fallback] Processed: {prompt[:100]}..."
```

When the API key is missing **or** when any `Exception` occurs during the HTTP call, the adapter returns this string instead of raising an error. This means:

1. **No API key configured?** → Silent fallback, no error.
2. **Network timeout?** → Silent fallback, no error.
3. **Rate limited?** → Silent fallback, no error.
4. **Invalid model name?** → Silent fallback, no error.

The downstream generator or validator receives `"[Claude fallback] Processed: Generate 5 MCQ..."` as if it were a valid LLM response and tries to parse it.

> [!CAUTION]
> The L2 validator's `_parse_llm_response` will parse `"[Claude fallback]..."` and extract `SCORE: 50` (default) with empty reasoning. Every question will silently pass with a fake score. **You have zero quality assurance without API keys.**

**Fix:** Raise `LLMUnavailableError` instead of returning garbage. Let the caller decide whether to skip validation or fail loudly. Add a `strict_mode` flag if graceful degradation is needed.

---

### CRIT-2: `validate_content()` is Hardcoded to Always Pass

**Files:** `claude.py:58-67`, `grok.py:59-68`, `kiloclaw.py:42-51`, `mimoclaw.py:42-51`, `ollama.py:35-44`

Every adapter's `validate_content()` ignores the LLM response and returns a hardcoded passing result:

```python
def validate_content(self, content: dict) -> ValidationResult:
    prompt = f"Validate: {content.get('question', '')}"
    self.generate(prompt, max_tokens=500)  # Response discarded!
    return ValidationResult(
        is_valid=True,     # Always true
        score=0.98,        # Always 0.98 (or 0.95, 0.9, 0.85, 0.8)
        issues=[],         # Always empty
        provider=self.name,
    )
```

The LLM response is **generated but never used**. This wastes tokens/money and returns meaningless results. Each adapter has a different hardcoded score (Claude: 0.98, Grok: 0.95, MiMo: 0.9, Kilo: 0.85, Ollama: 0.8), creating an illusion of provider quality differences when none exists.

**Fix:** Parse the LLM response or remove the method entirely and rely on the L2 validator (which actually parses responses).

---

### CRIT-3: `BudgetExceededError` Defined in Multiple Files

**Files:** `claude.py:8-10`, `grok.py:8-10`

```python
class BudgetExceededError(Exception):
    """Raised when budget is exceeded."""
    pass
```

This exception class is defined identically in both `claude.py` and `grok.py`, but **not** in `kiloclaw.py`, `mimoclaw.py`, or `ollama.py`. This means:
- `try/except BudgetExceededError` from one module won't catch it from the other.
- KiloClaw, MiMoClaw, and Ollama have **no budget checking at all**.

> [!WARNING]
> You can blow through your entire LLM budget using KiloClaw or MiMoClaw because they never call `cost_manager.check_budget()`.

**Fix:** Define `BudgetExceededError` once in `base.py`. Add budget checking to all adapters or enforce it at the factory/pool level.

---

### CRIT-4: Duplicate `ValidationResult` and `L2Result` Type Definitions

**Files:** `base.py:7-13` vs `types.py:6-12` vs `validator.py:19-27` vs `types.py:15-23`

There are **three different** `ValidationResult` classes:

| Location | Type | Fields |
|---|---|---|
| `llm/adapters/base.py:7` | `@dataclass` | `is_valid`, `score: float`, `issues: list[str]`, `provider: str` |
| `validators/l2/types.py:6` | `@dataclass` | `passed: bool`, `score: int`, `reasons: list[str]`, `suggestions: list[str]` |
| (Also using) `L2Result` | defined in both `types.py:15` **and** `validator.py:19` |

The LLM adapter's `ValidationResult` has `is_valid` + `score: float` + `issues`, while the L2 validator's has `passed` + `score: int` + `reasons` + `suggestions`. These are incompatible types with the same conceptual purpose but different field names and types.

`L2Result` is also defined in **both** `types.py:15-23` and `validator.py:19-27`. The `__init__.py` exports both under the same name, and since `validator.py` is imported last, it shadows the one from `types.py`.

**Fix:** Single `ValidationResult` in `types.py`, used by both LLM adapters and validators. Delete the duplicate `L2Result` from `types.py` (the `validator.py` version is the authoritative one).

---

### CRIT-5: Claude Token Counting is Inaccurate

**File:** `claude.py:51-52`

```python
tokens_in = len(prompt.split()) * 1.3
tokens_out = len(data["content"][0]["text"].split()) * 1.3
```

Token counts are estimated by `word_count * 1.3`, which is a rough heuristic. Claude's API response includes `usage.input_tokens` and `usage.output_tokens` as exact values, but they're never read. Meanwhile, Grok (`grok.py:50-54`) correctly reads `usage.prompt_tokens` and `usage.completion_tokens` from the response.

> [!WARNING]
> The cost tracker receives estimated (inaccurate) token counts for Claude while getting real counts for Grok. Budget tracking is unreliable.

**Fix:** Read `data["usage"]["input_tokens"]` and `data["usage"]["output_tokens"]` from the Claude response.

---

### CRIT-6: `DifficultyChecker._calculate_score` Has Wrong Scale

**File:** `difficulty_checker.py:107-121`

```python
DIFFICULTY_SCORES = {
    "easy": 30,
    "medium": 60,
    "hard": 90,
}

def _calculate_score(self, detected: str, expected: str) -> int:
    if detected == expected:
        return 100
    difference = abs(expected_val - detected_val)
    if difference == 1:   # Never true! Differences are 30, 60, etc.
        return 80
    elif difference == 2: # Never true!
        return 60
    return 40
```

The `difference` between scores is `30` (easy→medium), `60` (easy→hard), or `30` (medium→hard). But the conditions check for `difference == 1` and `difference == 2`. **These will never be true.** Any mismatch falls through to `return 40`.

This means the score is binary: 100 (exact match) or 40 (any mismatch). The intended gradual scoring between adjacent difficulties doesn't work.

**Fix:** Check `difference <= 30` for "close match" (80 points), `difference <= 60` for "far match" (60 points).

---

## 🟡 Architecture Improvements (5)

### ARCH-1: Massive Code Duplication Across 5 Adapters

All 5 LLM adapters (~70-89 LOC each) share almost identical structure:
- `__init__`: config + api_key + base_url (5×)
- `generate()`: budget check → requests.post → cost tracking → fallback (5×)
- `validate_content()`: hardcoded response (5×)
- `check_connection()`: GET /models (5×)
- `_fallback_generate()`: f-string (5×)

**~350 LOC** of near-identical code. Should extract `BaseHTTPAdapter(LLMAdapter)` with configuration-driven differences.

### ARCH-2: `ConnectionPool` is Not Actually a Pool

`pool.py` — The class holds a single adapter instance, not a pool. It doesn't manage connection limits, reuse, health checking intervals, or queue depth. It's closer to a "lazy singleton with fallback" pattern. The name is misleading for anyone expecting connection pool semantics.

### ARCH-3: Async Support is Half-Baked

`validator.py:175-192` — `validate_batch_async` uses `asyncio.get_event_loop()` (deprecated since Python 3.10) and wraps synchronous `self.validate()` in `run_in_executor`. Since all LLM calls use synchronous `requests.post`, there's no actual async benefit — just thread pool overhead.

**Fix:** Either use `httpx.AsyncClient` in adapters for real async, or remove the async facade.

### ARCH-4: 3 Duplicate `MockLLMAdapter` Classes

`MockLLMAdapter` is defined in `validator.py:238`, `single_pass.py:279`, `context_checker.py:140`, `difficulty_checker.py:124`, and `relevance_checker.py:98`. **5 separate implementations** that should be one class in `tests/conftest.py` or a shared module.

### ARCH-5: `requests` Imported Inside Methods, Not at Top

Every adapter does `import requests` inside `generate()` and `check_connection()`. This means:
- Import error is deferred, making `pip install` issues harder to debug.
- Slight performance overhead on repeated calls (though CPython caches imports).
- Inconsistent with PEP 8 which recommends top-level imports.

**Fix:** Top-level `import requests` (or optional import with clear error message).

---

## 🟢 Polish Items (6)

| ID | File | Issue |
|---|---|---|
| POL-1 | `factory.py:22` | Fallback order `["ollama", "claude", ...]` tries Ollama first — likely to fail in CI/cloud |
| POL-2 | `claude.py:43` | Model hardcoded to `claude-3-5-sonnet-20241022` — should be configurable |
| POL-3 | `grok.py:42` | Model hardcoded to `grok-2` — should be configurable |
| POL-4 | `ollama.py:15` | Default model `llama2` — should probably be `llama3.2` or latest |
| POL-5 | `validators/__init__.py:3` | `__all__ = ["l1", "l2"]` exports module names, not classes — consumers can't `from biopress.validators import L1Validator` |
| POL-6 | `l1/__init__.py:3` | `__all__` lists `"L1Validator"` but actual import on line 7 aliases `L1Validator = MathValidator` — works but confusing |

---

## 📊 Module Scorecard

| Module | Score | Highlights | Concerns |
|---|---|---|---|
| `adapters/base.py` | 8/10 | Clean ABC with 3 abstract methods | `ValidationResult` conflicts with L2 types |
| `adapters/claude.py` | 6/10 | Real API integration, budget check | Fake token counting, validate_content no-op |
| `adapters/grok.py` | 7/10 | Uses real usage stats from API | Budget error class duplicated |
| `adapters/kiloclaw.py` | 4/10 | Matches OpenAI-compatible pattern | No budget checking, no cost tracking |
| `adapters/mimoclaw.py` | 4/10 | Matches OpenAI-compatible pattern | No budget checking, no cost tracking |
| `adapters/ollama.py` | 6/10 | Local model support, correct API | No cost tracking, no budget |
| `factory.py` | 8/10 | Clean factory + fallback | No caching of adapter instances |
| `pool.py` | 5/10 | Lazy init, provider switching | Not a real pool, thread-unsafe singleton |
| `validators/l1/math_validator.py` | 8/10 | Solid SymPy integration, caching | Global mutable cache, no thread safety |
| `validators/l1/unit_validator.py` | 8/10 | Comprehensive unit tables | Static validation only, no dimensional analysis |
| `validators/l2/validator.py` | 7/10 | Weighted scoring, async batch | Mock in prod code, deprecated asyncio API |
| `validators/l2/single_pass.py` | 8/10 | L1+L2 combined, exam rules | Duplicate with validator.py patterns |
| `validators/l2/types.py` | 6/10 | Shared types concept | Duplicate L2Result, conflicts with base.py |
| `validators/l2/relevance_checker.py` | 7/10 | Good prompt engineering | LLM parsing fragile |
| `validators/l2/difficulty_checker.py` | 5/10 | Clean structure | Score calculation broken |
| `validators/l2/context_checker.py` | 7/10 | Grade-level aware scoring | Naive "no" detection in parsing |

---

## Summary Verdict

The LLM + Validators layer has the **best architecture** of any layer so far — clean ABCs, factory pattern, L1/L2 tiered validation, single-pass optimization, weighted scoring. But the execution has critical gaps:

| Aspect | Architecture | Implementation |
|---|---|---|
| Adapter abstraction | ✅ Clean ABC | ❌ Silent fallbacks, fake validation |
| Budget control | ✅ CostManager integration (2/5 adapters) | ❌ Missing from 3 adapters |
| L1 validation (math) | ✅ SymPy + caching | ✅ Works correctly |
| L2 validation (quality) | ✅ 3-checker pipeline + single-pass | ⚠️ Difficulty scoring broken |
| Type safety | ⚠️ Shared types module exists | ❌ 3 conflicting `ValidationResult` defs |
| Code reuse | ❌ 350 LOC duplicated across adapters | ❌ 5 duplicate MockLLMAdapter classes |

> [!IMPORTANT]
> **Founder-level assessment:** L1 (SymPy math validation) is production-ready and a genuine differentiator. L2 (LLM-based quality) has excellent design but will silently pass everything when API keys are missing. The adapter layer needs a "strict vs. graceful" mode decision, and budget enforcement must cover all providers.

---

## ✅ Hardening Compliance Checklist

Status as of Phase 7.2 Hardening Sweep:

| ID | Task | Status | Detail |
|---|---|---|---|
| CRIT-3 | Consolidated Exceptions | ✅ COMPLETED | `BudgetExceededError` & `LLMConnectionError` moved to `core/errors.py`. |
| CRIT-4 | Unified Result Types | ✅ COMPLETED | `ValidationResult` & `L2Result` centralized in `biopress.core.types`. |
| CRIT-6 | Difficulty Scoring Logic | ✅ COMPLETED | Fixed in `difficulty_checker.py` to use expected scale (0.0-1.0). |
| CRIT-1 | Silent Adapter Fallbacks | ⏳ PENDING | Adapters still return fallback strings in some cases; needs loud fail mode. |
| CRIT-2 | Fake `validate_content()` | ⏳ PENDING | Adapter-level validation still hardcoded. |
| CRIT-5 | Claude Token Counting | ⏳ PENDING | Still uses heuristic; needs usage stats switch. |


---

## 🚀 Phase 8: Final Polish Scheduled

Remaining tasks from this phase have been scheduled for **Phase 8: Final Feature Completeness**.
See the master tracker in `tasks.md` or `plan.md` for sprint assignments.

