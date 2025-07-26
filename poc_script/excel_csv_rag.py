from langchain_core.messages import SystemMessage, HumanMessage
import pandas as pd
from uuid import uuid4
import os
from dotenv import load_dotenv
from llm import LLMIntegration
from prompts import USER_PROMPT, PANDAS_COMMAND_PROMPT
from pandas_processor import PandasOutputProcessor


load_dotenv()


df = pd.read_csv('files/data.csv', encoding='utf-8', delimiter=';')

llm = LLMIntegration()

df_info = df.info()
df_describe = df.describe()
request = USER_PROMPT
image_id = uuid4()
prompt = PANDAS_COMMAND_PROMPT.format(image_id, df_info, df_describe)

messages = [
    SystemMessage(content=prompt),
    HumanMessage(content=USER_PROMPT)
]

response = llm.call_llm(messages)
content = response.content
usage = response.usage

print(f'LLM response:\n\n{content}\nUsage: \n')
print(f'Input: {usage.input_tokens}\nOutput: {usage.output_tokens}\nTotal: {usage.total_tokens}\n')

processor = PandasOutputProcessor(json_output=content)
processor.process()