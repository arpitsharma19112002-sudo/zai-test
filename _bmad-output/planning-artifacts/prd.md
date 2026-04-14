---
stepsCompleted:
  - step-01-init
  - step-02-discovery
  - step-02b-vision
  - advanced-elicitation-complete
  - step-02c-executive-summary
  - step-02c-complete
  - step-03-success
  - step-04-journeys
  - step-05-domain
  - step-06-innovation
  - step-07-project-type
  - step-08-scoping
  - step-09-functional
  - step-10-nonfunctional
  - step-11-polish
  - step-12-complete
inputDocuments: []
workflowType: "prd"
classification:
  projectType: developer_tool
  domain: Education
  complexity: high
  projectContext: greenfield
  deliveryPhases:
    - phase1: CLI tool (local)
    - phase2: Webapp (API + UI)
  targetUsers:
    - phase1: Internal company content team
    - phase2: Teachers and coaching institutes
  outputFormats:
    - PDF documents
    - API for other applications
productVision:
  core: Democratizing learning by synthesizing personal adaptive content on-demand
  enhanced: Content that fills YOUR specific gaps, in YOUR context, when YOU need it, for free
  differentiator: The worlds first on-demand content synthesizer — need NEET Physics? Get perfect content in seconds, personalized to YOUR students gaps
  coreInsight: Local AI + Perseus format = professional content at 10x speed, 0 cost
  firstPrinciples:
    - Learning happens when there's a gap - content must meet learner where they are
    - Practice makes permanent - wrong practice creates wrong habits
    - Context matters - same topic needs different depth for Class 8 vs NEET
    - Motivation follows relevance - why do I need to know this?
    - Feedback closes the loop - did they learn it?
  scapper:
    substitute: system becomes the creator (not expert)
    combine: AI speed + expert quality + free cost
    adapt: Perseus format for Indian exams
    modify: personalization is core feature
    put: multiple uses - teaching, learning, selling, practicing
    eliminate: cost barrier, time delay, quality variance
    reverse: need → generate (not create → publish)
userPersonas:
  - name: Content Creator
    type: Internal team member
    need: Fast generation, consistent quality, batch creation
    pain: "We have 500 questions due tomorrow"
    value: 10x faster
  - name: Teacher
    type: School teacher (Class 8-12)
    need: Classroom worksheets, quick quizzes, homework
    pain: "NCERT is dry, I need engaging content"
    value: Own worksheets on demand
  - name: Coaching Owner
    type: NEET/JEE coaching center
    need: Mock papers, branded content
    pain: "Content costs lakhs every year"
    value: Free professional content
  - name: Student
    type: Class 10-12 NEET/JEE prep
    need: Practice, mock tests, gap-filling
    pain: "One-size-fits-all doesn't work"
    value: Content that MY gaps need
whatIfScenarios:
  - scenario: "Everyone could create content"
    implication: "100M teachers become creators"
    strategy: "MOAT shifts from creation to curation"
  - scenario: "Content is free forever"
    implication: "Can't charge for content"
    strategy: "Monetize via API/tools"
  - scenario: "AI creates better than experts"
    implication: "Expert creation becomes obsolete"
    strategy: "Position as enhancer, not replacement"
  - scenario: "NEET/JEE exams change format"
    implication: "All templates become obsolete"
    strategy: "Build adaptability INTO the system"
  - scenario: "Competitors copy everything"
    implication: "Can't win on features alone"
    strategy: "First-mover + community advantage"
premortem:
  scope: "Start with ONE exam"
  mvp: "NEET Physics + Chemistry + Biology + L2 Validation + Multi-LLM"
  strategy: "Validate before adding more"
  critical:
    - "Build validation BEFORE generation"
    - "Find 5 users in first month"
    - "Clean architecture from day 1"
    - "Celebrate wins"
