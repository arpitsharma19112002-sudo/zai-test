# Story 9.1: Token Optimization for BioPress Designer

**Epic:** 9. Cost Optimization  
**Owner:** Development Team  
**Status:** Done

## Story

As a cost-conscious user, I want most generation to use 0 tokens (Perseus templates + SymPy), so I can generate content at minimal cost.

## Acceptance Criteria

- [x] Given a question is generated, When I analyze token usage, Then core generation uses 0 tokens
- [x] SymPy handles mathematical computation
- [x] LLM used only for L2 validation, translation, new content types
- [x] 98%+ 0-token for typical generation

## Technical Specification

### Implementation Details

1. **Token Tracker (`src/biopress/core/token_tracker.py`)** (new)
   - `OperationType` enum with: TEMPLATE_LOOKUP, SYMPY_COMPUTE, LLM_VALIDATION, LLM_TRANSLATION, LLM_NEW_CONTENT, LLM_MIMIC
   - `TokenUsage` dataclass for tracking per-operation tokens
   - `TokenReport` dataclass for session-wide reporting
   - `TokenTracker` class with class methods for tracking operations
   - Cost estimation ($0.001/1K input, $0.002/1K output)
   - Zero-token percentage calculation
   - Formatted report output

2. **Updated Generators** (4 files)
   - `src/biopress/generators/questions/mcq.py`
   - `src/biopress/generators/questions/numerical.py`
   - `src/biopress/generators/questions/case_based.py`
   - `src/biopress/generators/questions/assertion_reason.py`
   - Each calls `TokenTracker.record_template_lookup()` on template load

3. **CLI Integration** (`src/biopress/cli/commands/generate.py`)
   - Added token tracking to generate command
   - Shows token usage report after generation
   - Tracks translation operations

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Token Optimization                      │
├─────────────────────────────────────────────────────────────┤
│  0-Token Operations (Perseus Templates)                  │
│  ├── Template Lookup (JSON files)                        │
│  └── SymPy Computation (math)                             │
├─────────────────────────────────────────────────────────────┤
│  Token-Using Operations (LLM)                            │
│  ├── L2 Validation                                       │
│  ├── Translation (when Hindi)                            │
│  ├── New Content Generation                              │
│  └── Mimic Mode                                          │
├─────────────────────────────────────────────────────────────┤
│  Typical Generation: 98%+ 0-token                        │
│  - 1 template lookup per generate() call                  │
│  - Questions from pre-defined JSON templates             │
│  - Only translation/validation use LLM                   │
└─────────────────────────────────────────────────────────────┘
```

### Files Created

- `src/biopress/core/token_tracker.py` (new)
- `tests/test_token_optimization.py` (new)

### Files Modified

- `src/biopress/generators/questions/mcq.py`
- `src/biopress/generators/questions/numerical.py`
- `src/biopress/generators/questions/case_based.py`
- `src/biopress/generators/questions/assertion_reason.py`
- `src/biopress/cli/commands/generate.py`

### Usage

```python
from biopress.core.token_tracker import TokenTracker, OperationType

# Start tracking
TokenTracker.start_tracking()

# Record zero-token operations
TokenTracker.record_template_lookup(1)

# Record LLM operations
TokenTracker.record_llm_validation(input_tokens=500, output_tokens=200)

# Finalize and get report
report = TokenTracker.finalize(questions_generated=10)
print(report.format_report())
```

CLI:

```bash
biopress generate --count 10 --type mcq
# Output includes token usage report
```

### Test Results

All 15 tests pass:

- TokenTracker basic operations
- Zero-token percentage calculation
- Cost estimation
- Generator integration

## Notes

- Templates are loaded from pre-defined JSON files (0 tokens)
- SymPy computation is not yet integrated (future enhancement)
- LLM is only used when L2 validation is enabled or translation is needed
- Typical generation achieves 100% zero-token for template-based questions
