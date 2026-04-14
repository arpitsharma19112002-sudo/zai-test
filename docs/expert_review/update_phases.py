import os

phase_8_tasks = """
### Phase 8: Final Feature Completeness

#### Sprint 5: True AI Generation (Phase 2 Fixes)
- [ ] P2-CRIT-1: Replace static JSON templates with actual LLM generation in all 4 generators (MCQ, Numerical, etc.).
- [ ] P2-CRIT-2: Extract shared generator logic into a `BaseGenerator` class to remove duplication.
- [ ] P2-CRIT-3: Implement LLM-backed content translation in `translator.py`.

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
"""

phase_8_docs_note = """
---

## 🚀 Phase 8: Final Polish Scheduled

Remaining tasks from this phase have been scheduled for **Phase 8: Final Feature Completeness**.
See the master tracker in `tasks.md` or `plan.md` for sprint assignments.
"""

base_dir = "/Users/arpitsharma/Library/CloudStorage/GoogleDrive-arpit.sharma.19.11.2002@gmail.com/My Drive/BrightVidya/Researher/zai-test/docs/expert_review"

def append_to_file(filename, content):
    path = os.path.join(base_dir, filename)
    if os.path.exists(path):
        with open(path, "a") as f:
            f.write("\n" + content + "\n")
            print(f"Appended to {filename}")
    else:
        print(f"File not found: {filename}")

append_to_file("tasks.md", phase_8_tasks)
append_to_file("plan.md", phase_8_tasks)

for i in range(1, 8):
    if i == 7:
        append_to_file(f"phase_7_implementation_fixes.md", phase_8_docs_note)
    else:
        # We don't have the exact filenames for all phases memorized perfectly, let's find them
        pass

for filename in os.listdir(base_dir):
    if filename.startswith("phase_") and filename.endswith(".md"):
        append_to_file(filename, phase_8_docs_note)

