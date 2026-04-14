"""PDF export API route."""

import json
import os
import tempfile
from typing import Optional

from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Request
from fastapi.responses import FileResponse
from fastapi.background import BackgroundTask

from biopress.api.models.schemas import PDFRequest, PDFResponse
from biopress.pdf.builder import PDFBuilder

router = APIRouter()

VALID_STYLES = ["default", "ncert", "neet", "bilingual", "omr"]

limiter = None
try:
    from slowapi import Limiter
    from slowapi.util import get_remote_address
    limiter = Limiter(key_func=get_remote_address)
except ImportError:
    pass


async def _export_pdf_impl(
    content: Optional[str],
    style: str,
    title: Optional[str],
    include_answers: bool,
    file: Optional[UploadFile],
):
    """Implementation of PDF export."""
    if style not in VALID_STYLES:
        raise HTTPException(status_code=400, detail=f"Invalid style. Valid: {VALID_STYLES}")

    try:
        quiz_data = []

        if file:
            content_bytes = await file.read()
            try:
                data = json.loads(content_bytes.decode("utf-8"))
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="Invalid JSON in uploaded file")

            if "items" in data:
                quiz_data = data["items"]
            elif isinstance(data, list):
                quiz_data = data
            else:
                quiz_data = [data]
        elif content:
            try:
                data = json.loads(content)
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="Invalid JSON in content field")

            if "items" in data:
                quiz_data = data["items"]
            elif isinstance(data, list):
                quiz_data = data
            else:
                quiz_data = [data]
        else:
            raise HTTPException(status_code=400, detail="Either content or file must be provided")

        if not quiz_data:
            raise HTTPException(status_code=400, detail="No questions provided")

        builder = PDFBuilder(style=style)

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            output_path = tmp.name

        builder.build_from_data(
            quiz_data,
            output_path,
            style=style,
            title=title,
            include_answers=include_answers,
        )

        return FileResponse(
            output_path,
            media_type="application/pdf",
            filename=f"biopress-{style}-export.pdf",
            background=BackgroundTask(os.unlink, output_path),
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")


if limiter:
    @router.post("/export")
    @limiter.limit("10/minute")
    async def export_pdf(
        request: Request,
        content: Optional[str] = Form(default=None),
        style: str = Form(default="default"),
        title: Optional[str] = Form(default=None),
        include_answers: bool = Form(default=True),
        file: Optional[UploadFile] = File(default=None),
    ):
        """Export PDF from content via API with rate limiting (10/min)."""
        return await _export_pdf_impl(content, style, title, include_answers, file)
else:
    @router.post("/export")
    async def export_pdf(
        content: Optional[str] = Form(default=None),
        style: str = Form(default="default"),
        title: Optional[str] = Form(default=None),
        include_answers: bool = Form(default=True),
        file: Optional[UploadFile] = File(default=None),
    ):
        """Export PDF from content via API with style options."""
        return await _export_pdf_impl(content, style, title, include_answers, file)


@router.post("/pdf", response_model=PDFResponse)
async def generate_pdf(request: PDFRequest):
    """Generate PDF from questions via API."""
    if request.style not in VALID_STYLES:
        raise HTTPException(status_code=400, detail=f"Invalid style. Valid: {VALID_STYLES}")

    try:
        builder = PDFBuilder()
        
        quiz_data = []
        for q in request.questions:
            quiz_data.append({
                "id": q.id,
                "question": q.question,
                "options": q.options or [],
                "correct_answer": q.correct_answer,
                "explanation": q.explanation,
            })

        style_name = request.style
        
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            output_path = tmp.name

        builder.build_from_data(
            quiz_data,
            output_path,
            style=style_name,
            title=request.title,
            include_answers=request.include_answers,
        )

        return PDFResponse(
            status="success",
            message=f"PDF generated with {len(request.questions)} questions",
            file_path=output_path,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")