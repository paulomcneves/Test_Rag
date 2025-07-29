from pydantic import BaseModel
from typing import List

class QueryRequest(BaseModel):
    text: str

class DocumentResponse(BaseModel):
    content: str
    source: str = ""

class QueryResponse(BaseModel):
    response: str
    sources: List[DocumentResponse]
