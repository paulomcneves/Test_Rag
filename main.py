from fastapi import FastAPI
from api.endpoints import router

app = FastAPI(
    title="RAG API - Single User",
    description="API que responde perguntas com base em contexto local (RAG).",
    version="0.1.0"
)

app.include_router(router)
