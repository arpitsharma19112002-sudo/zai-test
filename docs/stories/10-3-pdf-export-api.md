# Story 10.3: PDF Export API for BioPress Designer

**Epic:** 10. REST API  
**Owner:** Development Team  
**Status:** Done

## Story

As a developer, I want to export PDFs via API, so I can integrate PDF generation into my workflow.

## Acceptance Criteria

- [x] Given API is running with content, When POST to `/api/export` with content and style, Then I receive PDF file download
- [x] PDF follows requested style
- [x] Rate limiting applied per user (10/minute when slowapi available)
- [x] Multipart upload support for larger content
- [x] PDF style options: default, neet, ncert, bilingual, omr

## Technical Specification

### Implementation Details

1. **API Route** (`src/biopress/api/routes/pdf.py`)
   - POST `/api/v1/export` endpoint (multipart/form-data)
   - Accepts JSON content via `content` field OR file upload via `file` field
   - Query/Form parameters: `style`, `title`, `include_answers`
   - Returns PDF file download with proper content-type

2. **Rate Limiting**
   - Uses `slowapi` for rate limiting when available
   - Default limit: 10 requests/minute per IP
   - Gracefully degrades if slowapi not installed

3. **PDF Styles Supported**
   - `default` - Standard BioPress style
   - `neet` - NEET 2-column format
   - `ncert` - NCERT textbook style
   - `bilingual` - English/Hindi format
   - `omr` - OMR-ready format

4. **Data Formats Accepted**
   - JSON with `"items"` array (Perseus format)
   - JSON array of questions
   - Single question object

5. **Tests** (`tests/test_pdf_api.py`)
   - `test_export_pdf_with_content` - JSON content submission
   - `test_export_pdf_with_file` - File upload
   - `test_export_pdf_all_styles` - All style options
   - `test_export_pdf_invalid_style` - Error handling
   - Rate limiting tests

### Usage

```bash
# Export PDF with JSON content
curl -X POST http://localhost:8000/api/v1/export \
  -F "content={\"items\":[...]}" \
  -F "style=neet" \
  -F "title=My Quiz" \
  -o output.pdf

# Export PDF with file upload
curl -X POST http://localhost:8000/api/v1/export \
  -F "file=@quiz.json" \
  -F "style=ncert" \
  -o output.pdf
```

### Response

- Content-Type: `application/pdf`
- Filename: `biopress-{style}-export.pdf`

### Dependencies

```toml
slowapi>=0.1.0  # Optional - for rate limiting
```

If slowapi is not installed, rate limiting is skipped.
