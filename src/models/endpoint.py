from pydantic import BaseModel


UPLOAD_DIR = 'files'
UPLOAD_INPUT_DIR = 'files/input'
UPLOAD_PLOTS_DIR = 'files/plots'


class QueryRequest(BaseModel):
    query: str
    file_name: str
    file_delimiter: str


class FileUploadResponse(BaseModel):
    file_id: str
    message: str
    file_path: str