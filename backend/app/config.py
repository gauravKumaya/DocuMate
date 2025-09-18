import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT", "us-east-gcp")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    # Pinecone Configuration
    PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "documate")
    VECTOR_DIMENSTION = 1024
    
    # File Processing
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    ALLOWED_FILE_TYPES = [".pdf"]
    TEMP_DIR = "/tmp"
    
    # Embedding Configuration
    EMBEDDING_MODEL = "nvidia/nv-embedqa-e5-v5"
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200

    # Retriever config for mmr
    FETCH_K = 12
    TOP_K = 6
    LAMBDA = 0.7

    # Generator model config
    GENERATOR_MODEL = "gemini-2.5-flash"

    
    # Server Configuration
    HOST = "0.0.0.0"
    PORT = int(os.getenv("PORT", 8000))

config = Config()