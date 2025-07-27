from fastapi import APIRouter, status, HTTPException, UploadFile, File
from src.models.endpoint import FileUploadResponse
from src.services.upload_service import UploadService


router = APIRouter()


@router.post("/upload", response_model=FileUploadResponse)
def upload(file: UploadFile = File(...)) -> dict:

    service = UploadService()
    response = service.upload(file=file)

    if "error" in response:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response["error"]
        )

    return response
