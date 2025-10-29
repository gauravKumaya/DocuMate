from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain\

from app.config import config

from app.services import prompt

config.GENERATOR_MODEL

class GeneratorService:
    def __init__(self, model_name: str = config.GENERATOR_MODEL, api_key: str = config.GOOGLE_API_KEY):
        self.model_name = model_name
        self.api_key = api_key

        self.model = ChatGoogleGenerativeAI(model=model_name, api_key=self.api_key)


    def genrate_response(self, context: str, query: str):
        system_prompt = prompt.system_prompt

        final_prompt = prompt.final_prompt

        final_prompt = final_prompt.format(context=context, query=query)    
        response = self.model.invoke(final_prompt).content

        return response





        
        