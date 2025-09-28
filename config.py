import os
from dotenv import load_dotenv

load_dotenv() 

def _csv(name: str, default: str = "") -> list[str]:
    raw = os.getenv(name, default)
    return [x.strip() for x in raw.split(",") if x.strip()]

def _bool(name: str, default: str = "false") -> bool:
    return os.getenv(name, default).strip().lower() in {"1", "true", "yes", "on"}

def _int(name: str, default: str) -> int:
    try:
        return int(os.getenv(name, default).strip())
    except Exception:
        return int(default)

# --- Server Vars ---
APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = _int("APP_PORT", "8080")

# --- CORS Vars ---
CORS_ALLOW_ORIGINS = _csv("CORS_ALLOW_ORIGINS_CSV")
CORS_ALLOW_CREDENTIALS = _bool("CORS_ALLOW_CREDENTIALS", "true")
CORS_ALLOW_METHODS = _csv("CORS_ALLOW_METHODS_CSV") or ["POST", "OPTIONS"]
CORS_ALLOW_HEADERS = _csv("CORS_ALLOW_HEADERS_CSV") or ["*"]

# --- PDF PROCESSING ---
PDF_MAX_FILE_SIZE_MB = _int("PDF_MAX_FILE_SIZE_MB", "30")
PDF_MAX_PAGES = _int("PDF_MAX_PAGES", "5000")
PDF_ALLOW_OCTET_STREAM = _bool("PDF_ALLOW_OCTET_STREAM", "true")
PDF_REJECT_ENCRYPTED = _bool("PDF_REJECT_ENCRYPTED", "true")
PDF_ENABLE_RISKY_MARKER_SCAN = _bool("PDF_ENABLE_RISKY_MARKER_SCAN", "true")
