# Story 8.2: Diagram Engine OER Sources

**Status:** ✅ Done

**Epic:** Advanced Features

## Implementation Summary

Added search functionality for OER (Open Educational Resource) diagram sources to enhance the diagram sourcing capabilities.

## Changes Made

### 1. Updated `src/biopress/generators/content/diagram_source.py`

- Added `LicenseType` enum with CC BY, CC BY-SA, CC BY-NC, CC BY-NC-SA, CC BY-ND, CC BY-NC-ND, CC0, GPL, MIT, Apache, ODBL options
- Added `License` dataclass for license information
- Added license verification to `DiagramSource.verify_license()` method
- Added `get_source_license()` method to each source

### 2. Implemented OER Sources

- **OpenStaxSource**: CC BY licensed textbook diagrams
- **LibreTextsSource**: CC BY licensed textbook diagrams
- **HyperPhysicsSource**: CC BY-NC-SA licensed physics diagrams
- **ServierSource**: CC BY licensed medical illustrations
- **BioiconsSource**: CC BY licensed biology icons
- **WikimediaSource**: CC BY-SA licensed commons diagrams

### 3. Added License Information

Each source now includes license metadata:

```python
LICENSE = License(
    license_type=LicenseType.CC_BY,
    attribution_required=True,
    commercial_use_allowed=True,
    modifications_allowed=True,
)
```

## Acceptance Criteria

- [x] All 6 diagram sources can be initialized
- [x] Each source has proper license metadata
- [x] License verification available via `verify_license()`
- [x] Sources can be retrieved via `get_default_sources()`

## Files Modified

- `src/biopress/generators/content/diagram_source.py`

## Files Created

- None (existing file updated)

## Tests Added

- None (basic functionality testing via existing test_diagram.py)
