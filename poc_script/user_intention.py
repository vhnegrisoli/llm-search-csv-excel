from langchain_core.messages import SystemMessage, HumanMessage
from llm import LLMIntegration
from pandas_processor import DataframeType
from prompts import USER_INTENTION_PROMPT


class UserIntention:

    def __init__(self):
        self._llm = LLMIntegration()

    def define_user_input(self, user_input: str) -> DataframeType:
        messages = [
            SystemMessage(content=USER_INTENTION_PROMPT),
            HumanMessage(content=user_input)
        ]
        response = self._llm.call_llm(messages=messages)
        return DataframeType.TEXT if DataframeType.TEXT.value in response.content else DataframeType.IMAGE 
