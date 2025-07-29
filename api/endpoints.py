from fastapi import APIRouter
from core.rag import get_rag_response
from api.schemas import QueryRequest, QueryResponse, DocumentResponse

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
async def handle_query(payload: QueryRequest):
    rag_result = get_rag_response(question=payload.text)

    return QueryResponse(
        response=rag_result["response"],
        sources=[
            DocumentResponse(content=src["content"], source=src.get("source", ""))
            for src in rag_result["sources"]
        ]
    )
