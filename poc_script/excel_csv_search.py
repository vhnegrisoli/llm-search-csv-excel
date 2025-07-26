from langchain_core.messages import SystemMessage, HumanMessage
import pandas as pd
from uuid import uuid4
import os
from dotenv import load_dotenv
from llm import LLMIntegration
from prompts import USER_PROMPT, PANDAS_COMMAND_PROMPT
from pandas_processor import PandasOutputProcessor
from dataframe_info_builder import DataframeInfoBuilder


load_dotenv()


df = pd.read_csv('files/data.csv', encoding='utf-8', delimiter=';')

llm = LLMIntegration()

request = USER_PROMPT
image_id = uuid4()

dataframe_infos = DataframeInfoBuilder(df=df).build_df_info()
prompt = PANDAS_COMMAND_PROMPT.format(image_id, dataframe_infos)

print(f'System prompt: \n{prompt}')
messages = [
    SystemMessage(content=prompt),
    HumanMessage(content=USER_PROMPT)
]

response = llm.call_llm(messages)
content = response.content

processor = PandasOutputProcessor(json_output=content)
processor.process()