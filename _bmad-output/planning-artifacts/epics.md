---
stepsCompleted:
  [
    step-01-validate-prerequisites,
    step-02-design-epics,
    step-03-create-stories,
    step-04-final-validation,
  ]
inputDocuments:
  - "_bmad-output/planning-artifacts/prd.md"
  - "_bmad-output/planning-artifacts/architecture.md"
---

# BioPress Designer - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for BioPress Designer, decomposing the requirements from the PRD, UX Design if it exists, and Architecture requirements into implementable stories.

## Requirements Inventory

### Functional Requirements

**FR1:** CLI interface with commands: generate, validate, review, export, config, kb
**FR2:** Generate MCQ questions for NEET Physics
**FR3:** Generate MCQ questions for NEET Chemistry
**FR4:** Generate MCQ questions for NEET Biology
**FR5:** Generate Numerical questions
**FR6:** Generate Case-based questions
**FR7:** Generate Assertion-Reason questions
**FR8:** L1 Validation using SymPy (mathematical correctness, units, answers)
**FR9:** L2 Validation using LLM (relevance, difficulty, context)
**FR10:** Multi-LLM support (MiMo Claw, Kilo Claw, Grok, Claude, OpenAI, Ollama)
**FR11:** PDF output with NEET 2-column style
**FR12:** PDF output with NCERT textbook style
**FR13:** PDF output with Coaching module style
**FR14:** PDF output with Bilingual (Hindi/English) style
**FR15:** PDF output with OMR-ready style
**FR16:** Progress indicator during generation (ETA, completion %, step indicator)
**FR17:** Language selection at start (Hindi/English)
**FR18:** Output preview before export
**FR19:** Text correction in visual editor
**FR20:** Question fix/replace in visual editor
**FR21:** Diagram replacement in visual editor
**FR22:** Add new question in visual editor
**FR23:** Delete question in visual editor
**FR24:** Visual editor for WYSIWYG editing
**FR25:** Progress dashboard with visual progress bars and badges
**FR26:** API support for Phase 2 (FastAPI)
**FR27:** Knowledge base management (load, query, update)
**FR28:** KB Bootstrapper for new exams/boards
**FR29:** Smart Diagram Verification (preview → approve/reject → targeted refinement)
**FR30:** Automatic Review Section in every PDF (Editorial Review & Sources)
**FR31:** Diagram Engine (OpenStax, LibreTexts, HyperPhysics, Servier, Bioicons, Wikimedia)
**FR32:** PDF Style System (JSON layouts in /kb/layouts/, agent-assisted creation)
**FR33:** Mimic Mode for statistical exam-pattern replication
**FR34:** Single-pass Relevance Analysis (no rejection loops)
**FR35:** Persistent Memory (optional, disabled by default)

### NonFunctional Requirements

**NFR1:** Token optimization - 98%+ 0-token core generation (Perseus templates + SymPy)
**NFR2:** Performance - 100+ questions/minute
**NFR3:** Reliability - >95% L1 validation pass rate
**NFR4:** Usability - Time to first question <30 seconds
**NFR5:** Scalability - 500+ questions per batch
**NFR6:** Security - Local AI, no data leaves local
**NFR7:** Maintainability - Swappable LLM architecture
**NFR8:** Cost - $0 (local) or <$0.01/question
**NFR9:** Compatibility - Perseus JSON standard

### Additional Requirements

**AR1:** Starter Template: Typer + Pydantic (from Architecture)
**AR2:** Project structure: cli/, core/, validators/, llm/, generators/, pdf/, visual/, kb/, api/
**AR3:** LLM Adapter pattern for multi-provider support
**AR4:** Two-layer plugin model (Tools + Capabilities with MCP exposure)
**AR5:** SQLite for KB storage + JSON files
**AR6:** NiceGUI for visual review tool (localhost:8080)
**AR7:** WeasyPrint or ReportLab for PDF rendering

### UX Design Requirements

None found - this is a CLI-first project with optional visual review tool.

### FR Coverage Map

