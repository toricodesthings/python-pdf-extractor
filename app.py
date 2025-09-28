from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

import config
from pdf_utils import (
    read_upload_enforcing_limit,
    basic_pdf_checks,
    deep_pdf_safety_checks,
    normalize_range,
    extract_pdf_range,
)

app = FastAPI(title="PDF Page Extractor", version="0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ALLOW_ORIGINS,
    allow_credentials=config.CORS_ALLOW_CREDENTIALS,
    allow_methods=config.CORS_ALLOW_METHODS,
    allow_headers=config.CORS_ALLOW_HEADERS,
)

@app.post("/extract", summary="Extract a page range from a PDF")
async def extract_pages(
    file: UploadFile = File(..., description="The source PDF file."),
    page_start: int = Form(..., description="1-indexed start page (inclusive)"),
    page_end: int = Form(..., description="1-indexed end page (inclusive)"),
):
    data = read_upload_enforcing_limit(file)
    
    basic_pdf_checks(data, file.content_type, file.filename)
    
    reader = deep_pdf_safety_checks(data)
    
    start0, end0 = normalize_range(page_start, page_end, total_pages=len(reader.pages))
    
    out_buf = extract_pdf_range(reader, start0, end0)

    base = (file.filename or "document.pdf").rsplit(".", 1)[0]
    
    out_name = f"{base}_pages_{page_start}-{page_end}.pdf"

    return StreamingResponse(
        out_buf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{out_name}"',
            "X-Content-Type-Options": "nosniff",
        },
    )

