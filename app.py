from fastapi import FastAPI
from src.routes.search_route import router as search_route

app = FastAPI(
    title="Excel/CSV Search Assistant API",
    description="Assistente que faz pesquisas e gera gráficos em planilhas com LangChain, Pandas e OpenAI.",
    version="1.0.0"
)

app.include_router(rag_router, prefix="/api", tags=["SEARCH"])