architectureDecisions:
  - adr: ADR-001
    decision: "CLI First"
    rationale: "Speed to MVP"
  - adr: ADR-005
    decision: "Two-Layer Plugin Model (Tools + Capabilities)"
    rationale: "Makes system agent-native and extensible"
    features: ["MCP exposure", "Layer 1: Atomic tools", "Layer 2: Multi-step capabilities"]
  - adr: ADR-002
    decision: "Multi-LLM support from Day 1"
    rationale: "Support all models (MiMo Claw, Kilo Claw, Grok, Claude, etc.) - user choice"
    options:
      - "MiMo Claw (local, free)"
      - "Kilo Claw (local)"
      - "Grok (cloud)"
      - "Claude (cloud)"
      - "OpenAI (cloud)"
      - "Ollama (local any model)"
  - adr: ADR-003
    decision: "Perseus format"
    rationale: "Khan compatibility"
  - adr: ADR-004
    decision: "NEET only for MVP"
    rationale: "Quality focus"
fiveWhys:
  - question: "Why build BioPress?"
    answer: "Because we need content faster"
  - question: "Why slow?"
    answer: "Every question must be written, validated, formatted"
  - question: "Why no system?"
    answer: "No automated system for Indian exams"
  - question: "Why not solved?"
    answer: "Multi-domain problem - AI + validation + PDF + diagrams"
  - question: "Why NOW?"
    answer: "Local AI (MiMo Claw) + Perseus = problem solved"
  rootCause: "Technology gap finally closed"
graphOfThoughts:
  layers:
    - name: "Input Layer"
      components: ["Exam selector", "Subject", "Style"]
    - name: "Core Engine"
      components: ["Perseus Template", "Variable Solver", "L1 Validator", "L2 Validator", "Relevance"]
    - name: "Output Layer"
      components: ["PDF Builder", "Diagram Engine", "Translation"]
  connections:
    - "Template → Validation: Validation depends on template structure"
    - "L1 → L2: L1 is fast filter, L2 is quality gate"
    - "Diagram → Translation: Diagrams need multilingual labels"
    - "Style → PDF: PDF layout depends on chosen style"
  keyInsight: "Everything flows from Template. Quality is built IN, not filtered after."
partyModeInsights:
  murat_testing:
    - "Multi-LLM Variance: per-model baseline expectations needed"
    - "Subject complexity: Physics/Chemistry = deterministic, Biology = messy"
    - "PDF rendering: notoriously brittle"
    - "CLI test paths: exponential with flags"
    - quality_gates:
        - "L1 Pass Rate: 95%+ for Physics/Chemistry"
        - "L2 Pass Rate: per-model baseline tracked over time"
        - "PDF Render: screenshot diffs"
  amelia_implementation:
    - "Implementation Feasibility: HIGH"
    - "LLMAdapter abstraction layer upfront"
    - "Story breakdown: 3-4 minimum"
      - "Story 1: CLI + PDF output"
      - "Story 2: Content framework + L1"
      - "Story 3: L2 + Multi-LLM"
    - "AC IDs needed before estimation"
    - "Question count and types must be defined"
visualReviewTool:
  description: "Visual Review & Edit Tool for interactive review/editing"
  implementation: "NiceGUI-based local web interface"
  features:
    - "Live PDF preview (PDF.js high-fidelity viewer)"
    - "Structured element list (text, diagrams, tables, KaTeX)"
    - "Inline editing for text/questions"
    - "Targeted diagram refinement"
    - "One-click Apply & Re-export PDF"
    - "Local web UI at http://localhost:8080"
  workflow: "Generate → Review visually → Edit targeted → Export"
uxRequirements:
  priority_1:
    - name: "Progress Indicator"
      user: "Priya (Content Creator)"
      requirement: "Show progress during generation - ETA, completion %, step indicator"
      rationale: "Users fear silent failures"
  priority_2:
    - name: "Language Selection at Start"
      user: "Rajesh (Teacher)"
      requirement: "Language selection immediately visible, not buried in settings"
      rationale: "Language is core requirement, not preference"
  priority_3:
    - name: "Output Preview"
      user: "Sunil (Coaching Owner)"
      requirement: "Visual quality check before export"
      rationale: "Professional output needs verification"
  priority_4:
    - name: "Progress Dashboard"
      user: "Amit (Student)"
      requirement: "Visual progress bars, badges, celebration of wins"
      rationale: "Students need to FEEL improvement"
