import pandas as pd
import io
import sys


class DataframeInfoBuilder:

    def __init__(self, df: pd.DataFrame):
        self._df = df

    def build_df_info(self) -> str:
        df_info = self._get_df_info_as_str()
        df_describe = self._df.describe(include='all')
        df_types = self._df.dtypes
        df_unique = self._df.nunique()
        df_nulls = self._df.isnull().sum()

        return f"""
        Dataframe Describe: 
            {df_describe}
        Dataframe Types:
            {df_types}
        Dataframe Nulls:
            {df_nulls}
        Dataframe Unique:
            {df_unique}
        Dataframe Info:
            {df_info}
    """

    def _get_df_info_as_str(self) -> str:
        buffer = io.StringIO()
        self._df.info(buf=buffer)
        return buffer.getvalue()



