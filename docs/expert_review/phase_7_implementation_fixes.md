# Phase 7: Implementation Roadmap & Fixes

> **Goal:** Sequenced execution of audit findings to reach v1.0.0.  
> **Strategy:** Foundation → Safety → Clean → Premium  
> **Total Sprints:** 4

---

## 🛠️ Sprint 1: "Make It Real" (Foundation)

**Goal:** Fix core architectural blockers and establish CI/CD.  
**Model Selection:** 🏆 **Opus 4.6 Thinking**  
**Rationale:** High reasoning load required to fix deep architectural silent failures and update ~350 tests.

### Tasks
- [x] **LLM Adapter Refactor:** 
    - Change `generate()` and `validate_content()` to raise `LLMConnectionError` instead of returning fallback strings.
    - Impact: Prevents silent garbage in production.
- [x] **Validator Logic:** 
    - Implement actual L2 scoring logic in `validate_content()`.
    - Fix the "always passes" bug in `biopress/validators/l2/validator.py`.
- [x] **API Corrections:** 
    - Fix the `/api/v1/validate` endpoint where `MathValidator.validate()` is called with wrong arguments.
- [x] **CI/CD Pipeline:** 
    - Create `.github/workflows/ci.yml`.
    - Include linting (ruff, mypy) and testing (pytest).
- [x] **Test Realignment:** 
    - Update `tests/test_llm.py` and others to `pytest.raises()` instead of checking for fallback strings.

---

## 🛡️ Sprint 2: "Make It Safe" (Security & Integrity)

**Goal:** Harden the API and fix data integrity bugs.  
**Model Selection:** 🏆 **Gemini 3.1 Pro**  
**Rationale:** Surgical, targeted fixes across multiple files. High speed and precision.

### Tasks
- [x] **API Auth:** 
    - Require `BIOPRESS_API_KEY` to be set; fail on startup/request if missing.
    - Fix the bypass logic in `api/routes/generate.py`.
- [x] **CORS Tightening:** 
    - Replace `allow_origins=["*"]` with a configurable list in `main.py`.
- [x] **Resource Cleanup:** 
    - Implement background unlinking for PDF temp files in `api/routes/pdf.py`.
- [x] **Global UTC:** 
    - Audit and replace all `datetime.now()` with `datetime.now(timezone.utc)`.
- [x] **Scoring Fix:** 
    - Fix the floating-point/None bug in `DifficultyChecker._calculate_score`.

---

## 🧹 Sprint 3: "Make It Clean" (Refactoring)

**Goal:** Eliminate technical debt and deduplicate code.  
**Model Selection:** 🏆 **Gemini 3.1 Pro**  
**Rationale:** Ideal for refactoring and centralizing logic.

### Tasks
- [x] **Deduplication:** 
    - Refactor `src/biopress/cli/commands/generate.py` to extract shared logic between subcommands.
    - Remove ~215 lines of redundant code.
- [x] **Style Unification:** 
    - Create a unified `PDFStyle` base class.
    - Refactor the 4 different `NamedTuple` definitions to use inheritance.
- [x] **Constant Centralization:** 
    - Move `VALID_EXAMS`, `VALID_SUBJECTS`, etc., to `biopress/core/constants.py`.
- [x] **Dead Code Removal:** 
    - Delete Node.js scaffold files (`package.json`, `jest.config.js`).
    - Remove fake `docs/reference/api.md` documentation.
- [x] **Roadmap Alignment:** 
    - Rewrite `ROADMAP.md` to reflect the actual BioPress Designer vision.

---

## ✨ Sprint 4: "Make It Premium" (Features)

**Goal:** Deliver advertised premium PDF and AI features.  
**Model Selection:** 🏆 **Opus 4.6 Thinking**  
**Rationale:** Complex library integrations (ReportLab) and advanced prompt engineering.

### Tasks
- [x] **NEET Layout:** 
    - Implement actual 2-column rendering in `pdf/renderer.py` using ReportLab `Frame` and `PageTemplate`.
- [x] **Font Support:** 
    - Implement Devanagari font registration to support Hindi language export.
- [x] **OMR Engine:** 
    - Implement OMR bubble rendering in `pdf/components/`.
- [x] **Visual Integration:** 
    - Connect the NiceGUI Editor's "Export PDF" button to the `PDFBuilder`.
- [x] **AI Engine:** 
    - Implement the actual generation prompts and parsing logic (transition from temp templates).
- [x] **Test Fixtures:** 
    - Centralize shared fixtures (like `temp_templates`) in `tests/conftest.py`.

---

## 📊 Summary of Criticality

| Sprint | 🔴 Critical Fixes | 🟡 Arch Improv | 🟢 Polish | Total |
|---|---|---|---|---|
| Sprint 1 | 5 | 2 | 3 | 10 |
| Sprint 2 | 5 | 3 | 2 | 10 |
| Sprint 3 | 2 | 5 | 5 | 12 |
| Sprint 4 | 2 | 4 | 3 | 9 |

---

> [!IMPORTANT]
> **Audit Status:** FINISHED  
> **Execution Status:** ✅ ALL 4 SPRINTS SHIPPED


---

## 🚀 Phase 8: Final Polish Scheduled

Remaining tasks from this phase have been scheduled for **Phase 8: Final Feature Completeness**.
See the master tracker in `tasks.md` or `plan.md` for sprint assignments.



---

## 🚀 Phase 8: Final Polish Scheduled

Remaining tasks from this phase have been scheduled for **Phase 8: Final Feature Completeness**.
See the master tracker in `tasks.md` or `plan.md` for sprint assignments.

