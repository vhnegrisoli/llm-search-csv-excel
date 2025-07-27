from langchain_core.messages import SystemMessage, HumanMessage
from src.llm.llm_integration import LLMIntegration
from src.models.llm_models import LLMResponse


class LLMService:

    def __init__(self):
        self._llm = LLMIntegration()

    def call_llm(self, system_prompt: str, user_prompt: str) -> LLMResponse:
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        return self._llm.call_llm(messages=messages)

    def call_llm_system(self, system_prompt: str) -> LLMResponse:
        messages = [
            SystemMessage(content=system_prompt)
        ]
        return self._llm.call_llm(messages=messages)

    def call_llm_llm(self, user_prompt: str) -> LLMResponse:
        messages = [
            HumanMessage(content=user_prompt)
        ]
        return self._llm.call_llm(messages=messages)