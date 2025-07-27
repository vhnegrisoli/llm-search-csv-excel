from fastapi import APIRouter, status, HTTPException
from src.models.endpoint import QueryRequest
from src.models.llm_models import LLMResponse
from src.services.command_service import CommandService

router = APIRouter()


@router.post("/search")
def search_csv_excel(request: QueryRequest) -> dict:

    service = CommandService(request=request)
    
    try:
        service.create_commands()
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)
        )

    return {'status': 'OK'}
