import ast
from typing import List
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from src.llm.prompts import PANDAS_OUTPUT_FORMATTER_PROMPT
from src.models.llm_models import LLMResponse, LLMUsageResponse
from src.models.endpoint import QueryRequest, UPLOAD_PLOTS_DIR
from src.models.dataframe import DataframeResponse, DataframeType, PandasResponse
from src.services.llm_service import LLMService


class PandasProcessorService:

    def __init__(self, df: pd.DataFrame, request: QueryRequest):
        self._df = df
        self._request = request
        self._llm_service = LLMService(request.provider)
        self._local_vars = {'df': self._df, 'pd': pd, 'plt': plt, 'sns': sns}
        self._result = None
        self._data = None

    def process(self, df_response: DataframeResponse, image_id: str) -> PandasResponse:
        command_type = df_response.type
        commands = df_response.commands

        if DataframeType.TEXT == command_type:
            return self._process_text_output(commands=commands)
        else:
            return self._process_image_output(commands=commands, image_id=image_id)
        
    def _process_text_output(self, commands: List[str]) -> PandasResponse:
        results = []
        for i, command in enumerate(commands, start=1):
            try:
                if self._is_expression(command):
                    result = eval(command, {"__builtins__": {}}, self._local_vars)
                    results.append(f"* Pandas output {i}: {result}")
                else:
                    exec(command, self._local_vars)
            except Exception as ex:
                results.append(f"{command} = ERROR: {ex}")

        pandas_output = "\n\n".join(results)

        print(f'\nPandas output: {pandas_output}\n')

        user_input = self._request.query
        prompt = PANDAS_OUTPUT_FORMATTER_PROMPT.format(user_input, pandas_output)
        llm_response = self._llm_service.call_llm_user(user_prompt=prompt)

        return PandasResponse(
            pandas_commands=commands,
            pandas_output=pandas_output,
            llm_response=llm_response
        )

    def _process_image_output(self, commands: List[str], image_id: str) -> PandasResponse:
        for command in commands:
            exec(command, self._local_vars)
        return PandasResponse(
            pandas_commands=commands,
            image_path=f'{UPLOAD_PLOTS_DIR}/{image_id}.png',
            llm_response=LLMResponse(
                content=''
            )
        )

    def _is_expression(self, command: str) -> bool:
        try:
            parsed = ast.parse(command)
            return isinstance(parsed.body[0], ast.Expr)
        except Exception:
            return False
