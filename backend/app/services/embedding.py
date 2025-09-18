from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from backend.app.config import config


class EmbeddingService:
    def __init__(self, model_name: str = config.EMBEDDING_MODEL, api_key: str = config.NVIDIA_API_KEY):
        """
        Initialize embedding client 
        """

        self.model_name = model_name
        self.api_key = api_key

        self.client = NVIDIAEmbeddings(
            model=self.model_name,
            truncate='NONE'
        )

    def get_embedding_model(self):
        """
        Return the embedding model client
        """

        return self.client
