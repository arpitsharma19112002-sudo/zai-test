# BioPress Designer — Expert Review Progress

## Phase Tracker

- [x] Phase 0: Documentation Infrastructure
- [x] Phase 1: Core Layer (Foundation) - *Review Complete*
- [x] Phase 2: Generators + Knowledge Base - *Review Complete*
- [x] Phase 3: LLM Adapters + Validators - *Review Complete*
- [x] Phase 4: PDF Export + Visual Editor - *Review Complete*
- [x] Phase 5: CLI + API + Configuration - *Review Complete*
- [x] Phase 6: Tests + Docs + CI/CD + Final Report - *Review Complete*

## Implementation Phase

### Sprint 1: Foundation ✅ (Model: Opus 4.6 Thinking)
- [x] Fix LLM adapter fallbacks (raise exceptions)
- [x] Implement actual `validate_content()` logic
- [x] Fix `/api/v1/validate` method signature crash
- [x] Create `.github/workflows/ci.yml`
- [x] Update tests to expect exceptions instead of fallback strings
- [x] Fix `/docs` endpoint shadow (bonus)

### Sprint 2: Safety ✅ (Model: Gemini 3.1 Pro)
- [x] Fix API key auth (reject Null/None)
- [x] Fix wildcard CORS origins
- [x] Implement PDF temp file background cleanup
- [x] Migrate `datetime` calls to UTC aware
- [x] Fix `DifficultyChecker` scoring logic

### Sprint 3: Clean ✅ (Model: Gemini 3.1 Pro)
- [x] Deduplicate `generate.py` command body (215 LOC)
- [x] Create `PDFStyle` base class and refactor children
- [x] Centralize constants in `core/constants.py`
- [x] Remove Node.js scaffold files and fake API docs
- [x] Update `ROADMAP.md` vision and milestones

### Sprint 4: Premium ✅ (Model: Opus 4.6 Thinking)
- [x] Implement real 2-column NEET PDF layout
- [x] Register Hindi/Devanagari fonts in ReportLab
- [x] Add OMR bubble rendering to PDF components
- [x] Hook Visual Editor Export button to PDFBuilder
- [x] Integrate actual LLM question generation logic (P2)
- [x] Implement `conftest.py` for shared fixtures (P6-ARCH-5)

### Phase 7.2: Final Hardening Sweep ✅
- [x] **Core Hardening (Ph-1):**
    - [x] Unify Version source (pyproject.toml)
    - [x] Expand `core/__init__.py` re-exports
    - [x] Add `threading.Lock` to global singletons
    - [x] Fix Memory LIKE pattern & thread safety
    - [x] Move `_current_report` to instance-level in TokenTracker
- [x] **Generator Hygiene (Ph-2):**
    - [x] Update `generators/__init__.py` re-exports
- [x] **LLM/Validator Sanitization (Ph-3):**
    - [x] Unify `LLMConnectionError` and `BudgetExceededError` in `core/errors.py`
    - [x] Standardize `ValidationResult` and `L2Result` in `core/types.py`
    - [x] Migrate all L2 checkers to unified schema
- [x] **Final Documentation Sync:**
    - [x] Append checklists to Phase 1-6 files
    - [x] Mark Phase 7 audit targets as 100% compliant
    - [x] Generate final walkthrough and handover documentation


### Phase 8: Final Feature Completeness

#### Sprint 5: True AI Generation (Phase 2 Fixes)
- [x] P2-CRIT-1: Refactor generators to support dual-mode generation (Static JSON templates AND Actual LLM generation) using a strategy pattern or fallback flag.
- [x] P2-CRIT-2: Extract shared generator logic into a `BaseGenerator` class to remove duplication.
- [x] P2-CRIT-3: Implement LLM-backed content translation in `translator.py`.

#### Sprint 6: Data & Diagram Integrity (Phase 2 & 3 Fixes)
- [ ] P2-CRIT-4 & P2-CRIT-5: Fix Mimic generator topic mapping and prevent fake question injection.
- [ ] P2-CRIT-7: Implement actual API calls (or safe fallbacks) for diagram sources.
- [ ] P3-CRIT-5: Update Claude adapter to parse exact token usage instead of heuristics.
- [ ] P2-ARCH-4: Add initial template data to KB layout directory.

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

