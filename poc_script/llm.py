from langchain_core.messages.base import BaseMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv
import os


load_dotenv()


class LLMUsageResponse(BaseModel):
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0


class LLMResponse(BaseModel):
    content: str
    usage: Optional[LLMUsageResponse] = None


class LLMIntegration:
    
    def __init__(self):
        self._model = os.getenv('OPENAI_MODEL', '')
        self._key = os.getenv('OPENAI_KEY', '')
        self._llm = ChatOpenAI(
            temperature=0,
            model=os.getenv('OPENAI_MODEL', ''),
            api_key=os.getenv('OPENAI_KEY', '')
        )
    
    def call_llm(self, messages: List[BaseMessage]) -> LLMResponse:
        response = self._llm.invoke(messages)
        content = response.content
        usage = response.response_metadata.get("token_usage", None)
        input = usage.get('prompt_tokens', 0)
        output = usage.get('completion_tokens', 0)
        llm_response = LLMResponse(
            content=content,
            usage=LLMUsageResponse(
                input_tokens=input,
                output_tokens=output,
                total_tokens=input+output
            )
        )
        self._log_response(response=llm_response)
        return llm_response
    
    def _log_response(self, response: LLMResponse) -> None:
        content = response.content
        usage = response.usage
        print(f'LLM response:\n\n{content}\nUsage: ')
        print(f'Input: {usage.input_tokens}')
        print(f'Output: {usage.output_tokens}')
        print(f'Total: {usage.total_tokens}')
