from pydantic import BaseModel
from src.models.llm_models import LLMUsageResponse, LLMProvider
from typing import Any, Optional, List


UPLOAD_DIR = 'files'
UPLOAD_INPUT_DIR = 'files/input'
UPLOAD_PLOTS_DIR = 'files/plots'


class QueryRequest(BaseModel):
    query: str
    file_name: str
    file_delimiter: str
    provider: Optional[LLMProvider] = LLMProvider.OPENAI


class QueryResponse(BaseModel):
    type: Optional[str] = None
    image_path: Optional[str] = None
    pandas_commands: List[str] = []
    pandas_output: Optional[Any] = None
    llm_output: Optional[str] = None
    usage: Optional[LLMUsageResponse] = None
    error_msg: Optional[str] = None


class FileUploadResponse(BaseModel):
    file_id: str
    message: str
    file_path: str