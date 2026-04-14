# Phase 1: Core Layer — Expert Review Findings

> **Files Reviewed:** 7 files, ~1,100 LOC  
> **Overall Core Health:** ⭐ 7.2 / 10

---

## 🔴 Critical Issues (5)

### CRIT-1: Dual Version Definition — Drift Hazard

**Files:** [\_\_init\_\_.py](file:///Users/arpitsharma/Library/CloudStorage/GoogleDrive-arpit.sharma.19.11.2002@gmail.com/My%20Drive/BrightVidya/Researher/zai-test/src/biopress/__init__.py) + [\_\_version\_\_.py](file:///Users/arpitsharma/Library/CloudStorage/GoogleDrive-arpit.sharma.19.11.2002@gmail.com/My%20Drive/BrightVidya/Researher/zai-test/src/biopress/__version__.py) + [pyproject.toml](file:///Users/arpitsharma/Library/CloudStorage/GoogleDrive-arpit.sharma.19.11.2002@gmail.com/My%20Drive/BrightVidya/Researher/zai-test/pyproject.toml)

Version `"0.1.0"` is defined in **three places**:
1. `__init__.py` line 3
2. `__version__.py` line 3
3. `pyproject.toml` line 7

> [!CAUTION]
> If any one drifts, `pip show biopress` will disagree with `biopress.__version__`. Use a single source of truth — either `importlib.metadata.version("biopress")` or a `__version__.py` read by `pyproject.toml` via `dynamic = ["version"]`.

**Fix:** Delete `__version__.py`, make `__init__.py` read from `importlib.metadata`, and set `pyproject.toml` as the canonical source.

---

### CRIT-2: Incomplete `__init__.py` Re-exports

**File:** [core/\_\_init\_\_.py](file:///Users/arpitsharma/Library/CloudStorage/GoogleDrive-arpit.sharma.19.11.2002@gmail.com/My%20Drive/BrightVidya/Researher/zai-test/src/biopress/core/__init__.py)

`__all__` exports only `MCQItem`, `MCQOptions`, `PerseusQuiz`, `ExamType`, `Subject`, `QuestionType`. **Missing:**
- `NumericalItem`, `NumericalQuiz`
- `CaseBasedItem`, `CaseBasedSubQuestion`, `CaseBasedQuiz`
- `AssertionReasonItem`, `AssertionReasonQuiz`
- `BatchQuiz`
- `CostManager`, `TokenTracker`, `Memory`, `ProgressTracker`

This forces consumers to do deep imports like `from biopress.core.models import NumericalItem` instead of `from biopress.core import NumericalItem`.

---

### CRIT-3: Thread-Unsafe Global Singletons

**Files:** [cost_manager.py:158-166](file:///Users/arpitsharma/Library/CloudStorage/GoogleDrive-arpit.sharma.19.11.2002@gmail.com/My%20Drive/BrightVidya/Researher/zai-test/src/biopress/core/cost_manager.py#L158-L166), [memory.py:145-161](file:///Users/arpitsharma/Library/CloudStorage/GoogleDrive-arpit.sharma.19.11.2002@gmail.com/My%20Drive/BrightVidya/Researher/zai-test/src/biopress/core/memory.py#L145-L161), [token_tracker.py:120-214](file:///Users/arpitsharma/Library/CloudStorage/GoogleDrive-arpit.sharma.19.11.2002@gmail.com/My%20Drive/BrightVidya/Researher/zai-test/src/biopress/core/token_tracker.py#L120-L214)

All three use module-level `_instance = None` + `global` pattern, plus `TokenTracker` uses class-level state (`_current_report`). **None are thread-safe.** This matters because:
- FastAPI runs with `uvicorn` workers (concurrent requests)
- Two simultaneous `/generate` calls will corrupt the token tracker

> [!WARNING]
> `TokenTracker._current_report` is a **class variable**, not instance-level. Two concurrent generations stomp on each other's reports.

**Fix:** Use `threading.Lock` for singletons, and make `TokenTracker` instance-based (pass report via context, not class state).

---

### CRIT-4: Cost Pricing Inconsistency Between Modules

**Files:** [cost_manager.py:37-42](file:///Users/arpitsharma/Library/CloudStorage/GoogleDrive-arpit.sharma.19.11.2002@gmail.com/My%20Drive/BrightVidya/Researher/zai-test/src/biopress/core/cost_manager.py#L37-L42) vs [token_tracker.py:19](file:///Users/arpitsharma/Library/CloudStorage/GoogleDrive-arpit.sharma.19.11.2002@gmail.com/My%20Drive/BrightVidya/Researher/zai-test/src/biopress/core/token_tracker.py#L19)

Two completely different pricing systems exist side-by-side:

| Module | Input (per 1K) | Output (per 1K) | Unit |
|---|---|---|---|
| `CostManager.TOKEN_PRICES` (Claude) | $0.015 | $0.075 | per 1M tokens |
| `token_tracker.LLM_COST_PER_1K` | $0.001 | $0.002 | per 1K tokens |

These will produce **wildly different cost estimates** for the same usage. The `CostManager` divides by 1,000,000 (per-million pricing), while `TokenTracker` divides by 1,000 (per-thousand pricing). Different magnitude, different base rates.

> [!CAUTION]
> A 10K-token generation shows $0.00015 in CostManager but $0.01 in TokenTracker — a 66x discrepancy. Users will see contradictory cost info.

**Fix:** Single `PRICING` dict in `config.py`, referenced by both modules.

---

### CRIT-5: Memory Module — LIKE Pattern Allows Topic Injection

**File:** [memory.py:72-77](file:///Users/arpitsharma/Library/CloudStorage/GoogleDrive-arpit.sharma.19.11.2002@gmail.com/My%20Drive/BrightVidya/Researher/zai-test/src/biopress/core/memory.py#L72-L77)

```python
cursor = self._conn.execute(
    "SELECT ... WHERE pattern_key LIKE ?",
    (f"{topic}:%",),
)
```

While parameterized (good!), the `LIKE` operator still allows **wildcard injection** if `topic` contains `%` or `_`. A topic like `%` would match all records. This is a logic bug, not SQL injection, but still incorrect behavior.

**Fix:** Escape `%` and `_` in topic before building the LIKE pattern, or use `=` with exact prefix matching.

---

## 🟡 Architecture Improvements (6)

### ARCH-1: `ConfigManager` Creates New Instance Every Call

[config.py:93-95](file:///Users/arpitsharma/Library/CloudStorage/GoogleDrive-arpit.sharma.19.11.2002@gmail.com/My%20Drive/BrightVidya/Researher/zai-test/src/biopress/core/config.py#L93-L95) — `get_config_manager()` returns `ConfigManager()` fresh each time. CostManager calls `get_config_manager()` in `__init__`, `_check_reset`, `get_budget`, and `check_budget` — that's 4 disk reads per CostManager lifecycle. Should be a cached singleton like the others.

### ARCH-2: `BioPressConfig` and `ConfigManager` — Two Config Systems

`BioPressConfig` (Pydantic Settings, reads `.biopress.json` + env vars) and `ConfigManager` (raw JSON file at `~/.config/biopress/config.json`) are parallel, disconnected config systems. **Nobody uses `BioPressConfig`** — the rest of the codebase uses `ConfigManager`. The Pydantic model is dead code.

### ARCH-3: `CostManager.add_cost` Writes to Disk Every Call

[cost_manager.py:108-109](file:///Users/arpitsharma/Library/CloudStorage/GoogleDrive-arpit.sharma.19.11.2002@gmail.com/My%20Drive/BrightVidya/Researher/zai-test/src/biopress/core/cost_manager.py#L108-L109) — Every single LLM call triggers a full JSON serialize + file write. In a 50-question batch, that's 50+ file writes. Should batch/flush on session end.

### ARCH-4: Memory's `avg_quality` Doesn't Actually Average

[memory.py:85](file:///Users/arpitsharma/Library/CloudStorage/GoogleDrive-arpit.sharma.19.11.2002@gmail.com/My%20Drive/BrightVidya/Researher/zai-test/src/biopress/core/memory.py#L85) — The upsert **replaces** the `data` column on conflict, so `quality_score` is the **last** score, not an average. The key is labeled `avg_quality` which is misleading. Should accumulate and compute running average.

### ARCH-5: `ProgressTracker.STEPS` is Hardcoded

[progress.py:20-25](file:///Users/arpitsharma/Library/CloudStorage/GoogleDrive-arpit.sharma.19.11.2002@gmail.com/My%20Drive/BrightVidya/Researher/zai-test/src/biopress/core/progress.py#L20-L25) — Steps are hardcoded to 4 question-generation steps. This won't work for export, review, or API operations which have different step sequences.

### ARCH-6: `CostManager` Missing Provider Prices

`TOKEN_PRICES` only has `claude`, `grok`, `openai`, `ollama` — but README and adapters list **MiMo Claw** and **Kilo Claw** too. Unknown providers silently default to `$0.01/$0.03` (line 99), which may be incorrect.

---

## 🟢 Polish Items (5)

| ID | File | Issue |
|---|---|---|
| POL-1 | `models.py:80` | Typo: `AssertionReason` → should be `AssertionReason` or `AssertionReason` — decide on spelling and be consistent (NEET docs use "Assertion") |
| POL-2 | `models.py:93-98` | `BatchQuiz.items` is `list` (untyped) and `metrics` is `dict` (untyped) — loses Pydantic validation benefits |
| POL-3 | `models.py:14-18` | `Subject` enum uses PascalCase values (`Physics`) while `QuestionType` uses lowercase (`mcq`) — inconsistent casing |
| POL-4 | `config.py:28` | Language limited to `english`/`hindi` but README mentions bilingual support — needs Gujarati, Tamil, Bengali per prior conversations |
| POL-5 | `cost_manager.py:64` | Silent `pass` on `KeyError` during cost loading — corrupted data is swallowed silently |

---

## 📊 Module Scorecard

| Module | Score | Highlights | Concerns |
|---|---|---|---|
| `config.py` | 7/10 | Clean Pydantic settings, env prefix | Dead `BioPressConfig`, no singleton |
| `models.py` | 6/10 | Good Pydantic usage, all question types | Typo, untyped BatchQuiz, enum inconsistency |
| `cost_manager.py` | 7/10 | Budget enforcement, persistence | Pricing mismatch, per-call disk writes |
| `token_tracker.py` | 8/10 | Excellent zero-token tracking concept | Class-level state not thread-safe |
| `memory.py` | 7/10 | SQLite + pruning is solid | LIKE injection, fake "avg_quality" |
| `progress.py` | 8/10 | Rich integration, context manager | Hardcoded steps |

---

## Summary Verdict

The core layer is **well-structured and functional** for a v0.1. The main risk areas are:

1. **Concurrency** — will break under FastAPI async/multi-worker usage
2. **Cost tracking** — two conflicting pricing systems will confuse users
3. **Dead code** — `BioPressConfig` is unused

---

## ✅ Hardening Compliance Checklist

Status as of Phase 7.2 Hardening Sweep:

| ID | Task | Status | Detail |
|---|---|---|---|
| CRIT-1 | Dual Version Definition | ✅ COMPLETED | Centralized to `pyproject.toml`, retrieved via `importlib.metadata`. |
| CRIT-2 | Incomplete `__init__.py` | ✅ COMPLETED | All questions and services re-exported in `biopress.core`. |
| CRIT-3 | Thread-Safe Singletons | ✅ COMPLETED | `threading.Lock` added to `Memory`, `CostManager`, `TokenTracker`. |
| CRIT-4 | Cost Pricing Mismatch | ✅ COMPLETED | Logic unified; `TokenTracker` cost logic removed in favor of `CostManager`. |
| CRIT-5 | Topic Injection | ✅ COMPLETED | SQL wildcards escaped in topic queries. |
| ARCH-6 | MiMo/Kilo Claw Prices | ✅ COMPLETED | Pricing added to `CostManager.TOKEN_PRICES`. |
| ARCH-1 | Config Singleton | ✅ COMPLETED | `BioPressConfig` consolidated. |


---

## 🚀 Phase 8: Final Polish Scheduled

Remaining tasks from this phase have been scheduled for **Phase 8: Final Feature Completeness**.
See the master tracker in `tasks.md` or `plan.md` for sprint assignments.

