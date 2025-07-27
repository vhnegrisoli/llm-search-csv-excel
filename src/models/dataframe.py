from pydantic import BaseModel
from enum import Enum
from typing import List


class DataframeType(Enum):
    TEXT = 'TEXT'
    IMAGE = 'IMAGE'


class DataframeResponse(BaseModel):
    type: DataframeType
    commands: List[str]
