# Phase 5: CLI + API + Configuration — Expert Review Findings

> **Files Reviewed:** ~16 files, ~1,700 LOC  
> **Overall Module Health:** ⭐ 6.5 / 10

> [!NOTE]
> The CLI is the most feature-complete layer of the project — 7 well-organized Typer subcommands with Rich progress bars, the KB command has full CRUD, and the API has proper Pydantic schemas. However, the `generate.py` command has a massive code duplication (entire function body copy-pasted), the API has a critical security flaw, and the validate route will crash at runtime.

---

## 🔴 Critical Issues (6)

### CRIT-1: `generate.py` Has Entire Command Body Duplicated

**File:** `cli/commands/generate.py`

The file is **431 lines** — nearly the entire thing is two copies of the same logic:

| Method | Lines | Purpose |
|---|---|---|
| `generate_main()` | 121-296 | The `generate_main` subcommand |
| `generate_default()` | 299-431 | The `@command.callback` default handler |

These are **identical** — same validation, same progress bar, same `_generate_questions()` call, same error handling. The only difference: `generate_default` doesn't call `TokenTracker.finalize()`.

> [!CAUTION]
> **215 lines of exact copy-paste.** If you fix a bug in one, you must remember to fix it in the other. This is the largest DRY violation in the entire codebase.

**Fix:** Make `generate_default()` call `generate_main()` directly (or use a shared `_execute_generate()` function).

---

### CRIT-2: API Key Auth Can Be Bypassed

**File:** `api/routes/generate.py:27-34`

```python
async def verify_api_key(key: str = Security(api_key_header)):
    if key is None:
        raise HTTPException(status_code=401, detail="API key missing")
    expected_key = os.getenv("BIOPRESS_API_KEY")
    if expected_key and key != expected_key:  # ← Problem here!
        raise HTTPException(status_code=403, detail="Invalid API key")
    return key
```

If `BIOPRESS_API_KEY` env var is **not set**, then `expected_key` is `None`, the `if expected_key and ...` condition is `False`, and **any API key is accepted** — including garbage strings. This means:

- Development: No auth (intended? undocumented).
- Production: If you forget to set the env var, auth is silently disabled.

> [!CAUTION]
> **Security issue.** An attacker can call the generate endpoint with any `X-API-Key` value and it will succeed. Only the `/generate` route is protected — `/validate` and `/pdf` have **no auth at all**.

**Fix:** Either require `BIOPRESS_API_KEY` to be set (fail on startup if missing) or apply auth middleware to *all* routes consistently.

---

### CRIT-3: Validate API Route Will Crash — Wrong Method Signature

**File:** `api/routes/validate.py:30`

```python
q_issues = math_validator.validate(question.question)
```

`MathValidator.validate()` expects a `dict[str, Any]` (with keys like `expression`, `expected_answer`, `unit`, `quantity`), but it receives `question.question` — a **plain string** (the question text).

```python
# MathValidator.validate() expects:
{"expression": "2+3", "expected_answer": 5}
# But receives:
"What is the force applied on a 5kg mass?"
```

The method will hit `question.get("expected_answer")` on a string, which raises `AttributeError: 'str' object has no attribute 'get'`.

Similarly, `unit_validator.validate(question.question)` on line 42 calls a method that **doesn't exist** — `UnitValidator` has `check_unit_consistency()` and `convert_units()`, but no `validate()` method.

> [!CAUTION]
> The `/api/v1/validate` endpoint will always crash with `AttributeError`. It is completely non-functional.

**Fix:** Pass `question.model_dump()` instead of `question.question`, and use the correct method names.

---

### CRIT-4: `generate_main` Side-Effects Config on Every Run

**File:** `cli/commands/generate.py:203-205`

```python
if language:
    config_mgr = get_config_manager()
    config_mgr.set("language", language)
```

Every time you run `biopress generate --language hindi`, it **permanently** changes the saved configuration. The next run *without* `--language` will default to Hindi because `_resolve_language()` reads from saved config. This is unexpected — CLI flags should be per-invocation, not permanent side effects.

**Fix:** Don't persist `language` to config unless the user explicitly runs `biopress config set language hindi`.

---

### CRIT-5: `/docs` Endpoint Shadows FastAPI's Built-in Swagger UI

**File:** `api/main.py:37-39`

```python
@app.get("/docs")
def docs():
    return {"swagger": "available at /docs"}
```

FastAPI automatically generates Swagger UI at `/docs`. This custom endpoint **overwrites** it with a JSON response `{"swagger": "available at /docs"}`. Users navigating to `/docs` see JSON instead of the interactive Swagger UI.

**Fix:** Remove this endpoint entirely. FastAPI's built-in `/docs` works out of the box.

---

### CRIT-6: PDF API Temp Files Are Never Cleaned Up

**Files:** `api/routes/pdf.py:73-74`, `api/routes/pdf.py:144-145`

```python
with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
    output_path = tmp.name
```

Both `export_pdf` and `generate_pdf` create temp files with `delete=False` but never clean them up. Every API call creates a new file in `/tmp/` that persists forever. Under load, this will fill the disk.

The `generate_pdf` endpoint returns a `PDFResponse` with `file_path=output_path` (the temp path) — but the client can't use this path since it's a server-local file path, not a download URL.

**Fix:** Use `background=BackgroundTask(os.unlink, output_path)` in `FileResponse`, or stream the PDF directly.

---

## 🟡 Architecture Improvements (5)

### ARCH-1: Validation Lists Duplicated Across CLI and API

`VALID_EXAMS`, `VALID_SUBJECTS`, `VALID_TYPES`, `VALID_LANGUAGES` are defined **three times**:
1. `cli/commands/generate.py:32-36`
2. `api/routes/generate.py:21-24`
3. `api/models/schemas.py` (as Field descriptions only, no actual validation)

