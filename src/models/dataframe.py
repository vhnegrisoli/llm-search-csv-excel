from pydantic import BaseModel
from enum import Enum
from typing import List, Optional, Any
from src.models.llm_models import LLMResponse


class DataframeType(Enum):
    TEXT = 'TEXT'
    IMAGE = 'IMAGE'


class DataframeResponse(BaseModel):
    type: DataframeType
    commands: List[str]


class PandasResponse(BaseModel):
    image_path: Optional[str] = None
    pandas_commands: List[str] = []
    pandas_output: Optional[Any] = None
    llm_response: Optional[LLMResponse] = None
