import pandas as pd
from uuid import uuid4
import json
from src.utils.file_utils import FileUtils
from src.models.llm_models import LLMUsageResponse
from src.models.endpoint import QueryRequest
from src.models.endpoint import UPLOAD_INPUT_DIR
from src.models.dataframe import PandasResponse, DataframeResponse
from src.llm.prompts import PANDAS_COMMAND_PROMPT
from src.services.pandas_processor_service import PandasProcessorService
from src.services.llm_service import LLMService
from src.services.dataframe_info_service import DataframeInfoService


CSV = 'csv'


class CommandService:

    def __init__(self, request: QueryRequest):
        self._request = request
        self._df = self._create_dataframe()
        self._llm_service = LLMService()
        self._dataframe_info_service = DataframeInfoService(df=self._df)
        self._pandas_processor_service = PandasProcessorService(df=self._df, request=request)

    def _create_dataframe(self) -> pd.DataFrame:
        ext = FileUtils.get_file_extension(self._request.file_name)
        file_path = f'{UPLOAD_INPUT_DIR}/{self._request.file_name}'
        if CSV == ext:
            delimiter = self._request.file_delimiter
            return pd.read_csv(file_path, encoding='utf-8', delimiter=delimiter)
        else:
            return pd.read_excel(file_path, encoding='utf-8')
    
    def create_commands(self) -> dict:
        image_id = str(uuid4())

        dataframe_infos = self._dataframe_info_service.build_df_info()
        prompt = PANDAS_COMMAND_PROMPT.format(image_id, dataframe_infos)

        print(f'System prompt: \n{prompt}')

        response = self._llm_service.call_llm(
            system_prompt=prompt,
            user_prompt=self._request.query
        )

        content = response.content
        df_response = self._parse_output(json_output=content)
        command_usage = response.usage
        
        try:
            pandas_response = self._pandas_processor_service.process(
                df_response=df_response,
                image_id=image_id
            )
        except Exception as ex:
            return self._build_error_output(
                error_msg=str(ex),
                df_response=df_response,
                usage=response.usage
            )

        pandas_usage = pandas_response.llm_response.usage

        return self._build_success_output(
            pandas_response=pandas_response,
            df_response=df_response,
            command_usage=command_usage,
            pandas_usage=pandas_usage
        )

    def _parse_output(self, json_output: str) -> DataframeResponse:
        json_output = json_output.replace('```json', '')
        json_output = json_output.replace('```', '')
        
        self._result = json.loads(json_output)
        return DataframeResponse(**self._result)
    
    def _build_success_output(self,
                              pandas_response: PandasResponse,
                              df_response: DataframeResponse,
                              command_usage: LLMUsageResponse,
                              pandas_usage: LLMUsageResponse) -> dict:
        return {
            'image_path': pandas_response.image_path,
            'pandas_commands': df_response.commands,
            'pandas_output': pandas_response.pandas_output,
            'llm_output': pandas_response.llm_response.content,
            'usage': {
                'input_tokens': command_usage.input_tokens + pandas_usage.input_tokens,
                'output_tokens': command_usage.output_tokens + pandas_usage.output_tokens,
                'total_tokens': command_usage.total_tokens + pandas_usage.total_tokens
            }
        }

    def _build_error_output(self,
                            error_msg: str,
                            df_response: DataframeResponse,
                            usage: LLMUsageResponse) -> dict:
        return {
            'pandas_commands': df_response.commands,
            'error_msg': error_msg,
            'usage': usage.model_dump()
        }