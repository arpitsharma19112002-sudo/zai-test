# BioPress Designer — Expert Code Review Plan

## Project Snapshot

| Metric | Value |
|---|---|
| **Source LOC** | ~8,033 lines (86 Python files) |
| **Test LOC** | ~5,069 lines (32 test files) |
| **Modules** | 8 (`core`, `generators`, `llm`, `validators`, `pdf`, `visual`, `cli`, `api`) |
| **Dependencies** | Typer, Pydantic, SymPy, ReportLab, NiceGUI, FastAPI, Uvicorn |
| **Question Types** | MCQ, Numerical, Case-Based, Assertion-Reason |
| **PDF Styles** | NEET 2-col, NCERT, Bilingual, OMR |
| **LLM Adapters** | MiMo Claw, Kilo Claw, Grok, Claude, Ollama |

---

## Why a Phased Review?

Each phase reads **~1,000–1,500 LOC** so we stay well within model context limits per conversation turn. This ensures deep, actionable feedback without truncation or rushing.

---

## Review Strategy: Audit First

**IMPORTANT:** We will complete all review phases before implementing any code changes. This prevents partial fixes from invalidating the subsequent stages of the review.

---

## Phase 0: Documentation Infrastructure ✅

**Goal:** Establish the persistent record of this review within the repository.

**Actions:**
- [x] Create `docs/expert_review/` directory.
- [x] Initialize `plan.md` (mirrored implementation plan).
- [x] Initialize `tasks.md` (mirrored task list).
- [x] Migrate existing Phase 1 findings to `phase_1_core.md`.

---

## Phase 1: Core Layer (Foundation) ✅

**Files (~7 files, ~1,100 LOC):**

| File | LOC | Priority |
|---|---|---|
| `core/config.py` | ~85 | 🔴 High |
| `core/models.py` | ~75 | 🔴 High |
| `core/cost_manager.py` | ~165 | 🟡 Medium |
| `core/token_tracker.py` | ~213 | 🟡 Medium |
| `core/memory.py` | ~168 | 🟡 Medium |
| `core/progress.py` | ~117 | 🟢 Low |
| `core/__init__.py` | ~15 | 🟢 Low |

**Review Criteria:**
- [x] Pydantic model design (v2 best practices, validators, serialization)
- [x] Config loading strategy (env vars, file-based, defaults)
- [x] Cost/token tracking accuracy and thread safety
- [x] Memory persistence strategy (file I/O vs DB)
- [x] Import hygiene and `__init__.py` re-exports

---

## Phase 2: Generators + Knowledge Base ✅

**Files (~16 files, ~1,800 LOC):**

| Sub-module | Files | LOC (approx) |
|---|---|---|
| `generators/questions/` | 6 (mcq, numerical, case_based, assertion_reason, batch, __init__) | ~950 |
| `generators/content/` | 4 (diagram, diagram_source, license_checker, __init__) | ~590 |
| `generators/mimic.py` | 1 | ~322 |
| `generators/translator.py` | 1 | ~111 |
| `kb/` | 6 (manager, loader, bootstrapper, rules, syllabus, __init__) | ~800 |

**Review Criteria:**
- [x] Prompt engineering quality (templates in JSON)
- [x] Batch generation logic (parallelism, error recovery)
- [x] Mimic engine design (style-matching accuracy)
- [x] KB bootstrapping and CRUD operations
- [x] Diagram source attribution and license checking
- [x] Translation pipeline correctness

---

## Phase 3: LLM Adapters + Validators ✅

**Files (~14 files, ~1,600 LOC):**

| Sub-module | Files | LOC (approx) |
|---|---|---|
| `llm/adapters/` | 6 (base, claude, grok, kiloclaw, mimoclaw, ollama) | ~600 |
| `llm/factory.py` + `pool.py` | 2 | ~120 |
| `validators/l1/` | 3 (math_validator, unit_validator, __init__) | ~400 |
| `validators/l2/` | 6 (validator, single_pass, context_checker, difficulty_checker, relevance_checker, types) | ~900 |

