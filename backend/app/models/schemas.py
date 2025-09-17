from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# ---------- Upload ----------
class DocumentUploadResponse(BaseModel):
    pdf_id: str
    message: Optional[str] = "File uploaded successfully"


# ---------- Query ----------
class QueryRequest(BaseModel):
    pdf_id: str
    query: str

class QueryResponse(BaseModel):
    pdf_id: str
    query: str
    answer: str
    sources: List[dict]
    confidence_score: Optional[float] = None


# ---------- Document Info ----------
class DocumentInfo(BaseModel):
    pdf_id: str
    filename: str
    upload_time: datetime
    chunk_count: int


# ---------- Error ----------
class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None