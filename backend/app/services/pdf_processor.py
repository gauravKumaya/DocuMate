from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from typing import List
from backend.app.config import config
# from backend.app.utils.logging import logger

def load_pdf(file_path: str) -> List[Document]:
    '''Loads the pdf file in List of Documents'''
    loader = PyPDFLoader(file_path)

    documents = loader.load()
    return documents


def filter_to_minimal_documents(docs: List[Document]) -> List[Document]:
    '''Removes some of the unwanted metadata'''

    minimal_docs = List[Document]

    for doc in docs:
        src = doc.metadata.get('source')
        page = doc.metadata.get('page')

        minimal_docs.append(
            Document(
                page_content=doc.page_content,
                metadata={'src': src, 'page': page}
            )
        )

    return minimal_docs

def text_split(minimal_docs: List[Document]) -> List[Document]:
    '''Splits a text into smaller chunk size'''

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
    )

    text_chunks = text_splitter.split_documents(minimal_docs)

    return text_chunks



def process_pdf(file_path: str) -> List[Document]:
    docs = load_pdf(file_path)

    minimal_docs = filter_to_minimal_documents(docs)

    text_chunks = text_split(minimal_docs)

    return text_chunks