| FR        | Epic | Description                                          |
| --------- | ---- | ---------------------------------------------------- |
| FR1       | 1    | CLI interface                                        |
| FR2-FR4   | 2    | MCQ generation (Physics, Chemistry, Biology)         |
| FR5       | 2    | Numerical questions                                  |
| FR6       | 2    | Case-based questions                                 |
| FR7       | 2    | Assertion-Reason questions                           |
| FR8       | 3    | L1 Validation (SymPy)                                |
| FR9       | 3    | L2 Validation (LLM)                                  |
| FR10      | 3    | Multi-LLM support                                    |
| FR11-FR15 | 4    | PDF styles (NEET, NCERT, Coaching, Bilingual, OMR)   |
| FR16      | 5    | Progress indicator                                   |
| FR17      | 5    | Language selection                                   |
| FR18      | 5    | Output preview                                       |
| FR19-FR23 | 6    | Visual editor (text, question, diagram, add, delete) |
| FR24      | 6    | WYSIWYG editing                                      |
| FR25      | 6    | Progress dashboard                                   |
| FR26      | 10   | API support                                          |
| FR27      | 7    | KB management                                        |
| FR28      | 7    | KB Bootstrapper                                      |
| FR29      | 8    | Diagram verification workflow                        |
| FR30      | 4    | Automatic Review Section                             |
| FR31      | 8    | Diagram Engine                                       |
| FR32      | 4    | PDF Style System                                     |
| FR33      | 8    | Mimic Mode                                           |
| FR34      | 3, 9 | Single-pass Relevance Analysis                       |
| FR35      | 9    | Persistent Memory (optional)                         |

## Epic List

### Epic 1: CLI Foundation

**Goal:** Users can access BioPress via command line with help, version, and configuration commands
**FRs covered:** FR1

### Epic 2: Content Generation Engine

**Goal:** Users can generate questions (MCQ, Numerical, Case-based, Assertion-Reason) for NEET Physics, Chemistry, and Biology
**FRs covered:** FR2-FR7

### Epic 3: Quality Validation Pipeline

**Goal:** Users get mathematically correct, relevant, and contextually appropriate content through automated validation
**FRs covered:** FR8-FR10, FR34

### Epic 4: PDF Document Generation

**Goal:** Users can export professional PDFs in multiple styles with automatic review section
**FRs covered:** FR11-FR15, FR30, FR32

### Epic 5: User Experience & Progress

**Goal:** Users see real-time progress during generation and can select preferred language at start
**FRs covered:** FR16-FR18

### Epic 6: Visual Review & Editing

**Goal:** Users can preview output, edit text/questions, replace diagrams, add/delete questions in a visual WYSIWYG editor
**FRs covered:** FR19-FR25

### Epic 7: Knowledge Base Management

**Goal:** Users can manage knowledge base, load syllabus/rules, and bootstrap new exams/boards automatically
**FRs covered:** FR27-FR28

### Epic 8: Advanced Features

**Goal:** Users get smart diagram verification, print-grade diagrams from OER sources, and statistical mock paper generation
**FRs covered:** FR29, FR31, FR33

### Epic 9: Optimization & Optional Features

**Goal:** System achieves 98%+ token optimization and optionally tracks historical patterns
**FRs covered:** FR34-FR35

### Epic 10: API Support (Future Phase)

**Goal:** External applications can access BioPress functionality via REST API
**FRs covered:** FR26

---

## Epic 1: CLI Foundation

### Story 1.1: Basic CLI Setup with Typer

As a CLI user,
I want to run `biopress --help` and see all available commands,
So that I can understand what the tool can do.

**Acceptance Criteria:**

**Given** the biopress package is installed
**When** I run `biopress --help`
**Then** I see a help message with all available commands (generate, validate, review, export, config, kb)
**And** each command has a brief description
**And** `--version` flag shows current version

### Story 1.2: Configuration Management

As a CLI user,
I want to set and view configuration options (LLM provider, output directory, etc.),
So that I can customize BioPress behavior.

**Acceptance Criteria:**

**Given** no prior configuration exists
**When** I run `biopress config set provider ollama` and then `biopress config get provider`
**Then** the output shows `ollama`
**And** `biopress config list` shows all current settings
**And** configuration persists between sessions

---

## Epic 2: Content Generation Engine

### Story 2.1: MCQ Question Generation

As a content creator,
I want to generate MCQ questions for Physics, Chemistry, or Biology,
So that I can quickly create practice questions for my students.

**Acceptance Criteria:**

**Given** a valid exam (NEET) and subject (Physics/Chemistry/Biology) is specified
**When** I run `biopress generate --exam NEET --subject Physics --type mcq --count 10 --topic "Newton's Laws"`
**Then** I receive 10 MCQ questions in Perseus JSON format
**And** each question has: question text, 4 options (A,B,C,D), correct answer, explanation
**And** questions are relevant to the specified topic

### Story 2.2: Numerical Question Generation

