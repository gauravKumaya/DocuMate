import os
import shutil
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from backend.app.models.schemas import DocumentUploadResponse
from backend.app.utils import temp_storage
from backend.app.services.pdf_processor import process_pdf
from backend.app.services.pinecone_client import PineconeClient

router = APIRouter()

pincone_client = PineconeClient()  # Initialize once

from fastapi import BackgroundTasks

@router.post("/", response_model=DocumentUploadResponse)
async def upload_file(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    pdf_id = str(uuid.uuid4())
    file_path = temp_storage.get_pdf_path(pdf_id)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Schedule background processing
    background_tasks.add_task(process_and_upsert, file_path, pdf_id)

    return DocumentUploadResponse(pdf_id=pdf_id, message="File uploaded, processing in background")


def process_and_upsert(file_path: str, pdf_id: str):
    text_chunks = process_pdf(file_path)
    pincone_client = PineconeClient()
    pincone_client.upsert_documents(text_chunks, pdf_id)