These lists will inevitably drift. Should be defined once in `core/constants.py` and imported everywhere.

### ARCH-2: `generate.py` Fake Progress Bar

`cli/commands/generate.py:252-266` — The progress bar includes `time.sleep(0.1)` and a fake loop (`for i in range(0, 100, 10): time.sleep(0.05)`) to simulate progress. The actual generation happens in one synchronous call. The progress animation is cosmetic theater.

This wastes ~0.5-1 second per run. For batch operations, this adds up.

### ARCH-3: `cli/commands/validate.py` is Empty

The entire file is 15 lines that display `--help`. No actual validation command is implemented. Users see:
```
biopress validate
```
And get a help page with no subcommands. This is confusing — either implement it or remove it from the registered commands.

### ARCH-4: CORS Allows All Origins in Production

`api/main.py:16` — `allow_origins=["*"]` is a development convenience that should not ship to production. Combined with the broken auth (CRIT-2), anyone can call the API from any domain.

### ARCH-5: `review.py` Has 3 Ways to Do the Same Thing

The review command has `launch`, `run` (alias for launch), `preview` (standalone), and `review_main` (callback that delegates to launch). Four entry points for two actions (preview and launch). This confuses `--help` output.

---

## 🟢 Polish Items (6)

| ID | File | Issue |
|---|---|---|
| POL-1 | `generate.py:5` | Uses Python `type` as parameter name — shadows builtin |
| POL-2 | `config.py:14` | `VALID_PROVIDERS` includes `"openai"` but no OpenAI adapter exists |
| POL-3 | `config.py:14` | `VALID_PROVIDERS` missing `"mimoclaw"` and `"kiloclaw"` which are actual adapters |
| POL-4 | `api.py:14-15` | CLI `-h` flag conflicts with Typer's built-in `--help` — use `--host` only |
| POL-5 | `schemas.py:19` | `QuestionModel.options` is `List[str]` but `MCQItem.options` is `MCQOptions` (dict-like) — format mismatch |
| POL-6 | `kb.py:149` | Subject name derived from filename: `"neet_physics.txt"` → `"Physics"` but `"neet_bio.txt"` → `"Bio"` (truncated) |

---

## 📊 Module Scorecard

| Module | Score | Highlights | Concerns |
|---|---|---|---|
| `cli/app.py` | 8/10 | Clean Typer setup, version flag | `invoke_without_command=True` |
| `cli/commands/generate.py` | 4/10 | Rich progress, full options | 215 LOC copy-pasted, fake progress |
| `cli/commands/config.py` | 8/10 | Thorough validation per key | Provider list outdated |
| `cli/commands/export.py` | 8/10 | Clean export + create-style | Good error handling |
| `cli/commands/review.py` | 6/10 | Preview summary is nice | 4 entry points for 2 actions |
| `cli/commands/validate.py` | 2/10 | — | Completely empty |
| `cli/commands/kb.py` | 9/10 | Full CRUD, search, bootstrap, sync | Best CLI command by far |
| `cli/commands/api.py` | 7/10 | Uvicorn integration, docs helper | `-h` flag conflict |
| `api/main.py` | 5/10 | FastAPI + CORS + versioned routes | `/docs` shadowed, wildcard CORS |
| `api/models/schemas.py` | 7/10 | Clean Pydantic v2 models | `options` format mismatch |
| `api/routes/generate.py` | 6/10 | Auth, validation, proper responses | Auth bypassable, no rate limit |
| `api/routes/validate.py` | 2/10 | Structure exists | Will crash — wrong arguments |
| `api/routes/pdf.py` | 7/10 | File upload + JSON, rate limiting | Temp file leak, dual endpoint overlap |

---

## Summary Verdict

The CLI is the **most feature-complete** surface of the project. `kb.py` alone (213 lines) has more working functionality than some entire modules. The API is well-structured but has critical bugs that make 2 of 3 endpoints non-functional.

| Feature | CLI | API |
|---|---|---|
| Generate questions | ✅ Works | ✅ Works (with auth bypass) |
| Validate questions | ❌ Empty command | ❌ Crashes at runtime |
| Export PDF | ✅ Works | ⚠️ Works but leaks temp files |
| Config management | ✅ Full CRUD | N/A |
| KB management | ✅ Full CRUD + search | N/A |
| Auth/Security | N/A | ❌ Bypassable, wildcard CORS |
| Progress UX | ⚠️ Fake animation | N/A |

> [!IMPORTANT]
> **Founder-level assessment:** The CLI is your best distribution channel right now — `kb.py` is production-quality and `export.py` works cleanly. The API needs immediate fixes before any external integration: the validate endpoint crashes, auth is bypassable, and Swagger UI is broken. The 215-line copy-paste in `generate.py` is the single largest technical debt item in the project.

---

## ✅ Hardening Compliance Checklist

Status as of Phase 7.2 Hardening Sweep:

| ID | Task | Status | Detail |
|---|---|---|---|
| CRIT-1 | CLI Code Duplication | ⏳ PENDING | 215-line copy-paste in `generate.py` remains. |
| CRIT-2 | API Auth Bypass | ⏳ PENDING | Auth logic still depends on optional env var. |
| CRIT-3 | Validate API Crash | ⏳ PENDING | Argument mismatch in `validate.py` remains. |
| CRIT-5 | `/docs` Shadowing | ⏳ PENDING | Built-in Swagger UI still overwritten. |


---

## 🚀 Phase 8: Final Polish Scheduled

Remaining tasks from this phase have been scheduled for **Phase 8: Final Feature Completeness**.
See the master tracker in `tasks.md` or `plan.md` for sprint assignments.

