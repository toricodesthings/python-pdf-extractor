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

## Running

Locate API directory then run ```python run.py```

🔒 Security Notes (modifable)
- Large PDFs (> configured MB) are rejected.
- Encrypted PDFs are blocked by default.
- Known risky markers (/JavaScript, /OpenAction, etc.) are rejected.
- Always validate CORS settings before deploying to production.