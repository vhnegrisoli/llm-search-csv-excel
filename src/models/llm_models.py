from pydantic import BaseModel
from typing import Optional


class LLMUsageResponse(BaseModel):
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0


class LLMResponse(BaseModel):
    content: str
    usage: Optional[LLMUsageResponse] = LLMUsageResponse()
