from io import BytesIO
from fastapi import HTTPException, UploadFile
from starlette.status import HTTP_400_BAD_REQUEST
from pypdf import PdfReader, PdfWriter
import config

MAGIC_HEADER = b"%PDF-"
SUSPICIOUS_PATTERNS = [
    b"/JavaScript", b"/JS", b"/AA", b"/OpenAction", b"/Launch", b"/EmbeddedFile", b"/EmbeddedFiles"
]

ALLOWED_CONTENT_TYPES = {"application/pdf"} | (
    {"application/octet-stream"} if config.PDF_ALLOW_OCTET_STREAM else set()
)

def read_upload_enforcing_limit(upload: UploadFile) -> bytes:
    max_bytes = config.PDF_MAX_FILE_SIZE_MB * 1024 * 1024
    data = b""
    chunk_size = 1024 * 1024
    while True:
        chunk = upload.file.read(chunk_size)
        if not chunk:
            break
        data += chunk
        if len(data) > max_bytes:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=f"File too large; max allowed is {config.PDF_MAX_FILE_SIZE_MB}MB.",
            )
    return data

def basic_pdf_checks(data: bytes, content_type: str | None, filename: str | None) -> None:
    if content_type and content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Unsupported Content-Type.")
    if not data.startswith(MAGIC_HEADER):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Not a valid PDF (bad header).")
    if filename and not filename.lower().endswith(".pdf"):
        pass

def deep_pdf_safety_checks(data: bytes) -> PdfReader:
    bio = BytesIO(data)
    try:
        reader = PdfReader(bio)
    except Exception as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"Failed to parse PDF: {e}")

    if config.PDF_REJECT_ENCRYPTED and getattr(reader, "is_encrypted", False):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Encrypted PDFs are not supported.")

    if config.PDF_ENABLE_RISKY_MARKER_SCAN:
        for pat in SUSPICIOUS_PATTERNS:
            if pat in data:
                raise HTTPException(
                    status_code=HTTP_400_BAD_REQUEST,
                    detail="PDF rejected due to potentially unsafe content (scripts/auto-actions/embedded files).",
                )

    num_pages = len(reader.pages)
    if num_pages == 0 or num_pages > config.PDF_MAX_PAGES:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="PDF has an invalid or excessive page count.")
    return reader

def normalize_range(start: int, end: int, total_pages: int):
    if start is None or end is None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Both page_start and page_end are required.")
    if start < 1 or end < 1:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Page numbers must start at 1.")
    if start > end:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="page_start cannot be greater than page_end.")
    if end > total_pages:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"page_end exceeds document length ({total_pages} pages).",
        )
    return start - 1, end - 1

def extract_pdf_range(reader: PdfReader, start0: int, end0: int):
    writer = PdfWriter()
    for idx in range(start0, end0 + 1):
        writer.add_page(reader.pages[idx])
    out = BytesIO()
    writer.write(out)
    writer.close()
    out.seek(0)
    return out
