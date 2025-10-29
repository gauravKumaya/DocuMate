from app.services.pinecone_client import PineconeClient
from app.services.generator import GeneratorService
from app.services import prompt

class QueryPipeline():
    def __init__(self):
        
        self.pinecone_client = PineconeClient()
        self.generator_service = GeneratorService()

    def run(self, query: str, pdf_id: str):
        """
        Process user query through the pipeline.
        Returns top_k matches from Pinecone.
        """

        retrieved_docs = self.pinecone_client.retrieve_context(text=query, pdf_id=pdf_id)

        context = "\n\n".join(doc.page_content for doc in retrieved_docs)


        response = self.generator_service.genrate_response(
            context=context,
            query=query
        )

        return response