As a content creator,
I want to generate numerical questions with calculations,
So that students can practice problem-solving skills.

**Acceptance Criteria:**

**Given** a valid exam and subject is specified
**When** I run `biopress generate --exam NEET --subject Physics --type numerical --count 5 --topic "Kinematics"`
**Then** I receive 5 numerical questions
**And** each question includes: problem statement, numerical answer, step-by-step solution
**And** numerical values are mathematically correct

### Story 2.3: Case-Based Question Generation

As a content creator,
I want to generate case-based questions with passages,
So that I can create application-level questions for NEET.

**Acceptance Criteria:**

**Given** a valid exam and subject is specified
**When** I run `biopress generate --exam NEET --subject Biology --type case-based --count 3`
**Then** I receive 3 case-based questions
**And** each includes: a passage (paragraph), 2-5 sub-questions based on the passage
**And** answers to all sub-questions are provided

### Story 2.4: Assertion-Reason Question Generation

As a content creator,
I want to generate assertion-reason type questions,
So that I can create questions testing conceptual understanding.

**Acceptance Criteria:**

**Given** a valid exam and subject is specified
**When** I run `biopress generate --exam NEET --subject Chemistry --type assertion-reason --count 5`
**Then** I receive 5 assertion-reason questions
**And** each has: assertion statement, reason statement, correct option (A/B/C/D as per NEET format)
**And** the logic connecting assertion and reason is correct

### Story 2.5: Batch Question Generation

As a content creator,
I want to generate multiple questions in a single command,
So that I can efficiently create large question banks.

**Acceptance Criteria:**

**Given** I specify multiple topics or a chapter
**When** I run `biopress generate --exam NEET --subject Physics --count 100`
**Then** I receive up to 100 questions
**And** questions are distributed across topics proportionally
**And** generation completes within reasonable time (<2 minutes)

---

## Epic 3: Quality Validation Pipeline

### Story 3.1: L1 Mathematical Validation with SymPy

As a content creator,
I want questions to be mathematically validated before output,
So that I can trust the numerical accuracy of generated content.

**Acceptance Criteria:**

**Given** a generated question with numerical answer
**When** the L1 validator processes it
**Then** mathematical expressions are evaluated using SymPy
**And** unit consistency is verified (e.g., velocity in m/s, not km/s without conversion)
**And** correct answers are verified to actually be correct
**And** questions passing validation are marked "L1_PASS"

### Story 3.2: L2 LLM-Based Quality Validation

As a content creator,
I want questions to be validated for relevance and difficulty by an LLM,
So that only high-quality questions are included in output.

**Acceptance Criteria:**

**Given** questions that pass L1 validation
**When** L2 validation runs
**Then** each question is checked for: relevance to the topic, appropriate difficulty level, correct context
**And** questions are scored for relevance (0-100)
**And** questions below threshold are flagged for review
**And** validation results include reasoning for each decision

### Story 3.3: Multi-LLM Adapter Support

As a technical user,
I want to switch between different LLM providers (MiMo Claw, Grok, Claude, etc.),
So that I can choose the best model for my needs and budget.

**Acceptance Criteria:**

**Given** multiple LLM adapters are configured
**When** I run `biopress config set provider grok` and generate content
**Then** the Grok adapter is used for L2 validation
**And** switching providers requires only a config change
**And** all adapters implement the same interface
**And** adapter failures are gracefully handled with fallback

### Story 3.4: Single-Pass Relevance Analysis

As a content creator,
I want relevance analysis to run in a single pass without rejection loops,
So that content generation is fast and efficient.

**Acceptance Criteria:**

**Given** bootstrapped per-exam rules are loaded
**When** content is validated
**Then** relevance is checked in one pass through the content
**And** no iterative rejection loops occur
**And** all questions are either accepted or rejected with clear reasons
**And** the process is 10x faster than multi-iteration approaches

---

## Epic 4: PDF Document Generation

### Story 4.1: Basic PDF Generation

As a content creator,
I want to export generated questions as a PDF,
So that I can print and distribute them to students.

**Acceptance Criteria:**

**Given** generated questions in Perseus JSON format
**When** I run `biopress export --input questions.json --output output.pdf`
**Then** a valid PDF file is created
**And** the PDF contains all questions with proper formatting
**And** the PDF is readable and printable

### Story 4.2: NEET 2-Column PDF Style

As a content creator,
I want PDFs formatted in NEET 2-column style,
So that the output matches the actual NEET exam format.

**Acceptance Criteria:**

