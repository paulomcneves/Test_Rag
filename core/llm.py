from langchain_openai import ChatOpenAI
from core.config import settings

def get_llm():
    return ChatOpenAI(
        model=settings.OPENAI_MODEL,
        temperature=settings.OPENAI_TEMPERATURE,
        max_tokens=settings.OPENAI_MAX_TOKENS,
        openai_api_key=settings.OPENAI_API_KEY,
        # Remova a linha abaixo ou adicione "json" ao seu prompt
        # model_kwargs={"response_format": {"type": "json_object"}}
    )