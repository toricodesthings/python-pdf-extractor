# 📄 PDF Page Extractor API

## Overview
A small [FastAPI](https://fastapi.tiangolo.com/) service that accepts a PDF, extracts a given page range, and returns a new PDF.  
Built with security in mind: limits file size, rejects encrypted PDFs, and blocks risky features like embedded JavaScript.

---

## 🚀 Features
- Upload a PDF and select page ranges (1-indexed).
- Extracts those pages into a brand-new PDF.
- Configurable via `.env` (CORS, file size, page limits).
- Rejects encrypted PDFs and those with suspicious content.
- Lightweight and container-friendly.

---

## 📦 Installation

Clone this repo, then install dependencies:

```bash
pip install -r requirements.txt
```

Then, rename .env.example to .env and set the your preferred parameters

## Running

Locate API directory then run ```python run.py```

## 📮 POST /extract — Request & Response
```bash
Endpoint
POST /extract
Content-Type: multipart/form-data
```

Form fields (multipart)
Field	Type	Required	Notes
file	File (PDF)	✅	The source PDF.
page_start	Integer (1+)	✅	1-indexed inclusive start page.
page_end	Integer (1+)	✅	1-indexed inclusive end page (must be ≥ page_start).

### Successful response
Status: 200 OK
Headers:
Content-Type: application/pdf
Content-Disposition: attachment; filename="<source>_pages_<start>-<end>.pdf"
Body: PDF bytes (the extracted pages).

### Error response
Status: 4xx (e.g., 400 Bad Request)
Body (JSON):
{ "detail": "Human-readable error message" }


🔒 Security Notes (modifable)
- Large PDFs (> configured MB) are rejected.
- Encrypted PDFs are blocked by default.
- Known risky markers (/JavaScript, /OpenAction, etc.) are rejected.
- Always validate CORS settings before deploying to production.