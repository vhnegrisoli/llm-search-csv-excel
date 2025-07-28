from langchain_core.messages.base import BaseMessage
from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain_openai.chat_models.base import BaseChatOpenAI
from typing import List
from dotenv import load_dotenv
import os
from src.models.llm_models import LLMResponse, LLMUsageResponse, LLMProvider


load_dotenv()


class LLMIntegration:

    def __init__(self, provider: LLMProvider):
        self._provider = provider
        self._llm = self._define_llm()

    def _define_llm(self) -> BaseChatOpenAI:
        if LLMProvider.OPENAI == self._provider:
            return self._define_openai()
        else:
            return self._define_azure_openai()

    def _define_openai(self) -> BaseChatOpenAI:
        openai_model = os.getenv('OPENAI_MODEL', '')
        openai_key = os.getenv('OPENAI_KEY', '')

        return ChatOpenAI(
            temperature=0,
            model=openai_model,
            api_key=openai_key
        )

    def _define_azure_openai(self) -> BaseChatOpenAI:
        azure_openai_key = os.getenv('AZURE_OPENAI_KEY', '')
        azure_openai_model = os.getenv('AZURE_OPENAI_MODEL', '')
        azure_openai_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT', '')
        azure_openai_api_version = os.getenv('AZURE_OPENAI_API_VERSION', '')
        
        return AzureChatOpenAI(
            temperature=1,
            deployment_name=azure_openai_model,
            openai_api_key=azure_openai_key,
            azure_endpoint=azure_openai_endpoint,
            openai_api_version=azure_openai_api_version
        )

    def call_llm(self, messages: List[BaseMessage]) -> LLMResponse:
        self._log_input(messages=messages)
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

    def _log_input(self, messages: List[BaseMessage]) -> None:
        print('Calling LLM:')
        for message in messages:
            print(f'{message.type}: {message.content}')

    def _log_response(self, response: LLMResponse) -> None:
        content = response.content
        usage = response.usage
        print(f'LLM response:\n{content}\nUsage: ')
        print(f'Input: {usage.input_tokens}')
        print(f'Output: {usage.output_tokens}')
        print(f'Total: {usage.total_tokens}')