**Review Criteria:**
- [x] Adapter interface consistency (base ABC contract)
- [x] Error handling and retry logic per LLM provider
- [x] Factory/pool patterns (connection reuse, rate limiting)
- [x] L1 validation: SymPy math correctness, unit dimensional analysis
- [x] L2 validation: LLM-based context/difficulty/relevance checks
- [x] Single-pass optimization (token efficiency)

---

## Phase 4: PDF Export + Visual Editor ✅

**Files (~14 files, ~1,500 LOC):**

| Sub-module | Files | LOC (approx) |
|---|---|---|
| `pdf/styles/` | 5 (default, neet, ncert, bilingual, omr) | ~400 |
| `pdf/` core | 5 (builder, renderer, style_system, review_section, components/question) | ~700 |
| `visual/` | 6 (app, pages/editor, pages/review, components/element_list, components/pdf_viewer) | ~500 |

**Review Criteria:**
- [x] ReportLab usage patterns (memory, font handling, page layout)
- [x] Style system extensibility (adding new exam formats)
- [x] Bilingual rendering accuracy (Hindi/English side-by-side)
- [x] NiceGUI component architecture
- [x] Editor UX flow (review → edit → re-export)
- [x] PDF component reuse and DRY compliance

---

## Phase 5: CLI + API + Configuration ✅

**Files (~14 files, ~1,200 LOC):**

| Sub-module | Files | LOC (approx) |
|---|---|---|
| `cli/` | 9 (app, commands/generate, config, export, review, validate, kb, api) | ~700 |
| `api/` | 5 (main, routes/generate, routes/pdf, routes/validate, models/schemas) | ~500 |

**Review Criteria:**
- [x] Typer CLI design (help text, error handling, exit codes)
- [x] FastAPI route organization and OpenAPI schema
- [x] Request/response model consistency with core models
- [x] Input validation and error responses
- [x] Config command UX
- [x] API security considerations (auth, CORS, rate limiting)

---

## Phase 6: Tests + Docs + CI/CD + Final Report ✅

**Files (~32 test files, ~5069 LOC + docs):**

| Area | Files | LOC (approx) |
|---|---|---|
| Tests | 32 | ~5,069 |
| Docs | ~15+ markdown files | ~2,000 |
| CI/CD | GitHub templates + workflows | ~200 |

**Review Criteria:**
- [x] Test coverage per module (identify gaps)
- [x] Test quality (mocking strategy, fixtures, edge cases)
- [x] Performance test validity
- [x] Documentation completeness vs actual features
- [x] Roadmap alignment with codebase state
- [x] CI/CD pipeline completeness

**Deliverable:** Consolidated **Expert Review Report** with:
---

## Phase 7: Implementation Roadmap (Post-Audit)

> [!IMPORTANT]
> This roadmap transforms the audit findings into a sequenced execution plan. We follow a "Foundation First" approach, prioritizing core logic and security before premium UI/PDF features.

### Sprint 1: "Make It Real" ✅ (Foundation Fixes)
**Model Selection:** 🏆 **Opus 4.6 Thinking**  
**Rationale:** High reasoning load required to fix deep architectural silent failures and update ~350 tests to new error-handling patterns.

- [x] **LLM Adapter Refactor:** Fix silent fallbacks (P3-CRIT-1).
- [x] **Validator Logic:** Implement real `validate_content()` (P3-CRIT-2).
- [x] **API Corrections:** Fix validate route crashes (P5-CRIT-3).
- [x] **CI/CD Pipeline:** Create `.github/workflows/ci.yml` (P6-CRIT-1).
- [x] **Test Realignment:** Update tests validating old fallback behavior (P6-CRIT-4).

### Sprint 2: "Make It Safe" ✅ (Security & Integrity)
**Model Selection:** 🏆 **Gemini 3.1 Pro**  
**Rationale:** Surgical, targeted fixes across multiple files. High speed and precision for mechanical logic corrections.