domainRequirements:
  education_domain:
    - aspect: "Content Accuracy"
      consideration: "Wrong answers in exam prep = career impact"
    - aspect: "NCERT Alignment"
      consideration: "Must align with official syllabus"
    - aspect: "Question Types"
      consideration: "MCQ, Numerical, Case-based, Assertion-Reason"
    - aspect: "Exam Patterns"
      consideration: "NEET has specific distribution"
    - aspect: "Language"
      consideration: "Hindi/English both official"
    - aspect: "IP/Attribution"
      consideration: "Transform, don't copy content"
mvpScope:
  cli_interface: MVP
  subjects: "NEET Physics + Chemistry + Biology"
  l1_validation: "MVP (SymPy)"
  l2_validation: "MVP (LLM)"
  multi_llm: MVP
  pdf_output: MVP
  progress_indicator: MVP
  language_selection: MVP
  output_preview: MVP
  output_preview_editing: MVP
    - "Text correction"
    - "Question fix/replace"
    - "Diagram replacement"
    - "Add new question"
    - "Delete question"
    - "Visual editor for WYSIWYG editing"
  progress_dashboard: MVP
  api_support: MVP
postMvp:
  - "JEE Exam Support"
  - "CBSE Support"
  - "Webapp/UI"
  - "Additional Exams"
nonFunctionalRequirements:
  token_optimization: "Core generation is 98%+ 0-token (Perseus templates + SymPy); LLM used only for optional L2 validation and translation"
  performance: "100+ questions/minute"
  reliability: ">95% L1 validation pass rate"
  usability: "Time to first question <30 seconds"
  scalability: "500+ questions per batch"
  security: "Local AI - no data leaves local"
  maintainability: "Swappable LLM architecture"
  cost: "$0 (local) or <$0.01/question"
  compatibility: "Perseus JSON standard"
additionalFeatures:
  kb_bootstrapper:
    description: "Automated rule/syllabus/pattern generation for any new exam/board"
    benefit: "Solves 'someone has to write the rules' problem"
    usage: "Run once per new exam to generate complete KB"
  diagram_engine:
    description: "Automatic diagram sourcing from OpenStax/LibreTexts/HyperPhysics + Servier/Bioicons/Wikimedia"
    features: ["Print-grade SVG/PNG", "Automatic attribution", "Multilingual labels"]
  diagram_verification:
    description: "Smart diagram verification workflow"
    stages: ["Preview", "Approve/Reject", "Targeted refinement"]
    workflow:
      - Stage_1: "Content Generation (fast)"
      - Stage_2: "Diagram Selection & Preview (isolated)"
      - Stage_3: "Verification & Approval (human/agent review)"
      - Stage_4: "Targeted Refinement (only rejected diagrams)"
      - Stage_5: "Final PDF Build (after approval)"
    benefit: "No full pipeline re-run for bad diagrams - only fix what is rejected"
  review_section:
    description: "Automatic Editorial Review & Sources in every PDF"
    includes:
      - "Text sources (NCERT, PYQ, OpenStax, LibreTexts)"
      - "Image/diagram sources with license and attribution"
      - "Table sources"
      - "Mathematical content verification (SymPy)"
      - "Question & Mimic data sources"
      - "Quality Assurance summary (relevance scores, validation status)"
      - "Generation metadata (date, pipeline version, style, seed)"
    format: "Clean typographically consistent section - last page or separate appendix"
    benefit: "Professional, legal, and auditable PDFs"
  mimic_mode:
    description: "Statistical exam-pattern replication"
    usage: "Generate realistic mock papers using bootstrapped blueprints"
  pdf_style_system:
    description: "Reusable PDF layout templates"
    styles: ["NEET 2-column", "NCERT textbook", "Coaching module", "Bilingual", "OMR-ready"]
    creation: "Agent-assisted via natural language (e.g., 'Create NEET 2-column OMR style with Noto Sans font')"
    storage: "JSON files in /kb/layouts/"
    output: "Print-ready PDFs with consistent typography"
