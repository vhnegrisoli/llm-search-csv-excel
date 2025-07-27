import pandas as pd
from uuid import uuid4
import io
from src.utils.file_utils import FileUtils
from src.models.endpoint import QueryRequest
from src.models.endpoint import UPLOAD_INPUT_DIR
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
    
    def create_commands(self) -> None:
        image_id = uuid4()

        dataframe_infos = self._dataframe_info_service.build_df_info()
        prompt = PANDAS_COMMAND_PROMPT.format(image_id, dataframe_infos)

        print(f'System prompt: \n{prompt}')

        response = self._llm_service.call_llm(
            system_prompt=prompt,
            user_prompt=self._request.query
        )

        content = response.content

        self._pandas_processor_service.process(json_output=content)
