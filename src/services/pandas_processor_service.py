import io
import sys
from langchain_core.messages import HumanMessage
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from llm import LLMIntegration
from src.llm.prompts import USER_PROMPT, PANDAS_OUTPUT_FORMATTER_PROMPT
from src.models.dataframe import DataframeResponse, DataframeType
import json


class PandasProcessorService:

    def __init__(self, json_output: str):
        self._json_output = self._parse_output(json_output=json_output)
        self._result = json.loads(self._json_output)
        self._data = DataframeResponse(**self._result)
        self._df = pd.read_csv('files/data.csv', encoding='utf-8', delimiter=';')

    def _parse_output(self, json_output: str) -> dict:
        json_output = json_output.replace('```json', '')
        json_output = json_output.replace('```', '')
        return json_output

    def process(self) -> None:
        data = self._data
        
        command_type = data.type
        commands = data.commands

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

            llm = LLMIntegration()
            user_input = USER_PROMPT
            prompt = PANDAS_OUTPUT_FORMATTER_PROMPT.format(user_input, pandas_output)
            llm.call_llm([HumanMessage(content=prompt)])
        else:
            for command in commands:
                exec(command, local_vars)