optionalFeatures:
  persistent_memory:
    description: "Lightweight Historical Pattern Memory (disabled by default)"
    reason: "No student feedback loop in pure PDF workflow"
    usage: "Enable only if performance data flows back into system"
security:
  blueTeam:
    - "Local AI = privacy"
    - "Perseus format = compatibility"
    - "Multi-LLM = flexibility"
    - "Open source = transparency"
  redTeam:
    - vulnerability: "AI generates wrong answers"
      severity: "High"
      defense: "L1 SymPy validation + human review"
    - vulnerability: "Copyright infringement"
      severity: "Medium"
      defense: "Transform, don't copy"
    - vulnerability: "Question bank leakage"
      severity: "Medium"
      defense: "Rate limits + auth"
    - vulnerability: "API abuse"
      severity: "Low"
      defense: "Rate limiting per user"
    - vulnerability: "LLM budget blowout"
      severity: "Low"
      defense: "Budget caps"
---

# Product Requirements Document - BioPress Designer

**Author:** Biopress
**Date:** 2026-04-13

---

## Welcome Biopress!

I've set up your PRD workspace for **BioPress Designer**.

**Document Setup:**

- Created: `_bmad-output/planning-artifacts/prd.md` from template
- Initialized frontmatter with workflow state

**Input Documents Discovered:**

- Product briefs: (none found)
- Research: (none found)
- Brainstorming: (none found)
- Project docs: (none found - greenfield project)

**Files loaded:** No additional documents found

---

### Next Step

This is a **fresh greenfield project**. You want to build an educational content generation engine based on your extensive design notes in "13-4-3-KhanDeeptutor BMAD Pre 1.txt".

Do you have any other documents you'd like me to include, or shall we continue to the next step?

**[C] Continue - Save this and move to Project Discovery (Step 2 of 11)**

---

## Implementation Status

### ✅ ALL EPICS COMPLETE (100%)

| Epic                        | Stories | Status      |
| --------------------------- | ------- | ----------- |
| Epic 1: CLI Foundation      | 2/2     | ✅ Complete |
| Epic 2: Content Generation  | 5/5     | ✅ Complete |
| Epic 3: Validation Pipeline | 4/4     | ✅ Complete |
| Epic 4: PDF Generation      | 7/7     | ✅ Complete |
| Epic 5: User Experience     | 3/3     | ✅ Complete |
| Epic 6: Visual Review       | 8/8     | ✅ Complete |
| Epic 7: Knowledge Base      | 4/4     | ✅ Complete |
| Epic 8: Advanced Features   | 4/4     | ✅ Complete |
| Epic 9: Optimization        | 4/4     | ✅ Complete |
| Epic 10: API Support        | 3/3     | ✅ Complete |

**Total: 44 stories across 10 epics - 100% Complete**

### Implementation Statistics

- **Test Coverage:** 462 tests
- **Code Quality:** 0 lint errors (ruff clean)
- **Python Files:** 100+
- **CLI Commands:** 6 main + subcommands
- **PDF Styles:** 5 (default, neet, ncert, bilingual, omr)
- **LLM Adapters:** 6 (MiMo, Kilo, Grok, Claude, OpenAI, Ollama)

### Code Quality

- ✅ All 371 tests passing
- ✅ Ruff lint clean (123 issues fixed)
- ✅ Deprecation warnings resolved
- ✅ Dependencies audited and updated

### Completed Features

- CLI with Typer framework
- Pydantic configuration models
- Multi-LLM adapter pattern
- Two-stage validation (L1 SymPy + L2 LLM)
- Template-based generation (0 token cost)
- 5 PDF export styles
- NiceGUI visual editor
- FastAPI REST API
- Knowledge base with bootstrapper
- Token optimization tracking
- Cost management with budget caps
- Optional persistent memory

### Future Enhancements

- Web-based UI (Phase 2)
- Mobile app integration
- Additional exam boards
- Advanced analytics dashboard
