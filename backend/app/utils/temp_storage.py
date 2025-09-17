import os

# Temp directory for PDF uploads
UPLOAD_DIR = "/tmp/documate_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_pdf_path(pdf_id: str) -> str:
    """Return the full path for a PDF file given its pdf_id"""
    return os.path.join(UPLOAD_DIR, f"{pdf_id}.pdf")
