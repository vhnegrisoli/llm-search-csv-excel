import os
import shutil
from src.utils.file_utils import FileUtils
from src.models.endpoint import UPLOAD_INPUT_DIR
from fastapi import UploadFile, File
from uuid import uuid4

class UploadService:

    def upload(self, file: UploadFile = File(...)) -> dict:
        try:
            extension = FileUtils.get_file_extension(file.filename)
            file_id = str(uuid4())
            file_name = f'{file_id}.{extension}'
            file_path = os.path.join(UPLOAD_INPUT_DIR, file_name)
            
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            return {
                "message": f"File {file_name} uploaded successfully!",
                "file_path": file_path,
                "file_id": file_id
            }
        except Exception as ex:
            return {
                "error": str(ex)
            }
