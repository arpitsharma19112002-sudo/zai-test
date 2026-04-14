# BioPress Designer Roadmap

This document outlines the high-level vision, executed milestones, and planned features for the **BioPress Designer** project.

## Vision

To build a flawless, fully automated exam generation engine that creates production-grade, camera-ready PDF test papers (NEET, JEE, CBSE) powered by advanced LLM generation and mathematical validation.

---

## The 4-Sprint Implementation Plan

Following a comprehensive expert audit, the system is being hardened and upgraded through a 4-Sprint execution sequence:

### 🟢 Sprint 1: "Make It Real" (Foundation)
**Status:** Complete

**Focus:** Eliminate silent failures and establish CI/CD.
- LLM Adapters refactored to explicitly raise connection errors instead of returning fake fallback responses.
- Fixed core validation endpoints (L2 logic).
- Configured GitHub Actions CI/CD for automated testing and linting.

### 🟢 Sprint 2: "Make It Safe" (Security & Integrity)
**Status:** Complete

**Focus:** Harden the system for public/production drops.
- Enforced strict API Key (`BIOPRESS_API_KEY`) verification.
- Tightened CORS using explicitly configured origin whitelists.
- Fixed temporal memory leaks (PDFs now dynamically clean themselves via background tasks).
- Implemented global UTC-awareness.
- Resolved logic gaps in `DifficultyChecker` scoring systems.

### 🟢 Sprint 3: "Make It Clean" (Refactoring)
**Status:** Complete

**Focus:** Deduplicate operations and reduce technical debt.
- Reduced massive CLI generator routines into synchronized core commands (>200 lines eliminated).
- Centralized `PDFStyle` base configurations avoiding dataclass duplications.
- Moved `VALID_EXAMS` and `VALID_SUBJECTS` to a unified global `constants.py`.
- Purged legacy Node/JS scaffold files.

### 🔵 Sprint 4: "Make It Premium" (Features)
**Status:** Next Up

**Focus:** Deliver the heralded high-fidelity visual and structural PDF assets.
- Deploy NEET 2-column ReportLab layout matrix.
- Implement specialized Devanagari Font support for Hindi language exports.
- Integrate the automated OMR bubble sheet rendering systems.
- Connect the frontend visual editor "Export PDF" to the Python PDF Builder interface.
- Complete AI prompt integration with specific prompt chains for assertions and numerical physics.

---

## Future Horizons (v2+)

- **Translation Pipeline V2:** Expand beyond bilingual arrays into native localized LLM parsing.
- **RAG Document Intake:** Inject proprietary institute documents into generation logic.
- **Scale Out Vectors:** Offload generated data dynamically into Qdrant for similarity-mapped test creation.
