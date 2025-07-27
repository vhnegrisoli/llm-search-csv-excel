import io
import sys
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from src.llm.prompts import PANDAS_OUTPUT_FORMATTER_PROMPT
from src.models.llm_models import LLMResponse, LLMUsageResponse
from src.models.endpoint import QueryRequest, UPLOAD_PLOTS_DIR
from src.models.dataframe import DataframeResponse, DataframeType, PandasResponse
from src.services.llm_service import LLMService
import json


class PandasProcessorService:

    def __init__(self, df: pd.DataFrame, request: QueryRequest):
        self._df = df
        self._request = request
        self._llm_service = LLMService()
        self._result = None
        self._data = None

    def _parse_output(self, json_output: str) -> dict:
        json_output = json_output.replace('```json', '')
        json_output = json_output.replace('```', '')
        
        self._result = json.loads(json_output)
        self._data = DataframeResponse(**self._result)
        
    def process(self, json_output: str, image_id: str) -> PandasResponse:
        self._parse_output(json_output=json_output)

        command_type = self._data.type
        commands = self._data.commands

        local_vars = {'df': self._df, 'pd': pd, 'plt': plt, 'sns': sns}

        if DataframeType.TEXT == command_type:
            
            for command in commands:
                buffer = io.StringIO()
                sys_stdout_original = sys.stdout
                sys.stdout = buffer
                try:
                    exec(command, local_vars)
                finally:
                    sys.stdout = sys_stdout_original
                output = buffer.getvalue()
                print("Capturado:", output)

            command = commands[0]
            pandas_output = eval(command, {"__builtins__": {}}, local_vars)
            
            print(f'\nPandas output: {pandas_output}\n')

            user_input = self._request.query
            prompt = PANDAS_OUTPUT_FORMATTER_PROMPT.format(user_input, pandas_output)
            llm_response = self._llm_service.call_llm_user(user_prompt=prompt)

            return PandasResponse(
                pandas_commands=commands,
                pandas_output=pandas_output,
                llm_response=llm_response
            )
        else:
            for command in commands:
                exec(command, local_vars)
            return PandasResponse(
                pandas_commands=commands,
                image_path=f'{UPLOAD_PLOTS_DIR}/{image_id}.png',
                llm_response=LLMResponse(
                    content=''
                )
            )