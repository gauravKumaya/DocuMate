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

@router.post("/", response_model=DocumentUploadResponse)
async def upload_file(file: UploadFile = File(...)):
    # Validate file type
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    # Create a unique PDF ID
    pdf_id = str(uuid.uuid4())

    # Save to temp storage safely
    file_path = temp_storage.get_pdf_path(pdf_id)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    finally:
        await file.close()  # Ensure file is closed

    # Process PDF
    try:
        text_chunks = process_pdf(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")

    # Upsert documents to Pinecone
    try:
        pincone_client.upsert_documents(text_chunks, pdf_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save to Pinecone: {str(e)}")

    return DocumentUploadResponse(pdf_id=pdf_id, message="File uploaded and processed successfully")
