from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.routes.search_route import router as search_route
from src.routes.upload_route import router as upload_route 
from src.models.endpoint import UPLOAD_DIR, UPLOAD_INPUT_DIR, UPLOAD_PLOTS_DIR
import os, shutil



app = FastAPI(
    title="Excel/CSV Search Assistant API",
    description="Assistente que faz pesquisas e gera gráficos em planilhas com LangChain, Pandas e OpenAI.",
    version="1.0.0"
)

def clean_up():
    if os.path.exists(UPLOAD_DIR):
        shutil.rmtree(UPLOAD_DIR)
    create_dirs()

def create_dirs():
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    os.makedirs(UPLOAD_INPUT_DIR, exist_ok=True)
    os.makedirs(UPLOAD_PLOTS_DIR, exist_ok=True)


clean_up()

app.include_router(search_route, prefix="/api", tags=["SEARCH"])
app.include_router(upload_route, prefix="/api", tags=["UPLOAD"])

app.mount("/files", StaticFiles(directory="files"), name="files")