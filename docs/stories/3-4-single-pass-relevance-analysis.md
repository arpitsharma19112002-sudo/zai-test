# Story 3.4: Single-Pass Relevance Analysis

**Epic:** 3. Quality Validation Framework  
**Owner:** Development Team  
**Status:** Done

## Story

As a content creator, I want relevance analysis to run in a single pass without rejection loops, so content generation is fast and efficient.

## Technical Specification

### Implementation Details

1. **Single-Pass Validator (`src/biopress/validators/l2/single_pass.py`)**
   - No rejection loops - single validation call per question
   - Bootstrapped per-exam rules (board, entrance, olympiad)
   - Combined L1+L2 validation in one pass

2. **L2Validator Integration (`src/biopress/validators/l2/validator.py`)**
   - Added `single_pass_mode: bool = False` parameter
   - Single-pass batch validation
   - Full backward compatibility

3. **Exam Rules**
   - board: topics_weight=0.4, difficulty_range=(easy, medium)
   - entrance: topics_weight=0.35, difficulty_range=(medium, hard)
   - olympiad: topics_weight=0.3, difficulty_range=(hard,)

### Files Modified

- `src/biopress/validators/l2/single_pass.py` (new)
- `src/biopress/validators/l2/validator.py` (updated)
- `src/biopress/validators/l2/types.py` (updated)
- `src/biopress/validators/l2/relevance_checker.py` (updated)
- `src/biopress/validators/l2/difficulty_checker.py` (updated)
- `src/biopress/validators/l2/context_checker.py` (updated)
- `src/biopress/validators/l2/__init__.py` (updated)
- `tests/test_l2_validator.py` (updated)

### Usage

```python
from biopress.validators.l2 import L2Validator, create_l2_validator

# Single-pass mode (faster, combined L1+L2)
validator = L2Validator(llm_adapter, single_pass_mode=True)
result = validator.validate(question)

# Traditional mode (legacy compatibility)
validator = create_l2_validator(llm_adapter)
result = validator.validate(question)

# Batch validation
results = validator.validate_batch(questions)
```

### Acceptance Criteria

- [x] Single-pass validation completes without loops
- [x] Exam-specific rules applied correctly
- [x] Combined L1+L2 scoring
- [x] Batch validation supported
- [x] Backward compatible with existing L2Validator
- [x] Tests pass

## Notes

This story enables faster content generation by eliminating the rejection and retry loops in the validation pipeline.
