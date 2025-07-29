from typing import TypedDict

class ConventionDocument(TypedDict):
    text: str
    metadata: dict

class RAGResult(TypedDict):
    response: str
    sources: list[ConventionDocument]