**Given** generated questions
**When** I run `biopress export --style neet-2column --output mock-test.pdf`
**Then** the PDF has two columns of questions
**And** question numbers are in NEET format (1-90)
**And** OMR-style answer bubbles are included
**And** header shows exam name and paper details

### Story 4.3: NCERT Textbook Style PDF

As a teacher,
I want PDFs in NCERT textbook format,
So that students can use them as chapter-wise worksheets.

**Acceptance Criteria:**

**Given** generated questions for a specific chapter
**When** I run `biopress export --style ncert --output chapter-worksheet.pdf`
**Then** the PDF follows NCERT typography and layout
**And** each topic has heading and questions grouped under it
**And** page numbers and chapter title are included
**And** a brief chapter summary is at the top

### Story 4.4: Bilingual PDF Generation

As a content creator,
I want PDFs with both Hindi and English text,
So that students can practice in their preferred language.

**Acceptance Criteria:**

**Given** generated questions with Hindi translations available
**When** I run `biopress export --style bilingual --output bilingual.pdf`
**Then** the PDF contains both Hindi and English versions
**And** questions are side-by-side or sequential based on config
**And** fonts support Devanagari script correctly
**And** technical terms are consistently translated

### Story 4.5: OMR-Ready PDF Generation

As a coaching owner,
I want OMR-ready answer sheets,
So that I can conduct automated tests with scanning.

**Acceptance Criteria:**

**Given** generated questions
**When** I run `biopress export --style omr-ready --output test-paper.pdf`
**Then** the PDF has clearly marked answer circles
**And** question IDs align with OMR bubble positions
**And** there's a separate answer key page
**And** timing instructions are printed at the top

### Story 4.6: Automatic Review Section

As a content creator,
I want every PDF to include a review section with sources,
So that the content is professional and legally compliant.

**Acceptance Criteria:**

**Given** any PDF is generated
**When** the PDF is complete
**Then** an Editorial Review & Sources section is appended
**And** it lists: text sources (NCERT, PYQ, etc.), diagram sources with attribution, quality scores, generation metadata
**And** the section is typographically consistent with the rest of the document

### Story 4.7: PDF Style System

As a content creator,
I want to create custom PDF styles using natural language,
So that I can quickly generate new layouts.

**Acceptance Criteria:**

**Given** I want to create a custom style
**When** I run `biopress config create-style "NEET 2-column OMR style with Noto Sans font"`
**Then** a JSON layout file is created in /kb/layouts/
**And** the style is available for future exports
**And** styles are stored as reusable JSON files

---

## Epic 5: User Experience & Progress

### Story 5.1: Progress Indicator During Generation

As a content creator,
I want to see progress during question generation,
So that I know the system is working and can estimate completion time.

**Acceptance Criteria:**

**Given** I run a generate command with 50 questions
**When** generation is in progress
**Then** I see a progress bar or percentage
**And** I see which step is running (Template loading, LLM calling, Validation, PDF building)
**And** ETA is shown after 5+ seconds of processing
**And** completion percentage updates in real-time

### Story 5.2: Language Selection at Start

As a teacher,
I want to select my preferred language immediately,
So that all output is in my chosen language without extra commands.

**Acceptance Criteria:**

**Given** the CLI is invoked
**When** I run `biopress generate --language english` or `--language hindi`
**Then** all generated content is in the selected language
**And** the language selection is remembered for subsequent commands
**And** `biopress config get language` shows the current setting
**And** both Hindi and English are fully supported

### Story 5.3: Output Preview Before Export

As a content creator,
I want to preview generated content before exporting to PDF,
So that I can verify quality and make adjustments.

**Acceptance Criteria:**

**Given** questions are generated
**When** I run `biopress review --preview`
**Then** a text summary of generated content is displayed
**And** it shows: question count, topic coverage, validation status
**And** I can see sample questions before committing to PDF export

---

## Epic 6: Visual Review & Editing

### Story 6.1: Visual Review Tool Launch

As a content creator,
I want to launch a visual review interface,
So that I can interact with my generated content.

**Acceptance Criteria:**

**Given** I have generated content
**When** I run `biopress review`
**Then** a local web interface opens at http://localhost:8080
**And** I see the generated content in a visual format
**And** the interface is accessible in a web browser
**And** the tool works without internet connection (local)

### Story 6.2: PDF Viewer in Visual Tool

As a content creator,
I want to view the PDF in the visual tool,
So that I can see exactly what the final output looks like.

**Acceptance Criteria:**

