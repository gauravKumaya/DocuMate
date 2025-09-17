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

@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_file(file: UploadFile = File(...)):
    
    # Validate file type
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only pdf files are allowed")
    
    # create pdf_id
    pdf_id = str(uuid.uuid4())

    # save to temp storage
    file_path = temp_storage.get_pdf_path(pdf_id)
    with open(file_path, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)


    text_chunks = process_pdf(file_path)

    pincone_client = PineconeClient()
    pincone_client.upsert_documents(text_chunks)



