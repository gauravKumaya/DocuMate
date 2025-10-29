from pinecone import Pinecone, ServerlessSpec
from app.config import config

from langchain.schema import Document
from typing import List

from langchain_pinecone import PineconeVectorStore

from app.services.embedding import EmbeddingService

class PineconeClient:
    def __init__(self, index_name: str = config.PINECONE_INDEX_NAME, api_key: str = config.PINECONE_API_KEY):
        """
        Initialize Pinecone client and index
        """

        self.api_key = api_key
        self.index_name = index_name
        self.pc = Pinecone(api_key=api_key)

        if not self.pc.has_index(index_name):
            self.pc.create_index(
                name=index_name,
                dimension=config.VECTOR_DIMENSTION,
                metric='cosine',
                spec=ServerlessSpec(cloud='aws', region='us-east-1')
            )

        self.index = self.pc.Index(self.index_name)
        
        service = EmbeddingService()
        self.embedding_model = service.get_embedding_model()

    
    def upsert_documents(self, text_chunks: List[Document], pdf_id: str):
        """
        Create the embeddings and upsert it into the vectore store
        """
        
        vector_store =  PineconeVectorStore(
            embedding=self.embedding_model,
            index_name=self.index_name,
            namespace=pdf_id
        )

        vector_store.add_documents(text_chunks)
    

    def retrieve_context(self, text: str, pdf_id: str):

        vector_store = PineconeVectorStore(
            embedding=self.embedding_model,
            index_name=self.index_name,
            namespace=pdf_id
        )

        retriever = vector_store.as_retriever(
            search_type='mmr', 
            search_kwargs={
                'k': config.TOP_K,
                'fetch_k': config.FETCH_K,
                'lambda_mult': config.LAMBDA
            }
        )

        retrieved_docs = retriever.invoke(text)

        return retrieved_docs


    