**Given** content is loaded in the visual tool
**When** I navigate to the preview tab
**Then** I can view the PDF with high fidelity
**And** I can zoom in/out and navigate pages
**And** all formatting is preserved (columns, fonts, images)

### Story 6.3: Text Correction in Editor

As a content creator,
I want to fix typos and edit question text in the visual editor,
So that I can correct errors before export.

**Acceptance Criteria:**

**Given** a question is displayed in the editor
**When** I click on the question text and make edits
**Then** the changes are saved immediately
**And** the updated text appears in the preview
**And** I can undo/redo changes

### Story 6.4: Question Fix/Replace

As a content creator,
I want to replace a question that doesn't meet my standards,
So that I can swap it with a better one.

**Acceptance Criteria:**

**Given** a question is selected in the editor
**When** I click "Replace Question"
**Then** I can regenerate just that question
**And** the new question replaces the old one
**And** the rest of the content remains unchanged

### Story 6.5: Diagram Replacement

As a content creator,
I want to replace a diagram in a question,
So that I can use a better visual for my students.

**Acceptance Criteria:**

**Given** a question with a diagram
**When** I click on the diagram and select "Replace"
**Then** I can search for alternative diagrams
**And** the selected diagram replaces the old one
**And** attribution is automatically updated

### Story 6.6: Add New Question

As a content creator,
I want to add new questions to the generated set,
So that I can customize the output to my needs.

**Acceptance Criteria:**

**Given** content is loaded in the editor
**When** I click "Add Question" and specify topic/type
**Then** a new question is generated and added
**And** the question appears in the correct position
**And** numbering is automatically updated

### Story 6.7: Delete Question

As a content creator,
I want to remove questions that don't meet my needs,
So that I can curate the final output.

**Acceptance Criteria:**

**Given** a question is selected
**When** I click "Delete" and confirm
**Then** the question is removed
**And** remaining questions are renumbered
**And** the change is reflected in preview and PDF

### Story 6.8: Progress Dashboard

As a content creator,
I want to see visual progress indicators and badges,
So that I feel motivated and can track my work.

**Acceptance Criteria:**

**Given** I'm working in the visual tool
**When** I complete actions (generate, edit, export)
**Then** progress bars update
**And** achievement badges are shown for milestones
**And** the dashboard shows statistics (questions created, time spent)

---

## Epic 7: Knowledge Base Management

### Story 7.1: Knowledge Base Initialization

As a content creator,
I want to load the knowledge base for NEET exams,
So that the system has the necessary syllabus and rules.

**Acceptance Criteria:**

**Given** the KB directory contains NEET syllabus files
**When** I run `biopress kb load --exam NEET`
**Then** syllabus, question patterns, and rules are loaded
**And** I can query the KB to verify what's loaded
**And** loading status is displayed

### Story 7.2: KB Query and Search

As a content creator,
I want to search the knowledge base for topics and rules,
So that I can understand what's available.

**Acceptance Criteria:**

**Given** KB is loaded
**When** I run `biopress kb search "Newton's Laws"`
**Then** I see all matching topics, rules, and associated content
**And** results include topic hierarchy
**And** I can see which questions are associated with each topic

### Story 7.3: KB Bootstrapper for New Exams

As a technical user,
I want to bootstrap a knowledge base for a new exam (e.g., JEE),
So that I can quickly add new exam support.

**Acceptance Criteria:**

**Given** I have syllabus documents for a new exam
**When** I run `biopress kb bootstrap --exam JEE --syllabus jee-syllabus.pdf`
**Then** the system analyzes the syllabus
**And** generates KB entries for topics, rules, and patterns
**And** the new exam is available for generation
**And** the process is automated without manual rule-writing

### Story 7.4: KB Update and Sync

As a content creator,
I want to update knowledge base rules,
So that the system reflects the latest exam patterns.

**Acceptance Criteria:**

**Given** KB is already initialized
**When** I run `biopress kb update --rules new-rules.json`
**Then** the rules are updated
**And** existing content is still valid
**And** new generation uses updated rules

---

## Epic 8: Advanced Features

### Story 8.1: Smart Diagram Verification Workflow

As a content creator,
I want to preview diagrams, approve/reject them, and get targeted refinement,
So that I don't have to re-run the entire pipeline for bad diagrams.

**Acceptance Criteria:**

**Given** content is generated with diagrams
**When** I run the verification workflow
**Then** Stage 1: Content generates (fast)
**And** Stage 2: Diagrams are isolated for preview
**And** Stage 3: I can approve or reject each diagram
**And** Stage 4: Only rejected diagrams are re-processed (targeted refinement)
**And** Stage 5: Final PDF builds only after all diagrams approved

