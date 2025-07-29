from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    OPENAI_TEMPERATURE: float = 0.7
    OPENAI_MAX_TOKENS: int = 1024
    EMBEDDING_MODEL: str = "text-embedding-ada-002"
    CHROMA_PATH: str = str(Path("chroma_db/data").absolute())
    COLLECTION_NAME: str = "convencoes"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()