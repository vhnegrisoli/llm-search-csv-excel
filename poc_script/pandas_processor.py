from langchain_core.messages import HumanMessage
from pydantic import BaseModel
from enum import Enum
from typing import List, Optional
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from llm import LLMIntegration
from prompts import USER_PROMPT, PANDAS_OUTPUT_FORMATTER_PROMPT
import json


class DataframeType(Enum):
    TEXT = 'TEXT'
    IMAGE = 'IMAGE'


class DataframeResponse(BaseModel):
    type: DataframeType
    commands: List[str]


class PandasOutputProcessor:

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

        local_vars = {'df': self._df}

        if DataframeType.TEXT == command_type:
            command = commands[0]
            pandas_output = eval(command, {"__builtins__": {}}, local_vars)
            
            print(f'\nPandas output: {pandas_output}\n')

            llm = LLMIntegration()
            user_input = USER_PROMPT
            prompt = PANDAS_OUTPUT_FORMATTER_PROMPT.format(user_input, pandas_output)
            print(f'Format LLM prompt: \n{prompt}\n')
            response = llm.call_llm([HumanMessage(content=prompt)])
            content = response.content
            usage = response.usage
            print(f'LLM response:\n\n{content}\nUsage: \n')
            print(f'Input: {usage.input_tokens}\nOutput: {usage.output_tokens}\nTotal: {usage.total_tokens}\n')
        else:
            for command in commands:
                eval(command, {"__builtins__": {}}, local_vars)


if __name__=="__main__":
    
    df = pd.read_csv('files/data.csv', encoding='utf-8', delimiter=';')
    res_1 = ''
    exec('res_1 = ' + "df[df['MONTH_ID'] == 3][df['YEAR_ID'] == 2004].groupby('PRODUCTLINE')['SALES'].sum().reset_index().to_string(index=False)")
    print(f'Res 1: \n{res_1}')