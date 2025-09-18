from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.routes import upload, query

app = FastAPI(
    title='DocuMate',
    description="Backend for handling PDF upload and query processing",
    version="1.0.0"
)

# Allow CORS (important for frontend communication)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this later to restrict specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/upload", tags=['upload'])
app.include_router(query.router, prefix="/query", tags=["query"])


# Health check endpoint
@app.get("/")
def root():
    return {"message": "DocuMate API is running!"}