- [x] **API Auth:** Require `BIOPRESS_API_KEY` or fail (P5-CRIT-2).
- [x] **CORS Tightening:** Restrict origins (P5-ARCH-4).
- [x] **Resource Cleanup:** Fix PDF temp file leakage (P5-CRIT-6).
- [x] **Global UTC:** Standardize all `datetime.now()` calls (P1).
- [x] **Math Bug:** Fix `DifficultyChecker` numeric overflow (P3).

### Sprint 3: "Make It Clean" ✅ (DRY & Refactoring)
**Model Selection:** 🏆 **Gemini 3.1 Pro**  
**Rationale:** Ideal for refactoring and centralizing logic. Excellent at extracting shared functions across modules.

- [x] **Deduplication:** Refactor `generate.py` to remove 215 duplicate LOC (P5-CRIT-1).
- [x] **Style Unification:** Create `PDFStyle` base class and unify schemas (P4-CRIT-1).
- [x] **Constant Centralization:** Move `VALID_EXAMS` etc. to `core/constants.py` (P5-ARCH-1).
- [x] **Dead Code Removal:** Delete Node.js scaffold files and fake API docs (P6-ARCH-1).
- [x] **Docs Rewrite:** Update `ROADMAP.md` for BioPress (P6-ARCH-3).

### Sprint 4: "Make It Premium" ✅ (Feature Completion)
**Model Selection:** 🏆 **Opus 4.6 Thinking**  
**Rationale:** Complex ReportLab implementation (Frames, PageTemplates) and advanced prompt engineering for real question generation.

- [x] **NEET Layout:** Implement real 2-column PDF rendering (P4-CRIT-1).
- [x] **Font Support:** Register Devanagari fonts for Hindi support (P4-POL-5).
- [x] **OMR Engine:** Implement OMR bubble rendering (P4).
- [x] **Visual Integration:** Connect Editor "Export" to `PDFBuilder` (P4-ARCH-5).
- [x] **AI Engine:** Implement actual LLM question generation logic (P2).
- [x] **Test Fixtures:** Implement `conftest.py` for shared fixtures (P6-ARCH-5).

---

> [!IMPORTANT]
> **Audit Status:** FINISHED  
> **Execution Status:** ✅ ALL 4 SPRINTS SHIPPED


### Phase 8: Final Feature Completeness

#### Sprint 5: True AI Generation (Phase 2 Fixes)
- [x] P2-CRIT-1: Refactor generators to support dual-mode generation (Static JSON templates AND Actual LLM generation) using a strategy pattern or fallback flag.
- [x] P2-CRIT-2: Extract shared generator logic into a `BaseGenerator` class to remove duplication.
- [x] P2-CRIT-3: Implement LLM-backed content translation in `translator.py`.

#### Sprint 6: Data & Diagram Integrity (Phase 2 & 3 Fixes)
- [x] P2-CRIT-4 & P2-CRIT-5: Fix Mimic generator topic mapping and prevent fake question injection.
- [x] P2-CRIT-7: Implement actual API calls (or safe fallbacks) for diagram sources.
- [x] P3-CRIT-5: Update Claude adapter to parse exact token usage instead of heuristics.
- [x] P2-ARCH-4: Add initial template data to KB layout directory.

#### Sprint 7: PDF & Visual Editor UX (Phase 4 Fixes)
- [ ] P4-ARCH-2: Integrate `matplotlib.mathtext` or `sympy` for LaTeX rendering in PDFs.
- [ ] P4-CRIT-2: Fix NiceGUI variable-before-definition closure bug in `editor.py`.
- [ ] P4-CRIT-4: Fix missing click handler attachment in `element_list.py` cards.
- [ ] P4-ARCH-3: Migrate NiceGUI global app state to proper per-session storage.

#### Sprint 8: CLI/API Polish (Phase 5 Fixes)
- [ ] P5-CRIT-4: Ensure CLI `--language` flags don't permanently side-effect the global `.json` config.
- [ ] P5-ARCH-1: Centralize duplicated validation lists (`VALID_EXAMS`, etc.) into `constants.py`.
- [ ] P5-ARCH-2: Replace fake `time.sleep` progress bar in `generate.py` with actual async tracking.
- [ ] P5-ARCH-3: Implement or remove the empty `validate` CLI command.

