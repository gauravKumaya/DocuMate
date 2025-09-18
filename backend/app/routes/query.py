from fastapi import APIRouter, HTTPException

from backend.app.models.schemas import QueryRequest, QueryResponse
from backend.app.pipelines.query_pipeline import QueryPipeline


router = APIRouter()


@router.post("/", response_model=QueryResponse)
async def query_document(request: QueryRequest):
    """
    Handle user query against uploaded document
    """

    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    query_pipeline = QueryPipeline()

    query = request.query
    pdf_id = request.pdf_id
    response = query_pipeline.run(query=query, pdf_id=pdf_id)

    return QueryResponse(
        pdf_id=pdf_id,
        query=query,
        answer=response,
    )