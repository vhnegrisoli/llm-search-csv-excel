from fastapi import APIRouter, status, HTTPException
from src.models.endpoint import QueryRequest
from src.models.llm_models import LLMResponse


router = APIRouter()


@router.post("/search", response_model=LLMResponse)
def query_rag(request: QueryRequest) -> dict:

    service = RagService()
    response = service.query_rag(request=request)

    if "error" in response:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response["error"]
        )

    return response
