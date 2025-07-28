from src.services.llm_service import LLMService
from src.models.dataframe import DataframeType
from src.llm.prompts import USER_INTENTION_PROMPT


class UserIntentionService:

    def __init__(self):
        self._llm_service = LLMService()

    def define_user_input(self, user_input: str) -> DataframeType:
        response = self._llm_service.call_llm(
            system_prompt=USER_INTENTION_PROMPT,
            user_prompt=user_input
        )
        return DataframeType.TEXT if DataframeType.TEXT.value in response.content else DataframeType.IMAGE 