### Story 8.2: Diagram Engine - OER Sources

As a content creator,
I want diagrams sourced from free educational sources (OpenStax, Servier, etc.),
So that I have professional visuals without copyright issues.

**Acceptance Criteria:**

**Given** a diagram is needed for a question
**When** the diagram engine runs
**Then** it searches OpenStax, LibreTexts, HyperPhysics for Physics/Chemistry
**And** it searches Servier, Bioicons, Wikimedia for Biology
**And** diagrams are print-grade SVG/PNG
**And** attribution is automatically included
**And** multilingual labels are supported (Hindi/English)

### Story 8.3: Mimic Mode - Statistical Mock Papers

As a coaching owner,
I want to generate realistic mock papers that match exam patterns,
So that my students get authentic test experience.

**Acceptance Criteria:**

**Given** I want to create a mock paper
**When** I run `biopress generate --mode mimic --exam NEET --count 90`
**Then** the system uses bootstrapped exam blueprints
**And** it replicates the difficulty distribution of real NEET
**And** topic weightage matches actual exam patterns
**And** the result is statistically valid mock test

### Story 8.4: Diagram License Compliance

As a content creator,
I want diagrams to have proper licenses,
So that I can use them legally in my materials.

**Acceptance Criteria:**

**Given** diagrams from various OER sources
**When** a diagram is selected
**Then** its license (CC-BY, etc.) is verified
**And** proper attribution is recorded
**And** incompatible licenses are flagged
**And** compliance report is included in PDF review section

---

## Epic 9: Optimization & Optional Features

### Story 9.1: Token Optimization

As a cost-conscious user,
I want most generation to use 0 tokens (Perseus templates + SymPy),
So that I can generate content at minimal cost.

**Acceptance Criteria:**

**Given** a question is generated
**When** I analyze token usage
**Then** core generation (template + variable solving) uses 0 tokens
**And** SymPy handles all mathematical computation
**And** LLM is used only for: optional L2 validation, translation, new content types
**And** overall token usage is 98%+ 0-token for typical generation

### Story 9.2: Cost Management

As a cost-conscious user,
I want to set budget caps for LLM usage,
So that I don't overspend on generation.

**Acceptance Criteria:**

**Given** I'm using cloud LLM providers
**When** I set `biopress config set budget 1.00`
**Then** generation stops when budget is reached
**And** I can see token usage and cost reports
**And** budget can be reset for new sessions

### Story 9.3: Persistent Memory (Optional)

As a user who wants improvement over time,
I want the system to optionally track patterns,
So that future generations improve based on past feedback.

**Acceptance Criteria:**

**Given** persistent memory is enabled in config
**When** I use the system over time
**Then** it tracks generation patterns
**And** it can optionally learn from corrections made in visual editor
**And** by default, memory is disabled (no student feedback loop)
**And** memory can be enabled via `biopress config set memory enabled`

### Story 9.4: Performance Optimization

As a content creator,
I want fast generation even for large batches,
So that I can be productive.

**Acceptance Criteria:**

**Given** I generate 500 questions
**When** the generation runs
**Then** I achieve 100+ questions/minute
**And** first question appears in <30 seconds
**And** L1 validation pass rate is >95%
**And** batch processing handles 500+ questions efficiently

---

## Epic 10: API Support (Future Phase)

### Story 10.1: FastAPI Setup

As a developer,
I want BioPress to expose a REST API,
So that I can integrate it into other applications.

**Acceptance Criteria:**

**Given** the biopress package is installed
**When** I run `biopress api start`
**Then** a FastAPI server starts on port 8000
**And** I can access `/docs` for Swagger UI
**And** basic health check endpoint returns status

### Story 10.2: Generate API Endpoint

As a developer,
I want to generate content via API,
So that I can automate content creation.

**Acceptance Criteria:**

**Given** API is running
**When** I send POST to `/api/generate` with exam, subject, type, count
**Then** I receive generated questions in JSON
**And** the response follows Perseus JSON format
**And** authentication is required (API key)

### Story 10.3: PDF Export API

As a developer,
I want to export PDFs via API,
So that I can integrate PDF generation into my workflow.

**Acceptance Criteria:**

**Given** API is running with generated content
**When** I send POST to `/api/export` with content and style
**Then** I receive a PDF file download
**And** the PDF follows the requested style
**And** rate limiting is applied per user
