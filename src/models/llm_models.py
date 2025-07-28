from pydantic import BaseModel
from typing import Optional
from enum import Enum


class LLMUsageResponse(BaseModel):
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0


class LLMResponse(BaseModel):
    content: str
    usage: Optional[LLMUsageResponse] = LLMUsageResponse()


class LLMProvider(Enum):
    OPENAI = "OPENAI"
    AZURE_OPENAI = "AZURE_OPENAI"
